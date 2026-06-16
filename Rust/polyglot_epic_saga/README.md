# polyglot_epic_saga

**Epic Narrative Generator** — treats each programming language as an epic hero on an odyssey, generating narrative poetry about legendary battles, companions, and prophetic destiny.

## Creative Concept

> *"Every language is a hero. Every feature is a legend."*

This module treats programming languages as characters in an epic mythological narrative. Rust is the scarred warrior who mastered the Ownership Blade after being exiled from the C/C++ highlands. Go is the pragmatic seafarer who built the Goroutine Armada. Each language's traits become epic attributes, their evolution becomes a hero's journey, and their ecosystem becomes a cast of mythological companions.

## Rotation Integration

- Reads `language_rotation.json` → `current_index` → selects "hero" language
- Generates an epic saga with 6 chapters: Hero Introduction, Legendary Deeds, Companion Council, Antagonist Alliance, Omens & Prophecy, Epic Closure
- After generation, `current_index` advances by 1 (mod 8) and `updated_at` is refreshed
- A log of all saga runs is kept in `polyglot_epic_saga_log.json`

## Saga Structure

| Chapter | Title | Content |
|---------|-------|---------|
| I | The Summoning | Birth/history of the hero |
| II | The Legendary Deeds | Three heroic feats that defined the language |
| III | The Companion Council | Three key tools/frameworks as allies |
| IV | The Antagonist Alliance | Three rivals/challenges |
| V | Omens & Prophecy | Future predictions for the language |
| VI | The Epic Closure | Closing verse summarizing the hero's essence |

## Supported Languages

Rust · Go · Swift · Kotlin · TypeScript · JavaScript · Java · C/C++

## Usage

```rust
use polyglot_epic_saga::{EpicSaga, Language, run_cycle};
use rand::rngs::StdRng;

// Generate a saga for a specific language
let mut rng = StdRng::from_entropy();
let saga = EpicSaga::generate(Language::Rust, &mut rng);
println!("{}", saga.render_text());

// Generate AND advance the rotation
let saga = run_cycle("path/to/language_rotation.json", &mut rng)?;
```

## Example Output

```
╔══════════════════════════════════════════════════════════════════╗
║          ⚔️  POLYGLOT EPIC SAGA  ⚔️                                  ║
╠══════════════════════════════════════════════════════════════════╣
║   The Heroic Chronicle of a Programming Language                 ║
╚══════════════════════════════════════════════════════════════════╝

🐾 HERO: Rust — Fearless in the Ownership Storm
   Archetype: The Scarred Warrior
   Weapon:    The Ownership Blade (zero-cost abstractions)
   Armor:     Lifetime Forged Platemail
   Home:      The Highlands of Memory Safety

═══════════════════════════════════════════════════════════════════
📜 CHAPTER I: THE SUMMONING
...
```

## CLI

```bash
# Run with default workspace paths
cargo run

# Run with custom rotation file
cargo run -- /path/to/language_rotation.json
```

## Tests

```bash
cargo test
```

All 13 tests cover: saga generation for all 8 languages, text rendering, JSON serialization, rotation advancement, log persistence, and distinctness guarantees.

## License

MIT
