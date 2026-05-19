"""
Basic usage examples for Z Algorithm Utilities

Demonstrates pattern matching, substring analysis, and period detection.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from z_algorithm_utils.mod import (
    z_array, find_all_occurrences, count_occurrences,
    longest_prefix_suffix, longest_repeated_substring,
    find_minimal_period, is_rotation, compress_string,
    ZPatternMatcher, visualize_z_array
)


def main():
    print("=" * 60)
    print("Z Algorithm Utilities - Basic Usage Examples")
    print("=" * 60)
    
    # 1. Z-Array Computation
    print("\n1. Z-Array Computation")
    print("-" * 40)
    s = "aabcaabxaaz"
    z = z_array(s)
    print(f"String: {s}")
    print(f"Z-array: {z}")
    print()
    
    # Visualize
    print("Visualization:")
    print(visualize_z_array("aaaa"))
    print()
    
    # 2. Pattern Matching
    print("\n2. Pattern Matching")
    print("-" * 40)
    text = "The quick brown fox jumps over the lazy dog. The fox is quick."
    pattern = "fox"
    
    positions = find_all_occurrences(pattern, text)
    print(f"Searching for '{pattern}' in text:")
    print(f"  Found at positions: {positions}")
    print(f"  Count: {count_occurrences(pattern, text)}")
    print()
    
    # Multiple patterns
    print("Multi-pattern search:")
    matcher = ZPatternMatcher(["quick", "fox", "dog"])
    results = matcher.search(text)
    print(f"  Found {len(results)} matches:")
    for _, pos, p in results:
        print(f"    '{p}' at position {pos}")
    print()
    
    # 3. Substring Analysis
    print("\n3. Substring Analysis")
    print("-" * 40)
    
    # Longest prefix-suffix
    s1 = "abacababacab"
    lps = longest_prefix_suffix(s1)
    print(f"String: {s1}")
    print(f"Longest prefix that is also suffix: {s1[:lps]} (length {lps})")
    print()
    
    # Longest repeated substring
    s2 = "banana"
    substr, positions = longest_repeated_substring(s2)
    print(f"String: {s2}")
    print(f"Longest repeated substring: '{substr}' at positions {positions}")
    print()
    
    # 4. Period Detection
    print("\n4. Period Detection")
    print("-" * 40)
    
    s3 = "abcabcabcabc"
    period = find_minimal_period(s3)
    print(f"String: {s3}")
    print(f"Minimal period: {period.period}")
    print(f"Is periodic: {period.is_periodic}")
    print(f"Repeating unit: '{period.period_string}'")
    print()
    
    # 5. Rotation Check
    print("\n5. Rotation Check")
    print("-" * 40)
    
    s4 = "waterbottle"
    s5 = "erbottlewat"
    print(f"Is '{s5}' a rotation of '{s4}'? {is_rotation(s4, s5)}")
    
    s6 = "erbottlewax"
    print(f"Is '{s6}' a rotation of '{s4}'? {is_rotation(s4, s6)}")
    print()
    
    # 6. Compression
    print("\n6. String Compression")
    print("-" * 40)
    
    s7 = "abcabcabcabcabc"
    pattern, count = compress_string(s7)
    print(f"Original: {s7}")
    print(f"Compressed: pattern='{pattern}', count={count}")
    print(f"Compression ratio: {len(s7)} -> {len(pattern) + len(str(count))}")
    print()
    
    # 7. DNA Sequence Analysis Example
    print("\n7. DNA Sequence Analysis Example")
    print("-" * 40)
    
    dna = "ATCGATCGATCGATCGATCG"
    substr, positions = longest_repeated_substring(dna)
    print(f"DNA sequence: {dna}")
    print(f"Longest repeated sequence: '{substr}'")
    print(f"Appears at: {positions}")
    
    period = find_minimal_period(dna)
    print(f"Sequence period: {period.period} (unit: '{period.period_string}')")
    print()
    
    # 8. Performance Note
    print("\n8. Performance")
    print("-" * 40)
    print("Z-algorithm is O(n) for Z-array computation")
    print("Pattern matching: O(n + m) using sentinel concatenation")
    print("Use iter_occurrences() for memory-efficient large text search")
    print()
    
    print("=" * 60)
    print("All examples completed successfully!")
    print("=" * 60)


if __name__ == "__main__":
    main()