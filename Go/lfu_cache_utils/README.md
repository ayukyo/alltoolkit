# LFU Cache Utils

A thread-safe LFU (Least Frequently Used) cache implementation for Go with O(1) time complexity for Get and Put operations.

## Features

- **O(1) Operations**: Both Get and Put operations run in constant time
- **Thread-Safe**: All operations are protected by mutex locks
- **Generics**: Works with any comparable key type and any value type
- **TTL Support**: Optional time-to-live for automatic expiration
- **LRU Tiebreaker**: When multiple items have the same frequency, the least recently used is evicted
- **Statistics**: Track hits, misses, evictions, and hit rate
- **Export/Import**: Serialize cache contents to JSON
- **Eviction Callback**: Custom callback when items are evicted

## Installation

```bash
go get github.com/ayukyo/alltoolkit/Go/lfu_cache_utils
```

## Usage

### Basic Usage

```go
package main

import (
    "fmt"
    "github.com/ayukyo/alltoolkit/Go/lfu_cache_utils"
)

func main() {
    // Create a cache with capacity 100
    cache := lfu_cache_utils.New[string, int](100)
    
    // Add items
    cache.Put("one", 1)
    cache.Put("two", 2)
    cache.Put("three", 3)
    
    // Get items
    if v, ok := cache.Get("one"); ok {
        fmt.Println("Got:", v) // Got: 1
    }
    
    // Check if exists
    if cache.Contains("two") {
        fmt.Println("Key 'two' exists")
    }
    
    // Delete an item
    cache.Delete("three")
}
```

### With Configuration

```go
cache := lfu_cache_utils.NewWithConfig[string, int](lfu_cache_utils.Config{
    Capacity: 1000,
    TTL:      time.Hour, // Items expire after 1 hour
    OnEvict: func(key string, value int) {
        fmt.Printf("Evicted: %s = %d\n", key, value)
    },
})
```

### Get or Set

```go
// Get existing value or set new one
value, found := cache.GetOrSet("key", 42)

// Get existing value or compute new one
value, found := cache.GetOrCompute("key", func() int {
    return expensiveComputation()
})
```

### Statistics

```go
stats := cache.Stats()
fmt.Printf("Size: %d/%d\n", stats.Size, stats.Capacity)
fmt.Printf("Hit Rate: %.2f%%\n", stats.HitRate * 100)
fmt.Printf("Evictions: %d\n", stats.Evictions)
```

### TTL (Time-to-Live)

```go
// Set cache-wide TTL
cache := lfu_cache_utils.NewWithConfig[string, int](lfu_cache_utils.Config{
    Capacity: 100,
    TTL:      5 * time.Minute,
})

// Or set TTL per item
cache.PutWithTTL("key", 42, 10*time.Second)

// Purge expired items
expired := cache.PurgeExpired()
```

### Iteration

```go
// Iterate over all items
cache.ForEach(func(key string, value int) bool {
    fmt.Printf("%s: %d\n", key, value)
    return true // continue iterating
})

// Get all keys or values
keys := cache.Keys()
values := cache.Values()
```

### Thread Safety

```go
// Safe for concurrent use
var wg sync.WaitGroup

for i := 0; i < 100; i++ {
    wg.Add(1)
    go func(n int) {
        defer wg.Done()
        cache.Put(n, n*10)
        cache.Get(n)
    }(i)
}
wg.Wait()
```

## How It Works

The LFU cache uses a combination of hash maps and doubly linked lists to achieve O(1) complexity:

1. **Hash Map**: Maps keys to cache entries for O(1) lookup
2. **Frequency Lists**: Each frequency level has a doubly linked list of items
3. **Frequency Nodes**: Maps keys to their position in frequency lists for O(1) updates

When accessing an item:
1. Find the item in O(1) via hash map
2. Remove from current frequency list in O(1)
3. Add to next frequency list in O(1)

When evicting:
1. Find minimum frequency list
2. Remove oldest item (front of list) in O(1)

## Performance

Benchmarks on a typical machine:

```
BenchmarkPut-8           10000000   150 ns/op
BenchmarkGet-8           20000000    60 ns/op
BenchmarkConcurrentGet-8  5000000   250 ns/op
BenchmarkConcurrentPut-8  3000000   400 ns/op
```

## API Reference

### Constructor Functions

- `New[K, V](capacity int) *LFUCache[K, V]` - Create a new LFU cache
- `NewWithConfig[K, V](config Config) *LFUCache[K, V]` - Create with custom configuration

### Methods

- `Put(key K, value V)` - Add or update an item
- `PutWithTTL(key K, value V, ttl time.Duration)` - Add with custom TTL
- `Get(key K) (V, bool)` - Get an item (updates frequency)
- `Peek(key K) (V, bool)` - Get without updating frequency
- `Delete(key K) bool` - Remove an item
- `Contains(key K) bool` - Check if key exists
- `Size() int` - Get current size
- `Capacity() int` - Get max capacity
- `Clear()` - Remove all items
- `Resize(newCapacity int)` - Change capacity
- `Keys() []K` - Get all keys
- `Values() []V` - Get all values
- `Stats() Stats` - Get cache statistics
- `GetFrequency(key K) (int, bool)` - Get access frequency
- `PurgeExpired() int` - Remove expired items
- `GetOrSet(key K, value V) (V, bool)` - Get or set value
- `GetOrCompute(key K, compute func() V) (V, bool)` - Get or compute value
- `ForEach(fn func(K, V) bool)` - Iterate over items
- `String() string` - String representation
- `ToJSON() (string, error)` - Export to JSON

## License

MIT License