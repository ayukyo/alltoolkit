# currency_utils

Comprehensive currency formatting, conversion and arithmetic utilities for Go with zero external dependencies.

## Features

- **20+ Supported Currencies** - USD, EUR, GBP, JPY, CNY, KRW, INR, and more (ISO 4217)
- **Formatting** - Currency symbols, code notation, compact notation
- **Parsing** - Parse currency strings like "$1,234.56" or "€1.234,56"
- **Conversion** - Convert between currencies using exchange rates
- **Arithmetic** - Add, subtract, multiply, divide money values
- **Allocation** - Split amounts evenly or by ratio
- **Number to Words** - Convert amounts to spoken words
- **Zero External Dependencies** - Pure Go standard library

## Installation

```go
import "github.com/ayukyo/alltoolkit/Go/currency_utils"
```

## Quick Start

```go
package main

import (
	"fmt"

	currency "github.com/ayukyo/alltoolkit/Go/currency_utils"
)

func main() {
	// Format
	fmt.Println(currency.MustFormat(1234.56, "USD")) // $1,234.56
	fmt.Println(currency.MustFormat(1234, "JPY"))    // ¥1,234

	// Parse
	m, _ := currency.Parse("$1,234.56 USD")
	fmt.Printf("Parsed: %.2f %s\n", m.Amount, m.Currency)

	// Convert
	usd := currency.Money{Amount: 100, Currency: "USD"}
	eur, _ := currency.Convert(usd, "EUR")
	fmt.Printf("100 USD = %.2f EUR\n", eur.Amount)

	// Arithmetic
	m1 := currency.Money{Amount: 100, Currency: "USD"}
	m2 := currency.Money{Amount: 50, Currency: "USD"}
	sum, _ := currency.Add(m1, m2)
	fmt.Printf("100 + 50 = %.2f USD\n", sum.Amount)

	// Number to words
	words, _ := currency.ToWords(1234.56, "USD")
	fmt.Println(words) // one thousand two hundred thirty four USD and 56/100
}
```

## Supported Currencies

| Code | Name | Symbol | Decimals |
|------|------|--------|----------|
| USD | US Dollar | $ | 2 |
| EUR | Euro | € | 2 |
| GBP | British Pound | £ | 2 |
| JPY | Japanese Yen | ¥ | 0 |
| CNY | Chinese Yuan | ¥ | 2 |
| CAD | Canadian Dollar | C$ | 2 |
| CHF | Swiss Franc | Fr | 2 |
| KRW | South Korean Won | ₩ | 0 |
| INR | Indian Rupee | ₹ | 2 |
| AUD | Australian Dollar | A$ | 2 |
| HKD | Hong Kong Dollar | HK$ | 2 |
| SGD | Singapore Dollar | S$ | 2 |
| NZD | New Zealand Dollar | NZ$ | 2 |
| SEK | Swedish Krona | kr | 2 |
| NOK | Norwegian Krone | kr | 2 |
| DKK | Danish Krone | kr | 2 |
| MXN | Mexican Peso | $ | 2 |
| BRL | Brazilian Real | R$ | 2 |
| RUB | Russian Ruble | ₽ | 2 |
| TRY | Turkish Lira | ₺ | 2 |
| ZAR | South African Rand | R | 2 |
| THB | Thai Baht | ฿ | 2 |
| PLN | Polish Złoty | zł | 2 |
| PHP | Philippine Peso | ₱ | 2 |
| IDR | Indonesian Rupiah | Rp | 0 |
| MYR | Malaysian Ringgit | RM | 2 |
| VND | Vietnamese Dong | ₫ | 0 |
| TWD | Taiwan Dollar | NT$ | 0 |
| AED | UAE Dirham | د.إ | 2 |
| SAR | Saudi Riyal | ﷼ | 2 |
| ILS | Israeli Shekel | ₪ | 2 |
| CZK | Czech Koruna | Kč | 2 |
| HUF | Hungarian Forint | Ft | 0 |
| RON | Romanian Leu | lei | 2 |

## Core Types

```go
// Currency code (ISO 4217)
type Code string

// Money represents a money value with currency
type Money struct {
	Amount   float64
	Currency Code
}

// Formatting options
type FormatOptions struct {
	Symbol         string
	ShowCode       bool
	ShowSymbol     bool
	ThousandsSep   string
	DecimalSep     string
	DecimalPlaces  int
	SymbolPos      SymbolPosition // 0: prefix, 1: suffix
	NegativeParens bool           // use (100) instead of -100
}
```

## Core Functions

### Formatting

```go
// Simple formatting with symbol
Format(1234.56, "USD") // "$1,234.56", nil

// Format with ISO code
FormatCode(1234.56, "USD") // "1,234.56 USD", nil

// Compact format (K/M/B/T)
FormatCompact(1500000, "USD") // "$1.50M USD"

// Custom formatting options
opts := FormatOptions{
	Symbol:         "USD",
	ShowSymbol:     true,
	ThousandsSep:   ".",
	DecimalSep:     ",",
	DecimalPlaces:  2,
	SymbolPos:      SymbolSuffix,
	NegativeParens: true,
}
FormatWithOptions(-1234.56, "USD", opts) // "(1.234,56 USD)"
```

### Parsing

```go
// Parse various formats
Parse("$1,234.56")      // &Money{1234.56, "USD"}
Parse("€1.234,56")      // &Money{1234.56, "EUR"}
Parse("1,234.56 USD")   // &Money{1234.56, "USD"}
Parse("USD 1234.56")    // &Money{1234.56, "USD"}
Parse("¥1,234")          // &Money{1234, "JPY"}
Parse("(100.00)")        // &Money{-100.00, "USD"}

// Parse just a number (remove separators)
ParseAmount("1,234.56") // 1234.56, nil
```

### Conversion

```go
// Convert between currencies
Convert(Money{Amount: 100, Currency: "USD"}, "EUR")
// &Money{Amount: 92.59, Currency: "EUR"}, nil

// Get exchange rate
GetExchangeRate("USD", "EUR") // 1.08, nil

// Direct amount conversion
ConvertAmount(100, "USD", "EUR") // 92.59, nil
```

### Arithmetic

```go
// Add/Subtract
Add(Money{100, "USD"}, Money{50, "USD"})
// Money{150, "USD"}

Subtract(Money{100, "USD"}, Money{30, "USD"})
// Money{70, "USD"}

// Add with different currencies (auto-converts)
Add(Money{100, "USD"}, Money{50, "EUR"})
// Money{154, "USD"} (50 EUR converted to USD first)

// Multiply/Divide
Multiply(Money{100, "USD"}, 1.5)
// Money{150, "USD"}

Divide(Money{100, "USD"}, 4)
// Money{25, "USD"}
```

### Allocation

```go
// Split evenly among recipients
Allocate(Money{100, "USD"}, 3)
// []Money{{33.33, "USD"}, {33.33, "USD"}, {33.34, "USD"}}

// Split by ratio (1:2:3)
SplitRatio(100, "USD", []int{1, 2, 3})
// []Money{{16.67, "USD"}, {33.33, "USD"}, {50, "USD"}}
```

### Comparison

```go
// Compare (returns -1, 0, 1)
Compare(Money{100, "USD"}, Money{200, "USD"}) // -1

// Min/Max
Min(Money{100, "USD"}, Money{200, "USD"})
// Money{100, "USD"}

Max(Money{100, "USD"}, Money{200, "USD"})
// Money{200, "USD"}

// Clamp
Clamp(Money{200, "USD"}, Money{50, "USD"}, Money{150, "USD"})
// Money{150, "USD"}
```

### Number to Words

```go
// To ISO code words
ToWords(1234.56, "USD")
// "one thousand two hundred thirty four USD and 56/100"

// To full English words
ToWordsLong(1234.56, "USD")
// "one thousand two hundred thirty four dollars and 56/100"
```

### Utility

```go
// Round to currency decimals
Round(1.234, "USD")  // 1.23
Round(1.235, "USD")  // 1.24
Round(1.235, "JPY")  // 1 (0 decimals)

// Floor/Ceil
Floor(1.9) // 1
Ceil(1.1)  // 2

// Absolute value
Abs(-5) // 5

// Check sign
IsZero(0)      // true
IsPositive(5) // true
IsNegative(-5) // true
```

## License

MIT