# Polyglot Pattern Translation Utilities

A zero-dependency Python utility that teaches idiomatic programming patterns across the language rotation: **Rust → Go → Swift → Kotlin → TypeScript → JavaScript → Java → C/C++** (循环)

Rather than just showing code in one language, this module shows how the **same programming concept** is expressed in each of 8 languages — the best way to understand what makes each language unique.

## Features

- **5 idiomatic patterns** demonstrated across all 8 languages:
  - **Null/Option Safety** — Handle missing values (Rust Option, Go pointers, Swift Optional, Kotlin nullable, TypeScript union, JavaScript dynamic, Java Optional, C++ std::optional)
  - **Error Handling** — Result/Either patterns (Rust `Result<T,E>`, Go multi-return, Swift throws, Kotlin Result, TS discriminated union, JS throw/catch, Java Optional, C++ std::expected)
  - **Concurrency** — Parallel task execution (Rust threads+channels, Go goroutines, Swift GCD, Kotlin coroutines, TS Promise.all, JS async, Java ExecutorService, C++ std::async)
  - **Iteration & Transformation** — Filter + map in every language (Rust iterators, Go slices, Swift collection chains, Kotlin extensions, TS arrays, JS arrays, Java streams, C++ ranges)
  - **Function Composition** — Chain operations: add1 → multiply2 → stringify (all 8 languages)

- **Language metadata**: extension, style, paradigm, GC presence, null-safety model
- **Rotation state utilities**: read, advance, preview next language from `language_rotation.json`
- **Markdown formatter**: Generate beautiful pattern documentation

## Installation

No external dependencies. Pure Python 3.6+ standard library.

```python
from polyglot_polyglot_utils import (
    get_pattern, get_all_patterns, format_pattern_markdown,
    advance_rotation, LANGUAGE_ROTATION, LANGUAGE_META,
)
```

## Quick Start

```python
# Show a pattern in all languages
from mod import get_pattern, format_pattern_markdown
pattern = get_pattern("null_safety")
print(format_pattern_markdown(pattern))
# => Renders as markdown with fenced code blocks per language

# Show a specific language's take on a pattern
rust_pattern = get_pattern("concurrency", language="Rust")
print(format_pattern_markdown(rust_pattern))

# Advance rotation and see what comes next
from mod import advance_rotation, get_next_language
next_lang = advance_rotation()
print(f"Now rotated to: {next_lang}")

# Preview next language without advancing
print(f"Coming up: {get_next_language()}")
```

## CLI

```bash
# Show all patterns in all languages (markdown output)
python mod.py --preview

# Show one pattern across all languages
python mod.py null_safety

# Show one pattern in one language
python mod.py iteration Rust

# List all available patterns
python mod.py --list

# Show language metadata
python mod.py --meta

# Show current rotation state
python mod.py --rotation

# Advance rotation (updates language_rotation.json)
python mod.py --advance
```

## Rotation Integration

This module reads from and writes to `~/.openclaw/workspace/language_rotation.json`, which is shared with `polyglot-companion` and `polyglot-quiz`. The rotation order is:

```
Rust → Go → Swift → Kotlin → TypeScript → JavaScript → Java → C/C++ → (repeat)
```

## Test Suite

```bash
python polyglot_polyglot_utils_test.py -v
# 72 tests covering: constants, metadata, pattern definitions,
# rotation logic, query API, markdown formatting, code content
```