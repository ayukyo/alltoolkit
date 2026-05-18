# LRU Cache Utils - Versatile Least Recently Used Cache Implementations

A comprehensive Python LRU cache library with advanced features, zero external dependencies.

## Features

- 🔄 **Thread-safe Operations** - All caches support concurrent access
- ⏱️ **TTL Support** - Time-to-live expiration for entries
- 📊 **Weight-based Eviction** - Evict by custom weight criteria
- 📈 **Statistics & Monitoring** - Track hits, misses, evictions
- 🎯 **Decorator Interface** - Easy function result caching
- 🏗️ **Multi-level Cache** - L1/L2 tiered caching
- 💾 **Memory-bounded Cache** - Size estimation and memory limits
- 🔧 **Background Refresh** - Automatic stale data refresh

## Installation

No external dependencies required. Just import:

```python
from lru_cache_utils import LRUCache, TTLCache, lru_cache
```

## Quick Start

### Basic LRU Cache

```python
from lru_cache_utils import LRUCache

cache = LRUCache(max_size=100)

# Set and get
cache.set('user_1', {'name': 'Alice'})
user = cache.get('user_1')

# Delete and check
cache.delete('user_1')
cache.contains('user_1')  # False
```

### With TTL (Time-to-Live)

```python
# Default 5-minute TTL
cache = LRUCache(max_size=100, ttl=300)

# Per-entry TTL
cache.set('temp_data', 'value', ttl=60)  # 1 minute
cache.set('permanent', 'value', ttl=None)  # No expiration
```

### Function Caching Decorator

```python
from lru_cache_utils import lru_cache

@lru_cache(maxsize=128, ttl=60)
def expensive_computation(n):
    # ... complex computation ...
    return result

# First call computes, subsequent calls cached
result1 = expensive_computation(100)  # Computes
result2 = expensive_computation(100)  # Cached

# Clear cache
expensive_computation.cache_clear()
```

## Cache Types

### LRUCache

Full-featured LRU cache with TTL and weight support:

```python
cache = LRUCache(
    max_size=1000,          # Maximum entries
    ttl=300,                # Default TTL (seconds)
    max_weight=5000,        # Maximum total weight
    on_evict=lambda k, v: print(f"Evicted: {k}")
)

# Weight-based entries
cache.set('large_data', data, weight=100)
```

### TTLCache

Optimized for TTL-based scenarios:

```python
cache = TTLCache(
    default_ttl=60,         # 1 minute default
    max_size=10000,
    cleanup_interval=30     # Auto cleanup every 30s
)

# Get remaining TTL
remaining = cache.get_ttl('key')

# Extend TTL
cache.extend_ttl('key', 30)
```

### BoundedLRUCache

Memory-aware cache with size estimation:

```python
cache = BoundedLRUCache(max_memory_mb=50)  # 50 MB limit

cache.set('large_object', data)
print(f"Memory usage: {cache.memory_usage_mb()} MB")
```

### MultiLevelCache

Tiered caching (fast L1 + slow L2):

```python
l1 = LRUCache(max_size=100)    # Fast, small
l2 = LRUCache(max_size=10000)  # Slow, large
cache = MultiLevelCache([l1, l2])

# Writes to all levels
cache.set('key', 'value')

# Reads from fastest available, promotes if found in slower level
value = cache.get('key')
```

### CachedFunction

Function wrapper with background refresh:

```python
def fetch_user(user_id):
    return database.query(user_id)

cached_fetch = CachedFunction(
    fetch_user,
    ttl=300,                     # 5-minute cache
    refresh_before_expiry=0.8,   # Refresh at 80% TTL
    background_refresh=True      # Non-blocking refresh
)

user = cached_fetch(123)  # Cached or fresh
```

## Advanced Usage

### Statistics Monitoring

```python
stats = cache.get_stats()
print(f"Hit rate: {stats.hit_rate:.2%}")
print(f"Total requests: {stats.total_requests}")
print(f"Evictions: {stats.evictions}")
print(f"Expired: {stats.expired}")

# Reset statistics
cache.reset_stats()
```

### Get-or-Set Pattern

```python
# Compute only if not cached
value = cache.get_or_set('key', lambda: expensive_operation())
```

### Entry Metadata

```python
entry = cache.get_entry('key')
print(f"Age: {entry.age} seconds")
print(f"Access count: {entry.access_count}")
print(f"Idle time: {entry.idle_time}")
```

### Manual Cleanup

```python
# Remove expired entries
expired_count = cache.prune_expired()
```

### Dict-like Interface

```python
cache['key'] = 'value'
value = cache['key']
del cache['key']
'key' in cache
len(cache)
```

## Thread Safety

All caches are thread-safe by default using RLock:

```python
from threading import Thread

def worker(cache, key):
    cache.set(key, compute_value())

threads = [
    Thread(target=worker, args=(cache, f'key_{i}'))
    for i in range(100)
]
for t in threads:
    t.start()
```

## Performance

| Operation | Time Complexity |
|-----------|-----------------|
| Get | O(1) |
| Set | O(1) |
| Delete | O(1) |
| Contains | O(1) |

Eviction: O(k) where k is number of evicted entries.

## License

MIT License - Part of AllToolkit

## Author

AllToolkit - 2026-05-18