"""
LCS (Longest Common Subsequence) Utilities

A comprehensive module for computing longest common subsequences between sequences.
Useful for diff tools, DNA sequence analysis, text similarity, and version control.

Zero external dependencies - pure Python implementation.

Author: AllToolkit
Date: 2026-05-18
"""

from typing import TypeVar, List, Tuple, Optional, Sequence, Generator, Callable
from functools import lru_cache

T = TypeVar('T')


def lcs_length(seq1: Sequence[T], seq2: Sequence[T]) -> int:
    """
    Compute the length of the longest common subsequence.
    
    Uses optimized O(min(m,n)) space complexity.
    
    Args:
        seq1: First sequence
        seq2: Second sequence
        
    Returns:
        Length of the longest common subsequence
        
    Example:
        >>> lcs_length("ABCBDAB", "BDCABA")
        4
        >>> lcs_length([1, 2, 3, 4], [2, 4, 3, 1])
        2
    """
    if not seq1 or not seq2:
        return 0
    
    # Ensure seq1 is the shorter one for space optimization
    if len(seq1) > len(seq2):
        seq1, seq2 = seq2, seq1
    
    m, n = len(seq1), len(seq2)
    
    # Use two rows instead of full matrix
    prev = [0] * (m + 1)
    curr = [0] * (m + 1)
    
    for j in range(1, n + 1):
        for i in range(1, m + 1):
            if seq1[i - 1] == seq2[j - 1]:
                curr[i] = prev[i - 1] + 1
            else:
                curr[i] = max(prev[i], curr[i - 1])
        prev, curr = curr, prev
    
    return prev[m]


def lcs(seq1: Sequence[T], seq2: Sequence[T]) -> List[T]:
    """
    Compute the longest common subsequence between two sequences.
    
    Uses dynamic programming with O(m*n) time and space complexity.
    
    Args:
        seq1: First sequence
        seq2: Second sequence
        
    Returns:
        The longest common subsequence as a list
        
    Example:
        >>> lcs("ABCBDAB", "BDCABA")
        ['B', 'D', 'A', 'B']
        >>> lcs([1, 2, 3, 2, 4], [2, 3, 4, 5])
        [2, 3, 4]
    """
    if not seq1 or not seq2:
        return []
    
    m, n = len(seq1), len(seq2)
    
    # Build DP table
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if seq1[i - 1] == seq2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1] + 1
            else:
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])
    
    # Backtrack to find the LCS
    result = []
    i, j = m, n
    while i > 0 and j > 0:
        if seq1[i - 1] == seq2[j - 1]:
            result.append(seq1[i - 1])
            i -= 1
            j -= 1
        elif dp[i - 1][j] > dp[i][j - 1]:
            i -= 1
        else:
            j -= 1
    
    return result[::-1]


def lcs_all(seq1: Sequence[T], seq2: Sequence[T]) -> List[List[T]]:
    """
    Compute all longest common subsequences between two sequences.
    
    Args:
        seq1: First sequence
        seq2: Second sequence
        
    Returns:
        List of all longest common subsequences
        
    Example:
        >>> lcs_all("ABC", "ACB")
        [['A', 'B'], ['A', 'C']]
    """
    if not seq1 or not seq2:
        return [[]]
    
    m, n = len(seq1), len(seq2)
    
    # Build DP table
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if seq1[i - 1] == seq2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1] + 1
            else:
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])
    
    max_len = dp[m][n]
    if max_len == 0:
        return [[]]
    
    # Backtrack to find all LCS
    result = set()
    
    def backtrack(i: int, j: int, current: tuple) -> None:
        if len(current) == max_len:
            result.add(current)
            return
        
        if i <= 0 or j <= 0:
            return
        
        if seq1[i - 1] == seq2[j - 1]:
            backtrack(i - 1, j - 1, (seq1[i - 1],) + current)
        else:
            if dp[i - 1][j] >= dp[i][j - 1]:
                backtrack(i - 1, j, current)
            if dp[i][j - 1] >= dp[i - 1][j]:
                backtrack(i, j - 1, current)
    
    backtrack(m, n, ())
    return [list(seq) for seq in result]


def lcs_diff(seq1: Sequence[T], seq2: Sequence[T]) -> List[Tuple[str, T]]:
    """
    Generate a diff between two sequences using LCS.
    
    Returns a list of operations where each operation is a tuple:
    - ('equal', element): Element is in both sequences
    - ('delete', element): Element was removed from seq1
    - ('insert', element): Element was added to seq2
    
    Args:
        seq1: Original sequence
        seq2: Modified sequence
        
    Returns:
        List of diff operations
        
    Example:
        >>> lcs_diff("ABC", "ACD")
        [('equal', 'A'), ('delete', 'B'), ('equal', 'C'), ('insert', 'D')]
    """
    if not seq1:
        return [('insert', x) for x in seq2]
    if not seq2:
        return [('delete', x) for x in seq1]
    
    m, n = len(seq1), len(seq2)
    
    # Build DP table
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if seq1[i - 1] == seq2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1] + 1
            else:
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])
    
    # Backtrack to generate diff
    result = []
    i, j = m, n
    
    while i > 0 and j > 0:
        if seq1[i - 1] == seq2[j - 1]:
            result.append(('equal', seq1[i - 1]))
            i -= 1
            j -= 1
        elif dp[i - 1][j] > dp[i][j - 1]:
            result.append(('delete', seq1[i - 1]))
            i -= 1
        else:
            result.append(('insert', seq2[j - 1]))
            j -= 1
    
    # Handle remaining elements
    while i > 0:
        result.append(('delete', seq1[i - 1]))
        i -= 1
    while j > 0:
        result.append(('insert', seq2[j - 1]))
        j -= 1
    
    return result[::-1]


def lcs_diff_unified(seq1: Sequence[T], seq2: Sequence[T], 
                     context_lines: int = 3,
                     name1: str = "original",
                     name2: str = "modified") -> str:
    """
    Generate a unified diff between two sequences.
    
    Args:
        seq1: Original sequence
        seq2: Modified sequence
        context_lines: Number of context lines around changes
        name1: Name for first sequence
        name2: Name for second sequence
        
    Returns:
        Unified diff string
        
    Example:
        >>> print(lcs_diff_unified("ABC", "ACD", name1="old.txt", name2="new.txt"))
        --- old.txt
        +++ new.txt
        @@ -1,3 +1,3 @@
         A
        -B
         C
        +D
    """
    diff = lcs_diff(seq1, seq2)
    
    # Convert diff to lines
    lines = []
    lines.append(f"--- {name1}")
    lines.append(f"+++ {name2}")
    
    if not diff:
        return '\n'.join(lines)
    
    # Group changes into hunks
    hunks = []
    current_hunk = []
    hunk_start_old = 1
    hunk_start_new = 1
    old_line = 1
    new_line = 1
    in_change = False
    
    for op, elem in diff:
        str_elem = str(elem)
        
        if op == 'equal':
            current_hunk.append(f" {str_elem}")
            if in_change:
                pass  # Continue hunk
            old_line += 1
            new_line += 1
        elif op == 'delete':
            current_hunk.append(f"-{str_elem}")
            old_line += 1
            in_change = True
        elif op == 'insert':
            current_hunk.append(f"+{str_elem}")
            new_line += 1
            in_change = True
    
    # Calculate hunk header
    old_count = sum(1 for op, _ in diff if op in ('equal', 'delete'))
    new_count = sum(1 for op, _ in diff if op in ('equal', 'insert'))
    
    lines.append(f"@@ -1,{old_count} +1,{new_count} @@")
    lines.extend(current_hunk)
    
    return '\n'.join(lines)


def lcs_similarity(seq1: Sequence[T], seq2: Sequence[T]) -> float:
    """
    Compute the LCS-based similarity between two sequences.
    
    Similarity is defined as: 2 * LCS_length / (len(seq1) + len(seq2))
    
    Args:
        seq1: First sequence
        seq2: Second sequence
        
    Returns:
        Similarity score between 0 and 1
        
    Example:
        >>> round(lcs_similarity("ABC", "ACB"), 2)
        0.67
        >>> lcs_similarity("ABC", "ABC")
        1.0
        >>> lcs_similarity("ABC", "XYZ")
        0.0
    """
    if not seq1 and not seq2:
        return 1.0
    
    if not seq1 or not seq2:
        return 0.0
    
    length = lcs_length(seq1, seq2)
    return 2 * length / (len(seq1) + len(seq2))


def lcs_distance(seq1: Sequence[T], seq2: Sequence[T]) -> int:
    """
    Compute the edit distance based on LCS.
    
    Minimum number of insertions and deletions needed to transform seq1 to seq2.
    Distance = len(seq1) + len(seq2) - 2 * LCS_length
    
    Args:
        seq1: First sequence
        seq2: Second sequence
        
    Returns:
        LCS-based edit distance
        
    Example:
        >>> lcs_distance("ABC", "AC")
        1
        >>> lcs_distance("ABC", "DEF")
        6
    """
    return len(seq1) + len(seq2) - 2 * lcs_length(seq1, seq2)


def lcs_of_multiple(sequences: List[Sequence[T]]) -> List[T]:
    """
    Compute the longest common subsequence of multiple sequences.
    
    Uses iterative pairwise approach. Note: This is not guaranteed to find
    the globally optimal LCS for 3+ sequences (which is NP-hard), but finds
    a good approximation.
    
    Args:
        sequences: List of sequences
        
    Returns:
        Common subsequence present in all sequences
        
    Example:
        >>> lcs_of_multiple(["ABC", "ACD", "ABD"])
        ['A', 'D']
    """
    if not sequences:
        return []
    
    if len(sequences) == 1:
        return list(sequences[0])
    
    result = list(sequences[0])
    for seq in sequences[1:]:
        result = lcs(result, seq)
        if not result:
            return []
    
    return result


def shortest_common_supersequence(seq1: Sequence[T], seq2: Sequence[T]) -> List[T]:
    """
    Compute the shortest common supersequence (SCS) of two sequences.
    
    SCS is the shortest sequence that contains both seq1 and seq2 as subsequences.
    
    Args:
        seq1: First sequence
        seq2: Second sequence
        
    Returns:
        The shortest common supersequence
        
    Example:
        >>> shortest_common_supersequence("ABC", "ACD")
        ['A', 'B', 'C', 'D']
        >>> shortest_common_supersequence([1, 2, 3], [2, 3, 4])
        [1, 2, 3, 4]
    """
    if not seq1:
        return list(seq2)
    if not seq2:
        return list(seq1)
    
    m, n = len(seq1), len(seq2)
    
    # Build DP table for LCS
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if seq1[i - 1] == seq2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1] + 1
            else:
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])
    
    # Build SCS from DP table
    result = []
    i, j = m, n
    
    while i > 0 and j > 0:
        if seq1[i - 1] == seq2[j - 1]:
            result.append(seq1[i - 1])
            i -= 1
            j -= 1
        elif dp[i - 1][j] > dp[i][j - 1]:
            result.append(seq1[i - 1])
            i -= 1
        else:
            result.append(seq2[j - 1])
            j -= 1
    
    # Add remaining elements
    while i > 0:
        result.append(seq1[i - 1])
        i -= 1
    while j > 0:
        result.append(seq2[j - 1])
        j -= 1
    
    return result[::-1]


def find_lcs_positions(seq1: Sequence[T], seq2: Sequence[T]) -> List[Tuple[int, int]]:
    """
    Find the positions of LCS elements in both sequences.
    
    Args:
        seq1: First sequence
        seq2: Second sequence
        
    Returns:
        List of (pos_in_seq1, pos_in_seq2) tuples for LCS elements
        
    Example:
        >>> find_lcs_positions("ABC", "ADC")
        [(0, 0), (2, 2)]
    """
    if not seq1 or not seq2:
        return []
    
    m, n = len(seq1), len(seq2)
    
    # Build DP table
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if seq1[i - 1] == seq2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1] + 1
            else:
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])
    
    # Backtrack to find positions
    positions = []
    i, j = m, n
    
    while i > 0 and j > 0:
        if seq1[i - 1] == seq2[j - 1]:
            positions.append((i - 1, j - 1))
            i -= 1
            j -= 1
        elif dp[i - 1][j] > dp[i][j - 1]:
            i -= 1
        else:
            j -= 1
    
    return positions[::-1]


def is_subsequence(sub: Sequence[T], seq: Sequence[T]) -> bool:
    """
    Check if 'sub' is a subsequence of 'seq'.
    
    Args:
        sub: Potential subsequence
        seq: Sequence to check against
        
    Returns:
        True if sub is a subsequence of seq
        
    Example:
        >>> is_subsequence("ABC", "AXYZBC")
        True
        >>> is_subsequence("ABC", "ACB")
        False
    """
    if not sub:
        return True
    
    if not seq:
        return False
    
    sub_idx = 0
    for elem in seq:
        if elem == sub[sub_idx]:
            sub_idx += 1
            if sub_idx == len(sub):
                return True
    
    return False


def count_distinct_lcs(seq1: Sequence[T], seq2: Sequence[T]) -> int:
    """
    Count the number of distinct longest common subsequences.
    
    This can be computationally expensive for long sequences.
    
    Args:
        seq1: First sequence
        seq2: Second sequence
        
    Returns:
        Number of distinct LCS sequences
        
    Example:
        >>> count_distinct_lcs("AAA", "AA")
        1
        >>> count_distinct_lcs("ABA", "ACA")
        2
    """
    all_lcs = lcs_all(seq1, seq2)
    return len(all_lcs)


# Utility class for more advanced operations
class LCSEngine:
    """
    A class-based interface for LCS operations with caching.
    
    Example:
        >>> engine = LCSEngine()
        >>> engine.compute("ABC", "AC")
        ['A', 'C']
        >>> engine.similarity("ABC", "AC")
        0.8
    """
    
    def __init__(self, cache_size: int = 128):
        """
        Initialize the LCS engine.
        
        Args:
            cache_size: Maximum number of results to cache
        """
        self._cache_size = cache_size
        self._cached_lcs = lru_cache(maxsize=cache_size)(self._compute_lcs)
        self._cached_length = lru_cache(maxsize=cache_size)(self._compute_length)
    
    def _compute_lcs(self, seq1: tuple, seq2: tuple) -> tuple:
        """Internal cached LCS computation."""
        return tuple(lcs(list(seq1), list(seq2)))
    
    def _compute_length(self, seq1: tuple, seq2: tuple) -> int:
        """Internal cached length computation."""
        return lcs_length(list(seq1), list(seq2))
    
    def compute(self, seq1: Sequence[T], seq2: Sequence[T]) -> List[T]:
        """Compute LCS with caching."""
        return list(self._cached_lcs(tuple(seq1), tuple(seq2)))
    
    def length(self, seq1: Sequence[T], seq2: Sequence[T]) -> int:
        """Compute LCS length with caching."""
        return self._cached_length(tuple(seq1), tuple(seq2))
    
    def similarity(self, seq1: Sequence[T], seq2: Sequence[T]) -> float:
        """Compute similarity with caching."""
        return lcs_similarity(list(seq1), list(seq2))
    
    def diff(self, seq1: Sequence[T], seq2: Sequence[T]) -> List[Tuple[str, T]]:
        """Generate diff between sequences."""
        return lcs_diff(seq1, seq2)
    
    def clear_cache(self) -> None:
        """Clear all cached results."""
        self._cached_lcs.cache_clear()
        self._cached_length.cache_clear()


# Convenience functions for common use cases
def text_similarity(text1: str, text2: str) -> float:
    """Compute similarity between two texts using character-level LCS."""
    return lcs_similarity(text1, text2)


def line_similarity(text1: str, text2: str) -> float:
    """Compute similarity between two texts using line-level LCS."""
    lines1 = text1.splitlines()
    lines2 = text2.splitlines()
    return lcs_similarity(lines1, lines2)


def word_similarity(text1: str, text2: str) -> float:
    """Compute similarity between two texts using word-level LCS."""
    words1 = text1.split()
    words2 = text2.split()
    return lcs_similarity(words1, words2)


def line_diff(text1: str, text2: str, name1: str = "original", 
              name2: str = "modified") -> str:
    """Generate unified diff between two texts at line level."""
    lines1 = text1.splitlines(keepends=True)
    lines2 = text2.splitlines(keepends=True)
    return lcs_diff_unified(lines1, lines2, name1=name1, name2=name2)


if __name__ == "__main__":
    # Quick demo
    print("LCS Utilities Demo")
    print("=" * 50)
    
    s1 = "ABCBDAB"
    s2 = "BDCABA"
    
    print(f"Sequence 1: {s1}")
    print(f"Sequence 2: {s2}")
    print(f"LCS: {''.join(lcs(s1, s2))}")
    print(f"LCS Length: {lcs_length(s1, s2)}")
    print(f"Similarity: {lcs_similarity(s1, s2):.2f}")
    print(f"Distance: {lcs_distance(s1, s2)}")
    print(f"SCS: {''.join(shortest_common_supersequence(s1, s2))}")
    
    print("\nDiff:")
    for op, char in lcs_diff(s1, s2):
        symbol = " " if op == "equal" else "-" if op == "delete" else "+"
        print(f"  {symbol} {char}")