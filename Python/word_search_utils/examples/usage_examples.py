"""
Word Search Utils - Usage Examples
===================================

This file demonstrates the various features of the word search puzzle
generator and solver.
"""

import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mod import (
    WordSearchGenerator,
    WordSearchSolver,
    WordSearchUtils,
    Direction,
    Difficulty,
    generate_puzzle,
    solve_puzzle,
)


def example_basic_generation():
    """Example 1: Basic puzzle generation."""
    print("=" * 60)
    print("Example 1: Basic Puzzle Generation")
    print("=" * 60)
    
    words = ["PYTHON", "JAVA", "JAVASCRIPT", "RUST", "GOLANG"]
    
    # Simple generation with default settings
    result = generate_puzzle(words)
    
    print(f"\nPuzzle size: {result.size[0]}x{result.size[1]}")
    print(f"Words placed: {len(result.words_placed)}")
    print(f"Words not placed: {len(result.words_not_placed)}")
    
    print("\nGenerated Puzzle:")
    print("-" * 40)
    print(result.get_grid_string())
    
    print("\nWord List:")
    for placement in result.words_placed:
        direction_symbol = {
            Direction.HORIZONTAL: "→",
            Direction.VERTICAL: "↓",
            Direction.DIAGONAL_DOWN: "↘",
            Direction.DIAGONAL_UP: "↗",
            Direction.HORIZONTAL_REVERSE: "←",
            Direction.VERTICAL_REVERSE: "↑",
            Direction.DIAGONAL_DOWN_REVERSE: "↖",
            Direction.DIAGONAL_UP_REVERSE: "↙",
        }.get(placement.direction, "?")
        print(f"  {placement.word} {direction_symbol}")


def example_difficulty_levels():
    """Example 2: Different difficulty levels."""
    print("\n" + "=" * 60)
    print("Example 2: Difficulty Levels")
    print("=" * 60)
    
    words = ["EASY", "MEDIUM", "HARD"]
    
    # Easy - only horizontal and vertical
    easy_result = generate_puzzle(words, size=(6, 6), difficulty="easy", seed=42)
    
    # Medium - adds diagonal directions
    medium_result = generate_puzzle(words, size=(6, 6), difficulty="medium", seed=42)
    
    # Hard - all directions including reverse
    hard_result = generate_puzzle(words, size=(6, 6), difficulty="hard", seed=42)
    
    print("\nEasy Puzzle (horizontal & vertical only):")
    print(easy_result.get_grid_string())
    
    print("\nMedium Puzzle (adds diagonal directions):")
    print(medium_result.get_grid_string())
    
    print("\nHard Puzzle (all directions including reverse):")
    print(hard_result.get_grid_string())


def example_custom_directions():
    """Example 3: Custom direction configuration."""
    print("\n" + "=" * 60)
    print("Example 3: Custom Direction Configuration")
    print("=" * 60)
    
    words = ["CUSTOM", "DIRECTIONS"]
    
    # Only allow horizontal and diagonal
    custom_directions = [
        Direction.HORIZONTAL,
        Direction.DIAGONAL_DOWN,
    ]
    
    generator = WordSearchGenerator(seed=123)
    result = generator.generate(
        words,
        size=(8, 8),
        directions=custom_directions,
    )
    
    print("\nPuzzle with custom directions (horizontal & diagonal only):")
    print(result.get_grid_string())
    
    print("\nPlaced words:")
    for p in result.words_placed:
        print(f"  {p.word}: {p.direction.name} at ({p.start_row}, {p.start_col})")


def example_solving_puzzle():
    """Example 4: Solving an existing puzzle."""
    print("\n" + "=" * 60)
    print("Example 4: Solving a Puzzle")
    print("=" * 60)
    
    # Create a known puzzle
    grid = [
        ['P', 'Y', 'T', 'H', 'O', 'N', 'X', 'A'],
        ['R', 'A', 'E', 'X', 'Q', 'W', 'Y', 'B'],
        ['O', 'B', 'S', 'C', 'D', 'E', 'Z', 'C'],
        ['G', 'C', 'T', 'O', 'D', 'E', 'J', 'D'],
        ['R', 'D', 'E', 'D', 'E', 'F', 'K', 'E'],
        ['A', 'E', 'S', 'E', 'G', 'H', 'L', 'F'],
        ['M', 'X', 'T', 'J', 'A', 'V', 'A', 'G'],
        ['Z', 'W', 'V', 'U', 'T', 'S', 'R', 'H'],
    ]
    
    words_to_find = ["PYTHON", "CODE", "JAVA", "TEST", "RAM"]
    
    print("\nPuzzle to solve:")
    for row in grid:
        print(' '.join(row))
    
    # Solve the puzzle
    found, not_found = solve_puzzle(grid, words_to_find)
    
    print(f"\nWords found: {len(found)}")
    for placement in found:
        print(f"  {placement.word}: {placement.direction.name} "
              f"starting at ({placement.start_row}, {placement.start_col})")
    
    if not_found:
        print(f"\nWords not found: {not_found}")


def example_with_seed_reproducibility():
    """Example 5: Reproducible puzzles with seed."""
    print("\n" + "=" * 60)
    print("Example 5: Reproducible Puzzles (Seeded)")
    print("=" * 60)
    
    words = ["REPRODUCIBLE", "RANDOM", "SEED", "TEST"]
    
    # Same seed = same puzzle
    gen1 = WordSearchGenerator(seed=999)
    result1 = gen1.generate(words, size=(10, 10))
    
    gen2 = WordSearchGenerator(seed=999)
    result2 = gen2.generate(words, size=(10, 10))
    
    print("\nFirst generation:")
    print(result1.get_grid_string())
    
    print("\nSecond generation (same seed):")
    print(result2.get_grid_string())
    
    print("\nPuzzles are identical:", result1.grid == result2.grid)


def example_fill_options():
    """Example 6: Fill character options."""
    print("\n" + "=" * 60)
    print("Example 6: Fill Character Options")
    print("=" * 60)
    
    words = ["DOTS", "PUZZLE"]
    
    # Generate with dots as fill
    generator = WordSearchGenerator(seed=456)
    result_dots = generator.generate(
        words,
        size=(5, 7),
        fill_char='.',
    )
    
    # Generate with custom alphabet (only vowels)
    result_vowels = generator.generate(
        words,
        size=(5, 7),
        alphabet='AEIOU',
    )
    
    print("\nPuzzle with dots as fill:")
    print(result_dots.get_grid_string())
    
    print("\nPuzzle with vowels only for random fill:")
    print(result_vowels.get_grid_string())


def example_hints_and_statistics():
    """Example 7: Generating hints and statistics."""
    print("\n" + "=" * 60)
    print("Example 7: Hints and Statistics")
    print("=" * 60)
    
    words = ["PYTHON", "JAVASCRIPT", "TYPESCRIPT", "RUST"]
    
    generator = WordSearchGenerator(seed=789)
    result = generator.generate(words, size=(12, 15))
    
    print("\nGenerated Puzzle:")
    print(result.get_grid_string())
    
    # Generate hints
    hints = WordSearchUtils.generate_word_hints(
        result.words_placed,
        show_direction=True,
        show_position=False
    )
    
    print("\nWord Hints (direction only):")
    for hint in hints:
        print(f"  {hint}")
    
    # Calculate fill ratio
    fill_ratio = WordSearchUtils.calculate_fill_ratio(
        result.grid, result.words_placed
    )
    
    print(f"\nFill ratio: {fill_ratio:.1%}")
    print(f"Grid size: {result.size[0]}x{result.size[1]} = {result.size[0] * result.size[1]} cells")
    
    word_cells = sum(len(p.word) for p in result.words_placed)
    print(f"Word cells: {word_cells}")


def example_solution_grid():
    """Example 8: Solution grid with highlights."""
    print("\n" + "=" * 60)
    print("Example 8: Solution Grid")
    print("=" * 60)
    
    words = ["SOLUTION", "GRID", "HIGHLIGHT"]
    
    generator = WordSearchGenerator(seed=321)
    result = generator.generate(words, size=(10, 12))
    
    print("\nPuzzle (for players):")
    print(result.get_grid_string())
    
    print("\nSolution (with word positions highlighted):")
    print(result.get_solution_string())


def example_word_placement_details():
    """Example 9: Detailed word placement information."""
    print("\n" + "=" * 60)
    print("Example 9: Word Placement Details")
    print("=" * 60)
    
    words = ["DETAILS", "POSITIONS", "COORDINATES"]
    
    generator = WordSearchGenerator(seed=654)
    result = generator.generate(words, size=(12, 12))
    
    print(f"\nTotal words placed: {len(result.words_placed)}")
    
    for placement in result.words_placed:
        print(f"\n{placement.word}:")
        print(f"  Direction: {placement.direction.name}")
        print(f"  Start: row {placement.start_row}, col {placement.start_col}")
        print(f"  Positions: {placement.positions}")


def example_manual_grid_creation():
    """Example 10: Manual grid creation and solving."""
    print("\n" + "=" * 60)
    print("Example 10: Manual Grid Creation")
    print("=" * 60)
    
    # Create a simple puzzle manually
    grid = WordSearchUtils.create_empty_grid(5, 5, fill='.')
    
    # Place words manually using placements
    from mod import WordPlacement
    
    # Place "HELLO" horizontally
    hello = WordPlacement("HELLO", 0, 0, Direction.HORIZONTAL)
    for i, (r, c) in enumerate(hello.positions):
        grid[r][c] = hello.word[i]
    
    # Place "WORLD" vertically
    world = WordPlacement("WORLD", 0, 4, Direction.VERTICAL)
    for i, (r, c) in enumerate(world.positions):
        grid[r][c] = world.word[i]
    
    print("\nManually created puzzle:")
    print(WordSearchUtils.grid_to_string(grid))
    
    # Now solve it
    words_to_find = ["HELLO", "WORLD"]
    found, not_found = WordSearchSolver.solve(grid, words_to_find)
    
    print(f"\nSolving for {words_to_find}:")
    print(f"Found: {[p.word for p in found]}")
    print(f"Not found: {not_found}")


def example_multi_word_generation():
    """Example 11: Large-scale puzzle generation."""
    print("\n" + "=" * 60)
    print("Example 11: Large-Scale Puzzle")
    print("=" * 60)
    
    programming_words = [
        "ALGORITHM", "FUNCTION", "VARIABLE", "LOOP",
        "ARRAY", "OBJECT", "CLASS", "METHOD",
        "STRING", "INTEGER", "BOOLEAN", "DEBUG",
    ]
    
    generator = WordSearchGenerator(seed=111)
    result = generator.generate(
        programming_words,
        size=(15, 15),
        difficulty=Difficulty.HARD,
    )
    
    print(f"\nLarge puzzle: {result.size[0]}x{result.size[1]}")
    print(f"Words placed: {len(result.words_placed)}/{len(programming_words)}")
    
    if result.words_not_placed:
        print(f"Could not place: {result.words_not_placed}")
    
    print("\n" + result.get_grid_string())
    
    # Word list with directions
    print("\nWord List:")
    for placement in result.words_placed:
        dir_arrow = {
            Direction.HORIZONTAL: "→",
            Direction.VERTICAL: "↓",
            Direction.DIAGONAL_DOWN: "↘",
            Direction.DIAGONAL_UP: "↗",
            Direction.HORIZONTAL_REVERSE: "←",
            Direction.VERTICAL_REVERSE: "↑",
            Direction.DIAGONAL_DOWN_REVERSE: "↖",
            Direction.DIAGONAL_UP_REVERSE: "↙",
        }.get(placement.direction, "?")
        print(f"  {placement.word:<12} {dir_arrow}")


if __name__ == "__main__":
    # Run all examples
    example_basic_generation()
    example_difficulty_levels()
    example_custom_directions()
    example_solving_puzzle()
    example_with_seed_reproducibility()
    example_fill_options()
    example_hints_and_statistics()
    example_solution_grid()
    example_word_placement_details()
    example_manual_grid_creation()
    example_multi_word_generation()
    
    print("\n" + "=" * 60)
    print("All examples completed!")
    print("=" * 60)