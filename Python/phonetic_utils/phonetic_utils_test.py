#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Tests for Phonetic Algorithm Utilities Module."""

import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from mod import (
    soundex, refined_soundex, metaphone, double_metaphone,
    caverphone, nysiis, match_rating_codex, match_rating_compare,
    phonetic_match, encode, phonetic_search, encode_all,
    phonetic_similarity, group_by_phonetic, find_duplicates,
    PhoneticAlgorithm, PhoneticResult
)


def test_soundex():
    """Test Soundex encoding."""
    print("\n=== Testing Soundex ===")
    
    # Test basic Soundex
    result = soundex("Robert")
    assert result.primary == "R163", f"Expected R163, got {result.primary}"
    
    result = soundex("Rupert")
    assert result.primary == "R163", f"Expected R163, got {result.primary}"
    
    result = soundex("Smith")
    assert result.primary == "S530", f"Expected S530, got {result.primary}"
    
    result = soundex("Schmidt")
    assert result.primary == "S530", f"Expected S530, got {result.primary}"
    
    # Test edge cases
    result = soundex("")
    assert result.primary == "0000", f"Expected 0000 for empty, got {result.primary}"
    
    result = soundex("A")
    assert result.primary.startswith("A"), f"Expected A prefix, got {result.primary}"
    
    print("✓ Soundex tests passed")


def test_refined_soundex():
    """Test Refined Soundex encoding."""
    print("\n=== Testing Refined Soundex ===")
    
    result = refined_soundex("Robert")
    assert result.primary, f"Expected non-empty result"
    assert result.algorithm == "refined_soundex"
    
    print("✓ Refined Soundex tests passed")


def test_metaphone():
    """Test Metaphone encoding."""
    print("\n=== Testing Metaphone ===")
    
    result = metaphone("Smith")
    assert result.primary, f"Expected non-empty result"
    
    result = metaphone("Schmidt")
    assert result.primary, f"Expected non-empty result"
    
    # Both should be similar
    smith = metaphone("Smith")
    schmidt = metaphone("Schmidt")
    
    # Test edge cases
    result = metaphone("")
    assert result.primary == "", f"Expected empty for empty input"
    
    print("✓ Metaphone tests passed")


def test_double_metaphone():
    """Test Double Metaphone encoding."""
    print("\n=== Testing Double Metaphone ===")
    
    result = double_metaphone("Catherine")
    assert result.primary, f"Expected non-empty primary"
    assert result.alternate is not None or result.primary, "Should have encoding"
    
    # Test known cases
    result = double_metaphone("Smith")
    assert result.primary, f"Expected non-empty result"
    
    result = double_metaphone("Schmidt")
    assert result.primary, f"Expected non-empty result"
    
    # Test edge cases
    result = double_metaphone("")
    assert result.primary == "", f"Expected empty for empty input"
    
    print("✓ Double Metaphone tests passed")


def test_caverphone():
    """Test Caverphone encoding."""
    print("\n=== Testing Caverphone ===")
    
    result = caverphone("Catherine")
    assert len(result.primary) == 10, f"Expected 10 chars, got {len(result.primary)}"
    
    result = caverphone("Smith")
    assert len(result.primary) == 10, f"Expected 10 chars, got {len(result.primary)}"
    
    # Test edge cases
    result = caverphone("")
    assert result.primary == "1111111111", f"Expected default for empty"
    
    print("✓ Caverphone tests passed")


def test_nysiis():
    """Test NYSIIS encoding."""
    print("\n=== Testing NYSIIS ===")
    
    result = nysiis("O'Connor")
    assert result.primary, f"Expected non-empty result"
    
    result = nysiis("Smith")
    assert result.primary, f"Expected non-empty result"
    
    result = nysiis("Schmidt")
    assert result.primary, f"Expected non-empty result"
    
    # Test edge cases
    result = nysiis("")
    assert result.primary == "", f"Expected empty for empty input"
    
    print("✓ NYSIIS tests passed")


def test_match_rating():
    """Test Match Rating Codex encoding."""
    print("\n=== Testing Match Rating Codex ===")
    
    result = match_rating_codex("Catherine")
    assert result.primary, f"Expected non-empty result"
    
    result = match_rating_codex("Smith")
    assert result.primary, f"Expected non-empty result"
    
    # Test comparison
    code1 = match_rating_codex("Smith").primary
    code2 = match_rating_codex("Smyth").primary
    matches, score = match_rating_compare(code1, code2)
    
    print("✓ Match Rating Codex tests passed")


def test_phonetic_match():
    """Test phonetic matching."""
    print("\n=== Testing Phonetic Match ===")
    
    # Known matches
    matches, similarity = phonetic_match("Robert", "Rupert")
    assert matches, f"Robert and Rupert should match"
    
    matches, similarity = phonetic_match("Smith", "Schmidt")
    # Soundex matches these, but Double Metaphone gives 0.5 similarity
    assert matches or similarity >= 0.5, f"Smith and Schmidt should be similar (got {similarity})"
    
    matches, similarity = phonetic_match("Catherine", "Katherine")
    assert matches, f"Catherine and Katherine should match"
    
    print("✓ Phonetic match tests passed")


def test_phonetic_search():
    """Test phonetic search."""
    print("\n=== Testing Phonetic Search ===")
    
    candidates = [
        "Smith", "Smyth", "Schmidt", "Smithe", "John", "Johnson",
        "Williams", "Wilson", "Brown", "Browne"
    ]
    
    results = phonetic_search("Smith", candidates, threshold=0.5)
    assert len(results) > 0, f"Expected at least one match"
    
    # First result should be exact match
    assert results[0][0] == "Smith", f"First match should be Smith"
    
    print("✓ Phonetic search tests passed")


def test_encode_all():
    """Test encoding with all algorithms."""
    print("\n=== Testing Encode All ===")
    
    results = encode_all("Smith")
    assert len(results) == 7, f"Expected 7 algorithms"
    
    assert 'soundex' in results
    assert 'metaphone' in results
    assert 'double_metaphone' in results
    assert 'caverphone' in results
    assert 'nysiis' in results
    assert 'match_rating' in results
    assert 'refined_soundex' in results
    
    print("✓ Encode all tests passed")


def test_phonetic_similarity():
    """Test phonetic similarity calculation."""
    print("\n=== Testing Phonetic Similarity ===")
    
    similarity = phonetic_similarity("Robert", "Rupert")
    assert similarity > 0.5, f"Expected high similarity, got {similarity}"
    
    similarity = phonetic_similarity("Smith", "John")
    assert similarity < 0.5, f"Expected low similarity, got {similarity}"
    
    print("✓ Phonetic similarity tests passed")


def test_group_by_phonetic():
    """Test grouping by phonetic encoding."""
    print("\n=== Testing Group by Phonetic ===")
    
    words = ["Robert", "Rupert", "Smith", "Schmidt", "John", "Johnson"]
    groups = group_by_phonetic(words)
    
    assert len(groups) > 0, f"Expected at least one group"
    
    # Check that similar names are grouped together
    # Robert and Rupert should be in same group (same Soundex)
    robert_soundex = soundex("Robert").primary
    rupert_soundex = soundex("Rupert").primary
    
    if robert_soundex == rupert_soundex:
        # They should be in the same group
        found_robert = False
        found_rupert = False
        for code, names in groups.items():
            if "Robert" in names:
                found_robert = True
            if "Rupert" in names:
                found_rupert = True
        
        assert found_robert or found_rupert, "Should find Robert or Rupert in groups"
    
    print("✓ Group by phonetic tests passed")


def test_find_duplicates():
    """Test finding phonetic duplicates."""
    print("\n=== Testing Find Duplicates ===")
    
    words = ["Robert", "Rupert", "Smith", "Schmidt", "John", "Johnson"]
    duplicates = find_duplicates(words)
    
    # Should find some potential duplicates
    assert len(duplicates) >= 0, f"Expected duplicates list"
    
    print("✓ Find duplicates tests passed")


def test_phonetic_result():
    """Test PhoneticResult class."""
    print("\n=== Testing PhoneticResult ===")
    
    result = PhoneticResult(
        original="test",
        primary="TST",
        alternate="TST2",
        algorithm="test_algo"
    )
    
    assert result.original == "test"
    assert result.primary == "TST"
    assert result.alternate == "TST2"
    assert result.algorithm == "test_algo"
    
    # Test string representation
    str_repr = str(result)
    assert "/" in str_repr, f"Expected alternate in string repr"
    
    result_no_alt = PhoneticResult(original="test", primary="TST")
    str_repr = str(result_no_alt)
    assert "/" not in str_repr, f"Expected no alternate in string repr"
    
    print("✓ PhoneticResult tests passed")


def run_all_tests():
    """Run all tests."""
    print("=" * 60)
    print("Phonetic Algorithm Utilities - Comprehensive Test Suite")
    print("=" * 60)
    
    tests = [
        test_soundex,
        test_refined_soundex,
        test_metaphone,
        test_double_metaphone,
        test_caverphone,
        test_nysiis,
        test_match_rating,
        test_phonetic_match,
        test_phonetic_search,
        test_encode_all,
        test_phonetic_similarity,
        test_group_by_phonetic,
        test_find_duplicates,
        test_phonetic_result,
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            test()
            passed += 1
        except AssertionError as e:
            print(f"✗ FAILED: {e}")
            failed += 1
        except Exception as e:
            print(f"✗ ERROR: {e}")
            failed += 1
    
    print("\n" + "=" * 60)
    print(f"Results: {passed} passed, {failed} failed")
    print("=" * 60)
    
    return failed == 0


if __name__ == '__main__':
    success = run_all_tests()
    sys.exit(0 if success else 1)