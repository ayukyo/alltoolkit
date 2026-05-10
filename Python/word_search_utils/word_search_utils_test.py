"""
Unit tests for Word Search Puzzle Generator and Solver
"""

import unittest
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from word_search_utils.mod import (
    Direction,
    Difficulty,
    WordPlacement,
    PuzzleResult,
    WordSearchGenerator,
    WordSearchSolver,
    WordSearchUtils,
    generate_puzzle,
    solve_puzzle,
)


class TestDirection(unittest.TestCase):
    """Test Direction enum."""
    
    def test_direction_count(self):
        """Should have 8 directions."""
        self.assertEqual(len(Direction), 8)
    
    def test_direction_values(self):
        """All directions should have unique values."""
        values = [d.value for d in Direction]
        self.assertEqual(len(values), len(set(values)))


class TestWordPlacement(unittest.TestCase):
    """Test WordPlacement dataclass."""
    
    def test_horizontal_placement(self):
        """Test horizontal word placement positions."""
        placement = WordPlacement("HELLO", 2, 3, Direction.HORIZONTAL)
        
        self.assertEqual(placement.start_row, 2)
        self.assertEqual(placement.start_col, 3)
        self.assertEqual(len(placement.positions), 5)
        
        expected = [(2, 3), (2, 4), (2, 5), (2, 6), (2, 7)]
        self.assertEqual(placement.positions, expected)
    
    def test_vertical_placement(self):
        """Test vertical word placement positions."""
        placement = WordPlacement("CAT", 1, 2, Direction.VERTICAL)
        
        expected = [(1, 2), (2, 2), (3, 2)]
        self.assertEqual(placement.positions, expected)
    
    def test_diagonal_down_placement(self):
        """Test diagonal down word placement positions."""
        placement = WordPlacement("AB", 0, 0, Direction.DIAGONAL_DOWN)
        
        expected = [(0, 0), (1, 1)]
        self.assertEqual(placement.positions, expected)
    
    def test_diagonal_up_placement(self):
        """Test diagonal up word placement positions."""
        placement = WordPlacement("XY", 3, 1, Direction.DIAGONAL_UP)
        
        expected = [(3, 1), (2, 2)]
        self.assertEqual(placement.positions, expected)
    
    def test_reverse_horizontal(self):
        """Test reverse horizontal placement."""
        placement = WordPlacement("TEST", 1, 5, Direction.HORIZONTAL_REVERSE)
        
        expected = [(1, 5), (1, 4), (1, 3), (1, 2)]
        self.assertEqual(placement.positions, expected)
    
    def test_reverse_vertical(self):
        """Test reverse vertical placement."""
        placement = WordPlacement("UP", 4, 0, Direction.VERTICAL_REVERSE)
        
        expected = [(4, 0), (3, 0)]
        self.assertEqual(placement.positions, expected)


class TestPuzzleResult(unittest.TestCase):
    """Test PuzzleResult dataclass."""
    
    def test_get_grid_string(self):
        """Test grid string output."""
        grid = [['A', 'B'], ['C', 'D']]
        result = PuzzleResult(grid, [], [], (2, 2))
        
        expected = "A B\nC D"
        self.assertEqual(result.get_grid_string(), expected)
    
    def test_get_solution_string(self):
        """Test solution string with highlights."""
        grid = [['A', 'B'], ['C', 'D']]
        placement = WordPlacement("AB", 0, 0, Direction.HORIZONTAL)
        result = PuzzleResult(grid, [placement], [], (2, 2))
        
        solution = result.get_solution_string()
        self.assertIn('[A]', solution)
        self.assertIn('[B]', solution)


class TestWordSearchGenerator(unittest.TestCase):
    """Test WordSearchGenerator class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.generator = WordSearchGenerator(seed=42)
    
    def test_basic_generation(self):
        """Test basic puzzle generation."""
        words = ["CAT", "DOG", "BIRD"]
        result = self.generator.generate(words)
        
        self.assertGreater(len(result.grid), 0)
        self.assertGreater(len(result.words_placed), 0)
    
    def test_generation_with_size(self):
        """Test generation with specified size."""
        words = ["TEST"]
        result = self.generator.generate(words, size=(5, 5))
        
        self.assertEqual(len(result.grid), 5)
        self.assertEqual(len(result.grid[0]), 5)
    
    def test_all_words_placed(self):
        """Test that all words are placed when possible."""
        words = ["A", "B", "C"]
        result = self.generator.generate(words, size=(5, 5))
        
        self.assertEqual(len(result.words_not_placed), 0)
        self.assertEqual(len(result.words_placed), 3)
    
    def test_reproducibility_with_seed(self):
        """Test that same seed produces same puzzle."""
        gen1 = WordSearchGenerator(seed=123)
        gen2 = WordSearchGenerator(seed=123)
        
        words = ["HELLO", "WORLD", "TEST"]
        result1 = gen1.generate(words, size=(10, 10))
        result2 = gen2.generate(words, size=(10, 10))
        
        self.assertEqual(result1.grid, result2.grid)
    
    def test_difficulty_easy(self):
        """Test easy difficulty uses only horizontal and vertical."""
        words = ["TEST"]
        result = self.generator.generate(
            words, 
            size=(5, 5),
            difficulty=Difficulty.EASY
        )
        
        if result.words_placed:
            direction = result.words_placed[0].direction
            self.assertIn(direction, [Direction.HORIZONTAL, Direction.VERTICAL])
    
    def test_fill_character(self):
        """Test custom fill character."""
        words = ["TEST"]
        result = self.generator.generate(
            words,
            size=(3, 5),
            fill_char='.'
        )
        
        # Check that empty cells are filled with '.'
        for row in result.grid:
            for cell in row:
                self.assertEqual(len(cell), 1)
    
    def test_normalize_word(self):
        """Test word normalization."""
        words = ["hello", "WORLD", "TeSt"]
        result = self.generator.generate(words, size=(5, 5))
        
        for placement in result.words_placed:
            self.assertTrue(placement.word.isupper())
    
    def test_invalid_word_handling(self):
        """Test handling of invalid words."""
        words = ["", "123", "!!!", "VALID"]
        result = self.generator.generate(words, size=(5, 5))
        
        # Only VALID should be processed
        placed_words = [p.word for p in result.words_placed]
        self.assertIn("VALID", placed_words)
    
    def test_grid_filled(self):
        """Test that grid is completely filled."""
        words = ["TEST"]
        result = self.generator.generate(words, size=(3, 3))
        
        for row in result.grid:
            for cell in row:
                self.assertEqual(len(cell), 1)
                self.assertTrue(cell.isupper())
    
    def test_auto_size_calculation(self):
        """Test automatic size calculation."""
        words = ["PYTHON", "PROGRAMMING", "LANGUAGE"]
        result = self.generator.generate(words, auto_size=True)
        
        # Should be big enough for longest word
        self.assertGreaterEqual(result.size[0], 8)
        self.assertGreaterEqual(result.size[1], 8)


class TestWordSearchSolver(unittest.TestCase):
    """Test WordSearchSolver class."""
    
    def test_find_horizontal_word(self):
        """Test finding a horizontal word."""
        grid = [
            ['H', 'E', 'L', 'L', 'O'],
            ['A', 'B', 'C', 'D', 'E'],
        ]
        
        found, not_found = WordSearchSolver.solve(grid, ["HELLO"])
        
        self.assertEqual(len(found), 1)
        self.assertEqual(len(not_found), 0)
        self.assertEqual(found[0].word, "HELLO")
        self.assertEqual(found[0].direction, Direction.HORIZONTAL)
    
    def test_find_vertical_word(self):
        """Test finding a vertical word."""
        grid = [
            ['C', 'A'],
            ['A', 'B'],
            ['T', 'C'],
        ]
        
        found, not_found = WordSearchSolver.solve(grid, ["CAT"])
        
        self.assertEqual(len(found), 1)
        self.assertEqual(found[0].direction, Direction.VERTICAL)
    
    def test_find_diagonal_word(self):
        """Test finding a diagonal word."""
        grid = [
            ['D', 'X', 'X'],
            ['X', 'O', 'X'],
            ['X', 'X', 'G'],
        ]
        
        found, not_found = WordSearchSolver.solve(grid, ["DOG"])
        
        self.assertEqual(len(found), 1)
        self.assertEqual(found[0].direction, Direction.DIAGONAL_DOWN)
    
    def test_find_reverse_word(self):
        """Test finding a reverse word."""
        grid = [
            ['O', 'L', 'L', 'E', 'H'],
            ['A', 'B', 'C', 'D', 'E'],
        ]
        
        found, not_found = WordSearchSolver.solve(grid, ["HELLO"])
        
        self.assertEqual(len(found), 1)
        self.assertEqual(found[0].direction, Direction.HORIZONTAL_REVERSE)
    
    def test_word_not_found(self):
        """Test when word is not in grid."""
        grid = [
            ['A', 'B'],
            ['C', 'D'],
        ]
        
        found, not_found = WordSearchSolver.solve(grid, ["XYZ"])
        
        self.assertEqual(len(found), 0)
        self.assertEqual(len(not_found), 1)
    
    def test_multiple_words(self):
        """Test finding multiple words."""
        grid = [
            ['C', 'A', 'T', 'T'],
            ['A', 'B', 'E', 'E'],
            ['R', 'C', 'S', 'S'],
            ['X', 'X', 'X', 'T'],
        ]
        
        # CAT: row 0, horizontal (C-A-T)
        # CAR: column 0, vertical (C-A-R)
        # TEST: column 3, vertical (T-E-S-T)
        found, not_found = WordSearchSolver.solve(grid, ["CAT", "TEST", "CAR"])
        
        self.assertEqual(len(found), 3)
    
    def test_custom_directions(self):
        """Test finding words with custom directions."""
        grid = [
            ['A', 'B', 'C'],
            ['X', 'Y', 'Z'],
        ]
        
        # Only search horizontal
        found, _ = WordSearchSolver.solve(
            grid, ["ABC"], 
            directions=[Direction.HORIZONTAL]
        )
        
        self.assertEqual(len(found), 1)


class TestWordSearchUtils(unittest.TestCase):
    """Test WordSearchUtils class."""
    
    def test_create_empty_grid(self):
        """Test creating empty grid."""
        grid = WordSearchUtils.create_empty_grid(3, 4)
        
        self.assertEqual(len(grid), 3)
        self.assertEqual(len(grid[0]), 4)
        self.assertEqual(grid[0][0], ' ')
    
    def test_copy_grid(self):
        """Test grid copying."""
        original = [['A', 'B'], ['C', 'D']]
        copy = WordSearchUtils.copy_grid(original)
        
        # Modify copy
        copy[0][0] = 'X'
        
        # Original should be unchanged
        self.assertEqual(original[0][0], 'A')
    
    def test_grid_to_string(self):
        """Test grid to string conversion."""
        grid = [['A', 'B'], ['C', 'D']]
        s = WordSearchUtils.grid_to_string(grid)
        
        self.assertEqual(s, "A B\nC D")
    
    def test_string_to_grid(self):
        """Test string to grid conversion."""
        s = "AB\nCD"
        grid = WordSearchUtils.string_to_grid(s)
        
        self.assertEqual(grid, [['A', 'B'], ['C', 'D']])
    
    def test_calculate_fill_ratio(self):
        """Test fill ratio calculation."""
        grid = [['A', 'B'], ['C', 'D']]
        placement = WordPlacement("AB", 0, 0, Direction.HORIZONTAL)
        
        ratio = WordSearchUtils.calculate_fill_ratio(grid, [placement])
        
        # 2 cells out of 4 = 0.5
        self.assertEqual(ratio, 0.5)
    
    def test_generate_word_hints(self):
        """Test hint generation."""
        placement = WordPlacement("TEST", 0, 0, Direction.HORIZONTAL)
        hints = WordSearchUtils.generate_word_hints([placement])
        
        self.assertEqual(len(hints), 1)
        self.assertIn("TEST", hints[0])
        self.assertIn("→", hints[0])  # Horizontal direction arrow


class TestConvenienceFunctions(unittest.TestCase):
    """Test convenience functions."""
    
    def test_generate_puzzle(self):
        """Test generate_puzzle convenience function."""
        result = generate_puzzle(
            ["PYTHON", "CODE", "TEST"],
            size=(8, 8),
            difficulty="easy",
            seed=42
        )
        
        self.assertEqual(len(result.grid), 8)
        self.assertGreater(len(result.words_placed), 0)
    
    def test_solve_puzzle(self):
        """Test solve_puzzle convenience function."""
        grid = [
            ['C', 'A', 'T'],
            ['D', 'X', 'Y'],
            ['E', 'Z', 'W'],
        ]
        
        found, not_found = solve_puzzle(grid, ["CAT"])
        
        self.assertEqual(len(found), 1)
        self.assertEqual(found[0].word, "CAT")


class TestIntegration(unittest.TestCase):
    """Integration tests for complete workflows."""
    
    def test_generate_and_solve(self):
        """Test generating a puzzle and then solving it."""
        words = ["PYTHON", "JAVA", "CODE", "TEST"]
        
        # Generate puzzle
        generator = WordSearchGenerator(seed=123)
        result = generator.generate(words, size=(10, 10))
        
        # Get placed words
        placed_words = [p.word for p in result.words_placed]
        
        # Solve the puzzle
        found, not_found = WordSearchSolver.solve(result.grid, placed_words)
        
        # All placed words should be found
        self.assertEqual(len(found), len(placed_words))
        self.assertEqual(len(not_found), 0)
        
        # Check positions match
        for original, solved in zip(result.words_placed, found):
            self.assertEqual(original.word, solved.word)
            self.assertEqual(original.start_row, solved.start_row)
            self.assertEqual(original.start_col, solved.start_col)
    
    def test_large_puzzle(self):
        """Test generating a larger puzzle."""
        words = [f"WORD{i}" for i in range(10)]
        
        generator = WordSearchGenerator(seed=456)
        result = generator.generate(words, size=(15, 15))
        
        # Should place most words
        self.assertGreater(len(result.words_placed), 5)
    
    def test_difficulty_progression(self):
        """Test that harder difficulties use more directions."""
        word = "TEST"
        
        easy_gen = WordSearchGenerator(seed=789)
        hard_gen = WordSearchGenerator(seed=789)
        
        # Generate multiple times and collect directions
        easy_dirs = set()
        hard_dirs = set()
        
        for _ in range(10):
            easy_result = easy_gen.generate(
                [word], size=(5, 5), difficulty=Difficulty.EASY
            )
            hard_result = hard_gen.generate(
                [word], size=(5, 5), difficulty=Difficulty.HARD
            )
            
            if easy_result.words_placed:
                easy_dirs.add(easy_result.words_placed[0].direction)
            if hard_result.words_placed:
                hard_dirs.add(hard_result.words_placed[0].direction)
        
        # Easy should only use horizontal/vertical
        for d in easy_dirs:
            self.assertIn(d, [Direction.HORIZONTAL, Direction.VERTICAL])


if __name__ == '__main__':
    unittest.main(verbosity=2)