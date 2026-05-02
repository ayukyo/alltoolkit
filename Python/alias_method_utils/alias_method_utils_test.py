"""
Unit Tests for Alias Method Utils

Tests for Walker's Alias Method implementation for O(1) weighted random sampling.
"""

import unittest
import random
from collections import Counter
from mod import (
    AliasMethod,
    WeightedRandomPicker,
    AliasMethodBuilder,
    create_alias_from_dict,
    sample_with_weights,
    weighted_shuffle,
)


class TestAliasMethod(unittest.TestCase):
    """Tests for AliasMethod class."""
    
    def test_basic_construction(self):
        """Test basic construction with simple weights."""
        weights = [1, 2, 3, 4]
        alias = AliasMethod(weights)
        self.assertEqual(len(alias), 4)
    
    def test_uniform_weights(self):
        """Test with uniform weights."""
        weights = [1, 1, 1, 1]
        alias = AliasMethod(weights)
        
        # Sample many times and check distribution
        samples = [alias.sample() for _ in range(10000)]
        counts = Counter(samples)
        
        # Each should be roughly 25% (2500)
        for i in range(4):
            self.assertGreater(counts[i], 2000)  # Allow some variance
            self.assertLess(counts[i], 3000)
    
    def test_weighted_distribution(self):
        """Test that weights are respected."""
        weights = [1, 9]  # 10% and 90%
        alias = AliasMethod(weights)
        
        # Sample many times
        samples = [alias.sample() for _ in range(10000)]
        counts = Counter(samples)
        
        # Should be roughly 10% and 90%
        ratio = counts[1] / counts[0]
        self.assertGreater(ratio, 6)  # At least 6:1
        self.assertLess(ratio, 12)  # At most 12:1
    
    def test_single_element(self):
        """Test with a single element."""
        weights = [5.0]
        alias = AliasMethod(weights)
        
        for _ in range(100):
            self.assertEqual(alias.sample(), 0)
    
    def test_zero_weights_allowed(self):
        """Test that zero weights are allowed."""
        weights = [1, 0, 0, 4]  # Only 0 and 3 should be selectable
        alias = AliasMethod(weights)
        
        samples = [alias.sample() for _ in range(1000)]
        counts = Counter(samples)
        
        # 0 and 3 should be the only values
        self.assertEqual(set(counts.keys()), {0, 3})
        # 3 should appear ~4x more often
        ratio = counts[3] / counts[0]
        self.assertGreater(ratio, 2.5)
        self.assertLess(ratio, 6)
    
    def test_empty_weights_raises(self):
        """Test that empty weights raise ValueError."""
        with self.assertRaises(ValueError):
            AliasMethod([])
    
    def test_all_zero_weights_raises(self):
        """Test that all zero weights raise ValueError."""
        with self.assertRaises(ValueError):
            AliasMethod([0, 0, 0])
    
    def test_negative_weights_raises(self):
        """Test that negative weights raise ValueError."""
        with self.assertRaises(ValueError):
            AliasMethod([1, -1, 2])
    
    def test_sample_with_rng(self):
        """Test sampling with custom random generator."""
        weights = [1, 2, 3]
        alias = AliasMethod(weights)
        
        rng = random.Random(42)
        samples = [alias.sample(rng) for _ in range(10)]
        
        # With seeded RNG, should get consistent results
        rng2 = random.Random(42)
        alias2 = AliasMethod(weights)
        samples2 = [alias2.sample(rng2) for _ in range(10)]
        
        self.assertEqual(samples, samples2)
    
    def test_sample_n_with_replacement(self):
        """Test sampling multiple items with replacement."""
        weights = [1, 1, 1]
        alias = AliasMethod(weights)
        
        samples = alias.sample_n(100, replace=True)
        self.assertEqual(len(samples), 100)
        self.assertTrue(all(0 <= s < 3 for s in samples))
    
    def test_sample_n_without_replacement(self):
        """Test sampling multiple items without replacement."""
        weights = [1, 2, 3, 4]
        alias = AliasMethod(weights)
        
        samples = alias.sample_n(4, replace=False)
        self.assertEqual(len(samples), 4)
        self.assertEqual(set(samples), {0, 1, 2, 3})  # All unique
    
    def test_sample_n_without_replacement_limited(self):
        """Test sampling without replacement when n > population."""
        weights = [1, 2, 3]
        alias = AliasMethod(weights)
        
        samples = alias.sample_n(10, replace=False)
        self.assertEqual(len(samples), 3)  # Limited to population size
        self.assertEqual(set(samples), {0, 1, 2})
    
    def test_sample_n_negative_raises(self):
        """Test that negative n raises ValueError."""
        weights = [1, 2, 3]
        alias = AliasMethod(weights)
        
        with self.assertRaises(ValueError):
            alias.sample_n(-1)
    
    def test_probabilities_property(self):
        """Test that probabilities are correctly normalized."""
        weights = [1, 2, 3]
        alias = AliasMethod(weights)
        
        probs = alias.probabilities
        self.assertAlmostEqual(sum(probs), 1.0, places=10)
        self.assertAlmostEqual(probs[0], 1/6, places=10)
        self.assertAlmostEqual(probs[1], 2/6, places=10)
        self.assertAlmostEqual(probs[2], 3/6, places=10)
    
    def test_weights_property(self):
        """Test that original weights are preserved."""
        weights = [1.5, 2.5, 3.5]
        alias = AliasMethod(weights)
        
        self.assertEqual(alias.weights, weights)
    
    def test_get_probability(self):
        """Test getting probability of specific index."""
        weights = [1, 2, 3]
        alias = AliasMethod(weights)
        
        self.assertAlmostEqual(alias.get_probability(0), 1/6, places=10)
        self.assertAlmostEqual(alias.get_probability(1), 2/6, places=10)
        self.assertAlmostEqual(alias.get_probability(2), 3/6, places=10)
    
    def test_get_probability_out_of_range(self):
        """Test that out of range index raises."""
        weights = [1, 2, 3]
        alias = AliasMethod(weights)
        
        with self.assertRaises(IndexError):
            alias.get_probability(5)
    
    def test_no_normalize(self):
        """Test construction without normalization."""
        weights = [0.25, 0.5, 0.25]  # Already sum to 1
        alias = AliasMethod(weights, normalize=False)
        
        probs = alias.probabilities
        self.assertAlmostEqual(probs[0], 0.25, places=10)
        self.assertAlmostEqual(probs[1], 0.5, places=10)
        self.assertAlmostEqual(probs[2], 0.25, places=10)
    
    def test_repr(self):
        """Test string representation."""
        weights = [1, 2, 3]
        alias = AliasMethod(weights)
        self.assertEqual(repr(alias), "AliasMethod(size=3)")


class TestWeightedRandomPicker(unittest.TestCase):
    """Tests for WeightedRandomPicker class."""
    
    def test_basic_picking(self):
        """Test basic item picking."""
        items = ['a', 'b', 'c']
        weights = [1, 2, 3]
        picker = WeightedRandomPicker(items, weights)
        
        # Should pick one of the items
        for _ in range(100):
            item = picker.pick()
            self.assertIn(item, items)
    
    def test_weighted_picking(self):
        """Test that weights affect picking probability."""
        items = ['rare', 'common']
        weights = [1, 9]  # 10% rare, 90% common
        picker = WeightedRandomPicker(items, weights)
        
        samples = [picker.pick() for _ in range(10000)]
        counts = Counter(samples)
        
        ratio = counts['common'] / counts['rare']
        self.assertGreater(ratio, 6)
        self.assertLess(ratio, 12)
    
    def test_pick_n(self):
        """Test picking multiple items."""
        items = ['a', 'b', 'c']
        weights = [1, 1, 1]
        picker = WeightedRandomPicker(items, weights)
        
        samples = picker.pick_n(50)
        self.assertEqual(len(samples), 50)
        self.assertTrue(all(s in items for s in samples))
    
    def test_pick_n_without_replacement(self):
        """Test picking without replacement."""
        items = ['a', 'b', 'c', 'd']
        weights = [1, 1, 1, 1]
        picker = WeightedRandomPicker(items, weights)
        
        samples = picker.pick_n(4, replace=False)
        self.assertEqual(len(samples), 4)
        self.assertEqual(set(samples), set(items))
    
    def test_items_property(self):
        """Test items property."""
        items = ['x', 'y', 'z']
        weights = [1, 2, 3]
        picker = WeightedRandomPicker(items, weights)
        
        self.assertEqual(picker.items, items)
    
    def test_probabilities_property(self):
        """Test probabilities property."""
        items = ['a', 'b']
        weights = [1, 3]
        picker = WeightedRandomPicker(items, weights)
        
        probs = picker.probabilities
        self.assertAlmostEqual(probs[0], 0.25, places=10)
        self.assertAlmostEqual(probs[1], 0.75, places=10)
    
    def test_get_item_probability(self):
        """Test getting probability of specific item."""
        items = ['a', 'b', 'c']
        weights = [1, 2, 3]
        picker = WeightedRandomPicker(items, weights)
        
        self.assertAlmostEqual(picker.get_item_probability('a'), 1/6, places=10)
        self.assertAlmostEqual(picker.get_item_probability('b'), 2/6, places=10)
        self.assertAlmostEqual(picker.get_item_probability('c'), 3/6, places=10)
    
    def test_get_item_probability_not_found(self):
        """Test that non-existent item raises ValueError."""
        items = ['a', 'b', 'c']
        weights = [1, 2, 3]
        picker = WeightedRandomPicker(items, weights)
        
        with self.assertRaises(ValueError):
            picker.get_item_probability('z')
    
    def test_length_mismatch_raises(self):
        """Test that mismatched lengths raise ValueError."""
        items = ['a', 'b', 'c']
        weights = [1, 2]
        
        with self.assertRaises(ValueError):
            WeightedRandomPicker(items, weights)
    
    def test_repr(self):
        """Test string representation."""
        items = ['a', 'b']
        weights = [1, 2]
        picker = WeightedRandomPicker(items, weights)
        self.assertEqual(repr(picker), "WeightedRandomPicker(size=2)")


class TestAliasMethodBuilder(unittest.TestCase):
    """Tests for AliasMethodBuilder class."""
    
    def test_basic_building(self):
        """Test basic builder functionality."""
        builder = AliasMethodBuilder()
        builder.add('a', 1.0)
        builder.add('b', 2.0)
        builder.add('c', 3.0)
        
        picker = builder.build_picker()
        
        samples = [picker.pick() for _ in range(100)]
        self.assertTrue(all(s in ['a', 'b', 'c'] for s in samples))
    
    def test_add_many(self):
        """Test adding multiple items at once."""
        builder = AliasMethodBuilder()
        builder.add_many(['a', 'b', 'c'], [1, 2, 3])
        
        self.assertEqual(builder.size, 3)
        
        picker = builder.build_picker()
        self.assertEqual(len(picker), 3)
    
    def test_negative_weight_raises(self):
        """Test that negative weight raises ValueError."""
        builder = AliasMethodBuilder()
        
        with self.assertRaises(ValueError):
            builder.add('a', -1)
    
    def test_add_many_length_mismatch(self):
        """Test that add_many with mismatched lengths raises."""
        builder = AliasMethodBuilder()
        
        with self.assertRaises(ValueError):
            builder.add_many(['a', 'b'], [1, 2, 3])
    
    def test_clear(self):
        """Test clearing the builder."""
        builder = AliasMethodBuilder()
        builder.add('a', 1)
        builder.add('b', 2)
        
        self.assertEqual(builder.size, 2)
        
        builder.clear()
        self.assertEqual(builder.size, 0)
    
    def test_build_empty_raises(self):
        """Test that building empty raises ValueError."""
        builder = AliasMethodBuilder()
        
        with self.assertRaises(ValueError):
            builder.build()
        
        with self.assertRaises(ValueError):
            builder.build_picker()
    
    def test_build_alias_method(self):
        """Test building AliasMethod directly."""
        builder = AliasMethodBuilder()
        builder.add('a', 1)
        builder.add('b', 2)
        
        alias = builder.build()
        self.assertEqual(len(alias), 2)


class TestConvenienceFunctions(unittest.TestCase):
    """Tests for convenience functions."""
    
    def test_create_alias_from_dict(self):
        """Test creating picker from dictionary."""
        weight_dict = {'apple': 1, 'banana': 2, 'cherry': 3}
        picker = create_alias_from_dict(weight_dict)
        
        self.assertEqual(len(picker), 3)
        
        samples = [picker.pick() for _ in range(100)]
        self.assertTrue(all(s in weight_dict for s in samples))
    
    def test_sample_with_weights(self):
        """Test sample_with_weights function."""
        items = ['a', 'b', 'c']
        weights = [1, 2, 3]
        
        samples = sample_with_weights(items, weights, n=100)
        self.assertEqual(len(samples), 100)
        self.assertTrue(all(s in items for s in samples))
    
    def test_sample_with_weights_no_replacement(self):
        """Test sample_with_weights without replacement."""
        items = ['a', 'b', 'c', 'd']
        weights = [1, 1, 1, 1]
        
        samples = sample_with_weights(items, weights, n=4, replace=False)
        self.assertEqual(len(samples), 4)
        self.assertEqual(set(samples), set(items))
    
    def test_weighted_shuffle(self):
        """Test weighted_shuffle function."""
        items = ['a', 'b', 'c', 'd']
        weights = [1, 2, 3, 4]
        
        shuffled = weighted_shuffle(items, weights)
        self.assertEqual(len(shuffled), 4)
        self.assertEqual(set(shuffled), set(items))
    
    def test_weighted_shuffle_respects_weights(self):
        """Test that weighted_shuffle respects weights."""
        items = ['rare', 'common']
        weights = [1, 9]
        
        # Shuffle many times and count first positions
        first_positions = Counter()
        for _ in range(1000):
            shuffled = weighted_shuffle(items, weights)
            first_positions[shuffled[0]] += 1
        
        # 'common' should appear first more often
        ratio = first_positions['common'] / first_positions['rare']
        self.assertGreater(ratio, 3)  # Should be biased towards 'common'


class TestEdgeCases(unittest.TestCase):
    """Tests for edge cases and special scenarios."""
    
    def test_large_weights(self):
        """Test with very large weights."""
        weights = [1e10, 1e10, 1e10]
        alias = AliasMethod(weights)
        
        samples = [alias.sample() for _ in range(100)]
        self.assertTrue(all(0 <= s < 3 for s in samples))
    
    def test_small_weights(self):
        """Test with very small weights."""
        weights = [1e-10, 1e-10, 1e-10]
        alias = AliasMethod(weights)
        
        samples = [alias.sample() for _ in range(100)]
        self.assertTrue(all(0 <= s < 3 for s in samples))
    
    def test_mixed_weights(self):
        """Test with mixed large and small weights."""
        weights = [1e-10, 1, 1e10]
        alias = AliasMethod(weights)
        
        samples = [alias.sample() for _ in range(100)]
        self.assertTrue(all(0 <= s < 3 for s in samples))
    
    def test_float_weights(self):
        """Test with floating point weights."""
        weights = [0.1, 0.2, 0.3, 0.4]
        alias = AliasMethod(weights)
        
        probs = alias.probabilities
        self.assertAlmostEqual(probs[0], 0.1, places=10)
        self.assertAlmostEqual(probs[1], 0.2, places=10)
        self.assertAlmostEqual(probs[2], 0.3, places=10)
        self.assertAlmostEqual(probs[3], 0.4, places=10)
    
    def test_integer_weights(self):
        """Test with integer weights."""
        weights = [1, 2, 3, 4]
        alias = AliasMethod(weights)
        
        probs = alias.probabilities
        self.assertAlmostEqual(sum(probs), 1.0, places=10)
    
    def test_binary_weights(self):
        """Test with binary (0/1) weights."""
        weights = [0, 1, 0, 1, 0]
        alias = AliasMethod(weights)
        
        samples = [alias.sample() for _ in range(1000)]
        unique_samples = set(samples)
        
        # Only indices 1 and 3 should be sampled
        self.assertEqual(unique_samples, {1, 3})
    
    def test_many_items(self):
        """Test with many items."""
        n = 10000
        weights = list(range(1, n + 1))
        alias = AliasMethod(weights)
        
        self.assertEqual(len(alias), n)
        
        # Sampling should still work efficiently
        samples = [alias.sample() for _ in range(100)]
        self.assertTrue(all(0 <= s < n for s in samples))
    
    def test_seeded_reproducibility(self):
        """Test that seeded RNG produces reproducible results."""
        weights = [1, 2, 3, 4, 5]
        alias = AliasMethod(weights)
        
        rng1 = random.Random(12345)
        samples1 = [alias.sample(rng1) for _ in range(100)]
        
        rng2 = random.Random(12345)
        samples2 = [alias.sample(rng2) for _ in range(100)]
        
        self.assertEqual(samples1, samples2)
    
    def test_picker_with_different_types(self):
        """Test picker with different item types."""
        # Numbers
        picker1 = WeightedRandomPicker([1, 2, 3], [1, 1, 1])
        self.assertIn(picker1.pick(), [1, 2, 3])
        
        # Tuples
        picker2 = WeightedRandomPicker([(1, 2), (3, 4)], [1, 1])
        self.assertIn(picker2.pick(), [(1, 2), (3, 4)])
        
        # Dicts
        picker3 = WeightedRandomPicker([{'a': 1}, {'b': 2}], [1, 1])
        self.assertIn(picker3.pick(), [{'a': 1}, {'b': 2}])


class TestPerformance(unittest.TestCase):
    """Tests for performance characteristics."""
    
    def test_sampling_is_o1(self):
        """Test that sampling remains fast with large distributions."""
        import time
        
        # Create large distribution
        n = 100000
        weights = list(range(1, n + 1))
        alias = AliasMethod(weights)
        
        # Time sampling (should be O(1) per sample)
        start = time.time()
        for _ in range(10000):
            alias.sample()
        elapsed = time.time() - start
        
        # Should be very fast (< 1 second for 10k samples)
        self.assertLess(elapsed, 1.0)
    
    def test_construction_is_on(self):
        """Test that construction is O(n)."""
        import time
        
        # Time construction with increasing sizes
        times = []
        sizes = [1000, 10000, 100000]
        
        for n in sizes:
            weights = list(range(1, n + 1))
            start = time.time()
            AliasMethod(weights)
            elapsed = time.time() - start
            times.append(elapsed)
        
        # Construction time should grow roughly linearly
        # Not a strict test, just sanity check
        # 100k items should still construct in < 1 second
        self.assertLess(times[-1], 1.0)


if __name__ == '__main__':
    unittest.main()