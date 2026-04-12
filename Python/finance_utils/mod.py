"""
AllToolkit - Python Finance Utilities

A zero-dependency, production-ready financial calculation module.
Provides time value of money, investment analysis, loan calculations,
bond valuation, depreciation, financial ratios, and more.
Built entirely with Python standard library.

Author: AllToolkit
License: MIT
"""

import math
from typing import List, Tuple, Optional, Dict, Any, Union
from datetime import date, timedelta


class FinanceError(Exception):
    """Base exception for finance operations."""
    pass


class InvalidRateError(FinanceError):
    """Raised when interest rate is invalid."""
    pass


class InvalidCashFlowError(FinanceError):
    """Raised when cash flow data is invalid."""
    pass


class ConvergenceError(FinanceError):
    """Raised when iterative calculation fails to converge."""
    pass


# ============================================================================
# Time Value of Money (TVM)
# ============================================================================

def future_value(present_value: float, rate: float, periods: int) -> float:
    """
    Calculate future value with compound interest.
    
    FV = PV × (1 + r)^n
    
    Args:
        present_value: Present value (initial investment)
        rate: Interest rate per period (as decimal, e.g., 0.05 for 5%)
        periods: Number of compounding periods
        
    Returns:
        Future value
        
    Raises:
        InvalidRateError: If rate is negative
    """
    if rate < -1:
        raise InvalidRateError("Interest rate must be >= -100%")
    if periods < 0:
        raise FinanceError("Periods must be non-negative")
    
    return present_value * ((1 + rate) ** periods)


def present_value(future_value: float, rate: float, periods: int) -> float:
    """
    Calculate present value (discount future value).
    
    PV = FV / (1 + r)^n
    
    Args:
        future_value: Future value
        rate: Discount rate per period (as decimal)
        periods: Number of periods
        
    Returns:
        Present value
        
    Raises:
        InvalidRateError: If rate is <= -1
    """
    if rate <= -1:
        raise InvalidRateError("Discount rate must be > -100%")
    if periods < 0:
        raise FinanceError("Periods must be non-negative")
    
    return future_value / ((1 + rate) ** periods)


def compound_interest(principal: float, rate: float, time: float, 
                      compounds_per_year: int = 1) -> float:
    """
    Calculate compound interest earned.
    
    A = P × (1 + r/n)^(n×t)
    Interest = A - P
    
    Args:
        principal: Initial principal amount
        rate: Annual interest rate (as decimal)
        time: Time in years
        compounds_per_year: Number of times interest compounds per year
        
    Returns:
        Interest earned (not total value)
        
    Raises:
        InvalidRateError: If rate is negative
    """
    if rate < 0:
        raise InvalidRateError("Interest rate must be non-negative")
    if compounds_per_year <= 0:
        raise FinanceError("Compounds per year must be positive")
    if time < 0:
        raise FinanceError("Time must be non-negative")
    
    amount = principal * ((1 + rate / compounds_per_year) ** (compounds_per_year * time))
    return amount - principal


def continuous_compound_interest(principal: float, rate: float, time: float) -> float:
    """
    Calculate interest with continuous compounding.
    
    A = P × e^(r×t)
    Interest = A - P
    
    Args:
        principal: Initial principal amount
        rate: Annual interest rate (as decimal)
        time: Time in years
        
    Returns:
        Interest earned
    """
    if rate < 0:
        raise InvalidRateError("Interest rate must be non-negative")
    if time < 0:
        raise FinanceError("Time must be non-negative")
    
    amount = principal * math.exp(rate * time)
    return amount - principal


def effective_annual_rate(nominal_rate: float, compounds_per_year: int) -> float:
    """
    Calculate effective annual rate (EAR) from nominal rate.
    
    EAR = (1 + r/n)^n - 1
    
    Args:
        nominal_rate: Nominal annual interest rate (as decimal)
        compounds_per_year: Number of compounding periods per year
        
    Returns:
        Effective annual rate (as decimal)
    """
    if compounds_per_year <= 0:
        raise FinanceError("Compounds per year must be positive")
    
    return ((1 + nominal_rate / compounds_per_year) ** compounds_per_year) - 1


def nominal_rate(effective_rate: float, compounds_per_year: int) -> float:
    """
    Calculate nominal rate from effective annual rate.
    
    r = n × ((1 + EAR)^(1/n) - 1)
    
    Args:
        effective_rate: Effective annual rate (as decimal)
        compounds_per_year: Number of compounding periods per year
        
    Returns:
        Nominal annual rate (as decimal)
    """
    if compounds_per_year <= 0:
        raise FinanceError("Compounds per year must be positive")
    
    return compounds_per_year * (((1 + effective_rate) ** (1 / compounds_per_year)) - 1)


# ============================================================================
# Annuities
# ============================================================================

def annuity_future_value(payment: float, rate: float, periods: int, 
                         annuity_due: bool = False) -> float:
    """
    Calculate future value of an annuity.
    
    Ordinary Annuity: FV = PMT × [((1 + r)^n - 1) / r]
    Annuity Due: FV = PMT × [((1 + r)^n - 1) / r] × (1 + r)
    
    Args:
        payment: Payment amount per period
        rate: Interest rate per period (as decimal)
        periods: Number of periods
        annuity_due: If True, payments at beginning of period (default: end)
        
    Returns:
        Future value of annuity
    """
    if rate == 0:
        return payment * periods
    
    if rate <= -1:
        raise InvalidRateError("Interest rate must be > -100%")
    
    fv = payment * (((1 + rate) ** periods - 1) / rate)
    
    if annuity_due:
        fv *= (1 + rate)
    
    return fv


def annuity_present_value(payment: float, rate: float, periods: int,
                          annuity_due: bool = False) -> float:
    """
    Calculate present value of an annuity.
    
    Ordinary Annuity: PV = PMT × [(1 - (1 + r)^(-n)) / r]
    Annuity Due: PV = PMT × [(1 - (1 + r)^(-n)) / r] × (1 + r)
    
    Args:
        payment: Payment amount per period
        rate: Discount rate per period (as decimal)
        periods: Number of periods
        annuity_due: If True, payments at beginning of period (default: end)
        
    Returns:
        Present value of annuity
    """
    if rate == 0:
        return payment * periods
    
    if rate <= -1:
        raise InvalidRateError("Discount rate must be > -100%")
    
    pv = payment * ((1 - (1 + rate) ** (-periods)) / rate)
    
    if annuity_due:
        pv *= (1 + rate)
    
    return pv


def annuity_payment(present_value: float, rate: float, periods: int,
                    annuity_due: bool = False) -> float:
    """
    Calculate annuity payment from present value.
    
    Ordinary Annuity: PMT = PV / [(1 - (1 + r)^(-n)) / r]
    
    Args:
        present_value: Present value (e.g., loan amount)
        rate: Interest rate per period (as decimal)
        periods: Number of periods
        annuity_due: If True, payments at beginning of period
        
    Returns:
        Payment amount per period
    """
    if rate == 0:
        return present_value / periods
    
    if rate <= -1:
        raise InvalidRateError("Interest rate must be > -100%")
    
    denominator = (1 - (1 + rate) ** (-periods)) / rate
    
    if annuity_due:
        denominator *= (1 + rate)
    
    return present_value / denominator


# ============================================================================
# Loan Calculations
# ============================================================================

def loan_payment(principal: float, annual_rate: float, years: int, 
                 payments_per_year: int = 12) -> float:
    """
    Calculate loan payment (mortgage-style amortizing loan).
    
    PMT = P × [r(1 + r)^n] / [(1 + r)^n - 1]
    
    Args:
        principal: Loan amount
        annual_rate: Annual interest rate (as decimal, e.g., 0.05 for 5%)
        years: Loan term in years
        payments_per_year: Number of payments per year (default: 12 for monthly)
        
    Returns:
        Payment amount per period
    """
    if principal <= 0:
        raise FinanceError("Principal must be positive")
    if years <= 0:
        raise FinanceError("Loan term must be positive")
    if payments_per_year <= 0:
        raise FinanceError("Payments per year must be positive")
    
    rate_per_period = annual_rate / payments_per_year
    total_payments = years * payments_per_year
    
    if rate_per_period == 0:
        return principal / total_payments
    
    payment = principal * (rate_per_period * (1 + rate_per_period) ** total_payments) / \
              ((1 + rate_per_period) ** total_payments - 1)
    
    return payment


def loan_amortization_schedule(principal: float, annual_rate: float, years: int,
                                payments_per_year: int = 12) -> List[Dict[str, Any]]:
    """
    Generate complete loan amortization schedule.
    
    Args:
        principal: Loan amount
        annual_rate: Annual interest rate (as decimal)
        years: Loan term in years
        payments_per_year: Number of payments per year
        
    Returns:
        List of dicts with keys: payment_number, payment, principal, interest, balance
    """
    payment = loan_payment(principal, annual_rate, years, payments_per_year)
    rate_per_period = annual_rate / payments_per_year
    total_payments = years * payments_per_year
    
    schedule = []
    balance = principal
    
    for i in range(1, total_payments + 1):
        interest = balance * rate_per_period
        principal_payment = payment - interest
        balance -= principal_payment
        
        if balance < 0:
            balance = 0
        
        schedule.append({
            'payment_number': i,
            'payment': payment,
            'principal': principal_payment,
            'interest': interest,
            'balance': balance
        })
    
    return schedule


def loan_total_interest(principal: float, annual_rate: float, years: int,
                        payments_per_year: int = 12) -> float:
    """
    Calculate total interest paid over loan life.
    
    Args:
        principal: Loan amount
        annual_rate: Annual interest rate (as decimal)
        years: Loan term in years
        payments_per_year: Number of payments per year
        
    Returns:
        Total interest paid
    """
    payment = loan_payment(principal, annual_rate, years, payments_per_year)
    total_payments = years * payments_per_year
    total_paid = payment * total_payments
    
    return total_paid - principal


def remaining_loan_balance(principal: float, annual_rate: float, 
                           years_original: int, years_elapsed: float,
                           payments_per_year: int = 12) -> float:
    """
    Calculate remaining loan balance after some payments.
    
    Args:
        principal: Original loan amount
        annual_rate: Annual interest rate (as decimal)
        years_original: Original loan term in years
        years_elapsed: Years that have passed
        payments_per_year: Number of payments per year
        
    Returns:
        Remaining balance
    """
    payment = loan_payment(principal, annual_rate, years_original, payments_per_year)
    rate_per_period = annual_rate / payments_per_year
    payments_made = int(years_elapsed * payments_per_year)
    total_payments = years_original * payments_per_year
    
    if payments_made >= total_payments:
        return 0.0
    
    # Remaining balance = PV of remaining payments
    remaining_periods = total_payments - payments_made
    balance = annuity_present_value(payment, rate_per_period, remaining_periods)
    
    return balance


# ============================================================================
# Investment Analysis
# ============================================================================

def net_present_value(cash_flows: List[float], discount_rate: float) -> float:
    """
    Calculate Net Present Value (NPV).
    
    NPV = Σ [CF_t / (1 + r)^t]
    
    Args:
        cash_flows: List of cash flows (CF[0] is typically initial investment, negative)
        discount_rate: Discount rate (as decimal)
        
    Returns:
        Net present value
    """
    if not cash_flows:
        raise InvalidCashFlowError("Cash flows cannot be empty")
    
    npv = 0.0
    for t, cf in enumerate(cash_flows):
        npv += cf / ((1 + discount_rate) ** t)
    
    return npv


def internal_rate_of_return(cash_flows: List[float], 
                            guess: float = 0.1,
                            max_iterations: int = 1000,
                            tolerance: float = 1e-10) -> float:
    """
    Calculate Internal Rate of Return (IRR) using Newton-Raphson method.
    
    IRR is the discount rate that makes NPV = 0.
    
    Args:
        cash_flows: List of cash flows (CF[0] is typically negative initial investment)
        guess: Initial guess for IRR
        max_iterations: Maximum iterations for convergence
        tolerance: Convergence tolerance
        
    Returns:
        Internal rate of return (as decimal)
        
    Raises:
        ConvergenceError: If IRR calculation fails to converge
        InvalidCashFlowError: If cash flows are invalid
    """
    if not cash_flows:
        raise InvalidCashFlowError("Cash flows cannot be empty")
    
    if len(cash_flows) < 2:
        raise InvalidCashFlowError("Need at least 2 cash flows for IRR")
    
    # Check for sign change (required for IRR to exist)
    has_positive = any(cf > 0 for cf in cash_flows)
    has_negative = any(cf < 0 for cf in cash_flows)
    
    if not (has_positive and has_negative):
        raise InvalidCashFlowError("Cash flows must have both positive and negative values")
    
    def npv(rate: float) -> float:
        return sum(cf / ((1 + rate) ** t) for t, cf in enumerate(cash_flows))
    
    def npv_derivative(rate: float) -> float:
        return sum(-t * cf / ((1 + rate) ** (t + 1)) for t, cf in enumerate(cash_flows) if t > 0)
    
    rate = guess
    
    for _ in range(max_iterations):
        npv_val = npv(rate)
        
        if abs(npv_val) < tolerance:
            return rate
        
        deriv = npv_derivative(rate)
        
        if abs(deriv) < 1e-15:
            # Derivative too small, try bisection
            break
        
        new_rate = rate - npv_val / deriv
        
        if new_rate <= -1:
            new_rate = (rate - 0.99) / 2
        
        rate = new_rate
    
    # Fall back to bisection method
    low, high = -0.9999, 10.0
    
    for _ in range(max_iterations):
        mid = (low + high) / 2
        npv_val = npv(mid)
        
        if abs(npv_val) < tolerance:
            return mid
        
        if npv_val > 0:
            low = mid
        else:
            high = mid
    
    raise ConvergenceError("IRR calculation failed to converge")


def profitability_index(cash_flows: List[float], discount_rate: float) -> float:
    """
    Calculate Profitability Index (PI).
    
    PI = PV of future cash flows / Initial investment
    
    Args:
        cash_flows: List of cash flows (CF[0] is initial investment)
        discount_rate: Discount rate (as decimal)
        
    Returns:
        Profitability index
    """
    if not cash_flows:
        raise InvalidCashFlowError("Cash flows cannot be empty")
    
    initial_investment = abs(cash_flows[0])
    
    if initial_investment == 0:
        raise InvalidCashFlowError("Initial investment cannot be zero")
    
    future_cfs = cash_flows[1:]
    if not future_cfs:
        return 0.0
    
    pv_future = sum(cf / ((1 + discount_rate) ** (t + 1)) for t, cf in enumerate(future_cfs))
    
    return pv_future / initial_investment


def payback_period(cash_flows: List[float]) -> float:
    """
    Calculate payback period (time to recover initial investment).
    
    Args:
        cash_flows: List of cash flows (CF[0] is initial investment, negative)
        
    Returns:
        Payback period in periods
        
    Raises:
        InvalidCashFlowError: If investment is never recovered
    """
    if not cash_flows:
        raise InvalidCashFlowError("Cash flows cannot be empty")
    
    initial = -cash_flows[0]  # Make positive
    
    if initial <= 0:
        raise InvalidCashFlowError("Initial cash flow should be negative (investment)")
    
    cumulative = 0.0
    
    for t in range(1, len(cash_flows)):
        cumulative += cash_flows[t]
        
        if cumulative >= initial:
            # Interpolate within this period
            prev_cumulative = cumulative - cash_flows[t]
            fraction = (initial - prev_cumulative) / cash_flows[t]
            return (t - 1) + fraction
    
    raise InvalidCashFlowError("Investment is never fully recovered")


def discounted_payback_period(cash_flows: List[float], discount_rate: float) -> float:
    """
    Calculate discounted payback period.
    
    Args:
        cash_flows: List of cash flows
        discount_rate: Discount rate (as decimal)
        
    Returns:
        Discounted payback period in periods
        
    Raises:
        InvalidCashFlowError: If investment is never recovered
    """
    if not cash_flows:
        raise InvalidCashFlowError("Cash flows cannot be empty")
    
    initial = -cash_flows[0]
    
    if initial <= 0:
        raise InvalidCashFlowError("Initial cash flow should be negative (investment)")
    
    cumulative = 0.0
    
    for t in range(1, len(cash_flows)):
        discounted_cf = cash_flows[t] / ((1 + discount_rate) ** t)
        cumulative += discounted_cf
        
        if cumulative >= initial:
            prev_cumulative = cumulative - discounted_cf
            if discounted_cf > 0:
                fraction = (initial - prev_cumulative) / discounted_cf
                return (t - 1) + fraction
    
    raise InvalidCashFlowError("Investment is never fully recovered")


# ============================================================================
# Bond Valuation
# ============================================================================

def bond_price(face_value: float, coupon_rate: float, yield_to_maturity: float,
               years_to_maturity: int, payments_per_year: int = 2) -> float:
    """
    Calculate bond price.
    
    Price = Σ [C / (1 + r)^t] + F / (1 + r)^n
    
    Args:
        face_value: Face/par value of bond
        coupon_rate: Annual coupon rate (as decimal)
        yield_to_maturity: YTM (as decimal)
        years_to_maturity: Years until maturity
        payments_per_year: Coupon payments per year (default: 2 for semi-annual)
        
    Returns:
        Bond price
    """
    if face_value <= 0:
        raise FinanceError("Face value must be positive")
    if years_to_maturity <= 0:
        raise FinanceError("Years to maturity must be positive")
    
    coupon_payment = face_value * coupon_rate / payments_per_year
    periods = years_to_maturity * payments_per_year
    rate_per_period = yield_to_maturity / payments_per_year
    
    # PV of coupon payments (annuity)
    pv_coupons = annuity_present_value(coupon_payment, rate_per_period, periods)
    
    # PV of face value
    pv_face = face_value / ((1 + rate_per_period) ** periods)
    
    return pv_coupons + pv_face


def bond_yield_to_maturity(face_value: float, coupon_rate: float, 
                           current_price: float, years_to_maturity: int,
                           payments_per_year: int = 2,
                           guess: float = 0.05) -> float:
    """
    Calculate bond yield to maturity (YTM) using Newton-Raphson.
    
    Args:
        face_value: Face/par value of bond
        coupon_rate: Annual coupon rate (as decimal)
        current_price: Current market price
        years_to_maturity: Years until maturity
        payments_per_year: Coupon payments per year
        guess: Initial guess for YTM
        
    Returns:
        Yield to maturity (as decimal)
    """
    coupon_payment = face_value * coupon_rate / payments_per_year
    periods = years_to_maturity * payments_per_year
    
    def bond_price_func(ytm: float) -> float:
        rate = ytm / payments_per_year
        pv_coupons = annuity_present_value(coupon_payment, rate, periods)
        pv_face = face_value / ((1 + rate) ** periods)
        return pv_coupons + pv_face
    
    # Use bisection for stability
    low, high = 0.0001, 1.0
    ytm = guess
    
    for _ in range(1000):
        price = bond_price_func(ytm)
        
        if abs(price - current_price) < 0.01:
            return ytm
        
        if price > current_price:
            low = ytm
        else:
            high = ytm
        
        ytm = (low + high) / 2
    
    return ytm


def bond_current_yield(face_value: float, coupon_rate: float, current_price: float) -> float:
    """
    Calculate bond current yield.
    
    Current Yield = Annual Coupon / Current Price
    
    Args:
        face_value: Face value
        coupon_rate: Annual coupon rate (as decimal)
        current_price: Current market price
        
    Returns:
        Current yield (as decimal)
    """
    if current_price <= 0:
        raise FinanceError("Current price must be positive")
    
    annual_coupon = face_value * coupon_rate
    return annual_coupon / current_price


def bond_duration(face_value: float, coupon_rate: float, yield_to_maturity: float,
                  years_to_maturity: int, payments_per_year: int = 2) -> float:
    """
    Calculate Macaulay duration of a bond.
    
    Args:
        face_value: Face value
        coupon_rate: Annual coupon rate (as decimal)
        yield_to_maturity: YTM (as decimal)
        years_to_maturity: Years to maturity
        payments_per_year: Payments per year
        
    Returns:
        Macaulay duration in years
    """
    coupon_payment = face_value * coupon_rate / payments_per_year
    periods = years_to_maturity * payments_per_year
    rate_per_period = yield_to_maturity / payments_per_year
    
    price = bond_price(face_value, coupon_rate, yield_to_maturity, years_to_maturity, payments_per_year)
    
    weighted_sum = 0.0
    
    for t in range(1, periods + 1):
        if t < periods:
            cf = coupon_payment
        else:
            cf = coupon_payment + face_value
        
        pv_cf = cf / ((1 + rate_per_period) ** t)
        weighted_sum += (t / payments_per_year) * pv_cf
    
    return weighted_sum / price


def bond_modified_duration(face_value: float, coupon_rate: float, 
                           yield_to_maturity: float, years_to_maturity: int,
                           payments_per_year: int = 2) -> float:
    """
    Calculate modified duration of a bond.
    
    Modified Duration = Macaulay Duration / (1 + YTM/n)
    
    Args:
        face_value: Face value
        coupon_rate: Annual coupon rate (as decimal)
        yield_to_maturity: YTM (as decimal)
        years_to_maturity: Years to maturity
        payments_per_year: Payments per year
        
    Returns:
        Modified duration
    """
    macaulay = bond_duration(face_value, coupon_rate, yield_to_maturity, 
                             years_to_maturity, payments_per_year)
    
    return macaulay / (1 + yield_to_maturity / payments_per_year)


# ============================================================================
# Depreciation
# ============================================================================

def straight_line_depreciation(cost: float, salvage_value: float, 
                               useful_life: int) -> List[Dict[str, Any]]:
    """
    Calculate straight-line depreciation schedule.
    
    Annual Depreciation = (Cost - Salvage Value) / Useful Life
    
    Args:
        cost: Initial cost of asset
        salvage_value: Salvage/residual value at end of life
        useful_life: Useful life in years
        
    Returns:
        List of dicts with: year, depreciation, accumulated_depreciation, book_value
    """
    if cost <= 0:
        raise FinanceError("Cost must be positive")
    if useful_life <= 0:
        raise FinanceError("Useful life must be positive")
    if salvage_value < 0:
        raise FinanceError("Salvage value cannot be negative")
    
    depreciable_amount = cost - salvage_value
    annual_depreciation = depreciable_amount / useful_life
    
    schedule = []
    accumulated = 0.0
    
    for year in range(1, useful_life + 1):
        accumulated += annual_depreciation
        book_value = cost - accumulated
        
        schedule.append({
            'year': year,
            'depreciation': annual_depreciation,
            'accumulated_depreciation': accumulated,
            'book_value': max(book_value, salvage_value)
        })
    
    return schedule


def declining_balance_depreciation(cost: float, salvage_value: float,
                                    useful_life: int, 
                                    rate: Optional[float] = None) -> List[Dict[str, Any]]:
    """
    Calculate declining balance depreciation schedule.
    
    Args:
        cost: Initial cost of asset
        salvage_value: Salvage value
        useful_life: Useful life in years
        rate: Depreciation rate (default: 2/useful_life for double-declining)
        
    Returns:
        Depreciation schedule
    """
    if cost <= 0:
        raise FinanceError("Cost must be positive")
    if useful_life <= 0:
        raise FinanceError("Useful life must be positive")
    
    if rate is None:
        rate = 2.0 / useful_life  # Double-declining balance
    
    schedule = []
    book_value = cost
    accumulated = 0.0
    
    for year in range(1, useful_life + 1):
        depreciation = book_value * rate
        
        # Don't depreciate below salvage value
        if book_value - depreciation < salvage_value:
            depreciation = book_value - salvage_value
        
        book_value -= depreciation
        accumulated += depreciation
        
        schedule.append({
            'year': year,
            'depreciation': depreciation,
            'accumulated_depreciation': accumulated,
            'book_value': book_value
        })
    
    return schedule


def sum_of_years_digits_depreciation(cost: float, salvage_value: float,
                                      useful_life: int) -> List[Dict[str, Any]]:
    """
    Calculate sum-of-years'-digits depreciation schedule.
    
    Args:
        cost: Initial cost
        salvage_value: Salvage value
        useful_life: Useful life in years
        
    Returns:
        Depreciation schedule
    """
    if cost <= 0:
        raise FinanceError("Cost must be positive")
    if useful_life <= 0:
        raise FinanceError("Useful life must be positive")
    
    depreciable_amount = cost - salvage_value
    sum_of_digits = useful_life * (useful_life + 1) / 2
    
    schedule = []
    accumulated = 0.0
    
    for year in range(1, useful_life + 1):
        remaining_life = useful_life - year + 1
        depreciation = depreciable_amount * (remaining_life / sum_of_digits)
        accumulated += depreciation
        book_value = cost - accumulated
        
        schedule.append({
            'year': year,
            'depreciation': depreciation,
            'accumulated_depreciation': accumulated,
            'book_value': max(book_value, salvage_value)
        })
    
    return schedule


# ============================================================================
# Financial Ratios
# ============================================================================

def return_on_investment(gain: float, cost: float) -> float:
    """
    Calculate Return on Investment (ROI).
    
    ROI = (Gain - Cost) / Cost
    
    Args:
        gain: Final value/gain from investment
        cost: Initial cost of investment
        
    Returns:
        ROI as decimal
    """
    if cost == 0:
        raise FinanceError("Cost cannot be zero")
    
    return (gain - cost) / cost


def return_on_equity(net_income: float, shareholders_equity: float) -> float:
    """
    Calculate Return on Equity (ROE).
    
    ROE = Net Income / Shareholders' Equity
    
    Args:
        net_income: Net income
        shareholders_equity: Shareholders' equity
        
    Returns:
        ROE as decimal
    """
    if shareholders_equity == 0:
        raise FinanceError("Shareholders' equity cannot be zero")
    
    return net_income / shareholders_equity


def return_on_assets(net_income: float, total_assets: float) -> float:
    """
    Calculate Return on Assets (ROA).
    
    ROA = Net Income / Total Assets
    
    Args:
        net_income: Net income
        total_assets: Total assets
        
    Returns:
        ROA as decimal
    """
    if total_assets == 0:
        raise FinanceError("Total assets cannot be zero")
    
    return net_income / total_assets


def current_ratio(current_assets: float, current_liabilities: float) -> float:
    """
    Calculate current ratio (liquidity ratio).
    
    Current Ratio = Current Assets / Current Liabilities
    
    Args:
        current_assets: Current assets
        current_liabilities: Current liabilities
        
    Returns:
        Current ratio
    """
    if current_liabilities == 0:
        raise FinanceError("Current liabilities cannot be zero")
    
    return current_assets / current_liabilities


def quick_ratio(cash: float, marketable_securities: float, 
                accounts_receivable: float, current_liabilities: float) -> float:
    """
    Calculate quick ratio (acid-test ratio).
    
    Quick Ratio = (Cash + Marketable Securities + AR) / Current Liabilities
    
    Args:
        cash: Cash and cash equivalents
        marketable_securities: Marketable securities
        accounts_receivable: Accounts receivable
        current_liabilities: Current liabilities
        
    Returns:
        Quick ratio
    """
    if current_liabilities == 0:
        raise FinanceError("Current liabilities cannot be zero")
    
    quick_assets = cash + marketable_securities + accounts_receivable
    return quick_assets / current_liabilities


def debt_to_equity(total_debt: float, shareholders_equity: float) -> float:
    """
    Calculate debt-to-equity ratio.
    
    D/E = Total Debt / Shareholders' Equity
    
    Args:
        total_debt: Total debt
        shareholders_equity: Shareholders' equity
        
    Returns:
        Debt-to-equity ratio
    """
    if shareholders_equity == 0:
        raise FinanceError("Shareholders' equity cannot be zero")
    
    return total_debt / shareholders_equity


def gross_profit_margin(revenue: float, cost_of_goods_sold: float) -> float:
    """
    Calculate gross profit margin.
    
    Gross Margin = (Revenue - COGS) / Revenue
    
    Args:
        revenue: Total revenue
        cost_of_goods_sold: Cost of goods sold
        
    Returns:
        Gross profit margin as decimal
    """
    if revenue == 0:
        raise FinanceError("Revenue cannot be zero")
    
    return (revenue - cost_of_goods_sold) / revenue


def net_profit_margin(revenue: float, net_income: float) -> float:
    """
    Calculate net profit margin.
    
    Net Margin = Net Income / Revenue
    
    Args:
        revenue: Total revenue
        net_income: Net income
        
    Returns:
        Net profit margin as decimal
    """
    if revenue == 0:
        raise FinanceError("Revenue cannot be zero")
    
    return net_income / revenue


def earnings_per_share(net_income: float, preferred_dividends: float,
                       shares_outstanding: int) -> float:
    """
    Calculate earnings per share (EPS).
    
    EPS = (Net Income - Preferred Dividends) / Shares Outstanding
    
    Args:
        net_income: Net income
        preferred_dividends: Preferred stock dividends
        shares_outstanding: Number of common shares outstanding
        
    Returns:
        Earnings per share
    """
    if shares_outstanding <= 0:
        raise FinanceError("Shares outstanding must be positive")
    
    return (net_income - preferred_dividends) / shares_outstanding


def price_to_earnings_ratio(stock_price: float, earnings_per_share: float) -> float:
    """
    Calculate P/E ratio.
    
    P/E = Stock Price / EPS
    
    Args:
        stock_price: Current stock price
        earnings_per_share: Earnings per share
        
    Returns:
        P/E ratio
    """
    if earnings_per_share == 0:
        raise FinanceError("EPS cannot be zero")
    
    return stock_price / earnings_per_share


def dividend_yield(annual_dividend: float, stock_price: float) -> float:
    """
    Calculate dividend yield.
    
    Dividend Yield = Annual Dividend / Stock Price
    
    Args:
        annual_dividend: Annual dividend per share
        stock_price: Current stock price
        
    Returns:
        Dividend yield as decimal
    """
    if stock_price == 0:
        raise FinanceError("Stock price cannot be zero")
    
    return annual_dividend / stock_price


# ============================================================================
# Currency & Exchange
# ============================================================================

def currency_convert(amount: float, exchange_rate: float) -> float:
    """
    Convert currency using exchange rate.
    
    Args:
        amount: Amount in source currency
        exchange_rate: Exchange rate (1 unit of source = X units of target)
        
    Returns:
        Amount in target currency
    """
    if exchange_rate <= 0:
        raise FinanceError("Exchange rate must be positive")
    
    return amount * exchange_rate


def cross_rate(rate_ab: float, rate_bc: float) -> float:
    """
    Calculate cross exchange rate.
    
    If A/B = rate_ab and B/C = rate_bc, then A/C = rate_ab × rate_bc
    
    Args:
        rate_ab: Exchange rate from currency A to B
        rate_bc: Exchange rate from currency B to C
        
    Returns:
        Cross rate from A to C
    """
    if rate_ab <= 0 or rate_bc <= 0:
        raise FinanceError("Exchange rates must be positive")
    
    return rate_ab * rate_bc


# ============================================================================
# Risk & Statistics for Finance
# ============================================================================

def expected_return(returns: List[float], probabilities: Optional[List[float]] = None) -> float:
    """
    Calculate expected return.
    
    E[R] = Σ (p_i × r_i)
    
    Args:
        returns: List of possible returns
        probabilities: List of probabilities (must sum to 1). If None, assumes equal probability.
        
    Returns:
        Expected return
    """
    if not returns:
        raise InvalidCashFlowError("Returns cannot be empty")
    
    if probabilities is None:
        probabilities = [1.0 / len(returns)] * len(returns)
    
    if len(returns) != len(probabilities):
        raise InvalidCashFlowError("Returns and probabilities must have same length")
    
    prob_sum = sum(probabilities)
    if abs(prob_sum - 1.0) > 0.0001:
        raise InvalidCashFlowError("Probabilities must sum to 1")
    
    return sum(r * p for r, p in zip(returns, probabilities))


def variance_returns(returns: List[float], population: bool = False) -> float:
    """
    Calculate variance of returns.
    
    Args:
        returns: List of returns
        population: If True, use population variance (divide by n); else sample variance (divide by n-1)
        
    Returns:
        Variance
    """
    if len(returns) < 2:
        raise InvalidCashFlowError("Need at least 2 returns for variance")
    
    mean_return = sum(returns) / len(returns)
    squared_diffs = [(r - mean_return) ** 2 for r in returns]
    
    if population:
        return sum(squared_diffs) / len(returns)
    else:
        return sum(squared_diffs) / (len(returns) - 1)


def std_dev_returns(returns: List[float], population: bool = False) -> float:
    """
    Calculate standard deviation of returns (volatility).
    
    Args:
        returns: List of returns
        population: If True, use population std dev
        
    Returns:
        Standard deviation
    """
    return math.sqrt(variance_returns(returns, population))


def covariance_returns(returns_a: List[float], returns_b: List[float]) -> float:
    """
    Calculate covariance between two return series.
    
    Args:
        returns_a: First return series
        returns_b: Second return series
        
    Returns:
        Covariance
    """
    if len(returns_a) != len(returns_b):
        raise InvalidCashFlowError("Return series must have same length")
    
    if len(returns_a) < 2:
        raise InvalidCashFlowError("Need at least 2 observations")
    
    mean_a = sum(returns_a) / len(returns_a)
    mean_b = sum(returns_b) / len(returns_b)
    
    cov_sum = sum((a - mean_a) * (b - mean_b) for a, b in zip(returns_a, returns_b))
    
    return cov_sum / (len(returns_a) - 1)


def correlation_returns(returns_a: List[float], returns_b: List[float]) -> float:
    """
    Calculate correlation coefficient between two return series.
    
    Args:
        returns_a: First return series
        returns_b: Second return series
        
    Returns:
        Correlation coefficient (-1 to 1)
    """
    cov = covariance_returns(returns_a, returns_b)
    std_a = std_dev_returns(returns_a)
    std_b = std_dev_returns(returns_b)
    
    if std_a == 0 or std_b == 0:
        return 0.0
    
    return cov / (std_a * std_b)


def beta(asset_returns: List[float], market_returns: List[float]) -> float:
    """
    Calculate beta (systematic risk) of an asset.
    
    Beta = Covariance(asset, market) / Variance(market)
    
    Args:
        asset_returns: Asset return series
        market_returns: Market return series
        
    Returns:
        Beta coefficient
    """
    cov = covariance_returns(asset_returns, market_returns)
    var_market = variance_returns(market_returns)
    
    if var_market == 0:
        return 0.0
    
    return cov / var_market


def sharpe_ratio(portfolio_return: float, risk_free_rate: float, 
                 portfolio_std_dev: float) -> float:
    """
    Calculate Sharpe ratio.
    
    Sharpe Ratio = (Portfolio Return - Risk-Free Rate) / Portfolio Std Dev
    
    Args:
        portfolio_return: Portfolio return (as decimal)
        risk_free_rate: Risk-free rate (as decimal)
        portfolio_std_dev: Portfolio standard deviation
        
    Returns:
        Sharpe ratio
    """
    if portfolio_std_dev == 0:
        raise FinanceError("Portfolio standard deviation cannot be zero")
    
    return (portfolio_return - risk_free_rate) / portfolio_std_dev


def value_at_loss(returns: List[float], confidence_level: float = 0.95) -> float:
    """
    Calculate Value at Risk (VaR) using historical method.
    
    Args:
        returns: Historical return series
        confidence_level: Confidence level (e.g., 0.95 for 95%)
        
    Returns:
        Value at Risk (as positive number representing potential loss)
    """
    if not returns:
        raise InvalidCashFlowError("Returns cannot be empty")
    
    if not 0 < confidence_level < 1:
        raise FinanceError("Confidence level must be between 0 and 1")
    
    sorted_returns = sorted(returns)
    index = int((1 - confidence_level) * len(sorted_returns))
    
    return -sorted_returns[index]


# ============================================================================
# Convenience Functions
# ============================================================================

def investment_summary(initial_investment: float, annual_return: float, 
                       years: int, annual_contribution: float = 0) -> Dict[str, Any]:
    """
    Generate comprehensive investment summary.
    
    Args:
        initial_investment: Initial investment amount
        annual_return: Expected annual return (as decimal)
        years: Investment horizon in years
        annual_contribution: Additional annual contribution (default: 0)
        
    Returns:
        Dictionary with investment projections
    """
    if annual_contribution == 0:
        final_value = future_value(initial_investment, annual_return, years)
        total_contributed = initial_investment
    else:
        # Future value with initial + annuity
        fv_initial = future_value(initial_investment, annual_return, years)
        fv_contributions = annuity_future_value(annual_contribution, annual_return, years)
        final_value = fv_initial + fv_contributions
        total_contributed = initial_investment + (annual_contribution * years)
    
    total_gain = final_value - total_contributed
    total_return_pct = (total_gain / total_contributed) * 100 if total_contributed > 0 else 0
    
    return {
        'initial_investment': initial_investment,
        'annual_contribution': annual_contribution,
        'annual_return': annual_return,
        'years': years,
        'total_contributed': total_contributed,
        'final_value': final_value,
        'total_gain': total_gain,
        'total_return_pct': total_return_pct
    }


def compare_loans(principal: float, options: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Compare multiple loan options.
    
    Args:
        principal: Loan amount
        options: List of dicts with 'annual_rate' and 'years' keys
        
    Returns:
        List of comparison results sorted by total cost
    """
    results = []
    
    for opt in options:
        rate = opt['annual_rate']
        years = opt['years']
        payments_per_year = opt.get('payments_per_year', 12)
        
        monthly_payment = loan_payment(principal, rate, years, payments_per_year)
        total_interest = loan_total_interest(principal, rate, years, payments_per_year)
        total_cost = principal + total_interest
        
        results.append({
            'annual_rate': rate,
            'years': years,
            'monthly_payment': monthly_payment,
            'total_interest': total_interest,
            'total_cost': total_cost
        })
    
    # Sort by total cost
    results.sort(key=lambda x: x['total_cost'])
    
    return results


def rule_of_72(annual_rate: float) -> float:
    """
    Calculate years to double investment using Rule of 72.
    
    Years to Double ≈ 72 / Annual Rate (%)
    
    Args:
        annual_rate: Annual return rate as percentage (e.g., 8 for 8%)
        
    Returns:
        Approximate years to double
    """
    if annual_rate <= 0:
        raise InvalidRateError("Annual rate must be positive")
    
    return 72 / annual_rate


def rule_of_72_exact(annual_rate: float) -> float:
    """
    Calculate exact years to double investment.
    
    Years = ln(2) / ln(1 + r)
    
    Args:
        annual_rate: Annual return rate as decimal (e.g., 0.08 for 8%)
        
    Returns:
        Exact years to double
    """
    if annual_rate <= 0:
        raise InvalidRateError("Annual rate must be positive")
    
    return math.log(2) / math.log(1 + annual_rate)


# ============================================================================
# Module Constants
# ============================================================================

VERSION = "1.0.0"
AUTHOR = "AllToolkit"
LICENSE = "MIT"
