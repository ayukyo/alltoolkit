#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AllToolkit - Huffman Coding Utilities Usage Examples

Demonstrates practical usage of Huffman coding functions.

Author: AllToolkit Contributors
License: MIT
"""

import sys
sys.path.insert(0, '..')

from mod import (
    build_frequency_table, build_huffman_tree,
    encode_text, decode_text,
    encode_bytes, decode_bytes,
    generate_canonical_codes,
    calculate_compression_ratio, calculate_compression_percentage,
    get_code_statistics,
    bits_to_bytes, bytes_to_bits,
    serialize_tree, deserialize_tree,
    visualize_tree, print_code_table,
    huffman_encode, huffman_decode,
    analyze_compression_potential,
    compare_with_fixed_length
)


def example_basic_text_encoding():
    """Example: Basic text encoding and decoding."""
    print("\n" + "=" * 60)
    print("Example 1: Basic Text Encoding")
    print("=" * 60)
    
    text = "hello world"
    print(f"Original text: '{text}'")
    print(f"Original size: {len(text.encode('utf-8'))} bytes")
    
    # Encode
    encoded_bits, tree = encode_text(text)
    print(f"Encoded bits: {encoded_bits[:50]}..." if len(encoded_bits) > 50 else f"Encoded bits: {encoded_bits}")
    print(f"Encoded length: {len(encoded_bits)} bits ({len(encoded_bits) / 8:.2f} bytes)")
    
    # Decode
    decoded = decode_text(encoded_bits, tree)
    print(f"Decoded text: '{decoded}'")
    print(f"Match: {decoded == text}")


def example_byte_encoding():
    """Example: Encoding binary data."""
    print("\n" + "=" * 60)
    print("Example 2: Binary Data Encoding")
    print("=" * 60)
    
    data = b"\x00\x01\x02\x00\x00\x00\xFF\xFF\xFE\x00\x01"
    print(f"Original data: {data.hex()}")
    print(f"Original size: {len(data)} bytes")
    
    # Encode
    encoded, tree, padding = encode_bytes(data)
    print(f"Encoded size: {len(encoded)} bytes")
    print(f"Padding bits: {padding}")
    
    # Decode
    decoded = decode_bytes(encoded, tree, padding)
    print(f"Decoded data: {decoded.hex()}")
    print(f"Match: {decoded == data}")


def example_frequency_analysis():
    """Example: Frequency analysis and tree building."""
    print("\n" + "=" * 60)
    print("Example 3: Frequency Analysis")
    print("=" * 60)
    
    text = "this is an example for huffman encoding"
    freq = build_frequency_table(text)
    
    print("Character frequencies:")
    for char, count in sorted(freq.items(), key=lambda x: -x[1]):
        print(f"  '{char}': {count}")
    
    tree = build_huffman_tree(freq)
    print("\nHuffman codes:")
    print_code_table(tree, sort_by='length')


def example_tree_visualization():
    """Example: Visualizing the Huffman tree."""
    print("\n" + "=" * 60)
    print("Example 4: Tree Visualization")
    print("=" * 60)
    
    text = "aaabbc"
    freq = build_frequency_table(text)
    tree = build_huffman_tree(freq)
    
    print(f"Text: '{text}'")
    print("\nHuffman Tree:")
    print(visualize_tree(tree))


def example_compression_analysis():
    """Example: Analyzing compression potential."""
    print("\n" + "=" * 60)
    print("Example 5: Compression Analysis")
    print("=" * 60)
    
    texts = [
        ("Repeated", "aaaaaaaaaa"),
        ("Uniform", "abcdefghij"),
        ("English", "the quick brown fox jumps over the lazy dog"),
        ("Binary", "010101010101010101010101010101"),
    ]
    
    for name, text in texts:
        analysis = analyze_compression_potential(text)
        print(f"\n{name}: '{text[:30]}{'...' if len(text) > 30 else ''}'")
        print(f"  Original: {analysis['original_size']} bytes")
        print(f"  Compressed: {analysis['compressed_size']} bytes")
        print(f"  Ratio: {analysis['compression_ratio']:.2f}x")
        print(f"  Savings: {analysis['compression_percentage']:.1f}%")
        print(f"  Entropy: {analysis['entropy_bits']:.3f} bits/symbol")
        print(f"  Avg code length: {analysis['average_code_length']:.3f} bits")
        print(f"  Efficiency: {analysis['efficiency']:.1f}%")


def example_one_shot_encoding():
    """Example: One-shot encoding and decoding."""
    print("\n" + "=" * 60)
    print("Example 6: One-Shot Encoding/Decoding")
    print("=" * 60)
    
    text = "Hello, Huffman coding!"
    print(f"Original: '{text}'")
    
    # One-shot encode
    encoded, tree_data, padding = huffman_encode(text)
    print(f"Encoded: {len(encoded)} bytes (padding: {padding} bits)")
    
    # One-shot decode
    decoded = huffman_decode(encoded, tree_data, padding)
    print(f"Decoded: '{decoded}'")
    print(f"Match: {decoded == text}")


def example_canonical_codes():
    """Example: Generating canonical Huffman codes."""
    print("\n" + "=" * 60)
    print("Example 7: Canonical Huffman Codes")
    print("=" * 60)
    
    # Code lengths from tree analysis
    code_lengths = {'a': 1, 'b': 2, 'c': 2, 'd': 3, 'e': 3, 'f': 3}
    
    print("Input code lengths:")
    for symbol, length in sorted(code_lengths.items()):
        print(f"  {symbol}: {length}")
    
    canonical = generate_canonical_codes(code_lengths)
    
    print("\nCanonical codes:")
    for symbol, code in sorted(canonical.items()):
        print(f"  {symbol}: {code}")


def example_bits_bytes_conversion():
    """Example: Converting between bits and bytes."""
    print("\n" + "=" * 60)
    print("Example 8: Bits/Bytes Conversion")
    print("=" * 60)
    
    bits_strings = ["0", "01", "011", "0110", "01101", "01101001"]
    
    for bits in bits_strings:
        data, padding = bits_to_bytes(bits)
        recovered = bytes_to_bits(data, padding)
        print(f"Bits: '{bits}' -> Bytes: {data.hex()}, Padding: {padding} -> Recovered: '{recovered}'")
        assert bits == recovered, "Roundtrip failed!"


def example_tree_serialization():
    """Example: Serializing and deserializing tree."""
    print("\n" + "=" * 60)
    print("Example 9: Tree Serialization")
    print("=" * 60)
    
    text = "serialization example"
    freq = build_frequency_table(text)
    tree = build_huffman_tree(freq)
    
    print(f"Original text: '{text}'")
    print(f"Code table size: {len(tree.code_table)} symbols")
    
    # Serialize
    tree_data = serialize_tree(tree)
    print(f"Serialized tree keys: {list(tree_data.keys())}")
    
    # Deserialize
    restored = deserialize_tree(tree_data)
    
    # Verify codes match
    match = tree.code_table == restored.code_table
    print(f"Codes match after restoration: {match}")


def example_comparison_with_fixed_length():
    """Example: Comparing with fixed-length encoding."""
    print("\n" + "=" * 60)
    print("Example 10: Comparison with Fixed-Length Encoding")
    print("=" * 60)
    
    text = "aaabbbcccd"
    freq = build_frequency_table(text)
    tree = build_huffman_tree(freq)
    
    comparison = compare_with_fixed_length(tree, len(text))
    
    print(f"Text: '{text}'")
    print(f"Unique symbols: {len(freq)}")
    print(f"Huffman bits/symbol: {comparison['huffman_bits_per_symbol']}")
    print(f"Fixed-length bits/symbol: {comparison['fixed_bits_per_symbol']}")
    print(f"Savings: {comparison['savings_percent']:.1f}%")
    print(f"Total Huffman bits: {comparison['total_huffman_bits']:.0f}")
    print(f"Total fixed bits: {comparison['total_fixed_bits']}")


def example_file_compression_simulation():
    """Example: Simulating file compression."""
    print("\n" + "=" * 60)
    print("Example 11: File Compression Simulation")
    print("=" * 60)
    
    # Simulate different file types
    file_types = {
        "Text file": "The quick brown fox jumps over the lazy dog. " * 20,
        "Repetitive": "AAAAAAAAAAAAAAAAAAAA" * 50,
        "Random-like": "aBcDeFgHiJkLmNoPqRsTuVwXyZ0123456789" * 10,
        "Code": "def function():\n    return value\n" * 20,
    }
    
    print(f"{'Type':<15} | {'Original':<10} | {'Compressed':<10} | {'Ratio':<8} | {'Savings'}")
    print("-" * 60)
    
    for file_type, content in file_types.items():
        analysis = analyze_compression_potential(content)
        print(f"{file_type:<15} | {analysis['original_size']:<10} | "
              f"{analysis['compressed_size']:<10} | "
              f"{analysis['compression_ratio']:<8.2f} | "
              f"{analysis['compression_percentage']:.1f}%")


def example_statistics():
    """Example: Getting code statistics."""
    print("\n" + "=" * 60)
    print("Example 12: Code Statistics")
    print("=" * 60)
    
    texts = [
        "aaaaa",  # Single dominant symbol
        "aaabbb",  # Two symbols
        "abcdefgh",  # Uniform distribution
        "aaabbc",  # Skewed distribution
    ]
    
    for text in texts:
        tree = build_huffman_tree(build_frequency_table(text))
        stats = get_code_statistics(tree)
        
        print(f"\nText: '{text}'")
        print(f"  Symbols: {stats['num_symbols']}")
        print(f"  Min code length: {stats['min_code_length']}")
        print(f"  Max code length: {stats['max_code_length']}")
        print(f"  Average code length: {stats['average_code_length']:.3f}")
        print(f"  Total bits: {stats['total_bits']}")


def example_practical_usage():
    """Example: Practical usage scenario."""
    print("\n" + "=" * 60)
    print("Example 13: Practical Usage - Message Compression")
    print("=" * 60)
    
    messages = [
        "Hello, World!",
        "This is a longer message that should compress better due to repetition.",
        "Error: File not found at /path/to/file.txt",
    ]
    
    for message in messages:
        print(f"\nMessage: '{message[:40]}{'...' if len(message) > 40 else ''}'")
        
        # Encode
        encoded, tree_data, padding = huffman_encode(message)
        original_size = len(message.encode('utf-8'))
        compressed_size = len(encoded)
        
        print(f"  Original size: {original_size} bytes")
        print(f"  Compressed size: {compressed_size} bytes")
        print(f"  Compression: {calculate_compression_percentage(original_size, compressed_size):.1f}% saved")
        
        # Decode and verify
        decoded = huffman_decode(encoded, tree_data, padding)
        print(f"  Verification: {'✓ Match' if decoded == message else '✗ Mismatch'}")


def main():
    """Run all examples."""
    print("=" * 60)
    print("Huffman Coding Utilities - Usage Examples")
    print("=" * 60)
    
    example_basic_text_encoding()
    example_byte_encoding()
    example_frequency_analysis()
    example_tree_visualization()
    example_compression_analysis()
    example_one_shot_encoding()
    example_canonical_codes()
    example_bits_bytes_conversion()
    example_tree_serialization()
    example_comparison_with_fixed_length()
    example_file_compression_simulation()
    example_statistics()
    example_practical_usage()
    
    print("\n" + "=" * 60)
    print("All examples completed successfully!")
    print("=" * 60)


if __name__ == "__main__":
    main()