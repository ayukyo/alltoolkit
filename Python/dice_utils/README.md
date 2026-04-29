# Dice Utilities (dice_utils)

A comprehensive, zero-dependency dice rolling and probability calculation module for Python.

## Features

- **Basic Dice Rolling**: All standard dice (d4, d6, d8, d10, d12, d20, d100)
- **Dice Notation Parser**: Full support for standard notation (e.g., `2d6+3`, `4d6k3`)
- **Keep/Drop Mechanics**: Keep highest/lowest, drop highest/lowest dice
- **Exploding Dice**: Reroll on maximum value, with compounding option
- **Dice Pools**: Success-based rolling with thresholds
- **Fate/Fudge Dice**: Special dice for Fate Core system
- **Advantage/Disadvantage**: D&D 5e style rolling
- **Probability Calculations**: Distribution, expected value, variance
- **Monte Carlo Simulation**: Statistical analysis of dice outcomes
- **Dice Roller Class**: History tracking and analysis

## Quick Start

```python
from dice_utils import mod as dice

# Basic rolling
result = dice.roll(6, count=3)  # 3d6
print(f"Rolled: {result.dice}, Total: {result.total}")

# Using notation
result = dice.roll_notation("4d6k3")  # D&D ability scores
print(f"Kept dice: {result.kept}, Dropped: {result.dropped}")

# Advantage/disadvantage
result = dice.roll_with_advantage(20)  # d20 with advantage
print(f"Rolled {result.dice}, kept max: {result.total}")

# Fate dice
result = dice.roll_fate(4)  # 4dF
print(f"Result: {result.total} (range -4 to +4)")
```

## Dice Notation

Supported notation patterns:

| Notation | Description | Example |
|----------|-------------|---------|
| `NdS` | Roll N dice with S sides | `2d6`, `1d20` |
| `NdS+M` | Add modifier | `3d6+5` |
| `NdS-M` | Subtract modifier | `1d20-2` |
| `NdSkK` | Keep highest K dice | `4d6k3` |
| `NdSlK` | Keep lowest K dice | `4d6l2` |
| `NdSdK` | Drop lowest K dice | `4d6d1` |
| `NdShK` | Drop highest K dice | `4d6h1` |
| `NdS!` | Exploding dice | `d6!` |
| `NdS!!` | Compound exploding | `d6!!` |
| `NdSr` | Reroll 1s | `4d6r` |
| `NdSrN` | Reroll values ≤ N | `4d6r2` |

## Probability Functions

```python
from dice_utils import mod as dice

# Expected value of 2d6
print(dice.expected_value(2, 6))  # 7.0

# Probability of rolling at least 7 on 2d6
print(dice.probability_at_least(2, 6, 7))  # ~0.583

# Full probability distribution
dist = dice.dice_probability(2, 6)
print(f"Mean: {dist.mean}")
print(f"Std Dev: {dist.std_dev}")
print(f"P(7) = {dist.probability(7)}")
print(f"P(>=7) = {dist.probability_at_least(7)}")
```

## Dice Roller Class

```python
from dice_utils import mod as dice

roller = dice.DiceRoller(seed=42)  # Reproducible rolls

# Roll various dice
roller.roll("2d6+3")
roller.roll("1d20")
roller.roll_with_advantage(20)
roller.roll_fate(4)

# Analyze history
analysis = roller.analyze_history()
print(f"Total rolls: {analysis['total_rolls']}")
print(f"Average total: {analysis['mean_total']}")
```

## Monte Carlo Simulation

```python
from dice_utils import mod as dice

# Simulate 10,000 rolls of "2d6+5"
stats = dice.monte_carlo_simulation("2d6+5", iterations=10000)
print(f"Mean: {stats['mean']}")
print(f"Range: {stats['min']} to {stats['max']}")

# Compare two dice systems
comparison = dice.compare_rolls("2d6", "1d12")
print(f"2d6 wins: {comparison['notation1_wins']:.2%}")
print(f"1d12 wins: {comparison['notation2_wins']:.2%}")
```

## Dice Pools (Success-Based)

```python
from dice_utils import mod as dice

# World of Darkness style pool
result = dice.roll_world_of_darkness(5, difficulty=6)
print(f"Successes: {result.successes}")
print(f"Botches: {result.botches}")

# Custom dice pool
result = dice.roll_pool(10, 5, success_threshold=6, 
                        critical_threshold=10, double_success=True)
print(f"Rolled: {result.dice}")
print(f"Successes: {result.successes} (criticals count double)")
```

## API Reference

### Basic Rolling Functions

- `roll(sides, count=1, modifier=0)` - General dice roll
- `roll_d4(count=1)` - Roll d4 dice
- `roll_d6(count=1)` - Roll d6 dice
- `roll_d8(count=1)` - Roll d8 dice
- `roll_d10(count=1)` - Roll d10 dice
- `roll_d12(count=1)` - Roll d12 dice
- `roll_d20(count=1)` - Roll d20 dice
- `roll_d100(count=1)` - Roll d100 dice

### Shorthand Functions

- `d(sides, count=1)` - Shorthand for `roll()`
- `d4()`, `d6()`, `d8()`, `d10()`, `d12()`, `d20()`, `d100()`
- `dF(count=4)` - Fate dice shorthand

### Notation Functions

- `roll_notation(notation)` - Roll using notation string
- `DiceNotationParser` - Parser class for notation

### Keep/Drop Functions

- `roll_keep_highest(sides, count, keep)` - Keep highest dice
- `roll_keep_lowest(sides, count, keep)` - Keep lowest dice
- `roll_drop_lowest(sides, count, drop)` - Drop lowest dice
- `roll_drop_highest(sides, count, drop)` - Drop highest dice

### Special Rolling

- `roll_exploding(sides, count=1, compound=False)` - Exploding dice
- `roll_with_advantage(sides=20)` - Roll twice, take higher
- `roll_with_disadvantage(sides=20)` - Roll twice, take lower
- `roll_fate(count=4)` / `roll_fudge(count=4)` - Fate dice

### Dice Pool Functions

- `roll_pool(sides, count, success_threshold, ...)` - Success-based pool
- `roll_world_of_darkness(count, difficulty=6, specialty=False)` - WoD pool

### Probability Functions

- `dice_distribution(count, sides)` - Get distribution of sums
- `dice_probability(count, sides)` - Get probability distribution
- `probability_at_least(count, sides, target)` - P(X >= target)
- `probability_at_most(count, sides, target)` - P(X <= target)
- `probability_between(count, sides, min, max)` - P(min <= X <= max)
- `expected_value(count, sides)` - Calculate mean
- `variance(count, sides)` - Calculate variance
- `standard_deviation(count, sides)` - Calculate std dev

### Analysis Functions

- `monte_carlo_simulation(notation, iterations=10000)` - Monte Carlo stats
- `analyze_rolls(results)` - Analyze DiceResult list
- `compare_rolls(notation1, notation2, iterations)` - Compare two systems

### Classes

- `DiceRoller` - Dice roller with history tracking
- `DiceResult` - Result of a dice roll
- `DicePoolResult` - Result of a dice pool roll
- `ProbabilityDistribution` - Probability distribution object

## Use Cases

- **Tabletop RPGs**: D&D, Pathfinder, World of Darkness, Fate Core
- **Board Games**: Custom dice mechanics
- **Game Development**: Probability calculations, balance testing
- **Statistical Analysis**: Monte Carlo simulations
- **Education**: Teaching probability concepts

## Zero Dependencies

This module uses only Python standard library:
- `random` - Dice rolling
- `collections.Counter` - Statistics
- `functools.lru_cache` - Probability caching
- `dataclasses` - Result objects
- `re` - Notation parsing

## License

MIT License - Part of AllToolkit