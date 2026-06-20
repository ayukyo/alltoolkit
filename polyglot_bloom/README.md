# 🌸 polyglot_bloom v1.0.0

A phenological garden engine for programming languages — each language is
treated as a plant species with its own flowering schedule, hardiness zone,
companion species, pollinators, soil chemistry, and seasonal events.

## Concept

Every language blooms on its own schedule. Some bloom in spring (fresh
releases), some in autumn (steady enterprise), some year-round. This
garden reveals what grows beside each language, who pollinates it, what
soil it needs, and when to expect the next bloom.

## What makes it different

- **Phenology lens** — no other tool in the collection treats languages
  as plants with bloom calendars, hardiness zones, companion planting,
  and pollinator strength.
- **Soil chemistry** — each language gets a pH and NPK (Nitrogen=jobs,
  Phosphorus=libraries, Potassium=stability) rating.
- **Companion planting analysis** — quantify how well two languages grow
  together (shared pollinators, overlapping zones, FFI affinity).
- **Bloom prediction** — uses release schedule + NPK to forecast next
  bloom strength for the rotation's current language.
- **Pollinator diversity** — categorizes a language's ecosystem
  supporters into foundations, corporations, and conferences.

## Usage

```bash
# Bloom report for the rotation's current language
python -m polyglot_bloom

# Bloom report for a specific language
python -m polyglot_bloom Java

# Tour all 8 language gardens (summary)
python -m polyglot_bloom --tour

# Year-long bloom calendar
python -m polyglot_bloom --calendar 2026

# Companion analysis between two languages
python -m polyglot_bloom --companion Rust Go

# Show current rotation language (does not advance)
python -m polyglot_bloom --current

# Run self-tests
python -m polyglot_bloom --test
```

## Python API

```python
from polyglot_bloom import (
    bloom_report,        # full phenological report
    bloom_calendar,      # year-long bloom calendar
    companion_analysis,  # companion planting between two languages
    garden_tour,         # tour all 8 gardens
    get_current_language,
    run_tests,
)

# Library use
report = bloom_report(language="Java", advance=True)
print(report["plant_profile"]["common_name"])    # "Enterprise Oak"
print(report["soil_health"]["rating"])          # "🪴 Healthy topsoil..."
print(report["next_bloom"]["predicted_bloom_strength"])
print(report["garden_health"]["score"])

# Companion analysis
c = companion_analysis("Rust", "C/C++")
print(c["benefit_score"], c["classification"])
```

## Rotation

Reads `language_rotation.json` from the workspace root and advances the
index after each `bloom_report()` call. Honors the rotation order:
Rust → Go → Swift → Kotlin → TypeScript → JavaScript → Java → C/C++ → Rust.

## Tests

The module ships with a self-test runner:

```bash
python -m polyglot_bloom --test
```

All 8 languages are tested for valid profiles, soil chemistry, bloom
prediction, calendar coverage, pollinator strength, companion symmetry,
and rotation advance mechanics.

## Distinct from sibling tools

- `polyglot_orbit` — celestial mechanics / gravity (spatial lens)
- `polyglot_weather` — atmospheric pressure (meteorology lens)
- `polyglot_fossil` — archaeology of dead languages (fossil lens)
- `polyglot_oracle` — philosophical counsel (oracle lens)
- `polyglot_lullaby` — bedtime narrative (calming lens)
- `polyglot_reef` — coral reef simulation (marine lens)
- `polyglot_topology` — shape & connectivity (topology lens)
- `polyglot_chef` — cooking recipes (culinary lens)
- `polyglot_signal` — waveform processing (signal lens)
- `polyglot_metamorphosis` — AST transformation (metamorphosis lens)

`polyglot_bloom` is the gardening / phenology lens — it asks: when does
this language grow, what grows beside it, and what feeds its roots?