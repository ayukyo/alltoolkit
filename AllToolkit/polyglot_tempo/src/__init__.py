"""
🎵 Polyglot Tempo v1.0
Language Rhythm Engine — treats each programming language as having
a musical tempo signature. Languages have distinct rhythms: Rust is
a precise metronome, JavaScript is syncopated jazz, Go is a steady
drum machine, C/C++ is a slow, heavy heartbeat.

This tool generates tempo profiles, beat patterns, and rhythm-based
insights for the current rotation language.

Distinct from existing tools:
  - polyglot_pulse:       vital signs / health metrics (medical analogy)
  - polyglot_gauntlet:    mastery challenges (sports analogy)
  - polyglot_reef:        ecosystem / ecological dynamics (biology)
  - polyglot_selector:    challenge generation (gaming)
  - language_archaeology: historical lineage & design philosophy

Tempo is about MUSICAL RHYTHM — BPM, time signatures, note values,
syncopation patterns, and how a language "feels" to program in.

Rotation order: Rust → Go → Swift → Kotlin → TypeScript → JavaScript → Java → C/C++ → Rust
"""

from .tempo import (
    TOOL_NAME,
    TOOL_VERSION,
    LANGUAGE_RHYTHMS,
    LANGUAGE_NOTE_VALUES,
    GENRE_DESCRIPTIONS,
    TEMPO_TIER_LABELS,
    get_tempo_profile,
    generate_beat_pattern,
    get_language_genre,
    compute_next_language,
    load_rotation,
    save_rotation,
    run_tests,
)

__all__ = [
    "TOOL_NAME",
    "TOOL_VERSION",
    "LANGUAGE_RHYTHMS",
    "LANGUAGE_NOTE_VALUES",
    "GENRE_DESCRIPTIONS",
    "TEMPO_TIER_LABELS",
    "get_tempo_profile",
    "generate_beat_pattern",
    "get_language_genre",
    "compute_next_language",
    "load_rotation",
    "save_rotation",
    "run_tests",
]