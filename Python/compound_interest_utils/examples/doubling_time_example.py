"""
Example: Doubling Time and Growth Analysis

Demonstrates investment doubling time calculations.
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mod import (
    doubling_time, doubling_time_rule72, doubling_time_rule69,
    tripling_time, quadrupling_time, time_to_reach_target
)


def main():
    print("=" * 60)
    print("DOUBLING TIME EXAMPLES")
    print("=" * 60)
    
    rates = [0.03, 0.05, 0.07, 0.10, 0.12]  # Various rates
    
    print("\nCompare exact vs Rule of 72 vs Rule of 69:")
    print("-" * 60)
    print(f"{'Rate':<8}{'Exact':>12}{'Rule 72':>12}{'Rule 69':>12}{'Diff':>10}")
    print("-" * 60)
    
    for rate in rates:
        exact = doubling_time(rate, 12)
        rule72 = doubling_time_rule72(rate)
        rule69 = doubling_time_rule69(rate)
        diff = abs(exact - rule72)
        
        print(f"{rate*100:.0f}%"
              f"{exact:>10.2f}y"
              f"{rule72:>10.2f}y"
              f"{rule69:>10.2f}y"
              f"{diff:>8.2f}y")
    
    # Doubling, Tripling, Quadrupling at 7%
    print("\n" + "=" * 60)
    print("\nGrowth milestones at 7% annual rate:")
    print("-" * 60)
    
    rate = 0.07
    double = doubling_time(rate, 12)
    triple = tripling_time(rate, 12)
    quadruple = quadrupling_time(rate, 12)
    
    print(f"  Time to double (2x):   {double:.2f} years")
    print(f"  Time to triple (3x):   {triple:.2f} years")
    print(f"  Time to quadruple (4x): {quadruple:.2f} years")
    print(f"\n  Note: Quadruple time = 2 × Double time = {2*double:.2f} years")
    
    # Time to reach custom target
    print("\n" + "=" * 60)
    print("\nTime to reach specific targets:")
    print("-" * 60)
    
    principal = 1000
    targets = [1500, 2000, 3000, 5000, 10000]
    
    for target in targets:
        time = time_to_reach_target(principal, target, rate, 12)
        multiplier = target / principal
        print(f"  ${principal} → ${target} ({multiplier:.0f}x): {time:.2f} years")
    
    print("\n" + "=" * 60)


if __name__ == '__main__':
    main()