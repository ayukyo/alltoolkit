"""
Unit tests for LFU Cache Utils.

Run with: python -m pytest lfu_cache_utils_test.py -v
Or simply: python lfu_cache_utils_test.py
"""

import unittest
import threading
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

from mod import (
    LFUCache, LFUCacheBuilder, CacheStats,
    create_lfu_cache, lfu_cache_decorator,
    Node, DoublyLinkedList
)


class TestDoublyLinkedList(unittest.TestCase):
    """Tests for DoublyLinkedList."""
    
    def test_append_and_pop(self):
        """Test append and pop operations."""
        lst = DoublyLinkedList()
        self.assertTrue(lst.is_empty())
        
        node1 = Node('a', 1)
        node2 = Node('b', 2)
        
        lst.append(node1)
        self.assertEqual(lst.size, 1)
        self.assertIs(lst.head, node1)
        self.assertIs(lst.tail, node1)
        
        lst.append(node2)
        self.assertEqual(lst.size, 2)
        self.assertIs(lst.head, node1)
        self.assertIs(lst.tail, node2)
        
        popped = lst.pop_head()
        self.assertIs(popped, node1)
        self.assertEqual(lst.size, 1)
        self.assertIs(lst.head, node2)
    
    def test_remove_middle(self):
        """Test removing middle node."""
        lst = DoublyLinkedList()
        node1 = Node('a', 1)
        node2 = Node('b', 2)
        node3 = Node('c', 3)
        
        lst.append(node1)
        lst.append(node2)
        lst.append(node3)
        
        lst.remove(node2)
        
        self.assertEqual(lst.size, 2)
        self.assertIs(node1.next, node3)
        self.assertIs(node3.prev, node1)


class TestLFUCache(unittest.TestCase):
    """Tests for LFUCache."""
    
    def test_basic_operations(self):
        """Test basic put and get operations."""
        cache = LFUCache(capacity=3)
        
        cache.put('a', 1)
        cache.put('b', 2)
        cache.put('c', 3)
        
        self.assertEqual(cache.get('a'), 1)
        self.assertEqual(cache.get('b'), 2)
        self.assertEqual(cache.get('c'), 3)
        self.assertEqual(cache.size, 3)
    
    def test_eviction_policy(self):
        """Test LFU eviction policy."""
        cache = LFUCache(capacity=3)
        
        cache.put('a', 1)
        cache.put('b', 2)
        cache.put('c', 3)
        
        # Access 'a' twice and 'b' once
        cache.get('a')
        cache.get('a')
        cache.get('b')
        
        # Now frequencies: a=3, b=2, c=1
        # 'c' should be evicted when we add 'd'
        evicted = cache.put('d', 4)
        
        self.assertEqual(evicted, 3)
        self.assertFalse(cache.contains('c'))
        self.assertTrue(cache.contains('a'))
        self.assertTrue(cache.contains('b'))
        self.assertTrue(cache.contains('d'))
    
    def test_lru_tiebreaker(self):
        """Test that LRU is used as tiebreaker for same frequency."""
        cache = LFUCache(capacity=3)
        
        cache.put('a', 1)
        cache.put('b', 2)
        cache.put('c', 3)
        
        # All have frequency 1, 'a' was added first (oldest)
        # Should evict 'a' when adding 'd'
        evicted = cache.put('d', 4)
        
        self.assertEqual(evicted, 1)
        self.assertFalse(cache.contains('a'))
        self.assertTrue(cache.contains('b'))
        self.assertTrue(cache.contains('c'))
    
    def test_update_existing_key(self):
        """Test updating an existing key."""
        cache = LFUCache(capacity=2)
        
        cache.put('a', 1)
        cache.put('b', 2)
        
        # Update 'a' - should not cause eviction
        result = cache.put('a', 10)
        self.assertIsNone(result)
        
        self.assertEqual(cache.get('a'), 10)
        self.assertEqual(cache.size, 2)
        
        # 'a' now has higher frequency, 'b' should be evicted
        cache.put('c', 3)
        self.assertFalse(cache.contains('b'))
    
    def test_delete(self):
        """Test delete operation."""
        cache = LFUCache(capacity=3)
        
        cache.put('a', 1)
        cache.put('b', 2)
        
        result = cache.delete('a')
        self.assertEqual(result, 1)
        self.assertFalse(cache.contains('a'))
        self.assertEqual(cache.size, 1)
        
        # Delete non-existent key
        result = cache.delete('x')
        self.assertIsNone(result)
    
    def test_clear(self):
        """Test clear operation."""
        cache = LFUCache(capacity=3)
        
        cache.put('a', 1)
        cache.put('b', 2)
        cache.put('c', 3)
        
        cache.clear()
        
        self.assertEqual(cache.size, 0)
        self.assertIsNone(cache.get('a'))
    
    def test_capacity_validation(self):
        """Test that invalid capacity raises error."""
        with self.assertRaises(ValueError):
            LFUCache(capacity=0)
        
        with self.assertRaises(ValueError):
            LFUCache(capacity=-1)
    
    def test_statistics(self):
        """Test cache statistics."""
        cache = LFUCache(capacity=2)
        
        # Miss
        cache.get('x')
        
        # Hit
        cache.put('a', 1)
        cache.get('a')
        cache.get('a')
        
        # Eviction
        cache.put('b', 2)
        cache.put('c', 3)  # Should evict 'a' (freq 3, but that's wrong - 'a' has freq 3)
        
        stats = cache.stats
        
        self.assertEqual(stats.hits, 2)
        self.assertEqual(stats.misses, 1)
        self.assertGreater(stats.evictions, 0)
        self.assertAlmostEqual(stats.hit_rate, 2/3, places=2)
    
    def test_peek(self):
        """Test peek (get without updating frequency/stats)."""
        cache = LFUCache(capacity=2)
        
        cache.put('a', 1)
        
        # Peek should not update frequency
        cache.peek('a')
        cache.peek('a')
        cache.peek('a')
        
        self.assertEqual(cache.get_freq('a'), 1)
    
    def test_get_freq(self):
        """Test frequency tracking."""
        cache = LFUCache(capacity=2)
        
        cache.put('a', 1)
        self.assertEqual(cache.get_freq('a'), 1)
        
        cache.get('a')
        self.assertEqual(cache.get_freq('a'), 2)
        
        cache.get('a')
        self.assertEqual(cache.get_freq('a'), 3)
        
        # Non-existent key
        self.assertEqual(cache.get_freq('x'), 0)
    
    def test_keys_values_items(self):
        """Test keys, values, items methods."""
        cache = LFUCache(capacity=3)
        
        cache.put('a', 1)
        cache.put('b', 2)
        cache.put('c', 3)
        
        self.assertCountEqual(cache.keys(), ['a', 'b', 'c'])
        self.assertCountEqual(cache.values(), [1, 2, 3])
        self.assertCountEqual(cache.items(), [('a', 1), ('b', 2), ('c', 3)])
    
    def test_contains(self):
        """Test contains operation."""
        cache = LFUCache(capacity=2)
        
        cache.put('a', 1)
        
        self.assertTrue(cache.contains('a'))
        self.assertFalse(cache.contains('b'))
        self.assertIn('a', cache)
        self.assertNotIn('b', cache)
    
    def test_len_and_repr(self):
        """Test __len__ and __repr__."""
        cache = LFUCache(capacity=10)
        
        self.assertEqual(len(cache), 0)
        
        cache.put('a', 1)
        cache.put('b', 2)
        
        self.assertEqual(len(cache), 2)
        
        repr_str = repr(cache)
        self.assertIn('LFUCache', repr_str)
        self.assertIn('capacity=10', repr_str)
        self.assertIn('size=2', repr_str)
    
    def test_thread_safety(self):
        """Test thread safety under concurrent access."""
        cache = LFUCache(capacity=100)
        errors = []
        
        def worker(thread_id):
            try:
                for i in range(100):
                    key = f't{thread_id}_k{i}'
                    cache.put(key, i)
                    cache.get(key)
                    cache.delete(key)
            except Exception as e:
                errors.append(str(e))
        
        threads = [threading.Thread(target=worker, args=(i,)) for i in range(10)]
        
        for t in threads:
            t.start()
        for t in threads:
            t.join()
        
        self.assertEqual(errors, [])


class TestLFUCacheBuilder(unittest.TestCase):
    """Tests for LFUCacheBuilder."""
    
    def test_builder_basic(self):
        """Test basic builder functionality."""
        cache = (LFUCacheBuilder()
                 .capacity(5)
                 .initial_items({'a': 1, 'b': 2, 'c': 3})
                 .build())
        
        self.assertEqual(cache.capacity, 5)
        self.assertEqual(cache.size, 3)
        self.assertEqual(cache.get('a'), 1)
    
    def test_builder_default_capacity(self):
        """Test default capacity."""
        cache = LFUCacheBuilder().build()
        self.assertEqual(cache.capacity, 128)


class TestCacheDecorator(unittest.TestCase):
    """Tests for lfu_cache_decorator."""
    
    def test_decorator_caching(self):
        """Test that decorator caches results."""
        call_count = [0]
        
        @lfu_cache_decorator(capacity=10)
        def expensive_func(x):
            call_count[0] += 1
            return x * x
        
        # First call - computed
        result1 = expensive_func(5)
        self.assertEqual(result1, 25)
        self.assertEqual(call_count[0], 1)
        
        # Second call - cached
        result2 = expensive_func(5)
        self.assertEqual(result2, 25)
        self.assertEqual(call_count[0], 1)
        
        # Different argument - computed
        result3 = expensive_func(6)
        self.assertEqual(result3, 36)
        self.assertEqual(call_count[0], 2)
    
    def test_decorator_eviction(self):
        """Test decorator cache eviction."""
        call_count = [0]
        
        @lfu_cache_decorator(capacity=2)
        def func(x):
            call_count[0] += 1
            return x
        
        func(1)
        func(2)
        func(3)  # Should evict 1
        
        # 1 should be recomputed
        func(1)
        self.assertGreater(call_count[0], 3)
    
    def test_decorator_utilities(self):
        """Test decorator utility methods."""
        @lfu_cache_decorator(capacity=5)
        def func(x):
            return x
        
        func(1)
        func(2)
        
        self.assertEqual(len(func.cache), 2)
        
        func.cache_clear()
        self.assertEqual(len(func.cache), 0)
        
        stats = func.cache_stats()
        self.assertIsInstance(stats, CacheStats)


class TestEdgeCases(unittest.TestCase):
    """Tests for edge cases."""
    
    def test_single_capacity(self):
        """Test cache with capacity 1."""
        cache = LFUCache(capacity=1)
        
        cache.put('a', 1)
        self.assertEqual(cache.get('a'), 1)
        
        cache.put('b', 2)
        self.assertIsNone(cache.get('a'))
        self.assertEqual(cache.get('b'), 2)
    
    def test_large_capacity(self):
        """Test cache with large capacity."""
        cache = LFUCache(capacity=10000)
        
        for i in range(5000):
            cache.put(i, i * 2)
        
        self.assertEqual(cache.size, 5000)
        self.assertEqual(cache.get(100), 200)
    
    def test_none_values(self):
        """Test storing None as values."""
        cache = LFUCache(capacity=2)
        
        cache.put('a', None)
        # get returns None for both 'not found' and 'stored None'
        # We need peek to distinguish
        self.assertTrue(cache.contains('a'))
        self.assertIsNone(cache.peek('a'))
    
    def test_complex_keys(self):
        """Test with complex hashable keys."""
        cache = LFUCache(capacity=5)
        
        # Tuple keys
        cache.put((1, 2), 'tuple_value')
        self.assertEqual(cache.get((1, 2)), 'tuple_value')
        
        # Frozen set keys
        cache.put(frozenset([1, 2, 3]), 'set_value')
        self.assertEqual(cache.get(frozenset([1, 2, 3])), 'set_value')
    
    def test_repeated_access_same_key(self):
        """Test repeated access to the same key."""
        cache = LFUCache(capacity=3)
        
        cache.put('a', 1)
        
        for _ in range(100):
            cache.get('a')
        
        self.assertEqual(cache.get_freq('a'), 101)
        
        # Add other items
        cache.put('b', 2)
        cache.put('c', 3)
        
        # 'a' has highest frequency, 'b' should be evicted
        cache.put('d', 4)
        
        self.assertTrue(cache.contains('a'))


class TestCacheStats(unittest.TestCase):
    """Tests for CacheStats."""
    
    def test_hit_rate(self):
        """Test hit rate calculation."""
        stats = CacheStats(hits=3, misses=1)
        
        self.assertAlmostEqual(stats.hit_rate, 0.75, places=2)
    
    def test_hit_rate_zero(self):
        """Test hit rate with no accesses."""
        stats = CacheStats()
        
        self.assertEqual(stats.hit_rate, 0.0)
    
    def test_reset(self):
        """Test stats reset."""
        stats = CacheStats(hits=10, misses=5, evictions=2, current_size=10)
        
        stats.reset()
        
        self.assertEqual(stats.hits, 0)
        self.assertEqual(stats.misses, 0)
        self.assertEqual(stats.evictions, 0)
        self.assertEqual(stats.current_size, 0)


if __name__ == '__main__':
    unittest.main(verbosity=2)