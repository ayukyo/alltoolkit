"""
BWT (Burrows-Wheeler Transform) Utilities - Usage Examples

This module demonstrates practical uses of BWT for:
1. Data compression preprocessing
2. Text pattern matching
3. Genome sequence analysis
4. Compression analysis
"""

import sys
import os
# Python 3.6 compatible path handling
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from bwt_utils.mod import (
    bwt_transform, bwt_inverse,
    mtf_encode, mtf_decode,
    bwt_mtf_compress, bwt_mtf_decompress,
    bwt_search, bwt_compress_ratio,
    BWT
)


def example_1_basic_transform():
    """Example 1: Basic BWT forward and inverse transform."""
    print("=" * 50)
    print("Example 1: Basic BWT Transform")
    print("=" * 50)
    
    original = "banana"
    print(f"Original: {original}")
    
    # Forward transform
    transformed, index = bwt_transform(original)
    print(f"Transformed: {transformed}")
    print(f"Index: {index}")
    
    # Inverse transform
    recovered = bwt_inverse(transformed, index)
    print(f"Recovered: {recovered}")
    print(f"Match: {original == recovered}")
    print()


def example_2_compression_pipeline():
    """Example 2: BWT + MTF compression pipeline."""
    print("=" * 50)
    print("Example 2: BWT + MTF Compression Pipeline")
    print("=" * 50)
    
    texts = [
        "banana",
        "mississippi",
        "abcabcabcabcabc",
        "the quick brown fox jumps over the lazy dog",
    ]
    
    for text in texts:
        print(f"\nOriginal: '{text}'")
        
        # Step 1: BWT
        transformed, idx = bwt_transform(text)
        print(f"After BWT: '{transformed}'")
        
        # Step 2: MTF encoding
        codes = mtf_encode(transformed)
        print(f"MTF codes: {codes[:20]}..." if len(codes) > 20 else f"MTF codes: {codes}")
        
        # Count small codes (good for compression)
        small_codes = sum(1 for c in codes if c < 4)
        ratio = small_codes / len(codes) * 100
        print(f"Small codes (0-3): {small_codes}/{len(codes)} ({ratio:.1f}%)")
    print()


def example_3_full_compress_cycle():
    """Example 3: Complete compression/decompression cycle."""
    print("=" * 50)
    print("Example 3: Complete Compress/Decompress Cycle")
    print("=" * 50)
    
    original = "abracadabra" * 5
    print(f"Original ({len(original)} chars): '{original[:40]}...'")
    
    # Compress
    codes, index, alphabet = bwt_mtf_compress(original)
    print(f"Compressed to {len(codes)} codes")
    print(f"Alphabet ({len(alphabet)} chars): {alphabet}")
    print(f"Index: {index}")
    
    # Decompress
    recovered = bwt_mtf_decompress(codes, index, alphabet)
    print(f"Recovered: '{recovered[:40]}...'")
    print(f"Match: {original == recovered}")
    
    # The codes would be further compressed with Huffman/Arithmetic coding
    # in a real compressor like bzip2
    print()


def example_4_pattern_search():
    """Example 4: BWT-based pattern search (FM-index style)."""
    print("=" * 50)
    print("Example 4: BWT-Based Pattern Search")
    print("=" * 50)
    
    text = "banana"
    patterns = ["ana", "ban", "na", "xyz"]
    
    print(f"Text: '{text}'")
    print()
    
    for pattern in patterns:
        positions = bwt_search(text, pattern)
        if positions:
            print(f"Pattern '{pattern}' found at positions: {positions}")
        else:
            print(f"Pattern '{pattern}' not found")
    print()


def example_5_compression_analysis():
    """Example 5: Analyzing compression potential."""
    print("=" * 50)
    print("Example 5: Compression Potential Analysis")
    print("=" * 50)
    
    texts = [
        ("Repetitive", "a" * 50),
        ("Natural English", "the quick brown fox jumps over the lazy dog"),
        ("Repeating pattern", "abc" * 20),
        ("Random-ish", "abcdefghijklmnopqrstuvwxyz"),
    ]
    
    for name, text in texts:
        analysis = bwt_compress_ratio(text)
        print(f"\n{name}:")
        print(f"  Length: {analysis['original_length']}")
        print(f"  Alphabet size: {analysis['alphabet_size']}")
        print(f"  Small code ratio: {analysis['small_code_ratio']:.2%}")
        print(f"  Potential: {analysis['compression_potential']}")
        print(f"  Code distribution: {analysis['code_distribution']}")
    print()


def example_6_object_oriented():
    """Example 6: Object-oriented interface."""
    print("=" * 50)
    print("Example 6: Object-Oriented Interface")
    print("=" * 50)
    
    data = "mississippi"
    print(f"Data: '{data}'")
    
    # Create BWT object
    bwt = BWT(data)
    
    # Transform
    transformed = bwt.transform()
    print(f"Transformed: '{transformed}'")
    print(f"Index: {bwt.index}")
    
    # Search
    positions = bwt.search("iss")
    print(f"'iss' found at: {positions}")
    
    # Analyze
    analysis = bwt.analyze()
    print(f"Compression potential: {analysis['compression_potential']}")
    
    # Inverse using static method
    recovered = BWT.inverse(transformed, bwt.index)
    print(f"Recovered: '{recovered}'")
    print()


def example_7_bytes_handling():
    """Example 7: Working with binary data."""
    print("=" * 50)
    print("Example 7: Binary Data Handling")
    print("=" * 50)
    
    # Binary data (e.g., from a file)
    data = b"\x00\x01\x02\x01\x00\xff\xfe\xfd" * 10
    print(f"Binary data ({len(data)} bytes): {data[:20]}...")
    
    # Transform
    transformed, idx = bwt_transform(data)
    print(f"Transformed ({len(transformed)} bytes): {transformed[:20]}...")
    
    # Recover
    recovered = bwt_inverse(transformed, idx)
    print(f"Recovered: {recovered[:20]}...")
    print(f"Match: {data == recovered}")
    print()


def example_8_mtf_encoding():
    """Example 8: Understanding MTF encoding."""
    print("=" * 50)
    print("Example 8: Move-to-Front Encoding Deep Dive")
    print("=" * 50)
    
    text = "aaabbbccc"
    print(f"Text: '{text}'")
    
    # Build alphabet from text (in order of first appearance)
    alphabet = ''.join(sorted(set(text)))
    print(f"Alphabet: '{alphabet}'")
    
    # Encode
    codes = mtf_encode(text)
    print(f"Codes: {codes}")
    
    # Explain each step
    print("\nStep-by-step encoding:")
    symbol_list = list(alphabet)
    for i, char in enumerate(text):
        idx = symbol_list.index(char)
        print(f"  '{char}' -> code {idx} (alphabet: {''.join(symbol_list)})")
        symbol_list.pop(idx)
        symbol_list.insert(0, char)
    
    # Decode
    recovered = mtf_decode(codes, alphabet)
    print(f"\nDecoded: '{recovered}'")
    print()


def example_9_real_world_text():
    """Example 9: Real-world text compression simulation."""
    print("=" * 50)
    print("Example 9: Real-World Text Compression")
    print("=" * 50)
    
    # Simulate a typical English text
    text = """
    The Burrows-Wheeler Transform is a reversible transformation
    that rearranges characters to group similar characters together.
    This property makes it extremely effective as a preprocessing
    step for compression algorithms like bzip2.
    """
    text = text.strip()
    
    print(f"Original text ({len(text)} chars):")
    print(f"  '{text[:60]}...'")
    
    # Analyze compression potential
    analysis = bwt_compress_ratio(text)
    print(f"\nCompression analysis:")
    print(f"  Alphabet size: {analysis['alphabet_size']}")
    print(f"  Unique codes: {analysis['unique_codes']}")
    print(f"  Small code ratio: {analysis['small_code_ratio']:.2%}")
    print(f"  Compression potential: {analysis['compression_potential']}")
    
    # Show transformed text
    transformed, idx = bwt_transform(text)
    print(f"\nAfter BWT ({len(transformed)} chars):")
    print(f"  '{transformed[:60]}...'")
    
    # Show code distribution
    print(f"\nCode distribution (top 10): {analysis['code_distribution']}")
    
    # Demonstrate roundtrip
    recovered = bwt_inverse(transformed, idx)
    print(f"\nRoundtrip successful: {text == recovered}")
    print()


def example_10_performance_tips():
    """Example 10: Performance considerations."""
    print("=" * 50)
    print("Example 10: Performance Tips")
    print("=" * 50)
    
    print("""
BWT Performance Characteristics:

1. TIME COMPLEXITY:
   - Transform: O(n² log n) for naive implementation
   - Inverse: O(n) using the first-last property
   - Production systems use O(n) suffix arrays

2. SPACE COMPLEXITY:
   - Both transform and inverse: O(n)
   
3. BEST USE CASES:
   - Text with repeating patterns
   - Genome sequences
   - Natural language text
   - Log files with repetitive entries

4. AVOID FOR:
   - Already compressed data (JPEG, MP3, etc.)
   - Random/encrypted data
   - Very small files (< 1KB)

5. COMPRESSION PIPELINE:
   Input → BWT → MTF → RLE → Huffman/Arithmetic → Output

6. IMPLEMENTATION NOTES:
   - This is a reference implementation
   - For production: consider using suffix arrays
   - For large files: external memory algorithms
""")
    print()


if __name__ == "__main__":
    example_1_basic_transform()
    example_2_compression_pipeline()
    example_3_full_compress_cycle()
    example_4_pattern_search()
    example_5_compression_analysis()
    example_6_object_oriented()
    example_7_bytes_handling()
    example_8_mtf_encoding()
    example_9_real_world_text()
    example_10_performance_tips()
    
    print("=" * 50)
    print("All examples completed!")
    print("=" * 50)