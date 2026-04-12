"""
AllToolkit - Python Text Utilities Test Suite

Comprehensive tests for text_utils module.
Run with: python text_utils_test.py
"""

import unittest
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from mod import (
    TextUtils,
    TextCase,
    TextStats,
    TextAnalysis,
    WordInfo,
    # Module-level functions
    to_case,
    clean,
    get_stats,
    analyze,
    remove_html,
    truncate,
    similarity,
    levenshtein_distance,
    extract_words,
    split_sentences,
    normalize_whitespace,
    hash_text,
)


class TestTextCase(unittest.TestCase):
    """Test case conversion functions."""
    
    def setUp(self):
        self.utils = TextUtils()
    
    def test_to_lower(self):
        self.assertEqual(self.utils.to_case("Hello World", TextCase.LOWER), "hello world")
    
    def test_to_upper(self):
        self.assertEqual(self.utils.to_case("Hello World", TextCase.UPPER), "HELLO WORLD")
    
    def test_to_title(self):
        self.assertEqual(self.utils.to_case("hello world", TextCase.TITLE), "Hello World")
    
    def test_to_sentence_case(self):
        self.assertEqual(self.utils.to_sentence_case("hello WORLD"), "Hello world")
        self.assertEqual(self.utils.to_sentence_case("  hello world"), "  Hello world")
    
    def test_to_camel_case(self):
        self.assertEqual(self.utils.to_case("hello world", TextCase.CAMEL), "helloWorld")
        self.assertEqual(self.utils.to_case("Hello World", TextCase.CAMEL), "helloWorld")
    
    def test_to_pascal_case(self):
        self.assertEqual(self.utils.to_case("hello world", TextCase.PASCAL), "HelloWorld")
    
    def test_to_snake_case(self):
        self.assertEqual(self.utils.to_case("Hello World", TextCase.SNAKE), "hello_world")
        self.assertEqual(self.utils.to_case("helloWorld", TextCase.SNAKE), "hello_world")
    
    def test_to_kebab_case(self):
        self.assertEqual(self.utils.to_case("Hello World", TextCase.KEBAB), "hello-world")
    
    def test_to_constant_case(self):
        self.assertEqual(self.utils.to_case("Hello World", TextCase.CONSTANT), "HELLO_WORLD")
    
    def test_split_into_words(self):
        words = self.utils.split_into_words("hello-world_test/path")
        self.assertEqual(words, ['hello', 'world', 'test', 'path'])
    
    def test_split_camel_case(self):
        words = self.utils.split_into_words("helloWorldTest")
        self.assertIn('hello', words)
        self.assertIn('World', words)  # Preserves case
        self.assertIn('Test', words)


class TestTextCleaning(unittest.TestCase):
    """Test text cleaning functions."""
    
    def setUp(self):
        self.utils = TextUtils()
    
    def test_clean_extra_spaces(self):
        text = "  Hello    World!  "
        cleaned = self.utils.clean(text, remove_extra_spaces=True)
        self.assertEqual(cleaned, "Hello World!")
    
    def test_clean_punctuation(self):
        text = "Hello, World!"
        cleaned = self.utils.clean(text, remove_punctuation=True)
        self.assertEqual(cleaned, "Hello World")
    
    def test_clean_digits(self):
        text = "Test123 with 456 digits"
        cleaned = self.utils.clean(text, remove_digits=True)
        self.assertEqual(cleaned, "Test with digits")
    
    def test_remove_html(self):
        html = "<p>Hello <b>World</b>!</p>"
        text = self.utils.remove_html(html)
        self.assertEqual(text, "Hello World!")
    
    def test_remove_html_entities(self):
        html = "Price: &pound;10 &amp; &euro;20"
        # Basic test - entities should be handled
        text = self.utils.remove_html(html)
        self.assertNotIn('<', text)
        self.assertNotIn('>', text)
    
    def test_remove_urls(self):
        text = "Visit https://example.com or http://test.org/page"
        cleaned = self.utils.remove_urls(text)
        self.assertNotIn("https://", cleaned)
        self.assertNotIn("http://", cleaned)
    
    def test_remove_emails(self):
        text = "Contact us at test@example.com or support@company.org"
        cleaned = self.utils.remove_emails(text)
        self.assertNotIn("@", cleaned)
    
    def test_normalize_whitespace(self):
        text = "Hello\t\tWorld\n\nTest"
        normalized = self.utils.normalize_whitespace(text)
        self.assertEqual(normalized, "Hello World Test")
    
    def test_normalize_line_endings_unix(self):
        text = "Line1\r\nLine2\rLine3\nLine4"
        normalized = self.utils.normalize_line_endings(text, 'unix')
        self.assertEqual(normalized, "Line1\nLine2\nLine3\nLine4")
    
    def test_normalize_line_endings_windows(self):
        text = "Line1\nLine2"
        normalized = self.utils.normalize_line_endings(text, 'windows')
        self.assertEqual(normalized, "Line1\r\nLine2")


class TestTextFormatting(unittest.TestCase):
    """Test text formatting functions."""
    
    def setUp(self):
        self.utils = TextUtils()
    
    def test_pad_left(self):
        result = self.utils.pad("test", 8, side='left')
        self.assertEqual(result, "    test")
    
    def test_pad_right(self):
        result = self.utils.pad("test", 8, side='right')
        self.assertEqual(result, "test    ")
    
    def test_pad_center(self):
        result = self.utils.pad("test", 8, side='center')
        self.assertEqual(result, "  test  ")
    
    def test_pad_custom_char(self):
        result = self.utils.pad("test", 8, side='left', char='0')
        self.assertEqual(result, "0000test")
    
    def test_pad_truncate(self):
        result = self.utils.pad("hello world", 5, side='right', truncate=True)
        self.assertEqual(result, "hello")
    
    def test_wrap_text(self):
        text = "This is a long sentence that should be wrapped."
        lines = self.utils.wrap(text, width=20)
        self.assertGreater(len(lines), 1)
        self.assertTrue(all(len(line) <= 20 for line in lines))
    
    def test_wrap_empty(self):
        lines = self.utils.wrap("", width=20)
        self.assertEqual(lines, [])


class TestTextAnalysis(unittest.TestCase):
    """Test text analysis functions."""
    
    def setUp(self):
        self.utils = TextUtils()
    
    def test_get_stats_basic(self):
        text = "Hello world. This is a test."
        stats = self.utils.get_stats(text)
        
        self.assertEqual(stats.word_count, 6)
        self.assertEqual(stats.sentence_count, 2)
        self.assertGreater(stats.char_count, 0)
        self.assertGreater(stats.avg_word_length, 0)
    
    def test_get_stats_empty(self):
        stats = self.utils.get_stats("")
        self.assertEqual(stats.word_count, 0)
        self.assertEqual(stats.sentence_count, 0)
    
    def test_extract_words(self):
        text = "Hello, World! 123 test."
        words = self.utils.extract_words(text)
        self.assertEqual(words, ['Hello', 'World', '123', 'test'])
    
    def test_extract_words_min_length(self):
        text = "I am a test"
        words = self.utils.extract_words(text, min_length=2)
        self.assertNotIn('a', words)
        self.assertIn('test', words)
    
    def test_split_sentences(self):
        text = "Hello world. How are you? I'm fine!"
        sentences = self.utils.split_sentences(text)
        self.assertEqual(len(sentences), 3)
    
    def test_get_ngrams(self):
        words = ['hello', 'world', 'test', 'case']
        bigrams = self.utils.get_ngrams(words, n=2)
        self.assertEqual(len(bigrams), 3)
        self.assertEqual(bigrams[0], ('hello', 'world'))
    
    def test_analyze_comprehensive(self):
        text = "The quick brown fox jumps over the lazy dog."
        analysis = self.utils.analyze(text, top_n=5)
        
        self.assertIsInstance(analysis, TextAnalysis)
        self.assertIsInstance(analysis.stats, TextStats)
        self.assertTrue(len(analysis.words) > 0)
        self.assertTrue(len(analysis.sentences) > 0)
    
    def test_keyword_density(self):
        text = "test test test other words here"
        density = self.utils.keyword_density(text)
        self.assertGreater(len(density), 0)
        # 'test' should be the most frequent
        self.assertEqual(density[0][0], 'test')


class TestTextTransformation(unittest.TestCase):
    """Test text transformation functions."""
    
    def setUp(self):
        self.utils = TextUtils()
    
    def test_reverse_chars(self):
        result = self.utils.reverse("hello")
        self.assertEqual(result, "olleh")
    
    def test_reverse_words(self):
        result = self.utils.reverse("hello world test", preserve_words=True)
        self.assertEqual(result, "test world hello")
    
    def test_rotate_right(self):
        result = self.utils.rotate("hello", 2)
        self.assertEqual(result, "lohel")
    
    def test_rotate_left(self):
        result = self.utils.rotate("hello", -2)
        self.assertEqual(result, "llohe")
    
    def test_alternate_case(self):
        result = self.utils.alternate_case("hello")
        self.assertEqual(result, "HeLlO")
    
    def test_mirror(self):
        result = self.utils.mirror("abc")
        self.assertEqual(result, "abccba")
    
    def test_truncate_start(self):
        result = self.utils.truncate("hello world", 8, suffix='...', align='start')
        self.assertEqual(result, "hello...")
    
    def test_truncate_end(self):
        result = self.utils.truncate("hello world", 8, suffix='...', align='end')
        self.assertEqual(result, "...world")
    
    def test_truncate_middle(self):
        result = self.utils.truncate("hello world", 9, suffix='...', align='middle')
        self.assertTrue('...' in result)
    
    def test_truncate_no_change(self):
        result = self.utils.truncate("short", 10)
        self.assertEqual(result, "short")
    
    def test_abbreviate(self):
        result = self.utils.abbreviate("Portable Network Graphics", 3)
        self.assertEqual(result, "PNG")


class TestTextSearch(unittest.TestCase):
    """Test search and replace functions."""
    
    def setUp(self):
        self.utils = TextUtils()
    
    def test_find_all(self):
        text = "test test test"
        positions = self.utils.find_all(text, "test")
        self.assertEqual(positions, [0, 5, 10])
    
    def test_find_all_case_insensitive(self):
        text = "Test TEST test"
        positions = self.utils.find_all(text, "test", case_sensitive=False)
        self.assertEqual(len(positions), 3)
    
    def test_replace_all(self):
        text = "hello world"
        result = self.utils.replace_all(text, {"hello": "hi", "world": "earth"})
        self.assertEqual(result, "hi earth")
    
    def test_highlight(self):
        text = "The quick brown fox"
        result = self.utils.highlight(text, ["quick", "fox"])
        self.assertIn("**quick**", result)
        self.assertIn("**fox**", result)


class TestTextComparison(unittest.TestCase):
    """Test text comparison functions."""
    
    def setUp(self):
        self.utils = TextUtils()
    
    def test_similarity_identical(self):
        sim = self.utils.similarity("hello world", "hello world")
        self.assertEqual(sim, 1.0)
    
    def test_similarity_different(self):
        sim = self.utils.similarity("hello world", "foo bar")
        self.assertEqual(sim, 0.0)
    
    def test_similarity_partial(self):
        sim = self.utils.similarity("hello world", "hello there")
        self.assertGreater(sim, 0.0)
        self.assertLess(sim, 1.0)
    
    def test_contains_all_true(self):
        text = "The quick brown fox"
        result = self.utils.contains_all(text, ["quick", "fox"])
        self.assertTrue(result)
    
    def test_contains_all_false(self):
        text = "The quick brown fox"
        result = self.utils.contains_all(text, ["quick", "elephant"])
        self.assertFalse(result)
    
    def test_contains_any_true(self):
        text = "The quick brown fox"
        result = self.utils.contains_any(text, ["elephant", "fox"])
        self.assertTrue(result)
    
    def test_contains_any_false(self):
        text = "The quick brown fox"
        result = self.utils.contains_any(text, ["elephant", "lion"])
        self.assertFalse(result)
    
    def test_levenshtein_identical(self):
        distance = self.utils.levenshtein_distance("hello", "hello")
        self.assertEqual(distance, 0)
    
    def test_levenshtein_different(self):
        distance = self.utils.levenshtein_distance("hello", "hallo")
        self.assertEqual(distance, 1)
    
    def test_levenshtein_empty(self):
        distance = self.utils.levenshtein_distance("", "hello")
        self.assertEqual(distance, 5)


class TestHashing(unittest.TestCase):
    """Test hashing and encoding functions."""
    
    def setUp(self):
        self.utils = TextUtils()
    
    def test_hash_md5(self):
        result = self.utils.hash_text("hello", 'md5')
        self.assertEqual(len(result), 32)  # MD5 hex length
    
    def test_hash_sha256(self):
        result = self.utils.hash_text("hello", 'sha256')
        self.assertEqual(len(result), 64)  # SHA256 hex length
    
    def test_hash_consistency(self):
        result1 = self.utils.hash_text("hello", 'md5')
        result2 = self.utils.hash_text("hello", 'md5')
        self.assertEqual(result1, result2)
    
    def test_base64_roundtrip(self):
        original = "Hello World!"
        encoded = self.utils.to_base64(original)
        decoded = self.utils.from_base64(encoded)
        self.assertEqual(decoded, original)
    
    def test_invalid_algorithm(self):
        with self.assertRaises(ValueError):
            self.utils.hash_text("hello", 'invalid')


class TestModuleLevelFunctions(unittest.TestCase):
    """Test module-level convenience functions."""
    
    def test_module_to_case(self):
        result = to_case("hello world", TextCase.UPPER)
        self.assertEqual(result, "HELLO WORLD")
    
    def test_module_clean(self):
        result = clean("  hello  world  ", remove_extra_spaces=True)
        self.assertEqual(result, "hello world")
    
    def test_module_get_stats(self):
        stats = get_stats("Hello world.")
        self.assertIsInstance(stats, TextStats)
    
    def test_module_analyze(self):
        analysis = analyze("Hello world. Test sentence.")
        self.assertIsInstance(analysis, TextAnalysis)
    
    def test_module_remove_html(self):
        result = remove_html("<p>Test</p>")
        self.assertEqual(result, "Test")
    
    def test_module_truncate(self):
        result = truncate("hello world", 8)
        self.assertEqual(len(result), 8)
    
    def test_module_similarity(self):
        sim = similarity("hello", "hello")
        self.assertEqual(sim, 1.0)
    
    def test_module_levenshtein(self):
        distance = levenshtein_distance("kitten", "sitting")
        self.assertEqual(distance, 3)
    
    def test_module_extract_words(self):
        words = extract_words("Hello, World!")
        self.assertEqual(words, ['Hello', 'World'])
    
    def test_module_split_sentences(self):
        sentences = split_sentences("Hello. World!")
        self.assertEqual(len(sentences), 2)
    
    def test_module_normalize_whitespace(self):
        result = normalize_whitespace("a  b\t\tc")
        self.assertEqual(result, "a b c")
    
    def test_module_hash(self):
        result = hash_text("test")
        self.assertEqual(len(result), 32)


class TestEdgeCases(unittest.TestCase):
    """Test edge cases and boundary conditions."""
    
    def setUp(self):
        self.utils = TextUtils()
    
    def test_empty_string(self):
        stats = self.utils.get_stats("")
        self.assertEqual(stats.word_count, 0)
    
    def test_whitespace_only(self):
        stats = self.utils.get_stats("   \t\n  ")
        self.assertEqual(stats.word_count, 0)
    
    def test_single_character(self):
        stats = self.utils.get_stats("a")
        self.assertEqual(stats.word_count, 1)
    
    def test_unicode_text(self):
        text = "你好世界 Hello 世界"
        words = self.utils.extract_words(text)
        self.assertGreater(len(words), 0)
    
    def test_very_long_word(self):
        word = "a" * 10000
        stats = self.utils.get_stats(word)
        self.assertEqual(stats.word_count, 1)
    
    def test_special_characters(self):
        text = "!@#$%^&*()_+-=[]{}|;':\",./<>?"
        cleaned = self.utils.clean(text, remove_punctuation=True)
        self.assertEqual(cleaned, "")
    
    def test_mixed_line_endings(self):
        text = "Line1\r\nLine2\rLine3\nLine4"
        normalized = self.utils.normalize_line_endings(text)
        self.assertNotIn('\r', normalized)


class TestCountSyllables(unittest.TestCase):
    """Test syllable counting."""
    
    def setUp(self):
        self.utils = TextUtils()
    
    def test_simple_words(self):
        self.assertEqual(self.utils.count_syllables("cat"), 1)
        self.assertEqual(self.utils.count_syllables("dog"), 1)
    
    def test_multi_syllable(self):
        self.assertGreater(self.utils.count_syllables("beautiful"), 1)
        self.assertGreater(self.utils.count_syllables("elephant"), 1)
    
    def test_silent_e(self):
        # Words ending in silent e
        self.assertEqual(self.utils.count_syllables("make"), 1)
        self.assertEqual(self.utils.count_syllables("like"), 1)


class TestStopWords(unittest.TestCase):
    """Test stop words functionality."""
    
    def test_custom_stop_words(self):
        custom_stops = {'custom', 'stop', 'words'}
        utils = TextUtils(stop_words=custom_stops)
        
        text = "This is a custom test with stop words"
        analysis = utils.analyze(text)
        
        # Custom stop words should be filtered from keywords
        self.assertNotIn('custom', analysis.keywords)
        self.assertNotIn('stop', analysis.keywords)
        self.assertNotIn('words', analysis.keywords)


def run_tests():
    """Run all tests and print results."""
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add all test classes
    test_classes = [
        TestTextCase,
        TestTextCleaning,
        TestTextFormatting,
        TestTextAnalysis,
        TestTextTransformation,
        TestTextSearch,
        TestTextComparison,
        TestHashing,
        TestModuleLevelFunctions,
        TestEdgeCases,
        TestCountSyllables,
        TestStopWords,
    ]
    
    for test_class in test_classes:
        tests = loader.loadTestsFromTestCase(test_class)
        suite.addTests(tests)
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Print summary
    print("\n" + "=" * 70)
    print("TEST SUMMARY")
    print("=" * 70)
    print(f"Tests run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print(f"Success: {result.wasSuccessful()}")
    
    if result.failures:
        print("\nFailures:")
        for test, traceback in result.failures:
            print(f"  - {test}")
    
    if result.errors:
        print("\nErrors:")
        for test, traceback in result.errors:
            print(f"  - {test}")
    
    return result.wasSuccessful()


if __name__ == '__main__':
    success = run_tests()
    sys.exit(0 if success else 1)
