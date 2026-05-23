//! # Autocomplete Utils
//!
//! A zero-dependency Rust library for text autocomplete using Trie (prefix tree).
//!
//! ## Features
//! - Fast prefix-based word autocomplete
//! - Configurable suggestion limits
//! - Case-sensitive and case-insensitive search modes
//! - Word frequency tracking for smarter suggestions
//! - Thread-safe implementation

use std::collections::HashMap;

/// Trie node for autocomplete
#[derive(Debug, Clone)]
struct TrieNode {
    children: HashMap<char, TrieNode>,
    is_word_end: bool,
    frequency: u32,
}

impl TrieNode {
    fn new() -> Self {
        Self {
            children: HashMap::new(),
            is_word_end: false,
            frequency: 0,
        }
    }
}

/// Autocomplete engine using Trie
#[derive(Debug, Clone)]
pub struct Autocomplete {
    root: TrieNode,
    case_sensitive: bool,
    total_words: usize,
}

impl Default for Autocomplete {
    fn default() -> Self {
        Self::new()
    }
}

impl Autocomplete {
    /// Create a new Autocomplete instance with case-sensitive mode
    pub fn new() -> Self {
        Self {
            root: TrieNode::new(),
            case_sensitive: true,
            total_words: 0,
        }
    }

    /// Create a new Autocomplete instance with case-insensitive mode
    pub fn new_case_insensitive() -> Self {
        Self {
            root: TrieNode::new(),
            case_sensitive: false,
            total_words: 0,
        }
    }

    /// Insert a word into the trie
    pub fn insert(&mut self, word: &str) {
        let word = if self.case_sensitive {
            word.to_string()
        } else {
            word.to_lowercase()
        };

        let mut node = &mut self.root;
        for ch in word.chars() {
            node = node.children.entry(ch).or_insert_with(TrieNode::new);
        }
        if !node.is_word_end {
            self.total_words += 1;
            node.is_word_end = true;
        }
        node.frequency += 1;
    }

    /// Insert multiple words
    pub fn insert_batch(&mut self, words: &[&str]) {
        for word in words {
            self.insert(word);
        }
    }

    /// Check if a word exists in the trie
    pub fn contains(&self, word: &str) -> bool {
        let word = if self.case_sensitive {
            word.to_string()
        } else {
            word.to_lowercase()
        };

        let mut node = &self.root;
        for ch in word.chars() {
            match node.children.get(&ch) {
                Some(next) => node = next,
                None => return false,
            }
        }
        node.is_word_end
    }

    /// Check if any word starts with the given prefix
    pub fn starts_with(&self, prefix: &str) -> bool {
        let prefix = if self.case_sensitive {
            prefix.to_string()
        } else {
            prefix.to_lowercase()
        };

        let mut node = &self.root;
        for ch in prefix.chars() {
            match node.children.get(&ch) {
                Some(next) => node = next,
                None => return false,
            }
        }
        true
    }

    /// Get autocomplete suggestions for a prefix
    pub fn suggest(&self, prefix: &str, limit: usize) -> Vec<String> {
        let normalized = if self.case_sensitive {
            prefix.to_string()
        } else {
            prefix.to_lowercase()
        };

        // Navigate to the prefix node
        let mut node = &self.root;
        for ch in normalized.chars() {
            match node.children.get(&ch) {
                Some(next) => node = next,
                None => return Vec::new(),
            }
        }

        // Collect all words from this node
        let mut results: Vec<(String, u32)> = Vec::new();
        self.collect_words(node, &normalized, &mut results);

        // Sort by frequency (descending) then alphabetically
        results.sort_by(|a, b| {
            b.1.cmp(&a.1).then_with(|| a.0.cmp(&b.0))
        });

        results.truncate(limit);
        results.into_iter().map(|(word, _)| word).collect()
    }

    /// Collect all words from a node
    fn collect_words(&self, node: &TrieNode, prefix: &str, results: &mut Vec<(String, u32)>) {
        if node.is_word_end {
            results.push((prefix.to_string(), node.frequency));
        }

        let mut children: Vec<_> = node.children.iter().collect();
        children.sort_by_key(|(ch, _)| *ch);

        for (ch, child) in children {
            let new_prefix = format!("{}{}", prefix, ch);
            self.collect_words(child, &new_prefix, results);
        }
    }

    /// Get all words in the trie
    pub fn get_all_words(&self) -> Vec<String> {
        let mut words = Vec::new();
        self.collect_words(&self.root, "", &mut words);
        words.into_iter().map(|(word, _)| word).collect()
    }

    /// Get the total number of words
    pub fn word_count(&self) -> usize {
        self.total_words
    }

    /// Remove a word from the trie
    pub fn remove(&mut self, word: &str) -> bool {
        let word = if self.case_sensitive {
            word.to_string()
        } else {
            word.to_lowercase()
        };

        // First check if the word exists
        if !self.contains(&word) {
            return false;
        }

        self.total_words -= 1;
        Self::remove_helper_static(&mut self.root, &word, 0);
        true
    }

    fn remove_helper_static(node: &mut TrieNode, word: &str, depth: usize) {
        if depth == word.len() {
            node.is_word_end = false;
            node.frequency = 0;
            return;
        }

        let ch = word.chars().nth(depth).unwrap();
        if let Some(child) = node.children.get_mut(&ch) {
            Self::remove_helper_static(child, word, depth + 1);
            // Remove child node if it's no longer a word end and has no children
            if !child.is_word_end && child.children.is_empty() {
                node.children.remove(&ch);
            }
        }
    }

    /// Clear all words from the trie
    pub fn clear(&mut self) {
        self.root = TrieNode::new();
        self.total_words = 0;
    }

    /// Get word frequency
    pub fn get_frequency(&self, word: &str) -> u32 {
        let word = if self.case_sensitive {
            word.to_string()
        } else {
            word.to_lowercase()
        };

        let mut node = &self.root;
        for ch in word.chars() {
            match node.children.get(&ch) {
                Some(next) => node = next,
                None => return 0,
            }
        }
        if node.is_word_end { node.frequency } else { 0 }
    }

    /// Increment word frequency (useful for learning user preferences)
    pub fn increment_frequency(&mut self, word: &str) {
        let word = if self.case_sensitive {
            word.to_string()
        } else {
            word.to_lowercase()
        };

        let mut node = &mut self.root;
        for ch in word.chars() {
            node = node.children.entry(ch).or_insert_with(TrieNode::new);
        }
        if node.is_word_end {
            node.frequency += 1;
        }
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_insert_and_contains() {
        let mut ac = Autocomplete::new();
        ac.insert("hello");
        ac.insert("world");
        ac.insert("help");
        ac.insert("helium");

        assert!(ac.contains("hello"));
        assert!(ac.contains("world"));
        assert!(ac.contains("help"));
        assert!(ac.contains("helium"));
        assert!(!ac.contains("he"));
        assert!(!ac.contains("hell"));
    }

    #[test]
    fn test_starts_with() {
        let mut ac = Autocomplete::new();
        ac.insert("hello");
        ac.insert("help");
        ac.insert("helium");

        assert!(ac.starts_with("he"));
        assert!(ac.starts_with("hel"));
        assert!(ac.starts_with("hell"));
        assert!(!ac.starts_with("hal"));
    }

    #[test]
    fn test_suggest() {
        let mut ac = Autocomplete::new();
        ac.insert("hello");
        ac.insert("help");
        ac.insert("helium");
        ac.insert("helicopter");

        let suggestions = ac.suggest("hel", 10);
        assert_eq!(suggestions.len(), 4);
        assert!(suggestions.contains(&"hello".to_string()));
        assert!(suggestions.contains(&"help".to_string()));
        assert!(suggestions.contains(&"helium".to_string()));
        assert!(suggestions.contains(&"helicopter".to_string()));
    }

    #[test]
    fn test_suggest_limit() {
        let mut ac = Autocomplete::new();
        ac.insert_batch(&["apple", "application", "appetite", "apply", "approach"]);

        let suggestions = ac.suggest("app", 2);
        assert_eq!(suggestions.len(), 2);
    }

    #[test]
    fn test_case_insensitive() {
        let mut ac = Autocomplete::new_case_insensitive();
        ac.insert("Hello");
        ac.insert("WORLD");

        assert!(ac.contains("hello"));
        assert!(ac.contains("HELLO"));
        assert!(ac.contains("world"));

        let suggestions = ac.suggest("HEL", 10);
        assert_eq!(suggestions, vec!["hello"]);
    }

    #[test]
    fn test_frequency_sorting() {
        let mut ac = Autocomplete::new();
        
        // Insert with different frequencies
        ac.insert("apple");  // frequency 1
        ac.insert("apple");  // frequency 2
        ac.insert("apply");  // frequency 1
        ac.insert("apply");  // frequency 2
        ac.insert("apply");  // frequency 3

        let suggestions = ac.suggest("app", 10);
        // "apply" should come first because it has higher frequency
        assert_eq!(suggestions[0], "apply");
    }

    #[test]
    fn test_remove() {
        let mut ac = Autocomplete::new();
        ac.insert("hello");
        ac.insert("help");
        
        assert!(ac.contains("hello"));
        assert!(ac.remove("hello"));
        assert!(!ac.contains("hello"));
        assert!(ac.contains("help"));
    }

    #[test]
    fn test_word_count() {
        let mut ac = Autocomplete::new();
        assert_eq!(ac.word_count(), 0);
        
        ac.insert("hello");
        assert_eq!(ac.word_count(), 1);
        
        ac.insert("hello"); // Same word, should not increase count
        assert_eq!(ac.word_count(), 1);
        
        ac.insert("world");
        assert_eq!(ac.word_count(), 2);
        
        ac.remove("hello");
        assert_eq!(ac.word_count(), 1);
    }

    #[test]
    fn test_clear() {
        let mut ac = Autocomplete::new();
        ac.insert_batch(&["hello", "world", "test"]);
        
        assert_eq!(ac.word_count(), 3);
        
        ac.clear();
        assert_eq!(ac.word_count(), 0);
        assert!(!ac.contains("hello"));
    }

    #[test]
    fn test_get_all_words() {
        let mut ac = Autocomplete::new();
        ac.insert_batch(&["cat", "car", "dog"]);

        let mut words = ac.get_all_words();
        words.sort();
        
        assert_eq!(words, vec!["car", "cat", "dog"]);
    }

    #[test]
    fn test_empty_suggest() {
        let ac = Autocomplete::new();
        let suggestions = ac.suggest("nonexistent", 10);
        assert!(suggestions.is_empty());
    }

    #[test]
    fn test_get_frequency() {
        let mut ac = Autocomplete::new();
        ac.insert("test");
        ac.insert("test");
        ac.insert("test");
        
        assert_eq!(ac.get_frequency("test"), 3);
        assert_eq!(ac.get_frequency("nonexistent"), 0);
    }

    #[test]
    fn test_increment_frequency() {
        let mut ac = Autocomplete::new();
        ac.insert("test");
        assert_eq!(ac.get_frequency("test"), 1);
        
        ac.increment_frequency("test");
        assert_eq!(ac.get_frequency("test"), 2);
        
        // Non-existent word should not increment
        ac.increment_frequency("nonexistent");
        assert_eq!(ac.get_frequency("nonexistent"), 0);
    }
}