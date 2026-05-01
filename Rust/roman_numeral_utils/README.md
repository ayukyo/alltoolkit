# Roman Numeral Utils

A zero-dependency Rust library for converting between Arabic numerals and Roman numerals.

## Features

- **Integer to Roman**: Convert integers (1 to 3,999,999) to Roman numerals
- **Roman to Integer**: Parse Roman numeral strings back to integers
- **Validation**: Check if a string is a valid Roman numeral
- **Case-insensitive**: Accepts both uppercase and lowercase input
- **Extended notation**: Supports vinculum (overline) notation for large numbers (≥4000)
- **Zero dependencies**: Uses only Rust standard library

## Installation

Add this to your `Cargo.toml`:

```toml
[dependencies]
roman_numeral_utils = { path = "./roman_numeral_utils" }
```

## Usage

### Basic Conversion

```rust
use roman_numeral_utils::{to_roman, from_roman};

// Integer to Roman numeral
let roman = to_roman(2024).unwrap();
assert_eq!(roman, "MMXXIV");

// Roman numeral to integer
let num = from_roman("MMXXIV").unwrap();
assert_eq!(num, 2024);

// Case-insensitive parsing
let num = from_roman("mmxxiv").unwrap();
assert_eq!(num, 2024);
```

### Validation

```rust
use roman_numeral_utils::is_valid_roman;

assert!(is_valid_roman("MMXXIV"));   // Valid
assert!(is_valid_roman("iv"));        // Valid (lowercase)
assert!(!is_valid_roman("IIII"));     // Invalid: too many I's
assert!(!is_valid_roman("VV"));       // Invalid: V cannot repeat
```

### Lowercase Output

```rust
use roman_numeral_utils::to_roman_lowercase;

let roman = to_roman_lowercase(2024).unwrap();
assert_eq!(roman, "mmxxiv");
```

### Get Symbol Reference

```rust
use roman_numeral_utils::get_symbols;

let symbols = get_symbols();
// Returns: [(1000, "M"), (900, "CM"), (500, "D"), ...]
```

## Supported Numbers

| Range | Description |
|-------|-------------|
| 1 - 3,999 | Standard Roman numerals (I to MMMCMXCIX) |
| 4,000 - 3,999,999 | Extended notation with vinculum (overline) |

### Standard Symbols

| Value | Symbol |
|-------|--------|
| 1 | I |
| 4 | IV |
| 5 | V |
| 9 | IX |
| 10 | X |
| 40 | XL |
| 50 | L |
| 90 | XC |
| 100 | C |
| 400 | CD |
| 500 | D |
| 900 | CM |
| 1000 | M |

## Error Handling

```rust
use roman_numeral_utils::{to_roman, from_roman, RomanError};

// Out of range
match to_roman(0) {
    Err(RomanError::OutOfRange(n)) => println!("Cannot convert {}", n),
    _ => {}
}

// Invalid format
match from_roman("IIII") {
    Err(RomanError::InvalidFormat(s)) => println!("Invalid: {}", s),
    _ => {}
}
```

## Examples

Run the example:

```bash
cargo run --example basic
```

## Testing

Run tests:

```bash
cargo test
```

## Historical Examples

```rust
assert_eq!(to_roman(1066).unwrap(), "MLXVI");      // Battle of Hastings
assert_eq!(to_roman(1215).unwrap(), "MCCXV");      // Magna Carta
assert_eq!(to_roman(1776).unwrap(), "MDCCLXXVI");  // US Independence
assert_eq!(to_roman(1945).unwrap(), "MCMXLV");     // End of WWII
assert_eq!(to_roman(2000).unwrap(), "MM");         // New Millennium
```

## License

MIT