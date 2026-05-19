# Luhn Algorithm Utilities (Zig)

A comprehensive Zig implementation of the Luhn algorithm for validating identification numbers such as credit cards, IMEI numbers, and various national identifiers.

## Features

- **Core Luhn validation**: Validate any number using the Luhn algorithm
- **Check digit calculation**: Compute the check digit for partial numbers
- **Credit card type detection**: Identify Visa, Mastercard, Amex, Discover, JCB, UnionPay, Maestro, Mir, and Diners Club
- **IMEI validation**: Validate International Mobile Equipment Identity numbers
- **National ID validation**: Support for Canadian SIN, South African ID
- **Number formatting**: Format numbers with spaces for readability
- **Test number generation**: Generate valid test numbers for development
- **Zero external dependencies**: Pure Zig implementation using only the standard library

## Installation

### Using Zig's Package Manager

Add to your `build.zig.zon`:

```zig
.{
    .dependencies = .{
        .luhn_utils = .{
            .path = "path/to/luhn_utils",
        },
    },
}
```

### Direct Import

Copy the `src/luhn_utils.zig` file to your project and import:

```zig
const luhn = @import("luhn_utils.zig");
```

## Usage

### Basic Validation

```zig
const std = @import("std");
const luhn = @import("luhn_utils");

pub fn main() !void {
    // Validate a credit card number
    const is_valid = try luhn.validate("4242424242424242");
    std.debug.print("Valid: {}\n", .{is_valid});
}
```

### Calculate Check Digit

```zig
const check_digit = try luhn.calculateCheckDigit("7992739871");
std.debug.print("Check digit: {}\n", .{check_digit}); // Output: 7
```

### Detect Card Type

```zig
const card_type = luhn.detectCardType("4242424242424242");
std.debug.print("Card type: {s}\n", .{card_type.name()}); // Output: Visa
```

### Detailed Validation

```zig
const allocator = std.heap.page_allocator;

var result = try luhn.validateWithDetails(allocator, "4242424242424242");
defer result.deinit(allocator);

std.debug.print("Valid: {}\n", .{result.is_valid});
std.debug.print("Card type: {s}\n", .{result.card_type.name()});
std.debug.print("Check digit: {}\n", .{result.check_digit});
std.debug.print("Formatted: {s}\n", .{result.formatted_number});
```

### IMEI Validation

```zig
// Validate IMEI (15 digits)
const is_valid = try luhn.validateIMEI("490154203237518");
```

### Canadian SIN Validation

```zig
const is_valid = try luhn.validateCanadianSIN("046454286");
```

### Format and Clean Numbers

```zig
const allocator = std.heap.page_allocator;

// Add spaces for readability
const formatted = try luhn.formatNumber(allocator, "4242424242424242", 4);
defer allocator.free(formatted);
// Result: "4242 4242 4242 4242"

// Remove spaces and dashes
const cleaned = try luhn.cleanNumber(allocator, "4242-4242-4242-4242");
defer allocator.free(cleaned);
// Result: "4242424242424242"
```

### Generate Test Numbers

```zig
const allocator = std.heap.page_allocator;

// Generate a valid 16-digit number with prefix "4242" (Visa-like)
const test_number = try luhn.generateTestNumber(allocator, "4242", 16);
defer allocator.free(test_number);
```

## API Reference

### Core Functions

| Function | Description |
|----------|-------------|
| `validate(number)` | Validate a number using Luhn algorithm |
| `calculateCheckDigit(number)` | Calculate the Luhn check digit |
| `validateWithDetails(allocator, number)` | Validate with detailed result |
| `detectCardType(number)` | Detect credit card type |
| `hasValidLength(number)` | Check if number has valid length for its type |

### Utility Functions

| Function | Description |
|----------|-------------|
| `cleanNumber(allocator, input)` | Remove spaces and dashes |
| `formatNumber(allocator, number, group_size)` | Add spaces for readability |
| `generateTestNumber(allocator, prefix, length)` | Generate a valid test number |

### Specialized Validation

| Function | Description |
|----------|-------------|
| `validateIMEI(imei)` | Validate IMEI (15 digits) |
| `validateIMEISV(imeisv)` | Validate IMEISV (16 digits) |
| `validateCanadianSIN(sin)` | Validate Canadian SIN (9 digits) |
| `validateSouthAfricanID(id)` | Validate South African ID (13 digits) |

### Types

#### CardType

```zig
pub const CardType = enum {
    visa,
    mastercard,
    amex,
    discover,
    diners_club,
    jcb,
    unionpay,
    maestro,
    mir,
    unknown,
};
```

#### ValidationResult

```zig
pub const ValidationResult = struct {
    is_valid: bool,
    card_type: CardType,
    check_digit: u8,
    computed_check_digit: u8,
    formatted_number: []const u8,
};
```

## Supported Card Types

| Card Type | Pattern | Length |
|-----------|---------|--------|
| Visa | Starts with 4 | 13, 16, 19 |
| Mastercard | 51-55, 2221-2720 | 16 |
| American Express | 34, 37 | 15 |
| Discover | 6011, 644-649, 65, 622126-622925 | 16, 19 |
| Diners Club | 300-305, 36, 38, 39 | 14, 16, 19 |
| JCB | 3528-3589 | 16, 19 |
| UnionPay | 62 | 16, 19 |
| Maestro | 50, 56-69 | 12-19 |
| Mir | 2200-2204 | 16 |

## Building and Testing

```bash
# Run tests
zig build test

# Run example
zig build example

# Build as library
zig build
```

## How the Luhn Algorithm Works

The Luhn algorithm works as follows:

1. Starting from the rightmost digit, double every second digit
2. If the doubled value is greater than 9, subtract 9
3. Sum all the digits
4. If the sum is divisible by 10, the number is valid

Example with `4242424242424242`:

```
Digits:      4  2  4  2  4  2  4  2  4  2  4  2  4  2  4  2
Position:    16 15 14 13 12 11 10 9  8  7  6  5  4  3  2  1

From right to left, double every second position:
Position 2:  4 → 8
Position 4:  4 → 8
Position 6:  4 → 8
... and so on

Sum: 8+2+8+2+8+2+8+2+8+2+8+2+8+2+8+2 = 80

80 % 10 = 0 → Valid!
```

## Test Card Numbers

These are test card numbers that pass Luhn validation but are not real cards:

- Visa: `4242424242424242`, `4111111111111111`
- Mastercard: `5555555555554444`
- Amex: `378282246310005`
- Discover: `6011111111111117`
- JCB: `3530111333300000`

## License

MIT License - Part of the AllToolkit collection.

## Author

Generated by AllToolkit automated development system.