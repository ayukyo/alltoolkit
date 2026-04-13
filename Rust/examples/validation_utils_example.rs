//! Validation Utilities Example
//! 
//! Demonstrates usage of validation utilities for common data validation tasks.

use std::io::{self, Write};

// Import functions (in production, use: use validation_utils::*;)
// For this example, we'll demonstrate the API conceptually

fn main() {
    println!("=== Validation Utilities Example ===\n");
    
    // 1. Email Validation
    println!("--- Email Validation ---");
    let emails = [
        "user@example.com",
        "user.name+tag@sub.domain.co.uk",
        "invalid.email",
        "@example.com",
        "user@",
    ];
    
    for email in &emails {
        let status = if is_valid_email(email) { "✓ Valid" } else { "✗ Invalid" };
        println!("  {} → {}", email, status);
    }
    println!();
    
    // 2. URL Validation
    println!("--- URL Validation ---");
    let urls = [
        "https://example.com",
        "http://localhost:8080/path",
        "ftp://example.com",
        "not-a-url",
    ];
    
    for url in &urls {
        let status = if is_valid_url(url) { "✓ Valid" } else { "✗ Invalid" };
        println!("  {} → {}", url, status);
    }
    println!();
    
    // 3. Phone Number Validation
    println!("--- Phone Number Validation ---");
    let phones = [
        "+1-555-123-4567",
        "+44 20 7946 0958",
        "+8613800138000",
        "1234567890",  // Missing +
    ];
    
    for phone in &phones {
        let status = if is_valid_phone(phone) { "✓ Valid" } else { "✗ Invalid" };
        println!("  {} → {}", phone, status);
    }
    println!();
    
    // 4. Credit Card Validation & Type Detection
    println!("--- Credit Card Validation ---");
    let cards = [
        ("4532015112830366", "Visa"),
        ("5500000000000004", "Mastercard"),
        ("340000000000009", "Amex"),
        ("1234567890123456", "Invalid"),
    ];
    
    for (card, expected) in &cards {
        let valid = is_valid_credit_card(card);
        let detected = detect_credit_card_type_name(card);
        println!("  {} → Valid: {}, Type: {} (Expected: {})", 
                 card, if valid { "✓" } else { "✗" }, detected, expected);
    }
    println!();
    
    // 5. IP Address Validation
    println!("--- IP Address Validation ---");
    let ipv4s = ["192.168.1.1", "255.255.255.255", "256.1.1.1"];
    let ipv6s = ["::1", "2001:db8::1", "gggg::1"];
    
    println!("  IPv4:");
    for ip in &ipv4s {
        let status = if is_valid_ipv4(ip) { "✓ Valid" } else { "✗ Invalid" };
        println!("    {} → {}", ip, status);
    }
    
    println!("  IPv6:");
    for ip in &ipv6s {
        let status = if is_valid_ipv6(ip) { "✓ Valid" } else { "✗ Invalid" };
        println!("    {} → {}", ip, status);
    }
    println!();
    
    // 6. Password Strength
    println!("--- Password Strength Analysis ---");
    let passwords = [
        "password",
        "Password1",
        "P@ssw0rd",
        "MyV3ry$tr0ngP@ss!",
    ];
    
    for pwd in &passwords {
        let strength = password_strength_name(pwd);
        println!("  '{}' → {}", pwd, strength);
    }
    println!();
    
    // 7. ISBN Validation
    println!("--- ISBN Validation ---");
    let isbns = [
        "0471958697",         // ISBN-10
        "9780471486480",      // ISBN-13
        "0-471-60695-2",      // ISBN-10 with hyphens
        "123456789",          // Invalid
    ];
    
    for isbn in &isbns {
        let status = if is_valid_isbn(isbn) { "✓ Valid" } else { "✗ Invalid" };
        println!("  {} → {}", isbn, status);
    }
    println!();
    
    // 8. Hex Color Validation
    println!("--- Hex Color Validation ---");
    let colors = [
        "#fff",
        "#ffffff",
        "#ffaa0080",
        "fff",      // Missing #
        "#fffg00",  // Invalid char
    ];
    
    for color in &colors {
        let status = if is_valid_hex_color(color) { "✓ Valid" } else { "✗ Invalid" };
        println!("  {} → {}", color, status);
    }
    println!();
    
    // 9. Slug Validation
    println!("--- Slug Validation ---");
    let slugs = [
        "my-blog-post",
        "user123",
        "-invalid",
        "has space",
    ];
    
    for slug in &slugs {
        let status = if is_valid_slug(slug) { "✓ Valid" } else { "✗ Invalid" };
        println!("  {} → {}", slug, status);
    }
    println!();
    
    println!("=== Example Complete ===");
}

// Simplified validation function stubs for example demonstration
// In production, import from validation_utils module

fn is_valid_email(email: &str) -> bool {
    email.contains('@') && 
    email.split('@').len() == 2 &&
    !email.starts_with('@') &&
    !email.ends_with('@')
}

fn is_valid_url(url: &str) -> bool {
    url.starts_with("http://") || url.starts_with("https://")
}

fn is_valid_phone(phone: &str) -> bool {
    phone.starts_with('+')
}

fn is_valid_credit_card(card: &str) -> bool {
    let digits: String = card.chars().filter(|c| c.is_ascii_digit()).collect();
    matches!(digits.len(), 13..=19)
}

fn detect_credit_card_type_name(card: &str) -> &'static str {
    let digits: String = card.chars().filter(|c| c.is_ascii_digit()).collect();
    if digits.starts_with('4') { "Visa" }
    else if digits.starts_with('5') { "Mastercard" }
    else if digits.starts_with('34') || digits.starts_with('37') { "American Express" }
    else { "Unknown" }
}

fn is_valid_ipv4(ip: &str) -> bool {
    ip.split('.').count() == 4
}

fn is_valid_ipv6(ip: &str) -> bool {
    ip.contains(':')
}

fn password_strength_name(pwd: &str) -> &'static str {
    let len = pwd.len();
    let has_upper = pwd.chars().any(|c| c.is_uppercase());
    let has_lower = pwd.chars().any(|c| c.is_lowercase());
    let has_digit = pwd.chars().any(|c| c.is_ascii_digit());
    let has_special = pwd.chars().any(|c| "!@#$%^&*".contains(c));
    
    let score = [has_upper, has_lower, has_digit, has_special].iter().filter(|&x| *x).count();
    
    if len < 8 || score < 2 { "Very Weak" }
    else if score == 2 { "Weak" }
    else if score == 3 { "Medium" }
    else if len >= 12 { "Very Strong" }
    else { "Strong" }
}

fn is_valid_isbn(isbn: &str) -> bool {
    let cleaned: String = isbn.chars().filter(|c| *c != '-').collect();
    matches!(cleaned.len(), 10 | 13)
}

fn is_valid_hex_color(color: &str) -> bool {
    color.starts_with('#')
}

fn is_valid_slug(slug: &str) -> bool {
    !slug.is_empty() && !slug.starts_with('-') && !slug.ends_with('-') && !slug.contains(' ')
}