# pomodoro.py

A script which runs timers for a [Pomodoro Technique](https://en.wikipedia.org/wiki/Pomodoro_Technique) workflow.

## Operation

The timers work by sleeping ten (but feel free to change this parameter in the script) seconds at a time until a timer is over, and the script then uses [notify-send](https://gitlab.gnome.org/GNOME/libnotify/) to send a corresponding message, which you have to dismiss before the next timer starts (on my KDE Plasma system the message sent via the parameters in the script stays indefinitely).

## Usage

Ran without any arguments, the script switches between 25-minute work and five-minute pause timers, but every fourth pause timer is four times that length, 20 minutes.

All of these parameters can be supplied via the command line.

**Command line arguments:**

1. Work timer length
2. Pause timer length
3. Frequency of long pauses (set to zero for no long pauses)
4. Length of long pauses (as a multiplier of short pauses)

So

```
python pomodoro.py 8 4 3 5
```

alternates between eight-minute work timers and four-minute pause timers, but every third pause is 20 minutes long. Any argument not supplied is replaced with the default.

The program can be exited by pressing Ctrl+C.

## Controlling a Running Process

If it becomes necessary to change a timer currently running or to skip a few timers, use the `skip.py` script.

The main script prints its PID at the top. Use that to invoke `skip.py`:

1. `skip.py PID`: skips the current timer
2. `skip.py PID 3`: skips the current timer and the next two
3. `skip.py PID +4`: adds four minutes to the current timer
4. `skip.py PID -5`: removes five minutes from the current timer
