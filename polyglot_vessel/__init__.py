#!/usr/bin/env python3
"""
🏺 Polyglot Vessel v1.0

A creative tool that captures each programming language's "essences" —
the core design principles, the fundamental substance that makes each
language unique — then distills them into a structured vessel report.

Creative concept: "Every programming language is a vessel carrying the accumulated
wisdom of its designers, its community, and its era. Some vessels are built
for speed (C/C++), others for safety (Rust), others for pragmatic delivery
(Go). This tool opens each vessel and analyses what's inside — the气压 (pressure),
the density, the volatility, the buoyancy — as a way of understanding the
language's fundamental character."

Each run:
  1. Reads language_rotation.json, advances current_index
  2. Selects the rotation language
  3. Generates a vessel "certificate of analysis" with:
     - Core Essence (the language's fundamental substance)
     - Pressure Rating (how demanding/hard the language is)
     - Density (how much is packed into each concept)
     - Volatility (how stable/changing the ecosystem is)
     - Buoyancy (how easy it is to float/start with)
     - Pour Temperature (optimal use-case temperature)
     - Distillation Notes (what to watch for)
  4. Updates language_rotation.json

Distinct from existing tools:
  - polyglot_spectrometer:  spectral decomposition of Hello World (barcode)
  - polyglot_meridian:      spectral positioning (coordinates in design space)
  - polyglot_resonator:     mental model frames (how each language THINKS)
  - polyglot_flavor:        sensory tasting notes (sommelier aesthetic)
  - polyglot_resonance:     harmonic frequency relationships (oscilloscope)
  - polyglot_dna:           genetic trait mapping (molecular biology)
  - polyglot_constellation: star/gravitational map (astronomy)
  - polyglot_harmony:       pairwise compatibility scores (musical intervals)
  - polyglot_faultline:     error archaeology (seismic/tectonic)
  - polyglot_topology:      neighborhood/connected-components map (math topology)
  - polyglot_weather:       atmospheric dynamics (pressure/fronts/storms)
  - polyglot_chronicle:     daily diary + today's challenge (temporal today)
  - polyglot_digest:        syntax-parallel code snippets (spatial syntax)
  - polyglot_weather:       mood/status conditions (atmospheric)

Polyglot Vessel is about MATERIAL ESSENCE — the physical-substance metaphor
for language design: pressure, density, volatility, buoyancy, temperature.
Like a chemist's certificate of analysis for a compound, this reveals the
fundamental properties that make each language what it is.

Rotation order: Rust → Go → Swift → Kotlin → TypeScript → JavaScript → Java → C/C++ → Rust
"""

from .src.vessel import (
    generate_vessel_report,
    format_vessel_report,
    load_rotation,
    save_rotation,
    advance_rotation,
    run_tests,
    TOOL_NAME,
    TOOL_VERSION,
    get_current_language,
)

__all__ = [
    "generate_vessel_report",
    "format_vessel_report",
    "load_rotation",
    "save_rotation",
    "advance_rotation",
    "run_tests",
    "get_current_language",
    "TOOL_NAME",
    "TOOL_VERSION",
]
