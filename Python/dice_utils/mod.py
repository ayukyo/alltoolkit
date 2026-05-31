#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AllToolkit - Dice Utilities Module
===================================
Comprehensive dice rolling and probability utilities with zero external dependencies.

Features:
    - Roll standard dice (d4, d6, d8, d10, d12, d20, d100)
    - Roll arbitrary dice notation (2d6+3, 4d20kh3, 8d6kl2)
    - Advantage/disadvantage rolls (roll twice, take higher/lower)
    - Reroll mechanics (xdy r1-2 means reroll 1s and 2s once)
    - Exploding dice (reroll and add when max is rolled)
    - Target number success counting (count successes above threshold)
    - Drop/keep highest/lowest (kh, kl, dh, dl)
    - Batch rolling and statistics
    - Probability distribution calculations
    - Weighted dice support

Dice Notation:
    XdY      - Roll X dice with Y sides
    +N/-N    - Add/subtract fixed modifier
    khN      - Keep highest N rolls
    klN      - Keep lowest N rolls
    dhN      - Drop highest N rolls
    dlN      - Drop lowest N rolls
    rN       - Reroll dice that show N or lower (once)
    !        - Exploding dice (reroll and add on max)
    >N       - Target number (count successes)
    >=N      - Target number inclusive

Examples:
    dice_roll("2d6")           -> [3, 5] (sum=8 by default)
    dice_parse("4d20kh3")       -> Roll 4d20, keep highest 3
    dice_parse("8d6dl2")       -> Roll 8d6, drop lowest 2
    dice_parse("3d10+2")       -> Roll 3d10 and add 2
    dice_parse("2d20!")        -> Exploding dice
    dice_parse("5d6r1")        -> Reroll 1s once
    dice_parse("6d6>=4")       -> Count successes (4+)

Author: AllToolkit
License: MIT
"""


import random
import re
from typing import Optional, List, Tuple, Dict, Union, Callable
from dataclasses import dataclass, field
from enum import Enum
from collections import Counter


# ============================================================================
# Types & Constants
# ============================================================================

RollResult = Union[int, List[int]]
DiceNotation = str
Modifier = int


# Standard dice types
class DiceType(Enum):
    D2 = 2
    D3 = 3
    D4 = 4
    D6 = 6
    D8 = 8
    D10 = 10
    D12 = 12
    D20 = 20
    D30 = 30
    D100 = 100


# ============================================================================
# Data Classes
# ============================================================================

@dataclass
class RollOutcome:
    """Represents a single roll outcome."""
    notation: str
    rolls: List[int]
    kept: List[int]
    dropped: List[int]
    modifier: int
    success_count: int = 0
    failure_count: int = 0
    
    @property
    def total(self) -> int:
        """Sum of kept rolls plus modifier."""
        return sum(self.kept) + self.modifier
    
    @property
    def raw_sum(self) -> int:
        """Sum of all rolls before modifiers."""
        return sum(self.rolls)
    
    @property
    def success_rate(self) -> float:
        """Success rate as a percentage."""
        total = self.success_count + self.failure_count
        if total == 0:
            return 0.0
        return (self.success_count / total) * 100
    
    def __repr__(self) -> str:
        return (
            f"RollOutcome(total={self.total}, rolls={self.rolls}, "
            f"kept={self.kept}, dropped={self.dropped}, "
            f"modifier={self.modifier})"
        )


@dataclass
class RollStats:
    """Statistical summary of multiple rolls."""
    notation: str
    count: int
    totals: List[int]
    min_total: int
    max_total: int
    mean: float
    median: float
    std_dev: float
    
    @property
    def average(self) -> float:
        """Alias for mean."""
        return self.mean
    
    def percentile(self, p: float) -> float:
        """Calculate percentile (0-100)."""
        if p < 0 or p > 100:
            raise ValueError("Percentile must be between 0 and 100")
        if not self.totals:
            return 0.0
        sorted_totals = sorted(self.totals)
        idx = (p / 100) * (len(sorted_totals) - 1)
        lower = int(idx)
        upper = min(lower + 1, len(sorted_totals) - 1)
        frac = idx - lower
        return sorted_totals[lower] * (1 - frac) + sorted_totals[upper] * frac


# ============================================================================
# Core Rolling Functions
# ============================================================================

def roll(dice: int, sides: int) -> List[int]:
    """
    Roll dice.
    
    Args:
        dice: Number of dice to roll
        sides: Number of sides per die
        
    Returns:
        List of individual roll results
        
    Examples:
        >>> roll(2, 6)
        [3, 5]
        >>> roll(1, 20)
        [14]
    """
    if dice < 1:
        return []
    if sides < 1:
        raise ValueError("Sides must be at least 1")
    if dice > 1000:
        raise ValueError("Cannot roll more than 1000 dice at once")
    return [random.randint(1, sides) for _ in range(dice)]


def roll_with_reroll(dice: int, sides: int, reroll_threshold: int, max_rerolls: int = 1) -> List[int]:
    """
    Roll dice with reroll mechanics.
    
    Args:
        dice: Number of dice to roll
        sides: Number of sides per die
        reroll_threshold: Dice at or below this value are rerolled
        max_rerolls: Maximum number of reroll passes (default 1)
        
    Returns:
        List of final roll results
        
    Examples:
        >>> roll_with_reroll(5, 6, 2)  # Reroll 1s and 2s once
        [6, 4, 3, 5, 6]
    """
    if dice < 1 or sides < 1 or reroll_threshold > sides:
        raise ValueError("Invalid parameters")
    
    results = [random.randint(1, sides) for _ in range(dice)]
    
    for _ in range(max_rerolls):
        new_results = []
        for r in results:
            if r <= reroll_threshold:
                new_results.append(random.randint(1, sides))
            else:
                new_results.append(r)
        results = new_results
    
    return results


def roll_exploding(dice: int, sides: int, max_explosions: int = 100) -> List[int]:
    """
    Roll exploding dice (reroll and add on max value).
    
    Args:
        dice: Number of dice to roll
        sides: Number of sides per die
        max_explosions: Maximum total explosions allowed (prevents infinite loops)
        
    Returns:
        List of all rolls including explosions
        
    Examples:
        >>> results = roll_exploding(3, 6)  # May include extra rolls
        [6, 6, 3, 6, 4]  # Two 6s exploded, giving two more rolls
    """
    if dice < 1 or sides < 1:
        raise ValueError("Invalid parameters")
    
    results = []
    explosion_count = 0
    
    for _ in range(dice):
        while True:
            r = random.randint(1, sides)
            results.append(r)
            if r == sides and explosion_count < max_explosions:
                explosion_count += 1
            else:
                break
    
    return results


def advantage(dice: int = 1, sides: int = 20) -> Tuple[int, int, int]:
    """
    Roll with advantage (take higher).
    
    Args:
        dice: Number of dice to roll (default 1)
        sides: Number of sides (default 20 for d20)
        
    Returns:
        Tuple of (roll1, roll2, result) where result is the higher
        
    Examples:
        >>> r1, r2, result = advantage()
        (14, 19, 19)
    """
    if dice != 1:
        raise ValueError("Advantage only supports single die rolls")
    roll1 = random.randint(1, sides)
    roll2 = random.randint(1, sides)
    return roll1, roll2, max(roll1, roll2)


def disadvantage(dice: int = 1, sides: int = 20) -> Tuple[int, int, int]:
    """
    Roll with disadvantage (take lower).
    
    Args:
        dice: Number of dice to roll (default 1)
        sides: Number of sides (default 20 for d20)
        
    Returns:
        Tuple of (roll1, roll2, result) where result is the lower
    """
    if dice != 1:
        raise ValueError("Disadvantage only supports single die rolls")
    roll1 = random.randint(1, sides)
    roll2 = random.randint(1, sides)
    return roll1, roll2, min(roll1, roll2)


# ============================================================================
# Dice Notation Parser
# ============================================================================

# Regex patterns for dice notation
DICE_PATTERN = re.compile(
    r'^(?P<count>\d*)d(?P<sides>\d+)'
    r'(?P<keep_high>kh\d+)?'
    r'(?P<keep_low>kl\d+)?'
    r'(?P<drop_high>dh\d+)?'
    r'(?P<drop_low>dl\d+)?'
    r'(?P<explode>!)?'
    r'(?P<reroll>r\d+)?'
    r'(?P<target>>=?\d+)?'
    r'(?P<modifier>[+-]\d+)?$'
)


def dice_parse(notation: str) -> RollOutcome:
    """
    Parse dice notation and roll.
    
    Args:
        notation: Dice notation string
        
    Returns:
        RollOutcome with all roll details
        
    Supported notation:
        XdY         - Roll X dice with Y sides
        +N / -N     - Add/subtract modifier
        khN         - Keep highest N
        klN         - Keep lowest N
        dhN         - Drop highest N
        dlN         - Drop lowest N
        !           - Exploding dice
        rN          - Reroll values of N or less (once)
        >=N / >N    - Target number for success counting
        
    Examples:
        >>> outcome = dice_parse("2d6")
        >>> outcome.total
        9
        >>> outcome = dice_parse("4d20kh3")  # Roll 4d20, keep highest 3
        >>> len(outcome.kept)
        3
        >>> outcome = dice_parse("3d10+5")
        >>> outcome.modifier
        5
    """
    notation = notation.lower().strip().replace(" ", "")
    
    match = DICE_PATTERN.match(notation)
    if not match:
        raise ValueError(f"Invalid dice notation: {notation}")
    
    groups = match.groupdict()
    
    dice_count = int(groups['count']) if groups['count'] else 1
    dice_sides = int(groups['sides'])
    modifier = int(groups['modifier']) if groups['modifier'] else 0
    target = groups['target']
    reroll = groups['reroll']
    exploding = groups['explode'] == '!'
    
    # Parse keep/drop values
    keep_high = int(groups['keep_high'][2:]) if groups['keep_high'] else None
    keep_low = int(groups['keep_low'][2:]) if groups['keep_low'] else None
    drop_high = int(groups['drop_high'][2:]) if groups['drop_high'] else None
    drop_low = int(groups['drop_low'][2:]) if groups['drop_low'] else None
    
    # Parse reroll threshold
    reroll_threshold = int(reroll[1:]) if reroll else None
    
    # Parse target number
    target_num = None
    target_inclusive = True
    if target:
        if target.startswith('>='):
            target_num = int(target[2:])
            target_inclusive = True
        else:
            target_num = int(target[1:])
            target_inclusive = False
    
    # Perform rolls
    if reroll_threshold:
        rolls = roll_with_reroll(dice_count, dice_sides, reroll_threshold)
    elif exploding:
        rolls = roll_exploding(dice_count, dice_sides)
    else:
        rolls = roll(dice_count, dice_sides)
    
    # Apply keep/drop
    kept = list(rolls)
    dropped = []
    
    # Keep highest
    if keep_high is not None:
        kept.sort(reverse=True)
        kept, drop_temp = kept[:keep_high], kept[keep_high:]
        dropped.extend(drop_temp)
    
    # Keep lowest
    if keep_low is not None:
        kept.sort()
        kept, drop_temp = kept[:keep_low], kept[keep_low:]
        dropped.extend(drop_temp)
    
    # Drop highest
    if drop_high is not None:
        rolls.sort(reverse=True)
        dropped.extend(rolls[:drop_high])
        kept = rolls[drop_high:]
    
    # Drop lowest
    if drop_low is not None:
        rolls.sort()
        dropped.extend(rolls[:drop_low])
        kept = rolls[drop_low:]
    
    # Handle case where nothing is kept (e.g., dh all dice)
    if not kept:
        kept = [0]
        rolls = rolls if rolls else [0]
    
    # Count successes
    success_count = 0
    failure_count = 0
    
    if target_num is not None:
        check_rolls = rolls if not (kept or dropped) else (kept if len(kept) > 0 else rolls)
        
        for r in check_rolls:
            if target_inclusive:
                if r >= target_num:
                    success_count += 1
                else:
                    failure_count += 1
            else:
                if r > target_num:
                    success_count += 1
                else:
                    failure_count += 1
    
    return RollOutcome(
        notation=notation,
        rolls=list(rolls),
        kept=list(kept),
        dropped=list(dropped),
        modifier=modifier,
        success_count=success_count,
        failure_count=failure_count
    )


def dice_roll(notation: str) -> int:
    """
    Roll dice notation and return total.
    
    Args:
        notation: Dice notation string
        
    Returns:
        Total sum of rolls (with modifiers)
        
    Examples:
        >>> dice_roll("2d6")
        8
        >>> dice_roll("d20+5")
        17
        >>> dice_roll("4d6kh3")  # Roll 4d6, keep highest 3, sum them
        12
    """
    outcome = dice_parse(notation)
    return outcome.total


# ============================================================================
# Fudge Dice (Special Dice System)
# ============================================================================

def roll_fudge(dice: int = 4) -> List[int]:
    """
    Roll Fudge/FATE dice (-1, 0, +1).
    
    Args:
        dice: Number of Fudge dice to roll (default 4)
        
    Returns:
        List of Fudge roll results (-1, 0, or 1)
        
    Examples:
        >>> roll_fudge(4)
        [-1, 0, 1, 0]
        >>> sum(roll_fudge(4))
        0
    """
    fudge_values = [-1, 0, 1]
    return [random.choice(fudge_values) for _ in range(dice)]


def fudge_total(dice: int = 4) -> int:
    """
    Roll Fudge dice and return total.
    
    Args:
        dice: Number of Fudge dice to roll
        
    Returns:
        Sum of Fudge rolls (-dice to +dice)
    """
    return sum(roll_fudge(dice))


# ============================================================================
# Statistics & Probability
# ============================================================================

def roll_distribution(dice: int, sides: int, trials: int = 10000) -> Dict[int, float]:
    """
    Calculate probability distribution by simulation.
    
    Args:
        dice: Number of dice
        sides: Number of sides per die
        trials: Number of simulation trials
        
    Returns:
        Dictionary mapping sum to probability
        
    Examples:
        >>> dist = roll_distribution(2, 6, trials=10000)
        >>> dist[7]  # Probability of rolling 7 with 2d6
        0.166
    """
    if trials < 1:
        raise ValueError("Trials must be at least 1")
    
    totals = Counter()
    total_trials = 0
    
    for _ in range(trials):
        r = sum(roll(dice, sides))
        totals[r] += 1
        total_trials += 1
    
    return {k: v / total_trials for k, v in totals.items()}


def expected_value(dice: int, sides: int) -> float:
    """
    Calculate expected value for dice roll.
    
    Args:
        dice: Number of dice
        sides: Number of sides per die
        
    Returns:
        Expected value of sum
        
    Examples:
        >>> expected_value(2, 6)
        7.0
        >>> expected_value(1, 20)
        10.5
    """
    # Expected value of single die: (1 + sides) / 2
    single_die_ev = (1 + sides) / 2
    return dice * single_die_ev


def variance(dice: int, sides: int) -> float:
    """
    Calculate variance for dice roll.
    
    Args:
        dice: Number of dice
        sides: Number of sides per die
        
    Returns:
        Variance of the sum
    """
    # Variance of single die: (sides^2 - 1) / 12
    single_die_var = (sides ** 2 - 1) / 12
    return dice * single_die_var


def standard_deviation(dice: int, sides: int) -> float:
    """
    Calculate standard deviation for dice roll.
    
    Args:
        dice: Number of dice
        sides: Number of sides per die
        
    Returns:
        Standard deviation of the sum
    """
    return variance(dice, sides) ** 0.5


def probability_at_least(dice: int, sides: int, target: int, trials: int = 10000) -> float:
    """
    Calculate probability of rolling at least target sum.
    
    Args:
        dice: Number of dice
        sides: Number of sides per die
        target: Target sum
        trials: Number of simulation trials
        
    Returns:
        Probability (0 to 1)
    """
    count = 0
    for _ in range(trials):
        if sum(roll(dice, sides)) >= target:
            count += 1
    return count / trials


def probability_exactly(dice: int, sides: int, target: int, trials: int = 10000) -> float:
    """
    Calculate probability of rolling exactly target sum.
    
    Args:
        dice: Number of dice
        sides: Number of sides per die
        target: Target sum
        trials: Number of simulation trials
        
    Returns:
        Probability (0 to 1)
    """
    count = 0
    for _ in range(trials):
        if sum(roll(dice, sides)) == target:
            count += 1
    return count / trials


# ============================================================================
# Batch Rolling
# ============================================================================

def batch_roll(notation: str, count: int) -> List[RollOutcome]:
    """
    Roll dice notation multiple times.
    
    Args:
        notation: Dice notation
        count: Number of times to roll
        
    Returns:
        List of RollOutcome objects
        
    Examples:
        >>> outcomes = batch_roll("2d6", 100)
        >>> len(outcomes)
        100
        >>> [o.total for o in outcomes[:5]]
        [9, 5, 11, 7, 8]
    """
    if count < 1:
        raise ValueError("Count must be at least 1")
    return [dice_parse(notation) for _ in range(count)]


def batch_stats(notation: str, count: int) -> RollStats:
    """
    Calculate statistics for multiple rolls.
    
    Args:
        notation: Dice notation
        count: Number of rolls
        
    Returns:
        RollStats with statistical summary
        
    Examples:
        >>> stats = batch_stats("d20", 1000)
        >>> stats.mean  # Average roll
        10.5
        >>> stats.percentile(95)  # 95th percentile
        19.0
    """
    if count < 1:
        raise ValueError("Count must be at least 1")
    
    outcomes = batch_roll(notation, count)
    totals = [o.total for o in outcomes]
    totals.sort()
    
    n = len(totals)
    mean = sum(totals) / n
    
    # Median
    if n % 2 == 0:
        median = (totals[n // 2 - 1] + totals[n // 2]) / 2
    else:
        median = totals[n // 2]
    
    # Standard deviation
    variance_val = sum((x - mean) ** 2 for x in totals) / n
    std_dev = variance_val ** 0.5
    
    return RollStats(
        notation=notation,
        count=count,
        totals=totals,
        min_total=totals[0],
        max_total=totals[-1],
        mean=mean,
        median=median,
        std_dev=std_dev
    )


# ============================================================================
# Weighted Dice
# ============================================================================

def roll_weighted(sides: int, weights: List[float]) -> int:
    """
    Roll weighted dice (probability distribution per side).
    
    Args:
        sides: Number of sides
        weights: Probability weight for each side (must sum to 1)
        
    Returns:
        Rolled value (1-indexed)
        
    Examples:
        >>> # Loaded d6 that favors 6
        >>> roll_weighted(6, [0.1, 0.1, 0.1, 0.1, 0.2, 0.4])
        6  # Most likely to be 6
    """
    if len(weights) != sides:
        raise ValueError("Number of weights must equal number of sides")
    if abs(sum(weights) - 1.0) > 0.001:
        raise ValueError("Weights must sum to 1")
    
    r = random.random()
    cumulative = 0.0
    for i, w in enumerate(weights):
        cumulative += w
        if r <= cumulative:
            return i + 1
    return sides


def roll_weighted_batch(dice: int, sides: int, weights: List[float]) -> List[int]:
    """
    Roll multiple weighted dice.
    
    Args:
        dice: Number of dice
        sides: Number of sides
        weights: Probability weights
        
    Returns:
        List of rolls
    """
    return [roll_weighted(sides, weights) for _ in range(dice)]


# ============================================================================
# Dice Pools
# ============================================================================

@dataclass
class DicePoolResult:
    """Result of rolling a dice pool."""
    results: List[int]
    success_threshold: int
    successes: int
    ones: int
    
    @property
    def net_successes(self) -> int:
        """Successes minus dramatic failures (1s that cancel successes)."""
        return self.successes - self.ones


def roll_pool(dice: int, sides: int = 10, success_threshold: int = 8) -> DicePoolResult:
    """
    Roll a dice pool with success counting (Storyteller/Storypath system).
    
    Args:
        dice: Number of dice in the pool
        sides: Number of sides (default 10)
        success_threshold: Minimum roll that counts as success (default 8)
        
    Returns:
        DicePoolResult with results and success count
        
    Examples:
        >>> result = roll_pool(8)  # Roll 8d10, count 8+ as success
        >>> result.successes
        3
        >>> result.net_successes  # Minus dramatic failures (1s)
        2
    """
    rolls = roll(dice, sides)
    successes = sum(1 for r in rolls if r >= success_threshold)
    ones = sum(1 for r in rolls if r == 1)
    
    return DicePoolResult(
        results=rolls,
        success_threshold=success_threshold,
        successes=successes,
        ones=ones
    )


# ============================================================================
# Convenience Exports
# ============================================================================

__all__ = [
    # Core functions
    'roll',
    'roll_with_reroll',
    'roll_exploding',
    'roll_fudge',
    'roll_weighted',
    'roll_weighted_batch',
    
    # Convenience
    'dice_roll',
    'dice_parse',
    'dice_parse_summary',
    
    # Fudge
    'fudge_total',
    
    # Stats
    'roll_distribution',
    'expected_value',
    'variance',
    'standard_deviation',
    'probability_at_least',
    'probability_exactly',
    'batch_roll',
    'batch_stats',
    
    # Advantage
    'advantage',
    'disadvantage',
    
    # Pools
    'roll_pool',
    
    # Types
    'DiceType',
    'RollOutcome',
    'RollStats',
    'DicePoolResult',
]