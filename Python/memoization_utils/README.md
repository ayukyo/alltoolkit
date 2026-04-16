# Memoization Utils

A comprehensive function memoization/caching toolkit for Python with zero external dependencies.

## Features

- **Basic Memoize** - Simple function result caching
- **LRU Memoize** - Size-bounded caching with least-recently-used eviction
- **TTL Memoize** - Time-to-live based cache expiration
- **Disk Memoize** - Persistent caching to disk (survives process restarts)
- **Async Memoize** - Caching for async/await functions
- **Method Memoize** - Per-instance caching for class methods
- **Statistics** - Track cache hits, misses, and performance

## Installation

```python
from memoization_utils import (
    memoize, memoize_method, MemoizeStats,
    lru_memoize, lru_memoize_method, clear_lru_caches,
    ttl_memoize, ttl_memoize_method, clear_ttl_caches,
    disk_memoize, disk_memoize_method, clear_disk_cache,
    async_memoize, async_ttl_memoize, async_lru_memoize,
    clear_async_caches,
)
```

## Quick Start

### Basic Memoize

```python
from memoization_utils import memoize

@memoize()
def fibonacci(n):
    if n < 2:
        return n
    return fibonacci(n-1) + fibonacci(n-2)

# First call: computed
fib(20)  # 6765

# Subsequent calls: cached (instant)
fib(20)

# Check cache stats
print(fibonacci.cache_info())
```

### LRU Memoize

```python
from memoization_utils import lru_memoize

@lru_memoize(maxsize=128)
def expensive_computation(x, y):
    return x ** y

result = expensive_computation(100, 50)  # Computed
result = expensive_computation(100, 50)  # Cached

# Get cache statistics
info = expensive_computation.cache_info()
print(f"Hit rate: {info['hit_rate']:.2%}")
print(f"Cache size: {info['size']}/{info['maxsize']}")

# Clear cache
expensive_computation.cache_clear()
```

### TTL Memoize

```python
from memoization_utils import ttl_memoize

@ttl_memoize(ttl=60.0)  # Cache for 60 seconds
def fetch_api_data(endpoint):
    # Simulate API call
    time.sleep(1)
    return {"data": "..."}

data1 = fetch_api_data("/users")  # Slow (1 second)
data2 = fetch_api_data("/users")  # Instant (cached)

time.sleep(61)

data3 = fetch_api_data("/users")  # Slow again (expired)
```

### Disk Memoize

```python
from memoization_utils import disk_memoize

@disk_memoize(cache_dir=".my_cache", ttl=3600)
def process_large_dataset(dataset_id):
    # Expensive processing
    time.sleep(5)
    return load_dataset(dataset_id)

# First run: processes and saves to disk
result = process_large_dataset("dataset_123")

# Even after restarting the program:
result = process_large_dataset("dataset_123")  # Loads from disk!

# Check cache stats
info = process_large_dataset.cache_info()
print(f"Cache size: {info['total_size_mb']:.2f} MB")
```

### Method Memoize

```python
from memoization_utils import memoize_method, lru_memoize_method

class DataProcessor:
    @memoize_method()
    def compute(self, x, y):
        # Per-instance caching
        return x * y + self.multiplier
    
    @lru_memoize_method(maxsize=100)
    def analyze(self, data_id):
        return self._analyze_data(data_id)

processor1 = DataProcessor()
processor2 = DataProcessor()

processor1.compute(5, 10)  # Computed
processor1.compute(5, 10)  # Cached
processor2.compute(5, 10)  # Computed (different instance)

# Clear cache for specific instance
processor1.compute.cache_clear()
```

### Async Memoize

```python
from memoization_utils import async_memoize, async_ttl_memoize

@async_memoize(maxsize=100)
async def fetch_user(user_id):
    async with aiohttp.ClientSession() as session:
        async with session.get(f'/users/{user_id}') as resp:
            return await resp.json()

@async_ttl_memoize(ttl=60.0)
async def get_stock_price(symbol):
    # Cached for 60 seconds
    async with aiohttp.ClientSession() as session:
        async with session.get(f'/stocks/{symbol}') as resp:
            return await resp.json()

# Usage
user = await fetch_user(123)  # Fetched from API
user = await fetch_user(123)  # Cached

# Clear async caches
await clear_async_caches()
```

## Advanced Usage

### Custom Key Function

```python
from memoization_utils import memoize

def custom_key(obj):
    return obj.id if hasattr(obj, 'id') else str(obj)

@memoize(key_func=custom_key)
def process_object(obj):
    return obj.process()
```

### Statistics Tracking

```python
from memoization_utils import memoize, MemoizeStats

stats = MemoizeStats()

@memoize(stats=stats)
def tracked_function(x):
    return x * 2

for i in range(100):
    tracked_function(i % 10)  # Will cache 10 values

print(f"Hits: {stats.hits}")
print(f"Misses: {stats.misses}")
print(f"Hit rate: {stats.hit_rate:.2%}")
print(f"Time saved: {stats.total_time_saved:.3f}s")
```

### Context Managers

```python
from memoization_utils import TTLMemoizeContext, AsyncMemoizeContext

# TTL context
with TTLMemoizeContext(ttl=60.0) as cache:
    @cache.decorate
    def fetch_data(url):
        return requests.get(url).json()
    
    data = fetch_data('/api/data')  # Cached for 60s

# Async context
async with AsyncMemoizeContext(maxsize=100) as cache:
    @cache.decorate
    async def async_fetch(url):
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                return await resp.json()
    
    data = await async_fetch('/api/data')
```

### Hash Keys for Unhashable Args

```python
from memoization_utils import memoize

@memoize(use_hash=True)
def process_list(data):
    # Can cache results for list inputs
    return sum(data)

process_list([1, 2, 3])  # Computed
process_list([1, 2, 3])  # Cached (via hash)
```

## Global Cache Management

```python
from memoization_utils import (
    clear_lru_caches, get_lru_cache_info,
    clear_ttl_caches, get_ttl_cache_info,
    clear_disk_cache, get_disk_cache_stats,
    clear_async_caches,
)

# Clear all caches of each type
clear_lru_caches()
clear_ttl_caches()
clear_disk_cache()
await clear_async_caches()

# Get info about all registered caches
all_lru_info = get_lru_cache_info()
all_ttl_info = get_ttl_cache_info()
all_disk_info = get_disk_cache_stats()
```

## API Reference

### Basic Memoize

| Decorator | Description |
|-----------|-------------|
| `memoize()` | Basic unlimited cache |
| `memoize(maxsize=n)` | Size-limited cache |
| `memoize_method()` | Per-instance caching |

| Parameters | Description |
|------------|-------------|
| `maxsize` | Maximum cache size (None = unlimited) |
| `key_func` | Custom function to generate cache keys |
| `use_hash` | Use hashed keys for unhashable arguments |
| `stats` | MemoizeStats instance for tracking |

### LRU Memoize

| Decorator | Description |
|-----------|-------------|
| `lru_memoize(maxsize)` | LRU-bounded cache |
| `lru_memoize_method(maxsize)` | Per-instance LRU cache |

### TTL Memoize

| Decorator | Description |
|-----------|-------------|
| `ttl_memoize(ttl)` | Time-to-live cache |
| `ttl_memoize_method(ttl)` | Per-instance TTL cache |

| Parameters | Description |
|------------|-------------|
| `ttl` | Time-to-live in seconds |
| `maxsize` | Maximum cache size |

### Disk Memoize

| Decorator | Description |
|-----------|-------------|
| `disk_memoize(cache_dir)` | Persistent disk cache |
| `disk_memoize_method(cache_dir)` | Per-instance disk cache |

| Parameters | Description |
|------------|-------------|
| `cache_dir` | Directory for cache files |
| `ttl` | Time-to-live (None = no expiration) |
| `max_size_mb` | Maximum total cache size in MB |
| `serializer` | "pickle" or "json" |

### Async Memoize

| Decorator | Description |
|-----------|-------------|
| `async_memoize(maxsize)` | LRU cache for async functions |
| `async_ttl_memoize(ttl)` | TTL cache for async functions |
| `async_lru_memoize(maxsize)` | Alias for async_memoize |

## Performance Tips

1. **Use LRU for bounded memory** - Prevents memory leaks with unlimited caches
2. **Use TTL for time-sensitive data** - API responses, stock prices, etc.
3. **Use Disk for large data** - Expensive computations that should persist
4. **Use async_memoize for I/O** - Database/API calls in async code
5. **Track statistics** - Monitor hit rates to tune cache sizes

## Zero Dependencies

Pure Python implementation using only standard library modules:
- `functools` - Decorator utilities
- `threading` - Thread-safe caching
- `asyncio` - Async support
- `pickle` / `json` - Serialization
- `hashlib` - Key hashing
- `pathlib` - File operations

## License

MIT