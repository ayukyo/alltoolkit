//! URL Utilities Module for Rust
//!
//! A comprehensive URL manipulation utility module providing:
//! - URL parsing and building
//! - URL encoding/decoding
//! - Query string manipulation
//! - URL validation and normalization
//!
//! # Examples
//!
//! ```
//! use url_utils::*;
//!
//! // Parse a URL
//! let url = parse_url("https://example.com/path?query=value").unwrap();
//! assert_eq!(url.scheme, "https");
//! assert_eq!(url.host, "example.com");
//!
//! // Build a URL
//! let url = UrlBuilder::new()
//!     .scheme("https")
//!     .host("api.example.com")
//!     .path("/v1/users")
//!     .query_param("page", "1")
//!     .build();
//! assert_eq!(url, "https://api.example.com/v1/users?page=1");
//! ```

use std::collections::HashMap;

/// Represents a parsed URL with all its components
#[derive(Debug, Clone, PartialEq)]
pub struct ParsedUrl {
    /// URL scheme (e.g., "https", "http", "ftp")
    pub scheme: String,
    /// Username for authentication (optional)
    pub username: Option<String>,
    /// Password for authentication (optional)
    pub password: Option<String>,
    /// Host name or IP address
    pub host: String,
    /// Port number (optional)
    pub port: Option<u16>,
    /// URL path
    pub path: String,
    /// Query string parameters
    pub query: HashMap<String, String>,
    /// URL fragment (hash)
    pub fragment: Option<String>,
}

impl ParsedUrl {
    /// Creates a new empty ParsedUrl
    pub fn new() -> Self {
        ParsedUrl {
            scheme: String::new(),
            username: None,
            password: None,
            host: String::new(),
            port: None,
            path: String::new(),
            query: HashMap::new(),
            fragment: None,
        }
    }

    /// Returns the full URL as a string
    pub fn to_string(&self) -> String {
        let mut result = String::new();

        // Scheme
        if !self.scheme.is_empty() {
            result.push_str(&self.scheme);
            result.push_str("://");
        }

        // Authentication
        if let Some(ref username) = self.username {
            result.push_str(&url_encode(username));
            if let Some(ref password) = self.password {
                result.push(':');
                result.push_str(&url_encode(password));
            }
            result.push('@');
        }

        // Host
        result.push_str(&self.host);

        // Port
        if let Some(port) = self.port {
            let default_port = match self.scheme.as_str() {
                "http" => Some(80),
                "https" => Some(443),
                "ftp" => Some(21),
                "ssh" => Some(22),
                _ => None,
            };
            if default_port != Some(port) {
                result.push(':');
                result.push_str(&port.to_string());
            }
        }

        // Path
        if !self.path.is_empty() {
            if !self.path.starts_with('/') {
                result.push('/');
            }
            result.push_str(&self.path);
        }

        // Query string
        if !self.query.is_empty() {
            result.push('?');
            let params: Vec<String> = self.query
                .iter()
                .map(|(k, v)| format!("{}={}", url_encode(k), url_encode(v)))
                .collect();
            result.push_str(&params.join("&"));
        }

        // Fragment
        if let Some(ref fragment) = self.fragment {
            result.push('#');
            result.push_str(&url_encode(fragment));
        }

        result
    }

    /// Returns the origin (scheme + host + port)
    pub fn origin(&self) -> String {
        let mut result = String::new();
        if !self.scheme.is_empty() {
            result.push_str(&self.scheme);
            result.push_str("://");
        }
        result.push_str(&self.host);
        if let Some(port) = self.port {
            let default_port = match self.scheme.as_str() {
                "http" => Some(80),
                "https" => Some(443),
                _ => None,
            };
            if default_port != Some(port) {
                result.push(':');
                result.push_str(&port.to_string());
            }
        }
        result
    }

    /// Returns true if the URL uses a secure scheme (https)
    pub fn is_secure(&self) -> bool {
        self.scheme == "https"
    }

    /// Returns the value of a query parameter
    pub fn get_param(&self, key: &str) -> Option<&String> {
        self.query.get(key)
    }

    /// Sets a query parameter
    pub fn set_param(&mut self, key: &str, value: &str) {
        self.query.insert(key.to_string(), value.to_string());
    }

    /// Removes a query parameter
    pub fn remove_param(&mut self, key: &str) -> Option<String> {
        self.query.remove(key)
    }
}

impl Default for ParsedUrl {
    fn default() -> Self {
        Self::new()
    }
}

/// Parses a URL string into its components
pub fn parse_url(url: &str) -> Result<ParsedUrl, String> {
    let mut parsed = ParsedUrl::new();
    let mut remaining = url;

    // Parse scheme
    if let Some(pos) = remaining.find("://") {
        parsed.scheme = remaining[..pos].to_lowercase();
        remaining = &remaining[pos + 3..];
    }

    // Parse authentication and host
    if let Some(at_pos) = remaining.find('@') {
        let auth_part = &remaining[..at_pos];
        remaining = &remaining[at_pos + 1..];

        if let Some(colon_pos) = auth_part.find(':') {
            parsed.username = Some(url_decode(&auth_part[..colon_pos]));
            parsed.password = Some(url_decode(&auth_part[colon_pos + 1..]));
        } else {
            parsed.username = Some(url_decode(auth_part));
        }
    }

    // Parse host and port
    let (host_part, rest) = if let Some(slash_pos) = remaining.find('/') {
        (&remaining[..slash_pos], &remaining[slash_pos..])
    } else if let Some(qmark_pos) = remaining.find('?') {
        (&remaining[..qmark_pos], &remaining[qmark_pos..])
    } else if let Some(hash_pos) = remaining.find('#') {
        (&remaining[..hash_pos], &remaining[hash_pos..])
    } else {
        (remaining, "")
    };

    if let Some(colon_pos) = host_part.rfind(':') {
        if host_part.starts_with('[') && host_part.contains("]:") {
            if let Some(bracket_end) = host_part.find(']') {
                parsed.host = host_part[..bracket_end + 1].to_string();
                if let Ok(port) = host_part[bracket_end + 2..].parse::<u16>() {
                    parsed.port = Some(port);
                }
            }
        } else if !host_part.starts_with('[') {
            parsed.host = host_part[..colon_pos].to_lowercase();
            if let Ok(port) = host_part[colon_pos + 1..].parse::<u16>() {
                parsed.port = Some(port);
            }
        } else {
            parsed.host = host_part.to_lowercase();
        }
    } else {
        parsed.host = host_part.to_lowercase();
    }

    if parsed.host.is_empty() {
        return Err("Missing host in URL".to_string());
    }

    // Parse path, query, and fragment
    let mut path_part = rest;
    
    // Parse fragment
    if let Some(hash_pos) = path_part.find('#') {
        parsed.fragment = Some(url_decode(&path_part[hash_pos + 1..]));
        path_part = &path_part[..hash_pos];
    }

    // Parse query string
    if let Some(qmark_pos) = path_part.find('?') {
        let query_str = &path_part[qmark_pos + 1..];
        path_part = &path_part[..qmark_pos];
        parsed.query = parse_query_string(query_str);
    }

    // Parse path
    if path_part.starts_with('/') {
        parsed.path = path_part.to_string();
    } else if !path_part.is_empty() {
        parsed.path = format!("/{}", path_part);
    }

    Ok(parsed)
}

/// URL-encodes a string according to RFC 3986
pub fn url_encode(input: &str) -> String {
    let mut result = String::with_capacity(input.len() * 3);
    for byte in input.bytes() {
        match byte {
            b'A'..=b'Z' | b'a'..=b'z' | b'0'..=b'9' |
            b'-' | b'_' | b'.' | b'~' => {
                result.push(byte as char);
            }
            _ => {
                result.push('%');
                result.push_str(&format!("{:02X}", byte));
            }
        }
    }
    result
}

/// URL-decodes a string
pub fn url_decode(input: &str) -> String {
    let mut result = String::with_capacity(input.len());
    let mut chars = input.chars().peekable();
    
    while let Some(ch) = chars.next() {
        if ch == '%' {
            let hex1 = chars.next();
            let hex2 = chars.next();
            if let (Some(h1), Some(h2)) = (hex1, hex2) {
                if let Ok(byte) = u8::from_str_radix(&format!("{}{}", h1, h2), 16) {
                    result.push(byte as char);
                } else {
                    result.push('%');
                    result.push(h1);
                    result.push(h2);
                }
            } else {
                result.push('%');
                if let Some(h) = hex1 {
                    result.push(h);
                }
            }
        } else if ch == '+' {
            result.push(' ');
        } else {
            result.push(ch);
        }
    }
    result
}

/// Parses a query string into a HashMap
pub fn parse_query_string(query: &str) -> HashMap<String, String> {
    let mut result = HashMap::new();
    if query.is_empty() {
        return result;
    }

    for pair in query.split('&') {
        if pair.is_empty() {
            continue;
        }
        if let Some(eq_pos) = pair.find('=') {
            let key = url_decode(&pair[..eq_pos]);
            let value = url_decode(&pair[eq_pos + 1..]);
            result.insert(key, value);
        } else {
            result.insert(url_decode(pair), String::new());
        }
    }
    result
}

/// Builds a query string from a HashMap
pub fn build_query_string(params: &HashMap<String, String>) -> String {
    if params.is_empty() {
        return String::new();
    }
    let pairs: Vec<String> = params
        .iter()
        .map(|(k, v)| format!("{}={}", url_encode(k), url_encode(v)))
        .collect();
    pairs.join("&")
}

/// Validates if a string is a valid URL
pub fn is_valid_url(url: &str) -> bool {
    if url.is_empty() {
        return false;
    }

    // Check for valid scheme
    let schemes = ["http://", "https://", "ftp://", "file://", "mailto:"];
    let has_valid_scheme = schemes.iter().any(|s| url.to_lowercase().starts_with(s));
    
    if !has_valid_scheme {
        // Allow relative URLs or URLs without scheme
        if url.starts_with('/') || url.starts_with("./") || url.starts_with("../") {
            return true;
        }
        // Check if it looks like a domain
        if url.contains('.') && !url.contains(' ') && !url.contains('\n') {
            return true;
        }
        return false;
    }

    // Basic validation
    if url.contains(' ') || url.contains('\n') || url.contains('\t') {
        return false;
    }

    true
}

/// Normalizes a URL by removing unnecessary components
pub fn normalize_url(url: &str) -> Result<String, String> {
    let parsed = parse_url(url)?;
    Ok(parsed.to_string())
}

/// URL Builder for constructing URLs programmatically
#[derive(Debug, Clone)]
pub struct UrlBuilder {
    scheme: String,
    username: Option<String>,
    password: Option<String>,
    host: String,
    port: Option<u16>,
    path: String,
    query: HashMap<String, String>,
    fragment: Option<String>,
}

impl UrlBuilder {
    /// Creates a new URL builder
    pub fn new() -> Self {
        UrlBuilder {
            scheme: String::new(),
            username: None,
            password: None,
            host: String::new(),
            port: None,
            path: String::new(),
            query: HashMap::new(),
            fragment: None,
        }
    }

    /// Sets the URL scheme
    pub fn scheme(mut self, scheme: &str) -> Self {
        self.scheme = scheme.to_lowercase();
        self
    }

    /// Sets the host
    pub fn host(mut self, host: &str) -> Self {
        self.host = host.to_lowercase();
        self
    }

    /// Sets the port
    pub fn port(mut self, port: u16) -> Self {
        self.port = Some(port);
        self
    }

    /// Sets the username for authentication
    pub fn username(mut self, username: &str) -> Self {
        self.username = Some(username.to_string());
        self
    }

    /// Sets the password for authentication
    pub fn password(mut self, password: &str) -> Self {
        self.password = Some(password.to_string());
        self
    }

    /// Sets the path
    pub fn path(mut self, path: &str) -> Self {
        self.path = if path.starts_with('/') {
            path.to_string()
        } else {
            format!("/{}", path)
        };
        self
    }

    /// Adds a query parameter
    pub fn query_param(mut self, key: &str, value: &str) -> Self {
        self.query.insert(key.to_string(), value.to_string());
        self
    }

    /// Adds multiple query parameters
    pub fn query_params(mut self, params: HashMap<String, String>) -> Self {
        self.query.extend(params);
        self
    }

    /// Sets the fragment (hash)
    pub fn fragment(mut self, fragment: &str) -> Self {
        self.fragment = Some(fragment.to_string());
        self
    }

    /// Builds the final URL string
    pub fn build(self) -> String {
        let parsed = ParsedUrl {
            scheme: self.scheme,
            username: self.username,
            password: self.password,
            host: self.host,
            port: self.port,
            path: self.path,
            query: self.query,
            fragment: self.fragment,
        };
        parsed.to_string()
    }
}

impl Default for UrlBuilder {
    fn default() -> Self {
        Self::new()
    }
}

/// Extracts the domain from a URL
pub fn get_domain(url: &str) -> Option<String> {
    // Only return domain for URLs with valid scheme
    let url_lower = url.to_lowercase();
    if !url_lower.starts_with("http://") && !url_lower.starts_with("https://") {
        return None;
    }
    parse_url(url).ok().map(|p| p.host)
}

/// Extracts the path from a URL
pub fn get_path(url: &str) -> Option<String> {
    // Only return path for URLs with valid scheme
    let url_lower = url.to_lowercase();
    if !url_lower.starts_with("http://") && !url_lower.starts_with("https://") {
        return None;
    }
    parse_url(url).ok().map(|p| p.path)
}

/// Joins a base URL with a relative path
pub fn join_url(base: &str, path: &str) -> Result<String, String> {
    let mut parsed = parse_url(base)?;
    
    if path.starts_with('/') {
        parsed.path = path.to_string();
    } else if parsed.path.ends_with('/') {
        parsed.path = format!("{}{}", parsed.path, path);
    } else {
        parsed.path = format!("{}/{}", parsed.path, path);
    }
    
    Ok(parsed.to_string())
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_parse_simple_url() {
        let url = parse_url("https://example.com").unwrap();
        assert_eq!(url.scheme, "https");
        assert_eq!(url.host, "example.com");
        assert_eq!(url.path, "");
    }

    #[test]
    fn test_parse_url_with_path() {
        let url = parse_url("https://example.com/path/to/resource").unwrap();
        assert_eq!(url.scheme, "https");
        assert_eq!(url.host, "example.com");
        assert_eq!(url.path, "/path/to/resource");
    }

    #[test]
    fn test_parse_url_with_query() {
        let url = parse_url("https://example.com/search?q=rust&lang=en").unwrap();
        assert_eq!(url.scheme, "https");
        assert_eq!(url.host, "example.com");
        assert_eq!(url.path, "/search");
        assert_eq!(url.get_param("q"), Some(&"rust".to_string()));
        assert_eq!(url.get_param("lang"), Some(&"en".to_string()));
    }

    #[test]
    fn test_parse_url_with_port() {
        let url = parse_url("http://localhost:8080/api").unwrap();
        assert_eq!(url.scheme, "http");
        assert_eq!(url.host, "localhost");
        assert_eq!(url.port, Some(8080));
        assert_eq!(url.path, "/api");
    }

    #[test]
    fn test_parse_url_with_auth() {
        let url = parse_url("https://user:pass@example.com/").unwrap();
        assert_eq!(url.scheme, "https");
        assert_eq!(url.username, Some("user".to_string()));
        assert_eq!(url.password, Some("pass".to_string()));
        assert_eq!(url.host, "example.com");
    }

    #[test]
    fn test_parse_url_with_fragment() {
        let url = parse_url("https://example.com/page#section1").unwrap();
        assert_eq!(url.path, "/page");
        assert_eq!(url.fragment, Some("section1".to_string()));
    }

    #[test]
    fn test_url_encode() {
        assert_eq!(url_encode("hello world"), "hello%20world");
        assert_eq!(url_encode("a+b=c"), "a%2Bb%3Dc");
        assert_eq!(url_encode("你好"), "%E4%BD%A0%E5%A5%BD");
    }

    #[test]
    fn test_url_decode() {
        assert_eq!(url_decode("hello%20world"), "hello world");
        assert_eq!(url_decode("a%2Bb%3Dc"), "a+b=c");
        assert_eq!(url_decode("hello+world"), "hello world");
    }

    #[test]
    fn test_parse_query_string() {
        let query = parse_query_string("a=1&b=2&c=3");
        assert_eq!(query.get("a"), Some(&"1".to_string()));
        assert_eq!(query.get("b"), Some(&"2".to_string()));
        assert_eq!(query.get("c"), Some(&"3".to_string()));
    }

    #[test]
    fn test_build_query_string() {
        let mut params = HashMap::new();
        params.insert("key".to_string(), "value".to_string());
        params.insert("foo".to_string(), "bar".to_string());
        let query = build_query_string(&params);
        assert!(query.contains("key=value"));
        assert!(query.contains("foo=bar"));
    }

    #[test]
    fn test_is_valid_url() {
        assert!(is_valid_url("https://example.com"));
        assert!(is_valid_url("http://localhost:3000"));
        assert!(is_valid_url("/relative/path"));
        assert!(!is_valid_url(""));
        assert!(!is_valid_url("not a url"));
    }

    #[test]
    fn test_url_builder() {
        let url = UrlBuilder::new()
            .scheme("https")
            .host("api.example.com")
            .path("/v1/users")
            .query_param("page", "1")
            .query_param("limit", "10")
            .build();
        assert!(url.contains("https://api.example.com/v1/users"));
        assert!(url.contains("page=1"));
        assert!(url.contains("limit=10"));
    }

    #[test]
    fn test_join_url() {
        let url1 = join_url("https://example.com/api", "users").unwrap();
        assert_eq!(url1, "https://example.com/api/users");
        
        let url2 = join_url("https://example.com/api/", "/absolute").unwrap();
        assert_eq!(url2, "https://example.com/absolute");
    }

    #[test]
    fn test_get_domain() {
        assert_eq!(get_domain("https://example.com/path"), Some("example.com".to_string()));
        assert_eq!(get_domain("not a url"), None);
    }

    #[test]
    fn test_roundtrip() {
        let original = "https://user:pass@example.com:8080/path?query=value#hash";
        let parsed = parse_url(original).unwrap();
        let rebuilt = parsed.to_string();
        assert!(rebuilt.contains("https://"));
        assert!(rebuilt.contains("example.com"));
        assert!(rebuilt.contains("/path"));
        assert!(rebuilt.contains("query=value"));
    }
}
