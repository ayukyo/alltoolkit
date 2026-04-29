# msgpack_utils - MessagePack Binary Serialization Utilities

A pure Python implementation of MessagePack serialization format with zero external dependencies.

## Overview

MessagePack is an efficient binary serialization format that is more compact and faster than JSON. This module provides a complete implementation suitable for embedded systems, data storage, network protocols, and any scenario where compact binary serialization is needed.

## Features

- **Pure Python**: No external dependencies, works on any Python 3.x environment
- **Complete Type Support**: All MessagePack types including extensions
- **Streaming API**: Handle large data or multiple messages efficiently
- **Datetime Support**: Automatic datetime encoding/decoding via extension type
- **Size Estimation**: Estimate serialized size without encoding
- **JSON Comparison**: Compare efficiency between MessagePack and JSON
- **Data Validation**: Check if bytes are valid MessagePack

## Installation

Simply copy the `msgpack_utils` folder to your project. No pip install needed.

## Quick Start

```python
from msgpack_utils.mod import packb, unpackb

# Basic encoding
data = {'name': 'Alice', 'age': 30, 'active': True}
packed = packb(data)  # Returns bytes
unpacked = unpackb(packed)  # Returns original data

# Compare with JSON
from msgpack_utils.mod import compare_with_json
result = compare_with_json(data)
print(f"MessagePack saved {result['bytes_saved']} bytes ({result['percent_smaller']}%)")
```

## Supported Types

| Python Type | MessagePack Type | Notes |
|-------------|------------------|-------|
| `None` | nil | |
| `bool` | bool | true/false |
| `int` | integer | Various sizes based on value |
| `float` | float | 64-bit precision |
| `str` | str | UTF-8 encoded |
| `bytes` | bin | Binary data |
| `list`/`tuple` | array | |
| `dict` | map | Keys can be str or int |
| `datetime` | ext | Timestamp extension type |

## API Reference

### Core Functions

```python
packb(obj: Any) -> bytes
    """Encode Python object to MessagePack bytes."""

unpackb(data: bytes) -> Any
    """Decode MessagePack bytes to Python object."""
```

### Streaming Functions

```python
pack_stream(obj: Any, stream: BinaryIO) -> int
    """Encode and write to a binary stream."""

unpack_stream(stream: BinaryIO) -> Any
    """Decode from a binary stream."""

StreamUnpacker(stream: BinaryIO)
    """Iterator for decoding multiple messages from stream."""
```

### Utility Functions

```python
estimate_size(obj: Any) -> int
    """Estimate MessagePack size without encoding."""

compare_with_json(obj: Any) -> dict
    """Compare MessagePack and JSON sizes."""

is_valid_msgpack(data: bytes) -> bool
    """Check if bytes are valid MessagePack."""
```

### Classes

```python
Encoder()
    """MessagePack encoder class."""

Decoder(data: bytes)
    """MessagePack decoder class with position tracking."""
```

### Exceptions

```python
MessagePackError
    """Base exception."""

EncodingError
    """Raised when encoding fails."""

DecodingError
    """Raised when decoding fails."""

InsufficientData
    """Raised when data is incomplete."""
```

## Examples

### Basic Usage

```python
# Simple types
packb(None)        # → b'\xc0'
packb(True)        # → b'\xc3'
packb(42)          # → b'\x2a'
packb("hello")     # → b'\xa5hello'

# Complex structures
data = {
    'users': [
        {'id': 1, 'name': 'Alice'},
        {'id': 2, 'name': 'Bob'}
    ],
    'metadata': {
        'total': 2,
        'page': 1
    }
}
packed = packb(data)
```

### Streaming Multiple Messages

```python
import io

stream = io.BytesIO()

# Write multiple messages
for i in range(5):
    pack_stream({'event': 'data', 'seq': i}, stream)

# Read them back
stream.seek(0)
unpacker = StreamUnpacker(stream)
for msg in unpacker:
    print(msg)
```

### Size Comparison

```python
# Large numeric array
data = list(range(10000))
result = compare_with_json(data)
print(f"JSON: {result['json_size']} bytes")
print(f"MsgPack: {result['msgpack_size']} bytes")
print(f"Saved: {result['percent_smaller']:.1f}%")
```

### Binary Data

```python
# Binary data is efficiently encoded
binary_data = bytes(range(256))
packed = packb({'data': binary_data})

# Compare with JSON (which needs to encode as array)
import json
json_version = json.dumps({'data': list(binary_data)}).encode()
print(f"MsgPack: {len(packed)} bytes")
print(f"JSON: {len(json_version)} bytes")
```

### Datetime Handling

```python
from datetime import datetime, timezone

dt = datetime(2024, 6, 15, 10, 30, 0, tzinfo=timezone.utc)
packed = packb(dt)
unpacked = unpackb(packed)
# Unpacked is datetime object
```

## Size Efficiency

MessagePack typically saves 10-30% compared to JSON for typical data structures:

- **Integers**: 1-9 bytes vs JSON string representation
- **Binary data**: Much more compact than JSON's array-of-numbers encoding
- **Small structures**: Header bytes are often 1 byte vs JSON's delimiters

## File Structure

```
msgpack_utils/
├── mod.py              # Main module with all functionality
├── msgpack_utils_test.py   # Comprehensive test suite
├── README.md           # This documentation
└── examples/
    └── usage_examples.py   # Usage demonstration
```

## Testing

Run tests:

```bash
python msgpack_utils_test.py
```

Run examples:

```bash
python examples/usage_examples.py
```

## Implementation Notes

- Uses big-endian byte order (standard for MessagePack)
- Float values always encoded as 64-bit for precision
- Datetime encoded as MessagePack timestamp extension type (-1)
- Extension types not recognized are returned as (type, data) tuples

## Comparison with Official msgpack Library

This implementation provides:
- ✅ Zero dependencies (official requires installation)
- ✅ Pure Python (easier to debug/modify)
- ✅ Streaming API included
- ✅ Size estimation utilities
- ✅ JSON comparison utilities
- ⚠️ Not as optimized for very large data
- ⚠️ No C acceleration

## License

MIT License - Free for any use.

## References

- [MessagePack Specification](https://msgpack.org/)
- [MessagePack Format Specification](https://github.com/msgpack/msgpack/blob/master/spec.md)