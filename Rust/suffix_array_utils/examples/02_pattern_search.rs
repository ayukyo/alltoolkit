//! Example 2: Pattern Search and Matching
//! Demonstrates pattern finding and counting operations

use suffix_array_utils::SuffixArray;

fn main() {
    println!("=== Pattern Search with Suffix Array ===\n");

    let text = "abracadabra";
    let sa = SuffixArray::new(text);

    println!("Text: \"{}\"\n", text);

    // Find all occurrences of a pattern
    let patterns = vec!["abra", "a", "ra", "cad", "xyz"];

    for pattern in patterns {
        let positions = sa.find_all(pattern);
        let count = sa.count(pattern);

        println!("Pattern \"{}\":", pattern);
        println!("  Found: {}", sa.contains(pattern));
        println!("  Count: {}", count);
        println!("  Positions: {:?}", positions);
        println!();
    }

    // Find with context
    println!("Occurrences with context:");
    let occurrences = sa.occurrences("abra");
    for occ in &occurrences {
        println!("  Position {}: ...{}...", occ.position, occ.context);
    }
    println!();

    // Find longest prefix of a pattern
    let test_patterns = vec!["abrakadabra", "xyz", "abracad", "hello"];
    println!("Longest prefix of patterns:");
    for p in test_patterns {
        let lp = sa.longest_prefix_of(p);
        println!("  \"{}\" -> \"{}\"", p, lp);
    }
}