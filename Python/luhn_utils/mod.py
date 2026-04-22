"""
Luhn Algorithm Utilities
========================

A comprehensive implementation of the Luhn algorithm (also known as the
"modulus 10" or "mod 10" algorithm) for validating and generating check digits.

The Luhn algorithm is used for validating:
- Credit card numbers
- IMEI numbers (International Mobile Equipment Identity)
- National Provider Identifier numbers (US healthcare)
- Canadian Social Insurance Numbers
- Greek Social Security Numbers (AMKA)
- South African ID numbers
- And many other identification numbers

Features:
- Validate numbers using Luhn algorithm
- Calculate check digits
- Generate valid test numbers
- Format and parse numbers
- Zero external dependencies

Reference: https://en.wikipedia.org/wiki/Luhn_algorithm
"""

from typing import Tuple, List, Optional
import random


def calculate_check_digit(number: str) -> int:
    """
    Calculate the Luhn check digit for a given number.
    
    The check digit is the digit that, when appended to the number,
    makes it pass the Luhn validation.
    
    Args:
        number: The number string (without check digit).
                Can contain spaces and hyphens (will be stripped).
    
    Returns:
        The check digit (0-9).
    
    Example:
        >>> calculate_check_digit("453201511283036")
        6
        >>> # Visa card number: 4532015112830366
    """
    # Remove non-digit characters
    clean_number = ''.join(c for c in number if c.isdigit())
    
    if not clean_number:
        raise ValueError("Number must contain at least one digit")
    
    # Double every other digit from right to left, starting with the first
    total = 0
    digits = [int(d) for d in clean_number]
    
    # We're calculating the check digit, so we double positions that would
    # NOT be doubled if the check digit was present (odd positions from right)
    for i, digit in enumerate(reversed(digits)):
        if i % 2 == 0:  # Double every other digit starting from the rightmost
            doubled = digit * 2
            if doubled > 9:
                doubled = doubled - 9
            total += doubled
        else:
            total += digit
    
    # Check digit is (10 - (total % 10)) % 10
    return (10 - (total % 10)) % 10


def validate(number: str) -> bool:
    """
    Validate a number using the Luhn algorithm.
    
    Args:
        number: The number string to validate.
                Can contain spaces and hyphens (will be stripped).
    
    Returns:
        True if the number is valid according to Luhn algorithm, False otherwise.
    
    Example:
        >>> validate("4532015112830366")  # Valid Visa card
        True
        >>> validate("4532015112830367")  # Invalid
        False
        >>> validate("4532-0151-1283-0366")  # With formatting
        True
    """
    # Remove non-digit characters
    clean_number = ''.join(c for c in number if c.isdigit())
    
    if len(clean_number) < 2:
        return False
    
    total = 0
    digits = [int(d) for d in clean_number]
    
    # Double every second digit from right to left
    for i, digit in enumerate(reversed(digits)):
        if i % 2 == 1:  # Double every second digit
            doubled = digit * 2
            if doubled > 9:
                doubled = doubled - 9
            total += doubled
        else:
            total += digit
    
    return total % 10 == 0


def add_check_digit(number: str) -> str:
    """
    Append the Luhn check digit to a number.
    
    Args:
        number: The number string (without check digit).
    
    Returns:
        The number with the check digit appended.
    
    Example:
        >>> add_check_digit("453201511283036")
        '4532015112830366'
    """
    check_digit = calculate_check_digit(number)
    clean_number = ''.join(c for c in number if c.isdigit())
    return clean_number + str(check_digit)


def strip_formatting(number: str) -> str:
    """
    Remove all non-digit characters from a number string.
    
    Args:
        number: The number string possibly containing spaces, hyphens, etc.
    
    Returns:
        The number string with only digits.
    
    Example:
        >>> strip_formatting("4532-0151-1283-0366")
        '4532015112830366'
        >>> strip_formatting("4532 0151 1283 0366")
        '4532015112830366'
    """
    return ''.join(c for c in number if c.isdigit())


def format_number(number: str, group_size: int = 4, separator: str = " ") -> str:
    """
    Format a number by grouping digits.
    
    Args:
        number: The number string.
        group_size: Number of digits per group (default: 4).
        separator: Separator between groups (default: space).
    
    Returns:
        The formatted number string.
    
    Example:
        >>> format_number("4532015112830366")
        '4532 0151 1283 0366'
        >>> format_number("4532015112830366", group_size=4, separator="-")
        '4532-0151-1283-0366'
    """
    clean_number = strip_formatting(number)
    
    if not clean_number:
        return ""
    
    groups = [clean_number[i:i+group_size] for i in range(0, len(clean_number), group_size)]
    return separator.join(groups)


def generate_valid_number(prefix: str, length: int = 16) -> str:
    """
    Generate a valid Luhn number with the given prefix.
    
    This is useful for generating test credit card numbers.
    
    Args:
        prefix: The prefix for the number (e.g., "4" for Visa).
        length: The desired total length of the number (default: 16).
    
    Returns:
        A valid Luhn number with the specified prefix and length.
    
    Example:
        >>> number = generate_valid_number("4", 16)  # Generate Visa-like number
        >>> validate(number)
        True
        >>> number = generate_valid_number("5", 16)  # Generate MasterCard-like number
        >>> validate(number)
        True
    """
    if length <= len(prefix):
        raise ValueError(f"Length must be greater than prefix length ({len(prefix)})")
    
    clean_prefix = strip_formatting(prefix)
    
    if not clean_prefix:
        raise ValueError("Prefix must contain at least one digit")
    
    # Fill remaining digits (except check digit) with random digits
    remaining_length = length - len(clean_prefix) - 1
    random_digits = ''.join(str(random.randint(0, 9)) for _ in range(remaining_length))
    
    # Combine prefix and random digits
    number_without_check = clean_prefix + random_digits
    
    # Calculate and append check digit
    return add_check_digit(number_without_check)


def generate_test_credit_cards(count: int = 5) -> List[Tuple[str, str]]:
    """
    Generate test credit card numbers for various card types.
    
    These are TEST numbers only and will not work for actual transactions.
    They are generated to pass Luhn validation.
    
    Args:
        count: Number of cards to generate per type (default: 5).
    
    Returns:
        List of tuples (card_type, card_number).
    
    Example:
        >>> cards = generate_test_credit_cards(2)
        >>> for card_type, number in cards:
        ...     print(f"{card_type}: {number}")
        ...     assert validate(number)
    """
    # Common card prefixes
    card_prefixes = {
        "Visa": ["4"],
        "MasterCard": ["51", "52", "53", "54", "55", "2221", "2222", "2223"],
        "American Express": ["34", "37"],
        "Discover": ["6011", "622126", "644", "645", "65"],
        "JCB": ["3528", "3529", "353"],
        "Diners Club": ["300", "301", "302", "303", "304", "305", "36", "38"],
        "UnionPay": ["62"],
    }
    
    cards = []
    
    for card_type, prefixes in card_prefixes.items():
        for _ in range(count):
            prefix = random.choice(prefixes)
            # Use appropriate length based on card type
            if card_type == "American Express":
                length = 15
            elif card_type == "Diners Club":
                length = 14
            else:
                length = 16
            
            try:
                number = generate_valid_number(prefix, length)
                cards.append((card_type, number))
            except ValueError:
                continue
    
    return cards


def find_check_digit_errors(number: str) -> List[int]:
    """
    Find positions where a single digit error would make the number valid.
    
    This is useful for error detection and correction suggestions.
    
    Args:
        number: The potentially invalid number string.
    
    Returns:
        List of positions (0-indexed) where changing the digit could fix the number.
    
    Example:
        >>> # If a number is invalid, find potential error positions
        >>> errors = find_check_digit_errors("4532015112830367")
    """
    clean_number = strip_formatting(number)
    
    if not clean_number:
        return []
    
    if validate(clean_number):
        return []  # Already valid
    
    error_positions = []
    digits = list(clean_number)
    
    for i in range(len(digits)):
        original = digits[i]
        for new_digit in '0123456789':
            if new_digit == original:
                continue
            digits[i] = new_digit
            if validate(''.join(digits)):
                error_positions.append(i)
                break
        digits[i] = original
    
    return error_positions


def calculate_luhn_sum(number: str) -> Tuple[int, bool]:
    """
    Calculate the Luhn sum and return both the sum and validity.
    
    This is useful for debugging or educational purposes.
    
    Args:
        number: The number string to calculate sum for.
    
    Returns:
        Tuple of (total_sum, is_valid).
    
    Example:
        >>> total, valid = calculate_luhn_sum("4532015112830366")
        >>> print(f"Sum: {total}, Valid: {valid}")
        Sum: 80, Valid: True
    """
    clean_number = ''.join(c for c in number if c.isdigit())
    
    if not clean_number:
        return (0, False)
    
    total = 0
    digits = [int(d) for d in clean_number]
    
    for i, digit in enumerate(reversed(digits)):
        if i % 2 == 1:
            doubled = digit * 2
            if doubled > 9:
                doubled = doubled - 9
            total += doubled
        else:
            total += digit
    
    return (total, total % 10 == 0)


def get_luhn_digit_transformations(digit: int, position: int, total_length: int) -> List[int]:
    """
    Get the valid transformations for a digit at a given position.
    
    This shows what values a digit can be changed to while maintaining
    Luhn validity.
    
    Args:
        digit: The current digit value (0-9).
        position: The position of the digit (0-indexed from left).
        total_length: The total length of the number.
    
    Returns:
        List of valid digit values that could replace the current digit.
    
    Example:
        >>> get_luhn_digit_transformations(5, 0, 16)
    """
    if digit < 0 or digit > 9:
        raise ValueError("Digit must be between 0 and 9")
    
    # Calculate position from right
    position_from_right = total_length - position - 1
    
    # If position from right is odd, digit is doubled
    is_doubled = position_from_right % 2 == 1
    
    valid_values = []
    for new_digit in range(10):
        if new_digit == digit:
            continue
        # Calculate the Luhn contribution of each digit
        if is_doubled:
            orig_contribution = digit * 2
            if orig_contribution > 9:
                orig_contribution -= 9
            new_contribution = new_digit * 2
            if new_contribution > 9:
                new_contribution -= 9
        else:
            orig_contribution = digit
            new_contribution = new_digit
        
        # The difference in contribution
        diff = new_contribution - orig_contribution
        
        # If difference is a multiple of 10, validity is preserved
        if diff % 10 == 0:
            valid_values.append(new_digit)
    
    return valid_values


class LuhnValidator:
    """
    A class-based validator for Luhn numbers.
    
    Provides a convenient interface for validating and generating
    Luhn-compliant numbers.
    
    Example:
        >>> validator = LuhnValidator()
        >>> validator.validate("4532015112830366")
        True
        >>> validator.generate("4", 16)  # Generate Visa-like number
        '4...'
    """
    
    def __init__(self, group_size: int = 4, separator: str = " "):
        """
        Initialize the validator with formatting options.
        
        Args:
            group_size: Default group size for formatting.
            separator: Default separator for formatting.
        """
        self.group_size = group_size
        self.separator = separator
    
    def validate(self, number: str) -> bool:
        """Validate a number using the Luhn algorithm."""
        return validate(number)
    
    def calculate_check_digit(self, number: str) -> int:
        """Calculate the check digit for a number."""
        return calculate_check_digit(number)
    
    def add_check_digit(self, number: str) -> str:
        """Append the check digit to a number."""
        return add_check_digit(number)
    
    def format(self, number: str) -> str:
        """Format a number with the default group size and separator."""
        return format_number(number, self.group_size, self.separator)
    
    def strip(self, number: str) -> str:
        """Remove formatting from a number."""
        return strip_formatting(number)
    
    def generate(self, prefix: str, length: int = 16) -> str:
        """Generate a valid Luhn number with the given prefix."""
        return generate_valid_number(prefix, length)
    
    def generate_batch(self, prefix: str, count: int, length: int = 16) -> List[str]:
        """Generate multiple valid Luhn numbers."""
        return [self.generate(prefix, length) for _ in range(count)]


# Convenience constants for common card prefixes
CARD_PREFIXES = {
    "visa": ["4"],
    "mastercard": ["51", "52", "53", "54", "55", "2221", "2222", "2223", "2224", "2225"],
    "amex": ["34", "37"],
    "discover": ["6011", "622126", "644", "645", "646", "647", "648", "649", "65"],
    "jcb": ["3528", "3529", "353", "354", "355", "356", "357", "358"],
    "diners": ["300", "301", "302", "303", "304", "305", "36", "38", "39"],
    "unionpay": ["62", "81"],
    "maestro": ["5018", "5020", "5038", "5893", "6304", "6759", "6761", "6762", "6763"],
    "mir": ["2200", "2201", "2202", "2203", "2204"],
}


def identify_card_type(number: str) -> Optional[str]:
    """
    Attempt to identify the card type based on the number prefix.
    
    This uses common prefix patterns and does not validate the number.
    Always validate the number separately before use.
    
    Args:
        number: The card number string.
    
    Returns:
        The card type name or None if not recognized.
    
    Example:
        >>> identify_card_type("4111111111111111")
        'visa'
        >>> identify_card_type("5500000000000004")
        'mastercard'
    """
    clean_number = strip_formatting(number)
    
    if not clean_number:
        return None
    
    for card_type, prefixes in CARD_PREFIXES.items():
        for prefix in prefixes:
            if clean_number.startswith(prefix):
                return card_type
    
    return None


if __name__ == "__main__":
    # Demo
    print("Luhn Algorithm Utilities Demo")
    print("=" * 50)
    
    # Validate examples
    test_numbers = [
        ("Valid Visa", "4532015112830366"),
        ("Valid MasterCard", "5500000000000004"),
        ("Valid Amex", "378282246310005"),
        ("Invalid", "4532015112830367"),
    ]
    
    print("\nValidation Tests:")
    for name, number in test_numbers:
        result = validate(number)
        status = "✓ Valid" if result else "✗ Invalid"
        print(f"  {name}: {number} -> {status}")
    
    # Generate test numbers
    print("\nGenerated Test Credit Cards:")
    cards = generate_test_credit_cards(3)
    for card_type, number in cards[:10]:
        print(f"  {card_type}: {format_number(number)}")
    
    # Check digit calculation
    print("\nCheck Digit Calculation:")
    partial = "453201511283036"
    check = calculate_check_digit(partial)
    full = add_check_digit(partial)
    print(f"  Partial: {partial}")
    print(f"  Check digit: {check}")
    print(f"  Full number: {full}")
    print(f"  Validation: {validate(full)}")
    
    # Card type identification
    print("\nCard Type Identification:")
    for name, number in test_numbers[:3]:
        card_type = identify_card_type(number)
        print(f"  {number} -> {card_type}")