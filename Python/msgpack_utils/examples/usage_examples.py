"""
MessagePack Utilities - Usage Examples

This file demonstrates various use cases for the msgpack_utils module.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from datetime import datetime, timezone
import io
import json

from msgpack_utils.mod import (
    packb, unpackb,
    pack_stream, unpack_stream,
    StreamUnpacker,
    estimate_size,
    compare_with_json,
    is_valid_msgpack,
    Encoder, Decoder
)


def example_basic_encoding():
    """Example: Basic encoding and decoding"""
    print("=" * 60)
    print("Example: Basic Encoding and Decoding")
    print("=" * 60)
    
    # Simple data types
    data_types = [
        None,
        True,
        False,
        42,
        -100,
        3.14159,
        "Hello, World!",
        b"\x00\x01\x02\x03",
        [1, 2, 3, 4, 5],
        {"key": "value", "number": 123}
    ]
    
    for data in data_types:
        packed = packb(data)
        unpacked = unpackb(packed)
        print(f"  {type(data).__name__}: {data}")
        print(f"    → packed {len(packed)} bytes: {packed.hex()}")
        print(f"    → unpacked: {unpacked}")
        print()


def example_complex_data():
    """Example: Complex nested data structures"""
    print("=" * 60)
    print("Example: Complex Nested Data Structures")
    print("=" * 60)
    
    # Complex nested structure
    user_data = {
        "users": [
            {
                "id": 1,
                "name": "Alice",
                "email": "alice@example.com",
                "scores": [95, 87, 92],
                "metadata": {
                    "created_at": datetime(2024, 1, 15, 10, 30, 0, tzinfo=timezone.utc),
                    "tags": ["admin", "verified"],
                    "preferences": {
                        "theme": "dark",
                        "language": "en"
                    }
                }
            },
            {
                "id": 2,
                "name": "Bob",
                "email": "bob@example.com",
                "scores": [88, 91, 85],
                "metadata": {
                    "created_at": datetime(2024, 2, 20, 14, 0, 0, tzinfo=timezone.utc),
                    "tags": ["user"]
                }
            }
        ],
        "pagination": {
            "total": 2,
            "page": 1,
            "per_page": 10
        },
        "binary_data": bytes(range(256))
    }
    
    packed = packb(user_data)
    unpacked = unpackb(packed)
    
    print(f"  Original data structure:")
    print(f"    - {len(user_data['users'])} users")
    print(f"    - User 1: {user_data['users'][0]['name']}")
    print(f"    - User 2: {user_data['users'][1]['name']}")
    print(f"    - Binary data: {len(user_data['binary_data'])} bytes")
    print()
    print(f"  Encoded size: {len(packed)} bytes")
    print(f"  Decoded successfully: {unpacked['users'][0]['name'] == 'Alice'}")
    print()


def example_json_comparison():
    """Example: Compare MessagePack vs JSON"""
    print("=" * 60)
    print("Example: MessagePack vs JSON Comparison")
    print("=" * 60)
    
    # Different types of data to compare
    test_cases = [
        ("Simple object", {"name": "Alice", "age": 30}),
        ("Array of numbers", list(range(100))),
        ("Large string", {"text": "x" * 1000}),
        ("Binary data", {"data": bytes(range(256))}),
        ("Mixed structure", {
            "numbers": list(range(50)),
            "strings": ["hello", "world"] * 25,
            "booleans": [True, False] * 25,
            "nested": {"a": 1, "b": 2, "c": {"d": 3, "e": 4}}
        })
    ]
    
    print()
    for name, data in test_cases:
        result = compare_with_json(data)
        print(f"  {name}:")
        print(f"    JSON:       {result['json_size']} bytes")
        print(f"    MessagePack: {result['msgpack_size']} bytes")
        print(f"    Saved:      {result['bytes_saved']} bytes ({result['percent_smaller']:.1f}%)")
        print()


def example_size_estimation():
    """Example: Size estimation without encoding"""
    print("=" * 60)
    print("Example: Size Estimation")
    print("=" * 60)
    
    test_data = [
        ("Empty dict", {}),
        ("Small dict", {"key": "value"}),
        ("Array of 100 ints", list(range(100))),
        ("String 1000 chars", "x" * 1000),
        ("Nested structure", {"level1": {"level2": {"level3": [1, 2, 3]}}})
    ]
    
    print()
    for name, data in test_data:
        estimated = estimate_size(data)
        actual = len(packb(data))
        print(f"  {name}:")
        print(f"    Estimated: {estimated} bytes")
        print(f"    Actual:    {actual} bytes")
        print(f"    Accuracy:  {'exact' if estimated == actual else 'overestimate'}")
        print()


def example_streaming():
    """Example: Streaming API"""
    print("=" * 60)
    print("Example: Streaming API")
    print("=" * 60)
    
    # Create stream with multiple messages
    stream = io.BytesIO()
    
    messages = [
        {"type": "event", "id": 1, "data": "First message"},
        {"type": "event", "id": 2, "data": "Second message"},
        {"type": "event", "id": 3, "data": "Third message"},
        {"type": "end", "reason": "complete"}
    ]
    
    print("  Writing messages to stream:")
    for msg in messages:
        bytes_written = pack_stream(msg, stream)
        print(f"    Message {msg['id'] if 'id' in msg else 'end'}: {bytes_written} bytes")
    print()
    
    # Read messages from stream
    stream.seek(0)
    unpacker = StreamUnpacker(stream)
    
    print("  Reading messages from stream:")
    for msg in unpacker:
        print(f"    Received: {msg}")
    print()


def example_binary_data():
    """Example: Handling binary data"""
    print("=" * 60)
    print("Example: Binary Data Handling")
    print("=" * 60)
    
    # Various binary data types
    binary_samples = [
        ("Empty bytes", b""),
        ("Small bytes", b"\x00\x01\x02\x03"),
        ("All byte values", bytes(range(256))),
        ("Random-like bytes", bytes([i % 256 for i in range(1000)]))
    ]
    
    print()
    for name, data in binary_samples:
        packed = packb(data)
        unpacked = unpackb(packed)
        
        # Compare sizes with JSON representation
        json_bytes = json.dumps(list(data)).encode('utf-8')
        
        print(f"  {name}:")
        print(f"    Original:  {len(data)} bytes")
        print(f"    MessagePack: {len(packed)} bytes (encoded)")
        print(f"    JSON array: {len(json_bytes)} bytes (alternative)")
        print(f"    Savings:  {len(json_bytes) - len(packed)} bytes")
        print(f"    Round-trip: {data == unpacked}")
        print()


def example_unicode():
    """Example: Unicode string handling"""
    print("=" * 60)
    print("Example: Unicode String Handling")
    print("=" * 60)
    
    unicode_samples = [
        ("English", "Hello, World!"),
        ("Chinese", "你好世界"),
        ("Japanese", "こんにちは世界"),
        ("Korean", "안녕하세요"),
        ("Arabic", "مرحبا"),
        ("Emoji", "😀🎉🚀🌍"),
        ("Mixed", "Hello 世界 🌍 你好!")
    ]
    
    print()
    for name, text in unicode_samples:
        packed = packb(text)
        unpacked = unpackb(packed)
        
        print(f"  {name}:")
        print(f"    Text: '{text}'")
        print(f"    Length: {len(text)} chars, {len(text.encode('utf-8'))} bytes UTF-8")
        print(f"    MessagePack: {len(packed)} bytes")
        print(f"    Round-trip: {text == unpacked}")
        print()


def example_validation():
    """Example: Data validation"""
    print("=" * 60)
    print("Example: Data Validation")
    print("=" * 60)
    
    valid_samples = [
        packb(None),
        packb(42),
        packb("hello"),
        packb([1, 2, 3]),
        packb({"key": "value"})
    ]
    
    invalid_samples = [
        b"not msgpack",
        b"\xc1",  # Invalid marker (never used)
        b"\x92\x01",  # Incomplete array (marker for 2 elements, only 1 provided)
    ]
    
    print()
    print("  Valid MessagePack data:")
    for data in valid_samples:
        print(f"    {data.hex()}: {is_valid_msgpack(data)}")
    print()
    print("  Invalid MessagePack data:")
    for data in invalid_samples:
        print(f"    {data.hex()}: {is_valid_msgpack(data)}")
    print()


def example_encoder_decoder():
    """Example: Direct Encoder/Decoder usage"""
    print("=" * 60)
    print("Example: Direct Encoder/Decoder Usage")
    print("=" * 60)
    
    encoder = Encoder()
    decoder = Decoder(b"")
    
    # Encode multiple values using same encoder
    values = [1, 2, 3, "hello", {"nested": True}]
    
    print()
    print("  Encoding multiple values:")
    for val in values:
        packed = encoder.encode(val)
        print(f"    {val} → {packed.hex()} ({len(packed)} bytes)")
    print()
    
    # Decode with position tracking
    combined = packb([10, 20, 30])
    decoder = Decoder(combined)
    result = decoder.decode()
    
    print("  Decoding with position tracking:")
    print(f"    Data: {combined.hex()}")
    print(f"    Result: {result}")
    print(f"    Position after decode: {decoder.position}")
    print(f"    Remaining bytes: {decoder.remaining}")
    print()


def example_datetime():
    """Example: Datetime handling"""
    print("=" * 60)
    print("Example: Datetime Handling")
    print("=" * 60)
    
    datetime_samples = [
        ("Current UTC", datetime.now(timezone.utc)),
        ("Specific date", datetime(2024, 6, 15, 10, 30, 45, tzinfo=timezone.utc)),
        ("Epoch", datetime(1970, 1, 1, 0, 0, 0, tzinfo=timezone.utc)),
        ("Future date", datetime(2099, 12, 31, 23, 59, 59, tzinfo=timezone.utc))
    ]
    
    print()
    for name, dt in datetime_samples:
        packed = packb(dt)
        unpacked = unpackb(packed)
        
        print(f"  {name}:")
        print(f"    Original: {dt.isoformat()}")
        print(f"    MessagePack: {len(packed)} bytes")
        print(f"    Unpacked: {unpacked.isoformat()}")
        print(f"    Timestamp match: {abs(dt.timestamp() - unpacked.timestamp()) < 0.001}")
        print()


def run_all_examples():
    """Run all examples"""
    print("\n" + "=" * 60)
    print("MessagePack Utilities - Usage Examples")
    print("=" * 60)
    print()
    
    example_basic_encoding()
    example_complex_data()
    example_json_comparison()
    example_size_estimation()
    example_streaming()
    example_binary_data()
    example_unicode()
    example_validation()
    example_encoder_decoder()
    example_datetime()
    
    print("=" * 60)
    print("All examples completed!")
    print("=" * 60)


if __name__ == '__main__':
    run_all_examples()