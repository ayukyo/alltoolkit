//! Z Algorithm Utilities for Rust
//!
//! A zero-dependency implementation of the Z-algorithm for efficient
//! string matching and pattern searching.
//!
//! The Z-algorithm computes an array Z where Z[i] is the length of the
//! longest substring starting at position i that matches the prefix of
//! the string. This allows O(n) pattern matching.
//!
//! Author: AllToolkit
//! License: MIT

use std::collections::HashMap;

/// Represents a match found using Z-algorithm
#[derive(Debug, Clone, PartialEq)]
pub struct ZMatch {
    /// Starting index of the match
    pub index: usize,
    /// Length of the match
    pub length: usize,
    /// The text containing the match
    pub text: String,
}

impl ZMatch {
    /// Get the matched substring
    pub fn substring(&self) -> &str {
        if self.index + self.length <= self.text.len() {
            &self.text[self.index..self.index + self.length]
        } else {
            ""
        }
    }
}

/// Represents the period information of a string
#[derive(Debug, Clone, PartialEq)]
pub struct StringPeriod {
    /// The original string
    pub string: String,
    /// The minimal period length
    pub period: usize,
    /// Whether the string is truly periodic
    pub is_periodic: bool,
}

impl StringPeriod {
    /// Get the repeating unit (period string)
    pub fn period_string(&self) -> &str {
        if self.period > 0 && self.period <= self.string.len() {
            &self.string[..self.period]
        } else {
            ""
        }
    }
}

// ============================================================================
// Core Z-Algorithm
// ============================================================================

/// Compute the Z-array for a string.
///
/// Z[i] is the length of the longest substring starting from i
/// that is also a prefix of the string.
///
/// Time complexity: O(n)
/// Space complexity: O(n)
///
/// # Example
/// ```
/// let z = z_array("aabcaabxaaz");
/// assert_eq!(z, vec![0, 1, 0, 0, 3, 1, 0, 0, 2, 1, 0]);
/// ```
pub fn z_array(s: &str) -> Vec<usize> {
    let n = s.len();
    if n == 0 {
        return vec![];
    }

    let bytes = s.as_bytes();
    let z = vec![0usize; n];
    let mut z = z;
    let mut l = 0;
    let mut r = 0;

    for i in 1..n {
        if i <= r {
            z[i] = std::cmp::min(r - i + 1, z[i - l]);
        }

        while i + z[i] < n && bytes[z[i]] == bytes[i + z[i]] {
            z[i] += 1;
            if i + z[i] - 1 > r {
                l = i;
                r = i + z[i] - 1;
            }
        }
    }

    z
}

/// Compute the Z-array for a byte slice.
pub fn z_array_bytes(data: &[u8]) -> Vec<usize> {
    let n = data.len();
    if n == 0 {
        return vec![];
    }

    let z = vec![0usize; n];
    let mut z = z;
    let mut l = 0;
    let mut r = 0;

    for i in 1..n {
        if i <= r {
            z[i] = std::cmp::min(r - i + 1, z[i - l]);
        }

        while i + z[i] < n && data[z[i]] == data[i + z[i]] {
            z[i] += 1;
            if i + z[i] - 1 > r {
                l = i;
                r = i + z[i] - 1;
            }
        }
    }

    z
}

/// Compute Z-array for pattern+sentinel+text concatenation.
pub fn z_array_with_sentinel(pattern: &str, text: &str, sentinel: &str) -> Vec<usize> {
    let combined = format!("{}{}{}", pattern, sentinel, text);
    z_array(&combined)
}

// ============================================================================
// Pattern Matching
// ============================================================================

/// Find all occurrences of pattern in text using Z-algorithm.
///
/// Time complexity: O(n + m)
pub fn find_all_occurrences(pattern: &str, text: &str) -> Vec<usize> {
    if pattern.is_empty() || text.is_empty() {
        return vec![];
    }

    let m = pattern.len();
    let n = text.len();
    if m > n {
        return vec![];
    }

    let combined = format!("{}${}", pattern, text);
    let z = z_array(&combined);

    let positions: Vec<usize> = z
        .iter()
        .enumerate()
        .skip(m + 1)
        .filter_map(|(i, &z_val)| {
            if z_val >= m {
                Some(i - m - 1)
            } else {
                None
            }
        })
        .collect();

    positions
}

/// Find the first occurrence of pattern in text.
pub fn find_first_occurrence(pattern: &str, text: &str) -> Option<usize> {
    let positions = find_all_occurrences(pattern, text);
    positions.first().copied()
}

/// Count the number of occurrences of pattern in text.
pub fn count_occurrences(pattern: &str, text: &str) -> usize {
    find_all_occurrences(pattern, text).len()
}

/// Find all matches with details.
pub fn find_matches(pattern: &str, text: &str) -> Vec<ZMatch> {
    let positions = find_all_occurrences(pattern, text);
    positions
        .iter()
        .map(|&pos| ZMatch {
            index: pos,
            length: pattern.len(),
            text: text.to_string(),
        })
        .collect()
}

// ============================================================================
// Substring Analysis
// ============================================================================

/// Find the length of the longest proper prefix that is also a suffix.
pub fn longest_prefix_suffix(s: &str) -> usize {
    if s.is_empty() {
        return 0;
    }

    let z = z_array(s);
    let n = s.len();

    let mut max_lps = 0;
    for i in 1..n {
        if i + z[i] == n {
            max_lps = std::cmp::max(max_lps, z[i]);
        }
    }

    max_lps
}

/// Find the longest substring that appears at least twice.
pub fn longest_repeated_substring(s: &str) -> (String, Vec<usize>) {
    if s.is_empty() {
        return (String::new(), vec![]);
    }

    let n = s.len();
    let z = z_array(s);

    let mut max_len = 0;
    let mut positions = vec![];

    for i in 1..n {
        if z[i] > max_len {
            max_len = z[i];
            positions = vec![i];
        } else if z[i] == max_len && max_len > 0 {
            positions.push(i);
        }
    }

    // Check for longer substrings not starting at 0
    for length in (max_len + 1..=n / 2).rev() {
        for start in 0..=n - length {
            let substr = &s[start..start + length];
            let found = find_all_occurrences(substr, s);
            if found.len() >= 2 {
                return (substr.to_string(), found);
            }
        }
    }

    if max_len == 0 {
        return (String::new(), vec![]);
    }

    (s[..max_len].to_string(), positions)
}

/// Find the length of the longest common prefix of two strings.
pub fn longest_common_prefix(s1: &str, s2: &str) -> usize {
    let combined = format!("{}${}", s1, s2);
    let z = z_array(&combined);

    let pos = s1.len() + 1;
    if pos < z.len() {
        z[pos]
    } else {
        0
    }
}

// ============================================================================
// Period Detection
// ============================================================================

/// Find the minimal period of a string.
pub fn find_minimal_period(s: &str) -> StringPeriod {
    if s.is_empty() {
        return StringPeriod {
            string: String::new(),
            period: 0,
            is_periodic: false,
        };
    }

    let n = s.len();
    let bytes = s.as_bytes();

    // Check all possible periods
    for p in 1..=n / 2 {
        if n % p != 0 {
            continue;
        }

        let valid = (p..n).all(|i| bytes[i] == bytes[i % p]);
        if valid {
            return StringPeriod {
                string: s.to_string(),
                period: p,
                is_periodic: true,
            };
        }
    }

    // Using Z-array approach for general case
    let z = z_array(s);

    for p in 1..=n {
        if p < n && p + z[p] >= n {
            let valid = (p..n).all(|i| bytes[i] == bytes[i - p]);
            if valid {
                return StringPeriod {
                    string: s.to_string(),
                    period: p,
                    is_periodic: p < n,
                };
            }
        }
    }

    StringPeriod {
        string: s.to_string(),
        period: n,
        is_periodic: false,
    }
}

/// Check if s2 is a rotation of s1.
pub fn is_rotation(s1: &str, s2: &str) -> bool {
    if s1.len() != s2.len() {
        return false;
    }

    if s1.is_empty() {
        return true;
    }

    let doubled = format!("{}{}", s1, s1);
    find_all_occurrences(s2, &doubled).len() > 0
}

/// Find all unique rotations of a string.
pub fn find_all_rotations(s: &str) -> Vec<String> {
    if s.is_empty() {
        return vec![String::new()];
    }

    let n = s.len();
    let rotations: Vec<String> = (0..n)
        .map(|i| format!("{}{}", &s[i..], &s[..i]))
        .collect();

    // Remove duplicates while preserving order
    let mut seen = HashMap::new();
    let mut unique = vec![];
    for rot in rotations {
        if !seen.contains_key(&rot) {
            seen.insert(rot.clone(), true);
            unique.push(rot);
        }
    }

    unique
}

// ============================================================================
// Compression
// ============================================================================

/// Compress a string by finding its smallest repeating unit.
pub fn compress_string(s: &str) -> (String, usize) {
    if s.is_empty() {
        return (String::new(), 1);
    }

    let period = find_minimal_period(s);

    if period.is_periodic {
        return (period.period_string().to_string(), s.len() / period.period);
    }

    (s.to_string(), 1)
}

/// Decompress a string pattern.
pub fn decompress_string(pattern: &str, count: usize) -> String {
    pattern.repeat(count)
}

// ============================================================================
// Similarity
// ============================================================================

/// Calculate a similarity score based on longest common prefix.
pub fn similarity_score(s1: &str, s2: &str) -> f64 {
    if s1.is_empty() && s2.is_empty() {
        return 1.0;
    }
    if s1.is_empty() || s2.is_empty() {
        return 0.0;
    }

    let lcp = longest_common_prefix(s1, s2);
    let max_len = std::cmp::max(s1.len(), s2.len());

    lcp as f64 / max_len as f64
}

/// Calculate similarity scores for multiple strings.
pub fn batch_similarity(base: &str, strings: &[&str]) -> Vec<f64> {
    if base.is_empty() {
        return strings
            .iter()
            .map(|s| if s.is_empty() { 1.0 } else { 0.0 })
            .collect();
    }

    let max_len = std::cmp::max(base.len(), strings.iter().map(|s| s.len()).max().unwrap_or(1));

    strings
        .iter()
        .map(|s| {
            if s.is_empty() {
                0.0
            } else {
                let lcp = longest_common_prefix(base, s);
                lcp as f64 / max_len as f64
            }
        })
        .collect()
}

// ============================================================================
// Utility Functions
// ============================================================================

/// Create a visual representation of the Z-array.
pub fn visualize_z_array(s: &str) -> String {
    let z = z_array(s);
    let mut lines = vec![];

    lines.push(format!("String: {}", s));

    let index_line = format!(
        "Index:  {}",
        (0..s.len())
            .map(|i| format!("{:2}", i))
            .collect::<Vec<_>>()
            .join(" ")
    );
    lines.push(index_line);

    let char_line = format!(
        "Char:   {}",
        s.chars()
            .map(|c| format!("{:2}", c))
            .collect::<Vec<_>>()
            .join(" ")
    );
    lines.push(char_line);

    let z_line = format!(
        "Z:      {}",
        z.iter()
            .map(|v| format!("{:2}", v))
            .collect::<Vec<_>>()
            .join(" ")
    );
    lines.push(z_line);

    lines.join("\n")
}

/// Validate that a Z-array is correct for a given string.
pub fn validate_z_array(s: &str, z: &[usize]) -> bool {
    if s.len() != z.len() {
        return false;
    }

    let computed = z_array(s);
    z == computed.as_slice()
}

/// Check if a string contains another string using Z-algorithm.
pub fn contains(pattern: &str, text: &str) -> bool {
    find_first_occurrence(pattern, text).is_some()
}

/// Replace all occurrences of pattern with replacement.
pub fn replace_all(pattern: &str, replacement: &str, text: &str) -> String {
    let positions = find_all_occurrences(pattern, text);
    if positions.is_empty() {
        return text.to_string();
    }

    let mut result = String::new();
    let mut last_pos = 0;
    let m = pattern.len();

    for pos in positions {
        result.push_str(&text[last_pos..pos]);
        result.push_str(replacement);
        last_pos = pos + m;
    }
    result.push_str(&text[last_pos..]);

    result
}

/// Split text by pattern occurrences.
pub fn split_by_pattern(pattern: &str, text: &str) -> Vec<String> {
    if pattern.is_empty() {
        return vec![text.to_string()];
    }

    let positions = find_all_occurrences(pattern, text);
    if positions.is_empty() {
        return vec![text.to_string()];
    }

    let mut parts = vec![];
    let mut last_pos = 0;
    let m = pattern.len();

    for pos in positions {
        parts.push(text[last_pos..pos].to_string());
        last_pos = pos + m;
    }
    parts.push(text[last_pos..].to_string());

    parts
}

// ============================================================================
// Pattern Matcher
// ============================================================================

/// Efficient multi-pattern matcher using Z-algorithm.
pub struct ZPatternMatcher {
    patterns: Vec<String>,
    z_arrays: Vec<Vec<usize>>,
}

impl ZPatternMatcher {
    /// Create a new pattern matcher with given patterns.
    pub fn new(patterns: &[&str]) -> Self {
        let patterns: Vec<String> = patterns.iter().map(|s| s.to_string()).collect();
        let z_arrays: Vec<Vec<usize>> = patterns.iter().map(|p| z_array(p)).collect();

        ZPatternMatcher { patterns, z_arrays }
    }

    /// Search for all patterns in text.
    pub fn search(&self, text: &str) -> Vec<(usize, usize, &str)> {
        let mut results = vec![];

        for (i, pattern) in self.patterns.iter().enumerate() {
            let positions = find_all_occurrences(pattern, text);
            for pos in positions {
                results.push((i, pos, pattern.as_str()));
            }
        }

        results
    }

    /// Find the first occurrence of any pattern.
    pub fn search_first(&self, text: &str) -> Option<(usize, usize, &str)> {
        let mut first_pos = text.len();
        let mut first_pattern_idx: Option<usize> = None;

        for (i, pattern) in self.patterns.iter().enumerate() {
            if let Some(pos) = find_first_occurrence(pattern, text) {
                if pos < first_pos {
                    first_pos = pos;
                    first_pattern_idx = Some(i);
                }
            }
        }

        first_pattern_idx.map(|idx| (idx, first_pos, self.patterns[idx].as_str()))
    }

    /// Count occurrences of each pattern.
    pub fn count_all(&self, text: &str) -> HashMap<&str, usize> {
        self.patterns
            .iter()
            .map(|p| (p.as_str(), count_occurrences(p, text)))
            .collect()
    }
}

// ============================================================================
// Tests
// ============================================================================

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_z_array_basic() {
        let z = z_array("aabcaabxaaz");
        assert_eq!(z, vec![0, 1, 0, 0, 3, 1, 0, 0, 2, 1, 0]);
    }

    #[test]
    fn test_z_array_empty() {
        assert_eq!(z_array(""), vec![]);
    }

    #[test]
    fn test_z_array_single_char() {
        assert_eq!(z_array("a"), vec![0]);
    }

    #[test]
    fn test_z_array_all_same() {
        assert_eq!(z_array("aaaa"), vec![0, 3, 2, 1]);
    }

    #[test]
    fn test_z_array_no_matches() {
        let z = z_array("abcd");
        assert!(z[1..].iter().all(|&v| v == 0));
    }

    #[test]
    fn test_find_all_occurrences() {
        assert_eq!(find_all_occurrences("abc", "abcabcabc"), vec![0, 3, 6]);
        assert!(find_all_occurrences("xyz", "abcabcabc").is_empty());
    }

    #[test]
    fn test_find_first_occurrence() {
        assert_eq!(find_first_occurrence("abc", "xyzabc"), Some(3));
        assert_eq!(find_first_occurrence("abc", "abcabc"), Some(0));
        assert_eq!(find_first_occurrence("xyz", "abcabc"), None);
    }

    #[test]
    fn test_count_occurrences() {
        assert_eq!(count_occurrences("a", "banana"), 3);
        assert_eq!(count_occurrences("ana", "banana"), 2);
    }

    #[test]
    fn test_longest_prefix_suffix() {
        assert_eq!(longest_prefix_suffix("ababa"), 3);
        assert_eq!(longest_prefix_suffix("abcd"), 0);
    }

    #[test]
    fn test_longest_common_prefix() {
        assert_eq!(longest_common_prefix("abcdef", "abcxyz"), 3);
        assert_eq!(longest_common_prefix("xyz", "abc"), 0);
    }

    #[test]
    fn test_find_minimal_period() {
        let period = find_minimal_period("abcabcabc");
        assert_eq!(period.period, 3);
        assert!(period.is_periodic);

        let period = find_minimal_period("abcde");
        assert_eq!(period.period, 5);
        assert!(!period.is_periodic);
    }

    #[test]
    fn test_is_rotation() {
        assert!(is_rotation("abcde", "cdeab"));
        assert!(is_rotation("abc", "abc"));
        assert!(!is_rotation("abcde", "abced"));
    }

    #[test]
    fn test_compress_string() {
        let (pattern, count) = compress_string("abcabcabc");
        assert_eq!(pattern, "abc");
        assert_eq!(count, 3);
    }

    #[test]
    fn test_decompress_string() {
        assert_eq!(decompress_string("abc", 3), "abcabcabc");
    }

    #[test]
    fn test_similarity_score() {
        assert_eq!(similarity_score("abcdef", "abcxyz"), 0.5);
        assert_eq!(similarity_score("same", "same"), 1.0);
    }

    #[test]
    fn test_contains() {
        assert!(contains("abc", "abcabc"));
        assert!(!contains("xyz", "abcabc"));
    }

    #[test]
    fn test_replace_all() {
        assert_eq!(replace_all("abc", "xyz", "abcabcabc"), "xyzxyzxyz");
    }

    #[test]
    fn test_split_by_pattern() {
        let parts = split_by_pattern(",", "a,b,c");
        assert_eq!(parts, vec!["a", "b", "c"]);
    }

    #[test]
    fn test_z_match() {
        let m = ZMatch {
            index: 2,
            length: 3,
            text: "abcdef".to_string(),
        };
        assert_eq!(m.substring(), "cde");
    }

    #[test]
    fn test_z_pattern_matcher() {
        let matcher = ZPatternMatcher::new(&["abc", "def"]);
        let results = matcher.search("abcabcdefdef");
        assert_eq!(results.len(), 4);

        let counts = matcher.count_all("abcabc");
        assert_eq!(counts["abc"], 2);
    }
}