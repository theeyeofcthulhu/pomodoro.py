#!/usr/bin/python

import os
import signal
import sys

def fifo_filename(pid):
    return f'/tmp/pomodoro-fifo-{pid}'

if __name__ == '__main__':
    pid = int(sys.argv[1])

    times = 1
    rewind = False
    if len(sys.argv) > 2:
        if sys.argv[2].startswith('+') or sys.argv[2].startswith('-'):
            rewind = True
        times = int(sys.argv[2])

    fn = fifo_filename(pid)

    if os.path.exists(fn):
        assert False, f'FIFO has already been opened'

    os.mkfifo(fn) 

    # tell process to read the FIFO for its own PID
    os.kill(pid, signal.SIGUSR1)

    with open(fn, 'w') as fifo:
        fifo.write(f'{'r' if rewind else ''}{times}')
