"""
AllToolkit - Cache Utils Advanced Examples

Advanced examples demonstrating sophisticated cache patterns and use cases.
"""

import sys
import os
import time
import hashlib

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mod import Cache, cached, CacheStats


def example_cached_decorator():
    """Example: Using @cached decorator for memoization."""
    print("=" * 60)
    print("Example 1: Memoization with @cached Decorator")
    print("=" * 60)
    print()
    
    call_counts = {"fibonacci": 0, "expensive_query": 0}
    
    # Fibonacci with caching
    @cached(ttl=60.0)
    def fibonacci(n):
        call_counts["fibonacci"] += 1
        if n < 2:
            return n
        return fibonacci(n - 1) + fibonacci(n - 2)
    
    print("  Computing fibonacci(10)...")
    result = fibonacci(10)
    print(f"  Result: {result}")
    print(f"  Function calls: {call_counts['fibonacci']}")
    print()
    
    # Expensive database query simulation
    @cached(ttl=30.0)
    def get_user_data(user_id):
        call_counts["expensive_query"] += 1
        time.sleep(0.1)  # Simulate slow query
        return {"id": user_id, "name": f"User_{user_id}", "timestamp": time.time()}
    
    print("  First query for user 123...")
    start = time.time()
    user1 = get_user_data(123)
    print(f"  Time: {(time.time() - start) * 1000:.1f}ms")
    
    print("  Second query for user 123 (cached)...")
    start = time.time()
    user2 = get_user_data(123)
    print(f"  Time: {(time.time() - start) * 1000:.1f}ms")
    
    print(f"  Total queries executed: {call_counts['expensive_query']}")
    print()


def example_multi_level_cache():
    """Example: Implementing a multi-level cache hierarchy."""
    print("=" * 60)
    print("Example 2: Multi-Level Cache Hierarchy")
    print("=" * 60)
    print()
    
    # L1: Fast, small cache (hot data)
    l1_cache = Cache(max_size=10, default_ttl=60.0)
    
    # L2: Larger, slower cache (warm data)
    l2_cache = Cache(max_size=100, default_ttl=300.0)
    
    def get_multi_level(key):
        """Get from L1, fallback to L2, populate both on miss."""
        # Try L1 first
        value = l1_cache.get(key)
        if value is not None:
            return value, "L1"
        
        # Try L2
        value = l2_cache.get(key)
        if value is not None:
            # Promote to L1
            l1_cache.set(key, value)
            return value, "L2"
        
        return None, "MISS"
    
    def set_multi_level(key, value):
        """Set in both caches."""
        l1_cache.set(key, value)
        l2_cache.set(key, value)
    
    # Simulate data source
    data_source = {f"key_{i}": f"value_{i}" for i in range(20)}
    
    # Access pattern
    access_log = {"L1": 0, "L2": 0, "MISS": 0}
    
    print("  Accessing keys 0-9 twice (first time miss, second time L1)...")
    for i in range(10):
        key = f"key_{i}"
        value, source = get_multi_level(key)
        if value is None:
            # Load from "data source"
            value = data_source[key]
            set_multi_level(key, value)
            source = "MISS"
        access_log[source] += 1
    
    print("  Accessing keys 0-9 again (should all be L1)...")
    for i in range(10):
        key = f"key_{i}"
        value, source = get_multi_level(key)
        access_log[source] += 1
    
    print(f"  Access log: {access_log}")
    print(f"  L1 size: {l1_cache.size}, L2 size: {l2_cache.size}")
    print()


def example_rate_limiting():
    """Example: Using cache for rate limiting."""
    print("=" * 60)
    print("Example 3: Rate Limiting with Cache")
    print("=" * 60)
    print()
    
    rate_cache = Cache[int](default_ttl=60.0)  # 1 minute window
    MAX_REQUESTS = 5
    
    def check_rate_limit(user_id):
        """Check if user has exceeded rate limit."""
        key = f"rate_limit:{user_id}"
        count = rate_cache.get(key, 0)
        
        if count >= MAX_REQUESTS:
            return False, count
        
        rate_cache.set(key, count + 1)
        return True, count + 1
    
    # Simulate requests
    user_id = "user_123"
    
    print(f"  Rate limit: {MAX_REQUESTS} requests per minute")
    print(f"  Simulating 7 requests for {user_id}...")
    print()
    
    for i in range(7):
        allowed, count = check_rate_limit(user_id)
        status = "✓ Allowed" if allowed else "✗ Blocked"
        print(f"  Request {i + 1}: {status} (count: {count})")
    
    print()
    
    # Show remaining TTL
    remaining = rate_cache.ttl(f"rate_limit:{user_id}")
    print(f"  Rate limit window expires in: {remaining:.1f}s")
    print()


def example_session_cache():
    """Example: Session management with cache."""
    print("=" * 60)
    print("Example 4: Session Management")
    print("=" * 60)
    print()
    
    session_cache = Cache(max_size=1000, default_ttl=1800.0)  # 30 min sessions
    
    def create_session(user_id):
        """Create a new session."""
        import secrets
        session_id = secrets.token_hex(16)
        
        session_data = {
            "user_id": user_id,
            "created_at": time.time(),
            "last_activity": time.time(),
            "login_count": 1,
        }
        
        session_cache.set(f"session:{session_id}", session_data)
        return session_id
    
    def get_session(session_id):
        """Get session data."""
        return session_cache.get(f"session:{session_id}")
    
    def update_session_activity(session_id):
        """Update last activity time."""
        key = f"session:{session_id}"
        session = session_cache.get(key)
        if session:
            session["last_activity"] = time.time()
            session["login_count"] = session.get("login_count", 0) + 1
            session_cache.set(key, session)
            return True
        return False
    
    def invalidate_session(session_id):
        """Invalidate a session."""
        return session_cache.delete(f"session:{session_id}")
    
    # Create sessions
    print("  Creating sessions...")
    session1 = create_session("alice")
    session2 = create_session("bob")
    print(f"  Session 1: {session1[:8]}...")
    print(f"  Session 2: {session2[:8]}...")
    
    # Update activity
    print()
    print("  Updating session activity...")
    update_session_activity(session1)
    update_session_activity(session1)
    
    session_data = get_session(session1)
    print(f"  Alice's login count: {session_data['login_count']}")
    
    # Invalidate
    print()
    print("  Invalidating Bob's session...")
    invalidate_session(session2)
    print(f"  Bob's session exists: {get_session(session2) is not None}")
    print()


def example_computed_cache():
    """Example: Caching computed/aggregated data."""
    print("=" * 60)
    print("Example 5: Caching Computed Results")
    print("=" * 60)
    print()
    
    result_cache = Cache(default_ttl=300.0)
    
    # Simulated large dataset
    dataset = list(range(10000))
    
    def compute_sum(data_id):
        """Compute sum with caching."""
        cache_key = f"compute:sum:{data_id}"
        
        def do_compute():
            print(f"    [Computing sum for {data_id}...]")
            time.sleep(0.1)  # Simulate computation
            return sum(dataset)
        
        return result_cache.get_or_set(cache_key, do_compute)
    
    def compute_average(data_id):
        """Compute average with caching."""
        cache_key = f"compute:avg:{data_id}"
        
        def do_compute():
            print(f"    [Computing average for {data_id}...]")
            time.sleep(0.1)
            return sum(dataset) / len(dataset)
        
        return result_cache.get_or_set(cache_key, do_compute)
    
    print("  First computation:")
    result1 = compute_sum("dataset_1")
    print(f"  Sum: {result1}")
    
    print()
    print("  Second computation (cached):")
    result2 = compute_sum("dataset_1")
    print(f"  Sum: {result2}")
    
    print()
    print("  Different dataset (new computation):")
    result3 = compute_sum("dataset_2")
    print(f"  Sum: {result3}")
    
    print()
    print(f"  Cache size: {result_cache.size}")
    print()


def example_cache_invalidation():
    """Example: Cache invalidation strategies."""
    print("=" * 60)
    print("Example 6: Cache Invalidation Strategies")
    print("=" * 60)
    print()
    
    cache = Cache(enable_stats=True)
    
    # Pattern-based keys
    def get_user_profile(user_id):
        return cache.get(f"user:profile:{user_id}")
    
    def set_user_profile(user_id, data):
        cache.set(f"user:profile:{user_id}", data, ttl=3600.0)
    
    def get_user_posts(user_id):
        return cache.get(f"user:posts:{user_id}")
    
    def set_user_posts(user_id, posts):
        cache.set(f"user:posts:{user_id}", posts, ttl=600.0)
    
    # Set up some data
    print("  Setting up user data...")
    for i in range(5):
        set_user_profile(i, {"id": i, "name": f"User_{i}"})
        set_user_posts(i, [f"Post_{i}_1", f"Post_{i}_2"])
    
    print(f"  Cache size: {cache.size}")
    
    # Invalidate all user data
    print()
    print("  Invalidating all user:profile:* keys...")
    keys_to_delete = [k for k in cache.keys() if k.startswith("user:profile:")]
    deleted = cache.delete_many(keys_to_delete)
    print(f"  Deleted {deleted} profile keys")
    
    print(f"  Remaining cache size: {cache.size}")
    
    # Show stats
    stats = cache.stats
    print()
    print(f"  Stats: sets={stats.sets}, deletes={stats.deletes}")
    print()


def example_warm_cache():
    """Example: Cache warming strategies."""
    print("=" * 60)
    print("Example 7: Cache Warming")
    print("=" * 60)
    print()
    
    cache = Cache(max_size=100)
    
    # Simulated database
    database = {
        "config:site_name": "MyApp",
        "config:version": "1.0.0",
        "config:max_users": 1000,
        "config:features": ["feature1", "feature2", "feature3"],
    }
    
    def load_from_db():
        """Simulate loading configuration from database."""
        print("    [Loading from database...]")
        time.sleep(0.1)
        return database
    
    def get_config():
        """Get configuration with warming."""
        config = cache.get("config:data")
        if config is None:
            config = load_from_db()
            cache.warm({"config:data": config}, ttl=3600.0)
        return config
    
    print("  First request (cache miss, load from DB)...")
    start = time.time()
    config1 = get_config()
    print(f"  Time: {(time.time() - start) * 1000:.1f}ms")
    
    print()
    print("  Second request (cache hit)...")
    start = time.time()
    config2 = get_config()
    print(f"  Time: {(time.time() - start) * 1000:.1f}ms")
    
    print()
    print(f"  Config site_name: {config2['config:site_name']}")
    print(f"  Config version: {config2['config:version']}")
    print()


def example_thread_safe_counter():
    """Example: Thread-safe distributed counter."""
    print("=" * 60)
    print("Example 8: Thread-Safe Counter")
    print("=" * 60)
    print()
    
    import threading
    
    counter_cache = Cache()
    counter_cache.set("page:home:views", 1000)
    
    def increment_views(page_id, increments=1):
        """Thread-safe view counter."""
        key = f"page:{page_id}:views"
        for _ in range(increments):
            counter_cache.increment(key, 1)
    
    # Simulate concurrent page views
    print("  Simulating 1000 concurrent page views...")
    
    threads = []
    for _ in range(10):
        t = threading.Thread(target=increment_views, args=("home", 100))
        threads.append(t)
        t.start()
    
    for t in threads:
        t.join()
    
    final_count = counter_cache.get("page:home:views")
    print(f"  Final view count: {final_count}")
    print(f"  Expected: 2000 (1000 initial + 1000 new)")
    print()


def main():
    """Run all advanced examples."""
    print()
    print("🧰 AllToolkit - Cache Utils Advanced Examples")
    print()
    
    example_cached_decorator()
    example_multi_level_cache()
    example_rate_limiting()
    example_session_cache()
    example_computed_cache()
    example_cache_invalidation()
    example_warm_cache()
    example_thread_safe_counter()
    
    print("=" * 60)
    print("All advanced examples completed!")
    print("=" * 60)


if __name__ == "__main__":
    main()
