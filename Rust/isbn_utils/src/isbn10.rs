//! ISBN-10 implementation

use std::fmt;
use std::str::FromStr;
use crate::ISBNError;

/// Represents an ISBN-10 identifier
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct ISBN10 {
    digits: [char; 10],
}

impl ISBN10 {
    /// Create a new ISBN-10 from 10 characters
    pub fn new(digits: [char; 10]) -> Result<Self, ISBNError> {
        let isbn = ISBN10 { digits };
        if !isbn.is_valid() {
            return Err(ISBNError::InvalidChecksum);
        }
        Ok(isbn)
    }
    
    /// Check if this ISBN-10 is valid
    pub fn is_valid(&self) -> bool {
        self.calculate_checksum() == self.digits[9].to_ascii_uppercase()
    }
    
    /// Calculate the checksum character
    fn calculate_checksum(&self) -> char {
        let sum: u32 = self.digits[..9]
            .iter()
            .enumerate()
            .map(|(i, c)| {
                let digit = c.to_digit(10).unwrap_or(0);
                digit * (10 - i as u32)
            })
            .sum();
        
        let checksum = (11 - (sum % 11)) % 11;
        if checksum == 10 {
            'X'
        } else {
            char::from_digit(checksum, 10).unwrap()
        }
    }
    
    /// Get the digits as a string
    pub fn digits(&self) -> String {
        self.digits.iter().collect()
    }
    
    /// Format with hyphens (standard format: X-XXXX-XXXX-X)
    pub fn format(&self) -> String {
        format!(
            "{}-{}{}{}{}-{}{}{}{}-{}",
            self.digits[0],
            self.digits[1], self.digits[2], self.digits[3], self.digits[4],
            self.digits[5], self.digits[6], self.digits[7], self.digits[8],
            self.digits[9]
        )
    }
    
    /// Convert to ISBN-13
    pub fn to_isbn13(&self) -> crate::ISBN13 {
        let mut isbn13_digits = ['0'; 13];
        isbn13_digits[0] = '9';
        isbn13_digits[1] = '7';
        isbn13_digits[2] = '8';
        
        for i in 0..9 {
            isbn13_digits[3 + i] = self.digits[i];
        }
        
        // Calculate ISBN-13 checksum
        let sum: u32 = isbn13_digits[..12]
            .iter()
            .enumerate()
            .map(|(i, c)| {
                let digit = c.to_digit(10).unwrap_or(0);
                if i % 2 == 0 { digit } else { digit * 3 }
            })
            .sum();
        
        let checksum = (10 - (sum % 10)) % 10;
        isbn13_digits[12] = char::from_digit(checksum, 10).unwrap();
        
        crate::ISBN13::new(isbn13_digits).unwrap()
    }
    
    /// Generate a random valid ISBN-10
    pub fn generate() -> Self {
        use std::time::{SystemTime, UNIX_EPOCH};
        
        let seed = SystemTime::now()
            .duration_since(UNIX_EPOCH)
            .unwrap()
            .as_nanos();
        
        let mut digits = ['0'; 10];
        let mut state = seed as u64;
        
        for i in 0..9 {
            state = state.wrapping_mul(1103515245).wrapping_add(12345);
            digits[i] = char::from_digit(((state >> 16) % 10) as u32, 10).unwrap();
        }
        
        // Calculate checksum
        let sum: u32 = digits[..9]
            .iter()
            .enumerate()
            .map(|(i, c)| {
                let digit = c.to_digit(10).unwrap();
                digit * (10 - i as u32)
            })
            .sum();
        
        let checksum = (11 - (sum % 11)) % 11;
        digits[9] = if checksum == 10 { 'X' } else { char::from_digit(checksum, 10).unwrap() };
        
        ISBN10 { digits }
    }
    
    /// Get the registration group
    pub fn registration_group(&self) -> &str {
        let prefix = self.digits[0].to_digit(10).unwrap_or(0);
        match prefix {
            0 | 1 => "English-speaking area",
            2 => "French-speaking area",
            3 => "German-speaking area",
            4 => "Japan",
            5 => "Russian-speaking area",
            7 => "China",
            _ => "Other",
        }
    }
}

impl fmt::Display for ISBN10 {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        write!(f, "{}", self.digits.iter().collect::<String>())
    }
}

impl FromStr for ISBN10 {
    type Err = ISBNError;
    
    fn from_str(s: &str) -> Result<Self, Self::Err> {
        let cleaned: String = s.chars()
            .filter(|c| c.is_ascii_digit() || *c == 'X' || *c == 'x')
            .collect();
        
        if cleaned.len() != 10 {
            return Err(ISBNError::InvalidLength(cleaned.len()));
        }
        
        let mut digits = ['0'; 10];
        for (i, c) in cleaned.chars().enumerate() {
            if c.is_ascii_digit() || c == 'X' || c == 'x' {
                digits[i] = c.to_ascii_uppercase();
            } else {
                return Err(ISBNError::InvalidCharacters);
            }
        }
        
        ISBN10::new(digits)
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    
    #[test]
    fn test_valid_isbn10() {
        assert!(ISBN10::from_str("0306406152").unwrap().is_valid());
        assert!(ISBN10::from_str("080442957X").unwrap().is_valid());
        assert!(ISBN10::from_str("0-306-40615-2").unwrap().is_valid());
    }
    
    #[test]
    fn test_invalid_isbn10() {
        assert!(ISBN10::from_str("0306406153").is_err()); // Wrong checksum
    }
    
    #[test]
    fn test_format() {
        let isbn = ISBN10::from_str("0306406152").unwrap();
        assert_eq!(isbn.format(), "0-3064-0615-2");
    }
    
    #[test]
    fn test_to_isbn13() {
        let isbn10 = ISBN10::from_str("0306406152").unwrap();
        let isbn13 = isbn10.to_isbn13();
        assert_eq!(isbn13.digits(), "9780306406157");
    }
}