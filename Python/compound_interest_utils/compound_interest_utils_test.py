"""
AllToolkit - Compound Interest Utilities Test Suite

Comprehensive tests for compound interest calculations.
Zero external dependencies - uses only Python standard library.

Author: AllToolkit
License: MIT
"""

import sys
import os
import math
import unittest

# Add parent directory to path for module import
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from compound_interest_utils.mod import (
    # Exceptions
    CompoundInterestError, InvalidPrincipalError, InvalidRateError,
    InvalidTimeError, InvalidFrequencyError,
    
    # Basic calculations
    compound_amount, compound_interest,
    continuous_compound_amount, continuous_compound_interest,
    
    # Rate conversions
    effective_annual_rate, nominal_rate_from_ear, equivalent_rate,
    annual_percentage_yield,
    
    # Doubling time
    doubling_time, doubling_time_rule72, doubling_time_rule69,
    tripling_time, quadrupling_time, time_to_reach_target,
    
    # Required calculations
    required_rate, required_principal,
    
    # Schedules
    compound_schedule, annual_compound_schedule,
    
    # Contributions
    future_value_with_contributions, required_contribution,
    
    # Inflation
    real_rate, inflation_adjusted_amount, purchasing_power,
    
    # Comparisons
    compare_compounding_frequencies, compare_rates,
    
    # Helpers
    investment_summary, savings_goal_analysis, compound_interest_table,
    get_compounding_frequency, COMPOUNDING_FREQUENCIES
)


class TestBasicCalculations(unittest.TestCase):
    """Test basic compound interest calculations."""
    
    def test_compound_amount_basic(self):
        """Test basic compound amount calculation."""
        # $1000 at 5% for 10 years, monthly compounding
        result = compound_amount(1000, 0.05, 10, 12)
        expected = 1000 * (1 + 0.05/12) ** (12*10)
        self.assertAlmostEqual(result, expected, places=6)
        self.assertAlmostEqual(result, 1647.01, places=2)
    
    def test_compound_amount_annual(self):
        """Test annual compounding."""
        result = compound_amount(1000, 0.05, 10, 1)
        expected = 1000 * 1.05 ** 10
        self.assertAlmostEqual(result, expected, places=6)
        self.assertAlmostEqual(result, 1628.89, places=2)
    
    def test_compound_amount_zero_rate(self):
        """Test zero interest rate."""
        result = compound_amount(1000, 0, 10, 12)
        self.assertEqual(result, 1000)
    
    def test_compound_amount_zero_time(self):
        """Test zero time period."""
        result = compound_amount(1000, 0.05, 0, 12)
        self.assertEqual(result, 1000)
    
    def test_compound_amount_negative_principal(self):
        """Test negative principal raises error."""
        with self.assertRaises(InvalidPrincipalError):
            compound_amount(-1000, 0.05, 10, 12)
    
    def test_compound_amount_invalid_rate(self):
        """Test rate below -100% raises error."""
        with self.assertRaises(InvalidRateError):
            compound_amount(1000, -1.5, 10, 12)
    
    def test_compound_interest(self):
        """Test interest calculation."""
        result = compound_interest(1000, 0.05, 10, 12)
        amount = compound_amount(1000, 0.05, 10, 12)
        self.assertAlmostEqual(result, amount - 1000, places=6)
        self.assertAlmostEqual(result, 647.01, places=2)
    
    def test_continuous_compound_amount(self):
        """Test continuous compounding."""
        result = continuous_compound_amount(1000, 0.05, 10)
        expected = 1000 * math.exp(0.05 * 10)
        self.assertAlmostEqual(result, expected, places=6)
        self.assertAlmostEqual(result, 1648.72, places=2)
    
    def test_continuous_compound_interest(self):
        """Test continuous compound interest."""
        result = continuous_compound_interest(1000, 0.05, 10)
        amount = continuous_compound_amount(1000, 0.05, 10)
        self.assertAlmostEqual(result, amount - 1000, places=6)


class TestRateConversions(unittest.TestCase):
    """Test rate conversion functions."""
    
    def test_effective_annual_rate_monthly(self):
        """Test EAR with monthly compounding."""
        result = effective_annual_rate(0.12, 12)
        expected = (1 + 0.12/12) ** 12 - 1
        self.assertAlmostEqual(result, expected, places=6)
        self.assertAlmostEqual(result, 0.1268, places=4)
    
    def test_effective_annual_rate_quarterly(self):
        """Test EAR with quarterly compounding."""
        result = effective_annual_rate(0.12, 4)
        self.assertAlmostEqual(result, 0.1255, places=4)
    
    def test_effective_annual_rate_daily(self):
        """Test EAR with daily compounding."""
        result = effective_annual_rate(0.12, 365)
        # Should be close to continuous
        continuous = math.exp(0.12) - 1
        self.assertAlmostEqual(result, continuous, places=3)
    
    def test_nominal_rate_from_ear(self):
        """Test nominal rate calculation."""
        ear = 0.1268  # ~12.68%
        result = nominal_rate_from_ear(ear, 12)
        self.assertAlmostEqual(result, 0.12, places=3)
    
    def test_equivalent_rate(self):
        """Test equivalent rate conversion."""
        # Convert 12% monthly to quarterly equivalent
        result = equivalent_rate(0.12, 12, 4)
        # Both should have same EAR
        ear1 = effective_annual_rate(0.12, 12)
        ear2 = effective_annual_rate(result, 4)
        self.assertAlmostEqual(ear1, ear2, places=6)
    
    def test_annual_percentage_yield(self):
        """Test APY equals EAR."""
        result = annual_percentage_yield(0.12, 12)
        ear = effective_annual_rate(0.12, 12)
        self.assertEqual(result, ear)
    
    def test_effective_rate_invalid_frequency(self):
        """Test invalid frequency raises error."""
        with self.assertRaises(InvalidFrequencyError):
            effective_annual_rate(0.12, 0)


class TestDoublingTime(unittest.TestCase):
    """Test doubling time calculations."""
    
    def test_doubling_time_exact(self):
        """Test exact doubling time."""
        # At 7%, should take ~10 years
        result = doubling_time(0.07, 12)
        self.assertAlmostEqual(result, 9.93, places=1)
    
    def test_doubling_time_rule72(self):
        """Test Rule of 72 approximation."""
        result = doubling_time_rule72(0.07)
        expected = 72 / 7
        self.assertAlmostEqual(result, expected, places=2)
        self.assertAlmostEqual(result, 10.29, places=2)
    
    def test_doubling_time_rule69(self):
        """Test Rule of 69 approximation."""
        result = doubling_time_rule69(0.07)
        expected = 69 / 7
        self.assertAlmostEqual(result, expected, places=2)
    
    def test_doubling_time_comparison(self):
        """Compare exact vs approximation."""
        exact = doubling_time(0.07, 12)
        approx = doubling_time_rule72(0.07)
        # Should be within 10% of each other
        self.assertAlmostEqual(exact, approx, delta=1)
    
    def test_tripling_time(self):
        """Test tripling time."""
        result = tripling_time(0.07, 12)
        # Should be about 1.585 * doubling time (ln(3)/ln(2))
        double = doubling_time(0.07, 12)
        self.assertAlmostEqual(result / double, math.log(3) / math.log(2), places=2)
    
    def test_quadrupling_time(self):
        """Test quadrupling time."""
        result = quadrupling_time(0.07, 12)
        # Should be 2 * doubling time
        double = doubling_time(0.07, 12)
        self.assertAlmostEqual(result, 2 * double, places=1)
    
    def test_time_to_reach_target(self):
        """Test time to reach target."""
        result = time_to_reach_target(1000, 2000, 0.07, 12)
        # Should equal doubling time
        double = doubling_time(0.07, 12)
        self.assertAlmostEqual(result, double, places=2)
    
    def test_time_to_reach_target_custom(self):
        """Test time to reach custom target."""
        result = time_to_reach_target(1000, 1500, 0.07, 12)
        # Verify by compound amount
        amount = compound_amount(1000, 0.07, result, 12)
        self.assertAlmostEqual(amount, 1500, places=0)
    
    def test_doubling_time_zero_rate(self):
        """Test doubling time with zero rate raises error."""
        with self.assertRaises(InvalidRateError):
            doubling_time(0, 12)


class TestRequiredCalculations(unittest.TestCase):
    """Test required rate and principal calculations."""
    
    def test_required_rate(self):
        """Test required rate calculation."""
        result = required_rate(1000, 2000, 10, 12)
        # Should be around 6.95%
        self.assertAlmostEqual(result, 0.0695, places=3)
        
        # Verify
        amount = compound_amount(1000, result, 10, 12)
        self.assertAlmostEqual(amount, 2000, places=0)
    
    def test_required_principal(self):
        """Test required principal calculation."""
        target = 2000
        rate = 0.07
        time = 10
        
        result = required_principal(target, rate, time, 12)
        
        # Verify
        amount = compound_amount(result, rate, time, 12)
        self.assertAlmostEqual(amount, target, places=2)
    
    def test_required_rate_exact(self):
        """Test required rate matches doubling time."""
        # To double in 10 years
        rate = required_rate(1000, 2000, 10, 12)
        double_time = doubling_time(rate, 12)
        self.assertAlmostEqual(double_time, 10, places=1)


class TestSchedules(unittest.TestCase):
    """Test schedule generation."""
    
    def test_compound_schedule_length(self):
        """Test schedule has correct length."""
        schedule = compound_schedule(1000, 0.05, 1, 12)
        self.assertEqual(len(schedule), 12)
    
    def test_compound_schedule_values(self):
        """Test schedule values are correct."""
        schedule = compound_schedule(1000, 0.05, 1, 12)
        
        # Last period ending balance should match compound_amount
        final = schedule[-1]['ending_balance']
        expected = compound_amount(1000, 0.05, 1, 12)
        self.assertAlmostEqual(final, expected, places=2)
        
        # Total interest should match compound_interest
        total_int = schedule[-1]['total_interest']
        expected_int = compound_interest(1000, 0.05, 1, 12)
        self.assertAlmostEqual(total_int, expected_int, places=2)
    
    def test_compound_schedule_with_contributions(self):
        """Test schedule with regular contributions."""
        schedule = compound_schedule(1000, 0.05, 1, 12, 100)
        
        # Total contributions should be principal + 12 contributions
        self.assertEqual(schedule[-1]['total_contributions'], 1000 + 12*100)
    
    def test_annual_compound_schedule(self):
        """Test annual schedule."""
        schedule = annual_compound_schedule(1000, 0.05, 3, 12)
        self.assertEqual(len(schedule), 3)
        
        # Year 1 should end with compound amount for 1 year
        year1_end = schedule[0]['ending_balance']
        expected = compound_amount(1000, 0.05, 1, 12)
        self.assertAlmostEqual(year1_end, expected, places=2)
        
        # Year 3 should end with compound amount for 3 years
        year3_end = schedule[2]['ending_balance']
        expected = compound_amount(1000, 0.05, 3, 12)
        self.assertAlmostEqual(year3_end, expected, places=2)


class TestContributions(unittest.TestCase):
    """Test regular contribution calculations."""
    
    def test_future_value_with_contributions(self):
        """Test future value with contributions."""
        # $1000 initial, $100/month, 7% rate, 10 years
        result = future_value_with_contributions(1000, 0.07, 10, 100, 12)
        
        # Should be significantly more than just principal
        fv_principal = compound_amount(1000, 0.07, 10, 12)
        self.assertGreater(result, fv_principal)
        
        # Approximate check: ~$19,300
        self.assertAlmostEqual(result, 19318, places=0)
    
    def test_future_value_contributions_beginning(self):
        """Test contributions at beginning of period."""
        result_end = future_value_with_contributions(1000, 0.07, 10, 100, 12, 'end')
        result_begin = future_value_with_contributions(1000, 0.07, 10, 100, 12, 'beginning')
        
        # Beginning should be slightly higher
        self.assertGreater(result_begin, result_end)
    
    def test_required_contribution(self):
        """Test required contribution calculation."""
        target = 100000
        principal = 10000
        rate = 0.07
        years = 20
        
        result = required_contribution(target, principal, rate, years, 12)
        
        # Verify
        fv = future_value_with_contributions(principal, rate, years, result, 12)
        self.assertAlmostEqual(fv, target, places=-2)  # Within $100
    
    def test_required_contribution_already_met(self):
        """Test when principal already exceeds target."""
        result = required_contribution(10000, 20000, 0.07, 10, 12)
        self.assertEqual(result, 0)


class TestInflation(unittest.TestCase):
    """Test inflation-adjusted calculations."""
    
    def test_real_rate(self):
        """Test real rate calculation."""
        result = real_rate(0.08, 0.03)
        # Fisher equation approximation: ~5%
        self.assertAlmostEqual(result, 0.0485, places=3)
    
    def test_real_rate_exact_formula(self):
        """Test real rate formula."""
        nominal = 0.08
        inflation = 0.03
        result = real_rate(nominal, inflation)
        
        expected = (1 + nominal) / (1 + inflation) - 1
        self.assertAlmostEqual(result, expected, places=6)
    
    def test_inflation_adjusted_amount(self):
        """Test inflation-adjusted future value."""
        result = inflation_adjusted_amount(1000, 0.08, 0.03, 10, 12)
        
        # Nominal amount
        nominal = compound_amount(1000, 0.08, 10, 12)
        # Purchasing power adjustment
        expected = nominal / (1.03 ** 10)
        
        self.assertAlmostEqual(result, expected, places=2)
    
    def test_purchasing_power(self):
        """Test purchasing power without investment."""
        result = purchasing_power(1000, 0.03, 10)
        expected = 1000 / (1.03 ** 10)
        self.assertAlmostEqual(result, expected, places=2)
        # Should be less than original
        self.assertLess(result, 1000)


class TestComparisons(unittest.TestCase):
    """Test comparison functions."""
    
    def test_compare_compounding_frequencies(self):
        """Test compounding frequency comparison."""
        result = compare_compounding_frequencies(1000, 0.05, 10)
        
        # Continuous should be highest
        self.assertGreater(result['continuous'], result['daily'])
        self.assertGreater(result['daily'], result['monthly'])
        self.assertGreater(result['monthly'], result['quarterly'])
        self.assertGreater(result['quarterly'], result['annually'])
        
        # All should have keys
        self.assertIn('annually', result)
        self.assertIn('monthly', result)
        self.assertIn('continuous', result)
    
    def test_compare_rates(self):
        """Test rate comparison."""
        result = compare_rates(1000, [0.03, 0.05, 0.07], 10, 12)
        
        # Higher rate should have higher amount
        self.assertGreater(result[0.07]['amount'], result[0.05]['amount'])
        self.assertGreater(result[0.05]['amount'], result[0.03]['amount'])
        
        # All rates should be present
        self.assertIn(0.03, result)
        self.assertIn(0.05, result)
        self.assertIn(0.07, result)


class TestHelperFunctions(unittest.TestCase):
    """Test helper functions."""
    
    def test_investment_summary(self):
        """Test investment summary."""
        result = investment_summary(1000, 0.07, 10, 12, 100)
        
        # Should have all key fields
        self.assertIn('principal', result)
        self.assertIn('final_amount', result)
        self.assertIn('total_interest', result)
        self.assertIn('schedule', result)
        self.assertIn('doubling_time_years', result)
        
        # Verify some values
        self.assertEqual(result['principal'], 1000)
        self.assertEqual(len(result['schedule']), 10)
    
    def test_investment_summary_with_inflation(self):
        """Test investment summary with inflation."""
        result = investment_summary(1000, 0.07, 10, 12, 0, inflation_rate=0.03)
        
        self.assertIn('real_rate', result)
        self.assertIn('real_final_value', result)
        self.assertIn('purchasing_power_loss', result)
        
        # Real final should be less than nominal
        self.assertLess(result['real_final_value'], result['final_amount'])
    
    def test_savings_goal_analysis(self):
        """Test savings goal analysis."""
        result = savings_goal_analysis(100000, 10000, 0.07, 20, 12)
        
        # Should have key fields
        self.assertIn('goal', result)
        self.assertIn('shortfall', result)
        self.assertIn('required_contribution_per_period', result)
        self.assertIn('on_track', result)
        
        # Should need contributions
        self.assertGreater(result['shortfall'], 0)
        self.assertGreater(result['required_contribution_per_period'], 0)
        self.assertFalse(result['on_track'])
    
    def test_savings_goal_on_track(self):
        """Test savings goal already met."""
        # Goal of 10000 with principal 20000 (already exceeded)
        result = savings_goal_analysis(10000, 20000, 0.07, 10, 12)
        
        # Should be on track
        self.assertTrue(result['on_track'])
        self.assertEqual(result['time_to_reach_goal_years'], 0)
    
    def test_compound_interest_table(self):
        """Test compound interest table generation."""
        table = compound_interest_table(1000, 0.05, 5, 12)
        
        # Should be a string
        self.assertIsInstance(table, str)
        
        # Should contain key info
        self.assertIn('Principal:', table)
        self.assertIn('Annual Rate:', table)
        self.assertIn('Year', table)
        self.assertIn('Interest', table)
    
    def test_get_compounding_frequency(self):
        """Test frequency name lookup."""
        self.assertEqual(get_compounding_frequency('annual'), 1)
        self.assertEqual(get_compounding_frequency('monthly'), 12)
        self.assertEqual(get_compounding_frequency('daily'), 365)
        self.assertIsNone(get_compounding_frequency('continuous'))
        
        # Should work with different case
        self.assertEqual(get_compounding_frequency('MONTHLY'), 12)
    
    def test_get_compounding_frequency_invalid(self):
        """Test invalid frequency name."""
        with self.assertRaises(InvalidFrequencyError):
            get_compounding_frequency('invalid')


class TestEdgeCases(unittest.TestCase):
    """Test edge cases and boundary conditions."""
    
    def test_large_principal(self):
        """Test with large principal."""
        result = compound_amount(1000000, 0.05, 10, 12)
        self.assertAlmostEqual(result, 1647009, places=0)
    
    def test_small_rate(self):
        """Test with very small rate."""
        result = compound_amount(1000, 0.001, 10, 12)
        # Should be slightly more than principal
        self.assertGreater(result, 1000)
        self.assertLess(result, 1100)
    
    def test_long_time(self):
        """Test with long time period."""
        result = compound_amount(1000, 0.05, 100, 12)
        # Should be very large
        self.assertGreater(result, 100000)
    
    def test_negative_rate(self):
        """Test with small negative rate."""
        result = compound_amount(1000, -0.05, 1, 12)
        # Should be less than principal
        self.assertLess(result, 1000)


class TestConsistency(unittest.TestCase):
    """Test mathematical consistency between functions."""
    
    def test_compound_amount_equals_continuous_limit(self):
        """Test that high frequency approaches continuous."""
        # Very high compounding frequency
        high_freq = compound_amount(1000, 0.05, 10, 36500)  # 100x per day
        continuous = continuous_compound_amount(1000, 0.05, 10)
        
        # Should be very close
        self.assertAlmostEqual(high_freq, continuous, places=2)
    
    def test_doubling_then_doubling_equals_quadrupling(self):
        """Test 2x doubling time equals quadrupling time."""
        double = doubling_time(0.07, 12)
        quadruple = quadrupling_time(0.07, 12)
        
        self.assertAlmostEqual(2 * double, quadruple, places=2)
    
    def test_schedule_totals_match_simple_calculation(self):
        """Test schedule totals match direct calculation."""
        schedule = compound_schedule(1000, 0.05, 2, 12)
        
        final_balance = schedule[-1]['ending_balance']
        direct = compound_amount(1000, 0.05, 2, 12)
        
        self.assertAlmostEqual(final_balance, direct, places=2)


def run_tests():
    """Run all tests and print results."""
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromModule(sys.modules[__name__])
    
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    return result.wasSuccessful()


if __name__ == '__main__':
    success = run_tests()
    sys.exit(0 if success else 1)