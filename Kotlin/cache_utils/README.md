# Cache Utilities for Kotlin

A comprehensive caching library with zero external dependencies, providing multiple cache strategies for different use cases.

## Features

- **LRU Cache**: Least Recently Used eviction strategy
- **TTL Cache**: Time-To-Live based expiration
- **LFU Cache**: Least Frequently Used eviction strategy
- **Two-Level Cache**: Combined LRU + TTL for multi-tier caching
- **MemoCache**: Function result memoization

## Installation

Simply copy `CacheUtils.kt` to your project. No external dependencies required.

## Quick Start

### LRU Cache

```kotlin
import cache_utils.*

val cache = LRUCache<String, User>(capacity = 100)

cache.put("user:1", User("Alice"))
val user = cache.get("user:1") // Returns User("Alice") or null

// With eviction callback
val cacheWithCallback = LRUCache<String, User>(capacity = 100) { key, value ->
    println("Evicted: $key")
}
```

### TTL Cache

```kotlin
import cache_utils.*

// Default 1 minute TTL
val cache = TTLCache<String, Session>(defaultTtlMs = 60_000L, maxSize = 1000)

cache.put("session:abc", session)
cache.put("session:xyz", session, 30_000L) // Custom 30 second TTL

// Auto-expires when accessed after TTL
val session = cache.get("session:abc") // null if expired
```

### LFU Cache

```kotlin
import cache_utils.*

val cache = LFUCache<String, Data>(capacity = 50)

cache.put("hot-data", data)
repeat(10) { cache.get("hot-data") } // Increase access frequency

// Least frequently accessed items are evicted first
```

### Two-Level Cache

```kotlin
import cache_utils.*

val cache = TwoLevelCache<String, Data>(
    lruCapacity = 100,    // Fast access layer
    ttlCapacity = 1000,   // Larger storage layer
    defaultTtlMs = 300_000L // 5 minutes
)

cache.put("key", data)
cache.put("key", data, 60_000L) // With custom TTL
```

### MemoCache (Function Memoization)

```kotlin
import cache_utils.*

val fibCache = MemoCache<Int, Long> { n ->
    // Expensive computation - only runs once per input
    computeFibonacci(n)
}

val result = fibCache.get(20) // Computes and caches
val cached = fibCache.get(20) // Returns cached result
```

## API Reference

### LRUCache

| Method | Description |
|--------|-------------|
| `put(key, value)` | Store a value |
| `get(key)` | Retrieve a value (returns null if not found) |
| `remove(key)` | Remove a value |
| `contains(key)` | Check if key exists |
| `clear()` | Clear all entries |
| `size` | Current cache size |
| `getStats()` | Get cache statistics |

### TTLCache

| Method | Description |
|--------|-------------|
| `put(key, value)` | Store with default TTL |
| `put(key, value, ttlMs)` | Store with custom TTL |
| `get(key)` | Retrieve value (returns null if expired) |
| `remove(key)` | Remove a value |
| `contains(key)` | Check if key exists and is not expired |
| `cleanupExpired()` | Remove all expired entries |
| `clear()` | Clear all entries |
| `size` | Current cache size |
| `getStats()` | Get cache statistics including eviction count |

### LFUCache

| Method | Description |
|--------|-------------|
| `put(key, value)` | Store a value |
| `get(key)` | Retrieve and increment access frequency |
| `remove(key)` | Remove a value |
| `contains(key)` | Check if key exists |
| `clear()` | Clear all entries |
| `size` | Current cache size |
| `getStats()` | Get cache statistics |

### TwoLevelCache

| Method | Description |
|--------|-------------|
| `put(key, value)` | Store in both levels |
| `put(key, value, ttlMs)` | Store with custom TTL |
| `get(key)` | Get from L1, then L2 (promotes to L1) |
| `remove(key)` | Remove from both levels |
| `clear()` | Clear both levels |
| `getStats()` | Get combined statistics |

### MemoCache

| Method | Description |
|--------|-------------|
| `get(key)` | Get cached result or compute and cache |
| `contains(key)` | Check if key is cached |
| `clear()` | Clear all cached results |
| `size` | Current cache size |

## Cache Statistics

All caches provide statistics:

```kotlin
data class CacheStats(
    val size: Int,
    val capacity: Int,
    val hits: Long,
    val misses: Long,
    val hitRate: Double
)

data class TTLCacheStats(
    val size: Int,
    val maxSize: Int,
    val hits: Long,
    val misses: Long,
    val hitRate: Double,
    val evictions: Long,
    val defaultTtlMs: Long
)
```

## Thread Safety

All cache implementations are thread-safe using:
- `ConcurrentHashMap` for storage
- `ReentrantLock` for compound operations
- Atomic counters for statistics

## Performance Characteristics

| Cache Type | Put | Get | Memory |
|------------|-----|-----|--------|
| LRU | O(1) | O(1) | O(capacity) |
| TTL | O(1) | O(1) | O(maxSize) |
| LFU | O(1) avg | O(1) | O(capacity) |
| Two-Level | O(1) | O(1) | O(L1+L2) |

## Use Cases

- **LRU Cache**: Recent data access patterns, navigation history, recent files
- **TTL Cache**: Session management, API response caching, temporary data
- **LFU Cache**: Hot data patterns, popular content caching, leaderboard data
- **Two-Level Cache**: Multi-tier caching, CDN-like patterns
- **MemoCache**: Expensive computations, recursive algorithms, API deduplication

## Testing

Run tests with:

```bash
kotlinc -cp CacheUtils.kt:CacheUtilsTest.kt -script CacheUtilsTest.kt
```

Or with Gradle/Maven using JUnit.

## License

MIT License - Part of AllToolkit Project