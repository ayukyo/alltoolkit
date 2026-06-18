# 🌌 Polyglot Constellation

A creative tool that maps programming languages as stars in a constellation — each language is a celestial body with gravitational relationships to others, forming patterns and mythological narratives across the programming night sky.

## Features

- **Star Classification**: Each language is a star with size, temperature, brightness
- **Gravitational Bonds**: Language relationships visualized as gravitational attraction
- **Constellation Patterns**: Thematic groupings across language "stars"
- **Mythological Narratives**: Created stories connecting language relationships
- **Rotation Support**: Automatically selects next language via `language_rotation.json`

## Installation

```bash
cd polyglot_constellation
python -m polyglot_constellation --help
```

## Usage

```bash
# Run tests
python -m polyglot_constellation --test

# Generate constellation for current rotation language
python -m polyglot_constellation

# Generate for specific language
python -m polyglot_constellation Rust

# JSON output
python -m polyglot_constellation --json
```

## Example Output

```
🌌 Polyglot Constellation
═══════════════════════════════════════════════════════════════

  Language: Rust 🦀
  Star Class: M (Red Dwarf)
  Constellation: The Iron Guardian

  ─── Stellar Map ─────────────────────────────────────────
           ✦ C/C++(0.8)
            \
             🦀 Rust (1.2) ✦ Swift(1.0)
            /
         ✦ Kotlin(0.9)
  ────────────────────────────────────────────────────────

  Gravitational Bond to C/C++: Strong (shared systems heritage)
  Gravitational Bond to Swift: Moderate (value semantics)
```

## Languages Covered

- Rust, Go, Swift, Kotlin, TypeScript, JavaScript, Java, C/C++

## Module Structure

```
polyglot_constellation/
├── __init__.py          # Main module (Star, GravitationalBond, constellation functions)
├── src/                 # Empty (code is in __init__.py)
├── tests/               # (add tests here)
└── README.md
```

## Tests

```bash
python -m pytest tests/ -v
```
