//! Base32 encoding and decoding utilities.
//! Implements RFC 4648 base32 alphabet.

/// The standard base32 alphabet (RFC 4648)
const BASE32_ALPHABET: &[u8; 32] = b"ABCDEFGHIJKLMNOPQRSTUVWXYZ234567";

/// Decoding map from ASCII byte to base32 value (0-31) or -1 for invalid
fn get_base32_value(byte: u8) -> i8 {
    match byte {
        b'A'..=b'Z' => (byte - b'A') as i8,
        b'2'..=b'7' => (byte - b'2' + 26) as i8,
        b'=' => -2, // padding
        _ => -1,
    }
}

/// Encodes a byte slice into base32 string with padding.
pub fn encode(data: &[u8]) -> String {
    const OUTPUT_BITS: u32 = 5;
    const OUTPUT_MASK: u64 = (1 << OUTPUT_BITS) - 1;

    if data.is_empty() {
        return String::new();
    }

    let mut result = String::with_capacity((data.len() + 7) / 8 * 8);
    let mut value: u64 = 0;
    let mut bits_in_value: u32 = 0;

    for &byte in data {
        value = (value << 8) | (byte as u64);
        bits_in_value += 8;

        while bits_in_value >= OUTPUT_BITS {
            bits_in_value -= OUTPUT_BITS;
            let index = ((value >> bits_in_value) & OUTPUT_MASK) as usize;
            result.push(BASE32_ALPHABET[index] as char);
        }
    }

    // Handle any remaining bits (left-aligned, zeros added on right)
    if bits_in_value > 0 {
        let index = ((value << (OUTPUT_BITS - bits_in_value)) & OUTPUT_MASK) as usize;
        result.push(BASE32_ALPHABET[index] as char);
    }

    // Add padding to make output length a multiple of 8
    let padding_needed = (8 - result.len() % 8) % 8;
    result.extend(std::iter::repeat('=').take(padding_needed));

    result
}

/// Encodes a byte slice into base32 string without padding.
pub fn encode_nopad(data: &[u8]) -> String {
    encode(data).trim_end_matches('=').to_string()
}

/// Decodes a base32 string (with or without padding) back to bytes.
pub fn decode(input: &str) -> Result<Vec<u8>, &'static str> {
    let input = input.trim().to_uppercase();
    
    if input.is_empty() {
        return Ok(Vec::new());
    }

    let chars: Vec<u8> = input
        .chars()
        .filter(|&c| c != '=')
        .map(|c| c as u8)
        .collect();

    if chars.is_empty() {
        return Err("Invalid input: no valid base32 characters");
    }

    let mut result = Vec::with_capacity(chars.len() * 5 / 8);
    let mut value: u64 = 0;
    let mut bits_in_value: u32 = 0;

    for &byte in &chars {
        let decoded_value = get_base32_value(byte);
        if decoded_value < 0 {
            return Err("Invalid base32 character found");
        }
        
        value = (value << 5) | (decoded_value as u64);
        bits_in_value += 5;

        if bits_in_value >= 8 {
            bits_in_value -= 8;
            result.push(((value >> bits_in_value) & 0xFF) as u8);
        }
    }

    Ok(result)
}

/// Decodes base32 string ignoring padding and whitespace.
pub fn decode_nopad(input: &str) -> Result<Vec<u8>, &'static str> {
    decode(input)
}

/// Validates if a string is valid base32.
pub fn is_valid(input: &str) -> bool {
    let input = input.trim().to_uppercase();
    
    if input.is_empty() {
        return true;
    }

    let chars: Vec<char> = input.chars().collect();
    
    // Find first padding position (if any)
    let first_padding = chars.iter().position(|&c| c == '=');
    
    // Check all characters are valid
    for &c in &chars {
        let value = get_base32_value(c as u8);
        if value < 0 && c != '=' {
            return false;
        }
    }
    
    // If padding exists, verify its placement
    if let Some(first_pad_idx) = first_padding {
        // All remaining chars must be padding
        if chars[first_pad_idx..].iter().any(|&c| c != '=') {
            return false;
        }
        // Padding position must be valid (indices 6 or 7 within a block, or at end)
        let valid_padding = first_pad_idx == 6 || first_pad_idx == 7 
            || first_pad_idx == (8 + 6) || first_pad_idx == (8 + 7)
            || first_pad_idx >= chars.len() - 2;
        if !valid_padding && first_pad_idx > 7 {
            return false;
        }
    }

    true
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_encode_basic() {
        // RFC 4648 test vectors (corrected)
        assert_eq!(encode(b""), "");
        assert_eq!(encode(b"f"), "MY======");
        assert_eq!(encode(b"fo"), "MZXQ====");
        assert_eq!(encode(b"foo"), "MZXW6===");
        assert_eq!(encode(b"foob"), "MZXW6YQ=");
        assert_eq!(encode(b"fooba"), "MZXW6YTB");
        assert_eq!(encode(b"foobar"), "MZXW6YTBOI======");
    }

    #[test]
    fn test_encode_hello() {
        assert_eq!(encode(b"Hello, World!"), "JBSWY3DPFQQFO33SNRSCC===");
    }

    #[test]
    fn test_encode_nopad() {
        assert_eq!(encode_nopad(b"f"), "MY");
        assert_eq!(encode_nopad(b"fo"), "MZXQ");
        assert_eq!(encode_nopad(b"foo"), "MZXW6");
        assert_eq!(encode_nopad(b"foob"), "MZXW6YQ");
        assert_eq!(encode_nopad(b"fooba"), "MZXW6YTB");
        assert_eq!(encode_nopad(b"foobar"), "MZXW6YTBOI");
    }

    #[test]
    fn test_decode_basic() {
        assert_eq!(decode("").unwrap(), b"");
        assert_eq!(decode("MY======").unwrap(), b"f");
        assert_eq!(decode("MZXQ====").unwrap(), b"fo");
        assert_eq!(decode("MZXW6===").unwrap(), b"foo");
        assert_eq!(decode("MZXW6YQ=").unwrap(), b"foob");
        assert_eq!(decode("MZXW6YTB").unwrap(), b"fooba");
        assert_eq!(decode("MZXW6YTBOI======").unwrap(), b"foobar");
    }

    #[test]
    fn test_decode_hello() {
        let result = decode("JBSWY3DPFQQFO33SNRSCC===");
        assert!(result.is_ok());
        assert_eq!(result.unwrap(), b"Hello, World!");
    }

    #[test]
    fn test_decode_lowercase() {
        assert_eq!(decode("mzxq====").unwrap(), b"fo");
    }

    #[test]
    fn test_decode_invalid() {
        assert!(decode("MZXW6YT!!").is_err());
        // Note: 'I' is a valid base32 character, so this decodes (incorrectly)
        assert!(decode("MZXW6YT!!====").is_err());
    }

    #[test]
    fn test_roundtrip() {
        let test_cases = [
            b"" as &[u8],
            b"f",
            b"fo",
            b"foo",
            b"foob",
            b"fooba",
            b"foobar",
            b"Hello, World!",
            b"Base32",
            b"a longer string with more data",
        ];

        for case in test_cases {
            let encoded = encode(case);
            let decoded = decode(&encoded).unwrap();
            assert_eq!(decoded.as_slice(), case, "Roundtrip failed for: {:?}", case);
            
            let encoded_nopad = encode_nopad(case);
            let decoded_nopad = decode(&encoded_nopad).unwrap();
            assert_eq!(decoded_nopad.as_slice(), case, "Roundtrip (nopad) failed for: {:?}", case);
        }
    }

    #[test]
    fn test_is_valid() {
        assert!(is_valid(""));
        assert!(is_valid("MZXQ===="));
        assert!(is_valid("MZXW6YTB"));
        assert!(is_valid("mzxq===="));
        assert!(is_valid("MY"));
        assert!(!is_valid("MZXW6YT!="));
        assert!(!is_valid("=MZXQ===="));
        assert!(!is_valid("MZXW6YT==X"));
    }

    #[test]
    fn test_rfc4648_test_vectors() {
        // RFC 4648 test vectors (corrected)
        assert_eq!(encode(b""), "");
        assert_eq!(encode(b"f"), "MY======");
        assert_eq!(encode(b"fo"), "MZXQ====");
        assert_eq!(encode(b"foo"), "MZXW6===");
        assert_eq!(encode(b"foob"), "MZXW6YQ=");
        assert_eq!(encode(b"fooba"), "MZXW6YTB");
        assert_eq!(encode(b"foobar"), "MZXW6YTBOI======");
    }
}