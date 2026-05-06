#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Levenshtein Utils Test Suite
Tests for Levenshtein distance and string similarity
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from levenshtein_utils.mod import (
    levenshtein_distance, similarity, find_closest, find_all_closest,
    edit_sequence, apply_edits, normalized_distance, ratio,
    hamming_distance, damerau_levenshtein_distance
)


class TestResultCollector:
    """Collects test results"""
    def __init__(self):
        self.passed = 0
        self.failed = 0
        self.tests = []
    
    def add_result(self, name, passed, message=""):
        self.tests.append((name, passed, message))
        if passed:
            self.passed += 1
        else:
            self.failed += 1
    
    def summary(self):
        total = self.passed + self.failed
        print(f"\n{'='*60}")
        print(f"Levenshtein Utils Test Results: {self.passed}/{total} passed")
        print(f"{'='*60}")
        if self.failed > 0:
            print("Failed tests:")
            for name, passed, msg in self.tests:
                if not passed:
                    print(f"  - {name}: {msg}")
        return self.failed == 0


results = TestResultCollector()


def test_levenshtein_distance():
    """Test basic Levenshtein distance"""
    try:
        # Same strings
        assert levenshtein_distance("abc", "abc") == 0
        
        # Empty strings
        assert levenshtein_distance("", "") == 0
        assert levenshtein_distance("", "abc") == 3
        assert levenshtein_distance("abc", "") == 3
        
        # Known examples
        assert levenshtein_distance("kitten", "sitting") == 3
        assert levenshtein_distance("book", "back") == 2
        assert levenshtein_distance("algorithm", "logarithm") == 3
        
        # Single character differences
        assert levenshtein_distance("a", "b") == 1
        assert levenshtein_distance("abc", "abd") == 1
        
        # Insertions
        assert levenshtein_distance("ab", "abc") == 1
        assert levenshtein_distance("abc", "abcd") == 1
        
        # Deletions
        assert levenshtein_distance("abc", "ab") == 1
        assert levenshtein_distance("abcd", "abc") == 1
        
        results.add_result("levenshtein_distance", True)
    except Exception as e:
        results.add_result("levenshtein_distance", False, str(e))


def test_levenshtein_custom_costs():
    """Test Levenshtein distance with custom costs"""
    try:
        # Standard costs
        assert levenshtein_distance("abc", "abd", insert_cost=1, delete_cost=1, replace_cost=1) == 1
        
        # Higher replace cost
        dist = levenshtein_distance("abc", "abd", replace_cost=2)
        # Replace 'c' with 'd' costs 2, or delete 'c' and insert 'd' costs 2
        assert dist == 2
        
        # Higher insert cost
        dist = levenshtein_distance("ab", "abc", insert_cost=2)
        assert dist == 2
        
        results.add_result("levenshtein_custom_costs", True)
    except Exception as e:
        results.add_result("levenshtein_custom_costs", False, str(e))


def test_similarity():
    """Test similarity calculation"""
    try:
        # Same strings
        assert similarity("abc", "abc") == 1.0
        
        # Empty strings
        assert similarity("", "") == 1.0
        assert similarity("", "abc") == 0.0
        assert similarity("abc", "") == 0.0
        
        # Known examples
        sim = similarity("kitten", "sitting")
        assert 0.5 < sim < 0.7
        
        # Completely different
        sim = similarity("abc", "xyz")
        assert sim == 0.0
        
        # Partial similarity
        sim = similarity("hello", "hallo")
        assert 0.7 < sim < 1.0
        
        results.add_result("similarity", True)
    except Exception as e:
        results.add_result("similarity", False, str(e))


def test_find_closest():
    """Test finding closest string"""
    try:
        candidates = ["apple", "banana", "orange", "applet"]
        
        # Find closest - appel is closest to apple/applet (2 edits)
        closest = find_closest("appel", candidates)
        assert closest in ["apple", "applet"]
        
        # With lower threshold - should match
        closest = find_closest("appel", candidates, threshold=0.5)
        assert closest is not None
        
        # High threshold - no match for xyz
        closest = find_closest("xyz", candidates, threshold=0.5)
        assert closest is None
        
        # Return distance
        result = find_closest("appel", candidates, return_distance=True)
        assert result is not None
        assert isinstance(result, tuple)
        assert len(result) == 2
        
        # Empty candidates
        assert find_closest("test", []) is None
        
        results.add_result("find_closest", True)
    except Exception as e:
        results.add_result("find_closest", False, str(e))


def test_find_all_closest():
    """Test finding all close strings"""
    try:
        candidates = ["apple", "applet", "application", "banana"]
        
        # Find all
        all_results = find_all_closest("apple", candidates, top_n=3)
        assert len(all_results) <= 3
        assert all_results[0][0] == "apple"
        assert all_results[0][1] == 1.0
        
        # With threshold
        filtered = find_all_closest("appel", candidates, threshold=0.5)
        for word, sim in filtered:
            assert sim >= 0.5
        
        # Empty candidates
        assert find_all_closest("test", []) == []
        
        results.add_result("find_all_closest", True)
    except Exception as e:
        results.add_result("find_all_closest", False, str(e))


def test_edit_sequence():
    """Test edit sequence generation"""
    try:
        # Get edit sequence
        dist, ops = edit_sequence("kitten", "sitting")
        assert dist == 3
        assert len(ops) > 0
        
        # Verify operations contain expected types
        op_types = [op[0] for op in ops]
        assert "replace" in op_types or "insert" in op_types
        
        # Same strings
        dist, ops = edit_sequence("abc", "abc")
        assert dist == 0
        assert len(ops) == 3  # Three equal operations
        for op, data in ops:
            assert op == "equal"
        
        results.add_result("edit_sequence", True)
    except Exception as e:
        results.add_result("edit_sequence", False, str(e))


def test_apply_edits():
    """Test applying edit operations"""
    try:
        # Get and apply edits
        dist, ops = edit_sequence("kitten", "sitting")
        result = apply_edits("kitten", ops)
        assert result == "sitting"
        
        # Same strings
        dist, ops = edit_sequence("abc", "abc")
        result = apply_edits("abc", ops)
        assert result == "abc"
        
        # Simple substitution
        dist, ops = edit_sequence("abc", "abd")
        result = apply_edits("abc", ops)
        assert result == "abd"
        
        results.add_result("apply_edits", True)
    except Exception as e:
        results.add_result("apply_edits", False, str(e))


def test_normalized_distance():
    """Test normalized distance"""
    try:
        # Same strings
        assert normalized_distance("abc", "abc") == 0.0
        
        # Empty strings
        assert normalized_distance("", "") == 0.0
        assert normalized_distance("", "abc") == 1.0
        assert normalized_distance("abc", "") == 1.0
        
        # Known values
        norm = normalized_distance("kitten", "sitting")
        assert 0 < norm < 1
        
        results.add_result("normalized_distance", True)
    except Exception as e:
        results.add_result("normalized_distance", False, str(e))


def test_ratio():
    """Test fuzzywuzzy-compatible ratio"""
    try:
        # Same strings
        assert ratio("abc", "abc") == 100.0
        
        # Empty strings
        assert ratio("", "") == 100.0
        
        # Known values - ratio is percentage
        r = ratio("hello world", "hello")
        assert 60 <= r <= 70
        
        r = ratio("fuzzy string matching", "fuzzy matching")
        assert 60 <= r <= 80
        
        results.add_result("ratio", True)
    except Exception as e:
        results.add_result("ratio", False, str(e))


def test_hamming_distance():
    """Test Hamming distance"""
    try:
        # Known examples
        assert hamming_distance("karolin", "kathrin") == 3
        assert hamming_distance("1011101", "1001001") == 2
        
        # Same strings
        assert hamming_distance("abc", "abc") == 0
        
        # Different lengths should raise
        try:
            hamming_distance("abc", "abcd")
            results.add_result("hamming_distance", False, "Should raise for different lengths")
        except ValueError:
            pass
        
        results.add_result("hamming_distance", True)
    except Exception as e:
        results.add_result("hamming_distance", False, str(e))


def test_damerau_levenshtein():
    """Test Damerau-Levenshtein distance"""
    try:
        # Transposition example
        dl = damerau_levenshtein_distance("abcd", "acbd")
        assert dl == 1  # One transposition
        
        # Standard Levenshtein for same example
        l = levenshtein_distance("abcd", "acbd")
        assert l == 2  # Two operations without transposition
        
        # DL should be <= L due to transpositions
        assert dl <= l
        
        # Same strings
        assert damerau_levenshtein_distance("abc", "abc") == 0
        
        # Empty strings
        assert damerau_levenshtein_distance("", "") == 0
        assert damerau_levenshtein_distance("", "abc") == 3
        
        results.add_result("damerau_levenshtein", True)
    except Exception as e:
        results.add_result("damerau_levenshtein", False, str(e))


def test_unicode_support():
    """Test Unicode string support"""
    try:
        # Chinese characters
        dist = levenshtein_distance("你好", "您好")
        assert dist == 1
        
        # Emoji
        dist = levenshtein_distance("🚀", "🚁")
        assert dist == 1
        
        # Mixed
        dist = levenshtein_distance("hello世界", "hello世界!")
        assert dist == 1
        
        results.add_result("unicode_support", True)
    except Exception as e:
        results.add_result("unicode_support", False, str(e))


def test_edge_cases():
    """Test edge cases"""
    try:
        # Very long strings
        long1 = "a" * 1000
        long2 = "b" * 1000
        dist = levenshtein_distance(long1, long2)
        assert dist == 1000
        
        # One character
        assert levenshtein_distance("a", "b") == 1
        
        # Long vs short
        dist = levenshtein_distance("a", "abcdefghij")
        assert dist == 9
        
        # Repeated patterns
        dist = levenshtein_distance("aaa", "bbb")
        assert dist == 3
        
        results.add_result("edge_cases", True)
    except Exception as e:
        results.add_result("edge_cases", False, str(e))


def test_case_sensitivity():
    """Test case sensitivity"""
    try:
        # Case matters
        assert levenshtein_distance("ABC", "abc") == 3
        
        # Different cases
        assert levenshtein_distance("hello", "HELLO") == 5
        
        results.add_result("case_sensitivity", True)
    except Exception as e:
        results.add_result("case_sensitivity", False, str(e))


def test_similarity_range():
    """Test similarity is always in valid range"""
    try:
        test_cases = [
            ("abc", "abc"),
            ("", ""),
            ("abc", ""),
            ("", "abc"),
            ("abcdef", "xyz"),
            ("hello", "hallo"),
            ("kitten", "sitting"),
        ]
        
        for s1, s2 in test_cases:
            sim = similarity(s1, s2)
            assert 0 <= sim <= 1
        
        results.add_result("similarity_range", True)
    except Exception as e:
        results.add_result("similarity_range", False, str(e))


def test_find_closest_exact_match():
    """Test find_closest with exact match"""
    try:
        candidates = ["apple", "banana", "orange"]
        closest = find_closest("apple", candidates)
        assert closest == "apple"
        
        # Should have highest similarity
        match_results = find_all_closest("apple", candidates)
        assert match_results[0][0] == "apple"
        assert match_results[0][1] == 1.0
        
        results.add_result("find_closest_exact_match", True)
    except Exception as e:
        results.add_result("find_closest_exact_match", False, str(e))


# Run all tests
def run_tests():
    """Run all test functions"""
    test_levenshtein_distance()
    test_levenshtein_custom_costs()
    test_similarity()
    test_find_closest()
    test_find_all_closest()
    test_edit_sequence()
    test_apply_edits()
    test_normalized_distance()
    test_ratio()
    test_hamming_distance()
    test_damerau_levenshtein()
    test_unicode_support()
    test_edge_cases()
    test_case_sensitivity()
    test_similarity_range()
    test_find_closest_exact_match()
    
    return results.summary()


if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)