"""
AllToolkit - Cache Utils Basic Usage Examples

Simple examples demonstrating common cache operations.
"""

import sys
import os
import time

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mod import (
    Cache, cached, get_default_cache,
    cache_get, cache_set, cache_delete, cache_clear,
)


def main():
    print("=" * 60)
    print("AllToolkit - Cache Utils Basic Examples")
    print("=" * 60)
    print()
    
    # 1. Basic Cache Operations
    print("1. Basic Cache Operations")
    print("-" * 40)
    cache = Cache()
    
    # Set values
    cache.set("name", "Alice")
    cache.set("age", 30)
    cache.set("city", "Shanghai")
    
    # Get values
    print(f"  Name: {cache.get('name')}")
    print(f"  Age: {cache.get('age')}")
    print(f"  City: {cache.get('city')}")
    
    # Get with default
    country = cache.get("country", "China")
    print(f"  Country (default): {country}")
    
    # Check existence
    print(f"  'name' in cache: {'name' in cache}")
    print(f"  'email' in cache: {'email' in cache}")
    print()
    
    # 2. TTL (Time To Live)
    print("2. TTL Expiration")
    print("-" * 40)
    cache_ttl = Cache(default_ttl=2.0)
    
    cache_ttl.set("temporary", "This will expire", ttl=1.0)
    print(f"  Before expiration: {cache_ttl.get('temporary')}")
    
    print("  Waiting 1.5 seconds...")
    time.sleep(1.5)
    
    result = cache_ttl.get("temporary")
    print(f"  After expiration: {result}")
    print()
    
    # 3. LRU Eviction
    print("3. LRU Eviction (max_size=3)")
    print("-" * 40)
    cache_lru = Cache(max_size=3)
    
    cache_lru.set("first", "1")
    cache_lru.set("second", "2")
    cache_lru.set("third", "3")
    print(f"  Initial keys: {cache_lru.keys()}")
    
    # This will evict "first" (least recently used)
    cache_lru.set("fourth", "4")
    print(f"  After adding 'fourth': {cache_lru.keys()}")
    print(f"  'first' evicted: {'first' not in cache_lru}")
    print()
    
    # 4. Cache Statistics
    print("4. Cache Statistics")
    print("-" * 40)
    cache_stats = Cache(enable_stats=True)
    
    cache_stats.set("a", "1")
    cache_stats.set("b", "2")
    
    cache_stats.get("a")  # Hit
    cache_stats.get("a")  # Hit
    cache_stats.get("b")  # Hit
    cache_stats.get("c")  # Miss
    
    stats = cache_stats.stats
    print(f"  Hits: {stats.hits}")
    print(f"  Misses: {stats.misses}")
    print(f"  Hit Rate: {stats.hit_rate:.2%}")
    print(f"  Total Requests: {stats.hits + stats.misses}")
    print()
    
    # 5. Bulk Operations
    print("5. Bulk Operations")
    print("-" * 40)
    cache_bulk = Cache()
    
    # Set many
    cache_bulk.set_many({
        "user1": "Alice",
        "user2": "Bob",
        "user3": "Charlie",
    })
    print(f"  Set 3 users")
    
    # Get many
    result = cache_bulk.get_many(["user1", "user2", "user4"])
    print(f"  Get many result: {result}")
    
    # Delete many
    deleted = cache_bulk.delete_many(["user1", "user3"])
    print(f"  Deleted {deleted} keys")
    print(f"  Remaining keys: {cache_bulk.keys()}")
    print()
    
    # 6. Atomic Increment/Decrement
    print("6. Atomic Increment/Decrement")
    print("-" * 40)
    cache_counter = Cache()
    
    cache_counter.set("visits", 100)
    print(f"  Initial visits: {cache_counter.get('visits')}")
    
    new_value = cache_counter.increment("visits", 5)
    print(f"  After +5: {new_value}")
    
    new_value = cache_counter.decrement("visits", 3)
    print(f"  After -3: {new_value}")
    print()
    
    # 7. Get or Set (Lazy Loading)
    print("7. Get or Set (Lazy Loading)")
    print("-" * 40)
    cache_lazy = Cache()
    
    call_count = [0]
    
    def expensive_computation():
        call_count[0] += 1
        print("    [Computing value...]")
        return f"Computed result (call #{call_count[0]})"
    
    print("  First call:")
    result1 = cache_lazy.get_or_set("expensive", expensive_computation, ttl=5.0)
    print(f"    Result: {result1}")
    
    print("  Second call (cached):")
    result2 = cache_lazy.get_or_set("expensive", expensive_computation, ttl=5.0)
    print(f"    Result: {result2}")
    print()
    
    # 8. Module-level Convenience Functions
    print("8. Module-level Convenience Functions")
    print("-" * 40)
    
    cache_set("global_key", "global_value")
    print(f"  Set via cache_set: global_key = {cache_get('global_key')}")
    
    cache_delete("global_key")
    print(f"  After delete: {cache_get('global_key')}")
    print()
    
    # 9. Dictionary-style Access
    print("9. Dictionary-style Access")
    print("-" * 40)
    cache_dict = Cache()
    
    cache_dict["key1"] = "value1"
    cache_dict["key2"] = "value2"
    
    print(f"  cache_dict['key1'] = {cache_dict['key1']}")
    print(f"  len(cache_dict) = {len(cache_dict)}")
    
    del cache_dict["key1"]
    print(f"  After del: keys = {cache_dict.keys()}")
    print()
    
    # 10. Cache Export
    print("10. Cache Export")
    print("-" * 40)
    cache_export = Cache(enable_stats=True)
    cache_export.set("item1", "value1", ttl=10.0)
    cache_export.set("item2", "value2")
    
    export = cache_export.to_dict()
    print(f"  Size: {export['size']}")
    print(f"  Max Size: {export['max_size']}")
    print(f"  Items: {list(export['items'].keys())}")
    print(f"  Stats: hits={export['stats']['hits']}, sets={export['stats']['sets']}")
    print()
    
    print("=" * 60)
    print("Examples completed!")
    print("=" * 60)


if __name__ == "__main__":
    main()
