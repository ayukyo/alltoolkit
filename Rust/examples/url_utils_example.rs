//! URL Utilities Example
//!
//! Demonstrates usage of the URL utilities module

// Include the module
#[path = "../url_utils/mod.rs"]
mod url_utils;

use url_utils::*;
use std::collections::HashMap;

fn main() {
    println!("========================================");
    println!("Rust URL Utilities - Usage Examples");
    println!("========================================\n");

    // Example 1: Parse a URL
    println!("Example 1: Parse a URL");
    println!("----------------------");
    let url_str = "https://user:pass@api.example.com:8080/v1/users?page=1&limit=10#details";
    println!("Input: {}", url_str);
    
    match parse_url(url_str) {
        Ok(url) => {
            println!("Scheme: {}", url.scheme);
            println!("Host: {}", url.host);
            println!("Port: {:?}", url.port);
            println!("Path: {}", url.path);
            println!("Query 'page': {:?}", url.get_param("page"));
            println!("Query 'limit': {:?}", url.get_param("limit"));
            println!("Fragment: {:?}", url.fragment);
            println!("Origin: {}", url.origin());
            println!("Is Secure: {}", url.is_secure());
        }
        Err(e) => println!("Error: {}", e),
    }
    println!();

    // Example 2: Build a URL using UrlBuilder
    println!("Example 2: Build URL with UrlBuilder");
    println!("------------------------------------");
    let url = UrlBuilder::new()
        .scheme("https")
        .host("api.example.com")
        .path("/v2/search")
        .query_param("q", "rust programming")
        .query_param("category", "tutorials")
        .query_param("page", "1")
        .fragment("results")
        .build();
    println!("Built URL: {}", url);
    println!();

    // Example 3: URL Encoding and Decoding
    println!("Example 3: URL Encoding/Decoding");
    println!("--------------------------------");
    let original = "Hello, World! How are you?";
    let encoded = url_encode(original);
    let decoded = url_decode(&encoded);
    println!("Original: {}", original);
    println!("Encoded:  {}", encoded);
    println!("Decoded:  {}", decoded);
    println!();

    // Example 4: Query String Manipulation
    println!("Example 4: Query String Manipulation");
    println!("------------------------------------");
    let query = "name=John&age=30&city=New%20York";
    println!("Query string: {}", query);
    let params = parse_query_string(query);
    println!("Parsed params:");
    for (key, value) in &params {
        println!("  {} = {}", key, value);
    }
    
    // Build new query string
    let mut new_params = HashMap::new();
    new_params.insert("language".to_string(), "rust".to_string());
    new_params.insert("version".to_string(), "1.70".to_string());
    let new_query = build_query_string(&new_params);
    println!("Built query: {}", new_query);
    println!();

    // Example 5: URL Validation
    println!("Example 5: URL Validation");
    println!("-------------------------");
    let urls = vec![
        "https://example.com",
        "http://localhost:3000",
        "/relative/path",
        "not a valid url",
        "",
        "ftp://files.example.com",
    ];
    for url in urls {
        let valid = is_valid_url(url);
        println!("  '{}' -> {}", url, if valid { "VALID" } else { "INVALID" });
    }
    println!();

    // Example 6: Join URLs
    println!("Example 6: Join URLs");
    println!("--------------------");
    let base = "https://api.example.com/v1";
    let paths = vec!["users", "posts", "comments"];
    for path in paths {
        match join_url(base, path) {
            Ok(url) => println!("  {} + {} = {}", base, path, url),
            Err(e) => println!("  Error: {}", e),
        }
    }
    println!();

    // Example 7: Extract Domain and Path
    println!("Example 7: Extract Domain and Path");
    println!("----------------------------------");
    let test_urls = vec![
        "https://www.rust-lang.org/learn",
        "https://github.com/rust-lang/rust",
        "https://crates.io/crates/url",
    ];
    for url in test_urls {
        println!("URL: {}", url);
        println!("  Domain: {:?}", get_domain(url));
        println!("  Path: {:?}", get_path(url));
    }
    println!();

    // Example 8: Modify URL Parameters
    println!("Example 8: Modify URL Parameters");
    println!("--------------------------------");
    let mut url = parse_url("https://api.example.com/items?page=1").unwrap();
    println!("Original URL: {}", url.to_string());
    
    url.set_param("page", "2");
    url.set_param("limit", "20");
    url.set_param("sort", "desc");
    println!("After adding params: {}", url.to_string());
    
    url.remove_param("limit");
    println!("After removing 'limit': {}", url.to_string());
    println!();

    // Example 9: Normalize URL
    println!("Example 9: Normalize URL");
    println!("------------------------");
    let messy_url = "HTTPS://Example.COM:443/path?query=value";
    println!("Original: {}", messy_url);
    match normalize_url(messy_url) {
        Ok(normalized) => println!("Normalized: {}", normalized),
        Err(e) => println!("Error: {}", e),
    }
    println!();

    // Example 10: Complex URL Building
    println!("Example 10: Complex URL Building");
    println!("--------------------------------");
    let api_url = UrlBuilder::new()
        .scheme("https")
        .username("api_user")
        .password("secret_key")
        .host("api.service.com")
        .port(8443)
        .path("/v3/resources")
        .query_param("format", "json")
        .query_param("include", "metadata,tags")
        .query_param("limit", "100")
        .fragment("response")
        .build();
    println!("Complex URL: {}", api_url);
    
    // Parse it back
    match parse_url(&api_url) {
        Ok(parsed) => {
            println!("Parsed back:");
            println!("  Username: {:?}", parsed.username);
            println!("  Host: {}", parsed.host);
            println!("  Port: {:?}", parsed.port);
            println!("  Query params count: {}", parsed.query.len());
        }
        Err(e) => println!("Parse error: {}", e),
    }

    println!("\n========================================");
    println!("Examples completed!");
    println!("========================================");
}
