#!/usr/bin/env python3
"""Compatibility entry point for the CV sorter."""

from pathlib import Path
import sys

SRC = Path(__file__).resolve().parent / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from cv_sorter.app import run


if __name__ == "__main__":
    run()
