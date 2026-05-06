#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AllToolkit - Bowling Score Calculator Utilities Tests
======================================================
Comprehensive test suite for bowling_utils module.

Tests cover:
- Score parsing (string and list formats)
- Score calculation (strike, spare, open frames)
- 10th frame special rules
- Validation functions
- Statistics functions
- Edge cases and error handling
"""

import unittest
from typing import List

# Import the module
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from mod import (
    # Parsing
    parse_roll_symbol,
    parse_score_string,
    parse_score_list,
    
    # Validation
    validate_rolls,
    validate_game_complete,
    
    # Calculation
    calculate_score,
    calculate_frame_scores,
    calculate_max_possible_score,
    
    # Statistics
    count_strikes,
    count_spares,
    count_gutter_rolls,
    get_game_statistics,
    
    # Analysis
    analyze_game,
    format_scorecard,
    get_frame_breakdown,
    
    # Special games
    is_perfect_game,
    is_gutter_game,
    is_all_spares,
    get_game_type,
    
    # Generators
    generate_perfect_game,
    generate_gutter_game,
    generate_all_spares_game,
    generate_random_game,
    
    # Convenience
    quick_score,
    parse_and_analyze,
    
    # Constants
    PERFECT_GAME_SCORE,
    GUTTER_GAME_SCORE,
    TOTAL_FRAMES,
)


class TestParseRollSymbol(unittest.TestCase):
    """Tests for parse_roll_symbol function."""
    
    def test_strike_symbols(self):
        """Test strike symbol parsing."""
        self.assertEqual(parse_roll_symbol('X'), 10)
        self.assertEqual(parse_roll_symbol('x'), 10)
    
    def test_spare_symbol(self):
        """Test spare symbol parsing."""
        self.assertEqual(parse_roll_symbol('/'), 10)
    
    def test_pin_numbers(self):
        """Test pin number parsing."""
        for i in range(10):
            self.assertEqual(parse_roll_symbol(str(i)), i)
    
    def test_gutter_symbols(self):
        """Test gutter symbol parsing."""
        self.assertEqual(parse_roll_symbol('-'), 0)
        self.assertEqual(parse_roll_symbol('0'), 0)
    
    def test_invalid_symbols(self):
        """Test invalid symbol handling."""
        with self.assertRaises(ValueError):
            parse_roll_symbol('A')
        with self.assertRaises(ValueError):
            parse_roll_symbol('11')


class TestParseScoreString(unittest.TestCase):
    """Tests for parse_score_string function."""
    
    def test_perfect_game_string(self):
        """Test perfect game string parsing."""
        rolls = parse_score_string("X X X X X X X X X XXX")
        self.assertEqual(rolls, [10] * 12)
    
    def test_gutter_game_string(self):
        """Test gutter game string parsing."""
        # A valid gutter game string has exactly 20 gutters
        # "-- -- -- -- -- -- -- -- -- --" = 10 frames with 2 gutters each
        rolls = parse_score_string("-- -- -- -- -- -- -- -- -- --")
        self.assertEqual(rolls, [0] * 20)
        self.assertEqual(calculate_score(rolls), 0)
    
    def test_mixed_game_string(self):
        """Test mixed game string parsing."""
        rolls = parse_score_string("X 7/ 9- 0-")
        self.assertEqual(rolls, [10, 7, 3, 9, 0, 0, 0])
    
    def test_string_with_spaces(self):
        """Test string with various spacing."""
        rolls = parse_score_string("X X X X X X X X X XXX")
        self.assertEqual(len(rolls), 12)
        self.assertEqual(calculate_score(rolls), 300)
    
    def test_spare_calculation(self):
        """Test that spare values are calculated correctly."""
        rolls = parse_score_string("5/")
        self.assertEqual(rolls, [5, 5])
        
        rolls = parse_score_string("3/")
        self.assertEqual(rolls, [3, 7])
        
        rolls = parse_score_string("9/")
        self.assertEqual(rolls, [9, 1])
    
    def test_invalid_spare(self):
        """Test invalid spare detection."""
        with self.assertRaises(ValueError):
            parse_score_string("X/")  # Invalid: strike followed by spare
    
    def test_invalid_string_format(self):
        """Test invalid string format."""
        with self.assertRaises(ValueError):
            parse_score_string("ABC")


class TestParseScoreList(unittest.TestCase):
    """Tests for parse_score_list function."""
    
    def test_integer_list(self):
        """Test integer list parsing."""
        rolls = parse_score_list([10, 10, 10])
        self.assertEqual(rolls, [10, 10, 10])
    
    def test_string_list(self):
        """Test string list parsing."""
        rolls = parse_score_list(['X', 'X', 'X'])
        self.assertEqual(rolls, [10, 10, 10])
    
    def test_mixed_list(self):
        """Test mixed integer/string list."""
        rolls = parse_score_list([10, '5', '/', 0])
        self.assertEqual(rolls, [10, 5, 5, 0])
    
    def test_invalid_list_element(self):
        """Test invalid list element."""
        with self.assertRaises(ValueError):
            parse_score_list([10, 11])  # Invalid: 11 pins
        
        with self.assertRaises(ValueError):
            parse_score_list([10, -1])  # Invalid: -1 pins


class TestValidateRolls(unittest.TestCase):
    """Tests for validate_rolls function."""
    
    def test_valid_perfect_game(self):
        """Test valid perfect game."""
        self.assertTrue(validate_rolls([10] * 12))
    
    def test_valid_gutter_game(self):
        """Test valid gutter game."""
        self.assertTrue(validate_rolls([0] * 20))
    
    def test_valid_all_spares(self):
        """Test valid all spares game."""
        rolls = [5, 5] * 10 + [5]
        self.assertTrue(validate_rolls(rolls))
    
    def test_invalid_frame_total(self):
        """Test invalid frame total (> 10 pins)."""
        self.assertFalse(validate_rolls([6, 6]))  # 12 pins in frame 1
    
    def test_invalid_roll_value(self):
        """Test invalid roll value."""
        self.assertFalse(validate_rolls([11]))  # Invalid: 11 pins
        self.assertFalse(validate_rolls([-1]))  # Invalid: -1 pins
    
    def test_empty_rolls(self):
        """Test empty rolls."""
        self.assertFalse(validate_rolls([]))


class TestValidateGameComplete(unittest.TestCase):
    """Tests for validate_game_complete function."""
    
    def test_complete_perfect_game(self):
        """Test complete perfect game."""
        is_complete, msg = validate_game_complete([10] * 12)
        self.assertTrue(is_complete)
        self.assertEqual(msg, "Game complete")
    
    def test_complete_gutter_game(self):
        """Test complete gutter game."""
        is_complete, msg = validate_game_complete([0] * 20)
        self.assertTrue(is_complete)
    
    def test_incomplete_game(self):
        """Test incomplete game."""
        is_complete, msg = validate_game_complete([10, 10])
        self.assertFalse(is_complete)
        self.assertIn("Waiting", msg)
    
    def test_incomplete_10th_frame_strike(self):
        """Test incomplete 10th frame after strike."""
        rolls = [10] * 9 + [10]  # Only one roll in 10th frame
        is_complete, msg = validate_game_complete(rolls)
        self.assertFalse(is_complete)
    
    def test_incomplete_10th_frame_spare(self):
        """Test incomplete 10th frame after spare."""
        rolls = [5, 5] * 9 + [5, 5]  # Missing bonus roll
        is_complete, msg = validate_game_complete(rolls)
        self.assertFalse(is_complete)


class TestCalculateScore(unittest.TestCase):
    """Tests for calculate_score function."""
    
    def test_perfect_game_score(self):
        """Test perfect game score (300)."""
        score = calculate_score([10] * 12)
        self.assertEqual(score, PERFECT_GAME_SCORE)
    
    def test_gutter_game_score(self):
        """Test gutter game score (0)."""
        score = calculate_score([0] * 20)
        self.assertEqual(score, GUTTER_GAME_SCORE)
    
    def test_all_spares_score(self):
        """Test all spares score (150)."""
        rolls = [5, 5] * 10 + [5]
        score = calculate_score(rolls)
        self.assertEqual(score, 150)
    
    def test_all_nine_open_frames(self):
        """Test all 9-pin open frames (90)."""
        rolls = [9, 0] * 10
        score = calculate_score(rolls)
        self.assertEqual(score, 90)
    
    def test_single_strike(self):
        """Test single strike scoring."""
        rolls = [10, 5, 3] + [0] * 16  # Strike + 5 + 3 = 18, then gutters
        score = calculate_score(rolls)
        # Frame 1: 10 + 5 + 3 = 18
        # Frame 2: 5 + 3 = 8
        # Frames 3-10: 0 each
        self.assertEqual(score, 26)
    
    def test_two_consecutive_strikes(self):
        """Test two consecutive strikes (double)."""
        rolls = [10, 10, 5, 3] + [0] * 14
        score = calculate_score(rolls)
        # Frame 1: 10 + 10 + 5 = 25
        # Frame 2: 10 + 5 + 3 = 18
        # Frame 3: 5 + 3 = 8
        # Total: 51
        self.assertEqual(score, 51)
    
    def test_three_consecutive_strikes(self):
        """Test three consecutive strikes (turkey)."""
        rolls = [10, 10, 10] + [0] * 14
        score = calculate_score(rolls)
        # Frame 1: 10 + 10 + 10 = 30
        # Frame 2: 10 + 10 + 0 = 20
        # Frame 3: 10 + 0 + 0 = 10
        # Frames 4-10: 0 each
        self.assertEqual(score, 60)
    
    def test_single_spare(self):
        """Test single spare scoring."""
        rolls = [5, 5, 3] + [0] * 17  # Spare + 3 = 13, then gutters
        score = calculate_score(rolls)
        # Frame 1: 10 + 3 = 13
        # Frame 2: 3 + 0 = 3
        # Frames 3-10: 0 each
        self.assertEqual(score, 16)
    
    def test_spare_followed_by_strike(self):
        """Test spare followed by strike."""
        rolls = [5, 5, 10] + [0] * 16
        score = calculate_score(rolls)
        # Frame 1: 10 + 10 = 20
        # Frame 2: 10 + 0 + 0 = 10
        # Total: 30
        self.assertEqual(score, 30)
    
    def test_10th_frame_strike(self):
        """Test 10th frame strike with bonus."""
        rolls = [0] * 18 + [10, 5, 3]
        score = calculate_score(rolls)
        # Frames 1-9: 0 each
        # Frame 10: 10 + 5 + 3 = 18
        self.assertEqual(score, 18)
    
    def test_10th_frame_spare(self):
        """Test 10th frame spare with bonus."""
        rolls = [0] * 18 + [5, 5, 3]
        score = calculate_score(rolls)
        # Frames 1-9: 0 each
        # Frame 10: 10 + 3 = 13
        self.assertEqual(score, 13)
    
    def test_10th_frame_open(self):
        """Test 10th frame open."""
        rolls = [0] * 18 + [5, 3]
        score = calculate_score(rolls)
        # Frames 1-9: 0 each
        # Frame 10: 5 + 3 = 8
        self.assertEqual(score, 8)
    
    def test_mixed_game(self):
        """Test mixed game scoring."""
        # Example from Wikipedia bowling scoring
        rolls = [10, 7, 3, 9, 0, 10, 0, 8, 8, 2, 0, 6, 10, 10, 10, 8, 1]
        score = calculate_score(rolls)
        # Frame 1: 10 + 7 + 3 = 20
        # Frame 2: 10 + 9 = 19
        # Frame 3: 9 + 0 = 9
        # Frame 4: 10 + 0 + 8 = 18
        # Frame 5: 0 + 8 = 8
        # Frame 6: 10 + 0 = 10
        # Frame 7: 0 + 6 = 6
        # Frame 8: 10 + 10 + 10 = 30
        # Frame 9: 10 + 10 + 8 = 28
        # Frame 10: 10 + 8 + 1 = 19
        # Total: 167
        self.assertEqual(score, 167)
    
    def test_incomplete_game(self):
        """Test incomplete game scoring."""
        rolls = [10, 5, 3]
        score = calculate_score(rolls)
        # Frame 1: 10 + 5 + 3 = 18
        # Frame 2: 5 + 3 = 8 (partial)
        self.assertEqual(score, 26)
    
    def test_invalid_roll_value(self):
        """Test invalid roll value raises error."""
        with self.assertRaises(ValueError):
            calculate_score([11])
        with self.assertRaises(ValueError):
            calculate_score([-1])
    
    def test_invalid_frame_total(self):
        """Test invalid frame total raises error."""
        with self.assertRaises(ValueError):
            calculate_score([6, 6])  # 12 pins in one frame
    
    def test_empty_rolls(self):
        """Test empty rolls returns 0."""
        self.assertEqual(calculate_score([]), 0)


class TestCalculateFrameScores(unittest.TestCase):
    """Tests for calculate_frame_scores function."""
    
    def test_perfect_game_frames(self):
        """Test perfect game frame scores."""
        frames = calculate_frame_scores([10] * 12)
        self.assertEqual(len(frames), 10)
        
        # Check cumulative scores
        expected_scores = [30, 60, 90, 120, 150, 180, 210, 240, 270, 300]
        for i, frame in enumerate(frames):
            self.assertEqual(frame.frame_score, expected_scores[i])
            self.assertTrue(frame.is_strike)
    
    def test_gutter_game_frames(self):
        """Test gutter game frame scores."""
        frames = calculate_frame_scores([0] * 20)
        self.assertEqual(len(frames), 10)
        
        for frame in frames:
            self.assertEqual(frame.frame_score, 0)
            self.assertTrue(frame.is_open)
    
    def test_strike_frame_details(self):
        """Test strike frame details."""
        frames = calculate_frame_scores([10, 5, 3] + [0] * 16)
        
        # Frame 1 should be strike with bonus
        frame1 = frames[0]
        self.assertTrue(frame1.is_strike)
        self.assertEqual(frame1.rolls, [10])
        self.assertEqual(frame1.bonus_rolls, [5, 3])
        self.assertEqual(frame1.frame_score, 18)
    
    def test_spare_frame_details(self):
        """Test spare frame details."""
        frames = calculate_frame_scores([5, 5, 3] + [0] * 17)
        
        # Frame 1 should be spare with bonus
        frame1 = frames[0]
        self.assertTrue(frame1.is_spare)
        self.assertEqual(frame1.rolls, [5, 5])
        self.assertEqual(frame1.bonus_rolls, [3])
        self.assertEqual(frame1.frame_score, 13)
    
    def test_open_frame_details(self):
        """Test open frame details."""
        frames = calculate_frame_scores([5, 3] + [0] * 18)
        
        # Frame 1 should be open
        frame1 = frames[0]
        self.assertTrue(frame1.is_open)
        self.assertEqual(frame1.rolls, [5, 3])
        self.assertEqual(frame1.bonus_rolls, [])
        self.assertEqual(frame1.frame_score, 8)
    
    def test_10th_frame_strike_details(self):
        """Test 10th frame strike details."""
        frames = calculate_frame_scores([0] * 18 + [10, 5, 3])
        
        frame10 = frames[9]
        self.assertTrue(frame10.is_strike)
        self.assertEqual(frame10.rolls, [10, 5, 3])
        self.assertEqual(frame10.frame_score, 18)
    
    def test_empty_rolls(self):
        """Test empty rolls."""
        frames = calculate_frame_scores([])
        self.assertEqual(frames, [])


class TestCalculateMaxPossibleScore(unittest.TestCase):
    """Tests for calculate_max_possible_score function."""
    
    def test_empty_game_max(self):
        """Test empty game max score."""
        self.assertEqual(calculate_max_possible_score([]), 300)
    
    def test_after_one_strike(self):
        """Test max after one strike (still can get perfect)."""
        # After one strike, can still get 9 more strikes + 10th frame 3 strikes = 12 strikes
        self.assertEqual(calculate_max_possible_score([10]), 300)
    
    def test_after_open_frame(self):
        """Test max after open frame (cannot get perfect)."""
        max_score = calculate_max_possible_score([5, 3])
        # Lost 2 pins in frame 1 (8 instead of 10)
        # Remaining 9 frames: max 270 (9 strikes)
        # Total: 8 + 270 = 278
        self.assertEqual(max_score, 278)
    
    def test_after_spare(self):
        """Test max after spare (can get near perfect)."""
        max_score = calculate_max_possible_score([5, 5])
        # Frame 1: spare, need strike bonus for max
        # Max bonus scenario: next roll is strike
        # Remaining: all strikes
        self.assertGreater(max_score, 270)
        self.assertLess(max_score, 300)
    
    def test_after_partial_frame(self):
        """Test max after partial frame (first roll only)."""
        # After first roll 5, can get spare + all strikes
        # Score depends on bonus structure - this is approximate
        max_score = calculate_max_possible_score([5])
        # Should be less than 300 since we lost potential for a strike in frame 1
        self.assertGreater(max_score, 200)
        self.assertLess(max_score, 300)
    
    def test_gutter_cannot_get_perfect(self):
        """Test gutter in first roll prevents perfect."""
        max_score = calculate_max_possible_score([0, 10])  # Gutter + strike
        # Lost the first roll (0), can't get perfect
        self.assertLess(max_score, 300)


class TestCountStrikes(unittest.TestCase):
    """Tests for count_strikes function."""
    
    def test_perfect_game_strikes(self):
        """Test perfect game strike count."""
        self.assertEqual(count_strikes([10] * 12), 12)
    
    def test_gutter_game_strikes(self):
        """Test gutter game strike count."""
        self.assertEqual(count_strikes([0] * 20), 0)
    
    def test_mixed_game_strikes(self):
        """Test mixed game strike count."""
        rolls = [10, 5, 5, 10, 0, 0]
        self.assertEqual(count_strikes(rolls), 2)


class TestCountSpares(unittest.TestCase):
    """Tests for count_spares function."""
    
    def test_all_spares_count(self):
        """Test all spares count."""
        rolls = [5, 5] * 10 + [5]
        self.assertEqual(count_spares(rolls), 10)
    
    def test_no_spares(self):
        """Test no spares count."""
        self.assertEqual(count_spares([10] * 12), 0)
        self.assertEqual(count_spares([0] * 20), 0)
    
    def test_mixed_game_spares(self):
        """Test mixed game spare count."""
        rolls = [5, 5, 10, 3, 7]
        self.assertEqual(count_spares(rolls), 2)


class TestCountGutterRolls(unittest.TestCase):
    """Tests for count_gutter_rolls function."""
    
    def test_gutter_game_count(self):
        """Test gutter game gutter count."""
        self.assertEqual(count_gutter_rolls([0] * 20), 20)
    
    def test_perfect_game_count(self):
        """Test perfect game gutter count."""
        self.assertEqual(count_gutter_rolls([10] * 12), 0)
    
    def test_mixed_game_count(self):
        """Test mixed game gutter count."""
        rolls = [0, 10, 5, 0]
        self.assertEqual(count_gutter_rolls(rolls), 2)


class TestGetGameStatistics(unittest.TestCase):
    """Tests for get_game_statistics function."""
    
    def test_perfect_game_stats(self):
        """Test perfect game statistics."""
        stats = get_game_statistics([10] * 12)
        
        self.assertEqual(stats['total_score'], 300)
        self.assertEqual(stats['strikes'], 12)
        self.assertEqual(stats['spares'], 0)
        self.assertEqual(stats['gutter_rolls'], 0)
        self.assertTrue(stats['is_perfect'])
        self.assertFalse(stats['is_gutter_game'])
        self.assertTrue(stats['is_complete'])
    
    def test_gutter_game_stats(self):
        """Test gutter game statistics."""
        stats = get_game_statistics([0] * 20)
        
        self.assertEqual(stats['total_score'], 0)
        self.assertEqual(stats['strikes'], 0)
        self.assertEqual(stats['spares'], 0)
        self.assertEqual(stats['gutter_rolls'], 20)
        self.assertTrue(stats['is_gutter_game'])
        self.assertFalse(stats['is_perfect'])
    
    def test_all_spares_stats(self):
        """Test all spares statistics."""
        rolls = [5, 5] * 10 + [5]
        stats = get_game_statistics(rolls)
        
        self.assertEqual(stats['total_score'], 150)
        self.assertEqual(stats['spares'], 10)
        self.assertEqual(stats['strikes'], 0)


class TestAnalyzeGame(unittest.TestCase):
    """Tests for analyze_game function."""
    
    def test_perfect_game_analysis(self):
        """Test perfect game analysis."""
        game = analyze_game([10] * 12)
        
        self.assertEqual(game.total_score, 300)
        self.assertEqual(game.strikes, 12)
        self.assertTrue(game.is_perfect)
        self.assertTrue(game.is_complete)
        self.assertEqual(game.max_possible_score, 300)
    
    def test_incomplete_game_analysis(self):
        """Test incomplete game analysis."""
        game = analyze_game([10, 5])
        
        self.assertFalse(game.is_complete)
        self.assertGreater(game.max_possible_score, game.total_score)


class TestFormatScorecard(unittest.TestCase):
    """Tests for format_scorecard function."""
    
    def test_perfect_game_scorecard(self):
        """Test perfect game scorecard format."""
        scorecard = format_scorecard([10] * 12)
        
        self.assertIn('300', scorecard)
        self.assertIn('X', scorecard)
    
    def test_gutter_game_scorecard(self):
        """Test gutter game scorecard format."""
        scorecard = format_scorecard([0] * 20)
        
        self.assertIn('0', scorecard)
    
    def test_empty_rolls_scorecard(self):
        """Test empty rolls scorecard."""
        scorecard = format_scorecard([])
        self.assertIn("No frames", scorecard)


class TestGetFrameBreakdown(unittest.TestCase):
    """Tests for get_frame_breakdown function."""
    
    def test_strike_breakdown(self):
        """Test strike frame breakdown."""
        rolls = [10, 5, 3] + [0] * 16
        breakdown = get_frame_breakdown(rolls)
        
        self.assertIn('Strike', breakdown)
        # Frame 1: strike + bonus [5, 3] = 18
        self.assertIn('18', breakdown)
    
    def test_spare_breakdown(self):
        """Test spare frame breakdown."""
        rolls = [5, 5, 3] + [0] * 17
        breakdown = get_frame_breakdown(rolls)
        
        self.assertIn('Spare', breakdown)
    
    def test_open_breakdown(self):
        """Test open frame breakdown."""
        rolls = [5, 3] + [0] * 18
        breakdown = get_frame_breakdown(rolls)
        
        self.assertIn('Open', breakdown)


class TestIsPerfectGame(unittest.TestCase):
    """Tests for is_perfect_game function."""
    
    def test_perfect_game_true(self):
        """Test perfect game detection."""
        self.assertTrue(is_perfect_game([10] * 12))
    
    def test_almost_perfect_false(self):
        """Test almost perfect game."""
        rolls = [10] * 11 + [9]
        self.assertFalse(is_perfect_game(rolls))
    
    def test_gutter_game_false(self):
        """Test gutter game is not perfect."""
        self.assertFalse(is_perfect_game([0] * 20))


class TestIsGutterGame(unittest.TestCase):
    """Tests for is_gutter_game function."""
    
    def test_gutter_game_true(self):
        """Test gutter game detection."""
        self.assertTrue(is_gutter_game([0] * 20))
    
    def test_almost_gutter_false(self):
        """Test almost gutter game."""
        rolls = [0] * 19 + [1]
        self.assertFalse(is_gutter_game(rolls))
    
    def test_perfect_game_false(self):
        """Test perfect game is not gutter."""
        self.assertFalse(is_gutter_game([10] * 12))


class TestIsAllSpares(unittest.TestCase):
    """Tests for is_all_spares function."""
    
    def test_all_spares_true(self):
        """Test all spares detection."""
        rolls = [5, 5] * 10 + [5]
        self.assertTrue(is_all_spares(rolls))
    
    def test_mixed_game_false(self):
        """Test mixed game."""
        rolls = [5, 5, 10, 3, 7] + [0] * 12
        self.assertFalse(is_all_spares(rolls))
    
    def test_all_open_false(self):
        """Test all open frames."""
        rolls = [5, 4] * 10
        self.assertFalse(is_all_spares(rolls))


class TestGetGameType(unittest.TestCase):
    """Tests for get_game_type function."""
    
    def test_perfect_game_type(self):
        """Test perfect game type."""
        self.assertEqual(get_game_type([10] * 12), "Perfect Game")
    
    def test_gutter_game_type(self):
        """Test gutter game type."""
        self.assertEqual(get_game_type([0] * 20), "Gutter Game")
    
    def test_all_spares_type(self):
        """Test all spares type."""
        rolls = [5, 5] * 10 + [5]
        self.assertEqual(get_game_type(rolls), "All Spares")
    
    def test_strike_game_type(self):
        """Test strike-only game type."""
        rolls = [10, 0, 0] * 9 + [10, 0, 0]
        game_type = get_game_type(rolls)
        self.assertIn("Strike Game", game_type)
    
    def test_all_open_type(self):
        """Test all open frames type."""
        rolls = [5, 4] * 10
        self.assertEqual(get_game_type(rolls), "All Open Frames")


class TestGeneratePerfectGame(unittest.TestCase):
    """Tests for generate_perfect_game function."""
    
    def test_perfect_game_generation(self):
        """Test perfect game generation."""
        rolls = generate_perfect_game()
        
        self.assertEqual(len(rolls), 12)
        self.assertEqual(calculate_score(rolls), 300)
        self.assertTrue(is_perfect_game(rolls))


class TestGenerateGutterGame(unittest.TestCase):
    """Tests for generate_gutter_game function."""
    
    def test_gutter_game_generation(self):
        """Test gutter game generation."""
        rolls = generate_gutter_game()
        
        self.assertEqual(len(rolls), 20)
        self.assertEqual(calculate_score(rolls), 0)
        self.assertTrue(is_gutter_game(rolls))


class TestGenerateAllSparesGame(unittest.TestCase):
    """Tests for generate_all_spares_game function."""
    
    def test_all_spares_generation(self):
        """Test all spares generation."""
        rolls = generate_all_spares_game(5)
        
        self.assertEqual(len(rolls), 21)
        self.assertEqual(calculate_score(rolls), 150)
        self.assertTrue(is_all_spares(rolls))
    
    def test_different_first_pin(self):
        """Test different first pin values (score varies based on bonus)."""
        # Score = 100 + 10 * first_pin (each spare gets bonus = next first_pin)
        expected_scores = {1: 110, 2: 120, 3: 130, 4: 140, 5: 150, 
                          6: 160, 7: 170, 8: 180, 9: 190}
        for pin, expected_score in expected_scores.items():
            rolls = generate_all_spares_game(pin)
            self.assertEqual(calculate_score(rolls), expected_score)
    
    def test_invalid_first_pin(self):
        """Test invalid first pin."""
        with self.assertRaises(ValueError):
            generate_all_spares_game(0)
        with self.assertRaises(ValueError):
            generate_all_spares_game(10)


class TestGenerateRandomGame(unittest.TestCase):
    """Tests for generate_random_game function."""
    
    def test_random_game_generation(self):
        """Test random game generation."""
        game = generate_random_game()
        
        # Should have valid structure
        self.assertTrue(validate_rolls(game))
        
        # Score should be between 0 and 300
        score = calculate_score(game)
        self.assertGreaterEqual(score, 0)
        self.assertLessEqual(score, 300)
    
    def test_high_strike_probability(self):
        """Test high strike probability."""
        game = generate_random_game(strike_prob=0.9, spare_prob=0.1)
        strikes = count_strikes(game)
        # Should have many strikes
        self.assertGreater(strikes, 5)


class TestQuickScore(unittest.TestCase):
    """Tests for quick_score function."""
    
    def test_string_input(self):
        """Test string input."""
        score = quick_score("X X X X X X X X X XXX")
        self.assertEqual(score, 300)
    
    def test_list_input(self):
        """Test list input."""
        score = quick_score([10] * 12)
        self.assertEqual(score, 300)
    
    def test_invalid_input_type(self):
        """Test invalid input type."""
        with self.assertRaises(ValueError):
            quick_score(123)  # Invalid: integer


class TestParseAndAnalyze(unittest.TestCase):
    """Tests for parse_and_analyze function."""
    
    def test_string_analysis(self):
        """Test string input analysis."""
        game = parse_and_analyze("X X X X X X X X X XXX")
        
        self.assertEqual(game.total_score, 300)
        self.assertTrue(game.is_perfect)
    
    def test_list_analysis(self):
        """Test list input analysis."""
        game = parse_and_analyze([10] * 12)
        
        self.assertEqual(game.total_score, 300)
        self.assertTrue(game.is_perfect)


class TestEdgeCases(unittest.TestCase):
    """Tests for edge cases and special scenarios."""
    
    def test_single_roll(self):
        """Test single roll."""
        score = calculate_score([10])
        # Frame 1: 10 + 0 + 0 = 10 (partial)
        self.assertEqual(score, 10)
    
    def test_all_eights(self):
        """Test all 8-pin open frames."""
        rolls = [8, 0] * 10
        score = calculate_score(rolls)
        self.assertEqual(score, 80)
    
    def test_strike_followed_by_gutter_spare(self):
        """Test strike followed by gutter then spare."""
        rolls = [10, 0, 10] + [0] * 16
        score = calculate_score(rolls)
        # Frame 1: 10 + 0 + 10 = 20
        # Frame 2: 0 + 10 = 10 + 0 = 10
        # Total: 30
        self.assertEqual(score, 30)
    
    def test_turkey_in_10th_frame(self):
        """Test three strikes in 10th frame."""
        rolls = [0] * 18 + [10, 10, 10]
        score = calculate_score(rolls)
        self.assertEqual(score, 30)
    
    def test_spare_strike_strike_in_10th(self):
        """Test spare then two strikes in 10th frame."""
        # Frame 10: spare (5+5), then bonus strikes X X
        # But bowling rules: spare in 10th gets ONLY ONE bonus roll
        # So having 2 strikes after spare is invalid input (extra rolls)
        # The score calculation only uses first bonus roll
        rolls = [0] * 18 + [5, 5, 10, 10]  # 4 rolls in 10th (spare + 2 bonus)
        score = calculate_score(rolls)
        # Frames 1-9: 0 each
        # Frame 10: spare + 1 bonus strike = 5+5+10 = 20
        self.assertEqual(score, 20)
    
    def test_very_long_game(self):
        """Test handling of excessively long roll list."""
        rolls = [10] * 20  # Too many rolls
        score = calculate_score(rolls)
        self.assertEqual(score, 300)  # Should cap at 300


class Test10thFrameSpecialCases(unittest.TestCase):
    """Tests for 10th frame special rules."""
    
    def test_10th_strike_open(self):
        """Test strike then open in 10th."""
        rolls = [0] * 18 + [10, 5, 3]
        score = calculate_score(rolls)
        self.assertEqual(score, 18)
    
    def test_10th_strike_spare(self):
        """Test strike then spare in 10th."""
        rolls = [0] * 18 + [10, 5, 5]
        score = calculate_score(rolls)
        self.assertEqual(score, 20)
    
    def test_10th_spare_strike(self):
        """Test spare then strike in 10th."""
        rolls = [0] * 18 + [5, 5, 10]
        score = calculate_score(rolls)
        self.assertEqual(score, 20)
    
    def test_10th_open_no_bonus(self):
        """Test open frame in 10th (no bonus)."""
        rolls = [0] * 18 + [5, 3]
        score = calculate_score(rolls)
        self.assertEqual(score, 8)


if __name__ == '__main__':
    # Run tests
    unittest.main(verbosity=2)