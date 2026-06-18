# 📢 Polyglot Echoes

A creative tool that surfaces iconic quotes, battle cries, community mantras, and memorable one-liners for each programming language — the echoes that resonate long after they're first spoken.

## Features

- **Echo Database**: Curated quotes and sayings for each language
- **Categories**: Battle cries, philosophy, gotchas, community sayings, designer voices, lingo
- **Cross-Language Mapping**: How the same concept sounds in each language's voice
- **Cultural Context**: What each echo means and what it hides
- **Rotation Support**: Automatically selects next language via `language_rotation.json`

## Installation

```bash
cd polyglot_echoes
python -m polyglot_echoes --help
```

## Usage

```bash
# Run tests
python -m polyglot_echoes --test

# Generate echo for current rotation language
python -m polyglot_echoes

# Generate for specific language
python -m polyglot_echoes Rust

# JSON output
python -m polyglot_echoes --json
```

## Example Output

```
📢 Polyglot Echoes — Language Voices
═══════════════════════════════════════════════════════════════

  Language: Rust 🦀
  Category: PHILOSOPHY 💧

  ─── The Echo ───────────────────────────────────────────
  "Fearless concurrency."

  Context: Rust's flagship promise — the compiler prevents
  data races at compile time.

  Meaning: You can write concurrent code without fear of
  hidden bugs. The type system makes safety guarantees.

  What It Hides: The borrow checker learning curve is steep.
  ────────────────────────────────────────────────────────
```

## Languages Covered

- Rust, Go, Swift, Kotlin, TypeScript, JavaScript, Java, C/C++

## Module Structure

```
polyglot_echoes/
├── src/
│   ├── __init__.py     # Package init
│   └── echoes.py        # Main module (echo functions)
├── tests/
│   └── test_echoes.py    # 21 test cases
└── README.md
```

## Tests

```bash
python -m pytest tests/ -v
```

Test coverage includes:
- Tool name and version constants
- Echoes database structure and categories
- `next_language()`, `pick_echo()` helper functions
- `generate_echo_report()` and `format_echo_report()`
- `echoes()` main function
- Rotation file operations
