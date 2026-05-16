# CBOR Utilities for Zig

A complete implementation of CBOR (Concise Binary Object Representation, RFC 8949) encoder and decoder in pure Zig.

## Overview

CBOR is a binary data serialization format that is:
- More compact than JSON
- Self-describing (no schema required)
- Binary-safe (handles arbitrary byte strings)
- Extensible (supports custom tags)
- Widely used in WebAuthn, COSE, IoT protocols, and CDDL specifications

## Features

### Encoding Support
- ✅ Positive integers (all sizes: u8, u16, u32, u64)
- ✅ Negative integers (all sizes)
- ✅ Byte strings
- ✅ UTF-8 text strings
- ✅ Arrays
- ✅ Maps (key-value pairs)
- ✅ Tags (semantic annotations)
- ✅ Simple values (false, true, null, undefined)
- ✅ Floats (half, single, double precision)
- ✅ Special floats (NaN, Infinity)

### Decoding Support
- ✅ All CBOR major types (0-7)
- ✅ Automatic length detection
- ✅ UTF-8 validation
- ✅ Depth and length limits for safety
- ✅ Full roundtrip support

### Additional Features
- ✅ JSON representation for debugging
- ✅ Value type introspection
- ✅ Zero external dependencies
- ✅ Comprehensive unit tests

## Usage

### Basic Encoding

```zig
const std = @import("std");
const cbor = @import("cbor");

pub fn main() !void {
    var buffer: [256]u8 = undefined;
    var encoder = cbor.Encoder.init(&buffer);

    // Encode a simple integer
    try encoder.encode(cbor.Value{ .positive_int = 42 });
    // Result: [0x2A]

    // Encode a text string
    encoder.pos = 0;
    try encoder.encode(cbor.Value{ .text_string = "hello" });
    // Result: [0x65, 'h', 'e', 'l', 'l', 'o']
}
```

### Encoding Complex Structures

```zig
const allocator = std.heap.page_allocator;

// Create an array
var arr = try allocator.alloc(cbor.Value, 3);
arr[0] = cbor.Value{ .positive_int = 1 };
arr[1] = cbor.Value{ .text_string = "test" };
arr[2] = cbor.Value{ .simple = .true_val };

var encoder = cbor.Encoder.init(buffer);
try encoder.encode(cbor.Value{ .array = arr });
```

### Decoding

```zig
const data = [_]u8{ 0x83, 0x01, 0x02, 0x03 }; // Array [1, 2, 3]

var decoder = cbor.Decoder.init(&data, allocator);
const value = try decoder.decode();
defer value.deinit(allocator);

// Access the array
for (value.array) |item| {
    std.debug.print("{}\n", .{item.positive_int});
}
```

### Convenience Functions

```zig
// Encode to new buffer (caller owns memory)
const encoded = try cbor.encode(allocator, value);
defer allocator.free(encoded);

// Decode from buffer
const decoded = try cbor.decode(allocator, encoded);
defer decoded.deinit(allocator);

// Check validity
const is_valid = cbor.isValid(encoded, allocator);
```

### JSON Representation

```zig
// Convert CBOR value to JSON string for debugging
const json = try value.toJson(allocator);
defer allocator.free(json);
std.debug.print("JSON: {s}\n", .{json});
```

## API Reference

### Value Types

```zig
pub const Value = union(enum) {
    positive_int: u64,
    negative_int: u64,   // Stored as absolute value - 1
    byte_string: []const u8,
    text_string: []const u8,
    array: []Value,
    map: []MapEntry,
    tag: TaggedValue,
    simple: SimpleValue,
    float: f64,
};
```

### Encoder

```zig
pub const Encoder = struct {
    pub fn init(buffer: []u8) Encoder;
    pub fn encode(self: *Encoder, value: Value) CborError!void;
    pub fn encodeWithOpts(self: *Encoder, value: Value, opts: EncodeOptions) CborError!void;
    pub fn encoded(self: Encoder) []const u8;
};
```

### Decoder

```zig
pub const Decoder = struct {
    pub fn init(data: []const u8, allocator: std.mem.Allocator) Decoder;
    pub fn initWithOpts(data: []const u8, allocator: std.mem.Allocator, opts: DecodeOptions) Decoder;
    pub fn decode(self: *Decoder) CborError!Value;
};
```

### Well-known Tags

```zig
pub const Tag = enum(u64) {
    standard_date_time_string = 0,   // ISO 8601
    epoch_date_time = 1,             // Unix timestamp
    positive_bignum = 2,
    negative_bignum = 3,
    decimal_fraction = 4,
    bigfloat = 5,
    uri = 32,
    base64url = 33,
    base64 = 34,
    regex = 35,
    mime_message = 36,
    uuid = 37,
    self_described_cbor = 55799,
};
```

## CBOR Encoding Reference

| CBOR Value | Encoding |
|------------|----------|
| 0 | `0x00` |
| 1 | `0x01` |
| 23 | `0x17` |
| 24 | `0x18 0x18` |
| 255 | `0x18 0xFF` |
| 256 | `0x19 0x01 0x00` |
| -1 | `0x20` |
| -10 | `0x29` |
| "hello" | `0x65 'h' 'e' 'l' 'l' 'o'` |
| [1,2,3] | `0x83 0x01 0x02 0x03` |
| {"a":1} | `0xA1 0x61 'a' 0x01` |
| true | `0xF5` |
| false | `0xF4` |
| null | `0xF6` |
| undefined | `0xF7` |

## Building

```bash
# Build the library
zig build

# Run tests
zig build test

# Run example
zig build run
```

## Dependencies

- **Zero external dependencies** - Pure Zig implementation
- Uses only `std` library features

## Testing

Run the comprehensive test suite:

```bash
zig build test
```

Tests include:
- Integer encoding/decoding (all sizes)
- String encoding/decoding
- Array and map handling
- Simple values (bool, null)
- Float handling (including special values)
- Roundtrip verification
- Complex nested structures
- JSON output

## License

MIT License

## References

- [RFC 8949 - CBOR](https://datatracker.ietf.org/doc/html/rfc8949)
- [CBOR Wikipedia](https://en.wikipedia.org/wiki/CBOR)