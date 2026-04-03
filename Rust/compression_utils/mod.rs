//! # Compression Utilities
//!
//! A zero-dependency compression utility module for Rust.
//! Provides common compression algorithms using only the Rust standard library.
//!
//! ## Features
//!
//! - **Run-Length Encoding (RLE)** - Simple lossless compression for repetitive data
//! - **Delta Encoding** - Efficient for sequences with small differences
//! - **Base64 Encoding** - Binary-to-text encoding for data transmission
//! - **Hex Encoding** - Binary-to-hexadecimal encoding
//! - **URL Encoding** - Percent-encoding for URLs
//!
//! ## Usage
//!
//! ```rust
//! // Run-Length Encoding
//! let compressed = rle_encode(b"AAABBBCCCC");
//! let decompressed = rle_decode(&compressed.data);
//!
//! // Delta Encoding
//! let data = vec![10, 12, 15, 15, 20];
//! let delta = delta_encode(&data);
//! let restored = delta_decode(&delta);
//! ```

/// Run-Length Encoding result containing the compressed data and metadata
#[derive(Debug, Clone, PartialEq)]
pub struct RleResult {
    /// The compressed byte data
    pub data: Vec<u8>,
    /// Original data length
    pub original_len: usize,
    /// Compression ratio (compressed / original)
    pub ratio: f64,
}

/// Compression statistics
#[derive(Debug, Clone, PartialEq)]
pub struct CompressionStats {
    /// Original size in bytes
    pub original_size: usize,
    /// Compressed size in bytes
    pub compressed_size: usize,
    /// Compression ratio (compressed / original)
    pub ratio: f64,
    /// Space saved percentage
    pub space_saved: f64,
}

/// Run-Length Encoding (RLE) compression
///
/// Compresses consecutive repeated bytes by storing the byte and its count.
/// Format: [count, byte, count, byte, ...]
///
/// # Arguments
/// * `data` - Input bytes to compress
///
/// # Returns
/// * `RleResult` - Compressed data with metadata
///
/// # Examples
/// ```
/// let compressed = rle_encode(b"AAABBBCCCC");
/// assert_eq!(compressed.data, vec![3, b'A', 3, b'B', 4, b'C']);
/// ```
pub fn rle_encode(data: &[u8]) -> RleResult {
    if data.is_empty() {
        return RleResult {
            data: Vec::new(),
            original_len: 0,
            ratio: 0.0,
        };
    }

    let mut result = Vec::new();
    let mut current = data[0];
    let mut count: u8 = 1;

    for &byte in &data[1..] {
        if byte == current && count < 255 {
            count += 1;
        } else {
            result.push(count);
            result.push(current);
            current = byte;
            count = 1;
        }
    }
    result.push(count);
    result.push(current);

    let ratio = result.len() as f64 / data.len() as f64;
    RleResult {
        data: result,
        original_len: data.len(),
        ratio,
    }
}

/// Run-Length Encoding (RLE) decompression
///
/// Decompresses data that was compressed using RLE.
///
/// # Arguments
/// * `data` - Compressed RLE data
///
/// # Returns
/// * `Vec<u8>` - Decompressed bytes
///
/// # Examples
/// ```
/// let compressed = rle_encode(b"AAABBBCCCC");
/// let decompressed = rle_decode(&compressed.data);
/// assert_eq!(decompressed, b"AAABBBCCCC");
/// ```
pub fn rle_decode(data: &[u8]) -> Vec<u8> {
    if data.is_empty() {
        return Vec::new();
    }

    let mut result = Vec::new();
    let mut i = 0;

    while i + 1 < data.len() {
        let count = data[i] as usize;
        let byte = data[i + 1];
        for _ in 0..count {
            result.push(byte);
        }
        i += 2;
    }

    result
}

/// Delta Encoding compression
///
/// Encodes data as differences between consecutive values.
/// Efficient for data with small incremental changes.
///
/// # Arguments
/// * `data` - Input slice of i64 values
///
/// # Returns
/// * `Vec<i64>` - Delta encoded values (first value + differences)
///
/// # Examples
/// ```
/// let data = vec![10, 12, 15, 15, 20];
/// let encoded = delta_encode(&data);
/// assert_eq!(encoded, vec![10, 2, 3, 0, 5]);
/// ```
pub fn delta_encode(data: &[i64]) -> Vec<i64> {
    if data.is_empty() {
        return Vec::new();
    }

    let mut result = Vec::with_capacity(data.len());
    result.push(data[0]);

    for i in 1..data.len() {
        result.push(data[i] - data[i - 1]);
    }

    result
}

/// Delta Encoding decompression
///
/// Decodes data that was compressed using delta encoding.
///
/// # Arguments
/// * `data` - Delta encoded values
///
/// # Returns
/// * `Vec<i64>` - Restored original values
///
/// # Examples
/// ```
/// let encoded = vec![10, 2, 3, 0, 5];
/// let decoded = delta_decode(&encoded);
/// assert_eq!(decoded, vec![10, 12, 15, 15, 20]);
/// ```
pub fn delta_decode(data: &[i64]) -> Vec<i64> {
    if data.is_empty() {
        return Vec::new();
    }

    let mut result = Vec::with_capacity(data.len());
    result.push(data[0]);

    for i in 1..data.len() {
        result.push(result[i - 1] + data[i]);
    }

    result
}

/// Base64 encoding
///
/// Encodes binary data to Base64 ASCII string.
/// Uses standard Base64 alphabet with padding.
///
/// # Arguments
/// * `data` - Input bytes to encode
///
/// # Returns
/// * `String` - Base64 encoded string
///
/// # Examples
/// ```
/// let encoded = base64_encode(b"Hello, World!");
/// assert_eq!(encoded, "SGVsbG8sIFdvcmxkIQ==");
/// ```
pub fn base64_encode(data: &[u8]) -> String {
    const BASE64_CHARS: &[u8] = b"ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/";

    if data.is_empty() {
        return String::new();
    }

    let mut result = String::with_capacity((data.len() + 2) / 3 * 4);
    let mut i = 0;

    while i < data.len() {
        let b1 = data[i];
        let b2 = if i + 1 < data.len() { data[i + 1] } else { 0 };
        let b3 = if i + 2 < data.len() { data[i + 2] } else { 0 };

        let bitmap = ((b1 as u32) << 16) | ((b2 as u32) << 8) | (b3 as u32);

        result.push(BASE64_CHARS[((bitmap >> 18) & 0x3F) as usize] as char);
        result.push(BASE64_CHARS[((bitmap >> 12) & 0x3F) as usize] as char);

        if i + 1 < data.len() {
            result.push(BASE64_CHARS[((bitmap >> 6) & 0x3F) as usize] as char);
        } else {
            result.push('=');
        }

        if i + 2 < data.len() {
            result.push(BASE64_CHARS[(bitmap & 0x3F) as usize] as char);
        } else {
            result.push('=');
        }

        i += 3;
    }

    result
}

/// Base64 decoding
///
/// Decodes a Base64 encoded string back to binary data.
///
/// # Arguments
/// * `data` - Base64 encoded string
///
/// # Returns
/// * `Option<Vec<u8>>` - Decoded bytes or None if invalid
///
/// # Examples
/// ```
/// let decoded = base64_decode("SGVsbG8sIFdvcmxkIQ==");
/// assert_eq!(decoded, Some(b"Hello, World!".to_vec()));
/// ```
pub fn base64_decode(data: &str) -> Option<Vec<u8>> {
    fn decode_char(c: char) -> Option<u8> {
        match c {
            'A'..='Z' => Some(c as u8 - b'A'),
            'a'..='z' => Some(c as u8 - b'a' + 26),
            '0'..='9' => Some(c as u8 - b'0' + 52),
            '+' => Some(62),
            '/' => Some(63),
            '=' => Some(0),
            _ => None,
        }
    }

    if data.is_empty() {
        return Some(Vec::new());
    }

    let data = data.trim();
    let len = data.len();

    if len % 4 != 0 {
        return None;
    }

    let padding = data.chars().rev().take_while(|&c| c == '=').count();
    let output_len = (len / 4) * 3 - padding;
    let mut result = Vec::with_capacity(output_len);

    let chars: Vec<char> = data.chars().collect();
    let mut i = 0;

    while i + 3 < len {
        let c1 = decode_char(chars[i])?;
        let c2 = decode_char(chars[i + 1])?;
        let c3 = decode_char(chars[i + 2])?;
        let c4 = decode_char(chars[i + 3])?;

        let bitmap = ((c1 as u32) << 18) | ((c2 as u32) << 12) | ((c3 as u32) << 6) | (c4 as u32);

        result.push((bitmap >> 16) as u8);
        if chars[i + 2] != '=' {
            result.push(((bitmap >> 8) & 0xFF) as u8);
        }
        if chars[i + 3] != '=' {
            result.push((bitmap & 0xFF) as u8);
        }

        i += 4;
    }

    Some(result)
}

/// Hex encoding
///
/// Encodes binary data to hexadecimal string.
///
/// # Arguments
/// * `data` - Input bytes to encode
///
/// # Returns
/// * `String` - Hex encoded string (lowercase)
///
/// # Examples
/// ```
/// let encoded = hex_encode(b"Hello");
/// assert_eq!(encoded, "48656c6c6f");
/// ```
pub fn hex_encode(data: &[u8]) -> String {
    const HEX_CHARS: &[u8] = b"0123456789abcdef";

    if data.is_empty() {
        return String::new();
    }

    let mut result = String::with_capacity(data.len() * 2);
    for &byte in data {
        result.push(HEX_CHARS[(byte >> 4) as usize] as char);
        result.push(HEX_CHARS[(byte & 0xF) as usize] as char);
    }
    result
}

/// Hex decoding
///
/// Decodes a hexadecimal string back to binary data.
///
/// # Arguments
/// * `data` - Hex encoded string
///
/// # Returns
/// * `Option<Vec<u8>>` - Decoded bytes or None if invalid
///
/// # Examples
/// ```
/// let decoded = hex_decode("48656c6c6f");
/// assert_eq!(decoded, Some(b"Hello".to_vec()));
/// ```
pub fn hex_decode(data: &str) -> Option<Vec<u8>> {
    fn decode_char(c: char) -> Option<u8> {
        match c {
            '0'..='9' => Some(c as u8 - b'0'),
            'a'..='f' => Some(c as u8 - b'a' + 10),
            'A'..='F' => Some(c as u8 - b'A' + 10),
            _ => None,
        }
    }

    let data = data.trim();
    if data.is_empty() {
        return Some(Vec::new());
    }

    if data.len() % 2 != 0 {
        return None;
    }

    let mut result = Vec::with_capacity(data.len() / 2);
    let chars: Vec<char> = data.chars().collect();

    for i in (0..chars.len()).step_by(2) {
        let high = decode_char(chars[i])?;
        let low = decode_char(chars[i + 1])?;
        result.push((high << 4) | low);
    }

    Some(result)
}

/// URL encoding (percent-encoding)
///
/// Encodes a string for use in URLs.
/// Alphanumeric and unreserved characters (-_.~) are not encoded.
///
/// # Arguments
/// * `data` - String to encode
///
/// # Returns
/// * `String` - URL encoded string
///
/// # Examples
/// ```
/// let encoded = url_encode("hello world!");
/// assert_eq!(encoded, "hello%20world%21");
/// ```
pub fn url_encode(data: &str) -> String {
    if data.is_empty() {
        return String::new();
    }

    let mut result = String::with_capacity(data.len());
    for byte in data.bytes() {
        match byte {
            b'A'..=b'Z' | b'a'..=b'z' | b'0'..=b'9' | b'-' | b'_' | b'.' | b'~' => {
                result.push(byte as char);
            }
            _ => {
                result.push('%');
                result.push_str(&format!("{:02X}", byte));
            }
        }
    }
    result
}

/// URL decoding (percent-decoding)
///
/// Decodes a percent-encoded URL string.
///
/// # Arguments
/// * `data` - URL encoded string
///
/// # Returns
/// * `Option<String>` - Decoded string or None if invalid
///
/// # Examples
/// ```
/// let decoded = url_decode("hello%20world%21");
/// assert_eq!(decoded, Some("hello world!".to_string()));
/// ```
pub fn url_decode(data: &str) -> Option<String> {
    if data.is_empty() {
        return Some(String::new());
    }

    let mut result = String::with_capacity(data.len());
    let chars: Vec<char> = data.chars().collect();
    let mut i = 0;

    while i < chars.len() {
        if chars[i] == '%' {
            if i + 2 >= chars.len() {
                return None;
            }
            let hex = &data[i + 1..i + 3];
            let byte = u8::from_str_radix(hex, 16).ok()?;
            result.push(byte as char);
            i += 3;
        } else if chars[i] == '+' {
            result.push(' ');
            i += 1;
        } else {
            result.push(chars[i]);
            i += 1;
        }
    }

    Some(result)
}

/// Calculate compression statistics
///
/// # Arguments
/// * `original` - Original data size
/// * `compressed` - Compressed data size
///
/// # Returns
/// * `CompressionStats` - Statistics about the compression
///
/// # Examples
/// ```
/// let stats = calc_stats(100, 60);
/// assert_eq!(stats.space_saved, 40.0);
/// ```
pub fn calc_stats(original: usize, compressed: usize) -> CompressionStats {
    let ratio = if original > 0 {
        compressed as f64 / original as f64
    } else {
        0.0
    };
    let space_saved = if original > 0 {
        (1.0 - ratio) * 100.0
    } else {
        0.0
    };

    CompressionStats {
        original_size: original,
        compressed_size: compressed,
        ratio,
        space_saved,
    }
}

/// Check if a string is valid Base64
///
/// # Arguments
/// * `data` - String to check
///
/// # Returns
/// * `bool` - True if valid Base64
///
/// # Examples
/// ```
/// assert!(is_valid_base64("SGVsbG8="));
/// assert!(!is_valid_base64("invalid!"));
/// ```
pub fn is_valid_base64(data: &str) -> bool {
    if data.is_empty() {
        return true;
    }
    let trimmed = data.trim();
    if trimmed.len() % 4 != 0 {
        return false;
    }
    base64_decode(data).is_some()
}

/// Check if a string is valid hex
///
/// # Arguments
/// * `data` - String to check
///
/// # Returns
/// * `bool` - True if valid hex
///
/// # Examples
/// ```
/// assert!(is_valid_hex("48656c6c6f"));
/// assert!(!is_valid_hex("xyz"));
/// ```
pub fn is_valid_hex(data: &str) -> bool {
    if data.is_empty() {
        return true;
    }
    let trimmed = data.trim();
    if trimmed.len() % 2 != 0 {
        return false;
    }
    hex_decode(data).is_some()
}

/// Compress using Burrows-Wheeler Transform (BWT) preprocessing
///
/// This is a simplified version that performs the BWT transform.
/// BWT rearranges data to group similar characters together,
/// making it more compressible by other algorithms like RLE.
///
/// # Arguments
/// * `data` - Input bytes
///
/// # Returns
/// * `(Vec<u8>, usize)` - Transformed data and original index
///
/// # Examples
/// ```
/// let (transformed, index) = bwt_transform(b"banana");
/// let restored = bwt_reverse(&transformed, index);
/// assert_eq!(restored, b"banana");
/// ```
pub fn bwt_transform(data: &[u8]) -> (Vec<u8>, usize) {
    if data.is_empty() {
        return (Vec::new(), 0);
    }

    let n = data.len();
    let mut rotations: Vec<Vec<u8>> = Vec::with_capacity(n);

    for i in 0..n {
        let mut rotation = Vec::with_capacity(n);
        for j in 0..n {
            rotation.push(data[(i + j) % n]);
        }
        rotations.push(rotation);
    }

    rotations.sort();

    let mut result = Vec::with_capacity(n);
    let mut original_index = 0;

    for (i, rotation) in rotations.iter().enumerate() {
        result.push(rotation[n - 1]);
        if rotation == &data.to_vec() {
            original_index = i;
        }
    }

    (result, original_index)
}

/// Reverse Burrows-Wheeler Transform
///
/// Reconstructs the original data from BWT transformed data.
///
/// # Arguments
/// * `data` - BWT transformed data
/// * `index` - Original index from bwt_transform
///
/// # Returns
/// * `Vec<u8>` - Restored original data
///
/// # Examples
/// ```
/// let (transformed, index) = bwt_transform(b"banana");
/// let restored = bwt_reverse(&transformed, index);
/// assert_eq!(restored, b"banana");
/// ```
pub fn bwt_reverse(data: &[u8], index: usize) -> Vec<u8> {
    if data.is_empty() {
        return Vec::new();
    }

    let n = data.len();
    let mut table: Vec<Vec<u8>> = Vec::with_capacity(n);

    for _ in 0..n {
        table.push(Vec::new());
    }

    for _ in 0..n {
        for (i, &byte) in data.iter().enumerate() {
            table[i].insert(0, byte);
        }
        table.sort();
    }

    table[index].clone()
}

/// Simple dictionary-based compression
///
/// Uses a basic LZW-like algorithm for compression.
/// Builds a dictionary of patterns and replaces them with codes.
///
/// # Arguments
/// * `data` - Input bytes
///
/// # Returns
/// * `Vec<u16>` - Compressed codes
///
/// # Examples
/// ```
/// let data = b"TOBEORNOTTOBEORTOBEORNOT";
/// let compressed = lzw_compress(data);
/// let decompressed = lzw_decompress(&compressed);
/// assert_eq!(decompressed, data.to_vec());
/// ```
pub fn lzw_compress(data: &[u8]) -> Vec<u16> {
    if data.is_empty() {
        return Vec::new();
    }

    // Initialize dictionary with single bytes
    let mut dict: std::collections::HashMap<Vec<u8>, u16> = std::collections::HashMap::new();
    for i in 0..=255 {
        dict.insert(vec![i as u8], i as u16);
    }

    let mut result = Vec::new();
    let mut current = Vec::new();
    let mut next_code: u16 = 256;

    for &byte in data {
        let mut test = current.clone();
        test.push(byte);

        if dict.contains_key(&test) {
            current = test;
        } else {
            result.push(dict[&current]);
            if next_code < 4096 {
                dict.insert(test, next_code);
                next_code += 1;
            }
            current = vec![byte];
        }
    }

    if !current.is_empty() {
        result.push(dict[&current]);
    }

    result
}

/// Simple dictionary-based decompression
///
/// Decompresses data compressed with lzw_compress.
///
/// # Arguments
/// * `data` - Compressed codes
///
/// # Returns
/// * `Vec<u8>` - Decompressed data
///
/// # Examples
/// ```
/// let data = b"TOBEORNOTTOBEORTOBEORNOT";
/// let compressed = lzw_compress(data);
/// let decompressed = lzw_decompress(&compressed);
/// assert_eq!(decompressed, data.to_vec());
/// ```
pub fn lzw_decompress(data: &[u16]) -> Vec<u8> {
    if data.is_empty() {
        return Vec::new();
    }

    // Initialize dictionary with single bytes
    let mut dict: std::collections::HashMap<u16, Vec<u8>> = std::collections::HashMap::new();
    for i in 0..=255 {
        dict.insert(i as u16, vec![i as u8]);
    }

    let mut result = Vec::new();
    let mut prev_code = data[0];
    result.extend(&dict[&prev_code]);

    let mut next_code: u16 = 256;

    for &code in &data[1..] {
        let entry = if dict.contains_key(&code) {
            dict[&code].clone()
        } else {
            let mut entry = dict[&prev_code].clone();
            entry.push(entry[0]);
            entry
        };

        result.extend(&entry);

        if next_code < 4096 {
            let mut new_entry = dict[&prev_code].clone();
            new_entry.push(entry[0]);
            dict.insert(next_code, new_entry);
            next_code += 1;
        }

        prev_code = code;
    }

    result
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_rle_encode_decode() {
        let data = b"AAABBBCCCC";
        let compressed = rle_encode(data);
        assert_eq!(compressed.data, vec![3, b'A', 3, b'B', 4, b'C']);
        assert_eq!(compressed.original_len, 10);

        let decompressed = rle_decode(&compressed.data);
        assert_eq!(decompressed, data.to_vec());
    }

    #[test]
    fn test_rle_empty() {
        let compressed = rle_encode(b"");
        assert!(compressed.data.is_empty());
        assert_eq!(compressed.original_len, 0);
    }

    #[test]
    fn test_delta_encode_decode() {
        let data = vec![10, 12, 15, 15, 20];
        let encoded = delta_encode(&data);
        assert_eq!(encoded, vec![10, 2, 3, 0, 5]);

        let decoded = delta_decode(&encoded);
        assert_eq!(decoded, data);
    }

    #[test]
    fn test_delta_empty() {
        let encoded = delta_encode(&[]);
        assert!(encoded.is_empty());
    }

    #[test]
    fn test_base64_encode_decode() {
        let data = b"Hello, World!";
        let encoded = base64_encode(data);
        assert_eq!(encoded, "SGVsbG8sIFdvcmxkIQ==");

        let decoded = base64_decode(&encoded);
        assert_eq!(decoded, Some(data.to_vec()));
    }

    #[test]
    fn test_base64_empty() {
        assert_eq!(base64_encode(b""), "");
        assert_eq!(base64_decode(""), Some(Vec::new()));
    }

    #[test]
    fn test_hex_encode_decode() {
        let data = b"Hello";
        let encoded = hex_encode(data);
        assert_eq!(encoded, "48656c6c6f");

        let decoded = hex_decode(&encoded);
        assert_eq!(decoded, Some(data.to_vec()));
    }

    #[test]
    fn test_url_encode_decode() {
        let data = "hello world!";
        let encoded = url_encode(data);
        assert_eq!(encoded, "hello%20world%21");

        let decoded = url_decode(&encoded);
        assert_eq!(decoded, Some(data.to_string()));
    }

    #[test]
    fn test_calc_stats() {
        let stats = calc_stats(100, 60);
        assert_eq!(stats.original_size, 100);
        assert_eq!(stats.compressed_size, 60);
        assert_eq!(stats.ratio, 0.6);
        assert_eq!(stats.space_saved, 40.0);
    }

    #[test]
    fn test_bwt() {
        let data = b"banana";
        let (transformed, index) = bwt_transform(data);
        let restored = bwt_reverse(&transformed, index);
        assert_eq!(restored, data.to_vec());
    }

    #[test]
    fn test_lzw() {
        let data = b"TOBEORNOTTOBEORTOBEORNOT";
        let compressed = lzw_compress(data);
        let decompressed = lzw_decompress(&compressed);
        assert_eq!(decompressed, data.to_vec());
    }

    #[test]
    fn test_is_valid_base64() {
        assert!(is_valid_base64("SGVsbG8="));
        assert!(!is_valid_base64("invalid!"));
    }

    #[test]
    fn test_is_valid_hex() {
        assert!(is_valid_hex("48656c6c6f"));
        assert!(!is_valid_hex("xyz"));
    }
}
