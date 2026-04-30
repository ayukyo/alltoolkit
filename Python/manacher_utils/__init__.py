"""
Manacher's Algorithm Utils
==========================

Efficient palindrome detection using Manacher's algorithm (O(n) complexity).

Key functions:
- longest_palindromic_substring: Find the longest palindrome
- count_palindromic_substrings: Count total palindromic substrings
- all_palindromic_substrings: Get all unique palindromes
- palindrome_info: Comprehensive palindrome information
- find_palindromes_by_length: Filter palindromes by minimum length
- longest_palindrome_at: Find palindrome at specific position
- is_palindrome: Check if substring is palindrome
"""

from .manacher_utils import (
    longest_palindromic_substring,
    count_palindromic_substrings,
    all_palindromic_substrings,
    palindrome_info,
    find_palindromes_by_length,
    longest_palindrome_at,
    is_palindrome,
    manacher,
    preprocess
)

__all__ = [
    'longest_palindromic_substring',
    'count_palindromic_substrings',
    'all_palindromic_substrings',
    'palindrome_info',
    'find_palindromes_by_length',
    'longest_palindrome_at',
    'is_palindrome',
    'manacher',
    'preprocess'
]