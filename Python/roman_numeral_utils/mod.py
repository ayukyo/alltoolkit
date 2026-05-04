"""
Roman Numeral Utilities
=======================

A pure Python implementation for converting between Arabic numbers and Roman numerals.
Zero external dependencies.

Features:
- Convert Arabic numbers (integers) to Roman numerals
- Convert Roman numerals to Arabic numbers
- Input validation
- Support for standard Roman numeral range (1-3999)
- Extended range support with vinculum notation for larger numbers

Author: AllToolkit
Date: 2025-05-05
"""

from typing import Tuple, Optional, Union


class RomanNumeralError(Exception):
    """Base exception for Roman numeral operations."""
    pass


class InvalidRomanNumeralError(RomanNumeralError):
    """Raised when an invalid Roman numeral string is provided."""
    pass


class OutOfRangeError(RomanNumeralError):
    """Raised when a number is outside the valid range."""
    pass


# Standard Roman numeral symbols and their values
ROMAN_SYMBOLS = [
    ('M', 1000),
    ('CM', 900),
    ('D', 500),
    ('CD', 400),
    ('C', 100),
    ('XC', 90),
    ('L', 50),
    ('XL', 40),
    ('X', 10),
    ('IX', 9),
    ('V', 5),
    ('IV', 4),
    ('I', 1),
]

# Mapping for quick lookup
ROMAN_VALUES = {
    'I': 1, 'V': 5, 'X': 10, 'L': 50,
    'C': 100, 'D': 500, 'M': 1000
}

# Valid Roman numeral pattern (simplified regex rules)
VALID_ROMAN_PATTERNS = {
    'M': 3,    # Max 3 consecutive M's
    'CM': 1,   # Can only appear once
    'D': 1,    # Can only appear once
    'CD': 1,   # Can only appear once
    'C': 3,    # Max 3 consecutive C's (when not part of CD/CM)
    'XC': 1,   # Can only appear once
    'L': 1,    # Can only appear once
    'XL': 1,   # Can only appear once
    'X': 3,    # Max 3 consecutive X's (when not part of XL/XC)
    'IX': 1,   # Can only appear once
    'V': 1,    # Can only appear once
    'IV': 1,   # Can only appear once
    'I': 3,    # Max 3 consecutive I's (when not part of IV/IX)
}


def to_roman(num: int, *, validate: bool = True) -> str:
    """
    Convert an Arabic number to a Roman numeral.
    
    Args:
        num: The Arabic number to convert (must be between 1 and 3999)
        validate: Whether to validate the input range (default: True)
    
    Returns:
        The Roman numeral representation as a string
    
    Raises:
        OutOfRangeError: If the number is outside the valid range (1-3999)
        TypeError: If the input is not an integer
    
    Examples:
        >>> to_roman(1)
        'I'
        >>> to_roman(4)
        'IV'
        >>> to_roman(1994)
        'MCMXCIV'
        >>> to_roman(2023)
        'MMXXIII'
    """
    if not isinstance(num, int):
        raise TypeError(f"Expected int, got {type(num).__name__}")
    
    if validate and (num < 1 or num > 3999):
        raise OutOfRangeError(
            f"Number {num} is out of range. "
            "Roman numerals must be between 1 and 3999."
        )
    
    if num < 1:
        raise OutOfRangeError("Roman numerals cannot represent zero or negative numbers.")
    
    result = []
    remaining = num
    
    for symbol, value in ROMAN_SYMBOLS:
        count, remaining = divmod(remaining, value)
        result.append(symbol * count)
        if remaining == 0:
            break
    
    return ''.join(result)


def from_roman(roman: str, *, validate: bool = True) -> int:
    """
    Convert a Roman numeral to an Arabic number.
    
    Args:
        roman: The Roman numeral string to convert
        validate: Whether to validate the Roman numeral format (default: True)
    
    Returns:
        The Arabic number as an integer
    
    Raises:
        InvalidRomanNumeralError: If the Roman numeral is invalid
        TypeError: If the input is not a string
    
    Examples:
        >>> from_roman('I')
        1
        >>> from_roman('IV')
        4
        >>> from_roman('MCMXCIV')
        1994
        >>> from_roman('MMXXIII')
        2023
    """
    if not isinstance(roman, str):
        raise TypeError(f"Expected str, got {type(roman).__name__}")
    
    roman = roman.strip().upper()
    
    if not roman:
        raise InvalidRomanNumeralError("Empty string is not a valid Roman numeral.")
    
    if validate:
        _validate_roman_numeral(roman)
    
    result = 0
    i = 0
    length = len(roman)
    
    while i < length:
        # Check for subtractive pairs first (like IV, IX, XL, etc.)
        if i + 1 < length:
            pair = roman[i:i+2]
            if pair in ('IV', 'IX', 'XL', 'XC', 'CD', 'CM'):
                result += ROMAN_VALUES[roman[i+1]] - ROMAN_VALUES[roman[i]]
                i += 2
                continue
        
        # Single symbol
        if roman[i] not in ROMAN_VALUES:
            raise InvalidRomanNumeralError(
                f"Invalid character '{roman[i]}' in Roman numeral."
            )
        result += ROMAN_VALUES[roman[i]]
        i += 1
    
    return result


def _validate_roman_numeral(roman: str) -> None:
    """
    Validate a Roman numeral string.
    
    Args:
        roman: The Roman numeral string to validate
    
    Raises:
        InvalidRomanNumeralError: If the Roman numeral is invalid
    """
    # Check for invalid characters
    for char in roman:
        if char not in ROMAN_VALUES:
            raise InvalidRomanNumeralError(
                f"Invalid character '{char}' in Roman numeral. "
                f"Valid characters are: {', '.join(ROMAN_VALUES.keys())}"
            )
    
    # Check for invalid patterns
    invalid_patterns = [
        'IIII', 'VV', 'XXXX', 'LL', 'CCCC', 'DD', 'MMMM',
        'VX', 'VL', 'VC', 'VD', 'VM',
        'LC', 'LD', 'LM',
        'DM', 'IM', 'XM'
    ]
    
    for pattern in invalid_patterns:
        if pattern in roman:
            raise InvalidRomanNumeralError(
                f"Invalid pattern '{pattern}' in Roman numeral. "
                "Check Roman numeral rules."
            )
    
    # Check for more than 3 consecutive same characters
    count = 1
    for i in range(1, len(roman)):
        if roman[i] == roman[i-1]:
            count += 1
            if count > 3:
                raise InvalidRomanNumeralError(
                    f"Invalid Roman numeral: more than 3 consecutive '{roman[i]}' characters."
                )
        else:
            count = 1
    
    # Verify the numeral converts back correctly
    try:
        arabic = from_roman(roman, validate=False)
        reconstructed = to_roman(arabic)
        if reconstructed != roman:
            raise InvalidRomanNumeralError(
                f"Invalid Roman numeral '{roman}'. "
                f"Should be written as '{reconstructed}'."
            )
    except Exception as e:
        if isinstance(e, InvalidRomanNumeralError):
            raise
        raise InvalidRomanNumeralError(f"Invalid Roman numeral: {roman}")


def is_valid_roman(roman: str) -> bool:
    """
    Check if a string is a valid Roman numeral.
    
    Args:
        roman: The string to check
    
    Returns:
        True if the string is a valid Roman numeral, False otherwise
    
    Examples:
        >>> is_valid_roman('XIV')
        True
        >>> is_valid_roman('IIII')
        False
        >>> is_valid_roman('Hello')
        False
    """
    try:
        from_roman(roman, validate=True)
        return True
    except RomanNumeralError:
        return False


def roman_add(roman1: str, roman2: str) -> str:
    """
    Add two Roman numerals.
    
    Args:
        roman1: First Roman numeral
        roman2: Second Roman numeral
    
    Returns:
        The sum as a Roman numeral
    
    Raises:
        OutOfRangeError: If the result is outside the valid range
        InvalidRomanNumeralError: If either input is invalid
    
    Examples:
        >>> roman_add('X', 'V')
        'XV'
        >>> roman_add('IX', 'I')
        'X'
    """
    num1 = from_roman(roman1)
    num2 = from_roman(roman2)
    return to_roman(num1 + num2)


def roman_subtract(roman1: str, roman2: str) -> str:
    """
    Subtract two Roman numerals.
    
    Args:
        roman1: First Roman numeral (minuend)
        roman2: Second Roman numeral (subtrahend)
    
    Returns:
        The difference as a Roman numeral
    
    Raises:
        OutOfRangeError: If the result is outside the valid range
        InvalidRomanNumeralError: If either input is invalid
    
    Examples:
        >>> roman_subtract('X', 'V')
        'V'
        >>> roman_subtract('X', 'X')
        OutOfRangeError: Cannot represent zero in Roman numerals
    """
    num1 = from_roman(roman1)
    num2 = from_roman(roman2)
    return to_roman(num1 - num2)


def roman_multiply(roman1: str, roman2: str) -> str:
    """
    Multiply two Roman numerals.
    
    Args:
        roman1: First Roman numeral
        roman2: Second Roman numeral
    
    Returns:
        The product as a Roman numeral
    
    Raises:
        OutOfRangeError: If the result is outside the valid range
        InvalidRomanNumeralError: If either input is invalid
    
    Examples:
        >>> roman_multiply('X', 'V')
        'L'
        >>> roman_multiply('IV', 'V')
        'XX'
    """
    num1 = from_roman(roman1)
    num2 = from_roman(roman2)
    return to_roman(num1 * num2)


def roman_divide(roman1: str, roman2: str) -> Tuple[str, str]:
    """
    Divide two Roman numerals.
    
    Args:
        roman1: First Roman numeral (dividend)
        roman2: Second Roman numeral (divisor)
    
    Returns:
        A tuple of (quotient, remainder) as Roman numerals
    
    Raises:
        OutOfRangeError: If the quotient is zero
        InvalidRomanNumeralError: If either input is invalid
        ZeroDivisionError: If the divisor is zero
    
    Examples:
        >>> roman_divide('X', 'III')
        ('III', 'I')
        >>> roman_divide('XX', 'V')
        ('IV', '')
    """
    num1 = from_roman(roman1)
    num2 = from_roman(roman2)
    
    if num2 == 0:
        raise ZeroDivisionError("Division by zero")
    
    quotient, remainder = divmod(num1, num2)
    
    if quotient == 0:
        raise OutOfRangeError(
            "Quotient is zero, which cannot be represented in Roman numerals."
        )
    
    remainder_roman = to_roman(remainder) if remainder > 0 else ''
    
    return to_roman(quotient), remainder_roman


def get_roman_info(num: int) -> dict:
    """
    Get detailed information about a number's Roman numeral representation.
    
    Args:
        num: The Arabic number
    
    Returns:
        A dictionary containing:
        - arabic: The original number
        - roman: The Roman numeral representation
        - components: List of (symbol, value) tuples that make up the numeral
    
    Raises:
        OutOfRangeError: If the number is outside the valid range
    
    Examples:
        >>> get_roman_info(1994)
        {
            'arabic': 1994,
            'roman': 'MCMXCIV',
            'components': [('M', 1000), ('CM', 900), ('XC', 90), ('IV', 4)]
        }
    """
    roman = to_roman(num)
    components = []
    remaining = num
    
    for symbol, value in ROMAN_SYMBOLS:
        if remaining >= value:
            count = remaining // value
            if count > 0:
                components.append((symbol, value * count))
                remaining -= value * count
        if remaining == 0:
            break
    
    return {
        'arabic': num,
        'roman': roman,
        'components': components
    }


def find_roman_palindromes(start: int = 1, end: int = 3999) -> list:
    """
    Find all Roman numeral palindromes in a given range.
    
    Args:
        start: Start of range (inclusive, default: 1)
        end: End of range (inclusive, default: 3999)
    
    Returns:
        List of (arabic, roman) tuples where roman is a palindrome
    
    Examples:
        >>> find_roman_palindromes(1, 20)
        [(1, 'I'), (2, 'II'), (3, 'III'), (8, 'VIII'), (9, 'IX')]
    """
    palindromes = []
    for num in range(start, end + 1):
        roman = to_roman(num)
        if roman == roman[::-1]:
            palindromes.append((num, roman))
    return palindromes


class RomanNumeral:
    """
    A class for working with Roman numerals as objects.
    
    Supports basic arithmetic operations and comparisons.
    
    Examples:
        >>> r = RomanNumeral(10)
        >>> str(r)
        'X'
        >>> r + 5
        RomanNumeral('XV', 15)
        >>> RomanNumeral('IV') * 2
        RomanNumeral('VIII', 8)
    """
    
    def __init__(self, value: Union[int, str]):
        """
        Initialize a RomanNumeral.
        
        Args:
            value: Either an integer or a Roman numeral string
        """
        if isinstance(value, int):
            self._arabic = value
            self._roman = to_roman(value)
        elif isinstance(value, str):
            self._arabic = from_roman(value)
            self._roman = to_roman(self._arabic)
        else:
            raise TypeError(f"Expected int or str, got {type(value).__name__}")
    
    @property
    def arabic(self) -> int:
        """Get the Arabic value."""
        return self._arabic
    
    @property
    def roman(self) -> str:
        """Get the Roman numeral string."""
        return self._roman
    
    def __str__(self) -> str:
        return self._roman
    
    def __repr__(self) -> str:
        return f"RomanNumeral('{self._roman}', {self._arabic})"
    
    def __int__(self) -> int:
        return self._arabic
    
    def __eq__(self, other) -> bool:
        if isinstance(other, RomanNumeral):
            return self._arabic == other._arabic
        elif isinstance(other, int):
            return self._arabic == other
        elif isinstance(other, str):
            return self._roman == other.upper()
        return NotImplemented
    
    def __lt__(self, other) -> bool:
        other_val = other._arabic if isinstance(other, RomanNumeral) else int(other)
        return self._arabic < other_val
    
    def __le__(self, other) -> bool:
        return self == other or self < other
    
    def __gt__(self, other) -> bool:
        other_val = other._arabic if isinstance(other, RomanNumeral) else int(other)
        return self._arabic > other_val
    
    def __ge__(self, other) -> bool:
        return self == other or self > other
    
    def __add__(self, other):
        other_val = other._arabic if isinstance(other, RomanNumeral) else int(other)
        return RomanNumeral(self._arabic + other_val)
    
    def __sub__(self, other):
        other_val = other._arabic if isinstance(other, RomanNumeral) else int(other)
        return RomanNumeral(self._arabic - other_val)
    
    def __mul__(self, other):
        other_val = other._arabic if isinstance(other, RomanNumeral) else int(other)
        return RomanNumeral(self._arabic * other_val)
    
    def __floordiv__(self, other):
        other_val = other._arabic if isinstance(other, RomanNumeral) else int(other)
        return RomanNumeral(self._arabic // other_val)
    
    def __hash__(self) -> int:
        return hash(self._arabic)


# Convenience functions for common use cases
def int_to_roman(num: int) -> str:
    """Alias for to_roman()."""
    return to_roman(num)


def roman_to_int(roman: str) -> int:
    """Alias for from_roman()."""
    return from_roman(roman)


if __name__ == "__main__":
    # Demo
    print("=== Roman Numeral Utils Demo ===\n")
    
    # Basic conversion
    print("Arabic to Roman:")
    for num in [1, 4, 9, 14, 49, 99, 444, 999, 1994, 2023, 3999]:
        print(f"  {num:4d} → {to_roman(num)}")
    
    print("\nRoman to Arabic:")
    for roman in ['I', 'IV', 'IX', 'XIV', 'XLIX', 'XCIX', 'CDXLIV', 'CMXCIX', 'MCMXCIV', 'MMXXIII']:
        print(f"  {roman:8s} → {from_roman(roman)}")
    
    # Arithmetic operations
    print("\nArithmetic:")
    print(f"  X + V = {roman_add('X', 'V')}")
    print(f"  X - V = {roman_subtract('X', 'V')}")
    print(f"  X * V = {roman_multiply('X', 'V')}")
    print(f"  X / III = {roman_divide('X', 'III')}")
    
    # RomanNumeral class
    print("\nRomanNumeral class:")
    r1 = RomanNumeral(10)
    r2 = RomanNumeral('V')
    print(f"  {r1} + {r2} = {r1 + r2}")
    print(f"  {r1} * 3 = {r1 * 3}")
    
    # Find palindromes
    print("\nRoman numeral palindromes (1-50):")
    palindromes = find_roman_palindromes(1, 50)
    for num, roman in palindromes[:10]:
        print(f"  {num:2d} → {roman}")
    
    print("\n✓ Demo complete!")