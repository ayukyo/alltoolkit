//! Example 6: Advanced Features - Palindromes, Rotations, and More
//! Demonstrates advanced string analysis capabilities

use suffix_array_utils::{min_lexicographic_rotation, SuffixArray};

fn main() {
    println!("=== Advanced Suffix Array Features ===\n");

    // Palindromic substrings
    println!("--- Longest Palindromic Substrings ---");
    let palindromes = vec!["babad", "racecar", "cbbd", "hello", "level"];
    for text in palindromes {
        let sa = SuffixArray::new(text);
        let lps = sa.longest_palindromic_substring();
        println!(
            "  \"{}\" -> {:?} (length: {})",
            text,
            lps,
            lps.map_or(0, |s| s.len())
        );
    }
    println!();

    // Minimum lexicographic rotation
    println!("--- Minimum Lexicographic Rotation ---");
    let rotations = vec!["banana", "abcde", "cdefab", "aaaa", "bbaa"];
    for text in rotations {
        let min_rot = min_lexicographic_rotation(text);
        println!("  \"{}\" -> \"{}\"", text, min_rot);
    }
    println!();

    // Rank and comparison operations
    println!("--- Rank and Comparison ---");
    let text = "banana";
    let sa = SuffixArray::new(text);
    println!("Text: \"{}\"", text);
    println!("Suffix array indices: {:?}", sa.indices());
    println!();

    // Get rank of each position
    println!("Rank of suffix starting at each position:");
    for i in 0..text.len() {
        let rank = sa.rank(i);
        println!("  Position {} ('{}') has rank {:?}", i, &text[i..], rank);
    }
    println!();

    // LCP between specific suffix positions
    println!("--- Longest Common Prefix ---");
    println!("LCP between specific suffix positions:");
    println!(
        "  LCP(0, 1): {}",
        sa.lcp_between(0, 1)
    ); // "banana" vs "anana"
    println!(
        "  LCP(2, 4): {}",
        sa.lcp_between(2, 4)
    ); // "nana" vs "na"
    println!();

    // Practical application: document similarity
    println!("--- Practical Application: Document Analysis ---");
    let doc = "The quick brown fox jumps over the lazy dog. The dog was not lazy.";
    let sa_doc = SuffixArray::new(doc);
    println!("Document: \"{}\"", doc);
    println!(
        "Longest repeated phrase: {:?}",
        sa_doc.longest_repeated_substring()
    );
    println!("Number of distinct substrings: {}", sa_doc.count_distinct_substrings());
    println!("Word 'the' appears {} times", sa_doc.count("the"));
    println!("Word 'lazy' appears {} times", sa_doc.count("lazy"));
}