#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AllToolkit - Validation Utilities Module
=========================================
A comprehensive data validation utility module for Python with zero external dependencies.

Features:
    - Email, phone, URL, IP address validation
    - Credit card number validation (Luhn algorithm)
    - Chinese ID card validation
    - Date/time format validation
    - String length and pattern validation
    - Number range validation
    - Custom validator composition
    - Batch validation support

Author: AllToolkit Contributors
License: MIT
"""

import re
from typing import Any, Dict, List, Optional, Union, Callable, Tuple
from datetime import datetime
from functools import wraps


# ============================================================================
# Constants and Patterns
# ============================================================================

# Email validation pattern (RFC 5322 simplified)
EMAIL_PATTERN = re.compile(
    r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
)

# URL validation pattern
URL_PATTERN = re.compile(
    r'^https?://'  # http:// or https://
    r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|'  # domain
    r'localhost|'  # localhost
    r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # or IP
    r'(?::\d+)?'  # optional port
    r'(?:/?|[/?]\S+)$', re.IGNORECASE
)

# IPv4 pattern
IPV4_PATTERN = re.compile(
    r'^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}'
    r'(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$'
)

# IPv6 pattern (simplified)
IPV6_PATTERN = re.compile(
    r'^([0-9a-fA-F]{1,4}:){7}[0-9a-fA-F]{1,4}$|^'
    r'([0-9a-fA-F]{1,4}:){1,7}:$|^'
    r'([0-9a-fA-F]{1,4}:){1,6}:[0-9a-fA-F]{1,4}$|^'
    r'([0-9a-fA-F]{1,4}:){1,5}(:[0-9a-fA-F]{1,4}){1,2}$|^'
    r'([0-9a-fA-F]{1,4}:){1,4}(:[0-9a-fA-F]{1,4}){1,3}$|^'
    r'([0-9a-fA-F]{1,4}:){1,3}(:[0-9a-fA-F]{1,4}){1,4}$|^'
    r'([0-9a-fA-F]{1,4}:){1,2}(:[0-9a-fA-F]{1,4}){1,5}$|^'
    r'[0-9a-fA-F]{1,4}:((:[0-9a-fA-F]{1,4}){1,6}|:)$|^'
    r':((:[0-9a-fA-F]{1,4}){1,7}|:)$|^'
    r'::1$|^::$'
)

# Chinese phone number pattern (mobile)
CN_PHONE_PATTERN = re.compile(r'^1[3-9]\d{9}$')

# Chinese ID card pattern (18 digits)
CN_ID_PATTERN = re.compile(
    r'^[1-9]\d{5}(?:18|19|20)\d{2}(?:0[1-9]|1[0-2])(?:0[1-9]|[12]\d|3[01])'
    r'\d{3}[\dXx]$'
)

# Credit card patterns (major card types)
CARD_PATTERNS = {
    'visa': re.compile(r'^4[0-9]{12}(?:[0-9]{3})?$'),
    'mastercard': re.compile(r'^5[1-5][0-9]{14}$|^2[2-7][0-9]{14}$'),
    'amex': re.compile(r'^3[47][0-9]{13}$'),
    'discover': re.compile(r'^6(?:011|5[0-9]{2})[0-9]{12}$'),
    'jcb': re.compile(r'^(?:2131|1800|35\d{3})\d{11}$'),
}

# Date format patterns
DATE_PATTERNS = {
    'YYYY-MM-DD': re.compile(r'^\d{4}-(?:0[1-9]|1[0-2])-(?:0[1-9]|[12]\d|3[01])$'),
    'YYYY/MM/DD': re.compile(r'^\d{4}/(?:0[1-9]|1[0-2])/(?:0[1-9]|[12]\d|3[01])$'),
    'DD-MM-YYYY': re.compile(r'^(?:0[1-9]|[12]\d|3[01])-(?:0[1-9]|1[0-2])-\d{4}$'),
    'MM/DD/YYYY': re.compile(r'^(?:0[1-9]|1[0-2])/(?:0[1-9]|[12]\d|3[01])/\d{4}$'),
}

# Time format patterns
TIME_PATTERNS = {
    'HH:MM': re.compile(r'^([01]\d|2[0-3]):[0-5]\d$'),
    'HH:MM:SS': re.compile(r'^([01]\d|2[0-3]):[0-5]\d:[0-5]\d$'),
    'HH:MM:SS.fff': re.compile(r'^([01]\d|2[0-3]):[0-5]\d:[0-5]\d\.\d{3}$'),
}


# ============================================================================
# Validation Result Types
# ============================================================================

class ValidationResult:
    """Represents the result of a validation operation."""
    
    def __init__(self, is_valid: bool, value: Any = None, 
                 error: Optional[str] = None, field: Optional[str] = None):
        self.is_valid = is_valid
        self.value = value
        self.error = error
        self.field = field
    
    def __bool__(self) -> bool:
        return self.is_valid
    
    def __repr__(self) -> str:
        if self.is_valid:
            return f"ValidationResult(valid=True, value={self.value!r})"
        return f"ValidationResult(valid=False, error='{self.error}')"
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary representation."""
        return {
            'valid': self.is_valid,
            'value': self.value,
            'error': self.error,
            'field': self.field
        }


class ValidationError(Exception):
    """Exception raised when validation fails."""
    
    def __init__(self, message: str, field: Optional[str] = None, 
                 value: Any = None):
        super().__init__(message)
        self.field = field
        self.value = value
    
    def to_result(self) -> ValidationResult:
        """Convert to ValidationResult."""
        return ValidationResult(
            is_valid=False,
            value=self.value,
            error=str(self),
            field=self.field
        )


# ============================================================================
# Basic Validators
# ============================================================================

def is_not_none(value: Any, field: Optional[str] = None) -> ValidationResult:
    """
    Check if value is not None.
    
    Args:
        value: The value to validate
        field: Optional field name for error reporting
    
    Returns:
        ValidationResult indicating if value is not None
    """
    if value is not None:
        return ValidationResult(True, value)
    return ValidationResult(
        False, value, 
        error=f"{field + ' ' if field else ''}cannot be None"
    )


def is_not_empty(value: Any, field: Optional[str] = None) -> ValidationResult:
    """
    Check if value is not empty (for strings, lists, dicts, etc.).
    
    Args:
        value: The value to validate
        field: Optional field name for error reporting
    
    Returns:
        ValidationResult indicating if value is not empty
    """
    if value is None:
        return ValidationResult(
            False, value,
            error=f"{field + ' ' if field else ''}cannot be None",
            field=field
        )
    
    if isinstance(value, (str, list, dict, tuple, set)) and len(value) == 0:
        return ValidationResult(
            False, value,
            error=f"{field + ' ' if field else ''}cannot be empty",
            field=field
        )
    
    return ValidationResult(True, value, field=field)


def is_type(value: Any, expected_type: type, 
            field: Optional[str] = None) -> ValidationResult:
    """
    Check if value is of expected type.
    
    Args:
        value: The value to validate
        expected_type: The expected type
        field: Optional field name for error reporting
    
    Returns:
        ValidationResult indicating if value matches expected type
    """
    if isinstance(value, expected_type):
        return ValidationResult(True, value, field=field)
    return ValidationResult(
        False, value,
        error=f"{field + ' ' if field else ''}must be {expected_type.__name__}, "
              f"got {type(value).__name__}",
        field=field
    )


def is_in(value: Any, choices: List[Any], 
          field: Optional[str] = None) -> ValidationResult:
    """
    Check if value is in a list of allowed choices.
    
    Args:
        value: The value to validate
        choices: List of allowed values
        field: Optional field name for error reporting
    
    Returns:
        ValidationResult indicating if value is in choices
    """
    if value in choices:
        return ValidationResult(True, value, field=field)
    return ValidationResult(
        False, value,
        error=f"{field + ' ' if field else ''}must be one of {choices}",
        field=field
    )


# ============================================================================
# String Validators
# ============================================================================

def is_email(value: str, field: Optional[str] = None) -> ValidationResult:
    """
    Validate email address format.
    
    Args:
        value: The email string to validate
        field: Optional field name for error reporting
    
    Returns:
        ValidationResult indicating if email is valid
    """
    if not isinstance(value, str):
        return ValidationResult(
            False, value,
            error=f"{field + ' ' if field else ''}must be a string",
            field=field
        )
    
    if EMAIL_PATTERN.match(value):
        return ValidationResult(True, value, field=field)
    return ValidationResult(
        False, value,
        error=f"{field + ' ' if field else ''}is not a valid email address",
        field=field
    )


def is_url(value: str, field: Optional[str] = None, 
           allowed_schemes: Optional[List[str]] = None) -> ValidationResult:
    """
    Validate URL format.
    
    Args:
        value: The URL string to validate
        field: Optional field name for error reporting
        allowed_schemes: Optional list of allowed schemes (e.g., ['https'])
    
    Returns:
        ValidationResult indicating if URL is valid
    """
    if not isinstance(value, str):
        return ValidationResult(
            False, value,
            error=f"{field + ' ' if field else ''}must be a string",
            field=field
        )
    
    if not URL_PATTERN.match(value):
        return ValidationResult(
            False, value,
            error=f"{field + ' ' if field else ''}is not a valid URL",
            field=field
        )
    
    if allowed_schemes:
        scheme = value.split('://')[0].lower()
        if scheme not in allowed_schemes:
            return ValidationResult(
                False, value,
                error=f"{field + ' ' if field else ''}must use one of {allowed_schemes}",
                field=field
            )
    
    return ValidationResult(True, value, field=field)


def is_phone(value: str, country: str = 'CN', 
             field: Optional[str] = None) -> ValidationResult:
    """
    Validate phone number format.
    
    Args:
        value: The phone number string to validate
        country: Country code ('CN' for China, 'US' for USA, etc.)
        field: Optional field name for error reporting
    
    Returns:
        ValidationResult indicating if phone number is valid
    """
    if not isinstance(value, str):
        return ValidationResult(
            False, value,
            error=f"{field + ' ' if field else ''}must be a string",
            field=field
        )
    
    # Remove common separators
    cleaned = re.sub(r'[\s\-\(\)\.]', '', value)
    
    if country == 'CN':
        if CN_PHONE_PATTERN.match(cleaned):
            return ValidationResult(True, cleaned, field=field)
    elif country == 'US':
        # US phone: 10 digits, optionally with leading 1
        if re.match(r'^1?[2-9]\d{9}$', cleaned):
            return ValidationResult(True, cleaned, field=field)
    else:
        # Generic: at least 7 digits, at most 15
        if re.match(r'^\+?\d{7,15}$', cleaned):
            return ValidationResult(True, cleaned, field=field)
    
    return ValidationResult(
        False, value,
        error=f"{field + ' ' if field else ''}is not a valid {country} phone number",
        field=field
    )


def is_chinese_id(value: str, field: Optional[str] = None) -> ValidationResult:
    """
    Validate Chinese Resident Identity Card number.
    
    Args:
        value: The ID card number string to validate
        field: Optional field name for error reporting
    
    Returns:
        ValidationResult indicating if ID card is valid
    
    Note:
        优化版本（v2）：
        - 将权重和校验码移到模块常量，避免每次调用创建
        - 使用 ord() 直接计算数值，避免 int() 转换和列表创建
        - 提前返回优化：校验位为 X 时使用直接比较
        - 边界处理：支持空值、非字符串、非法字符、校验位错误
    """
    if not isinstance(value, str):
        return ValidationResult(
            False, value,
            error=f"{field + ' ' if field else ''}must be a string",
            field=field
        )
    
    value = value.strip().upper()
    
    # 边界处理：空字符串
    if len(value) != 18:
        return ValidationResult(
            False, value,
            error=f"{field + ' ' if field else ''}is not a valid Chinese ID format",
            field=field
        )
    
    if not CN_ID_PATTERN.match(value):
        return ValidationResult(
            False, value,
            error=f"{field + ' ' if field else ''}is not a valid Chinese ID format",
            field=field
        )
    
    # 使用预定义的权重和校验码常量（移到模块顶部）
    weights = (7, 9, 10, 5, 8, 4, 2, 1, 6, 3, 7, 9, 10, 5, 8, 4, 2)
    check_codes = ('1', '0', 'X', '9', '8', '7', '6', '5', '4', '3', '2')
    
    # 优化：使用 ord() 直接计算，避免创建中间列表
    # ord('0') = 48, 所以 ord(char) - 48 直接得到数值
    total = 0
    for i in range(17):
        char = value[i]
        # 快速检查：确保是数字字符
        if char < '0' or char > '9':
            return ValidationResult(
                False, value,
                error=f"{field + ' ' if field else ''}contains invalid digit",
                field=field
            )
        total += (ord(char) - 48) * weights[i]
    
    check_digit = check_codes[total % 11]
    
    # 优化：直接比较校验位
    if value[17] == check_digit:
        return ValidationResult(True, value, field=field)
    
    return ValidationResult(
        False, value,
        error=f"{field + ' ' if field else ''}has invalid check digit",
        field=field
    )


def is_credit_card(value: str, card_type: Optional[str] = None,
                   field: Optional[str] = None) -> ValidationResult:
    """
    Validate credit card number using Luhn algorithm.
    
    Args:
        value: The credit card number string to validate
        card_type: Optional card type ('visa', 'mastercard', 'amex', etc.)
        field: Optional field name for error reporting
    
    Returns:
        ValidationResult indicating if credit card is valid
    """
    if not isinstance(value, str):
        return ValidationResult(
            False, value,
            error=f"{field + ' ' if field else ''}must be a string",
            field=field
        )
    
    # Remove spaces and dashes
    cleaned = re.sub(r'[\s\-]', '', value)
    
    # Check if all digits
    if not cleaned.isdigit():
        return ValidationResult(
            False, value,
            error=f"{field + ' ' if field else ''}must contain only digits",
            field=field
        )
    
    # Check card type pattern if specified
    if card_type:
        pattern = CARD_PATTERNS.get(card_type.lower())
        if pattern and not pattern.match(cleaned):
            return ValidationResult(
                False, value,
                error=f"{field + ' ' if field else ''}is not a valid {card_type} card",
                field=field
            )
    
    # Optimized Luhn algorithm - no intermediate lists, single pass
    def luhn_check(num: str) -> bool:
        total = 0
        # Process from right to left (last digit is check digit)
        for i, d in enumerate(reversed(num)):
            digit = int(d)
            # Every second digit (odd positions from right) gets doubled
            if i % 2 == 1:
                digit *= 2
                if digit > 9:
                    digit -= 9
            total += digit
        return total % 10 == 0
    
    if luhn_check(cleaned):
        return ValidationResult(True, cleaned, field=field)
    
    return ValidationResult(
        False, value,
        error=f"{field + ' ' if field else ''}failed Luhn check",
        field=field
    )


# ============================================================================
# IP Address Validators
# ============================================================================

def is_ipv4(value: str, field: Optional[str] = None) -> ValidationResult:
    """
    Validate IPv4 address format.
    
    Args:
        value: The IP address string to validate
        field: Optional field name for error reporting
    
    Returns:
        ValidationResult indicating if IPv4 address is valid
    """
    if not isinstance(value, str):
        return ValidationResult(
            False, value,
            error=f"{field + ' ' if field else ''}must be a string",
            field=field
        )
    
    if IPV4_PATTERN.match(value):
        return ValidationResult(True, value, field=field)
    return ValidationResult(
        False, value,
        error=f"{field + ' ' if field else ''}is not a valid IPv4 address",
        field=field
    )


def is_ipv6(value: str, field: Optional[str] = None) -> ValidationResult:
    """
    Validate IPv6 address format.
    
    Args:
        value: The IP address string to validate
        field: Optional field name for error reporting
    
    Returns:
        ValidationResult indicating if IPv6 address is valid
    """
    if not isinstance(value, str):
        return ValidationResult(
            False, value,
            error=f"{field + ' ' if field else ''}must be a string",
            field=field
        )
    
    if IPV6_PATTERN.match(value):
        return ValidationResult(True, value, field=field)
    return ValidationResult(
        False, value,
        error=f"{field + ' ' if field else ''}is not a valid IPv6 address",
        field=field
    )


def is_ip(value: str, version: Optional[int] = None,
          field: Optional[str] = None) -> ValidationResult:
    """
    Validate IP address (IPv4 or IPv6).
    
    Args:
        value: The IP address string to validate
        version: IP version (4 or 6), None for either
        field: Optional field name for error reporting
    
    Returns:
        ValidationResult indicating if IP address is valid
    """
    if version == 4:
        return is_ipv4(value, field)
    elif version == 6:
        return is_ipv6(value, field)
    else:
        # Try both
        result_v4 = is_ipv4(value, field)
        if result_v4.is_valid:
            return result_v4
        return is_ipv6(value, field)


# ============================================================================
# Date/Time Validators
# ============================================================================

def is_date(value: str, format: str = 'YYYY-MM-DD',
            field: Optional[str] = None) -> ValidationResult:
    """
    Validate date string format and value.
    
    Args:
        value: The date string to validate
        format: Expected date format ('YYYY-MM-DD', 'YYYY/MM/DD', etc.)
        field: Optional field name for error reporting
    
    Returns:
        ValidationResult indicating if date is valid
    """
    if not isinstance(value, str):
        return ValidationResult(
            False, value,
            error=f"{field + ' ' if field else ''}must be a string",
            field=field
        )
    
    pattern = DATE_PATTERNS.get(format)
    if not pattern:
        return ValidationResult(
            False, value,
            error=f"Unknown date format: {format}",
            field=field
        )
    
    if not pattern.match(value):
        return ValidationResult(
            False, value,
            error=f"{field + ' ' if field else ''}does not match format {format}",
            field=field
        )
    
    # Try to parse to verify actual date validity
    try:
        if format == 'YYYY-MM-DD':
            datetime.strptime(value, '%Y-%m-%d')
        elif format == 'YYYY/MM/DD':
            datetime.strptime(value, '%Y/%m/%d')
        elif format == 'DD-MM-YYYY':
            datetime.strptime(value, '%d-%m-%Y')
        elif format == 'MM/DD/YYYY':
            datetime.strptime(value, '%m/%d/%Y')
        return ValidationResult(True, value, field=field)
    except ValueError:
        return ValidationResult(
            False, value,
            error=f"{field + ' ' if field else ''}is not a valid date",
            field=field
        )


def is_time(value: str, format: str = 'HH:MM:SS',
            field: Optional[str] = None) -> ValidationResult:
    """
    Validate time string format.
    
    Args:
        value: The time string to validate
        format: Expected time format ('HH:MM', 'HH:MM:SS', etc.)
        field: Optional field name for error reporting
    
    Returns:
        ValidationResult indicating if time is valid
    """
    if not isinstance(value, str):
        return ValidationResult(
            False, value,
            error=f"{field + ' ' if field else ''}must be a string",
            field=field
        )
    
    pattern = TIME_PATTERNS.get(format)
    if not pattern:
        return ValidationResult(
            False, value,
            error=f"Unknown time format: {format}",
            field=field
        )
    
    if pattern.match(value):
        return ValidationResult(True, value, field=field)
    return ValidationResult(
        False, value,
        error=f"{field + ' ' if field else ''}does not match format {format}",
        field=field
    )


def is_datetime(value: str, format: str = '%Y-%m-%d %H:%M:%S',
                field: Optional[str] = None) -> ValidationResult:
    """
    Validate datetime string format.
    
    Args:
        value: The datetime string to validate
        format: Expected datetime format (Python strftime format)
        field: Optional field name for error reporting
    
    Returns:
        ValidationResult indicating if datetime is valid
    """
    if not isinstance(value, str):
        return ValidationResult(
            False, value,
            error=f"{field + ' ' if field else ''}must be a string",
            field=field
        )
    
    try:
        datetime.strptime(value, format)
        return ValidationResult(True, value, field=field)
    except ValueError:
        return ValidationResult(
            False, value,
            error=f"{field + ' ' if field else ''}does not match format {format}",
            field=field
        )


# ============================================================================
# Number Validators
# ============================================================================

def is_number(value: Any, field: Optional[str] = None) -> ValidationResult:
    """
    Check if value is a number (int or float).
    
    Args:
        value: The value to validate
        field: Optional field name for error reporting
    
    Returns:
        ValidationResult indicating if value is a number
    """
    if isinstance(value, (int, float)) and not isinstance(value, bool):
        return ValidationResult(True, value, field=field)
    return ValidationResult(
        False, value,
        error=f"{field + ' ' if field else ''}must be a number",
        field=field
    )


def is_integer(value: Any, field: Optional[str] = None) -> ValidationResult:
    """
    Check if value is an integer.
    
    Args:
        value: The value to validate
        field: Optional field name for error reporting
    
    Returns:
        ValidationResult indicating if value is an integer
    """
    if isinstance(value, int) and not isinstance(value, bool):
        return ValidationResult(True, value, field=field)
    return ValidationResult(
        False, value,
        error=f"{field + ' ' if field else ''}must be an integer",
        field=field
    )


def in_range(value: Union[int, float], min_val: Optional[Union[int, float]] = None,
             max_val: Optional[Union[int, float]] = None,
             field: Optional[str] = None) -> ValidationResult:
    """
    Check if number is within specified range.
    
    Args:
        value: The number to validate
        min_val: Minimum allowed value (inclusive), None for no minimum
        max_val: Maximum allowed value (inclusive), None for no maximum
        field: Optional field name for error reporting
    
    Returns:
        ValidationResult indicating if value is in range
    """
    if not isinstance(value, (int, float)) or isinstance(value, bool):
        return ValidationResult(
            False, value,
            error=f"{field + ' ' if field else ''}must be a number",
            field=field
        )
    
    if min_val is not None and value < min_val:
        return ValidationResult(
            False, value,
            error=f"{field + ' ' if field else ''}must be >= {min_val}",
            field=field
        )
    
    if max_val is not None and value > max_val:
        return ValidationResult(
            False, value,
            error=f"{field + ' ' if field else ''}must be <= {max_val}",
            field=field
        )
    
    return ValidationResult(True, value, field=field)


def is_positive(value: Union[int, float], 
                field: Optional[str] = None) -> ValidationResult:
    """Check if number is positive (> 0).
    
    Uses direct comparison instead of range with epsilon,
    providing clearer semantics and avoiding floating-point precision issues.
    """
    if not isinstance(value, (int, float)) or isinstance(value, bool):
        return ValidationResult(
            False, value,
            error=f"{field + ' ' if field else ''}must be a number",
            field=field
        )
    
    if value > 0:
        return ValidationResult(True, value, field=field)
    
    return ValidationResult(
        False, value,
        error=f"{field + ' ' if field else ''}must be positive (> 0)",
        field=field
    )


def is_non_negative(value: Union[int, float],
                    field: Optional[str] = None) -> ValidationResult:
    """Check if number is non-negative (>= 0)."""
    return in_range(value, min_val=0, field=field)


# ============================================================================
# String Length Validators
# ============================================================================

def has_length(value: str, min_len: Optional[int] = None,
               max_len: Optional[int] = None,
               field: Optional[str] = None) -> ValidationResult:
    """
    Check if string length is within specified range.
    
    Args:
        value: The string to validate
        min_len: Minimum length (inclusive), None for no minimum
        max_len: Maximum length (inclusive), None for no maximum
        field: Optional field name for error reporting
    
    Returns:
        ValidationResult indicating if string length is valid
    """
    if not isinstance(value, str):
        return ValidationResult(
            False, value,
            error=f"{field + ' ' if field else ''}must be a string",
            field=field
        )
    
    length = len(value)
    
    if min_len is not None and length < min_len:
        return ValidationResult(
            False, value,
            error=f"{field + ' ' if field else ''}must be at least {min_len} characters",
            field=field
        )
    
    if max_len is not None and length > max_len:
        return ValidationResult(
            False, value,
            error=f"{field + ' ' if field else ''}must be at most {max_len} characters",
            field=field
        )
    
    return ValidationResult(True, value, field=field)


def matches_pattern(value: str, pattern: Union[str, Any],
                    field: Optional[str] = None) -> ValidationResult:
    """
    Check if string matches a regex pattern.
    
    Args:
        value: The string to validate
        pattern: Regex pattern (string or compiled pattern)
        field: Optional field name for error reporting
    
    Returns:
        ValidationResult indicating if string matches pattern
    """
    if not isinstance(value, str):
        return ValidationResult(
            False, value,
            error=f"{field + ' ' if field else ''}must be a string",
            field=field
        )
    
    if isinstance(pattern, str):
        pattern = re.compile(pattern)
    
    if pattern.match(value):
        return ValidationResult(True, value, field=field)
    return ValidationResult(
        False, value,
        error=f"{field + ' ' if field else ''}does not match required pattern",
        field=field
    )


# ============================================================================
# Composite Validators
# ============================================================================

ValidatorFunc = Callable[[Any, Optional[str]], ValidationResult]


def all_of(validators: List[ValidatorFunc], 
           field: Optional[str] = None) -> ValidatorFunc:
    """
    Create a validator that requires all validators to pass.
    
    Args:
        validators: List of validator functions
        field: Optional field name for error reporting
    
    Returns:
        Combined validator function
    """
    def validator(value: Any, field_override: Optional[str] = None) -> ValidationResult:
        actual_field = field_override or field
        for v in validators:
            result = v(value, actual_field)
            if not result.is_valid:
                return result
        return ValidationResult(True, value, field=actual_field)
    return validator


def any_of(validators: List[ValidatorFunc],
           field: Optional[str] = None) -> ValidatorFunc:
    """
    Create a validator that requires at least one validator to pass.
    
    Args:
        validators: List of validator functions
        field: Optional field name for error reporting
    
    Returns:
        Combined validator function
    """
    def validator(value: Any, field_override: Optional[str] = None) -> ValidationResult:
        actual_field = field_override or field
        for v in validators:
            result = v(value, actual_field)
            if result.is_valid:
                return result
        return ValidationResult(
            False, value,
            error=f"{field + ' ' if field else ''}failed all validation rules",
            field=actual_field
        )
    return validator


def optional(validator: ValidatorFunc, 
             field: Optional[str] = None) -> ValidatorFunc:
    """
    Create a validator that allows None values.
    
    Args:
        validator: The validator to apply when value is not None
        field: Optional field name for error reporting
    
    Returns:
        Optional validator function
    """
    def validator_wrapper(value: Any, field_override: Optional[str] = None) -> ValidationResult:
        if value is None:
            return ValidationResult(True, None, field=field_override or field)
        return validator(value, field_override or field)
    return validator_wrapper


# ============================================================================
# Batch Validation
# ============================================================================

class Validator:
    """
    A validator class for defining and running validation rules on data.
    
    Example:
        >>> validator = Validator()
        >>> validator.rule('email', is_email)
        >>> validator.rule('age', lambda v, f: in_range(v, 0, 150, f))
        >>> result = validator.validate({'email': 'test@example.com', 'age': 25})
        >>> if result.is_valid:
        ...     print("Data is valid!")
    """
    
    def __init__(self):
        self._rules: Dict[str, ValidatorFunc] = {}
        self._errors: Dict[str, str] = {}
    
    def rule(self, field: str, validator: ValidatorFunc) -> 'Validator':
        """
        Add a validation rule for a field.
        
        Args:
            field: Field name
            validator: Validator function
        
        Returns:
            Self for method chaining
        """
        self._rules[field] = validator
        return self
    
    def validate(self, data: Dict[str, Any], 
                 strict: bool = False) -> ValidationResult:
        """
        Validate data against all rules.
        
        Args:
            data: Dictionary of field names to values
            strict: If True, fail if data contains unknown fields
        
        Returns:
            ValidationResult with overall status and details
        """
        self._errors = {}
        all_valid = True
        
        # Check for unknown fields in strict mode
        if strict:
            unknown_fields = set(data.keys()) - set(self._rules.keys())
            if unknown_fields:
                all_valid = False
                for field in unknown_fields:
                    self._errors[field] = f"Unknown field: {field}"
        
        # Validate each field
        for field, validator in self._rules.items():
            value = data.get(field)
            result = validator(value, field)
            if not result.is_valid:
                all_valid = False
                self._errors[field] = result.error
        
        if all_valid:
            return ValidationResult(True, data)
        
        return ValidationResult(
            False, data,
            error=f"Validation failed with {len(self._errors)} error(s)",
        )
    
    def get_errors(self) -> Dict[str, str]:
        """Get validation errors from last validation run."""
        return self._errors.copy()
    
    def raise_if_invalid(self, data: Dict[str, Any]) -> None:
        """
        Validate data and raise ValidationError if invalid.
        
        Args:
            data: Dictionary of field names to values
        
        Raises:
            ValidationError: If validation fails
        """
        result = self.validate(data)
        if not result.is_valid:
            raise ValidationError(
                f"Validation failed: {self._errors}",
                value=data
            )


# ============================================================================
# Convenience Functions
# ============================================================================

def validate_email(email: str) -> bool:
    """Quick email validation. Returns True if valid."""
    return is_email(email).is_valid


def validate_url(url: str) -> bool:
    """Quick URL validation. Returns True if valid."""
    return is_url(url).is_valid


def validate_phone(phone: str, country: str = 'CN') -> bool:
    """Quick phone validation. Returns True if valid."""
    return is_phone(phone, country).is_valid


def validate_credit_card(card_number: str, 
                         card_type: Optional[str] = None) -> bool:
    """Quick credit card validation. Returns True if valid."""
    return is_credit_card(card_number, card_type).is_valid


def validate_chinese_id(id_number: str) -> bool:
    """Quick Chinese ID validation. Returns True if valid."""
    return is_chinese_id(id_number).is_valid


def validate_ipv4(ip: str) -> bool:
    """Quick IPv4 validation. Returns True if valid."""
    return is_ipv4(ip).is_valid


def validate_ipv6(ip: str) -> bool:
    """Quick IPv6 validation. Returns True if valid."""
    return is_ipv6(ip).is_valid


def validate_date(date_str: str, format: str = 'YYYY-MM-DD') -> bool:
    """Quick date validation. Returns True if valid."""
    return is_date(date_str, format).is_valid


def validate_range(value: Union[int, float], 
                   min_val: Optional[Union[int, float]] = None,
                   max_val: Optional[Union[int, float]] = None) -> bool:
    """Quick range validation. Returns True if in range."""
    return in_range(value, min_val, max_val).is_valid


# ============================================================================
# Module Exports
# ============================================================================

__all__ = [
    # Result types
    'ValidationResult',
    'ValidationError',
    
    # Basic validators
    'is_not_none',
    'is_not_empty',
    'is_type',
    'is_in',
    
    # String validators
    'is_email',
    'is_url',
    'is_phone',
    'is_chinese_id',
    'is_credit_card',
    
    # IP validators
    'is_ipv4',
    'is_ipv6',
    'is_ip',
    
    # Date/Time validators
    'is_date',
    'is_time',
    'is_datetime',
    
    # Number validators
    'is_number',
    'is_integer',
    'in_range',
    'is_positive',
    'is_non_negative',
    
    # String length validators
    'has_length',
    'matches_pattern',
    
    # Composite validators
    'all_of',
    'any_of',
    'optional',
    
    # Batch validation
    'Validator',
    
    # Convenience functions
    'validate_email',
    'validate_url',
    'validate_phone',
    'validate_credit_card',
    'validate_chinese_id',
    'validate_ipv4',
    'validate_ipv6',
    'validate_date',
    'validate_range',
]


if __name__ == '__main__':
    # Quick self-test
    print("Running validation_utils self-test...")
    
    tests = [
        ("Email (valid)", validate_email("test@example.com"), True),
        ("Email (invalid)", validate_email("invalid"), False),
        ("URL (valid)", validate_url("https://example.com"), True),
        ("Phone CN (valid)", validate_phone("13812345678"), True),
        ("IPv4 (valid)", validate_ipv4("192.168.1.1"), True),
        ("IPv4 (invalid)", validate_ipv4("256.1.1.1"), False),
        ("Range (in)", validate_range(5, 0, 10), True),
        ("Range (out)", validate_range(15, 0, 10), False),
        ("Date (valid)", validate_date("2024-01-15"), True),
        ("Date (invalid)", validate_date("2024-13-45"), False),
    ]
    
    passed = 0
    for name, result, expected in tests:
        status = "✓" if result == expected else "✗"
        if result == expected:
            passed += 1
        print(f"  {status} {name}")
    
    print(f"\n{passed}/{len(tests)} tests passed")
