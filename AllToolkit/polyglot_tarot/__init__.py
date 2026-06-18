#! /usr/bin/env python3
"""🔮 Polyglot Tarot — A Programming Oracle."""

import sys
import os
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from polyglot_tarot.src import (
    tarot,
    format_tarot_reading,
    run_tests,
    TOOL_NAME,
    TOOL_VERSION,
    READING_ARCHETYPES,
    MAJOR_ARCANA,
    ROTATION_ORDER,
    SPREAD_POSITIONS,
    load_rotation,
    save_rotation,
    get_current_language,
    advance_rotation,
    draw_card,
    interpret_card,
    build_spread,
)

__all__ = [
    "tarot",
    "format_tarot_reading",
    "run_tests",
    "TOOL_NAME",
    "TOOL_VERSION",
    "READING_ARCHETYPES",
    "MAJOR_ARCANA",
    "ROTATION_ORDER",
    "SPREAD_POSITIONS",
    "load_rotation",
    "save_rotation",
    "get_current_language",
    "advance_rotation",
    "draw_card",
    "interpret_card",
    "build_spread",
]
