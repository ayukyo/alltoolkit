//! Fuzzy String Matching Utilities
//!
//! A zero-dependency fuzzy string matching library for Rust with multiple algorithms,
//! autocomplete scoring, and phonetic encoding support.
//!
//! # Features
//! - **Levenshtein distance** — edit distance with insertions, deletions, substitutions
//! - **Damerau-Levenshtein distance** — adds transposition support
//! - **Jaro-Winkler similarity** — prefix-heavy similarity metric
//! - **Token matching** — match strings across word boundaries
//! - **Phonetic encoding** — Soundex & Metaphone for pronunciation-based matching
//! - **Autocomplete scorer** — rank candidates by relevance to a query
//! - **Fuzzy filter** — filter & rank items by fuzzy score

use std::cmp::{max, min};
use std::collections::HashMap;

/// Result of a fuzzy match operation
#[derive(Debug, Clone)]
pub struct FuzzyScore {
    /// The candidate string that was scored
    pub candidate: String,
    /// Numerical score (higher = better match)
    pub score: f64,
    /// Match quality category
    pub quality: MatchQuality,
    /// Which character positions matched
    pub matched_indices: Vec<usize>,
}

impl FuzzyScore {
    pub fn new(candidate: String, score: f64, matched_indices: Vec<usize>) -> Self {
        let quality = match score {
            s if s >= 0.95 => MatchQuality::Exact,
            s if s >= 0.80 => MatchQuality::Excellent,
            s if s >= 0.60 => MatchQuality::Good,
            s if s >= 0.40 => MatchQuality::Partial,
            s if s >= 0.20 => MatchQuality::Weak,
            _ => MatchQuality::Poor,
        };
        Self {
            candidate,
            score,
            quality,
            matched_indices,
        }
    }
}

/// Match quality category
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum MatchQuality {
    /// Perfect match
    Exact,
    /// Very close match
    Excellent,
    /// Good match
    Good,
    /// Partial match
    Partial,
    /// Weak match
    Weak,
    /// Poor match
    Poor,
}

/// Compute Levenshtein (edit) distance between two strings.
/// Returns the minimum number of single-character edits (insert, delete, substitute).
pub fn levenshtein(s: &str, t: &str) -> usize {
    let s_chars: Vec<char> = s.chars().collect();
    let t_chars: Vec<char> = t.chars().collect();
    let m = s_chars.len();
    let n = t_chars.len();

    if m == 0 {
        return n;
    }
    if n == 0 {
        return m;
    }

    // Use two rows instead of full matrix for O(min(m,n)) space
    let mut prev: Vec<usize> = (0..=n).collect();
    let mut curr = vec![0usize; n + 1];

    for i in 1..=m {
        curr[0] = i;
        for j in 1..=n {
            let cost = if s_chars[i - 1] == t_chars[j - 1] { 0 } else { 1 };
            curr[j] = min(
                min(curr[j - 1], prev[j]) + 1, // deletion or insertion
                prev[j - 1] + cost,             // substitution
            );
        }
        std::mem::swap(&mut prev, &mut curr);
    }

    prev[n]
}

/// Normalized Levenshtein similarity (0.0 to 1.0)
pub fn levenshtein_similarity(s: &str, t: &str) -> f64 {
    let max_len = max(s.len(), t.len());
    if max_len == 0 {
        return 1.0;
    }
    let dist = levenshtein(s, t);
    1.0 - (dist as f64) / (max_len as f64)
}

/// Compute Damerau-Levenshtein distance — allows transposition as a single edit.
pub fn damerau_levenshtein(s: &str, t: &str) -> usize {
    let s_chars: Vec<char> = s.chars().collect();
    let t_chars: Vec<char> = t.chars().collect();
    let m = s_chars.len();
    let n = t_chars.len();

    if m == 0 {
        return n;
    }
    if n == 0 {
        return m;
    }

    let mut matrix = vec![vec![0usize; n + 1]; m + 1];

    for i in 0..=m {
        matrix[i][0] = i;
    }
    for j in 0..=n {
        matrix[0][j] = j;
    }

    for i in 1..=m {
        for j in 1..=n {
            let cost = if s_chars[i - 1] == t_chars[j - 1] { 0 } else { 1 };
            matrix[i][j] = min(
                min(matrix[i - 1][j], matrix[i][j - 1]) + 1,
                matrix[i - 1][j - 1] + cost,
            );

            // Transposition: swap adjacent chars in s with adjacent chars in t
            if i > 1 && j > 1
                && s_chars[i - 1] == t_chars[j - 2]
                && s_chars[i - 2] == t_chars[j - 1]
            {
                matrix[i][j] = min(matrix[i][j], matrix[i - 2][j - 2] + cost);
            }
        }
    }

    matrix[m][n]
}

/// Normalized Damerau-Levenshtein similarity (0.0 to 1.0)
pub fn damerau_similarity(s: &str, t: &str) -> f64 {
    let max_len = max(s.len(), t.len());
    if max_len == 0 {
        return 1.0;
    }
    let dist = damerau_levenshtein(s, t);
    1.0 - (dist as f64) / (max_len as f64)
}

/// Compute Jaro-Winkler similarity (0.0 to 1.0).
/// Gives higher scores to strings that match from the beginning.
pub fn jaro_winkler(s: &str, t: &str) -> f64 {
    let s_chars: Vec<char> = s.chars().collect();
    let t_chars: Vec<char> = t.chars().collect();
    let m = s_chars.len() as f64;
    let n = t_chars.len() as f64;

    if m == 0.0 && n == 0.0 {
        return 1.0;
    }
    if m == 0.0 || n == 0.0 {
        return 0.0;
    }

    let match_distance = ((if m > n { m } else { n }).floor() as usize / 2).max(1) - 1;
    let mut s_matches = vec![false; s_chars.len()];
    let mut t_matches = vec![false; t_chars.len()];
    let mut matches = 0usize;
    let mut transpositions = 0usize;

    // Find matches
    for i in 0..s_chars.len() {
        let start = if i >= match_distance { i - match_distance } else { 0 };
        let end = min(i + match_distance + 1, t_chars.len());

        for j in start..end {
            if t_matches[j] || s_chars[i] != t_chars[j] {
                continue;
            }
            s_matches[i] = true;
            t_matches[j] = true;
            matches += 1;
            break;
        }
    }

    if matches == 0 {
        return 0.0;
    }

    // Count transpositions
    let mut k = 0;
    for i in 0..s_chars.len() {
        if !s_matches[i] {
            continue;
        }
        while !t_matches[k] {
            k += 1;
        }
        if s_chars[i] != t_chars[k] {
            transpositions += 1;
        }
        k += 1;
    }

    let jaro = (matches as f64 / m
        + matches as f64 / n
        + (matches as f64 - transpositions as f64 / 2.0) / matches as f64)
        / 3.0;

    // Winkler modification — bonus for common prefix (up to 4 chars)
    let prefix_len = {
        let mut pl = 0;
        let min_len = min(s_chars.len(), t_chars.len());
        for i in 0..min_len {
            if s_chars[i] == t_chars[i] {
                pl += 1;
            } else {
                break;
            }
            if pl >= 4 {
                break;
            }
        }
        pl
    };

    jaro + (prefix_len as f64 * 0.1 * (1.0 - jaro))
}

/// Score how well `query` matches `candidate` for autocomplete.
/// Considers: consecutive matching, case-insensitive matching, word-boundary matching.
pub fn autocomplete_score(query: &str, candidate: &str) -> (f64, Vec<usize>) {
    let query_lower: Vec<char> = query.to_lowercase().chars().collect();
    let candidate_lower: Vec<char> = candidate.to_lowercase().chars().collect();
    let q_len = query_lower.len();
    let c_len = candidate_lower.len();

    if q_len == 0 {
        return (1.0, vec![]);
    }
    if c_len == 0 {
        return (0.0, vec![]);
    }

    let mut score = 0.0;
    let mut qi = 0;
    let mut consecutive = 0;
    let mut matched_indices = Vec::new();
    let mut prev_matched = false;

    for (i, c_char) in candidate_lower.iter().enumerate() {
        if qi >= q_len {
            break;
        }

        if *c_char == query_lower[qi] {
            matched_indices.push(i);

            // Bonus for consecutive matches
            if prev_matched {
                consecutive += 1;
                score += 1.0 + (consecutive as f64 * 0.5);
            } else {
                consecutive = 1;
                score += 1.0;
            }

            // Bonus for matching at word boundary (start of candidate or after separator)
            if i == 0 {
                score += 2.0;
            } else {
                let prev_char = candidate_lower[i - 1];
                if prev_char == ' ' || prev_char == '_' || prev_char == '-' || prev_char == '.' {
                    score += 2.0;
                } else if prev_char.is_uppercase() {
                    score += 1.5;
                }
            }

            // Bonus for case-exact match
            if let Some(c_orig) = candidate.chars().nth(i) {
                if c_orig.is_uppercase() && c_orig == query.chars().nth(qi).unwrap_or(' ') {
                    score += 0.5;
                }
            }

            prev_matched = true;
            qi += 1;
        } else {
            prev_matched = false;
            consecutive = 0;
        }
    }

    // Penalty for unmatched query characters
    if qi < q_len {
        score *= 0.1 * (qi as f64) / (q_len as f64);
    }

    // Normalize by candidate length (prefer shorter strings when scores are close)
    let len_bonus = 1.0 - ((c_len.saturating_sub(q_len)) as f64 * 0.01).clamp(0.0, 0.5);
    score *= len_bonus;

    // Bonus for exact prefix match
    if candidate_lower.starts_with(&query_lower) {
        score += 10.0;
    }

    (score, matched_indices)
}

/// Fuzzy filter: rank a list of candidates by how well they match the query.
/// Returns sorted results (best match first).
pub fn fuzzy_filter<T: AsRef<str>>(query: &str, candidates: &[T], threshold: f64) -> Vec<FuzzyScore> {
    let mut results: Vec<FuzzyScore> = candidates
        .iter()
        .filter_map(|c| {
            let c_str = c.as_ref();
            let (score, indices) = autocomplete_score(query, c_str);
            if score >= threshold {
                Some(FuzzyScore::new(c_str.to_string(), score, indices))
            } else {
                None
            }
        })
        .collect();

    results.sort_by(|a, b| b.score.partial_cmp(&a.score).unwrap_or(std::cmp::Ordering::Equal));
    results
}

// ─────────────────────────────────────────────────────────────────
// Phonetic Encoding
// ─────────────────────────────────────────────────────────────────

/// Soundex code generator — groups phonetically similar names together.
pub fn soundex(s: &str) -> String {
    let chars: Vec<char> = s.to_uppercase().chars().collect();
    if chars.is_empty() {
        return String::new();
    }

    let codes: HashMap<char, char> = [
        ('B', '1'), ('F', '1'), ('P', '1'), ('V', '1'),
        ('C', '2'), ('G', '2'), ('J', '2'), ('K', '2'), ('Q', '2'), ('S', '2'), ('X', '2'),
        ('D', '3'), ('T', '3'),
        ('L', '4'),
        ('M', '5'), ('N', '5'),
        ('R', '6'),
    ]
    .into_iter()
    .collect();

    let first_char = chars[0];
    let mut result = String::from(first_char.to_string());
    let mut prev_code = *codes.get(&first_char).unwrap_or(&'0');

    for ch in chars.iter().skip(1) {
        if result.len() >= 4 {
            break;
        }
        if let Some(&code) = codes.get(ch) {
            if code != prev_code && code != '0' {
                result.push(code);
            }
        }
        prev_code = *codes.get(ch).unwrap_or(&'0');
    }

    while result.len() < 4 {
        result.push('0');
    }

    result
}

/// Metaphone code generator — more accurate than Soundex for English words.
pub fn metaphone(s: &str) -> String {
    let chars: Vec<char> = s.to_uppercase().chars().collect();
    if chars.is_empty() {
        return String::new();
    }

    let mut result = String::new();
    let mut i = 0;
    let len = chars.len();

    let is_vowel = |c: char| -> bool {
        matches!(c, 'A' | 'E' | 'I' | 'O' | 'U' | 'Y')
    };

    // Skip leading silent letters
    if len >= 2 {
        let pair = format!("{}{}", chars[0], chars[1]);
        if pair == "KN" || pair == "GN" || pair == "PN" || pair == "AE" || pair == "WR" {
            i = 1;
        }
    }

    while i < len && result.len() < 6 {
        let c = chars[i];

        if is_vowel(c) {
            if i == 0 {
                result.push(c);
            }
            i += 1;
            continue;
        }

        match c {
            'B' => {
                if !(i == len - 1 && i > 0 && chars[i - 1] == 'M') {
                    result.push('F');
                }
            }
            'C' => {
                if i + 1 < len {
                    let next = chars[i + 1];
                    if next == 'H' {
                        result.push('X');
                        i += 2;
                        continue;
                    } else if matches!(next, 'E' | 'I' | 'Y') {
                        result.push('S');
                        i += 2;
                        continue;
                    }
                }
                result.push('K');
            }
            'D' => {
                if i + 2 < len {
                    let next2 = chars[i + 2];
                    if matches!(chars[i + 1], 'G' | 'J') && matches!(next2, 'E' | 'I' | 'Y') {
                        result.push('J');
                        i += 3;
                        continue;
                    }
                }
                result.push('T');
            }
            'F' => result.push('F'),
            'G' => {
                if i + 1 < len && chars[i + 1] == 'H' {
                    if i + 2 < len && !is_vowel(chars[i + 2]) {
                        i += 2;
                        continue;
                    }
                    result.push('F');
                    i += 2;
                    continue;
                } else if i + 1 < len && chars[i + 1] == 'N' {
                    i += 1;
                    continue;
                } else {
                    result.push('K');
                }
            }
            'H' => {
                if i + 1 < len && !is_vowel(chars[i + 1]) {
                    i += 1;
                    continue;
                }
                if i == 0 {
                    result.push('H');
                }
            }
            'J' => result.push('J'),
            'K' => {
                if i > 0 && chars[i - 1] == 'C' {
                    i += 1;
                    continue;
                }
                result.push('K');
            }
            'L' => result.push('L'),
            'M' => {
                if i + 1 < len && chars[i + 1] == 'B' && i + 2 == len {
                    i += 1;
                    continue;
                }
                result.push('M');
            }
            'N' => result.push('N'),
            'P' => {
                if i + 1 < len && chars[i + 1] == 'H' {
                    result.push('F');
                    i += 2;
                    continue;
                }
                result.push('P');
            }
            'Q' => result.push('K'),
            'R' => result.push('R'),
            'S' => {
                if i + 2 < len && chars[i + 1] == 'C' && is_vowel(chars[i + 2]) {
                    result.push('S');
                    i += 3;
                    continue;
                }
                result.push('S');
            }
            'T' => {
                if i + 2 < len && chars[i + 1] == 'C' && is_vowel(chars[i + 2]) {
                    result.push('S');
                    i += 3;
                    continue;
                }
                if i + 2 < len && chars[i + 1] == 'H' {
                    result.push('0'); // "th" sound
                    i += 2;
                    continue;
                }
                result.push('T');
            }
            'V' => result.push('F'),
            'W' => {
                if i + 1 < len && is_vowel(chars[i + 1]) {
                    result.push('W');
                }
            }
            'X' => result.push('K'),
            'Y' => {
                if i + 1 < len && is_vowel(chars[i + 1]) {
                    result.push('Y');
                }
            }
            'Z' => result.push('S'),
            _ => {}
        }
        i += 1;
    }

    result
}

/// Check if two strings sound similar using Metaphone
pub fn sounds_like(s: &str, t: &str) -> bool {
    metaphone(s) == metaphone(t)
}

/// Match using Soundex — returns true if the two strings have the same Soundex code
pub fn soundex_match(s: &str, t: &str) -> bool {
    soundex(s) == soundex(t)
}

/// Autocomplete result with multiple algorithm scores
#[derive(Debug, Clone)]
pub struct MultiScore {
    pub candidate: String,
    pub autocomplete_score: f64,
    pub jaro_winkler: f64,
    pub levenshtein_sim: f64,
    pub soundex_match: bool,
    pub metaphone_match: bool,
    pub combined_score: f64,
}

impl MultiScore {
    /// Compute a weighted combined score
    pub fn combined(&self) -> f64 {
        self.autocomplete_score * 0.4
            + self.jaro_winkler * 0.3
            + self.levenshtein_sim * 0.2
            + if self.soundex_match || self.metaphone_match { 0.1 } else { 0.0 }
    }
}

/// Score a candidate with all algorithms at once
pub fn multi_score(query: &str, candidate: &str) -> MultiScore {
    let (autocomplete, matched) = autocomplete_score(query, candidate);
    let jw = jaro_winkler(query, candidate);
    let lev = levenshtein_similarity(query, candidate);
    let sndx = soundex_match(query, candidate);
    let metaph = sounds_like(query, candidate);

    let mut ms = MultiScore {
        candidate: candidate.to_string(),
        autocomplete_score: autocomplete,
        jaro_winkler: jw,
        levenshtein_sim: lev,
        soundex_match: sndx,
        metaphone_match: metaph,
        combined_score: 0.0,
    };
    ms.combined_score = ms.combined();
    let _ = matched; // unused in this struct but returned from autocomplete_score
    ms
}

/// Best match result combining all signals
#[derive(Debug, Clone)]
pub struct MatchResult {
    pub candidate: String,
    pub score: f64,
    pub quality: MatchQuality,
    pub matched_indices: Vec<usize>,
    pub jaro_winkler: f64,
    pub phonetic_codes: (String, String),
}

impl MatchResult {
    /// Find the best match for query among candidates, returning all scoring details
    pub fn best_match<'a, T: AsRef<str>>(query: &str, candidates: &'a [T]) -> Option<MatchResult> {
        if candidates.is_empty() {
            return None;
        }

        let query_lower = query.to_lowercase();
        let q_soundex = soundex(&query_lower);
        let q_metaphone = metaphone(&query_lower);

        let mut best: Option<MatchResult> = None;

        for c in candidates {
            let c_str = c.as_ref();
            let c_lower = c_str.to_lowercase();
            let (auto_score, matched_indices) = autocomplete_score(query, c_str);
            let jw = jaro_winkler(&query_lower, &c_lower);
            let lev = levenshtein_similarity(&query_lower, &c_lower);
            let c_soundex = soundex(&c_lower);
            let c_metaphone = metaphone(&c_lower);

            let phonetic_match =
                (!q_soundex.is_empty() && q_soundex == c_soundex)
                || (!q_metaphone.is_empty() && q_metaphone == c_metaphone);

            let score = auto_score * 0.35 + jw * 0.25 + lev * 0.25 + if phonetic_match { 0.15 } else { 0.0 };
            let quality = match score {
                s if s >= 0.95 => MatchQuality::Exact,
                s if s >= 0.80 => MatchQuality::Excellent,
                s if s >= 0.60 => MatchQuality::Good,
                s if s >= 0.40 => MatchQuality::Partial,
                s if s >= 0.20 => MatchQuality::Weak,
                _ => MatchQuality::Poor,
            };

            let result = MatchResult {
                candidate: c_str.to_string(),
                score,
                quality,
                matched_indices,
                jaro_winkler: jw,
                phonetic_codes: (q_soundex.clone(), c_soundex),
            };

            match &best {
                None => best = Some(result),
                Some(b) if result.score > b.score => best = Some(result),
                _ => {}
            }
        }

        best
    }
}

// ─────────────────────────────────────────────────────────────────
// Tests
// ─────────────────────────────────────────────────────────────────

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_levenshtein_basic() {
        assert_eq!(levenshtein("kitten", "kitten"), 0);
        assert_eq!(levenshtein("kitten", "sitting"), 3);
        assert_eq!(levenshtein("", "abc"), 3);
        assert_eq!(levenshtein("abc", ""), 3);
    }

    #[test]
    fn test_levenshtein_similarity() {
        assert!((levenshtein_similarity("hello", "hello") - 1.0).abs() < 1e-9);
        assert!(levenshtein_similarity("hello", "hallo") > 0.7);
    }

    #[test]
    fn test_jaro_winkler() {
        let sim = jaro_winkler("MARTHA", "MARHTA");
        assert!(sim > 0.95);
        assert!((jaro_winkler("AAA", "AAA") - 1.0).abs() < 1e-9);
        assert!((jaro_winkler("", "") - 1.0).abs() < 1e-9);
        assert!((jaro_winkler("AAA", "AAA") - 1.0).abs() < 1e-9);
        assert!((jaro_winkler("", "B") - 0.0).abs() < 1e-9);
    }

    #[test]
    fn test_autocomplete_score() {
        let (score, _) = autocomplete_score("ve", "vector");
        assert!(score > 0.0);

        let (exact_score, _) = autocomplete_score("test", "test");
        assert!(exact_score > 10.0); // exact prefix bonus
    }

    #[test]
    fn test_autocomplete_score_word_boundary() {
        let (score1, _) = autocomplete_score("ab", "auto_box");
        let (score2, _) = autocomplete_score("ab", "autooldbox");

        // Word boundary match should score higher
        assert!(score1 > score2);
    }

    #[test]
    fn test_fuzzy_filter() {
        let items = vec!["apple", "apricot", "banana", "pineapple", "applepie"];
        let results = fuzzy_filter("apple", &items, 0.5);

        assert!(!results.is_empty());
        assert!(results[0].candidate == "applepie"
            || results[0].candidate == "apple"
            || results[0].candidate == "pineapple");
        // "apple" and "applepie" should be at the top
    }

    #[test]
    fn test_soundex() {
        assert_eq!(soundex("Robert"), "R163");
        assert_eq!(soundex("Rubert"), "R163");
        // Classic Soundex examples
        assert_eq!(soundex("Ashcraft"), "A226");
        assert_eq!(soundex("Tymczak"), "T522");
        assert_eq!(soundex("Pfister"), "P236");
        assert_eq!(soundex("Honewell"), "H540");
    }

    #[test]
    fn test_soundex_empty() {
        assert_eq!(soundex(""), "");
        assert_eq!(soundex("a"), "A000");
    }

    #[test]
    fn test_metaphone() {
        assert_eq!(metaphone("Catherine"), metaphone("Kathryn"));
        assert_eq!(metaphone("Mike"), "MK");
    }

    #[test]
    fn test_sounds_like() {
        assert!(sounds_like("Catherine", "Kathryn"));
        assert!(sounds_like("John", "Jon"));
    }

    #[test]
    fn test_damerau_levenshtein() {
        // Standard Levenshtein cases
        assert_eq!(damerau_levenshtein("kitten", "kitten"), 0);
        assert_eq!(damerau_levenshtein("kitten", "sitting"), 3);
        assert_eq!(damerau_levenshtein("CA", "ABC"), 3);
        assert_eq!(damerau_levenshtein("hello", "helo"), 1);
        // Adjacent transposition: AB <-> BA costs 1 (Damerau recognizes the swap)
        assert_eq!(damerau_levenshtein("AB", "BA"), 1);
    }

    #[test]
    fn test_multi_score() {
        let ms = multi_score("hello", "Hello");
        assert!(ms.combined_score > 0.0);
        assert!(ms.soundex_match || ms.metaphone_match || ms.jaro_winkler > 0.8);
    }

    #[test]
    fn test_best_match() {
        let items = vec!["Rust", "Go", "Swift", "Kotlin", "TypeScript"];
        let result = MatchResult::best_match("Rust", &items).unwrap();
        assert_eq!(result.candidate, "Rust");
        assert!(result.score > 0.9);
    }

    #[test]
    fn test_best_match_no_candidates() {
        let items: Vec<&str> = vec![];
        assert!(MatchResult::best_match("test", &items).is_none());
    }

    #[test]
    fn test_match_quality() {
        let ms = multi_score("hello", "hallo");
        // Combined score with multiple algorithms should be decent for "hallo" vs "hello"
        assert!(ms.combined_score > 0.2);
    }

    #[test]
    fn test_fuzzy_filter_threshold() {
        let items = vec!["apple", "banana"];
        let results = fuzzy_filter("xyz", &items, 0.5);
        assert!(results.is_empty());
    }

    #[test]
    fn test_autocomplete_matched_indices() {
        let (_, indices) = autocomplete_score("abc", "abcde");
        assert_eq!(indices, vec![0, 1, 2]);
    }

    #[test]
    fn test_autocomplete_consecutive_bonus() {
        let (_, indices1) = autocomplete_score("abc", "abcdef");
        let (_, indices2) = autocomplete_score("ac", "abcdef");

        // abc is consecutive → higher score
        let score1 = autocomplete_score("abc", "abcdef").0;
        let score2 = autocomplete_score("ac", "abcdef").0;
        assert!(score1 > score2);
        let _ = (indices1, indices2);
    }

    #[test]
    fn test_fuzzy_filter_sorted() {
        let items = vec!["Rust", "Ruby", "Rustacean"];
        let results = fuzzy_filter("Rust", &items, 0.0);
        assert!(results.len() == 3);
        assert!(results[0].score >= results[1].score);
        assert!(results[1].score >= results[2].score);
    }
}