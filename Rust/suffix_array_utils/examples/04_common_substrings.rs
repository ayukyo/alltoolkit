//! Example 4: Common Substrings Between Strings
//! Demonstrates finding common substrings between multiple strings

use suffix_array_utils::{common_substrings, longest_common_substring};

fn main() {
    println!("=== Common Substrings Analysis ===\n");

    // Example 1: Simple common substring
    let s1 = "banana";
    let s2 = "orange";
    let lcs = longest_common_substring(s1, s2);
    println!("String 1: \"{}\"", s1);
    println!("String 2: \"{}\"", s2);
    println!("Longest common substring: {:?}", lcs);
    println!();

    // Example 2: Finding all common substrings
    let common = common_substrings(s1, s2, 2);
    println!("Common substrings (min length 2): {:?}", common);
    println!();

    // Example 3: DNA sequence comparison
    let dna1 = "GATTACA";
    let dna2 = "GCATGCU";
    let lcs2 = longest_common_substring(dna1, dna2);
    println!("DNA 1: \"{}\"", dna1);
    println!("DNA 2: \"{}\"", dna2);
    println!("Longest common substring: {:?}", lcs2);
    println!();

    // Example 4: Finding common patterns in code
    let code1 = "func main() { fmt.Println(\"Hello\") }";
    let code2 = "func main() { fmt.Println(\"World\") }";
    let lcs3 = longest_common_substring(code1, code2);
    println!("Code 1: \"{}\"", code1);
    println!("Code 2: \"{}\"", code2);
    println!("Longest common substring: {:?}", lcs3);
    println!();

    // Example 5: No common substring
    let s3 = "abc";
    let s4 = "xyz";
    let lcs4 = longest_common_substring(s3, s4);
    println!("String 1: \"{}\"", s3);
    println!("String 2: \"{}\"", s4);
    match lcs4 {
        Some(s) => println!("Longest common substring: \"{}\"", s),
        None => println!("No common substring found"),
    }
}