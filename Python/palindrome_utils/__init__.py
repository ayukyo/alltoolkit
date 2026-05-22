"""
AllToolkit - Palindrome Utilities Module
=========================================
A comprehensive palindrome detection and processing utility module.

Features:
    - Check if string is palindrome
    - Find all palindrome substrings
    - Find longest palindrome substring
    - Count palindromes in text
    - Generate palindrome from string (minimum additions)
    - Support for case-sensitive/insensitive matching
    - Unicode support for multi-language palindromes
"""

from .mod import (
    is_palindrome,
    normalize_for_palindrome,
    find_all_palindromes,
    find_longest_palindrome,
    count_palindromes,
    find_palindromic_subsequences,
    min_insertions_to_palindrome,
    make_palindrome,
    find_palindrome_pairs,
    is_palindrome_number,
    generate_palindromes,
    longest_palindromic_subsequence_length,
    get_palindrome_info,
    is_semordnilap,
    is_mirrored_palindrome,
    PalindromeMatch
)

__all__ = [
    'is_palindrome',
    'normalize_for_palindrome',
    'find_all_palindromes',
    'find_longest_palindrome',
    'count_palindromes',
    'find_palindromic_subsequences',
    'min_insertions_to_palindrome',
    'make_palindrome',
    'find_palindrome_pairs',
    'is_palindrome_number',
    'generate_palindromes',
    'longest_palindromic_subsequence_length',
    'get_palindrome_info',
    'is_semordnilap',
    'is_mirrored_palindrome',
    'PalindromeMatch'
]