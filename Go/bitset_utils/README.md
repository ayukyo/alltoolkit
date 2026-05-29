# BitSet Utils

A comprehensive BitSet utility library for Go with zero external dependencies.

## Features

- **Dynamic Bit Sets**: Automatically growable bit sets
- **Bit Manipulation**: Set, Clear, Toggle, Get operations
- **Set Operations**: AND, OR, XOR, AND NOT, NOT
- **Search Operations**: Find first/last/next set/clear bits
- **Range Operations**: Set/clear ranges of bits efficiently
- **Shift Operations**: Left and right shift with proper handling
- **Conversion**: To/from bytes, strings, uint64 slices
- **Set Properties**: Subset, Intersects, Equals
- **Bulk Operations**: SetAll, ClearAll, FlipAll
- **Iteration**: Range-based iteration with early termination

## Installation

```go
import "bitset_utils"
```

## Quick Start

```go
package main

import (
    "fmt"
    "bitset_utils"
)

func main() {
    // Create a new BitSet
    bs := bitset_utils.NewBitSet(64)
    
    // Set some bits
    bs.Set(0)
    bs.Set(5)
    bs.Set(10)
    
    // Check if a bit is set
    if bs.Test(5) {
        fmt.Println("Bit 5 is set")
    }
    
    // Count set bits
    fmt.Printf("Set bits: %d\n", bs.Count())
    
    // String representation
    fmt.Printf("BitSet: %s\n", bs.String())
}
```

## API Reference

### Creation

```go
// Create a new BitSet with initial capacity
bs := bitset_utils.NewBitSet(100)

// Create from binary string
bs, err := bitset_utils.NewBitSetFromString("10110")

// Create from bytes
bs := bitset_utils.NewBitSetFromBytes([]byte{0xFF, 0x0F})

// Create from uint64 slice
bs := bitset_utils.NewBitSetFrom([]uint64{0xFF00FF00}, 32)
```

### Basic Operations

```go
// Set a bit
bs.Set(10)

// Clear a bit
bs.Clear(10)

// Toggle a bit
bs.Toggle(10)

// Get bit value
value, err := bs.Get(10)

// Test if bit is set
if bs.Test(10) {
    // bit is set
}
```

### Set Operations

```go
bs1, _ := bitset_utils.NewBitSetFromString("1100")
bs2, _ := bitset_utils.NewBitSetFromString("1010")

// AND operation
and := bs1.And(bs2)  // Result: "1000"

// OR operation
or := bs1.Or(bs2)    // Result: "1110"

// XOR operation
xor := bs1.Xor(bs2)   // Result: "0110"

// Difference (AND NOT)
diff := bs1.AndNot(bs2)  // Result: "0100"

// Complement
not := bs1.Not()      // Result: "0011"
```

### Search Operations

```go
bs := bitset_utils.NewBitSet(100)
bs.Set(10)
bs.Set(50)
bs.Set(90)

// Find first set bit
first := bs.FirstSet()  // Returns 10

// Find last set bit
last := bs.LastSet()    // Returns 90

// Find next set bit from position
next := bs.NextSet(11)  // Returns 50

// Find next clear bit from position
clear := bs.NextClear(0)  // Returns 0

// Get all set bit positions
positions := bs.SetBits()  // Returns [10, 50, 90]
```

### Range Operations

```go
bs := bitset_utils.NewBitSet(100)

// Set a range of bits
bs.SetRange(10, 20)  // Set bits 10-19

// Clear a range of bits
bs.ClearRange(15, 18)  // Clear bits 15-17

// Check if all bits in range are set
if bs.All(10, 15) {
    // All bits in [10, 15) are set
}
```

### Shift Operations

```go
bs, _ := bitset_utils.NewBitSetFromString("1011")

// Shift left
bs.ShiftLeft(2)  // Result: "101100"

// Shift right
bs.ShiftRight(1)  // Result: "10110"
```

### Conversion

```go
bs, _ := bitset_utils.NewBitSetFromString("10110")

// To string
s := bs.String()  // "10110"

// To bytes
bytes := bs.ToBytes()

// To uint64 slice
words := bs.ToUint64Slice()

// To set representation
setStr := bs.StringSet()  // "{1, 2, 4}"
```

### Set Properties

```go
bs1, _ := bitset_utils.NewBitSetFromString("1100")
bs2, _ := bitset_utils.NewBitSetFromString("1110")
bs3, _ := bitset_utils.NewBitSetFromString("0011")

// Subset check
if bs1.Subset(bs2) {
    // All bits in bs1 are also set in bs2
}

// Intersection check
if bs1.Intersects(bs2) {
    // bs1 and bs2 have at least one common set bit
}

// Equality check
if bs1.Equals(bs2) {
    // bs1 and bs2 are identical
}
```

### Bulk Operations

```go
bs := bitset_utils.NewBitSet(64)

// Set all bits
bs.SetAll()

// Clear all bits
bs.ClearAll()

// Flip all bits
bs.FlipAll()

// Check if empty
if bs.IsEmpty() {
    // No bits set
}

// Check if full
if bs.IsFull() {
    // All bits set
}

// Check if any bit set
if bs.Any() {
    // At least one bit set
}

// Check if no bits set
if bs.None() {
    // Same as IsEmpty()
}
```

### Iteration

```go
bs := bitset_utils.NewBitSet(100)
bs.Set(10)
bs.Set(20)
bs.Set(30)

// Iterate over all set bits
bs.Range(func(pos int) bool {
    fmt.Printf("Bit %d is set\n", pos)
    return true  // Continue iteration
})

// Early termination
bs.Range(func(pos int) bool {
    fmt.Printf("Bit %d is set\n", pos)
    return false  // Stop after first
})
```

### Other Operations

```go
// Clone a BitSet
clone := bs.Clone()

// Reverse bit order
bs.Reverse()

// Truncate to n bits
bs.Truncate(10)

// Copy from another BitSet
bs1.Copy(bs2, 5)  // Copy bs2 into bs1 starting at position 5
```

## Performance

The BitSet uses uint64 words internally for efficient operations:
- Single bit operations: O(1)
- Set/Clear range operations: O(n/64) where n is range size
- Count (population count): O(w) where w is number of words
- Set operations (AND, OR, XOR): O(w) where w is number of words

## Benchmarks

Run benchmarks with:
```bash
go test -bench=. -benchmem
```

## License

MIT License