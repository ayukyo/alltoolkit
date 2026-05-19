#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AllToolkit - Gamification Utilities Test
=========================================
Comprehensive tests for gamification_utils module.
"""

import unittest
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from datetime import datetime, timedelta
from mod import (
    # Enums
    LevelCurve, RankType, StreakBonusType, RewardType,
    
    # Data classes
    Level, Achievement, Streak, LeaderboardEntry, Challenge, Reward,
    
    # XP and Leveling
    calculate_xp_for_level_linear,
    calculate_xp_for_level_exponential,
    calculate_xp_for_level_sigmoid,
    calculate_xp_for_level_fibonacci,
    calculate_total_xp_for_level,
    calculate_level_from_xp,
    calculate_xp_progress_percentage,
    
    # Level Titles and Tiers
    get_level_title,
    get_tier_emoji,
    get_level_tier,
    DEFAULT_LEVEL_TITLES,
    
    # Streak Tracking
    calculate_streak_multiplier,
    update_streak,
    calculate_streak_bonus_xp,
    
    # Leaderboard
    calculate_rank,
    calculate_percentile,
    get_leaderboard,
    calculate_leaderboard_position,
    
    # Achievement System
    check_achievement_criteria,
    calculate_achievement_progress,
    get_achievements_by_tier,
    calculate_achievement_completion,
    
    # Daily Rewards
    calculate_daily_reward,
    get_daily_reward_sequence,
    
    # Challenges
    calculate_challenge_progress,
    update_challenge_progress,
    is_challenge_expired,
    generate_daily_challenges,
    
    # Points and Currency
    calculate_points_with_level_bonus,
    distribute_rewards,
    calculate_prestige_rewards,
    
    # Progress Visualization
    create_progress_bar,
    create_xp_bar,
)


class TestXPAndLeveling(unittest.TestCase):
    """Test XP and leveling functions."""
    
    def test_calculate_xp_for_level_linear(self):
        """Test linear XP progression."""
        self.assertEqual(calculate_xp_for_level_linear(1), 100)
        self.assertEqual(calculate_xp_for_level_linear(5, 100, 50), 300)
        self.assertEqual(calculate_xp_for_level_linear(1, 50), 50)
    
    def test_calculate_xp_for_level_exponential(self):
        """Test exponential XP progression."""
        self.assertEqual(calculate_xp_for_level_exponential(1, 100, 1.15), 100)
        # Level 5: 100 * 1.15^4 ≈ 174
        result = calculate_xp_for_level_exponential(5, 100, 1.15)
        self.assertEqual(result, 174)
    
    def test_calculate_xp_for_level_fibonacci(self):
        """Test Fibonacci XP progression."""
        self.assertEqual(calculate_xp_for_level_fibonacci(1), 100)
        self.assertEqual(calculate_xp_for_level_fibonacci(2), 100)
        self.assertEqual(calculate_xp_for_level_fibonacci(5), 500)  # 100 * fib(4) = 100 * 5
    
    def test_calculate_total_xp_for_level(self):
        """Test total XP calculation."""
        # Linear: 100 + 150 + 200 + 250 + 300 = 1000
        result = calculate_total_xp_for_level(5, LevelCurve.LINEAR, 100, increment=50)
        self.assertEqual(result, 1000)
    
    def test_calculate_level_from_xp(self):
        """Test level calculation from XP."""
        # With linear progression (100, 150, 200, 250...)
        level, xp_in, xp_need = calculate_level_from_xp(500, LevelCurve.LINEAR, 100, increment=50)
        self.assertEqual(level, 4)
        self.assertEqual(xp_in, 50)
        self.assertEqual(xp_need, 300)  # Level 4 needs 300 XP (100 + 150 + 200)
        
        # Level 1 with 0 XP
        level, xp_in, xp_need = calculate_level_from_xp(0, LevelCurve.LINEAR)
        self.assertEqual(level, 1)
        self.assertEqual(xp_in, 0)
    
    def test_calculate_xp_progress_percentage(self):
        """Test XP progress percentage."""
        result = calculate_xp_progress_percentage(125, LevelCurve.LINEAR, 100, increment=50)
        self.assertEqual(result, 12.5)  # Level 2, 25/200 = 12.5%


class TestLevelTitlesAndTiers(unittest.TestCase):
    """Test level title and tier functions."""
    
    def test_get_level_title(self):
        """Test level title retrieval."""
        self.assertEqual(get_level_title(1), 'Novice')
        self.assertEqual(get_level_title(15), 'Journeyman')
        self.assertEqual(get_level_title(50), 'Grandmaster')
        self.assertEqual(get_level_title(100), 'Godlike')
    
    def test_get_tier_emoji(self):
        """Test tier emoji retrieval."""
        self.assertEqual(get_tier_emoji(1), '🥉')  # Bronze
        self.assertEqual(get_tier_emoji(2), '🥈')  # Silver
        self.assertEqual(get_tier_emoji(3), '🥇')  # Gold
        self.assertEqual(get_tier_emoji(4), '💎')  # Platinum
    
    def test_get_level_tier(self):
        """Test level tier calculation."""
        self.assertEqual(get_level_tier(5), 1)   # Below first threshold (10)
        self.assertEqual(get_level_tier(15), 2)  # Between 10 and 25
        self.assertEqual(get_level_tier(60), 4)  # Between 50 and 75


class TestStreakTracking(unittest.TestCase):
    """Test streak tracking functions."""
    
    def test_calculate_streak_multiplier_linear(self):
        """Test linear streak multiplier."""
        self.assertAlmostEqual(calculate_streak_multiplier(7), 1.7, places=1)
        self.assertEqual(calculate_streak_multiplier(0), 1.0)
    
    def test_calculate_streak_multiplier_exponential(self):
        """Test exponential streak multiplier."""
        result = calculate_streak_multiplier(7, bonus_type=StreakBonusType.EXPONENTIAL)
        self.assertAlmostEqual(result, 1.1, places=1)  # Different formula
    
    def test_calculate_streak_multiplier_cap(self):
        """Test capped streak multiplier."""
        # Cap at 5.0 with 0.1 per day, max streak = 40
        result = calculate_streak_multiplier(100, bonus_type=StreakBonusType.CAP, max_multiplier=5.0)
        self.assertEqual(result, 5.0)
    
    def test_update_streak_continue(self):
        """Test streak continuation."""
        streak = Streak(current=5, best=10, last_activity=datetime.now() - timedelta(days=1))
        updated = update_streak(streak)
        self.assertEqual(updated.current, 6)
        self.assertEqual(updated.best, 10)
    
    def test_update_streak_break(self):
        """Test streak break."""
        streak = Streak(current=5, best=10, last_activity=datetime.now() - timedelta(days=3))
        updated = update_streak(streak)
        self.assertEqual(updated.current, 1)
    
    def test_calculate_streak_bonus_xp(self):
        """Test streak bonus XP."""
        result = calculate_streak_bonus_xp(100, 7)
        self.assertEqual(result, 170)


class TestLeaderboard(unittest.TestCase):
    """Test leaderboard functions."""
    
    def test_calculate_rank(self):
        """Test rank calculation."""
        self.assertEqual(calculate_rank(85, [100, 95, 85, 80, 75]), 3)
        self.assertEqual(calculate_rank(100, [100, 95, 85]), 1)
    
    def test_calculate_percentile(self):
        """Test percentile calculation."""
        result = calculate_percentile(85, [70, 75, 80, 85, 90, 95, 100])
        self.assertAlmostEqual(result, 42.86, places=1)
    
    def test_get_leaderboard(self):
        """Test leaderboard sorting."""
        entries = [
            LeaderboardEntry('u1', 'Alice', 100, 1),
            LeaderboardEntry('u2', 'Bob', 150, 1),
            LeaderboardEntry('u3', 'Charlie', 120, 1),
        ]
        board = get_leaderboard(entries)
        self.assertEqual(board[0].username, 'Bob')
        self.assertEqual(board[0].rank, 1)
        self.assertEqual(board[1].username, 'Charlie')
        self.assertEqual(board[1].rank, 2)
    
    def test_calculate_leaderboard_position(self):
        """Test finding user position."""
        entries = [
            LeaderboardEntry('u1', 'Alice', 100, 1),
            LeaderboardEntry('u2', 'Bob', 150, 2),
        ]
        board = get_leaderboard(entries)
        pos = calculate_leaderboard_position('u1', board)
        self.assertEqual(pos, 2)


class TestAchievementSystem(unittest.TestCase):
    """Test achievement system functions."""
    
    def test_check_achievement_criteria_threshold(self):
        """Test threshold achievement criteria."""
        self.assertTrue(check_achievement_criteria(10, {'type': 'threshold', 'value': 10}))
        self.assertFalse(check_achievement_criteria(5, {'type': 'threshold', 'value': 10}))
    
    def test_check_achievement_criteria_range(self):
        """Test range achievement criteria."""
        criteria = {'type': 'range', 'min': 5, 'max': 15}
        self.assertTrue(check_achievement_criteria(10, criteria))
        self.assertFalse(check_achievement_criteria(20, criteria))
    
    def test_check_achievement_criteria_streak(self):
        """Test streak achievement criteria."""
        self.assertTrue(check_achievement_criteria(7, {'type': 'streak', 'value': 7}))
        self.assertFalse(check_achievement_criteria(5, {'type': 'streak', 'value': 7}))
    
    def test_calculate_achievement_progress(self):
        """Test achievement progress calculation."""
        result = calculate_achievement_progress(50, {'type': 'threshold', 'value': 100})
        self.assertEqual(result, 50.0)
        
        result = calculate_achievement_progress(100, {'type': 'threshold', 'value': 100})
        self.assertEqual(result, 100.0)
    
    def test_achievement_unlock(self):
        """Test achievement unlock."""
        achievement = Achievement('test', 'Test', 'Description', tier=1)
        achievement.unlock()
        self.assertIsNotNone(achievement.unlocked_at)
    
    def test_get_achievements_by_tier(self):
        """Test grouping achievements by tier."""
        a1 = Achievement('a1', 'Test1', 'Desc', tier=1)
        a2 = Achievement('a2', 'Test2', 'Desc', tier=2)
        a3 = Achievement('a3', 'Test3', 'Desc', tier=1, unlocked_at=datetime.now())
        
        result = get_achievements_by_tier([a1, a2, a3])
        self.assertEqual(len(result[1]), 2)
        self.assertEqual(len(result[2]), 1)
        
        result_unlocked = get_achievements_by_tier([a1, a2, a3], unlocked_only=True)
        self.assertEqual(len(result_unlocked[1]), 1)
    
    def test_calculate_achievement_completion(self):
        """Test achievement completion calculation."""
        a1 = Achievement('a1', 'Test', 'Desc', tier=1, unlocked_at=datetime.now())
        a2 = Achievement('a2', 'Test2', 'Desc', tier=1)
        result = calculate_achievement_completion([a1, a2])
        self.assertEqual(result['total'], 2)
        self.assertEqual(result['unlocked'], 1)
        self.assertEqual(result['completion'], 50.0)


class TestDailyRewards(unittest.TestCase):
    """Test daily reward functions."""
    
    def test_calculate_daily_reward(self):
        """Test daily reward calculation."""
        self.assertEqual(calculate_daily_reward(1, 10), 10)
        # Day 7 has special bonus
        result = calculate_daily_reward(7, 10)
        self.assertTrue(result > 10)  # Day 7 has bonus
    
    def test_get_daily_reward_sequence(self):
        """Test daily reward sequence."""
        sequence = get_daily_reward_sequence(7, 10)
        self.assertEqual(len(sequence), 7)
        self.assertEqual(sequence[0]['day'], 1)
        self.assertEqual(sequence[6]['is_special'], True)


class TestChallenges(unittest.TestCase):
    """Test challenge functions."""
    
    def test_calculate_challenge_progress(self):
        """Test challenge progress calculation."""
        challenge = Challenge('test', 'Test', 'Desc', target=100, current=50)
        progress = calculate_challenge_progress(challenge)
        self.assertEqual(progress, 50.0)
    
    def test_update_challenge_progress(self):
        """Test challenge progress update."""
        challenge = Challenge('test', 'Test', 'Desc', target=100, current=50)
        updated = update_challenge_progress(challenge, 50)
        self.assertEqual(updated.current, 100)
        self.assertTrue(updated.is_completed)
    
    def test_is_challenge_expired(self):
        """Test challenge expiration check."""
        # Not expired
        challenge = Challenge('test', 'Test', 'Desc', target=10, 
                             expires_at=datetime.now() + timedelta(hours=1))
        self.assertFalse(is_challenge_expired(challenge))
        
        # Expired
        challenge = Challenge('test', 'Test', 'Desc', target=10,
                             expires_at=datetime.now() - timedelta(hours=1))
        self.assertTrue(is_challenge_expired(challenge))
    
    def test_generate_daily_challenges(self):
        """Test daily challenge generation."""
        challenges = generate_daily_challenges(3)
        self.assertEqual(len(challenges), 3)
        for c in challenges:
            self.assertTrue(c.is_daily)


class TestPointsAndCurrency(unittest.TestCase):
    """Test points and currency functions."""
    
    def test_calculate_points_with_level_bonus(self):
        """Test level bonus on points."""
        result = calculate_points_with_level_bonus(100, 10, 0.01)
        self.assertEqual(result, 110)
    
    def test_distribute_rewards_equal(self):
        """Test equal reward distribution."""
        result = distribute_rewards(100, ['a', 'b', 'c'])
        self.assertEqual(result['a'], 33)
        self.assertEqual(result['b'], 33)
        self.assertEqual(result['c'], 34)  # Remainder
    
    def test_distribute_rewards_weighted(self):
        """Test weighted reward distribution."""
        result = distribute_rewards(100, ['a', 'b', 'c'], [0.5, 0.3, 0.2])
        self.assertEqual(result['a'], 50)
        self.assertEqual(result['b'], 30)
        self.assertEqual(result['c'], 20)
    
    def test_calculate_prestige_rewards(self):
        """Test prestige rewards."""
        result = calculate_prestige_rewards(50, 50000)
        self.assertEqual(result['prestige_points'], 5)
        self.assertEqual(result['prestige_currency'], 50)


class TestProgressVisualization(unittest.TestCase):
    """Test progress visualization functions."""
    
    def test_create_progress_bar(self):
        """Test progress bar creation."""
        result = create_progress_bar(50, 100, 10)
        self.assertIn('█████', result)
        self.assertIn('50%', result)
    
    def test_create_xp_bar(self):
        """Test XP bar creation."""
        result = create_xp_bar(150, LevelCurve.LINEAR, 100, 10, increment=50)
        self.assertIn('Lv 2', result)


class TestDataClasses(unittest.TestCase):
    """Test data classes."""
    
    def test_level_dataclass(self):
        """Test Level dataclass."""
        level = Level(number=5, xp_required=300, xp_total=1000, title='Journeyman')
        self.assertEqual(level.number, 5)
        self.assertEqual(level.title, 'Journeyman')
    
    def test_reward_dataclass(self):
        """Test Reward dataclass."""
        reward = Reward(RewardType.XP, 100)
        self.assertEqual(reward.type, RewardType.XP)
        self.assertEqual(reward.amount, 100)
    
    def test_challenge_dataclass(self):
        """Test Challenge dataclass."""
        challenge = Challenge('test', 'Test', 'Desc', target=100)
        self.assertEqual(challenge.id, 'test')
        self.assertEqual(challenge.target, 100)


if __name__ == '__main__':
    unittest.main()