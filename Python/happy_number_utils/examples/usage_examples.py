#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""AllToolkit - Happy Number Utilities Examples

Usage examples demonstrating all features of the happy_number_utils module.

Author: AllToolkit
License: MIT
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mod import (
    digit_square_sum,
    digit_sum,
    is_happy,
    is_unhappy,
    analyze_number,
    get_happy_sequence,
    count_steps_to_happy,
    happy_numbers_in_range,
    unhappy_numbers_in_range,
    generate_happy_numbers,
    nth_happy_number,
    happy_numbers_up_to,
    is_prime,
    is_happy_prime,
    happy_primes_in_range,
    nth_happy_prime,
    analyze_range,
    analyze_properties,
    find_happy_palindromes,
    find_happy_power_of_10,
    find_smallest_happy_with_digits,
    find_largest_happy_with_digits,
    get_unhappy_cycle,
    analyze_cycle_structure,
    get_cycle_for_number,
    batch_check_happy,
    happy_number_report,
    happy_density_estimate,
    is_happy_base_equivalent,
    get_happy_numbers_by_digit_sum,
    NumberType,
)


def example_basic_checks():
    """Basic happy number checks."""
    print("\n" + "=" * 50)
    print("Example 1: Basic Happy Number Checks")
    print("=" * 50)
    
    numbers = [19, 7, 13, 4, 2, 100, 123]
    
    print("\nChecking if numbers are happy:")
    for n in numbers:
        status = "✓ Happy" if is_happy(n) else "✗ Unhappy"
        print(f"  {n}: {status}")
    
    print("\nDigit square sum calculation:")
    print(f"  digit_square_sum(19) = 1² + 9² = {digit_square_sum(19)}")
    print(f"  digit_square_sum(123) = 1² + 2² + 3² = {digit_square_sum(123)}")


def example_sequences():
    """Happy number sequences."""
    print("\n" + "=" * 50)
    print("Example 2: Happy Number Sequences")
    print("=" * 50)
    
    # Show sequences for different numbers
    test_numbers = [19, 7, 100, 4, 13]
    
    for n in test_numbers:
        result = analyze_number(n)
        print(f"\n{result.to_summary()}")
        print(f"  Sequence: {result.get_sequence_string()}")


def example_happy_numbers_in_range():
    """Finding happy numbers in ranges."""
    print("\n" + "=" * 50)
    print("Example 3: Happy Numbers in Ranges")
    print("=" * 50)
    
    # Find happy numbers from 1 to 100
    happy_nums = happy_numbers_in_range(1, 100)
    print(f"\nHappy numbers in [1, 100]: {happy_nums}")
    print(f"Count: {len(happy_nums)}")
    
    # Find happy numbers in a custom range
    happy_nums = happy_numbers_in_range(100, 200)
    print(f"\nHappy numbers in [100, 200]: {happy_nums}")
    print(f"Count: {len(happy_nums)}")


def example_nth_happy_numbers():
    """Finding nth happy numbers."""
    print("\n" + "=" * 50)
    print("Example 4: nth Happy Numbers")
    print("=" * 50)
    
    print("\nFinding specific happy numbers by index:")
    indices = [1, 5, 10, 50, 100, 500]
    for i in indices:
        happy_num = nth_happy_number(i)
        print(f"  {i}th happy number: {happy_num}")
    
    print("\nGenerating first 10 happy numbers:")
    gen = generate_happy_numbers(10)
    print(f"  {list(gen)}")


def example_happy_primes():
    """Happy primes - numbers that are both happy and prime."""
    print("\n" + "=" * 50)
    print("Example 5: Happy Primes")
    print("=" * 50)
    
    print("\nHappy primes are numbers that are both happy AND prime:")
    print("  7: happy + prime ✓")
    print("  13: happy + prime ✓")
    print("  19: happy + prime ✓")
    
    print("\nHappy primes in [1, 200]:")
    happy_primes = happy_primes_in_range(1, 200)
    print(f"  {happy_primes}")
    
    print("\nVerifying happy primes:")
    for n in happy_primes[:5]:
        print(f"  {n}: is_happy={is_happy(n)}, is_prime={is_prime(n)}, is_happy_prime={is_happy_prime(n)}")


def example_range_analysis():
    """Statistical analysis of ranges."""
    print("\n" + "=" * 50)
    print("Example 6: Range Analysis")
    print("=" * 50)
    
    # Analyze 1-100
    analysis = analyze_range(1, 100)
    print(f"\n{analysis.to_summary()}")
    
    # Analyze larger range
    analysis = analyze_range(1, 1000)
    print(f"\nAnalysis of [1, 1000]:")
    print(f"  Happy numbers: {analysis.happy_count} ({analysis.happy_percentage:.2f}%)")
    print(f"  Unhappy numbers: {analysis.unhappy_count}")


def example_properties():
    """Number properties analysis."""
    print("\n" + "=" * 50)
    print("Example 7: Number Properties")
    print("=" * 50)
    
    numbers = [19, 44, 7, 100, 123]
    
    print("\nAnalyzing mathematical properties:")
    for n in numbers:
        props = analyze_properties(n)
        print(f"\n{n}:")
        print(f"  Classification: {props.classification()}")
        print(f"  Digit count: {props.digit_count}")
        print(f"  Digit sum: {props.digit_sum}")
        print(f"  First/Last digit: {props.first_digit}/{props.last_digit}")
        print(f"  Is palindromic: {props.is_palindromic}")
        print(f"  Steps to 1: {props.happy_sequence_length if props.is_happy else 'N/A'}")


def example_special_happy_numbers():
    """Special happy numbers."""
    print("\n" + "=" * 50)
    print("Example 8: Special Happy Numbers")
    print("=" * 50)
    
    # Happy palindromes
    print("\nHappy palindromic numbers (up to 500):")
    palindromes = find_happy_palindromes(500)
    print(f"  {palindromes}")
    
    # Powers of 10 are always happy
    print("\nAll powers of 10 are happy (because 1² + 0² + ... = 1):")
    powers = find_happy_power_of_10(5)
    for p in powers:
        print(f"  {p} → digit_square_sum = {digit_square_sum(p)} = 1")
    
    # Smallest and largest by digit count
    print("\nSmallest and largest happy numbers by digit count:")
    for digits in [1, 2, 3]:
        smallest = find_smallest_happy_with_digits(digits)
        largest = find_largest_happy_with_digits(digits)
        print(f"  {digits} digit(s): smallest={smallest}, largest={largest}")


def example_unhappy_cycle():
    """The unhappy cycle."""
    print("\n" + "=" * 50)
    print("Example 9: The Unhappy Cycle")
    print("=" * 50)
    
    print("\nThe unhappy cycle: numbers that repeat infinitely:")
    cycle_info = analyze_cycle_structure()
    print(f"  Members: {cycle_info['members']}")
    print(f"  Length: {cycle_info['length']}")
    
    print("\nCycle order:")
    print("  4 → 16 → 37 → 58 → 89 → 145 → 42 → 20 → 4 (repeats)")
    
    print("\nDemonstration:")
    n = 4
    print(f"  Starting with {n}:")
    for i in range(10):
        print(f"    Step {i}: {n}")
        n = digit_square_sum(n)
    
    print("\nAll unhappy numbers eventually enter this cycle!")


def example_batch_processing():
    """Batch processing example."""
    print("\n" + "=" * 50)
    print("Example 10: Batch Processing")
    print("=" * 50)
    
    # Batch check many numbers
    numbers = list(range(1, 51))
    
    print("\nChecking happiness for numbers 1-50:")
    results = batch_check_happy(numbers)
    
    happy = [n for n, is_h in results.items() if is_h]
    unhappy = [n for n, is_h in results.items() if not is_h]
    
    print(f"  Happy: {happy}")
    print(f"  Unhappy: {unhappy}")


def example_full_report():
    """Generate full report."""
    print("\n" + "=" * 50)
    print("Example 11: Full Number Report")
    print("=" * 50)
    
    report = happy_number_report(19)
    print(report)


def example_fun_facts():
    """Fun mathematical facts."""
    print("\n" + "=" * 50)
    print("Example 12: Fun Mathematical Facts")
    print("=" * 50)
    
    print("\nInteresting happy number facts:")
    
    # Happy numbers with specific digit sums
    print("\nHappy numbers with digit sum = 10:")
    nums = get_happy_numbers_by_digit_sum(10, 200)
    print(f"  {nums}")
    
    # Density estimate
    print("\nEmpirical happy number density:")
    print(f"  Approximately {happy_density_estimate(1000)}% of numbers are happy")
    
    # Different bases
    print("\nHappiness in different bases:")
    n = 19
    for base in [10, 8, 2]:
        is_happy_in_base = is_happy_base_equivalent(n, base)
        print(f"  {n} in base {base}: {'happy' if is_happy_in_base else 'unhappy'}")


def example_practical_usage():
    """Practical usage examples."""
    print("\n" + "=" * 50)
    print("Example 13: Practical Usage")
    print("=" * 50)
    
    print("\n1. Find all happy numbers in a dataset:")
    dataset = [42, 49, 68, 79, 82, 91, 94, 97, 100, 101, 102]
    happy_in_dataset = [n for n in dataset if is_happy(n)]
    print(f"  Dataset: {dataset}")
    print(f"  Happy numbers: {happy_in_dataset}")
    
    print("\n2. Generate a sequence of happy numbers for lottery/game:")
    happy_nums = list(generate_happy_numbers(10, start=1))
    print(f"  First 10 happy numbers: {happy_nums}")
    
    print("\n3. Check if a specific number has interesting properties:")
    n = 97
    props = analyze_properties(n)
    print(f"  {n}: {props.classification()}")
    if props.is_happy and props.is_prime:
        print(f"    → This is a happy prime! (Steps to 1: {props.happy_sequence_length})")


def main():
    """Run all examples."""
    print("\n" + "=" * 60)
    print("Happy Number Utilities - Usage Examples")
    print("=" * 60)
    
    example_basic_checks()
    example_sequences()
    example_happy_numbers_in_range()
    example_nth_happy_numbers()
    example_happy_primes()
    example_range_analysis()
    example_properties()
    example_special_happy_numbers()
    example_unhappy_cycle()
    example_batch_processing()
    example_full_report()
    example_fun_facts()
    example_practical_usage()
    
    print("\n" + "=" * 60)
    print("Examples completed!")
    print("=" * 60)


if __name__ == '__main__':
    main()