# mtrie_utils

**Mutable Trie (Prefix Tree) with fuzzy matching, autocomplete, and JSON serialization.**

## Features

- **Mutable operations** — insert, delete, and search
- **Prefix matching** — find all words starting with a given prefix
- **Autocomplete** — configurable max results with boost-weighted ranking
- **Fuzzy search** — Levenshtein distance-based typo tolerance
- **Query boosting** — frequently searched terms rank higher
- **Case insensitive** — "Rust", "RUST", "rust" all treated as one word
- **Zero dependencies** — only `serde` for serialization

## Installation

```toml
[dependencies]
mtrie_utils = "0.1.0"
```

## Quick Start

```rust
use mtrie_utils::MTrie;

let mut trie = MTrie::new();
trie.insert("rust");
trie.insert("ruby");
trie.insert("rubyist");

// Exact match
assert!(trie.contains("rust"));

// Autocomplete
let suggestions = trie.autocomplete("ru", 5);
assert_eq!(suggestions, vec!["ruby", "rubyist", "rust"]);

// Fuzzy search (1 typo tolerance)
let matches = trie.fuzzy_search("rust", 1);
assert!(matches.iter().any(|(w, d)| w == "rust" && *d == 0));

// Boost popular terms
trie.record_query("rust");
trie.record_query("rust");
let results = trie.search_prefix("r");
assert_eq!(results[0], "rust"); // rust boosted above ruby

// Serialize to JSON
let json = trie.to_json().unwrap();
let restored = MTrie::from_json(&json).unwrap();
```

## Rotation Integration

This module is part of the AllToolkit hourly language rotation:
- **Current:** Rust (index 0)
- **Next:** Go (index 1)
- **Order:** Rust → Go → Swift → Kotlin → TypeScript → JavaScript → Java → C/C++ → Rust

## License

MIT
