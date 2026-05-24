# run_length_encoding_utils

Run-Length Encoding (RLE) utilities for Go with zero external dependencies.

## Overview

Run-Length Encoding is a simple but effective compression algorithm that works by replacing consecutive identical elements (runs) with a single instance and its count. This implementation provides comprehensive RLE utilities for bytes, integers, and runes (Unicode characters).

## Installation

```go
import "github.com/ayukyo/alltoolkit/Go/run_length_encoding_utils"
```

## Features

- **Byte RLE**: Encode/decode byte slices with compact binary format
- **Integer RLE**: Encode/decode integer slices
- **Unicode RLE**: Encode/decode rune slices (proper Unicode support)
- **String RLE**: Convenience functions for string encoding
- **Analysis Tools**: Compression ratio, statistics, compressibility check
- **Escape Handling**: Support for escape characters in binary format
- **Zero dependencies**: Pure Go implementation

## Quick Start

### Basic Encoding and Decoding

```go
package main

import (
    "fmt"
    "github.com/ayukyo/alltoolkit/Go/run_length_encoding_utils"
)

func main() {
    // Encode some data
    data := []byte("AAAAABBBCCCCC")
    encoded, err := run_length_encoding_utils.Encode(data)
    if err != nil {
        panic(err)
    }

    fmt.Printf("Original: %s\n", data)
    fmt.Printf("Runs: %s\n", encoded.String()) // "65:5, 66:3, 67:5"
    fmt.Printf("Number of runs: %d\n", encoded.NumRuns())

    // Decode back
    decoded, _ := encoded.Decode()
    fmt.Printf("Decoded: %s\n", decoded) // "AAAAABBBCCCCC"
}
```

### String Encoding

```go
// Convenience function for strings
encoded, _ := run_length_encoding_utils.EncodeString("WWWWWWWWWWWW")
decoded, _ := encoded.DecodeToString()
fmt.Println(decoded) // "WWWWWWWWWWWW"
```

### Compact Binary Format

```go
data := []byte("AAAAABBBBCCCC")
encoded, _ := run_length_encoding_utils.Encode(data)

// Pack into bytes (value + 2-byte count per run)
packed, _ := encoded.Bytes()
fmt.Printf("Compressed: %d bytes (from %d)\n", len(packed), len(data))

// Unpack and decode
decoded, _ := run_length_encoding_utils.FromBytes(packed)
result, _ := decoded.Decode()
```

### Analysis and Statistics

```go
data := []byte("AAAAABBBBCCCCCCCDDDDD")
encoded, _ := run_length_encoding_utils.Encode(data)

stats := encoded.Analyze()

fmt.Printf("Compression ratio: %.2fx\n", stats.CompressionRatio)
fmt.Printf("Longest run: %d\n", stats.LongestRun)
fmt.Printf("Average run length: %.2f\n", stats.AverageRunLength)
fmt.Printf("Most common value: %q\n", stats.MostCommonValue)
```

### Integer RLE

```go
data := []int{1, 1, 1, 2, 2, 3, 3, 3, 3, 3, 4, 4}

runs, _ := run_length_encoding_utils.EncodeInts(data)
// Runs: [{1,3}, {2,2}, {3,5}, {4,2}]

decoded, _ := run_length_encoding_utils.DecodeInts(runs)
```

### Unicode/Rune RLE

```go
text := "🚀🚀🚀🌟🌟🌟🌟"

runs, _ := run_length_encoding_utils.EncodeStringRunes(text)
// Properly handles multi-byte Unicode characters

decoded, _ := run_length_encoding_utils.DecodeRuneRunsToString(runs)
// "🚀🚀🚀🌟🌟🌟🌟"
```

### Checking Compressibility

```go
data := []byte("AAAAAAAAAAAAAA")
if run_length_encoding_utils.IsCompressible(data) {
    encoded, _ := run_length_encoding_utils.Encode(data)
    // Use compressed version
} else {
    // Skip compression - not beneficial
}
```

## API Reference

### Types

```go
type Run struct {
    Value byte
    Count int
}

type Encoded struct {
    Runs []Run
}

type IntRun struct {
    Value int
    Count int
}

type RuneRun struct {
    Value rune
    Count int
}

type Stats struct {
    OriginalSize     int
    EncodedSize      int
    NumRuns          int
    CompressionRatio float64
    AverageRunLength float64
    LongestRun       int
    MostCommonValue  byte
}
```

### Byte Functions

| Function | Description |
|----------|-------------|
| `Encode([]byte) (*Encoded, error)` | Encode byte slice |
| `EncodeString(string) (*Encoded, error)` | Encode string |
| `FromBytes([]byte) (*Encoded, error)` | Decode compact byte format |

### Encoded Methods

| Method | Description |
|--------|-------------|
| `Decode() ([]byte, error)` | Decode to byte slice |
| `DecodeToString() (string, error)` | Decode to string |
| `Bytes() ([]byte, error)` | Compact binary format |
| `BytesWithEscape(escape byte) ([]byte, error)` | Binary with escape handling |
| `String() string` | Human-readable representation |
| `Ratio() float64` | Compression ratio |
| `OriginalSize() int` | Size of original data |
| `NumRuns() int` | Number of runs |
| `Analyze() *Stats` | Get compression statistics |

### Integer Functions

| Function | Description |
|----------|-------------|
| `EncodeInts([]int) ([]IntRun, error)` | Encode integer slice |
| `DecodeInts([]IntRun) ([]int, error)` | Decode integer runs |

### Rune Functions

| Function | Description |
|----------|-------------|
| `EncodeRunes([]rune) ([]RuneRun, error)` | Encode rune slice |
| `DecodeRunes([]RuneRun) ([]rune, error)` | Decode rune runs |
| `EncodeStringRunes(string) ([]RuneRun, error)` | Encode string as runes |
| `DecodeRuneRunsToString([]RuneRun) (string, error)` | Decode to string |

### Utility Functions

| Function | Description |
|----------|-------------|
| `IsCompressible([]byte) bool` | Check if RLE would help |

## Use Cases

### Image Compression
RLE is commonly used in image formats like BMP, TIFF, and PCX for compressing simple graphics with large areas of solid color.

```go
// Simple bitmap row compression
row := []byte{255, 255, 255, 0, 0, 128, 128, 128, 128}
encoded, _ := run_length_encoding_utils.Encode(row)
// Reduces storage when images have large solid areas
```

### Data Transmission
Efficient for transmitting data with many repeated values.

```go
// Sensor data that stays constant
sensorData := []int{42, 42, 42, 42, 42, 42, 42, 42, 43, 43, 43}
runs, _ := run_length_encoding_utils.EncodeInts(sensorData)
```

### Log Compression
Compress logs with repeated status codes or messages.

```go
// Status codes in logs
statuses := []int{200, 200, 200, 404, 404, 200, 200}
runs, _ := run_length_encoding_utils.EncodeInts(statuses)
```

### Unicode Text
Properly handles multi-byte characters for text compression.

```go
// Chinese characters
text := "你好你好你好世界世界"
runs, _ := run_length_encoding_utils.EncodeStringRunes(text)
```

## Performance

### Time Complexity
- **Encoding**: O(n) where n is the input length
- **Decoding**: O(n) where n is the output length
- **Space**: O(k) where k is the number of runs

### When RLE Works Well
- Data with many consecutive repeated values
- Simple graphics and icons
- Log files with repeated status codes
- Sparse data with runs of zeros

### When RLE Doesn't Help
- Random or alternating data (may expand data)
- Data with no consecutive repetitions
- Already compressed data

## Limitations

- Binary format (`Bytes()`) limits count to 65535 per run (uint16)
- For larger runs, use `BytesWithEscape()` or the `Runs` slice directly
- RLE can expand data if there are few repetitions

## License

MIT License