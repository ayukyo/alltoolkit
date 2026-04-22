"""
Token Bucket Examples

Practical examples demonstrating various use cases:
1. API Rate Limiting
2. Web Request Throttling
3. Multi-tenant Rate Limiting
4. Sliding Window API Gateway
"""

import time
import threading
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from token_bucket_utils import (
    TokenBucket,
    ThreadSafeTokenBucket,
    HierarchicalTokenBucket,
    SlidingWindowBucket
)


def example_basic_rate_limiting():
    """
    Example 1: Basic API Rate Limiting
    
    Scenario: API allows 60 requests per minute with burst of 10.
    """
    print("\n=== Example 1: Basic API Rate Limiting ===")
    
    # 60 requests/min = 1 request/sec, burst capacity 10
    bucket = TokenBucket(capacity=10, refill_rate=1.0)
    
    print(f"Initial tokens: {bucket.tokens:.1f}")
    
    # Burst requests
    print("\nSending burst of 10 requests...")
    for i in range(10):
        success = bucket.consume(1)
        print(f"  Request {i+1}: {'✓' if success else '✗'}")
    
    print(f"\nTokens after burst: {bucket.available():.1f}")
    
    # Next request should fail
    success = bucket.consume(1)
    print(f"\nRequest 11: {'✓' if success else '✗ (rate limited)'}")
    
    # Wait for refill
    wait = bucket.wait_time(1)
    print(f"Wait time for next request: {wait:.2f}s")
    
    time.sleep(wait)
    success = bucket.consume(1)
    print(f"Request after wait: {'✓' if success else '✗'}")


def example_thread_safe_throttling():
    """
    Example 2: Thread-Safe Web Request Throttling
    
    Scenario: Web scraper with concurrent workers.
    """
    print("\n=== Example 2: Thread-Safe Throttling ===")
    
    results = {'success': 0, 'limited': 0}
    lock = threading.Lock()
    
    def on_limited(needed, wait_time):
        print(f"  ⚠ Rate limited - need to wait {wait_time:.2f}s")
    
    bucket = ThreadSafeTokenBucket(
        capacity=20,        # Burst capacity
        refill_rate=5,      # 5 requests/sec
        on_limited=on_limited
    )
    
    def worker(worker_id):
        for i in range(5):
            if bucket.consume(1):
                with lock:
                    results['success'] += 1
                print(f"  Worker {worker_id}: Request {i+1} ✓")
            else:
                with lock:
                    results['limited'] += 1
                print(f"  Worker {worker_id}: Request {i+1} ✗ (limited)")
    
    print("Starting 10 workers with 5 requests each...")
    threads = [threading.Thread(target=worker, args=(i,)) for i in range(10)]
    
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    
    print(f"\nResults: {results['success']} succeeded, {results['limited']} limited")


def example_multi_tenant():
    """
    Example 3: Multi-Tenant Rate Limiting
    
    Scenario: SaaS app with global + per-user limits.
    """
    print("\n=== Example 3: Multi-Tenant Rate Limiting ===")
    
    # Create per-user buckets with global limit
    global_bucket = HierarchicalTokenBucket()
    global_bucket.add_level(capacity=1000, refill_rate=100, name="global")
    
    print("Global limit: 1000 burst, 100/sec")
    
    # Simulate 3 users
    users = {
        'alice': HierarchicalTokenBucket(),
        'bob': HierarchicalTokenBucket(),
        'charlie': HierarchicalTokenBucket(),
    }
    
    for name, bucket in users.items():
        bucket.add_level(capacity=100, refill_rate=10, name="global")
        bucket.add_level(capacity=20, refill_rate=2, name=f"user_{name}")
    
    print("Per-user limits: 20 burst, 2/sec")
    
    # Alice makes burst
    print("\nAlice making burst of 15 requests...")
    for i in range(15):
        success, failed = users['alice'].consume(1)
        if not success:
            print(f"  Request {i+1}: ✗ (limited by {failed})")
            break
    
    print(f"Alice status: {users['alice'].status()}")
    
    # Bob tries
    print("\nBob making burst of 25 requests...")
    for i in range(25):
        success, failed = users['bob'].consume(1)
        if not success:
            print(f"  Request {i+1}: ✗ (limited by {failed})")
            break
    
    # Charlie waits and succeeds
    print("\nCharlie making 10 requests (within limit)...")
    for i in range(10):
        success, _ = users['charlie'].consume(1)
        print(f"  Request {i+1}: {'✓' if success else '✗'}")


def example_api_gateway():
    """
    Example 4: API Gateway with Sliding Window
    
    Scenario: Strict API limiting with smooth distribution.
    """
    print("\n=== Example 4: Sliding Window API Gateway ===")
    
    # 100 requests per second with burst of 50
    bucket = SlidingWindowBucket(
        capacity=50,      # Burst capacity
        rate=100,         # 100 requests/sec
        window_size=0.1   # 100ms window (10 requests per window)
    )
    
    print(f"Config: burst={50}, rate={100}/sec, window={0.1}s")
    print(f"Max requests per window: {100 * 0.1}")
    
    # Try burst
    print("\nAttempting burst of 15 requests...")
    for i in range(15):
        success = bucket.consume(1)
        if not success:
            print(f"  Request {i+1}: ✗ (limited)")
            break
    
    print(f"Requests in window: {bucket.requests_in_window()}")
    print(f"Available tokens: {bucket.available():.1f}")
    
    # Show wait time
    wait = bucket.wait_time(5)
    print(f"Wait time for 5 more requests: {wait:.3f}s")


def example_blocking_consumer():
    """
    Example 5: Blocking Consumer Pattern
    
    Scenario: Worker that waits for rate limit.
    """
    print("\n=== Example 5: Blocking Consumer ===")
    
    bucket = ThreadSafeTokenBucket(capacity=5, refill_rate=2)
    
    print("Bucket: capacity=5, rate=2/sec")
    print("\nTrying to consume 10 tokens (blocking with 2s timeout)...")
    
    start = time.time()
    success = bucket.consume_blocking(10, timeout=2.0)
    elapsed = time.time() - start
    
    print(f"Result: {'✓ Success' if success else '✗ Timeout'}")
    print(f"Time elapsed: {elapsed:.2f}s")
    print(f"Tokens available: {bucket.available():.1f}")


def example_rate_limit_decorator():
    """
    Example 6: Rate Limiting Decorator
    
    Scenario: Using token bucket as a function decorator.
    """
    print("\n=== Example 6: Rate Limit Decorator ===")
    
    bucket = TokenBucket(capacity=5, refill_rate=2)
    
    def rate_limited(bucket):
        """Decorator factory for rate limiting."""
        def decorator(func):
            def wrapper(*args, **kwargs):
                if bucket.consume(1):
                    return func(*args, **kwargs)
                else:
                    wait = bucket.wait_time(1)
                    raise Exception(f"Rate limited. Wait {wait:.2f}s")
            return wrapper
        return decorator
    
    @rate_limited(bucket)
    def api_call(endpoint):
        print(f"  Called: {endpoint}")
        return {"status": "ok"}
    
    print("Making 7 API calls with rate limit of 5 burst, 2/sec:")
    
    for i in range(7):
        try:
            result = api_call(f"/endpoint/{i+1}")
            print(f"  Call {i+1}: ✓")
        except Exception as e:
            print(f"  Call {i+1}: ✗ ({e})")


if __name__ == '__main__':
    print("=" * 60)
    print("Token Bucket Rate Limiter Examples")
    print("=" * 60)
    
    example_basic_rate_limiting()
    example_thread_safe_throttling()
    example_multi_tenant()
    example_api_gateway()
    example_blocking_consumer()
    example_rate_limit_decorator()
    
    print("\n" + "=" * 60)
    print("All examples completed!")
    print("=" * 60)