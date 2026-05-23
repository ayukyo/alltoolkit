//! Autocomplete Utils Examples
//!
//! Run with: cargo run --example autocomplete_demo

use autocomplete_utils::Autocomplete;

fn main() {
    println!("=== Autocomplete Utils Demo ===\n");

    // Create a new autocomplete instance
    let mut ac = Autocomplete::new();
    
    // Add some programming-related words
    let words = vec![
        "function",
        "variable",
        "const",
        "let",
        "class",
        "closure",
        "callback",
        "promise",
        "async",
        "await",
        "array",
        "object",
        "string",
        "number",
        "boolean",
        "null",
        "undefined",
        "console",
        "constructor",
        "continue",
        "context",
        "constantly",
    ];
    
    println!("Inserting {} words into the trie...\n", words.len());
    ac.insert_batch(&words);
    
    // Basic autocomplete suggestions
    println!("--- Autocomplete Suggestions ---");
    
    println!("\nPrefix 'con':");
    for word in ac.suggest("con", 5) {
        println!("  - {}", word);
    }
    
    println!("\nPrefix 'cl':");
    for word in ac.suggest("cl", 5) {
        println!("  - {}", word);
    }
    
    println!("\nPrefix 'a':");
    for word in ac.suggest("a", 10) {
        println!("  - {}", word);
    }
    
    // Frequency-based ranking
    println!("\n--- Frequency-based Ranking ---");
    let mut ac2 = Autocomplete::new();
    
    // Insert words with different frequencies
    for _ in 0..5 {
        ac2.insert("apple");
    }
    for _ in 0..3 {
        ac2.insert("application");
    }
    for _ in 0..1 {
        ac2.insert("appetite");
    }
    
    println!("\nWords starting with 'app' (sorted by frequency):");
    for word in ac2.suggest("app", 10) {
        let freq = ac2.get_frequency(&word);
        println!("  - {} (frequency: {})", word, freq);
    }
    
    // Case-insensitive mode
    println!("\n--- Case-insensitive Mode ---");
    let mut ac3 = Autocomplete::new_case_insensitive();
    ac3.insert("JavaScript");
    ac3.insert("Java");
    ac3.insert("JAVASCRIPT");
    
    println!("\nSearching for 'java' in case-insensitive mode:");
    for word in ac3.suggest("java", 5) {
        println!("  - {}", word);
    }
    
    println!("\nContains 'JAVASCRIPT': {}", ac3.contains("JAVASCRIPT"));
    println!("Contains 'javascript': {}", ac3.contains("javascript"));
    
    // Word operations
    println!("\n--- Word Operations ---");
    let mut ac4 = Autocomplete::new();
    ac4.insert_batch(&["hello", "help", "helicopter"]);
    
    println!("\nTotal words: {}", ac4.word_count());
    println!("Contains 'hello': {}", ac4.contains("hello"));
    println!("Starts with 'hel': {}", ac4.starts_with("hel"));
    
    // Remove a word
    println!("\nRemoving 'hello'...");
    ac4.remove("hello");
    println!("Contains 'hello': {}", ac4.contains("hello"));
    println!("Total words: {}", ac4.word_count());
    
    // Get all words
    println!("\n--- All Words ---");
    println!("All words in trie:");
    let mut all_words = ac4.get_all_words();
    all_words.sort();
    for word in all_words {
        println!("  - {}", word);
    }
    
    // Increment frequency example
    println!("\n--- Learning User Preferences ---");
    let mut ac5 = Autocomplete::new();
    ac5.insert("search");
    ac5.insert("settings");
    ac5.insert("share");
    
    println!("\nInitial frequencies:");
    for word in ac5.suggest("s", 10) {
        println!("  - {}: {}", word, ac5.get_frequency(&word));
    }
    
    // Simulate user selecting "settings" multiple times
    println!("\nUser selects 'settings' 5 times...");
    for _ in 0..5 {
        ac5.increment_frequency("settings");
    }
    
    println!("\nAfter learning:");
    for word in ac5.suggest("s", 10) {
        println!("  - {}: {}", word, ac5.get_frequency(&word));
    }
    
    println!("\n=== Demo Complete ===");
}