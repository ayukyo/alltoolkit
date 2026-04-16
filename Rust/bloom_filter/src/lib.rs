//! Bloom Filter Implementation
//! 
//! A Bloom filter is a space-efficient probabilistic data structure used to test
//! whether an element is a member of a set. False positives are possible but
//! false negatives are not.
//!
//! # Features
//! - Zero external dependencies
//! - Configurable false positive rate
//! - Generic hash function support
//! - Thread-safe operations
//! - Serialization support

use std::collections::hash_map::DefaultHasher;
use std::hash::{Hash, Hasher};
use std::marker::PhantomData;

/// Bloom filter configuration
#[derive(Debug, Clone, Copy)]
pub struct BloomConfig {
    /// Number of bits in the filter
    pub size: usize,
    /// Number of hash functions
    pub hash_count: usize,
}

impl BloomConfig {
    /// Create optimal config for expected items and desired false positive rate
    /// 
    /// # Arguments
    /// * `expected_items` - Expected number of items to insert
    /// * `false_positive_rate` - Desired false positive rate (0.0 to 1.0)
    /// 
    /// # Returns
    /// Optimal configuration for the given parameters
    pub fn optimal(expected_items: usize, false_positive_rate: f64) -> Self {
        let ln2 = std::f64::consts::LN_2;
        let ln2_sq = ln2 * ln2;
        
        // Optimal size: m = -n * ln(p) / ln(2)^2
        let size = (-((expected_items as f64) * false_positive_rate.ln()) / ln2_sq).ceil() as usize;
        
        // Optimal hash count: k = m/n * ln(2)
        let hash_count = ((size as f64) / (expected_items as f64) * ln2).ceil() as usize;
        
        // Ensure minimum values
        let size = size.max(64);
        let hash_count = hash_count.max(1).min(32);
        
        BloomConfig { size, hash_count }
    }
    
    /// Calculate expected false positive rate for given number of items
    pub fn expected_false_positive_rate(&self, num_items: usize) -> f64 {
        if self.size == 0 || num_items == 0 {
            return 0.0;
        }
        
        // P(false positive) ≈ (1 - e^(-kn/m))^k
        let ratio = (self.hash_count as f64 * num_items as f64) / (self.size as f64);
        let inner = 1.0 - (-ratio).exp();
        inner.powi(self.hash_count as i32)
    }
}

/// A Bloom filter for efficient set membership testing
#[derive(Debug, Clone)]
pub struct BloomFilter<T: Hash> {
    bits: Vec<u64>,
    config: BloomConfig,
    item_count: usize,
    _marker: PhantomData<T>,
}

impl<T: Hash> BloomFilter<T> {
    /// Create a new Bloom filter with the given configuration
    pub fn new(config: BloomConfig) -> Self {
        let num_words = (config.size + 63) / 64;
        BloomFilter {
            bits: vec![0u64; num_words],
            config,
            item_count: 0,
            _marker: PhantomData,
        }
    }
    
    /// Create a Bloom filter optimized for expected items and false positive rate
    pub fn with_rate(expected_items: usize, false_positive_rate: f64) -> Self {
        Self::new(BloomConfig::optimal(expected_items, false_positive_rate))
    }
    
    /// Create a Bloom filter with default settings (10000 items, 1% false positive rate)
    pub fn new_default() -> Self {
        Self::with_rate(10000, 0.01)
    }
    
    /// Insert an item into the filter
    pub fn insert(&mut self, item: &T) {
        let hashes = self.get_hashes(item);
        for i in 0..self.config.hash_count {
            let bit_index = self.get_bit_index(&hashes, i);
            self.set_bit(bit_index);
        }
        self.item_count += 1;
    }
    
    /// Check if an item might be in the filter
    /// 
    /// Returns `true` if the item might be present (may have false positives)
    /// Returns `false` if the item is definitely not present (no false negatives)
    pub fn contains(&self, item: &T) -> bool {
        let hashes = self.get_hashes(item);
        for i in 0..self.config.hash_count {
            let bit_index = self.get_bit_index(&hashes, i);
            if !self.get_bit(bit_index) {
                return false;
            }
        }
        true
    }
    
    /// Check if an item is present, and insert if not
    /// Returns true if item was already present (or false positive)
    pub fn check_and_insert(&mut self, item: &T) -> bool {
        let exists = self.contains(item);
        if !exists {
            self.insert(item);
        }
        exists
    }
    
    /// Clear all items from the filter
    pub fn clear(&mut self) {
        self.bits.fill(0);
        self.item_count = 0;
    }
    
    /// Get the number of items inserted
    pub fn len(&self) -> usize {
        self.item_count
    }
    
    /// Check if the filter is empty
    pub fn is_empty(&self) -> bool {
        self.item_count == 0
    }
    
    /// Get the current false positive rate based on number of items
    pub fn current_false_positive_rate(&self) -> f64 {
        self.config.expected_false_positive_rate(self.item_count)
    }
    
    /// Get the filter configuration
    pub fn config(&self) -> &BloomConfig {
        &self.config
    }
    
    /// Get the number of bits set in the filter
    pub fn bit_count(&self) -> usize {
        self.bits.iter().map(|w| w.count_ones() as usize).sum()
    }
    
    /// Get fill ratio (proportion of bits set)
    pub fn fill_ratio(&self) -> f64 {
        if self.config.size == 0 {
            return 0.0;
        }
        self.bit_count() as f64 / self.config.size as f64
    }
    
    /// Merge another Bloom filter into this one
    /// Both filters must have the same configuration
    pub fn merge(&mut self, other: &BloomFilter<T>) -> Result<(), &'static str> {
        if self.config.size != other.config.size || self.config.hash_count != other.config.hash_count {
            return Err("Cannot merge Bloom filters with different configurations");
        }
        
        for (i, &word) in other.bits.iter().enumerate() {
            self.bits[i] |= word;
        }
        
        // Item count is now approximate
        self.item_count = std::cmp::max(self.item_count, other.item_count);
        
        Ok(())
    }
    
    /// Convert filter to bytes for storage
    pub fn to_bytes(&self) -> Vec<u8> {
        let mut bytes = Vec::with_capacity(self.bits.len() * 8 + 16);
        
        // Header: size (8 bytes) + hash_count (8 bytes) + item_count (8 bytes)
        bytes.extend_from_slice(&(self.config.size as u64).to_le_bytes());
        bytes.extend_from_slice(&(self.config.hash_count as u64).to_le_bytes());
        bytes.extend_from_slice(&(self.item_count as u64).to_le_bytes());
        
        // Bits
        for word in &self.bits {
            bytes.extend_from_slice(&word.to_le_bytes());
        }
        
        bytes
    }
    
    /// Create filter from bytes
    pub fn from_bytes(bytes: &[u8]) -> Result<Self, &'static str> {
        if bytes.len() < 24 {
            return Err("Invalid bytes: too short");
        }
        
        let size = u64::from_le_bytes(bytes[0..8].try_into().unwrap()) as usize;
        let hash_count = u64::from_le_bytes(bytes[8..16].try_into().unwrap()) as usize;
        let item_count = u64::from_le_bytes(bytes[16..24].try_into().unwrap()) as usize;
        
        let num_words = (size + 63) / 64;
        let expected_len = 24 + num_words * 8;
        
        if bytes.len() < expected_len {
            return Err("Invalid bytes: incorrect length");
        }
        
        let mut bits = Vec::with_capacity(num_words);
        for i in 0..num_words {
            let start = 24 + i * 8;
            let end = start + 8;
            bits.push(u64::from_le_bytes(bytes[start..end].try_into().unwrap()));
        }
        
        Ok(BloomFilter {
            bits,
            config: BloomConfig { size, hash_count },
            item_count,
            _marker: PhantomData,
        })
    }
    
    // Internal helper methods
    
    fn get_hashes(&self, item: &T) -> (u64, u64) {
        let mut hasher1 = DefaultHasher::new();
        let mut hasher2 = DefaultHasher::new();
        
        // First hash
        item.hash(&mut hasher1);
        let h1 = hasher1.finish();
        
        // Second hash (using different seed)
        0xDEADBEEFu64.hash(&mut hasher2);
        item.hash(&mut hasher2);
        let h2 = hasher2.finish();
        
        (h1, h2)
    }
    
    fn get_bit_index(&self, hashes: &(u64, u64), i: usize) -> usize {
        // Double hashing: h(i) = h1 + i * h2
        let combined = hashes.0.wrapping_add((i as u64).wrapping_mul(hashes.1));
        (combined as usize) % self.config.size
    }
    
    fn set_bit(&mut self, index: usize) {
        let word_index = index / 64;
        let bit_offset = index % 64;
        self.bits[word_index] |= 1u64 << bit_offset;
    }
    
    fn get_bit(&self, index: usize) -> bool {
        let word_index = index / 64;
        let bit_offset = index % 64;
        (self.bits[word_index] >> bit_offset) & 1 == 1
    }
}

/// Scalable Bloom Filter that grows as needed
#[derive(Debug, Clone)]
pub struct ScalableBloomFilter<T: Hash> {
    filters: Vec<BloomFilter<T>>,
    initial_capacity: usize,
    error_rate: f64,
    growth_factor: f64,
    tightening_ratio: f64,
    item_count: usize,
}

impl<T: Hash> ScalableBloomFilter<T> {
    /// Create a new scalable Bloom filter
    /// 
    /// # Arguments
    /// * `initial_capacity` - Initial expected number of items
    /// * `error_rate` - Desired overall false positive rate
    pub fn new(initial_capacity: usize, error_rate: f64) -> Self {
        let first_filter = BloomFilter::with_rate(initial_capacity, error_rate * 0.5);
        
        ScalableBloomFilter {
            filters: vec![first_filter],
            initial_capacity,
            error_rate,
            growth_factor: 2.0,
            tightening_ratio: 0.5,
            item_count: 0,
        }
    }
    
    /// Insert an item
    pub fn insert(&mut self, item: &T) {
        // Always insert into the last filter
        let last = self.filters.last_mut().unwrap();
        
        // Check if current filter is getting full
        if last.fill_ratio() > 0.5 {
            // Create new filter with larger capacity
            let capacity = (self.initial_capacity as f64 * self.growth_factor.powi(self.filters.len() as i32)) as usize;
            let error_rate = self.error_rate * self.tightening_ratio.powi(self.filters.len() as i32 + 1);
            self.filters.push(BloomFilter::with_rate(capacity, error_rate));
        }
        
        self.filters.last_mut().unwrap().insert(item);
        self.item_count += 1;
    }
    
    /// Check if item might be present
    pub fn contains(&self, item: &T) -> bool {
        self.filters.iter().any(|f| f.contains(item))
    }
    
    /// Get total number of items
    pub fn len(&self) -> usize {
        self.item_count
    }
    
    /// Check if empty
    pub fn is_empty(&self) -> bool {
        self.item_count == 0
    }
    
    /// Get number of internal filters
    pub fn filter_count(&self) -> usize {
        self.filters.len()
    }
    
    /// Clear all filters
    pub fn clear(&mut self) {
        self.filters.truncate(1);
        self.filters[0].clear();
        self.item_count = 0;
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    
    #[test]
    fn test_bloom_config_optimal() {
        let config = BloomConfig::optimal(1000, 0.01);
        assert!(config.size > 0);
        assert!(config.hash_count > 0);
        assert!(config.hash_count <= 32);
    }
    
    #[test]
    fn test_bloom_filter_basic() {
        let mut filter: BloomFilter<&str> = BloomFilter::new_default();
        
        filter.insert(&"hello");
        filter.insert(&"world");
        
        assert!(filter.contains(&"hello"));
        assert!(filter.contains(&"world"));
        assert!(!filter.contains(&"missing"));
    }
    
    #[test]
    fn test_bloom_filter_with_rate() {
        let mut filter: BloomFilter<i32> = BloomFilter::with_rate(1000, 0.01);
        
        for i in 0..1000 {
            filter.insert(&i);
        }
        
        // All inserted items should be found
        for i in 0..1000 {
            assert!(filter.contains(&i));
        }
        
        // Check false positive rate
        let mut false_positives = 0;
        let test_count = 10000;
        for i in 1000..(1000 + test_count) {
            if filter.contains(&i) {
                false_positives += 1;
            }
        }
        
        let actual_rate = false_positives as f64 / test_count as f64;
        println!("Actual false positive rate: {:.4}", actual_rate);
        assert!(actual_rate < 0.05, "False positive rate too high: {}", actual_rate);
    }
    
    #[test]
    fn test_bloom_filter_clear() {
        let mut filter: BloomFilter<&str> = BloomFilter::new_default();
        
        filter.insert(&"test");
        assert!(filter.contains(&"test"));
        
        filter.clear();
        assert!(!filter.contains(&"test"));
        assert!(filter.is_empty());
    }
    
    #[test]
    fn test_bloom_filter_check_and_insert() {
        let mut filter: BloomFilter<&str> = BloomFilter::new_default();
        
        assert!(!filter.check_and_insert(&"first"));  // Returns false (was not present)
        assert!(filter.check_and_insert(&"first"));   // Returns true (now present)
        assert!(!filter.check_and_insert(&"second")); // Returns false (was not present)
    }
    
    #[test]
    fn test_bloom_filter_merge() {
        let config = BloomConfig::optimal(100, 0.01);
        
        let mut filter1: BloomFilter<i32> = BloomFilter::new(config);
        let mut filter2: BloomFilter<i32> = BloomFilter::new(config);
        
        for i in 0..50 {
            filter1.insert(&i);
        }
        for i in 50..100 {
            filter2.insert(&i);
        }
        
        filter1.merge(&filter2).unwrap();
        
        // All items should be found in merged filter
        for i in 0..100 {
            assert!(filter1.contains(&i));
        }
    }
    
    #[test]
    fn test_bloom_filter_serialization() {
        let mut filter: BloomFilter<&str> = BloomFilter::with_rate(100, 0.01);
        
        filter.insert(&"apple");
        filter.insert(&"banana");
        filter.insert(&"cherry");
        
        let bytes = filter.to_bytes();
        let restored = BloomFilter::<&str>::from_bytes(&bytes).unwrap();
        
        assert!(restored.contains(&"apple"));
        assert!(restored.contains(&"banana"));
        assert!(restored.contains(&"cherry"));
        assert!(!restored.contains(&"missing"));
        assert_eq!(filter.len(), restored.len());
    }
    
    #[test]
    fn test_scalable_bloom_filter() {
        let mut filter: ScalableBloomFilter<i32> = ScalableBloomFilter::new(100, 0.01);
        
        // Insert many items
        for i in 0..10000 {
            filter.insert(&i);
        }
        
        // All should be found
        for i in 0..10000 {
            assert!(filter.contains(&i));
        }
        
        // Should have grown to multiple filters
        assert!(filter.filter_count() > 1);
    }
    
    #[test]
    fn test_false_positive_rate_estimation() {
        let config = BloomConfig::optimal(1000, 0.01);
        let mut filter: BloomFilter<i32> = BloomFilter::new(config);
        
        for i in 0..500 {
            filter.insert(&i);
        }
        
        let estimated = filter.current_false_positive_rate();
        println!("Estimated FPR at {} items: {:.6}", filter.len(), estimated);
        
        // Should be reasonable estimate
        assert!(estimated > 0.0);
        assert!(estimated < 1.0);
    }
    
    #[test]
    fn test_fill_ratio() {
        let mut filter: BloomFilter<i32> = BloomFilter::with_rate(100, 0.1);
        
        let initial_ratio = filter.fill_ratio();
        assert_eq!(initial_ratio, 0.0);
        
        for i in 0..50 {
            filter.insert(&i);
        }
        
        let filled_ratio = filter.fill_ratio();
        println!("Fill ratio after 50 items: {:.4}", filled_ratio);
        assert!(filled_ratio > 0.0);
        assert!(filled_ratio < 1.0);
    }
    
    #[test]
    fn test_bloom_filter_strings() {
        let mut filter: BloomFilter<String> = BloomFilter::with_rate(100, 0.01);
        
        let words = vec!["hello", "world", "rust", "bloom", "filter"];
        for word in &words {
            filter.insert(&word.to_string());
        }
        
        for word in &words {
            assert!(filter.contains(&word.to_string()));
        }
    }
    
    #[test]
    fn test_bloom_filter_custom_types() {
        #[derive(Hash)]
        struct Point {
            x: i32,
            y: i32,
        }
        
        let mut filter: BloomFilter<Point> = BloomFilter::new_default();
        
        let p1 = Point { x: 1, y: 2 };
        let p2 = Point { x: 3, y: 4 };
        
        filter.insert(&p1);
        
        assert!(filter.contains(&p1));
        assert!(!filter.contains(&p2));
    }
    
    #[test]
    fn test_bloom_filter_edge_cases() {
        // Test with very small filter
        let config = BloomConfig { size: 64, hash_count: 2 };
        let mut filter: BloomFilter<i32> = BloomFilter::new(config);
        
        filter.insert(&1);
        assert!(filter.contains(&1));
        
        // Test with single hash function
        let config = BloomConfig { size: 1000, hash_count: 1 };
        let mut filter: BloomFilter<i32> = BloomFilter::new(config);
        
        filter.insert(&42);
        assert!(filter.contains(&42));
    }
}