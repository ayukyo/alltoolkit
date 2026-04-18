//! Trie (Prefix Tree) Implementation
//!
//! A Trie is a tree-like data structure used for efficient retrieval of keys,
//! typically strings. It's particularly useful for autocomplete, spell checking,
//! IP routing, and dictionary implementations.
//!
//! # Features
//! - Zero external dependencies
//! - Generic key type support (strings, bytes, any sequence of keys)
//! - Prefix search and autocomplete
//! - Pattern matching with wildcards
//! - Memory-efficient node representation

use std::collections::HashMap;
use std::hash::Hash;

/// A node in the Trie
#[derive(Debug, Clone)]
struct TrieNode<K, V> 
where
    K: Eq + Hash + Clone,
{
    /// Children nodes
    children: HashMap<K, TrieNode<K, V>>,
    /// Value at this node (if it's a terminal)
    value: Option<V>,
    /// Number of words ending at or below this node
    word_count: usize,
}

impl<K, V> TrieNode<K, V>
where
    K: Eq + Hash + Clone,
{
    fn new() -> Self {
        TrieNode {
            children: HashMap::new(),
            value: None,
            word_count: 0,
        }
    }
    
    fn is_terminal(&self) -> bool {
        self.value.is_some()
    }
}

/// A Trie (Prefix Tree) data structure
/// 
/// Supports efficient prefix-based operations on sequences of keys.
/// 
/// # Example
/// ```
/// use trie_utils::Trie;
/// 
/// let mut trie = Trie::new();
/// trie.insert("hello".chars(), 1);
/// trie.insert("world".chars(), 2);
/// 
/// assert!(trie.contains(&"hello".chars().collect::<Vec<_>>()));
/// assert!(trie.starts_with(&"hel".chars().collect::<Vec<_>>()));
/// ```
#[derive(Debug, Clone)]
pub struct Trie<K, V = ()>
where
    K: Eq + Hash + Clone,
{
    root: TrieNode<K, V>,
    len: usize,
}

impl<K, V> Trie<K, V>
where
    K: Eq + Hash + Clone,
{
    /// Create a new empty Trie
    pub fn new() -> Self {
        Trie {
            root: TrieNode::new(),
            len: 0,
        }
    }
    
    /// Insert a key-value pair into the Trie
    /// 
    /// If the key already exists, the value is updated.
    /// Returns the previous value if the key existed.
    pub fn insert<I>(&mut self, key: I, value: V) -> Option<V>
    where
        I: IntoIterator<Item = K>,
    {
        let mut node = &mut self.root;
        
        for k in key.into_iter() {
            node.word_count += 1;
            node = node.children.entry(k).or_insert_with(TrieNode::new);
        }
        
        let old_value = node.value.replace(value);
        if old_value.is_none() {
            node.word_count += 1;
            self.len += 1;
        }
        old_value
    }
    
    /// Get a reference to the value associated with a key
    pub fn get(&self, key: &[K]) -> Option<&V> {
        let mut node = &self.root;
        
        for k in key {
            node = node.children.get(k)?;
        }
        
        node.value.as_ref()
    }
    
    /// Get a mutable reference to the value associated with a key
    pub fn get_mut(&mut self, key: &[K]) -> Option<&mut V> {
        let mut node = &mut self.root;
        
        for k in key {
            node = node.children.get_mut(k)?;
        }
        
        node.value.as_mut()
    }
    
    /// Check if the Trie contains a key
    pub fn contains(&self, key: &[K]) -> bool {
        self.get(key).is_some()
    }
    
    /// Check if there are any keys with the given prefix
    pub fn starts_with(&self, prefix: &[K]) -> bool {
        let mut node = &self.root;
        
        for k in prefix {
            match node.children.get(k) {
                Some(next) => node = next,
                None => return false,
            }
        }
        
        true
    }
    
    /// Count the number of keys with the given prefix
    pub fn count_prefix(&self, prefix: &[K]) -> usize {
        let mut node = &self.root;
        
        for k in prefix {
            match node.children.get(k) {
                Some(next) => node = next,
                None => return 0,
            }
        }
        
        node.word_count
    }
    
    /// Remove a key from the Trie
    /// 
    /// Returns the value if the key existed.
    pub fn remove(&mut self, key: &[K]) -> Option<V> {
        if key.is_empty() {
            let value = self.root.value.take()?;
            self.root.word_count -= 1;
            self.len -= 1;
            return Some(value);
        }

        // First, navigate to the target node to check existence
        let mut current = &self.root;
        for k in key {
            if !current.children.contains_key(k) {
                return None;
            }
            current = current.children.get(k).unwrap();
        }
        
        // Now remove the value and update counts
        let value = {
            let node = self.get_node_mut(key)?;
            let val = node.value.take()?;
            node.word_count -= 1;
            self.len -= 1;
            val
        };
        
        // Clean up empty nodes
        self.cleanup_empty_nodes(key);
        
        Some(value)
    }
    
    fn get_node_mut(&mut self, path: &[K]) -> Option<&mut TrieNode<K, V>> {
        let mut node = &mut self.root;
        for k in path {
            node = node.children.get_mut(k)?;
        }
        Some(node)
    }
    
    fn cleanup_empty_nodes(&mut self, path: &[K]) {
        // Walk down to find which nodes can be removed
        // Start from the deepest and work backwards
        for depth in (0..path.len()).rev() {
            let node = if depth == 0 {
                &mut self.root
            } else {
                match self.get_node_mut(&path[..depth]) {
                    Some(n) => n,
                    None => continue,
                }
            };
            
            let child_key = &path[depth];
            if let Some(child) = node.children.get(child_key) {
                if child.value.is_none() && child.children.is_empty() {
                    node.children.remove(child_key);
                    node.word_count -= 1;
                } else {
                    // Stop if child has value or other children
                    break;
                }
            }
        }
    }
    
    /// Get all keys with the given prefix
    /// 
    /// Returns a list of (key, value) pairs.
    pub fn get_by_prefix(&self, prefix: &[K]) -> Vec<(Vec<K>, &V)> {
        let mut results = Vec::new();
        
        // Navigate to prefix node
        let mut node = &self.root;
        for k in prefix {
            match node.children.get(k) {
                Some(next) => node = next,
                None => return results,
            }
        }
        
        // Collect all words under this node
        let mut current_key: Vec<K> = prefix.to_vec();
        self.collect_words(node, &mut current_key, &mut results);
        
        results
    }
    
    fn collect_words<'a>(
        &'a self,
        node: &'a TrieNode<K, V>,
        current_key: &mut Vec<K>,
        results: &mut Vec<(Vec<K>, &'a V)>,
    ) {
        if let Some(value) = &node.value {
            results.push((current_key.clone(), value));
        }
        
        for (k, child) in &node.children {
            current_key.push(k.clone());
            self.collect_words(child, current_key, results);
            current_key.pop();
        }
    }
    
    /// Clear all keys from the Trie
    pub fn clear(&mut self) {
        self.root = TrieNode::new();
        self.len = 0;
    }
    
    /// Get the number of keys in the Trie
    pub fn len(&self) -> usize {
        self.len
    }
    
    /// Check if the Trie is empty
    pub fn is_empty(&self) -> bool {
        self.len == 0
    }
    
    /// Get all keys in the Trie
    pub fn keys(&self) -> Vec<Vec<K>> {
        let mut keys = Vec::new();
        let mut current = Vec::new();
        self.collect_keys(&self.root, &mut current, &mut keys);
        keys
    }
    
    fn collect_keys(&self, node: &TrieNode<K, V>, current: &mut Vec<K>, keys: &mut Vec<Vec<K>>) {
        if node.value.is_some() {
            keys.push(current.clone());
        }
        
        for (k, child) in &node.children {
            current.push(k.clone());
            self.collect_keys(child, current, keys);
            current.pop();
        }
    }
    
    /// Get all values in the Trie
    pub fn values(&self) -> Vec<&V> {
        let mut values = Vec::new();
        self.collect_values(&self.root, &mut values);
        values
    }
    
    fn collect_values<'a>(&'a self, node: &'a TrieNode<K, V>, values: &mut Vec<&'a V>) {
        if let Some(value) = &node.value {
            values.push(value);
        }
        
        for child in node.children.values() {
            self.collect_values(child, values);
        }
    }
    
    /// Get iterator over all (key, value) pairs
    pub fn iter(&self) -> TrieIterator<'_, K, V> {
        TrieIterator::new(self)
    }
    
    /// Find the longest prefix that exists in the Trie
    /// 
    /// Returns the longest prefix found and its value (if terminal).
    pub fn longest_prefix(&self, key: &[K]) -> Option<(Vec<K>, &V)> {
        let mut node = &self.root;
        let mut result: Option<(Vec<K>, &V)> = None;
        let mut current_key = Vec::new();
        
        for k in key {
            match node.children.get(k) {
                Some(next) => {
                    current_key.push(k.clone());
                    if let Some(value) = &next.value {
                        result = Some((current_key.clone(), value));
                    }
                    node = next;
                }
                None => break,
            }
        }
        
        result
    }
    
    /// Find the shortest unique prefix for a key
    /// 
    /// Returns the shortest prefix that uniquely identifies the key
    /// (no other key shares this prefix).
    /// Returns None if the key doesn't exist in the Trie.
    pub fn shortest_unique_prefix(&self, key: &[K]) -> Option<Vec<K>> {
        if !self.contains(key) {
            return None;
        }
        
        let mut prefix = Vec::new();
        let mut node = &self.root;
        
        for k in key {
            prefix.push(k.clone());
            let child = node.children.get(k).unwrap();
            
            // The prefix is unique when:
            // 1. The parent had multiple choices (we made a unique decision)
            // 2. AND our chosen path leads to exactly one word
            // OR
            // 3. The parent was a terminal (a shorter word exists, our prefix is unique)
            if (node.children.len() > 1 && child.word_count == 1) || node.is_terminal() {
                return Some(prefix);
            }
            
            node = child;
        }
        
        // We've reached the end of the key
        Some(prefix)
    }
}

impl<K, V> Default for Trie<K, V>
where
    K: Eq + Hash + Clone,
{
    fn default() -> Self {
        Self::new()
    }
}

/// Iterator over Trie entries
pub struct TrieIterator<'a, K, V>
where
    K: Eq + Hash + Clone,
{
    stack: Vec<(&'a TrieNode<K, V>, Vec<K>)>,
}

impl<'a, K, V> TrieIterator<'a, K, V>
where
    K: Eq + Hash + Clone,
{
    fn new(trie: &'a Trie<K, V>) -> Self {
        TrieIterator {
            stack: vec![(&trie.root, Vec::new())],
        }
    }
}

impl<'a, K, V> Iterator for TrieIterator<'a, K, V>
where
    K: Eq + Hash + Clone,
{
    type Item = (Vec<K>, &'a V);
    
    fn next(&mut self) -> Option<Self::Item> {
        while let Some((node, key)) = self.stack.pop() {
            // Push children to stack
            for (k, child) in &node.children {
                let mut child_key = key.clone();
                child_key.push(k.clone());
                self.stack.push((child, child_key));
            }
            
            // Return this node if it has a value
            if let Some(value) = &node.value {
                return Some((key, value));
            }
        }
        
        None
    }
}

// String-specific convenience methods
impl<V: Clone> Trie<char, V> {
    /// Create a Trie from a string key (convenience method)
    pub fn insert_str(&mut self, key: &str, value: V) -> Option<V> {
        self.insert(key.chars(), value)
    }
    
    /// Get value for string key
    pub fn get_str(&self, key: &str) -> Option<&V> {
        let key_vec: Vec<char> = key.chars().collect();
        self.get(&key_vec)
    }
    
    /// Check if string key exists
    pub fn contains_str(&self, key: &str) -> bool {
        let key_vec: Vec<char> = key.chars().collect();
        self.contains(&key_vec)
    }
    
    /// Check if any string starts with prefix
    pub fn starts_with_str(&self, prefix: &str) -> bool {
        let prefix_vec: Vec<char> = prefix.chars().collect();
        self.starts_with(&prefix_vec)
    }
    
    /// Remove string key
    pub fn remove_str(&mut self, key: &str) -> Option<V> {
        let key_vec: Vec<char> = key.chars().collect();
        self.remove(&key_vec)
    }
    
    /// Get all strings with prefix
    pub fn get_by_prefix_str(&self, prefix: &str) -> Vec<(String, &V)> {
        let prefix_vec: Vec<char> = prefix.chars().collect();
        self.get_by_prefix(&prefix_vec)
            .into_iter()
            .map(|(chars, v)| (chars.into_iter().collect(), v))
            .collect()
    }
    
    /// Get longest prefix match for string
    pub fn longest_prefix_str(&self, key: &str) -> Option<(String, &V)> {
        let key_vec: Vec<char> = key.chars().collect();
        self.longest_prefix(&key_vec)
            .map(|(chars, v)| (chars.into_iter().collect(), v))
    }
    
    /// Get all keys as strings
    pub fn keys_str(&self) -> Vec<String> {
        self.keys()
            .into_iter()
            .map(|chars| chars.into_iter().collect())
            .collect()
    }
    
    /// Autocomplete: get all words that start with prefix
    pub fn autocomplete(&self, prefix: &str, limit: Option<usize>) -> Vec<String> {
        let prefix_vec: Vec<char> = prefix.chars().collect();
        let mut results: Vec<String> = self.get_by_prefix(&prefix_vec)
            .into_iter()
            .map(|(chars, _)| chars.into_iter().collect())
            .collect();
        
        if let Some(limit) = limit {
            results.truncate(limit);
        }
        
        results
    }
    
    /// Count words with given prefix (string convenience)
    pub fn count_prefix_str(&self, prefix: &str) -> usize {
        let prefix_vec: Vec<char> = prefix.chars().collect();
        self.count_prefix(&prefix_vec)
    }
}

impl Trie<char, ()> {
    /// Create a simple string set (Trie with no values)
    pub fn string_set() -> Self {
        Self::new()
    }
    
    /// Insert a string into the set
    pub fn insert_word(&mut self, word: &str) -> bool {
        let was_new = self.insert(word.chars(), ()).is_none();
        was_new
    }
    
    /// Check if word exists
    pub fn contains_word(&self, word: &str) -> bool {
        self.contains_str(word)
    }
}

/// Pattern matching support
impl<V: Clone> Trie<char, V> {
    /// Search for words matching a pattern
    /// 
    /// Pattern uses '?' as single character wildcard and '*' as multi-character wildcard.
    pub fn search_pattern(&self, pattern: &str) -> Vec<(String, &V)> {
        let pattern_chars: Vec<char> = pattern.chars().collect();
        let mut results = Vec::new();
        let mut current = String::new();
        self.search_pattern_recursive(&self.root, &pattern_chars, 0, &mut current, &mut results);
        results
    }
    
    fn search_pattern_recursive<'a>(
        &'a self,
        node: &'a TrieNode<char, V>,
        pattern: &[char],
        pos: usize,
        current: &mut String,
        results: &mut Vec<(String, &'a V)>,
    ) {
        // Pattern fully matched
        if pos >= pattern.len() {
            if let Some(value) = &node.value {
                results.push((current.clone(), value));
            }
            return;
        }
        
        let pat_char = pattern[pos];
        
        match pat_char {
            '?' => {
                // Match any single character
                for (k, child) in &node.children {
                    current.push(*k);
                    self.search_pattern_recursive(child, pattern, pos + 1, current, results);
                    current.pop();
                }
            }
            '*' => {
                // Match zero or more characters
                // Option 1: Match zero characters (skip *)
                self.search_pattern_recursive(node, pattern, pos + 1, current, results);
                
                // Option 2: Match one or more characters
                for (k, child) in &node.children {
                    current.push(*k);
                    self.search_pattern_recursive(child, pattern, pos, current, results);
                    current.pop();
                }
            }
            _ => {
                // Match exact character
                if let Some(child) = node.children.get(&pat_char) {
                    current.push(pat_char);
                    self.search_pattern_recursive(child, pattern, pos + 1, current, results);
                    current.pop();
                }
            }
        }
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    
    #[test]
    fn test_basic_insert_and_get() {
        let mut trie: Trie<char, i32> = Trie::new();
        
        trie.insert_str("hello", 1);
        trie.insert_str("world", 2);
        
        assert_eq!(trie.get_str("hello"), Some(&1));
        assert_eq!(trie.get_str("world"), Some(&2));
        assert_eq!(trie.get_str("missing"), None);
    }
    
    #[test]
    fn test_contains() {
        let mut trie: Trie<char, ()> = Trie::new();
        
        trie.insert_str("apple", ());
        trie.insert_str("app", ());
        
        assert!(trie.contains_str("apple"));
        assert!(trie.contains_str("app"));
        assert!(!trie.contains_str("ap"));
        assert!(!trie.contains_str("applepie"));
    }
    
    #[test]
    fn test_starts_with() {
        let mut trie: Trie<char, i32> = Trie::new();
        
        trie.insert_str("apple", 1);
        trie.insert_str("application", 2);
        trie.insert_str("banana", 3);
        
        assert!(trie.starts_with_str("app"));
        assert!(trie.starts_with_str("apple"));
        assert!(!trie.starts_with_str("ape"));
        assert!(trie.starts_with_str("ban"));
        assert!(!trie.starts_with_str("cat"));
    }
    
    #[test]
    fn test_remove() {
        let mut trie: Trie<char, i32> = Trie::new();
        
        trie.insert_str("hello", 1);
        trie.insert_str("hell", 2);
        trie.insert_str("hello world", 3);
        
        assert_eq!(trie.len(), 3);
        
        let removed = trie.remove_str("hello");
        assert_eq!(removed, Some(1));
        assert_eq!(trie.len(), 2);
        
        assert!(!trie.contains_str("hello"));
        assert!(trie.contains_str("hell"));
        assert!(trie.contains_str("hello world"));
    }
    
    #[test]
    fn test_get_by_prefix() {
        let mut trie: Trie<char, i32> = Trie::new();
        
        trie.insert_str("apple", 1);
        trie.insert_str("application", 2);
        trie.insert_str("appreciate", 3);
        trie.insert_str("banana", 4);
        
        let results = trie.get_by_prefix_str("app");
        assert_eq!(results.len(), 3);
        
        let words: Vec<&str> = results.iter().map(|(s, _)| s.as_str()).collect();
        assert!(words.contains(&"apple"));
        assert!(words.contains(&"application"));
        assert!(words.contains(&"appreciate"));
    }
    
    #[test]
    fn test_autocomplete() {
        let mut trie: Trie<char, i32> = Trie::new();
        
        trie.insert_str("cat", 1);
        trie.insert_str("car", 2);
        trie.insert_str("card", 3);
        trie.insert_str("care", 4);
        trie.insert_str("careful", 5);
        trie.insert_str("caret", 6);
        trie.insert_str("carpet", 7);
        
        let results = trie.autocomplete("car", Some(3));
        assert_eq!(results.len(), 3);
        
        let all = trie.autocomplete("car", None);
        assert_eq!(all.len(), 6);
    }
    
    #[test]
    fn test_longest_prefix() {
        let mut trie: Trie<char, i32> = Trie::new();
        
        trie.insert_str("a", 1);
        trie.insert_str("ab", 2);
        trie.insert_str("abc", 3);
        
        let result = trie.longest_prefix_str("abcd");
        assert_eq!(result, Some((String::from("abc"), &3)));
        
        let result = trie.longest_prefix_str("xyz");
        assert_eq!(result, None);
    }
    
    #[test]
    fn test_shortest_unique_prefix() {
        let mut trie: Trie<char, i32> = Trie::new();
        
        trie.insert_str("apple", 1);
        trie.insert_str("application", 2);
        trie.insert_str("banana", 3);
        trie.insert_str("ball", 4);
        
        // "banana" diverges from "ball" at 'n' vs 'l' after 'ba'
        // So shortest unique prefix for banana is 'ban'
        let key_vec: Vec<char> = "banana".chars().collect();
        let prefix = trie.shortest_unique_prefix(&key_vec);
        assert_eq!(prefix, Some(vec!['b', 'a', 'n']));
        
        // "apple" diverges from "application" at 'e' vs 'i' after 'appl'
        // So shortest unique prefix for apple is 'apple' (the full word)
        let key_vec: Vec<char> = "apple".chars().collect();
        let prefix = trie.shortest_unique_prefix(&key_vec);
        assert_eq!(prefix, Some(vec!['a', 'p', 'p', 'l', 'e']));
        
        // Test with a single unique word
        trie.insert_str("unique", 5);
        let key_vec: Vec<char> = "unique".chars().collect();
        let prefix = trie.shortest_unique_prefix(&key_vec);
        // 'u' is unique because no other word starts with 'u'
        assert_eq!(prefix, Some(vec!['u']));
    }
    
    #[test]
    fn test_pattern_search() {
        let mut trie: Trie<char, i32> = Trie::new();
        
        trie.insert_str("cat", 1);
        trie.insert_str("bat", 2);
        trie.insert_str("rat", 3);
        trie.insert_str("car", 4);
        trie.insert_str("cart", 5);
        trie.insert_str("cast", 6);
        
        // Single character wildcard
        let results = trie.search_pattern("?at");
        assert_eq!(results.len(), 3); // cat, bat, rat
        
        // Multi-character wildcard
        // ca* matches all words starting with 'ca' followed by anything (including empty)
        // Since we have: car, cart, cast, cat - all start with 'ca', we get 4 results
        let results = trie.search_pattern("ca*");
        assert_eq!(results.len(), 4); // car, cart, cast, cat
        
        // Verify the words
        let words: Vec<&str> = results.iter().map(|(s, _)| s.as_str()).collect();
        assert!(words.contains(&"car"));
        assert!(words.contains(&"cart"));
        assert!(words.contains(&"cast"));
        assert!(words.contains(&"cat"));
        
        // Test with different pattern that only matches specific subset
        let results = trie.search_pattern("car*");
        assert_eq!(results.len(), 2); // car, cart
    }
    
    #[test]
    fn test_count_prefix() {
        let mut trie: Trie<char, i32> = Trie::new();
        
        trie.insert_str("apple", 1);
        trie.insert_str("app", 2);
        trie.insert_str("application", 3);
        trie.insert_str("apply", 4);
        
        assert_eq!(trie.count_prefix_str("app"), 4);
        assert_eq!(trie.count_prefix_str("appl"), 3);
        assert_eq!(trie.count_prefix_str("apple"), 1);
        assert_eq!(trie.count_prefix_str("b"), 0);
    }
    
    #[test]
    fn test_keys_and_values() {
        let mut trie: Trie<char, i32> = Trie::new();
        
        trie.insert_str("one", 1);
        trie.insert_str("two", 2);
        trie.insert_str("three", 3);
        
        let keys = trie.keys_str();
        assert_eq!(keys.len(), 3);
        
        let values: Vec<i32> = trie.values().into_iter().cloned().collect();
        assert!(values.contains(&1));
        assert!(values.contains(&2));
        assert!(values.contains(&3));
    }
    
    #[test]
    fn test_iterator() {
        let mut trie: Trie<char, i32> = Trie::new();
        
        trie.insert_str("a", 1);
        trie.insert_str("ab", 2);
        trie.insert_str("abc", 3);
        
        let entries: Vec<_> = trie.iter().collect();
        assert_eq!(entries.len(), 3);
    }
    
    #[test]
    fn test_update_value() {
        let mut trie: Trie<char, i32> = Trie::new();
        
        trie.insert_str("key", 1);
        assert_eq!(trie.get_str("key"), Some(&1));
        
        let old = trie.insert_str("key", 2);
        assert_eq!(old, Some(1));
        assert_eq!(trie.get_str("key"), Some(&2));
    }
    
    #[test]
    fn test_clear() {
        let mut trie: Trie<char, i32> = Trie::new();
        
        trie.insert_str("one", 1);
        trie.insert_str("two", 2);
        
        assert_eq!(trie.len(), 2);
        
        trie.clear();
        
        assert_eq!(trie.len(), 0);
        assert!(trie.is_empty());
        assert!(!trie.contains_str("one"));
    }
    
    #[test]
    fn test_empty_trie() {
        let trie: Trie<char, i32> = Trie::new();
        
        assert!(trie.is_empty());
        assert_eq!(trie.len(), 0);
        assert!(!trie.contains_str("anything"));
    }
    
    #[test]
    fn test_string_set() {
        let mut set = Trie::string_set();
        
        assert!(set.insert_word("hello"));
        assert!(!set.insert_word("hello")); // Already exists
        
        assert!(set.contains_word("hello"));
        assert!(!set.contains_word("world"));
        
        assert_eq!(set.len(), 1);
    }
    
    #[test]
    fn test_byte_trie() {
        let mut trie: Trie<u8, &str> = Trie::new();
        
        trie.insert([0x01, 0x02, 0x03].into_iter(), "first");
        trie.insert([0x01, 0x02, 0x04].into_iter(), "second");
        
        let key1: Vec<u8> = vec![0x01, 0x02, 0x03];
        let key2: Vec<u8> = vec![0x01, 0x02];
        
        assert!(trie.contains(&key1));
        assert!(trie.starts_with(&key2));
        
        let key_missing: Vec<u8> = vec![0x01, 0x02, 0x05];
        assert!(!trie.contains(&key_missing));
    }
    
    #[test]
    fn test_remove_leaf_node() {
        let mut trie: Trie<char, i32> = Trie::new();
        
        trie.insert_str("a", 1);
        trie.insert_str("ab", 2);
        trie.insert_str("abc", 3);
        
        // Remove leaf node
        let removed = trie.remove_str("abc");
        assert_eq!(removed, Some(3));
        assert!(!trie.contains_str("abc"));
        assert!(trie.contains_str("ab"));
        assert!(trie.contains_str("a"));
    }
    
    #[test]
    fn test_remove_branch_node() {
        let mut trie: Trie<char, i32> = Trie::new();
        
        trie.insert_str("a", 1);
        trie.insert_str("ab", 2);
        trie.insert_str("abc", 3);
        
        // Remove branch node (has children)
        let removed = trie.remove_str("a");
        assert_eq!(removed, Some(1));
        assert!(!trie.contains_str("a"));
        assert!(trie.contains_str("ab")); // Children still exist
        assert!(trie.contains_str("abc"));
    }
    
    #[test]
    fn test_large_trie() {
        let mut trie: Trie<char, i32> = Trie::new();
        
        // Insert many words
        for i in 0..1000 {
            let word = format!("word{}", i);
            trie.insert_str(&word, i);
        }
        
        assert_eq!(trie.len(), 1000);
        
        // All words should be found
        for i in 0..1000 {
            let word = format!("word{}", i);
            assert!(trie.contains_str(&word));
        }
        
        // Prefix search
        let results = trie.get_by_prefix_str("word9");
        assert_eq!(results.len(), 111); // word9, word90-99, word900-999
    }
}