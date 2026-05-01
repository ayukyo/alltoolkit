//! Example demonstrating roman_numeral_utils usage

use roman_numeral_utils::{to_roman, from_roman, is_valid_roman, to_roman_lowercase, get_symbols};

fn main() {
    println!("=== Roman Numeral Utils Demo ===\n");
    
    // Basic conversion: integer to Roman
    println!("Integer to Roman Numeral:");
    let years = [1, 4, 9, 40, 99, 100, 400, 500, 999, 1000, 2024, 3999];
    for year in years {
        match to_roman(year) {
            Ok(roman) => println!("  {:4} -> {}", year, roman),
            Err(e) => println!("  {:4} -> Error: {}", year, e),
        }
    }
    
    println!();
    
    // Roman numeral to integer
    println!("Roman Numeral to Integer:");
    let numerals = ["I", "IV", "IX", "XL", "XC", "C", "CD", "D", "CM", "M", "MMXXIV", "MMMCMXCIX"];
    for numeral in numerals {
        match from_roman(numeral) {
            Ok(num) => println!("  {:12} -> {}", numeral, num),
            Err(e) => println!("  {:12} -> Error: {}", numeral, e),
        }
    }
    
    println!();
    
    // Validation
    println!("Validation:");
    let test_cases = ["MMXXIV", "iv", "IIII", "VV", ""];
    for tc in test_cases {
        let status = if is_valid_roman(tc) { "✓ Valid" } else { "✗ Invalid" };
        println!("  {:8} -> {}", format!("'{}'", tc), status);
    }
    
    println!();
    
    // Lowercase output
    println!("Lowercase Output:");
    match to_roman_lowercase(2024) {
        Ok(roman) => println!("  2024 -> {} (lowercase)", roman),
        Err(e) => println!("  Error: {}", e),
    }
    
    println!();
    
    // Famous years
    println!("Famous Historical Years:");
    let famous = [
        (1066, "Battle of Hastings"),
        (1215, "Magna Carta"),
        (1776, "US Independence"),
        (1789, "French Revolution"),
        (1945, "End of WWII"),
        (2000, "New Millennium"),
        (2024, "Current Year"),
    ];
    for (year, event) in famous {
        match to_roman(year) {
            Ok(roman) => println!("  {} - {} ({})", roman, event, year),
            Err(e) => println!("  Error for {}: {}", year, e),
        }
    }
    
    println!();
    
    // Show all symbols
    println!("All Basic Roman Numeral Symbols:");
    let symbols = get_symbols();
    for (value, symbol) in symbols {
        println!("  {:4} -> {}", value, symbol);
    }
}