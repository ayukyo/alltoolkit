//! Basic usage examples for Z Algorithm Utilities (Rust)

use z_algorithm_utils::*;

fn main() {
    println!("{}", "="..repeat(60));
    println!("Z Algorithm Utilities - Rust Examples");
    println!("{}", "="..repeat(60));

    // 1. Z-Array Computation
    println!("\n1. Z-Array Computation");
    println!("{}", "-"..repeat(40));
    let s = "aabcaabxaaz";
    let z = z_array(s);
    println!("String: {}", s);
    println!("Z-array: {:?}", z);
    println!();

    // 2. Visualization
    println!("\n2. Visualization");
    println!("{}", "-"..repeat(40));
    println!("{}", visualize_z_array("aaaa"));
    println!();

    // 3. Pattern Matching
    println!("\n3. Pattern Matching");
    println!("{}", "-"..repeat(40));
    let text = "The quick brown fox jumps over the lazy dog. The fox is quick.";
    let pattern = "fox";
    let positions = find_all_occurrences(pattern, text);
    println!("Searching for '{}' in text:", pattern);
    println!("  Found at positions: {:?}", positions);
    println!("  Count: {}", count_occurrences(pattern, text));
    println!();

    // 4. Multi-pattern search
    println!("Multi-pattern search:");
    let matcher = ZPatternMatcher::new(&["quick", "fox", "dog"]);
    let results = matcher.search(text);
    println!("  Found {} matches:", results.len());
    for (i, pos, p) in results {
        println!("    '{}' at position {}", p, pos);
    }
    println!();

    // 5. Substring Analysis
    println!("\n5. Substring Analysis");
    println!("{}", "-"..repeat(40));
    let s1 = "abacababacab";
    let lps = longest_prefix_suffix(s1);
    println!("String: {}", s1);
    println!("Longest prefix-suffix length: {}", lps);
    println!();

    let s2 = "banana";
    let (substr, positions2) = longest_repeated_substring(s2);
    println!("String: {}", s2);
    println!("Longest repeated substring: '{}' at positions {:?}", substr, positions2);
    println!();

    // 6. Period Detection
    println!("\n6. Period Detection");
    println!("{}", "-"..repeat(40));
    let s3 = "abcabcabcabc";
    let period = find_minimal_period(s3);
    println!("String: {}", s3);
    println!("Minimal period: {}", period.period);
    println!("Is periodic: {}", period.is_periodic);
    println!("Repeating unit: '{}'", period.period_string());
    println!();

    // 7. Rotation Check
    println!("\n7. Rotation Check");
    println!("{}", "-"..repeat(40));
    let s4 = "waterbottle";
    let s5 = "erbottlewat";
    println!("Is '{}' a rotation of '{}'? {}", s5, s4, is_rotation(s4, s5));
    println!();

    // 8. Compression
    println!("\n8. String Compression");
    println!("{}", "-"..repeat(40));
    let s7 = "abcabcabcabcabc";
    let (pattern, count) = compress_string(s7);
    println!("Original: {}", s7);
    println!("Compressed: pattern='{}', count={}", pattern, count);
    println!();

    // 9. Helper Functions
    println!("\n9. Helper Functions");
    println!("{}", "-"..repeat(40));
    println!("Contains('abc', 'abcabc'): {}", contains("abc", "abcabc"));
    let replaced = replace_all("abc", "xyz", "abcabcabc");
    println!("ReplaceAll('abc'->'xyz'): {}", replaced);
    let parts = split_by_pattern(",", "a,b,c,d");
    println!("SplitByPattern(',', 'a,b,c,d'): {:?}", parts);
    println!();

    println!("{}", "="..repeat(60));
    println!("All examples completed successfully!");
    println!("{}", "="..repeat(60));
}