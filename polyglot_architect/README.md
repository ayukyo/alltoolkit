# 🏛️ Polyglot Architect

A creative tool that generates ASCII architectural blueprints showing how each language "builds" solutions differently — visualized as distinct architectural styles spanning brutalism, gothic, baroque, modernism, and more.

## Features

- **Architectural Blueprints**: ASCII floor plans and 3D perspectives for each language
- **Style Mapping**: Each language has a distinct architectural philosophy
- **Concept Themes**: Memory safety, concurrency, types, errors — each visualized
- **Rotation Support**: Automatically selects next language via `language_rotation.json`

## Installation

```bash
cd polyglot_architect
python -m polyglot_architect --help
```

## Usage

```bash
# Run tests
python -m polyglot_architect --test

# Generate architectural analysis for current rotation language
python -m polyglot_architect

# JSON output
python -m polyglot_architect --json
```

## Example Output

```
🏛️ Polyglot Architect — Language Architecture
═══════════════════════════════════════════════════════════════

  Language: Rust 🦀
  Theme: Memory Safety Building 🏗️
  Style: Brutalist Concrete

  ─── Blueprint ───────────────────────────────────────────
       ┌──────────────┐
       │ ░░▓▓██▓▓░░  │
    ┌──│──▓▓████▓▓──│──┐
    │  │  ████████  │  │
    │  │ ░░▓▓██▓▓░░ │  │
  ──┴──┴──────────┴──┴───
  ────────────────────────────────────────────────────────

  Foundation: Ownership algebra — statically proven non-aliasing
  Load Bearing: Lifetime annotations (rebar)
```

## Languages Covered

- Rust, Go, Swift, Kotlin, TypeScript, JavaScript, Java, C/C++

## Module Structure

```
polyglot_architect/
├── src/
│   └── __init__.py     # Main module (architect functions)
├── tests/              # (add tests here)
└── README.md
```

## Tests

```bash
python -m pytest tests/ -v
```
