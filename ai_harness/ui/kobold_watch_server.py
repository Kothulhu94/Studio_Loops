#!/usr/bin/env python3
"""Compatibility entrypoint for Loop_Central."""

from __future__ import annotations

import sys
from pathlib import Path


sys.path.insert(0, str(Path(__file__).resolve().parent))

from loop_central_server import *  # noqa: F401,F403,E402
from loop_central_server import main  # noqa: E402


if __name__ == "__main__":
    sys.exit(main())
