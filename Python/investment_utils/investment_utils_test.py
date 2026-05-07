"""
Unit tests for Investment Utils.

Run with: python -m pytest investment_utils_test.py -v
Or with: python investment_utils_test.py
"""

import unittest
import math
from investment_utils import (
    # Compound interest
    compound_interest,
    compound_interest_continuous,
    # Simple interest
    simple_interest,
    # SIP
    sip_returns,
    sip_step_up,
    # CAGR
    cagr,
    cagr_from_returns,
    # Present/Future value
    present_value,
    future_value,
    present_value_annuity,
    # ROI
    roi,
    annualized_roi,
    # IRR/NPV
    irr,
    npv,
    # Payback
    payback_period,
    discounted_payback_period,
    # Loan
    loan_payment,
    amortization_schedule,
    # Comparison
    compare_investments,
    inflation_adjusted_return,
    rule_of_72,
    rule_of_69,
    # Time value
    time_to_target,
    required_rate,
    # Inflation
    future_value_with_inflation,
    # Depreciation
    straight_line_depreciation,
    declining_balance_depreciation,
    CompoundingFrequency,
    InvestmentResult,
    SIPResult,
    AmortizationEntry,
)


class TestCompoundInterest(unittest.TestCase):
    """Tests for compound interest calculations."""
    
    def test_basic_compound_interest(self):
        """Test basic compound interest calculation."""
        result = compound_interest(10000, 0.08, 5)
        # A = 10000 * (1 + 0.08/12)^(12*5)
        expected = 10000 * math.pow(1 + 0.08/12, 60)
        self.assertAlmostEqual(result.total_amount, expected, places=1)
        self.assertEqual(result.principal, 10000)
        self.assertTrue(result.total_interest > 0)
    
    def test_annual_compounding(self):
        """Test annual compounding."""
        result = compound_interest(10000, 0.08, 5, n=1)
        # A = 10000 * (1.08)^5
        expected = 10000 * math.pow(1.08, 5)
        self.assertAlmostEqual(result.total_amount, expected, places=1)
    
    def test_quarterly_compounding(self):
        """Test quarterly compounding."""
        result = compound_interest(10000, 0.08, 5, n=4)
        expected = 10000 * math.pow(1 + 0.08/4, 20)
        self.assertAlmostEqual(result.total_amount, expected, places=1)
    
    def test_zero_rate(self):
        """Test with zero interest rate."""
        result = compound_interest(10000, 0, 5)
        self.assertEqual(result.total_amount, 10000)
        self.assertEqual(result.total_interest, 0)
    
    def test_zero_time(self):
        """Test with zero time period."""
        result = compound_interest(10000, 0.08, 0)
        self.assertEqual(result.total_amount, 10000)
    
    def test_negative_principal_raises(self):
        """Test that negative principal raises error."""
        with self.assertRaises(ValueError):
            compound_interest(-1000, 0.08, 5)
    
    def test_negative_rate_raises(self):
        """Test that negative rate raises error."""
        with self.assertRaises(ValueError):
            compound_interest(10000, -0.08, 5)
    
    def test_continuous_compounding(self):
        """Test continuous compounding."""
        result = compound_interest_continuous(10000, 0.08, 5)
        # A = 10000 * e^(0.08*5)
        expected = 10000 * math.exp(0.4)
        self.assertAlmostEqual(result.total_amount, expected, places=1)
    
    def test_effective_rate(self):
        """Test effective annual rate calculation."""
        result = compound_interest(10000, 0.08, 1, n=12)
        # Effective rate = (1 + 0.08/12)^12 - 1
        expected_effective = math.pow(1 + 0.08/12, 12) - 1
        self.assertAlmostEqual(result.effective_rate, expected_effective, places=4)


class TestSimpleInterest(unittest.TestCase):
    """Tests for simple interest calculations."""
    
    def test_basic_simple_interest(self):
        """Test basic simple interest."""
        result = simple_interest(10000, 0.08, 5)
        # A = 10000 * (1 + 0.08*5) = 10000 * 1.4 = 14000
        self.assertEqual(result.total_amount, 14000)
        self.assertEqual(result.total_interest, 4000)
    
    def test_zero_rate(self):
        """Test with zero rate."""
        result = simple_interest(10000, 0, 5)
        self.assertEqual(result.total_amount, 10000)
        self.assertEqual(result.total_interest, 0)
    
    def test_zero_time(self):
        """Test with zero time."""
        result = simple_interest(10000, 0.08, 0)
        self.assertEqual(result.total_amount, 10000)


class TestSIP(unittest.TestCase):
    """Tests for SIP calculations."""
    
    def test_basic_sip(self):
        """Test basic SIP calculation."""
        result = sip_returns(10000, 0.12, 10)
        self.assertEqual(result.total_invested, 10000 * 12 * 10)
        self.assertTrue(result.maturity_value > result.total_invested)
        self.assertTrue(result.total_returns > 0)
    
    def test_zero_rate_sip(self):
        """Test SIP with zero return rate."""
        result = sip_returns(10000, 0, 10)
        self.assertEqual(result.maturity_value, result.total_invested)
        self.assertEqual(result.total_returns, 0)
    
    def test_sip_step_up(self):
        """Test step-up SIP."""
        result = sip_step_up(10000, 0.1, 0.12, 10)
        # Total invested should be more than regular SIP
        self.assertTrue(result['total_invested'] > 10000 * 12 * 10)
        self.assertTrue(result['maturity_value'] > result['total_invested'])
        self.assertEqual(len(result['yearly_breakdown']), 10)
    
    def test_sip_step_up_yearly_increase(self):
        """Test that yearly investments increase."""
        result = sip_step_up(10000, 0.1, 0.12, 5)
        breakdown = result['yearly_breakdown']
        for i in range(1, len(breakdown)):
            self.assertTrue(
                breakdown[i]['monthly_investment'] > breakdown[i-1]['monthly_investment']
            )


class TestCAGR(unittest.TestCase):
    """Tests for CAGR calculations."""
    
    def test_basic_cagr(self):
        """Test basic CAGR calculation."""
        # 10000 to 20000 in 5 years
        rate = cagr(10000, 20000, 5)
        # CAGR = (20000/10000)^(1/5) - 1
        expected = math.pow(2, 1/5) - 1
        self.assertAlmostEqual(rate, expected, places=4)
    
    def test_cagr_from_returns(self):
        """Test CAGR from list of returns."""
        returns = [0.10, 0.15, -0.05, 0.20]
        rate = cagr_from_returns(returns)
        # Total growth = 1.1 * 1.15 * 0.95 * 1.2
        total = 1.1 * 1.15 * 0.95 * 1.2
        expected = math.pow(total, 1/4) - 1
        self.assertAlmostEqual(rate, expected, places=4)
    
    def test_cagr_zero_growth(self):
        """Test CAGR with no growth."""
        rate = cagr(10000, 10000, 5)
        self.assertEqual(rate, 0)
    
    def test_cagr_negative(self):
        """Test CAGR with loss."""
        rate = cagr(10000, 8000, 2)
        self.assertTrue(rate < 0)
    
    def test_cagr_invalid_values(self):
        """Test CAGR with invalid values."""
        with self.assertRaises(ValueError):
            cagr(0, 20000, 5)
        with self.assertRaises(ValueError):
            cagr(10000, 20000, 0)


class TestPresentFutureValue(unittest.TestCase):
    """Tests for present and future value calculations."""
    
    def test_present_value(self):
        """Test present value calculation."""
        pv = present_value(100000, 0.08, 5)
        # PV = 100000 / (1.08)^5
        expected = 100000 / math.pow(1.08, 5)
        self.assertAlmostEqual(pv, expected, places=1)
    
    def test_future_value(self):
        """Test future value calculation."""
        fv = future_value(10000, 0.08, 5)
        # FV = 10000 * (1.08)^5
        expected = 10000 * math.pow(1.08, 5)
        self.assertAlmostEqual(fv, expected, places=1)
    
    def test_pv_fv_inverse(self):
        """Test that PV and FV are inverse operations."""
        pv = present_value(100000, 0.08, 5)
        fv = future_value(pv, 0.08, 5)
        self.assertAlmostEqual(fv, 100000, places=0)
    
    def test_present_value_annuity(self):
        """Test present value of annuity."""
        pv = present_value_annuity(1000, 0.05, 10)
        # PV = 1000 * [1 - (1.05)^-10] / 0.05
        expected = 1000 * (1 - math.pow(1.05, -10)) / 0.05
        self.assertAlmostEqual(pv, expected, places=1)
    
    def test_annuity_zero_rate(self):
        """Test annuity with zero rate."""
        pv = present_value_annuity(1000, 0, 10)
        self.assertEqual(pv, 10000)


class TestROI(unittest.TestCase):
    """Tests for ROI calculations."""
    
    def test_basic_roi(self):
        """Test basic ROI calculation."""
        result = roi(10000, 15000)
        # ROI = (15000 - 10000) / 10000 = 0.5
        self.assertEqual(result, 0.5)
    
    def test_negative_roi(self):
        """Test negative ROI (loss)."""
        result = roi(10000, 8000)
        # ROI = (8000 - 10000) / 10000 = -0.2
        self.assertEqual(result, -0.2)
    
    def test_zero_roi(self):
        """Test zero ROI."""
        result = roi(10000, 10000)
        self.assertEqual(result, 0)
    
    def test_annualized_roi(self):
        """Test annualized ROI."""
        result = annualized_roi(10000, 12000, 180)
        # About 6 months, should be around 44.6% annualized
        self.assertTrue(result > 0.4 and result < 0.5)
    
    def test_roi_zero_investment(self):
        """Test ROI with zero investment raises error."""
        with self.assertRaises(ValueError):
            roi(0, 10000)


class TestIRRNPV(unittest.TestCase):
    """Tests for IRR and NPV calculations."""
    
    def test_basic_irr(self):
        """Test basic IRR calculation."""
        # Investment of 1000, returns of 300 for 5 years
        rate = irr([-1000, 300, 300, 300, 300, 300])
        # Should be around 15.2%
        self.assertTrue(0.14 < rate < 0.16)
    
    def test_irr_with_profit(self):
        """Test IRR with profitable investment."""
        # Investment of 100, return 120 in one year
        rate = irr([-100, 120])
        self.assertAlmostEqual(rate, 0.2, places=2)
    
    def test_npv_positive(self):
        """Test NPV with positive cash flows."""
        npv_value = npv([-1000, 300, 300, 300, 300, 300], 0.1)
        # NPV should be positive at 10% discount rate
        self.assertTrue(npv_value > 0)
    
    def test_npv_at_irr(self):
        """Test NPV at IRR rate should be ~0."""
        cash_flows = [-1000, 300, 300, 300, 300, 300]
        irr_rate = irr(cash_flows)
        npv_value = npv(cash_flows, irr_rate)
        self.assertAlmostEqual(npv_value, 0, places=1)


class TestPaybackPeriod(unittest.TestCase):
    """Tests for payback period calculations."""
    
    def test_basic_payback(self):
        """Test basic payback period."""
        # 1000 investment, 300/year
        period = payback_period(1000, [300, 300, 300, 300])
        # After 3 years: 900 recovered, need 100 more
        # 100/300 = 0.33 more in year 4
        self.assertAlmostEqual(period, 3.33, places=1)
    
    def test_exact_payback(self):
        """Test exact payback period."""
        period = payback_period(1000, [500, 500])
        self.assertEqual(period, 2)
    
    def test_payback_not_achieved(self):
        """Test when payback is not achieved."""
        period = payback_period(1000, [100, 100, 100])
        self.assertEqual(period, float('inf'))
    
    def test_discounted_payback(self):
        """Test discounted payback period."""
        period = discounted_payback_period(1000, [300, 400, 400, 200], 0.1)
        # Should be longer than regular payback
        regular = payback_period(1000, [300, 400, 400, 200])
        self.assertTrue(period >= regular)


class TestLoanCalculations(unittest.TestCase):
    """Tests for loan calculations."""
    
    def test_monthly_payment(self):
        """Test monthly loan payment."""
        payment = loan_payment(100000, 0.06, 30)
        # Standard mortgage formula
        self.assertTrue(590 < payment < 610)
    
    def test_zero_interest_loan(self):
        """Test loan with zero interest."""
        payment = loan_payment(12000, 0, 1)
        self.assertEqual(payment, 1000)  # 12000 / 12 months
    
    def test_amortization_schedule(self):
        """Test amortization schedule generation."""
        schedule = amortization_schedule(100000, 0.06, 1)
        self.assertEqual(len(schedule), 12)
        
        # First payment should have more interest than last
        self.assertTrue(schedule[0].interest > schedule[-1].interest)
        
        # All payments should be equal
        for entry in schedule:
            self.assertAlmostEqual(entry.payment, schedule[0].payment, places=2)
    
    def test_amortization_final_balance(self):
        """Test that final balance in amortization is near zero."""
        schedule = amortization_schedule(10000, 0.12, 1)
        self.assertAlmostEqual(schedule[-1].balance, 0, places=1)


class TestInvestmentComparison(unittest.TestCase):
    """Tests for investment comparison."""
    
    def test_compare_investments(self):
        """Test investment comparison."""
        investments = [
            {'name': 'Stock A', 'initial': 10000, 'final': 15000, 'years': 3},
            {'name': 'Stock B', 'initial': 10000, 'final': 14000, 'years': 2}
        ]
        result = compare_investments(investments)
        
        self.assertEqual(len(result['rankings']), 2)
        self.assertEqual(result['winner']['name'], 'Stock B')  # Higher CAGR
    
    def test_compare_with_loss(self):
        """Test comparison with loss."""
        investments = [
            {'name': 'Stock A', 'initial': 10000, 'final': 12000, 'years': 2},
            {'name': 'Stock B', 'initial': 10000, 'final': 9000, 'years': 2}
        ]
        result = compare_investments(investments)
        
        self.assertTrue(result['rankings'][0]['roi'] > result['rankings'][1]['roi'])


class TestInflationAdjustedReturn(unittest.TestCase):
    """Tests for inflation-adjusted return."""
    
    def test_inflation_adjusted(self):
        """Test inflation-adjusted return calculation."""
        real = inflation_adjusted_return(0.10, 0.03)
        # Real = (1.10 / 1.03) - 1 ≈ 0.068
        self.assertAlmostEqual(real, 0.068, places=3)
    
    def test_high_inflation(self):
        """Test with high inflation."""
        real = inflation_adjusted_return(0.05, 0.07)
        # Real return should be negative
        self.assertTrue(real < 0)


class TestRuleOf72(unittest.TestCase):
    """Tests for Rule of 72."""
    
    def test_rule_of_72(self):
        """Test Rule of 72 calculation."""
        years = rule_of_72(0.08)
        self.assertEqual(years, 9.0)  # 72/8 = 9
    
    def test_rule_of_69(self):
        """Test Rule of 69 (more precise)."""
        years = rule_of_69(0.08)
        self.assertAlmostEqual(years, math.log(2) / math.log(1.08), places=2)
    
    def test_rule_of_69_continuous(self):
        """Test Rule of 69 with continuous compounding."""
        years = rule_of_69(0.08, continuous=True)
        self.assertAlmostEqual(years, math.log(2) / 0.08, places=2)
    
    def test_zero_rate_raises(self):
        """Test that zero rate raises error."""
        with self.assertRaises(ValueError):
            rule_of_72(0)


class TestTimeValue(unittest.TestCase):
    """Tests for time value calculations."""
    
    def test_time_to_target(self):
        """Test time to reach target value."""
        years = time_to_target(10000, 20000, 0.08)
        # Should be about 9 years
        self.assertTrue(8 < years < 10)
    
    def test_required_rate(self):
        """Test required rate calculation."""
        rate = required_rate(10000, 20000, 5)
        # Should match CAGR calculation
        expected = cagr(10000, 20000, 5)
        self.assertEqual(rate, expected)
    
    def test_future_value_with_inflation(self):
        """Test future value with inflation adjustment."""
        result = future_value_with_inflation(10000, 0.08, 0.03, 10)
        
        self.assertTrue(result['nominal_value'] > result['real_value'])
        self.assertTrue(result['real_rate'] < 0.08)
        self.assertTrue(result['inflation_impact'] > 0)


class TestDepreciation(unittest.TestCase):
    """Tests for depreciation calculations."""
    
    def test_straight_line(self):
        """Test straight-line depreciation."""
        result = straight_line_depreciation(10000, 1000, 5)
        
        self.assertEqual(result['annual_depreciation'], 1800)
        self.assertEqual(result['total_depreciation'], 9000)
        self.assertEqual(len(result['schedule']), 5)
        
        # Final book value should be salvage value
        self.assertEqual(result['schedule'][-1]['book_value'], 1000)
    
    def test_declining_balance(self):
        """Test declining balance depreciation."""
        schedule = declining_balance_depreciation(10000, 1000, 5)
        
        # Depreciation should decrease over time
        self.assertTrue(schedule[0]['depreciation'] > schedule[1]['depreciation'])
        
        # Book value should not go below salvage
        for entry in schedule:
            self.assertTrue(entry['book_value'] >= 1000)
    
    def test_zero_salvage(self):
        """Test with zero salvage value."""
        result = straight_line_depreciation(10000, 0, 5)
        self.assertEqual(result['annual_depreciation'], 2000)


class TestEdgeCases(unittest.TestCase):
    """Tests for edge cases and boundary conditions."""
    
    def test_very_small_principal(self):
        """Test with very small principal."""
        result = compound_interest(0.01, 0.08, 1)
        self.assertTrue(result.total_amount > 0)
    
    def test_very_long_period(self):
        """Test with very long time period."""
        result = compound_interest(1000, 0.05, 100)
        self.assertTrue(result.total_amount > result.principal * 100)
    
    def test_very_high_rate(self):
        """Test with high interest rate."""
        result = compound_interest(1000, 1.0, 5)  # 100% interest
        self.assertTrue(result.total_amount > 1000)
    
    def test_fractional_years(self):
        """Test with fractional years."""
        result = compound_interest(10000, 0.08, 2.5)
        self.assertTrue(result.total_amount > 10000)
    
    def test_many_cash_flows(self):
        """Test IRR with many cash flows."""
        cash_flows = [-10000] + [1000] * 20
        rate = irr(cash_flows)
        self.assertTrue(-1 < rate < 1)


class TestDataClasses(unittest.TestCase):
    """Tests for data classes."""
    
    def test_investment_result(self):
        """Test InvestmentResult dataclass."""
        result = InvestmentResult(
            principal=10000,
            total_amount=15000,
            total_interest=5000,
            effective_rate=0.08
        )
        self.assertEqual(result.principal, 10000)
        self.assertEqual(result.total_amount, 15000)
    
    def test_sip_result(self):
        """Test SIPResult dataclass."""
        result = SIPResult(
            total_invested=1200000,
            maturity_value=2000000,
            total_returns=800000,
            annualized_return=0.10
        )
        self.assertEqual(result.total_invested, 1200000)
    
    def test_amortization_entry(self):
        """Test AmortizationEntry dataclass."""
        entry = AmortizationEntry(
            period=1,
            payment=1000,
            principal=800,
            interest=200,
            balance=92000
        )
        self.assertEqual(entry.period, 1)
        self.assertEqual(entry.payment, 1000)


if __name__ == '__main__':
    unittest.main(verbosity=2)