# LFU Cache Utilities

A Least Frequently Used (LFU) cache implementation in pure Go.

## Features

- O(1) get and set operations
- Frequency-based eviction
- Automatic frequency tracking
- Capacity management
- Custom TTL support
- Thread-safe operations
- Multiple frequency tiers
- Batch operations
- Eviction callbacks

## Installation

```bash
go get github.com/AllToolkit/Go/lfu_cache_utils
```

## Usage

```go
package main

import (
    "fmt"
    "time"
    "github.com/AllToolkit/Go/lfu_cache_utils"
)

func main() {
    // Basic cache with capacity
    cache := lfu.New(3)
    cache.Set("apple", 1)
    cache.Set("banana", 2)
    
    v, ok := cache.Get("apple")
    fmt.Printf("Value: %v, Found: %v\n", v, ok)
    
    // With TTL
    cache := lfu.NewWithTTL(3, 100*time.Millisecond)
    
    // With eviction callback
    evicted := make(map[string]interface{})
    cache := lfu.NewWithEvict(2, func(key string, value interface{}) {
        evicted[key] = value
    })
    
    // Batch operations
    items := map[string]interface{}{"k1": 1, "k2": 2}
    lfu.SetMulti(cache, items)
    results := lfu.GetMulti(cache, []string{"k1", "k2"})
}
```

## API Reference

### Cache Functions

- `New(capacity int) *LFUCache` - Create cache with capacity
- `NewWithTTL(capacity int, ttl time.Duration) *LFUCache` - Create cache with TTL
- `NewWithEvict(capacity int, onEvict func(key, value)) *LFUCache` - Create with eviction callback

### Methods

- `Get(key string) (interface{}, bool)` - Retrieve item
- `Set(key string, value interface{})` - Store item
- `SetWithTTL(key string, value interface{}, ttl time.Duration)` - Store with custom TTL
- `Delete(key string) bool` - Remove item
- `Contains(key string) bool` - Check existence
- `Clear()` - Clear all items
- `Len() int` - Item count
- `Keys() []string` - All keys
- `Stats() map[string]interface{}` - Cache statistics
- `Frequency(key string) (int, bool)` - Access frequency
- `Resize(capacity int)` - Change capacity
- `Cleanup() int` - Remove expired items
- `GetMulti(keys []string) map[string]interface{}` - Batch get
- `SetMulti(items map[string]interface{})` - Batch set
- `Update(key string, value interface{}) bool` - Update value
- `Touch(key string) bool` - Update access time

---

**Last updated**: 2026-05-31
