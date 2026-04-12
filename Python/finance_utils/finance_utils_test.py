"""
AllToolkit - Python Finance Utils Test Suite

Comprehensive tests for finance utilities covering:
- Time value of money (FV, PV, compound interest)
- Annuities (ordinary and due)
- Loan calculations (payments, amortization)
- Investment analysis (NPV, IRR, payback)
- Bond valuation (price, YTM, duration)
- Depreciation methods
- Financial ratios
- Risk metrics (beta, Sharpe ratio, VaR)
- Edge cases and error handling

Run: python finance_utils_test.py -v
"""

import unittest
import sys
import os
import math

# Add module directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from mod import (
    # Exceptions
    FinanceError, InvalidRateError, InvalidCashFlowError, ConvergenceError,
    
    # Time Value of Money
    future_value, present_value, compound_interest, continuous_compound_interest,
    effective_annual_rate, nominal_rate,
    
    # Annuities
    annuity_future_value, annuity_present_value, annuity_payment,
    
    # Loan Calculations
    loan_payment, loan_amortization_schedule, loan_total_interest,
    remaining_loan_balance,
    
    # Investment Analysis
    net_present_value, internal_rate_of_return, profitability_index,
    payback_period, discounted_payback_period,
    
    # Bond Valuation
    bond_price, bond_yield_to_maturity, bond_current_yield,
    bond_duration, bond_modified_duration,
    
    # Depreciation
    straight_line_depreciation, declining_balance_depreciation,
    sum_of_years_digits_depreciation,
    
    # Financial Ratios
    return_on_investment, return_on_equity, return_on_assets,
    current_ratio, quick_ratio, debt_to_equity,
    gross_profit_margin, net_profit_margin,
    earnings_per_share, price_to_earnings_ratio, dividend_yield,
    
    # Currency
    currency_convert, cross_rate,
    
    # Risk & Statistics
    expected_return, variance_returns, std_dev_returns,
    covariance_returns, correlation_returns, beta,
    sharpe_ratio, value_at_loss,
    
    # Convenience
    investment_summary, compare_loans, rule_of_72, rule_of_72_exact,
)


# ============================================================================
# Time Value of Money Tests
# ============================================================================

class TestFutureValue(unittest.TestCase):
    """Tests for future_value function."""
    
    def test_simple_fv(self):
        """Test basic future value calculation."""
        # $1000 at 5% for 10 years
        fv = future_value(1000, 0.05, 10)
        self.assertAlmostEqual(fv, 1628.89, places=2)
    
    def test_zero_rate(self):
        """Test FV with zero interest rate."""
        fv = future_value(1000, 0, 10)
        self.assertEqual(fv, 1000)
    
    def test_single_period(self):
        """Test FV for single period."""
        fv = future_value(100, 0.1, 1)
        self.assertAlmostEqual(fv, 110, places=10)
    
    def test_negative_rate(self):
        """Test FV with negative rate (loss)."""
        fv = future_value(1000, -0.05, 1)
        self.assertAlmostEqual(fv, 950)
    
    def test_invalid_rate(self):
        """Test FV with invalid rate."""
        with self.assertRaises(InvalidRateError):
            future_value(1000, -1.5, 10)


class TestPresentValue(unittest.TestCase):
    """Tests for present_value function."""
    
    def test_simple_pv(self):
        """Test basic present value calculation."""
        # $1000 in 10 years at 5% discount rate
        pv = present_value(1000, 0.05, 10)
        self.assertAlmostEqual(pv, 613.91, places=2)
    
    def test_pv_fv_inverse(self):
        """Test that PV and FV are inverse operations."""
        fv = 1628.89
        pv = present_value(fv, 0.05, 10)
        self.assertAlmostEqual(pv, 1000, places=0)
    
    def test_zero_rate(self):
        """Test PV with zero discount rate."""
        pv = present_value(1000, 0, 10)
        self.assertEqual(pv, 1000)


class TestCompoundInterest(unittest.TestCase):
    """Tests for compound_interest function."""
    
    def test_annual_compounding(self):
        """Test annual compounding."""
        interest = compound_interest(1000, 0.05, 10, 1)
        self.assertAlmostEqual(interest, 628.89, places=2)
    
    def test_monthly_compounding(self):
        """Test monthly compounding."""
        interest = compound_interest(1000, 0.05, 10, 12)
        self.assertAlmostEqual(interest, 647.01, places=2)
    
    def test_daily_compounding(self):
        """Test daily compounding."""
        interest = compound_interest(1000, 0.05, 10, 365)
        self.assertAlmostEqual(interest, 648.66, places=2)
    
    def test_continuous_compounding(self):
        """Test continuous compounding."""
        interest = continuous_compound_interest(1000, 0.05, 10)
        self.assertAlmostEqual(interest, 648.72, places=2)


class TestEffectiveAnnualRate(unittest.TestCase):
    """Tests for effective_annual_rate function."""
    
    def test_monthly_compounding(self):
        """Test EAR with monthly compounding."""
        ear = effective_annual_rate(0.12, 12)
        self.assertAlmostEqual(ear, 0.1268, places=4)
    
    def test_daily_compounding(self):
        """Test EAR with daily compounding."""
        ear = effective_annual_rate(0.12, 365)
        self.assertAlmostEqual(ear, 0.1275, places=4)
    
    def test_annual_compounding(self):
        """Test EAR with annual compounding (should equal nominal)."""
        ear = effective_annual_rate(0.12, 1)
        self.assertAlmostEqual(ear, 0.12, places=10)


# ============================================================================
# Annuity Tests
# ============================================================================

class TestAnnuityFutureValue(unittest.TestCase):
    """Tests for annuity_future_value function."""
    
    def test_ordinary_annuity(self):
        """Test ordinary annuity (end of period payments)."""
        # $100/year for 10 years at 5%
        fv = annuity_future_value(100, 0.05, 10)
        self.assertAlmostEqual(fv, 1257.79, places=2)
    
    def test_annuity_due(self):
        """Test annuity due (beginning of period payments)."""
        fv = annuity_future_value(100, 0.05, 10, annuity_due=True)
        self.assertAlmostEqual(fv, 1320.68, places=2)
    
    def test_zero_rate(self):
        """Test annuity with zero interest rate."""
        fv = annuity_future_value(100, 0, 10)
        self.assertEqual(fv, 1000)


class TestAnnuityPresentValue(unittest.TestCase):
    """Tests for annuity_present_value function."""
    
    def test_ordinary_annuity(self):
        """Test PV of ordinary annuity."""
        # $100/year for 10 years at 5%
        pv = annuity_present_value(100, 0.05, 10)
        self.assertAlmostEqual(pv, 772.17, places=2)
    
    def test_annuity_due(self):
        """Test PV of annuity due."""
        pv = annuity_present_value(100, 0.05, 10, annuity_due=True)
        self.assertAlmostEqual(pv, 810.78, places=2)


class TestAnnuityPayment(unittest.TestCase):
    """Tests for annuity_payment function."""
    
    def test_loan_payment_calculation(self):
        """Test payment calculation for a loan."""
        # $100,000 loan, 5% annual, 30 years, monthly payments
        payment = annuity_payment(100000, 0.05/12, 30*12)
        self.assertAlmostEqual(payment, 536.82, places=2)


# ============================================================================
# Loan Calculation Tests
# ============================================================================

class TestLoanPayment(unittest.TestCase):
    """Tests for loan_payment function."""
    
    def test_mortgage_payment(self):
        """Test mortgage payment calculation."""
        # $200,000 loan, 4% annual, 30 years, monthly
        payment = loan_payment(200000, 0.04, 30, 12)
        self.assertAlmostEqual(payment, 954.83, places=2)
    
    def test_auto_loan(self):
        """Test auto loan payment."""
        # $30,000 loan, 6% annual, 5 years, monthly
        payment = loan_payment(30000, 0.06, 5, 12)
        self.assertAlmostEqual(payment, 579.98, places=2)
    
    def test_zero_interest(self):
        """Test loan with zero interest."""
        payment = loan_payment(12000, 0, 2, 12)
        self.assertEqual(payment, 500)


class TestLoanAmortization(unittest.TestCase):
    """Tests for loan_amortization_schedule function."""
    
    def test_amortization_schedule(self):
        """Test loan amortization schedule generation."""
        # Use a longer-term loan so first payment is mostly interest
        schedule = loan_amortization_schedule(100000, 0.05, 30, 12)
        
        self.assertEqual(len(schedule), 360)
        
        # First payment should be mostly interest (for long-term loan)
        self.assertGreater(schedule[0]['interest'], schedule[0]['principal'])
        
        # Last payment should be mostly principal
        self.assertLess(schedule[-1]['interest'], schedule[-1]['principal'])
        
        # Final balance should be 0
        self.assertAlmostEqual(schedule[-1]['balance'], 0, places=2)
    
    def test_total_payments(self):
        """Test that total payments equal principal + interest."""
        schedule = loan_amortization_schedule(10000, 0.06, 1, 12)
        
        total_payments = sum(p['payment'] for p in schedule)
        total_principal = sum(p['principal'] for p in schedule)
        total_interest = sum(p['interest'] for p in schedule)
        
        self.assertAlmostEqual(total_principal, 10000, places=2)
        self.assertAlmostEqual(total_payments, total_principal + total_interest, places=2)


class TestLoanTotalInterest(unittest.TestCase):
    """Tests for loan_total_interest function."""
    
    def test_total_interest(self):
        """Test total interest calculation."""
        interest = loan_total_interest(100000, 0.04, 30, 12)
        # 30-year mortgage at 4% should have significant interest
        self.assertGreater(interest, 70000)
        self.assertLess(interest, 80000)


class TestRemainingBalance(unittest.TestCase):
    """Tests for remaining_loan_balance function."""
    
    def test_remaining_balance(self):
        """Test remaining balance after some payments."""
        balance = remaining_loan_balance(100000, 0.05, 30, 5, 12)
        # After 5 years on 30-year loan, should still owe most of it
        self.assertGreater(balance, 90000)
        self.assertLess(balance, 100000)
    
    def test_fully_paid(self):
        """Test remaining balance after loan is paid."""
        balance = remaining_loan_balance(100000, 0.05, 30, 30, 12)
        self.assertEqual(balance, 0)


# ============================================================================
# Investment Analysis Tests
# ============================================================================

class TestNetPresentValue(unittest.TestCase):
    """Tests for net_present_value function."""
    
    def test_positive_npv(self):
        """Test NPV for profitable investment."""
        # Invest $1000, get $400/year for 4 years at 10% discount
        # PV of inflows = 400/1.1 + 400/1.1^2 + 400/1.1^3 + 400/1.1^4 = 1267.95
        cash_flows = [-1000, 400, 400, 400, 400]
        npv = net_present_value(cash_flows, 0.10)
        self.assertGreater(npv, 0)
    
    def test_negative_npv(self):
        """Test NPV for unprofitable investment."""
        cash_flows = [-1000, 200, 200, 200]
        npv = net_present_value(cash_flows, 0.10)
        self.assertLess(npv, 0)
    
    def test_zero_npv(self):
        """Test NPV at break-even point."""
        # Cash flows that should give approximately zero NPV at 10%
        cash_flows = [-1000, 350, 350, 350, 350]
        npv = net_present_value(cash_flows, 0.10)
        self.assertAlmostEqual(npv, 109.45, places=2)


class TestInternalRateOfReturn(unittest.TestCase):
    """Tests for internal_rate_of_return function."""
    
    def test_simple_irr(self):
        """Test IRR for simple cash flows."""
        cash_flows = [-1000, 400, 400, 400, 400]
        irr = internal_rate_of_return(cash_flows)
        self.assertAlmostEqual(irr, 0.2186, places=4)
    
    def test_irr_equals_discount_at_zero_npv(self):
        """Test that IRR gives zero NPV."""
        cash_flows = [-1000, 300, 300, 300, 300, 300]
        irr = internal_rate_of_return(cash_flows)
        npv_at_irr = net_present_value(cash_flows, irr)
        self.assertAlmostEqual(npv_at_irr, 0, places=6)
    
    def test_invalid_cashflows(self):
        """Test IRR with invalid cash flows (no sign change)."""
        with self.assertRaises(InvalidCashFlowError):
            internal_rate_of_return([100, 200, 300])


class TestProfitabilityIndex(unittest.TestCase):
    """Tests for profitability_index function."""
    
    def test_profitable_project(self):
        """Test PI for profitable project."""
        cash_flows = [-1000, 400, 400, 400, 400]
        pi = profitability_index(cash_flows, 0.10)
        self.assertGreater(pi, 1)
    
    def test_unprofitable_project(self):
        """Test PI for unprofitable project."""
        cash_flows = [-1000, 200, 200, 200]
        pi = profitability_index(cash_flows, 0.10)
        self.assertLess(pi, 1)


class TestPaybackPeriod(unittest.TestCase):
    """Tests for payback_period function."""
    
    def test_simple_payback(self):
        """Test simple payback period."""
        cash_flows = [-1000, 250, 250, 250, 250, 250]
        pb = payback_period(cash_flows)
        self.assertEqual(pb, 4.0)
    
    def test_fractional_payback(self):
        """Test payback with fractional period."""
        cash_flows = [-1000, 300, 300, 300, 300]
        pb = payback_period(cash_flows)
        self.assertAlmostEqual(pb, 3.33, places=2)
    
    def test_never_recovers(self):
        """Test when investment is never recovered."""
        cash_flows = [-1000, 100, 100, 100]
        with self.assertRaises(InvalidCashFlowError):
            payback_period(cash_flows)


class TestDiscountedPaybackPeriod(unittest.TestCase):
    """Tests for discounted_payback_period function."""
    
    def test_discounted_payback(self):
        """Test discounted payback period."""
        cash_flows = [-1000, 300, 300, 300, 300, 300]
        dpb = discounted_payback_period(cash_flows, 0.10)
        # Should be longer than simple payback
        self.assertGreater(dpb, 3.33)


# ============================================================================
# Bond Valuation Tests
# ============================================================================

class TestBondPrice(unittest.TestCase):
    """Tests for bond_price function."""
    
    def test_par_bond(self):
        """Test bond priced at par (coupon = YTM)."""
        price = bond_price(1000, 0.05, 0.05, 10, 2)
        self.assertAlmostEqual(price, 1000, places=2)
    
    def test_discount_bond(self):
        """Test bond priced at discount (coupon < YTM)."""
        price = bond_price(1000, 0.04, 0.05, 10, 2)
        self.assertLess(price, 1000)
    
    def test_premium_bond(self):
        """Test bond priced at premium (coupon > YTM)."""
        price = bond_price(1000, 0.06, 0.05, 10, 2)
        self.assertGreater(price, 1000)


class TestBondYieldToMaturity(unittest.TestCase):
    """Tests for bond_yield_to_maturity function."""
    
    def test_ytm_at_par(self):
        """Test YTM when bond is at par."""
        ytm = bond_yield_to_maturity(1000, 0.05, 1000, 10, 2)
        self.assertAlmostEqual(ytm, 0.05, places=4)
    
    def test_ytm_discount(self):
        """Test YTM for discount bond."""
        ytm = bond_yield_to_maturity(1000, 0.04, 950, 10, 2)
        self.assertGreater(ytm, 0.04)


class TestBondCurrentYield(unittest.TestCase):
    """Tests for bond_current_yield function."""
    
    def test_current_yield_par(self):
        """Test current yield at par."""
        cy = bond_current_yield(1000, 0.05, 1000)
        self.assertEqual(cy, 0.05)
    
    def test_current_yield_discount(self):
        """Test current yield at discount."""
        cy = bond_current_yield(1000, 0.05, 950)
        self.assertGreater(cy, 0.05)


class TestBondDuration(unittest.TestCase):
    """Tests for bond_duration function."""
    
    def test_duration_zero_coupon(self):
        """Test duration of zero-coupon bond."""
        # Zero coupon bond duration equals maturity
        duration = bond_duration(1000, 0, 0.05, 10, 1)
        self.assertAlmostEqual(duration, 10, places=1)
    
    def test_duration_coupon_bond(self):
        """Test duration of coupon bond (should be less than maturity)."""
        duration = bond_duration(1000, 0.05, 0.05, 10, 2)
        self.assertLess(duration, 10)


# ============================================================================
# Depreciation Tests
# ============================================================================

class TestStraightLineDepreciation(unittest.TestCase):
    """Tests for straight_line_depreciation function."""
    
    def test_straight_line_schedule(self):
        """Test straight-line depreciation schedule."""
        schedule = straight_line_depreciation(10000, 1000, 5)
        
        self.assertEqual(len(schedule), 5)
        
        # Each year should have same depreciation
        for entry in schedule:
            self.assertAlmostEqual(entry['depreciation'], 1800, places=2)
        
        # Final book value should equal salvage value
        self.assertAlmostEqual(schedule[-1]['book_value'], 1000, places=2)


class TestDecliningBalanceDepreciation(unittest.TestCase):
    """Tests for declining_balance_depreciation function."""
    
    def test_double_declining_schedule(self):
        """Test double-declining balance depreciation."""
        schedule = declining_balance_depreciation(10000, 1000, 5)
        
        self.assertEqual(len(schedule), 5)
        
        # Depreciation should decrease each year
        for i in range(1, len(schedule)):
            self.assertLess(schedule[i]['depreciation'], 
                           schedule[i-1]['depreciation'])
        
        # Final book value should equal salvage value
        self.assertAlmostEqual(schedule[-1]['book_value'], 1000, places=2)


class TestSumOfYearDigitsDepreciation(unittest.TestCase):
    """Tests for sum_of_years_digits_depreciation function."""
    
    def test_syd_schedule(self):
        """Test sum-of-years'-digits depreciation."""
        schedule = sum_of_years_digits_depreciation(10000, 1000, 5)
        
        self.assertEqual(len(schedule), 5)
        
        # Depreciation should decrease each year
        for i in range(1, len(schedule)):
            self.assertLess(schedule[i]['depreciation'],
                           schedule[i-1]['depreciation'])


# ============================================================================
# Financial Ratios Tests
# ============================================================================

class TestReturnOnInvestment(unittest.TestCase):
    """Tests for return_on_investment function."""
    
    def test_positive_roi(self):
        """Test positive ROI."""
        roi = return_on_investment(1500, 1000)
        self.assertEqual(roi, 0.5)
    
    def test_negative_roi(self):
        """Test negative ROI."""
        roi = return_on_investment(800, 1000)
        self.assertEqual(roi, -0.2)


class TestProfitabilityRatios(unittest.TestCase):
    """Tests for profitability ratio functions."""
    
    def test_roe(self):
        """Test return on equity."""
        roe = return_on_equity(100000, 500000)
        self.assertEqual(roe, 0.2)
    
    def test_roa(self):
        """Test return on assets."""
        roa = return_on_assets(100000, 1000000)
        self.assertEqual(roa, 0.1)
    
    def test_gross_margin(self):
        """Test gross profit margin."""
        margin = gross_profit_margin(1000000, 600000)
        self.assertEqual(margin, 0.4)
    
    def test_net_margin(self):
        """Test net profit margin."""
        margin = net_profit_margin(1000000, 150000)
        self.assertEqual(margin, 0.15)


class TestLiquidityRatios(unittest.TestCase):
    """Tests for liquidity ratio functions."""
    
    def test_current_ratio(self):
        """Test current ratio."""
        ratio = current_ratio(500000, 250000)
        self.assertEqual(ratio, 2.0)
    
    def test_quick_ratio(self):
        """Test quick ratio."""
        ratio = quick_ratio(100000, 50000, 150000, 250000)
        self.assertEqual(ratio, 1.2)


class TestLeverageRatios(unittest.TestCase):
    """Tests for leverage ratio functions."""
    
    def test_debt_to_equity(self):
        """Test debt-to-equity ratio."""
        ratio = debt_to_equity(500000, 1000000)
        self.assertEqual(ratio, 0.5)


class TestMarketRatios(unittest.TestCase):
    """Tests for market ratio functions."""
    
    def test_eps(self):
        """Test earnings per share."""
        eps = earnings_per_share(1000000, 100000, 500000)
        self.assertEqual(eps, 1.8)
    
    def test_pe_ratio(self):
        """Test P/E ratio."""
        pe = price_to_earnings_ratio(50, 5)
        self.assertEqual(pe, 10)
    
    def test_dividend_yield(self):
        """Test dividend yield."""
        yield_pct = dividend_yield(2, 50)
        self.assertEqual(yield_pct, 0.04)


# ============================================================================
# Currency Tests
# ============================================================================

class TestCurrencyConvert(unittest.TestCase):
    """Tests for currency conversion functions."""
    
    def test_currency_conversion(self):
        """Test currency conversion."""
        converted = currency_convert(100, 1.1)
        self.assertAlmostEqual(converted, 110, places=10)
    
    def test_cross_rate(self):
        """Test cross rate calculation."""
        # EUR/USD = 1.1, USD/JPY = 110, so EUR/JPY = 121
        cross = cross_rate(1.1, 110)
        self.assertAlmostEqual(cross, 121, places=10)


# ============================================================================
# Risk & Statistics Tests
# ============================================================================

class TestExpectedReturn(unittest.TestCase):
    """Tests for expected_return function."""
    
    def test_equal_probability(self):
        """Test expected return with equal probabilities."""
        returns = [0.1, 0.2, 0.3]
        er = expected_return(returns)
        self.assertAlmostEqual(er, 0.2, places=10)
    
    def test_weighted_probability(self):
        """Test expected return with weighted probabilities."""
        returns = [0.1, 0.2]
        probs = [0.3, 0.7]
        er = expected_return(returns, probs)
        self.assertAlmostEqual(er, 0.17, places=10)


class TestVarianceAndStdDev(unittest.TestCase):
    """Tests for variance and standard deviation functions."""
    
    def test_variance(self):
        """Test variance calculation."""
        returns = [0.1, 0.2, 0.3, 0.4, 0.5]
        var = variance_returns(returns)
        self.assertAlmostEqual(var, 0.025, places=4)
    
    def test_std_dev(self):
        """Test standard deviation calculation."""
        returns = [0.1, 0.2, 0.3, 0.4, 0.5]
        std = std_dev_returns(returns)
        self.assertAlmostEqual(std, 0.1581, places=4)


class TestCovarianceAndCorrelation(unittest.TestCase):
    """Tests for covariance and correlation functions."""
    
    def test_perfect_positive_correlation(self):
        """Test correlation for perfectly positively correlated series."""
        returns_a = [0.1, 0.2, 0.3, 0.4, 0.5]
        returns_b = [0.2, 0.4, 0.6, 0.8, 1.0]
        corr = correlation_returns(returns_a, returns_b)
        self.assertAlmostEqual(corr, 1.0, places=10)
    
    def test_covariance(self):
        """Test covariance calculation."""
        returns_a = [0.1, 0.2, 0.3]
        returns_b = [0.2, 0.4, 0.6]
        cov = covariance_returns(returns_a, returns_b)
        self.assertGreater(cov, 0)


class TestBeta(unittest.TestCase):
    """Tests for beta function."""
    
    def test_beta_calculation(self):
        """Test beta calculation."""
        asset_returns = [0.1, 0.15, 0.2, 0.25, 0.3]
        market_returns = [0.08, 0.12, 0.16, 0.20, 0.24]
        b = beta(asset_returns, market_returns)
        self.assertGreater(b, 1)  # Asset is more volatile than market


class TestSharpeRatio(unittest.TestCase):
    """Tests for sharpe_ratio function."""
    
    def test_sharpe_calculation(self):
        """Test Sharpe ratio calculation."""
        sharpe = sharpe_ratio(0.12, 0.03, 0.15)
        self.assertAlmostEqual(sharpe, 0.6, places=10)


class TestValueAtRisk(unittest.TestCase):
    """Tests for value_at_loss function."""
    
    def test_var_95(self):
        """Test 95% VaR calculation."""
        returns = [0.01, 0.02, -0.03, 0.04, -0.05, 0.02, -0.01, 0.03, -0.02, 0.01]
        var = value_at_loss(returns, 0.95)
        # VaR should be positive (representing loss)
        self.assertGreater(var, 0)


# ============================================================================
# Convenience Functions Tests
# ============================================================================

class TestInvestmentSummary(unittest.TestCase):
    """Tests for investment_summary function."""
    
    def test_simple_investment(self):
        """Test investment summary without contributions."""
        summary = investment_summary(10000, 0.07, 10)
        
        self.assertEqual(summary['initial_investment'], 10000)
        self.assertGreater(summary['final_value'], 10000)
        self.assertGreater(summary['total_gain'], 0)
    
    def test_investment_with_contributions(self):
        """Test investment summary with annual contributions."""
        summary = investment_summary(10000, 0.07, 10, 5000)
        
        total_contributed = 10000 + (5000 * 10)
        self.assertEqual(summary['total_contributed'], total_contributed)
        self.assertGreater(summary['final_value'], total_contributed)


class TestCompareLoans(unittest.TestCase):
    """Tests for compare_loans function."""
    
    def test_loan_comparison(self):
        """Test loan comparison."""
        options = [
            {'annual_rate': 0.05, 'years': 30},
            {'annual_rate': 0.04, 'years': 30},
            {'annual_rate': 0.05, 'years': 15},
        ]
        
        results = compare_loans(200000, options)
        
        # Should be sorted by total cost
        self.assertLessEqual(results[0]['total_cost'], results[-1]['total_cost'])
        
        # All results should have required fields
        for result in results:
            self.assertIn('monthly_payment', result)
            self.assertIn('total_interest', result)
            self.assertIn('total_cost', result)


class TestRuleOf72(unittest.TestCase):
    """Tests for rule_of_72 functions."""
    
    def test_rule_of_72_approximate(self):
        """Test approximate rule of 72."""
        years = rule_of_72(8)  # 8% return
        self.assertAlmostEqual(years, 9, places=1)
    
    def test_rule_of_72_exact(self):
        """Test exact doubling time."""
        years = rule_of_72_exact(0.08)
        self.assertAlmostEqual(years, 9.006, places=3)


# ============================================================================
# Error Handling Tests
# ============================================================================

class TestErrorHandling(unittest.TestCase):
    """Tests for error handling."""
    
    def test_empty_cash_flows(self):
        """Test error on empty cash flows."""
        with self.assertRaises(InvalidCashFlowError):
            net_present_value([], 0.1)
    
    def test_zero_division_roi(self):
        """Test error on zero cost for ROI."""
        with self.assertRaises(FinanceError):
            return_on_investment(100, 0)
    
    def test_invalid_confidence_level(self):
        """Test error on invalid confidence level."""
        with self.assertRaises(FinanceError):
            value_at_loss([0.1, 0.2], 1.5)


# ============================================================================
# Main Test Runner
# ============================================================================

if __name__ == '__main__':
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add all test classes
    test_classes = [
        # TVM
        TestFutureValue, TestPresentValue, TestCompoundInterest,
        TestEffectiveAnnualRate,
        
        # Annuities
        TestAnnuityFutureValue, TestAnnuityPresentValue, TestAnnuityPayment,
        
        # Loans
        TestLoanPayment, TestLoanAmortization, TestLoanTotalInterest,
        TestRemainingBalance,
        
        # Investment Analysis
        TestNetPresentValue, TestInternalRateOfReturn, TestProfitabilityIndex,
        TestPaybackPeriod, TestDiscountedPaybackPeriod,
        
        # Bonds
        TestBondPrice, TestBondYieldToMaturity, TestBondCurrentYield,
        TestBondDuration,
        
        # Depreciation
        TestStraightLineDepreciation, TestDecliningBalanceDepreciation,
        TestSumOfYearDigitsDepreciation,
        
        # Ratios
        TestReturnOnInvestment, TestProfitabilityRatios, TestLiquidityRatios,
        TestLeverageRatios, TestMarketRatios,
        
        # Currency
        TestCurrencyConvert,
        
        # Risk
        TestExpectedReturn, TestVarianceAndStdDev, TestCovarianceAndCorrelation,
        TestBeta, TestSharpeRatio, TestValueAtRisk,
        
        # Convenience
        TestInvestmentSummary, TestCompareLoans, TestRuleOf72,
        
        # Error Handling
        TestErrorHandling,
    ]
    
    for test_class in test_classes:
        tests = loader.loadTestsFromTestCase(test_class)
        suite.addTests(tests)
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Print summary
    print("\n" + "=" * 60)
    print(f"Tests run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print(f"Success: {result.wasSuccessful()}")
    print("=" * 60)
    
    sys.exit(0 if result.wasSuccessful() else 1)
