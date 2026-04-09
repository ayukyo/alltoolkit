"""
AllToolkit - Python Cache Utils Test Suite

Comprehensive tests for cache utilities covering:
- Basic get/set/delete operations
- TTL expiration
- LRU eviction
- Size limits
- Thread safety
- Statistics tracking
- Bulk operations
- Decorator caching
- Edge cases and error handling

Run: python cache_utils_test.py -v
"""

import time
import threading
import unittest
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from mod import (
    Cache, CacheEntry, CacheStats,
    cached, get_default_cache, cache_get, cache_set, cache_delete, cache_clear,
)


class TestCacheEntry(unittest.TestCase):
    """Tests for CacheEntry dataclass."""
    
    def test_create_entry(self):
        """Test creating a cache entry."""
        entry = CacheEntry(value="test")
        self.assertEqual(entry.value, "test")
        self.assertIsNotNone(entry.created_at)
        self.assertIsNone(entry.expires_at)
        self.assertEqual(entry.access_count, 0)
    
    def test_entry_not_expired_without_ttl(self):
        """Test entry without TTL is never expired."""
        entry = CacheEntry(value="test", expires_at=None)
        self.assertFalse(entry.is_expired())
    
    def test_entry_not_expired_yet(self):
        """Test entry not expired before TTL."""
        future_time = time.time() + 10  # 10 seconds in future
        entry = CacheEntry(value="test", expires_at=future_time)
        self.assertFalse(entry.is_expired())
    
    def test_entry_expired(self):
        """Test entry is expired after TTL."""
        past_time = time.time() - 1  # 1 second in past
        entry = CacheEntry(value="test", expires_at=past_time)
        self.assertTrue(entry.is_expired())
    
    def test_touch_updates_access(self):
        """Test touch updates last_accessed and access_count."""
        entry = CacheEntry(value="test")
        initial_access = entry.access_count
        initial_time = entry.last_accessed
        
        time.sleep(0.01)
        entry.touch()
        
        self.assertEqual(entry.access_count, initial_access + 1)
        self.assertGreater(entry.last_accessed, initial_time)


class TestCacheStats(unittest.TestCase):
    """Tests for CacheStats class."""
    
    def test_initial_stats(self):
        """Test initial statistics values."""
        stats = CacheStats()
        self.assertEqual(stats.hits, 0)
        self.assertEqual(stats.misses, 0)
        self.assertEqual(stats.evictions, 0)
        self.assertEqual(stats.expirations, 0)
        self.assertEqual(stats.hit_rate, 0.0)
    
    def test_record_hit(self):
        """Test recording hits."""
        stats = CacheStats()
        stats.record_hit()
        stats.record_hit()
        self.assertEqual(stats.hits, 2)
    
    def test_record_miss(self):
        """Test recording misses."""
        stats = CacheStats()
        stats.record_miss()
        stats.record_miss()
        stats.record_miss()
        self.assertEqual(stats.misses, 3)
    
    def test_hit_rate_calculation(self):
        """Test hit rate calculation."""
        stats = CacheStats()
        stats.record_hit()
        stats.record_hit()
        stats.record_hit()
        stats.record_miss()
        stats.record_miss()
        
        self.assertEqual(stats.hits, 3)
        self.assertEqual(stats.misses, 2)
        self.assertAlmostEqual(stats.hit_rate, 0.6)
    
    def test_to_dict(self):
        """Test converting stats to dictionary."""
        stats = CacheStats()
        stats.record_hit()
        stats.record_miss()
        
        result = stats.to_dict()
        self.assertIn('hits', result)
        self.assertIn('misses', result)
        self.assertIn('hit_rate', result)
        self.assertEqual(result['hits'], 1)
        self.assertEqual(result['misses'], 1)
    
    def test_reset(self):
        """Test resetting statistics."""
        stats = CacheStats()
        stats.record_hit()
        stats.record_miss()
        stats.record_eviction()
        
        stats.reset()
        
        self.assertEqual(stats.hits, 0)
        self.assertEqual(stats.misses, 0)
        self.assertEqual(stats.evictions, 0)
    
    def test_str_representation(self):
        """Test string representation."""
        stats = CacheStats()
        stats.record_hit()
        stats.record_miss()
        
        str_repr = str(stats)
        self.assertIn('hits=1', str_repr)
        self.assertIn('misses=1', str_repr)


class TestCacheBasic(unittest.TestCase):
    """Basic cache operation tests."""
    
    def setUp(self):
        self.cache = Cache[str](max_size=100)
    
    def test_set_and_get(self):
        """Test basic set and get."""
        self.cache.set("key1", "value1")
        self.assertEqual(self.cache.get("key1"), "value1")
    
    def test_get_nonexistent_key(self):
        """Test getting a key that doesn't exist."""
        self.assertIsNone(self.cache.get("nonexistent"))
    
    def test_get_with_default(self):
        """Test get with default value."""
        result = self.cache.get("nonexistent", "default")
        self.assertEqual(result, "default")
    
    def test_delete_existing_key(self):
        """Test deleting an existing key."""
        self.cache.set("key1", "value1")
        result = self.cache.delete("key1")
        self.assertTrue(result)
        self.assertIsNone(self.cache.get("key1"))
    
    def test_delete_nonexistent_key(self):
        """Test deleting a key that doesn't exist."""
        result = self.cache.delete("nonexistent")
        self.assertFalse(result)
    
    def test_contains(self):
        """Test contains operator."""
        self.cache.set("key1", "value1")
        self.assertIn("key1", self.cache)
        self.assertNotIn("key2", self.cache)
    
    def test_len(self):
        """Test length of cache."""
        self.assertEqual(len(self.cache), 0)
        self.cache.set("key1", "value1")
        self.cache.set("key2", "value2")
        self.assertEqual(len(self.cache), 2)
    
    def test_getitem_setitem(self):
        """Test dictionary-style access."""
        self.cache["key1"] = "value1"
        self.assertEqual(self.cache["key1"], "value1")
    
    def test_delitem(self):
        """Test dictionary-style deletion."""
        self.cache["key1"] = "value1"
        del self.cache["key1"]
        self.assertNotIn("key1", self.cache)
    
    def test_delitem_nonexistent(self):
        """Test deleting nonexistent key raises KeyError."""
        with self.assertRaises(KeyError):
            del self.cache["nonexistent"]
    
    def test_getitem_nonexistent(self):
        """Test getting nonexistent key raises KeyError."""
        with self.assertRaises(KeyError):
            _ = self.cache["nonexistent"]
    
    def test_clear(self):
        """Test clearing cache."""
        self.cache.set("key1", "value1")
        self.cache.set("key2", "value2")
        self.cache.clear()
        self.assertEqual(len(self.cache), 0)
    
    def test_size_property(self):
        """Test size property."""
        self.assertEqual(self.cache.size, 0)
        self.cache.set("key1", "value1")
        self.assertEqual(self.cache.size, 1)
    
    def test_max_size_property(self):
        """Test max_size property."""
        cache = Cache(max_size=50)
        self.assertEqual(cache.max_size, 50)


class TestCacheTTL(unittest.TestCase):
    """TTL expiration tests."""
    
    def setUp(self):
        self.cache = Cache[str](default_ttl=1.0)
    
    def test_ttl_expiration(self):
        """Test that entries expire after TTL."""
        self.cache.set("key1", "value1", ttl=0.1)
        self.assertEqual(self.cache.get("key1"), "value1")
        
        time.sleep(0.15)
        
        self.assertIsNone(self.cache.get("key1"))
    
    def test_default_ttl(self):
        """Test default TTL is applied."""
        self.cache.set("key1", "value1")
        self.assertEqual(self.cache.get("key1"), "value1")
        
        time.sleep(1.1)
        
        self.assertIsNone(self.cache.get("key1"))
    
    def test_ttl_override(self):
        """Test TTL can override default."""
        cache = Cache[str](default_ttl=0.1)
        cache.set("key1", "value1", ttl=1.0)
        
        time.sleep(0.15)
        
        # Should still exist (using overridden TTL)
        self.assertEqual(cache.get("key1"), "value1")
    
    def test_no_expiration_without_ttl(self):
        """Test entries don't expire without TTL."""
        cache = Cache[str]()  # No default TTL
        cache.set("key1", "value1")
        
        time.sleep(0.1)
        
        self.assertEqual(cache.get("key1"), "value1")
    
    def test_ttl_remaining(self):
        """Test getting remaining TTL."""
        self.cache.set("key1", "value1", ttl=1.0)
        remaining = self.cache.ttl("key1")
        
        self.assertIsNotNone(remaining)
        self.assertLessEqual(remaining, 1.0)
        self.assertGreater(remaining, 0.5)
    
    def test_ttl_none_for_no_expiration(self):
        """Test TTL returns None for entries without expiration."""
        cache = Cache[str]()
        cache.set("key1", "value1")
        self.assertIsNone(cache.ttl("key1"))
    
    def test_ttl_none_for_nonexistent(self):
        """Test TTL returns None for nonexistent key."""
        self.assertIsNone(self.cache.ttl("nonexistent"))
    
    def test_touch_resets_ttl(self):
        """Test touch resets TTL."""
        self.cache.set("key1", "value1", ttl=0.2)
        time.sleep(0.1)
        
        # Touch to reset TTL
        self.cache.touch("key1", ttl=0.2)
        time.sleep(0.15)
        
        # Should still exist
        self.assertEqual(self.cache.get("key1"), "value1")
    
    def test_expire_method(self):
        """Test manual expiration of entries."""
        self.cache.set("key1", "value1", ttl=0.1)
        self.cache.set("key2", "value2", ttl=10.0)
        
        time.sleep(0.15)
        
        removed = self.cache.expire()
        self.assertEqual(removed, 1)
        self.assertNotIn("key1", self.cache)
        self.assertIn("key2", self.cache)


class TestCacheLRU(unittest.TestCase):
    """LRU eviction tests."""
    
    def setUp(self):
        self.cache = Cache[str](max_size=3)
    
    def test_lru_eviction(self):
        """Test LRU eviction when cache is full."""
        self.cache.set("key1", "value1")
        self.cache.set("key2", "value2")
        self.cache.set("key3", "value3")
        
        # This should evict key1 (least recently used)
        self.cache.set("key4", "value4")
        
        self.assertNotIn("key1", self.cache)
        self.assertIn("key2", self.cache)
        self.assertIn("key3", self.cache)
        self.assertIn("key4", self.cache)
    
    def test_access_updates_lru(self):
        """Test that accessing a key updates its LRU position."""
        self.cache.set("key1", "value1")
        self.cache.set("key2", "value2")
        self.cache.set("key3", "value3")
        
        # Access key1 to make it recently used
        self.cache.get("key1")
        
        # This should evict key2 (now least recently used)
        self.cache.set("key4", "value4")
        
        self.assertIn("key1", self.cache)
        self.assertNotIn("key2", self.cache)
    
    def test_set_updates_lru(self):
        """Test that setting an existing key updates its LRU position."""
        self.cache.set("key1", "value1")
        self.cache.set("key2", "value2")
        self.cache.set("key3", "value3")
        
        # Update key1
        self.cache.set("key1", "new_value1")
        
        # This should evict key2
        self.cache.set("key4", "value4")
        
        self.assertIn("key1", self.cache)
        self.assertEqual(self.cache.get("key1"), "new_value1")
        self.assertNotIn("key2", self.cache)


class TestCacheStatsTracking(unittest.TestCase):
    """Statistics tracking tests."""
    
    def test_stats_enabled(self):
        """Test that stats are tracked when enabled."""
        cache = Cache[str](enable_stats=True)
        cache.set("key1", "value1")
        cache.get("key1")
        cache.get("key2")
        
        stats = cache.stats
        self.assertIsNotNone(stats)
        self.assertEqual(stats.sets, 1)
        self.assertEqual(stats.hits, 1)
        self.assertEqual(stats.misses, 1)
    
    def test_stats_disabled(self):
        """Test that stats are not tracked when disabled."""
        cache = Cache[str](enable_stats=False)
        cache.set("key1", "value1")
        cache.get("key1")
        
        self.assertIsNone(cache.stats)
    
    def test_eviction_stats(self):
        """Test eviction statistics."""
        cache = Cache[str](max_size=2, enable_stats=True)
        cache.set("key1", "value1")
        cache.set("key2", "value2")
        cache.set("key3", "value3")  # Should evict key1
        
        stats = cache.stats
        self.assertGreater(stats.evictions, 0)
    
    def test_expiration_stats(self):
        """Test expiration statistics."""
        cache = Cache[str](enable_stats=True)
        cache.set("key1", "value1", ttl=0.1)
        
        time.sleep(0.15)
        cache.get("key1")  # Should trigger expiration
        
        stats = cache.stats
        self.assertGreater(stats.expirations, 0)


class TestCacheBulkOperations(unittest.TestCase):
    """Bulk operation tests."""
    
    def setUp(self):
        self.cache = Cache[str](max_size=100)
    
    def test_get_many(self):
        """Test getting multiple keys."""
        self.cache.set("key1", "value1")
        self.cache.set("key2", "value2")
        self.cache.set("key3", "value3")
        
        result = self.cache.get_many(["key1", "key2", "nonexistent"])
        
        self.assertEqual(len(result), 2)
        self.assertEqual(result["key1"], "value1")
        self.assertEqual(result["key2"], "value2")
    
    def test_set_many(self):
        """Test setting multiple keys."""
        items = {"key1": "value1", "key2": "value2", "key3": "value3"}
        self.cache.set_many(items)
        
        self.assertEqual(self.cache.get("key1"), "value1")
        self.assertEqual(self.cache.get("key2"), "value2")
        self.assertEqual(self.cache.get("key3"), "value3")
    
    def test_delete_many(self):
        """Test deleting multiple keys."""
        self.cache.set("key1", "value1")
        self.cache.set("key2", "value2")
        self.cache.set("key3", "value3")
        
        count = self.cache.delete_many(["key1", "key3", "nonexistent"])
        
        self.assertEqual(count, 2)
        self.assertNotIn("key1", self.cache)
        self.assertIn("key2", self.cache)
        self.assertNotIn("key3", self.cache)
    
    def test_keys(self):
        """Test getting all keys."""
        self.cache.set("key1", "value1")
        self.cache.set("key2", "value2")
        
        keys = self.cache.keys()
        self.assertEqual(len(keys), 2)
        self.assertIn("key1", keys)
        self.assertIn("key2", keys)
    
    def test_values(self):
        """Test getting all values."""
        self.cache.set("key1", "value1")
        self.cache.set("key2", "value2")
        
        values = self.cache.values()
        self.assertEqual(len(values), 2)
        self.assertIn("value1", values)
        self.assertIn("value2", values)
    
    def test_items(self):
        """Test getting all items."""
        self.cache.set("key1", "value1")
        self.cache.set("key2", "value2")
        
        items = self.cache.items()
        self.assertEqual(len(items), 2)
        
        item_dict = dict(items)
        self.assertEqual(item_dict["key1"], "value1")
        self.assertEqual(item_dict["key2"], "value2")


class TestCacheAdvanced(unittest.TestCase):
    """Advanced feature tests."""
    
    def setUp(self):
        self.cache = Cache[int](max_size=100)
    
    def test_increment(self):
        """Test atomic increment."""
        self.cache.set("counter", 10)
        result = self.cache.increment("counter", 5)
        self.assertEqual(result, 15)
        self.assertEqual(self.cache.get("counter"), 15)
    
    def test_increment_nonexistent(self):
        """Test increment on nonexistent key."""
        result = self.cache.increment("counter", 1, default=0)
        self.assertEqual(result, 1)
    
    def test_increment_non_numeric(self):
        """Test increment on non-numeric value."""
        self.cache.set("key", "not_a_number")
        result = self.cache.increment("key", 1, default=10)
        self.assertEqual(result, 11)
    
    def test_decrement(self):
        """Test atomic decrement."""
        self.cache.set("counter", 10)
        result = self.cache.decrement("counter", 3)
        self.assertEqual(result, 7)
    
    def test_get_or_set(self):
        """Test get_or_set functionality."""
        call_count = [0]
        
        def factory():
            call_count[0] += 1
            return "computed_value"
        
        # First call should compute
        result1 = self.cache.get_or_set("key", factory)
        self.assertEqual(result1, "computed_value")
        self.assertEqual(call_count[0], 1)
        
        # Second call should use cache
        result2 = self.cache.get_or_set("key", factory)
        self.assertEqual(result2, "computed_value")
        self.assertEqual(call_count[0], 1)  # Still 1
    
    def test_get_or_set_with_ttl(self):
        """Test get_or_set with TTL."""
        call_count = [0]
        
        def factory():
            call_count[0] += 1
            return "computed_value"
        
        self.cache.get_or_set("key", factory, ttl=0.1)
        
        time.sleep(0.15)
        
        # Should recompute after expiration
        self.cache.get_or_set("key", factory, ttl=0.1)
        self.assertEqual(call_count[0], 2)
    
    def test_warm(self):
        """Test cache warming."""
        items = {"key1": "value1", "key2": "value2"}
        
        # Warm empty cache
        count = self.cache.warm(items)
        self.assertEqual(count, 2)
        
        # Warm with existing keys (should not add)
        count = self.cache.warm(items)
        self.assertEqual(count, 0)
    
    def test_to_dict(self):
        """Test exporting cache to dictionary."""
        self.cache.set("key1", "value1", ttl=10.0)
        
        result = self.cache.to_dict()
        
        self.assertIn('items', result)
        self.assertIn('size', result)
        self.assertIn('max_size', result)
        self.assertIn('default_ttl', result)
        self.assertIn('stats', result)
        
        self.assertEqual(result['size'], 1)
        self.assertIn('key1', result['items'])


class TestCacheDecorator(unittest.TestCase):
    """Tests for @cached decorator."""
    
    def test_cached_decorator(self):
        """Test basic caching with decorator."""
        call_count = [0]
        
        @cached(ttl=1.0)
        def expensive_function(x, y):
            call_count[0] += 1
            return x + y
        
        result1 = expensive_function(1, 2)
        result2 = expensive_function(1, 2)
        
        self.assertEqual(result1, 3)
        self.assertEqual(result2, 3)
        self.assertEqual(call_count[0], 1)  # Only called once
    
    def test_cached_decorator_different_args(self):
        """Test caching with different arguments."""
        call_count = [0]
        
        @cached(ttl=1.0)
        def func(x):
            call_count[0] += 1
            return x * 2
        
        func(1)
        func(2)
        func(1)  # Should use cache
        
        self.assertEqual(call_count[0], 2)
    
    def test_cached_decorator_with_prefix(self):
        """Test caching with key prefix."""
        @cached(key_prefix="myprefix")
        def func(x):
            return x
        
        cache = func.cache
        func(1)
        
        # Check key has prefix
        keys = cache.keys()
        self.assertTrue(any("myprefix" in k for k in keys))
    
    def test_cached_decorator_shared_cache(self):
        """Test multiple functions sharing a cache."""
        shared_cache = Cache()
        
        @cached(cache=shared_cache, ttl=1.0)
        def func1(x):
            return x + 1
        
        @cached(cache=shared_cache, ttl=1.0)
        def func2(x):
            return x + 2
        
        func1(1)
        func2(2)
        
        self.assertEqual(len(shared_cache), 2)


class TestCacheThreadSafety(unittest.TestCase):
    """Thread safety tests."""
    
    def test_concurrent_set_get(self):
        """Test concurrent set and get operations."""
        cache = Cache[int](max_size=1000)
        errors = []
        
        def worker(thread_id):
            try:
                for i in range(100):
                    key = f"thread_{thread_id}_key_{i}"
                    cache.set(key, i)
                    value = cache.get(key)
                    if value != i:
                        errors.append(f"Thread {thread_id}: Expected {i}, got {value}")
            except Exception as e:
                errors.append(f"Thread {thread_id}: {e}")
        
        threads = []
        for i in range(10):
            t = threading.Thread(target=worker, args=(i,))
            threads.append(t)
            t.start()
        
        for t in threads:
            t.join()
        
        self.assertEqual(len(errors), 0, f"Errors occurred: {errors}")
    
    def test_concurrent_increment(self):
        """Test concurrent increment operations."""
        cache = Cache[int]()
        cache.set("counter", 0)
        num_threads = 10
        increments_per_thread = 100
        
        def worker():
            for _ in range(increments_per_thread):
                cache.increment("counter", 1)
        
        threads = []
        for _ in range(num_threads):
            t = threading.Thread(target=worker)
            threads.append(t)
            t.start()
        
        for t in threads:
            t.join()
        
        expected = num_threads * increments_per_thread
        self.assertEqual(cache.get("counter"), expected)


class TestCacheEdgeCases(unittest.TestCase):
    """Edge case and error handling tests."""
    
    def test_none_value(self):
        """Test caching None value."""
        cache = Cache()
        cache.set("key", None)
        self.assertIsNone(cache.get("key", "default"))  # Should return None, not default
    
    def test_contains_with_expired(self):
        """Test contains returns False for expired entries."""
        cache = Cache()
        cache.set("key", "value", ttl=0.1)
        
        time.sleep(0.15)
        
        self.assertNotIn("key", cache)
    
    def test_zero_max_size(self):
        """Test cache with max_size=0."""
        cache = Cache(max_size=0)
        cache.set("key", "value")
        # Should not be able to store anything
        self.assertEqual(len(cache), 0)
    
    def test_large_max_size(self):
        """Test cache with very large max_size."""
        cache = Cache(max_size=1000000)
        cache.set("key", "value")
        self.assertIn("key", cache)
    
    def test_special_characters_in_key(self):
        """Test keys with special characters."""
        cache = Cache()
        special_keys = [
            "key with spaces",
            "key:with:colons",
            "key/with/slashes",
            "key\\with\\backslashes",
            "key\twith\ttabs",
            "key\nwith\nnewlines",
            "key with unicode: 你好",
        ]
        
        for key in special_keys:
            cache.set(key, f"value_for_{key}")
            self.assertEqual(cache.get(key), f"value_for_{key}")
    
    def test_unicode_value(self):
        """Test caching unicode values."""
        cache = Cache[str]()
        unicode_value = "你好世界 🌍 Привет мир"
        cache.set("unicode_key", unicode_value)
        self.assertEqual(cache.get("unicode_key"), unicode_value)
    
    def test_complex_object(self):
        """Test caching complex objects."""
        cache = Cache[dict]()
        complex_obj = {
            "nested": {"key": "value"},
            "list": [1, 2, 3],
            "tuple": (4, 5, 6),
        }
        cache.set("complex", complex_obj)
        self.assertEqual(cache.get("complex"), complex_obj)


class TestModuleLevelFunctions(unittest.TestCase):
    """Tests for module-level convenience functions."""
    
    def tearDown(self):
        """Clear default cache after each test."""
        global _default_cache
        from mod import _default_cache
        if _default_cache:
            _default_cache.clear()
    
    def test_default_cache_get_set(self):
        """Test default cache get and set."""
        cache_set("test_key", "test_value")
        result = cache_get("test_key")
        self.assertEqual(result, "test_value")
    
    def test_default_cache_delete(self):
        """Test default cache delete."""
        cache_set("test_key", "test_value")
        result = cache_delete("test_key")
        self.assertTrue(result)
        self.assertIsNone(cache_get("test_key"))
    
    def test_default_cache_clear(self):
        """Test default cache clear."""
        cache_set("key1", "value1")
        cache_set("key2", "value2")
        cache_clear()
        self.assertIsNone(cache_get("key1"))
        self.assertIsNone(cache_get("key2"))
    
    def test_get_default_cache(self):
        """Test get_default_cache returns same instance."""
        cache1 = get_default_cache()
        cache2 = get_default_cache()
        self.assertIs(cache1, cache2)


class TestCacheIntegration(unittest.TestCase):
    """Integration tests for complete workflows."""
    
    def test_complete_workflow(self):
        """Test complete cache workflow."""
        cache = Cache[str](max_size=5, default_ttl=1.0, enable_stats=True)
        
        # Set values
        cache.set("a", "1")
        cache.set("b", "2")
        cache.set("c", "3")
        
        # Get values
        self.assertEqual(cache.get("a"), "1")
        self.assertEqual(cache.get("b"), "2")
        
        # Bulk operations
        cache.set_many({"d": "4", "e": "5"})
        result = cache.get_many(["a", "b", "c", "d", "e"])
        self.assertEqual(len(result), 5)
        
        # Increment
        cache.set("counter", 10)
        cache.increment("counter", 5)
        self.assertEqual(cache.get("counter"), 15)
        
        # Check stats
        stats = cache.stats
        self.assertGreater(stats.hits, 0)
        self.assertGreater(stats.sets, 0)
        
        # Export
        export = cache.to_dict()
        self.assertEqual(export['size'], 6)  # a, b, c, d, e, counter
    
    def test_lru_under_pressure(self):
        """Test LRU behavior under heavy load."""
        cache = Cache[int](max_size=10)
        
        # Insert 100 items
        for i in range(100):
            cache.set(f"key_{i}", i)
        
        # Should only have 10 items
        self.assertEqual(len(cache), 10)
        
        # Last 10 items should be present
        for i in range(90, 100):
            self.assertIn(f"key_{i}", cache)
        
        # First items should be evicted
        for i in range(90):
            self.assertNotIn(f"key_{i}", cache)


if __name__ == '__main__':
    unittest.main(verbosity=2)
