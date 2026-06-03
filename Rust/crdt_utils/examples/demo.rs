//! CRDT Utilities - Example Usage
//!
//! Demonstrates the conflict-free replicated data types for distributed systems.

use crdt_utils::{
    GCounter, PNCounter, TwoPhaseSet, ORSet, LWWRegister, RGA, VectorClock,
};

fn main() {
    println!("=== CRDT Utilities Demo ===\n");

    // ------------------------------------------------------------
    // G-Counter: Distributed vote counting
    // ------------------------------------------------------------
    println!("--- G-Counter (Distributed Vote Counter) ---");

    let mut replica_a = GCounter::new("A".to_string());
    let mut replica_b = GCounter::new("B".to_string());
    let mut replica_c = GCounter::new("C".to_string());

    // Replica A gets 5 votes
    replica_a.increment(5);
    // Replica B gets 3 votes
    replica_b.increment(3);
    // Replica C gets 2 votes
    replica_c.increment(2);

    // Merge all replicas
    replica_a.merge(&replica_b);
    replica_a.merge(&replica_c);

    println!("Total votes: {} (expected: 10)", replica_a.value());

    // ------------------------------------------------------------
    // PN-Counter: Distributed account balance
    // ------------------------------------------------------------
    println!("\n--- PN-Counter (Account Balance) ---");

    let mut account_1 = PNCounter::new("node1".to_string());
    let mut account_2 = PNCounter::new("node2".to_string());

    account_1.increment(1000);  // Deposit $1000
    account_1.decrement(300);   // Withdraw $300

    account_2.increment(500);   // Deposit $500
    account_2.decrement(100);   // Withdraw $100

    account_1.merge(&account_2);

    println!("Final balance: ${} (expected: $1100)", account_1.value());

    // ------------------------------------------------------------
    // 2P-Set: Collaborative document tags
    // ------------------------------------------------------------
    println!("\n--- 2P-Set (Document Tags) ---");

    let mut tags_alice = TwoPhaseSet::new();
    let mut tags_bob = TwoPhaseSet::new();

    tags_alice.add("rust".to_string());
    tags_alice.add("systems".to_string());

    tags_bob.add("distributed".to_string());
    tags_bob.add("rust".to_string()); // Duplicate attempt - should be ignored
    tags_bob.remove("systems");

    tags_alice.merge(&tags_bob);

    println!("Final tags: {:?}", tags_alice.elements());
    println!("Has 'rust': {}", tags_alice.contains("rust"));
    println!("Has 'systems': {}", tags_alice.contains("systems"));
    println!("Has 'distributed': {}", tags_alice.contains("distributed"));

    // ------------------------------------------------------------
    // OR-Set: Collaborative cart
    // ------------------------------------------------------------
    println!("\n--- OR-Set (Shopping Cart) ---");

    let mut cart_alice = ORSet::new();
    let mut cart_bob = ORSet::new();

    cart_alice.add("laptop".to_string());
    cart_alice.add("mouse".to_string());

    cart_bob.add("keyboard".to_string());
    cart_bob.add("laptop".to_string()); // Second add with different tag

    cart_alice.merge(&cart_bob);
    println!("Alice's cart after merge: {:?}", cart_alice.elements());

    // Alice removes laptop
    cart_alice.remove("laptop");
    println!("After removing 'laptop': {:?}", cart_alice.elements());

    // ------------------------------------------------------------
    // LWW-Register: Distributed config
    // ------------------------------------------------------------
    println!("\n--- LWW-Register (Config Value) ---");

    let mut config_replica_1 = LWWRegister::new();
    let mut config_replica_2 = LWWRegister::new();

    config_replica_1.set("version: 1.0".to_string());
    config_replica_2.set("version: 2.0".to_string());

    // Merge: replica_2's value wins (higher clock)
    config_replica_1.merge(&config_replica_2);
    println!("Winning config: {}", config_replica_1.get().unwrap());

    // ------------------------------------------------------------
    // RGA: Collaborative text editing
    // ------------------------------------------------------------
    println!("\n--- RGA (Collaborative Text Editor) ---");

    let mut doc_alice = RGA::new();
    let mut doc_bob = RGA::new();

    // Alice types "hello"
    let mut doc_alice = RGA::new();
    doc_alice.insert('h', None);
    doc_alice.insert('e', Some(1));
    doc_alice.insert('l', Some(2));
    doc_alice.insert('l', Some(3));
    doc_alice.insert('o', Some(4));

    // Bob types " world" (simulated)
    let mut doc_bob = RGA::new();
    doc_bob.insert(' ', None);
    doc_bob.insert('w', Some(5));
    doc_bob.insert('o', Some(6));
    doc_bob.insert('r', Some(7));
    doc_bob.insert('l', Some(8));
    doc_bob.insert('d', Some(9));

    doc_alice.merge(&doc_bob);
    println!("Merged document: '{}'", doc_alice.content());

    // Alice deletes 'o' and 'l'
    doc_alice.delete(5);
    doc_alice.delete(3);
    println!("After deletes: '{}'", doc_alice.content());

    // ------------------------------------------------------------
    // VectorClock: Causality tracking
    // ------------------------------------------------------------
    println!("\n--- VectorClock (Causality Tracking) ---");

    let mut clock_alice = VectorClock::new("Alice");
    let mut clock_bob = VectorClock::new("Bob");

    clock_alice.tick("Alice");
    clock_alice.tick("Alice"); // Alice: {A: 2}

    clock_bob.tick("Bob");
    clock_bob.tick("Bob");
    clock_bob.tick("Bob"); // Bob: {B: 3}

    // Merge clocks
    clock_alice.merge(&clock_bob);
    println!("Alice's merged clock: A={}, B={}",
             clock_alice.get("Alice"),
             clock_alice.get("Bob"));

    println!("\n=== Demo Complete ===");
}
