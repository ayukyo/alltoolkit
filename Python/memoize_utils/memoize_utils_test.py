#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AllToolkit - Memoize Utilities Tests

Tests for the memoize_utils module.
"""

import pytest
import time
from mod import (
    LRUCache,
    TTLCache,
    memoize,
    memoize_err,
    memoize2,
    memoize2_err,
    Entry,
    CacheStats,
    expired_entries,
    purge_map,
)


class TestEntry:
    """Tests for Entry class."""

    def test_entry_creation(self):
        """Test creating an Entry."""
        entry = Entry('value')
        assert entry.value == 'value'
        assert entry.access_count == 0

    def test_entry_not_expired_initially(self):
        """Test that entry is not expired initially."""
        entry = Entry('value', ttl=100)
        assert entry.is_expired() is False

    def test_entry_expired(self):
        """Test that entry becomes expired."""
        entry = Entry('value', ttl=0.01)
        time.sleep(0.02)
        assert entry.is_expired() is True

    def test_entry_age(self):
        """Test entry age calculation."""
        entry = Entry('value')
        time.sleep(0.01)
        assert entry.age() > 0

    def test_entry_ttl(self):
        """Test entry TTL calculation."""
        entry = Entry('value', ttl=1)
        time.sleep(0.01)
        ttl = entry.ttl()
        assert ttl > 0
        assert ttl <= 1


class TestCacheStats:
    """Tests for CacheStats class."""

    def test_cache_stats_creation(self):
        """Test creating CacheStats."""
        stats = CacheStats()
        assert stats.hits == 0
        assert stats.misses == 0

    def test_cache_stats_repr(self):
        """Test CacheStats string representation."""
        stats = CacheStats()
        repr_str = repr(stats)
        assert 'CacheStats' in repr_str


class TestLRUCache:
    """Tests for LRUCache class."""

    def test_cache_set_get(self):
        """Test basic set and get."""
        cache = LRUCache()
        cache.set('key', 'value')
        value, found = cache.get('key')
        assert found is True
        assert value == 'value'

    def test_cache_get_not_found(self):
        """Test getting non-existent key."""
        cache = LRUCache()
        value, found = cache.get('nonexistent')
        assert found is False
        assert value is None

    def test_cache_has(self):
        """Test has method."""
        cache = LRUCache()
        cache.set('key', 'value')
        assert cache.has('key') is True
        assert cache.has('nonexistent') is False

    def test_cache_delete(self):
        """Test deleting a key."""
        cache = LRUCache()
        cache.set('key', 'value')
        assert cache.delete('key') is True
        assert cache.has('key') is False

    def test_cache_delete_not_found(self):
        """Test deleting non-existent key."""
        cache = LRUCache()
        assert cache.delete('nonexistent') is False

    def test_cache_clear(self):
        """Test clearing cache."""
        cache = LRUCache()
        cache.set('key1', 'value1')
        cache.set('key2', 'value2')
        cache.clear()
        assert cache.size() == 0

    def test_cache_size(self):
        """Test size method."""
        cache = LRUCache()
        cache.set('key1', 'value1')
        cache.set('key2', 'value2')
        assert cache.size() == 2

    def test_cache_keys(self):
        """Test keys method."""
        cache = LRUCache()
        cache.set('key1', 'value1')
        cache.set('key2', 'value2')
        keys = cache.keys()
        assert 'key1' in keys
        assert 'key2' in keys

    def test_cache_lru_eviction(self):
        """Test LRU eviction when max size is reached."""
        cache = LRUCache(max_size=2)
        cache.set('key1', 'value1')
        cache.set('key2', 'value2')
        cache.set('key3', 'value3')
        # key1 should be evicted
        assert cache.has('key1') is False
        assert cache.has('key2') is True
        assert cache.has('key3') is True

    def test_cache_lru_update(self):
        """Test that accessing a key updates its LRU position."""
        cache = LRUCache(max_size=2)
        cache.set('key1', 'value1')
        cache.set('key2', 'value2')
        cache.get('key1')  # Access key1
        cache.set('key3', 'value3')
        # key2 should be evicted (it was LRU)
        assert cache.has('key2') is False
        assert cache.has('key1') is True

    def test_cache_update_existing(self):
        """Test updating an existing key."""
        cache = LRUCache()
        cache.set('key', 'value1')
        cache.set('key', 'value2')
        value, found = cache.get('key')
        assert found is True
        assert value == 'value2'

    def test_cache_ttl_expiration(self):
        """Test TTL expiration."""
        cache = LRUCache(ttl=0.01)
        cache.set('key', 'value')
        time.sleep(0.02)
        value, found = cache.get('key')
        assert found is False

    def test_cache_purge_expired(self):
        """Test purge_expired method."""
        cache = LRUCache(ttl=0.01)
        cache.set('key1', 'value1')
        cache.set('key2', 'value2')
        time.sleep(0.02)
        count = cache.purge_expired()
        assert count == 2
        assert cache.size() == 0

    def test_cache_get_or_compute(self):
        """Test get_or_compute method."""
        cache = LRUCache()
        computed = cache.get_or_compute('key', lambda: 'computed')
        assert computed == 'computed'
        # Second call should return cached value
        computed = cache.get_or_compute('key', lambda: 'different')
        assert computed == 'computed'


class TestTTLCache:
    """Tests for TTLCache class."""

    def test_ttl_cache_set_get(self):
        """Test basic set and get."""
        cache = TTLCache(ttl=60)
        cache.set('key', 'value')
        value, found = cache.get('key')
        assert found is True
        assert value == 'value'

    def test_ttl_cache_expiration(self):
        """Test TTL expiration."""
        cache = TTLCache(ttl=0.01)
        cache.set('key', 'value')
        time.sleep(0.02)
        value, found = cache.get('key')
        assert found is False

    def test_ttl_cache_delete(self):
        """Test deleting a key."""
        cache = TTLCache(ttl=60)
        cache.set('key', 'value')
        assert cache.delete('key') is True
        assert cache.has('key') is False


class TestMemoizeDecorators:
    """Tests for memoize decorator functions."""

    def test_memoize_single_arg(self):
        """Test memoizing single-argument function."""
        call_count = [0]
        
        @memoize(max_size=100)
        def expensive_func(n):
            call_count[0] += 1
            return n * 2
        
        assert expensive_func(5) == 10
        assert expensive_func(5) == 10  # Cached
        assert call_count[0] == 1

    def test_memoize_ttl(self):
        """Test memoize with TTL."""
        @memoize(ttl=0.01)
        def func(n):
            return n * 2
        
        assert func(5) == 10
        time.sleep(0.02)
        assert func(5) == 10  # Cache expired
        assert func(5) == 10  # New value

    def test_memoize_max_size(self):
        """Test memoize with max_size."""
        @memoize(max_size=2)
        def func(n):
            return n * 2
        
        func(1)
        func(2)
        func(3)  # Should evict func(1)
        func(1)  # Should recompute
        assert func(1) == 2


class TestMemoize2Decorators:
    """Tests for memoize2 decorator function."""

    def test_memoize2_two_args(self):
        """Test memoizing two-argument function."""
        call_count = [0]
        
        @memoize2(max_size=100)
        def add(a, b):
            call_count[0] += 1
            return a + b
        
        assert add(1, 2) == 3
        assert add(1, 2) == 3  # Cached
        assert call_count[0] == 1


class TestUtilityFunctions:
    """Tests for utility functions."""

    def test_expired_entries(self):
        """Test expired_entries function."""
        m = {}
        entry1 = Entry('value', ttl=60)
        entry2 = Entry('value', ttl=0.001)
        m['key1'] = entry1
        m['key2'] = entry2
        time.sleep(0.02)
        assert expired_entries(m) == 1

    def test_purge_map(self):
        """Test purge_map function."""
        m = {}
        entry1 = Entry('value', ttl=60)
        entry2 = Entry('value', ttl=0.001)
        m['key1'] = entry1
        m['key2'] = entry2
        time.sleep(0.02)
        count = purge_map(m)
        assert count == 1
        assert len(m) == 1


class TestThreadSafety:
    """Tests for thread safety features."""

    def test_cache_concurrent_access(self):
        """Test that cache handles concurrent access."""
        import threading
        
        cache = LRUCache(max_size=100)
        results = []
        
        def worker(key):
            cache.set(key, f'value_{key}')
            value, found = cache.get(key)
            if found:
                results.append(value)
        
        threads = [threading.Thread(target=worker, args=(i,)) for i in range(10)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()
        
        assert len(results) == 10


class TestEdgeCases:
    """Tests for edge cases."""

    def test_cache_with_zero_max_size(self):
        """Test cache with max_size=0 (unlimited)."""
        cache = LRUCache(max_size=0)
        for i in range(100):
            cache.set(f'key{i}', f'value{i}')
        assert cache.size() == 100

    def test_cache_with_custom_ttl(self):
        """Test setting custom TTL on individual entries."""
        cache = LRUCache(ttl=60)
        cache.set('key1', 'value1', ttl=0.01)
        time.sleep(0.02)
        assert cache.has('key1') is False
        # Other key with default TTL should still work
        cache.set('key2', 'value2')
        assert cache.has('key2') is True

    def test_get_or_compute_with_error(self):
        """Test get_or_compute_with_error method."""
        cache = LRUCache()
        
        def compute():
            return None, ValueError("test error")
        
        value, error = cache.get_or_compute_with_error('key', compute)
        assert value is None
        assert error is not None

    def test_entry_no_expiration(self):
        """Test entry with no TTL (never expires)."""
        entry = Entry('value', ttl=None)
        assert entry.is_expired() is False
        assert entry.ttl() == -1.0


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
