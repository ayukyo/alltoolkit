#!/usr/bin/env python3
"""
Polyglot Chef — A Kitchen Brigade Tribute to Programming Languages

Each language is a station in a professional brigade kitchen, with:
  - Kitchen station & role
  - Cooking philosophy (technique)
  - Signature dish (what the language "cooks" best)
  - Mise en place requirements
  - Service节奏 (service rhythm / flow)
  - Plating philosophy
  - Kitchen tool equivalents
  - Chef's philosophy

Concept: "Every language is a station in the brigade — Rust is the
Sautoir who meticulously prepares every ingredient, Go is the
Rôtisseur who keeps the pass flowing, JavaScript is the Entremetier
who improvises with whatever arrives on the pass. This tool is the
menu for tonight's service."

Distinct from existing tools:
  - polyglot_flavor:       sommelier wine-tasting (sensory profile)
  - polyglot_mood:         emotional personality (psychological profile)
  - polyglot_tempo:        rhythm & cadence (musical)
  - polyglot_signal:       error/null/warning semantics (communication)
  - polyglot_resonance:    frequency shift (physics)
  - polyglot_cartographer: geopolitical nation map (geopolitical)
  - polyglot_harmony:      pair compatibility (relational)
  - polyglot_digest:       syntax-parallel snippets (syntax)
  - polyglot_chronology:   historical timeline (temporal)
  - polyglot_translation:  cultural proverbs (cultural)

Chef is about WORKFLOW & EXECUTION PHILOSOPHY — how each language
prepares, times, and executes a "service", rendered as a kitchen
brigade report.

Rotation order: Rust → Go → Swift → Kotlin → TypeScript → JavaScript → Java → C/C++ → Rust
"""

from polyglot_chef.src.chef import (
    TOOL_NAME,
    TOOL_VERSION,
    ROTATION_ORDER,
    KITCHEN_DB,
    get_current_language,
    get_station_for_language,
    generate_station_report,
    format_station_card,
    run_tests,
)

__all__ = [
    "TOOL_NAME",
    "TOOL_VERSION",
    "ROTATION_ORDER",
    "KITCHEN_DB",
    "get_current_language",
    "get_station_for_language",
    "generate_station_report",
    "format_station_card",
    "run_tests",
]