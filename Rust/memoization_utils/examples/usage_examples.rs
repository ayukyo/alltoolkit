//! Usage Examples for memoization_utils
//!
//! This file demonstrates various use cases for the memoization utilities.

use memoization_utils::*;

fn main() {
    println!("=== Memoization Utils Examples ===\n");

    // Example 1: Basic Memoization
    basic_memoization();

    // Example 2: Capacity-Limited Cache with LRU
    lru_cache_example();

    // Example 3: Statistics Tracking
    stats_example();

    // Example 4: Recursive Fibonacci (Classic Example)
    fibonacci_example();

    // Example 5: Thread-Safe Cache
    thread_safe_example();

    // Example 6: Function Wrapper
    function_wrapper_example();

    // Example 7: Shared Cache Across Threads
    shared_cache_example();

    // Example 8: Complex Keys
    complex_key_example();

    // Example 9: Performance Comparison
    performance_comparison();
}

/// Example 1: Basic Memoization
fn basic_memoization() {
    println!("1. Basic Memoization");
    println!("---------------------");

    let mut cache: MemoCache<i32, i32> = MemoCache::new();

    // First computation (miss)
    let result1 = cache.get_or_compute(10, |k| {
        println!("  Computing square of {}", k);
        k * k
    });
    println!("  Result: {}", result1);

    // Second call (hit - cached)
    let result2 = cache.get_or_compute(10, |k| {
        println!("  This won't print - value is cached!");
        k * k + 1 // This won't execute
    });
    println!("  Cached result: {}", result2); // Still 100, not 101

    println!("  Cache size: {}", cache.len());
    println!();
}

/// Example 2: Capacity-Limited Cache with LRU Eviction
fn lru_cache_example() {
    println!("2. LRU Cache with Capacity Limit");
    println!("---------------------------------");

    let mut cache: MemoCache<i32, String> = MemoCache::with_capacity(3);

    // Add three items
    cache.get_or_compute(1, |_| "first".to_string());
    cache.get_or_compute(2, |_| "second".to_string());
    cache.get_or_compute(3, |_| "third".to_string());

    println!("  Cache after adding 1, 2, 3:");
    println!("    Contains 1: {}", cache.contains(&1));
    println!("    Contains 2: {}", cache.contains(&2));
    println!("    Contains 3: {}", cache.contains(&3));

    // Access 1 to make it recently used
    cache.get_or_compute(1, |_| "updated".to_string());

    // Add fourth item - should evict 2 (LRU)
    cache.get_or_compute(4, |_| "fourth".to_string());

    println!("  After adding 4 (capacity = 3):");
    println!("    Contains 1: {} (recently accessed)", cache.contains(&1));
    println!("    Contains 2: {} (evicted - LRU)", cache.contains(&2));
    println!("    Contains 3: {}", cache.contains(&3));
    println!("    Contains 4: {}", cache.contains(&4));
    println!("    Evictions: {}", cache.stats().evictions);
    println!();
}

/// Example 3: Statistics Tracking
fn stats_example() {
    println!("3. Cache Statistics");
    println!("-------------------");

    let mut cache: MemoCache<i32, i32> = MemoCache::new();

    // Compute some values
    for i in 1..=5 {
        cache.get_or_compute(i, |k| *k);
    }
    println!("  After 5 unique computations:");
    println!("    Misses: {}", cache.stats().misses);

    // Access cached values multiple times
    for _ in 0..10 {
        cache.get_or_compute(1, |k| *k);
    }
    for _ in 0..5 {
        cache.get_or_compute(2, |k| *k);
    }

    println!("  After accessing cached values:");
    println!("    Hits: {}", cache.stats().hits);
    println!("    Misses: {}", cache.stats().misses);
    println!("    Hit rate: {:.2}%", cache.hit_rate());
    println!();
}

/// Example 4: Recursive Fibonacci with Memoization
fn fibonacci_example() {
    println!("4. Fibonacci with Memoization");
    println!("------------------------------");

    let memo = RecursiveMemo::<u32, u64>::new();

    // Define fib as a standalone function for proper recursion
    fn fib(memo: &RecursiveMemo<u32, u64>, n: u32) -> u64 {
        if n <= 1 {
            n as u64
        } else {
            memo.memoize(n - 1, |m, k| fib(m, *k)) + memo.memoize(n - 2, |m, k| fib(m, *k))
        }
    }

    println!("  Fibonacci sequence:");
    for n in [0, 1, 5, 10, 20, 30] {
        let result = fib(&memo, n);
        println!("    fib({}) = {}", n, result);
    }

    println!("  Cache statistics:");
    println!("    Total computations (misses): {}", memo.stats().misses);
    println!("    Cache hits (reuses): {}", memo.stats().hits);
    println!("    Efficiency: ~{} unique computations for fib(30)",
             memo.stats().misses);
    println!();
}

/// Example 5: Thread-Safe Cache
fn thread_safe_example() {
    println!("5. Thread-Safe Cache");
    println!("--------------------");

    use std::sync::Arc;
    use std::thread;

    let cache = Arc::new(ThreadSafeMemoCache::<i32, i32>::with_capacity(10));

    let mut handles = vec![];

    for t in 0..3 {
        let cache_clone = Arc::clone(&cache);
        handles.push(thread::spawn(move || {
            for i in (t * 10)..((t + 1) * 10) {
                cache_clone.get_or_compute(i, |k| {
                    // Simulate expensive computation
                    k * k
                });
            }
        }));
    }

    for handle in handles {
        handle.join().unwrap();
    }

    println!("  After 3 threads each computing 10 values:");
    println!("    Cache size: {}", cache.len());
    println!("    Total hits: {}", cache.stats().hits);
    println!("    Total misses: {}", cache.stats().misses);
    println!();
}

/// Example 6: Function Wrapper
fn function_wrapper_example() {
    println!("6. Memoized Function Wrapper");
    println!("----------------------------");

    // Create a memoized factorial function
    let mut factorial = memoize(|n: &u32| -> u64 {
        if *n <= 1 { 1 } else {
            let mut result: u64 = 1;
            for i in 2..=*n { result *= i as u64; }
            result
        }
    });

    println!("  Factorial examples:");
    println!("    factorial(5) = {}", factorial(5));
    println!("    factorial(10) = {}", factorial(10));
    println!("    factorial(5) (cached) = {}", factorial(5));

    // Create memoized string length function
    let mut string_len = memoize(|s: &String| -> usize {
        println!("    Computing length...");
        s.len()
    });

    let hello = "Hello, World!".to_string();
    println!("  String length:");
    println!("    len(\"{}\") = {}", hello, string_len(hello.clone()));
    println!("    cached len = {}", string_len(hello.clone()));
    println!();
}

/// Example 7: Shared Cache Across Threads
fn shared_cache_example() {
    println!("7. Shared Cache (Arc<Mutex>)");
    println!("----------------------------");

    use std::sync::Arc;
    use std::thread;

    let shared = Arc::new(create_shared_cache::<String, i32>(20));

    // Thread 1 computes some values
    let shared1 = Arc::clone(&shared);
    let t1 = thread::spawn(move || {
        {
            let mut cache = shared1.lock().unwrap();
            cache.insert("a".to_string(), 1);
            cache.insert("b".to_string(), 2);
        }
    });

    // Thread 2 reads and adds more
    let shared2 = Arc::clone(&shared);
    let t2 = thread::spawn(move || {
        t1.join().unwrap(); // Wait for t1
        {
            let mut cache = shared2.lock().unwrap();
            cache.insert("c".to_string(), 3);
            // Read values from t1
            if let Some(val) = cache.get(&"a".to_string()) {
                println!("  Thread 2 read 'a' = {}", val);
            }
        }
    });

    t2.join().unwrap();

    let cache = shared.lock().unwrap();
    println!("  Final cache contents:");
    println!("    Size: {}", cache.len());
    println!("    'a' = {:?}", cache.get(&"a".to_string()));
    println!("    'b' = {:?}", cache.get(&"b".to_string()));
    println!("    'c' = {:?}", cache.get(&"c".to_string()));
    println!();
}

/// Example 8: Complex Keys
fn complex_key_example() {
    println!("8. Complex Keys (Tuples, Structs)");
    println!("---------------------------------");

    // Using tuples as keys
    let mut distance_cache: MemoCache<(i32, i32), i32> = MemoCache::new();

    let distance = distance_cache.get_or_compute((0, 5), |k| {
        // Manhattan distance
        (k.0 - k.1).abs()
    });
    println!("  Manhattan distance (0, 5) = {}", distance);
    println!("  Cached distance = {}", distance_cache.get_or_compute((0, 5), |_| 0));

    // Using string+int tuple
    let mut named_cache: MemoCache<(String, i32), String> = MemoCache::new();

    let location = named_cache.get_or_compute(("point".to_string(), 42), |coords| {
        format!("{} at index {}", coords.0, coords.1)
    });
    println!("  Named point: {}", location);

    // Using array-like tuple for coordinates (int-based)
    let mut grid_cache: MemoCache<(i32, i32), String> = MemoCache::new();

    let cell = grid_cache.get_or_compute((10, 20), |coords| {
        format!("Cell ({}, {})", coords.0, coords.1)
    });
    println!("  Grid cell: {}", cell);
    println!();
}

/// Example 9: Performance Comparison
fn performance_comparison() {
    println!("9. Performance Comparison");
    println!("-------------------------");

    use std::time::Instant;

    // Without memoization
    fn compute_expensive(n: i32) -> i32 {
        // Simulate expensive computation
        let mut result = n;
        for _ in 0..1000 {
            result = (result * 7 + 13) % 10000;
        }
        result
    }

    let start = Instant::now();
    for _ in 0..1000 {
        compute_expensive(42);
    }
    let no_memo_time = start.elapsed();

    // With memoization
    let mut cache: MemoCache<i32, i32> = MemoCache::new();
    let start = Instant::now();
    for _ in 0..1000 {
        cache.get_or_compute(42, |k| compute_expensive(*k));
    }
    let memo_time = start.elapsed();

    println!("  Computing expensive function 1000 times:");
    println!("    Without memoization: {:?}", no_memo_time);
    println!("    With memoization: {:?}", memo_time);
    println!("    Speedup: ~{}x", no_memo_time.as_nanos() / memo_time.as_nanos());
    println!("    Cache hits: {}", cache.stats().hits);
    println!("    Cache misses: {}", cache.stats().misses);
    println!();
}