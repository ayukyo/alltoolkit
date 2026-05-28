//! Basic usage example for Red-Black Tree Utils

use red_black_tree_utils::RedBlackTree;

fn main() {
    println!("=== Red-Black Tree Basic Usage ===\n");
    
    // Create a new red-black tree
    let mut tree = RedBlackTree::new();
    
    // Insert values
    println!("Inserting values: 50, 25, 75, 10, 30, 60, 90");
    tree.insert(50);
    tree.insert(25);
    tree.insert(75);
    tree.insert(10);
    tree.insert(30);
    tree.insert(60);
    tree.insert(90);
    
    println!("Tree size: {}", tree.len());
    println!("Tree height: {}", tree.height());
    println!("Tree is valid RB tree: {}", tree.verify());
    
    // Color statistics
    let (red, black) = tree.color_stats();
    println!("Color stats: {} red nodes, {} black nodes", red, black);
    
    // Black height
    println!("Black height: {}", tree.black_height());
    
    // Min and Max
    println!("\nMin value: {:?}", tree.min());
    println!("Max value: {:?}", tree.max());
    
    // Search
    println!("\nContains 25? {}", tree.contains(&25));
    println!("Contains 100? {}", tree.contains(&100));
    
    // Traversals
    println!("\nIn-order (sorted): {:?}", tree.iter().collect::<Vec<_>>());
    println!("Pre-order: {:?}", tree.iter_pre_order().collect::<Vec<_>>());
    println!("Level-order: {:?}", tree.iter_level_order().collect::<Vec<_>>());
    
    // Range query
    println!("\nRange [20, 60]: {:?}", tree.range(&20, &60));
    
    // Predecessor and Successor
    println!("\nPredecessor of 50: {:?}", tree.predecessor(&50));
    println!("Successor of 50: {:?}", tree.successor(&50));
    
    // Remove
    println!("\nRemoving 50...");
    tree.remove(&50);
    println!("Tree size: {}", tree.len());
    println!("In-order: {:?}", tree.iter().collect::<Vec<_>>());
    println!("Tree still valid: {}", tree.verify());
    
    // Clear
    println!("\nClearing tree...");
    tree.clear();
    println!("Tree is empty: {}", tree.is_empty());
}