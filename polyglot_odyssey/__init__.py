"""
🚀 Polyglot Odyssey v1.0

A time-travel journey through programming language history. Each rotation
language appears as a historical "waypoint era" with ASCII timeline maps,
archaeological artifacts, and a journey narrative for the current language.

Creative concept: "Programming languages are epochs in the grand story of
computation. Polyglot Odyssey generates an ASCII timeline journey — each
language is a destination with its own era, landmarks, cultural artifacts,
and a forward/backward path through the history of languages. The current
rotation language becomes your travel destination, with contextual travel
advice on what to pack (mental model), how to navigate (syntax patterns),
and what to see (signature features)."

Rotation order: Rust → Go → Swift → Kotlin → TypeScript → JavaScript → Java → C/C++ → Rust
"""

from .src import (
    TOOL_NAME,
    TOOL_VERSION,
    LANGUAGE_ERAS,
    TIMELINE_WAYPOINTS,
    odyssey,
    format_odyssey_report,
    run_tests,
    load_rotation,
    save_rotation,
    get_current_language,
    advance_rotation,
)

__all__ = [
    "TOOL_NAME",
    "TOOL_VERSION",
    "LANGUAGE_ERAS",
    "TIMELINE_WAYPOINTS",
    "odyssey",
    "format_odyssey_report",
    "run_tests",
    "load_rotation",
    "save_rotation",
    "get_current_language",
    "advance_rotation",
]
