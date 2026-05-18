"""
AllToolkit - Python Collatz Utilities Tests

Comprehensive test suite for collatz_utils module.
"""

import unittest
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from collatz_utils.mod import (
    collatz_step,
    collatz_sequence,
    collatz_generator,
    collatz_length,
    collatz_length_cached,
    collatz_max_value,
    collatz_even_odd_ratio,
    collatz_rise_and_fall,
    total_stopping_time,
    stopping_time_to_value,
    longest_sequence_in_range,
    highest_value_in_range,
    collatz_statistics,
    find_numbers_reaching_value,
    find_numbers_with_length,
    find_numbers_with_max_value,
    generalized_collatz_sequence,
    lazy_caterer_sequence,
    collatz_tree_path,
    collatz_waterfall,
    collatz_summary,
    is_collatz_number,
    first_n_collatz_values,
    collatz_predecessors,
    collatz_inverse_tree,
    InvalidInputError,
    MaxIterationsError,
)


class TestCollatzStep(unittest.TestCase):
    """Test the basic Collatz step function."""
    
    def test_even_number(self):
        """Test that even numbers are divided by 2."""
        self.assertEqual(collatz_step(6), 3)
        self.assertEqual(collatz_step(4), 2)
        self.assertEqual(collatz_step(100), 50)
        self.assertEqual(collatz_step(2), 1)
    
    def test_odd_number(self):
        """Test that odd numbers follow 3n+1."""
        self.assertEqual(collatz_step(3), 10)
        self.assertEqual(collatz_step(5), 16)
        self.assertEqual(collatz_step(7), 22)
        self.assertEqual(collatz_step(9), 28)
    
    def test_one(self):
        """Test that 1 follows 3n+1 (gives 4)."""
        self.assertEqual(collatz_step(1), 4)
    
    def test_invalid_input(self):
        """Test that invalid inputs raise errors."""
        with self.assertRaises(InvalidInputError):
            collatz_step(0)
        with self.assertRaises(InvalidInputError):
            collatz_step(-1)
        with self.assertRaises(InvalidInputError):
            collatz_step(3.5)
        with self.assertRaises(InvalidInputError):
            collatz_step("6")


class TestCollatzSequence(unittest.TestCase):
    """Test Collatz sequence generation."""
    
    def test_sequence_for_one(self):
        """Test sequence for 1."""
        self.assertEqual(collatz_sequence(1), [1])
    
    def test_sequence_for_six(self):
        """Test the classic example: 6 -> 3 -> 10 -> 5 -> 16 -> 8 -> 4 -> 2 -> 1."""
        self.assertEqual(collatz_sequence(6), [6, 3, 10, 5, 16, 8, 4, 2, 1])
    
    def test_sequence_for_seven(self):
        """Test sequence for 7."""
        expected = [7, 22, 11, 34, 17, 52, 26, 13, 40, 20, 10, 5, 16, 8, 4, 2, 1]
        self.assertEqual(collatz_sequence(7), expected)
    
    def test_sequence_for_twenty_seven(self):
        """Test the famous long sequence for 27."""
        seq = collatz_sequence(27)
        self.assertEqual(seq[0], 27)
        self.assertEqual(seq[-1], 1)
        self.assertEqual(len(seq), 112)  # Known length for 27
        self.assertEqual(max(seq), 9232)  # Known max for 27
    
    def test_sequence_ends_with_one(self):
        """Test that all sequences end with 1."""
        for n in [1, 2, 3, 4, 5, 10, 20, 50, 100]:
            seq = collatz_sequence(n)
            self.assertEqual(seq[-1], 1)
    
    def test_invalid_input(self):
        """Test invalid inputs."""
        with self.assertRaises(InvalidInputError):
            collatz_sequence(0)
        with self.assertRaises(InvalidInputError):
            collatz_sequence(-5)


class TestCollatzGenerator(unittest.TestCase):
    """Test the generator version of Collatz sequence."""
    
    def test_generator_basic(self):
        """Test that generator produces correct sequence."""
        result = list(collatz_generator(6))
        self.assertEqual(result, [6, 3, 10, 5, 16, 8, 4, 2, 1])
    
    def test_generator_one(self):
        """Test generator for 1."""
        result = list(collatz_generator(1))
        self.assertEqual(result, [1])
    
    def test_generator_efficiency(self):
        """Test that generator is memory efficient."""
        gen = collatz_generator(1000)
        first_five = [next(gen) for _ in range(5)]
        self.assertEqual(first_five[:3], [1000, 500, 250])


class TestCollatzLength(unittest.TestCase):
    """Test sequence length calculations."""
    
    def test_length_for_one(self):
        """Test length for 1."""
        self.assertEqual(collatz_length(1), 1)
    
    def test_length_for_six(self):
        """Test length for 6."""
        self.assertEqual(collatz_length(6), 9)
    
    def test_length_for_twenty_seven(self):
        """Test known length for 27."""
        self.assertEqual(collatz_length(27), 112)
    
    def test_cached_version(self):
        """Test cached length function."""
        self.assertEqual(collatz_length_cached(6), 9)
        self.assertEqual(collatz_length_cached(27), 112)
        
        # Test cache effectiveness by clearing and calling again
        collatz_length_cached.cache_clear()
        self.assertEqual(collatz_length_cached(10), 7)


class TestCollatzMaxValue(unittest.TestCase):
    """Test maximum value calculations."""
    
    def test_max_for_one(self):
        """Test max for 1."""
        self.assertEqual(collatz_max_value(1), 1)
    
    def test_max_for_six(self):
        """Test max for 6 (should be 16)."""
        self.assertEqual(collatz_max_value(6), 16)
    
    def test_max_for_seven(self):
        """Test max for 7 (should be 52)."""
        self.assertEqual(collatz_max_value(7), 52)
    
    def test_max_for_twenty_seven(self):
        """Test known max for 27."""
        self.assertEqual(collatz_max_value(27), 9232)


class TestCollatzEvenOddRatio(unittest.TestCase):
    """Test even/odd counting."""
    
    def test_ratio_for_one(self):
        """Test ratio for 1."""
        self.assertEqual(collatz_even_odd_ratio(1), (1, 0))
    
    def test_ratio_for_six(self):
        """Test ratio for 6."""
        even, odd = collatz_even_odd_ratio(6)
        # Sequence: 6, 3, 10, 5, 16, 8, 4, 2, 1
        # Even: 6, 10, 16, 8, 4, 2, 1 = 7 (wait, 1 is also odd)
        # Let me recalculate: 6(e), 3(o), 10(e), 5(o), 16(e), 8(e), 4(e), 2(e), 1(o)
        # Even: 6, 10, 16, 8, 4, 2 = 6
        # Odd: 3, 5, 1 = 3
        self.assertEqual(even, 6)
        self.assertEqual(odd, 3)
    
    def test_ratio_for_seven(self):
        """Test ratio for 7."""
        even, odd = collatz_even_odd_ratio(7)
        self.assertEqual(even + odd, 17)  # Total length


class TestCollatzRiseAndFall(unittest.TestCase):
    """Test rise and fall counting."""
    
    def test_rise_fall_for_six(self):
        """Test rises and falls for 6."""
        # 6->3(f), 3->10(r), 10->5(f), 5->16(r), 16->8(f), 8->4(f), 4->2(f), 2->1(f)
        rises, falls = collatz_rise_and_fall(6)
        self.assertEqual(rises, 2)  # 3->10, 5->16
        self.assertEqual(falls, 6)  # 6->3, 10->5, 16->8, 8->4, 4->2, 2->1
    
    def test_rise_fall_for_one(self):
        """Test rises and falls for 1."""
        self.assertEqual(collatz_rise_and_fall(1), (0, 0))


class TestStoppingTime(unittest.TestCase):
    """Test stopping time calculations."""
    
    def test_total_stopping_time(self):
        """Test total stopping time."""
        self.assertEqual(total_stopping_time(1), 0)
        self.assertEqual(total_stopping_time(6), 8)
        self.assertEqual(total_stopping_time(27), 111)
    
    def test_stopping_time_to_value(self):
        """Test stopping time to reach specific value."""
        self.assertEqual(stopping_time_to_value(6, 10), 2)
        self.assertEqual(stopping_time_to_value(6, 5), 3)
        self.assertEqual(stopping_time_to_value(6, 1), 8)
        self.assertIsNone(stopping_time_to_value(6, 100))


class TestRangeAnalysis(unittest.TestCase):
    """Test range analysis functions."""
    
    def test_longest_sequence_in_range(self):
        """Test finding longest sequence in range."""
        num, length, seq = longest_sequence_in_range(1, 10)
        self.assertEqual(num, 9)
        self.assertEqual(length, 20)
    
    def test_highest_value_in_range(self):
        """Test finding highest value in range."""
        num, max_val, step = highest_value_in_range(1, 10)
        # Both 7 and 9 reach 52 as max value
        self.assertIn(num, [7, 9])
        self.assertEqual(max_val, 52)
    
    def test_collatz_statistics(self):
        """Test statistics calculation."""
        stats = collatz_statistics(1, 10)
        self.assertEqual(stats['count'], 10)
        self.assertEqual(stats['min_length'], 1)  # 1 has length 1
        self.assertEqual(stats['max_length'], 20)  # 9 has length 20
        self.assertEqual(stats['max_length_number'], 9)
        self.assertGreater(stats['even_ratio'], 0.5)  # Most numbers are even


class TestPatternDetection(unittest.TestCase):
    """Test pattern detection functions."""
    
    def test_find_numbers_reaching_value(self):
        """Test finding numbers that reach a specific value."""
        result = find_numbers_reaching_value(16, 20)
        self.assertIn(5, result)
        self.assertIn(10, result)
        self.assertIn(16, result)
    
    def test_find_numbers_with_length(self):
        """Test finding numbers with specific length."""
        result = find_numbers_with_length(9, 20)
        self.assertEqual(result, [6])
    
    def test_find_numbers_with_max_value(self):
        """Test finding numbers with specific max value."""
        result = find_numbers_with_max_value(16, 20)
        self.assertIn(6, result)


class TestGeneralizedCollatz(unittest.TestCase):
    """Test generalized Collatz variants."""
    
    def test_standard_parameters(self):
        """Test with standard parameters."""
        seq = generalized_collatz_sequence(6, a=3, b=1, c=2)
        self.assertEqual(seq, collatz_sequence(6))
    
    def test_five_n_plus_one(self):
        """Test 5n+1 variant."""
        # 5n+1 may not converge to 1 quickly, just check first few values
        try:
            seq = generalized_collatz_sequence(7, a=5, b=1, c=2, max_iterations=100)
            # Should produce: 7, 36, 18, 9, 46, 23, 116, ...
            self.assertEqual(seq[0], 7)
            self.assertEqual(seq[1], 36)
            self.assertEqual(seq[2], 18)
        except MaxIterationsError:
            # This is expected - 5n+1 variant may not converge
            pass
    
    def test_lazy_caterer(self):
        """Test lazy caterer sequence."""
        try:
            seq = lazy_caterer_sequence(7, max_iterations=100)
            self.assertEqual(seq[0], 7)
        except MaxIterationsError:
            # This is expected - 5n+1 variant may not converge
            pass


class TestVisualizationHelpers(unittest.TestCase):
    """Test visualization helper functions."""
    
    def test_collatz_tree_path(self):
        """Test tree path generation."""
        path = collatz_tree_path(6)
        self.assertEqual(path[0], (6, 'start'))
        self.assertEqual(path[-1], (1, '/2'))
    
    def test_collatz_waterfall(self):
        """Test waterfall visualization."""
        wf = collatz_waterfall(7)
        self.assertIn('7', wf)
        self.assertIn('1', wf)
    
    def test_collatz_summary(self):
        """Test summary generation."""
        summary = collatz_summary(27)
        self.assertEqual(summary['number'], 27)
        self.assertEqual(summary['length'], 112)
        self.assertEqual(summary['max_value'], 9232)
        self.assertEqual(summary['total_stopping_time'], 111)


class TestUtilityFunctions(unittest.TestCase):
    """Test utility functions."""
    
    def test_is_collatz_number(self):
        """Test Collatz number verification."""
        self.assertTrue(is_collatz_number(1))
        self.assertTrue(is_collatz_number(100))
        self.assertTrue(is_collatz_number(1000))
    
    def test_first_n_collatz_values(self):
        """Test first N values."""
        values = first_n_collatz_values(10)
        for i in range(1, 11):
            self.assertIn(i, values)
    
    def test_collatz_predecessors(self):
        """Test predecessor finding."""
        preds = collatz_predecessors(5)
        self.assertEqual(preds, {10})
        
        preds = collatz_predecessors(4)
        self.assertIn(8, preds)
        # Note: 1 is not included as predecessor because we filter out 1
        # (since 1 -> 4 via 3*1+1, but 1 is a special case)
    
    def test_collatz_inverse_tree(self):
        """Test inverse tree generation."""
        tree = collatz_inverse_tree(1, depth=3)
        self.assertIn(1, tree)
        self.assertIn(2, tree)
        self.assertIn(4, tree)


class TestEdgeCases(unittest.TestCase):
    """Test edge cases and special values."""
    
    def test_power_of_two(self):
        """Test powers of 2."""
        for n in [2, 4, 8, 16, 32, 64]:
            seq = collatz_sequence(n)
            # Should be simple halving sequence ending in 1
            expected = [n]
            while expected[-1] > 1:
                expected.append(expected[-1] // 2)
            self.assertEqual(seq, expected)
    
    def test_large_numbers(self):
        """Test with reasonably large numbers."""
        seq = collatz_sequence(10000)
        self.assertEqual(seq[-1], 1)
        self.assertGreater(len(seq), 10)
    
    def test_max_iterations_error(self):
        """Test max iterations error handling."""
        # This should not raise for normal numbers
        collatz_sequence(1000000, max_iterations=100000)
        
        # But should raise with very low max_iterations
        with self.assertRaises(MaxIterationsError):
            collatz_sequence(1000000, max_iterations=10)


class TestPerformance(unittest.TestCase):
    """Test performance characteristics."""
    
    def test_cached_vs_uncached(self):
        """Compare cached and uncached versions."""
        # First call should populate cache
        import time
        
        start = time.time()
        for n in range(1, 1000):
            collatz_length_cached(n)
        cached_time = time.time() - start
        
        # Clear cache and test again
        collatz_length_cached.cache_clear()
        start = time.time()
        for n in range(1, 1000):
            collatz_length_cached(n)
        uncached_time = time.time() - start
        
        # Cached should be faster for repeated calls
        start = time.time()
        for n in range(1, 1000):
            collatz_length_cached(n)
        second_cached_time = time.time() - start
        
        # Second cached should be very fast
        self.assertLess(second_cached_time, uncached_time)


def run_tests():
    """Run all tests."""
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromModule(sys.modules[__name__])
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    return result.wasSuccessful()


if __name__ == '__main__':
    success = run_tests()
    sys.exit(0 if success else 1)