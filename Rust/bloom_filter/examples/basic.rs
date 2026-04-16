//! Basic usage example for Bloom Filter

use bloom_filter::{BloomConfig, BloomFilter, ScalableBloomFilter};

fn main() {
    println!("=== Bloom Filter Examples ===\n");
    
    // Example 1: Basic usage
    println!("1. Basic Bloom Filter Usage:");
    let mut filter = BloomFilter::<&str>::with_rate(1000, 0.01);
    
    // Insert some words
    let words = vec!["apple", "banana", "cherry", "date", "elderberry"];
    for word in &words {
        filter.insert(word);
        println!("   Inserted: {}", word);
    }
    println!();
    
    // Check membership
    println!("   Membership tests:");
    println!("   'apple' present? {}", filter.contains(&"apple"));
    println!("   'grape' present? {}", filter.contains(&"grape"));
    println!();
    
    // Example 2: Configuration
    println!("2. Custom Configuration:");
    let config = BloomConfig::optimal(10000, 0.001); // 0.1% false positive rate
    println!("   For 10000 items at 0.1% FPR:");
    println!("   - Bit array size: {}", config.size);
    println!("   - Hash functions: {}", config.hash_count);
    println!();
    
    // Example 3: Statistics
    println!("3. Filter Statistics:");
    println!("   Items inserted: {}", filter.len());
    println!("   Bits set: {}", filter.bit_count());
    println!("   Fill ratio: {:.2}%", filter.fill_ratio() * 100.0);
    println!("   Current FPR: {:.4}%", filter.current_false_positive_rate() * 100.0);
    println!();
    
    // Example 4: Scalable Bloom Filter
    println!("4. Scalable Bloom Filter:");
    let mut scalable: ScalableBloomFilter<i32> = ScalableBloomFilter::new(100, 0.01);
    
    // Insert many more items than initial capacity
    for i in 0..5000 {
        scalable.insert(&i);
    }
    
    println!("   Inserted 5000 items (initial capacity: 100)");
    println!("   Internal filters: {}", scalable.filter_count());
    println!("   Contains 100? {}", scalable.contains(&100));
    println!("   Contains 9999? {}", scalable.contains(&9999)); // Not inserted
    println!();
    
    // Example 5: Check and Insert
    println!("5. Check-and-Insert Pattern:");
    let mut filter2 = BloomFilter::<i32>::with_rate(100, 0.01);
    
    let result = filter2.check_and_insert(&42);
    println!("   First insert of 42: {} (was new)", !result);
    
    let result = filter2.check_and_insert(&42);
    println!("   Second insert of 42: {} (already existed)", result);
    println!();
    
    // Example 6: Serialization
    println!("6. Serialization:");
    let mut filter3 = BloomFilter::<&str>::with_rate(100, 0.01);
    filter3.insert(&"persistent");
    filter3.insert(&"storage");
    
    let bytes = filter3.to_bytes();
    println!("   Serialized to {} bytes", bytes.len());
    
    let restored = BloomFilter::<&str>::from_bytes(&bytes).unwrap();
    println!("   Restored filter contains 'persistent': {}", restored.contains(&"persistent"));
    println!("   Restored filter contains 'missing': {}", restored.contains(&"missing"));
    println!();
    
    // Example 7: Merge filters
    println!("7. Merging Filters:");
    let config = BloomConfig::optimal(100, 0.01);
    let mut filter_a: BloomFilter<i32> = BloomFilter::new(config);
    let mut filter_b: BloomFilter<i32> = BloomFilter::new(config);
    
    for i in 0..50 {
        filter_a.insert(&i);
    }
    for i in 50..100 {
        filter_b.insert(&i);
    }
    
    filter_a.merge(&filter_b).unwrap();
    println!("   Merged two filters (50 items each)");
    println!("   Contains 25? {}", filter_a.contains(&25));
    println!("   Contains 75? {}", filter_a.contains(&75));
    println!();
    
    // Example 8: False positive demonstration
    println!("8. False Positive Rate Test:");
    let mut test_filter = BloomFilter::<i32>::with_rate(1000, 0.01);
    
    // Insert 1000 items
    for i in 0..1000 {
        test_filter.insert(&i);
    }
    
    // Test 10000 items not in the set
    let mut false_positives = 0;
    let test_count = 10000;
    for i in 1000..(1000 + test_count) {
        if test_filter.contains(&i) {
            false_positives += 1;
        }
    }
    
    let actual_rate = false_positives as f64 / test_count as f64;
    println!("   Target FPR: 1.00%");
    println!("   Actual FPR: {:.4}%", actual_rate * 100.0);
    println!("   False positives found: {}/{}", false_positives, test_count);
}