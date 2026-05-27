//! Memoization Utilities for Rust
//!
//! This crate provides memoization (caching) utilities for functions,
//! enabling efficient caching of computation results to avoid redundant work.
//!
//! ## Features
//! - Simple memoization cache with configurable capacity
//! - Macro for easy function memoization
//! - Thread-safe memoization support
//! - LRU (Least Recently Used) eviction policy
//! - Statistics tracking (hits, misses, evictions)
//!
//! ## Zero External Dependencies
//! This implementation uses only Rust's standard library.

use std::collections::HashMap;
use std::hash::Hash;
use std::sync::{Arc, Mutex, RwLock};

/// A simple memoization cache that stores function results.
///
/// Uses LRU eviction when capacity limit is reached.
pub struct MemoCache<K, V> {
    data: HashMap<K, (V, u64)>,
    access_order: Vec<K>,
    capacity: usize,
    stats: CacheStats,
}

/// Statistics for a memoization cache.
#[derive(Debug, Clone, Copy, Default)]
pub struct CacheStats {
    /// Number of successful cache hits
    pub hits: u64,
    /// Number of cache misses (new computations)
    pub misses: u64,
    /// Number of entries evicted due to capacity limit
    pub evictions: u64,
}

impl<K, V> MemoCache<K, V>
where
    K: Eq + Hash + Clone,
    V: Clone,
{
    /// Creates a new memoization cache with unlimited capacity.
    pub fn new() -> Self {
        Self::with_capacity(usize::MAX)
    }

    /// Creates a new memoization cache with a specified capacity.
    ///
    /// When the cache exceeds this capacity, the least recently used
    /// entries will be evicted.
    pub fn with_capacity(capacity: usize) -> Self {
        MemoCache {
            data: HashMap::new(),
            access_order: Vec::new(),
            capacity,
            stats: CacheStats::default(),
        }
    }

    /// Gets a cached value or computes it using the provided function.
    ///
    /// # Arguments
    /// * `key` - The key to look up
    /// * `compute` - A function to compute the value if not cached
    ///
    /// # Returns
    /// The cached or newly computed value.
    pub fn get_or_compute<F>(&mut self, key: K, compute: F) -> V
    where
        F: FnOnce(&K) -> V,
    {
        let access_counter = self.stats.hits + self.stats.misses;

        if let Some((value, _)) = self.data.get(&key) {
            self.stats.hits += 1;
            // Update access order for LRU tracking
            if let Some(pos) = self.access_order.iter().position(|k| k == &key) {
                self.access_order.remove(pos);
                self.access_order.push(key.clone());
            }
            return value.clone();
        }

        self.stats.misses += 1;

        // Evict LRU entry if at capacity
        if self.data.len() >= self.capacity && self.capacity != usize::MAX {
            if let Some(lru_key) = self.access_order.first().cloned() {
                self.data.remove(&lru_key);
                self.access_order.remove(0);
                self.stats.evictions += 1;
            }
        }

        let value = compute(&key);
        self.data.insert(key.clone(), (value.clone(), access_counter));
        self.access_order.push(key.clone());
        value
    }

    /// Checks if a key exists in the cache without computing.
    pub fn contains(&self, key: &K) -> bool {
        self.data.contains_key(key)
    }

    /// Gets a cached value if it exists.
    pub fn get(&self, key: &K) -> Option<&V> {
        self.data.get(key).map(|(v, _)| v)
    }

    /// Manually inserts a value into the cache.
    pub fn insert(&mut self, key: K, value: V) {
        let access_counter = self.stats.hits + self.stats.misses;

        // Evict LRU entry if at capacity
        if self.data.len() >= self.capacity && self.capacity != usize::MAX && !self.data.contains_key(&key) {
            if let Some(lru_key) = self.access_order.first().cloned() {
                self.data.remove(&lru_key);
                self.access_order.remove(0);
                self.stats.evictions += 1;
            }
        }

        // Remove old key from access order if updating
        if self.data.contains_key(&key) {
            if let Some(pos) = self.access_order.iter().position(|k| k == &key) {
                self.access_order.remove(pos);
            }
        }

        self.data.insert(key.clone(), (value, access_counter));
        self.access_order.push(key);
    }

    /// Removes a specific entry from the cache.
    pub fn remove(&mut self, key: &K) -> Option<V> {
        if let Some(pos) = self.access_order.iter().position(|k| k == key) {
            self.access_order.remove(pos);
        }
        self.data.remove(key).map(|(v, _)| v)
    }

    /// Clears all entries from the cache.
    pub fn clear(&mut self) {
        self.data.clear();
        self.access_order.clear();
    }

    /// Returns the number of entries in the cache.
    pub fn len(&self) -> usize {
        self.data.len()
    }

    /// Returns true if the cache is empty.
    pub fn is_empty(&self) -> bool {
        self.data.is_empty()
    }

    /// Returns the cache statistics.
    pub fn stats(&self) -> CacheStats {
        self.stats
    }

    /// Returns the hit rate as a percentage (0.0 to 100.0).
    pub fn hit_rate(&self) -> f64 {
        let total = self.stats.hits + self.stats.misses;
        if total == 0 {
            0.0
        } else {
            (self.stats.hits as f64 / total as f64) * 100.0
        }
    }
}

impl<K, V> Default for MemoCache<K, V>
where
    K: Eq + Hash + Clone,
    V: Clone,
{
    fn default() -> Self {
        Self::new()
    }
}

/// A thread-safe memoization cache using RwLock.
pub struct ThreadSafeMemoCache<K, V> {
    inner: RwLock<MemoCache<K, V>>,
}

impl<K, V> ThreadSafeMemoCache<K, V>
where
    K: Eq + Hash + Clone,
    V: Clone,
{
    /// Creates a new thread-safe memoization cache with unlimited capacity.
    pub fn new() -> Self {
        Self::with_capacity(usize::MAX)
    }

    /// Creates a new thread-safe memoization cache with a specified capacity.
    pub fn with_capacity(capacity: usize) -> Self {
        ThreadSafeMemoCache {
            inner: RwLock::new(MemoCache::with_capacity(capacity)),
        }
    }

    /// Gets a cached value or computes it using the provided function.
    pub fn get_or_compute<F>(&self, key: K, compute: F) -> V
    where
        F: FnOnce(&K) -> V,
    {
        // First check if already cached (read lock)
        let cached_value: Option<V>;
        {
            let read_guard = self.inner.read().unwrap();
            if let Some((value, _)) = read_guard.data.get(&key) {
                cached_value = Some(value.clone());
            } else {
                cached_value = None;
            }
        }

        if let Some(value) = cached_value {
            // Update access order and stats (write lock)
            let mut write_guard = self.inner.write().unwrap();
            write_guard.stats.hits += 1;
            if let Some(pos) = write_guard.access_order.iter().position(|k| k == &key) {
                write_guard.access_order.remove(pos);
                write_guard.access_order.push(key.clone());
            }
            return value;
        }

        // Compute the value (write lock)
        let mut write_guard = self.inner.write().unwrap();
        write_guard.get_or_compute(key, compute)
    }

    /// Gets the cache statistics.
    pub fn stats(&self) -> CacheStats {
        self.inner.read().unwrap().stats()
    }

    /// Returns the number of entries in the cache.
    pub fn len(&self) -> usize {
        self.inner.read().unwrap().len()
    }

    /// Clears the cache.
    pub fn clear(&self) {
        self.inner.write().unwrap().clear();
    }
}

impl<K, V> Default for ThreadSafeMemoCache<K, V>
where
    K: Eq + Hash + Clone,
    V: Clone,
{
    fn default() -> Self {
        Self::new()
    }
}

/// An Arc-based memoization cache for sharing across threads.
pub type SharedMemoCache<K, V> = Arc<Mutex<MemoCache<K, V>>>;

/// Creates a shared memoization cache.
pub fn create_shared_cache<K, V>(capacity: usize) -> SharedMemoCache<K, V>
where
    K: Eq + Hash + Clone,
    V: Clone,
{
    Arc::new(Mutex::new(MemoCache::with_capacity(capacity)))
}

/// Memoize trait for automatic memoization support.
pub trait Memoize<K, V>: Sized
where
    K: Eq + Hash + Clone,
    V: Clone,
{
    /// Computes the value for a given key.
    fn compute(&self, key: &K) -> V;

    /// Creates a memoized version of this function.
    fn memoized(self) -> Memoized<K, V, Self> {
        Memoized {
            compute: self,
            cache: MemoCache::new(),
        }
    }

    /// Creates a memoized version with a capacity limit.
    fn memoized_with_capacity(self, capacity: usize) -> Memoized<K, V, Self> {
        Memoized {
            compute: self,
            cache: MemoCache::with_capacity(capacity),
        }
    }
}

/// A memoized function wrapper.
pub struct Memoized<K, V, F>
where
    K: Eq + Hash + Clone,
    V: Clone,
{
    compute: F,
    cache: MemoCache<K, V>,
}

impl<K, V, F> Memoized<K, V, F>
where
    K: Eq + Hash + Clone,
    V: Clone,
    F: Fn(&K) -> V,
{
    /// Calls the memoized function.
    pub fn call(&mut self, key: K) -> V {
        self.cache.get_or_compute(key, |k| (self.compute)(k))
    }

    /// Returns the cache statistics.
    pub fn stats(&self) -> CacheStats {
        self.cache.stats()
    }

    /// Clears the cache.
    pub fn clear(&mut self) {
        self.cache.clear();
    }
}

/// A recursive memoization helper for functions that call themselves.
///
/// Useful for memoizing recursive functions like Fibonacci, factorial, etc.
pub struct RecursiveMemo<K, V>
where
    K: Eq + Hash + Clone,
    V: Clone,
{
    cache: ThreadSafeMemoCache<K, V>,
}

impl<K, V> RecursiveMemo<K, V>
where
    K: Eq + Hash + Clone,
    V: Clone,
{
    /// Creates a new recursive memoization helper.
    pub fn new() -> Self {
        Self::with_capacity(usize::MAX)
    }

    /// Creates a new recursive memoization helper with capacity limit.
    pub fn with_capacity(capacity: usize) -> Self {
        RecursiveMemo {
            cache: ThreadSafeMemoCache::with_capacity(capacity),
        }
    }

    /// Memoizes a recursive computation.
    ///
    /// The compute function receives a reference to self for recursive calls.
    pub fn memoize<F>(&self, key: K, compute: F) -> V
    where
        F: FnOnce(&Self, &K) -> V,
    {
        // First check if already cached (read lock)
        {
            let read_guard = self.cache.inner.read().unwrap();
            if let Some((value, _)) = read_guard.data.get(&key) {
                // Need to increment hits, so we need write lock
                drop(read_guard);
                let mut write_guard = self.cache.inner.write().unwrap();
                write_guard.stats.hits += 1;
                // Update access order for LRU
                if let Some(pos) = write_guard.access_order.iter().position(|k| k == &key) {
                    write_guard.access_order.remove(pos);
                    write_guard.access_order.push(key.clone());
                }
                // Return the cached value
                return write_guard.data.get(&key).map(|(v, _)| v.clone()).unwrap();
            }
        }

        // Compute the value
        let value = compute(self, &key);

        // Store in cache (write lock)
        {
            let mut write_guard = self.cache.inner.write().unwrap();
            if !write_guard.data.contains_key(&key) {
                write_guard.stats.misses += 1;
                write_guard.data.insert(key.clone(), (value.clone(), 0));
                write_guard.access_order.push(key);
            }
        }

        value
    }

    /// Returns the cache statistics.
    pub fn stats(&self) -> CacheStats {
        self.cache.stats()
    }

    /// Clears the cache.
    pub fn clear(&self) {
        self.cache.clear();
    }
}

impl<K, V> Default for RecursiveMemo<K, V>
where
    K: Eq + Hash + Clone,
    V: Clone,
{
    fn default() -> Self {
        Self::new()
    }
}

/// Creates a memoized wrapper for a function (non-recursive version).
///
/// # Example
/// ```rust
/// use memoization_utils::memoize;
///
/// let mut squared = memoize(|n: &i32| -> i32 { *n * *n });
///
/// assert_eq!(squared(5), 25);
/// assert_eq!(squared(5), 25); // Cached
/// ```
pub fn memoize<K, V, F>(f: F) -> impl FnMut(K) -> V
where
    K: Eq + Hash + Clone,
    V: Clone,
    F: Fn(&K) -> V,
{
    let mut cache = MemoCache::new();
    move |key: K| cache.get_or_compute(key, |k| f(k))
}

/// Creates a memoized wrapper with capacity limit.
pub fn memoize_with_capacity<K, V, F>(capacity: usize, f: F) -> impl FnMut(K) -> V
where
    K: Eq + Hash + Clone,
    V: Clone,
    F: Fn(&K) -> V,
{
    let mut cache = MemoCache::with_capacity(capacity);
    move |key: K| cache.get_or_compute(key, |k| f(k))
}

#[cfg(test)]
mod tests {
    use super::*;
    use std::sync::Arc;
    use std::thread;

    #[test]
    fn test_basic_memoization() {
        let mut cache: MemoCache<i32, i32> = MemoCache::new();

        let result1 = cache.get_or_compute(5, |k| k * k);
        assert_eq!(result1, 25);

        let result2 = cache.get_or_compute(5, |k| k * k); // Should be cached
        assert_eq!(result2, 25);

        let stats = cache.stats();
        assert_eq!(stats.hits, 1);
        assert_eq!(stats.misses, 1);
    }

    #[test]
    fn test_capacity_limit() {
        let mut cache: MemoCache<i32, i32> = MemoCache::with_capacity(3);

        // Fill cache
        cache.get_or_compute(1, |k| *k);
        cache.get_or_compute(2, |k| *k);
        cache.get_or_compute(3, |k| *k);

        assert_eq!(cache.len(), 3);

        // Add another - should evict LRU (1)
        cache.get_or_compute(4, |k| *k);

        assert_eq!(cache.len(), 3);
        assert!(!cache.contains(&1));
        assert!(cache.contains(&4));

        let stats = cache.stats();
        assert_eq!(stats.evictions, 1);
    }

    #[test]
    fn test_lru_order() {
        let mut cache: MemoCache<i32, i32> = MemoCache::with_capacity(3);

        cache.get_or_compute(1, |k| *k);
        cache.get_or_compute(2, |k| *k);
        cache.get_or_compute(3, |k| *k);

        // Access 1 to make it recently used
        cache.get_or_compute(1, |k| *k);

        // Add 4 - should evict 2 (LRU)
        cache.get_or_compute(4, |k| *k);

        assert!(cache.contains(&1));
        assert!(!cache.contains(&2));
        assert!(cache.contains(&3));
        assert!(cache.contains(&4));
    }

    #[test]
    fn test_thread_safe_cache() {
        let cache = Arc::new(ThreadSafeMemoCache::<i32, i32>::new());
        let cache_clone = Arc::clone(&cache);

        let handle = thread::spawn(move || {
            for i in 0..100 {
                cache_clone.get_or_compute(i, |k| k * 2);
            }
        });

        for i in 0..100 {
            cache.get_or_compute(i, |k| k * 2);
        }

        handle.join().unwrap();

        let stats = cache.stats();
        // Some hits should occur due to concurrent access
        assert!(stats.hits > 0 || stats.misses == 200);
    }

    #[test]
    fn test_recursive_memo_fibonacci() {
        let memo = RecursiveMemo::<u32, u64>::new();

        // Define fib as a standalone function for proper recursion
        fn fib(memo: &RecursiveMemo<u32, u64>, n: u32) -> u64 {
            if n <= 1 {
                n as u64
            } else {
                memo.memoize(n - 1, |m, k| fib(m, *k)) + memo.memoize(n - 2, |m, k| fib(m, *k))
            }
        }

        let result = fib(&memo, 20);
        assert_eq!(result, 6765);

        let stats = memo.stats();
        // Should have many hits due to memoization
        println!("Fibonacci stats: hits={}, misses={}", stats.hits, stats.misses);
        assert!(stats.misses < 100); // Much fewer computations than naive recursion
    }

    #[test]
    fn test_memoize_function_wrapper() {
        let mut memoized_factorial = memoize(|n: &u32| -> u64 {
            if *n <= 1 { 1 } else {
                let mut result: u64 = 1;
                for i in 2..=*n { result *= i as u64; }
                result
            }
        });

        assert_eq!(memoized_factorial(5), 120);
        assert_eq!(memoized_factorial(5), 120); // Cached
        assert_eq!(memoized_factorial(10), 3628800);
    }

    #[test]
    fn test_clear_cache() {
        let mut cache: MemoCache<i32, i32> = MemoCache::new();

        cache.get_or_compute(1, |k| *k);
        cache.get_or_compute(2, |k| *k);

        assert_eq!(cache.len(), 2);

        cache.clear();

        assert!(cache.is_empty());
        assert_eq!(cache.stats().hits, 0);
    }

    #[test]
    fn test_hit_rate_calculation() {
        let mut cache: MemoCache<i32, i32> = MemoCache::new();

        // Miss
        cache.get_or_compute(1, |k| *k);
        // Hit
        cache.get_or_compute(1, |k| *k);
        // Hit
        cache.get_or_compute(1, |k| *k);

        assert_eq!(cache.hit_rate(), 66.66666666666666);
    }

    #[test]
    fn test_insert_manual() {
        let mut cache: MemoCache<String, i32> = MemoCache::new();

        cache.insert("test".to_string(), 42);

        assert_eq!(cache.get(&"test".to_string()), Some(&42));
        assert!(cache.contains(&"test".to_string()));
    }

    #[test]
    fn test_remove_entry() {
        let mut cache: MemoCache<i32, i32> = MemoCache::new();

        cache.get_or_compute(1, |k| *k);
        cache.get_or_compute(2, |k| *k);

        let removed = cache.remove(&1);

        assert_eq!(removed, Some(1));
        assert!(!cache.contains(&1));
        assert_eq!(cache.len(), 1);
    }

    #[test]
    fn test_shared_cache() {
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
}