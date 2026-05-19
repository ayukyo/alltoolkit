"""
AllToolkit - Python Compound Interest Utilities

A zero-dependency, production-ready compound interest calculation module.
Provides comprehensive compound interest calculations, growth projections,
investment doubling analysis, and amortization schedules.
Built entirely with Python standard library.

Author: AllToolkit
License: MIT
"""

import math
from typing import List, Dict, Any, Optional, Tuple
from datetime import datetime, timedelta


class CompoundInterestError(Exception):
    """Base exception for compound interest operations."""
    pass


class InvalidPrincipalError(CompoundInterestError):
    """Raised when principal is invalid."""
    pass


class InvalidRateError(CompoundInterestError):
    """Raised when interest rate is invalid."""
    pass


class InvalidTimeError(CompoundInterestError):
    """Raised when time period is invalid."""
    pass


class InvalidFrequencyError(CompoundInterestError):
    """Raised when compounding frequency is invalid."""
    pass


# ============================================================================
# Basic Compound Interest Calculations
# ============================================================================

def compound_amount(principal: float, rate: float, time: float,
                   compounds_per_year: int = 12) -> float:
    """
    Calculate the final amount with compound interest.
    
    A = P × (1 + r/n)^(n×t)
    
    Args:
        principal: Initial investment amount
        rate: Annual interest rate as decimal (e.g., 0.05 for 5%)
        time: Time period in years
        compounds_per_year: Compounding frequency (default: 12 for monthly)
        
    Returns:
        Final amount after compound interest
        
    Raises:
        InvalidPrincipalError: If principal is negative
        InvalidRateError: If rate is less than -1
        InvalidTimeError: If time is negative
        InvalidFrequencyError: If compounds_per_year is not positive
        
    Examples:
        >>> compound_amount(1000, 0.05, 10, 12)
        1647.009497...
        >>> compound_amount(1000, 0.05, 10, 1)  # Annual compounding
        1628.894626...
    """
    if principal < 0:
        raise InvalidPrincipalError("Principal cannot be negative")
    if rate < -1:
        raise InvalidRateError("Interest rate cannot be less than -100%")
    if time < 0:
        raise InvalidTimeError("Time period cannot be negative")
    if compounds_per_year <= 0:
        raise InvalidFrequencyError("Compounding frequency must be positive")
    
    return principal * ((1 + rate / compounds_per_year) ** (compounds_per_year * time))


def compound_interest(principal: float, rate: float, time: float,
                      compounds_per_year: int = 12) -> float:
    """
    Calculate total compound interest earned.
    
    Interest = A - P = P × [(1 + r/n)^(n×t) - 1]
    
    Args:
        principal: Initial investment amount
        rate: Annual interest rate as decimal
        time: Time period in years
        compounds_per_year: Compounding frequency
        
    Returns:
        Total interest earned
        
    Examples:
        >>> compound_interest(1000, 0.05, 10, 12)
        647.009497...
    """
    amount = compound_amount(principal, rate, time, compounds_per_year)
    return amount - principal


def continuous_compound_amount(principal: float, rate: float, time: float) -> float:
    """
    Calculate final amount with continuous compounding.
    
    A = P × e^(r×t)
    
    Args:
        principal: Initial investment amount
        rate: Annual interest rate as decimal
        time: Time period in years
        
    Returns:
        Final amount with continuous compounding
        
    Examples:
        >>> continuous_compound_amount(1000, 0.05, 10)
        1648.721270...
    """
    if principal < 0:
        raise InvalidPrincipalError("Principal cannot be negative")
    if rate < -1:
        raise InvalidRateError("Interest rate cannot be less than -100%")
    if time < 0:
        raise InvalidTimeError("Time period cannot be negative")
    
    return principal * math.exp(rate * time)


def continuous_compound_interest(principal: float, rate: float, time: float) -> float:
    """
    Calculate interest with continuous compounding.
    
    Interest = P × (e^(r×t) - 1)
    
    Args:
        principal: Initial investment amount
        rate: Annual interest rate as decimal
        time: Time period in years
        
    Returns:
        Total interest earned with continuous compounding
    """
    amount = continuous_compound_amount(principal, rate, time)
    return amount - principal


# ============================================================================
# Rate Conversions
# ============================================================================

def effective_annual_rate(nominal_rate: float, compounds_per_year: int) -> float:
    """
    Convert nominal annual rate to effective annual rate (EAR).
    
    EAR = (1 + r/n)^n - 1
    
    Args:
        nominal_rate: Nominal annual rate as decimal
        compounds_per_year: Compounding frequency per year
        
    Returns:
        Effective annual rate as decimal
        
    Examples:
        >>> effective_annual_rate(0.12, 12)  # 12% nominal, monthly compounding
        0.126825...
        >>> effective_annual_rate(0.12, 4)   # Quarterly compounding
        0.125508...
    """
    if compounds_per_year <= 0:
        raise InvalidFrequencyError("Compounding frequency must be positive")
    
    return ((1 + nominal_rate / compounds_per_year) ** compounds_per_year) - 1


def nominal_rate_from_ear(ear: float, compounds_per_year: int) -> float:
    """
    Convert effective annual rate to nominal rate.
    
    r = n × [(1 + EAR)^(1/n) - 1]
    
    Args:
        ear: Effective annual rate as decimal
        compounds_per_year: Compounding frequency per year
        
    Returns:
        Nominal annual rate as decimal
        
    Examples:
        >>> nominal_rate_from_ear(0.1268, 12)
        0.1199...
    """
    if compounds_per_year <= 0:
        raise InvalidFrequencyError("Compounding frequency must be positive")
    
    return compounds_per_year * (((1 + ear) ** (1 / compounds_per_year)) - 1)


def equivalent_rate(rate: float, from_frequency: int, to_frequency: int) -> float:
    """
    Convert rate between different compounding frequencies.
    
    Args:
        rate: Nominal rate at from_frequency
        from_frequency: Original compounding frequency
        to_frequency: Target compounding frequency
        
    Returns:
        Equivalent nominal rate at target frequency
        
    Examples:
        >>> equivalent_rate(0.12, 12, 4)  # Convert monthly to quarterly
        0.1205...
    """
    if from_frequency <= 0 or to_frequency <= 0:
        raise InvalidFrequencyError("Compounding frequencies must be positive")
    
    ear = effective_annual_rate(rate, from_frequency)
    return nominal_rate_from_ear(ear, to_frequency)


def annual_percentage_yield(nominal_rate: float, compounds_per_year: int) -> float:
    """
    Calculate APY (Annual Percentage Yield) - same as EAR.
    
    APY = (1 + r/n)^n - 1
    
    Args:
        nominal_rate: Nominal annual rate as decimal
        compounds_per_year: Compounding frequency per year
        
    Returns:
        APY as decimal
    """
    return effective_annual_rate(nominal_rate, compounds_per_year)


# ============================================================================
# Doubling Time & Growth Analysis
# ============================================================================

def doubling_time(rate: float, compounds_per_year: int = 12) -> float:
    """
    Calculate exact time to double investment.
    
    t = ln(2) / [n × ln(1 + r/n)]
    
    Args:
        rate: Annual interest rate as decimal
        compounds_per_year: Compounding frequency
        
    Returns:
        Time in years to double investment
        
    Examples:
        >>> doubling_time(0.07, 12)  # 7% annual rate, monthly compounding
        9.925...
    """
    if rate <= 0:
        raise InvalidRateError("Rate must be positive for doubling calculation")
    if compounds_per_year <= 0:
        raise InvalidFrequencyError("Compounding frequency must be positive")
    
    return math.log(2) / (compounds_per_year * math.log(1 + rate / compounds_per_year))


def doubling_time_rule72(rate: float) -> float:
    """
    Estimate doubling time using Rule of 72.
    
    t ≈ 72 / (r × 100)
    
    Args:
        rate: Annual interest rate as decimal (e.g., 0.07 for 7%)
        
    Returns:
        Estimated years to double
        
    Examples:
        >>> doubling_time_rule72(0.07)
        10.285...
    """
    if rate <= 0:
        raise InvalidRateError("Rate must be positive")
    
    return 72 / (rate * 100)


def doubling_time_rule69(rate: float) -> float:
    """
    Estimate doubling time using Rule of 69 (more accurate for continuous).
    
    t ≈ 69 / (r × 100)
    
    Args:
        rate: Annual interest rate as decimal
        
    Returns:
        Estimated years to double
    """
    if rate <= 0:
        raise InvalidRateError("Rate must be positive")
    
    return 69 / (rate * 100)


def tripling_time(rate: float, compounds_per_year: int = 12) -> float:
    """
    Calculate time to triple investment.
    
    t = ln(3) / [n × ln(1 + r/n)]
    
    Args:
        rate: Annual interest rate as decimal
        compounds_per_year: Compounding frequency
        
    Returns:
        Time in years to triple investment
    """
    if rate <= 0:
        raise InvalidRateError("Rate must be positive")
    if compounds_per_year <= 0:
        raise InvalidFrequencyError("Compounding frequency must be positive")
    
    return math.log(3) / (compounds_per_year * math.log(1 + rate / compounds_per_year))


def quadrupling_time(rate: float, compounds_per_year: int = 12) -> float:
    """
    Calculate time to quadruple investment.
    
    t = ln(4) / [n × ln(1 + r/n)]
    
    Args:
        rate: Annual interest rate as decimal
        compounds_per_year: Compounding frequency
        
    Returns:
        Time in years to quadruple investment
    """
    if rate <= 0:
        raise InvalidRateError("Rate must be positive")
    if compounds_per_year <= 0:
        raise InvalidFrequencyError("Compounding frequency must be positive")
    
    return math.log(4) / (compounds_per_year * math.log(1 + rate / compounds_per_year))


def time_to_reach_target(principal: float, target: float, rate: float,
                          compounds_per_year: int = 12) -> float:
    """
    Calculate time to reach a target amount.
    
    t = ln(FV/PV) / [n × ln(1 + r/n)]
    
    Args:
        principal: Initial investment
        target: Target amount
        rate: Annual interest rate as decimal
        compounds_per_year: Compounding frequency
        
    Returns:
        Time in years to reach target
        
    Examples:
        >>> time_to_reach_target(1000, 2000, 0.07, 12)
        9.925...
    """
    if principal <= 0:
        raise InvalidPrincipalError("Principal must be positive")
    if target <= principal:
        raise CompoundInterestError("Target must be greater than principal")
    if rate <= 0:
        raise InvalidRateError("Rate must be positive")
    if compounds_per_year <= 0:
        raise InvalidFrequencyError("Compounding frequency must be positive")
    
    return math.log(target / principal) / (compounds_per_year * math.log(1 + rate / compounds_per_year))


# ============================================================================
# Required Rate Calculations
# ============================================================================

def required_rate(principal: float, target: float, time: float,
                  compounds_per_year: int = 12) -> float:
    """
    Calculate required interest rate to reach target.
    
    r = n × [(FV/PV)^(1/(n×t)) - 1]
    
    Args:
        principal: Initial investment
        target: Target amount
        time: Time period in years
        compounds_per_year: Compounding frequency
        
    Returns:
        Required annual rate as decimal
        
    Examples:
        >>> required_rate(1000, 2000, 10, 12)
        0.0695...
    """
    if principal <= 0:
        raise InvalidPrincipalError("Principal must be positive")
    if target <= 0:
        raise CompoundInterestError("Target must be positive")
    if time <= 0:
        raise InvalidTimeError("Time must be positive")
    if compounds_per_year <= 0:
        raise InvalidFrequencyError("Compounding frequency must be positive")
    
    return compounds_per_year * ((target / principal) ** (1 / (compounds_per_year * time)) - 1)


def required_principal(target: float, rate: float, time: float,
                       compounds_per_year: int = 12) -> float:
    """
    Calculate initial investment needed to reach target.
    
    P = FV / (1 + r/n)^(n×t)
    
    Args:
        target: Target amount
        rate: Annual interest rate as decimal
        time: Time period in years
        compounds_per_year: Compounding frequency
        
    Returns:
        Required initial investment
    """
    if target <= 0:
        raise CompoundInterestError("Target must be positive")
    if rate < -1:
        raise InvalidRateError("Rate cannot be less than -100%")
    if time <= 0:
        raise InvalidTimeError("Time must be positive")
    if compounds_per_year <= 0:
        raise InvalidFrequencyError("Compounding frequency must be positive")
    
    return target / ((1 + rate / compounds_per_year) ** (compounds_per_year * time))


# ============================================================================
# Compound Interest Schedule
# ============================================================================

def compound_schedule(principal: float, rate: float, years: int,
                      compounds_per_year: int = 12,
                      contributions: float = 0) -> List[Dict[str, Any]]:
    """
    Generate a compound interest schedule.
    
    Args:
        principal: Initial investment
        rate: Annual interest rate as decimal
        years: Number of years
        compounds_per_year: Compounding frequency
        contributions: Regular contribution per compounding period (default: 0)
        
    Returns:
        List of dicts with period details:
        - period: Period number
        - starting_balance: Balance at start of period
        - contribution: Contribution this period
        - interest: Interest earned this period
        - ending_balance: Balance at end of period
        - total_interest: Cumulative interest
        - total_contributions: Cumulative contributions
        
    Examples:
        >>> schedule = compound_schedule(1000, 0.05, 1, 12, 100)
        >>> len(schedule)
        12
    """
    if principal < 0:
        raise InvalidPrincipalError("Principal cannot be negative")
    if rate < -1:
        raise InvalidRateError("Rate cannot be less than -100%")
    if years <= 0:
        raise InvalidTimeError("Years must be positive")
    if compounds_per_year <= 0:
        raise InvalidFrequencyError("Compounding frequency must be positive")
    
    schedule = []
    balance = principal
    total_interest = 0.0
    total_contributions = principal
    rate_per_period = rate / compounds_per_year
    total_periods = years * compounds_per_year
    
    for period in range(1, total_periods + 1):
        starting_balance = balance
        interest = balance * rate_per_period
        balance += interest + contributions
        total_interest += interest
        total_contributions += contributions
        
        schedule.append({
            'period': period,
            'starting_balance': starting_balance,
            'contribution': contributions,
            'interest': interest,
            'ending_balance': balance,
            'total_interest': total_interest,
            'total_contributions': total_contributions
        })
    
    return schedule


def annual_compound_schedule(principal: float, rate: float, years: int,
                             compounds_per_year: int = 12,
                             contributions: float = 0) -> List[Dict[str, Any]]:
    """
    Generate an annual summary compound interest schedule.
    
    Args:
        principal: Initial investment
        rate: Annual interest rate as decimal
        years: Number of years
        compounds_per_year: Compounding frequency per year
        contributions: Regular contribution per compounding period
        
    Returns:
        List of dicts with annual summaries
    """
    full_schedule = compound_schedule(principal, rate, years, compounds_per_year, contributions)
    
    annual = []
    for year in range(1, years + 1):
        start_period = (year - 1) * compounds_per_year
        end_period = year * compounds_per_year
        
        year_schedule = full_schedule[start_period:end_period]
        
        annual.append({
            'year': year,
            'starting_balance': year_schedule[0]['starting_balance'],
            'contributions': sum(p['contribution'] for p in year_schedule),
            'interest': sum(p['interest'] for p in year_schedule),
            'ending_balance': year_schedule[-1]['ending_balance'],
            'total_interest': year_schedule[-1]['total_interest'],
            'total_contributions': year_schedule[-1]['total_contributions']
        })
    
    return annual


# ============================================================================
# Regular Contributions
# ============================================================================

def future_value_with_contributions(principal: float, rate: float, years: int,
                                     contribution: float,
                                     compounds_per_year: int = 12,
                                     contribution_timing: str = 'end') -> float:
    """
    Calculate future value with regular contributions.
    
    FV = P(1 + r/n)^(nt) + PMT × [((1 + r/n)^(nt) - 1) / (r/n)]
    
    Args:
        principal: Initial investment
        rate: Annual interest rate as decimal
        years: Number of years
        contribution: Contribution per compounding period
        compounds_per_year: Compounding frequency per year
        contribution_timing: 'end' (ordinary annuity) or 'beginning' (annuity due)
        
    Returns:
        Future value
        
    Examples:
        >>> future_value_with_contributions(1000, 0.07, 10, 100, 12)
        19595.56...
    """
    if rate < -1:
        raise InvalidRateError("Rate cannot be less than -100%")
    if years <= 0:
        raise InvalidTimeError("Years must be positive")
    if compounds_per_year <= 0:
        raise InvalidFrequencyError("Compounding frequency must be positive")
    
    rate_per_period = rate / compounds_per_year
    periods = years * compounds_per_year
    
    # Future value of principal
    fv_principal = principal * ((1 + rate_per_period) ** periods)
    
    # Future value of contributions (annuity)
    if rate_per_period == 0:
        fv_contributions = contribution * periods
    else:
        fv_contributions = contribution * (((1 + rate_per_period) ** periods - 1) / rate_per_period)
        
        if contribution_timing == 'beginning':
            fv_contributions *= (1 + rate_per_period)
    
    return fv_principal + fv_contributions


def required_contribution(target: float, principal: float, rate: float, years: int,
                          compounds_per_year: int = 12,
                          contribution_timing: str = 'end') -> float:
    """
    Calculate required periodic contribution to reach target.
    
    Args:
        target: Target amount
        principal: Initial investment
        rate: Annual interest rate as decimal
        years: Number of years
        compounds_per_year: Compounding frequency
        contribution_timing: 'end' or 'beginning'
        
    Returns:
        Required contribution per period
        
    Examples:
        >>> required_contribution(100000, 10000, 0.07, 20, 12)
        155.35...
    """
    if target <= 0:
        raise CompoundInterestError("Target must be positive")
    if years <= 0:
        raise InvalidTimeError("Years must be positive")
    if compounds_per_year <= 0:
        raise InvalidFrequencyError("Compounding frequency must be positive")
    
    rate_per_period = rate / compounds_per_year
    periods = years * compounds_per_year
    
    # Future value of principal
    fv_principal = principal * ((1 + rate_per_period) ** periods)
    
    # Required from contributions
    fv_needed = target - fv_principal
    
    if fv_needed <= 0:
        return 0.0  # Already exceeds target
    
    if rate_per_period == 0:
        return fv_needed / periods
    
    annuity_factor = ((1 + rate_per_period) ** periods - 1) / rate_per_period
    
    if contribution_timing == 'beginning':
        annuity_factor *= (1 + rate_per_period)
    
    return fv_needed / annuity_factor


# ============================================================================
# Inflation-Adjusted Returns
# ============================================================================

def real_rate(nominal_rate: float, inflation_rate: float) -> float:
    """
    Calculate real interest rate adjusted for inflation.
    
    Real Rate = (1 + nominal) / (1 + inflation) - 1
    
    Args:
        nominal_rate: Nominal annual rate as decimal
        inflation_rate: Annual inflation rate as decimal
        
    Returns:
        Real interest rate as decimal
        
    Examples:
        >>> real_rate(0.08, 0.03)
        0.0485...
    """
    if inflation_rate <= -1:
        raise InvalidRateError("Inflation rate cannot be -100% or lower")
    
    return (1 + nominal_rate) / (1 + inflation_rate) - 1


def inflation_adjusted_amount(principal: float, nominal_rate: float,
                               inflation_rate: float, time: float,
                               compounds_per_year: int = 12) -> float:
    """
    Calculate future value in today's dollars (inflation-adjusted).
    
    Args:
        principal: Initial investment
        nominal_rate: Nominal annual rate as decimal
        inflation_rate: Annual inflation rate as decimal
        time: Time period in years
        compounds_per_year: Compounding frequency
        
    Returns:
        Inflation-adjusted future value
    """
    nominal_amount = compound_amount(principal, nominal_rate, time, compounds_per_year)
    purchasing_power = nominal_amount / ((1 + inflation_rate) ** time)
    return purchasing_power


def purchasing_power(principal: float, inflation_rate: float, time: float) -> float:
    """
    Calculate purchasing power of money after inflation (no investment return).
    
    Args:
        principal: Initial amount
        inflation_rate: Annual inflation rate as decimal
        time: Time period in years
        
    Returns:
        Purchasing power in today's dollars
    """
    return principal / ((1 + inflation_rate) ** time)


# ============================================================================
# Compound Interest Comparisons
# ============================================================================

def compare_compounding_frequencies(principal: float, rate: float, time: float) -> Dict[str, float]:
    """
    Compare returns across different compounding frequencies.
    
    Args:
        principal: Initial investment
        rate: Annual interest rate as decimal
        time: Time period in years
        
    Returns:
        Dictionary with amounts for each compounding frequency:
        - annually: 1x/year
        - semiannually: 2x/year
        - quarterly: 4x/year
        - monthly: 12x/year
        - daily: 365x/year
        - continuous: Continuous compounding
    """
    frequencies = {
        'annually': 1,
        'semiannually': 2,
        'quarterly': 4,
        'monthly': 12,
        'weekly': 52,
        'daily': 365,
        'continuous': None
    }
    
    results = {}
    for name, freq in frequencies.items():
        if freq is None:
            results[name] = continuous_compound_amount(principal, rate, time)
        else:
            results[name] = compound_amount(principal, rate, time, freq)
    
    return results


def compare_rates(principal: float, rates: List[float], time: float,
                  compounds_per_year: int = 12) -> Dict[float, Dict[str, float]]:
    """
    Compare returns across different interest rates.
    
    Args:
        principal: Initial investment
        rates: List of interest rates as decimals
        time: Time period in years
        compounds_per_year: Compounding frequency
        
    Returns:
        Dictionary with details for each rate
    """
    results = {}
    
    for rate in rates:
        amount = compound_amount(principal, rate, time, compounds_per_year)
        interest = amount - principal
        
        results[rate] = {
            'amount': amount,
            'interest': interest,
            'return_pct': (interest / principal) * 100 if principal > 0 else 0
        }
    
    return results


# ============================================================================
# Practical Helper Functions
# ============================================================================

def investment_summary(principal: float, rate: float, years: int,
                       compounds_per_year: int = 12,
                       contribution: float = 0,
                       inflation_rate: Optional[float] = None) -> Dict[str, Any]:
    """
    Generate comprehensive investment summary.
    
    Args:
        principal: Initial investment
        rate: Annual interest rate as decimal
        years: Investment period in years
        compounds_per_year: Compounding frequency
        contribution: Regular contribution per period
        inflation_rate: Optional inflation rate for real returns
        
    Returns:
        Dictionary with complete investment analysis
    """
    # Basic calculations
    final_amount = future_value_with_contributions(
        principal, rate, years, contribution, compounds_per_year
    )
    total_contributions = principal + (contribution * years * compounds_per_year)
    total_interest = final_amount - total_contributions
    
    # Schedule
    schedule = annual_compound_schedule(
        principal, rate, years, compounds_per_year, contribution
    )
    
    # Doubling time
    if rate > 0:
        double_time = doubling_time(rate, compounds_per_year)
    else:
        double_time = float('inf')
    
    # Effective rate
    ear = effective_annual_rate(rate, compounds_per_year)
    
    result = {
        'principal': principal,
        'annual_rate': rate,
        'effective_annual_rate': ear,
        'compounding_frequency': compounds_per_year,
        'years': years,
        'contribution_per_period': contribution,
        'total_contributions': total_contributions,
        'final_amount': final_amount,
        'total_interest': total_interest,
        'total_return_pct': (total_interest / total_contributions * 100) if total_contributions > 0 else 0,
        'annualized_return': (pow(final_amount / principal, 1/years) - 1) if principal > 0 else 0,
        'doubling_time_years': double_time,
        'schedule': schedule
    }
    
    # Add inflation-adjusted figures if provided
    if inflation_rate is not None:
        real_r = real_rate(rate, inflation_rate)
        real_final = inflation_adjusted_amount(principal, rate, inflation_rate, years, compounds_per_year)
        
        result['inflation_rate'] = inflation_rate
        result['real_rate'] = real_r
        result['real_final_value'] = real_final
        result['purchasing_power_loss'] = final_amount - real_final
    
    return result


def savings_goal_analysis(goal: float, principal: float, rate: float,
                          years: int, compounds_per_year: int = 12) -> Dict[str, Any]:
    """
    Analyze how to reach a savings goal.
    
    Args:
        goal: Target amount
        principal: Initial investment
        rate: Annual interest rate as decimal
        years: Time horizon in years
        compounds_per_year: Compounding frequency
        
    Returns:
        Dictionary with goal analysis
    """
    # Future value of current principal
    fv_principal = compound_amount(principal, rate, years, compounds_per_year)
    
    # Shortfall
    shortfall = max(0, goal - fv_principal)
    
    # Required contribution
    required_contrib = required_contribution(goal, principal, rate, years, compounds_per_year)
    
    # Time to reach goal with current setup
    if principal > 0 and fv_principal >= goal:
        if principal >= goal:
            time_to_goal = 0  # Already met the goal
        else:
            time_to_goal = time_to_reach_target(principal, goal, rate, compounds_per_year)
    else:
        time_to_goal = years
    
    # Required rate if no contributions
    required_r = required_rate(principal, goal, years, compounds_per_year) if principal > 0 else None
    
    return {
        'goal': goal,
        'principal': principal,
        'annual_rate': rate,
        'years': years,
        'future_value_of_principal': fv_principal,
        'shortfall': shortfall,
        'required_contribution_per_period': required_contrib,
        'required_contribution_per_month': required_contrib * (compounds_per_year / 12) if compounds_per_year >= 12 else required_contrib,
        'time_to_reach_goal_years': time_to_goal,
        'required_rate_without_contributions': required_r,
        'on_track': fv_principal >= goal
    }


def compound_interest_table(principal: float, rate: float, years: int,
                            compounds_per_year: int = 12) -> str:
    """
    Generate a formatted compound interest table.
    
    Args:
        principal: Initial investment
        rate: Annual interest rate as decimal
        years: Number of years
        compounds_per_year: Compounding frequency
        
    Returns:
        Formatted string table
    """
    schedule = annual_compound_schedule(principal, rate, years, compounds_per_year)
    
    lines = []
    lines.append(f"\n{'='*70}")
    lines.append(f"COMPOUND INTEREST SCHEDULE")
    lines.append(f"{'='*70}")
    lines.append(f"Principal:          ${principal:,.2f}")
    lines.append(f"Annual Rate:         {rate*100:.2f}%")
    lines.append(f"Effective Rate:      {effective_annual_rate(rate, compounds_per_year)*100:.4f}%")
    lines.append(f"Compounding:         {compounds_per_year}x per year")
    lines.append(f"{'='*70}")
    lines.append(f"{'Year':<6}{'Start':>12}{'Interest':>12}{'End':>14}{'Total Int':>14}")
    lines.append(f"{'-'*70}")
    
    for row in schedule:
        lines.append(
            f"{row['year']:<6}"
            f"${row['starting_balance']:>10,.2f}"
            f"${row['interest']:>10,.2f}"
            f"${row['ending_balance']:>12,.2f}"
            f"${row['total_interest']:>12,.2f}"
        )
    
    lines.append(f"{'='*70}")
    final = schedule[-1]
    lines.append(f"Total Interest Earned: ${final['total_interest']:,.2f}")
    lines.append(f"Total Return:           {(final['total_interest']/principal)*100:.2f}%")
    lines.append(f"{'='*70}\n")
    
    return '\n'.join(lines)


# ============================================================================
# Compounding Frequency Helpers
# ============================================================================

COMPOUNDING_FREQUENCIES = {
    'annual': 1,
    'annually': 1,
    'semiannual': 2,
    'semiannually': 2,
    'quarterly': 4,
    'monthly': 12,
    'weekly': 52,
    'daily': 365,
    'continuous': None  # Special case
}


def get_compounding_frequency(name: str) -> Optional[int]:
    """
    Get compounding frequency by name.
    
    Args:
        name: Frequency name (annual, monthly, daily, continuous, etc.)
        
    Returns:
        Frequency per year, or None for continuous
        
    Raises:
        InvalidFrequencyError: If name is not recognized
    """
    name_lower = name.lower().strip()
    
    if name_lower not in COMPOUNDING_FREQUENCIES:
        valid = ', '.join(COMPOUNDING_FREQUENCIES.keys())
        raise InvalidFrequencyError(f"Unknown frequency '{name}'. Valid options: {valid}")
    
    return COMPOUNDING_FREQUENCIES[name_lower]


# ============================================================================
# Module Constants
# ============================================================================

VERSION = "1.0.0"
AUTHOR = "AllToolkit"
LICENSE = "MIT"