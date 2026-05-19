# Z Algorithm Utilities (Rust)

A zero-dependency implementation of the Z-algorithm for efficient string matching and pattern searching in Rust.

## Features

- **Z-Array Computation**: O(n) algorithm for computing Z-values
- **Pattern Matching**: Find all/first occurrences using Z-algorithm
- **Substring Analysis**: Longest repeated substring, common prefixes
- **Period Detection**: Minimal period, rotation detection
- **String Compression**: Find repeating patterns
- **Multi-Pattern Matching**: Batch search with ZPatternMatcher
- **Bytes Support**: Works with byte slices

## Usage

```rust
use z_algorithm_utils::*;

// Compute Z-array
let z = z_array("aabcaabxaaz");
println!("{:?}", z); // [0, 1, 0, 0, 3, 1, 0, 0, 2, 1, 0]

// Find pattern occurrences
let positions = find_all_occurrences("abc", "abcabcabc");
println!("{:?}", positions); // [0, 3, 6]

// Find minimal period
let period = find_minimal_period("abcabcabc");
println!("Period: {}", period.period); // 3

// Multi-pattern search
let matcher = ZPatternMatcher::new(&["error", "warning"]);
let results = matcher.search("error: file not found");
```

## API Reference

### Core Functions

```rust
// Z-array computation
pub fn z_array(s: &str) -> Vec<usize>
pub fn z_array_bytes(data: &[u8]) -> Vec<usize>
pub fn z_array_with_sentinel(pattern: &str, text: &str, sentinel: &str) -> Vec<usize>

// Pattern matching
pub fn find_all_occurrences(pattern: &str, text: &str) -> Vec<usize>
pub fn find_first_occurrence(pattern: &str, text: &str) -> Option<usize>
pub fn count_occurrences(pattern: &str, text: &str) -> usize
pub fn find_matches(pattern: &str, text: &str) -> Vec<ZMatch>

// Substring analysis
pub fn longest_prefix_suffix(s: &str) -> usize
pub fn longest_repeated_substring(s: &str) -> (String, Vec<usize>)
pub fn longest_common_prefix(s1: &str, s2: &str) -> usize

// Period detection
pub fn find_minimal_period(s: &str) -> StringPeriod
pub fn is_rotation(s1: &str, s2: &str) -> bool
pub fn find_all_rotations(s: &str) -> Vec<String>

// Compression
pub fn compress_string(s: &str) -> (String, usize)
pub fn decompress_string(pattern: &str, count: usize) -> String

// Similarity
pub fn similarity_score(s1: &str, s2: &str) -> f64
pub fn batch_similarity(base: &str, strings: &[&str]) -> Vec<f64>

// Utility
pub fn visualize_z_array(s: &str) -> String
pub fn validate_z_array(s: &str, z: &[usize]) -> bool
pub fn contains(pattern: &str, text: &str) -> bool
pub fn replace_all(pattern: &str, replacement: &str, text: &str) -> String
pub fn split_by_pattern(pattern: &str, text: &str) -> Vec<String>
```

### Types

```rust
pub struct ZMatch {
    pub index: usize,
    pub length: usize,
    pub text: String,
}

impl ZMatch {
    pub fn substring(&self) -> &str
}

pub struct StringPeriod {
    pub string: String,
    pub period: usize,
    pub is_periodic: bool,
}

impl StringPeriod {
    pub fn period_string(&self) -> &str
}

pub struct ZPatternMatcher { ... }

impl ZPatternMatcher {
    pub fn new(patterns: &[&str]) -> Self
    pub fn search(&self, text: &str) -> Vec<(usize, usize, &str)>
    pub fn search_first(&self, text: &str) -> Option<(usize, usize, &str)>
    pub fn count_all(&self, text: &str) -> HashMap<&str, usize>
}
```

## Time Complexity

| Function | Time | Space |
|----------|------|-------|
| z_array | O(n) | O(n) |
| find_all_occurrences | O(n+m) | O(n+m) |
| longest_prefix_suffix | O(n) | O(n) |
| find_minimal_period | O(n) | O(n) |

## Zero Dependencies

Uses only Rust standard library.

## License

MIT License - Part of AllToolkit