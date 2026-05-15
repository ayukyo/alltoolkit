#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AllToolkit - Loan Calculator Utilities Test Suite
==================================================
Comprehensive tests for loan_calculator_utils module.

Run with: python -m pytest loan_calculator_utils_test.py -v
Or directly: python loan_calculator_utils_test.py
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from mod import (
    # Enums
    PaymentFrequency,
    PaymentType,
    InterestType,
    
    # Data Classes
    LoanParams,
    PaymentScheduleItem,
    LoanSummary,
    EarlyPayoffResult,
    RefinanceResult,
    
    # 基础计算
    monthly_rate,
    periodic_rate,
    periods_per_year,
    
    # 月供计算
    calculate_equal_payment,
    calculate_equal_principal_payment,
    calculate_interest_only_payment,
    calculate_payment,
    
    # 还款计划
    generate_amortization_schedule,
    calculate_loan_summary,
    
    # APR
    calculate_apr,
    
    # 提前还款
    analyze_early_payoff,
    
    # 再融资
    analyze_refinance,
    
    # 利息计算
    calculate_simple_interest,
    calculate_compound_interest,
    calculate_future_value,
    calculate_present_value,
    
    # 贷款比较
    compare_loans,
    
    # 房贷专用
    mortgage_qualification,
    calculate_down_payment_options,
    
    # 便捷函数
    monthly_payment,
    total_interest,
    loan_table,
)

import unittest
import math


class TestBasicCalculations(unittest.TestCase):
    """Test basic calculation functions."""
    
    def test_monthly_rate(self):
        """Test monthly rate conversion."""
        self.assertAlmostEqual(monthly_rate(12), 0.01)  # 12% annual = 1% monthly
        self.assertAlmostEqual(monthly_rate(6), 0.005)  # 6% annual = 0.5% monthly
        self.assertAlmostEqual(monthly_rate(0), 0)      # 0% annual = 0% monthly
    
    def test_periodic_rate(self):
        """Test periodic rate conversion for different frequencies."""
        # Monthly
        self.assertAlmostEqual(periodic_rate(12, PaymentFrequency.MONTHLY), 0.01)
        
        # Weekly (52 weeks/year)
        self.assertAlmostEqual(periodic_rate(52, PaymentFrequency.WEEKLY), 0.01)
        
        # Quarterly (4 quarters/year)
        self.assertAlmostEqual(periodic_rate(12, PaymentFrequency.QUARTERLY), 0.03)
        
        # Annual (1 payment/year)
        self.assertAlmostEqual(periodic_rate(12, PaymentFrequency.ANNUAL), 0.12)
    
    def test_periods_per_year(self):
        """Test periods per year calculation."""
        self.assertEqual(periods_per_year(PaymentFrequency.MONTHLY), 12)
        self.assertEqual(periods_per_year(PaymentFrequency.BI_WEEKLY), 26)
        self.assertEqual(periods_per_year(PaymentFrequency.WEEKLY), 52)
        self.assertEqual(periods_per_year(PaymentFrequency.QUARTERLY), 4)
        self.assertEqual(periods_per_year(PaymentFrequency.SEMI_ANNUAL), 2)
        self.assertEqual(periods_per_year(PaymentFrequency.ANNUAL), 1)


class TestLoanParams(unittest.TestCase):
    """Test LoanParams dataclass."""
    
    def test_valid_params(self):
        """Test creating valid loan parameters."""
        params = LoanParams(
            principal=100000,
            annual_rate=5,
            term_months=12
        )
        self.assertEqual(params.principal, 100000)
        self.assertEqual(params.annual_rate, 5)
        self.assertEqual(params.term_months, 12)
        self.assertEqual(params.payment_type, PaymentType.EQUAL_PAYMENT)
    
    def test_invalid_principal(self):
        """Test that negative/zero principal raises error."""
        with self.assertRaises(ValueError):
            LoanParams(principal=0, annual_rate=5, term_months=12)
        
        with self.assertRaises(ValueError):
            LoanParams(principal=-100, annual_rate=5, term_months=12)
    
    def test_invalid_rate(self):
        """Test that negative rate raises error."""
        with self.assertRaises(ValueError):
            LoanParams(principal=100000, annual_rate=-5, term_months=12)
    
    def test_invalid_term(self):
        """Test that negative/zero term raises error."""
        with self.assertRaises(ValueError):
            LoanParams(principal=100000, annual_rate=5, term_months=0)
        
        with self.assertRaises(ValueError):
            LoanParams(principal=100000, annual_rate=5, term_months=-12)
    
    def test_custom_payment_type(self):
        """Test custom payment type."""
        params = LoanParams(
            principal=100000,
            annual_rate=5,
            term_months=12,
            payment_type=PaymentType.EQUAL_PRINCIPAL
        )
        self.assertEqual(params.payment_type, PaymentType.EQUAL_PRINCIPAL)


class TestEqualPayment(unittest.TestCase):
    """Test equal payment (等额本息) calculations."""
    
    def test_basic_calculation(self):
        """Test basic monthly payment calculation."""
        params = LoanParams(principal=100000, annual_rate=5, term_months=12)
        payment = calculate_equal_payment(params)
        
        # Expected: ~8560.75
        self.assertAlmostEqual(payment, 8560.75, places=2)
    
    def test_zero_rate(self):
        """Test zero interest rate."""
        params = LoanParams(principal=100000, annual_rate=0, term_months=12)
        payment = calculate_equal_payment(params)
        
        # With zero rate, payment should be principal / term
        self.assertEqual(payment, 100000 / 12)
    
    def test_different_rates(self):
        """Test different interest rates."""
        test_cases = [
            (100000, 3, 360, 421.60),   # 30-year at 3%
            (100000, 5, 360, 536.82),   # 30-year at 5%
            (100000, 7, 360, 665.30),   # 30-year at 7%
        ]
        
        for principal, rate, term, expected in test_cases:
            with self.subTest(rate=rate):
                params = LoanParams(principal=principal, annual_rate=rate, term_months=term)
                payment = calculate_equal_payment(params)
                self.assertAlmostEqual(payment, expected, places=2)
    
    def test_with_down_payment(self):
        """Test payment with down payment."""
        params = LoanParams(
            principal=100000,
            annual_rate=5,
            term_months=12,
            down_payment=20000
        )
        payment = calculate_equal_payment(params)
        
        # Loan amount is 80000, so payment should be lower
        params_no_down = LoanParams(principal=80000, annual_rate=5, term_months=12)
        expected_payment = calculate_equal_payment(params_no_down)
        
        self.assertAlmostEqual(payment, expected_payment, places=2)


class TestEqualPrincipalPayment(unittest.TestCase):
    """Test equal principal (等额本金) calculations."""
    
    def test_payments_decreasing(self):
        """Test that payments decrease over time."""
        params = LoanParams(
            principal=120000,
            annual_rate=6,
            term_months=12,
            payment_type=PaymentType.EQUAL_PRINCIPAL
        )
        payments = calculate_equal_principal_payment(params)
        
        # First payment should be highest
        self.assertTrue(payments[0] > payments[-1])
        
        # Payments should be monotonically decreasing
        for i in range(len(payments) - 1):
            self.assertTrue(payments[i] > payments[i + 1])
    
    def test_principal_portion_constant(self):
        """Test that principal portion is constant."""
        params = LoanParams(
            principal=120000,
            annual_rate=6,
            term_months=12,
            payment_type=PaymentType.EQUAL_PRINCIPAL
        )
        payments = calculate_equal_principal_payment(params)
        
        principal_per_month = 120000 / 12
        r = monthly_rate(6)
        
        # Check first payment calculation
        expected_first = principal_per_month + 120000 * r
        self.assertAlmostEqual(payments[0], expected_first, places=2)
        
        # Check last payment calculation
        expected_last = principal_per_month + (120000 - 11 * principal_per_month) * r
        self.assertAlmostEqual(payments[-1], expected_last, places=2)


class TestInterestOnlyPayment(unittest.TestCase):
    """Test interest-only payment calculations."""
    
    def test_interest_only_payment(self):
        """Test interest-only payment calculation."""
        params = LoanParams(
            principal=100000,
            annual_rate=6,
            term_months=12,
            payment_type=PaymentType.INTEREST_ONLY
        )
        payment = calculate_interest_only_payment(params)
        
        # Monthly interest: 100000 * 0.06 / 12 = 500
        self.assertEqual(payment, 500.0)
    
    def test_interest_only_with_down_payment(self):
        """Test interest-only with down payment."""
        params = LoanParams(
            principal=100000,
            annual_rate=6,
            term_months=12,
            down_payment=20000,
            payment_type=PaymentType.INTEREST_ONLY
        )
        payment = calculate_interest_only_payment(params)
        
        # Loan amount: 80000, monthly interest: 80000 * 0.06 / 12 = 400
        self.assertEqual(payment, 400.0)


class TestAmortizationSchedule(unittest.TestCase):
    """Test amortization schedule generation."""
    
    def test_schedule_length(self):
        """Test that schedule has correct number of periods."""
        params = LoanParams(principal=10000, annual_rate=6, term_months=12)
        schedule = generate_amortization_schedule(params)
        
        self.assertEqual(len(schedule), 12)
    
    def test_schedule_final_balance(self):
        """Test that final balance is zero."""
        params = LoanParams(principal=10000, annual_rate=6, term_months=12)
        schedule = generate_amortization_schedule(params)
        
        self.assertEqual(schedule[-1].balance, 0)
    
    def test_schedule_interest_decreasing(self):
        """Test that interest portion decreases for equal payment."""
        params = LoanParams(principal=10000, annual_rate=6, term_months=12)
        schedule = generate_amortization_schedule(params)
        
        # Interest should decrease over time
        self.assertTrue(schedule[0].interest > schedule[-1].interest)
    
    def test_schedule_principal_increasing(self):
        """Test that principal portion increases for equal payment."""
        params = LoanParams(principal=10000, annual_rate=6, term_months=12)
        schedule = generate_amortization_schedule(params)
        
        # Principal should increase over time
        self.assertTrue(schedule[0].principal < schedule[-1].principal)
    
    def test_cumulative_totals(self):
        """Test cumulative interest and principal totals."""
        params = LoanParams(principal=10000, annual_rate=6, term_months=12)
        schedule = generate_amortization_schedule(params)
        
        # Cumulative principal at end should equal original principal
        self.assertAlmostEqual(schedule[-1].cumulative_principal, 10000, places=2)
        
        # Cumulative interest should match total interest from summary
        summary = calculate_loan_summary(params)
        self.assertAlmostEqual(schedule[-1].cumulative_interest, summary.total_interest, places=2)
    
    def test_equal_principal_schedule(self):
        """Test schedule for equal principal payment type."""
        params = LoanParams(
            principal=10000,
            annual_rate=6,
            term_months=12,
            payment_type=PaymentType.EQUAL_PRINCIPAL
        )
        schedule = generate_amortization_schedule(params)
        
        # Principal portion should be constant
        principal_per_month = 10000 / 12
        for item in schedule:
            self.assertAlmostEqual(item.principal, principal_per_month, places=2)
    
    def test_interest_only_schedule(self):
        """Test schedule for interest-only payment type."""
        params = LoanParams(
            principal=10000,
            annual_rate=6,
            term_months=12,
            payment_type=PaymentType.INTEREST_ONLY
        )
        schedule = generate_amortization_schedule(params)
        
        # Last payment should include full principal
        self.assertAlmostEqual(schedule[-1].principal, 10000, places=2)
        self.assertEqual(schedule[-1].balance, 0)


class TestLoanSummary(unittest.TestCase):
    """Test loan summary calculations."""
    
    def test_summary_totals(self):
        """Test summary total calculations."""
        params = LoanParams(principal=100000, annual_rate=5, term_months=12)
        summary = calculate_loan_summary(params)
        
        # Total payments = principal + interest
        self.assertAlmostEqual(summary.total_payments, summary.total_principal + summary.total_interest, places=2)
        
        # Total principal should equal loan amount
        self.assertEqual(summary.total_principal, 100000)
    
    def test_summary_interest(self):
        """Test that summary has positive interest."""
        params = LoanParams(principal=100000, annual_rate=5, term_months=12)
        summary = calculate_loan_summary(params)
        
        self.assertTrue(summary.total_interest > 0)
    
    def test_summary_zero_rate(self):
        """Test summary with zero interest rate."""
        params = LoanParams(principal=100000, annual_rate=0, term_months=12)
        summary = calculate_loan_summary(params)
        
        # No interest with zero rate
        self.assertAlmostEqual(summary.total_interest, 0, places=2)
        self.assertAlmostEqual(summary.total_payments, 100000, places=2)
    
    def test_summary_to_dict(self):
        """Test summary to_dict conversion."""
        params = LoanParams(principal=100000, annual_rate=5, term_months=12)
        summary = calculate_loan_summary(params)
        result = summary.to_dict()
        
        self.assertIn('principal', result)
        self.assertIn('total_payments', result)
        self.assertIn('total_interest', result)
        self.assertIn('monthly_payment', result)


class TestAPRCalculation(unittest.TestCase):
    """Test APR calculations."""
    
    def test_basic_apr(self):
        """Test basic APR calculation."""
        apr = calculate_apr(100000, 8560.75, 12, 0)
        # APR should be approximately the annual rate
        self.assertAlmostEqual(apr, 0.05, places=2)
    
    def test_apr_with_fees(self):
        """Test APR calculation with fees."""
        # With fees, APR should be higher than nominal rate
        apr_no_fees = calculate_apr(100000, 8560.75, 12, 0)
        apr_with_fees = calculate_apr(100000, 8560.75, 12, 1000)
        
        self.assertTrue(apr_with_fees > apr_no_fees)
    
    def test_apr_excessive_fees(self):
        """Test APR with excessive fees raises error."""
        with self.assertRaises(ValueError):
            calculate_apr(100000, 8560.75, 12, 100000)  # Fees equal principal


class TestSimpleInterest(unittest.TestCase):
    """Test simple interest calculations."""
    
    def test_basic_simple_interest(self):
        """Test basic simple interest."""
        interest = calculate_simple_interest(10000, 5, 2)
        # I = P * r * t = 10000 * 0.05 * 2 = 1000
        self.assertEqual(interest, 1000.0)
    
    def test_fractional_time(self):
        """Test simple interest with fractional time."""
        interest = calculate_simple_interest(10000, 5, 1.5)
        # I = 10000 * 0.05 * 1.5 = 750
        self.assertEqual(interest, 750.0)
    
    def test_zero_rate(self):
        """Test simple interest with zero rate."""
        interest = calculate_simple_interest(10000, 0, 2)
        self.assertEqual(interest, 0)


class TestCompoundInterest(unittest.TestCase):
    """Test compound interest calculations."""
    
    def test_basic_compound_interest(self):
        """Test basic compound interest."""
        interest = calculate_compound_interest(10000, 5, 2, 12)
        # A = 10000 * (1 + 0.05/12)^(12*2) ≈ 11049.41
        # Interest ≈ 1049.41
        self.assertAlmostEqual(interest, 1049.41, places=2)
    
    def test_compound_vs_simple(self):
        """Test that compound interest > simple interest."""
        simple = calculate_simple_interest(10000, 5, 2)
        compound = calculate_compound_interest(10000, 5, 2, 12)
        
        self.assertTrue(compound > simple)
    
    def test_different_compounding_periods(self):
        """Test different compounding periods."""
        # More frequent compounding = higher interest
        compound_monthly = calculate_compound_interest(10000, 5, 2, 12)
        compound_quarterly = calculate_compound_interest(10000, 5, 2, 4)
        compound_annual = calculate_compound_interest(10000, 5, 2, 1)
        
        self.assertTrue(compound_monthly > compound_quarterly)
        self.assertTrue(compound_quarterly > compound_annual)


class TestFutureValue(unittest.TestCase):
    """Test future value calculations."""
    
    def test_basic_future_value(self):
        """Test basic future value without contributions."""
        fv = calculate_future_value(10000, 5, 2)
        
        # Should be approximately compound interest result + principal
        expected = 10000 * (1 + 0.05/12) ** 24
        self.assertAlmostEqual(fv, expected, places=2)
    
    def test_future_value_with_contributions(self):
        """Test future value with regular contributions."""
        fv_no_contrib = calculate_future_value(10000, 5, 10)
        fv_with_contrib = calculate_future_value(10000, 5, 10, contributions=100)
        
        self.assertTrue(fv_with_contrib > fv_no_contrib)


class TestPresentValue(unittest.TestCase):
    """Test present value calculations."""
    
    def test_basic_present_value(self):
        """Test basic present value."""
        pv = calculate_present_value(10000, 5, 2)
        # PV = 10000 / (1 + 0.05/12)^24
        expected = 10000 / (1 + 0.05/12) ** 24
        self.assertAlmostEqual(pv, expected, places=2)
    
    def test_pv_fv_roundtrip(self):
        """Test that PV and FV are inverses."""
        fv = calculate_future_value(10000, 5, 2)
        pv = calculate_present_value(fv, 5, 2)
        
        self.assertAlmostEqual(pv, 10000, places=2)


class TestEarlyPayoffAnalysis(unittest.TestCase):
    """Test early payoff analysis."""
    
    def test_extra_payment_saves_months(self):
        """Test that extra payments save months."""
        params = LoanParams(principal=100000, annual_rate=5, term_months=360)
        result = analyze_early_payoff(params, extra_payment=100)
        
        self.assertTrue(result.months_saved > 0)
    
    def test_extra_payment_saves_interest(self):
        """Test that extra payments save interest."""
        params = LoanParams(principal=100000, annual_rate=5, term_months=360)
        result = analyze_early_payoff(params, extra_payment=100)
        
        self.assertTrue(result.interest_saved > 0)
    
    def test_lump_sum_payment(self):
        """Test lump sum payment effect."""
        params = LoanParams(principal=100000, annual_rate=5, term_months=360)
        result = analyze_early_payoff(params, lump_sum=10000, lump_sum_period=12)
        
        # Significant savings with lump sum
        self.assertTrue(result.months_saved > 0)
        self.assertTrue(result.interest_saved > 0)
    
    def test_to_dict(self):
        """Test EarlyPayoffResult to_dict."""
        params = LoanParams(principal=100000, annual_rate=5, term_months=360)
        result = analyze_early_payoff(params, extra_payment=100)
        dict_result = result.to_dict()
        
        self.assertIn('months_saved', dict_result)
        self.assertIn('interest_saved', dict_result)


class TestRefinanceAnalysis(unittest.TestCase):
    """Test refinance analysis."""
    
    def test_lower_rate_saves_money(self):
        """Test that lower rate saves money."""
        original = LoanParams(principal=200000, annual_rate=6, term_months=360)
        result = analyze_refinance(
            original,
            new_rate=4.5,
            new_term_months=360,
            closing_costs=5000
        )
        
        # Lower rate should reduce monthly payment
        self.assertTrue(result.monthly_savings > 0)
    
    def test_higher_rate_not_worth_it(self):
        """Test that higher rate is not worth refinancing."""
        original = LoanParams(principal=200000, annual_rate=4, term_months=360)
        result = analyze_refinance(
            original,
            new_rate=5,
            new_term_months=360,
            closing_costs=5000
        )
        
        # Higher rate should increase payment
        self.assertTrue(result.monthly_savings < 0)
        self.assertFalse(result.is_worth_it)
    
    def test_break_even_calculation(self):
        """Test break-even months calculation."""
        original = LoanParams(principal=200000, annual_rate=6, term_months=360)
        result = analyze_refinance(
            original,
            new_rate=4.5,
            new_term_months=360,
            closing_costs=5000
        )
        
        # Should have a positive break-even point
        if result.monthly_savings > 0:
            self.assertTrue(result.break_even_months > 0)
    
    def test_to_dict(self):
        """Test RefinanceResult to_dict."""
        original = LoanParams(principal=200000, annual_rate=6, term_months=360)
        result = analyze_refinance(
            original,
            new_rate=4.5,
            new_term_months=360,
            closing_costs=5000
        )
        dict_result = result.to_dict()
        
        self.assertIn('monthly_savings', dict_result)
        self.assertIn('is_worth_it', dict_result)


class TestCompareLoans(unittest.TestCase):
    """Test loan comparison."""
    
    def test_compare_two_loans(self):
        """Test comparing two loans."""
        loan1 = LoanParams(principal=100000, annual_rate=5, term_months=12)
        loan2 = LoanParams(principal=100000, annual_rate=4.5, term_months=24)
        
        result = compare_loans([loan1, loan2])
        
        self.assertEqual(len(result['loans']), 2)
        
        # Loan2 has lower rate but longer term
        self.assertEqual(result['shortest_term']['index'], 0)
    
    def test_find_lowest_interest(self):
        """Test finding loan with lowest total interest."""
        loan1 = LoanParams(principal=100000, annual_rate=5, term_months=12)
        loan2 = LoanParams(principal=100000, annual_rate=3, term_months=12)
        
        result = compare_loans([loan1, loan2])
        
        # Loan2 has lower rate = lower interest
        self.assertEqual(result['lowest_interest']['index'], 1)
    
    def test_find_lowest_payment(self):
        """Test finding loan with lowest monthly payment."""
        loan1 = LoanParams(principal=100000, annual_rate=5, term_months=12)
        loan2 = LoanParams(principal=100000, annual_rate=5, term_months=24)
        
        result = compare_loans([loan1, loan2])
        
        # Loan2 has longer term = lower monthly payment
        self.assertEqual(result['lowest_monthly_payment']['index'], 1)


class TestMortgageQualification(unittest.TestCase):
    """Test mortgage qualification."""
    
    def test_basic_qualification(self):
        """Test basic qualification calculation."""
        result = mortgage_qualification(
            annual_income=120000,
            monthly_debt=500,
            down_payment=50000,
            interest_rate=5
        )
        
        self.assertTrue(result['max_loan_amount'] > 0)
        self.assertTrue(result['max_home_price'] > 0)
    
    def test_dti_ratio(self):
        """Test debt-to-income ratio."""
        result = mortgage_qualification(
            annual_income=120000,
            monthly_debt=500,
            down_payment=50000,
            interest_rate=5
        )
        
        # DTI should be within limits
        self.assertTrue(result['debt_to_income_ratio'] <= 36)
    
    def test_high_debt_reduces_loan(self):
        """Test that high debt reduces max loan."""
        result_low_debt = mortgage_qualification(
            annual_income=120000,
            monthly_debt=100,
            down_payment=50000,
            interest_rate=5
        )
        
        result_high_debt = mortgage_qualification(
            annual_income=120000,
            monthly_debt=3000,
            down_payment=50000,
            interest_rate=5
        )
        
        # High debt should result in lower qualification
        self.assertTrue(result_high_debt['max_monthly_payment'] < result_low_debt['max_monthly_payment'])


class TestDownPaymentOptions(unittest.TestCase):
    """Test down payment options calculation."""
    
    def test_default_percentages(self):
        """Test default down payment percentages."""
        options = calculate_down_payment_options(500000, 5)
        
        self.assertEqual(len(options), 4)  # 5%, 10%, 15%, 20%
    
    def test_payment_variation(self):
        """Test that higher down payment = lower monthly payment."""
        options = calculate_down_payment_options(500000, 5)
        
        # Higher down payment should have lower monthly payment
        self.assertTrue(options[0]['monthly_payment'] > options[-1]['monthly_payment'])
    
    def test_interest_variation(self):
        """Test that higher down payment = lower total interest."""
        options = calculate_down_payment_options(500000, 5)
        
        # Higher down payment = smaller loan = less interest
        self.assertTrue(options[0]['total_interest'] > options[-1]['total_interest'])
    
    def test_custom_percentages(self):
        """Test custom down payment percentages."""
        options = calculate_down_payment_options(500000, 5, down_payment_percentages=[10, 20, 30])
        
        self.assertEqual(len(options), 3)


class TestConvenienceFunctions(unittest.TestCase):
    """Test convenience functions."""
    
    def test_monthly_payment_function(self):
        """Test monthly_payment convenience function."""
        payment = monthly_payment(100000, 5, 12)
        
        params = LoanParams(principal=100000, annual_rate=5, term_months=12)
        expected = calculate_equal_payment(params)
        
        self.assertAlmostEqual(payment, expected, places=2)
    
    def test_total_interest_function(self):
        """Test total_interest convenience function."""
        interest = total_interest(100000, 5, 12)
        
        self.assertTrue(interest > 0)
    
    def test_loan_table_function(self):
        """Test loan_table convenience function."""
        table = loan_table(10000, 6, 12)
        
        self.assertEqual(len(table), 12)
        self.assertIn('period', table[0])
        self.assertIn('payment', table[0])
        self.assertIn('balance', table[0])


class TestEdgeCases(unittest.TestCase):
    """Test edge cases and boundary conditions."""
    
    def test_very_short_term(self):
        """Test very short loan term."""
        params = LoanParams(principal=1000, annual_rate=5, term_months=1)
        payment = calculate_equal_payment(params)
        
        # Single payment should be approximately principal + one month interest
        expected = 1000 + 1000 * 0.05 / 12
        self.assertAlmostEqual(payment, expected, places=2)
    
    def test_very_long_term(self):
        """Test very long loan term."""
        params = LoanParams(principal=100000, annual_rate=5, term_months=600)  # 50 years
        payment = calculate_equal_payment(params)
        
        # Payment should be relatively small for long term
        self.assertTrue(payment < 1000)
    
    def test_high_interest_rate(self):
        """Test high interest rate."""
        params = LoanParams(principal=100000, annual_rate=20, term_months=12)
        summary = calculate_loan_summary(params)
        
        # High rate = high interest
        self.assertTrue(summary.total_interest > 10000)
    
    def test_large_principal(self):
        """Test large principal."""
        params = LoanParams(principal=10000000, annual_rate=5, term_months=12)
        payment = calculate_equal_payment(params)
        
        # Payment should be proportionally large
        params_small = LoanParams(principal=100000, annual_rate=5, term_months=12)
        payment_small = calculate_equal_payment(params_small)
        
        self.assertAlmostEqual(payment / payment_small, 100, places=2)


if __name__ == '__main__':
    unittest.main(verbosity=2)