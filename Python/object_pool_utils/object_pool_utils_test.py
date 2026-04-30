"""
AllToolkit - Python Object Pool Utilities Test Suite

Comprehensive test suite for object pooling utilities.
Run with: python object_pool_utils_test.py

Tests cover:
- Basic object pool operations (borrow, return)
- Thread-safe operations
- Object validation
- Object reset
- Pool statistics
- Idle object eviction
- Connection pool features
- Pool manager
- Edge cases and error handling
"""

import sys
import os
import threading
import time
import queue
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from mod import (
    ObjectPool, ConnectionPool, PoolManager, PoolStats, PooledObject,
    create_pool, create_connection_pool,
    PooledStringBuilder, PooledList, PooledDict
)


# Test counters for tracking factory/destructor calls
test_counters = {}


def reset_counters():
    """Reset test counters."""
    global test_counters
    test_counters = {
        'created': 0,
        'destroyed': 0,
        'validated': 0,
        'reset': 0,
    }


def test_basic_pool_creation():
    """Test basic pool creation."""
    reset_counters()
    
    def factory():
        test_counters['created'] += 1
        return {'id': test_counters['created']}
    
    pool = ObjectPool(factory=factory, max_size=5)
    
    assert pool.size == 0  # Initially empty (no min_idle)
    assert pool.idle_count == 0
    assert pool.active_count == 0
    
    pool.close()
    print("✓ test_basic_pool_creation passed")


def test_borrow_and_return():
    """Test basic borrow and return operations."""
    reset_counters()
    
    def factory():
        test_counters['created'] += 1
        return {'id': test_counters['created'], 'data': []}
    
    pool = ObjectPool(factory=factory, max_size=3)
    
    # Borrow an object
    obj1 = pool.borrow()
    assert obj1 is not None
    assert test_counters['created'] == 1
    assert pool.active_count == 1
    assert pool.idle_count == 0
    
    # Return the object
    pool.return_object(obj1)
    assert pool.active_count == 0
    assert pool.idle_count == 1
    
    # Borrow again - should reuse
    obj2 = pool.borrow()
    assert obj2 is obj1  # Same object
    assert test_counters['created'] == 1  # No new creation
    assert pool.active_count == 1
    
    pool.return_object(obj2)
    pool.close()
    print("✓ test_borrow_and_return passed")


def test_context_manager():
    """Test using pool with context manager."""
    reset_counters()
    
    def factory():
        test_counters['created'] += 1
        return {'id': test_counters['created']}
    
    pool = ObjectPool(factory=factory, max_size=3)
    
    # Use context manager
    with pool.use() as obj:
        assert obj is not None
        assert pool.active_count == 1
    
    # After context, object should be returned
    assert pool.active_count == 0
    assert pool.idle_count == 1
    
    pool.close()
    print("✓ test_context_manager passed")


def test_pool_exhaustion():
    """Test pool exhaustion and timeout."""
    reset_counters()
    
    def factory():
        test_counters['created'] += 1
        return {'id': test_counters['created']}
    
    pool = ObjectPool(factory=factory, max_size=2, borrow_timeout=0.5)
    
    # Borrow all objects
    obj1 = pool.borrow()
    obj2 = pool.borrow()
    
    assert pool.active_count == 2
    assert pool.idle_count == 0
    
    # Try to borrow another - should timeout
    try:
        pool.borrow(timeout=0.1)
        assert False, "Should have raised TimeoutError"
    except TimeoutError:
        pass
    
    # Return one and try again
    pool.return_object(obj1)
    
    obj3 = pool.borrow()  # Should succeed now
    assert obj3 is obj1
    
    pool.return_object(obj2)
    pool.return_object(obj3)
    pool.close()
    print("✓ test_pool_exhaustion passed")


def test_object_validation():
    """Test object validation."""
    reset_counters()
    
    def factory():
        test_counters['created'] += 1
        return {'id': test_counters['created'], 'valid': True}
    
    def validator(obj):
        test_counters['validated'] += 1
        return obj.get('valid', False)
    
    pool = ObjectPool(
        factory=factory,
        validator=validator,
        max_size=3,
        validation_on_borrow=True
    )
    
    # Borrow valid object
    obj1 = pool.borrow()
    assert obj1 is not None
    
    # Mark as invalid
    obj1['valid'] = False
    pool.return_object(obj1)
    
    # Borrow again - should create new since old is invalid
    obj2 = pool.borrow()
    assert obj2 is not obj1  # Should be a new object
    
    pool.return_object(obj2)
    pool.close()
    print("✓ test_object_validation passed")


def test_object_reset():
    """Test object reset on return."""
    reset_counters()
    
    def factory():
        test_counters['created'] += 1
        return {'id': test_counters['created'], 'data': []}
    
    def reset_func(obj):
        test_counters['reset'] += 1
        obj['data'].clear()
    
    pool = ObjectPool(
        factory=factory,
        reset=reset_func,
        max_size=3,
        reset_on_return=True
    )
    
    obj = pool.borrow()
    obj['data'].extend([1, 2, 3, 4, 5])
    
    pool.return_object(obj)
    
    # Reset should have been called
    assert test_counters['reset'] == 1
    
    # Borrow again - data should be cleared
    obj2 = pool.borrow()
    assert obj2 is obj
    assert len(obj2['data']) == 0
    
    pool.return_object(obj2)
    pool.close()
    print("✓ test_object_reset passed")


def test_destructor():
    """Test that destructor is called."""
    reset_counters()
    
    def factory():
        test_counters['created'] += 1
        return {'id': test_counters['created'], 'closed': False}
    
    def destructor(obj):
        test_counters['destroyed'] += 1
        obj['closed'] = True
    
    pool = ObjectPool(
        factory=factory,
        destructor=destructor,
        max_size=3
    )
    
    obj = pool.borrow()
    pool.return_object(obj)
    
    # Destructor not called yet
    assert test_counters['destroyed'] == 0
    
    # Clear the pool
    pool.clear()
    assert test_counters['destroyed'] == 1
    assert obj['closed'] == True
    
    pool.close()
    print("✓ test_destructor passed")


def test_pool_close():
    """Test pool closing behavior."""
    reset_counters()
    
    def factory():
        test_counters['created'] += 1
        return {'id': test_counters['created']}
    
    def destructor(obj):
        test_counters['destroyed'] += 1
    
    pool = ObjectPool(
        factory=factory,
        destructor=destructor,
        max_size=3
    )
    
    obj1 = pool.borrow()
    obj2 = pool.borrow()
    
    pool.close()
    
    assert pool.is_closed == True
    
    # All objects should be destroyed
    assert test_counters['destroyed'] == 2
    
    # Borrowing from closed pool should fail
    try:
        pool.borrow()
        assert False, "Should have raised RuntimeError"
    except RuntimeError:
        pass
    
    print("✓ test_pool_close passed")


def test_min_idle():
    """Test minimum idle objects."""
    reset_counters()
    
    def factory():
        test_counters['created'] += 1
        return {'id': test_counters['created']}
    
    pool = ObjectPool(
        factory=factory,
        max_size=5,
        min_idle=2
    )
    
    # Pool should have min_idle objects pre-created
    assert pool.idle_count == 2
    assert test_counters['created'] == 2
    
    pool.close()
    print("✓ test_min_idle passed")


def test_pool_statistics():
    """Test pool statistics tracking."""
    reset_counters()
    
    def factory():
        test_counters['created'] += 1
        return {'id': test_counters['created']}
    
    pool = ObjectPool(factory=factory, max_size=5)
    
    stats = pool.get_stats()
    assert stats.total_created == 0
    assert stats.total_borrowed == 0
    
    obj1 = pool.borrow()
    obj2 = pool.borrow()
    
    stats = pool.get_stats()
    assert stats.total_created == 2
    assert stats.total_borrowed == 2
    assert stats.current_active == 2
    assert stats.max_borrowed_at_once == 2
    
    pool.return_object(obj1)
    
    stats = pool.get_stats()
    assert stats.total_returned == 1
    assert stats.current_active == 1
    assert stats.current_idle == 1
    
    pool.return_object(obj2)
    pool.close()
    print("✓ test_pool_statistics passed")


def test_thread_safety():
    """Test thread-safe operations."""
    reset_counters()
    
    def factory():
        test_counters['created'] += 1
        return {'id': test_counters['created'], 'value': 0}
    
    pool = ObjectPool(factory=factory, max_size=10)
    
    results = []
    errors = []
    
    def worker(worker_id):
        try:
            for _ in range(10):
                with pool.use() as obj:
                    obj['value'] += 1
                    time.sleep(0.001)  # Simulate work
                results.append(worker_id)
        except Exception as e:
            errors.append(str(e))
    
    threads = [threading.Thread(target=worker, args=(i,)) for i in range(5)]
    
    for t in threads:
        t.start()
    
    for t in threads:
        t.join()
    
    assert len(errors) == 0, f"Thread errors: {errors}"
    assert len(results) == 50  # 5 threads * 10 iterations
    
    stats = pool.get_stats()
    assert stats.total_borrowed == 50
    assert stats.total_returned == 50
    
    pool.close()
    print("✓ test_thread_safety passed")


def test_idle_eviction():
    """Test idle object eviction."""
    reset_counters()
    
    def factory():
        test_counters['created'] += 1
        return {'id': test_counters['created']}
    
    def destructor(obj):
        test_counters['destroyed'] += 1
    
    pool = ObjectPool(
        factory=factory,
        destructor=destructor,
        max_size=5,
        max_idle_time=0.1,  # 100ms
        min_idle=0
    )
    
    # Borrow and return
    obj = pool.borrow()
    pool.return_object(obj)
    
    assert pool.idle_count == 1
    
    # Wait for eviction
    time.sleep(0.3)
    
    # Manually trigger eviction
    evicted = pool.evict_idle_objects()
    
    assert evicted >= 1
    assert test_counters['destroyed'] >= 1
    
    pool.close()
    print("✓ test_idle_eviction passed")


def test_connection_pool():
    """Test ConnectionPool specific features."""
    reset_counters()
    
    def factory():
        test_counters['created'] += 1
        return {'id': test_counters['created'], 'alive': True}
    
    def validator(conn):
        return conn.get('alive', False)
    
    pool = ConnectionPool(
        factory=factory,
        validator=validator,
        max_size=3,
        min_idle=1,
        max_idle_time=0  # Disable auto-eviction thread for test
    )
    
    # Should have min_idle connection
    assert pool.idle_count == 1
    
    # Borrow connection
    conn = pool.borrow()
    assert conn['alive'] == True
    assert pool.idle_count == 0
    
    # Return and check it's back in pool
    pool.return_object(conn)
    assert pool.idle_count == 1  # Back to idle
    
    # Test health check
    health = pool.health_check()
    assert 'healthy' in health
    assert 'unhealthy' in health
    
    pool.close()
    print("✓ test_connection_pool passed")


def test_connection_pool_max_lifetime():
    """Test ConnectionPool max lifetime feature."""
    reset_counters()
    
    def factory():
        test_counters['created'] += 1
        return {'id': test_counters['created'], 'alive': True}
    
    pool = ConnectionPool(
        factory=factory,
        max_size=2,
        max_lifetime=0.1,  # 100ms
        min_idle=0
    )
    
    # Borrow connection
    conn1 = pool.borrow()
    
    # Wait for lifetime to expire
    time.sleep(0.15)
    
    pool.return_object(conn1)
    
    # Borrow again - should create new due to expired lifetime
    conn2 = pool.borrow()
    
    # New connection should have been created
    assert test_counters['created'] >= 2
    
    pool.return_object(conn2)
    pool.close()
    print("✓ test_connection_pool_max_lifetime passed")


def test_pool_manager():
    """Test PoolManager."""
    reset_counters()
    
    manager = PoolManager()
    
    # Create pools
    pool1 = manager.create_pool(
        'pool1',
        factory=lambda: {'id': id(object())},
        max_size=3
    )
    
    pool2 = manager.create_pool(
        'pool2',
        factory=lambda: {'id': id(object())},
        max_size=5
    )
    
    # Get pools
    assert manager.get_pool('pool1') is pool1
    assert manager.get_pool('pool2') is pool2
    assert manager.get_pool('nonexistent') is None
    
    # Borrow from named pool
    with manager.use('pool1') as obj:
        assert obj is not None
    
    # Get all stats
    all_stats = manager.get_all_stats()
    assert 'pool1' in all_stats
    assert 'pool2' in all_stats
    
    # Close specific pool
    assert manager.close_pool('pool1') == True
    assert manager.get_pool('pool1') is None
    
    # Close all
    manager.close_all()
    print("✓ test_pool_manager passed")


def test_convenience_functions():
    """Test convenience functions."""
    reset_counters()
    
    # Test create_pool
    pool = create_pool(
        factory=lambda: {'id': id(object())},
        max_size=5
    )
    assert pool is not None
    
    with pool.use() as obj:
        assert obj is not None
    
    pool.close()
    
    # Test create_connection_pool
    conn_pool = create_connection_pool(
        factory=lambda: {'id': id(object()), 'alive': True},
        validator=lambda c: c.get('alive', False),
        max_size=3
    )
    assert conn_pool is not None
    
    with conn_pool.use() as conn:
        assert conn is not None
    
    conn_pool.close()
    print("✓ test_convenience_functions passed")


def test_pooled_resources():
    """Test example pooled resource classes."""
    # PooledStringBuilder
    sb = PooledStringBuilder()
    sb.append("Hello").append(" ").append("World")
    assert sb.build() == "Hello World"
    sb.clear()
    assert sb.build() == ""
    
    # PooledList
    pl = PooledList([1, 2, 3])
    assert len(pl) == 3
    pl.reset()
    assert len(pl) == 0
    
    # PooledDict
    pd = PooledDict({'a': 1, 'b': 2})
    assert len(pd) == 2
    pd.reset()
    assert len(pd) == 0
    
    print("✓ test_pooled_resources passed")


def test_pool_stats_properties():
    """Test PoolStats properties."""
    stats = PoolStats(
        total_created=10,
        total_destroyed=2,
        total_borrowed=50,
        total_returned=48,
        current_idle=3,
        current_active=2,
        total_wait_time_ms=150.0,
        total_borrow_count=50
    )
    
    assert stats.avg_wait_time_ms == 3.0
    assert stats.utilization_rate == 0.4  # 2 / (3+2)
    
    d = stats.to_dict()
    assert 'total_created' in d
    assert 'utilization_rate' in d
    
    print("✓ test_pool_stats_properties passed")


def test_invalid_config():
    """Test invalid configuration handling."""
    # max_size < 1
    try:
        ObjectPool(factory=lambda: None, max_size=0)
        assert False, "Should have raised ValueError"
    except ValueError:
        pass
    
    # min_idle > max_size
    try:
        ObjectPool(factory=lambda: None, max_size=2, min_idle=5)
        assert False, "Should have raised ValueError"
    except ValueError:
        pass
    
    # negative borrow_timeout
    try:
        ObjectPool(factory=lambda: None, borrow_timeout=-1)
        assert False, "Should have raised ValueError"
    except ValueError:
        pass
    
    print("✓ test_invalid_config passed")


def test_return_wrong_object():
    """Test returning an object not from this pool."""
    reset_counters()
    
    def factory():
        test_counters['created'] += 1
        return {'id': test_counters['created']}
    
    pool = ObjectPool(factory=factory, max_size=3)
    
    obj = pool.borrow()
    pool.return_object(obj)
    
    # Try to return an object that wasn't borrowed
    fake_obj = {'id': 999}
    pool.return_object(fake_obj)  # Should silently ignore
    
    stats = pool.get_stats()
    assert stats.total_returned == 1  # Only the first return counted
    
    pool.close()
    print("✓ test_return_wrong_object passed")


def test_pool_repr():
    """Test pool string representation."""
    def factory():
        return {'id': id(object())}
    
    pool = ObjectPool(factory=factory, max_size=5)
    repr_str = repr(pool)
    
    assert 'ObjectPool' in repr_str
    assert 'size' in repr_str
    assert 'idle' in repr_str
    assert 'active' in repr_str
    
    pool.close()
    print("✓ test_pool_repr passed")


def test_context_manager_on_pool():
    """Test pool as context manager."""
    reset_counters()
    
    def factory():
        test_counters['created'] += 1
        return {'id': test_counters['created']}
    
    def destructor(obj):
        test_counters['destroyed'] += 1
    
    with ObjectPool(
        factory=factory,
        destructor=destructor,
        max_size=3
    ) as pool:
        obj = pool.borrow()
        assert obj is not None
        # Pool auto-closes on exit
    
    # Pool should be closed and objects destroyed
    assert test_counters['destroyed'] == 1
    
    print("✓ test_context_manager_on_pool passed")


def run_all_tests():
    """Run all tests."""
    print("=" * 60)
    print("Object Pool Utilities Test Suite")
    print("=" * 60)
    print()
    
    tests = [
        test_basic_pool_creation,
        test_borrow_and_return,
        test_context_manager,
        test_pool_exhaustion,
        test_object_validation,
        test_object_reset,
        test_destructor,
        test_pool_close,
        test_min_idle,
        test_pool_statistics,
        test_thread_safety,
        test_idle_eviction,
        test_connection_pool,
        test_connection_pool_max_lifetime,
        test_pool_manager,
        test_convenience_functions,
        test_pooled_resources,
        test_pool_stats_properties,
        test_invalid_config,
        test_return_wrong_object,
        test_pool_repr,
        test_context_manager_on_pool,
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            test()
            passed += 1
        except Exception as e:
            failed += 1
            print(f"✗ {test.__name__} FAILED: {e}")
    
    print()
    print("=" * 60)
    print(f"Results: {passed} passed, {failed} failed")
    print("=" * 60)
    
    return failed == 0


if __name__ == '__main__':
    success = run_all_tests()
    sys.exit(0 if success else 1)