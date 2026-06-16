"""
📡 Polyglot Anomaly Detector v1.0.0

Creative concept: "Every programming language has quirks — edge cases, paradoxes,
gotchas, and counterintuitive behaviors that are unique to that language. Like
anomalies in a universe of consistent laws, these are the moments where the
language breaks from expectation and reveals something deeper about its design
philosophy. Rust's borrow checker doesn't allow recursive mutable borrows.
JavaScript's typeof null returns 'object'. Swift's String is a value type that
copies. Go's maps are not goroutine-safe by design. This tool catalogs the
anomalies, paradoxes, and delightful contradictions of each language."

What it does:
  - Reads language_rotation.json to select the current rotation language
  - Advances the rotation index atomically
  - Generates a structured anomaly report for the selected language
  - Returns the anomaly report with metadata and next-language hint

Rotation order: Rust → Go → Swift → Kotlin → TypeScript → JavaScript → Java → C/C++ → Rust
"""

from .src.anomaly import (
    detect_anomalies,
    format_anomaly_report,
    get_current_language,
    run_tests,
    TOOL_NAME,
    TOOL_VERSION,
)

__all__ = [
    "detect_anomalies",
    "format_anomaly_report",
    "get_current_language",
    "run_tests",
    "TOOL_NAME",
    "TOOL_VERSION",
]