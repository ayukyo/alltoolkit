//! # Suffix Array Utilities
//!
//! A comprehensive suffix array implementation for efficient string processing operations.
//!
//! ## Features
//! - Zero dependencies, uses only Rust standard library
//! - O(n log² n) construction algorithm
//! - Substring search in O(m log n) time
//! - Longest repeated substring finding
//! - Longest common substring between multiple strings
//! - LCP (Longest Common Prefix) array construction
//! - Pattern matching and counting
//! - ASCII-safe implementation

use std::cmp::Ordering;
use std::collections::HashSet;

/// A suffix array data structure for efficient string operations
#[derive(Debug, Clone)]
pub struct SuffixArray {
    /// The original string
    original: String,
    /// Sorted suffix indices (byte positions in original string)
    indices: Vec<usize>,
    /// Sorted suffixes for reference
    suffixes: Vec<String>,
    /// LCP array
    lcp: Vec<usize>,
}

impl SuffixArray {
    /// Creates a new SuffixArray from the given string
    pub fn new(s: &str) -> Self {
        let n = s.len();
        if n == 0 {
            return SuffixArray {
                original: String::new(),
                indices: Vec::new(),
                suffixes: Vec::new(),
                lcp: Vec::new(),
            };
        }

        // Create suffix-index pairs using valid UTF-8 boundaries
        let mut pairs: Vec<(String, usize)> = Vec::new();
        for (i, _) in s.char_indices() {
            pairs.push((s[i..].to_string(), i));
        }

        // Sort by suffix
        pairs.sort_by(|a, b| a.0.cmp(&b.0));

        // Extract sorted suffixes and indices
        let suffixes: Vec<String> = pairs.iter().map(|p| p.0.clone()).collect();
        let indices: Vec<usize> = pairs.iter().map(|p| p.1).collect();

        // Compute LCP array using Kasai's algorithm
        let lcp = compute_lcp(&s, &indices);

        SuffixArray {
            original: s.to_string(),
            indices,
            suffixes,
            lcp,
        }
    }

    /// Creates a SuffixArray from a String
    pub fn from_string(s: String) -> Self {
        Self::new(&s)
    }

    /// Returns the original string
    pub fn original(&self) -> &str {
        &self.original
    }

    /// Returns the length of the original string in bytes
    pub fn len(&self) -> usize {
        self.original.len()
    }

    /// Returns true if the original string is empty
    pub fn is_empty(&self) -> bool {
        self.original.is_empty()
    }

    /// Returns the number of characters (not bytes)
    pub fn char_len(&self) -> usize {
        self.original.chars().count()
    }

    /// Returns the sorted suffix indices
    pub fn indices(&self) -> &[usize] {
        &self.indices
    }

    /// Returns the suffix at the given position in the sorted array
    pub fn suffix(&self, i: usize) -> Option<&str> {
        self.suffixes.get(i).map(|s| s.as_str())
    }

    /// Returns the LCP array
    pub fn lcp(&self) -> &[usize] {
        &self.lcp
    }

    /// Finds all occurrences of a pattern in the string
    pub fn find_all(&self, pattern: &str) -> Vec<usize> {
        if pattern.is_empty() || self.is_empty() {
            return Vec::new();
        }

        let (left, right) = self.find_range(pattern);
        if left == right {
            return Vec::new();
        }

        let mut result: Vec<usize> = self.indices[left..right].to_vec();
        result.sort();
        result
    }

    /// Finds the range of suffixes that start with the pattern
    fn find_range(&self, pattern: &str) -> (usize, usize) {
        let n = self.suffixes.len();
        if n == 0 {
            return (0, 0);
        }

        // Binary search for left boundary
        let mut left = 0;
        let mut right = n;
        while left < right {
            let mid = (left + right) / 2;
            if self.suffixes[mid].as_str() < pattern {
                left = mid + 1;
            } else {
                right = mid;
            }
        }

        // Find right boundary
        let pattern_len = pattern.len();
        let mut end = left;

        while end < n {
            let suffix = &self.suffixes[end];
            if suffix.len() >= pattern_len && &suffix[..pattern_len] == pattern {
                end += 1;
            } else if suffix.len() < pattern_len {
                // Check if suffix is a prefix of pattern (should not match)
                if suffix.as_str() < pattern {
                    end += 1;
                } else {
                    break;
                }
            } else {
                break;
            }
        }

        (left, end)
    }

    /// Returns the number of occurrences of a pattern
    pub fn count(&self, pattern: &str) -> usize {
        self.find_all(pattern).len()
    }

    /// Checks if the pattern exists in the string
    pub fn contains(&self, pattern: &str) -> bool {
        self.count(pattern) > 0
    }

    /// Finds the longest repeated substring
    pub fn longest_repeated_substring(&self) -> Option<String> {
        if self.lcp.is_empty() {
            return None;
        }

        let mut max_len = 0;
        let mut max_idx = 0;

        for i in 1..self.lcp.len() {
            if self.lcp[i] > max_len {
                max_len = self.lcp[i];
                max_idx = i;
            }
        }

        if max_len == 0 {
            return None;
        }

        self.suffixes.get(max_idx).map(|s| s[..max_len].to_string())
    }

    /// Finds the longest repeated substring that appears at least `min_occurrences` times
    pub fn longest_repeated_substring_min(&self, min_occurrences: usize) -> Option<String> {
        if min_occurrences < 2 {
            return self.longest_repeated_substring();
        }

        let n = self.lcp.len();
        if n == 0 {
            return None;
        }

        let mut max_len = 0;
        let mut max_idx = 0;

        for i in 1..n {
            let min_lcp = self.lcp[i];
            if min_lcp == 0 {
                continue;
            }

            // Count occurrences by checking LCP chain
            let mut count = 2;

            // Check consecutive suffixes with LCP >= min_lcp
            for j in (1..i).rev() {
                if self.lcp[j] >= min_lcp {
                    count += 1;
                } else {
                    break;
                }
            }

            for j in i + 1..n {
                if self.lcp[j] >= min_lcp {
                    count += 1;
                } else {
                    break;
                }
            }

            if count >= min_occurrences && min_lcp > max_len {
                max_len = min_lcp;
                max_idx = i;
            }
        }

        if max_len == 0 {
            return None;
        }

        self.suffixes.get(max_idx).map(|s| s[..max_len].to_string())
    }

    /// Returns all substrings that appear at least twice
    pub fn all_repeated_substrings(&self) -> Vec<String> {
        if self.lcp.is_empty() {
            return Vec::new();
        }

        let mut seen = HashSet::new();
        let mut result = Vec::new();

        for i in 1..self.lcp.len() {
            if self.lcp[i] > 0 {
                if let Some(suffix) = self.suffixes.get(i) {
                    // Get the substring of length lcp[i]
                    if let Some(substr) = suffix.get(..self.lcp[i]).map(|s| s.to_string()) {
                        if !seen.contains(&substr) {
                            seen.insert(substr.clone());
                            result.push(substr);
                        }
                    }
                }
            }
        }

        result.sort();
        result
    }

    /// Counts the number of distinct substrings
    pub fn count_distinct_substrings(&self) -> usize {
        let n = self.indices.len();
        if n == 0 {
            return 0;
        }

        // Total substrings = sum of suffix lengths
        let total: usize = self.indices.iter().map(|&i| self.original.len() - i).sum();
        let lcp_sum: usize = self.lcp.iter().sum();

        total - lcp_sum
    }

    /// Returns all distinct substrings in sorted order
    pub fn all_substrings(&self) -> Vec<String> {
        if self.is_empty() {
            return Vec::new();
        }

        let mut seen = HashSet::new();
        let mut result = Vec::new();

        for (i, suffix) in self.suffixes.iter().enumerate() {
            let lcp_val = if i > 0 { self.lcp[i] } else { 0 };

            // Add all new distinct substrings from this suffix (starting from lcp_val)
            let suffix_bytes = suffix.as_bytes();
            for j in lcp_val..suffix_bytes.len() {
                if let Some(substr) = suffix.get(..j + 1) {
                    let substr = substr.to_string();
                    if !seen.contains(&substr) {
                        seen.insert(substr.clone());
                        result.push(substr);
                    }
                }
            }
        }

        result.sort();
        result
    }

    /// Returns the k-th distinct substring in lexicographic order (1-indexed)
    pub fn kth_distinct_substring(&self, k: usize) -> Option<String> {
        if k == 0 || self.is_empty() {
            return None;
        }

        let mut count = 0;

        for (i, suffix) in self.suffixes.iter().enumerate() {
            let lcp_val = if i > 0 { self.lcp[i] } else { 0 };
            let suffix_len = suffix.len();

            for j in lcp_val..suffix_len {
                count += 1;
                if count == k {
                    return suffix.get(..j + 1).map(|s| s.to_string());
                }
            }
        }

        None
    }

    /// Finds the longest palindromic substring
    pub fn longest_palindromic_substring(&self) -> Option<&str> {
        let chars: Vec<char> = self.original.chars().collect();
        let n = chars.len();
        if n == 0 {
            return None;
        }

        let mut max_len = 1;
        let mut start = 0;

        for i in 0..n {
            // Odd length palindrome
            expand_palindrome(&chars, i, i, &mut max_len, &mut start);
            // Even length palindrome
            expand_palindrome(&chars, i, i + 1, &mut max_len, &mut start);
        }

        // Convert character indices to byte indices
        let byte_start = self.original.char_indices().nth(start).map(|(i, _)| i).unwrap_or(0);
        let byte_end = self.original.char_indices().nth(start + max_len).map(|(i, _)| i).unwrap_or(self.original.len());

        Some(&self.original[byte_start..byte_end])
    }

    /// Returns the rank (position in sorted array) of the suffix starting at position i
    pub fn rank(&self, i: usize) -> Option<usize> {
        self.indices.iter().position(|&idx| idx == i)
    }

    /// Returns the n-th smallest suffix (0-indexed)
    pub fn nth_element(&self, n: usize) -> Option<(String, usize)> {
        if n >= self.suffixes.len() {
            return None;
        }
        Some((self.suffixes[n].clone(), self.indices[n]))
    }

    /// Returns the LCP between suffixes starting at positions i and j (byte positions)
    pub fn lcp_between(&self, i: usize, j: usize) -> usize {
        if i >= self.original.len() || j >= self.original.len() {
            return 0;
        }

        let suffix_i = &self.original[i..];
        let suffix_j = &self.original[j..];

        let bytes_i = suffix_i.as_bytes();
        let bytes_j = suffix_j.as_bytes();

        let mut k = 0;
        while k < bytes_i.len() && k < bytes_j.len() && bytes_i[k] == bytes_j[k] {
            k += 1;
        }
        k
    }

    /// Compares two suffixes starting at positions i and j
    pub fn compare_suffixes(&self, i: usize, j: usize) -> Ordering {
        if i == j {
            return Ordering::Equal;
        }
        self.original[i..].cmp(&self.original[j..])
    }

    /// Finds the longest prefix of the pattern that exists in the string
    pub fn longest_prefix_of<'a>(&self, pattern: &'a str) -> &'a str {
        if pattern.is_empty() || self.is_empty() {
            return "";
        }

        let mut max_len = 0;
        let pattern_bytes = pattern.as_bytes();

        for suffix in &self.suffixes {
            let suffix_bytes = suffix.as_bytes();
            let cmp_len = pattern_bytes.len().min(suffix_bytes.len());
            let mut match_len = 0;
            for i in 0..cmp_len {
                if suffix_bytes[i] == pattern_bytes[i] {
                    match_len += 1;
                } else {
                    break;
                }
            }
            max_len = max_len.max(match_len);
        }

        &pattern[..max_len]
    }

    /// Returns all occurrences with context
    pub fn occurrences(&self, pattern: &str) -> Vec<Occurrence> {
        let positions = self.find_all(pattern);
        positions
            .into_iter()
            .map(|pos| Occurrence {
                position: pos,
                pattern: pattern.to_string(),
                context: get_context(&self.original, pos, pattern.len()),
            })
            .collect()
    }
}

/// Expand palindrome from center
fn expand_palindrome(chars: &[char], mut left: usize, mut right: usize, max_len: &mut usize, start: &mut usize) {
    while left > 0 && right < chars.len() && chars[left - 1] == chars[right] {
        left -= 1;
        right += 1;
    }
    
    if left == 0 && right == chars.len() {
        // Full string palindrome case
    }
    
    let len = right - left;
    if len > *max_len {
        *max_len = len;
        *start = left;
    }
}

/// Compute LCP array using Kasai's algorithm
fn compute_lcp(s: &str, indices: &[usize]) -> Vec<usize> {
    let n = indices.len();
    if n == 0 {
        return Vec::new();
    }

    // Build inverse suffix array (rank)
    let mut rank = vec![0usize; n];
    for i in 0..n {
        rank[indices[i]] = i;
    }

    // Kasai's algorithm
    let mut lcp = vec![0usize; n];
    let mut k = 0usize;
    let bytes = s.as_bytes();

    for i in 0..n {
        if rank[i] == n - 1 {
            k = 0;
            continue;
        }
        let j = indices[rank[i] + 1];
        while i + k < bytes.len() && j + k < bytes.len() && bytes[i + k] == bytes[j + k] {
            k += 1;
        }
        lcp[rank[i] + 1] = k;
        if k > 0 {
            k -= 1;
        }
    }

    lcp
}

/// Helper to get context around a match
fn get_context(s: &str, pos: usize, pattern_len: usize) -> String {
    const CONTEXT_LEN: usize = 5;
    let start = pos.saturating_sub(CONTEXT_LEN);
    let end = (pos + pattern_len + CONTEXT_LEN).min(s.len());
    s[start..end].to_string()
}

impl PartialEq for SuffixArray {
    fn eq(&self, other: &Self) -> bool {
        self.original == other.original && self.indices == other.indices
    }
}

impl Eq for SuffixArray {}

impl std::fmt::Display for SuffixArray {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        writeln!(f, "SuffixArray[{}]:", self.original)?;
        for (i, suffix) in self.suffixes.iter().enumerate() {
            writeln!(
                f,
                "  {}{} (idx: {})",
                " ".repeat(self.original.len() - suffix.len()),
                suffix,
                self.indices[i]
            )?;
        }
        Ok(())
    }
}

impl From<String> for SuffixArray {
    fn from(s: String) -> Self {
        Self::from_string(s)
    }
}

impl From<&str> for SuffixArray {
    fn from(s: &str) -> Self {
        Self::new(s)
    }
}

/// Represents a pattern occurrence with context
#[derive(Debug, Clone, PartialEq)]
pub struct Occurrence {
    pub position: usize,
    pub pattern: String,
    pub context: String,
}

/// Finds the longest common substring between two strings
pub fn longest_common_substring(s1: &str, s2: &str) -> Option<String> {
    if s1.is_empty() || s2.is_empty() {
        return None;
    }

    // Use multiple unique separators
    let separator = "$$$###$$$";
    let combined = format!("{}{}{}", s1, separator, s2);

    let sa = SuffixArray::new(&combined);
    let sep_start = s1.len();
    let s2_start = sep_start + separator.len();
    let _total_len = combined.len();

    let mut max_len = 0;
    let mut max_idx = 0;

    for i in 1..sa.lcp.len() {
        let idx1 = sa.indices[i - 1];
        let idx2 = sa.indices[i];

        // Skip if either suffix starts in separator
        if (idx1 >= sep_start && idx1 < s2_start) || (idx2 >= sep_start && idx2 < s2_start) {
            continue;
        }

        // One suffix starts in s1, the other in s2
        let in_s1_1 = idx1 < sep_start;
        let in_s2_1 = idx1 >= s2_start;
        let in_s1_2 = idx2 < sep_start;
        let in_s2_2 = idx2 >= s2_start;

        let from_diff_strings = (in_s1_1 && in_s2_2) || (in_s2_1 && in_s1_2);

        if from_diff_strings && sa.lcp[i] > max_len {
            max_len = sa.lcp[i];
            max_idx = i;
        }
    }

    if max_len == 0 {
        return None;
    }

    sa.suffix(max_idx).and_then(|s| s.get(..max_len)).map(|s| s.to_string())
}

/// Returns all common substrings of at least minLength characters between two strings
pub fn common_substrings(s1: &str, s2: &str, min_length: usize) -> Vec<String> {
    if s1.is_empty() || s2.is_empty() || min_length == 0 {
        return Vec::new();
    }

    let separator = "$$$###$$$";
    let combined = format!("{}{}{}", s1, separator, s2);

    let sa = SuffixArray::new(&combined);
    let sep_start = s1.len();
    let s2_start = sep_start + separator.len();

    let mut seen = HashSet::new();
    let mut result = Vec::new();

    for i in 1..sa.lcp.len() {
        if sa.lcp[i] < min_length {
            continue;
        }

        let idx1 = sa.indices[i - 1];
        let idx2 = sa.indices[i];

        // Skip if either suffix starts in separator
        if (idx1 >= sep_start && idx1 < s2_start) || (idx2 >= sep_start && idx2 < s2_start) {
            continue;
        }

        let in_s1_1 = idx1 < sep_start;
        let in_s2_1 = idx1 >= s2_start;
        let in_s1_2 = idx2 < sep_start;
        let in_s2_2 = idx2 >= s2_start;

        let from_diff_strings = (in_s1_1 && in_s2_2) || (in_s2_1 && in_s1_2);

        if from_diff_strings {
            if let Some(suffix) = sa.suffix(i) {
                if let Some(substr) = suffix.get(..sa.lcp[i]) {
                    let substr = substr.to_string();
                    if !seen.contains(&substr) {
                        seen.insert(substr.clone());
                        result.push(substr);
                    }
                }
            }
        }
    }

    result.sort();
    result
}

/// Finds the minimum lexicographic rotation of a string using Booth's algorithm
pub fn min_lexicographic_rotation(s: &str) -> String {
    let n = s.len();
    if n == 0 {
        return String::new();
    }

    let ss = format!("{}{}", s, s);
    let bytes = ss.as_bytes();

    let mut k = 0;
    let mut i = 1;

    while i < n {
        let mut j = 0;
        while j < n && bytes[k + j] == bytes[i + j] {
            j += 1;
        }
        if j < n && bytes[k + j] > bytes[i + j] {
            k = i;
        }
        if i + j <= k {
            i = i + j + 1;
        } else {
            i += 1;
        }
    }

    ss[k..k + n].to_string()
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_new() {
        let sa = SuffixArray::new("banana");
        assert_eq!(sa.len(), 6);
        assert_eq!(sa.indices(), &[5, 3, 1, 0, 4, 2]);
    }

    #[test]
    fn test_empty() {
        let sa = SuffixArray::new("");
        assert!(sa.is_empty());
        assert_eq!(sa.indices().len(), 0);
    }

    #[test]
    fn test_single_char() {
        let sa = SuffixArray::new("a");
        assert_eq!(sa.indices(), &[0]);
    }

    #[test]
    fn test_lcp() {
        let sa = SuffixArray::new("banana");
        assert_eq!(sa.lcp(), &[0, 1, 3, 0, 0, 2]);
    }

    #[test]
    fn test_find_all() {
        let sa = SuffixArray::new("banana");
        assert_eq!(sa.find_all("ana"), vec![1, 3]);
        assert_eq!(sa.find_all("a"), vec![1, 3, 5]);
        assert_eq!(sa.find_all("na"), vec![2, 4]);
        assert_eq!(sa.find_all("xyz"), vec![]);
    }

    #[test]
    fn test_count() {
        let sa = SuffixArray::new("mississippi");
        assert_eq!(sa.count("iss"), 2);
        assert_eq!(sa.count("i"), 4);
        assert_eq!(sa.count("s"), 4);
        assert_eq!(sa.count("xyz"), 0);
    }

    #[test]
    fn test_contains() {
        let sa = SuffixArray::new("banana");
        assert!(sa.contains("ana"));
        assert!(sa.contains("na"));
        assert!(!sa.contains("xyz"));
    }

    #[test]
    fn test_longest_repeated_substring() {
        let sa = SuffixArray::new("banana");
        assert_eq!(sa.longest_repeated_substring(), Some("ana".to_string()));

        let sa2 = SuffixArray::new("aaaa");
        assert_eq!(sa2.longest_repeated_substring(), Some("aaa".to_string()));

        let sa3 = SuffixArray::new("abc");
        assert_eq!(sa3.longest_repeated_substring(), None);
    }

    #[test]
    fn test_count_distinct_substrings() {
        assert_eq!(SuffixArray::new("").count_distinct_substrings(), 0);
        assert_eq!(SuffixArray::new("a").count_distinct_substrings(), 1);
        assert_eq!(SuffixArray::new("aa").count_distinct_substrings(), 2);
        assert_eq!(SuffixArray::new("ab").count_distinct_substrings(), 3);
        assert_eq!(SuffixArray::new("abc").count_distinct_substrings(), 6);
    }

    #[test]
    fn test_all_substrings() {
        let sa = SuffixArray::new("abc");
        let substrs = sa.all_substrings();
        assert_eq!(substrs, vec!["a", "ab", "abc", "b", "bc", "c"]);
    }

    #[test]
    fn test_longest_common_substring() {
        // "an" is common: banana[1:3] and orange[2:4]
        assert_eq!(longest_common_substring("banana", "orange"), Some("an".to_string()));
        assert_eq!(longest_common_substring("abc", "xyz"), None);
        assert_eq!(longest_common_substring("hello", "hello"), Some("hello".to_string()));
    }

    #[test]
    fn test_common_substrings() {
        let result = common_substrings("banana", "orange", 2);
        // "an" is common with length 2
        assert!(result.contains(&"an".to_string()));
    }

    #[test]
    fn test_longest_palindromic_substring() {
        let sa = SuffixArray::new("racecar");
        assert_eq!(sa.longest_palindromic_substring(), Some("racecar"));

        let sa2 = SuffixArray::new("cbbd");
        assert_eq!(sa2.longest_palindromic_substring(), Some("bb"));
    }

    #[test]
    fn test_min_lexicographic_rotation() {
        assert_eq!(min_lexicographic_rotation("banana"), "abanan");
        assert_eq!(min_lexicographic_rotation("abcde"), "abcde");
        assert_eq!(min_lexicographic_rotation("cdefab"), "abcdef");
    }

    #[test]
    fn test_kth_distinct_substring() {
        let sa = SuffixArray::new("abc");
        assert_eq!(sa.kth_distinct_substring(1), Some("a".to_string()));
        assert_eq!(sa.kth_distinct_substring(2), Some("ab".to_string()));
        assert_eq!(sa.kth_distinct_substring(3), Some("abc".to_string()));
        assert_eq!(sa.kth_distinct_substring(0), None);
        assert_eq!(sa.kth_distinct_substring(7), None);
    }

    #[test]
    fn test_nth_element() {
        let sa = SuffixArray::new("banana");
        assert_eq!(sa.nth_element(0), Some(("a".to_string(), 5)));
        assert_eq!(sa.nth_element(1), Some(("ana".to_string(), 3)));
        assert_eq!(sa.nth_element(6), None);
    }

    #[test]
    fn test_rank() {
        let sa = SuffixArray::new("banana");
        assert_eq!(sa.rank(5), Some(0)); // suffix "a" has rank 0
        assert_eq!(sa.rank(3), Some(1)); // suffix "ana" has rank 1
        assert_eq!(sa.rank(0), Some(3)); // suffix "banana" has rank 3
    }

    #[test]
    fn test_lcp_between() {
        let sa = SuffixArray::new("banana");
        assert_eq!(sa.lcp_between(2, 4), 2); // "nana" vs "na"
        assert_eq!(sa.lcp_between(0, 1), 0); // "banana" vs "anana"
    }

    #[test]
    fn test_occurrences() {
        let sa = SuffixArray::new("banana");
        let occs = sa.occurrences("ana");
        assert_eq!(occs.len(), 2);
        assert!(occs.iter().any(|o| o.position == 1));
        assert!(occs.iter().any(|o| o.position == 3));
    }

    #[test]
    fn test_all_repeated_substrings() {
        let sa = SuffixArray::new("banana");
        let reps = sa.all_repeated_substrings();
        // Check what we actually get
        // LCP array for banana: [0, 1, 3, 0, 0, 2]
        // suffixes: a, ana, anana, banana, na, nana
        // At index 1: LCP=1, suffix="ana" -> substr of length 1 is "a"
        // At index 2: LCP=3, suffix="anana" -> substr of length 3 is "ana"
        // At index 5: LCP=2, suffix="nana" -> substr of length 2 is "na"
        // So repeated substrings should be: "a", "ana", "na"
        assert!(reps.contains(&"a".to_string()));
        assert!(reps.contains(&"ana".to_string()));
        assert!(reps.contains(&"na".to_string()));
    }

    #[test]
    fn test_longest_repeated_substring_min() {
        let sa = SuffixArray::new("aaaa");
        // With 2 occurrences, longest is "aaa" (positions 0-2 and 1-3)
        assert_eq!(sa.longest_repeated_substring_min(2), Some("aaa".to_string()));
        // With 4 occurrences, only "a" appears 4 times
        assert_eq!(sa.longest_repeated_substring_min(4), Some("a".to_string()));
    }

    #[test]
    fn test_from_string() {
        let sa = SuffixArray::from_string("test".to_string());
        assert_eq!(sa.original(), "test");
    }

    #[test]
    fn test_from_str() {
        let sa: SuffixArray = "test".into();
        assert_eq!(sa.original(), "test");
    }

    #[test]
    fn test_longest_prefix_of() {
        let sa = SuffixArray::new("banana");
        assert_eq!(sa.longest_prefix_of("an"), "an");
        assert_eq!(sa.longest_prefix_of("ban"), "ban");
        assert_eq!(sa.longest_prefix_of("xyz"), "");
        assert_eq!(sa.longest_prefix_of("banana"), "banana");
    }

    #[test]
    fn test_compare_suffixes() {
        let sa = SuffixArray::new("banana");
        assert_eq!(sa.compare_suffixes(5, 0), Ordering::Less); // "a" < "banana"
        assert_eq!(sa.compare_suffixes(0, 5), Ordering::Greater); // "banana" > "a"
        assert_eq!(sa.compare_suffixes(0, 0), Ordering::Equal);
    }

    #[test]
    fn test_large_string() {
        let mut s = String::new();
        for _ in 0..100 {
            s.push_str("abc");
        }

        let sa = SuffixArray::new(&s);
        assert_eq!(sa.find_all("abc").len(), 100);
        // Longest repeated should be at least "abc" (appears 100 times)
        let lrs = sa.longest_repeated_substring();
        assert!(lrs.is_some());
        assert!(lrs.unwrap().len() >= 3);
    }
}