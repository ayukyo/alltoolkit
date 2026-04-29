"""
Varint Utils - Usage Examples

This file demonstrates practical use cases for variable-length integer encoding.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mod import (
    encode_unsigned, decode_unsigned,
    encode_signed, decode_signed,
    encode_unsigned_batch, decode_unsigned_batch,
    encode_signed_batch, decode_signed_batch,
    zigzag_encode, zigzag_decode,
    VarintWriter, VarintReader,
    size_unsigned, size_signed,
    compare_efficiency,
    encode_int32, decode_int32,
    encode_int64, decode_int64,
    encode_uint32, decode_uint32,
    encode_uint64, decode_uint64,
)


def example_basic_encoding():
    """Basic unsigned varint encoding and decoding."""
    print("=" * 60)
    print("Example 1: Basic Unsigned Encoding")
    print("=" * 60)
    
    # Small values use 1 byte
    for value in [0, 1, 127]:
        encoded = encode_unsigned(value)
        print(f"  {value:6d} -> {encoded.hex():12s} ({len(encoded)} byte)")
    
    print()
    
    # Values 128-16383 use 2 bytes
    for value in [128, 300, 16383]:
        encoded = encode_unsigned(value)
        print(f"  {value:6d} -> {encoded.hex():12s} ({len(encoded)} bytes)")
    
    print()
    
    # Larger values use more bytes
    for value in [16384, 2097151, 2097152]:
        encoded = encode_unsigned(value)
        print(f"  {value:8d} -> {encoded.hex():15s} ({len(encoded)} bytes)")
    
    print()


def example_signed_encoding():
    """Signed varint encoding using ZigZag."""
    print("=" * 60)
    print("Example 2: Signed Encoding (ZigZag)")
    print("=" * 60)
    
    print("  ZigZag maps signed to unsigned so small values stay small:")
    print()
    
    for value in [-3, -2, -1, 0, 1, 2, 3]:
        encoded = encode_signed(value)
        zigzag = zigzag_encode(value)
        print(f"  {value:3d} -> ZigZag: {zigzag:3d} -> Varint: {encoded.hex()} ({len(encoded)} byte)")
    
    print()


def example_batch_operations():
    """Batch encoding and decoding for efficiency."""
    print("=" * 60)
    print("Example 3: Batch Operations")
    print("=" * 60)
    
    # Encode a list of values
    values = [1, 2, 3, 128, 256, 512, 1024, 2048]
    encoded = encode_unsigned_batch(values)
    
    print(f"  Values: {values}")
    print(f"  Encoded: {encoded.hex()}")
    print(f"  Size: {len(encoded)} bytes")
    print()
    
    # Decode back
    decoded = decode_unsigned_batch(encoded)
    print(f"  Decoded: {decoded}")
    
    print()
    
    # Signed batch
    signed_values = [0, 1, -1, 2, -2, 100, -100]
    signed_encoded = encode_signed_batch(signed_values)
    
    print(f"  Signed values: {signed_values}")
    print(f"  Encoded: {signed_encoded.hex()}")
    print(f"  Size: {len(signed_encoded)} bytes")
    
    signed_decoded = decode_signed_batch(signed_encoded)
    print(f"  Decoded: {signed_decoded}")
    
    print()


def example_streaming():
    """Streaming with VarintWriter and VarintReader."""
    print("=" * 60)
    print("Example 4: Streaming (Writer/Reader)")
    print("=" * 60)
    
    # Write values
    writer = VarintWriter()
    writer.write_unsigned(1)
    writer.write_unsigned(300)
    writer.write_signed(-42)
    writer.write_unsigned_batch([10, 20, 30])
    
    data = writer.get_bytes()
    print(f"  Wrote 6 values -> {len(data)} bytes: {data.hex()}")
    print()
    
    # Read values
    reader = VarintReader(data)
    
    values = []
    values.append(reader.read_unsigned())
    values.append(reader.read_unsigned())
    values.append(reader.read_signed())
    values.extend(reader.read_unsigned_batch(3))
    
    print(f"  Read values: {values}")
    print(f"  Bytes read: {reader.bytes_read()}")
    print(f"  Bytes remaining: {reader.bytes_remaining()}")
    
    print()
    
    # Demonstrate iteration
    writer2 = VarintWriter()
    writer2.write_unsigned_batch(list(range(1, 11)))
    
    reader2 = VarintReader(writer2.get_bytes())
    all_values = list(reader2.read_unsigned_all())
    print(f"  Iterate all: {all_values}")
    
    print()


def example_size_calculation():
    """Calculate size before encoding."""
    print("=" * 60)
    print("Example 5: Size Calculation")
    print("=" * 60)
    
    print("  Unsigned sizes:")
    for value in [0, 127, 128, 16383, 16384, 2097151, 2097152]:
        size = size_unsigned(value)
        print(f"    {value:10d} -> {size} byte(s)")
    
    print()
    
    print("  Signed sizes (ZigZag):")
    for value in [0, 1, -1, 63, -64, 64, -65, 1000, -1000]:
        size = size_signed(value)
        print(f"    {value:6d} -> {size} byte(s)")
    
    print()


def example_efficiency_comparison():
    """Compare varint vs fixed-size encoding."""
    print("=" * 60)
    print("Example 6: Efficiency Comparison")
    print("=" * 60)
    
    # Small values - varint is very efficient
    small_values = list(range(100))
    result = compare_efficiency(small_values)
    
    print("  Small values (0-99):")
    print(f"    Varint size: {result['varint_size']} bytes")
    print(f"    Fixed size:  {result['fixed_size']} bytes (8 bytes per value)")
    print(f"    Bytes saved: {result['bytes_saved']}")
    print(f"    Compression: {result['compression_ratio']:.2%}")
    
    print()
    
    # Mixed values
    import random
    random.seed(42)
    mixed_values = [random.randint(-10000, 10000) for _ in range(100)]
    result = compare_efficiency(mixed_values)
    
    print("  Mixed values (random -10000 to 10000):")
    print(f"    Varint size: {result['varint_size']} bytes")
    print(f"    Fixed size:  {result['fixed_size']} bytes")
    print(f"    Bytes saved: {result['bytes_saved']}")
    print(f"    Compression: {result['compression_ratio']:.2%}")
    print(f"    Avg varint:  {result['avg_varint_size']:.2f} bytes/value")
    
    print()
    
    # Large values - varint is less efficient
    large_values = [2**63 - 1] * 10  # Max int64
    result = compare_efficiency(large_values)
    
    print("  Large values (max int64 x 10):")
    print(f"    Varint size: {result['varint_size']} bytes")
    print(f"    Fixed size:  {result['fixed_size']} bytes")
    print(f"    Bytes saved: {result['bytes_saved']} (negative = varint is bigger)")
    print(f"    Compression: {result['compression_ratio']:.2%}")
    
    print()


def example_protocol_buffers():
    """Protocol Buffers style encoding."""
    print("=" * 60)
    print("Example 7: Protocol Buffers Style")
    print("=" * 60)
    
    # int32 - ZigZag + Varint (1-5 bytes)
    print("  int32 encoding:")
    for value in [0, -1, 2147483647, -2147483648]:
        encoded = encode_int32(value)
        decoded, consumed = decode_int32(encoded)
        print(f"    {value:12d} -> {encoded.hex():15s} ({consumed} bytes)")
    
    print()
    
    # uint32 - Unsigned varint (1-5 bytes)
    print("  uint32 encoding:")
    for value in [0, 255, 65535, 4294967295]:
        encoded = encode_uint32(value)
        decoded, consumed = decode_uint32(encoded)
        print(f"    {value:12d} -> {encoded.hex():15s} ({consumed} bytes)")
    
    print()
    
    # int64 - ZigZag + Varint (1-10 bytes)
    print("  int64 encoding:")
    for value in [0, -1, 2**63 - 1, -(2**63)]:
        encoded = encode_int64(value)
        decoded, consumed = decode_int64(encoded)
        print(f"    {value:20d} -> {encoded.hex():25s} ({consumed} bytes)")
    
    print()


def example_database_ids():
    """Practical use case: encoding database IDs."""
    print("=" * 60)
    print("Example 8: Database ID Encoding")
    print("=" * 60)
    
    # Typical database IDs are small positive integers
    ids = [1, 2, 3, 100, 1000, 10000, 100000]
    
    print("  Encoding database IDs:")
    
    # Fixed size (8 bytes each)
    fixed_total = len(ids) * 8
    
    # Varint size
    varint_total = sum(size_unsigned(id) for id in ids)
    
    encoded = encode_unsigned_batch(ids)
    decoded = decode_unsigned_batch(encoded)
    
    print(f"    IDs: {ids}")
    print(f"    Fixed size:  {fixed_total} bytes")
    print(f"    Varint size: {varint_total} bytes")
    print(f"    Saved: {fixed_total - varint_total} bytes ({(fixed_total - varint_total) / fixed_total * 100:.1f}%)")
    print(f"    Roundtrip OK: {decoded == ids}")
    
    print()


def example_network_protocol():
    """Practical use case: network message encoding."""
    print("=" * 60)
    print("Example 9: Network Message Encoding")
    print("=" * 60)
    
    # Simulate a network message with type, flags, payload size
    # Message format: [type: varint][flags: varint][payload_size: varint][payload]
    
    def create_message(msg_type: int, flags: int, payload: bytes) -> bytes:
        """Create a network message with varint headers."""
        writer = VarintWriter()
        writer.write_unsigned(msg_type)
        writer.write_unsigned(flags)
        writer.write_unsigned(len(payload))
        return writer.get_bytes() + payload
    
    def parse_message(data: bytes) -> tuple:
        """Parse a network message."""
        reader = VarintReader(data)
        msg_type = reader.read_unsigned()
        flags = reader.read_unsigned()
        payload_size = reader.read_unsigned()
        payload = data[reader.bytes_read():reader.bytes_read() + payload_size]
        return msg_type, flags, payload
    
    # Create messages
    messages = [
        (1, 0, b"Hello"),
        (2, 1, b"World!"),
        (100, 255, b"A" * 100),
    ]
    
    for msg_type, flags, payload in messages:
        encoded = create_message(msg_type, flags, payload)
        parsed_type, parsed_flags, parsed_payload = parse_message(encoded)
        
        print(f"  Message: type={msg_type}, flags={flags}, payload_len={len(payload)}")
        print(f"    Header: {encoded[:5].hex()}... ({5} bytes)")
        print(f"    Total:  {len(encoded)} bytes")
        print(f"    Parsed: type={parsed_type}, flags={parsed_flags}, payload_ok={parsed_payload == payload}")
        print()
    
    print()


def example_json_like_data():
    """Practical use case: encoding JSON-like data."""
    print("=" * 60)
    print("Example 10: Compact Data Storage")
    print("=" * 60)
    
    # Simulate a record with many small integers
    # Like sensor readings, timestamps, IDs, etc.
    
    record = {
        'id': 1,
        'user_id': 42,
        'timestamp': 1699876543,
        'value': 100,
        'status': 1,
        'flags': 0,
        'count': 500,
        'version': 1,
    }
    
    # Extract values
    values = list(record.values())
    
    # Compare storage
    fixed_size = len(values) * 8
    varint_size = sum(size_signed(v) for v in values)
    
    print("  Record with small integers:")
    print(f"    Values: {values}")
    print(f"    Fixed storage:  {fixed_size} bytes")
    print(f"    Varint storage: {varint_size} bytes")
    print(f"    Savings: {fixed_size - varint_size} bytes ({(fixed_size - varint_size) / fixed_size * 100:.1f}%)")
    
    print()
    
    # Encode and decode
    encoded = encode_signed_batch(values)
    decoded = decode_signed_batch(encoded)
    
    print(f"    Encoded hex: {encoded.hex()}")
    print(f"    Roundtrip OK: {decoded == values}")
    
    print()


if __name__ == '__main__':
    print("\n" + "=" * 60)
    print(" VARINT UTILS - USAGE EXAMPLES")
    print("=" * 60 + "\n")
    
    example_basic_encoding()
    example_signed_encoding()
    example_batch_operations()
    example_streaming()
    example_size_calculation()
    example_efficiency_comparison()
    example_protocol_buffers()
    example_database_ids()
    example_network_protocol()
    example_json_like_data()
    
    print("=" * 60)
    print(" All examples completed!")
    print("=" * 60 + "\n")