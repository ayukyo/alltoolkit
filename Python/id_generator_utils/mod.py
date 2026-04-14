#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""AllToolkit - ID Generator Utilities Module

Comprehensive ID generation utilities for Python with zero external dependencies.
Provides Snowflake ID, ULID, NanoID, ObjectId, and various ID generation strategies.

Author: AllToolkit
License: MIT
"""

import time
import threading
import random
import os
import hashlib
import struct
from typing import Union, Optional, Callable
from datetime import datetime, timezone
from collections import deque


# =============================================================================
# Constants
# =============================================================================

# Snowflake constants
SNOWFLAKE_EPOCH = 1704067200000  # 2024-01-01 00:00:00 UTC in milliseconds
SNOWFLAKE_MAX_WORKER_ID = 31
SNOWFLAKE_MAX_SEQUENCE = 4095

# ULID alphabet
ULID_ALPHABET = '0123456789ABCDEFGHJKMNPQRSTVWXYZ'
ULID_LENGTH = 26

# NanoID default alphabet
NANO_ALPHABET = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
NANO_DEFAULT_LENGTH = 21

# ObjectId
OBJECTID_LENGTH = 24


# =============================================================================
# Snowflake ID Generator
# =============================================================================

class SnowflakeGenerator:
    """
    Twitter Snowflake-like ID generator for distributed systems.
    
    Generates 64-bit IDs with structure:
    - 1 bit: unused (always 0)
    - 41 bits: timestamp (milliseconds since epoch)
    - 5 bits: worker ID (0-31)
    - 5 bits: data center ID (0-31)
    - 12 bits: sequence number (0-4095)
    
    Thread-safe implementation.
    
    Example:
        >>> gen = SnowflakeGenerator(worker_id=1, datacenter_id=1)
        >>> id1 = gen.generate()
        >>> id2 = gen.generate()
        >>> id2 > id1
        True
    """
    
    def __init__(
        self,
        worker_id: int = 0,
        datacenter_id: int = 0,
        epoch: int = SNOWFLAKE_EPOCH
    ):
        """
        Initialize Snowflake generator.
        
        Args:
            worker_id: Worker ID (0-31)
            datacenter_id: Data center ID (0-31)
            epoch: Custom epoch in milliseconds
            
        Raises:
            ValueError: If worker_id or datacenter_id is out of range
        """
        if worker_id < 0 or worker_id > SNOWFLAKE_MAX_WORKER_ID:
            raise ValueError(f"worker_id must be between 0 and {SNOWFLAKE_MAX_WORKER_ID}")
        if datacenter_id < 0 or datacenter_id > SNOWFLAKE_MAX_WORKER_ID:
            raise ValueError(f"datacenter_id must be between 0 and {SNOWFLAKE_MAX_WORKER_ID}")
        
        self.worker_id = worker_id
        self.datacenter_id = datacenter_id
        self.epoch = epoch
        self.sequence = 0
        self.last_timestamp = -1
        self._lock = threading.Lock()
    
    def _get_timestamp(self) -> int:
        """Get current timestamp in milliseconds."""
        return int(time.time() * 1000)
    
    def _wait_next_millis(self, last_timestamp: int) -> int:
        """Wait until next millisecond."""
        timestamp = self._get_timestamp()
        while timestamp <= last_timestamp:
            timestamp = self._get_timestamp()
        return timestamp
    
    def generate(self) -> int:
        """
        Generate a unique snowflake ID.
        
        Returns:
            64-bit unique ID
            
        Raises:
            RuntimeError: If system clock moves backwards
        """
        with self._lock:
            timestamp = self._get_timestamp()
            
            if timestamp < self.last_timestamp:
                raise RuntimeError(
                    f"Clock moved backwards! Refusing to generate ID for "
                    f"{self.last_timestamp - timestamp} milliseconds"
                )
            
            if timestamp == self.last_timestamp:
                self.sequence = (self.sequence + 1) & SNOWFLAKE_MAX_SEQUENCE
                if self.sequence == 0:
                    timestamp = self._wait_next_millis(self.last_timestamp)
            else:
                self.sequence = 0
            
            self.last_timestamp = timestamp
            
            return ((timestamp - self.epoch) << 22) | \
                   (self.datacenter_id << 17) | \
                   (self.worker_id << 12) | \
                   self.sequence
    
    def generate_batch(self, count: int) -> list:
        """
        Generate multiple IDs at once.
        
        Args:
            count: Number of IDs to generate
            
        Returns:
            List of unique IDs
        """
        return [self.generate() for _ in range(count)]
    
    @staticmethod
    def parse(id: int, epoch: int = SNOWFLAKE_EPOCH) -> dict:
        """
        Parse a snowflake ID into its components.
        
        Args:
            id: Snowflake ID
            epoch: Custom epoch used for generation
            
        Returns:
            Dictionary with timestamp, worker_id, datacenter_id, sequence
        """
        timestamp = (id >> 22) + epoch
        datacenter_id = (id >> 17) & 0x1F
        worker_id = (id >> 12) & 0x1F
        sequence = id & 0xFFF
        
        return {
            'timestamp': timestamp,
            'datetime': datetime.fromtimestamp(timestamp / 1000, tz=timezone.utc),
            'worker_id': worker_id,
            'datacenter_id': datacenter_id,
            'sequence': sequence
        }


# =============================================================================
# ULID (Universally Unique Lexicographically Sortable Identifier)
# =============================================================================

class ULID:
    """
    ULID generator - 128-bit IDs that are lexicographically sortable.
    
    Format: 26 characters using Crockford's base32 encoding
    - 10 characters: timestamp (48 bits, milliseconds since Unix epoch)
    - 16 characters: randomness (80 bits)
    
    Example:
        >>> ulid = ULID.generate()
        >>> len(ulid)
        26
        >>> ULID.get_timestamp(ulid)  # Get timestamp from ULID
    """
    
    _last_timestamp = 0
    _last_random = os.urandom(10)
    _lock = threading.Lock()
    
    @classmethod
    def generate(cls) -> str:
        """
        Generate a new ULID.
        
        Returns:
            26-character ULID string
        """
        with cls._lock:
            timestamp = int(time.time() * 1000)
            
            if timestamp == cls._last_timestamp:
                # Increment random portion
                cls._last_random = cls._increment_random(cls._last_random)
            else:
                cls._last_timestamp = timestamp
                cls._last_random = os.urandom(10)
            
            # Encode timestamp (48 bits = 6 bytes)
            time_bytes = struct.pack('>Q', timestamp)[2:8]  # Take bytes 2-7 (6 bytes)
            time_part = cls._encode_base32(time_bytes)
            
            # Encode randomness (80 bits = 10 bytes)
            random_part = cls._encode_base32(cls._last_random)
            
            return time_part + random_part
    
    @staticmethod
    def _increment_random(data: bytes) -> bytes:
        """Increment random bytes by 1."""
        result = bytearray(data)
        for i in range(len(result) - 1, -1, -1):
            result[i] = (result[i] + 1) & 0xFF
            if result[i] != 0:
                break
        return bytes(result)
    
    @classmethod
    def _encode_base32(cls, data: bytes) -> str:
        """
        Encode bytes to Crockford's base32.
        
        Each 5 bits maps to one character:
        - 6 bytes (48 bits) -> 10 characters
        - 10 bytes (80 bits) -> 16 characters
        """
        result = []
        # Convert bytes to integer
        value = int.from_bytes(data, 'big')
        
        # Calculate output length
        num_chars = (len(data) * 8 + 4) // 5
        
        # Encode from right to left
        for _ in range(num_chars):
            result.append(ULID_ALPHABET[value & 0x1F])
            value >>= 5
        
        return ''.join(reversed(result))
    
    @staticmethod
    def _decode_base32(ulid_part: str) -> int:
        """
        Decode base32 string to integer.
        
        Args:
            ulid_part: Base32 encoded string
            
        Returns:
            Integer value
        """
        value = 0
        for char in ulid_part.upper():
            idx = ULID_ALPHABET.index(char)
            value = (value << 5) | idx
        return value
    
    @staticmethod
    def get_timestamp(ulid: str) -> datetime:
        """
        Extract timestamp from a ULID.
        
        Args:
            ulid: 26-character ULID string
            
        Returns:
            datetime object
        """
        # Decode first 10 characters (timestamp)
        time_part = ulid[:10]
        timestamp_ms = ULID._decode_base32(time_part)
        
        return datetime.fromtimestamp(timestamp_ms / 1000, tz=timezone.utc)
    
    @staticmethod
    def compare(ulid1: str, ulid2: str) -> int:
        """
        Compare two ULIDs by timestamp.
        
        Args:
            ulid1: First ULID
            ulid2: Second ULID
            
        Returns:
            -1 if ulid1 < ulid2, 0 if equal, 1 if ulid1 > ulid2
        """
        if ulid1 < ulid2:
            return -1
        elif ulid1 > ulid2:
            return 1
        return 0


# =============================================================================
# NanoID Generator
# =============================================================================

class NanoID:
    """
    NanoID generator - small, secure, URL-friendly unique IDs.
    
    Uses cryptographically secure random number generation.
    
    Example:
        >>> NanoID.generate()
        'V1StGXR8_Z5jdHi6B-myT'
        >>> NanoID.generate(length=10, alphabet='0123456789')
        '4738924682'
    """
    
    @classmethod
    def generate(
        cls,
        length: int = NANO_DEFAULT_LENGTH,
        alphabet: str = NANO_ALPHABET
    ) -> str:
        """
        Generate a NanoID.
        
        Args:
            length: Length of the ID (default 21)
            alphabet: Characters to use (default alphanumeric)
            
        Returns:
            Random string ID
        """
        alphabet_len = len(alphabet)
        
        # Calculate mask for efficient sampling
        # We need the smallest 2^n - 1 >= alphabet_len
        mask = (1 << ((alphabet_len - 1).bit_length())) - 1
        
        result = []
        
        while len(result) < length:
            # Generate random bytes
            random_bytes = os.urandom(length * 2)
            
            for byte in random_bytes:
                # Use rejection sampling to avoid bias
                idx = byte & mask
                if idx < alphabet_len:
                    result.append(alphabet[idx])
                    if len(result) >= length:
                        break
        
        return ''.join(result)
    
    @classmethod
    def generate_custom(cls, alphabet: str, length: int = 21) -> str:
        """
        Generate NanoID with custom alphabet.
        
        Args:
            alphabet: Custom character set
            length: Length of the ID
            
        Returns:
            Random string ID
        """
        return cls.generate(length=length, alphabet=alphabet)
    
    @classmethod
    def numeric(cls, length: int = 16) -> str:
        """Generate numeric-only ID."""
        return cls.generate(length=length, alphabet='0123456789')
    
    @classmethod
    def lowercase(cls, length: int = 24) -> str:
        """Generate lowercase alphanumeric ID."""
        return cls.generate(length=length, alphabet='0123456789abcdefghijklmnopqrstuvwxyz')
    
    @classmethod
    def no_lookalikes(cls, length: int = 24) -> str:
        """Generate ID without lookalike characters (l1I, O0, etc.)."""
        safe_alphabet = '23456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghjkmnpqrstuvwxyz'
        return cls.generate(length=length, alphabet=safe_alphabet)
    
    @classmethod
    def url_safe(cls, length: int = 21) -> str:
        """Generate URL-safe ID with underscores and hyphens."""
        url_alphabet = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ_-'
        return cls.generate(length=length, alphabet=url_alphabet)


# =============================================================================
# ObjectId Generator (MongoDB-style)
# =============================================================================

class ObjectId:
    """
    MongoDB-style ObjectId generator.
    
    12-byte structure:
    - 4 bytes: timestamp (seconds since Unix epoch)
    - 3 bytes: machine identifier
    - 2 bytes: process ID
    - 3 bytes: counter
    
    Example:
        >>> oid = ObjectId.generate()
        >>> len(oid)
        24
        >>> ObjectId.get_timestamp(oid)
    """
    
    _machine_id = None
    _process_id = None
    _counter = None
    _lock = threading.Lock()
    
    @classmethod
    def _init(cls):
        """Initialize machine ID, process ID, and counter."""
        if cls._machine_id is None:
            # Generate machine ID from hostname or random
            try:
                hostname = os.uname().nodename.encode()
                cls._machine_id = hashlib.md5(hostname).digest()[:3]
            except:
                cls._machine_id = os.urandom(3)
            
            # Process ID (2 bytes)
            cls._process_id = os.getpid() & 0xFFFF
            
            # Counter (start with random)
            cls._counter = random.randint(0, 0xFFFFFF)
    
    @classmethod
    def generate(cls) -> str:
        """
        Generate a new ObjectId.
        
        Returns:
            24-character hex string
        """
        cls._init()
        
        with cls._lock:
            timestamp = int(time.time())
            cls._counter = (cls._counter + 1) & 0xFFFFFF
            
            # Pack into 12 bytes
            oid = struct.pack(
                '>IHB3sI',
                timestamp,
                cls._process_id,
                0,  # Padding for machine_id
                cls._machine_id,
                cls._counter
            )
            
            # Correct the structure
            oid = struct.pack('>I', timestamp)
            oid += cls._machine_id
            oid += struct.pack('>H', cls._process_id)
            oid += struct.pack('>I', cls._counter)[1:]  # 3 bytes
            
            return oid.hex().lower()
    
    @staticmethod
    def get_timestamp(oid: str) -> datetime:
        """
        Extract timestamp from ObjectId.
        
        Args:
            oid: 24-character hex string
            
        Returns:
            datetime object
        """
        timestamp_bytes = bytes.fromhex(oid[:8])
        timestamp = struct.unpack('>I', timestamp_bytes)[0]
        return datetime.fromtimestamp(timestamp, tz=timezone.utc)
    
    @staticmethod
    def is_valid(oid: str) -> bool:
        """
        Check if string is a valid ObjectId.
        
        Args:
            oid: String to validate
            
        Returns:
            True if valid ObjectId
        """
        if len(oid) != OBJECTID_LENGTH:
            return False
        try:
            int(oid, 16)
            return True
        except ValueError:
            return False


# =============================================================================
# Simple ID Generators
# =============================================================================

def short_id(length: int = 8, alphabet: str = None) -> str:
    """
    Generate a short random ID.
    
    Args:
        length: Length of the ID
        alphabet: Characters to use (default: alphanumeric)
        
    Returns:
        Random string ID
        
    Example:
        >>> short_id(8)
        'aB3x9KmP'
    """
    if alphabet is None:
        alphabet = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
    
    return NanoID.generate(length=length, alphabet=alphabet)


def timestamp_id(prefix: str = '', suffix: str = '') -> str:
    """
    Generate a timestamp-based ID.
    
    Format: {prefix}{timestamp_ms}{random}{suffix}
    
    Args:
        prefix: Optional prefix
        suffix: Optional suffix
        
    Returns:
        Timestamp-based ID
        
    Example:
        >>> timestamp_id('ORD')
        'ORD1713076800000x7kP'
    """
    ts = int(time.time() * 1000)
    rand = ''.join(random.choices('0123456789abcdef', k=4))
    return f"{prefix}{ts}{rand}{suffix}"


def sequential_id(
    prefix: str = '',
    start: int = 1,
    padding: int = 0
) -> Callable[[], str]:
    """
    Create a sequential ID generator.
    
    Args:
        prefix: Optional prefix
        start: Starting number
        padding: Zero-padding width
        
    Returns:
        Generator function
        
    Example:
        >>> gen = sequential_id('ITEM', padding=6)
        >>> gen()
        'ITEM000001'
        >>> gen()
        'ITEM000002'
    """
    counter = [start]  # Use list for closure mutability
    
    def generator() -> str:
        value = counter[0]
        counter[0] += 1
        if padding:
            return f"{prefix}{str(value).zfill(padding)}"
        return f"{prefix}{value}"
    
    return generator


def prefixed_uuid(prefix: str, separator: str = '_') -> str:
    """
    Generate a UUID with prefix.
    
    Args:
        prefix: Prefix string
        separator: Separator between prefix and UUID
        
    Returns:
        Prefixed UUID string
        
    Example:
        >>> prefixed_uuid('USER')
        'USER_a1b2c3d4-e5f6-7890-abcd-ef1234567890'
    """
    import uuid
    return f"{prefix}{separator}{uuid.uuid4()}"


def ksuid(timestamp: int = None) -> str:
    """
    Generate a K-Sortable Unique Identifier (KSUID).
    
    Format: {timestamp_seconds}{random_bytes}
    - 4 bytes: timestamp (seconds since epoch)
    - 16 bytes: random
    
    Args:
        timestamp: Custom timestamp (default: now)
        
    Returns:
        20-character base62 encoded string
        
    Example:
        >>> ksuid()
        'aWgEPTl1tmebfsQzFP4bxwgy80V'
    """
    BASE62 = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
    
    if timestamp is None:
        timestamp = int(time.time())
    
    # KSUID epoch: May 13, 2014
    ksuid_epoch = 1400000000
    adjusted_ts = timestamp - ksuid_epoch
    
    # Combine timestamp (4 bytes) + random (16 bytes)
    payload = struct.pack('>I', adjusted_ts) + os.urandom(16)
    
    # Convert to integer
    value = int.from_bytes(payload, 'big')
    
    # Encode to base62
    result = []
    while value > 0:
        value, remainder = divmod(value, 62)
        result.append(BASE62[remainder])
    
    return ''.join(reversed(result)).zfill(27)


def cuid2(length: int = 24) -> str:
    """
    Generate a CUID2 (Collision-resistant Unique Identifier).
    
    Secure, collision-resistant IDs optimized for horizontal scaling.
    
    Args:
        length: Length of the ID (default 24)
        
    Returns:
        CUID2 string
        
    Example:
        >>> cuid2()
        'clh3am8ji0000356uk8j6q8zo'
    """
    # Use crypto random for security
    random_bytes = os.urandom(length)
    
    # Encode to base36 for URL safety
    BASE36 = '0123456789abcdefghijklmnopqrstuvwxyz'
    
    value = int.from_bytes(random_bytes, 'big')
    result = []
    while value > 0 and len(result) < length:
        value, remainder = divmod(value, 36)
        result.append(BASE36[remainder])
    
    # Pad with random if needed
    while len(result) < length:
        result.append(BASE36[random.randint(0, 35)])
    
    return ''.join(reversed(result))


def tsid(prefix: str = '', node_id: int = 0) -> str:
    """
    Generate a Time-Sorted ID (TSID).
    
    Similar to Twitter Snowflake but with different bit allocation:
    - 42 bits: timestamp (milliseconds)
    - 8 bits: node ID
    - 14 bits: sequence
    
    Args:
        prefix: Optional prefix
        node_id: Node identifier (0-255)
        
    Returns:
        TSID string
        
    Example:
        >>> tsid('ORD')
        'ORD512345678901234'
    """
    TSID_EPOCH = 1704067200000  # 2024-01-01
    
    timestamp = int(time.time() * 1000) - TSID_EPOCH
    sequence = random.randint(0, 0x3FFF)
    
    # Pack into 64 bits
    value = ((timestamp & 0x3FFFFFFFFFF) << 22) | \
            ((node_id & 0xFF) << 14) | \
            (sequence & 0x3FFF)
    
    # Encode as base62
    BASE62 = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
    result = []
    while value > 0:
        value, remainder = divmod(value, 62)
        result.append(BASE62[remainder])
    
    return f"{prefix}{''.join(reversed(result))}"


# =============================================================================
# ID Analysis Utilities
# =============================================================================

def analyze_id(id_string: str) -> dict:
    """
    Analyze an ID string and determine its type.
    
    Args:
        id_string: ID to analyze
        
    Returns:
        Dictionary with type and properties
        
    Example:
        >>> analyze_id('aB3x9KmP')
        {'type': 'short_id', 'length': 8, ...}
    """
    result = {
        'string': id_string,
        'length': len(id_string),
        'type': 'unknown',
        'properties': {}
    }
    
    # Check for UUID
    if '-' in id_string and len(id_string) == 36:
        try:
            import uuid
            uuid.UUID(id_string)
            result['type'] = 'uuid'
            result['properties']['version'] = 'uuid4'  # Assume v4
        except ValueError:
            pass
    
    # Check for ObjectId
    if ObjectId.is_valid(id_string):
        result['type'] = 'objectid'
        try:
            ts = ObjectId.get_timestamp(id_string)
            result['properties']['timestamp'] = ts.isoformat()
        except:
            pass
    
    # Check for ULID
    if len(id_string) == 26 and all(c in ULID_ALPHABET for c in id_string.upper()):
        result['type'] = 'ulid'
        try:
            ts = ULID.get_timestamp(id_string)
            result['properties']['timestamp'] = ts.isoformat()
        except:
            pass
    
    # Check for numeric
    if id_string.isdigit():
        result['type'] = 'numeric'
        result['properties']['value'] = int(id_string)
    
    # Check for prefix pattern
    if '_' in id_string:
        parts = id_string.split('_', 1)
        if len(parts[0]) <= 10:  # Reasonable prefix length
            result['type'] = 'prefixed'
            result['properties']['prefix'] = parts[0]
    
    return result


# =============================================================================
# Convenience Functions
# =============================================================================

def uuid4_str() -> str:
    """Generate a standard UUID4 string."""
    import uuid
    return str(uuid.uuid4())


def uuid4_hex() -> str:
    """Generate a UUID4 as hex string (no dashes)."""
    import uuid
    return uuid.uuid4().hex


def uuid7_str() -> str:
    """
    Generate a UUID7 (time-ordered UUID).
    
    Uses Unix timestamp for time-ordered generation.
    """
    import uuid
    
    timestamp_ms = int(time.time() * 1000)
    
    # Create UUID with timestamp in first 48 bits
    # UUID v7 format: timestamp(48) + version(4) + rand_a(12) + variant(2) + rand_b(62)
    uuid_int = (timestamp_ms & 0xFFFFFFFFFFFF) << 80
    uuid_int |= (0b0111 << 76)  # Version 7
    uuid_int |= random.randint(0, (1 << 76) - 1) & ~(0xF << 76)  # Random bits
    
    return str(uuid.UUID(int=uuid_int))


# =============================================================================
# Exports
# =============================================================================

__all__ = [
    # Classes
    'SnowflakeGenerator',
    'ULID',
    'NanoID',
    'ObjectId',
    
    # Functions
    'short_id',
    'timestamp_id',
    'sequential_id',
    'prefixed_uuid',
    'ksuid',
    'cuid2',
    'tsid',
    'analyze_id',
    'uuid4_str',
    'uuid4_hex',
    'uuid7_str',
    
    # Constants
    'SNOWFLAKE_EPOCH',
    'ULID_ALPHABET',
    'NANO_ALPHABET',
]