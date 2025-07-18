#!/usr/bin/python3

from enum import Enum
import os
import subprocess
import signal
import sys
import time

from skip import fifo_filename

class Mode(Enum):
    WORK = 1
    PAUSE = 2

def toggle_mode(mode):
    assert mode == Mode.WORK or mode == Mode.PAUSE
    if mode == Mode.WORK:
        return Mode.PAUSE
    elif mode == Mode.PAUSE:
        return Mode.WORK

def erase_line():
    sys.stdout.write('\x1b[1A') # move up
    sys.stdout.write('\x1b[2K') # clear line
    sys.stdout.flush()

def minutes_and_seconds(s):
    negative = False
    if s < 0:
        negative = True
        s = -s
    return f'{'-' if negative else ''}{s//60}:{s%60:02}'

def sigint_handler(signum, frame):
    print(f'Worked for {minutes_and_seconds(global_counters[Mode.WORK])}; paused for {minutes_and_seconds(global_counters[Mode.PAUSE])}')
    sys.exit(0)

def sigusr1_handler(signum, frame):
    global skip_stack, rewind
    fn = fifo_filename(os.getpid())
    with open(fn, 'r') as fifo:
        read = fifo.read()
        if read.startswith('r'):
            rewind = int(read[1:])
        else:
            skip_stack += int(read)
    os.remove(fn)

rewind = 0
skip_stack = 0

WORK_TIMER_DEFAULT = 25 * 60
PAUSE_TIMER_DEFAULT = 5 * 60
LONG_PAUSE_FREQ_DEFAULT = 4
LONG_PAUSE_MULTIPLIER_DEFAULT = 4

timer_interval = 10

msgs = { Mode.WORK: "Work timer over",
         Mode.PAUSE: "Pause timer over" }

global_counters = { Mode.WORK: 0, Mode.PAUSE: 0 }

if __name__ == '__main__':
    signal.signal(signal.SIGINT, sigint_handler)
    signal.signal(signal.SIGUSR1, sigusr1_handler)

    if len(sys.argv) > 1 and sys.argv[1] == 'dbg':
        timer_durations = { Mode.WORK: 3,
                            Mode.PAUSE: 2 }
        timer_interval = 1
        long_pause_freq = 3
        long_pause_multiplier = 2
    else:
        timer_durations = { Mode.WORK: int(sys.argv[1]) * 60 if len(sys.argv) >= 2
                            else WORK_TIMER_DEFAULT,
                            Mode.PAUSE: int(sys.argv[2]) * 60 if len(sys.argv) >= 3
                            else PAUSE_TIMER_DEFAULT }
        long_pause_freq = int(sys.argv[3]) if len(sys.argv) >= 4 else LONG_PAUSE_FREQ_DEFAULT
        long_pause_multiplier = int(sys.argv[4]) if len(sys.argv) >= 5 else LONG_PAUSE_MULTIPLIER_DEFAULT

    print(f'[{os.getpid()}]')
    print(f'Starting cycle of {minutes_and_seconds(timer_durations[Mode.WORK])} long work blocks, {minutes_and_seconds(timer_durations[Mode.PAUSE])} long pause blocks')
    if long_pause_freq > 0:
        print(f'After every {long_pause_freq} work blocks the pause will instead be {minutes_and_seconds(timer_durations[Mode.PAUSE] * long_pause_multiplier)} long')

    cycles = 0
    mode = Mode.WORK
    while True:
        skipped = False

        timer = timer_durations[mode]

        if long_pause_freq > 0:
            if mode == Mode.PAUSE and cycles % long_pause_freq == 0:
                timer *= long_pause_multiplier
            elif mode == Mode.WORK:
                cycles += 1

        print(f'Started timer for {minutes_and_seconds(timer)}')

        if skip_stack > 0:
            timer = 0
            skip_stack -= 1
            skipped = True

        print(f'Remaining: {minutes_and_seconds(timer)}{'… skipped' if skipped else ''}')
        while timer > 0:
            time.sleep(timer_interval)

            erase_line()

            # skip_stack and rewind are set via IPC,
            # see sigusr1_handler() and skip.py
            if skip_stack > 0:
                print(f'Remaining: {minutes_and_seconds(timer)}… skipped')

                skipped = True
                skip_stack -= 1
                timer = 0
            elif rewind != 0:
                # user rewinds n minutes
                net_change = rewind * 60
                timer += net_change

                print(f'Remaining: {minutes_and_seconds(timer)}… rewound {minutes_and_seconds(net_change)}')

                rewind = 0
            else:
                timer -= timer_interval
                global_counters[mode] += timer_interval

                print(f'Remaining: {minutes_and_seconds(timer)}')

        if not skipped:
            subprocess.run(["notify-send", "-a", "pomodoro timer", "-w", "-t", "0", msgs[mode]])

        mode = toggle_mode(mode)
