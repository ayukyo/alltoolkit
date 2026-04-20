# CacheUtils - Ruby Memory Cache with LRU Eviction

A lightweight, zero-dependency memory cache implementation for Ruby with TTL support, LRU eviction, and thread safety.

## Features

- **LRU (Least Recently Used) eviction policy** - Automatically removes least recently accessed items when cache is full
- **TTL (Time To Live) support** - Cache entries can expire after a specified time
- **Maximum capacity limits** - Prevent memory overflow with size limits
- **Thread-safe operations** - Safe for use in multi-threaded applications
- **Statistics tracking** - Monitor cache performance with hits, misses, and evictions
- **Zero external dependencies** - Pure Ruby implementation, works with any Ruby version
- **Two cache types**: LRU Cache and Simple Cache (FIFO)

## Installation

No installation required! Just copy the file to your project:

```ruby
require_relative 'cache_utils'
```

## Quick Start

```ruby
require_relative 'cache_utils'

# Create a cache with max 1000 items
cache = CacheUtils::LRUCache.new(max_size: 1000)

# Basic operations
cache.set(:user_123, { name: 'Alice', age: 30 })
user = cache.get(:user_123)
# => { name: 'Alice', age: 30 }

# Using bracket syntax
cache[:config] = { theme: 'dark' }
config = cache[:config]
# => { theme: 'dark' }

# Check if key exists
cache.has_key?(:user_123) # => true

# Delete a key
cache.delete(:user_123)
```

## Usage Examples

### TTL (Time To Live)

```ruby
# Cache expires after 60 seconds
cache.set(:api_token, 'secret123', ttl: 60)

# Or set default TTL for all entries
cache = CacheUtils::LRUCache.new(max_size: 100, default_ttl: 300) # 5 minutes

# Check remaining TTL
info = cache.entry_info(:api_token)
puts info[:remaining_ttl] # => 58.5 (seconds remaining)
```

### Fetch with Block

```ruby
# Fetch from cache, or compute if missing
user = cache.fetch(:user_456, ttl: 60) do
  # This block only runs if :user_456 is not cached
  expensive_database_call(456)
end

# With default TTL
cache = CacheUtils::LRUCache.new(default_ttl: 60)
result = cache.fetch(:expensive_computation) { heavy_calculation }
```

### Increment/Decrement Counters

```ruby
# Atomic increment
cache.increment(:page_views)  # => 1
cache.increment(:page_views)  # => 2
cache.increment(:page_views, 5) # => 7

# Decrement
cache.decrement(:page_views)  # => 6
```

### Multi Operations

```ruby
# Set multiple values at once
cache.set_multi({ a: 1, b: 2, c: 3 })

# Get multiple values
values = cache.get_multi(:a, :b, :d)
# => { a: 1, b: 2 }  # :d is missing, not included
```

### Statistics

```ruby
cache.set(:key1, 'value1')
cache.get(:key1)  # hit
cache.get(:key2)  # miss

stats = cache.stats
puts stats[:hits]      # => 1
puts stats[:misses]    # => 1
puts cache.hit_rate    # => 0.5

# Eviction stats (when cache is full)
small_cache = CacheUtils::LRUCache.new(max_size: 2)
small_cache.set(:a, 1)
small_cache.set(:b, 2)
small_cache.set(:c, 3)  # evicts :a
puts small_cache.stats[:evictions]  # => 1
```

### Module-level Convenience Methods

```ruby
# Use a global default cache
CacheUtils.set(:key, 'value')
CacheUtils.get(:key)  # => 'value'

result = CacheUtils.fetch(:data) { compute_expensive_thing }
CacheUtils.delete(:key)
CacheUtils.clear

# Reset to a fresh cache
CacheUtils.reset_default_cache!
```

### Two Cache Types

#### LRUCache (Recommended)

```ruby
# Evicts least recently used items when full
cache = CacheUtils::LRUCache.new(max_size: 100)

cache.set(:a, 1)
cache.set(:b, 2)
cache.set(:c, 3)
cache.get(:a)  # Access :a, making it most recently used

cache.set(:d, 4)  # Evicts :b (least recently used), not :a
```

#### SimpleCache (Faster for small caches)

```ruby
# Uses FIFO eviction (first in, first out)
# Simpler data structure, slightly faster for small caches
cache = CacheUtils::SimpleCache.new(max_size: 100)

cache.set(:a, 1)
cache.set(:b, 2)
cache.set(:c, 3)
cache.set(:d, 4)  # Evicts :a (oldest entry)
```

### Factory Methods

```ruby
lru = CacheUtils.create_lru_cache(max_size: 500, default_ttl: 60)
simple = CacheUtils.create_simple_cache(max_size: 100)
```

## API Reference

### LRUCache

| Method | Description |
|--------|-------------|
| `get(key)` | Get value by key |
| `set(key, value, ttl: nil)` | Set value with optional TTL |
| `fetch(key, ttl: nil) { block }` | Get or compute |
| `delete(key)` | Remove key from cache |
| `has_key?(key)` | Check if key exists and not expired |
| `clear` | Remove all entries |
| `size` | Current number of entries |
| `keys` | Array of all keys |
| `values` | Array of all values |
| `stats` | Hash with `:hits`, `:misses`, `:evictions` |
| `hit_rate` | Float between 0.0 and 1.0 |
| `entry_info(key)` | Get detailed info about an entry |
| `touch(key, ttl: nil)` | Update TTL for existing key |
| `increment(key, delta, ttl: nil)` | Atomic increment |
| `decrement(key, delta, ttl: nil)` | Atomic decrement |
| `get_multi(*keys)` | Get multiple keys at once |
| `set_multi(hash, ttl: nil)` | Set multiple keys at once |
| `cleanup` | Remove all expired entries |

### SimpleCache

Same API as LRUCache, but uses FIFO eviction instead of LRU.

## Thread Safety

Both cache types are thread-safe. All public methods are synchronized using a mutex.

```ruby
# Safe for concurrent access
threads = 10.times.map do |i|
  Thread.new do
    100.times { |j| cache.set("key_#{i}_#{j}", j) }
  end
end
threads.each(&:join)
```

## Performance Tips

1. **Choose the right size**: Set `max_size` based on expected memory usage
2. **Use appropriate TTL**: Balance between freshness and cache hit rate
3. **Monitor stats**: Check `hit_rate` to tune your caching strategy
4. **Use SimpleCache for small caches**: Simpler structure, slightly faster

## License

MIT License - Part of AllToolkit

## Author

AllToolkit - Automated Tool Generation System
Date: 2026-04-20