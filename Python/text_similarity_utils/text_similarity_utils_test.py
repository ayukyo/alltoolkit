#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AllToolkit - Text Similarity Utilities Test Module

Comprehensive tests for all text similarity functions.

Author: AllToolkit Contributors
License: MIT
"""

import unittest
import math
from mod import (
    levenshtein_distance, levenshtein_ratio,
    damerau_levenshtein_distance,
    hamming_distance, hamming_ratio,
    jaro_similarity, jaro_winkler_similarity,
    jaccard_similarity, dice_coefficient, overlap_coefficient,
    cosine_similarity, cosine_similarity_words,
    TFIDFCalculator,
    lcs_length, lcs, lcs_ratio,
    ngram_similarity,
    soundex, metaphone, phonetic_similarity,
    find_best_match, find_all_matches, fuzzy_search,
    combined_similarity, compare_strings,
    similar
)


class TestLevenshteinDistance(unittest.TestCase):
    """Tests for Levenshtein distance functions."""
    
    def test_identical_strings(self):
        self.assertEqual(levenshtein_distance("", ""), 0)
        self.assertEqual(levenshtein_distance("hello", "hello"), 0)
    
    def test_empty_strings(self):
        self.assertEqual(levenshtein_distance("", "hello"), 5)
        self.assertEqual(levenshtein_distance("hello", ""), 5)
    
    def test_single_insertion(self):
        self.assertEqual(levenshtein_distance("hello", "hell"), 1)
        self.assertEqual(levenshtein_distance("hell", "hello"), 1)
    
    def test_single_deletion(self):
        self.assertEqual(levenshtein_distance("hello", "helo"), 1)
    
    def test_single_substitution(self):
        self.assertEqual(levenshtein_distance("hello", "hallo"), 1)
    
    def test_multiple_edits(self):
        self.assertEqual(levenshtein_distance("kitten", "sitting"), 3)
        self.assertEqual(levenshtein_distance("saturday", "sunday"), 3)
    
    def test_case_sensitivity(self):
        self.assertEqual(levenshtein_distance("Hello", "hello", case_sensitive=True), 1)
        self.assertEqual(levenshtein_distance("Hello", "hello", case_sensitive=False), 0)
    
    def test_ratio_identical(self):
        self.assertEqual(levenshtein_ratio("hello", "hello"), 1.0)
    
    def test_ratio_empty(self):
        self.assertEqual(levenshtein_ratio("", ""), 1.0)
        self.assertEqual(levenshtein_ratio("", "hello"), 0.0)
    
    def test_ratio_partial(self):
        ratio = levenshtein_ratio("hello", "hallo")
        self.assertAlmostEqual(ratio, 0.8, places=2)


class TestDamerauLevenshtein(unittest.TestCase):
    """Tests for Damerau-Levenshtein distance."""
    
    def test_identical_strings(self):
        self.assertEqual(damerau_levenshtein_distance("abc", "abc"), 0)
    
    def test_transposition(self):
        # Transposition of adjacent characters counts as 1
        self.assertEqual(damerau_levenshtein_distance("ab", "ba"), 1)
        self.assertEqual(damerau_levenshtein_distance("abc", "acb"), 1)
    
    def test_vs_levenshtein(self):
        # Regular Levenshtein would give 2 for this
        # Damerau-Levenshtein should give 1 (transposition)
        self.assertEqual(damerau_levenshtein_distance("ca", "ac"), 1)
    
    def test_multiple_edits(self):
        self.assertEqual(damerau_levenshtein_distance("abcd", "acbd"), 1)


class TestHammingDistance(unittest.TestCase):
    """Tests for Hamming distance functions."""
    
    def test_identical_strings(self):
        self.assertEqual(hamming_distance("hello", "hello"), 0)
    
    def test_single_difference(self):
        self.assertEqual(hamming_distance("hello", "hallo"), 1)
    
    def test_multiple_differences(self):
        self.assertEqual(hamming_distance("karolin", "kathrin"), 3)
    
    def test_different_lengths_raises(self):
        with self.assertRaises(ValueError):
            hamming_distance("hello", "hi")
    
    def test_ratio(self):
        ratio = hamming_ratio("karolin", "kathrin")
        self.assertAlmostEqual(ratio, 4/7, places=2)


class TestJaroSimilarity(unittest.TestCase):
    """Tests for Jaro and Jaro-Winkler similarity."""
    
    def test_identical_strings(self):
        self.assertEqual(jaro_similarity("hello", "hello"), 1.0)
        self.assertEqual(jaro_winkler_similarity("hello", "hello"), 1.0)
    
    def test_empty_strings(self):
        self.assertEqual(jaro_similarity("", ""), 1.0)
        self.assertEqual(jaro_similarity("", "hello"), 0.0)
    
    def test_no_match(self):
        self.assertEqual(jaro_similarity("abc", "xyz"), 0.0)
    
    def test_partial_match(self):
        jaro = jaro_similarity("MARTHA", "MARHTA")
        self.assertGreater(jaro, 0.9)
        self.assertLess(jaro, 1.0)
    
    def test_jaro_winkler_bonus(self):
        # Jaro-Winkler should give higher scores for matching prefixes
        jaro = jaro_similarity("MARTHA", "MARHTA")
        jw = jaro_winkler_similarity("MARTHA", "MARHTA")
        self.assertGreater(jw, jaro)
    
    def test_scaling_factor_validation(self):
        with self.assertRaises(ValueError):
            jaro_winkler_similarity("a", "b", p=0.3)  # p > 0.25
    
    def test_case_sensitivity(self):
        jw1 = jaro_winkler_similarity("Hello", "hello", case_sensitive=True)
        jw2 = jaro_winkler_similarity("Hello", "hello", case_sensitive=False)
        self.assertLess(jw1, 1.0)
        self.assertEqual(jw2, 1.0)


class TestSetBasedSimilarity(unittest.TestCase):
    """Tests for Jaccard, Dice, and Overlap coefficients."""
    
    def test_jaccard_identical(self):
        self.assertEqual(jaccard_similarity("hello", "hello"), 1.0)
    
    def test_jaccard_no_overlap(self):
        self.assertEqual(jaccard_similarity("abc", "xyz"), 0.0)
    
    def test_jaccard_partial(self):
        # 'hello' -> {h, e, l, o} (l is one char)
        # 'hallo' -> {h, a, l, o}
        # intersection -> {h, l, o} = 3
        # union -> {h, e, l, o, a} = 5
        jaccard = jaccard_similarity("hello", "hallo")
        self.assertAlmostEqual(jaccard, 3/5, places=2)
    
    def test_jaccard_ngram(self):
        jaccard = jaccard_similarity("hello", "hallo", ngram=2)
        self.assertGreater(jaccard, 0)
        self.assertLess(jaccard, 1)
    
    def test_dice_identical(self):
        self.assertEqual(dice_coefficient("hello", "hello"), 1.0)
    
    def test_dice_no_overlap(self):
        self.assertEqual(dice_coefficient("abc", "xyz"), 0.0)
    
    def test_dice_vs_jaccard(self):
        # Dice should generally give higher scores than Jaccard
        jaccard = jaccard_similarity("hello", "hallo", ngram=2)
        dice = dice_coefficient("hello", "hallo", ngram=2)
        # Both should be positive
        self.assertGreater(jaccard, 0)
        self.assertGreater(dice, 0)
    
    def test_overlap_coefficient(self):
        # When one set is subset of another, overlap = 1
        overlap = overlap_coefficient("ab", "abc")
        self.assertEqual(overlap, 1.0)


class TestCosineSimilarity(unittest.TestCase):
    """Tests for Cosine similarity."""
    
    def test_identical_strings(self):
        self.assertEqual(cosine_similarity("hello world", "hello world"), 1.0)
    
    def test_empty_strings(self):
        self.assertEqual(cosine_similarity("", ""), 1.0)
        self.assertEqual(cosine_similarity("", "hello"), 0.0)
    
    def test_no_overlap(self):
        self.assertEqual(cosine_similarity("abc", "xyz"), 0.0)
    
    def test_word_order_independence(self):
        # Word vectors should be order-independent
        sim = cosine_similarity_words("hello world", "world hello")
        self.assertAlmostEqual(sim, 1.0, places=5)
    
    def test_partial_overlap(self):
        sim = cosine_similarity("the quick brown fox", "quick brown fox")
        self.assertGreater(sim, 0.8)


class TestTFIDF(unittest.TestCase):
    """Tests for TF-IDF calculator."""
    
    def test_single_document(self):
        calc = TFIDFCalculator()
        calc.add_document("hello world")
        # Comparing a query that shares words with the document
        sim = calc.similarity("hello", "world")
        # With only one doc, the IDF is low, but there should be some similarity
        self.assertGreaterEqual(sim, 0)
    
    def test_multiple_documents(self):
        calc = TFIDFCalculator()
        calc.add_document("the quick brown fox")
        calc.add_document("the lazy dog")
        calc.add_document("quick brown fox jumps")
        
        # Comparing terms that have different IDF values
        # 'lazy' and 'dog' appear in only one document, so they have high IDF
        sim1 = calc.similarity("lazy dog", "the lazy")
        self.assertGreater(sim1, 0.3)
        
        # Common terms should still have some similarity via TF component
        sim2 = calc.similarity("jumps fox", "fox jumps")
        self.assertGreater(sim2, 0.5)
    
    def test_clear(self):
        calc = TFIDFCalculator()
        calc.add_document("test")
        calc.clear()
        self.assertEqual(len(calc.documents), 0)


class TestLCS(unittest.TestCase):
    """Tests for Longest Common Subsequence."""
    
    def test_identical_strings(self):
        self.assertEqual(lcs("hello", "hello"), "hello")
        self.assertEqual(lcs_length("hello", "hello"), 5)
    
    def test_empty_strings(self):
        self.assertEqual(lcs("", ""), "")
        self.assertEqual(lcs_length("", ""), 0)
        self.assertEqual(lcs("hello", ""), "")
    
    def test_no_common(self):
        self.assertEqual(lcs("abc", "xyz"), "")
    
    def test_partial_common(self):
        self.assertEqual(lcs_length("ABCBDAB", "BDCABA"), 4)
        result = lcs("ABCBDAB", "BDCABA")
        self.assertEqual(len(result), 4)
    
    def test_ratio(self):
        ratio = lcs_ratio("hello", "hallo")
        self.assertGreater(ratio, 0.6)


class TestNGramSimilarity(unittest.TestCase):
    """Tests for n-gram similarity."""
    
    def test_identical_strings(self):
        self.assertEqual(ngram_similarity("hello", "hello"), 1.0)
    
    def test_empty_strings(self):
        self.assertEqual(ngram_similarity("", ""), 1.0)
    
    def test_short_strings(self):
        # Strings shorter than n should fall back to character comparison
        sim = ngram_similarity("ab", "ac", n=3)
        self.assertGreater(sim, 0)
    
    def test_different_ngram_sizes(self):
        sim2 = ngram_similarity("hello", "hallo", n=2)
        sim3 = ngram_similarity("hello", "hallo", n=3)
        self.assertIsInstance(sim2, float)
        self.assertIsInstance(sim3, float)


class TestPhonetic(unittest.TestCase):
    """Tests for phonetic algorithms."""
    
    def test_soundex_basic(self):
        self.assertEqual(len(soundex("Robert")), 4)
        self.assertTrue(soundex("Robert").startswith("R"))
    
    def test_soundex_similar_names(self):
        # Robert and Rupert should have same Soundex
        self.assertEqual(soundex("Robert"), soundex("Rupert"))
    
    def test_soundex_empty(self):
        self.assertEqual(soundex(""), "0000")
    
    def test_metaphone_basic(self):
        self.assertIsInstance(metaphone("Smith"), str)
    
    def test_metaphone_similar_names(self):
        # Check that similar sounding names produce similar codes
        m1 = metaphone("Smith")
        m2 = metaphone("Schmidt")
        # Both should have similar phonetic representations
        self.assertIsInstance(m1, str)
        self.assertIsInstance(m2, str)
    
    def test_phonetic_similarity_soundex(self):
        sim = phonetic_similarity("Robert", "Rupert", algorithm="soundex")
        self.assertEqual(sim, 1.0)
    
    def test_phonetic_similarity_invalid_algorithm(self):
        with self.assertRaises(ValueError):
            phonetic_similarity("a", "b", algorithm="invalid")


class TestFuzzyMatching(unittest.TestCase):
    """Tests for fuzzy matching utilities."""
    
    def test_find_best_match(self):
        choices = ["apple", "orange", "banana"]
        match, score = find_best_match("appel", choices)
        self.assertEqual(match, "apple")
        self.assertGreater(score, 0.9)
    
    def test_find_best_match_threshold(self):
        choices = ["xyz", "abc"]
        match, score = find_best_match("hello", choices, threshold=0.5)
        # If no match above threshold, returns empty
        self.assertEqual(match, "")
        self.assertEqual(score, 0.0)
    
    def test_find_best_match_empty_choices(self):
        match, score = find_best_match("test", [])
        self.assertEqual(match, "")
        self.assertEqual(score, 0.0)
    
    def test_find_all_matches(self):
        choices = ["apple", "apple pie", "orange", "banana"]
        matches = find_all_matches("apple", choices, threshold=0.5)
        self.assertGreater(len(matches), 0)
        # Should be sorted by score
        scores = [m[1] for m in matches]
        self.assertEqual(scores, sorted(scores, reverse=True))
    
    def test_find_all_matches_no_results(self):
        choices = ["xyz", "abc"]
        matches = find_all_matches("hello", choices, threshold=0.9)
        self.assertEqual(len(matches), 0)
    
    def test_fuzzy_search(self):
        text = "I like appel pie and aple juice"
        matches = fuzzy_search("apple", text, threshold=0.6)
        self.assertGreater(len(matches), 0)
        # Check that we got positions
        for match in matches:
            start, end, word, score = match
            self.assertGreaterEqual(score, 0.6)
            self.assertEqual(text[start:end], word)


class TestCombinedSimilarity(unittest.TestCase):
    """Tests for combined and composite similarity."""
    
    def test_combined_identical(self):
        sim = combined_similarity("hello", "hello")
        self.assertEqual(sim, 1.0)
    
    def test_combined_empty(self):
        sim = combined_similarity("", "")
        self.assertEqual(sim, 1.0)
    
    def test_combined_custom_weights(self):
        weights = {
            'levenshtein': 1.0,
            'jaro_winkler': 0.0,
            'jaccard': 0.0,
            'cosine': 0.0
        }
        sim = combined_similarity("hello", "hallo", weights=weights)
        self.assertAlmostEqual(sim, 0.8, places=2)
    
    def test_compare_strings(self):
        result = compare_strings("hello", "hallo")
        
        self.assertIn('levenshtein', result)
        self.assertIn('jaro', result)
        self.assertIn('jaro_winkler', result)
        self.assertIn('jaccard_char', result)
        self.assertIn('dice', result)
        self.assertIn('cosine_bigram', result)
        self.assertIn('lcs', result)
        self.assertIn('combined', result)
        
        # All scores should be between 0 and 1
        for key, value in result.items():
            self.assertGreaterEqual(value, 0.0, f"{key} < 0")
            self.assertLessEqual(value, 1.0, f"{key} > 1")


class TestSimilarFunction(unittest.TestCase):
    """Tests for the similar() convenience function."""
    
    def test_similar_true(self):
        self.assertTrue(similar("hello", "hallo", threshold=0.7))
    
    def test_similar_false(self):
        self.assertFalse(similar("hello", "hallo", threshold=0.9))
    
    def test_similar_methods(self):
        methods = ['levenshtein', 'jaro', 'jaro_winkler', 'jaccard', 'dice', 'cosine', 'lcs']
        for method in methods:
            result = similar("hello", "hallo", threshold=0.5, method=method)
            self.assertIsInstance(result, bool, f"Method {method} failed")
    
    def test_similar_invalid_method(self):
        with self.assertRaises(ValueError):
            similar("a", "b", method="invalid")


class TestEdgeCases(unittest.TestCase):
    """Test edge cases and boundary conditions."""
    
    def test_unicode_strings(self):
        sim = jaro_similarity("café", "cafe")
        self.assertGreater(sim, 0.8)
    
    def test_whitespace_handling(self):
        sim = jaccard_similarity("hello world", "helloworld")
        self.assertGreater(sim, 0.5)
    
    def test_very_long_strings(self):
        s1 = "a" * 1000
        s2 = "a" * 999 + "b"
        dist = levenshtein_distance(s1, s2)
        self.assertEqual(dist, 1)
    
    def test_numbers_in_strings(self):
        sim = jaro_winkler_similarity("test123", "test456")
        self.assertGreater(sim, 0.7)
    
    def test_special_characters(self):
        sim = dice_coefficient("hello!", "hello?", ngram=2)
        self.assertGreater(sim, 0.7)


if __name__ == "__main__":
    unittest.main(verbosity=2)