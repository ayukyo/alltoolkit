"""Polyglot Prism — Spectral Analysis of Programming Languages."""

from .prism import (
    TOOL_NAME,
    TOOL_VERSION,
    ROTATION_ORDER,
    SPECTRAL_DB,
    get_current_language,
    get_spectral_data,
    generate_spectral_report,
    format_spectral_report,
    _wrap_text,
    run_tests,
)

__all__ = [
    "TOOL_NAME",
    "TOOL_VERSION",
    "ROTATION_ORDER",
    "SPECTRAL_DB",
    "get_current_language",
    "get_spectral_data",
    "generate_spectral_report",
    "format_spectral_report",
    "_wrap_text",
    "run_tests",
]