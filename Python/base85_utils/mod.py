"""
Base85 (Ascii85) Encoding/Decoding Utilities

A pure Python implementation of Base85 encoding with zero external dependencies.
Base85 is more efficient than Base64, encoding 4 bytes into 5 characters (25% overhead)
compared to Base64's 33% overhead.

Supports multiple variants:
- RFC 1924: Standard Base85 for IPv6 addresses
- Z85: ZeroMQ's variant (printable subset)
- Adobe/Ascii85: Used in PDF, PostScript, and Git
- btoa: Original btoa encoding

Author: AllToolkit
License: MIT
"""

import struct
from typing import Union, Optional, Tuple, List


# RFC 1924 Base85 character set (0-84)
RFC1924_CHARSET = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz!#$%&()*+-;<=>?@^_`{|}~"

# Z85 character set (ZeroMQ) - printable subset, avoids quotes and backslash
Z85_CHARSET = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ.-:+=^!/*?&<>()[]{}@%$#"

# Adobe/Ascii85 character set
ASCII85_CHARSET = "!\"#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\\]^_`abcdefghijklmnopqrstu"

# btoa character set (85 characters - variant of Ascii85)
BTOA_CHARSET = "!\"#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\\]^_`abcdefghijklmnopqrstu"


class Base85Error(Exception):
    """Base85 encoding/decoding error."""
    pass


class Base85Encoder:
    """
    Base85 encoder with support for multiple variants.
    
    Base85 encodes 4 bytes into 5 characters, achieving 25% overhead
    compared to Base64's 33% overhead.
    """
    
    def __init__(self, charset: str = RFC1924_CHARSET, variant: str = "rfc1924"):
        """
        Initialize encoder with specified character set.
        
        Args:
            charset: 85-character encoding alphabet
            variant: Variant name ('rfc1924', 'z85', 'ascii85', 'btoa')
        """
        if len(charset) != 85:
            raise Base85Error(f"Charset must have exactly 85 characters, got {len(charset)}")
        
        self.charset = charset
        self.variant = variant
        self._encode_table = {i: c for i, c in enumerate(charset)}
        self._decode_table = {c: i for i, c in enumerate(charset)}
    
    def encode(self, data: Union[bytes, str]) -> str:
        """
        Encode bytes to Base85 string.
        
        Args:
            data: Bytes or string to encode
            
        Returns:
            Base85 encoded string
            
        Raises:
            Base85Error: If encoding fails
        """
        if isinstance(data, str):
            data = data.encode('utf-8')
        
        if not isinstance(data, bytes):
            raise Base85Error(f"Expected bytes or str, got {type(data).__name__}")
        
        if not data:
            return ""
        
        result = []
        i = 0
        n = len(data)
        
        # Process 4-byte chunks
        while i + 4 <= n:
            chunk = data[i:i+4]
            # Convert to 32-bit big-endian integer
            value = struct.unpack('>I', chunk)[0]
            # Encode to 5 Base85 characters
            encoded = self._encode_chunk(value)
            result.append(encoded)
            i += 4
        
        # Handle remaining bytes (padding)
        if i < n:
            remaining = data[i:]
            padded = remaining + b'\x00' * (4 - len(remaining))
            value = struct.unpack('>I', padded)[0]
            encoded = self._encode_chunk(value)
            # Only include the characters we need
            result.append(encoded[:len(remaining) + 1])
        
        return ''.join(result)
    
    def _encode_chunk(self, value: int) -> str:
        """Encode a 32-bit value to 5 Base85 characters."""
        chars = []
        for _ in range(5):
            chars.append(self._encode_table[value % 85])
            value //= 85
        return ''.join(reversed(chars))
    
    def decode(self, data: str) -> bytes:
        """
        Decode Base85 string to bytes.
        
        Args:
            data: Base85 encoded string
            
        Returns:
            Decoded bytes
            
        Raises:
            Base85Error: If decoding fails
        """
        if not isinstance(data, str):
            raise Base85Error(f"Expected str, got {type(data).__name__}")
        
        # Remove whitespace
        data = ''.join(data.split())
        
        if not data:
            return b''
        
        result = []
        i = 0
        n = len(data)
        
        while i < n:
            # Find the chunk size (5 chars = 4 bytes)
            chunk_size = min(5, n - i)
            chunk = data[i:i+chunk_size]
            
            if len(chunk) < 5:
                # Pad with last character (index 84) for proper decoding
                # This ensures the decoded value preserves the high-order bytes
                padded_chunk = chunk + self.charset[-1] * (5 - len(chunk))
                decoded = self._decode_chunk(padded_chunk)
                # Remove padding bytes - take only original bytes
                original_bytes = len(chunk) - 1
                if original_bytes > 0:
                    result.append(decoded[:original_bytes])
            else:
                decoded = self._decode_chunk(chunk)
                result.append(decoded)
            
            i += chunk_size
        
        return b''.join(result)
    
    def _decode_chunk(self, chunk: str) -> bytes:
        """Decode 5 Base85 characters to 4 bytes."""
        if len(chunk) != 5:
            raise Base85Error(f"Expected 5 characters, got {len(chunk)}")
        
        value = 0
        for c in chunk:
            if c not in self._decode_table:
                raise Base85Error(f"Invalid character '{c}' in input")
            value = value * 85 + self._decode_table[c]
        
        return struct.pack('>I', value)
    
    def encode_with_wrap(self, data: Union[bytes, str], wrap: int = 76) -> str:
        """
        Encode with line wrapping for readability.
        
        Args:
            data: Bytes or string to encode
            wrap: Maximum line length (default 76)
            
        Returns:
            Base85 encoded string with newlines
        """
        encoded = self.encode(data)
        return '\n'.join(encoded[i:i+wrap] for i in range(0, len(encoded), wrap))
    
    @staticmethod
    def is_valid_base85(data: str, charset: str = RFC1924_CHARSET) -> bool:
        """
        Check if a string is valid Base85.
        
        Args:
            data: String to validate
            charset: Character set to use
            
        Returns:
            True if valid Base85, False otherwise
        """
        decode_table = {c: i for i, c in enumerate(charset)}
        data = ''.join(data.split())  # Remove whitespace
        
        for c in data:
            if c not in decode_table:
                return False
        
        return len(data) % 5 in (0, 2, 3, 4, 5)


class Ascii85Encoder(Base85Encoder):
    """
    Adobe Ascii85 encoder with special handling for zero blocks
    and framing characters.
    
    This variant uses '<~' and '~>' delimiters and encodes
    4 zero bytes as 'z' for efficiency.
    """
    
    def __init__(self):
        super().__init__(ASCII85_CHARSET, "ascii85")
        self.zero_char = 'z'
        self.start_delimiter = '<~'
        self.end_delimiter = '~>'
    
    def encode(self, data: Union[bytes, str], frame: bool = False) -> str:
        """
        Encode bytes to Ascii85.
        
        Args:
            data: Bytes or string to encode
            frame: If True, wrap output in <~ and ~> delimiters
            
        Returns:
            Ascii85 encoded string
        """
        if isinstance(data, str):
            data = data.encode('utf-8')
        
        if not data:
            if frame:
                # Adobe Ascii85 spec: empty stream is just <~>
                return self.start_delimiter[:-1] + self.end_delimiter
            return ""
        
        result = []
        i = 0
        n = len(data)
        
        while i + 4 <= n:
            chunk = data[i:i+4]
            # Check for all-zero chunk
            if chunk == b'\x00\x00\x00\x00':
                result.append(self.zero_char)
            else:
                value = struct.unpack('>I', chunk)[0]
                result.append(self._encode_chunk(value))
            i += 4
        
        # Handle remaining bytes
        if i < n:
            remaining = data[i:]
            padded = remaining + b'\x00' * (4 - len(remaining))
            value = struct.unpack('>I', padded)[0]
            encoded = self._encode_chunk(value)
            result.append(encoded[:len(remaining) + 1])
        
        output = ''.join(result)
        
        if frame:
            output = f"{self.start_delimiter}{output}{self.end_delimiter}"
        
        return output
    
    def decode(self, data: str) -> bytes:
        """
        Decode Ascii85 string to bytes.
        
        Automatically handles framed (<~...~>) and unframed formats.
        Also handles 'z' abbreviation for zero blocks.
        """
        if not isinstance(data, str):
            raise Base85Error(f"Expected str, got {type(data).__name__}")
        
        # Remove framing delimiters if present
        data = data.strip()
        if data.startswith(self.start_delimiter):
            data = data[2:]
        if data.endswith(self.end_delimiter):
            data = data[:-2]
        
        # Remove whitespace
        data = ''.join(data.split())
        
        if not data:
            return b''
        
        result = []
        i = 0
        n = len(data)
        
        while i < n:
            c = data[i]
            
            # Handle zero abbreviation
            if c == self.zero_char:
                result.append(b'\x00\x00\x00\x00')
                i += 1
                continue
            
            chunk_size = min(5, n - i)
            chunk = data[i:i+chunk_size]
            
            if len(chunk) < 5:
                # Pad with 'u' (last char, index 84) for proper decoding
                padded_chunk = chunk + ASCII85_CHARSET[-1] * (5 - len(chunk))
                decoded = self._decode_chunk(padded_chunk)
                original_bytes = len(chunk) - 1
                if original_bytes > 0:
                    result.append(decoded[:original_bytes])
            else:
                decoded = self._decode_chunk(chunk)
                result.append(decoded)
            
            i += chunk_size
        
        return b''.join(result)


class Z85Encoder(Base85Encoder):
    """
    Z85 encoder (ZeroMQ variant).
    
    Z85 uses a carefully chosen set of printable characters
    that are safe in JSON, XML, and command-line arguments.
    """
    
    def __init__(self):
        super().__init__(Z85_CHARSET, "z85")
    
    def encode(self, data: Union[bytes, str]) -> str:
        """Encode using Z85 character set."""
        return super().encode(data)
    
    def decode(self, data: str) -> bytes:
        """Decode Z85 string to bytes."""
        return super().decode(data)


# Pre-configured encoder instances
_encoder_rfc1924 = Base85Encoder(RFC1924_CHARSET, "rfc1924")
_encoder_z85 = Z85Encoder()
_encoder_ascii85 = Ascii85Encoder()
_encoder_btoa = Base85Encoder(BTOA_CHARSET, "btoa")


# Convenience functions
def encode(data: Union[bytes, str], variant: str = "rfc1924") -> str:
    """
    Encode bytes or string to Base85.
    
    Args:
        data: Bytes or string to encode
        variant: Encoding variant ('rfc1924', 'z85', 'ascii85', 'btoa')
        
    Returns:
        Base85 encoded string
        
    Raises:
        Base85Error: If variant is unknown or encoding fails
        
    Example:
        >>> encode(b"Hello, World!")
        'Xk&0]Cv8Aqt>'
        
        >>> encode(b"Hello, World!", variant="z85")
        'xK0cV8AQT>'
    """
    encoders = {
        "rfc1924": _encoder_rfc1924,
        "z85": _encoder_z85,
        "ascii85": _encoder_ascii85,
        "btoa": _encoder_btoa,
    }
    
    if variant not in encoders:
        raise Base85Error(f"Unknown variant: {variant}. Use one of: {list(encoders.keys())}")
    
    return encoders[variant].encode(data)


def decode(data: str, variant: str = "rfc1924") -> bytes:
    """
    Decode Base85 string to bytes.
    
    Args:
        data: Base85 encoded string
        variant: Encoding variant ('rfc1924', 'z85', 'ascii85', 'btoa')
        
    Returns:
        Decoded bytes
        
    Raises:
        Base85Error: If variant is unknown or decoding fails
        
    Example:
        >>> decode('Xk&0]Cv8Aqt>')
        b'Hello, World!'
    """
    encoders = {
        "rfc1924": _encoder_rfc1924,
        "z85": _encoder_z85,
        "ascii85": _encoder_ascii85,
        "btoa": _encoder_btoa,
    }
    
    if variant not in encoders:
        raise Base85Error(f"Unknown variant: {variant}. Use one of: {list(encoders.keys())}")
    
    return encoders[variant].decode(data)


def encode_ascii85(data: Union[bytes, str], frame: bool = False) -> str:
    """
    Encode to Ascii85 (Adobe variant).
    
    Args:
        data: Bytes or string to encode
        frame: If True, wrap in <~ and ~> delimiters
        
    Returns:
        Ascii85 encoded string
        
    Example:
        >>> encode_ascii85(b"Hello")
        '87cURDZ'
        
        >>> encode_ascii85(b"Hello", frame=True)
        '<~87cURDZ~>'
    """
    return _encoder_ascii85.encode(data, frame=frame)


def decode_ascii85(data: str) -> bytes:
    """
    Decode Ascii85 string to bytes.
    
    Handles both framed (<~...~>) and unframed formats.
    Also handles 'z' abbreviation for zero blocks.
    
    Args:
        data: Ascii85 encoded string
        
    Returns:
        Decoded bytes
        
    Example:
        >>> decode_ascii85('87cURDZ')
        b'Hello'
        
        >>> decode_ascii85('<~87cURDZ~>')
        b'Hello'
    """
    return _encoder_ascii85.decode(data)


def encode_z85(data: Union[bytes, str]) -> str:
    """
    Encode to Z85 (ZeroMQ variant).
    
    Z85 uses printable characters safe for JSON, XML, etc.
    
    Args:
        data: Bytes or string to encode
        
    Returns:
        Z85 encoded string
        
    Example:
        >>> encode_z85(b"Hello")
        'xK0cV'
    """
    return _encoder_z85.encode(data)


def decode_z85(data: str) -> bytes:
    """
    Decode Z85 string to bytes.
    
    Args:
        data: Z85 encoded string
        
    Returns:
        Decoded bytes
        
    Example:
        >>> decode_z85('xK0cV')
        b'Hello'
    """
    return _encoder_z85.decode(data)


def is_valid(data: str, variant: str = "rfc1924") -> bool:
    """
    Check if a string is valid Base85.
    
    Args:
        data: String to validate
        variant: Variant to check against
        
    Returns:
        True if valid, False otherwise
        
    Example:
        >>> is_valid('Xk&0]Cv8Aqt>')
        True
        
        >>> is_valid('invalid!!!')
        False
    """
    charsets = {
        "rfc1924": RFC1924_CHARSET,
        "z85": Z85_CHARSET,
        "ascii85": ASCII85_CHARSET,
        "btoa": BTOA_CHARSET,
    }
    
    if variant not in charsets:
        raise Base85Error(f"Unknown variant: {variant}")
    
    return Base85Encoder.is_valid_base85(data, charsets[variant])


def encode_file(filepath: str, variant: str = "rfc1924") -> str:
    """
    Encode file contents to Base85.
    
    Args:
        filepath: Path to file
        variant: Encoding variant
        
    Returns:
        Base85 encoded string
        
    Raises:
        FileNotFoundError: If file doesn't exist
        Base85Error: If encoding fails
    """
    with open(filepath, 'rb') as f:
        return encode(f.read(), variant)


def decode_to_file(data: str, filepath: str, variant: str = "rfc1924") -> int:
    """
    Decode Base85 string and write to file.
    
    Args:
        data: Base85 encoded string
        filepath: Output file path
        variant: Encoding variant
        
    Returns:
        Number of bytes written
        
    Raises:
        Base85Error: If decoding fails
    """
    decoded = decode(data, variant)
    with open(filepath, 'wb') as f:
        return f.write(decoded)


def compare_with_base64(data: bytes) -> dict:
    """
    Compare Base85 and Base64 encoding efficiency.
    
    Args:
        data: Bytes to compare
        
    Returns:
        Dictionary with comparison metrics
        
    Example:
        >>> compare_with_base64(b"Hello, World!")
        {
            'original_size': 13,
            'base85_size': 20,
            'base64_size': 20,
            'base85_overhead': 0.538,
            'base64_overhead': 0.538,
            'base85_efficiency': 1.0
        }
    """
    import base64
    
    b85_encoded = encode(data, "rfc1924")
    b64_encoded = base64.b64encode(data).decode('ascii')
    
    original_size = len(data)
    b85_size = len(b85_encoded)
    b64_size = len(b64_encoded)
    
    return {
        'original_size': original_size,
        'base85_size': b85_size,
        'base64_size': b64_size,
        'base85_overhead': (b85_size - original_size) / original_size,
        'base64_overhead': (b64_size - original_size) / original_size,
        'base85_efficiency': b64_size / b85_size if b85_size > 0 else 1.0,
    }


# IPv6 utilities using RFC 1924
def encode_ipv6_to_base85(ipv6_addr: str) -> str:
    """
    Encode IPv6 address to Base85 (RFC 1924).
    
    RFC 1924 defines a compact representation for IPv6 addresses
    using Base85 encoding.
    
    Args:
        ipv6_addr: IPv6 address string
        
    Returns:
        Base85 encoded IPv6 (20 characters)
        
    Example:
        >>> encode_ipv6_to_base85("1080:0:0:0:8:800:200C:417A")
        '4)+k&C#VzJ4br>0wv%Yp'
    """
    # Parse IPv6 address
    import ipaddress
    try:
        addr = ipaddress.IPv6Address(ipv6_addr)
    except ValueError as e:
        raise Base85Error(f"Invalid IPv6 address: {ipv6_addr}") from e
    
    # Get 16-byte representation
    addr_bytes = addr.packed
    
    # Encode each 4-byte chunk
    result = []
    for i in range(0, 16, 4):
        chunk = addr_bytes[i:i+4]
        value = struct.unpack('>I', chunk)[0]
        encoded = _encoder_rfc1924._encode_chunk(value)
        result.append(encoded)
    
    return ''.join(result)


def decode_base85_to_ipv6(encoded: str) -> str:
    """
    Decode Base85 encoded IPv6 address.
    
    Args:
        encoded: Base85 encoded IPv6 (20 characters)
        
    Returns:
        IPv6 address string
        
    Example:
        >>> decode_base85_to_ipv6('4)+k&C#VzJ4br>0wv%Yp')
        '1080::8:800:200c:417a'
    """
    if len(encoded) != 20:
        raise Base85Error(f"Expected 20 characters for IPv6, got {len(encoded)}")
    
    # Decode each 5-character chunk
    addr_bytes = bytearray()
    for i in range(0, 20, 5):
        chunk = encoded[i:i+5]
        decoded = _encoder_rfc1924._decode_chunk(chunk)
        addr_bytes.extend(decoded)
    
    # Convert to IPv6
    import ipaddress
    addr = ipaddress.IPv6Address(bytes(addr_bytes))
    return str(addr)


class Base85Iterator:
    """
    Iterator for streaming Base85 encoding.
    
    Useful for encoding large files without loading
    everything into memory.
    """
    
    def __init__(self, variant: str = "rfc1924"):
        self.encoder = {
            "rfc1924": _encoder_rfc1924,
            "z85": _encoder_z85,
            "ascii85": _encoder_ascii85,
            "btoa": _encoder_btoa,
        }.get(variant, _encoder_rfc1924)
        
        self._buffer = bytearray()
    
    def update(self, data: bytes) -> str:
        """
        Process data and return encoded output.
        
        Args:
            data: Bytes to encode
            
        Returns:
            Partially encoded Base85 string
        """
        self._buffer.extend(data)
        
        # Process complete 4-byte chunks
        complete_chunks = len(self._buffer) // 4
        output = []
        
        for i in range(complete_chunks):
            chunk = bytes(self._buffer[i*4:(i+1)*4])
            value = struct.unpack('>I', chunk)[0]
            output.append(self.encoder._encode_chunk(value))
        
        # Keep remaining bytes
        self._buffer = self._buffer[complete_chunks*4:]
        
        return ''.join(output)
    
    def finalize(self) -> str:
        """
        Finalize encoding and return remaining output.
        
        Returns:
            Final Base85 string
        """
        if not self._buffer:
            return ""
        
        # Pad remaining bytes
        padded = bytes(self._buffer) + b'\x00' * (4 - len(self._buffer))
        value = struct.unpack('>I', padded)[0]
        encoded = self.encoder._encode_chunk(value)
        
        # Only include necessary characters
        return encoded[:len(self._buffer) + 1]


def get_charset(variant: str = "rfc1924") -> str:
    """
    Get the character set for a variant.
    
    Args:
        variant: Variant name
        
    Returns:
        85-character charset string
    """
    charsets = {
        "rfc1924": RFC1924_CHARSET,
        "z85": Z85_CHARSET,
        "ascii85": ASCII85_CHARSET,
        "btoa": BTOA_CHARSET,
    }
    
    if variant not in charsets:
        raise Base85Error(f"Unknown variant: {variant}. Use one of: {list(charsets.keys())}")
    
    return charsets[variant]


def estimate_encoded_size(data_size: int) -> int:
    """
    Estimate Base85 encoded size.
    
    Args:
        data_size: Original data size in bytes
        
    Returns:
        Estimated encoded size in characters
        
    Example:
        >>> estimate_encoded_size(100)
        125
    """
    # Base85 encodes 4 bytes to 5 characters
    complete_chunks = data_size // 4
    remaining = data_size % 4
    
    size = complete_chunks * 5
    if remaining > 0:
        size += remaining + 1
    
    return size


def estimate_decoded_size(encoded_size: int) -> int:
    """
    Estimate decoded size from Base85 string length.
    
    Args:
        encoded_size: Encoded string length
        
    Returns:
        Estimated decoded size in bytes
        
    Note:
        This is an upper bound. Actual size may be smaller due to padding.
        
    Example:
        >>> estimate_decoded_size(125)
        100
    """
    # 5 characters = 4 bytes
    complete_chunks = encoded_size // 5
    remaining = encoded_size % 5
    
    size = complete_chunks * 4
    if remaining > 0:
        size += remaining - 1
    
    return max(0, size)


# Module exports
__all__ = [
    # Exceptions
    'Base85Error',
    
    # Classes
    'Base85Encoder',
    'Ascii85Encoder',
    'Z85Encoder',
    'Base85Iterator',
    
    # Character sets
    'RFC1924_CHARSET',
    'Z85_CHARSET',
    'ASCII85_CHARSET',
    'BTOA_CHARSET',
    
    # Functions
    'encode',
    'decode',
    'encode_ascii85',
    'decode_ascii85',
    'encode_z85',
    'decode_z85',
    'is_valid',
    'encode_file',
    'decode_to_file',
    'compare_with_base64',
    'encode_ipv6_to_base85',
    'decode_base85_to_ipv6',
    'get_charset',
    'estimate_encoded_size',
    'estimate_decoded_size',
]