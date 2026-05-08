"""
Tests for Suffix Automaton Utils.

Tests all major functionalities of the suffix automaton implementation.
"""

import unittest
from mod import (
    SuffixAutomaton,
    build_suffix_automaton,
    count_occurrences,
    find_all_occurrences,
    longest_common_substring,
    count_different_substrings,
    longest_repeating_substring,
    kth_different_substring,
    shortest_unique_substring,
    MultiSuffixAutomaton,
)


class TestSuffixAutomatonBasic(unittest.TestCase):
    """Basic tests for suffix automaton construction and queries."""
    
    def test_empty_string(self):
        """Test automaton for empty string."""
        sa = SuffixAutomaton("")
        self.assertEqual(sa.size, 1)
        self.assertEqual(sa.count_different_substrings(), 0)
        self.assertEqual(sa.count_occurrences(""), 1)
        self.assertEqual(sa.count_occurrences("a"), 0)
    
    def test_single_character(self):
        """Test automaton for single character."""
        sa = SuffixAutomaton("a")
        self.assertEqual(sa.count_occurrences("a"), 1)
        self.assertEqual(sa.count_occurrences("b"), 0)
        self.assertTrue(sa.contains("a"))
        self.assertFalse(sa.contains("b"))
        self.assertEqual(sa.count_different_substrings(), 1)
    
    def test_simple_string(self):
        """Test automaton for simple string."""
        sa = SuffixAutomaton("abc")
        self.assertTrue(sa.contains("abc"))
        self.assertTrue(sa.contains("ab"))
        self.assertTrue(sa.contains("bc"))
        self.assertTrue(sa.contains("a"))
        self.assertTrue(sa.contains("b"))
        self.assertTrue(sa.contains("c"))
        self.assertFalse(sa.contains("ac"))
        self.assertFalse(sa.contains("cba"))
    
    def test_repeated_pattern(self):
        """Test automaton with repeated patterns."""
        sa = SuffixAutomaton("aaaa")
        self.assertEqual(sa.count_occurrences("a"), 4)
        self.assertEqual(sa.count_occurrences("aa"), 3)
        self.assertEqual(sa.count_occurrences("aaa"), 2)
        self.assertEqual(sa.count_occurrences("aaaa"), 1)
        self.assertEqual(sa.count_occurrences("b"), 0)
    
    def test_abacaba(self):
        """Test classic 'abacaba' example."""
        sa = SuffixAutomaton("abacaba")
        self.assertEqual(sa.count_occurrences("aba"), 2)
        self.assertEqual(sa.count_occurrences("ac"), 1)
        self.assertEqual(sa.count_occurrences("ba"), 2)
        self.assertEqual(sa.count_occurrences("c"), 1)


class TestOccurrences(unittest.TestCase):
    """Tests for occurrence counting and finding."""
    
    def test_count_occurrences(self):
        """Test occurrence counting."""
        sa = SuffixAutomaton("abcabcabc")
        self.assertEqual(sa.count_occurrences("abc"), 3)
        self.assertEqual(sa.count_occurrences("ab"), 3)
        self.assertEqual(sa.count_occurrences("bc"), 3)
        self.assertEqual(sa.count_occurrences("cab"), 2)
        self.assertEqual(sa.count_occurrences("abcab"), 2)
    
    def test_find_all_occurrences(self):
        """Test finding all occurrence positions."""
        sa = SuffixAutomaton("abcabc")
        positions = sa.find_all_occurrences("abc")
        self.assertEqual(positions, [0, 3])
        
        positions = sa.find_all_occurrences("ab")
        self.assertEqual(positions, [0, 3])
        
        positions = sa.find_all_occurrences("bc")
        self.assertEqual(positions, [1, 4])
        
        positions = sa.find_all_occurrences("xyz")
        self.assertEqual(positions, [])
    
    def test_empty_pattern(self):
        """Test with empty pattern."""
        sa = SuffixAutomaton("abc")
        # Empty pattern occurs at all positions (n+1 positions)
        self.assertEqual(sa.count_occurrences(""), 4)
    
    def test_pattern_not_found(self):
        """Test pattern not in text."""
        sa = SuffixAutomaton("abcdef")
        self.assertEqual(sa.count_occurrences("xyz"), 0)
        self.assertEqual(sa.find_all_occurrences("xyz"), [])
        self.assertFalse(sa.contains("xyz"))


class TestDifferentSubstrings(unittest.TestCase):
    """Tests for counting different substrings."""
    
    def test_count_different_substrings(self):
        """Test counting unique substrings."""
        sa = SuffixAutomaton("aaa")
        # "a", "aa", "aaa" = 3 different substrings
        self.assertEqual(sa.count_different_substrings(), 3)
        
        sa = SuffixAutomaton("abc")
        # "a", "b", "c", "ab", "bc", "abc" = 6 different substrings
        self.assertEqual(sa.count_different_substrings(), 6)
        
        sa = SuffixAutomaton("abacaba")
        # Should be 21 different substrings
        self.assertEqual(sa.count_different_substrings(), 21)
    
    def test_different_substrings_vs_actual(self):
        """Verify count against actual unique substrings."""
        text = "abacaba"
        sa = SuffixAutomaton(text)
        
        # Generate all actual substrings
        actual = set()
        for i in range(len(text)):
            for j in range(i + 1, len(text) + 1):
                actual.add(text[i:j])
        
        self.assertEqual(sa.count_different_substrings(), len(actual))
    
    def test_repeated_string(self):
        """Test repeated string."""
        sa = SuffixAutomaton("aaaa")
        self.assertEqual(sa.count_different_substrings(), 4)


class TestLongestCommonSubstring(unittest.TestCase):
    """Tests for longest common substring."""
    
    def test_lcs_basic(self):
        """Test basic LCS finding."""
        sa = SuffixAutomaton("abcdef")
        lcs, length = sa.longest_common_substring("cdefgh")
        self.assertEqual(lcs, "cdef")
        self.assertEqual(length, 4)
    
    def test_lcs_no_common(self):
        """Test LCS when no common substring."""
        sa = SuffixAutomaton("abc")
        lcs, length = sa.longest_common_substring("xyz")
        self.assertEqual(lcs, "")
        self.assertEqual(length, 0)
    
    def test_lcs_single_char(self):
        """Test LCS with single common character."""
        sa = SuffixAutomaton("abc")
        lcs, length = sa.longest_common_substring("cba")
        self.assertEqual(length, 1)
    
    def test_lcs_same_string(self):
        """Test LCS with same string."""
        sa = SuffixAutomaton("abcdef")
        lcs, length = sa.longest_common_substring("abcdef")
        self.assertEqual(lcs, "abcdef")
        self.assertEqual(length, 6)
    
    def test_lcs_long(self):
        """Test LCS with longer strings."""
        sa = SuffixAutomaton("the quick brown fox jumps")
        lcs, length = sa.longest_common_substring("brown fox is lazy")
        self.assertEqual(lcs, "brown fox ")
        self.assertEqual(length, 10)


class TestLongestRepeatingSubstring(unittest.TestCase):
    """Tests for longest repeating substring."""
    
    def test_longest_repeating_basic(self):
        """Test basic repeating substring."""
        sa = SuffixAutomaton("abcabc")
        result, length = sa.longest_repeating_substring()
        self.assertEqual(length, 3)
        self.assertEqual(result, "abc")
    
    def test_longest_repeating_none(self):
        """Test when no substring repeats."""
        sa = SuffixAutomaton("abcdef")
        result, length = sa.longest_repeating_substring()
        self.assertEqual(length, 0)
    
    def test_longest_repeating_min_occurrences(self):
        """Test with different minimum occurrence requirements."""
        sa = SuffixAutomaton("abababab")
        result, length = sa.longest_repeating_substring(2)
        self.assertEqual(length, 6)
        
        result, length = sa.longest_repeating_substring(3)
        self.assertEqual(length, 4)
        
        result, length = sa.longest_repeating_substring(4)
        self.assertEqual(length, 2)
    
    def test_repeated_char(self):
        """Test repeated single character."""
        sa = SuffixAutomaton("aaaa")
        result, length = sa.longest_repeating_substring()
        self.assertEqual(result, "aaa")
        self.assertEqual(length, 3)


class TestKthSubstring(unittest.TestCase):
    """Tests for finding k-th different substring."""
    
    def test_kth_basic(self):
        """Test basic k-th substring."""
        sa = SuffixAutomaton("abc")
        # Sorted substrings: a, ab, abc, b, bc, c
        
        self.assertEqual(sa.kth_different_substring(1), "a")
        self.assertEqual(sa.kth_different_substring(2), "ab")
        self.assertEqual(sa.kth_different_substring(3), "abc")
        self.assertEqual(sa.kth_different_substring(4), "b")
        self.assertEqual(sa.kth_different_substring(5), "bc")
        self.assertEqual(sa.kth_different_substring(6), "c")
    
    def test_kth_invalid(self):
        """Test k-th with invalid index."""
        sa = SuffixAutomaton("abc")
        self.assertEqual(sa.kth_different_substring(0), "")
        self.assertEqual(sa.kth_different_substring(100), "")
    
    def test_kth_repeated(self):
        """Test k-th with repeated characters."""
        sa = SuffixAutomaton("aaa")
        # Sorted substrings: a, aa, aaa
        self.assertEqual(sa.kth_different_substring(1), "a")
        self.assertEqual(sa.kth_different_substring(2), "aa")
        self.assertEqual(sa.kth_different_substring(3), "aaa")


class TestShortestUniqueSubstring(unittest.TestCase):
    """Tests for shortest unique substring."""
    
    def test_shortest_unique_basic(self):
        """Test basic shortest unique substring."""
        sa = SuffixAutomaton("abcd")
        result = sa.shortest_unique_substring(0)
        self.assertEqual(result, "a")
    
    def test_shortest_unique_repeated(self):
        """Test shortest unique in string with repeats."""
        sa = SuffixAutomaton("aab")
        result = sa.shortest_unique_substring(0)
        self.assertEqual(result, "aa")  # "a" appears twice, "aa" appears once
        
        result = sa.shortest_unique_substring(1)
        self.assertEqual(result, "ab")
        
        result = sa.shortest_unique_substring(2)
        self.assertEqual(result, "b")
    
    def test_shortest_unique_last_position(self):
        """Test at last position."""
        sa = SuffixAutomaton("abc")
        result = sa.shortest_unique_substring(2)
        self.assertEqual(result, "c")


class TestConvenienceFunctions(unittest.TestCase):
    """Tests for convenience functions."""
    
    def test_build_suffix_automaton(self):
        """Test convenience build function."""
        sa = build_suffix_automaton("test")
        self.assertEqual(sa.count_occurrences("t"), 2)
    
    def test_count_occurrences_func(self):
        """Test convenience count_occurrences."""
        result = count_occurrences("abcabcabc", "abc")
        self.assertEqual(result, 3)
    
    def test_find_all_occurrences_func(self):
        """Test convenience find_all_occurrences."""
        result = find_all_occurrences("abcabc", "bc")
        self.assertEqual(result, [1, 4])
    
    def test_longest_common_substring_func(self):
        """Test convenience LCS function."""
        result = longest_common_substring("abcdef", "defghi")
        self.assertEqual(result, "def")
    
    def test_count_different_substrings_func(self):
        """Test convenience count function."""
        result = count_different_substrings("abc")
        self.assertEqual(result, 6)
    
    def test_longest_repeating_substring_func(self):
        """Test convenience repeating substring function."""
        result = longest_repeating_substring("abcabc")
        self.assertEqual(result, "abc")
    
    def test_kth_different_substring_func(self):
        """Test convenience k-th function."""
        result = kth_different_substring("abc", 1)
        self.assertEqual(result, "a")


class TestMultiSuffixAutomaton(unittest.TestCase):
    """Tests for multiple string suffix automaton."""
    
    def test_add_and_search(self):
        """Test adding strings and searching."""
        msa = MultiSuffixAutomaton()
        msa.add_text("abc")
        msa.add_text("def")
        msa.add_text("ghi")
        
        result = msa.pattern_in_texts("ab")
        self.assertEqual(result, [0])
        
        result = msa.pattern_in_texts("d")
        self.assertEqual(result, [1])
    
    def test_common_substring(self):
        """Test finding common substring."""
        msa = MultiSuffixAutomaton()
        msa.add_text("abcdef")
        msa.add_text("defghi")
        
        result = msa.common_substring_in_all()
        self.assertEqual(result, "def")


class TestAutomatonInfo(unittest.TestCase):
    """Tests for automaton information retrieval."""
    
    def test_get_info(self):
        """Test getting automaton info."""
        sa = SuffixAutomaton("abacaba")
        info = sa.get_info()
        
        self.assertEqual(info["text_length"], 7)
        self.assertEqual(info["num_states"], sa.size)
        self.assertGreater(info["num_states"], 0)
        self.assertEqual(info["num_different_substrings"], 21)
    
    def test_get_state_info(self):
        """Test getting state info."""
        sa = SuffixAutomaton("abc")
        
        info = sa.get_state_info(0)
        self.assertEqual(info["length"], 0)
        self.assertEqual(info["link"], -1)
        self.assertIn("transitions", info)
    
    def test_get_state_info_invalid(self):
        """Test state info with invalid index."""
        sa = SuffixAutomaton("abc")
        info = sa.get_state_info(-1)
        self.assertEqual(info, {})
        
        info = sa.get_state_info(100)
        self.assertEqual(info, {})
    
    def test_traverse(self):
        """Test traversing automaton."""
        sa = SuffixAutomaton("abc")
        
        state = sa.traverse("a")
        self.assertIsNotNone(state)
        
        state = sa.traverse("xyz")
        self.assertIsNone(state)


class TestAllSubstringsOfLength(unittest.TestCase):
    """Tests for getting substrings of specific length."""
    
    def test_length_one(self):
        """Test substrings of length 1."""
        sa = SuffixAutomaton("abc")
        result = sa.all_substrings_of_length(1)
        self.assertEqual(result, {"a", "b", "c"})
    
    def test_length_two(self):
        """Test substrings of length 2."""
        sa = SuffixAutomaton("abc")
        result = sa.all_substrings_of_length(2)
        self.assertEqual(result, {"ab", "bc"})
    
    def test_length_invalid(self):
        """Test with invalid lengths."""
        sa = SuffixAutomaton("abc")
        result = sa.all_substrings_of_length(0)
        self.assertEqual(result, {""})
        
        result = sa.all_substrings_of_length(10)
        self.assertEqual(result, set())


class TestEdgeCases(unittest.TestCase):
    """Tests for edge cases and boundary conditions."""
    
    def test_unicode(self):
        """Test with unicode characters."""
        sa = SuffixAutomaton("你好世界你好")
        self.assertEqual(sa.count_occurrences("你好"), 2)
        self.assertTrue(sa.contains("世界"))
    
    def test_numbers(self):
        """Test with numeric characters."""
        sa = SuffixAutomaton("123123123")
        self.assertEqual(sa.count_occurrences("123"), 3)
        self.assertEqual(sa.count_occurrences("231"), 2)
    
    def test_mixed_case(self):
        """Test with mixed case."""
        sa = SuffixAutomaton("AbCabc")
        self.assertEqual(sa.count_occurrences("abc"), 1)
        self.assertEqual(sa.count_occurrences("AbC"), 1)
    
    def test_special_chars(self):
        """Test with special characters."""
        sa = SuffixAutomaton("a.b.c.a.b.c")
        self.assertEqual(sa.count_occurrences("a.b"), 2)
    
    def test_long_string(self):
        """Test with longer string."""
        text = "abcdefghijklmnopqrstuvwxyz" * 10
        sa = SuffixAutomaton(text)
        self.assertEqual(sa.count_occurrences("abc"), 10)
        self.assertTrue(sa.contains("zabc"))


class TestComplexity(unittest.TestCase):
    """Tests to verify complexity guarantees."""
    
    def test_state_count(self):
        """Verify state count is at most 2n-1."""
        for text in ["", "a", "abc", "abcdef", "aaaaaaaa", "abcabcabc"]:
            sa = SuffixAutomaton(text)
            max_states = 2 * len(text) - 1 if len(text) > 0 else 1
            self.assertLessEqual(sa.size, max_states + 1)  # +1 for initial state
    
    def test_construction_time(self):
        """Test that construction doesn't explode for longer strings."""
        # This test should run quickly if O(n)
        import time
        text = "abc" * 1000
        
        start = time.time()
        sa = SuffixAutomaton(text)
        elapsed = time.time() - start
        
        # Should take less than 1 second for 3000 character string
        self.assertLess(elapsed, 1.0)
        self.assertEqual(sa.count_occurrences("abc"), 1000)


if __name__ == "__main__":
    unittest.main(verbosity=2)