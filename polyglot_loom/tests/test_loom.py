#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
pytest wrapper for polyglot_loom self-tests.

The module ships its own test runner via `python -m polyglot_loom --test`.
This file wraps it as a pytest-compatible test case for CI / discovery.
"""

import sys
from pathlib import Path

# Ensure parent (AllToolkit/) is on sys.path so `import polyglot_loom` works
sys.path.insert(0, str(Path(__file__).parent.parent.parent))


def test_polyglot_loom_self_tests_pass():
    from polyglot_loom import run_tests
    failures = run_tests()
    assert not failures, f"polyglot_loom self-tests failed: {failures}"