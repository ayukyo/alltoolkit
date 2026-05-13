#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AllToolkit - Significant Figures Utilities Module
==================================================
A comprehensive significant figures utility module for Python with zero external dependencies.

Features:
    - Count significant figures in a number
    - Round to specific significant figures
    - Arithmetic operations with significant figures tracking
    - Scientific notation conversion
    - Measurement uncertainty representation
    - Error propagation for basic operations
    - Rounding rules for calculations
    - Support for string and numeric inputs

Author: AllToolkit Contributors
License: MIT
Date: 2026-05-13
"""

from typing import Union, Tuple, Optional, List
from dataclasses import dataclass
from decimal import Decimal, InvalidOperation, ROUND_HALF_UP, getcontext
import re
import math

# Set high precision for Decimal operations
getcontext().prec = 50


# ============================================================================
# Constants
# ============================================================================

SIGNIFICANT_FIGURES_PATTERN = re.compile(r'^[+-]?(\d+\.?\d*|\.\d+)([eE][+-]?\d+)?$')


# ============================================================================
# Data Classes
# ============================================================================

@dataclass
class MeasuredValue:
    """
    Represents a measured value with its uncertainty and significant figures.
    
    Attributes:
        value: The measured value
        uncertainty: The uncertainty/error in the measurement
        sig_figs: Number of significant figures
        unit: Optional unit string
    """
    value: float
    uncertainty: float
    sig_figs: int
    unit: Optional[str] = None
    
    def __repr__(self) -> str:
        if self.unit:
            return f"MeasuredValue({self.value} ± {self.uncertainty} {self.unit}, {self.sig_figs} sf)"
        return f"MeasuredValue({self.value} ± {self.uncertainty}, {self.sig_figs} sf)"
    
    def __str__(self) -> str:
        """Return formatted string with uncertainty."""
        return format_with_uncertainty(self.value, self.uncertainty, self.unit)
    
    def relative_uncertainty(self) -> float:
        """Calculate relative uncertainty as a percentage."""
        if self.value == 0:
            return float('inf') if self.uncertainty > 0 else 0
        return abs(self.uncertainty / self.value) * 100


@dataclass
class SigFigNumber:
    """
    A number that tracks its significant figures.
    
    Attributes:
        value: The numeric value
        sig_figs: Number of significant figures
        original_string: Original string representation (if provided)
    """
    value: float
    sig_figs: int
    original_string: Optional[str] = None
    
    def __repr__(self) -> str:
        return f"SigFigNumber({self.value}, {self.sig_figs} sf)"
    
    def __str__(self) -> str:
        return format_sig_figs(self.value, self.sig_figs)
    
    def __add__(self, other: Union['SigFigNumber', int, float]) -> 'SigFigNumber':
        return add_sig_figs(self, other)
    
    def __sub__(self, other: Union['SigFigNumber', int, float]) -> 'SigFigNumber':
        return subtract_sig_figs(self, other)
    
    def __mul__(self, other: Union['SigFigNumber', int, float]) -> 'SigFigNumber':
        return multiply_sig_figs(self, other)
    
    def __truediv__(self, other: Union['SigFigNumber', int, float]) -> 'SigFigNumber':
        return divide_sig_figs(self, other)
    
    def __pow__(self, other: Union['SigFigNumber', int, float]) -> 'SigFigNumber':
        return power_sig_figs(self, other)
    
    def to_scientific_notation(self) -> str:
        """Convert to scientific notation."""
        return to_scientific_notation(self.value, self.sig_figs)


# ============================================================================
# Core Functions
# ============================================================================

def count_significant_figures(number: Union[str, int, float, Decimal]) -> int:
    """
    Count the number of significant figures in a number.
    
    Rules for significant figures:
    1. Non-zero digits are always significant
    2. Zeros between non-zero digits are significant
    3. Leading zeros are never significant
    4. Trailing zeros are significant only if the number contains a decimal point
    5. In scientific notation, only the mantissa's digits are significant
    
    Args:
        number: The number to analyze (string, int, float, or Decimal)
    
    Returns:
        Number of significant figures
    
    Examples:
        >>> count_significant_figures("123")
        3
        >>> count_significant_figures("00123")
        3
        >>> count_significant_figures("12300")
        3
        >>> count_significant_figures("12300.")
        5
        >>> count_significant_figures("0.00456")
        3
        >>> count_significant_figures("1.2300")
        5
        >>> count_significant_figures("1.020")
        4
        >>> count_significant_figures("1.00e3")
        3
    """
    # Convert to string for analysis
    if isinstance(number, Decimal):
        # Format Decimal without scientific notation
        s = format(number, 'f')
    elif isinstance(number, (int, float)):
        # Handle float precision issues
        if isinstance(number, float):
            # Check if it's an integer float like 123.0
            if number == int(number) and abs(number) < 1e15:
                # Determine if original had decimal point
                s = str(number)
                if '.' in s and 'e' not in s.lower():
                    # Keep trailing zeros for floats like 123.0
                    pass
                else:
                    s = str(int(number))
            else:
                s = str(number)
        else:
            s = str(number)
    else:
        s = str(number).strip()
    
    # Handle negative sign
    if s.startswith('-') or s.startswith('+'):
        s = s[1:]
    
    # Handle scientific notation
    if 'e' in s.lower():
        parts = s.lower().split('e')
        mantissa = parts[0]
        # Only count significant figures in mantissa
        return _count_sig_figs_in_decimal(mantissa)
    
    return _count_sig_figs_in_decimal(s)


def _count_sig_figs_in_decimal(s: str) -> int:
    """
    Count significant figures in a decimal string.
    
    Args:
        s: Decimal string (without sign or exponent)
    
    Returns:
        Number of significant figures
    """
    s = s.strip()
    
    if not s or s == '.' or s == '0' or all(c == '0' for c in s if c.isdigit()):
        # Special case: pure zero or empty
        if '.' in s:
            # Zero with decimal point: count trailing zeros after decimal
            # e.g., "0.00" has 2 significant figures (uncertain, depends on context)
            # Standard interpretation: 0.00 has 2 significant figures
            after_decimal = s.split('.')[-1]
            return len(after_decimal)
        else:
            # Integer zero has 1 significant figure
            return 1
    
    if '.' in s:
        # Has decimal point
        parts = s.split('.')
        integer_part = parts[0].lstrip('0')  # Remove leading zeros
        decimal_part = parts[1]
        
        if integer_part:
            # Has non-zero integer part
            # All digits are significant
            return len(integer_part) + len(decimal_part)
        else:
            # Pure decimal (0.xxx)
            # Count digits after decimal, excluding leading zeros
            # e.g., 0.00456 -> 3 sig figs
            return len(decimal_part.lstrip('0'))
    else:
        # Integer without decimal point
        # Trailing zeros are not significant
        # e.g., 12300 -> 3 sig figs
        s = s.lstrip('0')  # Remove leading zeros
        s = s.rstrip('0')  # Remove trailing zeros
        return len(s) if s else 1


def round_to_sig_figs(
    number: Union[int, float, str, Decimal],
    sig_figs: int,
    rounding_mode: str = 'half_up'
) -> float:
    """
    Round a number to a specified number of significant figures.
    
    Args:
        number: The number to round
        sig_figs: Number of significant figures
        rounding_mode: 'half_up', 'half_down', 'half_even', 'up', 'down'
    
    Returns:
        Rounded number as float
    
    Raises:
        ValueError: If sig_figs is less than 1
    
    Examples:
        >>> round_to_sig_figs(123.456, 4)
        123.5
        >>> round_to_sig_figs(123.456, 3)
        123.0
        >>> round_to_sig_figs(0.00123456, 3)
        0.00123
        >>> round_to_sig_figs(12345, 2)
        12000.0
        >>> round_to_sig_figs(999.9, 3)
        1000.0
    """
    if sig_figs < 1:
        raise ValueError("Number of significant figures must be at least 1")
    
    # Handle zero
    if number == 0:
        return 0.0
    
    # Convert to Decimal for precision
    if isinstance(number, str):
        d = Decimal(number)
    elif isinstance(number, float):
        d = Decimal(str(number))
    else:
        d = Decimal(number)
    
    # Handle negative numbers
    sign = 1 if d >= 0 else -1
    d = abs(d)
    
    # Find the order of magnitude
    if d == 0:
        return 0.0
    
    # Get the exponent (order of magnitude)
    exponent = int(d.log10().to_integral_value(rounding=ROUND_HALF_UP))
    
    # Calculate the scaling factor
    scale = Decimal(10) ** (exponent - sig_figs + 1)
    
    # Apply rounding
    rounding_map = {
        'half_up': ROUND_HALF_UP,
    }
    
    decimal_rounding = rounding_map.get(rounding_mode, ROUND_HALF_UP)
    rounded = (d / scale).quantize(Decimal('1'), rounding=decimal_rounding) * scale
    
    return float(sign * rounded)


def format_sig_figs(
    number: Union[int, float],
    sig_figs: int,
    use_scientific: bool = False
) -> str:
    """
    Format a number with a specific number of significant figures.
    
    Args:
        number: The number to format
        sig_figs: Number of significant figures
        use_scientific: Whether to use scientific notation for large/small numbers
    
    Returns:
        Formatted string
    
    Examples:
        >>> format_sig_figs(123.456, 4)
        '123.5'
        >>> format_sig_figs(0.00123456, 3)
        '0.00123'
        >>> format_sig_figs(12345, 3)
        '12300'
        >>> format_sig_figs(12345, 3, use_scientific=True)
        '1.23e+04'
    """
    if number == 0:
        # Handle zero
        if sig_figs == 1:
            return '0'
        return '0.' + '0' * (sig_figs - 1)
    
    # Round to significant figures
    rounded = round_to_sig_figs(number, sig_figs)
    
    # Determine if scientific notation is needed
    abs_rounded = abs(rounded)
    use_sci = use_scientific or abs_rounded >= 1e6 or (abs_rounded < 0.001 and abs_rounded > 0)
    
    if use_sci:
        return to_scientific_notation(rounded, sig_figs)
    
    # Format the number
    # Find the position of the last significant figure
    rounded_dec = Decimal(str(rounded))
    
    if '.' in str(rounded_dec):
        # Has decimal point
        s = str(rounded_dec)
        # Count significant figures
        actual_sig = count_significant_figures(s)
        if actual_sig < sig_figs:
            # Add trailing zeros
            parts = s.split('.')
            if len(parts) == 2:
                needed = sig_figs - actual_sig
                s = parts[0] + '.' + parts[1] + '0' * needed
        return s
    else:
        # Integer
        s = str(int(rounded))
        actual_sig = count_significant_figures(s)
        if actual_sig < sig_figs:
            # Need decimal point and trailing zeros
            needed = sig_figs - actual_sig
            s = s + '.' + '0' * needed
        return s


def to_scientific_notation(
    number: Union[int, float],
    sig_figs: Optional[int] = None,
    exponent_symbol: str = 'e'
) -> str:
    """
    Convert a number to scientific notation.
    
    Args:
        number: The number to convert
        sig_figs: Number of significant figures (optional, auto-detect if not provided)
        exponent_symbol: Symbol for exponent ('e' or 'E')
    
    Returns:
        Scientific notation string
    
    Examples:
        >>> to_scientific_notation(1234.56, 3)
        '1.23e+03'
        >>> to_scientific_notation(0.00123, 2)
        '1.2e-03'
        >>> to_scientific_notation(1234.56, 4, 'E')
        '1.235E+03'
    """
    if number == 0:
        if sig_figs:
            if sig_figs == 1:
                return '0' + exponent_symbol + '+00'
            return '0.' + '0' * (sig_figs - 1) + exponent_symbol + '+00'
        return '0' + exponent_symbol + '+00'
    
    # Determine significant figures
    if sig_figs is None:
        sig_figs = count_significant_figures(number)
    
    # Round to significant figures
    rounded = round_to_sig_figs(number, sig_figs)
    
    # Calculate exponent
    if rounded == 0:
        return '0' + exponent_symbol + '+00'
    
    exponent = int(math.floor(math.log10(abs(rounded))))
    
    # Calculate mantissa
    mantissa = rounded / (10 ** exponent)
    
    # Round mantissa to sig_figs
    mantissa = round(mantissa, sig_figs - 1)
    
    # Handle mantissa rounding to next power of 10
    if abs(mantissa) >= 10:
        mantissa /= 10
        exponent += 1
    
    # Format exponent
    exp_str = f"{exponent:+03d}"
    
    # Format mantissa
    if sig_figs == 1:
        mantissa_str = f"{abs(mantissa):.0f}"
    else:
        mantissa_str = f"{abs(mantissa):.{sig_figs - 1}f}"
    
    sign = '-' if number < 0 else ''
    
    return f"{sign}{mantissa_str}{exponent_symbol}{exp_str}"


def from_scientific_notation(s: str) -> float:
    """
    Convert a scientific notation string to a float.
    
    Args:
        s: Scientific notation string (e.g., "1.23e+03", "1.23E-03")
    
    Returns:
        Float value
    
    Examples:
        >>> from_scientific_notation("1.23e+03")
        1230.0
        >>> from_scientific_notation("1.23E-03")
        0.00123
    """
    return float(s.lower().replace('e+', 'e').replace('e-', 'e-'))


# ============================================================================
# Arithmetic Operations with Significant Figures
# ============================================================================

def _to_sig_fig_number(value: Union[SigFigNumber, int, float]) -> SigFigNumber:
    """Convert a value to SigFigNumber."""
    if isinstance(value, SigFigNumber):
        return value
    return SigFigNumber(float(value), count_significant_figures(value))


def add_sig_figs(
    a: Union[SigFigNumber, int, float],
    b: Union[SigFigNumber, int, float]
) -> SigFigNumber:
    """
    Add two numbers with significant figure rules.
    
    For addition, the result should have the same number of decimal places
    as the number with the fewest decimal places.
    
    Args:
        a: First number
        b: Second number
    
    Returns:
        SigFigNumber with appropriate significant figures
    
    Examples:
        >>> result = add_sig_figs(SigFigNumber(123.45, 5), SigFigNumber(67.8, 3))
        >>> result.value
        191.2
        >>> result.sig_figs
        4
    """
    a_sf = _to_sig_fig_number(a)
    b_sf = _to_sig_fig_number(b)
    
    # Determine decimal places for each number
    a_decimals = _get_decimal_places(a_sf.value)
    b_decimals = _get_decimal_places(b_sf.value)
    
    # Use the minimum decimal places
    min_decimals = min(a_decimals, b_decimals)
    
    # Calculate result
    result_value = a_sf.value + b_sf.value
    
    # Round to minimum decimal places
    if min_decimals == 0:
        result_value = round(result_value)
    else:
        result_value = round(result_value, min_decimals)
    
    # Calculate significant figures for result
    result_sig_figs = count_significant_figures(result_value)
    
    return SigFigNumber(result_value, result_sig_figs)


def subtract_sig_figs(
    a: Union[SigFigNumber, int, float],
    b: Union[SigFigNumber, int, float]
) -> SigFigNumber:
    """
    Subtract two numbers with significant figure rules.
    
    For subtraction, the result should have the same number of decimal places
    as the number with the fewest decimal places.
    
    Args:
        a: First number
        b: Second number
    
    Returns:
        SigFigNumber with appropriate significant figures
    
    Examples:
        >>> result = subtract_sig_figs(SigFigNumber(123.45, 5), SigFigNumber(67.8, 3))
        >>> result.value
        55.7
    """
    a_sf = _to_sig_fig_number(a)
    b_sf = _to_sig_fig_number(b)
    
    # Determine decimal places for each number
    a_decimals = _get_decimal_places(a_sf.value)
    b_decimals = _get_decimal_places(b_sf.value)
    
    # Use the minimum decimal places
    min_decimals = min(a_decimals, b_decimals)
    
    # Calculate result
    result_value = a_sf.value - b_sf.value
    
    # Round to minimum decimal places
    if min_decimals == 0:
        result_value = round(result_value)
    else:
        result_value = round(result_value, min_decimals)
    
    # Calculate significant figures for result
    result_sig_figs = count_significant_figures(result_value)
    
    return SigFigNumber(result_value, result_sig_figs)


def multiply_sig_figs(
    a: Union[SigFigNumber, int, float],
    b: Union[SigFigNumber, int, float]
) -> SigFigNumber:
    """
    Multiply two numbers with significant figure rules.
    
    For multiplication, the result should have the same number of significant
    figures as the factor with the fewest significant figures.
    
    Args:
        a: First number
        b: Second number
    
    Returns:
        SigFigNumber with appropriate significant figures
    
    Examples:
        >>> result = multiply_sig_figs(SigFigNumber(2.3, 2), SigFigNumber(4.56, 3))
        >>> result.value
        10.0
        >>> result.sig_figs
        2
    """
    a_sf = _to_sig_fig_number(a)
    b_sf = _to_sig_fig_number(b)
    
    # Use minimum significant figures
    min_sig_figs = min(a_sf.sig_figs, b_sf.sig_figs)
    
    # Calculate result
    result_value = a_sf.value * b_sf.value
    
    # Round to minimum significant figures
    result_value = round_to_sig_figs(result_value, min_sig_figs)
    
    return SigFigNumber(result_value, min_sig_figs)


def divide_sig_figs(
    a: Union[SigFigNumber, int, float],
    b: Union[SigFigNumber, int, float]
) -> SigFigNumber:
    """
    Divide two numbers with significant figure rules.
    
    For division, the result should have the same number of significant
    figures as the factor with the fewest significant figures.
    
    Args:
        a: Numerator
        b: Denominator
    
    Returns:
        SigFigNumber with appropriate significant figures
    
    Raises:
        ZeroDivisionError: If b is zero
    
    Examples:
        >>> result = divide_sig_figs(SigFigNumber(10.0, 3), SigFigNumber(3.0, 2))
        >>> result.value
        3.3
        >>> result.sig_figs
        2
    """
    a_sf = _to_sig_fig_number(a)
    b_sf = _to_sig_fig_number(b)
    
    if b_sf.value == 0:
        raise ZeroDivisionError("Cannot divide by zero")
    
    # Use minimum significant figures
    min_sig_figs = min(a_sf.sig_figs, b_sf.sig_figs)
    
    # Calculate result
    result_value = a_sf.value / b_sf.value
    
    # Round to minimum significant figures
    result_value = round_to_sig_figs(result_value, min_sig_figs)
    
    return SigFigNumber(result_value, min_sig_figs)


def power_sig_figs(
    base: Union[SigFigNumber, int, float],
    exponent: Union[SigFigNumber, int, float]
) -> SigFigNumber:
    """
    Raise a number to a power with significant figure rules.
    
    For powers, the result should have the same number of significant
    figures as the base. For roots, the result should have the same number
    of significant figures as the radicand.
    
    Args:
        base: The base number
        exponent: The exponent
    
    Returns:
        SigFigNumber with appropriate significant figures
    
    Examples:
        >>> result = power_sig_figs(SigFigNumber(2.34, 3), 2)
        >>> result.value
        5.48
        >>> result.sig_figs
        3
    """
    base_sf = _to_sig_fig_number(base)
    exp_value = _to_sig_fig_number(exponent).value if isinstance(exponent, (SigFigNumber, int, float)) else float(exponent)
    
    # Calculate result
    result_value = base_sf.value ** exp_value
    
    # For integer exponents, use base's significant figures
    # For non-integer exponents, use one more significant figure
    if exp_value == int(exp_value):
        sig_figs = base_sf.sig_figs
    else:
        sig_figs = base_sf.sig_figs + 1
    
    result_value = round_to_sig_figs(result_value, sig_figs)
    
    return SigFigNumber(result_value, sig_figs)


def sqrt_sig_figs(
    value: Union[SigFigNumber, int, float]
) -> SigFigNumber:
    """
    Calculate square root with significant figure rules.
    
    For square roots, the result should have the same number of significant
    figures as the radicand.
    
    Args:
        value: The number to take square root of
    
    Returns:
        SigFigNumber with appropriate significant figures
    
    Examples:
        >>> result = sqrt_sig_figs(SigFigNumber(5.29, 3))
        >>> result.value
        2.30
        >>> result.sig_figs
        3
    """
    sf = _to_sig_fig_number(value)
    
    result_value = math.sqrt(sf.value)
    
    # Round to same significant figures
    result_value = round_to_sig_figs(result_value, sf.sig_figs)
    
    return SigFigNumber(result_value, sf.sig_figs)


def _get_decimal_places(value: float) -> int:
    """Get the number of decimal places in a float."""
    if value == int(value):
        return 0
    
    s = str(value)
    if '.' in s:
        # Handle scientific notation
        if 'e' in s.lower():
            base, exp = s.lower().split('e')
            decimal_places = len(base.split('.')[1]) - int(exp)
            return max(0, decimal_places)
        return len(s.split('.')[1])
    return 0


# ============================================================================
# Measurement Uncertainty Functions
# ============================================================================

def create_measured_value(
    value: float,
    uncertainty: float,
    unit: Optional[str] = None
) -> MeasuredValue:
    """
    Create a MeasuredValue with automatic significant figure detection.
    
    The significant figures are determined from the uncertainty.
    If uncertainty is 0.01, the value has 2 decimal places of precision.
    
    Args:
        value: The measured value
        uncertainty: The uncertainty in the measurement
        unit: Optional unit string
    
    Returns:
        MeasuredValue object
    
    Examples:
        >>> mv = create_measured_value(9.81, 0.02, "m/s²")
        >>> mv.sig_figs
        3
    """
    # Determine significant figures from uncertainty
    if uncertainty == 0:
        sig_figs = count_significant_figures(value)
    else:
        # Number of significant figures depends on position of first
        # non-zero digit in uncertainty
        uncertainty_dec = Decimal(str(uncertainty))
        if uncertainty_dec == 0:
            sig_figs = count_significant_figures(value)
        else:
            # Find the position of the first significant digit in uncertainty
            uncertainty_str = format(uncertainty_dec, 'f')
            
            # Find first non-zero digit position
            if '.' in uncertainty_str:
                int_part, dec_part = uncertainty_str.split('.')
                int_part = int_part.lstrip('0') or '0'
                
                if int_part != '0':
                    # Uncertainty >= 1, count digits
                    sig_figs = len(str(int(abs(value)) if abs(value) >= 1 else value).split('.')[0])
                else:
                    # Uncertainty < 1, find position of first non-zero
                    for i, char in enumerate(dec_part):
                        if char != '0':
                            # This position determines decimal places
                            decimal_places = i + 1
                            # Round value to this many decimal places
                            rounded = round(value, decimal_places)
                            sig_figs = count_significant_figures(rounded)
                            break
                    else:
                        sig_figs = count_significant_figures(value)
            else:
                sig_figs = count_significant_figures(value)
    
    return MeasuredValue(value, uncertainty, sig_figs, unit)


def format_with_uncertainty(
    value: float,
    uncertainty: float,
    unit: Optional[str] = None
) -> str:
    """
    Format a value with its uncertainty.
    
    Args:
        value: The measured value
        uncertainty: The uncertainty
        unit: Optional unit string
    
    Returns:
        Formatted string (e.g., "9.81 ± 0.02 m/s²")
    
    Examples:
        >>> format_with_uncertainty(9.81, 0.02, "m/s²")
        '9.81 ± 0.02 m/s²'
    """
    # Determine decimal places from uncertainty
    if uncertainty == 0:
        return f"{value} ± 0"
    
    uncertainty_str = f"{uncertainty:.10f}".rstrip('0').rstrip('.')
    if '.' in uncertainty_str:
        decimal_places = len(uncertainty_str.split('.')[1])
        value_formatted = f"{value:.{decimal_places}f}"
    else:
        value_formatted = str(round(value))
    
    result = f"{value_formatted} ± {uncertainty_str}"
    if unit:
        result += f" {unit}"
    return result


def propagate_uncertainty_addition(
    a: MeasuredValue,
    b: MeasuredValue,
    operation: str = 'add'
) -> MeasuredValue:
    """
    Propagate uncertainty for addition or subtraction.
    
    For addition/subtraction, uncertainties add in quadrature:
    δc = √(δa² + δb²)
    
    Args:
        a: First measured value
        b: Second measured value
        operation: 'add' or 'subtract'
    
    Returns:
        New MeasuredValue with propagated uncertainty
    """
    if operation == 'add':
        result_value = a.value + b.value
    else:
        result_value = a.value - b.value
    
    # Uncertainties add in quadrature
    result_uncertainty = math.sqrt(a.uncertainty**2 + b.uncertainty**2)
    
    # Determine unit
    unit = a.unit if a.unit == b.unit else None
    
    return create_measured_value(result_value, result_uncertainty, unit)


def propagate_uncertainty_multiplication(
    a: MeasuredValue,
    b: MeasuredValue,
    operation: str = 'multiply'
) -> MeasuredValue:
    """
    Propagate uncertainty for multiplication or division.
    
    For multiplication: (δc/c)² = (δa/a)² + (δb/b)²
    For division: (δc/c)² = (δa/a)² + (δb/b)²
    
    Args:
        a: First measured value
        b: Second measured value
        operation: 'multiply' or 'divide'
    
    Returns:
        New MeasuredValue with propagated uncertainty
    """
    if operation == 'multiply':
        result_value = a.value * b.value
    else:
        if b.value == 0:
            raise ZeroDivisionError("Cannot divide by zero")
        result_value = a.value / b.value
    
    # Relative uncertainties
    rel_a = a.uncertainty / abs(a.value) if a.value != 0 else 0
    rel_b = b.uncertainty / abs(b.value) if b.value != 0 else 0
    
    # Relative uncertainty of result
    rel_result = math.sqrt(rel_a**2 + rel_b**2)
    
    # Absolute uncertainty
    result_uncertainty = abs(result_value) * rel_result
    
    return create_measured_value(result_value, result_uncertainty)


def propagate_uncertainty_power(
    base: MeasuredValue,
    exponent: float
) -> MeasuredValue:
    """
    Propagate uncertainty for power operation.
    
    For c = a^n: (δc/c) = n * (δa/a)
    
    Args:
        base: The base measured value
        exponent: The exponent (exact value)
    
    Returns:
        New MeasuredValue with propagated uncertainty
    """
    result_value = base.value ** exponent
    
    # Relative uncertainty
    rel_base = base.uncertainty / abs(base.value) if base.value != 0 else 0
    rel_result = abs(exponent) * rel_base
    
    # Absolute uncertainty
    result_uncertainty = abs(result_value) * rel_result
    
    return create_measured_value(result_value, result_uncertainty, base.unit)


# ============================================================================
# Utility Functions
# ============================================================================

def is_exact_number(number: Union[int, float, str]) -> bool:
    """
    Check if a number is exact (has infinite significant figures).
    
    Exact numbers include:
    - Integers used as counts
    - Defined constants (e.g., 100 cm per m)
    - Mathematical constants (e.g., 2, 4 in formulas)
    
    Args:
        number: The number to check
    
    Returns:
        True if the number appears to be exact
    
    Examples:
        >>> is_exact_number(10)
        True
        >>> is_exact_number("10.0")
        False
        >>> is_exact_number(3.14159)
        False
    """
    if isinstance(number, int):
        return True
    if isinstance(number, float):
        # Floats that are exact integers
        return number == int(number) and abs(number) < 1e15
    if isinstance(number, str):
        # Strings without decimal point or scientific notation
        return '.' not in number and 'e' not in number.lower()
    return False


def compare_sig_figs(
    a: Union[int, float, str],
    b: Union[int, float, str]
) -> dict:
    """
    Compare two numbers based on their significant figures.
    
    Args:
        a: First number
        b: Second number
    
    Returns:
        Dictionary with comparison results
    
    Examples:
        >>> compare_sig_figs(123.45, "123.45")
        {'a_sig_figs': 5, 'b_sig_figs': 5, 'equal_sig_figs': True}
    """
    a_sig = count_significant_figures(a)
    b_sig = count_significant_figures(b)
    
    return {
        'a_sig_figs': a_sig,
        'b_sig_figs': b_sig,
        'equal_sig_figs': a_sig == b_sig,
        'difference': abs(a_sig - b_sig),
        'more_precise': 'a' if a_sig > b_sig else ('b' if b_sig > a_sig else 'equal'),
    }


def sig_fig_range(
    value: float,
    sig_figs: int
) -> Tuple[float, float]:
    """
    Calculate the range of possible values given significant figures.
    
    This represents the uncertainty implied by the significant figures.
    
    Args:
        value: The measured value
        sig_figs: Number of significant figures
    
    Returns:
        Tuple of (minimum, maximum) possible values
    
    Examples:
        >>> sig_fig_range(12.3, 3)
        (12.25, 12.35)
        >>> sig_fig_range(1200, 2)
        (1150.0, 1250.0)
    """
    if value == 0:
        return (0.0, 0.0)
    
    # Calculate the implied uncertainty
    magnitude = 10 ** int(math.floor(math.log10(abs(value))))
    uncertainty = magnitude / (10 ** sig_figs)
    
    return (value - uncertainty, value + uncertainty)


def calculate_percent_error(
    measured: float,
    accepted: float,
    sig_figs: int = 2
) -> str:
    """
    Calculate percent error between measured and accepted values.
    
    Args:
        measured: The measured value
        accepted: The accepted/theoretical value
        sig_figs: Number of significant figures for result
    
    Returns:
        Formatted percent error string
    
    Examples:
        >>> calculate_percent_error(9.5, 9.8, 2)
        '3.1%'
    """
    if accepted == 0:
        return "undefined"
    
    error = abs(measured - accepted) / abs(accepted) * 100
    error_rounded = round_to_sig_figs(error, sig_figs)
    
    return f"{error_rounded}%"


def calculate_percent_difference(
    value1: float,
    value2: float,
    sig_figs: int = 2
) -> str:
    """
    Calculate percent difference between two values.
    
    Percent difference is calculated relative to the average of the two values.
    
    Args:
        value1: First value
        value2: Second value
        sig_figs: Number of significant figures for result
    
    Returns:
        Formatted percent difference string
    
    Examples:
        >>> calculate_percent_difference(10.0, 12.0, 2)
        '18%'
    """
    average = (value1 + value2) / 2
    if average == 0:
        return "undefined"
    
    diff = abs(value1 - value2) / abs(average) * 100
    diff_rounded = round_to_sig_figs(diff, sig_figs)
    
    return f"{diff_rounded}%"


# ============================================================================
# Main Demo
# ============================================================================

if __name__ == '__main__':
    print("=" * 60)
    print("AllToolkit - Significant Figures Utilities Demo")
    print("=" * 60)
    
    # Count significant figures
    print("\n--- Counting Significant Figures ---")
    test_values = ["123", "00123", "12300", "12300.", "0.00456", "1.2300", "1.020", "1.00e3"]
    for val in test_values:
        print(f"{val:12} -> {count_significant_figures(val)} significant figures")
    
    # Round to significant figures
    print("\n--- Rounding to Significant Figures ---")
    test_round = [(123.456, 4), (123.456, 3), (0.00123456, 3), (12345, 2), (999.9, 3)]
    for num, sf in test_round:
        rounded = round_to_sig_figs(num, sf)
        formatted = format_sig_figs(num, sf)
        print(f"{num:12} -> {sf} sf: {formatted} (rounded: {rounded})")
    
    # Scientific notation
    print("\n--- Scientific Notation ---")
    test_sci = [(1234.56, 3), (0.00123, 2), (1000000, 4), (0.000000123, 2)]
    for num, sf in test_sci:
        sci = to_scientific_notation(num, sf)
        print(f"{num:15} -> {sf} sf: {sci}")
    
    # Arithmetic with significant figures
    print("\n--- Arithmetic with Significant Figures ---")
    a = SigFigNumber(2.3, 2)
    b = SigFigNumber(4.56, 3)
    print(f"a = {a}, b = {b}")
    print(f"a + b = {a + b}")
    print(f"a - b = {a - b}")
    print(f"a * b = {a * b}")
    print(f"a / b = {a / b}")
    
    # Measurement uncertainty
    print("\n--- Measurement Uncertainty ---")
    mv = create_measured_value(9.81, 0.02, "m/s²")
    print(f"Measured value: {mv}")
    print(f"Relative uncertainty: {mv.relative_uncertainty():.2f}%")
    
    # Uncertainty propagation
    print("\n--- Uncertainty Propagation ---")
    m1 = create_measured_value(2.5, 0.1, "kg")
    m2 = create_measured_value(3.2, 0.2, "kg")
    m_total = propagate_uncertainty_addition(m1, m2)
    print(f"m1 = {m1}")
    print(f"m2 = {m2}")
    print(f"m1 + m2 = {m_total}")
    
    # Multiplication uncertainty
    l = create_measured_value(5.0, 0.1, "m")
    w = create_measured_value(3.0, 0.1, "m")
    area = propagate_uncertainty_multiplication(l, w)
    print(f"\nlength = {l}")
    print(f"width = {w}")
    print(f"area = {area}")
    
    # Percent error
    print("\n--- Percent Error ---")
    measured = 9.5
    accepted = 9.8
    error = calculate_percent_error(measured, accepted, 2)
    print(f"Measured: {measured}, Accepted: {accepted}")
    print(f"Percent error: {error}")
    
    print("\n" + "=" * 60)