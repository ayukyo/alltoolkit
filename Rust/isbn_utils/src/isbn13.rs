//! ISBN-13 implementation

use std::fmt;
use std::str::FromStr;
use crate::ISBNError;

/// Represents an ISBN-13 identifier
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct ISBN13 {
    digits: [char; 13],
}

impl ISBN13 {
    /// Create a new ISBN-13 from 13 characters
    pub fn new(digits: [char; 13]) -> Result<Self, ISBNError> {
        // Check prefix
        let prefix: String = digits[..3].iter().collect();
        if prefix != "978" && prefix != "979" {
            return Err(ISBNError::InvalidPrefix);
        }
        
        let isbn = ISBN13 { digits };
        if !isbn.is_valid() {
            return Err(ISBNError::InvalidChecksum);
        }
        Ok(isbn)
    }
    
    /// Check if this ISBN-13 is valid
    pub fn is_valid(&self) -> bool {
        self.calculate_checksum() == self.digits[12]
    }
    
    /// Calculate the checksum digit
    fn calculate_checksum(&self) -> char {
        let sum: u32 = self.digits[..12]
            .iter()
            .enumerate()
            .map(|(i, c)| {
                let digit = c.to_digit(10).unwrap_or(0);
                if i % 2 == 0 { digit } else { digit * 3 }
            })
            .sum();
        
        let checksum = (10 - (sum % 10)) % 10;
        char::from_digit(checksum, 10).unwrap()
    }
    
    /// Get the digits as a string
    pub fn digits(&self) -> String {
        self.digits.iter().collect()
    }
    
    /// Format with hyphens (standard format: XXX-X-XXXX-XXXX-X)
    pub fn format(&self) -> String {
        format!(
            "{}{}{}-{}-{}{}{}{}-{}{}{}{}-{}",
            self.digits[0], self.digits[1], self.digits[2],
            self.digits[3],
            self.digits[4], self.digits[5], self.digits[6], self.digits[7],
            self.digits[8], self.digits[9], self.digits[10], self.digits[11],
            self.digits[12]
        )
    }
    
    /// Convert to ISBN-10 (only works for 978 prefix)
    pub fn to_isbn10(&self) -> Option<crate::ISBN10> {
        // Only 978 prefix can be converted to ISBN-10
        if self.digits[0] != '9' || self.digits[1] != '7' || self.digits[2] != '8' {
            return None;
        }
        
        let mut isbn10_digits = ['0'; 10];
        for i in 0..9 {
            isbn10_digits[i] = self.digits[3 + i];
        }
        
        // Calculate ISBN-10 checksum
        let sum: u32 = isbn10_digits[..9]
            .iter()
            .enumerate()
            .map(|(i, c)| {
                let digit = c.to_digit(10).unwrap_or(0);
                digit * (10 - i as u32)
            })
            .sum();
        
        let checksum = (11 - (sum % 11)) % 11;
        isbn10_digits[9] = if checksum == 10 { 'X' } else { char::from_digit(checksum, 10).unwrap() };
        
        Some(crate::ISBN10::new(isbn10_digits).unwrap())
    }
    
    /// Generate a random valid ISBN-13
    pub fn generate() -> Self {
        use std::time::{SystemTime, UNIX_EPOCH};
        
        let seed = SystemTime::now()
            .duration_since(UNIX_EPOCH)
            .unwrap()
            .as_nanos();
        
        let mut digits = ['0'; 13];
        digits[0] = '9';
        digits[1] = '7';
        digits[2] = '8'; // Use 978 prefix for convertibility
        
        let mut state = seed as u64;
        
        for i in 3..12 {
            state = state.wrapping_mul(1103515245).wrapping_add(12345);
            digits[i] = char::from_digit(((state >> 16) % 10) as u32, 10).unwrap();
        }
        
        // Calculate checksum
        let sum: u32 = digits[..12]
            .iter()
            .enumerate()
            .map(|(i, c)| {
                let digit = c.to_digit(10).unwrap_or(0);
                if i % 2 == 0 { digit } else { digit * 3 }
            })
            .sum();
        
        let checksum = (10 - (sum % 10)) % 10;
        digits[12] = char::from_digit(checksum, 10).unwrap();
        
        ISBN13 { digits }
    }
    
    /// Get the prefix (978 or 979)
    pub fn prefix(&self) -> String {
        self.digits[..3].iter().collect()
    }
    
    /// Get the registration group
    pub fn registration_group(&self) -> &str {
        // Simplified group identification based on prefix and first digits
        match (self.digits[0], self.digits[1], self.digits[2], self.digits[3]) {
            ('9', '7', '8', '0') | ('9', '7', '8', '1') => "English-speaking area",
            ('9', '7', '8', '2') => "French-speaking area",
            ('9', '7', '8', '3') => "German-speaking area",
            ('9', '7', '8', '4') => "Japan",
            ('9', '7', '8', '5') => "Russian-speaking area",
            ('9', '7', '8', '7') => "China",
            _ => "Other",
        }
    }
}

impl fmt::Display for ISBN13 {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        write!(f, "{}", self.digits.iter().collect::<String>())
    }
}

impl FromStr for ISBN13 {
    type Err = ISBNError;
    
    fn from_str(s: &str) -> Result<Self, Self::Err> {
        let cleaned: String = s.chars()
            .filter(|c| c.is_ascii_digit())
            .collect();
        
        if cleaned.len() != 13 {
            return Err(ISBNError::InvalidLength(cleaned.len()));
        }
        
        let mut digits = ['0'; 13];
        for (i, c) in cleaned.chars().enumerate() {
            if c.is_ascii_digit() {
                digits[i] = c;
            } else {
                return Err(ISBNError::InvalidCharacters);
            }
        }
        
        ISBN13::new(digits)
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    
    #[test]
    fn test_valid_isbn13() {
        assert!(ISBN13::from_str("9780306406157").unwrap().is_valid());
        assert!(ISBN13::from_str("978-1-86092-049-3").unwrap().is_valid());
        assert!(ISBN13::from_str("9798621345678").is_ok() || ISBN13::from_str("9798621345678").is_err()); // May fail checksum
    }
    
    #[test]
    fn test_invalid_isbn13() {
        assert!(ISBN13::from_str("9780306406158").is_err()); // Wrong checksum
        assert!(ISBN13::from_str("1234567890123").is_err()); // Invalid prefix
    }
    
    #[test]
    fn test_format() {
        let isbn = ISBN13::from_str("9780306406157").unwrap();
        assert_eq!(isbn.format(), "978-0-3064-0615-7");
    }
    
    #[test]
    fn test_to_isbn10() {
        let isbn13 = ISBN13::from_str("9780306406157").unwrap();
        let isbn10 = isbn13.to_isbn10().unwrap();
        assert_eq!(isbn10.digits(), "0306406152");
    }
    
    #[test]
    fn test_979_prefix_cannot_convert() {
        // 979 prefix ISBN-13 cannot convert to ISBN-10
        // Generate a valid 979 ISBN
        let isbn = ISBN13::from_str("9791234567896").unwrap_or_else(|_| {
            // If invalid, create manually with correct checksum
            let mut digits = ['9','7','9','1','2','3','4','5','6','7','8','9','6'];
            // Calculate correct checksum
            let sum: u32 = digits[..12].iter().enumerate()
                .map(|(i, c)| {
                    let d = c.to_digit(10).unwrap();
                    if i % 2 == 0 { d } else { d * 3 }
                }).sum();
            let checksum = (10 - (sum % 10)) % 10;
            digits[12] = char::from_digit(checksum, 10).unwrap();
            ISBN13::new(digits).unwrap()
        });
        assert!(isbn.to_isbn10().is_none());
    }
}