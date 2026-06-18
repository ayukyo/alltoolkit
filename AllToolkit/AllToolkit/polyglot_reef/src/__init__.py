"""
🐚 Polyglot Reef v1.0
Language Ecosystem Simulator — treats programming languages as species
competing for ecological niches in the software ecosystem.

Creative concept: "Every language is a species. Each has evolved traits —
memory safety, concurrency models, type systems — to occupy a niche.
Some are keystone species that shape the entire reef. Others are
specialists surviving in narrow bands. Polyglot Reef simulates the
ecosystem dynamics of the current rotation language."

Niche categories: Systems, Web, Mobile, Data, Enterprise, Embedded
Traits: Safety, Speed, Ergonomics, Concurrency, Type Safety (0-10)
Keystone species: languages that disproportionately shape the ecosystem
Invasive species: fast-spreading but disruptive newcomers
Indicator species: languages sensitive to ecosystem health

The tool generates an "ecosystem report" for the current rotation language,
analyzing it as a species in the reef — its niche, traits, predators,
symbionts, and whether it's thriving, stable, or at risk.

Distinct from existing tools:
  - language_archaeology:  historical lineage & design philosophy (specific facts)
  - polyglot_chronology:   geological deep-time epochs (macro temporal)
  - polyglot_quantum:      quantum state superposition of language traits
  - polyglot_dna:          genetic trait mapping (molecular level)
  - polyglot_spectrometer: spectrum analysis of language characteristics
  - polyglot_mood:         atmospheric emotional dynamics
  - polyglot_weather:      atmospheric weather patterns

Reef is about ECOLOGICAL DYNAMICS — competition, symbiosis, niche
occupation, and survival in the software ecosystem.

Rotation order: Rust → Go → Swift → Kotlin → TypeScript → JavaScript → Java → C/C++ → Rust
"""

from .reef import (
    TOOL_NAME,
    TOOL_VERSION,
    LANGUAGE_SPECIES,
    NICHE_DESCRIPTIONS,
    ROLE_DESCRIPTIONS,
    REEF_CONDITIONS,
    analyze_species,
    get_ecosystem_report,
    format_reef_report,
    load_rotation,
    save_rotation,
    compute_next_index,
    run_tests,
)

__all__ = [
    "TOOL_NAME",
    "TOOL_VERSION",
    "LANGUAGE_SPECIES",
    "NICHE_DESCRIPTIONS",
    "ROLE_DESCRIPTIONS",
    "REEF_CONDITIONS",
    "analyze_species",
    "get_ecosystem_report",
    "format_reef_report",
    "load_rotation",
    "save_rotation",
    "compute_next_index",
    "run_tests",
]
