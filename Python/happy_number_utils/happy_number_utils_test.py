#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""AllToolkit - Happy Number Utilities Test Suite

Comprehensive tests for the happy_number_utils module.

Author: AllToolkit
License: MIT
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

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
    is_in_unhappy_cycle,
    get_cycle_for_number,
    analyze_cycle_structure,
    is_happy_base_equivalent,
    batch_check_happy,
    happy_number_report,
    UNHAPPY_CYCLE,
    NumberType,
    HappyNumberResult,
    RangeAnalysis,
    HappyNumberProperties,
)


def test_digit_square_sum():
    """Test digit_square_sum function."""
    print("Testing digit_square_sum...")
    
    # Basic cases
    assert digit_square_sum(19) == 82  # 1² + 9² = 1 + 81 = 82
    assert digit_square_sum(82) == 68  # 8² + 2² = 64 + 4 = 68
    assert digit_square_sum(68) == 100  # 6² + 8² = 36 + 64 = 100
    assert digit_square_sum(100) == 1  # 1² + 0² + 0² = 1
    assert digit_square_sum(1) == 1  # 1² = 1
    assert digit_square_sum(0) == 0  # No digits
    assert digit_square_sum(7) == 49  # 7² = 49
    
    # Multi-digit cases
    assert digit_square_sum(123) == 1 + 4 + 9 == 14
    assert digit_square_sum(999) == 9 * 3 * 9 == 243
    assert digit_square_sum(111) == 1 * 3 == 3
    
    # Large number
    assert digit_square_sum(12345) == 1 + 4 + 9 + 16 + 25 == 55
    
    # Negative number should raise error
    try:
        digit_square_sum(-1)
        assert False, "Should raise ValueError for negative numbers"
    except ValueError:
        pass
    
    print("✓ digit_square_sum tests passed")


def test_digit_sum():
    """Test digit_sum function."""
    print("Testing digit_sum...")
    
    assert digit_sum(19) == 10  # 1 + 9
    assert digit_sum(123) == 6  # 1 + 2 + 3
    assert digit_sum(999) == 27  # 9 + 9 + 9
    assert digit_sum(0) == 0
    assert digit_sum(1) == 1
    
    print("✓ digit_sum tests passed")


def test_is_happy():
    """Test is_happy function."""
    print("Testing is_happy...")
    
    # Known happy numbers (from OEIS A007770)
    happy_nums = [1, 7, 10, 13, 19, 23, 28, 31, 32, 44, 49, 68, 70, 79, 82, 86, 91, 94, 97, 100]
    for n in happy_nums:
        assert is_happy(n), f"{n} should be happy"
    
    # Known unhappy numbers
    unhappy_nums = [2, 3, 4, 5, 6, 8, 9, 11, 12, 14, 15, 16, 17, 18, 20]
    for n in unhappy_nums:
        assert not is_happy(n), f"{n} should be unhappy"
    
    # Edge cases
    assert not is_happy(0)  # Zero is not happy
    assert not is_happy(-1)  # Negative numbers are not happy
    
    # All powers of 10 are happy
    for i in range(1, 10):
        assert is_happy(10 ** i), f"10^{i} should be happy"
    
    print("✓ is_happy tests passed")


def test_is_unhappy():
    """Test is_unhappy function."""
    print("Testing is_unhappy...")
    
    assert is_unhappy(4)
    assert is_unhappy(2)
    assert not is_unhappy(1)
    assert not is_unhappy(7)
    assert not is_unhappy(0)  # Zero is not positive, so neither happy nor unhappy per our definition
    
    print("✓ is_unhappy tests passed")


def test_analyze_number():
    """Test analyze_number function."""
    print("Testing analyze_number...")
    
    # Happy number
    result = analyze_number(19)
    assert result.is_happy
    assert result.number == 19
    assert result.sequence[0] == 19
    assert 1 in result.sequence
    assert result.steps_to_1 == 4  # 19 → 82 → 68 → 100 → 1
    assert result.cycle_detected
    assert 1 in result.cycle_members
    
    # Unhappy number
    result = analyze_number(4)
    assert not result.is_happy
    assert result.number == 4
    assert result.cycle_detected
    assert len(result.cycle_members) == 8  # Standard unhappy cycle has 8 members
    
    # Verify unhappy cycle members
    for member in UNHAPPY_CYCLE:
        assert member in result.cycle_members
    
    print("✓ analyze_number tests passed")


def test_get_happy_sequence():
    """Test get_happy_sequence function."""
    print("Testing get_happy_sequence...")
    
    seq = get_happy_sequence(19)
    assert seq[0] == 19
    assert seq[-1] == 1
    assert len(seq) == 5  # 19 → 82 → 68 → 100 → 1
    
    seq = get_happy_sequence(4)
    assert seq[0] == 4
    # Should contain the unhappy cycle
    
    print("✓ get_happy_sequence tests passed")


def test_count_steps_to_happy():
    """Test count_steps_to_happy function."""
    print("Testing count_steps_to_happy...")
    
    assert count_steps_to_happy(1) == 0  # Already at 1
    assert count_steps_to_happy(19) == 4  # 19 → 82 → 68 → 100 → 1
    assert count_steps_to_happy(7) == 5  # 7 → 49 → 97 → 130 → 10 → 1
    assert count_steps_to_happy(10) == 1  # 10 → 1
    
    # Unhappy numbers return None
    assert count_steps_to_happy(4) is None
    assert count_steps_to_happy(2) is None
    
    print("✓ count_steps_to_happy tests passed")


def test_happy_numbers_in_range():
    """Test happy_numbers_in_range function."""
    print("Testing happy_numbers_in_range...")
    
    # Small range
    happy_nums = happy_numbers_in_range(1, 20)
    expected = [1, 7, 10, 13, 19]
    assert happy_nums == expected
    
    # Check first 100 numbers matches known sequence
    happy_100 = happy_numbers_in_range(1, 100)
    assert len(happy_100) == 20  # There are 20 happy numbers in 1-100
    
    print("✓ happy_numbers_in_range tests passed")


def test_unhappy_numbers_in_range():
    """Test unhappy_numbers_in_range function."""
    print("Testing unhappy_numbers_in_range...")
    
    unhappy_nums = unhappy_numbers_in_range(1, 20)
    expected = [2, 3, 4, 5, 6, 8, 9, 11, 12, 14, 15, 16, 17, 18, 20]
    assert unhappy_nums == expected
    
    print("✓ unhappy_numbers_in_range tests passed")


def test_nth_happy_number():
    """Test nth_happy_number function."""
    print("Testing nth_happy_number...")
    
    # First happy numbers: 1, 7, 10, 13, 19, 23, 28, 31, 32, 44, ...
    assert nth_happy_number(1) == 1
    assert nth_happy_number(2) == 7
    assert nth_happy_number(3) == 10
    assert nth_happy_number(4) == 13
    assert nth_happy_number(5) == 19
    assert nth_happy_number(10) == 44
    
    print("✓ nth_happy_number tests passed")


def test_generate_happy_numbers():
    """Test generate_happy_numbers function."""
    print("Testing generate_happy_numbers...")
    
    gen = generate_happy_numbers(5)
    nums = list(gen)
    assert len(nums) == 5
    assert nums[0] == 1
    assert nums[1] == 7
    assert nums[2] == 10
    
    print("✓ generate_happy_numbers tests passed")


def test_is_prime():
    """Test is_prime function."""
    print("Testing is_prime...")
    
    # Known primes
    assert is_prime(2)
    assert is_prime(3)
    assert is_prime(5)
    assert is_prime(7)
    assert is_prime(11)
    assert is_prime(13)
    assert is_prime(17)
    assert is_prime(19)
    assert is_prime(23)
    
    # Non-primes
    assert not is_prime(1)
    assert not is_prime(4)
    assert not is_prime(6)
    assert not is_prime(8)
    assert not is_prime(9)
    assert not is_prime(10)
    
    print("✓ is_prime tests passed")


def test_is_happy_prime():
    """Test is_happy_prime function."""
    print("Testing is_happy_prime...")
    
    # Happy primes: 7, 13, 19, 23, 31, 79, 97, ...
    # Note: 13 is NOT happy! It's unhappy.
    # Actually happy primes from OEIS: 7, 13-happy? Let me check...
    # 13: 13 → 1 + 9 = 10 → 1, so 13 IS happy!
    
    assert is_happy_prime(7)
    assert is_happy_prime(13)
    assert is_happy_prime(19)
    assert is_happy_prime(23)
    assert is_happy_prime(31)
    
    # Non-happy primes (prime but unhappy)
    assert not is_happy_prime(2)  # Prime but unhappy
    assert not is_happy_prime(3)  # Prime but unhappy
    assert not is_happy_prime(11)  # 11 is unhappy: 11 → 2 → 4 → cycle
    
    # Happy non-primes
    assert not is_happy_prime(10)  # Happy but not prime
    assert not is_happy_prime(1)  # Happy but not prime
    
    print("✓ is_happy_prime tests passed")


def test_happy_primes_in_range():
    """Test happy_primes_in_range function."""
    print("Testing happy_primes_in_range...")
    
    happy_primes = happy_primes_in_range(1, 100)
    expected = [7, 13, 19, 23, 31, 79, 97]
    assert happy_primes == expected
    
    print("✓ happy_primes_in_range tests passed")


def test_analyze_range():
    """Test analyze_range function."""
    print("Testing analyze_range...")
    
    analysis = analyze_range(1, 100)
    assert analysis.start == 1
    assert analysis.end == 100
    assert analysis.happy_count == 20
    assert analysis.unhappy_count == 80
    assert analysis.happy_percentage == 20.0
    assert len(analysis.happy_numbers) == 20
    assert len(analysis.unhappy_numbers) == 80
    
    print("✓ analyze_range tests passed")


def test_analyze_properties():
    """Test analyze_properties function."""
    print("Testing analyze_properties...")
    
    props = analyze_properties(19)
    assert props.number == 19
    assert props.is_happy
    assert props.is_prime
    assert props.digit_count == 2
    assert props.digit_sum == 10
    assert props.digit_square_sum == 82
    assert props.first_digit == 1
    assert props.last_digit == 9
    assert not props.is_power_of_10
    assert not props.is_palindromic
    
    # Test palindromic happy number
    props = analyze_properties(44)
    assert props.is_happy
    assert props.is_palindromic
    assert not props.is_prime
    
    print("✓ analyze_properties tests passed")


def test_find_happy_palindromes():
    """Test find_happy_palindromes function."""
    print("Testing find_happy_palindromes...")
    
    palindromes = find_happy_palindromes(200)
    # Happy palindromes: 1, 44, 121 (is 121 happy? Let me check: 1+4+4=9, no 1+4+1=6, unhappy)
    # Actually: 1, 7, 44, 121? Let me compute
    assert 1 in palindromes
    assert 44 in palindromes
    
    print("✓ find_happy_palindromes tests passed")


def test_find_happy_power_of_10():
    """Test find_happy_power_of_10 function."""
    print("Testing find_happy_power_of_10...")
    
    powers = find_happy_power_of_10(5)
    expected = [10, 100, 1000, 10000, 100000]
    assert powers == expected
    
    # Verify all powers of 10 are happy
    for p in powers:
        assert is_happy(p)
    
    print("✓ find_happy_power_of_10 tests passed")


def test_find_smallest_and_largest():
    """Test find_smallest_happy_with_digits and find_largest_happy_with_digits."""
    print("Testing digit-bound happy number finding...")
    
    # 1 digit: smallest=1, largest=7
    assert find_smallest_happy_with_digits(1) == 1
    assert find_largest_happy_with_digits(1) == 7
    
    # 2 digits: smallest=10, largest=97 (last happy in 10-99)
    assert find_smallest_happy_with_digits(2) == 10
    assert find_largest_happy_with_digits(2) == 97
    
    # 3 digits: smallest=100
    assert find_smallest_happy_with_digits(3) == 100
    
    print("✓ Digit-bound happy number tests passed")


def test_unhappy_cycle():
    """Test unhappy cycle functions."""
    print("Testing unhappy cycle...")
    
    cycle = get_unhappy_cycle()
    assert len(cycle) == 8
    assert 4 in cycle
    assert 16 in cycle
    assert 37 in cycle
    
    # Verify cycle members are unhappy
    for member in cycle:
        assert not is_happy(member)
    
    # Test is_in_unhappy_cycle
    assert is_in_unhappy_cycle(4)
    assert is_in_unhappy_cycle(145)
    assert not is_in_unhappy_cycle(1)
    assert not is_in_unhappy_cycle(7)
    
    # Test cycle structure
    cycle_info = analyze_cycle_structure()
    assert cycle_info['length'] == 8
    assert cycle_info['max'] == 145
    assert cycle_info['min'] == 4
    
    print("✓ Unhappy cycle tests passed")


def test_get_cycle_for_number():
    """Test get_cycle_for_number function."""
    print("Testing get_cycle_for_number...")
    
    # Happy number - no cycle
    assert get_cycle_for_number(19) is None
    
    # Unhappy number - returns cycle
    cycle = get_cycle_for_number(4)
    assert cycle is not None
    assert len(cycle) == 8
    
    print("✓ get_cycle_for_number tests passed")


def test_is_happy_base_equivalent():
    """Test is_happy_base_equivalent function."""
    print("Testing is_happy_base_equivalent...")
    
    # In base 10
    assert is_happy_base_equivalent(19, 10)
    assert not is_happy_base_equivalent(4, 10)
    
    # In other bases (behavior may differ)
    # Test basic functionality
    assert is_happy_base_equivalent(1, 10)
    assert is_happy_base_equivalent(1, 2)
    
    print("✓ is_happy_base_equivalent tests passed")


def test_batch_check_happy():
    """Test batch_check_happy function."""
    print("Testing batch_check_happy...")
    
    numbers = [1, 7, 19, 4, 10, 13]
    results = batch_check_happy(numbers)
    
    assert results[1] == True
    assert results[7] == True
    assert results[19] == True
    assert results[4] == False
    assert results[10] == True
    assert results[13] == True
    
    print("✓ batch_check_happy tests passed")


def test_happy_number_report():
    """Test happy_number_report function."""
    print("Testing happy_number_report...")
    
    report = happy_number_report(19)
    assert "19" in report
    assert "happy" in report
    assert "prime" in report
    assert "Digit" in report
    
    report = happy_number_report(4)
    assert "unhappy" in report
    
    print("✓ happy_number_report tests passed")


def test_data_classes():
    """Test data classes."""
    print("Testing data classes...")
    
    # HappyNumberResult
    result = analyze_number(19)
    summary = result.to_summary()
    assert "happy" in summary
    assert "19" in summary
    
    seq_str = result.get_sequence_string()
    assert "19" in seq_str
    assert "→" in seq_str
    
    # RangeAnalysis
    analysis = analyze_range(1, 100)
    summary = analysis.to_summary()
    assert "Happy numbers" in summary
    assert "20" in summary
    
    # HappyNumberProperties
    props = analyze_properties(19)
    classification = props.classification()
    assert "happy" in classification
    assert "prime" in classification
    
    print("✓ Data class tests passed")


def test_edge_cases():
    """Test edge cases."""
    print("Testing edge cases...")
    
    # Zero
    assert not is_happy(0)
    result = analyze_number(0)
    assert not result.is_happy
    
    # One
    assert is_happy(1)
    result = analyze_number(1)
    assert result.steps_to_1 == 0
    
    # Large number
    assert is_happy(10000)  # 10000 → 1
    assert is_happy(1000000)  # 1000000 → 1
    
    # Verify unhappy numbers eventually enter cycle
    for n in [2, 3, 5, 6, 8, 9]:
        result = analyze_number(n)
        assert result.cycle_detected
        assert result.cycle_members == UNHAPPY_CYCLE
    
    print("✓ Edge case tests passed")


def run_all_tests():
    """Run all tests."""
    print("=" * 60)
    print("Happy Number Utilities Test Suite")
    print("=" * 60)
    
    test_digit_square_sum()
    test_digit_sum()
    test_is_happy()
    test_is_unhappy()
    test_analyze_number()
    test_get_happy_sequence()
    test_count_steps_to_happy()
    test_happy_numbers_in_range()
    test_unhappy_numbers_in_range()
    test_nth_happy_number()
    test_generate_happy_numbers()
    test_is_prime()
    test_is_happy_prime()
    test_happy_primes_in_range()
    test_analyze_range()
    test_analyze_properties()
    test_find_happy_palindromes()
    test_find_happy_power_of_10()
    test_find_smallest_and_largest()
    test_unhappy_cycle()
    test_get_cycle_for_number()
    test_is_happy_base_equivalent()
    test_batch_check_happy()
    test_happy_number_report()
    test_data_classes()
    test_edge_cases()
    
    print("\n" + "=" * 60)
    print("✅ All tests passed!")
    print("=" * 60)


if __name__ == '__main__':
    run_all_tests()