#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""AllToolkit - Verhoeff Algorithm Utilities Module

Comprehensive Verhoeff check digit algorithm implementation with zero external dependencies.
The Verhoeff algorithm is a checksum formula that detects all single-digit errors
and all transposition errors (adjacent digit swaps) in numeric identifiers.

Algorithm Background:
- Developed by Dutch mathematician Jacobus Verhoeff in 1969
- Uses dihedral group D5 (symmetry group of a regular pentagon)
- More powerful than Luhn algorithm:
  * Catches all single-digit substitution errors (Luhn misses 10%)
  * Catches all adjacent digit transposition errors (Luhn misses some)
  * Catches about 95% of twin errors (aa → bb)
  * Catches about 94% of jump transpositions (abc → cba)

Use Cases:
- Numeric identifiers (IDs, account numbers)
- Enhanced error detection over Luhn
- Systems requiring strong validation
- Educational purposes (group theory applications)

Author: AllToolkit
License: MIT
"""

from typing import Tuple, Optional, List


# =============================================================================
# Dihedral Group D5 Multiplication Table
# =============================================================================

# D5 multiplication table: d[j][k] = j * k in D5
# This represents the symmetries of a regular pentagon
D5_MULTIPLICATION = (
    (0, 1, 2, 3, 4, 5, 6, 7, 8, 9),
    (1, 2, 3, 4, 0, 6, 7, 8, 9, 5),
    (2, 3, 4, 0, 1, 7, 8, 9, 5, 6),
    (3, 4, 0, 1, 2, 8, 9, 5, 6, 7),
    (4, 0, 1, 2, 3, 9, 5, 6, 7, 8),
    (5, 9, 8, 7, 6, 0, 4, 3, 2, 1),
    (6, 5, 9, 8, 7, 1, 0, 4, 3, 2),
    (7, 6, 5, 9, 8, 2, 1, 0, 4, 3),
    (8, 7, 6, 5, 9, 3, 2, 1, 0, 4),
    (9, 8, 7, 6, 5, 4, 3, 2, 1, 0),
)

# Permutation table: P[position mod 8]
# Based on the permutation σ = (1 5 8 9 4 2 7)(0)(3)(6)
# Each position uses σ^position
PERMUTATION = (
    (0, 1, 2, 3, 4, 5, 6, 7, 8, 9),
    (1, 5, 7, 6, 2, 8, 3, 0, 9, 4),
    (5, 8, 0, 3, 7, 9, 6, 1, 4, 2),
    (8, 9, 1, 6, 0, 4, 3, 5, 2, 7),
    (9, 4, 5, 3, 1, 2, 6, 8, 7, 0),
    (4, 2, 8, 6, 5, 7, 3, 9, 0, 1),
    (2, 7, 9, 3, 8, 0, 6, 4, 1, 5),
    (7, 0, 4, 6, 9, 1, 3, 2, 5, 8),
)

# Inverse table: INV[j] = inverse of j in D5
# INV[j] * j = 0 (the identity element)
INVERSE = (0, 4, 3, 2, 1, 5, 6, 7, 8, 9)


# =============================================================================
# Core Functions
# =============================================================================

def compute_check_digit(number: str) -> int:
    """
    Compute the Verhoeff check digit for a numeric string.
    
    The check digit is computed such that when appended to the number,
    the combined string will pass validation.
    
    Args:
        number: A string of digits (0-9). Can be any length.
        
    Returns:
        int: The check digit (0-9).
        
    Raises:
        ValueError: If the input contains non-digit characters.
        
    Examples:
        >>> compute_check_digit("12345")
        1
        >>> compute_check_digit("142857")
        3
        >>> compute_check_digit("0")
        0
        >>> compute_check_digit("")
        0
    """
    if not number:
        return 0
    
    if not number.isdigit():
        raise ValueError("Input must contain only digits (0-9)")
    
    # Compute check digit
    check = 0
    for i, digit_char in enumerate(reversed(number)):
        digit = int(digit_char)
        # Position from right: i+1 because check digit will be at position 0
        perm_index = (i + 1) % 8
        permuted = PERMUTATION[perm_index][digit]
        check = D5_MULTIPLICATION[check][permuted]
    
    # Find the digit that makes the total sum = 0
    # We need to find x such that D5[check][P[0][x]] = 0
    for x in range(10):
        if D5_MULTIPLICATION[check][PERMUTATION[0][x]] == 0:
            return x
    return 0  # Should never reach here


def compute_check_digit_int(number: int) -> int:
    """
    Compute the Verhoeff check digit for an integer.
    
    Args:
        number: A non-negative integer.
        
    Returns:
        int: The check digit (0-9).
        
    Raises:
        ValueError: If the input is negative.
        
    Examples:
        >>> compute_check_digit_int(12345)
        1
        >>> compute_check_digit_int(0)
        0
    """
    if number < 0:
        raise ValueError("Input must be a non-negative integer")
    return compute_check_digit(str(number))


def validate(number: str) -> bool:
    """
    Validate a numeric string with Verhoeff check digit.
    
    The input should be the original number with its check digit appended.
    
    Args:
        number: A string of digits including the check digit as the last digit.
        
    Returns:
        bool: True if valid, False otherwise.
        
    Examples:
        >>> validate("123451")  # 12345 with check digit 1
        True
        >>> validate("123450")  # Wrong check digit
        False
        >>> validate("123452")  # Wrong check digit
        False
        >>> validate("0")  # Single zero is valid (check digit for empty)
        True
        >>> validate("1")  # Invalid
        False
    """
    if not number:
        return False
    
    if not number.isdigit():
        return False
    
    # Verify the checksum
    check = 0
    for i, digit_char in enumerate(reversed(number)):
        digit = int(digit_char)
        perm_index = i % 8
        permuted = PERMUTATION[perm_index][digit]
        check = D5_MULTIPLICATION[check][permuted]
    
    # Valid if the final check is 0
    return check == 0


def validate_int(number: int) -> bool:
    """
    Validate an integer with Verhoeff check digit.
    
    The last digit of the integer is treated as the check digit.
    
    Args:
        number: A non-negative integer with check digit as the last digit.
        
    Returns:
        bool: True if valid, False otherwise.
        
    Examples:
        >>> validate_int(123451)
        True
        >>> validate_int(123450)
        False
    """
    if number < 0:
        return False
    return validate(str(number))


def append_check_digit(number: str) -> str:
    """
    Append the Verhoeff check digit to a numeric string.
    
    Args:
        number: A string of digits (0-9).
        
    Returns:
        str: The original string with check digit appended.
        
    Raises:
        ValueError: If the input contains non-digit characters.
        
    Examples:
        >>> append_check_digit("12345")
        '123451'
        >>> append_check_digit("142857")
        '1428573'
        >>> append_check_digit("")
        '0'
    """
    check_digit = compute_check_digit(number)
    return number + str(check_digit)


def append_check_digit_int(number: int) -> int:
    """
    Append the Verhoeff check digit to an integer.
    
    Args:
        number: A non-negative integer.
        
    Returns:
        int: The original integer with check digit appended.
        
    Raises:
        ValueError: If the input is negative.
        
    Examples:
        >>> append_check_digit_int(12345)
        123451
        >>> append_check_digit_int(0)
        0
    """
    if number < 0:
        raise ValueError("Input must be a non-negative integer")
    check_digit = compute_check_digit_int(number)
    return number * 10 + check_digit


def get_check_digit_position(number: str) -> int:
    """
    Get the position where the check digit should be (for reference).
    
    Args:
        number: A numeric string.
        
    Returns:
        int: The position (index) of the check digit (last position).
        
    Examples:
        >>> get_check_digit_position("123451")
        5
    """
    return len(number) - 1 if number else 0


def extract_data_digits(number: str) -> str:
    """
    Extract the data digits (without check digit) from a validated number.
    
    Args:
        number: A validated numeric string with check digit.
        
    Returns:
        str: The data digits without the check digit.
        
    Examples:
        >>> extract_data_digits("123451")
        '12345'
        >>> extract_data_digits("0")
        ''
    """
    return number[:-1] if number else ""


def extract_data_digits_int(number: int) -> int:
    """
    Extract the data digits (without check digit) from a validated integer.
    
    Args:
        number: A validated integer with check digit.
        
    Returns:
        int: The data digits without the check digit.
        
    Examples:
        >>> extract_data_digits_int(123451)
        12345
        >>> extract_data_digits_int(0)
        0
    """
    return number // 10


# =============================================================================
# Error Detection Analysis Functions
# =============================================================================

def detect_single_error(original: str, modified: str) -> Optional[Tuple[int, int, int]]:
    """
    Detect if there's a single digit substitution error.
    
    Args:
        original: The original validated number.
        modified: The potentially modified number.
        
    Returns:
        Optional[Tuple[int, int, int]]: (position, original_digit, modified_digit) if single error detected, None otherwise.
        
    Examples:
        >>> detect_single_error("123451", "123351")
        (3, 4, 3)
        >>> detect_single_error("123451", "123451")
        None
        >>> detect_single_error("123451", "123352")
        None  # Multiple differences
    """
    if len(original) != len(modified):
        return None
    
    differences = []
    for i, (o, m) in enumerate(zip(original, modified)):
        if o != m:
            differences.append((i, int(o), int(m)))
            if len(differences) > 1:
                return None
    
    return differences[0] if differences else None


def detect_transposition_error(original: str, modified: str) -> Optional[Tuple[int, int]]:
    """
    Detect if there's an adjacent digit transposition error.
    
    Args:
        original: The original validated number.
        modified: The potentially modified number.
        
    Returns:
        Optional[Tuple[int, int]]: (position1, position2) of transposed digits if detected, None otherwise.
        
    Examples:
        >>> detect_transposition_error("123451", "124351")
        (2, 3)
        >>> detect_transposition_error("123451", "123451")
        None
    """
    if len(original) != len(modified):
        return None
    
    differences = []
    for i, (o, m) in enumerate(zip(original, modified)):
        if o != m:
            differences.append(i)
    
    # Check if exactly two adjacent positions are swapped
    if len(differences) == 2:
        i, j = differences
        if j == i + 1:  # Must be adjacent
            if original[i] == modified[j] and original[j] == modified[i]:
                return (i, j)
    
    return None


def analyze_error(original: str, modified: str) -> dict:
    """
    Analyze the type of error between original and modified numbers.
    
    Args:
        original: The original validated number.
        modified: The potentially modified number.
        
    Returns:
        dict: Analysis result with error type and details.
        
    Examples:
        >>> analyze_error("123451", "123351")
        {'valid': False, 'error_type': 'single_substitution', 'position': 3, 'details': (3, 4, 3)}
        >>> analyze_error("123451", "124351")
        {'valid': False, 'error_type': 'transposition', 'position': (2, 3), 'details': (2, 3)}
        >>> analyze_error("123451", "123451")
        {'valid': True, 'error_type': None}
    """
    result = {
        'valid': validate(modified),
        'error_type': None,
        'position': None,
        'details': None
    }
    
    if original == modified:
        result['valid'] = validate(original)
        return result
    
    # Check for single substitution
    single_err = detect_single_error(original, modified)
    if single_err:
        result['error_type'] = 'single_substitution'
        result['position'] = single_err[0]
        result['details'] = single_err
        return result
    
    # Check for transposition
    trans_err = detect_transposition_error(original, modified)
    if trans_err:
        result['error_type'] = 'transposition'
        result['position'] = trans_err
        result['details'] = trans_err
        return result
    
    # Multiple or complex errors
    if len(original) != len(modified):
        result['error_type'] = 'length_change'
    else:
        diff_count = sum(1 for o, m in zip(original, modified) if o != m)
        if diff_count > 2:
            result['error_type'] = 'multiple_errors'
        else:
            result['error_type'] = 'non_adjacent_swap'
    
    return result


# =============================================================================
# Comparison with Other Checksum Algorithms
# =============================================================================

def compare_with_luhn(number: str) -> dict:
    """
    Compare Verhoeff check digit with Luhn check digit.
    
    Note: Luhn and Verhoeff use different algorithms and produce different check digits.
    Both can validate the same data correctly using their respective methods.
    
    Args:
        number: A numeric string without check digit.
        
    Returns:
        dict: Comparison result with both check digits.
        
    Examples:
        >>> compare_with_luhn("12345")
        {'number': '12345', 'verhoeff_check': 1, 'luhn_check': 5, 'verhoeff_full': '123451', 'luhn_full': '123455'}
    """
    # Luhn algorithm implementation
    def luhn_check_digit(n: str) -> int:
        digits = [int(d) for d in n]
        doubled = []
        for i, d in enumerate(reversed(digits)):
            if i % 2 == 0:
                doubled.append(d * 2)
            else:
                doubled.append(d)
        total = sum(d // 10 + d % 10 for d in doubled)
        return (10 - (total % 10)) % 10
    
    verhoeff_cd = compute_check_digit(number)
    luhn_cd = luhn_check_digit(number)
    
    return {
        'number': number,
        'verhoeff_check': verhoeff_cd,
        'luhn_check': luhn_cd,
        'verhoeff_full': append_check_digit(number),
        'luhn_full': number + str(luhn_cd)
    }


# =============================================================================
# Batch Operations
# =============================================================================

def validate_batch(numbers: List[str]) -> List[Tuple[str, bool]]:
    """
    Validate multiple numbers at once.
    
    Args:
        numbers: List of numeric strings to validate.
        
    Returns:
        List[Tuple[str, bool]]: List of (number, is_valid) tuples.
        
    Examples:
        >>> validate_batch(["123451", "123450", "1428573"])
        [('123451', True), ('123450', False), ('1428573', True)]
    """
    return [(n, validate(n)) for n in numbers]


def generate_with_check_digits(numbers: List[str]) -> List[str]:
    """
    Generate numbers with check digits appended.
    
    Args:
        numbers: List of numeric strings (without check digits).
        
    Returns:
        List[str]: List of numbers with check digits appended.
        
    Examples:
        >>> generate_with_check_digits(["12345", "142857", "999"])
        ['123451', '1428573', '9995']
    """
    return [append_check_digit(n) for n in numbers]


# =============================================================================
# Educational Functions
# =============================================================================

def explain_algorithm() -> str:
    """
    Return an explanation of how the Verhoeff algorithm works.
    
    Returns:
        str: Detailed explanation of the algorithm.
    """
    return """
Verhoeff Algorithm Explanation
==============================

The Verhoeff algorithm is a checksum formula that detects all single-digit
errors and all transposition errors in numeric identifiers.

Mathematical Foundation:
- Uses the dihedral group D5, which is the symmetry group of a regular pentagon
- D5 has 10 elements: rotations (0-4) and reflections (5-9)
- The group operation is not commutative: a * b ≠ b * a in general

How It Works:
1. For each digit in the number (from right to left):
   - Apply a permutation based on the digit's position
   - Multiply with the running checksum using the D5 multiplication table

2. The check digit is chosen such that:
   - When included, the final multiplication result is 0 (identity)
   - This requires finding the inverse element

Why It's Powerful:
- Catches ALL single-digit substitution errors (Luhn misses 10%)
- Catches ALL adjacent digit transposition errors (Luhn catches most, not all)
- Catches about 95% of twin errors (aa → bb)
- Catches about 94% of jump transpositions (abc → cba)

The Tables:
- D5_MULTIPLICATION: Group operation table
- PERMUTATION: Position-dependent permutations (cycles every 8 positions)
- INVERSE: Table for finding multiplicative inverses

Algorithm Complexity:
- Time: O(n) where n is the number of digits
- Space: O(1) - only needs constant extra space

Use Cases:
- National identification numbers
- Product codes
- Account numbers
- Any system requiring strong error detection
"""


def show_computation_steps(number: str) -> str:
    """
    Show the step-by-step computation for a number.
    
    Args:
        number: A numeric string (without check digit).
        
    Returns:
        str: Step-by-step explanation of the computation.
        
    Examples:
        >>> print(show_computation_steps("12345"))
    """
    if not number.isdigit():
        return f"Error: '{number}' contains non-digit characters"
    
    steps = []
    steps.append(f"Computing Verhoeff check digit for: {number}")
    steps.append("=" * 50)
    steps.append("")
    
    check = 0
    reversed_digits = list(reversed(number))
    
    for i, digit_char in enumerate(reversed_digits):
        digit = int(digit_char)
        perm_index = i % 8
        permuted = PERMUTATION[perm_index][digit]
        old_check = check
        check = D5_MULTIPLICATION[check][permuted]
        
        steps.append(f"Step {i+1}:")
        steps.append(f"  Digit (from right): {digit}")
        steps.append(f"  Position index: {i} (perm_index = {i} mod 8 = {perm_index})")
        steps.append(f"  Permutation[{perm_index}][{digit}] = {permuted}")
        steps.append(f"  D5[{old_check}][{permuted}] = {check}")
        steps.append("")
    
    check_digit = INVERSE[check]
    steps.append(f"Final checksum: {check}")
    steps.append(f"Inverse of {check} = {check_digit}")
    steps.append("")
    steps.append(f"Check digit: {check_digit}")
    steps.append(f"Full number: {number}{check_digit}")
    
    return "\n".join(steps)


# =============================================================================
# Constants for External Use
# =============================================================================

__all__ = [
    # Core functions
    'compute_check_digit',
    'compute_check_digit_int',
    'validate',
    'validate_int',
    'append_check_digit',
    'append_check_digit_int',
    'get_check_digit_position',
    'extract_data_digits',
    'extract_data_digits_int',
    
    # Error detection
    'detect_single_error',
    'detect_transposition_error',
    'analyze_error',
    
    # Comparison
    'compare_with_luhn',
    
    # Batch operations
    'validate_batch',
    'generate_with_check_digits',
    
    # Educational
    'explain_algorithm',
    'show_computation_steps',
    
    # Tables (for advanced use)
    'D5_MULTIPLICATION',
    'PERMUTATION',
    'INVERSE',
]


if __name__ == "__main__":
    # Demo
    print("Verhoeff Algorithm Demo")
    print("=" * 50)
    
    # Basic usage
    test_numbers = ["12345", "142857", "999999", "0", ""]
    
    for num in test_numbers:
        full = append_check_digit(num)
        is_valid = validate(full)
        print(f"{num or '(empty)':10} -> {full:12} Valid: {is_valid}")
    
    print()
    print("Error Detection Examples:")
    print("-" * 30)
    
    original = "123451"
    errors = [
        ("123351", "Single digit error"),
        ("124351", "Transposition error"),
        ("123452", "Wrong check digit"),
    ]
    
    for modified, desc in errors:
        analysis = analyze_error(original, modified)
        print(f"{desc}: {original} -> {modified}")
        print(f"  Detected: {analysis}")
        print()
    
    # Show computation steps
    print(show_computation_steps("12345"))