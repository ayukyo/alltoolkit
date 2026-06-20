# 🖨️ Polyglot Code Printer v1.0

A creative tool that generates "code prints" — beautifully formatted, idiomatic Hello World programs for the rotation language, complete with a postcard-style layout showing the language's personality, philosophy, and aesthetic signature.

## Features

- **8 Code Prints**: Each language gets a complete aesthetic profile
  - 🦀 **Rust**: Fearless Systems — borrow checker as mentor
  - 🐹 **Go**: Practical Concurrency — goroutines for the win
  - 🦅 **Swift**: Elegant Safety — optionals make null explicit
  - 🟣 **Kotlin**: Pragmatic Power — null-safety without the ceremony
  - 🔷 **TypeScript**: Structural Trust — types as contracts
  - 🟨 **JavaScript**: Ubiquitous Flexibility — prototype chain
  - ☕ **Java**: Enterprise Stability — verbose but battle-tested
  - ⚙️ **C/C++**: Raw Performance — pointer arithmetic freedom
- **Code Aesthetic**: Box-drawing character layouts with language-specific borders
- **Signature Idioms**: Each language's distinctive one-liner
- **Hello World**: Idiomatic implementation in each language
- **Rotation Support**: Auto-advances the next language via `language_rotation.json`

## Installation

```bash
cd polyglot_code_printer
python -m polyglot_code_printer --help
```

## Usage

```bash
# Run tests
python -m polyglot_code_printer --test

# Generate a code print for current rotation language
python -m polyglot_code_printer

# JSON output
python -m polyglot_code_printer --json
```

## Example Output

```
──────────────────────────────────
  🦀 Rust — Fearless Systems
──────────────────────────────────

  Philosophy:
  If it compiles, it is correct. The borrow checker is your strict but fair mentor.

  Signature Idiom:
  unwrap() — trusting that Option<T> or Result<T, E> is Some/Ok

  Hello World:
    fn main() {
        println!("Hello, world!");
    }

  → Next: Go
──────────────────────────────────
```

## API

### `generate_code_print(language=None, seed=None)`

Generates a code print for the rotation language.

- **language** (str, optional): Override language (for testing)
- **seed** (int, optional): Random seed for deterministic output (for testing)

Returns:
```python
{
    "tool": "polyglot-code-printer",
    "version": "1.0.0",
    "selected_language": "Rust",
    "selected_emoji": "🦀",
    "vibe": "Fearless Systems",
    "philosophy": "If it compiles, it is correct. ...",
    "aesthetic": "Minimalist with algebraic types. ...",
    "signature_idiom": "unwrap() — trusting that ...",
    "hello_world": "fn main() {\n    println!(\"Hello, world!\");\n}",
    "print_lines": ["╭───...", ...],
    "all_prints": {...},  # All 8 languages
    "rotation": ["Rust", "Go", ...],
    "next_language": "Go",
    "timestamp": "2026-06-21T00:00:00+08:00"
}
```

### `format_printable(result)`

Format the code print as a plain-text string for display.

### Helper Functions

- `get_current_language()` — Get the language at the current rotation index
- `advance_rotation()` — Advance to the next language and return the new current language
- `get_next_language()` — Get the next language in the rotation
- `_build_print_lines(language, cp)` — Build the multi-line code print layout
- `_wrap(text, width)` — Simple word-wrap at width

## Module Structure

```
polyglot_code_printer/
├── __init__.py             # Core module with CODE_PRINTS data
├── __main__.py             # CLI entry point
└── README.md
```

## Testing

```bash
# Module's own test suite
python -m polyglot_code_printer --test

# Pytest test suite
python -m pytest polyglot_code_printer/tests/ -v
```
