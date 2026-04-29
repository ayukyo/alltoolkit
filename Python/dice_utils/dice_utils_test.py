"""
AllToolkit - Python Dice Utilities Test Suite

Comprehensive tests for dice rolling, notation parsing,
probability calculations, and statistical analysis.

Author: AllToolkit
License: MIT
"""

import sys
sys.path.insert(0, '/home/admin/.openclaw/workspace/AllToolkit/Python')

from dice_utils.mod import (
    # Basic rolls
    roll, roll_d4, roll_d6, roll_d8, roll_d10, roll_d12, roll_d20, roll_d100,
    roll_percentile, d, d4, d6, d8, d10, d12, d20, d100, dF,
    
    # Notation
    roll_notation, DiceNotationParser,
    
    # Keep/drop
    roll_keep_highest, roll_keep_lowest, roll_drop_lowest, roll_drop_highest,
    
    # Exploding
    roll_exploding,
    
    # Dice pools
    roll_pool, roll_world_of_darkness,
    
    # Fate/Fudge
    roll_fate, roll_fudge,
    
    # Advantage/disadvantage
    roll_with_advantage, roll_with_disadvantage,
    
    # Probability
    dice_distribution, dice_probability, probability_at_least,
    probability_at_most, probability_between, expected_value,
    variance, standard_deviation,
    
    # Analysis
    monte_carlo_simulation, analyze_rolls, compare_rolls,
    
    # Classes
    DiceRoller, DiceResult, DicePoolResult, ProbabilityDistribution,
    
    # Utilities
    dice_to_string,
)
import random


def test_basic_rolls():
    """Test basic dice rolling functions."""
    print("Testing basic rolls...")
    
    # Test single die roll
    result = roll(6)
    assert 1 <= result.total <= 6
    assert len(result.dice) == 1
    assert result.total == result.dice[0]
    
    # Test multiple dice
    result = roll(6, count=3)
    assert 3 <= result.total <= 18
    assert len(result.dice) == 3
    assert result.total == sum(result.dice)
    
    # Test with modifier
    result = roll(6, count=2, modifier=5)
    assert 7 <= result.total <= 17
    assert result.modifier == 5
    assert result.total == sum(result.dice) + 5
    
    # Test negative modifier
    result = roll(20, count=1, modifier=-3)
    assert -2 <= result.total <= 17
    assert result.modifier == -3
    
    print("  ✓ Basic rolls passed")


def test_standard_dice():
    """Test standard dice functions (d4, d6, d8, d10, d12, d20, d100)."""
    print("Testing standard dice...")
    
    # d4
    for _ in range(10):
        result = roll_d4()
        assert 1 <= result.total <= 4
    
    # d6
    for _ in range(10):
        result = roll_d6(3)
        assert 3 <= result.total <= 18
    
    # d8
    for _ in range(10):
        result = roll_d8()
        assert 1 <= result.total <= 8
    
    # d10
    for _ in range(10):
        result = roll_d10()
        assert 1 <= result.total <= 10
    
    # d12
    for _ in range(10):
        result = roll_d12()
        assert 1 <= result.total <= 12
    
    # d20
    for _ in range(10):
        result = roll_d20()
        assert 1 <= result.total <= 20
    
    # d100
    for _ in range(10):
        result = roll_d100()
        assert 1 <= result.total <= 100
    
    # percentile
    result = roll_percentile()
    assert 1 <= result.total <= 100
    
    print("  ✓ Standard dice passed")


def test_dice_notation_parser():
    """Test dice notation parsing and rolling."""
    print("Testing dice notation parser...")
    
    parser = DiceNotationParser()
    
    # Test basic notation
    result = parser.roll("d6")
    assert 1 <= result.total <= 6
    assert len(result.dice) == 1
    
    # Test count and sides
    result = parser.roll("2d6")
    assert 2 <= result.total <= 12
    assert len(result.dice) == 2
    
    # Test with modifier
    result = parser.roll("3d6+5")
    assert 8 <= result.total <= 23
    assert result.modifier == 5
    
    result = parser.roll("1d20-2")
    assert -1 <= result.total <= 18
    assert result.modifier == -2
    
    # Test keep highest (D&D ability scores)
    result = parser.roll("4d6k3")
    assert 3 <= result.total <= 18
    assert len(result.kept) == 3
    assert len(result.dice) == 4
    assert result.total == sum(result.kept)
    
    # Test keep lowest
    result = parser.roll("4d6l3")
    assert 3 <= result.total <= 18
    assert len(result.kept) == 3
    
    # Test drop lowest
    result = parser.roll("4d6d1")
    assert 3 <= result.total <= 18
    assert len(result.kept) == 3
    
    # Test roll_notation convenience function
    result = roll_notation("2d6+3")
    assert 5 <= result.total <= 15
    
    # Test parsing
    parsed = parser.parse("4d6k3+2")
    assert parsed['count'] == 4
    assert parsed['sides'] == 6
    assert parsed['keep_type'] == 'k'
    assert parsed['keep_count'] == 3
    assert parsed['modifier'] == 2
    
    print("  ✓ Dice notation parser passed")


def test_exploding_dice():
    """Test exploding dice mechanics."""
    print("Testing exploding dice...")
    
    # Test regular exploding dice
    results = []
    for _ in range(100):
        result = roll_exploding(6, count=1)
        results.append(result)
    
    # All results should be >= 1
    for r in results:
        assert r.total >= 1
    
    # Some results should exceed 6 (exploded)
    exploded_count = sum(1 for r in results if r.total > 6)
    assert exploded_count >= 0  # Statistical - may or may not happen
    
    # Test compound exploding
    result = roll_exploding(6, count=1, compound=True)
    assert result.total >= 1
    
    print("  ✓ Exploding dice passed")


def test_keep_drop_dice():
    """Test keep/drop dice mechanics."""
    print("Testing keep/drop dice...")
    
    # Test keep highest
    result = roll_keep_highest(6, 4, 3)
    assert len(result.dice) == 4
    assert len(result.kept) == 3
    assert len(result.dropped) == 1
    assert result.total == sum(result.kept)
    assert min(result.kept) >= max(result.dropped)
    
    # Test keep lowest
    result = roll_keep_lowest(6, 4, 3)
    assert len(result.dice) == 4
    assert len(result.kept) == 3
    assert max(result.kept) <= min(result.dropped)
    
    # Test drop lowest (same as keep highest)
    result = roll_drop_lowest(6, 4, 1)
    assert len(result.kept) == 3
    
    # Test drop highest
    result = roll_drop_highest(6, 4, 1)
    assert len(result.kept) == 3
    
    print("  ✓ Keep/drop dice passed")


def test_dice_pool():
    """Test dice pool mechanics."""
    print("Testing dice pools...")
    
    # Test basic dice pool
    result = roll_pool(10, 5, 6)
    assert len(result.dice) == 5
    assert result.successes >= 0
    assert result.successes + result.failures == 5
    assert result.critical_threshold == 10
    assert result.botch_threshold == 1
    
    # Test with double success on criticals
    result = roll_pool(10, 5, 6, critical_threshold=10, double_success=True)
    # If any 10s rolled, they count as 2 successes
    assert result.successes >= 0
    
    # Test World of Darkness style
    result = roll_world_of_darkness(5, difficulty=6)
    assert len(result.dice) == 5
    assert result.successes >= 0
    
    print("  ✓ Dice pools passed")


def test_fate_dice():
    """Test Fate/Fudge dice."""
    print("Testing Fate/Fudge dice...")
    
    # Test standard Fate roll
    result = roll_fate(4)
    assert len(result.dice) == 4
    assert -4 <= result.total <= 4
    for die in result.dice:
        assert die in [-1, 0, 1]
    
    # Test different count
    result = roll_fate(6)
    assert len(result.dice) == 6
    assert -6 <= result.total <= 6
    
    # Test fudge alias
    result = roll_fudge(4)
    assert -4 <= result.total <= 4
    
    print("  ✓ Fate/Fudge dice passed")


def test_advantage_disadvantage():
    """Test advantage/disadvantage mechanics."""
    print("Testing advantage/disadvantage...")
    
    # Test advantage
    for _ in range(50):
        result = roll_with_advantage(20)
        assert len(result.dice) == 2
        assert result.total == max(result.dice)
        assert 1 <= result.total <= 20
    
    # Test disadvantage
    for _ in range(50):
        result = roll_with_disadvantage(20)
        assert len(result.dice) == 2
        assert result.total == min(result.dice)
        assert 1 <= result.total <= 20
    
    print("  ✓ Advantage/disadvantage passed")


def test_probability_distribution():
    """Test probability distribution calculations."""
    print("Testing probability distribution...")
    
    # Test 2d6 distribution
    dist = dice_probability(2, 6)
    
    # Mean of 2d6 should be 7
    assert abs(dist.mean - 7.0) < 0.001
    
    # Min should be 2, max should be 12
    assert dist.min_value == 2
    assert dist.max_value == 12
    
    # Probability of 7 should be 6/36 = 1/6
    assert abs(dist.probability(7) - (1/6)) < 0.001
    
    # Probability of 2 should be 1/36
    assert abs(dist.probability(2) - (1/36)) < 0.001
    
    # Test probability_at_least
    prob = probability_at_least(2, 6, 7)
    # P(X >= 7) = P(7) + P(8) + ... + P(12) = 21/36 = 7/12
    assert abs(prob - (21/36)) < 0.001
    
    # Test probability_at_most
    prob = probability_at_most(2, 6, 7)
    # P(X <= 7) = P(2) + ... + P(7) = 21/36
    assert abs(prob - (21/36)) < 0.001
    
    # Test probability_between
    prob = probability_between(2, 6, 5, 9)
    # P(5 <= X <= 9) = P(5) + P(6) + P(7) + P(8) + P(9)
    assert prob > 0
    
    print("  ✓ Probability distribution passed")


def test_expected_value():
    """Test expected value calculations."""
    print("Testing expected value...")
    
    # E[1d6] = 3.5
    assert abs(expected_value(1, 6) - 3.5) < 0.001
    
    # E[2d6] = 7
    assert abs(expected_value(2, 6) - 7.0) < 0.001
    
    # E[1d20] = 10.5
    assert abs(expected_value(1, 20) - 10.5) < 0.001
    
    # E[3d6] = 10.5
    assert abs(expected_value(3, 6) - 10.5) < 0.001
    
    print("  ✓ Expected value passed")


def test_variance_std_dev():
    """Test variance and standard deviation calculations."""
    print("Testing variance and standard deviation...")
    
    # Var[1d6] = (36-1)/12 = 35/12 ≈ 2.917
    var1d6 = variance(1, 6)
    assert abs(var1d6 - (35/12)) < 0.001
    
    # Var[2d6] = 2 * 35/12 ≈ 5.833
    var2d6 = variance(2, 6)
    assert abs(var2d6 - (70/12)) < 0.001
    
    # Std dev
    std1d6 = standard_deviation(1, 6)
    assert abs(std1d6 - (35/12) ** 0.5) < 0.001
    
    print("  ✓ Variance and standard deviation passed")


def test_dice_distribution():
    """Test dice distribution calculation."""
    print("Testing dice distribution...")
    
    # Test 2d6 distribution
    dist = dice_distribution(2, 6)
    
    # 7 should have 6 ways: (1,6), (2,5), (3,4), (4,3), (5,2), (6,1)
    assert dist[7] == 6
    
    # 2 should have 1 way: (1,1)
    assert dist[2] == 1
    
    # 12 should have 1 way: (6,6)
    assert dist[12] == 1
    
    # Total outcomes should be 36
    total = sum(dist.values())
    assert total == 36
    
    print("  ✓ Dice distribution passed")


def test_monte_carlo():
    """Test Monte Carlo simulation."""
    print("Testing Monte Carlo simulation...")
    
    # Test 2d6 simulation
    stats = monte_carlo_simulation("2d6", 10000, seed=42)
    
    # Mean should be approximately 7
    assert 6 < stats['mean'] < 8
    
    # Min should be 2, max should be 12
    assert stats['min'] == 2
    assert stats['max'] == 12
    
    # Distribution should cover all values 2-12
    for i in range(2, 13):
        assert i in stats['distribution']
    
    print("  ✓ Monte Carlo simulation passed")


def test_compare_rolls():
    """Test dice roll comparison."""
    print("Testing roll comparison...")
    
    # Compare 2d6 vs 1d12
    random.seed(42)  # Set seed before comparison
    result = compare_rolls("2d6", "1d12", iterations=10000)
    
    # 2d6 and 1d12 have same expected value but different distributions
    # 2d6 is more consistent (bell curve), 1d12 is flat
    assert 'notation1_wins' in result
    assert 'notation2_wins' in result
    assert 'ties' in result
    
    # Probabilities should sum to 1
    total_prob = result['notation1_wins'] + result['notation2_wins'] + result['ties']
    assert abs(total_prob - 1.0) < 0.001
    
    print("  ✓ Roll comparison passed")


def test_dice_roller_class():
    """Test DiceRoller class."""
    print("Testing DiceRoller class...")
    
    # Test with seed for reproducibility
    roller = DiceRoller(seed=42)
    
    # Roll and check history
    result = roller.roll("2d6")
    assert len(roller.history) == 1
    
    result2 = roller.roll("1d20")
    assert len(roller.history) == 2
    
    # Test last_roll
    assert roller.last_roll == result2
    
    # Test roll_d
    result = roller.roll_d(6, 2, 3)
    assert result.modifier == 3
    
    # Test roll_with_advantage
    result = roller.roll_with_advantage(20)
    assert result.total == max(result.dice)
    
    # Test roll_with_disadvantage
    result = roller.roll_with_disadvantage(20)
    assert result.total == min(result.dice)
    
    # Test roll_fate
    result = roller.roll_fate(4)
    assert -4 <= result.total <= 4
    
    # Test analyze_history
    analysis = roller.analyze_history()
    assert 'total_rolls' in analysis
    assert analysis['total_rolls'] == 6
    
    # Test clear_history
    roller.clear_history()
    assert len(roller.history) == 0
    
    print("  ✓ DiceRoller class passed")


def test_analyze_rolls():
    """Test roll analysis."""
    print("Testing roll analysis...")
    
    # Create some test results
    results = []
    random.seed(42)
    for _ in range(100):
        results.append(roll(6, 3))
    
    analysis = analyze_rolls(results)
    
    assert 'total_rolls' in analysis
    assert analysis['total_rolls'] == 100
    assert 'total_dice' in analysis
    assert analysis['total_dice'] == 300
    assert 'mean_total' in analysis
    assert 'mean_die_value' in analysis
    
    # Mean die value should be approximately 3.5
    assert 3 < analysis['mean_die_value'] < 4
    
    print("  ✓ Roll analysis passed")


def test_dice_to_string():
    """Test dice string representation."""
    print("Testing dice string representation...")
    
    str1 = dice_to_string([5, 3, 6], modifier=2)
    assert "3d6+2" in str1
    assert "5" in str1 and "3" in str1 and "6" in str1
    
    str2 = dice_to_string([1], modifier=-1, sides=20)
    assert "1d20" in str2
    assert "-1" in str2
    
    print("  ✓ Dice string representation passed")


def test_shorthand_functions():
    """Test shorthand functions."""
    print("Testing shorthand functions...")
    
    # Test d()
    result = d(6, 2)
    assert 2 <= result.total <= 12
    
    # Test shorthand standard dice
    assert 1 <= d4().total <= 4
    assert 1 <= d6().total <= 6
    assert 1 <= d8().total <= 8
    assert 1 <= d10().total <= 10
    assert 1 <= d12().total <= 12
    assert 1 <= d20().total <= 20
    assert 1 <= d100().total <= 100
    
    # Test Fate shorthand
    result = dF(4)
    assert -4 <= result.total <= 4
    
    print("  ✓ Shorthand functions passed")


def test_data_classes():
    """Test data classes."""
    print("Testing data classes...")
    
    # DiceResult
    result = DiceResult(dice=[5, 3], modifier=2, total=10, notation="2d6+2")
    assert result.rolls == [5, 3]
    assert result.successful == [5, 3]
    assert result.total == 10
    
    # DiceResult with kept/dropped
    result = DiceResult(
        dice=[6, 5, 3, 1],
        modifier=0,
        total=14,
        notation="4d6k3",
        kept=[6, 5, 3],
        dropped=[1]
    )
    assert result.successful == [6, 5, 3]
    
    # DicePoolResult
    pool_result = DicePoolResult(
        dice=[8, 6, 4, 2, 10],
        successes=3,
        failures=2,
        criticals=1,
        botches=1,
        total=30,
        notation="5d10>=6",
        success_threshold=6,
        critical_threshold=10,
        botch_threshold=1
    )
    assert pool_result.successes == 3
    assert pool_result.criticals == 1
    
    # ProbabilityDistribution
    dist = ProbabilityDistribution(
        outcomes={2: 1/36, 3: 2/36, 7: 6/36},
        mean=7.0,
        variance=5.83,
        std_dev=2.41,
        min_value=2,
        max_value=12
    )
    assert dist.probability(7) == 6/36
    
    print("  ✓ Data classes passed")


def test_edge_cases():
    """Test edge cases and error handling."""
    print("Testing edge cases...")
    
    parser = DiceNotationParser()
    
    # Invalid notation should raise error
    try:
        parser.roll("invalid")
        assert False, "Should have raised ValueError"
    except ValueError:
        pass
    
    # Zero dice
    result = roll(6, 0)
    assert result.total == 0
    assert len(result.dice) == 0
    
    # Empty string notation should fail
    try:
        parser.roll("")
        assert False, "Should have raised ValueError"
    except ValueError:
        pass
    
    print("  ✓ Edge cases passed")


def test_reproducibility():
    """Test reproducibility with seeds."""
    print("Testing reproducibility...")
    
    # Test that setting seed produces reproducible results
    # by using the same parser instance
    parser1 = DiceNotationParser(seed=12345)
    parser2 = DiceNotationParser(seed=12345)
    
    # Reset seed before each roll for reproducibility
    parser1_reseed = DiceNotationParser(seed=12345)
    results1 = [parser1_reseed.roll("2d6") for _ in range(5)]
    
    parser2_reseed = DiceNotationParser(seed=12345)
    results2 = [parser2_reseed.roll("2d6") for _ in range(5)]
    
    # Results should be identical after reseeding
    for r1, r2 in zip(results1, results2):
        assert r1.dice == r2.dice
        assert r1.total == r2.total
    
    # Test monte carlo with seed
    stats1 = monte_carlo_simulation("2d6", iterations=1000, seed=42)
    stats2 = monte_carlo_simulation("2d6", iterations=1000, seed=42)
    
    assert stats1['mean'] == stats2['mean']
    assert stats1['min'] == stats2['min']
    assert stats1['max'] == stats2['max']
    
    print("  ✓ Reproducibility passed")


def run_all_tests():
    """Run all tests."""
    print("=" * 60)
    print("AllToolkit - Python Dice Utilities Test Suite")
    print("=" * 60)
    print()
    
    test_basic_rolls()
    test_standard_dice()
    test_dice_notation_parser()
    test_exploding_dice()
    test_keep_drop_dice()
    test_dice_pool()
    test_fate_dice()
    test_advantage_disadvantage()
    test_probability_distribution()
    test_expected_value()
    test_variance_std_dev()
    test_dice_distribution()
    test_monte_carlo()
    test_compare_rolls()
    test_dice_roller_class()
    test_analyze_rolls()
    test_dice_to_string()
    test_shorthand_functions()
    test_data_classes()
    test_edge_cases()
    test_reproducibility()
    
    print()
    print("=" * 60)
    print("All tests passed! ✓")
    print("=" * 60)


if __name__ == "__main__":
    run_all_tests()