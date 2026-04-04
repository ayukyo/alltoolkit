//! # Random Utilities Example
//!
//! This example demonstrates the usage of the random_utils module
//! for generating random numbers, strings, passwords, UUIDs, and more.
//!
//! Run with: rustc --edition 2021 random_utils_example.rs -L ../random_utils && ./random_utils_example

#[path = "../random_utils/mod.rs"]
mod random_utils;

use random_utils::*;

fn main() {
    println!("╔══════════════════════════════════════════════════════════════╗");
    println!("║          Random Utilities - Usage Examples                   ║");
    println!("╚══════════════════════════════════════════════════════════════╝\n");

    example_random_numbers();
    example_random_strings();
    example_password_generation();
    example_uuid_generation();
    example_random_selection();
    example_random_colors();
    example_custom_charset();
}

fn example_random_numbers() {
    println!("📊 Random Number Generation");
    println!("─────────────────────────────────────────────────────────────");
    
    // Basic random integers
    println!("Random i32: {}", RandomUtils::random_i32());
    println!("Random i64: {}", RandomUtils::random_i64());
    println!("Random u32: {}", RandomUtils::random_u32());
    println!("Random u64: {}", RandomUtils::random_u64());
    
    // Range-based integers
    println!("\nRandom integers in range [1, 100]:");
    for _ in 0..5 {
        print!("{} ", RandomUtils::random_int(1, 100));
    }
    println!();
    
    // Dice roll simulation
    println!("\nRolling a dice 10 times:");
    for _ in 0..10 {
        print!("{} ", RandomUtils::random_int(1, 6));
    }
    println!();
    
    // Random floats
    println!("\nRandom floats [0.0, 1.0):");
    for _ in 0..5 {
        print!("{:.4} ", RandomUtils::random_float());
    }
    println!();
    
    // Random float in range
    println!("\nRandom floats in range [10.0, 20.0):");
    for _ in 0..5 {
        print!("{:.2} ", RandomUtils::random_float_range(10.0, 20.0));
    }
    println!();
    
    // Random booleans
    println!("\nRandom booleans:");
    for _ in 0..10 {
        print!("{} ", if RandomUtils::random_bool() { "T" } else { "F" });
    }
    println!();
    
    // Weighted probability
    println!("\nRandom bool with 70% true probability (20 samples):");
    for _ in 0..20 {
        print!("{} ", if RandomUtils::random_bool_with_probability(0.7) { "T" } else { "F" });
    }
    println!("\n");
}

fn example_random_strings() {
    println!("\n🔤 Random String Generation");
    println!("─────────────────────────────────────────────────────────────");
    
    // Alphabetic strings
    println!("Random alphabetic strings:");
    for len in [8, 16, 32] {
        println!("  Length {:2}: {}", len, RandomUtils::random_string(len));
    }
    
    // Alphanumeric strings
    println!("\nRandom alphanumeric strings:");
    for len in [8, 16, 32] {
        println!("  Length {:2}: {}", len, RandomUtils::random_alphanumeric(len));
    }
    
    // Numeric strings
    println!("\nRandom numeric strings:");
    for len in [4, 8, 16] {
        println!("  Length {:2}: {}", len, RandomUtils::random_numeric(len));
    }
    
    // Hex strings
    println!("\nRandom hex strings:");
    println!("  Lowercase (16): {}", RandomUtils::random_hex(16));
    println!("  Uppercase (16): {}", RandomUtils::random_hex_upper(16));
    
    // URL-safe strings
    println!("\nURL-safe random strings:");
    println!("  Length 32: {}", RandomUtils::random_urlsafe(32));
    println!("  Length 64: {}", RandomUtils::random_urlsafe(64));
    println!();
}

fn example_password_generation() {
    println!("\n🔐 Password Generation");
    println!("─────────────────────────────────────────────────────────────");
    
    println!("Secure random passwords (guaranteed to have lowercase, uppercase, digit, special):");
    for len in [8, 12, 16, 24, 32] {
        let password = RandomUtils::random_password(len);
        
        // Verify password requirements
        let has_lower = password.chars().any(|c| c.is_ascii_lowercase());
        let has_upper = password.chars().any(|c| c.is_ascii_uppercase());
        let has_digit = password.chars().any(|c| c.is_ascii_digit());
        let has_special = password.chars().any(|c| SPECIAL_CHARS.contains(c));
        
        println!("  Length {:2}: {}", len, password);
        println!("            [lower:{}, upper:{}, digit:{}, special:{}]",
            if has_lower { "✓" } else { "✗" },
            if has_upper { "✓" } else { "✗" },
            if has_digit { "✓" } else { "✗" },
            if has_special { "✓" } else { "✗" });
    }
    println!();
}

fn example_uuid_generation() {
    println!("\n🆔 UUID Generation (RFC 4122 v4)");
    println!("─────────────────────────────────────────────────────────────");
    
    println!("Standard UUID v4:");
    for i in 1..=5 {
        println!("  {}: {}", i, RandomUtils::uuid_v4());
    }
    
    println!("\nCompact UUID v4 (no hyphens):");
    for i in 1..=3 {
        println!("  {}: {}", i, RandomUtils::uuid_v4_compact());
    }
    
    println!("\nUppercase UUID v4:");
    println!("  {}", RandomUtils::uuid_v4_upper());
    
    // Validation
    let uuid = RandomUtils::uuid_v4();
    println!("\nUUID validation:");
    println!("  '{}' is valid: {}", uuid, RandomUtils::is_valid_uuid(&uuid));
    println!("  'invalid-uuid' is valid: {}", RandomUtils::is_valid_uuid("invalid-uuid"));
    println!();
}

fn example_random_selection() {
    println!("\n🎲 Random Selection from Collections");
    println!("─────────────────────────────────────────────────────────────");
    
    let fruits = vec!["Apple", "Banana", "Cherry", "Date", "Elderberry", "Fig", "Grape"];
    println!("Fruits: {:?}", fruits);
    
    // Pick single element
    println!("\nRandom picks (single):");
    for _ in 0..5 {
        if let Some(fruit) = RandomUtils::pick(&fruits) {
            print!("{} ", fruit);
        }
    }
    println!();
    
    // Pick multiple with replacement
    println!("\nRandom picks (10 with replacement):");
    let picks = RandomUtils::pick_multiple(&fruits, 10);
    for fruit in &picks {
        print!("{} ", fruit);
    }
    println!();
    
    // Pick multiple unique (without replacement)
    println!("\nRandom picks (5 unique, without replacement):");
    let unique_picks = RandomUtils::pick_unique(&fruits, 5);
    for fruit in &unique_picks {
        print!("{} ", fruit);
    }
    println!();
    
    // Shuffle
    println!("\nShuffled fruits:");
    let shuffled = RandomUtils::shuffled(&fruits);
    for fruit in &shuffled {
        print!("{} ", fruit);
    }
    println!("\n");
    
    // Numbers example
    let numbers: Vec<i32> = (1..=20).collect();
    println!("\nPick 5 unique numbers from 1-20:");
    let lucky_numbers = RandomUtils::pick_unique(&numbers, 5);
    for num in &lucky_numbers {
        print!("{} ", num);
    }
    println!("\n");
}

fn example_random_colors() {
    println!("\n🎨 Random Color Generation");
    println!("─────────────────────────────────────────────────────────────");
    
    println!("Random RGB colors:");
    for _ in 0..5 {
        let (r, g, b) = RandomUtils::random_rgb();
        println!("  RGB({}, {}, {})", r, g, b);
    }
    
    println!("\nRandom hex colors:");
    for _ in 0..5 {
        println!("  {}", RandomUtils::random_hex_color());
    }
    
    println!("\nRandom RGBA colors:");
    for _ in 0..3 {
        let (r, g, b, a) = RandomUtils::random_rgba();
        println!("  RGBA({}, {}, {}, {})", r, g, b, a);
    }
    println!();
}

fn example_custom_charset() {
    println!("\n🔧 Custom Character Set");
    println!("─────────────────────────────────────────────────────────────");
    
    // Binary string
    let binary = RandomUtils::random_string_from_charset(32, "01");
    println!("Random binary (32 chars): {}", binary);
    
    // DNA sequence
    let dna = RandomUtils::random_string_from_charset(40, "ACGT");
    println!("Random DNA sequence: {}", dna);
    
    // Emoji-like (using safe characters)
    let emoji_chars = "😀😁😂🤣😃😄😅😆😉😊😋😎😍😘🥰";
    let emoji_string = RandomUtils::random_string_from_charset(10, emoji_chars);
    println!("Random emoji string: {}", emoji_string);
    
    // Base32 encoded string
    let base32 = RandomUtils::random_string_from_charset(16, "ABCDEFGHIJKLMNOPQRSTUVWXYZ234567");
    println!("Random Base32: {}", base32);
    
    // Custom token format
    let custom_charset = "ABCDEFGHJKLMNPQRSTUVWXYZ23456789"; // No confusing chars (0/O, 1/I/l)
    let token = RandomUtils::random_string_from_charset(20, custom_charset);
    println!("Custom token (no confusing chars): {}", token);
    println!();
}