"""
CBOR Utilities - Usage Examples

This file demonstrates common use cases for the CBOR utilities module.
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mod import (
    encode, decode, encode_canonical, encode_to_file, decode_from_file,
    is_valid_cbor, get_cbor_type, estimate_size, dumps, loads,
    cbor2json, json2cbor
)


def main():
    """Run all examples."""
    print("=" * 60)
    print("CBOR Utilities - Usage Examples")
    print("=" * 60)
    
    # Basic Types
    print("\n--- Basic Types ---")
    for value in [0, 100, -1, 3.14, True, False, None, "hello", b"bytes"]:
        encoded = encode(value)
        decoded = decode(encoded)
        print(f"  {value!r:20} -> {len(encoded)} bytes, decoded: {decoded!r}")
    
    # Collections
    print("\n--- Collections ---")
    arr = [1, 2, 3, "four", 5.0]
    encoded = encode(arr)
    decoded = decode(encoded)
    print(f"  Array: {len(encoded)} bytes")
    
    map_data = {"name": "Alice", "age": 30, "active": True}
    encoded = encode(map_data)
    decoded = decode(encoded)
    print(f"  Map: {len(encoded)} bytes")
    
    # Compare with JSON
    print("\n--- CBOR vs JSON ---")
    import json
    test_data = {"name": "Alice", "scores": [95, 87, 92], "active": True}
    json_bytes = len(json.dumps(test_data).encode())
    cbor_bytes = len(encode(test_data))
    print(f"  JSON: {json_bytes} bytes, CBOR: {cbor_bytes} bytes")
    print(f"  Savings: {(1 - cbor_bytes/json_bytes)*100:.1f}%")
    
    # Binary data
    print("\n--- Binary Data ---")
    binary = {"header": b"\x89PNG\r\n\x1a\n", "size": 1024}
    encoded = encode(binary)
    decoded = decode(encoded)
    print(f"  Binary preserved: {decoded['header'] == binary['header']}")
    
    # Big integers
    print("\n--- Big Integers ---")
    big = 2**65
    encoded = encode(big)
    decoded = decode(encoded)
    print(f"  2^65 = {big} -> decoded: {decoded}, match: {big == decoded}")
    
    # Canonical encoding
    print("\n--- Canonical Encoding ---")
    m1 = {"z": 1, "a": 2, "b": 3}
    m2 = {"a": 2, "b": 3, "z": 1}
    c1 = encode_canonical(m1)
    c2 = encode_canonical(m2)
    print(f"  Deterministic: {c1 == c2}")
    
    # Validation
    print("\n--- Validation ---")
    valid_data = encode(42)
    print(f"  Valid CBOR: {is_valid_cbor(valid_data)}")
    print(f"  Invalid CBOR: {is_valid_cbor(b'not cbor')}")
    print(f"  Type of 42: {get_cbor_type(valid_data)}")
    
    # Size estimation
    print("\n--- Size Estimation ---")
    large_array = list(range(1000))
    estimated = estimate_size(large_array)
    actual = len(encode(large_array))
    print(f"  Array of 1000: estimated {estimated}, actual {actual}")
    
    # JSON-like API
    print("\n--- JSON-like API (dumps/loads) ---")
    data = {"message": "Hello, CBOR!", "count": 42}
    encoded = dumps(data)
    decoded = loads(encoded)
    print(f"  dumps/loads: {data == decoded}")
    
    # CBOR to JSON conversion
    print("\n--- CBOR to JSON ---")
    cbor_data = {"text": "hello", "binary": b"\x00\xff"}
    encoded = encode(cbor_data)
    json_obj = cbor2json(encoded)
    print(f"  Binary converted to base64: {json_obj['binary']}")
    
    print("\n" + "=" * 60)
    print("All examples completed!")
    print("=" * 60)


if __name__ == "__main__":
    main()