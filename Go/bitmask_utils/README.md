# BitMask Utils

A comprehensive bitmask utility library for Go with zero external dependencies.

## Features

- **Full-featured bit manipulation**: Set, Clear, Toggle, Get operations
- **Bitwise operations**: AND, OR, XOR, NOT
- **Shift operations**: Left shift, Right shift
- **Rotation**: Rotate left, Rotate right
- **Reverse**: Reverse all bits
- **Search operations**: Find first/last set/clear bit
- **Range operations**: Set, clear, or get bits in a range
- **Bulk operations**: Set/Clear multiple bits at once
- **Set operations**: Intersects, SubsetOf
- **Large bitmasks**: Supports bitmasks larger than 64 bits
- **Conversion**: To/From uint64, bytes, binary string

## Installation

```bash
go get github.com/ayukyo/alltoolkit/go/bitmask_utils
```

## Quick Start

```go
package main

import (
    "fmt"
    "bitmask_utils"
)

func main() {
    // Create a new bitmask with 16 bits
    bm := bitmask_utils.NewBitMask(16)
    
    // Set some bits
    bm.Set(5)
    bm.Set(10)
    bm.Set(15)
    
    // Check bits
    fmt.Println(bm.IsSet(5))  // true
    fmt.Println(bm.IsSet(6))  // false
    
    // Count set bits
    fmt.Println(bm.CountOnes())  // 3
    
    // Convert to binary string
    fmt.Println(bm.ToBinaryString())  // 1000010000010000
}
```

## API Reference

### Creation

```go
// Create a new bitmask with specified size
bm := bitmask_utils.NewBitMask(64)

// Create from uint64
bm := bitmask_utils.NewBitMaskFromUint64(0xFF)

// Create from byte slice
bm := bitmask_utils.NewBitMaskFromBytes([]byte{0x12, 0x34})
```

### Basic Operations

```go
// Set a bit
bm.Set(5)

// Clear a bit
bm.Clear(5)

// Toggle a bit
bm.Toggle(5)

// Get bit value
value, err := bm.Get(5)

// Check if bit is set
if bm.IsSet(5) { ... }

// Check if bit is clear
if bm.IsClear(5) { ... }
```

### Bulk Operations

```go
// Set all bits
bm.SetAll()

// Clear all bits
bm.ClearAll()

// Set multiple bits
bm.SetBits([]int{1, 3, 5})

// Clear multiple bits
bm.ClearBits([]int{1, 3, 5})
```

### Range Operations

```go
// Set bits in range [start, end)
bm.SetRange(5, 10)

// Clear bits in range
bm.ClearRange(5, 10)

// Get bits in range as new bitmask
sub, err := bm.GetRange(5, 10)
```

### Bitwise Operations

```go
bm1.And(bm2)   // Bitwise AND
bm1.Or(bm2)    // Bitwise OR
bm1.Xor(bm2)   // Bitwise XOR
bm.Not()       // Bitwise NOT
```

### Shift and Rotate

```go
bm.LeftShift(3)   // Shift left by 3
bm.RightShift(3)  // Shift right by 3
bm.RotateLeft(3)  // Rotate left by 3
bm.RotateRight(3) // Rotate right by 3
bm.Reverse()      // Reverse all bits
```

### Search Operations

```go
// Find first set bit
pos := bm.FindFirstSet()  // Returns -1 if none

// Find last set bit
pos := bm.FindLastSet()

// Find first clear bit
pos := bm.FindFirstClear()

// Get all set bit positions
positions := bm.GetSetBits()

// Get all clear bit positions
positions := bm.GetClearBits()
```

### Set Operations

```go
// Check if bitmasks intersect
if bm1.Intersects(bm2) { ... }

// Check if bm1 is subset of bm2
if bm1.SubsetOf(bm2) { ... }

// Check equality
if bm1.Equals(bm2) { ... }

// Check if empty (all zeros)
if bm1.IsEmpty() { ... }

// Check if full (all ones)
if bm1.IsFull() { ... }
```

### Conversion

```go
// To uint64 (first 64 bits)
val := bm.ToUint64()

// To byte slice
bytes := bm.ToBytes()

// To binary string
str := bm.ToBinaryString()

// String representation
str := bm.String()
```

### Utility

```go
// Get size
size := bm.Size()

// Count ones/zeros
ones := bm.CountOnes()
zeros := bm.CountZeros()

// Clone
copy := bm.Clone()

// Swap two bits
bm.Swap(5, 10)

// Copy from another bitmask
bm1.CopyFrom(bm2)

// Fill with pattern
bm.Fill(0xFF)
```

## Practical Examples

### Permission Flags

```go
type Permission int
const (
    Read Permission = iota
    Write
    Execute
    Delete
)

permissions := bitmask_utils.NewBitMask(4)
permissions.Set(int(Read))
permissions.Set(int(Write))

if permissions.IsSet(int(Read)) {
    fmt.Println("User can read")
}
```

### Feature Flags

```go
type Feature int
const (
    DarkMode Feature = iota
    Notifications
    Analytics
)

features := bitmask_utils.NewBitMask(3)
features.Set(int(DarkMode))
features.Set(int(Analytics))

// Enable notifications
features.Set(int(Notifications))

// Disable analytics
features.Clear(int(Analytics))
```

### Network Port Management

```go
ports := bitmask_utils.NewBitMask(65536)

// Mark ports as in use
ports.Set(80)
ports.Set(443)
ports.Set(8080)

// Find next available port
func findFreePort(ports *bitmask_utils.BitMask, start int) int {
    for i := start; i < ports.Size(); i++ {
        if ports.IsClear(i) {
            return i
        }
    }
    return -1
}

freePort := findFreePort(ports, 1024)
```

## Performance

Optimized for speed and memory efficiency:
- Uses `uint64` blocks for efficient storage
- Population count using Brian Kernighan's algorithm
- Block-based operations minimize iterations

## License

MIT License