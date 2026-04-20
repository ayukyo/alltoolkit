"""
AllToolkit - Bencode Utilities Examples

Comprehensive usage examples for bencode encoding/decoding.

Author: AllToolkit
License: MIT
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from bencode_utils.mod import (
    Bencoder, encode, decode, decode_to_str_dict, encode_to_file, decode_file,
    bencode_size, validate_bencode, is_bencodable, bencode_checksum, bencode_equal
)


def example_basic_encoding():
    """Example 1: Basic encoding operations."""
    print("=" * 60)
    print("Example 1: Basic Encoding Operations")
    print("=" * 60)
    
    # Encode integers
    print("\n--- Integers ---")
    print(f"encode(42) = {encode(42)}")
    print(f"encode(0) = {encode(0)}")
    print(f"encode(-123) = {encode(-123)}")
    
    # Encode strings
    print("\n--- Strings ---")
    print(f"encode('hello') = {encode('hello')}")
    print(f"encode('') = {encode('')}")
    print(f"encode('你好') = {encode('你好')}")  # UTF-8 encoded
    
    # Encode bytes
    print("\n--- Bytes ---")
    print(f"encode(b'spam') = {encode(b'spam')}")
    print(f"encode(b'\\x00\\x01\\xff') = {encode(b'\\x00\\x01\\xff')}")
    
    # Encode lists
    print("\n--- Lists ---")
    print(f"encode([]) = {encode([])}")
    print(f"encode([1, 2, 3]) = {encode([1, 2, 3])}")
    print(f"encode(['spam', 'eggs']) = {encode(['spam', 'eggs'])}")
    print(f"encode(['spam', 42]) = {encode(['spam', 42])}")
    
    # Encode dictionaries
    print("\n--- Dictionaries ---")
    print(f"encode({{}}) = {encode({})}")
    print(f"encode({{'spam': 'eggs'}}) = {encode({'spam': 'eggs'})}")
    print(f"encode({{'a': 1, 'b': 2}}) = {encode({'a': 1, 'b': 2})}")  # Keys are sorted
    
    print()


def example_basic_decoding():
    """Example 2: Basic decoding operations."""
    print("=" * 60)
    print("Example 2: Basic Decoding Operations")
    print("=" * 60)
    
    # Decode integers
    print("\n--- Integers ---")
    print(f"decode(b'i42e') = {decode(b'i42e')}")
    print(f"decode(b'i0e') = {decode(b'i0e')}")
    print(f"decode(b'i-123e') = {decode(b'i-123e')}")
    
    # Decode strings
    print("\n--- Strings (as bytes) ---")
    print(f"decode(b'5:hello') = {decode(b'5:hello')}")
    print(f"decode(b'0:') = {decode(b'0:')}")
    
    # Decode lists
    print("\n--- Lists ---")
    print(f"decode(b'le') = {decode(b'le')}")
    print(f"decode(b'li1ei2ei3ee') = {decode(b'li1ei2ei3ee')}")
    
    # Decode dictionaries
    print("\n--- Dictionaries ---")
    print(f"decode(b'de') = {decode(b'de')}")
    print(f"decode(b'd4:spam4:eggse') = {decode(b'd4:spam4:eggse')}")
    
    print()


def example_nested_structures():
    """Example 3: Nested and complex structures."""
    print("=" * 60)
    print("Example 3: Nested and Complex Structures")
    print("=" * 60)
    
    # Nested lists
    print("\n--- Nested Lists ---")
    nested_list = [[1, 2], [3, 4], [5, 6]]
    encoded = encode(nested_list)
    print(f"Original: {nested_list}")
    print(f"Encoded: {encoded}")
    print(f"Decoded: {decode(encoded)}")
    
    # Nested dictionaries
    print("\n--- Nested Dictionaries ---")
    nested_dict = {
        "outer": {
            "inner": {
                "value": 42
            }
        }
    }
    encoded = encode(nested_dict)
    print(f"Original: {nested_dict}")
    print(f"Encoded: {encoded}")
    decoded = decode(encoded)
    print(f"Decoded: {decoded}")
    
    # Mixed structure
    print("\n--- Mixed Structure ---")
    mixed = {
        "name": "test",
        "values": [1, 2, 3],
        "metadata": {
            "created": 1234567890,
            "author": "unknown"
        },
        "enabled": True  # Note: bool is not supported, will error
    }
    # Fix: use int instead of bool
    mixed["enabled"] = 1
    encoded = encode(mixed)
    print(f"Original: {mixed}")
    print(f"Encoded length: {len(encoded)} bytes")
    
    print()


def example_torrent_like():
    """Example 4: Torrent-like structure."""
    print("=" * 60)
    print("Example 4: Torrent-like Structure")
    print("=" * 60)
    
    # Create a minimal torrent structure
    torrent_data = {
        "announce": "http://tracker.example.com/announce",
        "announce-list": [
            ["http://tracker1.example.com/announce"],
            ["http://tracker2.example.com/announce"]
        ],
        "info": {
            "name": "example.txt",
            "piece length": 16384,
            "length": 1024,
            "pieces": b"\x00\x01\x02" * 7 + b"\x00\x01\x02\x03\x04",  # 20 bytes SHA1
        },
        "creation date": 1234567890,
        "comment": "Example torrent file",
        "created by": "AllToolkit"
    }
    
    encoded = encode(torrent_data)
    print(f"Announce URL: {torrent_data['announce']}")
    print(f"File name: {torrent_data['info']['name']}")
    print(f"File size: {torrent_data['info']['length']} bytes")
    print(f"Piece length: {torrent_data['info']['piece length']} bytes")
    print(f"Encoded size: {len(encoded)} bytes")
    
    # Decode and verify
    decoded = decode(encoded)
    print(f"\nDecoded announce: {decoded[b'announce']}")
    print(f"Decoded info name: {decoded[b'info'][b'name']}")
    
    # Use decode_to_str_dict for easier key access
    decoded_str = decode_to_str_dict(encoded)
    print(f"\nString-key decode announce: {decoded_str['announce']}")
    
    print()


def example_file_operations():
    """Example 5: File I/O operations."""
    print("=" * 60)
    print("Example 5: File I/O Operations")
    print("=" * 60)
    
    import tempfile
    
    # Create a temp file
    with tempfile.NamedTemporaryFile(mode='wb', suffix='.bencode', delete=False) as f:
        filepath = f.name
    
    try:
        # Write encoded data
        data = {
            "name": "test_data",
            "version": 1,
            "items": [10, 20, 30],
            "metadata": {
                "created": 1234567890,
                "modified": 1234567999
            }
        }
        
        print(f"Writing to: {filepath}")
        encode_to_file(data, filepath)
        
        # Read and decode
        decoded = decode_file(filepath)
        print(f"Decoded from file:")
        print(f"  name: {decoded[b'name']}")
        print(f"  version: {decoded[b'version']}")
        print(f"  items: {decoded[b'items']}")
        
        # Read with string keys
        decoded_str = decode_file_to_str_dict(filepath)
        print(f"\nDecoded with string keys:")
        print(f"  name: {decoded_str['name']}")
        
    finally:
        os.unlink(filepath)
    
    print()


def example_bencode_size():
    """Example 6: Size calculation."""
    print("=" * 60)
    print("Example 6: Size Calculation (without encoding)")
    print("=" * 60)
    
    # Calculate size without actually encoding
    print("\n--- Integer sizes ---")
    print(f"bencode_size(0) = {bencode_size(0)} bytes (i0e)")
    print(f"bencode_size(42) = {bencode_size(42)} bytes (i42e)")
    print(f"bencode_size(999999999) = {bencode_size(999999999)} bytes")
    
    print("\n--- String sizes ---")
    print(f"bencode_size('') = {bencode_size('')} bytes (0:)")
    print(f"bencode_size('hello') = {bencode_size('hello')} bytes (5:hello)")
    print(f"bencode_size('a' * 100) = {bencode_size('a' * 100)} bytes")
    
    print("\n--- List sizes ---")
    print(f"bencode_size([]) = {bencode_size([])} bytes (le)")
    print(f"bencode_size([1, 2, 3]) = {bencode_size([1, 2, 3])} bytes")
    
    print("\n--- Dict sizes ---")
    print(f"bencode_size({{}}) = {bencode_size({})} bytes (de)")
    print(f"bencode_size({{'a': 1}}) = {bencode_size({'a': 1})} bytes")
    
    # Verify with actual encoding
    print("\n--- Verification ---")
    test_data = [1, 2, 3]
    calculated = bencode_size(test_data)
    actual = len(encode(test_data))
    print(f"Calculated: {calculated}, Actual: {actual}, Match: {calculated == actual}")
    
    print()


def example_validation():
    """Example 7: Validation utilities."""
    print("=" * 60)
    print("Example 7: Validation Utilities")
    print("=" * 60)
    
    # Validate bencode data
    print("\n--- Validate bencode ---")
    valid_data = b"i42e"
    is_valid, error = validate_bencode(valid_data)
    print(f"validate_bencode(b'i42e') = valid={is_valid}, error={error}")
    
    invalid_data = b"invalid"
    is_valid, error = validate_bencode(invalid_data)
    print(f"validate_bencode(b'invalid') = valid={is_valid}, error={error}")
    
    # Check if values are bencodable
    print("\n--- Check bencodable ---")
    print(f"is_bencodable(42) = {is_bencodable(42)}")
    print(f"is_bencodable('hello') = {is_bencodable('hello')}")
    print(f"is_bencodable([1, 2, 3]) = {is_bencodable([1, 2, 3])}")
    print(f"is_bencodable({{'a': 1}}) = {is_bencodable({'a': 1})}")
    print(f"is_bencodable(3.14) = {is_bencodable(3.14)}")  # float not supported
    print(f"is_bencodable(None) = {is_bencodable(None)}")
    
    print()


def example_comparison():
    """Example 8: Comparison utilities."""
    print("=" * 60)
    print("Example 8: Comparison Utilities")
    print("=" * 60)
    
    # Compare via checksum
    print("\n--- Checksum comparison ---")
    data1 = {"a": 1, "b": 2}
    data2 = {"a": 1, "b": 2}
    data3 = {"a": 1, "b": 3}
    
    cs1 = bencode_checksum(data1)
    cs2 = bencode_checksum(data2)
    cs3 = bencode_checksum(data3)
    
    print(f"data1 checksum: {cs1.hex()}")
    print(f"data2 checksum: {cs2.hex()}")
    print(f"data3 checksum: {cs3.hex()}")
    print(f"data1 == data2 (checksum): {cs1 == cs2}")
    print(f"data1 == data3 (checksum): {cs1 == cs3}")
    
    # Direct comparison
    print("\n--- Direct comparison ---")
    print(f"bencode_equal(data1, data2) = {bencode_equal(data1, data2)}")
    print(f"bencode_equal(data1, data3) = {bencode_equal(data1, data3)}")
    
    # String vs bytes keys are equal in bencode
    print("\n--- String vs bytes keys ---")
    dict_str = {"a": 1}
    dict_bytes = {b"a": 1}
    print(f"dict_str = {dict_str}")
    print(f"dict_bytes = {dict_bytes}")
    print(f"bencode_equal(dict_str, dict_bytes) = {bencode_equal(dict_str, dict_bytes)}")
    
    print()


def example_custom_bencoder():
    """Example 9: Custom Bencoder instance."""
    print("=" * 60)
    print("Example 9: Custom Bencoder Instance")
    print("=" * 60)
    
    # Default encoding is utf-8
    default_encoder = Bencoder()
    utf8_encoded = default_encoder.encode("café")
    print(f"UTF-8 encoder: {utf8_encoded}")
    print(f"UTF-8 decoded: {default_encoder.decode(utf8_encoded)}")
    
    # Latin-1 encoding
    latin_encoder = Bencoder(encoding='latin-1')
    latin_encoded = latin_encoder.encode("café")
    print(f"\nLatin-1 encoder: {latin_encoded}")
    print(f"Latin-1 decoded: {latin_encoder.decode(latin_encoded)}")
    
    # Custom encoder for torrent operations
    torrent_encoder = Bencoder()
    
    torrent_data = {
        "info": {
            "name": "single_file.txt",
            "piece length": 16384,
            "length": 1024,
            "pieces": b"\x00" * 20
        }
    }
    
    print("\n--- Torrent encoder ---")
    encoded = torrent_encoder.encode(torrent_data)
    print(f"Encoded torrent: {len(encoded)} bytes")
    
    # Decode with string keys
    decoded = torrent_encoder.decode_to_str_dict(encoded)
    print(f"Info name: {decoded['info']['name']}")
    print(f"Piece length: {decoded['info']['piece length']}")
    
    print()


def example_error_handling():
    """Example 10: Error handling."""
    print("=" * 60)
    print("Example 10: Error Handling")
    print("=" * 60)
    
    from bencode_utils.mod import BencodeTypeError, BencodeDecodeError
    
    # Type errors
    print("\n--- Type errors ---")
    try:
        encode(3.14)  # Floats not supported
    except BencodeTypeError as e:
        print(f"encode(3.14) error: {e}")
    
    try:
        encode(None)  # None not supported
    except BencodeTypeError as e:
        print(f"encode(None) error: {e}")
    
    try:
        encode({1: "value"})  # Integer keys not supported
    except BencodeTypeError as e:
        print(f"encode({1: 'value'}) error: {e}")
    
    # Decode errors
    print("\n--- Decode errors ---")
    try:
        decode(b"i042e")  # Leading zeros invalid
    except BencodeDecodeError as e:
        print(f"decode(b'i042e') error: {e}")
    
    try:
        decode(b"i42")  # Missing 'e'
    except BencodeDecodeError as e:
        print(f"decode(b'i42') error: {e}")
    
    try:
        decode(b"invalid")  # Invalid format
    except BencodeDecodeError as e:
        print(f"decode(b'invalid') error: {e}")
    
    print()


def main():
    """Run all examples."""
    print("\n" + "=" * 60)
    print("AllToolkit - Bencode Utilities Examples")
    print("=" * 60 + "\n")
    
    example_basic_encoding()
    example_basic_decoding()
    example_nested_structures()
    example_torrent_like()
    example_file_operations()
    example_bencode_size()
    example_validation()
    example_comparison()
    example_custom_bencoder()
    example_error_handling()
    
    print("=" * 60)
    print("All examples completed!")
    print("=" * 60)


if __name__ == "__main__":
    main()