"""
Unit tests for BK-Tree implementation.
"""

import unittest
from bk_tree import (
    BKTree,
    BKTreeNode,
    SpellChecker,
    levenshtein_distance,
    build_tree_from_words,
    find_similar_words
)


class TestLevenshteinDistance(unittest.TestCase):
    """Test cases for Levenshtein distance calculation."""
    
    def test_identical_strings(self):
        """Distance between identical strings should be 0."""
        self.assertEqual(levenshtein_distance("hello", "hello"), 0)
        self.assertEqual(levenshtein_distance("", ""), 0)
        self.assertEqual(levenshtein_distance("a", "a"), 0)
    
    def test_empty_string(self):
        """Distance to empty string should be the length of the other string."""
        self.assertEqual(levenshtein_distance("", "abc"), 3)
        self.assertEqual(levenshtein_distance("abc", ""), 3)
        self.assertEqual(levenshtein_distance("", ""), 0)
    
    def test_single_insertion(self):
        """Single insertion should result in distance 1."""
        self.assertEqual(levenshtein_distance("abc", "ab"), 1)
        self.assertEqual(levenshtein_distance("ab", "abc"), 1)
    
    def test_single_deletion(self):
        """Single deletion should result in distance 1."""
        self.assertEqual(levenshtein_distance("abc", "ac"), 1)
        self.assertEqual(levenshtein_distance("ac", "abc"), 1)
    
    def test_single_substitution(self):
        """Single substitution should result in distance 1."""
        self.assertEqual(levenshtein_distance("abc", "axc"), 1)
        self.assertEqual(levenshtein_distance("cat", "bat"), 1)
    
    def test_multiple_operations(self):
        """Test multiple operations."""
        self.assertEqual(levenshtein_distance("kitten", "sitting"), 3)
        self.assertEqual(levenshtein_distance("saturday", "sunday"), 3)
    
    def test_case_sensitivity(self):
        """Distance should be case sensitive."""
        self.assertEqual(levenshtein_distance("hello", "Hello"), 1)
        self.assertEqual(levenshtein_distance("ABC", "abc"), 3)
    
    def test_unicode(self):
        """Should handle unicode characters."""
        self.assertEqual(levenshtein_distance("café", "cafe"), 1)
        self.assertEqual(levenshtein_distance("日本", "日"), 1)


class TestBKTreeNode(unittest.TestCase):
    """Test cases for BKTreeNode."""
    
    def test_node_creation(self):
        """Test node creation."""
        node = BKTreeNode("test")
        self.assertEqual(node.word, "test")
        self.assertEqual(node.children, {})
    
    def test_node_repr(self):
        """Test node string representation."""
        node = BKTreeNode("test")
        self.assertIn("test", repr(node))


class TestBKTree(unittest.TestCase):
    """Test cases for BKTree."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.tree = BKTree()
    
    def test_empty_tree(self):
        """Test empty tree properties."""
        self.assertEqual(self.tree.size(), 0)
        self.assertTrue(self.tree.is_empty())
        self.assertIsNone(self.tree.root)
        self.assertEqual(self.tree.get_height(), 0)
    
    def test_insert_single_word(self):
        """Test inserting a single word."""
        self.tree.insert("hello")
        self.assertEqual(self.tree.size(), 1)
        self.assertFalse(self.tree.is_empty())
        self.assertIsNotNone(self.tree.root)
        self.assertEqual(self.tree.root.word, "hello")
    
    def test_insert_multiple_words(self):
        """Test inserting multiple words."""
        words = ["apple", "banana", "cherry", "date"]
        for word in words:
            self.tree.insert(word)
        self.assertEqual(self.tree.size(), 4)
    
    def test_insert_duplicate(self):
        """Test inserting duplicate words."""
        self.tree.insert("hello")
        self.tree.insert("hello")
        self.assertEqual(self.tree.size(), 1)
    
    def test_insert_empty_word(self):
        """Test inserting empty word should raise error."""
        with self.assertRaises(ValueError):
            self.tree.insert("")
    
    def test_contains(self):
        """Test contains method."""
        self.tree.insert("hello")
        self.assertTrue(self.tree.contains("hello"))
        self.assertFalse(self.tree.contains("hallo"))
        self.assertFalse(self.tree.contains(""))
    
    def test_contains_operator(self):
        """Test 'in' operator."""
        self.tree.insert("hello")
        self.assertTrue("hello" in self.tree)
        self.assertFalse("hallo" in self.tree)
    
    def test_len_operator(self):
        """Test len operator."""
        self.assertEqual(len(self.tree), 0)
        self.tree.insert("hello")
        self.assertEqual(len(self.tree), 1)
    
    def test_search_empty_tree(self):
        """Test searching empty tree."""
        self.assertEqual(self.tree.search("hello"), [])
    
    def test_search_empty_word(self):
        """Test searching for empty word."""
        self.tree.insert("hello")
        self.assertEqual(self.tree.search(""), [])
    
    def test_search_exact_match(self):
        """Test searching for exact match."""
        self.tree.insert("hello")
        self.assertEqual(self.tree.search("hello", max_distance=0), ["hello"])
    
    def test_search_near_matches(self):
        """Test searching for near matches."""
        words = ["hello", "hallo", "help", "shell", "held"]
        for word in words:
            self.tree.insert(word)
        
        results = self.tree.search("hell", max_distance=1)
        # hell -> hello (add 'o', dist 1)
        # hell -> hallo (replace 'e'->'a', add 'o', dist 2)
        # hell -> help (replace 'l'->'p', dist 1)
        # hell -> shell (add 's', dist 1)
        # hell -> held (replace 'l'->'d', dist 1)
        self.assertIn("hello", results)
        self.assertIn("help", results)
        self.assertIn("shell", results)
        self.assertIn("held", results)
        self.assertNotIn("hallo", results)  # distance is 2
    
    def test_search_max_distance(self):
        """Test search with different max distances."""
        self.tree.insert("hello")
        
        results_dist_0 = self.tree.search("hallo", max_distance=0)
        self.assertEqual(results_dist_0, [])
        
        results_dist_1 = self.tree.search("hallo", max_distance=1)
        self.assertEqual(results_dist_1, ["hello"])
    
    def test_find_nearest(self):
        """Test finding nearest word."""
        words = ["apple", "banana", "cherry"]
        for word in words:
            self.tree.insert(word)
        
        self.assertEqual(self.tree.find_nearest("aple"), "apple")
        self.assertEqual(self.tree.find_nearest("banan"), "banana")
    
    def test_find_nearest_empty_tree(self):
        """Test finding nearest in empty tree."""
        self.assertIsNone(self.tree.find_nearest("hello"))
    
    def test_find_nearest_with_max_distance(self):
        """Test finding nearest with max distance constraint."""
        self.tree.insert("hello")
        
        self.assertEqual(self.tree.find_nearest("hallo", max_distance=1), "hello")
        self.assertIsNone(self.tree.find_nearest("xxxxxxxxx", max_distance=1))
    
    def test_get_all_words(self):
        """Test getting all words from tree."""
        words = {"apple", "banana", "cherry"}
        for word in words:
            self.tree.insert(word)
        
        self.assertEqual(self.tree.get_all_words(), words)
    
    def test_get_height(self):
        """Test getting tree height."""
        self.assertEqual(self.tree.get_height(), 0)
        
        self.tree.insert("hello")
        self.assertEqual(self.tree.get_height(), 1)
        
        # Height increases as we add words at different distances
        self.tree.insert("hallo")  # distance 1 from hello
        self.assertGreaterEqual(self.tree.get_height(), 1)
    
    def test_clear(self):
        """Test clearing tree."""
        self.tree.insert("hello")
        self.tree.insert("world")
        self.assertEqual(self.tree.size(), 2)
        
        self.tree.clear()
        self.assertEqual(self.tree.size(), 0)
        self.assertTrue(self.tree.is_empty())
        self.assertIsNone(self.tree.root)
    
    def test_repr(self):
        """Test string representation."""
        self.tree.insert("hello")
        self.assertIn("size=1", repr(self.tree))


class TestBKTreeCustomDistance(unittest.TestCase):
    """Test BKTree with custom distance function."""
    
    def test_custom_distance_function(self):
        """Test tree with custom distance function."""
        # Use a simple distance: absolute difference of lengths
        def length_distance(s1, s2):
            return abs(len(s1) - len(s2))
        
        tree = BKTree(distance_func=length_distance)
        tree.insert("a")
        tree.insert("ab")
        tree.insert("abc")
        
        # Search for words with length difference of 0
        results = tree.search("ab", max_distance=0)
        self.assertEqual(len(results), 1)
        self.assertIn("ab", results)


class TestSpellChecker(unittest.TestCase):
    """Test cases for SpellChecker."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.checker = SpellChecker(["apple", "banana", "cherry", "python", "programming"])
    
    def test_is_correct(self):
        """Test word correctness check."""
        self.assertTrue(self.checker.is_correct("apple"))
        self.assertTrue(self.checker.is_correct("APPLE"))  # case insensitive
        self.assertFalse(self.checker.is_correct("aple"))
    
    def test_add_word(self):
        """Test adding word to dictionary."""
        self.assertFalse(self.checker.is_correct("orange"))
        self.checker.add_word("orange")
        self.assertTrue(self.checker.is_correct("orange"))
    
    def test_add_words(self):
        """Test adding multiple words."""
        self.checker.add_words(["grape", "mango"])
        self.assertTrue(self.checker.is_correct("grape"))
        self.assertTrue(self.checker.is_correct("mango"))
    
    def test_suggest(self):
        """Test spelling suggestions."""
        suggestions = self.checker.suggest("pythn")
        self.assertIn("python", suggestions)
    
    def test_suggest_with_max_distance(self):
        """Test suggestions with max distance."""
        # Distance of 2 should find more matches
        suggestions_dist_1 = self.checker.suggest("pythn", max_distance=1)
        suggestions_dist_2 = self.checker.suggest("pythn", max_distance=2)
        
        self.assertGreaterEqual(len(suggestions_dist_2), len(suggestions_dist_1))
    
    def test_suggest_with_max_suggestions(self):
        """Test limiting number of suggestions."""
        suggestions = self.checker.suggest("pythn", max_distance=2, max_suggestions=1)
        self.assertLessEqual(len(suggestions), 1)
    
    def test_empty_checker(self):
        """Test empty spell checker."""
        checker = SpellChecker()
        self.assertFalse(checker.is_correct("hello"))
        self.assertEqual(checker.suggest("hello"), [])
    
    def test_repr(self):
        """Test string representation."""
        self.assertIn("words=5", repr(self.checker))


class TestUtilityFunctions(unittest.TestCase):
    """Test utility functions."""
    
    def test_build_tree_from_words(self):
        """Test building tree from word list."""
        words = ["apple", "banana", "cherry"]
        tree = build_tree_from_words(words)
        
        self.assertEqual(tree.size(), 3)
        self.assertTrue(tree.contains("apple"))
        self.assertTrue(tree.contains("banana"))
        self.assertTrue(tree.contains("cherry"))
    
    def test_find_similar_words(self):
        """Test finding similar words."""
        dictionary = ["hello", "hallo", "help", "shell", "world"]
        similar = find_similar_words("hell", dictionary, max_distance=1)
        # hell -> hello (dist 1), hell -> help (dist 1), hell -> shell (dist 1)
        # hell -> hallo (dist 2), so hallo should NOT be in results
        self.assertIn("hello", similar)
        self.assertIn("help", similar)
        self.assertIn("shell", similar)
        self.assertNotIn("hallo", similar)  # distance is 2
        self.assertNotIn("world", similar)  # distance is 4


class TestBKTreePerformance(unittest.TestCase):
    """Performance tests for BKTree."""
    
    def test_large_tree(self):
        """Test with a larger dataset."""
        tree = BKTree()
        
        # Generate words
        words = [f"word{i:05d}" for i in range(1000)]
        for word in words:
            tree.insert(word)
        
        self.assertEqual(tree.size(), 1000)
        
        # Search should still be fast
        results = tree.search("word00001", max_distance=1)
        self.assertGreater(len(results), 0)
    
    def test_search_sorted_by_distance(self):
        """Test that search results are sorted by distance."""
        tree = BKTree()
        tree.insert("aaa")
        tree.insert("aab")  # distance 1 from "aaa"
        tree.insert("abb")  # distance 2 from "aaa"
        tree.insert("abc")  # distance 3 from "aaa"
        
        results = tree.search("aaa", max_distance=3)
        
        # Results should be sorted by distance
        # aaa (dist 0), aab (dist 1), abb (dist 2), abc (dist 3)
        self.assertEqual(results, ["aaa", "aab", "abb", "abc"])


class TestEdgeCases(unittest.TestCase):
    """Test edge cases."""
    
    def test_single_character_words(self):
        """Test with single character words."""
        tree = BKTree()
        tree.insert("a")
        tree.insert("b")
        tree.insert("c")
        
        self.assertEqual(tree.size(), 3)
        self.assertTrue(tree.contains("a"))
        
        results = tree.search("a", max_distance=1)
        self.assertIn("a", results)
        self.assertIn("b", results)
        self.assertIn("c", results)
    
    def test_very_long_words(self):
        """Test with very long words."""
        tree = BKTree()
        long_word = "a" * 1000
        long_word2 = "a" * 999 + "b"
        
        tree.insert(long_word)
        tree.insert(long_word2)
        
        self.assertEqual(tree.size(), 2)
        self.assertTrue(tree.contains(long_word))
    
    def test_special_characters(self):
        """Test with special characters."""
        tree = BKTree()
        words = ["hello!", "hello?", "hello.", "hello-world"]
        
        for word in words:
            tree.insert(word)
        
        self.assertEqual(tree.size(), 4)
        results = tree.search("hello!", max_distance=1)
        self.assertIn("hello!", results)


if __name__ == "__main__":
    unittest.main(verbosity=2)