//! Base64 Utils - A comprehensive Base64 encoding/decoding library
//! 
//! This crate provides Base64, Base64URL, and Base32 encoding/decoding
//! utilities without any external dependencies.
//!
//! # Features
//! - Standard Base64 encoding/decoding (RFC 4648)
//! - URL-safe Base64 encoding/decoding (no padding)
//! - Base32 encoding/decoding
//! - No external dependencies
//! - No-std compatible (with `std` feature disabled)
//!
//! # Example
//! ```
//! use base64_utils::{Base64, Base64Variant};
//!
//! let encoded = Base64::encode(b"Hello, World!");
//! assert_eq!(encoded, "SGVsbG8sIFdvcmxkIQ==");
//!
//! let decoded = Base64::decode("SGVsbG8sIFdvcmxkIQ==").unwrap();
//! assert_eq!(decoded, b"Hello, World!");
//!
//! // URL-safe variant
//! let url_encoded = Base64::encode_url_safe(b"Hello, World!");
//! assert_eq!(url_encoded, "SGVsbG8sIFdvcmxkIQ");
//! ```

#![cfg_attr(not(feature = "std"), no_std)]

use core::fmt;

/// Base64 variant to use for encoding/decoding
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum Base64Variant {
    /// Standard Base64 with '+' and '/' characters and '=' padding
    Standard,
    /// URL-safe Base64 with '-' and '_' characters, no padding
    UrlSafe,
}

/// Base64 encoding/decoding errors
#[derive(Debug, Clone, PartialEq, Eq)]
pub enum Base64Error {
    /// Invalid character in input
    InvalidCharacter(char),
    /// Invalid padding
    InvalidPadding,
    /// Invalid length
    InvalidLength,
    /// Input contains non-ASCII characters
    NonAsciiInput,
}

impl fmt::Display for Base64Error {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        match self {
            Base64Error::InvalidCharacter(c) => write!(f, "Invalid Base64 character: '{}'", c),
            Base64Error::InvalidPadding => write!(f, "Invalid Base64 padding"),
            Base64Error::InvalidLength => write!(f, "Invalid Base64 string length"),
            Base64Error::NonAsciiInput => write!(f, "Input contains non-ASCII characters"),
        }
    }
}

#[cfg(feature = "std")]
impl std::error::Error for Base64Error {}

/// Standard Base64 alphabet
const STANDARD_ALPHABET: &[u8; 64] = b"ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/";

/// URL-safe Base64 alphabet
const URL_SAFE_ALPHABET: &[u8; 64] = b"ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-_";

/// Standard Base64 decoding table (maps ASCII to 0-63, 255 = invalid)
const STANDARD_DECODE_TABLE: [u8; 256] = generate_decode_table(b"ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/");

/// URL-safe Base64 decoding table
const URL_SAFE_DECODE_TABLE: [u8; 256] = generate_decode_table(b"ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-_");

/// Generate a decoding table at compile time
const fn generate_decode_table(alphabet: &[u8; 64]) -> [u8; 256] {
    let mut table = [255u8; 256];
    let mut i = 0;
    while i < 64 {
        table[alphabet[i] as usize] = i as u8;
        i += 1;
    }
    table
}

/// Base64 encoding and decoding utilities
pub struct Base64;

impl Base64 {
    /// Encodes bytes to standard Base64 string with padding
    /// 
    /// # Example
    /// ```
    /// use base64_utils::Base64;
    /// 
    /// let encoded = Base64::encode(b"Hello");
    /// assert_eq!(encoded, "SGVsbG8=");
    /// ```
    pub fn encode(data: &[u8]) -> String {
        Self::encode_with_alphabet(data, STANDARD_ALPHABET, true)
    }

    /// Encodes bytes to URL-safe Base64 string without padding
    /// 
    /// # Example
    /// ```
    /// use base64_utils::Base64;
    /// 
    /// let encoded = Base64::encode_url_safe(b"Hello");
    /// assert_eq!(encoded, "SGVsbG8");
    /// ```
    pub fn encode_url_safe(data: &[u8]) -> String {
        Self::encode_with_alphabet(data, URL_SAFE_ALPHABET, false)
    }

    /// Encodes bytes to Base64 string with specified variant
    /// 
    /// # Example
    /// ```
    /// use base64_utils::{Base64, Base64Variant};
    /// 
    /// let encoded = Base64::encode_with_variant(b"Hello", Base64Variant::Standard);
    /// assert_eq!(encoded, "SGVsbG8=");
    /// ```
    pub fn encode_with_variant(data: &[u8], variant: Base64Variant) -> String {
        match variant {
            Base64Variant::Standard => Self::encode(data),
            Base64Variant::UrlSafe => Self::encode_url_safe(data),
        }
    }

    /// Internal encoding function
    fn encode_with_alphabet(data: &[u8], alphabet: &[u8; 64], padding: bool) -> String {
        let len = data.len();
        let encoded_len = ((len + 2) / 3) * 4;
        let mut result = String::with_capacity(encoded_len);

        let chunks = len / 3;
        let remainder = len % 3;

        // Process complete chunks
        for i in 0..chunks {
            let idx = i * 3;
            let b0 = data[idx] as usize;
            let b1 = data[idx + 1] as usize;
            let b2 = data[idx + 2] as usize;

            result.push(alphabet[b0 >> 2] as char);
            result.push(alphabet[((b0 & 0x03) << 4) | (b1 >> 4)] as char);
            result.push(alphabet[((b1 & 0x0f) << 2) | (b2 >> 6)] as char);
            result.push(alphabet[b2 & 0x3f] as char);
        }

        // Handle remaining bytes
        if remainder > 0 {
            let idx = chunks * 3;
            let b0 = data[idx] as usize;

            result.push(alphabet[b0 >> 2] as char);

            if remainder == 1 {
                result.push(alphabet[(b0 & 0x03) << 4] as char);
                if padding {
                    result.push_str("==");
                }
            } else {
                let b1 = data[idx + 1] as usize;
                result.push(alphabet[((b0 & 0x03) << 4) | (b1 >> 4)] as char);
                result.push(alphabet[(b1 & 0x0f) << 2] as char);
                if padding {
                    result.push('=');
                }
            }
        }

        result
    }

    /// Decodes a standard Base64 string
    /// 
    /// # Example
    /// ```
    /// use base64_utils::Base64;
    /// 
    /// let decoded = Base64::decode("SGVsbG8=").unwrap();
    /// assert_eq!(decoded, b"Hello");
    /// ```
    pub fn decode(input: &str) -> Result<Vec<u8>, Base64Error> {
        Self::decode_with_table(input, &STANDARD_DECODE_TABLE, true)
    }

    /// Decodes a URL-safe Base64 string
    /// 
    /// # Example
    /// ```
    /// use base64_utils::Base64;
    /// 
    /// let decoded = Base64::decode_url_safe("SGVsbG8").unwrap();
    /// assert_eq!(decoded, b"Hello");
    /// ```
    pub fn decode_url_safe(input: &str) -> Result<Vec<u8>, Base64Error> {
        Self::decode_with_table(input, &URL_SAFE_DECODE_TABLE, false)
    }

    /// Decodes a Base64 string with automatic variant detection
    /// 
    /// # Example
    /// ```
    /// use base64_utils::Base64;
    /// 
    /// let decoded = Base64::decode_auto("SGVsbG8=").unwrap();
    /// assert_eq!(decoded, b"Hello");
    /// 
    /// let decoded_url = Base64::decode_auto("SGVsbG8").unwrap();
    /// assert_eq!(decoded_url, b"Hello");
    /// ```
    pub fn decode_auto(input: &str) -> Result<Vec<u8>, Base64Error> {
        // Try URL-safe first (no padding), then standard
        if input.contains('+') || input.contains('/') {
            Self::decode(input)
        } else {
            Self::decode_url_safe(input).or_else(|_| Self::decode(input))
        }
    }

    /// Internal decoding function
    fn decode_with_table(input: &str, table: &[u8; 256], allow_padding: bool) -> Result<Vec<u8>, Base64Error> {
        let input = input.trim();

        // Check for non-ASCII
        if !input.is_ascii() {
            return Err(Base64Error::NonAsciiInput);
        }

        // Remove padding for processing
        let (data, _padding_len) = if allow_padding && input.ends_with("==") {
            (&input[..input.len() - 2], 2)
        } else if allow_padding && input.ends_with('=') {
            (&input[..input.len() - 1], 1)
        } else {
            (input, 0)
        };

        // Validate length
        if data.is_empty() {
            return Ok(Vec::new());
        }

        if data.len() % 4 != 0 && allow_padding {
            // For standard Base64, length must be multiple of 4 (including padding)
            // But we've already stripped padding, so data.len() % 4 should be 0, 2, or 3
            if data.len() % 4 == 1 {
                return Err(Base64Error::InvalidLength);
            }
        }

        let mut result = Vec::with_capacity((data.len() * 3) / 4);
        let bytes = data.as_bytes();

        // Process 4 characters at a time
        let chunks = bytes.len() / 4;
        let remainder = bytes.len() % 4;

        for i in 0..chunks {
            let idx = i * 4;
            let b0 = Self::decode_char(bytes[idx], table)?;
            let b1 = Self::decode_char(bytes[idx + 1], table)?;
            let b2 = Self::decode_char(bytes[idx + 2], table)?;
            let b3 = Self::decode_char(bytes[idx + 3], table)?;

            result.push((b0 << 2) | (b1 >> 4));
            result.push((b1 << 4) | (b2 >> 2));
            result.push((b2 << 6) | b3);
        }

        // Handle remaining characters
        if remainder >= 2 {
            let idx = chunks * 4;
            let b0 = Self::decode_char(bytes[idx], table)?;
            let b1 = Self::decode_char(bytes[idx + 1], table)?;

            result.push((b0 << 2) | (b1 >> 4));

            if remainder == 3 {
                let b2 = Self::decode_char(bytes[idx + 2], table)?;
                result.push((b1 << 4) | (b2 >> 2));
            }
        }

        Ok(result)
    }

    /// Decode a single character
    fn decode_char(c: u8, table: &[u8; 256]) -> Result<u8, Base64Error> {
        let val = table[c as usize];
        if val == 255 {
            Err(Base64Error::InvalidCharacter(c as char))
        } else {
            Ok(val)
        }
    }

    /// Validates if a string is valid Base64
    /// 
    /// # Example
    /// ```
    /// use base64_utils::Base64;
    /// 
    /// assert!(Base64::is_valid("SGVsbG8="));
    /// assert!(!Base64::is_valid("SGVs!m8="));
    /// ```
    pub fn is_valid(input: &str) -> bool {
        Self::decode(input).is_ok()
    }

    /// Validates if a string is valid Base64 with strict padding check
    pub fn is_valid_strict(input: &str, require_padding: bool) -> bool {
        if require_padding {
            let has_padding = input.ends_with('=') || input.len() % 4 == 0;
            if !has_padding && !input.is_empty() {
                return false;
            }
        }
        Self::decode(input).is_ok()
    }

    /// Calculates the encoded length for given input length
    /// 
    /// # Example
    /// ```
    /// use base64_utils::Base64;
    /// 
    /// assert_eq!(Base64::encoded_len(5), 8);
    /// assert_eq!(Base64::encoded_len(6), 8);
    /// ```
    pub fn encoded_len(input_len: usize) -> usize {
        ((input_len + 2) / 3) * 4
    }

    /// Calculates the decoded length for given input length
    /// 
    /// # Example
    /// ```
    /// use base64_utils::Base64;
    /// 
    /// assert_eq!(Base64::decoded_len(8), 6);
    /// assert_eq!(Base64::decoded_len(4), 3);
    /// ```
    pub fn decoded_len(input_len: usize) -> usize {
        (input_len / 4) * 3
    }
}

/// Base32 encoding and decoding utilities
pub struct Base32;

/// Base32 alphabet (RFC 4648)
const BASE32_ALPHABET: &[u8; 32] = b"ABCDEFGHIJKLMNOPQRSTUVWXYZ234567";

/// Base32 decoding table
const BASE32_DECODE_TABLE: [u8; 256] = generate_base32_decode_table();

const fn generate_base32_decode_table() -> [u8; 256] {
    let mut table = [255u8; 256];
    let alphabet = b"ABCDEFGHIJKLMNOPQRSTUVWXYZ234567";
    let mut i = 0;
    while i < 32 {
        table[alphabet[i] as usize] = i as u8;
        // Lowercase support
        if alphabet[i] >= b'A' && alphabet[i] <= b'Z' {
            table[(alphabet[i] + 32) as usize] = i as u8;
        }
        i += 1;
    }
    table
}

impl Base32 {
    /// Encodes bytes to Base32 string with padding
    /// 
    /// # Example
    /// ```
    /// use base64_utils::Base32;
    /// 
    /// let encoded = Base32::encode(b"Hello");
    /// assert_eq!(encoded, "JBSWY3DP");
    /// ```
    pub fn encode(data: &[u8]) -> String {
        let len = data.len();
        let encoded_len = ((len + 4) / 5) * 8;
        let mut result = String::with_capacity(encoded_len);

        let chunks = len / 5;
        let remainder = len % 5;

        // Process complete chunks (5 bytes -> 8 characters)
        for i in 0..chunks {
            let idx = i * 5;
            let b0 = data[idx] as usize;
            let b1 = data[idx + 1] as usize;
            let b2 = data[idx + 2] as usize;
            let b3 = data[idx + 3] as usize;
            let b4 = data[idx + 4] as usize;

            result.push(BASE32_ALPHABET[b0 >> 3] as char);
            result.push(BASE32_ALPHABET[((b0 & 0x07) << 2) | (b1 >> 6)] as char);
            result.push(BASE32_ALPHABET[(b1 >> 1) & 0x1f] as char);
            result.push(BASE32_ALPHABET[((b1 & 0x01) << 4) | (b2 >> 4)] as char);
            result.push(BASE32_ALPHABET[((b2 & 0x0f) << 1) | (b3 >> 7)] as char);
            result.push(BASE32_ALPHABET[(b3 >> 2) & 0x1f] as char);
            result.push(BASE32_ALPHABET[((b3 & 0x03) << 3) | (b4 >> 5)] as char);
            result.push(BASE32_ALPHABET[b4 & 0x1f] as char);
        }

        // Handle remaining bytes with padding (RFC 4648)
        // 1 byte -> 2 chars + 6 padding
        // 2 bytes -> 4 chars + 4 padding
        // 3 bytes -> 5 chars + 3 padding
        // 4 bytes -> 7 chars + 1 padding
        if remainder > 0 {
            let idx = chunks * 5;
            let b0 = data[idx] as usize;

            result.push(BASE32_ALPHABET[b0 >> 3] as char);

            if remainder == 1 {
                // 1 byte: take remaining 3 bits + 2 zero bits
                result.push(BASE32_ALPHABET[(b0 & 0x07) << 2] as char);
                result.push_str("======"); // 6 padding
            } else if remainder == 2 {
                let b1 = data[idx + 1] as usize;
                result.push(BASE32_ALPHABET[((b0 & 0x07) << 2) | (b1 >> 6)] as char);
                result.push(BASE32_ALPHABET[(b1 >> 1) & 0x1f] as char);
                result.push(BASE32_ALPHABET[(b1 & 0x01) << 4] as char);
                result.push_str("===="); // 4 padding
            } else if remainder == 3 {
                let b1 = data[idx + 1] as usize;
                let b2 = data[idx + 2] as usize;
                result.push(BASE32_ALPHABET[((b0 & 0x07) << 2) | (b1 >> 6)] as char);
                result.push(BASE32_ALPHABET[(b1 >> 1) & 0x1f] as char);
                result.push(BASE32_ALPHABET[((b1 & 0x01) << 4) | (b2 >> 4)] as char);
                result.push(BASE32_ALPHABET[(b2 & 0x0f) << 1] as char);
                result.push_str("==="); // 3 padding
            } else if remainder == 4 {
                let b1 = data[idx + 1] as usize;
                let b2 = data[idx + 2] as usize;
                let b3 = data[idx + 3] as usize;
                result.push(BASE32_ALPHABET[((b0 & 0x07) << 2) | (b1 >> 6)] as char);
                result.push(BASE32_ALPHABET[(b1 >> 1) & 0x1f] as char);
                result.push(BASE32_ALPHABET[((b1 & 0x01) << 4) | (b2 >> 4)] as char);
                result.push(BASE32_ALPHABET[((b2 & 0x0f) << 1) | (b3 >> 7)] as char);
                result.push(BASE32_ALPHABET[(b3 >> 2) & 0x1f] as char);
                result.push(BASE32_ALPHABET[(b3 & 0x03) << 3] as char);
                result.push('='); // 1 padding
            }
        }

        result
    }

    /// Decodes a Base32 string
    /// 
    /// # Example
    /// ```
    /// use base64_utils::Base32;
    /// 
    /// let decoded = Base32::decode("JBSWY3DP").unwrap();
    /// assert_eq!(decoded, b"Hello");
    /// ```
    pub fn decode(input: &str) -> Result<Vec<u8>, Base64Error> {
        let input = input.trim().to_uppercase();
        
        if !input.is_ascii() {
            return Err(Base64Error::NonAsciiInput);
        }

        // Remove padding
        let data = input.trim_end_matches('=');

        if data.is_empty() {
            return Ok(Vec::new());
        }

        if data.len() % 8 != 0 && data.len() < 2 {
            return Err(Base64Error::InvalidLength);
        }

        let mut result = Vec::with_capacity((data.len() * 5) / 8);
        let bytes = data.as_bytes();

        // Process 8 characters at a time
        let chunks = bytes.len() / 8;
        let remainder = bytes.len() % 8;

        for i in 0..chunks {
            let idx = i * 8;
            let vals: [u8; 8] = [
                Self::decode_char_32(bytes[idx])?,
                Self::decode_char_32(bytes[idx + 1])?,
                Self::decode_char_32(bytes[idx + 2])?,
                Self::decode_char_32(bytes[idx + 3])?,
                Self::decode_char_32(bytes[idx + 4])?,
                Self::decode_char_32(bytes[idx + 5])?,
                Self::decode_char_32(bytes[idx + 6])?,
                Self::decode_char_32(bytes[idx + 7])?,
            ];

            result.push((vals[0] << 3) | (vals[1] >> 2));
            result.push((vals[1] << 6) | (vals[2] << 1) | (vals[3] >> 4));
            result.push((vals[3] << 4) | (vals[4] >> 1));
            result.push((vals[4] << 7) | (vals[5] << 2) | (vals[6] >> 3));
            result.push((vals[6] << 5) | vals[7]);
        }

        // Handle remaining characters
        if remainder > 0 {
            let idx = chunks * 8;
            let mut vals = [0u8; 8];
            for i in 0..remainder {
                vals[i] = Self::decode_char_32(bytes[idx + i])?;
            }

            if remainder >= 2 {
                result.push((vals[0] << 3) | (vals[1] >> 2));
            }
            if remainder >= 4 {
                result.push((vals[1] << 6) | (vals[2] << 1) | (vals[3] >> 4));
            }
            if remainder >= 5 {
                result.push((vals[3] << 4) | (vals[4] >> 1));
            }
            if remainder >= 7 {
                result.push((vals[4] << 7) | (vals[5] << 2) | (vals[6] >> 3));
            }
        }

        Ok(result)
    }

    fn decode_char_32(c: u8) -> Result<u8, Base64Error> {
        let val = BASE32_DECODE_TABLE[c as usize];
        if val == 255 {
            Err(Base64Error::InvalidCharacter(c as char))
        } else {
            Ok(val)
        }
    }

    /// Validates if a string is valid Base32
    pub fn is_valid(input: &str) -> bool {
        Self::decode(input).is_ok()
    }
}

// ==================== Tests ====================

#[cfg(test)]
mod tests {
    use super::*;

    mod base64_encode {
        use super::*;

        #[test]
        fn test_empty() {
            assert_eq!(Base64::encode(b""), "");
        }

        #[test]
        fn test_single_byte() {
            assert_eq!(Base64::encode(b"A"), "QQ==");
        }

        #[test]
        fn test_two_bytes() {
            assert_eq!(Base64::encode(b"AB"), "QUI=");
        }

        #[test]
        fn test_three_bytes() {
            assert_eq!(Base64::encode(b"ABC"), "QUJD");
        }

        #[test]
        fn test_hello_world() {
            assert_eq!(Base64::encode(b"Hello, World!"), "SGVsbG8sIFdvcmxkIQ==");
        }

        #[test]
        fn test_foobar() {
            assert_eq!(Base64::encode(b"foobar"), "Zm9vYmFy");
        }

        #[test]
        fn test_binary_data() {
            let data: Vec<u8> = (0..=255).collect();
            let encoded = Base64::encode(&data);
            assert!(Base64::decode(&encoded).is_ok());
        }

        #[test]
        fn test_url_safe_no_padding() {
            assert_eq!(Base64::encode_url_safe(b"Hello, World!"), "SGVsbG8sIFdvcmxkIQ");
        }

        #[test]
        fn test_url_safe_special_chars() {
            // Data that would produce + and / in standard encoding
            let data = [0xfb, 0xff];
            assert_eq!(Base64::encode(&data), "+/8=");
            assert_eq!(Base64::encode_url_safe(&data), "-_8");
        }

        #[test]
        fn test_encoded_len() {
            assert_eq!(Base64::encoded_len(0), 0);
            assert_eq!(Base64::encoded_len(1), 4);
            assert_eq!(Base64::encoded_len(2), 4);
            assert_eq!(Base64::encoded_len(3), 4);
            assert_eq!(Base64::encoded_len(4), 8);
            assert_eq!(Base64::encoded_len(5), 8);
            assert_eq!(Base64::encoded_len(6), 8);
        }
    }

    mod base64_decode {
        use super::*;

        #[test]
        fn test_empty() {
            assert_eq!(Base64::decode("").unwrap(), b"");
        }

        #[test]
        fn test_single_byte() {
            assert_eq!(Base64::decode("QQ==").unwrap(), b"A");
        }

        #[test]
        fn test_two_bytes() {
            assert_eq!(Base64::decode("QUI=").unwrap(), b"AB");
        }

        #[test]
        fn test_three_bytes() {
            assert_eq!(Base64::decode("QUJD").unwrap(), b"ABC");
        }

        #[test]
        fn test_hello_world() {
            assert_eq!(Base64::decode("SGVsbG8sIFdvcmxkIQ==").unwrap(), b"Hello, World!");
        }

        #[test]
        fn test_foobar() {
            assert_eq!(Base64::decode("Zm9vYmFy").unwrap(), b"foobar");
        }

        #[test]
        fn test_url_safe() {
            assert_eq!(Base64::decode_url_safe("SGVsbG8sIFdvcmxkIQ").unwrap(), b"Hello, World!");
        }

        #[test]
        fn test_url_safe_special() {
            assert_eq!(Base64::decode_url_safe("-_8").unwrap(), &[0xfb, 0xff]);
        }

        #[test]
        fn test_decode_auto_standard() {
            assert_eq!(Base64::decode_auto("SGVsbG8=").unwrap(), b"Hello");
        }

        #[test]
        fn test_decode_auto_url_safe() {
            assert_eq!(Base64::decode_auto("SGVsbG8").unwrap(), b"Hello");
        }

        #[test]
        fn test_invalid_character() {
            assert!(matches!(Base64::decode("SGVs!m8="), Err(Base64Error::InvalidCharacter('!'))));
        }

        #[test]
        fn test_non_ascii() {
            assert!(matches!(Base64::decode("SGVs中文"), Err(Base64Error::NonAsciiInput)));
        }

        #[test]
        fn test_roundtrip() {
            let original = b"The quick brown fox jumps over the lazy dog";
            let encoded = Base64::encode(original);
            let decoded = Base64::decode(&encoded).unwrap();
            assert_eq!(decoded, original);
        }
    }

    mod base64_validation {
        use super::*;

        #[test]
        fn test_is_valid() {
            assert!(Base64::is_valid("SGVsbG8="));
            assert!(Base64::is_valid("Zm9vYmFy"));
            assert!(!Base64::is_valid("SGVs!m8="));
        }

        #[test]
        fn test_is_valid_strict() {
            assert!(Base64::is_valid_strict("SGVsbG8=", true));
            assert!(!Base64::is_valid_strict("SGVsbG8", true));
        }
    }

    mod base32_encode {
        use super::*;

        #[test]
        fn test_empty() {
            assert_eq!(Base32::encode(b""), "");
        }

        #[test]
        fn test_single_byte() {
            // 'A' (65) -> bits 01000001 -> first 5 bits: 01000 = 8 -> 'I', remaining 3 bits: 001 + 00 = 00100 = 4 -> 'E'
            assert_eq!(Base32::encode(b"A"), "IE======");
        }

        #[test]
        fn test_hello() {
            assert_eq!(Base32::encode(b"Hello"), "JBSWY3DP");
        }

        #[test]
        fn test_hello_world() {
            assert_eq!(Base32::encode(b"Hello, World!"), "JBSWY3DPFQQFO33SNRSCC===");
        }

        #[test]
        fn test_foobar() {
            assert_eq!(Base32::encode(b"foobar"), "MZXW6YTBOI======");
        }

        #[test]
        fn test_roundtrip() {
            let original = b"The quick brown fox jumps over the lazy dog";
            let encoded = Base32::encode(original);
            let decoded = Base32::decode(&encoded).unwrap();
            assert_eq!(decoded, original);
        }
    }

    mod base32_decode {
        use super::*;

        #[test]
        fn test_empty() {
            assert_eq!(Base32::decode("").unwrap(), b"");
        }

        #[test]
        fn test_single_byte() {
            assert_eq!(Base32::decode("IE======").unwrap(), b"A");
        }

        #[test]
        fn test_hello() {
            assert_eq!(Base32::decode("JBSWY3DP").unwrap(), b"Hello");
        }

        #[test]
        fn test_hello_world() {
            assert_eq!(Base32::decode("JBSWY3DPFQQFO33SNRSCC===").unwrap(), b"Hello, World!");
        }

        #[test]
        fn test_lowercase() {
            assert_eq!(Base32::decode("jbswy3dp").unwrap(), b"Hello");
        }

        #[test]
        fn test_invalid_character() {
            assert!(matches!(Base32::decode("JBSWY31P"), Err(Base64Error::InvalidCharacter('1'))));
        }
    }

    mod base32_validation {
        use super::*;

        #[test]
        fn test_is_valid() {
            assert!(Base32::is_valid("JBSWY3DP"));
            assert!(Base32::is_valid("jbswy3dp"));
            assert!(!Base32::is_valid("JBSWY31P"));
        }
    }

    mod edge_cases {
        use super::*;

        #[test]
        fn test_base64_whitespace() {
            assert_eq!(Base64::decode(" SGVsbG8= ").unwrap(), b"Hello");
        }

        #[test]
        fn test_base64_long_data() {
            let data: Vec<u8> = (0..=255).cycle().take(10000).collect();
            let encoded = Base64::encode(&data);
            let decoded = Base64::decode(&encoded).unwrap();
            assert_eq!(decoded, data);
        }

        #[test]
        fn test_base32_long_data() {
            let data: Vec<u8> = (0..=255).cycle().take(10000).collect();
            let encoded = Base32::encode(&data);
            let decoded = Base32::decode(&encoded).unwrap();
            assert_eq!(decoded, data);
        }
    }
}