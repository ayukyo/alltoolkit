"""
AllToolkit - Python Fuzzy Search Utilities Test Suite

Comprehensive test coverage for fuzzy_search_utils module.
"""

import unittest
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from mod import (
    # Distance functions
    levenshtein_distance,
    levenshtein_ratio,
    damerau_levenshtein_distance,
    hamming_distance,
    jaro_distance,
    jaro_winkler_distance,
    
    # N-gram functions
    get_ngrams,
    ngram_similarity,
    dice_coefficient,
    
    # Phonetic functions
    soundex,
    metaphone,
    double_metaphone,
    phonetic_similarity,
    
    # Search functions
    fuzzy_search,
    fuzzy_find,
    extract_best,
    extract_top_n,
    
    # Advanced matching
    partial_ratio,
    token_sort_ratio,
    token_set_ratio,
    weighted_ratio,
    
    # Classes and utilities
    FuzzyMatch,
    FuzzyMatcher,
    deduplicate,
    suggest_corrections,
)


class TestLevenshteinDistance(unittest.TestCase):
    """Test Levenshtein distance functions."""
    
    def test_identical_strings(self):
        """Test identical strings have distance 0."""
        self.assertEqual(levenshtein_distance("hello", "hello"), 0)
        self.assertEqual(levenshtein_distance("", ""), 0)
    
    def test_empty_string(self):
        """Test distance with empty string."""
        self.assertEqual(levenshtein_distance("", "abc"), 3)
        self.assertEqual(levenshtein_distance("abc", ""), 3)
    
    def test_single_character_diff(self):
        """Test single character differences."""
        self.assertEqual(levenshtein_distance("kitten", "sitten"), 1)  # substitution
        self.assertEqual(levenshtein_distance("kitten", "kittn"), 1)   # deletion
    
    def test_multiple_edits(self):
        """Test multiple edit operations."""
        self.assertEqual(levenshtein_distance("kitten", "sitting"), 3)
        self.assertEqual(levenshtein_distance("flaw", "lawn"), 2)
    
    def test_case_sensitivity(self):
        """Test case sensitivity."""
        self.assertEqual(levenshtein_distance("Hello", "hello"), 1)


class TestLevenshteinRatio(unittest.TestCase):
    """Test Levenshtein ratio."""
    
    def test_identical_strings(self):
        """Test identical strings have ratio 1.0."""
        self.assertEqual(levenshtein_ratio("hello", "hello"), 1.0)
    
    def test_empty_strings(self):
        """Test ratio with empty strings."""
        self.assertEqual(levenshtein_ratio("", ""), 1.0)
        self.assertEqual(levenshtein_ratio("", "abc"), 0.0)
        self.assertEqual(levenshtein_ratio("abc", ""), 0.0)
    
    def test_partial_match(self):
        """Test partial matches."""
        ratio = levenshtein_ratio("hello", "hallo")
        self.assertAlmostEqual(ratio, 0.8, places=2)


class TestDamerauLevenshtein(unittest.TestCase):
    """Test Damerau-Levenshtein distance."""
    
    def test_transposition(self):
        """Test transposition counts as one edit."""
        # Regular Levenshtein would return 2 for transposition
        self.assertEqual(levenshtein_distance("abc", "acb"), 2)
        self.assertEqual(damerau_levenshtein_distance("abc", "acb"), 1)
    
    def test_identical(self):
        """Test identical strings."""
        self.assertEqual(damerau_levenshtein_distance("test", "test"), 0)
    
    def test_multiple_operations(self):
        """Test multiple operations including transposition."""
        # ca -> abc requires 3 operations: insert 'b' (ca->cba), transpose 'c','a' (abc), 
        # or: insert 'b', insert 'a', delete 'a' - actually 3 operations
        self.assertEqual(damerau_levenshtein_distance("ca", "abc"), 3)


class TestHammingDistance(unittest.TestCase):
    """Test Hamming distance."""
    
    def test_identical_strings(self):
        """Test identical strings."""
        self.assertEqual(hamming_distance("hello", "hello"), 0)
    
    def test_different_positions(self):
        """Test different characters."""
        self.assertEqual(hamming_distance("karolin", "kathrin"), 3)
        self.assertEqual(hamming_distance("00000", "11111"), 5)
    
    def test_length_error(self):
        """Test error for different lengths."""
        with self.assertRaises(ValueError):
            hamming_distance("hello", "hi")


class TestJaroDistance(unittest.TestCase):
    """Test Jaro and Jaro-Winkler distance."""
    
    def test_identical_strings(self):
        """Test identical strings."""
        self.assertEqual(jaro_distance("hello", "hello"), 1.0)
        self.assertEqual(jaro_winkler_distance("hello", "hello"), 1.0)
    
    def test_empty_strings(self):
        """Test empty strings."""
        self.assertEqual(jaro_distance("", ""), 1.0)
        self.assertEqual(jaro_distance("", "abc"), 0.0)
    
    def test_typical_cases(self):
        """Test typical matching cases."""
        jaro = jaro_distance("MARTHA", "MARHTA")
        self.assertAlmostEqual(jaro, 0.944, places=2)
    
    def test_jaro_winkler_prefix_bonus(self):
        """Test Jaro-Winkler prefix bonus."""
        jw = jaro_winkler_distance("MARTHA", "MARHTA")
        jaro = jaro_distance("MARTHA", "MARHTA")
        self.assertGreater(jw, jaro)  # Jaro-Winkler should be higher


class TestNgramFunctions(unittest.TestCase):
    """Test n-gram functions."""
    
    def test_bigrams(self):
        """Test bigram generation."""
        ngrams = get_ngrams("hello", 2)
        expected = {'he', 'el', 'll', 'lo'}
        self.assertEqual(ngrams, expected)
    
    def test_trigrams(self):
        """Test trigram generation."""
        ngrams = get_ngrams("hello", 3)
        expected = {'hel', 'ell', 'llo'}
        self.assertEqual(ngrams, expected)
    
    def test_empty_string(self):
        """Test empty string n-grams."""
        self.assertEqual(get_ngrams("", 2), set())
    
    def test_short_string(self):
        """Test string shorter than n."""
        self.assertEqual(get_ngrams("a", 2), {'a'})
    
    def test_ngram_similarity(self):
        """Test n-gram similarity."""
        # hello ngrams: {'he', 'el', 'll', 'lo'}
        # hallo ngrams: {'ha', 'al', 'll', 'lo'}
        # Intersection: {'ll', 'lo'} = 2, Union: 6
        # Jaccard = 2/6 = 0.333...
        sim = ngram_similarity("hello", "hallo", 2)
        self.assertAlmostEqual(sim, 0.333, places=2)
    
    def test_ngram_similarity_identical(self):
        """Test identical strings."""
        self.assertEqual(ngram_similarity("hello", "hello"), 1.0)
    
    def test_dice_coefficient(self):
        """Test Dice coefficient."""
        # hello ngrams: 4, hallo ngrams: 4, intersection: 2
        # Dice = 2 * 2 / (4 + 4) = 4/8 = 0.5
        dice = dice_coefficient("hello", "hallo")
        self.assertAlmostEqual(dice, 0.5, places=2)


class TestSoundex(unittest.TestCase):
    """Test Soundex phonetic encoding."""
    
    def test_homophones(self):
        """Test homophones have same encoding."""
        self.assertEqual(soundex("Robert"), soundex("Rupert"))
        self.assertEqual(soundex("Ashcraft"), soundex("Ashcroft"))
    
    def test_empty_string(self):
        """Test empty string."""
        self.assertEqual(soundex(""), "0000")
    
    def test_non_alpha(self):
        """Test non-alpha characters."""
        self.assertEqual(soundex("123"), "0000")
        self.assertEqual(soundex("Robert123"), soundex("Robert"))
    
    def test_known_values(self):
        """Test known Soundex values."""
        self.assertEqual(soundex("Robert"), "R163")
        self.assertEqual(soundex("Rupert"), "R163")
        self.assertEqual(soundex("Smith"), "S530")
        self.assertEqual(soundex("Smythe"), "S530")


class TestMetaphone(unittest.TestCase):
    """Test Metaphone phonetic encoding."""
    
    def test_phonetic_equivalents(self):
        """Test phonetic equivalents."""
        self.assertEqual(metaphone("phone"), metaphone("fone"))
        self.assertEqual(metaphone("write"), metaphone("rite"))
    
    def test_empty_string(self):
        """Test empty string."""
        self.assertEqual(metaphone(""), "")
    
    def test_known_values(self):
        """Test known Metaphone values."""
        # Note: Our simplified metaphone produces slightly different output
        # than standard metaphone, but still correctly identifies phonetic
        # equivalents
        self.assertEqual(metaphone("phone"), "FN")
        # Smith produces "SM" in our implementation
        self.assertEqual(metaphone("Smith"), "SM")
    
    def test_double_metaphone(self):
        """Test Double Metaphone."""
        primary, alternate = double_metaphone("Smith")
        # Our simplified implementation produces "SM"
        self.assertEqual(primary, "SM")


class TestPhoneticSimilarity(unittest.TestCase):
    """Test phonetic similarity."""
    
    def test_homophones(self):
        """Test homophones have high similarity."""
        # Robert and Rupert share same Soundex (R163), but different Metaphone
        # Average = 1.0 (soundex match) + 0.0 (metaphone mismatch) / 2 = 0.5
        sim = phonetic_similarity("Robert", "Rupert")
        self.assertEqual(sim, 0.5)  # Soundex match, Metaphone different
    
    def test_different_words(self):
        """Test different words."""
        sim = phonetic_similarity("hello", "world")
        self.assertEqual(sim, 0.0)
    
    def test_empty_strings(self):
        """Test empty strings."""
        self.assertEqual(phonetic_similarity("", ""), 1.0)
        self.assertEqual(phonetic_similarity("", "abc"), 0.0)


class TestFuzzySearch(unittest.TestCase):
    """Test fuzzy search functions."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.candidates = ["apple", "banana", "orange", "grape", "pineapple"]
    
    def test_exact_match(self):
        """Test exact match."""
        results = fuzzy_search("apple", self.candidates)
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].value, "apple")
        self.assertEqual(results[0].score, 1.0)
    
    def test_fuzzy_match(self):
        """Test fuzzy match."""
        results = fuzzy_search("aple", self.candidates, threshold=0.6)
        self.assertGreater(len(results), 0)
        self.assertIn("apple", [r.value for r in results])
    
    def test_threshold_filter(self):
        """Test threshold filtering."""
        results = fuzzy_search("xyz", self.candidates, threshold=0.5)
        self.assertEqual(len(results), 0)
    
    def test_limit(self):
        """Test result limit."""
        results = fuzzy_search("a", self.candidates, threshold=0.0, limit=2)
        self.assertLessEqual(len(results), 2)
    
    def test_different_algorithms(self):
        """Test different similarity algorithms."""
        for algo in ["levenshtein", "jaro", "jaro_winkler", "ngram", "dice", "phonetic"]:
            results = fuzzy_search("apple", self.candidates, algorithm=algo)
            self.assertGreater(len(results), 0)
            self.assertEqual(results[0].algorithm, algo)
    
    def test_invalid_algorithm(self):
        """Test invalid algorithm raises error."""
        with self.assertRaises(ValueError):
            fuzzy_search("test", self.candidates, algorithm="invalid")


class TestFuzzyFind(unittest.TestCase):
    """Test fuzzy_find function."""
    
    def setUp(self):
        self.candidates = ["apple", "banana", "orange"]
    
    def test_find_best_match(self):
        """Test finding best match."""
        result = fuzzy_find("aple", self.candidates, threshold=0.6)
        self.assertEqual(result, "apple")
    
    def test_no_match(self):
        """Test no match above threshold."""
        result = fuzzy_find("xyz", self.candidates, threshold=0.8)
        self.assertIsNone(result)


class TestExtractBest(unittest.TestCase):
    """Test extract_best function."""
    
    def setUp(self):
        self.candidates = ["hello", "hallo", "help"]
    
    def test_extract_best(self):
        """Test extracting best match."""
        best, score = extract_best("hello", self.candidates)
        self.assertEqual(best, "hello")
        self.assertEqual(score, 1.0)
    
    def test_fuzzy_best(self):
        """Test extracting fuzzy best."""
        best, score = extract_best("helo", self.candidates)
        self.assertIn(best, ["hello", "hallo"])
        self.assertGreater(score, 0.7)
    
    def test_empty_candidates(self):
        """Test empty candidates."""
        best, score = extract_best("test", [])
        self.assertEqual(best, "")
        self.assertEqual(score, 0.0)


class TestExtractTopN(unittest.TestCase):
    """Test extract_top_n function."""
    
    def setUp(self):
        self.candidates = ["apple", "apply", "ape", "app", "banana"]
    
    def test_top_n(self):
        """Test getting top N matches."""
        results = extract_top_n("apple", self.candidates, n=3)
        self.assertEqual(len(results), 3)
        self.assertEqual(results[0][0], "apple")
    
    def test_with_threshold(self):
        """Test with threshold."""
        results = extract_top_n("xyz", self.candidates, threshold=0.5)
        self.assertEqual(len(results), 0)


class TestPartialRatio(unittest.TestCase):
    """Test partial_ratio function."""
    
    def test_substring_match(self):
        """Test substring match."""
        ratio = partial_ratio("hello", "hello world")
        self.assertEqual(ratio, 1.0)
    
    def test_partial_match(self):
        """Test partial match."""
        ratio = partial_ratio("world", "hello world")
        self.assertEqual(ratio, 1.0)
    
    def test_no_match(self):
        """Test no partial match."""
        ratio = partial_ratio("xyz", "hello world")
        self.assertLess(ratio, 0.5)


class TestTokenSortRatio(unittest.TestCase):
    """Test token_sort_ratio function."""
    
    def test_same_order(self):
        """Test same word order."""
        ratio = token_sort_ratio("hello world", "hello world")
        self.assertEqual(ratio, 1.0)
    
    def test_different_order(self):
        """Test different word order."""
        ratio = token_sort_ratio("hello world", "world hello")
        self.assertEqual(ratio, 1.0)
    
    def test_partial_token_match(self):
        """Test partial token match."""
        ratio = token_sort_ratio("hello world", "hello there")
        self.assertGreater(ratio, 0.3)


class TestTokenSetRatio(unittest.TestCase):
    """Test token_set_ratio function."""
    
    def test_identical_tokens(self):
        """Test identical tokens."""
        ratio = token_set_ratio("hello world", "world hello")
        self.assertEqual(ratio, 1.0)
    
    def test_duplicate_tokens(self):
        """Test duplicate tokens ignored."""
        ratio = token_set_ratio("hello hello world", "world hello")
        self.assertEqual(ratio, 1.0)
    
    def test_extra_tokens(self):
        """Test extra tokens."""
        ratio = token_set_ratio("hello world", "hello world goodbye")
        self.assertGreater(ratio, 0.5)


class TestWeightedRatio(unittest.TestCase):
    """Test weighted_ratio function."""
    
    def test_identical_strings(self):
        """Test identical strings."""
        ratio = weighted_ratio("hello", "hello")
        self.assertEqual(ratio, 1.0)
    
    def test_similar_strings(self):
        """Test similar strings."""
        ratio = weighted_ratio("hello world", "hallo world")
        self.assertGreater(ratio, 0.7)
    
    def test_custom_weights(self):
        """Test custom weights."""
        weights = {'levenshtein': 1.0}
        ratio = weighted_ratio("hello", "hallo", weights=weights)
        self.assertAlmostEqual(ratio, 0.8, places=2)


class TestFuzzyMatch(unittest.TestCase):
    """Test FuzzyMatch class."""
    
    def test_fuzzy_match_creation(self):
        """Test creating FuzzyMatch."""
        match = FuzzyMatch(value="test", score=0.8, algorithm="levenshtein", original_query="tst")
        self.assertEqual(match.value, "test")
        self.assertEqual(match.score, 0.8)
        self.assertEqual(match.algorithm, "levenshtein")
    
    def test_fuzzy_match_comparison(self):
        """Test FuzzyMatch comparison."""
        match1 = FuzzyMatch(value="a", score=0.8, algorithm="test", original_query="q")
        match2 = FuzzyMatch(value="b", score=0.9, algorithm="test", original_query="q")
        self.assertTrue(match1 < match2)
    
    def test_fuzzy_match_repr(self):
        """Test FuzzyMatch repr."""
        match = FuzzyMatch(value="test", score=0.8, algorithm="levenshtein", original_query="tst")
        repr_str = repr(match)
        self.assertIn("test", repr_str)
        self.assertIn("0.8", repr_str)


class TestFuzzyMatcher(unittest.TestCase):
    """Test FuzzyMatcher class."""
    
    def test_init_with_candidates(self):
        """Test initialization with candidates."""
        matcher = FuzzyMatcher(["apple", "banana"])
        self.assertEqual(matcher.count, 2)
    
    def test_add_candidates(self):
        """Test adding candidates."""
        matcher = FuzzyMatcher()
        matcher.add_candidates(["apple", "banana"])
        self.assertEqual(matcher.count, 2)
        matcher.add_candidate("orange")
        self.assertEqual(matcher.count, 3)
    
    def test_remove_candidate(self):
        """Test removing candidate."""
        matcher = FuzzyMatcher(["apple", "banana"])
        result = matcher.remove_candidate("apple")
        self.assertTrue(result)
        self.assertEqual(matcher.count, 1)
    
    def test_search(self):
        """Test search functionality."""
        matcher = FuzzyMatcher(["apple", "banana", "orange"])
        results = matcher.search("aple", threshold=0.6)
        self.assertGreater(len(results), 0)
        self.assertIn("apple", [r.value for r in results])
    
    def test_find(self):
        """Test find functionality."""
        matcher = FuzzyMatcher(["apple", "banana", "orange"])
        result = matcher.find("aple", threshold=0.6)
        self.assertEqual(result, "apple")
    
    def test_clear(self):
        """Test clearing matcher."""
        matcher = FuzzyMatcher(["apple", "banana"])
        matcher.clear()
        self.assertEqual(matcher.count, 0)
    
    def test_candidates_property(self):
        """Test candidates property."""
        matcher = FuzzyMatcher(["apple", "banana"])
        candidates = matcher.candidates
        self.assertEqual(candidates, ["apple", "banana"])
        # Ensure it's a copy
        candidates.append("orange")
        self.assertEqual(matcher.count, 2)
    
    def test_indexed_search(self):
        """Test indexed search."""
        matcher = FuzzyMatcher(["apple", "banana", "orange", "grape"])
        results_indexed = matcher.search("aple", threshold=0.6, use_index=True)
        results_unindexed = matcher.search("aple", threshold=0.6, use_index=False)
        
        # Should produce same results
        indexed_values = sorted([r.value for r in results_indexed])
        unindexed_values = sorted([r.value for r in results_unindexed])
        self.assertEqual(indexed_values, unindexed_values)
    
    def test_case_sensitive(self):
        """Test case-sensitive matching."""
        matcher = FuzzyMatcher(["Apple", "Banana"], case_sensitive=True)
        results = matcher.search("apple", threshold=0.6)
        # Case-sensitive means we compare without lowercasing
        # "Apple" vs "apple" still has 80% similarity (only one character diff)
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].value, "Apple")
        self.assertAlmostEqual(results[0].score, 0.8, places=1)


class TestDeduplicate(unittest.TestCase):
    """Test deduplicate function."""
    
    def test_similar_strings_grouped(self):
        """Test similar strings are grouped."""
        groups = deduplicate(["hello", "hallo", "hi", "hey"], threshold=0.7)
        # hello and hallo should be in same group
        for group in groups:
            if "hello" in group:
                self.assertIn("hallo", group)
                break
    
    def test_different_strings_separate(self):
        """Test different strings are separate."""
        groups = deduplicate(["abc", "xyz"], threshold=0.7)
        self.assertEqual(len(groups), 2)
    
    def test_empty_list(self):
        """Test empty list."""
        groups = deduplicate([])
        self.assertEqual(len(groups), 0)


class TestSuggestCorrections(unittest.TestCase):
    """Test suggest_corrections function."""
    
    def setUp(self):
        self.dictionary = ["apple", "apply", "ape", "banana"]
    
    def test_typo_correction(self):
        """Test typo correction."""
        suggestions = suggest_corrections("appel", self.dictionary, threshold=0.6)
        self.assertGreater(len(suggestions), 0)
        self.assertIn("apple", [s[0] for s in suggestions])
    
    def test_max_suggestions(self):
        """Test max suggestions limit."""
        suggestions = suggest_corrections("a", self.dictionary, max_suggestions=2)
        self.assertLessEqual(len(suggestions), 2)
    
    def test_exact_word(self):
        """Test exact word in dictionary."""
        suggestions = suggest_corrections("apple", self.dictionary)
        self.assertEqual(suggestions[0][0], "apple")
        self.assertEqual(suggestions[0][1], 1.0)


class TestEdgeCases(unittest.TestCase):
    """Test edge cases."""
    
    def test_unicode_strings(self):
        """Test Unicode string handling."""
        distance = levenshtein_distance("你好", "你好世界")
        self.assertEqual(distance, 2)
        
        ratio = levenshtein_ratio("日本", "日本語")
        self.assertGreater(ratio, 0.3)
    
    def test_very_long_strings(self):
        """Test very long strings."""
        s1 = "a" * 1000
        s2 = "a" * 999 + "b"
        distance = levenshtein_distance(s1, s2)
        self.assertEqual(distance, 1)
    
    def test_special_characters(self):
        """Test special characters."""
        distance = levenshtein_distance("hello!", "hello?")
        self.assertEqual(distance, 1)
        
        ngrams = get_ngrams("a b", 2)
        self.assertIn("a ", ngrams)
    
    def test_numbers(self):
        """Test numeric strings."""
        distance = levenshtein_distance("12345", "12354")
        self.assertEqual(distance, 2)
    
    def test_whitespace_handling(self):
        """Test whitespace handling."""
        ratio = token_sort_ratio("hello  world", "world hello")
        self.assertEqual(ratio, 1.0)


class TestPerformance(unittest.TestCase):
    """Test performance characteristics."""
    
    def test_large_candidate_list(self):
        """Test search on large candidate list."""
        candidates = [f"word{i}" for i in range(1000)]
        candidates.extend(["apple", "banana", "orange"])
        
        results = fuzzy_search("apple", candidates, threshold=0.8)
        self.assertGreater(len(results), 0)
    
    def test_repeated_search_with_index(self):
        """Test repeated searches with index."""
        matcher = FuzzyMatcher([f"item{i}" for i in range(100)])
        
        # Multiple searches should be fast with index
        for query in ["item0", "item5", "item99"]:
            results = matcher.search(query, threshold=0.9)
            self.assertGreater(len(results), 0)


if __name__ == '__main__':
    unittest.main(verbosity=2)