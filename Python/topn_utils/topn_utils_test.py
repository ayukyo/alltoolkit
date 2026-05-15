"""
Unit tests for topn_utils module.

Run with: python -m pytest topn_utils_test.py -v
Or: python topn_utils_test.py
"""

import unittest
import time
import random
from topn_utils import (
    TopNSelector,
    TopNResult,
    heap_top_n,
    quickselect_top_n,
    streaming_top_n,
    TimeWindowTopN,
    CategoryTopN,
    WeightedTopN,
    IncrementalTopN,
    top_n,
    bottom_n,
    benchmark_top_n,
)


class TestHeapTopN(unittest.TestCase):
    """Tests for heap_top_n function."""
    
    def test_basic(self):
        """Test basic top-N selection."""
        data = [5, 2, 8, 1, 9, 3]
        result = heap_top_n(data, 3)
        self.assertEqual(len(result), 3)
        scores = [s for _, s in result]
        self.assertEqual(scores, [9, 8, 5])
    
    def test_n_larger_than_data(self):
        """Test when n is larger than data size."""
        data = [1, 2, 3]
        result = heap_top_n(data, 10)
        self.assertEqual(len(result), 3)
        scores = [s for _, s in result]
        self.assertEqual(scores, [3, 2, 1])
    
    def test_n_zero(self):
        """Test with n=0."""
        result = heap_top_n([1, 2, 3], 0)
        self.assertEqual(result, [])
    
    def test_empty_data(self):
        """Test with empty data."""
        result = heap_top_n([], 5)
        self.assertEqual(result, [])
    
    def test_custom_key(self):
        """Test with custom key function."""
        data = ["apple", "banana", "cherry", "date"]
        result = heap_top_n(data, 2, key=len)
        self.assertEqual(len(result), 2)
        items = [item for item, _ in result]
        self.assertIn("banana", items)
        self.assertIn("cherry", items)
    
    def test_duplicate_scores(self):
        """Test handling of duplicate scores."""
        data = [5, 5, 5, 5, 5]
        result = heap_top_n(data, 3)
        self.assertEqual(len(result), 3)
        for item, score in result:
            self.assertEqual(score, 5)
    
    def test_keep_ties(self):
        """Test keep_ties option."""
        data = [5, 5, 5, 1, 2, 3]
        result = heap_top_n(data, 2, keep_ties=True)
        # Should keep all items with score 5
        self.assertGreaterEqual(len(result), 3)
        for item, score in result:
            self.assertEqual(score, 5)
    
    def test_negative_scores(self):
        """Test with negative scores."""
        data = [-5, -2, -8, -1, -9, -3]
        result = heap_top_n(data, 3)
        scores = [s for _, s in result]
        self.assertEqual(scores, [-1, -2, -3])


class TestQuickselectTopN(unittest.TestCase):
    """Tests for quickselect_top_n function."""
    
    def test_basic(self):
        """Test basic top-N selection."""
        data = [5, 2, 8, 1, 9, 3]
        result = quickselect_top_n(data.copy(), 3)
        self.assertEqual(len(result), 3)
        scores = [s for _, s in result]
        self.assertEqual(scores, [9, 8, 5])
    
    def test_n_larger_than_data(self):
        """Test when n is larger than data size."""
        data = [1, 2, 3]
        result = quickselect_top_n(data.copy(), 10)
        self.assertEqual(len(result), 3)
        scores = [s for _, s in result]
        self.assertEqual(scores, [3, 2, 1])
    
    def test_n_zero(self):
        """Test with n=0."""
        result = quickselect_top_n([1, 2, 3], 0)
        self.assertEqual(result, [])
    
    def test_empty_data(self):
        """Test with empty data."""
        result = quickselect_top_n([], 5)
        self.assertEqual(result, [])
    
    def test_custom_key(self):
        """Test with custom key function."""
        data = ["apple", "banana", "cherry", "date"]
        result = quickselect_top_n(data.copy(), 2, key=len)
        items = [item for item, _ in result]
        self.assertIn("banana", items)
        self.assertIn("cherry", items)
    
    def test_large_dataset(self):
        """Test with large dataset."""
        random.seed(42)
        data = [random.random() * 1000 for _ in range(10000)]
        result = quickselect_top_n(data.copy(), 100)
        self.assertEqual(len(result), 100)
        # Verify sorted
        scores = [s for _, s in result]
        self.assertEqual(scores, sorted(scores, reverse=True))


class TestStreamingTopN(unittest.TestCase):
    """Tests for streaming_top_n function."""
    
    def test_basic(self):
        """Test basic streaming top-N."""
        data = range(100)
        result = streaming_top_n(data, 5)
        self.assertEqual(len(result), 5)
        items = [item for item, _ in result]
        self.assertEqual(items, [99, 98, 97, 96, 95])
    
    def test_checkpoint(self):
        """Test checkpoint functionality."""
        checkpoints = []
        
        def save_checkpoint(top_items):
            checkpoints.append(len(top_items))
        
        data = range(1000)
        result = streaming_top_n(
            data, 5,
            checkpoint_func=save_checkpoint,
            checkpoint_interval=100
        )
        self.assertGreater(len(checkpoints), 0)
    
    def test_empty_data(self):
        """Test with empty data."""
        result = streaming_top_n([], 5)
        self.assertEqual(result, [])


class TestTopNSelector(unittest.TestCase):
    """Tests for TopNSelector class."""
    
    def test_basic(self):
        """Test basic selector functionality."""
        selector = TopNSelector(lambda x: x, max_size=5)
        selector.add_items([5, 2, 8, 1, 9, 3, 7, 4, 6])
        result = selector.get_top_n(3)
        scores = [s for _, s in result]
        self.assertEqual(scores, [9, 8, 7])
    
    def test_max_size(self):
        """Test max_size constraint."""
        selector = TopNSelector(lambda x: x, max_size=3)
        added = selector.add_items([1, 2, 3, 4, 5, 6, 7, 8, 9])
        self.assertEqual(selector.size, 3)
    
    def test_rejected_items(self):
        """Test that low-score items are rejected."""
        selector = TopNSelector(lambda x: x, max_size=3)
        selector.add_items([10, 9, 8, 1, 2, 3])
        result = selector.get_top_n()
        items = [item for item, _ in result]
        self.assertEqual(items, [10, 9, 8])
    
    def test_custom_key(self):
        """Test with custom key function."""
        selector = TopNSelector(lambda x: -x)
        selector.add_items([1, 2, 3, 4, 5])
        result = selector.get_top_n(3)
        scores = [s for _, s in result]
        self.assertEqual(scores, [-1, -2, -3])
    
    def test_clear(self):
        """Test clear functionality."""
        selector = TopNSelector(lambda x: x)
        selector.add_items([1, 2, 3])
        selector.clear()
        self.assertEqual(selector.size, 0)
    
    def test_comparisons_tracking(self):
        """Test that comparisons are tracked."""
        selector = TopNSelector(lambda x: x)
        selector.add_items([1, 2, 3, 4, 5])
        self.assertGreater(selector.comparisons, 0)


class TestTimeWindowTopN(unittest.TestCase):
    """Tests for TimeWindowTopN class."""
    
    def test_basic(self):
        """Test basic time-windowed tracking."""
        window = TimeWindowTopN(window_seconds=60, n=5)
        window.add("item1", 10.0)
        window.add("item2", 20.0)
        window.add("item3", 15.0)
        result = window.get_top_n(2)
        self.assertEqual(len(result), 2)
        items = [item for item, _ in result]
        self.assertEqual(items, ["item2", "item3"])
    
    def test_expiry(self):
        """Test that old items expire."""
        window = TimeWindowTopN(window_seconds=1, n=5)
        
        # Add items with old timestamp
        old_time = time.time() - 2
        window.add("old_item", 100.0, timestamp=old_time)
        
        # Add new item
        window.add("new_item", 1.0)
        
        result = window.get_top_n()
        items = [item for item, _ in result]
        self.assertNotIn("old_item", items)
        self.assertIn("new_item", items)
    
    def test_clear(self):
        """Test clear functionality."""
        window = TimeWindowTopN(window_seconds=60, n=5)
        window.add("item1", 10.0)
        window.clear()
        result = window.get_top_n()
        self.assertEqual(result, [])


class TestCategoryTopN(unittest.TestCase):
    """Tests for CategoryTopN class."""
    
    def test_basic(self):
        """Test basic category-based tracking."""
        cat_top = CategoryTopN(n=3)
        cat_top.add("fruit", "apple", 5.0)
        cat_top.add("fruit", "banana", 3.0)
        cat_top.add("fruit", "cherry", 7.0)
        cat_top.add("vegetable", "carrot", 4.0)
        
        fruit_result = cat_top.get_top_n("fruit")
        veg_result = cat_top.get_top_n("vegetable")
        
        self.assertEqual(len(fruit_result), 3)
        self.assertEqual(len(veg_result), 1)
    
    def test_top_n_per_category(self):
        """Test getting top-N for each category."""
        cat_top = CategoryTopN(n=2)
        cat_top.add("a", "item1", 10.0)
        cat_top.add("a", "item2", 20.0)
        cat_top.add("a", "item3", 30.0)  # Should be included (highest)
        cat_top.add("b", "item4", 5.0)
        
        a_result = cat_top.get_top_n("a")
        self.assertEqual(len(a_result), 2)
        items = [item for item, _ in a_result]
        self.assertIn("item3", items)
        self.assertIn("item2", items)
    
    def test_all_categories(self):
        """Test getting all categories."""
        cat_top = CategoryTopN(n=3)
        cat_top.add("cat1", "item1", 1.0)
        cat_top.add("cat2", "item2", 2.0)
        
        categories = cat_top.get_all_categories()
        self.assertEqual(set(categories), {"cat1", "cat2"})
    
    def test_clear_category(self):
        """Test clearing specific category."""
        cat_top = CategoryTopN(n=3)
        cat_top.add("a", "item1", 1.0)
        cat_top.add("b", "item2", 2.0)
        
        cat_top.clear("a")
        self.assertEqual(cat_top.get_top_n("a"), [])
        self.assertEqual(len(cat_top.get_top_n("b")), 1)


class TestWeightedTopN(unittest.TestCase):
    """Tests for WeightedTopN class."""
    
    def test_basic(self):
        """Test basic weighted scoring."""
        weighted = WeightedTopN()
        weighted.add_weight("a", 0.5)
        weighted.add_weight("b", 0.5)
        
        weighted.add_item("item1", {"a": 100, "b": 0})  # Score: 50
        weighted.add_item("item2", {"a": 0, "b": 100})  # Score: 50
        weighted.add_item("item3", {"a": 100, "b": 100})  # Score: 100
        
        result = weighted.get_top_n()
        items = [item for item, _, _ in result]
        self.assertEqual(items[0], "item3")
    
    def test_weight_normalization(self):
        """Test that weights are normalized."""
        weighted = WeightedTopN()
        weighted.add_weight("a", 1)
        weighted.add_weight("b", 3)  # Should be normalized to 0.25, 0.75
        
        weighted.add_item("item1", {"a": 100, "b": 0})  # Score: 25
        weighted.add_item("item2", {"a": 0, "b": 100})  # Score: 75
        
        result = weighted.get_top_n()
        self.assertEqual(result[0][0], "item2")
        self.assertEqual(result[1][0], "item1")
    
    def test_missing_scores(self):
        """Test handling of missing score dimensions."""
        weighted = WeightedTopN()
        weighted.add_weight("a", 1.0)
        
        weighted.add_item("item1", {"a": 100})
        weighted.add_item("item2", {})  # Missing score defaults to 0
        
        result = weighted.get_top_n()
        self.assertEqual(result[0][0], "item1")


class TestIncrementalTopN(unittest.TestCase):
    """Tests for IncrementalTopN class."""
    
    def test_basic(self):
        """Test basic incremental tracking."""
        inc = IncrementalTopN(n=5)
        inc.update("a", 10)
        inc.update("b", 20)
        inc.update("c", 15)
        
        result = inc.get_top_n()
        items = [item for item, _ in result]
        self.assertEqual(items, ["b", "c", "a"])
    
    def test_update_max_mode(self):
        """Test update in max mode."""
        inc = IncrementalTopN(n=5, mode="max")
        inc.update("a", 10)
        inc.update("a", 20)  # Should replace
        inc.update("a", 5)   # Should be ignored
        
        self.assertEqual(inc.get_score("a"), 20)
    
    def test_update_sum_mode(self):
        """Test update in sum mode."""
        inc = IncrementalTopN(n=5, mode="sum")
        inc.update("a", 10)
        inc.update("a", 20)
        inc.update("a", 5)
        
        self.assertEqual(inc.get_score("a"), 35)
    
    def test_remove(self):
        """Test item removal."""
        inc = IncrementalTopN(n=5)
        inc.update("a", 10)
        inc.update("b", 20)
        
        removed = inc.remove("a")
        self.assertTrue(removed)
        self.assertIsNone(inc.get_score("a"))
        
        removed = inc.remove("nonexistent")
        self.assertFalse(removed)
    
    def test_get_rank(self):
        """Test rank retrieval."""
        inc = IncrementalTopN(n=5)
        inc.update("a", 100)
        inc.update("b", 50)
        inc.update("c", 75)
        
        self.assertEqual(inc.get_rank("a"), 1)
        self.assertEqual(inc.get_rank("c"), 2)
        self.assertEqual(inc.get_rank("b"), 3)
        self.assertIsNone(inc.get_rank("nonexistent"))
    
    def test_get_percentile(self):
        """Test percentile calculation."""
        inc = IncrementalTopN(n=100)
        inc.update("a", 100)
        inc.update("b", 50)
        inc.update("c", 75)
        
        # a is highest (100%), c is middle (50%), b is lowest (0%)
        self.assertEqual(inc.get_percentile("a"), 100.0)
        self.assertEqual(inc.get_percentile("b"), 0.0)
    
    def test_clear(self):
        """Test clear functionality."""
        inc = IncrementalTopN(n=5)
        inc.update("a", 10)
        inc.clear()
        self.assertEqual(inc.size, 0)


class TestConvenienceFunctions(unittest.TestCase):
    """Tests for convenience functions."""
    
    def test_top_n(self):
        """Test top_n function."""
        data = [5, 2, 8, 1, 9, 3]
        result = top_n(data, 3)
        scores = [s for _, s in result]
        self.assertEqual(scores, [9, 8, 5])
    
    def test_top_n_with_algorithm(self):
        """Test top_n with algorithm selection."""
        data = [5, 2, 8, 1, 9, 3]
        
        result_heap = top_n(data, 3, algorithm="heap")
        result_quick = top_n(data.copy(), 3, algorithm="quickselect")
        
        self.assertEqual(result_heap, result_quick)
    
    def test_bottom_n(self):
        """Test bottom_n function."""
        data = [5, 2, 8, 1, 9, 3, 1]  # Added another 1
        result = bottom_n(data, 3)
        scores = [s for _, s in result]
        self.assertEqual(scores, [1, 1, 2])


class TestBenchmarkTopN(unittest.TestCase):
    """Tests for benchmark_top_n function."""
    
    def test_benchmark(self):
        """Test that benchmark runs without error."""
        results = benchmark_top_n(size=1000, n=10)
        
        self.assertIn("heap", results)
        self.assertIn("quickselect", results)
        self.assertIn("sorted", results)
        
        for algo, data in results.items():
            self.assertIn("time_seconds", data)
            self.assertIn("items_per_second", data)


class TestEdgeCases(unittest.TestCase):
    """Tests for edge cases and error handling."""
    
    def test_single_item(self):
        """Test with single item."""
        result = heap_top_n([42], 5)
        self.assertEqual(result, [(42, 42)])
    
    def test_all_same_scores(self):
        """Test with all items having same score."""
        data = [5] * 100
        result = heap_top_n(data, 10)
        self.assertEqual(len(result), 10)
        for item, score in result:
            self.assertEqual(score, 5)
    
    def test_very_large_n(self):
        """Test with n much larger than data."""
        data = [1, 2, 3]
        result = heap_top_n(data, 1000000)
        self.assertEqual(len(result), 3)
    
    def test_floating_point_scores(self):
        """Test with floating point scores."""
        data = [1.5, 2.7, 3.14159, 0.001]
        result = heap_top_n(data, 2)
        scores = [s for _, s in result]
        self.assertAlmostEqual(scores[0], 3.14159, places=5)
        self.assertAlmostEqual(scores[1], 2.7, places=5)
    
    def test_mixed_types(self):
        """Test with custom objects."""
        class Item:
            def __init__(self, name, score):
                self.name = name
                self.score = score
        
        items = [Item("a", 1), Item("b", 3), Item("c", 2)]
        result = heap_top_n(items, 2, key=lambda x: x.score)
        
        self.assertEqual(result[0][0].name, "b")
        self.assertEqual(result[1][0].name, "c")


class TestPerformance(unittest.TestCase):
    """Performance tests."""
    
    def test_large_dataset_heap(self):
        """Test heap algorithm with large dataset."""
        random.seed(42)
        data = [random.random() * 1000 for _ in range(100000)]
        
        start = time.time()
        result = heap_top_n(data, 100)
        elapsed = time.time() - start
        
        self.assertEqual(len(result), 100)
        self.assertLess(elapsed, 1.0)  # Should complete in under 1 second
    
    def test_large_dataset_quickselect(self):
        """Test quickselect algorithm with large dataset."""
        random.seed(42)
        data = [random.random() * 1000 for _ in range(100000)]
        
        start = time.time()
        result = quickselect_top_n(data.copy(), 100)
        elapsed = time.time() - start
        
        self.assertEqual(len(result), 100)
        self.assertLess(elapsed, 1.0)
    
    def test_streaming_memory(self):
        """Test that streaming uses limited memory."""
        # Generate a large iterator (doesn't create list in memory)
        def large_iterator():
            for i in range(1000000):
                yield random.random() * 1000
        
        random.seed(42)
        result = streaming_top_n(large_iterator(), 100)
        
        self.assertEqual(len(result), 100)


if __name__ == "__main__":
    unittest.main(verbosity=2)