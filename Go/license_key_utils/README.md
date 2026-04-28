# License Key Utils

License key generation and validation utilities for Go. Supports multiple key formats with checksums and expiration.

## Features

- 🔑 **Multiple Key Formats**: Standard (XXXX-XXXX-XXXX-XXXX), UUID-style, Compact
- ✅ **Checksum Validation**: Built-in checksum for key verification
- ⏰ **Expiration Support**: Keys with embedded expiry dates
- 🏷️ **Product Binding**: Keys bound to specific products
- 🔒 **No Confusing Characters**: Excludes I, O, 0, 1 to avoid confusion
- ⚡ **Zero Dependencies**: Pure Go standard library

## Installation

```go
import "github.com/ayukyo/alltoolkit/Go/license_key_utils"
```

## Quick Start

### Basic Key Generation

```go
package main

import (
    "fmt"
    "github.com/ayukyo/alltoolkit/Go/license_key_utils"
)

func main() {
    // Generate a simple license key
    key, _ := license_key_utils.Generate()
    fmt.Println(key)  // Output: XXXX-XXXX-XXXX-XXXX
}
```

### Custom Configuration

```go
config := license_key_utils.KeyConfig{
    Format:     license_key_utils.FormatStandard,
    Segments:   4,
    SegmentLen: 5,
    Separator:  "-",
    Prefix:     "PROD-",
    Suffix:     "-ENT",
}

key, _ := license_key_utils.GenerateWithConfig(config)
// Output: PROD-XXXXX-XXXXX-XXXXX-XXXXX-ENT
```

### UUID Format

```go
config := license_key_utils.KeyConfig{
    Format: license_key_utils.FormatUUID,
}

key, _ := license_key_utils.GenerateWithConfig(config)
// Output: XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX
```

### Compact Format

```go
config := license_key_utils.KeyConfig{
    Format: license_key_utils.FormatCompact,
}

key, _ := license_key_utils.GenerateWithConfig(config)
// Output: XXXXXXXXXXXXXXXX (no separators)
```

## Key with Checksum

```go
config := license_key_utils.KeyConfig{
    Format:     license_key_utils.FormatStandard,
    Segments:   4,
    SegmentLen: 4,
    Separator:  "-",
    Secret:     "your-secret-key",
}

// Generate key with checksum
key, _ := license_key_utils.GenerateWithChecksum(config)
// Output: XXXX-XXXX-XXXX-XXXX-XXXX (last 4 chars are checksum)

// Validate key
err := license_key_utils.ValidateChecksum(key, config)
if err != nil {
    fmt.Println("Invalid key")
}
```

## Product-Bound Keys

```go
productID := "MY-APP-001"
config := license_key_utils.DefaultConfig()

// Generate product-specific key
key, _ := license_key_utils.GenerateProductKey(productID, config)

// Validate for specific product
err := license_key_utils.ValidateProductKey(key, productID, config)
if err != nil {
    fmt.Println("Invalid product key")
}
```

## Keys with Expiration

```go
config := license_key_utils.DefaultConfig()

// Generate key valid for 30 days
key, _ := license_key_utils.GenerateWithExpiry(config, 30)

// Check if expired
err := license_key_utils.ValidateExpiry(key, config)
if err == license_key_utils.ErrKeyExpired {
    fmt.Println("Key has expired")
}
```

## Batch Generation

```go
config := license_key_utils.DefaultConfig()

// Generate 100 unique keys
keys, _ := license_key_utils.GenerateBatch(100, config)

for i, key := range keys {
    fmt.Printf("Key %d: %s\n", i+1, key)
}
```

## Key Parsing

```go
key := "ABCD-EFGH-IJKL-MNOP"

lk, err := license_key_utils.ParseKey(key)
if err != nil {
    panic(err)
}

fmt.Println("Format:", lk.Metadata["format"])  // standard, uuid, or compact
fmt.Println("Issue Date:", lk.IssueDate)
```

## Key Masking

```go
config := license_key_utils.DefaultConfig()
key := "ABCD-EFGH-IJKL-MNOP"

masked := license_key_utils.MaskKey(key, config)
fmt.Println(masked)  // Output: ****-****-****-MNOP
```

## Key Reformatting

```go
// Convert compact key to standard format
config := license_key_utils.KeyConfig{
    Format:     license_key_utils.FormatStandard,
    SegmentLen: 4,
    Separator:  "-",
}

formatted := license_key_utils.FormatKey("ABCDEFGHIJKLMNOP", config)
// Output: ABCD-EFGH-IJKL-MNOP
```

## API Reference

### Types

```go
type KeyFormat int
    FormatStandard  // XXXX-XXXX-XXXX-XXXX
    FormatUUID      // xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
    FormatCompact   // XXXXXXXXXXXXXXXX
    FormatCustom    // Custom segment lengths

type KeyConfig struct {
    Format        KeyFormat
    Segments      int    // Number of segments
    SegmentLen    int    // Length of each segment
    Separator     string // Separator between segments
    Prefix        string // Optional prefix
    Suffix        string // Optional suffix
    Secret        string // Secret for checksum
    ExpiryDays    int    // Days until expiration
}

type LicenseKey struct {
    Key            string
    ProductID      string
    CustomerID     string
    IssueDate      time.Time
    ExpiryDate     *time.Time
    MaxActivations int
    Activations    int
    Metadata       map[string]string
}
```

### Functions

```go
// Generate a random license key with default configuration
func Generate() (string, error)

// Generate with custom configuration
func GenerateWithConfig(config KeyConfig) (string, error)

// Generate with built-in checksum
func GenerateWithChecksum(config KeyConfig) (string, error)

// Validate key checksum
func ValidateChecksum(key string, config KeyConfig) error

// Generate with expiration
func GenerateWithExpiry(config KeyConfig, expiryDays int) (string, error)

// Validate key expiration
func ValidateExpiry(key string, config KeyConfig) error

// Generate multiple unique keys
func GenerateBatch(count int, config KeyConfig) ([]string, error)

// Parse a license key
func ParseKey(key string) (*LicenseKey, error)

// Generate product-specific key
func GenerateProductKey(productID string, config KeyConfig) (string, error)

// Validate product-specific key
func ValidateProductKey(key, productID string, config KeyConfig) error

// Reformat a key
func FormatKey(key string, config KeyConfig) string

// Mask a key for display
func MaskKey(key string, config KeyConfig) string

// Get default configuration
func DefaultConfig() KeyConfig
```

## Errors

```go
var (
    ErrInvalidKeyFormat   // Key format is invalid
    ErrKeyExpired         // Key has expired
    ErrInvalidChecksum    // Checksum validation failed
    ErrTooManyActivations // Activation limit reached
)
```

## Character Set

Keys use only non-confusing characters:
- **Uppercase letters**: A-Z (excluding I, O)
- **Digits**: 2-9 (excluding 0, 1)

This avoids confusion between:
- I and 1
- O and 0

## License

MIT License