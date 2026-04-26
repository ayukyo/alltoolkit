//! # Text Distance Utilities
//!
//! A comprehensive collection of string/text distance and similarity algorithms.
//! All algorithms are implemented from scratch with zero external dependencies.
//!
//! ## Features
//!
//! - **Edit Distance Metrics**: Hamming, Levenshtein, Damerau-Levenshtein
//! - **Similarity Measures**: Jaro, Jaro-Winkler, Cosine, Sorensen-Dice
//! - **Phonetic Algorithms**: Soundex (for comparison)
//! - **N-gram based**: N-gram similarity, Q-gram distance
//!
//! ## Usage
//!
//! ```rust
//! use text_distance_utils::{
//!     hamming_distance, levenshtein_distance, damerau_levenshtein_distance,
//!     jaro_similarity, jaro_winkler_similarity, cosine_similarity, dice_coefficient
//! };
//!
//! // Edit distances
//! let dist = hamming_distance("karolin", "kathrin");  // 3
//! let dist = levenshtein_distance("kitten", "sitting");  // 3
//! let dist = damerau_levenshtein_distance("ca", "abc");  // 2
//!
//! // Similarity scores (0.0 to 1.0)
//! let sim = jaro_similarity("MARTHA", "MARHTA");  // ~0.944
//! let sim = jaro_winkler_similarity("MARTHA", "MARHTA");  // ~0.961
//! let sim = cosine_similarity("hello world", "world hello");  // 1.0
//! let sim = dice_coefficient("night", "nacht");  // ~0.25
//! ```

use std::collections::{HashMap, HashSet};

// ============================================================================
// HAMMING DISTANCE
// ============================================================================

/// Computes the Hamming distance between two strings.
///
/// The Hamming distance is the number of positions at which the corresponding
/// characters are different. Both strings must have the same length.
///
/// # Arguments
///
/// * `s1` - First string
/// * `s2` - Second string (must have same length as s1)
///
/// # Returns
///
/// * `Ok(usize)` - The Hamming distance
/// * `Err(String)` - Error if strings have different lengths
///
/// # Time Complexity
///
/// O(n) where n is the length of the strings
///
/// # Examples
///
/// ```
/// use text_distance_utils::hamming_distance;
///
/// assert_eq!(hamming_distance("karolin", "kathrin"), Ok(3));
/// assert_eq!(hamming_distance("0000", "1111"), Ok(4));
/// assert_eq!(hamming_distance("hello", "hello"), Ok(0));
/// ```
pub fn hamming_distance(s1: &str, s2: &str) -> Result<usize, String> {
    let chars1: Vec<char> = s1.chars().collect();
    let chars2: Vec<char> = s2.chars().collect();

    if chars1.len() != chars2.len() {
        return Err(format!(
            "Strings must have equal length: {} vs {}",
            chars1.len(),
            chars2.len()
        ));
    }

    Ok(chars1
        .iter()
        .zip(chars2.iter())
        .filter(|(c1, c2)| c1 != c2)
        .count())
}

/// Computes the Hamming similarity between two strings.
///
/// Returns a value between 0.0 and 1.0, where 1.0 means identical.
///
/// # Examples
///
/// ```
/// use text_distance_utils::hamming_similarity;
///
/// assert_eq!(hamming_similarity("karolin", "kathrin"), Ok(4.0/7.0));
/// ```
pub fn hamming_similarity(s1: &str, s2: &str) -> Result<f64, String> {
    let distance = hamming_distance(s1, s2)?;
    let len = s1.chars().count();
    if len == 0 {
        return Ok(1.0);
    }
    Ok(1.0 - (distance as f64 / len as f64))
}

// ============================================================================
// LEVENSHTEIN DISTANCE
// ============================================================================

/// Computes the Levenshtein distance between two strings.
///
/// The Levenshtein distance is the minimum number of single-character edits
/// (insertions, deletions, or substitutions) required to change one string
/// into the other.
///
/// # Arguments
///
/// * `s1` - First string
/// * `s2` - Second string
///
/// # Returns
///
/// The minimum number of edits required to transform s1 into s2.
///
/// # Time Complexity
///
/// O(m * n) where m and n are the lengths of the strings
///
/// # Space Complexity
///
/// O(min(m, n)) using optimized two-row algorithm
///
/// # Examples
///
/// ```
/// use text_distance_utils::levenshtein_distance;
///
/// assert_eq!(levenshtein_distance("kitten", "sitting"), 3);
/// assert_eq!(levenshtein_distance("book", "back"), 2);
/// assert_eq!(levenshtein_distance("", "hello"), 5);
/// ```
pub fn levenshtein_distance(s1: &str, s2: &str) -> usize {
    let chars1: Vec<char> = s1.chars().collect();
    let chars2: Vec<char> = s2.chars().collect();

    let len1 = chars1.len();
    let len2 = chars2.len();

    // Handle edge cases
    if len1 == 0 {
        return len2;
    }
    if len2 == 0 {
        return len1;
    }

    // Use two rows instead of full matrix for space efficiency
    let mut prev_row: Vec<usize> = (0..=len2).collect();
    let mut curr_row: Vec<usize> = vec![0; len2 + 1];

    for (i, c1) in chars1.iter().enumerate() {
        curr_row[0] = i + 1;

        for (j, c2) in chars2.iter().enumerate() {
            let cost = if c1 == c2 { 0 } else { 1 };

            curr_row[j + 1] = (prev_row[j + 1] + 1) // deletion
                .min(curr_row[j] + 1) // insertion
                .min(prev_row[j] + cost); // substitution
        }

        std::mem::swap(&mut prev_row, &mut curr_row);
    }

    prev_row[len2]
}

/// Computes the Levenshtein similarity between two strings.
///
/// Returns a value between 0.0 and 1.0, where 1.0 means identical.
///
/// # Examples
///
/// ```
/// use text_distance_utils::levenshtein_similarity;
///
/// let sim = levenshtein_similarity("kitten", "sitting");
/// assert!(sim > 0.5 && sim < 0.7);
/// ```
pub fn levenshtein_similarity(s1: &str, s2: &str) -> f64 {
    let len1 = s1.chars().count();
    let len2 = s2.chars().count();
    let max_len = len1.max(len2);

    if max_len == 0 {
        return 1.0;
    }

    let distance = levenshtein_distance(s1, s2);
    1.0 - (distance as f64 / max_len as f64)
}

// ============================================================================
// DAMERAU-LEVENSHTEIN DISTANCE
// ============================================================================

/// Computes the Damerau-Levenshtein distance between two strings.
///
/// Like Levenshtein distance but also allows transposition of adjacent
/// characters as a single edit operation.
///
/// # Arguments
///
/// * `s1` - First string
/// * `s2` - Second string
///
/// # Returns
///
/// The minimum number of edits (including transpositions) required.
///
/// # Time Complexity
///
/// O(m * n) where m and n are the lengths of the strings
///
/// # Examples
///
/// ```
/// use text_distance_utils::damerau_levenshtein_distance;
///
/// // Transposition counts as 1 edit (vs 2 for regular Levenshtein)
/// assert_eq!(damerau_levenshtein_distance("ca", "ac"), 1);
/// assert_eq!(damerau_levenshtein_distance("abcd", "acbd"), 1);
/// ```
pub fn damerau_levenshtein_distance(s1: &str, s2: &str) -> usize {
    let chars1: Vec<char> = s1.chars().collect();
    let chars2: Vec<char> = s2.chars().collect();

    let len1 = chars1.len();
    let len2 = chars2.len();

    if len1 == 0 {
        return len2;
    }
    if len2 == 0 {
        return len1;
    }

    // Create distance matrix
    let mut matrix: Vec<Vec<usize>> = vec![vec![0; len2 + 1]; len1 + 1];

    // Initialize first row and column
    for i in 0..=len1 {
        matrix[i][0] = i;
    }
    for j in 0..=len2 {
        matrix[0][j] = j;
    }

    // Fill the matrix
    for i in 1..=len1 {
        for j in 1..=len2 {
            let cost = if chars1[i - 1] == chars2[j - 1] { 0 } else { 1 };

            matrix[i][j] = (matrix[i - 1][j] + 1) // deletion
                .min(matrix[i][j - 1] + 1) // insertion
                .min(matrix[i - 1][j - 1] + cost); // substitution

            // Check for transposition
            if i > 1 && j > 1 && chars1[i - 1] == chars2[j - 2] && chars1[i - 2] == chars2[j - 1] {
                matrix[i][j] = matrix[i][j].min(matrix[i - 2][j - 2] + cost);
            }
        }
    }

    matrix[len1][len2]
}

/// Computes the Damerau-Levenshtein similarity between two strings.
///
/// Returns a value between 0.0 and 1.0.
pub fn damerau_levenshtein_similarity(s1: &str, s2: &str) -> f64 {
    let len1 = s1.chars().count();
    let len2 = s2.chars().count();
    let max_len = len1.max(len2);

    if max_len == 0 {
        return 1.0;
    }

    let distance = damerau_levenshtein_distance(s1, s2);
    1.0 - (distance as f64 / max_len as f64)
}

// ============================================================================
// JARO SIMILARITY
// ============================================================================

/// Computes the Jaro similarity between two strings.
///
/// Jaro similarity is a measure of similarity between two strings.
/// The higher the Jaro similarity, the more similar the strings are.
///
/// # Arguments
///
/// * `s1` - First string
/// * `s2` - Second string
///
/// # Returns
///
/// A value between 0.0 (no similarity) and 1.0 (identical).
///
/// # Examples
///
/// ```
/// use text_distance_utils::jaro_similarity;
///
/// assert!((jaro_similarity("MARTHA", "MARHTA") - 0.944).abs() < 0.01);
/// assert_eq!(jaro_similarity("hello", "hello"), 1.0);
/// assert_eq!(jaro_similarity("", ""), 1.0);
/// ```
pub fn jaro_similarity(s1: &str, s2: &str) -> f64 {
    let chars1: Vec<char> = s1.chars().collect();
    let chars2: Vec<char> = s2.chars().collect();

    let len1 = chars1.len();
    let len2 = chars2.len();

    // Both empty strings are considered equal
    if len1 == 0 && len2 == 0 {
        return 1.0;
    }

    // One empty string means zero similarity
    if len1 == 0 || len2 == 0 {
        return 0.0;
    }

    // Calculate the match distance
    let match_distance = (len1.max(len2) / 2).saturating_sub(1);

    let mut s1_matches = vec![false; len1];
    let mut s2_matches = vec![false; len2];

    let mut matches = 0usize;
    let mut transpositions = 0usize;

    // Find matches
    for (i, &c1) in chars1.iter().enumerate() {
        let start = i.saturating_sub(match_distance);
        let end = (i + match_distance + 1).min(len2);

        for j in start..end {
            if s2_matches[j] || chars2[j] != c1 {
                continue;
            }
            s1_matches[i] = true;
            s2_matches[j] = true;
            matches += 1;
            break;
        }
    }

    if matches == 0 {
        return 0.0;
    }

    // Count transpositions
    let mut k = 0;
    for (i, &matched) in s1_matches.iter().enumerate() {
        if matched {
            while !s2_matches[k] {
                k += 1;
            }
            if chars1[i] != chars2[k] {
                transpositions += 1;
            }
            k += 1;
        }
    }

    let matches = matches as f64;
    let transpositions = (transpositions / 2) as f64;

    (matches / len1 as f64 + matches / len2 as f64 + (matches - transpositions) / matches) / 3.0
}

// ============================================================================
// JARO-WINKLER SIMILARITY
// ============================================================================

/// Computes the Jaro-Winkler similarity between two strings.
///
/// Jaro-Winkler is a modification of Jaro similarity that gives extra weight
/// to strings that match from the beginning.
///
/// # Arguments
///
/// * `s1` - First string
/// * `s2` - Second string
///
/// # Returns
///
/// A value between 0.0 (no similarity) and 1.0 (identical).
///
/// # Examples
///
/// ```
/// use text_distance_utils::{jaro_similarity, jaro_winkler_similarity};
///
/// // Jaro-Winkler favors strings that match from the start
/// let jaro = jaro_similarity("MARTHA", "MARHTA");
/// let jw = jaro_winkler_similarity("MARTHA", "MARHTA");
/// assert!(jw > jaro);
/// ```
pub fn jaro_winkler_similarity(s1: &str, s2: &str) -> f64 {
    let jaro_sim = jaro_similarity(s1, s2);

    if jaro_sim == 0.0 {
        return 0.0;
    }

    let chars1: Vec<char> = s1.chars().collect();
    let chars2: Vec<char> = s2.chars().collect();

    // Calculate common prefix length (max 4 characters)
    let common_prefix_len = chars1
        .iter()
        .zip(chars2.iter())
        .take(4)
        .take_while(|(c1, c2)| c1 == c2)
        .count();

    // Winkler modification: boost score based on common prefix
    let scaling_factor = 0.1;
    jaro_sim + (common_prefix_len as f64 * scaling_factor * (1.0 - jaro_sim))
}

// ============================================================================
// N-GRAM BASED SIMILARITY
// ============================================================================

/// Generates n-grams (shingles) from a string.
///
/// # Arguments
///
/// * `s` - Input string
/// * `n` - Size of each gram
///
/// # Returns
///
/// A set of n-grams.
///
/// # Examples
///
/// ```
/// use text_distance_utils::generate_ngrams;
///
/// let ngrams = generate_ngrams("hello", 2);
/// assert!(ngrams.contains("he"));
/// assert!(ngrams.contains("el"));
/// assert!(ngrams.contains("ll"));
/// assert!(ngrams.contains("lo"));
/// ```
pub fn generate_ngrams(s: &str, n: usize) -> HashSet<String> {
    if n == 0 || s.is_empty() {
        return HashSet::new();
    }

    let chars: Vec<char> = s.chars().collect();
    if chars.len() < n {
        return HashSet::new();
    }

    (0..=chars.len() - n)
        .map(|i| chars[i..i + n].iter().collect())
        .collect()
}

/// Computes the n-gram similarity between two strings.
///
/// Uses Jaccard similarity on n-gram sets.
///
/// # Arguments
///
/// * `s1` - First string
/// * `s2` - Second string
/// * `n` - Size of n-grams (typically 2 or 3)
///
/// # Returns
///
/// A value between 0.0 and 1.0.
pub fn ngram_similarity(s1: &str, s2: &str, n: usize) -> f64 {
    let ngrams1 = generate_ngrams(s1, n);
    let ngrams2 = generate_ngrams(s2, n);

    if ngrams1.is_empty() && ngrams2.is_empty() {
        return 1.0;
    }

    if ngrams1.is_empty() || ngrams2.is_empty() {
        return 0.0;
    }

    let intersection = ngrams1.intersection(&ngrams2).count();
    let union = ngrams1.union(&ngrams2).count();

    intersection as f64 / union as f64
}

/// Computes the Sørensen-Dice coefficient between two strings.
///
/// The Dice coefficient is a similarity measure that compares the bigrams
/// (2-character sequences) of two strings.
///
/// # Arguments
///
/// * `s1` - First string
/// * `s2` - Second string
///
/// # Returns
///
/// A value between 0.0 and 1.0.
///
/// # Examples
///
/// ```
/// use text_distance_utils::dice_coefficient;
///
/// let coef = dice_coefficient("night", "nacht");
/// assert!(coef > 0.0 && coef < 0.5);
/// ```
pub fn dice_coefficient(s1: &str, s2: &str) -> f64 {
    let bigrams1 = generate_ngrams(s1, 2);
    let bigrams2 = generate_ngrams(s2, 2);

    if bigrams1.is_empty() && bigrams2.is_empty() {
        return 1.0;
    }

    if bigrams1.is_empty() || bigrams2.is_empty() {
        return 0.0;
    }

    let intersection = bigrams1.intersection(&bigrams2).count();

    (2.0 * intersection as f64) / (bigrams1.len() + bigrams2.len()) as f64
}

// ============================================================================
// COSINE SIMILARITY
// ============================================================================

/// Tokenizes a string into words.
///
/// Converts to lowercase and splits on non-alphanumeric characters.
fn tokenize(s: &str) -> Vec<String> {
    s.to_lowercase()
        .split(|c: char| !c.is_alphanumeric())
        .filter(|s| !s.is_empty())
        .map(|s| s.to_string())
        .collect()
}

/// Creates a term frequency map from a list of tokens.
fn term_frequency(tokens: &[String]) -> HashMap<String, usize> {
    let mut tf = HashMap::new();
    for token in tokens {
        *tf.entry(token.clone()).or_insert(0) += 1;
    }
    tf
}

/// Computes the cosine similarity between two strings.
///
/// Treats strings as bags of words and computes cosine similarity
/// of their term frequency vectors.
///
/// # Arguments
///
/// * `s1` - First string
/// * `s2` - Second string
///
/// # Returns
///
/// A value between 0.0 (no shared terms) and 1.0 (identical term distribution).
///
/// # Examples
///
/// ```
/// use text_distance_utils::cosine_similarity;
///
/// // Identical strings have similarity ~1.0
/// assert!((cosine_similarity("hello world", "hello world") - 1.0).abs() < 0.001);
///
/// // No shared words have similarity 0.0
/// assert_eq!(cosine_similarity("hello world", "foo bar"), 0.0);
///
/// // Some overlap
/// let sim = cosine_similarity("the quick brown fox", "the quick blue cat");
/// assert!(sim > 0.0 && sim < 1.0);
/// ```
pub fn cosine_similarity(s1: &str, s2: &str) -> f64 {
    let tokens1 = tokenize(s1);
    let tokens2 = tokenize(s2);

    if tokens1.is_empty() && tokens2.is_empty() {
        return 1.0;
    }

    if tokens1.is_empty() || tokens2.is_empty() {
        return 0.0;
    }

    let tf1 = term_frequency(&tokens1);
    let tf2 = term_frequency(&tokens2);

    // Get all unique terms
    let all_terms: HashSet<&String> = tf1.keys().chain(tf2.keys()).collect();

    // Compute dot product and magnitudes
    let mut dot_product: f64 = 0.0;
    let mut magnitude1: f64 = 0.0;
    let mut magnitude2: f64 = 0.0;

    for term in all_terms {
        let freq1 = tf1.get(term).copied().unwrap_or(0) as f64;
        let freq2 = tf2.get(term).copied().unwrap_or(0) as f64;

        dot_product += freq1 * freq2;
        magnitude1 += freq1 * freq1;
        magnitude2 += freq2 * freq2;
    }

    let magnitude = magnitude1.sqrt() * magnitude2.sqrt();

    if magnitude == 0.0 {
        return 0.0;
    }

    dot_product / magnitude
}

/// Computes the cosine similarity using n-grams instead of words.
///
/// # Arguments
///
/// * `s1` - First string
/// * `s2` - Second string
/// * `n` - Size of n-grams
///
/// # Returns
///
/// A value between 0.0 and 1.0.
pub fn cosine_ngram_similarity(s1: &str, s2: &str, n: usize) -> f64 {
    let ngrams1 = generate_ngrams(s1, n);
    let ngrams2 = generate_ngrams(s2, n);

    if ngrams1.is_empty() && ngrams2.is_empty() {
        return 1.0;
    }

    if ngrams1.is_empty() || ngrams2.is_empty() {
        return 0.0;
    }

    // Get all unique n-grams
    let all_ngrams: HashSet<&String> = ngrams1.iter().chain(ngrams2.iter()).collect();

    // Compute dot product and magnitudes
    let mut dot_product: f64 = 0.0;
    let mut magnitude1: f64 = 0.0;
    let mut magnitude2: f64 = 0.0;

    for ngram in all_ngrams {
        let in_first = ngrams1.contains(ngram) as i32 as f64;
        let in_second = ngrams2.contains(ngram) as i32 as f64;

        dot_product += in_first * in_second;
        magnitude1 += in_first * in_first;
        magnitude2 += in_second * in_second;
    }

    let magnitude = magnitude1.sqrt() * magnitude2.sqrt();

    if magnitude == 0.0 {
        return 0.0;
    }

    dot_product / magnitude
}

// ============================================================================
// OVERLAP COEFFICIENT
// ============================================================================

/// Computes the overlap coefficient (Szymkiewicz-Simpson) between two strings.
///
/// The overlap coefficient measures the overlap between two sets divided
/// by the size of the smaller set.
///
/// # Arguments
///
/// * `s1` - First string
/// * `s2` - Second string
///
/// # Returns
///
/// A value between 0.0 and 1.0.
///
/// # Examples
///
/// ```
/// use text_distance_utils::overlap_coefficient;
///
/// // One string's words are a subset of the other's
/// assert_eq!(overlap_coefficient("hello world", "hello"), 1.0);
/// ```
pub fn overlap_coefficient(s1: &str, s2: &str) -> f64 {
    let tokens1: HashSet<String> = tokenize(s1).into_iter().collect();
    let tokens2: HashSet<String> = tokenize(s2).into_iter().collect();

    if tokens1.is_empty() && tokens2.is_empty() {
        return 1.0;
    }

    if tokens1.is_empty() || tokens2.is_empty() {
        return 0.0;
    }

    let intersection = tokens1.intersection(&tokens2).count();
    let min_size = tokens1.len().min(tokens2.len());

    intersection as f64 / min_size as f64
}

// ============================================================================
// Q-GRAM DISTANCE
// ============================================================================

/// Computes the q-gram distance between two strings.
///
/// The q-gram distance is the number of q-grams that are not shared
/// between the two strings.
///
/// # Arguments
///
/// * `s1` - First string
/// * `s2` - Second string
/// * `q` - Size of q-grams (typically 2 or 3)
///
/// # Returns
///
/// The q-gram distance (non-negative integer).
pub fn qgram_distance(s1: &str, s2: &str, q: usize) -> usize {
    let qgrams1 = generate_ngrams(s1, q);
    let qgrams2 = generate_ngrams(s2, q);

    let union: HashSet<&String> = qgrams1.union(&qgrams2).collect();

    let mut distance = 0;
    for qgram in union {
        let in1 = qgrams1.contains(qgram);
        let in2 = qgrams2.contains(qgram);

        if in1 ^ in2 {
            distance += 1;
        }
    }

    distance
}

// ============================================================================
// LAI DISTANCE (Normalized Levenshtein)
// ============================================================================

/// Computes the normalized Levenshtein distance.
///
/// Returns a value between 0.0 (identical) and 1.0 (completely different).
///
/// # Examples
///
/// ```
/// use text_distance_utils::normalized_levenshtein_distance;
///
/// let dist = normalized_levenshtein_distance("kitten", "sitting");
/// assert!(dist > 0.0 && dist < 1.0);
/// ```
pub fn normalized_levenshtein_distance(s1: &str, s2: &str) -> f64 {
    1.0 - levenshtein_similarity(s1, s2)
}

// ============================================================================
// OPTIMAL STRING ALIGNMENT DISTANCE
// ============================================================================

/// Computes the Optimal String Alignment (OSA) distance.
///
/// Similar to Damerau-Levenshtein but each substring can only be edited once.
///
/// # Examples
///
/// ```
/// use text_distance_utils::osa_distance;
///
/// let dist = osa_distance("ca", "abc");
/// assert_eq!(dist, 3);
/// ```
pub fn osa_distance(s1: &str, s2: &str) -> usize {
    let chars1: Vec<char> = s1.chars().collect();
    let chars2: Vec<char> = s2.chars().collect();

    let len1 = chars1.len();
    let len2 = chars2.len();

    if len1 == 0 {
        return len2;
    }
    if len2 == 0 {
        return len1;
    }

    let mut matrix: Vec<Vec<usize>> = vec![vec![0; len2 + 1]; len1 + 1];

    for i in 0..=len1 {
        matrix[i][0] = i;
    }
    for j in 0..=len2 {
        matrix[0][j] = j;
    }

    for i in 1..=len1 {
        for j in 1..=len2 {
            let cost = if chars1[i - 1] == chars2[j - 1] { 0 } else { 1 };

            matrix[i][j] = (matrix[i - 1][j] + 1) // deletion
                .min(matrix[i][j - 1] + 1) // insertion
                .min(matrix[i - 1][j - 1] + cost); // substitution

            // Transposition (OSA version - each char can only be transposed once)
            if i > 1
                && j > 1
                && chars1[i - 1] == chars2[j - 2]
                && chars1[i - 2] == chars2[j - 1]
            {
                matrix[i][j] = matrix[i][j].min(matrix[i - 2][j - 2] + 1);
            }
        }
    }

    matrix[len1][len2]
}

// ============================================================================
// FUZZY STRING MATCHING
// ============================================================================

/// Finds the best matching string from a list of candidates.
///
/// Uses Levenshtein similarity to find the closest match.
///
/// # Arguments
///
/// * `query` - The string to match
/// * `candidates` - List of candidate strings
///
/// # Returns
///
/// An optional tuple of (best_match_index, similarity_score).
///
/// # Examples
///
/// ```
/// use text_distance_utils::best_match;
///
/// let candidates = vec!["hello", "hallo", "hola", "hi"];
/// let result = best_match("hell", &candidates);
/// assert_eq!(result, Some((0, 0.8)));
/// ```
pub fn best_match(query: &str, candidates: &[&str]) -> Option<(usize, f64)> {
    if candidates.is_empty() {
        return None;
    }

    let mut best_idx = 0;
    let mut best_score = levenshtein_similarity(query, candidates[0]);

    for (i, candidate) in candidates.iter().enumerate().skip(1) {
        let score = levenshtein_similarity(query, candidate);
        if score > best_score {
            best_score = score;
            best_idx = i;
        }
    }

    Some((best_idx, best_score))
}

/// Finds all strings matching above a given threshold.
///
/// # Arguments
///
/// * `query` - The string to match
/// * `candidates` - List of candidate strings
/// * `threshold` - Minimum similarity threshold (0.0 to 1.0)
///
/// # Returns
///
/// A vector of (index, similarity_score) tuples for matches above threshold.
///
/// # Examples
///
/// ```
/// use text_distance_utils::find_matches;
///
/// let candidates = vec!["hello", "hallo", "world", "help"];
/// let matches = find_matches("hell", &candidates, 0.5);
/// assert!(!matches.is_empty());
/// ```
pub fn find_matches(query: &str, candidates: &[&str], threshold: f64) -> Vec<(usize, f64)> {
    candidates
        .iter()
        .enumerate()
        .map(|(i, candidate)| (i, levenshtein_similarity(query, candidate)))
        .filter(|(_, score)| *score >= threshold)
        .collect()
}

// ============================================================================
// UTILITY FUNCTIONS
// ============================================================================

/// Returns a summary of all distance/similarity metrics between two strings.
///
/// # Arguments
///
/// * `s1` - First string
/// * `s2` - Second string
///
/// # Returns
///
/// A HashMap containing all computed metrics.
///
/// # Examples
///
/// ```
/// use text_distance_utils::compare_strings;
///
/// let metrics = compare_strings("kitten", "sitting");
/// println!("Levenshtein distance: {}", metrics.get("levenshtein_distance").unwrap());
/// println!("Jaro-Winkler similarity: {}", metrics.get("jaro_winkler_similarity").unwrap());
/// ```
pub fn compare_strings(s1: &str, s2: &str) -> HashMap<&'static str, f64> {
    let mut result = HashMap::new();

    // Distances
    if let Ok(dist) = hamming_distance(s1, s2) {
        result.insert("hamming_distance", dist as f64);
    }
    result.insert("levenshtein_distance", levenshtein_distance(s1, s2) as f64);
    result.insert(
        "damerau_levenshtein_distance",
        damerau_levenshtein_distance(s1, s2) as f64,
    );
    result.insert("osa_distance", osa_distance(s1, s2) as f64);

    // Similarities
    result.insert("levenshtein_similarity", levenshtein_similarity(s1, s2));
    result.insert(
        "damerau_levenshtein_similarity",
        damerau_levenshtein_similarity(s1, s2),
    );
    result.insert("jaro_similarity", jaro_similarity(s1, s2));
    result.insert("jaro_winkler_similarity", jaro_winkler_similarity(s1, s2));
    result.insert("dice_coefficient", dice_coefficient(s1, s2));
    result.insert("cosine_similarity", cosine_similarity(s1, s2));
    result.insert("overlap_coefficient", overlap_coefficient(s1, s2));

    // N-gram similarities
    result.insert("bigram_similarity", ngram_similarity(s1, s2, 2));
    result.insert("trigram_similarity", ngram_similarity(s1, s2, 3));

    // Q-gram distances
    result.insert("qgram_distance_2", qgram_distance(s1, s2, 2) as f64);
    result.insert("qgram_distance_3", qgram_distance(s1, s2, 3) as f64);

    result
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_hamming_distance() {
        assert_eq!(hamming_distance("karolin", "kathrin"), Ok(3));
        assert_eq!(hamming_distance("0000", "1111"), Ok(4));
        assert_eq!(hamming_distance("hello", "hello"), Ok(0));
        assert!(hamming_distance("hello", "hi").is_err());
    }

    #[test]
    fn test_levenshtein_distance() {
        assert_eq!(levenshtein_distance("kitten", "sitting"), 3);
        assert_eq!(levenshtein_distance("book", "back"), 2);
        assert_eq!(levenshtein_distance("", "hello"), 5);
        assert_eq!(levenshtein_distance("hello", ""), 5);
        assert_eq!(levenshtein_distance("", ""), 0);
        assert_eq!(levenshtein_distance("hello", "hello"), 0);
    }

    #[test]
    fn test_damerau_levenshtein_distance() {
        // Transposition counts as 1
        assert_eq!(damerau_levenshtein_distance("ca", "ac"), 1);
        assert_eq!(damerau_levenshtein_distance("abcd", "acbd"), 1);
    }

    #[test]
    fn test_jaro_similarity() {
        assert!((jaro_similarity("MARTHA", "MARHTA") - 0.944).abs() < 0.01);
        assert_eq!(jaro_similarity("hello", "hello"), 1.0);
        assert_eq!(jaro_similarity("", ""), 1.0);
        assert_eq!(jaro_similarity("hello", ""), 0.0);
    }

    #[test]
    fn test_jaro_winkler_similarity() {
        // Jaro-Winkler should give higher scores for matching prefixes
        assert!(jaro_winkler_similarity("MARTHA", "MARHTA") > jaro_similarity("MARTHA", "MARHTA"));
        assert_eq!(jaro_winkler_similarity("hello", "hello"), 1.0);
    }

    #[test]
    fn test_dice_coefficient() {
        assert!(dice_coefficient("night", "nacht") > 0.0);
        assert!(dice_coefficient("night", "nacht") < 0.5);
        assert_eq!(dice_coefficient("hello", "hello"), 1.0);
    }

    #[test]
    fn test_cosine_similarity() {
        assert!((cosine_similarity("hello world", "hello world") - 1.0).abs() < 0.001);
        assert_eq!(cosine_similarity("hello world", "foo bar"), 0.0);
        // Same words in different order should still be 1.0
        assert!((cosine_similarity("hello world", "world hello") - 1.0).abs() < 0.001);
    }

    #[test]
    fn test_best_match() {
        let candidates = vec!["hello", "hallo", "hola", "hi"];
        let result = best_match("hell", &candidates);
        assert!(result.is_some());
        let (idx, score) = result.unwrap();
        assert_eq!(idx, 0);
        assert!(score > 0.7);
    }

    #[test]
    fn test_find_matches() {
        let candidates = vec!["hello", "hallo", "world", "help"];
        let matches = find_matches("hell", &candidates, 0.5);
        assert!(!matches.is_empty());
        assert!(matches.iter().any(|(i, _)| *i == 0)); // "hello" should match
    }

    #[test]
    fn test_ngram_similarity() {
        assert!(ngram_similarity("hello", "hella", 2) > 0.5);
        assert_eq!(ngram_similarity("", "", 2), 1.0);
    }

    #[test]
    fn test_overlap_coefficient() {
        assert_eq!(overlap_coefficient("hello world", "hello"), 1.0);
        assert!(overlap_coefficient("hello world", "hello there") > 0.0);
    }
}