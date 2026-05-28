//! # Xorshift Random Number Generator Utilities
//!
//! A collection of fast, high-quality Xorshift PRNG implementations.
//! Zero external dependencies, suitable for games, simulations, and procedural generation.
//!
//! ## Features
//! - Multiple Xorshift variants (Xorshift32, Xorshift64, Xorshift128, Xorshift128+, Xorwow)
//! - Splittable64 for parallel computations
//! - Xoshiro256** for high-quality output
//! - Utility functions for common random operations
//!
//! ## Example
//! ```
//! use xorshift_utils::{Xorshift64, Rng};
//!
//! let mut rng = Xorshift64::new(42);
//! let n = rng.next_u64();
//! let bounded = rng.next_bounded(100);
//! ```

use std::time::{SystemTime, UNIX_EPOCH};

/// Trait for random number generators.
pub trait Rng {
    /// Returns the next random u64.
    fn next_u64(&mut self) -> u64;
    
    /// Returns the next random u32.
    fn next_u32(&mut self) -> u32 {
        self.next_u64() as u32
    }
    
    /// Returns a random f64 in [0.0, 1.0).
    fn next_f64(&mut self) -> f64 {
        (self.next_u64() >> 11) as f64 / (1u64 << 53) as f64
    }
    
    /// Returns a random f32 in [0.0, 1.0).
    fn next_f32(&mut self) -> f32 {
        (self.next_u32() >> 8) as f32 / (1u32 << 24) as f32
    }
    
    /// Returns a random integer in [0, bound).
    fn next_bounded(&mut self, bound: u64) -> u64 {
        if bound == 0 {
            return 0;
        }
        
        // Avoid modulo bias using rejection sampling
        let threshold = (u64::MAX - bound + 1) % bound;
        loop {
            let r = self.next_u64();
            if r >= threshold {
                return r % bound;
            }
        }
    }
    
    /// Returns a random integer in [min, max].
    fn next_range(&mut self, min: i64, max: i64) -> i64 {
        if min >= max {
            return min;
        }
        let range = (max - min + 1) as u64;
        min + self.next_bounded(range) as i64
    }
    
    /// Returns a random boolean.
    fn next_bool(&mut self) -> bool {
        self.next_u64() & 1 == 1
    }
    
    /// Fills a buffer with random bytes.
    fn fill_bytes(&mut self, buf: &mut [u8]) {
        for chunk in buf.chunks_mut(8) {
            let r = self.next_u64();
            for (i, byte) in chunk.iter_mut().enumerate() {
                *byte = (r >> (i * 8)) as u8;
            }
        }
    }
    
    /// Shuffles a slice in place using Fisher-Yates algorithm.
    fn shuffle<T>(&mut self, slice: &mut [T]) {
        for i in (1..slice.len()).rev() {
            let j = self.next_bounded((i + 1) as u64) as usize;
            slice.swap(i, j);
        }
    }
    
    /// Returns a random element from a slice, or None if empty.
    fn choose<'a, T>(&mut self, slice: &'a [T]) -> Option<&'a T> {
        if slice.is_empty() {
            None
        } else {
            Some(&slice[self.next_bounded(slice.len() as u64) as usize])
        }
    }
}

// ============================================================================
// Xorshift32
// ============================================================================

/// Xorshift32 PRNG.
///
/// Simple and fast 32-bit generator. Good for embedded systems.
/// Period: 2^32 - 1
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub struct Xorshift32 {
    state: u32,
}

impl Xorshift32 {
    /// Creates a new Xorshift32 with the given seed.
    /// 
    /// # Panics
    /// Panics if seed is 0.
    pub fn new(seed: u32) -> Self {
        assert_ne!(seed, 0, "Seed must not be 0");
        Self { state: seed }
    }
    
    /// Creates a new Xorshift32 seeded from system time.
    pub fn from_time() -> Self {
        let seed = SystemTime::now()
            .duration_since(UNIX_EPOCH)
            .map(|d| d.as_nanos() as u32)
            .unwrap_or(1);
        Self::new(if seed == 0 { 1 } else { seed })
    }
    
    /// Returns the next random u32.
    pub fn next_u32(&mut self) -> u32 {
        self.state ^= self.state << 13;
        self.state ^= self.state >> 17;
        self.state ^= self.state << 5;
        self.state
    }
    
    /// Returns a random f32 in [0.0, 1.0).
    pub fn next_f32(&mut self) -> f32 {
        (self.next_u32() >> 8) as f32 / (1u32 << 24) as f32
    }
    
    /// Returns a random integer in [0, bound).
    pub fn next_bounded(&mut self, bound: u32) -> u32 {
        if bound == 0 {
            return 0;
        }
        let threshold = (u32::MAX - bound + 1) % bound;
        loop {
            let r = self.next_u32();
            if r >= threshold {
                return r % bound;
            }
        }
    }
}

// ============================================================================
// Xorshift64
// ============================================================================

/// Xorshift64 PRNG.
///
/// Simple and fast 64-bit generator.
/// Period: 2^64 - 1
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub struct Xorshift64 {
    state: u64,
}

impl Xorshift64 {
    /// Creates a new Xorshift64 with the given seed.
    /// 
    /// # Panics
    /// Panics if seed is 0.
    pub fn new(seed: u64) -> Self {
        assert_ne!(seed, 0, "Seed must not be 0");
        Self { state: seed }
    }
    
    /// Creates a new Xorshift64 seeded from system time.
    pub fn from_time() -> Self {
        let seed = SystemTime::now()
            .duration_since(UNIX_EPOCH)
            .map(|d| d.as_nanos() as u64)
            .unwrap_or(1);
        Self::new(if seed == 0 { 1 } else { seed })
    }
    
    /// Returns the next random u64.
    pub fn next_u64(&mut self) -> u64 {
        self.state ^= self.state << 13;
        self.state ^= self.state >> 7;
        self.state ^= self.state << 17;
        self.state
    }
}

impl Rng for Xorshift64 {
    fn next_u64(&mut self) -> u64 {
        self.next_u64()
    }
}

// ============================================================================
// Xorshift128
// ============================================================================

/// Xorshift128 PRNG.
///
/// Uses 128 bits of state for longer period.
/// Period: 2^128 - 1
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub struct Xorshift128 {
    state: [u32; 4],
}

impl Xorshift128 {
    /// Creates a new Xorshift128 with the given seed.
    /// 
    /// # Panics
    /// Panics if all seed values are 0.
    pub fn new(seed: [u32; 4]) -> Self {
        assert!(seed.iter().any(|&x| x != 0), "At least one seed value must be non-zero");
        Self { state: seed }
    }
    
    /// Creates a new Xorshift128 from a single 64-bit seed.
    pub fn from_u64(seed: u64) -> Self {
        let s = seed;
        let state = [
            (s & 0xFFFFFFFF) as u32 | 1,
            ((s >> 32) & 0xFFFFFFFF) as u32 | 2,
            ((s.wrapping_mul(6364136223846793005) >> 32) & 0xFFFFFFFF) as u32 | 3,
            ((s.wrapping_mul(1442695040888963407) >> 32) & 0xFFFFFFFF) as u32 | 4,
        ];
        Self { state }
    }
    
    /// Creates a new Xorshift128 seeded from system time.
    pub fn from_time() -> Self {
        let seed = SystemTime::now()
            .duration_since(UNIX_EPOCH)
            .map(|d| d.as_nanos() as u64)
            .unwrap_or(1);
        Self::from_u64(seed)
    }
    
    /// Returns the next random u32.
    pub fn next_u32(&mut self) -> u32 {
        let t = self.state[3];
        let s = self.state[0];
        
        self.state[3] = self.state[2];
        self.state[2] = self.state[1];
        self.state[1] = s;
        
        let t = t ^ (t << 11) ^ (s ^ (s >> 8));
        self.state[0] = t;
        
        t
    }
    
    /// Returns the next random u64.
    pub fn next_u64(&mut self) -> u64 {
        ((self.next_u32() as u64) << 32) | (self.next_u32() as u64)
    }
}

impl Rng for Xorshift128 {
    fn next_u64(&mut self) -> u64 {
        self.next_u64()
    }
}

// ============================================================================
// Xorshift128+
// ============================================================================

/// Xorshift128+ PRNG.
///
/// Improved version of Xorshift128 with better statistical properties.
/// Used in many JavaScript engines and browsers.
/// Period: 2^128 - 1
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub struct Xorshift128Plus {
    state: [u64; 2],
}

impl Xorshift128Plus {
    /// Creates a new Xorshift128+ with the given seed.
    /// 
    /// # Panics
    /// Panics if all seed values are 0.
    pub fn new(seed: [u64; 2]) -> Self {
        assert!(seed.iter().any(|&x| x != 0), "At least one seed value must be non-zero");
        Self { state: seed }
    }
    
    /// Creates a new Xorshift128+ from a single seed.
    pub fn from_seed(seed: u64) -> Self {
        let mut s = seed;
        if s == 0 {
            s = 1;
        }
        // Use splitmix64 to expand seed
        let s1 = {
            let mut z = s.wrapping_add(0x9e3779b97f4a7c15);
            z = (z ^ (z >> 30)).wrapping_mul(0xbf58476d1ce4e5b9);
            z = (z ^ (z >> 27)).wrapping_mul(0x94d049bb133111eb);
            z ^ (z >> 31)
        };
        let s2 = {
            let mut z = s.wrapping_add(0x9e3779b97f4a7c15).wrapping_add(s1);
            z = (z ^ (z >> 30)).wrapping_mul(0xbf58476d1ce4e5b9);
            z = (z ^ (z >> 27)).wrapping_mul(0x94d049bb133111eb);
            z ^ (z >> 31)
        };
        Self::new([s1, s2])
    }
    
    /// Creates a new Xorshift128+ seeded from system time.
    pub fn from_time() -> Self {
        let seed = SystemTime::now()
            .duration_since(UNIX_EPOCH)
            .map(|d| d.as_nanos() as u64)
            .unwrap_or(1);
        Self::from_seed(seed)
    }
    
    /// Returns the next random u64.
    pub fn next_u64(&mut self) -> u64 {
        let mut s1 = self.state[0];
        let s0 = self.state[1];
        
        let result = s0.wrapping_add(s1);
        
        self.state[0] = s0;
        s1 ^= s1 << 23;
        self.state[1] = s1 ^ s0 ^ (s1 >> 17) ^ (s0 >> 26);
        
        result
    }
}

impl Rng for Xorshift128Plus {
    fn next_u64(&mut self) -> u64 {
        self.next_u64()
    }
}

// ============================================================================
// Xorwow
// ============================================================================

/// Xorwow PRNG.
///
/// Combines xorshift with a Weyl sequence.
/// Used in CUDA's default PRNG.
/// Period: 2^160 - 2^32
#[derive(Debug, Clone, Copy)]
pub struct Xorwow {
    state: [u32; 4],
    counter: u32,
}

impl Xorwow {
    /// Creates a new Xorwow with the given seed.
    /// 
    /// # Panics
    /// Panics if all seed values are 0.
    pub fn new(seed: [u32; 4]) -> Self {
        assert!(seed.iter().any(|&x| x != 0), "At least one seed value must be non-zero");
        Self { state: seed, counter: 0 }
    }
    
    /// Creates a new Xorwow from a single seed.
    pub fn from_seed(seed: u64) -> Self {
        let s = seed;
        let state = [
            ((s & 0xFFFFFFFF) as u32).max(1),
            (((s >> 32) & 0xFFFFFFFF) as u32).max(1),
            ((s.wrapping_mul(6364136223846793005) & 0xFFFFFFFF) as u32).max(1),
            ((s.wrapping_mul(1442695040888963407) & 0xFFFFFFFF) as u32).max(1),
        ];
        Self::new(state)
    }
    
    /// Creates a new Xorwow seeded from system time.
    pub fn from_time() -> Self {
        let seed = SystemTime::now()
            .duration_since(UNIX_EPOCH)
            .map(|d| d.as_nanos() as u64)
            .unwrap_or(1);
        Self::from_seed(seed)
    }
    
    /// Returns the next random u32.
    pub fn next_u32(&mut self) -> u32 {
        let mut t = self.state[3];
        
        self.state[3] = self.state[2];
        self.state[2] = self.state[1];
        self.state[1] = self.state[0];
        
        t ^= t >> 2;
        t ^= t << 1;
        t ^= self.state[0] ^ (self.state[0] << 4);
        
        self.state[0] = t;
        self.counter = self.counter.wrapping_add(362437);
        
        t.wrapping_add(self.counter)
    }
    
    /// Returns the next random u64.
    pub fn next_u64(&mut self) -> u64 {
        ((self.next_u32() as u64) << 32) | (self.next_u32() as u64)
    }
}

impl Rng for Xorwow {
    fn next_u64(&mut self) -> u64 {
        self.next_u64()
    }
}

// ============================================================================
// SplitMix64
// ============================================================================

/// SplitMix64 PRNG.
///
/// Designed for easy splitting of the state for parallel computations.
/// Often used to initialize other PRNGs.
/// Period: 2^64
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub struct SplitMix64 {
    state: u64,
}

impl SplitMix64 {
    /// Creates a new SplitMix64 with the given seed.
    pub fn new(seed: u64) -> Self {
        Self { state: seed }
    }
    
    /// Creates a new SplitMix64 seeded from system time.
    pub fn from_time() -> Self {
        let seed = SystemTime::now()
            .duration_since(UNIX_EPOCH)
            .map(|d| d.as_nanos() as u64)
            .unwrap_or(0);
        Self::new(seed)
    }
    
    /// Returns the next random u64.
    pub fn next_u64(&mut self) -> u64 {
        self.state = self.state.wrapping_add(0x9e3779b97f4a7c15);
        
        let mut z = self.state;
        z = (z ^ (z >> 30)).wrapping_mul(0xbf58476d1ce4e5b9);
        z = (z ^ (z >> 27)).wrapping_mul(0x94d049bb133111eb);
        z ^ (z >> 31)
    }
    
    /// Splits the generator, returning a new independent generator.
    pub fn split(&mut self) -> Self {
        Self::new(self.next_u64())
    }
}

impl Rng for SplitMix64 {
    fn next_u64(&mut self) -> u64 {
        self.next_u64()
    }
}

// ============================================================================
// Xoshiro256**
// ============================================================================

/// Xoshiro256** PRNG.
///
/// High-quality 256-bit state generator.
/// Has excellent statistical properties and is the recommended choice.
/// Period: 2^256 - 1
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub struct Xoshiro256StarStar {
    state: [u64; 4],
}

impl Xoshiro256StarStar {
    /// Creates a new Xoshiro256** with the given seed.
    /// 
    /// # Panics
    /// Panics if all seed values are 0.
    pub fn new(seed: [u64; 4]) -> Self {
        assert!(seed.iter().any(|&x| x != 0), "At least one seed value must be non-zero");
        Self { state: seed }
    }
    
    /// Creates a new Xoshiro256** from a single seed using SplitMix64.
    pub fn from_seed(seed: u64) -> Self {
        let mut splitmix = SplitMix64::new(seed);
        Self::new([
            splitmix.next_u64(),
            splitmix.next_u64(),
            splitmix.next_u64(),
            splitmix.next_u64(),
        ])
    }
    
    /// Creates a new Xoshiro256** seeded from system time.
    pub fn from_time() -> Self {
        let seed = SystemTime::now()
            .duration_since(UNIX_EPOCH)
            .map(|d| d.as_nanos() as u64)
            .unwrap_or(0);
        Self::from_seed(seed)
    }
    
    /// Returns the next random u64.
    pub fn next_u64(&mut self) -> u64 {
        let result = self.state[1]
            .wrapping_mul(5)
            .rotate_left(7)
            .wrapping_mul(9);
        
        let t = self.state[1] << 17;
        
        self.state[2] ^= self.state[0];
        self.state[3] ^= self.state[1];
        self.state[1] ^= self.state[2];
        self.state[0] ^= self.state[3];
        
        self.state[2] ^= t;
        self.state[3] = self.state[3].rotate_left(45);
        
        result
    }
    
    /// Jumps ahead by 2^128 steps.
    pub fn jump(&mut self) {
        const JUMP: [u64; 4] = [
            0x180ec6d33cfd0aba,
            0xd5a61266f0c9392c,
            0xa9582618e03fc9aa,
            0x39abdc4529b1661c,
        ];
        
        let mut s = [0u64; 4];
        
        for j in 0..4 {
            for b in 0..64 {
                if (JUMP[j] >> b) & 1 != 0 {
                    s[0] ^= self.state[0];
                    s[1] ^= self.state[1];
                    s[2] ^= self.state[2];
                    s[3] ^= self.state[3];
                }
                self.next_u64();
            }
        }
        
        self.state = s;
    }
}

impl Rng for Xoshiro256StarStar {
    fn next_u64(&mut self) -> u64 {
        self.next_u64()
    }
}

// ============================================================================
// Utility Functions
// ============================================================================

/// Generates a random u64 using a simple Xorshift algorithm.
/// Useful for one-off random numbers without creating a struct.
/// 
/// # Example
/// ```
/// let n = xorshift_utils::quick_u64(42);
/// ```
pub fn quick_u64(seed: u64) -> u64 {
    let mut state = if seed == 0 { 1 } else { seed };
    state ^= state << 13;
    state ^= state >> 7;
    state ^= state << 17;
    state
}

/// Generates a random f64 in [0.0, 1.0) using a simple algorithm.
pub fn quick_f64(seed: u64) -> f64 {
    (quick_u64(seed) >> 11) as f64 / (1u64 << 53) as f64
}

/// Generates a random integer in [min, max] using a simple algorithm.
pub fn quick_range(seed: u64, min: i64, max: i64) -> i64 {
    if min >= max {
        return min;
    }
    let range = (max - min + 1) as u64;
    min + (quick_u64(seed) % range) as i64
}

/// Generates a random alphanumeric string of the given length.
pub fn random_string(rng: &mut impl Rng, length: usize) -> String {
    const CHARSET: &[u8] = b"ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789";
    
    (0..length)
        .map(|_| CHARSET[rng.next_bounded(CHARSET.len() as u64) as usize] as char)
        .collect()
}

/// Generates a random UUID v4 (pseudo-random, not cryptographically secure).
pub fn random_uuid(rng: &mut impl Rng) -> String {
    let mut bytes = [0u8; 16];
    rng.fill_bytes(&mut bytes);
    
    // Set version to 4 (random)
    bytes[6] = (bytes[6] & 0x0F) | 0x40;
    // Set variant to RFC 4122
    bytes[8] = (bytes[8] & 0x3F) | 0x80;
    
    format!(
        "{:02x}{:02x}{:02x}{:02x}-{:02x}{:02x}-{:02x}{:02x}-{:02x}{:02x}-{:02x}{:02x}{:02x}{:02x}{:02x}{:02x}",
        bytes[0], bytes[1], bytes[2], bytes[3],
        bytes[4], bytes[5],
        bytes[6], bytes[7],
        bytes[8], bytes[9],
        bytes[10], bytes[11], bytes[12], bytes[13], bytes[14], bytes[15]
    )
}

/// Returns a weighted random choice.
/// 
/// # Arguments
/// * `rng` - Random number generator
/// * `weights` - Slice of weights (must not be empty, weights should be positive)
/// 
/// # Returns
/// Index of the chosen element
pub fn weighted_choice(rng: &mut impl Rng, weights: &[f64]) -> usize {
    assert!(!weights.is_empty(), "Weights must not be empty");
    
    let total: f64 = weights.iter().sum();
    let mut r = rng.next_f64() * total;
    
    for (i, &w) in weights.iter().enumerate() {
        r -= w;
        if r <= 0.0 {
            return i;
        }
    }
    
    weights.len() - 1
}

/// Returns a random Gaussian (normal) distributed value using Box-Muller transform.
/// 
/// # Arguments
/// * `rng` - Random number generator
/// * `mean` - Mean of the distribution
/// * `stddev` - Standard deviation of the distribution
pub fn gaussian(rng: &mut impl Rng, mean: f64, stddev: f64) -> f64 {
    let u1 = rng.next_f64();
    let u2 = rng.next_f64();
    
    let z0 = (-2.0 * u1.ln()).sqrt() * (2.0 * std::f64::consts::PI * u2).cos();
    
    mean + z0 * stddev
}

/// Returns a random integer from a Poisson distribution.
/// 
/// # Arguments
/// * `rng` - Random number generator
/// * `lambda` - Mean of the distribution (must be positive)
pub fn poisson(rng: &mut impl Rng, lambda: f64) -> u64 {
    assert!(lambda > 0.0, "Lambda must be positive");
    
    let l = (-lambda).exp();
    let mut k = 0u64;
    let mut p = 1.0;
    
    loop {
        p *= rng.next_f64();
        if p <= l {
            return k;
        }
        k += 1;
    }
}

/// Returns a random integer from a geometric distribution.
/// 
/// # Arguments
/// * `rng` - Random number generator
/// * `p` - Probability of success (0.0 < p <= 1.0)
pub fn geometric(rng: &mut impl Rng, p: f64) -> u64 {
    assert!(p > 0.0 && p <= 1.0, "Probability must be in (0, 1]");
    
    let u = rng.next_f64();
    ((1.0 - u).ln() / (1.0 - p).ln()).ceil() as u64
}

/// Returns a random integer from an exponential distribution.
/// 
/// # Arguments
/// * `rng` - Random number generator
/// * `lambda` - Rate parameter (must be positive)
pub fn exponential(rng: &mut impl Rng, lambda: f64) -> f64 {
    assert!(lambda > 0.0, "Lambda must be positive");
    (-rng.next_f64().ln()) / lambda
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_xorshift32() {
        let mut rng = Xorshift32::new(42);
        
        // Should produce consistent values
        let v1 = rng.next_u32();
        let v2 = rng.next_u32();
        assert_ne!(v1, v2);
        
        // Same seed should produce same sequence
        let mut rng2 = Xorshift32::new(42);
        assert_eq!(rng2.next_u32(), v1);
        
        // next_f32 should be in [0, 1)
        for _ in 0..100 {
            let f = rng.next_f32();
            assert!(f >= 0.0 && f < 1.0);
        }
    }

    #[test]
    fn test_xorshift64() {
        let mut rng = Xorshift64::new(42);
        
        let v1 = rng.next_u64();
        let v2 = rng.next_u64();
        assert_ne!(v1, v2);
        
        let mut rng2 = Xorshift64::new(42);
        assert_eq!(rng2.next_u64(), v1);
    }

    #[test]
    fn test_xorshift128() {
        let mut rng = Xorshift128::new([1, 2, 3, 4]);
        
        let v1 = rng.next_u64();
        let v2 = rng.next_u64();
        assert_ne!(v1, v2);
        
        // Test from_u64
        let mut rng3 = Xorshift128::from_u64(42);
        let mut rng4 = Xorshift128::from_u64(42);
        assert_eq!(rng3.next_u64(), rng4.next_u64());
    }

    #[test]
    fn test_xorshift128_plus() {
        let mut rng = Xorshift128Plus::new([1, 2]);
        
        let v1 = rng.next_u64();
        let v2 = rng.next_u64();
        assert_ne!(v1, v2);
        
        // Test from_seed
        let mut rng3 = Xorshift128Plus::from_seed(42);
        let mut rng4 = Xorshift128Plus::from_seed(42);
        assert_eq!(rng3.next_u64(), rng4.next_u64());
    }

    #[test]
    fn test_xorwow() {
        let mut rng = Xorwow::new([1, 2, 3, 4]);
        
        let v1 = rng.next_u64();
        let v2 = rng.next_u64();
        assert_ne!(v1, v2);
    }

    #[test]
    fn test_splitmix64() {
        let mut rng = SplitMix64::new(42);
        
        let v1 = rng.next_u64();
        let v2 = rng.next_u64();
        assert_ne!(v1, v2);
        
        // Test split
        let mut rng2 = SplitMix64::new(42);
        let mut child = rng2.split();
        let _v3 = rng2.next_u64(); // Parent stream continues
        
        // Child should produce different values
        let child_v = child.next_u64();
        assert_ne!(child_v, _v3); // Different streams
        
        let mut rng3 = SplitMix64::new(42);
        assert_eq!(rng3.next_u64(), v1);
    }

    #[test]
    fn test_xoshiro256_star_star() {
        let mut rng = Xoshiro256StarStar::new([1, 2, 3, 4]);
        
        let v1 = rng.next_u64();
        let v2 = rng.next_u64();
        assert_ne!(v1, v2);
        
        // Test from_seed
        let mut rng3 = Xoshiro256StarStar::from_seed(42);
        let mut rng4 = Xoshiro256StarStar::from_seed(42);
        assert_eq!(rng3.next_u64(), rng4.next_u64());
        
        // Test jump
        let mut rng5 = Xoshiro256StarStar::from_seed(42);
        rng5.jump();
        let jumped = rng5.next_u64();
        
        let mut rng6 = Xoshiro256StarStar::from_seed(42);
        let normal = rng6.next_u64();
        assert_ne!(jumped, normal); // Jumped state should be different
    }

    #[test]
    fn test_rng_trait() {
        let mut rng = Xorshift64::new(42);
        
        // Test next_bounded
        for _ in 0..100 {
            let v = rng.next_bounded(10);
            assert!(v < 10);
        }
        
        // Test next_range
        for _ in 0..100 {
            let v = rng.next_range(-5, 5);
            assert!(v >= -5 && v <= 5);
        }
        
        // Test next_bool
        let mut trues = 0;
        for _ in 0..1000 {
            if rng.next_bool() {
                trues += 1;
            }
        }
        // Should be roughly 50%
        assert!(trues > 400 && trues < 600);
        
        // Test fill_bytes
        let mut buf = [0u8; 16];
        rng.fill_bytes(&mut buf);
        assert!(buf.iter().any(|&b| b != 0));
    }

    #[test]
    fn test_shuffle() {
        let mut rng = Xorshift64::new(42);
        
        let mut arr = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10];
        let original = arr;
        rng.shuffle(&mut arr);
        
        // Should be a permutation
        let mut sorted = arr;
        sorted.sort();
        assert_eq!(sorted, original);
        
        // Should be different (with very high probability)
        assert_ne!(arr, original);
    }

    #[test]
    fn test_choose() {
        let mut rng = Xorshift64::new(42);
        
        let arr = [1, 2, 3, 4, 5];
        
        for _ in 0..100 {
            let choice = rng.choose(&arr);
            assert!(arr.contains(choice.unwrap()));
        }
        
        // Empty slice
        let empty: &[i32] = &[];
        assert!(rng.choose(empty).is_none());
    }

    #[test]
    fn test_quick_functions() {
        let v = quick_u64(42);
        assert_ne!(v, 0);
        
        let f = quick_f64(42);
        assert!(f >= 0.0 && f < 1.0);
        
        let r = quick_range(42, -10, 10);
        assert!(r >= -10 && r <= 10);
    }

    #[test]
    fn test_random_string() {
        let mut rng = Xorshift64::new(42);
        
        let s1 = random_string(&mut rng, 10);
        assert_eq!(s1.len(), 10);
        assert!(s1.chars().all(|c| c.is_ascii_alphanumeric()));
        
        let s2 = random_string(&mut rng, 20);
        assert_eq!(s2.len(), 20);
        
        let s3 = random_string(&mut rng, 0);
        assert_eq!(s3.len(), 0);
    }

    #[test]
    fn test_random_uuid() {
        let mut rng = Xorshift64::new(42);
        
        let uuid = random_uuid(&mut rng);
        
        // Should be valid UUID format
        assert_eq!(uuid.len(), 36);
        assert!(uuid.chars().nth(8).unwrap() == '-');
        assert!(uuid.chars().nth(13).unwrap() == '-');
        assert!(uuid.chars().nth(18).unwrap() == '-');
        assert!(uuid.chars().nth(23).unwrap() == '-');
        
        // Version should be 4
        assert!(uuid.chars().nth(14).unwrap() == '4');
        
        // Variant should be 8, 9, a, or b
        let variant_char = uuid.chars().nth(19).unwrap();
        assert!(matches!(variant_char, '8' | '9' | 'a' | 'b'));
    }

    #[test]
    fn test_weighted_choice() {
        let mut rng = Xorshift64::new(42);
        
        // All same weight
        let weights = [1.0, 1.0, 1.0, 1.0];
        let mut counts = [0; 4];
        for _ in 0..10000 {
            let choice = weighted_choice(&mut rng, &weights);
            counts[choice] += 1;
        }
        // Each should be roughly 25%
        for &c in &counts {
            assert!(c > 2000 && c < 3000);
        }
        
        // Weighted
        let weights = [0.1, 0.3, 0.6];
        let mut counts = [0; 3];
        for _ in 0..10000 {
            let choice = weighted_choice(&mut rng, &weights);
            counts[choice] += 1;
        }
        // Index 2 should have most hits
        assert!(counts[2] > counts[1]);
        assert!(counts[1] > counts[0]);
    }

    #[test]
    fn test_gaussian() {
        let mut rng = Xorshift64::new(42);
        
        // Generate many values and check mean and stddev
        let n = 10000;
        let mean = 50.0;
        let stddev = 10.0;
        
        let sum: f64 = (0..n).map(|_| gaussian(&mut rng, mean, stddev)).sum();
        let actual_mean = sum / n as f64;
        
        // Mean should be close to 50
        assert!((actual_mean - mean).abs() < 1.0);
    }

    #[test]
    fn test_poisson() {
        let mut rng = Xorshift64::new(42);
        
        let lambda = 5.0;
        let n = 10000;
        let sum: u64 = (0..n).map(|_| poisson(&mut rng, lambda)).sum();
        let actual_mean = sum as f64 / n as f64;
        
        // Mean should be close to lambda
        assert!((actual_mean - lambda).abs() < 0.5);
    }

    #[test]
    fn test_geometric() {
        let mut rng = Xorshift64::new(42);
        
        let p = 0.3;
        let n = 10000;
        let sum: u64 = (0..n).map(|_| geometric(&mut rng, p)).sum();
        let actual_mean = sum as f64 / n as f64;
        
        // Mean of geometric is 1/p
        let expected_mean = 1.0 / p;
        assert!((actual_mean - expected_mean).abs() < 0.5);
    }

    #[test]
    fn test_exponential() {
        let mut rng = Xorshift64::new(42);
        
        let lambda = 2.0;
        let n = 10000;
        let sum: f64 = (0..n).map(|_| exponential(&mut rng, lambda)).sum();
        let actual_mean = sum / n as f64;
        
        // Mean of exponential is 1/lambda
        let expected_mean = 1.0 / lambda;
        assert!((actual_mean - expected_mean).abs() < 0.1);
    }

    #[test]
    #[should_panic(expected = "Seed must not be 0")]
    fn test_xorshift32_zero_seed() {
        Xorshift32::new(0);
    }

    #[test]
    #[should_panic(expected = "Seed must not be 0")]
    fn test_xorshift64_zero_seed() {
        Xorshift64::new(0);
    }

    #[test]
    #[should_panic(expected = "At least one seed")]
    fn test_xorshift128_zero_seed() {
        Xorshift128::new([0, 0, 0, 0]);
    }

    #[test]
    #[should_panic(expected = "At least one seed")]
    fn test_xorshift128_plus_zero_seed() {
        Xorshift128Plus::new([0, 0]);
    }

    #[test]
    fn test_from_time() {
        // Should not panic
        let _ = Xorshift32::from_time();
        let _ = Xorshift64::from_time();
        let _ = Xorshift128::from_time();
        let _ = Xorshift128Plus::from_time();
        let _ = Xorwow::from_time();
        let _ = SplitMix64::from_time();
        let _ = Xoshiro256StarStar::from_time();
    }

    #[test]
    fn test_period_quality() {
        // Test that generators don't repeat early values
        let mut rng = Xorshift64::new(12345);
        let first = rng.next_u64();
        
        for _ in 0..1000000 {
            if rng.next_u64() == first {
                panic!("Period too short!");
            }
        }
    }

    #[test]
    fn test_no_zeroes() {
        // Some xorshift variants can produce 0, but shouldn't get stuck
        let mut rng = Xorshift64::new(1);
        let mut count_zero = 0;
        
        for _ in 0..10000 {
            if rng.next_u64() == 0 {
                count_zero += 1;
            }
        }
        
        // Zero is possible but shouldn't happen too often
        assert!(count_zero < 10);
    }
}