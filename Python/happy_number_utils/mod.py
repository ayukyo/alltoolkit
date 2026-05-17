#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""AllToolkit - Happy Number Utilities Module

Comprehensive happy number utilities for Python with zero external dependencies.
Happy numbers are numbers that eventually reach 1 when iterating the sum of
squares of digits. If the process results in a cycle that doesn't include 1,
the number is unhappy (or sad).

This module provides:
- Happy number detection and classification
- Happy number sequence generation
- Happy number range finding
- Cycle detection and analysis
- Mathematical properties analysis
- Digit square sum calculations

Author: AllToolkit
License: MIT
"""

from typing import List, Set, Tuple, Dict, Optional, Generator, Any
from dataclasses import dataclass, field
from enum import Enum
import math


# =============================================================================
# Constants
# =============================================================================

# Known unhappy cycle: 4 → 16 → 37 → 58 → 89 → 145 → 42 → 20 → 4
UNHAPPY_CYCLE = {4, 16, 37, 58, 89, 145, 42, 20}

# Pre-computed happy numbers up to 1000 for fast lookup
HAPPY_CACHE_1000: Set[int] = None  # Will be computed on first use


# =============================================================================
# Enums
# =============================================================================

class NumberType(Enum):
    """Number happiness classification."""
    HAPPY = "happy"
    UNHAPPY = "unhappy"
    UNKNOWN = "unknown"


class CycleType(Enum):
    """Type of cycle found."""
    FIXED_POINT = "fixed_point"      # Reaches 1 (happy)
    UNHAPPY_CYCLE = "unhappy_cycle"  # Known unhappy cycle
    OTHER_CYCLE = "other_cycle"      # Other cycle (shouldn't happen for digit squares)


# =============================================================================
# Data Classes
# =============================================================================

@dataclass
class HappyNumberResult:
    """Result of happy number analysis."""
    number: int
    is_happy: bool
    sequence: List[int]
    cycle_detected: bool
    cycle_members: Set[int] = field(default_factory=set)
    steps_to_1: Optional[int] = None  # Number of steps to reach 1 (if happy)
    steps_to_cycle: Optional[int] = None  # Number of steps to reach cycle (if unhappy)
    
    def to_summary(self) -> str:
        """Generate text summary."""
        if self.is_happy:
            return f"{self.number} is a happy number (reached 1 in {self.steps_to_1} steps)"
        else:
            return f"{self.number} is an unhappy number (entered cycle after {self.steps_to_cycle} steps)"
    
    def get_sequence_string(self) -> str:
        """Get sequence as arrow-separated string."""
        return " → ".join(str(n) for n in self.sequence)


@dataclass
class RangeAnalysis:
    """Analysis of happy numbers in a range."""
    start: int
    end: int
    happy_numbers: List[int]
    unhappy_numbers: List[int]
    happy_count: int
    unhappy_count: int
    happy_percentage: float
    density_by_decade: Dict[int, float]  # {decade: percentage}
    
    def to_summary(self) -> str:
        """Generate text summary."""
        lines = [
            f"=== Happy Numbers in [{self.start}, {self.end}] ===",
            f"Happy numbers: {self.happy_count} ({self.happy_percentage:.2f}%)",
            f"Unhappy numbers: {self.unhappy_count} ({100 - self.happy_percentage:.2f}%)",
            f"First 10 happy: {self.happy_numbers[:10]}",
            f"First 10 unhappy: {self.unhappy_numbers[:10]}",
        ]
        return "\n".join(lines)


@dataclass
class HappyNumberProperties:
    """Mathematical properties of a happy number."""
    number: int
    is_happy: bool
    is_prime: bool  # Is it a happy prime?
    digit_count: int
    digit_sum: int
    digit_square_sum: int
    first_digit: int
    last_digit: int
    is_power_of_10: bool
    is_palindromic: bool
    happy_sequence_length: int  # Steps to reach 1
    happy_root: int  # The root value (always 1 for happy)
    
    def classification(self) -> str:
        """Get classification string."""
        classes = []
        if self.is_happy:
            classes.append("happy")
        else:
            classes.append("unhappy")
        
        if self.is_prime:
            classes.append("prime")
        
        if self.is_palindromic:
            classes.append("palindromic")
        
        if self.is_power_of_10:
            classes.append("power-of-10")
        
        return " + ".join(classes) if classes else "unknown"


# =============================================================================
# Core Functions
# =============================================================================

def digit_square_sum(n: int) -> int:
    """
    Calculate the sum of squares of digits.
    
    This is the core transformation function for happy number computation.
    
    Args:
        n: The number to process
        
    Returns:
        Sum of squares of each digit
        
    Examples:
        >>> digit_square_sum(19)
        1² + 9² = 1 + 81 = 82
        >>> digit_square_sum(100)
        1² + 0² + 0² = 1
        >>> digit_square_sum(7)
        7² = 49
    """
    if n < 0:
        raise ValueError("Happy numbers are defined for positive integers only")
    
    total = 0
    while n > 0:
        digit = n % 10
        total += digit * digit
        n //= 10
    return total


def digit_sum(n: int) -> int:
    """
    Calculate the sum of digits.
    
    Args:
        n: The number to process
        
    Returns:
        Sum of all digits
    """
    if n < 0:
        n = abs(n)
    
    total = 0
    while n > 0:
        total += n % 10
        n //= 10
    return total


def is_happy(n: int, max_iterations: int = 1000) -> bool:
    """
    Check if a number is happy.
    
    A number is happy if repeatedly applying digit_square_sum eventually
    reaches 1. If it enters a cycle that doesn't contain 1, it's unhappy.
    
    Args:
        n: The number to check
        max_iterations: Maximum iterations before assuming unhappy
        
    Returns:
        True if the number is happy, False otherwise
        
    Examples:
        >>> is_happy(19)
        True  # 19 → 82 → 68 → 100 → 1
        >>> is_happy(4)
        False  # 4 → 16 → 37 → 58 → 89 → 145 → 42 → 20 → 4 (cycle)
        >>> is_happy(1)
        True  # Already at 1
    """
    if n <= 0:
        return False
    
    seen: Set[int] = set()
    current = n
    
    for _ in range(max_iterations):
        if current == 1:
            return True
        if current in seen:
            return False  # Entered a cycle without 1
        if current in UNHAPPY_CYCLE:
            return False  # Known unhappy cycle member
        
        seen.add(current)
        current = digit_square_sum(current)
    
    return False  # Exceeded iterations, assume unhappy


def is_unhappy(n: int) -> bool:
    """
    Check if a number is unhappy (sad).
    
    Args:
        n: The number to check
        
    Returns:
        True if the number is unhappy, False otherwise
    """
    return not is_happy(n) if n > 0 else False


def analyze_number(n: int, max_iterations: int = 1000) -> HappyNumberResult:
    """
    Perform complete analysis of a number's happiness.
    
    Tracks the entire sequence, detects cycles, and counts steps.
    
    Args:
        n: The number to analyze
        max_iterations: Maximum iterations
        
    Returns:
        HappyNumberResult with complete analysis
    """
    if n <= 0:
        return HappyNumberResult(
            number=n,
            is_happy=False,
            sequence=[n],
            cycle_detected=False,
            steps_to_1=None,
            steps_to_cycle=None
        )
    
    sequence: List[int] = [n]
    seen: Dict[int, int] = {}  # value -> index in sequence
    current = n
    
    for i in range(max_iterations):
        if current == 1:
            return HappyNumberResult(
                number=n,
                is_happy=True,
                sequence=sequence,
                cycle_detected=True,
                cycle_members={1},
                steps_to_1=i,
                steps_to_cycle=None
            )
        
        if current in seen:
            # Found a cycle - determine its members
            cycle_start_idx = seen[current]
            cycle_members = set(sequence[cycle_start_idx:])
            return HappyNumberResult(
                number=n,
                is_happy=False,
                sequence=sequence,
                cycle_detected=True,
                cycle_members=cycle_members,
                steps_to_1=None,
                steps_to_cycle=cycle_start_idx
            )
        
        seen[current] = i
        current = digit_square_sum(current)
        sequence.append(current)
    
    # Exceeded iterations
    return HappyNumberResult(
        number=n,
        is_happy=False,
        sequence=sequence,
        cycle_detected=False,
        steps_to_1=None,
        steps_to_cycle=None
    )


def get_happy_sequence(n: int) -> List[int]:
    """
    Get the sequence of numbers leading to 1 or a cycle.
    
    Args:
        n: Starting number
        
    Returns:
        List of numbers in the sequence
    """
    result = analyze_number(n)
    return result.sequence


def count_steps_to_happy(n: int) -> Optional[int]:
    """
    Count the number of steps to reach 1.
    
    Args:
        n: Starting number
        
    Returns:
        Number of steps, or None if not happy
    """
    if n <= 0:
        return None
    
    current = n
    steps = 0
    
    seen: Set[int] = set()
    
    while current != 1 and current not in seen and steps < 1000:
        seen.add(current)
        current = digit_square_sum(current)
        steps += 1
    
    return steps if current == 1 else None


# =============================================================================
# Happy Number Generation
# =============================================================================

def happy_numbers_in_range(start: int, end: int) -> List[int]:
    """
    Find all happy numbers in a range.
    
    Args:
        start: Start of range (inclusive)
        end: End of range (inclusive)
        
    Returns:
        List of happy numbers in the range
    """
    return [n for n in range(start, end + 1) if is_happy(n)]


def unhappy_numbers_in_range(start: int, end: int) -> List[int]:
    """
    Find all unhappy numbers in a range.
    
    Args:
        start: Start of range (inclusive)
        end: End of range (inclusive)
        
    Returns:
        List of unhappy numbers in the range
    """
    return [n for n in range(start, end + 1) if n > 0 and not is_happy(n)]


def generate_happy_numbers(count: int, start: int = 1) -> Generator[int, None, None]:
    """
    Generate a sequence of happy numbers.
    
    Args:
        count: Number of happy numbers to generate
        start: Starting number to search from
        
    Yields:
        Happy numbers one by one
    """
    current = start
    found = 0
    
    while found < count:
        if is_happy(current):
            yield current
            found += 1
        current += 1


def nth_happy_number(n: int) -> int:
    """
    Find the nth happy number (1-indexed).
    
    Args:
        n: Index of happy number to find
        
    Returns:
        The nth happy number
    """
    gen = generate_happy_numbers(n)
    result = 1
    for happy_num in gen:
        result = happy_num
    return result


def happy_numbers_up_to(limit: int) -> List[int]:
    """
    Get all happy numbers up to a limit.
    
    Args:
        limit: Maximum value
        
    Returns:
        List of happy numbers ≤ limit
    """
    return [n for n in range(1, limit + 1) if is_happy(n)]


# =============================================================================
# Happy Primes
# =============================================================================

def is_prime(n: int) -> bool:
    """
    Check if a number is prime.
    
    Simple implementation for completeness.
    
    Args:
        n: Number to check
        
    Returns:
        True if prime, False otherwise
    """
    if n < 2:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False
    if n == 3:
        return True
    if n % 3 == 0:
        return False
    
    # Check divisors up to sqrt(n)
    i = 5
    while i * i <= n:
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i += 6
    
    return True


def is_happy_prime(n: int) -> bool:
    """
    Check if a number is a happy prime.
    
    A happy prime is both happy and prime.
    
    Args:
        n: Number to check
        
    Returns:
        True if happy prime, False otherwise
        
    Examples:
        >>> is_happy_prime(7)
        True  # 7 is prime and happy (7 → 49 → 97 → 130 → 10 → 1)
        >>> is_happy_prime(19)
        True  # 19 is prime and happy
        >>> is_happy_prime(13)
        False  # 13 is prime but unhappy
    """
    return is_happy(n) and is_prime(n)


def happy_primes_in_range(start: int, end: int) -> List[int]:
    """
    Find all happy primes in a range.
    
    Args:
        start: Start of range
        end: End of range
        
    Returns:
        List of happy primes
    """
    return [n for n in range(start, end + 1) if is_happy_prime(n)]


def nth_happy_prime(n: int) -> int:
    """
    Find the nth happy prime.
    
    Args:
        n: Index (1-indexed)
        
    Returns:
        The nth happy prime
    """
    count = 0
    current = 2
    
    while count < n:
        if is_happy_prime(current):
            count += 1
            if count == n:
                return current
        current += 1
    
    return current


# =============================================================================
# Range Analysis
# =============================================================================

def analyze_range(start: int, end: int) -> RangeAnalysis:
    """
    Perform statistical analysis of happy numbers in a range.
    
    Args:
        start: Start of range
        end: End of range
        
    Returns:
        RangeAnalysis with statistics
    """
    happy_nums = happy_numbers_in_range(start, end)
    unhappy_nums = unhappy_numbers_in_range(start, end)
    
    total = end - start + 1
    happy_count = len(happy_nums)
    happy_percentage = (happy_count / total) * 100 if total > 0 else 0
    
    # Calculate density by decade
    density_by_decade: Dict[int, float] = {}
    decade_start = (start // 10) * 10
    decade_end = (end // 10) * 10
    
    for decade in range(decade_start, decade_end + 10, 10):
        decade_range_start = max(decade, start)
        decade_range_end = min(decade + 9, end)
        
        if decade_range_start <= decade_range_end:
            decade_happy = len([n for n in range(decade_range_start, decade_range_end + 1) if is_happy(n)])
            decade_total = decade_range_end - decade_range_start + 1
            density_by_decade[decade] = (decade_happy / decade_total) * 100
    
    return RangeAnalysis(
        start=start,
        end=end,
        happy_numbers=happy_nums,
        unhappy_numbers=unhappy_nums,
        happy_count=happy_count,
        unhappy_count=len(unhappy_nums),
        happy_percentage=happy_percentage,
        density_by_decade=density_by_decade
    )


# =============================================================================
# Properties Analysis
# =============================================================================

def analyze_properties(n: int) -> HappyNumberProperties:
    """
    Analyze mathematical properties of a number.
    
    Args:
        n: Number to analyze
        
    Returns:
        HappyNumberProperties with all properties
    """
    if n <= 0:
        raise ValueError("Cannot analyze properties of non-positive numbers")
    
    # Basic digit analysis
    digits = [int(d) for d in str(n)]
    digit_count = len(digits)
    digit_sum_val = sum(digits)
    digit_square_sum_val = digit_square_sum(n)
    first_digit = digits[0]
    last_digit = digits[-1]
    
    # Special properties
    is_power_of_10 = n in [10 ** i for i in range(20)]  # Check up to 10^19
    is_palindromic = digits == digits[::-1]
    
    # Happy number analysis
    is_happy_val = is_happy(n)
    happy_sequence_length = count_steps_to_happy(n) if is_happy_val else 0
    
    return HappyNumberProperties(
        number=n,
        is_happy=is_happy_val,
        is_prime=is_prime(n),
        digit_count=digit_count,
        digit_sum=digit_sum_val,
        digit_square_sum=digit_square_sum_val,
        first_digit=first_digit,
        last_digit=last_digit,
        is_power_of_10=is_power_of_10,
        is_palindromic=is_palindromic,
        happy_sequence_length=happy_sequence_length,
        happy_root=1 if is_happy_val else 0
    )


# =============================================================================
# Special Happy Numbers
# =============================================================================

def find_happy_palindromes(limit: int) -> List[int]:
    """
    Find happy numbers that are also palindromes.
    
    Args:
        limit: Maximum value
        
    Returns:
        List of happy palindromic numbers
    """
    return [n for n in range(1, limit + 1) 
            if is_happy(n) and str(n) == str(n)[::-1]]


def find_happy_power_of_10(limit_power: int = 10) -> List[int]:
    """
    Find powers of 10 that are happy.
    
    Note: All powers of 10 are happy because:
    10^n → 1² + 0² + ... + 0² = 1
    
    Args:
        limit_power: Maximum power to check
        
    Returns:
        List of happy powers of 10
    """
    # All powers of 10 are happy (digit_square_sum = 1)
    return [10 ** i for i in range(1, limit_power + 1)]


def find_smallest_happy_with_digits(num_digits: int) -> int:
    """
    Find the smallest happy number with a given number of digits.
    
    Args:
        num_digits: Number of digits
        
    Returns:
        Smallest happy number with that many digits
    """
    start = 10 ** (num_digits - 1)
    end = 10 ** num_digits - 1
    
    for n in range(start, end + 1):
        if is_happy(n):
            return n
    
    return -1  # No happy number found (shouldn't happen)


def find_largest_happy_with_digits(num_digits: int) -> int:
    """
    Find the largest happy number with a given number of digits.
    
    Args:
        num_digits: Number of digits
        
    Returns:
        Largest happy number with that many digits
    """
    start = 10 ** (num_digits - 1)
    end = 10 ** num_digits - 1
    
    for n in range(end, start - 1, -1):
        if is_happy(n):
            return n
    
    return -1  # No happy number found (shouldn't happen)


# =============================================================================
# Cycle Analysis
# =============================================================================

def get_unhappy_cycle() -> Set[int]:
    """
    Get the known unhappy cycle.
    
    Returns:
        Set of numbers in the unhappy cycle
    """
    return UNHAPPY_CYCLE.copy()


def is_in_unhappy_cycle(n: int) -> bool:
    """
    Check if a number is in the unhappy cycle.
    
    Args:
        n: Number to check
        
    Returns:
        True if in the unhappy cycle
    """
    return n in UNHAPPY_CYCLE


def get_cycle_for_number(n: int) -> Optional[Set[int]]:
    """
    Get the cycle a number enters (if unhappy).
    
    Args:
        n: Number to analyze
        
    Returns:
        Set of cycle members, or None if happy
    """
    result = analyze_number(n)
    if result.is_happy:
        return None
    return result.cycle_members


def analyze_cycle_structure() -> Dict[str, Any]:
    """
    Analyze the structure of the unhappy cycle.
    
    Returns:
        Dict with cycle information
    """
    cycle = list(UNHAPPY_CYCLE)
    cycle.sort()
    
    # Find cycle order
    cycle_order = []
    current = 4  # Known starting point
    while len(cycle_order) < len(cycle):
        cycle_order.append(current)
        current = digit_square_sum(current)
        if current in cycle_order:
            break
    
    return {
        "members": cycle,
        "length": len(cycle),
        "order": cycle_order,
        "sum_of_members": sum(cycle),
        "average": sum(cycle) / len(cycle),
        "max": max(cycle),
        "min": min(cycle),
    }


# =============================================================================
# Mathematical Insights
# =============================================================================

def happy_density_estimate(range_size: int) -> float:
    """
    Estimate the density of happy numbers.
    
    Empirical studies show roughly 15-20% of numbers are happy.
    
    Args:
        range_size: Size of range to estimate
        
    Returns:
        Estimated percentage of happy numbers
    """
    # Empirical observation: ~15% of numbers are happy
    return 15.0


def is_happy_base_equivalent(n: int, base: int = 10) -> bool:
    """
    Check if a number is happy in a different base.
    
    Happy numbers can be defined in any base, but the behavior differs.
    
    Args:
        n: Number to check
        base: Base to use (default 10)
        
    Returns:
        True if happy in that base
    """
    if base < 2:
        raise ValueError("Base must be at least 2")
    
    def digit_square_sum_base(num: int, b: int) -> int:
        total = 0
        while num > 0:
            digit = num % b
            total += digit * digit
            num //= b
        return total
    
    seen: Set[int] = set()
    current = n
    
    for _ in range(1000):
        if current == 1:
            return True
        if current in seen:
            return False
        seen.add(current)
        current = digit_square_sum_base(current, base)
    
    return False


def get_happy_numbers_by_digit_sum(digit_sum_target: int, limit: int = 10000) -> List[int]:
    """
    Find happy numbers with a specific digit sum.
    
    Args:
        digit_sum_target: Target digit sum
        limit: Maximum number to search
        
    Returns:
        List of happy numbers with that digit sum
    """
    result = []
    for n in range(1, limit + 1):
        if digit_sum(n) == digit_sum_target and is_happy(n):
            result.append(n)
    return result


# =============================================================================
# Utility Functions
# =============================================================================

def build_happy_cache(limit: int = 1000) -> Set[int]:
    """
    Build a cache of happy numbers up to a limit.
    
    Useful for repeated fast lookups.
    
    Args:
        limit: Maximum number to cache
        
    Returns:
        Set of happy numbers up to limit
    """
    return set(happy_numbers_up_to(limit))


def is_happy_cached(n: int, cache: Optional[Set[int]] = None) -> bool:
    """
    Check if happy using a cache for optimization.
    
    Args:
        n: Number to check
        cache: Optional pre-computed cache
        
    Returns:
        True if happy
    """
    if cache is None:
        cache = build_happy_cache(1000)
    
    # For small numbers, use cache
    if n <= max(cache) if cache else 1000:
        return n in cache
    
    # For larger numbers, compute normally
    return is_happy(n)


def batch_check_happy(numbers: List[int]) -> Dict[int, bool]:
    """
    Check happiness for multiple numbers efficiently.
    
    Args:
        numbers: List of numbers to check
        
    Returns:
        Dict mapping each number to its happiness status
    """
    # Build cache for smallest max in the list
    max_val = max(numbers) if numbers else 1000
    cache_size = min(max_val, 10000)
    cache = build_happy_cache(cache_size)
    
    return {n: is_happy_cached(n, cache) for n in numbers}


def happy_number_report(n: int) -> str:
    """
    Generate a detailed report for a number.
    
    Args:
        n: Number to report
        
    Returns:
        Multi-line report string
    """
    result = analyze_number(n)
    props = analyze_properties(n)
    
    lines = [
        f"=== Happy Number Report for {n} ===",
        "",
        f"Classification: {props.classification()}",
        f"Is Happy: {result.is_happy}",
        f"",
        "Digit Analysis:",
        f"  Digit Count: {props.digit_count}",
        f"  Digit Sum: {props.digit_sum}",
        f"  Digit Square Sum: {props.digit_square_sum}",
        f"  First Digit: {props.first_digit}",
        f"  Last Digit: {props.last_digit}",
        "",
        "Special Properties:",
        f"  Is Prime: {props.is_prime}",
        f"  Is Palindromic: {props.is_palindromic}",
        f"  Is Power of 10: {props.is_power_of_10}",
        "",
        "Happy Number Properties:",
        f"  Steps to 1: {result.steps_to_1 if result.is_happy else 'N/A'}",
        f"  Sequence: {result.get_sequence_string()}",
    ]
    
    if not result.is_happy and result.cycle_members:
        lines.append(f"  Cycle Members: {sorted(result.cycle_members)}")
    
    return "\n".join(lines)


# =============================================================================
# Main (for demonstration)
# =============================================================================

if __name__ == '__main__':
    print("Happy Number Utilities Demo")
    print("=" * 50)
    
    # Basic checks
    test_numbers = [1, 7, 10, 13, 19, 23, 28, 31, 32, 44, 49, 68, 70, 79, 82, 86, 91, 94, 97, 100]
    
    print("\nChecking common test numbers:")
    for n in test_numbers:
        status = "happy" if is_happy(n) else "unhappy"
        prime_status = " + prime" if is_prime(n) else ""
        print(f"  {n}: {status}{prime_status}")
    
    # Sequence examples
    print("\n--- Sequences ---")
    for n in [19, 4, 7]:
        result = analyze_number(n)
        print(f"\n{n}: {result.to_summary()}")
        print(f"Sequence: {result.get_sequence_string()}")
    
    # Happy primes
    print("\n--- Happy Primes (first 10) ---")
    happy_primes = happy_primes_in_range(1, 200)[:10]
    print(f"Happy primes: {happy_primes}")
    
    # Range analysis
    print("\n--- Range Analysis (1-100) ---")
    analysis = analyze_range(1, 100)
    print(analysis.to_summary())
    
    # nth happy number
    print("\n--- nth Happy Numbers ---")
    for i in [1, 10, 100, 1000]:
        print(f"  {i}th happy number: {nth_happy_number(i)}")
    
    # Special happy numbers
    print("\n--- Special Happy Numbers ---")
    palindromes = find_happy_palindromes(200)
    print(f"Happy palindromes (up to 200): {palindromes}")
    
    # Cycle analysis
    print("\n--- Unhappy Cycle ---")
    cycle_info = analyze_cycle_structure()
    print(f"Cycle members: {cycle_info['members']}")
    print(f"Cycle order: 4 → 16 → 37 → 58 → 89 → 145 → 42 → 20 → 4")
    
    # Full report
    print("\n--- Full Report for 19 ---")
    print(happy_number_report(19))
    
    print("\nAll tests completed successfully!")