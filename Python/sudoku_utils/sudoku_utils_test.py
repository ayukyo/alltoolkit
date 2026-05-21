"""
Test suite for sudoku_utils module.

Tests all major functionality including solving, generating, validating,
and analyzing sudoku puzzles.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sudoku_utils.mod import (
    SudokuGrid, SudokuSolver, SudokuGenerator, SudokuValidator,
    SudokuAnalyzer, Difficulty, solve, generate, validate, is_solved, analyze
)


def test_sudoku_grid():
    """Test SudokuGrid class."""
    print("Testing SudokuGrid...")
    
    # Test empty grid creation
    grid = SudokuGrid()
    assert grid.count_given() == 0
    assert len(grid.get_empty_cells()) == 81
    
    # Test grid from list
    data = [
        [5, 3, 0, 0, 7, 0, 0, 0, 0],
        [6, 0, 0, 1, 9, 5, 0, 0, 0],
        [0, 9, 8, 0, 0, 0, 0, 6, 0],
        [8, 0, 0, 0, 6, 0, 0, 0, 3],
        [4, 0, 0, 8, 0, 3, 0, 0, 1],
        [7, 0, 0, 0, 2, 0, 0, 0, 6],
        [0, 6, 0, 0, 0, 0, 2, 8, 0],
        [0, 0, 0, 4, 1, 9, 0, 0, 5],
        [0, 0, 0, 0, 8, 0, 0, 7, 9],
    ]
    grid = SudokuGrid(data)
    assert grid.count_given() == 30
    assert grid.get(0, 0) == 5
    assert grid.get(0, 2) == 0
    
    # Test row/col/box access
    assert grid.get_row(0) == [5, 3, 0, 0, 7, 0, 0, 0, 0]
    assert grid.get_col(0) == [5, 6, 0, 8, 4, 7, 0, 0, 0]
    assert grid.get_box(0, 0) == [5, 3, 0, 6, 0, 0, 0, 9, 8]
    
    # Test set/get
    grid.set(0, 2, 4)
    assert grid.get(0, 2) == 4
    
    # Test from_string (81 digits)
    grid2 = SudokuGrid.from_string("530070000600195000098000060800000045000000003700000026060000080000410005000080079")
    assert grid2.get(0, 0) == 5
    assert grid2.get(0, 2) == 0
    
    # Test from flat
    flat = [i % 10 for i in range(81)]
    grid3 = SudokuGrid.from_flat(flat)
    assert grid3.to_flat() == flat
    
    # Test to_list
    assert len(grid.to_list()) == 9
    assert len(grid.to_list()[0]) == 9
    
    # Test copy
    grid_copy = grid.copy()
    grid.set(0, 0, 9)
    assert grid_copy.get(0, 0) == 5  # Original unchanged
    
    # Test string representation
    str_repr = str(grid)
    assert "5" in str_repr
    assert "|" in str_repr  # Box borders
    assert "-" in str_repr
    
    print("✓ SudokuGrid tests passed")


def test_sudoku_solver():
    """Test SudokuSolver class."""
    print("Testing SudokuSolver...")
    
    # Test puzzle (medium difficulty)
    puzzle_data = [
        [5, 3, 0, 0, 7, 0, 0, 0, 0],
        [6, 0, 0, 1, 9, 5, 0, 0, 0],
        [0, 9, 8, 0, 0, 0, 0, 6, 0],
        [8, 0, 0, 0, 6, 0, 0, 0, 3],
        [4, 0, 0, 8, 0, 3, 0, 0, 1],
        [7, 0, 0, 0, 2, 0, 0, 0, 6],
        [0, 6, 0, 0, 0, 0, 2, 8, 0],
        [0, 0, 0, 4, 1, 9, 0, 0, 5],
        [0, 0, 0, 0, 8, 0, 0, 7, 9],
    ]
    grid = SudokuGrid(puzzle_data)
    solver = SudokuSolver(grid)
    
    # Test is_valid_placement
    # Cell (0, 2): box contains [5, 3, 0, 6, 0, 0, 0, 9, 8]
    # Row 0 contains [5, 3, 0, 0, 7, 0, 0, 0, 0]
    assert solver.is_valid_placement(0, 2, 1) == True   # 1 is valid
    assert solver.is_valid_placement(0, 2, 3) == False  # 3 already in box
    assert solver.is_valid_placement(0, 2, 5) == False  # 5 already in box
    assert solver.is_valid_placement(0, 2, 6) == False  # 6 already in box
    assert solver.is_valid_placement(0, 2, 9) == False  # 9 already in box
    
    # Test get_possible_values
    possible = solver.get_possible_values(0, 2)
    # Row 0 has [5, 3, _, _, 7, _, _, _, _] -> used: {5, 3, 7}
    # Col 2 has values from rows 0-8 -> used: {8} (row 2 has 8 at col 2)
    # Box (0,0) has [5, 3, _, 6, _, _, _, 9, 8] -> used: {5, 3, 6, 9, 8}
    # Combined used: {5, 3, 7, 8, 6, 9}
    # Possible: {1, 2, 4}
    assert 4 in possible
    assert 1 in possible  # 1 is valid
    assert 2 in possible  # 2 is valid
    assert 5 not in possible  # 5 in row and box
    assert 3 not in possible  # 3 in row and box
    assert len(possible) == 3  # {1, 2, 4}
    
    # Test solve
    solution = solver.get_solution()
    assert solution is not None
    assert SudokuValidator.is_valid_solution(solution)
    
    # Verify specific known solution values
    assert solution.get(0, 2) == 4
    assert solution.get(0, 3) == 6
    
    # Test count_solutions
    solver2 = SudokuSolver(grid)
    assert solver2.count_solutions(2) == 1  # Unique solution
    
    # Test has_unique_solution
    solver3 = SudokuSolver(grid)
    assert solver3.has_unique_solution() == True
    
    print("✓ SudokuSolver tests passed")


def test_sudoku_generator():
    """Test SudokuGenerator class."""
    print("Testing SudokuGenerator...")
    
    # Test generate_solved
    solved = SudokuGenerator.generate_solved()
    assert SudokuValidator.is_valid_solution(solved)
    assert solved.is_filled()
    
    # Test generate with different difficulties
    for difficulty in [Difficulty.EASY, Difficulty.MEDIUM, Difficulty.HARD]:
        puzzle = SudokuGenerator.generate(difficulty)
        assert SudokuValidator.is_valid_grid(puzzle)
        assert not puzzle.is_filled()  # Should have empty cells
        
        # Verify unique solution
        solver = SudokuSolver(puzzle)
        assert solver.has_unique_solution()
        
        # Check difficulty matches (roughly)
        given = puzzle.count_given()
        if difficulty == Difficulty.EASY:
            assert 36 <= given <= 45
        elif difficulty == Difficulty.MEDIUM:
            assert 27 <= given <= 35
        elif difficulty == Difficulty.HARD:
            assert 22 <= given <= 26
    
    # Test generate_with_solution
    puzzle, solution = SudokuGenerator.generate_with_solution(Difficulty.MEDIUM)
    assert SudokuValidator.is_valid_grid(puzzle)
    assert SudokuValidator.is_valid_solution(solution)
    
    # Verify puzzle matches solution for given cells
    for r in range(9):
        for c in range(9):
            if puzzle.get(r, c) != 0:
                assert puzzle.get(r, c) == solution.get(r, c)
    
    print("✓ SudokuGenerator tests passed")


def test_sudoku_validator():
    """Test SudokuValidator class."""
    print("Testing SudokuValidator...")
    
    # Test is_valid_grid
    valid_puzzle = [
        [5, 3, 0, 0, 7, 0, 0, 0, 0],
        [6, 0, 0, 1, 9, 5, 0, 0, 0],
        [0, 9, 8, 0, 0, 0, 0, 6, 0],
        [8, 0, 0, 0, 6, 0, 0, 0, 3],
        [4, 0, 0, 8, 0, 3, 0, 0, 1],
        [7, 0, 0, 0, 2, 0, 0, 0, 6],
        [0, 6, 0, 0, 0, 0, 2, 8, 0],
        [0, 0, 0, 4, 1, 9, 0, 0, 5],
        [0, 0, 0, 0, 8, 0, 0, 7, 9],
    ]
    assert SudokuValidator.is_valid_grid(SudokuGrid(valid_puzzle))
    
    # Test invalid grid (duplicate in row)
    invalid_row = [[5, 5, 0, 0, 0, 0, 0, 0, 0]] + [[0]*9 for _ in range(8)]
    assert not SudokuValidator.is_valid_grid(SudokuGrid(invalid_row))
    
    # Test invalid grid (duplicate in column)
    invalid_col = [[5] + [0]*8] + [[5] + [0]*8] + [[0]*9 for _ in range(7)]
    assert not SudokuValidator.is_valid_grid(SudokuGrid(invalid_col))
    
    # Test invalid grid (duplicate in box)
    invalid_box = [
        [5, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 5, 0, 0, 0, 0, 0, 0, 0],
    ] + [[0]*9 for _ in range(7)]
    assert not SudokuValidator.is_valid_grid(SudokuGrid(invalid_box))
    
    # Test is_valid_solution
    solved = SudokuGenerator.generate_solved()
    assert SudokuValidator.is_valid_solution(solved)
    
    # Test invalid solution (not filled)
    assert not SudokuValidator.is_valid_solution(SudokuGrid())
    
    # Test find_conflicts
    conflict_grid = [[5, 5, 0, 0, 0, 0, 0, 0, 0]] + [[0]*9 for _ in range(8)]
    conflicts = SudokuValidator.find_conflicts(SudokuGrid(conflict_grid))
    assert len(conflicts) > 0
    
    print("✓ SudokuValidator tests passed")


def test_sudoku_analyzer():
    """Test SudokuAnalyzer class."""
    print("Testing SudokuAnalyzer...")
    
    # Test estimate_difficulty
    easy_puzzle = SudokuGenerator.generate(Difficulty.EASY)
    difficulty = SudokuAnalyzer.estimate_difficulty(easy_puzzle)
    assert difficulty == Difficulty.EASY
    
    hard_puzzle = SudokuGenerator.generate(Difficulty.HARD)
    difficulty = SudokuAnalyzer.estimate_difficulty(hard_puzzle)
    assert difficulty in [Difficulty.HARD, Difficulty.EXPERT, Difficulty.EVIL]
    
    # Test get_progress
    grid = SudokuGrid([
        [5, 3, 4, 6, 7, 8, 9, 1, 2],
        [6, 7, 2, 1, 9, 5, 3, 4, 8],
        [1, 9, 8, 3, 4, 2, 5, 6, 7],
        [8, 5, 9, 7, 6, 1, 4, 2, 3],
        [4, 2, 6, 8, 5, 3, 7, 9, 1],
        [7, 1, 3, 9, 2, 4, 8, 5, 6],
        [9, 6, 1, 5, 3, 7, 2, 8, 4],
        [2, 8, 7, 4, 1, 9, 6, 3, 5],
        [3, 4, 5, 2, 8, 6, 1, 7, 0],  # One empty cell
    ])
    filled, total, percentage = SudokuAnalyzer.get_progress(grid)
    assert filled == 80
    assert total == 81
    assert abs(percentage - 98.77) < 0.1
    
    # Test get_hint (naked single)
    hint = SudokuAnalyzer.get_hint(grid)
    assert hint is not None
    r, c, val, technique = hint
    assert r == 8 and c == 8
    assert val == 9
    assert "single" in technique.lower()
    
    # Test get_all_hints
    puzzle = SudokuGenerator.generate(Difficulty.EASY)
    hints = SudokuAnalyzer.get_all_hints(puzzle)
    assert len(hints) > 0
    
    print("✓ SudokuAnalyzer tests passed")


def test_convenience_functions():
    """Test convenience functions."""
    print("Testing convenience functions...")
    
    # Test solve
    puzzle = SudokuGenerator.generate(Difficulty.EASY)
    solution = solve(puzzle)
    assert solution is not None
    assert is_solved(solution)
    
    # Test generate
    new_puzzle = generate(Difficulty.MEDIUM)
    assert validate(new_puzzle)
    
    # Test validate
    assert validate(puzzle)
    
    # Test is_solved
    assert is_solved(solution)
    assert not is_solved(puzzle)
    
    # Test analyze
    analysis = analyze(puzzle)
    assert "given_cells" in analysis
    assert "empty_cells" in analysis
    assert "difficulty" in analysis
    assert "is_valid" in analysis
    assert "has_unique_solution" in analysis
    assert analysis["is_valid"] == True
    assert analysis["has_unique_solution"] == True
    
    print("✓ Convenience function tests passed")


def test_edge_cases():
    """Test edge cases and error handling."""
    print("Testing edge cases...")
    
    # Test empty grid
    empty_grid = SudokuGrid()
    solver = SudokuSolver(empty_grid)
    solution = solver.get_solution()
    assert solution is not None
    assert SudokuValidator.is_valid_solution(solution)
    
    # Test solved grid
    solved = SudokuGenerator.generate_solved()
    solver = SudokuSolver(solved)
    assert solver.has_unique_solution()
    
    # Test invalid grid size
    try:
        invalid = SudokuGrid([[1, 2, 3]])  # Wrong size
        assert False, "Should have raised ValueError"
    except ValueError:
        pass
    
    # Test invalid cell value
    try:
        grid = SudokuGrid()
        grid.set(0, 0, 10)  # Invalid value
        assert False, "Should have raised ValueError"
    except ValueError:
        pass
    
    # Test from_string with invalid input
    try:
        SudokuGrid.from_string("123")  # Too short
        assert False, "Should have raised ValueError"
    except ValueError:
        pass
    
    print("✓ Edge case tests passed")


def test_performance():
    """Test performance with multiple puzzles."""
    print("Testing performance...")
    
    import time
    
    # Generate and solve multiple puzzles
    difficulties = [Difficulty.EASY, Difficulty.MEDIUM, Difficulty.HARD]
    
    for difficulty in difficulties:
        start = time.time()
        
        for _ in range(3):  # 3 puzzles per difficulty
            puzzle = SudokuGenerator.generate(difficulty)
            solver = SudokuSolver(puzzle)
            solution = solver.get_solution()
            assert solution is not None
            assert SudokuValidator.is_valid_solution(solution)
        
        elapsed = time.time() - start
        print(f"  Generated and solved 3 {difficulty.value} puzzles in {elapsed:.3f}s")
    
    print("✓ Performance tests passed")


def test_string_formatting():
    """Test string formatting and parsing."""
    print("Testing string formatting...")
    
    # Test from_string with various formats
    # Single line
    grid1 = SudokuGrid.from_string("530070000600195000098000060800000045000000003700000026060000080000410005000080079")
    assert grid1.count_given() == 25  # Count of non-zero digits in the string
    
    # With dots for zeros (full 81 characters)
    # Using same puzzle but with dots for zeros
    grid2 = SudokuGrid.from_string("53..7....6..195....98....6.8......45........37......26.6.....8....41...5....8..79")
    assert grid2.count_given() == 25  # Same as grid1
    
    # Multi-line with separators
    multi_line = """
    5 3 0 | 0 7 0 | 0 0 0
    6 0 0 | 1 9 5 | 0 0 0
    0 9 8 | 0 0 0 | 0 6 0
    ------+-------+------
    8 0 0 | 0 6 0 | 0 0 3
    4 0 0 | 8 0 3 | 0 0 1
    7 0 0 | 0 2 0 | 0 0 6
    ------+-------+------
    0 6 0 | 0 0 0 | 2 8 0
    0 0 0 | 4 1 9 | 0 0 5
    0 0 0 | 0 8 0 | 0 7 9
    """
    grid3 = SudokuGrid.from_string(multi_line)
    assert grid3.count_given() == 30
    
    # Test __str__ output
    str_output = str(grid3)
    assert "5" in str_output
    assert "|" in str_output
    
    print("✓ String formatting tests passed")


def run_all_tests():
    """Run all test suites."""
    print("\n" + "="*50)
    print("Sudoku Utils Test Suite")
    print("="*50 + "\n")
    
    test_sudoku_grid()
    test_sudoku_solver()
    test_sudoku_generator()
    test_sudoku_validator()
    test_sudoku_analyzer()
    test_convenience_functions()
    test_edge_cases()
    test_performance()
    test_string_formatting()
    
    print("\n" + "="*50)
    print("All tests passed! ✓")
    print("="*50)


if __name__ == "__main__":
    run_all_tests()