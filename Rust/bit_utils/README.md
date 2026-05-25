# Bit Utils

A comprehensive collection of bit manipulation utilities for Rust. Zero external dependencies, pure Rust implementation.

## Features

- **Bit Counting**: Count set/unset bits
- **Bit Position Finding**: Find first/last set/unset bits
- **Bit Manipulation**: Set, clear, toggle individual bits
- **Bit Rotation & Reversal**: Rotate and reverse bit sequences
- **Bit Masking**: Create and apply bit masks
- **Gray Code**: Binary to Gray code conversion and vice versa
- **Parity Checking**: Even/odd parity detection
- **Morton Encoding**: Interleave/deinterleave bits (Z-order curve)
- **Power of 2 Utilities**: Next power of 2, power of 2 check
- **Alignment Utilities**: Align up/down to power-of-2 boundaries

## Supported Types

- `u8`
- `u16`
- `u32`
- `u64`
- `u128`
- `usize`

## Usage

### Basic Bit Operations

```rust
use bit_utils::BitOps;

let value: u8 = 0b10101010;

// Count bits
assert_eq!(value.count_ones(), 4);
assert_eq!(value.count_zeros(), 4);

// Find bit positions
assert_eq!(value.first_set_bit(), Some(1));  // LSB is position 0
assert_eq!(value.last_set_bit(), Some(7));   // MSB is position 7

// Check if bit is set
assert!(value.is_bit_set(1));
assert!(!value.is_bit_set(0));

// Manipulate bits
let modified = value.set_bit(0);      // 0b10101011
let modified = value.clear_bit(7);    // 0b00101010
let modified = value.toggle_bit(3);   // 0b10100010
```

### Bit Masking

```rust
use bit_utils::BitOps;

// Create masks
let mask = u8::mask_range(0, 3);   // 0b00001111
let mask = u8::mask_range(4, 7);   // 0b11110000

// Extract bits
let value: u8 = 0b11011010;
let low = value.extract_bits(0, 3);   // 0b1010
let high = value.extract_bits(4, 7);  // 0b1101
```

### Rotation and Reversal

```rust
use bit_utils::BitOps;

let value: u8 = 0b11010010;
let rotated_left = value.rotate_left_bits(2);   // 0b01001101
let rotated_right = value.rotate_right_bits(2); // 0b10110100
let reversed = value.reverse_bits();            // 0b01001011
```

### Gray Code

```rust
use bit_utils::{binary_to_gray, gray_to_binary};

// Convert binary to Gray code
let gray = binary_to_gray(4u8);  // Returns 6

// Convert Gray code back to binary
let binary = gray_to_binary(6u8);  // Returns 4
```

### Parity

```rust
use bit_utils::{has_even_parity, has_odd_parity, parity_bit};

let value: u8 = 0b10101010;
assert!(has_even_parity(value));
assert!(!has_odd_parity(value));
assert_eq!(parity_bit(value), 0);
```

### Morton Encoding (Z-order Curve)

```rust
use bit_utils::{interleave_bits, deinterleave_bits};

// Interleave bits from two 32-bit numbers into 64-bit
let z = interleave_bits(0b11, 0b101);  // Returns 0b111001

// Deinterleave back
let (a, b) = deinterleave_bits(z);  // Returns (0b11, 0b101)
```

### Power of 2 Utilities

```rust
use bit_utils::{next_power_of_two, is_power_of_two};

assert_eq!(next_power_of_two(5u32), Some(8));
assert_eq!(next_power_of_two(8u32), Some(8));
assert!(is_power_of_two(8u8));
assert!(!is_power_of_two(5u8));
```

### Alignment

```rust
use bit_utils::{align_up, align_down};

assert_eq!(align_up(5u32, 4), Some(8));
assert_eq!(align_down(5u32, 4), Some(4));
assert_eq!(align_up(8u32, 4), Some(8));
```

### String Formatting

```rust
use bit_utils::{to_binary_string, to_hex_string};

assert_eq!(to_binary_string(5u8), "00000101");
assert_eq!(to_hex_string(255u8), "FF");
```

### Batch Operations

```rust
use bit_utils::{set_bits, clear_bits, toggle_bits};

let value: u8 = 0;
let result = set_bits(value, &[0, 2, 4]);  // 0b00010101

let value: u8 = 0b11111111;
let result = clear_bits(value, &[0, 2, 4]);  // 0b11101010

let value: u8 = 0b00001010;
let result = toggle_bits(value, &[0, 2, 4]);  // 0b00010101
```

## Trait Methods

The `BitOps` trait provides the following methods:

| Method | Description |
|--------|-------------|
| `count_ones()` | Count set bits |
| `count_zeros()` | Count unset bits |
| `first_set_bit()` | Position of least significant set bit |
| `last_set_bit()` | Position of most significant set bit |
| `first_unset_bit()` | Position of least significant unset bit |
| `is_bit_set(pos)` | Check if bit at position is set |
| `set_bit(pos)` | Set bit at position |
| `clear_bit(pos)` | Clear bit at position |
| `toggle_bit(pos)` | Toggle bit at position |
| `reverse_bits()` | Reverse all bits |
| `rotate_left_bits(n)` | Rotate left by n positions |
| `rotate_right_bits(n)` | Rotate right by n positions |
| `bit_width()` | Number of bits in type |
| `mask_range(start, end)` | Create mask with bits in range set |
| `extract_bits(start, end)` | Extract bits in range |
| `leading_zeros()` | Count leading zeros |
| `trailing_zeros()` | Count trailing zeros |
| `leading_ones()` | Count leading ones |
| `trailing_ones()` | Count trailing ones |

## License

MIT License