//! Range queries example

use skiplist::SkipList;

fn main() {
    println!("=== SkipList Range Queries Example ===\n");

    // Create and populate
    let mut list: SkipList<i32, String> = SkipList::new();
    
    for i in 0..20 {
        list.insert(i, format!("value_{}", i));
    }
    
    println!("Populated list with 20 elements (0-19)");
    println!("All elements: {:?}", list.keys().collect::<Vec<_>>());

    // Range queries with different bounds
    println!("\n--- Range: 5..10 (exclusive) ---");
    let range = list.range(5..10);
    for (k, v) in range {
        println!("  {}: {}", k, v);
    }

    println!("\n--- Range: 5..=10 (inclusive) ---");
    let range = list.range(5..=10);
    for (k, v) in range {
        println!("  {}: {}", k, v);
    }

    println!("\n--- Range: 15.. (open-ended) ---");
    let range = list.range(15..);
    for (k, v) in range {
        println!("  {}: {}", k, v);
    }

    println!("\n--- Range: ..5 (from beginning) ---");
    let range = list.range(..5);
    for (k, v) in range {
        println!("  {}: {}", k, v);
    }

    println!("\n--- Range: ..=5 (from beginning inclusive) ---");
    let range = list.range(..=5);
    for (k, v) in range {
        println!("  {}: {}", k, v);
    }

    println!("\n--- Range: .. (all elements) ---");
    let range: Vec<_> = list.range(..).collect();
    println!("  Count: {}", range.len());

    // String key example
    println!("\n--- Range with string keys ---");
    let mut str_list: SkipList<String, i32> = SkipList::new();
    
    let words = ["apple", "banana", "cherry", "date", "elderberry", "fig", "grape"];
    for (i, word) in words.iter().enumerate() {
        str_list.insert(word.to_string(), i as i32);
    }
    
    println!("Words in alphabetical order:");
    for (k, v) in str_list.iter() {
        println!("  {}: {}", k, v);
    }

    println!("\nRange: 'b'..='e' (words starting with b to e):");
    // Note: We need to use the exact keys for range queries
    let range = str_list.range("banana".to_string()..="elderberry".to_string());
    for (k, v) in range {
        println!("  {}: {}", k, v);
    }

    println!("\n=== Example Complete ===");
}