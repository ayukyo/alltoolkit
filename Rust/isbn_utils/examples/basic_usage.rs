//! Basic usage examples for isbn_utils

use isbn_utils::{ISBN, generate_isbn10, generate_isbn13, validate};

fn main() {
    println!("=== ISBN Utils Examples ===\n");
    
    // Example 1: Validate ISBN-10
    println!("1. Validate ISBN-10:");
    let isbn10_str = "0-306-40615-2";
    match validate(isbn10_str) {
        Ok(isbn) => {
            println!("   {} is valid: {}", isbn10_str, isbn.is_valid());
            println!("   Digits: {}", isbn.digits());
            println!("   Formatted: {}", isbn.format());
        }
        Err(e) => println!("   Error: {}", e),
    }
    println!();
    
    // Example 2: Validate ISBN-13
    println!("2. Validate ISBN-13:");
    let isbn13_str = "978-0-306-40615-7";
    match validate(isbn13_str) {
        Ok(isbn) => {
            println!("   {} is valid: {}", isbn13_str, isbn.is_valid());
            println!("   Digits: {}", isbn.digits());
            println!("   Formatted: {}", isbn.format());
        }
        Err(e) => println!("   Error: {}", e),
    }
    println!();
    
    // Example 3: Convert ISBN-10 to ISBN-13
    println!("3. Convert ISBN-10 to ISBN-13:");
    match validate("080442957X") {
        Ok(isbn) => {
            let isbn13 = isbn.to_isbn13();
            println!("   ISBN-10: {}", isbn);
            println!("   ISBN-13: {}", isbn13);
            println!("   ISBN-13 formatted: {}", isbn13.format());
        }
        Err(e) => println!("   Error: {}", e),
    }
    println!();
    
    // Example 4: Convert ISBN-13 to ISBN-10
    println!("4. Convert ISBN-13 to ISBN-10 (978 prefix only):");
    match validate("9780306406157") {
        Ok(isbn) => {
            println!("   ISBN-13: {}", isbn);
            if let Some(isbn10) = isbn.to_isbn10() {
                println!("   ISBN-10: {}", isbn10);
                println!("   ISBN-10 formatted: {}", isbn10.format());
            }
        }
        Err(e) => println!("   Error: {}", e),
    }
    println!();
    
    // Example 5: Generate random ISBNs
    println!("5. Generate random valid ISBNs:");
    let random_isbn10 = generate_isbn10();
    let random_isbn13 = generate_isbn13();
    println!("   Random ISBN-10: {} (valid: {})", random_isbn10, random_isbn10.is_valid());
    println!("   Random ISBN-13: {} (valid: {})", random_isbn13, random_isbn13.is_valid());
    println!();
    
    // Example 6: Check registration group
    println!("6. Check registration groups:");
    if let Ok(isbn) = validate("7-04-012345-6") {
        if let ISBN::ISBN10(isbn10) = isbn {
            println!("   ISBN {} is from: {}", isbn10, isbn10.registration_group());
        }
    }
    if let Ok(isbn) = validate("978-4-06-123456-7") {
        if let ISBN::ISBN13(isbn13) = isbn {
            println!("   ISBN {} is from: {}", isbn13, isbn13.registration_group());
        }
    }
    println!();
    
    // Example 7: Detect invalid ISBNs
    println!("7. Invalid ISBN detection:");
    let test_cases = vec![
        "invalid-isbn",
        "12345",
        "9780306406158", // Wrong checksum
        "0306406153",    // Wrong checksum
    ];
    for test in test_cases {
        match validate(test) {
            Ok(isbn) => println!("   {} -> Valid: {}", test, isbn.is_valid()),
            Err(e) => println!("   {} -> Error: {}", test, e),
        }
    }
    println!();
    
    // Example 8: ISBN-10 with X checksum
    println!("8. ISBN-10 with X checksum:");
    match validate("0-8044-2957-X") {
        Ok(isbn) => {
            println!("   ISBN: {}", isbn.format());
            println!("   Valid: {}", isbn.is_valid());
            let isbn13 = isbn.to_isbn13();
            println!("   As ISBN-13: {}", isbn13.format());
        }
        Err(e) => println!("   Error: {}", e),
    }
    
    println!("\n=== All examples completed! ===");
}