# Levenshtein Utils

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A comprehensive Rust library for Levenshtein distance and fuzzy string matching with **zero external dependencies**.

## Features

- **Levenshtein Distance**: Classic edit distance algorithm with O(min(m,n)) space optimization
- **Damerau-Levenshtein**: Extended distance allowing transpositions
- **Optimal String Alignment (OSA)**: Restricted Damerau-Levenshtein
- **Similarity Metrics**: Similarity ratio, normalized distance
- **Jaro & Jaro-Winkler**: Advanced similarity algorithms for names and short strings
- **Fuzzy Search**: Find closest matches, threshold-based matching
- **Edit Operations**: Get the sequence of edits to transform one string to another
- **Hamming Distance**: For strings of equal length
- **Longest Common Subsequence (LCS)**: Length and string extraction
- **Diff Visualization**: Generate human-readable diff output

## Installation

Add this to your `Cargo.toml`:

```toml
[dependencies]
levenshtein_utils = { path = "../levenshtein_utils" }
```

## Quick Start

```rust
use levenshtein_utils::{
    levenshtein_distance, similarity_ratio, find_closest, find_matches,
    jaro_winkler_similarity, edit_operations,
};

fn main() {
    // Basic distance
    let dist = levenshtein_distance("kitten", "sitting");
    println!("Distance: {}", dist); // Output: 3

    // Similarity ratio (0.0 to 1.0)
    let ratio = similarity_ratio("hello", "hallo");
    println!("Similarity: {:.2}%", ratio * 100.0); // Output: 80.00%

    // Find closest match
    let words = vec!["apple", "banana", "cherry"];
    let closest = find_closest("aple", &words);
    println!("Closest: {:?}", closest); // Output: Some("apple")

    // Find all matches within threshold
    let matches = find_matches("hello", &["hallo", "help", "held", "world"], 2);
    println!("Matches: {:?}", matches); // Output: ["hallo", "help", "held"]

    // Jaro-Winkler for name matching
    let sim = jaro_winkler_similarity("Martha", "Marhta");
    println!("JW Similarity: {:.4}", sim); // Output: > 0.96
}
```

## API Reference

### Distance Functions

| Function | Description |
|----------|-------------|
| `levenshtein_distance(a, b)` | Standard edit distance |
| `levenshtein_distance_matrix(a, b)` | Returns distance + full matrix |
| `damerau_levenshtein_distance(a, b)` | Distance with transpositions |
| `osa_distance(a, b)` | Optimal String Alignment distance |
| `hamming_distance(a, b)` | For equal-length strings |

### Similarity Functions

| Function | Returns | Description |
|----------|---------|-------------|
| `similarity_ratio(a, b)` | `f64` | 0.0 (different) to 1.0 (identical) |
| `normalized_distance(a, b)` | `f64` | 0.0 (identical) to 1.0 (different) |
| `jaro_similarity(a, b)` | `f64` | Jaro similarity score |
| `jaro_winkler_similarity(a, b)` | `f64` | Jaro with prefix bonus |

### Search Functions

| Function | Description |
|----------|-------------|
| `find_closest(query, candidates)` | Returns closest match |
| `find_matches(query, candidates, max_dist)` | All matches within distance |
| `find_similar(query, candidates, min_ratio)` | All matches above similarity |
| `find_top_matches(query, candidates, n)` | Top N matches with scores |

### Utility Functions

| Function | Description |
|----------|-------------|
| `edit_operations(a, b)` | Sequence of edits to transform |
| `lcs_length(a, b)` | Length of longest common subsequence |
| `lcs_string(a, b)` | The LCS as a string |
| `diff(a, b)` | Human-readable diff |

## Examples

### Spell Checking

```rust
use levenshtein_utils::find_matches;

let dictionary = vec!["hello", "world", "rust", "programming"];
let misspelled = "prgraming";

let suggestions = find_matches(misspelled, &dictionary, 3);
// Returns: ["programming"]
```

### Autocomplete

```rust
use levenshtein_utils::find_closest;

let commands = vec!["install", "uninstall", "update", "search"];
let user_input = "intsall";

if let Some(suggestion) = find_closest(user_input, &commands) {
    println!("Did you mean '{}'?", suggestion);
}
// Output: Did you mean 'install'?
```

### DNA Sequence Alignment

```rust
use levenshtein_utils::{levenshtein_distance, similarity_ratio};

let seq1 = "ACGTACGT";
let seq2 = "ACGTTACG";

let dist = levenshtein_distance(seq1, seq2);
let similarity = similarity_ratio(seq1, seq2);

println!("Distance: {}", dist);        // Output: 2
println!("Similarity: {:.2}%", similarity * 100.0); // Output: 75.00%
```

## Algorithm Details

### Levenshtein Distance

The standard algorithm computes the minimum number of single-character edits (insertions, deletions, substitutions) to transform one string into another. Our implementation uses a space-optimized two-row approach with O(min(m,n)) space complexity.

### Damerau-Levenshtein

Extends the standard algorithm to also count transpositions of adjacent characters as a single edit operation. This is useful for detecting common typing errors like "teh" vs "the".

### Jaro-Winkler

Gives extra weight to strings that match from the beginning, making it particularly effective for comparing names and short strings. The scaling factor defaults to 0.1.

## Performance

| Operation | Time Complexity | Space Complexity |
|-----------|----------------|------------------|
| levenshtein_distance | O(m × n) | O(min(m, n)) |
| damerau_levenshtein_distance | O(m × n) | O(m × n) |
| jaro_similarity | O(m + n) | O(m + n) |
| hamming_distance | O(n) | O(1) |
| lcs_length | O(m × n) | O(n) |

## License

MIT License - See [LICENSE](LICENSE) for details.

## Contributing

Contributions are welcome! Please feel free to submit issues or pull requests.