"""Sentinel — language ecosystem watchtower."""

from pathlib import Path

from .sentinel import (
    ROTATION_ORDER,
    ROTATION_FILE,
    get_current_language,
    advance_rotation,
    generate_sentinel_report,
    format_report,
)
from .config import load_config, save_config

__all__ = [
    "ROTATION_ORDER",
    "ROTATION_FILE",
    "get_current_language",
    "advance_rotation",
    "generate_sentinel_report",
    "format_report",
    "load_config",
    "save_config",
]


def run_tests() -> None:
    """Run the test suite."""
    import pytest
    import sys
    sys.exit(pytest.main(["-v", str(Path(__file__).parent.parent / "tests")]))