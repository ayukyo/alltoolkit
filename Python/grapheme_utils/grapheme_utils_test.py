"""
Tests for Grapheme Cluster Utilities

Run with: python -m pytest grapheme_utils_test.py -v
Or: python grapheme_utils_test.py
"""

import unittest
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from grapheme_utils.mod import (
    grapheme_count, grapheme_split, grapheme_slice, grapheme_reverse,
    grapheme_at, grapheme_index, grapheme_find, grapheme_contains,
    grapheme_replace, grapheme_info, grapheme_equal, truncate_graphemes,
    pad_graphemes, is_combining_mark, is_variation_selector, is_zwj,
    is_regional_indicator, is_emoji_modifier, normalize_graphemes,
    graphemes_to_code_points, code_points_to_graphemes,
    grapheme_length_in_bytes, graphemes
)


class TestBasicGraphemes(unittest.TestCase):
    """Tests for basic ASCII and simple Unicode graphemes."""
    
    def test_empty_string(self):
        """Test empty string handling."""
        self.assertEqual(grapheme_count(""), 0)
        self.assertEqual(grapheme_split(""), [])
        self.assertEqual(list(graphemes("")), [])
    
    def test_ascii_string(self):
        """Test ASCII string."""
        text = "Hello"
        self.assertEqual(grapheme_count(text), 5)
        self.assertEqual(grapheme_split(text), ['H', 'e', 'l', 'l', 'o'])
    
    def test_ascii_with_spaces(self):
        """Test ASCII with spaces."""
        text = "Hello World"
        self.assertEqual(grapheme_count(text), 11)
        self.assertEqual(grapheme_split(text), ['H', 'e', 'l', 'l', 'o', ' ', 'W', 'o', 'r', 'l', 'd'])
    
    def test_ascii_with_numbers(self):
        """Test ASCII with numbers."""
        text = "Test123"
        self.assertEqual(grapheme_count(text), 7)
    
    def test_ascii_with_punctuation(self):
        """Test ASCII with punctuation."""
        text = "Hello, World!"
        self.assertEqual(grapheme_count(text), 13)


class TestCombiningCharacters(unittest.TestCase):
    """Tests for combining characters."""
    
    def test_latin_with_acute(self):
        """Test Latin letter with combining acute accent."""
        # 'é' as 'e' + combining acute accent
        text = "e\u0301"
        self.assertEqual(grapheme_count(text), 1)
        # The grapheme cluster is 'e' + combining accent (2 code points, 1 grapheme)
        clusters = grapheme_split(text)
        self.assertEqual(len(clusters), 1)
        self.assertEqual(len(clusters[0]), 2)  # 2 code points
    
    def test_latin_with_multiple_diacritics(self):
        """Test Latin letter with multiple combining marks."""
        # 'e' with acute and diaeresis
        text = "e\u0301\u0308"
        self.assertEqual(grapheme_count(text), 1)
    
    def test_cafe_with_combining(self):
        """Test 'café' with combining accent."""
        text = "cafe\u0301"  # cafe + combining acute
        self.assertEqual(grapheme_count(text), 4)
    
    def test_precomposed_vs_combining(self):
        """Test precomposed vs decomposed forms are grapheme-equivalent."""
        # Precomposed 'é' vs 'e' + combining acute
        precomposed = "é"
        decomposed = "e\u0301"
        
        # After normalization, they should be equal
        self.assertTrue(grapheme_equal(precomposed, decomposed))


class TestEmoji(unittest.TestCase):
    """Tests for emoji handling."""
    
    def test_simple_emoji(self):
        """Test simple emoji."""
        text = "😀"
        self.assertEqual(grapheme_count(text), 1)
    
    def test_emoji_sequence(self):
        """Test sequence of simple emoji."""
        text = "😀👍🎉"
        self.assertEqual(grapheme_count(text), 3)
        self.assertEqual(grapheme_split(text), ['😀', '👍', '🎉'])
    
    def test_zwj_sequence_family(self):
        """Test family emoji (ZWJ sequence)."""
        # Family: man, woman, girl, boy
        text = "👨‍👩‍👧‍👦"
        self.assertEqual(grapheme_count(text), 1)
        split_result = grapheme_split(text)
        self.assertEqual(len(split_result), 1)
    
    def test_zwj_sequence_couple(self):
        """Test couple emoji (ZWJ sequence)."""
        # Couple with heart
        text = "👩‍❤️‍👨"
        self.assertEqual(grapheme_count(text), 1)
    
    def test_emoji_with_skin_tone(self):
        """Test emoji with skin tone modifier."""
        # Thumbs up with medium skin tone
        text = "👍🏽"
        self.assertEqual(grapheme_count(text), 1)
    
    def test_emoji_with_text(self):
        """Test emoji mixed with text."""
        text = "Hello 👋 World"
        self.assertEqual(grapheme_count(text), 13)
        self.assertEqual(grapheme_split(text)[6], '👋')


class TestFlagEmoji(unittest.TestCase):
    """Tests for flag emoji (regional indicators)."""
    
    def test_us_flag(self):
        """Test US flag emoji."""
        text = "🇺🇸"
        self.assertEqual(grapheme_count(text), 1)
    
    def test_multiple_flags(self):
        """Test multiple flag emoji."""
        text = "🇺🇸🇬🇧🇫🇷"  # US, UK, France - Note: may be combined depending on implementation
        self.assertEqual(grapheme_count(text), 3)  # Each flag should be 2 regional indicators
        self.assertEqual(len(grapheme_split(text)), 3)
    
    def test_flag_with_text(self):
        """Test flag with text."""
        text = "USA 🇺🇸"
        self.assertEqual(grapheme_count(text), 5)  # "USA " + 1 flag


class TestComplexScripts(unittest.TestCase):
    """Tests for complex script handling."""
    
    def test_devanagari(self):
        """Test Devanagari (Hindi) text."""
        text = "नमस्ते"  # "namaste"
        # Should be treated as 4 graphemes
        self.assertEqual(grapheme_count(text), 4)
    
    def test_arabic(self):
        """Test Arabic text."""
        text = "مرحبا"  # "hello"
        self.assertEqual(grapheme_count(text), 5)
    
    def test_thai(self):
        """Test Thai text."""
        text = "สวัสดี"  # "hello"
        self.assertGreater(grapheme_count(text), 0)
    
    def test_chinese(self):
        """Test Chinese characters."""
        text = "中文测试"
        self.assertEqual(grapheme_count(text), 4)
    
    def test_japanese(self):
        """Test Japanese text (hiragana, katakana, kanji)."""
        text = "こんにちは世界"
        self.assertEqual(grapheme_count(text), 7)


class TestGraphemeSlice(unittest.TestCase):
    """Tests for grapheme slicing."""
    
    def test_slice_basic(self):
        """Test basic slicing."""
        text = "Hello World"
        self.assertEqual(grapheme_slice(text, 0, 5), "Hello")
        self.assertEqual(grapheme_slice(text, 6), "World")
        self.assertEqual(grapheme_slice(text, 0, 1), "H")
    
    def test_slice_emoji(self):
        """Test slicing with emoji."""
        text = "👨‍👩‍👧‍👦Hello"
        self.assertEqual(grapheme_slice(text, 0, 1), "👨‍👩‍👧‍👦")
        self.assertEqual(grapheme_slice(text, 1, 3), "He")
    
    def test_slice_negative(self):
        """Test negative indices are not supported."""
        text = "Hello"
        # Negative indices should work via Python list slicing
        clusters = grapheme_split(text)
        self.assertEqual(''.join(clusters[-3:]), "llo")
    
    def test_slice_out_of_bounds(self):
        """Test out of bounds slicing."""
        text = "Hi"
        self.assertEqual(grapheme_slice(text, 0, 10), "Hi")
        self.assertEqual(grapheme_slice(text, 5, 10), "")


class TestGraphemeReverse(unittest.TestCase):
    """Tests for grapheme reversal."""
    
    def test_reverse_basic(self):
        """Test basic reversal."""
        self.assertEqual(grapheme_reverse("hello"), "olleh")
    
    def test_reverse_with_spaces(self):
        """Test reversal with spaces."""
        self.assertEqual(grapheme_reverse("hello world"), "dlrow olleh")
    
    def test_reverse_with_emoji(self):
        """Test reversal with emoji."""
        text = "👋👨‍👩‍👧‍👦"
        reversed_text = grapheme_reverse(text)
        self.assertEqual(grapheme_count(reversed_text), 2)
    
    def test_reverse_with_combining(self):
        """Test reversal with combining characters."""
        text = "cafe\u0301"  # cafe + combining acute
        reversed_text = grapheme_reverse(text)
        self.assertEqual(grapheme_count(reversed_text), 4)


class TestGraphemeFind(unittest.TestCase):
    """Tests for grapheme finding."""
    
    def test_find_basic(self):
        """Test basic finding."""
        text = "Hello World"
        self.assertEqual(grapheme_find(text, "World"), 6)
        self.assertEqual(grapheme_find(text, "Hello"), 0)
    
    def test_find_not_found(self):
        """Test finding when not present."""
        text = "Hello"
        self.assertEqual(grapheme_find(text, "xyz"), -1)
    
    def test_find_emoji(self):
        """Test finding with emoji."""
        text = "👋Hello"
        self.assertEqual(grapheme_find(text, "Hello"), 1)
        self.assertEqual(grapheme_find(text, "👋"), 0)
    
    def test_contains(self):
        """Test contains method."""
        text = "Hello World"
        self.assertTrue(grapheme_contains(text, "World"))
        self.assertFalse(grapheme_contains(text, "xyz"))


class TestGraphemeReplace(unittest.TestCase):
    """Tests for grapheme replacement."""
    
    def test_replace_basic(self):
        """Test basic replacement."""
        text = "hello hello"
        self.assertEqual(grapheme_replace(text, "ll", "pp"), "heppo heppo")
    
    def test_replace_with_count(self):
        """Test replacement with count."""
        text = "hello hello"
        self.assertEqual(grapheme_replace(text, "l", "x", 2), "hexxo hello")
    
    def test_replace_emoji(self):
        """Test replacement with emoji."""
        text = "Hello 👋"
        self.assertEqual(grapheme_replace(text, "👋", "World"), "Hello World")


class TestGraphemeInfo(unittest.TestCase):
    """Tests for grapheme info."""
    
    def test_info_ascii(self):
        """Test info for ASCII."""
        info = grapheme_info("Hi")
        self.assertEqual(len(info), 2)
        self.assertEqual(info[0]['grapheme'], 'H')
        self.assertEqual(info[0]['code_points'], [72])
        self.assertEqual(info[0]['length_code_points'], 1)
    
    def test_info_emoji(self):
        """Test info for emoji."""
        info = grapheme_info("👨‍👩‍👧‍👦")
        self.assertEqual(len(info), 1)
        self.assertTrue(info[0]['is_emoji'])
        self.assertTrue(info[0]['has_zwj'])
        self.assertGreater(len(info[0]['code_points']), 1)


class TestTruncate(unittest.TestCase):
    """Tests for truncation."""
    
    def test_truncate_no_change(self):
        """Test when no truncation needed."""
        text = "Hello"
        self.assertEqual(truncate_graphemes(text, 10), "Hello")
    
    def test_truncate_basic(self):
        """Test basic truncation."""
        text = "Hello World"
        self.assertEqual(truncate_graphemes(text, 5), "Hello...")
    
    def test_truncate_emoji(self):
        """Test truncation with emoji."""
        text = "👨‍👩‍👧‍👦 Family"
        truncated = truncate_graphemes(text, 2)
        self.assertTrue(truncated.startswith("👨‍👩‍👧‍👦"))


class TestPad(unittest.TestCase):
    """Tests for padding."""
    
    def test_pad_right(self):
        """Test right padding."""
        self.assertEqual(pad_graphemes("Hi", 5), "Hi   ")
    
    def test_pad_left(self):
        """Test left padding."""
        self.assertEqual(pad_graphemes("Hi", 5, side='left'), "   Hi")
    
    def test_pad_center(self):
        """Test center padding."""
        self.assertEqual(pad_graphemes("Hi", 6, side='center'), "  Hi  ")
    
    def test_pad_no_change(self):
        """Test when no padding needed."""
        self.assertEqual(pad_graphemes("Hello", 3), "Hello")
    
    def test_pad_invalid_side(self):
        """Test invalid side parameter."""
        with self.assertRaises(ValueError):
            pad_graphemes("Hi", 5, side='invalid')


class TestUtilityFunctions(unittest.TestCase):
    """Tests for utility functions."""
    
    def test_is_combining_mark(self):
        """Test combining mark detection."""
        self.assertTrue(is_combining_mark('\u0301'))  # Combining acute
        self.assertFalse(is_combining_mark('a'))
    
    def test_is_variation_selector(self):
        """Test variation selector detection."""
        self.assertTrue(is_variation_selector('\uFE0F'))  # VS16
        self.assertFalse(is_variation_selector('a'))
    
    def test_is_zwj(self):
        """Test ZWJ detection."""
        self.assertTrue(is_zwj('\u200D'))
        self.assertFalse(is_zwj('a'))
    
    def test_is_regional_indicator(self):
        """Test regional indicator detection."""
        self.assertTrue(is_regional_indicator('🇦'))
        self.assertFalse(is_regional_indicator('a'))
    
    def test_is_emoji_modifier(self):
        """Test emoji modifier detection."""
        self.assertTrue(is_emoji_modifier('\U0001F3FB'))  # Light skin tone
        self.assertFalse(is_emoji_modifier('a'))
    
    def test_code_points_conversion(self):
        """Test code points conversion."""
        text = "Hi"
        cps = graphemes_to_code_points(text)
        self.assertEqual(cps, [72, 105])
        self.assertEqual(code_points_to_graphemes(cps), text)
    
    def test_normalize(self):
        """Test normalization."""
        # Different ways to write é
        precomposed = "é"
        decomposed = "e\u0301"
        
        # After NFC normalization, they should be the same
        self.assertEqual(normalize_graphemes(precomposed), 
                        normalize_graphemes(decomposed))


class TestGraphemeAt(unittest.TestCase):
    """Tests for grapheme_at function."""
    
    def test_at_basic(self):
        """Test basic grapheme_at."""
        self.assertEqual(grapheme_at("Hello", 0), "H")
        self.assertEqual(grapheme_at("Hello", 4), "o")
    
    def test_at_emoji(self):
        """Test grapheme_at with emoji."""
        text = "👨‍👩‍👧‍👦Hello"
        self.assertEqual(grapheme_at(text, 0), "👨‍👩‍👧‍👦")
        self.assertEqual(grapheme_at(text, 1), "H")
    
    def test_at_out_of_bounds(self):
        """Test out of bounds access."""
        with self.assertRaises(IndexError):
            grapheme_at("Hi", 10)


class TestGraphemeIndex(unittest.TestCase):
    """Tests for grapheme_index function."""
    
    def test_index_basic(self):
        """Test basic index finding."""
        self.assertEqual(grapheme_index("Hello", "l"), 2)
    
    def test_index_not_found(self):
        """Test index not found."""
        with self.assertRaises(ValueError):
            grapheme_index("Hello", "z")
    
    def test_index_emoji(self):
        """Test index with emoji."""
        text = "Hi 👨‍👩‍👧‍👦"
        self.assertEqual(grapheme_index(text, "👨‍👩‍👧‍👦"), 3)


class TestByteLength(unittest.TestCase):
    """Tests for byte length calculations."""
    
    def test_ascii_bytes(self):
        """Test ASCII byte length."""
        self.assertEqual(grapheme_length_in_bytes("Hello"), [1, 1, 1, 1, 1])
    
    def test_unicode_bytes(self):
        """Test Unicode byte length."""
        # Chinese characters are 3 bytes each in UTF-8
        self.assertEqual(grapheme_length_in_bytes("中文"), [3, 3])
    
    def test_emoji_bytes(self):
        """Test emoji byte length."""
        lengths = grapheme_length_in_bytes("😀")
        self.assertGreater(lengths[0], 1)


class TestIterator(unittest.TestCase):
    """Tests for the graphemes iterator."""
    
    def test_iterator_basic(self):
        """Test basic iteration."""
        text = "Hi"
        result = list(graphemes(text))
        self.assertEqual(result, ['H', 'i'])
    
    def test_iterator_emoji(self):
        """Test iteration with emoji."""
        text = "👋Hi"
        result = list(graphemes(text))
        self.assertEqual(len(result), 3)
        self.assertEqual(result[0], '👋')


class TestEdgeCases(unittest.TestCase):
    """Tests for edge cases."""
    
    def test_single_char(self):
        """Test single character."""
        self.assertEqual(grapheme_count("a"), 1)
        self.assertEqual(grapheme_split("a"), ['a'])
    
    def test_newlines(self):
        """Test newlines and special characters."""
        text = "a\nb"
        self.assertEqual(grapheme_count(text), 3)
    
    def test_tabs(self):
        """Test tabs."""
        text = "a\tb"
        self.assertEqual(grapheme_count(text), 3)
    
    def test_mixed_content(self):
        """Test mixed content."""
        text = "Hello 👋 World 中文 🇺🇸"
        count = grapheme_count(text)
        self.assertGreater(count, 0)
        
        # Make sure all graphemes are captured
        split_result = grapheme_split(text)
        self.assertEqual(len(split_result), count)


if __name__ == '__main__':
    unittest.main(verbosity=2)