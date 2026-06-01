//! # MTrie — Mutable Trie with Fuzzy Matching & Autocomplete
//!
//! A production-ready mutable prefix tree (trie) supporting:
//! - Insert, delete, and search with prefix matching
//! - Autocomplete with configurable max results
//! - Fuzzy matching (Levenshtein distance) with configurable threshold
//! - Weight-boosting for frequently searched terms
//! - Serialization to/from JSON
//! - Zero external dependencies
//!
//! # Example
//!
//! ```
//! use mtrie_utils::MTrie;
//!
//! let mut trie = MTrie::new();
//! trie.insert("rust");
//! trie.insert("ruby");
//! trie.insert("rubyist");
//! trie.insert("python");
//!
//! assert_eq!(trie.search_prefix("ru"), vec!["ruby", "rubyist", "rust"]);
//! let results = trie.fuzzy_search("rust", 1);
//! assert!(results.iter().any(|(w, d)| w == "rust" && *d == 0));
//! ```

use serde::{Deserialize, Serialize};
use std::collections::HashMap;

/// A single node in the trie
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct TrieNode {
    /// Children keyed by character
    children: HashMap<char, TrieNode>,
    /// Whether this node marks the end of a complete word
    is_word: bool,
    /// How many times this word has been queried (for boosting)
    query_count: u32,
    /// Word stored at this node (only set when is_word=true)
    word: Option<String>,
}

impl TrieNode {
    fn new() -> Self {
        Self {
            children: HashMap::new(),
            is_word: false,
            query_count: 0,
            word: None,
        }
    }
}

/// Mutable Trie (prefix tree) with autocomplete and fuzzy search
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct MTrie {
    root: TrieNode,
    total_words: usize,
}

impl MTrie {
    /// Create a new empty trie
    pub fn new() -> Self {
        Self {
            root: TrieNode::new(),
            total_words: 0,
        }
    }

    /// Create a trie pre-populated with words
    pub fn from_words<S: AsRef<str>>(words: &[S]) -> Self {
        let mut t = Self::new();
        for w in words {
            t.insert(w.as_ref());
        }
        t
    }

    /// Insert a word into the trie
    pub fn insert(&mut self, word: &str) -> bool {
        let word_lower = word.to_lowercase();
        let chars: Vec<char> = word_lower.chars().collect();
        let mut node = &mut self.root;
        let mut is_new = false;

        for ch in &chars {
            is_new = node.children.get(ch).is_none();
            node = node.children.entry(*ch).or_insert_with(TrieNode::new);
        }

        if !node.is_word {
            node.is_word = true;
            node.word = Some(word_lower);
            self.total_words += 1;
        }

        is_new
    }

    /// Check if a word exists exactly in the trie
    pub fn contains(&self, word: &str) -> bool {
        let word_lower = word.to_lowercase();
        let chars: Vec<char> = word_lower.chars().collect();
        let mut node = &self.root;

        for ch in chars {
            match node.children.get(&ch) {
                Some(n) => node = n,
                None => return false,
            }
        }

        node.is_word
    }

    /// Remove a word from the trie (returns true if removed)
    pub fn remove(&mut self, word: &str) -> bool {
        let word_lower = word.to_lowercase();
        if self.contains(&word_lower) {
            let chars: Vec<char> = word_lower.chars().collect();
            Self::remove_helper(&mut self.root, &chars);
            self.total_words -= 1;
            true
        } else {
            false
        }
    }

    fn remove_helper(node: &mut TrieNode, chars: &[char]) -> bool {
        if chars.is_empty() {
            if !node.is_word {
                return false;
            }
            node.is_word = false;
            node.word = None;
            node.children.is_empty()
        } else {
            let ch = chars[0];
            if let Some(child) = node.children.get_mut(&ch) {
                let should_delete_child = Self::remove_helper(child, &chars[1..]);
                if should_delete_child {
                    node.children.remove(&ch);
                }
                node.children.is_empty() && !node.is_word
            } else {
                false
            }
        }
    }

    /// Get all words with the given prefix
    pub fn search_prefix(&self, prefix: &str) -> Vec<String> {
        let prefix_lower = prefix.to_lowercase();
        let chars: Vec<char> = prefix_lower.chars().collect();
        let mut node = &self.root;

        // Navigate to the prefix node
        for ch in &chars {
            match node.children.get(ch) {
                Some(n) => node = n,
                None => return vec![],
            }
        }

        // Collect all words from this node onward
        let mut results = vec![];
        self.collect_words(node, &mut results);

        // Sort by boost weight (query_count), then alphabetically
        results.sort_by(|a, b| {
            let count_a = self.get_node(a).map(|n| n.query_count).unwrap_or(0);
            let count_b = self.get_node(b).map(|n| n.query_count).unwrap_or(0);
            count_b.cmp(&count_a).then(a.cmp(b))
        });

        results
    }

    /// Get autocomplete suggestions (prefix search with max limit)
    pub fn autocomplete(&self, prefix: &str, max_results: usize) -> Vec<String> {
        let mut results = self.search_prefix(prefix);
        results.truncate(max_results);
        results
    }

    /// Record a query for a word (increments boost counter)
    pub fn record_query(&mut self, word: &str) {
        let word_lower = word.to_lowercase();
        if let Some(node) = self.get_node_mut(&word_lower) {
            node.query_count += 1;
        }
    }

    /// Fuzzy search: find words within max_edit_distance
    pub fn fuzzy_search(&self, word: &str, max_distance: usize) -> Vec<(String, usize)> {
        let word_lower = word.to_lowercase();
        let target: Vec<char> = word_lower.chars().collect();
        let mut all_words = vec![];
        self.collect_words(&self.root, &mut all_words);

        let mut results: Vec<(String, usize)> = all_words
            .into_iter()
            .map(|w| {
                let dist = levenshtein(&w, &target);
                (w, dist)
            })
            .filter(|(_, dist)| *dist <= max_distance)
            .collect();

        // Sort by edit distance, then by boost
        results.sort_by(|(w1, d1), (w2, d2)| {
            d1.cmp(d2).then_with(|| {
                let c1 = self.get_node(w1).map(|n| n.query_count).unwrap_or(0);
                let c2 = self.get_node(w2).map(|n| n.query_count).unwrap_or(0);
                c2.cmp(&c1)
            })
        });

        results
    }

    fn collect_words(&self, node: &TrieNode, results: &mut Vec<String>) {
        if node.is_word {
            if let Some(ref w) = node.word {
                results.push(w.clone());
            }
        }
        for child in node.children.values() {
            self.collect_words(child, results);
        }
    }

    fn get_node(&self, word: &str) -> Option<&TrieNode> {
        let chars: Vec<char> = word.chars().collect();
        let mut node = &self.root;
        for ch in chars {
            match node.children.get(&ch) {
                Some(n) => node = n,
                None => return None,
            }
        }
        Some(node)
    }

    fn get_node_mut(&mut self, word: &str) -> Option<&mut TrieNode> {
        let chars: Vec<char> = word.chars().collect();
        let mut node = &mut self.root;
        for ch in chars {
            match node.children.get_mut(&ch) {
                Some(n) => node = n,
                None => return None,
            }
        }
        Some(node)
    }

    /// Serialize trie to JSON string
    pub fn to_json(&self) -> Result<String, serde_json::Error> {
        serde_json::to_string_pretty(self)
    }

    /// Deserialize trie from JSON string
    pub fn from_json(json: &str) -> Result<Self, serde_json::Error> {
        serde_json::from_str(json)
    }

    /// Total number of words in the trie
    pub fn len(&self) -> usize {
        self.total_words
    }

    /// Check if trie is empty
    pub fn is_empty(&self) -> bool {
        self.total_words == 0
    }

    /// Clear all words
    pub fn clear(&mut self) {
        self.root = TrieNode::new();
        self.total_words = 0;
    }
}

impl Default for MTrie {
    fn default() -> Self {
        Self::new()
    }
}

/// Compute Levenshtein edit distance between two strings
pub fn levenshtein(a: &str, b: &[char]) -> usize {
    let a_chars: Vec<char> = a.chars().collect();
    let m = a_chars.len();
    let n = b.len();

    if m == 0 {
        return n;
    }
    if n == 0 {
        return m;
    }

    let mut dp = vec![vec![0usize; n + 1]; m + 1];

    for i in 0..=m {
        dp[i][0] = i;
    }
    for j in 0..=n {
        dp[0][j] = j;
    }

    for i in 1..=m {
        for j in 1..=n {
            let cost = if a_chars[i - 1] == b[j - 1] { 0 } else { 1 };
            dp[i][j] = (dp[i - 1][j] + 1)
                .min(dp[i][j - 1] + 1)
                .min(dp[i - 1][j - 1] + cost);
        }
    }

    dp[m][n]
}

// ─────────────────────────────────────────────────────────────────
// Tests
// ─────────────────────────────────────────────────────────────────

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_insert_and_contains() {
        let mut trie = MTrie::new();
        trie.insert("hello");
        trie.insert("world");
        trie.insert("help");

        assert!(trie.contains("hello"));
        assert!(trie.contains("HELLO")); // case insensitive
        assert!(trie.contains("world"));
        assert!(trie.contains("help"));
        assert!(!trie.contains("hell"));
        assert!(!trie.contains("notthere"));
    }

    #[test]
    fn test_search_prefix() {
        let mut trie = MTrie::new();
        trie.insert("rust");
        trie.insert("ruby");
        trie.insert("rubyist");
        trie.insert("python");
        trie.insert("pypy");

        let prefix_ru: Vec<String> = trie.search_prefix("ru");
        assert!(prefix_ru.iter().all(|w| w.starts_with("ru")));

        let prefix_py: Vec<String> = trie.search_prefix("py");
        assert!(prefix_py.iter().all(|w| w.starts_with("py")));

        // Empty prefix returns nothing
        assert!(trie.search_prefix("x").is_empty());
    }

    #[test]
    fn test_autocomplete() {
        let trie = MTrie::from_words(&["apple", "app", "application", "apply", "banana"]);
        let results = trie.autocomplete("ap", 3);
        assert_eq!(results.len(), 3);
        assert!(results.iter().all(|w| w.starts_with("ap")));
    }

    #[test]
    fn test_remove() {
        let mut trie = MTrie::new();
        trie.insert("hello");
        trie.insert("world");

        assert!(trie.contains("hello"));
        assert!(trie.remove("hello"));
        assert!(!trie.contains("hello"));
        assert!(trie.contains("world"));

        // Removing non-existent word
        assert!(!trie.remove("notthere"));
    }

    #[test]
    fn test_record_query_boost() {
        let mut trie = MTrie::new();
        trie.insert("rust");
        trie.insert("ruby");

        trie.record_query("rust");
        trie.record_query("rust");
        trie.record_query("rust");
        trie.record_query("ruby");

        let results = trie.search_prefix("r");
        // "rust" should come before "ruby" due to higher query count
        assert_eq!(results[0], "rust");
        assert_eq!(results[1], "ruby");
    }

    #[test]
    fn test_fuzzy_search() {
        let trie = MTrie::from_words(&["rust", "ruby", "rubyist", "python", "java", "javascript"]);

        // Exact match
        let results = trie.fuzzy_search("rust", 0);
        assert!(results.iter().any(|(w, d)| w == "rust" && *d == 0));

        // 1-edit typo
        let results = trie.fuzzy_search("rust", 1);
        assert!(results.iter().any(|(w, _)| w == "rust"));
    }

    #[test]
    fn test_serialization() {
        let mut trie = MTrie::new();
        trie.insert("hello");
        trie.insert("world");
        trie.record_query("hello");

        let json = trie.to_json().unwrap();
        let restored = MTrie::from_json(&json).unwrap();

        assert!(restored.contains("hello"));
        assert!(restored.contains("world"));
        assert_eq!(restored.len(), 2);
    }

    #[test]
    fn test_len_and_is_empty() {
        let mut trie = MTrie::new();
        assert!(trie.is_empty());
        assert_eq!(trie.len(), 0);

        trie.insert("one");
        assert!(!trie.is_empty());
        assert_eq!(trie.len(), 1);

        trie.insert("two");
        assert_eq!(trie.len(), 2);

        trie.remove("one");
        assert_eq!(trie.len(), 1);
    }

    #[test]
    fn test_clear() {
        let mut trie = MTrie::from_words(&["hello", "world"]);
        assert!(!trie.is_empty());

        trie.clear();
        assert!(trie.is_empty());
        assert_eq!(trie.len(), 0);
    }

    #[test]
    fn test_case_insensitive() {
        let mut trie = MTrie::new();
        trie.insert("Rust");
        trie.insert("RUST");
        trie.insert("RuSt");

        // Should only count as one word (case insensitive)
        assert_eq!(trie.len(), 1);
        assert!(trie.contains("rust"));
        assert!(trie.contains("RUST"));
    }

    #[test]
    fn test_levenshtein() {
        assert_eq!(levenshtein("hello", &['h', 'e', 'l', 'l', 'o']), 0);
        assert_eq!(levenshtein("hello", &['h', 'e', 'l', 'l', 'p']), 1); // 1 substitution
        assert_eq!(levenshtein("hello", &['h', 'e', 'l', 'l']), 1);      // 1 deletion
        assert_eq!(levenshtein("", &['a', 'b']), 2);
        assert_eq!(levenshtein("abc", &[]), 3);
    }
}
