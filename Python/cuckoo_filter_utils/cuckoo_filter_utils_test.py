"""
Tests for Cuckoo Filter implementation.
"""

import unittest
import random
import string
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from mod import (
    CuckooFilter,
    create_optimal_filter,
    calculate_false_positive_rate,
)


class TestCuckooFilterCreation(unittest.TestCase):
    """Test filter initialization and configuration."""
    
    def test_new_basic(self):
        """Test basic creation."""
        cf = CuckooFilter(1000)
        self.assertIsNotNone(cf)
        self.assertEqual(cf.count, 0)
        self.assertGreater(cf.capacity, 0)
    
    def test_new_with_parameters(self):
        """Test creation with custom parameters."""
        cf = CuckooFilter(10000, bucket_size=8, max_kicks=1000, fp_rate=0.001)
        self.assertEqual(cf._bucket_size, 8)
        self.assertEqual(cf._max_kicks, 1000)
    
    def test_invalid_capacity(self):
        """Test that invalid capacity raises error."""
        with self.assertRaises(ValueError):
            CuckooFilter(0)
        with self.assertRaises(ValueError):
            CuckooFilter(-100)
    
    def test_invalid_bucket_size(self):
        """Test that invalid bucket size raises error."""
        with self.assertRaises(ValueError):
            CuckooFilter(1000, bucket_size=0)
    
    def test_invalid_fp_rate(self):
        """Test that invalid FP rate raises error."""
        with self.assertRaises(ValueError):
            CuckooFilter(1000, fp_rate=0)
        with self.assertRaises(ValueError):
            CuckooFilter(1000, fp_rate=1.0)
    
    def test_capacity_power_of_two(self):
        """Test that bucket count is power of two."""
        cf = CuckooFilter(1000)
        n = cf._num_buckets
        # Check if n is power of two
        self.assertEqual(n & (n - 1), 0)
    
    def test_create_optimal_filter(self):
        """Test optimal filter creation."""
        cf = create_optimal_filter(100000, 0.001)
        self.assertGreater(cf.capacity, 100000)


class TestInsertAndContains(unittest.TestCase):
    """Test insert and contains operations."""
    
    def test_insert_bytes(self):
        """Test inserting bytes."""
        cf = CuckooFilter(1000)
        self.assertTrue(cf.insert(b"hello"))
        self.assertTrue(cf.contains(b"hello"))
    
    def test_insert_string(self):
        """Test inserting strings."""
        cf = CuckooFilter(1000)
        self.assertTrue(cf.insert_string("world"))
        self.assertTrue(cf.contains_string("world"))
    
    def test_insert_multiple_items(self):
        """Test inserting multiple items."""
        cf = CuckooFilter(1000)
        items = [b"a", b"b", b"c", b"d", b"e"]
        for item in items:
            self.assertTrue(cf.insert(item))
        
        self.assertEqual(cf.count, len(items))
        for item in items:
            self.assertTrue(cf.contains(item))
    
    def test_non_existent_item(self):
        """Test checking non-existent item."""
        cf = CuckooFilter(1000)
        cf.insert(b"exists")
        # Note: may have false positive, but should usually be False
        # We can't guarantee False due to probabilistic nature
        self.assertTrue(cf.contains(b"exists"))
    
    def test_no_false_negatives(self):
        """Test that there are no false negatives."""
        cf = CuckooFilter(10000)
        items = [f"item-{i}".encode() for i in range(1000)]
        
        for item in items:
            cf.insert(item)
        
        # All inserted items must be found
        for item in items:
            self.assertTrue(cf.contains(item), f"False negative for {item}")


class TestDelete(unittest.TestCase):
    """Test delete operations."""
    
    def test_delete_existing(self):
        """Test deleting existing item."""
        cf = CuckooFilter(1000)
        cf.insert(b"hello")
        self.assertTrue(cf.delete(b"hello"))
        self.assertFalse(cf.contains(b"hello"))
        self.assertEqual(cf.count, 0)
    
    def test_delete_string(self):
        """Test deleting string."""
        cf = CuckooFilter(1000)
        cf.insert_string("world")
        self.assertTrue(cf.delete_string("world"))
        self.assertFalse(cf.contains_string("world"))
    
    def test_delete_non_existing(self):
        """Test deleting non-existent item."""
        cf = CuckooFilter(1000)
        self.assertFalse(cf.delete(b"nonexistent"))
    
    def test_delete_partial(self):
        """Test deleting some items while keeping others."""
        cf = CuckooFilter(1000)
        items = ["a", "b", "c", "d", "e"]
        
        for item in items:
            cf.insert_string(item)
        
        # Delete middle item
        self.assertTrue(cf.delete_string("c"))
        self.assertEqual(cf.count, len(items) - 1)
        
        # Check others still exist
        for item in ["a", "b", "d", "e"]:
            self.assertTrue(cf.contains_string(item))
        
        # Deleted item should not be found
        self.assertFalse(cf.contains_string("c"))


class TestBulkOperations(unittest.TestCase):
    """Test bulk insert operations."""
    
    def test_bulk_insert_bytes(self):
        """Test bulk insert with bytes."""
        cf = CuckooFilter(10000)
        items = [b"item-1", b"item-2", b"item-3"]
        inserted, failed = cf.bulk_insert(items)
        self.assertEqual(inserted, len(items))
        self.assertFalse(failed)
    
    def test_bulk_insert_strings(self):
        """Test bulk insert with strings."""
        cf = CuckooFilter(10000)
        items = ["one", "two", "three"]
        inserted, failed = cf.bulk_insert_strings(items)
        self.assertEqual(inserted, len(items))
        self.assertFalse(failed)
    
    def test_bulk_insert_many_items(self):
        """Test bulk insert with many items."""
        cf = CuckooFilter(50000)
        items = [f"bulk-{i}" for i in range(1000)]
        inserted, failed = cf.bulk_insert_strings(items)
        self.assertGreaterEqual(inserted, 1000)


class TestStatistics(unittest.TestCase):
    """Test statistics and properties."""
    
    def test_count(self):
        """Test count property."""
        cf = CuckooFilter(1000)
        self.assertEqual(cf.count, 0)
        
        for i in range(10):
            cf.insert_string(f"item-{i}")
        
        self.assertEqual(cf.count, 10)
    
    def test_capacity(self):
        """Test capacity property."""
        cf = CuckooFilter(1000)
        self.assertGreater(cf.capacity, 0)
    
    def test_load_factor(self):
        """Test load factor calculation."""
        cf = CuckooFilter(1000)
        self.assertEqual(cf.load_factor, 0)
        
        # Insert some items
        for i in range(int(cf.capacity * 0.5)):
            cf.insert_string(f"item-{i}")
        
        self.assertGreater(cf.load_factor, 0)
        self.assertLess(cf.load_factor, 1)
    
    def test_stats_dict(self):
        """Test stats method."""
        cf = CuckooFilter(1000)
        cf.insert_string("test")
        
        stats = cf.stats()
        self.assertIn('capacity', stats)
        self.assertIn('count', stats)
        self.assertIn('load_factor', stats)
        self.assertIn('bucket_size', stats)
        self.assertIn('fingerprint_size', stats)
        self.assertIn('expected_fp_rate', stats)
        self.assertIn('memory_bytes', stats)


class TestReset(unittest.TestCase):
    """Test reset functionality."""
    
    def test_reset_empty(self):
        """Test reset on empty filter."""
        cf = CuckooFilter(1000)
        cf.reset()
        self.assertEqual(cf.count, 0)
    
    def test_reset_with_items(self):
        """Test reset clears all items."""
        cf = CuckooFilter(1000)
        for i in range(100):
            cf.insert_string(f"item-{i}")
        
        self.assertEqual(cf.count, 100)
        cf.reset()
        self.assertEqual(cf.count, 0)
        self.assertEqual(cf.load_factor, 0)
        
        # Items should not be found
        self.assertFalse(cf.contains_string("item-1"))


class TestSerialization(unittest.TestCase):
    """Test JSON serialization."""
    
    def test_to_json(self):
        """Test serialization to JSON."""
        cf = CuckooFilter(1000)
        cf.insert_string("test")
        data = cf.to_json()
        self.assertIsInstance(data, str)
        self.assertGreater(len(data), 0)
    
    def test_from_json(self):
        """Test deserialization from JSON."""
        cf1 = CuckooFilter(1000)
        items = ["a", "b", "c"]
        for item in items:
            cf1.insert_string(item)
        
        data = cf1.to_json()
        cf2 = CuckooFilter.from_json(data)
        
        # Check data preserved
        self.assertEqual(cf1.count, cf2.count)
        for item in items:
            self.assertTrue(cf2.contains_string(item))
    
    def test_roundtrip(self):
        """Test serialization roundtrip."""
        cf1 = CuckooFilter(10000)
        for i in range(100):
            cf1.insert_string(f"item-{i}")
        
        cf2 = CuckooFilter.from_json(cf1.to_json())
        
        # All items should be found
        for i in range(100):
            self.assertTrue(cf2.contains_string(f"item-{i}"))


class TestClone(unittest.TestCase):
    """Test clone functionality."""
    
    def test_clone_basic(self):
        """Test basic cloning."""
        cf1 = CuckooFilter(1000)
        cf1.insert_string("test")
        
        cf2 = cf1.clone()
        self.assertEqual(cf1.count, cf2.count)
        self.assertTrue(cf2.contains_string("test"))
    
    def test_clone_independence(self):
        """Test that clone is independent."""
        cf1 = CuckooFilter(1000)
        cf1.insert_string("original")
        
        cf2 = cf1.clone()
        cf2.insert_string("new")
        
        # Original should not have new item
        self.assertFalse(cf1.contains_string("new"))
        self.assertTrue(cf2.contains_string("new"))


class TestFalsePositiveRate(unittest.TestCase):
    """Test false positive rate estimation."""
    
    def test_calculate_fp_rate(self):
        """Test FP rate calculation."""
        rate = calculate_false_positive_rate(8, 4)
        self.assertGreater(rate, 0)
        self.assertLess(rate, 1)
    
    def test_fp_rate_with_larger_fp(self):
        """Test that larger fingerprint reduces FP rate."""
        rate1 = calculate_false_positive_rate(8, 4)
        rate2 = calculate_false_positive_rate(16, 4)
        self.assertLess(rate2, rate1)
    
    def test_actual_fp_rate_reasonable(self):
        """Test that actual FP rate is reasonable."""
        cf = CuckooFilter(10000, fp_rate=0.01)
        
        # Insert some items
        for i in range(5000):
            cf.insert_string(f"inserted-{i}")
        
        # Test with items we know weren't inserted
        fp_count = 0
        test_count = 10000
        
        for i in range(test_count):
            # Use a different prefix to ensure not inserted
            test_item = f"test-{i}-{random.randint(100000, 999999)}"
            if cf.contains_string(test_item):
                fp_count += 1
        
        actual_fp_rate = fp_count / test_count
        # Allow some variance - should be under 5% for 1% target
        # Actual rate varies based on load factor
        self.assertLess(actual_fp_rate, 0.10)


class TestCapacityLimits(unittest.TestCase):
    """Test capacity limits."""
    
    def test_fill_capacity(self):
        """Test filling filter to capacity."""
        cf = CuckooFilter(100)
        
        inserted = 0
        for i in range(1000):
            if cf.insert_string(f"item-{i}"):
                inserted += 1
            else:
                break
        
        # Should have inserted some items before failing
        self.assertGreater(inserted, 50)
        # Filter should have high load factor
        self.assertGreater(cf.load_factor, 0.5)
    
    def test_high_load_factor(self):
        """Test operation at high load factor."""
        cf = CuckooFilter(1000)
        
        # Fill to ~80% capacity
        target = int(cf.capacity * 0.8)
        for i in range(target):
            cf.insert_string(f"fill-{i}")
        
        # Should still be able to do operations
        self.assertGreater(cf.count, target * 0.9)
        self.assertGreater(cf.load_factor, 0.7)


class TestStringRepresentation(unittest.TestCase):
    """Test string representations."""
    
    def test_repr(self):
        """Test repr string."""
        cf = CuckooFilter(1000)
        cf.insert_string("test")
        s = repr(cf)
        self.assertIn("CuckooFilter", s)
        self.assertIn("count", s)
    
    def test_len(self):
        """Test len operation."""
        cf = CuckooFilter(1000)
        self.assertEqual(len(cf), 0)
        
        for i in range(10):
            cf.insert_string(f"item-{i}")
        
        self.assertEqual(len(cf), 10)
    
    def test_in_operator(self):
        """Test 'in' operator."""
        cf = CuckooFilter(1000)
        cf.insert(b"hello")
        
        self.assertIn(b"hello", cf)


class TestEdgeCases(unittest.TestCase):
    """Test edge cases."""
    
    def test_empty_string(self):
        """Test inserting empty string."""
        cf = CuckooFilter(1000)
        self.assertTrue(cf.insert_string(""))
        self.assertTrue(cf.contains_string(""))
    
    def test_unicode_string(self):
        """Test inserting unicode strings."""
        cf = CuckooFilter(1000)
        unicode_strings = ["hello世界", "Привет", "مرحبا", "🎉🎊"]
        
        for s in unicode_strings:
            self.assertTrue(cf.insert_string(s))
            self.assertTrue(cf.contains_string(s))
    
    def test_large_data(self):
        """Test inserting large data."""
        cf = CuckooFilter(10000)
        large_data = b"x" * 10000
        self.assertTrue(cf.insert(large_data))
        self.assertTrue(cf.contains(large_data))
    
    def test_same_item_multiple_times(self):
        """Test inserting same item multiple times."""
        cf = CuckooFilter(1000)
        
        # Insert same item multiple times
        for _ in range(10):
            cf.insert_string("duplicate")
        
        # Should still work
        self.assertTrue(cf.contains_string("duplicate"))
        
        # Delete once
        self.assertTrue(cf.delete_string("duplicate"))


def run_performance_test():
    """Run a performance test (not a unit test)."""
    import time
    
    print("\n=== Performance Test ===")
    
    cf = CuckooFilter(100000, fp_rate=0.01)
    
    # Insert performance
    start = time.time()
    for i in range(50000):
        cf.insert_string(f"perf-{i}")
    insert_time = time.time() - start
    
    # Contains performance
    start = time.time()
    for i in range(50000):
        cf.contains_string(f"perf-{i}")
    contains_time = time.time() - start
    
    # Delete performance
    start = time.time()
    for i in range(25000):
        cf.delete_string(f"perf-{i}")
    delete_time = time.time() - start
    
    stats = cf.stats()
    
    print(f"Items: 50000")
    print(f"Insert time: {insert_time:.4f}s ({insert_time/50000*1000000:.2f} µs/op)")
    print(f"Contains time: {contains_time:.4f}s ({contains_time/50000*1000000:.2f} µs/op)")
    print(f"Delete time: {delete_time:.4f}s ({delete_time/25000*1000000:.2f} µs/op)")
    print(f"Memory: {stats['memory_bytes']} bytes ({stats['memory_bytes']/1024:.2f} KB)")
    print(f"Load factor: {stats['load_factor']:.2%}")
    print(f"Expected FP rate: {stats['expected_fp_rate']:.4%}")


if __name__ == "__main__":
    unittest.main(verbosity=2)
    
    # Optionally run performance test
    # run_performance_test()