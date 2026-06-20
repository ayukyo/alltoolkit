#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
pytest wrapper for polyglot_horology self-tests.

The module ships its own test runner via `python -m polyglot_horology --test`.
This file wraps it as a pytest-compatible test case for CI / discovery.
"""

import sys
from pathlib import Path

# Ensure parent of polyglot_horology is on sys.path so `import polyglot_horology` works
sys.path.insert(0, str(Path(__file__).parent.parent))


def test_polyglot_horology_self_tests_pass():
    from polyglot_horology import run_tests
    failures = run_tests()
    assert not failures, f"polyglot_horology self-tests failed: {failures}"
