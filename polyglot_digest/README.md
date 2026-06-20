# 🌮 Polyglot Digest v1.0

A cross-language syntax parallel viewer — renders the same programming concept side-by-side across all 8 rotation languages simultaneously. Each digest presents a programming concept (algorithm, pattern, idiom) as a syntax-parallel snippet set, allowing developers to compare how the same idea is expressed across languages.

## Features

- **6 Programming Concepts**:
  - 👋 **Hello World**: The eternal first program
  - 🔢 **Fibonacci**: Recursive vs iterative approaches
  - 🌐 **HTTP Get**: Network I/O across languages
  - 🏛️ **Singleton Pattern**: OOP design pattern
  - ⚠️ **Error Handling**: Result/Option types and exceptions
  - 📚 **Generic Stack**: Type-parameterized data structures
- **8 Languages Side-by-Side**: Rust, Go, Swift, Kotlin, TypeScript, JavaScript, Java, C/C++
- **Syntax Parallelism**: "One concept, eight dialects"
- **Random Selection**: Each call picks a random concept (or use forced key)
- **Rotation Support**: Auto-advances the next language via `language_rotation.json`

## Installation

```bash
cd polyglot_digest
python -m polyglot_digest --help
```

## Usage

```bash
# Run tests
python -m polyglot_digest --test

# Generate a digest for current rotation language
python -m polyglot_digest

# Force a specific concept
python -c "from polyglot_digest import digest; import json; print(json.dumps(digest(language='Rust', concept_key='fn_fibonacci'), indent=2))"
```

## API

### `digest(language=None, concept_key=None)`

Main entry point. Generates a polyglot digest.

- **language** (str, optional): Override the selected language
- **concept_key** (str, optional): Override the concept selection

Returns:
```python
{
    "tool": "polyglot-digest",
    "version": "1.0.0",
    "selected_language": "Rust",
    "next_language": "Go",
    "concept": {
        "key": "hello_world",
        "title": "Hello, World!",
        "description": "The eternal first program — print a greeting to stdout.",
        "tags": ["basics", "io"]
    },
    "snippets": {
        "Rust": "fn main() {\n    println!(\"Hello, World!\");\n}",
        "Go": "package main\n\nimport \"fmt\"\n\n...",
        # ... 6 more languages
    },
    "rotation": ["Rust", "Go", ...],
    "timestamp": "2026-06-21T00:00:00+08:00"
}
```

### Helper Functions

- `get_concept(concept_key)` — Get a concept by key, or None if not found
- `get_all_concept_keys()` — Return all available concept keys
- `select_concept(forced_key=None)` — Select a concept (random or forced)
- `build_parallel_snippet(concept_key, languages)` — Build syntax-parallel snippets

## Concepts Reference

| Key | Title | Tags |
|-----|-------|------|
| `hello_world` | Hello, World! | basics, io |
| `fn_fibonacci` | Fibonacci Sequence | algorithms, recursion |
| `fn_http_get` | HTTP GET Request | networking, async |
| `pattern_singleton` | Singleton Pattern | patterns, oop |
| `fn_error_handling` | Error Handling | error-handling, robustness |
| `fn_generic_stack` | Generic Stack | generics, data-structures |

## Module Structure

```
polyglot_digest/
├── __init__.py             # Core module with CONCEPT_BANK
├── __main__.py             # CLI entry point
└── README.md
```

## Testing

```bash
# Module's own test suite
python -m polyglot_digest --test

# Pytest test suite
python -m pytest polyglot_digest/tests/ -v
```
