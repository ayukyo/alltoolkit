"""
AllToolkit - Python Amortization Utilities Tests

Comprehensive test suite for amortization calculations.

Author: AllToolkit
License: MIT
"""

import unittest
import sys
import os
from datetime import date, timedelta

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from mod import (
    AmortizationUtils,
    AmortizationSchedule,
    AmortizationPayment,
    calculate_mortgage_payment,
    generate_mortgage_schedule
)


class TestAmortizationPayment(unittest.TestCase):
    """Test AmortizationPayment class."""
    
    def test_payment_creation(self):
        """Test basic payment creation."""
        payment = AmortizationPayment(
            payment_number=1,
            payment_date=date(2024, 1, 1),
            payment_amount=1000.0,
            principal=800.0,
            interest=200.0,
            remaining_balance=92000.0,
            cumulative_principal=800.0,
            cumulative_interest=200.0
        )
        
        self.assertEqual(payment.payment_number, 1)
        self.assertEqual(payment.payment_amount, 1000.0)
        self.assertEqual(payment.principal, 800.0)
        self.assertEqual(payment.interest, 200.0)
        self.assertEqual(payment.remaining_balance, 92000.0)
    
    def test_payment_to_dict(self):
        """Test payment serialization to dict."""
        payment = AmortizationPayment(
            payment_number=1,
            payment_date=date(2024, 1, 1),
            payment_amount=1000.0,
            principal=800.0,
            interest=200.0,
            remaining_balance=92000.0
        )
        
        result = payment.to_dict()
        
        self.assertEqual(result['payment_number'], 1)
        self.assertEqual(result['payment_date'], '2024-01-01')
        self.assertEqual(result['payment_amount'], 1000.0)
        self.assertEqual(result['principal'], 800.0)
        self.assertEqual(result['interest'], 200.0)
    
    def test_payment_repr(self):
        """Test payment string representation."""
        payment = AmortizationPayment(
            payment_number=1,
            payment_date=None,
            payment_amount=1000.0,
            principal=800.0,
            interest=200.0,
            remaining_balance=92000.0
        )
        
        repr_str = repr(payment)
        
        self.assertIn('#1', repr_str)
        self.assertIn('1000.00', repr_str)


class TestAmortizationSchedule(unittest.TestCase):
    """Test AmortizationSchedule class."""
    
    def test_schedule_creation(self):
        """Test basic schedule creation."""
        schedule = AmortizationSchedule(
            principal=100000,
            annual_rate=0.05,
            term_months=120
        )
        
        self.assertEqual(schedule.principal, 100000)
        self.assertEqual(schedule.annual_rate, 0.05)
        self.assertEqual(schedule.term_months, 120)
    
    def test_schedule_properties(self):
        """Test schedule calculated properties."""
        schedule = AmortizationSchedule(
            principal=100000,
            annual_rate=0.05,
            term_months=120
        )
        
        # Monthly payment should be calculated
        self.assertAlmostEqual(schedule.monthly_payment, 1060.66, places=2)
        
        # Total payment should be monthly * months
        self.assertAlmostEqual(schedule.total_payment, schedule.monthly_payment * 120, places=2)
        
        # Total interest should be total - principal
        self.assertAlmostEqual(schedule.total_interest, schedule.total_payment - 100000, places=2)
    
    def test_schedule_to_dict(self):
        """Test schedule serialization."""
        schedule = AmortizationSchedule(
            principal=100000,
            annual_rate=0.05,
            term_months=120,
            start_date=date(2024, 1, 1)
        )
        
        result = schedule.to_dict()
        
        self.assertEqual(result['principal'], 100000)
        self.assertEqual(result['annual_rate'], 0.05)
        self.assertEqual(result['term_months'], 120)
        self.assertEqual(result['start_date'], '2024-01-01')


class TestAmortizationUtils(unittest.TestCase):
    """Test AmortizationUtils class."""
    
    def test_calculate_monthly_payment_basic(self):
        """Test basic monthly payment calculation."""
        # $100,000 loan at 5% for 10 years (120 months)
        payment = AmortizationUtils.calculate_monthly_payment(100000, 0.05, 120)
        
        # Expected payment is approximately $1,060.66
        self.assertAlmostEqual(payment, 1060.66, places=2)
    
    def test_calculate_monthly_payment_mortgage(self):
        """Test mortgage payment calculation."""
        # $200,000 loan at 6% for 30 years (360 months)
        payment = AmortizationUtils.calculate_monthly_payment(200000, 0.06, 360)
        
        # Expected payment is approximately $1,199.10
        self.assertAlmostEqual(payment, 1199.10, places=2)
    
    def test_calculate_monthly_payment_zero_rate(self):
        """Test payment calculation with zero interest."""
        # $12,000 loan at 0% for 12 months
        payment = AmortizationUtils.calculate_monthly_payment(12000, 0, 12)
        
        self.assertEqual(payment, 1000.0)
    
    def test_calculate_monthly_payment_zero_principal(self):
        """Test payment calculation with zero principal."""
        payment = AmortizationUtils.calculate_monthly_payment(0, 0.05, 12)
        
        self.assertEqual(payment, 0.0)
    
    def test_calculate_interest_portion(self):
        """Test interest portion calculation."""
        # $100,000 balance at 6% annual rate
        # Monthly interest = 100000 * (0.06 / 12) = 500
        interest = AmortizationUtils.calculate_interest_portion(100000, 0.06)
        
        self.assertAlmostEqual(interest, 500.0, places=2)
    
    def test_generate_schedule_basic(self):
        """Test basic schedule generation."""
        schedule = AmortizationUtils.generate_schedule(
            principal=10000,
            annual_rate=0.05,
            term_months=12
        )
        
        self.assertEqual(len(schedule.payments), 12)
        self.assertAlmostEqual(schedule.principal, 10000)
        
        # Last payment should have near-zero balance
        last_payment = schedule.payments[-1]
        self.assertLess(last_payment.remaining_balance, 0.01)
    
    def test_generate_schedule_with_dates(self):
        """Test schedule generation with specific start date."""
        start = date(2024, 1, 1)
        schedule = AmortizationUtils.generate_schedule(
            principal=10000,
            annual_rate=0.05,
            term_months=12,
            start_date=start
        )
        
        self.assertEqual(schedule.start_date, start)
        self.assertEqual(schedule.payments[0].payment_date, start)
        self.assertEqual(schedule.payments[1].payment_date, date(2024, 2, 1))
    
    def test_generate_schedule_with_extra_payments(self):
        """Test schedule with extra monthly payments."""
        # Original schedule
        original = AmortizationUtils.generate_schedule(
            principal=100000,
            annual_rate=0.05,
            term_months=120
        )
        
        # With extra $100/month
        with_extra = AmortizationUtils.generate_schedule(
            principal=100000,
            annual_rate=0.05,
            term_months=120,
            extra_monthly=100
        )
        
        # Should pay off faster
        self.assertLess(len(with_extra.payments), len(original.payments))
        self.assertLess(with_extra.total_interest, original.total_interest)
    
    def test_calculate_remaining_balance(self):
        """Test remaining balance calculation."""
        # $100,000 at 5% for 10 years
        # After 12 months, should have balance remaining
        balance = AmortizationUtils.calculate_remaining_balance(
            principal=100000,
            annual_rate=0.05,
            term_months=120,
            months_paid=12
        )
        
        self.assertGreater(balance, 90000)
        self.assertLess(balance, 100000)
    
    def test_calculate_remaining_balance_zero_months(self):
        """Test remaining balance with zero months paid."""
        balance = AmortizationUtils.calculate_remaining_balance(
            principal=100000,
            annual_rate=0.05,
            term_months=120,
            months_paid=0
        )
        
        self.assertEqual(balance, 100000)
    
    def test_calculate_early_payoff(self):
        """Test early payoff analysis."""
        result = AmortizationUtils.calculate_early_payoff(
            principal=200000,
            annual_rate=0.05,
            term_months=360,
            months_paid=60,
            extra_payment=50000
        )
        
        self.assertIn('remaining_balance', result)
        self.assertIn('extra_payment', result)
        self.assertIn('interest_saved', result)
        self.assertIn('months_saved', result)
        
        self.assertEqual(result['extra_payment'], 50000)
        self.assertGreater(result['interest_saved'], 0)
    
    def test_calculate_extra_payment_impact(self):
        """Test extra payment impact analysis."""
        result = AmortizationUtils.calculate_extra_payment_impact(
            principal=200000,
            annual_rate=0.05,
            term_months=360,
            extra_monthly=200
        )
        
        self.assertIn('months_saved', result)
        self.assertIn('interest_saved', result)
        self.assertIn('years_saved', result)
        
        # Should save time and interest
        self.assertGreater(result['months_saved'], 0)
        self.assertGreater(result['interest_saved'], 0)
    
    def test_calculate_refinance_comparison(self):
        """Test refinance comparison."""
        result = AmortizationUtils.calculate_refinance_comparison(
            current_balance=180000,
            current_rate=0.06,
            current_remaining_months=300,
            new_rate=0.045,
            new_term_months=360,
            closing_costs=5000
        )
        
        self.assertIn('current', result)
        self.assertIn('refinance', result)
        self.assertIn('comparison', result)
        
        self.assertEqual(result['current']['balance'], 180000)
        self.assertEqual(result['refinance']['closing_costs'], 5000)
        
        # Lower rate should have lower payment
        self.assertGreater(
            result['current']['monthly_payment'],
            result['refinance']['monthly_payment']
        )
    
    def test_calculate_apr(self):
        """Test APR calculation."""
        apr = AmortizationUtils.calculate_apr(
            principal=200000,
            monthly_payment=1073.64,
            term_months=360,
            fees=5000
        )
        
        # APR should be slightly higher than nominal rate due to fees
        # For this case, around 5.27%
        self.assertGreater(apr, 0.04)  # At least 4%
        self.assertLess(apr, 0.08)  # Less than 8%
    
    def test_find_term_for_payment(self):
        """Test finding term for target payment."""
        result = AmortizationUtils.find_term_for_payment(
            principal=100000,
            annual_rate=0.05,
            target_payment=1500
        )
        
        self.assertTrue(result['possible'])
        self.assertGreater(result['term_months'], 0)
        self.assertLess(result['monthly_payment'], 1500.01)
    
    def test_find_term_for_payment_too_low(self):
        """Test finding term when payment is too low."""
        result = AmortizationUtils.find_term_for_payment(
            principal=100000,
            annual_rate=0.05,
            target_payment=100  # Very low payment
        )
        
        self.assertFalse(result['possible'])
        self.assertIn('minimum_payment', result)
    
    def test_calculate_affordable_principal(self):
        """Test affordable principal calculation."""
        result = AmortizationUtils.calculate_affordable_principal(
            monthly_payment=1500,
            annual_rate=0.05,
            term_months=360,
            down_payment=50000
        )
        
        self.assertIn('loan_amount', result)
        self.assertIn('down_payment', result)
        self.assertIn('total_home_price', result)
        
        self.assertEqual(result['down_payment'], 50000)
        self.assertGreater(result['total_home_price'], result['loan_amount'])


class TestConvenienceFunctions(unittest.TestCase):
    """Test convenience functions."""
    
    def test_calculate_mortgage_payment(self):
        """Test mortgage payment convenience function."""
        # Note: This function takes rate as percentage (e.g., 6.5 for 6.5%)
        payment = calculate_mortgage_payment(
            principal=200000,
            annual_rate=6.5,  # Percentage
            years=30
        )
        
        # Expected payment around $1,264
        self.assertAlmostEqual(payment, 1264.14, places=2)
    
    def test_generate_mortgage_schedule(self):
        """Test mortgage schedule convenience function."""
        schedule = generate_mortgage_schedule(
            principal=200000,
            annual_rate=6.5,  # Percentage
            years=30
        )
        
        self.assertEqual(len(schedule.payments), 360)
        self.assertAlmostEqual(schedule.principal, 200000)


class TestEdgeCases(unittest.TestCase):
    """Test edge cases and boundary conditions."""
    
    def test_very_small_loan(self):
        """Test with very small loan amount."""
        schedule = AmortizationUtils.generate_schedule(
            principal=100,
            annual_rate=0.05,
            term_months=12
        )
        
        self.assertEqual(len(schedule.payments), 12)
    
    def test_very_high_rate(self):
        """Test with high interest rate."""
        payment = AmortizationUtils.calculate_monthly_payment(
            principal=10000,
            annual_rate=0.25,  # 25% interest
            term_months=36
        )
        
        self.assertGreater(payment, 0)
    
    def test_short_term(self):
        """Test with short loan term."""
        schedule = AmortizationUtils.generate_schedule(
            principal=1000,
            annual_rate=0.05,
            term_months=3
        )
        
        self.assertEqual(len(schedule.payments), 3)
    
    def test_schedule_get_payment(self):
        """Test getting a specific payment from schedule."""
        schedule = AmortizationUtils.generate_schedule(
            principal=10000,
            annual_rate=0.05,
            term_months=12
        )
        
        # Get first payment
        first = schedule.get_payment(1)
        self.assertIsNotNone(first)
        self.assertEqual(first.payment_number, 1)
        
        # Get invalid payment
        invalid = schedule.get_payment(100)
        self.assertIsNone(invalid)
    
    def test_schedule_year_summary(self):
        """Test year summary calculation."""
        schedule = AmortizationUtils.generate_schedule(
            principal=100000,
            annual_rate=0.05,
            term_months=36,  # 3 years
            start_date=date(2024, 1, 1)
        )
        
        year_2024 = schedule.get_year_summary(2024)
        
        self.assertEqual(year_2024['year'], 2024)
        self.assertEqual(year_2024['payments_count'], 12)
        self.assertGreater(year_2024['total_principal'], 0)
        self.assertGreater(year_2024['total_interest'], 0)


class TestRealWorldScenarios(unittest.TestCase):
    """Test real-world loan scenarios."""
    
    def test_typical_mortgage(self):
        """Test typical 30-year mortgage."""
        # $300,000 at 7% for 30 years
        schedule = AmortizationUtils.generate_schedule(
            principal=300000,
            annual_rate=0.07,
            term_months=360
        )
        
        # Verify basic properties
        self.assertAlmostEqual(schedule.monthly_payment, 1995.91, places=2)
        self.assertEqual(len(schedule.payments), 360)
        
        # First payment should be mostly interest
        first = schedule.payments[0]
        self.assertGreater(first.interest, first.principal)
        
        # Last payment should be mostly principal
        last = schedule.payments[-1]
        self.assertGreater(last.principal, last.interest)
    
    def test_auto_loan(self):
        """Test typical auto loan."""
        # $25,000 at 5.5% for 5 years
        schedule = AmortizationUtils.generate_schedule(
            principal=25000,
            annual_rate=0.055,
            term_months=60
        )
        
        self.assertAlmostEqual(schedule.monthly_payment, 477.53, places=2)
        self.assertEqual(len(schedule.payments), 60)
    
    def test_personal_loan(self):
        """Test typical personal loan."""
        # $10,000 at 10% for 3 years
        schedule = AmortizationUtils.generate_schedule(
            principal=10000,
            annual_rate=0.10,
            term_months=36
        )
        
        self.assertAlmostEqual(schedule.monthly_payment, 322.67, places=2)
        
        # Total interest should be reasonable
        self.assertGreater(schedule.total_interest, 1000)
        self.assertLess(schedule.total_interest, 2000)
    
    def test_early_payoff_analysis(self):
        """Test early payoff scenario."""
        # 5 years into a 30-year mortgage
        result = AmortizationUtils.calculate_early_payoff(
            principal=300000,
            annual_rate=0.07,
            term_months=360,
            months_paid=60,
            extra_payment=50000
        )
        
        # Should save significant interest
        self.assertGreater(result['interest_saved'], 50000)
        self.assertGreater(result['months_saved'], 0)  # At least some months saved


if __name__ == '__main__':
    unittest.main()