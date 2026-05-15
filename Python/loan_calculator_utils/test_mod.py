"""
Test Module for Loan Calculator Utils

Tests all loan calculation functions including:
- Monthly payment calculations
- Amortization schedule generation
- APR calculation
- Early payoff analysis
- Refinance analysis
- Interest calculations
"""

import unittest
from mod import (
    LoanParams, PaymentType, PaymentFrequency,
    calculate_equal_payment, calculate_equal_principal_payment,
    calculate_interest_only_payment, calculate_payment,
    generate_amortization_schedule, calculate_loan_summary,
    calculate_apr, analyze_early_payoff, analyze_refinance,
    calculate_simple_interest, calculate_compound_interest,
    calculate_future_value, calculate_present_value,
    compare_loans, mortgage_qualification, calculate_down_payment_options,
    monthly_payment, total_interest, loan_table,
    monthly_rate, periodic_rate, periods_per_year,
)


class TestBasicCalculations(unittest.TestCase):
    """Test basic calculation functions"""
    
    def test_monthly_rate(self):
        """Test monthly rate conversion"""
        self.assertAlmostEqual(monthly_rate(12), 0.01, places=4)
        self.assertAlmostEqual(monthly_rate(6), 0.005, places=4)
        self.assertAlmostEqual(monthly_rate(0), 0.0, places=4)
    
    def test_periodic_rate(self):
        """Test periodic rate conversion"""
        self.assertAlmostEqual(
            periodic_rate(12, PaymentFrequency.MONTHLY), 0.01, places=4
        )
        self.assertAlmostEqual(
            periodic_rate(12, PaymentFrequency.BI_WEEKLY), 12 / 100 / 26, places=4
        )
        self.assertAlmostEqual(
            periodic_rate(12, PaymentFrequency.WEEKLY), 12 / 100 / 52, places=4
        )
    
    def test_periods_per_year(self):
        """Test periods per year mapping"""
        self.assertEqual(periods_per_year(PaymentFrequency.MONTHLY), 12)
        self.assertEqual(periods_per_year(PaymentFrequency.BI_WEEKLY), 26)
        self.assertEqual(periods_per_year(PaymentFrequency.WEEKLY), 52)
        self.assertEqual(periods_per_year(PaymentFrequency.QUARTERLY), 4)
        self.assertEqual(periods_per_year(PaymentFrequency.ANNUAL), 1)


class TestEqualPayment(unittest.TestCase):
    """Test equal payment (等额本息) calculations"""
    
    def test_basic_calculation(self):
        """Test basic monthly payment calculation"""
        params = LoanParams(principal=100000, annual_rate=5, term_months=12)
        payment = calculate_equal_payment(params)
        
        # Verify payment is reasonable
        self.assertGreater(payment, 100000 / 12)  # Should be greater than principal spread
        self.assertLess(payment, 100000 / 12 * 1.1)  # Should not be too high
    
    def test_zero_interest(self):
        """Test zero interest loan"""
        params = LoanParams(principal=10000, annual_rate=0, term_months=10)
        payment = calculate_equal_payment(params)
        self.assertEqual(payment, 1000.0)  # Exactly principal / periods
    
    def test_high_interest(self):
        """Test high interest loan"""
        params = LoanParams(principal=10000, annual_rate=24, term_months=12)
        payment = calculate_equal_payment(params)
        
        # Total payment should exceed principal significantly
        total = payment * 12
        self.assertGreater(total, 10000 * 1.1)
    
    def test_long_term(self):
        """Test long term loan (mortgage)"""
        params = LoanParams(principal=500000, annual_rate=5, term_months=360)
        payment = calculate_equal_payment(params)
        
        # Verify reasonable mortgage payment
        self.assertGreater(payment, 2000)
        self.assertLess(payment, 3000)


class TestEqualPrincipal(unittest.TestCase):
    """Test equal principal (等额本金) calculations"""
    
    def test_decreasing_payments(self):
        """Test that payments decrease over time"""
        params = LoanParams(
            principal=120000, annual_rate=6, term_months=12,
            payment_type=PaymentType.EQUAL_PRINCIPAL
        )
        payments = calculate_equal_principal_payment(params)
        
        # First payment should be highest
        self.assertEqual(payments[0], max(payments))
        # Last payment should be lowest
        self.assertEqual(payments[-1], min(payments))
        # Verify decreasing trend
        for i in range(len(payments) - 1):
            self.assertGreater(payments[i], payments[i + 1])
    
    def test_principal_is_equal(self):
        """Test that principal portion is equal each period"""
        params = LoanParams(
            principal=120000, annual_rate=6, term_months=12,
            payment_type=PaymentType.EQUAL_PRINCIPAL
        )
        payments = calculate_equal_principal_payment(params)
        r = monthly_rate(6)
        
        principal_per_period = 120000 / 12
        remaining = 120000
        
        for i, payment in enumerate(payments):
            interest = remaining * r
            expected_principal = principal_per_period
            expected_payment = expected_principal + interest
            
            self.assertAlmostEqual(payment, expected_payment, places=2)
            remaining -= principal_per_period


class TestInterestOnly(unittest.TestCase):
    """Test interest only payment calculations"""
    
    def test_interest_only_payment(self):
        """Test interest only payment"""
        params = LoanParams(
            principal=100000, annual_rate=6, term_months=12,
            payment_type=PaymentType.INTEREST_ONLY
        )
        payment = calculate_interest_only_payment(params)
        
        # Interest should be 100000 * 0.06 / 12 = 500
        self.assertAlmostEqual(payment, 500.0, places=2)
    
    def test_schedule_has_principal_at_end(self):
        """Test that principal is repaid at end"""
        params = LoanParams(
            principal=100000, annual_rate=6, term_months=12,
            payment_type=PaymentType.INTEREST_ONLY
        )
        schedule = generate_amortization_schedule(params)
        
        # All periods except last should have zero principal
        for item in schedule[:-1]:
            self.assertAlmostEqual(item.principal, 0.0, places=2)
        
        # Last period should have full principal
        self.assertAlmostEqual(schedule[-1].principal, 100000.0, places=2)


class TestAmortizationSchedule(unittest.TestCase):
    """Test amortization schedule generation"""
    
    def test_schedule_length(self):
        """Test schedule has correct number of periods"""
        params = LoanParams(principal=10000, annual_rate=6, term_months=12)
        schedule = generate_amortization_schedule(params)
        
        self.assertEqual(len(schedule), 12)
    
    def test_balance_decreases(self):
        """Test that balance decreases over time"""
        params = LoanParams(principal=10000, annual_rate=6, term_months=12)
        schedule = generate_amortization_schedule(params)
        
        for i in range(len(schedule) - 1):
            self.assertGreater(schedule[i].balance, schedule[i + 1].balance)
        
        # Final balance should be zero
        self.assertAlmostEqual(schedule[-1].balance, 0.0, places=2)
    
    def test_interest_decreases(self):
        """Test that interest portion decreases"""
        params = LoanParams(principal=10000, annual_rate=6, term_months=12)
        schedule = generate_amortization_schedule(params)
        
        # Interest should decrease over time (for equal payment)
        for i in range(len(schedule) - 1):
            self.assertGreater(schedule[i].interest, schedule[i + 1].interest)
    
    def test_principal_increases(self):
        """Test that principal portion increases"""
        params = LoanParams(principal=10000, annual_rate=6, term_months=12)
        schedule = generate_amortization_schedule(params)
        
        # Principal should increase over time (for equal payment)
        for i in range(len(schedule) - 1):
            self.assertLess(schedule[i].principal, schedule[i + 1].principal)
    
    def test_cumulative_totals(self):
        """Test cumulative interest and principal"""
        params = LoanParams(principal=10000, annual_rate=6, term_months=12)
        schedule = generate_amortization_schedule(params)
        
        # Final cumulative principal should equal original principal
        self.assertAlmostEqual(schedule[-1].cumulative_principal, 10000.0, places=2)
        
        # Cumulative totals should match sum of individual values
        total_interest = sum(item.interest for item in schedule)
        self.assertAlmostEqual(schedule[-1].cumulative_interest, total_interest, places=2)


class TestLoanSummary(unittest.TestCase):
    """Test loan summary calculation"""
    
    def test_total_payments(self):
        """Test total payments calculation"""
        params = LoanParams(principal=100000, annual_rate=5, term_months=12)
        summary = calculate_loan_summary(params)
        
        # Total payments = monthly payment * periods
        expected_total = summary.monthly_payment * 12
        self.assertAlmostEqual(summary.total_payments, expected_total, places=2)
    
    def test_total_interest(self):
        """Test total interest calculation"""
        params = LoanParams(principal=100000, annual_rate=5, term_months=12)
        summary = calculate_loan_summary(params)
        
        # Total interest = total payments - principal
        expected_interest = summary.total_payments - params.principal
        self.assertAlmostEqual(summary.total_interest, expected_interest, places=2)
    
    def test_comparison_equal_vs_equal_principal(self):
        """Compare equal payment vs equal principal total interest"""
        params_equal = LoanParams(principal=100000, annual_rate=5, term_months=12)
        params_equal_p = LoanParams(
            principal=100000, annual_rate=5, term_months=12,
            payment_type=PaymentType.EQUAL_PRINCIPAL
        )
        
        summary_equal = calculate_loan_summary(params_equal)
        summary_equal_p = calculate_loan_summary(params_equal_p)
        
        # Equal principal should have less total interest
        self.assertLess(summary_equal_p.total_interest, summary_equal.total_interest)


class TestAPRCalculation(unittest.TestCase):
    """Test APR calculation"""
    
    def test_apr_with_fees(self):
        """Test APR is higher than rate when fees exist"""
        principal = 100000
        payment = monthly_payment(100000, 5, 12)
        apr = calculate_apr(principal, payment, 12, fees=2000)
        
        # APR should be higher than stated rate due to fees
        self.assertGreater(apr, 0.05)
    
    def test_apr_no_fees(self):
        """Test APR equals rate when no fees"""
        principal = 100000
        payment = monthly_payment(100000, 5, 12)
        apr = calculate_apr(principal, payment, 12, fees=0)
        
        # APR should approximately equal stated rate
        self.assertAlmostEqual(apr, 0.05, places=2)


class TestEarlyPayoff(unittest.TestCase):
    """Test early payoff analysis"""
    
    def test_extra_payment_saves_interest(self):
        """Test extra payment saves interest"""
        params = LoanParams(principal=100000, annual_rate=5, term_months=12)
        result = analyze_early_payoff(params, extra_payment=1000)
        
        # Should save some interest
        self.assertGreater(result.interest_saved, 0)
    
    def test_lump_sum_payment(self):
        """Test lump sum payment effect"""
        params = LoanParams(principal=100000, annual_rate=5, term_months=12)
        result = analyze_early_payoff(params, lump_sum=50000, lump_sum_period=3)
        
        # Should significantly reduce term
        self.assertGreater(result.months_saved, 4)
    
    def test_months_saved(self):
        """Test months saved calculation"""
        params = LoanParams(principal=100000, annual_rate=5, term_months=360)
        result = analyze_early_payoff(params, extra_payment=200)
        
        # Should save months
        self.assertGreater(result.months_saved, 0)


class TestRefinance(unittest.TestCase):
    """Test refinance analysis"""
    
    def test_lower_rate_saves_money(self):
        """Test lower rate saves money"""
        original = LoanParams(principal=200000, annual_rate=6, term_months=360)
        result = analyze_refinance(
            original, new_rate=4.5, new_term_months=360, closing_costs=5000
        )
        
        # Lower rate should save monthly payment
        self.assertGreater(result.monthly_savings, 0)
        # Lower rate should save total interest
        self.assertGreater(result.total_savings, 0)
    
    def test_high_closing_costs(self):
        """Test high closing costs can make refinance unfavorable"""
        original = LoanParams(principal=100000, annual_rate=5, term_months=120)
        result = analyze_refinance(
            original, new_rate=4.5, new_term_months=120, closing_costs=10000
        )
        
        # High closing costs might make it not worth it
        # Check net savings accounting
        if result.net_savings < 0:
            self.assertFalse(result.is_worth_it)
    
    def test_break_even_calculation(self):
        """Test break-even months calculation"""
        original = LoanParams(principal=200000, annual_rate=6, term_months=360)
        result = analyze_refinance(
            original, new_rate=4.5, new_term_months=360, closing_costs=5000
        )
        
        # Break-even should be positive
        self.assertGreater(result.break_even_months, 0)


class TestInterestCalculations(unittest.TestCase):
    """Test simple and compound interest calculations"""
    
    def test_simple_interest(self):
        """Test simple interest calculation"""
        interest = calculate_simple_interest(10000, 5, 2)
        # I = P * r * t = 10000 * 0.05 * 2 = 1000
        self.assertEqual(interest, 1000.0)
    
    def test_compound_interest(self):
        """Test compound interest calculation"""
        interest = calculate_compound_interest(10000, 5, 2, compounds_per_year=12)
        # Should be greater than simple interest
        simple_interest = calculate_simple_interest(10000, 5, 2)
        self.assertGreater(interest, simple_interest)
    
    def test_future_value(self):
        """Test future value calculation"""
        fv = calculate_future_value(10000, 5, 10)
        # Should be greater than principal
        self.assertGreater(fv, 10000)
    
    def test_future_value_with_contributions(self):
        """Test future value with contributions"""
        fv_no_contrib = calculate_future_value(10000, 5, 10)
        fv_with_contrib = calculate_future_value(10000, 5, 10, contributions=100)
        
        # With contributions should be higher
        self.assertGreater(fv_with_contrib, fv_no_contrib)
    
    def test_present_value(self):
        """Test present value calculation"""
        pv = calculate_present_value(10000, 5, 2)
        # Present value should be less than future value
        self.assertLess(pv, 10000)


class TestLoanComparison(unittest.TestCase):
    """Test loan comparison"""
    
    def test_compare_different_rates(self):
        """Test comparing loans with different rates"""
        loan1 = LoanParams(principal=100000, annual_rate=5, term_months=12)
        loan2 = LoanParams(principal=100000, annual_rate=4, term_months=12)
        
        result = compare_loans([loan1, loan2])
        
        # Lower rate should have lower interest
        self.assertEqual(result['lowest_interest']['index'], 1)
    
    def test_compare_different_terms(self):
        """Test comparing loans with different terms"""
        loan1 = LoanParams(principal=100000, annual_rate=5, term_months=12)
        loan2 = LoanParams(principal=100000, annual_rate=5, term_months=24)
        
        result = compare_loans([loan1, loan2])
        
        # Shorter term should be identified
        self.assertEqual(result['shortest_term']['index'], 0)


class TestMortgageQualification(unittest.TestCase):
    """Test mortgage qualification"""
    
    def test_qualification_calculation(self):
        """Test mortgage qualification"""
        result = mortgage_qualification(
            annual_income=120000, monthly_debt=500, down_payment=50000, interest_rate=5
        )
        
        # Should return valid loan amount
        self.assertGreater(result['max_loan_amount'], 0)
        self.assertGreater(result['max_home_price'], result['max_loan_amount'])
    
    def test_dti_calculation(self):
        """Test DTI is calculated"""
        result = mortgage_qualification(
            annual_income=120000, monthly_debt=500, down_payment=50000, interest_rate=5
        )
        
        # DTI should be positive
        self.assertGreater(result['debt_to_income_ratio'], 0)
        self.assertLess(result['debt_to_income_ratio'], 100)


class TestDownPaymentOptions(unittest.TestCase):
    """Test down payment options"""
    
    def test_multiple_options(self):
        """Test multiple down payment options"""
        options = calculate_down_payment_options(500000, 5)
        
        # Should return 4 options (5%, 10%, 15%, 20%)
        self.assertEqual(len(options), 4)
    
    def test_higher_down_payment_lower_interest(self):
        """Test higher down payment reduces total interest"""
        options = calculate_down_payment_options(500000, 5)
        
        # Higher down payment should have lower total interest
        for i in range(len(options) - 1):
            self.assertGreater(options[i]['total_interest'], options[i + 1]['total_interest'])


class TestConvenienceFunctions(unittest.TestCase):
    """Test convenience functions"""
    
    def test_monthly_payment_func(self):
        """Test monthly_payment convenience function"""
        payment = monthly_payment(100000, 5, 12)
        
        # Should match full calculation
        params = LoanParams(principal=100000, annual_rate=5, term_months=12)
        expected = calculate_equal_payment(params)
        
        self.assertAlmostEqual(payment, expected, places=2)
    
    def test_total_interest_func(self):
        """Test total_interest convenience function"""
        interest = total_interest(100000, 5, 12)
        
        # Should be positive
        self.assertGreater(interest, 0)
    
    def test_loan_table_func(self):
        """Test loan_table convenience function"""
        table = loan_table(10000, 6, 12)
        
        # Should return 12 entries
        self.assertEqual(len(table), 12)
        
        # Each entry should have required fields
        for entry in table:
            self.assertIn('period', entry)
            self.assertIn('payment', entry)
            self.assertIn('principal', entry)
            self.assertIn('interest', entry)
            self.assertIn('balance', entry)


class TestEdgeCases(unittest.TestCase):
    """Test edge cases"""
    
    def test_zero_interest(self):
        """Test zero interest loan"""
        params = LoanParams(principal=10000, annual_rate=0, term_months=10)
        summary = calculate_loan_summary(params)
        
        # No interest should be paid
        self.assertAlmostEqual(summary.total_interest, 0, places=2)
    
    def test_very_short_term(self):
        """Test very short term"""
        params = LoanParams(principal=1000, annual_rate=10, term_months=1)
        summary = calculate_loan_summary(params)
        
        # Single payment
        self.assertEqual(summary.number_of_payments, 1)
    
    def test_large_loan(self):
        """Test large loan amount"""
        params = LoanParams(principal=10000000, annual_rate=4, term_months=360)
        payment = calculate_equal_payment(params)
        
        # Payment should be reasonable proportion
        self.assertGreater(payment, params.principal / params.term_months)


if __name__ == '__main__':
    unittest.main()