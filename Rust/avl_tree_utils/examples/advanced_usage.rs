//! Advanced usage examples for AVL Tree Utils
//! 
//! Demonstrates:
//! - Using custom types
//! - Performance with large datasets
//! - Database-like operations

use avl_tree_utils::AVLTree;
use std::cmp::Ordering;

/// A record representing a person with age
#[derive(Debug, Clone)]
struct Person {
    id: u32,
    name: String,
    age: u32,
}

impl Person {
    fn new(id: u32, name: &str, age: u32) -> Self {
        Person {
            id,
            name: name.to_string(),
            age,
        }
    }
}

impl PartialEq for Person {
    fn eq(&self, other: &Self) -> bool {
        self.id == other.id
    }
}

impl Eq for Person {}

impl PartialOrd for Person {
    fn partial_cmp(&self, other: &Self) -> Option<Ordering> {
        Some(self.cmp(other))
    }
}

impl Ord for Person {
    fn cmp(&self, other: &Self) -> Ordering {
        // Sort by age first, then by id for uniqueness
        self.age.cmp(&other.age)
            .then_with(|| self.id.cmp(&other.id))
    }
}

fn main() {
    println!("=== AVL Tree Advanced Usage ===\n");
    
    // Example 1: Custom types
    println!("--- Example 1: Custom Types (Person by age) ---");
    let mut people: AVLTree<Person> = AVLTree::new();
    
    people.insert(Person::new(1, "Alice", 30));
    people.insert(Person::new(2, "Bob", 25));
    people.insert(Person::new(3, "Charlie", 35));
    people.insert(Person::new(4, "Diana", 25)); // Same age as Bob, different id
    people.insert(Person::new(5, "Eve", 40));
    
    println!("People sorted by age:");
    for person in people.iter() {
        println!("  {} (age {}, id {})", person.name, person.age, person.id);
    }
    
    // Example 2: Using as a sorted set
    println!("\n--- Example 2: Using as a Sorted Set ---");
    let mut sorted_set: AVLTree<i32> = AVLTree::new();
    
    // Insert random order
    let values = vec![5, 2, 8, 1, 9, 3, 7, 4, 6];
    for v in &values {
        sorted_set.insert(*v);
    }
    
    println!("Original: {:?}", values);
    println!("Sorted (in-order traversal): {:?}", sorted_set.iter().collect::<Vec<_>>());
    
    // Example 3: Range-based filtering
    println!("\n--- Example 3: Range Filtering ---");
    let mut numbers: AVLTree<i32> = AVLTree::new();
    for i in 1..=100 {
        numbers.insert(i);
    }
    
    let teens = numbers.range(&13, &19);
    println!("Teen numbers (13-19): {:?}", teens);
    
    let multiples_of_25: Vec<_> = numbers.iter()
        .filter(|&&n| n % 25 == 0)
        .collect();
    println!("Multiples of 25: {:?}", multiples_of_25);
    
    // Example 4: Performance with large dataset
    println!("\n--- Example 4: Performance Test ---");
    let mut large_tree: AVLTree<i32> = AVLTree::new();
    
    // Insert 10,000 elements in sorted order (worst case for regular BST)
    let start = std::time::Instant::now();
    for i in 0..10_000 {
        large_tree.insert(i);
    }
    let insert_time = start.elapsed();
    
    println!("Inserted 10,000 elements in {:?}", insert_time);
    println!("Tree height: {} (log2(10000) ≈ 13.3)", large_tree.height());
    println!("Tree is valid: {}", large_tree.verify());
    
    // Search performance
    let start = std::time::Instant::now();
    let found = large_tree.contains(&5000);
    let search_time = start.elapsed();
    println!("Search for 5000: found={}, time={:?}", found, search_time);
    
    // Example 5: Database-like operations (using cents for price, since f64 doesn't impl Ord)
    println!("\n--- Example 5: Database-like Operations ---");
    let mut product_prices: AVLTree<(String, u32)> = AVLTree::new(); // price in cents
    
    // Products with prices (sorted by tuple comparison: name first, then price)
    product_prices.insert(("Apple".to_string(), 199));  // $1.99
    product_prices.insert(("Banana".to_string(), 99));   // $0.99
    product_prices.insert(("Cherry".to_string(), 299));  // $2.99
    product_prices.insert(("Date".to_string(), 399));    // $3.99
    product_prices.insert(("Elderberry".to_string(), 499)); // $4.99
    
    println!("Products sorted by name:");
    for (name, price_cents) in product_prices.iter() {
        println!("  {}: ${:.2}", name, *price_cents as f64 / 100.0);
    }
    
    // Example 6: Set operations simulation
    println!("\n--- Example 6: Set Operations ---");
    let set1: AVLTree<i32> = vec![1, 2, 3, 4, 5].into_iter().collect();
    let set2: AVLTree<i32> = vec![4, 5, 6, 7, 8].into_iter().collect();
    
    // Union
    let mut union: AVLTree<i32> = AVLTree::new();
    for &v in set1.iter() {
        union.insert(v);
    }
    for &v in set2.iter() {
        union.insert(v);
    }
    println!("Union: {:?}", union.iter().collect::<Vec<_>>());
    
    // Intersection
    let intersection: Vec<_> = set1.iter()
        .filter(|v| set2.contains(v))
        .collect();
    println!("Intersection: {:?}", intersection);
    
    // Difference
    let difference: Vec<_> = set1.iter()
        .filter(|v| !set2.contains(v))
        .collect();
    println!("Set1 - Set2: {:?}", difference);
    
    // Example 7: Building from iterator
    println!("\n--- Example 7: From Iterator ---");
    let tree: AVLTree<i32> = (1..=5).collect();
    println!("Tree from 1..=5: {:?}", tree.iter().collect::<Vec<_>>());
    
    println!("\n=== All examples completed! ===");
}