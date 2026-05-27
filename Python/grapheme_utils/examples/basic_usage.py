#!/usr/bin/env python3
"""
Grapheme Utilities - Basic Usage Examples

This example demonstrates the core functionality of grapheme_utils.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mod import (
    grapheme_count, grapheme_split, grapheme_slice, grapheme_reverse,
    grapheme_info, truncate_graphemes, pad_graphemes, grapheme_find,
    grapheme_replace, grapheme_equal, normalize_graphemes
)


def main():
    print("=" * 60)
    print("Grapheme Utilities - Basic Usage Examples")
    print("=" * 60)
    
    # Example 1: Counting graphemes
    print("\n1. Counting Graphemes")
    print("-" * 40)
    text1 = "Hello World"
    text2 = "👨‍👩‍👧‍👦"  # Family emoji
    text3 = "नमस्ते"  # Hindi "namaste"
    text4 = "café"  # With accent
    
    print(f"'{text1}': {len(text1)} code points, {grapheme_count(text1)} graphemes")
    print(f"'{text2}': {len(text2)} code points, {grapheme_count(text2)} grapheme")
    print(f"'{text3}': {len(text3)} code points, {grapheme_count(text3)} graphemes")
    print(f"'{text4}': {len(text4)} code points, {grapheme_count(text4)} graphemes")
    
    # Example 2: Splitting strings
    print("\n2. Splitting Strings")
    print("-" * 40)
    text = "Hello 👋 World"
    clusters = grapheme_split(text)
    print(f"Text: {text}")
    print(f"Split: {clusters}")
    
    # Example 3: Slicing
    print("\n3. Slicing by Grapheme Index")
    print("-" * 40)
    text = "👨‍👩‍👧‍👦Hello World"
    print(f"Text: {text}")
    print(f"Slice [0:1]: '{grapheme_slice(text, 0, 1)}'")
    print(f"Slice [1:6]: '{grapheme_slice(text, 1, 6)}'")
    print(f"Slice [6:]: '{grapheme_slice(text, 6)}'")
    
    # Example 4: Reversing
    print("\n4. Reversing Strings")
    print("-" * 40)
    texts = ["hello", "café", "👋👨‍👩‍👧‍👦", "नमस्ते"]
    for t in texts:
        print(f"'{t}' → '{grapheme_reverse(t)}'")
    
    # Example 5: Getting grapheme info
    print("\n5. Grapheme Information")
    print("-" * 40)
    text = "é👨‍👩‍👧‍👦"
    info = grapheme_info(text)
    for i, item in enumerate(info):
        print(f"Grapheme {i}: '{item['grapheme']}'")
        print(f"  Code points: {item['code_points']}")
        print(f"  Length (code points): {item['length_code_points']}")
        print(f"  Length (bytes UTF-8): {item['length_bytes']}")
        print(f"  Is emoji: {item['is_emoji']}")
        print(f"  Has combining marks: {item['has_combining']}")
        print(f"  Has ZWJ: {item['has_zwj']}")
    
    # Example 6: Truncation
    print("\n6. Truncation")
    print("-" * 40)
    text = "This is a long sentence with emoji 👨‍👩‍👧‍👦 at the end"
    print(f"Original: {text}")
    print(f"Truncated (10): {truncate_graphemes(text, 10)}")
    print(f"Truncated (5): {truncate_graphemes(text, 5)}")
    
    # Example 7: Padding
    print("\n7. Padding")
    print("-" * 40)
    text = "Hi"
    print(f"Original: '{text}'")
    print(f"Pad right (10): '{pad_graphemes(text, 10)}'")
    print(f"Pad left (10): '{pad_graphemes(text, 10, side='left')}'")
    print(f"Pad center (10): '{pad_graphemes(text, 10, side='center')}'")
    
    # Example 8: Finding
    print("\n8. Finding Substrings")
    print("-" * 40)
    text = "Hello 👋 World"
    print(f"Text: {text}")
    print(f"Find 'World': index {grapheme_find(text, 'World')}")
    print(f"Find '👋': index {grapheme_find(text, '👋')}")
    print(f"Find 'xyz': index {grapheme_find(text, 'xyz')}")
    
    # Example 9: Replacement
    print("\n9. Replacement")
    print("-" * 40)
    text = "Hello 👋, goodbye 👋"
    print(f"Original: {text}")
    print(f"Replace 👋 with 👍: {grapheme_replace(text, '👋', '👍')}")
    print(f"Replace 👋 once: {grapheme_replace(text, '👋', '👍', count=1)}")
    
    # Example 10: Normalization and comparison
    print("\n10. Normalization and Comparison")
    print("-" * 40)
    # Two ways to write é
    precomposed = "é"  # Single code point U+00E9
    decomposed = "e\u0301"  # 'e' + combining acute accent U+0301
    
    print(f"Precomposed 'é': {len(precomposed)} code point(s)")
    print(f"Decomposed 'e + ́': {len(decomposed)} code point(s)")
    print(f"Direct equality: {precomposed == decomposed}")
    print(f"Grapheme equality: {grapheme_equal(precomposed, decomposed)}")
    
    # Normalized forms
    print(f"NFC normalized: '{normalize_graphemes(decomposed, 'NFC')}'")
    
    print("\n" + "=" * 60)
    print("Examples complete!")


if __name__ == "__main__":
    main()