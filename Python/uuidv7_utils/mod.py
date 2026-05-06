"""
UUIDv7 Utils - UUIDv7 Generation and Utilities

UUIDv7 is a time-ordered UUID format defined in RFC 9562.
It combines a Unix timestamp with random bits, making it ideal for:
- Database primary keys (monotonically increasing)
- Distributed systems (no coordination needed)
- Sortable identifiers
- Time-based queries

Features:
- Zero external dependencies (pure Python stdlib)
- Thread-safe generation
- Multiple generation strategies
- Timestamp extraction and manipulation
- Batch generation support
- Conversion utilities

Author: AllToolkit
Version: 1.0.0
License: MIT
"""

import time
import secrets
import threading
import re
from typing import Optional, Union, List, Tuple
from datetime import datetime, timezone
from dataclasses import dataclass
from enum import Enum


class UUIDv7Strategy(Enum):
    """UUIDv7 generation strategies"""
    RANDOM = "random"           # Full random bits after timestamp
    MONOTONIC = "monotonic"      # Monotonically increasing within same millisecond
    SORTABLE = "sortable"        # Optimized for sorting performance


@dataclass
class UUIDv7Components:
    """Parsed components of a UUIDv7"""
    timestamp_ms: int
    version: int
    variant: int
    rand_a: int
    rand_b: int
    
    @property
    def datetime(self) -> datetime:
        """Get the datetime from timestamp"""
        return datetime.fromtimestamp(
            self.timestamp_ms / 1000.0, 
            tz=timezone.utc
        )


class UUIDv7:
    """
    UUIDv7 - Time-ordered UUID implementation
    
    Format (128 bits total, big-endian):
    Bits 0-47 (48 bits): Unix timestamp in milliseconds
    Bits 48-51 (4 bits): version = 7
    Bits 52-63 (12 bits): rand_a
    Bits 64-65 (2 bits): variant = 10
    Bits 66-127 (62 bits): rand_b
    
    Example:
        >>> uuid = UUIDv7.generate()
        >>> print(uuid)
        018f3b6a-1b2c-7d3e-8f4a-5b6c7d8e9f0a
        >>> uuid.timestamp
        1712534567890
        >>> uuid.datetime
        datetime.datetime(2024, 4, 7, 12, 42, 47, 890000, tzinfo=datetime.timezone.utc)
    """
    
    # Version and variant values
    VERSION = 7
    VARIANT = 0b10  # RFC 4122 variant
    
    def __init__(self, value: Optional[Union[int, str, bytes]] = None):
        """
        Initialize UUIDv7 from various formats.
        
        Args:
            value: UUID value as int, hex string, or bytes.
                   If None, generates a new UUIDv7.
        """
        if value is None:
            self._int = self._generate_int()
        elif isinstance(value, int):
            if value < 0 or value >= (1 << 128):
                raise ValueError("UUID value must be 128-bit unsigned integer")
            self._int = value
        elif isinstance(value, str):
            self._int = self._parse_hex(value)
        elif isinstance(value, bytes):
            if len(value) != 16:
                raise ValueError("UUID bytes must be exactly 16 bytes")
            self._int = int.from_bytes(value, 'big')
        else:
            raise TypeError(f"Cannot create UUIDv7 from {type(value)}")
    
    @staticmethod
    def _generate_int() -> int:
        """Generate a 128-bit integer for UUIDv7"""
        # Get current timestamp in milliseconds
        timestamp_ms = int(time.time() * 1000)
        
        # Generate random bits for rand_a (12 bits) and rand_b (62 bits) = 74 bits
        rand_bits = secrets.randbits(74)
        
        # Build UUIDv7:
        # Bytes layout (16 bytes = 128 bits):
        # Byte 0-5 (48 bits): timestamp_ms
        # Byte 6 (8 bits): version(4) + rand_a_high(4)
        # Byte 7 (8 bits): rand_a_low(8 bits, but we use as part of variant+rand_b)
        # Byte 8-15 (64 bits): variant(2) + rand_b(62)
        
        # Actually let's build it properly:
        # Bits 0-47: timestamp (48 bits)
        # Bits 48-51: version 7 (4 bits)
        # Bits 52-63: rand_a (12 bits)
        # Bits 64-65: variant 10 (2 bits)
        # Bits 66-127: rand_b (62 bits)
        
        result = 0
        
        # Timestamp: bits 0-47 (shift left 80 bits to occupy top 48 bits)
        result = (timestamp_ms & 0xFFFFFFFFFFFF) << 80
        
        # Version: bits 48-51 (value 7, shift left 76 bits)
        result |= (7 << 76)
        
        # rand_a: bits 52-63 (12 bits from random, shift left 64 bits)
        rand_a = (rand_bits >> 62) & 0xFFF
        result |= (rand_a << 64)
        
        # variant: bits 64-65 (value 2, shift left 62 bits)
        result |= (2 << 62)
        
        # rand_b: bits 66-127 (62 bits from random)
        rand_b = rand_bits & 0x3FFFFFFFFFFFFFFF
        result |= rand_b
        
        return result
    
    @staticmethod
    def _parse_hex(s: str) -> int:
        """Parse a hex string to UUID integer"""
        # Remove dashes and braces
        s = s.replace('-', '').replace('{', '').replace('}', '')
        
        # Handle urn:uuid: prefix
        if s.lower().startswith('urn:uuid:'):
            s = s[9:]
        
        if len(s) != 32:
            raise ValueError(f"Invalid UUID string length: {len(s)}")
        
        try:
            return int(s, 16)
        except ValueError:
            raise ValueError(f"Invalid hex string: {s}")
    
    @classmethod
    def generate(cls) -> 'UUIDv7':
        """
        Generate a new UUIDv7.
        
        Returns:
            New UUIDv7 instance
        """
        return cls(cls._generate_int())
    
    @classmethod
    def generate_monotonic(cls) -> 'UUIDv7':
        """
        Generate a monotonically increasing UUIDv7.
        Ensures UUIDs generated within the same millisecond are ordered.
        
        Returns:
            New UUIDv7 instance with monotonic guarantee
        """
        # Get class-level state
        if not hasattr(cls, '_class_last_timestamp'):
            cls._class_last_timestamp = 0
            cls._class_last_counter = 0
            cls._class_lock = threading.Lock()
        
        with cls._class_lock:
            timestamp_ms = int(time.time() * 1000)
            
            if timestamp_ms > cls._class_last_timestamp:
                cls._class_last_timestamp = timestamp_ms
                cls._class_last_counter = 0
            else:
                cls._class_last_counter += 1
                # Check for counter overflow (12 bits = 4096)
                if cls._class_last_counter > 0xFFF:
                    # Wait for next millisecond
                    while int(time.time() * 1000) <= timestamp_ms:
                        time.sleep(0.0001)
                    return cls.generate_monotonic()
            
            counter = cls._class_last_counter
            rand_b = secrets.randbits(62)
            
            result = (timestamp_ms & 0xFFFFFFFFFFFF) << 80
            result |= (7 << 76)  # version
            result |= (counter << 64)  # rand_a as counter
            result |= (2 << 62)  # variant
            result |= rand_b
            
            return cls(result)
    
    @classmethod
    def from_timestamp(cls, timestamp_ms: int, random_bits: Optional[int] = None) -> 'UUIDv7':
        """
        Create a UUIDv7 from a specific timestamp.
        
        Args:
            timestamp_ms: Unix timestamp in milliseconds
            random_bits: Optional 74-bit random value (auto-generated if None)
            
        Returns:
            UUIDv7 with the specified timestamp
        """
        if timestamp_ms < 0 or timestamp_ms >= (1 << 48):
            raise ValueError("Timestamp must be a 48-bit unsigned integer")
        
        if random_bits is None:
            random_bits = secrets.randbits(74)
        elif random_bits < 0 or random_bits >= (1 << 74):
            raise ValueError("Random bits must be a 74-bit unsigned integer")
        
        rand_a = (random_bits >> 62) & 0xFFF
        rand_b = random_bits & 0x3FFFFFFFFFFFFFFF
        
        result = (timestamp_ms & 0xFFFFFFFFFFFF) << 80
        result |= (7 << 76)  # version
        result |= (rand_a << 64)
        result |= (2 << 62)  # variant
        result |= rand_b
        
        return cls(result)
    
    @classmethod
    def from_datetime(cls, dt: datetime) -> 'UUIDv7':
        """
        Create a UUIDv7 from a datetime object.
        
        Args:
            dt: datetime object (will be converted to UTC if naive)
            
        Returns:
            UUIDv7 with the specified datetime
        """
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        timestamp_ms = int(dt.timestamp() * 1000)
        return cls.from_timestamp(timestamp_ms)
    
    @property
    def int(self) -> int:
        """Get the UUID as an integer"""
        return self._int
    
    @property
    def bytes(self) -> bytes:
        """Get the UUID as 16 bytes (big-endian)"""
        return self._int.to_bytes(16, 'big')
    
    @property
    def hex(self) -> str:
        """Get the UUID as 32-character hex string (no dashes)"""
        return f'{self._int:032x}'
    
    @property
    def urn(self) -> str:
        """Get the UUID as URN (urn:uuid:...)"""
        return f'urn:uuid:{str(self)}'
    
    @property
    def timestamp(self) -> int:
        """Get the Unix timestamp in milliseconds (bits 0-47)"""
        return (self._int >> 80) & 0xFFFFFFFFFFFF
    
    @property
    def datetime(self) -> datetime:
        """Get the datetime representation of the timestamp"""
        return datetime.fromtimestamp(self.timestamp / 1000.0, tz=timezone.utc)
    
    @property
    def version(self) -> int:
        """Get the UUID version (bits 48-51)"""
        return (self._int >> 76) & 0xF
    
    @property
    def variant(self) -> int:
        """Get the UUID variant (bits 64-65)"""
        return (self._int >> 62) & 0x3
    
    @property
    def rand_a(self) -> int:
        """Get rand_a field (bits 52-63)"""
        return (self._int >> 64) & 0xFFF
    
    @property
    def rand_b(self) -> int:
        """Get rand_b field (bits 66-127)"""
        return self._int & 0x3FFFFFFFFFFFFFFF
    
    @property
    def components(self) -> UUIDv7Components:
        """Get parsed components of the UUID"""
        return UUIDv7Components(
            timestamp_ms=self.timestamp,
            version=self.version,
            variant=self.variant,
            rand_a=self.rand_a,
            rand_b=self.rand_b
        )
    
    def __str__(self) -> str:
        """Standard UUID format: xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"""
        h = self.hex
        return f'{h[0:8]}-{h[8:12]}-{h[12:16]}-{h[16:20]}-{h[20:32]}'
    
    def __repr__(self) -> str:
        return f'UUIDv7(\'{str(self)}\')'
    
    def __int__(self) -> int:
        return self._int
    
    def __bytes__(self) -> bytes:
        return self.bytes
    
    def __hash__(self) -> int:
        return self._int
    
    def __eq__(self, other: object) -> bool:
        if isinstance(other, UUIDv7):
            return self._int == other._int
        if isinstance(other, str):
            try:
                return self._int == self._parse_hex(other)
            except ValueError:
                return False
        if isinstance(other, int):
            return self._int == other
        return NotImplemented
    
    def __lt__(self, other: 'UUIDv7') -> bool:
        if isinstance(other, UUIDv7):
            return self._int < other._int
        return NotImplemented
    
    def __le__(self, other: 'UUIDv7') -> bool:
        if isinstance(other, UUIDv7):
            return self._int <= other._int
        return NotImplemented
    
    def __gt__(self, other: 'UUIDv7') -> bool:
        if isinstance(other, UUIDv7):
            return self._int > other._int
        return NotImplemented
    
    def __ge__(self, other: 'UUIDv7') -> bool:
        if isinstance(other, UUIDv7):
            return self._int >= other._int
        return NotImplemented
    
    def __bool__(self) -> bool:
        return True
    
    def __format__(self, format_spec: str) -> str:
        """Format the UUID according to format spec"""
        if format_spec == 'x':
            return self.hex
        elif format_spec == 'X':
            return self.hex.upper()
        elif format_spec == 's':
            return str(self)
        elif format_spec == 'n':
            return self.hex  # No dashes
        elif format_spec == 'b':
            return self.bytes.hex()
        elif format_spec == 'B':
            return repr(self.bytes)
        elif format_spec == 'u':
            return self.urn
        else:
            return str(self)


class UUIDv7Generator:
    """
    Thread-safe UUIDv7 generator with monotonic guarantee.
    
    This class maintains internal state to ensure that all UUIDs
    generated within the same millisecond are monotonically increasing.
    
    Example:
        >>> gen = UUIDv7Generator()
        >>> uuid1 = gen.generate()
        >>> uuid2 = gen.generate()
        >>> assert uuid1 < uuid2  # Always true
    """
    
    def __init__(self, node_id: Optional[int] = None):
        """
        Initialize the generator.
        
        Args:
            node_id: Optional 10-bit node identifier (0-1023)
                    If provided, embedded in rand_a for distributed systems
        """
        self._lock = threading.Lock()
        self._last_timestamp_ms = 0
        self._last_counter = 0
        
        if node_id is not None:
            if node_id < 0 or node_id > 0x3FF:
                raise ValueError("Node ID must be a 10-bit integer (0-1023)")
        self._node_id = node_id
    
    def generate(self) -> UUIDv7:
        """
        Generate a new monotonically increasing UUIDv7.
        
        Returns:
            New UUIDv7 instance
        """
        with self._lock:
            timestamp_ms = int(time.time() * 1000)
            
            if timestamp_ms > self._last_timestamp_ms:
                # New millisecond, reset counter
                self._last_timestamp_ms = timestamp_ms
                self._last_counter = 0
            else:
                # Same millisecond, increment counter
                self._last_counter += 1
                
                # Check for counter overflow (12 bits = 4096)
                if self._last_counter > 0xFFF:
                    # Wait for next millisecond
                    while int(time.time() * 1000) <= timestamp_ms:
                        time.sleep(0.0001)  # Sleep 0.1ms
                    return self.generate()
            
            return self._build_uuid(timestamp_ms, self._last_counter)
    
    def _build_uuid(self, timestamp_ms: int, counter: int) -> UUIDv7:
        """Build a UUIDv7 from timestamp and counter"""
        # Random bits for rand_b (62 bits)
        rand_b = secrets.randbits(62)
        
        # Build rand_a
        if self._node_id is not None:
            # Use node_id in upper 10 bits, counter in lower 2 bits
            rand_a = (self._node_id << 2) | (counter & 0x3)
        else:
            rand_a = counter
        
        # Build UUID
        result = (timestamp_ms & 0xFFFFFFFFFFFF) << 80
        result |= (7 << 76)  # version
        result |= (rand_a << 64)
        result |= (2 << 62)  # variant
        result |= rand_b
        
        return UUIDv7(result)
    
    def generate_batch(self, count: int) -> List[UUIDv7]:
        """
        Generate multiple UUIDv7s in a batch.
        
        Args:
            count: Number of UUIDs to generate
            
        Returns:
            List of UUIDv7 instances
        """
        return [self.generate() for _ in range(count)]


class UUIDv7Validator:
    """UUIDv7 validation utilities"""
    
    # Regex pattern for UUID format
    UUID_PATTERN = re.compile(
        r'^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$',
        re.IGNORECASE
    )
    
    @classmethod
    def is_valid_uuid(cls, value: str) -> bool:
        """Check if string is a valid UUID format"""
        return bool(cls.UUID_PATTERN.match(value))
    
    @classmethod
    def is_uuidv7(cls, value: Union[str, UUIDv7]) -> bool:
        """Check if value is a valid UUIDv7"""
        try:
            if isinstance(value, UUIDv7):
                return value.version == 7
            uuid = UUIDv7(value)
            return uuid.version == 7
        except (ValueError, TypeError):
            return False
    
    @classmethod
    def validate(cls, value: Union[str, UUIDv7]) -> UUIDv7:
        """Validate and return UUIDv7, or raise ValueError"""
        if isinstance(value, UUIDv7):
            if value.version != 7:
                raise ValueError(f"Not a UUIDv7 (version {value.version})")
            return value
        
        if not cls.is_valid_uuid(value):
            raise ValueError(f"Invalid UUID format: {value}")
        
        uuid = UUIDv7(value)
        if uuid.version != 7:
            raise ValueError(f"Not a UUIDv7 (version {uuid.version})")
        
        return uuid


class UUIDv7Set:
    """
    A set-like collection for UUIDv7 with efficient storage and operations.
    
    Internally stores UUIDs as integers for memory efficiency.
    
    Example:
        >>> uuid_set = UUIDv7Set()
        >>> uuid = UUIDv7.generate()
        >>> uuid_set.add(uuid)
        >>> uuid in uuid_set
        True
    """
    
    def __init__(self, uuids: Optional[List[UUIDv7]] = None):
        self._set: set = set()
        if uuids:
            for uuid in uuids:
                self.add(uuid)
    
    def add(self, uuid: UUIDv7) -> None:
        """Add a UUID to the set"""
        self._set.add(uuid.int)
    
    def remove(self, uuid: UUIDv7) -> None:
        """Remove a UUID from the set"""
        self._set.remove(uuid.int)
    
    def discard(self, uuid: UUIDv7) -> None:
        """Remove a UUID if present"""
        self._set.discard(uuid.int)
    
    def __contains__(self, uuid: UUIDv7) -> bool:
        return uuid.int in self._set
    
    def __len__(self) -> int:
        return len(self._set)
    
    def __iter__(self):
        for i in self._set:
            yield UUIDv7(i)
    
    def __repr__(self) -> str:
        return f'UUIDv7Set({len(self)} UUIDs)'
    
    def to_list(self) -> List[UUIDv7]:
        """Convert to list of UUIDv7"""
        return list(self)
    
    def to_hex_list(self) -> List[str]:
        """Convert to list of hex strings"""
        return [uuid.hex for uuid in self]
    
    def to_str_list(self) -> List[str]:
        """Convert to list of string representations"""
        return [str(uuid) for uuid in self]


class UUIDv7Range:
    """
    A range of UUIDv7s defined by timestamp bounds.
    
    Useful for time-based queries and filtering.
    
    Example:
        >>> start_time = datetime(2024, 1, 1, tzinfo=timezone.utc)
        >>> end_time = datetime(2024, 1, 2, tzinfo=timezone.utc)
        >>> range_ = UUIDv7Range.from_datetime_range(start_time, end_time)
        >>> uuid = UUIDv7.generate()
        >>> uuid in range_
        False  # Generated now, not in 2024
    """
    
    def __init__(self, start_ms: int, end_ms: int):
        if start_ms > end_ms:
            raise ValueError("Start must be <= end")
        self.start_ms = start_ms
        self.end_ms = end_ms
    
    @classmethod
    def from_datetime_range(cls, start: datetime, end: datetime) -> 'UUIDv7Range':
        """Create range from datetime objects"""
        if start.tzinfo is None:
            start = start.replace(tzinfo=timezone.utc)
        if end.tzinfo is None:
            end = end.replace(tzinfo=timezone.utc)
        
        start_ms = int(start.timestamp() * 1000)
        end_ms = int(end.timestamp() * 1000)
        return cls(start_ms, end_ms)
    
    @classmethod
    def from_timestamp(cls, timestamp_ms: int, duration_ms: int) -> 'UUIDv7Range':
        """Create range from timestamp and duration"""
        return cls(timestamp_ms, timestamp_ms + duration_ms)
    
    @classmethod
    def last_hours(cls, hours: int) -> 'UUIDv7Range':
        """Create range for the last N hours"""
        now_ms = int(time.time() * 1000)
        return cls(now_ms - hours * 3600 * 1000, now_ms)
    
    @classmethod
    def last_days(cls, days: int) -> 'UUIDv7Range':
        """Create range for the last N days"""
        now_ms = int(time.time() * 1000)
        return cls(now_ms - days * 24 * 3600 * 1000, now_ms)
    
    def __contains__(self, uuid: UUIDv7) -> bool:
        return self.start_ms <= uuid.timestamp <= self.end_ms
    
    def __repr__(self) -> str:
        start_dt = datetime.fromtimestamp(self.start_ms / 1000, tz=timezone.utc)
        end_dt = datetime.fromtimestamp(self.end_ms / 1000, tz=timezone.utc)
        return f'UUIDv7Range({start_dt} to {end_dt})'
    
    @property
    def duration_ms(self) -> int:
        """Get duration in milliseconds"""
        return self.end_ms - self.start_ms
    
    @property
    def duration_seconds(self) -> float:
        """Get duration in seconds"""
        return self.duration_ms / 1000.0
    
    def start_datetime(self) -> datetime:
        """Get start as datetime"""
        return datetime.fromtimestamp(self.start_ms / 1000, tz=timezone.utc)
    
    def end_datetime(self) -> datetime:
        """Get end as datetime"""
        return datetime.fromtimestamp(self.end_ms / 1000, tz=timezone.utc)


# Convenience functions
def generate() -> UUIDv7:
    """Generate a new UUIDv7"""
    return UUIDv7.generate()


def generate_monotonic() -> UUIDv7:
    """Generate a monotonically increasing UUIDv7"""
    return UUIDv7.generate_monotonic()


def generate_batch(count: int, monotonic: bool = True) -> List[UUIDv7]:
    """
    Generate multiple UUIDv7s.
    
    Args:
        count: Number of UUIDs to generate
        monotonic: If True, guarantees monotonically increasing order
        
    Returns:
        List of UUIDv7 instances
    """
    if monotonic:
        gen = UUIDv7Generator()
        return gen.generate_batch(count)
    return [UUIDv7.generate() for _ in range(count)]


def parse(value: Union[str, int, bytes]) -> UUIDv7:
    """Parse a value to UUIDv7"""
    return UUIDv7(value)


def is_uuidv7(value: Union[str, UUIDv7]) -> bool:
    """Check if value is a valid UUIDv7"""
    return UUIDv7Validator.is_uuidv7(value)


def from_timestamp(timestamp_ms: int) -> UUIDv7:
    """Create UUIDv7 from Unix timestamp in milliseconds"""
    return UUIDv7.from_timestamp(timestamp_ms)


def from_datetime(dt: datetime) -> UUIDv7:
    """Create UUIDv7 from datetime"""
    return UUIDv7.from_datetime(dt)


# Module-level generator for monotonic generation
_generator = UUIDv7Generator()


def get_generator() -> UUIDv7Generator:
    """Get the module-level UUIDv7 generator"""
    return _generator