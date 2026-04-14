//! Validation example for env_utils
//!
//! Run with: cargo run --example validation

use env_utils::{
    validate_required, require_env, set_env, remove_env, get_all_env, has_env, get_env_or,
};

fn main() {
    println!("=== env_utils Validation Example ===\n");
    
    // Set up some environment variables
    set_env("DATABASE_URL", "postgres://localhost/mydb");
    set_env("API_KEY", "secret-key-12345");
    // Intentionally NOT setting SECRET_KEY to demonstrate validation
    
    println!("1. Validate Required Environment Variables\n");
    let required_vars = [
        "DATABASE_URL",
        "API_KEY", 
        "SECRET_KEY",  // This one is missing
        "REDIS_URL",   // This one is missing
    ];
    
    let missing = validate_required(&required_vars);
    
    if missing.is_empty() {
        println!("✓ All required environment variables are set!\n");
    } else {
        println!("✗ Missing required environment variables:");
        for var in &missing {
            println!("  - {}", var);
        }
        println!();
    }
    
    println!("2. Check Individual Variables\n");
    
    let checks = [
        ("DATABASE_URL", "Database connection string"),
        ("API_KEY", "API authentication key"),
        ("SECRET_KEY", "Application secret"),
        ("REDIS_URL", "Redis connection URL"),
    ];
    
    for (var, desc) in &checks {
        let status = if has_env(var) { "✓ SET" } else { "✗ MISSING" };
        println!("  {} - {} [{}]", var, desc, status);
    }
    
    println!("\n3. Require with Defaults (Graceful Degradation)\n");
    
    // For optional configs, use defaults
    let log_level: String = get_env_or("LOG_LEVEL", "info".to_string());
    let max_retries: u32 = get_env_or("MAX_RETRIES", 3);
    let timeout_ms: u64 = get_env_or("TIMEOUT_MS", 5000);
    let enable_metrics: bool = get_env_or("ENABLE_METRICS", false);
    
    println!("  LOG_LEVEL: {}", log_level);
    println!("  MAX_RETRIES: {}", max_retries);
    println!("  TIMEOUT_MS: {}", timeout_ms);
    println!("  ENABLE_METRICS: {}", enable_metrics);
    
    println!("\n4. Require with Error Handling\n");
    
    // For required configs, handle errors
    match require_env::<String>("DATABASE_URL") {
        Ok(url) => println!("✓ DATABASE_URL: {}", url),
        Err(e) => eprintln!("✗ Error: {}", e),
    }
    
    match require_env::<String>("SECRET_KEY") {
        Ok(key) => println!("✓ SECRET_KEY: {}", key),
        Err(e) => eprintln!("✗ Error: {}", e),
    }
    
    println!("\n5. Environment Variable Count\n");
    
    let all_env = get_all_env();
    println!("Total environment variables: {}", all_env.len());
    
    // Show app-specific variables (those we set)
    println!("\nApp-specific variables:");
    for (key, value) in all_env.iter() {
        if key.starts_with("APP") || matches!(key.as_str(), "DATABASE_URL" | "API_KEY") {
            // Truncate long values
            let display_value = if value.len() > 30 {
                format!("{}...", &value[..27])
            } else {
                value.clone()
            };
            println!("  {} = {}", key, display_value);
        }
    }
    
    // Clean up
    remove_env("DATABASE_URL");
    remove_env("API_KEY");
    
    println!("\n✓ Cleaned up test environment variables");
}