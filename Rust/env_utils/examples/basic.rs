//! Basic usage example for env_utils
//!
//! Run with: cargo run --example basic

use env_utils::{get_env, get_env_or, require_env, set_env, has_env, remove_env};

fn main() {
    println!("=== env_utils Basic Example ===\n");
    
    // Set some environment variables
    set_env("APP_NAME", "MyApplication");
    set_env("APP_PORT", "8080");
    set_env("APP_DEBUG", "true");
    set_env("APP_RATE", "0.95");
    set_env("APP_COUNT", "42");
    
    // Get as string
    let app_name: String = get_env_or("APP_NAME", "DefaultApp".to_string());
    println!("App Name: {}", app_name);
    
    // Get as integer with default
    let port: u16 = get_env_or("APP_PORT", 3000);
    println!("Port: {}", port);
    
    // Get as boolean
    let debug: bool = get_env_or("APP_DEBUG", false);
    println!("Debug Mode: {}", debug);
    
    // Get as float
    let rate: f64 = get_env_or("APP_RATE", 0.5);
    println!("Rate: {}", rate);
    
    // Get required value
    match require_env::<i32>("APP_COUNT") {
        Ok(count) => println!("Count: {}", count),
        Err(e) => eprintln!("Error: {}", e),
    }
    
    // Check existence
    println!("\nAPP_NAME exists: {}", has_env("APP_NAME"));
    println!("NONEXISTENT exists: {}", has_env("NONEXISTENT"));
    
    // Get optional value
    match get_env("APP_NAME") {
        Some(value) => println!("\nAPP_NAME = {}", value),
        None => println!("\nAPP_NAME not found"),
    }
    
    // Clean up
    remove_env("APP_NAME");
    remove_env("APP_PORT");
    remove_env("APP_DEBUG");
    remove_env("APP_RATE");
    remove_env("APP_COUNT");
    
    println!("\nEnvironment variables cleaned up.");
}