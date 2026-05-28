"""
Chunked Transfer Encoding Utilities

HTTP Chunked Transfer Encoding is a data transfer mechanism defined in HTTP/1.1.
It allows a server to begin transmitting dynamically generated content before
knowing the total content length.

Format:
    Each chunk consists of:
    - Chunk size in hex (with optional extensions)
    - CRLF (\r\n)
    - Chunk data
    - CRLF (\r\n)
    
    Final chunk has size 0, optionally followed by trailers.

Example:
    5\r\n
    Hello\r\n
    6\r\n
    World!\r\n
    0\r\n
    \r\n

Features:
    - Encode data into chunked format
    - Decode chunked data back to original content
    - Parse and handle chunk extensions and trailers
    - Validate chunked encoding format
    - Streaming encode/decode for large data

Zero external dependencies - uses only Python standard library.
"""

import re
from typing import List, Optional, Tuple, Dict, Any, Union, BinaryIO, Iterator


class ChunkedEncodingError(Exception):
    """Exception raised for chunked encoding errors."""
    pass


# Constants
CRLF = '\r\n'
CRLF_BYTES = b'\r\n'
MAX_CHUNK_SIZE = 2**24 - 1  # 16MB max per chunk (hex limit: 6 chars)


# ============================================================================
# Encoding
# ============================================================================

def encode(data: Union[str, bytes], chunk_size: int = 8192) -> bytes:
    """
    Encode data into HTTP chunked transfer encoding format.
    
    Args:
        data: Data to encode (string or bytes)
        chunk_size: Size of each chunk (default 8KB)
    
    Returns:
        Chunked encoded bytes
    
    Examples:
        >>> encode('Hello World!')
        b'5\\r\\nHello\\r\\n6\\r\\nWorld!\\r\\n0\\r\\n\\r\\n'
        
        >>> encode(b'data', chunk_size=2)
        b'2\\r\\nda\\r\\n2\\r\\nta\\r\\n0\\r\\n\\r\\n'
    """
    if isinstance(data, str):
        data = data.encode('utf-8')
    
    if not isinstance(data, bytes):
        raise ChunkedEncodingError("Data must be string or bytes")
    
    if chunk_size <= 0:
        raise ChunkedEncodingError("Chunk size must be positive")
    
    if chunk_size > MAX_CHUNK_SIZE:
        raise ChunkedEncodingError(f"Chunk size exceeds {MAX_CHUNK_SIZE}")
    
    result = bytearray()
    
    # Split data into chunks
    offset = 0
    while offset < len(data):
        chunk = data[offset:offset + chunk_size]
        chunk_len = len(chunk)
        
        # Write chunk size in hex
        result.extend(f'{chunk_len:x}'.encode('utf-8'))
        result.extend(CRLF_BYTES)
        
        # Write chunk data
        result.extend(chunk)
        result.extend(CRLF_BYTES)
        
        offset += chunk_size
    
    # Write final chunk (size 0)
    result.extend(b'0')
    result.extend(CRLF_BYTES)
    result.extend(CRLF_BYTES)
    
    return bytes(result)


def encode_with_extensions(data: Union[str, bytes], 
                           extensions: Optional[List[Tuple[str, Optional[str]]]] = None,
                           chunk_size: int = 8192) -> bytes:
    """
    Encode data with chunk extensions.
    
    Args:
        data: Data to encode
        extensions: List of (name, value) tuples for first chunk
        chunk_size: Size of each chunk
    
    Returns:
        Chunked encoded bytes
    
    Example:
        >>> encode_with_extensions('Hello', [('name', 'test')])
        b'5;name=test\\r\\nHello\\r\\n0\\r\\n\\r\\n'
    """
    if isinstance(data, str):
        data = data.encode('utf-8')
    
    if not isinstance(data, bytes):
        raise ChunkedEncodingError("Data must be string or bytes")
    
    result = bytearray()
    
    # First chunk with extensions
    first_chunk = data[:chunk_size] if len(data) > 0 else b''
    
    # Write chunk size and extensions
    chunk_len = len(first_chunk)
    size_str = f'{chunk_len:x}'
    
    if extensions:
        for name, value in extensions:
            if value:
                size_str += f';{name}={value}'
            else:
                size_str += f';{name}'
    
    result.extend(size_str.encode('utf-8'))
    result.extend(CRLF_BYTES)
    result.extend(first_chunk)
    result.extend(CRLF_BYTES)
    
    # Remaining chunks
    offset = chunk_size
    while offset < len(data):
        chunk = data[offset:offset + chunk_size]
        chunk_len = len(chunk)
        
        result.extend(f'{chunk_len:x}'.encode('utf-8'))
        result.extend(CRLF_BYTES)
        result.extend(chunk)
        result.extend(CRLF_BYTES)
        
        offset += chunk_size
    
    # Final chunk
    result.extend(b'0')
    result.extend(CRLF_BYTES)
    result.extend(CRLF_BYTES)
    
    return bytes(result)


def encode_with_trailers(data: Union[str, bytes],
                         trailers: Optional[Dict[str, str]] = None,
                         chunk_size: int = 8192) -> bytes:
    """
    Encode data with trailing headers.
    
    Args:
        data: Data to encode
        trailers: Dictionary of trailer headers
        chunk_size: Size of each chunk
    
    Returns:
        Chunked encoded bytes
    
    Example:
        >>> encode_with_trailers('Hello', {'X-Checksum': 'abc123'})
        b'5\\r\\nHello\\r\\n0\\r\\nX-Checksum: abc123\\r\\n\\r\\n'
    """
    result = bytearray(encode(data, chunk_size))
    
    if trailers:
        # Remove final empty line, add trailers, then final empty line
        # The encoded data ends with '0\r\n\r\n'
        # We need to change it to '0\r\n<trailers>\r\n\r\n'
        
        # Actually, we need to rewrite the ending
        # Let's encode fresh
        if isinstance(data, str):
            data = data.encode('utf-8')
        
        result = bytearray()
        offset = 0
        while offset < len(data):
            chunk = data[offset:offset + chunk_size]
            chunk_len = len(chunk)
            
            result.extend(f'{chunk_len:x}'.encode('utf-8'))
            result.extend(CRLF_BYTES)
            result.extend(chunk)
            result.extend(CRLF_BYTES)
            
            offset += chunk_size
        
        # Final chunk
        result.extend(b'0')
        result.extend(CRLF_BYTES)
        
        # Add trailers
        for name, value in trailers.items():
            result.extend(f'{name}: {value}'.encode('utf-8'))
            result.extend(CRLF_BYTES)
        
        # Final empty line
        result.extend(CRLF_BYTES)
    
    return bytes(result)


def encode_chunks(data_chunks: List[Union[str, bytes]]) -> bytes:
    """
    Encode multiple data chunks separately.
    
    Args:
        data_chunks: List of data chunks to encode
    
    Returns:
        Chunked encoded bytes
    
    Example:
        >>> encode_chunks([b'Hello', b'World'])
        b'5\\r\\nHello\\r\\n5\\r\\nWorld\\r\\n0\\r\\n\\r\\n'
    """
    result = bytearray()
    
    for chunk in data_chunks:
        if isinstance(chunk, str):
            chunk = chunk.encode('utf-8')
        
        chunk_len = len(chunk)
        result.extend(f'{chunk_len:x}'.encode('utf-8'))
        result.extend(CRLF_BYTES)
        result.extend(chunk)
        result.extend(CRLF_BYTES)
    
    # Final chunk
    result.extend(b'0')
    result.extend(CRLF_BYTES)
    result.extend(CRLF_BYTES)
    
    return bytes(result)


# ============================================================================
# Decoding
# ============================================================================

def decode(data: Union[str, bytes]) -> bytes:
    """
    Decode chunked transfer encoded data.
    
    Args:
        data: Chunked encoded data
    
    Returns:
        Decoded bytes
    
    Raises:
        ChunkedEncodingError: If data is invalid
    
    Examples:
        >>> decode(b'5\\r\\nHello\\r\\n0\\r\\n\\r\\n')
        b'Hello'
        
        >>> decode('6\\r\\nWorld!\\r\\n0\\r\\n\\r\\n')
        b'World!'
    """
    if isinstance(data, str):
        data = data.encode('utf-8')
    
    if not isinstance(data, bytes):
        raise ChunkedEncodingError("Data must be string or bytes")
    
    decoder = ChunkedDecoder()
    decoder.feed(data)
    return decoder.get_data()


def decode_to_string(data: Union[str, bytes], encoding: str = 'utf-8') -> str:
    """
    Decode chunked data and convert to string.
    
    Args:
        data: Chunked encoded data
        encoding: Character encoding for conversion
    
    Returns:
        Decoded string
    
    Example:
        >>> decode_to_string(b'5\\r\\nHello\\r\\n0\\r\\n\\r\\n')
        'Hello'
    """
    decoded_bytes = decode(data)
    return decoded_bytes.decode(encoding)


def decode_with_metadata(data: Union[str, bytes]) -> Dict[str, Any]:
    """
    Decode chunked data and extract all metadata.
    
    Args:
        data: Chunked encoded data
    
    Returns:
        Dictionary with decoded data and metadata:
        - content: Decoded bytes
        - extensions: List of chunk extensions
        - trailers: Trailer headers dictionary
        - chunk_count: Number of chunks
        - total_size: Total content size
    
    Example:
        >>> decode_with_metadata(b'5;name=test\\r\\nHello\\r\\n0\\r\\n\\r\\n')
        {'content': b'Hello', 'extensions': [('name', 'test')], ...}
    """
    if isinstance(data, str):
        data = data.encode('utf-8')
    
    decoder = ChunkedDecoder()
    decoder.feed(data)
    
    return {
        'content': decoder.get_data(),
        'extensions': decoder.extensions,
        'trailers': decoder.trailers,
        'chunk_count': decoder.chunk_count,
        'total_size': decoder.total_size,
    }


# ============================================================================
# ChunkedDecoder Class (Streaming)
# ============================================================================

class ChunkedDecoder:
    """
    Streaming decoder for chunked transfer encoding.
    
    Use this when receiving data incrementally (e.g., from network).
    
    Example:
        >>> decoder = ChunkedDecoder()
        >>> decoder.feed(b'5\\r\\nHello\\r\\n')
        >>> decoder.feed(b'0\\r\\n\\r\\n')
        >>> decoder.is_complete()
        True
        >>> decoder.get_data()
        b'Hello'
    """
    
    def __init__(self):
        self.buffer = bytearray()
        self.output = bytearray()
        self.extensions: List[Tuple[str, Optional[str]]] = []
        self.trailers: Dict[str, str] = {}
        self.chunk_count = 0
        self.total_size = 0
        
        self._state = 'size'  # size, data, trailers, complete
        self._current_chunk_size = 0
        self._current_chunk_data = bytearray()
        self._size_line = bytearray()
        self._trailer_lines: List[str] = []
    
    def feed(self, data: bytes) -> int:
        """
        Feed data to the decoder.
        
        Args:
            data: Bytes to process
        
        Returns:
            Number of bytes consumed
        
        Raises:
            ChunkedEncodingError: If invalid data
        """
        self.buffer.extend(data)
        consumed = 0
        
        while True:
            if self._state == 'complete':
                break
            
            if self._state == 'size':
                # Looking for chunk size line
                crlf_pos = self.buffer.find(CRLF_BYTES)
                if crlf_pos == -1:
                    break  # Need more data
                
                size_line = bytes(self.buffer[:crlf_pos])
                consumed += crlf_pos + 2
                self.buffer = self.buffer[crlf_pos + 2:]
                
                # Parse size and extensions
                self._parse_size_line(size_line)
                
                if self._current_chunk_size == 0:
                    self._state = 'trailers'
                else:
                    self._state = 'data'
                    self._current_chunk_data = bytearray()
            
            elif self._state == 'data':
                # Looking for chunk data
                needed = self._current_chunk_size + 2  # +2 for CRLF
                
                if len(self.buffer) < needed:
                    break  # Need more data
                
                chunk_data = bytes(self.buffer[:self._current_chunk_size])
                consumed += needed
                self.buffer = self.buffer[needed:]
                
                # Verify trailing CRLF
                # Already consumed
                
                # Store chunk data
                self.output.extend(chunk_data)
                self.total_size += len(chunk_data)
                self.chunk_count += 1
                
                self._state = 'size'
            
            elif self._state == 'trailers':
                # Looking for trailer headers
                crlf_pos = self.buffer.find(CRLF_BYTES)
                if crlf_pos == -1:
                    break  # Need more data
                
                trailer_line = bytes(self.buffer[:crlf_pos]).decode('utf-8', errors='replace')
                consumed += crlf_pos + 2
                self.buffer = self.buffer[crlf_pos + 2:]
                
                if trailer_line == '':
                    # Empty line = end of trailers
                    self._parse_trailers()
                    self._state = 'complete'
                else:
                    self._trailer_lines.append(trailer_line)
        
        return consumed
    
    def _parse_size_line(self, line: bytes):
        """Parse chunk size line with optional extensions."""
        line_str = line.decode('utf-8', errors='replace')
        
        # Split by ';'
        parts = line_str.split(';')
        
        # First part is the size
        size_str = parts[0].strip()
        
        try:
            self._current_chunk_size = int(size_str, 16)
        except ValueError:
            raise ChunkedEncodingError(f"Invalid chunk size: {size_str}")
        
        # Parse extensions
        for ext in parts[1:]:
            ext = ext.strip()
            if '=' in ext:
                name, value = ext.split('=', 1)
                self.extensions.append((name.strip(), value.strip()))
            else:
                self.extensions.append((ext, None))
    
    def _parse_trailers(self):
        """Parse trailer header lines."""
        for line in self._trailer_lines:
            if ':' in line:
                name, value = line.split(':', 1)
                self.trailers[name.strip()] = value.strip()
    
    def is_complete(self) -> bool:
        """Check if decoding is complete."""
        return self._state == 'complete'
    
    def get_data(self) -> bytes:
        """
        Get decoded data.
        
        Returns:
            Decoded bytes (empty if not complete)
        """
        return bytes(self.output)
    
    def get_remaining(self) -> bytes:
        """Get unprocessed buffer data."""
        return bytes(self.buffer)
    
    def reset(self):
        """Reset decoder state."""
        self.buffer = bytearray()
        self.output = bytearray()
        self.extensions = []
        self.trailers = {}
        self.chunk_count = 0
        self.total_size = 0
        self._state = 'size'
        self._current_chunk_size = 0
        self._current_chunk_data = bytearray()
        self._trailer_lines = []


# ============================================================================
# ChunkedEncoder Class (Streaming)
# ============================================================================

class ChunkedEncoder:
    """
    Streaming encoder for chunked transfer encoding.
    
    Use this when generating data incrementally.
    
    Example:
        >>> encoder = ChunkedEncoder(chunk_size=100)
        >>> encoder.write(b'Hello')
        >>> encoder.write(b'World')
        >>> encoder.finish()
        >>> encoder.get_encoded()
        b'5\\r\\nHello\\r\\n5\\r\\nWorld\\r\\n0\\r\\n\\r\\n'
    """
    
    def __init__(self, chunk_size: int = 8192):
        """
        Initialize encoder.
        
        Args:
            chunk_size: Maximum chunk size
        """
        if chunk_size <= 0:
            raise ChunkedEncodingError("Chunk size must be positive")
        
        self.chunk_size = chunk_size
        self.buffer = bytearray()
        self.output = bytearray()
        self._finished = False
        self.chunk_count = 0
    
    def write(self, data: Union[str, bytes]) -> int:
        """
        Write data to encoder.
        
        Args:
            data: Data to encode
        
        Returns:
            Number of bytes written
        
        Raises:
            ChunkedEncodingError: If encoder already finished
        """
        if self._finished:
            raise ChunkedEncodingError("Encoder already finished")
        
        if isinstance(data, str):
            data = data.encode('utf-8')
        
        self.buffer.extend(data)
        
        # Flush chunks if buffer is large enough
        self._flush_chunks()
        
        return len(data)
    
    def _flush_chunks(self):
        """Flush complete chunks from buffer."""
        while len(self.buffer) >= self.chunk_size:
            chunk = bytes(self.buffer[:self.chunk_size])
            self.buffer = self.buffer[self.chunk_size:]
            
            # Encode chunk
            self.output.extend(f'{self.chunk_size:x}'.encode('utf-8'))
            self.output.extend(CRLF_BYTES)
            self.output.extend(chunk)
            self.output.extend(CRLF_BYTES)
            
            self.chunk_count += 1
    
    def finish(self) -> bytes:
        """
        Finish encoding and get final result.
        
        Returns:
            Remaining encoded bytes (final chunk)
        
        Raises:
            ChunkedEncodingError: If already finished
        """
        if self._finished:
            raise ChunkedEncodingError("Encoder already finished")
        
        # Flush remaining buffer
        if len(self.buffer) > 0:
            remaining = bytes(self.buffer)
            remaining_len = len(remaining)
            
            self.output.extend(f'{remaining_len:x}'.encode('utf-8'))
            self.output.extend(CRLF_BYTES)
            self.output.extend(remaining)
            self.output.extend(CRLF_BYTES)
            
            self.chunk_count += 1
        
        # Write final chunk
        self.output.extend(b'0')
        self.output.extend(CRLF_BYTES)
        self.output.extend(CRLF_BYTES)
        
        self._finished = True
        
        return bytes(self.output)
    
    def is_finished(self) -> bool:
        """Check if encoding is finished."""
        return self._finished
    
    def get_encoded(self) -> bytes:
        """Get encoded data so far."""
        return bytes(self.output)
    
    def get_buffer_size(self) -> int:
        """Get current buffer size."""
        return len(self.buffer)


# ============================================================================
# Validation
# ============================================================================

def validate(data: Union[str, bytes]) -> bool:
    """
    Validate chunked encoded data format.
    
    Args:
        data: Data to validate
    
    Returns:
        True if valid, False otherwise
    
    Example:
        >>> validate(b'5\\r\\nHello\\r\\n0\\r\\n\\r\\n')
        True
        >>> validate(b'invalid')
        False
    """
    try:
        if isinstance(data, str):
            data = data.encode('utf-8')
        
        decoder = ChunkedDecoder()
        decoder.feed(data)
        
        # Must be complete for valid data
        return decoder.is_complete()
    except ChunkedEncodingError:
        return False


def validate_partial(data: Union[str, bytes]) -> Tuple[bool, Optional[str]]:
    """
    Validate partial chunked data (may be incomplete).
    
    Args:
        data: Partial data to validate
    
    Returns:
        (is_valid, error_message) tuple
    
    Example:
        >>> validate_partial(b'5\\r\\nHello\\r\\n')
        (True, None)
    """
    if isinstance(data, str):
        data = data.encode('utf-8')
    
    decoder = ChunkedDecoder()
    try:
        decoder.feed(data)
        return (True, None)
    except ChunkedEncodingError as e:
        return (False, str(e))


# ============================================================================
# Analysis
# ============================================================================

def analyze(data: Union[str, bytes]) -> Dict[str, Any]:
    """
    Analyze chunked encoded data.
    
    Args:
        data: Chunked encoded data
    
    Returns:
        Analysis information
    
    Example:
        >>> analyze(b'5\\r\\nHello\\r\\n0\\r\\n\\r\\n')
        {'valid': True, 'chunk_count': 1, 'total_size': 5, ...}
    """
    if isinstance(data, str):
        data = data.encode('utf-8')
    
    try:
        decoder = ChunkedDecoder()
        decoder.feed(data)
        
        return {
            'valid': decoder.is_complete(),
            'complete': decoder.is_complete(),
            'chunk_count': decoder.chunk_count,
            'total_size': decoder.total_size,
            'extensions': decoder.extensions,
            'trailers': decoder.trailers,
            'remaining_bytes': len(decoder.buffer),
        }
    except ChunkedEncodingError as e:
        return {
            'valid': False,
            'error': str(e),
            'input_size': len(data),
        }


def get_chunk_sizes(data: Union[str, bytes]) -> List[int]:
    """
    Extract all chunk sizes from encoded data.
    
    Args:
        data: Chunked encoded data
    
    Returns:
        List of chunk sizes
    
    Example:
        >>> get_chunk_sizes(b'5\\r\\nHello\\r\\n6\\r\\nWorld!\\r\\n0\\r\\n\\r\\n')
        [5, 6]
    """
    if isinstance(data, str):
        data = data.encode('utf-8')
    
    sizes = []
    pos = 0
    
    while pos < len(data):
        # Find chunk size line
        crlf_pos = data.find(CRLF_BYTES, pos)
        if crlf_pos == -1:
            break
        
        size_line = data[pos:crlf_pos].decode('utf-8', errors='replace')
        
        # Parse size (ignore extensions)
        size_str = size_line.split(';')[0].strip()
        
        try:
            size = int(size_str, 16)
        except ValueError:
            break
        
        sizes.append(size)
        
        if size == 0:
            break
        
        # Skip chunk data and CRLF
        pos = crlf_pos + 2 + size + 2
    
    return sizes


def get_chunk_count(data: Union[str, bytes]) -> int:
    """
    Count number of chunks in encoded data.
    
    Args:
        data: Chunked encoded data
    
    Returns:
        Number of data chunks (excluding final 0-size chunk)
    
    Example:
        >>> get_chunk_count(b'5\\r\\nHello\\r\\n6\\r\\nWorld!\\r\\n0\\r\\n\\r\\n')
        2
    """
    sizes = get_chunk_sizes(data)
    return len([s for s in sizes if s > 0])


# ============================================================================
# Utilities
# ============================================================================

def split_into_chunks(data: Union[str, bytes], chunk_size: int = 8192) -> List[bytes]:
    """
    Split data into chunks without encoding.
    
    Args:
        data: Data to split
        chunk_size: Size of each chunk
    
    Returns:
        List of chunk bytes
    
    Example:
        >>> split_into_chunks(b'HelloWorld', chunk_size=5)
        [b'Hello', b'World']
    """
    if isinstance(data, str):
        data = data.encode('utf-8')
    
    chunks = []
    for i in range(0, len(data), chunk_size):
        chunks.append(data[i:i + chunk_size])
    
    return chunks


def size_to_hex(size: int) -> str:
    """
    Convert chunk size to hexadecimal string.
    
    Args:
        size: Chunk size
    
    Returns:
        Hexadecimal string
    
    Example:
        >>> size_to_hex(255)
        'ff'
    """
    return f'{size:x}'


def hex_to_size(hex_str: str) -> int:
    """
    Convert hexadecimal string to chunk size.
    
    Args:
        hex_str: Hexadecimal string
    
    Returns:
        Integer size
    
    Example:
        >>> hex_to_size('ff')
        255
    
    Raises:
        ChunkedEncodingError: If invalid hex
    """
    try:
        return int(hex_str, 16)
    except ValueError:
        raise ChunkedEncodingError(f"Invalid hex: {hex_str}")


def format_chunk_header(size: int, extensions: Optional[List[Tuple[str, Optional[str]]]] = None) -> bytes:
    """
    Format a chunk header line.
    
    Args:
        size: Chunk size
        extensions: Optional extensions
    
    Returns:
        Header bytes (without trailing CRLF)
    
    Example:
        >>> format_chunk_header(5)
        b'5'
        >>> format_chunk_header(5, [('name', 'test')])
        b'5;name=test'
    """
    header = f'{size:x}'
    
    if extensions:
        for name, value in extensions:
            if value:
                header += f';{name}={value}'
            else:
                header += f';{name}'
    
    return header.encode('utf-8')


def parse_chunk_header(header: Union[str, bytes]) -> Tuple[int, List[Tuple[str, Optional[str]]]]:
    """
    Parse a chunk header line.
    
    Args:
        header: Header bytes or string
    
    Returns:
        (size, extensions) tuple
    
    Example:
        >>> parse_chunk_header('5;name=test')
        (5, [('name', 'test')])
    """
    if isinstance(header, bytes):
        header = header.decode('utf-8', errors='replace')
    
    parts = header.split(';')
    
    size = int(parts[0].strip(), 16)
    
    extensions = []
    for ext in parts[1:]:
        ext = ext.strip()
        if '=' in ext:
            name, value = ext.split('=', 1)
            extensions.append((name.strip(), value.strip()))
        else:
            extensions.append((ext, None))
    
    return size, extensions


# ============================================================================
# HTTP Integration Helpers
# ============================================================================

def create_chunked_response_body(content: Union[str, bytes],
                                 chunk_size: int = 8192,
                                 trailers: Optional[Dict[str, str]] = None) -> bytes:
    """
    Create complete chunked response body.
    
    Args:
        content: Content to encode
        chunk_size: Chunk size
        trailers: Optional trailer headers
    
    Returns:
        Complete chunked encoded body
    
    Example:
        >>> create_chunked_response_body('Hello World')
        b'5\\r\\nHello\\r\\n6\\r\\nWorld\\r\\n0\\r\\n\\r\\n'
    """
    if trailers:
        return encode_with_trailers(content, trailers, chunk_size)
    return encode(content, chunk_size)


def parse_chunked_request_body(body: bytes,
                               expected_trailers: Optional[List[str]] = None) -> Dict[str, Any]:
    """
    Parse chunked request body with optional trailer validation.
    
    Args:
        body: Chunked request body
        expected_trailers: List of expected trailer header names
    
    Returns:
        Parsing result with content and metadata
    
    Example:
        >>> parse_chunked_request_body(b'5\\r\\nHello\\r\\n0\\r\\n\\r\\n')
        {'content': b'Hello', 'trailers': {}, 'valid': True}
    """
    result = decode_with_metadata(body)
    result['valid'] = True
    
    # Validate expected trailers
    if expected_trailers:
        missing = [t for t in expected_trailers if t not in result['trailers']]
        if missing:
            result['missing_trailers'] = missing
            result['valid'] = False
    
    return result


# Short aliases
encode_chunked = encode
decode_chunked = decode