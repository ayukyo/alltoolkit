# src/__init__.py
from .fugue import fugue, format_fugue, run_tests, advance_rotation, load_rotation, save_rotation
from .fugue import FUGUE_THEMES, ROTATION_ORDER, TOOL_NAME, TOOL_VERSION

__all__ = [
    "fugue", "format_fugue", "run_tests",
    "advance_rotation", "load_rotation", "save_rotation",
    "FUGUE_THEMES", "ROTATION_ORDER", "TOOL_NAME", "TOOL_VERSION",
]
