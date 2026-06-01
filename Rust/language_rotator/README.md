# language_rotator

A smart round-robin language selector for AllToolkit, written in Rust.

## Features

- **Round-robin selection** with automatic index rotation — no repeats back-to-back
- **Weighted preference system** — boost or bury languages by weight
- **Streak tracking** — configurable per-language `avoid_streak` flag prevents consecutive repeats
- **Cooldown enforcement** — configurable minimum interval between selections per language
- **JSON persistence** — load/save with atomic rename for crash-safety
- **Event history** — every selection is logged with timestamp and whether it was forced

## Rotation Order

```
Rust → Go → Swift → Kotlin → TypeScript → JavaScript → Java → C/C++ → Rust (loop)
```

## Usage

```rust
use language_rotator::{LanguageEntry, LanguageRotator};

// Build from code
let languages = vec![
    LanguageEntry::new("Rust"),
    LanguageEntry::new("Go"),
    LanguageEntry::new("Swift"),
];
let mut rotator = LanguageRotator::new(languages);

// Select next
let sel = rotator.select().unwrap();
println!("Selected: {}", sel.language); // "Rust"

// Persist to disk
rotator.save("state.json").unwrap();

// Reload later
let rotator = LanguageRotator::load("state.json").unwrap();
```

## CLI

```bash
cargo run --example cli language_rotation.json   # select next
cargo run --example cli language_rotation.json --status   # show status
cargo run --example cli language_rotation.json --history   # show history
cargo run --example cli language_rotation.json --force Go  # force-select Go
```

## Data Format

```json
{
  "languages": [
    {
      "name": "Rust",
      "weight": 1.0,
      "use_count": 5,
      "last_used": 1748824800000,
      "cooldown_ms": 0,
      "avoid_streak": true
    }
  ],
  "current_index": 1,
  "last_selected": "Rust",
  "history": [
    { "language": "Rust", "index": 0, "timestamp": 1748824800000, "was_forced": false }
  ]
}
```

## Fields

| Field | Description |
|---|---|
| `name` | Language identifier |
| `weight` | Preference weight (higher = more preferred in weighted mode) |
| `use_count` | Total number of times this language has been selected |
| `last_used` | Millisecond UNIX timestamp of last selection |
| `cooldown_ms` | Minimum milliseconds between selections (0 = no limit) |
| `avoid_streak` | If `true`, skip this language if it would repeat the last selection |
| `current_index` | Next position in the round-robin ring |
| `last_selected` | Name of the last selected language |
| `history` | Chronological log of all selection events |