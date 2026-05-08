"""
Usage Examples for Suffix Automaton Utils.

This file demonstrates various use cases of the suffix automaton
implementation.
"""

from mod import (
    SuffixAutomaton,
    build_suffix_automaton,
    count_occurrences,
    find_all_occurrences,
    longest_common_substring,
    count_different_substrings,
    longest_repeating_substring,
    kth_different_substring,
    shortest_unique_substring,
    MultiSuffixAutomaton,
)


def example_basic_usage():
    """Basic usage of suffix automaton."""
    print("\n=== Basic Usage ===")
    
    # Create automaton for a text
    sa = SuffixAutomaton("abacaba")
    
    print(f"Text: abacaba")
    print(f"Number of states: {sa.size}")
    print(f"Different substrings: {sa.count_different_substrings()}")
    
    # Check if substring exists
    print(f"Contains 'aba': {sa.contains('aba')}")
    print(f"Contains 'xyz': {sa.contains('xyz')}")
    
    # Count occurrences
    print(f"'aba' occurrences: {sa.count_occurrences('aba')}")
    print(f"'a' occurrences: {sa.count_occurrences('a')}")


def example_find_occurrences():
    """Finding all occurrence positions."""
    print("\n=== Finding Occurrences ===")
    
    text = "The quick brown fox jumps over the lazy dog. The fox is quick."
    sa = SuffixAutomaton(text)
    
    pattern = "The"
    positions = sa.find_all_occurrences(pattern)
    print(f"Pattern '{pattern}' found at positions: {positions}")
    
    pattern = "fox"
    positions = sa.find_all_occurrences(pattern)
    print(f"Pattern '{pattern}' found at positions: {positions}")
    
    pattern = "quick"
    positions = sa.find_all_occurrences(pattern)
    print(f"Pattern '{pattern}' found at positions: {positions}")


def example_count_different_substrings():
    """Counting unique substrings."""
    print("\n=== Counting Different Substrings ===")
    
    texts = [
        ("aaa", "all 'a's"),
        ("abc", "all unique chars"),
        ("abacaba", "mixed pattern"),
        ("abcd", "sequential"),
    ]
    
    for text, desc in texts:
        sa = SuffixAutomaton(text)
        count = sa.count_different_substrings()
        # n(n+1)/2 is max for all unique characters
        max_count = len(text) * (len(text) + 1) // 2
        print(f"'{text}' ({desc}): {count} unique substrings (max: {max_count})")


def example_longest_common_substring():
    """Finding longest common substring."""
    print("\n=== Longest Common Substring ===")
    
    pairs = [
        ("programming", "programmer"),
        ("abcdefgh", "cdefghij"),
        ("The quick brown fox", "A quick brown dog"),
        ("apple", "orange"),
    ]
    
    for text1, text2 in pairs:
        sa = SuffixAutomaton(text1)
        lcs, length = sa.longest_common_substring(text2)
        print(f"'{text1}' vs '{text2}'")
        print(f"  LCS: '{lcs}' (length {length})")


def example_longest_repeating_substring():
    """Finding longest repeating substring."""
    print("\n=== Longest Repeating Substring ===")
    
    texts = [
        "abcabcabc",
        "aaaa",
        "abababab",
        "abcdef",
        "mississippi",
    ]
    
    for text in texts:
        sa = SuffixAutomaton(text)
        result, length = sa.longest_repeating_substring()
        print(f"'{text}': longest repeating = '{result}' (length {length})")
        
        # Also check with minimum occurrences
        if length > 0:
            result2, length2 = sa.longest_repeating_substring(min_occurrences=3)
            print(f"  With >=3 occurrences: '{result2}' (length {length2})")


def example_kth_substring():
    """Finding k-th lexicographically smallest substring."""
    print("\n=== K-th Lexicographically Smallest Substring ===")
    
    text = "cab"
    sa = SuffixAutomaton(text)
    
    print(f"Text: '{text}'")
    print(f"Total different substrings: {sa.count_different_substrings()}")
    
    # List all substrings in lexicographic order
    for k in range(1, sa.count_different_substrings() + 1):
        substring = sa.kth_different_substring(k)
        print(f"  {k}-th: '{substring}'")


def example_shortest_unique_substring():
    """Finding shortest unique substring at each position."""
    print("\n=== Shortest Unique Substring ===")
    
    text = "aababc"
    sa = SuffixAutomaton(text)
    
    print(f"Text: '{text}'")
    
    for i in range(len(text)):
        result = sa.shortest_unique_substring(i)
        print(f"  Position {i} ('{text[i]}'): shortest unique = '{result}'")


def example_convenience_functions():
    """Using convenience functions."""
    print("\n=== Convenience Functions ===")
    
    # One-shot operations without creating full automaton
    text = "abracadabra"
    
    print(f"Text: '{text}'")
    
    # Count occurrences directly
    count = count_occurrences(text, "abra")
    print(f"'abra' count: {count}")
    
    # Find all positions
    positions = find_all_occurrences(text, "ra")
    print(f"'ra' positions: {positions}")
    
    # LCS with another string
    lcs = longest_common_substring(text, "dabraca")
    print(f"LCS with 'dabraca': '{lcs}'")
    
    # Count different substrings
    diff = count_different_substrings(text)
    print(f"Different substrings: {diff}")
    
    # Longest repeating substring
    repeat = longest_repeating_substring(text)
    print(f"Longest repeating: '{repeat}'")


def example_multi_suffix_automaton():
    """Working with multiple strings."""
    print("\n=== Multi-String Suffix Automaton ===")
    
    msa = MultiSuffixAutomaton()
    
    # Add multiple texts
    texts = [
        "The quick brown fox jumps",
        "A lazy brown dog sleeps",
        "The fox and dog are friends",
    ]
    
    for text in texts:
        msa.add_text(text)
        print(f"Added: '{text}'")
    
    # Find pattern in which texts
    patterns = ["The", "fox", "brown", "dog", "lazy"]
    print("\nPattern distribution:")
    
    for pattern in patterns:
        indices = msa.pattern_in_texts(pattern)
        print(f"  '{pattern}' found in texts: {indices}")


def example_complex_analysis():
    """Complex text analysis."""
    print("\n=== Complex Text Analysis ===")
    
    # Analyze DNA-like sequence
    dna = "ATCGATCGATCGTTACGATCG"
    sa = SuffixAutomaton(dna)
    
    print(f"DNA sequence: '{dna}'")
    
    # Find common subsequences
    other_seq = "ATCGTTAC"
    lcs, length = sa.longest_common_substring(other_seq)
    print(f"LCS with '{other_seq}': '{lcs}'")
    
    # Find repeating patterns
    for min_occ in [2, 3, 4]:
        result, length = sa.longest_repeating_substring(min_occ)
        print(f"Repeating (>= {min_occ} times): '{result}' (length {length})")
    
    # Count unique patterns
    print(f"Total unique substrings: {sa.count_different_substrings()}")
    
    # Get automaton stats
    info = sa.get_info()
    print(f"Automaton stats:")
    print(f"  States: {info['num_states']}")
    print(f"  Transitions: {info['num_transitions']}")


def example_substring_by_length():
    """Get all substrings of specific length."""
    print("\n=== Substrings by Length ===")
    
    text = "abcd"
    sa = SuffixAutomaton(text)
    
    print(f"Text: '{text}'")
    
    for length in range(1, len(text) + 1):
        substrings = sa.all_substrings_of_length(length)
        print(f"  Length {length}: {sorted(substrings)}")


def example_pattern_search():
    """Efficient pattern search for multiple patterns."""
    print("\n=== Efficient Multi-Pattern Search ===")
    
    # Build automaton once
    text = "Lorem ipsum dolor sit amet, consectetur adipiscing elit. " * 10
    sa = SuffixAutomaton(text)
    
    print(f"Text length: {len(text)} characters")
    
    # Search many patterns efficiently
    patterns = [
        "Lorem",
        "ipsum",
        "dolor",
        "sit",
        "amet",
        "consectetur",
        "adipiscing",
        "elit",
        "xyz",  # Not found
    ]
    
    print("\nPattern search results:")
    for pattern in patterns:
        count = sa.count_occurrences(pattern)
        positions = sa.find_all_occurrences(pattern)[:3]  # First 3
        print(f"  '{pattern}': {count} occurrences at {positions}{'...' if len(sa.find_all_occurrences(pattern)) > 3 else ''}")


def example_state_traversal():
    """Traversing automaton states."""
    print("\n=== State Traversal ===")
    
    text = "abc"
    sa = SuffixAutomaton(text)
    
    print(f"Text: '{text}'")
    print(f"Number of states: {sa.size}")
    
    # Traverse to a specific pattern
    patterns = ["a", "ab", "abc", "b", "bc", "c"]
    
    for pattern in patterns:
        state = sa.traverse(pattern)
        if state is not None:
            info = sa.get_state_info(state)
            print(f"  Pattern '{pattern}': state {state}, length={info['length']}, count={info['count']}")
        else:
            print(f"  Pattern '{pattern}': not found")


def run_all_examples():
    """Run all examples."""
    example_basic_usage()
    example_find_occurrences()
    example_count_different_substrings()
    example_longest_common_substring()
    example_longest_repeating_substring()
    example_kth_substring()
    example_shortest_unique_substring()
    example_convenience_functions()
    example_multi_suffix_automaton()
    example_complex_analysis()
    example_substring_by_length()
    example_pattern_search()
    example_state_traversal()


if __name__ == "__main__":
    print("=" * 60)
    print("Suffix Automaton Utils - Usage Examples")
    print("=" * 60)
    
    run_all_examples()
    
    print("\n" + "=" * 60)
    print("All examples completed!")
    print("=" * 60)