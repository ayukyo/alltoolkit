//! Leaderboard application example

use skiplist::IndexedSkipList;
use std::collections::HashMap;

fn main() {
    println!("=== Leaderboard Application Example ===\n");

    // Game leaderboard - higher score = better rank
    // Using negative scores so higher scores come first
    let mut leaderboard: IndexedSkipList<i64, String> = IndexedSkipList::new();
    
    // Player name -> score mapping (for updates)
    let mut player_scores: HashMap<String, i64> = HashMap::new();

    // Initial players
    println!("--- Adding initial players ---");
    let players = [
        ("Alice", 1500),
        ("Bob", 1200),
        ("Charlie", 1800),
        ("Diana", 2000),
        ("Eve", 900),
        ("Frank", 1600),
        ("Grace", 1400),
        ("Henry", 1000),
    ];

    for (name, score) in players {
        player_scores.insert(name.to_string(), score);
        leaderboard.insert(-score, name.to_string());
        println!("  {} joined with score {}", name, score);
    }

    // Display leaderboard
    println!("\n--- Current Leaderboard ---");
    println!("Rank | Player   | Score");
    println!("-----|----------|-------");
    for rank in 0..leaderboard.len() {
        if let Some((score, name)) = leaderboard.get_by_rank(rank) {
            println!("{:4} | {:8} | {}", rank + 1, name, -score);
        }
    }

    // Find player's rank
    println!("\n--- Player Rankings ---");
    for (name, score) in &player_scores {
        if let Some(rank) = leaderboard.rank_of(&-*score) {
            println!("{} is ranked #{}", name, rank + 1);
        }
    }

    // Score updates (create new leaderboard to simulate)
    println!("\n--- Score Updates (creating new leaderboard) ---");
    
    // Update scores in the map
    *player_scores.get_mut("Alice").unwrap() += 100; // Alice: 1500 -> 1600
    *player_scores.get_mut("Bob").unwrap() -= 50;    // Bob: 1200 -> 1150
    
    // New player joins
    player_scores.insert("Ivy".to_string(), 1700);
    
    // Rebuild leaderboard with updated scores
    let mut new_leaderboard: IndexedSkipList<i64, String> = IndexedSkipList::new();
    for (name, score) in &player_scores {
        new_leaderboard.insert(-score, name.clone());
    }

    println!("Alice gained 100 points: 1500 -> 1600");
    println!("Bob lost 50 points: 1200 -> 1150");
    println!("Ivy joined with score 1700");

    // Updated leaderboard
    println!("\n--- Updated Leaderboard ---");
    println!("Rank | Player   | Score");
    println!("-----|----------|-------");
    for rank in 0..new_leaderboard.len() {
        if let Some((score, name)) = new_leaderboard.get_by_rank(rank) {
            println!("{:4} | {:8} | {}", rank + 1, name, -score);
        }
    }

    // Top 3 players
    println!("\n--- Top 3 Players ---");
    for rank in 0..3 {
        if let Some((score, name)) = new_leaderboard.get_by_rank(rank) {
            println!("{}. {} (score: {})", rank + 1, name, -score);
        }
    }

    // Players in score range
    println!("\n--- Players with scores between 1400-1700 ---");
    let count = new_leaderboard.count_less_than(&-1700) 
        + new_leaderboard.count_greater_than(&-1400);
    let in_range = new_leaderboard.len() - count;
    println!("Count: {}", in_range);

    // Statistics
    println!("\n--- Statistics ---");
    if let Some((min_score, min_name)) = new_leaderboard.last() {
        println!("Lowest score: {} ({})", min_name, -min_score);
    }
    if let Some((max_score, max_name)) = new_leaderboard.first() {
        println!("Highest score: {} ({})", max_name, -max_score);
    }

    println!("\n=== Example Complete ===");
}