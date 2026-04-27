#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AllToolkit - Aho-Corasick Utilities Test Suite
===============================================
Comprehensive tests for the Aho-Corasick string matching implementation.
"""

import unittest
import tempfile
import os
import sys

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from mod import (
    AhoCorasick,
    Match,
    SensitiveWordFilter,
    WildcardAhoCorasick,
    MultiPatternReplacer,
    build_automaton,
    find_all,
    contains_any,
    replace_patterns,
    highlight_patterns
)


class TestMatch(unittest.TestCase):
    """Test the Match dataclass."""
    
    def test_match_creation(self):
        """Test match creation with all attributes."""
        match = Match(0, 5, "hello", value=42)
        self.assertEqual(match.start, 0)
        self.assertEqual(match.end, 5)
        self.assertEqual(match.pattern, "hello")
        self.assertEqual(match.value, 42)
    
    def test_match_length(self):
        """Test match length calculation."""
        match = Match(0, 5, "hello")
        self.assertEqual(len(match), 5)
        self.assertEqual(match.length, 5)
    
    def test_match_equality(self):
        """Test match equality comparison."""
        m1 = Match(0, 5, "hello")
        m2 = Match(0, 5, "hello")
        m3 = Match(0, 5, "world")
        self.assertEqual(m1, m2)
        self.assertNotEqual(m1, m3)
    
    def test_match_hash(self):
        """Test match hashing for set operations."""
        m1 = Match(0, 5, "hello")
        m2 = Match(0, 5, "hello")
        matches = {m1, m2}
        self.assertEqual(len(matches), 1)
    
    def test_match_repr(self):
        """Test match string representation."""
        match = Match(0, 5, "hello")
        self.assertIn("hello", repr(match))
        self.assertIn("0", repr(match))
        self.assertIn("5", repr(match))


class TestAhoCorasickBasic(unittest.TestCase):
    """Basic functionality tests for AhoCorasick."""
    
    def test_empty_automaton(self):
        """Test automaton with no patterns."""
        ac = AhoCorasick()
        self.assertEqual(ac.findall("hello world"), [])
        self.assertFalse(ac.contains("hello"))
    
    def test_single_pattern(self):
        """Test automaton with single pattern."""
        ac = AhoCorasick(["hello"])
        matches = ac.findall("hello world hello")
        self.assertEqual(len(matches), 2)
        self.assertEqual(matches[0].pattern, "hello")
        self.assertEqual(matches[1].pattern, "hello")
    
    def test_multiple_patterns(self):
        """Test automaton with multiple patterns."""
        ac = AhoCorasick(["he", "she", "his", "hers"])
        matches = ac.findall("ushers")
        
        # Should find: 'she' at [1:4], 'he' at [2:4], 'hers' at [2:6]
        patterns_found = [m.pattern for m in matches]
        self.assertIn("she", patterns_found)
        self.assertIn("he", patterns_found)
        self.assertIn("hers", patterns_found)
    
    def test_overlapping_patterns(self):
        """Test overlapping pattern detection."""
        ac = AhoCorasick(["abc", "bc", "c"])
        matches = ac.findall("abc")
        
        self.assertEqual(len(matches), 3)
        patterns = [m.pattern for m in matches]
        self.assertIn("abc", patterns)
        self.assertIn("bc", patterns)
        self.assertIn("c", patterns)
    
    def test_pattern_not_found(self):
        """Test when pattern is not in text."""
        ac = AhoCorasick(["xyz"])
        matches = ac.findall("hello world")
        self.assertEqual(len(matches), 0)
    
    def test_empty_text(self):
        """Test searching empty text."""
        ac = AhoCorasick(["hello"])
        matches = ac.findall("")
        self.assertEqual(len(matches), 0)
    
    def test_empty_pattern(self):
        """Test adding empty pattern."""
        ac = AhoCorasick()
        ac.add_pattern("")  # Should be ignored
        self.assertEqual(len(ac), 0)


class TestAhoCorasickCaseSensitivity(unittest.TestCase):
    """Test case sensitivity handling."""
    
    def test_case_sensitive_default(self):
        """Test default case sensitivity."""
        ac = AhoCorasick(["Hello"])
        matches = ac.findall("hello HELLO Hello")
        
        # Only exact case match
        self.assertEqual(len(matches), 1)
        self.assertEqual(matches[0].pattern, "Hello")
    
    def test_case_insensitive(self):
        """Test case insensitive matching."""
        ac = AhoCorasick(["hello"], case_sensitive=False)
        matches = ac.findall("HELLO hello HeLLo")
        
        self.assertEqual(len(matches), 3)
    
    def test_case_insensitive_patterns(self):
        """Test case insensitive with multiple patterns."""
        ac = AhoCorasick(["hello", "world"], case_sensitive=False)
        matches = ac.findall("HELLO World")
        
        self.assertEqual(len(matches), 2)


class TestAhoCorasickMethods(unittest.TestCase):
    """Test various methods of AhoCorasick."""
    
    def test_finditer(self):
        """Test iterator-based finding."""
        ac = AhoCorasick(["a", "b", "c"])
        matches = list(ac.finditer("abc"))
        self.assertEqual(len(matches), 3)
    
    def test_search(self):
        """Test finding first match."""
        ac = AhoCorasick(["world", "hello"])
        match = ac.search("say hello world")
        
        self.assertIsNotNone(match)
        self.assertEqual(match.pattern, "hello")
    
    def test_search_no_match(self):
        """Test search with no matches."""
        ac = AhoCorasick(["xyz"])
        match = ac.search("hello world")
        self.assertIsNone(match)
    
    def test_count(self):
        """Test match counting."""
        ac = AhoCorasick(["a", "aa"])
        count = ac.count("aaaa")
        # 'a' matches 4 times, 'aa' matches 3 times
        self.assertEqual(count, 7)
    
    def test_count_unique(self):
        """Test unique match counting."""
        ac = AhoCorasick(["a", "b"])
        count = ac.count("a b a b a", unique=True)
        # 'a' at positions 0, 4, 8; 'b' at positions 2, 6 = 5 unique matches
        self.assertEqual(count, 5)
    
    def test_contains(self):
        """Test contains method."""
        ac = AhoCorasick(["hello", "world"])
        self.assertTrue(ac.contains("say hello"))
        self.assertTrue(ac.contains("world here"))
        self.assertFalse(ac.contains("no match"))


class TestAhoCorasickReplace(unittest.TestCase):
    """Test replacement functionality."""
    
    def test_replace_basic(self):
        """Test basic replacement."""
        ac = AhoCorasick(["bad", "evil"])
        result = ac.replace("this is bad and evil", "good")
        self.assertEqual(result, "this is good and good")
    
    def test_replace_with_callable(self):
        """Test replacement with callable."""
        ac = AhoCorasick(["cat", "dog"])
        result = ac.replace("cat and dog", lambda m: m.pattern.upper())
        self.assertEqual(result, "CAT and DOG")
    
    def test_replace_different_lengths(self):
        """Test replacement with different length strings."""
        ac = AhoCorasick(["foo"])
        result = ac.replace("foo bar foo", "foobar")
        self.assertEqual(result, "foobar bar foobar")
    
    def test_replace_empty_text(self):
        """Test replacement in empty text."""
        ac = AhoCorasick(["hello"])
        result = ac.replace("", "world")
        self.assertEqual(result, "")


class TestAhoCorasickHighlight(unittest.TestCase):
    """Test highlighting functionality."""
    
    def test_highlight_basic(self):
        """Test basic highlighting."""
        ac = AhoCorasick(["hello"])
        result = ac.highlight("hello world")
        self.assertEqual(result, "<mark>hello</mark> world")
    
    def test_highlight_custom_markers(self):
        """Test highlighting with custom markers."""
        ac = AhoCorasick(["test"])
        result = ac.highlight("this is a test", "[", "]")
        self.assertEqual(result, "this is a [test]")
    
    def test_highlight_multiple_matches(self):
        """Test highlighting multiple matches."""
        ac = AhoCorasick(["a"])
        result = ac.highlight("a b a")
        self.assertEqual(result, "<mark>a</mark> b <mark>a</mark>")


class TestAhoCorasickExtract(unittest.TestCase):
    """Test extraction functionality."""
    
    def test_extract(self):
        """Test pattern extraction."""
        ac = AhoCorasick(["cat", "dog", "bird"])
        found = ac.extract("I have a cat, a dog, and another cat")
        
        self.assertEqual(len(found), 3)
        self.assertIn("cat", found)
        self.assertIn("dog", found)
    
    def test_extract_unique(self):
        """Test unique pattern extraction."""
        ac = AhoCorasick(["cat", "dog"])
        found = ac.extract_unique("cat cat dog dog cat")
        
        self.assertEqual(found, {"cat", "dog"})
    
    def test_get_pattern_positions(self):
        """Test getting pattern positions."""
        ac = AhoCorasick(["ab", "bc"])
        positions = ac.get_pattern_positions("abc")
        
        self.assertIn("ab", positions)
        self.assertIn("bc", positions)
        self.assertEqual(positions["ab"], [(0, 2)])
        self.assertEqual(positions["bc"], [(1, 3)])


class TestAhoCorasickPatternManagement(unittest.TestCase):
    """Test pattern management methods."""
    
    def test_add_pattern(self):
        """Test adding patterns incrementally."""
        ac = AhoCorasick()
        ac.add_pattern("hello")
        ac.add_pattern("world")
        
        self.assertEqual(len(ac), 2)
        self.assertIn("hello", ac)
        self.assertIn("world", ac)
    
    def test_add_patterns(self):
        """Test adding multiple patterns."""
        ac = AhoCorasick()
        ac.add_patterns(["a", "b", "c"])
        
        self.assertEqual(len(ac), 3)
    
    def test_add_pattern_with_value(self):
        """Test adding pattern with associated value."""
        ac = AhoCorasick()
        ac.add_pattern("hello", value="greeting")
        
        matches = ac.findall("hello")
        self.assertEqual(len(matches), 1)
        self.assertEqual(matches[0].value, "greeting")
    
    def test_remove_pattern(self):
        """Test pattern removal."""
        ac = AhoCorasick(["hello", "world"])
        
        result = ac.remove_pattern("hello")
        self.assertTrue(result)
        self.assertEqual(len(ac), 1)
        self.assertNotIn("hello", ac)
        
        matches = ac.findall("hello world")
        self.assertEqual(len(matches), 1)
        self.assertEqual(matches[0].pattern, "world")
    
    def test_remove_nonexistent_pattern(self):
        """Test removing pattern that doesn't exist."""
        ac = AhoCorasick(["hello"])
        result = ac.remove_pattern("nonexistent")
        self.assertFalse(result)
    
    def test_pattern_count(self):
        """Test pattern count property."""
        ac = AhoCorasick(["a", "b", "c"])
        self.assertEqual(ac.pattern_count, 3)
    
    def test_patterns_property(self):
        """Test patterns property."""
        ac = AhoCorasick(["a", "b"])
        patterns = ac.patterns
        self.assertEqual(patterns, {"a", "b"})


class TestAhoCorasickSerialization(unittest.TestCase):
    """Test serialization functionality."""
    
    def test_to_dict(self):
        """Test conversion to dictionary."""
        ac = AhoCorasick(["hello", "world"], case_sensitive=False)
        data = ac.to_dict()
        
        self.assertIn("patterns", data)
        self.assertIn("case_sensitive", data)
        self.assertEqual(set(data["patterns"]), {"hello", "world"})
        self.assertFalse(data["case_sensitive"])
    
    def test_from_dict(self):
        """Test creation from dictionary."""
        data = {
            "patterns": ["hello", "world"],
            "case_sensitive": True
        }
        ac = AhoCorasick.from_dict(data)
        
        self.assertEqual(len(ac), 2)
        self.assertTrue(ac.contains("hello world"))
    
    def test_to_json(self):
        """Test JSON serialization."""
        ac = AhoCorasick(["test"])
        json_str = ac.to_json()
        
        self.assertIn("test", json_str)
        self.assertIn("patterns", json_str)
    
    def test_from_json(self):
        """Test JSON deserialization."""
        ac1 = AhoCorasick(["hello", "world"], case_sensitive=False)
        json_str = ac1.to_json()
        
        ac2 = AhoCorasick.from_json(json_str)
        self.assertEqual(len(ac2), 2)
        matches = ac2.findall("HELLO")
        self.assertEqual(len(matches), 1)
        self.assertEqual(matches[0].pattern, "hello")
    
    def test_save_load_file(self):
        """Test saving and loading from file."""
        ac1 = AhoCorasick(["hello", "world"])
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            temp_path = f.name
        
        try:
            ac1.save(temp_path)
            ac2 = AhoCorasick.load(temp_path)
            
            self.assertEqual(len(ac2), 2)
            self.assertTrue(ac2.contains("hello"))
        finally:
            os.unlink(temp_path)


class TestSensitiveWordFilter(unittest.TestCase):
    """Test SensitiveWordFilter class."""
    
    def test_basic_filtering(self):
        """Test basic word filtering."""
        sf = SensitiveWordFilter(["bad", "evil"])
        
        self.assertTrue(sf.check("this is bad"))
        self.assertTrue(sf.check("evil content"))
        self.assertFalse(sf.check("good content"))
    
    def test_clean(self):
        """Test word replacement."""
        sf = SensitiveWordFilter(["bad", "evil"])
        result = sf.clean("this is bad and evil")
        self.assertEqual(result, "this is *** and ***")
    
    def test_custom_replacement(self):
        """Test custom replacement."""
        sf = SensitiveWordFilter(["bad"])
        result = sf.clean("bad word", replacement="#")
        self.assertEqual(result, "# word")
    
    def test_case_insensitive_default(self):
        """Test case insensitive by default."""
        sf = SensitiveWordFilter(["bad"])
        self.assertTrue(sf.check("BAD"))
        self.assertTrue(sf.check("Bad"))
    
    def test_find_words(self):
        """Test finding sensitive words."""
        sf = SensitiveWordFilter(["bad", "evil", "spam"])
        found = sf.find("bad and evil content")
        self.assertEqual(found, {"bad", "evil"})
    
    def test_highlight(self):
        """Test highlighting."""
        sf = SensitiveWordFilter(["bad"])
        result = sf.highlight("bad word")
        self.assertEqual(result, "<mark>bad</mark> word")
    
    def test_add_remove_words(self):
        """Test adding and removing words."""
        sf = SensitiveWordFilter()
        sf.add_word("test")
        
        self.assertTrue(sf.check("test"))
        self.assertEqual(len(sf), 1)
        
        sf.remove_word("test")
        self.assertFalse(sf.check("test"))


class TestMultiPatternReplacer(unittest.TestCase):
    """Test MultiPatternReplacer class."""
    
    def test_basic_replacement(self):
        """Test basic multi-pattern replacement."""
        replacer = MultiPatternReplacer()
        replacer.add("foo", "bar")
        replacer.add("hello", "hi")
        
        result = replacer.replace("foo says hello")
        self.assertEqual(result, "bar says hi")
    
    def test_different_replacements(self):
        """Test different replacements for different patterns."""
        replacer = MultiPatternReplacer()
        replacer.add("cat", "dog")
        replacer.add("black", "white")
        
        result = replacer.replace("black cat")
        self.assertEqual(result, "white dog")
    
    def test_add_many(self):
        """Test adding multiple patterns at once."""
        replacer = MultiPatternReplacer()
        replacer.add_many([("a", "1"), ("b", "2"), ("c", "3")])
        
        result = replacer.replace("a b c")
        self.assertEqual(result, "1 2 3")
    
    def test_empty_replacer(self):
        """Test empty replacer."""
        replacer = MultiPatternReplacer()
        result = replacer.replace("hello world")
        self.assertEqual(result, "hello world")


class TestWildcardAhoCorasick(unittest.TestCase):
    """Test WildcardAhoCorasick class."""
    
    def test_wildcard_pattern(self):
        """Test wildcard pattern matching."""
        wac = WildcardAhoCorasick(['c?t'])
        matches = wac.findall("cat cut")
        
        self.assertGreater(len(matches), 0)
    
    def test_multiple_wildcards(self):
        """Test pattern with multiple wildcards."""
        wac = WildcardAhoCorasick(['a?c'])
        matches = wac.findall("abc adc")
        self.assertGreater(len(matches), 0)


class TestConvenienceFunctions(unittest.TestCase):
    """Test convenience functions."""
    
    def test_build_automaton(self):
        """Test build_automaton function."""
        ac = build_automaton(["hello", "world"])
        self.assertTrue(ac.contains("hello world"))
    
    def test_find_all(self):
        """Test find_all function."""
        matches = find_all(["a", "b"], "a b c a b")
        self.assertEqual(len(matches), 4)
    
    def test_contains_any(self):
        """Test contains_any function."""
        self.assertTrue(contains_any(["hello"], "hello world"))
        self.assertFalse(contains_any(["xyz"], "hello world"))
    
    def test_replace_patterns(self):
        """Test replace_patterns function."""
        result = replace_patterns(["bad"], "bad word", "good")
        self.assertEqual(result, "good word")
    
    def test_highlight_patterns(self):
        """Test highlight_patterns function."""
        result = highlight_patterns(["test"], "test case")
        self.assertEqual(result, "<mark>test</mark> case")


class TestEdgeCases(unittest.TestCase):
    """Test edge cases and special scenarios."""
    
    def test_unicode_patterns(self):
        """Test Unicode pattern matching."""
        ac = AhoCorasick(["你好", "世界"])
        matches = ac.findall("你好世界")
        
        self.assertEqual(len(matches), 2)
    
    def test_overlapping_at_start(self):
        """Test patterns that overlap at start."""
        ac = AhoCorasick(["a", "ab", "abc"])
        matches = ac.findall("abc")
        
        self.assertEqual(len(matches), 3)
    
    def test_long_pattern(self):
        """Test with very long pattern."""
        long_pattern = "a" * 1000
        ac = AhoCorasick([long_pattern])
        
        text = "b" * 500 + long_pattern + "b" * 500
        matches = ac.findall(text)
        
        self.assertEqual(len(matches), 1)
        self.assertEqual(matches[0].pattern, long_pattern)
    
    def test_many_patterns(self):
        """Test with many patterns."""
        patterns = [f"pattern{i}" for i in range(100)]
        ac = AhoCorasick(patterns)
        
        self.assertEqual(len(ac), 100)
        self.assertTrue(ac.contains("pattern50"))
    
    def test_special_characters(self):
        """Test patterns with special characters."""
        ac = AhoCorasick(["a.b", "c*d", "e+f"])
        matches = ac.findall("a.b c*d e+f")
        
        self.assertEqual(len(matches), 3)
    
    def test_whitespace_patterns(self):
        """Test patterns containing whitespace."""
        ac = AhoCorasick(["hello world", "foo bar"])
        matches = ac.findall("hello world foo bar")
        
        self.assertEqual(len(matches), 2)
    
    def test_duplicate_patterns(self):
        """Test adding duplicate patterns."""
        ac = AhoCorasick()
        ac.add_pattern("test")
        ac.add_pattern("test")  # Duplicate
        
        self.assertEqual(len(ac), 1)
        matches = ac.findall("test")
        self.assertEqual(len(matches), 1)
    
    def test_pattern_contained_in_another(self):
        """Test patterns where one is contained in another."""
        ac = AhoCorasick(["a", "aa", "aaa"])
        matches = ac.findall("aaa")
        
        # Should match all three: 'a' at positions 0, 1, 2; 'aa' at 0-1, 1-2; 'aaa' at 0-2
        self.assertEqual(len(matches), 6)
    
    def test_single_character_patterns(self):
        """Test single character patterns."""
        ac = AhoCorasick(["a", "b", "c"])
        matches = ac.findall("abcabc")
        
        self.assertEqual(len(matches), 6)


class TestPerformance(unittest.TestCase):
    """Performance-related tests."""
    
    def test_large_text_search(self):
        """Test searching in large text."""
        import time
        
        patterns = ["pattern1", "pattern2", "pattern3"]
        ac = AhoCorasick(patterns)
        
        # Generate large text
        text = "some text " * 10000 + "pattern2" + " more text " * 1000
        
        start = time.time()
        matches = ac.findall(text)
        elapsed = time.time() - start
        
        self.assertGreater(len(matches), 0)
        self.assertLess(elapsed, 1.0)  # Should complete in under 1 second
    
    def test_rebuild_after_removal(self):
        """Test that removal triggers proper rebuild."""
        ac = AhoCorasick(["a", "b", "c"])
        ac.remove_pattern("b")
        
        # Should still work correctly
        matches = ac.findall("abc")
        patterns = {m.pattern for m in matches}
        
        self.assertEqual(patterns, {"a", "c"})


if __name__ == '__main__':
    unittest.main(verbosity=2)