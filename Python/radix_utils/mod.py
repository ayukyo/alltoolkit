"""
AllToolkit - Python Radix (Base) Conversion Utilities

A zero-dependency, production-ready radix conversion utility module.
Supports conversion between arbitrary bases (2-36), including binary,
octal, decimal, and hexadecimal, with support for fractions and negative numbers.

Author: AllToolkit
License: MIT
"""

from typing import Union, Tuple, Optional


class RadixUtils:
    """
    Radix (base) conversion utilities.
    
    Provides functions for:
    - Converting between arbitrary bases (2-36)
    - Binary, octal, decimal, hexadecimal conversions
    - Fractional number conversion
    - Negative number handling
    - Input validation
    - Common format shortcuts
    """
    
    # Character set for bases up to 36
    DIGITS = '0123456789abcdefghijklmnopqrstuvwxyz'
    DIGIT_MAP = {c: i for i, c in enumerate(DIGITS)}
    
    MIN_BASE = 2
    MAX_BASE = 36
    
    @staticmethod
    def validate_base(base: int) -> None:
        """
        Validate that base is within supported range.
        
        Args:
            base: The base to validate
            
        Raises:
            ValueError: If base is outside valid range
        """
        if not isinstance(base, int):
            raise TypeError(f"Base must be an integer, got {type(base).__name__}")
        if base < RadixUtils.MIN_BASE or base > RadixUtils.MAX_BASE:
            raise ValueError(f"Base must be between {RadixUtils.MIN_BASE} and {RadixUtils.MAX_BASE}, got {base}")
    
    @staticmethod
    def validate_digits(number_str: str, base: int) -> None:
        """
        Validate that all digits in number_str are valid for the given base.
        
        Args:
            number_str: The number string to validate
            base: The base to validate against
            
        Raises:
            ValueError: If any digit is invalid for the base
        """
        RadixUtils.validate_base(base)
        valid_digits = set(RadixUtils.DIGITS[:base] + RadixUtils.DIGITS[:base].upper())
        # Allow negative sign and decimal point
        valid_digits.update(['-', '.'])
        
        for i, char in enumerate(number_str):
            if char not in valid_digits:
                raise ValueError(f"Invalid digit '{char}' for base {base} at position {i}")
    
    @staticmethod
    def to_decimal(number_str: str, from_base: int) -> Union[int, float]:
        """
        Convert a number from any base (2-36) to decimal.
        
        Args:
            number_str: The number string to convert
            from_base: The base of the input number (2-36)
            
        Returns:
            Decimal value as int or float
            
        Raises:
            ValueError: If base is invalid or number has invalid digits
            TypeError: If number_str is not a string
            
        Example:
            >>> RadixUtils.to_decimal("1010", 2)
            10
            >>> RadixUtils.to_decimal("ff", 16)
            255
            >>> RadixUtils.to_decimal("z", 36)
            35
        """
        if not isinstance(number_str, str):
            raise TypeError(f"Input must be a string, got {type(number_str).__name__}")
        
        RadixUtils.validate_base(from_base)
        
        # Handle empty string
        number_str = number_str.strip()
        if not number_str:
            raise ValueError("Input string cannot be empty")
        
        # Handle negative numbers
        negative = False
        if number_str.startswith('-'):
            negative = True
            number_str = number_str[1:]
        
        # Handle sign without digits
        if not number_str or number_str == '.':
            raise ValueError("Invalid number format")
        
        # Split into integer and fractional parts
        if '.' in number_str:
            integer_part, fractional_part = number_str.split('.', 1)
        else:
            integer_part = number_str
            fractional_part = ''
        
        # Validate digits
        all_digits = integer_part + fractional_part
        RadixUtils.validate_digits(('-' if negative else '') + all_digits, from_base)
        
        # Convert integer part
        decimal_int = 0
        for char in integer_part.lower():
            decimal_int = decimal_int * from_base + RadixUtils.DIGIT_MAP[char]
        
        # Convert fractional part
        decimal_frac = 0.0
        if fractional_part:
            multiplier = 1.0 / from_base
            for char in fractional_part.lower():
                decimal_frac += RadixUtils.DIGIT_MAP[char] * multiplier
                multiplier /= from_base
        
        result = decimal_int + decimal_frac
        return -result if negative else result
    
    @staticmethod
    def from_decimal(decimal: Union[int, float], to_base: int, precision: int = 10) -> str:
        """
        Convert a decimal number to any base (2-36).
        
        Args:
            decimal: The decimal number to convert
            to_base: The target base (2-36)
            precision: Maximum fractional digits (default: 10)
            
        Returns:
            Number string in target base
            
        Raises:
            ValueError: If base is invalid or precision is negative
            TypeError: If decimal is not a number
            
        Example:
            >>> RadixUtils.from_decimal(10, 2)
            '1010'
            >>> RadixUtils.from_decimal(255, 16)
            'ff'
            >>> RadixUtils.from_decimal(35, 36)
            'z'
        """
        if not isinstance(decimal, (int, float)):
            raise TypeError(f"Input must be a number, got {type(decimal).__name__}")
        
        RadixUtils.validate_base(to_base)
        
        if precision < 0:
            raise ValueError(f"Precision must be non-negative, got {precision}")
        
        # Handle negative numbers
        negative = decimal < 0
        decimal = abs(decimal)
        
        # Split into integer and fractional parts
        integer_part = int(decimal)
        fractional_part = decimal - integer_part
        
        # Convert integer part
        if integer_part == 0:
            result_int = '0'
        else:
            digits = []
            while integer_part > 0:
                digits.append(RadixUtils.DIGITS[integer_part % to_base])
                integer_part //= to_base
            result_int = ''.join(reversed(digits))
        
        # Convert fractional part
        result_frac = ''
        if fractional_part > 0 and precision > 0:
            frac_digits = []
            count = 0
            while fractional_part > 0 and count < precision:
                fractional_part *= to_base
                digit = int(fractional_part)
                frac_digits.append(RadixUtils.DIGITS[digit])
                fractional_part -= digit
                count += 1
            result_frac = ''.join(frac_digits).rstrip('0')  # Remove trailing zeros
        
        result = result_int
        if result_frac:
            result += '.' + result_frac
        
        return '-' + result if negative else result
    
    @staticmethod
    def convert(number_str: str, from_base: int, to_base: int, precision: int = 10) -> str:
        """
        Convert a number from one base to another.
        
        Args:
            number_str: The number string to convert
            from_base: The source base (2-36)
            to_base: The target base (2-36)
            precision: Maximum fractional digits for the result (default: 10)
            
        Returns:
            Number string in target base
            
        Example:
            >>> RadixUtils.convert("1010", 2, 16)
            'a'
            >>> RadixUtils.convert("ff", 16, 2)
            '11111111'
            >>> RadixUtils.convert("255", 10, 16)
            'ff'
        """
        decimal = RadixUtils.to_decimal(number_str, from_base)
        
        # Use integer output if the result is a whole number
        if isinstance(decimal, float) and decimal == int(decimal):
            decimal = int(decimal)
        
        return RadixUtils.from_decimal(decimal, to_base, precision)
    
    # ==================== Binary (Base 2) Shortcuts ====================
    
    @staticmethod
    def to_binary(number_str: str, from_base: int = 10) -> str:
        """
        Convert a number to binary (base 2).
        
        Args:
            number_str: The number string to convert
            from_base: The source base (default: 10)
            
        Returns:
            Binary string
            
        Example:
            >>> RadixUtils.to_binary("255")
            '11111111'
            >>> RadixUtils.to_binary("ff", 16)
            '11111111'
        """
        return RadixUtils.convert(number_str, from_base, 2)
    
    @staticmethod
    def from_binary(binary_str: str, to_base: int = 10) -> str:
        """
        Convert a binary number to another base.
        
        Args:
            binary_str: The binary string to convert
            to_base: The target base (default: 10)
            
        Returns:
            Number string in target base
            
        Example:
            >>> RadixUtils.from_binary("11111111")
            '255'
            >>> RadixUtils.from_binary("11111111", 16)
            'ff'
        """
        return RadixUtils.convert(binary_str, 2, to_base)
    
    # ==================== Octal (Base 8) Shortcuts ====================
    
    @staticmethod
    def to_octal(number_str: str, from_base: int = 10) -> str:
        """
        Convert a number to octal (base 8).
        
        Args:
            number_str: The number string to convert
            from_base: The source base (default: 10)
            
        Returns:
            Octal string
            
        Example:
            >>> RadixUtils.to_octal("255")
            '377'
            >>> RadixUtils.to_octal("11111111", 2)
            '377'
        """
        return RadixUtils.convert(number_str, from_base, 8)
    
    @staticmethod
    def from_octal(octal_str: str, to_base: int = 10) -> str:
        """
        Convert an octal number to another base.
        
        Args:
            octal_str: The octal string to convert
            to_base: The target base (default: 10)
            
        Returns:
            Number string in target base
            
        Example:
            >>> RadixUtils.from_octal("377")
            '255'
            >>> RadixUtils.from_octal("377", 16)
            'ff'
        """
        return RadixUtils.convert(octal_str, 8, to_base)
    
    # ==================== Hexadecimal (Base 16) Shortcuts ====================
    
    @staticmethod
    def to_hex(number_str: str, from_base: int = 10, uppercase: bool = False) -> str:
        """
        Convert a number to hexadecimal (base 16).
        
        Args:
            number_str: The number string to convert
            from_base: The source base (default: 10)
            uppercase: Whether to use uppercase letters (default: False)
            
        Returns:
            Hexadecimal string
            
        Example:
            >>> RadixUtils.to_hex("255")
            'ff'
            >>> RadixUtils.to_hex("11111111", 2)
            'ff'
            >>> RadixUtils.to_hex("255", uppercase=True)
            'FF'
        """
        result = RadixUtils.convert(number_str, from_base, 16)
        return result.upper() if uppercase else result
    
    @staticmethod
    def from_hex(hex_str: str, to_base: int = 10) -> str:
        """
        Convert a hexadecimal number to another base.
        
        Args:
            hex_str: The hexadecimal string to convert
            to_base: The target base (default: 10)
            
        Returns:
            Number string in target base
            
        Example:
            >>> RadixUtils.from_hex("ff")
            '255'
            >>> RadixUtils.from_hex("FF")
            '255'
            >>> RadixUtils.from_hex("ff", 2)
            '11111111'
        """
        return RadixUtils.convert(hex_str, 16, to_base)
    
    # ==================== Base 36 Shortcuts ====================
    
    @staticmethod
    def to_base36(number_str: str, from_base: int = 10) -> str:
        """
        Convert a number to base 36.
        
        Args:
            number_str: The number string to convert
            from_base: The source base (default: 10)
            
        Returns:
            Base 36 string
            
        Example:
            >>> RadixUtils.to_base36("12345")
            '9ix'
        """
        return RadixUtils.convert(number_str, from_base, 36)
    
    @staticmethod
    def from_base36(base36_str: str, to_base: int = 10) -> str:
        """
        Convert a base 36 number to another base.
        
        Args:
            base36_str: The base 36 string to convert
            to_base: The target base (default: 10)
            
        Returns:
            Number string in target base
            
        Example:
            >>> RadixUtils.from_base36("9ix")
            '12345'
        """
        return RadixUtils.convert(base36_str, 36, to_base)
    
    # ==================== Batch Conversion ====================
    
    @staticmethod
    def convert_all_bases(number_str: str, from_base: int, precision: int = 10) -> dict:
        """
        Convert a number to all common bases at once.
        
        Args:
            number_str: The number string to convert
            from_base: The source base
            precision: Maximum fractional digits (default: 10)
            
        Returns:
            Dictionary with binary, octal, decimal, hexadecimal, and base36 results
            
        Example:
            >>> RadixUtils.convert_all_bases("255", 10)
            {'binary': '11111111', 'octal': '377', 'decimal': '255', 'hexadecimal': 'ff', 'base36': '73'}
        """
        return {
            'binary': RadixUtils.convert(number_str, from_base, 2, precision),
            'octal': RadixUtils.convert(number_str, from_base, 8, precision),
            'decimal': RadixUtils.convert(number_str, from_base, 10, precision),
            'hexadecimal': RadixUtils.convert(number_str, from_base, 16, precision),
            'base36': RadixUtils.convert(number_str, from_base, 36, precision),
        }
    
    # ==================== Bit Operations ====================
    
    @staticmethod
    def count_bits(number_str: str, from_base: int = 10) -> int:
        """
        Count the number of bits required to represent a number.
        
        Args:
            number_str: The number string
            from_base: The source base (default: 10)
            
        Returns:
            Number of bits required
            
        Example:
            >>> RadixUtils.count_bits("255")
            8
            >>> RadixUtils.count_bits("256")
            9
        """
        decimal = RadixUtils.to_decimal(number_str, from_base)
        # Convert to int if it's a float
        if isinstance(decimal, float):
            if not decimal.is_integer():
                raise ValueError("Bit operations are only supported for integers")
            decimal = int(decimal)
        
        if decimal < 0:
            decimal = abs(decimal)
            # Account for sign bit
            return decimal.bit_length() + 1 if decimal > 0 else 2
        return max(1, decimal.bit_length()) if decimal > 0 else 1
    
    @staticmethod
    def get_bit(number_str: str, from_base: int, bit_index: int) -> int:
        """
        Get the value of a specific bit in a number.
        
        Args:
            number_str: The number string
            from_base: The source base
            bit_index: The bit index (0 = least significant bit)
            
        Returns:
            0 or 1
            
        Example:
            >>> RadixUtils.get_bit("10", 10, 1)
            1
            >>> RadixUtils.get_bit("10", 10, 0)
            0
        """
        decimal = RadixUtils.to_decimal(number_str, from_base)
        if isinstance(decimal, float):
            if not decimal.is_integer():
                raise ValueError("Bit operations are only supported for integers")
            decimal = int(decimal)
        
        return 1 if (decimal >> bit_index) & 1 else 0
    
    @staticmethod
    def set_bit(number_str: str, from_base: int, bit_index: int, to_base: int = 10) -> str:
        """
        Set a specific bit in a number.
        
        Args:
            number_str: The number string
            from_base: The source base
            bit_index: The bit index to set (0 = least significant bit)
            to_base: The output base (default: 10)
            
        Returns:
            Number string with bit set
            
        Example:
            >>> RadixUtils.set_bit("10", 10, 0)
            '11'
        """
        decimal = RadixUtils.to_decimal(number_str, from_base)
        if isinstance(decimal, float):
            if not decimal.is_integer():
                raise ValueError("Bit operations are only supported for integers")
            decimal = int(decimal)
        
        result = decimal | (1 << bit_index)
        return RadixUtils.from_decimal(result, to_base)
    
    @staticmethod
    def clear_bit(number_str: str, from_base: int, bit_index: int, to_base: int = 10) -> str:
        """
        Clear a specific bit in a number.
        
        Args:
            number_str: The number string
            from_base: The source base
            bit_index: The bit index to clear (0 = least significant bit)
            to_base: The output base (default: 10)
            
        Returns:
            Number string with bit cleared
            
        Example:
            >>> RadixUtils.clear_bit("11", 10, 0)
            '10'
        """
        decimal = RadixUtils.to_decimal(number_str, from_base)
        if isinstance(decimal, float):
            if not decimal.is_integer():
                raise ValueError("Bit operations are only supported for integers")
            decimal = int(decimal)
        
        result = decimal & ~(1 << bit_index)
        return RadixUtils.from_decimal(result, to_base)
    
    # ==================== Validation Utilities ====================
    
    @staticmethod
    def is_valid(number_str: str, base: int) -> bool:
        """
        Check if a number string is valid for a given base.
        
        Args:
            number_str: The number string to validate
            base: The base to validate against
            
        Returns:
            True if valid, False otherwise
            
        Example:
            >>> RadixUtils.is_valid("1010", 2)
            True
            >>> RadixUtils.is_valid("1020", 2)
            False
        """
        try:
            RadixUtils.validate_digits(number_str, base)
            return True
        except (ValueError, TypeError):
            return False
    
    @staticmethod
    def detect_base(number_str: str) -> Optional[int]:
        """
        Try to detect the base of a number string from common prefixes.
        
        Args:
            number_str: The number string to analyze
            
        Returns:
            Detected base, or None if unable to detect
            
        Example:
            >>> RadixUtils.detect_base("0b1010")
            2
            >>> RadixUtils.detect_base("0o755")
            8
            >>> RadixUtils.detect_base("0xff")
            16
        """
        number_str = number_str.strip().lower()
        
        # Check for common prefixes
        if number_str.startswith('0b'):
            return 2
        if number_str.startswith('0o'):
            return 8
        if number_str.startswith('0x'):
            return 16
        
        # Try to infer from characters
        has_letters = any(c.isalpha() for c in number_str if c not in ['-', '.'])
        if has_letters:
            max_char = max(c for c in number_str.lower() if c.isalpha())
            return ord(max_char) - ord('a') + 11
        
        # If only digits and <= 7, might be octal
        if all(c in '01234567' for c in number_str if c not in ['-', '.']):
            return 8  # Could also be decimal
        
        # Default assumption
        return 10
    
    @staticmethod
    def strip_prefix(number_str: str) -> Tuple[str, Optional[int]]:
        """
        Strip common base prefixes (0b, 0o, 0x) from a number string.
        
        Args:
            number_str: The number string to process
            
        Returns:
            Tuple of (stripped_string, detected_base or None)
            
        Example:
            >>> RadixUtils.strip_prefix("0xff")
            ('ff', 16)
            >>> RadixUtils.strip_prefix("255")
            ('255', None)
        """
        number_str = number_str.strip()
        negative = number_str.startswith('-')
        if negative:
            number_str = number_str[1:]
        
        base = None
        if number_str.lower().startswith('0b'):
            number_str = number_str[2:]
            base = 2
        elif number_str.lower().startswith('0o'):
            number_str = number_str[2:]
            base = 8
        elif number_str.lower().startswith('0x'):
            number_str = number_str[2:]
            base = 16
        
        result = '-' + number_str if negative else number_str
        return result, base


# ==================== Convenience Functions ====================

def to_decimal(number_str: str, from_base: int) -> Union[int, float]:
    """Convert a number from any base to decimal."""
    return RadixUtils.to_decimal(number_str, from_base)


def from_decimal(decimal: Union[int, float], to_base: int, precision: int = 10) -> str:
    """Convert a decimal number to any base."""
    return RadixUtils.from_decimal(decimal, to_base, precision)


def convert(number_str: str, from_base: int, to_base: int, precision: int = 10) -> str:
    """Convert a number from one base to another."""
    return RadixUtils.convert(number_str, from_base, to_base, precision)


def to_binary(number_str: str, from_base: int = 10) -> str:
    """Convert a number to binary."""
    return RadixUtils.to_binary(number_str, from_base)


def from_binary(binary_str: str, to_base: int = 10) -> str:
    """Convert a binary number to another base."""
    return RadixUtils.from_binary(binary_str, to_base)


def to_octal(number_str: str, from_base: int = 10) -> str:
    """Convert a number to octal."""
    return RadixUtils.to_octal(number_str, from_base)


def from_octal(octal_str: str, to_base: int = 10) -> str:
    """Convert an octal number to another base."""
    return RadixUtils.from_octal(octal_str, to_base)


def to_hex(number_str: str, from_base: int = 10, uppercase: bool = False) -> str:
    """Convert a number to hexadecimal."""
    return RadixUtils.to_hex(number_str, from_base, uppercase)


def from_hex(hex_str: str, to_base: int = 10) -> str:
    """Convert a hexadecimal number to another base."""
    return RadixUtils.from_hex(hex_str, to_base)


def to_base36(number_str: str, from_base: int = 10) -> str:
    """Convert a number to base 36."""
    return RadixUtils.to_base36(number_str, from_base)


def from_base36(base36_str: str, to_base: int = 10) -> str:
    """Convert a base 36 number to another base."""
    return RadixUtils.from_base36(base36_str, to_base)


def convert_all_bases(number_str: str, from_base: int, precision: int = 10) -> dict:
    """Convert a number to all common bases at once."""
    return RadixUtils.convert_all_bases(number_str, from_base, precision)


def is_valid(number_str: str, base: int) -> bool:
    """Check if a number string is valid for a given base."""
    return RadixUtils.is_valid(number_str, base)


def detect_base(number_str: str) -> Optional[int]:
    """Detect the base of a number string from common prefixes."""
    return RadixUtils.detect_base(number_str)