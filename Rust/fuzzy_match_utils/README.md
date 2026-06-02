# fuzzy_match_utils

A zero-dependency fuzzy string matching library for Rust, written for [AllToolkit](https://github.com/AllToolkit/AllToolkit).

## Features

- **Levenshtein distance** — classic edit distance (insert, delete, substitute)
- **Damerau-Levenshtein distance** — adds transposition support
- **Jaro-Winkler similarity** — prefix-weighted similarity (0.0 to 1.0)
- **Autocomplete scorer** — ranked candidate scoring for search/type-ahead
- **Fuzzy filter** — filter + sort a list by fuzzy match score
- **Soundex** — phonetic grouping for names
- **Metaphone** — more accurate pronunciation-based matching
- **Multi-algorithm scoring** — combine all signals into a single ranked result

## Installation

```toml
[dependencies]
fuzzy_match_utils = { path = "./fuzzy_match_utils" }
```

Or in a workspace member:

```toml
[dependencies]
fuzzy_match_utils = { version = "0.1", package = "fuzzy_match_utils" }
```

## Usage

```rust
use fuzzy_match_utils::*;

// Basic similarity
let sim = jaro_winkler("MARTHA", "MARHTA");
assert!(sim > 0.95);

// Autocomplete scoring
let (score, matched) = autocomplete_score("ve", "vector");
println!("Score: {score}, Matched indices: {matched:?}");

// Fuzzy filter
let items = vec!["apple", "apricot", "banana", "pineapple"];
let results = fuzzy_filter("apple", &items, 0.5);
for r in results {
    println!("{} — {:.2}", r.candidate, r.score);
}

// Best match with multi-algorithm scoring
let items = vec!["Rust", "Go", "Swift", "Kotlin", "TypeScript"];
let result = MatchResult::best_match("Rust", &items).unwrap();
println!("Best: {} ({:.2})", result.candidate, result.score);

// Phonetic matching
assert!(sounds_like("Catherine", "Kathryn"));
assert!(sounds_like("John", "Jon"));
```

## Algorithm Details

| Algorithm | Best for | Range |
|---|---|---|
| Levenshtein | General edit distance | 0 to max_len |
| Damerau-Levenshtein | Edit distance with transposition | 0 to max_len |
| Jaro-Winkler | Short strings, prefix matches | 0.0 to 1.0 |
| Autocomplete score | Type-ahead / search ranking | 0.0 to ~15+ |
| Soundex | Names with similar sounds | Code string |
| Metaphone | English pronunciation matching | Code string |

## Testing

```bash
cargo test
```