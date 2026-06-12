#!/usr/bin/env python3
"""
🪨 Polyglot Fossil v1.0

A "language archaeology" tool that identifies inherited syntax and conceptual
"fossils" across the programming language rotation chain.

Creative concept: "Every language carries fossils — syntax and concepts inherited
from its ancestors. This tool digs through the rotation strata to reveal which
fossils a language inherited from its predecessors, which it mutated, and which
it evolved entirely new."

For the current rotation language, this tool:
  1. Reads language_rotation.json to get the current language
  2. Traces back the rotation chain to identify ancestors
  3. Excavates syntax/concept fossils inherited from each ancestor
  4. Classifies each fossil as: INHERITED | MUTATED | NOVEL
  5. Generates a stratified layer diagram of the language's evolutionary history
  6. Updates language_rotation.json

Rotation order: Rust → Go → Swift → Kotlin → TypeScript → JavaScript → Java → C/C++ → Rust

Distinct from existing tools:
  - language_archaeology:   historical lineage & design philosophy (broader view)
  - language_compass:        learning journey maps
  - language_ecohub:         package ecosystem field guide
  - language_mastery:       XP/level progress tracking
  - language_sage:           idioms, pro tips, pitfalls
  - language_synapse:        conceptual bridges between languages
  - language_ethos:          philosophical manifesto
  - polyglot_flavor:         sensory tasting notes
  - polyglot_digest:         syntax-parallel code snippets
  - polyglot_chronicle:      daily history and trivia
  - polyglot_code_printer:   code output formatting
  - polyglot_resonator:      frequency/resonance analysis
  - polyglot_harmony:        compatibility scores between pairs
  - polyglot_cipher:         cryptographic ciphers themed on languages
  - polyglot_constellation:  stellar mapping of language relationships

Fossil is about EVOLUTIONARY ARCHAEOLOGY — digging into the strata of language
evolution to see what's inherited, mutated, or newly evolved.
"""

__version__ = "0.1.0"
__author__ = "AllToolkit"

from .src.forge import (
    fossil_dig,
    get_fossils,
    FossilRecord,
    FossilClassification,
    ROTATION_ORDER,
)

__all__ = [
    "fossil_dig",
    "get_fossils",
    "FossilRecord",
    "FossilClassification",
    "ROTATION_ORDER",
]