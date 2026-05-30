# Tests for memoize_utils

import time
import unittest
from typing import Tuple, Optional

from mod import (
    Entry, CacheStats, LRUCache, TTLCache,
    memoize, memoize_err, memoize2, memoize2_err,
    expired_entries, purge_map
)


class TestEntry(unittest.TestCase):
    """Tests for Entry class."""

    def test_entry_no_expiry(self):
        """Entry with no TTL should not expire."""
        entry = Entry("value")
        self.assertFalse(entry.is_expired())
        self.assertEqual(entry.value, "value")

    def test_entry_with_ttl(self):
        """Entry with TTL should expire after TTL passes."""
        entry = Entry("value", ttl=0.1)
        self.assertFalse(entry.is_expired())
        time.sleep(0.15)
        self.assertTrue(entry.is_expired())

    def test_entry_age(self):
        """Age should return time since creation."""
        entry = Entry("value")
        time.sleep(0.05)
        self.assertGreater(entry.age(), 0.04)

    def test_entry_ttl(self):
        """TTL should return remaining time."""
        entry = Entry("value", ttl=1.0)
        ttl = entry.ttl()
        self.assertGreater(ttl, 0.9)
        self.assertLessEqual(ttl, 1.0)


class TestCacheStats(unittest.TestCase):
    """Tests for CacheStats class."""

    def test_cache_stats_repr(self):
        """Stats should have proper string representation."""
        stats = CacheStats()
        stats.hits = 80
        stats.misses = 20
        repr_str = repr(stats)
        self.assertIn("80", repr_str)
        self.assertIn("20", repr_str)


class TestLRUCache(unittest.TestCase):
    """Tests for LRUCache class."""

    def test_cache_basic_operations(self):
        """Test basic set/get operations."""
        cache = LRUCache(max_size=10)
        cache.set("key1", "value1")
        value, found = cache.get("key1")
        self.assertTrue(found)
        self.assertEqual(value, "value1")

    def test_cache_get_not_found(self):
        """Getting non-existent key should return not found."""
        cache = LRUCache()
        value, found = cache.get("nonexistent")
        self.assertFalse(found)
        self.assertIsNone(value)

    def test_cache_lru_eviction(self):
        """Cache should evict least recently used when full."""
        cache = LRUCache(max_size=3)
        cache.set("a", 1)
        cache.set("b", 2)
        cache.set("c", 3)
        cache.set("d", 4)  # Should evict 'a'

        self.assertFalse(cache.has("a"))
        self.assertTrue(cache.has("b"))
        self.assertTrue(cache.has("c"))
        self.assertTrue(cache.has("d"))

    def test_cache_update_existing(self):
        """Updating existing key should update value and move to front."""
        cache = LRUCache(max_size=3)
        cache.set("a", 1)
        cache.set("b", 2)
        cache.set("a", 10)  # Update 'a'
        cache.set("c", 3)
        cache.set("d", 4)  # Should evict 'b' (least recently used)

        value, found = cache.get("a")
        self.assertTrue(found)
        self.assertEqual(value, 10)

    def test_cache_ttl_expiration(self):
        """Entries should expire after TTL."""
        cache = LRUCache(max_size=10, ttl=0.1)
        cache.set("key", "value")
        self.assertTrue(cache.has("key"))
        time.sleep(0.15)
        self.assertFalse(cache.has("key"))

    def test_cache_delete(self):
        """Delete should remove entry."""
        cache = LRUCache()
        cache.set("key", "value")
        self.assertTrue(cache.delete("key"))
        self.assertFalse(cache.has("key"))
        self.assertFalse(cache.delete("nonexistent"))

    def test_cache_clear(self):
        """Clear should remove all entries."""
        cache = LRUCache()
        cache.set("a", 1)
        cache.set("b", 2)
        cache.clear()
        self.assertEqual(cache.size(), 0)

    def test_cache_has(self):
        """Has should check existence."""
        cache = LRUCache()
        cache.set("key", "value")
        self.assertTrue(cache.has("key"))
        self.assertFalse(cache.has("nonexistent"))

    def test_cache_size(self):
        """Size should return correct count."""
        cache = LRUCache()
        self.assertEqual(cache.size(), 0)
        cache.set("a", 1)
        cache.set("b", 2)
        self.assertEqual(cache.size(), 2)

    def test_cache_keys(self):
        """Keys should return all keys."""
        cache = LRUCache()
        cache.set("a", 1)
        cache.set("b", 2)
        keys = cache.keys()
        self.assertEqual(set(keys), {"a", "b"})

    def test_cache_purge_expired(self):
        """Purge expired should remove expired entries."""
        cache = LRUCache(ttl=0.05)
        cache.set("a", 1)
        cache.set("b", 2)
        time.sleep(0.1)
        count = cache.purge_expired()
        self.assertEqual(count, 2)
        self.assertEqual(cache.size(), 0)

    def test_cache_stats(self):
        """Stats should track hits and misses."""
        cache = LRUCache(stats_enabled=True)
        cache.set("a", 1)
        cache.get("a")  # Hit
        cache.get("b")  # Miss
        stats = cache.get_stats()
        self.assertEqual(stats.hits, 1)
        self.assertEqual(stats.misses, 1)

    def test_cache_get_or_compute(self):
        """Get or compute should compute if not found."""
        cache = LRUCache()
        call_count = [0]

        def compute():
            call_count[0] += 1
            return 42

        result = cache.get_or_compute("key", compute)
        self.assertEqual(result, 42)
        self.assertEqual(call_count[0], 1)

        result = cache.get_or_compute("key", compute)
        self.assertEqual(result, 42)
        self.assertEqual(call_count[0], 1)  # Not recomputed

    def test_cache_get_or_compute_with_error(self):
        """Get or compute should propagate errors."""
        cache = LRUCache()

        def compute():
            return None, ValueError("test error")

        value, err = cache.get_or_compute_with_error("key", compute)
        self.assertIsNone(value)
        self.assertIsInstance(err, ValueError)

    def test_cache_on_evict_callback(self):
        """On evict callback should be called when entries are evicted."""
        evicted = []

        def on_evict(key, value):
            evicted.append((key, value))

        cache = LRUCache(max_size=2, on_evict=on_evict)
        cache.set("a", 1)
        cache.set("b", 2)
        cache.set("c", 3)  # Should evict 'a'

        self.assertEqual(evicted, [("a", 1)])

    def test_cache_generic_types(self):
        """Cache should work with various types."""
        cache = LRUCache[int, str](max_size=10)
        cache.set(1, "one")
        cache.set(2, "two")
        value, found = cache.get(1)
        self.assertTrue(found)
        self.assertEqual(value, "one")


class TestTTLCache(unittest.TestCase):
    """Tests for TTLCache class."""

    def test_ttl_cache_basic(self):
        """TTL cache should work correctly."""
        cache = TTLCache(ttl=1.0)
        cache.set("key", "value")
        value, found = cache.get("key")
        self.assertTrue(found)
        self.assertEqual(value, "value")

    def test_ttl_cache_expiration(self):
        """TTL cache entries should expire."""
        cache = TTLCache(ttl=0.1)
        cache.set("key", "value")
        time.sleep(0.15)
        value, found = cache.get("key")
        self.assertFalse(found)

    def test_ttl_cache_custom_ttl(self):
        """Custom TTL should override default."""
        cache = TTLCache(ttl=0.05)
        cache.set("key", "value", ttl=1.0)
        time.sleep(0.1)
        value, found = cache.get("key")
        self.assertTrue(found)  # Should still exist


class TestMemoizeDecorator(unittest.TestCase):
    """Tests for memoize decorator."""

    def test_memoize_single_arg(self):
        """Memoize should cache single argument function."""
        call_count = [0]

        @memoize(max_size=10, ttl=60)
        def expensive_func(n):
            call_count[0] += 1
            return n * 2

        result = expensive_func(5)
        self.assertEqual(result, 10)
        self.assertEqual(call_count[0], 1)

        result = expensive_func(5)
        self.assertEqual(result, 10)
        self.assertEqual(call_count[0], 1)  # Not recomputed

        result = expensive_func(10)
        self.assertEqual(result, 20)
        self.assertEqual(call_count[0], 2)

    def test_memoize_err(self):
        """Memoize with error should handle errors."""
        call_count = [0]

        @memoize_err(max_size=10)
        def func_with_error(n):
            call_count[0] += 1
            if n < 0:
                return None, ValueError("negative not allowed")
            return n * 2, None

        result, err = func_with_error(5)
        self.assertEqual(result, 10)
        self.assertIsNone(err)

        result, err = func_with_error(-1)
        self.assertIsNone(result)
        self.assertIsInstance(err, ValueError)

        # Original call should not be cached due to error
        result, err = func_with_error(-1)
        self.assertIsNone(result)
        self.assertEqual(call_count[0], 3)

    def test_memoize2(self):
        """Memoize2 should cache two argument function."""
        call_count = [0]

        @memoize2(max_size=10)
        def add(a, b):
            call_count[0] += 1
            return a + b

        result = add(1, 2)
        self.assertEqual(result, 3)
        self.assertEqual(call_count[0], 1)

        result = add(1, 2)
        self.assertEqual(result, 3)
        self.assertEqual(call_count[0], 1)  # Cached

        result = add(3, 4)
        self.assertEqual(result, 7)
        self.assertEqual(call_count[0], 2)


class TestUtilityFunctions(unittest.TestCase):
    """Tests for utility functions."""

    def test_expired_entries(self):
        """Expired entries should count correctly."""
        m = {
            "a": Entry("value", ttl=0.1),
            "b": Entry("value", ttl=0.1),
        }
        self.assertEqual(expired_entries(m), 0)
        time.sleep(0.15)
        self.assertEqual(expired_entries(m), 2)

    def test_purge_map(self):
        """Purge map should remove expired entries."""
        m = {
            "a": Entry("value", ttl=0.1),
            "b": Entry("value", ttl=0.1),
        }
        time.sleep(0.15)
        count = purge_map(m)
        self.assertEqual(count, 2)
        self.assertEqual(len(m), 0)


if __name__ == "__main__":
    unittest.main()