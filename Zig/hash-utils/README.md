# Hash Utils (Zig)

A comprehensive hash utility library for Zig, providing implementations of common hash algorithms with zero external dependencies.

## Features

- **Hash Algorithms**: MD5, SHA-1, SHA-256, SHA-512
- **HMAC**: HMAC-SHA256, HMAC-SHA512
- **Key Derivation**: PBKDF2-HMAC-SHA256
- **Utility Functions**: Hex encoding/decoding
- **Incremental Hashing**: Update hash context with multiple data chunks
- **Buffer Operations**: Hash directly into pre-allocated buffers

## Installation

Add to your `build.zig.zon`:

```zig
dependencies = .{
    .hash_utils = .{
        .path = "path/to/hash-utils",
    },
},
```

Then in your `build.zig`:

```zig
const hash_utils = b.dependency("hash_utils", .{
    .target = target,
    .optimize = optimize,
});
exe.root_module.addImport("hash-utils", hash_utils.module("hash-utils"));
```

## Usage

### Basic Hashing

```zig
const std = @import("std");
const hash = @import("hash-utils");

pub fn main() !void {
    const allocator = std.heap.page_allocator;

    // One-shot hashing
    const md5 = try hash.Md5.hashHex(allocator, "Hello, World!");
    defer allocator.free(md5);
    std.debug.print("MD5: {s}\n", .{md5});

    const sha256 = try hash.Sha256.hashHex(allocator, "Hello, World!");
    defer allocator.free(sha256);
    std.debug.print("SHA-256: {s}\n", .{sha256});
}
```

### Incremental Hashing

```zig
var ctx = hash.Sha256.init();
ctx.update("Part 1");
ctx.update("Part 2");
ctx.update("Part 3");

var digest: [32]u8 = undefined;
ctx.final(&digest);

const hex = try hash.toHex(allocator, &digest);
defer allocator.free(hex);
```

### Generic Hash Function

```zig
const HashAlgorithm = hash.HashAlgorithm;

// Use the generic hashWith function
const md5 = try hash.hashWith(allocator, data, .md5);
const sha1 = try hash.hashWith(allocator, data, .sha1);
const sha256 = try hash.hashWith(allocator, data, .sha256);
const sha512 = try hash.hashWith(allocator, data, .sha512);
```

### HMAC

```zig
const key = "secret_key";
const message = "Message to authenticate";

// HMAC-SHA256
const hmac_sha256 = try hash.HmacSha256.hashHex(allocator, key, message);
defer allocator.free(hmac_sha256);

// HMAC-SHA512
const hmac_sha512 = try hash.HmacSha512.hashHex(allocator, key, message);
defer allocator.free(hmac_sha512);
```

### PBKDF2 Key Derivation

```zig
const password = "user_password";
const salt = "random_salt";
const iterations: u32 = 10000;
const key_len: usize = 32;

const derived_key = try hash.pbkdf2Sha256Hex(
    allocator,
    password,
    salt,
    iterations,
    key_len
);
defer allocator.free(derived_key);
```

### Hex Conversion

```zig
const bytes = [_]u8{ 0xDE, 0xAD, 0xBE, 0xEF };

// To lowercase hex
const hex_lower = try hash.toHex(allocator, &bytes);
defer allocator.free(hex_lower); // "deadbeef"

// To uppercase hex
const hex_upper = try hash.toHexUpper(allocator, &bytes);
defer allocator.free(hex_upper); // "DEADBEEF"

// From hex to bytes
const decoded = try hash.fromHex(allocator, "deadbeef");
defer allocator.free(decoded);

// Validate hex string
if (hash.isValidHex("0123456789abcdef")) {
    // Valid hex string
}
```

### Buffer Operations

```zig
// Hash directly into a buffer
var buffer: [64]u8 = undefined;
const len = try hash.hashInto(&buffer, "data", .sha256);

// Hash to hex string in buffer
var hex_buffer: [128]u8 = undefined;
const hex_len = try hash.hashHexInto(&hex_buffer, "data", .sha512);
```

## API Reference

### Hash Types

| Type | Digest Size | Hex Length |
|------|-------------|------------|
| MD5 | 16 bytes | 32 chars |
| SHA-1 | 20 bytes | 40 chars |
| SHA-256 | 32 bytes | 64 chars |
| SHA-512 | 64 bytes | 128 chars |

### Functions

#### `hashWith(allocator, data, algorithm)`
Generic hash function that accepts a `HashAlgorithm` enum.

#### `hashInto(buffer, data, algorithm)`
Hash directly into a pre-allocated buffer. Returns bytes written.

#### `hashHexInto(buffer, data, algorithm)`
Hash to hex string directly into a pre-allocated buffer. Returns chars written.

#### `toHex(allocator, data)`
Convert bytes to lowercase hex string.

#### `toHexUpper(allocator, data)`
Convert bytes to uppercase hex string.

#### `fromHex(allocator, hex)`
Convert hex string to bytes.

#### `isValidHex(hex)`
Check if string is valid hexadecimal.

### Hash Context Methods

Each hash type (Md5, Sha1, Sha256, Sha512) provides:

- `init()` - Create new context
- `update(data)` - Add data to hash
- `final(out)` - Finalize and write digest to buffer
- `hash(data)` - One-shot hash, returns digest array
- `hashHex(allocator, data)` - One-shot hash, returns hex string

### HMAC Types

- `HmacSha256` - HMAC with SHA-256
- `HmacSha512` - HMAC with SHA-512

### Key Derivation

- `pbkdf2Sha256(allocator, password, salt, iterations, key_len)` - PBKDF2 with SHA-256
- `pbkdf2Sha256Hex(allocator, password, salt, iterations, key_len)` - PBKDF2 returning hex

## Building

```bash
# Build
zig build

# Run tests
zig build test

# Run examples
zig build run-basic
zig build run-advanced
```

## Test Vectors

This library uses well-known test vectors from:
- RFC 1321 (MD5)
- RFC 3174 (SHA-1)
- FIPS 180-4 (SHA-256, SHA-512)
- RFC 4231 (HMAC)
- RFC 6070 (PBKDF2)

## License

MIT License - Part of the AllToolkit project.