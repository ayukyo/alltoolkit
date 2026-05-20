"""
Word Ladder Utils - Usage Examples

Examples demonstrating word ladder puzzle functionality.

Author: AllToolkit Auto-Generator
Date: 2026-05-20
"""

import os
import sys
# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from word_ladder_utils.mod import (
    WordLadderSolver,
    find_shortest_path,
    find_all_paths,
    get_neighbors,
    is_valid_word,
    is_valid_transformation,
    validate_ladder,
    generate_puzzle,
    get_ladder_difficulty,
    create_solver,
    add_words
)


def example_1_basic_usage():
    """
    Example 1: Basic word ladder solving.
    
    Find the shortest path from "cat" to "dog".
    """
    print("=" * 60)
    print("Example 1: Basic Word Ladder - cat to dog")
    print("=" * 60)
    
    path = find_shortest_path("cat", "dog")
    
    if path:
        print(f"\nFound path with {len(path)} steps:")
        for i, word in enumerate(path):
            arrow = " → " if i < len(path) - 1 else ""
            print(f"  {i + 1}. {word}{arrow}")
        
        # Visual representation
        print("\nVisual:")
        print("  " + " → ".join(path))
    else:
        print("No path found!")


def example_2_multiple_paths():
    """
    Example 2: Finding multiple paths.
    
    Find all possible shortest paths between two words.
    """
    print("\n" + "=" * 60)
    print("Example 2: Finding Multiple Paths")
    print("=" * 60)
    
    paths = find_all_paths("cat", "dog", max_paths=5)
    
    print(f"\nFound {len(paths)} shortest paths from 'cat' to 'dog':")
    for i, path in enumerate(paths, 1):
        print(f"\nPath {i} ({len(path)} steps):")
        print("  " + " → ".join(path))


def example_3_neighbors():
    """
    Example 3: Finding word neighbors.
    
    Get all words that differ by exactly one letter.
    """
    print("\n" + "=" * 60)
    print("Example 3: Word Neighbors")
    print("=" * 60)
    
    words_to_check = ["cat", "love", "cold", "happy"]
    
    for word in words_to_check:
        neighbors = get_neighbors(word)
        print(f"\nNeighbors of '{word}' ({len(neighbors)} total):")
        # Show first 10 neighbors
        print(f"  First 10: {neighbors[:10]}")
        if len(neighbors) > 10:
            print(f"  ... and {len(neighbors) - 10} more")


def example_4_longer_ladders():
    """
    Example 4: Longer word ladders.
    
    Solve puzzles with longer words (4-5 letters).
    """
    print("\n" + "=" * 60)
    print("Example 4: Longer Word Ladders")
    print("=" * 60)
    
    puzzles = [
        ("cold", "warm"),
        ("love", "hate"),
        ("stone", "money"),
        ("happy", "sadly"),
    ]
    
    for start, end in puzzles:
        print(f"\n'{start}' → '{end}':")
        path = find_shortest_path(start, end)
        if path:
            print(f"  Path: " + " → ".join(path))
            print(f"  Length: {len(path)} steps")
        else:
            print("  No path found")


def example_5_generate_puzzles():
    """
    Example 5: Generate random puzzles.
    
    Create word ladder puzzles with configurable difficulty.
    """
    print("\n" + "=" * 60)
    print("Example 5: Generate Puzzles")
    print("=" * 60)
    
    # Generate puzzles for different word lengths
    for length in [3, 4, 5]:
        print(f"\n{length}-letter word puzzle:")
        puzzle = generate_puzzle(length=length, min_path_length=4)
        
        if puzzle:
            start, end, solution_len = puzzle
            print(f"  Start: '{start}'")
            print(f"  End: '{end}'")
            print(f"  Solution length: {solution_len} steps")
            
            # Show the solution
            solution = find_shortest_path(start, end)
            if solution:
                print(f"  Solution: " + " → ".join(solution))
        else:
            print("  Could not generate puzzle")


def example_6_difficulty_rating():
    """
    Example 6: Calculate puzzle difficulty.
    
    Analyze the difficulty of word ladder puzzles.
    """
    print("\n" + "=" * 60)
    print("Example 6: Difficulty Rating")
    print("=" * 60)
    
    puzzles = [
        ("cat", "dog"),
        ("cold", "warm"),
        ("love", "hate"),
        ("stone", "money"),
    ]
    
    print("\nDifficulty ratings (1-10 scale):")
    for start, end in puzzles:
        difficulty = get_ladder_difficulty(start, end)
        if difficulty["solvable"]:
            print(f"\n'{start}' → '{end}':")
            print(f"  Difficulty: {difficulty['difficulty']}/10")
            print(f"  Path length: {difficulty['path_length']} steps")
            print(f"  Branching factor: {difficulty['branching_factor']}")
        else:
            print(f"\n'{start}' → '{end}': Unsolvable")


def example_7_validation():
    """
    Example 7: Validate word ladders.
    
    Check if a sequence of words forms a valid ladder.
    """
    print("\n" + "=" * 60)
    print("Example 7: Validate Ladders")
    print("=" * 60)
    
    # Valid ladder
    valid_ladder = ["cat", "cot", "dot", "dog"]
    is_valid, message = validate_ladder(valid_ladder)
    print(f"\nLadder: {valid_ladder}")
    print(f"Valid: {is_valid}, Message: '{message}'")
    
    # Invalid ladder - wrong transformation
    invalid_ladder1 = ["cat", "dog"]
    is_valid, message = validate_ladder(invalid_ladder1)
    print(f"\nLadder: {invalid_ladder1}")
    print(f"Valid: {is_valid}, Message: '{message}'")
    
    # Invalid ladder - invalid word
    invalid_ladder2 = ["cat", "xyz", "dog"]
    is_valid, message = validate_ladder(invalid_ladder2)
    print(f"\nLadder: {invalid_ladder2}")
    print(f"Valid: {is_valid}, Message: '{message}'")


def example_8_custom_solver():
    """
    Example 8: Custom word dictionary.
    
    Create a solver with custom words.
    """
    print("\n" + "=" * 60)
    print("Example 8: Custom Solver")
    print("=" * 60)
    
    # Create a solver with limited words
    custom_words = {
        3: {"cat", "cot", "dot", "dog", "bat", "hat", "mat", "rat"}
    }
    solver = create_solver(custom_words=custom_words)
    
    print("\nCustom word dictionary:")
    print(f"  Words: {sorted(custom_words[3])}")
    
    # Solve in limited dictionary
    path = solver.find_shortest_path("cat", "dog")
    print(f"\nPath from 'cat' to 'dog' in custom dict:")
    if path:
        print("  " + " → ".join(path))
    
    # Word not in dictionary
    path2 = solver.find_shortest_path("cat", "fat")
    print(f"\nPath from 'cat' to 'fat' (not in dict):")
    print(f"  Result: {path2}")


def example_9_adding_words():
    """
    Example 9: Adding words dynamically.
    
    Add new words to an existing solver.
    """
    print("\n" + "=" * 60)
    print("Example 9: Adding Words Dynamically")
    print("=" * 60)
    
    # Create solver with initial words
    solver = create_solver(custom_words={3: {"cat", "dog"}})
    
    print("\nInitial dictionary:")
    print(f"  'cat' valid: {solver.is_valid_word('cat')}")
    print(f"  'bat' valid: {solver.is_valid_word('bat')}")
    
    # Add new words
    solver.add_words(["bat", "hat", "mat", "rat", "cot", "dot"])
    
    print("\nAfter adding words:")
    print(f"  'bat' valid: {solver.is_valid_word('bat')}")
    print(f"  'cot' valid: {solver.is_valid_word('cot')}")
    
    # Now can solve a path
    path = solver.find_shortest_path("cat", "dog")
    print(f"\nPath from 'cat' to 'dog':")
    if path:
        print("  " + " → ".join(path))


def example_10_game_simulation():
    """
    Example 10: Simulate a word ladder game.
    
    Show how to use the utilities in an interactive game.
    """
    print("\n" + "=" * 60)
    print("Example 10: Word Ladder Game Simulation")
    print("=" * 60)
    
    # Generate a puzzle
    puzzle = generate_puzzle(length=4, min_path_length=5)
    
    if puzzle:
        start, end, solution_len = puzzle
        print(f"\n=== WORD LADDER GAME ===")
        print(f"Transform '{start}' into '{end}'")
        print(f"Change one letter at a time!")
        print(f"Minimum steps needed: {solution_len}")
        
        # Show solution
        print("\n=== SOLUTION ===")
        solution = find_shortest_path(start, end)
        if solution:
            for i, word in enumerate(solution):
                if i == 0:
                    print(f"  Start: {word}")
                elif i == len(solution) - 1:
                    print(f"  Goal:  {word} ✓")
                else:
                    print(f"  Step {i}: {word}")
        
        # Show all possible moves at each step
        print("\n=== POSSIBLE MOVES ===")
        for word in solution[:3]:  # First 3 words
            neighbors = get_neighbors(word)
            print(f"  From '{word}': {neighbors[:8]}...")


def example_11_transformation_check():
    """
    Example 11: Check if transformation is valid.
    
    Validate individual transformations between words.
    """
    print("\n" + "=" * 60)
    print("Example 11: Transformation Validation")
    print("=" * 60)
    
    pairs = [
        ("cat", "cot"),
        ("cat", "bat"),
        ("cat", "dog"),
        ("cold", "cord"),
        ("love", "live"),
        ("love", "hate"),
    ]
    
    print("\nTransformation validity:")
    for word1, word2 in pairs:
        is_valid = is_valid_transformation(word1, word2)
        diff_count = sum(1 for c1, c2 in zip(word1, word2) if c1 != c2)
        status = "✓ Valid" if is_valid else "✗ Invalid"
        print(f"  '{word1}' → '{word2}': {status} ({diff_count} letter change)")


def example_12_word_statistics():
    """
    Example 12: Word and path statistics.
    
    Analyze statistics about word neighbors and paths.
    """
    print("\n" + "=" * 60)
    print("Example 12: Word Statistics")
    print("=" * 60)
    
    from mod import get_words_of_length
    
    # Get word count by length
    print("\nDictionary statistics:")
    for length in [3, 4, 5, 6]:
        words = get_words_of_length(length)
        print(f"  {length}-letter words: {len(words)}")
    
    # Analyze neighbor counts
    print("\nAverage neighbor count by word length:")
    for length in [3, 4, 5]:
        words = list(get_words_of_length(length))[:20]  # Sample
        avg_neighbors = sum(len(get_neighbors(w)) for w in words) / len(words)
        print(f"  {length}-letter: {avg_neighbors:.1f} average neighbors")


def run_all_examples():
    """Run all examples."""
    example_1_basic_usage()
    example_2_multiple_paths()
    example_3_neighbors()
    example_4_longer_ladders()
    example_5_generate_puzzles()
    example_6_difficulty_rating()
    example_7_validation()
    example_8_custom_solver()
    example_9_adding_words()
    example_10_game_simulation()
    example_11_transformation_check()
    example_12_word_statistics()
    
    print("\n" + "=" * 60)
    print("All examples completed!")
    print("=" * 60)


if __name__ == "__main__":
    run_all_examples()