//! Unit tests for LRU Cache

use super::*;
use std::thread;
use std::time::Duration;

#[test]
fn test_basic_operations() {
    let mut cache = LruCache::new(3);

    // Insert
    cache.put("a", 1);
    cache.put("b", 2);
    cache.put("c", 3);

    assert_eq!(cache.len(), 3);
    assert_eq!(cache.get(&"a"), Some(&1));
    assert_eq!(cache.get(&"b"), Some(&2));
    assert_eq!(cache.get(&"c"), Some(&3));
}

#[test]
fn test_eviction() {
    let mut cache = LruCache::new(2);

    cache.put("a", 1);
    cache.put("b", 2);
    cache.put("c", 3); // Should evict "a"

    assert_eq!(cache.len(), 2);
    assert_eq!(cache.get(&"a"), None);
    assert_eq!(cache.get(&"b"), Some(&2));
    assert_eq!(cache.get(&"c"), Some(&3));
}

#[test]
fn test_lru_order() {
    let mut cache = LruCache::new(3);

    cache.put("a", 1);
    cache.put("b", 2);
    cache.put("c", 3);

    // Access "a" to make it most recently used
    cache.get(&"a");

    // Insert "d" - should evict "b" (least recently used)
    cache.put("d", 4);

    assert_eq!(cache.get(&"a"), Some(&1)); // Still present
    assert_eq!(cache.get(&"b"), None); // Evicted
    assert_eq!(cache.get(&"c"), Some(&3));
    assert_eq!(cache.get(&"d"), Some(&4));
}

#[test]
fn test_update_existing() {
    let mut cache = LruCache::new(3);

    cache.put("a", 1);
    cache.put("b", 2);

    // Update existing key
    let old = cache.put("a", 100);
    assert_eq!(old, Some(1));
    assert_eq!(cache.get(&"a"), Some(&100));
    assert_eq!(cache.len(), 2);
}

#[test]
fn test_remove() {
    let mut cache = LruCache::new(3);

    cache.put("a", 1);
    cache.put("b", 2);

    let removed = cache.remove(&"a");
    assert_eq!(removed, Some(1));
    assert_eq!(cache.get(&"a"), None);
    assert_eq!(cache.len(), 1);

    // Remove non-existent
    let removed = cache.remove(&"nonexistent");
    assert_eq!(removed, None);
}

#[test]
fn test_contains_key() {
    let mut cache = LruCache::new(3);

    cache.put("a", 1);
    assert!(cache.contains_key(&"a"));
    assert!(!cache.contains_key(&"b"));
}

#[test]
fn test_clear() {
    let mut cache = LruCache::new(3);

    cache.put("a", 1);
    cache.put("b", 2);
    cache.put("c", 3);

    cache.clear();
    assert_eq!(cache.len(), 0);
    assert!(cache.is_empty());
}

#[test]
fn test_lru_key() {
    let mut cache = LruCache::new(3);

    cache.put("a", 1);
    cache.put("b", 2);
    cache.put("c", 3);

    // "a" is least recently used
    assert_eq!(cache.lru_key(), Some(&"a"));

    // Access "a" makes "b" the LRU
    cache.get(&"a");
    assert_eq!(cache.lru_key(), Some(&"b"));
}

#[test]
fn test_keys_values_entries() {
    let mut cache = LruCache::new(3);

    cache.put("a", 1);
    cache.put("b", 2);
    cache.put("c", 3);

    // Access "a" to make order: a (MRU), c, b (LRU)
    cache.get(&"a");

    let keys: Vec<_> = cache.keys();
    assert_eq!(keys, vec![&"a", &"c", &"b"]);

    let values: Vec<_> = cache.values();
    assert_eq!(values, vec![&1, &3, &2]);

    let entries: Vec<_> = cache.entries();
    assert_eq!(entries.len(), 3);
    assert_eq!(entries[0].key, &"a");
    assert_eq!(entries[0].value, &1);
}

#[test]
fn test_get_mut() {
    let mut cache = LruCache::new(3);

    cache.put("a", 1);
    if let Some(v) = cache.get_mut(&"a") {
        *v += 10;
    }

    assert_eq!(cache.get(&"a"), Some(&11));
}

#[test]
fn test_peek() {
    let mut cache = LruCache::new(3);

    cache.put("a", 1);
    cache.put("b", 2);
    cache.put("c", 3);

    // Peek doesn't update LRU order
    let _ = cache.peek(&"a");

    // Insert should evict "a" (still LRU since peek didn't update)
    cache.put("d", 4);

    assert_eq!(cache.get(&"a"), None);
}

#[test]
fn test_stats() {
    let mut cache = LruCache::new(3);

    cache.put("a", 1);
    cache.put("b", 2);

    cache.get(&"a"); // hit
    cache.get(&"b"); // hit
    cache.get(&"c"); // miss
    cache.get(&"d"); // miss

    let stats = cache.stats();
    assert_eq!(stats.hits, 2);
    assert_eq!(stats.misses, 2);
    assert_eq!(stats.inserts, 2);
    assert!((stats.hit_rate() - 0.5).abs() < 0.001);
}

#[test]
fn test_stats_updates() {
    let mut cache = LruCache::new(3);

    cache.put("a", 1);
    cache.put("a", 2); // Update

    let stats = cache.stats();
    assert_eq!(stats.inserts, 1);
    assert_eq!(stats.updates, 1);
}

#[test]
fn test_stats_evictions() {
    let mut cache = LruCache::new(2);

    cache.put("a", 1);
    cache.put("b", 2);
    cache.put("c", 3); // Eviction

    let stats = cache.stats();
    assert_eq!(stats.evictions, 1);
}

#[test]
fn test_reset_stats() {
    let mut cache = LruCache::new(3);

    cache.put("a", 1);
    cache.get(&"a");

    cache.reset_stats();
    let stats = cache.stats();
    assert_eq!(stats.hits, 0);
    assert_eq!(stats.misses, 0);
}

#[test]
fn test_capacity() {
    let cache: LruCache<i32, i32> = LruCache::new(100);
    assert_eq!(cache.capacity(), 100);
}

#[test]
fn test_default() {
    let cache: LruCache<i32, i32> = LruCache::default();
    assert_eq!(cache.capacity(), 100);
}

#[test]
fn test_builder() {
    let cache = LruCacheBuilder::new()
        .capacity(50)
        .build::<&str, i32>();

    assert_eq!(cache.capacity(), 50);
}

#[test]
fn test_ttl_expiration() {
    let mut cache = LruCache::new(3);

    cache.put_with_ttl("a", 1, Some(Duration::from_millis(10)));
    cache.put("b", 2);

    // Immediately accessible
    assert_eq!(cache.get(&"a"), Some(&1));

    // Wait for expiration
    thread::sleep(Duration::from_millis(20));

    // Should be expired now
    assert_eq!(cache.get(&"a"), None);
    assert_eq!(cache.get(&"b"), Some(&2)); // Still present
}

#[test]
fn test_peek_expired() {
    let mut cache = LruCache::new(3);

    cache.put_with_ttl("a", 1, Some(Duration::from_millis(10)));

    thread::sleep(Duration::from_millis(20));

    // Peek should also return None for expired
    assert_eq!(cache.peek(&"a"), None);
}

#[test]
fn test_contains_key_expired() {
    let mut cache = LruCache::new(3);

    cache.put_with_ttl("a", 1, Some(Duration::from_millis(10)));

    assert!(cache.contains_key(&"a"));

    thread::sleep(Duration::from_millis(20));

    assert!(!cache.contains_key(&"a"));
}

#[test]
fn test_evict_expired() {
    let mut cache = LruCache::new(10);

    cache.put_with_ttl("a", 1, Some(Duration::from_millis(10)));
    cache.put_with_ttl("b", 2, Some(Duration::from_millis(10)));
    cache.put("c", 3); // No TTL

    thread::sleep(Duration::from_millis(20));

    let evicted = cache.evict_expired();
    assert_eq!(evicted, 2);
    assert_eq!(cache.len(), 1);
    assert_eq!(cache.get(&"c"), Some(&3));
}

#[test]
fn test_string_keys() {
    let mut cache = LruCache::new(3);

    cache.put(String::from("hello"), "world");
    cache.put(String::from("foo"), "bar");

    assert_eq!(cache.get(&String::from("hello")), Some(&"world"));
    assert_eq!(cache.get(&String::from("foo")), Some(&"bar"));
}

#[test]
fn test_integer_keys() {
    let mut cache = LruCache::new(3);

    cache.put(1, "one");
    cache.put(2, "two");
    cache.put(3, "three");

    assert_eq!(cache.get(&1), Some(&"one"));
    assert_eq!(cache.get(&2), Some(&"two"));
    assert_eq!(cache.get(&3), Some(&"three"));
}

#[test]
fn test_struct_values() {
    #[derive(Debug, Clone, PartialEq)]
    struct Data {
        id: u32,
        name: String,
    }

    let mut cache = LruCache::new(3);

    cache.put(
        "user1",
        Data {
            id: 1,
            name: "Alice".to_string(),
        },
    );
    cache.put(
        "user2",
        Data {
            id: 2,
            name: "Bob".to_string(),
        },
    );

    let user1 = cache.get(&"user1").unwrap();
    assert_eq!(user1.id, 1);
    assert_eq!(user1.name, "Alice");
}

#[test]
fn test_cache_stats_summary() {
    let mut cache = LruCache::new(3);

    cache.put("a", 1);
    cache.get(&"a");
    cache.get(&"b");

    let summary = cache.stats().summary();
    assert!(summary.contains("hits: 1"));
    assert!(summary.contains("misses: 1"));
    assert!(summary.contains("hit_rate: 50.00%"));
}

#[test]
fn test_large_cache() {
    let mut cache = LruCache::new(1000);

    for i in 0..1000 {
        cache.put(i, i * 2);
    }

    assert_eq!(cache.len(), 1000);
    assert_eq!(cache.get(&500), Some(&1000));

    // Add one more - should evict LRU
    cache.put(1000, 2000);
    assert_eq!(cache.len(), 1000);
    assert_eq!(cache.get(&0), None); // First inserted is evicted
}

#[test]
fn test_zero_capacity_panic() {
    let result = std::panic::catch_unwind(|| {
        let _: LruCache<i32, i32> = LruCache::new(0);
    });
    assert!(result.is_err());
}

#[test]
fn test_update_moves_to_front() {
    let mut cache = LruCache::new(3);

    cache.put("a", 1);
    cache.put("b", 2);
    cache.put("c", 3);

    // Update "a" - should move to front
    cache.put("a", 10);

    // Add new key - should evict "b" (now LRU)
    cache.put("d", 4);

    assert_eq!(cache.get(&"a"), Some(&10));
    assert_eq!(cache.get(&"b"), None);
    assert_eq!(cache.get(&"c"), Some(&3));
    assert_eq!(cache.get(&"d"), Some(&4));
}

#[test]
fn test_multiple_evictions() {
    let mut cache = LruCache::new(2);

    cache.put("a", 1);
    cache.put("b", 2);
    cache.put("c", 3);
    cache.put("d", 4);

    assert_eq!(cache.len(), 2);
    assert_eq!(cache.stats().evictions, 2);
}