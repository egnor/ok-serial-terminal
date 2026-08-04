"""
An interactive serial port terminal built on
[ok-serial](https://github.com/egnor/ok-py-serial#readme).
This package is a CLI utility (`okterm`), not a library.
"""

import importlib.metadata

# the distribution name ("ok-serial-terminal") differs from the module name
__version__ = importlib.metadata.version("ok-serial-terminal")
