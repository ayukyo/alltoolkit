//! INI Utilities Example
//!
//! Demonstrates various use cases for the INI configuration module.

use std::collections::HashMap;

#[path = "../ini_utils/mod.rs"]
mod ini_utils;

use ini_utils::*;

fn main() {
    println!("========================================");
    println!("      INI Utils Example Program");
    println!("========================================\n");

    example_1_basic_usage();
    example_2_type_conversions();
    example_3_sections_and_keys();
    example_4_serialization();
    example_5_merging_configs();
    example_6_list_values();
    example_7_boolean_values();
    example_8_unicode_support();
    example_9_error_handling();
    example_10_file_operations();
    example_11_convenience_functions();

    println!("\n========================================");
    println!("         All examples completed!");
    println!("========================================");
}

fn example_1_basic_usage() {
    println!("Example 1: Basic Usage");
    println!("----------------------");

    let mut config = IniConfig::new();
    config.set("database", "host", "localhost");
    config.set("database", "port", "5432");
    config.set("database", "name", "myapp");
    config.set("", "debug", "true");

    println!("Database host: {}", config.get("database", "host").unwrap_or(&"unknown".to_string()));
    println!("Database port: {}", config.get("database", "port").unwrap_or(&"unknown".to_string()));
    println!("Debug mode: {}", config.get("", "debug").unwrap_or(&"false".to_string()));

    if config.has("database", "host") {
        println!("Host is configured!");
    }
    println!();
}

fn example_2_type_conversions() {
    println!("Example 2: Type Conversions");
    println!("----------------------------");

    let content = r#"
[server]
port = 8080
max_connections = 100
timeout = 30.5
enabled = true
"#;

    let config = IniConfig::parse(content).expect("Failed to parse");

    println!("Port: {} (i32)", config.get_int("server", "port", 0));
    println!("Max connections: {} (i32)", config.get_int("server", "max_connections", 0));
    println!("Timeout: {} (f64)", config.get_float("server", "timeout", 0.0));
    println!("Enabled: {} (bool)", config.get_bool("server", "enabled", false));
    println!("Missing key with default: {}", config.get_int("server", "missing_key", 42));
    println!();
}

fn example_3_sections_and_keys() {
    println!("Example 3: Sections and Keys");
    println!("-----------------------------");

    let mut config = IniConfig::new();
    config.set("database", "host", "localhost");
    config.set("database", "port", "5432");
    config.set("cache", "enabled", "true");
    config.set("cache", "ttl", "3600");
    config.set("", "app_name", "MyApp");

    println!("Sections:");
    for section in config.sections() {
        println!("  [{}]", section);
        for key in config.keys(&section) {
            if let Some(value) = config.get(&section, &key) {
                println!("    {} = {}", key, value);
            }
        }
    }
    println!();
}

fn example_4_serialization() {
    println!("Example 4: Serialization");
    println!("------------------------");

    let mut config = IniConfig::new();
    config.set("database", "host", "localhost");
    config.set("database", "port", "5432");
    config.set("logging", "level", "info");
    config.set("", "version", "1.0.0");

    let ini_string = config.to_string();
    println!("Generated INI:\n{}", ini_string);

    let reparsed = IniConfig::parse(&ini_string).expect("Failed to parse");
    println!("Round-trip successful: {}", 
        reparsed.get("database", "host") == Some(&"localhost".to_string()));
    println!();
}

fn example_5_merging_configs() {
    println!("Example 5: Merging Configurations");
    println!("----------------------------------");

    let mut base = IniConfig::new();
    base.set("database", "host", "localhost");
    base.set("database", "port", "5432");

    let mut override_config = IniConfig::new();
    override_config.set("database", "port", "3306");
    override_config.set("cache", "enabled", "true");

    println!("Before merge - Port: {}", base.get("database", "port").unwrap_or(&"?".to_string()));
    base.merge(&override_config, true);
    println!("After merge - Port: {}", base.get("database", "port").unwrap_or(&"?".to_string()));
    println!("After merge - Has cache: {}", base.has_section("cache"));
    println!();
}

fn example_6_list_values() {
    println!("Example 6: List Values");
    println!("----------------------");

    let mut config = IniConfig::new();
    config.set("features", "enabled", "login, signup, profile, admin");

    let features = config.get_list("features", "enabled", ",");
    println!("Enabled features:");
    for feature in &features {
        println!("  - {}", feature);
    }
    println!();
}

fn example_7_boolean_values() {
    println!("Example 7: Boolean Values");
    println!("--------------------------");

    let content = r#"
[settings]
debug = true
enabled = yes
active = 1
verbose = false
"#;

    let config = IniConfig::parse(content).expect("Failed to parse");

    println!("True values:");
    println!("  debug=true: {}", config.get_bool("settings", "debug", false));
    println!("  enabled=yes: {}", config.get_bool("settings", "enabled", false));
    println!("  active=1: {}", config.get_bool("settings", "active", false));

    println!("False values:");
    println!("  verbose=false: {}", config.get_bool("settings", "verbose", true));
    println!();
}

fn example_8_unicode_support() {
    println!("Example 8: Unicode Support");
    println!("---------------------------");

    let mut config = IniConfig::new();
    config.set("section", "chinese", "你好世界");
    config.set("section", "emoji", "Hello 🌍");

    println!("Chinese: {}", config.get("section", "chinese").unwrap_or(&"?".to_string()));
    println!("Emoji: {}", config.get("section", "emoji").unwrap_or(&"?".to_string()));

    let output = config.to_string();
    let reparsed = IniConfig::parse(&output).expect("Failed to parse");
    println!("Round-trip Chinese: {}", 
        reparsed.get("section", "chinese") == Some(&"你好世界".to_string()));
    println!();
}

fn example_9_error_handling() {
    println!("Example 9: Error Handling");
    println!("-------------------------");

    let invalid_configs = vec![
        ("[]", "Empty section name"),
        ("[section]\n= value", "Empty key name"),
        ("[section]\ninvalid line", "Invalid line format"),
    ];

    for (content, desc) in invalid_configs {
        match IniConfig::parse(content) {
            Ok(_) => println!("{}: Unexpectedly succeeded", desc),
            Err(e) => println!("{}: Error caught - {}", desc, e),
        }
    }
    println!();
}

fn example_10_file_operations() {
    println!("Example 10: File Operations");
    println!("----------------------------");

    let mut config = IniConfig::new();
    config.set("app", "name", "MyApp");
    config.set("app", "version", "1.0.0");

    let temp_path = "/tmp/test_config.ini";
    
    match config.to_file(temp_path) {
        Ok(_) => {
            println!("Config written to {}", temp_path);
            
            match IniConfig::from_file(temp_path) {
                Ok(loaded) => {
                    println!("Config loaded successfully");
                    println!("App name: {}", loaded
