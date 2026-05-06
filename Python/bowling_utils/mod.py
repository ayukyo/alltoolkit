#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AllToolkit - Bowling Score Calculator Utilities
=================================================
A comprehensive bowling score calculation utility module for Python with zero external dependencies.

Features:
    - Parse bowling scores from various formats (string, list, tuple)
    - Calculate total score with proper strike/spare handling
    - Validate bowling game input
    - Frame-by-frame score breakdown
    - Perfect game (300) and gutter game (0) detection
    - Maximum possible score from current state
    - Bowling game statistics (strikes, spares, average pins per frame)
    - Support for 10th frame special rules
    - Detailed error messages for invalid inputs

Author: AllToolkit Contributors
License: MIT
"""

from typing import List, Tuple, Optional, Union, Dict
from dataclasses import dataclass
import re


# ============================================================================
# Constants
# ============================================================================

TOTAL_FRAMES = 10
MAX_PINS_PER_FRAME = 10
MAX_PINS_PER_ROLL = 10
PERFECT_GAME_SCORE = 300
GUTTER_GAME_SCORE = 0

# Symbols for display
STRIKE_SYMBOL = 'X'
SPARE_SYMBOL = '/'
GUTTER_SYMBOL = '-'
MISS_SYMBOL = '-'

# Pre-compiled regex for score string parsing
_SCORE_PATTERN = re.compile(r'^[0-9Xx/-]+$')


# ============================================================================
# Data Classes
# ============================================================================

@dataclass
class FrameScore:
    """Container for a single frame's score information."""
    frame_number: int
    rolls: List[int]  # Pins knocked down in each roll
    roll_symbols: List[str]  # Symbols for display (X, /, digits)
    frame_score: int  # Score for this frame (cumulative)
    frame_pins: int  # Pins knocked down in this frame only
    is_strike: bool
    is_spare: bool
    is_open: bool
    bonus_rolls: List[int]  # Bonus rolls counted for strike/spare


@dataclass
class BowlingGame:
    """Container for a complete bowling game."""
    frames: List[FrameScore]
    total_score: int
    strikes: int  # Total number of strikes
    spares: int  # Total number of spares
    open_frames: int  # Total number of open frames
    gutter_rolls: int  # Total number of gutter rolls (0 pins)
    is_perfect: bool  # True if score is 300
    is_gutter_game: bool  # True if score is 0
    average_pins_per_frame: float
    max_possible_score: int  # Maximum possible score from current state
    is_complete: bool  # True if game has all required rolls


# ============================================================================
# Input Parsing Functions
# ============================================================================

def parse_roll_symbol(symbol: str) -> int:
    """
    Parse a single roll symbol to pins knocked down.
    
    Args:
        symbol: Single character representing a roll.
                Valid symbols: X, x (strike), / (spare), - (gutter), 0-9 (pins)
    
    Returns:
        Number of pins knocked down (0-10).
    
    Raises:
        ValueError: If symbol is invalid.
    
    Examples:
        >>> parse_roll_symbol('X')
        10
        >>> parse_roll_symbol('/')
        10  # Context-dependent (spare means 10 minus previous roll)
        >>> parse_roll_symbol('5')
        5
        >>> parse_roll_symbol('-')
        0
    """
    symbol = symbol.upper().strip()
    
    if symbol == 'X':
        return 10
    elif symbol == '/':
        return 10  # Will be adjusted based on previous roll context
    elif symbol == '-' or symbol == '0':
        return 0
    elif symbol.isdigit():
        pins = int(symbol)
        if pins < 0 or pins > 10:
            raise ValueError(f"Invalid pin count: {symbol}")
        return pins
    else:
        raise ValueError(f"Invalid roll symbol: {symbol}")


def parse_score_string(score_str: str) -> List[int]:
    """
    Parse a bowling score string to a list of pins knocked down per roll.
    
    Supports various formats:
    - 'X' for strikes
    - '/' for spares (calculated from previous roll)
    - '-' for gutters (0 pins)
    - '0-9' for specific pin counts
    - Spaces and separators are ignored
    
    Args:
        score_str: String representation of bowling game.
                   Examples: "X X X X X X X X X XXX", "12 34 5/", "X- 5/ 12"
    
    Returns:
        List of pins knocked down in each roll.
    
    Raises:
        ValueError: If score string is invalid.
    
    Examples:
        >>> parse_score_string("X X X X X X X X X XXX")  # Perfect game
        [10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10]
        >>> parse_score_string("12 3/ X 45")  # Mixed
        [1, 2, 3, 7, 10, 4, 5]
    """
    # Remove spaces and separators, but keep the bowling symbols
    score_str = score_str.upper().strip()
    
    # Validate the string format
    if not _SCORE_PATTERN.match(score_str.replace(' ', '')):
        raise ValueError(f"Invalid score string format: {score_str}")
    
    # Remove spaces
    score_str = score_str.replace(' ', '')
    
    rolls = []
    prev_pins = 0
    
    for i, symbol in enumerate(score_str):
        if symbol == '/':
            # Spare: pins knocked down = 10 - previous roll
            spare_pins = 10 - prev_pins
            if spare_pins <= 0 or spare_pins > 10:
                raise ValueError(f"Invalid spare at position {i}: previous roll was {prev_pins}")
            rolls.append(spare_pins)
            prev_pins = spare_pins
        else:
            pins = parse_roll_symbol(symbol)
            rolls.append(pins)
            prev_pins = pins
    
    return rolls


def parse_score_list(score_list: List[Union[int, str]]) -> List[int]:
    """
    Parse a list of scores to a list of pins knocked down per roll.
    
    Handles mixed input with integers and string symbols.
    
    Args:
        score_list: List of roll values (int or str).
                   Examples: [10, 10, 10], ['X', 'X', 'X'], [1, 2, 3, '/']
    
    Returns:
        List of pins knocked down in each roll.
    
    Raises:
        ValueError: If any element is invalid.
    
    Examples:
        >>> parse_score_list([10, 10, 10])
        [10, 10, 10]
        >>> parse_score_list(['X', '/', '5'])
        [10, 10, 5]  # '/' = 10 pins (spare value)
    """
    rolls = []
    prev_pins = 0
    
    for i, item in enumerate(score_list):
        if isinstance(item, int):
            if item < 0 or item > 10:
                raise ValueError(f"Invalid pin count at index {i}: {item}")
            rolls.append(item)
            prev_pins = item
        elif isinstance(item, str):
            pins = parse_roll_symbol(item)
            if item.upper() == '/':
                # Adjust spare value based on previous roll
                spare_pins = 10 - prev_pins
                if spare_pins <= 0:
                    raise ValueError(f"Invalid spare at index {i}: previous roll was {prev_pins}")
                rolls.append(spare_pins)
                prev_pins = spare_pins
            else:
                rolls.append(pins)
                prev_pins = pins
        else:
            raise ValueError(f"Invalid type at index {i}: {type(item)}")
    
    return rolls


# ============================================================================
# Validation Functions
# ============================================================================

def validate_rolls(rolls: List[int]) -> bool:
    """
    Validate that a list of rolls represents a valid bowling game.
    
    Checks:
    - Each roll is between 0-10
    - Frame pin totals are valid (max 10 per frame, except 10th)
    - 10th frame rules are correct (bonus rolls for strike/spare)
    - Correct number of rolls
    
    Args:
        rolls: List of pins knocked down per roll.
    
    Returns:
        True if valid, False otherwise.
    
    Examples:
        >>> validate_rolls([10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10])
        True
        >>> validate_rolls([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
        False  # Too many rolls for gutter game
    """
    if not rolls:
        return False
    
    # Check each roll is valid
    for roll in rolls:
        if roll < 0 or roll > 10:
            return False
    
    # Simulate frame-by-frame to validate
    frame = 1
    roll_idx = 0
    
    while frame <= TOTAL_FRAMES and roll_idx < len(rolls):
        if frame < 10:  # Frames 1-9
            first_roll = rolls[roll_idx]
            roll_idx += 1
            
            if first_roll == 10:  # Strike
                frame += 1
            else:
                if roll_idx >= len(rolls):
                    return True  # Incomplete game is still valid input
                
                second_roll = rolls[roll_idx]
                roll_idx += 1
                
                # Check frame total
                if first_roll + second_roll > 10:
                    return False
                
                frame += 1
        else:  # 10th frame
            first_roll = rolls[roll_idx]
            roll_idx += 1
            
            if roll_idx >= len(rolls):
                return True  # Incomplete
            
            second_roll = rolls[roll_idx]
            roll_idx += 1
            
            # Check second roll validity
            if first_roll != 10:  # Not a strike
                if first_roll + second_roll > 10:
                    return False
            
            # Check if bonus rolls are needed and present
            if first_roll == 10:  # Strike in 10th
                # Need at least 2 more rolls
                if roll_idx >= len(rolls):
                    return True  # Incomplete
                
                third_roll = rolls[roll_idx]
                roll_idx += 1
                
                if third_roll == 10:  # Another strike
                    if roll_idx >= len(rolls):
                        return True  # Incomplete (could have 4th for 3 strikes)
                    # Can have one more roll
                elif roll_idx < len(rolls):
                    fourth_roll = rolls[roll_idx]
                    # Check third + fourth combination
                    if third_roll + fourth_roll > 10:
                        return False
                    roll_idx += 1
            elif first_roll + second_roll == 10:  # Spare in 10th
                # Need one more roll
                if roll_idx >= len(rolls):
                    return True  # Incomplete
                roll_idx += 1  # Third roll
            else:  # Open frame
                # No bonus rolls needed
                pass
            
            frame += 1
    
    return True


def validate_game_complete(rolls: List[int]) -> Tuple[bool, str]:
    """
    Check if a bowling game is complete (all required rolls present).
    
    Args:
        rolls: List of pins knocked down per roll.
    
    Returns:
        Tuple of (is_complete, status_message).
    
    Examples:
        >>> validate_game_complete([10] * 12)  # Perfect game
        (True, 'Game complete')
        >>> validate_game_complete([5, 5] * 10 + [5])  # Spare game incomplete
        (False, 'Waiting for 1 bonus roll')
    """
    if not rolls:
        return (False, "No rolls recorded")
    
    roll_idx = 0
    frame = 1
    
    while frame <= TOTAL_FRAMES:
        if roll_idx >= len(rolls):
            return (False, f"Waiting for roll in frame {frame}")
        
        if frame < 10:
            first_roll = rolls[roll_idx]
            roll_idx += 1
            
            if first_roll == 10:  # Strike
                frame += 1
            else:
                if roll_idx >= len(rolls):
                    return (False, f"Waiting for second roll in frame {frame}")
                
                second_roll = rolls[roll_idx]
                roll_idx += 1
                
                if first_roll + second_roll > 10:
                    return (False, f"Invalid frame {frame}: too many pins")
                
                frame += 1
        else:  # 10th frame
            first_roll = rolls[roll_idx]
            roll_idx += 1
            
            if roll_idx >= len(rolls):
                return (False, "Waiting for second roll in frame 10")
            
            second_roll = rolls[roll_idx]
            roll_idx += 1
            
            if first_roll == 10:  # Strike in 10th
                # Check second roll validity (can be strike)
                if roll_idx >= len(rolls):
                    return (False, "Waiting for bonus roll after strike")
                
                third_roll = rolls[roll_idx]
                roll_idx += 1
                
                if third_roll == 10:  # Third strike
                    # Can optionally have more for X X X X pattern
                    pass
                elif roll_idx < len(rolls):
                    # Check if third + fourth is valid spare
                    pass
            elif first_roll + second_roll == 10:  # Spare in 10th
                if roll_idx >= len(rolls):
                    return (False, "Waiting for bonus roll after spare")
                roll_idx += 1
            # Open frame: game complete
            
            frame += 1
    
    return (True, "Game complete")


# ============================================================================
# Score Calculation Functions
# ============================================================================

def calculate_score(rolls: List[int]) -> int:
    """
    Calculate the total bowling score from a list of rolls.
    
    Properly handles:
    - Strikes: 10 + next 2 rolls
    - Spares: 10 + next 1 roll
    - 10th frame bonus rolls
    - Incomplete games
    
    Args:
        rolls: List of pins knocked down per roll.
    
    Returns:
        Total score (0-300 for complete game).
    
    Raises:
        ValueError: If rolls are invalid.
    
    Examples:
        >>> calculate_score([10] * 12)  # Perfect game
        300
        >>> calculate_score([0] * 20)  # Gutter game
        0
        >>> calculate_score([5, 5] * 10 + [5])  # All spares
        150
        >>> calculate_score([9, 0] * 10)  # All 9-pin open frames
        90
    """
    if not rolls:
        return 0
    
    # Validate basic roll values
    for roll in rolls:
        if roll < 0 or roll > 10:
            raise ValueError(f"Invalid roll value: {roll}")
    
    score = 0
    roll_idx = 0
    frame = 1
    
    while frame <= TOTAL_FRAMES and roll_idx < len(rolls):
        if frame < 10:  # Frames 1-9
            first_roll = rolls[roll_idx]
            
            if first_roll == 10:  # Strike
                # Add strike (10) + bonus from next 2 rolls
                bonus1 = rolls[roll_idx + 1] if roll_idx + 1 < len(rolls) else 0
                bonus2 = rolls[roll_idx + 2] if roll_idx + 2 < len(rolls) else 0
                
                # Special case: if bonus1 is a strike, bonus2 counts properly
                score += 10 + bonus1 + bonus2
                roll_idx += 1
            else:
                second_roll = rolls[roll_idx + 1] if roll_idx + 1 < len(rolls) else 0
                
                # Validate frame total
                if first_roll + second_roll > 10:
                    raise ValueError(f"Invalid frame {frame}: {first_roll} + {second_roll} > 10")
                
                if first_roll + second_roll == 10:  # Spare
                    bonus = rolls[roll_idx + 2] if roll_idx + 2 < len(rolls) else 0
                    score += 10 + bonus
                else:  # Open frame
                    score += first_roll + second_roll
                
                roll_idx += 2
            
            frame += 1
        else:  # 10th frame
            # Just sum remaining rolls
            remaining_rolls = rolls[roll_idx:]
            
            # Validate 10th frame structure
            if len(remaining_rolls) < 2:
                # Incomplete, just sum what we have
                score += sum(remaining_rolls)
            elif remaining_rolls[0] == 10:  # Strike in 10th
                # Need at least 3 rolls
                score += sum(remaining_rolls[:3]) if len(remaining_rolls) >= 3 else sum(remaining_rolls)
            elif remaining_rolls[0] + remaining_rolls[1] == 10:  # Spare in 10th
                # Need at least 3 rolls
                score += sum(remaining_rolls[:3]) if len(remaining_rolls) >= 3 else sum(remaining_rolls)
            else:  # Open frame
                score += remaining_rolls[0] + remaining_rolls[1]
            
            frame += 1
    
    return min(score, PERFECT_GAME_SCORE)


def calculate_frame_scores(rolls: List[int]) -> List[FrameScore]:
    """
    Calculate detailed frame-by-frame scores.
    
    Args:
        rolls: List of pins knocked down per roll.
    
    Returns:
        List of FrameScore objects for each frame.
    
    Examples:
        >>> frames = calculate_frame_scores([10, 10, 10])
        >>> frames[0].frame_score  # Cumulative score after frame 1
        30
    """
    if not rolls:
        return []
    
    frames = []
    roll_idx = 0
    cumulative_score = 0
    
    for frame_num in range(1, TOTAL_FRAMES + 1):
        if roll_idx >= len(rolls):
            break
        
        frame_rolls = []
        roll_symbols = []
        bonus_rolls = []
        is_strike = False
        is_spare = False
        is_open = False
        
        if frame_num < 10:  # Frames 1-9
            first_roll = rolls[roll_idx]
            
            if first_roll == 10:  # Strike
                frame_rolls = [10]
                roll_symbols = [STRIKE_SYMBOL]
                is_strike = True
                
                # Get bonus rolls
                bonus1 = rolls[roll_idx + 1] if roll_idx + 1 < len(rolls) else 0
                bonus2 = rolls[roll_idx + 2] if roll_idx + 2 < len(rolls) else 0
                bonus_rolls = [bonus1, bonus2]
                
                frame_pins = 10
                cumulative_score += 10 + bonus1 + bonus2
                roll_idx += 1
            else:
                second_roll = rolls[roll_idx + 1] if roll_idx + 1 < len(rolls) else 0
                frame_rolls = [first_roll, second_roll]
                
                if first_roll == 0:
                    roll_symbols.append(GUTTER_SYMBOL)
                else:
                    roll_symbols.append(str(first_roll))
                
                if first_roll + second_roll == 10:  # Spare
                    roll_symbols.append(SPARE_SYMBOL)
                    is_spare = True
                    
                    bonus = rolls[roll_idx + 2] if roll_idx + 2 < len(rolls) else 0
                    bonus_rolls = [bonus]
                    cumulative_score += 10 + bonus
                else:  # Open frame
                    if second_roll == 0:
                        roll_symbols.append(GUTTER_SYMBOL)
                    else:
                        roll_symbols.append(str(second_roll))
                    is_open = True
                    cumulative_score += first_roll + second_roll
                
                frame_pins = first_roll + second_roll
                roll_idx += 2
        else:  # 10th frame
            remaining_rolls = rolls[roll_idx:]
            
            first_roll = remaining_rolls[0] if remaining_rolls else 0
            second_roll = remaining_rolls[1] if len(remaining_rolls) > 1 else 0
            
            frame_rolls = [first_roll]
            
            if first_roll == 10:  # Strike
                roll_symbols = [STRIKE_SYMBOL]
                is_strike = True
                
                third_roll = remaining_rolls[2] if len(remaining_rolls) > 2 else 0
                frame_rolls.append(second_roll)
                frame_rolls.append(third_roll)
                
                # Add symbols for bonus rolls
                if second_roll == 10:
                    roll_symbols.append(STRIKE_SYMBOL)
                elif second_roll == 0:
                    roll_symbols.append(GUTTER_SYMBOL)
                else:
                    roll_symbols.append(str(second_roll))
                
                if len(remaining_rolls) > 2:
                    if third_roll == 10:
                        roll_symbols.append(STRIKE_SYMBOL)
                    elif second_roll + third_roll == 10 and second_roll != 10:
                        roll_symbols.append(SPARE_SYMBOL)
                    elif third_roll == 0:
                        roll_symbols.append(GUTTER_SYMBOL)
                    else:
                        roll_symbols.append(str(third_roll))
                
                frame_pins = sum(frame_rolls)
                cumulative_score += sum(frame_rolls)
            elif first_roll + second_roll == 10:  # Spare
                roll_symbols = [str(first_roll) if first_roll > 0 else GUTTER_SYMBOL, SPARE_SYMBOL]
                is_spare = True
                
                third_roll = remaining_rolls[2] if len(remaining_rolls) > 2 else 0
                frame_rolls.append(second_roll)
                frame_rolls.append(third_roll)
                
                if third_roll == 10:
                    roll_symbols.append(STRIKE_SYMBOL)
                elif third_roll == 0:
                    roll_symbols.append(GUTTER_SYMBOL)
                else:
                    roll_symbols.append(str(third_roll))
                
                frame_pins = sum(frame_rolls)
                cumulative_score += sum(frame_rolls)
            else:  # Open frame
                roll_symbols = [
                    str(first_roll) if first_roll > 0 else GUTTER_SYMBOL,
                    str(second_roll) if second_roll > 0 else GUTTER_SYMBOL
                ]
                is_open = True
                frame_rolls.append(second_roll)
                frame_pins = first_roll + second_roll
                cumulative_score += frame_pins
        
        frames.append(FrameScore(
            frame_number=frame_num,
            rolls=frame_rolls,
            roll_symbols=roll_symbols,
            frame_score=min(cumulative_score, PERFECT_GAME_SCORE),
            frame_pins=min(frame_pins, 10) if frame_num < 10 else frame_pins,
            is_strike=is_strike,
            is_spare=is_spare,
            is_open=is_open,
            bonus_rolls=bonus_rolls
        ))
    
    return frames


def calculate_max_possible_score(rolls: List[int]) -> int:
    """
    Calculate the maximum possible score given current rolls.
    
    Assumes remaining rolls are strikes.
    
    Args:
        rolls: Current rolls in the game.
    
    Returns:
        Maximum possible final score.
    
    Examples:
        >>> calculate_max_possible_score([10, 10, 10])  # After 3 strikes
        300  # Still possible to get perfect game
        >>> calculate_max_possible_score([])  # Empty game
        300  # Perfect game possible
    """
    if not rolls:
        return PERFECT_GAME_SCORE
    
    # First, check if perfect game is still possible
    # Perfect game requires ALL strikes (no spares or open frames)
    roll_idx = 0
    frame = 1
    all_strikes = True
    
    while frame <= TOTAL_FRAMES and roll_idx < len(rolls):
        if frame < 10:
            first_roll = rolls[roll_idx]
            roll_idx += 1
            
            if first_roll == 10:  # Strike
                frame += 1
            else:
                # Not a strike - perfect game impossible
                all_strikes = False
                if roll_idx >= len(rolls):
                    frame += 1
                    break
                else:
                    roll_idx += 1  # Consume second roll
                    frame += 1
        else:  # 10th frame
            break
    
    if all_strikes:
        return PERFECT_GAME_SCORE
    
    # If perfect not possible, calculate approximate max
    current_score = calculate_score(rolls)
    
    # Count remaining frames
    remaining_frames = TOTAL_FRAMES - frame + 1
    
    # Each remaining frame can contribute up to 30 (if strike)
    remaining_max = remaining_frames * 30
    
    return min(current_score + remaining_max, PERFECT_GAME_SCORE)


# ============================================================================
# Statistics Functions
# ============================================================================

def count_strikes(rolls: List[int]) -> int:
    """
    Count the total number of strikes in a game.
    
    Args:
        rolls: List of pins knocked down per roll.
    
    Returns:
        Number of strikes (0-12 for complete game).
    
    Examples:
        >>> count_strikes([10] * 12)
        12
        >>> count_strikes([5, 5, 10, 3, 7])
        1
    """
    return sum(1 for roll in rolls if roll == 10)


def count_spares(rolls: List[int]) -> int:
    """
    Count the total number of spares in a game.
    
    Note: Spares in 10th frame bonus rolls are counted separately.
    
    Args:
        rolls: List of pins knocked down per roll.
    
    Returns:
        Number of spares (0-10 for complete game).
    
    Examples:
        >>> count_spares([5, 5] * 10 + [5])
        10
    """
    spares = 0
    roll_idx = 0
    frame = 1
    
    while frame <= TOTAL_FRAMES and roll_idx < len(rolls) - 1:
        if frame < 10:
            first_roll = rolls[roll_idx]
            
            if first_roll == 10:  # Strike
                roll_idx += 1
            else:
                second_roll = rolls[roll_idx + 1]
                if first_roll + second_roll == 10 and first_roll != 10:
                    spares += 1
                roll_idx += 2
            
            frame += 1
        else:  # 10th frame
            first_roll = rolls[roll_idx]
            second_roll = rolls[roll_idx + 1] if roll_idx + 1 < len(rolls) else 0
            
            if first_roll != 10 and first_roll + second_roll == 10:
                spares += 1
            
            break
    
    return spares


def count_gutter_rolls(rolls: List[int]) -> int:
    """
    Count the number of gutter rolls (0 pins knocked down).
    
    Args:
        rolls: List of pins knocked down per roll.
    
    Returns:
        Number of gutter rolls.
    
    Examples:
        >>> count_gutter_rolls([0, 0, 0, 0])
        4
        >>> count_gutter_rolls([10, 5, 0])
        1
    """
    return sum(1 for roll in rolls if roll == 0)


def get_game_statistics(rolls: List[int]) -> Dict[str, Union[int, float]]:
    """
    Get comprehensive statistics for a bowling game.
    
    Args:
        rolls: List of pins knocked down per roll.
    
    Returns:
        Dictionary with game statistics.
    
    Examples:
        >>> stats = get_game_statistics([10] * 12)
        >>> stats['strikes']
        12
        >>> stats['is_perfect']
        True
    """
    frames = calculate_frame_scores(rolls)
    total_score = calculate_score(rolls)
    strikes = count_strikes(rolls)
    spares = count_spares(rolls)
    gutter_rolls = count_gutter_rolls(rolls)
    open_frames = sum(1 for f in frames if f.is_open)
    
    is_complete, _ = validate_game_complete(rolls)
    
    return {
        'total_score': total_score,
        'strikes': strikes,
        'spares': spares,
        'open_frames': open_frames,
        'gutter_rolls': gutter_rolls,
        'is_perfect': total_score == PERFECT_GAME_SCORE,
        'is_gutter_game': total_score == GUTTER_GAME_SCORE,
        'average_pins_per_frame': total_score / len(frames) if frames else 0,
        'max_possible_score': calculate_max_possible_score(rolls),
        'is_complete': is_complete,
        'frames_played': len(frames),
    }


# ============================================================================
# Game Analysis Functions
# ============================================================================

def analyze_game(rolls: List[int]) -> BowlingGame:
    """
    Perform complete analysis of a bowling game.
    
    Args:
        rolls: List of pins knocked down per roll.
    
    Returns:
        BowlingGame object with complete game information.
    
    Examples:
        >>> game = analyze_game([10] * 12)
        >>> game.is_perfect
        True
        >>> game.total_score
        300
    """
    frames = calculate_frame_scores(rolls)
    stats = get_game_statistics(rolls)
    is_complete, _ = validate_game_complete(rolls)
    
    return BowlingGame(
        frames=frames,
        total_score=stats['total_score'],
        strikes=stats['strikes'],
        spares=stats['spares'],
        open_frames=stats['open_frames'],
        gutter_rolls=stats['gutter_rolls'],
        is_perfect=stats['is_perfect'],
        is_gutter_game=stats['is_gutter_game'],
        average_pins_per_frame=stats['average_pins_per_frame'],
        max_possible_score=stats['max_possible_score'],
        is_complete=is_complete,
    )


def format_scorecard(rolls: List[int], show_cumulative: bool = True) -> str:
    """
    Format a bowling scorecard for display.
    
    Creates a visual representation of the bowling game.
    
    Args:
        rolls: List of pins knocked down per roll.
        show_cumulative: Whether to show cumulative scores.
    
    Returns:
        Formatted scorecard string.
    
    Examples:
        >>> print(format_scorecard([10] * 12))
        |  1  |  2  |  3  |  4  |  5  |  6  |  7  |  8  |  9  |   10   |
        |  X  |  X  |  X  |  X  |  X  |  X  |  X  |  X  |  X  | X X X |
        |  30 |  60 |  90 | 120 | 150 | 180 | 210 | 240 | 270 |  300  |
    """
    frames = calculate_frame_scores(rolls)
    
    if not frames:
        return "No frames recorded"
    
    # Header
    header = "|  1  |  2  |  3  |  4  |  5  |  6  |  7  |  8  |  9  |   10   |"
    
    # Rolls row
    rolls_row = ""
    for i, frame in enumerate(frames):
        symbols = "".join(frame.roll_symbols)
        if i < 9:  # Frames 1-9
            rolls_row += f"| {symbols:^3} |"
        else:  # Frame 10
            rolls_row += f"| {symbols:^7} |"
    
    # Score row
    if show_cumulative:
        score_row = ""
        for i, frame in enumerate(frames):
            score = frame.frame_score
            if i < 9:
                score_row += f"| {score:^3} |"
            else:
                score_row += f"| {score:^7} |"
        
        return f"{header}\n{rolls_row}\n{score_row}"
    
    return f"{header}\n{rolls_row}"


def get_frame_breakdown(rolls: List[int]) -> str:
    """
    Get a detailed text breakdown of each frame.
    
    Args:
        rolls: List of pins knocked down per roll.
    
    Returns:
        Detailed breakdown string.
    
    Examples:
        >>> print(get_frame_breakdown([10, 5, 5, 3, 4]))
        Frame 1: Strike (10) + bonus [5, 5] = 20
        Frame 2: Spare (5 + 5) + bonus [3] = 13
        Frame 3: Open (3 + 4) = 7
    """
    frames = calculate_frame_scores(rolls)
    
    if not frames:
        return "No frames recorded"
    
    breakdown = []
    cumulative = 0
    
    for frame in frames:
        frame_type = ""
        if frame.is_strike:
            frame_type = f"Strike ({frame.rolls[0]})"
            if frame.bonus_rolls:
                frame_type += f" + bonus [{', '.join(str(b) for b in frame.bonus_rolls)}]"
        elif frame.is_spare:
            frame_type = f"Spare ({frame.rolls[0]} + {frame.rolls[1]})"
            if frame.bonus_rolls:
                frame_type += f" + bonus [{', '.join(str(b) for b in frame.bonus_rolls)}]"
        else:
            frame_type = f"Open ({frame.rolls[0]} + {frame.rolls[1]})"
        
        frame_score = frame.frame_score - cumulative
        cumulative = frame.frame_score
        
        breakdown.append(f"Frame {frame.frame_number}: {frame_type} = {frame_score}")
    
    return "\n".join(breakdown)


# ============================================================================
# Special Game Types
# ============================================================================

def is_perfect_game(rolls: List[int]) -> bool:
    """
    Check if the game is a perfect game (300 points, 12 strikes).
    
    Args:
        rolls: List of pins knocked down per roll.
    
    Returns:
        True if perfect game.
    
    Examples:
        >>> is_perfect_game([10] * 12)
        True
    """
    return len(rolls) >= 12 and all(roll == 10 for roll in rolls[:12])


def is_gutter_game(rolls: List[int]) -> bool:
    """
    Check if the game is a gutter game (all rolls are 0).
    
    Args:
        rolls: List of pins knocked down per roll.
    
    Returns:
        True if gutter game.
    
    Examples:
        >>> is_gutter_game([0] * 20)
        True
    """
    return len(rolls) >= 20 and all(roll == 0 for roll in rolls[:20])


def is_all_spares(rolls: List[int]) -> bool:
    """
    Check if every frame is a spare (score would be 150).
    
    Args:
        rolls: List of pins knocked down per roll.
    
    Returns:
        True if all spares.
    
    Examples:
        >>> is_all_spares([5, 5] * 10 + [5])
        True
    """
    if len(rolls) < 21:
        return False
    
    # Check frames 1-9
    for i in range(9):
        first_roll = rolls[i * 2]
        second_roll = rolls[i * 2 + 1]
        if first_roll + second_roll != 10 or first_roll == 10:
            return False
    
    # Check 10th frame (spare + bonus)
    frame10_first = rolls[18]
    frame10_second = rolls[19]
    if frame10_first + frame10_second != 10:
        return False
    
    return True


def get_game_type(rolls: List[int]) -> str:
    """
    Get a descriptive type name for the game.
    
    Args:
        rolls: List of pins knocked down per roll.
    
    Returns:
        Game type description.
    
    Examples:
        >>> get_game_type([10] * 12)
        'Perfect Game'
        >>> get_game_type([0] * 20)
        'Gutter Game'
    """
    if is_perfect_game(rolls):
        return "Perfect Game"
    elif is_gutter_game(rolls):
        return "Gutter Game"
    elif is_all_spares(rolls):
        return "All Spares"
    
    stats = get_game_statistics(rolls)
    
    if stats['strikes'] > 0 and stats['spares'] == 0:
        return f"Strike Game ({stats['strikes']} strikes)"
    elif stats['spares'] > 0 and stats['strikes'] == 0:
        return f"Spare Game ({stats['spares']} spares)"
    elif stats['open_frames'] == TOTAL_FRAMES:
        return "All Open Frames"
    
    return f"Mixed Game ({stats['strikes']} strikes, {stats['spares']} spares)"


# ============================================================================
# Test Game Generators
# ============================================================================

def generate_perfect_game() -> List[int]:
    """
    Generate a perfect game (12 strikes, 300 points).
    
    Returns:
        List of 12 strikes.
    
    Examples:
        >>> calculate_score(generate_perfect_game())
        300
    """
    return [10] * 12


def generate_gutter_game() -> List[int]:
    """
    Generate a gutter game (20 gutter rolls, 0 points).
    
    Returns:
        List of 20 zeros.
    
    Examples:
        >>> calculate_score(generate_gutter_game())
        0
    """
    return [0] * 20


def generate_all_spares_game(first_pin: int = 5) -> List[int]:
    """
    Generate a game with all spares.
    
    Args:
        first_pin: Pins knocked down in first roll of each frame (1-9).
    
    Returns:
        List of rolls for all-spare game.
    
    Raises:
        ValueError: If first_pin is out of range.
    
    Examples:
        >>> calculate_score(generate_all_spares_game(5))
        150
        >>> calculate_score(generate_all_spares_game(3))
        150
    """
    if first_pin < 1 or first_pin > 9:
        raise ValueError("first_pin must be between 1 and 9")
    
    rolls = []
    for _ in range(9):  # Frames 1-9
        rolls.extend([first_pin, 10 - first_pin])
    
    # Frame 10: spare + bonus
    rolls.extend([first_pin, 10 - first_pin, first_pin])
    
    return rolls


def generate_random_game(strike_prob: float = 0.2, spare_prob: float = 0.3) -> List[int]:
    """
    Generate a random bowling game.
    
    Args:
        strike_prob: Probability of strike (default: 20%).
        spare_prob: Probability of spare after non-strike first roll (default: 30%).
    
    Returns:
        List of rolls for a random game.
    
    Examples:
        >>> game = generate_random_game()
        >>> len(game) >= 20  # At least 20 rolls for complete game
        True
    """
    import random
    
    rolls = []
    
    for frame in range(1, TOTAL_FRAMES + 1):
        if random.random() < strike_prob:
            # Strike
            rolls.append(10)
        else:
            # First roll (random pins 0-9)
            first_roll = random.randint(0, 9)
            rolls.append(first_roll)
            
            # Second roll
            remaining = 10 - first_roll
            if random.random() < spare_prob and remaining > 0:
                # Spare
                rolls.append(remaining)
            else:
                # Open (random pins from remaining)
                second_roll = random.randint(0, remaining)
                rolls.append(second_roll)
    
    # Handle 10th frame bonus rolls
    if len(rolls) >= 20:
        frame10_first = rolls[18]
        frame10_second = rolls[19]
        
        if frame10_first == 10:  # Strike in 10th
            # Need 2 more rolls
            if random.random() < strike_prob:
                rolls.append(10)
            else:
                bonus1 = random.randint(0, 9)
                rolls.append(bonus1)
                remaining = 10 - bonus1
                if random.random() < spare_prob and remaining > 0:
                    rolls.append(remaining)
                else:
                    rolls.append(random.randint(0, remaining))
        elif frame10_first + frame10_second == 10:  # Spare in 10th
            # Need 1 more roll
            if random.random() < strike_prob:
                rolls.append(10)
            else:
                rolls.append(random.randint(0, 10))
    
    return rolls


# ============================================================================
# Convenience Functions
# ============================================================================

def quick_score(score_input: Union[str, List]) -> int:
    """
    Quick score calculation from string or list input.
    
    Args:
        score_input: Score string or list of rolls.
    
    Returns:
        Total score.
    
    Examples:
        >>> quick_score("X X X X X X X X X XXX")
        300
        >>> quick_score([10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10])
        300
        >>> quick_score("12 34 5/ X-")
        35
    """
    if isinstance(score_input, str):
        rolls = parse_score_string(score_input)
    elif isinstance(score_input, list):
        rolls = parse_score_list(score_input)
    else:
        raise ValueError(f"Invalid input type: {type(score_input)}")
    
    return calculate_score(rolls)


def parse_and_analyze(score_input: Union[str, List]) -> BowlingGame:
    """
    Parse input and perform complete analysis.
    
    Args:
        score_input: Score string or list of rolls.
    
    Returns:
        BowlingGame object with complete analysis.
    
    Examples:
        >>> game = parse_and_analyze("X X X X X X X X X XXX")
        >>> game.is_perfect
        True
    """
    if isinstance(score_input, str):
        rolls = parse_score_string(score_input)
    elif isinstance(score_input, list):
        rolls = parse_score_list(score_input)
    else:
        raise ValueError(f"Invalid input type: {type(score_input)}")
    
    return analyze_game(rolls)


if __name__ == '__main__':
    # Demo
    print("=" * 60)
    print("Bowling Score Calculator Utilities Demo")
    print("=" * 60)
    
    # Perfect game
    print("\n1. Perfect Game (12 strikes):")
    perfect = generate_perfect_game()
    game = analyze_game(perfect)
    print(f"   Rolls: {' '.join(str(r) for r in perfect[:12])}")
    print(f"   Score: {game.total_score}")
    print(f"   Type: {get_game_type(perfect)}")
    print(f"   Scorecard:\n{format_scorecard(perfect)}")
    
    # Gutter game
    print("\n2. Gutter Game (all zeros):")
    gutter = generate_gutter_game()
    game = analyze_game(gutter)
    print(f"   Score: {game.total_score}")
    print(f"   Type: {get_game_type(gutter)}")
    
    # All spares
    print("\n3. All Spares Game:")
    spares = generate_all_spares_game(5)
    game = analyze_game(spares)
    print(f"   Score: {game.total_score}")
    print(f"   Type: {get_game_type(spares)}")
    print(f"   Scorecard:\n{format_scorecard(spares)}")
    
    # Mixed game
    print("\n4. Mixed Game Example:")
    mixed = [10, 7, 3, 9, 0, 10, 0, 8, 8, 2, 0, 6, 10, 10, 10, 8, 1]
    game = analyze_game(mixed)
    print(f"   Input: {mixed}")
    print(f"   Score: {game.total_score}")
    print(f"   Strikes: {game.strikes}, Spares: {game.spares}")
    print(f"   Scorecard:\n{format_scorecard(mixed)}")
    print(f"   Breakdown:\n{get_frame_breakdown(mixed)}")
    
    # String parsing
    print("\n5. String Parsing:")
    score_str = "X 7/ 9- X X X X X X X X X"
    print(f"   Input: '{score_str}'")
    print(f"   Score: {quick_score(score_str)}")
    
    # Random game
    print("\n6. Random Game:")
    random_game = generate_random_game()
    game = analyze_game(random_game)
    print(f"   Score: {game.total_score}")
    print(f"   Type: {get_game_type(random_game)}")
    print(f"   Scorecard:\n{format_scorecard(random_game)}")