"""
Unit tests for LCS Utilities

Run with: python -m pytest lcs_utils_test.py -v
Or with: python lcs_utils_test.py
"""

import unittest
from mod import (
    lcs_length,
    lcs,
    lcs_all,
    lcs_diff,
    lcs_diff_unified,
    lcs_similarity,
    lcs_distance,
    lcs_of_multiple,
    shortest_common_supersequence,
    find_lcs_positions,
    is_subsequence,
    count_distinct_lcs,
    LCSEngine,
    text_similarity,
    line_similarity,
    word_similarity,
    line_diff,
)


class TestLCSLength(unittest.TestCase):
    """Tests for lcs_length function."""
    
    def test_basic(self):
        self.assertEqual(lcs_length("ABC", "ABC"), 3)
        self.assertEqual(lcs_length("ABC", "DEF"), 0)
        self.assertEqual(lcs_length("ABCBDAB", "BDCABA"), 4)
    
    def test_empty_sequences(self):
        self.assertEqual(lcs_length("", ""), 0)
        self.assertEqual(lcs_length("ABC", ""), 0)
        self.assertEqual(lcs_length("", "ABC"), 0)
    
    def test_single_element(self):
        self.assertEqual(lcs_length("A", "A"), 1)
        self.assertEqual(lcs_length("A", "B"), 0)
    
    def test_lists(self):
        self.assertEqual(lcs_length([1, 2, 3], [1, 2, 3]), 3)
        self.assertEqual(lcs_length([1, 2, 3], [2, 3, 4]), 2)
        self.assertEqual(lcs_length([1, 2, 3, 4], [2, 4, 3, 1]), 2)
    
    def test_longer_sequences(self):
        s1 = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        s2 = "ABCDEFGHIJLMNOPQRSTUVWXYZ"
        self.assertEqual(lcs_length(s1, s2), 25)


class TestLCS(unittest.TestCase):
    """Tests for lcs function."""
    
    def test_basic(self):
        result = lcs("ABC", "ABC")
        self.assertEqual(result, ['A', 'B', 'C'])
        
        result = lcs("ABCBDAB", "BDCABA")
        self.assertEqual(result, ['B', 'D', 'A', 'B'])
    
    def test_empty_sequences(self):
        self.assertEqual(lcs("", ""), [])
        self.assertEqual(lcs("ABC", ""), [])
        self.assertEqual(lcs("", "ABC"), [])
    
    def test_no_common(self):
        self.assertEqual(lcs("ABC", "DEF"), [])
    
    def test_lists(self):
        result = lcs([1, 2, 3, 2, 4], [2, 3, 4, 5])
        self.assertEqual(result, [2, 3, 4])
    
    def test_subsequence(self):
        result = lcs("ABC", "AXBYCZ")
        self.assertEqual(result, ['A', 'B', 'C'])
    
    def test_reverse(self):
        result = lcs("ABC", "CBA")
        # One of the LCS could be ['A'], ['B'], or ['C']
        self.assertEqual(len(result), 1)
        self.assertIn(result[0], ['A', 'B', 'C'])


class TestLCSAll(unittest.TestCase):
    """Tests for lcs_all function."""
    
    def test_basic(self):
        results = lcs_all("ABC", "ACB")
        # Should find both ['A', 'B'] and ['A', 'C']
        self.assertEqual(len(results), 2)
        self.assertIn(['A', 'B'], results)
        self.assertIn(['A', 'C'], results)
    
    def test_single_lcs(self):
        results = lcs_all("ABC", "ABC")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0], ['A', 'B', 'C'])
    
    def test_empty_sequences(self):
        results = lcs_all("", "")
        self.assertEqual(results, [[]])
        
        results = lcs_all("ABC", "DEF")
        self.assertEqual(results, [[]])
    
    def test_all_same(self):
        results = lcs_all("AAA", "AA")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0], ['A', 'A'])


class TestLCSDiff(unittest.TestCase):
    """Tests for lcs_diff function."""
    
    def test_identical(self):
        diff = lcs_diff("ABC", "ABC")
        expected = [('equal', 'A'), ('equal', 'B'), ('equal', 'C')]
        self.assertEqual(diff, expected)
    
    def test_insertion(self):
        diff = lcs_diff("AC", "ABC")
        expected = [
            ('equal', 'A'),
            ('insert', 'B'),
            ('equal', 'C')
        ]
        self.assertEqual(diff, expected)
    
    def test_deletion(self):
        diff = lcs_diff("ABC", "AC")
        expected = [
            ('equal', 'A'),
            ('delete', 'B'),
            ('equal', 'C')
        ]
        self.assertEqual(diff, expected)
    
    def test_empty_sequences(self):
        diff = lcs_diff("", "ABC")
        expected = [
            ('insert', 'A'),
            ('insert', 'B'),
            ('insert', 'C')
        ]
        self.assertEqual(diff, expected)
        
        diff = lcs_diff("ABC", "")
        expected = [
            ('delete', 'A'),
            ('delete', 'B'),
            ('delete', 'C')
        ]
        self.assertEqual(diff, expected)
    
    def test_replacement(self):
        diff = lcs_diff("ABC", "ADC")
        # B deleted, D inserted
        self.assertIn(('delete', 'B'), diff)
        self.assertIn(('insert', 'D'), diff)


class TestLCSDiffUnified(unittest.TestCase):
    """Tests for lcs_diff_unified function."""
    
    def test_basic(self):
        result = lcs_diff_unified("ABC", "ACD", name1="old.txt", name2="new.txt")
        self.assertIn("--- old.txt", result)
        self.assertIn("+++ new.txt", result)
        self.assertIn("-B", result)
        self.assertIn("+D", result)
    
    def test_identical(self):
        result = lcs_diff_unified("ABC", "ABC")
        self.assertIn("--- original", result)
        self.assertIn("+++ modified", result)
    
    def test_empty(self):
        result = lcs_diff_unified("", "ABC")
        self.assertIn("+++ modified", result)


class TestLCSSimilarity(unittest.TestCase):
    """Tests for lcs_similarity function."""
    
    def test_identical(self):
        self.assertEqual(lcs_similarity("ABC", "ABC"), 1.0)
    
    def test_no_common(self):
        self.assertEqual(lcs_similarity("ABC", "DEF"), 0.0)
    
    def test_partial(self):
        sim = lcs_similarity("ABC", "ADC")
        self.assertAlmostEqual(sim, 2/3, places=2)
    
    def test_empty(self):
        self.assertEqual(lcs_similarity("", ""), 1.0)
        self.assertEqual(lcs_similarity("ABC", ""), 0.0)
        self.assertEqual(lcs_similarity("", "ABC"), 0.0)
    
    def test_case_sensitivity(self):
        self.assertEqual(lcs_similarity("abc", "ABC"), 0.0)


class TestLCSDistance(unittest.TestCase):
    """Tests for lcs_distance function."""
    
    def test_identical(self):
        self.assertEqual(lcs_distance("ABC", "ABC"), 0)
    
    def test_no_common(self):
        self.assertEqual(lcs_distance("ABC", "DEF"), 6)
    
    def test_partial(self):
        # LCS of "ABC" and "AC" is "AC" (length 2)
        # Distance = 3 + 2 - 2*2 = 1
        self.assertEqual(lcs_distance("ABC", "AC"), 1)
    
    def test_empty(self):
        self.assertEqual(lcs_distance("", ""), 0)
        self.assertEqual(lcs_distance("ABC", ""), 3)


class TestLCSOfMultiple(unittest.TestCase):
    """Tests for lcs_of_multiple function."""
    
    def test_two_sequences(self):
        result = lcs_of_multiple(["ABC", "ADC"])
        self.assertEqual(result, ['A', 'C'])
    
    def test_three_sequences(self):
        result = lcs_of_multiple(["ABC", "ADC", "AEC"])
        self.assertEqual(result, ['A', 'C'])
    
    def test_no_common(self):
        result = lcs_of_multiple(["ABC", "DEF", "GHI"])
        self.assertEqual(result, [])
    
    def test_empty_list(self):
        self.assertEqual(lcs_of_multiple([]), [])
    
    def test_single_sequence(self):
        result = lcs_of_multiple(["ABC"])
        self.assertEqual(result, ['A', 'B', 'C'])


class TestShortestCommonSupersequence(unittest.TestCase):
    """Tests for shortest_common_supersequence function."""
    
    def test_basic(self):
        result = shortest_common_supersequence("ABC", "ACD")
        self.assertEqual(len(result), 4)
        # Check both sequences are subsequences
        self.assertTrue(is_subsequence("ABC", result))
        self.assertTrue(is_subsequence("ACD", result))
    
    def test_identical(self):
        result = shortest_common_supersequence("ABC", "ABC")
        self.assertEqual(result, ['A', 'B', 'C'])
    
    def test_no_common(self):
        result = shortest_common_supersequence("ABC", "DEF")
        self.assertEqual(len(result), 6)
    
    def test_empty(self):
        result = shortest_common_supersequence("", "ABC")
        self.assertEqual(result, ['A', 'B', 'C'])
        
        result = shortest_common_supersequence("ABC", "")
        self.assertEqual(result, ['A', 'B', 'C'])


class TestFindLCSPositions(unittest.TestCase):
    """Tests for find_lcs_positions function."""
    
    def test_basic(self):
        positions = find_lcs_positions("ABC", "ADC")
        # LCS is "AC"
        self.assertEqual(len(positions), 2)
        # Check positions match
        for pos1, pos2 in positions:
            self.assertEqual("ABC"[pos1], "ADC"[pos2])
    
    def test_no_common(self):
        positions = find_lcs_positions("ABC", "DEF")
        self.assertEqual(positions, [])
    
    def test_empty(self):
        self.assertEqual(find_lcs_positions("", "ABC"), [])
        self.assertEqual(find_lcs_positions("ABC", ""), [])


class TestIsSubsequence(unittest.TestCase):
    """Tests for is_subsequence function."""
    
    def test_basic(self):
        self.assertTrue(is_subsequence("ABC", "AXBYCZ"))
        self.assertTrue(is_subsequence("AC", "ABC"))
        self.assertTrue(is_subsequence("", "ABC"))
        self.assertTrue(is_subsequence("ABC", "ABC"))
    
    def test_not_subsequence(self):
        self.assertFalse(is_subsequence("ABC", "ACB"))
        self.assertFalse(is_subsequence("ABC", "AB"))
        self.assertFalse(is_subsequence("ABC", ""))
    
    def test_with_lists(self):
        self.assertTrue(is_subsequence([1, 3], [1, 2, 3, 4]))
        self.assertFalse(is_subsequence([1, 4], [1, 2, 3]))


class TestCountDistinctLCS(unittest.TestCase):
    """Tests for count_distinct_lcs function."""
    
    def test_single_lcs(self):
        count = count_distinct_lcs("ABC", "ABC")
        self.assertEqual(count, 1)
    
    def test_multiple_lcs(self):
        # "ABC" and "ACB" have two LCS: "AB" and "AC"
        count = count_distinct_lcs("ABC", "ACB")
        self.assertEqual(count, 2)  # "AB" and "AC"
    
    def test_no_common(self):
        count = count_distinct_lcs("ABC", "DEF")
        self.assertEqual(count, 1)  # Empty string is one LCS


class TestLCSEngine(unittest.TestCase):
    """Tests for LCSEngine class."""
    
    def setUp(self):
        self.engine = LCSEngine()
    
    def test_compute(self):
        result = self.engine.compute("ABC", "AC")
        self.assertEqual(result, ['A', 'C'])
    
    def test_length(self):
        length = self.engine.length("ABC", "AC")
        self.assertEqual(length, 2)
    
    def test_similarity(self):
        sim = self.engine.similarity("ABC", "AC")
        self.assertAlmostEqual(sim, 4/5, places=2)
    
    def test_diff(self):
        diff = self.engine.diff("ABC", "AC")
        self.assertEqual(len(diff), 3)
    
    def test_caching(self):
        # Same call twice - should use cache
        r1 = self.engine.compute("ABC", "DEF")
        r2 = self.engine.compute("ABC", "DEF")
        self.assertEqual(r1, r2)
    
    def test_clear_cache(self):
        self.engine.compute("ABC", "DEF")
        self.engine.clear_cache()
        # Should work after clear
        result = self.engine.compute("ABC", "DEF")
        self.assertEqual(result, [])


class TestConvenienceFunctions(unittest.TestCase):
    """Tests for convenience functions."""
    
    def test_text_similarity(self):
        sim = text_similarity("hello world", "hello there")
        self.assertGreater(sim, 0.5)
    
    def test_line_similarity(self):
        text1 = "line1\nline2\nline3"
        text2 = "line1\nline3\nline4"
        sim = line_similarity(text1, text2)
        self.assertGreater(sim, 0.5)
    
    def test_word_similarity(self):
        text1 = "the quick brown fox"
        text2 = "the quick blue fox"
        sim = word_similarity(text1, text2)
        self.assertGreater(sim, 0.5)
    
    def test_line_diff(self):
        text1 = "line1\nline2\nline3"
        text2 = "line1\nline4\nline3"
        diff = line_diff(text1, text2)
        self.assertIn("--- original", diff)
        self.assertIn("+++ modified", diff)


class TestEdgeCases(unittest.TestCase):
    """Tests for edge cases and boundary conditions."""
    
    def test_single_character(self):
        self.assertEqual(lcs("A", "A"), ['A'])
        self.assertEqual(lcs("A", "B"), [])
        self.assertEqual(lcs_length("A", "A"), 1)
    
    def test_repeated_characters(self):
        result = lcs("AAA", "AAA")
        self.assertEqual(result, ['A', 'A', 'A'])
        
        result = lcs("AAA", "AA")
        self.assertEqual(len(result), 2)
    
    def test_long_sequence(self):
        s1 = "A" * 1000
        s2 = "A" * 1000
        self.assertEqual(lcs_length(s1, s2), 1000)
    
    def test_unicode(self):
        result = lcs("你好世界", "你好中国")
        self.assertEqual(len(result), 2)  # "你好"
    
    def test_numbers(self):
        result = lcs([1, 2, 3], [2, 3, 4])
        self.assertEqual(result, [2, 3])
    
    def test_mixed_types(self):
        # Comparing different types works - elements just won't match
        result = lcs("123", [1, 2, 3])
        self.assertEqual(result, [])  # No common elements (string vs int)


if __name__ == "__main__":
    unittest.main(verbosity=2)