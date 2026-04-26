//! Example usage of skiplist_utils
//! 
//! Run with: cargo run --example basic_usage

use skiplist_utils::SkipList;

fn main() {
    println!("=== Skip List Utils Examples ===\n");

    // Example 1: Basic usage
    basic_example();

    // Example 2: Out of order insert
    out_of_order_example();

    // Example 3: String keys
    string_keys_example();

    // Example 4: Min/Max operations
    min_max_example();

    // Example 5: Rank operations
    rank_example();

    // Example 6: Iterator
    iterator_example();

    // Example 7: Large dataset performance
    large_dataset_example();

    // Example 8: For each with early exit
    for_each_example();
}

fn basic_example() {
    println!("--- Basic Usage ---");
    
    let mut sl = SkipList::new();

    // Insert elements
    sl.insert(1, "one");
    sl.insert(2, "two");
    sl.insert(3, "three");

    println!("Length: {}", sl.len());
    println!("Is empty: {}", sl.is_empty());

    // Search
    if let Some(value) = sl.get(&2) {
        println!("Found key 2: {}", value);
    }

    // Contains
    println!("Contains 3: {}", sl.contains(&3));
    println!("Contains 100: {}", sl.contains(&100));

    // Update existing key
    sl.insert(2, "TWO UPDATED");
    println!("Updated value for key 2: {}", sl.get(&2).unwrap());

    // Remove
    if let Some(value) = sl.remove(&1) {
        println!("Removed key 1 with value: {}", value);
    }
    println!("Length after removal: {}", sl.len());

    println!();
}

fn out_of_order_example() {
    println!("--- Out of Order Insert ---");
    
    let mut sl = SkipList::new();
    
    // Insert in random order
    sl.insert(5, "five");
    sl.insert(1, "one");
    sl.insert(10, "ten");
    sl.insert(3, "three");
    sl.insert(7, "seven");

    // Keys are automatically sorted
    println!("Keys (sorted): {:?}", sl.keys());
    println!("Values (sorted by key): {:?}", sl.values());
    println!();
}

fn string_keys_example() {
    println!("--- String Keys ---");
    
    let mut sl = SkipList::new();
    
    sl.insert("banana".to_string(), 1);
    sl.insert("apple".to_string(), 2);
    sl.insert("cherry".to_string(), 3);
    sl.insert("date".to_string(), 4);

    // String keys are sorted alphabetically
    println!("Keys: {:?}", sl.keys());
    
    // Get a specific value
    println!("Value for 'cherry': {}", sl.get(&"cherry".to_string()).unwrap());
    println!();
}

fn min_max_example() {
    println!("--- Min/Max Operations ---");
    
    let mut sl = SkipList::new();
    
    sl.insert(50, "fifty");
    sl.insert(25, "twenty-five");
    sl.insert(75, "seventy-five");
    sl.insert(10, "ten");
    sl.insert(90, "ninety");

    if let Some((min_key, min_val)) = sl.min() {
        println!("Min: key={}, value={}", min_key, min_val);
    }

    if let Some((max_key, max_val)) = sl.max() {
        println!("Max: key={}, value={}", max_key, max_val);
    }
    println!();
}

fn rank_example() {
    println!("--- Rank Operations ---");
    
    let mut sl = SkipList::new();
    
    // Insert scores
    sl.insert(85, "Alice");
    sl.insert(92, "Bob");
    sl.insert(78, "Charlie");
    sl.insert(88, "Diana");
    sl.insert(95, "Eve");
    sl.insert(82, "Frank");

    println!("All scores sorted: {:?}", sl.keys());

    // Get rank of specific key
    println!("Rank of 88 (Diana): {:?}", sl.rank(&88));
    println!("Rank of 78 (Charlie): {:?}", sl.rank(&78));

    // Get element by rank
    if let Some((key, value)) = sl.get_by_rank(3) {
        println!("Element at rank 3: key={}, value={}", key, value);
    }
    println!();
}

fn iterator_example() {
    println!("--- Iterator ---");
    
    let mut sl = SkipList::new();
    
    sl.insert(1, "first");
    sl.insert(2, "second");
    sl.insert(3, "third");
    sl.insert(4, "fourth");

    println!("Iterating through all elements:");
    for (key, value) in sl.iter() {
        println!("  key={}, value={}", key, value);
    }
    println!();
}

fn large_dataset_example() {
    println!("--- Large Dataset Performance ---");
    
    let mut sl = SkipList::with_max_level(20);
    let n = 10000;

    // Insert elements
    for i in 0..n {
        sl.insert(i, i * i);
    }
    
    println!("Inserted {} elements", n);
    println!("Length: {}", sl.len());
    println!("Current level: {}", sl.level());
    println!("Max level: {}", sl.max_level());

    // Search performance test
    let search_key = 5000;
    if let Some(value) = sl.get(&search_key) {
        println!("Found key {}: {}", search_key, value);
    }

    // Delete half
    for i in 0..n/2 {
        sl.remove(&i);
    }
    println!("After deleting half, length: {}", sl.len());
    println!();
}

fn for_each_example() {
    println!("--- For Each with Early Exit ---");
    
    let mut sl = SkipList::new();
    
    sl.insert(1, "one");
    sl.insert(2, "two");
    sl.insert(3, "three");
    sl.insert(4, "four");
    sl.insert(5, "five");

    println!("Full iteration:");
    let mut count = 0;
    sl.for_each(|key, value| {
        println!("  key={}, value={}", key, value);
        count += 1;
        true
    });
    println!("Iterated {} times", count);

    println!("\nEarly exit (stop after 3):");
    count = 0;
    sl.for_each(|key, value| {
        println!("  key={}, value={}", key, value);
        count += 1;
        count < 3
    });
    println!("Iterated {} times before exit", count);
    println!();
}