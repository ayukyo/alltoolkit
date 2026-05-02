//! # Levenshtein Utils
//!
//! Comprehensive Levenshtein distance and fuzzy string matching utilities
//! with zero external dependencies.
//!
//! ## Features
//!
//! - **Levenshtein Distance**: Classic edit distance algorithm
//! - **Damerau-Levenshtein**: Extended distance with transpositions
//! - **Optimal String Alignment**: Restricted Damerau-Levenshtein
//! - **Fuzzy Matching**: Threshold-based similarity matching
//! - **Search Functions**: Find closest matches in collections
//! - **Memory Efficient**: Multiple algorithm variants for different use cases
//!
//! ## Example
//!
//! ```rust
//! use levenshtein_utils::{levenshtein_distance, similarity_ratio, find_closest};
//!
//! let dist = levenshtein_distance("kitten", "sitting");
//! assert_eq!(dist, 3);
//!
//! let ratio = similarity_ratio("hello", "hallo");
//! assert_eq!(ratio, 0.8);
//!
//! let words = vec!["apple", "banana", "cherry", "date"];
//! let closest = find_closest("aple", &words);
//! assert_eq!(closest, Some("apple"));
//! ```

use std::cmp::min;

// ============================================================================
// Core Distance Functions
// ============================================================================

/// Calculate the Levenshtein distance between two strings.
///
/// The Levenshtein distance is the minimum number of single-character edits
/// (insertions, deletions, or substitutions) required to change one string
/// into the other.
///
/// # Arguments
///
/// * `a` - First string
/// * `b` - Second string
///
/// # Returns
///
/// The minimum number of edits required to transform `a` into `b`.
///
/// # Time Complexity
///
/// O(m * n) where m and n are the lengths of the input strings.
///
/// # Space Complexity
///
/// O(min(m, n)) - uses optimized two-row algorithm.
///
/// # Examples
///
/// ```
/// use levenshtein_utils::levenshtein_distance;
///
/// assert_eq!(levenshtein_distance("", ""), 0);
/// assert_eq!(levenshtein_distance("a", ""), 1);
/// assert_eq!(levenshtein_distance("", "a"), 1);
/// assert_eq!(levenshtein_distance("kitten", "sitting"), 3);
/// assert_eq!(levenshtein_distance("book", "back"), 2);
/// ```
pub fn levenshtein_distance(a: &str, b: &str) -> usize {
    if a.is_empty() {
        return b.chars().count();
    }
    if b.is_empty() {
        return a.chars().count();
    }

    let a_chars: Vec<char> = a.chars().collect();
    let b_chars: Vec<char> = b.chars().collect();

    // Optimize by using shorter string for column iteration
    if a_chars.len() < b_chars.len() {
        return levenshtein_distance_impl(&b_chars, &a_chars);
    }
    levenshtein_distance_impl(&a_chars, &b_chars)
}

/// Internal implementation using two-row optimization.
fn levenshtein_distance_impl(longer: &[char], shorter: &[char]) -> usize {
    let shorter_len = shorter.len();

    // Previous row of distances
    let mut prev_row: Vec<usize> = (0..=shorter_len).collect();

    for (i, &long_char) in longer.iter().enumerate() {
        let mut curr_row = vec![i + 1; shorter_len + 1];

        for (j, &short_char) in shorter.iter().enumerate() {
            let cost = if long_char == short_char { 0 } else { 1 };
            curr_row[j + 1] = min(
                min(
                    curr_row[j] + 1,       // deletion
                    prev_row[j + 1] + 1,   // insertion
                ),
                prev_row[j] + cost,        // substitution
            );
        }

        prev_row = curr_row;
    }

    prev_row[shorter_len]
}

/// Calculate the Levenshtein distance with full matrix (for debugging/visualization).
///
/// This version uses a full matrix and returns it, which is useful for
/// understanding the algorithm or visualizing the edit path.
///
/// # Returns
///
/// A tuple containing (distance, full_matrix) where matrix[i][j] represents
/// the distance between the first i characters of `a` and first j characters of `b`.
pub fn levenshtein_distance_matrix(a: &str, b: &str) -> (usize, Vec<Vec<usize>>) {
    let a_chars: Vec<char> = a.chars().collect();
    let b_chars: Vec<char> = b.chars().collect();

    let m = a_chars.len();
    let n = b_chars.len();

    let mut matrix = vec![vec![0; n + 1]; m + 1];

    // Initialize first column
    for i in 0..=m {
        matrix[i][0] = i;
    }

    // Initialize first row
    for j in 0..=n {
        matrix[0][j] = j;
    }

    // Fill the matrix
    for (i, &a_char) in a_chars.iter().enumerate() {
        for (j, &b_char) in b_chars.iter().enumerate() {
            let cost = if a_char == b_char { 0 } else { 1 };
            matrix[i + 1][j + 1] = min(
                min(
                    matrix[i][j + 1] + 1,   // deletion
                    matrix[i + 1][j] + 1,   // insertion
                ),
                matrix[i][j] + cost,        // substitution
            );
        }
    }

    (matrix[m][n], matrix)
}

// ============================================================================
// Damerau-Levenshtein Distance (OSA variant)
// ============================================================================

/// Calculate the Damerau-Levenshtein distance between two strings.
///
/// This extends the Levenshtein distance by also allowing transpositions
/// of adjacent characters as a single edit operation.
///
/// Note: This implementation uses the Optimal String Alignment (OSA) variant,
/// which allows transpositions but each substring can only be edited once.
///
/// # Arguments
///
/// * `a` - First string
/// * `b` - Second string
///
/// # Returns
///
/// The minimum number of edits (including transpositions) required.
///
/// # Examples
///
/// ```
/// use levenshtein_utils::damerau_levenshtein_distance;
///
/// // Regular Levenshtein would return 2 for this, but with transposition it's 1
/// assert_eq!(damerau_levenshtein_distance("ca", "ac"), 1);
///
/// // Transposition case
/// assert_eq!(damerau_levenshtein_distance("ab", "ba"), 1);
/// ```
pub fn damerau_levenshtein_distance(a: &str, b: &str) -> usize {
    osa_distance(a, b)
}

/// Calculate the Optimal String Alignment (OSA) distance.
///
/// Also known as restricted Damerau-Levenshtein distance. This version
/// allows transpositions but each substring can only be edited once.
///
/// # Examples
///
/// ```
/// use levenshtein_utils::osa_distance;
///
/// assert_eq!(osa_distance("ca", "abc"), 3);
/// assert_eq!(osa_distance("ab", "ba"), 1);
/// ```
pub fn osa_distance(a: &str, b: &str) -> usize {
    let a_chars: Vec<char> = a.chars().collect();
    let b_chars: Vec<char> = b.chars().collect();

    let m = a_chars.len();
    let n = b_chars.len();

    if m == 0 {
        return n;
    }
    if n == 0 {
        return m;
    }

    let mut matrix = vec![vec![0; n + 1]; m + 1];

    // Initialize first column and row
    for i in 0..=m {
        matrix[i][0] = i;
    }
    for j in 0..=n {
        matrix[0][j] = j;
    }

    // Fill the matrix
    for i in 1..=m {
        for j in 1..=n {
            let cost = if a_chars[i - 1] == b_chars[j - 1] { 0 } else { 1 };

            matrix[i][j] = min(
                min(
                    matrix[i - 1][j] + 1,       // deletion
                    matrix[i][j - 1] + 1,       // insertion
                ),
                matrix[i - 1][j - 1] + cost,    // substitution
            );

            // Transposition (only if adjacent characters are swapped)
            if i > 1 && j > 1
                && a_chars[i - 1] == b_chars[j - 2]
                && a_chars[i - 2] == b_chars[j - 1]
            {
                matrix[i][j] = min(matrix[i][j], matrix[i - 2][j - 2] + 1);
            }
        }
    }

    matrix[m][n]
}

// ============================================================================
// Similarity Functions
// ============================================================================

/// Calculate the similarity ratio between two strings (0.0 to 1.0).
///
/// A ratio of 1.0 means the strings are identical, while 0.0 means
/// they are completely different.
///
/// # Formula
///
/// ratio = 1.0 - (distance / max(len(a), len(b)))
///
/// # Examples
///
/// ```
/// use levenshtein_utils::similarity_ratio;
///
/// assert_eq!(similarity_ratio("hello", "hello"), 1.0);
/// assert_eq!(similarity_ratio("hello", "hallo"), 0.8);
/// assert_eq!(similarity_ratio("", ""), 1.0);
/// ```
pub fn similarity_ratio(a: &str, b: &str) -> f64 {
    if a.is_empty() && b.is_empty() {
        return 1.0;
    }

    let a_len = a.chars().count();
    let b_len = b.chars().count();
    let max_len = a_len.max(b_len);
    
    if max_len == 0 {
        return 1.0;
    }

    let distance = levenshtein_distance(a, b);
    1.0 - (distance as f64 / max_len as f64)
}

/// Calculate normalized Levenshtein distance (0.0 to 1.0).
///
/// This is the inverse of similarity_ratio.
pub fn normalized_distance(a: &str, b: &str) -> f64 {
    1.0 - similarity_ratio(a, b)
}

/// Calculate Jaro similarity between two strings.
///
/// Jaro similarity is a measure of similarity between two strings
/// that accounts for transpositions of characters.
///
/// # Examples
///
/// ```
/// use levenshtein_utils::jaro_similarity;
///
/// let sim = jaro_similarity("MARTHA", "MARHTA");
/// assert!(sim > 0.94);
/// ```
pub fn jaro_similarity(a: &str, b: &str) -> f64 {
    let a_chars: Vec<char> = a.chars().collect();
    let b_chars: Vec<char> = b.chars().collect();

    let m = a_chars.len();
    let n = b_chars.len();

    if m == 0 && n == 0 {
        return 1.0;
    }
    if m == 0 || n == 0 {
        return 0.0;
    }

    // Matching distance
    let match_distance = (m.max(n) / 2).saturating_sub(1);

    let mut a_matches = vec![false; m];
    let mut b_matches = vec![false; n];

    let mut matches = 0usize;
    let mut transpositions = 0usize;

    // Find matches
    for (i, &a_char) in a_chars.iter().enumerate() {
        let start = i.saturating_sub(match_distance);
        let end = (i + match_distance + 1).min(n);

        for j in start..end {
            if b_matches[j] || b_chars[j] != a_char {
                continue;
            }
            a_matches[i] = true;
            b_matches[j] = true;
            matches += 1;
            break;
        }
    }

    if matches == 0 {
        return 0.0;
    }

    // Count transpositions
    let mut k = 0;
    for (i, &matched) in a_matches.iter().enumerate() {
        if matched {
            while !b_matches[k] {
                k += 1;
            }
            if a_chars[i] != b_chars[k] {
                transpositions += 1;
            }
            k += 1;
        }
    }

    let matches = matches as f64;
    let transpositions = (transpositions as f64) / 2.0;

    (matches / m as f64 + matches / n as f64 + (matches - transpositions) / matches) / 3.0
}

/// Calculate Jaro-Winkler similarity between two strings.
///
/// Jaro-Winkler gives extra weight to strings that match from the beginning.
/// This is especially useful for comparing names and short strings.
///
/// # Examples
///
/// ```
/// use levenshtein_utils::jaro_winkler_similarity;
///
/// let sim = jaro_winkler_similarity("MARTHA", "MARHTA");
/// assert!(sim > 0.96);
///
/// let sim2 = jaro_winkler_similarity("hello", "hallo");
/// assert!(sim2 > 0.84);
/// ```
pub fn jaro_winkler_similarity(a: &str, b: &str) -> f64 {
    let jaro = jaro_similarity(a, b);

    // Find common prefix length (up to 4 characters)
    let prefix_len = a.chars()
        .zip(b.chars())
        .take_while(|(a, b)| a == b)
        .count()
        .min(4);

    let scaling_factor = 0.1;
    jaro + (prefix_len as f64 * scaling_factor * (1.0 - jaro))
}

// ============================================================================
// Fuzzy Search Functions
// ============================================================================

/// Find the closest match to a query string in a list of candidates.
///
/// # Returns
///
/// `Some(closest_string)` if any candidate exists, `None` if the list is empty.
///
/// # Examples
///
/// ```
/// use levenshtein_utils::find_closest;
///
/// let words = vec!["apple", "banana", "cherry", "date"];
/// assert_eq!(find_closest("aple", &words), Some("apple"));
/// assert_eq!(find_closest("bnana", &words), Some("banana"));
/// ```
pub fn find_closest<'a>(query: &str, candidates: &[&'a str]) -> Option<&'a str> {
    candidates
        .iter()
        .map(|&c| (c, levenshtein_distance(query, c)))
        .min_by_key(|&(_, dist)| dist)
        .map(|(c, _)| c)
}

/// Find all matches within a maximum edit distance threshold.
///
/// # Examples
///
/// ```
/// use levenshtein_utils::find_matches;
///
/// let words = vec!["apple", "apply", "banana", "orange"];
/// let matches = find_matches("aple", &words, 2);
/// assert_eq!(matches, vec!["apple", "apply"]);
/// ```
pub fn find_matches<'a>(query: &str, candidates: &[&'a str], max_distance: usize) -> Vec<&'a str> {
    candidates
        .iter()
        .filter(|&&c| levenshtein_distance(query, c) <= max_distance)
        .copied()
        .collect()
}

/// Find all matches above a similarity threshold.
///
/// # Examples
///
/// ```
/// use levenshtein_utils::find_similar;
///
/// let words = vec!["hello", "hallo", "hola", "hi"];
/// let similar = find_similar("hello", &words, 0.7);
/// assert!(similar.contains(&"hello"));
/// assert!(similar.contains(&"hallo"));
/// ```
pub fn find_similar<'a>(query: &str, candidates: &[&'a str], min_ratio: f64) -> Vec<&'a str> {
    candidates
        .iter()
        .filter(|&&c| similarity_ratio(query, c) >= min_ratio)
        .copied()
        .collect()
}

/// Match result with score.
#[derive(Debug, Clone, PartialEq)]
pub struct MatchResult<'a> {
    pub value: &'a str,
    pub distance: usize,
    pub similarity: f64,
}

/// Find top N closest matches sorted by distance.
///
/// # Examples
///
/// ```
/// use levenshtein_utils::find_top_matches;
///
/// let words = vec!["apple", "apply", "apt", "banana"];
/// let top2 = find_top_matches("aple", &words, 2);
/// assert_eq!(top2.len(), 2);
/// assert_eq!(top2[0].value, "apple");
/// ```
pub fn find_top_matches<'a>(query: &str, candidates: &[&'a str], n: usize) -> Vec<MatchResult<'a>> {
    let mut results: Vec<MatchResult> = candidates
        .iter()
        .map(|&c| {
            let dist = levenshtein_distance(query, c);
            let sim = similarity_ratio(query, c);
            MatchResult {
                value: c,
                distance: dist,
                similarity: sim,
            }
        })
        .collect();

    results.sort_by(|a, b| a.distance.cmp(&b.distance));
    results.truncate(n);
    results
}

// ============================================================================
// Edit Operations
// ============================================================================

/// Edit operation types.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum EditOp {
    Insert(usize, char),
    Delete(usize, char),
    Substitute(usize, char, char),
    Transpose(usize, usize),
    Match(usize, char),
}

/// Get the sequence of edit operations to transform `a` into `b`.
///
/// # Returns
///
/// A vector of edit operations in order.
///
/// # Examples
///
/// ```
/// use levenshtein_utils::{edit_operations, EditOp};
///
/// let ops = edit_operations("kitten", "sitting");
/// assert!(ops.len() > 0);
/// ```
pub fn edit_operations(a: &str, b: &str) -> Vec<EditOp> {
    let a_chars: Vec<char> = a.chars().collect();
    let b_chars: Vec<char> = b.chars().collect();

    let m = a_chars.len();
    let n = b_chars.len();

    // Build the full matrix for backtracking
    let mut matrix = vec![vec![0; n + 1]; m + 1];

    for i in 0..=m {
        matrix[i][0] = i;
    }
    for j in 0..=n {
        matrix[0][j] = j;
    }

    for i in 1..=m {
        for j in 1..=n {
            let cost = if a_chars[i - 1] == b_chars[j - 1] { 0 } else { 1 };
            matrix[i][j] = min(
                min(matrix[i - 1][j] + 1, matrix[i][j - 1] + 1),
                matrix[i - 1][j - 1] + cost,
            );
        }
    }

    // Backtrack to find operations
    let mut ops = Vec::new();
    let mut i = m;
    let mut j = n;

    while i > 0 || j > 0 {
        if i > 0 && j > 0 && a_chars[i - 1] == b_chars[j - 1] {
            ops.push(EditOp::Match(i - 1, a_chars[i - 1]));
            i -= 1;
            j -= 1;
        } else if i > 0 && j > 0 && matrix[i][j] == matrix[i - 1][j - 1] + 1 {
            ops.push(EditOp::Substitute(i - 1, a_chars[i - 1], b_chars[j - 1]));
            i -= 1;
            j -= 1;
        } else if j > 0 && (i == 0 || matrix[i][j] == matrix[i][j - 1] + 1) {
            ops.push(EditOp::Insert(j - 1, b_chars[j - 1]));
            j -= 1;
        } else if i > 0 {
            ops.push(EditOp::Delete(i - 1, a_chars[i - 1]));
            i -= 1;
        }
    }

    ops.reverse();
    ops
}

// ============================================================================
// Hamming Distance
// ============================================================================

/// Calculate the Hamming distance between two strings.
///
/// Hamming distance is the number of positions at which the corresponding
/// characters are different. The strings must be of equal length.
///
/// # Panics
///
/// Panics if the strings have different lengths.
///
/// # Examples
///
/// ```
/// use levenshtein_utils::hamming_distance;
///
/// assert_eq!(hamming_distance("karolin", "kathrin"), 3);
/// assert_eq!(hamming_distance("1011101", "1001001"), 2);
/// ```
pub fn hamming_distance(a: &str, b: &str) -> usize {
    let a_chars: Vec<char> = a.chars().collect();
    let b_chars: Vec<char> = b.chars().collect();

    assert_eq!(
        a_chars.len(),
        b_chars.len(),
        "Hamming distance requires strings of equal length"
    );

    a_chars
        .iter()
        .zip(b_chars.iter())
        .filter(|(a, b)| a != b)
        .count()
}

/// Calculate Hamming distance with a default value for strings of different lengths.
///
/// Returns None if strings have different lengths.
pub fn hamming_distance_safe(a: &str, b: &str) -> Option<usize> {
    let a_chars: Vec<char> = a.chars().collect();
    let b_chars: Vec<char> = b.chars().collect();

    if a_chars.len() != b_chars.len() {
        return None;
    }

    Some(
        a_chars
            .iter()
            .zip(b_chars.iter())
            .filter(|(a, b)| a != b)
            .count(),
    )
}

// ============================================================================
// Longest Common Subsequence
// ============================================================================

/// Calculate the length of the longest common subsequence.
///
/// # Examples
///
/// ```
/// use levenshtein_utils::lcs_length;
///
/// assert_eq!(lcs_length("ABCBDAB", "BDCABA"), 4);
/// assert_eq!(lcs_length("kitten", "sitting"), 4);
/// ```
pub fn lcs_length(a: &str, b: &str) -> usize {
    let a_chars: Vec<char> = a.chars().collect();
    let b_chars: Vec<char> = b.chars().collect();

    let m = a_chars.len();
    let n = b_chars.len();

    if m == 0 || n == 0 {
        return 0;
    }

    let mut prev_row = vec![0; n + 1];

    for &a_char in &a_chars {
        let mut curr_row = vec![0; n + 1];

        for (j, &b_char) in b_chars.iter().enumerate() {
            curr_row[j + 1] = if a_char == b_char {
                prev_row[j] + 1
            } else {
                prev_row[j + 1].max(curr_row[j])
            };
        }

        prev_row = curr_row;
    }

    prev_row[n]
}

/// Get the longest common subsequence as a string.
///
/// # Examples
///
/// ```
/// use levenshtein_utils::lcs_string;
///
/// let result = lcs_string("ABCBDAB", "BDCABA");
/// assert!(result.contains("BCBA") || result.contains("BDAB"));
/// ```
pub fn lcs_string(a: &str, b: &str) -> String {
    let a_chars: Vec<char> = a.chars().collect();
    let b_chars: Vec<char> = b.chars().collect();

    let m = a_chars.len();
    let n = b_chars.len();

    if m == 0 || n == 0 {
        return String::new();
    }

    // Build full matrix
    let mut matrix = vec![vec![0; n + 1]; m + 1];

    for i in 1..=m {
        for j in 1..=n {
            matrix[i][j] = if a_chars[i - 1] == b_chars[j - 1] {
                matrix[i - 1][j - 1] + 1
            } else {
                matrix[i - 1][j].max(matrix[i][j - 1])
            };
        }
    }

    // Backtrack to find LCS
    let mut result = Vec::new();
    let mut i = m;
    let mut j = n;

    while i > 0 && j > 0 {
        if a_chars[i - 1] == b_chars[j - 1] {
            result.push(a_chars[i - 1]);
            i -= 1;
            j -= 1;
        } else if matrix[i - 1][j] > matrix[i][j - 1] {
            i -= 1;
        } else {
            j -= 1;
        }
    }

    result.reverse();
    result.into_iter().collect()
}

// ============================================================================
// Diff Visualization
// ============================================================================

/// Generate a diff visualization between two strings.
///
/// # Examples
///
/// ```
/// use levenshtein_utils::diff;
///
/// let result = diff("kitten", "sitting");
/// assert!(result.contains("-k") || result.contains("+s") || result.contains("~"));
/// ```
pub fn diff(a: &str, b: &str) -> String {
    let ops = edit_operations(a, b);
    let a_chars: Vec<char> = a.chars().collect();
    let mut result = String::new();

    for op in ops {
        match op {
            EditOp::Match(_, c) => {
                result.push(c);
            }
            EditOp::Insert(_, c) => {
                result.push_str(&format!("+{}", c));
            }
            EditOp::Delete(_, c) => {
                result.push_str(&format!("-{}", c));
            }
            EditOp::Substitute(_, old, new) => {
                result.push_str(&format!("~{}→{}", old, new));
            }
            EditOp::Transpose(i, j) => {
                result.push_str(&format!("⟨{}↔{}⟩", a_chars[i], a_chars[j]));
            }
        }
    }

    result
}

// ============================================================================
// Tests
// ============================================================================

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_levenshtein_distance_basic() {
        assert_eq!(levenshtein_distance("", ""), 0);
        assert_eq!(levenshtein_distance("a", ""), 1);
        assert_eq!(levenshtein_distance("", "a"), 1);
        assert_eq!(levenshtein_distance("abc", "abc"), 0);
        assert_eq!(levenshtein_distance("kitten", "sitting"), 3);
        assert_eq!(levenshtein_distance("saturday", "sunday"), 3);
        assert_eq!(levenshtein_distance("book", "back"), 2);
    }

    #[test]
    fn test_levenshtein_distance_unicode() {
        assert_eq!(levenshtein_distance("你好", "你好"), 0);
        assert_eq!(levenshtein_distance("你好", "您好"), 1);
        assert_eq!(levenshtein_distance("日本語", "日本"), 1);
    }

    #[test]
    fn test_similarity_ratio() {
        assert_eq!(similarity_ratio("hello", "hello"), 1.0);
        assert_eq!(similarity_ratio("", ""), 1.0);
        
        let ratio = similarity_ratio("hello", "hallo");
        assert!((ratio - 0.8).abs() < 0.01);
        
        let ratio = similarity_ratio("kitten", "sitting");
        assert!((ratio - 0.571).abs() < 0.01);
    }

    #[test]
    fn test_find_closest() {
        let words = vec!["apple", "banana", "cherry", "date"];
        assert_eq!(find_closest("aple", &words), Some("apple"));
        assert_eq!(find_closest("bnana", &words), Some("banana"));
        assert_eq!(find_closest("chery", &words), Some("cherry"));
    }

    #[test]
    fn test_find_matches() {
        let words = vec!["apple", "apply", "banana", "orange"];
        let matches = find_matches("aple", &words, 2);
        assert_eq!(matches, vec!["apple", "apply"]);
    }

    #[test]
    fn test_damerau_levenshtein() {
        // OSA variant - transposition allowed
        assert_eq!(damerau_levenshtein_distance("ca", "ac"), 1);
        assert_eq!(levenshtein_distance("ca", "ac"), 2);
        assert_eq!(damerau_levenshtein_distance("ab", "ba"), 1);
    }

    #[test]
    fn test_osa_distance() {
        assert_eq!(osa_distance("ab", "ba"), 1);
        assert_eq!(osa_distance("ca", "abc"), 3);
        assert_eq!(osa_distance("ca", "ac"), 1);
    }

    #[test]
    fn test_jaro_similarity() {
        let sim = jaro_similarity("MARTHA", "MARHTA");
        assert!(sim > 0.94);

        let sim = jaro_similarity("hello", "hallo");
        assert!(sim > 0.73);
    }

    #[test]
    fn test_jaro_winkler() {
        let sim = jaro_winkler_similarity("MARTHA", "MARHTA");
        assert!(sim > 0.96);
        
        let sim = jaro_winkler_similarity("hello", "hello");
        assert_eq!(sim, 1.0);
    }

    #[test]
    fn test_hamming_distance() {
        assert_eq!(hamming_distance("karolin", "kathrin"), 3);
        assert_eq!(hamming_distance("1011101", "1001001"), 2);
        assert_eq!(hamming_distance_safe("abc", "abcd"), None);
    }

    #[test]
    fn test_lcs() {
        assert_eq!(lcs_length("ABCBDAB", "BDCABA"), 4);
        assert_eq!(lcs_length("kitten", "sitting"), 4);
        
        let lcs = lcs_string("ABCBDAB", "BDCABA");
        assert!(lcs.len() == 4);
    }

    #[test]
    fn test_edit_operations() {
        let ops = edit_operations("kitten", "sitting");
        assert!(!ops.is_empty());
        
        // Verify the number of non-match operations equals the distance
        let non_matches: Vec<_> = ops.iter().filter(|op| !matches!(op, EditOp::Match(_, _))).collect();
        assert_eq!(non_matches.len(), 3);
    }

    #[test]
    fn test_find_top_matches() {
        let words = vec!["apple", "apply", "apt", "banana"];
        let top2 = find_top_matches("aple", &words, 2);
        
        assert_eq!(top2.len(), 2);
        assert_eq!(top2[0].value, "apple");
        assert!(top2[0].similarity > top2[1].similarity);
    }

    #[test]
    fn test_diff() {
        let d = diff("hello", "hallo");
        assert!(d.contains("~e→a") || d.contains("+a") || d.contains("-e"));
    }
}