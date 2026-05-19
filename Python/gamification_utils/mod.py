#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AllToolkit - Gamification Utilities Module
============================================
A comprehensive gamification utility module with zero external dependencies.

Features:
    - XP (Experience Points) calculation and leveling systems
    - Multiple leveling curve algorithms (linear, exponential, sigmoid)
    - Achievement and badge management
    - Streak tracking with multipliers and bonuses
    - Leaderboard utilities with ranking systems
    - Daily reward and bonus calculations
    - Point and currency systems
    - Challenge and quest management
    - Progress tracking towards goals
    - Reward distribution algorithms

Author: AllToolkit Contributors
License: MIT
"""

import math
from typing import Union, List, Dict, Tuple, Optional, Callable
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime, timedelta


# ============================================================================
# Enums
# ============================================================================

class LevelCurve(Enum):
    """Level curve algorithm types."""
    LINEAR = 'linear'
    EXPONENTIAL = 'exponential'
    SIGMOID = 'sigmoid'
    CUSTOM = 'custom'
    FIBONACCI = 'fibonacci'


class RankType(Enum):
    """Ranking display types."""
    NUMERIC = 'numeric'
    TIER = 'tier'
    PERCENTILE = 'percentile'


class StreakBonusType(Enum):
    """Streak bonus calculation types."""
    LINEAR = 'linear'
    EXPONENTIAL = 'exponential'
    CAP = 'cap'
    THRESHOLD = 'threshold'


class RewardType(Enum):
    """Types of rewards."""
    XP = 'xp'
    CURRENCY = 'currency'
    ITEM = 'item'
    BADGE = 'badge'
    TITLE = 'title'
    MULTIPLIER = 'multiplier'


# ============================================================================
# Data Classes
# ============================================================================

@dataclass
class Level:
    """Represents a level with its properties."""
    number: int
    xp_required: int
    xp_total: int
    title: Optional[str] = None
    rewards: List[Dict] = field(default_factory=list)


@dataclass
class Achievement:
    """Represents an achievement/badge."""
    id: str
    name: str
    description: str
    icon: Optional[str] = None
    xp_reward: int = 0
    currency_reward: int = 0
    is_secret: bool = False
    tier: int = 1  # 1=bronze, 2=silver, 3=gold, 4=platinum
    criteria: Dict = field(default_factory=dict)
    unlocked_at: Optional[datetime] = None
    
    def unlock(self) -> 'Achievement':
        """Unlock this achievement."""
        self.unlocked_at = datetime.now()
        return self


@dataclass
class Streak:
    """Represents a streak with its properties."""
    current: int = 0
    best: int = 0
    last_activity: Optional[datetime] = None
    multiplier: float = 1.0


@dataclass
class LeaderboardEntry:
    """Represents a leaderboard entry."""
    user_id: str
    username: str
    score: float
    rank: int
    level: int = 1
    streak: int = 0
    achievements_count: int = 0
    extra: Dict = field(default_factory=dict)


@dataclass
class Challenge:
    """Represents a challenge or quest."""
    id: str
    name: str
    description: str
    target: int
    current: int = 0
    xp_reward: int = 0
    currency_reward: int = 0
    expires_at: Optional[datetime] = None
    is_completed: bool = False
    is_daily: bool = False


@dataclass
class Reward:
    """Represents a reward."""
    type: RewardType
    amount: int
    item_id: Optional[str] = None
    description: Optional[str] = None


# ============================================================================
# XP and Leveling Systems
# ============================================================================

def calculate_xp_for_level_linear(level: int, base_xp: int = 100, increment: int = 50) -> int:
    """
    Calculate XP required for a level using linear progression.
    
    Formula: base_xp + (level - 1) * increment
    
    Args:
        level: Target level (1-indexed)
        base_xp: XP required for level 1
        increment: XP increase per level
    
    Returns:
        XP required to reach this level from previous
    
    Examples:
        >>> calculate_xp_for_level_linear(1)
        100
        >>> calculate_xp_for_level_linear(5, 100, 50)
        300
    """
    if level <= 1:
        return base_xp
    return base_xp + (level - 1) * increment


def calculate_xp_for_level_exponential(level: int, base_xp: int = 100, 
                                       growth_rate: float = 1.15) -> int:
    """
    Calculate XP required for a level using exponential progression.
    
    Formula: base_xp * (growth_rate ^ (level - 1))
    
    Args:
        level: Target level
        base_xp: XP required for level 1
        growth_rate: Exponential growth multiplier
    
    Returns:
        XP required to reach this level from previous
    
    Examples:
        >>> calculate_xp_for_level_exponential(1, 100, 1.15)
        100
        >>> calculate_xp_for_level_exponential(5, 100, 1.15)
        174
    """
    if level <= 1:
        return base_xp
    return int(base_xp * (growth_rate ** (level - 1)))


def calculate_xp_for_level_sigmoid(level: int, max_level: int = 100,
                                   base_xp: int = 100,
                                   max_xp: int = 10000) -> int:
    """
    Calculate XP using sigmoid curve (slow start, fast middle, slow end).
    
    Good for systems where mid-level progression should be faster.
    
    Args:
        level: Target level
        max_level: Maximum possible level
        base_xp: Minimum XP per level
        max_xp: Maximum XP per level
    
    Returns:
        XP required for this level
    
    Examples:
        >>> calculate_xp_for_level_sigmoid(1, 100, 100, 10000)
        500
    """
    if level <= 1:
        return base_xp
    
    # Sigmoid curve centered at max_level/2
    x = (level - 1) / (max_level - 1)  # Normalize to 0-1
    sigmoid = 1 / (1 + math.exp(-10 * (x - 0.5)))
    return int(base_xp + (max_xp - base_xp) * sigmoid)


def calculate_xp_for_level_fibonacci(level: int, base_xp: int = 100) -> int:
    """
    Calculate XP using Fibonacci sequence progression.
    
    Creates a natural feeling progression curve.
    
    Args:
        level: Target level
        base_xp: Base XP multiplier
    
    Returns:
        XP required for this level
    
    Examples:
        >>> calculate_xp_for_level_fibonacci(1)
        100
        >>> calculate_xp_for_level_fibonacci(5)
        300
    """
    if level <= 1:
        return base_xp
    if level == 2:
        return base_xp
    
    # Calculate Fibonacci number for level
    fib_prev, fib_curr = 1, 1
    for _ in range(level - 1):
        fib_prev, fib_curr = fib_curr, fib_prev + fib_curr
    
    return base_xp * fib_prev


def calculate_total_xp_for_level(level: int, curve: LevelCurve = LevelCurve.EXPONENTIAL,
                                  base_xp: int = 100, **kwargs) -> int:
    """
    Calculate total XP required to reach a level from level 1.
    
    Args:
        level: Target level
        curve: Level curve algorithm
        base_xp: Base XP for level 1
        **kwargs: Additional curve-specific parameters
    
    Returns:
        Total XP required from level 1
    
    Examples:
        >>> calculate_total_xp_for_level(5, LevelCurve.LINEAR, 100, increment=50)
        1000
    """
    total = 0
    for l in range(1, level + 1):
        if curve == LevelCurve.LINEAR:
            total += calculate_xp_for_level_linear(l, base_xp, kwargs.get('increment', 50))
        elif curve == LevelCurve.EXPONENTIAL:
            total += calculate_xp_for_level_exponential(l, base_xp, kwargs.get('growth_rate', 1.15))
        elif curve == LevelCurve.SIGMOID:
            total += calculate_xp_for_level_sigmoid(l, kwargs.get('max_level', 100), 
                                                    base_xp, kwargs.get('max_xp', 10000))
        elif curve == LevelCurve.FIBONACCI:
            total += calculate_xp_for_level_fibonacci(l, base_xp)
        elif curve == LevelCurve.CUSTOM:
            custom_func = kwargs.get('custom_func')
            if custom_func:
                total += custom_func(l)
            else:
                total += base_xp
    return total


def calculate_level_from_xp(xp: int, curve: LevelCurve = LevelCurve.EXPONENTIAL,
                            base_xp: int = 100, max_level: int = 100, **kwargs) -> Tuple[int, int, int]:
    """
    Calculate current level from total XP.
    
    Args:
        xp: Total XP accumulated
        curve: Level curve algorithm
        base_xp: Base XP for level 1
        max_level: Maximum possible level
        **kwargs: Additional curve-specific parameters
    
    Returns:
        Tuple of (current_level, xp_into_level, xp_needed_for_next)
    
    Examples:
        >>> calculate_level_from_xp(500, LevelCurve.LINEAR, 100, increment=50)
        (4, 50, 250)
    """
    if xp <= 0:
        return (1, 0, calculate_xp_for_level_linear(1, base_xp, kwargs.get('increment', 50)))
    
    level = 1
    total_xp = 0
    
    while level < max_level:
        if curve == LevelCurve.LINEAR:
            level_xp = calculate_xp_for_level_linear(level, base_xp, kwargs.get('increment', 50))
        elif curve == LevelCurve.EXPONENTIAL:
            level_xp = calculate_xp_for_level_exponential(level, base_xp, kwargs.get('growth_rate', 1.15))
        elif curve == LevelCurve.SIGMOID:
            level_xp = calculate_xp_for_level_sigmoid(level, kwargs.get('max_level', 100),
                                                      base_xp, kwargs.get('max_xp', 10000))
        elif curve == LevelCurve.FIBONACCI:
            level_xp = calculate_xp_for_level_fibonacci(level, base_xp)
        elif curve == LevelCurve.CUSTOM:
            custom_func = kwargs.get('custom_func')
            if custom_func:
                level_xp = custom_func(level)
            else:
                level_xp = base_xp
        else:
            level_xp = base_xp
        
        if total_xp + level_xp > xp:
            break
        
        total_xp += level_xp
        level += 1
    
    # Calculate XP into current level and needed for next
    xp_into_level = xp - total_xp
    
    if level >= max_level:
        next_level_xp = level_xp
    else:
        if curve == LevelCurve.LINEAR:
            next_level_xp = calculate_xp_for_level_linear(level + 1, base_xp, kwargs.get('increment', 50))
        elif curve == LevelCurve.EXPONENTIAL:
            next_level_xp = calculate_xp_for_level_exponential(level + 1, base_xp, kwargs.get('growth_rate', 1.15))
        elif curve == LevelCurve.SIGMOID:
            next_level_xp = calculate_xp_for_level_sigmoid(level + 1, kwargs.get('max_level', 100),
                                                           base_xp, kwargs.get('max_xp', 10000))
        elif curve == LevelCurve.FIBONACCI:
            next_level_xp = calculate_xp_for_level_fibonacci(level + 1, base_xp)
        else:
            next_level_xp = level_xp
    
    return (min(level, max_level), xp_into_level, next_level_xp)


def calculate_xp_progress_percentage(xp: int, curve: LevelCurve = LevelCurve.EXPONENTIAL,
                                     base_xp: int = 100, **kwargs) -> float:
    """
    Calculate progress percentage through current level.
    
    Args:
        xp: Total XP accumulated
        curve: Level curve algorithm
        base_xp: Base XP for level 1
        **kwargs: Additional parameters
    
    Returns:
        Progress percentage (0-100)
    
    Examples:
        >>> calculate_xp_progress_percentage(125, LevelCurve.LINEAR, 100, increment=50)
        25.0
    """
    level, xp_into, xp_needed = calculate_level_from_xp(xp, curve, base_xp, **kwargs)
    if xp_needed == 0:
        return 100.0
    return (xp_into / xp_needed) * 100


# ============================================================================
# Level Titles and Tiers
# ============================================================================

# Common RPG-style level titles
DEFAULT_LEVEL_TITLES = {
    (1, 5): 'Novice',
    (6, 10): 'Apprentice',
    (11, 20): 'Journeyman',
    (21, 30): 'Expert',
    (31, 40): 'Master',
    (41, 50): 'Grandmaster',
    (51, 60): 'Legend',
    (61, 70): 'Hero',
    (71, 80): 'Champion',
    (81, 90): 'Immortal',
    (91, 100): 'Godlike',
}

# Tier colors
TIER_COLORS = {
    1: '#CD7F32',  # Bronze
    2: '#C0C0C0',  # Silver
    3: '#FFD700',  # Gold
    4: '#E5E4E2',  # Platinum
    5: '#B9F2FF',  # Diamond
}


def get_level_title(level: int, titles: Dict = None) -> str:
    """
    Get the title for a level.
    
    Args:
        level: Current level
        titles: Custom title mapping (level_range -> title)
    
    Returns:
        Title for the level
    
    Examples:
        >>> get_level_title(15)
        'Journeyman'
        >>> get_level_title(50)
        'Grandmaster'
    """
    titles = titles or DEFAULT_LEVEL_TITLES
    for (min_level, max_level), title in titles.items():
        if min_level <= level <= max_level:
            return title
    return 'Unknown'


def get_tier_emoji(tier: int) -> str:
    """
    Get emoji for achievement tier.
    
    Args:
        tier: Tier level (1=bronze, 2=silver, 3=gold, 4=platinum, 5=diamond)
    
    Returns:
        Tier emoji
    
    Examples:
        >>> get_tier_emoji(1)
        '🥉'
        >>> get_tier_emoji(3)
        '🥇'
    """
    tier_emojis = {
        1: '🥉',  # Bronze
        2: '🥈',  # Silver
        3: '🥇',  # Gold
        4: '💎',  # Platinum
        5: '💠',  # Diamond
    }
    return tier_emojis.get(tier, '🏅')


def get_level_tier(level: int, thresholds: List[int] = None) -> int:
    """
    Get tier for a level.
    
    Args:
        level: Current level
        thresholds: Tier threshold levels [bronze, silver, gold, platinum]
    
    Returns:
        Tier number (1-5)
    
    Examples:
        >>> get_level_tier(25)
        2
    """
    thresholds = thresholds or [10, 25, 50, 75, 100]
    for i, threshold in enumerate(thresholds):
        if level < threshold:
            return i + 1
    return len(thresholds)


# ============================================================================
# Streak Tracking
# ============================================================================

def calculate_streak_multiplier(streak: int, base_multiplier: float = 1.0,
                                bonus_type: StreakBonusType = StreakBonusType.LINEAR,
                                max_multiplier: float = 5.0,
                                bonus_per_day: float = 0.1) -> float:
    """
    Calculate the XP multiplier based on streak.
    
    Args:
        streak: Current streak length
        base_multiplier: Base multiplier (default 1.0 = no bonus)
        bonus_type: How to calculate bonus
        max_multiplier: Maximum possible multiplier
        bonus_per_day: Bonus per day for linear type
    
    Returns:
        XP multiplier
    
    Examples:
        >>> calculate_streak_multiplier(7)
        1.7
        >>> calculate_streak_multiplier(7, bonus_type=StreakBonusType.EXPONENTIAL)
        1.9487171...
    """
    if streak <= 0:
        return base_multiplier
    
    if bonus_type == StreakBonusType.LINEAR:
        multiplier = base_multiplier + (streak * bonus_per_day)
    elif bonus_type == StreakBonusType.EXPONENTIAL:
        # Growth rate decreases to prevent unbounded multiplier
        multiplier = base_multiplier * (1 + bonus_per_day) ** (streak / 7)
    elif bonus_type == StreakBonusType.CAP:
        # Streak bonus caps at certain streak length
        cap_streak = int((max_multiplier - base_multiplier) / bonus_per_day)
        effective_streak = min(streak, cap_streak)
        multiplier = base_multiplier + (effective_streak * bonus_per_day)
    elif bonus_type == StreakBonusType.THRESHOLD:
        # Bonus increases at certain streak milestones
        thresholds = [7, 14, 30, 60, 100, 180, 365]
        multiplier = base_multiplier
        for i, threshold in enumerate(thresholds):
            if streak >= threshold:
                multiplier = base_multiplier + (i + 1) * bonus_per_day * 5
    else:
        multiplier = base_multiplier
    
    return min(multiplier, max_multiplier)


def update_streak(streak: Streak, activity_date: datetime = None,
                  grace_hours: int = 24) -> Streak:
    """
    Update streak based on activity date.
    
    Args:
        streak: Current streak object
        activity_date: Date of activity (default: now)
        grace_hours: Hours of grace period for maintaining streak
    
    Returns:
        Updated streak object
    
    Examples:
        >>> from datetime import datetime, timedelta
        >>> s = Streak(current=5, best=10, last_activity=datetime.now() - timedelta(days=1))
        >>> updated = update_streak(s)
        >>> updated.current
        6
    """
    if activity_date is None:
        activity_date = datetime.now()
    
    if streak.last_activity is None:
        # First activity
        streak.current = 1
        streak.best = max(streak.best, streak.current)
        streak.last_activity = activity_date
        return streak
    
    time_diff = activity_date - streak.last_activity
    hours_diff = time_diff.total_seconds() / 3600
    
    if hours_diff <= grace_hours:
        # Within grace period - no streak change (already counted today)
        pass
    elif hours_diff <= 48:  # Within ~2 days
        # Continue streak
        streak.current += 1
        streak.best = max(streak.best, streak.current)
    else:
        # Streak broken
        streak.current = 1
    
    streak.last_activity = activity_date
    return streak


def calculate_streak_bonus_xp(base_xp: int, streak: int, 
                              bonus_type: StreakBonusType = StreakBonusType.LINEAR,
                              **kwargs) -> int:
    """
    Calculate bonus XP from streak.
    
    Args:
        base_xp: Base XP earned
        streak: Current streak
        bonus_type: Bonus calculation type
        **kwargs: Additional parameters
    
    Returns:
        Total XP (base + bonus)
    
    Examples:
        >>> calculate_streak_bonus_xp(100, 7)
        170
    """
    multiplier = calculate_streak_multiplier(streak, bonus_type=bonus_type, **kwargs)
    return int(base_xp * multiplier)


# ============================================================================
# Leaderboard Utilities
# ============================================================================

def calculate_rank(score: float, scores: List[float], 
                   rank_type: RankType = RankType.NUMERIC) -> int:
    """
    Calculate rank for a score among a list of scores.
    
    Args:
        score: Score to rank
        scores: List of all scores
        rank_type: How to display rank
    
    Returns:
        Rank position (1-indexed)
    
    Examples:
        >>> calculate_rank(85, [100, 95, 85, 80, 75])
        3
    """
    sorted_scores = sorted(scores, reverse=True)
    for i, s in enumerate(sorted_scores):
        if s <= score:
            return i + 1
    return len(sorted_scores) + 1


def calculate_percentile(score: float, scores: List[float]) -> float:
    """
    Calculate percentile for a score.
    
    Args:
        score: Score to calculate percentile for
        scores: List of all scores
    
    Returns:
        Percentile (0-100)
    
    Examples:
        >>> calculate_percentile(85, [70, 75, 80, 85, 90, 95, 100])
        57.14...
    """
    if not scores:
        return 0.0
    
    scores_below = sum(1 for s in scores if s < score)
    return (scores_below / len(scores)) * 100


def get_leaderboard(entries: List[LeaderboardEntry], 
                    sort_by: str = 'score',
                    limit: int = None) -> List[LeaderboardEntry]:
    """
    Sort and rank leaderboard entries.
    
    Args:
        entries: List of leaderboard entries
        sort_by: Field to sort by
        limit: Maximum entries to return
    
    Returns:
        Sorted and ranked entries
    
    Examples:
        >>> entries = [
        ...     LeaderboardEntry('u1', 'Alice', 100, 1),
        ...     LeaderboardEntry('u2', 'Bob', 150, 1),
        ...     LeaderboardEntry('u3', 'Charlie', 120, 1),
        ... ]
        >>> board = get_leaderboard(entries)
        >>> board[0].username
        'Bob'
    """
    # Sort by specified field (descending for score/xp/streak)
    reverse = sort_by in ['score', 'level', 'streak', 'achievements_count']
    sorted_entries = sorted(entries, key=lambda e: getattr(e, sort_by, 0), reverse=reverse)
    
    # Assign ranks
    for i, entry in enumerate(sorted_entries):
        entry.rank = i + 1
    
    if limit:
        sorted_entries = sorted_entries[:limit]
    
    return sorted_entries


def calculate_leaderboard_position(user_id: str, 
                                    entries: List[LeaderboardEntry]) -> Optional[int]:
    """
    Find a user's position on the leaderboard.
    
    Args:
        user_id: User to find
        entries: Sorted leaderboard entries
    
    Returns:
        Position (1-indexed) or None if not found
    """
    for entry in entries:
        if entry.user_id == user_id:
            return entry.rank
    return None


# ============================================================================
# Achievement System
# ============================================================================

def check_achievement_criteria(current_value: Union[int, float],
                               criteria: Dict) -> bool:
    """
    Check if achievement criteria are met.
    
    Args:
        current_value: Current progress value
        criteria: Achievement criteria dict
    
    Returns:
        True if achievement should be unlocked
    
    Examples:
        >>> check_achievement_criteria(10, {'type': 'threshold', 'value': 10})
        True
    """
    criteria_type = criteria.get('type', 'threshold')
    
    if criteria_type == 'threshold':
        # Simple threshold check
        threshold = criteria.get('value', 0)
        return current_value >= threshold
    
    elif criteria_type == 'range':
        # Range check
        min_val = criteria.get('min', float('-inf'))
        max_val = criteria.get('max', float('inf'))
        return min_val <= current_value <= max_val
    
    elif criteria_type == 'exact':
        # Exact value match
        target = criteria.get('value', None)
        return current_value == target
    
    elif criteria_type == 'percentage':
        # Percentage threshold
        percentage = criteria.get('value', 100)
        base = criteria.get('base', 100)
        return (current_value / base * 100) >= percentage
    
    elif criteria_type == 'streak':
        # Streak check
        required_streak = criteria.get('value', 0)
        return current_value >= required_streak
    
    elif criteria_type == 'count':
        # Count check (e.g., achievements unlocked, items collected)
        required_count = criteria.get('value', 0)
        return current_value >= required_count
    
    return False


def calculate_achievement_progress(current_value: Union[int, float],
                                   criteria: Dict) -> float:
    """
    Calculate progress towards achievement (0-100).
    
    Args:
        current_value: Current progress value
        criteria: Achievement criteria dict
    
    Returns:
        Progress percentage
    
    Examples:
        >>> calculate_achievement_progress(50, {'type': 'threshold', 'value': 100})
        50.0
    """
    criteria_type = criteria.get('type', 'threshold')
    
    if criteria_type == 'threshold':
        threshold = criteria.get('value', 1)
        if threshold == 0:
            return 100.0
        return min(100.0, (current_value / threshold) * 100)
    
    elif criteria_type == 'range':
        min_val = criteria.get('min', 0)
        max_val = criteria.get('max', 1)
        if max_val == min_val:
            return 100.0
        progress = (current_value - min_val) / (max_val - min_val) * 100
        return max(0, min(100, progress))
    
    elif criteria_type == 'exact':
        target = criteria.get('value', 0)
        return 100.0 if current_value == target else 0.0
    
    elif criteria_type == 'percentage':
        percentage = criteria.get('value', 100)
        base = criteria.get('base', 100)
        current_percentage = (current_value / base * 100) if base > 0 else 0
        return min(100.0, (current_percentage / percentage) * 100)
    
    elif criteria_type == 'streak' or criteria_type == 'count':
        required = criteria.get('value', 1)
        if required == 0:
            return 100.0
        return min(100.0, (current_value / required) * 100)
    
    return 0.0


def get_achievements_by_tier(achievements: List[Achievement], 
                            unlocked_only: bool = False) -> Dict[int, List[Achievement]]:
    """
    Group achievements by tier.
    
    Args:
        achievements: List of achievements
        unlocked_only: Only include unlocked achievements
    
    Returns:
        Dict mapping tier to list of achievements
    """
    result = {1: [], 2: [], 3: [], 4: [], 5: []}
    
    for achievement in achievements:
        if unlocked_only and not achievement.unlocked_at:
            continue
        result[achievement.tier].append(achievement)
    
    return result


def calculate_achievement_completion(achievements: List[Achievement]) -> Dict[str, float]:
    """
    Calculate achievement completion statistics.
    
    Args:
        achievements: List of achievements
    
    Returns:
        Dict with completion stats
    
    Examples:
        >>> a1 = Achievement('a1', 'Test', 'Desc', tier=1, unlocked_at=datetime.now())
        >>> a2 = Achievement('a2', 'Test2', 'Desc', tier=1)
        >>> calculate_achievement_completion([a1, a2])
        {'total': 2, 'unlocked': 1, 'completion': 50.0, ...}
    """
    total = len(achievements)
    unlocked = sum(1 for a in achievements if a.unlocked_at)
    
    total_xp = sum(a.xp_reward for a in achievements if a.unlocked_at)
    total_currency = sum(a.currency_reward for a in achievements if a.unlocked_at)
    
    by_tier = get_achievements_by_tier(achievements)
    by_tier_unlocked = get_achievements_by_tier(achievements, unlocked_only=True)
    
    return {
        'total': total,
        'unlocked': unlocked,
        'completion': (unlocked / total * 100) if total > 0 else 0,
        'total_xp_earned': total_xp,
        'total_currency_earned': total_currency,
        'by_tier': {
            tier: {
                'total': len(by_tier[tier]),
                'unlocked': len(by_tier_unlocked[tier]),
                'completion': (len(by_tier_unlocked[tier]) / len(by_tier[tier]) * 100) 
                              if by_tier[tier] else 0
            }
            for tier in range(1, 6)
        }
    }


# ============================================================================
# Daily Rewards
# ============================================================================

def calculate_daily_reward(day: int, base_reward: int = 10,
                          streak_bonus: float = 0.1,
                          max_day: int = 7,
                          special_days: Dict[int, int] = None) -> int:
    """
    Calculate daily login reward.
    
    Args:
        day: Current consecutive login day
        base_reward: Base reward amount
        streak_bonus: Bonus multiplier per day
        max_day: Day at which sequence resets
        special_days: Dict mapping day numbers to bonus amounts
    
    Returns:
        Reward amount for the day
    
    Examples:
        >>> calculate_daily_reward(1, 10)
        10
        >>> calculate_daily_reward(7, 10)
        20
    """
    special_days = special_days or {7: 100}  # Day 7 gives bonus
    
    effective_day = ((day - 1) % max_day) + 1
    
    # Calculate base with streak bonus
    reward = int(base_reward * (1 + streak_bonus * (effective_day - 1)))
    
    # Add special day bonus
    if effective_day in special_days:
        reward += special_days[effective_day]
    
    return reward


def get_daily_reward_sequence(days: int = 7, base_reward: int = 10,
                              streak_bonus: float = 0.1,
                              special_days: Dict[int, int] = None) -> List[Dict]:
    """
    Get full daily reward sequence.
    
    Args:
        days: Number of days in sequence
        base_reward: Base reward amount
        streak_bonus: Bonus per day
        special_days: Special day bonuses
    
    Returns:
        List of daily reward info
    
    Examples:
        >>> seq = get_daily_reward_sequence(7, 10)
        >>> len(seq)
        7
    """
    special_days = special_days or {7: 100}
    sequence = []
    
    for day in range(1, days + 1):
        reward = calculate_daily_reward(day, base_reward, streak_bonus, days, special_days)
        is_special = day in special_days
        sequence.append({
            'day': day,
            'reward': reward,
            'is_special': is_special,
            'bonus': special_days.get(day, 0) if is_special else 0,
        })
    
    return sequence


# ============================================================================
# Challenges and Quests
# ============================================================================

def calculate_challenge_progress(challenge: Challenge) -> float:
    """
    Calculate progress percentage for a challenge.
    
    Args:
        challenge: Challenge object
    
    Returns:
        Progress percentage (0-100)
    """
    if challenge.target == 0:
        return 100.0
    return min(100.0, (challenge.current / challenge.target) * 100)


def update_challenge_progress(challenge: Challenge, progress: int) -> Challenge:
    """
    Update challenge progress.
    
    Args:
        challenge: Challenge object
        progress: Progress amount to add
    
    Returns:
        Updated challenge
    """
    challenge.current += progress
    
    if challenge.current >= challenge.target and not challenge.is_completed:
        challenge.is_completed = True
    
    return challenge


def is_challenge_expired(challenge: Challenge, current_time: datetime = None) -> bool:
    """
    Check if challenge has expired.
    
    Args:
        challenge: Challenge object
        current_time: Current time (default: now)
    
    Returns:
        True if expired
    """
    if challenge.expires_at is None:
        return False
    
    if current_time is None:
        current_time = datetime.now()
    
    return current_time > challenge.expires_at


def generate_daily_challenges(count: int = 3, base_xp: int = 50,
                              base_target: int = 10,
                              expires_hours: int = 24) -> List[Challenge]:
    """
    Generate daily challenges.
    
    Args:
        count: Number of challenges to generate
        base_xp: Base XP reward
        base_target: Base target value
        expires_hours: Hours until expiration
    
    Returns:
        List of Challenge objects
    """
    challenge_templates = [
        {'id': 'login', 'name': 'Daily Login', 'description': 'Log in today', 'target': 1, 'xp': 25},
        {'id': 'xp_earn', 'name': 'XP Hunter', 'description': 'Earn XP', 'target': 100, 'xp': 50},
        {'id': 'streak', 'name': 'Keep it Going', 'description': 'Maintain your streak', 'target': 1, 'xp': 30},
        {'id': 'achievement', 'name': 'Achievement Seeker', 'description': 'Unlock an achievement', 'target': 1, 'xp': 100},
        {'id': 'challenge', 'name': 'Challenge Accepted', 'description': 'Complete challenges', 'target': 2, 'xp': 75},
    ]
    
    challenges = []
    expires_at = datetime.now() + timedelta(hours=expires_hours)
    
    for i in range(min(count, len(challenge_templates))):
        template = challenge_templates[i]
        challenge = Challenge(
            id=f"daily_{template['id']}_{datetime.now().strftime('%Y%m%d')}",
            name=template['name'],
            description=template['description'],
            target=template['target'],
            xp_reward=template['xp'],
            expires_at=expires_at,
            is_daily=True,
        )
        challenges.append(challenge)
    
    return challenges


# ============================================================================
# Points and Currency
# ============================================================================

def calculate_points_with_level_bonus(base_points: int, level: int,
                                      bonus_per_level: float = 0.01,
                                      max_bonus: float = 0.5) -> int:
    """
    Calculate points with level bonus multiplier.
    
    Args:
        base_points: Base points earned
        level: Current level
        bonus_per_level: Bonus percentage per level (0.01 = 1%)
        max_bonus: Maximum bonus percentage
    
    Returns:
        Points with level bonus applied
    
    Examples:
        >>> calculate_points_with_level_bonus(100, 10, 0.01)
        110
    """
    level_bonus = min(level * bonus_per_level, max_bonus)
    return int(base_points * (1 + level_bonus))


def distribute_rewards(total_reward: int, recipients: List[str],
                       weights: List[float] = None) -> Dict[str, int]:
    """
    Distribute rewards among recipients.
    
    Args:
        total_reward: Total reward to distribute
        recipients: List of recipient IDs
        weights: Distribution weights (must sum to 1.0)
    
    Returns:
        Dict mapping recipient to reward amount
    
    Examples:
        >>> distribute_rewards(100, ['a', 'b', 'c'], [0.5, 0.3, 0.2])
        {'a': 50, 'b': 30, 'c': 20}
    """
    if not recipients:
        return {}
    
    if weights is None:
        # Equal distribution
        weight = 1.0 / len(recipients)
        weights = [weight] * len(recipients)
    
    distributed = {}
    remaining = total_reward
    
    for i, recipient in enumerate(recipients[:-1]):
        amount = int(total_reward * weights[i])
        distributed[recipient] = amount
        remaining -= amount
    
    # Give remainder to last recipient
    distributed[recipients[-1]] = remaining
    
    return distributed


def calculate_prestige_rewards(level: int, xp_earned: int,
                              prestige_multiplier: float = 0.1) -> Dict[str, int]:
    """
    Calculate rewards when prestiging (resetting level for bonuses).
    
    Args:
        level: Level being prestiged
        xp_earned: Total XP earned
        prestige_multiplier: Reward multiplier per level
    
    Returns:
        Dict with prestige rewards
    
    Examples:
        >>> calculate_prestige_rewards(50, 50000)
        {'prestige_points': 5, 'prestige_currency': 250}
    """
    prestige_points = max(1, level // 10)
    prestige_currency = int(xp_earned * prestige_multiplier / 100)
    
    return {
        'prestige_points': prestige_points,
        'prestige_currency': prestige_currency,
        'prestige_level': level,
        'total_xp_earned': xp_earned,
    }


# ============================================================================
# Progress Visualization
# ============================================================================

def create_progress_bar(current: int, maximum: int, 
                        width: int = 20,
                        filled: str = '█',
                        empty: str = '░',
                        show_percent: bool = True) -> str:
    """
    Create a text progress bar.
    
    Args:
        current: Current progress value
        maximum: Maximum progress value
        width: Width of bar in characters
        filled: Character for filled portion
        empty: Character for empty portion
        show_percent: Show percentage after bar
    
    Returns:
        Progress bar string
    
    Examples:
        >>> create_progress_bar(50, 100, 10)
        '█████░░░░░ 50%'
    """
    if maximum == 0:
        percent = 100
        filled_count = width
    else:
        percent = min(100, (current / maximum) * 100)
        filled_count = int(width * percent / 100)
    
    bar = filled * filled_count + empty * (width - filled_count)
    
    if show_percent:
        return f"{bar} {percent:.0f}%"
    return bar


def create_xp_bar(xp: int, curve: LevelCurve = LevelCurve.EXPONENTIAL,
                  base_xp: int = 100, width: int = 20, **kwargs) -> str:
    """
    Create an XP progress bar with level info.
    
    Args:
        xp: Total XP
        curve: Level curve algorithm
        base_xp: Base XP for level 1
        width: Width of progress bar
        **kwargs: Additional parameters
    
    Returns:
        XP bar string with level
    
    Examples:
        >>> create_xp_bar(150, LevelCurve.LINEAR, 100, 10, increment=50)
        'Lv 2 ████░░░░░░ 50%'
    """
    level, xp_into, xp_needed = calculate_level_from_xp(xp, curve, base_xp, **kwargs)
    
    if xp_needed == 0:
        bar = create_progress_bar(1, 1, width, show_percent=False)
    else:
        bar = create_progress_bar(xp_into, xp_needed, width, show_percent=False)
    
    percent = (xp_into / xp_needed * 100) if xp_needed > 0 else 100
    
    return f"Lv {level} {bar} {percent:.0f}%"


# ============================================================================
# Main Demo
# ============================================================================

if __name__ == '__main__':
    print("=== Gamification Utilities Demo ===\n")
    
    # Leveling
    print("Leveling System:")
    print(f"  Linear L5: {calculate_xp_for_level_linear(5)} XP")
    print(f"  Exponential L5: {calculate_xp_for_level_exponential(5)} XP")
    print(f"  Fibonacci L5: {calculate_xp_for_level_fibonacci(5)} XP")
    print(f"  Total XP for L10 (linear): {calculate_total_xp_for_level(10, LevelCurve.LINEAR)}")
    
    # Level from XP
    level, xp_in, xp_need = calculate_level_from_xp(500, LevelCurve.LINEAR, increment=50)
    print(f"  Level from 500 XP: {level} ({xp_in}/{xp_need} XP)")
    
    # Level title
    print(f"  Level 25 title: {get_level_title(25)}")
    print(f"  Level 25 tier: {get_tier_emoji(get_level_tier(25))}")
    
    # Streak
    print("\nStreak System:")
    for days in [1, 7, 14, 30, 100]:
        mult = calculate_streak_multiplier(days)
        print(f"  {days}-day streak: {mult:.2f}x multiplier")
    
    # Achievements
    print("\nAchievement System:")
    a1 = Achievement('first_login', 'First Steps', 'Log in for the first time', 
                     xp_reward=50, tier=1, criteria={'type': 'threshold', 'value': 1})
    a2 = Achievement('streak_7', 'Week Warrior', 'Maintain a 7-day streak',
                     xp_reward=100, tier=2, criteria={'type': 'streak', 'value': 7})
    
    progress = calculate_achievement_progress(3, {'type': 'streak', 'value': 7})
    print(f"  3-day streak progress to 7: {progress:.1f}%")
    
    # Daily rewards
    print("\nDaily Rewards:")
    sequence = get_daily_reward_sequence(7, 10, 0.1, {7: 100})
    for day in sequence:
        special = " (SPECIAL!)" if day['is_special'] else ""
        print(f"  Day {day['day']}: {day['reward']} coins{special}")
    
    # Progress bar
    print("\nProgress Visualization:")
    print(f"  {create_progress_bar(75, 100, 20)}")
    print(f"  {create_xp_bar(500, LevelCurve.LINEAR, 100, 20, increment=50)}")
    
    # Leaderboard
    print("\nLeaderboard:")
    entries = [
        LeaderboardEntry('u1', 'Alice', 1500, 1, level=25, streak=14),
        LeaderboardEntry('u2', 'Bob', 2300, 1, level=30, streak=7),
        LeaderboardEntry('u3', 'Charlie', 1800, 1, level=28, streak=21),
    ]
    board = get_leaderboard(entries, sort_by='score', limit=3)
    for entry in board:
        print(f"  #{entry.rank} {entry.username}: {entry.score} XP (Lv {entry.level})")
    
    # Challenges
    print("\nChallenges:")
    challenges = generate_daily_challenges(3)
    for c in challenges:
        progress = calculate_challenge_progress(c)
        print(f"  {c.name}: {progress:.0f}% ({c.current}/{c.target})")
    
    # Prestige
    print("\nPrestige:")
    prestige = calculate_prestige_rewards(50, 50000)
    print(f"  Prestige from Lv 50: {prestige['prestige_points']} points, {prestige['prestige_currency']} currency")