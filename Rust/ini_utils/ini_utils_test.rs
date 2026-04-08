//! INI Utilities Test Suite
//!
//! Comprehensive tests for INI configuration parsing and generation.

use std::collections::HashMap;

// Include the module under test
#[path = "mod.rs"]
mod ini_utils;

use ini_utils::*;

fn main() {
    println!("Running INI Utils Tests...\n");

    let mut passed = 0;
    let mut failed = 0;

    // Test 1: Basic parsing
    print!("Test 1: Basic parsing... ");
    match test_basic_parsing() {
        Ok(()) => { println!("PASSED"); passed += 1; }
        Err(e) => { println!("FAILED: {}", e); failed += 1; }
    }

    // Test 2: Global section
    print!("Test 2: Global section... ");
    match test_global_section() {
        Ok(()) => { println!("PASSED"); passed += 1; }
        Err(e) => { println!("FAILED: {}", e); failed += 1; }
    }

    // Test 3: Type conversions
    print!("Test 3: Type conversions... ");
    match test_type_conversions() {
        Ok(()) => { println!("PASSED"); passed += 1; }
        Err(e) => { println!("FAILED: {}", e); failed += 1; }
    }

    // Test 4: Boolean values
    print!("Test 4: Boolean values... ");
    match test_boolean_values() {
        Ok(()) => { println!("PASSED"); passed += 1; }
        Err(e) => { println!("FAILED: {}", e); failed += 1; }
    }

    // Test 5: Set and get
    print!("Test 5: Set and get... ");
    match test_set_and_get() {
        Ok(()) => { println!("PASSED"); passed += 1; }
        Err(e) => { println!("FAILED: {}", e); failed += 1; }
    }

    // Test 6: Section operations
    print!("Test 6: Section operations... ");
    match test_section_operations() {
        Ok(()) => { println!("PASSED"); passed += 1; }
        Err(e) => { println!("FAILED: {}", e); failed += 1; }
    }

    // Test 7: Remove operations
    print!("Test 7: Remove operations... ");
    match test_remove_operations() {
        Ok(()) => { println!("PASSED"); passed += 1; }
        Err(e) => { println!("FAILED: {}", e); failed += 1; }
    }

    // Test 8: Serialization
    print!("Test 8: Serialization... ");
    match test_serialization() {
        Ok(()) => { println!("PASSED"); passed += 1; }
        Err(e) => { println!("FAILED: {}", e); failed += 1; }
    }

    // Test 9: Merge
    print!("Test 9: Merge... ");
    match test_merge() {
        Ok(()) => { println!("PASSED"); passed += 1; }
        Err(e) => { println!("FAILED: {}", e); failed += 1; }
    }

    // Test 10: Quoted values
    print!("Test 10: Quoted values... ");
    match test_quoted_values() {
        Ok(()) => { println!("PASSED"); passed += 1; }
        Err(e) => { println!("FAILED: {}", e); failed += 1; }
    }

    // Test 11: List values
    print!("Test 11: List values... ");
    match test_list_values() {
        Ok(()) => { println!("PASSED"); passed += 1; }
        Err(e) => { println!("FAILED: {}", e); failed += 1; }
    }

    // Test 12: Empty values
    print!("Test 12: Empty values... ");
    match test_empty_values() {
        Ok(()) => { println!("PASSED"); passed += 1; }
        Err(e) => { println!("FAILED: {}", e); failed += 1; }
    }

    // Test 13: Multiple sections
    print!("Test 13: Multiple sections... ");
    match test_multiple_sections() {
        Ok(()) => { println!("PASSED"); passed += 1; }
        Err(e) => { println!("FAILED: {}", e); failed += 1; }
    }

    // Test 14: Convenience functions
    print!("Test 14: Convenience functions... ");
    match test_convenience_functions() {
        Ok(()) => { println!("PASSED"); passed += 1; }
        Err(e) => { println!("FAILED: {}", e); failed += 1; }
    }

    // Test 15: Error handling
    print!("Test 15: Error handling... ");
    match test_error_handling() {
        Ok(()) => { println!("PASSED"); passed += 1; }
        Err(e) => { println!("FAILED: {}", e); failed += 1; }
    }

    // Test 16: Default values
    print!("Test 16: Default values... ");
    match test_default_values() {
        Ok(()) => { println!("PASSED"); passed += 1; }
        Err(e) => { println!("FAILED: {}", e); failed += 1; }
    }

    // Test 17: Unicode support
    print!("Test 17: Unicode support... ");
    match test_unicode_support() {
        Ok(()) => { println!("PASSED"); passed += 1; }
        Err(e) => { println!("FAILED: {}", e); failed += 1; }
    }

    // Test 18: Whitespace handling
    print!("Test 18: Whitespace handling... ");
    match test_whitespace_handling() {
        Ok(()) => { println!("PASSED"); passed += 1; }
        Err(e) => { println!("FAILED: {}", e); failed += 1; }
    }

    // Test 19: Clear
    print!("Test 19: Clear... ");
    match test_clear() {
        Ok(()) => { println!("PASSED"); passed += 1; }
        Err(e) => { println!("FAILED: {}", e); failed += 1; }
    }

    // Test 20: Get or
    print!("Test 20: Get or... ");
    match test_get_or() {
        Ok(()) => { println!("PASSED"); passed += 1; }
        Err(e) => { println!("FAILED: {}", e); failed += 1; }
    }

    println!("\n========================================");
    println!("Results: {} passed, {} failed", passed, failed);
    println!("========================================");

    if failed > 0 {
        std::process::exit(1);
    }
}

fn test_basic_parsing() -> Result<(), String> {
    let content = r#"
[database]
host = localhost
port = 5432
name = mydb
"#;

    let config = IniConfig::parse(content).map_err(|e| e.to_string())?;

    assert_eq!(config.get("database", "host"), Some(&"localhost".to_string()));
    assert_eq!(config.get("database", "port"), Some(&"5432".to_string()));
    assert_eq!(config.get("database", "name"), Some(&"mydb".to_string()));

    Ok(())
}

fn test_global_section() -> Result<(), String> {
    let content = r#"
debug = true
level = info

[database]
host = localhost
"#;

    let config = IniConfig::parse(content).map_err(|e| e.to_string())?;

    assert_eq!(config.get("", "debug"), Some(&"true".to_string()));
    assert_eq!(config.get("", "level"), Some(&"info".to_string()));
    assert_eq!(config.get("database", "host"), Some(&"localhost".to_string()));

    Ok(())
}

fn test_type_conversions() -> Result<(), String> {
    let content = r#"
[database]
port = 5432
timeout = 30.5
max_connections = 100
"#;

    let config = IniConfig::parse(content).map_err(|e| e.to_string())?;

    assert_eq!(config.get_int("database", "port", 0), 5432);
    assert_eq!(config.get_float("database", "timeout", 0.0), 30.5);
    assert_eq!(config.get_int("database", "max_connections", 0), 100);

    // Test defaults
    assert_eq!(config.get_int("database", "missing", 999), 999);
    assert_eq!(config.get_float("database", "missing", 1.5), 1.5);

    Ok(())
}

fn test_boolean_values() -> Result<(), String> {
    let content = r#"
[settings]
debug = true
enabled = yes
active = 1
on = on
verbose = false
disabled = no
off = 0
"#;

    let config = IniConfig::parse(content).map_err(|e| e.to_string())?;

    assert_eq!(config.get_bool("settings", "debug", false), true);
    assert_eq!(config.get_bool("settings", "enabled", false), true);
    assert_eq!(config.get_bool("settings", "active", false), true);
    assert_eq!(config.get_bool("settings", "on", false), true);
    assert_eq!(config.get_bool("settings", "verbose", true), false);
    assert_eq!(config.get_bool("settings", "disabled", true), false);
    assert_eq!(config.get_bool("settings", "off", true), false);

    Ok(())
}

fn test_set_and_get() -> Result<(), String> {
    let mut config = IniConfig::new();

    config.set("database", "host", "localhost");
    config.set("database", "port", "5432");
    config.set("", "debug", "true");

    assert_eq!(config.get("database", "host"), Some(&"localhost".to_string()));
    assert_eq!(config.get("database", "port"), Some(&"5432".to_string()));
    assert_eq!(config.get("", "debug"), Some(&"true".to_string()));

    Ok(())
}

fn test_section_operations() -> Result<(), String> {
    let mut config = IniConfig::new();

    config.set("section1", "key1", "value1");
    config.set("section2", "key1", "value2");

    assert!(config.has_section("section1"));
    assert!(config.has_section("section2"));
    assert!(!config.has_section("missing"));

    let sections = config.sections();
    assert!(sections.contains(&"section1".to_string()));
    assert!(sections.contains(&"section2".to_string()));

    Ok(())
}

fn test_remove_operations() -> Result<(), String> {
    let mut config = IniConfig::new();

    config.set("database", "host", "localhost");
    config.set("database", "port", "5432");

    assert!(config.has("database", "host"));
    assert!(config.remove("database", "host"));
    assert!(!config.has("database", "host"));
    assert!(!config.remove("database", "host"));

    assert!(config.has_section("database"));
    config.remove_section("database");
    assert!(!config.has_section("database"));

    Ok(())
}

fn test_serialization() -> Result<(), String> {
    let mut config = IniConfig::new();
    config.set("database", "host", "localhost");
    config.set("database", "port", "5432");
    config.set("", "debug", "true");

    let output = config.to_string();

    assert!(output.contains("[database]"));
    assert!(output.contains("host = localhost"));
    assert!(output.contains("port = 5432"));
    assert!(output.contains("debug = true"));

    // Test round-trip
    let reparsed = IniConfig::parse(&output).map_err(|e| e.to_string())?;
    assert_eq!(reparsed.get("database", "host"), Some(&"localhost".to_string()));
    assert_eq!(reparsed.get("database", "port"), Some(&"5432".to_string()));

    Ok(())
}

fn test_merge() -> Result<(), String> {
    let mut config1 = IniConfig::new();
    config1.set("section1", "key1", "value1");

    let mut config2 = IniConfig::new();
    config2.set("section1", "key2", "value2");
    config2.set("section2", "key1", "value1");

    config1.merge(&config2, true);

    assert!(config1.has("section1", "key1"));
    assert!(config1.has("section1", "key2"));
    assert!(config1.has("section2", "key1"));

    Ok(())
}

fn test_quoted_values() -> Result<(), String> {
    let content = r#"
[section]
key1 = "quoted value"
key2 = 'single quoted'
key3 = "value with = sign"
"#;

    let config = IniConfig::parse(content).map_err(|e| e.to_string())?;

    assert_eq!(config.get("section", "key1"), Some(&"quoted value".to_string()));
    assert_eq!(config.get("section", "key2"), Some(&"single quoted".to_string()));
    assert_eq!(config.get("section", "key3"), Some(&"value with = sign".to_string()));

    Ok(())
}

fn test_list_values() -> Result<(), String> {
    let mut config = IniConfig::new();
    config.set("section", "items", "a, b, c");
    config.set("section", "paths", "/usr/bin:/usr/local/bin");

    let items = config.get_list("section", "items", ",");
    assert_eq!(items, vec!["a", "b", "c"]);

    let paths = config.get_list("section", "paths", ":");
    assert_eq!(paths, vec!["/usr/bin", "/usr/local/bin"]);

    Ok(())
}

fn test_empty_values() -> Result<(), String> {
    let content = r#"
[section]
key1 =
key2 = value
"#;

    let config = IniConfig::parse(content).map_err(|e| e.to_string())?;

    assert_eq!(config.get("section", "key1"), Some(&"".to_string()));
    assert_eq!(config.get("section", "key2"), Some(&"value".to_string()));

    Ok(())
}

fn test_multiple_sections() -> Result<(), String> {
    let content = r#"
[section1]
key = value1

[section2]
key = value2

[section3]
key = value3
"#;

    let config = IniConfig::parse(content).map_err(|e| e.to_string())?;

    assert_eq!(config.get("section1", "key"), Some(&"value1".to_string()));
    assert_eq!(config.get("section2", "key"), Some(&"value2".to_string()));
    assert_eq!(config.get("section3", "key"), Some(&"value3".to_string()));

    let sections = config.sections();
    assert_eq!(sections.len(), 3);

    Ok(())
}

fn test_convenience_functions() -> Result<(), String> {
    let content = r#"
[database]
host = localhost
"#;

    let config = parse_ini(content).map_err(|e| e.to_string())?;
    assert_eq!(config.get("database", "host"), Some(&"localhost".to_string()));

    let mut data: HashMap<String, HashMap<String, String>> = HashMap::new();
    let mut inner = HashMap::new();
    inner.insert("key".to_string(), "value".to_string());
    data.insert("section".to_string(), inner);

    let config2 = create_ini(data);
    assert_eq!(config2.get("section", "key"), Some(&"value".to_string()));

    Ok(())
}

fn test_error_handling() -> Result<(), String> {
    // Empty section name
    let content1 = "[]";
    assert!(IniConfig::parse(content1).is_err());

    // Empty key
    let content2 = "[section]\n= value";
    assert!(IniConfig::parse(content2).is_err());

    // Invalid line
    let content3 = "[section]\ninvalid line";
    assert!(IniConfig::parse(content3).is_err());

    Ok(())
}

fn test_default_values() -> Result<(), String> {
    let config = IniConfig::new();

    assert_eq!(config.get_int("missing", "key", 42), 42);
    assert_eq!(config.get_float("missing", "key", 3.14), 3.14);
    assert_eq!(config.get_bool("missing", "key", true), true);
    assert_eq!(config.get_bool("missing", "key", false), false);

    Ok(())
}

fn test_unicode_support() -> Result<(), String> {
    let mut config = IniConfig::new();
    config.set("section", "chinese", "你好世界");
    config.set("section", "emoji", "Hello 🌍");
    config.set("section", "japanese", "こんにちは");

    assert_eq!(config.get("section", "chinese"), Some(&"你好世界".to_string()));
    assert_eq!(config.get("section", "emoji"), Some(&"Hello 🌍".to_string()));
    assert_eq!(config.get("section", "japanese"), Some(&"こんにちは".to_string()));

    // Test round-trip
    let output = config.to_string();
    let reparsed = IniConfig::parse(&output).map_err(|e| e.to_string())?;
    assert_eq!(reparsed.get("section", "chinese"), Some(&"你好世界".to_string()));

    Ok(())
}

fn test_whitespace_handling() -> Result<(), String> {
    let content = r#"
[  section  ]
  key  =  value with spaces  
"#;

    let config = IniConfig::parse(content).map_err(|e| e.to_string())?;

    assert_eq!(config.get("section", "key"), Some(&"value with spaces".to_string()));

    Ok(())
}

fn test_clear() -> Result<(), String> {
    let mut config = IniConfig::new();
    config.set("section", "key", "value");
    config.set("", "global", "value");

    assert!(config.has_section("section"));
    config.clear();
    assert!(!config.has_section("section"));
    assert_eq!(config.get("", "global"), None);

    Ok(())
}

fn test_get_or() -> Result<(), String> {
    let mut config = IniConfig::new();
    config.set("section", "key", "value");

    assert_eq!(config.get_or("section", "key", "default"), "value");
    assert_eq!(config.get_or("section", "missing", "default"), "default");

    Ok(())
}
