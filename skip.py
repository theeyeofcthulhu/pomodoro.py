#!/usr/bin/python

import os
import re
import signal
import sys

def fifo_filename(pid):
    return f'/tmp/pomodoro-fifo-{pid}'

if __name__ == '__main__':
    # pid is encoded in file name when this script is softlinked into /tmp/
    match = re.search(r'\d{6}', sys.argv[0])
    if match:
        pid = int(match.group())
    else:
        print('No PID encoded in file name')
        sys.exit(1)

    times = 1
    rewind = False
    if len(sys.argv) > 1:
        if sys.argv[1].startswith('+') or sys.argv[1].startswith('-'):
            rewind = True
        times = int(sys.argv[1])

    fn = fifo_filename(pid)

    assert not os.path.exists(fn), 'FIFO has already been opened'

    os.mkfifo(fn) 

    # tell process to read the FIFO for its own PID
    os.kill(pid, signal.SIGUSR1)

    with open(fn, 'w') as fifo:
        fifo.write(f'{'r' if rewind else ''}{times}')
