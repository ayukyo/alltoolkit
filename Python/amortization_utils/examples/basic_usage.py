#!/usr/bin/env python3
"""
AllToolkit - Amortization Utils Examples

Real-world examples demonstrating amortization calculations.

Author: AllToolkit
License: MIT
"""

import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from datetime import date
from amortization_utils.mod import (
    AmortizationUtils,
    calculate_mortgage_payment,
    generate_mortgage_schedule
)


def example_basic_mortgage():
    """Example: Basic mortgage calculation."""
    print("=" * 60)
    print("Example 1: Basic Mortgage Calculation")
    print("=" * 60)
    
    # Home loan: $300,000 at 6.5% for 30 years
    payment = calculate_mortgage_payment(
        principal=300000,
        annual_rate=6.5,  # Percentage form for convenience function
        years=30
    )
    
    print(f"\nLoan Details:")
    print(f"  Principal: $300,000")
    print(f"  Rate: 6.5%")
    print(f"  Term: 30 years")
    print(f"\nMonthly Payment: ${payment:,.2f}")


def example_full_amortization_schedule():
    """Example: Generate full amortization schedule."""
    print("\n" + "=" * 60)
    print("Example 2: Full Amortization Schedule")
    print("=" * 60)
    
    schedule = AmortizationUtils.generate_schedule(
        principal=250000,
        annual_rate=0.06,  # 6%
        term_months=360,
        start_date=date(2024, 1, 1)
    )
    
    print(f"\nLoan: $250,000 at 6% for 30 years")
    print(f"Monthly Payment: ${schedule.monthly_payment:,.2f}")
    print(f"Total Payment: ${schedule.total_payment:,.2f}")
    print(f"Total Interest: ${schedule.total_interest:,.2f}")
    print(f"Interest/Principal Ratio: {schedule.interest_to_principal_ratio:.1%}")
    
    print(f"\nFirst 6 Payments:")
    print("-" * 85)
    print(f"{'#':<4} {'Date':<12} {'Payment':<12} {'Principal':<12} {'Interest':<12} {'Balance':<15}")
    print("-" * 85)
    
    for p in schedule.payments[:6]:
        date_str = p.payment_date.strftime('%Y-%m-%d') if p.payment_date else 'N/A'
        print(f"{p.payment_number:<4} {date_str:<12} ${p.payment_amount:<11,.2f} "
              f"${p.principal:<11,.2f} ${p.interest:<11,.2f} ${p.remaining_balance:<14,.2f}")
    
    print(f"\n... {len(schedule.payments) - 12} payments omitted ...\n")
    
    print("Last 6 Payments:")
    print("-" * 85)
    for p in schedule.payments[-6:]:
        date_str = p.payment_date.strftime('%Y-%m-%d') if p.payment_date else 'N/A'
        print(f"{p.payment_number:<4} {date_str:<12} ${p.payment_amount:<11,.2f} "
              f"${p.principal:<11,.2f} ${p.interest:<11,.2f} ${p.remaining_balance:<14,.2f}")


def example_extra_payments():
    """Example: Impact of extra monthly payments."""
    print("\n" + "=" * 60)
    print("Example 3: Extra Payment Impact Analysis")
    print("=" * 60)
    
    scenarios = [
        ("No extra", 0),
        ("$100 extra", 100),
        ("$200 extra", 200),
        ("$500 extra", 500),
    ]
    
    print(f"\nLoan: $300,000 at 6% for 30 years")
    print(f"\n{'Scenario':<15} {'Term':<12} {'Saved':<12} {'Interest Saved':<20}")
    print("-" * 60)
    
    for name, extra in scenarios:
        result = AmortizationUtils.calculate_extra_payment_impact(
            principal=300000,
            annual_rate=0.06,
            term_months=360,
            extra_monthly=extra
        )
        
        years = result['new_term_months'] // 12
        months = result['new_term_months'] % 12
        term_str = f"{years}y {months}m"
        
        print(f"{name:<15} {term_str:<12} {result['months_saved']:<12} ${result['interest_saved']:>15,.2f}")


def example_lump_sum_payoff():
    """Example: Lump sum early payoff."""
    print("\n" + "=" * 60)
    print("Example 4: Lump Sum Early Payoff Analysis")
    print("=" * 60)
    
    print(f"\nLoan: $400,000 at 7% for 30 years")
    print(f"After 5 years of payments, considering $100,000 lump sum payoff\n")
    
    result = AmortizationUtils.calculate_early_payoff(
        principal=400000,
        annual_rate=0.07,
        term_months=360,
        months_paid=60,
        extra_payment=100000
    )
    
    print(f"Current Remaining Balance: ${result['remaining_balance']:,.2f}")
    print(f"Lump Sum Payment: ${result['extra_payment']:,.2f}")
    print(f"New Balance After Payment: ${result['new_balance']:,.2f}")
    print(f"\nOriginal Months Remaining: {result['original_months_remaining']}")
    print(f"New Months Remaining: {result['new_months_remaining']}")
    print(f"Months Saved: {result['months_saved']} ({result['months_saved'] // 12} years)")
    print(f"\nInterest Saved: ${result['interest_saved']:,.2f}")


def example_refinance_analysis():
    """Example: Refinance comparison."""
    print("\n" + "=" * 60)
    print("Example 5: Refinance Analysis")
    print("=" * 60)
    
    print(f"\nCurrent Loan: $350,000 remaining at 7.5% with 25 years left")
    print(f"Refinance Option: 5.5% for 30 years with $8,000 closing costs\n")
    
    comparison = AmortizationUtils.calculate_refinance_comparison(
        current_balance=350000,
        current_rate=0.075,
        current_remaining_months=300,
        new_rate=0.055,
        new_term_months=360,
        closing_costs=8000
    )
    
    print("CURRENT LOAN:")
    print(f"  Balance: ${comparison['current']['balance']:,.2f}")
    print(f"  Rate: {comparison['current']['rate']:.3f}%")
    print(f"  Remaining: {comparison['current']['remaining_months']} months")
    print(f"  Monthly Payment: ${comparison['current']['monthly_payment']:,.2f}")
    print(f"  Remaining Interest: ${comparison['current']['total_remaining_interest']:,.2f}")
    
    print("\nREFINANCE OPTION:")
    print(f"  New Rate: {comparison['refinance']['new_rate']:.3f}%")
    print(f"  New Term: {comparison['refinance']['new_term_months']} months")
    print(f"  Monthly Payment: ${comparison['refinance']['monthly_payment']:,.2f}")
    print(f"  Total Interest: ${comparison['refinance']['total_interest']:,.2f}")
    print(f"  Closing Costs: ${comparison['refinance']['closing_costs']:,.2f}")
    
    print("\nCOMPARISON:")
    comp = comparison['comparison']
    print(f"  Monthly Savings: ${comp['monthly_payment_difference']:,.2f}")
    print(f"  Interest Difference: ${comp['interest_difference']:,.2f}")
    print(f"  Net Savings: ${comp['net_savings']:,.2f}")
    
    if comp['break_even_months']:
        print(f"  Break-even: {comp['break_even_months']} months")
    
    print(f"  RECOMMENDATION: {'Refinance' if comp['is_worth_it'] else 'Keep current loan'}")


def example_affordability():
    """Example: Home affordability calculation."""
    print("\n" + "=" * 60)
    print("Example 6: Home Affordability Calculator")
    print("=" * 60)
    
    print(f"\nAssuming:")
    print(f"  Monthly budget for mortgage: $2,500")
    print(f"  Interest rate: 6.5%")
    print(f"  Loan term: 30 years")
    print(f"  Down payment: $80,000\n")
    
    result = AmortizationUtils.calculate_affordable_principal(
        monthly_payment=2500,
        annual_rate=0.065,
        term_months=360,
        down_payment=80000
    )
    
    print(f"Based on your budget:")
    print(f"  Maximum Loan Amount: ${result['loan_amount']:,.2f}")
    print(f"  Down Payment: ${result['down_payment']:,.2f}")
    print(f"  Total Home Price: ${result['total_home_price']:,.2f}")
    print(f"  Down Payment Percentage: {result['down_payment_percentage']:.1f}%")


def example_find_term():
    """Example: Find term for target payment."""
    print("\n" + "=" * 60)
    print("Example 7: Find Loan Term for Target Payment")
    print("=" * 60)
    
    print(f"\nLoan: $50,000 at 8% interest")
    print(f"Target monthly payment: $500\n")
    
    result = AmortizationUtils.find_term_for_payment(
        principal=50000,
        annual_rate=0.08,
        target_payment=500
    )
    
    if result['possible']:
        print(f"Loan will be paid off in: {result['term_months']} months ({result['years']} years)")
        print(f"Actual monthly payment: ${result['monthly_payment']:,.2f}")
        print(f"Total interest: ${result['total_interest']:,.2f}")
        print(f"Total payment: ${result['total_payment']:,.2f}")
    else:
        print(f"Payment too low! Minimum payment: ${result['minimum_payment']:,.2f}")


def example_year_summary():
    """Example: Year-by-year summary."""
    print("\n" + "=" * 60)
    print("Example 8: Year-by-Year Summary")
    print("=" * 60)
    
    schedule = AmortizationUtils.generate_schedule(
        principal=200000,
        annual_rate=0.05,
        term_months=60,  # 5 year loan
        start_date=date(2024, 1, 1)
    )
    
    print(f"\nLoan: $200,000 at 5% for 5 years\n")
    print(f"{'Year':<8} {'Principal':<15} {'Interest':<15} {'Total':<15}")
    print("-" * 55)
    
    for year_summary in schedule.summarize_by_year():
        print(f"{year_summary['year']:<8} ${year_summary['total_principal']:>13,.2f} "
              f"${year_summary['total_interest']:>13,.2f} "
              f"${year_summary['total_payments']:>13,.2f}")


def example_apr():
    """Example: APR calculation."""
    print("\n" + "=" * 60)
    print("Example 9: APR Calculation")
    print("=" * 60)
    
    scenarios = [
        ("No fees", 0),
        ("$3,000 fees", 3000),
        ("$5,000 fees", 5000),
        ("$10,000 fees", 10000),
    ]
    
    print(f"\nLoan: $250,000 at 6% for 30 years")
    print(f"Monthly payment: $1,498.88\n")
    
    print(f"{'Fees':<15} {'APR':<10}")
    print("-" * 25)
    
    for name, fees in scenarios:
        apr = AmortizationUtils.calculate_apr(
            principal=250000,
            monthly_payment=1498.88,
            term_months=360,
            fees=fees
        )
        print(f"{name:<15} {apr * 100:.3f}%")


def main():
    """Run all examples."""
    example_basic_mortgage()
    example_full_amortization_schedule()
    example_extra_payments()
    example_lump_sum_payoff()
    example_refinance_analysis()
    example_affordability()
    example_find_term()
    example_year_summary()
    example_apr()
    
    print("\n" + "=" * 60)
    print("All examples completed!")
    print("=" * 60)


if __name__ == '__main__':
    main()