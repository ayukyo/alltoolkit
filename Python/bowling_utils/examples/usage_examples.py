#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AllToolkit - Bowling Score Calculator Examples
================================================
Practical examples demonstrating bowling_utils module usage.

Topics covered:
1. Basic score calculation
2. Different input formats
3. Game analysis and statistics
4. Scorecard formatting
5. 10th frame special rules
6. Incomplete game handling
7. Special game types
8. Random game generation
"""

import sys
import os
# Add the bowling_utils parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from bowling_utils.mod import (
    # Parsing
    parse_score_string,
    parse_score_list,
    parse_and_analyze,
    
    # Calculation
    calculate_score,
    calculate_frame_scores,
    calculate_max_possible_score,
    quick_score,
    
    # Validation
    validate_rolls,
    validate_game_complete,
    
    # Statistics
    count_strikes,
    count_spares,
    count_gutter_rolls,
    get_game_statistics,
    
    # Analysis
    analyze_game,
    format_scorecard,
    get_frame_breakdown,
    get_game_type,
    
    # Special games
    is_perfect_game,
    is_gutter_game,
    is_all_spares,
    
    # Generators
    generate_perfect_game,
    generate_gutter_game,
    generate_all_spares_game,
    generate_random_game,
    
    # Constants
    PERFECT_GAME_SCORE,
)


def example_1_basic_score_calculation():
    """
    Example 1: Basic score calculation from different inputs.
    
    Shows how to calculate bowling scores from:
    - Roll lists
    - Score strings
    - Quick score calculation
    """
    print("=" * 60)
    print("Example 1: Basic Score Calculation")
    print("=" * 60)
    
    # Calculate from roll list
    print("\n1. From roll list (integers):")
    rolls = [10, 7, 3, 9, 0, 10, 0, 8, 8, 2, 0, 6, 10, 10, 10, 8, 1]
    score = calculate_score(rolls)
    print(f"   Rolls: {rolls}")
    print(f"   Total score: {score}")
    
    # Calculate from score string
    print("\n2. From score string:")
    score_str = "X 7/ 9- X -8 8/ -6 X X X 81"
    parsed = parse_score_string(score_str)
    score = calculate_score(parsed)
    print(f"   Score string: '{score_str}'")
    print(f"   Parsed rolls: {parsed}")
    print(f"   Total score: {score}")
    
    # Quick score calculation
    print("\n3. Quick score (one function call):")
    print(f"   String: '{score_str}' -> {quick_score(score_str)}")
    print(f"   List: {rolls} -> {quick_score(rolls)}")
    
    # Perfect game
    print("\n4. Perfect game:")
    perfect_rolls = generate_perfect_game()
    print(f"   Rolls: {perfect_rolls}")
    print(f"   Score: {calculate_score(perfect_rolls)}")
    print(f"   Is perfect: {is_perfect_game(perfect_rolls)}")


def example_2_input_formats():
    """
    Example 2: Different input formats for bowling scores.
    
    Shows how to parse:
    - Strings with various symbols (X, /, -, digits)
    - Lists with mixed types
    - Spaced and unspaced formats
    """
    print("\n" + "=" * 60)
    print("Example 2: Input Formats")
    print("=" * 60)
    
    # String formats
    print("\n1. String formats:")
    
    formats = [
        ("X X X X X X X X X XXX", "Perfect game"),
        ("-- -- -- -- -- -- -- -- -- --", "Gutter game (20 gutters)"),
        ("X 7/ 9- X -8 8/ -6 X X X 81", "Mixed game"),
        ("5/5/5/5/5/5/5/5/5/5/5", "All spares"),
        ("X X X X 5/ 9- 8/ X 7/ X 9/", "With various patterns"),
    ]
    
    for score_str, desc in formats:
        rolls = parse_score_string(score_str)
        score = calculate_score(rolls)
        print(f"   '{score_str}' ({desc})")
        print(f"   -> Rolls: {rolls}, Score: {score}")
    
    # List formats
    print("\n2. List formats:")
    
    # Integer list
    int_list = [10, 10, 10, 5, 5, 0, 0]
    print(f"   Integer list: {int_list}")
    print(f"   -> Parsed: {parse_score_list(int_list)}")
    
    # String list
    str_list = ['X', 'X', 'X', '5', '/', '-', '-']
    print(f"   String list: {str_list}")
    parsed = parse_score_list(str_list)
    print(f"   -> Parsed: {parsed}")
    
    # Mixed list
    mixed_list = [10, '5', '/', 0, 'X']
    print(f"   Mixed list: {mixed_list}")
    print(f"   -> Parsed: {parse_score_list(mixed_list)}")


def example_3_game_analysis():
    """
    Example 3: Comprehensive game analysis.
    
    Shows how to get:
    - Frame-by-frame breakdown
    - Statistics (strikes, spares, averages)
    - Game type classification
    - Detailed scorecard
    """
    print("\n" + "=" * 60)
    print("Example 3: Game Analysis")
    print("=" * 60)
    
    # Analyze a mixed game
    rolls = [10, 7, 3, 9, 0, 10, 0, 8, 8, 2, 0, 6, 10, 10, 10, 8, 1]
    
    print("\n1. Full game analysis:")
    game = analyze_game(rolls)
    
    print(f"   Total score: {game.total_score}")
    print(f"   Strikes: {game.strikes}")
    print(f"   Spares: {game.spares}")
    print(f"   Open frames: {game.open_frames}")
    print(f"   Gutter rolls: {game.gutter_rolls}")
    print(f"   Average pins/frame: {game.average_pins_per_frame:.2f}")
    print(f"   Game type: {get_game_type(rolls)}")
    print(f"   Is complete: {game.is_complete}")
    
    # Frame breakdown
    print("\n2. Frame-by-frame breakdown:")
    print(get_frame_breakdown(rolls))
    
    # Statistics
    print("\n3. Statistics dictionary:")
    stats = get_game_statistics(rolls)
    for key, value in stats.items():
        print(f"   {key}: {value}")
    
    # Scorecard
    print("\n4. Visual scorecard:")
    print(format_scorecard(rolls))


def example_4_10th_frame_rules():
    """
    Example 4: 10th frame special rules.
    
    Shows how the 10th frame works:
    - Strike: get 2 bonus rolls
    - Spare: get 1 bonus roll
    - Open: no bonus rolls
    """
    print("\n" + "=" * 60)
    print("Example 4: 10th Frame Special Rules")
    print("=" * 60)
    
    # Strike in 10th (2 bonus rolls)
    print("\n1. Strike in 10th (gets 2 bonus rolls):")
    rolls = [0] * 18 + [10, 5, 3]
    print(f"   Rolls: {rolls}")
    print(f"   Score: {calculate_score(rolls)}")
    print(format_scorecard(rolls))
    
    # Three strikes in 10th
    print("\n2. Turkey in 10th (X X X):")
    rolls = [0] * 18 + [10, 10, 10]
    print(f"   Rolls: {rolls}")
    print(f"   Score: {calculate_score(rolls)}")
    print(format_scorecard(rolls))
    
    # Spare in 10th (1 bonus roll)
    print("\n3. Spare in 10th (gets 1 bonus roll):")
    rolls = [0] * 18 + [5, 5, 7]
    print(f"   Rolls: {rolls}")
    print(f"   Score: {calculate_score(rolls)}")
    print(format_scorecard(rolls))
    
    # Open frame in 10th (no bonus)
    print("\n4. Open frame in 10th (no bonus rolls):")
    rolls = [0] * 18 + [5, 3]
    print(f"   Rolls: {rolls}")
    print(f"   Score: {calculate_score(rolls)}")
    print(format_scorecard(rolls))
    
    # Strike-spare in 10th
    print("\n5. Strike then spare in 10th (X 5/):")
    rolls = [0] * 18 + [10, 5, 5]
    print(f"   Rolls: {rolls}")
    print(f"   Score: {calculate_score(rolls)}")
    print(format_scorecard(rolls))


def example_5_incomplete_games():
    """
    Example 5: Handling incomplete games.
    
    Shows:
    - Validating incomplete games
    - Calculating partial scores
    - Maximum possible score prediction
    """
    print("\n" + "=" * 60)
    print("Example 5: Incomplete Games")
    print("=" * 60)
    
    # After first strike
    print("\n1. After first strike:")
    rolls = [10]
    is_complete, msg = validate_game_complete(rolls)
    print(f"   Rolls: {rolls}")
    print(f"   Current score: {calculate_score(rolls)}")
    print(f"   Max possible: {calculate_max_possible_score(rolls)}")
    print(f"   Complete: {is_complete} - {msg}")
    
    # After strike and spare
    print("\n2. After strike and spare:")
    rolls = [10, 5, 5]
    is_complete, msg = validate_game_complete(rolls)
    print(f"   Rolls: {rolls}")
    print(f"   Current score: {calculate_score(rolls)}")
    print(f"   Max possible: {calculate_max_possible_score(rolls)}")
    print(f"   Complete: {is_complete} - {msg}")
    
    # After 5 frames
    print("\n3. After 5 frames (mixed):")
    rolls = [10, 7, 3, 9, 0, 10, 0, 8, 8, 2]
    is_complete, msg = validate_game_complete(rolls)
    print(f"   Rolls: {rolls}")
    print(f"   Current score: {calculate_score(rolls)}")
    print(f"   Max possible: {calculate_max_possible_score(rolls)}")
    print(f"   Complete: {is_complete} - {msg}")
    
    # After open frame (cannot get perfect)
    print("\n4. After open frame (perfect game impossible):")
    rolls = [5, 3]
    max_score = calculate_max_possible_score(rolls)
    print(f"   Rolls: {rolls}")
    print(f"   Current score: {calculate_score(rolls)}")
    print(f"   Max possible: {max_score} (lost {PERFECT_GAME_SCORE - max_score} points)")


def example_6_special_game_types():
    """
    Example 6: Special game types.
    
    Shows:
    - Perfect game (300)
    - Gutter game (0)
    - All spares (150)
    - Game type classification
    """
    print("\n" + "=" * 60)
    print("Example 6: Special Game Types")
    print("=" * 60)
    
    # Perfect game
    print("\n1. Perfect Game (300):")
    rolls = generate_perfect_game()
    print(f"   Rolls: {rolls}")
    print(f"   Score: {calculate_score(rolls)}")
    print(f"   Type: {get_game_type(rolls)}")
    print(f"   Is perfect: {is_perfect_game(rolls)}")
    print(format_scorecard(rolls))
    
    # Gutter game
    print("\n2. Gutter Game (0):")
    rolls = generate_gutter_game()
    print(f"   Rolls: {rolls}")
    print(f"   Score: {calculate_score(rolls)}")
    print(f"   Type: {get_game_type(rolls)}")
    print(f"   Is gutter: {is_gutter_game(rolls)}")
    print(format_scorecard(rolls))
    
    # All spares
    print("\n3. All Spares (150):")
    rolls = generate_all_spares_game(5)
    print(f"   Rolls: {rolls}")
    print(f"   Score: {calculate_score(rolls)}")
    print(f"   Type: {get_game_type(rolls)}")
    print(f"   Is all spares: {is_all_spares(rolls)}")
    print(format_scorecard(rolls))
    
    # Different spare configurations
    print("\n4. All Spares with different first pins:")
    for first_pin in [1, 3, 5, 7, 9]:
        rolls = generate_all_spares_game(first_pin)
        score = calculate_score(rolls)
        print(f"   First pin: {first_pin} -> Score: {score}")
    
    # All open frames
    print("\n5. All Open Frames:")
    rolls = [9, 0] * 10  # 9-pin open frames
    print(f"   Rolls: {rolls}")
    print(f"   Score: {calculate_score(rolls)}")
    print(f"   Type: {get_game_type(rolls)}")


def example_7_random_games():
    """
    Example 7: Generating random games.
    
    Shows:
    - Random game generation
    - Customizing strike/spare probabilities
    - Analyzing random games
    """
    print("\n" + "=" * 60)
    print("Example 7: Random Game Generation")
    print("=" * 60)
    
    # Default random game
    print("\n1. Default random game (20% strikes, 30% spares):")
    game = generate_random_game()
    print(f"   Rolls: {game}")
    print(f"   Score: {calculate_score(game)}")
    print(f"   Type: {get_game_type(game)}")
    print(format_scorecard(game))
    
    # High strike probability
    print("\n2. High strike probability (80% strikes):")
    game = generate_random_game(strike_prob=0.8, spare_prob=0.2)
    stats = get_game_statistics(game)
    print(f"   Score: {stats['total_score']}")
    print(f"   Strikes: {stats['strikes']}")
    print(f"   Spares: {stats['spares']}")
    
    # High spare probability
    print("\n3. High spare probability (80% spares):")
    game = generate_random_game(strike_prob=0.1, spare_prob=0.8)
    stats = get_game_statistics(game)
    print(f"   Score: {stats['total_score']}")
    print(f"   Strikes: {stats['strikes']}")
    print(f"   Spares: {stats['spares']}")
    
    # Low everything (mostly open frames)
    print("\n4. Mostly open frames (5% strikes, 10% spares):")
    game = generate_random_game(strike_prob=0.05, spare_prob=0.1)
    stats = get_game_statistics(game)
    print(f"   Score: {stats['total_score']}")
    print(f"   Open frames: {stats['open_frames']}")


def example_8_validation():
    """
    Example 8: Input validation.
    
    Shows:
    - Validating roll values
    - Validating frame totals
    - Checking game completeness
    - Error handling
    """
    print("\n" + "=" * 60)
    print("Example 8: Input Validation")
    print("=" * 60)
    
    # Valid games
    print("\n1. Valid games:")
    valid_games = [
        ([10] * 12, "Perfect game"),
        ([0] * 20, "Gutter game"),
        ([5, 5] * 10 + [5], "All spares"),
    ]
    
    for rolls, desc in valid_games:
        is_valid = validate_rolls(rolls)
        is_complete, msg = validate_game_complete(rolls)
        print(f"   {desc}: Valid={is_valid}, Complete={is_complete}")
    
    # Invalid games
    print("\n2. Invalid games:")
    
    # Too many pins in frame
    print("   Frame > 10 pins:")
    try:
        calculate_score([6, 6])
    except ValueError as e:
        print(f"   Error: {e}")
    
    # Invalid pin count
    print("   Invalid pin count (> 10):")
    try:
        calculate_score([11])
    except ValueError as e:
        print(f"   Error: {e}")
    
    # Invalid string format
    print("   Invalid string format:")
    try:
        parse_score_string("ABC")
    except ValueError as e:
        print(f"   Error: {e}")
    
    # Invalid spare (strike followed by spare)
    print("   Invalid spare sequence:")
    try:
        parse_score_string("X/")
    except ValueError as e:
        print(f"   Error: {e}")


def example_9_statistics():
    """
    Example 9: Detailed statistics.
    
    Shows:
    - Strike/spare counts
    - Gutter roll counts
    - Average calculations
    - Complete statistics dictionary
    """
    print("\n" + "=" * 60)
    print("Example 9: Detailed Statistics")
    print("=" * 60)
    
    # Various games with statistics
    games = [
        (generate_perfect_game(), "Perfect Game"),
        (generate_gutter_game(), "Gutter Game"),
        (generate_all_spares_game(5), "All Spares"),
        ([10, 7, 3, 9, 0] * 3 + [10, 10, 10, 8, 1], "Mixed Game"),
    ]
    
    for rolls, desc in games:
        print(f"\n{desc}:")
        stats = get_game_statistics(rolls)
        
        print(f"   Total score: {stats['total_score']}")
        print(f"   Strikes: {stats['strikes']}")
        print(f"   Spares: {stats['spares']}")
        print(f"   Open frames: {stats['open_frames']}")
        print(f"   Gutter rolls: {stats['gutter_rolls']}")
        print(f"   Avg pins/frame: {stats['average_pins_per_frame']:.2f}")
        print(f"   Is perfect: {stats['is_perfect']}")
        print(f"   Is gutter game: {stats['is_gutter_game']}")
        print(f"   Max possible: {stats['max_possible_score']}")
        print(f"   Complete: {stats['is_complete']}")


def example_10_common_patterns():
    """
    Example 10: Common bowling patterns and their scores.
    
    Shows:
    - Turkey (3 strikes in a row)
    - Double (2 strikes in a row)
    - Dutch 200 (strike-spare pattern)
    - Various game patterns
    """
    print("\n" + "=" * 60)
    print("Example 10: Common Bowling Patterns")
    print("=" * 60)
    
    # Turkey
    print("\n1. Turkey (3 consecutive strikes):")
    rolls = [10, 10, 10] + [0] * 14
    frames = calculate_frame_scores(rolls)
    print(f"   Frame 1 (Strike): {frames[0].frame_score} (10 + 10 + 10)")
    print(f"   Frame 2 (Strike): {frames[1].frame_score} (10 + 10 + 0)")
    print(f"   Frame 3 (Strike): {frames[2].frame_score} (10 + 0 + 0)")
    print(f"   Total: {calculate_score(rolls)}")
    
    # Dutch 200 (alternating strike-spare)
    print("\n2. Dutch 200 pattern (X, spare, X, spare...):")
    rolls = []
    for _ in range(5):
        rolls.extend([10, 5, 5])
    print(f"   Rolls: {rolls}")
    print(f"   Score: {calculate_score(rolls)}")
    print(format_scorecard(rolls))
    
    # All strikes except one spare
    print("\n3. Almost perfect (one spare):")
    rolls = [10] * 9 + [5, 5, 10]
    print(f"   Rolls: {rolls}")
    print(f"   Score: {calculate_score(rolls)}")
    print(format_scorecard(rolls))
    
    # 7-10 split (open frame pattern)
    print("\n4. All 7-10 splits (worst consistent open):")
    rolls = [7, 0] * 10
    print(f"   Rolls: {rolls}")
    print(f"   Score: {calculate_score(rolls)}")


def main():
    """Run all examples."""
    print("\n" + "=" * 60)
    print("BOWLING SCORE CALCULATOR - USAGE EXAMPLES")
    print("=" * 60)
    
    example_1_basic_score_calculation()
    example_2_input_formats()
    example_3_game_analysis()
    example_4_10th_frame_rules()
    example_5_incomplete_games()
    example_6_special_game_types()
    example_7_random_games()
    example_8_validation()
    example_9_statistics()
    example_10_common_patterns()
    
    print("\n" + "=" * 60)
    print("All examples completed!")
    print("=" * 60)


if __name__ == "__main__":
    main()