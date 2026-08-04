# OK serial terminal &nbsp; ⌨️〡🔌〡〇〡〇

An interactive [serial port](https://en.wikipedia.org/wiki/Serial_port) terminal for Python users, built on [ok-serial](https://github.com/egnor/ok-py-serial#readme).

Think twice before using this! Consider something more established:

- [tio](https://github.com/tio/tio) - not Python, but a great serial terminal utility
- [picocom](https://github.com/npat-efault/picocom) - the classic minimal serial terminal
- [screen](https://www.gnu.org/software/screen/) - the terminal multiplexer is also a serial terminal
- [minicom](https://salsa.debian.org/minicom-team/minicom) - if you're nostalgic for the DOS era
- [pyserial's miniterm](https://pyserial.readthedocs.io/en/latest/tools.html#module-serial.tools.miniterm) - `python -m serial.tools.miniterm`, already installed if you have pyserial

## Installation

```bash
pip install ok-serial-terminal
```

(or `uv add ok-serial-terminal`, `uv tool install ok-serial-terminal`, etc.)

To try it without installing anything, `uvx ok-serial-terminal <port> [baud]` (or `pipx run ok-serial-terminal ...`). The command is installed under both `okterm` and the longer `ok-serial-terminal`; they're the same program.

## Usage

```bash
okterm <port> [baud]
```

For example, `okterm MyDevice 115200`. The baud rate defaults to 115200 if
omitted. The port is an [ok-serial match expression](https://github.com/egnor/ok-py-serial#port-matching), so `okterm RP2040`, `okterm 2e8a:0005`, and `okterm /dev/ttyACM0` all work. Run [`okserial`](https://github.com/egnor/ok-py-serial#readme) (from the `ok-serial` package) to see which ports are visible and what attributes they have.

Once connected, ctrl-`]` opens a menu and ctrl-`\` quits.

Options (see `okterm --help`):

- `--plain` / `-p` - plain passthrough, no status decorations
- `--reconnect` / `-r` - reconnect automatically if the port goes away
- `--scan-time` / `-s SECONDS` - keep scanning this long for a matching port
- `--oblivious` / `--polite` / `--exclusive` / `--stomp` - [port sharing mode](https://github.com/egnor/ok-py-serial#sharing-modes) (default `--exclusive`)

Unless `--plain` is given (or stdin/stdout aren't the same terminal), `okterm` decorates the display with connection status, control signal state, and an indicator for typed characters the device hasn't echoed back.

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

None of this is `okterm`-specific — as far as [ok-serial](https://github.com/egnor/ok-py-serial#readme) is concerned `./socat.tmp` is just another serial port, so `ok_serial.SerialConnection(match="socat.tmp", baud=115200)` works the same way from your own code.

Working in a checkout of this repo, `mise run socat-run` and `mise run socat-ab` wrap the two arrangements above (a program on a pty, and a pair of connected ptys).
