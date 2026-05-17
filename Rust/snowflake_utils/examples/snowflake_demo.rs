/// Snowflake ID Generator Examples
/// 
/// Run with: cargo run --example snowflake_demo

use snowflake_utils::{SnowflakeGenerator, SnowflakeId, DEFAULT_EPOCH};

fn main() {
    println!("=== Snowflake ID Generator Demo ===\n");
    
    // Create a generator with node ID 1
    let generator = SnowflakeGenerator::new(1, DEFAULT_EPOCH);
    println!("Generator created with node_id: {}, epoch: {}", 
             generator.node_id(), generator.epoch());
    
    // Generate a single ID
    println!("\n--- Single ID Generation ---");
    let id = generator.generate();
    println!("Generated ID: {}", id);
    println!("ID (hex): {:016x}", id);
    
    // Parse the ID
    let (timestamp, node_id, sequence) = generator.parse_id(id);
    println!("Parsed components:");
    println!("  Timestamp: {} ms since epoch", timestamp);
    println!("  Node ID: {}", node_id);
    println!("  Sequence: {}", sequence);
    
    // Using SnowflakeId helper
    println!("\n--- Using SnowflakeId Helper ---");
    let sf_id = SnowflakeId::new(id);
    println!("ID: {}", sf_id);
    println!("Debug: {:?}", sf_id);
    println!("Hex: {}", sf_id.to_hex());
    println!("Node ID: {}", sf_id.node_id_component());
    println!("Sequence: {}", sf_id.sequence_component());
    
    // Parse with epoch for human-readable timestamp
    let parsed = sf_id.parse_with_epoch(DEFAULT_EPOCH);
    println!("\nParsed with epoch:");
    println!("  ID: {}", parsed.id);
    println!("  Timestamp (ms): {}", parsed.timestamp_ms);
    println!("  Timestamp (s): {:.3}", parsed.as_secs());
    println!("  Node ID: {}", parsed.node_id);
    println!("  Sequence: {}", parsed.sequence);
    
    // Generate multiple IDs
    println!("\n--- Batch ID Generation ---");
    let batch = generator.generate_batch(10);
    println!("Generated {} IDs:", batch.len());
    for (i, &id) in batch.iter().enumerate() {
        let sf = SnowflakeId::new(id);
        println!("  {}: {} (node: {}, seq: {})", 
                 i + 1, id, sf.node_id_component(), sf.sequence_component());
    }
    
    // Verify uniqueness
    println!("\n--- Uniqueness Test ---");
    let test_ids = generator.generate_batch(10000);
    let unique_count: std::collections::HashSet<_> = test_ids.iter().collect();
    println!("Generated 10000 IDs, unique: {} (should be 10000)", unique_count.len());
    
    // Multiple generators (simulating distributed system)
    println!("\n--- Distributed System Simulation ---");
    let gen1 = SnowflakeGenerator::new(1, DEFAULT_EPOCH);
    let gen2 = SnowflakeGenerator::new(2, DEFAULT_EPOCH);
    let gen3 = SnowflakeGenerator::new(100, DEFAULT_EPOCH);
    
    let id1 = gen1.generate();
    let id2 = gen2.generate();
    let id3 = gen3.generate();
    
    println!("Node 1 ID: {} (node: {})", id1, SnowflakeGenerator::get_node_id(id1));
    println!("Node 2 ID: {} (node: {})", id2, SnowflakeGenerator::get_node_id(id2));
    println!("Node 100 ID: {} (node: {})", id3, SnowflakeGenerator::get_node_id(id3));
    
    // String and hex conversion
    println!("\n--- String/Hex Conversions ---");
    let original_id = generator.generate();
    let sf = SnowflakeId::new(original_id);
    
    let id_str = sf.to_string();
    let id_hex = sf.to_hex();
    
    println!("Original ID: {}", original_id);
    println!("String: {}", id_str);
    println!("Hex: {}", id_hex);
    
    let from_str = SnowflakeId::from_string(&id_str).unwrap();
    let from_hex = SnowflakeId::from_hex(&id_hex).unwrap();
    
    println!("From string: {}", from_str.id());
    println!("From hex: {}", from_hex.id());
    assert_eq!(from_str.id(), original_id);
    assert_eq!(from_hex.id(), original_id);
    
    println!("\n=== Demo Complete ===");
}