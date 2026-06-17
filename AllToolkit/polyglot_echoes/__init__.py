#!/usr/bin/env python3
"""
📢 Polyglot Echoes v1.0

Echoes: iconic quotes, battle cries, and community mantras.
"""

from .src.echoes import (
    echoes,
    generate_echo_report,
    format_echo_report,
    get_current_language,
    advance_rotation,
    pick_echo,
    run_tests,
    TOOL_NAME,
    TOOL_VERSION,
)

__all__ = [
    "echoes",
    "generate_echo_report",
    "format_echo_report",
    "get_current_language",
    "advance_rotation",
    "pick_echo",
    "run_tests",
    "TOOL_NAME",
    "TOOL_VERSION",
]
