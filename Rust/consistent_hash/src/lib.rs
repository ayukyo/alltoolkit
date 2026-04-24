//! Consistent Hashing Implementation
//! 
//! A consistent hashing library for distributed systems with zero external dependencies.
//! Provides virtual nodes support for better distribution and minimal rebalancing on node changes.
//!
//! # Features
//! - Zero external dependencies
//! - Virtual nodes for better distribution
//! - Minimal data movement on node changes
//! - Thread-safe operations
//! - Weighted node support
//! - MurmurHash3-based hashing
//!
//! # Example
//! ```
//! use consistent_hash::ConsistentHash;
//!
//! let mut ring = ConsistentHash::<&str>::new();
//! ring.add_node("server1", 150);  // 150 virtual nodes
//! ring.add_node("server2", 150);
//! ring.add_node("server3", 150);
//!
//! // Get node for a key
//! let node = ring.get("user:12345").unwrap();
//! println!("Key 'user:12345' maps to {}", node);
//! ```

use std::collections::BTreeMap;
use std::hash::{Hash, Hasher};
use std::sync::{Arc, RwLock};

/// Default number of virtual nodes per physical node
const DEFAULT_VIRTUAL_NODES: usize = 150;

/// A node in the consistent hash ring
#[derive(Debug, Clone)]
pub struct Node<T: Clone + Eq + Hash> {
    /// The actual node identifier
    pub identifier: T,
    /// Number of virtual nodes (weight)
    pub virtual_nodes: usize,
    /// Node weight for weighted distribution
    pub weight: f64,
}

impl<T: Clone + Eq + Hash> Node<T> {
    /// Create a new node
    pub fn new(identifier: T, virtual_nodes: usize) -> Self {
        Node {
            identifier,
            virtual_nodes,
            weight: 1.0,
        }
    }

    /// Create a new node with weight
    pub fn with_weight(identifier: T, virtual_nodes: usize, weight: f64) -> Self {
        Node {
            identifier,
            virtual_nodes,
            weight,
        }
    }
}

/// Consistent Hash Ring Configuration
#[derive(Debug, Clone)]
pub struct RingConfig {
    /// Number of virtual nodes per physical node
    pub virtual_nodes: usize,
    /// Whether to use weighted distribution
    pub weighted: bool,
}

impl Default for RingConfig {
    fn default() -> Self {
        RingConfig {
            virtual_nodes: DEFAULT_VIRTUAL_NODES,
            weighted: false,
        }
    }
}

impl RingConfig {
    /// Create a new configuration with specified virtual nodes
    pub fn with_virtual_nodes(virtual_nodes: usize) -> Self {
        RingConfig {
            virtual_nodes,
            ..Default::default()
        }
    }
}

/// Consistent Hash Ring
/// 
/// A thread-safe consistent hash ring implementation supporting virtual nodes
/// for better distribution of keys across nodes.
#[derive(Debug)]
pub struct ConsistentHash<T: Clone + Eq + Hash> {
    /// The hash ring (sorted by hash value)
    ring: Arc<RwLock<BTreeMap<u64, Node<T>>>>,
    /// Mapping from identifier to nodes (for quick removal)
    node_map: Arc<RwLock<Vec<Node<T>>>>,
    /// Configuration
    config: RingConfig,
}

impl<T: Clone + Eq + Hash> ConsistentHash<T> {
    /// Create a new consistent hash ring with default configuration
    pub fn new() -> Self {
        Self::with_config(RingConfig::default())
    }

    /// Create a new consistent hash ring with specified number of virtual nodes
    pub fn with_virtual_nodes(virtual_nodes: usize) -> Self {
        Self::with_config(RingConfig::with_virtual_nodes(virtual_nodes))
    }

    /// Create a new consistent hash ring with custom configuration
    pub fn with_config(config: RingConfig) -> Self {
        ConsistentHash {
            ring: Arc::new(RwLock::new(BTreeMap::new())),
            node_map: Arc::new(RwLock::new(Vec::new())),
            config,
        }
    }

    /// Add a node to the ring with default virtual nodes
    pub fn add(&mut self, identifier: T) {
        self.add_node(identifier, self.config.virtual_nodes);
    }

    /// Add a node to the ring with specified number of virtual nodes
    pub fn add_node(&mut self, identifier: T, virtual_nodes: usize) {
        let node = Node::new(identifier, virtual_nodes);
        self.insert_node(node);
    }

    /// Add a weighted node to the ring
    pub fn add_weighted(&mut self, identifier: T, weight: f64) {
        let virtual_nodes = ((self.config.virtual_nodes as f64) * weight) as usize;
        let virtual_nodes = virtual_nodes.max(1);
        let node = Node::with_weight(identifier, virtual_nodes, weight);
        self.insert_node(node);
    }

    fn insert_node(&mut self, node: Node<T>) {
        let mut ring = self.ring.write().unwrap();
        let mut node_map = self.node_map.write().unwrap();

        // Generate virtual node hashes
        for i in 0..node.virtual_nodes {
            let hash = self.hash_virtual_node(&node.identifier, i);
            ring.insert(hash, node.clone());
        }

        node_map.push(node);
    }

    /// Remove a node from the ring
    pub fn remove(&mut self, identifier: &T) -> bool {
        let mut ring = self.ring.write().unwrap();
        let mut node_map = self.node_map.write().unwrap();

        // Find the node
        let node_idx = node_map.iter().position(|n| n.identifier == *identifier);
        if let Some(idx) = node_idx {
            let node = node_map.remove(idx);

            // Remove all virtual nodes
            for i in 0..node.virtual_nodes {
                let hash = self.hash_virtual_node(&node.identifier, i);
                ring.remove(&hash);
            }
            true
        } else {
            false
        }
    }

    /// Get the node responsible for a key
    pub fn get(&self, key: &str) -> Option<T> {
        let ring = self.ring.read().unwrap();
        
        if ring.is_empty() {
            return None;
        }

        let hash = self.hash_key(key);
        
        // Find the first node with hash >= key hash
        match ring.range(hash..).next() {
            Some((_, node)) => Some(node.identifier.clone()),
            None => {
                // Wrap around to the first node
                ring.values().next().map(|n| n.identifier.clone())
            }
        }
    }

    /// Get the node responsible for a key using a generic hashable key
    pub fn get_by_key<K: Hash>(&self, key: &K) -> Option<T> {
        let ring = self.ring.read().unwrap();
        
        if ring.is_empty() {
            return None;
        }

        let hash = self.hash_hashable(key);
        
        match ring.range(hash..).next() {
            Some((_, node)) => Some(node.identifier.clone()),
            None => {
                ring.values().next().map(|n| n.identifier.clone())
            }
        }
    }

    /// Get N nodes responsible for a key (for replication)
    pub fn get_n(&self, key: &str, n: usize) -> Vec<T> {
        let ring = self.ring.read().unwrap();
        
        if ring.is_empty() || n == 0 {
            return Vec::new();
        }

        let hash = self.hash_key(key);
        let total_nodes = self.node_count();
        let n = n.min(total_nodes);
        let mut result = Vec::with_capacity(n);
        let mut seen = std::collections::HashSet::new();

        // Start from the first matching node
        let mut iter = ring.range(hash..).chain(ring.iter());
        
        while result.len() < n {
            if let Some((_, node)) = iter.next() {
                if seen.insert(self.hash_identifier(&node.identifier)) {
                    result.push(node.identifier.clone());
                }
            } else {
                break;
            }
        }

        result
    }

    /// Check if a node exists in the ring
    pub fn contains(&self, identifier: &T) -> bool {
        let node_map = self.node_map.read().unwrap();
        node_map.iter().any(|n| n.identifier == *identifier)
    }

    /// Get the number of physical nodes
    pub fn node_count(&self) -> usize {
        self.node_map.read().unwrap().len()
    }

    /// Get the number of virtual nodes
    pub fn virtual_node_count(&self) -> usize {
        self.ring.read().unwrap().len()
    }

    /// Check if the ring is empty
    pub fn is_empty(&self) -> bool {
        self.ring.read().unwrap().is_empty()
    }

    /// Clear all nodes from the ring
    pub fn clear(&mut self) {
        let mut ring = self.ring.write().unwrap();
        let mut node_map = self.node_map.write().unwrap();
        ring.clear();
        node_map.clear();
    }

    /// Get all node identifiers
    pub fn nodes(&self) -> Vec<T> {
        self.node_map.read().unwrap().iter().map(|n| n.identifier.clone()).collect()
    }

    /// Calculate the distribution balance
    /// Returns a value between 0.0 (perfect balance) and 1.0 (worst imbalance)
    pub fn distribution_balance(&self, sample_keys: &[&str]) -> f64 {
        if sample_keys.is_empty() || self.is_empty() {
            return 0.0;
        }

        let mut distribution: std::collections::HashMap<u64, usize> = std::collections::HashMap::new();
        let node_count = self.node_count();

        // Count key distribution
        for key in sample_keys {
            if let Some(node) = self.get(key) {
                let node_hash = self.hash_identifier(&node);
                *distribution.entry(node_hash).or_insert(0) += 1;
            }
        }

        if distribution.is_empty() {
            return 0.0;
        }

        // Calculate standard deviation
        let ideal_count = sample_keys.len() as f64 / node_count as f64;
        let variance: f64 = distribution.values()
            .map(|&count| {
                let diff = count as f64 - ideal_count;
                diff * diff
            })
            .sum::<f64>() / node_count as f64;

        let std_dev = variance.sqrt();
        
        // Normalize to 0-1 range (lower is better)
        let max_dev = ideal_count; // Maximum possible deviation
        (std_dev / max_dev).min(1.0)
    }

    /// Get statistics about the ring
    pub fn stats(&self) -> RingStats {
        RingStats {
            node_count: self.node_count(),
            virtual_node_count: self.virtual_node_count(),
            virtual_nodes_per_node: if self.node_count() > 0 {
                self.virtual_node_count() as f64 / self.node_count() as f64
            } else {
                0.0
            },
        }
    }

    // Internal hashing methods using MurmurHash3-like algorithm
    
    fn hash_key(&self, key: &str) -> u64 {
        murmur3_hash(key.as_bytes(), 0)
    }

    fn hash_virtual_node(&self, identifier: &T, replica: usize) -> u64 {
        let mut hasher = SimpleHasher::new();
        identifier.hash(&mut hasher);
        replica.hash(&mut hasher);
        hasher.finish()
    }

    fn hash_identifier(&self, identifier: &T) -> u64 {
        let mut hasher = SimpleHasher::new();
        identifier.hash(&mut hasher);
        hasher.finish()
    }

    fn hash_hashable<K: Hash>(&self, key: &K) -> u64 {
        let mut hasher = SimpleHasher::new();
        key.hash(&mut hasher);
        hasher.finish()
    }
}

impl<T: Clone + Eq + Hash> Default for ConsistentHash<T> {
    fn default() -> Self {
        Self::new()
    }
}

impl<T: Clone + Eq + Hash> Clone for ConsistentHash<T> {
    fn clone(&self) -> Self {
        ConsistentHash {
            ring: Arc::new(RwLock::new(self.ring.read().unwrap().clone())),
            node_map: Arc::new(RwLock::new(self.node_map.read().unwrap().clone())),
            config: self.config.clone(),
        }
    }
}

/// Statistics about the hash ring
#[derive(Debug, Clone)]
pub struct RingStats {
    /// Number of physical nodes
    pub node_count: usize,
    /// Number of virtual nodes
    pub virtual_node_count: usize,
    /// Average virtual nodes per physical node
    pub virtual_nodes_per_node: f64,
}

/// MurmurHash3-like hash function
/// A simplified implementation for consistent hashing
fn murmur3_hash(data: &[u8], seed: u32) -> u64 {
    const C1: u64 = 0x87c37b91114253d5;
    const C2: u64 = 0x4cf5ad432745937f;
    const R1: u32 = 31;
    const R2: u32 = 27;
    const M: u64 = 5;
    const N1: u64 = 0x52dce729;
    const N2: u64 = 0x38495ab5;

    let mut h: u64 = seed as u64;
    let len = data.len();
    let nblocks = len / 8;

    // Body
    for i in 0..nblocks {
        let start = i * 8;
        let mut k = u64::from_le_bytes([
            data[start],
            data[start + 1],
            data[start + 2],
            data[start + 3],
            data[start + 4],
            data[start + 5],
            data[start + 6],
            data[start + 7],
        ]);

        k = k.wrapping_mul(C1);
        k = k.rotate_left(R1);
        k = k.wrapping_mul(C2);

        h ^= k;
        h = h.rotate_left(R2);
        h = h.wrapping_mul(M).wrapping_add(N1);
    }

    // Tail
    let tail = &data[nblocks * 8..];
    let mut k1: u64 = 0;

    match tail.len() {
        7 => {
            k1 ^= (tail[6] as u64) << 48;
            k1 ^= (tail[5] as u64) << 40;
            k1 ^= (tail[4] as u64) << 32;
            k1 ^= (tail[3] as u64) << 24;
            k1 ^= (tail[2] as u64) << 16;
            k1 ^= (tail[1] as u64) << 8;
            k1 ^= tail[0] as u64;
            k1 = k1.wrapping_mul(C1);
            k1 = k1.rotate_left(R1);
            k1 = k1.wrapping_mul(C2);
            h ^= k1;
        }
        6 => {
            k1 ^= (tail[5] as u64) << 40;
            k1 ^= (tail[4] as u64) << 32;
            k1 ^= (tail[3] as u64) << 24;
            k1 ^= (tail[2] as u64) << 16;
            k1 ^= (tail[1] as u64) << 8;
            k1 ^= tail[0] as u64;
            k1 = k1.wrapping_mul(C1);
            k1 = k1.rotate_left(R1);
            k1 = k1.wrapping_mul(C2);
            h ^= k1;
        }
        5 => {
            k1 ^= (tail[4] as u64) << 32;
            k1 ^= (tail[3] as u64) << 24;
            k1 ^= (tail[2] as u64) << 16;
            k1 ^= (tail[1] as u64) << 8;
            k1 ^= tail[0] as u64;
            k1 = k1.wrapping_mul(C1);
            k1 = k1.rotate_left(R1);
            k1 = k1.wrapping_mul(C2);
            h ^= k1;
        }
        4 => {
            k1 ^= (tail[3] as u64) << 24;
            k1 ^= (tail[2] as u64) << 16;
            k1 ^= (tail[1] as u64) << 8;
            k1 ^= tail[0] as u64;
            k1 = k1.wrapping_mul(C1);
            k1 = k1.rotate_left(R1);
            k1 = k1.wrapping_mul(C2);
            h ^= k1;
        }
        3 => {
            k1 ^= (tail[2] as u64) << 16;
            k1 ^= (tail[1] as u64) << 8;
            k1 ^= tail[0] as u64;
            k1 = k1.wrapping_mul(C1);
            k1 = k1.rotate_left(R1);
            k1 = k1.wrapping_mul(C2);
            h ^= k1;
        }
        2 => {
            k1 ^= (tail[1] as u64) << 8;
            k1 ^= tail[0] as u64;
            k1 = k1.wrapping_mul(C1);
            k1 = k1.rotate_left(R1);
            k1 = k1.wrapping_mul(C2);
            h ^= k1;
        }
        1 => {
            k1 ^= tail[0] as u64;
            k1 = k1.wrapping_mul(C1);
            k1 = k1.rotate_left(R1);
            k1 = k1.wrapping_mul(C2);
            h ^= k1;
        }
        _ => {}
    }

    // Finalization
    h ^= len as u64;
    h ^= h >> 33;
    h = h.wrapping_mul(N2);
    h ^= h >> 33;
    h = h.wrapping_mul(N2);
    h ^= h >> 33;

    h
}

/// Simple hasher for internal use
struct SimpleHasher {
    state: u64,
}

impl SimpleHasher {
    fn new() -> Self {
        SimpleHasher { state: 0 }
    }
}

impl Hasher for SimpleHasher {
    fn finish(&self) -> u64 {
        self.state
    }

    fn write(&mut self, bytes: &[u8]) {
        self.state = self.state.wrapping_add(murmur3_hash(bytes, self.state as u32));
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use std::collections::HashMap;

    #[test]
    fn test_basic_operations() {
        let mut ring = ConsistentHash::<&str>::new();
        
        ring.add_node("node1", 100);
        ring.add_node("node2", 100);
        ring.add_node("node3", 100);

        assert_eq!(ring.node_count(), 3);
        assert_eq!(ring.virtual_node_count(), 300);
        
        assert!(ring.contains(&"node1"));
        assert!(ring.contains(&"node2"));
        assert!(ring.contains(&"node3"));
        assert!(!ring.contains(&"node4"));
    }

    #[test]
    fn test_get_node() {
        let mut ring = ConsistentHash::<&str>::new();
        ring.add_node("server1", 100);
        ring.add_node("server2", 100);

        let node = ring.get("user:12345");
        assert!(node.is_some());
        
        // Same key should always return same node
        let node2 = ring.get("user:12345");
        assert_eq!(node, node2);
    }

    #[test]
    fn test_remove_node() {
        let mut ring = ConsistentHash::<&str>::new();
        ring.add_node("node1", 100);
        ring.add_node("node2", 100);

        assert!(ring.remove(&"node1"));
        assert_eq!(ring.node_count(), 1);
        assert!(!ring.contains(&"node1"));
        assert!(ring.contains(&"node2"));

        // Removing non-existent node should return false
        assert!(!ring.remove(&"node1"));
    }

    #[test]
    fn test_empty_ring() {
        let ring = ConsistentHash::<&str>::new();
        
        assert!(ring.is_empty());
        assert_eq!(ring.node_count(), 0);
        assert!(ring.get("any-key").is_none());
    }

    #[test]
    fn test_get_n_replicas() {
        let mut ring = ConsistentHash::<&str>::new();
        ring.add_node("node1", 100);
        ring.add_node("node2", 100);
        ring.add_node("node3", 100);
        ring.add_node("node4", 100);

        let nodes = ring.get_n("test-key", 3);
        assert_eq!(nodes.len(), 3);
        
        // All returned nodes should be unique
        let unique: std::collections::HashSet<_> = nodes.iter().collect();
        assert_eq!(unique.len(), 3);
    }

    #[test]
    fn test_get_n_more_than_nodes() {
        let mut ring = ConsistentHash::<&str>::new();
        ring.add_node("node1", 100);
        ring.add_node("node2", 100);

        let nodes = ring.get_n("test-key", 5);
        assert_eq!(nodes.len(), 2); // Only 2 nodes available
    }

    #[test]
    fn test_consistency() {
        let mut ring1 = ConsistentHash::<&str>::new();
        ring1.add_node("node1", 100);
        ring1.add_node("node2", 100);
        ring1.add_node("node3", 100);

        // Create identical ring
        let mut ring2 = ConsistentHash::<&str>::new();
        ring2.add_node("node1", 100);
        ring2.add_node("node2", 100);
        ring2.add_node("node3", 100);

        // Both rings should give same results
        for key in &["key1", "key2", "key3", "key4", "key5"] {
            assert_eq!(ring1.get(key), ring2.get(key));
        }
    }

    #[test]
    fn test_minimal_rebalancing() {
        let mut ring = ConsistentHash::<&str>::new();
        ring.add_node("node1", 150);
        ring.add_node("node2", 150);
        ring.add_node("node3", 150);

        // Record key assignments
        let keys: Vec<&str> = (0..1000).map(|i| Box::leak(format!("key{}", i).into_boxed_str()) as &str).collect();
        let original_mapping: HashMap<&str, &str> = keys.iter()
            .map(|&key| (key, ring.get(key).unwrap()))
            .collect();

        // Add a new node
        ring.add_node("node4", 150);

        // Check how many keys moved
        let mut moved = 0;
        for &key in &keys {
            let new_node = ring.get(key).unwrap();
            if new_node != *original_mapping.get(key).unwrap() {
                moved += 1;
            }
        }

        // Approximately 1/4 of keys should move (adding 4th node)
        let moved_ratio = moved as f64 / keys.len() as f64;
        println!("Keys moved: {} / {} ({:.1}%)", moved, keys.len(), moved_ratio * 100.0);
        
        // Should be roughly 25% (+/- 10%)
        assert!(moved_ratio > 0.15 && moved_ratio < 0.35, 
                "Unexpected rebalancing ratio: {}", moved_ratio);
    }

    #[test]
    fn test_weighted_nodes() {
        let mut ring = ConsistentHash::<&str>::new();
        ring.add_weighted("heavy", 2.0);
        ring.add_weighted("light", 0.5);

        // Heavy node should have 4x the virtual nodes of light node
        let stats = ring.stats();
        let ratio = stats.virtual_nodes_per_node;
        println!("Virtual nodes per node: {}", ratio);
        
        // Check distribution over many keys
        let mut counts: HashMap<&str, usize> = HashMap::new();
        for i in 0..1000 {
            let key = Box::leak(format!("key{}", i).into_boxed_str()) as &str;
            let node = ring.get(key).unwrap();
            *counts.entry(node).or_insert(0) += 1;
        }

        let heavy_count = counts.get("heavy").unwrap_or(&0);
        let light_count = counts.get("light").unwrap_or(&0);
        
        println!("Heavy: {}, Light: {}", heavy_count, light_count);
        
        // Heavy should receive more keys
        assert!(*heavy_count > *light_count);
    }

    #[test]
    fn test_distribution() {
        let mut ring = ConsistentHash::<&str>::new();
        for i in 1..=5 {
            let node = Box::leak(format!("node{}", i).into_boxed_str()) as &str;
            ring.add_node(node, 150);
        }

        let keys: Vec<&str> = (0..10000).map(|i| Box::leak(format!("key{}", i).into_boxed_str()) as &str).collect();
        let balance = ring.distribution_balance(&keys);
        
        println!("Distribution balance: {:.4}", balance);
        
        // Should be reasonably balanced (lower is better)
        assert!(balance < 0.5, "Distribution too unbalanced: {}", balance);
    }

    #[test]
    fn test_clear() {
        let mut ring = ConsistentHash::<&str>::new();
        ring.add_node("node1", 100);
        ring.add_node("node2", 100);

        ring.clear();
        
        assert!(ring.is_empty());
        assert_eq!(ring.node_count(), 0);
        assert_eq!(ring.virtual_node_count(), 0);
    }

    #[test]
    fn test_clone() {
        let mut ring1 = ConsistentHash::<&str>::new();
        ring1.add_node("node1", 100);
        ring1.add_node("node2", 100);

        let ring2 = ring1.clone();
        
        assert_eq!(ring1.node_count(), ring2.node_count());
        assert_eq!(ring1.virtual_node_count(), ring2.virtual_node_count());
        
        // They should give same results
        assert_eq!(ring1.get("test"), ring2.get("test"));
    }

    #[test]
    fn test_get_by_key() {
        let mut ring = ConsistentHash::<&str>::new();
        ring.add_node("node1", 100);
        ring.add_node("node2", 100);

        let result = ring.get_by_key(&42);
        assert!(result.is_some());

        let result2 = ring.get_by_key(&42);
        assert_eq!(result, result2);
    }

    #[test]
    fn test_stats() {
        let mut ring = ConsistentHash::<&str>::new();
        ring.add_node("node1", 100);
        ring.add_node("node2", 200);

        let stats = ring.stats();
        assert_eq!(stats.node_count, 2);
        assert_eq!(stats.virtual_node_count, 300);
        assert_eq!(stats.virtual_nodes_per_node, 150.0);
    }

    #[test]
    fn test_nodes() {
        let mut ring = ConsistentHash::<&str>::new();
        ring.add_node("node1", 100);
        ring.add_node("node2", 100);
        ring.add_node("node3", 100);

        let nodes = ring.nodes();
        assert_eq!(nodes.len(), 3);
        assert!(nodes.contains(&"node1"));
        assert!(nodes.contains(&"node2"));
        assert!(nodes.contains(&"node3"));
    }

    #[test]
    fn test_murmur3_hash_deterministic() {
        let data = b"test data";
        let h1 = murmur3_hash(data, 0);
        let h2 = murmur3_hash(data, 0);
        assert_eq!(h1, h2);
    }

    #[test]
    fn test_murmur3_hash_different_inputs() {
        let h1 = murmur3_hash(b"hello", 0);
        let h2 = murmur3_hash(b"world", 0);
        assert_ne!(h1, h2);
    }

    #[test]
    fn test_ring_config() {
        let mut ring = ConsistentHash::<&str>::with_virtual_nodes(200);
        ring.add("node1");

        let stats = ring.stats();
        assert_eq!(stats.virtual_node_count, 200);
    }

    #[test]
    fn test_thread_safety() {
        use std::sync::Arc;
        use std::thread;

        let mut ring = ConsistentHash::<String>::new();
        ring.add_node("node1".to_string(), 100);
        ring.add_node("node2".to_string(), 100);
        
        let ring = Arc::new(ring);
        let mut handles = vec![];

        for _ in 0..4 {
            let ring_clone = Arc::clone(&ring);
            handles.push(thread::spawn(move || {
                for i in 0..100 {
                    let key = format!("key{}", i);
                    let _ = ring_clone.get(&key);
                }
            }));
        }

        for handle in handles {
            handle.join().unwrap();
        }
    }
}