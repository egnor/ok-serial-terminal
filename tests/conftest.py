import ok_logging_setup

_log_setup = {"LEVEL": "ok_serial_terminal=DEBUG,WARNING", "OUTPUT": "stdout"}
ok_logging_setup.install({f"OK_LOGGING_{k}": v for k, v in _log_setup.items()})
