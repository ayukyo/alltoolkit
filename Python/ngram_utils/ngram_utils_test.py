"""
Unit tests for N-gram Utilities Module

Tests all functions and classes in ngram_utils/mod.py
"""

import unittest
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from mod import (
    char_ngrams, word_ngrams, token_ngrams, ngram_frequencies,
    all_ngrams, jaccard_similarity, dice_similarity, cosine_similarity,
    ngram_profile, language_distance, build_language_profiles,
    detect_language, ngram_frequency_analysis, most_common_ngrams,
    build_ngram_model, predict_next, text_similarity, ngram_overlap,
    unique_ngrams, ngram_positions, sentence_ngrams, NGramAnalyzer,
    get_common_language_profiles, bigrams, trigrams, quadgrams
)


class TestCharNgrams(unittest.TestCase):
    """Test character N-gram generation."""
    
    def test_basic_bigrams(self):
        """Test basic bigram generation."""
        result = char_ngrams("hello", 2)
        expected = ['he', 'el', 'll', 'lo']
        self.assertEqual(result, expected)
    
    def test_basic_trigrams(self):
        """Test basic trigram generation."""
        result = char_ngrams("hello", 3)
        expected = ['hel', 'ell', 'llo']
        self.assertEqual(result, expected)
    
    def test_empty_string(self):
        """Test empty string returns empty list."""
        self.assertEqual(char_ngrams("", 2), [])
    
    def test_short_string(self):
        """Test string shorter than n."""
        self.assertEqual(char_ngrams("hi", 3), ['hi'])
    
    def test_single_char(self):
        """Test single character."""
        self.assertEqual(char_ngrams("a", 1), ['a'])
    
    def test_padding(self):
        """Test padded N-grams."""
        result = char_ngrams("hi", 2, pad=True)
        self.assertEqual(result, [' h', 'hi', 'i '])
    
    def test_padding_trigrams(self):
        """Test padded trigrams."""
        result = char_ngrams("a", 3, pad=True)
        self.assertEqual(result, ['  a', ' a ', 'a  '])
    
    def test_n_zero(self):
        """Test n=0 returns empty list."""
        self.assertEqual(char_ngrams("hello", 0), [])
    
    def test_n_one(self):
        """Test unigrams (n=1)."""
        result = char_ngrams("abc", 1)
        self.assertEqual(result, ['a', 'b', 'c'])


class TestWordNgrams(unittest.TestCase):
    """Test word N-gram generation."""
    
    def test_basic_word_bigrams(self):
        """Test basic word bigram generation."""
        result = word_ngrams("hello world test", 2)
        expected = ['hello world', 'world test']
        self.assertEqual(result, expected)
    
    def test_word_trigrams(self):
        """Test word trigram generation."""
        result = word_ngrams("the quick brown fox", 3)
        expected = ['the quick brown', 'quick brown fox']
        self.assertEqual(result, expected)
    
    def test_empty_text(self):
        """Test empty text returns empty list."""
        self.assertEqual(word_ngrams("", 2), [])
    
    def test_single_word(self):
        """Test single word."""
        result = word_ngrams("hello", 2)
        self.assertEqual(result, ['hello'])
    
    def test_custom_tokenizer(self):
        """Test with custom tokenizer."""
        def tokenizer(text):
            return text.split('-')
        
        result = word_ngrams("a-b-c", 2, tokenizer=tokenizer)
        self.assertEqual(result, ['a b', 'b c'])
    
    def test_punctuation_handling(self):
        """Test punctuation is handled."""
        result = word_ngrams("Hello, world!", 2)
        self.assertEqual(result, ['hello world'])


class TestTokenNgrams(unittest.TestCase):
    """Test token N-gram generation."""
    
    def test_basic_tokens(self):
        """Test basic token N-grams."""
        result = token_ngrams(['a', 'b', 'c', 'd'], 2)
        expected = [('a', 'b'), ('b', 'c'), ('c', 'd')]
        self.assertEqual(result, expected)
    
    def test_token_trigrams(self):
        """Test token trigrams."""
        result = token_ngrams(['a', 'b', 'c', 'd'], 3)
        expected = [('a', 'b', 'c'), ('b', 'c', 'd')]
        self.assertEqual(result, expected)
    
    def test_empty_tokens(self):
        """Test empty token list."""
        self.assertEqual(token_ngrams([], 2), [])
    
    def test_short_token_list(self):
        """Test token list shorter than n."""
        result = token_ngrams(['a', 'b'], 3)
        self.assertEqual(result, [('a', 'b')])


class TestNgramFrequencies(unittest.TestCase):
    """Test N-gram frequency calculations."""
    
    def test_basic_frequencies(self):
        """Test basic frequency counting."""
        result = ngram_frequencies(['a', 'b', 'a', 'c', 'a'])
        expected = {'a': 3, 'b': 1, 'c': 1}
        self.assertEqual(result, expected)
    
    def test_normalized_frequencies(self):
        """Test normalized frequencies sum to 1."""
        result = ngram_frequencies(['a', 'b', 'a', 'c'], normalize=True)
        self.assertAlmostEqual(result['a'], 0.5)
        self.assertAlmostEqual(result['b'], 0.25)
        self.assertAlmostEqual(result['c'], 0.25)
        total = sum(result.values())
        self.assertAlmostEqual(total, 1.0)
    
    def test_empty_list(self):
        """Test empty list returns empty dict."""
        self.assertEqual(ngram_frequencies([]), {})


class TestAllNgrams(unittest.TestCase):
    """Test all N-grams generation."""
    
    def test_char_mode(self):
        """Test character mode."""
        result = all_ngrams("hi", 1, 2, 'char')
        self.assertIn('h', result)
        self.assertIn('i', result)
        self.assertIn('hi', result)
    
    def test_word_mode(self):
        """Test word mode."""
        result = all_ngrams("a b c", 1, 2, 'word')
        self.assertIn('a', result)
        self.assertIn('b', result)
        self.assertIn('c', result)
        self.assertIn('a b', result)
        self.assertIn('b c', result)


class TestSimilarityFunctions(unittest.TestCase):
    """Test similarity calculation functions."""
    
    def test_jaccard_identical(self):
        """Test Jaccard similarity with identical sets."""
        result = jaccard_similarity({'a', 'b'}, {'a', 'b'})
        self.assertEqual(result, 1.0)
    
    def test_jaccard_disjoint(self):
        """Test Jaccard similarity with disjoint sets."""
        result = jaccard_similarity({'a', 'b'}, {'c', 'd'})
        self.assertEqual(result, 0.0)
    
    def test_jaccard_partial(self):
        """Test Jaccard similarity with partial overlap."""
        result = jaccard_similarity({'a', 'b', 'c'}, {'b', 'c', 'd'})
        self.assertEqual(result, 0.5)
    
    def test_jaccard_empty_both(self):
        """Test Jaccard similarity with both empty."""
        result = jaccard_similarity(set(), set())
        self.assertEqual(result, 1.0)
    
    def test_jaccard_one_empty(self):
        """Test Jaccard similarity with one empty."""
        result = jaccard_similarity({'a'}, set())
        self.assertEqual(result, 0.0)
    
    def test_dice_identical(self):
        """Test Dice similarity with identical sets."""
        result = dice_similarity({'a', 'b'}, {'a', 'b'})
        self.assertEqual(result, 1.0)
    
    def test_dice_partial(self):
        """Test Dice similarity with partial overlap."""
        result = dice_similarity({'a', 'b', 'c'}, {'b', 'c', 'd'})
        self.assertAlmostEqual(result, 2/3, places=4)
    
    def test_cosine_identical(self):
        """Test cosine similarity with identical vectors."""
        result = cosine_similarity({'a': 1, 'b': 2}, {'a': 1, 'b': 2})
        self.assertAlmostEqual(result, 1.0)
    
    def test_cosine_orthogonal(self):
        """Test cosine similarity with orthogonal vectors."""
        result = cosine_similarity({'a': 1}, {'b': 1})
        self.assertEqual(result, 0.0)
    
    def test_cosine_empty(self):
        """Test cosine similarity with empty."""
        result = cosine_similarity({}, {'a': 1})
        self.assertEqual(result, 0.0)


class TestNgramProfile(unittest.TestCase):
    """Test N-gram profile generation."""
    
    def test_basic_profile(self):
        """Test basic profile generation."""
        profile = ngram_profile("hello", n=2, top_k=10)
        self.assertIsInstance(profile, dict)
        self.assertTrue(len(profile) <= 10)
    
    def test_profile_ranks(self):
        """Test profile has ranks (lower = more frequent)."""
        text = "aaab"
        profile = ngram_profile(text, n=2, top_k=10)
        # 'aa' should appear twice, 'ab' once
        # 'aa' should have lower rank (more frequent)
        if 'aa' in profile and 'ab' in profile:
            self.assertLess(profile['aa'], profile['ab'])
    
    def test_empty_text(self):
        """Test empty text profile."""
        profile = ngram_profile("", n=2)
        self.assertEqual(profile, {})


class TestLanguageDistance(unittest.TestCase):
    """Test language distance calculation."""
    
    def test_identical_profiles(self):
        """Test identical profiles have zero distance."""
        profile = {'a': 1, 'b': 2, 'c': 3}
        distance = language_distance(profile, profile)
        self.assertEqual(distance, 0)
    
    def test_different_profiles(self):
        """Test different profiles have positive distance."""
        profile1 = {'a': 1, 'b': 2}
        profile2 = {'x': 1, 'y': 2}
        distance = language_distance(profile1, profile2)
        self.assertGreater(distance, 0)


class TestBuildLanguageProfiles(unittest.TestCase):
    """Test language profile building."""
    
    def test_build_profiles(self):
        """Test building language profiles."""
        texts = {
            'en': 'hello world test',
            'es': 'hola mundo prueba'
        }
        profiles = build_language_profiles(texts, n=2, top_k=10)
        
        self.assertIn('en', profiles)
        self.assertIn('es', profiles)
        self.assertIsInstance(profiles['en'], dict)


class TestDetectLanguage(unittest.TestCase):
    """Test language detection."""
    
    def test_detect_english(self):
        """Test detecting English text."""
        profiles = {
            'en': ngram_profile('the quick brown fox jumps over lazy dog', n=3),
            'es': ngram_profile('el rápido zorro marrón salta sobre perro perezoso', n=3)
        }
        lang, dist = detect_language('the fox jumps', profiles, n=3)
        self.assertEqual(lang, 'en')
    
    def test_detect_returns_tuple(self):
        """Test detection returns (language, distance) tuple."""
        profiles = {'en': ngram_profile('hello world', n=2)}
        result = detect_language('hello', profiles, n=2)
        self.assertIsInstance(result, tuple)
        self.assertEqual(len(result), 2)


class TestNgramFrequencyAnalysis(unittest.TestCase):
    """Test comprehensive frequency analysis."""
    
    def test_analysis_structure(self):
        """Test analysis returns correct structure."""
        analysis = ngram_frequency_analysis("hello", min_n=1, max_n=2, mode='char')
        
        self.assertIn(1, analysis)
        self.assertIn(2, analysis)
        self.assertIsInstance(analysis[1], list)
        self.assertIsInstance(analysis[2][0], tuple)
    
    def test_analysis_top_k(self):
        """Test top_k limits results."""
        analysis = ngram_frequency_analysis("abcdefghijklmnopqrstuvwxyz", min_n=1, max_n=1, top_k=5)
        self.assertLessEqual(len(analysis[1]), 5)


class TestMostCommonNgrams(unittest.TestCase):
    """Test most common N-grams function."""
    
    def test_most_common_char(self):
        """Test most common character N-grams."""
        result = most_common_ngrams("aab", 1, 'char', top_k=3)
        # 'a' appears twice, 'b' once
        self.assertEqual(result[0], ('a', 2))
        self.assertEqual(result[1], ('b', 1))
    
    def test_most_common_word(self):
        """Test most common word N-grams."""
        result = most_common_ngrams("hello hello world", 1, 'word', top_k=5)
        self.assertEqual(result[0], ('hello', 2))


class TestBuildNgramModel(unittest.TestCase):
    """Test N-gram model building."""
    
    def test_word_model(self):
        """Test word N-gram model."""
        model = build_ngram_model("the cat the dog", n=2)
        # Context 'the' can be followed by 'cat' or 'dog'
        self.assertIn(('the',), model)
    
    def test_char_model(self):
        """Test character N-gram model."""
        model = build_ngram_model("ab", n=2, mode='char')
        self.assertIn(('a',), model)
    
    def test_model_frequencies(self):
        """Test model tracks frequencies."""
        model = build_ngram_model("a b a c", n=2)
        # 'a' appears twice, followed by 'b' and 'c' once each
        self.assertEqual(model[('a',)]['b'], 1)
        self.assertEqual(model[('a',)]['c'], 1)


class TestPredictNext(unittest.TestCase):
    """Test next token prediction."""
    
    def test_basic_prediction(self):
        """Test basic prediction."""
        model = build_ngram_model("the cat the dog", n=2)
        predictions = predict_next(model, ['the'])
        self.assertGreater(len(predictions), 0)
        # Check predictions are (token, probability) tuples
        self.assertEqual(len(predictions[0]), 2)
    
    def test_prediction_probabilities(self):
        """Test prediction probabilities sum correctly."""
        model = build_ngram_model("a b a c a d", n=2)
        predictions = predict_next(model, ['a'])
        total_prob = sum(prob for _, prob in predictions)
        self.assertAlmostEqual(total_prob, 1.0, places=5)
    
    def test_unknown_context(self):
        """Test prediction with unknown context."""
        model = build_ngram_model("hello world", n=2)
        predictions = predict_next(model, ['unknown'])
        self.assertEqual(predictions, [])
    
    def test_empty_context(self):
        """Test prediction with empty context."""
        model = build_ngram_model("hello world", n=2)
        predictions = predict_next(model, [])
        self.assertEqual(predictions, [])


class TestTextSimilarity(unittest.TestCase):
    """Test text similarity function."""
    
    def test_identical_text(self):
        """Test identical text has similarity 1.0."""
        result = text_similarity("hello", "hello", n=2, method='jaccard')
        self.assertEqual(result, 1.0)
    
    def test_different_text(self):
        """Test completely different text."""
        result = text_similarity("abc", "xyz", n=2, method='jaccard')
        self.assertEqual(result, 0.0)
    
    def test_partial_similarity(self):
        """Test partially similar text."""
        result = text_similarity("hello", "hallo", n=2, method='jaccard')
        self.assertGreater(result, 0.0)
        self.assertLess(result, 1.0)
    
    def test_all_methods(self):
        """Test all similarity methods."""
        for method in ['jaccard', 'dice', 'cosine']:
            result = text_similarity("hello", "hallo", n=2, method=method)
            self.assertIsInstance(result, float)
            self.assertGreaterEqual(result, 0.0)
            self.assertLessEqual(result, 1.0)
    
    def test_invalid_method(self):
        """Test invalid method raises error."""
        with self.assertRaises(ValueError):
            text_similarity("a", "b", n=2, method='invalid')


class TestNgramOverlap(unittest.TestCase):
    """Test N-gram overlap function."""
    
    def test_overlap_structure(self):
        """Test overlap returns correct structure."""
        result = ngram_overlap("hello world", "hello there", n=2, mode='word')
        
        self.assertIn('intersection', result)
        self.assertIn('intersection_size', result)
        self.assertIn('union_size', result)
        self.assertIn('jaccard', result)
    
    def test_word_overlap(self):
        """Test word overlap detection."""
        result = ngram_overlap("a b c", "a b d", n=1, mode='word')
        self.assertIn('a', result['intersection'])
        self.assertIn('b', result['intersection'])
    
    def test_char_overlap(self):
        """Test character overlap detection."""
        result = ngram_overlap("ab", "ab", n=2, mode='char')
        self.assertEqual(result['jaccard'], 1.0)


class TestUniqueNgrams(unittest.TestCase):
    """Test unique N-grams function."""
    
    def test_unique_char_ngrams(self):
        """Test unique character N-grams."""
        result = unique_ngrams("aabb", 2, 'char')
        self.assertEqual(result, {'aa', 'ab', 'bb'})
    
    def test_unique_word_ngrams(self):
        """Test unique word N-grams."""
        result = unique_ngrams("hello world hello", 1, 'word')
        self.assertEqual(result, {'hello', 'world'})
    
    def test_empty_text(self):
        """Test empty text returns empty set."""
        result = unique_ngrams("", 2, 'char')
        self.assertEqual(result, set())


class TestNgramPositions(unittest.TestCase):
    """Test N-gram position finding."""
    
    def test_char_positions(self):
        """Test character N-gram positions."""
        result = ngram_positions("abab", 2, 'char')
        self.assertEqual(result['ab'], [0, 2])
        self.assertEqual(result['ba'], [1])
    
    def test_word_positions(self):
        """Test word N-gram positions."""
        result = ngram_positions("a b a c", 1, 'word')
        self.assertEqual(result['a'], [0, 2])
    
    def test_single_occurrence(self):
        """Test single occurrence N-grams."""
        result = ngram_positions("abc", 2, 'char')
        self.assertEqual(result['ab'], [0])
        self.assertEqual(result['bc'], [1])


class TestSentenceNgrams(unittest.TestCase):
    """Test sentence N-gram generation."""
    
    def test_basic_sentences(self):
        """Test basic sentence N-grams."""
        result = sentence_ngrams("Hello. World. Test.", 2)
        self.assertEqual(result, ['Hello. World.', 'World. Test.'])
    
    def test_short_text(self):
        """Test text with fewer sentences than n."""
        result = sentence_ngrams("Hello. World.", 3)
        self.assertEqual(result, ['Hello. World.'])
    
    def test_single_sentence(self):
        """Test single sentence."""
        result = sentence_ngrams("Hello world.", 2)
        self.assertEqual(result, ['Hello world.'])
    
    def test_question_mark(self):
        """Test sentence splitting on question marks."""
        result = sentence_ngrams("Hello? World!", 2)
        self.assertEqual(result, ['Hello? World!'])


class TestNGramAnalyzer(unittest.TestCase):
    """Test NGramAnalyzer class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.analyzer = NGramAnalyzer("Hello world! Hello there!")
    
    def test_char_ngrams(self):
        """Test character N-grams via analyzer."""
        result = self.analyzer.char_ngrams(2)
        self.assertTrue(len(result) > 0)
        self.assertTrue(all(len(ng) == 2 for ng in result))
    
    def test_word_ngrams(self):
        """Test word N-grams via analyzer."""
        result = self.analyzer.word_ngrams(2)
        self.assertTrue(len(result) > 0)
    
    def test_frequencies(self):
        """Test frequency calculation via analyzer."""
        freq = self.analyzer.frequencies(2, mode='word', normalize=True)
        self.assertIsInstance(freq, dict)
        total = sum(freq.values())
        self.assertAlmostEqual(total, 1.0, places=5)
    
    def test_most_common(self):
        """Test most common N-grams via analyzer."""
        result = self.analyzer.most_common(2, mode='word', top_k=3)
        self.assertTrue(len(result) <= 3)
    
    def test_unique(self):
        """Test unique N-grams via analyzer."""
        result = self.analyzer.unique(2, mode='char')
        self.assertIsInstance(result, set)
    
    def test_similarity_to(self):
        """Test similarity calculation via analyzer."""
        result = self.analyzer.similarity_to("Hello world!", n=2)
        self.assertIsInstance(result, float)
        self.assertGreaterEqual(result, 0.0)
        self.assertLessEqual(result, 1.0)
    
    def test_analysis(self):
        """Test comprehensive analysis via analyzer."""
        result = self.analyzer.analysis(min_n=1, max_n=2, mode='char')
        self.assertIn(1, result)
        self.assertIn(2, result)
    
    def test_repr(self):
        """Test string representation."""
        repr_str = repr(self.analyzer)
        self.assertIn('NGramAnalyzer', repr_str)


class TestConvenienceFunctions(unittest.TestCase):
    """Test convenience functions."""
    
    def test_bigrams(self):
        """Test bigrams convenience function."""
        result = bigrams("hello", mode='char')
        self.assertEqual(len(result[0]), 2)
    
    def test_trigrams(self):
        """Test trigrams convenience function."""
        result = trigrams("hello", mode='char')
        self.assertEqual(len(result[0]), 3)
    
    def test_quadgrams(self):
        """Test quadgrams convenience function."""
        result = quadgrams("hello world", mode='char')
        self.assertEqual(len(result[0]), 4)


class TestCommonLanguageProfiles(unittest.TestCase):
    """Test pre-built language profiles."""
    
    def test_get_profiles(self):
        """Test getting pre-built language profiles."""
        profiles = get_common_language_profiles()
        
        # Check all expected languages are present
        expected = ['en', 'es', 'fr', 'de', 'it', 'pt', 'nl', 'ru', 'zh', 'ja', 'ko', 'ar']
        for lang in expected:
            self.assertIn(lang, profiles)
            self.assertIsInstance(profiles[lang], dict)
    
    def test_profile_structure(self):
        """Test profile structure."""
        profiles = get_common_language_profiles(n=3, top_k=50)
        
        for lang, profile in profiles.items():
            self.assertIsInstance(profile, dict)
            self.assertTrue(len(profile) <= 50)


class TestEdgeCases(unittest.TestCase):
    """Test edge cases and error handling."""
    
    def test_whitespace_handling(self):
        """Test handling of extra whitespace."""
        result = word_ngrams("hello   world", 2)
        self.assertEqual(result, ['hello world'])
    
    def test_unicode_text(self):
        """Test handling of Unicode text."""
        result = char_ngrams("你好世界", 2)
        self.assertEqual(result, ['你好', '好世', '世界'])
    
    def test_numbers_in_text(self):
        """Test handling of numbers."""
        result = word_ngrams("test 123 abc", 1)
        self.assertIn('123', result)
    
    def test_mixed_case(self):
        """Test case handling in word N-grams."""
        result = word_ngrams("Hello HELLO hello", 1)
        # Should be lowercase by default
        self.assertEqual(result, ['hello', 'hello', 'hello'])
    
    def test_special_characters(self):
        """Test special characters in N-grams."""
        result = char_ngrams("a@b#c", 2)
        self.assertEqual(result, ['a@', '@b', 'b#', '#c'])


if __name__ == '__main__':
    unittest.main(verbosity=2)