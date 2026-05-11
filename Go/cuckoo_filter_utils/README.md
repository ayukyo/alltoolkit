# Cuckoo Filter Utils

A complete implementation of the Cuckoo Filter probabilistic data structure for Go.

## Overview

Cuckoo filters are an improvement over Bloom filters for set membership testing. They provide:
- **Deletion support** - Unlike Bloom filters, items can be removed
- **Lower false positive rate** - For the same memory usage (at low load)
- **O(1) operations** - Constant time for add, remove, and contains

## Features

### Core Operations
- `Add(data []byte)` - Add an item to the filter
- `Contains(data []byte)` - Check if an item might be in the filter
- `Remove(data []byte)` - Remove an item from the filter

### Advanced Operations
- `Clone()` - Create a copy of the filter
- `Reset()` - Clear all items
- `Merge(other)` - Combine two filters
- `ForEach(fn)` - Iterate over stored fingerprints
- `BucketIndex(data)` - Debug bucket positions

### Configuration Options
- `Capacity` - Expected number of items
- `FalsePositiveRate` - Target probability (0.001 - 0.5)
- `BucketSize` - Fingerprints per bucket (2-8)
- `MaxKicks` - Maximum relocation attempts

### Statistics & Analysis
- `Count()` - Number of items stored
- `Capacity()` - Maximum items
- `LoadFactor()` - Current fill ratio
- `FalsePositiveRate()` - Expected FP rate
- `Size()` - Memory usage in bytes
- `GetStats()` - Complete statistics

## Usage

### Basic Example

```go
package main

import (
    "fmt"
    cuckoo "github.com/ayukyo/alltoolkit/Go/cuckoo_filter_utils"
)

func main() {
    // Create a filter with default options
    cf, err := cuckoo.New(cuckoo.DefaultOptions(1000))
    if err != nil {
        panic(err)
    }

    // Add items
    cf.Add([]byte("apple"))
    cf.Add([]byte("banana"))
    cf.Add([]byte("cherry"))

    // Check membership
    fmt.Println("Contains apple:", cf.Contains([]byte("apple")))   // true
    fmt.Println("Contains grape:", cf.Contains([]byte("grape")))   // false (probably)

    // Remove items
    cf.Remove([]byte("banana"))
    fmt.Println("After removal:", cf.Contains([]byte("banana")))    // false
}
```

### Custom Configuration

```go
opts := cuckoo.Options{
    Capacity:          10000,
    FalsePositiveRate: 0.01,  // Target 1% FP rate
    BucketSize:        4,
    MaxKicks:          500,
}

cf, err := cuckoo.New(opts)
```

### Getting Statistics

```go
stats := cf.GetStats()
fmt.Printf("Items: %d / %d\n", stats.Count, stats.Capacity)
fmt.Printf("Load Factor: %.2f\n", stats.LoadFactor)
fmt.Printf("Memory: %d bytes\n", stats.MemoryBytes)
```

## Important Notes

### False Positive Rate Behavior

The actual false positive rate depends on:
- **Fingerprint size**: Larger fingerprints (more bits) = lower FP rate
- **Load factor**: Higher load = more fingerprint collisions = higher FP rate
- **Number of items**: More items = more potential collisions

At low load factors (<5%), the actual FP rate is close to theoretical `2b/2^f`.
At higher loads, the FP rate increases due to fingerprint collisions.

**Recommendation**: Use this filter with relatively low load (<10%) for best FP performance.

### No False Negatives

Cuckoo filters guarantee **zero false negatives**. If an item was added, `Contains` will always return `true`.

## Algorithm Details

### How It Works

1. **Fingerprint**: A small hash (8 bits max) of the item
2. **Two Hash Functions**: Compute two bucket indices using partial-key cuckoo hashing
3. **Insertion**: Try both buckets; if full, relocate existing items ("kick")
4. **Lookup**: Check both buckets for the fingerprint
5. **Deletion**: Find and remove the fingerprint from either bucket

### Space Complexity

- Memory = numBuckets × bucketSize bytes
- For n items with target FP rate ε:
  - Fingerprint bits: f ≈ log₂(1/ε) + log₂(b) (capped at 8)

### Time Complexity

- **Add**: O(1) expected, O(k) worst case (k = MaxKicks)
- **Contains**: O(1)
- **Remove**: O(1)

## Comparison with Bloom Filter

| Feature | Bloom Filter | Cuckoo Filter |
|---------|-------------|---------------|
| Deletion | No | Yes |
| False Positive | Yes | Yes (load-dependent) |
| False Negative | No | No |
| Count support | No | Yes |
| Memory efficiency | Good | Good at low load |

## Benchmarks

Run benchmarks:
```bash
go test -bench=. -benchmem
```

Typical results (Intel Xeon):
- Add: ~8.8 μs/op, 0 allocs
- Contains: ~138 ns/op, 1 alloc
- Remove: ~280 ns/op, 3 allocs
- Mixed operations: ~2 μs/op, 0 allocs

## Test Coverage

38 unit tests covering:
- Basic operations (add/contains/remove)
- False positive rate measurement
- Capacity and load factor
- Clone, merge, reset
- Edge cases (empty data, duplicates)
- Large-scale stress testing
- Benchmark performance tests

## References

- Fan et al., "Cuckoo Filter: Practically Better Than Bloom", CONCURRENCY 2014
- https://www.cs.cmu.edu/~dga/papers/cuckoo-conext2014.pdf