"""
ULID (Universally Unique Lexicographically Sortable Identifier) Utils

A pure Python implementation of ULID - a 26-character, lexicographically 
sortable unique identifier that is URL-safe and uses Crockford's Base32 encoding.

Features:
- Generate ULIDs with timestamp component
- Parse ULIDs to extract timestamp and random components
- Validate ULIDs
- Convert between ULID and other formats (UUID, hex, bytes)
- Monotonic ULID generation (incrementing within same millisecond)

ULID Structure:
- 48 bits timestamp (milliseconds since Unix epoch)
- 80 bits randomness
- Total: 128 bits = 26 characters in Crockford's Base32

Example:
    >>> from ulid_utils import ULID
    >>> ulid = ULID.generate()
    >>> print(ulid)
    01ARZ3NDEKTSV4RRFFQ69G5FAV
    >>> ulid.timestamp()
    1505945976.341
"""

import time
import os
from datetime import datetime, timezone
from typing import Optional, Union
import struct

# Crockford's Base32 encoding (excludes I, L, O, U to avoid ambiguity)
CROCKFORD_ALPHABET = '0123456789ABCDEFGHJKMNPQRSTVWXYZ'
CROCKFORD_DECODE = {}
for i, char in enumerate(CROCKFORD_ALPHABET):
    CROCKFORD_DECODE[char] = i
    CROCKFORD_DECODE[char.lower()] = i

# Constants
ULID_LENGTH = 26
ULID_BYTES = 16
TIMESTAMP_BYTES = 6
RANDOMNESS_BYTES = 10


class ULIDError(ValueError):
    """Exception raised for ULID-related errors."""
    pass


class ULID:
    """
    ULID (Universally Unique Lexicographically Sortable Identifier) class.
    
    ULIDs are 26-character, lexicographically sortable unique identifiers
    that encode a timestamp and randomness component using Crockford's Base32.
    """
    
    __slots__ = ('_bytes',)
    
    def __init__(self, data: Union[bytes, str, 'ULID', None] = None):
        """
        Initialize a ULID instance.
        
        Args:
            data: Can be one of:
                - None: Generate a new ULID with current timestamp
                - bytes: 16-byte ULID representation
                - str: 26-character ULID string
                - ULID: Copy from another ULID instance
        """
        if data is None:
            self._bytes = self._generate_bytes()
        elif isinstance(data, ULID):
            self._bytes = data._bytes
        elif isinstance(data, bytes):
            if len(data) != ULID_BYTES:
                raise ULIDError(f"ULID bytes must be {ULID_BYTES} bytes, got {len(data)}")
            self._bytes = data
        elif isinstance(data, str):
            self._bytes = self._decode_str(data)
        else:
            raise ULIDError(f"Invalid ULID data type: {type(data)}")
    
    @staticmethod
    def _generate_bytes(timestamp_ms: Optional[int] = None,
                         randomness: Optional[bytes] = None) -> bytes:
        """Generate 16 bytes for ULID."""
        if timestamp_ms is None:
            timestamp_ms = int(time.time() * 1000)
        
        if timestamp_ms < 0 or timestamp_ms >= 2**48:
            raise ULIDError(f"Timestamp must be between 0 and 2^48-1, got {timestamp_ms}")
        
        if randomness is None:
            randomness = os.urandom(RANDOMNESS_BYTES)
        elif len(randomness) != RANDOMNESS_BYTES:
            raise ULIDError(f"Randomness must be {RANDOMNESS_BYTES} bytes, got {len(randomness)}")
        
        # Pack timestamp (6 bytes, big-endian)
        timestamp_bytes = struct.pack('>Q', timestamp_ms)[2:]
        
        return timestamp_bytes + randomness
    
    @staticmethod
    def _decode_str(ulid_str: str) -> bytes:
        """Decode a ULID string to 16 bytes."""
        if len(ulid_str) != ULID_LENGTH:
            raise ULIDError(f"ULID string must be {ULID_LENGTH} characters, got {len(ulid_str)}")
        
        # Validate characters and decode to 5-bit values
        values = []
        for char in ulid_str.upper():
            if char not in CROCKFORD_DECODE:
                raise ULIDError(f"Invalid ULID character: '{char}'")
            values.append(CROCKFORD_DECODE[char])
        
        # Convert 26 * 5 bits = 130 bits to 16 bytes = 128 bits
        # The encoding works like this:
        # First 10 characters encode the 6-byte timestamp (48 bits) + first 2 bits of randomness
        # Last 16 characters encode the remaining 80 bits of randomness
        
        # Alternative approach: treat it as 130 bits and drop the last 2 bits
        # Process 8 bits at a time
        
        result = bytearray(16)
        
        # Process character by character, accumulating bits
        # chars[0-1] -> first 2 bytes (10 bits -> 8 bits + 2 overflow)
        # chars[2-3] -> next 2 bytes
        # ... and so on
        
        # Byte index and bit tracking
        byte_idx = 0
        bit_accum = 0
        bit_count = 0
        
        for val in values:
            bit_accum = (bit_accum << 5) | val
            bit_count += 5
            
            while bit_count >= 8 and byte_idx < 16:
                bit_count -= 8
                result[byte_idx] = (bit_accum >> bit_count) & 0xFF
                byte_idx += 1
        
        # The remaining bits (should be 2) are dropped as they're overflow padding
        
        return bytes(result)
    
    def _encode_bytes(self) -> str:
        """Encode 16 bytes to ULID string."""
        result = []
        
        # Process bytes to 5-bit values
        bit_accum = 0
        bit_count = 0
        
        for byte in self._bytes:
            bit_accum = (bit_accum << 8) | byte
            bit_count += 8
            
            while bit_count >= 5:
                bit_count -= 5
                idx = (bit_accum >> bit_count) & 0x1F
                result.append(CROCKFORD_ALPHABET[idx])
        
        # Handle remaining 3 bits (pad with 2 zeros to make 5 bits)
        if bit_count > 0:
            idx = (bit_accum << (5 - bit_count)) & 0x1F
            result.append(CROCKFORD_ALPHABET[idx])
        
        return ''.join(result)
    
    @classmethod
    def generate(cls, timestamp_ms: Optional[int] = None) -> 'ULID':
        """Generate a new ULID."""
        bytes_data = cls._generate_bytes(timestamp_ms=timestamp_ms)
        return cls(bytes_data)
    
    @classmethod
    def from_datetime(cls, dt: datetime) -> 'ULID':
        """Create a ULID from a datetime object."""
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        timestamp_ms = int(dt.timestamp() * 1000)
        bytes_data = cls._generate_bytes(timestamp_ms=timestamp_ms)
        return cls(bytes_data)
    
    @classmethod
    def from_uuid(cls, uuid_obj) -> 'ULID':
        """Create a ULID from a UUID object."""
        return cls(uuid_obj.bytes)
    
    @classmethod
    def from_hex(cls, hex_str: str) -> 'ULID':
        """Create a ULID from a hexadecimal string."""
        hex_str = hex_str.lower()
        if hex_str.startswith('0x'):
            hex_str = hex_str[2:]
        if len(hex_str) != 32:
            raise ULIDError(f"Hex string must be 32 characters, got {len(hex_str)}")
        return cls(bytes.fromhex(hex_str))
    
    @classmethod
    def from_int(cls, value: int) -> 'ULID':
        """Create a ULID from an integer."""
        if value < 0 or value >= 2**128:
            raise ULIDError(f"Integer must be between 0 and 2^128-1")
        return cls(value.to_bytes(16, 'big'))
    
    @classmethod
    def parse(cls, ulid_str: str) -> 'ULID':
        """Parse a ULID string."""
        return cls(ulid_str)
    
    @classmethod
    def monotonic(cls, last: Optional['ULID'] = None) -> 'ULID':
        """Generate a monotonic ULID."""
        now_ms = int(time.time() * 1000)
        
        if last is None:
            return cls(cls._generate_bytes(timestamp_ms=now_ms))
        
        last_ms = last.timestamp_ms()
        
        if now_ms > last_ms:
            return cls(cls._generate_bytes(timestamp_ms=now_ms))
        
        if now_ms == last_ms:
            last_random = last.randomness()
            random_int = int.from_bytes(last_random, 'big') + 1
            
            if random_int >= 2**80:
                while int(time.time() * 1000) <= now_ms:
                    time.sleep(0.0001)
                return cls(cls._generate_bytes())
            
            new_random = random_int.to_bytes(RANDOMNESS_BYTES, 'big')
            return cls(cls._generate_bytes(timestamp_ms=now_ms, randomness=new_random))
        
        return cls(cls._generate_bytes(timestamp_ms=now_ms))
    
    def timestamp_ms(self) -> int:
        """Get the timestamp component in milliseconds."""
        return int.from_bytes(self._bytes[:TIMESTAMP_BYTES], 'big')
    
    def timestamp(self) -> float:
        """Get the timestamp component in seconds."""
        return self.timestamp_ms() / 1000.0
    
    def datetime(self) -> datetime:
        """Get the timestamp as a datetime object (UTC)."""
        return datetime.fromtimestamp(self.timestamp(), tz=timezone.utc)
    
    def randomness(self) -> bytes:
        """Get the randomness component (10 bytes)."""
        return self._bytes[TIMESTAMP_BYTES:]
    
    def bytes(self) -> bytes:
        """Get the 16-byte representation."""
        return self._bytes
    
    def hex(self) -> str:
        """Get the hexadecimal representation."""
        return self._bytes.hex()
    
    def to_uuid(self):
        """Convert to UUID object."""
        import uuid
        return uuid.UUID(bytes=self._bytes)
    
    def to_int(self) -> int:
        """Convert to integer."""
        return int.from_bytes(self._bytes, 'big')
    
    @classmethod
    def is_valid(cls, ulid_str: str) -> bool:
        """Check if a string is a valid ULID."""
        try:
            cls(ulid_str)
            return True
        except (ULIDError, ValueError):
            return False
    
    def __str__(self) -> str:
        return self._encode_bytes()
    
    def __repr__(self) -> str:
        return f"ULID('{self._encode_bytes()}')"
    
    def __bytes__(self) -> bytes:
        return self._bytes
    
    def __int__(self) -> int:
        return self.to_int()
    
    def __hash__(self) -> int:
        return hash(self._bytes)
    
    def __eq__(self, other) -> bool:
        if isinstance(other, ULID):
            return self._bytes == other._bytes
        if isinstance(other, str):
            try:
                return self._bytes == self._decode_str(other)
            except ULIDError:
                return False
        if isinstance(other, bytes):
            return self._bytes == other
        return NotImplemented
    
    def __lt__(self, other) -> bool:
        if isinstance(other, ULID):
            return self._bytes < other._bytes
        return NotImplemented
    
    def __le__(self, other) -> bool:
        if isinstance(other, ULID):
            return self._bytes <= other._bytes
        return NotImplemented
    
    def __gt__(self, other) -> bool:
        if isinstance(other, ULID):
            return self._bytes > other._bytes
        return NotImplemented
    
    def __ge__(self, other) -> bool:
        if isinstance(other, ULID):
            return self._bytes >= other._bytes
        return NotImplemented
    
    def __len__(self) -> int:
        return ULID_LENGTH


# Module-level convenience functions
def generate(timestamp_ms: Optional[int] = None) -> ULID:
    """Generate a new ULID."""
    bytes_data = ULID._generate_bytes(timestamp_ms=timestamp_ms)
    return ULID(bytes_data)


def parse(ulid_str: str) -> ULID:
    """Parse a ULID string."""
    return ULID(ulid_str)


def is_valid(ulid_str: str) -> bool:
    """Check if a string is a valid ULID."""
    return ULID.is_valid(ulid_str)


def monotonic(last: Optional[ULID] = None) -> ULID:
    """Generate a monotonic ULID."""
    return ULID.monotonic(last)


def from_datetime(dt: datetime) -> ULID:
    """Create a ULID from datetime."""
    return ULID.from_datetime(dt)


def from_uuid(uuid_obj) -> ULID:
    """Create a ULID from UUID."""
    return ULID.from_uuid(uuid_obj)


def from_hex(hex_str: str) -> ULID:
    """Create a ULID from hex string."""
    return ULID.from_hex(hex_str)


def from_int(value: int) -> ULID:
    """Create a ULID from integer."""
    return ULID.from_int(value)


# Batch generation
def generate_batch(count: int, timestamp_ms: Optional[int] = None) -> list:
    """Generate multiple ULIDs."""
    return [generate(timestamp_ms) for _ in range(count)]


def generate_monotonic_batch(count: int) -> list:
    """Generate a batch of monotonic ULIDs."""
    if count <= 0:
        return []
    
    result = [monotonic()]
    for _ in range(1, count):
        result.append(monotonic(result[-1]))
    return result


# Compare ULIDs
def compare(ulid1: ULID, ulid2: ULID) -> int:
    """Compare two ULIDs."""
    if ulid1 < ulid2:
        return -1
    elif ulid1 > ulid2:
        return 1
    return 0


def min_ulid(ulids: list) -> ULID:
    """Find the minimum ULID from a list."""
    return min(ulids, key=lambda u: u.bytes())


def max_ulid(ulids: list) -> ULID:
    """Find the maximum ULID from a list."""
    return max(ulids, key=lambda u: u.bytes())


def extract_timestamps(ulids: list) -> list:
    """Extract timestamps from a list of ULIDs."""
    return sorted([(u, u.timestamp_ms()) for u in ulids], key=lambda x: x[0])


if __name__ == "__main__":
    print("ULID Utils Demo")
    print("=" * 50)
    
    ulid = generate()
    print(f"Generated ULID: {ulid}")
    print(f"Timestamp (ms): {ulid.timestamp_ms()}")
    print(f"Datetime: {ulid.datetime()}")
    print(f"Hex: {ulid.hex()}")
    
    print("\n" + "=" * 50)
    print("Parse known ULID:")
    parsed = parse('01ARZ3NDEKTSV4RRFFQ69G5FAV')
    print(f"  Input: 01ARZ3NDEKTSV4RRFFQ69G5FAV")
    print(f"  Output: {parsed}")
    print(f"  Hex: {parsed.hex()}")
    print(f"  Timestamp: {parsed.datetime()}")
    
    print("\n" + "=" * 50)
    print("Monotonic ULIDs:")
    batch = generate_monotonic_batch(5)
    for u in batch:
        print(f"  {u}")