"""
LFU Cache Utils - Usage Examples

Demonstrates practical use cases for the LFU Cache implementation.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mod import (
    LFUCache, LFUCacheBuilder,
    create_lfu_cache, lfu_cache_decorator
)


def example_basic_usage():
    """Basic LFU cache operations."""
    print("=" * 60)
    print("Example 1: Basic Usage")
    print("=" * 60)
    
    cache = LFUCache(capacity=3)
    
    # Add items
    cache.put('apple', 1)
    cache.put('banana', 2)
    cache.put('cherry', 3)
    
    print(f"Initial cache: {cache}")
    print(f"Keys: {cache.keys()}")
    
    # Access items to increase their frequency
    cache.get('apple')  # freq=2
    cache.get('apple')  # freq=3
    cache.get('banana') # freq=2
    
    print(f"\nFrequencies: apple={cache.get_freq('apple')}, "
          f"banana={cache.get_freq('banana')}, cherry={cache.get_freq('cherry')}")
    
    # Add new item - should evict 'cherry' (lowest frequency)
    print("\nAdding 'date' to full cache...")
    evicted = cache.put('date', 4)
    print(f"Evicted: {evicted}")
    print(f"'cherry' in cache: {cache.contains('cherry')}")
    print(f"Final keys: {cache.keys()}")


def example_api_rate_limiting():
    """Using LFU cache for API response caching."""
    print("\n" + "=" * 60)
    print("Example 2: API Response Caching")
    print("=" * 60)
    
    # Simulate an API cache
    api_cache = LFUCache(capacity=100)
    
    # Simulate API calls
    def fetch_user(user_id):
        """Simulate fetching user from API."""
        cached = api_cache.get(user_id)
        if cached is not None:
            print(f"  Cache HIT for user {user_id}")
            return cached
        
        print(f"  Cache MISS - Fetching user {user_id} from API...")
        # Simulate expensive API call
        user_data = {'id': user_id, 'name': f'User{user_id}', 'active': True}
        api_cache.put(user_id, user_data)
        return user_data
    
    # First request - miss
    user1 = fetch_user(101)
    
    # Second request - hit
    user1_again = fetch_user(101)
    
    print(f"\nCache stats: {api_cache.stats}")
    print(f"Hit rate: {api_cache.stats.hit_rate:.1%}")


def example_function_memoization():
    """Using decorator for function memoization."""
    print("\n" + "=" * 60)
    print("Example 3: Function Memoization with Decorator")
    print("=" * 60)
    
    computation_count = {'total': 0}
    
    @lfu_cache_decorator(capacity=50)
    def fibonacci(n):
        """Compute Fibonacci number (expensive without caching)."""
        computation_count['total'] += 1
        if n <= 1:
            return n
        return fibonacci(n - 1) + fibonacci(n - 2)
    
    # First computation
    print("Computing fib(30)...")
    result1 = fibonacci(30)
    print(f"Result: {result1}")
    print(f"Computations performed: {computation_count['total']}")
    
    # Reset counter
    computation_count['total'] = 0
    
    # Second computation - all cached
    print("\nComputing fib(30) again...")
    result2 = fibonacci(30)
    print(f"Result: {result2}")
    print(f"Computations performed: {computation_count['total']} (all cached!)")
    
    print(f"\nCache size: {len(fibonacci.cache)}")
    print(f"Cache stats: {fibonacci.cache_stats()}")


def example_database_query_cache():
    """Using LFU cache for database query results."""
    print("\n" + "=" * 60)
    print("Example 4: Database Query Cache")
    print("=" * 60)
    
    query_cache = LFUCache(capacity=50)
    
    def execute_query(sql, params=None):
        """Simulate database query with caching."""
        # Create cache key from query and params
        key = (sql, tuple(sorted(params.items())) if params else None)
        
        result = query_cache.get(key)
        if result is not None:
            print(f"  [CACHE HIT] {sql[:50]}...")
            return result
        
        print(f"  [EXECUTING] {sql[:50]}...")
        # Simulate query execution
        result = {'data': [1, 2, 3], 'count': 3}
        query_cache.put(key, result)
        return result
    
    # Execute queries
    execute_query("SELECT * FROM users WHERE active = ?", {'active': True})
    execute_query("SELECT * FROM products WHERE category = ?", {'category': 'electronics'})
    execute_query("SELECT * FROM users WHERE active = ?", {'active': True})  # Cached!
    
    print(f"\nQuery cache stats: {query_cache.stats}")


def example_web_session_cache():
    """Using LFU cache for web session storage."""
    print("\n" + "=" * 60)
    print("Example 5: Web Session Cache")
    print("=" * 60)
    
    session_cache = LFUCache(capacity=1000)
    
    def create_session(user_id):
        """Create a new session."""
        session_id = f"sess_{user_id}_{hash(user_id) % 10000}"
        session_data = {
            'user_id': user_id,
            'created_at': '2026-04-30T03:00:00Z',
            'preferences': {'theme': 'dark', 'lang': 'en'}
        }
        session_cache.put(session_id, session_data)
        return session_id
    
    def get_session(session_id):
        """Get session data."""
        return session_cache.get(session_id)
    
    def update_session(session_id, key, value):
        """Update session data."""
        session = session_cache.peek(session_id)
        if session:
            session[key] = value
            # Put updates frequency too
            session_cache.put(session_id, session)
    
    # Create and use sessions
    sess1 = create_session('user_123')
    sess2 = create_session('user_456')
    
    print(f"Created sessions: {sess1}, {sess2}")
    print(f"Session 1 data: {get_session(sess1)}")
    
    update_session(sess1, 'last_action', 'view_dashboard')
    print(f"Updated session 1: {get_session(sess1)}")
    
    print(f"\nSession cache: {session_cache}")


def example_builder_pattern():
    """Using the builder pattern for cache configuration."""
    print("\n" + "=" * 60)
    print("Example 6: Builder Pattern Configuration")
    print("=" * 60)
    
    # Build a cache with specific configuration
    cache = (LFUCacheBuilder()
             .capacity(10)
             .initial_items({
                 'config1': {'value': 100, 'name': 'Max Connections'},
                 'config2': {'value': 30, 'name': 'Timeout (seconds)'},
                 'config3': {'value': True, 'name': 'Debug Mode'},
             })
             .build())
    
    print(f"Built cache: {cache}")
    print(f"Pre-loaded items: {cache.items()}")


def example_cache_monitoring():
    """Monitoring cache performance."""
    print("\n" + "=" * 60)
    print("Example 7: Cache Monitoring")
    print("=" * 60)
    
    cache = LFUCache(capacity=5)
    
    # Simulate usage
    for i in range(20):
        # Some keys are accessed more frequently
        if i % 3 == 0:
            cache.put('hot_key', f'value_{i}')
            cache.get('hot_key')
        cache.put(f'key_{i % 10}', f'value_{i}')
    
    stats = cache.stats
    
    print(f"Cache: {cache}")
    print(f"Current size: {stats.current_size}")
    print(f"Total hits: {stats.hits}")
    print(f"Total misses: {stats.misses}")
    print(f"Total evictions: {stats.evictions}")
    print(f"Hit rate: {stats.hit_rate:.1%}")
    
    # Reset stats
    cache.reset_stats()
    print(f"\nAfter reset: {cache.stats}")


def example_priority_based_eviction():
    """Demonstrating frequency-based priority eviction."""
    print("\n" + "=" * 60)
    print("Example 8: Priority-Based Eviction Demo")
    print("=" * 60)
    
    cache = LFUCache(capacity=4)
    
    # Fill cache
    items = [('A', 1), ('B', 2), ('C', 3), ('D', 4)]
    for key, value in items:
        cache.put(key, value)
    
    print("Initial cache: A, B, C, D (all freq=1)")
    
    # Create different access patterns
    for _ in range(3):
        cache.get('A')  # A becomes freq=4
    for _ in range(2):
        cache.get('B')  # B becomes freq=3
    cache.get('C')  # C becomes freq=2
    # D remains freq=1
    
    print("\nAccess patterns:")
    for key in ['A', 'B', 'C', 'D']:
        print(f"  {key}: frequency = {cache.get_freq(key)}")
    
    # Now add new items - should evict in frequency order
    print("\nAdding E (evicts D with lowest freq):")
    evicted = cache.put('E', 5)
    print(f"  Evicted: {evicted} (was D)")
    
    print("Adding F (evicts C with lowest freq):")
    evicted = cache.put('F', 6)
    print(f"  Evicted: {evicted} (was C)")
    
    print(f"\nFinal cache keys: {cache.keys()}")
    print(f"Frequencies: {[(k, cache.get_freq(k)) for k in cache.keys()]}")


def main():
    """Run all examples."""
    example_basic_usage()
    example_api_rate_limiting()
    example_function_memoization()
    example_database_query_cache()
    example_web_session_cache()
    example_builder_pattern()
    example_cache_monitoring()
    example_priority_based_eviction()
    
    print("\n" + "=" * 60)
    print("All examples completed!")
    print("=" * 60)


if __name__ == '__main__':
    main()