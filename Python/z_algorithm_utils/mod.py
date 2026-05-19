"""
AllToolkit - Python Z Algorithm Utilities

A zero-dependency implementation of the Z-algorithm for efficient string matching
and pattern searching. Provides O(n) computation of Z-array and various string
analysis utilities.

Author: AllToolkit
License: MIT
"""

from typing import List, Tuple, Optional, Iterator
from dataclasses import dataclass


# ============================================================================
# Data Classes
# ============================================================================

@dataclass
class ZMatch:
    """Represents a match found using Z-algorithm."""
    index: int
    length: int
    text: str
    
    def __repr__(self) -> str:
        return f"ZMatch(index={self.index}, length={self.length})"
    
    @property
    def matched_substring(self) -> str:
        """Get the matched substring."""
        return self.text[self.index:self.index + self.length]


@dataclass
class StringPeriod:
    """Represents the period information of a string."""
    string: str
    period: int
    is_periodic: bool
    
    def __repr__(self) -> str:
        return f"StringPeriod(period={self.period}, is_periodic={self.is_periodic})"
    
    @property
    def period_string(self) -> str:
        """Get the repeating unit."""
        return self.string[:self.period]


# ============================================================================
# Core Z-Algorithm
# ============================================================================

def z_array(s: str) -> List[int]:
    """
    Compute the Z-array for a string.
    
    Z[i] is the length of the longest substring starting from i
    that is also a prefix of the string.
    
    Time complexity: O(n)
    Space complexity: O(n)
    
    Args:
        s: Input string
        
    Returns:
        List of Z values where Z[0] is defined as 0
        
    Example:
        >>> z_array("aabcaabxaaz")
        [0, 1, 0, 0, 3, 1, 0, 0, 2, 1, 0]
    """
    n = len(s)
    if n == 0:
        return []
    
    z = [0] * n
    l, r = 0, 0  # [l, r] is the rightmost Z-box
    
    for i in range(1, n):
        if i <= r:
            # i is within current Z-box
            z[i] = min(r - i + 1, z[i - l])
        
        # Try to extend the Z-box
        while i + z[i] < n and s[z[i]] == s[i + z[i]]:
            z[i] += 1
        
        # Update Z-box if we extended past r
        if i + z[i] - 1 > r:
            l, r = i, i + z[i] - 1
    
    return z


def z_array_bytes(data: bytes) -> List[int]:
    """
    Compute the Z-array for a byte sequence.
    
    Args:
        data: Input bytes
        
    Returns:
        List of Z values
    """
    n = len(data)
    if n == 0:
        return []
    
    z = [0] * n
    l, r = 0, 0
    
    for i in range(1, n):
        if i <= r:
            z[i] = min(r - i + 1, z[i - l])
        
        while i + z[i] < n and data[z[i]] == data[i + z[i]]:
            z[i] += 1
        
        if i + z[i] - 1 > r:
            l, r = i, i + z[i] - 1
    
    return z


def z_array_with_sentinel(pattern: str, text: str, sentinel: str = "$") -> List[int]:
    """
    Compute Z-array for pattern$text concatenation.
    
    Args:
        pattern: Pattern to search for
        text: Text to search in
        sentinel: Separator character (must not appear in pattern or text)
        
    Returns:
        Z-array of the concatenated string
    """
    combined = pattern + sentinel + text
    return z_array(combined)


# ============================================================================
# Pattern Matching
# ============================================================================

def find_all_occurrences(pattern: str, text: str) -> List[int]:
    """
    Find all occurrences of pattern in text using Z-algorithm.
    
    Time complexity: O(n + m) where n = len(text), m = len(pattern)
    
    Args:
        pattern: Pattern to search for
        text: Text to search in
        
    Returns:
        List of starting indices where pattern occurs
        
    Example:
        >>> find_all_occurrences("abc", "abcabcabc")
        [0, 3, 6]
    """
    if not pattern or not text:
        return []
    
    m, n = len(pattern), len(text)
    if m > n:
        return []
    
    # Build Z-array for pattern$text
    combined = pattern + "$" + text
    z = z_array(combined)
    
    # Find all positions where Z[i] >= m
    positions = []
    for i in range(m + 1, len(z)):
        if z[i] >= m:
            positions.append(i - m - 1)
    
    return positions


def find_first_occurrence(pattern: str, text: str) -> int:
    """
    Find the first occurrence of pattern in text.
    
    Args:
        pattern: Pattern to search for
        text: Text to search in
        
    Returns:
        Index of first occurrence, or -1 if not found
    """
    if not pattern or not text:
        return -1
    
    m, n = len(pattern), len(text)
    if m > n:
        return -1
    
    combined = pattern + "$" + text
    z = z_array(combined)
    
    for i in range(m + 1, len(z)):
        if z[i] >= m:
            return i - m - 1
    
    return -1


def count_occurrences(pattern: str, text: str) -> int:
    """
    Count the number of occurrences of pattern in text.
    
    Args:
        pattern: Pattern to search for
        text: Text to search in
        
    Returns:
        Number of occurrences
    """
    return len(find_all_occurrences(pattern, text))


def find_matches(pattern: str, text: str) -> List[ZMatch]:
    """
    Find all matches of pattern in text with details.
    
    Args:
        pattern: Pattern to search for
        text: Text to search in
        
    Returns:
        List of ZMatch objects
    """
    positions = find_all_occurrences(pattern, text)
    return [ZMatch(index=pos, length=len(pattern), text=text) for pos in positions]


# ============================================================================
# Substring Analysis
# ============================================================================

def longest_prefix_suffix(s: str) -> int:
    """
    Find the length of the longest proper prefix that is also a suffix.
    
    Args:
        s: Input string
        
    Returns:
        Length of longest proper prefix that is also a suffix
        
    Example:
        >>> longest_prefix_suffix("ababa")
        3  # "aba"
    """
    if not s:
        return 0
    
    z = z_array(s)
    n = len(s)
    
    # Find the maximum Z value where the substring ends at the string end
    # i + z[i] == n means s[i:n] matches s[0:z[i]]
    max_lps = 0
    for i in range(1, n):
        if i + z[i] == n:
            max_lps = max(max_lps, z[i])
    
    return max_lps


def longest_repeated_substring(s: str) -> Tuple[str, List[int]]:
    """
    Find the longest substring that appears at least twice in the string.
    
    Args:
        s: Input string
        
    Returns:
        Tuple of (longest repeated substring, list of starting positions)
        
    Example:
        >>> longest_repeated_substring("banana")
        ('ana', [1, 3])
    """
    if not s:
        return ("", [])
    
    n = len(s)
    z = z_array(s)
    
    max_len = 0
    positions = []
    
    for i in range(1, n):
        if z[i] > max_len:
            max_len = z[i]
            positions = [i]
        elif z[i] == max_len and max_len > 0:
            positions.append(i)
    
    # Also need to check if longer substring exists elsewhere
    # We need to search for substrings not starting at 0
    for length in range(n // 2, max_len, -1):
        for start in range(n - length):
            substr = s[start:start + length]
            # Use Z-algorithm to find this substring
            found = find_all_occurrences(substr, s)
            if len(found) >= 2:
                return (substr, found)
    
    if max_len == 0:
        return ("", [])
    
    return (s[:max_len], positions)


def find_all_repeated_substrings(s: str, min_length: int = 2) -> List[Tuple[str, List[int]]]:
    """
    Find all repeated substrings with at least min_length.
    
    Args:
        s: Input string
        min_length: Minimum length of repeated substrings
        
    Returns:
        List of (substring, positions) tuples, sorted by length descending
    """
    if len(s) < min_length * 2:
        return []
    
    n = len(s)
    result = []
    seen = set()
    
    # Check all possible lengths
    for length in range(n // 2, min_length - 1, -1):
        for start in range(n - length + 1):
            substr = s[start:start + length]
            if substr in seen:
                continue
            
            positions = find_all_occurrences(substr, s)
            if len(positions) >= 2:
                result.append((substr, positions))
                seen.add(substr)
    
    # Sort by length descending
    result.sort(key=lambda x: -len(x[0]))
    return result


def longest_common_prefix(s1: str, s2: str) -> int:
    """
    Find the length of the longest common prefix of two strings.
    
    Args:
        s1: First string
        s2: Second string
        
    Returns:
        Length of longest common prefix
    """
    combined = s1 + "$" + s2
    z = z_array(combined)
    
    # The Z value at position len(s1) + 1 gives the LCP
    pos = len(s1) + 1
    if pos < len(z):
        return z[pos]
    return 0


# ============================================================================
# Period and Palindrome Detection
# ============================================================================

def find_minimal_period(s: str) -> StringPeriod:
    """
    Find the minimal period of a string.
    
    A string has period p if s[i] == s[i + p] for all valid i.
    
    Args:
        s: Input string
        
    Returns:
        StringPeriod object with period information
        
    Example:
        >>> find_minimal_period("abcabcabc")
        StringPeriod(period=3, is_periodic=True)
    """
    if not s:
        return StringPeriod(string=s, period=0, is_periodic=False)
    
    n = len(s)
    
    # Check all possible periods
    for p in range(1, n // 2 + 1):
        if n % p != 0:
            continue
        
        # Verify period p
        is_valid = True
        for i in range(p, n):
            if s[i] != s[i % p]:
                is_valid = False
                break
        
        if is_valid:
            return StringPeriod(string=s, period=p, is_periodic=True)
    
    # Using Z-array approach for more general case
    z = z_array(s)
    
    # Find smallest period
    for p in range(1, n + 1):
        if p + z[p] >= n if p < n else True:
            # Check if this is truly a period
            valid = True
            for i in range(p, n):
                if s[i] != s[i - p]:
                    valid = False
                    break
            if valid:
                return StringPeriod(string=s, period=p, is_periodic=(p < n))
    
    return StringPeriod(string=s, period=n, is_periodic=False)


def is_rotation(s1: str, s2: str) -> bool:
    """
    Check if s2 is a rotation of s1.
    
    Args:
        s1: First string
        s2: Second string
        
    Returns:
        True if s2 is a rotation of s1
        
    Example:
        >>> is_rotation("abcde", "cdeab")
        True
    """
    if len(s1) != len(s2):
        return False
    
    if not s1:  # Both empty
        return True
    
    # s2 is rotation of s1 iff s2 is substring of s1 + s1
    return len(find_all_occurrences(s2, s1 + s1)) > 0


def find_all_rotations(s: str) -> List[str]:
    """
    Find all unique rotations of a string.
    
    Args:
        s: Input string
        
    Returns:
        List of all rotations (may have duplicates for periodic strings)
    """
    if not s:
        return [""]
    
    n = len(s)
    rotations = [s[i:] + s[:i] for i in range(n)]
    
    # Remove duplicates while preserving order
    seen = set()
    unique = []
    for rot in rotations:
        if rot not in seen:
            seen.add(rot)
            unique.append(rot)
    
    return unique


# ============================================================================
# Palindrome Extensions
# ============================================================================

def longest_palindromic_prefix(s: str) -> str:
    """
    Find the longest prefix that is a palindrome.
    
    Uses Z-algorithm on s + "$" + reverse(s).
    
    Args:
        s: Input string
        
    Returns:
        Longest palindromic prefix
    """
    if not s:
        return ""
    
    # Build combined string
    combined = s + "$" + s[::-1]
    z = z_array(combined)
    
    # Find the largest Z value in the reversed part
    n = len(s)
    max_len = 0
    
    for i in range(n + 1, len(z)):
        # Position in reversed string
        rev_pos = i - n - 1
        # Position in original string
        orig_pos = n - 1 - rev_pos
        
        if z[i] == orig_pos + 1:
            # This means s[0:z[i]] matches the suffix starting at orig_pos
            if z[i] > max_len:
                max_len = z[i]
    
    return s[:max_len]


def longest_palindromic_suffix(s: str) -> str:
    """
    Find the longest suffix that is a palindrome.
    
    Args:
        s: Input string
        
    Returns:
        Longest palindromic suffix
    """
    if not s:
        return ""
    
    # Reverse, find longest palindromic prefix, then reverse back
    reversed_s = s[::-1]
    result = longest_palindromic_prefix(reversed_s)
    return result[::-1]


# ============================================================================
# String Similarity
# ============================================================================

def similarity_score(s1: str, s2: str) -> float:
    """
    Calculate a similarity score based on longest common prefix.
    
    Args:
        s1: First string
        s2: Second string
        
    Returns:
        Similarity score between 0 and 1
    """
    if not s1 and not s2:
        return 1.0
    if not s1 or not s2:
        return 0.0
    
    lcp = longest_common_prefix(s1, s2)
    max_len = max(len(s1), len(s2))
    
    return lcp / max_len


def batch_similarity(base: str, strings: List[str]) -> List[float]:
    """
    Calculate similarity scores for multiple strings against a base string.
    
    Uses Z-algorithm for efficient computation.
    
    Args:
        base: Base string to compare against
        strings: List of strings to compare
        
    Returns:
        List of similarity scores
    """
    if not base:
        return [0.0 if s else 1.0 for s in strings]
    
    max_len = max(len(base), max((len(s) for s in strings), default=1))
    
    results = []
    for s in strings:
        if not s:
            results.append(0.0)
        else:
            lcp = longest_common_prefix(base, s)
            results.append(lcp / max_len)
    
    return results


# ============================================================================
# Advanced Operations
# ============================================================================

def distinct_substring_count(s: str) -> int:
    """
    Count the number of distinct substrings using Z-algorithm.
    
    Time complexity: O(n^2)
    
    Args:
        s: Input string
        
    Returns:
        Number of distinct substrings
    """
    n = len(s)
    if n == 0:
        return 0
    
    # Use suffix-based approach
    total = 0
    for i in range(n):
        # Compute Z-array for suffix s[i:]
        suffix = s[i:]
        z = z_array(suffix)
        # Number of new substrings starting at i
        total += (n - i) - max(z) if z else (n - i)
    
    return total


def compress_string(s: str) -> Tuple[str, int]:
    """
    Compress a string by finding its smallest repeating unit.
    
    Args:
        s: Input string
        
    Returns:
        Tuple of (compressed form, repetition count)
        
    Example:
        >>> compress_string("abcabcabc")
        ('abc', 3)
    """
    if not s:
        return ("", 1)
    
    period = find_minimal_period(s)
    
    if period.is_periodic:
        return (period.period_string, len(s) // period.period)
    
    return (s, 1)


def decompress_string(pattern: str, count: int) -> str:
    """
    Decompress a string pattern.
    
    Args:
        pattern: The repeating unit
        count: Number of repetitions
        
    Returns:
        Decompressed string
    """
    return pattern * count


# ============================================================================
# Search Iterator
# ============================================================================

def iter_occurrences(pattern: str, text: str) -> Iterator[int]:
    """
    Iterate over all occurrences of pattern in text.
    
    Memory-efficient generator version for large texts.
    
    Args:
        pattern: Pattern to search for
        text: Text to search in
        
    Yields:
        Starting indices of matches
    """
    if not pattern or not text:
        return
    
    m, n = len(pattern), len(text)
    if m > n:
        return
    
    combined = pattern + "$" + text
    z = z_array(combined)
    
    for i in range(m + 1, len(z)):
        if z[i] >= m:
            yield i - m - 1


# ============================================================================
# Border Array (KMP relation)
# ============================================================================

def z_to_border(z: List[int]) -> List[int]:
    """
    Convert Z-array to border array (failure function).
    
    The border array b[i] is the length of the longest proper border
    (prefix that is also suffix) of s[0:i+1].
    
    Args:
        z: Z-array
        
    Returns:
        Border array
    """
    n = len(z)
    if n == 0:
        return []
    
    border = [0] * n
    
    for i in range(1, n):
        if z[i] > 0:
            # s[i:i+z[i]] == s[0:z[i]]
            # So border[i + z[i] - 1] >= z[i]
            end = i + z[i] - 1
            if end < n:
                border[end] = max(border[end], z[i])
    
    # Propagate border values
    for i in range(n - 1):
        border[i + 1] = max(border[i + 1], border[i] - 1) if border[i] > 0 else border[i + 1]
    
    return border


def border_to_z(border: List[int]) -> List[int]:
    """
    Convert border array to Z-array.
    
    Args:
        border: Border array (failure function)
        
    Returns:
        Z-array
    """
    n = len(border)
    if n == 0:
        return []
    
    # Reconstruct string prefix and compute Z
    z = [0] * n
    for i in range(1, n):
        if border[i - 1] > 0:
            z[i - border[i - 1] + 1] = max(z[i - border[i - 1] + 1], border[i - 1])
    
    return z


# ============================================================================
# Pattern Matcher Class
# ============================================================================

class ZPatternMatcher:
    """
    Efficient pattern matcher using Z-algorithm.
    
    Precompute patterns for efficient multi-pattern matching.
    """
    
    def __init__(self, patterns: List[str]):
        """
        Initialize with a list of patterns.
        
        Args:
            patterns: List of patterns to search for
        """
        self.patterns = patterns
        self._z_arrays = [z_array(p) for p in patterns]
    
    def search(self, text: str) -> List[Tuple[int, int, str]]:
        """
        Search for all patterns in text.
        
        Args:
            text: Text to search in
            
        Returns:
            List of (pattern_index, position, pattern) tuples
        """
        results = []
        for i, pattern in enumerate(self.patterns):
            positions = find_all_occurrences(pattern, text)
            for pos in positions:
                results.append((i, pos, pattern))
        
        return results
    
    def search_first(self, text: str) -> Optional[Tuple[int, int, str]]:
        """
        Find the first occurrence of any pattern.
        
        Args:
            text: Text to search in
            
        Returns:
            Tuple of (pattern_index, position, pattern) or None
        """
        first_match = None
        first_pos = len(text)
        first_pattern_idx = -1
        
        for i, pattern in enumerate(self.patterns):
            pos = find_first_occurrence(pattern, text)
            if pos != -1 and pos < first_pos:
                first_pos = pos
                first_pattern_idx = i
        
        if first_pattern_idx >= 0:
            return (first_pattern_idx, first_pos, self.patterns[first_pattern_idx])
        return None
    
    def count_all(self, text: str) -> dict:
        """
        Count occurrences of each pattern.
        
        Args:
            text: Text to search in
            
        Returns:
            Dictionary mapping pattern to count
        """
        return {p: count_occurrences(p, text) for p in self.patterns}


# ============================================================================
# Utility Functions
# ============================================================================

def visualize_z_array(s: str) -> str:
    """
    Create a visual representation of the Z-array.
    
    Args:
        s: Input string
        
    Returns:
        String visualization of the Z-array
    """
    z = z_array(s)
    lines = []
    
    lines.append(f"String: {s}")
    lines.append(f"Index:  {' '.join(str(i).rjust(2) for i in range(len(s)))}")
    lines.append(f"Char:   {' '.join(c.rjust(2) for c in s)}")
    lines.append(f"Z:      {' '.join(str(v).rjust(2) for v in z)}")
    
    # Add visual boxes
    for i, val in enumerate(z):
        if val > 0:
            box_start = i
            box_end = i + val - 1
            if box_end < len(s):
                line = [' '] * len(s) * 3
                for j in range(box_start, box_end + 1):
                    line[j * 3:j * 3 + 3] = ['[', s[j], ']']
                lines.append(''.join(line).rstrip())
    
    return '\n'.join(lines)


def validate_z_array(s: str, z: List[int]) -> bool:
    """
    Validate that a Z-array is correct for a given string.
    
    Args:
        s: Input string
        z: Z-array to validate
        
    Returns:
        True if the Z-array is valid
    """
    if len(s) != len(z):
        return False
    
    computed = z_array(s)
    return z == computed