#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AllToolkit - Palindrome Utilities Usage Examples
=================================================
Practical examples demonstrating palindrome_utils module capabilities.
"""

import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from palindrome_utils.mod import (
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
    is_mirrored_palindrome
)


def example_basic_detection():
    """Basic palindrome detection examples."""
    print("=" * 60)
    print("Basic Palindrome Detection")
    print("=" * 60)
    
    # Simple palindromes
    test_strings = [
        "racecar",
        "level",
        "deed",
        "hello",
        "world",
        "A man, a plan, a canal: Panama",
        "Was it a car or a cat I saw?",
        "上海自来水来自海上",
        "黄山落叶松叶落山黄"
    ]
    
    for s in test_strings:
        result = is_palindrome(s)
        print(f"  '{s}' → {result}")
    
    print()
    
    # Case-sensitive checking
    print("Case-sensitive checking:")
    print(f"  'RaceCar' (case-sensitive): {is_palindrome('RaceCar', case_sensitive=True)}")
    print(f"  'RaceCar' (case-insensitive): {is_palindrome('RaceCar', case_sensitive=False)}")
    print()


def example_find_palindromes():
    """Finding palindromes in strings."""
    print("=" * 60)
    print("Finding Palindromes in Strings")
    print("=" * 60)
    
    strings = ["ababa", "racecar", "google", "abcba"]
    
    for s in strings:
        print(f"\nString: '{s}'")
        
        # Find all palindromes
        palindromes = find_all_palindromes(s, min_length=2)
        if palindromes:
            print("  All palindromes:")
            for p in palindromes:
                print(f"    - '{p.text}' at position {p.start}-{p.end}")
        else:
            print("  No palindromes found")
        
        # Find longest
        longest = find_longest_palindrome(s)
        if longest:
            print(f"  Longest: '{longest.text}' (length {longest.length})")
        
        # Count
        count = count_palindromes(s)
        print(f"  Total count: {count}")
    
    print()


def example_palindrome_transformation():
    """Palindrome transformation examples."""
    print("=" * 60)
    print("Palindrome Transformation")
    print("=" * 60)
    
    strings = ["ab", "abc", "google", "abcd"]
    
    for s in strings:
        min_ins = min_insertions_to_palindrome(s)
        result = make_palindrome(s)
        
        print(f"  '{s}' → '{result}'")
        print(f"    Minimum insertions: {min_ins}")
        print(f"    Verification: {is_palindrome(result)}")
    
    print()


def example_palindrome_numbers():
    """Palindrome number examples."""
    print("=" * 60)
    print("Palindrome Numbers")
    print("=" * 60)
    
    numbers = [121, 123, 12321, 12345678987654321, -121, 0, 11]
    
    for n in numbers:
        result = is_palindrome_number(n)
        print(f"  {n} → {result}")
    
    print()


def example_palindrome_pairs():
    """Palindrome pairs examples."""
    print("=" * 60)
    print("Palindrome Pairs")
    print("=" * 60)
    
    word_lists = [
        ["abcd", "dcba", "lls", "s", "sssll"],
        ["bat", "tab", "cat"],
        ["hello", "olleh", "world"]
    ]
    
    for words in word_lists:
        print(f"\nWord list: {words}")
        pairs = find_palindrome_pairs(words)
        
        if pairs:
            print("  Palindrome pairs:")
            for i, j in pairs:
                combined = words[i] + words[j]
                print(f"    ({i}, {j}): '{words[i]}' + '{words[j]}' = '{combined}'")
        else:
            print("  No palindrome pairs found")
    
    print()


def example_palindrome_generation():
    """Palindrome generation examples."""
    print("=" * 60)
    print("Palindrome Generation")
    print("=" * 60)
    
    # Generate palindromes of various lengths
    charset = "abc"
    
    for length in [1, 2, 3, 4]:
        palindromes = generate_palindromes(length, charset)
        print(f"  Length {length} palindromes with charset '{charset}':")
        print(f"    {palindromes}")
        print(f"    Count: {len(palindromes)}")
    
    print()


def example_palindromic_subsequences():
    """Palindromic subsequences examples."""
    print("=" * 60)
    print("Palindromic Subsequences")
    print("=" * 60)
    
    strings = ["abc", "aaa", "aba", "bbbab"]
    
    for s in strings:
        print(f"\nString: '{s}'")
        
        # All subsequences
        subsequences = find_palindromic_subsequences(s)
        print(f"  All subsequences: {sorted(subsequences)}")
        
        # Longest subsequence length
        longest_len = longest_palindromic_subsequence_length(s)
        print(f"  Longest subsequence length: {longest_len}")
    
    print()


def example_special_palindromes():
    """Special palindrome types examples."""
    print("=" * 60)
    print("Special Palindrome Types")
    print("=" * 60)
    
    # Semordnilaps
    print("\nSemordnilaps (words that form other words when reversed):")
    words = ["stressed", "desserts", "dog", "god", "racecar"]
    for word in words:
        result = is_semordnilap(word)
        reversed_word = word[::-1]
        print(f"  '{word}' → reversed: '{reversed_word}' → semordnilap: {result}")
    
    # Mirrored palindromes
    print("\nMirrored Palindromes:")
    words = ["AHA", "IOIO", "ATOYOTA", "MOM", "DAD"]
    for word in words:
        result = is_mirrored_palindrome(word)
        print(f"  '{word}' → mirrored palindrome: {result}")
    
    print()


def example_comprehensive_info():
    """Comprehensive palindrome information example."""
    print("=" * 60)
    print("Comprehensive Palindrome Information")
    print("=" * 60)
    
    strings = ["racecar", "google", "abcba", "上海自来水来自海上"]
    
    for s in strings:
        print(f"\nAnalysis of '{s}':")
        info = get_palindrome_info(s)
        
        print(f"  Is palindrome: {info['is_palindrome']}")
        print(f"  Normalized: '{info['normalized']}'")
        print(f"  Longest palindrome: {info['longest_palindrome']}")
        print(f"  Palindrome count: {info['palindrome_count']}")
        
        if info['all_palindromes']:
            print(f"  All palindromes: {info['all_palindromes']}")
        
        print(f"  Min insertions for palindrome: {info['min_insertions_for_palindrome']}")
        print(f"  Longest palindromic subsequence length: {info['longest_palindromic_subsequence']}")
        
        if info['palindromes_by_length']:
            print("  Palindromes by length:")
            for length, texts in info['palindromes_by_length'].items():
                print(f"    Length {length}: {texts}")
    
    print()


def example_practical_applications():
    """Practical application examples."""
    print("=" * 60)
    print("Practical Applications")
    print("=" * 60)
    
    # 1. Word game validation
    print("\n1. Word game validation (check if player input is palindrome):")
    player_inputs = ["racecar", "kayak", "hello", "A man, a plan, a canal: Panama"]
    for input_word in player_inputs:
        is_valid = is_palindrome(input_word)
        print(f"  '{input_word}' → Valid palindrome: {is_valid}")
    
    # 2. Data validation (check if IDs are palindromes)
    print("\n2. ID validation (numeric palindrome check):")
    ids = [121, 12345, 12321, 123454321]
    for id_num in ids:
        is_valid = is_palindrome_number(id_num)
        print(f"  ID {id_num} → Valid palindrome: {is_valid}")
    
    # 3. Text analysis (find palindromic phrases)
    print("\n3. Text analysis (find palindromic phrases in text):")
    text = "The racecar drove by. A kayak floated. The deed was done."
    
    # Extract words and check
    words = text.replace('.', '').split()
    palindromic_words = [w for w in words if is_palindrome(w)]
    print(f"  Text: '{text}'")
    print(f"  Palindromic words found: {palindromic_words}")
    
    # 4. Password generation (generate palindromic passwords)
    print("\n4. Palindromic password generation:")
    charset = "abcdefghijklmnopqrstuvwxyz0123456789"
    passwords = generate_palindromes(8, charset)[:5]  # First 5
    print(f"  Sample 8-character palindromic passwords:")
    for pwd in passwords:
        print(f"    {pwd}")
    
    print()


def run_all_examples():
    """Run all examples."""
    example_basic_detection()
    example_find_palindromes()
    example_palindrome_transformation()
    example_palindrome_numbers()
    example_palindrome_pairs()
    example_palindrome_generation()
    example_palindromic_subsequences()
    example_special_palindromes()
    example_comprehensive_info()
    example_practical_applications()
    
    print("=" * 60)
    print("All examples completed!")
    print("=" * 60)


if __name__ == '__main__':
    run_all_examples()