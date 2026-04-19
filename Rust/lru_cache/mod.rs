//! LRU Cache - Least Recently Used Cache Implementation
//!
//! A zero-dependency implementation of an LRU (Least Recently Used) cache
//! with O(1) average time complexity for get, put, and eviction operations.
//!
//! # Features
//!
//! - O(1) get, put, and eviction operations
//! - Capacity-based automatic eviction
//! - Zero external dependencies (uses only std)
//! - Thread-safe optional wrapper
//! - TTL (Time-To-Live) support
//! - Statistics tracking
//!
//! # Example
//!
//! ```
//! use lru_cache::LruCache;
//!
//! let mut cache = LruCache::new(3);
//! cache.put("a", 1);
//! cache.put("b", 2);
//! cache.put("c", 3);
//! assert_eq!(cache.get(&"a"), Some(&1));
//! cache.put("d", 4); // Evicts "b" (least recently used)
//! assert_eq!(cache.get(&"b"), None);
//! ```

use std::collections::HashMap;
use std::time::{Duration, Instant};

/// A node in the doubly linked list
struct Node<K, V> {
    key: K,
    value: V,
    prev: Option<usize>,
    next: Option<usize>,
    created_at: Option<Instant>,
    ttl: Option<Duration>,
}

/// LRU Cache implementation using a HashMap and doubly linked list
pub struct LruCache<K, V> {
    map: HashMap<K, usize>,
    nodes: Vec<Node<K, V>>,
    head: Option<usize>, // Most recently used
    tail: Option<usize>, // Least recently used
    capacity: usize,
    stats: CacheStats,
}

/// Cache statistics
#[derive(Debug, Clone, Default)]
pub struct CacheStats {
    pub hits: u64,
    pub misses: u64,
    pub evictions: u64,
    pub inserts: u64,
    pub updates: u64,
}

impl CacheStats {
    pub fn hit_rate(&self) -> f64 {
        let total = self.hits + self.misses;
        if total == 0 {
            0.0
        } else {
            self.hits as f64 / total as f64
        }
    }
}

/// An entry in the cache for iteration
#[derive(Debug, Clone)]
pub struct Entry<K, V> {
    pub key: K,
    pub value: V,
}

impl<K, V> LruCache<K, V>
where
    K: std::hash::Hash + Eq + Clone,
    V: Clone,
{
    /// Creates a new LRU cache with the specified capacity
    pub fn new(capacity: usize) -> Self {
        assert!(capacity > 0, "Capacity must be greater than 0");
        LruCache {
            map: HashMap::with_capacity(capacity),
            nodes: Vec::with_capacity(capacity),
            head: None,
            tail: None,
            capacity,
            stats: CacheStats::default(),
        }
    }

    /// Returns the number of entries in the cache
    pub fn len(&self) -> usize {
        self.map.len()
    }

    /// Returns true if the cache is empty
    pub fn is_empty(&self) -> bool {
        self.map.is_empty()
    }

    /// Returns the capacity of the cache
    pub fn capacity(&self) -> usize {
        self.capacity
    }

    /// Returns cache statistics
    pub fn stats(&self) -> &CacheStats {
        &self.stats
    }

    /// Resets cache statistics
    pub fn reset_stats(&mut self) {
        self.stats = CacheStats::default();
    }

    /// Gets a reference to the value associated with the key
    /// Returns None if the key is not present or has expired
    pub fn get(&mut self, key: &K) -> Option<&V> {
        if let Some(&idx) = self.map.get(key) {
            // Check TTL
            if self.is_expired(idx) {
                self.remove_by_index(idx);
                self.stats.misses += 1;
                return None;
            }
            self.move_to_head(idx);
            self.stats.hits += 1;
            Some(&self.nodes[idx].value)
        } else {
            self.stats.misses += 1;
            None
        }
    }

    /// Gets a mutable reference to the value associated with the key
    pub fn get_mut(&mut self, key: &K) -> Option<&mut V> {
        if let Some(&idx) = self.map.get(key) {
            // Check TTL
            if self.is_expired(idx) {
                self.remove_by_index(idx);
                self.stats.misses += 1;
                return None;
            }
            self.move_to_head(idx);
            self.stats.hits += 1;
            Some(&mut self.nodes[idx].value)
        } else {
            self.stats.misses += 1;
            None
        }
    }

    /// Gets the value and returns it cloned, without updating LRU order
    pub fn peek(&self, key: &K) -> Option<&V> {
        self.map.get(key).and_then(|&idx| {
            if self.is_expired(idx) {
                None
            } else {
                Some(&self.nodes[idx].value)
            }
        })
    }

    /// Inserts a key-value pair into the cache
    /// If the key already exists, the value is updated and moved to the front
    pub fn put(&mut self, key: K, value: V) -> Option<V> {
        self.put_with_ttl(key, value, None)
    }

    /// Inserts a key-value pair with a TTL (time-to-live)
    pub fn put_with_ttl(&mut self, key: K, value: V, ttl: Option<Duration>) -> Option<V> {
        if let Some(&idx) = self.map.get(&key) {
            // Update existing entry
            let old_value = std::mem::replace(&mut self.nodes[idx].value, value);
            self.nodes[idx].created_at = Some(Instant::now());
            self.nodes[idx].ttl = ttl;
            self.move_to_head(idx);
            self.stats.updates += 1;
            Some(old_value)
        } else {
            // Insert new entry
            let old_value = self.insert_new(key.clone(), value, ttl);
            self.stats.inserts += 1;
            old_value
        }
    }

    /// Removes a key from the cache
    pub fn remove(&mut self, key: &K) -> Option<V> {
        if let Some(&idx) = self.map.get(key) {
            let node = self.remove_node(idx);
            self.map.remove(key);
            Some(node.value)
        } else {
            None
        }
    }

    /// Checks if the cache contains a key (without updating LRU order)
    pub fn contains_key(&self, key: &K) -> bool {
        self.map.get(key).map_or(false, |&idx| !self.is_expired(idx))
    }

    /// Clears all entries from the cache
    pub fn clear(&mut self) {
        self.map.clear();
        self.nodes.clear();
        self.head = None;
        self.tail = None;
    }

    /// Returns the least recently used key (without removing it)
    pub fn lru_key(&self) -> Option<&K> {
        self.tail.map(|idx| &self.nodes[idx].key)
    }

    /// Returns all keys in LRU order (most recent first)
    pub fn keys(&self) -> Vec<&K> {
        let mut keys = Vec::with_capacity(self.map.len());
        let mut current = self.head;
        while let Some(idx) = current {
            keys.push(&self.nodes[idx].key);
            current = self.nodes[idx].next;
        }
        keys
    }

    /// Returns all values in LRU order (most recent first)
    pub fn values(&self) -> Vec<&V> {
        let mut values = Vec::with_capacity(self.map.len());
        let mut current = self.head;
        while let Some(idx) = current {
            values.push(&self.nodes[idx].value);
            current = self.nodes[idx].next;
        }
        values
    }

    /// Returns all entries in LRU order (most recent first)
    pub fn entries(&self) -> Vec<Entry<&K, &V>> {
        let mut entries = Vec::with_capacity(self.map.len());
        let mut current = self.head;
        while let Some(idx) = current {
            entries.push(Entry {
                key: &self.nodes[idx].key,
                value: &self.nodes[idx].value,
            });
            current = self.nodes[idx].next;
        }
        entries
    }

    /// Evicts expired entries
    pub fn evict_expired(&mut self) -> usize {
        let expired: Vec<K> = self
            .nodes
            .iter()
            .enumerate()
            .filter_map(|(idx, node)| {
                if self.is_expired(idx) {
                    Some(node.key.clone())
                } else {
                    None
                }
            })
            .collect();

        let count = expired.len();
        for key in expired {
            self.remove(&key);
        }
        count
    }

    // Private helper methods

    fn is_expired(&self, idx: usize) -> bool {
        if let Some(ttl) = self.nodes[idx].ttl {
            if let Some(created_at) = self.nodes[idx].created_at {
                return created_at.elapsed() > ttl;
            }
        }
        false
    }

    fn insert_new(&mut self, key: K, value: V, ttl: Option<Duration>) -> Option<V> {
        // Evict if at capacity
        let evicted = if self.map.len() >= self.capacity {
            self.evict_lru()
        } else {
            None
        };

        // Add new node
        let new_idx = self.nodes.len();
        let node = Node {
            key,
            value,
            prev: None,
            next: self.head,
            created_at: Some(Instant::now()),
            ttl,
        };
        self.nodes.push(node);

        // Update head's prev pointer
        if let Some(head_idx) = self.head {
            self.nodes[head_idx].prev = Some(new_idx);
        }

        // Update head
        self.head = Some(new_idx);

        // If this is the first node, it's also the tail
        if self.tail.is_none() {
            self.tail = Some(new_idx);
        }

        // Add to map
        self.map.insert(self.nodes[new_idx].key.clone(), new_idx);

        evicted
    }

    fn evict_lru(&mut self) -> Option<V> {
        if let Some(tail_idx) = self.tail {
            self.stats.evictions += 1;
            let node = self.remove_node(tail_idx);
            self.map.remove(&node.key);
            Some(node.value)
        } else {
            None
        }
    }

    fn remove_by_index(&mut self, idx: usize) {
        // Save the key before remove_node potentially swaps nodes
        let key = self.nodes[idx].key.clone();
        if self.map.contains_key(&key) {
            self.remove_node(idx);
            self.map.remove(&key);
        }
    }

    fn remove_node(&mut self, idx: usize) -> Node<K, V> {
        let node = &self.nodes[idx];
        let prev = node.prev;
        let next = node.next;

        // Update neighbors
        if let Some(prev_idx) = prev {
            self.nodes[prev_idx].next = next;
        } else {
            self.head = next;
        }

        if let Some(next_idx) = next {
            self.nodes[next_idx].prev = prev;
        } else {
            self.tail = prev;
        }

        // Remove the node (swap with last if not last)
        let removed = self.nodes.swap_remove(idx);

        // Update the index of swapped node if it exists
        if idx < self.nodes.len() {
            let _swapped_idx = self.nodes.len(); // This is now the old index of swapped element
            if let Some(&swapped_new_idx) = self.map.get(&self.nodes[idx].key) {
                // The swapped node is now at position idx
                // We need to update prev/next pointers
                let swapped_prev = self.nodes[idx].prev;
                let swapped_next = self.nodes[idx].next;

                if let Some(p) = swapped_prev {
                    self.nodes[p].next = Some(idx);
                }
                if let Some(n) = swapped_next {
                    self.nodes[n].prev = Some(idx);
                }

                // Update head/tail if needed
                if self.head == Some(swapped_new_idx) {
                    self.head = Some(idx);
                }
                if self.tail == Some(swapped_new_idx) {
                    self.tail = Some(idx);
                }

                // Update map
                self.map.insert(self.nodes[idx].key.clone(), idx);
            }
        }

        removed
    }

    fn move_to_head(&mut self, idx: usize) {
        if self.head == Some(idx) {
            return; // Already at head
        }

        // Detach from current position
        let node = &self.nodes[idx];
        let prev = node.prev;
        let next = node.next;

        if let Some(prev_idx) = prev {
            self.nodes[prev_idx].next = next;
        }

        if let Some(next_idx) = next {
            self.nodes[next_idx].prev = prev;
        } else {
            // Was tail
            self.tail = prev;
        }

        // Attach to head
        self.nodes[idx].prev = None;
        self.nodes[idx].next = self.head;

        if let Some(head_idx) = self.head {
            self.nodes[head_idx].prev = Some(idx);
        }

        self.head = Some(idx);
    }
}

impl<K, V> Default for LruCache<K, V>
where
    K: std::hash::Hash + Eq + Clone,
    V: Clone,
{
    fn default() -> Self {
        Self::new(100)
    }
}

/// Builder pattern for LRU Cache construction
pub struct LruCacheBuilder {
    capacity: usize,
}

impl LruCacheBuilder {
    pub fn new() -> Self {
        LruCacheBuilder { capacity: 100 }
    }

    pub fn capacity(mut self, capacity: usize) -> Self {
        self.capacity = capacity;
        self
    }

    pub fn build<K, V>(self) -> LruCache<K, V>
    where
        K: std::hash::Hash + Eq + Clone,
        V: Clone,
    {
        LruCache::new(self.capacity)
    }
}

impl Default for LruCacheBuilder {
    fn default() -> Self {
        Self::new()
    }
}

#[cfg(test)]
mod tests;

pub use self::stats::CacheStatsExt;

mod stats {
    use super::CacheStats;

    pub trait CacheStatsExt {
        fn summary(&self) -> String;
    }

    impl CacheStatsExt for CacheStats {
        fn summary(&self) -> String {
            format!(
                "hits: {}, misses: {}, evictions: {}, inserts: {}, updates: {}, hit_rate: {:.2}%",
                self.hits,
                self.misses,
                self.evictions,
                self.inserts,
                self.updates,
                self.hit_rate() * 100.0
            )
        }
    }
}