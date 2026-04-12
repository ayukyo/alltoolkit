#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AllToolkit - Secrets Utilities Module
======================================
A comprehensive secrets management utility module for Python with zero external dependencies.

Features:
    - Secure password generation with customizable complexity
    - API key and token generation
    - Secure random value generation
    - Password strength evaluation
    - Secret hashing and verification
    - TOTP (Time-based One-Time Password) generation
    - Secure secret storage helpers

Author: AllToolkit Contributors
License: MIT
"""

import secrets
import hashlib
import hmac
import base64
import string
import time
import struct
import os
from typing import Optional, Tuple, List, Any
from datetime import datetime, timezone


# ============================================================================
# Character Sets for Password Generation
# ============================================================================

LOWERCASE = string.ascii_lowercase
UPPERCASE = string.ascii_uppercase
DIGITS = string.digits
SPECIAL = "!@#$%^&*()_+-=[]{}|;:,.<>?"
ALPHANUMERIC = LOWERCASE + UPPERCASE + DIGITS
ALL_CHARS = ALPHANUMERIC + SPECIAL


# ============================================================================
# Password Generation Functions
# ============================================================================

def generate_password(
    length: int = 16,
    use_lowercase: bool = True,
    use_uppercase: bool = True,
    use_digits: bool = True,
    use_special: bool = True,
    exclude_ambiguous: bool = False
) -> str:
    """
    Generate a cryptographically secure random password.
    
    Args:
        length: Password length (minimum 4, default: 16)
        use_lowercase: Include lowercase letters (default: True)
        use_uppercase: Include uppercase letters (default: True)
        use_digits: Include digits (default: True)
        use_special: Include special characters (default: True)
        exclude_ambiguous: Exclude ambiguous characters like 'l', '1', 'I', 'O', '0' (default: False)
    
    Returns:
        A cryptographically secure random password
    
    Raises:
        ValueError: If length < 4 or no character sets selected
    
    Example:
        >>> generate_password(16)
        'Kx9#mP2$nQ7@wL5!'
        >>> generate_password(12, use_special=False)
        'aB3dE6fG9hJ2'
    """
    if length < 4:
        raise ValueError("Password length must be at least 4 characters")
    
    # Build character pool
    char_pool = ""
    required_chars = []
    
    if use_lowercase:
        chars = LOWERCASE
        if exclude_ambiguous:
            chars = chars.replace('l', '')
        char_pool += chars
        required_chars.append(secrets.choice(chars))
    
    if use_uppercase:
        chars = UPPERCASE
        if exclude_ambiguous:
            chars = chars.replace('I', '').replace('O', '')
        char_pool += chars
        required_chars.append(secrets.choice(chars))
    
    if use_digits:
        chars = DIGITS
        if exclude_ambiguous:
            chars = chars.replace('1', '').replace('0', '')
        char_pool += chars
        required_chars.append(secrets.choice(chars))
    
    if use_special:
        chars = SPECIAL
        if exclude_ambiguous:
            chars = chars.replace('|', '').replace(';', '')
        char_pool += chars
        required_chars.append(secrets.choice(chars))
    
    if not char_pool:
        raise ValueError("At least one character set must be selected")
    
    # Generate remaining characters
    remaining_length = length - len(required_chars)
    password_chars = required_chars + [secrets.choice(char_pool) for _ in range(remaining_length)]
    
    # Shuffle using cryptographically secure method
    for i in range(len(password_chars) - 1, 0, -1):
        j = secrets.randbelow(i + 1)
        password_chars[i], password_chars[j] = password_chars[j], password_chars[i]
    
    return ''.join(password_chars)


def generate_passphrase(
    word_count: int = 4,
    separator: str = '-',
    word_list: Optional[List[str]] = None
) -> str:
    """
    Generate a memorable passphrase from random words.
    
    Args:
        word_count: Number of words in the passphrase (default: 4)
        separator: Character to separate words (default: '-')
        word_list: Custom word list (default: uses built-in common words)
    
    Returns:
        A memorable passphrase
    
    Example:
        >>> generate_passphrase(4)
        'correct-horse-battery-staple'
        >>> generate_passphrase(3, separator='_')
        'purple_dragon_mountain'
    """
    if word_list is None:
        word_list = _get_default_word_list()
    
    if word_count < 1:
        raise ValueError("Word count must be at least 1")
    
    if word_count > len(word_list):
        raise ValueError(f"Word count ({word_count}) exceeds word list size ({len(word_list)})")
    
    words = []
    used_indices = set()
    
    for _ in range(word_count):
        while True:
            index = secrets.randbelow(len(word_list))
            if index not in used_indices:
                used_indices.add(index)
                words.append(word_list[index])
                break
    
    return separator.join(words)


def _get_default_word_list() -> List[str]:
    """Get the default word list for passphrase generation."""
    # Common English words - efficient list for passphrase generation
    return [
        'apple', 'brave', 'cloud', 'dragon', 'eagle', 'forest', 'ghost', 'harbor',
        'island', 'jungle', 'knight', 'lemon', 'mountain', 'note', 'ocean', 'piano',
        'queen', 'river', 'sunset', 'tiger', 'umbrella', 'violet', 'whale', 'xenon',
        'yellow', 'zebra', 'anchor', 'basket', 'candle', 'diamond', 'envelope', 'falcon',
        'garden', 'hammer', 'igloo', 'jacket', 'kitchen', 'lantern', 'marble', 'needle',
        'orange', 'penguin', 'quartz', 'rabbit', 'spider', 'turtle', 'unicorn', 'valley',
        'window', 'xylophone', 'yacht', 'zenith', 'aurora', 'breeze', 'crystal', 'dawn',
        'echo', 'flame', 'glacier', 'horizon', 'iris', 'jasmine', 'koala', 'lunar',
        'meadow', 'nebula', 'oasis', 'prism', 'quantum', 'ripple', 'storm', 'thunder',
        'unity', 'velvet', 'wander', 'crimson', 'azure', 'golden', 'silver', 'copper'
    ]


# ============================================================================
# API Key and Token Generation
# ============================================================================

def generate_api_key(prefix: str = 'ak', length: int = 32) -> str:
    """
    Generate a cryptographically secure API key with optional prefix.
    
    Args:
        prefix: Key prefix for identification (default: 'ak')
        length: Length of the random portion in bytes (default: 32)
    
    Returns:
        URL-safe API key string
    
    Example:
        >>> generate_api_key()
        'ak_7Fz9Kx2mPq5Nw8Rt3Yv6Bc1Df4Gh7Jk0'
        >>> generate_api_key('sk', 24)
        'sk_3Qw7Er9Ty2Ui5Op8As1Df4'
    """
    random_bytes = secrets.token_urlsafe(length)
    return f"{prefix}_{random_bytes}"


def generate_bearer_token(length: int = 64) -> str:
    """
    Generate a cryptographically secure bearer token for authentication.
    
    Args:
        length: Length of the random portion in bytes (default: 64)
    
    Returns:
        URL-safe bearer token
    
    Example:
        >>> generate_bearer_token()
        'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...truncated'
    """
    return secrets.token_urlsafe(length)


def generate_session_id(prefix: str = 'sess') -> str:
    """
    Generate a unique session identifier.
    
    Args:
        prefix: Session ID prefix (default: 'sess')
    
    Returns:
        Unique session ID
    
    Example:
        >>> generate_session_id()
        'sess_9Kx2mPq5Nw8Rt3Yv6Bc1Df4Gh7Jk0Lp3'
    """
    random_part = secrets.token_urlsafe(24)
    timestamp = int(time.time() * 1000).to_bytes(8, 'big').hex()[:8]
    return f"{prefix}_{timestamp}_{random_part}"


# ============================================================================
# Password Strength Evaluation
# ============================================================================

def evaluate_password_strength(password: str) -> Tuple[int, str, List[str]]:
    """
    Evaluate the strength of a password.
    
    Args:
        password: The password to evaluate
    
    Returns:
        Tuple of (score 0-100, strength label, list of suggestions)
    
    Example:
        >>> evaluate_password_strength("weak")
        (15, 'Very Weak', ['Password is too short', 'Add uppercase letters', ...])
        >>> evaluate_password_strength("Str0ng!Pass#2024")
        (95, 'Very Strong', [])
    """
    score = 0
    suggestions = []
    
    # Length scoring
    length = len(password)
    if length < 8:
        suggestions.append("Password should be at least 8 characters")
    elif length < 12:
        score += 10
    elif length < 16:
        score += 20
    else:
        score += 30
    
    # Character variety scoring
    has_lower = any(c in LOWERCASE for c in password)
    has_upper = any(c in UPPERCASE for c in password)
    has_digit = any(c in DIGITS for c in password)
    has_special = any(c in SPECIAL for c in password)
    
    variety_count = sum([has_lower, has_upper, has_digit, has_special])
    
    if not has_lower:
        suggestions.append("Add lowercase letters")
    if not has_upper:
        suggestions.append("Add uppercase letters")
    if not has_digit:
        suggestions.append("Add numbers")
    if not has_special:
        suggestions.append("Add special characters (!@#$%^&*)")
    
    score += variety_count * 15  # Up to 60 points for variety
    
    # Pattern penalties
    common_patterns = [
        '123', 'abc', 'qwerty', 'password', 'admin', 'letmein',
        'welcome', 'monkey', 'dragon', 'master', 'login'
    ]
    password_lower = password.lower()
    
    for pattern in common_patterns:
        if pattern in password_lower:
            score -= 20
            suggestions.append(f"Avoid common patterns like '{pattern}'")
            break
    
    # Repeated character penalty
    for i in range(len(password) - 2):
        if password[i] == password[i+1] == password[i+2]:
            score -= 10
            suggestions.append("Avoid repeated characters")
            break
    
    # Normalize score
    score = max(0, min(100, score))
    
    # Determine strength label
    if score < 25:
        strength = "Very Weak"
    elif score < 50:
        strength = "Weak"
    elif score < 70:
        strength = "Moderate"
    elif score < 85:
        strength = "Strong"
    else:
        strength = "Very Strong"
    
    return (score, strength, suggestions)


def is_password_strong(password: str, min_score: int = 70) -> bool:
    """
    Check if a password meets minimum strength requirements.
    
    Args:
        password: The password to check
        min_score: Minimum required score (default: 70)
    
    Returns:
        True if password meets requirements
    
    Example:
        >>> is_password_strong("MyStr0ng!Pass")
        True
        >>> is_password_strong("weak")
        False
    """
    score, _, _ = evaluate_password_strength(password)
    return score >= min_score


# ============================================================================
# Secret Hashing and Verification
# ============================================================================

def hash_secret(
    secret: str,
    salt: Optional[str] = None,
    algorithm: str = 'sha256',
    iterations: int = 100000
) -> str:
    """
    Hash a secret using PBKDF2 for secure storage.
    
    Args:
        secret: The secret to hash
        salt: Optional salt (generated if not provided)
        algorithm: Hash algorithm ('sha256', 'sha512') (default: 'sha256')
        iterations: Number of iterations for PBKDF2 (default: 100000)
    
    Returns:
        Base64-encoded hash with salt prefix
    
    Example:
        >>> hashed = hash_secret("my_password")
        >>> hashed.startswith('sha256:')
        True
    """
    if salt is None:
        salt = secrets.token_hex(16)
    
    if algorithm == 'sha512':
        hash_func = hashlib.sha512
    else:
        hash_func = hashlib.sha256
    
    derived = hashlib.pbkdf2_hmac(
        algorithm,
        secret.encode('utf-8'),
        salt.encode('utf-8'),
        iterations,
        dklen=32
    )
    
    hash_b64 = base64.b64encode(derived).decode('ascii')
    return f"{algorithm}:{iterations}:{salt}:{hash_b64}"


def verify_secret(secret: str, hashed: str) -> bool:
    """
    Verify a secret against a stored hash.
    
    Args:
        secret: The secret to verify
        hashed: The stored hash string
    
    Returns:
        True if secret matches the hash
    
    Example:
        >>> hashed = hash_secret("my_password")
        >>> verify_secret("my_password", hashed)
        True
        >>> verify_secret("wrong_password", hashed)
        False
    """
    try:
        parts = hashed.split(':')
        if len(parts) != 4:
            return False
        
        algorithm, iterations, salt, stored_hash = parts
        iterations = int(iterations)
        
        # Re-hash with same parameters
        if algorithm == 'sha512':
            hash_func = hashlib.sha512
        else:
            hash_func = hashlib.sha256
        
        derived = hashlib.pbkdf2_hmac(
            algorithm,
            secret.encode('utf-8'),
            salt.encode('utf-8'),
            iterations,
            dklen=32
        )
        
        hash_b64 = base64.b64encode(derived).decode('ascii')
        
        # Constant-time comparison
        return hmac.compare_digest(hash_b64, stored_hash)
    
    except (ValueError, IndexError, TypeError):
        return False


# ============================================================================
# TOTP (Time-based One-Time Password) Generation
# ============================================================================

def generate_totp(
    secret: str,
    time_step: int = 30,
    digits: int = 6,
    timestamp: Optional[float] = None
) -> str:
    """
    Generate a TOTP code for two-factor authentication.
    
    Args:
        secret: Base32-encoded shared secret
        time_step: Time step in seconds (default: 30)
        digits: Number of digits in the code (default: 6)
        timestamp: Optional timestamp (uses current time if not provided)
    
    Returns:
        TOTP code as a zero-padded string
    
    Example:
        >>> secret = 'JBSWY3DPEHPK3PXP'  # Base32 encoded
        >>> generate_totp(secret)
        '123456'
    """
    if timestamp is None:
        timestamp = time.time()
    
    # Calculate time counter
    counter = int(timestamp // time_step)
    
    # Decode base32 secret
    try:
        key = base64.b32decode(secret.upper().replace(' ', ''))
    except Exception:
        # If not valid base32, treat as raw bytes
        key = secret.encode('utf-8')[:20].ljust(20, b'\x00')
    
    # Pack counter as big-endian 8-byte integer
    counter_bytes = struct.pack('>Q', counter)
    
    # Generate HMAC-SHA1
    hmac_hash = hmac.new(key, counter_bytes, hashlib.sha1).digest()
    
    # Dynamic truncation
    offset = hmac_hash[-1] & 0x0F
    truncated = struct.unpack('>I', hmac_hash[offset:offset+4])[0]
    truncated &= 0x7FFFFFFF
    
    # Generate code
    code = truncated % (10 ** digits)
    
    return str(code).zfill(digits)


def verify_totp(
    secret: str,
    code: str,
    time_step: int = 30,
    digits: int = 6,
    window: int = 1
) -> bool:
    """
    Verify a TOTP code with time window tolerance.
    
    Args:
        secret: Base32-encoded shared secret
        code: The code to verify
        time_step: Time step in seconds (default: 30)
        digits: Number of digits in the code (default: 6)
        window: Number of time steps to check before/after current (default: 1)
    
    Returns:
        True if code is valid within the time window
    
    Example:
        >>> secret = 'JBSWY3DPEHPK3PXP'
        >>> code = generate_totp(secret)
        >>> verify_totp(secret, code)
        True
    """
    current_time = time.time()
    
    for offset in range(-window, window + 1):
        expected = generate_totp(
            secret,
            time_step=time_step,
            digits=digits,
            timestamp=current_time + (offset * time_step)
        )
        if hmac.compare_digest(code, expected):
            return True
    
    return False


def generate_totp_secret() -> str:
    """
    Generate a new random TOTP secret.
    
    Returns:
        Base32-encoded secret suitable for TOTP
    
    Example:
        >>> secret = generate_totp_secret()
        >>> len(secret)
        32
    """
    random_bytes = secrets.token_bytes(20)
    return base64.b32encode(random_bytes).decode('ascii').rstrip('=')


# ============================================================================
# Secure Random Utilities
# ============================================================================

def secure_random_int(min_value: int, max_value: int) -> int:
    """
    Generate a cryptographically secure random integer in range.
    
    Args:
        min_value: Minimum value (inclusive)
        max_value: Maximum value (inclusive)
    
    Returns:
        Random integer in range [min_value, max_value]
    
    Example:
        >>> secure_random_int(1, 100)
        42
    """
    if min_value > max_value:
        raise ValueError("min_value must be <= max_value")
    
    range_size = max_value - min_value + 1
    return min_value + secrets.randbelow(range_size)


def secure_random_bytes(length: int) -> bytes:
    """
    Generate cryptographically secure random bytes.
    
    Args:
        length: Number of bytes to generate
    
    Returns:
        Random bytes
    
    Example:
        >>> secure_random_bytes(16)
        b'\\x8f\\x3a\\x9c...'
    """
    return secrets.token_bytes(length)


def secure_random_hex(length: int = 32) -> str:
    """
    Generate cryptographically secure random hex string.
    
    Args:
        length: Number of hex characters (must be even, default: 32)
    
    Returns:
        Random hex string
    
    Example:
        >>> secure_random_hex(16)
        'a3f7c9e2b1d4f6a8'
    """
    return secrets.token_hex(length // 2)


def secure_shuffle(items: List[Any]) -> List[Any]:
    """
    Cryptographically secure shuffle of a list.
    
    Args:
        items: List to shuffle
    
    Returns:
        New shuffled list (original unchanged)
    
    Example:
        >>> secure_shuffle([1, 2, 3, 4, 5])
        [3, 1, 5, 2, 4]
    """
    result = items.copy()
    for i in range(len(result) - 1, 0, -1):
        j = secrets.randbelow(i + 1)
        result[i], result[j] = result[j], result[i]
    return result


def secure_choice(items: List[Any]) -> Any:
    """
    Cryptographically secure random choice from a list.
    
    Args:
        items: Non-empty list to choose from
    
    Returns:
        Random item from the list
    
    Raises:
        ValueError: If list is empty
    
    Example:
        >>> secure_choice(['red', 'green', 'blue'])
        'green'
    """
    if not items:
        raise ValueError("Cannot choose from empty list")
    return items[secrets.randbelow(len(items))]


# ============================================================================
# Secret Storage Helpers
# ============================================================================

def store_secret_env(name: str, value: str) -> bool:
    """
    Store a secret in environment variable (for current process).
    
    Note: This only sets the variable for the current process and its children.
    For persistent storage, use a secrets manager or encrypted file.
    
    Args:
        name: Environment variable name
        value: Secret value
    
    Returns:
        True if successfully set
    
    Example:
        >>> store_secret_env('API_KEY', 'sk-123456')
        True
        >>> os.environ.get('API_KEY')
        'sk-123456'
    """
    try:
        os.environ[name] = value
        return True
    except Exception:
        return False


def get_secret_env(name: str, default: Optional[str] = None) -> Optional[str]:
    """
    Get a secret from environment variable.
    
    Args:
        name: Environment variable name
        default: Default value if not found
    
    Returns:
        Secret value or default
    
    Example:
        >>> get_secret_env('API_KEY', default='no-key')
        'sk-123456'
    """
    return os.environ.get(name, default)


def mask_secret(secret: str, visible_chars: int = 4) -> str:
    """
    Mask a secret for safe display (e.g., in logs).
    
    Args:
        secret: The secret to mask
        visible_chars: Number of characters to show at start and end (default: 4)
    
    Returns:
        Masked secret string
    
    Example:
        >>> mask_secret("sk-1234567890abcdef")
        'sk-1************cdef'
        >>> mask_secret("short", visible_chars=2)
        'sh***rt'
    """
    if len(secret) <= visible_chars * 2:
        return '*' * len(secret)
    
    start = secret[:visible_chars]
    end = secret[-visible_chars:]
    middle_length = len(secret) - (visible_chars * 2)
    
    return f"{start}{'*' * middle_length}{end}"


# ============================================================================
# Utility Functions
# ============================================================================

def is_secure_string(s: str, min_length: int = 8) -> bool:
    """
    Check if a string meets basic security requirements.
    
    Args:
        s: String to check
        min_length: Minimum length requirement (default: 8)
    
    Returns:
        True if string meets requirements
    
    Example:
        >>> is_secure_string("Str0ng!Pass")
        True
        >>> is_secure_string("weak")
        False
    """
    if len(s) < min_length:
        return False
    
    has_lower = any(c in LOWERCASE for c in s)
    has_upper = any(c in UPPERCASE for c in s)
    has_digit = any(c in DIGITS for c in s)
    
    return has_lower and has_upper and has_digit


def compare_secrets(a: str, b: str) -> bool:
    """
    Constant-time comparison of two secrets to prevent timing attacks.
    
    Args:
        a: First secret
        b: Second secret
    
    Returns:
        True if secrets are equal
    
    Example:
        >>> compare_secrets("secret1", "secret1")
        True
        >>> compare_secrets("secret1", "secret2")
        False
    """
    return hmac.compare_digest(
        a.encode('utf-8') if isinstance(a, str) else a,
        b.encode('utf-8') if isinstance(b, str) else b
    )


# ============================================================================
# Main Entry Point (for CLI usage)
# ============================================================================

if __name__ == '__main__':
    import argparse
    
    parser = argparse.ArgumentParser(description='Secrets Utilities CLI')
    parser.add_argument('--password', action='store_true', help='Generate a password')
    parser.add_argument('--length', type=int, default=16, help='Password length')
    parser.add_argument('--passphrase', action='store_true', help='Generate a passphrase')
    parser.add_argument('--words', type=int, default=4, help='Number of words')
    parser.add_argument('--api-key', action='store_true', help='Generate an API key')
    parser.add_argument('--totp-secret', action='store_true', help='Generate TOTP secret')
    parser.add_argument('--hash', type=str, help='Hash a secret')
    parser.add_argument('--verify', nargs=2, metavar=('SECRET', 'HASH'), help='Verify a secret')
    parser.add_argument('--strength', type=str, help='Evaluate password strength')
    
    args = parser.parse_args()
    
    if args.password:
        print(generate_password(args.length))
    elif args.passphrase:
        print(generate_passphrase(args.words))
    elif args.api_key:
        print(generate_api_key())
    elif args.totp_secret:
        print(generate_totp_secret())
    elif args.hash:
        print(hash_secret(args.hash))
    elif args.verify:
        result = verify_secret(args.verify[0], args.verify[1])
        print(f"Valid: {result}")
    elif args.strength:
        score, strength, suggestions = evaluate_password_strength(args.strength)
        print(f"Score: {score}/100")
        print(f"Strength: {strength}")
        if suggestions:
            print("Suggestions:")
            for s in suggestions:
                print(f"  - {s}")
    else:
        parser.print_help()
