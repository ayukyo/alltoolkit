#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AllToolkit - Slug Utilities Test Suite
=======================================
Comprehensive tests for the slug_utils module.
"""

import unittest
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from slug_utils.mod import (
    transliterate,
    normalize,
    generate_slug,
    generate_unique_slug,
    generate_sequential_slug,
    generate_date_slug,
    generate_category_slug,
    generate_hierarchical_slug,
    generate_slug_batch,
    slug_from_filename,
    is_valid_slug,
    fix_slug,
    slug_to_text,
    compare_slugs,
    get_slug_words,
    count_slug_words,
    SlugGenerator,
)


class TestTransliteration(unittest.TestCase):
    """Tests for transliteration functions."""
    
    def test_latin_characters(self):
        """Test Latin character transliteration."""
        self.assertEqual(transliterate("Héllo Wörld"), "Hello World")
        self.assertEqual(transliterate("Café"), "Cafe")
        self.assertEqual(transliterate("Naïve"), "Naive")
        self.assertEqual(transliterate("Ångström"), "Angstrom")
    
    def test_cyrillic_characters(self):
        """Test Cyrillic character transliteration."""
        self.assertEqual(transliterate("Привет"), "Privet")
        self.assertEqual(transliterate("Мир"), "Mir")
    
    def test_greek_characters(self):
        """Test Greek character transliteration."""
        self.assertEqual(transliterate("Γειά"), "Geia")
        # υ → y in our mapping
        self.assertIn("soy", transliterate("σου").lower())
    
    def test_mixed_characters(self):
        """Test mixed character sets."""
        result = transliterate("Café Привет")
        self.assertIn("Cafe", result)
        self.assertIn("Privet", result)
    
    def test_ascii_passthrough(self):
        """Test that ASCII passes through unchanged."""
        self.assertEqual(transliterate("Hello World"), "Hello World")
        self.assertEqual(transliterate("abc123"), "abc123")


class TestNormalize(unittest.TestCase):
    """Tests for normalize function."""
    
    def test_lowercase(self):
        """Test lowercase conversion."""
        self.assertEqual(normalize("HELLO"), "hello")
        self.assertEqual(normalize("HeLLo WoRLD"), "hello world")
    
    def test_no_lowercase(self):
        """Test without lowercase conversion."""
        self.assertEqual(normalize("HELLO", lowercase=False), "HELLO")
        self.assertEqual(normalize("HeLLo", lowercase=False), "HeLLo")
    
    def test_transliteration_in_normalize(self):
        """Test that normalize includes transliteration."""
        self.assertIn("hello", normalize("Héllo").lower())


class TestGenerateSlug(unittest.TestCase):
    """Tests for generate_slug function."""
    
    def test_basic_slug(self):
        """Test basic slug generation."""
        self.assertEqual(generate_slug("Hello World"), "hello-world")
        self.assertEqual(generate_slug("This is a test"), "this-is-a-test")
    
    def test_special_characters(self):
        """Test handling of special characters."""
        self.assertEqual(generate_slug("Hello! World?"), "hello-world")
        # @ is replaced with separator (not in WORD_MAP)
        self.assertEqual(generate_slug("Test@Example.com"), "test-example-com")
        self.assertEqual(generate_slug("Price: $100"), "price-100")
        # & is in WORD_MAP and becomes 'and'
        self.assertEqual(generate_slug("Tom & Jerry"), "tom-and-jerry")
    
    def test_custom_separator(self):
        """Test custom separator."""
        self.assertEqual(generate_slug("Hello World", separator="_"), "hello_world")
        self.assertEqual(generate_slug("Hello World", separator=""), "helloworld")
        self.assertEqual(generate_slug("Hello World", separator="."), "hello.world")
    
    def test_max_length(self):
        """Test maximum length constraint."""
        slug = generate_slug("This is a very long title", max_length=10)
        self.assertLessEqual(len(slug), 10)
        self.assertEqual(slug, "this-is-a")
    
    def test_max_length_word_boundary(self):
        """Test max length with word boundary."""
        slug = generate_slug("Hello Beautiful World", max_length=12)
        self.assertLessEqual(len(slug), 12)
        # Should cut at word boundary
    
    def test_empty_string(self):
        """Test empty string input."""
        self.assertEqual(generate_slug(""), "")
    
    def test_whitespace_only(self):
        """Test whitespace-only input."""
        self.assertEqual(generate_slug("   "), "")
    
    def test_numbers(self):
        """Test numbers in slug."""
        self.assertEqual(generate_slug("Test 123"), "test-123")
        self.assertEqual(generate_slug("2024 Report"), "2024-report")
    
    def test_multiple_spaces(self):
        """Test multiple spaces normalization."""
        self.assertEqual(generate_slug("Hello    World"), "hello-world")
    
    def test_custom_map(self):
        """Test custom character mappings."""
        custom = {"&": "and", "@": "at"}
        self.assertEqual(generate_slug("Tom & Jerry", custom_map=custom), "tom-and-jerry")
    
    def test_strip_common_words(self):
        """Test stripping common words."""
        slug = generate_slug("The Quick Brown Fox", strip_common_words=True)
        self.assertNotIn("the", slug)
    
    def test_allowed_chars(self):
        """Test additional allowed characters."""
        # When @ is allowed, it's preserved in the slug
        slug = generate_slug("test@example", allowed_chars="@")
        self.assertEqual(slug, "test@example")
        
        # When @ is NOT allowed, it becomes a separator
        slug = generate_slug("test@example")
        self.assertEqual(slug, "test-example")  # @ becomes separator


class TestUniqueSlug(unittest.TestCase):
    """Tests for generate_unique_slug function."""
    
    def test_no_conflict(self):
        """Test when no conflict exists."""
        result = generate_unique_slug("Hello World", [])
        self.assertEqual(result, "hello-world")
    
    def test_single_conflict(self):
        """Test with single conflict."""
        result = generate_unique_slug("Hello World", ["hello-world"])
        self.assertEqual(result, "hello-world-2")
    
    def test_multiple_conflicts(self):
        """Test with multiple conflicts."""
        existing = ["hello-world", "hello-world-2", "hello-world-3"]
        result = generate_unique_slug("Hello World", existing)
        self.assertEqual(result, "hello-world-4")
    
    def test_custom_separator(self):
        """Test unique slug with custom separator."""
        existing = ["hello_world"]
        result = generate_unique_slug("Hello World", existing, separator="_")
        self.assertEqual(result, "hello_world_2")
    
    def test_max_length_with_unique(self):
        """Test unique slug with max length."""
        existing = ["hello-world"]
        result = generate_unique_slug("Hello World Test", existing, max_length=15)
        self.assertLessEqual(len(result), 15)
        self.assertNotIn(result, existing)


class TestSequentialSlug(unittest.TestCase):
    """Tests for generate_sequential_slug function."""
    
    def test_basic_sequential(self):
        """Test basic sequential slug."""
        self.assertEqual(generate_sequential_slug("Blog Post", 1), "blog-post-1")
        self.assertEqual(generate_sequential_slug("Blog Post", 5), "blog-post-5")
    
    def test_zero_padding(self):
        """Test zero-padded sequential slug."""
        self.assertEqual(generate_sequential_slug("Post", 1, index_width=3), "post-001")
        self.assertEqual(generate_sequential_slug("Post", 100, index_width=3), "post-100")
    
    def test_custom_separator(self):
        """Test sequential slug with custom separator."""
        self.assertEqual(generate_sequential_slug("Post", 1, separator="_"), "post_1")


class TestDateSlug(unittest.TestCase):
    """Tests for generate_date_slug function."""
    
    def test_with_date(self):
        """Test slug with explicit date."""
        result = generate_date_slug("My Post", "2024-01-15")
        self.assertIn("2024-01-15", result)
        self.assertIn("my-post", result)
    
    def test_date_format(self):
        """Test custom date format."""
        result = generate_date_slug("My Post", "2024-01-15", date_format="%Y/%m/%d")
        self.assertIn("2024/01/15", result)
    
    def test_iso_format(self):
        """Test ISO date format."""
        result = generate_date_slug("Post", "2024-06-20")
        self.assertIn("2024-06-20", result)


class TestCategorySlug(unittest.TestCase):
    """Tests for generate_category_slug function."""
    
    def test_basic_category(self):
        """Test basic category slug."""
        result = generate_category_slug("My Post", "Tech")
        self.assertEqual(result, "tech-my-post")
    
    def test_category_with_separator(self):
        """Test category slug with custom separator."""
        result = generate_category_slug("My Post", "Tech", separator="_")
        self.assertEqual(result, "tech_my_post")


class TestHierarchicalSlug(unittest.TestCase):
    """Tests for generate_hierarchical_slug function."""
    
    def test_basic_hierarchical(self):
        """Test basic hierarchical slug."""
        result = generate_hierarchical_slug(["Tech", "Programming", "Python"])
        self.assertEqual(result, "tech/programming/python")
    
    def test_custom_path_separator(self):
        """Test custom path separator."""
        result = generate_hierarchical_slug(["A", "B", "C"], path_separator=">")
        self.assertEqual(result, "a>b>c")
    
    def test_empty_parts(self):
        """Test with empty parts."""
        result = generate_hierarchical_slug(["A", "", "B"])
        self.assertEqual(result, "a/b")


class TestBatchGeneration(unittest.TestCase):
    """Tests for generate_slug_batch function."""
    
    def test_basic_batch(self):
        """Test basic batch generation."""
        texts = ["Hello", "World", "Test"]
        result = generate_slug_batch(texts)
        self.assertEqual(result, ["hello", "world", "test"])
    
    def test_unique_batch(self):
        """Test unique batch generation."""
        texts = ["Hello", "Hello", "Hello"]
        result = generate_slug_batch(texts, ensure_unique=True)
        self.assertEqual(result, ["hello", "hello-2", "hello-3"])
    
    def test_non_unique_batch(self):
        """Test non-unique batch generation."""
        texts = ["Hello", "Hello", "Hello"]
        result = generate_slug_batch(texts, ensure_unique=False)
        self.assertEqual(result, ["hello", "hello", "hello"])


class TestFilenameSlug(unittest.TestCase):
    """Tests for slug_from_filename function."""
    
    def test_basic_filename(self):
        """Test basic filename conversion."""
        self.assertEqual(slug_from_filename("Document.pdf"), "document")
    
    def test_keep_extension(self):
        """Test keeping extension."""
        self.assertEqual(slug_from_filename("Document.pdf", remove_extension=False), "document-pdf")
    
    def test_complex_filename(self):
        """Test complex filename."""
        self.assertEqual(slug_from_filename("My Document (1).pdf"), "my-document-1")


class TestValidation(unittest.TestCase):
    """Tests for is_valid_slug function."""
    
    def test_valid_slugs(self):
        """Test valid slugs."""
        self.assertTrue(is_valid_slug("hello-world"))
        self.assertTrue(is_valid_slug("test123"))
        self.assertTrue(is_valid_slug("a-b-c"))
    
    def test_invalid_slugs(self):
        """Test invalid slugs."""
        self.assertFalse(is_valid_slug("hello world"))
        self.assertFalse(is_valid_slug("hello_world"))
        self.assertFalse(is_valid_slug(""))
        self.assertFalse(is_valid_slug("hello!"))
    
    def test_custom_separator(self):
        """Test validation with custom separator."""
        self.assertTrue(is_valid_slug("hello_world", separator="_"))
        self.assertFalse(is_valid_slug("hello-world", separator="_"))
    
    def test_allow_uppercase(self):
        """Test validation with uppercase allowed."""
        self.assertTrue(is_valid_slug("Hello-World", allow_uppercase=True))
        self.assertFalse(is_valid_slug("Hello-World", allow_uppercase=False))
    
    def test_max_length(self):
        """Test validation with max length."""
        self.assertTrue(is_valid_slug("hello", max_length=10))
        self.assertFalse(is_valid_slug("hello-world", max_length=5))


class TestFixSlug(unittest.TestCase):
    """Tests for fix_slug function."""
    
    def test_fix_spaces(self):
        """Test fixing spaces."""
        self.assertEqual(fix_slug("hello world"), "hello-world")
    
    def test_fix_underscores(self):
        """Test fixing underscores."""
        self.assertEqual(fix_slug("hello_world"), "hello-world")
    
    def test_fix_multiple_separators(self):
        """Test fixing multiple separators."""
        self.assertEqual(fix_slug("hello___world"), "hello-world")
    
    def test_fix_leading_trailing(self):
        """Test fixing leading/trailing separators."""
        self.assertEqual(fix_slug("-hello-world-"), "hello-world")
    
    def test_fix_invalid_chars(self):
        """Test removing invalid characters."""
        # Invalid chars are replaced with separator, then cleaned
        self.assertEqual(fix_slug("hello!@#world"), "hello-world")


class TestSlugToText(unittest.TestCase):
    """Tests for slug_to_text function."""
    
    def test_basic_conversion(self):
        """Test basic slug to text."""
        self.assertEqual(slug_to_text("hello-world"), "Hello World")
    
    def test_multiple_words(self):
        """Test multiple words."""
        self.assertEqual(slug_to_text("my-blog-post-2024"), "My Blog Post 2024")
    
    def test_custom_separator(self):
        """Test custom separator."""
        self.assertEqual(slug_to_text("hello_world", separator="_"), "Hello World")


class TestCompareSlugs(unittest.TestCase):
    """Tests for compare_slugs function."""
    
    def test_identical(self):
        """Test identical slugs."""
        self.assertTrue(compare_slugs("hello-world", "hello-world"))
    
    def test_case_difference(self):
        """Test case differences."""
        self.assertTrue(compare_slugs("Hello-World", "hello-world"))
        self.assertFalse(compare_slugs("Hello-World", "hello-world", ignore_case=False))
    
    def test_different(self):
        """Test different slugs."""
        self.assertFalse(compare_slugs("hello-world", "hello-world-2"))


class TestGetSlugWords(unittest.TestCase):
    """Tests for get_slug_words function."""
    
    def test_basic_words(self):
        """Test basic word extraction."""
        self.assertEqual(get_slug_words("hello-world"), ["hello", "world"])
    
    def test_empty_slug(self):
        """Test empty slug."""
        self.assertEqual(get_slug_words(""), [])
    
    def test_custom_separator(self):
        """Test custom separator."""
        self.assertEqual(get_slug_words("hello_world_test", separator="_"), 
                        ["hello", "world", "test"])


class TestCountSlugWords(unittest.TestCase):
    """Tests for count_slug_words function."""
    
    def test_word_count(self):
        """Test word counting."""
        self.assertEqual(count_slug_words("hello-world"), 2)
        self.assertEqual(count_slug_words("a-b-c-d"), 4)
    
    def test_empty_slug(self):
        """Test empty slug."""
        self.assertEqual(count_slug_words(""), 0)


class TestSlugGenerator(unittest.TestCase):
    """Tests for SlugGenerator class."""
    
    def test_basic_generation(self):
        """Test basic slug generation."""
        gen = SlugGenerator()
        self.assertEqual(gen.generate("Hello World"), "hello-world")
    
    def test_custom_settings(self):
        """Test with custom settings."""
        gen = SlugGenerator(separator="_", max_length=30)
        # Use short title to ensure underscore is present
        result = gen.generate("Hello World")
        self.assertEqual(result, "hello_world")
        # Test max_length truncation
        result = gen.generate("A Very Very Long Title")
        self.assertLessEqual(len(result), 30)
        self.assertIn("_", result)
    
    def test_unique_generation(self):
        """Test unique generation."""
        gen = SlugGenerator()
        slug1 = gen.generate_unique("Hello")
        slug2 = gen.generate_unique("Hello")
        self.assertNotEqual(slug1, slug2)
    
    def test_batch_generation(self):
        """Test batch generation."""
        gen = SlugGenerator()
        result = gen.generate_batch(["Hello", "World"])
        self.assertEqual(result, ["hello", "world"])
    
    def test_reset(self):
        """Test resetting generator."""
        gen = SlugGenerator()
        gen.generate_unique("Hello")
        gen.reset()
        self.assertEqual(len(gen._existing), 0)


class TestEdgeCases(unittest.TestCase):
    """Tests for edge cases."""
    
    def test_unicode_extreme(self):
        """Test extreme unicode characters."""
        # Test that it doesn't crash
        result = generate_slug("🎉 Party Time 🎊")
        self.assertIsInstance(result, str)
    
    def test_very_long_input(self):
        """Test very long input."""
        long_text = "a" * 1000
        result = generate_slug(long_text, max_length=100)
        self.assertLessEqual(len(result), 100)
    
    def test_numbers_only(self):
        """Test numbers only input."""
        self.assertEqual(generate_slug("123 456"), "123-456")
    
    def test_mixed_case(self):
        """Test mixed case input."""
        self.assertEqual(generate_slug("HeLLo WoRLD"), "hello-world")
    
    def test_consecutive_separators(self):
        """Test consecutive separators in input."""
        self.assertEqual(generate_slug("Hello---World"), "hello-world")


if __name__ == "__main__":
    # Run tests with verbosity
    unittest.main(verbosity=2)