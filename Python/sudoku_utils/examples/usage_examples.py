"""
Sudoku Utils - Usage Examples

Demonstrates how to use the sudoku_utils module for:
- Solving puzzles
- Generating new puzzles
- Validating solutions
- Analyzing puzzles
- Getting hints
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from sudoku_utils.mod import (
    SudokuGrid, SudokuSolver, SudokuGenerator, SudokuValidator,
    SudokuAnalyzer, Difficulty, solve, generate, validate, is_solved, analyze
)


def example_basic_solve():
    """Basic puzzle solving example."""
    print("\n" + "="*50)
    print("Example 1: Basic Puzzle Solving")
    print("="*50)
    
    # Define a puzzle (0 or . for empty cells)
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
    
    puzzle = SudokuGrid(puzzle_data)
    
    print("\nOriginal Puzzle:")
    print(puzzle)
    
    # Solve using convenience function
    solution = solve(puzzle)
    
    if solution:
        print("\nSolution:")
        print(solution)
        print("\n✓ Puzzle solved!")
    else:
        print("\n✗ No solution found!")


def example_generate_puzzle():
    """Generate puzzles with different difficulties."""
    print("\n" + "="*50)
    print("Example 2: Generating Puzzles")
    print("="*50)
    
    for difficulty in [Difficulty.EASY, Difficulty.MEDIUM, Difficulty.HARD]:
        puzzle = generate(difficulty)
        given = puzzle.count_given()
        
        print(f"\n{difficulty.value.upper()} Puzzle ({given} given cells):")
        print(puzzle)
    
    # Generate with solution
    print("\n" + "-"*30)
    print("Generating puzzle with solution...")
    puzzle, solution = SudokuGenerator.generate_with_solution(Difficulty.MEDIUM)
    
    print("\nPuzzle:")
    print(puzzle)
    print("\nSolution:")
    print(solution)


def example_parsing_formats():
    """Parse puzzles from different string formats."""
    print("\n" + "="*50)
    print("Example 3: Parsing Different Formats")
    print("="*50)
    
    # Single line format
    single_line = "530070000600195000098000060800000045000000003700000026060000080000410005000080079"
    grid1 = SudokuGrid.from_string(single_line)
    print("\nFrom single line (81 digits):")
    print(grid1)
    
    # With dots
    with_dots = "53..7....6..195....98......."
    grid2 = SudokuGrid.from_string(with_dots)
    print("\nWith dots for empty cells:")
    print(grid2)
    
    # Multi-line with box separators
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
    print("\nFrom multi-line with separators:")
    print(grid3)


def example_validation():
    """Validate puzzles and find conflicts."""
    print("\n" + "="*50)
    print("Example 4: Validation and Conflict Detection")
    print("="*50)
    
    # Valid puzzle
    valid = [
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
    
    puzzle = SudokuGrid(valid)
    print("\nValid puzzle:")
    print(f"  is_valid_grid: {validate(puzzle)}")
    
    # Invalid puzzle (duplicate in row)
    invalid = [
        [5, 5, 0, 0, 7, 0, 0, 0, 0],  # Two 5s in first row
        [6, 0, 0, 1, 9, 5, 0, 0, 0],
        [0, 9, 8, 0, 0, 0, 0, 6, 0],
        [8, 0, 0, 0, 6, 0, 0, 0, 3],
        [4, 0, 0, 8, 0, 3, 0, 0, 1],
        [7, 0, 0, 0, 2, 0, 0, 0, 6],
        [0, 6, 0, 0, 0, 0, 2, 8, 0],
        [0, 0, 0, 4, 1, 9, 0, 0, 5],
        [0, 0, 0, 0, 8, 0, 0, 7, 9],
    ]
    
    invalid_puzzle = SudokuGrid(invalid)
    print("\nInvalid puzzle (duplicate 5 in row):")
    print(f"  is_valid_grid: {validate(invalid_puzzle)}")
    
    # Find conflicts
    conflicts = SudokuValidator.find_conflicts(invalid_puzzle)
    print("\n  Conflicts found:")
    for r, c, val, conflict_type in conflicts:
        print(f"    Cell ({r}, {c}) = {val}: {conflict_type}")


def example_analyze_and_hints():
    """Analyze puzzles and get hints."""
    print("\n" + "="*50)
    print("Example 5: Analysis and Hints")
    print("="*50)
    
    puzzle = generate(Difficulty.MEDIUM)
    
    print("\nGenerated Puzzle:")
    print(puzzle)
    
    # Analyze
    analysis = analyze(puzzle)
    print("\nAnalysis:")
    print(f"  Given cells: {analysis['given_cells']}")
    print(f"  Empty cells: {analysis['empty_cells']}")
    print(f"  Difficulty: {analysis['difficulty']}")
    print(f"  Valid: {analysis['is_valid']}")
    print(f"  Unique solution: {analysis['has_unique_solution']}")
    
    # Get progress
    filled, total, pct = SudokuAnalyzer.get_progress(puzzle)
    print(f"\nProgress: {filled}/{total} cells filled ({pct:.1f}%)")
    
    # Get a hint
    hint = SudokuAnalyzer.get_hint(puzzle)
    if hint:
        r, c, val, technique = hint
        print(f"\nHint: Cell ({r}, {c}) = {val}")
        print(f"  Technique: {technique}")
    
    # Get all hints
    all_hints = SudokuAnalyzer.get_all_hints(puzzle)
    print(f"\nTotal hints available: {len(all_hints)}")
    print("First 5 hints:")
    for r, c, val, technique in all_hints[:5]:
        print(f"  ({r}, {c}) = {val} [{technique}]")


def example_solver_details():
    """Detailed solver usage."""
    print("\n" + "="*50)
    print("Example 6: Solver Details")
    print("="*50)
    
    puzzle = generate(Difficulty.EASY)
    solver = SudokuSolver(puzzle)
    
    print("\nPuzzle:")
    print(puzzle)
    
    # Check possible values for first empty cell
    empty_cells = puzzle.get_empty_cells()
    if empty_cells:
        r, c = empty_cells[0]
        possible = solver.get_possible_values(r, c)
        print(f"\nPossible values for cell ({r}, {c}): {sorted(possible)}")
    
    # Check unique solution
    print(f"\nHas unique solution: {solver.has_unique_solution()}")
    
    # Count solutions (up to 2)
    num_solutions = solver.count_solutions(2)
    print(f"Solutions found: {num_solutions}")
    
    # Get solution
    solution = solver.get_solution()
    if solution:
        print("\nSolution:")
        print(solution)


def example_difficulty_levels():
    """Generate puzzles at all difficulty levels."""
    print("\n" + "="*50)
    print("Example 7: All Difficulty Levels")
    print("="*50)
    
    difficulties = [
        Difficulty.EASY,
        Difficulty.MEDIUM,
        Difficulty.HARD,
        Difficulty.EXPERT,
        Difficulty.EVIL,
    ]
    
    for diff in difficulties:
        puzzle = generate(diff)
        given = puzzle.count_given()
        
        # Verify solvable
        solution = solve(puzzle)
        has_solution = solution is not None
        
        print(f"\n{diff.value.upper():7} ({given:2} given): {'' if has_solution else 'not '}solvable")


def example_conversions():
    """Convert between formats."""
    print("\n" + "="*50)
    print("Example 8: Format Conversions")
    print("="*50)
    
    puzzle = generate(Difficulty.EASY)
    
    print("\nOriginal:")
    print(puzzle)
    
    # To nested list
    as_list = puzzle.to_list()
    print(f"\nAs list: {as_list[0]} ...")
    
    # To flat list
    as_flat = puzzle.to_flat()
    print(f"As flat: {as_flat[:20]} ...")
    
    # From flat
    reconstructed = SudokuGrid.from_flat(as_flat)
    print(f"\nReconstructed from flat:")
    print(reconstructed)
    
    # Verify
    assert puzzle.to_flat() == reconstructed.to_flat()
    print("\n✓ Round-trip conversion successful!")


def main():
    """Run all examples."""
    print("\n" + "#"*50)
    print("# Sudoku Utils - Usage Examples")
    print("#"*50)
    
    example_basic_solve()
    example_generate_puzzle()
    example_parsing_formats()
    example_validation()
    example_analyze_and_hints()
    example_solver_details()
    example_difficulty_levels()
    example_conversions()
    
    print("\n" + "#"*50)
    print("# All examples completed!")
    print("#"*50 + "\n")


if __name__ == "__main__":
    main()