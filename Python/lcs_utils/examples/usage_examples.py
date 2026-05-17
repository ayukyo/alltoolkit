"""
LCS Utilities - Usage Examples

This file demonstrates various use cases for the LCS (Longest Common Subsequence) utilities.

Run with: python usage_examples.py
"""

import sys
sys.path.insert(0, '..')

from mod import (
    lcs_length,
    lcs,
    lcs_all,
    lcs_diff,
    lcs_diff_unified,
    lcs_similarity,
    lcs_distance,
    lcs_of_multiple,
    shortest_common_supersequence,
    find_lcs_positions,
    is_subsequence,
    count_distinct_lcs,
    LCSEngine,
    text_similarity,
    line_similarity,
    word_similarity,
    line_diff,
)


def separator(title: str) -> None:
    """Print a section separator."""
    print(f"\n{'='*60}")
    print(f"  {title}")
    print('='*60)


def example_basic_lcs():
    """Basic LCS computation examples."""
    separator("Basic LCS Computation")
    
    s1 = "ABCBDAB"
    s2 = "BDCABA"
    
    print(f"Sequence 1: {s1}")
    print(f"Sequence 2: {s2}")
    print(f"\nLCS: {''.join(lcs(s1, s2))}")
    print(f"LCS Length: {lcs_length(s1, s2)}")
    
    # With lists
    print("\n--- With Lists ---")
    list1 = [1, 2, 3, 2, 4, 5]
    list2 = [2, 3, 4, 6, 5]
    print(f"List 1: {list1}")
    print(f"List 2: {list2}")
    print(f"LCS: {lcs(list1, list2)}")


def example_similarity():
    """Similarity measurement examples."""
    separator("Similarity Measurement")
    
    pairs = [
        ("kitten", "sitting"),
        ("algorithm", "altruistic"),
        ("python", "java"),
        ("hello", "hello"),
        ("abc", "xyz"),
    ]
    
    print(f"{'String 1':<15} {'String 2':<15} {'Similarity':<12} {'Distance':<10}")
    print("-" * 55)
    
    for s1, s2 in pairs:
        sim = lcs_similarity(s1, s2)
        dist = lcs_distance(s1, s2)
        print(f"{s1:<15} {s2:<15} {sim:<12.2%} {dist:<10}")


def example_diff():
    """Diff generation examples."""
    separator("Diff Generation")
    
    # Simple diff
    s1 = "ABCDEF"
    s2 = "ABXDEY"
    
    print(f"Original: {s1}")
    print(f"Modified: {s2}")
    print("\nDiff operations:")
    
    for op, char in lcs_diff(s1, s2):
        if op == 'equal':
            print(f"  = {char}")
        elif op == 'delete':
            print(f"  - {char}")
        elif op == 'insert':
            print(f"  + {char}")
    
    # Unified diff
    print("\n--- Unified Diff ---")
    text1 = "Line 1\nLine 2\nLine 3\nLine 4"
    text2 = "Line 1\nLine 2 Modified\nLine 3\nLine 5"
    
    print(line_diff(text1, text2, "original.txt", "modified.txt"))


def example_all_lcs():
    """Multiple LCS solutions."""
    separator("All LCS Solutions")
    
    s1 = "ABC"
    s2 = "ACB"
    
    print(f"Sequence 1: {s1}")
    print(f"Sequence 2: {s2}")
    print(f"\nAll distinct LCS (length {lcs_length(s1, s2)}):")
    
    for i, solution in enumerate(lcs_all(s1, s2), 1):
        print(f"  Solution {i}: {''.join(solution)}")
    
    print(f"\nTotal distinct LCS: {count_distinct_lcs(s1, s2)}")


def example_multiple_sequences():
    """LCS of multiple sequences."""
    separator("LCS of Multiple Sequences")
    
    sequences = ["ABC", "ADC", "AEC", "AFC"]
    print(f"Sequences: {sequences}")
    print(f"Common subsequence: {lcs_of_multiple(sequences)}")
    
    # More complex example
    sequences = [
        "The quick brown fox",
        "The quick black cat",
        "The quick white dog"
    ]
    print(f"\nSequences:")
    for s in sequences:
        print(f"  - {s}")
    
    # Word-level LCS
    words_seqs = [s.split() for s in sequences]
    common = lcs_of_multiple(words_seqs)
    print(f"Common words: {' '.join(common)}")


def example_supersequence():
    """Shortest Common Supersequence."""
    separator("Shortest Common Supersequence")
    
    s1 = "ABC"
    s2 = "ACD"
    
    print(f"Sequence 1: {s1}")
    print(f"Sequence 2: {s2}")
    
    scs = shortest_common_supersequence(s1, s2)
    print(f"SCS: {''.join(scs)}")
    
    # Verify
    print(f"\nVerification:")
    print(f"  '{s1}' is subsequence: {is_subsequence(s1, scs)}")
    print(f"  '{s2}' is subsequence: {is_subsequence(s2, scs)}")


def example_positions():
    """Finding LCS positions."""
    separator("LCS Position Mapping")
    
    s1 = "PROGRAMMING"
    s2 = "PRANKING"
    
    print(f"Sequence 1: {s1}")
    print(f"Sequence 2: {s2}")
    
    positions = find_lcs_positions(s1, s2)
    lcs_result = lcs(s1, s2)
    
    print(f"\nLCS: {''.join(lcs_result)}")
    print(f"Positions in each sequence:")
    
    for i, (pos1, pos2) in enumerate(positions):
        print(f"  {lcs_result[i]}: pos {pos1} in '{s1}', pos {pos2} in '{s2}'")


def example_subsequence():
    """Subsequence checking."""
    separator("Subsequence Checking")
    
    tests = [
        ("ABC", "AXBYCZ", True),
        ("AC", "ABC", True),
        ("ABC", "ACB", False),
        ("", "ABC", True),
        ("ABC", "", False),
    ]
    
    for sub, seq, expected in tests:
        result = is_subsequence(sub, seq)
        status = "✓" if result == expected else "✗"
        print(f"  '{sub}' ⊂ '{seq}': {result} {status}")


def example_text_comparison():
    """Text comparison utilities."""
    separator("Text Comparison")
    
    text1 = """
    The quick brown fox jumps over the lazy dog.
    This is a sample text for testing.
    Lorem ipsum dolor sit amet.
    """
    
    text2 = """
    The quick brown fox jumped over the lazy cat.
    This is another sample for testing.
    Lorem ipsum dolor sit amet.
    """
    
    print("Text 1 vs Text 2:")
    print(f"  Character similarity: {text_similarity(text1, text2):.2%}")
    print(f"  Line similarity: {line_similarity(text1, text2):.2%}")
    print(f"  Word similarity: {word_similarity(text1, text2):.2%}")


def example_engine():
    """Using the LCS Engine class."""
    separator("LCS Engine (Cached)")
    
    engine = LCSEngine(cache_size=128)
    
    # Multiple comparisons with caching
    strings = ["algorithm", "altruistic", "arithmetic", "algebraic"]
    
    print("Similarity matrix:")
    print(f"{'':<12}", end="")
    for s in strings:
        print(f"{s[:8]:<10}", end="")
    print()
    
    for s1 in strings:
        print(f"{s1[:10]:<12}", end="")
        for s2 in strings:
            sim = engine.similarity(s1, s2)
            print(f"{sim:<10.2f}", end="")
        print()


def example_dna_sequence():
    """DNA sequence analysis example."""
    separator("DNA Sequence Analysis")
    
    dna1 = "ACGTACGTACGT"
    dna2 = "ACGTTTACGTAC"
    
    print(f"DNA 1: {dna1}")
    print(f"DNA 2: {dna2}")
    print(f"\nLCS: {''.join(lcs(dna1, dna2))}")
    print(f"Similarity: {lcs_similarity(dna1, dna2):.2%}")
    print(f"Edit distance: {lcs_distance(dna1, dna2)}")
    
    # Find mutation points
    diff = lcs_diff(dna1, dna2)
    mutations = [(op, char, i) for i, (op, char) in enumerate(diff) if op != 'equal']
    print(f"\nMutations detected: {len(mutations)}")


def example_version_comparison():
    """Version string comparison using LCS."""
    separator("Version String Analysis")
    
    v1 = "1.2.3-alpha.4"
    v2 = "1.3.0-beta.2"
    
    print(f"Version 1: {v1}")
    print(f"Version 2: {v2}")
    print(f"Character similarity: {lcs_similarity(v1, v2):.2%}")
    
    # Component comparison
    parts1 = v1.replace('-', '.').split('.')
    parts2 = v2.replace('-', '.').split('.')
    
    print(f"\nVersion 1 parts: {parts1}")
    print(f"Version 2 parts: {parts2}")
    print(f"Common parts: {lcs(parts1, parts2)}")


def example_code_review():
    """Code review helper using LCS diff."""
    separator("Code Review Helper")
    
    old_code = """def process(data):
    result = []
    for item in data:
        if item.valid:
            result.append(item)
    return result"""
    
    new_code = """def process(data):
    result = []
    for item in data:
        if item.is_valid():
            result.append(item.transform())
    return sorted(result)"""
    
    print("Old Code:")
    print(old_code)
    print("\nNew Code:")
    print(new_code)
    print("\nDifferences:")
    print(line_diff(old_code, new_code, "old.py", "new.py"))


def main():
    """Run all examples."""
    example_basic_lcs()
    example_similarity()
    example_diff()
    example_all_lcs()
    example_multiple_sequences()
    example_supersequence()
    example_positions()
    example_subsequence()
    example_text_comparison()
    example_engine()
    example_dna_sequence()
    example_version_comparison()
    example_code_review()
    
    separator("All Examples Completed!")


if __name__ == "__main__":
    main()