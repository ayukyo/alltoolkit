# Base64 Utils

A comprehensive Base64 and Base32 encoding/decoding library for Rust with zero external dependencies.

## Features

- **Standard Base64** encoding/decoding (RFC 4648)
- **URL-safe Base64** encoding/decoding (no padding)
- **Base32** encoding/decoding (RFC 4648)
- **Automatic variant detection** for decoding
- **No external dependencies** - pure Rust implementation
- **No-std compatible** (with `std` feature disabled)
- **Comprehensive test suite** with edge case coverage

## Installation

Add to your `Cargo.toml`:

```toml
[dependencies]
base64_utils = "0.1.0"
```

## Usage

### Base64 Encoding

```rust
use base64_utils::Base64;

// Standard encoding with padding
let encoded = Base64::encode(b"Hello, World!");
assert_eq!(encoded, "SGVsbG8sIFdvcmxkIQ==");

// URL-safe encoding (no padding)
let url_encoded = Base64::encode_url_safe(b"Hello, World!");
assert_eq!(url_encoded, "SGVsbG8sIFdvcmxkIQ");
```

### Base64 Decoding

```rust
use base64_utils::Base64;

// Standard decoding
let decoded = Base64::decode("SGVsbG8sIFdvcmxkIQ==").unwrap();
assert_eq!(decoded, b"Hello, World!");

// URL-safe decoding
let url_decoded = Base64::decode_url_safe("SGVsbG8sIFdvcmxkIQ").unwrap();

// Auto-detect variant
let auto_decoded = Base64::decode_auto("SGVsbG8sIFdvcmxkIQ==").unwrap();
```

### Base32 Encoding/Decoding

```rust
use base64_utils::Base32;

let encoded = Base32::encode(b"Hello");
assert_eq!(encoded, "JBSWY3DP");

let decoded = Base32::decode("JBSWY3DP").unwrap();
assert_eq!(decoded, b"Hello");

// Lowercase input supported
let decoded_lower = Base32::decode("jbswy3dp").unwrap();
assert_eq!(decoded_lower, b"Hello");
```

### Validation

```rust
use base64_utils::Base64;

assert!(Base64::is_valid("SGVsbG8="));
assert!(!Base64::is_valid("SGVs!m8="));

// Strict validation (requires proper padding)
assert!(Base64::is_valid_strict("SGVsbG8=", true));
```

### Length Calculations

```rust
use base64_utils::Base64;

// Calculate encoded output length
assert_eq!(Base64::encoded_len(5), 8);

// Calculate decoded output length
assert_eq!(Base64::decoded_len(8), 6);
```

## API Reference

### Base64

| Method | Description |
|--------|-------------|
| `encode(data: &[u8])` | Encode to standard Base64 with padding |
| `encode_url_safe(data: &[u8])` | Encode to URL-safe Base64 without padding |
| `encode_with_variant(data, variant)` | Encode with specified variant |
| `decode(input: &str)` | Decode standard Base64 |
| `decode_url_safe(input: &str)` | Decode URL-safe Base64 |
| `decode_auto(input: &str)` | Auto-detect and decode |
| `is_valid(input: &str)` | Check if valid Base64 |
| `is_valid_strict(input, require_padding)` | Strict validation |
| `encoded_len(input_len)` | Calculate encoded length |
| `decoded_len(input_len)` | Calculate decoded length |

### Base32

| Method | Description |
|--------|-------------|
| `encode(data: &[u8])` | Encode to Base32 with padding |
| `decode(input: &str)` | Decode Base32 (case-insensitive) |
| `is_valid(input: &str)` | Check if valid Base32 |

### Variants

```rust
use base64_utils::Base64Variant;

// Standard: A-Z, a-z, 0-9, +, / with = padding
let standard = Base64Variant::Standard;

// URL-safe: A-Z, a-z, 0-9, -, _ no padding
let url_safe = Base64Variant::UrlSafe;
```

## Error Types

```rust
use base64_utils::Base64Error;

// Possible errors:
// - InvalidCharacter(char) - Invalid Base64/Base32 character
// - InvalidPadding - Invalid '=' padding
// - InvalidLength - Invalid string length
// - NonAsciiInput - Input contains non-ASCII characters
```

## Examples

Run the examples:

```bash
cargo run --example basic_usage
```

## No-std Support

Disable the default `std` feature for no-std environments:

```toml
[dependencies]
base64_utils = { version = "0.1.0", default-features = false }
```

## Performance

- Zero-copy encoding where possible
- Pre-allocated output buffers
- Compile-time decode tables
- No regex or complex parsing

## Testing

Run the test suite:

```bash
cargo test
```

## License

MIT License - see LICENSE file for details.

## Contributing

Contributions welcome! Please ensure all tests pass and add tests for new features.