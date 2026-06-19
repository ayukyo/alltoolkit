#! /usr/bin/env python3
"""
🔮 Polyglot Tarot v1.0
The Programming Oracle — programming concepts as mystical tarot readings.

Every language speaks a different dialect of truth. When you ask the Oracle
a question about a concept, the language that answers is determined by rotation.
The card it draws is determined by the language's "fortune seed" — its position
in the rotation and the question's archetype. The reading combines:

  1. A CARD — drawn from a 22-card Major Arcana deck,
     each mapped to a programming archetype
  2. A POSITION — upright or reversed, flipping based on
     language volatility and rotation index parity
  3. A LANGUAGE ANSWER — the current rotation language's
     interpretation of the card's meaning for a concept
  4. A SPREAD — a Celtic Cross layout with 6 positions
     (past/present/challenge/root/goal/path/outcome)
  5. A CODA — a one-line cryptic prophecy

Each reading is deterministic for a given (language × seed) pair but feels
mystical and varied. The same language never draws the same card twice
in a row — unless the rotation demands it.

The Oracle is a creative divination tool, not a factual reference.
It says what the language THINKS about a concept, which is not always
what the language DOES. That tension — between self-perception and
reality — is the heart of the reading.

Distinct from existing tools:
  - polyglot_resonance:  concept frequency mapping (scientific waveform view)
  - polyglot_echoes:     legendary quotes (historical words of wisdom)
  - polyglot_vessel:      physical properties metaphor (material chemistry)
  - polyglot_digest:     syntax-parallel snippets (same logic, different syntax)
  - polyglot_cartographer: geopolitical world map (spatial geography)
  - polyglot_architect:  architectural blueprints (structural design)
  - polyglot_spectrometer: quality spectrum (measurable qualities)
  - polyglot_signal:     signal vocabulary (alarm semantics)
  - polyglot_chronology:  temporal history (deep time epochs)
  - polyglot_meridian:   spectral positioning (coordinate axes)
  - polyglot_harmony:    pairwise compatibility (relationship scores)
  - polyglot_forge:      skill progression paths (learning curves)

Polyglot Tarot is about PERCEPTUAL FRAME — how a language's philosophy
colours the meaning of any programming concept, revealed through the
mystical lens of tarot.

Rotation order: Rust → Go → Swift → Kotlin → TypeScript → JavaScript → Java → C/C++ → Rust
"""

from .tarot import (
    TOOL_NAME,
    TOOL_VERSION,
    MAJOR_ARCANA,
    READING_ARCHETYPES,
    ROTATION_ORDER,
    SPREAD_POSITIONS,
    load_rotation,
    save_rotation,
    get_current_language,
    advance_rotation,
    tarot,
    draw_card,
    interpret_card,
    build_spread,
    format_tarot_reading,
    format_card,
    run_tests,
    _compute_seed,
)

__all__ = [
    "TOOL_NAME",
    "TOOL_VERSION",
    "MAJOR_ARCANA",
    "READING_ARCHETYPES",
    "ROTATION_ORDER",
    "SPREAD_POSITIONS",
    "load_rotation",
    "save_rotation",
    "get_current_language",
    "advance_rotation",
    "tarot",
    "draw_card",
    "interpret_card",
    "build_spread",
    "format_tarot_reading",
    "format_card",
    "run_tests",
    "_compute_seed",
]
