"""
Tests for Lorem Ipsum Generator
================================

Comprehensive test suite for lorem_utils module.

Run with: python -m pytest lorem_utils_test.py -v
Or simply: python lorem_utils_test.py
"""

import unittest
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from lorem_utils import (
    LoremGenerator,
    words, sentence, sentences, paragraph, paragraphs,
    title, headline, html_paragraphs, list_items,
    buzzword, buzzwords, email, username, url, phone,
    address, name, company, generate
)


class TestLoremGenerator(unittest.TestCase):
    """Tests for LoremGenerator class."""
    
    def test_words_default(self):
        """Test default word generation."""
        gen = LoremGenerator(seed=42)
        result = gen.words()
        self.assertIsInstance(result, str)
        self.assertEqual(len(result.split()), 5)
        self.assertTrue(result[0].isupper())  # First word capitalized
    
    def test_words_custom_count(self):
        """Test custom word count."""
        gen = LoremGenerator(seed=42)
        for count in [1, 10, 50, 100]:
            result = gen.words(count)
            self.assertEqual(len(result.split()), count)
    
    def test_words_as_list(self):
        """Test word generation as list."""
        gen = LoremGenerator(seed=42)
        result = gen.words(5, as_list=True)
        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 5)
    
    def test_words_no_capitalize(self):
        """Test words without capitalization."""
        gen = LoremGenerator(seed=42)
        result = gen.words(5, capitalize_first=False)
        self.assertFalse(result[0].isupper())
    
    def test_sentence_default(self):
        """Test default sentence generation."""
        gen = LoremGenerator(seed=42)
        result = gen.sentence()
        self.assertIsInstance(result, str)
        self.assertTrue(result.endswith(('.', '!', '?')))
        self.assertTrue(result[0].isupper())
        word_count = len(result.rstrip('.!?').split())
        self.assertGreaterEqual(word_count, 8)
        self.assertLessEqual(word_count, 15)
    
    def test_sentence_custom_length(self):
        """Test custom sentence length."""
        gen = LoremGenerator(seed=42)
        result = gen.sentence(min_words=3, max_words=5)
        word_count = len(result.rstrip('.!?').split())
        self.assertGreaterEqual(word_count, 3)
        self.assertLessEqual(word_count, 5)
    
    def test_sentences_default(self):
        """Test default sentences generation."""
        gen = LoremGenerator(seed=42)
        result = gen.sentences(3)
        self.assertIsInstance(result, str)
        # Count sentence endings
        endings = sum(1 for c in result if c in '.!?')
        self.assertEqual(endings, 3)
    
    def test_sentences_as_list(self):
        """Test sentences as list."""
        gen = LoremGenerator(seed=42)
        result = gen.sentences(3, as_list=True)
        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 3)
        for s in result:
            self.assertTrue(s.endswith(('.', '!', '?')))
    
    def test_paragraph_default(self):
        """Test default paragraph generation."""
        gen = LoremGenerator(seed=42)
        result = gen.paragraph()
        self.assertIsInstance(result, str)
        # Should have multiple sentences
        endings = sum(1 for c in result if c in '.!?')
        self.assertGreaterEqual(endings, 4)
        self.assertLessEqual(endings, 7)
    
    def test_paragraphs_default(self):
        """Test default paragraphs generation."""
        gen = LoremGenerator(seed=42)
        result = gen.paragraphs(2)
        self.assertIsInstance(result, str)
        # Should have paragraph separator
        self.assertIn('\n\n', result)
    
    def test_paragraphs_as_list(self):
        """Test paragraphs as list."""
        gen = LoremGenerator(seed=42)
        result = gen.paragraphs(3, as_list=True)
        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 3)
    
    def test_paragraphs_custom_separator(self):
        """Test custom paragraph separator."""
        gen = LoremGenerator(seed=42)
        result = gen.paragraphs(2, separator='|||')
        self.assertIn('|||', result)
    
    def test_title(self):
        """Test title generation."""
        gen = LoremGenerator(seed=42)
        result = gen.title()
        self.assertIsInstance(result, str)
        self.assertFalse(result.endswith('.'))
        # All words should be capitalized
        words_list = result.split()
        for word in words_list:
            self.assertTrue(word[0].isupper())
    
    def test_headline(self):
        """Test headline generation."""
        gen = LoremGenerator(seed=42)
        result = gen.headline()
        self.assertIsInstance(result, str)
        word_count = len(result.split())
        self.assertGreaterEqual(word_count, 4)
        self.assertLessEqual(word_count, 8)
    
    def test_html_paragraphs(self):
        """Test HTML paragraphs generation."""
        gen = LoremGenerator(seed=42)
        result = gen.html_paragraphs(2)
        self.assertIn('<p>', result)
        self.assertIn('</p>', result)
        self.assertEqual(result.count('<p>'), 2)
    
    def test_html_paragraphs_custom_tag(self):
        """Test HTML paragraphs with custom tag."""
        gen = LoremGenerator(seed=42)
        result = gen.html_paragraphs(2, wrap_tag='div')
        self.assertIn('<div>', result)
        self.assertIn('</div>', result)
    
    def test_list_items_unordered(self):
        """Test unordered list items."""
        gen = LoremGenerator(seed=42)
        result = gen.list_items(5, ordered=False)
        self.assertIn('•', result)
        lines = result.split('\n')
        self.assertEqual(len(lines), 5)
    
    def test_list_items_ordered(self):
        """Test ordered list items."""
        gen = LoremGenerator(seed=42)
        result = gen.list_items(5, ordered=True)
        self.assertIn('1.', result)
        self.assertIn('5.', result)
    
    def test_buzzword(self):
        """Test buzzword generation."""
        gen = LoremGenerator(seed=42)
        result = gen.buzzword()
        self.assertIsInstance(result, str)
        self.assertTrue(result[0].isupper())
    
    def test_buzzwords(self):
        """Test multiple buzzwords."""
        gen = LoremGenerator(seed=42)
        result = gen.buzzwords(4)
        self.assertIsInstance(result, str)
        self.assertEqual(len(result.split(',')), 4)
    
    def test_email(self):
        """Test email generation."""
        gen = LoremGenerator(seed=42)
        result = gen.email()
        self.assertIn('@', result)
        self.assertIn('example.com', result)
    
    def test_email_custom_domain(self):
        """Test email with custom domain."""
        gen = LoremGenerator(seed=42)
        result = gen.email(domain='test.org')
        self.assertIn('test.org', result)
    
    def test_username(self):
        """Test username generation."""
        gen = LoremGenerator(seed=42)
        result = gen.username()
        self.assertIsInstance(result, str)
        self.assertGreater(len(result), 0)
    
    def test_url(self):
        """Test URL generation."""
        gen = LoremGenerator(seed=42)
        result = gen.url()
        self.assertIn('https://', result)
        self.assertIn('example.com', result)
    
    def test_url_custom_domain(self):
        """Test URL with custom domain."""
        gen = LoremGenerator(seed=42)
        result = gen.url(domain='mysite.io')
        self.assertIn('mysite.io', result)
    
    def test_phone(self):
        """Test phone number generation."""
        gen = LoremGenerator(seed=42)
        result = gen.phone()
        self.assertIsInstance(result, str)
        # Should match format (XXX) XXX-XXXX
        import re
        self.assertTrue(re.match(r'\(\d{3}\) \d{3}-\d{4}', result))
    
    def test_address(self):
        """Test address generation."""
        gen = LoremGenerator(seed=42)
        result = gen.address()
        self.assertIsInstance(result, str)
        self.assertGreater(len(result), 0)
    
    def test_name(self):
        """Test name generation."""
        gen = LoremGenerator(seed=42)
        result = gen.name()
        self.assertIsInstance(result, str)
        words_list = result.split()
        self.assertEqual(len(words_list), 2)
        for word in words_list:
            self.assertTrue(word[0].isupper())
    
    def test_company(self):
        """Test company name generation."""
        gen = LoremGenerator(seed=42)
        result = gen.company()
        self.assertIsInstance(result, str)
        # Should have a suffix
        suffixes = ['Inc', 'LLC', 'Corp', 'Ltd', 'Co', 'Group']
        has_suffix = any(result.endswith(s) for s in suffixes)
        self.assertTrue(has_suffix)
    
    def test_reproducible_with_seed(self):
        """Test that same seed produces same output."""
        gen1 = LoremGenerator(seed=12345)
        gen2 = LoremGenerator(seed=12345)
        
        result1 = gen1.paragraph()
        result2 = gen2.paragraph()
        
        self.assertEqual(result1, result2)
    
    def test_different_seeds_different_output(self):
        """Test that different seeds produce different output."""
        gen1 = LoremGenerator(seed=1)
        gen2 = LoremGenerator(seed=2)
        
        result1 = gen1.paragraph()
        result2 = gen2.paragraph()
        
        self.assertNotEqual(result1, result2)
    
    def test_reset_seed(self):
        """Test seed reset functionality."""
        gen = LoremGenerator(seed=42)
        result1 = gen.words(10)
        
        gen.reset_seed(42)
        result2 = gen.words(10)
        
        self.assertEqual(result1, result2)
    
    def test_extended_word_pool(self):
        """Test extended word pool option."""
        gen = LoremGenerator(seed=42, use_extended=True)
        result = gen.words(10)
        self.assertIsInstance(result, str)
        self.assertEqual(len(result.split()), 10)


class TestConvenienceFunctions(unittest.TestCase):
    """Tests for module-level convenience functions."""
    
    def test_words_function(self):
        """Test words() function."""
        result = words(5, seed=42)
        self.assertIsInstance(result, str)
        self.assertEqual(len(result.split()), 5)
    
    def test_sentence_function(self):
        """Test sentence() function."""
        result = sentence(seed=42)
        self.assertIsInstance(result, str)
        self.assertTrue(result.endswith(('.', '!', '?')))
    
    def test_sentences_function(self):
        """Test sentences() function."""
        result = sentences(3, seed=42)
        self.assertIsInstance(result, str)
        endings = sum(1 for c in result if c in '.!?')
        self.assertEqual(endings, 3)
    
    def test_paragraph_function(self):
        """Test paragraph() function."""
        result = paragraph(seed=42)
        self.assertIsInstance(result, str)
        self.assertGreater(len(result), 0)
    
    def test_paragraphs_function(self):
        """Test paragraphs() function."""
        result = paragraphs(2, seed=42)
        self.assertIsInstance(result, str)
        self.assertIn('\n\n', result)
    
    def test_title_function(self):
        """Test title() function."""
        result = title(seed=42)
        self.assertIsInstance(result, str)
        self.assertFalse(result.endswith('.'))
    
    def test_headline_function(self):
        """Test headline() function."""
        result = headline(seed=42)
        self.assertIsInstance(result, str)
    
    def test_html_paragraphs_function(self):
        """Test html_paragraphs() function."""
        result = html_paragraphs(2, seed=42)
        self.assertIn('<p>', result)
        self.assertIn('</p>', result)
    
    def test_list_items_function(self):
        """Test list_items() function."""
        result = list_items(5, seed=42)
        self.assertIn('•', result)
    
    def test_buzzword_function(self):
        """Test buzzword() function."""
        result = buzzword(seed=42)
        self.assertIsInstance(result, str)
    
    def test_buzzwords_function(self):
        """Test buzzwords() function."""
        result = buzzwords(4, seed=42)
        self.assertEqual(len(result.split(',')), 4)
    
    def test_email_function(self):
        """Test email() function."""
        result = email(seed=42)
        self.assertIn('@', result)
    
    def test_username_function(self):
        """Test username() function."""
        result = username(seed=42)
        self.assertIsInstance(result, str)
    
    def test_url_function(self):
        """Test url() function."""
        result = url(seed=42)
        self.assertIn('https://', result)
    
    def test_phone_function(self):
        """Test phone() function."""
        result = phone(seed=42)
        import re
        self.assertTrue(re.match(r'\(\d{3}\) \d{3}-\d{4}', result))
    
    def test_address_function(self):
        """Test address() function."""
        result = address(seed=42)
        self.assertIsInstance(result, str)
    
    def test_name_function(self):
        """Test name() function."""
        result = name(seed=42)
        self.assertEqual(len(result.split()), 2)
    
    def test_company_function(self):
        """Test company() function."""
        result = company(seed=42)
        self.assertIsInstance(result, str)
    
    def test_generate_function(self):
        """Test generate() function with various types."""
        # Test all content types
        types = [
            ('words', 5),
            ('sentence', None),
            ('sentences', 3),
            ('paragraph', None),
            ('paragraphs', 2),
            ('title', None),
            ('headline', None),
            ('html_paragraphs', 2),
            ('list_items', 5),
            ('buzzword', None),
            ('buzzwords', 4),
            ('email', None),
            ('username', None),
            ('url', None),
            ('phone', None),
            ('address', None),
            ('name', None),
            ('company', None),
        ]
        
        for content_type, count in types:
            if count is not None:
                result = generate(content_type, count=count, seed=42)
            else:
                result = generate(content_type, seed=42)
            
            self.assertIsInstance(result, str, f"Failed for type: {content_type}")
            self.assertGreater(len(result), 0, f"Empty result for type: {content_type}")
    
    def test_generate_invalid_type(self):
        """Test generate() with invalid type."""
        with self.assertRaises(ValueError):
            generate('invalid_type')


class TestEdgeCases(unittest.TestCase):
    """Tests for edge cases and boundary conditions."""
    
    def test_zero_words(self):
        """Test zero word request."""
        gen = LoremGenerator(seed=42)
        result = gen.words(0)
        self.assertEqual(result, '')
    
    def test_single_word(self):
        """Test single word request."""
        gen = LoremGenerator(seed=42)
        result = gen.words(1)
        self.assertEqual(len(result.split()), 1)
    
    def test_large_word_count(self):
        """Test large word count."""
        gen = LoremGenerator(seed=42)
        result = gen.words(1000)
        self.assertEqual(len(result.split()), 1000)
    
    def test_zero_sentences(self):
        """Test zero sentence request."""
        gen = LoremGenerator(seed=42)
        result = gen.sentences(0)
        self.assertEqual(result, '')
    
    def test_zero_paragraphs(self):
        """Test zero paragraph request."""
        gen = LoremGenerator(seed=42)
        result = gen.paragraphs(0)
        self.assertEqual(result, '')
    
    def test_single_paragraph(self):
        """Test single paragraph."""
        gen = LoremGenerator(seed=42)
        result = gen.paragraphs(1)
        self.assertIsInstance(result, str)
        self.assertNotIn('\n\n', result)  # No separator for single paragraph
    
    def test_minimum_sentence_length(self):
        """Test minimum sentence length."""
        gen = LoremGenerator(seed=42)
        result = gen.sentence(min_words=1, max_words=1)
        words = result.rstrip('.!?').split()
        self.assertEqual(len(words), 1)
    
    def test_minimum_paragraph_length(self):
        """Test minimum paragraph length."""
        gen = LoremGenerator(seed=42)
        result = gen.paragraph(min_sentences=1, max_sentences=1)
        endings = sum(1 for c in result if c in '.!?')
        self.assertEqual(endings, 1)
    
    def test_empty_list_items(self):
        """Test zero list items."""
        gen = LoremGenerator(seed=42)
        result = gen.list_items(0)
        self.assertEqual(result, '')


class TestReproducibility(unittest.TestCase):
    """Tests for reproducibility with seeds."""
    
    def test_seed_reproducibility_words(self):
        """Test seed reproducibility for words."""
        result1 = words(10, seed=12345)
        result2 = words(10, seed=12345)
        self.assertEqual(result1, result2)
    
    def test_seed_reproducibility_paragraphs(self):
        """Test seed reproducibility for paragraphs."""
        result1 = paragraphs(3, seed=12345)
        result2 = paragraphs(3, seed=12345)
        self.assertEqual(result1, result2)
    
    def test_seed_reproducibility_fake_data(self):
        """Test seed reproducibility for fake data."""
        gen1 = LoremGenerator(seed=999)
        gen2 = LoremGenerator(seed=999)
        
        self.assertEqual(gen1.name(), gen2.name())
        self.assertEqual(gen1.email(), gen2.email())
        self.assertEqual(gen1.phone(), gen2.phone())
        self.assertEqual(gen1.address(), gen2.address())


if __name__ == '__main__':
    # Run tests with verbosity
    unittest.main(verbosity=2)