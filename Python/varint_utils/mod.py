"""
Varint (Variable-Length Integer) Utils Module

This module provides functions for encoding and decoding variable-length integers.
Varint encoding is a compact way to store integers, especially when most values are small.
It's widely used in Protocol Buffers, databases, and network protocols.

Key features:
- Support for unsigned varints (1-10 bytes for 64-bit integers)
- Support for signed varints with ZigZag encoding
- Batch encoding/decoding for efficiency
- Streaming support for large datasets
- Zero external dependencies
"""

from typing import List, Tuple, Iterator, Optional
from functools import reduce


# Constants
MAX_UINT64 = (1 << 64) - 1
MAX_INT64 = (1 << 63) - 1
MIN_INT64 = -(1 << 63)

# Continuation bit (MSB)
CONTINUATION_BIT = 0x80
# Lower 7 bits mask
VALUE_MASK = 0x7F


class VarintError(Exception):
    """Base exception for varint utilities."""
    pass


class VarintOverflowError(VarintError):
    """Raised when varint exceeds maximum size."""
    pass


class VarintDecodeError(VarintError):
    """Raised when varint decoding fails."""
    pass


# ============================================================================
# Unsigned Varint Encoding/Decoding
# ============================================================================

def encode_unsigned(value: int) -> bytes:
    """
    Encode an unsigned integer as a varint.
    
    Args:
        value: Unsigned integer to encode (0 <= value <= 2^64-1)
    
    Returns:
        Encoded varint bytes
    
    Raises:
        VarintError: If value is negative or too large
    
    Examples:
        >>> encode_unsigned(0)
        b'\\x00'
        >>> encode_unsigned(1)
        b'\\x01'
        >>> encode_unsigned(300)
        b'\\xac\\x02'
        >>> encode_unsigned(128)
        b'\\x80\\x01'
    """
    if value < 0:
        raise VarintError(f"Cannot encode negative value as unsigned varint: {value}")
    if value > MAX_UINT64:
        raise VarintError(f"Value exceeds maximum uint64: {value}")
    
    result = bytearray()
    while value > VALUE_MASK:
        result.append((value & VALUE_MASK) | CONTINUATION_BIT)
        value >>= 7
    result.append(value)
    return bytes(result)


def decode_unsigned(data: bytes, offset: int = 0) -> Tuple[int, int]:
    """
    Decode an unsigned varint from bytes.
    
    Args:
        data: Bytes containing encoded varint
        offset: Starting position in bytes (default: 0)
    
    Returns:
        Tuple of (decoded value, number of bytes consumed)
    
    Raises:
        VarintDecodeError: If data is invalid or incomplete
        VarintOverflowError: If varint exceeds 64 bits
    
    Examples:
        >>> decode_unsigned(b'\\x00')
        (0, 1)
        >>> decode_unsigned(b'\\xac\\x02')
        (300, 2)
        >>> decode_unsigned(b'\\x80\\x01')
        (128, 2)
    """
    if not data or offset >= len(data):
        raise VarintDecodeError("Empty data or invalid offset")
    
    result = 0
    shift = 0
    bytes_consumed = 0
    
    for i in range(offset, min(offset + 10, len(data))):
        byte = data[i]
        bytes_consumed += 1
        
        # Extract lower 7 bits and add to result
        result |= (byte & VALUE_MASK) << shift
        
        # Check if this is the last byte (MSB not set)
        if not (byte & CONTINUATION_BIT):
            return result, bytes_consumed
        
        shift += 7
        
        # Check for overflow (>10 bytes for uint64)
        if bytes_consumed >= 10:
            # The 10th byte should only use 1 bit for uint64
            if shift >= 64:
                raise VarintOverflowError("Varint exceeds 64 bits")
    
    raise VarintDecodeError("Incomplete varint: missing termination byte")


def encode_unsigned_batch(values: List[int]) -> bytes:
    """
    Encode multiple unsigned integers as concatenated varints.
    
    Args:
        values: List of unsigned integers to encode
    
    Returns:
        Concatenated encoded varint bytes
    
    Examples:
        >>> encode_unsigned_batch([1, 2, 300])
        b'\\x01\\x02\\xac\\x02'
    """
    return b''.join(encode_unsigned(v) for v in values)


def decode_unsigned_batch(data: bytes, count: Optional[int] = None) -> List[int]:
    """
    Decode multiple unsigned varints from bytes.
    
    Args:
        data: Bytes containing encoded varints
        count: Number of values to decode (None = decode all)
    
    Returns:
        List of decoded values
    
    Raises:
        VarintDecodeError: If decoding fails or count doesn't match
    
    Examples:
        >>> decode_unsigned_batch(b'\\x01\\x02\\xac\\x02')
        [1, 2, 300]
        >>> decode_unsigned_batch(b'\\x01\\x02\\xac\\x02', count=2)
        [1, 2]
    """
    values = []
    offset = 0
    
    while offset < len(data):
        if count is not None and len(values) >= count:
            break
        
        value, consumed = decode_unsigned(data, offset)
        values.append(value)
        offset += consumed
    
    if count is not None and len(values) != count:
        raise VarintDecodeError(f"Expected {count} values, got {len(values)}")
    
    return values


# ============================================================================
# ZigZag Encoding/Decoding (for signed integers)
# ============================================================================

def zigzag_encode(value: int) -> int:
    """
    Encode a signed integer using ZigZag encoding.
    
    ZigZag encoding maps signed integers to unsigned integers so that
    numbers with small absolute values have small encoded values.
    
    Mapping:
        0 -> 0
        -1 -> 1
        1 -> 2
        -2 -> 3
        2 -> 4
        ...
    
    Args:
        value: Signed integer to encode
    
    Returns:
        ZigZag-encoded unsigned integer
    
    Examples:
        >>> zigzag_encode(0)
        0
        >>> zigzag_encode(-1)
        1
        >>> zigzag_encode(1)
        2
        >>> zigzag_encode(-2)
        3
        >>> zigzag_encode(2147483647)
        4294967294
    """
    # Use 64-bit ZigZag encoding
    if value >= 0:
        return value << 1
    else:
        return ((-value - 1) << 1) | 1


def zigzag_decode(value: int) -> int:
    """
    Decode a ZigZag-encoded integer back to signed integer.
    
    Args:
        value: ZigZag-encoded unsigned integer
    
    Returns:
        Original signed integer
    
    Examples:
        >>> zigzag_decode(0)
        0
        >>> zigzag_decode(1)
        -1
        >>> zigzag_decode(2)
        1
        >>> zigzag_decode(3)
        -2
    """
    return (value >> 1) ^ -(value & 1)


# ============================================================================
# Signed Varint Encoding/Decoding
# ============================================================================

def encode_signed(value: int) -> bytes:
    """
    Encode a signed integer as a varint using ZigZag encoding.
    
    This is ideal for values that are typically close to zero,
    as negative numbers don't expand to 10 bytes.
    
    Args:
        value: Signed integer to encode
    
    Returns:
        Encoded varint bytes
    
    Raises:
        VarintError: If value exceeds 64-bit range
    
    Examples:
        >>> encode_signed(0)
        b'\\x00'
        >>> encode_signed(-1)
        b'\\x01'
        >>> encode_signed(1)
        b'\\x02'
        >>> encode_signed(-2)
        b'\\x03'
    """
    if value < MIN_INT64 or value > MAX_INT64:
        raise VarintError(f"Value exceeds int64 range: {value}")
    
    zigzag_value = zigzag_encode(value)
    return encode_unsigned(zigzag_value)


def decode_signed(data: bytes, offset: int = 0) -> Tuple[int, int]:
    """
    Decode a signed varint (with ZigZag encoding) from bytes.
    
    Args:
        data: Bytes containing encoded varint
        offset: Starting position in bytes (default: 0)
    
    Returns:
        Tuple of (decoded signed value, bytes consumed)
    
    Examples:
        >>> decode_signed(b'\\x00')
        (0, 1)
        >>> decode_signed(b'\\x01')
        (-1, 1)
        >>> decode_signed(b'\\x02')
        (1, 1)
    """
    unsigned_value, consumed = decode_unsigned(data, offset)
    signed_value = zigzag_decode(unsigned_value)
    return signed_value, consumed


def encode_signed_batch(values: List[int]) -> bytes:
    """
    Encode multiple signed integers as concatenated varints.
    
    Args:
        values: List of signed integers to encode
    
    Returns:
        Concatenated encoded varint bytes
    
    Examples:
        >>> encode_signed_batch([0, -1, 1, -2])
        b'\\x00\\x01\\x02\\x03'
    """
    return b''.join(encode_signed(v) for v in values)


def decode_signed_batch(data: bytes, count: Optional[int] = None) -> List[int]:
    """
    Decode multiple signed varints from bytes.
    
    Args:
        data: Bytes containing encoded varints
        count: Number of values to decode (None = decode all)
    
    Returns:
        List of decoded signed values
    
    Examples:
        >>> decode_signed_batch(b'\\x00\\x01\\x02\\x03')
        [0, -1, 1, -2]
    """
    values = []
    offset = 0
    
    while offset < len(data):
        if count is not None and len(values) >= count:
            break
        
        value, consumed = decode_signed(data, offset)
        values.append(value)
        offset += consumed
    
    if count is not None and len(values) != count:
        raise VarintDecodeError(f"Expected {count} values, got {len(values)}")
    
    return values


# ============================================================================
# Streaming Support
# ============================================================================

class VarintWriter:
    """
    A streaming writer for varints.
    
    Useful for writing large numbers of varints to a file or buffer
    without holding all values in memory.
    
    Examples:
        >>> writer = VarintWriter()
        >>> writer.write_unsigned(1)
        >>> writer.write_unsigned(300)
        >>> writer.write_signed(-42)
        >>> data = writer.get_bytes()
    """
    
    def __init__(self):
        self._buffer = bytearray()
    
    def write_unsigned(self, value: int) -> 'VarintWriter':
        """Write an unsigned varint."""
        self._buffer.extend(encode_unsigned(value))
        return self
    
    def write_signed(self, value: int) -> 'VarintWriter':
        """Write a signed varint (ZigZag encoded)."""
        self._buffer.extend(encode_signed(value))
        return self
    
    def write_unsigned_batch(self, values: List[int]) -> 'VarintWriter':
        """Write multiple unsigned varints."""
        for v in values:
            self.write_unsigned(v)
        return self
    
    def write_signed_batch(self, values: List[int]) -> 'VarintWriter':
        """Write multiple signed varints."""
        for v in values:
            self.write_signed(v)
        return self
    
    def get_bytes(self) -> bytes:
        """Get all written bytes."""
        return bytes(self._buffer)
    
    def clear(self) -> None:
        """Clear the buffer."""
        self._buffer.clear()
    
    def __len__(self) -> int:
        """Return the number of bytes written."""
        return len(self._buffer)


class VarintReader:
    """
    A streaming reader for varints.
    
    Useful for reading large numbers of varints from bytes
    without decoding all at once.
    
    Examples:
        >>> data = encode_unsigned_batch([1, 300, 128])
        >>> reader = VarintReader(data)
        >>> list(reader.read_unsigned_all())
        [1, 300, 128]
    """
    
    def __init__(self, data: bytes):
        self._data = data
        self._offset = 0
    
    def has_more(self) -> bool:
        """Check if there's more data to read."""
        return self._offset < len(self._data)
    
    def read_unsigned(self) -> int:
        """Read next unsigned varint."""
        if not self.has_more():
            raise VarintDecodeError("No more data to read")
        
        value, consumed = decode_unsigned(self._data, self._offset)
        self._offset += consumed
        return value
    
    def read_signed(self) -> int:
        """Read next signed varint."""
        if not self.has_more():
            raise VarintDecodeError("No more data to read")
        
        value, consumed = decode_signed(self._data, self._offset)
        self._offset += consumed
        return value
    
    def read_unsigned_batch(self, count: int) -> List[int]:
        """Read multiple unsigned varints."""
        values = []
        for _ in range(count):
            if not self.has_more():
                raise VarintDecodeError(f"Expected {count} values, got {len(values)}")
            values.append(self.read_unsigned())
        return values
    
    def read_signed_batch(self, count: int) -> List[int]:
        """Read multiple signed varints."""
        values = []
        for _ in range(count):
            if not self.has_more():
                raise VarintDecodeError(f"Expected {count} values, got {len(values)}")
            values.append(self.read_signed())
        return values
    
    def read_unsigned_all(self) -> Iterator[int]:
        """Iterate over all unsigned varints."""
        while self.has_more():
            yield self.read_unsigned()
    
    def read_signed_all(self) -> Iterator[int]:
        """Iterate over all signed varints."""
        while self.has_more():
            yield self.read_signed()
    
    def bytes_read(self) -> int:
        """Return the number of bytes read."""
        return self._offset
    
    def bytes_remaining(self) -> int:
        """Return the number of bytes remaining."""
        return len(self._data) - self._offset
    
    def reset(self) -> None:
        """Reset to the beginning."""
        self._offset = 0


# ============================================================================
# Utility Functions
# ============================================================================

def size_unsigned(value: int) -> int:
    """
    Calculate the byte size needed to encode an unsigned integer.
    
    Args:
        value: Unsigned integer to measure
    
    Returns:
        Number of bytes needed
    
    Examples:
        >>> size_unsigned(0)
        1
        >>> size_unsigned(127)
        1
        >>> size_unsigned(128)
        2
        >>> size_unsigned(16383)
        2
        >>> size_unsigned(16384)
        3
    """
    if value < 0:
        raise VarintError(f"Cannot measure size of negative value: {value}")
    
    if value == 0:
        return 1
    
    size = 0
    while value > 0:
        size += 1
        value >>= 7
    return size


def size_signed(value: int) -> int:
    """
    Calculate the byte size needed to encode a signed integer.
    
    Args:
        value: Signed integer to measure
    
    Returns:
        Number of bytes needed
    
    Examples:
        >>> size_signed(0)
        1
        >>> size_signed(-1)
        1
        >>> size_signed(63)
        1
        >>> size_signed(-64)
        1
        >>> size_signed(64)
        2
    """
    zigzag_value = zigzag_encode(value)
    return size_unsigned(zigzag_value)


def estimate_size_unsigned(values: List[int]) -> int:
    """
    Estimate total byte size for encoding multiple unsigned integers.
    
    Args:
        values: List of unsigned integers
    
    Returns:
        Total number of bytes needed
    
    Examples:
        >>> estimate_size_unsigned([0, 127, 128])
        4
    """
    return sum(size_unsigned(v) for v in values)


def estimate_size_signed(values: List[int]) -> int:
    """
    Estimate total byte size for encoding multiple signed integers.
    
    Args:
        values: List of signed integers
    
    Returns:
        Total number of bytes needed
    
    Examples:
        >>> estimate_size_signed([0, -1, 1, -2])
        4
    """
    return sum(size_signed(v) for v in values)


def compare_efficiency(values: List[int]) -> dict:
    """
    Compare fixed-size encoding vs varint encoding efficiency.
    
    Args:
        values: List of signed integers
    
    Returns:
        Dictionary with comparison metrics
    
    Examples:
        >>> result = compare_efficiency([0, 1, 2, 3, 4, 5])
        >>> result['varint_size']
        6
        >>> result['fixed_size']
        48  # 6 values * 8 bytes
        >>> result['compression_ratio']
        0.125
    """
    varint_size = estimate_size_signed(values)
    fixed_size = len(values) * 8  # Assuming 64-bit fixed encoding
    
    return {
        'value_count': len(values),
        'varint_size': varint_size,
        'fixed_size': fixed_size,
        'bytes_saved': fixed_size - varint_size,
        'compression_ratio': varint_size / fixed_size if fixed_size > 0 else 0,
        'avg_varint_size': varint_size / len(values) if values else 0
    }


# ============================================================================
# Specialized Encoders
# ============================================================================

def encode_int32(value: int) -> bytes:
    """
    Encode a 32-bit signed integer (Protocol Buffers style).
    
    Uses ZigZag + Varint encoding, producing 1-5 bytes.
    
    Args:
        value: 32-bit signed integer
    
    Returns:
        Encoded bytes (1-5 bytes)
    """
    if value < -(1 << 31) or value > (1 << 31) - 1:
        raise VarintError(f"Value out of int32 range: {value}")
    
    # ZigZag encode then varint encode
    zigzag = (value << 1) ^ (value >> 31)
    return encode_unsigned(zigzag)


def decode_int32(data: bytes, offset: int = 0) -> Tuple[int, int]:
    """
    Decode a 32-bit signed integer.
    
    Args:
        data: Encoded bytes
        offset: Starting position
    
    Returns:
        Tuple of (decoded value, bytes consumed)
    """
    unsigned, consumed = decode_unsigned(data, offset)
    # ZigZag decode
    value = (unsigned >> 1) ^ -(unsigned & 1)
    
    # Ensure it's in int32 range
    if value < -(1 << 31) or value > (1 << 31) - 1:
        raise VarintOverflowError(f"Decoded value out of int32 range: {value}")
    
    return value, consumed


def encode_int64(value: int) -> bytes:
    """
    Encode a 64-bit signed integer (Protocol Buffers style).
    
    Uses ZigZag + Varint encoding, producing 1-10 bytes.
    
    Args:
        value: 64-bit signed integer
    
    Returns:
        Encoded bytes (1-10 bytes)
    """
    return encode_signed(value)


def decode_int64(data: bytes, offset: int = 0) -> Tuple[int, int]:
    """
    Decode a 64-bit signed integer.
    
    Args:
        data: Encoded bytes
        offset: Starting position
    
    Returns:
        Tuple of (decoded value, bytes consumed)
    """
    return decode_signed(data, offset)


def encode_uint32(value: int) -> bytes:
    """
    Encode a 32-bit unsigned integer.
    
    Produces 1-5 bytes.
    
    Args:
        value: 32-bit unsigned integer
    
    Returns:
        Encoded bytes (1-5 bytes)
    """
    if value > (1 << 32) - 1:
        raise VarintError(f"Value out of uint32 range: {value}")
    return encode_unsigned(value)


def decode_uint32(data: bytes, offset: int = 0) -> Tuple[int, int]:
    """
    Decode a 32-bit unsigned integer.
    
    Args:
        data: Encoded bytes
        offset: Starting position
    
    Returns:
        Tuple of (decoded value, bytes consumed)
    """
    unsigned, consumed = decode_unsigned(data, offset)
    if unsigned > (1 << 32) - 1:
        raise VarintOverflowError(f"Decoded value out of uint32 range: {unsigned}")
    return unsigned, consumed


def encode_uint64(value: int) -> bytes:
    """
    Encode a 64-bit unsigned integer.
    
    Produces 1-10 bytes.
    
    Args:
        value: 64-bit unsigned integer
    
    Returns:
        Encoded bytes (1-10 bytes)
    """
    return encode_unsigned(value)


def decode_uint64(data: bytes, offset: int = 0) -> Tuple[int, int]:
    """
    Decode a 64-bit unsigned integer.
    
    Args:
        data: Encoded bytes
        offset: Starting position
    
    Returns:
        Tuple of (decoded value, bytes consumed)
    """
    return decode_unsigned(data, offset)


# ============================================================================
# Helper for Protocol Buffers compatibility
# ============================================================================

def encode_varint(value: int, signed: bool = False) -> bytes:
    """
    General-purpose varint encoder.
    
    Args:
        value: Integer to encode
        signed: If True, use ZigZag encoding for signed values
    
    Returns:
        Encoded varint bytes
    
    Examples:
        >>> encode_varint(300)
        b'\\xac\\x02'
        >>> encode_varint(-1, signed=True)
        b'\\x01'
    """
    if signed:
        return encode_signed(value)
    return encode_unsigned(value)


def decode_varint(data: bytes, offset: int = 0, signed: bool = False) -> Tuple[int, int]:
    """
    General-purpose varint decoder.
    
    Args:
        data: Encoded bytes
        offset: Starting position
        signed: If True, decode as signed varint
    
    Returns:
        Tuple of (decoded value, bytes consumed)
    
    Examples:
        >>> decode_varint(b'\\xac\\x02')
        (300, 2)
        >>> decode_varint(b'\\x01', signed=True)
        (-1, 1)
    """
    if signed:
        return decode_signed(data, offset)
    return decode_unsigned(data, offset)


# Exports
__all__ = [
    # Exceptions
    'VarintError',
    'VarintOverflowError', 
    'VarintDecodeError',
    
    # Unsigned encoding/decoding
    'encode_unsigned',
    'decode_unsigned',
    'encode_unsigned_batch',
    'decode_unsigned_batch',
    
    # ZigZag encoding/decoding
    'zigzag_encode',
    'zigzag_decode',
    
    # Signed encoding/decoding
    'encode_signed',
    'decode_signed',
    'encode_signed_batch',
    'decode_signed_batch',
    
    # Streaming classes
    'VarintWriter',
    'VarintReader',
    
    # Size utilities
    'size_unsigned',
    'size_signed',
    'estimate_size_unsigned',
    'estimate_size_signed',
    'compare_efficiency',
    
    # Protocol Buffers style
    'encode_int32',
    'decode_int32',
    'encode_int64',
    'decode_int64',
    'encode_uint32',
    'decode_uint32',
    'encode_uint64',
    'decode_uint64',
    
    # General purpose
    'encode_varint',
    'decode_varint',
]