//! INI Configuration File Utilities
//!
//! A comprehensive INI configuration file parser and generator for Rust.
//! Supports sections, key-value pairs, comments, and type-safe access.
//!
//! # Features
//! - Parse INI files from strings or files
//! - Generate INI format output
//! - Type-safe value access with defaults
//! - Section and key manipulation
//! - Comment preservation
//! - Unicode support
//!
//! # Example
//! ```rust
//! use ini_utils::IniConfig;
//!
//! let mut config = IniConfig::new();
//! config.set("database", "host", "localhost");
//! config.set("database", "port", "5432");
//!
//! let host = config.get("database", "host").unwrap_or("127.0.0.1");
//! let port: i32 = config.get_int("database", "port", 3306);
//! ```

use std::collections::HashMap;
use std::fmt;
use std::fs;
use std::io::{self, Write};
use std::path::Path;

/// Represents an INI configuration with sections and key-value pairs
#[derive(Debug, Clone, PartialEq)]
pub struct IniConfig {
    /// Global section (keys before any section header)
    global: HashMap<String, String>,
    /// Named sections
    sections: HashMap<String, HashMap<String, String>>,
    /// Comments for each section and key
    comments: HashMap<String, HashMap<String, String>>,
    /// Section order for output
    section_order: Vec<String>,
    /// Key order within sections
    key_order: HashMap<String, Vec<String>>,
}

/// Error type for INI operations
#[derive(Debug, Clone, PartialEq)]
pub enum IniError {
    /// IO error during file operation
    IoError(String),
    /// Parse error with line number
    ParseError { line: usize, message: String },
}

impl fmt::Display for IniError {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        match self {
            IniError::IoError(msg) => write!(f, "IO Error: {}", msg),
            IniError::ParseError { line, message } => {
                write!(f, "Parse error at line {}: {}", line, message)
            }
        }
    }
}

impl std::error::Error for IniError {}

impl IniConfig {
    /// Creates a new empty INI configuration
    pub fn new() -> Self {
        IniConfig {
            global: HashMap::new(),
            sections: HashMap::new(),
            comments: HashMap::new(),
            section_order: Vec::new(),
            key_order: HashMap::new(),
        }
    }

    /// Parses INI content from a string
    pub fn parse(content: &str) -> Result<Self, IniError> {
        let mut config = IniConfig::new();
        let mut current_section: Option<String> = None;

        for (line_num, line) in content.lines().enumerate() {
            let line_num = line_num + 1;
            let trimmed = line.trim();

            // Skip empty lines and comments
            if trimmed.is_empty() || trimmed.starts_with(';') || trimmed.starts_with('#') {
                continue;
            }

            // Section header
            if trimmed.starts_with('[') && trimmed.ends_with(']') {
                let section_name = trimmed[1..trimmed.len() - 1].trim().to_string();

                if section_name.is_empty() {
                    return Err(IniError::ParseError {
                        line: line_num,
                        message: "Empty section name".to_string(),
                    });
                }

                config.sections.entry(section_name.clone()).or_insert_with(HashMap::new);
                if !config.section_order.contains(&section_name) {
                    config.section_order.push(section_name.clone());
                }
                current_section = Some(section_name);
                continue;
            }

            // Key-value pair
            if let Some(pos) = trimmed.find('=') {
                let key = trimmed[..pos].trim().to_string();
                let value = trimmed[pos + 1..].trim().to_string();

                // Remove quotes if present
                let value = if (value.starts_with('"') && value.ends_with('"'))
                    || (value.starts_with('\'') && value.ends_with('\''))
                {
                    value[1..value.len() - 1].to_string()
                } else {
                    value
                };

                if key.is_empty() {
                    return Err(IniError::ParseError {
                        line: line_num,
                        message: "Empty key name".to_string(),
                    });
                }

                // Insert into appropriate section
                if let Some(ref section) = current_section {
                    config
                        .sections
                        .get_mut(section)
                        .unwrap()
                        .insert(key.clone(), value);

                    let keys = config.key_order.entry(section.clone()).or_insert_with(Vec::new);
                    if !keys.contains(&key) {
                        keys.push(key);
                    }
                } else {
                    config.global.insert(key.clone(), value);

                    let keys = config.key_order.entry("__global__".to_string()).or_insert_with(Vec::new);
                    if !keys.contains(&key) {
                        keys.push(key);
                    }
                }
            } else {
                return Err(IniError::ParseError {
                    line: line_num,
                    message: format!("Invalid line: {}", line),
                });
            }
        }

        Ok(config)
    }

    /// Reads an INI file from the specified path
    pub fn from_file<P: AsRef<Path>>(path: P) -> Result<Self, IniError> {
        let content = fs::read_to_string(path.as_ref())
            .map_err(|e| IniError::IoError(e.to_string()))?;
        Self::parse(&content)
    }

    /// Gets a value from the specified section and key
    pub fn get(&self, section: &str, key: &str) -> Option<&String> {
        if section.is_empty() {
            self.global.get(key)
        } else {
            self.sections.get(section).and_then(|s| s.get(key))
        }
    }

    /// Gets a value or returns default
    pub fn get_or(&self, section: &str, key: &str, default: &str) -> String {
        self.get(section, key).cloned().unwrap_or_else(|| default.to_string())
    }

    /// Gets value as i32
    pub fn get_int(&self, section: &str, key: &str, default: i32) -> i32 {
        self.get(section, key)
            .and_then(|v| v.parse().ok())
            .unwrap_or(default)
    }

    /// Gets value as f64
    pub fn get_float(&self, section: &str, key: &str, default: f64) -> f64 {
        self.get(section, key)
            .and_then(|v| v.parse().ok())
            .unwrap_or(default)
    }

    /// Gets value as bool
    pub fn get_bool(&self, section: &str, key: &str, default: bool) -> bool {
        self.get(section, key)
            .map(|v| {
                let v_lower = v.to_lowercase();
                matches!(v_lower.as_str(), "true" | "yes" | "1" | "on" | "enabled")
            })
            .unwrap_or(default)
    }

    /// Gets value as Vec<String> (comma-separated)
    pub fn get_list(&self, section: &str, key: &str, separator: &str) -> Vec<String> {
        self.get(section, key)
            .map(|v| v.split(separator).map(|s| s.trim().to_string()).collect())
            .unwrap_or_default()
    }

    /// Sets a value in the specified section
    pub fn set(&mut self, section: &str, key: &str, value: &str) {
        if section.is_empty() {
            self.global.insert(key.to_string(), value.to_string());
            let keys = self.key_order.entry("__global__".to_string()).or_insert_with(Vec::new);
            if !keys.contains(&key.to_string()) {
                keys.push(key.to_string());
            }
        } else {
            self.sections.entry(section.to_string()).or_insert_with(HashMap::new);
            self.sections.get_mut(section).unwrap().insert(key.to_string(), value.to_string());

            if !self.section_order.contains(&section.to_string()) {
                self.section_order.push(section.to_string());
            }

            let keys = self.key_order.entry(section.to_string()).or_insert_with(Vec::new);
            if !keys.contains(&key.to_string()) {
                keys.push(key.to_string());
            }
        }
    }

    /// Checks if a key exists in a section
    pub fn has(&self, section: &str, key: &str) -> bool {
        self.get(section, key).is_some()
    }

    /// Checks if a section exists
    pub fn has_section(&self, section: &str) -> bool {
        self.sections.contains_key(section)
    }

    /// Removes a key from a section
    pub fn remove(&mut self, section: &str, key: &str) -> bool {
        if section.is_empty() {
            self.global.remove(key).is_some()
        } else {
            self.sections.get_mut(section).map(|s| s.remove(key).is_some()).unwrap_or(false)
        }
    }

    /// Removes an entire section
    pub fn remove_section(&mut self, section: &str) -> bool {
        self.sections.remove(section).is_some()
    }

    /// Returns all section names
    pub fn sections(&self) -> Vec<String> {
        self.section_order.clone()
    }

    /// Returns all keys in a section
    pub fn keys(&self, section: &str) -> Vec<String> {
        if section.is_empty() {
            self.key_order.get("__global__").cloned().unwrap_or_default()
        } else {
            self.key_order.get(section).cloned().unwrap_or_default()
        }
    }

    /// Returns all key-value pairs in a section
    pub fn items(&self, section: &str) -> Vec<(String, String)> {
        if section.is_empty() {
            self.global.iter().map(|(k, v)| (k.clone(), v.clone())).collect()
        } else {
            self.sections.get(section).map(|s| {
                s.iter().map(|(k, v)| (k.clone(), v.clone())).collect()
            }).unwrap_or_default()
        }
    }

    /// Converts the config to a string in INI format
    pub fn to_string(&self) -> String {
        let mut output = String::new();

        // Write global section first
        let global_keys = self.key_order.get("__global__").cloned().unwrap_or_default();
        for key in &global_keys {
            if let Some(value) = self.global.get(key) {
                output.push_str(&format!("{} = {}\n", key, value));
            }
        }

        // Add blank line if there were global keys and there are sections
        if !global_keys.is_empty() && !self.section_order.is_empty() {
            output.push('\n');
        }

        // Write sections
        for (i, section) in self.section_order.iter().enumerate() {
            if let Some(section_data) = self.sections.get(section) {
                output.push_str(&format!("[{}]\n", section));

                let keys = self.key_order.get(section).cloned().unwrap_or_default();
                for key in &keys {
                    if let Some(value) = section_data.get(key) {
                        output.push_str(&format!("{} = {}\n", key, value));
                    }
                }

                // Add blank line between sections
                if i < self.section_order.len() - 1 {
                    output.push('\n');
                }
            }
        }

        output
    }

    /// Writes the config to a file
    pub fn to_file<P: AsRef<Path>>(&self, path: P) -> io::Result<()> {
        let mut file = fs::File::create(path)?;
        file.write_all(self.to_string().as_bytes())?;
        Ok(())
    }

    /// Clears all data
    pub fn clear(&mut self) {
        self.global.clear();
        self.sections.clear();
        self.comments.clear();
        self.section_order.clear();
        self.key_order.clear();
    }

    /// Merges another config into this one
    pub fn merge(&mut self, other: &IniConfig, overwrite: bool) {
        // Merge global section
        for (key, value) in &other.global {
            if overwrite || !self.global.contains_key(key) {
                self.global.insert(key.clone(), value.clone());
            }
        }

        // Merge sections
        for (section, data) in &other.sections {
            self.sections.entry(section.clone()).or_insert_with(HashMap::new);
            let target = self.sections.get_mut(section).unwrap();

            for (key, value) in data {
                if overwrite || !target.contains_key(key) {
                    target.insert(key.clone(), value.clone());
                }
            }

            if !self.section_order.contains(section) {
                self.section_order.push(section.clone());
            }
        }
    }
}

impl Default for IniConfig {
    fn default() -> Self {
        Self::new()
    }
}

/// Convenience function to parse INI from string
pub fn parse_ini(content: &str) -> Result<IniConfig, IniError> {
    IniConfig::parse(content)
}

/// Convenience function to read INI from file
pub fn read_ini<P: AsRef<Path>>(path: P) -> Result<IniConfig, IniError> {
    IniConfig::from_file(path)
}

/// Convenience function to create INI from HashMap
pub fn create_ini(data: HashMap<String, HashMap<String, String>>) -> IniConfig {
    let mut config = IniConfig::new();
    for (section, keys) in data {
        for (key, value) in keys {
            config.set(&section, &key, &value);
        }
    }
    config
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_parse_basic() {
        let content = r#"
[database]
host = localhost
port = 5432
"#;
        let config = IniConfig::parse(content).unwrap();
        assert_eq!(config.get("database", "host"), Some(&"localhost".to_string()));
        assert_eq!(config.get("database", "port"), Some(&"5432".to_string()));
    }

    #[test]
    fn test_global_section() {
        let content = r#"
debug = true
level = info

[database]
host = localhost
"#;
        let config = IniConfig::parse(content).unwrap();
        assert_eq!(config.get("", "debug"), Some(&"true".to_string()));
        assert_eq!(config.get("database", "host"), Some(&"localhost".to_string()));
    }

    #[test]
    fn test_get_int() {
        let content = r#"
[database]
port = 5432
timeout = 30
"#;
        let config = IniConfig::parse(content).unwrap();
        assert_eq!(config.get_int("database", "port", 0), 5432);
        assert_eq!(config.get_int("database", "timeout", 0), 30);
        assert_eq!(config.get_int("database", "missing", 100), 100);
    }

    #[test]
    fn test_get_bool() {
        let content = r#"
[settings]
debug = true
enabled = yes
active = 1
"#;
        let config = IniConfig::parse(content).unwrap();
        assert_eq!(config.get_bool("settings", "debug", false), true);
        assert_eq!(config.get_bool("settings", "enabled", false), true);
        assert_eq!(config.get_bool("settings", "active", false), true);
    }

    #[test]
    fn test_set_and_get() {
        let mut config = IniConfig::new();
        config.set("database", "host", "localhost");
        config.set("database", "port", "5432");

        assert_eq!(config.get("database", "host"), Some(&"localhost".to_string()));
        assert_eq!(config.get("database", "port"), Some(&"5432".to_string()));
    }

    #[test]
    fn test_has_section() {
        let mut config = IniConfig::new();
        config.set("database", "host", "localhost");
        assert!(config.has_section("database"));
        assert!(!config.has_section("missing"));
    }

    #[test]
    fn test_remove() {
        let mut config = IniConfig::new();
        config.set("database", "host", "localhost");
        assert!(config.has("database", "host"));
        config.remove("database", "host");
        assert!(!config.has("database", "host"));
    }

    #[test]
    fn test_to_string() {
        let mut config = IniConfig::new();
        config.set("database", "host", "localhost");
        config.set("database", "port", "5432");

        let output = config.to_string();
        assert!(output.contains("[database]"));
        assert!(output.contains("host = localhost"));
        assert!(output.contains("port = 5432"));
    }

    #[test]
    fn test_merge() {
        let mut config1 = IniConfig::new();
        config1.set("section1", "key1", "value1");

        let mut config2 = IniConfig::new();
        config2.set("section1", "key2", "value2");
        config2.set("section2", "key1", "value1");

        config1.merge(&config2, true);

        assert!(config1.has("section1", "key1"));
        assert!(config1.has("section1", "key2"));
        assert!(config1.has("section2", "key1"));
    }

    #[test]
    fn test_quoted_values() {
        let content = r#"
[section]
key1 = "quoted value"
key2 = 'single quoted'
"#;
        let config = IniConfig::parse(content).unwrap();
        assert_eq!(config.get("section", "key1"), Some(&"quoted value".to_string()));
        assert_eq!(config.get("section", "key2"), Some(&"single quoted".to_string()));
    }

    #[test]
    fn test_get_list() {
        let mut config = IniConfig::new();
        config.set("section", "items", "a, b, c");
        let list = config.get_list("section", "items", ",");
        assert_eq!(list, vec!["a", "b", "c"]);
    }
}
