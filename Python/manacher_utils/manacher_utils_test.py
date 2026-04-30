"""
Test suite for Manacher's Algorithm implementation
===================================================

Comprehensive tests for palindrome detection utilities.
"""

import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from manacher_utils import (
    longest_palindromic_substring,
    all_palindromic_substrings,
    count_palindromic_substrings,
    palindrome_info,
    find_palindromes_by_length,
    longest_palindrome_at,
    is_palindrome,
    manacher,
    preprocess
)


def test_preprocess():
    """Test string preprocessing."""
    print("Testing preprocess()...")
    
    assert preprocess("") == "^#$"
    assert preprocess("a") == "^#a#$"
    assert preprocess("ab") == "^#a#b#$"
    assert preprocess("abc") == "^#a#b#c#$"
    assert preprocess("aba") == "^#a#b#a#$"
    
    print("  ✓ preprocess() tests passed")


def test_manacher_basic():
    """Test basic Manacher algorithm output."""
    print("Testing manacher() basic...")
    
    # Empty string
    assert manacher("") == []
    
    # Single character
    P = manacher("a")
    assert max(P) == 1
    
    # Known patterns
    P = manacher("aba")
    assert max(P) == 3  # "aba" has radius 3
    
    P = manacher("aaaa")
    assert max(P) == 4  # entire string is palindrome
    
    print("  ✓ manacher() basic tests passed")


def test_longest_palindromic_substring():
    """Test finding longest palindromic substring."""
    print("Testing longest_palindromic_substring()...")
    
    # Basic cases
    assert longest_palindromic_substring("") == ""
    assert longest_palindromic_substring("a") == "a"
    assert longest_palindromic_substring("ab") in ["a", "b"]
    
    # Known cases
    result = longest_palindromic_substring("babad")
    assert result in ["bab", "aba"]
    assert len(result) == 3
    
    assert longest_palindromic_substring("cbbd") == "bb"
    
    # Full palindrome
    assert longest_palindromic_substring("racecar") == "racecar"
    assert longest_palindromic_substring("aaaa") == "aaaa"
    
    # Multiple equal length palindromes
    result = longest_palindromic_substring("abaab")
    assert result in ["aba", "baab"]
    
    # No palindrome longer than 1
    result = longest_palindromic_substring("abc")
    assert len(result) == 1
    
    print("  ✓ longest_palindromic_substring() tests passed")


def test_count_palindromic_substrings():
    """Test counting palindromic substrings."""
    print("Testing count_palindromic_substrings()...")
    
    assert count_palindromic_substrings("") == 0
    assert count_palindromic_substrings("a") == 1
    assert count_palindromic_substrings("ab") == 2
    assert count_palindromic_substrings("abc") == 3
    assert count_palindromic_substrings("aba") == 4  # a, b, a, aba
    assert count_palindromic_substrings("aaa") == 6  # a(3), aa(2), aaa(1)
    assert count_palindromic_substrings("aaaa") == 10
    
    print("  ✓ count_palindromic_substrings() tests passed")


def test_all_palindromic_substrings():
    """Test finding all palindromic substrings."""
    print("Testing all_palindromic_substrings()...")
    
    # Empty string
    assert all_palindromic_substrings("") == []
    
    # Single character
    assert all_palindromic_substrings("a") == ["a"]
    
    # Two different characters
    result = all_palindromic_substrings("ab")
    assert set(result) == {"a", "b"}
    
    # Multiple palindromes
    result = all_palindromic_substrings("aba")
    assert "aba" in result
    assert "a" in result
    assert "b" in result
    
    # Check that result is sorted by length descending
    result = all_palindromic_substrings("abaab")
    lengths = [len(x) for x in result]
    assert lengths == sorted(lengths, reverse=True)
    
    print("  ✓ all_palindromic_substrings() tests passed")


def test_palindrome_info():
    """Test comprehensive palindrome info."""
    print("Testing palindrome_info()...")
    
    # Empty string
    info = palindrome_info("")
    assert info['longest'] == ""
    assert info['length'] == 0
    assert info['count'] == 0
    assert info['has_palindrome'] == False
    
    # Single character
    info = palindrome_info("a")
    assert info['longest'] == "a"
    assert info['length'] == 1
    assert info['count'] == 1
    assert info['has_palindrome'] == False
    
    # Full palindrome
    info = palindrome_info("racecar")
    assert info['longest'] == "racecar"
    assert info['length'] == 7
    assert info['has_palindrome'] == True
    
    # Check centers
    info = palindrome_info("babad")
    assert len(info['centers']) > 0
    
    print("  ✓ palindrome_info() tests passed")


def test_find_palindromes_by_length():
    """Test finding palindromes by minimum length."""
    print("Testing find_palindromes_by_length()...")
    
    # Empty string
    assert find_palindromes_by_length("") == []
    
    # No palindromes >= 2
    assert find_palindromes_by_length("ab") == []
    
    # Some palindromes >= 2
    result = find_palindromes_by_length("aba", 2)
    assert "aba" in result
    
    result = find_palindromes_by_length("abaab", 3)
    assert set(result) == {"aba", "baab"}
    
    result = find_palindromes_by_length("abaab", 4)
    assert result == ["baab"]
    
    print("  ✓ find_palindromes_by_length() tests passed")


def test_longest_palindrome_at():
    """Test finding palindrome at specific position."""
    print("Testing longest_palindrome_at()...")
    
    # Empty or out of bounds
    assert longest_palindrome_at("", 0) == ""
    assert longest_palindrome_at("abc", 10) == ""
    
    # Known positions
    assert longest_palindrome_at("babad", 1) == "bab"
    assert longest_palindrome_at("racecar", 3) == "racecar"
    
    # Edge cases
    assert longest_palindrome_at("abc", 0) == "a"
    
    print("  ✓ longest_palindrome_at() tests passed")


def test_is_palindrome():
    """Test palindrome checking."""
    print("Testing is_palindrome()...")
    
    # Empty string
    assert is_palindrome("", 0, 0) == True
    
    # Invalid indices
    assert is_palindrome("abc", -1, 2) == False
    assert is_palindrome("abc", 0, 10) == False
    
    # Valid palindromes
    assert is_palindrome("aba", 0, 3) == True
    assert is_palindrome("aba", 1, 2) == True  # "b"
    assert is_palindrome("cbbd", 1, 3) == True  # "bb"
    
    # Non-palindromes
    assert is_palindrome("abc", 0, 3) == False
    assert is_palindrome("abaab", 1, 4) == False
    
    print("  ✓ is_palindrome() tests passed")


def test_performance():
    """Test performance with larger strings."""
    print("Testing performance...")
    
    # Create a large palindrome
    large_palindrome = "a" * 10000
    result = longest_palindromic_substring(large_palindrome)
    assert result == large_palindrome
    
    # Random-like string (mostly single character palindromes)
    import time
    random_like = "abcdefghij" * 1000
    start = time.time()
    count = count_palindromic_substrings(random_like)
    elapsed = time.time() - start
    
    # Should complete in reasonable time (< 1 second for 10000 chars)
    assert elapsed < 1.0
    assert count == len(random_like)  # Only single chars
    
    print(f"  ✓ Performance test passed ({elapsed:.3f}s for {len(random_like)} chars)")


def run_all_tests():
    """Run all test functions."""
    print("\n" + "=" * 60)
    print("Manacher's Algorithm Test Suite")
    print("=" * 60 + "\n")
    
    test_preprocess()
    test_manacher_basic()
    test_longest_palindromic_substring()
    test_count_palindromic_substrings()
    test_all_palindromic_substrings()
    test_palindrome_info()
    test_find_palindromes_by_length()
    test_longest_palindrome_at()
    test_is_palindrome()
    test_performance()
    
    print("\n" + "=" * 60)
    print("✓ All tests passed!")
    print("=" * 60)


if __name__ == "__main__":
    run_all_tests()