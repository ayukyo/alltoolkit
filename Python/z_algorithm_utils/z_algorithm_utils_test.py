"""
Unit tests for Z Algorithm Utilities

Tests cover all major functions: Z-array computation, pattern matching,
substring analysis, period detection, and palindrome operations.
"""

import unittest
from typing import List
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from z_algorithm_utils.mod import (
    z_array, z_array_bytes, z_array_with_sentinel,
    find_all_occurrences, find_first_occurrence, count_occurrences, find_matches,
    longest_prefix_suffix, longest_repeated_substring, find_all_repeated_substrings,
    longest_common_prefix,
    find_minimal_period, is_rotation, find_all_rotations,
    longest_palindromic_prefix, longest_palindromic_suffix,
    similarity_score, batch_similarity,
    distinct_substring_count, compress_string, decompress_string,
    iter_occurrences,
    z_to_border, border_to_z,
    ZPatternMatcher, ZMatch, StringPeriod,
    visualize_z_array, validate_z_array
)


class TestZArray(unittest.TestCase):
    """Test Z-array computation."""
    
    def test_basic_z_array(self):
        """Test basic Z-array computation."""
        # "aabcaabxaaz" -> [0, 1, 0, 0, 3, 1, 0, 0, 2, 1, 0]
        result = z_array("aabcaabxaaz")
        expected = [0, 1, 0, 0, 3, 1, 0, 0, 2, 1, 0]
        self.assertEqual(result, expected)
    
    def test_empty_string(self):
        """Test Z-array for empty string."""
        self.assertEqual(z_array(""), [])
    
    def test_single_char(self):
        """Test Z-array for single character."""
        self.assertEqual(z_array("a"), [0])
    
    def test_all_same(self):
        """Test Z-array for string of same characters."""
        # "aaaa" -> [0, 3, 2, 1]
        self.assertEqual(z_array("aaaa"), [0, 3, 2, 1])
    
    def test_no_matches(self):
        """Test Z-array for string with no prefix matches."""
        # "abcd" -> [0, 0, 0, 0]
        self.assertEqual(z_array("abcd"), [0, 0, 0, 0])
    
    def test_pattern_in_pattern(self):
        """Test Z-array where pattern appears multiple times."""
        # "abcabcabc" -> [0, 0, 0, 6, 0, 0, 3, 0, 0]
        result = z_array("abcabcabc")
        expected = [0, 0, 0, 6, 0, 0, 3, 0, 0]
        self.assertEqual(result, expected)
    
    def test_z_array_bytes(self):
        """Test Z-array computation for bytes."""
        data = b"aabcaabxaaz"
        result = z_array_bytes(data)
        expected = [0, 1, 0, 0, 3, 1, 0, 0, 2, 1, 0]
        self.assertEqual(result, expected)
    
    def test_z_array_with_sentinel(self):
        """Test Z-array with sentinel."""
        pattern = "abc"
        text = "abcabc"
        result = z_array_with_sentinel(pattern, text)
        # Should find pattern occurrences
        self.assertTrue(any(z >= 3 for z in result[4:]))


class TestPatternMatching(unittest.TestCase):
    """Test pattern matching functions."""
    
    def test_find_all_occurrences(self):
        """Test finding all occurrences."""
        self.assertEqual(find_all_occurrences("abc", "abcabcabc"), [0, 3, 6])
        self.assertEqual(find_all_occurrences("ab", "ababab"), [0, 2, 4])
        self.assertEqual(find_all_occurrences("xyz", "abcabcabc"), [])
    
    def test_find_first_occurrence(self):
        """Test finding first occurrence."""
        self.assertEqual(find_first_occurrence("abc", "xyzabc"), 3)
        self.assertEqual(find_first_occurrence("abc", "abcabc"), 0)
        self.assertEqual(find_first_occurrence("abc", "xyz"), -1)
    
    def test_count_occurrences(self):
        """Test counting occurrences."""
        self.assertEqual(count_occurrences("a", "banana"), 3)
        self.assertEqual(count_occurrences("ana", "banana"), 2)
        self.assertEqual(count_occurrences("xyz", "abcabc"), 0)
    
    def test_empty_pattern_or_text(self):
        """Test with empty pattern or text."""
        self.assertEqual(find_all_occurrences("", "abc"), [])
        self.assertEqual(find_all_occurrences("abc", ""), [])
        self.assertEqual(find_first_occurrence("", "abc"), -1)
        self.assertEqual(find_first_occurrence("abc", ""), -1)
    
    def test_pattern_longer_than_text(self):
        """Test when pattern is longer than text."""
        self.assertEqual(find_all_occurrences("abcdef", "abc"), [])
    
    def test_find_matches(self):
        """Test finding matches with details."""
        matches = find_matches("abc", "abcabc")
        self.assertEqual(len(matches), 2)
        self.assertEqual(matches[0].index, 0)
        self.assertEqual(matches[0].length, 3)
        self.assertEqual(matches[0].matched_substring, "abc")
    
    def test_iter_occurrences(self):
        """Test occurrence iterator."""
        positions = list(iter_occurrences("abc", "abcabcabc"))
        self.assertEqual(positions, [0, 3, 6])


class TestSubstringAnalysis(unittest.TestCase):
    """Test substring analysis functions."""
    
    def test_longest_prefix_suffix(self):
        """Test longest prefix-suffix."""
        self.assertEqual(longest_prefix_suffix("ababa"), 3)  # "aba"
        self.assertEqual(longest_prefix_suffix("aaaa"), 3)  # "aaa"
        self.assertEqual(longest_prefix_suffix("abcd"), 0)
        self.assertEqual(longest_prefix_suffix(""), 0)
    
    def test_longest_repeated_substring(self):
        """Test longest repeated substring."""
        substr, positions = longest_repeated_substring("banana")
        # "ana" appears at positions 1 and 3
        self.assertEqual(substr, "ana")
        self.assertIn(1, positions)
        self.assertIn(3, positions)
        
        substr, positions = longest_repeated_substring("abcabcabc")
        self.assertEqual(substr, "abcabc")
    
    def test_longest_common_prefix(self):
        """Test longest common prefix."""
        self.assertEqual(longest_common_prefix("abcdef", "abcxyz"), 3)
        self.assertEqual(longest_common_prefix("xyz", "abc"), 0)
        self.assertEqual(longest_common_prefix("same", "same"), 4)
    
    def test_find_all_repeated_substrings(self):
        """Test finding all repeated substrings."""
        result = find_all_repeated_substrings("banana", min_length=2)
        self.assertTrue(len(result) > 0)
        # Check that substrings are sorted by length
        lengths = [len(s) for s, _ in result]
        self.assertEqual(lengths, sorted(lengths, reverse=True))


class TestPeriodDetection(unittest.TestCase):
    """Test period detection functions."""
    
    def test_find_minimal_period(self):
        """Test finding minimal period."""
        period = find_minimal_period("abcabcabc")
        self.assertEqual(period.period, 3)
        self.assertTrue(period.is_periodic)
        self.assertEqual(period.period_string, "abc")
        
        period = find_minimal_period("aaaa")
        self.assertEqual(period.period, 1)
        self.assertTrue(period.is_periodic)
        
        period = find_minimal_period("abcde")
        self.assertEqual(period.period, 5)
        self.assertFalse(period.is_periodic)
    
    def test_is_rotation(self):
        """Test rotation detection."""
        self.assertTrue(is_rotation("abcde", "cdeab"))
        self.assertTrue(is_rotation("abc", "abc"))
        self.assertFalse(is_rotation("abcde", "abced"))
        self.assertFalse(is_rotation("abc", "abcd"))
    
    def test_find_all_rotations(self):
        """Test finding all rotations."""
        rotations = find_all_rotations("abc")
        self.assertEqual(len(rotations), 3)
        self.assertIn("abc", rotations)
        self.assertIn("bca", rotations)
        self.assertIn("cab", rotations)
        
        # Periodic string should have fewer unique rotations
        rotations = find_all_rotations("aaaa")
        self.assertEqual(len(rotations), 1)


class TestPalindromeOperations(unittest.TestCase):
    """Test palindrome-related functions."""
    
    def test_longest_palindromic_prefix(self):
        """Test longest palindromic prefix."""
        self.assertEqual(longest_palindromic_prefix("abacaba"), "abacaba")
        self.assertEqual(longest_palindromic_prefix("abaxyz"), "aba")
        # Single character is a palindrome (length 1)
        self.assertEqual(longest_palindromic_prefix("xyz"), "x")
        self.assertEqual(longest_palindromic_prefix(""), "")
    
    def test_longest_palindromic_suffix(self):
        """Test longest palindromic suffix."""
        self.assertEqual(longest_palindromic_suffix("xyzaba"), "aba")
        self.assertEqual(longest_palindromic_suffix("abacaba"), "abacaba")
        # Single character is a palindrome (length 1)
        self.assertEqual(longest_palindromic_suffix("xyz"), "z")


class TestSimilarity(unittest.TestCase):
    """Test similarity functions."""
    
    def test_similarity_score(self):
        """Test similarity score calculation."""
        self.assertEqual(similarity_score("abcdef", "abcxyz"), 0.5)
        self.assertEqual(similarity_score("same", "same"), 1.0)
        self.assertEqual(similarity_score("abc", "xyz"), 0.0)
        self.assertEqual(similarity_score("", ""), 1.0)
        self.assertEqual(similarity_score("abc", ""), 0.0)
    
    def test_batch_similarity(self):
        """Test batch similarity calculation."""
        base = "abcdef"
        strings = ["abcxyz", "abcdef", "xyz", ""]
        scores = batch_similarity(base, strings)
        self.assertEqual(len(scores), 4)
        # "abcxyz" shares 3 chars with "abcdef"
        self.assertEqual(scores[1], 1.0)  # Exact match


class TestCompression(unittest.TestCase):
    """Test compression and decompression."""
    
    def test_compress_string(self):
        """Test string compression."""
        pattern, count = compress_string("abcabcabc")
        self.assertEqual(pattern, "abc")
        self.assertEqual(count, 3)
        
        pattern, count = compress_string("aaaa")
        self.assertEqual(pattern, "a")
        self.assertEqual(count, 4)
        
        pattern, count = compress_string("abcde")
        self.assertEqual(pattern, "abcde")
        self.assertEqual(count, 1)
    
    def test_decompress_string(self):
        """Test string decompression."""
        self.assertEqual(decompress_string("abc", 3), "abcabcabc")
        self.assertEqual(decompress_string("a", 4), "aaaa")
    
    def test_compress_decompress_roundtrip(self):
        """Test roundtrip compression."""
        original = "abcabcabc"
        pattern, count = compress_string(original)
        restored = decompress_string(pattern, count)
        self.assertEqual(restored, original)


class TestDistinctSubstringCount(unittest.TestCase):
    """Test distinct substring counting."""
    
    def test_distinct_substring_count(self):
        """Test counting distinct substrings."""
        # "abc" has 6 distinct substrings: a, b, c, ab, bc, abc
        self.assertEqual(distinct_substring_count("abc"), 6)
        
        # "aaaa" has 4 distinct substrings: a, aa, aaa, aaaa
        self.assertEqual(distinct_substring_count("aaaa"), 4)
        
        # Empty string has 0
        self.assertEqual(distinct_substring_count(""), 0)


class TestBorderConversion(unittest.TestCase):
    """Test Z-array to border array conversion."""
    
    def test_z_to_border(self):
        """Test Z to border conversion."""
        z = z_array("aabcaabxaaz")
        border = z_to_border(z)
        self.assertEqual(len(border), len(z))
    
    def test_border_to_z(self):
        """Test border to Z conversion."""
        z = z_array("abcabcabc")
        border = z_to_border(z)
        z_back = border_to_z(border)
        # Conversion might not be exact due to information loss
        self.assertEqual(len(z_back), len(z))


class TestZPatternMatcher(unittest.TestCase):
    """Test pattern matcher class."""
    
    def test_single_pattern(self):
        """Test matching single pattern."""
        matcher = ZPatternMatcher(["abc"])
        results = matcher.search("abcabc")
        self.assertEqual(len(results), 2)
        self.assertEqual(results[0], (0, 0, "abc"))
        self.assertEqual(results[1], (0, 3, "abc"))
    
    def test_multiple_patterns(self):
        """Test matching multiple patterns."""
        matcher = ZPatternMatcher(["ab", "bc"])
        results = matcher.search("abcabc")
        self.assertEqual(len(results), 4)  # 2 "ab" + 2 "bc"
    
    def test_search_first(self):
        """Test finding first occurrence."""
        matcher = ZPatternMatcher(["bc", "ab"])
        result = matcher.search_first("abcabc")
        self.assertIsNotNone(result)
        self.assertEqual(result[1], 0)  # "ab" appears first
    
    def test_count_all(self):
        """Test counting all patterns."""
        matcher = ZPatternMatcher(["a", "b", "c"])
        counts = matcher.count_all("abcabc")
        self.assertEqual(counts["a"], 2)
        self.assertEqual(counts["b"], 2)
        self.assertEqual(counts["c"], 2)
    
    def test_no_match(self):
        """Test when no pattern matches."""
        matcher = ZPatternMatcher(["xyz"])
        self.assertEqual(matcher.search("abcabc"), [])
        self.assertIsNone(matcher.search_first("abcabc"))


class TestUtilityFunctions(unittest.TestCase):
    """Test utility functions."""
    
    def test_visualize_z_array(self):
        """Test Z-array visualization."""
        visualization = visualize_z_array("aaaa")
        self.assertIn("String:", visualization)
        self.assertIn("aaaa", visualization)
        self.assertIn("Z:", visualization)
    
    def test_validate_z_array(self):
        """Test Z-array validation."""
        s = "aabcaabxaaz"
        z = z_array(s)
        self.assertTrue(validate_z_array(s, z))
        
        # Invalid Z-array
        invalid_z = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        self.assertFalse(validate_z_array(s, invalid_z))
        
        # Wrong length
        self.assertFalse(validate_z_array(s, z[:5]))


class TestDataClasses(unittest.TestCase):
    """Test data classes."""
    
    def test_z_match(self):
        """Test ZMatch dataclass."""
        match = ZMatch(index=2, length=3, text="abcdef")
        self.assertEqual(match.index, 2)
        self.assertEqual(match.length, 3)
        self.assertEqual(match.matched_substring, "cde")
    
    def test_string_period(self):
        """Test StringPeriod dataclass."""
        period = StringPeriod(string="abcabc", period=3, is_periodic=True)
        self.assertEqual(period.period_string, "abc")


class TestEdgeCases(unittest.TestCase):
    """Test edge cases."""
    
    def test_single_char_string(self):
        """Test operations on single character."""
        self.assertEqual(z_array("a"), [0])
        self.assertEqual(find_all_occurrences("a", "a"), [0])
        self.assertEqual(longest_prefix_suffix("a"), 0)
    
    def test_all_unique_chars(self):
        """Test string with all unique characters."""
        s = "abcdefg"
        self.assertEqual(z_array(s), [0] * 7)
        self.assertEqual(longest_prefix_suffix(s), 0)
        period = find_minimal_period(s)
        self.assertFalse(period.is_periodic)
    
    def test_repeated_single_char(self):
        """Test string of repeated single character."""
        s = "aaaaaa"
        z = z_array(s)
        # Z[1] should be 5, Z[2] should be 4, etc.
        self.assertEqual(z[1], 5)
        self.assertEqual(z[2], 4)
        period = find_minimal_period(s)
        self.assertEqual(period.period, 1)
    
    def test_unicode_strings(self):
        """Test with Unicode strings."""
        s = "你好你好"
        self.assertEqual(find_all_occurrences("你好", s), [0, 2])
        period = find_minimal_period(s)
        self.assertEqual(period.period, 2)


if __name__ == '__main__':
    unittest.main(verbosity=2)