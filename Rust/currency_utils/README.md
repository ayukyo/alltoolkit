# Currency Utils

A comprehensive currency formatting and conversion utility library for Rust.

## Features

- **Format currency amounts** with proper symbols, separators, and decimal places
- **Parse currency strings** like "$1,234.56" or "¥100,000"
- **Convert between currencies** using hardcoded exchange rates
- **Currency arithmetic** - add, subtract, multiply, divide money values
- **Cross-currency operations** - combine different currencies with automatic conversion
- **20+ supported currencies** - USD, EUR, GBP, JPY, CNY, and more
- **Customizable formatting** - symbols, codes, separators, negative formats
- **Number to words** - format amounts as spoken words
- **Zero external dependencies** - uses only Rust standard library

## Supported Currencies

| Code | Name | Symbol | Decimal Places |
|------|------|--------|----------------|
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
| + 9 more | | | |

## Installation

Add to your `Cargo.toml`:

```toml
[dependencies]
currency_utils = "0.1.0"
```

## Usage

### Basic Formatting

```rust
use currency_utils::{Currency, CurrencyUtils};

let utils = CurrencyUtils::new();

// Format amounts
println!("{}", utils.format(1234.56, Currency::USD));  // "$1,234.56"
println!("{}", utils.format(1234.56, Currency::EUR));  // "1.234,56 €"
println!("{}", utils.format(1234567.0, Currency::JPY)); // "¥1,234,567"
```

### Money Struct

```rust
use currency_utils::{Currency, Money};

let usd = Money::usd(100.0);
let eur = Money::eur(92.0);
let cny = Money::cny(724.0);

println!("{}", usd); // "$100.00"
```

### Currency Conversion

```rust
use currency_utils::{Currency, CurrencyUtils};

let utils = CurrencyUtils::new();

// Convert $100 to EUR
let eur = utils.convert(100.0, Currency::USD, Currency::EUR);
println!("$100 = €{}", eur); // ≈ €92

// Convert and format in one step
let formatted = utils.convert_and_format(100.0, Currency::USD, Currency::JPY);
println!("{}", formatted); // "¥14,950"
```

### Parsing Currency Strings

```rust
use currency_utils::{Currency, Money};

let money: Money = "$1,234.56".parse().unwrap();
println!("Amount: {}, Currency: {}", money.amount, money.currency);

let jpy: Money = "¥100,000".parse().unwrap();
println!("{} yen", jpy.amount);
```

### Money Arithmetic

```rust
use currency_utils::{Currency, CurrencyUtils, Money};

let utils = CurrencyUtils::new();

let m1 = Money::usd(100.0);
let m2 = Money::usd(50.0);

// Same currency arithmetic
let sum = utils.add(m1, m2);        // $150.00
let diff = utils.subtract(m1, m2);  // $50.00
let doubled = utils.multiply(m1, 2.0); // $200.00

// Cross-currency arithmetic
let eur = Money::eur(92.0); // ≈ $100
let total = utils.add(m1, eur); // ≈ $200
```

### Format Options

```rust
use currency_utils::{Currency, CurrencyUtils, FormatOptions};

let utils = CurrencyUtils::new();

// Without symbol
let options = FormatOptions::new().with_symbol(false);
println!("{}", utils.format_with_options(1234.56, Currency::USD, &options));
// Output: "1,234.56"

// With currency code
let options = FormatOptions::new().with_code(true);
println!("{}", utils.format_with_options(1234.56, Currency::USD, &options));
// Output: "$1,234.56 USD"

// Parentheses for negative
let options = FormatOptions::new().with_parentheses_for_negative(true);
println!("{}", utils.format_with_options(-1234.56, Currency::USD, &options));
// Output: "($1,234.56)"
```

### Format as Words

```rust
use currency_utils::{Currency, CurrencyUtils, Money};

let utils = CurrencyUtils::new();

println!("{}", utils.format_as_words(Money::usd(1234.56)));
// Output: "one thousand two hundred thirty-four Dollars and 56 cents"

println!("{}", utils.format_as_words(Money::usd(1000000.0)));
// Output: "one million Dollars"
```

### Aggregation Functions

```rust
use currency_utils::{Currency, CurrencyUtils, Money};

let utils = CurrencyUtils::new();

let amounts = [
    Money::usd(100.0),
    Money::usd(200.0),
    Money::usd(300.0),
];

let sum = utils.sum(&amounts, Currency::USD);     // $600.00
let avg = utils.average(&amounts, Currency::USD); // $200.00
let min = utils.min(&amounts);                     // $100.00
let max = utils.max(&amounts);                     // $300.00
```

## API Reference

### Currency Enum

- `code()` - Get ISO 4217 code (e.g., "USD")
- `symbol()` - Get currency symbol (e.g., "$")
- `name()` - Get full name (e.g., "US Dollar")
- `decimal_places()` - Get decimal places (0-2)
- `all()` - Get all supported currencies

### Money Struct

- `new(amount, currency)` - Create new Money
- `usd(amount)` / `eur(amount)` / `cny(amount)` / etc. - Convenience constructors
- `format()` - Format with default options
- `convert_to(target, utils)` - Convert to another currency

### CurrencyUtils

- `format(amount, currency)` - Format amount
- `format_with_options(amount, currency, options)` - Format with custom options
- `convert(amount, from, to)` - Convert between currencies
- `parse(string)` - Parse currency string
- `add/subtract/multiply/divide()` - Arithmetic operations
- `compare/equal/less_than/greater_than()` - Comparison
- `sum/average/min/max()` - Aggregation
- `round/round_up/round_down()` - Rounding
- `format_as_words(money)` - Format as spoken words

### FormatOptions

- `with_symbol(bool)` - Include/exclude symbol
- `with_code(bool)` - Include/exclude code
- `with_thousands_separator(bool)` - Use/separate thousands
- `with_decimal_places(u8)` - Custom decimal places
- `with_parentheses_for_negative(bool)` - Use parentheses for negatives

## Notes

- Exchange rates are **hardcoded approximate values** for demonstration
- In production, use real-time rates from a currency API
- Rates are relative to USD as base currency
- Formatting respects locale conventions (e.g., EUR uses comma as decimal separator)

## License

MIT License