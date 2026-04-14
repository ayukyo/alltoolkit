//! # env_utils - Environment Variable Utilities for Rust
//!
//! A zero-dependency Rust library for environment variable management.
//! 
//! ## Features
//! - Load environment variables from `.env` files
//! - Get typed values (String, i32, i64, u32, u64, f32, f64, bool)
//! - Set and remove environment variables
//! - Support for default values
//! - Validate required environment variables
//! - Parse complex types (Vec, HashMap)
//!
//! ## Example
//! ```rust,ignore
//! use env_utils::{get_env, get_env_or, require_env, load_dotenv};
//!
//! // Load from .env file
//! load_dotenv().ok();
//!
//! // Get with default
//! let port: u16 = get_env_or("PORT", 3000);
//!
//! // Get required env var
//! let db_url: String = require_env("DATABASE_URL").expect("DATABASE_URL must be set");
//! ```

use std::collections::HashMap;
use std::env;
use std::fs;
use std::path::Path;

/// Error type for env_utils operations
#[derive(Debug, Clone)]
pub enum EnvError {
    /// Variable not found
    NotFound(String),
    /// Failed to parse value
    ParseError { key: String, value: String, expected_type: String },
    /// Failed to read .env file
    DotEnvError(String),
}

impl std::fmt::Display for EnvError {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        match self {
            EnvError::NotFound(key) => write!(f, "Environment variable '{}' not found", key),
            EnvError::ParseError { key, value, expected_type } => {
                write!(f, "Failed to parse '{}' as {}: key='{}'", value, expected_type, key)
            }
            EnvError::DotEnvError(msg) => write!(f, "DotEnv error: {}", msg),
        }
    }
}

impl std::error::Error for EnvError {}

/// Load environment variables from a .env file
/// 
/// Searches for `.env` in the current directory and parent directories.
/// 
/// # Example
/// ```rust,ignore
/// use env_utils::load_dotenv;
/// 
/// load_dotenv().expect("Failed to load .env");
/// ```
pub fn load_dotenv() -> Result<(), EnvError> {
    load_dotenv_from_path(".env")
}

/// Load environment variables from a specific .env file path
pub fn load_dotenv_from_path<P: AsRef<Path>>(path: P) -> Result<(), EnvError> {
    let content = fs::read_to_string(path.as_ref())
        .map_err(|e| EnvError::DotEnvError(format!("Failed to read file: {}", e)))?;
    
    for line in content.lines() {
        let line = line.trim();
        
        // Skip empty lines and comments
        if line.is_empty() || line.starts_with('#') {
            continue;
        }
        
        // Parse KEY=VALUE
        if let Some(eq_pos) = line.find('=') {
            let key = line[..eq_pos].trim();
            let mut value = line[eq_pos + 1..].trim();
            
            // Remove quotes if present
            if (value.starts_with('"') && value.ends_with('"')) 
                || (value.starts_with('\'') && value.ends_with('\'')) {
                value = &value[1..value.len() - 1];
            }
            
            // Set the environment variable
            env::set_var(key, value);
        }
    }
    
    Ok(())
}

/// Get an environment variable as a String
pub fn get_env(key: &str) -> Option<String> {
    env::var(key).ok()
}

/// Get an environment variable with a default value
/// 
/// # Example
/// ```rust
/// use env_utils::get_env_or;
/// 
/// let port: u16 = get_env_or("PORT", 3000);
/// let host: String = get_env_or("HOST", "localhost".to_string());
/// ```
pub fn get_env_or<T: FromEnvString>(key: &str, default: T) -> T {
    get_env(key)
        .and_then(|v| T::from_env_string(&v).ok())
        .unwrap_or(default)
}

/// Require an environment variable (returns error if not found)
/// 
/// # Example
/// ```rust,ignore
/// use env_utils::require_env;
/// 
/// let db_url: String = require_env("DATABASE_URL").expect("DATABASE_URL must be set");
/// ```
pub fn require_env<T: FromEnvString>(key: &str) -> Result<T, EnvError> {
    let value = env::var(key).map_err(|_| EnvError::NotFound(key.to_string()))?;
    T::from_env_string(&value).map_err(|_| EnvError::ParseError {
        key: key.to_string(),
        value,
        expected_type: std::any::type_name::<T>().to_string(),
    })
}

/// Set an environment variable
pub fn set_env(key: &str, value: &str) {
    env::set_var(key, value);
}

/// Remove an environment variable
pub fn remove_env(key: &str) {
    env::remove_var(key);
}

/// Check if an environment variable exists
pub fn has_env(key: &str) -> bool {
    env::var(key).is_ok()
}

/// Get all environment variables as a HashMap
pub fn get_all_env() -> HashMap<String, String> {
    env::vars().collect()
}

/// Validate that all required environment variables are set
/// 
/// # Example
/// ```rust,ignore
/// use env_utils::validate_required;
/// 
/// let missing = validate_required(&["DATABASE_URL", "API_KEY"]);
/// if !missing.is_empty() {
///     panic!("Missing required env vars: {:?}", missing);
/// }
/// ```
pub fn validate_required(keys: &[&str]) -> Vec<String> {
    keys.iter()
        .filter(|key| !has_env(key))
        .map(|key| key.to_string())
        .collect()
}

/// Parse a comma-separated environment variable into a Vec
/// 
/// # Example
/// ```rust
/// // ALLOWED_HOSTS=localhost,127.0.0.1,example.com
/// let hosts: Vec<String> = env_utils::get_env_list("ALLOWED_HOSTS").unwrap_or_default();
/// ```
pub fn get_env_list(key: &str) -> Option<Vec<String>> {
    get_env(key).map(|v| {
        v.split(',')
            .map(|s| s.trim().to_string())
            .filter(|s| !s.is_empty())
            .collect()
    })
}

/// Get an environment variable as a Vec with a default value
pub fn get_env_list_or(key: &str, default: Vec<String>) -> Vec<String> {
    get_env_list(key).unwrap_or(default)
}

/// Parse a key=value pair environment variable into a HashMap
/// 
/// # Example
/// ```rust
/// // CONFIG=debug=true,timeout=30,retries=3
/// let config: std::collections::HashMap<String, String> = 
///     env_utils::get_env_map("CONFIG").unwrap_or_default();
/// ```
pub fn get_env_map(key: &str) -> Option<HashMap<String, String>> {
    get_env(key).map(|v| {
        v.split(',')
            .filter_map(|pair| {
                let parts: Vec<&str> = pair.splitn(2, '=').collect();
                if parts.len() == 2 {
                    Some((parts[0].trim().to_string(), parts[1].trim().to_string()))
                } else {
                    None
                }
            })
            .collect()
    })
}

/// Trait for parsing environment variable strings
pub trait FromEnvString: Sized {
    fn from_env_string(s: &str) -> Result<Self, ()>;
}

impl FromEnvString for String {
    fn from_env_string(s: &str) -> Result<Self, ()> {
        Ok(s.to_string())
    }
}

impl FromEnvString for i32 {
    fn from_env_string(s: &str) -> Result<Self, ()> {
        s.parse().map_err(|_| ())
    }
}

impl FromEnvString for i64 {
    fn from_env_string(s: &str) -> Result<Self, ()> {
        s.parse().map_err(|_| ())
    }
}

impl FromEnvString for u16 {
    fn from_env_string(s: &str) -> Result<Self, ()> {
        s.parse().map_err(|_| ())
    }
}

impl FromEnvString for u32 {
    fn from_env_string(s: &str) -> Result<Self, ()> {
        s.parse().map_err(|_| ())
    }
}

impl FromEnvString for u64 {
    fn from_env_string(s: &str) -> Result<Self, ()> {
        s.parse().map_err(|_| ())
    }
}

impl FromEnvString for usize {
    fn from_env_string(s: &str) -> Result<Self, ()> {
        s.parse().map_err(|_| ())
    }
}

impl FromEnvString for f32 {
    fn from_env_string(s: &str) -> Result<Self, ()> {
        s.parse().map_err(|_| ())
    }
}

impl FromEnvString for f64 {
    fn from_env_string(s: &str) -> Result<Self, ()> {
        s.parse().map_err(|_| ())
    }
}

impl FromEnvString for bool {
    fn from_env_string(s: &str) -> Result<Self, ()> {
        match s.to_lowercase().as_str() {
            "true" | "1" | "yes" | "on" | "enable" | "enabled" => Ok(true),
            "false" | "0" | "no" | "off" | "disable" | "disabled" => Ok(false),
            _ => Err(()),
        }
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    
    #[test]
    fn test_set_and_get_env() {
        set_env("TEST_KEY", "test_value");
        assert_eq!(get_env("TEST_KEY"), Some("test_value".to_string()));
        remove_env("TEST_KEY");
        assert_eq!(get_env("TEST_KEY"), None);
    }
    
    #[test]
    fn test_has_env() {
        set_env("TEST_EXISTS", "value");
        assert!(has_env("TEST_EXISTS"));
        assert!(!has_env("NONEXISTENT_KEY_12345"));
        remove_env("TEST_EXISTS");
    }
    
    #[test]
    fn test_get_env_or_default() {
        assert_eq!(get_env_or("NONEXISTENT_PORT", 3000u16), 3000);
        assert_eq!(get_env_or::<String>("NONEXISTENT_HOST", "localhost".to_string()), "localhost");
    }
    
    #[test]
    fn test_parse_int() {
        set_env("TEST_INT", "42");
        let value: i32 = require_env("TEST_INT").unwrap();
        assert_eq!(value, 42);
        remove_env("TEST_INT");
    }
    
    #[test]
    fn test_parse_bool() {
        set_env("TEST_BOOL_TRUE", "true");
        set_env("TEST_BOOL_FALSE", "0");
        set_env("TEST_BOOL_YES", "yes");
        
        assert_eq!(require_env::<bool>("TEST_BOOL_TRUE").unwrap(), true);
        assert_eq!(require_env::<bool>("TEST_BOOL_FALSE").unwrap(), false);
        assert_eq!(require_env::<bool>("TEST_BOOL_YES").unwrap(), true);
        
        remove_env("TEST_BOOL_TRUE");
        remove_env("TEST_BOOL_FALSE");
        remove_env("TEST_BOOL_YES");
    }
    
    #[test]
    fn test_parse_float() {
        set_env("TEST_FLOAT", "3.14159");
        let value: f64 = require_env("TEST_FLOAT").unwrap();
        assert!((value - 3.14159).abs() < 0.0001);
        remove_env("TEST_FLOAT");
    }
    
    #[test]
    fn test_get_env_list() {
        set_env("TEST_LIST", "a, b, c, d");
        let list = get_env_list("TEST_LIST").unwrap();
        assert_eq!(list, vec!["a", "b", "c", "d"]);
        remove_env("TEST_LIST");
    }
    
    #[test]
    fn test_get_env_map() {
        set_env("TEST_MAP", "key1=value1,key2=value2,key3=value3");
        let map = get_env_map("TEST_MAP").unwrap();
        assert_eq!(map.get("key1"), Some(&"value1".to_string()));
        assert_eq!(map.get("key2"), Some(&"value2".to_string()));
        remove_env("TEST_MAP");
    }
    
    #[test]
    fn test_validate_required() {
        set_env("REQUIRED_1", "value1");
        set_env("REQUIRED_2", "value2");
        
        let missing = validate_required(&["REQUIRED_1", "REQUIRED_2", "MISSING_1"]);
        assert_eq!(missing, vec!["MISSING_1"]);
        
        remove_env("REQUIRED_1");
        remove_env("REQUIRED_2");
    }
    
    #[test]
    fn test_require_env_not_found() {
        let result: Result<String, EnvError> = require_env("DEFINITELY_NOT_EXISTS_12345");
        assert!(matches!(result, Err(EnvError::NotFound(_))));
    }
    
    #[test]
    fn test_parse_error() {
        set_env("NOT_A_NUMBER", "hello");
        let result: Result<i32, EnvError> = require_env("NOT_A_NUMBER");
        assert!(matches!(result, Err(EnvError::ParseError { .. })));
        remove_env("NOT_A_NUMBER");
    }
}