"""
🌡️ Polyglot Mood — cross-language personality & emotional profiling.

Creative concept: "Every language has a personality. This tool maps the
emotional landscape of our rotation — the mood shifts as we move from
Rust's methodical caution to Go's cheerful pragmatism, from Swift's
elegant expressiveness to Kotlin's pragmatic conciseness."

For the current rotation language, Polyglot Mood generates:
  1. A personality archetype (e.g., "The Perfectionist", "The Pragmatist")
  2. An emotional fingerprint (mood spectrum across 5 dimensions)
  3. A "vibe check" comparing current ↔ next language in the rotation
  4. Practical mood-aware coding tips that match the language's temperament
  5. A haiku that captures the language's emotional essence

Distinct from existing tools:
  - polyglot_harmony:   compatibility matrix (syntax/paradigm/interop/transfer scores)
  - polyglot_digest:    syntax-parallel snippets (same problem, different syntax)
  - polyglot_resonator: mental model frames (how each language THINKS)
  - polyglot_dna:       genetic trait mapping (what each language IS)
  - polyglot_chronicle: daily history + challenge log (temporal today)
  - polyglot_bridges:   semantic problem→solution maps (conceptual translation)
  - polyglot_wire:      FFI & interop mapping (physical wire protocols)
  - polyglot_faultline: pain-point & frustration analysis

Polyglot Mood is about AFFECT — the emotional/personality dimension
of each language that colors how developers feel while using them.
"""

__version__ = "0.1.0"
__author__ = "AllToolkit"

from .src.mood import (
    get_mood_profile,
    get_consecutive_mood,
    MoodProfile,
    MoodSpectrum,
    VibeCheck,
    ROTATION_FILE,
)

__all__ = [
    "get_mood_profile",
    "get_consecutive_mood",
    "MoodProfile",
    "MoodSpectrum",
    "VibeCheck",
    "ROTATION_FILE",
]