# Number Utils - Zig

A comprehensive number manipulation library for Zig with zero external dependencies.

## Features

### Number Parsing
- `parseInt(T, input, base)` - Parse integer with specified base (2-36)
- `parseFloat(T, input)` - Parse float from string

### Number Formatting
- `formatIntWithSeparator(value, separator)` - Format integer with thousands separator
- `formatFloat(value, precision)` - Format float with precision
- `formatHex(value, uppercase)` - Format as hexadecimal
- `formatBinary(value)` - Format as binary
- `formatOctal(value)` - Format as octal

### Range Operations
- `clamp(value, min, max)` - Clamp value between bounds
- `inRange(value, min, max)` - Check if value in range
- `lerp(a, b, t)` - Linear interpolation
- `mapRange(value, ...)` - Map value to new range
- `wrap(value, min, max)` - Wrap value within range

### Number Utilities
- `isEven(value)` / `isOdd(value)` - Parity check
- `isPowerOfTwo(value)` - Check if power of 2
- `nextPowerOfTwo(value)` / `prevPowerOfTwo(value)` - Power of 2 utilities
- `countTrailingZeros(value)` / `countLeadingZeros(value)` - Count zeros
- `popcount(value)` - Count set bits
- `digitCount(value)` - Number of digits
- `digitAt(value, position)` - Get digit at position

### Random Number Generation
- `SimpleRandom` struct with:
  - `init(seed)` - Initialize with seed
  - `next()` - Get next random value
  - `nextInt(T, min, max)` - Random integer in range
  - `nextFloat(T)` - Random float 0-1
  - `nextFloatRange(T, min, max)` - Random float in range
  - `shuffle(T, items)` - Shuffle array

### Math Utilities
- `gcd(T, a, b)` - Greatest common divisor
- `lcm(T, a, b)` - Least common multiple
- `factorial(T, n)` - Factorial (with overflow protection)
- `fibonacci(T, n)` - Fibonacci number
- `isPrime(n)` - Prime check
- `isqrt(T, n)` - Integer square root
- `sumOfDigits(n)` - Sum of digits
- `productOfDigits(n)` - Product of digits
- `reverseDigits(n)` - Reverse digits

## Installation

Add to your `build.zig.zon`:

```zig
.dependencies = .{
    .number_utils = .{
        .path = "path/to/number_utils",
    },
},
```

## Usage

```zig
const number_utils = @import("number_utils");

// Parsing
const val = number_utils.parseInt(i32, "12345", 10);

// Formatting
const formatted = number_utils.formatIntWithSeparator(allocator, 1234567, ",");

// Range operations
const clamped = number_utils.clamp(15, 0, 10);

// Random
var rng = number_utils.SimpleRandom.init(42);
const random_val = rng.nextInt(u32, 0, 100);

// Math
const result = number_utils.gcd(u64, 12, 18);
```

## Building

```bash
# Run tests
zig build test

# Run example
zig build example
```

## Zero Dependencies

This library uses only Zig's standard library - no external dependencies required.

## License

MIT