//! Basic SkipList operations example

use skiplist::SkipList;

fn main() {
    println!("=== SkipList Basic Operations Example ===\n");

    // Create a new skip list
    let mut list: SkipList<i32, String> = SkipList::new();
    println!("Created empty skip list");

    // Insert some values
    println!("\n--- Inserting values ---");
    list.insert(10, "ten".to_string());
    list.insert(20, "twenty".to_string());
    list.insert(5, "five".to_string());
    list.insert(15, "fifteen".to_string());
    list.insert(25, "twenty-five".to_string());
    
    println!("Inserted: 10, 20, 5, 15, 25");
    println!("Length: {}", list.len());

    // Get values
    println!("\n--- Getting values ---");
    println!("get(10) = {:?}", list.get(&10));
    println!("get(5) = {:?}", list.get(&5));
    println!("get(100) = {:?}", list.get(&100)); // Not found

    // Update existing key
    println!("\n--- Updating existing key ---");
    let old = list.insert(10, "TEN (updated)".to_string());
    println!("Updated key 10, old value: {:?}", old);
    println!("get(10) now = {:?}", list.get(&10));

    // Check if key exists
    println!("\n--- Checking if keys exist ---");
    println!("contains_key(10) = {}", list.contains_key(&10));
    println!("contains_key(100) = {}", list.contains_key(&100));

    // Get first and last
    println!("\n--- First and last elements ---");
    println!("First: {:?}", list.first_key_value());
    println!("Last: {:?}", list.last_key_value());

    // Iterate over all elements (ordered)
    println!("\n--- Iteration (ordered) ---");
    println!("All elements in order:");
    for (key, value) in list.iter() {
        println!("  {}: {}", key, value);
    }

    // Iterate keys only
    println!("\n--- Keys only ---");
    println!("Keys: {:?}", list.keys().collect::<Vec<_>>());

    // Iterate values only
    println!("\n--- Values only ---");
    println!("Values: {:?}", list.values().collect::<Vec<_>>());

    // Remove a value
    println!("\n--- Removing values ---");
    let removed = list.remove(&15);
    println!("Removed key 15, value: {:?}", removed);
    println!("Length after removal: {}", list.len());
    println!("get(15) = {:?}", list.get(&15)); // Not found

    // Clear the list
    println!("\n--- Clearing the list ---");
    list.clear();
    println!("List cleared");
    println!("is_empty: {}", list.is_empty());
    println!("Length: {}", list.len());

    println!("\n=== Example Complete ===");
}