//! Integration tests for memoization_utils
//!
//! These tests verify the functionality of the memoization utilities
//! including basic caching, LRU eviction, thread safety, and recursive memoization.

use memoization_utils::*;

mod basic_tests {
    use super::*;

    #[test]
    fn test_new_cache_is_empty() {
        let cache: MemoCache<i32, i32> = MemoCache::new();
        assert!(cache.is_empty());
        assert_eq!(cache.len(), 0);
    }

    #[test]
    fn test_with_capacity_creates_empty_cache() {
        let cache: MemoCache<i32, i32> = MemoCache::with_capacity(100);
        assert!(cache.is_empty());
        assert_eq!(cache.len(), 0);
    }

    #[test]
    fn test_default_creates_empty_cache() {
        let cache: MemoCache<i32, i32> = MemoCache::default();
        assert!(cache.is_empty());
    }

    #[test]
    fn test_single_value_caching() {
        let mut cache: MemoCache<i32, String> = MemoCache::new();

        let result = cache.get_or_compute(42, |k| format!("value_{}", k));
        assert_eq!(result, "value_42");

        // Second call should return cached value
        let result2 = cache.get_or_compute(42, |k| format!("different_{}", k));
        assert_eq!(result2, "value_42"); // Not "different_42"

        let stats = cache.stats();
        assert_eq!(stats.hits, 1);
        assert_eq!(stats.misses, 1);
        assert_eq!(stats.evictions, 0);
    }

    #[test]
    fn test_multiple_values() {
        let mut cache: MemoCache<i32, i32> = MemoCache::new();

        for i in 1..=10 {
            cache.get_or_compute(i, |k| *k * 2);
        }

        assert_eq!(cache.len(), 10);

        // All should be cached
        for i in 1..=10 {
            assert!(cache.contains(&i));
            assert_eq!(cache.get(&i), Some(&(i * 2)));
        }

        let stats = cache.stats();
        assert_eq!(stats.misses, 10);
        assert_eq!(stats.hits, 0);
    }

    #[test]
    fn test_contains_without_compute() {
        let mut cache: MemoCache<String, i32> = MemoCache::new();

        cache.get_or_compute("key".to_string(), |_| 123);

        assert!(cache.contains(&"key".to_string()));
        assert!(!cache.contains(&"other".to_string()));
    }
}

mod lru_tests {
    use super::*;

    #[test]
    fn test_lru_eviction_on_capacity() {
        let mut cache: MemoCache<i32, i32> = MemoCache::with_capacity(2);

        cache.get_or_compute(1, |k| *k);
        cache.get_or_compute(2, |k| *k);

        assert_eq!(cache.len(), 2);

        // Adding third should evict first (LRU)
        cache.get_or_compute(3, |k| *k);

        assert_eq!(cache.len(), 2);
        assert!(!cache.contains(&1));
        assert!(cache.contains(&2));
        assert!(cache.contains(&3));

        assert_eq!(cache.stats().evictions, 1);
    }

    #[test]
    fn test_access_updates_lru_order() {
        let mut cache: MemoCache<i32, i32> = MemoCache::with_capacity(3);

        // Add 1, 2, 3
        cache.get_or_compute(1, |k| *k);
        cache.get_or_compute(2, |k| *k);
        cache.get_or_compute(3, |k| *k);

        // Access 1 - makes it most recently used
        cache.get_or_compute(1, |k| *k);

        // Add 4 - should evict 2 (now LRU)
        cache.get_or_compute(4, |k| *k);

        assert!(cache.contains(&1));
        assert!(!cache.contains(&2)); // Evicted
        assert!(cache.contains(&3));
        assert!(cache.contains(&4));
    }

    #[test]
    fn test_capacity_zero_edge_case() {
        let mut cache: MemoCache<i32, i32> = MemoCache::with_capacity(0);

        // Even with capacity 0, we should handle gracefully
        // In our implementation, capacity 0 means max capacity due to usize::MAX behavior
        // Or we could interpret it as no caching
        let result = cache.get_or_compute(1, |k| *k);
        assert_eq!(result, 1);
    }

    #[test]
    fn test_large_capacity_no_eviction() {
        let mut cache: MemoCache<i32, i32> = MemoCache::with_capacity(1000);

        for i in 0..100 {
            cache.get_or_compute(i, |k| *k);
        }

        assert_eq!(cache.len(), 100);
        assert_eq!(cache.stats().evictions, 0);
    }
}

mod stats_tests {
    use super::*;

    #[test]
    fn test_initial_stats() {
        let cache: MemoCache<i32, i32> = MemoCache::new();
        let stats = cache.stats();

        assert_eq!(stats.hits, 0);
        assert_eq!(stats.misses, 0);
        assert_eq!(stats.evictions, 0);
    }

    #[test]
    fn test_hit_rate_zero_total() {
        let cache: MemoCache<i32, i32> = MemoCache::new();
        assert_eq!(cache.hit_rate(), 0.0);
    }

    #[test]
    fn test_hit_rate_calculation() {
        let mut cache: MemoCache<i32, i32> = MemoCache::new();

        // 3 misses
        cache.get_or_compute(1, |k| *k);
        cache.get_or_compute(2, |k| *k);
        cache.get_or_compute(3, |k| *k);

        // 7 hits
        for _ in 0..7 {
            cache.get_or_compute(1, |k| *k);
        }

        // Hit rate = 7 / 10 = 70%
        assert_eq!(cache.hit_rate(), 70.0);
    }

    #[test]
    fn test_hit_rate_100_percent() {
        let mut cache: MemoCache<i32, i32> = MemoCache::new();

        cache.get_or_compute(1, |k| *k); // Miss
        cache.get_or_compute(1, |k| *k); // Hit
        cache.get_or_compute(1, |k| *k); // Hit

        // After first miss, all hits
        // Total: 3, Hits: 2, Rate: 66.67%
        // But if we compute fresh:
        let mut cache2: MemoCache<i32, i32> = MemoCache::new();
        cache2.get_or_compute(1, |k| *k);
        let _ = cache2.get(&1); // This doesn't count as operation

        // Actually, let's do proper test
        let mut cache3: MemoCache<i32, i32> = MemoCache::new();
        cache3.get_or_compute(1, |k| *k); // 1 miss
        for _ in 0..99 {
            cache3.get_or_compute(1, |k| *k); // 99 hits
        }
        // Hit rate = 99%
        assert!((cache3.hit_rate() - 99.0).abs() < 0.01);
    }
}

mod thread_safe_tests {
    use super::*;
    use std::sync::Arc;
    use std::thread;

    #[test]
    fn test_thread_safe_basic() {
        let cache = ThreadSafeMemoCache::<i32, i32>::new();

        let result = cache.get_or_compute(5, |k| *k * *k); // 5 * 5 = 25
        assert_eq!(result, 25);

        // Second call should cache
        let result2 = cache.get_or_compute(5, |_k| 0); // Would return 0 if not cached
        assert_eq!(result2, 25); // Cached value
    }

    #[test]
    fn test_concurrent_access() {
        let cache = Arc::new(ThreadSafeMemoCache::<i32, i32>::new());
        let mut handles = vec![];

        // Spawn 10 threads, each accessing 0-9
        for _ in 0..10 {
            let cache_clone = Arc::clone(&cache);
            handles.push(thread::spawn(move || {
                for i in 0..10 {
                    cache_clone.get_or_compute(i, |k| *k * 2);
                }
            }));
        }

        for handle in handles {
            handle.join().unwrap();
        }

        // All 10 values should be cached
        assert_eq!(cache.len(), 10);

        // Many hits should have occurred
        let stats = cache.stats();
        assert!(stats.hits > 0);
        assert!(stats.hits + stats.misses == 100); // 10 threads * 10 calls
    }

    #[test]
    fn test_thread_safe_clear() {
        let cache = ThreadSafeMemoCache::<i32, i32>::new();

        cache.get_or_compute(1, |k| *k);
        cache.get_or_compute(2, |k| *k);

        assert_eq!(cache.len(), 2);

        cache.clear();

        assert_eq!(cache.len(), 0);
    }
}

mod recursive_memo_tests {
    use super::*;

    #[test]
    fn test_fibonacci_memoization() {
        let memo = RecursiveMemo::<u32, u64>::new();

        // Define fib as a standalone function that takes memo reference
        fn fib(memo: &RecursiveMemo<u32, u64>, n: u32) -> u64 {
            if n <= 1 {
                n as u64
            } else {
                memo.memoize(n - 1, |m, k| fib(m, *k)) + memo.memoize(n - 2, |m, k| fib(m, *k))
            }
        }

        // Known Fibonacci values
        assert_eq!(fib(&memo, 0), 0);
        assert_eq!(fib(&memo, 1), 1);
        assert_eq!(fib(&memo, 10), 55);
        assert_eq!(fib(&memo, 20), 6765);
        assert_eq!(fib(&memo, 30), 832040);
    }

    #[test]
    fn test_factorial_memoization() {
        let memo = RecursiveMemo::<u32, u64>::new();

        fn factorial(memo: &RecursiveMemo<u32, u64>, n: u32) -> u64 {
            if n <= 1 {
                1
            } else {
                n as u64 * memo.memoize(n - 1, |m, k| factorial(m, *k))
            }
        }

        assert_eq!(factorial(&memo, 0), 1);
        assert_eq!(factorial(&memo, 1), 1);
        assert_eq!(factorial(&memo, 5), 120);
        assert_eq!(factorial(&memo, 10), 3628800);
    }

    #[test]
    fn test_recursive_stats() {
        let memo = RecursiveMemo::<u32, u64>::new();

        fn fib(memo: &RecursiveMemo<u32, u64>, n: u32) -> u64 {
            if n <= 1 {
                n as u64
            } else {
                memo.memoize(n - 1, |m, k| fib(m, *k)) + memo.memoize(n - 2, |m, k| fib(m, *k))
            }
        }

        fib(&memo, 20);

        let stats = memo.stats();
        // With memoization, we should have far fewer misses than naive recursion
        // Naive would compute fib(20) ~ 2^20 times
        // Memoized only computes each value once
        assert!(stats.misses <= 21); // fib(0) through fib(20)
        assert!(stats.hits > 0); // Many reuses
    }
}

mod insert_remove_tests {
    use super::*;

    #[test]
    fn test_manual_insert() {
        let mut cache: MemoCache<String, i32> = MemoCache::new();

        cache.insert("key1".to_string(), 100);
        cache.insert("key2".to_string(), 200);

        assert_eq!(cache.get(&"key1".to_string()), Some(&100));
        assert_eq!(cache.get(&"key2".to_string()), Some(&200));
    }

    #[test]
    fn test_insert_updates_existing() {
        let mut cache: MemoCache<i32, i32> = MemoCache::new();

        cache.get_or_compute(1, |_| 100);
        assert_eq!(cache.get(&1), Some(&100));

        cache.insert(1, 200);
        assert_eq!(cache.get(&1), Some(&200));
    }

    #[test]
    fn test_remove_existing() {
        let mut cache: MemoCache<i32, i32> = MemoCache::new();

        cache.get_or_compute(1, |k| *k);
        cache.get_or_compute(2, |k| *k);

        let removed = cache.remove(&1);

        assert_eq!(removed, Some(1));
        assert!(!cache.contains(&1));
        assert!(cache.contains(&2));
    }

    #[test]
    fn test_remove_non_existing() {
        let mut cache: MemoCache<i32, i32> = MemoCache::new();

        let removed = cache.remove(&999);
        assert_eq!(removed, None);
    }

    #[test]
    fn test_clear_removes_all() {
        let mut cache: MemoCache<i32, i32> = MemoCache::new();

        for i in 0..100 {
            cache.get_or_compute(i, |k| *k);
        }

        assert_eq!(cache.len(), 100);

        cache.clear();

        assert!(cache.is_empty());
        assert_eq!(cache.len(), 0);
    }
}

mod shared_cache_tests {
    use super::*;
    use std::sync::Arc;
    use std::thread;

    #[test]
    fn test_create_shared_cache() {
        let shared = create_shared_cache::<i32, i32>(10);

        {
            let mut cache = shared.lock().unwrap();
            cache.get_or_compute(5, |k| *k * *k); // 5 * 5 = 25
        }

        {
            let cache = shared.lock().unwrap();
            assert_eq!(cache.get(&5), Some(&25));
        }
    }

    #[test]
    fn test_shared_cache_concurrent() {
        let shared = Arc::new(create_shared_cache::<i32, i32>(50));
        let mut handles = vec![];

        for t in 0..5 {
            let cache_clone = Arc::clone(&shared);
            handles.push(thread::spawn(move || {
                for i in t * 10..(t + 1) * 10 {
                    let mut cache = cache_clone.lock().unwrap();
                    cache.get_or_compute(i, |k| *k);
                }
            }));
        }

        for handle in handles {
            handle.join().unwrap();
        }

        let cache = shared.lock().unwrap();
        assert_eq!(cache.len(), 50);
    }
}

mod function_wrapper_tests {
    use super::*;

    #[test]
    fn test_memoize_wrapper() {
        let mut squared = memoize(|n: &i32| -> i32 { n * n });

        assert_eq!(squared(5), 25);
        assert_eq!(squared(5), 25); // Cached
        assert_eq!(squared(10), 100);
    }

    #[test]
    fn test_memoize_with_capacity() {
        let mut cache = memoize_with_capacity(3, |n: &i32| -> i32 { n * n });

        cache(1);
        cache(2);
        cache(3);
        cache(4); // Should evict one

        // Verify it works
        assert_eq!(cache(2), 4); // Should still be cached
        assert_eq!(cache(4), 16);
    }
}

mod complex_key_tests {
    use super::*;

    #[test]
    fn test_tuple_key() {
        let mut cache: MemoCache<(i32, i32), i32> = MemoCache::new();

        let result = cache.get_or_compute((3, 4), |k| k.0 * k.1);
        assert_eq!(result, 12);

        let result2 = cache.get_or_compute((3, 4), |k| 0);
        assert_eq!(result2, 12); // Cached, not 0
    }

    #[test]
    fn test_string_key() {
        let mut cache: MemoCache<String, usize> = MemoCache::new();

        let len = cache.get_or_compute("hello".to_string(), |s| s.len());
        assert_eq!(len, 5);

        let len2 = cache.get_or_compute("hello".to_string(), |_| 0);
        assert_eq!(len2, 5); // Cached
    }
}

mod edge_case_tests {
    use super::*;

    #[test]
    fn test_empty_key_types() {
        // Test with unit type as value
        let mut cache: MemoCache<i32, ()> = MemoCache::new();
        cache.get_or_compute(1, |_| ());
        assert!(cache.contains(&1));
    }

    #[test]
    fn test_large_values() {
        let mut cache: MemoCache<i32, Vec<u64>> = MemoCache::new();

        let large_vec: Vec<u64> = (0..1000).collect();
        cache.get_or_compute(1, |_| large_vec.clone());

        assert_eq!(cache.get(&1).unwrap().len(), 1000);
    }

    #[test]
    fn test_negative_numbers() {
        let mut cache: MemoCache<i32, i32> = MemoCache::new();

        assert_eq!(cache.get_or_compute(-5, |k| *k), -5);
        assert_eq!(cache.get_or_compute(-10, |k| *k * 2), -20);
    }
}