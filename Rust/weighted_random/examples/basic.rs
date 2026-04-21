//! Basic usage example for weighted_random
//!
//! Run with: cargo run --example basic

use weighted_random::{Selector, WeightedItem, SelectorBuilder};

fn main() {
    println!("=== Weighted Random Selector - Basic Examples ===\n");

    // Example 1: Creating a selector with WeightedItem
    example_weighted_items();

    // Example 2: Using the builder pattern
    example_builder();

    // Example 3: Uniform selection from slice
    example_from_slice();

    // Example 4: Select multiple items
    example_select_n();

    // Example 5: Unique selection
    example_select_unique();

    // Example 6: Statistical distribution
    example_distribution();
}

fn example_weighted_items() {
    println!("--- Example 1: Weighted Items ---");

    let items = vec![
        WeightedItem::new("common", 70.0),
        WeightedItem::new("rare", 20.0),
        WeightedItem::new("epic", 8.0),
        WeightedItem::new("legendary", 2.0),
    ];

    let selector = Selector::new(items).unwrap();

    println!("Selector info:");
    println!("  Items: {}", selector.len());
    println!("  Total weight: {}", selector.total_weight());

    println!("\nSelecting 10 items:");
    for _ in 0..10 {
        println!("  Selected: {}", selector.select());
    }
    println!();
}

fn example_builder() {
    println!("--- Example 2: Builder Pattern ---");

    let selector = SelectorBuilder::new()
        .add("low", 10.0)
        .add("medium", 30.0)
        .add("high", 60.0)
        .build()
        .unwrap();

    println!("Built selector with {} items", selector.len());
    println!("  Total weight: {}", selector.total_weight());

    println!("\nSelecting 5 items:");
    for _ in 0..5 {
        println!("  {}", selector.select());
    }
    println!();
}

fn example_from_slice() {
    println!("--- Example 3: Uniform Selection ---");

    let items = vec!["apple", "banana", "cherry", "date"];
    let selector = Selector::from_slice(&items).unwrap();

    println!("Uniform selector with {} items", selector.len());

    println!("\nRandom selections (equal probability):");
    for _ in 0..4 {
        println!("  {}", selector.select());
    }
    println!();
}

fn example_select_n() {
    println!("--- Example 4: Select N Items ---");

    let items = vec![
        WeightedItem::new(1, 10.0),
        WeightedItem::new(2, 20.0),
        WeightedItem::new(3, 30.0),
    ];

    let selector = Selector::new(items).unwrap();

    println!("Selecting 10 items in one call:");
    let selected = selector.select_n_cloned(10);
    for item in selected {
        println!("  {}", item);
    }
    println!();
}

fn example_select_unique() {
    println!("--- Example 5: Unique Selection ---");

    let items = vec![
        WeightedItem::new("Alice", 30.0),
        WeightedItem::new("Bob", 20.0),
        WeightedItem::new("Charlie", 10.0),
        WeightedItem::new("Diana", 40.0),
    ];

    let selector = Selector::new(items).unwrap();

    println!("Selecting 3 unique winners:");
    let winners = selector.select_unique_cloned(3).unwrap();

    for (i, winner) in winners.iter().enumerate() {
        println!("  {}. {}", i + 1, winner);
    }
    println!();
}

fn example_distribution() {
    println!("--- Example 6: Statistical Distribution ---");

    let items = vec![
        WeightedItem::new("a", 1.0),
        WeightedItem::new("b", 2.0),
        WeightedItem::new("c", 3.0),
        WeightedItem::new("d", 4.0),
    ];

    let selector = Selector::new(items).unwrap();

    // Run many selections and count occurrences
    let mut counts: std::collections::HashMap<&str, usize> = std::collections::HashMap::new();
    let iterations = 100_000;

    for _ in 0..iterations {
        let item = selector.select();
        *counts.entry(item).or_insert(0) += 1;
    }

    println!("Distribution over {} iterations:", iterations);
    let expected = [("a", 0.1), ("b", 0.2), ("c", 0.3), ("d", 0.4)];

    for (item, exp_prob) in expected {
        let count = counts.get(item).unwrap_or(&0);
        let actual_prob = *count as f64 / iterations as f64;
        println!("  {}: expected {:.1}% (~{}), actual {:.2}% ({})", 
                 item, exp_prob * 100.0, (exp_prob * iterations as f64) as usize,
                 actual_prob * 100.0, count);
    }
    println!();
}