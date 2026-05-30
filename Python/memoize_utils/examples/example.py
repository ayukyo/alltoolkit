#!/usr/bin/env python3
"""
Example usage for memoize_utils package.
"""

import os
import time
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from mod import LRUCache, TTLCache, memoize, memoize2


def example_lru_cache():
    """Example using LRUCache directly."""
    print("=== LRU Cache Example ===")

    # Create cache with max size of 3
    cache = LRUCache(max_size=3, stats_enabled=True)

    # Set some values
    cache.set("apple", 1)
    cache.set("banana", 2)
    cache.set("cherry", 3)
    print("Initial cache: {}".format(cache.keys()))

    # Access 'apple' to make it recently used
    print("Get apple: {}".format(cache.get("apple")))
    print("After access: {}".format(cache.keys()))

    # Add one more - should evict 'banana' (least recently used)
    cache.set("date", 4)
    print("After adding date: {}".format(cache.keys()))
    print("Has apple: {}".format(cache.has("apple")))
    print("Has banana: {}".format(cache.has("banana")))

    # Stats
    print("Stats: {}".format(cache.get_stats()))


def example_lru_cache_with_ttl():
    """Example using LRU cache with TTL."""
    print("\n=== LRU Cache with TTL ===")

    cache = LRUCache(max_size=10, ttl=0.5)

    cache.set("key1", "value1")
    print("Has key1: {}".format(cache.has("key1")))

    time.sleep(0.6)
    print("After 0.6s - Has key1: {}".format(cache.has("key1")))

    # Custom TTL overrides default
    cache.set("key2", "value2", ttl=2.0)
    time.sleep(0.6)
    print("After 0.6s - Has key2: {}".format(cache.has("key2")))


def example_ttl_cache():
    """Example using simple TTL cache."""
    print("\n=== TTL Cache Example ===")

    cache = TTLCache(ttl=0.3)

    cache.set("token", "abc123")
    print("Has token: {}".format(cache.has("token")))

    time.sleep(0.4)
    print("After 0.4s - Has token: {}".format(cache.has("token")))


def example_memoize_decorator():
    """Example using memoize decorator."""
    print("\n=== Memoize Decorator Example ===")

    call_count = [0]

    @memoize(max_size=100, ttl=60)
    def fibonacci(n):
        call_count[0] += 1
        if n <= 1:
            return n
        return fibonacci(n - 1) + fibonacci(n - 2)

    # First call - computes
    result = fibonacci(10)
    print("fibonacci(10) = {}, calls = {}".format(result, call_count[0]))

    # Second call - cached
    result = fibonacci(10)
    print("fibonacci(10) = {}, calls = {}".format(result, call_count[0]))

    # Different argument - computes
    result = fibonacci(8)
    print("fibonacci(8) = {}, calls = {}".format(result, call_count[0]))


def example_memoize2():
    """Example using memoize2 decorator."""
    print("\n=== Memoize2 Decorator Example ===")

    call_count = [0]

    @memoize2(max_size=100)
    def distance(point1, point2):
        call_count[0] += 1
        (x1, y1), (x2, y2) = point1, point2
        return ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5

    d1 = distance((0, 0), (3, 4))
    print("Distance (0,0) to (3,4) = {}, calls = {}".format(d1, call_count[0]))

    d2 = distance((0, 0), (3, 4))  # Same - cached
    print("Distance (0,0) to (3,4) = {}, calls = {}".format(d2, call_count[0]))

    d3 = distance((1, 1), (4, 5))  # Different - computes
    print("Distance (1,1) to (4,5) = {}, calls = {}".format(d3, call_count[0]))


def example_database_simulation():
    """Simulate a database query cache."""
    print("\n=== Database Query Cache Simulation ===")

    cache = LRUCache(max_size=5, ttl=2.0, stats_enabled=True)

    def simulate_db_query(sql):
        # Check cache first
        result, found = cache.get(sql)
        if found:
            print("[CACHE HIT] {}".format(sql))
            return result

        print("[CACHE MISS - querying DB] {}".format(sql))
        # Simulate expensive query
        time.sleep(0.1)
        result = "Result for: {}".format(sql)
        cache.set(sql, result)
        return result

    # First queries - cache misses
    simulate_db_query("SELECT * FROM users WHERE id = 1")
    simulate_db_query("SELECT * FROM users WHERE id = 2")

    # Same query - cache hit
    simulate_db_query("SELECT * FROM users WHERE id = 1")

    # Stats
    print("\nCache stats: {}".format(cache.get_stats()))


if __name__ == "__main__":
    example_lru_cache()
    example_lru_cache_with_ttl()
    example_ttl_cache()
    example_memoize_decorator()
    example_memoize2()
    example_database_simulation()
    print("\n✅ All examples completed!")