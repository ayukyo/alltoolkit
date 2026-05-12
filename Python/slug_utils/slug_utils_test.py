"""
Tests for slug_utils module

Run with: python slug_utils_test.py
"""

import unittest
from mod import (
    slugify,
    slugify_unique,
    deslugify,
    is_valid_slug,
    slug_range,
    slug,
    url_slug,
    file_slug,
    transliterate,
)


class TestTransliterate(unittest.TestCase):
    """Tests for transliterate function."""
    
    def test_ascii_passthrough(self):
        """ASCII characters should pass through unchanged (case preserved)."""
        self.assertEqual(transliterate("hello"), "hello")
        self.assertEqual(transliterate("HELLO"), "HELLO")
        self.assertEqual(transliterate("Hello World 123"), "Hello World 123")
    
    def test_accented_characters(self):
        """Accented characters should be transliterated."""
        self.assertEqual(transliterate("café"), "cafe")
        self.assertEqual(transliterate("naïve"), "naive")
        self.assertEqual(transliterate("résumé"), "resume")
        self.assertEqual(transliterate("façade"), "facade")
    
    def test_german_characters(self):
        """German umlauts should be transliterated."""
        self.assertEqual(transliterate("größe"), "grosse")
        self.assertEqual(transliterate("übung"), "ubung")
        self.assertEqual(transliterate("käse"), "kase")
    
    def test_cyrillic_characters(self):
        """Cyrillic characters should be transliterated."""
        self.assertEqual(transliterate("привет"), "privet")
        self.assertEqual(transliterate("мир"), "mir")
        self.assertEqual(transliterate("спасибо"), "spasibo")
    
    def test_greek_characters(self):
        """Greek characters should be transliterated."""
        self.assertEqual(transliterate("αβγδ"), "abgd")
        self.assertEqual(transliterate("λόγος"), "logos")


class TestSlugify(unittest.TestCase):
    """Tests for slugify function."""
    
    def test_basic_slugify(self):
        """Test basic slug generation."""
        self.assertEqual(slugify("Hello World"), "hello-world")
        self.assertEqual(slugify("Hello, World!"), "hello-world")
        self.assertEqual(slugify("Hello    World"), "hello-world")
    
    def test_custom_separator(self):
        """Test custom separator."""
        self.assertEqual(slugify("Hello World", separator='_'), "hello_world")
        self.assertEqual(slugify("Hello World", separator='.'), "hello.world")
        self.assertEqual(slugify("Hello World", separator=''), "helloworld")
    
    def test_case_handling(self):
        """Test case handling options."""
        self.assertEqual(slugify("Hello WORLD"), "hello-world")
        self.assertEqual(slugify("Hello WORLD", lowercase=False), "Hello-WORLD")
        self.assertEqual(slugify("Hello World", lowercase=True), "hello-world")
    
    def test_special_characters(self):
        """Test special character handling."""
        self.assertEqual(slugify("Hello @#$ World"), "hello-world")
        self.assertEqual(slugify("Hello! World?"), "hello-world")
        self.assertEqual(slugify("Hello (World)"), "hello-world")
        self.assertEqual(slugify("Hello [World]"), "hello-world")
    
    def test_quotes_removal(self):
        """Test that quotes are removed entirely."""
        self.assertEqual(slugify("Don't Stop"), "dont-stop")
        self.assertEqual(slugify('She said "Hello"'), "she-said-hello")
        self.assertEqual(slugify("It's a test"), "its-a-test")
    
    def test_max_length(self):
        """Test max length truncation."""
        self.assertEqual(slugify("Hello World", max_length=5), "hello")
        self.assertEqual(slugify("Hello World", max_length=11), "hello-world")
        self.assertEqual(slugify("Hello World", max_length=50), "hello-world")
    
    def test_word_boundary(self):
        """Test word boundary preservation."""
        self.assertEqual(
            slugify("Hello World", max_length=8, word_boundary=True),
            "hello"
        )
        self.assertEqual(
            slugify("Hello Beautiful World", max_length=12, word_boundary=True),
            "hello"
        )
    
    def test_remove_words(self):
        """Test word removal."""
        self.assertEqual(
            slugify("The Quick Brown Fox", remove_words={'the'}),
            "quick-brown-fox"
        )
        self.assertEqual(
            slugify("A An The Test", remove_words={'a', 'an', 'the'}),
            "test"
        )
    
    def test_keep_chars(self):
        """Test keeping additional characters."""
        self.assertEqual(
            slugify("hello@world.com", keep_chars={'@', '.'}),
            "hello@world.com"
        )
        self.assertEqual(
            slugify("price: $100", keep_chars={'$'}),
            "price-$100"
        )
    
    def test_empty_string(self):
        """Test empty string handling."""
        self.assertEqual(slugify(""), "")
        self.assertEqual(slugify("   "), "")
        self.assertEqual(slugify("!!!"), "")
    
    def test_unicode_input(self):
        """Test Unicode character handling."""
        self.assertEqual(slugify("Café Restaurant"), "cafe-restaurant")
        self.assertEqual(slugify("naïve approach"), "naive-approach")
        self.assertEqual(slugify("Moscow: Москва"), "moscow-moskva")
    
    def test_multiple_separators(self):
        """Test consecutive separators are collapsed."""
        self.assertEqual(slugify("Hello---World"), "hello-world")
        self.assertEqual(slugify("Hello    World"), "hello-world")


class TestSlugifyUnique(unittest.TestCase):
    """Tests for slugify_unique function."""
    
    def test_unique_new_slug(self):
        """Test slug that doesn't exist yet."""
        existing = {"hello-world", "test-slug"}
        self.assertEqual(slugify_unique("New Title", existing), "new-title")
    
    def test_unique_duplicate_slug(self):
        """Test slug that already exists."""
        existing = {"hello-world"}
        self.assertEqual(slugify_unique("Hello World", existing), "hello-world-2")
    
    def test_unique_multiple_duplicates(self):
        """Test slug with multiple existing duplicates."""
        existing = {"hello-world", "hello-world-2", "hello-world-3"}
        self.assertEqual(slugify_unique("Hello World", existing), "hello-world-4")
    
    def test_unique_with_custom_separator(self):
        """Test unique slug with custom separator."""
        existing = {"hello_world"}
        self.assertEqual(
            slugify_unique("Hello World", existing, separator='_'),
            "hello_world_2"
        )


class TestDeslugify(unittest.TestCase):
    """Tests for deslugify function."""
    
    def test_basic_deslugify(self):
        """Test basic slug conversion back to string."""
        self.assertEqual(deslugify("hello-world"), "hello world")
        self.assertEqual(deslugify("hello_world", separator='_'), "hello world")
    
    def test_empty_slug(self):
        """Test empty slug."""
        self.assertEqual(deslugify(""), "")


class TestIsValidSlug(unittest.TestCase):
    """Tests for is_valid_slug function."""
    
    def test_valid_slugs(self):
        """Test valid slug recognition."""
        self.assertTrue(is_valid_slug("hello-world"))
        self.assertTrue(is_valid_slug("hello"))
        self.assertTrue(is_valid_slug("hello-world-123"))
        self.assertTrue(is_valid_slug("hello_world", separator='_'))
    
    def test_invalid_slugs(self):
        """Test invalid slug detection."""
        self.assertFalse(is_valid_slug("Hello World"))  # Space
        self.assertFalse(is_valid_slug("hello world"))  # Space
        self.assertFalse(is_valid_slug("hello!"))  # Special char
        self.assertFalse(is_valid_slug("hello@world"))  # Special char
        self.assertFalse(is_valid_slug(""))  # Empty
    
    def test_uppercase_option(self):
        """Test uppercase allowance option."""
        self.assertFalse(is_valid_slug("Hello-World"))
        self.assertTrue(is_valid_slug("Hello-World", allow_uppercase=True))
    
    def test_length_constraints(self):
        """Test min and max length constraints."""
        self.assertFalse(is_valid_slug("ab", min_length=3))
        self.assertTrue(is_valid_slug("abc", min_length=3))
        self.assertFalse(is_valid_slug("hello-world", max_length=5))
        self.assertTrue(is_valid_slug("hello", max_length=5))
    
    def test_separator_validation(self):
        """Test separator validation."""
        self.assertFalse(is_valid_slug("-hello"))  # Starts with separator
        self.assertFalse(is_valid_slug("hello-"))  # Ends with separator
        self.assertFalse(is_valid_slug("hello--world"))  # Double separator


class TestSlugRange(unittest.TestCase):
    """Tests for slug_range function."""
    
    def test_within_limit(self):
        """Test slug that's already within limit."""
        self.assertEqual(slug_range("Hello World", 20), "hello-world")
    
    def test_removes_filler_words(self):
        """Test filler word removal."""
        self.assertEqual(slug_range("The Quick Brown Fox", 15), "quick-brown-fox")
    
    def test_progressive_truncation(self):
        """Test progressive word removal."""
        # 'very' (4 chars) removed first, then 'here' (4 chars), then 'long' (4 chars)
        # Result: 'title' which is 5 chars
        result = slug_range("A Very Long Title Here", 12)
        self.assertEqual(len(result) <= 12, True)
        self.assertEqual(result, "very-title")
    
    def test_exact_length(self):
        """Test slug that exactly fits."""
        result = slug_range("Hello World", 11)
        self.assertEqual(len(result), 11)
        self.assertEqual(result, "hello-world")


class TestAliases(unittest.TestCase):
    """Tests for convenience aliases."""
    
    def test_slug_alias(self):
        """Test slug alias."""
        self.assertEqual(slug("Hello World"), "hello-world")
    
    def test_url_slug_alias(self):
        """Test url_slug alias."""
        self.assertEqual(url_slug("Hello World"), "hello-world")
    
    def test_file_slug_alias(self):
        """Test file_slug alias."""
        self.assertEqual(file_slug("Hello World"), "hello_world")


class TestEdgeCases(unittest.TestCase):
    """Tests for edge cases and special inputs."""
    
    def test_only_special_chars(self):
        """Test string with only special characters."""
        self.assertEqual(slugify("@#$%^&*()"), "")
        self.assertEqual(slugify("!!!???"), "")
    
    def test_numbers_preserved(self):
        """Test that numbers are preserved."""
        self.assertEqual(slugify("Hello 123 World"), "hello-123-world")
        self.assertEqual(slugify("2024 Year"), "2024-year")
    
    def test_mixed_case_numbers(self):
        """Test mixed case with numbers."""
        self.assertEqual(slugify("Test123CASE"), "test123case")
    
    def test_multiple_spaces(self):
        """Test multiple consecutive spaces."""
        self.assertEqual(slugify("Hello    World"), "hello-world")
    
    def test_leading_trailing_spaces(self):
        """Test leading and trailing spaces."""
        self.assertEqual(slugify("  Hello World  "), "hello-world")
    
    def test_leading_trailing_separators(self):
        """Test that result doesn't have leading/trailing separators."""
        result = slugify("-Hello World-")
        self.assertFalse(result.startswith('-'))
        self.assertFalse(result.endswith('-'))
    
    def test_very_long_string(self):
        """Test very long string handling."""
        long_text = " ".join(["word"] * 100)
        result = slugify(long_text)
        self.assertTrue(len(result) > 0)
        self.assertFalse(result.startswith('-'))
        self.assertFalse(result.endswith('-'))
    
    def test_japanese_characters(self):
        """Test Japanese characters (not in transliteration map)."""
        result = slugify("ユーザー認証")
        # Should produce something, even if empty for non-mapped chars
        self.assertIsInstance(result, str)


if __name__ == '__main__':
    # Run all tests
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromModule(__import__(__name__))
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Print summary
    print("\n" + "=" * 50)
    print(f"Tests run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print(f"Success rate: {((result.testsRun - len(result.failures) - len(result.errors)) / result.testsRun * 100):.1f}%")