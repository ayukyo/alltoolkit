//! Advanced usage example for Red-Black Tree Utils

use red_black_tree_utils::RedBlackTree;
use std::cmp::Ordering;

#[derive(Debug, Clone, Eq, PartialEq)]
struct Person {
    id: u32,
    name: String,
    age: u32,
}

impl Ord for Person {
    fn cmp(&self, other: &Self) -> Ordering {
        self.age.cmp(&other.age)
            .then_with(|| self.id.cmp(&other.id))
    }
}

impl PartialOrd for Person {
    fn partial_cmp(&self, other: &Self) -> Option<Ordering> {
        Some(self.cmp(other))
    }
}

fn main() {
    println!("=== Red-Black Tree Advanced Usage ===\n");
    
    // Example 1: Large scale operations
    println!("--- Large Scale Operations ---");
    let mut tree = RedBlackTree::new();
    
    // Insert 10,000 elements
    for i in 0..10_000 {
        tree.insert(i);
    }
    
    println!("Inserted 10,000 elements");
    println!("Tree size: {}", tree.len());
    println!("Tree height: {} (theoretical min: ~14)", tree.height());
    println!("Black height: {}", tree.black_height());
    println!("Tree is valid: {}", tree.verify());
    
    // Remove half the elements
    for i in (0..10_000).step_by(2) {
        tree.remove(&i);
    }
    
    println!("\nRemoved 5,000 elements (even numbers)");
    println!("Tree size: {}", tree.len());
    println!("Tree still valid: {}", tree.verify());
    
    // Example 2: Sequential vs Random Insertions
    println!("\n--- Sequential vs Random Insertions ---");
    
    // Sequential (worst case for BST)
    let mut seq_tree = RedBlackTree::new();
    for i in 0..1_000 {
        seq_tree.insert(i);
    }
    println!("Sequential insert height: {}", seq_tree.height());
    
    // Random order (better case for BST)
    let mut rand_tree = RedBlackTree::new();
    let mut values: Vec<i32> = (0..1_000).collect();
    // Simple shuffle simulation using deterministic pattern
    for i in 0..1_000 {
        let idx = (i * 7 + 3) % 1_000;
        rand_tree.insert(values[idx % values.len()]);
    }
    println!("Shuffled insert height: {}", rand_tree.height());
    
    // Example 3: Custom Types
    println!("\n--- Custom Types (People sorted by age) ---");
    
    let mut people: RedBlackTree<Person> = RedBlackTree::new();
    people.insert(Person { id: 1, name: "Alice".into(), age: 30 });
    people.insert(Person { id: 2, name: "Bob".into(), age: 25 });
    people.insert(Person { id: 3, name: "Charlie".into(), age: 35 });
    people.insert(Person { id: 4, name: "Diana".into(), age: 28 });
    
    println!("Youngest: {:?}", people.min());
    println!("Oldest: {:?}", people.max());
    
    // Range query: people aged 26-32
    let range = people.range(
        &Person { id: 0, name: "".into(), age: 26 },
        &Person { id: u32::MAX, name: "".into(), age: 32 }
    );
    println!("People aged 26-32: {:?}", range);
    
    // Example 4: Stress Test
    println!("\n--- Stress Test ---");
    
    let mut stress_tree = RedBlackTree::new();
    
    // Insert 100,000 elements
    for i in 0..100_000 {
        stress_tree.insert(i);
    }
    
    println!("Inserted 100,000 elements");
    println!("Height: {} (should be < 35)", stress_tree.height());
    
    // Verify all elements exist
    let mut found = 0;
    for i in 0..100_000 {
        if stress_tree.contains(&i) {
            found += 1;
        }
    }
    println!("All elements found: {}", found == 100_000);
    
    // Remove 50,000 elements and verify tree validity
    for i in (0..100_000).step_by(2) {
        stress_tree.remove(&i);
    }
    
    println!("After removing 50,000 elements:");
    println!("Size: {}", stress_tree.len());
    println!("Tree valid: {}", stress_tree.verify());
    
    // Example 5: Color Distribution Analysis
    println!("\n--- Color Distribution Analysis ---");
    
    let mut analysis_tree = RedBlackTree::new();
    for i in 1..=100 {
        analysis_tree.insert(i);
    }
    
    let (red, black) = analysis_tree.color_stats();
    let total = red + black;
    let red_ratio = red as f64 / total as f64;
    
    println!("Total nodes: {}", total);
    println!("Red nodes: {} ({:.1}%)", red, red_ratio * 100.0);
    println!("Black nodes: {} ({:.1}%)", black, (1.0 - red_ratio) * 100.0);
    println!("Red:Black ratio: {:.2}:1", red as f64 / black as f64);
    
    // Example 6: From Iterator
    println!("\n--- From Iterator ---");
    
    let tree: RedBlackTree<i32> = vec![5, 3, 7, 1, 9, 2, 8, 4, 6].into_iter().collect();
    println!("Created from vector: {:?}", tree.iter().collect::<Vec<_>>());
    println!("Sorted order: {:?}", tree.iter().collect::<Vec<_>>());
}