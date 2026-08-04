# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Build & Development Commands

This project uses mise for tool/script management.

```bash
# Install tools and sync dependencies
mise install

# Run all checks (ruff, mypy, pytest)
mise run check

# Run tests only
uv run pytest

# Run a single test file
uv run pytest tests/test_chunker.py

# Run a specific test
uv run pytest tests/test_keyboard.py::test_kitty_key_reports
```

## Architecture

**ok-serial-terminal** provides `okterm`, an interactive serial terminal built on
the [ok-serial](https://github.com/egnor/ok-py-serial) library. The `ok_terminal`
package is a CLI utility, not a library; nothing here is meant to be imported by
other projects.

### Core Components

- **`main.py`**: the `okterm` click command plus `_TerminalSession`, the asyncio
  event loop that shuttles data between stdin/stdout and a
  `ok_serial.SerialConnectionMonitor`. Runs one task for the serial monitor, one
  for stdin, and a main loop that renders output.

- **`chunker.py`**: `TerminalChunker` - splits a byte stream into chunks
  (escape sequences, text runs) using timing to disambiguate

- **`keyboard.py`**: `chunk_to_key_event()` - maps input chunks to
  `TerminalKeyEvent` (named key + modifiers)

- **`decorator.py`**: `TerminalDecorator` - the "fancy" display layer, adding
  status lines above the serial output and an unechoed-input indicator to the
  right; falls back to plain passthrough with `--plain`

- **`mode_tracker.py`**: `TerminalModeTracker` - tracks terminal state (alternate
  screen, cursor keys, mouse reporting, etc.) from the escape sequences flowing
  through, so the decorator knows what it can safely do

- **`async_stdio.py`**: `AsyncReader`/`AsyncWriter` and `raw_tty_context()` -
  nonblocking asyncio I/O on stdin/stdout, and raw-mode setup

- **`timeout_math.py`**: `to_deadline()`/`from_deadline()` timeout helpers
  (a copy of the same helpers in `ok_serial`)

### Testing

Tests use pseudo-TTYs (`pty.openpty()`) to exercise terminal I/O without a real
terminal. There is no serial hardware or port in the tests; the serial side is
`ok_serial`'s business.

For manual testing against a fake serial port, `mise run socat-run` puts a
program (default `$SHELL`) on a pty at `./socat.run.tmp`, and `mise run
socat-ab` connects a pair of ptys at `./socat.a.tmp` and `./socat.b.tmp`. Both
need [socat](http://www.dest-unreach.org/socat/) installed. Then
`uv run okterm socat.run.tmp`.
