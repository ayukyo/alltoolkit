//! Bloom Filter Utilities
//! 
//! A Bloom filter is a space-efficient probabilistic data structure used to test
//! whether an element is a member of a set. False positives are possible but
//! false negatives are not.
//!
//! Features:
//! - Configurable false positive rate
//! - Multiple hash functions using SipHash
//! - Add and check operations
//! - Merge two filters (union)
//! - Serialization support
//! - Zero external dependencies

use std::collections::hash_map::DefaultHasher;
use std::hash::{Hash, Hasher};

/// Bloom filter configuration
#[derive(Debug, Clone)]
pub struct BloomFilterConfig {
    /// Expected number of elements
    pub expected_items: usize,
    /// Desired false positive rate (0.0 to 1.0)
    pub false_positive_rate: f64,
}

impl Default for BloomFilterConfig {
    fn default() -> Self {
        Self {
            expected_items: 1000,
            false_positive_rate: 0.01,
        }
    }
}

/// Bloom filter implementation
#[derive(Debug, Clone)]
pub struct BloomFilter {
    /// Bit array
    bits: Vec<u8>,
    /// Number of bits
    num_bits: usize,
    /// Number of hash functions
    num_hashes: usize,
    /// Number of items added
    item_count: usize,
}

impl BloomFilter {
    /// Create a new Bloom filter with given configuration
    pub fn new(config: BloomFilterConfig) -> Self {
        let (num_bits, num_hashes) = Self::calculate_optimal_params(
            config.expected_items,
            config.false_positive_rate,
        );
        
        let num_bytes = (num_bits + 7) / 8;
        
        Self {
            bits: vec![0u8; num_bytes],
            num_bits,
            num_hashes,
            item_count: 0,
        }
    }
    
    /// Create a Bloom filter with custom size
    pub fn with_size(num_bits: usize, num_hashes: usize) -> Self {
        let num_bytes = (num_bits + 7) / 8;
        
        Self {
            bits: vec![0u8; num_bytes],
            num_bits,
            num_hashes,
            item_count: 0,
        }
    }
    
    /// Calculate optimal number of bits and hash functions
    pub fn calculate_optimal_params(expected_items: usize, false_positive_rate: f64) -> (usize, usize) {
        let ln2 = std::f64::consts::LN_2;
        let ln2_squared = ln2 * ln2;
        
        let num_bits = (-1.0 * expected_items as f64 * false_positive_rate.ln() / ln2_squared).ceil() as usize;
        let num_bits = num_bits.max(64); // Minimum 64 bits
        
        let num_hashes = (num_bits as f64 / expected_items as f64 * ln2).round() as usize;
        let num_hashes = num_hashes.max(1).min(32); // Between 1 and 32 hash functions
        
        (num_bits, num_hashes)
    }
    
    /// Add an item to the filter
    pub fn add<T: Hash>(&mut self, item: &T) {
        let hashes = self.hash_item(item);
        
        for i in 0..self.num_hashes {
            let bit_index = self.get_bit_index(&hashes, i);
            self.set_bit(bit_index);
        }
        
        self.item_count += 1;
    }
    
    /// Check if an item might be in the filter
    /// Returns false: definitely not in filter
    /// Returns true: probably in filter (may be false positive)
    pub fn contains<T: Hash>(&self, item: &T) -> bool {
        let hashes = self.hash_item(item);
        
        for i in 0..self.num_hashes {
            let bit_index = self.get_bit_index(&hashes, i);
            if !self.get_bit(bit_index) {
                return false;
            }
        }
        
        true
    }
    
    /// Get the current false positive rate based on number of items
    pub fn current_false_positive_rate(&self) -> f64 {
        if self.item_count == 0 {
            return 0.0;
        }
        
        let ratio = self.num_bits as f64 / self.item_count as f64;
        let exp_term = -(self.num_hashes as f64 / ratio);
        (1.0 - exp_term.exp()).powi(self.num_hashes as i32)
    }
    
    /// Get number of items added
    pub fn len(&self) -> usize {
        self.item_count
    }
    
    /// Check if filter is empty
    pub fn is_empty(&self) -> bool {
        self.item_count == 0
    }
    
    /// Get number of bits
    pub fn num_bits(&self) -> usize {
        self.num_bits
    }
    
    /// Get number of hash functions
    pub fn num_hashes(&self) -> usize {
        self.num_hashes
    }
    
    /// Clear all items from the filter
    pub fn clear(&mut self) {
        self.bits.fill(0);
        self.item_count = 0;
    }
    
    /// Merge another filter into this one (union)
    /// Both filters must have the same size and number of hash functions
    pub fn merge(&mut self, other: &BloomFilter) -> Result<(), BloomFilterError> {
        if self.num_bits != other.num_bits || self.num_hashes != other.num_hashes {
            return Err(BloomFilterError::IncompatibleFilters);
        }
        
        for i in 0..self.bits.len() {
            self.bits[i] |= other.bits[i];
        }
        
        // Item count is now approximate
        self.item_count = std::cmp::max(self.item_count, other.item_count);
        
        Ok(())
    }
    
    /// Get the bit array as bytes (for serialization)
    pub fn to_bytes(&self) -> &[u8] {
        &self.bits
    }
    
    /// Create filter from bytes (for deserialization)
    pub fn from_bytes(bytes: Vec<u8>, num_bits: usize, num_hashes: usize) -> Result<Self, BloomFilterError> {
        let expected_len = (num_bits + 7) / 8;
        if bytes.len() != expected_len {
            return Err(BloomFilterError::InvalidDataSize);
        }
        
        Ok(Self {
            bits: bytes,
            num_bits,
            num_hashes,
            item_count: 0,
        })
    }
    
    /// Count set bits (for estimating fill level)
    pub fn count_set_bits(&self) -> usize {
        self.bits.iter().map(|b| b.count_ones() as usize).sum()
    }
    
    /// Get fill ratio
    pub fn fill_ratio(&self) -> f64 {
        self.count_set_bits() as f64 / self.num_bits as f64
    }
    
    // Private helper methods
    
    fn hash_item<T: Hash>(&self, item: &T) -> (u64, u64) {
        let mut hasher1 = DefaultHasher::new();
        item.hash(&mut hasher1);
        let hash1 = hasher1.finish();
        
        let mut hasher2 = DefaultHasher::new();
        format!("{}:salt", hash1).hash(&mut hasher2);
        let hash2 = hasher2.finish();
        
        (hash1, hash2)
    }
    
    fn get_bit_index(&self, hashes: &(u64, u64), i: usize) -> usize {
        // Double hashing: h(i) = h1 + i * h2
        let index = hashes.0.wrapping_add((i as u64).wrapping_mul(hashes.1));
        (index % self.num_bits as u64) as usize
    }
    
    fn set_bit(&mut self, index: usize) {
        let byte_index = index / 8;
        let bit_offset = index % 8;
        self.bits[byte_index] |= 1 << bit_offset;
    }
    
    fn get_bit(&self, index: usize) -> bool {
        let byte_index = index / 8;
        let bit_offset = index % 8;
        (self.bits[byte_index] & (1 << bit_offset)) != 0
    }
}

/// Bloom filter errors
#[derive(Debug, Clone, PartialEq, Eq)]
pub enum BloomFilterError {
    /// Filters have incompatible sizes
    IncompatibleFilters,
    /// Invalid data size for deserialization
    InvalidDataSize,
}

impl std::fmt::Display for BloomFilterError {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        match self {
            BloomFilterError::IncompatibleFilters => write!(f, "Incompatible filter sizes"),
            BloomFilterError::InvalidDataSize => write!(f, "Invalid data size"),
        }
    }
}

impl std::error::Error for BloomFilterError {}

/// Counting Bloom Filter - supports removal
#[derive(Debug, Clone)]
pub struct CountingBloomFilter {
    /// Counter array (4 bits per counter)
    counters: Vec<u8>,
    /// Number of counters
    num_counters: usize,
    /// Number of hash functions
    num_hashes: usize,
    /// Number of items
    item_count: usize,
    /// Maximum counter value
    max_count: u8,
}

impl CountingBloomFilter {
    /// Create a new counting Bloom filter
    pub fn new(config: BloomFilterConfig) -> Self {
        let (num_bits, num_hashes) = BloomFilter::calculate_optimal_params(
            config.expected_items,
            config.false_positive_rate,
        );
        
        // Each counter is 4 bits, so we need half as many bytes
        let num_bytes = (num_bits + 1) / 2;
        
        Self {
            counters: vec![0u8; num_bytes],
            num_counters: num_bits,
            num_hashes,
            item_count: 0,
            max_count: 15, // 4-bit counter max
        }
    }
    
    /// Add an item to the filter
    pub fn add<T: Hash>(&mut self, item: &T) {
        let hashes = self.hash_item(item);
        
        for i in 0..self.num_hashes {
            let counter_index = self.get_bit_index(&hashes, i);
            self.increment_counter(counter_index);
        }
        
        self.item_count += 1;
    }
    
    /// Remove an item from the filter
    /// Returns true if the item was present (and removed)
    pub fn remove<T: Hash>(&mut self, item: &T) -> bool {
        if !self.contains(item) {
            return false;
        }
        
        let hashes = self.hash_item(item);
        
        for i in 0..self.num_hashes {
            let counter_index = self.get_bit_index(&hashes, i);
            self.decrement_counter(counter_index);
        }
        
        self.item_count = self.item_count.saturating_sub(1);
        true
    }
    
    /// Check if an item might be in the filter
    pub fn contains<T: Hash>(&self, item: &T) -> bool {
        let hashes = self.hash_item(item);
        
        for i in 0..self.num_hashes {
            let counter_index = self.get_bit_index(&hashes, i);
            if self.get_counter(counter_index) == 0 {
                return false;
            }
        }
        
        true
    }
    
    /// Get number of items
    pub fn len(&self) -> usize {
        self.item_count
    }
    
    /// Check if empty
    pub fn is_empty(&self) -> bool {
        self.item_count == 0
    }
    
    // Private helper methods
    
    fn hash_item<T: Hash>(&self, item: &T) -> (u64, u64) {
        let mut hasher1 = DefaultHasher::new();
        item.hash(&mut hasher1);
        let hash1 = hasher1.finish();
        
        let mut hasher2 = DefaultHasher::new();
        format!("{}:salt", hash1).hash(&mut hasher2);
        let hash2 = hasher2.finish();
        
        (hash1, hash2)
    }
    
    fn get_bit_index(&self, hashes: &(u64, u64), i: usize) -> usize {
        let index = hashes.0.wrapping_add((i as u64).wrapping_mul(hashes.1));
        (index % self.num_counters as u64) as usize
    }
    
    fn get_counter(&self, index: usize) -> u8 {
        let byte_index = index / 2;
        let is_high_nibble = index % 2 == 0;
        
        if is_high_nibble {
            self.counters[byte_index] >> 4
        } else {
            self.counters[byte_index] & 0x0F
        }
    }
    
    fn increment_counter(&mut self, index: usize) {
        let current = self.get_counter(index);
        if current < self.max_count {
            let byte_index = index / 2;
            let is_high_nibble = index % 2 == 0;
            
            if is_high_nibble {
                self.counters[byte_index] = (self.counters[byte_index] & 0x0F) | ((current + 1) << 4);
            } else {
                self.counters[byte_index] = (self.counters[byte_index] & 0xF0) | (current + 1);
            }
        }
    }
    
    fn decrement_counter(&mut self, index: usize) {
        let current = self.get_counter(index);
        if current > 0 {
            let byte_index = index / 2;
            let is_high_nibble = index % 2 == 0;
            
            if is_high_nibble {
                self.counters[byte_index] = (self.counters[byte_index] & 0x0F) | ((current - 1) << 4);
            } else {
                self.counters[byte_index] = (self.counters[byte_index] & 0xF0) | (current - 1);
            }
        }
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    
    #[test]
    fn test_bloom_filter_basic() {
        let config = BloomFilterConfig {
            expected_items: 100,
            false_positive_rate: 0.01,
        };
        let mut filter = BloomFilter::new(config);
        
        // Add items
        filter.add(&"apple");
        filter.add(&"banana");
        filter.add(&"cherry");
        
        // Check items
        assert!(filter.contains(&"apple"));
        assert!(filter.contains(&"banana"));
        assert!(filter.contains(&"cherry"));
        assert!(!filter.contains(&"grape"));
        assert!(!filter.contains(&"orange"));
    }
    
    #[test]
    fn test_bloom_filter_clear() {
        let mut filter = BloomFilter::with_size(1024, 3);
        
        filter.add(&"test1");
        filter.add(&"test2");
        assert!(!filter.is_empty());
        
        filter.clear();
        assert!(filter.is_empty());
        assert!(!filter.contains(&"test1"));
    }
    
    #[test]
    fn test_bloom_filter_merge() {
        let mut filter1 = BloomFilter::with_size(1024, 3);
        let mut filter2 = BloomFilter::with_size(1024, 3);
        
        filter1.add(&"apple");
        filter1.add(&"banana");
        
        filter2.add(&"cherry");
        filter2.add(&"date");
        
        filter1.merge(&filter2).unwrap();
        
        assert!(filter1.contains(&"apple"));
        assert!(filter1.contains(&"banana"));
        assert!(filter1.contains(&"cherry"));
        assert!(filter1.contains(&"date"));
    }
    
    #[test]
    fn test_bloom_filter_merge_incompatible() {
        let filter1 = BloomFilter::with_size(1024, 3);
        let filter2 = BloomFilter::with_size(2048, 3);
        
        let mut filter1 = filter1;
        let result = filter1.merge(&filter2);
        
        assert_eq!(result, Err(BloomFilterError::IncompatibleFilters));
    }
    
    #[test]
    fn test_bloom_filter_serialization() {
        let mut filter = BloomFilter::new(BloomFilterConfig {
            expected_items: 50,
            false_positive_rate: 0.1,
        });
        
        filter.add(&"hello");
        filter.add(&"world");
        
        let bytes = filter.to_bytes().to_vec();
        let num_bits = filter.num_bits();
        let num_hashes = filter.num_hashes();
        
        let restored = BloomFilter::from_bytes(bytes, num_bits, num_hashes).unwrap();
        
        assert!(restored.contains(&"hello"));
        assert!(restored.contains(&"world"));
    }
    
    #[test]
    fn test_counting_bloom_filter() {
        let mut filter = CountingBloomFilter::new(BloomFilterConfig {
            expected_items: 100,
            false_positive_rate: 0.01,
        });
        
        filter.add(&"test");
        assert!(filter.contains(&"test"));
        
        filter.remove(&"test");
        assert!(!filter.contains(&"test"));
    }
    
    #[test]
    fn test_counting_bloom_filter_multiple_adds() {
        let mut filter = CountingBloomFilter::new(BloomFilterConfig {
            expected_items: 100,
            false_positive_rate: 0.01,
        });
        
        filter.add(&"test");
        filter.add(&"test");
        filter.add(&"test");
        
        filter.remove(&"test");
        assert!(filter.contains(&"test")); // Still present
        
        filter.remove(&"test");
        assert!(filter.contains(&"test")); // Still present
        
        filter.remove(&"test");
        assert!(!filter.contains(&"test")); // Now removed
    }
    
    #[test]
    fn test_false_positive_rate() {
        let config = BloomFilterConfig {
            expected_items: 1000,
            false_positive_rate: 0.01,
        };
        let mut filter = BloomFilter::new(config);
        
        // Add 1000 items
        for i in 0..1000 {
            filter.add(&format!("item_{}", i));
        }
        
        // Test 10000 items not in the filter
        let mut false_positives = 0;
        for i in 1000..11000 {
            if filter.contains(&format!("item_{}", i)) {
                false_positives += 1;
            }
        }
        
        let actual_rate = false_positives as f64 / 10000.0;
        println!("Actual false positive rate: {:.4}", actual_rate);
        
        // Should be close to target
        assert!(actual_rate < 0.05, "False positive rate too high: {}", actual_rate);
    }
    
    #[test]
    fn test_optimal_params() {
        let (bits, hashes) = BloomFilter::calculate_optimal_params(1000, 0.01);
        
        // For 1000 items at 1% FPR, expect roughly 9586 bits and 7 hashes
        assert!(bits > 5000 && bits < 15000);
        assert!(hashes >= 5 && hashes <= 10);
    }
    
    #[test]
    fn test_fill_ratio() {
        let mut filter = BloomFilter::with_size(1000, 3);
        
        assert_eq!(filter.fill_ratio(), 0.0);
        
        filter.add(&"test");
        assert!(filter.fill_ratio() > 0.0);
        
        // Add more items
        for i in 0..100 {
            filter.add(&format!("item_{}", i));
        }
        
        assert!(filter.fill_ratio() > 0.0 && filter.fill_ratio() <= 1.0);
    }
    
    #[test]
    fn test_different_types() {
        let mut filter = BloomFilter::new(BloomFilterConfig::default());
        
        // Test with different types
        filter.add(&42i32);
        filter.add(&3.14f64.to_bits()); // Use to_bits() for f64
        filter.add(&"string");
        filter.add(&'c');
        filter.add(&vec![1, 2, 3]);
        
        assert!(filter.contains(&42i32));
        assert!(filter.contains(&3.14f64.to_bits()));
        assert!(filter.contains(&"string"));
        assert!(filter.contains(&'c'));
        assert!(filter.contains(&vec![1, 2, 3]));
        
        assert!(!filter.contains(&0i32));
        assert!(!filter.contains(&"other"));
    }
}

/// Example usage
pub fn example() {
    println!("=== Bloom Filter Example ===\n");
    
    // Create a bloom filter for 1000 items with 1% false positive rate
    let config = BloomFilterConfig {
        expected_items: 1000,
        false_positive_rate: 0.01,
    };
    let mut filter = BloomFilter::new(config);
    
    println!("Created filter with {} bits and {} hash functions", 
        filter.num_bits(), filter.num_hashes());
    
    // Add items
    let words = vec!["apple", "banana", "cherry", "date", "elderberry"];
    for word in &words {
        filter.add(word);
        println!("Added: {}", word);
    }
    
    println!("\nTesting membership:");
    for word in &words {
        println!("  {} -> {}", word, filter.contains(word));
    }
    
    println!("\nTesting non-members:");
    let non_members = vec!["grape", "kiwi", "lemon"];
    for word in &non_members {
        println!("  {} -> {} (correct: {})", 
            word, filter.contains(word), false);
    }
    
    println!("\nFilter stats:");
    println!("  Items added: {}", filter.len());
    println!("  Fill ratio: {:.2}%", filter.fill_ratio() * 100.0);
    println!("  Current FPR: {:.4}", filter.current_false_positive_rate());
    
    // Counting Bloom Filter example
    println!("\n=== Counting Bloom Filter Example ===\n");
    
    let mut counting_filter = CountingBloomFilter::new(BloomFilterConfig {
        expected_items: 100,
        false_positive_rate: 0.05,
    });
    
    counting_filter.add(&"removable");
    println!("Added 'removable': contains = {}", counting_filter.contains(&"removable"));
    
    counting_filter.remove(&"removable");
    println!("Removed 'removable': contains = {}", counting_filter.contains(&"removable"));
    
    // Merge example
    println!("\n=== Merge Example ===\n");
    
    let mut filter1 = BloomFilter::with_size(512, 3);
    let mut filter2 = BloomFilter::with_size(512, 3);
    
    filter1.add(&"a");
    filter1.add(&"b");
    filter2.add(&"c");
    filter2.add(&"d");
    
    filter1.merge(&filter2).unwrap();
    
    println!("Merged filter contains:");
    for item in &["a", "b", "c", "d"] {
        println!("  {} -> {}", item, filter1.contains(item));
    }
}