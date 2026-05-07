#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""AllToolkit - Verhoeff Utilities Examples

Basic usage examples for the Verhoeff check digit algorithm.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from verhoeff_utils.mod import (
    compute_check_digit,
    validate,
    append_check_digit,
    detect_single_error,
    detect_transposition_error,
    analyze_error,
    compare_with_luhn,
    show_computation_steps,
    explain_algorithm,
)


def example_basic_usage():
    """Demonstrate basic Verhoeff operations."""
    print("=" * 60)
    print("Basic Verhoeff Operations")
    print("=" * 60)
    
    # Compute check digit
    number = "12345"
    check = compute_check_digit(number)
    print(f"\n1. Compute check digit for '{number}': {check}")
    
    # Append check digit
    full_number = append_check_digit(number)
    print(f"   Full number with check digit: {full_number}")
    
    # Validate
    is_valid = validate(full_number)
    print(f"   Validate '{full_number}': {is_valid}")
    
    # Validate wrong number
    is_valid_wrong = validate("123450")
    print(f"   Validate '123450' (wrong): {is_valid_wrong}")
    
    print("\n" + "-" * 60)


def example_error_detection():
    """Demonstrate error detection capabilities."""
    print("\n" + "=" * 60)
    print("Error Detection Examples")
    print("=" * 60)
    
    original = "123451"
    
    # Single digit error
    print(f"\nOriginal: {original}")
    
    # Single digit substitution
    modified1 = "123351"  # 4 -> 3
    analysis1 = analyze_error(original, modified1)
    print(f"\nSingle substitution: {original} -> {modified1}")
    print(f"   Error type: {analysis1['error_type']}")
    print(f"   Position: {analysis1['position']}")
    print(f"   Details: {analysis1['details']}")
    
    # Transposition error
    modified2 = "124351"  # 3 <-> 4
    analysis2 = analyze_error(original, modified2)
    print(f"\nTransposition: {original} -> {modified2}")
    print(f"   Error type: {analysis2['error_type']}")
    print(f"   Position: {analysis2['position']}")
    
    # Multiple errors
    modified3 = "123352"
    analysis3 = analyze_error(original, modified3)
    print(f"\nMultiple errors: {original} -> {modified3}")
    print(f"   Error type: {analysis3['error_type']}")
    
    print("\n" + "-" * 60)


def example_comparison_with_luhn():
    """Compare Verhoeff with Luhn algorithm."""
    print("\n" + "=" * 60)
    print("Verhoeff vs Luhn Comparison")
    print("=" * 60)
    
    numbers = ["12345", "987654321", "11111", "999"]
    
    for num in numbers:
        result = compare_with_luhn(num)
        print(f"\nNumber: {num}")
        print(f"   Verhoeff check digit: {result['verhoeff_check']}")
        print(f"   Luhn check digit: {result['luhn_check']}")
        print(f"   Verhoeff full: {result['verhoeff_full']}")
        print(f"   Luhn full: {result['luhn_full']}")
    
    print("\n" + "-" * 60)


def example_computation_steps():
    """Show step-by-step computation."""
    print("\n" + "=" * 60)
    print("Step-by-Step Computation")
    print("=" * 60)
    
    print(show_computation_steps("12345"))
    
    print("-" * 60)


def example_real_world_use_cases():
    """Demonstrate real-world use cases."""
    print("\n" + "=" * 60)
    print("Real-World Use Cases")
    print("=" * 60)
    
    # Case 1: Generating ID numbers
    print("\nCase 1: Generating valid ID numbers")
    base_ids = ["10001", "10002", "10003", "10004", "10005"]
    for base_id in base_ids:
        full_id = append_check_digit(base_id)
        print(f"   Base: {base_id} -> Full ID: {full_id}")
    
    # Case 2: Validating user input
    print("\nCase 2: Validating user input")
    user_inputs = ["100019", "100018", "100011", "invalid"]
    for inp in user_inputs:
        valid = validate(inp)
        status = "✓ Valid" if valid else "✗ Invalid"
        print(f"   Input: {inp:12} -> {status}")
    
    # Case 3: Detecting data entry errors
    print("\nCase 3: Detecting data entry errors")
    stored_value = "123451"
    entered_values = ["123451", "123351", "124351", "12342"]  # correct, typo, swap, partial
    
    print(f"   Stored value: {stored_value}")
    for entered in entered_values:
        if entered == stored_value:
            print(f"   Entered: {entered:12} -> ✓ Correct")
        elif not validate(entered):
            print(f"   Entered: {entered:12} -> ✗ Fails check (error detected)")
        else:
            print(f"   Entered: {entered:12} -> ? Valid but different")
    
    print("\n" + "-" * 60)


def example_why_verhoeff():
    """Explain why Verhoeff is superior to Luhn."""
    print("\n" + "=" * 60)
    print("Why Choose Verhoeff Over Luhn?")
    print("=" * 60)
    
    print("""
Verhoeff Algorithm Advantages:

1. Catches ALL single-digit errors
   - Luhn misses about 10% of single-digit errors
   - Verhoeff catches 100%

2. Catches ALL adjacent transposition errors
   - Luhn catches most, but misses some (like 09 <-> 90)
   - Verhoeff catches 100%

3. Better for critical applications
   - ID numbers, account numbers, product codes
   - Any system where data integrity is crucial

4. Similar computational complexity
   - Both are O(n) time complexity
   - Verhoeff uses lookup tables instead of arithmetic

When to use Verhoeff:
- Financial systems (account numbers)
- Healthcare (patient IDs)
- Government (ID numbers)
- Inventory systems (product codes)
- Any system with manual data entry

When Luhn might be sufficient:
- Credit card numbers (industry standard)
- Quick checksum for non-critical data
- When backward compatibility is needed
""")
    
    print("-" * 60)


def main():
    """Run all examples."""
    example_basic_usage()
    example_error_detection()
    example_comparison_with_luhn()
    example_computation_steps()
    example_real_world_use_cases()
    example_why_verhoeff()
    
    print("\n" + "=" * 60)
    print("For more information:")
    print("=" * 60)
    print("\nRun: print(explain_algorithm())")
    print()


if __name__ == "__main__":
    main()