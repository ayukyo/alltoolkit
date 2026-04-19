//! Usage examples for LRU Cache
//!
//! Run with: cargo run --example usage

use std::time::Duration;
use std::thread;

// Since this is in the examples folder, we would normally use the crate.
// For standalone testing, we'll include the module inline or use the library.
// This example assumes the library structure.

fn main() {
    println!("=== LRU Cache Usage Examples ===\n");

    // Example 1: Basic Usage
    basic_usage();

    // Example 2: Caching Expensive Computations
    cache_expensive_computation();

    // Example 3: Web Page Cache Simulation
    web_page_cache();

    // Example 4: TTL-based Expiration
    ttl_expiration();

    // Example 5: Statistics Tracking
    statistics_tracking();

    // Example 6: Builder Pattern
    builder_pattern();

    println!("\n=== All examples completed ===");
}

fn basic_usage() {
    println!("--- Example 1: Basic Usage ---");

    // Create a cache with capacity 3
    let mut cache = lru_cache::LruCache::new(3);

    // Insert items
    cache.put("apple", 1);
    cache.put("banana", 2);
    cache.put("cherry", 3);

    println!("Cache contents: {:?}", cache.entries());
    println!("Cache size: {}", cache.len());

    // Retrieve an item
    if let Some(value) = cache.get(&"apple") {
        println!("Got 'apple': {}", value);
    }

    // Insert another item - triggers eviction of LRU (banana)
    cache.put("date", 4);
    println!("\nAfter inserting 'date':");
    println!("Contains 'banana': {}", cache.contains_key(&"banana"));
    println!("Contains 'apple': {}", cache.contains_key(&"apple"));

    // Update an existing item
    cache.put("apple", 100);
    println!("\nAfter updating 'apple': {:?}", cache.get(&"apple"));

    // Remove an item
    cache.remove(&"cherry");
    println!("After removing 'cherry', size: {}", cache.len());

    println!();
}

fn cache_expensive_computation() {
    println!("--- Example 2: Caching Expensive Computations ---");

    let mut cache: lru_cache::LruCache<i32, u64> = lru_cache::LruCache::new(100);

    // Simulate Fibonacci cache
    fn fib(n: i32) -> u64 {
        if n <= 1 {
            return n as u64;
        }
        fib(n - 1) + fib(n - 2)
    }

    // Compute and cache Fibonacci numbers
    for n in [10, 20, 30, 10, 20, 40] {
        if let Some(&result) = cache.get(&n) {
            println!("Cache hit for fib({}): {}", n, result);
        } else {
            let result = fib(n);
            cache.put(n, result);
            println!("Computed fib({}): {}", n, result);
        }
    }

    println!("\nCache statistics: {}", cache.stats().summary());
    println!();
}

fn web_page_cache() {
    println!("--- Example 3: Web Page Cache Simulation ---");

    #[derive(Clone, Debug)]
    struct WebPage {
        url: String,
        content: String,
        size_bytes: usize,
    }

    let mut cache: lru_cache::LruCache<String, WebPage> = lru_cache::LruCache::new(3);

    // Simulate caching web pages
    let pages = vec![
        WebPage {
            url: "https://example.com".to_string(),
            content: "Example Domain".to_string(),
            size_bytes: 1024,
        },
        WebPage {
            url: "https://rust-lang.org".to_string(),
            content: "Rust Programming Language".to_string(),
            size_bytes: 2048,
        },
        WebPage {
            url: "https://github.com".to_string(),
            content: "GitHub: Let's build from here".to_string(),
            size_bytes: 3072,
        },
    ];

    for page in &pages {
        cache.put(page.url.clone(), page.clone());
        println!("Cached: {}", page.url);
    }

    // Access example.com to make it recently used
    cache.get(&"https://example.com".to_string());
    println!("\nAccessed example.com (now most recently used)");

    // Add another page - should evict rust-lang.org (LRU)
    let new_page = WebPage {
        url: "https://stackoverflow.com".to_string(),
        content: "Stack Overflow".to_string(),
        size_bytes: 1536,
    };
    cache.put(new_page.url.clone(), new_page);
    println!("\nAdded stackoverflow.com");

    println!("\nCurrent cache contents:");
    for entry in cache.entries() {
        println!("  {} ({} bytes)", entry.key, entry.value.size_bytes);
    }

    println!();
}

fn ttl_expiration() {
    println!("--- Example 4: TTL-based Expiration ---");

    let mut cache = lru_cache::LruCache::new(10);

    // Store items with different TTLs
    cache.put_with_ttl("session_1", "user_data_1", Some(Duration::from_millis(50)));
    cache.put_with_ttl("session_2", "user_data_2", Some(Duration::from_millis(200)));
    cache.put("permanent", "static_data"); // No expiration

    println!("Stored sessions with different TTLs");
    println!("Initial size: {}", cache.len());

    // Wait for first session to expire
    thread::sleep(Duration::from_millis(60));
    println!("\nAfter 60ms:");
    println!("session_1 exists: {}", cache.contains_key(&"session_1"));
    println!("session_2 exists: {}", cache.contains_key(&"session_2"));
    println!("permanent exists: {}", cache.contains_key(&"permanent"));

    // Evict expired entries
    let evicted = cache.evict_expired();
    println!("Evicted {} expired entries", evicted);
    println!("Current size: {}", cache.len());

    println!();
}

fn statistics_tracking() {
    println!("--- Example 5: Statistics Tracking ---");

    let mut cache = lru_cache::LruCache::new(5);

    // Simulate a workload
    for i in 0..10 {
        cache.put(i, i * 2);
    }

    // Mix of hits and misses
    for key in [0, 1, 2, 5, 6, 7, 8, 9] {
        let _ = cache.get(&key);
    }

    let stats = cache.stats();
    println!("Cache statistics:");
    println!("  Hits: {}", stats.hits);
    println!("  Misses: {}", stats.misses);
    println!("  Evictions: {}", stats.evictions);
    println!("  Inserts: {}", stats.inserts);
    println!("  Updates: {}", stats.updates);
    println!("  Hit rate: {:.2}%", stats.hit_rate() * 100.0);

    // Reset stats
    cache.reset_stats();
    println!("\nAfter reset: {} hits, {} misses", cache.stats().hits, cache.stats().misses);

    println!();
}

fn builder_pattern() {
    println!("--- Example 6: Builder Pattern ---");

    let mut cache = lru_cache::LruCacheBuilder::new()
        .capacity(10)
        .build::<&str, i32>();

    cache.put("one", 1);
    cache.put("two", 2);
    cache.put("three", 3);

    println!("Created cache with capacity: {}", cache.capacity());
    println!("Entries: {:?}", cache.entries());

    println!();
}

// Module for standalone compilation
mod lru_cache {
    use std::collections::HashMap;
    use std::time::{Duration, Instant};

    struct Node<K, V> {
        key: K,
        value: V,
        prev: Option<usize>,
        next: Option<usize>,
        created_at: Option<Instant>,
        ttl: Option<Duration>,
    }

    pub struct LruCache<K, V> {
        map: HashMap<K, usize>,
        nodes: Vec<Node<K, V>>,
        head: Option<usize>,
        tail: Option<usize>,
        capacity: usize,
        stats: CacheStats,
    }

    #[derive(Debug, Clone, Default)]
    pub struct CacheStats {
        pub hits: u64,
        pub misses: u64,
        pub evictions: u64,
        pub inserts: u64,
        pub updates: u64,
    }

    impl CacheStats {
        pub fn hit_rate(&self) -> f64 {
            let total = self.hits + self.misses;
            if total == 0 { 0.0 } else { self.hits as f64 / total as f64 }
        }

        pub fn summary(&self) -> String {
            format!(
                "hits: {}, misses: {}, evictions: {}, inserts: {}, updates: {}, hit_rate: {:.2}%",
                self.hits, self.misses, self.evictions, self.inserts, self.updates,
                self.hit_rate() * 100.0
            )
        }
    }

    #[derive(Debug, Clone)]
    pub struct Entry<K, V> {
        pub key: K,
        pub value: V,
    }

    impl<K, V> LruCache<K, V>
    where
        K: std::hash::Hash + Eq + Clone,
        V: Clone,
    {
        pub fn new(capacity: usize) -> Self {
            assert!(capacity > 0, "Capacity must be greater than 0");
            LruCache {
                map: HashMap::with_capacity(capacity),
                nodes: Vec::with_capacity(capacity),
                head: None,
                tail: None,
                capacity,
                stats: CacheStats::default(),
            }
        }

        pub fn len(&self) -> usize { self.map.len() }
        pub fn is_empty(&self) -> bool { self.map.is_empty() }
        pub fn capacity(&self) -> usize { self.capacity }
        pub fn stats(&self) -> &CacheStats { &self.stats }
        pub fn reset_stats(&mut self) { self.stats = CacheStats::default(); }
        pub fn contains_key(&self, key: &K) -> bool {
            self.map.get(key).map_or(false, |&idx| !self.is_expired(idx))
        }
        pub fn lru_key(&self) -> Option<&K> { self.tail.map(|idx| &self.nodes[idx].key) }

        pub fn get(&mut self, key: &K) -> Option<&V> {
            if let Some(&idx) = self.map.get(key) {
                if self.is_expired(idx) {
                    self.remove_by_index(idx);
                    self.stats.misses += 1;
                    return None;
                }
                self.move_to_head(idx);
                self.stats.hits += 1;
                Some(&self.nodes[idx].value)
            } else {
                self.stats.misses += 1;
                None
            }
        }

        pub fn put(&mut self, key: K, value: V) -> Option<V> {
            self.put_with_ttl(key, value, None)
        }

        pub fn put_with_ttl(&mut self, key: K, value: V, ttl: Option<Duration>) -> Option<V> {
            if let Some(&idx) = self.map.get(&key) {
                let old_value = std::mem::replace(&mut self.nodes[idx].value, value);
                self.nodes[idx].created_at = Some(Instant::now());
                self.nodes[idx].ttl = ttl;
                self.move_to_head(idx);
                self.stats.updates += 1;
                Some(old_value)
            } else {
                let evicted = if self.map.len() >= self.capacity { self.evict_lru() } else { None };
                self.insert_new(key, value, ttl);
                self.stats.inserts += 1;
                evicted
            }
        }

        pub fn remove(&mut self, key: &K) -> Option<V> {
            if let Some(&idx) = self.map.get(key) {
                let node = self.remove_node(idx);
                self.map.remove(key);
                Some(node.value)
            } else {
                None
            }
        }

        pub fn clear(&mut self) {
            self.map.clear();
            self.nodes.clear();
            self.head = None;
            self.tail = None;
        }

        pub fn entries(&self) -> Vec<Entry<&K, &V>> {
            let mut entries = Vec::with_capacity(self.map.len());
            let mut current = self.head;
            while let Some(idx) = current {
                entries.push(Entry { key: &self.nodes[idx].key, value: &self.nodes[idx].value });
                current = self.nodes[idx].next;
            }
            entries
        }

        pub fn evict_expired(&mut self) -> usize {
            let expired: Vec<K> = self.nodes.iter().enumerate()
                .filter_map(|(idx, _)| if self.is_expired(idx) { Some(self.nodes[idx].key.clone()) } else { None })
                .collect();
            let count = expired.len();
            for key in expired { self.remove(&key); }
            count
        }

        fn is_expired(&self, idx: usize) -> bool {
            if let Some(ttl) = self.nodes[idx].ttl {
                if let Some(created_at) = self.nodes[idx].created_at {
                    return created_at.elapsed() > ttl;
                }
            }
            false
        }

        fn insert_new(&mut self, key: K, value: V, ttl: Option<Duration>) {
            let new_idx = self.nodes.len();
            let node = Node { key: key.clone(), value, prev: None, next: self.head, created_at: Some(Instant::now()), ttl };
            self.nodes.push(node);
            if let Some(head_idx) = self.head { self.nodes[head_idx].prev = Some(new_idx); }
            self.head = Some(new_idx);
            if self.tail.is_none() { self.tail = Some(new_idx); }
            self.map.insert(key, new_idx);
        }

        fn evict_lru(&mut self) -> Option<V> {
            if let Some(tail_idx) = self.tail {
                self.stats.evictions += 1;
                let node = self.remove_node(tail_idx);
                self.map.remove(&node.key);
                Some(node.value)
            } else { None }
        }

        fn remove_by_index(&mut self, idx: usize) {
            if self.map.contains_key(&self.nodes[idx].key) {
                self.remove_node(idx);
                self.map.remove(&self.nodes[idx].key);
            }
        }

        fn remove_node(&mut self, idx: usize) -> Node<K, V> {
            let node = &self.nodes[idx];
            let prev = node.prev;
            let next = node.next;
            if let Some(prev_idx) = prev { self.nodes[prev_idx].next = next; } else { self.head = next; }
            if let Some(next_idx) = next { self.nodes[next_idx].prev = prev; } else { self.tail = prev; }
            let removed = self.nodes.swap_remove(idx);
            if idx < self.nodes.len() {
                if let Some(p) = self.nodes[idx].prev { self.nodes[p].next = Some(idx); }
                if let Some(n) = self.nodes[idx].next { self.nodes[n].prev = Some(idx); }
                if self.head == Some(self.nodes.len()) { self.head = Some(idx); }
                if self.tail == Some(self.nodes.len()) { self.tail = Some(idx); }
                self.map.insert(self.nodes[idx].key.clone(), idx);
            }
            removed
        }

        fn move_to_head(&mut self, idx: usize) {
            if self.head == Some(idx) { return; }
            let node = &self.nodes[idx];
            let prev = node.prev;
            let next = node.next;
            if let Some(prev_idx) = prev { self.nodes[prev_idx].next = next; }
            if let Some(next_idx) = next { self.nodes[next_idx].prev = prev; } else { self.tail = prev; }
            self.nodes[idx].prev = None;
            self.nodes[idx].next = self.head;
            if let Some(head_idx) = self.head { self.nodes[head_idx].prev = Some(idx); }
            self.head = Some(idx);
        }
    }

    impl<K, V> Default for LruCache<K, V>
    where K: std::hash::Hash + Eq + Clone, V: Clone {
        fn default() -> Self { Self::new(100) }
    }

    pub struct LruCacheBuilder { capacity: usize }

    impl LruCacheBuilder {
        pub fn new() -> Self { LruCacheBuilder { capacity: 100 } }
        pub fn capacity(mut self, capacity: usize) -> Self { self.capacity = capacity; self }
        pub fn build<K, V>(self) -> LruCache<K, V>
        where K: std::hash::Hash + Eq + Clone, V: Clone {
            LruCache::new(self.capacity)
        }
    }

    impl Default for LruCacheBuilder {
        fn default() -> Self { Self::new() }
    }
}