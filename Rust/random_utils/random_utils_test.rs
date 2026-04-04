//! # Random Utilities Test Suite
//!
//! Comprehensive tests for the random_utils module.
//! Run with: rustc --test random_utils_test.rs -L . && ./random_utils_test

use std::collections::HashSet;

// Include the module under test
#[path = "mod.rs"]
mod random_utils;

use random_utils::*;

fn main() {
    println!("Running Random Utilities Tests...\n");
    
    test_random_int();
    test_random_float();
    test_random_bool();
    test_random_string();
    test_random_alphanumeric();
    test_random_numeric();
    test_random_hex();
    test_random_password();
    test_uuid_v4();
    test_uuid_v4_compact();
    test_pick();
    test_pick_empty();
    test_pick_unique();
    test_shuffle();
    test_random_rgb();
    test_random_hex_color();
    test_is_valid_uuid();
    test_random_bool_with_probability();
    test_random_normal();
    test_random_exponential();
    
    println!("\n✅ All tests passed!");
}

fn test_random_int() {
    print!("Testing random_int... ");
    for _ in 0..100 {
        let result = RandomUtils::random_int(1, 10);
        assert!(result >= 1 && result <= 10, "Value {} out of range", result);
    }
    println!("✓");
}

fn test_random_float() {
    print!("Testing random_float... ");
    for _ in 0..100 {
        let result = RandomUtils::random_float();
        assert!(result >= 0.0 && result < 1.0, "Value {} out of range", result);
    }
    println!("✓");
}

fn test_random_bool() {
    print!("Testing random_bool... ");
    let mut trues = 0;
    let mut falses = 0;
    for _ in 0..1000 {
        if RandomUtils::random_bool() {
            trues += 1;
        } else {
            falses += 1;
        }
    }
    // Should be roughly 50/50
    assert!(trues > 400 && trues < 600, "Distribution seems off: {} trues, {} falses", trues, falses);
    println!("✓");
}

fn test_random_bool_with_probability() {
    print!("Testing random_bool_with_probability... ");
    let mut trues = 0;
    for _ in 0..1000 {
        if RandomUtils::random_bool_with_probability(0.3) {
            trues += 1;
        }
    }
    // Should be roughly 30%
    assert!(trues > 250 && trues < 350, "Expected ~300 trues, got {}", trues);
    
    // Edge cases
    assert!(!RandomUtils::random_bool_with_probability(0.0));
    assert!(RandomUtils::random_bool_with_probability(1.0));
    println!("✓");
}

fn test_random_string() {
    print!("Testing random_string... ");
    for length in [1, 10, 50, 100] {
        let s = RandomUtils::random_string(length);
        assert_eq!(s.len(), length, "String length mismatch");
        assert!(s.chars().all(|c| c.is_ascii_alphabetic()), "Non-alphabetic char found");
    }
    println!("✓");
}

fn test_random_alphanumeric() {
    print!("Testing random_alphanumeric... ");
    for length in [1, 10, 50] {
        let s = RandomUtils::random_alphanumeric(length);
        assert_eq!(s.len(), length);
        assert!(s.chars().all(|c| c.is_ascii_alphanumeric()));
    }
    println!("✓");
}

fn test_random_numeric() {
    print!("Testing random_numeric... ");
    for length in [4, 8, 16] {
        let s = RandomUtils::random_numeric(length);
        assert_eq!(s.len(), length);
        assert!(s.chars().all(|c| c.is_ascii_digit()));
    }
    println!("✓");
}

fn test_random_hex() {
    print!("Testing random_hex... ");
    let s = RandomUtils::random_hex(16);
    assert_eq!(s.len(), 16);
    assert!(s.chars().all(|c| c.is_ascii_hexdigit() && c.is_ascii_lowercase()));
    
    let s_upper = RandomUtils::random_hex_upper(16);
    assert!(s_upper.chars().all(|c| c.is_ascii_hexdigit() && c.is_ascii_uppercase()));
    println!("✓");
}

fn test_random_password() {
    print!("Testing random_password... ");
    for length in [4, 16, 32] {
        let password = RandomUtils::random_password(length);
        assert_eq!(password.len(), length);
        
        let has_lowercase = password.chars().any(|c| c.is_ascii_lowercase());
        let has_uppercase = password.chars().any(|c| c.is_ascii_uppercase());
        let has_digit = password.chars().any(|c| c.is_ascii_digit());
        let has_special = password.chars().any(|c| SPECIAL_CHARS.contains(c));
        
        assert!(has_lowercase, "Password missing lowercase at length {}", length);
        assert!(has_uppercase, "Password missing uppercase at length {}", length);
        assert!(has_digit, "Password missing digit at length {}", length);
        assert!(has_special, "Password missing special char at length {}", length);
    }
    println!("✓");
}

fn test_uuid_v4() {
    print!("Testing uuid_v4... ");
    for _ in 0..10 {
        let uuid = RandomUtils::uuid_v4();
        assert_eq!(uuid.len(), 36, "UUID length should be 36");
        assert!(RandomUtils::is_valid_uuid(&uuid));
        
        // Check format
        let parts: Vec<&str> = uuid.split('-').collect();
        assert_eq!(parts.len(), 5);
        assert_eq!(parts[0].len(), 8);
        assert_eq!(parts[1].len(), 4);
        assert_eq!(parts[2].len(), 4);
        assert_eq!(parts[3].len(), 4);
        assert_eq!(parts[4].len(), 12);
        
        // Check version (4) and variant (8, 9, a, or b)
        assert!(parts[2].starts_with('4'), "Version should be 4");
        let variant_char = parts[3].chars().next().unwrap();
        assert!(variant_char == '8' || variant_char == '9' || variant_char == 'a' || variant_char == 'b',
            "Variant should be RFC 4122");
    }
    println!("✓");
}

fn test_uuid_v4_compact() {
    print!("Testing uuid_v4_compact... ");
    let uuid = RandomUtils::uuid_v4_compact();
    assert_eq!(uuid.len(), 32);
    assert!(uuid.chars().all(|c| c.is_ascii_hexdigit()));
    println!("✓");
}

fn test_pick() {
    print!("Testing pick... ");
    let items = vec![1, 2, 3, 4, 5];
    for _ in 0..100 {
        let picked = RandomUtils::pick(&items);
        assert!(picked.is_some());
        assert!(items.contains(&picked.unwrap()));
    }
    println!("✓");
}

fn test_pick_empty() {
    print!("Testing pick_empty... ");
    let items: Vec<i32> = vec![];
    let picked = RandomUtils::pick(&items);
    assert!(picked.is_none());
    println!("✓");
}

fn test_pick_unique() {
    print!("Testing pick_unique... ");
    let items = vec![1, 2, 3, 4, 5];
    
    // Pick 3 unique items
    let picked = RandomUtils::pick_unique(&items, 3);
    assert_eq!(picked.len(), 3);
    let set: HashSet<_> = picked.iter().collect();
    assert_eq!(set.len(), 3, "All items should be unique");
    
    // Pick more than available
    let picked = RandomUtils::pick_unique(&items, 10);
    assert_eq!(picked.len(), 5);
    
    // Pick 0
    let picked = RandomUtils::pick_unique(&items, 0);
    assert!(picked.is_empty());
    println!("✓");
}

fn test_shuffle() {
    print!("Testing shuffle... ");
    let mut items = vec![1, 2, 3, 4, 5, 6, 7, 8, 9, 10];
    let original = items.clone();
    RandomUtils::shuffle(&mut items);
    
    // Length preserved
    assert_eq!(items.len(), 10);
    
    // All elements still present
    let mut sorted = items.clone();
    sorted.sort();
    assert_eq!(sorted, original);
    
    // Test shuffled copy
    let shuffled = RandomUtils::shuffled(&original);
    assert_eq!(shuffled.len(), 10);
    let mut sorted = shuffled.clone();
    sorted.sort();
    assert_eq!(sorted, original);
    println!("✓");
}

fn test_random_rgb() {
    print!("Testing random_rgb... ");
    for _ in 0..10 {
        let (r, g, b) = RandomUtils::random_rgb();
        assert!(r <= 255);
        assert!(g <= 255);
        assert!(b <= 255);
    }
    println!("✓");
}

fn test_random_hex_color() {
    print!("Testing random_hex_color... ");
    for _ in 0..10 {
        let color = RandomUtils::random_hex_color();
        assert_eq!(color.len(), 7);
        assert!(color.starts_with('#'));
        assert!(color[1..].chars().all(|c| c.is_ascii_hexdigit()));
    }
    println!("✓");
}

fn test_is_valid_uuid() {
    print!("Testing is_valid_uuid... ");
    assert!(RandomUtils::is_valid_uuid("550e8400-e29b-41d4-a716-446655440000"));
    assert!(RandomUtils::is_valid_uuid("550e8400e29b41d4a716446655440000"));
    assert!(!RandomUtils::is_valid_uuid("invalid"));
    assert!(!RandomUtils::is_valid_uuid("550e8400-e29b-41d4-a716"));
    assert!(!RandomUtils::is_valid_uuid(""));
    println!("✓");
}

fn test_random_normal() {
    print!("Testing random_normal... ");
    let mut sum = 0.0;
    let n = 1000;
    for _ in 0..n {
        let val = RandomUtils::random_normal(0.0, 1.0);
        sum += val;
    }
    let mean = sum / n as f64;
    // Mean should be close to 0
    assert!(mean.abs() < 0.2, "Mean {} too far from 0", mean);
    println!("✓");
}

fn test_random_exponential() {
    print!("Testing random_exponential... ");
    for _ in 0..100 {
        let val = RandomUtils::random_exponential(1.0);
        assert!(val >= 0.0, "Exponential should be non-negative");
    }
    println!("✓");
}