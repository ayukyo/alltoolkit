//! URL Utilities Test Suite
use std::collections::HashMap;

#[path = "mod.rs"]
mod url_utils;
use url_utils::*;

fn main() {
    println!("Running URL Utils Test Suite...\n");
    let mut passed = 0;
    let mut failed = 0;
    
    // Test 1: Parse simple URL
    print!("Test 1: Parse simple URL... ");
    match parse_url("https://example.com") {
        Ok(url) => {
            if url.scheme == "https" && url.host == "example.com" {
                println!("PASSED"); passed += 1;
            } else { println!("FAILED"); failed += 1; }
        }
        Err(e) => { println!("FAILED: {}", e); failed += 1; }
    }
    
    // Test 2: Parse URL with path
    print!("Test 2: Parse URL with path... ");
    match parse_url("https://example.com/path/to/resource") {
        Ok(url) => {
            if url.path == "/path/to/resource" { println!("PASSED"); passed += 1; }
            else { println!("FAILED"); failed += 1; }
        }
        Err(e) => { println!("FAILED: {}", e); failed += 1; }
    }
    
    // Test 3: Parse URL with query
    print!("Test 3: Parse URL with query... ");
    match parse_url("https://example.com/search?q=rust&lang=en") {
        Ok(url) => {
            if url.get_param("q") == Some(&"rust".to_string()) { println!("PASSED"); passed += 1; }
            else { println!("FAILED"); failed += 1; }
        }
        Err(e) => { println!("FAILED: {}", e); failed += 1; }
    }
    
    // Test 4: Parse URL with port
    print!("Test 4: Parse URL with port... ");
    match parse_url("http://localhost:8080/api") {
        Ok(url) => {
            if url.port == Some(8080) { println!("PASSED"); passed += 1; }
            else { println!("FAILED"); failed += 1; }
        }
        Err(e) => { println!("FAILED: {}", e); failed += 1; }
    }
    
    // Test 5: Parse URL with auth
    print!("Test 5: Parse URL with auth... ");
    match parse_url("https://user:pass@example.com/") {
        Ok(url) => {
            if url.username == Some("user".to_string()) { println!("PASSED"); passed += 1; }
            else { println!("FAILED"); failed += 1; }
        }
        Err(e) => { println!("FAILED: {}", e); failed += 1; }
    }
    
    // Test 6: Parse URL with fragment
    print!("Test 6: Parse URL with fragment... ");
    match parse_url("https://example.com/page#section1") {
        Ok(url) => {
            if url.fragment == Some("section1".to_string()) { println!("PASSED"); passed += 1; }
            else { println!("FAILED"); failed += 1; }
        }
        Err(e) => { println!("FAILED: {}", e); failed += 1; }
    }
    
    // Test 7: URL encoding
    print!("Test 7: URL encoding... ");
    if url_encode("hello world") == "hello%20world" { println!("PASSED"); passed += 1; }
    else { println!("FAILED"); failed += 1; }
    
    // Test 8: URL decoding
    print!("Test 8: URL decoding... ");
    if url_decode("hello%20world") == "hello world" { println!("PASSED"); passed += 1; }
    else { println!("FAILED"); failed += 1; }
    
    // Test 9: Parse query string
    print!("Test 9: Parse query string... ");
    let query = parse_query_string("a=1&b=2");
    if query.get("a") == Some(&"1".to_string()) { println!("PASSED"); passed += 1; }
    else { println!("FAILED"); failed += 1; }
    
    // Test 10: Build query string
    print!("Test 10: Build query string... ");
    let mut params = HashMap::new();
    params.insert("key".to_string(), "value".to_string());
    let query = build_query_string(&params);
    if query.contains("key=value") { println!("PASSED"); passed += 1; }
    else { println!("FAILED"); failed += 1; }
    
    // Test 11: URL validation
    print!("Test 11: URL validation... ");
    if is_valid_url("https://example.com") && !is_valid_url("") { println!("PASSED"); passed += 1; }
    else { println!("FAILED"); failed += 1; }
    
    // Test 12: URL Builder
    print!("Test 12: URL Builder... ");
    let url = UrlBuilder::new().scheme("https").host("api.example.com").path("/v1").query_param("page", "1").build();
    if url.contains("api.example.com") && url.contains("page=1") { println!("PASSED"); passed += 1; }
    else { println!("FAILED: {}", url); failed += 1; }
    
    // Test 13: Join URL
    print!("Test 13: Join URL... ");
    match join_url("https://example.com/api", "users") {
        Ok(url) => {
            if url.contains("/api/users") { println!("PASSED"); passed += 1; }
            else { println!("FAILED: {}", url); failed += 1; }
        }
        Err(e) => { println!("FAILED: {}", e); failed += 1; }
    }
    
    // Test 14: Get domain
    print!("Test 14: Get domain... ");
    if get_domain("https://example.com/path") == Some("example.com".to_string()) { println!("PASSED"); passed += 1; }
    else { println!("FAILED"); failed += 1; }
    
    // Test 15: Get path
    print!("Test 15: Get path... ");
    if get_path("https://example.com/api/users") == Some("/api/users".to_string()) { println!("PASSED"); passed += 1; }
    else { println!("FAILED"); failed += 1; }
    
    // Test 16: Origin
    print!("Test 16: Origin... ");
    match parse_url("https://example.com:8080/path") {
        Ok(url) => {
            if url.origin() == "https://example.com:8080" { println!("PASSED"); passed += 1; }
            else { println!("FAILED: {}", url.origin()); failed += 1; }
        }
        Err(e) => { println!("FAILED: {}", e); failed += 1; }
    }
    
    // Test 17: Is secure
    print!("Test 17: Is secure... ");
    match parse_url("https://example.com") {
        Ok(url) => {
            if url.is_secure() { println!("PASSED"); passed += 1; }
            else { println!("FAILED"); failed += 1; }
        }
        Err(e) => { println!("FAILED: {}", e); failed += 1; }
    }
    
    // Test 18: Set/remove param
    print!("Test 18: Set/remove param... ");
    match parse_url("https://example.com") {
        Ok(mut url) => {
            url.set_param("key", "value");
            if url.get_param("key") == Some(&"value".to_string()) {
                url.remove_param("key");
                if url.get_param("key") == None { println!("PASSED"); passed += 1; }
                else { println!("FAILED"); failed += 1; }
            } else { println!("FAILED"); failed += 1; }
        }
        Err(e) => { println!("FAILED: {}", e); failed += 1; }
    }
    
    // Test 19: Complex URL
    print!("Test 19: Complex URL... ");
    let complex = "https://user:pass@api.example.com:8080/v1/users?page=1&limit=10#section";
    match parse_url(complex) {
        Ok(url) => {
            if url.scheme == "https" && url.host == "api.example.com" && url.port == Some(8080) {
                println!("PASSED"); passed += 1;
            } else { println!("FAILED"); failed += 1; }
        }
        Err(e) => { println!("FAILED: {}", e); failed += 1; }
    }
    
    // Test 20: URL roundtrip
    print!("Test 20: URL roundtrip... ");
    let original = "https://example.com/path?query=value";
    match parse_url(original) {
        Ok(parsed) => {
            let rebuilt = parsed.to_string();
            if rebuilt.contains("example.com") && rebuilt.contains("/path") {
                println!("PASSED"); passed += 1;
            } else { println!("FAILED: {}", rebuilt); failed += 1; }
        }
        Err(e) => { println!("FAILED: {}", e); failed += 1; }
    }
    
    // Test 21: Empty query param value
    print!("Test 21: Empty query param value... ");
    match parse_url("https://example.com?key=") {
        Ok(url) => {
            if url.get_param("key") == Some(&"".to_string()) { println!("PASSED"); passed += 1; }
            else { println!("FAILED"); failed += 1; }
        }
        Err(e) => { println!("FAILED: {}", e); failed += 1; }
    }
    
    // Test 22: Query string with special chars
    print!("Test 22: Query string with special chars... ");
    match parse_url("https://example.com?q=hello%20world") {
        Ok(url) => {
            if url.get_param("q") == Some(&"hello world".to_string()) { println!("PASSED"); passed += 1; }
            else { println!("FAILED"); failed += 1; }
        }
        Err(e) => { println!("FAILED: {}", e); failed += 1; }
    }
    
    // Test 23: URL with file scheme
    print!("Test 23: URL with file scheme... ");
    match parse_url("file://localhost/just/a/path") {
        Ok(url) => {
            if url.scheme == "file" && url.path == "/just/a/path" { println!("PASSED"); passed += 1; }
            else { println!("FAILED: scheme={}, path={}", url.scheme, url.path); failed += 1; }
        }
        Err(e) => { println!("FAILED: {}", e); failed += 1; }
    }
    
    // Test 24: Normalize URL
    print!("Test 24: Normalize URL... ");
    match normalize_url("HTTPS://Example.COM:443/path") {
        Ok(url) => {
            if url.contains("https://example.com/path") { println!("PASSED"); passed += 1; }
            else { println!("FAILED: {}", url); failed += 1; }
        }
        Err(e) => { println!("FAILED: {}", e); failed += 1; }
    }
    
    // Test 25: Multiple query params
    print!("Test 25: Multiple query params... ");
    match parse_url("https://example.com?a=1&b=2&c=3&d=4") {
        Ok(url) => {
            if url.query.len() == 4 { println!("PASSED"); passed += 1; }
            else { println!("FAILED: {}", url.query.len()); failed += 1; }
        }
        Err(e) => { println!("FAILED: {}", e); failed += 1; }
    }
    
    println!("\n========================================");
    println!("Test Results: {} passed, {} failed", passed, failed);
    println!("========================================");
    
    if failed > 0 {
        std::process::exit(1);
    }
}