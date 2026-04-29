"""
Test suite for semaphore_utils module.

Tests all semaphore implementations including:
- Semaphore (basic counting semaphore)
- WeightedSemaphore
- SemaphorePool
- AsyncSemaphore
- AsyncWeightedSemaphore
- BoundedSemaphore
- PrioritySemaphore
- RateLimiter
- ConcurrencyLimit

Author: AllToolkit
Date: 2026-04-29
"""

import threading
import time
import asyncio
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from semaphore_utils.semaphore_utils import (
    Semaphore,
    WeightedSemaphore,
    SemaphorePool,
    AsyncSemaphore,
    AsyncWeightedSemaphore,
    BoundedSemaphore,
    PrioritySemaphore,
    RateLimiter,
    ConcurrencyLimit,
    TimeoutError,
    acquire_all,
    run_with_semaphore,
)


def test_semaphore_basic():
    """Test basic semaphore operations."""
    print("Testing Semaphore basic operations...")
    
    sem = Semaphore(3)
    
    # Initial state
    assert sem.capacity == 3
    assert sem.available() == 3
    assert sem.in_use() == 0
    print("  ✓ Initial state correct")
    
    # Acquire and release
    assert sem.acquire()
    assert sem.in_use() == 1
    assert sem.available() == 2
    print("  ✓ Acquire works")
    
    # Try acquire
    assert sem.try_acquire()
    assert sem.in_use() == 2
    print("  ✓ TryAcquire works")
    
    # Try acquire again
    assert sem.try_acquire()
    assert sem.in_use() == 3
    print("  ✓ Third acquire works")
    
    # Should fail now (at capacity)
    assert not sem.try_acquire()
    print("  ✓ TryAcquire fails when full")
    
    # Release
    sem.release()
    assert sem.available() == 1
    print("  ✓ Release works")
    
    # Try acquire should work now
    assert sem.try_acquire()
    print("  ✓ TryAcquire works after release")
    
    sem.release()
    sem.release()
    sem.release()
    assert sem.available() == 3
    print("  ✓ Multiple releases work")
    
    print("✓ Semaphore basic tests passed\n")


def test_semaphore_context_manager():
    """Test semaphore as context manager."""
    print("Testing Semaphore context manager...")
    
    sem = Semaphore(2)
    
    with sem:
        assert sem.in_use() == 1
        print("  ✓ Acquired in context")
        
        with sem:
            assert sem.in_use() == 2
            print("  ✓ Nested context works")
        
        assert sem.in_use() == 1
        print("  ✓ Nested context released")
    
    assert sem.in_use() == 0
    print("  ✓ Context released")
    
    print("✓ Context manager tests passed\n")


def test_semaphore_timeout():
    """Test semaphore timeout behavior."""
    print("Testing Semaphore timeout...")
    
    sem = Semaphore(1)
    
    # Acquire first permit
    sem.acquire()
    
    # Try to acquire with timeout (should fail)
    try:
        sem.acquire(timeout=0.1)
        assert False, "Should have raised TimeoutError"
    except TimeoutError:
        print("  ✓ Timeout raised correctly")
    
    # Release and try again (should succeed)
    sem.release()
    assert sem.acquire(timeout=1.0)
    print("  ✓ Acquire works after release")
    
    sem.release()
    print("✓ Timeout tests passed\n")


def test_semaphore_concurrent():
    """Test semaphore with concurrent access."""
    print("Testing Semaphore concurrent access...")
    
    sem = Semaphore(3)
    results = []
    
    def worker(worker_id):
        with sem:
            results.append(f"Worker {worker_id} acquired")
            time.sleep(0.05)
            results.append(f"Worker {worker_id} done")
    
    threads = [threading.Thread(target=worker, args=(i,)) for i in range(10)]
    
    start = time.time()
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    
    elapsed = time.time() - start
    
    # Should take at least (10 workers / 3 capacity) * 0.05s
    assert elapsed >= 0.15, f"Elapsed {elapsed}s should be >= 0.15s"
    assert len(results) == 20  # 10 workers * 2 messages
    print(f"  ✓ 10 workers processed in {elapsed:.2f}s (capacity=3)")
    
    print("✓ Concurrent tests passed\n")


def test_weighted_semaphore():
    """Test weighted semaphore."""
    print("Testing WeightedSemaphore...")
    
    sem = WeightedSemaphore(100)
    
    assert sem.capacity == 100
    assert sem.available() == 100
    print("  ✓ Initial state")
    
    # Acquire weight
    assert sem.acquire(30)
    assert sem.in_use() == 30
    assert sem.available() == 70
    print("  ✓ Acquire 30 units")
    
    # Acquire more
    assert sem.acquire(50)
    assert sem.in_use() == 80
    print("  ✓ Acquire 50 more units")
    
    # Try acquire too much (should fail)
    assert not sem.try_acquire(30)  # Only 20 available
    print("  ✓ TryAcquire fails when not enough")
    
    # Try acquire valid amount
    assert sem.try_acquire(20)
    assert sem.in_use() == 100
    print("  ✓ TryAcquire 20 units")
    
    # Release
    sem.release(30)
    assert sem.available() == 30
    print("  ✓ Release 30 units")
    
    # Context manager
    with sem.acquire_context(10):
        assert sem.in_use() == 80  # 70 + 10 = 80
        print("  ✓ Context manager works")
    
    assert sem.in_use() == 70
    print("  ✓ Context released")
    
    sem.release(80)
    print("✓ WeightedSemaphore tests passed\n")


def test_semaphore_pool():
    """Test semaphore pool."""
    print("Testing SemaphorePool...")
    
    pool = SemaphorePool(5)
    
    # Get semaphores
    sem1 = pool.get('db')
    assert sem1.capacity == 5
    print("  ✓ Created 'db' semaphore")
    
    sem2 = pool.get('api')
    assert sem2.capacity == 5
    print("  ✓ Created 'api' semaphore")
    
    # Custom capacity
    sem3 = pool.get('cache', capacity=10)
    assert sem3.capacity == 10
    print("  ✓ Created 'cache' semaphore with custom capacity")
    
    # Keys and size
    assert set(pool.keys()) == {'db', 'api', 'cache'}
    assert pool.size() == 3
    print("  ✓ Keys and size correct")
    
    # Stats
    stats = pool.stats()
    assert 'db' in stats
    assert stats['db']['capacity'] == 5
    print("  ✓ Stats work")
    
    # Remove
    pool.remove('db')
    assert pool.size() == 2
    print("  ✓ Remove works")
    
    print("✓ SemaphorePool tests passed\n")


def test_bounded_semaphore():
    """Test bounded semaphore."""
    print("Testing BoundedSemaphore...")
    
    sem = BoundedSemaphore(2)
    
    # Acquire both permits
    sem.acquire()
    sem.acquire()
    print("  ✓ Acquired both permits")
    
    # Release both
    sem.release()
    sem.release()
    print("  ✓ Released both permits")
    
    # Try to release again (should raise)
    try:
        sem.release()
        assert False, "Should have raised ValueError"
    except ValueError as e:
        assert "released too many times" in str(e)
        print("  ✓ Over-release raises error")
    
    print("✓ BoundedSemaphore tests passed\n")


def test_priority_semaphore():
    """Test priority semaphore."""
    print("Testing PrioritySemaphore...")
    
    sem = PrioritySemaphore(1)
    results = []
    
    def worker(worker_id, priority):
        sem.acquire(priority=priority)
        results.append(f"Worker {worker_id} (priority {priority})")
        time.sleep(0.05)
        sem.release()
    
    # Create threads with different priorities
    threads = [
        threading.Thread(target=worker, args=(1, 10)),  # Low priority
        threading.Thread(target=worker, args=(2, 1)),   # High priority
        threading.Thread(target=worker, args=(3, 5)),   # Medium priority
    ]
    
    # Acquire first permit
    sem.acquire()
    
    # Start threads
    for t in threads:
        t.start()
        time.sleep(0.01)  # Ensure threads queue up
    
    # Release permit
    sem.release()
    
    # Wait for threads
    for t in threads:
        t.join()
    
    # Higher priority (lower number) should go first
    assert results[0] == "Worker 2 (priority 1)"
    print(f"  ✓ Priority order: {results}")
    
    print("✓ PrioritySemaphore tests passed\n")


def test_rate_limiter():
    """Test rate limiter."""
    print("Testing RateLimiter...")
    
    limiter = RateLimiter(5, 1.0)  # 5 permits per second
    
    # Should be able to acquire immediately (burst)
    start = time.time()
    for i in range(5):
        assert limiter.try_acquire()
    elapsed = time.time() - start
    assert elapsed < 0.1, "Burst should be fast"
    print(f"  ✓ Burst of 5 acquired in {elapsed:.3f}s")
    
    # Should fail now
    assert not limiter.try_acquire()
    print("  ✓ TryAcquire fails after burst")
    
    # Wait and try again
    time.sleep(0.2)
    # Should have some tokens now
    assert limiter.try_acquire()
    print("  ✓ TryAcquire works after refill")
    
    print("✓ RateLimiter tests passed\n")


def test_concurrency_limit():
    """Test concurrency limit."""
    print("Testing ConcurrencyLimit...")
    
    limit = ConcurrencyLimit(max_concurrent=2)
    
    with limit:
        assert limit.available == 1
        print("  ✓ First acquire works")
        
        with limit:
            assert limit.available == 0
            print("  ✓ Second acquire works")
    
    assert limit.available == 2
    print("  ✓ Both released")
    
    print("✓ ConcurrencyLimit tests passed\n")


def test_acquire_all():
    """Test acquire_all function."""
    print("Testing acquire_all...")
    
    sem1 = Semaphore(1)
    sem2 = Semaphore(1)
    
    # Acquire both
    acquire_all(sem1, sem2)
    
    assert sem1.in_use() == 1
    assert sem2.in_use() == 1
    print("  ✓ Both acquired")
    
    sem1.release()
    sem2.release()
    print("✓ acquire_all tests passed\n")


def test_run_with_semaphore():
    """Test run_with_semaphore function."""
    print("Testing run_with_semaphore...")
    
    sem = Semaphore(1)
    
    def compute(x, y):
        return x + y
    
    result = run_with_semaphore(sem, compute, 5, 3)
    assert result == 8
    assert sem.available() == 1
    print("  ✓ Function executed correctly")
    
    print("✓ run_with_semaphore tests passed\n")


async def test_async_semaphore():
    """Test async semaphore."""
    print("Testing AsyncSemaphore...")
    
    sem = AsyncSemaphore(3)
    
    async def worker(worker_id):
        async with sem:
            await asyncio.sleep(0.05)
            return f"Worker {worker_id} done"
    
    results = await asyncio.gather(
        worker(1), worker(2), worker(3),
        worker(4), worker(5)
    )
    
    assert len(results) == 5
    print(f"  ✓ 5 async workers completed: {results}")
    
    print("✓ AsyncSemaphore tests passed\n")


async def test_async_weighted_semaphore():
    """Test async weighted semaphore."""
    print("Testing AsyncWeightedSemaphore...")
    
    sem = AsyncWeightedSemaphore(100)
    
    # Acquire weight
    await sem.acquire(30)
    assert sem.in_use() == 30
    print("  ✓ Acquired 30 units")
    
    await sem.release(30)
    assert sem.in_use() == 0
    print("  ✓ Released 30 units")
    
    print("✓ AsyncWeightedSemaphore tests passed\n")


def test_invalid_inputs():
    """Test invalid inputs."""
    print("Testing invalid inputs...")
    
    # Zero capacity
    try:
        Semaphore(0)
        assert False
    except ValueError:
        print("  ✓ Zero capacity raises error")
    
    # Negative capacity
    try:
        Semaphore(-1)
        assert False
    except ValueError:
        print("  ✓ Negative capacity raises error")
    
    # Weighted zero weight
    sem = WeightedSemaphore(100)
    try:
        sem.acquire(0)
        assert False
    except ValueError:
        print("  ✓ Zero weight raises error")
    
    # Weight exceeds capacity
    try:
        sem.acquire(200)
        assert False
    except ValueError:
        print("  ✓ Weight exceeding capacity raises error")
    
    print("✓ Invalid input tests passed\n")


def run_tests():
    """Run all tests."""
    print("=" * 60)
    print("Semaphore Utils Test Suite")
    print("=" * 60)
    print()
    
    # Synchronous tests
    test_semaphore_basic()
    test_semaphore_context_manager()
    test_semaphore_timeout()
    test_semaphore_concurrent()
    test_weighted_semaphore()
    test_semaphore_pool()
    test_bounded_semaphore()
    test_priority_semaphore()
    test_rate_limiter()
    test_concurrency_limit()
    test_acquire_all()
    test_run_with_semaphore()
    test_invalid_inputs()
    
    # Async tests (Python 3.6 compatible)
    loop = asyncio.get_event_loop()
    loop.run_until_complete(test_async_semaphore())
    loop.run_until_complete(test_async_weighted_semaphore())
    
    print("=" * 60)
    print("ALL TESTS PASSED ✓")
    print("=" * 60)


if __name__ == "__main__":
    run_tests()