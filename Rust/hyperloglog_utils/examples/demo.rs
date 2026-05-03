//! Example demonstrating HyperLogLog cardinality estimation

use hyperloglog_utils::{HyperLogLog, SparseHyperLogLog};
use std::time::Instant;

fn main() {
    println!("=== HyperLogLog Utils Demo ===\n");

    // Demo 1: Basic usage
    println!("1. Basic Usage");
    println!("--------------");
    let mut hll = HyperLogLog::new(12).unwrap();
    
    let words = ["apple", "banana", "cherry", "date", "elderberry", 
                 "fig", "grape", "honeydew", "apple", "banana"]; // duplicates
    
    for word in words {
        hll.insert(word.as_bytes());
    }
    
    println!("Inserted {} words (with duplicates)", words.len());
    println!("Estimated unique words: {}", hll.count());
    println!("Actual unique words: 8\n");

    // Demo 2: Different precisions
    println!("2. Precision Comparison");
    println!("-----------------------");
    let n = 100_000u64;
    
    for precision in [8, 10, 12, 14] {
        let mut hll = HyperLogLog::new(precision).unwrap();
        for i in 0..n {
            hll.insert(&i.to_be_bytes());
        }
        
        let count = hll.count();
        let error = ((count as f64 - n as f64).abs() / n as f64) * 100.0;
        println!("Precision {}: Estimated = {}, Error = {:.2}%", 
                 precision, count, error);
    }
    println!();

    // Demo 3: Merge operation
    println!("3. Merge Operation");
    println!("------------------");
    let mut hll1 = HyperLogLog::new(12).unwrap();
    let mut hll2 = HyperLogLog::new(12).unwrap();
    
    // Split the data between two instances
    for i in 0..5000 {
        hll1.insert(&format!("user-{}", i).as_bytes());
    }
    for i in 5000..10000 {
        hll2.insert(&format!("user-{}", i).as_bytes());
    }
    
    println!("HLL1 count: {}", hll1.count());
    println!("HLL2 count: {}", hll2.count());
    
    hll1.merge(&hll2).unwrap();
    println!("After merge: {}", hll1.count());
    println!("Expected: ~10000\n");

    // Demo 4: Serialization
    println!("4. Serialization");
    println!("----------------");
    let mut hll = HyperLogLog::new(12).unwrap();
    for i in 0..5000 {
        hll.insert(&format!("item-{}", i).as_bytes());
    }
    
    let bytes = hll.to_bytes();
    println!("Serialized size: {} bytes", bytes.len());
    
    let hll2 = HyperLogLog::from_bytes(&bytes).unwrap();
    println!("Deserialized count: {}", hll2.count());
    println!("Original count: {}\n", hll.count());

    // Demo 5: Sparse HyperLogLog
    println!("5. Sparse HyperLogLog");
    println!("--------------------");
    let mut sparse = SparseHyperLogLog::new(12).unwrap();
    
    for i in 0..50 {
        sparse.insert(&format!("element-{}", i).as_bytes());
    }
    
    println!("Sparse count: {}", sparse.count());
    println!("Actual: 50\n");

    // Demo 6: Performance benchmark
    println!("6. Performance Benchmark");
    println!("------------------------");
    let mut hll = HyperLogLog::new(14).unwrap();
    let n = 1_000_000u64;
    
    let start = Instant::now();
    for i in 0..n {
        hll.insert(&i.to_be_bytes());
    }
    let insert_time = start.elapsed();
    
    let count = hll.count();
    let error = ((count as f64 - n as f64).abs() / n as f64) * 100.0;
    
    println!("Inserted {} elements in {:?}", n, insert_time);
    println!("Rate: {:.0} ops/sec", n as f64 / insert_time.as_secs_f64());
    println!("Estimated count: {}", count);
    println!("Error: {:.2}%", error);
    println!("Memory used: {} KB", (1 << 14) / 1024);
}