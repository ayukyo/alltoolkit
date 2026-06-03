# language_safety_matrix

A **Memory & Type Safety Analysis Tool** — generates a comparative multi-dimensional safety matrix across programming languages.

## Creative Concept

Every programming language makes trade-offs between **control** and **safety**. This tool analyzes 8 distinct safety axes for each language and renders both individual radar profiles and comparative matrices, helping developers reason about risk tolerance and correctness boundaries.

## Distinct from Existing Tools

| Tool | Focus |
|---|---|
| `language_sage` | Idioms, pro tips, pitfalls (learning) |
| `language_archaeology` | Historical origins, design philosophy (history) |
| `language_probe` | Runtime availability, version, capabilities (runtime) |
| `language_mastery` | XP/level progress tracking (gamification) |
| `language_compass` | Learning journey milestones (education path) |
| `language_rotator` | Round-robin scheduling with weights/cooldowns (orchestration) |
| **`language_safety_matrix`** | **Safety analysis across 8 axes (technical comparison)** |

## Safety Axes

1. **Memory Safety** — heap/stack safety, dangling pointers, GC vs manual
2. **Type Safety** — static vs dynamic, implicit conversions, type erasure
3. **Concurrency Safety** — data race prevention, thread safety in type system
4. **Null Safety** — nullable types, NPE risk, Option/Optional types
5. **Overflow Safety** — arithmetic overflow handling, UB risk
6. **Aliasing Safety** — reference vs value semantics, shared mutable state
7. **Uninitialized Safety** — initialization requirements, UB from uninitialized reads
8. **Escape Safety** — escape analysis, heap vs stack allocation guarantees

## Rotation Order

```
Rust → Go → Swift → Kotlin → TypeScript → JavaScript → Java → C/C++ → Rust (loop)
```

## Usage

```rust
use language_safety_matrix::{LanguageSafetyProfile, generate_matrix};

// Single language profile
let profile = LanguageSafetyProfile::generate("Rust");
println!("{}", profile.radar_chart());

// Multi-language comparison matrix
let matrix = generate_matrix(&["Rust", "Go", "JavaScript", "C/C++"]);
for (lang, profile) in &matrix {
    println!("{}: {:.0}% overall", lang, profile.overall_score * 100.0);
}
```

## CLI

```bash
cargo run --example cli Rust                    # Rust safety profile
cargo run --example cli Rust Go JavaScript      # Compare 3 languages
cargo run --example cli --all                   # All 8 languages matrix
cargo run --example cli --axes                  # List safety axes
```

## Output Example

```
🛡️ Safety Radar: Rust (97% overall)

  Memory Safety      [████████████████████] 100%  Ownership + borrowing enforces exclusive access...
  Type Safety        [████████████████████] 100%  Strong static typing with inference...
  Concurrency Safety [████████████████████] 100%  Send/Sync traits encode thread safety...
  ...

  Risk Profile: 🛡️ Fort Knox — maximum safety with zero-cost abstractions
```