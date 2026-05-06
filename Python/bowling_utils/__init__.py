#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AllToolkit - Bowling Score Calculator Utilities
=================================================
A comprehensive bowling score calculation utility module.

This module provides:
    - Parse bowling scores from various formats
    - Calculate total score with proper strike/spare handling
    - Validate bowling game input
    - Frame-by-frame score breakdown
    - Perfect game (300) and gutter game (0) detection
    - Maximum possible score from current state
    - Bowling game statistics
"""

from bowling_utils.mod import (
    # Parsing
    parse_roll_symbol,
    parse_score_string,
    parse_score_list,
    parse_and_analyze,
    
    # Validation
    validate_rolls,
    validate_game_complete,
    
    # Calculation
    calculate_score,
    calculate_frame_scores,
    calculate_max_possible_score,
    quick_score,
    
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
    GUTTER_GAME_SCORE,
    TOTAL_FRAMES,
    
    # Data classes
    FrameScore,
    BowlingGame,
)

__all__ = [
    'parse_roll_symbol',
    'parse_score_string',
    'parse_score_list',
    'parse_and_analyze',
    'validate_rolls',
    'validate_game_complete',
    'calculate_score',
    'calculate_frame_scores',
    'calculate_max_possible_score',
    'quick_score',
    'count_strikes',
    'count_spares',
    'count_gutter_rolls',
    'get_game_statistics',
    'analyze_game',
    'format_scorecard',
    'get_frame_breakdown',
    'get_game_type',
    'is_perfect_game',
    'is_gutter_game',
    'is_all_spares',
    'generate_perfect_game',
    'generate_gutter_game',
    'generate_all_spares_game',
    'generate_random_game',
    'PERFECT_GAME_SCORE',
    'GUTTER_GAME_SCORE',
    'TOTAL_FRAMES',
    'FrameScore',
    'BowlingGame',
]