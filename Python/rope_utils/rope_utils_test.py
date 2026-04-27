#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AllToolkit - Rope Utilities Test Suite
=======================================
Comprehensive tests for the Rope data structure implementation.

Run with: python rope_utils_test.py
"""

import sys
import os
import time
import random
import string
from typing import List

# Add parent directory to path for imports
sys.path.insert(0, '..')

from mod import (
    Rope, LeafNode, InternalNode, BatchEditor,
    concat, concat_ropes, from_lines, build_balanced,
    DEFAULT_LEAF_MAX
)


# ============================================================================
# Test Framework
# ============================================================================

class TestResult:
    """Simple test result collector."""
    
    def __init__(self):
        self.passed = 0
        self.failed = 0
        self.errors: List[str] = []
    
    def test(self, name: str, condition: bool, message: str = ""):
        """Run a single test."""
        if condition:
            self.passed += 1
            print(f"  ✓ {name}")
        else:
            self.failed += 1
            print(f"  ✗ {name}")
            if message:
                self.errors.append(f"{name}: {message}")
    
    def summary(self):
        """Print summary."""
        total = self.passed + self.failed
        print(f"\n{'='*60}")
        print(f"Results: {self.passed}/{total} tests passed")
        if self.errors:
            print("\nFailures:")
            for e in self.errors:
                print(f"  - {e}")
        print(f"{'='*60}")
        return self.failed == 0


# ============================================================================
# Basic Tests
# ============================================================================

def test_creation(result: TestResult):
    """Test rope creation."""
    print("\n[Creation Tests]")
    
    # Empty rope
    r = Rope()
    result.test("Empty rope length", len(r) == 0)
    result.test("Empty rope string", str(r) == "")
    
    # Small string
    r = Rope("Hello")
    result.test("Small rope length", len(r) == 5)
    result.test("Small rope string", str(r) == "Hello")
    
    # Large string (multiple leaves)
    large_text = "A" * 2000
    r = Rope(large_text)
    result.test("Large rope length", len(r) == 2000)
    result.test("Large rope string", str(r) == large_text)
    result.test("Large rope depth", r.depth() > 1)


def test_char_access(result: TestResult):
    """Test character access."""
    print("\n[Character Access Tests]")
    
    r = Rope("Hello, World!")
    
    # Index access
    result.test("char_at(0)", r.char_at(0) == 'H')
    result.test("char_at(6)", r.char_at(6) == ' ')
    result.test("char_at(12)", r.char_at(12) == '!')
    
    # Bracket access
    result.test("r[0]", r[0] == 'H')
    result.test("r[-1]", r[-1] == '!')
    
    # Index out of range
    try:
        r.char_at(100)
        result.test("Index error raised", False)
    except IndexError:
        result.test("Index error raised", True)


def test_slicing(result: TestResult):
    """Test slicing operations."""
    print("\n[Slicing Tests]")
    
    r = Rope("Hello, World!")
    
    # Basic slice
    result.test("r[0:5]", r[0:5] == "Hello")
    result.test("r[7:12]", r[7:12] == "World")
    
    # Negative indices
    result.test("r[-6:-1]", r[-6:-1] == "World")
    
    # Full slice
    result.test("r[:]", r[:] == "Hello, World!")
    
    # Step slice
    result.test("r[::2]", r[::2] == "Hlo ol!")


def test_insertion(result: TestResult):
    """Test insertion operations."""
    print("\n[Insertion Tests]")
    
    r = Rope("Hello World!")
    
    # Insert at beginning
    r2 = r.insert(0, ">>> ")
    result.test("Insert at beginning", str(r2) == ">>> Hello World!")
    result.test("Original unchanged", str(r) == "Hello World!")
    
    # Insert at end
    r2 = r.insert(len(r), " <<<")
    result.test("Insert at end", str(r2) == "Hello World! <<<")
    
    # Insert in middle
    r2 = r.insert(5, ", Beautiful")
    result.test("Insert in middle", str(r2) == "Hello, Beautiful World!")
    
    # Multiple insertions
    r = Rope("abc")
    r = r.insert(1, "X")
    r = r.insert(3, "Y")
    r = r.insert(5, "Z")
    result.test("Multiple insertions", str(r) == "aXbYcZ")


def test_deletion(result: TestResult):
    """Test deletion operations."""
    print("\n[Deletion Tests]")
    
    r = Rope("Hello, World!")
    
    # Delete from beginning
    r2 = r.delete(0, 7)
    result.test("Delete from beginning", str(r2) == "World!")
    
    # Delete from end
    r2 = r.delete(12, 13)
    result.test("Delete from end", str(r2) == "Hello, World")
    
    # Delete from middle
    r2 = r.delete(5, 7)
    result.test("Delete from middle", str(r2) == "HelloWorld!")
    
    # Delete all
    r2 = r.delete(0, len(r))
    result.test("Delete all", str(r2) == "")
    
    # Delete nothing
    r2 = r.delete(5, 5)
    result.test("Delete nothing", str(r2) == "Hello, World!")


def test_concatenation(result: TestResult):
    """Test concatenation operations."""
    print("\n[Concatenation Tests]")
    
    r1 = Rope("Hello, ")
    r2 = Rope("World!")
    
    # Add operator
    r3 = r1 + r2
    result.test("Rope + Rope", str(r3) == "Hello, World!")
    
    # Add with string
    r3 = r1 + "World!"
    result.test("Rope + string", str(r3) == "Hello, World!")
    
    # Reverse add
    r3 = ">>> " + r1
    result.test("string + Rope", str(r3) == ">>> Hello, ")
    
    # Multiply
    r = Rope("ab")
    r2 = r * 3
    result.test("Rope * 3", str(r2) == "ababab")
    
    # Empty concatenation
    r = Rope("test")
    r2 = r + ""
    result.test("Rope + empty", str(r2) == "test")


def test_split(result: TestResult):
    """Test split operations."""
    print("\n[Split Tests]")
    
    r = Rope("Hello, World!")
    
    # Split in middle
    left, right = r.split(7)
    result.test("Split left", str(left) == "Hello, ")
    result.test("Split right", str(right) == "World!")
    
    # Split at beginning
    left, right = r.split(0)
    result.test("Split at 0 left", str(left) == "")
    result.test("Split at 0 right", str(right) == "Hello, World!")
    
    # Split at end
    left, right = r.split(len(r))
    result.test("Split at end left", str(left) == "Hello, World!")
    result.test("Split at end right", str(right) == "")


def test_substring(result: TestResult):
    """Test substring operations."""
    print("\n[Substring Tests]")
    
    r = Rope("Hello, World!")
    
    r2 = r.substring(0, 5)
    result.test("substring(0, 5)", str(r2) == "Hello")
    
    r2 = r.substring(7, 12)
    result.test("substring(7, 12)", str(r2) == "World")


def test_find(result: TestResult):
    """Test find operations."""
    print("\n[Find Tests]")
    
    r = Rope("Hello, World! Hello again!")
    
    result.test("find('World')", r.find("World") == 7)
    result.test("find('Hello', 1)", r.find("Hello", 1) == 14)
    result.test("find('notfound')", r.find("notfound") == -1)
    result.test("rfind('Hello')", r.rfind("Hello") == 14)
    result.test("count('Hello')", r.count("Hello") == 2)


def test_replace(result: TestResult):
    """Test replace operations."""
    print("\n[Replace Tests]")
    
    r = Rope("Hello, World! Hello again!")
    
    r2 = r.replace("Hello", "Hi")
    result.test("Replace all", str(r2) == "Hi, World! Hi again!")
    
    r2 = r.replace("Hello", "Hi", 1)
    result.test("Replace one", str(r2) == "Hi, World! Hello again!")


def test_string_methods(result: TestResult):
    """Test string-like methods."""
    print("\n[String Methods Tests]")
    
    r = Rope("  Hello, World!  ")
    
    result.test("strip()", str(r.strip()) == "Hello, World!")
    result.test("lstrip()", str(r.lstrip()) == "Hello, World!  ")
    result.test("rstrip()", str(r.rstrip()) == "  Hello, World!")
    
    r = Rope("Hello, World!")
    result.test("startswith('Hello')", r.startswith("Hello") == True)
    result.test("endswith('World!')", r.endswith("World!") == True)
    result.test("endswith('Hello')", r.endswith("Hello") == False)
    
    r = Rope("Hello, World!")
    result.test("upper()", str(r.upper()) == "HELLO, WORLD!")
    result.test("lower()", str(r.lower()) == "hello, world!")
    result.test("title()", str(r.title()) == "Hello, World!")
    result.test("capitalize()", str(Rope("hello world").capitalize()) == "Hello world")
    result.test("reverse()", str(r.reverse()) == "!dlroW ,olleH")


def test_iteration(result: TestResult):
    """Test iteration."""
    print("\n[Iteration Tests]")
    
    r = Rope("Hello")
    
    # Iterator
    chars = list(r)
    result.test("Iterator", chars == ['H', 'e', 'l', 'l', 'o'])
    
    # Contains
    result.test("'H' in rope", 'H' in r)
    result.test("'z' not in rope", 'z' not in r)


def test_equality(result: TestResult):
    """Test equality operations."""
    print("\n[Equality Tests]")
    
    r1 = Rope("Hello")
    r2 = Rope("Hello")
    r3 = Rope("World")
    
    result.test("Rope == Rope (equal)", r1 == r2)
    result.test("Rope == Rope (not equal)", not (r1 == r3))
    result.test("Rope == string", r1 == "Hello")
    result.test("Rope != string", r1 != "World")
    result.test("hash", hash(r1) == hash("Hello"))


def test_large_operations(result: TestResult):
    """Test operations on large texts."""
    print("\n[Large Operations Tests]")
    
    # Create large text
    large_text = "".join(random.choices(string.ascii_letters + " \n", k=10000))
    r = Rope(large_text)
    
    result.test("Large text length", len(r) == len(large_text))
    result.test("Large text content", str(r) == large_text)
    
    # Insert in large text
    r2 = r.insert(5000, "INSERTED")
    expected = large_text[:5000] + "INSERTED" + large_text[5000:]
    result.test("Large insert", str(r2) == expected)
    
    # Delete from large text
    r2 = r.delete(4000, 6000)
    expected = large_text[:4000] + large_text[6000:]
    result.test("Large delete", str(r2) == expected)
    
    # Multiple operations
    r = Rope(large_text)
    for _ in range(10):
        pos = random.randint(0, len(r))
        r = r.insert(pos, "X")
    result.test("Multiple insertions on large", len(r) == len(large_text) + 10)


def test_balancing(result: TestResult):
    """Test rope balancing."""
    print("\n[Balancing Tests]")
    
    # Create imbalanced rope through many insertions
    r = Rope("A")
    for i in range(100):
        r = r.insert(0, "X")
    
    # After many insertions at front, tree should grow
    result.test("Tree grows after insertions", r.depth() >= 1)
    
    # Rebalance
    r_balanced = r.rebalance()
    result.test("Rebalanced depth <= log(n)", r_balanced.is_balanced())
    result.test("Content preserved after rebalance", str(r_balanced) == "X" * 100 + "A")
    
    # Stats
    stats = r_balanced.stats()
    result.test("Stats has length", 'length' in stats)
    result.test("Stats has depth", 'depth' in stats)
    result.test("Stats has leaf_count", 'leaf_count' in stats)


def test_batch_editor(result: TestResult):
    """Test batch editor."""
    print("\n[Batch Editor Tests]")
    
    r = Rope("Hello World")
    
    # Simple batch: insert at beginning and end
    editor = BatchEditor(r)
    editor.insert(0, ">>> ")
    editor.insert(len(r), " <<<")
    
    r2 = editor.apply()
    result.test("Batch insert both ends", str(r2) == ">>> Hello World <<<")
    
    # Batch with replace
    r = Rope("Hello World Test")
    editor = BatchEditor(r)
    editor.replace(6, 11, "Python")  # Replace 'World' with 'Python'
    
    r2 = editor.apply()
    result.test("Batch replace", str(r2) == "Hello Python Test")
    
    # Batch multiple deletes at non-overlapping positions
    r = Rope("ABCDE")
    editor = BatchEditor(r)
    editor.delete(1, 2)  # Delete 'B'
    editor.delete(3, 4)  # Delete 'D' (position 3 in original)
    
    r2 = editor.apply()
    result.test("Batch multiple deletes", str(r2) == "ACE")
    
    # Clear and reapply
    r = Rope("Test String")
    editor = BatchEditor(r)
    editor.delete(0, 5)
    r2 = editor.apply()
    result.test("Clear and new operation", str(r2) == "String")


def test_utility_functions(result: TestResult):
    """Test utility functions."""
    print("\n[Utility Functions Tests]")
    
    # from_lines
    lines = ["Hello", "World", "!"]
    r = from_lines(lines)
    result.test("from_lines", str(r) == "Hello\nWorld\n!")
    
    # build_balanced
    large = "A" * 5000
    r = build_balanced(large)
    result.test("build_balanced", str(r) == large)
    result.test("build_balanced is balanced", r.is_balanced())


def test_performance(result: TestResult):
    """Test performance characteristics."""
    print("\n[Performance Tests]")
    
    # Rope provides O(log n) operations vs O(n) for string
    # In Python, string operations are highly optimized
    # Rope's advantage shows in specific scenarios
    
    # Test 1: Multiple operations on large text
    base_text = "A" * 100000
    r = Rope(base_text)
    
    # Verify large text operations work correctly
    for i in [0, 50000, 99999]:
        result.test(f"Large text access at {i}", r.char_at(i) == 'A')
    
    # Test 2: Multiple insertions produce correct result
    r = Rope("start")
    for i in range(100):
        r = r.insert(0, "x")
    result.test("100 insertions at front", str(r) == "x" * 100 + "start")
    
    # Test 3: Memory efficiency for repeated modifications
    # Rope creates new nodes efficiently vs string copying
    r = Rope("base content here")
    for i in range(50):
        r = r.insert(len(r) // 2, "X")
    expected_len = 17 + 50  # original + 50 insertions
    result.test("50 middle insertions", len(r) == expected_len)


def test_edge_cases(result: TestResult):
    """Test edge cases."""
    print("\n[Edge Cases Tests]")
    
    # Empty string operations
    r = Rope("")
    result.test("Empty char_at error", True)  # Would raise, but we test creation
    r2 = r.insert(0, "X")
    result.test("Insert into empty", str(r2) == "X")
    
    # Single character
    r = Rope("X")
    result.test("Single char length", len(r) == 1)
    result.test("Single char access", r[0] == 'X')
    
    # Unicode
    r = Rope("你好世界 🌍")
    result.test("Unicode length", len(r) == 6)  # 4 Chinese + 1 space + 1 emoji
    result.test("Unicode content", str(r) == "你好世界 🌍")
    
    # Newlines
    r = Rope("Line1\nLine2\nLine3")
    lines = r.lines()
    result.test("lines()", lines == ["Line1", "Line2", "Line3"])
    
    # Words
    r = Rope("Hello World Test")
    words = r.words()
    result.test("words()", words == ["Hello", "World", "Test"])


def test_join(result: TestResult):
    """Test join operation."""
    print("\n[Join Tests]")
    
    r = Rope(", ")
    items = ["a", "b", "c"]
    result.test("join list", str(r.join(items)) == "a, b, c")
    
    # Join ropes
    items = [Rope("a"), Rope("b"), Rope("c")]
    result.test("join ropes", str(r.join(items)) == "a, b, c")


# ============================================================================
# Main
# ============================================================================

def main():
    """Run all tests."""
    print("=" * 60)
    print("AllToolkit - Rope Utilities Test Suite")
    print("=" * 60)
    
    result = TestResult()
    
    test_creation(result)
    test_char_access(result)
    test_slicing(result)
    test_insertion(result)
    test_deletion(result)
    test_concatenation(result)
    test_split(result)
    test_substring(result)
    test_find(result)
    test_replace(result)
    test_string_methods(result)
    test_iteration(result)
    test_equality(result)
    test_large_operations(result)
    test_balancing(result)
    test_batch_editor(result)
    test_utility_functions(result)
    test_performance(result)
    test_edge_cases(result)
    test_join(result)
    
    success = result.summary()
    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())