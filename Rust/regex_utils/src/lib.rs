//! # Regex Utilities
//!
//! A comprehensive regular expression utility module for Rust.
//! Provides pattern matching, validation, extraction, replacement,
//! and common regex patterns for everyday use.
//!
//! ## Usage
//!
//! ```ignore
//! use regex_utils::{is_email, extract_numbers, replace_all};
//!
//! assert!(is_email("user@example.com"));
//! let numbers = extract_numbers("Price: $100, discount: $20");
//! assert_eq!(numbers, vec!["100", "20"]);
//! ```

use std::collections::HashMap;

// ============================================================================
// Common Regex Patterns
// ============================================================================

/// Common regex patterns for validation and matching
pub mod patterns {
    /// Email address pattern
    pub const EMAIL: &str = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$";

    /// IPv4 address pattern
    pub const IPV4: &str = r"^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$";

    /// IPv6 address pattern (simplified)
    pub const IPV6: &str = r"^([0-9a-fA-F]{1,4}:){7}[0-9a-fA-F]{1,4}$|^::([0-9a-fA-F]{1,4}:){0,6}[0-9a-fA-F]{1,4}$";

    /// URL pattern (http/https)
    pub const URL: &str = r"^https?://[^\s/$.?#].[^\s]*$";

    /// Phone number pattern (international format)
    pub const PHONE: &str = r"^\+[1-9]\d{6,14}$|^[1-9]\d{6,14}$";

    /// Credit card pattern (basic validation)
    pub const CREDIT_CARD: &str = r"^[0-9]{13,19}$";

    /// Date pattern (YYYY-MM-DD)
    pub const DATE: &str = r"^\d{4}-(?:0[1-9]|1[0-2])-(?:0[1-9]|[12]\d|3[01])$";

    /// Time pattern (HH:MM:SS)
    pub const TIME: &str = r"^(?:[01]\d|2[0-3]):[0-5]\d:[0-5]\d$";

    /// DateTime pattern (ISO 8601)
    pub const DATETIME: &str = r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d+)?(?:Z|[+-]\d{2}:\d{2})?$";

    /// UUID pattern
    pub const UUID: &str = r"^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}$";

    /// Hex color pattern (#RGB, #RRGGBB, #RRGGBBAA)
    pub const HEX_COLOR: &str = r"^#(?:[0-9a-fA-F]{3}|[0-9a-fA-F]{6}|[0-9a-fA-F]{8})$";

    /// Username pattern (alphanumeric + underscore, 3-20 chars)
    pub const USERNAME: &str = r"^[a-zA-Z][a-zA-Z0-9_]{2,19}$";

    /// Password strength pattern
    pub const STRONG_PASSWORD: &str = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9])(?=.*[@$!%*?&])[A-Za-z0-9@$!%*?&]{8,}$";

    /// Chinese mobile phone pattern
    pub const CHINA_PHONE: &str = r"^1[3-9]\d{9}$";

    /// Chinese ID card pattern (18 digits)
    pub const CHINA_ID: &str = r"^[1-9]\d{5}(?:18|19|20)\d{2}(?:0[1-9]|1[0-2])(?:0[1-9]|[12]\d|3[01])\d{3}[\dXx]$";

    /// Postcode pattern (Chinese 6-digit)
    pub const CHINA_POSTCODE: &str = r"^[1-9]\d{5}$";

    /// License plate pattern (Chinese) - simplified version
    pub const CHINA_LICENSE: &str = r"^[京津沪渝冀豫云辽黑湘皖鲁新苏浙赣鄂桂甘晋蒙陕吉闽贵粤青藏川宁][A-Z][A-Z0-9]{4,5}$";
}

// ============================================================================
// Validation Functions
// ============================================================================

/// Validates if a string matches the given regex pattern.
pub fn matches_pattern(pattern: &str, text: &str) -> bool {
    regex::Regex::new(pattern)
        .map(|re| re.is_match(text))
        .unwrap_or(false)
}

/// Validates an email address.
pub fn is_email(email: &str) -> bool {
    matches_pattern(patterns::EMAIL, email)
}

/// Validates an IPv4 address.
pub fn is_ipv4(ip: &str) -> bool {
    matches_pattern(patterns::IPV4, ip)
}

/// Validates an IPv6 address (simplified validation).
pub fn is_ipv6(ip: &str) -> bool {
    matches_pattern(patterns::IPV6, ip)
}

/// Validates a URL (http/https).
pub fn is_url(url: &str) -> bool {
    matches_pattern(patterns::URL, url)
}

/// Validates a phone number (international E.164 format).
pub fn is_phone(phone: &str) -> bool {
    matches_pattern(patterns::PHONE, phone)
}

/// Validates a Chinese mobile phone number.
pub fn is_china_phone(phone: &str) -> bool {
    matches_pattern(patterns::CHINA_PHONE, phone)
}

/// Validates a date string (YYYY-MM-DD format).
pub fn is_date(date: &str) -> bool {
    matches_pattern(patterns::DATE, date)
}

/// Validates a time string (HH:MM:SS format).
pub fn is_time(time: &str) -> bool {
    matches_pattern(patterns::TIME, time)
}

/// Validates a UUID string.
pub fn is_uuid(uuid: &str) -> bool {
    matches_pattern(patterns::UUID, uuid)
}

/// Validates a hex color code.
pub fn is_hex_color(color: &str) -> bool {
    matches_pattern(patterns::HEX_COLOR, color)
}

/// Validates a username (alphanumeric + underscore, 3-20 chars).
pub fn is_username(username: &str) -> bool {
    matches_pattern(patterns::USERNAME, username)
}

/// Validates a strong password.
pub fn is_strong_password(password: &str) -> bool {
    matches_pattern(patterns::STRONG_PASSWORD, password)
}

/// Validates a Chinese ID card number (18 digits).
pub fn is_china_id(id_card: &str) -> bool {
    matches_pattern(patterns::CHINA_ID, id_card)
}

/// Validates a Chinese postcode (6 digits).
pub fn is_china_postcode(postcode: &str) -> bool {
    matches_pattern(patterns::CHINA_POSTCODE, postcode)
}

/// Validates a Chinese vehicle license plate.
pub fn is_china_license(plate: &str) -> bool {
    matches_pattern(patterns::CHINA_LICENSE, plate)
}

// ============================================================================
// Extraction Functions
// ============================================================================

/// Extracts all matches of a pattern from text.
pub fn extract_all(pattern: &str, text: &str) -> Vec<String> {
    regex::Regex::new(pattern)
        .map(|re| re.find_iter(text).map(|m| m.as_str().to_string()).collect())
        .unwrap_or_default()
}

/// Extracts all numbers from text.
pub fn extract_numbers(text: &str) -> Vec<String> {
    extract_all(r"\d+", text)
}

/// Extracts all email addresses from text.
pub fn extract_emails(text: &str) -> Vec<String> {
    // Use pattern without anchors for extraction
    extract_all(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", text)
}

/// Extracts all URLs from text.
pub fn extract_urls(text: &str) -> Vec<String> {
    // Use pattern without anchors for extraction
    extract_all(r"https?://[^\s/$.?#].[^\s]*", text)
}

/// Extracts all phone numbers from text (international format).
pub fn extract_phones(text: &str) -> Vec<String> {
    extract_all(r"\+?[1-9]\d{1,14}", text)
}

/// Extracts all Chinese phone numbers from text.
pub fn extract_china_phones(text: &str) -> Vec<String> {
    // Use pattern without anchors for extraction
    extract_all(r"1[3-9]\d{9}", text)
}

/// Extracts the first capture group from the first match.
pub fn extract_first_capture(pattern: &str, text: &str) -> Option<String> {
    let re = regex::Regex::new(pattern).ok()?;
    re.captures(text)
        .and_then(|caps| caps.get(1).map(|m| m.as_str().to_string()))
}

/// Extracts all capture groups from all matches.
pub fn extract_captures(pattern: &str, text: &str) -> Vec<Vec<String>> {
    regex::Regex::new(pattern)
        .map(|re| {
            re.captures_iter(text)
                .map(|caps| {
                    caps.iter()
                        .skip(1)
                        .filter_map(|m| m.map(|m| m.as_str().to_string()))
                        .collect()
                })
                .collect()
        })
        .unwrap_or_default()
}

/// Extracts named capture groups from the first match.
pub fn extract_named_captures(pattern: &str, text: &str) -> HashMap<String, String> {
    let mut result = HashMap::new();

    if let Ok(re) = regex::Regex::new(pattern) {
        if let Some(caps) = re.captures(text) {
            for name in re.capture_names().flatten() {
                if let Some(m) = caps.name(name) {
                    result.insert(name.to_string(), m.as_str().to_string());
                }
            }
        }
    }

    result
}

// ============================================================================
// Replacement Functions
// ============================================================================

/// Replaces all matches of a pattern with a replacement string.
pub fn replace_all(pattern: &str, text: &str, replacement: &str) -> String {
    regex::Regex::new(pattern)
        .map(|re| re.replace_all(text, replacement).to_string())
        .unwrap_or_else(|_| text.to_string())
}

/// Replaces only the first match of a pattern.
pub fn replace_first(pattern: &str, text: &str, replacement: &str) -> String {
    regex::Regex::new(pattern)
        .map(|re| re.replace(text, replacement).to_string())
        .unwrap_or_else(|_| text.to_string())
}

/// Removes all matches of a pattern from text.
pub fn remove_all(pattern: &str, text: &str) -> String {
    replace_all(pattern, text, "")
}

/// Strips HTML tags from text.
pub fn strip_html(html: &str) -> String {
    replace_all(r"<[^>]*>", html, "")
}

/// Normalizes whitespace in text.
pub fn normalize_whitespace(text: &str) -> String {
    let result = replace_all(r"\s+", text, " ");
    result.trim().to_string()
}

/// Sanitizes a filename by removing invalid characters.
pub fn sanitize_filename(filename: &str) -> String {
    let result = replace_all(r#"[<>:"/\\|?*]"#, filename, "");
    let result = replace_all(r#"[\s\[\](),;]+"#, &result, "_");
    result.trim_matches(|c: char| c == '_' || c == '.').to_string()
}

// ============================================================================
// Utility Functions
// ============================================================================

/// Counts the number of matches of a pattern in text.
pub fn count_matches(pattern: &str, text: &str) -> usize {
    regex::Regex::new(pattern)
        .map(|re| re.find_iter(text).count())
        .unwrap_or(0)
}

/// Checks if a pattern matches anywhere in the text.
pub fn contains_pattern(pattern: &str, text: &str) -> bool {
    regex::Regex::new(pattern)
        .map(|re| re.is_match(text))
        .unwrap_or(false)
}

/// Splits text by a regex pattern.
pub fn split_by(pattern: &str, text: &str) -> Vec<String> {
    regex::Regex::new(pattern)
        .map(|re| re.split(text).map(|s| s.to_string()).collect())
        .unwrap_or_else(|_| vec![text.to_string()])
}

/// Escapes special regex characters in a string.
pub fn escape_regex(text: &str) -> String {
    regex::escape(text)
}

/// Tests if a regex pattern is valid.
pub fn is_valid_regex(pattern: &str) -> bool {
    regex::Regex::new(pattern).is_ok()
}

// ============================================================================
// Module Tests
// ============================================================================

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_is_email() {
        assert!(is_email("user@example.com"));
        assert!(!is_email("invalid"));
    }

    #[test]
    fn test_is_ipv4() {
        assert!(is_ipv4("192.168.1.1"));
        assert!(!is_ipv4("256.1.1.1"));
    }

    #[test]
    fn test_is_url() {
        assert!(is_url("https://example.com"));
        assert!(!is_url("not-a-url"));
    }

    #[test]
    fn test_extract_numbers() {
        let numbers = extract_numbers("Price: $100, discount: $20");
        assert_eq!(numbers, vec!["100", "20"]);
    }

    #[test]
    fn test_extract_emails() {
        let emails = extract_emails("Contact: user@example.com");
        assert_eq!(emails, vec!["user@example.com"]);
    }

    #[test]
    fn test_replace_all() {
        let result = replace_all(r"\d+", "abc123def", "NUM");
        assert_eq!(result, "abcNUMdef");
    }

    #[test]
    fn test_strip_html() {
        let result = strip_html("<p>Hello</p>");
        assert_eq!(result, "Hello");
    }

    #[test]
    fn test_count_matches() {
        let count = count_matches(r"\d+", "abc123def456");
        assert_eq!(count, 2);
    }

    #[test]
    fn test_is_valid_regex() {
        assert!(is_valid_regex(r"\d+"));
        assert!(!is_valid_regex(r"[\d+"));
    }
}
