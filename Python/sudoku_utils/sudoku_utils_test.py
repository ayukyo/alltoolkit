#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AllToolkit - Sudoku Utilities Test Suite
========================================
Comprehensive tests for the Sudoku utilities module.

Author: AllToolkit Contributors
License: MIT
"""

import sys
import os
import unittest
import random

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sudoku_utils.mod import (
    SudokuGrid, SudokuSolver, SudokuGenerator, SudokuValidator,
    SudokuHint, SudokuDifficultyEstimator, SudokuFormatter,
    Difficulty, create_puzzle, solve_puzzle, is_valid_puzzle,
    is_solved_puzzle, get_hint, estimate_difficulty, parse_puzzle,
    format_puzzle
)


class TestSudokuGrid(unittest.TestCase):
    """Test SudokuGrid class."""
    
    def test_empty_grid(self):
        """Test creating an empty grid."""
        grid = SudokuGrid()
        self.assertEqual(len(grid.get_empty_cells()), 81)
        for i in range(9):
            for j in range(9):
                self.assertEqual(grid.get(i, j), 0)
    
    def test_grid_with_values(self):
        """Test creating a grid with initial values."""
        data = [
            [5, 3, 0, 0, 7, 0, 0, 0, 0],
            [6, 0, 0, 1, 9, 5, 0, 0, 0],
            [0, 9, 8, 0, 0, 0, 0, 6, 0],
            [8, 0, 0, 0, 6, 0, 0, 0, 3],
            [4, 0, 0, 8, 0, 3, 0, 0, 1],
            [7, 0, 0, 0, 2, 0, 0, 0, 6],
            [0, 6, 0, 0, 0, 0, 2, 8, 0],
            [0, 0, 0, 4, 1, 9, 0, 0, 5],
            [0, 0, 0, 0, 8, 0, 0, 7, 9]
        ]
        grid = SudokuGrid(data)
        
        self.assertEqual(grid.get(0, 0), 5)
        self.assertEqual(grid.get(0, 1), 3)
        self.assertEqual(grid.get(0, 2), 0)
        self.assertEqual(grid.get(0, 4), 7)
    
    def test_grid_validation(self):
        """Test grid validation on construction."""
        # Invalid grid size
        with self.assertRaises(ValueError):
            SudokuGrid([[1, 2, 3]])  # Not 9x9
        
        # Invalid value
        with self.assertRaises(ValueError):
            SudokuGrid([[10 for _ in range(9)] for _ in range(9)])  # Value > 9
    
    def test_get_row_col_box(self):
        """Test row, column, and box extraction."""
        grid = SudokuGrid()
        grid.set(0, 0, 5)
        grid.set(0, 1, 3)
        
        row = grid.get_row(0)
        self.assertEqual(row[0], 5)
        self.assertEqual(row[1], 3)
        
        grid.set(1, 0, 6)
        col = grid.get_col(0)
        self.assertEqual(col[0], 5)
        self.assertEqual(col[1], 6)
        
        box = grid.get_box(0)
        self.assertEqual(box[0], 5)
        self.assertEqual(box[1], 3)
        self.assertEqual(box[3], 6)
    
    def test_candidates(self):
        """Test candidate calculation."""
        grid = SudokuGrid()
        grid.set(0, 0, 5)
        
        # Candidates for cell (0, 1) should not include 5 (same row)
        candidates = grid.get_candidates(0, 1)
        self.assertNotIn(5, candidates)
        self.assertIn(1, candidates)
        self.assertIn(2, candidates)
        
        grid.set(1, 0, 3)
        candidates = grid.get_candidates(0, 1)
        self.assertNotIn(5, candidates)  # Same row
        self.assertNotIn(3, candidates)  # Same box
    
    def test_copy(self):
        """Test grid copying."""
        grid = SudokuGrid()
        grid.set(0, 0, 5)
        
        copy = grid.copy()
        self.assertEqual(copy.get(0, 0), 5)
        
        copy.set(0, 0, 6)
        self.assertEqual(grid.get(0, 0), 5)  # Original unchanged
        self.assertEqual(copy.get(0, 0), 6)  # Copy changed
    
    def test_to_list(self):
        """Test conversion to list."""
        grid = SudokuGrid()
        grid.set(0, 0, 5)
        
        data = grid.to_list()
        self.assertEqual(data[0][0], 5)
        self.assertEqual(len(data), 9)
        self.assertEqual(len(data[0]), 9)


class TestSudokuSolver(unittest.TestCase):
    """Test SudokuSolver class."""
    
    def test_solve_simple_puzzle(self):
        """Test solving a simple puzzle."""
        # A simple puzzle
        data = [
            [5, 3, 0, 0, 7, 0, 0, 0, 0],
            [6, 0, 0, 1, 9, 5, 0, 0, 0],
            [0, 9, 8, 0, 0, 0, 0, 6, 0],
            [8, 0, 0, 0, 6, 0, 0, 0, 3],
            [4, 0, 0, 8, 0, 3, 0, 0, 1],
            [7, 0, 0, 0, 2, 0, 0, 0, 6],
            [0, 6, 0, 0, 0, 0, 2, 8, 0],
            [0, 0, 0, 4, 1, 9, 0, 0, 5],
            [0, 0, 0, 0, 8, 0, 0, 7, 9]
        ]
        grid = SudokuGrid(data)
        
        solution = solve_puzzle(grid)
        self.assertIsNotNone(solution)
        self.assertTrue(is_solved_puzzle(solution))
    
    def test_solve_unsolvable(self):
        """Test handling unsolvable puzzle."""
        # Create an invalid puzzle (two 5s in same row)
        data = [[5, 5, 0, 0, 0, 0, 0, 0, 0] for _ in range(9)]
        grid = SudokuGrid()
        grid.set(0, 0, 5)
        grid.set(0, 1, 5)  # Invalid
        
        solution = solve_puzzle(grid)
        self.assertIsNone(solution)  # Should return None for invalid puzzle
    
    def test_solve_empty_grid(self):
        """Test solving an empty grid (should work)."""
        grid = SudokuGrid()
        solution = solve_puzzle(grid)
        self.assertIsNotNone(solution)
        self.assertTrue(is_solved_puzzle(solution))
    
    def test_count_solutions(self):
        """Test solution counting."""
        # A puzzle with unique solution
        grid = create_puzzle(Difficulty.EASY)
        count = SudokuSolver.count_solutions(grid, 10)
        self.assertEqual(count, 1)
    
    def test_solve_copy(self):
        """Test that solve_copy doesn't modify original."""
        grid = SudokuGrid()
        solution = SudokuSolver.solve_copy(grid)
        
        self.assertIsNotNone(solution)
        self.assertEqual(len(grid.get_empty_cells()), 81)  # Original still empty
        self.assertEqual(len(solution.get_empty_cells()), 0)  # Solution filled


class TestSudokuGenerator(unittest.TestCase):
    """Test SudokuGenerator class."""
    
    def test_generate_puzzle(self):
        """Test puzzle generation."""
        puzzle = create_puzzle(Difficulty.MEDIUM)
        
        # Should have some empty cells
        empty = len(puzzle.get_empty_cells())
        self.assertGreater(empty, 20)
        self.assertLess(empty, 60)
        
        # Should be valid
        self.assertTrue(is_valid_puzzle(puzzle))
        
        # Should have unique solution
        count = SudokuSolver.count_solutions(puzzle, 2)
        self.assertEqual(count, 1)
    
    def test_generate_different_difficulties(self):
        """Test generating different difficulties."""
        easy = create_puzzle(Difficulty.EASY)
        medium = create_puzzle(Difficulty.MEDIUM)
        hard = create_puzzle(Difficulty.HARD)
        expert = create_puzzle(Difficulty.EXPERT)
        
        # Check that harder puzzles have fewer givens
        easy_givens = 81 - len(easy.get_empty_cells())
        medium_givens = 81 - len(medium.get_empty_cells())
        hard_givens = 81 - len(hard.get_empty_cells())
        expert_givens = 81 - len(expert.get_empty_cells())
        
        # Generally harder puzzles have fewer givens
        self.assertGreaterEqual(easy_givens, medium_givens)
        self.assertGreaterEqual(medium_givens, hard_givens)
    
    def test_generate_with_solution(self):
        """Test generating puzzle with solution."""
        puzzle, solution = SudokuGenerator.generate_with_solution(Difficulty.MEDIUM)
        
        self.assertTrue(is_valid_puzzle(puzzle))
        self.assertTrue(is_solved_puzzle(solution))
        
        # Solution should match puzzle's given numbers
        for i in range(9):
            for j in range(9):
                if puzzle.get(i, j) != 0:
                    self.assertEqual(puzzle.get(i, j), solution.get(i, j))
    
    def test_all_generated_puzzles_solvable(self):
        """Test that all generated puzzles are solvable."""
        for diff in [Difficulty.EASY, Difficulty.MEDIUM, Difficulty.HARD]:
            puzzle = create_puzzle(diff)
            solution = solve_puzzle(puzzle)
            self.assertIsNotNone(solution)


class TestSudokuValidator(unittest.TestCase):
    """Test SudokuValidator class."""
    
    def test_valid_grid(self):
        """Test valid grid check."""
        grid = SudokuGrid()
        self.assertTrue(is_valid_puzzle(grid))
        
        grid.set(0, 0, 5)
        self.assertTrue(is_valid_puzzle(grid))
    
    def test_invalid_grid_conflicts(self):
        """Test conflict detection."""
        grid = SudokuGrid()
        grid.set(0, 0, 5)
        grid.set(0, 1, 5)  # Same row
        
        self.assertFalse(is_valid_puzzle(grid))
        
        conflicts = SudokuValidator.get_conflicts(grid)
        self.assertGreater(len(conflicts), 0)
    
    def test_complete_check(self):
        """Test completeness check."""
        grid = SudokuGrid()
        self.assertFalse(SudokuValidator.is_complete(grid))
        
        # Fill grid
        solution = solve_puzzle(grid)
        self.assertTrue(SudokuValidator.is_complete(solution))
    
    def test_solved_check(self):
        """Test solved check."""
        puzzle = create_puzzle(Difficulty.EASY)
        self.assertFalse(is_solved_puzzle(puzzle))
        
        solution = solve_puzzle(puzzle)
        self.assertTrue(is_solved_puzzle(solution))


class TestSudokuHint(unittest.TestCase):
    """Test SudokuHint class."""
    
    def test_get_hint(self):
        """Test getting a hint."""
        puzzle = create_puzzle(Difficulty.EASY)
        solution = solve_puzzle(puzzle)
        
        hint = get_hint(puzzle, solution)
        self.assertIsNotNone(hint)
        
        row, col, val, technique = hint
        self.assertEqual(solution.get(row, col), val)
    
    def test_hint_progress(self):
        """Test that hints help progress the puzzle."""
        puzzle = create_puzzle(Difficulty.EASY)
        solution = solve_puzzle(puzzle)
        
        # Apply hints until puzzle is solved
        max_hints = 81
        hints_used = 0
        
        while not is_solved_puzzle(puzzle) and hints_used < max_hints:
            hint = get_hint(puzzle, solution)
            if hint:
                row, col, val, technique = hint
                puzzle.set(row, col, val)
                hints_used += 1
            else:
                break
        
        self.assertTrue(is_solved_puzzle(puzzle))


class TestSudokuDifficultyEstimator(unittest.TestCase):
    """Test SudokuDifficultyEstimator class."""
    
    def test_estimate_easy_puzzle(self):
        """Test estimating easy puzzle."""
        puzzle = create_puzzle(Difficulty.EASY)
        difficulty, metrics = estimate_difficulty(puzzle)
        
        self.assertIn(difficulty, [Difficulty.EASY, Difficulty.MEDIUM])
        self.assertIn('givens', metrics)
        self.assertGreater(metrics['givens'], 30)
    
    def test_estimate_hard_puzzle(self):
        """Test estimating hard puzzle."""
        puzzle = create_puzzle(Difficulty.HARD)
        difficulty, metrics = estimate_difficulty(puzzle)
        
        self.assertIn(difficulty, [Difficulty.MEDIUM, Difficulty.HARD, Difficulty.EXPERT])
        self.assertLess(metrics['givens'], 45)
    
    def test_metrics_calculated(self):
        """Test that metrics are calculated."""
        puzzle = create_puzzle(Difficulty.MEDIUM)
        difficulty, metrics = estimate_difficulty(puzzle)
        
        # Check metrics exist
        self.assertIn('givens', metrics)
        self.assertIn('empty_cells', metrics)
        self.assertIn('avg_candidates', metrics)
        self.assertIn('naked_singles', metrics)
        self.assertIn('hidden_singles', metrics)
        
        # Check values are reasonable
        self.assertEqual(metrics['givens'] + metrics['empty_cells'], 81)


class TestSudokuFormatter(unittest.TestCase):
    """Test SudokuFormatter class."""
    
    def test_to_string(self):
        """Test string conversion."""
        grid = SudokuGrid()
        grid.set(0, 0, 5)
        
        s = format_puzzle(grid, 'string')
        self.assertEqual(len(s), 81)
        self.assertEqual(s[0], '5')
    
    def test_from_string(self):
        """Test parsing from string."""
        s = "53..7....6..195....98....6.8...6...34..8.3..17...2...6.6....28....419..5....8..79"
        grid = parse_puzzle(s)
        
        self.assertEqual(grid.get(0, 0), 5)
        self.assertEqual(grid.get(0, 1), 3)
        self.assertEqual(grid.get(0, 2), 0)
    
    def test_string_roundtrip(self):
        """Test string roundtrip."""
        puzzle = create_puzzle(Difficulty.EASY)
        s = format_puzzle(puzzle, 'string')
        parsed = parse_puzzle(s)
        
        for i in range(9):
            for j in range(9):
                self.assertEqual(puzzle.get(i, j), parsed.get(i, j))
    
    def test_json_format(self):
        """Test JSON format."""
        puzzle = create_puzzle(Difficulty.EASY)
        json_str = format_puzzle(puzzle, 'json')
        
        parsed = SudokuFormatter.from_json(json_str)
        
        for i in range(9):
            for j in range(9):
                self.assertEqual(puzzle.get(i, j), parsed.get(i, j))
    
    def test_markdown_format(self):
        """Test Markdown format."""
        puzzle = create_puzzle(Difficulty.EASY)
        md = format_puzzle(puzzle, 'markdown')
        
        # Should contain table markers
        self.assertIn('|', md)
        self.assertIn('---', md)
    
    def test_pretty_format(self):
        """Test pretty format."""
        puzzle = create_puzzle(Difficulty.EASY)
        pretty = format_puzzle(puzzle, 'pretty')
        
        # Should contain borders
        self.assertIn('-', pretty)
        self.assertIn('|', pretty)


class TestConvenienceFunctions(unittest.TestCase):
    """Test convenience functions."""
    
    def test_create_puzzle(self):
        """Test create_puzzle function."""
        puzzle = create_puzzle(Difficulty.EASY)
        self.assertIsInstance(puzzle, SudokuGrid)
        self.assertTrue(is_valid_puzzle(puzzle))
    
    def test_solve_puzzle(self):
        """Test solve_puzzle function."""
        puzzle = create_puzzle(Difficulty.MEDIUM)
        solution = solve_puzzle(puzzle)
        
        self.assertIsNotNone(solution)
        self.assertTrue(is_solved_puzzle(solution))
    
    def test_parse_puzzle(self):
        """Test parse_puzzle function."""
        s = "53..7....6..195....98....6.8...6...34..8.3..17...2...6.6....28....419..5....8..79"
        puzzle = parse_puzzle(s)
        
        self.assertEqual(puzzle.get(0, 0), 5)
    
    def test_format_puzzle(self):
        """Test format_puzzle function."""
        puzzle = create_puzzle(Difficulty.EASY)
        
        # Test different formats
        string_fmt = format_puzzle(puzzle, 'string')
        self.assertEqual(len(string_fmt), 81)
        
        pretty_fmt = format_puzzle(puzzle, 'pretty')
        self.assertIsInstance(pretty_fmt, str)


class TestEdgeCases(unittest.TestCase):
    """Test edge cases and error handling."""
    
    def test_invalid_string_length(self):
        """Test parsing invalid string length."""
        with self.assertRaises(ValueError):
            parse_puzzle("123")  # Too short
    
    def test_invalid_format_type(self):
        """Test invalid format type."""
        puzzle = create_puzzle(Difficulty.EASY)
        with self.assertRaises(ValueError):
            format_puzzle(puzzle, 'invalid_format')
    
    def test_set_fixed_cell(self):
        """Test setting a fixed cell."""
        puzzle = create_puzzle(Difficulty.EASY)
        
        # Find a fixed cell
        fixed_cell = None
        for i in range(9):
            for j in range(9):
                if puzzle.is_fixed(i, j):
                    fixed_cell = (i, j)
                    break
        
        if fixed_cell:
            row, col = fixed_cell
            result = puzzle.set(row, col, 9)  # Try to change
            self.assertFalse(result)
    
    def test_solve_already_solved(self):
        """Test solving an already solved puzzle."""
        grid = SudokuGrid()
        solution = solve_puzzle(grid)
        
        # Solving again should still work
        solution2 = solve_puzzle(solution)
        self.assertIsNotNone(solution2)


class TestPerformance(unittest.TestCase):
    """Test performance of solver."""
    
    def test_solve_multiple_puzzles(self):
        """Test solving multiple puzzles quickly."""
        puzzles = [create_puzzle(Difficulty.HARD) for _ in range(5)]
        
        solutions = []
        for puzzle in puzzles:
            solution = solve_puzzle(puzzle)
            solutions.append(solution)
        
        # All should be solved
        for solution in solutions:
            self.assertIsNotNone(solution)
            self.assertTrue(is_solved_puzzle(solution))
    
    def test_solve_evil_puzzle(self):
        """Test solving a difficult puzzle."""
        puzzle = create_puzzle(Difficulty.EVIL)
        solution = solve_puzzle(puzzle)
        
        self.assertIsNotNone(solution)
        self.assertTrue(is_solved_puzzle(solution))


if __name__ == '__main__':
    unittest.main(verbosity=2)