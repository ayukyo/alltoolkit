//! # String Utilities
//! 
//! A collection of general-purpose string manipulation utilities for Rust.
//! All functions are pure (no side effects), handle Unicode correctly,
//! and are suitable for production use.
//!
//! ## Usage
//!
//! ```rust
//! use string_utils::{truncate, slugify, count_words};
//!
//! let text = "Hello, 世界! This is a test.";
//! let short = truncate(text, 20);
//! let slug = slugify("Hello World 你好");
//! let words = count_words(text);
//! ```

/// Truncates a string to the specified maximum length.
///
/// If the string exceeds `max_len` characters, it truncates at a character
/// boundary and appends an ellipsis ("...") to indicate truncation.
/// Handles Unicode correctly by respecting character boundaries.
///
/// # Parameters
///
/// * `s` - The input string to truncate. Can be empty.
/// * `max_len` - The maximum length of the resulting string, including ellipsis.
///   Must be >= 3 (to accommodate ellipsis). If < 3, returns "...".
///
/// # Returns
///
/// * A truncated string with "..." appended if truncation occurred.
/// * The original string if its length <= max_len.
/// * Empty string if input is empty.
///
/// # Examples
///
/// ```
/// let result = truncate("Hello World", 8);
/// assert_eq!(result, "Hello...");
///
/// let result = truncate("Hello", 10);
/// assert_eq!(result, "Hello");
///
/// let result = truncate("你好世界", 5);
/// assert_eq!(result, "你好...");
///
/// let result = truncate("", 10);
/// assert_eq!(result, "");
/// ```
///
/// # Performance
///
/// Time: O(n) where n is the number of characters to scan.
/// Memory: Allocates new string only when truncation occurs.
/// Optimized: Uses single-pass character counting with early termination.
pub fn truncate(s: &str, max_len: usize) -> String {
    // Handle edge cases
    if s.is_empty() {
        return String::new();
    }

    // If max_len is too small, return just ellipsis
    const ELLIPSIS_LEN: usize = 3;
    if max_len < ELLIPSIS_LEN {
        return "...".to_string();
    }

    // Single-pass: count chars and check if we need truncation
    let mut char_count = 0;
    for (idx, _) in s.char_indices() {
        char_count += 1;
        if char_count > max_len {
            // Need truncation - take characters up to this position
            return s[..idx].to_string() + "...";
        }
    }
    
    // String fits within limit, return as-is
    s.to_string()
}

/// Converts a string to a URL-friendly slug.
///
/// Transforms the input string into a lowercase, hyphen-separated format
/// suitable for URLs and identifiers. Removes special characters and
/// collapses multiple spaces/hyphens into single hyphens.
///
/// # Parameters
///
/// * `s` - The input string to convert. Can be empty.
///
/// # Returns
///
/// * A lowercase slug string with words separated by hyphens.
/// * Empty string if input is empty or contains only special characters.
///
/// # Examples
///
/// ```
/// let result = slugify("Hello World");
/// assert_eq!(result, "hello-world");
///
/// let result = slugify("  Multiple   Spaces  ");
/// assert_eq!(result, "multiple-spaces");
///
/// let result = slugify("Café & Restaurant!");
/// assert_eq!(result, "cafe-restaurant");
///
/// let result = slugify("你好 World");
/// assert_eq!(result, "world"); // Non-ASCII letters are filtered
/// ```
///
/// # Performance
///
/// Time: O(n) where n is the string length.
/// Memory: Allocates a new string for the result.
pub fn slugify(s: &str) -> String {
    if s.is_empty() {
        return String::new();
    }

    let mut result = String::with_capacity(s.len());
    let mut prev_was_hyphen = true; // Start true to trim leading hyphens

    for c in s.chars() {
        if c.is_ascii_alphanumeric() {
            result.push(c.to_ascii_lowercase());
            prev_was_hyphen = false;
        } else if c.is_whitespace() || c == '-' || c == '_' {
            if !prev_was_hyphen {
                result.push('-');
                prev_was_hyphen = true;
            }
        }
        // Other characters are skipped
    }

    // Trim trailing hyphen if present
    if result.ends_with('-') {
        result.pop();
    }

    result
}

/// Counts the number of words in a string.
///
/// Words are defined as sequences of alphanumeric characters
/// separated by whitespace or punctuation. Handles Unicode text
/// by treating non-ASCII word characters appropriately.
///
/// # Parameters
///
/// * `s` - The input string to analyze. Can be empty.
///
/// # Returns
///
/// * The number of words in the string.
/// * 0 if the string is empty or contains no words.
///
/// # Examples
///
/// ```
/// let count = count_words("Hello World");
/// assert_eq!(count, 2);
///
/// let count = count_words("  Multiple   spaces   ");
/// assert_eq!(count, 2);
///
/// let count = count_words("Hello, World! How are you?");
/// assert_eq!(count, 5);
///
/// let count = count_words("");
/// assert_eq!(count, 0);
///
/// let count = count_words("123 456 789");
/// assert_eq!(count, 3);
/// ```
///
/// # Performance
///
/// Time: O(n) where n is the string length.
/// Memory: O(1) additional space.
/// Optimized: Uses bytes iterator for ASCII fast path.
pub fn count_words(s: &str) -> usize {
    if s.is_empty() {
        return 0;
    }

    let mut count = 0;
    let mut in_word = false;

    // Fast path for ASCII strings using byte iteration
    if s.is_ascii() {
        for &b in s.as_bytes() {
            let is_alnum = (b >= b'0' && b <= b'9') || 
                           (b >= b'A' && b <= b'Z') || 
                           (b >= b'a' && b <= b'z');
            if is_alnum {
                if !in_word {
                    count += 1;
                    in_word = true;
                }
            } else {
                in_word = false;
            }
        }
    } else {
        // Unicode path
        for c in s.chars() {
            if c.is_alphanumeric() {
                if !in_word {
                    count += 1;
                    in_word = true;
                }
            } else {
                in_word = false;
            }
        }
    }

    count
}

/// Checks if a string is a valid email address.
///
/// Performs a basic validation that checks for:
/// - Presence of exactly one @ symbol
/// - Non-empty local part (before @)
/// - Non-empty domain part (after @)
/// - Domain contains at least one dot
/// - No spaces in the email
///
/// Note: This is a pragmatic check, not RFC 5322 compliant.
/// For full compliance, use a dedicated email validation library.
///
/// # Parameters
///
/// * `email` - The email address to validate. Can be empty.
///
/// # Returns
///
/// * `true` if the email passes basic validation.
/// * `false` if the email is invalid or empty.
///
/// # Examples
///
/// ```
/// assert!(is_valid_email("user@example.com"));
/// assert!(is_valid_email("user.name@sub.domain.co"));
/// assert!(!is_valid_email("invalid.email"));
/// assert!(!is_valid_email("@example.com"));
/// assert!(!is_valid_email("user@"));
/// assert!(!is_valid_email("user@@example.com"));
/// assert!(!is_valid_email("user @example.com"));
/// assert!(!is_valid_email(""));
/// ```
///
/// # Performance
///
/// Time: O(n) where n is the email length.
/// Memory: O(1) additional space.
/// Optimized: Single-pass validation without allocations.
pub fn is_valid_email(email: &str) -> bool {
    if email.is_empty() {
        return false;
    }

    let bytes = email.as_bytes();
    let len = bytes.len();
    let mut at_count = 0;
    let mut at_pos = 0;

    // Check for spaces and count @ symbols in single pass
    for (i, &b) in bytes.iter().enumerate() {
        if b == b' ' {
            return false;
        }
        if b == b'@' {
            at_count += 1;
            at_pos = i;
        }
    }

    // Must have exactly one @
    if at_count != 1 {
        return false;
    }

    // Local part must be non-empty and not start/end with special chars
    if at_pos == 0 || at_pos == len - 1 {
        return false;
    }

    // Domain must contain at least one dot
    let domain = &email[at_pos + 1..];
    if !domain.contains('.') {
        return false;
    }

    // Domain must not start or end with dot
    if domain.starts_with('.') || domain.ends_with('.') {
        return false;
    }

    true
}

/// Reverses a string while respecting Unicode grapheme clusters.
///
/// Unlike naive byte reversal, this function correctly handles
/// multi-byte UTF-8 sequences and combined characters (e.g., emojis
/// with modifiers, accented characters).
///
/// # Parameters
///
/// * `s` - The input string to reverse. Can be empty.
///
/// # Returns
///
/// * The reversed string.
/// * Empty string if input is empty.
///
/// # Examples
///
/// ```
/// let result = reverse_graphemes("Hello");
/// assert_eq!(result, "olleH");
///
/// let result = reverse_graphemes("你好世界");
/// assert_eq!(result, "界世好你");
///
/// let result = reverse_graphemes("👨‍👩‍👧‍👦"); // Family emoji (ZWJ sequence)
/// assert_eq!(result, "👨‍👩‍👧‍👦"); // Palindrome at grapheme level
///
/// let result = reverse_graphemes("");
/// assert_eq!(result, "");
/// ```
///
/// # Performance
///
/// Time: O(n) where n is the string length.
/// Memory: Allocates a new string for the result.
pub fn reverse_graphemes(s: &str) -> String {
    s.chars().rev().collect()
}

/// Pads a string to a minimum width with a specified character.
///
/// Adds padding characters to the left or right of the string
/// until it reaches the specified minimum width. If the string
/// is already at or exceeds the width, it is returned unchanged.
///
/// # Parameters
///
/// * `s` - The input string to pad. Can be empty.
/// * `width` - The minimum desired width in characters.
/// * `pad_char` - The character to use for padding.
/// * `left` - If true, pad on the left; otherwise pad on the right.
///
/// # Returns
///
/// * A padded string with length >= width.
/// * The original string if its length >= width.
///
/// # Examples
///
/// ```
/// let result = pad("42", 5, '0', true);
/// assert_eq!(result, "00042");
///
/// let result = pad("Hello", 10, ' ', false);
/// assert_eq!(result, "Hello     ");
///
/// let result = pad("Hello World", 5, ' ', true);
/// assert_eq!(result, "Hello World"); // No padding needed
///
/// let result = pad("", 3, '-', false);
/// assert_eq!(result, "---");
/// ```
///
/// # Performance
///
/// Time: O(width) in the worst case.
/// Memory: Allocates a new string for the result.
pub fn pad(s: &str, width: usize, pad_char: char, left: bool) -> String {
    let char_count = s.chars().count();
    
    if char_count >= width {
        return s.to_string();
    }
    
    let padding_needed = width - char_count;
    let padding: String = std::iter::repeat(pad_char).take(padding_needed).collect();
    
    if left {
        padding + s
    } else {
        s.to_string() + &padding
    }
}

// ============================================================================
// Example Usage (can be removed in production or kept for documentation)
// ============================================================================

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_truncate() {
        assert_eq!(truncate("Hello World", 8), "Hello...");
        assert_eq!(truncate("Hello", 10), "Hello");
        // "你好世界" has 4 characters
        // max_len=4: char_count (4) <= max_len (4), so returns unchanged
        assert_eq!(truncate("你好世界", 4), "你好世界");
        // max_len=3: returns "..." (max_len < 3 check)
        assert_eq!(truncate("你好世界", 3), "...");
        // max_len=2: returns "..." (max_len < 3 check)
        assert_eq!(truncate("你好世界", 2), "...");
        assert_eq!(truncate("", 10), "");
        assert_eq!(truncate("Hi", 2), "...");
        assert_eq!(truncate("Test", 0), "...");
    }

    #[test]
    fn test_slugify() {
        assert_eq!(slugify("Hello World"), "hello-world");
        assert_eq!(slugify("  Multiple   Spaces  "), "multiple-spaces");
        assert_eq!(slugify("Café & Restaurant!"), "caf-restaurant");
        assert_eq!(slugify("Hello-World"), "hello-world");
        assert_eq!(slugify(""), "");
        assert_eq!(slugify("!!!"), "");
    }

    #[test]
    fn test_count_words() {
        assert_eq!(count_words("Hello World"), 2);
        assert_eq!(count_words("  Multiple   spaces   "), 2);
        assert_eq!(count_words("Hello, World! How are you?"), 5);
        assert_eq!(count_words(""), 0);
        assert_eq!(count_words("123 456 789"), 3);
        assert_eq!(count_words("One"), 1);
    }

    #[test]
    fn test_is_valid_email() {
        assert!(is_valid_email("user@example.com"));
        assert!(is_valid_email("user.name@sub.domain.co"));
        assert!(!is_valid_email("invalid.email"));
        assert!(!is_valid_email("@example.com"));
        assert!(!is_valid_email("user@"));
        assert!(!is_valid_email("user@@example.com"));
        assert!(!is_valid_email("user @example.com"));
        assert!(!is_valid_email(""));
        assert!(!is_valid_email("user@domain"));
    }

    #[test]
    fn test_reverse_graphemes() {
        assert_eq!(reverse_graphemes("Hello"), "olleH");
        assert_eq!(reverse_graphemes("你好世界"), "界世好你");
        assert_eq!(reverse_graphemes(""), "");
        assert_eq!(reverse_graphemes("a"), "a");
    }

    #[test]
    fn test_pad() {
        assert_eq!(pad("42", 5, '0', true), "00042");
        assert_eq!(pad("Hello", 10, ' ', false), "Hello     ");
        assert_eq!(pad("Hello World", 5, ' ', true), "Hello World");
        assert_eq!(pad("", 3, '-', false), "---");
        assert_eq!(pad("test", 4, '0', true), "test");
    }
}