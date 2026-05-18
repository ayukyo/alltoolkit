"""
LRU Cache Utils - Comprehensive Test Suite

Tests all LRU cache implementations and utilities.

Author: AllToolkit
Date: 2026-05-18
"""

import threading
import time
import unittest
from concurrent.futures import ThreadPoolExecutor, as_completed

from lru_cache_utils import (
    LRUCache,
    TTLCache,
    lru_cache,
    memoize,
    MultiLevelCache,
    CachedFunction,
    BoundedLRUCache,
    CacheStats,
    CacheEntry,
)


class TestCacheStats(unittest.TestCase):
    """Test CacheStats class."""
    
    def test_empty_stats(self):
        """Test empty statistics."""
        stats = CacheStats()
        self.assertEqual(stats.hits, 0)
        self.assertEqual(stats.misses, 0)
        self.assertEqual(stats.evictions, 0)
        self.assertEqual(stats.hit_rate, 0.0)
        self.assertEqual(stats.total_requests, 0)
    
    def test_hit_rate(self):
        """Test hit rate calculation."""
        stats = CacheStats()
        stats.hits = 75
        stats.misses = 25
        self.assertEqual(stats.hit_rate, 0.75)
    
    def test_reset(self):
        """Test statistics reset."""
        stats = CacheStats()
        stats.hits = 100
        stats.misses = 50
        stats.reset()
        self.assertEqual(stats.hits, 0)
        self.assertEqual(stats.misses, 0)
    
    def test_to_dict(self):
        """Test dictionary conversion."""
        stats = CacheStats()
        stats.hits = 10
        stats.misses = 5
        d = stats.to_dict()
        self.assertEqual(d['hits'], 10)
        self.assertEqual(d['misses'], 5)
        self.assertEqual(d['hit_rate'], 10/15)


class TestCacheEntry(unittest.TestCase):
    """Test CacheEntry class."""
    
    def test_entry_creation(self):
        """Test entry creation."""
        entry = CacheEntry(
            value="test",
            created_at=time.time(),
            last_accessed=time.time(),
        )
        self.assertEqual(entry.value, "test")
        self.assertEqual(entry.access_count, 1)
        self.assertFalse(entry.is_expired)
    
    def test_expiration(self):
        """Test entry expiration check."""
        entry = CacheEntry(
            value="test",
            created_at=time.time() - 10,
            last_accessed=time.time(),
            ttl=5,
        )
        self.assertTrue(entry.is_expired)
        
        entry.ttl = 20
        self.assertFalse(entry.is_expired)
    
    def test_age(self):
        """Test entry age calculation."""
        entry = CacheEntry(
            value="test",
            created_at=time.time() - 5,
            last_accessed=time.time(),
        )
        age = entry.age
        self.assertGreaterEqual(age, 4.9)
        self.assertLessEqual(age, 5.1)
    
    def test_idle_time(self):
        """Test idle time calculation."""
        entry = CacheEntry(
            value="test",
            created_at=time.time(),
            last_accessed=time.time() - 3,
        )
        idle = entry.idle_time
        self.assertGreaterEqual(idle, 2.9)
        self.assertLessEqual(idle, 3.1)


class TestLRUCache(unittest.TestCase):
    """Test LRUCache class."""
    
    def test_basic_set_get(self):
        """Test basic set and get operations."""
        cache = LRUCache(max_size=10)
        cache.set('key1', 'value1')
        self.assertEqual(cache.get('key1'), 'value1')
    
    def test_eviction(self):
        """Test LRU eviction."""
        cache = LRUCache(max_size=3)
        cache.set('a', 1)
        cache.set('b', 2)
        cache.set('c', 3)
        cache.set('d', 4)  # Should evict 'a'
        
        self.assertIsNone(cache.get('a'))
        self.assertEqual(cache.get('b'), 2)
        self.assertEqual(cache.get('c'), 3)
        self.assertEqual(cache.get('d'), 4)
    
    def test_lru_order(self):
        """Test LRU order is maintained."""
        cache = LRUCache(max_size=3)
        cache.set('a', 1)
        cache.set('b', 2)
        cache.set('c', 3)
        
        # Access 'a' to make it recently used
        cache.get('a')
        
        # Add new item, should evict 'b' (oldest after accessing 'a')
        cache.set('d', 4)
        
        self.assertEqual(cache.get('a'), 1)  # 'a' should still be there
        self.assertIsNone(cache.get('b'))     # 'b' should be evicted
    
    def test_delete(self):
        """Test delete operation."""
        cache = LRUCache(max_size=10)
        cache.set('key', 'value')
        self.assertTrue(cache.delete('key'))
        self.assertIsNone(cache.get('key'))
        self.assertFalse(cache.delete('key'))
    
    def test_contains(self):
        """Test contains operation."""
        cache = LRUCache(max_size=10)
        cache.set('key', 'value')
        self.assertTrue(cache.contains('key'))
        self.assertFalse(cache.contains('nonexistent'))
    
    def test_clear(self):
        """Test clear operation."""
        cache = LRUCache(max_size=10)
        cache.set('a', 1)
        cache.set('b', 2)
        cache.clear()
        self.assertEqual(cache.size(), 0)
    
    def test_ttl_expiration(self):
        """Test TTL expiration."""
        cache = LRUCache(max_size=10, ttl=0.5)
        cache.set('key', 'value')
        self.assertEqual(cache.get('key'), 'value')
        
        time.sleep(0.6)
        self.assertIsNone(cache.get('key'))
    
    def test_per_entry_ttl(self):
        """Test per-entry TTL."""
        cache = LRUCache(max_size=10)
        cache.set('key1', 'value1', ttl=0.5)
        cache.set('key2', 'value2', ttl=5)
        
        time.sleep(0.6)
        self.assertIsNone(cache.get('key1'))
        self.assertEqual(cache.get('key2'), 'value2')
    
    def test_weight_based_eviction(self):
        """Test weight-based eviction."""
        cache = LRUCache(max_size=100, max_weight=10)
        cache.set('a', 'value', weight=5)
        cache.set('b', 'value', weight=5)
        self.assertEqual(cache.weight(), 10)
        
        cache.set('c', 'value', weight=3)  # Should evict 'a'
        self.assertEqual(cache.weight(), 8)
        self.assertIsNone(cache.get('a'))
    
    def test_on_evict_callback(self):
        """Test on_evict callback."""
        evicted = []
        
        def on_evict(key, value):
            evicted.append((key, value))
        
        cache = LRUCache(max_size=2, on_evict=on_evict)
        cache.set('a', 1)
        cache.set('b', 2)
        cache.set('c', 3)
        
        self.assertEqual(evicted, [('a', 1)])
    
    def test_statistics(self):
        """Test cache statistics."""
        cache = LRUCache(max_size=3)
        cache.set('a', 1)
        cache.get('a')  # hit
        cache.get('b')  # miss
        cache.set('b', 2)
        cache.set('c', 3)
        cache.set('d', 4)  # eviction
        
        stats = cache.get_stats()
        self.assertEqual(stats.hits, 1)
        self.assertEqual(stats.misses, 1)
        self.assertEqual(stats.inserts, 4)
        self.assertEqual(stats.evictions, 1)
    
    def test_get_or_set(self):
        """Test get_or_set operation."""
        cache = LRUCache(max_size=10)
        call_count = 0
        
        def factory():
            nonlocal call_count
            call_count += 1
            return 'computed'
        
        result1 = cache.get_or_set('key', factory)
        result2 = cache.get_or_set('key', factory)
        
        self.assertEqual(result1, 'computed')
        self.assertEqual(result2, 'computed')
        self.assertEqual(call_count, 1)
    
    def test_prune_expired(self):
        """Test prune_expired operation."""
        cache = LRUCache(max_size=10)
        cache.set('a', 1, ttl=0.1)
        cache.set('b', 2, ttl=10)
        cache.set('c', 3, ttl=0.1)
        
        time.sleep(0.2)
        count = cache.prune_expired()
        
        self.assertEqual(count, 2)
        self.assertEqual(cache.size(), 1)
        self.assertEqual(cache.get('b'), 2)
    
    def test_dict_interface(self):
        """Test dict-like interface."""
        cache = LRUCache(max_size=10)
        
        # __setitem__ and __getitem__
        cache['key'] = 'value'
        self.assertEqual(cache['key'], 'value')
        
        # __contains__
        self.assertTrue('key' in cache)
        
        # __delitem__
        del cache['key']
        self.assertFalse('key' in cache)
        
        # __len__
        cache['a'] = 1
        cache['b'] = 2
        self.assertEqual(len(cache), 2)
    
    def test_thread_safety(self):
        """Test thread safety."""
        cache = LRUCache(max_size=100)
        errors = []
        
        def writer(start):
            try:
                for i in range(start, start + 100):
                    cache.set(f'key_{i}', i)
            except Exception as e:
                errors.append(e)
        
        def reader(start):
            try:
                for i in range(start, start + 100):
                    cache.get(f'key_{i}')
            except Exception as e:
                errors.append(e)
        
        threads = []
        for i in range(5):
            threads.append(threading.Thread(target=writer, args=(i * 100,)))
            threads.append(threading.Thread(target=reader, args=(i * 100,)))
        
        for t in threads:
            t.start()
        for t in threads:
            t.join()
        
        self.assertEqual(errors, [])


class TestTTLCache(unittest.TestCase):
    """Test TTLCache class."""
    
    def test_basic_operations(self):
        """Test basic set and get."""
        cache = TTLCache(default_ttl=60)
        cache.set('key', 'value')
        self.assertEqual(cache.get('key'), 'value')
    
    def test_expiration(self):
        """Test automatic expiration."""
        cache = TTLCache(default_ttl=0.5)
        cache.set('key', 'value')
        self.assertEqual(cache.get('key'), 'value')
        
        time.sleep(0.6)
        self.assertIsNone(cache.get('key'))
    
    def test_get_ttl(self):
        """Test get_ttl method."""
        cache = TTLCache(default_ttl=10)
        cache.set('key', 'value')
        
        ttl = cache.get_ttl('key')
        self.assertIsNotNone(ttl)
        self.assertGreater(ttl, 8)
        self.assertLessEqual(ttl, 10)
        
        ttl = cache.get_ttl('nonexistent')
        self.assertIsNone(ttl)
    
    def test_extend_ttl(self):
        """Test extend_ttl method."""
        cache = TTLCache(default_ttl=1)
        cache.set('key', 'value')
        
        original_ttl = cache.get_ttl('key')
        self.assertTrue(cache.extend_ttl('key', 5))
        new_ttl = cache.get_ttl('key')
        
        self.assertGreater(new_ttl, original_ttl)
    
    def test_cleanup(self):
        """Test manual cleanup."""
        cache = TTLCache(default_ttl=0.1)
        cache.set('a', 1)
        cache.set('b', 2)
        cache.set('c', 3)
        
        time.sleep(0.2)
        count = cache.cleanup()
        
        self.assertEqual(count, 3)
        self.assertEqual(cache.size(), 0)
    
    def test_max_size(self):
        """Test max size enforcement."""
        cache = TTLCache(default_ttl=60, max_size=3)
        cache.set('a', 1)
        cache.set('b', 2)
        cache.set('c', 3)
        cache.set('d', 4)  # Should evict oldest
        
        self.assertEqual(cache.size(), 3)


class TestLRUCacheDecorator(unittest.TestCase):
    """Test lru_cache decorator."""
    
    def test_basic_caching(self):
        """Test basic function caching."""
        call_count = 0
        
        @lru_cache(maxsize=10)
        def expensive(n):
            nonlocal call_count
            call_count += 1
            return n * n
        
        result1 = expensive(5)
        result2 = expensive(5)
        
        self.assertEqual(result1, 25)
        self.assertEqual(result2, 25)
        self.assertEqual(call_count, 1)
    
    def test_ttl(self):
        """Test TTL in decorator."""
        call_count = 0
        
        @lru_cache(maxsize=10, ttl=0.5)
        def func(n):
            nonlocal call_count
            call_count += 1
            return n
        
        func(1)
        func(1)
        self.assertEqual(call_count, 1)
        
        time.sleep(0.6)
        func(1)
        self.assertEqual(call_count, 2)
    
    def test_typed(self):
        """Test typed parameter."""
        call_count = 0
        
        @lru_cache(maxsize=10, typed=True)
        def func(x):
            nonlocal call_count
            call_count += 1
            return x
        
        # Different types should be cached separately
        result_int = func(1)      # int
        result_float = func(1.0)  # float
        
        # Both should have been computed (not shared cache)
        self.assertEqual(call_count, 2)
    
    def test_cache_clear(self):
        """Test cache_clear method."""
        @lru_cache(maxsize=10)
        def func(n):
            return n
        
        func(1)
        func(2)
        func.cache_clear()
        
        self.assertEqual(len(func.cache), 0)
    
    def test_cache_info(self):
        """Test cache_info method."""
        @lru_cache(maxsize=10)
        def func(n):
            return n
        
        func(1)
        func(1)
        func(2)
        
        info = func.cache_info()
        self.assertEqual(info.hits, 1)
        self.assertEqual(info.inserts, 2)


class TestMultiLevelCache(unittest.TestCase):
    """Test MultiLevelCache class."""
    
    def test_multi_level(self):
        """Test multi-level caching."""
        l1 = LRUCache(max_size=10)
        l2 = LRUCache(max_size=100)
        cache = MultiLevelCache([l1, l2])
        
        # Set in all levels
        cache.set('key', 'value')
        self.assertEqual(l1.get('key'), 'value')
        self.assertEqual(l2.get('key'), 'value')
        
        # Clear L1, should get from L2
        l1.delete('key')
        result = cache.get('key')
        self.assertEqual(result, 'value')
        
        # Should have promoted to L1
        self.assertEqual(l1.get('key'), 'value')
    
    def test_delete_from_all_levels(self):
        """Test delete removes from all levels."""
        l1 = LRUCache(max_size=10)
        l2 = LRUCache(max_size=100)
        cache = MultiLevelCache([l1, l2])
        
        cache.set('key', 'value')
        cache.delete('key')
        
        self.assertIsNone(l1.get('key'))
        self.assertIsNone(l2.get('key'))
    
    def test_clear_all_levels(self):
        """Test clear removes from all levels."""
        l1 = LRUCache(max_size=10)
        l2 = LRUCache(max_size=100)
        cache = MultiLevelCache([l1, l2])
        
        cache.set('a', 1)
        cache.set('b', 2)
        cache.clear()
        
        self.assertEqual(l1.size(), 0)
        self.assertEqual(l2.size(), 0)


class TestCachedFunction(unittest.TestCase):
    """Test CachedFunction class."""
    
    def test_basic_caching(self):
        """Test basic function caching."""
        call_count = 0
        
        def fetch(key):
            nonlocal call_count
            call_count += 1
            return f"value_{key}"
        
        cached = CachedFunction(fetch, ttl=60)
        
        result1 = cached(1)
        result2 = cached(1)
        
        self.assertEqual(result1, "value_1")
        self.assertEqual(result2, "value_1")
        self.assertEqual(call_count, 1)
    
    def test_invalidation(self):
        """Test cache invalidation."""
        call_count = 0
        
        def fetch(key):
            nonlocal call_count
            call_count += 1
            return f"value_{key}"
        
        cached = CachedFunction(fetch, ttl=60)
        cached(1)
        cached.invalidate(1)
        cached(1)
        
        self.assertEqual(call_count, 2)
    
    def test_statistics(self):
        """Test cache statistics."""
        def fetch(key):
            return key
        
        cached = CachedFunction(fetch, ttl=60)
        cached(1)
        cached(1)
        
        stats = cached.get_stats()
        self.assertEqual(stats.hits, 1)
        self.assertEqual(stats.inserts, 1)


class TestBoundedLRUCache(unittest.TestCase):
    """Test BoundedLRUCache class."""
    
    def test_basic_operations(self):
        """Test basic set and get."""
        cache = BoundedLRUCache(max_memory_mb=1)
        cache.set('key', 'value')
        self.assertEqual(cache.get('key'), 'value')
    
    def test_memory_limit(self):
        """Test memory limit enforcement."""
        cache = BoundedLRUCache(max_memory_mb=0.0001)  # ~100 bytes
        
        # Add items until eviction occurs
        cache.set('a', 'x' * 500)
        cache.set('b', 'x' * 500)
        
        # Some should have been evicted
        stats = cache.get_stats()
        self.assertGreater(stats.evictions, 0)
    
    def test_memory_tracking(self):
        """Test memory tracking."""
        cache = BoundedLRUCache(max_memory_mb=1)
        cache.set('key', 'x' * 100)
        
        usage = cache.memory_usage()
        self.assertGreaterEqual(usage, 100)  # At least string length
    
    def test_on_evict_callback(self):
        """Test on_evict callback."""
        evicted = []
        
        def on_evict(key, value):
            evicted.append((key, value))
        
        cache = BoundedLRUCache(max_memory_mb=0.00005, on_evict=on_evict)  # ~50 bytes
        cache.set('a', 'x' * 1000)  # Large enough to trigger eviction
        
        # At least one eviction should have happened
        stats = cache.get_stats()
        self.assertGreater(stats.evictions, 0)


class TestMemoize(unittest.TestCase):
    """Test memoize decorator."""
    
    def test_basic_memoization(self):
        """Test basic memoization."""
        call_count = 0
        
        @memoize()
        def func(n):
            nonlocal call_count
            call_count += 1
            return n * 2
        
        self.assertEqual(func(5), 10)
        self.assertEqual(func(5), 10)
        self.assertEqual(call_count, 1)
    
    def test_with_ttl(self):
        """Test memoization with TTL."""
        call_count = 0
        
        @memoize(ttl=0.5)
        def func(n):
            nonlocal call_count
            call_count += 1
            return n
        
        func(1)
        time.sleep(0.6)
        func(1)
        
        self.assertEqual(call_count, 2)


class TestEdgeCases(unittest.TestCase):
    """Test edge cases and corner scenarios."""
    
    def test_empty_cache(self):
        """Test operations on empty cache."""
        cache = LRUCache(max_size=10)
        self.assertIsNone(cache.get('nonexistent'))
        self.assertFalse(cache.delete('nonexistent'))
        self.assertEqual(cache.size(), 0)
    
    def test_size_one(self):
        """Test cache with size 1."""
        cache = LRUCache(max_size=1)
        cache.set('a', 1)
        cache.set('b', 2)
        
        self.assertIsNone(cache.get('a'))
        self.assertEqual(cache.get('b'), 2)
    
    def test_none_values(self):
        """Test caching None values."""
        cache = LRUCache(max_size=10)
        cache.set('key', None)
        
        # None is a valid cached value
        self.assertEqual(cache.get('key'), None)
    
    def test_zero_ttl(self):
        """Test zero TTL (immediate expiration)."""
        cache = LRUCache(max_size=10, ttl=0)
        cache.set('key', 'value')
        
        # Small delay to ensure expiration
        time.sleep(0.01)
        self.assertIsNone(cache.get('key'))
    
    def test_negative_values(self):
        """Test caching negative values."""
        cache = LRUCache(max_size=10)
        cache.set(-1, -100)
        self.assertEqual(cache.get(-1), -100)
    
    def test_large_keys(self):
        """Test large string keys."""
        cache = LRUCache(max_size=10)
        key = 'x' * 10000
        cache.set(key, 'value')
        self.assertEqual(cache.get(key), 'value')
    
    def test_update_existing(self):
        """Test updating existing entries."""
        cache = LRUCache(max_size=10)
        cache.set('key', 'value1')
        cache.set('key', 'value2')
        
        self.assertEqual(cache.get('key'), 'value2')
        self.assertEqual(cache.size(), 1)
    
    def test_concurrent_reads_writes(self):
        """Test concurrent reads and writes."""
        cache = LRUCache(max_size=1000)
        errors = []
        
        def writer(offset):
            try:
                for i in range(100):
                    cache.set(f'key_{offset}_{i}', i)
            except Exception as e:
                errors.append(e)
        
        def reader(offset):
            try:
                for i in range(100):
                    cache.get(f'key_{offset}_{i}')
            except Exception as e:
                errors.append(e)
        
        with ThreadPoolExecutor(max_workers=20) as executor:
            futures = []
            for i in range(10):
                futures.append(executor.submit(writer, i))
                futures.append(executor.submit(reader, i))
            
            for future in as_completed(futures):
                future.result()
        
        self.assertEqual(errors, [])


if __name__ == '__main__':
    unittest.main(verbosity=2)