//! Example 5: Distinct Substrings and Advanced Operations
//! Demonstrates counting and enumerating distinct substrings

use suffix_array_utils::SuffixArray;

fn main() {
    println!("=== Distinct Substrings Analysis ===\n");

    // Count distinct substrings
    let texts = vec!["abc", "aaa", "banana", "hello"];

    for text in texts {
        let sa = SuffixArray::new(text);
        let n = text.len();
        let total = n * (n + 1) / 2;
        let distinct = sa.count_distinct_substrings();

        println!("Text: \"{}\"", text);
        println!("  Total substrings: {}", total);
        println!("  Distinct substrings: {}", distinct);
        println!("  Repeated substrings: {}", total - distinct);
        println!();
    }

    // Enumerate all distinct substrings
    let text = "abc";
    let sa = SuffixArray::new(text);
    let substrings = sa.all_substrings();
    println!("All distinct substrings of \"{}\":", text);
    for (i, s) in substrings.iter().enumerate() {
        println!("  {}: \"{}\"", i + 1, s);
    }
    println!();

    // Get k-th distinct substring
    println!("K-th distinct substrings:");
    for k in 1..=6 {
        let substr = sa.kth_distinct_substring(k);
        println!("  {}-th: {:?}", k, substr);
    }
    println!();

    // Display distinct substrings of "banana"
    let sa2 = SuffixArray::new("banana");
    let substrings2 = sa2.all_substrings();
    println!(
        "All {} distinct substrings of \"banana\":",
        substrings2.len()
    );
    for (i, s) in substrings2.iter().enumerate() {
        if i < 10 || i >= substrings2.len() - 5 {
            println!("  {}: \"{}\"", i + 1, s);
        } else if i == 10 {
            println!("  ... ({} more)", substrings2.len() - 15);
        }
    }
}