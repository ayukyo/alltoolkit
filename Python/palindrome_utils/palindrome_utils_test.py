#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AllToolkit - Palindrome Utilities Test Suite
=============================================
Comprehensive tests for palindrome detection and processing functions.
"""

import unittest
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from palindrome_utils.mod import (
    is_palindrome,
    normalize_for_palindrome,
    find_all_palindromes,
    find_longest_palindrome,
    count_palindromes,
    find_palindromic_subsequences,
    min_insertions_to_palindrome,
    make_palindrome,
    find_palindrome_pairs,
    is_palindrome_number,
    generate_palindromes,
    longest_palindromic_subsequence_length,
    get_palindrome_info,
    is_semordnilap,
    is_mirrored_palindrome,
    PalindromeMatch
)


class TestIsPalindrome(unittest.TestCase):
    """Test is_palindrome function."""
    
    def test_basic_palindromes(self):
        """Test basic palindrome strings."""
        self.assertTrue(is_palindrome("racecar"))
        self.assertTrue(is_palindrome("level"))
        self.assertTrue(is_palindrome("deed"))
        self.assertTrue(is_palindrome("madam"))
        self.assertTrue(is_palindrome("radar"))
        self.assertTrue(is_palindrome("civic"))
        self.assertTrue(is_palindrome("kayak"))
        self.assertTrue(is_palindrome("rotor"))
    
    def test_non_palindromes(self):
        """Test non-palindrome strings."""
        self.assertFalse(is_palindrome("hello"))
        self.assertFalse(is_palindrome("world"))
        self.assertFalse(is_palindrome("python"))
        self.assertFalse(is_palindrome("abcdef"))
    
    def test_with_spaces_and_punctuation(self):
        """Test palindromes with spaces and punctuation."""
        self.assertTrue(is_palindrome("A man, a plan, a canal: Panama"))
        self.assertTrue(is_palindrome("Was it a car or a cat I saw?"))
        self.assertTrue(is_palindrome("No 'x' in Nixon"))
        self.assertTrue(is_palindrome("Able was I ere I saw Elba"))
    
    def test_case_sensitive(self):
        """Test case-sensitive palindrome checking."""
        self.assertFalse(is_palindrome("Race Car", case_sensitive=True))
        self.assertTrue(is_palindrome("Race Car", case_sensitive=False))
        self.assertFalse(is_palindrome("Level", case_sensitive=True))
        self.assertTrue(is_palindrome("Level", case_sensitive=False))
    
    def test_empty_string(self):
        """Test empty string."""
        self.assertTrue(is_palindrome(""))
        self.assertTrue(is_palindrome("   "))
    
    def test_single_character(self):
        """Test single character strings."""
        self.assertTrue(is_palindrome("a"))
        self.assertTrue(is_palindrome("A"))
        self.assertTrue(is_palindrome("x"))
    
    def test_unicode_palindromes(self):
        """Test Unicode palindrome strings."""
        self.assertTrue(is_palindrome("上海自来水来自海上"))
        self.assertTrue(is_palindrome("黄山落叶松叶落山黄"))
        # Mixed Chinese-English not palindrome
        self.assertFalse(is_palindrome("中文 palindrome 测试"))
    
    def test_numeric_palindromes(self):
        """Test numeric palindrome strings."""
        self.assertTrue(is_palindrome("12321"))
        self.assertTrue(is_palindrome("123454321"))
        self.assertFalse(is_palindrome("12345"))


class TestNormalizeForPalindrome(unittest.TestCase):
    """Test normalize_for_palindrome function."""
    
    def test_basic_normalization(self):
        """Test basic normalization."""
        self.assertEqual(normalize_for_palindrome("RaceCar"), "racecar")
        self.assertEqual(normalize_for_palindrome("HELLO"), "hello")
    
    def test_with_punctuation(self):
        """Test normalization with punctuation removal."""
        self.assertEqual(
            normalize_for_palindrome("A man, a plan, a canal: Panama"),
            "amanaplanacanalpanama"
        )
        self.assertEqual(
            normalize_for_palindrome("Was it a car or a cat I saw?"),
            "wasitacaroracatisaw"
        )
    
    def test_case_sensitive(self):
        """Test case-sensitive normalization."""
        self.assertEqual(
            normalize_for_palindrome("Hello World!", case_sensitive=True),
            "HelloWorld"
        )
        self.assertEqual(
            normalize_for_palindrome("Hello World!", case_sensitive=False),
            "helloworld"
        )


class TestFindAllPalindromes(unittest.TestCase):
    """Test find_all_palindromes function."""
    
    def test_basic_find(self):
        """Test basic palindrome finding."""
        palindromes = find_all_palindromes("ababa")
        texts = [p.text for p in palindromes]
        self.assertIn("aba", texts)
        self.assertIn("bab", texts)
        self.assertIn("ababa", texts)
    
    def test_min_length(self):
        """Test minimum length filtering."""
        palindromes = find_all_palindromes("aaa", min_length=1)
        # Should find 'a', 'aa', 'aaa' but we use min_length=2 by default
        palindromes_default = find_all_palindromes("aaa", min_length=2)
        texts = [p.text for p in palindromes_default]
        self.assertIn("aa", texts)
        self.assertIn("aaa", texts)
    
    def test_empty_string(self):
        """Test empty string."""
        palindromes = find_all_palindromes("")
        self.assertEqual(len(palindromes), 0)
    
    def test_no_palindromes(self):
        """Test string with no palindromes of min length."""
        palindromes = find_all_palindromes("abc")
        self.assertEqual(len(palindromes), 0)
    
    def test_positions(self):
        """Test that positions are correct."""
        palindromes = find_all_palindromes("aba")
        for p in palindromes:
            # Verify position matches text
            self.assertEqual(p.text, "aba"[p.start:p.end])
            self.assertEqual(p.length, p.end - p.start)
    
    def test_case_insensitive(self):
        """Test case-insensitive finding."""
        palindromes = find_all_palindromes("ABA", case_sensitive=False)
        texts = [p.text for p in palindromes]
        self.assertIn("ABA", texts)
    
    def test_case_sensitive(self):
        """Test case-sensitive finding."""
        palindromes = find_all_palindromes("ABA", case_sensitive=True)
        # 'ABA' IS a palindrome in case-sensitive mode (A==A, B==B, A==A)
        self.assertEqual(len(palindromes), 1)
        self.assertEqual(palindromes[0].text, "ABA")
        
        # But 'ABC' is not
        palindromes = find_all_palindromes("ABC", case_sensitive=True)
        self.assertEqual(len(palindromes), 0)


class TestFindLongestPalindrome(unittest.TestCase):
    """Test find_longest_palindrome function."""
    
    def test_basic_longest(self):
        """Test basic longest palindrome finding."""
        longest = find_longest_palindrome("babad")
        self.assertIsNotNone(longest)
        # Could be "bab" or "aba"
        self.assertIn(longest.text, ["bab", "aba"])
    
    def test_even_length(self):
        """Test even-length palindrome."""
        longest = find_longest_palindrome("cbbd")
        self.assertIsNotNone(longest)
        self.assertEqual(longest.text, "bb")
    
    def test_full_string_palindrome(self):
        """Test when full string is palindrome."""
        longest = find_longest_palindrome("racecar")
        self.assertIsNotNone(longest)
        self.assertEqual(longest.text, "racecar")
        self.assertEqual(longest.length, 7)
    
    def test_no_palindrome(self):
        """Test string with no palindrome of length > 1."""
        longest = find_longest_palindrome("abc")
        # Single characters are palindromes, so returns first char
        self.assertIsNotNone(longest)
        self.assertEqual(longest.text, "a")
        self.assertEqual(longest.length, 1)
    
    def test_empty_string(self):
        """Test empty string."""
        longest = find_longest_palindrome("")
        self.assertIsNone(longest)


class TestCountPalindromes(unittest.TestCase):
    """Test count_palindromes function."""
    
    def test_basic_count(self):
        """Test basic palindrome counting."""
        # "aaa" has "aa" (positions 0-1), "aa" (positions 1-2), "aaa" (positions 0-2)
        count = count_palindromes("aaa")
        self.assertEqual(count, 3)
    
    def test_unique_count(self):
        """Test unique palindrome counting."""
        count = count_palindromes("aaa", unique=True)
        # With unique=True, we check by (text, start, end) tuple
        # So "aaa" at 0-3, "aa" at 0-2, "aa" at 1-3 are all considered different
        self.assertEqual(count, 3)
    
    def test_no_palindromes(self):
        """Test string with no palindromes."""
        count = count_palindromes("abc")
        self.assertEqual(count, 0)


class TestFindPalindromicSubsequences(unittest.TestCase):
    """Test find_palindromic_subsequences function."""
    
    def test_basic_subsequences(self):
        """Test basic subsequences."""
        subsequences = find_palindromic_subsequences("abc")
        self.assertIn("a", subsequences)
        self.assertIn("b", subsequences)
        self.assertIn("c", subsequences)
    
    def test_repeated_chars(self):
        """Test string with repeated characters."""
        subsequences = find_palindromic_subsequences("aaa")
        self.assertIn("a", subsequences)
        self.assertIn("aa", subsequences)
        self.assertIn("aaa", subsequences)
    
    def test_palindrome_string(self):
        """Test palindrome string."""
        subsequences = find_palindromic_subsequences("aba")
        self.assertIn("a", subsequences)
        self.assertIn("b", subsequences)
        self.assertIn("aba", subsequences)
    
    def test_empty_string(self):
        """Test empty string."""
        subsequences = find_palindromic_subsequences("")
        self.assertEqual(len(subsequences), 0)


class TestMinInsertionsToPalindrome(unittest.TestCase):
    """Test min_insertions_to_palindrome function."""
    
    def test_basic_insertions(self):
        """Test basic insertion calculations."""
        self.assertEqual(min_insertions_to_palindrome("ab"), 1)
        self.assertEqual(min_insertions_to_palindrome("abc"), 2)
        self.assertEqual(min_insertions_to_palindrome("abcd"), 3)
    
    def test_already_palindrome(self):
        """Test string that's already palindrome."""
        self.assertEqual(min_insertions_to_palindrome("racecar"), 0)
        self.assertEqual(min_insertions_to_palindrome("aba"), 0)
    
    def test_google(self):
        """Test specific example."""
        self.assertEqual(min_insertions_to_palindrome("google"), 2)
    
    def test_empty_string(self):
        """Test empty string."""
        self.assertEqual(min_insertions_to_palindrome(""), 0)
    
    def test_single_char(self):
        """Test single character."""
        self.assertEqual(min_insertions_to_palindrome("a"), 0)


class TestMakePalindrome(unittest.TestCase):
    """Test make_palindrome function."""
    
    def test_basic_make(self):
        """Test basic palindrome creation."""
        result = make_palindrome("abc")
        self.assertEqual(result, "abcba")
        self.assertTrue(is_palindrome(result))
    
    def test_already_palindrome(self):
        """Test string that's already palindrome."""
        result = make_palindrome("racecar")
        self.assertEqual(result, "racecar")
    
    def test_two_chars(self):
        """Test two character string."""
        result = make_palindrome("ab")
        self.assertEqual(result, "aba")
        self.assertTrue(is_palindrome(result))
    
    def test_empty_string(self):
        """Test empty string."""
        result = make_palindrome("")
        self.assertEqual(result, "")


class TestFindPalindromePairs(unittest.TestCase):
    """Test find_palindrome_pairs function."""
    
    def test_basic_pairs(self):
        """Test basic pair finding."""
        pairs = find_palindrome_pairs(["abcd", "dcba", "lls", "s", "sssll"])
        self.assertIn((0, 1), pairs)  # "abcd" + "dcba" = "abcddcba" (palindrome)
        self.assertIn((1, 0), pairs)  # "dcba" + "abcd" = "dcbaabcd" (palindrome)
    
    def test_bat_tab(self):
        """Test bat/tab example."""
        pairs = find_palindrome_pairs(["bat", "tab", "cat"])
        self.assertIn((0, 1), pairs)  # "bat" + "tab" = "battab"
        self.assertIn((1, 0), pairs)  # "tab" + "bat" = "tabbat"
    
    def test_empty_list(self):
        """Test empty list."""
        pairs = find_palindrome_pairs([])
        self.assertEqual(len(pairs), 0)
    
    def test_single_word(self):
        """Test single word list."""
        pairs = find_palindrome_pairs(["a"])
        self.assertEqual(len(pairs), 0)


class TestIsPalindromeNumber(unittest.TestCase):
    """Test is_palindrome_number function."""
    
    def test_palindrome_numbers(self):
        """Test palindrome numbers."""
        self.assertTrue(is_palindrome_number(121))
        self.assertTrue(is_palindrome_number(12321))
        self.assertTrue(is_palindrome_number(123454321))
        self.assertTrue(is_palindrome_number(1))
        self.assertTrue(is_palindrome_number(0))
        self.assertTrue(is_palindrome_number(11))
        self.assertTrue(is_palindrome_number(22))
    
    def test_non_palindrome_numbers(self):
        """Test non-palindrome numbers."""
        self.assertFalse(is_palindrome_number(123))
        self.assertFalse(is_palindrome_number(10))
        self.assertFalse(is_palindrome_number(100))
        self.assertFalse(is_palindrome_number(12345))
    
    def test_negative_numbers(self):
        """Test negative numbers."""
        self.assertFalse(is_palindrome_number(-121))
        self.assertFalse(is_palindrome_number(-1))
    
    def test_large_numbers(self):
        """Test large palindrome numbers."""
        self.assertTrue(is_palindrome_number(12345678987654321))
        self.assertFalse(is_palindrome_number(12345678901234567))


class TestGeneratePalindromes(unittest.TestCase):
    """Test generate_palindromes function."""
    
    def test_length_1(self):
        """Test length 1 generation."""
        palindromes = generate_palindromes(1, "ab")
        self.assertEqual(sorted(palindromes), ["a", "b"])
    
    def test_length_2(self):
        """Test length 2 generation."""
        palindromes = generate_palindromes(2, "ab")
        self.assertEqual(sorted(palindromes), ["aa", "bb"])
    
    def test_length_3(self):
        """Test length 3 generation."""
        palindromes = generate_palindromes(3, "ab")
        self.assertEqual(sorted(palindromes), ["aaa", "aba", "bab", "bbb"])
    
    def test_empty_charset(self):
        """Test empty charset."""
        palindromes = generate_palindromes(1, "")
        self.assertEqual(len(palindromes), 0)
    
    def test_invalid_length(self):
        """Test invalid length."""
        palindromes = generate_palindromes(0, "ab")
        self.assertEqual(len(palindromes), 0)
        palindromes = generate_palindromes(-1, "ab")
        self.assertEqual(len(palindromes), 0)


class TestLongestPalindromicSubsequenceLength(unittest.TestCase):
    """Test longest_palindromic_subsequence_length function."""
    
    def test_basic_subsequence(self):
        """Test basic subsequence length."""
        self.assertEqual(longest_palindromic_subsequence_length("bbbab"), 4)
        self.assertEqual(longest_palindromic_subsequence_length("cbbd"), 2)
    
    def test_single_char(self):
        """Test single character."""
        self.assertEqual(longest_palindromic_subsequence_length("a"), 1)
    
    def test_all_same(self):
        """Test all same characters."""
        self.assertEqual(longest_palindromic_subsequence_length("aaa"), 3)
    
    def test_palindrome_string(self):
        """Test palindrome string."""
        self.assertEqual(longest_palindromic_subsequence_length("aba"), 3)
        self.assertEqual(longest_palindromic_subsequence_length("racecar"), 7)
    
    def test_empty_string(self):
        """Test empty string."""
        self.assertEqual(longest_palindromic_subsequence_length(""), 0)


class TestGetPalindromeInfo(unittest.TestCase):
    """Test get_palindrome_info function."""
    
    def test_basic_info(self):
        """Test basic palindrome info."""
        info = get_palindrome_info("racecar")
        self.assertTrue(info['is_palindrome'])
        self.assertEqual(info['longest_palindrome'], "racecar")
        self.assertEqual(info['min_insertions_for_palindrome'], 0)
        self.assertEqual(info['longest_palindromic_subsequence'], 7)
    
    def test_non_palindrome_info(self):
        """Test non-palindrome info."""
        info = get_palindrome_info("hello")
        self.assertFalse(info['is_palindrome'])
        self.assertEqual(info['min_insertions_for_palindrome'], 3)
    
    def test_empty_string_info(self):
        """Test empty string info."""
        info = get_palindrome_info("")
        self.assertTrue(info['is_palindrome'])
        self.assertIsNone(info['longest_palindrome'])


class TestSpecialPalindromeTypes(unittest.TestCase):
    """Test special palindrome type functions."""
    
    def test_semordnilap(self):
        """Test semordnilap detection."""
        self.assertTrue(is_semordnilap("stressed"))
        self.assertFalse(is_semordnilap("racecar"))
        self.assertTrue(is_semordnilap("dog"))
    
    def test_mirrored_palindrome(self):
        """Test mirrored palindrome detection."""
        # Characters that are vertically symmetric
        self.assertTrue(is_mirrored_palindrome("AHA"))
        self.assertTrue(is_mirrored_palindrome("ATOYOTA"))
        self.assertTrue(is_mirrored_palindrome("MOM"))
        self.assertTrue(is_mirrored_palindrome("OTTO"))
        
        # Characters that are not in the mirror map
        self.assertFalse(is_mirrored_palindrome("ABC"))
        self.assertFalse(is_mirrored_palindrome("DAD"))  # D is not in default mirror map
        self.assertFalse(is_mirrored_palindrome("IOIO"))  # Not symmetric in layout


class TestPalindromeMatch(unittest.TestCase):
    """Test PalindromeMatch dataclass."""
    
    def test_match_creation(self):
        """Test PalindromeMatch creation."""
        match = PalindromeMatch("aba", 0, 3, 3)
        self.assertEqual(match.text, "aba")
        self.assertEqual(match.start, 0)
        self.assertEqual(match.end, 3)
        self.assertEqual(match.length, 3)
    
    def test_match_repr(self):
        """Test PalindromeMatch representation."""
        match = PalindromeMatch("aba", 0, 3, 3)
        repr_str = repr(match)
        self.assertIn("aba", repr_str)
        self.assertIn("pos=0-3", repr_str)


def run_tests():
    """Run all tests."""
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromModule(sys.modules[__name__])
    
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    return result


if __name__ == '__main__':
    run_tests()