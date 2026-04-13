//! # Validation Utilities
//! 
//! A comprehensive collection of data validation utilities for Rust.
//! All functions are pure (no side effects), zero-dependency, and suitable for production use.
//!
//! ## Features
//!
//! - Email validation (RFC 5321/5322 compliant)
//! - URL validation (http/https)
//! - Phone number validation (international format)
//! - Credit card validation (Luhn algorithm)
//! - IP address validation (IPv4/IPv6)
//! - Password strength validation
//! - Credit card type detection
//! - ISBN validation
//!
//! ## Usage
//!
//! ```rust
//! use validation_utils::{
//!     is_valid_email, is_valid_url, is_valid_phone, 
//!     is_valid_credit_card, is_valid_ipv4, is_valid_ipv6,
//!     PasswordStrength, validate_password_strength
//! };
//!
//! assert!(is_valid_email("user@example.com"));
//! assert!(is_valid_url("https://example.com"));
//! assert!(is_valid_phone("+1-555-123-4567"));
//! assert!(is_valid_credit_card("4532015112830366")); // Visa test card
//! assert!(is_valid_ipv4("192.168.1.1"));
//! assert!(is_valid_ipv6("::1"));
//! ```

/// Validates an email address according to RFC 5321/5322.
///
/// Performs comprehensive validation including:
/// - Presence of exactly one @ symbol
/// - Non-empty local part (before @) with valid characters
/// - Non-empty domain part (after @) with valid structure
/// - Domain contains at least one dot
/// - No spaces or control characters
/// - Local part length <= 64 characters (RFC 5321)
/// - Total length <= 254 characters (RFC 5321)
/// - Domain labels 1-63 characters (RFC 1035)
///
/// # Parameters
///
/// * `email` - The email address to validate
///
/// # Returns
///
/// * `true` if the email passes validation, `false` otherwise
///
/// # Examples
///
/// ```
/// assert!(is_valid_email("user@example.com"));
/// assert!(is_valid_email("user.name+tag@sub.domain.co.uk"));
/// assert!(!is_valid_email("invalid.email"));
/// assert!(!is_valid_email("user@"));
/// assert!(!is_valid_email("@example.com"));
/// ```
pub fn is_valid_email(email: &str) -> bool {
    const MAX_LOCAL_LEN: usize = 64;
    const MAX_TOTAL_LEN: usize = 254;
    const MAX_LABEL_LEN: usize = 63;
    
    let len = email.len();
    if len == 0 || len > MAX_TOTAL_LEN {
        return false;
    }

    let bytes = email.as_bytes();
    let mut at_count = 0;
    let mut at_pos = 0;
    let mut last_dot_pos: Option<usize> = None;

    for (i, &b) in bytes.iter().enumerate() {
        if b == b'@' {
            if i > MAX_LOCAL_LEN || i == 0 {
                return false;
            }
            at_count += 1;
            at_pos = i;
            if at_count > 1 {
                return false;
            }
            continue;
        }
        
        if b == b'.' && at_count == 1 {
            if last_dot_pos == Some(i - 1) {
                return false;
            }
            if let Some(last_dot) = last_dot_pos {
                if i - last_dot - 1 > MAX_LABEL_LEN {
                    return false;
                }
            } else if i - at_pos - 1 > MAX_LABEL_LEN {
                return false;
            }
            last_dot_pos = Some(i);
        }
        
        // Check for invalid characters
        if b <= b' ' || matches!(b, b'(' | b')' | b'<' | b'>' | b',' | b';' | b':' | b'\\' | b'"') {
            return false;
        }
    }

    if at_count != 1 {
        return false;
    }

    let domain = &email[at_pos + 1..];
    let domain_len = domain.len();
    if domain_len < 3 || !domain.contains('.') {
        return false;
    }

    let domain_bytes = domain.as_bytes();
    if domain_bytes[0] == b'.' || domain_bytes[domain_len - 1] == b'.' {
        return false;
    }
    
    if let Some(last_dot) = last_dot_pos {
        if domain_len - (last_dot - at_pos) - 1 > MAX_LABEL_LEN {
            return false;
        }
    }

    true
}

/// Validates a URL (http or https).
///
/// Checks for:
/// - Valid http or https scheme
/// - Non-empty host
/// - Proper URL structure
///
/// # Parameters
///
/// * `url` - The URL to validate
///
/// # Returns
///
/// * `true` if the URL is valid, `false` otherwise
///
/// # Examples
///
/// ```
/// assert!(is_valid_url("https://example.com"));
/// assert!(is_valid_url("http://sub.domain.com/path?query=1"));
/// assert!(!is_valid_url("ftp://example.com"));
/// assert!(!is_valid_url("not-a-url"));
/// ```
pub fn is_valid_url(url: &str) -> bool {
    let url = url.trim();
    
    // Must start with http:// or https://
    let lower = url.to_lowercase();
    if !lower.starts_with("http://") && !lower.starts_with("https://") {
        return false;
    }
    
    // Extract the part after scheme
    let after_scheme = if lower.starts_with("https://") {
        &url[8..]
    } else {
        &url[7..]
    };
    
    if after_scheme.is_empty() {
        return false;
    }
    
    // Find the host (everything before first / or end)
    let host_end = after_scheme.find('/').unwrap_or(after_scheme.len());
    let host = &after_scheme[..host_end];
    
    // Host must not be empty and must contain at least one dot or be localhost
    if host.is_empty() {
        return false;
    }
    
    // Check for valid host characters
    for c in host.chars() {
        if !c.is_alphanumeric() && c != '.' && c != '-' && c != ':' && c != '[' && c != ']' {
            return false;
        }
    }
    
    // Must have at least a domain or be localhost
    if host == "localhost" || host.contains('.') || host.starts_with('[') {
        return true;
    }
    
    // Allow IP addresses without dots
    host.parse::<std::net::Ipv4Addr>().is_ok() || 
    host.starts_with('[') // IPv6 in brackets
}

/// Validates a phone number in international format.
///
/// Accepts formats:
/// - +[country code][number] (e.g., +1234567890)
/// - With separators: +1-555-123-4567, +1 555 123 4567
///
/// # Parameters
///
/// * `phone` - The phone number to validate
///
/// # Returns
///
/// * `true` if the phone number is valid, `false` otherwise
///
/// # Examples
///
/// ```
/// assert!(is_valid_phone("+1234567890"));
/// assert!(is_valid_phone("+1-555-123-4567"));
/// assert!(is_valid_phone("+44 20 7946 0958"));
/// assert!(!is_valid_phone("1234567890")); // Missing +
/// assert!(!is_valid_phone("+123")); // Too short
/// ```
pub fn is_valid_phone(phone: &str) -> bool {
    let phone = phone.trim();
    
    // Must start with +
    if !phone.starts_with('+') {
        return false;
    }
    
    // Extract digits only
    let digits: String = phone[1..].chars()
        .filter(|c| c.is_ascii_digit())
        .collect();
    
    // Must have 7-15 digits (international phone number length)
    matches!(digits.len(), 7..=15)
}

/// Validates a credit card number using the Luhn algorithm.
///
/// Supports all major card types. The number should be digits only
/// or with spaces/dashes (which are stripped).
///
/// # Parameters
///
/// * `card_number` - The credit card number to validate
///
/// # Returns
///
/// * `true` if the card number passes Luhn check, `false` otherwise
///
/// # Examples
///
/// ```
/// assert!(is_valid_credit_card("4532015112830366")); // Visa test card
/// assert!(is_valid_credit_card("5500-0000-0000-0004")); // Mastercard test
/// assert!(!is_valid_credit_card("1234567890123456"));
/// assert!(!is_valid_credit_card("123"));
/// ```
pub fn is_valid_credit_card(card_number: &str) -> bool {
    // Remove spaces and dashes
    let digits: String = card_number.chars()
        .filter(|c| c.is_ascii_digit())
        .collect();
    
    // Must have 13-19 digits
    if !matches!(digits.len(), 13..=19) {
        return false;
    }
    
    // Luhn algorithm
    let mut sum = 0u32;
    let mut alternate = false;
    
    for c in digits.chars().rev() {
        let mut d = (c as u32) - ('0' as u32);
        
        if alternate {
            d *= 2;
            if d > 9 {
                d -= 9;
            }
        }
        
        sum += d;
        alternate = !alternate;
    }
    
    sum % 10 == 0
}

/// Credit card type enumeration.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum CreditCardType {
    Visa,
    Mastercard,
    AmericanExpress,
    Discover,
    JCB,
    DinersClub,
    Unknown,
}

/// Detects the credit card type from the card number.
///
/// # Parameters
///
/// * `card_number` - The credit card number
///
/// # Returns
///
/// * The detected card type
///
/// # Examples
///
/// ```
/// assert_eq!(detect_credit_card_type("4532015112830366"), CreditCardType::Visa);
/// assert_eq!(detect_credit_card_type("5500000000000004"), CreditCardType::Mastercard);
/// assert_eq!(detect_credit_card_type("340000000000009"), CreditCardType::AmericanExpress);
/// ```
pub fn detect_credit_card_type(card_number: &str) -> CreditCardType {
    let digits: String = card_number.chars()
        .filter(|c| c.is_ascii_digit())
        .collect();
    
    if digits.is_empty() {
        return CreditCardType::Unknown;
    }
    
    // Check by prefix patterns
    let first = &digits[0..1];
    let first_two = if digits.len() >= 2 { &digits[0..2] } else { "" };
    let first_three = if digits.len() >= 3 { &digits[0..3] } else { "" };
    let first_four = if digits.len() >= 4 { &digits[0..4] } else { "" };
    
    // Visa: starts with 4, length 13, 16, or 19
    if first == "4" && matches!(digits.len(), 13 | 16 | 19) {
        return CreditCardType::Visa;
    }
    
    // Mastercard: starts with 51-55 or 2221-2720, length 16
    if digits.len() == 16 {
        if let Ok(n) = first_two.parse::<u32>() {
            if (51..=55).contains(&n) {
                return CreditCardType::Mastercard;
            }
        }
        if let Ok(n) = first_four.parse::<u32>() {
            if (2221..=2720).contains(&n) {
                return CreditCardType::Mastercard;
            }
        }
    }
    
    // American Express: starts with 34 or 37, length 15
    if digits.len() == 15 && (first_two == "34" || first_two == "37") {
        return CreditCardType::AmericanExpress;
    }
    
    // Discover: starts with 6011, 65, or 644-649, length 16-19
    if matches!(digits.len(), 16..=19) {
        if first_four == "6011" || first_two == "65" {
            return CreditCardType::Discover;
        }
        if let Ok(n) = first_three.parse::<u32>() {
            if (644..=649).contains(&n) {
                return CreditCardType::Discover;
            }
        }
    }
    
    // JCB: starts with 3528-3589, length 16
    if digits.len() == 16 {
        if let Ok(n) = first_four.parse::<u32>() {
            if (3528..=3589).contains(&n) {
                return CreditCardType::JCB;
            }
        }
    }
    
    // Diners Club: starts with 300-305, 36, or 38, length 14
    if digits.len() == 14 {
        if first_two == "36" || first_two == "38" {
            return CreditCardType::DinersClub;
        }
        if let Ok(n) = first_three.parse::<u32>() {
            if (300..=305).contains(&n) {
                return CreditCardType::DinersClub;
            }
        }
    }
    
    CreditCardType::Unknown
}

/// Validates an IPv4 address.
///
/// # Parameters
///
/// * `ip` - The IPv4 address string to validate
///
/// # Returns
///
/// * `true` if valid IPv4, `false` otherwise
///
/// # Examples
///
/// ```
/// assert!(is_valid_ipv4("192.168.1.1"));
/// assert!(is_valid_ipv4("0.0.0.0"));
/// assert!(is_valid_ipv4("255.255.255.255"));
/// assert!(!is_valid_ipv4("256.1.1.1"));
/// assert!(!is_valid_ipv4("1.1.1"));
/// ```
pub fn is_valid_ipv4(ip: &str) -> bool {
    let parts: Vec<&str> = ip.split('.').collect();
    if parts.len() != 4 {
        return false;
    }
    
    for part in parts {
        // Each part must be a valid number
        if part.is_empty() || part.len() > 3 {
            return false;
        }
        
        // Check for leading zeros (except single "0")
        if part.len() > 1 && part.starts_with('0') {
            return false;
        }
        
        // Must be all digits
        if !part.chars().all(|c| c.is_ascii_digit()) {
            return false;
        }
        
        // Must be 0-255
        match part.parse::<u8>() {
            Ok(_) => {},
            Err(_) => return false,
        }
    }
    
    true
}

/// Validates an IPv6 address.
///
/// Supports full notation and compressed notation with ::.
///
/// # Parameters
///
/// * `ip` - The IPv6 address string to validate
///
/// # Returns
///
/// * `true` if valid IPv6, `false` otherwise
///
/// # Examples
///
/// ```
/// assert!(is_valid_ipv6("::1"));
/// assert!(is_valid_ipv6("2001:db8::1"));
/// assert!(is_valid_ipv6("fe80::1%eth0")); // With zone ID
/// assert!(is_valid_ipv6("2001:0db8:85a3:0000:0000:8a2e:0370:7334"));
/// assert!(!is_valid_ipv6("gggg::1"));
/// assert!(!is_valid_ipv6("1:2:3:4:5:6:7:8:9")); // Too many groups
/// ```
pub fn is_valid_ipv6(ip: &str) -> bool {
    // Remove zone ID if present (e.g., %eth0)
    let ip = if let Some(idx) = ip.find('%') {
        &ip[..idx]
    } else {
        ip
    };
    
    // Handle :: (all zeros)
    if ip == "::" {
        return true;
    }
    
    let double_colon_count = ip.matches("::").count();
    if double_colon_count > 1 {
        return false;
    }
    
    let has_double_colon = ip.contains("::");
    
    // Split by single colon, treating :: specially
    let parts: Vec<&str> = if has_double_colon {
        // Replace :: with a marker, then split
        ip.split("::")
            .flat_map(|s| if s.is_empty() { vec![] } else { s.split(':').collect() })
            .collect()
    } else {
        ip.split(':').collect()
    };
    
    // IPv6 has 8 groups of 16-bit values
    // With ::, we can have fewer (the missing ones are zeros)
    let max_groups = if has_double_colon { 7 } else { 8 };
    
    if parts.len() > max_groups || (parts.is_empty() && !has_double_colon) {
        return false;
    }
    
    for part in &parts {
        if part.is_empty() {
            continue; // Empty parts are OK with ::
        }
        
        // Each part is 1-4 hex digits
        if part.len() > 4 {
            return false;
        }
        
        if !part.chars().all(|c| c.is_ascii_hexdigit()) {
            return false;
        }
    }
    
    // Without ::, must have exactly 8 parts
    if !has_double_colon && parts.len() != 8 {
        return false;
    }
    
    true
}

/// Password strength levels.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum PasswordStrength {
    VeryWeak,
    Weak,
    Medium,
    Strong,
    VeryStrong,
}

/// Validates password strength based on multiple criteria.
///
/// Checks:
/// - Minimum length (default 8)
/// - Contains lowercase letters
/// - Contains uppercase letters
/// - Contains digits
/// - Contains special characters
///
/// # Parameters
///
/// * `password` - The password to validate
///
/// # Returns
///
/// * `PasswordStrength` enum value
///
/// # Examples
///
/// ```
/// assert_eq!(validate_password_strength("password"), PasswordStrength::VeryWeak);
/// assert_eq!(validate_password_strength("Password1"), PasswordStrength::Medium);
/// assert_eq!(validate_password_strength("P@ssw0rd!123"), PasswordStrength::VeryStrong);
/// ```
pub fn validate_password_strength(password: &str) -> PasswordStrength {
    let len = password.len();
    let mut score = 0;
    
    // Length scoring
    if len >= 8 {
        score += 1;
    }
    if len >= 12 {
        score += 1;
    }
    if len >= 16 {
        score += 1;
    }
    
    let has_lowercase = password.chars().any(|c| c.is_ascii_lowercase());
    let has_uppercase = password.chars().any(|c| c.is_ascii_uppercase());
    let has_digit = password.chars().any(|c| c.is_ascii_digit());
    let has_special = password.chars().any(|c| "!@#$%^&*()_+-=[]{}|;':\",./<>?`~".contains(c));
    
    // Character type scoring
    if has_lowercase {
        score += 1;
    }
    if has_uppercase {
        score += 1;
    }
    if has_digit {
        score += 1;
    }
    if has_special {
        score += 2;
    }
    
    // Mixed types bonus
    let type_count = [has_lowercase, has_uppercase, has_digit, has_special]
        .iter().filter(|&&x| x).count();
    if type_count >= 3 {
        score += 1;
    }
    if type_count == 4 {
        score += 1;
    }
    
    match score {
        0..=2 => PasswordStrength::VeryWeak,
        3..=4 => PasswordStrength::Weak,
        5..=6 => PasswordStrength::Medium,
        7..=8 => PasswordStrength::Strong,
        _ => PasswordStrength::VeryStrong,
    }
}

/// Validates an ISBN-10 or ISBN-13 number.
///
/// # Parameters
///
/// * `isbn` - The ISBN string to validate (can include hyphens)
///
/// # Returns
///
/// * `true` if valid ISBN, `false` otherwise
///
/// # Examples
///
/// ```
/// assert!(is_valid_isbn("0471958697")); // ISBN-10
/// assert!(is_valid_isbn("0-471-60695-2")); // ISBN-10 with hyphens
/// assert!(is_valid_isbn("9780471486480")); // ISBN-13
/// assert!(is_valid_isbn("978-0-13-235088-4")); // ISBN-13 with hyphens
/// assert!(!is_valid_isbn("123456789")); // Invalid
/// ```
pub fn is_valid_isbn(isbn: &str) -> bool {
    let cleaned: String = isbn.chars()
        .filter(|c| *c != '-' && *c != ' ')
        .collect();
    
    match cleaned.len() {
        10 => validate_isbn10(&cleaned),
        13 => validate_isbn13(&cleaned),
        _ => false,
    }
}

fn validate_isbn10(isbn: &str) -> bool {
    let chars: Vec<char> = isbn.chars().collect();
    
    let mut sum = 0u32;
    for (i, &c) in chars.iter().enumerate() {
        let digit = if i == 9 && c == 'X' {
            10
        } else if c.is_ascii_digit() {
            (c as u32) - ('0' as u32)
        } else {
            return false;
        };
        sum += digit * (10 - i as u32);
    }
    
    sum % 11 == 0
}

fn validate_isbn13(isbn: &str) -> bool {
    let chars: Vec<char> = isbn.chars().collect();
    
    let mut sum = 0u32;
    for (i, &c) in chars.iter().enumerate() {
        if !c.is_ascii_digit() {
            return false;
        }
        let digit = (c as u32) - ('0' as u32);
        let weight = if i % 2 == 0 { 1 } else { 3 };
        sum += digit * weight;
    }
    
    sum % 10 == 0
}

/// Validates a hex color code.
///
/// Accepts formats:
/// - #RGB
/// - #RRGGBB
/// - #RGBA
/// - #RRGGBBAA
///
/// # Parameters
///
/// * `color` - The hex color string to validate
///
/// # Returns
///
/// * `true` if valid hex color, `false` otherwise
///
/// # Examples
///
/// ```
/// assert!(is_valid_hex_color("#fff"));
/// assert!(is_valid_hex_color("#ffffff"));
/// assert!(is_valid_hex_color("#ffaa0080"));
/// assert!(!is_valid_hex_color("fff")); // Missing #
/// assert!(!is_valid_hex_color("#fffg00")); // Invalid char
/// ```
pub fn is_valid_hex_color(color: &str) -> bool {
    let color = color.trim();
    
    if !color.starts_with('#') {
        return false;
    }
    
    let hex = &color[1..];
    let len = hex.len();
    
    if !matches!(len, 3 | 4 | 6 | 8) {
        return false;
    }
    
    hex.chars().all(|c| c.is_ascii_hexdigit())
}

/// Validates a slug (URL-friendly identifier).
///
/// Rules:
/// - Lowercase letters, numbers, and hyphens only
/// - Must start and end with alphanumeric
/// - No consecutive hyphens
/// - Length between 1 and 64
///
/// # Parameters
///
/// * `slug` - The slug string to validate
///
/// # Returns
///
/// * `true` if valid slug, `false` otherwise
///
/// # Examples
///
/// ```
/// assert!(is_valid_slug("my-blog-post"));
/// assert!(is_valid_slug("user123"));
/// assert!(!is_valid_slug("-invalid"));
/// assert!(!is_valid_slug("invalid-"));
/// assert!(!is_valid_slug("has space"));
/// ```
pub fn is_valid_slug(slug: &str) -> bool {
    let len = slug.len();
    
    // Check length
    if len == 0 || len > 64 {
        return false;
    }
    
    let chars: Vec<char> = slug.chars().collect();
    
    // Must start and end with alphanumeric
    if !chars[0].is_ascii_alphanumeric() || !chars[len - 1].is_ascii_alphanumeric() {
        return false;
    }
    
    // Check all characters and no consecutive hyphens
    let mut prev_hyphen = false;
    for &c in &chars {
        if !c.is_ascii_alphanumeric() && c != '-' {
            return false;
        }
        if c == '-' {
            if prev_hyphen {
                return false;
            }
            prev_hyphen = true;
        } else {
            prev_hyphen = false;
        }
    }
    
    true
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_is_valid_email() {
        assert!(is_valid_email("user@example.com"));
        assert!(is_valid_email("user.name@example.com"));
        assert!(is_valid_email("user+tag@example.com"));
        assert!(is_valid_email("user@sub.domain.co.uk"));
        assert!(!is_valid_email(""));
        assert!(!is_valid_email("user@"));
        assert!(!is_valid_email("@example.com"));
        assert!(!is_valid_email("user@example"));
        assert!(!is_valid_email("user @example.com"));
        assert!(!is_valid_email("user@@example.com"));
    }

    #[test]
    fn test_is_valid_url() {
        assert!(is_valid_url("https://example.com"));
        assert!(is_valid_url("http://example.com"));
        assert!(is_valid_url("https://sub.domain.com/path"));
        assert!(is_valid_url("https://example.com?query=1"));
        assert!(is_valid_url("http://localhost:8080"));
        assert!(!is_valid_url(""));
        assert!(!is_valid_url("ftp://example.com"));
        assert!(!is_valid_url("not-a-url"));
        assert!(!is_valid_url("http://"));
    }

    #[test]
    fn test_is_valid_phone() {
        assert!(is_valid_phone("+1234567890"));
        assert!(is_valid_phone("+1-555-123-4567"));
        assert!(is_valid_phone("+44 20 7946 0958"));
        assert!(is_valid_phone("+8613800138000"));
        assert!(!is_valid_phone("1234567890"));
        assert!(!is_valid_phone("+123"));
        assert!(!is_valid_phone(""));
        assert!(!is_valid_phone("abc"));
    }

    #[test]
    fn test_is_valid_credit_card() {
        // Test card numbers (these pass Luhn but are not real cards)
        assert!(is_valid_credit_card("4532015112830366")); // Visa
        assert!(is_valid_credit_card("5500000000000004")); // Mastercard
        assert!(is_valid_credit_card("340000000000009")); // Amex
        assert!(is_valid_credit_card("6011000000000004")); // Discover
        assert!(!is_valid_credit_card("1234567890123456"));
        assert!(!is_valid_credit_card("123"));
        assert!(!is_valid_credit_card(""));
    }

    #[test]
    fn test_detect_credit_card_type() {
        assert_eq!(detect_credit_card_type("4532015112830366"), CreditCardType::Visa);
        assert_eq!(detect_credit_card_type("5500000000000004"), CreditCardType::Mastercard);
        assert_eq!(detect_credit_card_type("340000000000009"), CreditCardType::AmericanExpress);
        assert_eq!(detect_credit_card_type("6011000000000004"), CreditCardType::Discover);
        assert_eq!(detect_credit_card_type("1234567890123456"), CreditCardType::Unknown);
    }

    #[test]
    fn test_is_valid_ipv4() {
        assert!(is_valid_ipv4("192.168.1.1"));
        assert!(is_valid_ipv4("0.0.0.0"));
        assert!(is_valid_ipv4("255.255.255.255"));
        assert!(is_valid_ipv4("127.0.0.1"));
        assert!(!is_valid_ipv4("256.1.1.1"));
        assert!(!is_valid_ipv4("1.1.1"));
        assert!(!is_valid_ipv4("1.1.1.1.1"));
        assert!(!is_valid_ipv4(""));
        assert!(!is_valid_ipv4("01.1.1.1")); // Leading zero
    }

    #[test]
    fn test_is_valid_ipv6() {
        assert!(is_valid_ipv6("::1"));
        assert!(is_valid_ipv6("::"));
        assert!(is_valid_ipv6("2001:db8::1"));
        assert!(is_valid_ipv6("fe80::1"));
        assert!(is_valid_ipv6("2001:0db8:85a3:0000:0000:8a2e:0370:7334"));
        assert!(is_valid_ipv6("fe80::1%eth0")); // With zone ID
        assert!(!is_valid_ipv6("gggg::1"));
        assert!(!is_valid_ipv6("1:2:3:4:5:6:7:8:9"));
        assert!(!is_valid_ipv6(""));
    }

    #[test]
    fn test_validate_password_strength() {
        assert_eq!(validate_password_strength(""), PasswordStrength::VeryWeak);
        assert_eq!(validate_password_strength("password"), PasswordStrength::VeryWeak);
        assert_eq!(validate_password_strength("Password"), PasswordStrength::Weak);
        assert_eq!(validate_password_strength("Password1"), PasswordStrength::Medium);
        assert_eq!(validate_password_strength("Password12"), PasswordStrength::Medium);
        assert_eq!(validate_password_strength("P@ssw0rd"), PasswordStrength::Strong);
        assert_eq!(validate_password_strength("P@ssw0rd!123"), PasswordStrength::VeryStrong);
    }

    #[test]
    fn test_is_valid_isbn() {
        assert!(is_valid_isbn("0471958697"));
        assert!(is_valid_isbn("0-471-60695-2"));
        assert!(is_valid_isbn("9780471486480"));
        assert!(is_valid_isbn("978-0-13-235088-4"));
        assert!(!is_valid_isbn("123456789"));
        assert!(!is_valid_isbn(""));
        assert!(!is_valid_isbn("12345678901234"));
    }

    #[test]
    fn test_is_valid_hex_color() {
        assert!(is_valid_hex_color("#fff"));
        assert!(is_valid_hex_color("#ffffff"));
        assert!(is_valid_hex_color("#ffaa"));
        assert!(is_valid_hex_color("#ffaa0080"));
        assert!(!is_valid_hex_color("fff"));
        assert!(!is_valid_hex_color("#fffg00"));
        assert!(!is_valid_hex_color("#ff"));
        assert!(!is_valid_hex_color(""));
    }

    #[test]
    fn test_is_valid_slug() {
        assert!(is_valid_slug("my-blog-post"));
        assert!(is_valid_slug("user123"));
        assert!(is_valid_slug("a"));
        assert!(!is_valid_slug("-invalid"));
        assert!(!is_valid_slug("invalid-"));
        assert!(!is_valid_slug("has space"));
        assert!(!is_valid_slug("has--double"));
        assert!(!is_valid_slug(""));
    }
}