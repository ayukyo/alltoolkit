"""
LRU Cache Utility Module - Usage Examples

This file demonstrates various use cases for the LRU cache implementation.
"""

import sys
import os
import time

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from lru_cache_utils.mod import (
    LRUCache, lru_cache, memoize, TTLCache
)


def example_basic_usage():
    """Example: Basic LRU cache usage."""
    print("\n=== Basic Usage ===\n")
    
    # Create a cache with capacity of 3
    cache = LRUCache[str, int](capacity=3)
    
    # Add items
    cache.put('a', 1)
    cache.put('b', 2)
    cache.put('c', 3)
    print(f"Added: a=1, b=2, c=3")
    print(f"Cache items (LRU order): {cache.items()}")
    
    # Access 'a' to make it most recently used
    cache.get('a')
    print(f"\nAccessed 'a'")
    
    # Add a new item - 'b' should be evicted (least recently used)
    cache.put('d', 4)
    print(f"Added d=4")
    print(f"Cache items: {cache.items()}")
    
    # Check eviction
    print(f"\nIs 'b' in cache? {cache.contains('b')}")
    print(f"Is 'a' in cache? {cache.contains('a')}")


def example_ttl_expiration():
    """Example: TTL (Time-To-Live) expiration."""
    print("\n=== TTL Expiration ===\n")
    
    # Create cache with 2 second TTL
    cache = LRUCache[str, str](capacity=10, ttl=2.0)
    
    cache.put('session', 'user123')
    print(f"Added session: {cache.get('session')}")
    
    print(f"Waiting 1.5 seconds...")
    time.sleep(1.5)
    print(f"Session still valid: {cache.get('session')}")
    
    print(f"Waiting another 1 second...")
    time.sleep(1.0)
    print(f"Session expired: {cache.get('session')}")


def example_eviction_callback():
    """Example: Eviction callback for cleanup."""
    print("\n=== Eviction Callback ===\n")
    
    evicted_items = []
    
    def on_evict(key, value):
        print(f"  Evicted: {key} = {value}")
        evicted_items.append((key, value))
    
    cache = LRUCache[str, int](capacity=3, on_evict=on_evict)
    
    print("Adding items to cache:")
    cache.put('a', 1)
    cache.put('b', 2)
    cache.put('c', 3)
    cache.put('d', 4)  # Triggers eviction of 'a'
    cache.put('e', 5)  # Triggers eviction of 'b'
    
    print(f"\nTotal evictions: {len(evicted_items)}")


def example_statistics():
    """Example: Cache statistics."""
    print("\n=== Cache Statistics ===\n")
    
    cache = LRUCache[str, int](capacity=5)
    
    # Populate cache
    for i in range(5):
        cache.put(f'key{i}', i * 10)
    
    # Generate hits and misses
    cache.get('key0')  # hit
    cache.get('key1')  # hit
    cache.get('key2')  # hit
    cache.get('missing')  # miss
    cache.get('key0')  # hit
    
    stats = cache.stats()
    print("Cache Statistics:")
    for key, value in stats.items():
        if isinstance(value, float):
            print(f"  {key}: {value:.2%}" if 'rate' in key else f"  {key}: {value:.4f}")
        else:
            print(f"  {key}: {value}")


def example_decorator():
    """Example: Using the lru_cache decorator."""
    print("\n=== LRU Cache Decorator ===\n")
    
    call_count = 0
    
    @lru_cache(capacity=100)
    def fibonacci(n):
        nonlocal call_count
        call_count += 1
        if n < 2:
            return n
        return fibonacci(n - 1) + fibonacci(n - 2)
    
    print("Calculating fibonacci(20):")
    result = fibonacci(20)
    print(f"  Result: {result}")
    print(f"  Function calls: {call_count}")
    
    # Without caching, fibonacci(20) would need 21891 recursive calls
    print(f"  Cache stats: {fibonacci.cache_stats()}")


def example_get_or_set():
    """Example: get_or_set for lazy computation."""
    print("\n=== Get or Set Pattern ===\n")
    
    cache = LRUCache[str, dict](capacity=10)
    
    compute_count = 0
    
    def expensive_computation(key):
        nonlocal compute_count
        compute_count += 1
        print(f"  Computing value for '{key}'...")
        time.sleep(0.1)  # Simulate expensive operation
        return {'data': f'value_{key}', 'computed_at': time.time()}
    
    # First access - computes
    print("First access:")
    result1 = cache.get_or_set('user:123', lambda: expensive_computation('user:123'))
    print(f"  Result: {result1}")
    
    # Second access - cached
    print("\nSecond access (cached):")
    result2 = cache.get_or_set('user:123', lambda: expensive_computation('user:123'))
    print(f"  Result: {result2}")
    
    print(f"\nTotal computations: {compute_count}")


def example_thread_safe():
    """Example: Thread-safe cache."""
    print("\n=== Thread-Safe Cache ===\n")
    
    import threading
    
    cache = LRUCache[int, int](capacity=100, thread_safe=True)
    
    def worker(worker_id, count):
        for i in range(count):
            key = worker_id * 1000 + i
            cache.put(key, key * 2)
            cache.get(key)
    
    threads = [
        threading.Thread(target=worker, args=(i, 50))
        for i in range(10)
    ]
    
    print("Running 10 threads with 50 operations each...")
    start = time.time()
    
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    
    elapsed = time.time() - start
    print(f"Completed in {elapsed:.4f} seconds")
    print(f"Final cache size: {cache.size()}")


def example_api_cache():
    """Example: Simulating API response cache."""
    print("\n=== API Response Cache ===\n")
    
    # Simulate API cache with 5-minute TTL
    api_cache = LRUCache[str, dict](capacity=1000, ttl=300)
    
    def fetch_user(user_id):
        # Check cache first
        cached = api_cache.get(user_id)
        if cached is not None:
            print(f"  Cache hit for user {user_id}")
            return cached
        
        # Simulate API call
        print(f"  Fetching user {user_id} from API...")
        user_data = {
            'id': user_id,
            'name': f'User {user_id}',
            'email': f'user{user_id}@example.com'
        }
        
        # Cache for 5 minutes (300 seconds)
        api_cache.put(user_id, user_data)
        return user_data
    
    print("First request:")
    user1 = fetch_user('user123')
    
    print("\nSecond request (should be cached):")
    user2 = fetch_user('user123')
    
    print(f"\nSame data? {user1 == user2}")


def example_rate_limiting():
    """Example: Using cache for rate limiting."""
    print("\n=== Rate Limiting with Cache ===\n")
    
    # Cache to track request counts per IP
    # TTL of 60 seconds for rate limit window
    rate_cache = LRUCache[str, list](capacity=10000, ttl=60, thread_safe=True)
    
    def check_rate_limit(ip, max_requests=5):
        """Check if IP has exceeded rate limit."""
        now = time.time()
        
        # Get existing timestamps or create new list
        timestamps = rate_cache.get(ip, [])
        
        # Filter to only recent requests
        recent = [ts for ts in timestamps if now - ts < 60]
        
        if len(recent) >= max_requests:
            return False, len(recent)
        
        # Add new request
        recent.append(now)
        rate_cache.put(ip, recent)
        
        return True, len(recent)
    
    print("Simulating requests from IP 192.168.1.1:")
    for i in range(7):
        allowed, count = check_rate_limit('192.168.1.1', max_requests=5)
        status = "ALLOWED" if allowed else "BLOCKED"
        print(f"  Request {i+1}: {status} (count: {count})")


def example_memoization():
    """Example: Simple memoization."""
    print("\n=== Simple Memoization ===\n")
    
    @memoize
    def expensive_function(n):
        print(f"  Computing expensive_function({n})...")
        time.sleep(0.1)
        return sum(range(n))
    
    print("First call:")
    result1 = expensive_function(1000)
    print(f"  Result: {result1}")
    
    print("\nSecond call (memoized):")
    result2 = expensive_function(1000)
    print(f"  Result: {result2}")


def example_ttl_cache():
    """Example: TTL-only cache (no LRU eviction)."""
    print("\n=== TTL-Only Cache ===\n")
    
    # Cache that only expires based on time, not usage
    cache = TTLCache[str, str](ttl=2.0)
    
    cache.put('temp_token', 'abc123')
    print(f"Stored temp_token: {cache.get('temp_token')}")
    
    print("Waiting 2.5 seconds...")
    time.sleep(2.5)
    
    print(f"After expiry: {cache.get('temp_token')}")


def example_batch_operations():
    """Example: Batch operations."""
    print("\n=== Batch Operations ===\n")
    
    cache = LRUCache[str, int](capacity=100)
    
    # Put multiple items at once
    items = {f'key{i}': i * 10 for i in range(10)}
    cache.put_all(items)
    print(f"Added {len(items)} items")
    
    # Get multiple items at once
    keys = ['key0', 'key2', 'key4', 'key999']
    result = cache.get_all(keys)
    print(f"Retrieved {len(result)} items: {result}")


def main():
    """Run all examples."""
    print("="*60)
    print("LRU Cache Utility Module - Usage Examples")
    print("="*60)
    
    example_basic_usage()
    example_ttl_expiration()
    example_eviction_callback()
    example_statistics()
    example_decorator()
    example_get_or_set()
    example_thread_safe()
    example_api_cache()
    example_rate_limiting()
    example_memoization()
    example_ttl_cache()
    example_batch_operations()
    
    print("\n" + "="*60)
    print("All examples completed!")
    print("="*60)


if __name__ == '__main__':
    main()