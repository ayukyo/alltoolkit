#!/usr/bin/env python3
"""
🌌 Polyglot Semantics v1.0.0

Creative concept: "Every programming language is a lens through which
humans communicate intent to machines. But beneath the visible syntax —
the keywords, operators, and structures — there lies a deeper semantic
universe. The same concept maps differently across languages: a 'class'
in JavaScript (prototype chain) means something fundamentally different
from a 'class' in Python (inheritance hierarchy). A 'function' in Go
(_first-class, multi-return) is semantically light-years from a 'function'
in C (pointer to code). Polyglot Semantics maps these conceptual topologies —
how languages carve up the space of ideas differently, and where their
boundaries overlap or diverge. It reveals the semantic fingerprint: the
unique way each language partitions 'existence', 'action', 'state', and
'relation' into distinct syntactic forms."

What it does:
  - Reads language_rotation.json to select the current rotation language
  - Advances the rotation index atomically
  - Generates a structured semantic fingerprint for the selected language
  - Returns the fingerprint with metadata and next-language hint

Distinct from existing tools:
  - polyglot_prism:        spectral decomposition (scientific wavelengths)
  - polyglot_signal:       error handling vocabulary
  - polyglot_digest:       syntax parallels (surface-level similarities)
  - polyglot_translation:   cultural idioms and proverbs
  - polyglot_chronology:   geological deep-time timeline
  - polyglot_harmony:      pair compatibility analysis
  - polyglot_resonator:    mental model differences
  - polyglot_tempo:        rhythm and cadence patterns
  - polyglot_mood:         emotional personality profiles
  - polyglot_craft:        practical signature patterns
  - polyglot_cartographer: geospatial world map
  - polyglot_codex:        literary traditions and philosophy

This tool: SEMANTIC TOPOLOGY — how languages map concepts to syntax,
the conceptual boundaries, the semantic fingerprint of each language.

Rotation order: Rust → Go → Swift → Kotlin → TypeScript → JavaScript → Java → C/C++ → Rust
"""

from .src.semantics import (
    analyze_semantics,
    format_semantic_fingerprint,
    get_current_language,
    run_tests,
    TOOL_NAME,
    TOOL_VERSION,
)

__all__ = [
    "analyze_semantics",
    "format_semantic_fingerprint",
    "get_current_language",
    "run_tests",
    "TOOL_NAME",
    "TOOL_VERSION",
]