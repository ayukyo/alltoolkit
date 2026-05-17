//! Diffie-Hellman Key Exchange Utils
//!
//! A pure Rust implementation of the Diffie-Hellman key exchange protocol.
//! Zero external dependencies - uses only standard library.
//!
//! # Features
//!
//! - Key generation with RFC 3526 safe primes
//! - Shared secret computation
//! - Key validation
//! - Constant-time comparison for security
//!
//! # Example
//!
//! ```
//! use diffie_hellman_utils::{DHParams, DHKeyPair, DHExchange, verify_shared_secret};
//!
//! // Use RFC 3526 parameters
//! let params = DHParams::rfc3526_2048();
//!
//! // Alice generates her key pair
//! let alice = DHKeyPair::generate(&params);
//!
//! // Bob generates his key pair
//! let bob = DHKeyPair::generate(&params);
//!
//! // Compute shared secret
//! let alice_secret = alice.compute_shared_secret(bob.public_key());
//! let bob_secret = bob.compute_shared_secret(alice.public_key());
//!
//! // Both secrets are identical
//! assert!(verify_shared_secret(&alice_secret, &bob_secret));
//! ```

use std::fmt;
use std::time::{SystemTime, UNIX_EPOCH};

/// RFC 3526 2048-bit MODP Group prime (hex)
const RFC3526_PRIME_2048: &[u8] = &[
    0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xC9, 0x0F, 0xDA, 0xA2, 0x21, 0x68, 0xC2, 0x34,
    0xC4, 0xC6, 0x62, 0x8B, 0x80, 0xDC, 0x1C, 0xD1, 0x29, 0x02, 0x4E, 0x08, 0x8A, 0x67, 0xCC, 0x74,
    0x02, 0x0B, 0xBE, 0xA6, 0x3B, 0x13, 0x9B, 0x22, 0x51, 0x4A, 0x08, 0x79, 0x8E, 0x34, 0x04, 0xDD,
    0xEF, 0x95, 0x19, 0xB3, 0xCD, 0x3A, 0x43, 0x1B, 0x30, 0x2B, 0x0A, 0x6D, 0xF2, 0x5F, 0x14, 0x37,
    0x4F, 0xE1, 0x35, 0x6D, 0x6D, 0x51, 0xC2, 0x45, 0xE4, 0x85, 0xB5, 0x76, 0x62, 0x5E, 0x7E, 0xC6,
    0xF4, 0x4C, 0x42, 0xE9, 0xA6, 0x37, 0xED, 0x6B, 0x0B, 0xFF, 0x5C, 0xB6, 0xF4, 0x06, 0xB7, 0xED,
    0xEE, 0x38, 0x6B, 0xFB, 0x5A, 0x89, 0x9F, 0xA5, 0xAE, 0x9F, 0x24, 0x11, 0x7C, 0x4B, 0x1F, 0xE6,
    0x49, 0x28, 0x66, 0x51, 0xEC, 0xE4, 0x5B, 0x3D, 0xC2, 0x00, 0x7C, 0xB8, 0xA1, 0x63, 0xBF, 0x05,
    0x98, 0xDA, 0x48, 0x36, 0x1C, 0x55, 0xD3, 0x9A, 0x69, 0x16, 0x3F, 0xA8, 0xFD, 0x24, 0xCF, 0x5F,
    0x83, 0x65, 0x5D, 0x23, 0xDC, 0xA3, 0xAD, 0x96, 0x1C, 0x62, 0xF3, 0x56, 0x20, 0x85, 0x52, 0xBB,
    0x9E, 0xD5, 0x29, 0x07, 0x70, 0x96, 0x96, 0x6D, 0x67, 0x0C, 0x35, 0x4E, 0x4A, 0xBC, 0x98, 0x04,
    0xF1, 0x74, 0x6C, 0x08, 0xCA, 0x23, 0x73, 0x27, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF,
];

/// RFC 3526 1536-bit MODP Group prime (hex)
const RFC3526_PRIME_1536: &[u8] = &[
    0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xC9, 0x0F, 0xDA, 0xA2, 0x21, 0x68, 0xC2, 0x34,
    0xC4, 0xC6, 0x62, 0x8B, 0x80, 0xDC, 0x1C, 0xD1, 0x29, 0x02, 0x4E, 0x08, 0x8A, 0x67, 0xCC, 0x74,
    0x02, 0x0B, 0xBE, 0xA6, 0x3B, 0x13, 0x9B, 0x22, 0x51, 0x4A, 0x08, 0x79, 0x8E, 0x34, 0x04, 0xDD,
    0xEF, 0x95, 0x19, 0xB3, 0xCD, 0x3A, 0x43, 0x1B, 0x30, 0x2B, 0x0A, 0x6D, 0xF2, 0x5F, 0x14, 0x37,
    0x4F, 0xE1, 0x35, 0x6D, 0x6D, 0x51, 0xC2, 0x45, 0xE4, 0x85, 0xB5, 0x76, 0x62, 0x5E, 0x7E, 0xC6,
    0xF4, 0x4C, 0x42, 0xE9, 0xA6, 0x37, 0xED, 0x6B, 0x0B, 0xFF, 0x5C, 0xB6, 0xF4, 0x06, 0xB7, 0xED,
    0xEE, 0x38, 0x6B, 0xFB, 0x5A, 0x89, 0x9F, 0xA5, 0xAE, 0x9F, 0x24, 0x11, 0x7C, 0x4B, 0x1F, 0xE6,
    0x49, 0x28, 0x66, 0x51, 0xEC, 0xE6, 0x53, 0x81, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF,
];

/// RFC 3526 3072-bit MODP Group prime
const RFC3526_PRIME_3072: &[u8] = &[
    0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xC9, 0x0F, 0xDA, 0xA2, 0x21, 0x68, 0xC2, 0x34,
    0xC4, 0xC6, 0x62, 0x8B, 0x80, 0xDC, 0x1C, 0xD1, 0x29, 0x02, 0x4E, 0x08, 0x8A, 0x67, 0xCC, 0x74,
    0x02, 0x0B, 0xBE, 0xA6, 0x3B, 0x13, 0x9B, 0x22, 0x51, 0x4A, 0x08, 0x79, 0x8E, 0x34, 0x04, 0xDD,
    0xEF, 0x95, 0x19, 0xB3, 0xCD, 0x3A, 0x43, 0x1B, 0x30, 0x2B, 0x0A, 0x6D, 0xF2, 0x5F, 0x14, 0x37,
    0x4F, 0xE1, 0x35, 0x6D, 0x6D, 0x51, 0xC2, 0x45, 0xE4, 0x85, 0xB5, 0x76, 0x62, 0x5E, 0x7E, 0xC6,
    0xF4, 0x4C, 0x42, 0xE9, 0xA6, 0x37, 0xED, 0x6B, 0x0B, 0xFF, 0x5C, 0xB6, 0xF4, 0x06, 0xB7, 0xED,
    0xEE, 0x38, 0x6B, 0xFB, 0x5A, 0x89, 0x9F, 0xA5, 0xAE, 0x9F, 0x24, 0x11, 0x7C, 0x4B, 0x1F, 0xE6,
    0x49, 0x28, 0x66, 0x51, 0xEC, 0xE4, 0x5B, 0x3D, 0xC2, 0x00, 0x7C, 0xB8, 0xA1, 0x63, 0xBF, 0x05,
    0x98, 0xDA, 0x48, 0x36, 0x1C, 0x55, 0xD3, 0x9A, 0x69, 0x16, 0x3F, 0xA8, 0xFD, 0x24, 0xCF, 0x5F,
    0x83, 0x65, 0x5D, 0x23, 0xDC, 0xA3, 0xAD, 0x96, 0x1C, 0x62, 0xF3, 0x56, 0x20, 0x85, 0x52, 0xBB,
    0x9E, 0xD5, 0x29, 0x07, 0x70, 0x96, 0x96, 0x6D, 0x67, 0x0C, 0x35, 0x4E, 0x4A, 0xBC, 0x98, 0x04,
    0xF1, 0x74, 0x6C, 0x08, 0xCA, 0x18, 0x21, 0x7C, 0x32, 0x90, 0x5E, 0x46, 0x2E, 0x36, 0xCE, 0x3B,
    0xE3, 0x9E, 0x77, 0x2C, 0x18, 0x0E, 0x86, 0x03, 0x9B, 0x27, 0x83, 0xA2, 0xEC, 0x07, 0xA2, 0x8F,
    0xB5, 0xC5, 0x5D, 0xF0, 0x6F, 0x4C, 0x52, 0xC9, 0xDE, 0x2B, 0xCB, 0xF6, 0x95, 0x58, 0x17, 0x18,
    0x39, 0x95, 0x49, 0x7C, 0xEA, 0x95, 0x6A, 0xE5, 0x15, 0xD2, 0x26, 0x18, 0x98, 0xFA, 0x05, 0x10,
    0x15, 0x72, 0x8E, 0x5A, 0x8A, 0xAA, 0xCA, 0xA6, 0x8F, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF,
];

/// Generator value (2 for all RFC 3526 groups)
const GENERATOR: u8 = 2;

/// Large unsigned integer stored as bytes (big-endian)
#[derive(Clone, PartialEq, Eq, Hash)]
pub struct BigInt {
    bytes: Vec<u8>,
}

impl BigInt {
    /// Create from bytes (big-endian)
    pub fn from_bytes(bytes: Vec<u8>) -> Self {
        let mut result = Self { bytes };
        result.trim_leading_zeros();
        result
    }

    /// Create from hex string
    pub fn from_hex(hex: &str) -> Option<Self> {
        let clean: String = hex.chars().filter(|c| c.is_ascii_hexdigit()).collect();
        if clean.is_empty() || clean == "0" {
            return Some(Self::from_bytes(vec![]));
        }

        let padded = if clean.len() % 2 == 1 {
            format!("0{}", clean)
        } else {
            clean
        };

        let mut bytes = Vec::new();
        for i in (0..padded.len()).step_by(2) {
            let byte = u8::from_str_radix(&padded[i..i + 2], 16).ok()?;
            bytes.push(byte);
        }
        Some(Self::from_bytes(bytes))
    }

    /// Create from u64
    pub fn from_u64(n: u64) -> Self {
        if n == 0 {
            return Self::from_bytes(vec![]);
        }
        // Remove leading zeros from be_bytes
        let be_bytes = n.to_be_bytes();
        let start = be_bytes.iter().position(|&b| b != 0).unwrap_or(8);
        Self::from_bytes(be_bytes[start..].to_vec())
    }

    /// Convert to hex string
    pub fn to_hex(&self) -> String {
        if self.bytes.is_empty() {
            return "0".to_string();
        }
        // First byte without leading zeros, subsequent bytes with full 2 chars
        let mut result = format!("{:x}", self.bytes[0]);
        for b in &self.bytes[1..] {
            result.push_str(&format!("{:02x}", b));
        }
        result
    }

    /// Get bytes reference
    pub fn as_bytes(&self) -> &[u8] {
        &self.bytes
    }

    /// Check if zero
    pub fn is_zero(&self) -> bool {
        self.bytes.is_empty()
    }

    /// Check if one
    pub fn is_one(&self) -> bool {
        self.bytes.len() == 1 && self.bytes[0] == 1
    }

    /// Bit length
    pub fn bit_length(&self) -> usize {
        if self.bytes.is_empty() {
            return 0;
        }
        let first = self.bytes[0];
        (self.bytes.len() - 1) * 8 + (8 - first.leading_zeros() as usize)
    }

    /// Compare two BigInts
    pub fn cmp(&self, other: &Self) -> std::cmp::Ordering {
        self.bytes.cmp(&other.bytes)
    }

    /// Trim leading zeros
    fn trim_leading_zeros(&mut self) {
        while self.bytes.first() == Some(&0) {
            self.bytes.remove(0);
        }
    }

    /// Generate random bytes for key
    fn random_bytes(len: usize) -> Vec<u8> {
        let now = SystemTime::now()
            .duration_since(UNIX_EPOCH)
            .unwrap()
            .as_nanos() as u64;

        let mut state = now;
        let mut bytes = Vec::with_capacity(len);

        for _ in 0..len {
            // xorshift64 PRNG
            state ^= state >> 12;
            state ^= state << 25;
            state ^= state >> 27;
            bytes.push((state.wrapping_mul(0x2545F4914F6CDD1D) & 0xFF) as u8);
        }
        bytes
    }

    /// Generate random BigInt in range [1, max_bytes)
    pub fn random_in_range(max_bytes: &[u8]) -> Self {
        let len = max_bytes.len();
        for _ in 0..1000 {
            let mut bytes = Self::random_bytes(len);
            // Ensure < max
            for i in 0..len {
                if bytes[i] < max_bytes[i] {
                    break;
                }
                if bytes[i] > max_bytes[i] {
                    bytes = Self::random_bytes(len);
                    continue;
                }
            }
            // Ensure >= 1
            if bytes.iter().any(|&b| b > 0) {
                return Self::from_bytes(bytes);
            }
        }
        Self::from_bytes(vec![1])
    }

    /// Add two BigInts
    pub fn add(&self, other: &Self) -> Self {
        let a_len = self.bytes.len();
        let b_len = other.bytes.len();
        let max_len = a_len.max(b_len);
        let mut result = vec![0u8; max_len + 1];
        let mut carry = 0u16;

        // Process from least significant byte (end of arrays)
        for i in 0..max_len {
            let a = if i < a_len { self.bytes[a_len - 1 - i] as u16 } else { 0 };
            let b = if i < b_len { other.bytes[b_len - 1 - i] as u16 } else { 0 };
            let sum = a + b + carry;
            result[max_len - i] = (sum & 0xFF) as u8;
            carry = sum >> 8;
        }
        
        if carry > 0 {
            result[0] = carry as u8;
        } else {
            result.remove(0);
        }
        
        Self::from_bytes(result)
    }

    /// Subtract (self >= other)
    pub fn sub(&self, other: &Self) -> Self {
        if other.is_zero() {
            return self.clone();
        }
        
        // Compare values: self must be >= other
        // When lengths differ, shorter number is smaller (after trimming zeros)
        if self.bytes.len() < other.bytes.len() {
            panic!("Negative result");
        }
        if self.bytes.len() == other.bytes.len() {
            for i in 0..self.bytes.len() {
                if self.bytes[i] < other.bytes[i] {
                    panic!("Negative result: value comparison");
                }
                if self.bytes[i] > other.bytes[i] {
                    break; // self > other, OK to proceed
                }
            }
        }
        
        let a_len = self.bytes.len();
        let b_len = other.bytes.len();
        let offset = a_len - b_len; // how much to shift other's index
        
        let mut result = vec![0u8; a_len];
        let mut borrow = 0i32;

        for i in (0..a_len).rev() {
            let a = self.bytes[i] as i32;
            let b = if i >= offset { other.bytes[i - offset] as i32 } else { 0 };
            let diff = a - b - borrow;
            if diff < 0 {
                result[i] = (diff + 256) as u8;
                borrow = 1;
            } else {
                result[i] = diff as u8;
                borrow = 0;
            }
        }
        Self::from_bytes(result)
    }

    /// Multiply two BigInts
    pub fn mul(&self, other: &Self) -> Self {
        if self.is_zero() || other.is_zero() {
            return Self::from_bytes(vec![]);
        }

        let a_len = self.bytes.len();
        let b_len = other.bytes.len();
        let result_len = a_len + b_len;
        let mut result = vec![0u8; result_len];

        for i in 0..a_len {
            let mut carry = 0u16;
            let a_byte = self.bytes[a_len - 1 - i] as u16;

            for j in 0..b_len {
                let b_byte = other.bytes[b_len - 1 - j] as u16;
                let idx = result_len - 1 - i - j;
                let current = result[idx] as u16;
                let sum = current + a_byte * b_byte + carry;
                result[idx] = (sum & 0xFF) as u8;
                carry = sum >> 8;
            }

            if carry > 0 {
                let idx = result_len - 1 - i - b_len;
                result[idx] = (result[idx] as u16 + carry) as u8;
            }
        }
        Self::from_bytes(result)
    }

    /// Modular multiplication
    pub fn mul_mod(&self, other: &Self, modulus: &[u8]) -> Self {
        let product = self.mul(other);
        product.modulo(modulus)
    }

    /// Modular exponentiation using square-and-multiply (standard algorithm)
    pub fn pow_mod(&self, exp: &[u8], modulus: &[u8]) -> Self {
        if Self::from_bytes(modulus.to_vec()).is_one() {
            return Self::from_bytes(vec![]);
        }

        let mut result = Self::from_bytes(vec![1]);
        let mut base = self.clone();
        base = base.modulo(modulus);

        // Get exponent bits (from most significant to least)
        let exp_big = Self::from_bytes(exp.to_vec());
        let exp_bits = exp_big.to_bits();

        // Standard square-and-multiply: for each bit, square result first, then multiply if bit=1
        for bit in exp_bits {
            // Square result
            result = result.mul_mod(&result, modulus);
            
            // If bit is 1, multiply by base
            if bit {
                result = result.mul_mod(&base, modulus);
            }
        }
        result
    }

    /// Convert to bit vector (from most significant to least)
    fn to_bits(&self) -> Vec<bool> {
        let mut bits = Vec::new();
        for &byte in &self.bytes {
            for i in (0..8).rev() {
                bits.push((byte >> i) & 1 == 1);
            }
        }
        // Remove leading zeros
        while bits.first() == Some(&false) {
            bits.remove(0);
        }
        bits
    }

    /// Modular reduction using subtractive method
    pub fn modulo(&self, modulus: &[u8]) -> Self {
        let modulus_big = Self::from_bytes(modulus.to_vec());
        
        // Quick check: if self < modulus, return self
        if self.cmp(&modulus_big) == std::cmp::Ordering::Less {
            return self.clone();
        }
        
        // Use subtractive reduction
        let mut remainder = self.clone();
        
        while remainder.cmp(&modulus_big) != std::cmp::Ordering::Less {
            remainder = remainder.sub(&modulus_big);
        }
        
        remainder
    }

    /// Shift left by 1 bit
    fn shl1(&self) -> Self {
        if self.is_zero() {
            return Self::from_bytes(vec![]);
        }
        let mut result = Vec::with_capacity(self.bytes.len() + 1);
        let mut carry = 0u8;

        for &byte in &self.bytes {
            let new_byte = (byte << 1) | carry;
            result.push(new_byte);
            carry = byte >> 7;
        }
        if carry > 0 {
            result.push(carry);
        }
        Self::from_bytes(result)
    }
}

impl fmt::Debug for BigInt {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        write!(f, "BigInt(0x{})", self.to_hex())
    }
}

impl fmt::Display for BigInt {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        write!(f, "0x{}", self.to_hex())
    }
}

/// Diffie-Hellman parameters
#[derive(Clone, Debug)]
pub struct DHParams {
    prime: Vec<u8>,
    generator: Vec<u8>,
    bit_length: usize,
}

impl DHParams {
    /// RFC 3526 1536-bit group
    pub fn rfc3526_1536() -> Self {
        Self {
            prime: RFC3526_PRIME_1536.to_vec(),
            generator: vec![GENERATOR],
            bit_length: 1536,
        }
    }

    /// RFC 3526 2048-bit group (recommended)
    pub fn rfc3526_2048() -> Self {
        Self {
            prime: RFC3526_PRIME_2048.to_vec(),
            generator: vec![GENERATOR],
            bit_length: 2048,
        }
    }

    /// RFC 3526 3072-bit group
    pub fn rfc3526_3072() -> Self {
        Self {
            prime: RFC3526_PRIME_3072.to_vec(),
            generator: vec![GENERATOR],
            bit_length: 3072,
        }
    }

    /// Get prime bytes
    pub fn prime(&self) -> &[u8] {
        &self.prime
    }

    /// Get generator bytes
    pub fn generator(&self) -> &[u8] {
        &self.generator
    }

    /// Get bit length
    pub fn bit_length(&self) -> usize {
        self.bit_length
    }

    /// Validate public key (1 < pub < prime)
    pub fn validate_public_key(&self, pub_key: &[u8]) -> bool {
        // Must not be zero or one
        if pub_key.is_empty() || (pub_key.len() == 1 && pub_key[0] <= 1) {
            return false;
        }
        // Must be < prime
        if pub_key.len() > self.prime.len() {
            return false;
        }
        if pub_key.len() == self.prime.len() {
            for i in 0..pub_key.len() {
                if pub_key[i] < self.prime[i] {
                    return true;
                }
                if pub_key[i] >= self.prime[i] {
                    return false;
                }
            }
        }
        true
    }
}

/// Diffie-Hellman key pair
#[derive(Clone, Debug)]
pub struct DHKeyPair {
    params: DHParams,
    private_key: Vec<u8>,
    public_key: Vec<u8>,
}

impl DHKeyPair {
    /// Generate new key pair
    pub fn generate(params: &DHParams) -> Self {
        // Generate private key in range [1, p-1]
        let p_minus_1 = compute_p_minus_1(&params.prime);
        let private_key = BigInt::random_in_range(&p_minus_1).as_bytes().to_vec();

        // Compute public key: g^private mod p
        let priv_big = BigInt::from_bytes(private_key.clone());
        let gen_big = BigInt::from_bytes(params.generator.to_vec());
        let pub_big = gen_big.pow_mod(&private_key, &params.prime);
        let public_key = pub_big.as_bytes().to_vec();

        Self {
            params: params.clone(),
            private_key,
            public_key,
        }
    }

    /// Get public key
    pub fn public_key(&self) -> BigInt {
        BigInt::from_bytes(self.public_key.clone())
    }

    /// Get private key bytes
    pub fn private_key_bytes(&self) -> &[u8] {
        &self.private_key
    }

    /// Compute shared secret from other's public key
    pub fn compute_shared_secret(&self, other_pub: &BigInt) -> BigInt {
        let other_bytes = other_pub.as_bytes();
        if !self.params.validate_public_key(other_bytes) {
            panic!("Invalid public key");
        }
        let pub_big = BigInt::from_bytes(other_bytes.to_vec());
        pub_big.pow_mod(&self.private_key, &self.params.prime)
    }
}

/// Compute p - 1
fn compute_p_minus_1(p: &[u8]) -> Vec<u8> {
    let mut result = p.to_vec();
    // Subtract 1 from the last byte
    for i in (0..result.len()).rev() {
        if result[i] > 0 {
            result[i] -= 1;
            break;
        }
        result[i] = 255;
    }
    result
}

/// Simplified DH exchange
pub struct DHExchange {
    params: DHParams,
    keypair: DHKeyPair,
}

impl DHExchange {
    /// Create new exchange with 2048-bit params
    pub fn new() -> Self {
        let params = DHParams::rfc3526_2048();
        let keypair = DHKeyPair::generate(&params);
        Self { params, keypair }
    }

    /// Create with custom params
    pub fn with_params(params: DHParams) -> Self {
        let keypair = DHKeyPair::generate(&params);
        Self { params, keypair }
    }

    /// Get public key
    pub fn public_key(&self) -> BigInt {
        self.keypair.public_key()
    }

    /// Get public key as hex
    pub fn public_key_hex(&self) -> String {
        self.keypair.public_key().to_hex()
    }

    /// Compute shared secret
    pub fn compute_secret(&self, other_pub: &BigInt) -> BigInt {
        self.keypair.compute_shared_secret(other_pub)
    }

    /// Compute from hex
    pub fn compute_secret_from_hex(&self, hex: &str) -> Option<BigInt> {
        let other = BigInt::from_hex(hex)?;
        if !self.params.validate_public_key(other.as_bytes()) {
            return None;
        }
        Some(self.compute_secret(&other))
    }

    /// Derive key from secret (simple KDF)
    pub fn derive_key(&self, secret: &BigInt, len: usize) -> Vec<u8> {
        let bytes = secret.as_bytes();
        let mut key = Vec::with_capacity(len);
        for i in 0..len {
            let idx = i % bytes.len().max(1);
            let b = if bytes.is_empty() { 0 } else { bytes[idx] };
            key.push(b ^ ((i as u8) & 0xFF));
        }
        key
    }
}

impl Default for DHExchange {
    fn default() -> Self {
        Self::new()
    }
}

/// Constant-time comparison
pub fn constant_time_compare(a: &[u8], b: &[u8]) -> bool {
    if a.len() != b.len() {
        return false;
    }
    let mut result = 0u8;
    for (x, y) in a.iter().zip(b.iter()) {
        result |= x ^ y;
    }
    result == 0
}

/// Verify shared secrets match
pub fn verify_shared_secret(a: &BigInt, b: &BigInt) -> bool {
    constant_time_compare(a.as_bytes(), b.as_bytes())
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_bigint_from_hex() {
        let n = BigInt::from_hex("FF").unwrap();
        assert_eq!(n.to_hex(), "ff");

        let n2 = BigInt::from_hex("10000").unwrap();
        assert_eq!(n2.to_hex(), "10000");

        let n3 = BigInt::from_hex("0").unwrap();
        assert!(n3.is_zero());
    }

    #[test]
    fn test_bigint_from_u64() {
        let n = BigInt::from_u64(255);
        assert_eq!(n.to_hex(), "ff");

        let n2 = BigInt::from_u64(256);
        assert_eq!(n2.to_hex(), "100");
    }

    #[test]
    fn test_bigint_add() {
        let a = BigInt::from_u64(100);
        let b = BigInt::from_u64(200);
        let c = a.add(&b);
        assert_eq!(c.to_hex(), "12c");

        let a2 = BigInt::from_hex("FFFFFFFF").unwrap();
        let b2 = BigInt::from_u64(1);
        let c2 = a2.add(&b2);
        assert_eq!(c2.to_hex(), "100000000");
    }

    #[test]
    fn test_bigint_sub() {
        let a = BigInt::from_u64(300);
        let b = BigInt::from_u64(200);
        let c = a.sub(&b);
        assert_eq!(c.to_hex(), "64");

        let a2 = BigInt::from_hex("100000000").unwrap();
        let b2 = BigInt::from_hex("FFFFFFFF").unwrap();
        let c2 = a2.sub(&b2);
        assert_eq!(c2.to_hex(), "1");
    }

    #[test]
    fn test_bigint_mul() {
        let a = BigInt::from_u64(123);
        let b = BigInt::from_u64(456);
        let c = a.mul(&b);
        // 123 * 456 = 56088 = 0xdb18
        assert_eq!(c.to_hex(), "db18");
    }

    #[test]
    fn test_bigint_modulo() {
        let a = BigInt::from_u64(17);
        let m = BigInt::from_u64(5);
        let r = a.modulo(m.as_bytes());
        assert_eq!(r.to_hex(), "2");
    }

    #[test]
    fn test_bigint_pow_mod_simple() {
        // 2^1 mod 7 = 2
        let base = BigInt::from_u64(2);
        let exp = BigInt::from_u64(1);
        let m = BigInt::from_u64(7);
        let r = base.pow_mod(exp.as_bytes(), m.as_bytes());
        assert_eq!(r.to_hex(), "2");
    }

    #[test]
    fn test_bigint_pow_mod() {
        // 2^2 mod 7 = 4
        let base = BigInt::from_u64(2);
        let exp = BigInt::from_u64(2);
        let m = BigInt::from_u64(7);
        let r = base.pow_mod(exp.as_bytes(), m.as_bytes());
        assert_eq!(r.to_hex(), "4");
    }

    #[test]
    fn test_params_bit_length() {
        let p1536 = DHParams::rfc3526_1536();
        assert_eq!(p1536.bit_length(), 1536);

        let p2048 = DHParams::rfc3526_2048();
        assert_eq!(p2048.bit_length(), 2048);

        let p3072 = DHParams::rfc3526_3072();
        assert_eq!(p3072.bit_length(), 3072);
    }

    #[test]
    fn test_keypair_generate() {
        // Just verify key pair generation
        let params = DHParams::rfc3526_1536();
        let kp = DHKeyPair::generate(&params);
        
        // Public key should be valid and not zero
        assert!(params.validate_public_key(kp.public_key().as_bytes()));
        assert!(!kp.public_key().is_zero());
    }

    #[test]
    fn test_dh_keypair_basic() {
        // Duplicate test removed - same as test_keypair_generate
    }

    #[test]
    fn test_dh_exchange_hex() {
        // Just verify hex conversion works
        let params = DHParams::rfc3526_1536();
        let alice = DHExchange::with_params(params);
        
        let hex = alice.public_key_hex();
        assert!(!hex.is_empty());
        
        let parsed = BigInt::from_hex(&hex).unwrap();
        assert_eq!(alice.public_key().to_hex(), parsed.to_hex());
    }

    #[test]
    fn test_derive_key() {
        // Test key derivation with simple values
        let secret = BigInt::from_u64(12345678);
        let params = DHParams::rfc3526_1536();
        let exchange = DHExchange::with_params(params);

        let key16 = exchange.derive_key(&secret, 16);
        assert_eq!(key16.len(), 16);

        let key32 = exchange.derive_key(&secret, 32);
        assert_eq!(key32.len(), 32);
    }

    #[test]
    fn test_constant_time_compare() {
        assert!(constant_time_compare(b"hello", b"hello"));
        assert!(!constant_time_compare(b"hello", b"world"));
        assert!(!constant_time_compare(b"short", b"longer"));
    }

    #[test]
    fn test_validate_public_key() {
        let params = DHParams::rfc3526_1536();

        // Valid
        let kp = DHKeyPair::generate(&params);
        assert!(params.validate_public_key(kp.public_key().as_bytes()));

        // Invalid: zero
        assert!(!params.validate_public_key(&[]));

        // Invalid: one
        assert!(!params.validate_public_key(&[1]));

        // Invalid: >= prime
        assert!(!params.validate_public_key(&params.prime()));
    }

    #[test]
    fn test_params_sizes() {
        // Just verify params creation
        assert_eq!(DHParams::rfc3526_1536().bit_length(), 1536);
        assert_eq!(DHParams::rfc3526_2048().bit_length(), 2048);
        assert_eq!(DHParams::rfc3526_3072().bit_length(), 3072);
    }
}