"""
Roman Numeral Utilities
=======================

A comprehensive library for converting between Arabic numerals and Roman numerals.
Zero external dependencies - uses only Python standard library.

Features:
- Convert integers to Roman numerals (1 to 3999)
- Convert Roman numerals to integers
- Validate Roman numeral format
- Parse mixed content for Roman numerals
- Support for subtractive and additive notation

Author: AllToolkit
Date: 2026-05-10
"""

from typing import Optional, List, Tuple, Generator
import re


# Roman numeral mappings
ROMAN_TO_ARABIC = {
    'I': 1,
    'V': 5,
    'X': 10,
    'L': 50,
    'C': 100,
    'D': 500,
    'M': 1000,
}

ARABIC_TO_ROMAN = [
    (1000, 'M'),
    (900, 'CM'),
    (500, 'D'),
    (400, 'CD'),
    (100, 'C'),
    (90, 'XC'),
    (50, 'L'),
    (40, 'XL'),
    (10, 'X'),
    (9, 'IX'),
    (5, 'V'),
    (4, 'IV'),
    (1, 'I'),
]

# Valid Roman numeral pattern (basic validation)
ROMAN_PATTERN = re.compile(
    r'^M{0,3}'  # 0-3 M's (1000-3000)
    r'(CM|CD|D?C{0,3})'  # 900, 400, or 0-300 (500-800, 100-300)
    r'(XC|XL|L?X{0,3})'  # 90, 40, or 0-30 (50-80, 10-30)
    r'(IX|IV|V?I{0,3})$'  # 9, 4, or 0-3 (5-8, 1-3)
)


def to_roman(num: int) -> str:
    """
    Convert an integer to a Roman numeral.
    
    Args:
        num: Integer to convert (1-3999)
        
    Returns:
        Roman numeral string
        
    Raises:
        ValueError: If number is out of range (not 1-3999)
        TypeError: If input is not an integer
        
    Examples:
        >>> to_roman(1)
        'I'
        >>> to_roman(4)
        'IV'
        >>> to_roman(1994)
        'MCMXCIV'
    """
    if not isinstance(num, int):
        raise TypeError(f"Expected int, got {type(num).__name__}")
    
    if num < 1 or num > 3999:
        raise ValueError(f"Number out of range (1-3999), got {num}")
    
    result = []
    for value, symbol in ARABIC_TO_ROMAN:
        while num >= value:
            result.append(symbol)
            num -= value
    return ''.join(result)


def from_roman(roman: str) -> int:
    """
    Convert a Roman numeral to an integer.
    
    Args:
        roman: Roman numeral string (case-insensitive)
        
    Returns:
        Integer value
        
    Raises:
        ValueError: If input is not a valid Roman numeral
        TypeError: If input is not a string
        
    Examples:
        >>> from_roman('I')
        1
        >>> from_roman('IV')
        4
        >>> from_roman('MCMXCIV')
        1994
    """
    if not isinstance(roman, str):
        raise TypeError(f"Expected str, got {type(roman).__name__}")
    
    roman = roman.upper().strip()
    
    if not roman:
        raise ValueError("Empty string is not a valid Roman numeral")
    
    if not is_valid_roman(roman):
        raise ValueError(f"Invalid Roman numeral: {roman}")
    
    result = 0
    prev_value = 0
    
    for char in reversed(roman):
        value = ROMAN_TO_ARABIC[char]
        if value < prev_value:
            result -= value
        else:
            result += value
        prev_value = value
    
    return result


def is_valid_roman(roman: str) -> bool:
    """
    Check if a string is a valid Roman numeral.
    
    Args:
        roman: String to validate (case-insensitive)
        
    Returns:
        True if valid, False otherwise
        
    Examples:
        >>> is_valid_roman('IV')
        True
        >>> is_valid_roman('IIII')
        False
        >>> is_valid_roman('IX')
        True
    """
    if not isinstance(roman, str):
        return False
    
    roman = roman.upper().strip()
    
    if not roman:
        return False
    
    # Check if all characters are valid Roman numerals
    if not all(char in ROMAN_TO_ARABIC for char in roman):
        return False
    
    # Check against the pattern
    return bool(ROMAN_PATTERN.match(roman))


def parse_roman_in_text(text: str) -> List[Tuple[str, int, int, int]]:
    """
    Find and parse all Roman numerals in a text.
    
    Args:
        text: Text to search for Roman numerals
        
    Returns:
        List of tuples (roman, value, start_pos, end_pos)
        
    Examples:
        >>> parse_roman_in_text("Chapter IV and Chapter IX")
        [('IV', 4, 8, 10), ('IX', 9, 21, 23)]
    """
    # Pattern to find potential Roman numerals
    pattern = re.compile(r'\b[MCDXLVI]{1,15}\b')
    results = []
    
    for match in pattern.finditer(text):
        roman = match.group()
        if is_valid_roman(roman):
            try:
                value = from_roman(roman)
                results.append((roman, value, match.start(), match.end()))
            except ValueError:
                continue
    
    return results


def roman_range(start: int, end: int, step: int = 1) -> Generator[str, None, None]:
    """
    Generate Roman numerals in a range (similar to Python's range).
    
    Args:
        start: Start value (inclusive)
        end: End value (exclusive)
        step: Step value (default 1)
        
    Yields:
        Roman numeral strings
        
    Examples:
        >>> list(roman_range(1, 6))
        ['I', 'II', 'III', 'IV', 'V']
    """
    for num in range(start, end, step):
        yield to_roman(num)


def add_roman(roman1: str, roman2: str) -> str:
    """
    Add two Roman numerals and return the result.
    
    Args:
        roman1: First Roman numeral
        roman2: Second Roman numeral
        
    Returns:
        Sum as Roman numeral
        
    Examples:
        >>> add_roman('X', 'V')
        'XV'
        >>> add_roman('IV', 'I')
        'V'
    """
    return to_roman(from_roman(roman1) + from_roman(roman2))


def subtract_roman(roman1: str, roman2: str) -> str:
    """
    Subtract two Roman numerals and return the result.
    
    Args:
        roman1: First Roman numeral (minuend)
        roman2: Second Roman numeral (subtrahend)
        
    Returns:
        Difference as Roman numeral
        
    Raises:
        ValueError: If result is not in valid range (1-3999)
        
    Examples:
        >>> subtract_roman('X', 'V')
        'V'
        >>> subtract_roman('V', 'I')
        'IV'
    """
    result = from_roman(roman1) - from_roman(roman2)
    return to_roman(result)


def compare_roman(roman1: str, roman2: str) -> int:
    """
    Compare two Roman numerals.
    
    Args:
        roman1: First Roman numeral
        roman2: Second Roman numeral
        
    Returns:
        -1 if roman1 < roman2, 0 if equal, 1 if roman1 > roman2
        
    Examples:
        >>> compare_roman('V', 'X')
        -1
        >>> compare_roman('X', 'X')
        0
        >>> compare_roman('X', 'V')
        1
    """
    val1 = from_roman(roman1)
    val2 = from_roman(roman2)
    if val1 < val2:
        return -1
    elif val1 > val2:
        return 1
    return 0


def get_roman_info(roman: str) -> dict:
    """
    Get detailed information about a Roman numeral.
    
    Args:
        roman: Roman numeral string
        
    Returns:
        Dictionary with information
        
    Examples:
        >>> info = get_roman_info('MCMXCIV')
        >>> info['value']
        1994
        >>> info['valid']
        True
    """
    roman = roman.upper().strip()
    valid = is_valid_roman(roman)
    
    info = {
        'roman': roman,
        'valid': valid,
        'value': None,
        'length': len(roman),
        'characters': list(roman) if roman else [],
        'breakdown': [],
    }
    
    if valid:
        info['value'] = from_roman(roman)
        # Generate breakdown
        remaining = info['value']
        for value, symbol in ARABIC_TO_ROMAN:
            if remaining >= value:
                count = remaining // value
                info['breakdown'].append({
                    'symbol': symbol,
                    'value': value,
                    'count': count,
                })
                remaining -= value * count
    
    return info


def format_with_ordinal(num: int, use_roman: bool = True) -> str:
    """
    Format a number with Roman numeral or ordinal suffix.
    
    Args:
        num: Number to format
        use_roman: If True, use Roman numeral; otherwise use ordinal suffix
        
    Returns:
        Formatted string
        
    Examples:
        >>> format_with_ordinal(1)
        'I'
        >>> format_with_ordinal(1, use_roman=False)
        '1st'
        >>> format_with_ordinal(3, use_roman=False)
        '3rd'
    """
    if use_roman:
        return to_roman(num)
    
    if num % 100 in (11, 12, 13):
        suffix = 'th'
    else:
        suffix = {1: 'st', 2: 'nd', 3: 'rd'}.get(num % 10, 'th')
    
    return f"{num}{suffix}"


# Common Roman numeral constants
ROMAN_ONES = ['I', 'II', 'III', 'IV', 'V', 'VI', 'VII', 'VIII', 'IX', 'X']
ROMAN_TENS = ['X', 'XX', 'XXX', 'XL', 'L', 'LX', 'LXX', 'LXXX', 'XC', 'C']
ROMAN_HUNDREDS = ['C', 'CC', 'CCC', 'CD', 'D', 'DC', 'DCC', 'DCCC', 'CM', 'M']


if __name__ == '__main__':
    # Demo
    print("Roman Numeral Utilities Demo")
    print("=" * 40)
    
    # Basic conversions
    for i in [1, 4, 9, 49, 99, 499, 999, 1994, 2024, 3999]:
        roman = to_roman(i)
        back = from_roman(roman)
        print(f"{i:4} -> {roman:8} -> {back}")
    
    print("\n" + "=" * 40)
    
    # Parse text
    text = "King Henry VIII had VI wives. Chapter IV starts on page XIX."
    parsed = parse_roman_in_text(text)
    print(f"\nParsing: {text}")
    for roman, value, start, end in parsed:
        print(f"  Found '{roman}' ({value}) at position {start}-{end}")
    
    print("\n" + "=" * 40)
    
    # Arithmetic
    print("\nArithmetic:")
    print(f"  X + V = {add_roman('X', 'V')}")
    print(f"  X - V = {subtract_roman('X', 'V')}")
    print(f"  IV + I = {add_roman('IV', 'I')}")