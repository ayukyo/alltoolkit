//! Consistent Hash Example
//! 
//! Demonstrates usage of the consistent hash ring for distributed systems.

use consistent_hash::ConsistentHash;

fn main() {
    println!("=== Consistent Hash Ring Demo ===\n");

    // Create a consistent hash ring with default settings
    let mut ring = ConsistentHash::<&str>::new();
    
    // Add nodes (servers) with virtual nodes for better distribution
    println!("Adding servers to the ring...");
    ring.add_node("server1.example.com", 150);
    ring.add_node("server2.example.com", 150);
    ring.add_node("server3.example.com", 150);
    
    println!("Ring statistics:");
    let stats = ring.stats();
    println!("  Physical nodes: {}", stats.node_count);
    println!("  Virtual nodes: {}", stats.virtual_node_count);
    println!("  Virtual nodes per physical node: {:.1}", stats.virtual_nodes_per_node);
    println!();

    // Route keys to servers
    println!("Routing keys to servers:");
    let keys = ["user:1001", "user:1002", "user:1003", "session:abc", "cache:item:xyz"];
    for key in &keys {
        if let Some(server) = ring.get(key) {
            println!("  '{}' -> {}", key, server);
        }
    }
    println!();

    // Add a new server
    println!("Adding server4.example.com...");
    ring.add_node("server4.example.com", 150);
    
    // Check distribution after adding server
    println!("\nChecking key distribution after adding server4:");
    let test_keys: Vec<_> = (0..1000).map(|i| format!("key{}", i)).collect();
    for key in &test_keys {
        // Keys are now distributed across 4 servers
        let _ = ring.get(key);
    }
    println!("  (Keys distributed across {} servers)", ring.node_count());
    println!();

    // Weighted nodes example
    println!("=== Weighted Nodes Demo ===\n");
    let mut weighted_ring = ConsistentHash::<&str>::new();
    
    // Add servers with different weights (capacity)
    weighted_ring.add_weighted("powerful-server", 3.0);  // 3x capacity
    weighted_ring.add_weighted("normal-server", 1.0);
    weighted_ring.add_weighted("small-server", 0.5);     // 0.5x capacity
    
    println!("Weighted ring statistics:");
    let wstats = weighted_ring.stats();
    println!("  Physical nodes: {}", wstats.node_count);
    println!("  Virtual nodes: {}", wstats.virtual_node_count);
    println!();

    // Distribution test
    let mut distribution: std::collections::HashMap<&str, i32> = std::collections::HashMap::new();
    for i in 0..10000 {
        let key = format!("key{}", i);
        if let Some(server) = weighted_ring.get(&key) {
            *distribution.entry(server).or_insert(0) += 1;
        }
    }
    
    println!("Key distribution (10000 keys):");
    for (server, count) in &distribution {
        let percentage = (*count as f64 / 10000.0) * 100.0;
        println!("  {}: {} keys ({:.1}%)", server, count, percentage);
    }
    println!();

    // Replication example - get N nodes for a key
    println!("=== Replication Demo ===\n");
    let mut repl_ring = ConsistentHash::<&str>::new();
    repl_ring.add_node("db-primary", 100);
    repl_ring.add_node("db-replica1", 100);
    repl_ring.add_node("db-replica2", 100);
    repl_ring.add_node("db-replica3", 100);
    
    let key = "user:12345";
    let replicas = repl_ring.get_n(key, 3);
    println!("Replica nodes for key '{}':", key);
    for (i, node) in replicas.iter().enumerate() {
        println!("  Replica {}: {}", i + 1, node);
    }

    println!("\n=== Demo Complete ===");
}