#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Pytest configuration for AllToolkit Python modules.
Ensures proper import paths for test modules.
"""

import sys
import os
import pytest

# Get the directory containing this conftest.py
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))


@pytest.hookimpl(tryfirst=True)
def pytest_configure(config):
    """Configure pytest with proper Python path - runs first."""
    # Pre-add all module directories to sys.path before any collection
    for item in sorted(os.listdir(ROOT_DIR)):
        module_dir = os.path.join(ROOT_DIR, item)
        if os.path.isdir(module_dir) and not item.startswith('.') and not item.startswith('_'):
            abs_path = os.path.abspath(module_dir)
            if abs_path not in sys.path:
                sys.path.insert(0, abs_path)


@pytest.hookimpl(hookwrapper=True, tryfirst=True)
def pytest_pycollect_makemodule(module_path, path, parent):
    """Hook to set sys.path before importing test modules."""
    # Get the directory containing the test file
    test_dir = str(path.dirname)
    if test_dir not in sys.path:
        sys.path.insert(0, test_dir)
    yield