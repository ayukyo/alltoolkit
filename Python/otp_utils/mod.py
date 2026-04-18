#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AllToolkit - OTP Utilities Module
=================================
A comprehensive One-Time Password (OTP) utility module for Python with zero external dependencies.

Features:
    - TOTP (Time-based One-Time Password) generation and validation
    - HOTP (HMAC-based One-Time Password) generation and validation
    - Base32 secret encoding/decoding
    - OTP URI generation for QR codes (authenticator apps)
    - Configurable digits (6, 7, 8) and hash algorithms (SHA1, SHA256, SHA512)
    - Recovery codes generation

Based on RFC 4226 (HOTP) and RFC 6238 (TOTP).

Author: AllToolkit Contributors
License: MIT
"""

import hmac
import hashlib
import time
import struct
import base64
import secrets
import re
from typing import Optional, List, Tuple, Callable
from urllib.parse import quote, urlencode

# ============================================================================
# Constants
# ============================================================================

DEFAULT_DIGITS = 6
DEFAULT_PERIOD = 30  # seconds
DEFAULT_WINDOW = 1   # TOTP validation window (past/future intervals)

SUPPORTED_DIGITS = (6, 7, 8)
SUPPORTED_ALGORITHMS = ('SHA1', 'SHA256', 'SHA512')


# ============================================================================
# Base32 Utilities
# ============================================================================

def encode_base32(data: bytes) -> str:
    """
    Encode bytes to Base32 string (without padding).
    
    Args:
        data: The bytes to encode
    
    Returns:
        Base32 encoded string (uppercase, no padding)
    
    Example:
        >>> encode_base32(b'Hello')
        'JBSWY3DPEE======'
    """
    return base64.b32encode(data).decode('ascii').rstrip('=')


def decode_base32(data: str) -> bytes:
    """
    Decode Base32 string to bytes.
    
    Args:
        data: The Base32 string (with or without padding)
    
    Returns:
        Decoded bytes
    
    Raises:
        ValueError: If the input is not valid Base32
    
    Example:
        >>> decode_base32('JBSWY3DPEE')
        b'Hello'
    """
    # Add padding if necessary
    padding = 8 - (len(data) % 8) if len(data) % 8 != 0 else 0
    padded = data.upper() + '=' * padding
    try:
        return base64.b32decode(padded)
    except Exception as e:
        raise ValueError(f"Invalid Base32 string: {e}")


def generate_secret(length: int = 20) -> str:
    """
    Generate a random Base32 secret for TOTP/HOTP.
    
    Args:
        length: The length of the secret in bytes (default: 20 for 160 bits)
    
    Returns:
        A random Base32 encoded secret
    
    Example:
        >>> secret = generate_secret()
        >>> len(decode_base32(secret)) == 20
        True
    """
    random_bytes = secrets.token_bytes(length)
    return encode_base32(random_bytes)


# ============================================================================
# Core OTP Functions
# ============================================================================

def _hmac_digest(secret: bytes, counter: bytes, algorithm: str = 'SHA1') -> bytes:
    """
    Compute HMAC digest.
    
    Args:
        secret: The secret key bytes
        counter: The counter value bytes
        algorithm: The hash algorithm ('SHA1', 'SHA256', 'SHA512')
    
    Returns:
        The HMAC digest bytes
    """
    if algorithm == 'SHA1':
        hash_func = hashlib.sha1
    elif algorithm == 'SHA256':
        hash_func = hashlib.sha256
    elif algorithm == 'SHA512':
        hash_func = hashlib.sha512
    else:
        raise ValueError(f"Unsupported algorithm: {algorithm}")
    
    return hmac.new(secret, counter, hash_func).digest()


def _dynamic_truncate(digest: bytes, digits: int) -> int:
    """
    Apply dynamic truncation to get the OTP code.
    
    Args:
        digest: The HMAC digest bytes
        digits: Number of digits for the OTP
    
    Returns:
        The truncated integer value
    """
    # Get offset from last 4 bits
    offset = digest[-1] & 0x0F
    
    # Extract 4 bytes starting at offset
    binary = (
        (digest[offset] & 0x7F) << 24 |
        (digest[offset + 1] & 0xFF) << 16 |
        (digest[offset + 2] & 0xFF) << 8 |
        (digest[offset + 3] & 0xFF)
    )
    
    # Get the last 'digits' digits
    return binary % (10 ** digits)


def generate_hotp(secret: str, counter: int, digits: int = DEFAULT_DIGITS,
                  algorithm: str = 'SHA1') -> str:
    """
    Generate an HOTP (HMAC-based One-Time Password).
    
    Args:
        secret: The Base32 encoded secret
        counter: The counter value (must be synchronized)
        digits: Number of digits (6, 7, or 8)
        algorithm: Hash algorithm ('SHA1', 'SHA256', 'SHA512')
    
    Returns:
        The OTP code as a string
    
    Raises:
        ValueError: If digits or algorithm is not supported
    
    Example:
        >>> generate_hotp('JBSWY3DPEHPK3PXP', 0, digits=6)
        '284893'
    """
    if digits not in SUPPORTED_DIGITS:
        raise ValueError(f"Digits must be one of {SUPPORTED_DIGITS}")
    if algorithm not in SUPPORTED_ALGORITHMS:
        raise ValueError(f"Algorithm must be one of {SUPPORTED_ALGORITHMS}")
    
    secret_bytes = decode_base32(secret)
    counter_bytes = struct.pack('>Q', counter)
    digest = _hmac_digest(secret_bytes, counter_bytes, algorithm)
    code = _dynamic_truncate(digest, digits)
    
    return str(code).zfill(digits)


def validate_hotp(secret: str, counter: int, code: str, digits: int = DEFAULT_DIGITS,
                  algorithm: str = 'SHA1') -> bool:
    """
    Validate an HOTP code.
    
    Args:
        secret: The Base32 encoded secret
        counter: The expected counter value
        code: The code to validate
        digits: Number of digits
        algorithm: Hash algorithm
    
    Returns:
        True if the code is valid, False otherwise
    
    Example:
        >>> validate_hotp('JBSWY3DPEHPK3PXP', 0, '284893')
        True
    """
    try:
        expected = generate_hotp(secret, counter, digits, algorithm)
        return hmac.compare_digest(expected, code)
    except ValueError:
        return False


# ============================================================================
# TOTP Functions
# ============================================================================

def _get_time_counter(timestamp: Optional[int] = None, period: int = DEFAULT_PERIOD) -> int:
    """
    Get the time-based counter value.
    
    Args:
        timestamp: Unix timestamp (default: current time)
        period: Time period in seconds
    
    Returns:
        The time-based counter value
    """
    if timestamp is None:
        timestamp = int(time.time())
    return timestamp // period


def generate_totp(secret: str, timestamp: Optional[int] = None,
                  digits: int = DEFAULT_DIGITS, period: int = DEFAULT_PERIOD,
                  algorithm: str = 'SHA1') -> str:
    """
    Generate a TOTP (Time-based One-Time Password).
    
    Args:
        secret: The Base32 encoded secret
        timestamp: Unix timestamp (default: current time)
        digits: Number of digits (6, 7, or 8)
        period: Time period in seconds (default: 30)
        algorithm: Hash algorithm ('SHA1', 'SHA256', 'SHA512')
    
    Returns:
        The OTP code as a string
    
    Example:
        >>> generate_totp('JBSWY3DPEHPK3PXP', timestamp=1234567890, digits=6)
        '680647'
    """
    counter = _get_time_counter(timestamp, period)
    return generate_hotp(secret, counter, digits, algorithm)


def validate_totp(secret: str, code: str, timestamp: Optional[int] = None,
                  digits: int = DEFAULT_DIGITS, period: int = DEFAULT_PERIOD,
                  algorithm: str = 'SHA1', window: int = DEFAULT_WINDOW) -> bool:
    """
    Validate a TOTP code with a time window for clock drift.
    
    Args:
        secret: The Base32 encoded secret
        code: The code to validate
        timestamp: Unix timestamp (default: current time)
        digits: Number of digits
        period: Time period in seconds
        algorithm: Hash algorithm
        window: Number of intervals to check before/after (default: 1)
    
    Returns:
        True if the code is valid within the window, False otherwise
    
    Example:
        >>> # Validate a code within 1 interval window
        >>> validate_totp('JBSWY3DPEHPK3PXP', '680647', timestamp=1234567890)
        True
    """
    try:
        if timestamp is None:
            timestamp = int(time.time())
        
        current_counter = _get_time_counter(timestamp, period)
        
        # Check current interval and surrounding intervals
        for offset in range(-window, window + 1):
            counter = current_counter + offset
            expected = generate_hotp(secret, counter, digits, algorithm)
            if hmac.compare_digest(expected, code):
                return True
        
        return False
    except ValueError:
        return False


# ============================================================================
# OTP URI Generation
# ============================================================================

def build_totp_uri(secret: str, account: str, issuer: str,
                   digits: int = DEFAULT_DIGITS, period: int = DEFAULT_PERIOD,
                   algorithm: str = 'SHA1') -> str:
    """
    Build an otpauth:// URI for TOTP (for QR code generation).
    
    Args:
        secret: The Base32 encoded secret
        account: The account name (e.g., 'user@example.com')
        issuer: The issuer name (e.g., 'MyApp')
        digits: Number of digits
        period: Time period in seconds
        algorithm: Hash algorithm
    
    Returns:
        An otpauth:// URI string
    
    Example:
        >>> uri = build_totp_uri('JBSWY3DPEHPK3PXP', 'user@example.com', 'MyApp')
        >>> uri.startswith('otpauth://totp/')
        True
    """
    params = {
        'secret': secret,
        'issuer': issuer,
        'algorithm': algorithm,
        'digits': digits,
        'period': period
    }
    
    # Format: otpauth://totp/Issuer:Account?params
    label = quote(f"{issuer}:{account}", safe=':')
    query = urlencode(params)
    
    return f"otpauth://totp/{label}?{query}"


def build_hotp_uri(secret: str, account: str, issuer: str, counter: int,
                   digits: int = DEFAULT_DIGITS, algorithm: str = 'SHA1') -> str:
    """
    Build an otpauth:// URI for HOTP (for QR code generation).
    
    Args:
        secret: The Base32 encoded secret
        account: The account name
        issuer: The issuer name
        counter: The current counter value
        digits: Number of digits
        algorithm: Hash algorithm
    
    Returns:
        An otpauth:// URI string
    
    Example:
        >>> uri = build_hotp_uri('JBSWY3DPEHPK3PXP', 'user@example.com', 'MyApp', 0)
        >>> uri.startswith('otpauth://hotp/')
        True
    """
    params = {
        'secret': secret,
        'issuer': issuer,
        'algorithm': algorithm,
        'digits': digits,
        'counter': counter
    }
    
    label = quote(f"{issuer}:{account}", safe=':')
    query = urlencode(params)
    
    return f"otpauth://hotp/{label}?{query}"


def parse_otp_uri(uri: str) -> dict:
    """
    Parse an otpauth:// URI into its components.
    
    Args:
        uri: The otpauth:// URI string
    
    Returns:
        A dictionary with the URI components
    
    Raises:
        ValueError: If the URI is not a valid OTP URI
    
    Example:
        >>> parse_otp_uri('otpauth://totp/MyApp:user@example.com?secret=JBSWY3DPEHPK3PXP&issuer=MyApp')
        {'type': 'totp', 'account': 'user@example.com', 'secret': 'JBSWY3DPEHPK3PXP', ...}
    """
    if not uri.startswith('otpauth://'):
        raise ValueError("Invalid OTP URI: must start with 'otpauth://'")
    
    # Parse type
    parts = uri[10:].split('?', 1)
    if len(parts) != 2:
        raise ValueError("Invalid OTP URI: missing query parameters")
    
    type_and_label = parts[0]
    query_string = parts[1]
    
    # Parse type (totp or hotp)
    type_parts = type_and_label.split('/', 1)
    if len(type_parts) != 2:
        raise ValueError("Invalid OTP URI: invalid format")
    
    otp_type = type_parts[0].lower()
    if otp_type not in ('totp', 'hotp'):
        raise ValueError(f"Invalid OTP type: {otp_type}")
    
    # Parse label
    label = type_parts[1]
    
    # Parse account and issuer from label
    if ':' in label:
        issuer, account = label.split(':', 1)
        issuer = issuer
        account = account
    else:
        issuer = None
        account = label
    
    # Parse query parameters
    params = {}
    for pair in query_string.split('&'):
        if '=' in pair:
            key, value = pair.split('=', 1)
            params[key.lower()] = value
    
    result = {
        'type': otp_type,
        'account': account,
        'secret': params.get('secret', ''),
        'digits': int(params.get('digits', DEFAULT_DIGITS)),
        'algorithm': params.get('algorithm', 'SHA1').upper(),
    }
    
    if issuer or 'issuer' in params:
        result['issuer'] = params.get('issuer', issuer or '')
    
    if otp_type == 'totp':
        result['period'] = int(params.get('period', DEFAULT_PERIOD))
    else:
        result['counter'] = int(params.get('counter', 0))
    
    return result


# ============================================================================
# Recovery Codes
# ============================================================================

def generate_recovery_codes(count: int = 10, length: int = 8) -> List[str]:
    """
    Generate recovery codes for 2FA backup.
    
    Args:
        count: Number of codes to generate (default: 10)
        length: Length of each code (default: 8)
    
    Returns:
        A list of recovery codes
    
    Example:
        >>> codes = generate_recovery_codes(5, 8)
        >>> len(codes)
        5
        >>> all(len(code) == 8 for code in codes)
        True
    """
    codes = []
    chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
    
    for _ in range(count):
        code = ''.join(secrets.choice(chars) for _ in range(length))
        # Insert a dash in the middle for readability
        if length >= 6:
            mid = length // 2
            code = code[:mid] + '-' + code[mid:]
        codes.append(code)
    
    return codes


def validate_recovery_code(codes: List[str], input_code: str,
                           consume: bool = True) -> Tuple[bool, List[str]]:
    """
    Validate a recovery code.
    
    Args:
        codes: The list of valid recovery codes
        input_code: The code to validate
        consume: Whether to remove the code from the list (default: True)
    
    Returns:
        A tuple of (is_valid, remaining_codes)
    
    Example:
        >>> codes = ['ABCD-EFGH', 'IJKL-MNOP']
        >>> is_valid, remaining = validate_recovery_code(codes, 'ABCD-EFGH')
        >>> is_valid
        True
        >>> 'ABCD-EFGH' in remaining
        False
    """
    # Normalize input code
    normalized = input_code.upper().replace(' ', '').replace('-', '')
    
    for i, code in enumerate(codes):
        # Normalize stored code
        stored = code.upper().replace(' ', '').replace('-', '')
        if stored == normalized:
            if consume:
                return True, codes[:i] + codes[i+1:]
            return True, codes
    
    return False, codes


# ============================================================================
# Time Utilities
# ============================================================================

def get_remaining_seconds(period: int = DEFAULT_PERIOD,
                         timestamp: Optional[int] = None) -> int:
    """
    Get remaining seconds until the next TOTP refresh.
    
    Args:
        period: Time period in seconds
        timestamp: Unix timestamp (default: current time)
    
    Returns:
        Remaining seconds
    
    Example:
        >>> remaining = get_remaining_seconds()
        >>> 0 <= remaining <= 30
        True
    """
    if timestamp is None:
        timestamp = int(time.time())
    return period - (timestamp % period)


def format_code(code: str, group_size: int = 3) -> str:
    """
    Format an OTP code with spaces for readability.
    
    Args:
        code: The OTP code
        group_size: Number of digits per group (default: 3)
    
    Returns:
        Formatted code string
    
    Example:
        >>> format_code('123456')
        '123 456'
        >>> format_code('12345678', 4)
        '1234 5678'
    """
    return ' '.join(code[i:i+group_size] for i in range(0, len(code), group_size))


# ============================================================================
# Convenience Classes
# ============================================================================

class TOTP:
    """
    TOTP (Time-based One-Time Password) convenience class.
    
    Example:
        >>> totp = TOTP('JBSWY3DPEHPK3PXP')
        >>> code = totp.generate()
        >>> totp.validate(code)
        True
    """
    
    def __init__(self, secret: str, digits: int = DEFAULT_DIGITS,
                 period: int = DEFAULT_PERIOD, algorithm: str = 'SHA1'):
        """
        Initialize TOTP instance.
        
        Args:
            secret: The Base32 encoded secret
            digits: Number of digits
            period: Time period in seconds
            algorithm: Hash algorithm
        """
        self.secret = secret
        self.digits = digits
        self.period = period
        self.algorithm = algorithm
    
    def generate(self, timestamp: Optional[int] = None) -> str:
        """Generate current TOTP code."""
        return generate_totp(self.secret, timestamp, self.digits,
                            self.period, self.algorithm)
    
    def validate(self, code: str, timestamp: Optional[int] = None,
                 window: int = DEFAULT_WINDOW) -> bool:
        """Validate TOTP code."""
        return validate_totp(self.secret, code, timestamp, self.digits,
                           self.period, self.algorithm, window)
    
    def get_uri(self, account: str, issuer: str) -> str:
        """Get otpauth:// URI for this TOTP."""
        return build_totp_uri(self.secret, account, issuer,
                            self.digits, self.period, self.algorithm)
    
    def get_remaining_seconds(self, timestamp: Optional[int] = None) -> int:
        """Get remaining seconds until next refresh."""
        return get_remaining_seconds(self.period, timestamp)


class HOTP:
    """
    HOTP (HMAC-based One-Time Password) convenience class.
    
    Example:
        >>> hotp = HOTP('JBSWY3DPEHPK3PXP')
        >>> code = hotp.generate(0)
        >>> hotp.validate(code, 0)
        True
    """
    
    def __init__(self, secret: str, digits: int = DEFAULT_DIGITS,
                 algorithm: str = 'SHA1'):
        """
        Initialize HOTP instance.
        
        Args:
            secret: The Base32 encoded secret
            digits: Number of digits
            algorithm: Hash algorithm
        """
        self.secret = secret
        self.digits = digits
        self.algorithm = algorithm
        self._counter = 0
    
    @property
    def counter(self) -> int:
        """Current counter value."""
        return self._counter
    
    def generate(self, counter: Optional[int] = None) -> str:
        """
        Generate HOTP code.
        
        Args:
            counter: Counter value (default: current counter, then increments)
        
        Returns:
            HOTP code
        """
        if counter is None:
            counter = self._counter
            self._counter += 1
        return generate_hotp(self.secret, counter, self.digits, self.algorithm)
    
    def validate(self, code: str, counter: int) -> bool:
        """Validate HOTP code."""
        return validate_hotp(self.secret, counter, code, self.digits, self.algorithm)
    
    def get_uri(self, account: str, issuer: str, counter: Optional[int] = None) -> str:
        """Get otpauth:// URI for this HOTP."""
        if counter is None:
            counter = self._counter
        return build_hotp_uri(self.secret, account, issuer, counter,
                            self.digits, self.algorithm)
    
    def reset_counter(self, value: int = 0) -> None:
        """Reset the counter to a specific value."""
        self._counter = value


# ============================================================================
# Export All
# ============================================================================

__all__ = [
    # Constants
    'DEFAULT_DIGITS',
    'DEFAULT_PERIOD',
    'DEFAULT_WINDOW',
    'SUPPORTED_DIGITS',
    'SUPPORTED_ALGORITHMS',
    
    # Base32 utilities
    'encode_base32',
    'decode_base32',
    'generate_secret',
    
    # HOTP functions
    'generate_hotp',
    'validate_hotp',
    
    # TOTP functions
    'generate_totp',
    'validate_totp',
    
    # URI functions
    'build_totp_uri',
    'build_hotp_uri',
    'parse_otp_uri',
    
    # Recovery codes
    'generate_recovery_codes',
    'validate_recovery_code',
    
    # Time utilities
    'get_remaining_seconds',
    'format_code',
    
    # Classes
    'TOTP',
    'HOTP',
]