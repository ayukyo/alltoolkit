# ISBN Utilities for Go

A comprehensive Go package for ISBN (International Standard Book Number) validation, generation, conversion, and formatting. Supports both ISBN-10 and ISBN-13 formats with zero external dependencies.

## Features

- ✅ **Validation**: Validate ISBN-10 and ISBN-13 numbers with checksum verification
- 🔄 **Conversion**: Convert between ISBN-10 and ISBN-13 formats
- 🔢 **Generation**: Generate ISBN numbers with automatic check digit calculation
- 📝 **Formatting**: Format ISBN numbers with standard hyphens
- 🧹 **Cleaning**: Remove non-essential characters from ISBN strings
- 📊 **Parsing**: Parse ISBN to extract components

## Installation

```bash
go get github.com/ayukyo/alltoolkit/go/isbn_utils
```

## Usage

### Basic Validation

```go
package main

import (
    "fmt"
    isbn_utils "github.com/ayukyo/alltoolkit/go/isbn_utils"
)

func main() {
    // Validate any ISBN (auto-detects format)
    valid, err := isbn_utils.Validate("0306406152")
    fmt.Println(valid, err) // true, nil
    
    // Validate specific formats
    isbn10Valid, _ := isbn_utils.ValidateISBN10("0306406152")
    isbn13Valid, _ := isbn_utils.ValidateISBN13("9783161484100")
    
    // Quick boolean checks
    if isbn_utils.IsISBN("0306406152") {
        fmt.Println("Valid ISBN!")
    }
}
```

### ISBN Conversion

```go
// ISBN-10 to ISBN-13
isbn13, err := isbn_utils.ToISBN13("0306406152")
// isbn13 = "9780306406157"

// ISBN-13 to ISBN-10 (only for 978 prefix)
isbn10, err := isbn_utils.ToISBN10("9780306406157")
// isbn10 = "0306406152"

// Normalize to ISBN-13
normalized, err := isbn_utils.Normalize("0306406152")
// normalized = "9780306406157"
```

### Check Digit Generation

```go
// Generate ISBN-10 check digit (for 9-digit prefix)
check, err := isbn_utils.GenerateCheckDigit10("030640615")
// check = "2"

// Generate ISBN-13 check digit (for 12-digit prefix)
check, err := isbn_utils.GenerateCheckDigit13("978316148410")
// check = "0"

// Generate complete ISBN
isbn10, err := isbn_utils.GenerateISBN10("030640615")
// isbn10 = "0306406152"

isbn13, err := isbn_utils.GenerateISBN13("978316148410")
// isbn13 = "9783161484100"
```

### Formatting and Cleaning

```go
// Format ISBN with hyphens
formatted := isbn_utils.Format("0306406152")
// formatted = "0-30640-615-2"

formatted13 := isbn_utils.Format("9783161484100")
// formatted13 = "978-3-16148-410-0"

// Clean ISBN (remove hyphens, spaces, etc.)
clean := isbn_utils.Clean("ISBN 0-306-40615-2")
// clean = "0306406152"
```

### Parsing and Type Detection

```go
// Get ISBN type
isbnType, _ := isbn_utils.GetType("0306406152")
// isbnType = "ISBN-10"

// Parse ISBN
parsed, _ := isbn_utils.Parse("978-3-16-148410-0")
fmt.Println(parsed.Number)    // "9783161484100"
fmt.Println(parsed.Type)      // "ISBN-13"
fmt.Println(parsed.Prefix)    // "978"
fmt.Println(parsed.Check)      // "0"
```

## API Reference

### Validation Functions

| Function | Description |
|----------|-------------|
| `Validate(isbn string) (bool, error)` | Validate any ISBN (auto-detect format) |
| `ValidateISBN10(isbn string) (bool, error)` | Validate ISBN-10 |
| `ValidateISBN13(isbn string) (bool, error)` | Validate ISBN-13 |
| `IsISBN(isbn string) bool` | Quick check if string is valid ISBN |
| `IsISBN10(isbn string) bool` | Quick check if string is valid ISBN-10 |
| `IsISBN13(isbn string) bool` | Quick check if string is valid ISBN-13 |

### Conversion Functions

| Function | Description |
|----------|-------------|
| `ToISBN13(isbn10 string) (string, error)` | Convert ISBN-10 to ISBN-13 |
| `ToISBN10(isbn13 string) (string, error)` | Convert ISBN-13 to ISBN-10 (978 prefix only) |
| `Normalize(isbn string) (string, error)` | Normalize to ISBN-13 |

### Generation Functions

| Function | Description |
|----------|-------------|
| `GenerateCheckDigit10(prefix string) (string, error)` | Calculate ISBN-10 check digit |
| `GenerateCheckDigit13(prefix string) (string, error)` | Calculate ISBN-13 check digit |
| `GenerateISBN10(prefix string) (string, error)` | Generate complete ISBN-10 |
| `GenerateISBN13(prefix string) (string, error)` | Generate complete ISBN-13 |

### Utility Functions

| Function | Description |
|----------|-------------|
| `Clean(isbn string) string` | Remove non-essential characters |
| `Format(isbn string) string` | Add hyphens in standard positions |
| `GetType(isbn string) (string, error)` | Get ISBN type (ISBN-10 or ISBN-13) |
| `Parse(isbn string) (*ISBN, error)` | Parse ISBN into components |

## Error Types

```go
var (
    ErrInvalidISBN          = errors.New("invalid ISBN format")
    ErrInvalidChecksum      = errors.New("invalid ISBN checksum")
    ErrInvalidLength        = errors.New("invalid ISBN length")
    ErrConversionNotPossible = errors.New("ISBN conversion not possible")
)
```

## Running Tests

```bash
go test -v
```

## Running Examples

```bash
cd examples && go run main.go
```

## License

MIT License - Part of the AllToolkit project