#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""AllToolkit - Random Utilities Module

Comprehensive random utilities for Python with zero external dependencies.
Provides secure random generation, UUIDs, random selection, shuffling, and more.

Author: AllToolkit
License: MIT
"""

import random
import secrets
import uuid
import string
import time
from typing import (
    Union, List, Tuple, Dict, Any, Optional, 
    Sequence, TypeVar, Iterable, Callable
)
from pathlib import Path
from datetime import datetime, timedelta


# =============================================================================
# Type Aliases
# =============================================================================

T = TypeVar('T')
RandomSource = Union[random.Random, secrets.SystemRandom]


# =============================================================================
# Constants
# =============================================================================

DEFAULT_CHARSET_ALPHANUMERIC = string.ascii_letters + string.digits
DEFAULT_CHARSET_LOWERCASE = string.ascii_lowercase
DEFAULT_CHARSET_UPPERCASE = string.ascii_uppercase
DEFAULT_CHARSET_DIGITS = string.digits
DEFAULT_CHARSET_HEX = string.hexdigits.lower()
DEFAULT_CHARSET_BASE62 = string.ascii_letters + string.digits
DEFAULT_CHARSET_BASE64 = string.ascii_letters + string.digits + '+/'


# =============================================================================
# Secure Random Generation
# =============================================================================

def secure_random_bytes(n: int) -> bytes:
    """
    Generate n cryptographically secure random bytes.
    
    Uses secrets module for cryptographic security.
    
    Args:
        n: Number of bytes to generate
        
    Returns:
        Random bytes
        
    Example:
        >>> data = secure_random_bytes(16)
        >>> len(data)
        16
    """
    return secrets.token_bytes(n)


def secure_random_int(lower: int, upper: int) -> int:
    """
    Generate a cryptographically secure random integer in [lower, upper].
    
    Args:
        lower: Lower bound (inclusive)
        upper: Upper bound (inclusive)
        
    Returns:
        Random integer
        
    Raises:
        ValueError: If lower > upper
        
    Example:
        >>> result = secure_random_int(1, 100)
        >>> 1 <= result <= 100
        True
    """
    if lower > upper:
        raise ValueError(f"lower ({lower}) must be <= upper ({upper})")
    return secrets.randbelow(upper - lower + 1) + lower


def secure_random_float() -> float:
    """
    Generate a cryptographically secure random float in [0.0, 1.0).
    
    Returns:
        Random float
        
    Example:
        >>> result = secure_random_float()
        >>> 0.0 <= result < 1.0
        True
    """
    return secrets.randbelow(2**53) / 2**53


def secure_random_choice(seq: Sequence[T]) -> T:
    """
    Choose a random element from a sequence using cryptographic security.
    
    Args:
        seq: Non-empty sequence to choose from
        
    Returns:
        Random element from sequence
        
    Raises:
        ValueError: If sequence is empty
        
    Example:
        >>> result = secure_random_choice(['a', 'b', 'c'])
        >>> result in ['a', 'b', 'c']
        True
    """
    if not seq:
        raise ValueError("Cannot choose from empty sequence")
    return seq[secrets.randbelow(len(seq))]


def secure_random_sample(seq: Sequence[T], k: int) -> List[T]:
    """
    Choose k unique random elements from a sequence.
    
    Args:
        seq: Sequence to sample from
        k: Number of elements to choose
        
    Returns:
        List of k random elements
        
    Raises:
        ValueError: If k > len(seq) or k < 0
        
    Example:
        >>> result = secure_random_sample([1, 2, 3, 4, 5], 3)
        >>> len(result) == 3 and len(set(result)) == 3
        True
    """
    if k < 0:
        raise ValueError(f"k must be non-negative, got {k}")
    if k > len(seq):
        raise ValueError(f"Sample size {k} exceeds population size {len(seq)}")
    
    # Use Fisher-Yates style selection for security
    population = list(seq)
    result = []
    for _ in range(k):
        idx = secrets.randbelow(len(population))
        result.append(population.pop(idx))
    return result


# =============================================================================
# Random String Generation
# =============================================================================

def random_string(length: int = 16, 
                  charset: str = DEFAULT_CHARSET_ALPHANUMERIC,
                  secure: bool = True) -> str:
    """
    Generate a random string of specified length.
    
    Args:
        length: Length of the string to generate
        charset: Characters to choose from
        secure: If True, use cryptographically secure random
        
    Returns:
        Random string
        
    Raises:
        ValueError: If charset is empty or length is negative
        
    Example:
        >>> result = random_string(10)
        >>> len(result) == 10
        True
        >>> all(c in DEFAULT_CHARSET_ALPHANUMERIC for c in result)
        True
    """
    if not charset:
        raise ValueError("Charset cannot be empty")
    if length < 0:
        raise ValueError(f"Length must be non-negative, got {length}")
    
    if secure:
        return ''.join(
            charset[secrets.randbelow(len(charset))] 
            for _ in range(length)
        )
    else:
        return ''.join(
            random.choice(charset) 
            for _ in range(length)
        )


def random_password(length: int = 16, 
                    use_lowercase: bool = True,
                    use_uppercase: bool = True,
                    use_digits: bool = True,
                    use_special: bool = True,
                    secure: bool = True) -> str:
    """
    Generate a random password with specified character types.
    
    Args:
        length: Password length
        use_lowercase: Include lowercase letters
        use_uppercase: Include uppercase letters
        use_digits: Include digits
        use_special: Include special characters
        secure: Use cryptographically secure random
        
    Returns:
        Random password
        
    Raises:
        ValueError: If no character types selected or length too short
        
    Example:
        >>> pwd = random_password(12)
        >>> len(pwd) == 12
        True
    """
    special_chars = '!@#$%^&*()_+-=[]{}|;:,.<>?'
    
    charset = ''
    required_chars = []
    
    if use_lowercase:
        charset += string.ascii_lowercase
        required_chars.append(random.choice(string.ascii_lowercase))
    if use_uppercase:
        charset += string.ascii_uppercase
        required_chars.append(random.choice(string.ascii_uppercase))
    if use_digits:
        charset += string.digits
        required_chars.append(random.choice(string.digits))
    if use_special:
        charset += special_chars
        required_chars.append(random.choice(special_chars))
    
    if not charset:
        raise ValueError("At least one character type must be selected")
    
    min_length = len(required_chars)
    if length < min_length:
        raise ValueError(f"Length must be at least {min_length} for selected character types")
    
    # Generate remaining characters
    remaining_length = length - min_length
    if secure:
        remaining = ''.join(
            charset[secrets.randbelow(len(charset))] 
            for _ in range(remaining_length)
        )
    else:
        remaining = ''.join(
            random.choice(charset) 
            for _ in range(remaining_length)
        )
    
    # Combine and shuffle
    password_chars = list(required_chars) + list(remaining)
    
    if secure:
        # Fisher-Yates shuffle with secure random
        for i in range(len(password_chars) - 1, 0, -1):
            j = secrets.randbelow(i + 1)
            password_chars[i], password_chars[j] = password_chars[j], password_chars[i]
    else:
        random.shuffle(password_chars)
    
    return ''.join(password_chars)


def random_token(length: int = 32, url_safe: bool = True) -> str:
    """
    Generate a random token suitable for authentication/verification.
    
    Args:
        length: Token length in bytes (before encoding)
        url_safe: If True, use URL-safe base64 encoding
        
    Returns:
        Random token string
        
    Example:
        >>> token = random_token()
        >>> len(token) >= 32
        True
    """
    if url_safe:
        return secrets.token_urlsafe(length)
    else:
        return secrets.token_hex(length)


def random_uuid(version: int = 4) -> str:
    """
    Generate a random UUID.
    
    Args:
        version: UUID version (1, 3, 4, or 5)
                 Note: versions 3 and 5 require namespace and name
        
    Returns:
        UUID string
        
    Raises:
        ValueError: If version not supported
        
    Example:
        >>> uid = random_uuid()
        >>> len(uid) == 36  # UUID format: 8-4-4-4-12
        True
    """
    if version == 4:
        return str(uuid.uuid4())
    elif version == 1:
        return str(uuid.uuid1())
    else:
        raise ValueError(f"UUID version {version} not supported. Use 1 or 4.")


def random_slug(length: int = 8, separator: str = '-') -> str:
    """
    Generate a random slug (URL-friendly identifier).
    
    Args:
        length: Number of random segments
        separator: Character to separate segments
        
    Returns:
        Random slug string
        
    Example:
        >>> slug = random_slug()
        >>> '-' in slug or len(slug) > 0
        True
    """
    segments = [random_string(4, DEFAULT_CHARSET_LOWERCASE + string.digits) 
                for _ in range(length)]
    return separator.join(segments)


# =============================================================================
# Random Number Generation
# =============================================================================

def random_int(lower: int, upper: int, secure: bool = False) -> int:
    """
    Generate a random integer in [lower, upper].
    
    Args:
        lower: Lower bound (inclusive)
        upper: Upper bound (inclusive)
        secure: Use cryptographically secure random
        
    Returns:
        Random integer
        
    Example:
        >>> result = random_int(1, 10)
        >>> 1 <= result <= 10
        True
    """
    if secure:
        return secure_random_int(lower, upper)
    return random.randint(lower, upper)


def random_float(lower: float = 0.0, upper: float = 1.0, 
                 secure: bool = False) -> float:
    """
    Generate a random float in [lower, upper).
    
    Args:
        lower: Lower bound (inclusive)
        upper: Upper bound (exclusive)
        secure: Use cryptographically secure random
        
    Returns:
        Random float
        
    Example:
        >>> result = random_float()
        >>> 0.0 <= result < 1.0
        True
    """
    if secure:
        return lower + secure_random_float() * (upper - lower)
    return random.uniform(lower, upper)


def random_gauss(mean: float = 0.0, std: float = 1.0) -> float:
    """
    Generate a random float from Gaussian (normal) distribution.
    
    Args:
        mean: Mean (center) of the distribution
        std: Standard deviation
        
    Returns:
        Random float from normal distribution
        
    Example:
        >>> result = random_gauss()
        >>> isinstance(result, float)
        True
    """
    return random.gauss(mean, std)


def random_bool(probability: float = 0.5) -> bool:
    """
    Generate a random boolean with specified probability of True.
    
    Args:
        probability: Probability of returning True (0.0 to 1.0)
        
    Returns:
        Random boolean
        
    Raises:
        ValueError: If probability out of range
        
    Example:
        >>> result = random_bool()
        >>> result in [True, False]
        True
    """
    if not 0.0 <= probability <= 1.0:
        raise ValueError(f"Probability must be between 0.0 and 1.0, got {probability}")
    return random.random() < probability


# =============================================================================
# Random Selection and Shuffling
# =============================================================================

def random_choice(seq: Sequence[T], secure: bool = False) -> T:
    """
    Choose a random element from a sequence.
    
    Args:
        seq: Non-empty sequence
        secure: Use cryptographically secure random
        
    Returns:
        Random element
        
    Raises:
        ValueError: If sequence is empty
        
    Example:
        >>> result = random_choice([1, 2, 3])
        >>> result in [1, 2, 3]
        True
    """
    if secure:
        return secure_random_choice(seq)
    if not seq:
        raise ValueError("Cannot choose from empty sequence")
    return random.choice(seq)


def random_sample(seq: Sequence[T], k: int, 
                  secure: bool = False) -> List[T]:
    """
    Choose k unique random elements from a sequence.
    
    Args:
        seq: Sequence to sample from
        k: Number of elements
        secure: Use cryptographically secure random
        
    Returns:
        List of k random elements
        
    Example:
        >>> result = random_sample([1, 2, 3, 4, 5], 3)
        >>> len(result) == 3
        True
    """
    if secure:
        return secure_random_sample(seq, k)
    return random.sample(list(seq), k)


def random_shuffle(seq: List[T], secure: bool = False) -> List[T]:
    """
    Shuffle a list in place and return it.
    
    Args:
        seq: List to shuffle
        secure: Use cryptographically secure random
        
    Returns:
        The same list, shuffled
        
    Example:
        >>> original = [1, 2, 3, 4, 5]
        >>> result = random_shuffle(original.copy())
        >>> set(result) == set(original)
        True
    """
    if secure:
        # Fisher-Yates shuffle with secure random
        for i in range(len(seq) - 1, 0, -1):
            j = secrets.randbelow(i + 1)
            seq[i], seq[j] = seq[j], seq[i]
    else:
        random.shuffle(seq)
    return seq


def weighted_choice(items: Sequence[T], 
                    weights: Sequence[float]) -> T:
    """
    Choose a random element with weighted probability.
    
    Args:
        items: Sequence of items to choose from
        weights: Sequence of weights (must match items length)
        
    Returns:
        Random element based on weights
        
    Raises:
        ValueError: If lengths don't match or weights invalid
        
    Example:
        >>> result = weighted_choice(['a', 'b'], [0.9, 0.1])
        >>> result in ['a', 'b']
        True
    """
    if len(items) != len(weights):
        raise ValueError("items and weights must have same length")
    if not items:
        raise ValueError("Cannot choose from empty sequence")
    if any(w < 0 for w in weights):
        raise ValueError("Weights must be non-negative")
    
    total = sum(weights)
    if total == 0:
        raise ValueError("Sum of weights must be positive")
    
    # Normalize weights
    normalized = [w / total for w in weights]
    
    # Cumulative weights
    cumulative = []
    running = 0.0
    for w in normalized:
        running += w
        cumulative.append(running)
    
    # Select based on random value
    r = random.random()
    for i, threshold in enumerate(cumulative):
        if r < threshold:
            return items[i]
    
    return items[-1]  # Fallback for floating point edge cases


# =============================================================================
# Random Date and Time
# =============================================================================

def random_datetime(start: datetime = None, 
                    end: datetime = None) -> datetime:
    """
    Generate a random datetime between start and end.
    
    Args:
        start: Start datetime (default: 1970-01-01)
        end: End datetime (default: now)
        
    Returns:
        Random datetime
        
    Example:
        >>> from datetime import datetime
        >>> start = datetime(2020, 1, 1)
        >>> end = datetime(2025, 12, 31)
        >>> result = random_datetime(start, end)
        >>> start <= result <= end
        True
    """
    if start is None:
        start = datetime(1970, 1, 1)
    if end is None:
        end = datetime.now()
    
    if start > end:
        start, end = end, start
    
    delta = end - start
    random_seconds = random.randint(0, int(delta.total_seconds()))
    return start + timedelta(seconds=random_seconds)


def random_date(start_year: int = 1970, 
                end_year: int = None) -> datetime:
    """
    Generate a random date.
    
    Args:
        start_year: Start year (inclusive)
        end_year: End year (inclusive, default: current year)
        
    Returns:
        Random datetime (date portion)
        
    Example:
        >>> result = random_date(2000, 2020)
        >>> 2000 <= result.year <= 2020
        True
    """
    if end_year is None:
        end_year = datetime.now().year
    
    start = datetime(start_year, 1, 1)
    end = datetime(end_year, 12, 31, 23, 59, 59)
    
    return random_datetime(start, end)


def random_time() -> datetime:
    """
    Generate a random time of day.
    
    Returns:
        Random datetime with arbitrary date and random time
        
    Example:
        >>> result = random_time()
        >>> 0 <= result.hour < 24
        True
    """
    return random_datetime(
        datetime(2000, 1, 1, 0, 0, 0),
        datetime(2000, 1, 1, 23, 59, 59)
    )


# =============================================================================
# Random Data Generation
# =============================================================================

def random_email(domain: str = "example.com") -> str:
    """
    Generate a random email address.
    
    Args:
        domain: Email domain
        
    Returns:
        Random email address
        
    Example:
        >>> email = random_email()
        >>> '@' in email and email.endswith('example.com')
        True
    """
    username = random_string(
        random_int(5, 12), 
        DEFAULT_CHARSET_LOWERCASE + string.digits + '._'
    )
    return f"{username}@{domain}"


def random_phone(country_code: str = "+1", length: int = 10) -> str:
    """
    Generate a random phone number.
    
    Args:
        country_code: Country code prefix
        length: Number of digits after country code
        
    Returns:
        Random phone number string
        
    Example:
        >>> phone = random_phone()
        >>> phone.startswith('+1')
        True
    """
    number = ''.join(secrets.choice(string.digits) for _ in range(length))
    return f"{country_code}{number}"


def random_ipv4(private: bool = False) -> str:
    """
    Generate a random IPv4 address.
    
    Args:
        private: If True, generate a private IP (10.x.x.x, 172.16-31.x.x, 192.168.x.x)
        
    Returns:
        Random IPv4 address string
        
    Example:
        >>> ip = random_ipv4()
        >>> len(ip.split('.')) == 4
        True
    """
    if private:
        choice = secrets.randbelow(3)
        if choice == 0:
            return f"10.{random_int(0, 255)}.{random_int(0, 255)}.{random_int(1, 254)}"
        elif choice == 1:
            return f"172.{random_int(16, 31)}.{random_int(0, 255)}.{random_int(1, 254)}"
        else:
            return f"192.168.{random_int(0, 255)}.{random_int(1, 254)}"
    else:
        return f"{random_int(1, 223)}.{random_int(0, 255)}.{random_int(0, 255)}.{random_int(1, 254)}"


def random_color(format: str = 'hex') -> str:
    """
    Generate a random color.
    
    Args:
        format: Output format ('hex', 'rgb', 'hsl')
        
    Returns:
        Color string in specified format
        
    Raises:
        ValueError: If format not supported
        
    Example:
        >>> color = random_color()
        >>> color.startswith('#') and len(color) == 7
        True
    """
    if format == 'hex':
        r = secrets.randbelow(256)
        g = secrets.randbelow(256)
        b = secrets.randbelow(256)
        return f"#{r:02x}{g:02x}{b:02x}"
    
    elif format == 'rgb':
        r = secrets.randbelow(256)
        g = secrets.randbelow(256)
        b = secrets.randbelow(256)
        return f"rgb({r}, {g}, {b})"
    
    elif format == 'hsl':
        h = secrets.randbelow(360)
        s = secrets.randbelow(101)
        l = secrets.randbelow(101)
        return f"hsl({h}, {s}%, {l}%)"
    
    else:
        raise ValueError(f"Unsupported color format: {format}. Use 'hex', 'rgb', or 'hsl'.")


# =============================================================================
# Random ID Generation
# =============================================================================

def random_id(prefix: str = "", length: int = 12, 
              separator: str = "_", timestamp: bool = False) -> str:
    """
    Generate a random unique identifier.
    
    Args:
        prefix: Optional prefix
        length: Length of random portion
        separator: Separator between prefix and random part
        timestamp: If True, include timestamp
        
    Returns:
        Random ID string
        
    Example:
        >>> id_val = random_id("user")
        >>> id_val.startswith("user_")
        True
    """
    parts = []
    
    if prefix:
        parts.append(prefix)
    
    if timestamp:
        parts.append(str(int(time.time() * 1000)))
    
    parts.append(random_string(length, DEFAULT_CHARSET_ALPHANUMERIC.lower()))
    
    return separator.join(parts)


def random_correlation_id() -> str:
    """
    Generate a random correlation/tracing ID.
    
    Returns:
        Correlation ID string
        
    Example:
        >>> cid = random_correlation_id()
        >>> len(cid) > 0
        True
    """
    return f"corr-{random_uuid()}"


def random_request_id() -> str:
    """
    Generate a random request ID.
    
    Returns:
        Request ID string
        
    Example:
        >>> rid = random_request_id()
        >>> rid.startswith('req-')
        True
    """
    return f"req-{random_string(16, DEFAULT_CHARSET_HEX)}"


# =============================================================================
# Seeded Random (Reproducible)
# =============================================================================

class SeededRandom:
    """
    Seeded random number generator for reproducible randomness.
    
    Example:
        >>> rng = SeededRandom(42)
        >>> rng.random_int(1, 100)
        82
        >>> rng2 = SeededRandom(42)
        >>> rng2.random_int(1, 100) == rng.random_int(1, 100)
        True
    """
    
    def __init__(self, seed: int):
        """
        Initialize with a seed.
        
        Args:
            seed: Random seed
        """
        self._rng = random.Random(seed)
    
    def random_int(self, lower: int, upper: int) -> int:
        """Generate random int in [lower, upper]."""
        return self._rng.randint(lower, upper)
    
    def random_float(self, lower: float = 0.0, upper: float = 1.0) -> float:
        """Generate random float in [lower, upper)."""
        return self._rng.uniform(lower, upper)
    
    def random_choice(self, seq: Sequence[T]) -> T:
        """Choose random element from sequence."""
        return self._rng.choice(seq)
    
    def random_sample(self, seq: Sequence[T], k: int) -> List[T]:
        """Sample k elements from sequence."""
        return self._rng.sample(list(seq), k)
    
    def random_shuffle(self, seq: List[T]) -> List[T]:
        """Shuffle list in place."""
        self._rng.shuffle(seq)
        return seq
    
    def random_string(self, length: int = 16, 
                      charset: str = DEFAULT_CHARSET_ALPHANUMERIC) -> str:
        """Generate random string."""
        return ''.join(
            self._rng.choice(charset) 
            for _ in range(length)
        )
    
    def random_bool(self, probability: float = 0.5) -> bool:
        """Generate random boolean."""
        return self._rng.random() < probability
    
    def seed(self, seed: int):
        """Reseed the generator."""
        self._rng.seed(seed)


# =============================================================================
# Random Math Utilities
# =============================================================================

def random_point_2d(min_x: float = 0, max_x: float = 1,
                    min_y: float = 0, max_y: float = 1) -> Tuple[float, float]:
    """
    Generate a random 2D point.
    
    Args:
        min_x, max_x: X range
        min_y, max_y: Y range
        
    Returns:
        (x, y) tuple
        
    Example:
        >>> x, y = random_point_2d()
        >>> 0 <= x <= 1 and 0 <= y <= 1
        True
    """
    return (
        random.uniform(min_x, max_x),
        random.uniform(min_y, max_y)
    )


def random_point_3d(min_x: float = 0, max_x: float = 1,
                    min_y: float = 0, max_y: float = 1,
                    min_z: float = 0, max_z: float = 1) -> Tuple[float, float, float]:
    """
    Generate a random 3D point.
    
    Args:
        min_x, max_x: X range
        min_y, max_y: Y range
        min_z, max_z: Z range
        
    Returns:
        (x, y, z) tuple
    """
    return (
        random.uniform(min_x, max_x),
        random.uniform(min_y, max_y),
        random.uniform(min_z, max_z)
    )


def random_vector(length: int, min_val: float = -1.0, 
                  max_val: float = 1.0) -> List[float]:
    """
    Generate a random vector.
    
    Args:
        length: Vector dimension
        min_val: Minimum value
        max_val: Maximum value
        
    Returns:
        List of random floats
        
    Example:
        >>> v = random_vector(3)
        >>> len(v) == 3
        True
    """
    return [random.uniform(min_val, max_val) for _ in range(length)]


def random_matrix(rows: int, cols: int, 
                  min_val: float = 0.0, max_val: float = 1.0) -> List[List[float]]:
    """
    Generate a random matrix.
    
    Args:
        rows: Number of rows
        cols: Number of columns
        min_val: Minimum value
        max_val: Maximum value
        
    Returns:
        2D list representing matrix
        
    Example:
        >>> m = random_matrix(2, 3)
        >>> len(m) == 2 and len(m[0]) == 3
        True
    """
    return [
        [random.uniform(min_val, max_val) for _ in range(cols)]
        for _ in range(rows)
    ]


# =============================================================================
# Dice and Games
# =============================================================================

def roll_dice(sides: int = 6, count: int = 1) -> List[int]:
    """
    Roll one or more dice.
    
    Args:
        sides: Number of sides per die
        count: Number of dice to roll
        
    Returns:
        List of roll results
        
    Raises:
        ValueError: If sides < 2 or count < 1
        
    Example:
        >>> result = roll_dice(6, 2)
        >>> len(result) == 2 and all(1 <= r <= 6 for r in result)
        True
    """
    if sides < 2:
        raise ValueError(f"Dice must have at least 2 sides, got {sides}")
    if count < 1:
        raise ValueError(f"Must roll at least 1 die, got {count}")
    
    return [random_int(1, sides) for _ in range(count)]


def roll_d20() -> int:
    """Roll a 20-sided die (D&D style)."""
    return roll_dice(20, 1)[0]


def coin_flip() -> str:
    """
    Flip a coin.
    
    Returns:
        'heads' or 'tails'
        
    Example:
        >>> result = coin_flip()
        >>> result in ['heads', 'tails']
        True
    """
    return random_choice(['heads', 'tails'])


def draw_card(deck_type: str = 'standard') -> str:
    """
    Draw a random card from a deck.
    
    Args:
        deck_type: 'standard' (52 cards), 'poker' (52 cards), or 'short' (32 cards)
        
    Returns:
        Card string (e.g., 'A♠', 'K♥', '7♦')
        
    Raises:
        ValueError: If deck_type not supported
    """
    suits = ['♠', '♥', '♦', '♣']
    
    if deck_type in ['standard', 'poker']:
        ranks = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']
    elif deck_type == 'short':
        ranks = ['7', '8', '9', '10', 'J', 'Q', 'K', 'A']
    else:
        raise ValueError(f"Unknown deck type: {deck_type}")
    
    suit = random_choice(suits)
    rank = random_choice(ranks)
    return f"{rank}{suit}"


# =============================================================================
# Main Entry Point
# =============================================================================

if __name__ == "__main__":
    # Demo usage
    print("Random Utilities Demo")
    print("=" * 50)
    
    print("\nSecure Random:")
    print(f"  Bytes: {secure_random_bytes(8).hex()}")
    print(f"  Int (1-100): {secure_random_int(1, 100)}")
    print(f"  Float: {secure_random_float():.6f}")
    
    print("\nRandom Strings:")
    print(f"  String: {random_string(16)}")
    print(f"  Password: {random_password(16)}")
    print(f"  Token: {random_token()}")
    print(f"  UUID: {random_uuid()}")
    print(f"  Slug: {random_slug()}")
    
    print("\nRandom Numbers:")
    print(f"  Int (1-100): {random_int(1, 100)}")
    print(f"  Float: {random_float():.6f}")
    print(f"  Gauss: {random_gauss():.6f}")
    print(f"  Bool: {random_bool()}")
    
    print("\nRandom Selection:")
    items = ['apple', 'banana', 'cherry', 'date']
    print(f"  Choice: {random_choice(items)}")
    print(f"  Sample: {random_sample(items, 2)}")
    print(f"  Shuffle: {random_shuffle(items.copy())}")
    
    print("\nRandom Data:")
    print(f"  Email: {random_email()}")
    print(f"  Phone: {random_phone()}")
    print(f"  IPv4: {random_ipv4()}")
    print(f"  Color: {random_color()}")
    
    print("\nRandom IDs:")
    print(f"  ID: {random_id('user')}")
    print(f"  Correlation: {random_correlation_id()}")
    print(f"  Request: {random_request_id()}")
    
    print("\nGames:")
    print(f"  Dice (2d6): {roll_dice(6, 2)}")
    print(f"  D20: {roll_d20()}")
    print(f"  Coin: {coin_flip()}")
    print(f"  Card: {draw_card()}")
    
    print("\nSeeded Random:")
    rng = SeededRandom(42)
    print(f"  With seed 42: {rng.random_string(10)}")
    rng2 = SeededRandom(42)
    print(f"  Same seed: {rng2.random_string(10)}")
