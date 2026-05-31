#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AllToolkit - Dice Utils Test Suite
===================================
Test cases for dice utilities module.
"""

import unittest
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mod import (
    roll, roll_with_reroll, roll_exploding, roll_fudge,
    dice_roll, dice_parse,
    fudge_total, advantage, disadvantage,
    roll_distribution, expected_value, variance, standard_deviation,
    probability_at_least, probability_exactly,
    batch_roll, batch_stats,
    roll_weighted, roll_weighted_batch,
    roll_pool, RollOutcome, RollStats, DicePoolResult
)


class TestCoreRolls(unittest.TestCase):
    """Test core rolling functions."""
    
    def test_roll_basic(self):
        """Test basic roll function."""
        result = roll(2, 6)
        self.assertEqual(len(result), 2)
        for r in result:
            self.assertGreaterEqual(r, 1)
            self.assertLessEqual(r, 6)
    
    def test_roll_single_die(self):
        """Test rolling single die."""
        result = roll(1, 20)
        self.assertEqual(len(result), 1)
        self.assertGreaterEqual(result[0], 1)
        self.assertLessEqual(result[0], 20)
    
    def test_roll_invalid_dice_count(self):
        """Test rolling invalid dice count."""
        result = roll(0, 6)
        self.assertEqual(result, [])
    
    def test_roll_too_many_dice(self):
        """Test rolling too many dice raises error."""
        with self.assertRaises(ValueError):
            roll(1001, 6)
    
    def test_roll_invalid_sides(self):
        """Test rolling invalid sides raises error."""
        with self.assertRaises(ValueError):
            roll(2, 0)


class TestRerollMechanics(unittest.TestCase):
    """Test reroll mechanics."""
    
    def test_reroll_basic(self):
        """Test basic reroll."""
        result = roll_with_reroll(5, 6, 2, max_rerolls=1)
        self.assertEqual(len(result), 5)
        for r in result:
            self.assertGreaterEqual(r, 1)
            self.assertLessEqual(r, 6)
            # No 1s or 2s after reroll
            self.assertGreater(r, 2)
    
    def test_reroll_multiple(self):
        """Test multiple reroll passes."""
        # With 3 reroll passes, all low rolls should be gone
        result = roll_with_reroll(10, 6, 3, max_rerolls=3)
        self.assertEqual(len(result), 10)
        for r in result:
            self.assertGreaterEqual(r, 4)  # Should be 4, 5, or 6


class TestExplodingDice(unittest.TestCase):
    """Test exploding dice mechanics."""
    
    def test_exploding_returns_list(self):
        """Test exploding dice returns a list."""
        result = roll_exploding(3, 6)
        self.assertIsInstance(result, list)
        self.assertGreaterEqual(len(result), 3)  # May or may not have explosions
    
    def test_exploding_values(self):
        """Test exploding dice values are valid."""
        result = roll_exploding(5, 6)
        for r in result:
            self.assertGreaterEqual(r, 1)
            self.assertLessEqual(r, 6)


class TestFudgeDice(unittest.TestCase):
    """Test Fudge/FATE dice."""
    
    def test_fudge_values(self):
        """Test Fudge dice return -1, 0, or 1."""
        result = roll_fudge(4)
        self.assertEqual(len(result), 4)
        for r in result:
            self.assertIn(r, [-1, 0, 1])
    
    def test_fudge_total(self):
        """Test Fudge total is within expected range."""
        total = fudge_total(4)
        self.assertIsInstance(total, int)
        self.assertGreaterEqual(total, -4)
        self.assertLessEqual(total, 4)


class TestDiceNotation(unittest.TestCase):
    """Test dice notation parser."""
    
    def test_simple_roll(self):
        """Test simple XdY notation."""
        outcome = dice_parse("2d6")
        self.assertEqual(len(outcome.rolls), 2)
        for r in outcome.rolls:
            self.assertGreaterEqual(r, 1)
            self.assertLessEqual(r, 6)
    
    def test_roll_with_modifier(self):
        """Test roll with modifier."""
        outcome = dice_parse("2d6+3")
        self.assertEqual(outcome.modifier, 3)
        self.assertEqual(outcome.total, sum(outcome.rolls) + 3)
    
    def test_roll_with_negative_modifier(self):
        """Test roll with negative modifier."""
        outcome = dice_parse("3d8-2")
        self.assertEqual(outcome.modifier, -2)
        self.assertEqual(outcome.total, sum(outcome.rolls) - 2)
    
    def test_keep_highest(self):
        """Test keep highest (kh)."""
        outcome = dice_parse("4d20kh3")
        self.assertEqual(len(outcome.kept), 3)
        self.assertEqual(len(outcome.dropped), 1)
    
    def test_keep_lowest(self):
        """Test keep lowest (kl)."""
        outcome = dice_parse("4d20kl2")
        self.assertEqual(len(outcome.kept), 2)
        self.assertEqual(len(outcome.dropped), 2)
    
    def test_drop_highest(self):
        """Test drop highest (dh)."""
        outcome = dice_parse("4d6dh1")
        self.assertEqual(len(outcome.kept), 3)
        self.assertEqual(len(outcome.dropped), 1)
    
    def test_drop_lowest(self):
        """Test drop lowest (dl)."""
        outcome = dice_parse("4d6dl1")
        self.assertEqual(len(outcome.kept), 3)
        self.assertEqual(len(outcome.dropped), 1)
    
    def test_exploding_notation(self):
        """Test exploding dice notation (!)."""
        outcome = dice_parse("2d6!")
        # Just check it doesn't error and returns something
        self.assertIsInstance(outcome.rolls, list)
    
    def test_reroll_notation(self):
        """Test reroll notation (rN)."""
        outcome = dice_parse("5d6r2")
        self.assertEqual(len(outcome.rolls), 5)
        # No values should be 1 or 2 after reroll
        for r in outcome.rolls:
            self.assertGreater(r, 2)
    
    def test_target_greater(self):
        """Test target number (>N)."""
        outcome = dice_parse("6d6>4")
        self.assertEqual(outcome.success_count + outcome.failure_count, 6)
    
    def test_target_greater_equal(self):
        """Test target number inclusive (>=N)."""
        outcome = dice_parse("6d6>=4")
        self.assertGreaterEqual(outcome.success_count + outcome.failure_count, 6)
    
    def test_invalid_notation(self):
        """Test invalid notation raises error."""
        with self.assertRaises(ValueError):
            dice_parse("invalid")
    
    def test_dice_roll_convenience(self):
        """Test dice_roll convenience function returns int."""
        result = dice_roll("d20+5")
        self.assertIsInstance(result, int)
        self.assertGreaterEqual(result, 6)  # min d20 + 5
        self.assertLessEqual(result, 25)  # max d20 + 5


class TestAdvantageDisadvantage(unittest.TestCase):
    """Test advantage and disadvantage rolls."""
    
    def test_advantage_returns_tuple(self):
        """Test advantage returns tuple of 3 values."""
        result = advantage()
        self.assertEqual(len(result), 3)
        r1, r2, final = result
        self.assertEqual(final, max(r1, r2))
    
    def test_disadvantage_returns_tuple(self):
        """Test disadvantage returns tuple of 3 values."""
        result = disadvantage()
        self.assertEqual(len(result), 3)
        r1, r2, final = result
        self.assertEqual(final, min(r1, r2))


class TestStatistics(unittest.TestCase):
    """Test statistical functions."""
    
    def test_expected_value(self):
        """Test expected value calculation."""
        ev = expected_value(2, 6)
        self.assertEqual(ev, 7.0)
    
    def test_variance(self):
        """Test variance calculation."""
        var = variance(1, 6)
        self.assertAlmostEqual(var, 35/12, places=3)
    
    def test_standard_deviation(self):
        """Test standard deviation calculation."""
        sd = standard_deviation(2, 6)
        expected = (35/6) ** 0.5
        self.assertAlmostEqual(sd, expected, places=3)
    
    def test_distribution_sums_to_one(self):
        """Test distribution probabilities sum to 1."""
        dist = roll_distribution(2, 6, trials=5000)
        total = sum(dist.values())
        self.assertAlmostEqual(total, 1.0, places=1)


class TestBatchRolling(unittest.TestCase):
    """Test batch rolling functions."""
    
    def test_batch_roll_returns_list(self):
        """Test batch_roll returns list of outcomes."""
        results = batch_roll("2d6", 10)
        self.assertEqual(len(results), 10)
        for r in results:
            self.assertIsInstance(r, RollOutcome)
    
    def test_batch_stats(self):
        """Test batch_stats returns stats object."""
        stats = batch_stats("d20", 100)
        self.assertIsInstance(stats, RollStats)
        self.assertEqual(stats.count, 100)
        self.assertGreater(stats.mean, 0)


class TestWeightedDice(unittest.TestCase):
    """Test weighted dice functions."""
    
    def test_weighted_basic(self):
        """Test basic weighted roll."""
        weights = [0.1] * 5 + [0.5]  # 6 sides, sum to 1
        result = roll_weighted(6, weights)
        self.assertGreaterEqual(result, 1)
        self.assertLessEqual(result, 6)
    
    def test_weighted_batch(self):
        """Test weighted batch roll."""
        weights = [0.2] * 5
        results = roll_weighted_batch(10, 5, weights)
        self.assertEqual(len(results), 10)
        for r in results:
            self.assertGreaterEqual(r, 1)
            self.assertLessEqual(r, 5)


class TestDicePools(unittest.TestCase):
    """Test dice pool functions."""
    
    def test_pool_result(self):
        """Test dice pool result."""
        result = roll_pool(8, 10, 8)
        self.assertIsInstance(result, DicePoolResult)
        self.assertEqual(len(result.results), 8)
        self.assertGreaterEqual(result.successes, 0)
        self.assertLessEqual(result.successes, 8)
    
    def test_pool_net_successes(self):
        """Test net successes calculation."""
        result = roll_pool(10, 10, 8)
        # Note: net_successes can be negative if many 1s
        self.assertEqual(result.net_successes, result.successes - result.ones)


class TestRollOutcome(unittest.TestCase):
    """Test RollOutcome dataclass."""
    
    def test_total_property(self):
        """Test total property."""
        outcome = RollOutcome(
            notation="2d6+3",
            rolls=[3, 5],
            kept=[3, 5],
            dropped=[],
            modifier=3
        )
        self.assertEqual(outcome.total, 11)
    
    def test_success_rate(self):
        """Test success rate calculation."""
        outcome = RollOutcome(
            notation="6d6>=4",
            rolls=[3, 4, 5, 2, 6, 4],
            kept=[4, 5, 6, 4],
            dropped=[3, 2],
            modifier=0,
            success_count=4,
            failure_count=2
        )
        self.assertAlmostEqual(outcome.success_rate, 66.67, places=2)


if __name__ == '__main__':
    unittest.main(verbosity=2)