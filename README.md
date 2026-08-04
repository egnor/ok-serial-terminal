# OK serial terminal &nbsp; 🔌〡〇〡〇〡💻

An interactive [serial port](https://en.wikipedia.org/wiki/Serial_port) terminal, built on [ok-serial](https://github.com/egnor/ok-py-serial#readme).

Think twice before using this! Consider something more established:

- [tio](https://github.com/tio/tio) - not Python, but a great serial terminal utility
- [picocom](https://github.com/npat-efault/picocom) - the classic minimal serial terminal
- [screen](https://www.gnu.org/software/screen/) - the terminal multiplexer is also a serial terminal
- [minicom](https://salsa.debian.org/minicom-team/minicom) - if you're nostalgic for the DOS era
- [pyserial's miniterm](https://pyserial.readthedocs.io/en/latest/tools.html#module-serial.tools.miniterm) - `python -m serial.tools.miniterm`, already installed if you have pyserial

## Installation and Usage

Install the Python package, which installs the `okterm` utility:

```sh
pip install ok-serial-terminal
# or 'uv add ok-serial-terminal', 'uv tool install ok-serial-terminal', etc.
okterm <port> [baud]
```

OR, skip the package install and run it directly with [uvx](https://docs.astral.sh/uv/guides/tools/) or [pipx](https://pipx.pypa.io/stable/):

```sh
uvx ok-serial-terminal <port> [baud]
# or `pipx run ok-serial-terminal <port> [baud]`
```

The baud rate defaults to 115200 if omitted. The port is an [ok-serial match expression](https://github.com/egnor/ok-py-serial#port-matching), so `okterm RP2040`, `okterm 2e8a:0005`, and `okterm /dev/ttyACM0` all work. Run [`okserial`](https://github.com/egnor/ok-py-serial#readme) (or `uvx ok-serial`, etc.) to list visible ports and their attributes.

On a terminal (unless `--plain` is given), `okterm` decorates the display with connection status, control signal state, and an indicator for unechoed typed characters. In this mode, ctrl-`]` opens a menu and ctrl-`\` quits.

In plain mode (I/O redirected or `--plain` given), data is pass-through and ^C quits.

See `okterm --help` for more options (locking mode, etc).

## Socat for testing and profit

On Unix-ish systems, [socat](http://www.dest-unreach.org/socat/) is handy for connecting serial-port apps (`okterm` or otherwise) to non-serial endpoints (like a Unix program or a TCP socket). Install it with your favorite package manager (eg. `sudo apt install socat`), and run something like this in one window:

```sh
socat pty,raw,echo=0,link=socat.tmp exec:$SHELL,pty,stderr,setsid,ctty
```

The first socat argument `pty,raw,echo=0,link=socat.tmp` allocates a pseudoterminal (pty) that looks like a serial port, and creates a `./socat.tmp` symlink to the device. The `,raw,echo=0` suppresses default pty echo behavior to avoid the shell looping on its own output.

The second socat argument starts a shell on its own pty, but this could be any socat endpoint (`exec:cat`, `tcp:localhost:8000`, etc).

Socat will then shuffle data between the two points. Try this in another window (in the same directory):

```sh
okterm socat.tmp
```

You should get a terminal connected to the pty socat allocated; hit enter and you should see a shell prompt.

(None of this is `okterm`-specific — as far as [ok-serial](https://github.com/egnor/ok-py-serial#readme) is concerned `./socat.tmp` is just another serial port, so `ok_serial.SerialConnection(match="socat.tmp", baud=115200)` works the same way from your own code.)
