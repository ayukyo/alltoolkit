"""
AllToolkit - Dice Utilities Probability Example

Demonstrates probability calculations for dice outcomes.
"""

import sys
sys.path.insert(0, '/home/admin/.openclaw/workspace/AllToolkit/Python')

from dice_utils import mod as dice


def main():
    print("=" * 60)
    print("Dice Utilities - Probability Example")
    print("=" * 60)
    print()
    
    # Expected values
    print("Expected Values:")
    print(f"  E[1d6] = {dice.expected_value(1, 6)}")
    print(f"  E[2d6] = {dice.expected_value(2, 6)}")
    print(f"  E[3d6] = {dice.expected_value(3, 6)}")
    print(f"  E[1d20] = {dice.expected_value(1, 20)}")
    print(f"  E[1d100] = {dice.expected_value(1, 100)}")
    print()
    
    # Variance and standard deviation
    print("Variance and Standard Deviation:")
    print(f"  Var[1d6] = {dice.variance(1, 6):.3f}")
    print(f"  SD[1d6] = {dice.standard_deviation(1, 6):.3f}")
    print(f"  Var[2d6] = {dice.variance(2, 6):.3f}")
    print(f"  SD[2d6] = {dice.standard_deviation(2, 6):.3f}")
    print()
    
    # Probability distribution for 2d6
    print("2d6 Probability Distribution:")
    dist = dice.dice_probability(2, 6)
    print(f"  Mean: {dist.mean}")
    print(f"  Variance: {dist.variance:.3f}")
    print(f"  Standard Deviation: {dist.std_dev:.3f}")
    print(f"  Min: {dist.min_value}, Max: {dist.max_value}")
    print()
    print("  Outcome probabilities:")
    for outcome in sorted(dist.outcomes.keys()):
        prob = dist.outcomes[outcome]
        bar_length = int(prob * 60)
        bar = "█" * bar_length
        print(f"    {outcome:2d}: {prob:.4f} {bar}")
    print()
    
    # Specific probabilities
    print("Specific Probabilities:")
    print(f"  P(7 on 2d6) = {dice.dice_probability(2, 6).probability(7):.4f}")
    print(f"  P(2 on 2d6) = {dice.dice_probability(2, 6).probability(2):.4f}")
    print(f"  P(12 on 2d6) = {dice.dice_probability(2, 6).probability(12):.4f}")
    print()
    
    # Cumulative probabilities
    print("Cumulative Probabilities (2d6):")
    print(f"  P(X >= 7) = {dice.probability_at_least(2, 6, 7):.4f}")
    print(f"  P(X >= 10) = {dice.probability_at_least(2, 6, 10):.4f}")
    print(f"  P(X <= 7) = {dice.probability_at_most(2, 6, 7):.4f}")
    print(f"  P(X <= 4) = {dice.probability_at_most(2, 6, 4):.4f}")
    print(f"  P(5 <= X <= 9) = {dice.probability_between(2, 6, 5, 9):.4f}")
    print()
    
    # Distribution for 3d6
    print("3d6 Distribution:")
    dist3d6 = dice.dice_probability(3, 6)
    print(f"  Mean: {dist3d6.mean}")
    print(f"  SD: {dist3d6.std_dev:.3f}")
    print(f"  P(X >= 15) = {dist3d6.probability_at_least(15):.4f}")
    print(f"  P(X <= 10) = {dist3d6.probability_at_most(10):.4f}")
    print()
    
    # Distribution comparison
    print("Comparing 2d6 vs 1d12:")
    print("  Both have E[X] = 7, but different distributions:")
    dist2d6 = dice.dice_probability(2, 6)
    dist1d12 = dice.dice_probability(1, 12)
    
    print(f"    2d6: mean={dist2d6.mean}, sd={dist2d6.std_dev:.3f}")
    print(f"    1d12: mean={dist1d12.mean}, sd={dist1d12.std_dev:.3f}")
    
    print()
    print("  2d6 is bell-shaped (concentrated around mean)")
    print("  1d12 is uniform (equal probability for each outcome)")
    print()
    
    # Monte Carlo simulation
    print("Monte Carlo Simulation (2d6):")
    stats = dice.monte_carlo_simulation("2d6", iterations=10000)
    print(f"  Simulated mean: {stats['mean']:.3f} (expected: 7.0)")
    print(f"  Simulated std_dev: {stats['std_dev']:.3f}")
    print(f"  Observed range: {stats['min']} to {stats['max']}")
    print()


if __name__ == "__main__":
    main()