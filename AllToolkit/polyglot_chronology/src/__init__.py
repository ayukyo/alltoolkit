#!/usr/bin/env python3
"""
🗺️ Polyglot Chronology v1.0
Temporal Cartography — maps programming languages as geological eras
and evolutionary epochs, revealing the deep-time forces that shaped them.

Creative concept: "Languages are not born in a vacuum — they emerge from the
geological pressures of their era: the memory crises, the concurrency earthquakes,
the type-system continental drifts. Chronology reads those pressures."

Each language is mapped to a geological/evolutionary epoch with:
  - Era signature (Precambrian, Paleozoic, Mesozoic, Cenozoic, etc.)
  - Formative pressures (what crisis drove this language into existence?)
  - Fossil record (the code fossils / artifacts that survived from this era)
  - Extinction resistance (why did this language survive its era?)
  - Epoch alignment (which era does this language best belong to?)

The tool generates a "temporal map" for the current rotation language,
showing where it sits on the programming-language geological timescale,
what pressures shaped it, and how it relates to neighboring languages
across deep time.

Distinct from existing tools:
  - language_archaeology:   historical lineage & design philosophy (specific facts)
  - polyglot_chronicle:    daily diary + challenge (day-scale temporal)
  - polyglot_dna:           genetic trait mapping (molecular level)
  - polyglot_weather:       atmospheric dynamics (weather-scale)
  - polyglot_sentinel:      threat detection (present-moment threats)
  - polyglot_harmony:       compatibility analysis (pair relationships)
  - polyglot_constellation: spatial night-sky navigation (spatial)

Chronology is about DEEP GEOLOGICAL TIME — the macro-scale forces spanning
decades that birth, shape, and test every programming language.

Rotation order: Rust → Go → Swift → Kotlin → TypeScript → JavaScript → Java → C/C++ → Rust
"""

from .chronology import (
    run_tests,
    get_current_language,
    get_epoch_for_language,
    generate_temporal_map,
    format_epoch_card,
)

__all__ = [
    "run_tests",
    "get_current_language",
    "get_epoch_for_language",
    "generate_temporal_map",
    "format_epoch_card",
]