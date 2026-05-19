"""
Example: Basic Compound Interest Calculations

Demonstrates fundamental compound interest calculations.
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mod import (
    compound_amount, compound_interest,
    continuous_compound_amount, continuous_compound_interest,
    effective_annual_rate
)


def main():
    print("=" * 60)
    print("BASIC COMPOUND INTEREST EXAMPLES")
    print("=" * 60)
    
    principal = 1000  # $1,000 initial investment
    rate = 0.05       # 5% annual rate
    years = 10        # 10 years
    
    # Different compounding frequencies
    frequencies = ['annually', 'quarterly', 'monthly', 'daily']
    
    print(f"\nPrincipal: ${principal}")
    print(f"Annual Rate: {rate*100}%")
    print(f"Time: {years} years")
    print("\n" + "-" * 60)
    
    for freq_name in frequencies:
        freq_map = {'annually': 1, 'quarterly': 4, 'monthly': 12, 'daily': 365}
        freq = freq_map[freq_name]
        
        amount = compound_amount(principal, rate, years, freq)
        interest = compound_interest(principal, rate, years, freq)
        
        print(f"\n{freq_name.upper()} COMPOUNDING ({freq}x/year):")
        print(f"  Final Amount:    ${amount:.2f}")
        print(f"  Interest Earned: ${interest:.2f}")
        print(f"  Return:          {(interest/principal)*100:.2f}%")
    
    # Continuous compounding
    print("\n" + "-" * 60)
    print("\nCONTINUOUS COMPOUNDING:")
    amount = continuous_compound_amount(principal, rate, years)
    interest = continuous_compound_interest(principal, rate, years)
    print(f"  Final Amount:    ${amount:.2f}")
    print(f"  Interest Earned: ${interest:.2f}")
    
    # Effective Annual Rate comparison
    print("\n" + "-" * 60)
    print("\nEFFECTIVE ANNUAL RATES:")
    print(f"  Monthly:     {effective_annual_rate(rate, 12)*100:.4f}%")
    print(f"  Quarterly:   {effective_annual_rate(rate, 4)*100:.4f}%")
    print(f"  Annual:      {effective_annual_rate(rate, 1)*100:.2f}%")
    
    print("\n" + "=" * 60)


if __name__ == '__main__':
    main()