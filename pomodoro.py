#!/usr/bin/python3

from enum import Enum
import subprocess
import sys
import time

class Mode(Enum):
    LEARN = 1
    PAUSE = 2

def toggle_mode(mode):
    if mode == Mode.LEARN:
        return Mode.PAUSE
    elif mode == Mode.PAUSE:
        return Mode.LEARN
    else:
        print("toggle_mode: faulty input")
        exit(1)

def erase_line():
    sys.stdout.write('\x1b[1A') # move up
    sys.stdout.write('\x1b[2K') # clear line
    sys.stdout.flush()

def minutes_and_seconds(s):
    return f'{s//60}:{s%60:02}'

LEARN_TIMER_DEFAULT = 25 * 60
PAUSE_TIMER_DEFAULT = 5 * 60
LONG_PAUSE_FREQ_DEFAULT = 4
LONG_PAUSE_MULTIPLIER_DEFAULT = 4

timer_interval = 10

msgs = { Mode.LEARN: "Learn timer over",
         Mode.PAUSE: "Pause timer over" }

if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'dbg':
        timer_durations = { Mode.LEARN: 3,
                            Mode.PAUSE: 2 }
        timer_interval = 1
        long_pause_freq = 3
        long_pause_multiplier = 2
    else:
        timer_durations = { Mode.LEARN: int(sys.argv[1]) * 60 if len(sys.argv) >= 2
                            else LEARN_TIMER_DEFAULT,
                            Mode.PAUSE: int(sys.argv[2]) * 60 if len(sys.argv) >= 3
                            else PAUSE_TIMER_DEFAULT }
        long_pause_freq = int(sys.argv[3]) if len(sys.argv) >= 4 else LONG_PAUSE_FREQ_DEFAULT
        long_pause_multiplier = int(sys.argv[4]) if len(sys.argv) >= 5 else LONG_PAUSE_MULTIPLIER_DEFAULT

    print(f'Starting cycle of {minutes_and_seconds(timer_durations[Mode.LEARN])} long work blocks, {minutes_and_seconds(timer_durations[Mode.PAUSE])} long pause blocks')
    if long_pause_freq > 0:
        print(f'After every {long_pause_freq} work blocks, the pause will instead be {minutes_and_seconds(timer_durations[Mode.PAUSE] * long_pause_multiplier)} long')

    cycles = 0
    mode = Mode.LEARN
    while True:
        timer = timer_durations[mode]

        if long_pause_freq > 0:
            if cycles > 0 and cycles % long_pause_freq == 0 and mode == Mode.PAUSE:
                timer = timer * long_pause_multiplier
            elif mode == Mode.LEARN:
                cycles = cycles + 1

        print(f'Started timer for {minutes_and_seconds(timer)}', end='\n')
        print(f'Remaining: {minutes_and_seconds(timer)}')
        while timer > 0:
            time.sleep(timer_interval)
            timer = timer - timer_interval
            erase_line()
            print(f'Remaining: {minutes_and_seconds(timer)}')

        subprocess.run(["notify-send", "-a", "pomodoro timer", "-w", "-t", "0", msgs[mode]])

        mode = toggle_mode(mode)
