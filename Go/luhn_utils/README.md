# Luhn Algorithm Utilities (Go)

A comprehensive implementation of the Luhn algorithm (also known as the "modulus 10" or "mod 10" algorithm) for validating and generating check digits.

## Features

- **Validate** numbers using the Luhn algorithm
- **Calculate check digits** for partial numbers
- **Generate valid test numbers** for testing
- **Format and parse** numbers with custom separators
- **Identify card types** based on prefixes
- **Find potential errors** in invalid numbers
- **Zero external dependencies** - uses only Go standard library

## Installation

```go
import "github.com/ayukyo/alltoolkit/Go/luhn_utils"
```

## Quick Start

```go
package main

import (
    "fmt"
    "github.com/ayukyo/alltoolkit/Go/luhn_utils"
)

func main() {
    // Validate a credit card number
    valid := luhn_utils.Validate("4532015112830366")
    fmt.Printf("Valid: %v\n", valid) // Valid: true

    // Calculate check digit
    digit, _ := luhn_utils.CalculateCheckDigit("453201511283036")
    fmt.Printf("Check digit: %d\n", digit) // Check digit: 6

    // Generate a test number
    number, _ := luhn_utils.GenerateValidNumber("4", 16)
    fmt.Printf("Generated: %s\n", number) // Generated: 4... (valid Luhn)

    // Identify card type
    cardType := luhn_utils.IdentifyCardType("4111111111111111")
    fmt.Printf("Card type: %s\n", cardType) // Card type: visa
}
```

## API Reference

### Core Functions

#### `Validate(number string) bool`

Validates a number using the Luhn algorithm.

```go
luhn_utils.Validate("4532015112830366") // true (Visa)
luhn_utils.Validate("4532015112830367") // false
luhn_utils.Validate("4532-0151-1283-0366") // true (with formatting)
```

#### `CalculateCheckDigit(number string) (int, error)`

Calculates the Luhn check digit for a given number.

```go
digit, err := luhn_utils.CalculateCheckDigit("453201511283036")
// digit = 6
```

#### `AddCheckDigit(number string) (string, error)`

Appends the check digit to a number.

```go
full, _ := luhn_utils.AddCheckDigit("453201511283036")
// full = "4532015112830366"
```

### Formatting Functions

#### `StripFormatting(number string) string`

Removes all non-digit characters from a number.

```go
luhn_utils.StripFormatting("4532-0151-1283-0366")
// Returns: "4532015112830366"
```

#### `FormatNumber(number string, groupSize int, separator string) string`

Formats a number by grouping digits.

```go
luhn_utils.FormatNumber("4532015112830366", 4, " ")
// Returns: "4532 0151 1283 0366"

luhn_utils.FormatNumber("4532015112830366", 4, "-")
// Returns: "4532-0151-1283-0366"
```

### Generation Functions

#### `GenerateValidNumber(prefix string, length int) (string, error)`

Generates a valid Luhn number with the given prefix.

```go
// Generate Visa-like number (starts with 4, 16 digits)
visa, _ := luhn_utils.GenerateValidNumber("4", 16)

// Generate Amex-like number (starts with 34, 15 digits)
amex, _ := luhn_utils.GenerateValidNumber("34", 15)
```

#### `GenerateBatch(prefix string, count int, length int) ([]string, error)`

Generates multiple valid Luhn numbers.

```go
numbers, _ := luhn_utils.GenerateBatch("4", 5, 16)
// Returns 5 valid 16-digit numbers starting with 4
```

#### `GenerateTestCreditCards(countPerType int) []CardType`

Generates test credit card numbers for various card types.

```go
cards := luhn_utils.GenerateTestCreditCards(2)
for _, card := range cards {
    fmt.Printf("%s: %s\n", card.Type, card.Number)
}
// Output:
// visa: 4...
// mastercard: 5...
// amex: 34...
// ...
```

### Card Type Identification

#### `IdentifyCardType(number string) string`

Identifies the card type based on the number prefix.

```go
luhn_utils.IdentifyCardType("4111111111111111") // "visa"
luhn_utils.IdentifyCardType("5500000000000004") // "mastercard"
luhn_utils.IdentifyCardType("378282246310005")  // "amex"
```

Supported card types:
- `visa` - Visa
- `mastercard` - MasterCard
- `amex` - American Express
- `discover` - Discover
- `jcb` - JCB
- `diners` - Diners Club
- `unionpay` - UnionPay
- `maestro` - Maestro
- `mir` - Mir

### Utility Functions

#### `CalculateLuhnSum(number string) (int, bool)`

Calculates the Luhn sum and returns both the sum and validity.

```go
sum, valid := luhn_utils.CalculateLuhnSum("4532015112830366")
fmt.Printf("Sum: %d, Valid: %v\n", sum, valid)
// Sum: 80, Valid: true
```

#### `FindCheckDigitErrors(number string) []int`

Finds positions where a single digit error would make the number valid.

```go
errors := luhn_utils.FindCheckDigitErrors("4532015112830367")
// Returns positions of potential errors
```

### Validator Class

A convenient class-based interface for working with Luhn numbers.

```go
// Create validator with formatting options
v := luhn_utils.NewValidator(4, "-")

// Validate
v.Validate("4532015112830366") // true

// Calculate check digit
digit, _ := v.CalculateCheckDigit("453201511283036")

// Add check digit
full, _ := v.AddCheckDigit("453201511283036")

// Format with defaults
formatted := v.Format("4532015112830366")
// "4532-0151-1283-0366"

// Strip formatting
clean := v.Strip("4532-0151-1283-0366")
// "4532015112830366"

// Generate valid number
num, _ := v.Generate("4", 16)

// Generate batch
batch, _ := v.GenerateBatch("4", 5, 16)
```

## Use Cases

The Luhn algorithm is used for validating:

- Credit card numbers
- IMEI numbers (International Mobile Equipment Identity)
- National Provider Identifier numbers (US healthcare)
- Canadian Social Insurance Numbers
- Greek Social Security Numbers (AMKA)
- South African ID numbers
- And many other identification numbers

## Testing

Run the tests:

```bash
go test ./...
```

Run benchmarks:

```bash
go test -bench=. ./...
```

## Example Application

See `examples/main.go` for a complete example application.

## License

MIT License