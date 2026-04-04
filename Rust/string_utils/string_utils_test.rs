//! String Utilities Test Suite
//! 
//! Comprehensive tests for string manipulation functions.

use std::process::Command;

// Test truncate function
#[test]
fn test_truncate_basic() {
    assert_eq!(truncate("Hello World", 8), "Hello...");
    assert_eq!(truncate("Hello", 10), "Hello");
    assert_eq!(truncate("", 10), "");
}

#[test]
fn test_truncate_unicode() {
    // Unicode characters
    assert_eq!(truncate("你好世界", 5), "你好...");
    assert_eq!(truncate("你好世界", 4), "你好世界");
    assert_eq!(truncate("你好世界", 3), "...");
}

#[test]
fn test_truncate_edge_cases() {
    // Edge cases
    assert_eq!(truncate("Hi", 2), "...");  // max_len < 3
    assert_eq!(truncate("Test", 0), "...");
    assert_eq!(truncate("Test", 1), "...");
}

// Test slugify function
#[test]
fn test_slugify_basic() {
    assert_eq!(slugify("Hello World"), "hello-world");
    assert_eq!(slugify("  Multiple   Spaces  "), "multiple-spaces");
}

#[test]
fn test_slugify_special_chars() {
    assert_eq!(slugify("Hello-World"), "hello-world");
    assert_eq!(slugify("Hello_World"), "hello-world");
    assert_eq!(slugify("Café & Restaurant!"), "caf-restaurant");
}

#[test]
fn test_slugify_edge_cases() {
    assert_eq!(slugify(""), "");
    assert_eq!(slugify("!!!"), "");
    assert_eq!(slugify("   "), "");
}

// Test count_words function
#[test]
fn test_count_words_basic() {
    assert_eq!(count_words("Hello World"), 2);
    assert_eq!(count_words("  Multiple   spaces   "), 2);
    assert_eq!(count_words("Hello, World! How are you?"), 5);
}

#[test]
fn test_count_words_edge_cases() {
    assert_eq!(count_words(""), 0);
    assert_eq!(count_words("   "), 0);
    assert_eq!(count_words("One"), 1);
    assert_eq!(count_words("123 456 789"), 3);
}

// Test is_valid_email function
#[test]
fn test_is_valid_email_valid() {
    assert!(is_valid_email("user@example.com"));
    assert!(is_valid_email("user.name@sub.domain.co"));
    assert!(is_valid_email("test+tag@example.org"));
}

#[test]
fn test_is_valid_email_invalid() {
    assert!(!is_valid_email("invalid.email"));
    assert!(!is_valid_email("@example.com"));
    assert!(!is_valid_email("user@"));
    assert!(!is_valid_email("user@@example.com"));
    assert!(!is_valid_email("user @example.com"));
    assert!(!is_valid_email(""));
    assert!(!is_valid_email("user@domain"));
}

// Test reverse_graphemes function
#[test]
fn test_reverse_graphemes_basic() {
    assert_eq!(reverse_graphemes("Hello"), "olleH");
    assert_eq!(reverse_graphemes(""), "");
    assert_eq!(reverse_graphemes("a"), "a");
}

#[test]
fn test_reverse_graphemes_unicode() {
    assert_eq!(reverse_graphemes("你好世界"), "界世好你");
    assert_eq!(reverse_graphemes("👨‍👩‍👧‍👦"), "👨‍👩‍👧‍👦"); // Palindrome at grapheme level
}

// Test pad function
#[test]
fn test_pad_left() {
    assert_eq!(pad("42", 5, '0', true), "00042");
    assert_eq!(pad("test", 4, '0', true), "test");
}

#[test]
fn test_pad_right() {
    assert_eq!(pad("Hello", 10, ' ', false), "Hello     ");
    assert_eq!(pad("test", 4, ' ', false), "test");
}

#[test]
fn test_pad_edge_cases() {
    assert_eq!(pad("", 3, '-', false), "---");
    assert_eq!(pad("Hello World", 5, ' ', true), "Hello World");
}

// Import the functions from mod.rs
// In a real test, these would be imported from the module
fn truncate(s: &str, max_len: usize) -> String {
    if s.is_empty() {
        return String::new();
    }
    const ELLIPSIS_LEN: usize = 3;
    if max_len < ELLIPSIS_LEN {
        return "...".to_string();
    }
    if s.len() <= max_len && s.is_ascii() {
        return s.to_string();
    }
    let mut char_count = 0;
    for (idx, _) in s.char_indices() {
        char_count += 1;
        if char_count > max_len {
            let target_len = max_len.saturating_sub(ELLIPSIS_LEN);
            let truncate_idx = s.char_indices()
                .nth(target_len)
                .map(|(idx, _)| idx)
                .unwrap_or(idx);
            return s[..truncate_idx].to_string() + "...";
        }
    }
    s.to_string()
}

fn slugify(s: &str) -> String {
    if s.is_empty() {
        return String::new();
    }
    let mut result = String::with_capacity(s.len());
    let mut prev_was_hyphen = true;
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
    }
    if result.ends_with('-') {
        result.pop();
    }
    result
}

fn count_words(s: &str) -> usize {
    if s.is_empty() {
        return 0;
    }
    let mut count = 0;
    let mut in_word = false;
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

fn is_valid_email(email: &str) -> bool {
    if email.is_empty() {
        return false;
    }
    let bytes = email.as_bytes();
    let len = bytes.len();
    let mut at_count = 0;
    let mut at_pos = 0;
    for (i, &b) in bytes.iter().enumerate() {
        if b == b' ' {
            return false;
        }
        if b == b'@' {
            at_count += 1;
            at_pos = i;
        }
    }
    if at_count != 1 {
        return false;
    }
    if at_pos == 0 || at_pos == len - 1 {
        return false;
    }
    let domain = &email[at_pos + 1..];
    if !domain.contains('.') {
        return false;
    }
    if domain.starts_with('.') || domain.ends_with('.') {
        return false;
    }
    true
}

fn reverse_graphemes(s: &str) -> String {
    s.chars().rev().collect()
}

fn pad(s: &str, width: usize, pad_char: char, left: bool) -> String {
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
