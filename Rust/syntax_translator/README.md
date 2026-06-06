# syntax_translator

**Cross-Language Syntax Translator** — converts code snippets between any two languages in the rotation.

## Creative Concept

> *"Every language speaks the same ideas differently."*

A pattern-based code translator that transforms syntax between languages while preserving semantics. Reads `language_rotation.json` for round-robin selection and advances the index after each translation.

## Language Rotation Order

```
Rust → Go → Swift → Kotlin → TypeScript → JavaScript → Java → C/C++ → Rust (loop)
```

## Features

- **Bidirectional translation** between all 8 rotation languages
- **Pattern-based transformation** with 50+ rules covering function signatures, variable declarations, print statements, loops, match/switch, class/struct, null handling, lambdas
- **Language profiles** with type system, null safety, mutability, and concurrency metadata
- **Confidence scoring** (0.0–1.0) based on rules applied vs. gaps
- **Coverage reports** per language pair showing patterns covered and remaining gaps
- **Rotation integration** — reads from and updates `language_rotation.json`

## Usage

```rust
use syntax_translator::{SyntaxTranslator, Language};

let translator = SyntaxTranslator::new();

// Translate Rust code to Go
let result = translator.translate(
    r#"fn main() { println!("hello"); }"#,
    "Rust",
    "Go"
).unwrap();
println!("{}", result.translated_code);
// Output: func main() { fmt.Println("hello"); }

// Translate and rotate in one call
let result = translator.translate_and_rotate(code, &path).unwrap();
```

## Rotation Integration

```rust
use syntax_translator::SyntaxTranslator;
use std::path::Path;

let path = Path::new("/home/admin/.openclaw/workspace/language_rotation.json");
let translator = SyntaxTranslator::new();

// Get current → next from rotation
let (from, to) = SyntaxTranslator::get_next_from_rotation(path).unwrap();
// from = "Rust", to = "Go" (when index=0)

// Translate and advance rotation
let result = translator.translate_and_rotate(code, path).unwrap();
```

## Coverage Report

```rust
let cov = translator.coverage_report("Rust", "Go").unwrap();
println!("{} -> {}: {:.0}% coverage ({} patterns)",
    cov.from, cov.to, cov.coverage_percent, cov.patterns_available);
```

## CLI

```bash
cargo run --example cli language_rotation.json "fn main() { println!(\"hello\"); }" Rust Go
cargo run --example coverage language_rotation.json Rust Go
```

## Running Tests

```bash
cargo test
```

**All 25 tests pass** ✓

## Translation Rules Summary

| From → To | Key Patterns |
|---|---|
| Rust → Go | `fn` → `func`, `println!` → `fmt.Println`, `let mut` → `:=`, `match` → `switch` |
| Rust → TypeScript | `fn` → `function`, `println!` → `console.log`, `let mut` → `let` |
| Go → Rust | `func` → `fn`, `fmt.Println` → `println!`, `:=` → `let mut`, `switch` → `match` |
| Swift → Rust | `func` → `fn`, `print` → `println!`, `if let` → `if let Some` |
| Kotlin → Rust | `fun` → `fn`, `println` → `println!`, `when` → `match`, `null` → `None` |
| TypeScript → Rust | `function` → `fn`, `console.log` → `println!`, `interface` → `struct` |
| Java → Rust | `public static void main` → `fn main`, `System.out.println` → `println!` |
| C/C++ → Rust | `int main()` → `fn main()`, `printf` → `println!` |