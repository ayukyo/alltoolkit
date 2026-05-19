#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AllToolkit - Gamification Utilities Examples
=============================================
Example usage scenarios for the gamification_utils module.
"""

from datetime import datetime, timedelta
from mod import (
    # Enums
    LevelCurve, StreakBonusType, RankType, RewardType,
    # Data classes
    Achievement, Streak, LeaderboardEntry, Challenge,
    # XP and Leveling
    calculate_xp_for_level_linear, calculate_xp_for_level_exponential,
    calculate_total_xp_for_level, calculate_level_from_xp,
    calculate_xp_progress_percentage,
    # Titles
    get_level_title, get_tier_emoji, get_level_tier,
    # Streak
    calculate_streak_multiplier, update_streak, calculate_streak_bonus_xp,
    # Leaderboard
    get_leaderboard, calculate_percentile,
    # Achievements
    check_achievement_criteria, calculate_achievement_progress,
    calculate_achievement_completion,
    # Daily Rewards
    get_daily_reward_sequence, calculate_daily_reward,
    # Challenges
    generate_daily_challenges, update_challenge_progress,
    # Points
    calculate_points_with_level_bonus, distribute_rewards,
    calculate_prestige_rewards,
    # Visualization
    create_progress_bar, create_xp_bar,
)


def example_leveling_system():
    """
    Example: Setting up a leveling system for a game/app.
    """
    print("\n=== Example: Leveling System ===")
    
    # Different leveling curves
    print("Leveling Curves Comparison (Levels 1-10):")
    for level in range(1, 11):
        linear = calculate_xp_for_level_linear(level, 100, 50)
        exponential = calculate_xp_for_level_exponential(level, 100, 1.15)
        
        print(f"  Level {level}: Linear={linear}, Exp={exponential}")
    
    # Calculate total XP needed
    total_linear = calculate_total_xp_for_level(10, LevelCurve.LINEAR, 100, increment=50)
    total_exp = calculate_total_xp_for_level(10, LevelCurve.EXPONENTIAL, 100)
    
    print(f"\nTotal XP to reach Level 10:")
    print(f"  Linear: {total_linear}")
    print(f"  Exponential: {total_exp}")
    
    # Current level from XP
    current_xp = 850
    level, xp_in_level, xp_for_next = calculate_level_from_xp(
        current_xp, LevelCurve.LINEAR, 100, increment=50
    )
    
    print(f"\nPlayer with {current_xp} XP:")
    print(f"  Level: {level} ({get_level_title(level)})")
    print(f"  Progress: {xp_in_level}/{xp_for_next} XP")
    print(f"  Tier: {get_tier_emoji(get_level_tier(level))}")
    
    # Progress bar visualization
    print(f"  {create_xp_bar(current_xp, LevelCurve.LINEAR, 100, 20, increment=50)}")


def example_streak_system():
    """
    Example: Streak tracking for daily activities.
    """
    print("\n=== Example: Streak Tracking System ===")
    
    # Create a streak
    streak = Streak(current=7, best=30, last_activity=datetime.now() - timedelta(hours=25))
    
    # Update streak (simulate user activity today)
    updated_streak = update_streak(streak)
    
    print(f"Original streak: {streak.current} days")
    print(f"Updated streak: {updated_streak.current} days")
    print(f"Best streak: {updated_streak.best} days")
    
    # Calculate multiplier
    multiplier = calculate_streak_multiplier(updated_streak.current)
    print(f"XP Multiplier: {multiplier:.2f}x")
    
    # Apply multiplier to earned XP
    base_xp = 100
    bonus_xp = calculate_streak_bonus_xp(base_xp, updated_streak.current)
    print(f"Earned {base_xp} base XP → {bonus_xp} total XP (with streak bonus)")
    
    # Different bonus types
    print("\nStreak Bonus Comparison:")
    streaks = [1, 7, 14, 30, 100]
    for s in streaks:
        linear = calculate_streak_multiplier(s, bonus_type=StreakBonusType.LINEAR)
        exponential = calculate_streak_multiplier(s, bonus_type=StreakBonusType.EXPONENTIAL)
        threshold = calculate_streak_multiplier(s, bonus_type=StreakBonusType.THRESHOLD)
        print(f"  {s} days: Linear={linear:.2f}x, Exp={exponential:.2f}x, Threshold={threshold:.2f}x")


def example_achievement_system():
    """
    Example: Achievement and badge system.
    """
    print("\n=== Example: Achievement System ===")
    
    # Define achievements
    achievements = [
        Achievement('first_login', 'First Steps', 'Log in for the first time',
                   xp_reward=50, tier=1, criteria={'type': 'threshold', 'value': 1}),
        Achievement('week_warrior', 'Week Warrior', 'Maintain a 7-day streak',
                   xp_reward=100, tier=2, criteria={'type': 'streak', 'value': 7}),
        Achievement('month_master', 'Month Master', 'Maintain a 30-day streak',
                   xp_reward=500, tier=3, criteria={'type': 'streak', 'value': 30}),
        Achievement('xp_hunter', 'XP Hunter', 'Earn 1000 total XP',
                   xp_reward=200, tier=2, criteria={'type': 'threshold', 'value': 1000}),
        Achievement('level_10', 'Rising Star', 'Reach level 10',
                   xp_reward=150, tier=2, criteria={'type': 'threshold', 'value': 10}),
    ]
    
    # Check progress on achievements
    player_data = {
        'logins': 1,
        'streak': 14,
        'total_xp': 500,
        'level': 5,
    }
    
    print("Achievement Progress:")
    for achievement in achievements:
        criteria_type = achievement.criteria.get('type')
        if criteria_type == 'threshold':
            current = player_data.get('total_xp', 0) if achievement.id == 'xp_hunter' else \
                     player_data.get('level', 1) if achievement.id == 'level_10' else \
                     player_data.get('logins', 0)
        elif criteria_type == 'streak':
            current = player_data.get('streak', 0)
        else:
            current = 0
        
        progress = calculate_achievement_progress(current, achievement.criteria)
        unlocked = check_achievement_criteria(current, achievement.criteria)
        
        tier_emoji = get_tier_emoji(achievement.tier)
        status = "✓ UNLOCKED" if unlocked else f"{progress:.0f}%"
        
        print(f"  {tier_emoji} {achievement.name}: {status}")
    
    # Unlock achievements that are met
    for achievement in achievements:
        criteria_type = achievement.criteria.get('type')
        current = player_data.get('streak', 0) if criteria_type == 'streak' else \
                 player_data.get('logins', 0) if achievement.id == 'first_login' else \
                 player_data.get('total_xp', 0) if achievement.id == 'xp_hunter' else \
                 player_data.get('level', 1)
        
        if check_achievement_criteria(current, achievement.criteria):
            achievement.unlock()
    
    # Calculate completion
    completion = calculate_achievement_completion(achievements)
    print(f"\nCompletion: {completion['unlocked']}/{completion['total']} ({completion['completion']:.1f}%)")
    print(f"XP Earned from Achievements: {completion['total_xp_earned']}")


def example_leaderboard():
    """
    Example: Leaderboard ranking system.
    """
    print("\n=== Example: Leaderboard System ===")
    
    # Create entries
    entries = [
        LeaderboardEntry('u1', 'Alice', 1500, 0, level=25, streak=14, achievements_count=12),
        LeaderboardEntry('u2', 'Bob', 2300, 0, level=30, streak=7, achievements_count=8),
        LeaderboardEntry('u3', 'Charlie', 1800, 0, level=28, streak=21, achievements_count=15),
        LeaderboardEntry('u4', 'Diana', 2100, 0, level=29, streak=5, achievements_count=10),
        LeaderboardEntry('u5', 'Eve', 1900, 0, level=27, streak=30, achievements_count=20),
    ]
    
    # Sort by score
    leaderboard = get_leaderboard(entries, sort_by='score', limit=5)
    
    print("Top Players (by XP):")
    print("-" * 50)
    for entry in leaderboard:
        print(f"#{entry.rank} {entry.username}: {entry.score} XP")
        print(f"    Level {entry.level} ({get_level_title(entry.level)})")
        print(f"    Streak: {entry.streak} days | Achievements: {entry.achievements_count}")
    
    # Percentile calculation
    scores = [e.score for e in entries]
    alice_percentile = calculate_percentile(1500, scores)
    print(f"\nAlice's percentile: {alice_percentile:.1f}%")
    
    # Sort by streak instead
    streak_leader = get_leaderboard(entries, sort_by='streak', limit=3)
    print("\nTop Streaks:")
    for entry in streak_leader:
        print(f"#{entry.rank} {entry.username}: {entry.streak} days")


def example_daily_rewards():
    """
    Example: Daily login reward system.
    """
    print("\n=== Example: Daily Login Rewards ===")
    
    # 7-day reward cycle
    sequence = get_daily_reward_sequence(7, base_reward=10, streak_bonus=0.1,
                                          special_days={7: 100})
    
    print("7-Day Reward Cycle:")
    print("-" * 40)
    for day in sequence:
        special_marker = "🎁 SPECIAL!" if day['is_special'] else ""
        print(f"  Day {day['day']}: {day['reward']} coins {special_marker}")
    
    # Extended cycle
    print("\nExtended Rewards (30 days):")
    total_rewards = 0
    for day in range(1, 31):
        reward = calculate_daily_reward(day, 10, 0.1, 7, {7: 100})
        total_rewards += reward
        if day % 7 == 0:
            print(f"  Week {day//7} complete: Total rewards so far = {total_rewards} coins")
    
    print(f"  30-day total: {total_rewards} coins")


def example_challenge_system():
    """
    Example: Daily challenge system.
    """
    print("\n=== Example: Challenge System ===")
    
    # Generate daily challenges
    challenges = generate_daily_challenges(3)
    
    print("Today's Challenges:")
    print("-" * 50)
    for challenge in challenges:
        progress = 0  # Start fresh
        bar = create_progress_bar(progress, challenge.target * 100, 20)
        print(f"  {challenge.name}")
        print(f"    {challenge.description}")
        print(f"    Reward: {challenge.xp_reward} XP")
        print(f"    {bar}")
    
    # Simulate progress
    print("\nSimulating Progress:")
    for challenge in challenges:
        # Add some progress
        progress_amount = challenge.target // 2  # 50% progress
        update_challenge_progress(challenge, progress_amount)
        
        bar = create_progress_bar(challenge.current * 100, challenge.target * 100, 20)
        status = "✓ COMPLETE!" if challenge.is_completed else bar
        print(f"  {challenge.name}: {status} (+{challenge.xp_reward} XP)")


def example_reward_distribution():
    """
    Example: Distributing rewards among team/group.
    """
    print("\n=== Example: Reward Distribution ===")
    
    # Equal distribution
    print("Equal Distribution of 1000 coins among 4 players:")
    equal = distribute_rewards(1000, ['Alice', 'Bob', 'Charlie', 'Diana'])
    for player, reward in equal.items():
        print(f"  {player}: {reward} coins")
    
    # Weighted distribution (based on contribution)
    print("\nWeighted Distribution (by contribution):")
    weights = [0.4, 0.3, 0.2, 0.1]  # 40%, 30%, 20%, 10%
    weighted = distribute_rewards(1000, ['Alice', 'Bob', 'Charlie', 'Diana'], weights)
    for player, reward in weighted.items():
        print(f"  {player}: {reward} coins")
    
    # Level-based bonus
    print("\nLevel Bonus on 100 XP:")
    for level in [1, 10, 25, 50]:
        bonus_xp = calculate_points_with_level_bonus(100, level, 0.02)
        print(f"  Level {level}: {bonus_xp} XP (+{(bonus_xp-100)} bonus)")


def example_prestige_system():
    """
    Example: Prestige/reset system for veterans.
    """
    print("\n=== Example: Prestige System ===")
    
    # Calculate prestige rewards for different levels
    print("Prestige Rewards:")
    print("-" * 50)
    
    for level in [50, 75, 100]:
        total_xp = calculate_total_xp_for_level(level, LevelCurve.EXPONENTIAL, 100)
        prestige = calculate_prestige_rewards(level, total_xp)
        
        print(f"Prestiging at Level {level}:")
        print(f"  Total XP earned: {total_xp}")
        print(f"  Prestige points: {prestige['prestige_points']}")
        print(f"  Prestige currency: {prestige['prestige_currency']}")
        print()


def example_full_gamification_profile():
    """
    Example: Complete gamification profile for a user.
    """
    print("\n=== Example: Complete User Profile ===")
    
    # User data
    user_xp = 4500
    user_streak = Streak(current=14, best=30)
    
    # Calculate level
    level, xp_in_level, xp_for_next = calculate_level_from_xp(
        user_xp, LevelCurve.LINEAR, 100, increment=50
    )
    
    # Create achievements
    achievements = [
        Achievement('first_login', 'First Steps', 'First login', tier=1, xp_reward=50, unlocked_at=datetime.now()),
        Achievement('week_warrior', 'Week Warrior', '7-day streak', tier=2, xp_reward=100),
        Achievement('level_10', 'Rising Star', 'Level 10', tier=2, xp_reward=150),
    ]
    
    # Unlock week warrior (14 > 7)
    if user_streak.current >= 7:
        achievements[1].unlock()
    
    print(f"🎮 USER PROFILE")
    print("=" * 50)
    print(f"  Level: {level} {get_tier_emoji(get_level_tier(level))} ({get_level_title(level)})")
    print(f"  XP: {xp_in_level}/{xp_for_next} ({calculate_xp_progress_percentage(user_xp, LevelCurve.LINEAR, 100, increment=50):.1f}%)")
    print(f"  {create_xp_bar(user_xp, LevelCurve.LINEAR, 100, 20, increment=50)}")
    print()
    print(f"  Streak: {user_streak.current} days (best: {user_streak.best})")
    print(f"  Streak Bonus: {calculate_streak_multiplier(user_streak.current):.2f}x")
    print()
    
    completion = calculate_achievement_completion(achievements)
    print(f"  Achievements: {completion['unlocked']}/{completion['total']}")
    for achievement in achievements:
        emoji = get_tier_emoji(achievement.tier)
        status = "✓" if achievement.unlocked_at else "○"
        print(f"    {status} {emoji} {achievement.name}")
    
    print()
    print(f"  Daily Challenge Progress:")
    challenges = generate_daily_challenges(2)
    for challenge in challenges:
        update_challenge_progress(challenge, challenge.target // 2)
        bar = create_progress_bar(challenge.current * 100, challenge.target * 100, 15)
        print(f"    {challenge.name}: {bar}")


def main():
    """Run all examples."""
    print("=" * 60)
    print("AllToolkit - Gamification Utilities Examples")
    print("=" * 60)
    
    example_leveling_system()
    example_streak_system()
    example_achievement_system()
    example_leaderboard()
    example_daily_rewards()
    example_challenge_system()
    example_reward_distribution()
    example_prestige_system()
    example_full_gamification_profile()
    
    print("\n" + "=" * 60)
    print("All examples completed!")
    print("=" * 60)


if __name__ == '__main__':
    main()