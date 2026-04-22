//! Example 1: Basic Suffix Array Operations
//! Demonstrates creation and basic operations on suffix arrays

use suffix_array_utils::SuffixArray;

fn main() {
    println!("=== Suffix Array Basic Usage ===\n");

    // Create a suffix array
    let text = "banana";
    let sa = SuffixArray::new(text);

    println!("Original text: \"{}\"", sa.original());
    println!("Text length: {}", sa.len());
    println!();

    // Show all suffixes in sorted order
    println!("Sorted suffixes:");
    for i in 0..sa.len() {
        if let Some((suffix, idx)) = sa.nth_element(i) {
            let padding = " ".repeat(sa.len() - suffix.len());
            println!("  {}: {}{} (starts at index {})", i, padding, suffix, idx);
        }
    }
    println!();

    // Get suffix indices
    println!("Suffix array indices: {:?}", sa.indices());
    println!();

    // Show LCP array
    let lcp = sa.lcp();
    println!("LCP array: {:?}", lcp);
    println!();

    // Access individual suffix
    println!("Suffix at position 0: {:?}", sa.suffix(0));
    println!("Suffix at position 3: {:?}", sa.suffix(3));
}