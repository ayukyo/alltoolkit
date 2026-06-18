# 🏺 Polyglot Vessel

A creative tool that maps programming languages as vessels with physical properties — pressure ratings, density, volatility, buoyancy, and distillation notes — revealing the essence of each language as a tangible substance.

## Features

- **Vessel Certificates**: Physical property profiles for each language
- **Property Visualization**: ASCII bars showing pressure, density, volatility, buoyancy
- **Distillation Notes**: Practical wisdom about each language's nature
- **Compatibility Mapping**: Which languages "pour well" together
- **Overall Assessment**: Quality grade and usability/reliability scores
- **Rotation Support**: Automatically selects next language via `language_rotation.json`

## Installation

```bash
cd polyglot_vessel
python -m polyglot_vessel --help
```

## Usage

```bash
# Run tests
python -m polyglot_vessel --test

# Generate vessel report for current rotation language
python -m polyglot_vessel

# Generate with specific seed (deterministic)
python -m polyglot_vessel --seed 42

# JSON output
python -m polyglot_vessel --json
```

## Example Output

```
🏺 Polyglot Vessel — Language Essence
═══════════════════════════════════════════════════════════════

  Vessel: Rust 🦀
  Core Essence: Ownership & Borrowing — the language that
  proves memory safety at compile time

  ─── Physical Properties ─────────────────────────────────
  Pressure:  [██████████░░░░░░░░░] 9.2/10 — EXTREME
  Density:   [██████████████████░] 9.5/10 — EXTREMELY DENSE
  Volatility:[████░░░░░░░░░░░░░░░] 2.1/10 — CRYSTALLISED
  Buoyancy:  [█████░░░░░░░░░░░░░░] 3.0/10 — SINKS DEEPLY
  ────────────────────────────────────────────────────────

  Pour Temperature: Cold (Compile-Time Verification)
  Vessel Shape: Blown-glass borosilicate
  Overall Grade: A — Exceptional (with handling warnings)
```

## Languages Covered

- Rust, Go, Swift, Kotlin, TypeScript, JavaScript, Java, C/C++

## Module Structure

```
polyglot_vessel/
├── src/
│   ├── __init__.py     # Package init
│   └── vessel.py        # Main module (vessel functions)
├── tests/
│   └── test_vessel.py   # 23 test cases
└── README.md
```

## Tests

```bash
python -m pytest tests/ -v
```

Test coverage includes:
- Tool name and version constants
- VESSEL_DATA structure validation
- Label helper functions (pressure, density, volatility, buoyancy)
- `advance_rotation()`, `get_current_language()` rotation functions
- `generate_vessel_report()` and `format_vessel_report()`
- Physical property calculations
