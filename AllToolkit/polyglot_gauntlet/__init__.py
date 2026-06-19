#!/usr/bin/env python3
"""
⚔️ Polyglot Gauntlet v1.0

A language challenge arena — the current rotation language issues you a
code gauntlet: a specific programming challenge that tests a hard-won skill
unique to that language. Complete the challenge, and earn XP toward mastery.

Creative concept: "Every language has a defining challenge — a rite of passage
that separates those who merely use the language from those who have truly
mastered it. The Gauntlet is where you face that challenge head-on."

Each language has:
  - ONE canonical gauntlet challenge (the "rite of passage")
  - A scoring rubric (speed, elegance, safety, creativity)
  - Failure modes that are characteristic of that language
  - A success story that demonstrates mastery

How it works:
  1. Read language_rotation.json to get current language and index
  2. Load that language's gauntlet challenge
  3. Present the challenge with full context, difficulty, and rubric
  4. Optionally: verify completion against expected patterns
  5. Update language_rotation.json's current_index (advance by 1)

The gauntlet is NOT about algorithmic puzzles. It's about language-specific
rites of passage — the challenge that most directly tests whether you
understand what makes that language special.

Rotation order: Rust → Go → Swift → Kotlin → TypeScript → JavaScript → Java → C/C++ → Rust

Distinct from existing tools:
  - polyglot_tarot:        mystical card readings (perceptual divination)
  - polyglot_oracle:       personal counsel from language philosophy
  - polyglot_resonator:    mental model mapping across all languages
  - polyglot_fossil:       evolutionary archaeology of syntax fossils
  - polyglot_vessel:       physical chemistry properties metaphor
  - polyglot_reef:         ecological species competition
  - language_mastery:      XP/level progress tracking
  - language_sage:         idioms, tips, and pitfalls
  - polyglot_forge:        skill progression paths

Polyglot Gauntlet is about RITES OF PASSAGE — the one challenge that defines
whether you've truly understood a language, not just learned it.
"""

__version__ = "1.0.0"
__author__ = "AllToolkit"

from .src.gauntlet import (
    TOOL_NAME,
    TOOL_VERSION,
    ROTATION_ORDER,
    load_rotation,
    save_rotation,
    get_current_language,
    advance_rotation,
    get_gauntlet,
    format_gauntlet,
    run_tests,
)

__all__ = [
    "TOOL_NAME",
    "TOOL_VERSION",
    "ROTATION_ORDER",
    "load_rotation",
    "save_rotation",
    "get_current_language",
    "advance_rotation",
    "get_gauntlet",
    "format_gauntlet",
    "run_tests",
]
