"""
Comprehensive tests for BWT (Burrows-Wheeler Transform) Utilities.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import unittest
from bwt_utils.mod import (
    bwt_transform, bwt_inverse,
    mtf_encode, mtf_decode,
    bwt_mtf_compress, bwt_mtf_decompress,
    bwt_search, bwt_compress_ratio,
    BWT, transform, inverse
)


class TestBWTTransform(unittest.TestCase):
    """Tests for basic BWT forward and inverse transforms."""
    
    def test_simple_string(self):
        """Test BWT with simple strings."""
        test_cases = [
            "banana",
            "abracadabra",
            "mississippi",
        ]
        
        for s in test_cases:
            with self.subTest(s=s):
                transformed, idx = bwt_transform(s)
                recovered = bwt_inverse(transformed, idx)
                self.assertEqual(recovered, s)
    
    def test_single_char(self):
        """Test BWT with single character."""
        s = "a"
        transformed, idx = bwt_transform(s)
        recovered = bwt_inverse(transformed, idx)
        self.assertEqual(recovered, s)
    
    def test_empty_string(self):
        """Test BWT with empty string."""
        s = ""
        transformed, idx = bwt_transform(s)
        # Empty string becomes just "$"
        self.assertEqual(transformed, "$")
        self.assertEqual(idx, 0)
        recovered = bwt_inverse(transformed, idx)
        self.assertEqual(recovered, "")
    
    def test_repeated_chars(self):
        """Test BWT with repeated characters."""
        test_cases = [
            "aaaa",
            "bbbbbbbb",
            "abababab",
        ]
        
        for s in test_cases:
            with self.subTest(s=s):
                transformed, idx = bwt_transform(s)
                recovered = bwt_inverse(transformed, idx)
                self.assertEqual(recovered, s)
    
    def test_with_spaces(self):
        """Test BWT with spaces and special chars."""
        test_cases = [
            "hello world",
            "foo bar baz",
            "a b c d e",
        ]
        
        for s in test_cases:
            with self.subTest(s=s):
                transformed, idx = bwt_transform(s)
                recovered = bwt_inverse(transformed, idx)
                self.assertEqual(recovered, s)
    
    def test_unicode(self):
        """Test BWT with unicode characters."""
        test_cases = [
            "こんにちは",
            "你好世界",
            "🎉🎊🎈",
        ]
        
        for s in test_cases:
            with self.subTest(s=s):
                transformed, idx = bwt_transform(s)
                recovered = bwt_inverse(transformed, idx)
                self.assertEqual(recovered, s)
    
    def test_bytes(self):
        """Test BWT with bytes input."""
        data = b"banana\x00binary"
        transformed, idx = bwt_transform(data)
        recovered = bwt_inverse(transformed, idx)
        self.assertEqual(recovered, data)
    
    def test_long_string(self):
        """Test BWT with longer string."""
        s = "the quick brown fox jumps over the lazy dog " * 10
        transformed, idx = bwt_transform(s)
        recovered = bwt_inverse(transformed, idx)
        self.assertEqual(recovered, s)
    
    def test_known_transform(self):
        """Test known BWT results."""
        # "banana$" sorted rotations:
        # $banana, a$banan, ana$ban, anana$b, banana$, na$bana, nana$ba
        # Last column: annb$aa, index of original "banana$" is 4 (not 3 as in some references)
        transformed, idx = bwt_transform("banana")
        self.assertEqual(idx, 4)  # Correct index for this sorting order
        self.assertEqual(len(transformed), 7)  # 6 + $


class TestMTFEncodeDecode(unittest.TestCase):
    """Tests for Move-to-Front encoding and decoding."""
    
    def test_basic_encode(self):
        """Test basic MTF encoding."""
        # With alphabet "ab", encoding "aaabbbaaa":
        # a at 0 -> 0, alphabet stays [a,b]
        # a at 0 -> 0, alphabet stays [a,b]
        # a at 0 -> 0, alphabet stays [a,b]
        # b at 1 -> 1, alphabet becomes [b,a]
        # b at 0 -> 0, alphabet stays [b,a]
        # b at 0 -> 0, alphabet stays [b,a]
        # a at 1 -> 1, alphabet becomes [a,b]
        # a at 0 -> 0, alphabet stays [a,b]
        # a at 0 -> 0, alphabet stays [a,b]
        codes = mtf_encode("aaabbbaaa")
        self.assertEqual(codes, [0, 0, 0, 1, 0, 0, 1, 0, 0])
    
    def test_basic_decode(self):
        """Test basic MTF decoding."""
        result = mtf_decode([0, 0, 0, 1, 0, 0, 1, 0, 0], "ab")
        self.assertEqual(result, "aaabbbaaa")
    
    def test_roundtrip(self):
        """Test MTF encode/decode roundtrip."""
        test_cases = [
            "hello",
            "mississippi",
            "abracadabra",
            "aaaa",
        ]
        
        for s in test_cases:
            with self.subTest(s=s):
                codes = mtf_encode(s)
                # Use alphabet in order of first appearance (default behavior)
                alphabet = ''.join(dict.fromkeys(s))  # Preserves order, removes duplicates
                result = mtf_decode(codes, alphabet)
                self.assertEqual(result, s)
    
    def test_custom_alphabet(self):
        """Test MTF with custom alphabet."""
        codes = mtf_encode("abc", "cba")
        self.assertEqual(codes, [2, 2, 2])
    
    def test_bytes_mtf(self):
        """Test MTF with bytes."""
        data = b"\x01\x01\x02\x02"
        codes = mtf_encode(data)
        alphabet = bytes(sorted(set(data)))
        result = mtf_decode(codes, alphabet)
        self.assertEqual(result, data)
    
    def test_repeated_pattern(self):
        """Test MTF with highly repetitive pattern."""
        s = "a" * 100 + "b" * 100
        codes = mtf_encode(s)
        # After first 'a', all 'a's should be 0
        # After switching to 'b', 'b' moves to front, so code 0
        # Then all remaining 'b's should be 0
        self.assertEqual(codes[:100], [0] * 100)


class TestCombinedTransforms(unittest.TestCase):
    """Tests for combined BWT + MTF transforms."""
    
    def test_compress_decompress_string(self):
        """Test combined BWT+MTF compress/decompress."""
        test_cases = [
            "banana",
            "mississippi",
            "abracadabra",
            "the quick brown fox",
        ]
        
        for s in test_cases:
            with self.subTest(s=s):
                codes, index, alphabet = bwt_mtf_compress(s)
                recovered = bwt_mtf_decompress(codes, index, alphabet)
                self.assertEqual(recovered, s)
    
    def test_compress_decompress_bytes(self):
        """Test combined transforms with bytes."""
        data = b"\x00\x01\x02\x01\x00" * 20
        codes, index, alphabet = bwt_mtf_compress(data)
        recovered = bwt_mtf_decompress(codes, index, alphabet)
        self.assertEqual(recovered, data)
    
    def test_small_codes_after_bwt(self):
        """Test that BWT+MTF produces many small codes."""
        # Text with repeating patterns should produce many 0s and 1s
        s = "abcabcabcabcabcabcabc"
        codes, _, _ = bwt_mtf_compress(s)
        small_code_count = sum(1 for c in codes if c < 3)
        self.assertGreater(small_code_count / len(codes), 0.5)


class TestBWTSearch(unittest.TestCase):
    """Tests for BWT-based pattern search."""
    
    def test_find_single_match(self):
        """Test finding single occurrence."""
        text = "hello world"
        positions = bwt_search(text, "world")
        self.assertEqual(positions, [6])
    
    def test_find_multiple_matches(self):
        """Test finding multiple occurrences."""
        text = "banana"
        positions = bwt_search(text, "ana")
        self.assertEqual(sorted(positions), [1, 3])
    
    def test_find_overlapping(self):
        """Test finding overlapping patterns."""
        text = "aaaa"
        positions = bwt_search(text, "aa")
        self.assertEqual(sorted(positions), [0, 1, 2])
    
    def test_find_none(self):
        """Test when pattern not found."""
        text = "hello world"
        positions = bwt_search(text, "xyz")
        self.assertEqual(positions, [])
    
    def test_empty_pattern(self):
        """Test with empty pattern."""
        positions = bwt_search("hello", "")
        self.assertEqual(positions, [])
    
    def test_longer_than_text(self):
        """Test pattern longer than text."""
        positions = bwt_search("hi", "hello")
        self.assertEqual(positions, [])
    
    def test_pattern_at_start(self):
        """Test pattern at text start."""
        text = "hello world"
        positions = bwt_search(text, "hello")
        self.assertEqual(positions, [0])
    
    def test_pattern_at_end(self):
        """Test pattern at text end."""
        text = "hello world"
        positions = bwt_search(text, "world")
        self.assertEqual(positions, [6])


class TestBWTAnalysis(unittest.TestCase):
    """Tests for BWT compression analysis."""
    
    def test_repetitive_text(self):
        """Test analysis of repetitive text."""
        analysis = bwt_compress_ratio("a" * 100)
        self.assertEqual(analysis['compression_potential'], 'high')
        self.assertGreater(analysis['small_code_ratio'], 0.9)
    
    def test_random_like_text(self):
        """Test analysis of less compressible text."""
        analysis = bwt_compress_ratio("abcdefghijklmnopqrstuvwxyz")
        # Less repetitive, lower small code ratio
        self.assertIn(analysis['compression_potential'], ['low', 'medium', 'high'])
    
    def test_analysis_structure(self):
        """Test analysis returns expected fields."""
        analysis = bwt_compress_ratio("test string")
        self.assertIn('original_length', analysis)
        self.assertIn('transformed_length', analysis)
        self.assertIn('alphabet_size', analysis)
        self.assertIn('compression_potential', analysis)


class TestBWTClass(unittest.TestCase):
    """Tests for object-oriented BWT interface."""
    
    def test_basic_usage(self):
        """Test basic BWT class usage."""
        bwt = BWT("banana")
        transformed = bwt.transform()
        recovered = BWT.inverse(transformed, bwt.index)
        self.assertEqual(recovered, "banana")
    
    def test_lazy_transform(self):
        """Test lazy evaluation of transform."""
        bwt = BWT("test")
        # Access index before transform
        idx = bwt.index
        self.assertIsNotNone(idx)
        self.assertIsNotNone(bwt._transformed)
    
    def test_search_method(self):
        """Test search through BWT class."""
        bwt = BWT("banana")
        positions = bwt.search("ana")
        self.assertEqual(sorted(positions), [1, 3])
    
    def test_analyze_method(self):
        """Test analyze through BWT class."""
        bwt = BWT("aaaa")
        analysis = bwt.analyze()
        self.assertEqual(analysis['compression_potential'], 'high')


class TestConvenienceFunctions(unittest.TestCase):
    """Tests for convenience aliases."""
    
    def test_transform_alias(self):
        """Test transform alias."""
        t1, i1 = bwt_transform("test")
        t2, i2 = transform("test")
        self.assertEqual(t1, t2)
        self.assertEqual(i1, i2)
    
    def test_inverse_alias(self):
        """Test inverse alias."""
        transformed, idx = bwt_transform("test")
        r1 = bwt_inverse(transformed, idx)
        r2 = inverse(transformed, idx)
        self.assertEqual(r1, r2)


class TestEdgeCases(unittest.TestCase):
    """Tests for edge cases and error handling."""
    
    def test_sentinel_in_input(self):
        """Test handling of sentinel character in input."""
        # The '$' is used as sentinel, but should still work
        s = "test$string"
        transformed, idx = bwt_transform(s)
        recovered = bwt_inverse(transformed, idx)
        self.assertEqual(recovered, s)
    
    def test_newlines(self):
        """Test with newlines."""
        s = "line1\nline2\nline3"
        transformed, idx = bwt_transform(s)
        recovered = bwt_inverse(transformed, idx)
        self.assertEqual(recovered, s)
    
    def test_mixed_content(self):
        """Test with mixed content types."""
        s = "Hello 123 !@# 世界 🎉"
        transformed, idx = bwt_transform(s)
        recovered = bwt_inverse(transformed, idx)
        self.assertEqual(recovered, s)


if __name__ == "__main__":
    unittest.main(verbosity=2)