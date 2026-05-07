//! ISBN Utilities Library
//! 
//! A comprehensive library for working with ISBN-10 and ISBN-13 identifiers.
//! 
//! # Features
//! - Validate ISBN-10 and ISBN-13
//! - Generate valid ISBNs
//! - Format ISBNs with hyphens
//! - Parse ISBNs from strings
//! - Convert between ISBN-10 and ISBN-13

mod isbn10;
mod isbn13;

pub use isbn10::ISBN10;
pub use isbn13::ISBN13;

use std::fmt;
use std::str::FromStr;

/// Represents an ISBN that can be either ISBN-10 or ISBN-13
#[derive(Debug, Clone, PartialEq, Eq)]
pub enum ISBN {
    ISBN10(ISBN10),
    ISBN13(ISBN13),
}

impl ISBN {
    /// Create a new ISBN from a string
    pub fn new(s: &str) -> Result<Self, ISBNError> {
        let cleaned: String = s.chars().filter(|c| c.is_ascii_digit() || *c == 'X' || *c == 'x').collect();
        
        match cleaned.len() {
            10 => Ok(ISBN::ISBN10(ISBN10::from_str(&cleaned)?)),
            13 => Ok(ISBN::ISBN13(ISBN13::from_str(&cleaned)?)),
            _ => Err(ISBNError::InvalidLength(cleaned.len())),
        }
    }
    
    /// Check if this is a valid ISBN
    pub fn is_valid(&self) -> bool {
        match self {
            ISBN::ISBN10(isbn) => isbn.is_valid(),
            ISBN::ISBN13(isbn) => isbn.is_valid(),
        }
    }
    
    /// Convert to ISBN-13 format
    pub fn to_isbn13(&self) -> ISBN {
        match self {
            ISBN::ISBN10(isbn) => ISBN::ISBN13(isbn.to_isbn13()),
            ISBN::ISBN13(isbn) => ISBN::ISBN13(isbn.clone()),
        }
    }
    
    /// Convert to ISBN-10 if possible (only works for 978 prefix)
    pub fn to_isbn10(&self) -> Option<ISBN> {
        match self {
            ISBN::ISBN10(isbn) => Some(ISBN::ISBN10(isbn.clone())),
            ISBN::ISBN13(isbn) => isbn.to_isbn10().map(ISBN::ISBN10),
        }
    }
    
    /// Format with hyphens
    pub fn format(&self) -> String {
        match self {
            ISBN::ISBN10(isbn) => isbn.format(),
            ISBN::ISBN13(isbn) => isbn.format(),
        }
    }
    
    /// Get the raw digits as a string
    pub fn digits(&self) -> String {
        match self {
            ISBN::ISBN10(isbn) => isbn.digits(),
            ISBN::ISBN13(isbn) => isbn.digits(),
        }
    }
}

impl fmt::Display for ISBN {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        match self {
            ISBN::ISBN10(isbn) => write!(f, "{}", isbn),
            ISBN::ISBN13(isbn) => write!(f, "{}", isbn),
        }
    }
}

impl FromStr for ISBN {
    type Err = ISBNError;
    
    fn from_str(s: &str) -> Result<Self, Self::Err> {
        ISBN::new(s)
    }
}

/// Errors that can occur when working with ISBNs
#[derive(Debug, Clone, PartialEq, Eq)]
pub enum ISBNError {
    InvalidLength(usize),
    InvalidCharacters,
    InvalidChecksum,
    InvalidPrefix,
    CannotConvertToISBN10,
}

impl fmt::Display for ISBNError {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        match self {
            ISBNError::InvalidLength(len) => write!(f, "Invalid ISBN length: {} (expected 10 or 13)", len),
            ISBNError::InvalidCharacters => write!(f, "ISBN contains invalid characters"),
            ISBNError::InvalidChecksum => write!(f, "Invalid ISBN checksum"),
            ISBNError::InvalidPrefix => write!(f, "Invalid ISBN-13 prefix (must be 978 or 979)"),
            ISBNError::CannotConvertToISBN10 => write!(f, "Cannot convert to ISBN-10 (only 978 prefix supported)"),
        }
    }
}

impl std::error::Error for ISBNError {}

/// Generate a random valid ISBN-13
pub fn generate_isbn13() -> ISBN13 {
    ISBN13::generate()
}

/// Generate a random valid ISBN-10
pub fn generate_isbn10() -> ISBN10 {
    ISBN10::generate()
}

/// Validate an ISBN string
pub fn validate(s: &str) -> Result<ISBN, ISBNError> {
    ISBN::new(s)
}

#[cfg(test)]
mod tests {
    use super::*;
    
    #[test]
    fn test_isbn10_validation() {
        // Valid ISBN-10
        assert!(ISBN::new("0-306-40615-2").unwrap().is_valid());
        assert!(ISBN::new("0306406152").unwrap().is_valid());
        assert!(ISBN::new("0-19-852663-6").unwrap().is_valid());
        
        // ISBN-10 with X
        assert!(ISBN::new("0-8044-2957-X").unwrap().is_valid());
    }
    
    #[test]
    fn test_isbn13_validation() {
        // Valid ISBN-13
        assert!(ISBN::new("978-0-306-40615-7").unwrap().is_valid());
        assert!(ISBN::new("9780306406157").unwrap().is_valid());
        assert!(ISBN::new("978-1-86092-049-3").unwrap().is_valid());
    }
    
    #[test]
    fn test_isbn10_to_isbn13() {
        let isbn10 = ISBN::new("0-306-40615-2").unwrap();
        let isbn13 = isbn10.to_isbn13();
        assert_eq!(isbn13.digits(), "9780306406157");
    }
    
    #[test]
    fn test_isbn13_to_isbn10() {
        let isbn13 = ISBN::new("978-0-306-40615-7").unwrap();
        let isbn10 = isbn13.to_isbn10().unwrap();
        assert_eq!(isbn10.digits(), "0306406152");
    }
    
    #[test]
    fn test_invalid_isbn() {
        assert!(ISBN::new("invalid").is_err());
        assert!(ISBN::new("12345").is_err());
        assert!(ISBN::new("9780306406158").is_err()); // Wrong checksum
        assert!(ISBN::new("0306406153").is_err()); // Wrong checksum ISBN-10
    }
    
    #[test]
    fn test_generate() {
        let isbn10 = generate_isbn10();
        assert!(isbn10.is_valid());
        
        let isbn13 = generate_isbn13();
        assert!(isbn13.is_valid());
    }
}