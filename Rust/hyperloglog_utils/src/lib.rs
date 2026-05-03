//! HyperLogLog Utils - A memory-efficient cardinality estimation data structure
//!
//! HyperLogLog is a probabilistic algorithm for estimating the cardinality
//! (number of distinct elements) of a multiset with a typical error rate of
//! about 1.04/sqrt(m), where m is the number of registers.
//!
//! # Features
//! - Zero external dependencies
//! - Configurable precision (4-16 bits for register indexing)
//! - Standard hash function using FNV-1a
//! - Merge multiple HyperLogLog instances
//! - Serialization support
//!
//! # Example
//! ```
//! use hyperloglog_utils::HyperLogLog;
//!
//! let mut hll = HyperLogLog::new(12).unwrap();
//! hll.insert(b"hello");
//! hll.insert(b"world");
//! hll.insert(b"hello"); // duplicate
//!
//! let count = hll.count();
//! println!("Estimated unique elements: {}", count);
//! ```

use std::hash::{Hash, Hasher};

/// FNV-1a hash implementation (no external dependencies)
#[derive(Default)]
struct FnvHasher(u64);

impl FnvHasher {
    fn new() -> Self {
        FnvHasher(0xcbf29ce484222325)
    }
}

impl Hasher for FnvHasher {
    fn finish(&self) -> u64 {
        self.0
    }

    fn write(&mut self, bytes: &[u8]) {
        for byte in bytes {
            self.0 ^= *byte as u64;
            self.0 = self.0.wrapping_mul(0x100000001b3);
        }
    }
}

/// Improved hash function for HyperLogLog
/// Uses a combination of techniques to ensure good bit distribution across all 64 bits
fn improved_hash(data: &[u8]) -> u64 {
    // Start with FNV-1a
    let mut hash = 0xcbf29ce484222325u64;
    for byte in data {
        hash ^= *byte as u64;
        hash = hash.wrapping_mul(0x100000001b3);
    }
    
    // Apply finalizer with better bit mixing
    // This is based on Austin Appleby's MurmurHash3 finalizer
    hash ^= hash >> 33;
    hash = hash.wrapping_mul(0xff51afd7ed558ccd);
    hash ^= hash >> 33;
    hash = hash.wrapping_mul(0xc4ceb9fe1a85ec53);
    hash ^= hash >> 33;
    
    hash
}

/// HyperLogLog data structure for cardinality estimation
#[derive(Clone, Debug)]
pub struct HyperLogLog {
    /// Number of registers (m = 2^precision)
    m: usize,
    /// Precision (number of bits used for register indexing, typically 4-16)
    precision: u8,
    /// Registers storing the maximum leading zeros
    registers: Vec<u8>,
    /// Alpha constant for bias correction
    alpha_m: f64,
}

impl HyperLogLog {
    /// Create a new HyperLogLog with specified precision
    ///
    /// # Arguments
    /// * `precision` - Number of bits for register indexing (4-16)
    ///   - precision 4: 16 registers, ~26% error
    ///   - precision 12: 4096 registers, ~1.6% error
    ///   - precision 16: 65536 registers, ~0.4% error
    ///
    /// # Errors
    /// Returns None if precision is outside the valid range [4, 16]
    ///
    /// # Example
    /// ```
    /// use hyperloglog_utils::HyperLogLog;
    ///
    /// let hll = HyperLogLog::new(12).unwrap();
    /// assert_eq!(hll.register_count(), 4096);
    /// ```
    pub fn new(precision: u8) -> Option<Self> {
        if precision < 4 || precision > 16 {
            return None;
        }

        let m = 1usize << precision;
        let alpha_m = match m {
            m if m >= 128 => {
                let m_f64 = m as f64;
                0.7213 / (1.0 + 1.079 / m_f64)
            }
            m if m == 16 => 0.673,
            m if m == 32 => 0.697,
            m if m == 64 => 0.709,
            _ => unreachable!(),
        };

        Some(HyperLogLog {
            m,
            precision,
            registers: vec![0; m],
            alpha_m,
        })
    }

    /// Create a new HyperLogLog with a target error rate
    ///
    /// # Arguments
    /// * `error_rate` - Desired error rate (e.g., 0.01 for 1% error)
    ///
    /// # Example
    /// ```
    /// use hyperloglog_utils::HyperLogLog;
    ///
    /// let hll = HyperLogLog::with_error_rate(0.01).unwrap();
    /// ```
    pub fn with_error_rate(error_rate: f64) -> Option<Self> {
        if error_rate <= 0.0 || error_rate > 1.0 {
            return None;
        }

        // Error ≈ 1.04 / sqrt(m), so m ≈ (1.04 / error)^2
        let m_approx = (1.04 / error_rate).powi(2);
        let precision = (m_approx.log2().ceil() as u8).clamp(4, 16);
        Self::new(precision)
    }

    /// Get the number of registers
    pub fn register_count(&self) -> usize {
        self.m
    }

    /// Get the precision
    pub fn precision(&self) -> u8 {
        self.precision
    }

    /// Insert a value into the HyperLogLog
    ///
    /// # Example
    /// ```
    /// use hyperloglog_utils::HyperLogLog;
    ///
    /// let mut hll = HyperLogLog::new(8).unwrap();
    /// hll.insert(b"hello");
    /// hll.insert(&42u64.to_be_bytes());
    /// ```
    pub fn insert(&mut self, data: &[u8]) {
        let hash = self.hash(data);
        self.insert_hash(hash);
    }

    /// Insert a hashable value into the HyperLogLog
    pub fn insert_hashable<T: Hash>(&mut self, value: &T) {
        let mut hasher = FnvHasher::new();
        value.hash(&mut hasher);
        let hash = hasher.finish();
        self.insert_hash(hash);
    }

    /// Insert a pre-computed hash value
    fn insert_hash(&mut self, hash: u64) {
        // Use the LAST (lowest) precision bits as register index
        let mask = (1u64 << self.precision) - 1;
        let index = (hash & mask) as usize;
        
        // Mask out index bits for remaining (bits [precision, 63])
        let remaining_mask = !mask;
        let remaining = hash & remaining_mask;
        
        // Count zeros in remaining (from bit 63)
        let zeros = Self::count_leading_zeros(remaining);
        
        // The rank is zeros + 1, capped at 64 - p + 1
        let max_rank = (64 - self.precision) as u32 + 1;
        let rank = ((zeros + 1).min(max_rank)) as u8;

        // Update register if new value is larger
        if rank > self.registers[index] {
            self.registers[index] = rank;
        }
    }

    /// Count leading zeros in a u64
    fn count_leading_zeros(mut value: u64) -> u32 {
        if value == 0 {
            return 64;
        }
        let mut count = 0u32;
        while (value & (1u64 << 63)) == 0 {
            value <<= 1;
            count += 1;
        }
        count
    }

    /// Hash a byte slice using improved hash function
    fn hash(&self, data: &[u8]) -> u64 {
        improved_hash(data)
    }

    /// Estimate the cardinality (number of unique elements)
    ///
    /// # Example
    /// ```
    /// use hyperloglog_utils::HyperLogLog;
    ///
    /// let mut hll = HyperLogLog::new(12).unwrap();
    /// for i in 0u64..10000 {
    ///     hll.insert(&i.to_be_bytes());
    /// }
    /// let count = hll.count();
    /// assert!(count > 9000 && count < 11000);
    /// ```
    pub fn count(&self) -> u64 {
        // Calculate harmonic mean
        let sum: f64 = self.registers.iter()
            .map(|&r| 2f64.powi(-(i32::from(r))))
            .sum();

        let estimate = self.alpha_m * (self.m as f64) * (self.m as f64) / sum;

        // Apply small range correction
        let empty_registers = self.registers.iter().filter(|&&r| r == 0).count();

        if estimate <= 2.5 * (self.m as f64) && empty_registers > 0 {
            // Linear counting for small cardinalities
            let empty_f64 = empty_registers as f64;
            let m_f64 = self.m as f64;
            (m_f64 * (m_f64 / empty_f64).ln()) as u64
        } else if estimate < (1u64 << 32) as f64 {
            estimate as u64
        } else {
            // Large range correction
            let two_32 = 2f64.powi(32);
            (-(two_32 * (1.0 - estimate / two_32).ln())) as u64
        }
    }

    /// Merge another HyperLogLog into this one
    ///
    /// Both HyperLogLogs must have the same precision.
    ///
    /// # Example
    /// ```
    /// use hyperloglog_utils::HyperLogLog;
    ///
    /// let mut hll1 = HyperLogLog::new(12).unwrap();
    /// let mut hll2 = HyperLogLog::new(12).unwrap();
    ///
    /// hll1.insert(b"a");
    /// hll1.insert(b"b");
    /// hll2.insert(b"b");
    /// hll2.insert(b"c");
    ///
    /// hll1.merge(&hll2).unwrap();
    /// // hll1 now contains a, b, c
    /// ```
    pub fn merge(&mut self, other: &HyperLogLog) -> Result<(), &'static str> {
        if self.precision != other.precision {
            return Err("Cannot merge HyperLogLogs with different precision");
        }

        for i in 0..self.m {
            self.registers[i] = self.registers[i].max(other.registers[i]);
        }

        Ok(())
    }

    /// Check if the HyperLogLog is empty (all registers are zero)
    pub fn is_empty(&self) -> bool {
        self.registers.iter().all(|&r| r == 0)
    }

    /// Clear all registers
    pub fn clear(&mut self) {
        self.registers.fill(0);
    }

    /// Serialize the HyperLogLog to bytes
    ///
    /// Format: [precision: 1 byte] [registers: m bytes]
    pub fn to_bytes(&self) -> Vec<u8> {
        let mut bytes = Vec::with_capacity(1 + self.m);
        bytes.push(self.precision);
        bytes.extend_from_slice(&self.registers);
        bytes
    }

    /// Deserialize a HyperLogLog from bytes
    pub fn from_bytes(bytes: &[u8]) -> Result<HyperLogLog, &'static str> {
        if bytes.is_empty() {
            return Err("Empty bytes");
        }

        let precision = bytes[0];
        let hll = HyperLogLog::new(precision)
            .ok_or("Invalid precision")?;

        if bytes.len() != 1 + hll.m {
            return Err("Invalid byte length");
        }

        let mut hll = hll;
        hll.registers.copy_from_slice(&bytes[1..]);

        Ok(hll)
    }

    /// Get the raw registers (for advanced use)
    pub fn registers(&self) -> &[u8] {
        &self.registers
    }

    /// Get mutable access to registers (for advanced use)
    pub fn registers_mut(&mut self) -> &mut [u8] {
        &mut self.registers
    }
}

impl Default for HyperLogLog {
    fn default() -> Self {
        Self::new(12).expect("Default precision should be valid")
    }
}

/// Sparse HyperLogLog for memory-efficient small cardinality estimation
///
/// Uses a hash map for sparse representation when cardinality is small,
/// switching to dense representation when needed.
#[derive(Clone, Debug)]
pub struct SparseHyperLogLog {
    /// Dense HyperLogLog (used when cardinality grows)
    dense: Option<HyperLogLog>,
    /// Sparse representation: hash -> leading zeros
    sparse: std::collections::HashMap<u32, u8>,
    /// Precision
    precision: u8,
    /// Maximum sparse size before switching to dense
    max_sparse_size: usize,
}

impl SparseHyperLogLog {
    /// Create a new sparse HyperLogLog
    pub fn new(precision: u8) -> Option<Self> {
        if precision < 4 || precision > 16 {
            return None;
        }
        Some(SparseHyperLogLog {
            dense: None,
            sparse: std::collections::HashMap::new(),
            precision,
            max_sparse_size: 256,
        })
    }

    /// Insert a value
    pub fn insert(&mut self, data: &[u8]) {
        if let Some(ref mut hll) = self.dense {
            hll.insert(data);
            return;
        }

        // Hash and extract index using improved hash
        let hash = improved_hash(data);
        let mask = (1u64 << self.precision) - 1;
        let index = (hash & mask) as u32;
        
        // Mask out index bits for remaining
        let remaining_mask = !mask;
        let remaining = hash & remaining_mask;
        
        // Count zeros in remaining (from bit 63)
        let zeros = HyperLogLog::count_leading_zeros(remaining);
        
        // The rank is zeros + 1, capped at 64 - p + 1
        let max_rank = (64 - self.precision) as u32 + 1;
        let rank = ((zeros + 1).min(max_rank)) as u8;

        self.sparse
            .entry(index)
            .and_modify(|v| *v = (*v).max(rank))
            .or_insert(rank);

        // Switch to dense if sparse gets too large
        if self.sparse.len() > self.max_sparse_size {
            self.convert_to_dense();
        }
    }

    /// Convert sparse representation to dense
    fn convert_to_dense(&mut self) {
        let mut hll = HyperLogLog::new(self.precision).unwrap();
        for (&index, &zeros) in &self.sparse {
            hll.registers[index as usize] = zeros;
        }
        self.dense = Some(hll);
        self.sparse.clear();
    }

    /// Estimate cardinality
    pub fn count(&self) -> u64 {
        if let Some(ref hll) = self.dense {
            hll.count()
        } else {
            self.sparse.len() as u64
        }
    }

    /// Merge another sparse HyperLogLog
    pub fn merge(&mut self, other: &SparseHyperLogLog) -> Result<(), &'static str> {
        if self.precision != other.precision {
            return Err("Cannot merge HyperLogLogs with different precision");
        }

        // Ensure both are in the same representation
        if self.dense.is_none() && other.dense.is_some() {
            self.convert_to_dense();
        }

        match (&mut self.dense, &other.dense) {
            (Some(ref mut hll), Some(ref other_hll)) => {
                hll.merge(other_hll)
            }
            (None, None) => {
                for (&index, &zeros) in &other.sparse {
                    self.sparse
                        .entry(index)
                        .and_modify(|v| *v = (*v).max(zeros))
                        .or_insert(zeros);
                }
                if self.sparse.len() > self.max_sparse_size {
                    self.convert_to_dense();
                }
                Ok(())
            }
            (Some(ref mut hll), None) => {
                // Dense + sparse: insert sparse into dense
                for (&index, &zeros) in &other.sparse {
                    if hll.registers[index as usize] < zeros {
                        hll.registers[index as usize] = zeros;
                    }
                }
                Ok(())
            }
            (None, Some(_)) => {
                // Self is sparse, other is dense - convert self to dense first
                self.convert_to_dense();
                if let Some(ref mut self_hll) = self.dense {
                    if let Some(ref other_hll) = other.dense {
                        return self_hll.merge(other_hll);
                    }
                }
                Ok(())
            }
        }
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_new_valid_precision() {
        for p in 4..=16 {
            let hll = HyperLogLog::new(p);
            assert!(hll.is_some());
            let hll = hll.unwrap();
            assert_eq!(hll.precision(), p);
            assert_eq!(hll.register_count(), 1 << p);
        }
    }

    #[test]
    fn test_new_invalid_precision() {
        assert!(HyperLogLog::new(0).is_none());
        assert!(HyperLogLog::new(3).is_none());
        assert!(HyperLogLog::new(17).is_none());
        assert!(HyperLogLog::new(255).is_none());
    }

    #[test]
    fn test_empty() {
        let hll = HyperLogLog::new(12).unwrap();
        assert!(hll.is_empty());
        assert_eq!(hll.count(), 0);
    }

    #[test]
    fn test_single_insert() {
        let mut hll = HyperLogLog::new(12).unwrap();
        hll.insert(b"test");
        assert!(!hll.is_empty());
        assert!(hll.count() >= 1);
    }

    #[test]
    fn test_duplicates() {
        let mut hll = HyperLogLog::new(12).unwrap();
        for _ in 0..100 {
            hll.insert(b"duplicate");
        }
        // Should estimate close to 1
        let count = hll.count();
        assert!(count >= 1 && count <= 3, "Expected ~1, got {}", count);
    }

    #[test]
    fn test_cardinality_small() {
        let mut hll = HyperLogLog::new(12).unwrap();
        let n = 100u64;
        for i in 0u64..n {
            hll.insert(&i.to_be_bytes());
        }
        let count = hll.count();
        let error = ((count as f64 - n as f64).abs() / n as f64) * 100.0;
        assert!(error < 20.0, "Error too high: {}%", error);
    }

    #[test]
    fn test_cardinality_medium() {
        let mut hll = HyperLogLog::new(12).unwrap();
        let n = 10000u64;
        for i in 0u64..n {
            hll.insert(&i.to_be_bytes());
        }
        let count = hll.count();
        let error = ((count as f64 - n as f64).abs() / n as f64) * 100.0;
        assert!(error < 10.0, "Error too high: {}%", error);
    }

    #[test]
    fn test_cardinality_large() {
        let mut hll = HyperLogLog::new(14).unwrap();
        let n = 100000u64;
        for i in 0u64..n {
            hll.insert(&i.to_be_bytes());
        }
        let count = hll.count();
        let error = ((count as f64 - n as f64).abs() / n as f64) * 100.0;
        assert!(error < 5.0, "Error too high: {}%", error);
    }

    #[test]
    fn test_merge() {
        let mut hll1 = HyperLogLog::new(12).unwrap();
        let mut hll2 = HyperLogLog::new(12).unwrap();

        for i in 0u64..500 {
            hll1.insert(&i.to_be_bytes());
        }
        for i in 500u64..1000 {
            hll2.insert(&i.to_be_bytes());
        }

        hll1.merge(&hll2).unwrap();

        let count = hll1.count();
        let error = ((count as f64 - 1000.0).abs() / 1000.0) * 100.0;
        assert!(error < 10.0, "Error after merge too high: {}%", error);
    }

    #[test]
    fn test_merge_different_precision() {
        let mut hll1 = HyperLogLog::new(12).unwrap();
        let hll2 = HyperLogLog::new(10).unwrap();
        assert!(hll1.merge(&hll2).is_err());
    }

    #[test]
    fn test_clear() {
        let mut hll = HyperLogLog::new(12).unwrap();
        for i in 0u64..100 {
            hll.insert(&i.to_be_bytes());
        }
        assert!(!hll.is_empty());
        hll.clear();
        assert!(hll.is_empty());
    }

    #[test]
    fn test_serialization() {
        let mut hll1 = HyperLogLog::new(12).unwrap();
        for i in 0u64..1000 {
            hll1.insert(&i.to_be_bytes());
        }

        let bytes = hll1.to_bytes();
        let hll2 = HyperLogLog::from_bytes(&bytes).unwrap();

        assert_eq!(hll1.precision(), hll2.precision());
        assert_eq!(hll1.count(), hll2.count());
    }

    #[test]
    fn test_with_error_rate() {
        let hll = HyperLogLog::with_error_rate(0.01).unwrap();
        assert!(hll.precision() >= 12);

        let hll = HyperLogLog::with_error_rate(0.1).unwrap();
        assert!(hll.precision() >= 6);
    }

    #[test]
    fn test_insert_hashable() {
        let mut hll = HyperLogLog::new(12).unwrap();
        hll.insert_hashable(&42);
        hll.insert_hashable(&"hello");
        hll.insert_hashable(&42); // duplicate
        assert!(hll.count() >= 2);
    }

    #[test]
    fn test_sparse_hyperloglog() {
        let mut hll = SparseHyperLogLog::new(12).unwrap();
        for i in 0u64..100 {
            hll.insert(&i.to_be_bytes());
        }
        let count = hll.count();
        assert!(count >= 80 && count <= 120, "Expected ~100, got {}", count);
    }

    #[test]
    fn test_sparse_merge() {
        let mut hll1 = SparseHyperLogLog::new(12).unwrap();
        let mut hll2 = SparseHyperLogLog::new(12).unwrap();

        for i in 0u64..50 {
            hll1.insert(&i.to_be_bytes());
        }
        for i in 50u64..100 {
            hll2.insert(&i.to_be_bytes());
        }

        hll1.merge(&hll2).unwrap();
        let count = hll1.count();
        assert!(count >= 80 && count <= 120, "Expected ~100, got {}", count);
    }
}