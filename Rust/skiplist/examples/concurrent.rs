//! Concurrent SkipList example

use skiplist::ConcurrentSkipList;
use std::sync::Arc;
use std::thread;
use std::time::Duration;

fn main() {
    println!("=== Concurrent SkipList Example ===\n");

    // Create a concurrent skip list
    let list = Arc::new(ConcurrentSkipList::<i32, String>::new());
    
    println!("Created concurrent skip list");

    // Spawn writer threads
    println!("\n--- Spawning writer threads ---");
    let mut handles = vec![];

    for thread_id in 0..4 {
        let list_clone = Arc::clone(&list);
        handles.push(thread::spawn(move || {
            for i in 0..25 {
                let key = thread_id * 100 + i;
                list_clone.insert(key, format!("Thread {} - Item {}", thread_id, i));
                println!("  [Thread {}] Inserted key {}", thread_id, key);
                thread::sleep(Duration::from_millis(10));
            }
        }));
    }

    // Wait for all writers
    for handle in handles {
        handle.join().unwrap();
    }

    println!("\n--- After all writes ---");
    println!("Total elements: {}", list.len());

    // Spawn reader threads
    println!("\n--- Spawning reader threads ---");
    let mut reader_handles = vec![];

    for thread_id in 0..4 {
        let list_clone = Arc::clone(&list);
        reader_handles.push(thread::spawn(move || {
            let mut found = 0;
            for i in 0..25 {
                let key = thread_id * 100 + i;
                if list_clone.contains_key(&key) {
                    found += 1;
                }
            }
            println!("  [Reader {}] Found {} keys", thread_id, found);
        }));
    }

    for handle in reader_handles {
        handle.join().unwrap();
    }

    // Get first and last
    println!("\n--- First and last elements ---");
    if let Some((k, v)) = list.first_key_value() {
        println!("First: {} -> {}", k, v);
    }
    if let Some((k, v)) = list.last_key_value() {
        println!("Last: {} -> {}", k, v);
    }

    // Convert to vector
    println!("\n--- All elements (sorted) ---");
    let vec = list.to_vec();
    println!("Total: {} elements", vec.len());
    for (k, v) in vec.iter().take(10) {
        println!("  {} -> {}", k, v);
    }
    println!("  ... ({} more)", vec.len() - 10);

    // Concurrent modifications
    println!("\n--- Concurrent modifications ---");
    
    // Remove some elements from multiple threads
    let mut remove_handles = vec![];
    for thread_id in 0..4 {
        let list_clone = Arc::clone(&list);
        remove_handles.push(thread::spawn(move || {
            let mut removed = 0;
            for i in 0..5 {
                let key = thread_id * 100 + i;
                if list_clone.remove(&key).is_some() {
                    removed += 1;
                }
            }
            println!("  [Remover {}] Removed {} keys", thread_id, removed);
        }));
    }

    for handle in remove_handles {
        handle.join().unwrap();
    }

    println!("\n--- After removals ---");
    println!("Remaining elements: {}", list.len());

    // Clear from multiple threads would race, so we do it once
    println!("\n--- Clearing ---");
    list.clear();
    println!("List cleared");
    println!("is_empty: {}", list.is_empty());

    println!("\n=== Example Complete ===");
}