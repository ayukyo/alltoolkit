//! Indexed SkipList rank queries example

use skiplist::IndexedSkipList;

fn main() {
    println!("=== Indexed SkipList Rank Queries Example ===\n");

    // Create indexed skip list
    let mut list: IndexedSkipList<i32, String> = IndexedSkipList::new();

    // Insert values (will be automatically sorted)
    println!("--- Inserting values ---");
    list.insert(100, "one hundred".to_string());
    list.insert(10, "ten".to_string());
    list.insert(50, "fifty".to_string());
    list.insert(30, "thirty".to_string());
    list.insert(70, "seventy".to_string());
    list.insert(20, "twenty".to_string());
    list.insert(80, "eighty".to_string());
    list.insert(40, "forty".to_string());
    list.insert(60, "sixty".to_string());
    list.insert(90, "ninety".to_string());

    println!("Inserted 10 values (10, 20, 30, ..., 100)");
    println!("Length: {}", list.len());

    // Show sorted order
    println!("\n--- Elements in sorted order ---");
    for (k, v) in list.iter() {
        println!("  {}: {}", k, v);
    }

    // Get by rank
    println!("\n--- Get elements by rank ---");
    println!("get_by_rank(0) = {:?}", list.get_by_rank(0));
    println!("get_by_rank(4) = {:?}", list.get_by_rank(4));
    println!("get_by_rank(9) = {:?}", list.get_by_rank(9));
    println!("get_by_rank(10) = {:?}", list.get_by_rank(10)); // Out of bounds

    // Get rank of keys
    println!("\n--- Get rank of specific keys ---");
    println!("rank_of(10) = {:?}", list.rank_of(&10));
    println!("rank_of(50) = {:?}", list.rank_of(&50));
    println!("rank_of(100) = {:?}", list.rank_of(&100));
    println!("rank_of(55) = {:?}", list.rank_of(&55)); // Not in list

    // Count operations
    println!("\n--- Count operations ---");
    println!("count_less_than(50) = {} (elements less than 50)", list.count_less_than(&50));
    println!("count_less_than(60) = {}", list.count_less_than(&60));
    println!("count_greater_than(50) = {} (elements greater than 50)", list.count_greater_than(&50));
    println!("count_greater_than(50) + count_less_than(50) + contains(50) = {}",
        list.count_greater_than(&50) + list.count_less_than(&50) + if list.contains_key(&50) { 1 } else { 0 });

    // First and last
    println!("\n--- First and last ---");
    println!("First: {:?}", list.first());
    println!("Last: {:?}", list.last());

    // Leaderboard simulation
    println!("\n=== Simulating a Leaderboard ===");
    let mut leaderboard: IndexedSkipList<i64, String> = IndexedSkipList::new();
    
    // Insert scores (higher score = better rank)
    // Using negative scores to reverse order (highest score = rank 0)
    leaderboard.insert(-1000, "Player A".to_string());
    leaderboard.insert(-850, "Player B".to_string());
    leaderboard.insert(-900, "Player C".to_string());
    leaderboard.insert(-1100, "Player D".to_string());
    leaderboard.insert(-800, "Player E".to_string());

    println!("Leaderboard (highest score first):");
    for i in 0..leaderboard.len() {
        if let Some((score, name)) = leaderboard.get_by_rank(i) {
            println!("  Rank {}: {} (score: {})", i + 1, name, -score);
        }
    }

    println!("\nFind Player C's rank:");
    if let Some(rank) = leaderboard.rank_of(&-900) {
        println!("  Player C is at rank {}", rank + 1);
    }

    println!("\n=== Example Complete ===");
}