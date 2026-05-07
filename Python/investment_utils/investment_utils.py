"""
Investment Utils - Comprehensive investment calculation utilities.

A zero-dependency library for financial calculations including:
- Compound interest
- Simple interest
- SIP (Systematic Investment Plan) returns
- CAGR (Compound Annual Growth Rate)
- Present/Future value
- ROI (Return on Investment)
- IRR (Internal Rate of Return)
- Payback period
- Amortization schedules
- Investment comparison

Author: AllToolkit
Date: 2026-05-07
"""

from typing import List, Tuple, Dict, Optional
from dataclasses import dataclass
from enum import Enum
import math


class CompoundingFrequency(Enum):
    """Compounding frequency options."""
    ANNUALLY = 1
    SEMI_ANNUALLY = 2
    QUARTERLY = 4
    MONTHLY = 12
    WEEKLY = 52
    DAILY = 365
    CONTINUOUSLY = 0


@dataclass
class InvestmentResult:
    """Result container for investment calculations."""
    principal: float
    total_amount: float
    total_interest: float
    effective_rate: float


@dataclass
class SIPResult:
    """Result container for SIP calculations."""
    total_invested: float
    maturity_value: float
    total_returns: float
    annualized_return: float


@dataclass
class AmortizationEntry:
    """Single entry in an amortization schedule."""
    period: int
    payment: float
    principal: float
    interest: float
    balance: float


# ============== Compound Interest ==============

def compound_interest(
    principal: float,
    rate: float,
    time: float,
    n: int = 12,
    rounds: int = 2
) -> InvestmentResult:
    """
    Calculate compound interest.
    
    Formula: A = P * (1 + r/n)^(n*t)
    
    Args:
        principal: Initial investment amount
        rate: Annual interest rate (as decimal, e.g., 0.08 for 8%)
        time: Time period in years
        n: Compounding frequency per year (default monthly)
        rounds: Decimal places to round to
    
    Returns:
        InvestmentResult with principal, total amount, interest earned, and effective rate
    
    Examples:
        >>> result = compound_interest(10000, 0.08, 5)
        >>> result.total_amount
        14898.46
        >>> result = compound_interest(10000, 0.08, 5, n=1)  # Annual compounding
        >>> result.total_amount
        14693.28
    """
    if principal < 0:
        raise ValueError("Principal cannot be negative")
    if rate < 0:
        raise ValueError("Rate cannot be negative")
    if time < 0:
        raise ValueError("Time cannot be negative")
    if n <= 0:
        raise ValueError("Compounding frequency must be positive")
    
    amount = principal * math.pow(1 + rate / n, n * time)
    interest = amount - principal
    effective_rate = math.pow(1 + rate / n, n) - 1
    
    return InvestmentResult(
        principal=round(principal, rounds),
        total_amount=round(amount, rounds),
        total_interest=round(interest, rounds),
        effective_rate=round(effective_rate, 4)
    )


def compound_interest_continuous(
    principal: float,
    rate: float,
    time: float,
    rounds: int = 2
) -> InvestmentResult:
    """
    Calculate compound interest with continuous compounding.
    
    Formula: A = P * e^(r*t)
    
    Args:
        principal: Initial investment amount
        rate: Annual interest rate (as decimal)
        time: Time period in years
        rounds: Decimal places to round to
    
    Returns:
        InvestmentResult with calculated values
    
    Examples:
        >>> result = compound_interest_continuous(10000, 0.08, 5)
        >>> round(result.total_amount)
        14918.0
    """
    if principal < 0:
        raise ValueError("Principal cannot be negative")
    if rate < 0:
        raise ValueError("Rate cannot be negative")
    if time < 0:
        raise ValueError("Time cannot be negative")
    
    amount = principal * math.exp(rate * time)
    interest = amount - principal
    effective_rate = math.exp(rate) - 1
    
    return InvestmentResult(
        principal=round(principal, rounds),
        total_amount=round(amount, rounds),
        total_interest=round(interest, rounds),
        effective_rate=round(effective_rate, 4)
    )


# ============== Simple Interest ==============

def simple_interest(
    principal: float,
    rate: float,
    time: float,
    rounds: int = 2
) -> InvestmentResult:
    """
    Calculate simple interest.
    
    Formula: A = P * (1 + r*t)
    
    Args:
        principal: Initial investment amount
        rate: Annual interest rate (as decimal)
        time: Time period in years
        rounds: Decimal places to round to
    
    Returns:
        InvestmentResult with calculated values
    
    Examples:
        >>> result = simple_interest(10000, 0.08, 5)
        >>> result.total_amount
        14000.0
    """
    if principal < 0:
        raise ValueError("Principal cannot be negative")
    if rate < 0:
        raise ValueError("Rate cannot be negative")
    if time < 0:
        raise ValueError("Time cannot be negative")
    
    interest = principal * rate * time
    amount = principal + interest
    
    return InvestmentResult(
        principal=round(principal, rounds),
        total_amount=round(amount, rounds),
        total_interest=round(interest, rounds),
        effective_rate=round(rate, 4)
    )


# ============== SIP Calculations ==============

def sip_returns(
    monthly_investment: float,
    annual_rate: float,
    years: int,
    rounds: int = 2
) -> SIPResult:
    """
    Calculate SIP (Systematic Investment Plan) returns.
    
    Formula: FV = P * [(1+r)^n - 1] / r * (1+r)
    where r = monthly rate, n = total months
    
    Args:
        monthly_investment: Monthly investment amount
        annual_rate: Expected annual return rate (as decimal)
        years: Investment period in years
        rounds: Decimal places to round to
    
    Returns:
        SIPResult with total invested, maturity value, returns, and annualized return
    
    Examples:
        >>> result = sip_returns(10000, 0.12, 10)
        >>> result.total_invested
        1200000.0
        >>> result.maturity_value > result.total_invested
        True
    """
    if monthly_investment < 0:
        raise ValueError("Monthly investment cannot be negative")
    if annual_rate < 0:
        raise ValueError("Rate cannot be negative")
    if years < 0:
        raise ValueError("Years cannot be negative")
    
    monthly_rate = annual_rate / 12
    total_months = years * 12
    total_invested = monthly_investment * total_months
    
    # SIP Future Value formula
    if monthly_rate == 0:
        maturity_value = total_invested
    else:
        maturity_value = monthly_investment * (
            (math.pow(1 + monthly_rate, total_months) - 1) / monthly_rate
        ) * (1 + monthly_rate)
    
    total_returns = maturity_value - total_invested
    
    # Calculate annualized return (XIRR approximation)
    if total_invested > 0:
        annualized_return = (math.pow(maturity_value / total_invested, 1/years) - 1) if years > 0 else 0
    else:
        annualized_return = 0
    
    return SIPResult(
        total_invested=round(total_invested, rounds),
        maturity_value=round(maturity_value, rounds),
        total_returns=round(total_returns, rounds),
        annualized_return=round(annualized_return, 4)
    )


def sip_step_up(
    initial_monthly: float,
    step_up_rate: float,
    annual_rate: float,
    years: int,
    rounds: int = 2
) -> Dict:
    """
    Calculate Step-up SIP returns (increasing monthly investment each year).
    
    Args:
        initial_monthly: Initial monthly investment
        step_up_rate: Annual increase rate (as decimal, e.g., 0.1 for 10%)
        annual_rate: Expected annual return rate (as decimal)
        years: Investment period in years
        rounds: Decimal places to round to
    
    Returns:
        Dictionary with total invested, maturity value, and yearly breakdown
    
    Examples:
        >>> result = sip_step_up(10000, 0.1, 0.12, 10)
        >>> result['total_invested'] > 1200000  # More than regular SIP
        True
    """
    if initial_monthly < 0:
        raise ValueError("Initial monthly investment cannot be negative")
    if step_up_rate < 0:
        raise ValueError("Step-up rate cannot be negative")
    if annual_rate < 0:
        raise ValueError("Annual rate cannot be negative")
    if years < 0:
        raise ValueError("Years cannot be negative")
    
    monthly_rate = annual_rate / 12
    total_invested = 0
    yearly_values = []
    accumulated_value = 0
    
    current_monthly = initial_monthly
    
    for year in range(years):
        # Invest each month of this year
        year_investment = current_monthly * 12
        total_invested += year_investment
        
        # Calculate growth for this year's investments
        months_remaining = (years - year - 1) * 12
        if monthly_rate > 0:
            year_future_value = current_monthly * (
                (math.pow(1 + monthly_rate, 12) - 1) / monthly_rate
            ) * math.pow(1 + monthly_rate, months_remaining)
        else:
            year_future_value = year_investment
        
        accumulated_value += year_future_value
        
        yearly_values.append({
            'year': year + 1,
            'monthly_investment': round(current_monthly, rounds),
            'year_investment': round(year_investment, rounds)
        })
        
        # Step up for next year
        current_monthly *= (1 + step_up_rate)
    
    maturity_value = accumulated_value
    
    return {
        'total_invested': round(total_invested, rounds),
        'maturity_value': round(maturity_value, rounds),
        'total_returns': round(maturity_value - total_invested, rounds),
        'yearly_breakdown': yearly_values
    }


# ============== CAGR Calculations ==============

def cagr(
    beginning_value: float,
    ending_value: float,
    years: float,
    rounds: int = 4
) -> float:
    """
    Calculate Compound Annual Growth Rate.
    
    Formula: CAGR = (EV / BV)^(1/n) - 1
    
    Args:
        beginning_value: Initial value of investment
        ending_value: Final value of investment
        years: Number of years
        rounds: Decimal places to round to
    
    Returns:
        CAGR as decimal (multiply by 100 for percentage)
    
    Examples:
        >>> cagr(10000, 20000, 5)
        0.1487
        >>> round(cagr(100, 200, 10) * 100, 2)
        7.18
    """
    if beginning_value <= 0:
        raise ValueError("Beginning value must be positive")
    if ending_value < 0:
        raise ValueError("Ending value cannot be negative")
    if years <= 0:
        raise ValueError("Years must be positive")
    
    rate = math.pow(ending_value / beginning_value, 1 / years) - 1
    return round(rate, rounds)


def cagr_from_returns(returns: List[float], rounds: int = 4) -> float:
    """
    Calculate CAGR from a list of annual returns.
    
    Args:
        returns: List of annual return percentages (as decimals)
        rounds: Decimal places to round to
    
    Returns:
        CAGR as decimal
    
    Examples:
        >>> cagr_from_returns([0.10, 0.15, -0.05, 0.20])
        0.0958
    """
    if not returns:
        raise ValueError("Returns list cannot be empty")
    
    total_growth = 1.0
    for r in returns:
        total_growth *= (1 + r)
    
    years = len(returns)
    rate = math.pow(total_growth, 1 / years) - 1
    return round(rate, rounds)


# ============== Present/Future Value ==============

def present_value(
    future_value: float,
    rate: float,
    periods: int,
    rounds: int = 2
) -> float:
    """
    Calculate present value of a future amount.
    
    Formula: PV = FV / (1 + r)^n
    
    Args:
        future_value: Future value
        rate: Discount rate per period (as decimal)
        periods: Number of periods
        rounds: Decimal places to round to
    
    Returns:
        Present value
    
    Examples:
        >>> present_value(100000, 0.08, 5)
        68058.32
    """
    if future_value < 0:
        raise ValueError("Future value cannot be negative")
    if rate < 0:
        raise ValueError("Rate cannot be negative")
    if periods < 0:
        raise ValueError("Periods cannot be negative")
    
    pv = future_value / math.pow(1 + rate, periods)
    return round(pv, rounds)


def future_value(
    present_value: float,
    rate: float,
    periods: int,
    rounds: int = 2
) -> float:
    """
    Calculate future value of a present amount.
    
    Formula: FV = PV * (1 + r)^n
    
    Args:
        present_value: Present value
        rate: Interest rate per period (as decimal)
        periods: Number of periods
        rounds: Decimal places to round to
    
    Returns:
        Future value
    
    Examples:
        >>> future_value(10000, 0.08, 5)
        14693.28
    """
    if present_value < 0:
        raise ValueError("Present value cannot be negative")
    if rate < 0:
        raise ValueError("Rate cannot be negative")
    if periods < 0:
        raise ValueError("Periods cannot be negative")
    
    fv = present_value * math.pow(1 + rate, periods)
    return round(fv, rounds)


def present_value_annuity(
    payment: float,
    rate: float,
    periods: int,
    rounds: int = 2
) -> float:
    """
    Calculate present value of an annuity (series of equal payments).
    
    Formula: PV = PMT * [1 - (1 + r)^-n] / r
    
    Args:
        payment: Periodic payment amount
        rate: Discount rate per period (as decimal)
        periods: Number of periods
        rounds: Decimal places to round to
    
    Returns:
        Present value of annuity
    
    Examples:
        >>> present_value_annuity(1000, 0.05, 10)
        7721.73
    """
    if payment < 0:
        raise ValueError("Payment cannot be negative")
    if rate < 0:
        raise ValueError("Rate cannot be negative")
    if periods < 0:
        raise ValueError("Periods cannot be negative")
    
    if rate == 0:
        return round(payment * periods, rounds)
    
    pv = payment * (1 - math.pow(1 + rate, -periods)) / rate
    return round(pv, rounds)


# ============== ROI Calculations ==============

def roi(
    initial_investment: float,
    final_value: float,
    rounds: int = 4
) -> float:
    """
    Calculate Return on Investment.
    
    Formula: ROI = (Final - Initial) / Initial
    
    Args:
        initial_investment: Initial investment amount
        final_value: Final value of investment
        rounds: Decimal places to round to
    
    Returns:
        ROI as decimal (multiply by 100 for percentage)
    
    Examples:
        >>> roi(10000, 15000)
        0.5
        >>> roi(10000, 8000)
        -0.2
    """
    if initial_investment == 0:
        raise ValueError("Initial investment cannot be zero")
    
    return_rate = (final_value - initial_investment) / initial_investment
    return round(return_rate, rounds)


def annualized_roi(
    initial_investment: float,
    final_value: float,
    days: int,
    rounds: int = 4
) -> float:
    """
    Calculate annualized ROI.
    
    Formula: Annualized ROI = (1 + ROI)^(365/days) - 1
    
    Args:
        initial_investment: Initial investment amount
        final_value: Final value of investment
        days: Number of days held
        rounds: Decimal places to round to
    
    Returns:
        Annualized ROI as decimal
    
    Examples:
        >>> annualized_roi(10000, 12000, 180)
        0.446
    """
    if initial_investment == 0:
        raise ValueError("Initial investment cannot be zero")
    if days <= 0:
        raise ValueError("Days must be positive")
    
    total_return = final_value / initial_investment
    annualized = math.pow(total_return, 365 / days) - 1
    return round(annualized, rounds)


# ============== IRR Calculations ==============

def irr(
    cash_flows: List[float],
    guess: float = 0.1,
    max_iterations: int = 1000,
    tolerance: float = 1e-6
) -> float:
    """
    Calculate Internal Rate of Return using Newton-Raphson method.
    
    IRR is the rate that makes NPV of cash flows equal to zero.
    
    Args:
        cash_flows: List of cash flows (negative for outflows, positive for inflows)
        guess: Initial guess for IRR
        max_iterations: Maximum iterations for convergence
        tolerance: Convergence tolerance
    
    Returns:
        IRR as decimal
    
    Examples:
        >>> irr([-1000, 300, 300, 300, 300, 300])
        0.1524
    """
    if not cash_flows:
        raise ValueError("Cash flows cannot be empty")
    if len(cash_flows) < 2:
        raise ValueError("Need at least 2 cash flows")
    
    rate = guess
    
    for _ in range(max_iterations):
        npv = 0
        d_npv = 0  # Derivative of NPV
        
        for i, cf in enumerate(cash_flows):
            discount = math.pow(1 + rate, i)
            npv += cf / discount
            d_npv -= i * cf / math.pow(1 + rate, i + 1)
        
        if abs(npv) < tolerance:
            return round(rate, 4)
        
        if d_npv == 0:
            break
        
        rate = rate - npv / d_npv
    
    return round(rate, 4)


def npv(
    cash_flows: List[float],
    rate: float,
    rounds: int = 2
) -> float:
    """
    Calculate Net Present Value.
    
    Formula: NPV = sum(CF_i / (1 + r)^i)
    
    Args:
        cash_flows: List of cash flows
        rate: Discount rate (as decimal)
        rounds: Decimal places to round to
    
    Returns:
        NPV value
    
    Examples:
        >>> npv([-1000, 300, 300, 300, 300, 300], 0.1)
        137.24
    """
    if not cash_flows:
        return 0.0
    
    total = 0
    for i, cf in enumerate(cash_flows):
        total += cf / math.pow(1 + rate, i)
    
    return round(total, rounds)


# ============== Payback Period ==============

def payback_period(
    initial_investment: float,
    cash_flows: List[float],
    rounds: int = 2
) -> float:
    """
    Calculate payback period in periods.
    
    Args:
        initial_investment: Initial investment (positive number)
        cash_flows: List of periodic cash flows
        rounds: Decimal places to round to
    
    Returns:
        Payback period (same unit as cash flow periods)
    
    Examples:
        >>> payback_period(1000, [200, 300, 400, 200])
        3.5
    """
    if initial_investment <= 0:
        raise ValueError("Initial investment must be positive")
    if not cash_flows:
        raise ValueError("Cash flows cannot be empty")
    
    cumulative = -initial_investment
    
    for i, cf in enumerate(cash_flows):
        prev_cumulative = cumulative
        cumulative += cf
        
        if cumulative >= 0:
            # Payback happens in this period
            remaining = -prev_cumulative
            if cf > 0:
                fraction = remaining / cf
                return round(i + fraction, rounds)
            return round(float(i), rounds)
    
    # Payback not achieved
    return float('inf')


def discounted_payback_period(
    initial_investment: float,
    cash_flows: List[float],
    rate: float,
    rounds: int = 2
) -> float:
    """
    Calculate discounted payback period.
    
    Args:
        initial_investment: Initial investment (positive number)
        cash_flows: List of periodic cash flows
        rate: Discount rate (as decimal)
        rounds: Decimal places to round to
    
    Returns:
        Discounted payback period
    
    Examples:
        >>> discounted_payback_period(1000, [300, 400, 400, 200], 0.1)
        3.38
    """
    if initial_investment <= 0:
        raise ValueError("Initial investment must be positive")
    if not cash_flows:
        raise ValueError("Cash flows cannot be empty")
    
    cumulative = -initial_investment
    
    for i, cf in enumerate(cash_flows):
        prev_cumulative = cumulative
        discounted_cf = cf / math.pow(1 + rate, i + 1)
        cumulative += discounted_cf
        
        if cumulative >= 0:
            remaining = -prev_cumulative
            if discounted_cf > 0:
                fraction = remaining / discounted_cf
                return round(i + fraction, rounds)
            return round(float(i), rounds)
    
    return float('inf')


# ============== Amortization ==============

def loan_payment(
    principal: float,
    annual_rate: float,
    years: int,
    rounds: int = 2
) -> float:
    """
    Calculate monthly loan payment.
    
    Formula: PMT = P * r * (1 + r)^n / ((1 + r)^n - 1)
    
    Args:
        principal: Loan amount
        annual_rate: Annual interest rate (as decimal)
        years: Loan term in years
        rounds: Decimal places to round to
    
    Returns:
        Monthly payment amount
    
    Examples:
        >>> loan_payment(100000, 0.06, 30)
        599.55
    """
    if principal <= 0:
        raise ValueError("Principal must be positive")
    if annual_rate < 0:
        raise ValueError("Rate cannot be negative")
    if years <= 0:
        raise ValueError("Years must be positive")
    
    monthly_rate = annual_rate / 12
    num_payments = years * 12
    
    if monthly_rate == 0:
        return round(principal / num_payments, rounds)
    
    payment = principal * monthly_rate * math.pow(1 + monthly_rate, num_payments)
    payment /= (math.pow(1 + monthly_rate, num_payments) - 1)
    
    return round(payment, rounds)


def amortization_schedule(
    principal: float,
    annual_rate: float,
    years: int
) -> List[AmortizationEntry]:
    """
    Generate amortization schedule for a loan.
    
    Args:
        principal: Loan amount
        annual_rate: Annual interest rate (as decimal)
        years: Loan term in years
    
    Returns:
        List of AmortizationEntry for each payment period
    
    Examples:
        >>> schedule = amortization_schedule(100000, 0.06, 1)
        >>> len(schedule)
        12
        >>> schedule[0].payment == schedule[1].payment
        True
    """
    if principal <= 0:
        raise ValueError("Principal must be positive")
    if annual_rate < 0:
        raise ValueError("Rate cannot be negative")
    if years <= 0:
        raise ValueError("Years must be positive")
    
    monthly_rate = annual_rate / 12
    num_payments = years * 12
    payment = loan_payment(principal, annual_rate, years)
    
    schedule = []
    balance = principal
    
    for period in range(1, num_payments + 1):
        interest = balance * monthly_rate
        principal_paid = payment - interest
        balance -= principal_paid
        
        if balance < 0:
            balance = 0
        
        schedule.append(AmortizationEntry(
            period=period,
            payment=round(payment, 2),
            principal=round(principal_paid, 2),
            interest=round(interest, 2),
            balance=round(abs(balance), 2)
        ))
    
    return schedule


# ============== Investment Comparison ==============

def compare_investments(
    investments: List[Dict[str, float]],
    rounds: int = 2
) -> Dict:
    """
    Compare multiple investment options.
    
    Args:
        investments: List of dicts with 'name', 'initial', 'final', 'years'
        rounds: Decimal places to round to
    
    Returns:
        Dictionary with comparison results ranked by CAGR
    
    Examples:
        >>> investments = [
        ...     {'name': 'Stock A', 'initial': 10000, 'final': 15000, 'years': 3},
        ...     {'name': 'Stock B', 'initial': 10000, 'final': 14000, 'years': 2}
        ... ]
        >>> result = compare_investments(investments)
        >>> result['winner']['name']
        'Stock B'
    """
    if not investments:
        raise ValueError("Investments list cannot be empty")
    
    results = []
    
    for inv in investments:
        inv_cagr = cagr(inv['initial'], inv['final'], inv['years'])
        inv_roi = roi(inv['initial'], inv['final'])
        profit = inv['final'] - inv['initial']
        
        results.append({
            'name': inv['name'],
            'initial': inv['initial'],
            'final': inv['final'],
            'years': inv['years'],
            'profit': round(profit, rounds),
            'roi': round(inv_roi, 4),
            'roi_percent': round(inv_roi * 100, 2),
            'cagr': round(inv_cagr, 4),
            'cagr_percent': round(inv_cagr * 100, 2)
        })
    
    # Sort by CAGR descending
    results.sort(key=lambda x: x['cagr'], reverse=True)
    
    return {
        'rankings': results,
        'winner': results[0] if results else None
    }


def inflation_adjusted_return(
    nominal_return: float,
    inflation_rate: float,
    rounds: int = 4
) -> float:
    """
    Calculate real (inflation-adjusted) return.
    
    Formula: Real = (1 + Nominal) / (1 + Inflation) - 1
    
    Args:
        nominal_return: Nominal return rate (as decimal)
        inflation_rate: Inflation rate (as decimal)
        rounds: Decimal places to round to
    
    Returns:
        Real return rate as decimal
    
    Examples:
        >>> inflation_adjusted_return(0.10, 0.03)
        0.068
    """
    if nominal_return < -1:
        raise ValueError("Nominal return cannot be less than -100%")
    if inflation_rate < -1:
        raise ValueError("Inflation rate cannot be less than -100%")
    
    real_return = (1 + nominal_return) / (1 + inflation_rate) - 1
    return round(real_return, rounds)


def rule_of_72(rate: float) -> float:
    """
    Calculate years to double investment using Rule of 72.
    
    Args:
        rate: Annual return rate (as decimal, e.g., 0.08 for 8%)
    
    Returns:
        Approximate years to double
    
    Examples:
        >>> rule_of_72(0.08)
        9.0
    """
    if rate <= 0:
        raise ValueError("Rate must be positive")
    
    return round(72 / (rate * 100), 1)


def rule_of_69(rate: float, continuous: bool = False) -> float:
    """
    More precise doubling time calculation.
    
    For continuous compounding: ln(2) / r = 69.3 / r%
    For annual compounding: ln(2) / ln(1 + r)
    
    Args:
        rate: Annual return rate (as decimal)
        continuous: Whether compounding is continuous
    
    Returns:
        Years to double
    
    Examples:
        >>> rule_of_69(0.08)
        9.01
    """
    if rate <= 0:
        raise ValueError("Rate must be positive")
    
    if continuous:
        return round(math.log(2) / rate, 2)
    else:
        return round(math.log(2) / math.log(1 + rate), 2)


# ============== Time Value of Money ==============

def time_to_target(
    present_value: float,
    target_value: float,
    rate: float,
    rounds: int = 2
) -> float:
    """
    Calculate time needed to reach a target value.
    
    Args:
        present_value: Current value
        target_value: Desired future value
        rate: Annual growth rate (as decimal)
        rounds: Decimal places to round to
    
    Returns:
        Years needed to reach target
    
    Examples:
        >>> time_to_target(10000, 20000, 0.08)
        9.01
    """
    if present_value <= 0:
        raise ValueError("Present value must be positive")
    if target_value <= present_value:
        raise ValueError("Target value must be greater than present value")
    if rate <= 0:
        raise ValueError("Rate must be positive")
    
    years = math.log(target_value / present_value) / math.log(1 + rate)
    return round(years, rounds)


def required_rate(
    present_value: float,
    target_value: float,
    years: float,
    rounds: int = 4
) -> float:
    """
    Calculate required rate to reach target in given time.
    
    Args:
        present_value: Current value
        target_value: Desired future value
        years: Time period in years
        rounds: Decimal places to round to
    
    Returns:
        Required annual rate as decimal
    
    Examples:
        >>> required_rate(10000, 20000, 5)
        0.1487
    """
    if present_value <= 0:
        raise ValueError("Present value must be positive")
    if target_value <= present_value:
        raise ValueError("Target value must be greater than present value")
    if years <= 0:
        raise ValueError("Years must be positive")
    
    rate = math.pow(target_value / present_value, 1 / years) - 1
    return round(rate, rounds)


# ============== Inflation Impact ==============

def future_value_with_inflation(
    present_value: float,
    nominal_rate: float,
    inflation_rate: float,
    years: int,
    rounds: int = 2
) -> Dict:
    """
    Calculate future value adjusted for inflation.
    
    Args:
        present_value: Current value
        nominal_rate: Nominal return rate (as decimal)
        inflation_rate: Expected inflation rate (as decimal)
        years: Investment period in years
        rounds: Decimal places to round to
    
    Returns:
        Dictionary with nominal value, real value, and purchasing power
    
    Examples:
        >>> result = future_value_with_inflation(10000, 0.08, 0.03, 10)
        >>> result['nominal_value'] > result['real_value']
        True
    """
    if present_value < 0:
        raise ValueError("Present value cannot be negative")
    if years < 0:
        raise ValueError("Years cannot be negative")
    
    nominal_fv = future_value(present_value, nominal_rate, years)
    real_rate = inflation_adjusted_return(nominal_rate, inflation_rate)
    real_fv = future_value(present_value, real_rate, years)
    
    # Purchasing power relative to today
    purchasing_power = real_fv / present_value if present_value > 0 else 1
    
    return {
        'nominal_value': nominal_fv,
        'real_value': round(real_fv, rounds),
        'real_rate': round(real_rate, 4),
        'real_rate_percent': round(real_rate * 100, 2),
        'purchasing_power': round(purchasing_power, 4),
        'inflation_impact': round(nominal_fv - real_fv, rounds)
    }


# ============== Depreciation ==============

def straight_line_depreciation(
    cost: float,
    salvage_value: float,
    useful_life: int,
    rounds: int = 2
) -> Dict:
    """
    Calculate straight-line depreciation.
    
    Args:
        cost: Initial cost of asset
        salvage_value: Expected salvage value
        useful_life: Useful life in years
        rounds: Decimal places to round to
    
    Returns:
        Dictionary with annual depreciation and book values
    
    Examples:
        >>> result = straight_line_depreciation(10000, 1000, 5)
        >>> result['annual_depreciation']
        1800.0
    """
    if cost < 0:
        raise ValueError("Cost cannot be negative")
    if salvage_value < 0:
        raise ValueError("Salvage value cannot be negative")
    if salvage_value > cost:
        raise ValueError("Salvage value cannot exceed cost")
    if useful_life <= 0:
        raise ValueError("Useful life must be positive")
    
    annual_dep = (cost - salvage_value) / useful_life
    book_values = []
    book_value = cost
    
    for year in range(1, useful_life + 1):
        book_value -= annual_dep
        book_values.append({
            'year': year,
            'depreciation': round(annual_dep, rounds),
            'book_value': round(max(book_value, salvage_value), rounds)
        })
    
    return {
        'annual_depreciation': round(annual_dep, rounds),
        'total_depreciation': round(cost - salvage_value, rounds),
        'schedule': book_values
    }


def declining_balance_depreciation(
    cost: float,
    salvage_value: float,
    useful_life: int,
    rate: float = None,
    rounds: int = 2
) -> List[Dict]:
    """
    Calculate declining balance depreciation.
    
    Args:
        cost: Initial cost of asset
        salvage_value: Expected salvage value
        useful_life: Useful life in years
        rate: Depreciation rate (default: double = 2/useful_life)
        rounds: Decimal places to round to
    
    Returns:
        List of yearly depreciation values
    
    Examples:
        >>> result = declining_balance_depreciation(10000, 1000, 5)
        >>> result[0]['depreciation'] > result[1]['depreciation']
        True
    """
    if cost < 0:
        raise ValueError("Cost cannot be negative")
    if salvage_value < 0:
        raise ValueError("Salvage value cannot be negative")
    if salvage_value > cost:
        raise ValueError("Salvage value cannot exceed cost")
    if useful_life <= 0:
        raise ValueError("Useful life must be positive")
    
    if rate is None:
        rate = 2 / useful_life  # Double declining balance
    
    schedule = []
    book_value = cost
    total_dep = 0
    
    for year in range(1, useful_life + 1):
        dep = book_value * rate
        
        # Ensure we don't go below salvage value
        if book_value - dep < salvage_value:
            dep = book_value - salvage_value
        
        total_dep += dep
        book_value -= dep
        
        schedule.append({
            'year': year,
            'depreciation': round(dep, rounds),
            'book_value': round(max(book_value, salvage_value), rounds),
            'accumulated_depreciation': round(total_dep, rounds)
        })
        
        if book_value <= salvage_value:
            break
    
    return schedule


if __name__ == "__main__":
    # Quick demo
    print("Investment Utils Demo")
    print("=" * 50)
    
    # Compound interest
    result = compound_interest(10000, 0.08, 5)
    print(f"\nCompound Interest (10000 @ 8% for 5 years):")
    print(f"  Total Amount: ${result.total_amount:,.2f}")
    print(f"  Interest Earned: ${result.total_interest:,.2f}")
    
    # SIP
    sip = sip_returns(10000, 0.12, 10)
    print(f"\nSIP Returns (10000/month @ 12% for 10 years):")
    print(f"  Total Invested: ${sip.total_invested:,.2f}")
    print(f"  Maturity Value: ${sip.maturity_value:,.2f}")
    print(f"  Returns: ${sip.total_returns:,.2f}")
    
    # CAGR
    growth = cagr(10000, 20000, 5)
    print(f"\nCAGR (10000 to 20000 in 5 years): {growth * 100:.2f}%")
    
    # Loan
    payment = loan_payment(100000, 0.06, 30)
    print(f"\nMonthly Loan Payment (100k @ 6% for 30 years): ${payment:,.2f}")
    
    # ROI
    return_rate = roi(10000, 15000)
    print(f"\nROI (10000 to 15000): {return_rate * 100:.2f}%")
    
    # Rule of 72
    years = rule_of_72(0.08)
    print(f"\nRule of 72: {years} years to double at 8%")