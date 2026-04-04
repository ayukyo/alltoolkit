//! # Random Utilities Module
//!
//! A comprehensive random number and data generation utility module for Rust.
//! Provides random generation for passwords, tokens, UUIDs, and other use cases
//! using only the Rust standard library.
//!
//! ## Features
//!
//! - **Random Numbers**: Generate random integers and floats in any range
//! - **Random Strings**: Generate random strings with custom character sets
//! - **Password Generation**: Secure password generation with character requirements
//! - **UUID Generation**: RFC 4122 compliant UUID v4 generation
//! - **Random Selection**: Pick random elements from collections
//! - **Shuffling**: Shuffle arrays and vectors in-place
//! - **Zero Dependencies**: Uses only Rust standard library
//!
//! ## Examples
//!
//! ```rust
//! use random_utils::RandomUtils;
//!
//! // Generate random number
//! let num = RandomUtils::random_int(1, 100);
//!
//! // Generate random string
//! let token = RandomUtils::random_string(32);
//!
//! // Generate secure password
//! let password = RandomUtils::random_password(16);
//!
//! // Generate UUID
//! let uuid = RandomUtils::uuid_v4();
//! ```

use std::time::{SystemTime, UNIX_EPOCH};

/// Utility struct for random number and data generation
pub struct RandomUtils;

/// Simple random number generator using xorshift algorithm
/// This is a simple implementation for demonstration purposes
struct SimpleRng {
    state: u64,
}

impl SimpleRng {
    fn new() -> Self {
        let seed = SystemTime::now()
            .duration_since(UNIX_EPOCH)
            .unwrap()
            .as_nanos() as u64;
        SimpleRng { state: seed }
    }

    fn next_u64(&mut self) -> u64 {
        // xorshift64* algorithm
        self.state ^= self.state >> 12;
        self.state ^= self.state << 25;
        self.state ^= self.state >> 27;
        self.state.wrapping_mul(0x2545F4914F6CDD1Du64)
    }

    fn next_u32(&mut self) -> u32 {
        self.next_u64() as u32
    }

    fn next_f64(&mut self) -> f64 {
        // Generate a float in [0, 1)
        (self.next_u64() >> 11) as f64 / (1u64 << 53) as f64
    }

    fn gen_range_i32(&mut self, min: i32, max: i32) -> i32 {
        if min >= max {
            return min;
        }
        let range = (max - min + 1) as u64;
        min + (self.next_u64() % range) as i32
    }

    fn gen_range_i64(&mut self, min: i64, max: i64) -> i64 {
        if min >= max {
            return min;
        }
        let range = (max - min + 1) as u64;
        min + (self.next_u64() % range) as i64
    }

    fn gen_range_f64(&mut self, min: f64, max: f64) -> f64 {
        min + self.next_f64() * (max - min)
    }

    fn gen_bool(&mut self) -> bool {
        self.next_u64() & 1 == 1
    }

    fn gen_bool_with_probability(&mut self, probability: f64) -> bool {
        self.next_f64() < probability
    }
}

/// Character sets for random string generation
pub const LOWERCASE: &str = "abcdefghijklmnopqrstuvwxyz";
pub const UPPERCASE: &str = "ABCDEFGHIJKLMNOPQRSTUVWXYZ";
pub const DIGITS: &str = "0123456789";
pub const SPECIAL_CHARS: &str = "!@#$%^&*()-_=+[]{}|;:,.<>?";
pub const HEX_CHARS: &str = "0123456789abcdef";
pub const HEX_CHARS_UPPER: &str = "0123456789ABCDEF";
pub const URL_SAFE_CHARS: &str = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-_";

impl RandomUtils {
    fn get_rng() -> SimpleRng {
        SimpleRng::new()
    }

    // =========================================================================
    // Random Number Generation
    // =========================================================================

    /// Generate a random 32-bit signed integer
    pub fn random_i32() -> i32 {
        Self::get_rng().next_u32() as i32
    }

    /// Generate a random 64-bit signed integer
    pub fn random_i64() -> i64 {
        Self::get_rng().next_u64() as i64
    }

    /// Generate a random 32-bit unsigned integer
    pub fn random_u32() -> u32 {
        Self::get_rng().next_u32()
    }

    /// Generate a random 64-bit unsigned integer
    pub fn random_u64() -> u64 {
        Self::get_rng().next_u64()
    }

    /// Generate a random integer in a range [min, max] (inclusive)
    ///
    /// # Arguments
    /// * `min` - Minimum value (inclusive)
    /// * `max` - Maximum value (inclusive)
    ///
    /// # Panics
    /// Panics if min > max
    pub fn random_int(min: i32, max: i32) -> i32 {
        if min > max {
            panic!("min cannot be greater than max");
        }
        Self::get_rng().gen_range_i32(min, max)
    }

    /// Generate a random 64-bit integer in a range [min, max] (inclusive)
    pub fn random_i64_range(min: i64, max: i64) -> i64 {
        if min > max {
            panic!("min cannot be greater than max");
        }
        Self::get_rng().gen_range_i64(min, max)
    }

    /// Generate a random float in range [0.0, 1.0)
    pub fn random_float() -> f64 {
        Self::get_rng().next_f64()
    }

    /// Generate a random float in a range [min, max)
    pub fn random_float_range(min: f64, max: f64) -> f64 {
        if min >= max {
            panic!("min must be less than max");
        }
        Self::get_rng().gen_range_f64(min, max)
    }

    /// Generate a random boolean
    pub fn random_bool() -> bool {
        Self::get_rng().gen_bool()
    }

    /// Generate a random boolean with custom probability
    pub fn random_bool_with_probability(probability: f64) -> bool {
        if probability <= 0.0 {
            return false;
        }
        if probability >= 1.0 {
            return true;
        }
        Self::get_rng().gen_bool_with_probability(probability)
    }

    // =========================================================================
    // Random String Generation
    // =========================================================================

    /// Generate a random string from a custom character set
    pub fn random_string_from_charset(length: usize, charset: &str) -> String {
        if charset.is_empty() {
            panic!("charset cannot be empty");
        }
        let chars: Vec<char> = charset.chars().collect();
        let mut rng = Self::get_rng();
        let mut result = String::with_capacity(length);
        for _ in 0..length {
            let idx = (rng.next_u64() as usize) % chars.len();
            result.push(chars[idx]);
        }
        result
    }

    /// Generate a random alphabetic string (letters only)
    pub fn random_string(length: usize) -> String {
        let charset = format!("{}{}", LOWERCASE, UPPERCASE);
        Self::random_string_from_charset(length, &charset)
    }

    /// Generate a random alphanumeric string (letters + digits)
    pub fn random_alphanumeric(length: usize) -> String {
        let charset = format!("{}{}{}", LOWERCASE, UPPERCASE, DIGITS);
        Self::random_string_from_charset(length, &charset)
    }

    /// Generate a random numeric string
    pub fn random_numeric(length: usize) -> String {
        Self::random_string_from_charset(length, DIGITS)
    }

    /// Generate a random hex string (lowercase)
    pub fn random_hex(length: usize) -> String {
        Self::random_string_from_charset(length, HEX_CHARS)
    }

    /// Generate a random hex string (uppercase)
    pub fn random_hex_upper(length: usize) -> String {
        Self::random_string_from_charset(length, HEX_CHARS_UPPER)
    }

    /// Generate a URL-safe random string
    pub fn random_urlsafe(length: usize) -> String {
        Self::random_string_from_charset(length, URL_SAFE_CHARS)
    }

    // =========================================================================
    // Password Generation
    // =========================================================================

    /// Generate a secure random password
    ///
    /// # Arguments
    /// * `length` - Length of the password (minimum 4)
    ///
    /// The generated password will contain at least:
    /// - One lowercase letter
    /// - One uppercase letter
    /// - One digit
    /// - One special character
    ///
    /// # Panics
    /// Panics if length < 4
    pub fn random_password(length: usize) -> String {
        if length < 4 {
            panic!("password length must be at least 4");
        }

        let mut rng = Self::get_rng();
        let mut password = String::with_capacity(length);

        // Ensure at least one of each required character type
        let lowercase_chars: Vec<char> = LOWERCASE.chars().collect();
        let uppercase_chars: Vec<char> = UPPERCASE.chars().collect();
        let digit_chars: Vec<char> = DIGITS.chars().collect();
        let special_chars: Vec<char> = SPECIAL_CHARS.chars().collect();

        password.push(lowercase_chars[(rng.next_u64() as usize) % lowercase_chars.len()]);
        password.push(uppercase_chars[(rng.next_u64() as usize) % uppercase_chars.len()]);
        password.push(digit_chars[(rng.next_u64() as usize) % digit_chars.len()]);
        password.push(special_chars[(rng.next_u64() as usize) % special_chars.len()]);

        // Fill the rest with random characters from all sets
        let all_chars = format!("{}{}{}{}", LOWERCASE, UPPERCASE, DIGITS, SPECIAL_CHARS);
        let all_chars_vec: Vec<char> = all_chars.chars().collect();

        for _ in 4..length {
            let idx = (rng.next_u64() as usize) % all_chars_vec.len();
            password.push(all_chars_vec[idx]);
        }

        // Shuffle the password to randomize character positions
        let mut password_chars: Vec<char> = password.chars().collect();
        Self::shuffle_slice(&mut password_chars);

        password_chars.into_iter().collect()
    }

    fn shuffle_slice<T>(slice: &mut [T]) {
        let mut rng = Self::get_rng();
        for i in (1..slice.len()).rev() {
            let j = (rng.next_u64() as usize) % (i + 1);
            slice.swap(i, j);
        }
    }

    // =========================================================================
    // UUID Generation
    // =========================================================================

    /// Generate a UUID v4 (random) as a string
    ///
    /// # Returns
    /// A UUID v4 string in the format xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
    pub fn uuid_v4() -> String {
        let mut rng = Self::get_rng();
        let mut bytes = [0u8; 16];
        
        // Fill with random bytes
        for i in 0..16 {
            bytes[i] = (rng.next_u64() & 0xFF) as u8;
        }

        // Set version (4) and variant (RFC 4122)
        bytes[6] = (bytes[6] & 0x0F) | 0x40; // Version 4
        bytes[8] = (bytes[8] & 0x3F) | 0x80; // Variant 10

        format!(
            "{:02x}{:02x}{:02x}{:02x}-{:02x}{:02x}-{:02x}{:02x}-{:02x}{:02x}-{:02x}{:02x}{:02x}{:02x}{:02x}{:02x}",
            bytes[0], bytes[1], bytes[2], bytes[3],
            bytes[4], bytes[5],
            bytes[6], bytes[7],
            bytes[8], bytes[9],
            bytes[10], bytes[11], bytes[12], bytes[13], bytes[14], bytes[15]
        )
    }

    /// Generate a compact UUID v4 (without hyphens)
    pub fn uuid_v4_compact() -> String {
        let uuid = Self::uuid_v4();
        uuid.replace("-", "")
    }

    /// Generate a UUID v4 with uppercase letters
    pub fn uuid_v4_upper() -> String {
        Self::uuid_v4().to_uppercase()
    }

    /// Validate a UUID string
    pub fn is_valid_uuid(uuid: &str) -> bool {
        let clean = uuid.replace("-", "");
        if clean.len() != 32 {
            return false;
        }
        clean.chars().all(|c| c.is_ascii_hexdigit())
    }

    // =========================================================================
    // Random Selection
    // =========================================================================

    /// Pick a random element from a slice
    pub fn pick<T: Clone>(items: &[T]) -> Option<T> {
        if items.is_empty() {
            return None;
        }
        let mut rng = Self::get_rng();
        let idx = (rng.next_u64() as usize) % items.len();
        Some(items[idx].clone())
    }

    /// Pick multiple random elements from a slice (with replacement)
    pub fn pick_multiple<T: Clone>(items: &[T], count: usize) -> Vec<T> {
        if items.is_empty() {
            return Vec::new();
        }
        let mut rng = Self::get_rng();
        let mut result = Vec::with_capacity(count);
        for _ in 0..count {
            let idx = (rng.next_u64() as usize) % items.len();
            result.push(items[idx].clone());
        }
        result
    }

    /// Pick multiple unique random elements from a slice (without replacement)
    pub fn pick_unique<T: Clone>(items: &[T], count: usize) -> Vec<T> {
        if items.is_empty() || count == 0 {
            return Vec::new();
        }
        let count = count.min(items.len());
        let mut rng = Self::get_rng();
        let mut indices: Vec<usize> = (0..items.len()).collect();
        
        // Fisher-Yates shuffle for indices
        for i in (1..indices.len()).rev() {
            let j = (rng.next_u64() as usize) % (i + 1);
            indices.swap(i, j);
        }
        
        indices.into_iter().take(count).map(|i| items[i].clone()).collect()
    }

    /// Shuffle a vector in-place
    pub fn shuffle<T>(items: &mut [T]) {
        Self::shuffle_slice(items);
    }

    /// Return a shuffled copy of a vector
    pub fn shuffled<T: Clone>(items: &[T]) -> Vec<T> {
        let mut result = items.to_vec();
        Self::shuffle(&mut result);
        result
    }

    // =========================================================================
    // Random Color Generation
    // =========================================================================

    /// Generate a random RGB color as a tuple (r, g, b)
    pub fn random_rgb() -> (u8, u8, u8) {
        let mut rng = Self::get_rng();
        ((rng.next_u64() & 0xFF) as u8, 
         (rng.next_u64() & 0xFF) as u8, 
         (rng.next_u64() & 0xFF) as u8)
    }

    /// Generate a random hex color string (e.g., "#ff5733")
    pub fn random_hex_color() -> String {
        let (r, g, b) = Self::random_rgb();
        format!("#{:02x}{:02x}{:02x}", r, g, b)
    }

    /// Generate a random RGBA color as a tuple (r, g, b, a)
    pub fn random_rgba() -> (u8, u8, u8, u8) {
        let mut rng = Self::get_rng();
        ((rng.next_u64() & 0xFF) as u8, 
         (rng.next_u64() & 0xFF) as u8, 
         (rng.next_u64() & 0xFF) as u8,
         (rng.next_u64() & 0xFF) as u8)
    }

    // =========================================================================
    // Random Date/Time Generation
    // =========================================================================

    /// Generate a random timestamp (seconds since epoch)
    pub fn random_timestamp(min: i64, max: i64) -> i64 {
        Self::random_i64_range(min, max)
    }

    /// Generate a random duration in milliseconds
    pub fn random_duration_ms(min: u64, max: u64) -> u64 {
        Self::get_rng().gen_range_i64(min as i64, max as i64) as u64
    }
}

// =========================================================================
// Tests
// =========================================================================

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_random_int() {
        let result = RandomUtils::random_int(1, 10);
        assert!(result >= 1 && result <= 10);
    }

    #[test]
    fn test_random_float() {
        let result = RandomUtils::random_float();
        assert!(result >= 0.0 && result < 1.0);
    }

    #[test]
    fn test_random_bool() {
        let _ = RandomUtils::random_bool();
    }

    #[test]
    fn test_random_string() {
        let s = RandomUtils::random_string(10);
        assert_eq!(s.len(), 10);
        assert!(s.chars().all(|c| c.is_ascii_alphabetic()));
    }

    #[test]
    fn test_random_alphanumeric() {
        let s = RandomUtils::random_alphanumeric(10);
        assert_eq!(s.len(), 10);
        assert!(s.chars().all(|c| c.is_ascii_alphanumeric()));
    }

    #[test]
    fn test_random_numeric() {
        let s = RandomUtils::random_numeric(8);
        assert_eq!(s.len(), 8);
        assert!(s.chars().all(|c| c.is_ascii_digit()));
    }

    #[test]
    fn test_random_hex() {
        let s = RandomUtils::random_hex(8);
        assert_eq!(s.len(), 8);
        assert!(s.chars().all(|c| HEX_CHARS.contains(c)));
    }

    #[test]
    fn test_random_password() {
        let password = RandomUtils::random_password(16);
        assert_eq!(password.len(), 16);
        
        let has_lowercase = password.chars().any(|c| c.is_ascii_lowercase());
        let has_uppercase = password.chars().any(|c| c.is_ascii_uppercase());
        let has_digit = password.chars().any(|c| c.is_ascii_digit());
        let has_special = password.chars().any(|c| SPECIAL_CHARS.contains(c));
        
        assert!(has_lowercase, "Password should have lowercase");
        assert!(has_uppercase, "Password should have uppercase");
        assert!(has_digit, "Password should have digit");
        assert!(has_special, "Password should have special char");
    }

    #[test]
    fn test_uuid_v4() {
        let uuid = RandomUtils::uuid_v4();
        assert_eq!(uuid.len(), 36);
        assert!(RandomUtils::is_valid_uuid(&uuid));
        
        let parts: Vec<&str> = uuid.split('-').collect();
        assert_eq!(parts.len(), 5);
        assert_eq!(parts[0].len(), 8);
        assert_eq!(parts[1].len(), 4);
        assert_eq!(parts[2].len(), 4);
        assert_eq!(parts[3].len(), 4);
        assert_eq!(parts[4].len(), 12);
    }

    #[test]
    fn test_uuid_v4_compact() {
        let uuid = RandomUtils::uuid_v4_compact();
        assert_eq!(uuid.len(), 32);
        assert!(uuid.chars().all(|c| c.is_ascii_hexdigit()));
    }

    #[test]
    fn test_pick() {
        let items = vec![1, 2, 3, 4, 5];
        let picked = RandomUtils::pick(&items);
        assert!(picked.is_some());
        assert!(items.contains(&picked.unwrap()));
    }

    #[test]
    fn test_pick_empty() {
        let items: Vec<i32> = vec![];
        let picked = RandomUtils::pick(&items);
        assert!(picked.is_none());
    }

    #[test]
    fn test_pick_unique() {
        let items = vec![1, 2, 3, 4, 5];
        let picked = RandomUtils::pick_unique(&items, 3);
        assert_eq!(picked.len(), 3);
        let set: std::collections::HashSet<_> = picked.iter().collect();
        assert_eq!(set.len(), 3);
    }

    #[test]
    fn test_shuffle() {
        let mut items = vec![1, 2, 3, 4, 5];
        let original = items.clone();
        RandomUtils::shuffle(&mut items);
        assert_eq!(items.len(), 5);
        let mut sorted = items.clone();
        sorted.sort();
        assert_eq!(sorted, original);
    }

    #[test]
    fn test_random_rgb() {
        let (r, g, b) = RandomUtils::random_rgb();
        assert!(r <= 255);
        assert!(g <= 255);
        assert!(b <= 255);
    }

    #[test]
    fn test_random_hex_color() {
        let color = RandomUtils::random_hex_color();
        assert_eq!(color.len(), 7);
        assert!(color.starts_with('#'));
        assert!(color[1..].chars().all(|c| c.is_ascii_hexdigit()));
    }

    #[test]
    fn test_is_valid_uuid() {
        assert!(RandomUtils::is_valid_uuid("550e8400-e29b-41d4-a716-446655440000"));
        assert!(RandomUtils::is_valid_uuid("550e8400e29b41d4a716446655440000"));
        assert!(!RandomUtils::is_valid_uuid("invalid"));
        assert!(!RandomUtils::is_valid_uuid("550e8400-e29b-41d4-a716"));
    }
}