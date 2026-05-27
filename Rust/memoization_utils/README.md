# Memoization Utilities for Rust

A comprehensive memoization (caching) library for Rust, enabling efficient caching of computation results to avoid redundant work.

## Features

- **Basic Memoization Cache** - Simple cache with `get_or_compute` pattern
- **LRU Eviction** - Automatic eviction of least recently used entries when capacity limit is reached
- **Thread-Safe Support** - `ThreadSafeMemoCache` using `RwLock` for concurrent access
- **Shared Cache** - `Arc<Mutex>` based cache for sharing across threads
- **Recursive Memoization** - `RecursiveMemo` for memoizing recursive functions (Fibonacci, factorial, etc.)
- **Statistics Tracking** - Track hits, misses, evictions, and hit rate
- **Zero External Dependencies** - Pure Rust standard library implementation

## Installation

Add to your `Cargo.toml`:

```toml
[dependencies]
memoization_utils = "0.1.0"
```

## Quick Start

### Basic Usage

```rust
use memoization_utils::MemoCache;

let mut cache = MemoCache::new();

// First call computes the value
let result = cache.get_or_compute(5, |k| k * k);
// result = 25

// Second call returns cached value
let cached = cache.get_or_compute(5, |k| 0); // Would return 0 if not cached
// cached = 25 (still cached)

println!("Hit rate: {:.2}%", cache.hit_rate());
```

### Capacity-Limited Cache with LRU

```rust
use memoization_utils::MemoCache;

let mut cache = MemoCache::with_capacity(3);

cache.get_or_compute(1, |_| "first");
cache.get_or_compute(2, |_| "second");
cache.get_or_compute(3, |_| "third");

// Access 1 to make it recently used
cache.get_or_compute(1, |_| "");

// Add fourth item - evicts 2 (LRU)
cache.get_or_compute(4, |_| "fourth");

assert!(cache.contains(&1));   // Still cached
assert!(!cache.contains(&2));  // Evicted
```

### Recursive Fibonacci

```rust
use memoization_utils::RecursiveMemo;

let memo = RecursiveMemo::<u32, u64>::new();

fn fib(memo: &RecursiveMemo<u32, u64>, n: u32) -> u64 {
    if n <= 1 {
        n as u64
    } else {
        memo.memoize(n - 1, |m, k| fib(m, *k)) + memo.memoize(n - 2, |m, k| fib(m, *k))
    }
}

println!("fib(30) = {}", fib(&memo, 30));
println!("Computations: {}", memo.stats().misses); // Only 31, not millions!
```

### Thread-Safe Cache

```rust
use memoization_utils::ThreadSafeMemoCache;
use std::sync::Arc;
use std::thread;

let cache = Arc::new(ThreadSafeMemoCache::<i32, i32>::new());

let cache_clone = Arc::clone(&cache);
thread::spawn(move || {
    cache_clone.get_or_compute(5, |k| *k * *k);
});
```

### Function Wrapper

```rust
use memoization_utils::memoize;

let mut factorial = memoize(|n: &u32| -> u64 {
    if *n <= 1 { 1 } else {
        let mut result: u64 = 1;
        for i in 2..=*n { result *= i as u64; }
        result
    }
});

println!("5! = {}", factorial(5));   // Computes
println!("5! = {}", factorial(5));   // Cached
```

## API Reference

### `MemoCache<K, V>`

| Method | Description |
|--------|-------------|
| `new()` | Create unlimited capacity cache |
| `with_capacity(n)` | Create cache with LRU eviction |
| `get_or_compute(key, f)` | Get cached or compute new value |
| `get(&key)` | Get cached value if exists |
| `contains(&key)` | Check if key is cached |
| `insert(key, value)` | Manually insert value |
| `remove(&key)` | Remove entry from cache |
| `clear()` | Clear all entries |
| `len()` | Number of cached entries |
| `stats()` | Get CacheStats (hits, misses, evictions) |
| `hit_rate()` | Hit rate percentage (0.0-100.0) |

### `ThreadSafeMemoCache<K, V>`

Thread-safe version using `RwLock`. Same API but all methods are thread-safe.

### `RecursiveMemo<K, V>`

For memoizing recursive functions with a `memoize(key, compute)` method that takes a closure receiving the memo reference for recursive calls.

### `memoize(f)` / `memoize_with_capacity(n, f)`

Create a memoized function wrapper.

## Statistics

Track cache efficiency:

```rust
let stats = cache.stats();
println!("Hits: {}", stats.hits);
println!("Misses: {}", stats.misses);
println!("Evictions: {}", stats.evictions);
println!("Hit rate: {:.2}%", cache.hit_rate());
```

## Performance

Memoization can dramatically improve performance for repeated expensive computations:

```
Without memoization: 11.17ms
With memoization: 437µs
Speedup: ~25x
```

## License

MIT License