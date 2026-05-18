# ISBN Validator

A fast, zero-dependency ISBN (International Standard Book Number) validation and conversion library for Zig.

## Features

- **ISBN-10 Validation** - Validate 10-digit ISBNs with checksum verification
- **ISBN-13 Validation** - Validate 13-digit ISBNs with checksum verification
- **Format Detection** - Automatically detect ISBN type
- **Format Conversion** - Convert between ISBN-10 and ISBN-13
- **Hyphen Formatting** - Format ISBNs with standard hyphen placement
- **Check Digit Calculation** - Calculate check digits for partial ISBNs
- **X Check Digit Support** - Handle ISBN-10 with X (Roman numeral 10)
- **Zero Allocation Parsing** - Parse and validate without memory allocation

## Installation

Add to your `build.zig.zon`:

```zig
.dependencies = .{
    .isbn_validator = .{
        .path = "path/to/isbn_validator",
    },
},
```

Or copy the `src/` directory to your project.

## Usage

### Basic Validation

```zig
const isbn = @import("isbn_validator");

// Quick validation
if (isbn.isValidIsbn("0-306-40615-2")) {
    // Valid ISBN-10
}

if (isbn.isValidIsbn("978-0-306-40615-7")) {
    // Valid ISBN-13
}
```

### Parse and Inspect

```zig
const std = @import("std");
const isbn = @import("isbn_validator");

const allocator = std.heap.page_allocator;

// Parse ISBN
const parsed = try isbn.Isbn.parse(allocator, "0-306-40615-2");
defer parsed.deinit();

// Check type
switch (parsed.type) {
    .isbn10 => std.debug.print("ISBN-10\n", .{}),
    .isbn13 => std.debug.print("ISBN-13\n", .{}),
    .unknown => std.debug.print("Unknown\n", .{}),
}
```

### Static Parsing (No Allocation)

```zig
const isbn = @import("isbn_validator");

// Parse without allocation - returns type info only
const parsed = try isbn.Isbn.parseStatic("978-0-306-40615-7");

if (parsed.isValid()) {
    // Valid ISBN
}
```

### Format Conversion

```zig
const std = @import("std");
const isbn = @import("isbn_validator");
const allocator = std.heap.page_allocator;

// ISBN-10 to ISBN-13
const isbn10 = try isbn.Isbn.parse(allocator, "0-306-40615-2");
defer isbn10.deinit();

const isbn13 = try isbn10.toIsbn13(allocator);
defer isbn13.deinit();
// isbn13.digits == "9780306406157"

// ISBN-13 to ISBN-10 (only works for 978 prefix)
const isbn13_parsed = try isbn.Isbn.parse(allocator, "978-0-306-40615-7");
defer isbn13_parsed.deinit();

const isbn10_converted = try isbn13_parsed.toIsbn10(allocator);
defer isbn10_converted.deinit();
// isbn10_converted.digits == "0306406152"
```

### Format with Hyphens

```zig
const std = @import("std");
const isbn = @import("isbn_validator");
const allocator = std.heap.page_allocator;

const parsed = try isbn.Isbn.parse(allocator, "9780306406157");
defer parsed.deinit();

const formatted = try parsed.format(allocator);
defer allocator.free(formatted);
// formatted == "978-0-30640-615-7"
```

### Calculate Check Digits

```zig
const isbn = @import("isbn_validator");

// Calculate ISBN-10 check digit
const check10 = try isbn.calculateIsbn10CheckDigit("030640615");
// check10 == '2'

// Calculate ISBN-13 check digit
const check13 = try isbn.calculateIsbn13CheckDigit("978030640615");
// check13 == '7'
```

### Detect ISBN Type

```zig
const isbn = @import("isbn_validator");

const isbn_type = isbn.detectIsbnType("0-306-40615-2");
// isbn_type == .isbn10

const isbn_type2 = isbn.detectIsbnType("978-0-306-40615-7");
// isbn_type2 == .isbn13
```

## API Reference

### Types

```zig
pub const IsbnType = enum {
    isbn10,
    isbn13,
    unknown,
};

pub const IsbnError = error{
    InvalidLength,
    InvalidCharacter,
    InvalidChecksum,
    EmptyInput,
};
```

### Functions

| Function | Description |
|----------|-------------|
| `isValidIsbn(input: []const u8) bool` | Quick validation check |
| `detectIsbnType(input: []const u8) IsbnType` | Detect ISBN type |
| `calculateIsbn10CheckDigit(input: []const u8) IsbnError!u8` | Calculate ISBN-10 check digit |
| `calculateIsbn13CheckDigit(input: []const u8) IsbnError!u8` | Calculate ISBN-13 check digit |

### Isbn Structure

| Method | Description |
|--------|-------------|
| `parse(allocator, input)` | Parse and validate with allocation |
| `parseStatic(input)` | Parse without allocation |
| `deinit()` | Free allocated memory |
| `format(allocator)` | Format with hyphens |
| `toIsbn13(allocator)` | Convert to ISBN-13 |
| `toIsbn10(allocator)` | Convert to ISBN-10 |
| `isValid()` | Check if valid |

## ISBN Format

### ISBN-10
- 10 digits (0-9) with optional 'X' as check digit
- Checksum: `(d1*10 + d2*9 + ... + d10) % 11 == 0`
- Example: `0-306-40615-2`

### ISBN-13
- 13 digits (0-9)
- Prefix: 978 or 979
- Checksum: `(d1 + d2*3 + d3 + d4*3 + ... + d13) % 10 == 0`
- Example: `978-0-306-40615-7`

## Building

```bash
# Build the library
zig build

# Run tests
zig build test

# Run examples
zig build example
```

## License

MIT License