# polyglot_syntax_matrix

> 🌏 Comparative syntax reference for 8 languages — side-by-side equivalent code snippets

**Rust · Go · Swift · Kotlin · TypeScript · JavaScript · Java · C/C++**

## Overview

`polyglot_syntax_matrix` is a structured reference for comparing idiomatic syntax across 8 mainstream programming languages. It organizes equivalent code patterns across 10 categories, making it trivial to cross-reference language idioms without context-switching to documentation.

## Categories

| Category | What's covered |
|---|---|
| **Hello World** | Minimal programs |
| **Variables & Mutability** | Immutable/mutable bindings, type inference |
| **Functions** | Definitions, parameters, return types, arrow forms |
| **Control Flow** | switch/match/when, if, ternary |
| **Structs & Classes** | Types with methods, data classes, records |
| **Error Handling** | Result/Option, try/catch, ? / error multivalue |
| **Concurrency** | async/await, goroutines, coroutines, actors |
| **Collections** | Arrays/lists, maps/dicts, iteration, functional ops |
| **Option / Null Handling** | Optional chaining, nullish coalescing, safe calls |
| **Traits & Interfaces** | Protocols, traits, interfaces, abstract classes |

## Usage

### Library

```rust
use polyglot_syntax_matrix::{SyntaxMatrix, Category};

let matrix = SyntaxMatrix::new();

// Full report
println!("{}", matrix.generate_report());

// Per-category
println!("{}", matrix.category_snippets(Category::Concurrency).render_text());

// Per-language summary
println!("{}", matrix.language_summary("Rust"));
```

### CLI

```bash
cargo run --example cli
```

## Output Example

```
╔══════════════════════════════════════════════════════════╗
║       🌏 Polyglot Syntax Matrix — 8 Languages              ║
╠══════════════════════════════════════════════════════════╣
║  Rust · Go · Swift · Kotlin · TS · JS · Java · C/C++   ║
╚══════════════════════════════════════════════════════════╝

▸ Hello World
────────────────
  ◆ Rust
    fn main() {
        println!("Hello, world!");
    }

  ◆ Go
    func main() {
        fmt.Println("Hello, world!")
    }
  ...
```

## Design Notes

- All snippets are **idiomatic** — not minimal — reflecting real-world usage
- Each snippet includes optional **gotcha notes** (💎 prefixed)
- Snippets are language-identical within a category only in trivial cases;
  most categories (especially error handling and concurrency) produce distinctly
  different code per language
- Serializes to JSON for tooling integration (language-server plugins, docs generators)

## Rotation Order

```
Rust → Go → Swift → Kotlin → TypeScript → JavaScript → Java → C/C++ → Rust (loop)
```

This module was generated as the **Rust** step of the language rotation cycle.