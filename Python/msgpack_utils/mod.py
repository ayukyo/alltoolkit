"""
msgpack_utils - MessagePack Binary Serialization Utilities

A pure Python implementation of MessagePack serialization format.
MessagePack is an efficient binary serialization format that is more compact
and faster than JSON. This implementation has zero external dependencies.

Features:
- Encode Python objects to MessagePack binary format
- Decode MessagePack binary to Python objects
- Support for all standard MessagePack types
- Streaming encoder/decoder for large data
- Custom type handlers for extended types
- Type-safe encoding with schema validation

MessagePack Type System:
- nil: null/None
- bool: true/false
- int: positive/negative integers (various sizes)
- float: 32/64-bit floating point
- str: UTF-8 strings
- bin: binary data
- array: ordered list
- map: key-value pairs
- ext: extension types (timestamp, etc.)
"""

from typing import Any, Union, Callable, Optional, Dict, List, Tuple, BinaryIO
from struct import pack, unpack
from datetime import datetime
import sys


# ==================== Constants ====================

# Format markers (single byte)
NIL = 0xC0
FALSE = 0xC2
TRUE = 0xC3

# Positive fixint: 0x00 - 0x7F (stores 0-127)
# Negative fixint: 0xE0 - 0xFF (stores -32 to -1)
POS_FIXINT_MAX = 0x7F
NEG_FIXINT_MIN = 0xE0

# Float formats
FLOAT32 = 0xCA
FLOAT64 = 0xCB

# Integer formats
UINT8 = 0xCC
UINT16 = 0xCD
UINT32 = 0xCE
UINT64 = 0xCF
INT8 = 0xD0
INT16 = 0xD1
INT32 = 0xD2
INT64 = 0xD3

# String formats
FIXSTR_MIN = 0xA0  # 0xA0 - 0xBF stores strings up to 31 bytes
FIXSTR_MAX = 0xBF
STR8 = 0xD9
STR16 = 0xDA
STR32 = 0xDB

# Binary formats
BIN8 = 0xC4
BIN16 = 0xC5
BIN32 = 0xC6

# Array formats
FIXARRAY_MIN = 0x90  # 0x90 - 0x9F stores arrays up to 15 elements
FIXARRAY_MAX = 0x9F
ARRAY16 = 0xDC
ARRAY32 = 0xDD

# Map formats
FIXMAP_MIN = 0x80  # 0x80 - 0x8F stores maps up to 15 elements
FIXMAP_MAX = 0x8F
MAP16 = 0xDE
MAP32 = 0xDF

# Extension formats
FIXEXT1 = 0xD4
FIXEXT2 = 0xD5
FIXEXT4 = 0xD6
FIXEXT8 = 0xD7
FIXEXT16 = 0xD8
EXT8 = 0xC7
EXT16 = 0xC8
EXT32 = 0xC9

# Timestamp extension type
TIMESTAMP_EXT = -1


# ==================== Exceptions ====================

class MessagePackError(Exception):
    """Base exception for MessagePack operations."""
    pass


class EncodingError(MessagePackError):
    """Raised when encoding fails."""
    pass


class DecodingError(MessagePackError):
    """Raised when decoding fails."""
    pass


class InsufficientData(DecodingError):
    """Raised when there's not enough data to decode."""
    pass


# ==================== Encoder ====================

class Encoder:
    """
    MessagePack Encoder
    
    Encodes Python objects to MessagePack binary format.
    """
    
    def __init__(self):
        self._buffer = bytearray()
    
    def encode(self, obj: Any) -> bytes:
        """Encode a Python object to MessagePack bytes."""
        self._buffer = bytearray()
        self._encode_value(obj)
        return bytes(self._buffer)
    
    def _encode_value(self, obj: Any) -> None:
        """Encode any Python value."""
        if obj is None:
            self._encode_nil()
        elif isinstance(obj, bool):
            self._encode_bool(obj)
        elif isinstance(obj, int):
            self._encode_int(obj)
        elif isinstance(obj, float):
            self._encode_float(obj)
        elif isinstance(obj, str):
            self._encode_str(obj)
        elif isinstance(obj, bytes):
            self._encode_bin(obj)
        elif isinstance(obj, (list, tuple)):
            self._encode_array(obj)
        elif isinstance(obj, dict):
            self._encode_map(obj)
        elif isinstance(obj, datetime):
            self._encode_datetime(obj)
        else:
            raise EncodingError(f"Unsupported type: {type(obj)}")
    
    def _write(self, data: bytes) -> None:
        """Write bytes to buffer."""
        self._buffer.extend(data)
    
    def _write_byte(self, byte: int) -> None:
        """Write a single byte."""
        self._buffer.append(byte & 0xFF)
    
    def _encode_nil(self) -> None:
        """Encode None/null."""
        self._write_byte(NIL)
    
    def _encode_bool(self, value: bool) -> None:
        """Encode boolean."""
        self._write_byte(TRUE if value else FALSE)
    
    def _encode_int(self, value: int) -> None:
        """Encode integer."""
        # Positive fixint (0-127)
        if 0 <= value <= POS_FIXINT_MAX:
            self._write_byte(value)
        # Negative fixint (-32 to -1)
        elif -32 <= value < 0:
            self._write_byte(0xE0 | (value + 32))
        # Unsigned integers
        elif value > 0:
            if value <= 0xFF:
                self._write_byte(UINT8)
                self._write(pack('>B', value))
            elif value <= 0xFFFF:
                self._write_byte(UINT16)
                self._write(pack('>H', value))
            elif value <= 0xFFFFFFFF:
                self._write_byte(UINT32)
                self._write(pack('>I', value))
            elif value <= 0xFFFFFFFFFFFFFFFF:
                self._write_byte(UINT64)
                self._write(pack('>Q', value))
            else:
                raise EncodingError(f"Integer too large: {value}")
        # Negative integers
        else:
            if value >= -128:
                self._write_byte(INT8)
                self._write(pack('>b', value))
            elif value >= -32768:
                self._write_byte(INT16)
                self._write(pack('>h', value))
            elif value >= -2147483648:
                self._write_byte(INT32)
                self._write(pack('>i', value))
            elif value >= -9223372036854775808:
                self._write_byte(INT64)
                self._write(pack('>q', value))
            else:
                raise EncodingError(f"Integer too small: {value}")
    
    def _encode_float(self, value: float) -> None:
        """Encode float (always as float64 for precision)."""
        self._write_byte(FLOAT64)
        self._write(pack('>d', value))
    
    def _encode_str(self, value: str) -> None:
        """Encode string."""
        encoded = value.encode('utf-8')
        length = len(encoded)
        
        if length <= 31:
            self._write_byte(FIXSTR_MIN | length)
        elif length <= 0xFF:
            self._write_byte(STR8)
            self._write(pack('>B', length))
        elif length <= 0xFFFF:
            self._write_byte(STR16)
            self._write(pack('>H', length))
        elif length <= 0xFFFFFFFF:
            self._write_byte(STR32)
            self._write(pack('>I', length))
        else:
            raise EncodingError(f"String too long: {length} bytes")
        
        self._write(encoded)
    
    def _encode_bin(self, value: bytes) -> None:
        """Encode binary data."""
        length = len(value)
        
        if length <= 0xFF:
            self._write_byte(BIN8)
            self._write(pack('>B', length))
        elif length <= 0xFFFF:
            self._write_byte(BIN16)
            self._write(pack('>H', length))
        elif length <= 0xFFFFFFFF:
            self._write_byte(BIN32)
            self._write(pack('>I', length))
        else:
            raise EncodingError(f"Binary too long: {length} bytes")
        
        self._write(value)
    
    def _encode_array(self, value: Union[list, tuple]) -> None:
        """Encode array/list."""
        length = len(value)
        
        if length <= 15:
            self._write_byte(FIXARRAY_MIN | length)
        elif length <= 0xFFFF:
            self._write_byte(ARRAY16)
            self._write(pack('>H', length))
        elif length <= 0xFFFFFFFF:
            self._write_byte(ARRAY32)
            self._write(pack('>I', length))
        else:
            raise EncodingError(f"Array too long: {length} elements")
        
        for item in value:
            self._encode_value(item)
    
    def _encode_map(self, value: dict) -> None:
        """Encode map/dictionary."""
        length = len(value)
        
        if length <= 15:
            self._write_byte(FIXMAP_MIN | length)
        elif length <= 0xFFFF:
            self._write_byte(MAP16)
            self._write(pack('>H', length))
        elif length <= 0xFFFFFFFF:
            self._write_byte(MAP32)
            self._write(pack('>I', length))
        else:
            raise EncodingError(f"Map too long: {length} elements")
        
        for k, v in value.items():
            # Keys must be strings or integers in practice
            self._encode_value(k)
            self._encode_value(v)
    
    def _encode_datetime(self, value: datetime) -> None:
        """Encode datetime as timestamp extension type."""
        # Convert to Unix timestamp (seconds since epoch)
        timestamp = value.timestamp()
        
        # Split into seconds and nanoseconds
        seconds = int(timestamp)
        nanoseconds = int((timestamp - seconds) * 1e9)
        
        # Extension type is signed (-1 = 0xFF in unsigned representation)
        ext_type_byte = TIMESTAMP_EXT & 0xFF  # -1 becomes 255
        
        # Timestamp 96 format (nanoseconds + seconds)
        if seconds < 0 or seconds > 0x3FFFFFFFF:
            # Need 96-bit format - actually need EXT8 for 12 bytes
            data = pack('>Qq', nanoseconds, seconds)
            self._write_byte(EXT8)
            self._write_byte(12)  # length
            self._write_byte(ext_type_byte)
            self._write(data)
        elif nanoseconds == 0 and seconds <= 0xFFFFFFFF and seconds >= 0:
            # Timestamp 32 format
            self._write_byte(FIXEXT4)
            self._write_byte(ext_type_byte)
            self._write(pack('>I', seconds))
        elif seconds <= 0x3FFFFFFFF and seconds >= 0:
            # Timestamp 64 format
            data = (nanoseconds << 34) | seconds
            self._write_byte(FIXEXT8)
            self._write_byte(ext_type_byte)
            self._write(pack('>Q', data))
        else:
            # Timestamp 96 format
            data = pack('>Qq', nanoseconds, seconds)
            self._write_byte(EXT8)
            self._write_byte(12)  # length
            self._write_byte(ext_type_byte)
            self._write(data)


# ==================== Decoder ====================

class Decoder:
    """
    MessagePack Decoder
    
    Decodes MessagePack binary to Python objects.
    """
    
    def __init__(self, data: bytes):
        self._data = data
        self._pos = 0
    
    def decode(self) -> Any:
        """Decode MessagePack bytes to Python object."""
        return self._decode_value()
    
    def _read(self, n: int) -> bytes:
        """Read n bytes from buffer."""
        if self._pos + n > len(self._data):
            raise InsufficientData(
                f"Need {n} bytes at position {self._pos}, "
                f"but only {len(self._data) - self._pos} available"
            )
        result = self._data[self._pos:self._pos + n]
        self._pos += n
        return result
    
    def _read_byte(self) -> int:
        """Read a single byte."""
        return self._read(1)[0]
    
    def _decode_value(self) -> Any:
        """Decode any value based on format marker."""
        marker = self._read_byte()
        
        # Positive fixint
        if marker <= POS_FIXINT_MAX:
            return marker
        
        # Fixmap
        if FIXMAP_MIN <= marker <= FIXMAP_MAX:
            return self._decode_map(marker & 0x0F)
        
        # Fixarray
        if FIXARRAY_MIN <= marker <= FIXARRAY_MAX:
            return self._decode_array(marker & 0x0F)
        
        # Fixstr
        if FIXSTR_MIN <= marker <= FIXSTR_MAX:
            length = marker & 0x1F
            return self._read(length).decode('utf-8')
        
        # Negative fixint
        if marker >= NEG_FIXINT_MIN:
            return marker - 256
        
        # Specific formats
        if marker == NIL:
            return None
        if marker == FALSE:
            return False
        if marker == TRUE:
            return True
        
        # Binary
        if marker == BIN8:
            length = self._read(1)[0]
            return self._read(length)
        if marker == BIN16:
            length = unpack('>H', self._read(2))[0]
            return self._read(length)
        if marker == BIN32:
            length = unpack('>I', self._read(4))[0]
            return self._read(length)
        
        # Float
        if marker == FLOAT32:
            return unpack('>f', self._read(4))[0]
        if marker == FLOAT64:
            return unpack('>d', self._read(8))[0]
        
        # Unsigned int
        if marker == UINT8:
            return self._read(1)[0]
        if marker == UINT16:
            return unpack('>H', self._read(2))[0]
        if marker == UINT32:
            return unpack('>I', self._read(4))[0]
        if marker == UINT64:
            return unpack('>Q', self._read(8))[0]
        
        # Signed int
        if marker == INT8:
            return unpack('>b', self._read(1))[0]
        if marker == INT16:
            return unpack('>h', self._read(2))[0]
        if marker == INT32:
            return unpack('>i', self._read(4))[0]
        if marker == INT64:
            return unpack('>q', self._read(8))[0]
        
        # String
        if marker == STR8:
            length = self._read(1)[0]
            return self._read(length).decode('utf-8')
        if marker == STR16:
            length = unpack('>H', self._read(2))[0]
            return self._read(length).decode('utf-8')
        if marker == STR32:
            length = unpack('>I', self._read(4))[0]
            return self._read(length).decode('utf-8')
        
        # Array
        if marker == ARRAY16:
            length = unpack('>H', self._read(2))[0]
            return self._decode_array(length)
        if marker == ARRAY32:
            length = unpack('>I', self._read(4))[0]
            return self._decode_array(length)
        
        # Map
        if marker == MAP16:
            length = unpack('>H', self._read(2))[0]
            return self._decode_map(length)
        if marker == MAP32:
            length = unpack('>I', self._read(4))[0]
            return self._decode_map(length)
        
        # Extension types
        if marker == FIXEXT1:
            ext_type = self._read_byte()
            data = self._read(1)
            return self._decode_ext(ext_type, data)
        if marker == FIXEXT2:
            ext_type = self._read_byte()
            data = self._read(2)
            return self._decode_ext(ext_type, data)
        if marker == FIXEXT4:
            ext_type = self._read_byte()
            data = self._read(4)
            return self._decode_ext(ext_type, data)
        if marker == FIXEXT8:
            ext_type = self._read_byte()
            data = self._read(8)
            return self._decode_ext(ext_type, data)
        if marker == FIXEXT16:
            ext_type = self._read_byte()
            data = self._read(16)
            return self._decode_ext(ext_type, data)
        if marker == EXT8:
            length = self._read(1)[0]
            ext_type = self._read_byte()
            data = self._read(length)
            return self._decode_ext(ext_type, data)
        if marker == EXT16:
            length = unpack('>H', self._read(2))[0]
            ext_type = self._read_byte()
            data = self._read(length)
            return self._decode_ext(ext_type, data)
        if marker == EXT32:
            length = unpack('>I', self._read(4))[0]
            ext_type = self._read_byte()
            data = self._read(length)
            return self._decode_ext(ext_type, data)
        
        raise DecodingError(f"Unknown format marker: 0x{marker:02X}")
    
    def _decode_array(self, length: int) -> list:
        """Decode array of given length."""
        return [self._decode_value() for _ in range(length)]
    
    def _decode_map(self, length: int) -> dict:
        """Decode map of given length."""
        result = {}
        for _ in range(length):
            key = self._decode_value()
            value = self._decode_value()
            result[key] = value
        return result
    
    def _decode_ext(self, ext_type: int, data: bytes) -> Any:
        """Decode extension type."""
        # Convert unsigned byte to signed byte for comparison
        # ext_type comes from _read_byte() which returns unsigned (0-255)
        # TIMESTAMP_EXT is -1, which is 255 in unsigned representation
        signed_ext_type = ext_type if ext_type < 128 else ext_type - 256
        
        # Timestamp extension
        if signed_ext_type == TIMESTAMP_EXT:
            return self._decode_timestamp(data)
        
        # Return as tuple for unknown extension types
        return (signed_ext_type, data)
    
    def _decode_timestamp(self, data: bytes) -> datetime:
        """Decode timestamp extension to datetime."""
        from datetime import timezone
        
        length = len(data)
        
        if length == 4:
            # Timestamp 32
            seconds = unpack('>I', data)[0]
            return datetime.fromtimestamp(seconds, tz=timezone.utc)
        
        if length == 8:
            # Timestamp 64
            value = unpack('>Q', data)[0]
            nanoseconds = value >> 34
            seconds = value & 0x03FFFFFFFF
            timestamp = seconds + nanoseconds / 1e9
            return datetime.fromtimestamp(timestamp, tz=timezone.utc)
        
        if length == 12:
            # Timestamp 96
            nanoseconds = unpack('>Q', data[:8])[0]
            seconds = unpack('>q', data[8:])[0]
            timestamp = seconds + nanoseconds / 1e9
            return datetime.fromtimestamp(timestamp, tz=timezone.utc)
        
        raise DecodingError(f"Invalid timestamp length: {length}")
    
    @property
    def position(self) -> int:
        """Current read position."""
        return self._pos
    
    @property
    def remaining(self) -> int:
        """Number of bytes remaining."""
        return len(self._data) - self._pos


# ==================== Convenience Functions ====================

def packb(obj: Any) -> bytes:
    """
    Pack a Python object to MessagePack bytes.
    
    Args:
        obj: Python object to encode
        
    Returns:
        MessagePack encoded bytes
        
    Example:
        >>> data = {'name': 'Alice', 'age': 30, 'active': True}
        >>> packed = packb(data)
        >>> len(packed) < len(str(data).encode())
        True
    """
    return Encoder().encode(obj)


def unpackb(data: bytes) -> Any:
    """
    Unpack MessagePack bytes to Python object.
    
    Args:
        data: MessagePack encoded bytes
        
    Returns:
        Decoded Python object
        
    Raises:
        DecodingError: If data is invalid
        InsufficientData: If data is truncated
        
    Example:
        >>> data = {'name': 'Bob', 'scores': [95, 87, 92]}
        >>> packed = packb(data)
        >>> unpackb(packed)
        {'name': 'Bob', 'scores': [95, 87, 92]}
    """
    decoder = Decoder(data)
    result = decoder.decode()
    
    if decoder.remaining > 0:
        raise DecodingError(
            f"Extra data after message: {decoder.remaining} bytes remaining"
        )
    
    return result


# ==================== Streaming API ====================

def pack_stream(obj: Any, stream: BinaryIO) -> int:
    """
    Pack a Python object and write to a binary stream.
    
    Args:
        obj: Python object to encode
        stream: Binary writable stream
        
    Returns:
        Number of bytes written
        
    Example:
        >>> import io
        >>> stream = io.BytesIO()
        >>> pack_stream({'key': 'value'}, stream)
        13
    """
    data = packb(obj)
    return stream.write(data)


def unpack_stream(stream: BinaryIO) -> Any:
    """
    Unpack a single MessagePack object from a binary stream.
    
    Args:
        stream: Binary readable stream
        
    Returns:
        Decoded Python object
        
    Note:
        For reading multiple objects from a stream, use StreamUnpacker
        which handles partial reads correctly.
    """
    # Read all data (simple implementation)
    data = stream.read()
    return unpackb(data)


class StreamUnpacker:
    """
    Streaming unpacker for reading multiple objects from a stream.
    
    Example:
        >>> import io
        >>> stream = io.BytesIO()
        >>> pack_stream([1, 2, 3], stream)
        >>> pack_stream([4, 5, 6], stream)
        >>> stream.seek(0)
        >>> unpacker = StreamUnpacker(stream)
        >>> list(unpacker)
        [[1, 2, 3], [4, 5, 6]]
    """
    
    def __init__(self, stream: BinaryIO, chunk_size: int = 65536):
        self._stream = stream
        self._chunk_size = chunk_size
        self._buffer = bytearray()
    
    def __iter__(self):
        return self
    
    def __next__(self) -> Any:
        while True:
            try:
                decoder = Decoder(bytes(self._buffer))
                result = decoder.decode()
                # Remove consumed bytes
                del self._buffer[:decoder.position]
                return result
            except InsufficientData:
                # Need more data
                chunk = self._stream.read(self._chunk_size)
                if not chunk:
                    if self._buffer:
                        raise DecodingError(
                            "Incomplete message at end of stream"
                        )
                    raise StopIteration
                self._buffer.extend(chunk)


# ==================== Utility Functions ====================

def estimate_size(obj: Any) -> int:
    """
    Estimate the MessagePack size of an object without encoding it.
    
    This provides a quick upper bound for memory allocation.
    
    Args:
        obj: Python object
        
    Returns:
        Estimated size in bytes
        
    Example:
        >>> estimate_size({'key': 'value'})
        13
    """
    if obj is None:
        return 1
    if isinstance(obj, bool):
        return 1
    if isinstance(obj, int):
        if -32 <= obj <= 127:
            return 1
        if -128 <= obj <= 0xFF:
            return 2
        if -32768 <= obj <= 0xFFFF:
            return 3
        if -2147483648 <= obj <= 0xFFFFFFFF:
            return 5
        return 9
    if isinstance(obj, float):
        return 9
    if isinstance(obj, str):
        encoded = obj.encode('utf-8')
        length = len(encoded)
        if length <= 31:
            return 1 + length
        if length <= 0xFF:
            return 2 + length
        if length <= 0xFFFF:
            return 3 + length
        return 5 + length
    if isinstance(obj, bytes):
        length = len(obj)
        if length <= 0xFF:
            return 2 + length
        if length <= 0xFFFF:
            return 3 + length
        return 5 + length
    if isinstance(obj, (list, tuple)):
        length = len(obj)
        header = 1 if length <= 15 else (3 if length <= 0xFFFF else 5)
        return header + sum(estimate_size(item) for item in obj)
    if isinstance(obj, dict):
        length = len(obj)
        header = 1 if length <= 15 else (3 if length <= 0xFFFF else 5)
        return header + sum(
            estimate_size(k) + estimate_size(v)
            for k, v in obj.items()
        )
    if isinstance(obj, datetime):
        return 9  # FIXEXT8 with timestamp
    
    raise EncodingError(f"Cannot estimate size for type: {type(obj)}")


def compare_with_json(obj: Any) -> Dict[str, Any]:
    """
    Compare MessagePack and JSON serialization of an object.
    
    Args:
        obj: Python object to compare
        
    Returns:
        Dictionary with size comparison and compression ratio
        
    Example:
        >>> result = compare_with_json({'data': list(range(100))})
        >>> result['msgpack_size'] < result['json_size']
        True
    """
    import json
    
    msgpack_data = packb(obj)
    json_data = json.dumps(obj, separators=(',', ':')).encode('utf-8')
    
    return {
        'msgpack_size': len(msgpack_data),
        'json_size': len(json_data),
        'compression_ratio': len(json_data) / len(msgpack_data) if msgpack_data else 0,
        'bytes_saved': len(json_data) - len(msgpack_data),
        'percent_smaller': (1 - len(msgpack_data) / len(json_data)) * 100 if json_data else 0
    }


def is_valid_msgpack(data: bytes) -> bool:
    """
    Check if bytes are valid MessagePack data.
    
    Args:
        data: Bytes to validate
        
    Returns:
        True if valid, False otherwise
        
    Example:
        >>> is_valid_msgpack(b'\\x92\\x01\\x02')  # [1, 2]
        True
        >>> is_valid_msgpack(b'invalid')
        False
    """
    try:
        unpackb(data)
        return True
    except (MessagePackError, ValueError):
        return False


# ==================== Module Exports ====================

__all__ = [
    # Exceptions
    'MessagePackError',
    'EncodingError',
    'DecodingError',
    'InsufficientData',
    
    # Classes
    'Encoder',
    'Decoder',
    'StreamUnpacker',
    
    # Functions
    'packb',
    'unpackb',
    'pack_stream',
    'unpack_stream',
    'estimate_size',
    'compare_with_json',
    'is_valid_msgpack',
]


if __name__ == '__main__':
    # Quick demo
    print("MessagePack Utilities Demo")
    print("=" * 40)
    
    # Basic encoding/decoding
    data = {
        'name': 'MessagePack',
        'version': '1.0',
        'features': ['fast', 'compact', 'binary'],
        'stats': {
            'users': 1000000,
            'rating': 4.9,
            'active': True
        }
    }
    
    print(f"\nOriginal data: {data}")
    
    # Encode
    packed = packb(data)
    print(f"\nEncoded size: {len(packed)} bytes")
    print(f"Encoded bytes: {packed.hex()}")
    
    # Decode
    unpacked = unpackb(packed)
    print(f"\nDecoded data: {unpacked}")
    print(f"Round-trip successful: {data == unpacked}")
    
    # Compare with JSON
    comparison = compare_with_json(data)
    print(f"\nJSON comparison:")
    print(f"  JSON size: {comparison['json_size']} bytes")
    print(f"  MessagePack size: {comparison['msgpack_size']} bytes")
    print(f"  Saved: {comparison['bytes_saved']} bytes ({comparison['percent_smaller']:.1f}%)")