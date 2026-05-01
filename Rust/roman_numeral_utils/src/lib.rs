//! # Roman Numeral Utils
//! 
//! A zero-dependency library for converting between Arabic numerals and Roman numerals.
//! 
//! ## Features
//! 
//! - Convert integers to Roman numerals (1 to 3,999)
//! - Convert Roman numerals back to integers
//! - Validate Roman numeral strings
//! - Support for standard notation only
//! 
//! ## Example
//! 
//! ```rust
//! use roman_numeral_utils::{to_roman, from_roman, is_valid_roman};
//! 
//! let roman = to_roman(2024).unwrap();
//! assert_eq!(roman, "MMXXIV");
//! 
//! let num = from_roman("MMXXIV").unwrap();
//! assert_eq!(num, 2024);
//! 
//! assert!(is_valid_roman("MMXXIV"));
//! ```

use std::fmt;

/// Error types for Roman numeral operations
#[derive(Debug, Clone, PartialEq)]
pub enum RomanError {
    /// Number is out of valid range (1 to 3,999)
    OutOfRange(i64),
    /// Invalid Roman numeral character
    InvalidCharacter(char),
    /// Invalid Roman numeral format
    InvalidFormat(String),
    /// Empty input string
    EmptyInput,
}

impl fmt::Display for RomanError {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        match self {
            RomanError::OutOfRange(n) => write!(f, "Number {} is out of range (1 to 3,999)", n),
            RomanError::InvalidCharacter(c) => write!(f, "Invalid Roman numeral character: '{}'", c),
            RomanError::InvalidFormat(s) => write!(f, "Invalid Roman numeral format: {}", s),
            RomanError::EmptyInput => write!(f, "Empty input string"),
        }
    }
}

impl std::error::Error for RomanError {}

/// Roman numeral symbols and their values in descending order
const SYMBOLS: [(i64, &str); 13] = [
    (1000, "M"),
    (900, "CM"),
    (500, "D"),
    (400, "CD"),
    (100, "C"),
    (90, "XC"),
    (50, "L"),
    (40, "XL"),
    (10, "X"),
    (9, "IX"),
    (5, "V"),
    (4, "IV"),
    (1, "I"),
];

/// Character values for Roman numerals
const CHAR_VALUES: &[(char, i64)] = &[
    ('I', 1),
    ('V', 5),
    ('X', 10),
    ('L', 50),
    ('C', 100),
    ('D', 500),
    ('M', 1000),
];

/// Convert an integer to a Roman numeral string.
/// 
/// Supports numbers from 1 to 3,999.
/// 
/// # Arguments
/// 
/// * `num` - The integer to convert (must be between 1 and 3,999)
/// 
/// # Returns
/// 
/// * `Ok(String)` - The Roman numeral representation
/// * `Err(RomanError)` - If the number is out of range
/// 
/// # Example
/// 
/// ```rust
/// use roman_numeral_utils::to_roman;
/// 
/// assert_eq!(to_roman(1).unwrap(), "I");
/// assert_eq!(to_roman(4).unwrap(), "IV");
/// assert_eq!(to_roman(2024).unwrap(), "MMXXIV");
/// assert_eq!(to_roman(3999).unwrap(), "MMMCMXCIX");
/// ```
pub fn to_roman(num: i64) -> Result<String, RomanError> {
    if num < 1 || num > 3999 {
        return Err(RomanError::OutOfRange(num));
    }
    
    let mut result = String::new();
    let mut remaining = num;
    
    for (value, symbol) in SYMBOLS {
        while remaining >= value {
            result.push_str(symbol);
            remaining -= value;
        }
    }
    
    Ok(result)
}

/// Convert a Roman numeral string to an integer.
/// 
/// Supports standard Roman numerals (I to MMMCMXCIX, i.e., 1 to 3999).
/// 
/// # Arguments
/// 
/// * `roman` - The Roman numeral string (case-insensitive)
/// 
/// # Returns
/// 
/// * `Ok(i64)` - The integer value
/// * `Err(RomanError)` - If the string is not a valid Roman numeral
/// 
/// # Example
/// 
/// ```rust
/// use roman_numeral_utils::from_roman;
/// 
/// assert_eq!(from_roman("I").unwrap(), 1);
/// assert_eq!(from_roman("IV").unwrap(), 4);
/// assert_eq!(from_roman("MMXXIV").unwrap(), 2024);
/// assert_eq!(from_roman("mmxxiv").unwrap(), 2024); // case-insensitive
/// ```
pub fn from_roman(roman: &str) -> Result<i64, RomanError> {
    let roman = roman.trim();
    
    if roman.is_empty() {
        return Err(RomanError::EmptyInput);
    }
    
    // Convert to uppercase for consistent processing
    let roman_upper = roman.to_uppercase();
    let chars: Vec<char> = roman_upper.chars().collect();
    
    // Check for invalid characters
    for &c in &chars {
        if !CHAR_VALUES.iter().any(|(ch, _)| *ch == c) {
            return Err(RomanError::InvalidCharacter(c));
        }
    }
    
    let mut result: i64 = 0;
    let mut i = 0;
    
    while i < chars.len() {
        let current_val = get_char_value(chars[i]);
        
        if i + 1 < chars.len() {
            let next_val = get_char_value(chars[i + 1]);
            
            if current_val < next_val {
                // Subtractive notation (e.g., IV = 4)
                result += next_val - current_val;
                i += 2;
                continue;
            }
        }
        
        result += current_val;
        i += 1;
    }
    
    // Validate by converting back
    if let Ok(expected) = to_roman(result) {
        if expected != roman_upper {
            // The input might be in non-canonical form
            // Check if it's still valid by counting repetitions
            if !is_valid_format(&roman_upper) {
                return Err(RomanError::InvalidFormat(roman.to_string()));
            }
        }
    }
    
    if result < 1 || result > 3999 {
        return Err(RomanError::OutOfRange(result));
    }
    
    Ok(result)
}

/// Get the value of a single Roman numeral character.
fn get_char_value(c: char) -> i64 {
    CHAR_VALUES
        .iter()
        .find(|(ch, _)| *ch == c)
        .map(|(_, v)| *v)
        .unwrap_or(0)
}

/// Validate a Roman numeral format (checks for invalid repetitions).
fn is_valid_format(roman: &str) -> bool {
    let chars: Vec<char> = roman.chars().collect();
    let mut i = 0;
    
    while i < chars.len() {
        let c = chars[i];
        
        // Count consecutive repeats
        let mut count = 1;
        while i + count < chars.len() && chars[i + count] == c {
            count += 1;
        }
        
        // Check repeat rules
        match c {
            'I' | 'X' | 'C' | 'M' => {
                if count > 3 {
                    return false;
                }
            }
            'V' | 'L' | 'D' => {
                if count > 1 {
                    return false;
                }
            }
            _ => {}
        }
        
        // Check for invalid subtractive combinations
        if count == 1 && i + 1 < chars.len() {
            let next = chars[i + 1];
            if get_char_value(c) < get_char_value(next) {
                // Check valid subtractive pairs
                match (c, next) {
                    ('I', 'V') | ('I', 'X') => {}
                    ('X', 'L') | ('X', 'C') => {}
                    ('C', 'D') | ('C', 'M') => {}
                    _ => return false,
                }
            }
        }
        
        i += count;
    }
    
    true
}

/// Check if a string is a valid Roman numeral.
/// 
/// # Arguments
/// 
/// * `roman` - The string to validate
/// 
/// # Returns
/// 
/// * `true` if the string is a valid Roman numeral
/// * `false` otherwise
/// 
/// # Example
/// 
/// ```rust
/// use roman_numeral_utils::is_valid_roman;
/// 
/// assert!(is_valid_roman("MMXXIV"));
/// assert!(is_valid_roman("iv"));
/// assert!(!is_valid_roman("IIII"));  // Invalid: too many I's
/// assert!(!is_valid_roman("VV"));    // Invalid: V cannot repeat
/// ```
pub fn is_valid_roman(roman: &str) -> bool {
    from_roman(roman).is_ok()
}

/// Convert an integer to a Roman numeral with lowercase output.
/// 
/// # Example
/// 
/// ```rust
/// use roman_numeral_utils::to_roman_lowercase;
/// 
/// assert_eq!(to_roman_lowercase(2024).unwrap(), "mmxxiv");
/// ```
pub fn to_roman_lowercase(num: i64) -> Result<String, RomanError> {
    to_roman(num).map(|s| s.to_lowercase())
}

/// Get a list of all Roman numeral symbols and their values.
/// 
/// Useful for educational purposes or for building custom formatters.
/// 
/// # Example
/// 
/// ```rust
/// use roman_numeral_utils::get_symbols;
/// 
/// let symbols = get_symbols();
/// assert!(symbols.iter().any(|(v, s)| *v == 1000 && *s == "M"));
/// ```
pub fn get_symbols() -> Vec<(i64, &'static str)> {
    SYMBOLS.to_vec()
}

/// Convert a range of numbers to Roman numerals and return as a map.
/// 
/// # Example
/// 
/// ```rust
/// use roman_numeral_utils::to_roman_range;
/// 
/// let range = to_roman_range(1, 10).unwrap();
/// assert_eq!(range.get(&1), Some(&"I".to_string()));
/// assert_eq!(range.get(&10), Some(&"X".to_string()));
/// ```
pub fn to_roman_range(start: i64, end: i64) -> Result<std::collections::HashMap<i64, String>, RomanError> {
    if start < 1 || end > 3999 || start > end {
        return Err(RomanError::OutOfRange(start));
    }
    
    let mut result = std::collections::HashMap::new();
    for n in start..=end {
        result.insert(n, to_roman(n)?);
    }
    
    Ok(result)
}

/// Generate all Roman numerals for a given number of digits.
/// 
/// # Example
/// 
/// ```rust
/// use roman_numeral_utils::generate_ones;
/// 
/// let ones = generate_ones();
/// assert_eq!(ones.get(&1), Some(&"I".to_string()));
/// assert_eq!(ones.get(&9), Some(&"IX".to_string()));
/// ```
pub fn generate_ones() -> std::collections::HashMap<u32, String> {
    let mut result = std::collections::HashMap::new();
    for n in 1..=9 {
        if let Ok(roman) = to_roman(n as i64) {
            result.insert(n, roman);
        }
    }
    result
}

/// Generate tens place Roman numerals (10-90).
pub fn generate_tens() -> std::collections::HashMap<u32, String> {
    let mut result = std::collections::HashMap::new();
    for n in (10..=90).step_by(10) {
        if let Ok(roman) = to_roman(n as i64) {
            result.insert(n, roman);
        }
    }
    result
}

/// Generate hundreds place Roman numerals (100-900).
pub fn generate_hundreds() -> std::collections::HashMap<u32, String> {
    let mut result = std::collections::HashMap::new();
    for n in (100..=900).step_by(100) {
        if let Ok(roman) = to_roman(n as i64) {
            result.insert(n, roman);
        }
    }
    result
}

/// Generate thousands place Roman numerals (1000-3000).
pub fn generate_thousands() -> std::collections::HashMap<u32, String> {
    let mut result = std::collections::HashMap::new();
    for n in (1000..=3000).step_by(1000) {
        if let Ok(roman) = to_roman(n as i64) {
            result.insert(n, roman);
        }
    }
    result
}

#[cfg(test)]
mod tests {
    use super::*;
    
    #[test]
    fn test_to_roman_basic() {
        assert_eq!(to_roman(1).unwrap(), "I");
        assert_eq!(to_roman(4).unwrap(), "IV");
        assert_eq!(to_roman(5).unwrap(), "V");
        assert_eq!(to_roman(9).unwrap(), "IX");
        assert_eq!(to_roman(10).unwrap(), "X");
        assert_eq!(to_roman(40).unwrap(), "XL");
        assert_eq!(to_roman(50).unwrap(), "L");
        assert_eq!(to_roman(90).unwrap(), "XC");
        assert_eq!(to_roman(100).unwrap(), "C");
        assert_eq!(to_roman(400).unwrap(), "CD");
        assert_eq!(to_roman(500).unwrap(), "D");
        assert_eq!(to_roman(900).unwrap(), "CM");
        assert_eq!(to_roman(1000).unwrap(), "M");
    }
    
    #[test]
    fn test_to_roman_complex() {
        assert_eq!(to_roman(2024).unwrap(), "MMXXIV");
        assert_eq!(to_roman(1987).unwrap(), "MCMLXXXVII");
        assert_eq!(to_roman(3999).unwrap(), "MMMCMXCIX");
        assert_eq!(to_roman(1776).unwrap(), "MDCCLXXVI");
        assert_eq!(to_roman(1492).unwrap(), "MCDXCII");
    }
    
    #[test]
    fn test_to_roman_edge_cases() {
        assert!(to_roman(0).is_err());
        assert!(to_roman(-1).is_err());
        assert!(to_roman(4000).is_err());
        assert!(to_roman(10000).is_err());
    }
    
    #[test]
    fn test_from_roman_basic() {
        assert_eq!(from_roman("I").unwrap(), 1);
        assert_eq!(from_roman("IV").unwrap(), 4);
        assert_eq!(from_roman("V").unwrap(), 5);
        assert_eq!(from_roman("IX").unwrap(), 9);
        assert_eq!(from_roman("X").unwrap(), 10);
        assert_eq!(from_roman("XL").unwrap(), 40);
        assert_eq!(from_roman("L").unwrap(), 50);
        assert_eq!(from_roman("XC").unwrap(), 90);
        assert_eq!(from_roman("C").unwrap(), 100);
        assert_eq!(from_roman("CD").unwrap(), 400);
        assert_eq!(from_roman("D").unwrap(), 500);
        assert_eq!(from_roman("CM").unwrap(), 900);
        assert_eq!(from_roman("M").unwrap(), 1000);
    }
    
    #[test]
    fn test_from_roman_complex() {
        assert_eq!(from_roman("MMXXIV").unwrap(), 2024);
        assert_eq!(from_roman("MCMLXXXVII").unwrap(), 1987);
        assert_eq!(from_roman("MMMCMXCIX").unwrap(), 3999);
        assert_eq!(from_roman("MDCCLXXVI").unwrap(), 1776);
        assert_eq!(from_roman("MCDXCII").unwrap(), 1492);
    }
    
    #[test]
    fn test_from_roman_case_insensitive() {
        assert_eq!(from_roman("mmxxiv").unwrap(), 2024);
        assert_eq!(from_roman("MmXxIv").unwrap(), 2024);
        assert_eq!(from_roman("  MMXXIV  ").unwrap(), 2024);
    }
    
    #[test]
    fn test_from_roman_invalid() {
        assert!(from_roman("").is_err());
        assert!(from_roman("   ").is_err());
        assert!(from_roman("ABC").is_err());
        assert!(from_roman("IIII").is_err());
        assert!(from_roman("VV").is_err());
        assert!(from_roman("LL").is_err());
        assert!(from_roman("DD").is_err());
    }
    
    #[test]
    fn test_roundtrip() {
        for num in [1, 4, 9, 40, 90, 400, 900, 1000, 2024, 3999] {
            let roman = to_roman(num).unwrap();
            let back = from_roman(&roman).unwrap();
            assert_eq!(num, back, "Roundtrip failed for {}", num);
        }
    }
    
    #[test]
    fn test_is_valid_roman() {
        assert!(is_valid_roman("MMXXIV"));
        assert!(is_valid_roman("iv"));
        assert!(is_valid_roman("MMMCMXCIX"));
        assert!(!is_valid_roman("IIII"));
        assert!(!is_valid_roman("VV"));
        assert!(!is_valid_roman("LL"));
        assert!(!is_valid_roman(""));
    }
    
    #[test]
    fn test_to_roman_lowercase() {
        assert_eq!(to_roman_lowercase(2024).unwrap(), "mmxxiv");
        assert_eq!(to_roman_lowercase(3999).unwrap(), "mmmcmxcix");
    }
    
    #[test]
    fn test_get_symbols() {
        let symbols = get_symbols();
        assert!(!symbols.is_empty());
        assert!(symbols.iter().any(|(v, s)| *v == 1000 && *s == "M"));
        assert!(symbols.iter().any(|(v, s)| *v == 900 && *s == "CM"));
    }
    
    #[test]
    fn test_to_roman_range() {
        let range = to_roman_range(1, 10).unwrap();
        assert_eq!(range.get(&1), Some(&"I".to_string()));
        assert_eq!(range.get(&5), Some(&"V".to_string()));
        assert_eq!(range.get(&10), Some(&"X".to_string()));
    }
    
    #[test]
    fn test_generate_ones() {
        let ones = generate_ones();
        assert_eq!(ones.get(&1), Some(&"I".to_string()));
        assert_eq!(ones.get(&4), Some(&"IV".to_string()));
        assert_eq!(ones.get(&9), Some(&"IX".to_string()));
    }
    
    #[test]
    fn test_famous_years() {
        // Famous historical years
        assert_eq!(to_roman(1066).unwrap(), "MLXVI");  // Battle of Hastings
        assert_eq!(to_roman(1215).unwrap(), "MCCXV");  // Magna Carta
        assert_eq!(to_roman(1776).unwrap(), "MDCCLXXVI");  // US Independence
        assert_eq!(to_roman(1789).unwrap(), "MDCCLXXXIX");  // French Revolution
        assert_eq!(to_roman(1945).unwrap(), "MCMXLV");  // End of WWII
        assert_eq!(to_roman(2000).unwrap(), "MM");  // New Millennium
    }
    
    #[test]
    fn test_all_numbers() {
        // Test all numbers from 1 to 3999
        for n in 1..=3999 {
            let roman = to_roman(n).expect(&format!("Failed to convert {}", n));
            let back = from_roman(&roman).expect(&format!("Failed to parse {}", roman));
            assert_eq!(n, back, "Roundtrip failed for {}", n);
        }
    }
    
    #[test]
    fn test_error_messages() {
        match to_roman(0) {
            Err(RomanError::OutOfRange(n)) => assert_eq!(n, 0),
            _ => panic!("Expected OutOfRange error"),
        }
        
        match from_roman("") {
            Err(RomanError::EmptyInput) => {}
            _ => panic!("Expected EmptyInput error"),
        }
        
        match from_roman("ABC") {
            Err(RomanError::InvalidCharacter(c)) => assert_eq!(c, 'A'),
            _ => panic!("Expected InvalidCharacter error"),
        }
    }
}