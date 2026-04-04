//! JSON Utilities Module for Rust
//!
//! A zero-dependency JSON parsing and generation library.
//! Provides complete JSON support with type-safe access and pretty printing.
//!
//! # Features
//! - Zero dependencies, uses only Rust standard library
//! - Complete JSON support: null, boolean, number, string, array, object
//! - Type-safe access with default values
//! - Pretty printing with customizable indentation
//! - Round-trip parsing (parse → generate → parse)
//! - Safe parsing with Result return type
//!
//! # Example
//! ```rust
//! use json_utils::{JsonValue, parse_json};
//!
//! // Parse JSON
//! let json = r#"{"name": "John", "age": 30}"#;
//! let value = parse_json(json).unwrap();
//!
//! // Access values
//! let name = value.get("name").as_string();
//! let age = value.get("age").as_i64();
//! ```

use std::collections::HashMap;
use std::fmt;

/// Represents any JSON value
#[derive(Debug, Clone, PartialEq)]
pub enum JsonValue {
    Null,
    Bool(bool),
    Number(f64),
    String(String),
    Array(Vec<JsonValue>),
    Object(HashMap<String, JsonValue>),
}

/// Error type for JSON parsing
#[derive(Debug, Clone, PartialEq)]
pub enum JsonError {
    UnexpectedChar { expected: char, found: char, position: usize },
    UnexpectedEndOfInput,
    InvalidNumber { text: String, position: usize },
    InvalidEscape { escape: char, position: usize },
    InvalidUnicode { text: String, position: usize },
    InvalidValue { text: String, position: usize },
    Custom(String),
}

impl fmt::Display for JsonError {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        match self {
            JsonError::UnexpectedChar { expected, found, position } => {
                write!(f, "Expected '{}' but found '{}' at position {}", expected, found, position)
            }
            JsonError::UnexpectedEndOfInput => write!(f, "Unexpected end of input"),
            JsonError::InvalidNumber { text, position } => {
                write!(f, "Invalid number '{}' at position {}", text, position)
            }
            JsonError::InvalidEscape { escape, position } => {
                write!(f, "Invalid escape sequence '\\{}' at position {}", escape, position)
            }
            JsonError::InvalidUnicode { text, position } => {
                write!(f, "Invalid unicode escape '{}' at position {}", text, position)
            }
            JsonError::InvalidValue { text, position } => {
                write!(f, "Invalid value '{}' at position {}", text, position)
            }
            JsonError::Custom(msg) => write!(f, "{}", msg),
        }
    }
}

impl std::error::Error for JsonError {}

/// Result type for JSON operations
pub type JsonResult<T> = Result<T, JsonError>;

impl JsonValue {
    /// Creates a null JSON value
    pub fn null() -> Self {
        JsonValue::Null
    }

    /// Creates a boolean JSON value
    pub fn bool(value: bool) -> Self {
        JsonValue::Bool(value)
    }

    /// Creates a number JSON value
    pub fn number(value: f64) -> Self {
        JsonValue::Number(value)
    }

    /// Creates a string JSON value
    pub fn string(value: impl Into<String>) -> Self {
        JsonValue::String(value.into())
    }

    /// Creates an array JSON value
    pub fn array(values: Vec<JsonValue>) -> Self {
        JsonValue::Array(values)
    }

    /// Creates an object JSON value
    pub fn object(values: HashMap<String, JsonValue>) -> Self {
        JsonValue::Object(values)
    }

    /// Returns true if the value is null
    pub fn is_null(&self) -> bool {
        matches!(self, JsonValue::Null)
    }

    /// Returns true if the value is a boolean
    pub fn is_bool(&self) -> bool {
        matches!(self, JsonValue::Bool(_))
    }

    /// Returns true if the value is a number
    pub fn is_number(&self) -> bool {
        matches!(self, JsonValue::Number(_))
    }

    /// Returns true if the value is a string
    pub fn is_string(&self) -> bool {
        matches!(self, JsonValue::String(_))
    }

    /// Returns true if the value is an array
    pub fn is_array(&self) -> bool {
        matches!(self, JsonValue::Array(_))
    }

    /// Returns true if the value is an object
    pub fn is_object(&self) -> bool {
        matches!(self, JsonValue::Object(_))
    }

    /// Returns the boolean value, or default if not a boolean
    pub fn as_bool(&self) -> bool {
        match self {
            JsonValue::Bool(b) => *b,
            _ => false,
        }
    }

    /// Returns the boolean value with a default
    pub fn as_bool_or(&self, default: bool) -> bool {
        match self {
            JsonValue::Bool(b) => *b,
            _ => default,
        }
    }

    /// Returns the number as f64, or 0.0 if not a number
    pub fn as_f64(&self) -> f64 {
        match self {
            JsonValue::Number(n) => *n,
            _ => 0.0,
        }
    }

    /// Returns the number as f64 with a default
    pub fn as_f64_or(&self, default: f64) -> f64 {
        match self {
            JsonValue::Number(n) => *n,
            _ => default,
        }
    }

    /// Returns the number as i64, or 0 if not a number
    pub fn as_i64(&self) -> i64 {
        match self {
            JsonValue::Number(n) => *n as i64,
            _ => 0,
        }
    }

    /// Returns the number as i64 with a default
    pub fn as_i64_or(&self, default: i64) -> i64 {
        match self {
            JsonValue::Number(n) => *n as i64,
            _ => default,
        }
    }

    /// Returns the string value, or empty string if not a string
    pub fn as_string(&self) -> String {
        match self {
            JsonValue::String(s) => s.clone(),
            _ => String::new(),
        }
    }

    /// Returns the string value with a default
    pub fn as_string_or(&self, default: impl Into<String>) -> String {
        match self {
            JsonValue::String(s) => s.clone(),
            _ => default.into(),
        }
    }

    /// Returns the array, or empty array if not an array
    pub fn as_array(&self) -> Vec<JsonValue> {
        match self {
            JsonValue::Array(a) => a.clone(),
            _ => Vec::new(),
        }
    }

    /// Returns the object, or empty object if not an object
    pub fn as_object(&self) -> HashMap<String, JsonValue> {
        match self {
            JsonValue::Object(o) => o.clone(),
            _ => HashMap::new(),
        }
    }

    /// Gets a value from an object by key
    pub fn get(&self, key: &str) -> &JsonValue {
        match self {
            JsonValue::Object(o) => o.get(key).unwrap_or(&JsonValue::Null),
            _ => &JsonValue::Null,
        }
    }

    /// Gets a value from an array by index
    pub fn get_index(&self, index: usize) -> &JsonValue {
        match self {
            JsonValue::Array(a) => a.get(index).unwrap_or(&JsonValue::Null),
            _ => &JsonValue::Null,
        }
    }

    /// Returns true if the object has the key
    pub fn has(&self, key: &str) -> bool {
        match self {
            JsonValue::Object(o) => o.contains_key(key),
            _ => false,
        }
    }

    /// Returns the length of an array or object
    pub fn len(&self) -> usize {
        match self {
            JsonValue::Array(a) => a.len(),
            JsonValue::Object(o) => o.len(),
            _ => 0,
        }
    }

    /// Returns true if the array or object is empty
    pub fn is_empty(&self) -> bool {
        self.len() == 0
    }

    /// Returns all keys of an object
    pub fn keys(&self) -> Vec<String> {
        match self {
            JsonValue::Object(o) => o.keys().cloned().collect(),
            _ => Vec::new(),
        }
    }

    /// Converts the JSON value to a compact JSON string
    pub fn to_json(&self) -> String {
        self.to_string()
    }

    /// Converts the JSON value to a pretty-printed JSON string
    pub fn to_pretty_json(&self) -> String {
        self.to_pretty_string_with_indent(2)
    }

    /// Converts the JSON value to a pretty-printed JSON string with custom indent
    pub fn to_pretty_string_with_indent(&self, indent: usize) -> String {
        self.format_pretty(0, indent)
    }

    fn format_pretty(&self, depth: usize, indent: usize) -> String {
        let indent_str = " ".repeat(depth * indent);
        let next_indent_str = " ".repeat((depth + 1) * indent);

        match self {
            JsonValue::Null => "null".to_string(),
            JsonValue::Bool(b) => b.to_string(),
            JsonValue::Number(n) => {
                if n.is_finite() {
                    if n.fract() == 0.0 {
                        format!("{:.0}", n)
                    } else {
                        format!("{}", n)
                    }
                } else {
                    "null".to_string()
                }
            }
            JsonValue::String(s) => format_json_string(s),
            JsonValue::Array(arr) => {
                if arr.is_empty() {
                    "[]".to_string()
                } else {
                    let items: Vec<String> = arr
                        .iter()
                        .map(|v| format!("\n{}{}", next_indent_str, v.format_pretty(depth + 1, indent)))
                        .collect();
                    format!("[{},{}
{}]", items.join(","), indent_str, indent_str)
                }
            }
            JsonValue::Object(obj) => {
                if obj.is_empty() {
                    "{}".to_string()
                } else {
                    let items: Vec<String> = obj
                        .iter()
                        .map(|(k, v)| {
                            format!(
                                "\n{}{}: {}",
                                next_indent_str,
                                format_json_string(k),
                                v.format_pretty(depth + 1, indent)
                            )
                        })
                        .collect();
                    format!("{{{},\n{}}}", items.join(","), indent_str)
                }
            }
        }
    }

    /// Merges another JSON object into this one (only works for objects)
    pub fn merge(&mut self, other: &JsonValue) {
        if let (JsonValue::Object(self_obj), JsonValue::Object(other_obj)) = (self, other) {
            for (k, v) in other_obj.iter() {
                self_obj.insert(k.clone(), v.clone());
            }
        }
    }
}

impl fmt::Display for JsonValue {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        match self {
            JsonValue::Null => write!(f, "null"),
            JsonValue::Bool(b) => write!(f, "{}", b),
            JsonValue::Number(n) => {
                if n.is_finite() {
                    if n.fract() == 0.0 {
                        write!(f, "{:.0}", n)
                    } else {
                        write!(f, "{}", n)
                    }
                } else {
                    write!(f, "null")
                }
            }
            JsonValue::String(s) => write!(f, "{}", format_json_string(s)),
            JsonValue::Array(arr) => {
                write!(f, "[")?;
                for (i, v) in arr.iter().enumerate() {
                    if i > 0 {
                        write!(f, ",")?;
                    }
                    write!(f, "{}", v)?;
                }
                write!(f, "]")
            }
            JsonValue::Object(obj) => {
                write!(f, "{{")?;
                let mut first = true;
                for (k, v) in obj.iter() {
                    if !first {
                        write!(f, ",")?;
                    }
                    first = false;
                    write!(f, "{}:{}", format_json_string(k), v)?;
                }
                write!(f, "}}")
            }
        }
    }
}

/// Formats a string for JSON output with proper escaping
fn format_json_string(s: &str) -> String {
    let mut result = String::with_capacity(s.len() + 2);
    result.push('"');
    for c in s.chars() {
        match c {
            '"' => result.push_str("\\\""),
            '\\' => result.push_str("\\\\"),
            '\n' => result.push_str("\\n"),
            '\r' => result.push_str("\\r"),
            '\t' => result.push_str("\\t"),
            '\x08' => result.push_str("\\b"),
            '\x0C' => result.push_str("\\f"),
            c if c < '\x20' => {
                result.push_str(&format!("\\u{:04x}", c as u32));
            }
            c => result.push(c),
        }
    }
    result.push('"');
    result
}

/// Parses a JSON string into a JsonValue
pub fn parse_json(input: &str) -> JsonResult<JsonValue> {
    let mut parser = JsonParser::new(input);
    parser.parse()
}

/// Parses a JSON string, returning null on error
pub fn parse_json_or_null(input: &str) -> JsonValue {
    parse_json(input).unwrap_or(JsonValue::Null)
}

/// Validates if a string is valid JSON
pub fn is_valid_json(input: &str) -> bool {
    parse_json(input).is_ok()
}

/// Creates a JSON object from key-value pairs
pub fn json_object() -> JsonValue {
    JsonValue::Object(HashMap::new())
}

/// Creates a JSON array from values
pub fn json_array() -> JsonValue {
    JsonValue::Array(Vec::new())
}

/// Converts a value to JsonValue
pub fn to_json_value<T: Into<JsonValue>>(value: T) -> JsonValue {
    value.into()
}

// Implement Into<JsonValue> for common types
impl From<()> for JsonValue {
    fn from(_: ()) -> Self {
        JsonValue::Null
    }
}

impl From<bool> for JsonValue {
    fn from(value: bool) -> Self {
        JsonValue::Bool(value)
    }
}

impl From<i8> for JsonValue {
    fn from(value: i8) -> Self {
        JsonValue::Number(value as f64)
    }
}

impl From<i16> for JsonValue {
    fn from(value: i16) -> Self {
        JsonValue::Number(value as f64)
    }
}

impl From<i32> for JsonValue {
    fn from(value: i32) -> Self {
        JsonValue::Number(value as f64)
    }
}

impl From<i64> for JsonValue {
    fn from(value: i64) -> Self {
        JsonValue::Number(value as f64)
    }
}

impl From<u8> for JsonValue {
    fn from(value: u8) -> Self {
        JsonValue::Number(value as f64)
    }
}

impl From<u16> for JsonValue {
    fn from(value: u16) -> Self {
        JsonValue::Number(value as f64)
    }
}

impl From<u32> for JsonValue {
    fn from(value: u32) -> Self {
        JsonValue::Number(value as f64)
    }
}

impl From<u64> for JsonValue {
    fn from(value: u64) -> Self {
        JsonValue::Number(value as f64)
    }
}

impl From<f32> for JsonValue {
    fn from(value: f32) -> Self {
        JsonValue::Number(value as f64)
    }
}

impl From<f64> for JsonValue {
    fn from(value: f64) -> Self {
        JsonValue::Number(value)
    }
}

impl From<String> for JsonValue {
    fn from(value: String) -> Self {
        JsonValue::String(value)
    }
}

impl From<&str> for JsonValue {
    fn from(value: &str) -> Self {
        JsonValue::String(value.to_string())
    }
}

impl<T: Into<JsonValue>> From<Vec<T>> for JsonValue {
    fn from(value: Vec<T>) -> Self {
        JsonValue::Array(value.into_iter().map(|v| v.into()).collect())
    }
}

impl<T: Into<JsonValue>> From<HashMap<String, T>> for JsonValue {
    fn from(value: HashMap<String, T>) -> Self {
        JsonValue::Object(value.into_iter().map(|(k, v)| (k, v.into())).collect())
    }
}

impl<T: Into<JsonValue>> From<Option<T>> for JsonValue {
    fn from(value: Option<T>) -> Self {
        match value {
            Some(v) => v.into(),
            None => JsonValue::Null,
        }
    }
}

// JSON Parser implementation
struct JsonParser {
    input: String,
    position: usize,
}

impl JsonParser {
    fn new(input: &str) -> Self {
        JsonParser {
            input: input.to_string(),
            position: 0,
        }
    }

    fn parse(&mut self) -> JsonResult<JsonValue> {
        self.skip_whitespace();
        let value = self.parse_value()?;
        self.skip_whitespace();
        if !self.is_at_end() {
            return Err(JsonError::InvalidValue {
                text: self.input.clone(),
                position: self.position,
            });
        }
        Ok(value)
    }

    fn parse_value(&mut self) -> JsonResult<JsonValue> {
        self.skip_whitespace();

        if self.is_at_end() {
            return Err(JsonError::UnexpectedEndOfInput);
        }

        match self.peek() {
            Some('n') => self.parse_null(),
            Some('t') | Some('f') => self.parse_bool(),
            Some('"') => self.parse_string(),
            Some('[') => self.parse_array(),
            Some('{') => self.parse_object(),
            Some(c) if c == '-' || c.is_ascii_digit() => self.parse_number(),
            Some(c) => Err(JsonError::InvalidValue {
                text: c.to_string(),
                position: self.position,
            }),
            None => Err(JsonError::UnexpectedEndOfInput),
        }
    }

    fn parse_null(&mut self) -> JsonResult<JsonValue> {
        self.expect_keyword("null")?;
        Ok(JsonValue::Null)
    }

    fn parse_bool(&mut self) -> JsonResult<JsonValue> {
        if self.peek() == Some('t') {
            self.expect_keyword("true")?;
            Ok(JsonValue::Bool(true))
        } else {
            self.expect_keyword("false")?;
            Ok(JsonValue::Bool(false))
        }
    }

    fn parse_number(&mut self) -> JsonResult<JsonValue> {
        let start = self.position;

        // Optional minus sign
        if self.peek() == Some('-') {
            self.advance();
        }

        // Integer part
        if self.peek() == Some('0') {
            self.advance();
        } else if self.peek().map(|c| c.is_ascii_digit()).unwrap_or(false) {
            while self.peek().map(|c| c.is_ascii_digit()).unwrap_or(false) {
                self.advance();
            }
        } else {
            return Err(JsonError::InvalidNumber {
                text: self.input[start..self.position].to_string(),
                position: start,
            });
        }

        // Fractional part
        if self.peek() == Some('.') {
            self.advance();
            if !self.peek().map(|c| c.is_ascii_digit()).unwrap_or(false) {
                return Err(JsonError::InvalidNumber {
                    text: self.input[start..self.position].to_string(),
                    position: self.position,
                });
            }
            while self.peek().map(|c| c.is_ascii_digit()).unwrap_or(false) {
                self.advance();
            }
        }

        // Exponent part
        if self.peek().map(|c| c == 'e' || c == 'E').unwrap_or(false) {
            self.advance();
            if self.peek().map(|c| c == '+' || c == '-').unwrap_or(false) {
                self.advance();
            }
            if !self.peek().map(|c| c.is_ascii_digit()).unwrap_or(false) {
                return Err(JsonError::InvalidNumber {
                    text: self.input[start..self.position].to_string(),
                    position: self.position,
                });
            }
            while self.peek().map(|c| c.is_ascii_digit()).unwrap_or(false) {
                self.advance();
            }
        }

        let num_str = &self.input[start..self.position];
        match num_str.parse::<f64>() {
            Ok(n) => Ok(JsonValue::Number(n)),
            Err(_) => Err(JsonError::InvalidNumber {
                text: num_str.to_string(),
                position: start,
            }),
        }
    }

    fn parse_string(&mut self) -> JsonResult<JsonValue> {
        self.expect_char('"')?;
        let mut result = String::new();

        while !self.is_at_end() {
            match self.peek() {
                Some('"') => {
                    self.advance();
                    return Ok(JsonValue::String(result));
                }
                Some('\\') => {
                    self.advance();
                    match self.peek() {
                        Some('"') => { result.push('"'); self.advance(); }
                        Some('\\') => { result.push('\\'); self.advance(); }
                        Some('/') => { result.push('/'); self.advance(); }
                        Some('b') => { result.push('\x08'); self.advance(); }
                        Some('f') => { result.push('\x0C'); self.advance(); }
                        Some('n') => { result.push('\n'); self.advance(); }
                        Some('r') => { result.push('\r'); self.advance(); }
                        Some('t') => { result.push('\t'); self.advance(); }
                        Some('u') => {
                            self.advance();
                            let hex_start = self.position;
                            for _ in 0..4 {
                                if !self.peek().map(|c| c.is_ascii_hexdigit()).unwrap_or(false) {
                                    return Err(JsonError::InvalidUnicode {
                                        text: self.input[hex_start..self.position].to_string(),
                                        position: hex_start,
                                    });
                                }
                                self.advance();
                            }
                            let hex_str = &self.input[hex_start..self.position];
                            match u32::from_str_radix(hex_str, 16) {
                                Ok(code_point) => {
                                    match std::char::from_u32(code_point) {
                                        Some(c) => result.push(c),
                                        None => return Err(JsonError::InvalidUnicode {
                                            text: hex_str.to_string(),
                                            position: hex_start,
                                        }),
                                    }
                                }
                                Err(_) => return Err(JsonError::InvalidUnicode {
                                    text: hex_str.to_string(),
                                    position: hex_start,
                                }),
                            }
                        }
                        Some(c) => {
                            return Err(JsonError::InvalidEscape {
                                escape: c,
                                position: self.position,
                            });
                        }
                        None => return Err(JsonError::UnexpectedEndOfInput),
                    }
                }
                Some(c) => {
                    if c < '\x20' {
                        return Err(JsonError::InvalidValue {
                            text: c.to_string(),
                            position: self.position,
                        });
                    }
                    result.push(c);
                    self.advance();
                }
                None => return Err(JsonError::UnexpectedEndOfInput),
            }
        }

        Err(JsonError::UnexpectedEndOfInput)
    }

    fn parse_array(&mut self) -> JsonResult<JsonValue> {
        self.expect_char('[')?;
        self.skip_whitespace();

        let mut values = Vec::new();

        if self.peek() == Some(']') {
            self.advance();
            return Ok(JsonValue::Array(values));
        }

        loop {
            self.skip_whitespace();
            values.push(self.parse_value()?);
            self.skip_whitespace();

            match self.peek() {
                Some(',') => {
                    self.advance();
                    continue;
                }
                Some(']') => {
                    self.advance();
                    break;
                }
                _ => return Err(JsonError::UnexpectedChar {
                    expected: ',',
                    found: self.peek().unwrap_or('\0'),
                    position: self.position,
                }),
            }
        }

        Ok(JsonValue::Array(values))
    }

    fn parse_object(&mut self) -> JsonResult<JsonValue> {
        self.expect_char('{')?;
        self.skip_whitespace();

        let mut map = HashMap::new();

        if self.peek() == Some('}') {
            self.advance();
            return Ok(JsonValue::Object(map));
        }

        loop {
            self.skip_whitespace();

            // Parse key
            let key = match self.parse_value()? {
                JsonValue::String(s) => s,
                _ => return Err(JsonError::InvalidValue {
                    text: "non-string key".to_string(),
                    position: self.position,
                }),
            };

            self.skip_whitespace();
            self.expect_char(':')?;
            self.skip_whitespace();

            // Parse value
            let value = self.parse_value()?;
            map.insert(key, value);

            self.skip_whitespace();

            match self.peek() {
                Some(',') => {
                    self.advance();
                    continue;
                }
                Some('}') => {
                    self.advance();
                    break;
                }
                _ => return Err(JsonError::UnexpectedChar {
                    expected: ',',
                    found: self.peek().unwrap_or('\0'),
                    position: self.position,
                }),
            }
        }

        Ok(JsonValue::Object(map))
    }

    fn skip_whitespace(&mut self) {
        while self.peek().map(|c| c.is_ascii_whitespace()).unwrap_or(false) {
            self.advance();
        }
    }

    fn expect_char(&mut self, expected: char) -> JsonResult<()> {
        match self.peek() {
            Some(c) if c == expected => {
                self.advance();
                Ok(())
            }
            Some(c) => Err(JsonError::UnexpectedChar {
                expected,
                found: c,
                position: self.position,
            }),
            None => Err(JsonError::UnexpectedEndOfInput),
        }
    }

    fn expect_keyword(&mut self, keyword: &str) -> JsonResult<()> {
        for expected in keyword.chars() {
            match self.peek() {
                Some(c) if c == expected => self.advance(),
                Some(c) => return Err(JsonError::UnexpectedChar {
                    expected,
                    found: c,
                    position: self.position,
                }),
                None => return Err(JsonError::UnexpectedEndOfInput),
            }
        }
        Ok(())
    }

    fn peek(&self) -> Option<char> {
        self.input.chars().nth(self.position)
    }

    fn advance(&mut self) {
        if !self.is_at_end() {
            self.position += 1;
        }
    }

    fn is_at_end(&self) -> bool {
        self.position >= self.input.len()
    }
}

/// Pretty prints a JSON string
pub fn pretty_print_json(input: &str) -> String {
    match parse_json(input) {
        Ok(value) => value.to_pretty_json(),
        Err(_) => input.to_string(),
    }
}

/// Minifies a JSON string
pub fn minify_json(input: &str) -> String {
    match parse_json(input) {
        Ok(value) => value.to_json(),
        Err(_) => input.to_string(),
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_parse_null() {
        assert_eq!(parse_json("null").unwrap(), JsonValue::Null);
    }

    #[test]
    fn test_parse_bool() {
        assert_eq!(parse_json("true").unwrap(), JsonValue::Bool(true));
        assert_eq!(parse_json("false").unwrap(), JsonValue::Bool(false));
    }

    #[test]
    fn test_parse_number() {
        assert_eq!(parse_json("42").unwrap().as_i64(), 42);
        assert_eq!(parse_json("-42").unwrap().as_i64(), -42);
        assert_eq!(parse_json("3.14").unwrap().as_f64(), 3.14);
        assert_eq!(parse_json("1e10").unwrap().as_f64(), 1e10);
        assert_eq!(parse_json("-1.5e-3").unwrap().as_f64(), -1.5e-3);
    }

    #[test]
    fn test_parse_string() {
        assert_eq!(parse_json("\"hello\"").unwrap().as_string(), "hello");
        assert_eq!(parse_json("\"hello\\nworld\"").unwrap().as_string(), "hello\nworld");
        assert_eq!(parse_json("\"hello\\tworld\"").unwrap().as_string(), "hello\tworld");
        assert_eq!(parse_json("\"hello\\\"world\"").unwrap().as_string(), "hello\"world");
        assert_eq!(parse_json("\"\\u0041\"").unwrap().as_string(), "A");
    }

    #[test]
    fn test_parse_array() {
        let arr = parse_json("[1, 2, 3]").unwrap();
        assert_eq!(arr.len(), 3);
        assert_eq!(arr.get_index(0).as_i64(), 1);
        assert_eq!(arr.get_index(1).as_i64(), 2);
        assert_eq!(arr.get_index(2).as_i64(), 3);
    }

    #[test]
    fn test_parse_object() {
        let obj = parse_json(r#"{"name": "John", "age": 30}"#).unwrap();
        assert_eq!(obj.get("name").as_string(), "John");
        assert_eq!(obj.get("age").as_i64(), 30);
        assert!(obj.has("name"));
        assert!(!obj.has("missing"));
    }

    #[test]
    fn test_nested_object() {
        let obj = parse_json(r#"{"user": {"name": "John", "age": 30}}"#).unwrap();
        assert_eq!(obj.get("user").get("name").as_string(), "John");
        assert_eq!(obj.get("user").get("age").as_i64(), 30);
    }

    #[test]
    fn test_type_checking() {
        assert!(JsonValue::Null.is_null());
        assert!(JsonValue::Bool(true).is_bool());
        assert!(JsonValue::Number(42.0).is_number());
        assert!(JsonValue::String("test".to_string()).is_string());
        assert!(JsonValue::Array(vec![]).is_array());
        assert!(JsonValue::Object(HashMap::new()).is_object());
    }

    #[test]
    fn test_as_functions() {
        assert_eq!(JsonValue::Bool(true).as_bool(), true);
        assert_eq!(JsonValue::Bool(false).as_bool(), false);
        assert_eq!(JsonValue::Number(42.0).as_i64(), 42);
        assert_eq!(JsonValue::Number(3.14).as_f64(), 3.14);
        assert_eq!(JsonValue::String("test".to_string()).as_string(), "test");
    }

    #[test]
    fn test_default_values() {
        assert_eq!(JsonValue::Null.as_bool_or(true), true);
        assert_eq!(JsonValue::Null.as_i64_or(42), 42);
        assert_eq!(JsonValue::Null.as_f64_or(3.14), 3.14);
        assert_eq!(JsonValue::Null.as_string_or("default"), "default");
    }

    #[test]
    fn test_to_json() {
        assert_eq!(JsonValue::Null.to_json(), "null");
        assert_eq!(JsonValue::Bool(true).to_json(), "true");
        assert_eq!(JsonValue::Number(42.0).to_json(), "42");
        assert_eq!(JsonValue::String("hello".to_string()).to_json(), "\"hello\"");
    }

    #[test]
    fn test_escape_sequences() {
        let s = JsonValue::String("hello\nworld\t!\"test\"".to_string()).to_json();
        assert!(s.contains("\\n"));
        assert!(s.contains("\\t"));
        assert!(s.contains("\\\""));
    }

    #[test]
    fn test_round_trip() {
        let original = r#"{"name": "John", "age": 30, "active": true}"#;
        let parsed = parse_json(original).unwrap();
        let output = parsed.to_json();
        let reparsed = parse_json(&output).unwrap();
        assert_eq!(parsed, reparsed);
    }

    #[test]
    fn test_is_valid_json() {
        assert!(is_valid_json("{}"));
        assert!(is_valid_json("[]"));
        assert!(is_valid_json("null"));
        assert!(is_valid_json("true"));
        assert!(is_valid_json("123"));
        assert!(is_valid_json("\"test\""));
        assert!(!is_valid_json(""));
        assert!(!is_valid_json("{invalid}"));
        assert!(!is_valid_json("undefined"));
    }

    #[test]
    fn test_from_conversions() {
        let _: JsonValue = ().into();
        let _: JsonValue = true.into();
        let _: JsonValue = 42i32.into();
        let _: JsonValue = 3.14f64.into();
        let _: JsonValue = "test".into();
        let _: JsonValue = vec![1i32, 2, 3].into();
    }

    #[test]
    fn test_merge() {
        let mut obj1 = parse_json(r#"{"a": 1}"#).unwrap();
        let obj2 = parse_json(r#"{"b": 2}"#).unwrap();
        obj1.merge(&obj2);
        assert_eq!(obj1.get("a").as_i64(), 1);
        assert_eq!(obj1.get("b").as_i64(), 2);
    }

    #[test]
    fn test_empty_array() {
        let arr = parse_json("[]").unwrap();
        assert!(arr.is_empty());
        assert_eq!(arr.len(), 0);
    }

    #[test]
    fn test_empty_object() {
        let obj = parse_json("{}").unwrap();
        assert!(obj.is_empty());
        assert_eq!(obj.len(), 0);
    }

    #[test]
    fn test_keys() {
        let obj = parse_json(r#"{"a": 1, "b": 2}"#).unwrap();
        let keys = obj.keys();
        assert_eq!(keys.len(), 2);
        assert!(keys.contains(&"a".to_string()));
        assert!(keys.contains(&"b".to_string()));
    }

    #[test]
    fn test_pretty_print() {
        let obj = parse_json(r#"{"a":1}"#).unwrap();
        let pretty = obj.to_pretty_json();
        assert!(pretty.contains("\n"));
        assert!(pretty.contains("  "));
    }
}
