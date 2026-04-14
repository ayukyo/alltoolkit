//! .env file loading example
//!
//! Run with: cargo run --example dotenv

use env_utils::{load_dotenv_from_path, get_env_or, get_env_list, get_env_map};

fn main() {
    println!("=== env_utils DotEnv Example ===\n");
    
    // Create a sample .env file
    let env_content = r#"
# Application Configuration
APP_NAME=DotEnvDemo
APP_ENV=development

# Server Configuration  
HOST=0.0.0.0
PORT=8080

# Feature Flags
DEBUG=true
FEATURE_X=on
CACHE_ENABLED=1

# Numeric Values
MAX_CONNECTIONS=100
TIMEOUT_SECONDS=30
RATE_LIMIT=99.5

# List Values
ALLOWED_ORIGINS=http://localhost:3000,http://example.com,https://app.example.com

# Key-Value Map
DATABASE_CONFIG=host=localhost,port=5432,name=mydb,pool_size=10
"#;
    
    // Write sample .env
    std::fs::write(".env.example", env_content).expect("Failed to write .env.example");
    println!("Created sample .env.example file");
    
    // Load from specific path
    match load_dotenv_from_path(".env.example") {
        Ok(()) => println!("✓ Successfully loaded .env.example"),
        Err(e) => {
            eprintln!("✗ Failed to load .env: {}", e);
            return;
        }
    }
    
    // Read loaded values
    println!("\n--- Loaded Environment Variables ---\n");
    
    println!("Application:");
    println!("  APP_NAME: {}", get_env_or("APP_NAME", "unnamed".to_string()));
    println!("  APP_ENV: {}", get_env_or("APP_ENV", "production".to_string()));
    
    println!("\nServer:");
    println!("  HOST: {}", get_env_or("HOST", "127.0.0.1".to_string()));
    println!("  PORT: {}", get_env_or::<u16>("PORT", 3000));
    
    println!("\nFeature Flags:");
    println!("  DEBUG: {}", get_env_or::<bool>("DEBUG", false));
    println!("  FEATURE_X: {}", get_env_or::<bool>("FEATURE_X", false));
    println!("  CACHE_ENABLED: {}", get_env_or::<bool>("CACHE_ENABLED", false));
    
    println!("\nNumeric Values:");
    println!("  MAX_CONNECTIONS: {}", get_env_or::<u32>("MAX_CONNECTIONS", 50));
    println!("  TIMEOUT_SECONDS: {}", get_env_or::<u32>("TIMEOUT_SECONDS", 10));
    println!("  RATE_LIMIT: {}", get_env_or::<f64>("RATE_LIMIT", 0.0));
    
    println!("\nList Values:");
    let origins = get_env_list("ALLOWED_ORIGINS").unwrap_or_default();
    println!("  ALLOWED_ORIGINS:");
    for origin in &origins {
        println!("    - {}", origin);
    }
    
    println!("\nMap Values:");
    let db_config = get_env_map("DATABASE_CONFIG").unwrap_or_default();
    println!("  DATABASE_CONFIG:");
    for (key, value) in &db_config {
        println!("    {} = {}", key, value);
    }
    
    // Clean up
    std::fs::remove_file(".env.example").ok();
    println!("\n✓ Cleaned up .env.example");
}