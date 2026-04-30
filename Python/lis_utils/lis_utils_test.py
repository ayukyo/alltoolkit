"""
Tests for LIS (Longest Increasing Subsequence) Utils
"""

import unittest
from mod import (
    lis_length,
    lis_sequence,
    lis_with_indices,
    lds_length,
    lds_sequence,
    lnds_length,
    lnds_sequence,
    count_lis,
    lis_all_sequences,
    lis_on_sequence,
    minimum_removals_for_sorted,
    patience_sort,
    find_lis,
)


class TestLISLength(unittest.TestCase):
    """Tests for lis_length function."""
    
    def test_empty_array(self):
        self.assertEqual(lis_length([]), 0)
    
    def test_single_element(self):
        self.assertEqual(lis_length([5]), 1)
    
    def test_increasing_sequence(self):
        self.assertEqual(lis_length([1, 2, 3, 4, 5]), 5)
    
    def test_decreasing_sequence(self):
        self.assertEqual(lis_length([5, 4, 3, 2, 1]), 1)
    
    def test_mixed_sequence(self):
        self.assertEqual(lis_length([10, 9, 2, 5, 3, 7, 101, 18]), 4)
    
    def test_with_duplicates(self):
        self.assertEqual(lis_length([2, 2, 2, 2, 2]), 1)
    
    def test_negative_numbers(self):
        self.assertEqual(lis_length([-5, -3, -1, 0, 2]), 5)
    
    def test_example_1(self):
        self.assertEqual(lis_length([0, 1, 0, 3, 2, 3]), 4)
    
    def test_example_2(self):
        self.assertEqual(lis_length([7, 7, 7, 7, 7, 7, 7]), 1)


class TestLISSequence(unittest.TestCase):
    """Tests for lis_sequence function."""
    
    def test_empty_array(self):
        self.assertEqual(lis_sequence([]), [])
    
    def test_single_element(self):
        self.assertEqual(lis_sequence([5]), [5])
    
    def test_increasing_sequence(self):
        self.assertEqual(lis_sequence([1, 2, 3, 4, 5]), [1, 2, 3, 4, 5])
    
    def test_decreasing_sequence(self):
        result = lis_sequence([5, 4, 3, 2, 1])
        self.assertEqual(len(result), 1)
        self.assertIn(result[0], [5, 4, 3, 2, 1])
    
    def test_mixed_sequence(self):
        result = lis_sequence([10, 9, 2, 5, 3, 7, 101, 18])
        self.assertEqual(len(result), 4)
        # Verify it's a valid LIS
        self._verify_increasing(result)
        self._verify_subsequence([10, 9, 2, 5, 3, 7, 101, 18], result)
    
    def test_with_duplicates(self):
        result = lis_sequence([2, 2, 2, 2, 2])
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0], 2)
    
    def test_negative_numbers(self):
        result = lis_sequence([-5, -3, -1, 0, 2])
        self.assertEqual(result, [-5, -3, -1, 0, 2])
    
    def _verify_increasing(self, arr):
        for i in range(1, len(arr)):
            self.assertLess(arr[i-1], arr[i])
    
    def _verify_subsequence(self, original, subseq):
        idx = 0
        for val in subseq:
            while idx < len(original) and original[idx] != val:
                idx += 1
            self.assertLess(idx, len(original))
            idx += 1


class TestLISWithIndices(unittest.TestCase):
    """Tests for lis_with_indices function."""
    
    def test_empty_array(self):
        seq, idx = lis_with_indices([])
        self.assertEqual(seq, [])
        self.assertEqual(idx, [])
    
    def test_single_element(self):
        seq, idx = lis_with_indices([5])
        self.assertEqual(seq, [5])
        self.assertEqual(idx, [0])
    
    def test_increasing_sequence(self):
        seq, idx = lis_with_indices([1, 2, 3, 4, 5])
        self.assertEqual(seq, [1, 2, 3, 4, 5])
        self.assertEqual(idx, [0, 1, 2, 3, 4])
    
    def test_mixed_sequence(self):
        arr = [10, 9, 2, 5, 3, 7, 101, 18]
        seq, idx = lis_with_indices(arr)
        self.assertEqual(len(seq), 4)
        self.assertEqual(len(idx), 4)
        # Verify indices match
        for i, (s, ix) in enumerate(zip(seq, idx)):
            self.assertEqual(arr[ix], s)


class TestLDS(unittest.TestCase):
    """Tests for Longest Decreasing Subsequence functions."""
    
    def test_lds_length_empty(self):
        self.assertEqual(lds_length([]), 0)
    
    def test_lds_length_single(self):
        self.assertEqual(lds_length([5]), 1)
    
    def test_lds_length_decreasing(self):
        self.assertEqual(lds_length([5, 4, 3, 2, 1]), 5)
    
    def test_lds_length_increasing(self):
        self.assertEqual(lds_length([1, 2, 3, 4, 5]), 1)
    
    def test_lds_length_mixed(self):
        self.assertEqual(lds_length([10, 9, 2, 5, 3, 7, 101, 18]), 4)
    
    def test_lds_sequence_decreasing(self):
        self.assertEqual(lds_sequence([5, 4, 3, 2, 1]), [5, 4, 3, 2, 1])
    
    def test_lds_sequence_valid(self):
        arr = [10, 9, 2, 5, 3, 7, 101, 18]
        result = lds_sequence(arr)
        # Verify decreasing
        for i in range(1, len(result)):
            self.assertGreater(result[i-1], result[i])


class TestLNDS(unittest.TestCase):
    """Tests for Longest Non-Decreasing Subsequence functions."""
    
    def test_lnds_length_empty(self):
        self.assertEqual(lnds_length([]), 0)
    
    def test_lnds_length_with_duplicates(self):
        # Non-decreasing allows equal elements
        self.assertEqual(lnds_length([1, 1, 1, 1]), 4)
    
    def test_lnds_length_mixed(self):
        self.assertEqual(lnds_length([1, 3, 5, 4, 7, 7, 2]), 5)
    
    def test_lnds_sequence_with_duplicates(self):
        result = lnds_sequence([1, 1, 1, 1])
        self.assertEqual(result, [1, 1, 1, 1])
    
    def test_lnds_sequence_mixed(self):
        result = lnds_sequence([1, 3, 5, 4, 7, 7, 2])
        self.assertEqual(len(result), 5)
        # Verify non-decreasing
        for i in range(1, len(result)):
            self.assertLessEqual(result[i-1], result[i])


class TestCountLIS(unittest.TestCase):
    """Tests for count_lis function."""
    
    def test_empty_array(self):
        self.assertEqual(count_lis([]), 0)
    
    def test_single_element(self):
        self.assertEqual(count_lis([5]), 1)
    
    def test_increasing_sequence(self):
        self.assertEqual(count_lis([1, 2, 3, 4, 5]), 1)
    
    def test_multiple_lis(self):
        # [1, 3, 5, 7] and [1, 3, 4, 7]
        self.assertEqual(count_lis([1, 3, 5, 4, 7]), 2)
    
    def test_all_duplicates(self):
        # Each position can be an LIS of length 1, so 5 different LIS
        self.assertEqual(count_lis([2, 2, 2, 2, 2]), 5)
    
    def test_multiple_paths(self):
        # LIS length 4: sequences [1,2,3,7], [1,2,4,7], [1,2,5,7]
        # Note: actually 3 distinct LIS of length 4
        self.assertEqual(count_lis([1, 2, 4, 3, 5, 4, 7]), 3)


class TestLISAllSequences(unittest.TestCase):
    """Tests for lis_all_sequences function."""
    
    def test_empty_array(self):
        self.assertEqual(lis_all_sequences([]), [[]])
    
    def test_single_element(self):
        self.assertEqual(lis_all_sequences([5]), [[5]])
    
    def test_increasing_sequence(self):
        self.assertEqual(lis_all_sequences([1, 2, 3, 4, 5]), [[1, 2, 3, 4, 5]])
    
    def test_multiple_lis(self):
        result = lis_all_sequences([1, 3, 5, 4, 7])
        self.assertEqual(len(result), 2)
        self.assertIn([1, 3, 5, 7], result)
        self.assertIn([1, 3, 4, 7], result)
    
    def test_all_sequences_valid(self):
        arr = [1, 3, 5, 4, 7]
        for seq in lis_all_sequences(arr):
            # Verify increasing
            for i in range(1, len(seq)):
                self.assertLess(seq[i-1], seq[i])
            # Verify it's a subsequence
            idx = 0
            for val in seq:
                while idx < len(arr) and arr[idx] != val:
                    idx += 1
                self.assertLess(idx, len(arr))
                idx += 1


class TestLISOnSequence(unittest.TestCase):
    """Tests for lis_on_sequence function."""
    
    def test_empty(self):
        self.assertEqual(lis_on_sequence([]), [])
    
    def test_dict_objects(self):
        data = [{'val': 1}, {'val': 3}, {'val': 2}, {'val': 5}]
        result = lis_on_sequence(data, key=lambda x: x['val'])
        self.assertEqual(len(result), 3)
        # Verify increasing by key
        for i in range(1, len(result)):
            self.assertLess(result[i-1]['val'], result[i]['val'])
    
    def test_tuple_objects(self):
        data = [(1, 'a'), (3, 'b'), (2, 'c'), (4, 'd')]
        result = lis_on_sequence(data, key=lambda x: x[0])
        self.assertEqual(len(result), 3)
    
    def test_custom_class(self):
        class Item:
            def __init__(self, value):
                self.value = value
        
        # LIS length for [5, 2, 8, 6] is 2 (e.g., [2, 8] or [5, 8])
        data = [Item(5), Item(2), Item(8), Item(6)]
        result = lis_on_sequence(data, key=lambda x: x.value)
        self.assertEqual(len(result), 2)


class TestMinimumRemovals(unittest.TestCase):
    """Tests for minimum_removals_for_sorted function."""
    
    def test_empty(self):
        self.assertEqual(minimum_removals_for_sorted([]), 0)
    
    def test_already_sorted(self):
        self.assertEqual(minimum_removals_for_sorted([1, 2, 3, 4, 5]), 0)
    
    def test_reverse_sorted(self):
        self.assertEqual(minimum_removals_for_sorted([5, 4, 3, 2, 1]), 4)
    
    def test_mixed(self):
        # LIS length is 4, so remove 8 - 4 = 4
        self.assertEqual(minimum_removals_for_sorted([5, 2, 8, 6, 3, 6, 9, 5]), 4)


class TestPatienceSort(unittest.TestCase):
    """Tests for patience_sort function."""
    
    def test_empty(self):
        self.assertEqual(patience_sort([]), [])
    
    def test_single_element(self):
        self.assertEqual(patience_sort([5]), [5])
    
    def test_sorted(self):
        self.assertEqual(patience_sort([1, 2, 3, 4, 5]), [1, 2, 3, 4, 5])
    
    def test_reverse_sorted(self):
        self.assertEqual(patience_sort([5, 4, 3, 2, 1]), [1, 2, 3, 4, 5])
    
    def test_mixed(self):
        self.assertEqual(patience_sort([5, 2, 8, 6, 3, 6, 9, 5]), 
                        [2, 3, 5, 5, 6, 6, 8, 9])
    
    def test_with_duplicates(self):
        self.assertEqual(patience_sort([3, 1, 2, 1, 3]), [1, 1, 2, 3, 3])


class TestFindLIS(unittest.TestCase):
    """Tests for convenience find_lis function."""
    
    def test_mode_length(self):
        self.assertEqual(find_lis([10, 9, 2, 5, 3, 7, 101, 18], mode="length"), 4)
    
    def test_mode_sequence(self):
        result = find_lis([10, 9, 2, 5, 3, 7, 101, 18], mode="sequence")
        self.assertEqual(len(result), 4)
    
    def test_mode_indices(self):
        seq, idx = find_lis([10, 9, 2, 5, 3, 7, 101, 18], mode="indices")
        self.assertEqual(len(seq), 4)
        self.assertEqual(len(idx), 4)
    
    def test_mode_count(self):
        self.assertEqual(find_lis([1, 3, 5, 4, 7], mode="count"), 2)
    
    def test_invalid_mode(self):
        with self.assertRaises(ValueError):
            find_lis([1, 2, 3], mode="invalid")


if __name__ == "__main__":
    unittest.main()