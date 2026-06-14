#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AllToolkit - Palindrome Utilities Module
========================================
A comprehensive palindrome detection and processing utility module for Python
with zero external dependencies.

Features:
    - Check if string is palindrome
    - Find all palindrome substrings
    - Find longest palindrome substring
    - Count palindromes in text
    - Generate palindrome from string (minimum additions)
    - Support for case-sensitive/insensitive matching
    - Support for ignoring non-alphanumeric characters
    - Unicode support for multi-language palindromes

Author: AllToolkit Contributors
License: MIT
Date: 2026-05-23
"""

import re
from typing import List, Tuple, Optional, Set
from dataclasses import dataclass


@dataclass
class PalindromeMatch:
    """Represents a palindrome match in a string."""
    text: str
    start: int
    end: int
    length: int
    
    def __repr__(self):
        return f"PalindromeMatch('{self.text}', pos={self.start}-{self.end})"


def is_palindrome(
    s: str,
    case_sensitive: bool = False,
    alnum_only: bool = True,
    ignore_spaces: bool = True,
    ignore_punctuation: bool = True
) -> bool:
    """
    Check if a string is a palindrome.
    
    Args:
        s: String to check
        case_sensitive: If True, case matters (default False)
        alnum_only: If True, only consider alphanumeric characters (default True)
        ignore_spaces: If True, ignore spaces (default True)
        ignore_punctuation: If True, ignore punctuation (default True)
    
    Returns:
        True if string is a palindrome, False otherwise
    
    Examples:
        >>> is_palindrome("racecar")
        True
        >>> is_palindrome("A man, a plan, a canal: Panama")
        True
        >>> is_palindrome("hello")
        False
        >>> is_palindrome("Race Car", case_sensitive=True)
        False
        >>> is_palindrome("上海自来水来自海上")  # Chinese palindrome
        True
    """
    if not s:
        return True
    
    # Normalize string
    processed = s
    
    if not case_sensitive:
        processed = processed.lower()
    
    if alnum_only or ignore_spaces or ignore_punctuation:
        # Keep only alphanumeric characters
        processed = ''.join(c for c in processed if c.isalnum())
    
    # Optimized palindrome check: early-exit two-pointer comparison
    # avoids creating reversed string slice for most non-palindromes
    left, right = 0, len(processed) - 1
    while left < right:
        if processed[left] != processed[right]:
            return False
        left += 1
        right -= 1
    
    return True


def normalize_for_palindrome(
    s: str,
    case_sensitive: bool = False,
    alnum_only: bool = True
) -> str:
    """
    Normalize a string for palindrome checking.
    
    Args:
        s: String to normalize
        case_sensitive: If True, preserve case (default False)
        alnum_only: If True, keep only alphanumeric characters (default True)
    
    Returns:
        Normalized string
    
    Examples:
        >>> normalize_for_palindrome("A man, a plan, a canal: Panama")
        'amanaplanacanalpanama'
        >>> normalize_for_palindrome("Hello World!", case_sensitive=True)
        'HelloWorld'
    """
    if not case_sensitive:
        s = s.lower()
    
    if alnum_only:
        s = ''.join(c for c in s if c.isalnum())
    
    return s


def find_all_palindromes(
    s: str,
    min_length: int = 2,
    case_sensitive: bool = False,
    unique: bool = True
) -> List[PalindromeMatch]:
    """
    Find all palindrome substrings in a string.
    
    Uses center expansion algorithm (O(n^2) time complexity).
    
    Args:
        s: String to search
        min_length: Minimum length of palindromes to find (default 2)
        case_sensitive: If True, case matters (default False)
        unique: If True, return only unique palindromes (default True)
    
    Returns:
        List of PalindromeMatch objects
    
    Examples:
        >>> palindromes = find_all_palindromes("ababa")
        >>> [p.text for p in palindromes]
        ['aba', 'bab', 'ababa']
        >>> find_all_palindromes("abc", min_length=1)
        []
    """
    if not s:
        return []
    
    if not case_sensitive:
        search_str = s.lower()
    else:
        search_str = s
    
    n = len(s)
    palindromes = []
    seen = set() if unique else None
    
    def expand_around_center(left: int, right: int):
        """Expand around center to find palindromes."""
        while left >= 0 and right < n and search_str[left] == search_str[right]:
            length = right - left + 1
            if length >= min_length:
                text = s[left:right + 1]
                if unique:
                    key = (text, left, right)
                    if key not in seen:
                        seen.add(key)
                        palindromes.append(PalindromeMatch(text, left, right + 1, length))
                else:
                    palindromes.append(PalindromeMatch(text, left, right + 1, length))
            left -= 1
            right += 1
    
    # Check for odd-length palindromes
    for i in range(n):
        expand_around_center(i, i)
    
    # Check for even-length palindromes
    for i in range(n - 1):
        expand_around_center(i, i + 1)
    
    # Sort by starting position, then by length (longest first)
    palindromes.sort(key=lambda p: (p.start, -p.length))
    
    return palindromes


def find_longest_palindrome(
    s: str,
    case_sensitive: bool = False
) -> Optional[PalindromeMatch]:
    """
    Find the longest palindrome substring in a string.
    
    Uses Manacher's algorithm (O(n) time complexity).
    
    Args:
        s: String to search
        case_sensitive: If True, case matters (default False)
    
    Returns:
        PalindromeMatch of the longest palindrome, or None if not found
    
    Examples:
        >>> find_longest_palindrome("babad")
        PalindromeMatch('bab', pos=0-3)
        >>> find_longest_palindrome("cbbd")
        PalindromeMatch('bb', pos=1-3)
        >>> find_longest_palindrome("abc")
        None
    """
    if not s:
        return None
    
    if not case_sensitive:
        search_str = s.lower()
    else:
        search_str = s
    
    # Preprocess string to handle even-length palindromes
    # Insert '#' between characters and at boundaries
    processed = '#' + '#'.join(search_str) + '#'
    n = len(processed)
    
    # Array to store palindrome radius at each position
    p = [0] * n
    center = 0
    right = 0
    
    max_radius = 0
    max_center = 0
    
    for i in range(n):
        # Mirror of i around center
        mirror = 2 * center - i
        
        if i < right:
            p[i] = min(right - i, p[mirror])
        
        # Expand around i
        left_bound = i - p[i] - 1
        right_bound = i + p[i] + 1
        
        while left_bound >= 0 and right_bound < n and processed[left_bound] == processed[right_bound]:
            p[i] += 1
            left_bound -= 1
            right_bound += 1
        
        # Update center and right boundary
        if i + p[i] > right:
            center = i
            right = i + p[i]
        
        # Track maximum
        if p[i] > max_radius:
            max_radius = p[i]
            max_center = i
    
    if max_radius == 0:
        return None
    
    # Extract original indices
    start = (max_center - max_radius) // 2
    length = max_radius
    
    return PalindromeMatch(s[start:start + length], start, start + length, length)


def count_palindromes(
    s: str,
    min_length: int = 2,
    case_sensitive: bool = False,
    unique: bool = False
) -> int:
    """
    Count the number of palindrome substrings in a string.
    
    Args:
        s: String to search
        min_length: Minimum length of palindromes to count (default 2)
        case_sensitive: If True, case matters (default False)
        unique: If True, count only unique palindromes (default False)
    
    Returns:
        Number of palindrome substrings
    
    Examples:
        >>> count_palindromes("aaa")
        3
        >>> count_palindromes("aaa", unique=True)
        2
        >>> count_palindromes("abc")
        0
    """
    palindromes = find_all_palindromes(s, min_length, case_sensitive, unique)
    return len(palindromes)


def find_palindromic_subsequences(
    s: str,
    case_sensitive: bool = False
) -> List[str]:
    """
    Find all distinct palindromic subsequences in a string.
    
    A subsequence is a sequence that can be derived from the string
    by deleting some or no elements without changing the order.
    
    Args:
        s: String to search
        case_sensitive: If True, case matters (default False)
    
    Returns:
        List of distinct palindromic subsequences
    
    Examples:
        >>> sorted(find_palindromic_subsequences("abc"))
        ['a', 'b', 'c']
        >>> sorted(find_palindromic_subsequences("aaa"))
        ['a', 'aa', 'aaa']
        >>> sorted(find_palindromic_subsequences("aba"))
        ['a', 'aba', 'b']
    
    Note:
        Time complexity is O(n^2) where n is the length of the string.
        For strings with many repeated characters, the number of
        subsequences can be exponential.
    """
    if not s:
        return []
    
    if not case_sensitive:
        s = s.lower()
    
    n = len(s)
    
    # dp[i][j] = set of palindromic subsequences in s[i:j+1]
    dp = [[set() for _ in range(n)] for _ in range(n)]
    
    # Single characters are palindromes
    for i in range(n):
        dp[i][i].add(s[i])
    
    # Fill the DP table
    for length in range(2, n + 1):
        for i in range(n - length + 1):
            j = i + length - 1
            
            if s[i] == s[j]:
                # If endpoints match, they can form palindromes
                # with any palindrome in between
                if length == 2:
                    dp[i][j].add(s[i] + s[j])
                else:
                    # Add the outer characters to all inner palindromes
                    for inner in dp[i + 1][j - 1]:
                        dp[i][j].add(s[i] + inner + s[j])
                    # Also add the bare endpoints
                    dp[i][j].add(s[i] + s[j])
            
            # Include palindromes from inner ranges
            dp[i][j].update(dp[i + 1][j])
            dp[i][j].update(dp[i][j - 1])
    
    return list(dp[0][n - 1])


def min_insertions_to_palindrome(s: str) -> int:
    """
    Calculate the minimum number of insertions needed to make a string a palindrome.
    
    Uses dynamic programming approach.
    
    Args:
        s: String to analyze
    
    Returns:
        Minimum number of insertions needed
    
    Examples:
        >>> min_insertions_to_palindrome("ab")
        1
        >>> min_insertions_to_palindrome("abc")
        2
        >>> min_insertions_to_palindrome("racecar")
        0
        >>> min_insertions_to_palindrome("google")
        2
    """
    if not s:
        return 0
    
    n = len(s)
    
    # dp[i][j] = minimum insertions to make s[i:j+1] a palindrome
    dp = [[0] * n for _ in range(n)]
    
    # Fill for all lengths
    for length in range(2, n + 1):
        for i in range(n - length + 1):
            j = i + length - 1
            
            if s[i] == s[j]:
                dp[i][j] = dp[i + 1][j - 1]
            else:
                dp[i][j] = min(dp[i + 1][j], dp[i][j - 1]) + 1
    
    return dp[0][n - 1]


def make_palindrome(s: str, case_sensitive: bool = False) -> str:
    """
    Convert a string to a palindrome by adding minimum characters.
    
    Adds characters to the end of the string to make it a palindrome.
    
    Args:
        s: String to convert
        case_sensitive: If True, case matters (default False)
    
    Returns:
        Palindrome string
    
    Examples:
        >>> make_palindrome("abc")
        'abcba'
        >>> make_palindrome("ab")
        'aba'
        >>> make_palindrome("racecar")
        'racecar'
    """
    if not s:
        return s
    
    if is_palindrome(s, case_sensitive=case_sensitive):
        return s
    
    if not case_sensitive:
        s = s.lower()
    
    # Find the longest palindromic suffix
    n = len(s)
    
    for i in range(n):
        suffix = s[i:]
        if is_palindrome(suffix, case_sensitive=True):
            # Add reverse of prefix before the suffix
            prefix = s[:i]
            return s + prefix[::-1]
    
    return s + s[:-1][::-1]


def find_palindrome_pairs(words: List[str], case_sensitive: bool = False) -> List[Tuple[int, int]]:
    """
    Find all pairs of indices where concatenation forms a palindrome.
    
    Args:
        words: List of strings
        case_sensitive: If True, case matters (default False)
    
    Returns:
        List of tuples (i, j) where words[i] + words[j] is a palindrome
    
    Examples:
        >>> find_palindrome_pairs(["abcd", "dcba", "lls", "s", "sssll"])
        [(0, 1), (1, 0), (2, 4), (3, 2)]
        >>> find_palindrome_pairs(["bat", "tab", "cat"])
        [(0, 1), (1, 0)]
    
    Note:
        Time complexity is O(n * k^2) where n is the number of words
        and k is the average length of words.
    """
    if not words:
        return []
    
    if not case_sensitive:
        words = [w.lower() for w in words]
    
    n = len(words)
    pairs = []
    
    # Build a map of word to its index
    word_map = {word: i for i, word in enumerate(words)}
    
    for i, word in enumerate(words):
        word_len = len(word)
        
        # For each possible split point
        for j in range(word_len + 1):
            prefix = word[:j]
            suffix = word[j:]
            
            # Case 1: prefix is palindrome, find reverse of suffix
            if is_palindrome(prefix, case_sensitive=True):
                reverse_suffix = suffix[::-1]
                if reverse_suffix in word_map:
                    k = word_map[reverse_suffix]
                    if k != i:
                        pairs.append((k, i))
            
            # Case 2: suffix is palindrome, find reverse of prefix
            if j < word_len and is_palindrome(suffix, case_sensitive=True):
                reverse_prefix = prefix[::-1]
                if reverse_prefix in word_map:
                    k = word_map[reverse_prefix]
                    if k != i:
                        pairs.append((i, k))
    
    # Remove duplicates and sort
    pairs = list(set(pairs))
    pairs.sort()
    
    return pairs


def is_palindrome_number(n: int) -> bool:
    """
    Check if an integer is a palindrome without converting to string.
    
    Args:
        n: Integer to check
    
    Returns:
        True if integer is a palindrome, False otherwise
    
    Examples:
        >>> is_palindrome_number(121)
        True
        >>> is_palindrome_number(123)
        False
        >>> is_palindrome_number(-121)
        False
        >>> is_palindrome_number(0)
        True
    """
    if n < 0:
        return False
    
    if n < 10:
        return True
    
    # Find the divisor to extract the leading digit
    divisor = 1
    temp = n
    while temp >= 10:
        temp //= 10
        divisor *= 10
    
    # Fixed: use `n >= divisor` instead of `n > 0` to correctly handle
    # numbers ending with zeros (e.g. 1000 should return False, not True)
    # Added `divisor > 0` guard: divisor shrinks by 100 each iteration and can
    # reach 0 for long palindromes, causing ZeroDivisionError
    while n >= divisor and divisor > 0:
        leading = n // divisor
        trailing = n % 10
        
        if leading != trailing:
            return False
        
        # Remove leading and trailing digits
        n = (n % divisor) // 10
        divisor //= 100
    
    return True


def generate_palindromes(
    length: int,
    charset: str = "abcdefghijklmnopqrstuvwxyz",
    unique: bool = True
) -> List[str]:
    """
    Generate all possible palindromes of a given length.
    
    Args:
        length: Length of palindromes to generate
        charset: Characters to use (default lowercase letters)
        unique: If True, return only unique palindromes (default True)
    
    Returns:
        List of palindrome strings
    
    Examples:
        >>> generate_palindromes(1, "ab")
        ['a', 'b']
        >>> generate_palindromes(2, "ab")
        ['aa', 'bb']
        >>> generate_palindromes(3, "ab")
        ['aaa', 'aba', 'bab', 'bbb']
    
    Note:
        For large lengths, this generates an exponential number of palindromes.
        Use with caution.
    """
    if length <= 0:
        return []
    
    from itertools import product
    
    palindromes = []
    half_length = (length + 1) // 2
    
    # Generate all possible first halves
    for half in product(charset, repeat=half_length):
        half_str = ''.join(half)
        
        # Construct palindrome
        if length % 2 == 0:
            palindrome = half_str + half_str[::-1]
        else:
            palindrome = half_str + half_str[:-1][::-1]
        
        palindromes.append(palindrome)
    
    if unique:
        palindromes = list(set(palindromes))
    
    palindromes.sort()
    return palindromes


def longest_palindromic_subsequence_length(s: str) -> int:
    """
    Find the length of the longest palindromic subsequence.
    
    Uses dynamic programming (O(n^2) time, O(n^2) space).
    
    Args:
        s: Input string
    
    Returns:
        Length of longest palindromic subsequence
    
    Examples:
        >>> longest_palindromic_subsequence_length("bbbab")
        4
        >>> longest_palindromic_subsequence_length("cbbd")
        2
        >>> longest_palindromic_subsequence_length("abc")
        1
    """
    if not s:
        return 0
    
    n = len(s)
    
    # dp[i][j] = length of longest palindromic subsequence in s[i:j+1]
    dp = [[0] * n for _ in range(n)]
    
    # Single characters are palindromes of length 1
    for i in range(n):
        dp[i][i] = 1
    
    # Fill for all lengths
    for length in range(2, n + 1):
        for i in range(n - length + 1):
            j = i + length - 1
            
            if s[i] == s[j]:
                dp[i][j] = dp[i + 1][j - 1] + 2
            else:
                dp[i][j] = max(dp[i + 1][j], dp[i][j - 1])
    
    return dp[0][n - 1]


def get_palindrome_info(s: str) -> dict:
    """
    Get comprehensive information about palindromes in a string.
    
    Args:
        s: String to analyze
    
    Returns:
        Dictionary with palindrome statistics and information
    
    Examples:
        >>> info = get_palindrome_info("racecar")
        >>> info['is_palindrome']
        True
        >>> info['longest_palindrome']
        'racecar'
        >>> info['palindrome_count']
        3
    """
    is_palin = is_palindrome(s)
    longest = find_longest_palindrome(s)
    all_palindromes = find_all_palindromes(s, min_length=2)
    
    return {
        'original_string': s,
        'normalized': normalize_for_palindrome(s),
        'is_palindrome': is_palin,
        'longest_palindrome': longest.text if longest else None,
        'longest_palindrome_position': (longest.start, longest.end) if longest else None,
        'palindrome_count': len(all_palindromes),
        'all_palindromes': [p.text for p in all_palindromes],
        'palindromes_by_length': _group_by_length(all_palindromes),
        'min_insertions_for_palindrome': min_insertions_to_palindrome(s),
        'longest_palindromic_subsequence': longest_palindromic_subsequence_length(s)
    }


def _group_by_length(palindromes: List[PalindromeMatch]) -> dict:
    """Group palindromes by their length."""
    groups = {}
    for p in palindromes:
        if p.length not in groups:
            groups[p.length] = []
        groups[p.length].append(p.text)
    return dict(sorted(groups.items()))


# ============================================================================
# Special Palindrome Types
# ============================================================================

def is_semordnilap(s: str) -> bool:
    """
    Check if a string is a semordnilap (word that forms another word when reversed).
    
    Note: This function only checks if the reversed string is different.
    A true semordnilap should form another valid word when reversed.
    
    Args:
        s: String to check
    
    Returns:
        True if reversed string is different from original
    
    Examples:
        >>> is_semordnilap("stressed")
        True  # reversed is "desserts"
        >>> is_semordnilap("racecar")
        False  # is a palindrome, reversed is same
    """
    return s.lower() != s[::-1].lower()


def is_mirrored_palindrome(s: str, mirror_map: dict = None) -> bool:
    """
    Check if a string is a mirrored palindrome (reads same when mirrored).
    
    A mirrored palindrome is a string that looks the same when held up
    to a mirror. Each character must have a valid mirror character.
    
    Default mirror map includes common characters and their mirrors.
    
    Args:
        s: String to check
        mirror_map: Dictionary mapping characters to their mirrors
    
    Returns:
        True if string is a mirrored palindrome
    
    Examples:
        >>> is_mirrored_palindrome("AHA")
        True
        >>> is_mirrored_palindrome("ATOYOTA")
        True
        >>> is_mirrored_palindrome("IOIO")
        False
    """
    if mirror_map is None:
        # Default mirror map (vertical mirror - characters that look the same when reflected)
        # These characters are symmetric about a vertical axis
        mirror_map = {
            'A': 'A', 'H': 'H', 'I': 'I', 'M': 'M', 'O': 'O',
            'T': 'T', 'U': 'U', 'V': 'V', 'W': 'W', 'X': 'X', 'Y': 'Y',
            '0': '0', '1': '1', '8': '8',
        }
    
    s = s.upper()
    
    # For mirrored palindrome, each character from right must mirror to left character
    # E.g., "ATOYOTA" reversed is "ATOYOTA", each char maps to itself
    # For proper mirror, we need: mirror_map[char] == reversed_string's corresponding char
    
    try:
        n = len(s)
        for i in range(n):
            # Character at position i must mirror to character at position n-1-i
            char_from_left = s[i]
            char_from_right = s[n - 1 - i]
            
            # Check if left char's mirror equals right char
            if mirror_map.get(char_from_left) != char_from_right:
                return False
        
        return True
    except KeyError:
        return False


if __name__ == '__main__':
    # Quick demo
    print("=== Palindrome Detection Examples ===")
    print(f"is_palindrome('racecar'): {is_palindrome('racecar')}")
    print(f"is_palindrome('A man, a plan, a canal: Panama'): {is_palindrome('A man, a plan, a canal: Panama')}")
    print(f"is_palindrome('上海自来水来自海上'): {is_palindrome('上海自来水来自海上')}")
    
    print("\n=== Find All Palindromes ===")
    palindromes = find_all_palindromes("ababa")
    for p in palindromes:
        print(f"  {p}")
    
    print("\n=== Find Longest Palindrome ===")
    longest = find_longest_palindrome("babad")
    print(f"  Longest in 'babad': {longest}")
    
    print("\n=== Palindrome Number Check ===")
    print(f"is_palindrome_number(121): {is_palindrome_number(121)}")
    print(f"is_palindrome_number(123): {is_palindrome_number(123)}")
    
    print("\n=== Min Insertions to Palindrome ===")
    print(f"min_insertions_to_palindrome('google'): {min_insertions_to_palindrome('google')}")
    print(f"make_palindrome('google'): {make_palindrome('google')}")
    
    print("\n=== Palindrome Pairs ===")
    pairs = find_palindrome_pairs(["abcd", "dcba", "lls", "s", "sssll"])
    print(f"Pairs: {pairs}")
    
    print("\n=== Comprehensive Palindrome Info ===")
    info = get_palindrome_info("racecar")
    for key, value in info.items():
        if key != 'all_palindromes':
            print(f"  {key}: {value}")