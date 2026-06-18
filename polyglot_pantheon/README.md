# ⚡ Polyglot Pantheon

A creative tool that maps programming languages as gods in a living mythology — each language is a deity with a domain, portfolio of powers, mythology origin story, worship practices, and prophecy for the current age.

## Features

- **Divine Classification**: Each language has a deity with divine rank and domain
- **Mythology & Portfolio**: Powers, blessings, and origin stories for each language-deity
- **Divine Relationships**: Alliances and rivalries between language-deities
- **Worship Practices**: How developers "invoke" each language-deity
- **Prophecy**: Future predictions for each language-deity
- **Rotation Support**: Automatically selects next language via `language_rotation.json`

## Installation

```bash
cd polyglot_pantheon
python -m polyglot_pantheon --help
```

## Usage

```bash
# Run tests
python -m polyglot_pantheon --test

# Generate pantheon for current rotation language
python -m polyglot_pantheon

# JSON output
python -m polyglot_pantheon --json
```

## Example Output

```
⚡ Polyglot Pantheon — Language Deities
═══════════════════════════════════════════════════════════════

  Deity: Rust 🦀
  Divine Name: The Iron Guardian
  Domain: Memory Safety & Zero-Cost Abstractions
  Divine Rank: Elder Deity

  ─── Divine Power ────────────────────────────────────────
  Portfolio: systems programming, memory safety, concurrency
  Blessing: Fearless concurrency — data races compile-time impossible
  Sacred Text: The Rustonomicon
  ────────────────────────────────────────────────────────

  Divine Relationships:
    Allies: C/C++ (shared systems heritage), Swift (value semantics)
    Rivals: Go (simplicity over safety)
```

## Languages Covered

- Rust, Go, Swift, Kotlin, TypeScript, JavaScript, Java, C/C++

## Module Structure

```
polyglot_pantheon/
├── src/
│   ├── __init__.py     # Package init
│   └── pantheon.py     # Main module (pantheon functions)
├── tests/
│   └── test_pantheon.py  # 18 test cases
└── README.md
```

## Tests

```bash
python -m pytest tests/ -v
```

Test coverage includes:
- Tool name and version constants
- Language deities structure validation
- `build_divinity_bar()` and `build_domain_web()` helpers
- `pantheon()` main function
- Rotation file operations
- Divine relationships and power levels
