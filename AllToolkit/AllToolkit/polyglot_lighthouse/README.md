# 🗼 Polyglot Lighthouse v1.0

> *Maritime navigation for programming languages.*

Every programming language is a lighthouse standing on the coastline of the computing world. Its beam is its idiom. Its height is its abstraction level. Its foghorn names the rocks it's saved us from. Sailors navigate from beacon to beacon.

`polyglot_lighthouse` is the maritime-navigation lens on the language rotation. It's the first tool in the polyglot family that treats each language as a real-world **coastal beacon** with IALA light characteristics, focal height, nominal range, foghorn morse codes, sea conditions, bearings, and safe-harbor recommendations.

## Quick Start

```bash
# from inside the module directory
python3 __main__.py --test       # run the full 157-test self-check
python3 __main__.py --report     # generate a lighthouse report for the current rotation language
python3 __main__.py --lightlist  # show the full Light List
python3 __main__.py --bearing Rust Go          # bearing & nautical distance between two lighthouses
python3 __main__.py --harbor ios,apple,macos   # recommend a safe harbor for a use case
python3 __main__.py --current    # show the current rotation language (no advance)
```

Or, as a module:

```python
from polyglot_lighthouse import (
    lighthouse_report,    # full report for current rotation language; advances index
    light_list,           # all lighthouses in rotation
    bearing_between,      # bearing & nautical distance between two lighthouses
    safe_harbor,          # recommend a safe harbor for use-case keywords
    get_current_language, # peek without advancing
    run_tests,            # run the full self-check
)
```

## What Makes a Lighthouse

Each language in the rotation is modeled as a fully-detailed lighthouse with:

| Field | Meaning |
|---|---|
| `beam_color` / `beam_color_name` | Color of the lantern (W/R/G/Y) |
| `light_character` | IALA light-characteristic string (`Fl W 4s`, `VQ W 1s`, …) |
| `period_seconds` | Full cycle of the light signal |
| `flash_count` | Number of flashes per period |
| `nominal_range_nm` | Visible reach in nautical miles (ecosystem reach) |
| `focal_height_m` | Tower height above sea (abstraction level) |
| `tower_shape` | Silhouette / structure shape |
| `year_first_lit` | Release year of the language |
| `age_years` | Years since first light (computed) |
| `automatized` | Does a keeper live on-site (managed runtime)? |
| `sea_location` | Body of water / coast it stands on |
| `foghorn_pattern` | Morse code of warning tone |
| `foghorn_decoded_letters` | Decoded Morse letters |
| `foghorn_period_s`, `foghorn_tone_hz` | Cadence and pitch of the warning tone |
| `known_rocks` | List of named "rocks" the language warns about (footguns) |
| `keeper_name` | Organization / foundation behind the language |
| `icon` | Emoji |
| `color_hex` | Signature color |
| `description` | Short prose |
| `current_visibility_km` | Sea-condition visibility |

## The Light List (eight lighthouses, one rotation)

| Icon | Language | Char. | Color | Year | Range (nm) | Height (m) | Sea |
|---|---|---|---|---|---|---|---|
| 🦀 | Rust     | `Fl W 4s`    | White  | 2010 | 22 | 38 | Memory-Safe Strait |
| 🐹 | Go       | `Iso W 2s`   | White  | 2009 | 28 | 24 | Cloud Sea |
| 🦅 | Swift    | `Fl R 3s (2)`| Red    | 2014 | 17 | 30 | Apple Archipelago |
| 🟣 | Kotlin   | `Fl G 5s (3)`| Green  | 2011 | 20 | 26 | JVM Bay |
| 🔷 | TypeScript | `VQ W 1s`  | White  | 2012 | 30 | 42 | Web Ocean |
| 🟨 | JavaScript | `Fl Y 2s`  | Yellow | 1995 | 35 | 18 | Web Ocean (central strait) |
| ☕ | Java     | `LFl Y 8s`   | Yellow | 1995 | 26 | 32 | Enterprise Harbor |
| ⚙️ | C/C++    | `Fl W 7.5s`  | White  | 1972 | 38 | 14 | Bare-Metal Reef |

## Sea Conditions

The `sea_conditions` block in the report summarizes current weather at the lighthouse:

- **`current_visibility_km`** — fluctuating ±2 km around the profile baseline.
- **`fog_density_pct`** — derived from visibility (lower visibility = thicker fog).
- **`harbor_score`** — weighted blend of range, focal height, automatization, visibility, and known-rock count.
- **`harbor_grade`** — 🟢 First-class / 🟡 Good / 🟠 Adequate / 🔴 Treacherous.
- **`wind_note`** — poetic flavor string.

## Bearings

For the current lighthouse, the report includes `bearings`: a list of every other lighthouse with:

- **`nautical_miles`** — Haversine distance using deterministic lighthouse coordinates (Rust → Seattle, Go → SF, Swift → Cupertino, Kotlin → Prague, TypeScript → Redmond, JavaScript → London, Java → Palo Alto, C/C++ → Boston).
- **`bearing_deg`** — initial great-circle bearing.
- **`bearing_cardinal`** — 32-point compass reading.
- **`within_nominal_range`** — true if you can see their light from this tower.
- **`mutually_visible`** — true if both can see each other's lights.

Plus two convenience lists: `visible_lighthouses` and `mutually_visible_lighthouses`.

## Safe Harbor

Given a list of use-case keywords, `safe_harbor` returns a sorted score across all eight lighthouses using transparent per-language affinity weights. Examples:

```python
safe_harbor(["systems", "embedded"])        # → C/C++, Rust
safe_harbor(["cloud", "backend"])           # → Go
safe_harbor(["ios", "apple"])               # → Swift
safe_harbor(["android", "mobile"])          # → Kotlin (top 3)
safe_harbor(["web", "frontend"])            # → TypeScript, JavaScript
safe_harbor(["enterprise", "jvm"])          # → Java
```

## Rotation Integration

`polyglot_lighthouse` reads `language_rotation.json` from the workspace root and advances `current_index` by 1 every time `lighthouse_report()` is called (so the next caller gets the next language in the rotation). The rotation order is:

```
Rust → Go → Swift → Kotlin → TypeScript → JavaScript → Java → C/C++ → Rust
```

The test suite deliberately exercises the rotation advance to make sure `current_index` and `last_language` are updated atomically and correctly.

## Tests

157 self-checks, organized into 13 sections:

```
=== Rotation File Tests ===
=== Light Character Parser Tests ===
=== Morse Decoder Tests ===
=== Light List Tests ===
=== Lighthouse Report Tests ===
=== Sea Conditions Tests ===
=== Bearings Tests ===
=== Lighthouse Coordinates Tests ===
=== Distance / Bearing Function Tests ===
=== Rotation Advance Tests ===
=== Safe Harbor Tests ===
=== Language Override Tests ===
=== Deterministic Seed Tests ===
=== Tool Metadata Tests ===
=== Foghorn Decoding for All Languages ===
=== Harbor Affinity Score Symmetry Tests ===
```

Run them with `python3 __main__.py --test`.

## Why "Lighthouse"?

Existing tools in the polyglot family already cover:

- `polyglot_orbit` — celestial mechanics / gravitational pulls
- `polyglot_weather` — atmospheric pressure / climate
- `polyglot_resonance` — wave physics
- `polyglot_quantum` — quantum physics
- `polyglot_spectrometer` — spectral analysis
- `polyglot_oracle` — personal counsel
- `polyglot_dna` — genetic / trait comparison
- `polyglot_recovery` — restorative lens
- `polyglot_chronicle` — daily log
- `polyglot_flavor` — sensory notes
- `polyglot_cipher` — cryptographic puzzles
- `polyglot_cartographer` — graph traversal
- `polyglot_topology` — shape lens
- `polyglot_fugue` — musical counterpoint
- `polyglot_tempo` — rhythm engine
- `polyglot_tarot` — divinatory lens
- `polyglot_lullaby` — bedtime compositions

None of them model the coastline. **Lighthouse** is the maritime-navigation lens: it asks not "what's the gravity?", "what's the climate?", "what's the wave?" — but **"where is the light, how far does it reach, what's the foghorn saying, and which harbor is safest for tonight's weather?"**

## File Layout

```
polyglot_lighthouse/
├── __init__.py     # the entire module — all profiles, helpers, API, tests
├── __main__.py     # CLI entry point
├── README.md       # this file
└── tests/
    └── test_lighthouse.py   # pytest-compatible test runner
```

## Author

Generated by the `AllToolkit` hourly tool generator.
Rotation timestamp: see `language_rotation.json`.