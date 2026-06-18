#!/usr/bin/env python3
"""
🎵 Polyglot Tempo v1.0
Rhythm Pattern Generator — programming languages as musical rhythms.
"""

from .tempo import (
    TOOL_NAME,
    TOOL_VERSION,
    ROTATION_ORDER,
    RHYTHM_DATA,
    load_rotation,
    save_rotation,
    get_current_language,
    advance_rotation,
    get_previous_language,
    tempo,
    generate_rhythm_report,
    format_rhythm_card,
    run_tests,
)

__all__ = [
    "TOOL_NAME",
    "TOOL_VERSION",
    "ROTATION_ORDER",
    "RHYTHM_DATA",
    "load_rotation",
    "save_rotation",
    "get_current_language",
    "advance_rotation",
    "get_previous_language",
    "tempo",
    "generate_rhythm_report",
    "format_rhythm_card",
    "run_tests",
]
