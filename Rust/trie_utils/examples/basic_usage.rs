//! Basic usage examples for Trie

use trie_utils::Trie;

fn main() {
    println!("=== Trie Basic Usage Examples ===\n");
    
    // Create a new Trie
    let mut trie = Trie::new();
    
    // Insert words with values
    println!("1. Inserting words with values:");
    trie.insert_str("apple", 1);
    trie.insert_str("app", 2);
    trie.insert_str("application", 3);
    trie.insert_str("banana", 4);
    trie.insert_str("band", 5);
    println!("   Inserted: apple(1), app(2), application(3), banana(4), band(5)");
    println!("   Trie size: {} words\n", trie.len());
    
    // Check if words exist
    println!("2. Check if words exist:");
    println!("   Contains 'apple': {}", trie.contains_str("apple"));
    println!("   Contains 'app': {}", trie.contains_str("app"));
    println!("   Contains 'ap': {} (not a complete word)\n", trie.contains_str("ap"));
    
    // Get values
    println!("3. Get values:");
    println!("   Value for 'apple': {:?}", trie.get_str("apple"));
    println!("   Value for 'banana': {:?}", trie.get_str("banana"));
    println!("   Value for 'missing': {:?}\n", trie.get_str("missing"));
    
    // Prefix search
    println!("4. Prefix search:");
    println!("   Starts with 'app': {}", trie.starts_with_str("app"));
    println!("   Starts with 'ban': {}", trie.starts_with_str("ban"));
    println!("   Starts with 'cat': {}\n", trie.starts_with_str("cat"));
    
    // Count words with prefix
    println!("5. Count words with prefix:");
    println!("   Words starting with 'app': {}", trie.count_prefix_str("app"));
    println!("   Words starting with 'ban': {}", trie.count_prefix_str("ban"));
    println!("   Words starting with 'c': {}\n", trie.count_prefix_str("c"));
    
    // Get all words with prefix
    println!("6. Get all words with prefix 'app':");
    let words = trie.get_by_prefix_str("app");
    for (word, value) in words {
        println!("   {} -> {}", word, value);
    }
    println!();
    
    // Autocomplete
    println!("7. Autocomplete for 'ban' (limit 5):");
    let suggestions = trie.autocomplete("ban", Some(5));
    println!("   Suggestions: {:?}", suggestions);
    println!();
    
    // Remove a word
    println!("8. Remove 'app':");
    let removed = trie.remove_str("app");
    println!("   Removed value: {:?}", removed);
    println!("   Contains 'app': {}", trie.contains_str("app"));
    println!("   Contains 'apple': {} (still exists)", trie.contains_str("apple"));
    println!("   Trie size: {} words\n", trie.len());
    
    // Longest prefix match
    println!("9. Longest prefix match:");
    trie.insert_str("htt", 100);
    trie.insert_str("http", 101);
    trie.insert_str("https", 102);
    
    let result = trie.longest_prefix_str("http://example.com");
    println!("   Longest prefix for 'http://example.com': {:?}", result);
    
    let result = trie.longest_prefix_str("https://example.com");
    println!("   Longest prefix for 'https://example.com': {:?}\n", result);
    
    // Get all keys
    println!("10. All keys in the trie:");
    let all_keys = trie.keys_str();
    println!("    {:?}\n", all_keys);
    
    // Iterator
    println!("11. Iterate over all entries:");
    for (key, value) in trie.iter() {
        let word: String = key.into_iter().collect();
        println!("    {} -> {}", word, value);
    }
    
    println!("\n=== Basic Examples Complete ===");
}