#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AllToolkit - Gamification Utilities Tests
==========================================
Comprehensive tests for gamification_utils module.
"""

import unittest
from datetime import datetime, timedelta
from mod import (
    # Enums
    LevelCurve, RankType, StreakBonusType, RewardType,
    # Data classes
    Level, Achievement, Streak, LeaderboardEntry, Challenge, Reward,
    # XP and Leveling
    calculate_xp_for_level_linear, calculate_xp_for_level_exponential,
    calculate_xp_for_level_sigmoid, calculate_xp_for_level_fibonacci,
    calculate_total_xp_for_level, calculate_level_from_xp,
    calculate_xp_progress_percentage,
    # Titles and Tiers
    get_level_title, get_tier_emoji, get_level_tier,
    DEFAULT_LEVEL_TITLES, TIER_COLORS,
    # Streak
    calculate_streak_multiplier, update_streak,
    calculate_streak_bonus_xp,
    # Leaderboard
    calculate_rank, calculate_percentile,
    get_leaderboard, calculate_leaderboard_position,
    # Achievements
    check_achievement_criteria, calculate_achievement_progress,
    get_achievements_by_tier, calculate_achievement_completion,
    # Daily Rewards
    calculate_daily_reward, get_daily_reward_sequence,
    # Challenges
    calculate_challenge_progress, update_challenge_progress,
    is_challenge_expired, generate_daily_challenges,
    # Points and Currency
    calculate_points_with_level_bonus, distribute_rewards,
    calculate_prestige_rewards,
    # Progress Visualization
    create_progress_bar, create_xp_bar,
)


class TestXPAndLeveling(unittest.TestCase):
    """Test XP calculation and leveling functions."""
    
    def test_calculate_xp_for_level_linear(self):
        self.assertEqual(calculate_xp_for_level_linear(1), 100)
        self.assertEqual(calculate_xp_for_level_linear(1, 50), 50)
        self.assertEqual(calculate_xp_for_level_linear(5, 100, 50), 300)
        
    def test_calculate_xp_for_level_exponential(self):
        self.assertEqual(calculate_xp_for_level_exponential(1), 100)
        # Level 5 with growth rate 1.15: 100 * 1.15^4
        result = calculate_xp_for_level_exponential(5, 100, 1.15)
        self.assertAlmostEqual(result, 174, places=0)
        
    def test_calculate_xp_for_level_sigmoid(self):
        # Level 1 should return base_xp
        result = calculate_xp_for_level_sigmoid(1, 100, 100, 10000)
        self.assertEqual(result, 100)
        
        # Higher levels have higher XP requirements
        result_high = calculate_xp_for_level_sigmoid(50, 100, 100, 10000)
        result_low = calculate_xp_for_level_sigmoid(20, 100, 100, 10000)
        self.assertGreater(result_high, result_low)
        
    def test_calculate_xp_for_level_fibonacci(self):
        self.assertEqual(calculate_xp_for_level_fibonacci(1), 100)
        self.assertEqual(calculate_xp_for_level_fibonacci(2), 100)
        # Level 5: Fibonacci calculation result
        self.assertEqual(calculate_xp_for_level_fibonacci(5), 500)
        # Level 6: Fibonacci calculation result
        self.assertEqual(calculate_xp_for_level_fibonacci(6), 800)
        
    def test_calculate_total_xp_for_level(self):
        # Linear: 100 + 150 + 200 + 250 + 300 = 1000
        total = calculate_total_xp_for_level(5, LevelCurve.LINEAR, 100, increment=50)
        self.assertEqual(total, 1000)
        
        # Exponential total
        total_exp = calculate_total_xp_for_level(5, LevelCurve.EXPONENTIAL, 100)
        self.assertGreater(total_exp, 500)
        
    def test_calculate_level_from_xp(self):
        # XP calculation: Level 1=100, L2=150, L3=200, L4=250, L5=300, L6=350, L7=400
        # Total for level 1: 100, level 2: 250, level 3: 450, level 4: 700, level 5: 1000
        level, xp_in, xp_need = calculate_level_from_xp(1000, LevelCurve.LINEAR, 100, increment=50)
        self.assertEqual(level, 6)  # 1000 XP reaches level 6 boundary
        self.assertEqual(xp_in, 0)  # Exactly at boundary
        self.assertEqual(xp_need, 400)  # Next level (7) needs 400
        
        # Partial level progress: 500 XP (at level 4, 50 XP into level)
        level, xp_in, xp_need = calculate_level_from_xp(500, LevelCurve.LINEAR, 100, increment=50)
        self.assertEqual(level, 4)
        self.assertEqual(xp_in, 50)  # Into level 4 by 50 XP (500 - 450)
        self.assertEqual(xp_need, 300)  # Next level (5) needs 300
        
    def test_calculate_level_from_xp_zero(self):
        level, xp_in, xp_need = calculate_level_from_xp(0, LevelCurve.LINEAR)
        self.assertEqual(level, 1)
        
    def test_calculate_xp_progress_percentage(self):
        # 125 XP: level 2 (total for L1=100, L2 needs 150)
        # xp_into = 125-100 = 25, next level needs 200
        # progress = 25/200 * 100 = 12.5%
        percent = calculate_xp_progress_percentage(125, LevelCurve.LINEAR, 100, increment=50)
        self.assertAlmostEqual(percent, 12.5, places=1)
        
    def test_calculate_level_from_xp_max_level(self):
        # High XP with max level cap
        level, xp_in, xp_need = calculate_level_from_xp(1000000, LevelCurve.LINEAR, 100, 
                                                        max_level=50, increment=50)
        self.assertEqual(level, 50)


class TestLevelTitlesAndTiers(unittest.TestCase):
    """Test level titles and tier functions."""
    
    def test_get_level_title(self):
        self.assertEqual(get_level_title(1), 'Novice')
        self.assertEqual(get_level_title(8), 'Apprentice')
        self.assertEqual(get_level_title(15), 'Journeyman')
        self.assertEqual(get_level_title(50), 'Grandmaster')
        self.assertEqual(get_level_title(100), 'Godlike')
        
    def test_get_level_title_custom(self):
        custom_titles = {(1, 10): 'Beginner', (11, 20): 'Pro'}
        self.assertEqual(get_level_title(5, custom_titles), 'Beginner')
        self.assertEqual(get_level_title(15, custom_titles), 'Pro')
        
    def test_get_tier_emoji(self):
        self.assertEqual(get_tier_emoji(1), '🥉')
        self.assertEqual(get_tier_emoji(2), '🥈')
        self.assertEqual(get_tier_emoji(3), '🥇')
        self.assertEqual(get_tier_emoji(4), '💎')
        self.assertEqual(get_tier_emoji(5), '💠')
        
    def test_get_level_tier(self):
        self.assertEqual(get_level_tier(1), 1)
        self.assertEqual(get_level_tier(15), 2)
        self.assertEqual(get_level_tier(30), 3)
        self.assertEqual(get_level_tier(60), 4)
        self.assertEqual(get_level_tier(90), 5)
        
    def test_get_level_tier_custom_thresholds(self):
        thresholds = [5, 10, 20, 30, 40]
        self.assertEqual(get_level_tier(3, thresholds), 1)
        self.assertEqual(get_level_tier(7, thresholds), 2)


class TestStreakTracking(unittest.TestCase):
    """Test streak calculation functions."""
    
    def test_calculate_streak_multiplier_linear(self):
        self.assertEqual(calculate_streak_multiplier(0), 1.0)
        # 7 days * 0.1 = 0.7 bonus, so 1.7 total
        self.assertAlmostEqual(calculate_streak_multiplier(7), 1.7)
        
    def test_calculate_streak_multiplier_max(self):
        # Very high streak should be capped
        result = calculate_streak_multiplier(1000, max_multiplier=5.0)
        self.assertLessEqual(result, 5.0)
        
    def test_calculate_streak_multiplier_exponential(self):
        # Exponential growth with base 0.1 per 7 days
        result = calculate_streak_multiplier(7, bonus_type=StreakBonusType.EXPONENTIAL)
        self.assertGreater(result, 1.0)  # At least some bonus
        
    def test_calculate_streak_multiplier_threshold(self):
        # Threshold-based bonus
        result = calculate_streak_multiplier(30, bonus_type=StreakBonusType.THRESHOLD)
        self.assertGreater(result, 1.0)
        
    def test_update_streak_first_activity(self):
        streak = Streak()
        updated = update_streak(streak)
        self.assertEqual(updated.current, 1)
        self.assertEqual(updated.best, 1)
        
    def test_update_streak_continue(self):
        streak = Streak(current=5, best=10, last_activity=datetime.now() - timedelta(hours=25))
        updated = update_streak(streak)
        self.assertEqual(updated.current, 6)
        self.assertEqual(updated.best, 10)
        
    def test_update_streak_break(self):
        streak = Streak(current=5, best=10, last_activity=datetime.now() - timedelta(days=3))
        updated = update_streak(streak)
        self.assertEqual(updated.current, 1)
        
    def test_update_streak_grace_period(self):
        streak = Streak(current=5, best=10, last_activity=datetime.now() - timedelta(hours=12))
        updated = update_streak(streak, grace_hours=24)
        self.assertEqual(updated.current, 5)  # No change, within grace
        
    def test_calculate_streak_bonus_xp(self):
        # 7-day streak with 0.1 bonus = 1.7 multiplier
        # 100 * 1.7 = 170
        result = calculate_streak_bonus_xp(100, 7)
        self.assertEqual(result, 170)


class TestLeaderboard(unittest.TestCase):
    """Test leaderboard functions."""
    
    def test_calculate_rank(self):
        scores = [100, 95, 85, 80, 75]
        self.assertEqual(calculate_rank(100, scores), 1)
        self.assertEqual(calculate_rank(85, scores), 3)
        self.assertEqual(calculate_rank(70, scores), 6)
        
    def test_calculate_percentile(self):
        scores = [70, 75, 80, 85, 90, 95, 100]
        result = calculate_percentile(85, scores)
        self.assertAlmostEqual(result, 42.86, places=1)
        
    def test_get_leaderboard(self):
        entries = [
            LeaderboardEntry('u1', 'Alice', 100, 1),
            LeaderboardEntry('u2', 'Bob', 150, 1),
            LeaderboardEntry('u3', 'Charlie', 120, 1),
        ]
        board = get_leaderboard(entries, sort_by='score')
        
        self.assertEqual(board[0].username, 'Bob')
        self.assertEqual(board[0].rank, 1)
        self.assertEqual(board[1].username, 'Charlie')
        self.assertEqual(board[1].rank, 2)
        self.assertEqual(board[2].username, 'Alice')
        self.assertEqual(board[2].rank, 3)
        
    def test_get_leaderboard_limit(self):
        entries = [
            LeaderboardEntry('u1', 'Alice', 100, 1),
            LeaderboardEntry('u2', 'Bob', 150, 1),
            LeaderboardEntry('u3', 'Charlie', 120, 1),
        ]
        board = get_leaderboard(entries, sort_by='score', limit=2)
        self.assertEqual(len(board), 2)
        
    def test_calculate_leaderboard_position(self):
        entries = [
            LeaderboardEntry('u1', 'Alice', 100, 1),
            LeaderboardEntry('u2', 'Bob', 150, 2),
            LeaderboardEntry('u3', 'Charlie', 120, 3),
        ]
        board = get_leaderboard(entries)
        position = calculate_leaderboard_position('u1', board)
        self.assertEqual(position, 3)


class TestAchievements(unittest.TestCase):
    """Test achievement functions."""
    
    def test_check_achievement_criteria_threshold(self):
        criteria = {'type': 'threshold', 'value': 10}
        self.assertTrue(check_achievement_criteria(10, criteria))
        self.assertTrue(check_achievement_criteria(15, criteria))
        self.assertFalse(check_achievement_criteria(5, criteria))
        
    def test_check_achievement_criteria_range(self):
        criteria = {'type': 'range', 'min': 10, 'max': 20}
        self.assertTrue(check_achievement_criteria(15, criteria))
        self.assertFalse(check_achievement_criteria(5, criteria))
        self.assertFalse(check_achievement_criteria(25, criteria))
        
    def test_check_achievement_criteria_exact(self):
        criteria = {'type': 'exact', 'value': 100}
        self.assertTrue(check_achievement_criteria(100, criteria))
        self.assertFalse(check_achievement_criteria(99, criteria))
        
    def test_check_achievement_criteria_percentage(self):
        criteria = {'type': 'percentage', 'value': 80, 'base': 100}
        self.assertTrue(check_achievement_criteria(80, criteria))
        self.assertFalse(check_achievement_criteria(70, criteria))
        
    def test_check_achievement_criteria_streak(self):
        criteria = {'type': 'streak', 'value': 7}
        self.assertTrue(check_achievement_criteria(7, criteria))
        self.assertTrue(check_achievement_criteria(10, criteria))
        self.assertFalse(check_achievement_criteria(5, criteria))
        
    def test_calculate_achievement_progress(self):
        criteria = {'type': 'threshold', 'value': 100}
        result = calculate_achievement_progress(50, criteria)
        self.assertEqual(result, 50.0)
        
    def test_achievement_unlock(self):
        achievement = Achievement('test', 'Test', 'Test achievement')
        achievement.unlock()
        self.assertIsNotNone(achievement.unlocked_at)
        
    def test_get_achievements_by_tier(self):
        achievements = [
            Achievement('a1', 'A1', 'Desc', tier=1),
            Achievement('a2', 'A2', 'Desc', tier=2, unlocked_at=datetime.now()),
            Achievement('a3', 'A3', 'Desc', tier=1, unlocked_at=datetime.now()),
        ]
        by_tier = get_achievements_by_tier(achievements)
        self.assertEqual(len(by_tier[1]), 2)
        self.assertEqual(len(by_tier[2]), 1)
        
        by_tier_unlocked = get_achievements_by_tier(achievements, unlocked_only=True)
        self.assertEqual(len(by_tier_unlocked[1]), 1)
        self.assertEqual(len(by_tier_unlocked[2]), 1)
        
    def test_calculate_achievement_completion(self):
        achievements = [
            Achievement('a1', 'A1', 'Desc', tier=1, xp_reward=50, unlocked_at=datetime.now()),
            Achievement('a2', 'A2', 'Desc', tier=1, xp_reward=100),
            Achievement('a3', 'A3', 'Desc', tier=2, xp_reward=200, unlocked_at=datetime.now()),
        ]
        result = calculate_achievement_completion(achievements)
        
        self.assertEqual(result['total'], 3)
        self.assertEqual(result['unlocked'], 2)
        self.assertAlmostEqual(result['completion'], 66.67, places=1)
        self.assertEqual(result['total_xp_earned'], 250)


class TestDailyRewards(unittest.TestCase):
    """Test daily reward functions."""
    
    def test_calculate_daily_reward(self):
        # Day 1: base = 10
        self.assertEqual(calculate_daily_reward(1, 10), 10)
        
        # Day 7 with special bonus: base + streak + 100 special
        result = calculate_daily_reward(7, 10, 0.1, 7, {7: 100})
        # 10 * (1 + 0.1 * 6) = 16, + 100 = 116
        self.assertEqual(result, 116)
        
    def test_get_daily_reward_sequence(self):
        sequence = get_daily_reward_sequence(7, 10, 0.1, {7: 100})
        self.assertEqual(len(sequence), 7)
        self.assertEqual(sequence[0]['day'], 1)
        self.assertEqual(sequence[6]['is_special'], True)
        
    def test_daily_reward_cycle(self):
        # Day 8 should cycle back to day 1
        result = calculate_daily_reward(8, 10, 0.1, 7)
        self.assertEqual(result, 10)  # Day 1 reward


class TestChallenges(unittest.TestCase):
    """Test challenge functions."""
    
    def test_calculate_challenge_progress(self):
        challenge = Challenge('c1', 'Test', 'Test challenge', target=10, current=5)
        progress = calculate_challenge_progress(challenge)
        self.assertEqual(progress, 50.0)
        
    def test_update_challenge_progress(self):
        challenge = Challenge('c1', 'Test', 'Test challenge', target=10, current=5)
        updated = update_challenge_progress(challenge, 5)
        self.assertEqual(updated.current, 10)
        self.assertTrue(updated.is_completed)
        
    def test_is_challenge_expired(self):
        challenge = Challenge('c1', 'Test', 'Test', target=10,
                              expires_at=datetime.now() - timedelta(hours=1))
        self.assertTrue(is_challenge_expired(challenge))
        
        challenge2 = Challenge('c2', 'Test', 'Test', target=10,
                               expires_at=datetime.now() + timedelta(hours=1))
        self.assertFalse(is_challenge_expired(challenge2))
        
    def test_generate_daily_challenges(self):
        challenges = generate_daily_challenges(3)
        self.assertEqual(len(challenges), 3)
        for c in challenges:
            self.assertTrue(c.is_daily)
            self.assertIsNotNone(c.expires_at)


class TestPointsAndCurrency(unittest.TestCase):
    """Test points and currency functions."""
    
    def test_calculate_points_with_level_bonus(self):
        # Level 10 with 1% per level = 10% bonus
        result = calculate_points_with_level_bonus(100, 10, 0.01)
        self.assertEqual(result, 110)
        
    def test_calculate_points_with_level_bonus_max(self):
        # Very high level with max bonus cap
        result = calculate_points_with_level_bonus(100, 100, 0.01, 0.5)
        self.assertEqual(result, 150)  # Capped at 50%
        
    def test_distribute_rewards_equal(self):
        result = distribute_rewards(100, ['a', 'b', 'c', 'd'])
        self.assertEqual(result['a'], 25)
        self.assertEqual(result['d'], 25)
        
    def test_distribute_rewards_weighted(self):
        result = distribute_rewards(100, ['a', 'b', 'c'], [0.5, 0.3, 0.2])
        self.assertEqual(result['a'], 50)
        self.assertEqual(result['b'], 30)
        self.assertEqual(result['c'], 20)
        
    def test_calculate_prestige_rewards(self):
        result = calculate_prestige_rewards(50, 50000)
        self.assertEqual(result['prestige_points'], 5)
        self.assertEqual(result['prestige_currency'], 50)  # 50000 * 0.1 / 100


class TestProgressVisualization(unittest.TestCase):
    """Test progress visualization functions."""
    
    def test_create_progress_bar(self):
        bar = create_progress_bar(50, 100, 10, show_percent=True)
        self.assertIn('50%', bar)
        
    def test_create_progress_bar_width(self):
        bar = create_progress_bar(50, 100, 10, show_percent=False)
        # 50/100 = 50%, 10 chars * 50% = 5 filled
        self.assertEqual(len(bar.replace('█', '').replace('░', '')), 0)
        self.assertEqual(bar.count('█'), 5)
        self.assertEqual(bar.count('░'), 5)
        
    def test_create_progress_bar_full(self):
        bar = create_progress_bar(100, 100, 10)
        self.assertIn('100%', bar)
        
    def test_create_xp_bar(self):
        bar = create_xp_bar(500, LevelCurve.LINEAR, 100, 10, increment=50)
        self.assertIn('Lv', bar)
        self.assertIn('%', bar)


class TestEnums(unittest.TestCase):
    """Test enum values."""
    
    def test_level_curve_enum(self):
        self.assertEqual(LevelCurve.LINEAR.value, 'linear')
        self.assertEqual(LevelCurve.EXPONENTIAL.value, 'exponential')
        
    def test_rank_type_enum(self):
        self.assertEqual(RankType.NUMERIC.value, 'numeric')
        self.assertEqual(RankType.PERCENTILE.value, 'percentile')
        
    def test_streak_bonus_type_enum(self):
        self.assertEqual(StreakBonusType.LINEAR.value, 'linear')
        self.assertEqual(StreakBonusType.EXPONENTIAL.value, 'exponential')
        
    def test_reward_type_enum(self):
        self.assertEqual(RewardType.XP.value, 'xp')
        self.assertEqual(RewardType.CURRENCY.value, 'currency')


class TestDataClasses(unittest.TestCase):
    """Test data class functionality."""
    
    def test_level_dataclass(self):
        level = Level(number=5, xp_required=300, xp_total=1000, title='Expert')
        self.assertEqual(level.number, 5)
        self.assertEqual(level.xp_required, 300)
        
    def test_streak_dataclass(self):
        streak = Streak(current=10, best=15, multiplier=1.5)
        self.assertEqual(streak.current, 10)
        self.assertEqual(streak.best, 15)
        
    def test_leaderboard_entry_dataclass(self):
        entry = LeaderboardEntry('u1', 'Alice', 1000, 1, level=25)
        self.assertEqual(entry.user_id, 'u1')
        self.assertEqual(entry.score, 1000)
        
    def test_challenge_dataclass(self):
        challenge = Challenge('c1', 'Test', 'Test', target=10)
        self.assertEqual(challenge.id, 'c1')
        self.assertEqual(challenge.target, 10)
        
    def test_reward_dataclass(self):
        reward = Reward(RewardType.XP, 100)
        self.assertEqual(reward.type, RewardType.XP)
        self.assertEqual(reward.amount, 100)


if __name__ == '__main__':
    unittest.main(verbosity=2)