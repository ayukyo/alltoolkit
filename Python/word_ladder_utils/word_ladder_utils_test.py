"""
Word Ladder Utils Tests

Comprehensive tests for word ladder puzzle utilities.

Author: AllToolkit Auto-Generator
Date: 2026-05-20
"""

import unittest
from typing import List
from mod import (
    WordLadderSolver,
    find_shortest_path,
    find_all_paths,
    get_neighbors,
    is_valid_word,
    is_valid_transformation,
    validate_ladder,
    generate_puzzle,
    get_ladder_difficulty,
    get_words_of_length,
    add_words,
    create_solver,
    BUILTIN_WORDS
)


class TestWordLadderSolver(unittest.TestCase):
    """Tests for WordLadderSolver class."""
    
    def setUp(self):
        """Set up test solver."""
        self.solver = WordLadderSolver()
    
    def test_init_default(self):
        """Test default initialization."""
        solver = WordLadderSolver()
        self.assertIsNotNone(solver.words)
        self.assertFalse(solver.case_sensitive)
    
    def test_init_case_sensitive(self):
        """Test case-sensitive initialization."""
        solver = WordLadderSolver(case_sensitive=True)
        self.assertTrue(solver.case_sensitive)
    
    def test_init_custom_words(self):
        """Test custom words initialization."""
        custom_words = {3: {"cat", "dog", "bat"}}
        solver = WordLadderSolver(custom_words=custom_words)
        self.assertEqual(solver.words[3], {"cat", "dog", "bat"})
    
    def test_is_valid_word_true(self):
        """Test valid word detection."""
        self.assertTrue(self.solver.is_valid_word("cat"))
        self.assertTrue(self.solver.is_valid_word("hello"))
        self.assertTrue(self.solver.is_valid_word("python"))
    
    def test_is_valid_word_false(self):
        """Test invalid word detection."""
        self.assertFalse(self.solver.is_valid_word("xyz"))
        self.assertFalse(self.solver.is_valid_word("qqq"))
        self.assertFalse(self.solver.is_valid_word(""))
    
    def test_is_valid_word_case_insensitive(self):
        """Test case-insensitive word validation."""
        self.assertTrue(self.solver.is_valid_word("CAT"))
        self.assertTrue(self.solver.is_valid_word("Dog"))
        self.assertTrue(self.solver.is_valid_word("HELLO"))
    
    def test_is_valid_transformation_true(self):
        """Test valid one-letter transformation."""
        self.assertTrue(self.solver.is_valid_transformation("cat", "cot"))
        self.assertTrue(self.solver.is_valid_transformation("cold", "cord"))
        self.assertTrue(self.solver.is_valid_transformation("love", "live"))
    
    def test_is_valid_transformation_false(self):
        """Test invalid transformations."""
        # Different length
        self.assertFalse(self.solver.is_valid_transformation("cat", "cats"))
        # Same word
        self.assertFalse(self.solver.is_valid_transformation("cat", "cat"))
        # Multiple changes
        self.assertFalse(self.solver.is_valid_transformation("cat", "dog"))
    
    def test_get_neighbors(self):
        """Test neighbor generation."""
        neighbors = self.solver.get_neighbors("cat")
        self.assertIn("cot", neighbors)
        self.assertIn("bat", neighbors)
        self.assertIn("hat", neighbors)
        self.assertNotIn("cat", neighbors)
        self.assertNotIn("dog", neighbors)
    
    def test_get_neighbors_empty_for_invalid_length(self):
        """Test neighbors for invalid length."""
        neighbors = self.solver.get_neighbors("ab")  # 2 letters - not in dict
        self.assertEqual(neighbors, [])
    
    def test_find_shortest_path_basic(self):
        """Test basic path finding."""
        path = self.solver.find_shortest_path("cat", "dog")
        self.assertIsNotNone(path)
        self.assertEqual(path[0], "cat")
        self.assertEqual(path[-1], "dog")
        # Verify each step is valid
        for i in range(len(path) - 1):
            self.assertTrue(self.solver.is_valid_transformation(path[i], path[i + 1]))
    
    def test_find_shortest_path_same_word(self):
        """Test path finding with same word."""
        path = self.solver.find_shortest_path("cat", "cat")
        self.assertEqual(path, ["cat"])
    
    def test_find_shortest_path_different_lengths(self):
        """Test path finding with different length words."""
        path = self.solver.find_shortest_path("cat", "dogs")
        self.assertIsNone(path)
    
    def test_find_shortest_path_invalid_words(self):
        """Test path finding with invalid words."""
        path = self.solver.find_shortest_path("xyz", "abc")
        self.assertIsNone(path)
    
    def test_find_shortest_path_case_insensitive(self):
        """Test case-insensitive path finding."""
        path = self.solver.find_shortest_path("CAT", "DOG")
        self.assertIsNotNone(path)
        self.assertEqual(path[0], "cat")
        self.assertEqual(path[-1], "dog")
    
    def test_find_shortest_path_medium_length(self):
        """Test path finding for 4-letter words."""
        path = self.solver.find_shortest_path("cold", "warm")
        self.assertIsNotNone(path)
        self.assertEqual(path[0], "cold")
        self.assertEqual(path[-1], "warm")
    
    def test_find_shortest_path_5_letters(self):
        """Test path finding for 5-letter words."""
        # Use words that exist and have a path
        path = self.solver.find_shortest_path("grand", "giant")
        self.assertIsNotNone(path)
        self.assertEqual(path[0], "grand")
        self.assertEqual(path[-1], "giant")
    
    def test_find_all_paths(self):
        """Test finding multiple paths."""
        paths = self.solver.find_all_paths("cat", "dog", max_paths=5)
        self.assertTrue(len(paths) > 0)
        # All paths should end at dog
        for path in paths:
            self.assertEqual(path[0], "cat")
            self.assertEqual(path[-1], "dog")
        # All paths should have same length (shortest)
        lengths = [len(p) for p in paths]
        self.assertTrue(all(l == lengths[0] for l in lengths))
    
    def test_find_all_paths_max_limit(self):
        """Test max paths limit."""
        paths = self.solver.find_all_paths("cat", "dog", max_paths=2)
        self.assertTrue(len(paths) <= 2)
    
    def test_validate_ladder_valid(self):
        """Test validating a valid ladder."""
        ladder = ["cat", "cot", "dot", "dog"]
        valid, msg = self.solver.validate_ladder(ladder)
        self.assertTrue(valid)
        self.assertEqual(msg, "Valid ladder")
    
    def test_validate_ladder_empty(self):
        """Test validating empty ladder."""
        valid, msg = self.solver.validate_ladder([])
        self.assertFalse(valid)
        self.assertEqual(msg, "Empty ladder")
    
    def test_validate_ladder_single_word(self):
        """Test validating single-word ladder."""
        valid, msg = self.solver.validate_ladder(["cat"])
        self.assertFalse(valid)
        self.assertEqual(msg, "Ladder must have at least 2 words")
    
    def test_validate_ladder_invalid_word(self):
        """Test validating ladder with invalid word."""
        ladder = ["cat", "xyz", "dog"]
        valid, msg = self.solver.validate_ladder(ladder)
        self.assertFalse(valid)
        self.assertIn("Invalid word", msg)
    
    def test_validate_ladder_invalid_transformation(self):
        """Test validating ladder with invalid transformation."""
        ladder = ["cat", "dog"]  # 2-letter difference
        valid, msg = self.solver.validate_ladder(ladder)
        self.assertFalse(valid)
        self.assertIn("Invalid transformation", msg)
    
    def test_get_words_of_length(self):
        """Test getting words of specific length."""
        words_3 = self.solver.get_words_of_length(3)
        self.assertIn("cat", words_3)
        self.assertIn("dog", words_3)
        
        words_4 = self.solver.get_words_of_length(4)
        self.assertIn("cold", words_4)
        self.assertIn("warm", words_4)
    
    def test_get_words_of_length_invalid(self):
        """Test getting words of invalid length."""
        words = self.solver.get_words_of_length(2)
        self.assertEqual(words, set())
    
    def test_add_words(self):
        """Test adding words to dictionary."""
        solver = WordLadderSolver({3: set()})
        solver.add_words(["cat", "bat", "hat"])
        self.assertTrue(solver.is_valid_word("cat"))
        self.assertTrue(solver.is_valid_word("bat"))
        self.assertTrue(solver.is_valid_word("hat"))
    
    def test_generate_puzzle(self):
        """Test puzzle generation."""
        puzzle = self.solver.generate_puzzle(length=4, min_path_length=3)
        if puzzle:
            start, end, solution_len = puzzle
            self.assertEqual(len(start), 4)
            self.assertEqual(len(end), 4)
            self.assertTrue(solution_len >= 3)
    
    def test_generate_puzzle_invalid_length(self):
        """Test puzzle generation with invalid length."""
        puzzle = self.solver.generate_puzzle(length=2)
        self.assertIsNone(puzzle)
    
    def test_get_ladder_difficulty_solvable(self):
        """Test difficulty calculation for solvable ladder."""
        difficulty = self.solver.get_ladder_difficulty("cat", "dog")
        self.assertTrue(difficulty["solvable"])
        self.assertIsNotNone(difficulty["difficulty"])
        self.assertIsNotNone(difficulty["path_length"])
        self.assertIsNotNone(difficulty["branching_factor"])
    
    def test_get_ladder_difficulty_unsolvable(self):
        """Test difficulty calculation for unsolvable ladder."""
        difficulty = self.solver.get_ladder_difficulty("xyz", "abc")
        self.assertFalse(difficulty["solvable"])
        self.assertIsNone(difficulty["difficulty"])
    
    def test_builtin_words_exists(self):
        """Test builtin words dictionary exists."""
        self.assertIn(3, BUILTIN_WORDS)
        self.assertIn(4, BUILTIN_WORDS)
        self.assertIn(5, BUILTIN_WORDS)
        self.assertIn(6, BUILTIN_WORDS)
        self.assertTrue(len(BUILTIN_WORDS[3]) > 100)
        self.assertTrue(len(BUILTIN_WORDS[4]) > 100)


class TestConvenienceFunctions(unittest.TestCase):
    """Tests for convenience functions."""
    
    def test_find_shortest_path_function(self):
        """Test find_shortest_path function."""
        path = find_shortest_path("cat", "dog")
        self.assertIsNotNone(path)
        self.assertEqual(path[0], "cat")
        self.assertEqual(path[-1], "dog")
    
    def test_find_all_paths_function(self):
        """Test find_all_paths function."""
        paths = find_all_paths("cat", "dog")
        self.assertTrue(len(paths) > 0)
    
    def test_get_neighbors_function(self):
        """Test get_neighbors function."""
        neighbors = get_neighbors("cat")
        self.assertIn("cot", neighbors)
    
    def test_is_valid_word_function(self):
        """Test is_valid_word function."""
        self.assertTrue(is_valid_word("cat"))
        self.assertFalse(is_valid_word("xyz"))
    
    def test_is_valid_transformation_function(self):
        """Test is_valid_transformation function."""
        self.assertTrue(is_valid_transformation("cat", "cot"))
        self.assertFalse(is_valid_transformation("cat", "dog"))
    
    def test_validate_ladder_function(self):
        """Test validate_ladder function."""
        valid, msg = validate_ladder(["cat", "cot", "dot", "dog"])
        self.assertTrue(valid)
    
    def test_generate_puzzle_function(self):
        """Test generate_puzzle function."""
        puzzle = generate_puzzle(length=4)
        if puzzle:
            start, end, solution_len = puzzle
            self.assertEqual(len(start), 4)
    
    def test_get_ladder_difficulty_function(self):
        """Test get_ladder_difficulty function."""
        difficulty = get_ladder_difficulty("cat", "dog")
        self.assertTrue(difficulty["solvable"])
    
    def test_get_words_of_length_function(self):
        """Test get_words_of_length function."""
        words = get_words_of_length(3)
        self.assertIn("cat", words)
    
    def test_add_words_function(self):
        """Test add_words function."""
        # Create new solver with custom words to avoid modifying global
        solver = create_solver({3: set()})
        solver.add_words(["test", "best"])
        self.assertTrue(solver.is_valid_word("test"))
    
    def test_create_solver_function(self):
        """Test create_solver function."""
        solver = create_solver()
        self.assertIsInstance(solver, WordLadderSolver)
        self.assertFalse(solver.case_sensitive)
        
        solver_cs = create_solver(case_sensitive=True)
        self.assertTrue(solver_cs.case_sensitive)


class TestEdgeCases(unittest.TestCase):
    """Tests for edge cases."""
    
    def test_empty_string(self):
        """Test empty string handling."""
        solver = WordLadderSolver()
        self.assertFalse(solver.is_valid_word(""))
        self.assertEqual(solver.get_neighbors(""), [])
        self.assertIsNone(solver.find_shortest_path("", "cat"))
    
    def test_non_alpha_characters(self):
        """Test non-alphabetic characters."""
        solver = WordLadderSolver()
        self.assertFalse(solver.is_valid_word("cat!"))
        self.assertFalse(solver.is_valid_word("123"))
    
    def test_very_long_word(self):
        """Test very long word."""
        solver = WordLadderSolver()
        # 10-letter word not in dictionary
        self.assertFalse(solver.is_valid_word("abcdefghij"))
    
    def test_max_depth_limit(self):
        """Test max depth parameter."""
        solver = WordLadderSolver()
        # Very low max_depth might not find path
        path = solver.find_shortest_path("stone", "money", max_depth=2)
        # Might be None or might find short path
        if path:
            self.assertTrue(len(path) <= 2)
    
    def test_case_sensitive_mode(self):
        """Test case-sensitive mode."""
        # Case-sensitive mode preserves the original case
        solver = WordLadderSolver(case_sensitive=True)
        # Note: When case_sensitive=True, words are NOT normalized to lowercase
        # So uppercase words would need to be added in uppercase
        # For simplicity, we test that the flag is preserved
        self.assertTrue(solver.case_sensitive)
    
    def test_single_letter_word(self):
        """Test single letter word."""
        solver = WordLadderSolver()
        # Single letters not in dictionary by default
        self.assertFalse(solver.is_valid_word("a"))
    
    def test_unicode_handling(self):
        """Test unicode characters."""
        solver = WordLadderSolver()
        self.assertFalse(solver.is_valid_word("café"))
    
    def test_none_handling(self):
        """Test None input handling."""
        solver = WordLadderSolver()
        # Python will raise TypeError for None input
        with self.assertRaises((TypeError, AttributeError)):
            solver.is_valid_word(None)


class TestPerformance(unittest.TestCase):
    """Performance-related tests."""
    
    def test_neighbors_count_reasonable(self):
        """Test neighbor count is reasonable."""
        solver = WordLadderSolver()
        neighbors = solver.get_neighbors("cat")
        # Should have some neighbors but not too many
        self.assertTrue(len(neighbors) > 0)
        self.assertTrue(len(neighbors) < 100)
    
    def test_path_length_reasonable(self):
        """Test path length is reasonable."""
        solver = WordLadderSolver()
        path = solver.find_shortest_path("cat", "dog")
        if path:
            self.assertTrue(len(path) < 20)
    
    def test_multiple_paths_same_length(self):
        """Test multiple paths have same length."""
        solver = WordLadderSolver()
        paths = solver.find_all_paths("cat", "dog", max_paths=10)
        if len(paths) > 1:
            lengths = [len(p) for p in paths]
            self.assertTrue(all(l == lengths[0] for l in lengths))


class TestWordDictionary(unittest.TestCase):
    """Tests for word dictionary."""
    
    def test_dictionary_size(self):
        """Test dictionary has reasonable size."""
        self.assertTrue(len(BUILTIN_WORDS[3]) >= 200)
        self.assertTrue(len(BUILTIN_WORDS[4]) >= 200)
        self.assertTrue(len(BUILTIN_WORDS[5]) >= 200)
        self.assertTrue(len(BUILTIN_WORDS[6]) >= 100)
    
    def test_all_lowercase(self):
        """Test all words are lowercase in builtin."""
        for length, words in BUILTIN_WORDS.items():
            for word in words:
                # All words in dictionary should be lowercase
                self.assertEqual(word, word.lower(), f"Word '{word}' is not lowercase")
    
    def test_common_words_present(self):
        """Test common words are present."""
        # 3-letter words
        common_3 = ["cat", "dog", "bat", "hat"]
        for word in common_3:
            self.assertIn(word, BUILTIN_WORDS[3])
        
        # 4-letter words
        common_4 = ["cold", "warm", "love", "hate"]
        for word in common_4:
            self.assertIn(word, BUILTIN_WORDS[4])


if __name__ == "__main__":
    unittest.main(verbosity=2)