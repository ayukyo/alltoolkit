//! MTrie usage examples
//!
//! Run with: cargo run --example usage_examples

use mtrie_utils::MTrie;

fn main() {
    println!("=== MTrie Autocomplete Demo ===\n");

    // Build a trie with programming languages
    let mut trie = MTrie::from_words(&[
        "rust", "ruby", "rubyist", "rubyonrails",
        "python", "pypy", "pypi",
        "typescript", "typescript-react", "typescript-vue",
        "javascript", "javascript-react", "javascript-node",
        "java", "javascript", "kotlin", "swift",
        "go", "golang",
        "c", "c++", "c#",
        "zig", "zsh",
    ]);

    // Simulate some query history (boost popular terms)
    for _ in 0..5 { trie.record_query("rust"); }
    for _ in 0..3 { trie.record_query("python"); }
    for _ in 0..2 { trie.record_query("javascript"); }

    // Autocomplete examples
    println!("🔍 Prefix 'ru':");
    for (i, word) in trie.autocomplete("ru", 5).iter().enumerate() {
        println!("   {}: {}", i + 1, word);
    }

    println!("\n🔍 Prefix 'py':");
    for (i, word) in trie.autocomplete("py", 5).iter().enumerate() {
        println!("   {}: {}", i + 1, word);
    }

    println!("\n🔍 Prefix 'ts':");
    for (i, word) in trie.autocomplete("ts", 5).iter().enumerate() {
        println!("   {}: {}", i + 1, word);
    }

    // Fuzzy search
    println!("\n🔍 Fuzzy search 'rust' (max 1 edit):");
    for (word, dist) in trie.fuzzy_search("rust", 1) {
        println!("   - {} (distance: {})", word, dist);
    }

    println!("\n🔍 Fuzzy search 'jvascript' (max 2 edits):");
    for (word, dist) in trie.fuzzy_search("jvascript", 2) {
        println!("   - {} (distance: {})", word, dist);
    }

    // Serialize and restore
    println!("\n📦 Serialization demo:");
    let json = trie.to_json().unwrap();
    println!("   JSON length: {} bytes", json.len());

    let restored = MTrie::from_json(&json).unwrap();
    println!("   Restored {} words, contains 'rust': {}", restored.len(), restored.contains("rust"));

    // Trie stats
    println!("\n📊 Trie stats:");
    println!("   Total words: {}", trie.len());
    println!("   Is empty: {}", trie.is_empty());

    // Remove a word
    println!("\n🗑️  Removing 'zig':");
    println!("   Before: contains 'zig' = {}", trie.contains("zig"));
    trie.remove("zig");
    println!("   After:  contains 'zig' = {}", trie.contains("zig"));
    println!("   New length: {}", trie.len());
}
