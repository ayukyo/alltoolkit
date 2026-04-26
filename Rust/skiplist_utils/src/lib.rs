//! # Skip List Utils
//!
//! A generic Skip List implementation in Rust.
//!
//! Skip List is a probabilistic data structure that provides O(log n) average
//! time complexity for search, insertion, and deletion operations.

use std::cmp::Ordering;
use std::fmt::Debug;

/// Default maximum level for the skip list
pub const DEFAULT_MAX_LEVEL: usize = 16;

/// Default probability for level generation
pub const DEFAULT_PROBABILITY: f64 = 0.5;

/// A node in the skip list
struct Node<K, V> {
    key: K,
    value: V,
    forward: Vec<usize>, // indices in the nodes vector
}

/// A skip list data structure using arena allocation
pub struct SkipList<K, V> {
    nodes: Vec<Node<K, V>>,
    level: usize,
    max_level: usize,
    probability: f64,
    length: usize,
    rng_state: u64,
}

impl<K, V> SkipList<K, V>
where
    K: Ord + Clone,
    V: Clone,
{
    /// Creates a new skip list with default settings
    pub fn new() -> Self {
        Self::with_max_level(DEFAULT_MAX_LEVEL)
    }

    /// Creates a new skip list with specified max level
    pub fn with_max_level(max_level: usize) -> Self {
        Self::with_config(max_level, DEFAULT_PROBABILITY)
    }

    /// Creates a new skip list with custom configuration
    pub fn with_config(max_level: usize, probability: f64) -> Self {
        let max_level = if max_level < 1 { DEFAULT_MAX_LEVEL } else { max_level };
        let probability = if probability <= 0.0 || probability >= 1.0 {
            DEFAULT_PROBABILITY
        } else {
            probability
        };

        SkipList {
            nodes: Vec::new(),
            level: 0,
            max_level,
            probability,
            length: 0,
            rng_state: 0x853c49e6748fea9b,
        }
    }

    fn next_u64(&mut self) -> u64 {
        let mut x = self.rng_state;
        x ^= x << 13;
        x ^= x >> 7;
        x ^= x << 17;
        self.rng_state = x;
        x
    }

    fn random_level(&mut self) -> usize {
        let mut level = 0;
        while (self.next_u64() as f64) / (u64::MAX as f64) < self.probability 
            && level < self.max_level - 1 {
            level += 1;
        }
        level
    }

    fn header_idx(&self) -> usize {
        0
    }

    /// Inserts a key-value pair into the skip list
    pub fn insert(&mut self, key: K, value: V) {
        // Initialize header if needed (index 0)
        if self.nodes.is_empty() {
            let header = Node {
                // Header node has dummy key/value
                key: key.clone(), // placeholder, will be overwritten
                value: value.clone(), // placeholder
                forward: vec![usize::MAX; self.max_level + 1],
            };
            self.nodes.push(header);
        }

        let mut update: Vec<usize> = vec![self.header_idx(); self.max_level + 1];
        let mut current = self.header_idx();

        // Find insertion position
        for i in (0..self.level).rev() {
            while self.nodes[current].forward[i] != usize::MAX {
                let next = self.nodes[current].forward[i];
                match self.nodes[next].key.cmp(&key) {
                    Ordering::Less => current = next,
                    Ordering::Greater => break,
                    Ordering::Equal => {
                        // Key exists, update value
                        self.nodes[next].value = value;
                        return;
                    }
                }
            }
            update[i] = current;
        }

        // Check level 0 for duplicate
        if self.nodes[current].forward[0] != usize::MAX {
            let next = self.nodes[current].forward[0];
            if self.nodes[next].key == key {
                self.nodes[next].value = value;
                return;
            }
        }

        let new_level = self.random_level();

        if new_level >= self.level {
            for i in self.level..=new_level {
                update[i] = self.header_idx();
            }
            self.level = new_level + 1;
        }

        // Create new node
        let new_idx = self.nodes.len();
        let mut new_node = Node {
            key,
            value,
            forward: vec![usize::MAX; new_level + 1],
        };

        // Set forward pointers
        for i in 0..=new_level {
            new_node.forward[i] = self.nodes[update[i]].forward[i];
            self.nodes[update[i]].forward[i] = new_idx;
        }

        self.nodes.push(new_node);
        self.length += 1;
    }

    /// Removes a key from the skip list
    pub fn remove(&mut self, key: &K) -> Option<V> {
        if self.nodes.is_empty() {
            return None;
        }

        let mut update: Vec<usize> = vec![self.header_idx(); self.max_level + 1];
        let mut current = self.header_idx();

        for i in (0..self.level).rev() {
            while self.nodes[current].forward[i] != usize::MAX {
                let next = self.nodes[current].forward[i];
                if self.nodes[next].key < *key {
                    current = next;
                } else {
                    break;
                }
            }
            update[i] = current;
        }

        current = self.nodes[current].forward[0];
        if current == usize::MAX {
            return None;
        }

        if self.nodes[current].key != *key {
            return None;
        }

        let value = self.nodes[current].value.clone();

        // Update forward pointers
        for i in 0..self.level {
            if self.nodes[update[i]].forward[i] != current {
                break;
            }
            self.nodes[update[i]].forward[i] = self.nodes[current].forward[i];
        }

        // Update level
        while self.level > 0 && self.nodes[self.header_idx()].forward[self.level - 1] == usize::MAX {
            self.level -= 1;
        }

        // Mark node as removed by setting its forward pointers to MAX
        // We don't actually remove from vector to maintain indices
        for i in 0..self.nodes[current].forward.len() {
            self.nodes[current].forward[i] = usize::MAX;
        }

        self.length -= 1;
        Some(value)
    }

    /// Searches for a value by key
    pub fn get(&self, key: &K) -> Option<&V> {
        if self.nodes.is_empty() {
            return None;
        }

        let mut current = self.header_idx();

        for i in (0..self.level).rev() {
            while self.nodes[current].forward[i] != usize::MAX {
                let next = self.nodes[current].forward[i];
                match self.nodes[next].key.cmp(key) {
                    Ordering::Less => current = next,
                    Ordering::Equal => return Some(&self.nodes[next].value),
                    Ordering::Greater => break,
                }
            }
        }

        current = self.nodes[current].forward[0];
        if current != usize::MAX && self.nodes[current].key == *key {
            Some(&self.nodes[current].value)
        } else {
            None
        }
    }

    /// Checks if a key exists
    pub fn contains(&self, key: &K) -> bool {
        self.get(key).is_some()
    }

    /// Returns the number of elements
    pub fn len(&self) -> usize {
        self.length
    }

    /// Checks if the skip list is empty
    pub fn is_empty(&self) -> bool {
        self.length == 0
    }

    /// Removes all elements
    pub fn clear(&mut self) {
        self.nodes.clear();
        self.level = 0;
        self.length = 0;
    }

    /// Returns the minimum key-value pair
    pub fn min(&self) -> Option<(&K, &V)> {
        if self.nodes.is_empty() || self.length == 0 {
            return None;
        }
        let first = self.nodes[self.header_idx()].forward[0];
        if first == usize::MAX {
            None
        } else {
            Some((&self.nodes[first].key, &self.nodes[first].value))
        }
    }

    /// Returns the maximum key-value pair
    pub fn max(&self) -> Option<(&K, &V)> {
        if self.nodes.is_empty() || self.length == 0 {
            return None;
        }

        let mut current = self.header_idx();
        for i in (0..self.level).rev() {
            while self.nodes[current].forward[i] != usize::MAX {
                current = self.nodes[current].forward[i];
            }
        }

        if current == self.header_idx() {
            None
        } else {
            Some((&self.nodes[current].key, &self.nodes[current].value))
        }
    }

    /// Returns all keys in sorted order
    pub fn keys(&self) -> Vec<&K> {
        let mut keys = Vec::with_capacity(self.length);
        if !self.nodes.is_empty() {
            let mut current = self.nodes[self.header_idx()].forward[0];
            while current != usize::MAX {
                keys.push(&self.nodes[current].key);
                current = self.nodes[current].forward[0];
            }
        }
        keys
    }

    /// Returns all values in sorted order by key
    pub fn values(&self) -> Vec<&V> {
        let mut values = Vec::with_capacity(self.length);
        if !self.nodes.is_empty() {
            let mut current = self.nodes[self.header_idx()].forward[0];
            while current != usize::MAX {
                values.push(&self.nodes[current].value);
                current = self.nodes[current].forward[0];
            }
        }
        values
    }

    /// Returns all key-value pairs in sorted order
    pub fn iter(&self) -> Iter<'_, K, V> {
        let first = if self.nodes.is_empty() {
            usize::MAX
        } else {
            self.nodes[self.header_idx()].forward[0]
        };
        Iter { nodes: &self.nodes, current: first }
    }

    /// Returns the rank (1-based position) of a key
    pub fn rank(&self, key: &K) -> Option<usize> {
        if self.nodes.is_empty() {
            return None;
        }

        let mut rank = 0;
        let mut current = self.nodes[self.header_idx()].forward[0];
        while current != usize::MAX {
            match self.nodes[current].key.cmp(key) {
                Ordering::Less => {
                    rank += 1;
                    current = self.nodes[current].forward[0];
                }
                Ordering::Equal => return Some(rank + 1),
                Ordering::Greater => break,
            }
        }
        None
    }

    /// Returns the key-value pair at the given rank (1-based)
    pub fn get_by_rank(&self, rank: usize) -> Option<(&K, &V)> {
        if rank < 1 || rank > self.length || self.nodes.is_empty() {
            return None;
        }

        let mut current = self.nodes[self.header_idx()].forward[0];
        for _ in 1..rank {
            if current == usize::MAX {
                return None;
            }
            current = self.nodes[current].forward[0];
        }

        if current == usize::MAX {
            None
        } else {
            Some((&self.nodes[current].key, &self.nodes[current].value))
        }
    }

    /// Returns the current level
    pub fn level(&self) -> usize {
        self.level
    }

    /// Returns the maximum level
    pub fn max_level(&self) -> usize {
        self.max_level
    }

    /// Applies a function to each element
    pub fn for_each<F>(&self, mut f: F)
    where
        F: FnMut(&K, &V) -> bool,
    {
        if self.nodes.is_empty() {
            return;
        }
        let mut current = self.nodes[self.header_idx()].forward[0];
        while current != usize::MAX {
            if !f(&self.nodes[current].key, &self.nodes[current].value) {
                break;
            }
            current = self.nodes[current].forward[0];
        }
    }
}

impl<K, V> Default for SkipList<K, V>
where
    K: Ord + Clone,
    V: Clone,
{
    fn default() -> Self {
        Self::new()
    }
}

/// Iterator over the skip list
pub struct Iter<'a, K, V> {
    nodes: &'a Vec<Node<K, V>>,
    current: usize,
}

impl<'a, K, V> Iterator for Iter<'a, K, V> {
    type Item = (&'a K, &'a V);

    fn next(&mut self) -> Option<Self::Item> {
        if self.current == usize::MAX {
            return None;
        }
        let key = &self.nodes[self.current].key;
        let value = &self.nodes[self.current].value;
        self.current = self.nodes[self.current].forward[0];
        Some((key, value))
    }
}

impl<K, V> SkipList<K, V>
where
    K: Ord + Clone + Debug,
    V: Clone + Debug,
{
    /// Prints the skip list structure (for debugging)
    pub fn print(&self) {
        if self.nodes.is_empty() {
            println!("Empty skip list");
            return;
        }

        for i in (0..self.level).rev() {
            print!("Level {}: ", i);
            let mut current = self.nodes[self.header_idx()].forward[i];
            while current != usize::MAX {
                print!("{:?} ", self.nodes[current].key);
                current = self.nodes[current].forward[i];
            }
            println!();
        }
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_new() {
        let sl: SkipList<i32, String> = SkipList::new();
        assert!(sl.is_empty());
        assert_eq!(sl.len(), 0);
    }

    #[test]
    fn test_insert_and_get() {
        let mut sl = SkipList::new();
        sl.insert(1, "one".to_string());
        sl.insert(2, "two".to_string());
        sl.insert(3, "three".to_string());

        assert_eq!(sl.len(), 3);
        assert_eq!(sl.get(&1), Some(&"one".to_string()));
        assert_eq!(sl.get(&2), Some(&"two".to_string()));
        assert_eq!(sl.get(&3), Some(&"three".to_string()));
        assert_eq!(sl.get(&4), None);
    }

    #[test]
    fn test_update() {
        let mut sl = SkipList::new();
        sl.insert(1, "one".to_string());
        sl.insert(1, "ONE".to_string());

        assert_eq!(sl.len(), 1);
        assert_eq!(sl.get(&1), Some(&"ONE".to_string()));
    }

    #[test]
    fn test_remove() {
        let mut sl = SkipList::new();
        sl.insert(1, "one".to_string());
        sl.insert(2, "two".to_string());
        sl.insert(3, "three".to_string());

        assert_eq!(sl.remove(&2), Some("two".to_string()));
        assert_eq!(sl.len(), 2);
        assert!(!sl.contains(&2));

        assert_eq!(sl.remove(&100), None);
    }

    #[test]
    fn test_contains() {
        let mut sl = SkipList::new();
        sl.insert(1, "one".to_string());

        assert!(sl.contains(&1));
        assert!(!sl.contains(&2));
    }

    #[test]
    fn test_min_max() {
        let mut sl = SkipList::new();
        sl.insert(5, "five".to_string());
        sl.insert(2, "two".to_string());
        sl.insert(8, "eight".to_string());
        sl.insert(1, "one".to_string());

        assert_eq!(sl.min(), Some((&1, &"one".to_string())));
        assert_eq!(sl.max(), Some((&8, &"eight".to_string())));
    }

    #[test]
    fn test_min_max_empty() {
        let sl: SkipList<i32, String> = SkipList::new();
        assert_eq!(sl.min(), None);
        assert_eq!(sl.max(), None);
    }

    #[test]
    fn test_keys_values() {
        let mut sl = SkipList::new();
        sl.insert(3, "three".to_string());
        sl.insert(1, "one".to_string());
        sl.insert(2, "two".to_string());

        let keys: Vec<&i32> = sl.keys();
        assert_eq!(keys, vec![&1, &2, &3]);

        let values: Vec<&String> = sl.values();
        assert_eq!(values, vec![&"one".to_string(), &"two".to_string(), &"three".to_string()]);
    }

    #[test]
    fn test_iter() {
        let mut sl = SkipList::new();
        sl.insert(1, "one".to_string());
        sl.insert(2, "two".to_string());
        sl.insert(3, "three".to_string());

        let pairs: Vec<_> = sl.iter().collect();
        assert_eq!(pairs.len(), 3);
        assert_eq!(pairs[0], (&1, &"one".to_string()));
        assert_eq!(pairs[1], (&2, &"two".to_string()));
        assert_eq!(pairs[2], (&3, &"three".to_string()));
    }

    #[test]
    fn test_rank() {
        let mut sl = SkipList::new();
        sl.insert(10, "ten".to_string());
        sl.insert(5, "five".to_string());
        sl.insert(15, "fifteen".to_string());
        sl.insert(20, "twenty".to_string());

        assert_eq!(sl.rank(&5), Some(1));
        assert_eq!(sl.rank(&10), Some(2));
        assert_eq!(sl.rank(&15), Some(3));
        assert_eq!(sl.rank(&20), Some(4));
        assert_eq!(sl.rank(&100), None);
    }

    #[test]
    fn test_get_by_rank() {
        let mut sl = SkipList::new();
        sl.insert(10, "ten".to_string());
        sl.insert(5, "five".to_string());
        sl.insert(15, "fifteen".to_string());

        assert_eq!(sl.get_by_rank(1), Some((&5, &"five".to_string())));
        assert_eq!(sl.get_by_rank(2), Some((&10, &"ten".to_string())));
        assert_eq!(sl.get_by_rank(3), Some((&15, &"fifteen".to_string())));
        assert_eq!(sl.get_by_rank(0), None);
        assert_eq!(sl.get_by_rank(100), None);
    }

    #[test]
    fn test_clear() {
        let mut sl = SkipList::new();
        sl.insert(1, "one".to_string());
        sl.insert(2, "two".to_string());

        sl.clear();
        assert!(sl.is_empty());
        assert_eq!(sl.len(), 0);
    }

    #[test]
    fn test_for_each() {
        let mut sl = SkipList::new();
        sl.insert(1, "one".to_string());
        sl.insert(2, "two".to_string());
        sl.insert(3, "three".to_string());

        let mut count = 0;
        sl.for_each(|_, _| {
            count += 1;
            true
        });
        assert_eq!(count, 3);

        // Test early exit
        count = 0;
        sl.for_each(|_, _| {
            count += 1;
            count < 2
        });
        assert_eq!(count, 2);
    }

    #[test]
    fn test_string_keys() {
        let mut sl = SkipList::new();
        sl.insert("banana".to_string(), 1);
        sl.insert("apple".to_string(), 2);
        sl.insert("cherry".to_string(), 3);

        let keys: Vec<_> = sl.keys();
        assert_eq!(keys, vec![&"apple".to_string(), &"banana".to_string(), &"cherry".to_string()]);
    }

    #[test]
    fn test_large_dataset() {
        let mut sl = SkipList::new();
        let n = 10000;

        for i in 0..n {
            sl.insert(i, i * i);
        }

        assert_eq!(sl.len(), n);

        for i in 0..n {
            assert_eq!(sl.get(&i), Some(&(i * i)));
        }

        // Delete half
        for i in 0..n/2 {
            assert!(sl.remove(&i).is_some());
        }

        assert_eq!(sl.len(), n / 2);

        // Verify deleted
        for i in 0..n/2 {
            assert!(!sl.contains(&i));
        }

        // Verify remaining
        for i in n/2..n {
            assert!(sl.contains(&i));
        }
    }

    #[test]
    fn test_out_of_order_insert() {
        let mut sl = SkipList::new();
        sl.insert(5, "five".to_string());
        sl.insert(1, "one".to_string());
        sl.insert(10, "ten".to_string());
        sl.insert(3, "three".to_string());
        sl.insert(7, "seven".to_string());

        let keys: Vec<_> = sl.keys();
        assert_eq!(keys, vec![&1, &3, &5, &7, &10]);
    }
}