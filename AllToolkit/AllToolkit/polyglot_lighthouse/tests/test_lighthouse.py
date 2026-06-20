#!/usr/bin/env python3
"""
Pytest-compatible test entry for polyglot_lighthouse.

This file invokes the module's built-in `run_tests()` so the same 157
self-checks are available via both:

  * python3 __main__.py --test
  * pytest tests/test_lighthouse.py
"""

import os
import sys

# Make the parent package importable when running pytest from the
# AllToolkit/AllToolkit directory.
HERE = os.path.dirname(os.path.abspath(__file__))
PKG_PARENT = os.path.dirname(os.path.dirname(HERE))
if PKG_PARENT not in sys.path:
    sys.path.insert(0, PKG_PARENT)

from polyglot_lighthouse import run_tests  # noqa: E402


def test_polyglot_lighthouse_suite() -> None:
    """Run the module's built-in 157-check self-test suite.

    run_tests() raises SystemExit(1) on any failure, which pytest will
    surface as a failed test. On success it prints a green summary.
    """
    run_tests()