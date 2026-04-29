"""
AllToolkit - Python Dice Utilities

A zero-dependency, production-ready dice rolling and probability calculation module.
Supports standard dice, dice notation parsing, probability distributions,
dice pools, Fate/Fudge dice, and statistical analysis.

Author: AllToolkit
License: MIT
"""

from typing import List, Tuple, Optional, Dict, Union, Callable, Iterator
from dataclasses import dataclass
from functools import lru_cache
from collections import Counter
import random
import re


# ============================================================================
# Data Classes
# ============================================================================

@dataclass
class DiceResult:
    """Represents the result of a dice roll."""
    dice: List[int]
    modifier: int
    total: int
    notation: str
    kept: Optional[List[int]] = None
    dropped: Optional[List[int]] = None
    
    def __repr__(self) -> str:
        return f"DiceResult(total={self.total}, dice={self.dice}, notation='{self.notation}')"
    
    @property
    def rolls(self) -> List[int]:
        """Get all rolls including dropped ones."""
        return self.dice
    
    @property
    def successful(self) -> List[int]:
        """Get kept rolls only."""
        return self.kept if self.kept is not None else self.dice


@dataclass
class DicePoolResult:
    """Represents the result of a dice pool roll."""
    dice: List[int]
    successes: int
    failures: int
    criticals: int
    botches: int
    total: int
    notation: str
    success_threshold: int
    critical_threshold: int
    botch_threshold: Optional[int]
    
    def __repr__(self) -> str:
        return (f"DicePoolResult(successes={self.successes}, criticals={self.criticals}, "
                f"total={self.total}, notation='{self.notation}')")


@dataclass
class ProbabilityDistribution:
    """Represents a probability distribution for dice outcomes."""
    outcomes: Dict[int, float]
    mean: float
    variance: float
    std_dev: float
    min_value: int
    max_value: int
    
    def probability(self, value: int) -> float:
        """Get probability of a specific value."""
        return self.outcomes.get(value, 0.0)
    
    def probability_at_least(self, value: int) -> float:
        """Get probability of rolling at least a given value."""
        return sum(p for v, p in self.outcomes.items() if v >= value)
    
    def probability_at_most(self, value: int) -> float:
        """Get probability of rolling at most a given value."""
        return sum(p for v, p in self.outcomes.items() if v <= value)
    
    def probability_between(self, min_val: int, max_val: int) -> float:
        """Get probability of rolling between min_val and max_val (inclusive)."""
        return sum(p for v, p in self.outcomes.items() if min_val <= v <= max_val)


# ============================================================================
# Basic Dice Rolling
# ============================================================================

def roll(sides: int, count: int = 1, modifier: int = 0) -> DiceResult:
    """
    Roll one or more dice with a modifier.
    
    Args:
        sides: Number of sides on each die
        count: Number of dice to roll (default: 1)
        modifier: Modifier to add to total (default: 0)
    
    Returns:
        DiceResult with roll details
    
    Example:
        >>> result = roll(20)  # Roll a d20
        >>> result.total >= 1
        True
        >>> result = roll(6, count=3, modifier=2)  # Roll 3d6+2
    """
    dice = [random.randint(1, sides) for _ in range(count)]
    total = sum(dice) + modifier
    notation = f"{count}d{sides}" + (f"+{modifier}" if modifier > 0 else f"{modifier}" if modifier < 0 else "")
    
    return DiceResult(
        dice=dice,
        modifier=modifier,
        total=total,
        notation=notation
    )


def roll_d4(count: int = 1) -> DiceResult:
    """Roll one or more d4 dice."""
    return roll(4, count)


def roll_d6(count: int = 1) -> DiceResult:
    """Roll one or more d6 dice."""
    return roll(6, count)


def roll_d8(count: int = 1) -> DiceResult:
    """Roll one or more d8 dice."""
    return roll(8, count)


def roll_d10(count: int = 1) -> DiceResult:
    """Roll one or more d10 dice."""
    return roll(10, count)


def roll_d12(count: int = 1) -> DiceResult:
    """Roll one or more d12 dice."""
    return roll(12, count)


def roll_d20(count: int = 1) -> DiceResult:
    """Roll one or more d20 dice."""
    return roll(20, count)


def roll_d100(count: int = 1) -> DiceResult:
    """Roll one or more d100 (percentile) dice."""
    return roll(100, count)


def roll_percentile() -> DiceResult:
    """Roll percentile dice (d100) for a percentage result."""
    return roll_d100(1)


# ============================================================================
# Dice Notation Parser
# ============================================================================

class DiceNotationParser:
    """
    Parse and evaluate dice notation.
    
    Supported notation:
        - NdS: Roll N dice with S sides (e.g., 3d6, 1d20)
        - NdS+M: Add modifier (e.g., 2d6+3)
        - NdS-M: Subtract modifier (e.g., 1d20-2)
        - NdSkK: Keep highest K dice (e.g., 4d6k3)
        - NdSlK: Keep lowest K dice (e.g., 4d6l3)
        - NdShK: Drop highest K dice (e.g., 4d6h1)
        - NdSdK: Drop lowest K dice (e.g., 4d6d1)
        - NdS!: Exploding dice (roll again on max)
        - NdS!!: Exploding and compounding dice
        - NdSr: Reroll 1s
        - NdSrN: Reroll values <= N
    
    Example:
        >>> parser = DiceNotationParser()
        >>> parser.roll("2d6+3")
        DiceResult(total=..., dice=[...], notation='2d6+3')
        >>> parser.roll("4d6k3")  # D&D ability score generation
        DiceResult(total=..., ...)
    """
    
    # Pattern for basic dice notation
    DICE_PATTERN = re.compile(
        r'^(\d+)?d(\d+)'  # Required: count and sides
        r'(?:([kdhl])(\d+))?'  # Keep/drop modifier
        r'(?:([+-])(\d+))?'  # Arithmetic modifier
        r'([!]*|r(?:\d+)?)?'  # Special modifiers (explode, reroll)
        r'$',
        re.IGNORECASE
    )
    
    def __init__(self, seed: Optional[int] = None):
        """Initialize parser with optional random seed for reproducibility."""
        self.seed = seed
        if seed is not None:
            random.seed(seed)
    
    def parse(self, notation: str) -> Dict:
        """
        Parse dice notation into components.
        
        Args:
            notation: Dice notation string
        
        Returns:
            Dict with parsed components
        
        Raises:
            ValueError: If notation is invalid
        """
        notation = notation.strip().replace(' ', '')
        
        match = self.DICE_PATTERN.match(notation)
        if not match:
            raise ValueError(f"Invalid dice notation: {notation}")
        
        count = int(match.group(1)) if match.group(1) else 1
        sides = int(match.group(2))
        keep_type = match.group(3)
        keep_count = int(match.group(4)) if match.group(4) else None
        mod_op = match.group(5)
        mod_val = int(match.group(6)) if match.group(6) else 0
        special = match.group(7) or ''
        
        # Parse special modifiers
        explode = special.count('!')
        reroll_threshold = 0
        if special.startswith('r'):
            reroll_str = special[1:]
            reroll_threshold = int(reroll_str) if reroll_str else 1
        
        return {
            'count': count,
            'sides': sides,
            'keep_type': keep_type,
            'keep_count': keep_count,
            'modifier': mod_val if mod_op == '+' else -mod_val if mod_op == '-' else 0,
            'explode': explode,
            'reroll_threshold': reroll_threshold,
            'notation': notation,
        }
    
    def roll(self, notation: str) -> DiceResult:
        """
        Roll dice according to notation.
        
        Args:
            notation: Dice notation string
        
        Returns:
            DiceResult with roll details
        """
        parsed = self.parse(notation)
        
        count = parsed['count']
        sides = parsed['sides']
        keep_type = parsed['keep_type']
        keep_count = parsed['keep_count']
        modifier = parsed['modifier']
        explode = parsed['explode']
        reroll_threshold = parsed['reroll_threshold']
        
        # Roll dice
        dice = []
        
        if explode > 0:
            # Exploding dice
            dice = self._roll_exploding(count, sides, explode == 2)
        elif reroll_threshold > 0:
            # Reroll dice below threshold
            dice = [self._roll_with_reroll(sides, reroll_threshold) for _ in range(count)]
        else:
            dice = [random.randint(1, sides) for _ in range(count)]
        
        # Apply keep/drop modifiers
        kept = dice.copy()
        dropped = []
        
        if keep_type == 'k':
            # Keep highest N
            sorted_dice = sorted(dice, reverse=True)
            kept = sorted_dice[:keep_count]
            dropped = sorted_dice[keep_count:]
        elif keep_type == 'l':
            # Keep lowest N
            sorted_dice = sorted(dice)
            kept = sorted_dice[:keep_count]
            dropped = sorted_dice[keep_count:]
        elif keep_type == 'h':
            # Drop highest N (keep lowest)
            sorted_dice = sorted(dice)
            dropped = sorted_dice[-keep_count:] if keep_count else []
            kept = sorted_dice[:-keep_count] if keep_count else sorted_dice
        elif keep_type == 'd':
            # Drop lowest N (keep highest)
            sorted_dice = sorted(dice, reverse=True)
            dropped = sorted_dice[-keep_count:] if keep_count else []
            kept = sorted_dice[:-keep_count] if keep_count else sorted_dice
        
        total = sum(kept) + modifier
        
        return DiceResult(
            dice=dice,
            modifier=modifier,
            total=total,
            notation=parsed['notation'],
            kept=kept,
            dropped=dropped if dropped else None
        )
    
    def _roll_exploding(self, count: int, sides: int, compound: bool = False) -> List[int]:
        """Roll exploding dice."""
        results = []
        for _ in range(count):
            roll = random.randint(1, sides)
            results.append(roll)
            # Keep rolling on max
            while roll == sides:
                roll = random.randint(1, sides)
                if compound:
                    results[-1] += roll
                else:
                    results.append(roll)
        return results
    
    def _roll_with_reroll(self, sides: int, threshold: int) -> int:
        """Roll with rerolls below threshold."""
        roll = random.randint(1, sides)
        while roll <= threshold:
            roll = random.randint(1, sides)
        return roll
    
    def evaluate(self, notation: str) -> DiceResult:
        """Alias for roll()."""
        return self.roll(notation)


# Global parser instance
_parser = DiceNotationParser()


def roll_notation(notation: str, seed: Optional[int] = None) -> DiceResult:
    """
    Roll dice using standard notation.
    
    Args:
        notation: Dice notation string (e.g., "2d6+3", "4d6k3", "1d20")
        seed: Optional random seed for reproducibility
    
    Returns:
        DiceResult with roll details
    
    Example:
        >>> roll_notation("2d6+3")
        DiceResult(total=..., dice=[...], notation='2d6+3')
        >>> roll_notation("4d6k3")  # Keep highest 3
        DiceResult(total=..., kept=[...], ...)
    """
    parser = DiceNotationParser(seed) if seed is not None else _parser
    return parser.roll(notation)


# ============================================================================
# Keep/Drop Dice
# ============================================================================

def roll_keep_highest(sides: int, count: int, keep: int) -> DiceResult:
    """
    Roll dice and keep the highest values.
    
    Args:
        sides: Number of sides on each die
        count: Number of dice to roll
        keep: Number of highest dice to keep
    
    Returns:
        DiceResult with kept dice
    
    Example:
        >>> result = roll_keep_highest(6, 4, 3)  # 4d6k3, D&D ability scores
        >>> len(result.kept) == 3
        True
    """
    dice = [random.randint(1, sides) for _ in range(count)]
    sorted_dice = sorted(dice, reverse=True)
    kept = sorted_dice[:keep]
    dropped = sorted_dice[keep:]
    
    return DiceResult(
        dice=dice,
        modifier=0,
        total=sum(kept),
        notation=f"{count}d{sides}k{keep}",
        kept=kept,
        dropped=dropped
    )


def roll_keep_lowest(sides: int, count: int, keep: int) -> DiceResult:
    """
    Roll dice and keep the lowest values.
    
    Args:
        sides: Number of sides on each die
        count: Number of dice to roll
        keep: Number of lowest dice to keep
    
    Returns:
        DiceResult with kept dice
    """
    dice = [random.randint(1, sides) for _ in range(count)]
    sorted_dice = sorted(dice)
    kept = sorted_dice[:keep]
    dropped = sorted_dice[keep:]
    
    return DiceResult(
        dice=dice,
        modifier=0,
        total=sum(kept),
        notation=f"{count}d{sides}l{keep}",
        kept=kept,
        dropped=dropped
    )


def roll_drop_lowest(sides: int, count: int, drop: int) -> DiceResult:
    """
    Roll dice and drop the lowest values.
    
    Args:
        sides: Number of sides on each die
        count: Number of dice to roll
        drop: Number of lowest dice to drop
    
    Returns:
        DiceResult with remaining dice
    """
    return roll_keep_highest(sides, count, count - drop)


def roll_drop_highest(sides: int, count: int, drop: int) -> DiceResult:
    """
    Roll dice and drop the highest values.
    
    Args:
        sides: Number of sides on each die
        count: Number of dice to roll
        drop: Number of highest dice to drop
    
    Returns:
        DiceResult with remaining dice
    """
    return roll_keep_lowest(sides, count, count - drop)


# ============================================================================
# Exploding Dice
# ============================================================================

def roll_exploding(sides: int, count: int = 1, compound: bool = False) -> DiceResult:
    """
    Roll exploding dice (reroll on maximum value).
    
    Args:
        sides: Number of sides on each die
        count: Number of dice to roll
        compound: If True, add exploded rolls to the original die
    
    Returns:
        DiceResult with all rolls (including explosions)
    
    Example:
        >>> result = roll_exploding(6, 1)  # d6!
        >>> len(result.dice) >= 1
        True
    """
    dice = []
    for _ in range(count):
        roll = random.randint(1, sides)
        if compound:
            # Compound: add to same die
            while roll == sides:
                roll = random.randint(1, sides)
                dice[-1] += roll if dice else roll
            if not dice:
                dice.append(roll)
        else:
            # Regular explode: add new die
            dice.append(roll)
            while roll == sides:
                roll = random.randint(1, sides)
                dice.append(roll)
    
    notation = f"{count}d{sides}!" + ("!" if compound else "")
    
    return DiceResult(
        dice=dice,
        modifier=0,
        total=sum(dice),
        notation=notation
    )


# ============================================================================
# Dice Pools
# ============================================================================

def roll_pool(
    sides: int,
    count: int,
    success_threshold: int,
    critical_threshold: Optional[int] = None,
    botch_threshold: Optional[int] = None,
    double_success: bool = False,
) -> DicePoolResult:
    """
    Roll a dice pool and count successes.
    
    Args:
        sides: Number of sides on each die
        count: Number of dice to roll
        success_threshold: Minimum value for a success
        critical_threshold: Value for critical success (default: sides)
        botch_threshold: Value for botch/failure (default: 1)
        double_success: Count criticals as 2 successes
    
    Returns:
        DicePoolResult with success counts
    
    Example:
        >>> result = roll_pool(10, 5, 6, critical_threshold=10, botch_threshold=1)
        >>> result.successes >= 0
        True
    """
    if critical_threshold is None:
        critical_threshold = sides
    if botch_threshold is None:
        botch_threshold = 1
    
    dice = [random.randint(1, sides) for _ in range(count)]
    
    successes = 0
    failures = 0
    criticals = 0
    botches = 0
    
    for die in dice:
        if die >= critical_threshold:
            criticals += 1
            successes += 2 if double_success else 1
        elif die >= success_threshold:
            successes += 1
        elif die <= botch_threshold:
            botches += 1
            failures += 1
        else:
            failures += 1
    
    notation = f"{count}d{sides}>={success_threshold}"
    
    return DicePoolResult(
        dice=dice,
        successes=successes,
        failures=failures,
        criticals=criticals,
        botches=botches,
        total=sum(dice),
        notation=notation,
        success_threshold=success_threshold,
        critical_threshold=critical_threshold,
        botch_threshold=botch_threshold
    )


def roll_world_of_darkness(
    count: int,
    difficulty: int = 6,
    specialty: bool = False,
) -> DicePoolResult:
    """
    Roll World of Darkness style dice pool (d10 system).
    
    Args:
        count: Number of d10 dice to roll
        difficulty: Target number for success
        specialty: If True, 10s count as 2 successes
    
    Returns:
        DicePoolResult with success counts
    """
    dice = [random.randint(1, 10) for _ in range(count)]
    
    successes = 0
    failures = 0
    criticals = 0
    botches = 0
    
    for die in dice:
        if die == 1:
            botches += 1
            # Botches subtract from successes in WoD
        elif die == 10:
            criticals += 1
            successes += 2 if specialty else 1
        elif die >= difficulty:
            successes += 1
        else:
            failures += 1
    
    # Apply botches
    actual_successes = max(0, successes - botches)
    
    return DicePoolResult(
        dice=dice,
        successes=actual_successes,
        failures=failures,
        criticals=criticals,
        botches=botches,
        total=sum(dice),
        notation=f"{count}d10>={difficulty}",
        success_threshold=difficulty,
        critical_threshold=10,
        botch_threshold=1
    )


# ============================================================================
# Fate/Fudge Dice
# ============================================================================

FATE_FACES = [-1, -1, 0, 0, 1, 1]  # [-, -, ' ', ' ', +, +]


def roll_fate(count: int = 4) -> DiceResult:
    """
    Roll Fate/Fudge dice (dF).
    
    Each die has: -, -, blank, blank, +, +
    Values: -1, -1, 0, 0, +1, +1
    
    Args:
        count: Number of Fate dice to roll (default: 4)
    
    Returns:
        DiceResult with Fate dice results
    
    Example:
        >>> result = roll_fate(4)
        >>> -4 <= result.total <= 4
        True
    """
    dice = [random.choice(FATE_FACES) for _ in range(count)]
    
    return DiceResult(
        dice=dice,
        modifier=0,
        total=sum(dice),
        notation=f"{count}dF"
    )


def roll_fudge(count: int = 4) -> DiceResult:
    """Alias for roll_fate()."""
    return roll_fate(count)


# ============================================================================
# Probability Calculations
# ============================================================================

@lru_cache(maxsize=128)
def dice_distribution(count: int, sides: int) -> Dict[int, int]:
    """
    Calculate the distribution of sums for NdS dice.
    
    Uses dynamic programming for efficient calculation.
    
    Args:
        count: Number of dice
        sides: Number of sides on each die
    
    Returns:
        Dict mapping sum to number of ways to achieve it
    
    Example:
        >>> dist = dice_distribution(2, 6)
        >>> dist[7]  # Ways to roll 7 with 2d6
        6
    """
    if count == 0:
        return {0: 1}
    
    if count == 1:
        return {i: 1 for i in range(1, sides + 1)}
    
    # Use dynamic programming
    prev_dist = dice_distribution(count - 1, sides)
    result: Dict[int, int] = {}
    
    for prev_sum, ways in prev_dist.items():
        for face in range(1, sides + 1):
            new_sum = prev_sum + face
            result[new_sum] = result.get(new_sum, 0) + ways
    
    return result


def dice_probability(count: int, sides: int) -> ProbabilityDistribution:
    """
    Calculate the probability distribution for NdS dice.
    
    Args:
        count: Number of dice
        sides: Number of sides on each die
    
    Returns:
        ProbabilityDistribution with all statistics
    
    Example:
        >>> dist = dice_probability(2, 6)
        >>> dist.mean
        7.0
        >>> dist.probability(7)  # Probability of rolling 7
        0.1666...
    """
    dist = dice_distribution(count, sides)
    total_outcomes = sides ** count
    
    # Calculate probabilities
    outcomes = {k: v / total_outcomes for k, v in dist.items()}
    
    # Calculate mean
    mean = sum(value * prob for value, prob in outcomes.items())
    
    # Calculate variance
    variance = sum((value - mean) ** 2 * prob for value, prob in outcomes.items())
    
    # Standard deviation
    std_dev = variance ** 0.5
    
    # Min and max
    min_value = count
    max_value = count * sides
    
    return ProbabilityDistribution(
        outcomes=outcomes,
        mean=mean,
        variance=variance,
        std_dev=std_dev,
        min_value=min_value,
        max_value=max_value
    )


def probability_at_least(count: int, sides: int, target: int) -> float:
    """
    Calculate probability of rolling at least a target value.
    
    Args:
        count: Number of dice
        sides: Number of sides on each die
        target: Target sum to reach or exceed
    
    Returns:
        Probability between 0.0 and 1.0
    
    Example:
        >>> probability_at_least(2, 6, 7)
        0.5833...
    """
    dist = dice_probability(count, sides)
    return dist.probability_at_least(target)


def probability_at_most(count: int, sides: int, target: int) -> float:
    """
    Calculate probability of rolling at most a target value.
    
    Args:
        count: Number of dice
        sides: Number of sides on each die
        target: Target sum to not exceed
    
    Returns:
        Probability between 0.0 and 1.0
    """
    dist = dice_probability(count, sides)
    return dist.probability_at_most(target)


def probability_between(count: int, sides: int, min_val: int, max_val: int) -> float:
    """
    Calculate probability of rolling between min and max (inclusive).
    
    Args:
        count: Number of dice
        sides: Number of sides on each die
        min_val: Minimum sum
        max_val: Maximum sum
    
    Returns:
        Probability between 0.0 and 1.0
    """
    dist = dice_probability(count, sides)
    return dist.probability_between(min_val, max_val)


def expected_value(count: int, sides: int) -> float:
    """
    Calculate expected value (mean) of NdS roll.
    
    E[NdS] = N * (S + 1) / 2
    
    Args:
        count: Number of dice
        sides: Number of sides on each die
    
    Returns:
        Expected value
    
    Example:
        >>> expected_value(2, 6)
        7.0
    """
    return count * (sides + 1) / 2


def variance(count: int, sides: int) -> float:
    """
    Calculate variance of NdS roll.
    
    Var(NdS) = N * (S^2 - 1) / 12
    
    Args:
        count: Number of dice
        sides: Number of sides on each die
    
    Returns:
        Variance
    """
    return count * (sides ** 2 - 1) / 12


def standard_deviation(count: int, sides: int) -> float:
    """
    Calculate standard deviation of NdS roll.
    
    Args:
        count: Number of dice
        sides: Number of sides on each die
    
    Returns:
        Standard deviation
    """
    return variance(count, sides) ** 0.5


# ============================================================================
# Statistical Analysis
# ============================================================================

def monte_carlo_simulation(
    notation: str,
    iterations: int = 10000,
    seed: Optional[int] = None,
) -> Dict[str, Union[float, int, Dict[int, float]]]:
    """
    Run Monte Carlo simulation for dice notation.
    
    Args:
        notation: Dice notation string
        iterations: Number of iterations to run
        seed: Random seed for reproducibility
    
    Returns:
        Dict with statistics and distribution
    
    Example:
        >>> stats = monte_carlo_simulation("2d6", 10000)
        >>> 6.5 < stats['mean'] < 7.5
        True
    """
    if seed is not None:
        random.seed(seed)
    
    parser = DiceNotationParser()
    results = []
    
    for _ in range(iterations):
        result = parser.roll(notation)
        results.append(result.total)
    
    # Calculate statistics
    mean = sum(results) / iterations
    variance = sum((x - mean) ** 2 for x in results) / iterations
    std_dev = variance ** 0.5
    
    # Build distribution
    counter = Counter(results)
    distribution = {k: v / iterations for k, v in sorted(counter.items())}
    
    return {
        'mean': mean,
        'variance': variance,
        'std_dev': std_dev,
        'min': min(results),
        'max': max(results),
        'median': sorted(results)[iterations // 2],
        'distribution': distribution,
        'iterations': iterations,
    }


def analyze_rolls(results: List[DiceResult]) -> Dict[str, float]:
    """
    Analyze a series of dice roll results.
    
    Args:
        results: List of DiceResult objects
    
    Returns:
        Dict with analysis statistics
    """
    if not results:
        return {}
    
    totals = [r.total for r in results]
    all_dice = [d for r in results for d in r.dice]
    
    mean_total = sum(totals) / len(totals)
    var_total = sum((t - mean_total) ** 2 for t in totals) / len(totals)
    
    mean_die = sum(all_dice) / len(all_dice) if all_dice else 0
    var_die = sum((d - mean_die) ** 2 for d in all_dice) / len(all_dice) if all_dice else 0
    
    # Count frequency of each die value
    die_counter = Counter(all_dice)
    total_rolls = len(all_dice)
    
    return {
        'total_rolls': len(results),
        'total_dice': len(all_dice),
        'mean_total': mean_total,
        'variance_total': var_total,
        'std_dev_total': var_total ** 0.5,
        'min_total': min(totals),
        'max_total': max(totals),
        'mean_die_value': mean_die,
        'variance_die': var_die,
        'die_distribution': {k: v / total_rolls for k, v in sorted(die_counter.items())},
    }


# ============================================================================
# Advantage/Disadvantage
# ============================================================================

def roll_with_advantage(sides: int = 20) -> DiceResult:
    """
    Roll with advantage (roll twice, take higher).
    
    Args:
        sides: Number of sides on the die (default: 20)
    
    Returns:
        DiceResult with the higher of two rolls
    
    Example:
        >>> result = roll_with_advantage(20)
        >>> len(result.dice) == 2
        True
        >>> result.total == max(result.dice)
        True
    """
    dice = [random.randint(1, sides) for _ in range(2)]
    total = max(dice)
    
    return DiceResult(
        dice=dice,
        modifier=0,
        total=total,
        notation=f"2d{sides}kh1"
    )


def roll_with_disadvantage(sides: int = 20) -> DiceResult:
    """
    Roll with disadvantage (roll twice, take lower).
    
    Args:
        sides: Number of sides on the die (default: 20)
    
    Returns:
        DiceResult with the lower of two rolls
    """
    dice = [random.randint(1, sides) for _ in range(2)]
    total = min(dice)
    
    return DiceResult(
        dice=dice,
        modifier=0,
        total=total,
        notation=f"2d{sides}kl1"
    )


# ============================================================================
# Dice Comparison
# ============================================================================

def compare_rolls(notation1: str, notation2: str, iterations: int = 10000) -> Dict[str, float]:
    """
    Compare two dice notations by simulation.
    
    Args:
        notation1: First dice notation
        notation2: Second dice notation
        iterations: Number of simulation iterations
    
    Returns:
        Dict with comparison statistics
    
    Example:
        >>> result = compare_rolls("2d6", "1d12")
        >>> result['notation1_wins'] + result['notation2_wins'] + result['ties']
        1.0
    """
    parser = DiceNotationParser()
    
    wins1 = 0
    wins2 = 0
    ties = 0
    
    for _ in range(iterations):
        r1 = parser.roll(notation1)
        r2 = parser.roll(notation2)
        
        if r1.total > r2.total:
            wins1 += 1
        elif r2.total > r1.total:
            wins2 += 1
        else:
            ties += 1
    
    return {
        'notation1': notation1,
        'notation2': notation2,
        'notation1_wins': wins1 / iterations,
        'notation2_wins': wins2 / iterations,
        'ties': ties / iterations,
        'iterations': iterations,
    }


# ============================================================================
# Dice String Generation
# ============================================================================

def dice_to_string(dice: List[int], modifier: int = 0, sides: Optional[int] = None) -> str:
    """
    Convert dice rolls to notation string.
    
    Args:
        dice: List of dice values
        modifier: Modifier to add
        sides: Number of sides (inferred if not provided)
    
    Returns:
        Notation string
    
    Example:
        >>> dice_to_string([5, 3, 6], modifier=2)
        '3d6+2 (5, 3, 6)'
    """
    count = len(dice)
    sides_val = sides or max(dice) if dice else 6
    total = sum(dice) + modifier
    
    base = f"{count}d{sides_val}"
    if modifier > 0:
        base += f"+{modifier}"
    elif modifier < 0:
        base += str(modifier)
    
    return f"{base} ({', '.join(map(str, dice))}) = {total}"


# ============================================================================
# Dice Roller Class
# ============================================================================

class DiceRoller:
    """
    A configurable dice roller with history tracking.
    
    Example:
        >>> roller = DiceRoller(seed=42)
        >>> roller.roll("2d6+3")
        DiceResult(...)
        >>> roller.history
        [...]
    """
    
    def __init__(self, seed: Optional[int] = None):
        """
        Initialize the dice roller.
        
        Args:
            seed: Random seed for reproducibility
        """
        self.seed = seed
        self.parser = DiceNotationParser(seed)
        self.history: List[DiceResult] = []
    
    def roll(self, notation: str) -> DiceResult:
        """Roll dice using notation and record to history."""
        result = self.parser.roll(notation)
        self.history.append(result)
        return result
    
    def roll_d(self, sides: int, count: int = 1, modifier: int = 0) -> DiceResult:
        """Roll standard dice."""
        notation = f"{count}d{sides}"
        if modifier > 0:
            notation += f"+{modifier}"
        elif modifier < 0:
            notation += str(modifier)
        return self.roll(notation)
    
    def roll_with_advantage(self, sides: int = 20) -> DiceResult:
        """Roll with advantage."""
        result = roll_with_advantage(sides)
        self.history.append(result)
        return result
    
    def roll_with_disadvantage(self, sides: int = 20) -> DiceResult:
        """Roll with disadvantage."""
        result = roll_with_disadvantage(sides)
        self.history.append(result)
        return result
    
    def roll_fate(self, count: int = 4) -> DiceResult:
        """Roll Fate dice."""
        result = roll_fate(count)
        self.history.append(result)
        return result
    
    def clear_history(self) -> None:
        """Clear roll history."""
        self.history = []
    
    def analyze_history(self) -> Dict[str, float]:
        """Analyze all recorded rolls."""
        return analyze_rolls(self.history)
    
    @property
    def total_rolls(self) -> int:
        """Get total number of rolls."""
        return len(self.history)
    
    @property
    def last_roll(self) -> Optional[DiceResult]:
        """Get the last roll."""
        return self.history[-1] if self.history else None


# ============================================================================
# Convenience Functions
# ============================================================================

def d(sides: int, count: int = 1) -> DiceResult:
    """Shorthand for roll()."""
    return roll(sides, count)


def d4(count: int = 1) -> DiceResult:
    """Shorthand for roll_d4()."""
    return roll_d4(count)


def d6(count: int = 1) -> DiceResult:
    """Shorthand for roll_d6()."""
    return roll_d6(count)


def d8(count: int = 1) -> DiceResult:
    """Shorthand for roll_d8()."""
    return roll_d8(count)


def d10(count: int = 1) -> DiceResult:
    """Shorthand for roll_d10()."""
    return roll_d10(count)


def d12(count: int = 1) -> DiceResult:
    """Shorthand for roll_d12()."""
    return roll_d12(count)


def d20(count: int = 1) -> DiceResult:
    """Shorthand for roll_d20()."""
    return roll_d20(count)


def d100(count: int = 1) -> DiceResult:
    """Shorthand for roll_d100()."""
    return roll_d100(count)


def dF(count: int = 4) -> DiceResult:
    """Shorthand for roll_fate()."""
    return roll_fate(count)