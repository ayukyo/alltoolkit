#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Tests for rabin_karp_utils"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from mod import (
    RollingHash, MatchResult,
    rabin_karp_search, multi_pattern_search, find_all_occurrences,
    contains_pattern, count_occurrences, find_with_wildcards,
    find_longest_repeated_substring, find_common_substring,
    compute_similarity, detect_plagiarism, double_hash_search,
    RabinKarpMatcher, two_d_pattern_search
)

import unittest


class TestRollingHash(unittest.TestCase):
    def test_compute(self):
        roller = RollingHash()
        h = roller.compute("hello")
        self.assertIsInstance(h, int)
        self.assertTrue(h >= 0)

    def test_slide(self):
        roller = RollingHash()
        roller.compute("abc")
        new_hash = roller.slide("a", "d", 3)
        self.assertIsInstance(new_hash, int)


class TestMatchResult(unittest.TestCase):
    def test_repr(self):
        result = MatchResult(0, "test", 4)
        self.assertIn("MatchResult", repr(result))
        self.assertEqual(result.index, 0)
        self.assertEqual(result.pattern, "test")


class TestRabinKarpSearch(unittest.TestCase):
    def test_basic_search(self):
        text = "abracadabra"
        pattern = "abra"
        results = rabin_karp_search(text, pattern)
        self.assertIn(0, results)
        self.assertIn(7, results)

    def test_no_match(self):
        text = "hello world"
        pattern = "xyz"
        results = rabin_karp_search(text, pattern)
        self.assertEqual(results, [])

    def test_empty_text(self):
        results = rabin_karp_search("", "pattern")
        self.assertEqual(results, [])

    def test_empty_pattern(self):
        results = rabin_karp_search("text", "")
        self.assertEqual(results, [])

    def test_pattern_longer_than_text(self):
        results = rabin_karp_search("abc", "abcdef")
        self.assertEqual(results, [])

    def test_full_match(self):
        text = "hello"
        pattern = "hello"
        results = rabin_karp_search(text, pattern)
        self.assertEqual(results, [0])

    def test_single_char_pattern(self):
        text = "hello"
        pattern = "l"
        results = rabin_karp_search(text, pattern)
        self.assertIn(2, results)
        self.assertIn(3, results)


class TestMultiPatternSearch(unittest.TestCase):
    def test_multi_pattern(self):
        text = "hello world"
        patterns = ["lo", "wor", "ld"]
        results = multi_pattern_search(text, patterns)
        self.assertEqual(len(results), 3)
        indices = [r.index for r in results]
        self.assertIn(3, indices)
        self.assertIn(6, indices)
        self.assertIn(9, indices)

    def test_multi_pattern_no_match(self):
        text = "hello"
        patterns = ["xyz", "abc"]
        results = multi_pattern_search(text, patterns)
        self.assertEqual(results, [])

    def test_multi_pattern_empty_patterns(self):
        results = multi_pattern_search("hello", [])
        self.assertEqual(results, [])


class TestFindAllOccurrences(unittest.TestCase):
    def test_find_all(self):
        text = "banana"
        pattern = "ana"
        results = find_all_occurrences(text, pattern)
        self.assertEqual(len(results), 2)
        self.assertEqual(results[0].index, 1)
        self.assertEqual(results[1].index, 3)


class TestContainsPattern(unittest.TestCase):
    def test_contains_true(self):
        self.assertTrue(contains_pattern("hello world", "world"))

    def test_contains_false(self):
        self.assertFalse(contains_pattern("hello world", "xyz"))


class TestCountOccurrences(unittest.TestCase):
    def test_count(self):
        self.assertEqual(count_occurrences("banana", "ana"), 2)

    def test_count_no_match(self):
        self.assertEqual(count_occurrences("hello", "xyz"), 0)


class TestFindWithWildcards(unittest.TestCase):
    def test_wildcard_match(self):
        results = find_with_wildcards("hello", "h?llo")
        self.assertIn(0, results)

    def test_no_wildcard_match(self):
        results = find_with_wildcards("hello", "h?xyz")
        self.assertEqual(results, [])

    def test_no_wildcards_falls_back(self):
        results = find_with_wildcards("hello", "hello")
        self.assertIn(0, results)


class TestFindLongestRepeatedSubstring(unittest.TestCase):
    def test_banana(self):
        result = find_longest_repeated_substring("banana")
        self.assertIsNotNone(result)
        substring, positions = result
        self.assertEqual(substring, "ana")
        self.assertIn(1, positions)
        self.assertIn(3, positions)

    def test_no_repeat(self):
        result = find_longest_repeated_substring("abc")
        self.assertIsNone(result)


class TestFindCommonSubstring(unittest.TestCase):
    def test_common_substring(self):
        result = find_common_substring(["programming", "programmer", "program"])
        self.assertEqual(result, "program")

    def test_no_common(self):
        result = find_common_substring(["abc", "def"])
        self.assertIsNone(result)


class TestComputeSimilarity(unittest.TestCase):
    def test_identical_texts(self):
        similarity = compute_similarity("hello", "hello")
        self.assertEqual(similarity, 1.0)

    def test_different_texts(self):
        similarity = compute_similarity("hello", "world")
        self.assertTrue(0.0 <= similarity <= 1.0)

    def test_empty_text(self):
        similarity = compute_similarity("", "hello")
        self.assertEqual(similarity, 0.0)


class TestDetectPlagiarism(unittest.TestCase):
    def test_detect_similar(self):
        docs = ["Hello world", "Hello there", "Completely different"]
        results = detect_plagiarism(docs, threshold=0.2, k=3)
        self.assertGreaterEqual(len(results), 1)

    def test_no_plagiarism(self):
        docs = ["abc def", "ghi jkl"]
        results = detect_plagiarism(docs, threshold=0.9)
        self.assertEqual(results, [])


class TestDoubleHashSearch(unittest.TestCase):
    def test_double_hash(self):
        text = "abracadabra"
        pattern = "abra"
        results = double_hash_search(text, pattern)
        self.assertIn(0, results)
        self.assertIn(7, results)

    def test_double_hash_no_match(self):
        results = double_hash_search("hello", "xyz")
        self.assertEqual(results, [])


class TestRabinKarpMatcher(unittest.TestCase):
    def test_matcher_init(self):
        patterns = ["hello", "world"]
        matcher = RabinKarpMatcher(patterns)
        self.assertEqual(len(matcher.patterns), 2)

    def test_matcher_search(self):
        patterns = ["hello", "world"]
        matcher = RabinKarpMatcher(patterns)
        results = matcher.search("hello world")
        self.assertGreaterEqual(len(results), 1)

    def test_matcher_search_iter(self):
        patterns = ["a", "b"]
        matcher = RabinKarpMatcher(patterns)
        results = list(matcher.search_iter("abc"))
        self.assertGreaterEqual(len(results), 2)

    def test_add_pattern(self):
        matcher = RabinKarpMatcher(["hello"])
        matcher.add_pattern("world")
        self.assertEqual(len(matcher.patterns), 2)

    def test_remove_pattern(self):
        matcher = RabinKarpMatcher(["hello", "world"])
        matcher.remove_pattern("hello")
        self.assertNotIn("hello", matcher.patterns)


class TestTwoDPatternSearch(unittest.TestCase):
    def test_2d_pattern(self):
        text_grid = ["abcde", "fghij", "klmno"]
        pattern_grid = ["ghi", "lmn"]
        results = two_d_pattern_search(text_grid, pattern_grid)
        self.assertIn((1, 1), results)

    def test_2d_no_match(self):
        text_grid = ["abcde", "fghij"]
        pattern_grid = ["xyz", "uvw"]
        results = two_d_pattern_search(text_grid, pattern_grid)
        self.assertEqual(results, [])


if __name__ == "__main__":
    unittest.main()