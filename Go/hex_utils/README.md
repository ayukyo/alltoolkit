# Hex Utils

A comprehensive Go library for hexadecimal encoding, decoding, and manipulation with zero external dependencies.

## Features

- **Basic Encoding/Decoding**: Convert between bytes and hex strings
- **String Utilities**: Encode/decode strings to/from hex
- **Validation**: Check and validate hex strings with detailed error messages
- **Case Handling**: Support for both uppercase and lowercase hex
- **Hex Dumping**: Multiple output formats (xxd-style, compact, C-style, Python-style)
- **Integer Conversion**: Convert between integers and hex strings
- **Bitwise Operations**: XOR operations on hex strings
- **Byte Order**: Reverse hex strings for endianness conversion
- **Streaming**: HexReader for streaming hex decoding

## Installation

```bash
go get github.com/ayukyo/alltoolkit/Go/hex_utils
```

## Quick Start

```go
package main

import (
    "fmt"
    hexutils "github.com/ayukyo/alltoolkit/Go/hex_utils"
)

func main() {
    // Basic encoding
    data := []byte("Hello, World!")
    encoded := hexutils.HexEncode(data)
    fmt.Println(encoded) // 48656c6c6f2c20576f726c6421

    // Basic decoding
    decoded, _ := hexutils.HexDecode("48656c6c6f")
    fmt.Println(string(decoded)) // Hello

    // String utilities
    hexStr := hexutils.HexEncodeString("Hello")
    original, _ := hexutils.HexDecodeToString(hexStr)

    // Validation
    if hexutils.IsHex("48656c6c6f") {
        fmt.Println("Valid hex!")
    }

    // Hex dump (xxd-style)
    fmt.Println(hexutils.HexDump(data))

    // Integer conversion
    num, _ := hexutils.HexToInt("ff")
    fmt.Println(num) // 255
    fmt.Println(hexutils.IntToHex(255)) // ff
}
```

## API Reference

### Encoding/Decoding

| Function | Description |
|----------|-------------|
| `HexEncode(data []byte) string` | Encode bytes to hex string |
| `HexDecode(s string) ([]byte, error)` | Decode hex string to bytes |
| `HexEncodeString(s string) string` | Encode string to hex |
| `HexDecodeToString(hexStr string) (string, error)` | Decode hex to string |
| `HexEncodeUpper(data []byte) string` | Encode to uppercase hex |
| `HexDecodeIgnoreCase(s string) ([]byte, error)` | Decode hex ignoring case |

### Validation

| Function | Description |
|----------|-------------|
| `IsHex(s string) bool` | Check if string is valid hex |
| `ValidateHex(s string) error` | Validate with detailed error |

### Hex Dump Formats

| Function | Description |
|----------|-------------|
| `HexDump(data []byte) string` | xxd-style hex dump |
| `HexDumpCompact(data []byte) string` | Space-separated hex bytes |
| `HexDumpCStyle(data []byte, varName string) string` | C array format |
| `HexDumpPythonStyle(data []byte) string` | Python bytes format |

### Integer Conversion

| Function | Description |
|----------|-------------|
| `HexToInt(hexStr string) (int64, error)` | Convert hex to int64 |
| `IntToHex(n int64) string` | Convert int64 to hex |
| `IntToHexPadded(n int64, width int) string` | Convert with zero padding |

### Bitwise Operations

| Function | Description |
|----------|-------------|
| `XorHex(hex1, hex2 string) (string, error)` | XOR two hex strings |
| `ReverseHex(hexStr string) (string, error)` | Reverse byte order |

### Streaming

```go
reader, err := hexutils.NewHexReader("48656c6c6f")
buf := make([]byte, 3)
n, err := reader.Read(buf)
reader.Reset()
```

### Aliases

| Function | Description |
|----------|-------------|
| `BytesToHex(data []byte) string` | Alias for HexEncode |
| `HexToBytes(s string) ([]byte, error)` | Alias for HexDecode |

## Error Types

```go
var (
    ErrInvalidHexLength  = errors.New("hex string must have even length")
    ErrInvalidHexChar    = errors.New("hex string contains invalid characters")
    ErrEmptyInput        = errors.New("input cannot be empty")
)
```

## Examples

### Hex Dump Output

```go
data := []byte("Hello, World! This is a test.")
fmt.Println(hexutils.HexDump(data))
```

Output:
```
00000000: 4865 6c6c 6f2c 2057 6f72 6c64 2120 5468  Hello, World! Th
00000010: 6973 2069 7320 6120 7465 7374 2e              is is a test.
```

### C-Style Output

```go
data := []byte{0x48, 0x65, 0x6c, 0x6c, 0x6f}
fmt.Println(hexutils.HexDumpCStyle(data, "hello"))
```

Output:
```c
unsigned char hello[] = {
    0x48, 0x65, 0x6c, 0x6c, 0x6f
};
```

### Python-Style Output

```go
data := []byte{0x48, 0x65, 0x6c, 0x6c, 0x6f}
fmt.Println(hexutils.HexDumpPythonStyle(data))
```

Output:
```python
b'\x48\x65\x6c\x6c\x6f'
```

## Testing

Run the test suite:

```bash
go test -v
```

Run benchmarks:

```bash
go test -bench=.
```

## License

MIT License