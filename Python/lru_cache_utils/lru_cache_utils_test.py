"""
Tests for LRU Cache Utility Module

Comprehensive tests covering all functionality of the LRU cache implementation.
"""

import time
import threading
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from mod import (
    LRUCache, lru_cache, memoize, TTLCache,
    Node
)


class TestNode:
    """Tests for Node class."""
    
    def test_basic_node(self):
        """Test basic node creation."""
        node = Node('key', 'value')
        assert node.key == 'key'
        assert node.value == 'value'
        assert node.prev is None
        assert node.next is None
        assert node.expires_at is None
        assert node.access_count == 0
    
    def test_node_with_ttl(self):
        """Test node with TTL."""
        node = Node('key', 'value', ttl=10.0)
        assert node.expires_at is not None
        assert node.expires_at > time.time()
        assert node.expires_at <= time.time() + 10.0


class TestLRUCache:
    """Tests for LRUCache class."""
    
    def test_basic_put_get(self):
        """Test basic put and get operations."""
        cache = LRUCache[str, int](capacity=3)
        
        cache.put('a', 1)
        cache.put('b', 2)
        cache.put('c', 3)
        
        assert cache.get('a') == 1
        assert cache.get('b') == 2
        assert cache.get('c') == 3
    
    def test_eviction(self):
        """Test LRU eviction when capacity is exceeded."""
        cache = LRUCache[str, int](capacity=3)
        
        cache.put('a', 1)
        cache.put('b', 2)
        cache.put('c', 3)
        cache.put('d', 4)  # 'a' should be evicted
        
        assert cache.get('a') is None
        assert cache.get('b') == 2
        assert cache.get('c') == 3
        assert cache.get('d') == 4
    
    def test_lru_order_update(self):
        """Test that accessing an item updates its LRU position."""
        cache = LRUCache[str, int](capacity=3)
        
        cache.put('a', 1)
        cache.put('b', 2)
        cache.put('c', 3)
        
        # Access 'a' to make it most recently used
        cache.get('a')
        
        # Now add 'd', 'b' should be evicted (not 'a')
        cache.put('d', 4)
        
        assert cache.get('a') == 1
        assert cache.get('b') is None
        assert cache.get('c') == 3
        assert cache.get('d') == 4
    
    def test_update_existing_key(self):
        """Test updating an existing key."""
        cache = LRUCache[str, int](capacity=3)
        
        cache.put('a', 1)
        cache.put('a', 2)
        
        assert cache.size() == 1
        assert cache.get('a') == 2
    
    def test_delete(self):
        """Test delete operation."""
        cache = LRUCache[str, int](capacity=3)
        
        cache.put('a', 1)
        assert cache.delete('a') is True
        assert cache.get('a') is None
        assert cache.delete('a') is False
    
    def test_contains(self):
        """Test contains check."""
        cache = LRUCache[str, int](capacity=3)
        
        cache.put('a', 1)
        assert cache.contains('a') is True
        assert cache.contains('b') is False
    
    def test_clear(self):
        """Test clear operation."""
        cache = LRUCache[str, int](capacity=3)
        
        cache.put('a', 1)
        cache.put('b', 2)
        cache.clear()
        
        assert cache.is_empty()
        assert cache.size() == 0
    
    def test_keys_values_items(self):
        """Test keys, values, and items methods."""
        cache = LRUCache[str, int](capacity=3)
        
        cache.put('a', 1)
        cache.put('b', 2)
        cache.put('c', 3)
        
        # Access 'a' to make it most recent
        cache.get('a')
        
        keys = cache.keys()
        values = cache.values()
        items = cache.items()
        
        assert keys == ['a', 'c', 'b']  # Most recent first
        assert values == [1, 3, 2]
        assert items == [('a', 1), ('c', 3), ('b', 2)]
    
    def test_capacity_change(self):
        """Test changing capacity."""
        cache = LRUCache[str, int](capacity=5)
        
        cache.put('a', 1)
        cache.put('b', 2)
        cache.put('c', 3)
        cache.put('d', 4)
        cache.put('e', 5)
        
        # Reduce capacity
        cache.capacity = 3
        
        assert cache.size() == 3
        # Least recently used should be evicted: a, b
        assert cache.get('c') == 3
        assert cache.get('d') == 4
        assert cache.get('e') == 5
    
    def test_stats(self):
        """Test statistics."""
        cache = LRUCache[str, int](capacity=3)
        
        cache.put('a', 1)
        cache.get('a')  # hit
        cache.get('b')  # miss
        
        stats = cache.stats()
        assert stats['hits'] == 1
        assert stats['misses'] == 1
        assert stats['hit_rate'] == 0.5
        assert stats['capacity'] == 3
        assert stats['size'] == 1
    
    def test_zero_capacity(self):
        """Test that zero capacity raises error."""
        try:
            LRUCache[str, int](capacity=0)
            assert False, "Should have raised ValueError"
        except ValueError:
            pass
    
    def test_negative_capacity(self):
        """Test that negative capacity raises error."""
        try:
            LRUCache[str, int](capacity=-1)
            assert False, "Should have raised ValueError"
        except ValueError:
            pass
    
    def test_dict_interface(self):
        """Test dictionary-like interface."""
        cache = LRUCache[str, int](capacity=3)
        
        # __setitem__ and __getitem__
        cache['a'] = 1
        assert cache['a'] == 1
        
        # __contains__
        assert 'a' in cache
        assert 'b' not in cache
        
        # __delitem__
        del cache['a']
        assert 'a' not in cache
        
        # __len__
        cache['b'] = 2
        assert len(cache) == 1
    
    def test_get_with_default(self):
        """Test get with default value."""
        cache = LRUCache[str, int](capacity=3)
        
        cache.put('a', 1)
        assert cache.get('a', 0) == 1
        assert cache.get('b', 0) == 0
    
    def test_keyerror_on_missing(self):
        """Test that __getitem__ raises KeyError for missing key."""
        cache = LRUCache[str, int](capacity=3)
        
        try:
            _ = cache['missing']
            assert False, "Should have raised KeyError"
        except KeyError:
            pass
    
    def test_delitem_keyerror(self):
        """Test that __delitem__ raises KeyError for missing key."""
        cache = LRUCache[str, int](capacity=3)
        
        try:
            del cache['missing']
            assert False, "Should have raised KeyError"
        except KeyError:
            pass


class TestLRUCacheWithTTL:
    """Tests for LRU cache with TTL."""
    
    def test_basic_ttl(self):
        """Test basic TTL functionality."""
        cache = LRUCache[str, int](capacity=3, ttl=0.1)  # 100ms
        
        cache.put('temp', 1)
        assert cache.get('temp') == 1
        
        time.sleep(0.15)
        assert cache.get('temp') is None
    
    def test_ttl_override(self):
        """Test TTL override on put."""
        cache = LRUCache[str, int](capacity=3, ttl=10.0)
        
        # Override TTL for specific item
        cache.put('short', 1, ttl=0.1)
        cache.put('long', 2)
        
        time.sleep(0.15)
        assert cache.get('short') is None
        assert cache.get('long') == 2
    
    def test_refresh_ttl(self):
        """Test refreshing TTL."""
        cache = LRUCache[str, int](capacity=3, ttl=0.2)
        
        cache.put('a', 1)
        time.sleep(0.1)
        
        # Refresh TTL
        cache.refresh_ttl('a')
        time.sleep(0.15)
        
        # Should still be there
        assert cache.get('a') == 1
    
    def test_contains_with_expired(self):
        """Test contains check with expired items."""
        cache = LRUCache[str, int](capacity=3, ttl=0.1)
        
        cache.put('a', 1)
        time.sleep(0.15)
        
        assert cache.contains('a') is False
    
    def test_expired_item_eviction_on_access(self):
        """Test that expired items are evicted on access."""
        cache = LRUCache[str, int](capacity=3, ttl=0.1)
        
        cache.put('a', 1)
        time.sleep(0.15)
        
        # Access should evict the expired item
        cache.get('a')
        
        stats = cache.stats()
        assert stats['expirations'] >= 1


class TestLRUCacheWithCallback:
    """Tests for LRU cache with eviction callback."""
    
    def test_eviction_callback(self):
        """Test that eviction callback is called."""
        evicted = []
        
        def on_evict(key, value):
            evicted.append((key, value))
        
        cache = LRUCache[str, int](capacity=2, on_evict=on_evict)
        
        cache.put('a', 1)
        cache.put('b', 2)
        cache.put('c', 3)  # 'a' should be evicted
        
        assert ('a', 1) in evicted


class TestLRUCacheThreadSafe:
    """Tests for thread-safe LRU cache."""
    
    def test_concurrent_access(self):
        """Test concurrent read/write operations."""
        cache = LRUCache[int, int](capacity=100, thread_safe=True)
        errors = []
        
        def writer(start, count):
            try:
                for i in range(start, start + count):
                    cache.put(i, i * 10)
            except Exception as e:
                errors.append(e)
        
        def reader(start, count):
            try:
                for i in range(start, start + count):
                    cache.get(i)
            except Exception as e:
                errors.append(e)
        
        threads = []
        for i in range(5):
            threads.append(threading.Thread(target=writer, args=(i * 20, 20)))
            threads.append(threading.Thread(target=reader, args=(i * 20, 20)))
        
        for t in threads:
            t.start()
        for t in threads:
            t.join()
        
        assert len(errors) == 0
    
    def test_concurrent_eviction(self):
        """Test concurrent operations that cause eviction."""
        cache = LRUCache[int, int](capacity=10, thread_safe=True)
        errors = []
        
        def worker(start):
            try:
                for i in range(100):
                    cache.put(start + i, start + i)
            except Exception as e:
                errors.append(e)
        
        threads = [threading.Thread(target=worker, args=(i * 100,)) for i in range(10)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()
        
        assert len(errors) == 0
        assert cache.size() <= 10


class TestLRUCacheMethods:
    """Tests for additional LRU cache methods."""
    
    def test_put_all(self):
        """Test put_all method."""
        cache = LRUCache[str, int](capacity=5)
        
        cache.put_all({'a': 1, 'b': 2, 'c': 3})
        
        assert cache.size() == 3
        assert cache.get('a') == 1
    
    def test_get_all(self):
        """Test get_all method."""
        cache = LRUCache[str, int](capacity=5)
        
        cache.put_all({'a': 1, 'b': 2, 'c': 3})
        
        result = cache.get_all(['a', 'b', 'd'])
        
        assert result == {'a': 1, 'b': 2}
    
    def test_get_or_set(self):
        """Test get_or_set method."""
        cache = LRUCache[str, int](capacity=3)
        
        # First call computes
        value = cache.get_or_set('a', lambda: 42)
        assert value == 42
        
        # Second call uses cache
        value = cache.get_or_set('a', lambda: 999)
        assert value == 42
    
    def test_peek(self):
        """Test peek method (get without updating LRU position)."""
        cache = LRUCache[str, int](capacity=3)
        
        cache.put('a', 1)
        cache.put('b', 2)
        cache.put('c', 3)
        
        # Peek at 'a' without updating position
        assert cache.peek('a') == 1
        
        # Add new item - 'b' should be evicted (a is still LRU)
        cache.put('d', 4)
        
        assert cache.get('a') is None
    
    def test_touch(self):
        """Test touch method."""
        cache = LRUCache[str, int](capacity=3)
        
        cache.put('a', 1)
        cache.put('b', 2)
        cache.put('c', 3)
        
        # Touch 'a' to make it most recent
        assert cache.touch('a') is True
        assert cache.touch('missing') is False
        
        # Add new item - 'b' should be evicted
        cache.put('d', 4)
        
        assert cache.get('a') == 1
        assert cache.get('b') is None
    
    def test_is_full_is_empty(self):
        """Test is_full and is_empty methods."""
        cache = LRUCache[str, int](capacity=2)
        
        assert cache.is_empty()
        assert not cache.is_full()
        
        cache.put('a', 1)
        assert not cache.is_empty()
        assert not cache.is_full()
        
        cache.put('b', 2)
        assert not cache.is_empty()
        assert cache.is_full()
    
    def test_reset_stats(self):
        """Test reset_stats method."""
        cache = LRUCache[str, int](capacity=3)
        
        cache.put('a', 1)
        cache.get('a')
        cache.get('b')
        
        stats = cache.stats()
        assert stats['hits'] == 1
        assert stats['misses'] == 1
        
        cache.reset_stats()
        
        stats = cache.stats()
        assert stats['hits'] == 0
        assert stats['misses'] == 0
    
    def test_repr(self):
        """Test __repr__ method."""
        cache = LRUCache[str, int](capacity=3)
        cache.put('a', 1)
        
        repr_str = repr(cache)
        assert 'LRUCache' in repr_str
        assert 'capacity=3' in repr_str
        assert 'size=1' in repr_str


class TestLRUCacheDecorator:
    """Tests for lru_cache decorator."""
    
    def test_basic_decoration(self):
        """Test basic function decoration."""
        call_count = [0]
        
        @lru_cache(capacity=3)
        def expensive(n):
            call_count[0] += 1
            return n * 2
        
        assert expensive(5) == 10
        assert call_count[0] == 1
        
        # Cached result
        assert expensive(5) == 10
        assert call_count[0] == 1  # Not called again
        
        # Different argument
        assert expensive(10) == 20
        assert call_count[0] == 2
    
    def test_decorator_with_kwargs(self):
        """Test decorator with keyword arguments."""
        @lru_cache(capacity=3)
        def add(a, b=0):
            return a + b
        
        assert add(1, b=2) == 3
        assert add(1, b=2) == 3  # Cached
    
    def test_decorator_cache_access(self):
        """Test accessing cache through decorator."""
        @lru_cache(capacity=3)
        def square(n):
            return n * n
        
        square(2)
        square(3)
        
        # Access cache stats
        stats = square.cache_stats()  # type: ignore
        assert stats['size'] == 2
        
        # Clear cache
        square.cache_clear()  # type: ignore
        stats = square.cache_stats()  # type: ignore
        assert stats['size'] == 0
    
    def test_decorator_with_ttl(self):
        """Test decorator with TTL."""
        @lru_cache(capacity=3, ttl=0.1)
        def get_time():
            return time.time()
        
        t1 = get_time()
        time.sleep(0.05)
        t2 = get_time()
        
        assert t1 == t2  # Same cached value
        
        time.sleep(0.1)
        t3 = get_time()
        
        assert t3 != t1  # New value after TTL


class TestMemoize:
    """Tests for memoize decorator."""
    
    def test_basic_memoization(self):
        """Test basic memoization."""
        call_count = [0]
        
        @memoize
        def fib(n):
            call_count[0] += 1
            if n < 2:
                return n
            return fib(n - 1) + fib(n - 2)
        
        result = fib(10)
        assert result == 55
        # Memoization prevents exponential calls
        assert call_count[0] < 20
    
    def test_memoize_different_args(self):
        """Test memoization with different arguments."""
        @memoize
        def identity(x):
            return x
        
        assert identity(1) == 1
        assert identity(2) == 2
        assert identity(1) == 1  # Cached
    
    def test_memoize_cache_clear(self):
        """Test clearing memoize cache."""
        @memoize
        def func(x):
            return x
        
        func(1)
        assert len(func.cache) == 1  # type: ignore
        
        func.cache_clear()  # type: ignore
        assert len(func.cache) == 0  # type: ignore


class TestTTLCache:
    """Tests for TTL-only cache."""
    
    def test_basic_ttl_cache(self):
        """Test basic TTL cache operations."""
        cache = TTLCache[str, int](ttl=0.1)
        
        cache.put('a', 1)
        assert cache.get('a') == 1
        
        time.sleep(0.15)
        assert cache.get('a') is None
    
    def test_ttl_override(self):
        """Test TTL override."""
        cache = TTLCache[str, int](ttl=10.0)
        
        cache.put('short', 1, ttl=0.1)
        cache.put('long', 2)
        
        time.sleep(0.15)
        assert cache.get('short') is None
        assert cache.get('long') == 2
    
    def test_delete(self):
        """Test delete operation."""
        cache = TTLCache[str, int](ttl=10.0)
        
        cache.put('a', 1)
        assert cache.delete('a') is True
        assert cache.delete('a') is False
        assert cache.get('a') is None
    
    def test_clear(self):
        """Test clear operation."""
        cache = TTLCache[str, int](ttl=10.0)
        
        cache.put('a', 1)
        cache.put('b', 2)
        cache.clear()
        
        assert cache.size() == 0
    
    def test_cleanup(self):
        """Test automatic cleanup."""
        cache = TTLCache[str, int](ttl=0.05, cleanup_interval=0.05)
        
        cache.put('a', 1)
        cache.put('b', 2)
        
        assert cache.size() == 2
        
        time.sleep(0.1)
        
        # Access triggers cleanup
        cache.get('a')
        
        assert cache.size() == 0


def run_tests():
    """Run all tests."""
    test_classes = [
        TestNode,
        TestLRUCache,
        TestLRUCacheWithTTL,
        TestLRUCacheWithCallback,
        TestLRUCacheThreadSafe,
        TestLRUCacheMethods,
        TestLRUCacheDecorator,
        TestMemoize,
        TestTTLCache,
    ]
    
    passed = 0
    failed = 0
    
    for test_class in test_classes:
        instance = test_class()
        test_methods = [m for m in dir(instance) if m.startswith('test_')]
        
        for method_name in test_methods:
            try:
                getattr(instance, method_name)()
                passed += 1
                print(f"  ✓ {test_class.__name__}.{method_name}")
            except AssertionError as e:
                failed += 1
                print(f"  ✗ {test_class.__name__}.{method_name}")
                print(f"    AssertionError: {e}")
            except Exception as e:
                failed += 1
                print(f"  ✗ {test_class.__name__}.{method_name}")
                print(f"    {type(e).__name__}: {e}")
    
    print(f"\n{'='*50}")
    print(f"Results: {passed} passed, {failed} failed")
    return failed == 0


if __name__ == '__main__':
    print("="*50)
    print("LRU Cache Utils Test Suite")
    print("="*50 + "\n")
    
    success = run_tests()
    sys.exit(0 if success else 1)