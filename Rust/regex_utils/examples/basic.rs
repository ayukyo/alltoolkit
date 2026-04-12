//! # Regex Utils Examples
//!
//! This file demonstrates practical usage of the regex_utils module.
//! Run with: cargo run --example basic

use regex_utils::{
    is_email, is_phone, is_url, is_date,
    extract_emails, extract_numbers, extract_urls,
    replace_all, sanitize_filename,
};

fn main() {
    println!("🔍 Regex Utils Examples\n");

    // Example 1: Email Validation
    println!("📧 Email Validation:");
    let emails = vec![
        "user@example.com",
        "invalid.email",
        "admin@test.org",
        "@missing.com",
    ];
    
    for email in emails {
        let status = if is_email(email) { "✓" } else { "✗" };
        println!("  {} {}", status, email);
    }
    println!();

    // Example 2: Phone Number Validation
    println!("📱 Phone Number Validation:");
    let phones = vec![
        "+1234567890",
        "13812345678",
        "123",
        "+8619912345678",
    ];
    
    for phone in phones {
        let status = if is_phone(phone) { "✓" } else { "✗" };
        println!("  {} {}", status, phone);
    }
    println!();

    // Example 3: URL Validation
    println!("🌐 URL Validation:");
    let urls = vec![
        "https://example.com",
        "http://localhost:8080",
        "not-a-url",
        "ftp://invalid.com",
    ];
    
    for url in urls {
        let status = if is_url(url) { "✓" } else { "✗" };
        println!("  {} {}", status, url);
    }
    println!();

    // Example 4: Extract Emails from Text
    println!("📥 Extract Emails from Text:");
    let text = "Contact us at support@example.com or sales@company.org for help.";
    let emails = extract_emails(text);
    println!("  Found {} emails:", emails.len());
    for email in emails {
        println!("    - {}", email);
    }
    println!();

    // Example 5: Extract Numbers from Text
    println!("🔢 Extract Numbers from Text:");
    let text = "The price is $100, with a 20% discount, final: $80.";
    let numbers = extract_numbers(text);
    println!("  Found numbers: {:?}", numbers);
    println!();

    // Example 6: Extract URLs from Text
    println!("🔗 Extract URLs from Text:");
    let text = "Visit https://example.com or http://test.org/path for more info.";
    let urls = extract_urls(text);
    println!("  Found {} URLs:", urls.len());
    for url in urls {
        println!("    - {}", url);
    }
    println!();

    // Example 7: Replace Pattern
    println!("🔄 Replace Pattern:");
    let text = "Order #12345, Item #67890";
    let result = replace_all(r"#\d+", text, "#REDACTED");
    println!("  Original: {}", text);
    println!("  Redacted: {}", result);
    println!();

    // Example 8: Sanitize Filename
    println!("📁 Sanitize Filename:");
    let filenames = vec![
        "my file: name?.txt",
        "document (final version).pdf",
        "test<>file.txt",
    ];
    
    for filename in filenames {
        let sanitized = sanitize_filename(filename);
        println!("  '{}' → '{}'", filename, sanitized);
    }
    println!();

    // Example 9: Date Validation
    println!("📅 Date Validation:");
    let dates = vec![
        "2024-06-15",
        "2024-13-01",
        "2024/06/15",
        "2000-01-01",
    ];
    
    for date in dates {
        let status = if is_date(date) { "✓" } else { "✗" };
        println!("  {} {}", status, date);
    }
    println!();

    println!("✅ All examples completed!");
}
