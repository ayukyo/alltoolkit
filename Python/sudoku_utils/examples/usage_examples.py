#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AllToolkit - Sudoku Utilities Usage Examples
=============================================
Demonstrates various ways to use the Sudoku utilities module.

Author: AllToolkit Contributors
License: MIT
"""

import sys
import os

# Add Python directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from sudoku_utils.mod import (
    SudokuGrid, SudokuSolver, SudokuGenerator, SudokuValidator,
    SudokuHint, SudokuDifficultyEstimator, SudokuFormatter,
    Difficulty, create_puzzle, solve_puzzle, is_valid_puzzle,
    is_solved_puzzle, get_hint, estimate_difficulty, parse_puzzle,
    format_puzzle
)


def example_1_basic_usage():
    """
    Example 1: Basic puzzle generation and solving
    """
    print("\n" + "=" * 60)
    print("Example 1: Basic Usage")
    print("=" * 60)
    
    # Generate a puzzle
    print("\n1. Generate a Medium difficulty puzzle:")
    puzzle = create_puzzle(Difficulty.MEDIUM)
    print(format_puzzle(puzzle, 'pretty'))
    
    # Solve it
    print("\n2. Solve the puzzle:")
    solution = solve_puzzle(puzzle)
    if solution:
        print(format_puzzle(solution, 'pretty'))
    else:
        print("Could not solve!")
    
    # Validate
    print("\n3. Validation:")
    print(f"   Puzzle is valid: {is_valid_puzzle(puzzle)}")
    print(f"   Solution is solved: {is_solved_puzzle(solution) if solution else 'N/A'}")


def example_2_difficulty_levels():
    """
    Example 2: Generate puzzles at different difficulty levels
    """
    print("\n" + "=" * 60)
    print("Example 2: Different Difficulty Levels")
    print("=" * 60)
    
    for diff in [Difficulty.EASY, Difficulty.MEDIUM, Difficulty.HARD, Difficulty.EXPERT]:
        print(f"\n{diff.name} puzzle:")
        puzzle = create_puzzle(diff)
        
        # Get statistics
        empty_count = len(puzzle.get_empty_cells())
        given_count = 81 - empty_count
        
        # Estimate actual difficulty
        estimated_diff, metrics = estimate_difficulty(puzzle)
        
        print(f"   Given numbers: {given_count}")
        print(f"   Empty cells: {empty_count}")
        print(f"   Estimated difficulty: {estimated_diff.name}")
        print(f"   Average candidates: {metrics['avg_candidates']:.2f}")
        
        # Show first few cells
        print("   Top-left corner:")
        for i in range(3):
            row_str = "   "
            for j in range(3):
                val = puzzle.get(i, j)
                row_str += f"{val if val != 0 else '.'} "
            print(row_str)


def example_3_parse_and_solve():
    """
    Example 3: Parse a puzzle from string and solve it
    """
    print("\n" + "=" * 60)
    print("Example 3: Parse and Solve")
    print("=" * 60)
    
    # Famous puzzle string
    puzzle_string = "53..7....6..195....98....6.8...6...34..8.3..17...2...6.6....28....419..5....8..79"
    
    print("\n1. Parse puzzle from string:")
    print(f"   Input: {puzzle_string[:40]}...")
    
    puzzle = parse_puzzle(puzzle_string)
    print("\n   Grid:")
    print(format_puzzle(puzzle, 'pretty'))
    
    print("\n2. Solve and show solution:")
    solution = solve_puzzle(puzzle)
    if solution:
        print(format_puzzle(solution, 'pretty'))
        
        # Convert back to string
        solution_string = format_puzzle(solution, 'string')
        print(f"\n   Solution string: {solution_string[:40]}...")
    else:
        print("   Could not solve!")


def example_4_get_hints():
    """
    Example 4: Get hints for stuck players
    """
    print("\n" + "=" * 60)
    print("Example 4: Hint System")
    print("=" * 60)
    
    # Generate puzzle and solution
    puzzle, solution = SudokuGenerator.generate_with_solution(Difficulty.EASY)
    
    print("\n1. Original puzzle:")
    print(format_puzzle(puzzle, 'pretty'))
    
    print("\n2. Getting hints one by one:")
    
    # Simulate player getting stuck and asking for hints
    for hint_num in range(1, 6):
        hint = get_hint(puzzle, solution)
        if hint:
            row, col, val, technique = hint
            print(f"\n   Hint #{hint_num}:")
            print(f"   Place {val} at row {row+1}, column {col+1}")
            print(f"   Reason: {technique}")
            
            # Apply the hint
            puzzle.set(row, col, val)
            
            # Show progress
            empty = len(puzzle.get_empty_cells())
            print(f"   Progress: {81 - empty}/81 cells filled")
        else:
            print(f"\n   No more hints needed - puzzle is complete!")
            break
    
    print("\n3. Remaining grid:")
    print(format_puzzle(puzzle, 'pretty'))


def example_5_validate_and_find_conflicts():
    """
    Example 5: Validate puzzles and find conflicts
    """
    print("\n" + "=" * 60)
    print("Example 5: Validation and Conflict Detection")
    print("=" * 60)
    
    # Create a valid puzzle
    print("\n1. Valid puzzle:")
    puzzle = create_puzzle(Difficulty.EASY)
    print(f"   Is valid: {is_valid_puzzle(puzzle)}")
    
    # Create a puzzle with conflicts (manually)
    print("\n2. Creating a puzzle with conflict:")
    bad_puzzle = SudokuGrid()
    bad_puzzle.set(0, 0, 5)
    bad_puzzle.set(0, 1, 5)  # Conflict: same row!
    
    print(f"   Is valid: {is_valid_puzzle(bad_puzzle)}")
    
    conflicts = SudokuValidator.get_conflicts(bad_puzzle)
    print(f"   Number of conflicts found: {len(conflicts)}")
    
    for c1_row, c1_col, c2_row, c2_col in conflicts:
        val1 = bad_puzzle.get(c1_row, c1_col)
        val2 = bad_puzzle.get(c2_row, c2_col)
        print(f"   Conflict: ({c1_row+1},{c1_col+1})={val1} conflicts with ({c2_row+1},{c2_col+1})={val2}")


def example_6_formats():
    """
    Example 6: Different output formats
    """
    print("\n" + "=" * 60)
    print("Example 6: Output Formats")
    print("=" * 60)
    
    puzzle = create_puzzle(Difficulty.MEDIUM)
    
    print("\n1. Pretty format (with borders):")
    print(format_puzzle(puzzle, 'pretty')[:100] + "...")
    
    print("\n2. String format (compact):")
    print(format_puzzle(puzzle, 'string'))
    
    print("\n3. JSON format (first 100 chars):")
    print(format_puzzle(puzzle, 'json')[:100] + "...")
    
    print("\n4. Markdown format (table):")
    print(format_puzzle(puzzle, 'markdown'))
    
    print("\n5. 2D array format:")
    data = puzzle.to_list()
    print(f"   First row: {data[0]}")


def example_7_cell_operations():
    """
    Example 7: Working with individual cells
    """
    print("\n" + "=" * 60)
    print("Example 7: Cell Operations")
    print("=" * 60)
    
    puzzle = create_puzzle(Difficulty.EASY)
    
    print("\n1. Checking cell properties:")
    
    # Find first empty cell
    empty_cells = puzzle.get_empty_cells()
    if empty_cells:
        row, col = empty_cells[0]
        print(f"   First empty cell: row {row+1}, column {col+1}")
        print(f"   Candidates for this cell: {puzzle.get_candidates(row, col)}")
        
        print("\n2. Setting a value:")
        print(f"   Before: value = {puzzle.get(row, col)}")
        
        candidates = list(puzzle.get_candidates(row, col))
        if candidates:
            puzzle.set(row, col, candidates[0])
            print(f"   After: value = {puzzle.get(row, col)}")
            
            print("\n3. Checking if cell is fixed (given number):")
            print(f"   Is fixed: {puzzle.is_fixed(row, col)}")
            
            # Try to change a fixed cell
            for i in range(9):
                for j in range(9):
                    if puzzle.is_fixed(i, j):
                        print(f"   Found fixed cell at ({i+1}, {j+1}) with value {puzzle.get(i, j)}")
                        print(f"   Trying to change it to 9...")
                        result = puzzle.set(i, j, 9)
                        print(f"   Success: {result}")
                        break
                break


def example_8_row_col_box_operations():
    """
    Example 8: Working with rows, columns, and boxes
    """
    print("\n" + "=" * 60)
    print("Example 8: Row, Column, Box Operations")
    print("=" * 60)
    
    puzzle, solution = SudokuGenerator.generate_with_solution(Difficulty.EASY)
    
    print("\n1. Get row contents:")
    print(f"   Row 1: {puzzle.get_row(0)}")
    print(f"   Row 5: {puzzle.get_row(4)}")
    
    print("\n2. Get column contents:")
    print(f"   Column 1: {puzzle.get_col(0)}")
    print(f"   Column 5: {puzzle.get_col(4)}")
    
    print("\n3. Get 3x3 box contents:")
    print(f"   Box 0 (top-left): {puzzle.get_box(0)}")
    print(f"   Box 4 (center): {puzzle.get_box(4)}")
    print(f"   Box 8 (bottom-right): {puzzle.get_box(8)}")
    
    print("\n4. Box numbering explained:")
    print("   Boxes are numbered left-to-right, top-to-bottom:")
    print("   0 | 1 | 2")
    print("   3 | 4 | 5")
    print("   6 | 7 | 8")


def example_9_check_unique_solution():
    """
    Example 9: Check for unique solution
    """
    print("\n" + "=" * 60)
    print("Example 9: Unique Solution Check")
    print("=" * 60)
    
    print("\n1. Generated puzzle (always has unique solution):")
    puzzle = create_puzzle(Difficulty.MEDIUM)
    
    count = SudokuSolver.count_solutions(puzzle, max_count=10)
    print(f"   Number of solutions: {count}")
    print(f"   Has unique solution: {SudokuValidator.has_unique_solution(puzzle)}")
    
    print("\n2. Empty grid (has many solutions):")
    empty = SudokuGrid()
    count = SudokuSolver.count_solutions(empty, max_count=10)
    print(f"   Number of solutions (limited to 10): {count}")
    print(f"   (Actually millions of solutions exist)")
    
    print("\n3. Partially filled grid:")
    partial = SudokuGrid()
    partial.set(0, 0, 1)
    partial.set(1, 1, 2)
    partial.set(2, 2, 3)
    
    count = SudokuSolver.count_solutions(partial, max_count=10)
    print(f"   Number of solutions (limited to 10): {count}")


def example_10_full_game_flow():
    """
    Example 10: Complete game flow demonstration
    """
    print("\n" + "=" * 60)
    print("Example 10: Complete Game Flow")
    print("=" * 60)
    
    # Generate
    print("\n1. Generate new puzzle:")
    puzzle = create_puzzle(Difficulty.MEDIUM)
    difficulty, metrics = estimate_difficulty(puzzle)
    
    print(f"   Generated difficulty: {difficulty.name}")
    print(f"   Given numbers: {metrics['givens']}")
    print(format_puzzle(puzzle, 'pretty'))
    
    # Solve
    print("\n2. Solve the puzzle:")
    solution = solve_puzzle(puzzle)
    print(format_puzzle(solution, 'pretty'))
    
    # Save
    print("\n3. Save puzzle as string:")
    puzzle_string = format_puzzle(puzzle, 'string')
    print(f"   Puzzle: {puzzle_string}")
    
    solution_string = format_puzzle(solution, 'string')
    print(f"   Solution: {solution_string}")
    
    # Load
    print("\n4. Load puzzle from string:")
    loaded = parse_puzzle(puzzle_string)
    
    # Verify
    print("\n5. Verify loaded puzzle matches original:")
    match = True
    for i in range(9):
        for j in range(9):
            if puzzle.get(i, j) != loaded.get(i, j):
                match = False
                break
    print(f"   Match: {match}")


def main():
    """Run all examples."""
    print("\n" + "=" * 60)
    print("Sudoku Utilities - Usage Examples")
    print("=" * 60)
    
    example_1_basic_usage()
    example_2_difficulty_levels()
    example_3_parse_and_solve()
    example_4_get_hints()
    example_5_validate_and_find_conflicts()
    example_6_formats()
    example_7_cell_operations()
    example_8_row_col_box_operations()
    example_9_check_unique_solution()
    example_10_full_game_flow()
    
    print("\n" + "=" * 60)
    print("All examples completed!")
    print("=" * 60)


if __name__ == "__main__":
    main()