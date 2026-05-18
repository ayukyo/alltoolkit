"""
CBOR (Concise Binary Object Representation) Utilities

A pure Python implementation of CBOR encoding and decoding according to RFC 8949.
Zero external dependencies - works with Python standard library only.

CBOR is a binary data format that is a superset of JSON, designed for:
- Efficient encoding/decoding
- Small code size
- Extensibility via tags
- Support for more data types than JSON

Major Types:
    0: Unsigned integer (0 to 2^64-1)
    1: Negative integer (-1 to -2^64)
    2: Byte string
    3: Text string (UTF-8)
    4: Array
    5: Map
    6: Tagged value
    7: Simple values and floating point numbers

Usage:
    >>> from cbor_utils import encode, decode
    >>> data = {"name": "Alice", "age": 30, "active": True}
    >>> encoded = encode(data)
    >>> decoded = decode(encoded)
    >>> assert decoded == data
"""

import struct
import math
from typing import Any, Union, Optional, Tuple, Dict, List
from datetime import datetime, timezone
from functools import wraps

# Major types
MT_UNSIGNED_INT = 0
MT_NEGATIVE_INT = 1
MT_BYTE_STRING = 2
MT_TEXT_STRING = 3
MT_ARRAY = 4
MT_MAP = 5
MT_TAG = 6
MT_SIMPLE_FLOAT = 7

# Additional information values
AI_ONE_BYTE = 24
AI_TWO_BYTES = 25
AI_FOUR_BYTES = 26
AI_EIGHT_BYTES = 27
AI_INDEFINITE = 31

# Simple values
SIMPLE_FALSE = 20
SIMPLE_TRUE = 21
SIMPLE_NULL = 22
SIMPLE_UNDEFINED = 23

# Well-known tags
TAG_DATETIME_STRING = 0
TAG_DATETIME_EPOCH = 1
TAG_POSITIVE_BIGINT = 2
TAG_NEGATIVE_BIGINT = 3
TAG_DECIMAL_FRACTION = 4
TAG_BIGFLOAT = 5
TAG_BASE64URL = 21
TAG_BASE64 = 22
TAG_BASE16 = 23
TAG_CBOR = 24
TAG_URI = 32
TAG_BASE64URL_STRING = 33
TAG_BASE64_STRING = 34
TAG_MIME = 36
TAG_CBOR_UUID = 37
TAG_SET = 258
_TAG_BIGFLOAT_DECIMAL = 265
TAG_STRING_REF_NAMESPACE = 256
TAG_STRING_REF = 259


class CBORError(Exception):
    """Base exception for CBOR errors."""
    pass


class CBOREncodingError(CBORError):
    """Raised when encoding fails."""
    pass


class CBORDecodingError(CBORError):
    """Raised when decoding fails."""
    pass


class CBORUnsupportedTypeError(CBORError):
    """Raised when an unsupported type is encountered during encoding."""
    pass


class CBORMapKeyError(CBORError):
    """Raised when an invalid map key is used."""
    pass


class _CBORStream:
    """A simple byte stream reader for CBOR decoding."""
    
    def __init__(self, data: bytes):
        self._data = data
        self._pos = 0
    
    def read(self, n: int) -> bytes:
        """Read n bytes from the stream."""
        if self._pos + n > len(self._data):
            raise CBORDecodingError(
                f"Not enough data: need {n} bytes at position {self._pos}, "
                f"but only {len(self._data) - self._pos} available"
            )
        result = self._data[self._pos:self._pos + n]
        self._pos += n
        return result
    
    def peek(self, n: int = 1) -> bytes:
        """Peek at the next n bytes without consuming them."""
        if self._pos + n > len(self._data):
            raise CBORDecodingError(
                f"Not enough data to peek: need {n} bytes at position {self._pos}"
            )
        return self._data[self._pos:self._pos + n]
    
    def remaining(self) -> int:
        """Return the number of remaining bytes."""
        return len(self._data) - self._pos
    
    def at_end(self) -> bool:
        """Check if we've reached the end of the stream."""
        return self._pos >= len(self._data)


class _Encoder:
    """Internal CBOR encoder class."""
    
    def __init__(self, 
                 canonical: bool = False,
                 datetime_mode: Optional[str] = None,
                 date_as_datetime: bool = False,
                 sort_keys: bool = False,
                 string_ref: bool = False):
        self._canonical = canonical
        self._datetime_mode = datetime_mode  # None, 'string', or 'epoch'
        self._sort_keys = canonical or sort_keys
        self._string_ref = string_ref
        self._string_table: Dict[str, int] = {}
        self._string_table_idx = 0
    
    def encode(self, value: Any) -> bytes:
        """Encode a Python value to CBOR bytes."""
        if value is None:
            return self._encode_simple(SIMPLE_NULL)
        
        if value is True:
            return self._encode_simple(SIMPLE_TRUE)
        
        if value is False:
            return self._encode_simple(SIMPLE_FALSE)
        
        if isinstance(value, int):
            return self._encode_int(value)
        
        if isinstance(value, float):
            return self._encode_float(value)
        
        if isinstance(value, str):
            return self._encode_string(value)
        
        if isinstance(value, bytes):
            return self._encode_bytes(value)
        
        if isinstance(value, bytearray):
            return self._encode_bytes(bytes(value))
        
        if isinstance(value, (list, tuple)):
            return self._encode_array(value)
        
        if isinstance(value, dict):
            return self._encode_map(value)
        
        if isinstance(value, datetime):
            return self._encode_datetime(value)
        
        # Try to encode as a custom type
        return self._encode_custom(value)
    
    def _encode_head(self, major_type: int, value: int) -> bytes:
        """Encode a CBOR head (major type + additional info)."""
        if value < 24:
            # Value fits in additional info
            return bytes([major_type << 5 | value])
        elif value < 256:
            # One byte follows
            return bytes([major_type << 5 | AI_ONE_BYTE, value])
        elif value < 65536:
            # Two bytes follow
            return bytes([major_type << 5 | AI_TWO_BYTES]) + struct.pack('>H', value)
        elif value < 4294967296:
            # Four bytes follow
            return bytes([major_type << 5 | AI_FOUR_BYTES]) + struct.pack('>I', value)
        else:
            # Eight bytes follow
            return bytes([major_type << 5 | AI_EIGHT_BYTES]) + struct.pack('>Q', value)
    
    def _encode_simple(self, value: int) -> bytes:
        """Encode a simple value."""
        return bytes([MT_SIMPLE_FLOAT << 5 | value])
    
    def _encode_int(self, value: int) -> bytes:
        """Encode an integer."""
        # Check if we need big integer encoding (tag 2 or 3)
        if value >= 2**64:
            # Use tag 2 (positive big integer) with byte string
            byte_len = (value.bit_length() + 7) // 8
            byte_data = value.to_bytes(byte_len, 'big')
            # Remove leading zero byte if high bit is 0 (minimize encoding)
            if byte_data[0] == 0 and len(byte_data) > 1:
                byte_data = byte_data[1:]
            return bytes([MT_TAG << 5 | AI_ONE_BYTE, TAG_POSITIVE_BIGINT]) + \
                   self._encode_head(MT_BYTE_STRING, len(byte_data)) + byte_data
        elif value < -2**64:
            # Use tag 3 (negative big integer) with byte string
            # Negative big int is encoded as -1 - value
            neg_value = -value - 1
            byte_len = (neg_value.bit_length() + 7) // 8
            byte_data = neg_value.to_bytes(byte_len, 'big')
            # Remove leading zero byte if high bit is 0 (minimize encoding)
            if byte_data[0] == 0 and len(byte_data) > 1:
                byte_data = byte_data[1:]
            return bytes([MT_TAG << 5 | AI_ONE_BYTE, TAG_NEGATIVE_BIGINT]) + \
                   self._encode_head(MT_BYTE_STRING, len(byte_data)) + byte_data
        elif value >= 0:
            return self._encode_head(MT_UNSIGNED_INT, value)
        else:
            # Negative integers are encoded as -1 - value
            return self._encode_head(MT_NEGATIVE_INT, -value - 1)
    
    def _encode_float(self, value: float) -> bytes:
        """Encode a floating point number."""
        if math.isnan(value):
            # NaN
            return bytes([0xF9, 0x7E, 0x00])
        
        if math.isinf(value):
            if value > 0:
                # Positive infinity
                return bytes([0xF9, 0x7C, 0x00])
            else:
                # Negative infinity
                return bytes([0xF9, 0xFC, 0x00])
        
        # In canonical mode or for integer-like floats, use shorter encoding
        if self._canonical:
            # Check if it can be encoded as an integer
            if value == int(value) and abs(value) < 2**53:
                return self._encode_int(int(value))
            
            # Try to use the shortest floating-point representation
            # First try half-precision (16-bit)
            try:
                half = self._float_to_half(value)
                if self._half_to_float(half) == value:
                    return bytes([MT_SIMPLE_FLOAT << 5 | AI_TWO_BYTES]) + struct.pack('>H', half)
            except (ValueError, OverflowError):
                pass
        
        # Use double-precision (64-bit) for best accuracy
        return bytes([MT_SIMPLE_FLOAT << 5 | AI_EIGHT_BYTES]) + struct.pack('>d', value)
    
    def _float_to_half(self, value: float) -> int:
        """Convert a float to IEEE 754 half-precision (16-bit)."""
        # IEEE 754 half-precision format:
        # 1 sign bit, 5 exponent bits, 10 mantissa bits
        # Exponent bias: 15
        
        if value == 0.0:
            return 0 if math.copysign(1, value) > 0 else 0x8000
        
        sign = 0
        if value < 0:
            sign = 1
            value = -value
        
        # Normalize
        exponent = 0
        while value >= 2.0:
            value /= 2.0
            exponent += 1
        while value < 1.0:
            value *= 2.0
            exponent -= 1
        
        exponent += 15  # Bias
        
        if exponent <= 0:
            # Subnormal
            mantissa = int(value * (2 ** (10 + exponent)) + 0.5)
            return sign << 15 | mantissa
        elif exponent >= 31:
            # Overflow to infinity
            return sign << 15 | 0x7C00
        else:
            # Normal
            mantissa = int((value - 1.0) * (2 ** 10) + 0.5)
            if mantissa >= 0x400:
                mantissa = 0x3FF
            return sign << 15 | (exponent << 10) | mantissa
    
    def _half_to_float(self, value: int) -> float:
        """Convert IEEE 754 half-precision (16-bit) to float."""
        sign = (value >> 15) & 1
        exponent = (value >> 10) & 0x1F
        mantissa = value & 0x3FF
        
        if exponent == 0:
            # Subnormal or zero
            if mantissa == 0:
                return -0.0 if sign else 0.0
            result = mantissa * (2 ** -24)
        elif exponent == 31:
            # Infinity or NaN
            if mantissa == 0:
                return float('-inf') if sign else float('inf')
            return float('nan')
        else:
            # Normal
            result = (mantissa + 0x400) * (2 ** (exponent - 25))
        
        return -result if sign else result
    
    def _encode_string(self, value: str) -> bytes:
        """Encode a text string."""
        encoded = value.encode('utf-8')
        return self._encode_head(MT_TEXT_STRING, len(encoded)) + encoded
    
    def _encode_bytes(self, value: bytes) -> bytes:
        """Encode a byte string."""
        return self._encode_head(MT_BYTE_STRING, len(value)) + value
    
    def _encode_array(self, value: Union[list, tuple]) -> bytes:
        """Encode an array."""
        result = self._encode_head(MT_ARRAY, len(value))
        for item in value:
            result += self.encode(item)
        return result
    
    def _encode_map(self, value: dict) -> bytes:
        """Encode a map."""
        result = self._encode_head(MT_MAP, len(value))
        
        items = list(value.items())
        
        if self._sort_keys:
            # Sort keys in bytewise lex order (canonical CBOR)
            items.sort(key=lambda kv: self._sort_key(kv[0]))
        
        for key, val in items:
            result += self.encode(key)
            result += self.encode(val)
        
        return result
    
    def _sort_key(self, key: Any) -> Tuple[int, bytes]:
        """Generate a sort key for canonical ordering."""
        encoded = self.encode(key)
        return (len(encoded), encoded)
    
    def _encode_datetime(self, value: datetime) -> bytes:
        """Encode a datetime object."""
        if self._datetime_mode == 'string':
            # Encode as ISO 8601 string with tag 0
            dt_str = value.isoformat()
            if value.tzinfo is None:
                dt_str += 'Z'
            return (bytes([MT_TAG << 5 | AI_ONE_BYTE, TAG_DATETIME_STRING]) + 
                    self._encode_string(dt_str))
        else:
            # Encode as epoch timestamp with tag 1 (default)
            epoch = value.timestamp()
            if epoch == int(epoch):
                encoded = self._encode_int(int(epoch))
            else:
                encoded = self._encode_float(epoch)
            return bytes([MT_TAG << 5 | AI_ONE_BYTE, TAG_DATETIME_EPOCH]) + encoded
    
    def _encode_custom(self, value: Any) -> bytes:
        """Encode custom types. Override this method for extensibility."""
        # Try common patterns
        if hasattr(value, '__cbor_encode__'):
            return value.__cbor_encode__(self)
        
        if hasattr(value, 'to_cbor'):
            return self.encode(value.to_cbor())
        
        # Check for set
        if isinstance(value, set):
            result = self._encode_head(MT_TAG, TAG_SET)
            result += self._encode_head(MT_ARRAY, len(value))
            for item in value:
                result += self.encode(item)
            return result
        
        # Check for complex number
        if isinstance(value, complex):
            # Encode as array [real, imag] with tag
            result = bytes([MT_TAG << 5 | AI_TWO_BYTES]) + struct.pack('>H', 265)
            result += self._encode_array([value.real, value.imag])
            return result
        
        raise CBORUnsupportedTypeError(
            f"Cannot encode object of type {type(value).__name__}: {value!r}"
        )


class _Decoder:
    """Internal CBOR decoder class."""
    
    def __init__(self, 
                 string_refs: bool = False,
                 tag_hook: Optional[callable] = None,
                 object_hook: Optional[callable] = None):
        self._string_refs = string_refs
        self._tag_hook = tag_hook
        self._object_hook = object_hook
        self._string_table: Dict[int, str] = {}
        self._bytes_table: Dict[int, bytes] = {}
    
    def decode(self, data: Union[bytes, _CBORStream]) -> Any:
        """Decode CBOR bytes to a Python value."""
        if isinstance(data, bytes):
            stream = _CBORStream(data)
        else:
            stream = data
        
        return self._decode_item(stream)
    
    def _decode_item(self, stream: _CBORStream) -> Any:
        """Decode a single CBOR item."""
        if stream.at_end():
            raise CBORDecodingError("Unexpected end of data")
        
        first_byte = stream.read(1)[0]
        major_type = first_byte >> 5
        additional_info = first_byte & 0x1F
        
        # For simple/float values (major type 7), handle float encoding specially
        # because the additional info bytes are the actual float data
        if major_type == MT_SIMPLE_FLOAT:
            return self._decode_simple_float_direct(additional_info, stream)
        
        # Decode the value based on additional info for other types
        value = self._decode_additional_info(additional_info, stream)
        
        # Decode based on major type
        if major_type == MT_UNSIGNED_INT:
            return value
        
        if major_type == MT_NEGATIVE_INT:
            return -value - 1
        
        if major_type == MT_BYTE_STRING:
            if value is None:  # Indefinite length
                return self._decode_indefinite_bytes(stream)
            return stream.read(value)
        
        if major_type == MT_TEXT_STRING:
            if value is None:  # Indefinite length
                return self._decode_indefinite_string(stream)
            encoded = stream.read(value)
            return encoded.decode('utf-8')
        
        if major_type == MT_ARRAY:
            if value is None:  # Indefinite length
                return self._decode_indefinite_array(stream)
            return [self._decode_item(stream) for _ in range(value)]
        
        if major_type == MT_MAP:
            if value is None:  # Indefinite length
                return self._decode_indefinite_map(stream)
            # Use regular loop to ensure correct order (dict comprehension order varies by Python version)
            result = {}
            for _ in range(value):
                key = self._decode_item(stream)
                val = self._decode_item(stream)
                result[key] = val
            return result
        
        if major_type == MT_TAG:
            return self._decode_tagged(value, stream)
        
        raise CBORDecodingError(f"Unknown major type: {major_type}")
    
    def _decode_additional_info(self, ai: int, stream: _CBORStream) -> Optional[int]:
        """Decode the value from additional info."""
        if ai < 24:
            return ai
        if ai == AI_ONE_BYTE:
            return stream.read(1)[0]
        if ai == AI_TWO_BYTES:
            return struct.unpack('>H', stream.read(2))[0]
        if ai == AI_FOUR_BYTES:
            return struct.unpack('>I', stream.read(4))[0]
        if ai == AI_EIGHT_BYTES:
            return struct.unpack('>Q', stream.read(8))[0]
        if ai in (27, 28, 29, 30):
            raise CBORDecodingError(f"Invalid additional info: {ai}")
        if ai == AI_INDEFINITE:
            return None  # Indefinite length marker
        
        return ai
    
    def _decode_simple_float_direct(self, ai: int, stream: _CBORStream) -> Any:
        """Decode simple values and floats directly from stream."""
        if ai < 24:
            # Simple value encoded directly in additional info
            if ai == SIMPLE_FALSE:
                return False
            if ai == SIMPLE_TRUE:
                return True
            if ai == SIMPLE_NULL:
                return None
            if ai == SIMPLE_UNDEFINED:
                return None  # Python has no undefined
            return ai  # Other simple values
        
        if ai == AI_ONE_BYTE:
            # Simple value (one byte follows)
            simple_value = stream.read(1)[0]
            if simple_value == SIMPLE_FALSE:
                return False
            if simple_value == SIMPLE_TRUE:
                return True
            if simple_value == SIMPLE_NULL:
                return None
            if simple_value == SIMPLE_UNDEFINED:
                return None
            return simple_value
        
        if ai == AI_TWO_BYTES:
            # Half-precision float (2 bytes follow)
            half = struct.unpack('>H', stream.read(2))[0]
            return self._half_to_float(half)
        
        if ai == AI_FOUR_BYTES:
            # Single-precision float (4 bytes follow)
            return struct.unpack('>f', stream.read(4))[0]
        
        if ai == AI_EIGHT_BYTES:
            # Double-precision float (8 bytes follow)
            return struct.unpack('>d', stream.read(8))[0]
        
        raise CBORDecodingError(f"Invalid simple/float encoding: ai={ai}")
    
    def _half_to_float(self, value: int) -> float:
        """Convert IEEE 754 half-precision to float."""
        sign = (value >> 15) & 1
        exponent = (value >> 10) & 0x1F
        mantissa = value & 0x3FF
        
        if exponent == 0:
            if mantissa == 0:
                return -0.0 if sign else 0.0
            result = mantissa * (2 ** -24)
        elif exponent == 31:
            if mantissa == 0:
                return float('-inf') if sign else float('inf')
            return float('nan')
        else:
            result = (mantissa + 0x400) * (2 ** (exponent - 25))
        
        return -result if sign else result
    
    def _decode_indefinite_bytes(self, stream: _CBORStream) -> bytes:
        """Decode an indefinite-length byte string."""
        result = b''
        while True:
            first = stream.peek(1)[0]
            if first == 0xFF:  # Break marker
                stream.read(1)
                break
            chunk = self._decode_item(stream)
            if not isinstance(chunk, bytes):
                raise CBORDecodingError(
                    f"Expected byte string chunk, got {type(chunk)}"
                )
            result += chunk
        return result
    
    def _decode_indefinite_string(self, stream: _CBORStream) -> str:
        """Decode an indefinite-length text string."""
        result = ''
        while True:
            first = stream.peek(1)[0]
            if first == 0xFF:  # Break marker
                stream.read(1)
                break
            chunk = self._decode_item(stream)
            if not isinstance(chunk, str):
                raise CBORDecodingError(
                    f"Expected text string chunk, got {type(chunk)}"
                )
            result += chunk
        return result
    
    def _decode_indefinite_array(self, stream: _CBORStream) -> list:
        """Decode an indefinite-length array."""
        result = []
        while True:
            first = stream.peek(1)[0]
            if first == 0xFF:  # Break marker
                stream.read(1)
                break
            result.append(self._decode_item(stream))
        return result
    
    def _decode_indefinite_map(self, stream: _CBORStream) -> dict:
        """Decode an indefinite-length map."""
        result = {}
        while True:
            first = stream.peek(1)[0]
            if first == 0xFF:  # Break marker
                stream.read(1)
                break
            key = self._decode_item(stream)
            value = self._decode_item(stream)
            result[key] = value
        return result
    
    def _decode_tagged(self, tag: int, stream: _CBORStream) -> Any:
        """Decode a tagged value."""
        value = self._decode_item(stream)
        
        # Handle well-known tags
        if tag == TAG_DATETIME_STRING:
            # ISO 8601 string
            return self._parse_datetime_string(value)
        
        if tag == TAG_DATETIME_EPOCH:
            # Unix timestamp - convert to UTC datetime
            # Use utcfromtimestamp for Python 3.6 compatibility
            # and add timezone info
            try:
                dt = datetime.utcfromtimestamp(value).replace(tzinfo=timezone.utc)
            except (AttributeError, TypeError):
                # Fallback for edge cases
                dt = datetime.fromtimestamp(value)
            return dt
        
        if tag == TAG_POSITIVE_BIGINT:
            # Big positive integer
            return int.from_bytes(value, 'big')
        
        if tag == TAG_NEGATIVE_BIGINT:
            # Big negative integer
            return -int.from_bytes(value, 'big') - 1
        
        if tag == TAG_SET:
            # Set
            return set(value)
        
        if tag == TAG_URI:
            # URI string
            return value  # Just return the string for now
        
        if tag == TAG_BASE64URL:
            # Base64URL encoded data
            import base64
            return base64.urlsafe_b64decode(value + b'=' * (-len(value) % 4))
        
        if tag == TAG_BASE64:
            # Base64 encoded data
            import base64
            return base64.b64decode(value)
        
        if tag == TAG_BASE16:
            # Hex encoded data
            return bytes.fromhex(value)
        
        # Call custom tag hook if provided
        if self._tag_hook:
            return self._tag_hook(tag, value)
        
        # Return as tuple (tag, value)
        return (tag, value)
    
    def _parse_datetime_string(self, value: str) -> datetime:
        """Parse an ISO 8601 datetime string."""
        # Handle Z suffix
        value = value.replace('Z', '+00:00')
        
        # Handle timezone with colon (Python 3.6 %z only accepts +HHMM/-HHMM)
        # Convert +00:00 to +0000
        import re
        value = re.sub(r'([+-])(\d{2}):(\d{2})', r'\1\2\3', value)
        
        # Handle various ISO 8601 formats
        formats = [
            '%Y-%m-%dT%H:%M:%S.%f%z',  # With microseconds and timezone
            '%Y-%m-%dT%H:%M:%S%z',     # With timezone
            '%Y-%m-%dT%H:%M:%S.%f',    # With microseconds, no timezone
            '%Y-%m-%dT%H:%M:%S',       # No timezone
            '%Y-%m-%d %H:%M:%S.%f',    # Space separator
            '%Y-%m-%d %H:%M:%S',
            '%Y-%m-%d',
        ]
        
        for fmt in formats:
            try:
                dt = datetime.strptime(value, fmt)
                # Add UTC timezone if missing
                if dt.tzinfo is None and ('+' in value or value.endswith('Z')):
                    dt = dt.replace(tzinfo=timezone.utc)
                return dt
            except ValueError:
                continue
        
        # If still no timezone and no separator, assume UTC
        if '+' not in value and '-' not in value[10:]:
            try:
                return datetime.strptime(value, '%Y-%m-%dT%H:%M:%S').replace(tzinfo=timezone.utc)
            except ValueError:
                pass
        
        raise CBORDecodingError(f"Cannot parse datetime: {value}")


# Public API

def encode(value: Any, 
           canonical: bool = False,
           datetime_mode: Optional[str] = None,
           sort_keys: bool = False) -> bytes:
    """
    Encode a Python value to CBOR bytes.
    
    Args:
        value: The Python value to encode
        canonical: If True, encode in canonical form (deterministic)
        datetime_mode: How to encode datetime objects
            - None or 'epoch': Unix timestamp (default)
            - 'string': ISO 8601 string
        sort_keys: Sort map keys in canonical order
    
    Returns:
        CBOR-encoded bytes
    
    Raises:
        CBORUnsupportedTypeError: If the value type is not supported
    
    Examples:
        >>> encode({"name": "Alice", "age": 30})
        b'\\xa2enamedAliceiage\\x18\\x1e'
        
        >>> encode([1, 2, 3])
        b'\\x83\\x01\\x02\\x03'
        
        >>> encode(b"hello")
        b'ehello'
    """
    encoder = _Encoder(canonical=canonical, datetime_mode=datetime_mode, 
                       sort_keys=sort_keys)
    return encoder.encode(value)


def decode(data: bytes,
           string_refs: bool = False,
           tag_hook: Optional[callable] = None,
           object_hook: Optional[callable] = None) -> Any:
    """
    Decode CBOR bytes to a Python value.
    
    Args:
        data: CBOR-encoded bytes
        string_refs: Enable string reference handling
        tag_hook: Custom function to handle tags, receives (tag, value)
        object_hook: Custom function to process decoded objects
    
    Returns:
        The decoded Python value
    
    Raises:
        CBORDecodingError: If the data is invalid CBOR
    
    Examples:
        >>> decode(b'\\xa2enamedAliceiage\\x18\\x1e')
        {'name': 'Alice', 'age': 30}
        
        >>> decode(b'\\x83\\x01\\x02\\x03')
        [1, 2, 3]
        
        >>> decode(b'ehello')
        b'hello'
    """
    decoder = _Decoder(string_refs=string_refs, tag_hook=tag_hook,
                       object_hook=object_hook)
    result = decoder.decode(data)
    
    if object_hook:
        return object_hook(result)
    return result


def encode_to_file(value: Any, filepath: str, **kwargs) -> None:
    """
    Encode a value and write to a file.
    
    Args:
        value: The Python value to encode
        filepath: Path to the output file
        **kwargs: Additional arguments for encode()
    """
    with open(filepath, 'wb') as f:
        f.write(encode(value, **kwargs))


def decode_from_file(filepath: str, **kwargs) -> Any:
    """
    Decode CBOR from a file.
    
    Args:
        filepath: Path to the CBOR file
        **kwargs: Additional arguments for decode()
    
    Returns:
        The decoded Python value
    """
    with open(filepath, 'rb') as f:
        return decode(f.read(), **kwargs)


def is_valid_cbor(data: bytes) -> bool:
    """
    Check if bytes are valid CBOR.
    
    Args:
        data: Bytes to check
    
    Returns:
        True if valid CBOR, False otherwise
    """
    try:
        decode(data)
        return True
    except CBORError:
        return False


def get_cbor_type(data: bytes) -> str:
    """
    Get the CBOR type of encoded data.
    
    Args:
        data: CBOR-encoded bytes
    
    Returns:
        Type name string: 'int', 'float', 'bool', 'null', 'bytes', 
                         'str', 'array', 'map', 'tag', or 'unknown'
    """
    if not data:
        raise CBORDecodingError("Empty data")
    
    first_byte = data[0]
    major_type = first_byte >> 5
    
    type_map = {
        MT_UNSIGNED_INT: 'int',
        MT_NEGATIVE_INT: 'int',
        MT_BYTE_STRING: 'bytes',
        MT_TEXT_STRING: 'str',
        MT_ARRAY: 'array',
        MT_MAP: 'map',
        MT_TAG: 'tag',
        MT_SIMPLE_FLOAT: 'unknown',  # Could be float, bool, or null
    }
    
    if major_type == MT_SIMPLE_FLOAT:
        ai = first_byte & 0x1F
        if ai < 24:
            if ai == SIMPLE_FALSE or ai == SIMPLE_TRUE:
                return 'bool'
            if ai == SIMPLE_NULL:
                return 'null'
        return 'float'
    
    return type_map.get(major_type, 'unknown')


def encode_canonical(value: Any) -> bytes:
    """
    Encode in canonical CBOR form (deterministic encoding).
    
    Canonical CBOR ensures that equivalent data always encodes to
    the same bytes, which is useful for:
    - Hashing
    - Digital signatures
    - Comparison
    
    Args:
        value: The Python value to encode
    
    Returns:
        Canonical CBOR bytes
    """
    return encode(value, canonical=True)


def estimate_size(value: Any) -> int:
    """
    Estimate the size of the CBOR encoding without actually encoding.
    
    Args:
        value: The Python value
    
    Returns:
        Estimated size in bytes
    """
    if value is None or value is True or value is False:
        return 1
    
    if isinstance(value, int):
        if 0 <= value < 24:
            return 1
        elif value < 256:
            return 2
        elif value < 65536:
            return 3
        elif value < 4294967296:
            return 5
        else:
            return 9
    
    if isinstance(value, float):
        return 9  # Assume 64-bit encoding
    
    if isinstance(value, str):
        encoded = value.encode('utf-8')
        return estimate_size(len(encoded)) + len(encoded)
    
    if isinstance(value, (bytes, bytearray)):
        return estimate_size(len(value)) + len(value)
    
    if isinstance(value, (list, tuple)):
        return estimate_size(len(value)) + sum(estimate_size(item) for item in value)
    
    if isinstance(value, dict):
        return (estimate_size(len(value)) + 
                sum(estimate_size(k) + estimate_size(v) for k, v in value.items()))
    
    return 0


# Utility functions for common use cases

def dumps(obj: Any) -> bytes:
    """Alias for encode(). Matches JSON module interface."""
    return encode(obj)


def loads(data: bytes) -> Any:
    """Alias for decode(). Matches JSON module interface."""
    return decode(data)


def cbor2json(data: bytes) -> Any:
    """
    Convert CBOR to JSON-compatible Python objects.
    
    Converts byte strings to base64-encoded strings and handles
    other CBOR-specific types for JSON compatibility.
    
    Args:
        data: CBOR-encoded bytes
    
    Returns:
        JSON-compatible Python object
    """
    import base64
    
    def convert(obj):
        if isinstance(obj, bytes):
            return base64.b64encode(obj).decode('ascii')
        if isinstance(obj, dict):
            return {convert(k): convert(v) for k, v in obj.items()}
        if isinstance(obj, (list, tuple)):
            return [convert(item) for item in obj]
        if isinstance(obj, datetime):
            return obj.isoformat()
        if isinstance(obj, set):
            return [convert(item) for item in obj]
        return obj
    
    return convert(decode(data))


def json2cbor(obj: Any) -> bytes:
    """
    Convert JSON-compatible Python objects to CBOR.
    
    This is essentially the same as encode() but provided for
    symmetry with cbor2json().
    
    Args:
        obj: JSON-compatible Python object
    
    Returns:
        CBOR-encoded bytes
    """
    return encode(obj)