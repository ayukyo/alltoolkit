//! Example 3: Repeated Substrings
//! Demonstrates finding repeated and longest repeated substrings

use suffix_array_utils::SuffixArray;

fn main() {
    println!("=== Repeated Substrings Analysis ===\n");

    // Example 1: Simple repeated substring
    let text1 = "banana";
    let sa1 = SuffixArray::new(text1);
    println!("Text: \"{}\"", text1);
    println!(
        "Longest repeated substring: {:?}",
        sa1.longest_repeated_substring()
    );
    println!("All repeated substrings: {:?}", sa1.all_repeated_substrings());
    println!();

    // Example 2: Multiple repetitions
    let text2 = "abcabcabc";
    let sa2 = SuffixArray::new(text2);
    println!("Text: \"{}\"", text2);
    println!(
        "Longest repeated substring: {:?}",
        sa2.longest_repeated_substring()
    );
    println!();

    // Example 3: DNA sequence analysis
    let text3 = "GATAGACA";
    let sa3 = SuffixArray::new(text3);
    println!("DNA sequence: \"{}\"", text3);
    println!(
        "Longest repeated substring: {:?}",
        sa3.longest_repeated_substring()
    );
    println!();

    // Example 4: With minimum occurrence requirement
    let text4 = "aaaa";
    let sa4 = SuffixArray::new(text4);
    println!("Text: \"{}\"", text4);
    println!(
        "Longest repeated (min 2): {:?}",
        sa4.longest_repeated_substring_min(2)
    );
    println!(
        "Longest repeated (min 3): {:?}",
        sa4.longest_repeated_substring_min(3)
    );
    println!(
        "Longest repeated (min 4): {:?}",
        sa4.longest_repeated_substring_min(4)
    );
    println!();

    // Example 5: No repetition
    let text5 = "abcdefgh";
    let sa5 = SuffixArray::new(text5);
    println!("Text: \"{}\"", text5);
    match sa5.longest_repeated_substring() {
        Some(s) => println!("Longest repeated substring: \"{}\"", s),
        None => println!("No repeated substring found"),
    }
}