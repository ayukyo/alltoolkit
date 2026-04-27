#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Tests for Weighted Random Utilities Module

Comprehensive test suite for weighted random selection utilities.
"""

import unittest
import random
import math
from collections import Counter
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from mod import (
    weighted_choice,
    weighted_choice_with_index,
    weighted_sample,
    weighted_shuffle,
    AliasMethod,
    WeightedReservoirSampler,
    normalize_weights,
    cumulative_weights,
    probability_from_cumulative,
    softmax_weights,
    exponential_weights,
    inverse_transform_sample,
    rejection_sample,
    weight_to_probability,
    probability_to_weight,
    kl_divergence,
    entropy,
    effective_size,
    batch_weighted_choice,
    weighted_coin_flip,
    weighted_random_range,
    EmptyWeightsError,
    InvalidWeightError,
    TotalWeightZeroError,
)


class TestWeightedChoice(unittest.TestCase):
    """Tests for weighted_choice function."""
    
    def test_basic_selection(self):
        """Test basic weighted selection."""
        items = ['a', 'b', 'c']
        weights = [1, 1, 1]
        
        # Should always return one of the items
        for _ in range(100):
            result = weighted_choice(items, weights)
            self.assertIn(result, items)
    
    def test_weight_distribution(self):
        """Test that selections follow weight distribution."""
        items = ['a', 'b', 'c']
        weights = [1, 2, 3]  # Total = 6, so a=1/6, b=2/6, c=3/6
        
        # Run many trials
        counter = Counter()
        for _ in range(10000):
            counter[weighted_choice(items, weights)] += 1
        
        # Check approximate distribution
        total = sum(counter.values())
        a_ratio = counter['a'] / total
        b_ratio = counter['b'] / total
        c_ratio = counter['c'] / total
        
        # Should be close to expected values (within 10% tolerance)
        self.assertAlmostEqual(a_ratio, 1/6, delta=0.05)
        self.assertAlmostEqual(b_ratio, 2/6, delta=0.05)
        self.assertAlmostEqual(c_ratio, 3/6, delta=0.05)
    
    def test_single_item(self):
        """Test with single item."""
        items = ['only']
        weights = [1]
        
        for _ in range(10):
            result = weighted_choice(items, weights)
            self.assertEqual(result, 'only')
    
    def test_reproducibility(self):
        """Test reproducibility with seeded random."""
        items = ['a', 'b', 'c', 'd', 'e']
        weights = [1, 2, 3, 4, 5]
        
        rng1 = random.Random(42)
        rng2 = random.Random(42)
        
        results1 = [weighted_choice(items, weights, random_instance=rng1) for _ in range(20)]
        results2 = [weighted_choice(items, weights, random_instance=rng2) for _ in range(20)]
        
        self.assertEqual(results1, results2)
    
    def test_empty_items(self):
        """Test that empty items raise error."""
        with self.assertRaises(EmptyWeightsError):
            weighted_choice([], [])
    
    def test_empty_weights(self):
        """Test that empty weights raise error."""
        with self.assertRaises(EmptyWeightsError):
            weighted_choice(['a', 'b'], [])
    
    def test_negative_weight(self):
        """Test that negative weights raise error."""
        with self.assertRaises(InvalidWeightError):
            weighted_choice(['a', 'b'], [1, -1])
    
    def test_zero_total_weight(self):
        """Test that zero total weight raises error."""
        with self.assertRaises(TotalWeightZeroError):
            weighted_choice(['a', 'b'], [0, 0])
    
    def test_mismatched_lengths(self):
        """Test that mismatched lengths raise error."""
        with self.assertRaises(ValueError):
            weighted_choice(['a', 'b', 'c'], [1, 2])


class TestWeightedChoiceWithIndex(unittest.TestCase):
    """Tests for weighted_choice_with_index function."""
    
    def test_returns_correct_index(self):
        """Test that returned index matches item."""
        items = ['a', 'b', 'c']
        weights = [1, 2, 3]
        
        for _ in range(100):
            item, idx = weighted_choice_with_index(items, weights)
            self.assertEqual(item, items[idx])
    
    def test_index_distribution(self):
        """Test that indices follow expected distribution."""
        items = ['a', 'b', 'c']
        weights = [1, 2, 3]
        
        counter = Counter()
        for _ in range(10000):
            _, idx = weighted_choice_with_index(items, weights)
            counter[idx] += 1
        
        total = sum(counter.values())
        self.assertAlmostEqual(counter[0] / total, 1/6, delta=0.05)
        self.assertAlmostEqual(counter[1] / total, 2/6, delta=0.05)
        self.assertAlmostEqual(counter[2] / total, 3/6, delta=0.05)


class TestWeightedSample(unittest.TestCase):
    """Tests for weighted_sample function."""
    
    def test_sample_with_replacement(self):
        """Test sampling with replacement."""
        items = ['a', 'b', 'c']
        weights = [1, 1, 1]
        
        sample = weighted_sample(items, weights, k=10)
        self.assertEqual(len(sample), 10)
        
        for item in sample:
            self.assertIn(item, items)
    
    def test_sample_without_replacement(self):
        """Test sampling without replacement."""
        items = ['a', 'b', 'c', 'd']
        weights = [1, 1, 1, 1]
        
        sample = weighted_sample(items, weights, k=4, replace=False)
        self.assertEqual(len(sample), 4)
        self.assertEqual(len(set(sample)), 4)  # All unique
    
    def test_sample_too_many_without_replacement(self):
        """Test that sampling too many items raises error."""
        items = ['a', 'b']
        weights = [1, 1]
        
        with self.assertRaises(ValueError):
            weighted_sample(items, weights, k=3, replace=False)
    
    def test_weight_distribution_in_sample(self):
        """Test that sampling follows weight distribution."""
        items = ['a', 'b', 'c']
        weights = [1, 2, 3]
        
        # Sample with replacement many times
        all_samples = []
        for _ in range(100):
            all_samples.extend(weighted_sample(items, weights, k=100))
        
        counter = Counter(all_samples)
        total = len(all_samples)
        
        # Check approximate distribution
        self.assertAlmostEqual(counter['a'] / total, 1/6, delta=0.05)
        self.assertAlmostEqual(counter['b'] / total, 2/6, delta=0.05)
        self.assertAlmostEqual(counter['c'] / total, 3/6, delta=0.05)


class TestAliasMethod(unittest.TestCase):
    """Tests for AliasMethod class."""
    
    def test_basic_sampling(self):
        """Test basic alias method sampling."""
        items = ['a', 'b', 'c', 'd']
        weights = [1, 2, 3, 4]
        
        alias = AliasMethod(items, weights)
        
        for _ in range(100):
            result = alias.sample()
            self.assertIn(result, items)
    
    def test_sample_n(self):
        """Test sampling multiple items."""
        items = ['a', 'b', 'c']
        weights = [1, 2, 3]
        
        alias = AliasMethod(items, weights)
        samples = alias.sample_n(100)
        
        self.assertEqual(len(samples), 100)
        for s in samples:
            self.assertIn(s, items)
    
    def test_distribution(self):
        """Test that alias method produces correct distribution."""
        items = ['a', 'b', 'c']
        weights = [1, 2, 3]
        
        alias = AliasMethod(items, weights)
        
        counter = Counter(alias.sample_n(10000))
        total = sum(counter.values())
        
        self.assertAlmostEqual(counter['a'] / total, 1/6, delta=0.02)
        self.assertAlmostEqual(counter['b'] / total, 2/6, delta=0.02)
        self.assertAlmostEqual(counter['c'] / total, 3/6, delta=0.02)
    
    def test_uniform_weights(self):
        """Test with uniform weights."""
        items = ['a', 'b', 'c', 'd']
        weights = [1, 1, 1, 1]
        
        alias = AliasMethod(items, weights)
        
        counter = Counter(alias.sample_n(10000))
        
        # All should be approximately equal
        for item in items:
            self.assertAlmostEqual(counter[item] / 10000, 0.25, delta=0.02)
    
    def test_single_item(self):
        """Test with single item."""
        items = ['only']
        weights = [1]
        
        alias = AliasMethod(items, weights)
        
        for _ in range(10):
            self.assertEqual(alias.sample(), 'only')
    
    def test_properties(self):
        """Test property accessors."""
        items = ['a', 'b', 'c']
        weights = [1, 2, 3]
        
        alias = AliasMethod(items, weights)
        
        self.assertEqual(alias.items, items)
        self.assertEqual(len(alias.probabilities), 3)
        self.assertEqual(len(alias.aliases), 3)
    
    def test_reproducibility(self):
        """Test reproducibility with seeded random."""
        items = ['a', 'b', 'c', 'd']
        weights = [1, 2, 3, 4]
        
        alias1 = AliasMethod(items, weights)
        alias2 = AliasMethod(items, weights)
        
        rng1 = random.Random(42)
        rng2 = random.Random(42)
        
        results1 = [alias1.sample(rng1) for _ in range(20)]
        results2 = [alias2.sample(rng2) for _ in range(20)]
        
        self.assertEqual(results1, results2)


class TestWeightedReservoirSampler(unittest.TestCase):
    """Tests for WeightedReservoirSampler class."""
    
    def test_basic_reservoir(self):
        """Test basic reservoir sampling."""
        sampler = WeightedReservoirSampler(k=3)
        
        for item, weight in [('a', 1), ('b', 2), ('c', 3), ('d', 4)]:
            sampler.add(item, weight)
        
        sample = sampler.sample()
        self.assertEqual(len(sample), 3)
    
    def test_reservoir_size(self):
        """Test that reservoir respects size limit."""
        sampler = WeightedReservoirSampler(k=2)
        
        for i in range(100):
            sampler.add(f'item_{i}', 1)
        
        sample = sampler.sample()
        self.assertEqual(len(sample), 2)
    
    def test_zero_weights(self):
        """Test that zero weights are skipped."""
        sampler = WeightedReservoirSampler(k=5)
        
        sampler.add('a', 1)
        sampler.add('b', 0)  # Should be skipped
        sampler.add('c', 2)
        
        sample = sampler.sample()
        self.assertIn('a', sample)
        self.assertIn('c', sample)
        self.assertNotIn('b', sample)
    
    def test_clear(self):
        """Test clearing reservoir."""
        sampler = WeightedReservoirSampler(k=3)
        
        for item, weight in [('a', 1), ('b', 2), ('c', 3)]:
            sampler.add(item, weight)
        
        self.assertEqual(sampler.size, 3)
        
        sampler.clear()
        self.assertEqual(sampler.size, 0)
    
    def test_capacity_property(self):
        """Test capacity property."""
        sampler = WeightedReservoirSampler(k=10)
        self.assertEqual(sampler.capacity, 10)


class TestWeightedShuffle(unittest.TestCase):
    """Tests for weighted_shuffle function."""
    
    def test_all_items_present(self):
        """Test that all items are present in shuffled result."""
        items = ['a', 'b', 'c', 'd']
        weights = [1, 2, 3, 4]
        
        shuffled = weighted_shuffle(items, weights)
        
        self.assertEqual(len(shuffled), 4)
        self.assertEqual(set(shuffled), set(items))
    
    def test_empty_list(self):
        """Test shuffling empty list."""
        result = weighted_shuffle([], [])
        self.assertEqual(result, [])
    
    def test_reproducibility(self):
        """Test reproducibility with seeded random."""
        items = ['a', 'b', 'c', 'd']
        weights = [1, 2, 3, 4]
        
        rng1 = random.Random(42)
        rng2 = random.Random(42)
        
        result1 = weighted_shuffle(items, weights, random_instance=rng1)
        result2 = weighted_shuffle(items, weights, random_instance=rng2)
        
        self.assertEqual(result1, result2)


class TestWeightUtilities(unittest.TestCase):
    """Tests for weight utility functions."""
    
    def test_normalize_weights(self):
        """Test weight normalization."""
        weights = [1, 2, 3]
        normalized = normalize_weights(weights)
        
        self.assertAlmostEqual(sum(normalized), 1.0)
        self.assertAlmostEqual(normalized[0], 1/6)
        self.assertAlmostEqual(normalized[1], 2/6)
        self.assertAlmostEqual(normalized[2], 3/6)
    
    def test_normalize_zero_weights(self):
        """Test normalizing zero weights raises error."""
        with self.assertRaises(TotalWeightZeroError):
            normalize_weights([0, 0, 0])
    
    def test_cumulative_weights(self):
        """Test cumulative weight calculation."""
        weights = [1, 2, 3, 4]
        cum = cumulative_weights(weights)
        
        self.assertEqual(cum, [1, 3, 6, 10])
    
    def test_probability_from_cumulative(self):
        """Test probability lookup from cumulative weights."""
        cum = [1, 3, 6, 10]
        
        self.assertEqual(probability_from_cumulative(cum, 0), 0)
        self.assertEqual(probability_from_cumulative(cum, 0.5), 0)
        self.assertEqual(probability_from_cumulative(cum, 1), 1)
        self.assertEqual(probability_from_cumulative(cum, 3), 2)
        self.assertEqual(probability_from_cumulative(cum, 9), 3)
    
    def test_softmax_weights(self):
        """Test softmax weight calculation."""
        values = [1, 2, 3]
        probs = softmax_weights(values)
        
        self.assertAlmostEqual(sum(probs), 1.0)
        # Higher values should have higher probabilities
        self.assertLess(probs[0], probs[1])
        self.assertLess(probs[1], probs[2])
    
    def test_softmax_equal_values(self):
        """Test softmax with equal values."""
        values = [1, 1, 1]
        probs = softmax_weights(values)
        
        self.assertAlmostEqual(sum(probs), 1.0)
        # All should be equal
        self.assertAlmostEqual(probs[0], probs[1])
        self.assertAlmostEqual(probs[1], probs[2])
    
    def test_softmax_temperature(self):
        """Test softmax temperature effect."""
        values = [1, 2, 10]
        
        # Low temperature = more peaked
        probs_low = softmax_weights(values, temperature=0.1)
        # High temperature = more uniform
        probs_high = softmax_weights(values, temperature=10)
        
        # Low temp should have more extreme distribution
        self.assertGreater(probs_low[2] - probs_low[0], probs_high[2] - probs_high[0])
    
    def test_softmax_invalid_temperature(self):
        """Test that invalid temperature raises error."""
        with self.assertRaises(ValueError):
            softmax_weights([1, 2, 3], temperature=0)
        
        with self.assertRaises(ValueError):
            softmax_weights([1, 2, 3], temperature=-1)
    
    def test_exponential_weights(self):
        """Test exponential weight transformation."""
        weights = [1, 4, 9]
        exp_weights = exponential_weights(weights, decay=0.5)
        
        # sqrt(1) = 1, sqrt(4) = 2, sqrt(9) = 3
        self.assertAlmostEqual(exp_weights[0], 1.0)
        self.assertAlmostEqual(exp_weights[1], 2.0)
        self.assertAlmostEqual(exp_weights[2], 3.0)


class TestDistributionFunctions(unittest.TestCase):
    """Tests for distribution-related functions."""
    
    def test_inverse_transform_sample(self):
        """Test inverse transform sampling."""
        cdf = [0.25, 0.5, 0.75, 1.0]
        
        counter = Counter()
        for _ in range(10000):
            idx = inverse_transform_sample(cdf)
            counter[idx] += 1
        
        # Each should have approximately 25%
        for i in range(4):
            self.assertAlmostEqual(counter[i] / 10000, 0.25, delta=0.02)
    
    def test_inverse_transform_sample_with_values(self):
        """Test inverse transform with explicit values."""
        cdf = [0.25, 0.5, 0.75, 1.0]
        values = ['a', 'b', 'c', 'd']
        
        for _ in range(100):
            result = inverse_transform_sample(cdf, values)
            self.assertIn(result, values)
    
    def test_rejection_sample(self):
        """Test rejection sampling."""
        # Sample from uniform [0, 1] with acceptance proportional to x
        rng = random.Random(42)
        
        proposal = lambda: rng.random()
        acceptance = lambda x: x  # Linear acceptance
        
        samples = rejection_sample(proposal, acceptance, 100, random_instance=rng)
        
        self.assertEqual(len(samples), 100)
        
        # Mean should be higher than 0.5 (acceptance favors higher values)
        mean = sum(samples) / len(samples)
        self.assertGreater(mean, 0.5)
    
    def test_rejection_sample_max_iterations(self):
        """Test rejection sample with low acceptance."""
        # Very low acceptance rate
        proposal = lambda: 0.999  # Always proposes 0.999
        acceptance = lambda x: 0.001  # Very low acceptance
        
        samples = rejection_sample(proposal, acceptance, 10, max_iterations=100)
        
        # May not get all samples due to max iterations
        self.assertLessEqual(len(samples), 10)


class TestProbabilityUtilities(unittest.TestCase):
    """Tests for probability utility functions."""
    
    def test_weight_to_probability(self):
        """Test weight to probability conversion."""
        items = [('a', 1), ('b', 2), ('c', 3)]
        probs = weight_to_probability(items)
        
        self.assertAlmostEqual(probs['a'], 1/6)
        self.assertAlmostEqual(probs['b'], 2/6)
        self.assertAlmostEqual(probs['c'], 3/6)
    
    def test_probability_to_weight(self):
        """Test probability to weight conversion."""
        probs = [0.2, 0.3, 0.5]
        weights = probability_to_weight(probs, scale=100)
        
        self.assertEqual(weights, [20.0, 30.0, 50.0])
    
    def test_kl_divergence_identical(self):
        """Test KL divergence of identical distributions."""
        p = [0.25, 0.25, 0.25, 0.25]
        q = [0.25, 0.25, 0.25, 0.25]
        
        self.assertEqual(kl_divergence(p, q), 0.0)
    
    def test_kl_divergence_different(self):
        """Test KL divergence of different distributions."""
        p = [1.0, 0.0]  # Deterministic
        q = [0.5, 0.5]  # Uniform
        
        # KL should be positive
        self.assertGreater(kl_divergence(p, q), 0)
    
    def test_kl_divergence_infinite(self):
        """Test KL divergence when q has zero where p doesn't."""
        p = [0.5, 0.5]
        q = [1.0, 0.0]  # Zero where p has probability
        
        self.assertEqual(kl_divergence(p, q), float('inf'))
    
    def test_entropy_uniform(self):
        """Test entropy of uniform distribution."""
        # Uniform distribution over n outcomes has entropy log2(n)
        probs = [0.25, 0.25, 0.25, 0.25]
        
        self.assertAlmostEqual(entropy(probs), 2.0)  # log2(4) = 2
    
    def test_entropy_deterministic(self):
        """Test entropy of deterministic distribution."""
        probs = [1.0, 0.0, 0.0, 0.0]
        
        self.assertEqual(entropy(probs), 0.0)
    
    def test_effective_size_uniform(self):
        """Test effective size with uniform weights."""
        weights = [1, 1, 1, 1]
        
        self.assertEqual(effective_size(weights), 4.0)
    
    def test_effective_size_concentrated(self):
        """Test effective size with concentrated weights."""
        weights = [100, 1, 1, 1]
        
        # ESS should be less than 4 but more than 1
        ess = effective_size(weights)
        self.assertGreater(ess, 1)
        self.assertLess(ess, 4)
    
    def test_effective_size_zero(self):
        """Test effective size with zero weights."""
        weights = [0, 0, 0]
        
        self.assertEqual(effective_size(weights), 0.0)


class TestBatchOperations(unittest.TestCase):
    """Tests for batch operations."""
    
    def test_batch_weighted_choice(self):
        """Test batch weighted choice."""
        items = ['a', 'b', 'c']
        weights = [1, 2, 3]
        
        samples = batch_weighted_choice(items, weights, 1000)
        
        self.assertEqual(len(samples), 1000)
        
        counter = Counter(samples)
        total = sum(counter.values())
        
        # Check distribution
        self.assertAlmostEqual(counter['a'] / total, 1/6, delta=0.03)
        self.assertAlmostEqual(counter['b'] / total, 2/6, delta=0.03)
        self.assertAlmostEqual(counter['c'] / total, 3/6, delta=0.03)
    
    def test_batch_weighted_choice_zero(self):
        """Test batch with zero count."""
        items = ['a', 'b']
        weights = [1, 1]
        
        samples = batch_weighted_choice(items, weights, 0)
        self.assertEqual(samples, [])


class TestConvenienceFunctions(unittest.TestCase):
    """Tests for convenience functions."""
    
    def test_weighted_coin_flip(self):
        """Test weighted coin flip."""
        rng = random.Random(42)
        
        # Test probability 1 (always True)
        for _ in range(10):
            self.assertTrue(weighted_coin_flip(1.0, random_instance=rng))
        
        # Test probability 0 (always False)
        for _ in range(10):
            self.assertFalse(weighted_coin_flip(0.0, random_instance=rng))
        
        # Test probability 0.5 (roughly half True)
        counter = Counter()
        for _ in range(1000):
            counter[weighted_coin_flip(0.5, random_instance=rng)] += 1
        
        self.assertAlmostEqual(counter[True] / 1000, 0.5, delta=0.05)
    
    def test_weighted_coin_flip_invalid(self):
        """Test weighted coin with invalid probability."""
        with self.assertRaises(ValueError):
            weighted_coin_flip(-0.1)
        
        with self.assertRaises(ValueError):
            weighted_coin_flip(1.1)
    
    def test_weighted_random_range(self):
        """Test weighted random range selection."""
        weights = [1, 2, 3, 4]
        
        counter = Counter()
        for _ in range(10000):
            result = weighted_random_range(0, 4, weights)
            counter[result] += 1
        
        total = sum(counter.values())
        
        # Check distribution
        self.assertAlmostEqual(counter[0] / total, 1/10, delta=0.02)
        self.assertAlmostEqual(counter[1] / total, 2/10, delta=0.02)
        self.assertAlmostEqual(counter[2] / total, 3/10, delta=0.02)
        self.assertAlmostEqual(counter[3] / total, 4/10, delta=0.02)


class TestEdgeCases(unittest.TestCase):
    """Tests for edge cases."""
    
    def test_very_small_weights(self):
        """Test with very small weights."""
        items = ['a', 'b', 'c']
        weights = [1e-10, 1e-10, 1e-10]
        
        # Should still work
        for _ in range(10):
            result = weighted_choice(items, weights)
            self.assertIn(result, items)
    
    def test_very_large_weights(self):
        """Test with very large weights."""
        items = ['a', 'b', 'c']
        weights = [1e10, 1e10, 1e10]
        
        for _ in range(10):
            result = weighted_choice(items, weights)
            self.assertIn(result, items)
    
    def test_mixed_small_large_weights(self):
        """Test with mixed small and large weights."""
        items = ['a', 'b', 'c']
        weights = [1e-10, 1.0, 1e10]
        
        # 'c' should almost always be selected
        counter = Counter()
        for _ in range(100):
            counter[weighted_choice(items, weights)] += 1
        
        self.assertGreater(counter['c'], 90)  # Should be selected most times
    
    def test_float_weights(self):
        """Test with float weights."""
        items = ['a', 'b', 'c']
        weights = [0.1, 0.3, 0.6]
        
        for _ in range(10):
            result = weighted_choice(items, weights)
            self.assertIn(result, items)


class TestAliasMethodEdgeCases(unittest.TestCase):
    """Tests for AliasMethod edge cases."""
    
    def test_uniform_weights(self):
        """Test alias with uniform weights."""
        items = list(range(10))
        weights = [1] * 10
        
        alias = AliasMethod(items, weights)
        
        counter = Counter(alias.sample_n(10000))
        
        # Each should have roughly 10%
        for item in items:
            self.assertAlmostEqual(counter[item] / 10000, 0.1, delta=0.02)
    
    def test_extreme_weight_ratio(self):
        """Test alias with extreme weight ratio."""
        items = ['rare', 'common']
        weights = [1, 999]
        
        alias = AliasMethod(items, weights)
        
        counter = Counter(alias.sample_n(10000))
        
        self.assertGreater(counter['common'], 9000)
        self.assertLess(counter['rare'], 100)


def run_tests():
    """Run all tests."""
    unittest.main(verbosity=2)


if __name__ == '__main__':
    run_tests()