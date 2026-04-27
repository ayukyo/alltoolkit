#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AllToolkit - Huffman Coding Utilities Test Module

Comprehensive tests for all Huffman coding functions.

Author: AllToolkit Contributors
License: MIT
"""

import sys
import os
import unittest
import math

# Add module directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mod import (
    HuffmanNode, HuffmanTree,
    build_frequency_table, build_huffman_tree,
    encode_text, decode_text,
    encode_bytes, decode_bytes,
    generate_canonical_codes,
    calculate_compression_ratio, calculate_compression_percentage,
    get_code_statistics,
    bits_to_bytes, bytes_to_bits,
    serialize_tree, deserialize_tree,
    visualize_tree,
    huffman_encode, huffman_decode,
    analyze_compression_potential,
    compare_with_fixed_length
)


class TestHuffmanNode(unittest.TestCase):
    """Tests for HuffmanNode class."""
    
    def test_leaf_node_creation(self):
        """Test creating a leaf node."""
        node = HuffmanNode(symbol='a', frequency=5)
        self.assertEqual(node.symbol, 'a')
        self.assertEqual(node.frequency, 5)
        self.assertTrue(node.is_leaf())
    
    def test_internal_node_creation(self):
        """Test creating an internal node."""
        left = HuffmanNode(symbol='a', frequency=3)
        right = HuffmanNode(symbol='b', frequency=2)
        internal = HuffmanNode(frequency=5, left=left, right=right)
        self.assertIsNone(internal.symbol)
        self.assertEqual(internal.frequency, 5)
        self.assertFalse(internal.is_leaf())
    
    def test_node_comparison(self):
        """Test node comparison for priority queue."""
        node1 = HuffmanNode(symbol='a', frequency=3)
        node2 = HuffmanNode(symbol='b', frequency=5)
        self.assertTrue(node1 < node2)
        self.assertTrue(node1 <= node2)
        self.assertTrue(node2 > node1)
        self.assertFalse(node1 == node2)


class TestHuffmanTree(unittest.TestCase):
    """Tests for HuffmanTree class."""
    
    def test_empty_tree(self):
        """Test empty tree creation."""
        tree = HuffmanTree()
        self.assertIsNone(tree.root)
        self.assertEqual(tree.code_table, {})
    
    def test_single_symbol_tree(self):
        """Test tree with single symbol."""
        tree = build_huffman_tree({'a': 5})
        self.assertIsNotNone(tree.root)
        self.assertIn('a', tree.code_table)
        # Single symbol should have code '0'
        self.assertEqual(tree.code_table['a'], '0')
    
    def test_two_symbol_tree(self):
        """Test tree with two symbols."""
        tree = build_huffman_tree({'a': 5, 'b': 3})
        self.assertIsNotNone(tree.root)
        self.assertEqual(len(tree.code_table), 2)
        # Codes should be distinct
        codes = list(tree.code_table.values())
        self.assertEqual(len(set(codes)), 2)
    
    def test_multiple_symbol_tree(self):
        """Test tree with multiple symbols."""
        tree = build_huffman_tree({'a': 5, 'b': 2, 'c': 1, 'd': 1})
        self.assertIsNotNone(tree.root)
        self.assertEqual(len(tree.code_table), 4)
        # All codes should be unique
        codes = list(tree.code_table.values())
        self.assertEqual(len(set(codes)), 4)
        # Most frequent symbol should have shortest code
        a_code_len = len(tree.code_table['a'])
        for symbol, code in tree.code_table.items():
            if symbol != 'a':
                self.assertLessEqual(a_code_len, len(code))


class TestBuildFrequencyTable(unittest.TestCase):
    """Tests for frequency table building."""
    
    def test_simple_string(self):
        """Test frequency table for simple string."""
        freq = build_frequency_table("hello")
        self.assertEqual(freq['h'], 1)
        self.assertEqual(freq['e'], 1)
        self.assertEqual(freq['l'], 2)
        self.assertEqual(freq['o'], 1)
    
    def test_empty_string(self):
        """Test frequency table for empty string."""
        freq = build_frequency_table("")
        self.assertEqual(freq, {})
    
    def test_single_character(self):
        """Test frequency table for single character."""
        freq = build_frequency_table("aaaaa")
        self.assertEqual(freq['a'], 5)
        self.assertEqual(len(freq), 1)
    
    def test_bytes_mode(self):
        """Test frequency table for bytes."""
        freq = build_frequency_table(b"hello", byte_mode=True)
        self.assertEqual(freq[ord('h')], 1)
        self.assertEqual(freq[ord('l')], 2)


class TestEncodeDecodeText(unittest.TestCase):
    """Tests for text encoding and decoding."""
    
    def test_simple_text(self):
        """Test encoding and decoding simple text."""
        text = "hello"
        encoded, tree = encode_text(text)
        decoded = decode_text(encoded, tree)
        self.assertEqual(decoded, text)
    
    def test_empty_text(self):
        """Test encoding empty text."""
        encoded, tree = encode_text("")
        self.assertEqual(encoded, "")
        decoded = decode_text(encoded, tree)
        self.assertEqual(decoded, "")
    
    def test_single_character(self):
        """Test encoding single character."""
        text = "a"
        encoded, tree = encode_text(text)
        decoded = decode_text(encoded, tree)
        self.assertEqual(decoded, text)
    
    def test_repeated_character(self):
        """Test encoding repeated character."""
        text = "aaaaa"
        encoded, tree = encode_text(text)
        decoded = decode_text(encoded, tree)
        self.assertEqual(decoded, text)
    
    def test_all_ascii_characters(self):
        """Test encoding all printable ASCII characters."""
        text = "".join(chr(i) for i in range(32, 127))
        encoded, tree = encode_text(text)
        decoded = decode_text(encoded, tree)
        self.assertEqual(decoded, text)
    
    def test_unicode_text(self):
        """Test encoding Unicode text."""
        text = "你好世界 🌍"
        encoded, tree = encode_text(text)
        decoded = decode_text(encoded, tree)
        self.assertEqual(decoded, text)
    
    def test_prebuilt_tree(self):
        """Test using a pre-built tree."""
        text1 = "aaabbc"
        text2 = "abc"
        
        # Build tree from first text
        freq = build_frequency_table(text1)
        tree = build_huffman_tree(freq)
        
        # Encode second text with same tree
        encoded, _ = encode_text(text2, tree)
        decoded = decode_text(encoded, tree)
        self.assertEqual(decoded, text2)


class TestEncodeDecodeBytes(unittest.TestCase):
    """Tests for bytes encoding and decoding."""
    
    def test_simple_bytes(self):
        """Test encoding and decoding simple bytes."""
        data = b"hello world"
        encoded, tree, padding = encode_bytes(data)
        decoded = decode_bytes(encoded, tree, padding)
        self.assertEqual(decoded, data)
    
    def test_empty_bytes(self):
        """Test encoding empty bytes."""
        encoded, tree, padding = encode_bytes(b"")
        self.assertEqual(encoded, b"")
        decoded = decode_bytes(encoded, tree, padding)
        self.assertEqual(decoded, b"")
    
    def test_binary_data(self):
        """Test encoding binary data."""
        data = bytes(range(256))
        encoded, tree, padding = encode_bytes(data)
        decoded = decode_bytes(encoded, tree, padding)
        self.assertEqual(decoded, data)
    
    def test_single_byte(self):
        """Test encoding single byte."""
        data = b"x"
        encoded, tree, padding = encode_bytes(data)
        decoded = decode_bytes(encoded, tree, padding)
        self.assertEqual(decoded, data)
    
    def test_repeated_byte(self):
        """Test encoding repeated byte."""
        data = b"aaaaa"
        encoded, tree, padding = encode_bytes(data)
        decoded = decode_bytes(encoded, tree, padding)
        self.assertEqual(decoded, data)


class TestCanonicalCodes(unittest.TestCase):
    """Tests for canonical Huffman codes."""
    
    def test_simple_lengths(self):
        """Test generating canonical codes from lengths."""
        lengths = {'a': 1, 'b': 2, 'c': 2}
        codes = generate_canonical_codes(lengths)
        self.assertEqual(len(codes), 3)
        # All codes should be unique
        code_values = list(codes.values())
        self.assertEqual(len(set(code_values)), 3)
    
    def test_various_lengths(self):
        """Test canonical codes with various lengths."""
        lengths = {'a': 2, 'b': 2, 'c': 3, 'd': 3, 'e': 3}
        codes = generate_canonical_codes(lengths)
        # Check no prefix conflicts
        code_list = sorted(codes.values(), key=len)
        for i, code1 in enumerate(code_list):
            for code2 in code_list[i+1:]:
                # No code should be a prefix of another
                self.assertFalse(code2.startswith(code1) or code1.startswith(code2))


class TestCompressionCalculations(unittest.TestCase):
    """Tests for compression calculations."""
    
    def test_compression_ratio_no_compression(self):
        """Test compression ratio with no compression."""
        ratio = calculate_compression_ratio(100, 100)
        self.assertEqual(ratio, 1.0)
    
    def test_compression_ratio_half(self):
        """Test compression ratio with 50% compression."""
        ratio = calculate_compression_ratio(100, 50)
        self.assertEqual(ratio, 2.0)
    
    def test_compression_ratio_zero_original(self):
        """Test compression ratio with zero original size."""
        ratio = calculate_compression_ratio(0, 0)
        self.assertEqual(ratio, 1.0)
    
    def test_compression_percentage_half(self):
        """Test compression percentage with 50% compression."""
        percentage = calculate_compression_percentage(100, 50)
        self.assertEqual(percentage, 50.0)
    
    def test_compression_percentage_none(self):
        """Test compression percentage with no compression."""
        percentage = calculate_compression_percentage(100, 100)
        self.assertEqual(percentage, 0.0)


class TestCodeStatistics(unittest.TestCase):
    """Tests for code statistics."""
    
    def test_statistics_simple(self):
        """Test statistics for simple tree."""
        tree = build_huffman_tree({'a': 5, 'b': 2, 'c': 1})
        stats = get_code_statistics(tree)
        
        self.assertEqual(stats['num_symbols'], 3)
        self.assertEqual(stats['min_code_length'], 1)
        self.assertGreater(stats['average_code_length'], 0)
    
    def test_statistics_empty(self):
        """Test statistics for empty tree."""
        tree = HuffmanTree()
        stats = get_code_statistics(tree)
        
        self.assertEqual(stats['num_symbols'], 0)
        self.assertEqual(stats['min_code_length'], 0)
        self.assertEqual(stats['max_code_length'], 0)


class TestBitsBytesConversion(unittest.TestCase):
    """Tests for bits to bytes conversion."""
    
    def test_full_bytes(self):
        """Test conversion with full bytes."""
        bits = "0110100110010110"
        data, padding = bits_to_bytes(bits)
        self.assertEqual(padding, 0)
        recovered = bytes_to_bits(data, padding)
        self.assertEqual(recovered, bits)
    
    def test_partial_byte(self):
        """Test conversion with partial byte."""
        bits = "01101"
        data, padding = bits_to_bytes(bits)
        self.assertEqual(padding, 3)
        recovered = bytes_to_bits(data, padding)
        self.assertEqual(recovered, bits)
    
    def test_empty_bits(self):
        """Test conversion with empty bits."""
        data, padding = bits_to_bytes("")
        self.assertEqual(data, b"")
        self.assertEqual(padding, 0)
    
    def test_roundtrip(self):
        """Test roundtrip conversion."""
        for bits in ["0", "01", "011", "0110", "01101", "011010"]:
            data, padding = bits_to_bytes(bits)
            recovered = bytes_to_bits(data, padding)
            self.assertEqual(recovered, bits)


class TestTreeSerialization(unittest.TestCase):
    """Tests for tree serialization."""
    
    def test_serialize_deserialize(self):
        """Test serialization and deserialization."""
        tree = build_huffman_tree({'a': 5, 'b': 2, 'c': 1})
        data = serialize_tree(tree)
        restored = deserialize_tree(data)
        
        self.assertEqual(restored.code_table, tree.code_table)
    
    def test_empty_tree(self):
        """Test serializing empty tree."""
        tree = HuffmanTree()
        data = serialize_tree(tree)
        restored = deserialize_tree(data)
        
        self.assertIsNone(restored.root)
        self.assertEqual(restored.code_table, {})
    
    def test_single_symbol(self):
        """Test serializing single symbol tree."""
        tree = build_huffman_tree({'x': 10})
        data = serialize_tree(tree)
        restored = deserialize_tree(data)
        
        self.assertEqual(restored.code_table['x'], tree.code_table['x'])
    
    def test_preserves_encoding(self):
        """Test that serialization preserves encoding capability."""
        original = "this is a test message"
        tree = build_huffman_tree(build_frequency_table(original))
        
        # Encode with original tree
        encoded1, _ = encode_text(original, tree)
        
        # Serialize and deserialize
        data = serialize_tree(tree)
        restored = deserialize_tree(data)
        
        # Encode with restored tree (using same code table)
        encoded2, _ = encode_text(original, restored)
        
        self.assertEqual(encoded1, encoded2)


class TestVisualizeTree(unittest.TestCase):
    """Tests for tree visualization."""
    
    def test_visualize_simple(self):
        """Test visualizing simple tree."""
        tree = build_huffman_tree({'a': 5, 'b': 2, 'c': 1})
        viz = visualize_tree(tree)
        self.assertIsInstance(viz, str)
        self.assertIn('(', viz)  # Contains tree structure
    
    def test_visualize_empty(self):
        """Test visualizing empty tree."""
        tree = HuffmanTree()
        viz = visualize_tree(tree)
        self.assertEqual(viz, "(empty tree)")


class TestConvenienceFunctions(unittest.TestCase):
    """Tests for convenience functions."""
    
    def test_huffman_encode_decode_string(self):
        """Test one-shot encoding/decoding of string."""
        text = "hello world"
        encoded, tree_data, padding = huffman_encode(text)
        decoded = huffman_decode(encoded, tree_data, padding)
        self.assertEqual(decoded, text)
    
    def test_huffman_encode_decode_bytes(self):
        """Test one-shot encoding/decoding of bytes."""
        data = b"binary\x00\x01\xff data"
        encoded, tree_data, padding = huffman_encode(data)
        decoded = huffman_decode(encoded, tree_data, padding)
        self.assertEqual(decoded, data)
    
    def test_huffman_encode_empty(self):
        """Test encoding empty data."""
        encoded, tree_data, padding = huffman_encode("")
        self.assertEqual(encoded, b"")
        decoded = huffman_decode(encoded, tree_data, padding)
        self.assertEqual(decoded, "")


class TestCompressionAnalysis(unittest.TestCase):
    """Tests for compression analysis."""
    
    def test_analyze_simple_text(self):
        """Test analysis of simple text."""
        analysis = analyze_compression_potential("aaabbc")
        self.assertIn('compression_ratio', analysis)
        self.assertIn('compression_percentage', analysis)
        self.assertIn('entropy_bits', analysis)
        self.assertGreater(analysis['entropy_bits'], 0)
    
    def test_analyze_uniform_distribution(self):
        """Test analysis with uniform distribution."""
        # All characters equally frequent
        analysis = analyze_compression_potential("abcdef")
        # Should have lower compression than skewed distribution
        self.assertGreater(analysis['entropy_bits'], 2)
    
    def test_analyze_skewed_distribution(self):
        """Test analysis with skewed distribution."""
        # One character very frequent
        analysis = analyze_compression_potential("aaaaaab")
        # Should have lower entropy (more compressible)
        self.assertLess(analysis['entropy_bits'], 2)
    
    def test_analyze_empty(self):
        """Test analysis of empty data."""
        analysis = analyze_compression_potential("")
        self.assertEqual(analysis['original_size'], 0)
        self.assertEqual(analysis['compressed_size'], 0)


class TestCompareWithFixedLength(unittest.TestCase):
    """Tests for comparison with fixed-length encoding."""
    
    def test_comparison_simple(self):
        """Test comparison with simple tree."""
        tree = build_huffman_tree({'a': 5, 'b': 2, 'c': 1})
        comparison = compare_with_fixed_length(tree, 100)
        
        self.assertIn('huffman_bits_per_symbol', comparison)
        self.assertIn('fixed_bits_per_symbol', comparison)
        self.assertIn('savings_percent', comparison)
    
    def test_single_symbol(self):
        """Test comparison with single symbol."""
        tree = build_huffman_tree({'a': 100})
        comparison = compare_with_fixed_length(tree, 100)
        
        self.assertEqual(comparison['huffman_bits_per_symbol'], 1)
        self.assertEqual(comparison['fixed_bits_per_symbol'], 1)


class TestEdgeCases(unittest.TestCase):
    """Tests for edge cases."""
    
    def test_very_long_text(self):
        """Test encoding very long text."""
        text = "a" * 10000 + "b" * 5000 + "c" * 1000
        encoded, tree = encode_text(text)
        decoded = decode_text(encoded, tree)
        self.assertEqual(decoded, text)
    
    def test_all_same_character(self):
        """Test encoding text with all same character."""
        text = "x" * 1000
        encoded, tree = encode_text(text)
        decoded = decode_text(encoded, tree)
        self.assertEqual(decoded, text)
    
    def test_binary_data_all_bytes(self):
        """Test encoding binary data with all possible bytes."""
        data = bytes(range(256)) * 2
        encoded, tree, padding = encode_bytes(data)
        decoded = decode_bytes(encoded, tree, padding)
        self.assertEqual(decoded, data)
    
    def test_alternating_characters(self):
        """Test encoding alternating characters."""
        text = "ab" * 1000
        encoded, tree = encode_text(text)
        decoded = decode_text(encoded, tree)
        self.assertEqual(decoded, text)


class TestEfficiency(unittest.TestCase):
    """Tests for encoding efficiency."""
    
    def test_efficiency_near_entropy(self):
        """Test that encoding efficiency is near entropy."""
        text = "aaabbbcccddd"
        analysis = analyze_compression_potential(text)
        
        # Efficiency should be reasonably high
        self.assertGreater(analysis['efficiency'], 50)
    
    def test_optimality_for_known_distribution(self):
        """Test optimality for known distribution."""
        # For known distributions, Huffman is optimal
        # With 3 symbols, most frequent should have shortest code
        text = "aaaaabbc"
        tree = build_huffman_tree(build_frequency_table(text))
        
        # a should have shorter code than c (least frequent)
        self.assertLessEqual(len(tree.code_table['a']), len(tree.code_table['c']))


if __name__ == "__main__":
    unittest.main(verbosity=2)