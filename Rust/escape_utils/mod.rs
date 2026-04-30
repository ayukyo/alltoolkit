//! # Escape Utilities
//!
//! A comprehensive collection of escape and unescape functions for Rust.
//! All functions are pure (no side effects), handle Unicode correctly,
//! and are suitable for production use.
//!
//! ## Features
//!
//! - HTML escape/unescape (XSS prevention)
//! - URL encoding/decoding (percent encoding)
//! - JSON string escape/unescape
//! - Shell argument escape (POSIX compliant)
//! - Regex pattern escape
//! - Unicode escape/unescape (\uXXXX format)
//! - XML attribute escape/unescape
//! - SQL string escape (basic protection)
//! - CSV field escape/unescape
//! - C-style string escape/unescape
//!
//! ## Usage
//!
//! ```rust
//! use escape_utils::{escape_html, escape_url, escape_json};
//!
//! let safe_html = escape_html("<script>alert('XSS')</script>");
//! let safe_url = escape_url("hello world");
//! let safe_json = escape_json("Line1\nLine2");
//! ```

use std::borrow::Cow;

// ============================================================================
// HTML Escape Functions
// ============================================================================

/// HTML escape - converts special characters to HTML entities.
///
/// Escapes: `&` → `&amp;`, `<` → `&lt;`, `>` → `&gt;`,
/// `"` → `&quot;`, `'` → `&#39;`
///
/// # Examples
///
/// ```
/// use escape_utils::escape_html;
///
/// assert_eq!(escape_html("<div>"), "&lt;div&gt;");
/// assert_eq!(escape_html("a & b"), "a &amp; b");
/// assert_eq!(escape_html("it's"), "it&#39;s");
/// ```
pub fn escape_html(s: &str) -> Cow<'_, str> {
    if !s.contains(&['&', '<', '>', '"', '\''][..]) {
        return Cow::Borrowed(s);
    }
    
    let mut result = String::with_capacity(s.len() * 2);
    for c in s.chars() {
        match c {
            '&' => result.push_str("&amp;"),
            '<' => result.push_str("&lt;"),
            '>' => result.push_str("&gt;"),
            '"' => result.push_str("&quot;"),
            '\'' => result.push_str("&#39;"),
            _ => result.push(c),
        }
    }
    Cow::Owned(result)
}

/// HTML unescape - converts HTML entities back to characters.
///
/// Supports named entities (`&amp;`, `&lt;`, etc.), decimal entities (`&#39;`),
/// and hexadecimal entities (`&#x27;`).
///
/// # Examples
///
/// ```
/// use escape_utils::unescape_html;
///
/// assert_eq!(unescape_html("&lt;div&gt;"), "<div>");
/// assert_eq!(unescape_html("a &amp; b"), "a & b");
/// assert_eq!(unescape_html("&#39;"), "'");
/// ```
pub fn unescape_html(s: &str) -> Cow<'_, str> {
    if !s.contains('&') {
        return Cow::Borrowed(s);
    }
    
    let mut result = String::with_capacity(s.len());
    let mut chars = s.chars().peekable();
    
    while let Some(c) = chars.next() {
        if c == '&' {
            // Try to parse entity
            let entity = parse_html_entity(&mut chars);
            result.push_str(&entity);
        } else {
            result.push(c);
        }
    }
    
    Cow::Owned(result)
}

fn parse_html_entity(chars: &mut std::iter::Peekable<std::str::Chars<'_>>) -> String {
    let mut entity = String::new();
    
    // Collect entity characters until ';' or end
    while let Some(c) = chars.peek() {
        if *c == ';' {
            chars.next();
            break;
        }
        entity.push(chars.next().unwrap());
    }
    
    // Parse the entity
    if entity.is_empty() {
        return "&".to_string();
    }
    
    // Named entities
    match entity.as_str() {
        "amp" => return "&".to_string(),
        "lt" => return "<".to_string(),
        "gt" => return ">".to_string(),
        "quot" => return "\"".to_string(),
        "apos" => return "'".to_string(),
        "nbsp" => return "\u{00A0}".to_string(),
        "copy" => return "\u{00A9}".to_string(),
        "reg" => return "\u{00AE}".to_string(),
        "euro" => return "\u{20AC}".to_string(),
        _ => {}
    }
    
    // Numeric entities
    if entity.starts_with('#') {
        let num_part = &entity[1..];
        if num_part.starts_with('x') || num_part.starts_with('X') {
            // Hexadecimal
            let hex = &num_part[1..];
            if let Ok(code) = u32::from_str_radix(hex, 16) {
                if let Some(c) = char::from_u32(code) {
                    return c.to_string();
                }
            }
        } else {
            // Decimal
            if let Ok(code) = num_part.parse::<u32>() {
                if let Some(c) = char::from_u32(code) {
                    return c.to_string();
                }
            }
        }
    }
    
    // Unknown entity, return as-is with &
    format!("&{};", entity)
}

// ============================================================================
// URL Escape Functions
// ============================================================================

/// URL encoding (percent encoding).
///
/// Encodes characters that are not safe for URLs.
///
/// # Examples
///
/// ```
/// use escape_utils::escape_url;
///
/// assert_eq!(escape_url("hello world"), "hello%20world");
/// assert_eq!(escape_url("a=1&b=2"), "a%3D1%26b%3D2");
/// ```
pub fn escape_url(s: &str) -> String {
    let mut result = String::with_capacity(s.len() * 3);
    
    for c in s.chars() {
        match c {
            // Safe characters (RFC 3986 unreserved)
            'A'..='Z' | 'a'..='z' | '0'..='9' | '-' | '.' | '_' | '~' => {
                result.push(c);
            }
            // Encode everything else
            _ => {
                for byte in c.to_string().as_bytes() {
                    result.push_str(&format!("%{:02X}", byte));
                }
            }
        }
    }
    
    result
}

/// URL decoding (percent decoding).
///
/// Decodes %XX encoded characters.
///
/// # Examples
///
/// ```
/// use escape_utils::unescape_url;
///
/// assert_eq!(unescape_url("hello%20world"), "hello world");
/// assert_eq!(unescape_url("a%3D1%26b%3D2"), "a=1&b=2");
/// ```
pub fn unescape_url(s: &str) -> Cow<'_, str> {
    if !s.contains('%') {
        return Cow::Borrowed(s);
    }
    
    let mut result = String::with_capacity(s.len());
    let bytes = s.as_bytes();
    let mut i = 0;
    
    while i < bytes.len() {
        if bytes[i] == b'%' && i + 2 < bytes.len() {
            let hex = &s[i + 1..i + 3];
            if let Ok(code) = u8::from_str_radix(hex, 16) {
                result.push(code as char);
                i += 3;
                continue;
            }
        }
        result.push(bytes[i] as char);
        i += 1;
    }
    
    Cow::Owned(result)
}

// ============================================================================
// JSON String Escape Functions
// ============================================================================

/// JSON string escape.
///
/// Escapes characters for safe inclusion in JSON strings.
///
/// # Examples
///
/// ```
/// use escape_utils::escape_json;
///
/// assert_eq!(escape_json("He said \"Hi\""), "He said \\\"Hi\\\"");
/// assert_eq!(escape_json("Line1\nLine2"), "Line1\\nLine2");
/// ```
pub fn escape_json(s: &str) -> String {
    let mut result = String::with_capacity(s.len() * 2);
    
    for c in s.chars() {
        match c {
            '\\' => result.push_str("\\\\"),
            '"' => result.push_str("\\\""),
            '\n' => result.push_str("\\n"),
            '\r' => result.push_str("\\r"),
            '\t' => result.push_str("\\t"),
            '\x08' => result.push_str("\\b"),  // Backspace
            '\x0C' => result.push_str("\\f"),  // Form feed
            c if c < '\x20' => {
                // Control characters as \uXXXX
                result.push_str(&format!("\\u{:04X}", c as u32));
            }
            _ => result.push(c),
        }
    }
    
    result
}

/// JSON string unescape.
///
/// Unescapes JSON string escape sequences.
///
/// # Examples
///
/// ```
/// use escape_utils::unescape_json;
///
/// assert_eq!(unescape_json("Line1\\nLine2"), "Line1\nLine2");
/// assert_eq!(unescape_json("\\u4F60\\u597D"), "你好");
/// ```
pub fn unescape_json(s: &str) -> Cow<'_, str> {
    if !s.contains('\\') {
        return Cow::Borrowed(s);
    }
    
    let mut result = String::with_capacity(s.len());
    let mut chars = s.chars().peekable();
    
    while let Some(c) = chars.next() {
        if c == '\\' {
            if let Some(next) = chars.next() {
                match next {
                    '"' => result.push('"'),
                    '\\' => result.push('\\'),
                    '/' => result.push('/'),
                    'n' => result.push('\n'),
                    'r' => result.push('\r'),
                    't' => result.push('\t'),
                    'b' => result.push('\x08'),
                    'f' => result.push('\x0C'),
                    'u' => {
                        // Parse \uXXXX
                        let hex: String = chars.by_ref().take(4).collect();
                        if let Ok(code) = u32::from_str_radix(&hex, 16) {
                            if let Some(uc) = char::from_u32(code) {
                                result.push(uc);
                            }
                        }
                    }
                    _ => {
                        result.push('\\');
                        result.push(next);
                    }
                }
            }
        } else {
            result.push(c);
        }
    }
    
    Cow::Owned(result)
}

// ============================================================================
// Shell Escape Functions
// ============================================================================

/// Shell argument escape (POSIX compliant, single-quote style).
///
/// Wraps argument in single quotes, handling embedded single quotes.
///
/// # Examples
///
/// ```
/// use escape_utils::escape_shell_arg;
///
/// assert_eq!(escape_shell_arg("hello"), "hello");
/// assert_eq!(escape_shell_arg("hello world"), "'hello world'");
/// assert_eq!(escape_shell_arg("it's fine"), "'it'\"'\"'s fine'");
/// ```
pub fn escape_shell_arg(s: &str) -> Cow<'_, str> {
    if s.is_empty() {
        return Cow::Borrowed("''");
    }
    
    // Check if it's safe (alphanumeric and some safe chars)
    if s.chars().all(|c| c.is_ascii_alphanumeric() || c == '.' || c == '-' || c == '_' || c == '/') {
        return Cow::Borrowed(s);
    }
    
    // Contains single quote - need special handling
    if s.contains('\'') {
        // POSIX style: 'it'"'"'s' = "it" + "'" + "s"
        let escaped = s.replace("'", "'\"'\"'");
        return Cow::Owned(format!("'{}'", escaped));
    }
    
    // No single quote - just wrap in single quotes
    Cow::Owned(format!("'{}'", s))
}

/// Shell command escape.
///
/// Escapes special characters for shell commands.
///
/// # Examples
///
/// ```
/// use escape_utils::escape_shell;
///
/// assert_eq!(escape_shell("echo hello"), "echo\\ hello");
/// ```
pub fn escape_shell(s: &str) -> String {
    let mut result = String::with_capacity(s.len() * 2);
    
    for c in s.chars() {
        match c {
            'A'..='Z' | 'a'..='z' | '0'..='9' | '_' | '.' | ',' | ':' | '/' | '@' | '-' => {
                result.push(c);
            }
            _ => {
                result.push('\\');
                result.push(c);
            }
        }
    }
    
    result
}

// ============================================================================
// Regex Escape Functions
// ============================================================================

/// Regex pattern escape.
///
/// Escapes regex special characters for literal matching.
///
/// # Examples
///
/// ```
/// use escape_utils::escape_regex;
///
/// assert_eq!(escape_regex("a.b"), "a\\.b");
/// assert_eq!(escape_regex("(group)"), "\\(group\\)");
/// ```
pub fn escape_regex(s: &str) -> String {
    let special = ['\\', '.', '^', '$', '*', '+', '?', '{', '}', '[', ']', '(', ')', '|', '#', '-', '&'];
    
    if !s.chars().any(|c| special.contains(&c)) {
        return s.to_string();
    }
    
    let mut result = String::with_capacity(s.len() * 2);
    
    for c in s.chars() {
        if special.contains(&c) {
            result.push('\\');
        }
        result.push(c);
    }
    
    result
}

// ============================================================================
// Unicode Escape Functions
// ============================================================================

/// Unicode escape (to \uXXXX format).
///
/// Escapes non-ASCII characters.
///
/// # Examples
///
/// ```
/// use escape_utils::escape_unicode;
///
/// assert_eq!(escape_unicode("你好"), "\\u4F60\\u597D");
/// ```
pub fn escape_unicode(s: &str) -> String {
    let mut result = String::with_capacity(s.len() * 6);
    
    for c in s.chars() {
        if (c as u32) < 0x80 {
            result.push(c);
        } else {
            result.push_str(&format!("\\u{:04X}", c as u32));
        }
    }
    
    result
}

/// Unicode unescape (from \uXXXX format).
///
/// # Examples
///
/// ```
/// use escape_utils::unescape_unicode;
///
/// assert_eq!(unescape_unicode("\\u4F60\\u597D"), "你好");
/// ```
pub fn unescape_unicode(s: &str) -> Cow<'_, str> {
    if !s.contains("\\u") {
        return Cow::Borrowed(s);
    }
    
    let mut result = String::with_capacity(s.len());
    let mut chars = s.chars().peekable();
    
    while let Some(c) = chars.next() {
        if c == '\\' && chars.peek() == Some(&'u') {
            chars.next(); // consume 'u'
            let hex: String = chars.by_ref().take(4).collect();
            if let Ok(code) = u32::from_str_radix(&hex, 16) {
                if let Some(uc) = char::from_u32(code) {
                    result.push(uc);
                    continue;
                }
            }
            // Failed to parse, restore original
            result.push('\\');
            result.push('u');
            result.push_str(&hex);
        } else {
            result.push(c);
        }
    }
    
    Cow::Owned(result)
}

// ============================================================================
// XML Attribute Escape Functions
// ============================================================================

/// XML attribute escape.
///
/// Escapes characters for safe XML attribute values.
///
/// # Examples
///
/// ```
/// use escape_utils::escape_xml_attr;
///
/// assert_eq!(escape_xml_attr("<tag>"), "&lt;tag&gt;");
/// ```
pub fn escape_xml_attr(s: &str) -> String {
    let mut result = String::with_capacity(s.len() * 2);
    
    for c in s.chars() {
        match c {
            '&' => result.push_str("&amp;"),
            '<' => result.push_str("&lt;"),
            '>' => result.push_str("&gt;"),
            '"' => result.push_str("&quot;"),
            '\'' => result.push_str("&apos;"),
            '\t' => result.push_str("&#x9;"),
            '\n' => result.push_str("&#xA;"),
            '\r' => result.push_str("&#xD;"),
            _ => result.push(c),
        }
    }
    
    result
}

/// XML attribute unescape.
///
/// # Examples
///
/// ```
/// use escape_utils::unescape_xml_attr;
///
/// assert_eq!(unescape_xml_attr("&lt;tag&gt;"), "<tag>");
/// ```
pub fn unescape_xml_attr(s: &str) -> String {
    let mut result = s.to_string();
    
    result = result.replace("&#xD;", "\r");
    result = result.replace("&#xA;", "\n");
    result = result.replace("&#x9;", "\t");
    result = result.replace("&apos;", "'");
    result = result.replace("&quot;", "\"");
    result = result.replace("&gt;", ">");
    result = result.replace("&lt;", "<");
    result = result.replace("&amp;", "&");
    
    result
}

// ============================================================================
// SQL String Escape Functions
// ============================================================================

/// SQL string escape (basic protection).
///
/// **Warning**: This is basic protection. For production, use prepared statements!
///
/// # Examples
///
/// ```
/// use escape_utils::escape_sql_string;
///
/// assert_eq!(escape_sql_string("O'Brien"), "O''Brien");
/// ```
pub fn escape_sql_string(s: &str) -> String {
    s.replace("'", "''")
        .replace("\\", "\\\\")
        .replace("\x00", "\\0")
}

/// SQL LIKE pattern escape.
///
/// # Examples
///
/// ```
/// use escape_utils::escape_sql_like;
///
/// assert_eq!(escape_sql_like("100%"), "100\\%");
/// ```
pub fn escape_sql_like(s: &str, escape_char: char) -> String {
    let esc = escape_char.to_string();
    s.replace("%", &format!("{}%", esc))
        .replace("_", &format!("{}_", esc))
}

// ============================================================================
// CSV Field Escape Functions
// ============================================================================

/// CSV field escape.
///
/// Escapes fields for CSV format according to RFC 4180.
///
/// # Examples
///
/// ```
/// use escape_utils::escape_csv_field;
///
/// assert_eq!(escape_csv_field("hello"), "hello");
/// assert_eq!(escape_csv_field("a,b"), "\"a,b\"");
/// assert_eq!(escape_csv_field("a\"b"), "\"a\"\"b\"");
/// ```
pub fn escape_csv_field(s: &str) -> Cow<'_, str> {
    let needs_quoting = s.contains(',') || s.contains('"') || s.contains('\n') || s.contains('\r');
    
    if !needs_quoting {
        return Cow::Borrowed(s);
    }
    
    let escaped = s.replace("\"", "\"\"");
    Cow::Owned(format!("\"{}\"", escaped))
}

/// CSV field unescape.
///
/// # Examples
///
/// ```
/// use escape_utils::unescape_csv_field;
///
/// assert_eq!(unescape_csv_field("\"a\"\"b\""), "a\"b");
/// ```
pub fn unescape_csv_field(s: &str) -> Cow<'_, str> {
    if !s.starts_with('"') || !s.ends_with('"') {
        return Cow::Borrowed(s);
    }
    
    let inner = &s[1..s.len()-1];
    Cow::Owned(inner.replace("\"\"", "\""))
}

// ============================================================================
// C-Style String Escape Functions
// ============================================================================

/// C-style string escape.
///
/// # Examples
///
/// ```
/// use escape_utils::escape_c_string;
///
/// assert_eq!(escape_c_string("Line1\nLine2"), "Line1\\nLine2");
/// ```
pub fn escape_c_string(s: &str) -> String {
    let mut result = String::with_capacity(s.len() * 2);
    
    for c in s.chars() {
        match c {
            '\\' => result.push_str("\\\\"),
            '"' => result.push_str("\\\""),
            '\'' => result.push_str("\\\'"),
            '\x07' => result.push_str("\\a"), // Bell
            '\x08' => result.push_str("\\b"), // Backspace
            '\x0C' => result.push_str("\\f"), // Form feed
            '\n' => result.push_str("\\n"),
            '\r' => result.push_str("\\r"),
            '\t' => result.push_str("\\t"),
            '\x0B' => result.push_str("\\v"), // Vertical tab
            _ => result.push(c),
        }
    }
    
    result
}

/// C-style string unescape.
///
/// # Examples
///
/// ```
/// use escape_utils::unescape_c_string;
///
/// assert_eq!(unescape_c_string("Line1\\nLine2"), "Line1\nLine2");
/// ```
pub fn unescape_c_string(s: &str) -> Cow<'_, str> {
    if !s.contains('\\') {
        return Cow::Borrowed(s);
    }
    
    let mut result = String::with_capacity(s.len());
    let mut chars = s.chars().peekable();
    
    while let Some(c) = chars.next() {
        if c == '\\' {
            if let Some(next) = chars.next() {
                match next {
                    'a' => result.push('\x07'),
                    'b' => result.push('\x08'),
                    'f' => result.push('\x0C'),
                    'n' => result.push('\n'),
                    'r' => result.push('\r'),
                    't' => result.push('\t'),
                    'v' => result.push('\x0B'),
                    '"' => result.push('"'),
                    '\'' => result.push('\''),
                    '\\' => result.push('\\'),
                    'x' => {
                        // Hex escape \xNN
                        let hex: String = chars.by_ref().take(2).collect();
                        if let Ok(code) = u8::from_str_radix(&hex, 16) {
                            result.push(code as char);
                        }
                    }
                    '0'..='7' => {
                        // Octal escape \0NN or \NN
                        let mut octal = String::from(next);
                        for _ in 0..2 {
                            if let Some(&c) = chars.peek() {
                                if c >= '0' && c <= '7' {
                                    octal.push(chars.next().unwrap());
                                } else {
                                    break;
                                }
                            }
                        }
                        if let Ok(code) = u8::from_str_radix(&octal, 8) {
                            result.push(code as char);
                        }
                    }
                    _ => {
                        result.push('\\');
                        result.push(next);
                    }
                }
            }
        } else {
            result.push(c);
        }
    }
    
    Cow::Owned(result)
}

// ============================================================================
// Utility Functions
// ============================================================================

/// Check if a string needs escaping for a given context.
///
/// # Examples
///
/// ```
/// use escape_utils::needs_escape;
///
/// assert_eq!(needs_escape("<div>", "html"), true);
/// assert_eq!(needs_escape("hello", "html"), false);
/// ```
pub fn needs_escape(s: &str, context: &str) -> bool {
    match context {
        "html" => s.contains(&['&', '<', '>', '"', '\''][..]),
        "url" => !s.chars().all(|c| c.is_ascii_alphanumeric() || c == '-' || c == '.' || c == '_' || c == '~'),
        "json" => s.contains(&['"', '\\', '\n', '\r', '\t'][..]),
        "sql" => s.contains("'") || s.contains("\\") || s.contains("\x00"),
        "shell" => !s.chars().all(|c| c.is_ascii_alphanumeric() || c == '.' || c == '-' || c == '_' || c == '/'),
        "regex" => s.contains(&['\\', '.', '^', '$', '*', '+', '?', '{', '}', '[', ']', '(', ')', '|'][..]),
        "csv" => s.contains(',') || s.contains('"') || s.contains('\n') || s.contains('\r'),
        _ => false,
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    
    #[test]
    fn test_escape_html() {
        assert_eq!(escape_html("<div>"), "&lt;div&gt;");
        assert_eq!(escape_html("a & b"), "a &amp; b");
        assert_eq!(escape_html("it's"), "it&#39;s");
        assert_eq!(escape_html("<a>&'\""), "&lt;a&gt;&amp;&#39;&quot;");
    }
    
    #[test]
    fn test_unescape_html() {
        assert_eq!(unescape_html("&lt;div&gt;"), "<div>");
        assert_eq!(unescape_html("a &amp; b"), "a & b");
        assert_eq!(unescape_html("&#39;"), "'");
        assert_eq!(unescape_html("&#x27;"), "'");
    }
    
    #[test]
    fn test_escape_url() {
        assert_eq!(escape_url("hello world"), "hello%20world");
        assert_eq!(escape_url("a=1&b=2"), "a%3D1%26b%3D2");
    }
    
    #[test]
    fn test_unescape_url() {
        assert_eq!(unescape_url("hello%20world"), "hello world");
        assert_eq!(unescape_url("a%3D1%26b%3D2"), "a=1&b=2");
    }
    
    #[test]
    fn test_escape_json() {
        assert_eq!(escape_json("He said \"Hi\""), "He said \\\"Hi\\\"");
        assert_eq!(escape_json("Line1\nLine2"), "Line1\\nLine2");
        assert_eq!(escape_json("a\\b"), "a\\\\b");
    }
    
    #[test]
    fn test_unescape_json() {
        assert_eq!(unescape_json("Line1\\nLine2"), "Line1\nLine2");
        assert_eq!(unescape_json("a\\\\b"), "a\\b");
    }
    
    #[test]
    fn test_escape_shell_arg() {
        assert_eq!(escape_shell_arg("hello"), "hello");
        assert_eq!(escape_shell_arg("hello world"), "'hello world'");
        assert_eq!(escape_shell_arg("it's fine"), "'it'\"'\"'s fine'");
        assert_eq!(escape_shell_arg(""), "''");
    }
    
    #[test]
    fn test_escape_regex() {
        assert_eq!(escape_regex("a.b"), "a\\.b");
        assert_eq!(escape_regex("(group)"), "\\(group\\)");
        assert_eq!(escape_regex("[abc]"), "\\[abc\\]");
    }
    
    #[test]
    fn test_escape_unicode() {
        assert_eq!(escape_unicode("你好"), "\\u4F60\\u597D");
        assert_eq!(escape_unicode("hello"), "hello");
    }
    
    #[test]
    fn test_unescape_unicode() {
        assert_eq!(unescape_unicode("\\u4F60\\u597D"), "你好");
    }
    
    #[test]
    fn test_escape_sql_string() {
        assert_eq!(escape_sql_string("O'Brien"), "O''Brien");
        assert_eq!(escape_sql_string("test\\value"), "test\\\\value");
    }
    
    #[test]
    fn test_escape_csv_field() {
        assert_eq!(escape_csv_field("hello"), "hello");
        assert_eq!(escape_csv_field("a,b"), "\"a,b\"");
        assert_eq!(escape_csv_field("a\"b"), "\"a\"\"b\"");
    }
    
    #[test]
    fn test_unescape_csv_field() {
        assert_eq!(unescape_csv_field("hello"), "hello");
        assert_eq!(unescape_csv_field("\"a,b\""), "a,b");
        assert_eq!(unescape_csv_field("\"a\"\"b\""), "a\"b");
    }
    
    #[test]
    fn test_escape_c_string() {
        assert_eq!(escape_c_string("Line1\nLine2"), "Line1\\nLine2");
        assert_eq!(escape_c_string("a\\b"), "a\\\\b");
    }
    
    #[test]
    fn test_unescape_c_string() {
        assert_eq!(unescape_c_string("Line1\\nLine2"), "Line1\nLine2");
        assert_eq!(unescape_c_string("a\\\\b"), "a\\b");
    }
    
    #[test]
    fn test_needs_escape() {
        assert_eq!(needs_escape("<div>", "html"), true);
        assert_eq!(needs_escape("hello", "html"), false);
        assert_eq!(needs_escape("hello world", "url"), true);
    }
}