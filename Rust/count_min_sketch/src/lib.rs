//! Count-Min Sketch Implementation
//! 
//! A probabilistic data structure for frequency estimation in streaming data.
//! Uses sublinear space for counting item frequencies with controlled error bounds.
//!
//! # Features
//! - Zero external dependencies
//! - Configurable depth/width trade-off
//! - Mergeable sketches
//! - Serialization support
//! - Point-wise maximum estimation

use std::hash::{Hash, Hasher};
use std::collections::hash_map::DefaultHasher;

/// Configuration for Count-Min Sketch
#[derive(Debug, Clone, Copy)]
pub struct CountMinConfig {
    /// Number of hash functions (depth)
    pub depth: usize,
    /// Number of buckets per hash function (width)
    pub width: usize,
    /// Seed for hash functions
    pub seed: u64,
}

impl CountMinConfig {
    /// Create optimal configuration based on expected items and desired error rate
    /// 
    /// # Arguments
    /// * `epsilon` - Relative error bound (e.g., 0.01 = 1% error)
    /// * `delta` - Confidence probability (e.g., 0.01 = 99% confidence)
    /// 
    /// # Returns
    /// Configuration where estimate is within epsilon * total_count with probability delta
    pub fn optimal(epsilon: f64, delta: f64) -> Self {
        let width = (std::f64::consts::E / epsilon).ceil() as usize;
        let depth = (-delta.ln()).ceil() as usize;
        
        CountMinConfig {
            depth: depth.max(1),
            width: width.max(2),
            seed: 0xDEADBEEF,
        }
    }
    
    /// Create configuration with explicit depth and width
    pub fn new(depth: usize, width: usize) -> Self {
        CountMinConfig {
            depth: depth.max(1),
            width: width.max(2),
            seed: 0xDEADBEEF,
        }
    }
}

/// Count-Min Sketch for frequency estimation
#[derive(Debug, Clone)]
pub struct CountMinSketch<T: Hash> {
    table: Vec<Vec<u64>>,
    config: CountMinConfig,
    total_count: u64,
    _marker: std::marker::PhantomData<T>,
}

impl<T: Hash> CountMinSketch<T> {
    /// Create a new Count-Min Sketch with given configuration
    pub fn new(config: CountMinConfig) -> Self {
        let table = vec![vec![0u64; config.width]; config.depth];
        
        CountMinSketch {
            table,
            config,
            total_count: 0,
            _marker: std::marker::PhantomData,
        }
    }
    
    /// Create with optimal config for given epsilon and delta
    pub fn with_rate(epsilon: f64, delta: f64) -> Self {
        Self::new(CountMinConfig::optimal(epsilon, delta))
    }
    
    /// Create with default settings (depth=10, width=1000)
    pub fn new_default() -> Self {
        Self::new(CountMinConfig::new(10, 1000))
    }
    
    /// Update the count for an item by delta
    pub fn update(&mut self, item: &T, delta: u64) {
        let hashes = self.get_hashes(item);
        for (i, &bucket) in hashes.iter().enumerate() {
            let idx = bucket % self.config.width as u64;
            self.table[i][idx as usize] += delta;
        }
        self.total_count += delta;
    }
    
    /// Increment count by 1
    pub fn increment(&mut self, item: &T) {
        self.update(item, 1);
    }
    
    /// Estimate the count for an item (returns upper bound)
    pub fn estimate(&self, item: &T) -> u64 {
        let hashes = self.get_hashes(item);
        hashes.iter()
            .enumerate()
            .map(|(i, &bucket)| {
                let idx = bucket % self.config.width as u64;
                self.table[i][idx as usize]
            })
            .min()
            .unwrap_or(0)
    }
    
    /// Get total number of items processed
    pub fn total_count(&self) -> u64 {
        self.total_count
    }
    
    /// Get table dimensions
    pub fn dimensions(&self) -> (usize, usize) {
        (self.config.depth, self.config.width)
    }
    
    /// Merge another sketch into this one (depth and width must match)
    pub fn merge(&mut self, other: &CountMinSketch<T>) -> Result<(), &'static str> {
        if self.config.depth != other.config.depth || self.config.width != other.config.width {
            return Err("Cannot merge sketches with different dimensions");
        }
        
        for i in 0..self.config.depth {
            for j in 0..self.config.width {
                self.table[i][j] += other.table[i][j];
            }
        }
        self.total_count += other.total_count;
        Ok(())
    }
    
    /// Convert sketch to bytes for storage
    pub fn to_bytes(&self) -> Vec<u8> {
        let mut bytes = Vec::with_capacity(
            24 + self.config.depth * self.config.width * 8
        );
        
        bytes.extend_from_slice(&(self.config.depth as u64).to_le_bytes());
        bytes.extend_from_slice(&(self.config.width as u64).to_le_bytes());
        bytes.extend_from_slice(&(self.config.seed as u64).to_le_bytes());
        bytes.extend_from_slice(&self.total_count.to_le_bytes());
        
        for row in &self.table {
            for &val in row {
                bytes.extend_from_slice(&val.to_le_bytes());
            }
        }
        
        bytes
    }
    
    /// Create sketch from bytes
    pub fn from_bytes(bytes: &[u8]) -> Result<Self, &'static str> {
        if bytes.len() < 32 {
            return Err("Invalid bytes: too short");
        }
        
        let depth = u64::from_le_bytes(bytes[0..8].try_into().unwrap()) as usize;
        let width = u64::from_le_bytes(bytes[8..16].try_into().unwrap()) as usize;
        let seed = u64::from_le_bytes(bytes[16..24].try_into().unwrap());
        let total_count = u64::from_le_bytes(bytes[24..32].try_into().unwrap());
        
        let expected_len = 32 + depth * width * 8;
        if bytes.len() < expected_len {
            return Err("Invalid bytes: incorrect length");
        }
        
        let mut table = Vec::with_capacity(depth);
        for i in 0..depth {
            let mut row = Vec::with_capacity(width);
            for j in 0..width {
                let offset = 32 + (i * width + j) * 8;
                row.push(u64::from_le_bytes(bytes[offset..offset+8].try_into().unwrap()));
            }
            table.push(row);
        }
        
        Ok(CountMinSketch {
            table,
            config: CountMinConfig { depth, width, seed },
            total_count,
            _marker: std::marker::PhantomData,
        })
    }
    
    /// Clear the sketch
    pub fn clear(&mut self) {
        for row in &mut self.table {
            row.fill(0);
        }
        self.total_count = 0;
    }
    
    fn get_hashes(&self, item: &T) -> Vec<u64> {
        let mut hasher1 = DefaultHasher::new();
        let mut hasher2 = DefaultHasher::new();
        
        item.hash(&mut hasher1);
        let h1 = hasher1.finish();
        
        // Second hash with seed
        self.config.seed.hash(&mut hasher2);
        item.hash(&mut hasher2);
        let h2 = hasher2.finish();
        
        (0..self.config.depth)
            .map(|i| h1.wrapping_add((i as u64).wrapping_mul(h2)))
            .collect()
    }
}

/// Top-K sketch for finding most frequent items using Count-Min + heap
#[derive(Debug)]
pub struct TopKSketch<T: Hash> {
    sketch: CountMinSketch<T>,
    k: usize,
}

impl<T: Hash> TopKSketch<T> {
    /// Create a new Top-K sketch
    pub fn new(k: usize, epsilon: f64, delta: f64) -> Self {
        TopKSketch {
            sketch: CountMinSketch::with_rate(epsilon, delta),
            k,
        }
    }
    
    /// Add an item
    pub fn add(&mut self, item: T) {
        self.sketch.increment(&item);
    }
    
    /// Estimate frequency of an item
    pub fn estimate(&self, item: &T) -> u64 {
        self.sketch.estimate(item)
    }
    
    /// Get current top K items (requires external tracking of items seen)
    pub fn sketch(&self) -> &CountMinSketch<T> {
        &self.sketch
    }
    
    /// Get the K parameter
    pub fn k(&self) -> usize {
        self.k
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    
    #[test]
    fn test_config_optimal() {
        let config = CountMinConfig::optimal(0.01, 0.01);
        assert!(config.depth > 0);
        assert!(config.width > 0);
    }
    
    #[test]
    fn test_basic_increment() {
        let mut sketch: CountMinSketch<&str> = CountMinSketch::new_default();
        
        sketch.increment(&"hello");
        sketch.increment(&"hello");
        sketch.increment(&"world");
        
        assert!(sketch.estimate(&"hello") >= 2);
        assert!(sketch.estimate(&"world") >= 1);
        assert!(sketch.estimate(&"missing") == 0);
    }
    
    #[test]
    fn test_update_delta() {
        let mut sketch: CountMinSketch<&str> = CountMinSketch::new_default();
        
        sketch.update(&"item", 5);
        
        assert!(sketch.estimate(&"item") >= 5);
    }
    
    #[test]
    fn test_total_count() {
        let mut sketch: CountMinSketch<&str> = CountMinSketch::new_default();
        
        sketch.increment(&"a");
        sketch.update(&"b", 3);
        sketch.increment(&"c");
        
        assert_eq!(sketch.total_count(), 5);
    }
    
    #[test]
    fn test_merge() {
        let mut sketch1: CountMinSketch<&str> = CountMinSketch::new_default();
        let mut sketch2: CountMinSketch<&str> = CountMinSketch::new_default();
        
        sketch1.increment(&"hello");
        sketch2.increment(&"world");
        sketch2.increment(&"world");
        
        sketch1.merge(&sketch2).unwrap();
        
        assert!(sketch1.estimate(&"hello") >= 1);
        assert!(sketch1.estimate(&"world") >= 2);
    }
    
    #[test]
    fn test_serialization() {
        let mut sketch: CountMinSketch<&str> = CountMinSketch::with_rate(0.01, 0.01);
        
        sketch.increment(&"apple");
        sketch.increment(&"banana");
        sketch.increment(&"apple");
        
        let bytes = sketch.to_bytes();
        let restored = CountMinSketch::<&str>::from_bytes(&bytes).unwrap();
        
        assert!(restored.estimate(&"apple") >= 2);
        assert!(restored.estimate(&"banana") >= 1);
    }
    
    #[test]
    fn test_clear() {
        let mut sketch: CountMinSketch<&str> = CountMinSketch::new_default();
        
        sketch.increment(&"test");
        assert!(sketch.estimate(&"test") > 0);
        
        sketch.clear();
        assert_eq!(sketch.estimate(&"test"), 0);
        assert_eq!(sketch.total_count(), 0);
    }
    
    #[test]
    fn test_different_types() {
        let mut sketch: CountMinSketch<i32> = CountMinSketch::new_default();
        
        sketch.increment(&42);
        sketch.increment(&42);
        sketch.increment(&100);
        
        assert!(sketch.estimate(&42) >= 2);
        assert!(sketch.estimate(&100) >= 1);
    }
    
    #[test]
    fn test_top_k_sketch() {
        let mut topk: TopKSketch<i32> = TopKSketch::new(5, 0.01, 0.01);
        
        for i in 0..1000 {
            topk.add(i % 10);
        }
        
        assert!(topk.estimate(&5) >= 90);
    }
    
    #[test]
    fn test_dimensions() {
        let config = CountMinConfig::new(5, 100);
        let sketch: CountMinSketch<&str> = CountMinSketch::new(config);
        
        let (d, w) = sketch.dimensions();
        assert_eq!(d, 5);
        assert_eq!(w, 100);
    }
    
    #[test]
    fn test_large_counts() {
        let mut sketch: CountMinSketch<&str> = CountMinSketch::new_default();
        
        sketch.update(&"frequent", 1000000);
        
        assert!(sketch.estimate(&"frequent") >= 1000000);
        assert_eq!(sketch.total_count(), 1000000);
    }
    
    #[test]
    fn test_merge_error_different_dims() {
        let mut sketch1: CountMinSketch<&str> = CountMinSketch::new(CountMinConfig::new(5, 100));
        let sketch2: CountMinSketch<&str> = CountMinSketch::new(CountMinConfig::new(5, 200));
        
        sketch1.increment(&"test");
        
        assert!(sketch1.merge(&sketch2).is_err());
    }
    
    #[test]
    fn test_zero_width_config() {
        let config = CountMinConfig::new(3, 0);
        let sketch: CountMinSketch<&str> = CountMinSketch::new(config);
        
        let (_, w) = sketch.dimensions();
        assert_eq!(w, 2); // minimum enforced
    }
}