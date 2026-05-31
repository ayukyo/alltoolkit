#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AllToolkit - Dice Utils Usage Examples
======================================
Usage examples for dice utilities module.
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mod import (
    roll, roll_with_reroll, roll_exploding, roll_fudge,
    dice_roll, dice_parse,
    fudge_total, advantage, disadvantage,
    roll_distribution, expected_value, variance, standard_deviation,
    probability_at_least, probability_exactly,
    batch_roll, batch_stats,
    roll_weighted, roll_weighted_batch,
    roll_pool,
    RollOutcome, RollStats, DicePoolResult
)


def example_basic_rolling():
    """Basic dice rolling examples."""
    print("=" * 50)
    print("Basic Dice Rolling")
    print("=" * 50)
    
    # Roll a single d6
    print("\n1. Roll a single d6:")
    result = roll(1, 6)
    print(f"   roll(1, 6) = {result}")
    
    # Roll multiple dice
    print("\n2. Roll three d6:")
    result = roll(3, 6)
    print(f"   roll(3, 6) = {result}")
    
    # Roll a d20
    print("\n3. Roll a d20 (for D&D):")
    result = roll(1, 20)
    print(f"   roll(1, 20) = {result}")


def example_dice_notation():
    """Dice notation examples."""
    print("\n" + "=" * 50)
    print("Dice Notation")
    print("=" * 50)
    
    # Simple notation
    print("\n1. Simple notation (2d6):")
    outcome = dice_parse("2d6")
    print(f"   dice_parse('2d6') = {outcome}")
    print(f"   Total: {outcome.total}")
    
    # With modifier
    print("\n2. With modifier (2d6+3):")
    outcome = dice_parse("2d6+3")
    print(f"   dice_parse('2d6+3')")
    print(f"   Rolls: {outcome.rolls}")
    print(f"   Modifier: {outcome.modifier}")
    print(f"   Total: {outcome.total}")
    
    # Keep highest
    print("\n3. Keep highest 3 of 4d20:")
    outcome = dice_parse("4d20kh3")
    print(f"   dice_parse('4d20kh3')")
    print(f"   All rolls: {outcome.rolls}")
    print(f"   Kept: {outcome.kept}")
    print(f"   Dropped: {outcome.dropped}")
    print(f"   Total: {outcome.total}")
    
    # Drop lowest
    print("\n4. Drop lowest 2 of 8d6:")
    outcome = dice_parse("8d6dl2")
    print(f"   dice_parse('8d6dl2')")
    print(f"   Total: {outcome.total}")
    
    # Exploding dice
    print("\n5. Exploding dice (2d6!):")
    outcome = dice_parse("2d6!")
    print(f"   dice_parse('2d6!')")
    print(f"   Rolls: {outcome.rolls}")
    print(f"   Total: {outcome.total}")
    
    # Reroll
    print("\n6. Reroll 1s and 2s (5d6r2):")
    outcome = dice_parse("5d6r2")
    print(f"   dice_parse('5d6r2')")
    print(f"   Rolls: {outcome.rolls}")
    print(f"   (All rolls > 2)")
    
    # Target number
    print("\n7. Target number (6d6>=4):")
    outcome = dice_parse("6d6>=4")
    print(f"   dice_parse('6d6>=4')")
    print(f"   Rolls: {outcome.rolls}")
    print(f"   Successes (4+): {outcome.success_count}")
    print(f"   Failures: {outcome.failure_count}")


def example_convenience_function():
    """Convenience function examples."""
    print("\n" + "=" * 50)
    print("Convenience Function (dice_roll)")
    print("=" * 50)
    
    print("\n1. dice_roll('d20+5'):")
    result = dice_roll("d20+5")
    print(f"   Result: {result}")
    
    print("\n2. dice_roll('4d6kh3'):")
    result = dice_roll("4d6kh3")
    print(f"   Result: {result}")
    
    print("\n3. dice_roll('d100'):")  # percentile dice
    result = dice_roll("d100")
    print(f"   Result: {result}")


def example_advantage_disadvantage():
    """Advantage/disadvantage examples."""
    print("\n" + "=" * 50)
    print("Advantage & Disadvantage")
    print("=" * 50)
    
    print("\n1. Roll with advantage (d20):")
    r1, r2, result = advantage()
    print(f"   advantage() = ({r1}, {r2}, {result})")
    print(f"   Take higher: {result}")
    
    print("\n2. Roll with disadvantage (d20):")
    r1, r2, result = disadvantage()
    print(f"   disadvantage() = ({r1}, {r2}, {result})")
    print(f"   Take lower: {result}")


def example_fudge_dice():
    """Fudge/FATE dice examples."""
    print("\n" + "=" * 50)
    print("Fudge/FATE Dice")
    print("=" * 50)
    
    print("\n1. Roll 4 Fudge dice:")
    result = roll_fudge(4)
    print(f"   roll_fudge(4) = {result}")
    print(f"   Total: {sum(result)}")
    
    print("\n2. Using fudge_total:")
    total = fudge_total(4)
    print(f"   fudge_total(4) = {total}")


def example_statistics():
    """Statistics examples."""
    print("\n" + "=" * 50)
    print("Statistics & Probability")
    print("=" * 50)
    
    print("\n1. Expected value of 2d6:")
    ev = expected_value(2, 6)
    print(f"   expected_value(2, 6) = {ev}")
    
    print("\n2. Variance of 2d6:")
    var = variance(2, 6)
    print(f"   variance(2, 6) = {var:.4f}")
    
    print("\n3. Standard deviation of 2d6:")
    sd = standard_deviation(2, 6)
    print(f"   standard_deviation(2, 6) = {sd:.4f}")
    
    print("\n4. Probability of rolling 8+ with 2d6:")
    prob = probability_at_least(2, 6, 8, trials=10000)
    print(f"   probability_at_least(2, 6, 8) = {prob:.2%}")
    
    print("\n5. Distribution simulation (2d6, 5000 trials):")
    dist = roll_distribution(2, 6, trials=5000)
    for k in sorted(dist.keys()):
        print(f"   {k}: {'#' * int(dist[k] * 200):<50} {dist[k]:.2%}")


def example_batch_rolling():
    """Batch rolling examples."""
    print("\n" + "=" * 50)
    print("Batch Rolling")
    print("=" * 50)
    
    print("\n1. Batch roll 10 times:")
    results = batch_roll("2d6", 10)
    totals = [r.total for r in results]
    print(f"   Totals: {totals}")
    
    print("\n2. Statistics for 100 d20 rolls:")
    stats = batch_stats("d20", 100)
    print(f"   Count: {stats.count}")
    print(f"   Mean: {stats.mean:.2f}")
    print(f"   Median: {stats.median:.2f}")
    print(f"   Std Dev: {stats.std_dev:.2f}")
    print(f"   Min: {stats.min_total}")
    print(f"   Max: {stats.max_total}")
    print(f"   95th percentile: {stats.percentile(95):.1f}")


def example_weighted_dice():
    """Weighted dice examples."""
    print("\n" + "=" * 50)
    print("Weighted Dice")
    print("=" * 50)
    
    # Loaded dice
    weights = [0.05, 0.05, 0.1, 0.1, 0.2, 0.5]  # Heavily favors 6
    
    print("\n1. Loaded d6 (50% chance of rolling 6):")
    results = roll_weighted_batch(20, 6, weights)
    count_6 = results.count(6)
    print(f"   20 rolls: {results}")
    print(f"   Count of 6: {count_6} ({count_6/20:.0%})")


def example_dice_pools():
    """Dice pool examples (Storyteller system)."""
    print("\n" + "=" * 50)
    print("Dice Pools (Storyteller System)")
    print("=" * 50)
    
    print("\n1. Roll 8d10, count 8+ as success:")
    result = roll_pool(8, 10, 8)
    print(f"   Rolls: {result.results}")
    print(f"   Successes (8+): {result.successes}")
    print(f"   Dramatic failures (1s): {result.ones}")
    print(f"   Net successes: {result.net_successes}")


def example_complex_rolls():
    """Complex dice notation examples."""
    print("\n" + "=" * 50)
    print("Complex Rolls")
    print("=" * 50)
    
    examples = [
        "2d20kh1+5",      # Roll 2d20, keep highest 1, add 5
        "8d6dl2",         # Roll 8d6, drop lowest 2
        "4d20kh2",        # Roll 4d20, keep highest 2
        "3d10+2",         # Roll 3d10, add 2
        "6d6>=4",         # Roll 6d6, count successes
        "5d8r1",          # Roll 5d8, reroll 1s once
        "2d12!",          # Roll 2d12 exploding
    ]
    
    print("\nComplex notation examples:")
    for notation in examples:
        outcome = dice_parse(notation)
        print(f"\n   {notation}:")
        print(f"      Rolls: {outcome.rolls}")
        print(f"      Kept: {outcome.kept}")
        print(f"      Modifier: {outcome.modifier}")
        print(f"      Total: {outcome.total}")


if __name__ == "__main__":
    example_basic_rolling()
    example_dice_notation()
    example_convenience_function()
    example_advantage_disadvantage()
    example_fudge_dice()
    example_statistics()
    example_batch_rolling()
    example_weighted_dice()
    example_dice_pools()
    example_complex_rolls()
    
    print("\n" + "=" * 50)
    print("All examples completed!")
    print("=" * 50)