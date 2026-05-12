# Bitmask Utils

A comprehensive Python library for bitmask manipulation with zero external dependencies.

## Features

- **Bitmask Class**: Full-featured class for managing bitmasks with method chaining
- **Functional API**: Simple functions for common operations
- **Utility Functions**: Helper functions for bit manipulation
- **Zero Dependencies**: Pure Python standard library implementation

## Installation

```python
from bitmask_utils.mod import Bitmask, from_bits, from_binary, from_hex
```

## Quick Start

### Basic Operations

```python
from bitmask_utils.mod import Bitmask

# Create a bitmask
mask = Bitmask(bits=8)

# Set, clear, toggle bits
mask.set(0).set(2).set(4)  # Set bits 0, 2, 4
mask.clear(0)               # Clear bit 0
mask.toggle(1)              # Toggle bit 1

# Check bits
if mask.has(2):
    print("Bit 2 is set!")

# Get values
print(mask.to_int())   # Integer: 20
print(mask.to_bin())   # Binary: 0b00010100
print(mask.to_hex())   # Hex: 0x14
```

### Multi-bit Operations

```python
# Set multiple bits at once
mask.set_all([0, 1, 2, 3])

# Clear multiple bits
mask.clear_all([0, 2])

# Check multiple bits
if mask.has_all([1, 3]):
    print("Bits 1 and 3 are set!")

if mask.has_any([0, 2]):
    print("Either bit 0 or 2 is set!")
```

### Range Operations

```python
# Set a range of bits
mask.set_range(2, 5)   # Set bits 2-5 inclusive

# Clear a range of bits
mask.clear_range(0, 3)  # Clear bits 0-3 inclusive
```

### Query Operations

```python
# Count bits
print(mask.count_set())    # Number of 1s
print(mask.count_clear())  # Number of 0s

# Find bits
print(mask.first_set())    # First 1 bit position
print(mask.last_set())     # Last 1 bit position

# Get lists of bit positions
print(mask.get_set_bits())   # [0, 2, 4, ...]
print(mask.get_clear_bits()) # [1, 3, 5, ...]
```

### Manipulation Operations

```python
# Invert all bits
mask.invert()

# Shift bits
mask.shift_left(2)
mask.shift_right(2)

# Rotate bits (circular shift)
mask.rotate_left(3)
mask.rotate_right(3)

# Reset or fill
mask.reset()  # Set all to 0
mask.fill()   # Set all to 1
```

### Logical Operations

```python
mask1 = Bitmask(0b11110000, bits=8)
mask2 = Bitmask(0b10101010, bits=8)

# AND, OR, XOR
mask1.and_with(mask2)
mask1.or_with(mask2)
mask1.xor_with(mask2)

# Or use operators
result = mask1 & mask2  # AND
result = mask1 | mask2  # OR
result = mask1 ^ mask2  # XOR
result = ~mask1         # NOT
result = mask1 << 2     # Left shift
result = mask1 >> 2     # Right shift
```

### Comparison Operations

```python
mask1 = Bitmask(0b1010, bits=4)
mask2 = Bitmask(0b1110, bits=4)

# Subset/superset
if mask1.is_subset(mask2):
    print("mask1 is a subset of mask2")

if mask2.is_superset(mask1):
    print("mask2 is a superset of mask1")

# Overlap check
if mask1.overlaps(mask2):
    print("masks have common bits")

if mask1.is_disjoint(mask2):
    print("masks have no common bits")
```

### Functional API

```python
from bitmask_utils.mod import (
    create_bitmask, from_bits, from_binary, from_hex,
    combine_bitmasks, intersect_bitmasks
)

# Create from different sources
mask = create_bitmask(255, bits=8)
mask = from_bits([0, 2, 4], total_bits=8)
mask = from_binary("10101010")
mask = from_hex("ff")

# Combine bitmasks
combined = combine_bitmasks(mask1, mask2, mask3)
intersected = intersect_bitmasks(mask1, mask2, mask3)
```

### Utility Functions

```python
from bitmask_utils.mod import (
    count_bits, parity, reverse_bits,
    next_power_of_2, is_power_of_2,
    get_lsb, get_msb,
    gray_code, from_gray_code
)

# Count set bits
count_bits(255)  # 8

# Parity (XOR of all bits)
parity(7)  # 1

# Reverse bits
reverse_bits(0b11010010, 8)  # 0b01001011

# Power of 2 operations
is_power_of_2(16)     # True
is_power_of_2(15)     # False
next_power_of_2(10)   # 16

# Find bit positions
get_lsb(0b10100)  # 2 (least significant bit)
get_msb(0b10100, 8)  # 4 (most significant bit)

# Gray code conversion
gray = gray_code(5)        # 7
back = from_gray_code(gray)  # 5
```

## Use Cases

### Permission System

```python
# Define permissions
READ = 0
WRITE = 1
EXECUTE = 2
ADMIN = 3

# Create user permissions
user_perms = Bitmask(bits=4)
user_perms.set_all([READ, WRITE])

# Check permissions
if user_perms.has(READ):
    print("User can read")

# Grant admin access
user_perms.set(ADMIN)

# Check if user has all permissions
if user_perms.has_all([READ, WRITE, EXECUTE, ADMIN]):
    print("User is super admin!")
```

### State Machine Flags

```python
# Define states
IDLE = 0
RUNNING = 1
PAUSED = 2
ERROR = 3

state = Bitmask(bits=4)
state.set(IDLE)

# Transition to running
state.clear(IDLE).set(RUNNING)

# Check current state
if state.has(RUNNING) and not state.has_any([PAUSED, ERROR]):
    print("System is running normally")
```

### Day of Week Selection

```python
# Days: 0=Mon, 1=Tue, 2=Wed, 3=Thu, 4=Fri, 5=Sat, 6=Sun
weekdays = from_bits([0, 1, 2, 3, 4], total_bits=7)
weekends = from_bits([5, 6], total_bits=7)

# Check if a day is a weekday
if weekdays.has(2):  # Wednesday
    print("It's a weekday!")

# Combine schedules
full_week = combine_bitmasks(weekdays, weekends)
```

## API Reference

### Bitmask Class

| Method | Description |
|--------|-------------|
| `set(bit)` | Set a bit to 1 |
| `clear(bit)` | Clear a bit to 0 |
| `toggle(bit)` | Toggle a bit |
| `has(bit)` | Check if bit is set |
| `get(bit)` | Get bit value (0 or 1) |
| `set_all(bits)` | Set multiple bits |
| `clear_all(bits)` | Clear multiple bits |
| `toggle_all(bits)` | Toggle multiple bits |
| `has_all(bits)` | Check if all bits set |
| `has_any(bits)` | Check if any bit set |
| `has_none(bits)` | Check if no bits set |
| `set_range(start, end)` | Set bit range |
| `clear_range(start, end)` | Clear bit range |
| `count_set()` | Count 1 bits |
| `count_clear()` | Count 0 bits |
| `first_set()` | Find first 1 bit |
| `last_set()` | Find last 1 bit |
| `get_set_bits()` | List of 1 bit positions |
| `get_clear_bits()` | List of 0 bit positions |
| `invert()` | Invert all bits |
| `shift_left(n)` | Shift left |
| `shift_right(n)` | Shift right |
| `rotate_left(n)` | Rotate left |
| `rotate_right(n)` | Rotate right |
| `and_with(other)` | Bitwise AND |
| `or_with(other)` | Bitwise OR |
| `xor_with(other)` | Bitwise XOR |
| `is_subset(other)` | Subset check |
| `is_superset(other)` | Superset check |
| `overlaps(other)` | Overlap check |
| `is_disjoint(other)` | Disjoint check |
| `to_int()` | Integer value |
| `to_bin()` | Binary string |
| `to_hex()` | Hex string |
| `to_list()` | List of bits |
| `to_set()` | Set of positions |
| `copy()` | Create copy |
| `reset()` | Set all to 0 |
| `fill()` | Set all to 1 |

### Utility Functions

| Function | Description |
|----------|-------------|
| `count_bits(n)` | Count set bits |
| `parity(n)` | Calculate parity |
| `reverse_bits(n, bits)` | Reverse bits |
| `next_power_of_2(n)` | Next power of 2 |
| `is_power_of_2(n)` | Check if power of 2 |
| `get_lsb(n)` | Get LSB position |
| `get_msb(n, bits)` | Get MSB position |
| `gray_code(n)` | Binary to Gray code |
| `from_gray_code(g)` | Gray code to binary |

## Running Tests

```bash
cd Python/bitmask_utils
python test.py
```

## License

MIT License