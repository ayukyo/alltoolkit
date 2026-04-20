"""
AllToolkit - Python Bencode Utilities

A zero-dependency, production-ready Bencode encoding/decoding utility module.
Bencode is the encoding format used by the BitTorrent protocol.

Supports:
- String encoding/decoding
- Integer encoding/decoding
- List encoding/decoding
- Dictionary encoding/decoding
- Nested structures
- File I/O operations
- Torrent file parsing (basic .torrent file support)

Author: AllToolkit
License: MIT
"""

from typing import Any, Dict, List, Union, Tuple, Optional, BinaryIO
from io import BytesIO
import struct


class BencodeError(Exception):
    """Base exception for bencode operations."""
    pass


class BencodeEncodeError(BencodeError):
    """Error during encoding."""
    pass


class BencodeDecodeError(BencodeError):
    """Error during decoding."""
    pass


class BencodeTypeError(BencodeError):
    """Invalid type for bencode operation."""
    pass


# Type alias for bencodable types
Bencodable = Union[int, bytes, str, List['Bencodable'], Dict[bytes, 'Bencodable'], Dict[str, 'Bencodable']]


class Bencoder:
    """
    Bencode encoder/decoder class.
    
    Bencode format:
    - Strings: <length>:<content> (e.g., "4:spam")
    - Integers: i<integer>e (e.g., "i42e")
    - Lists: l<items>e (e.g., "l4:spami42ee")
    - Dictionaries: d<key-value pairs>e (e.g., "d3:foo3:bare")
    
    Keys in dictionaries must be strings and are sorted in lexicographic order.
    """
    
    def __init__(self, encoding: str = 'utf-8'):
        """
        Initialize the bencoder.
        
        Args:
            encoding: Default encoding for string operations (default: utf-8)
        """
        self.encoding = encoding
    
    # ==================== Encoding ====================
    
    def encode(self, data: Bencodable) -> bytes:
        """
        Encode a Python object to bencode format.
        
        Args:
            data: The data to encode (int, str, bytes, list, or dict)
            
        Returns:
            Bencode-encoded bytes
            
        Raises:
            BencodeEncodeError: If data cannot be encoded
        """
        try:
            return self._encode_value(data)
        except (TypeError, ValueError) as e:
            raise BencodeEncodeError(f"Failed to encode data: {e}")
    
    def _encode_value(self, value: Any) -> bytes:
        """Encode a single value."""
        if isinstance(value, int):
            return self._encode_int(value)
        elif isinstance(value, bytes):
            return self._encode_bytes(value)
        elif isinstance(value, str):
            return self._encode_bytes(value.encode(self.encoding))
        elif isinstance(value, (list, tuple)):
            return self._encode_list(value)
        elif isinstance(value, dict):
            return self._encode_dict(value)
        else:
            raise BencodeTypeError(f"Unsupported type: {type(value).__name__}")
    
    def _encode_int(self, value: int) -> bytes:
        """Encode an integer: i<value>e"""
        if not isinstance(value, int) or isinstance(value, bool):
            raise BencodeTypeError(f"Expected int, got {type(value).__name__}")
        return f"i{value}e".encode('ascii')
    
    def _encode_bytes(self, value: bytes) -> bytes:
        """Encode bytes: <length>:<content>"""
        return f"{len(value)}:".encode('ascii') + value
    
    def _encode_list(self, value: List) -> bytes:
        """Encode a list: l<items>e"""
        result = b"l"
        for item in value:
            result += self._encode_value(item)
        result += b"e"
        return result
    
    def _encode_dict(self, value: Dict) -> bytes:
        """Encode a dictionary: d<key-value pairs>e
        
        Keys must be strings/bytes and are sorted lexicographically.
        """
        result = b"d"
        
        # Convert all keys to bytes for sorting
        items = []
        for k, v in value.items():
            if isinstance(k, str):
                key_bytes = k.encode(self.encoding)
            elif isinstance(k, bytes):
                key_bytes = k
            else:
                raise BencodeTypeError(f"Dictionary keys must be str or bytes, got {type(k).__name__}")
            items.append((key_bytes, v))
        
        # Sort by bytes key
        items.sort(key=lambda x: x[0])
        
        for key_bytes, v in items:
            result += self._encode_bytes(key_bytes)
            result += self._encode_value(v)
        
        result += b"e"
        return result
    
    # ==================== Decoding ====================
    
    def decode(self, data: Union[bytes, str]) -> Bencodable:
        """
        Decode bencode data to a Python object.
        
        Args:
            data: Bencode-encoded data (bytes or str)
            
        Returns:
            Decoded Python object (int, bytes, list, or dict)
            
        Raises:
            BencodeDecodeError: If data cannot be decoded
        """
        if isinstance(data, str):
            data = data.encode('ascii')
        
        try:
            result, pos = self._decode_value(data, 0)
            if pos != len(data):
                raise BencodeDecodeError(f"Extra data after position {pos}")
            return result
        except (IndexError, ValueError) as e:
            raise BencodeDecodeError(f"Failed to decode data: {e}")
    
    def _decode_value(self, data: bytes, pos: int) -> Tuple[Bencodable, int]:
        """Decode a single value starting at position pos.
        
        Returns:
            Tuple of (decoded_value, next_position)
        """
        if pos >= len(data):
            raise BencodeDecodeError("Unexpected end of data")
        
        char = chr(data[pos])
        
        if char == 'i':
            return self._decode_int(data, pos)
        elif char.isdigit():
            return self._decode_bytes(data, pos)
        elif char == 'l':
            return self._decode_list(data, pos)
        elif char == 'd':
            return self._decode_dict(data, pos)
        else:
            raise BencodeDecodeError(f"Unexpected character '{char}' at position {pos}")
    
    def _decode_int(self, data: bytes, pos: int) -> Tuple[int, int]:
        """Decode an integer starting at position pos."""
        if chr(data[pos]) != 'i':
            raise BencodeDecodeError(f"Expected 'i' at position {pos}")
        
        pos += 1
        end = data.index(b'e', pos)
        
        # Handle negative numbers
        num_str = data[pos:end].decode('ascii')
        if not num_str or (num_str[0] == '-' and len(num_str) > 1 and num_str[1] == '0'):
            raise BencodeDecodeError(f"Invalid integer format: {num_str}")
        if num_str[0] == '0' and len(num_str) > 1:
            raise BencodeDecodeError(f"Leading zeros not allowed: {num_str}")
        
        try:
            value = int(num_str)
        except ValueError:
            raise BencodeDecodeError(f"Invalid integer: {num_str}")
        
        return value, end + 1
    
    def _decode_bytes(self, data: bytes, pos: int) -> Tuple[bytes, int]:
        """Decode a byte string starting at position pos."""
        # Find the colon
        colon = data.index(b':', pos)
        
        # Parse length
        length_str = data[pos:colon].decode('ascii')
        try:
            length = int(length_str)
        except ValueError:
            raise BencodeDecodeError(f"Invalid length: {length_str}")
        
        if length < 0:
            raise BencodeDecodeError(f"Negative length: {length}")
        
        # Extract bytes
        start = colon + 1
        end = start + length
        
        if end > len(data):
            raise BencodeDecodeError(f"String length {length} exceeds data bounds")
        
        return data[start:end], end
    
    def _decode_list(self, data: bytes, pos: int) -> Tuple[List, int]:
        """Decode a list starting at position pos."""
        if chr(data[pos]) != 'l':
            raise BencodeDecodeError(f"Expected 'l' at position {pos}")
        
        pos += 1
        result = []
        
        while chr(data[pos]) != 'e':
            value, pos = self._decode_value(data, pos)
            result.append(value)
        
        return result, pos + 1
    
    def _decode_dict(self, data: bytes, pos: int) -> Tuple[Dict[bytes, Any], int]:
        """Decode a dictionary starting at position pos."""
        if chr(data[pos]) != 'd':
            raise BencodeDecodeError(f"Expected 'd' at position {pos}")
        
        pos += 1
        result = {}
        last_key = None
        
        while chr(data[pos]) != 'e':
            # Decode key (must be bytes)
            key, pos = self._decode_bytes(data, pos)
            
            # Verify keys are sorted
            if last_key is not None and key <= last_key:
                raise BencodeDecodeError(f"Dictionary keys not sorted: {key} <= {last_key}")
            last_key = key
            
            # Decode value
            value, pos = self._decode_value(data, pos)
            result[key] = value
        
        return result, pos + 1
    
    # ==================== Convenience Methods ====================
    
    def decode_to_str_dict(self, data: Union[bytes, str]) -> Dict[str, Any]:
        """
        Decode bencode data to a dictionary with string keys.
        
        This is useful for torrent files where keys are typically ASCII strings.
        
        Args:
            data: Bencode-encoded data
            
        Returns:
            Dictionary with string keys
        """
        result = self.decode(data)
        if not isinstance(result, dict):
            raise BencodeTypeError("Expected dictionary at root level")
        
        return self._convert_keys_to_str(result)
    
    def _convert_keys_to_str(self, d: Dict) -> Dict[str, Any]:
        """Recursively convert bytes keys to string keys."""
        result = {}
        for k, v in d.items():
            str_key = k.decode(self.encoding) if isinstance(k, bytes) else k
            if isinstance(v, dict):
                result[str_key] = self._convert_keys_to_str(v)
            elif isinstance(v, list):
                result[str_key] = [
                    self._convert_keys_to_str(item) if isinstance(item, dict) else item
                    for item in v
                ]
            else:
                result[str_key] = v
        return result
    
    # ==================== File I/O ====================
    
    def encode_to_file(self, data: Bencodable, filepath: str) -> None:
        """
        Encode data and write to file.
        
        Args:
            data: Data to encode
            filepath: Path to output file
        """
        encoded = self.encode(data)
        with open(filepath, 'wb') as f:
            f.write(encoded)
    
    def decode_file(self, filepath: str) -> Bencodable:
        """
        Decode a bencode file.
        
        Args:
            filepath: Path to bencode file
            
        Returns:
            Decoded Python object
        """
        with open(filepath, 'rb') as f:
            data = f.read()
        return self.decode(data)
    
    def decode_file_to_str_dict(self, filepath: str) -> Dict[str, Any]:
        """
        Decode a bencode file to dictionary with string keys.
        
        Args:
            filepath: Path to bencode file (e.g., .torrent file)
            
        Returns:
            Dictionary with string keys
        """
        with open(filepath, 'rb') as f:
            data = f.read()
        return self.decode_to_str_dict(data)
    
    # ==================== Torrent Utilities ====================
    
    def parse_torrent_info(self, filepath: str) -> Dict[str, Any]:
        """
        Parse basic info from a .torrent file.
        
        Args:
            filepath: Path to .torrent file
            
        Returns:
            Dictionary with torrent info (name, files, piece length, etc.)
        """
        data = self.decode_file_to_str_dict(filepath)
        
        result = {
            'announce': data.get('announce', b'').decode(self.encoding) if isinstance(data.get('announce'), bytes) else data.get('announce'),
            'announce_list': [],
            'comment': data.get('comment', b'').decode(self.encoding) if isinstance(data.get('comment'), bytes) else data.get('comment'),
            'created_by': data.get('created by', b'').decode(self.encoding) if isinstance(data.get('created by'), bytes) else data.get('created by'),
            'creation_date': data.get('creation date'),
            'encoding': data.get('encoding', b'').decode(self.encoding) if isinstance(data.get('encoding'), bytes) else data.get('encoding'),
            'info': {}
        }
        
        # Parse announce-list
        announce_list = data.get('announce-list', [])
        if announce_list:
            for tier in announce_list:
                if isinstance(tier, list):
                    result['announce_list'].append([
                        url.decode(self.encoding) if isinstance(url, bytes) else url
                        for url in tier
                    ])
        
        # Parse info dictionary
        info = data.get('info', {})
        if info:
            result['info'] = {
                'name': info.get('name', b'').decode(self.encoding) if isinstance(info.get('name'), bytes) else info.get('name'),
                'piece_length': info.get('piece length'),
                'private': info.get('private') == 1,
                'pieces': len(info.get('pieces', b'')) // 20,  # Number of pieces (each 20 bytes SHA1)
            }
            
            # Files
            if 'files' in info:
                # Multi-file torrent
                result['info']['files'] = []
                for f in info['files']:
                    path = f.get('path', [])
                    if isinstance(path, list):
                        path = '/'.join(
                            p.decode(self.encoding) if isinstance(p, bytes) else p
                            for p in path
                        )
                    result['info']['files'].append({
                        'path': path,
                        'length': f.get('length')
                    })
            else:
                # Single-file torrent
                result['info']['length'] = info.get('length')
        
        return result
    
    def get_torrent_files(self, filepath: str) -> List[Dict[str, Any]]:
        """
        Get list of files in a torrent.
        
        Args:
            filepath: Path to .torrent file
            
        Returns:
            List of files with path and size
        """
        info = self.parse_torrent_info(filepath)
        files = info.get('info', {}).get('files', [])
        
        if not files:
            # Single file torrent
            name = info.get('info', {}).get('name', 'unknown')
            length = info.get('info', {}).get('length', 0)
            return [{'path': name, 'size': length}]
        
        return files
    
    def get_torrent_total_size(self, filepath: str) -> int:
        """
        Get total size of files in a torrent.
        
        Args:
            filepath: Path to .torrent file
            
        Returns:
            Total size in bytes
        """
        files = self.get_torrent_files(filepath)
        return sum(f.get('size', f.get('length', 0)) for f in files)


# ==================== Module-level Functions ====================

# Default encoder instance
_default_encoder = Bencoder()


def encode(data: Bencodable) -> bytes:
    """Encode data to bencode format."""
    return _default_encoder.encode(data)


def decode(data: Union[bytes, str]) -> Bencodable:
    """Decode bencode data."""
    return _default_encoder.decode(data)


def decode_to_str_dict(data: Union[bytes, str]) -> Dict[str, Any]:
    """Decode bencode data to dictionary with string keys."""
    return _default_encoder.decode_to_str_dict(data)


def encode_to_file(data: Bencodable, filepath: str) -> None:
    """Encode data and write to file."""
    _default_encoder.encode_to_file(data, filepath)


def decode_file(filepath: str) -> Bencodable:
    """Decode a bencode file."""
    return _default_encoder.decode_file(filepath)


def decode_file_to_str_dict(filepath: str) -> Dict[str, Any]:
    """Decode a bencode file to dictionary with string keys."""
    return _default_encoder.decode_file_to_str_dict(filepath)


def parse_torrent_info(filepath: str) -> Dict[str, Any]:
    """Parse basic info from a .torrent file."""
    return _default_encoder.parse_torrent_info(filepath)


def get_torrent_files(filepath: str) -> List[Dict[str, Any]]:
    """Get list of files in a torrent."""
    return _default_encoder.get_torrent_files(filepath)


def get_torrent_total_size(filepath: str) -> int:
    """Get total size of files in a torrent."""
    return _default_encoder.get_torrent_total_size(filepath)


# ==================== Utility Functions ====================

def bencode_size(data: Bencodable) -> int:
    """
    Calculate the size of encoded data without actually encoding.
    
    Args:
        data: Data to measure
        
    Returns:
        Size in bytes of encoded data
    """
    if isinstance(data, int):
        # i<digits>e
        return len(f"i{data}e")
    elif isinstance(data, bytes):
        return len(str(len(data))) + 1 + len(data)
    elif isinstance(data, str):
        encoded = data.encode('utf-8')
        return len(str(len(encoded))) + 1 + len(encoded)
    elif isinstance(data, (list, tuple)):
        return 2 + sum(bencode_size(item) for item in data)
    elif isinstance(data, dict):
        size = 2
        for k, v in data.items():
            if isinstance(k, str):
                k = k.encode('utf-8')
            size += len(str(len(k))) + 1 + len(k)
            size += bencode_size(v)
        return size
    else:
        raise BencodeTypeError(f"Unsupported type: {type(data).__name__}")


def validate_bencode(data: bytes) -> Tuple[bool, Optional[str]]:
    """
    Validate bencode data.
    
    Args:
        data: Bencode data to validate
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    try:
        encoder = Bencoder()
        encoder.decode(data)
        return True, None
    except BencodeError as e:
        return False, str(e)


def is_bencodable(value: Any) -> bool:
    """
    Check if a value can be bencoded.
    
    Args:
        value: Value to check
        
    Returns:
        True if value can be bencoded
    """
    if isinstance(value, (int, bytes, str)):
        return True
    elif isinstance(value, (list, tuple)):
        return all(is_bencodable(item) for item in value)
    elif isinstance(value, dict):
        return all(
            isinstance(k, (str, bytes)) and is_bencodable(v)
            for k, v in value.items()
        )
    return False


def bencode_checksum(data: Bencodable) -> bytes:
    """
    Calculate a simple checksum of encoded data.
    
    This is useful for comparing data structures without
    doing a full comparison.
    
    Args:
        data: Data to checksum
        
    Returns:
        8-byte checksum
    """
    encoded = encode(data)
    
    # Simple hash using Python's hash of bytes
    # (Not cryptographically secure, just for quick comparison)
    h = 0x811c9dc5  # FNV offset basis
    for b in encoded:
        h ^= b
        h = (h * 0x01000193) & 0xFFFFFFFF  # FNV prime, 32-bit
    
    return struct.pack('>I', h)


def bencode_equal(data1: Bencodable, data2: Bencodable) -> bool:
    """
    Compare two bencodable values for equality via their encoded form.
    
    This ensures that different Python representations that encode
    to the same bencode are considered equal (e.g., str vs bytes keys).
    
    Args:
        data1: First value
        data2: Second value
        
    Returns:
        True if values encode to the same bencode
    """
    try:
        return encode(data1) == encode(data2)
    except BencodeError:
        return False