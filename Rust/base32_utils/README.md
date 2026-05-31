# base32_utils

Base32 encoding and decoding utilities for Rust, implementing RFC 4648.

## Features

- **Zero dependencies** - Pure Rust implementation with no external crates
- **RFC 4648 compliant** - Follows the standard Base32 alphabet (A-Z, 2-7)
- **Padding support** - Both padded and unpadded encoding/decoding
- **Validation** - Check if a string is valid Base32
- **Case insensitive** - Decoding handles lowercase input

## Installation

Add to your `Cargo.toml`:

```toml
[dependencies]
base32_utils = "0.1.0"
```

## Usage

```rust
use base32_utils::{encode, decode};

let encoded = encode(b"Hello, World!");
assert_eq!(encoded, "JBSWY3DPFQQFO33SNRSCC===");

let decoded = decode("JBSWY3DPFQQFO33SNRSCC===").unwrap();
assert_eq!(decoded, b"Hello, World!");
```

## API

### encode(data: &[u8]) -> String

Encodes a byte slice into Base32 string with padding.

### encode_nopad(data: &[u8]) -> String

Encodes a byte slice into Base32 string without padding.

### decode(input: &str) -> Result<Vec<u8>, &'static str>

Decodes a Base32 string (with or without padding) back to bytes.

### decode_nopad(input: &str) -> Result<Vec<u8>, &'static str>

Alias for `decode` (padding is ignored).

### is_valid(input: &str) -> bool

Validates if a string is valid Base32.

## RFC 4648 Test Vectors

| Input | Encoded |
|-------|---------|
| `""` | `""` |
| `"f"` | `"MY======"` |
| `"fo"` | `"MZXQ===="` |
| `"foo"` | `"MZXW6==="` |
| `"foob"` | `"MZXW6YQ="` |
| `"fooba"` | `"MZXW6YTB"` |
| `"foobar"` | `"MZXW6YTBOI======"` |

## License

MIT