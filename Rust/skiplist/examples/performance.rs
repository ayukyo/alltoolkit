//! Performance benchmark example

use skiplist::{IndexedSkipList, SkipList, SkipListConfig};
use std::time::Instant;

fn main() {
    println!("=== SkipList Performance Benchmark ===\n");

    let sizes = [1000, 10_000, 100_000];
    
    for size in sizes {
        println!("\n--- Testing with {} elements ---", size);

        // Insert benchmark
        let mut list: SkipList<i32, i32> = SkipList::with_capacity(size);
        let start = Instant::now();
        
        for i in 0..size {
            list.insert(i as i32, i as i32);
        }
        
        let insert_time = start.elapsed();
        println!("Insert: {:?}", insert_time);
        println!("  Per element: {:?}", insert_time / size as u32);

        // Get benchmark
        let start = Instant::now();
        
        let mut found = 0;
        for i in 0..size {
            if list.get(&(i as i32)).is_some() {
                found += 1;
            }
        }
        
        let get_time = start.elapsed();
        println!("Get (all): {:?}", get_time);
        println!("  Per element: {:?}", get_time / size as u32);
        println!("  Found: {} elements", found);

        // Remove benchmark
        let start = Instant::now();
        
        for i in 0..size / 2 {
            list.remove(&(i as i32));
        }
        
        let remove_time = start.elapsed();
        println!("Remove (half): {:?}", remove_time);
        println!("  Per element: {:?}", remove_time / (size / 2) as u32);
        println!("  Remaining: {} elements", list.len());

        // Iteration benchmark
        let start = Instant::now();
        
        let count = list.iter().count();
        
        let iter_time = start.elapsed();
        println!("Iterate: {:?}", iter_time);
        println!("  Counted: {} elements", count);
    }

    // IndexedSkipList performance
    println!("\n\n=== IndexedSkipList Performance ===\n");
    
    let size = 10_000;
    let mut indexed_list: IndexedSkipList<i32, i32> = IndexedSkipList::new();

    println!("--- Testing IndexedSkipList with {} elements ---", size);

    // Insert
    let start = Instant::now();
    for i in 0..size {
        indexed_list.insert(i as i32, i as i32);
    }
    let insert_time = start.elapsed();
    println!("Insert: {:?}", insert_time);

    // Get by rank
    let start = Instant::now();
    let mut sum = 0;
    for i in 0..size {
        if let Some((_, v)) = indexed_list.get_by_rank(i) {
            sum += v;
        }
    }
    let rank_time = start.elapsed();
    println!("Get by rank (all): {:?}", rank_time);
    println!("  Sum verification: {}", sum);

    // Get rank of
    let start = Instant::now();
    for i in 0..size {
        indexed_list.rank_of(&(i as i32));
    }
    let rank_of_time = start.elapsed();
    println!("Rank of (all): {:?}", rank_of_time);

    // Count less than
    let start = Instant::now();
    for i in (0..size).step_by(100) {
        indexed_list.count_less_than(&(i as i32));
    }
    let count_time = start.elapsed();
    println!("Count less than ({} queries): {:?}", size / 100, count_time);

    // Configuration impact
    println!("\n\n=== Configuration Impact ===\n");
    
    let configs = [
        ("Default (p=0.25, level=16)", SkipListConfig::default()),
        ("Low probability (p=0.1, level=16)", SkipListConfig::new(0.1, 16)),
        ("High probability (p=0.5, level=16)", SkipListConfig::new(0.5, 16)),
        ("Small max level (p=0.25, level=8)", SkipListConfig::new(0.25, 8)),
        ("Large max level (p=0.25, level=32)", SkipListConfig::new(0.25, 32)),
    ];

    let size = 10_000;

    for (name, config) in configs {
        println!("\n{}", name);
        
        let mut list: SkipList<i32, i32> = SkipList::with_config(config);
        
        let start = Instant::now();
        for i in 0..size {
            list.insert(i as i32, i as i32);
        }
        let insert_time = start.elapsed();
        
        let start = Instant::now();
        for i in 0..size {
            list.get(&(i as i32));
        }
        let get_time = start.elapsed();
        
        println!("  Insert: {:?}", insert_time);
        println!("  Get: {:?}", get_time);
        println!("  Expected overhead: {:.2}x", config.expected_overhead());
    }

    println!("\n=== Benchmark Complete ===");
}