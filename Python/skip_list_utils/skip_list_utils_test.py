"""
Tests for Skip List Utilities

Run with: python skip_list_utils_test.py
"""

import unittest
import threading
import time
import random
from typing import List, Tuple

# Import the module
from mod import (
    SkipList, ConcurrentSkipList, SkipListSet,
    SkipListError, DuplicateKeyError,
    create_skip_list, create_sorted_dict
)


class TestSkipListBasic(unittest.TestCase):
    """Basic skip list operations tests."""
    
    def test_empty_skip_list(self):
        """Test empty skip list properties."""
        sl = SkipList[int]()
        self.assertEqual(sl.size, 0)
        self.assertTrue(sl.is_empty)
        self.assertEqual(sl.current_level, 1)
        self.assertIsNone(sl.first())
        self.assertIsNone(sl.last())
        self.assertIsNone(sl.min_key())
        self.assertIsNone(sl.max_key())
    
    def test_single_insert_search(self):
        """Test inserting and searching a single element."""
        sl = SkipList[int]()
        sl.insert(5, "five")
        
        self.assertEqual(sl.size, 1)
        self.assertFalse(sl.is_empty)
        self.assertEqual(sl.search(5), "five")
        self.assertIn(5, sl)
        self.assertNotIn(10, sl)
    
    def test_multiple_inserts_sorted(self):
        """Test inserting multiple elements maintains sorted order."""
        sl = SkipList[int]()
        values = [(3, "three"), (1, "one"), (4, "four"), (1, "five")]
        
        for key, val in values:
            sl[key] = val  # Use __setitem__
        
        keys = list(sl.keys())
        self.assertEqual(keys, [1, 3, 4])
        
        values = list(sl.values())
        self.assertEqual(values, ["five", "three", "four"])
    
    def test_getitem(self):
        """Test __getitem__ access."""
        sl = SkipList[str]()
        sl.insert("a", 1)
        sl.insert("b", 2)
        
        self.assertEqual(sl["a"], 1)
        self.assertEqual(sl["b"], 2)
        
        with self.assertRaises(KeyError):
            _ = sl["c"]
    
    def test_get_with_default(self):
        """Test get method with default value."""
        sl = SkipList[int]()
        sl.insert(1, "one")
        
        self.assertEqual(sl.get(1), "one")
        self.assertEqual(sl.get(2), None)
        self.assertEqual(sl.get(2, "default"), "default")
    
    def test_duplicate_key_error(self):
        """Test that duplicate keys raise error by default."""
        sl = SkipList[int]()
        sl.insert(1, "one")
        
        with self.assertRaises(DuplicateKeyError):
            sl.insert(1, "another one")
    
    def test_allow_duplicates(self):
        """Test skip list with duplicates allowed."""
        sl = SkipList[int](allow_duplicates=True)
        sl.insert(1, "first")
        sl.insert(1, "second")  # Should update value
        
        self.assertEqual(sl.size, 1)
        self.assertEqual(sl.search(1), "second")
    
    def test_setitem_update(self):
        """Test that __setitem__ updates existing values."""
        sl = SkipList[int]()
        sl[1] = "first"
        sl[1] = "updated"
        
        self.assertEqual(sl.size, 1)
        self.assertEqual(sl[1], "updated")
    
    def test_delete(self):
        """Test deleting elements."""
        sl = SkipList[int]()
        sl.insert(1, "one")
        sl.insert(2, "two")
        sl.insert(3, "three")
        
        self.assertTrue(sl.delete(2))
        self.assertEqual(sl.size, 2)
        self.assertNotIn(2, sl)
        
        self.assertFalse(sl.delete(99))  # Non-existent key
        self.assertEqual(sl.size, 2)
    
    def test_delitem(self):
        """Test __delitem__ operator."""
        sl = SkipList[int]()
        sl[1] = "one"
        sl[2] = "two"
        
        del sl[1]
        self.assertEqual(sl.size, 1)
        self.assertNotIn(1, sl)
        
        with self.assertRaises(KeyError):
            del sl[99]
    
    def test_clear(self):
        """Test clearing the skip list."""
        sl = SkipList[int]()
        for i in range(100):
            sl.insert(i, f"val_{i}")
        
        sl.clear()
        self.assertEqual(sl.size, 0)
        self.assertTrue(sl.is_empty)
        self.assertEqual(sl.current_level, 1)
    
    def test_iteration(self):
        """Test iteration over elements."""
        sl = SkipList[int]()
        values = [(5, "five"), (2, "two"), (8, "eight"), (1, "one")]
        
        for k, v in values:
            sl.insert(k, v)
        
        items = list(sl)
        self.assertEqual(items, [(1, "one"), (2, "two"), (5, "five"), (8, "eight")])
        
        keys = list(sl.keys())
        self.assertEqual(keys, [1, 2, 5, 8])
        
        values = list(sl.values())
        self.assertEqual(values, ["one", "two", "five", "eight"])


class TestSkipListRange(unittest.TestCase):
    """Range query tests."""
    
    def test_range_all(self):
        """Test range query returning all elements."""
        sl = SkipList[int]()
        for i in range(1, 6):
            sl.insert(i, i * 10)
        
        items = list(sl.range())
        self.assertEqual(len(items), 5)
        self.assertEqual(items, [(1, 10), (2, 20), (3, 30), (4, 40), (5, 50)])
    
    def test_range_with_start(self):
        """Test range query with start key."""
        sl = SkipList[int]()
        for i in range(1, 11):
            sl.insert(i, i * 10)
        
        items = list(sl.range(start_key=5))
        self.assertEqual(len(items), 6)
        self.assertEqual(items[0], (5, 50))
        self.assertEqual(items[-1], (10, 100))
    
    def test_range_with_end(self):
        """Test range query with end key."""
        sl = SkipList[int]()
        for i in range(1, 11):
            sl.insert(i, i * 10)
        
        items = list(sl.range(end_key=5))
        self.assertEqual(len(items), 5)
        self.assertEqual(items[0], (1, 10))
        self.assertEqual(items[-1], (5, 50))
    
    def test_range_exclusive_end(self):
        """Test range query with exclusive end."""
        sl = SkipList[int]()
        for i in range(1, 11):
            sl.insert(i, i * 10)
        
        items = list(sl.range(end_key=5, inclusive=False))
        self.assertEqual(len(items), 4)
        self.assertEqual(items[-1], (4, 40))
    
    def test_range_both_bounds(self):
        """Test range query with both bounds."""
        sl = SkipList[int]()
        for i in range(1, 21):
            sl.insert(i, i * 10)
        
        items = list(sl.range(start_key=5, end_key=10))
        self.assertEqual(len(items), 6)
        self.assertEqual(items[0], (5, 50))
        self.assertEqual(items[-1], (10, 100))
    
    def test_count_range(self):
        """Test counting elements in range."""
        sl = SkipList[int]()
        for i in range(1, 101):
            sl.insert(i, i)
        
        self.assertEqual(sl.count_range(25, 75), 51)
        self.assertEqual(sl.count_range(25, 75, inclusive=False), 50)
        self.assertEqual(sl.count_range(end_key=50), 50)
        self.assertEqual(sl.count_range(start_key=50), 51)


class TestSkipListNavigation(unittest.TestCase):
    """Navigation method tests."""
    
    def test_first_last(self):
        """Test first and last methods."""
        sl = SkipList[int]()
        
        self.assertIsNone(sl.first())
        self.assertIsNone(sl.last())
        
        sl.insert(5, "five")
        self.assertEqual(sl.first(), (5, "five"))
        self.assertEqual(sl.last(), (5, "five"))
        
        sl.insert(2, "two")
        sl.insert(8, "eight")
        
        self.assertEqual(sl.first(), (2, "two"))
        self.assertEqual(sl.last(), (8, "eight"))
    
    def test_predecessor(self):
        """Test predecessor method."""
        sl = SkipList[int]()
        for i in [5, 2, 8, 1, 9, 3]:
            sl.insert(i, str(i))
        
        self.assertEqual(sl.predecessor(5), 3)
        self.assertEqual(sl.predecessor(2), 1)
        self.assertEqual(sl.predecessor(1), None)  # No predecessor for min
        self.assertEqual(sl.predecessor(4), 3)  # Predecessor of non-existent key
        self.assertEqual(sl.predecessor(10), 9)  # Predecessor of key > max
    
    def test_successor(self):
        """Test successor method."""
        sl = SkipList[int]()
        for i in [5, 2, 8, 1, 9, 3]:
            sl.insert(i, str(i))
        
        self.assertEqual(sl.successor(5), 8)
        self.assertEqual(sl.successor(2), 3)
        self.assertEqual(sl.successor(9), None)  # No successor for max
        self.assertEqual(sl.successor(4), 5)  # Successor of non-existent key
        self.assertEqual(sl.successor(0), 1)  # Successor of key < min
    
    def test_min_max_key(self):
        """Test min_key and max_key methods."""
        sl = SkipList[str]()
        sl.insert("c", 3)
        sl.insert("a", 1)
        sl.insert("b", 2)
        
        self.assertEqual(sl.min_key(), "a")
        self.assertEqual(sl.max_key(), "c")


class TestSkipListConversion(unittest.TestCase):
    """Conversion method tests."""
    
    def test_to_list(self):
        """Test conversion to list."""
        sl = SkipList[int]()
        sl.insert(3, "c")
        sl.insert(1, "a")
        sl.insert(2, "b")
        
        self.assertEqual(sl.to_list(), [(1, "a"), (2, "b"), (3, "c")])
    
    def test_to_dict(self):
        """Test conversion to dictionary."""
        sl = SkipList[int]()
        sl.insert(1, "one")
        sl.insert(2, "two")
        
        d = sl.to_dict()
        self.assertEqual(d, {1: "one", 2: "two"})
    
    def test_from_dict(self):
        """Test creation from dictionary."""
        d = {3: "c", 1: "a", 2: "b"}
        sl = SkipList[int].from_dict(d)
        
        self.assertEqual(sl.size, 3)
        self.assertEqual(list(sl.keys()), [1, 2, 3])
    
    def test_from_sorted(self):
        """Test creation from sorted data."""
        data = [(1, "a"), (2, "b"), (3, "c")]
        sl = SkipList[int].from_sorted(data)
        
        self.assertEqual(sl.size, 3)
        self.assertEqual(list(sl.keys()), [1, 2, 3])


class TestSkipListTypes(unittest.TestCase):
    """Tests with different key types."""
    
    def test_string_keys(self):
        """Test with string keys."""
        sl = SkipList[str]()
        sl.insert("charlie", 3)
        sl.insert("alpha", 1)
        sl.insert("bravo", 2)
        
        keys = list(sl.keys())
        self.assertEqual(keys, ["alpha", "bravo", "charlie"])
    
    def test_float_keys(self):
        """Test with float keys."""
        sl = SkipList[float]()
        sl.insert(3.14, "pi")
        sl.insert(2.71, "e")
        sl.insert(1.41, "sqrt2")
        
        keys = list(sl.keys())
        self.assertEqual(keys, [1.41, 2.71, 3.14])
    
    def test_tuple_keys(self):
        """Test with tuple keys (lexicographic order)."""
        sl = SkipList[Tuple[int, int]]()
        sl.insert((2, 1), "a")
        sl.insert((1, 2), "b")
        sl.insert((1, 1), "c")
        sl.insert((2, 2), "d")
        
        keys = list(sl.keys())
        self.assertEqual(keys, [(1, 1), (1, 2), (2, 1), (2, 2)])


class TestSkipListPerformance(unittest.TestCase):
    """Performance-related tests."""
    
    def test_large_insert(self):
        """Test inserting many elements."""
        sl = SkipList[int]()
        n = 10000
        
        for i in range(n):
            sl.insert(i, f"val_{i}")
        
        self.assertEqual(sl.size, n)
        self.assertEqual(sl.min_key(), 0)
        self.assertEqual(sl.max_key(), n - 1)
    
    def test_search_performance(self):
        """Test search is efficient."""
        sl = SkipList[int]()
        n = 5000
        
        for i in range(n):
            sl.insert(i * 2, i)  # Even numbers
        
        # Search for existing and non-existing keys
        self.assertEqual(sl.search(100), 50)
        self.assertIsNone(sl.search(101))  # Odd number doesn't exist
    
    def test_random_insert_order(self):
        """Test that random insert order still produces sorted iteration."""
        sl = SkipList[int]()
        n = 1000
        values = list(range(n))
        random.shuffle(values)
        
        for v in values:
            sl.insert(v, v)
        
        keys = list(sl.keys())
        self.assertEqual(keys, list(range(n)))
    
    def test_deterministic_with_seed(self):
        """Test that seeding produces deterministic behavior."""
        sl1 = SkipList[int]()
        sl2 = SkipList[int]()
        
        sl1.seed(42)
        sl2.seed(42)
        
        values = list(range(100))
        random.shuffle(values)
        
        for v in values:
            sl1.insert(v)
            sl2.insert(v)
        
        # Both should have same structure
        self.assertEqual(sl1.current_level, sl2.current_level)
        self.assertEqual(list(sl1.keys()), list(sl2.keys()))


class TestSkipListVisualization(unittest.TestCase):
    """Visualization tests."""
    
    def test_visualize_empty(self):
        """Test visualization of empty list."""
        sl = SkipList[int]()
        viz = sl.visualize()
        self.assertEqual(viz, "SkipList(empty)")
    
    def test_visualize_non_empty(self):
        """Test visualization produces output."""
        sl = SkipList[int]()
        sl.seed(42)  # Deterministic
        
        for i in [5, 2, 8, 1, 9]:
            sl.insert(i)
        
        viz = sl.visualize()
        self.assertIn("SkipList(size=5", viz)
        self.assertIn("L0:", viz)


class TestConcurrentSkipList(unittest.TestCase):
    """Thread-safe skip list tests."""
    
    def test_concurrent_inserts(self):
        """Test concurrent inserts are safe."""
        sl = ConcurrentSkipList[int]()
        n = 1000
        threads = []
        
        def insert_range(start):
            for i in range(start, start + n):
                sl.insert(i, f"val_{i}")
        
        # Create multiple threads
        for i in range(4):
            t = threading.Thread(target=insert_range, args=(i * n,))
            threads.append(t)
        
        # Start all threads
        for t in threads:
            t.start()
        
        # Wait for completion
        for t in threads:
            t.join()
        
        self.assertEqual(sl.size, 4000)
    
    def test_concurrent_read_write(self):
        """Test concurrent reads and writes."""
        sl = ConcurrentSkipList[int]()
        
        # Initial inserts
        for i in range(100):
            sl.insert(i, i)
        
        errors = []
        
        def reader():
            for i in range(100):
                try:
                    _ = sl.search(i)
                except Exception as e:
                    errors.append(e)
        
        def writer():
            for i in range(100, 200):
                sl.insert(i, i)
        
        threads = [
            threading.Thread(target=reader),
            threading.Thread(target=reader),
            threading.Thread(target=writer),
            threading.Thread(target=reader),
        ]
        
        for t in threads:
            t.start()
        for t in threads:
            t.join()
        
        self.assertEqual(len(errors), 0)
        self.assertEqual(sl.size, 200)
    
    def test_thread_safe_iteration(self):
        """Test that iteration is thread-safe."""
        sl = ConcurrentSkipList[int]()
        for i in range(100):
            sl.insert(i, i)
        
        results = []
        
        def iterate():
            items = list(sl)
            results.append(len(items))
        
        threads = [threading.Thread(target=iterate) for _ in range(10)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()
        
        self.assertEqual(results, [100] * 10)


class TestSkipListSet(unittest.TestCase):
    """Skip list set tests."""
    
    def test_basic_operations(self):
        """Test basic set operations."""
        s = SkipListSet[int]()
        
        self.assertTrue(s.add(5))
        self.assertFalse(s.add(5))  # Already exists
        self.assertTrue(s.add(3))
        
        self.assertEqual(s.size, 2)
        self.assertIn(5, s)
        self.assertIn(3, s)
    
    def test_remove_discard(self):
        """Test remove and discard."""
        s = SkipListSet[int]()
        s.add(1)
        s.add(2)
        s.add(3)
        
        self.assertTrue(s.remove(2))
        self.assertEqual(s.size, 2)
        self.assertFalse(s.remove(99))  # Non-existent
        
        self.assertTrue(s.discard(3))
        self.assertFalse(s.discard(99))  # Non-existent, but no error
    
    def test_iteration(self):
        """Test set iteration is sorted."""
        s = SkipListSet[int]()
        for i in [5, 2, 8, 1, 9]:
            s.add(i)
        
        self.assertEqual(list(s), [1, 2, 5, 8, 9])
    
    def test_first_last(self):
        """Test first and last elements."""
        s = SkipListSet[int]()
        s.add(5)
        s.add(2)
        s.add(8)
        
        self.assertEqual(s.first(), 2)
        self.assertEqual(s.last(), 8)
    
    def test_range(self):
        """Test range iteration."""
        s = SkipListSet[int]()
        for i in range(1, 11):
            s.add(i)
        
        items = list(s.range(3, 7))
        self.assertEqual(items, [3, 4, 5, 6, 7])
    
    def test_set_operations(self):
        """Test set operations."""
        a = SkipListSet[int].from_iterable([1, 2, 3, 4])
        b = SkipListSet[int].from_iterable([3, 4, 5, 6])
        
        # Union
        u = a.union(b)
        self.assertEqual(set(u), {1, 2, 3, 4, 5, 6})
        
        # Intersection
        i = a.intersection(b)
        self.assertEqual(set(i), {3, 4})
        
        # Difference
        d = a.difference(b)
        self.assertEqual(set(d), {1, 2})
        
        # Subset/superset
        c = SkipListSet[int].from_iterable([2, 3])
        self.assertTrue(c.issubset(a))
        self.assertTrue(a.issuperset(c))
        self.assertTrue(a.isdisjoint(SkipListSet[int].from_iterable([10, 11])))
    
    def test_from_iterable(self):
        """Test creating set from iterable."""
        s = SkipListSet[int].from_iterable([5, 2, 8, 2, 1, 5])
        self.assertEqual(list(s), [1, 2, 5, 8])
    
    def test_to_list(self):
        """Test conversion to list."""
        s = SkipListSet[int]()
        s.add(3)
        s.add(1)
        s.add(2)
        
        self.assertEqual(s.to_list(), [1, 2, 3])


class TestUtilityFunctions(unittest.TestCase):
    """Utility function tests."""
    
    def test_create_skip_list_empty(self):
        """Test creating empty skip list."""
        sl = create_skip_list()
        self.assertEqual(sl.size, 0)
    
    def test_create_skip_list_with_items(self):
        """Test creating skip list with items."""
        items = [(3, "c"), (1, "a"), (2, "b")]
        sl = create_skip_list(items)
        
        self.assertEqual(sl.size, 3)
        self.assertEqual(list(sl.keys()), [1, 2, 3])
    
    def test_create_sorted_dict(self):
        """Test creating sorted dictionary."""
        d = {"c": 3, "a": 1, "b": 2}
        sl = create_sorted_dict(d)
        
        self.assertEqual(list(sl.keys()), ["a", "b", "c"])
        self.assertEqual(sl["a"], 1)


class TestEdgeCases(unittest.TestCase):
    """Edge case tests."""
    
    def test_invalid_max_level(self):
        """Test invalid max_level raises error."""
        with self.assertRaises(ValueError):
            SkipList[int](max_level=0)
        
        with self.assertRaises(ValueError):
            SkipList[int](max_level=-1)
    
    def test_invalid_probability(self):
        """Test invalid probability raises error."""
        with self.assertRaises(ValueError):
            SkipList[int](probability=0)
        
        with self.assertRaises(ValueError):
            SkipList[int](probability=1)
        
        with self.assertRaises(ValueError):
            SkipList[int](probability=-0.5)
        
        with self.assertRaises(ValueError):
            SkipList[int](probability=1.5)
    
    def test_range_empty_skip_list(self):
        """Test range query on empty skip list."""
        sl = SkipList[int]()
        items = list(sl.range())
        self.assertEqual(items, [])
    
    def test_predecessor_successor_boundary(self):
        """Test predecessor/successor at boundaries."""
        sl = SkipList[int]()
        sl.insert(10, "ten")
        
        self.assertIsNone(sl.predecessor(10))
        self.assertIsNone(sl.successor(10))
    
    def test_large_key_range(self):
        """Test with large key range."""
        sl = SkipList[int]()
        sl.insert(1, "one")
        sl.insert(1000000, "million")
        
        self.assertEqual(sl.size, 2)
        self.assertEqual(sl.search(1), "one")
        self.assertEqual(sl.search(1000000), "million")
        self.assertIsNone(sl.search(500000))
    
    def test_negative_keys(self):
        """Test with negative keys."""
        sl = SkipList[int]()
        sl.insert(-5, "neg five")
        sl.insert(5, "five")
        sl.insert(0, "zero")
        sl.insert(-10, "neg ten")
        
        keys = list(sl.keys())
        self.assertEqual(keys, [-10, -5, 0, 5])


class TestRepr(unittest.TestCase):
    """Representation tests."""
    
    def test_repr_empty(self):
        """Test repr of empty skip list."""
        sl = SkipList[int]()
        self.assertEqual(repr(sl), "SkipList({})")
    
    def test_repr_with_items(self):
        """Test repr with items."""
        sl = SkipList[int]()
        sl.insert(1, "one")
        sl.insert(2, "two")
        
        self.assertEqual(repr(sl), "SkipList({1: 'one', 2: 'two'})")
    
    def test_repr_set(self):
        """Test repr of skip list set."""
        s = SkipListSet[int]()
        self.assertEqual(repr(s), "SkipListSet({})")
        
        s.add(1)
        s.add(2)
        self.assertEqual(repr(s), "SkipListSet({1, 2})")


if __name__ == "__main__":
    unittest.main(verbosity=2)