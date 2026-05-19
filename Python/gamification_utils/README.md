# Gamification Utilities

A comprehensive gamification utility module for Python with zero external dependencies.

## Features

- **XP & Leveling Systems** - Multiple progression curves (linear, exponential, sigmoid, Fibonacci)
- **Achievement System** - Badge management with tiers and progress tracking
- **Streak Tracking** - Multiplier and bonus calculations for consecutive activities
- **Leaderboard Utilities** - Ranking systems with percentile calculations
- **Daily Rewards** - Login reward sequences with special bonuses
- **Challenge Management** - Quest tracking with expiration handling
- **Progress Visualization** - Text progress bars and XP displays

## Quick Start

```python
from gamification_utils.mod import (
    calculate_level_from_xp,
    get_level_title,
    calculate_streak_multiplier,
    Achievement,
    LeaderboardEntry,
    get_leaderboard,
)

# Calculate level from XP
level, xp_in, xp_need = calculate_level_from_xp(500)
print(f"Level {level}: {xp_in}/{xp_need} XP")

# Get level title
title = get_level_title(25)  # "Expert"

# Streak multiplier
mult = calculate_streak_multiplier(7)  # ~1.7x for 7-day streak

# Leaderboard
entries = [
    LeaderboardEntry('u1', 'Alice', 1500, 1, level=25, streak=14),
    LeaderboardEntry('u2', 'Bob', 2300, 1, level=30, streak=7),
]
board = get_leaderboard(entries)
```

## Level Curves

### Linear
`base_xp + (level - 1) * increment`

- Predictable progression
- Same increase per level

### Exponential  
`base_xp * (growth_rate ^ (level - 1))`

- Common in RPG games
- Increasing difficulty

### Fibonacci
`base_xp * fib(level - 1)`

- Natural feeling progression
- Moderate late-game scaling

### Sigmoid
Slow start → Fast middle → Slow end

- Balanced progression
- Good for capped systems

## Streak Bonuses

- **Linear**: +10% per day (default)
- **Exponential**: Compounding growth
- **Cap**: Maximum multiplier limit
- **Threshold**: Milestone bonuses

## Achievement Tiers

| Tier | Emoji | Name |
|------|-------|------|
| 1 | 🥉 | Bronze |
| 2 | 🥈 | Silver |
| 3 | 🥇 | Gold |
| 4 | 💎 | Platinum |
| 5 | 💠 | Diamond |

## Level Titles

| Levels | Title |
|--------|-------|
| 1-5 | Novice |
| 6-10 | Apprentice |
| 11-20 | Journeyman |
| 21-30 | Expert |
| 31-40 | Master |
| 41-50 | Grandmaster |
| 51-60 | Legend |
| 61-70 | Hero |
| 71-80 | Champion |
| 81-90 | Immortal |
| 91-100 | Godlike |

## API Reference

### XP Functions

- `calculate_xp_for_level_linear(level, base_xp, increment)`
- `calculate_xp_for_level_exponential(level, base_xp, growth_rate)`
- `calculate_xp_for_level_fibonacci(level, base_xp)`
- `calculate_total_xp_for_level(level, curve, base_xp, **kwargs)`
- `calculate_level_from_xp(xp, curve, base_xp, max_level, **kwargs)`
- `calculate_xp_progress_percentage(xp, curve, base_xp, **kwargs)`

### Streak Functions

- `calculate_streak_multiplier(streak, base_multiplier, bonus_type, ...)`
- `update_streak(streak, activity_date, grace_hours)`
- `calculate_streak_bonus_xp(base_xp, streak, bonus_type, ...)`

### Achievement Functions

- `check_achievement_criteria(current_value, criteria)`
- `calculate_achievement_progress(current_value, criteria)`
- `get_achievements_by_tier(achievements, unlocked_only)`
- `calculate_achievement_completion(achievements)`

### Leaderboard Functions

- `calculate_rank(score, scores, rank_type)`
- `calculate_percentile(score, scores)`
- `get_leaderboard(entries, sort_by, limit)`
- `calculate_leaderboard_position(user_id, entries)`

### Daily Rewards

- `calculate_daily_reward(day, base_reward, streak_bonus, ...)`
- `get_daily_reward_sequence(days, base_reward, ...)`

### Challenges

- `calculate_challenge_progress(challenge)`
- `update_challenge_progress(challenge, progress)`
- `is_challenge_expired(challenge, current_time)`
- `generate_daily_challenges(count, base_xp, ...)`

### Visualization

- `create_progress_bar(current, maximum, width, ...)`
- `create_xp_bar(xp, curve, base_xp, width, ...)`

## Testing

```bash
python gamification_utils_test.py
```

## License

MIT License - Part of AllToolkit