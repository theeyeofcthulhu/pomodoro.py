# pomodoro.py

A script which runs timers for a [Pomodoro Technique](https://en.wikipedia.org/wiki/Pomodoro_Technique) workflow.

## Operation

By default, the timers work by sleeping ten seconds at a time until a timer is over, and the script then uses [notify-send](https://gitlab.gnome.org/GNOME/libnotify/) to send a corresponding message, which you have to dismiss before the next timer starts (on my KDE Plasma system the message sent via the parameters in the script stays indefinitely). If the message is not dismissed for more ten seconds (or the configured timer interval), the number of intervals the timer was extended by through not dismissing the message is printed out and added to the totals.

## Usage

Ran without any arguments and the default config, the script switches between 25-minute work and five-minute pause timers, but every fourth pause timer is four times that length, 20 minutes.

All of these parameters can be supplied via the command line, and their default values can also be changed.

### Command line arguments:

1. Work timer length
2. Pause timer length
3. Frequency of long pauses (set to zero for no long pauses)
4. Length of long pauses (as a multiplier of short pauses)

So

```
python pomodoro.py 8 4 3 5
```

alternates between eight-minute work timers and four-minute pause timers, but every third pause is 20 minutes long. Any argument not supplied is replaced with the default.

### Config

Copy `config_default.py` into `config.py` and input your preferred values. The script will then load `config.py` instead of `config_default.py`

The program can be exited by pressing Ctrl+C.

## Controlling a Running Process

If it becomes necessary to change a timer currently running or to skip a few timers, use the link to `script.py` that was put into your `/tmp/` directory when you started the program. It's called `/tmp/pomodoro-skip-PID.py` with PID being the process ID of the running `pomodoro.py`. If you are only running one timer at a time, as intended, you can easily get to your script by shell autocomplete. If not, you can find out the PID belonging to any process by pressing Ctrl+Z to pause it, running `jobs -p` to get the PID, and then `fg` to resume it. The link is deleted when the program exits.

Here's how the `skip.py` script works.

1. `skip.py`: skips the current timer
2. `skip.py 3`: skips the current timer and the next two
3. `skip.py +4`: adds four minutes to the current timer
4. `skip.py -5`: removes five minutes from the current timer
