# Bloom Filter - Zig Implementation

A space-efficient probabilistic data structure for membership testing.

## Overview

A Bloom filter is a space-efficient probabilistic data structure used to test whether an element is a member of a set. False positive matches are possible, but false negatives are not. In other words, a query returns either "possibly in set" or "definitely not in set".

## Features

- **Space-efficient**: Uses significantly less memory than a full hash set
- **Configurable false positive rate**: Adjust accuracy based on your needs
- **Multiple hash functions**: Uses double hashing for better distribution
- **Operations**: Add, check, clear, union, intersection
- **Serialization**: Save and restore filter state
- **Counting Bloom Filter**: Supports item removal
- **Scalable Bloom Filter**: Auto-expands to maintain accuracy

## Usage

### Basic Bloom Filter

```zig
const std = @import("std");
const bloom_filter = @import("bloom_filter");

pub fn main() !void {
    const allocator = std.heap.page_allocator;
    
    // Create a Bloom filter for ~1000 items with 1% false positive rate
    var bf = try bloom_filter.BloomFilter.init(allocator, .{
        .expected_items = 1000,
        .false_positive_rate = 0.01,
    });
    defer bf.deinit();
    
    // Add items
    bf.add("apple");
    bf.add("banana");
    bf.add("cherry");
    
    // Check membership
    if (bf.mightContain("apple")) {
        // Possibly in set
    }
    
    if (!bf.mightContain("orange")) {
        // Definitely NOT in set
    }
}
```

### Counting Bloom Filter (supports removal)

```zig
var cbf = try bloom_filter.CountingBloomFilter.init(allocator, .{
    .expected_items = 100,
    .false_positive_rate = 0.01,
});
defer cbf.deinit();

cbf.add("apple");
cbf.add("banana");

// Remove an item
if (cbf.remove("apple")) {
    // Successfully removed
}
```

### Scalable Bloom Filter (auto-expands)

```zig
var sbf = try bloom_filter.ScalableBloomFilter.init(allocator, 0.01);
defer sbf.deinit();

// Add any number of items - filter will grow as needed
for (0..10000) |i| {
    var buf: [20]u8 = undefined;
    const str = std.fmt.bufPrint(&buf, "item_{}", .{i}) catch unreachable;
    sbf.add(str);
}
```

### Serialization

```zig
// Serialize
const data = try bf.serialize(allocator);
defer allocator.free(data);

// Deserialize
var bf2 = try bloom_filter.BloomFilter.deserialize(allocator, data);
defer bf2.deinit();
```

## API Reference

### BloomFilter

| Method | Description |
|--------|-------------|
| `init(allocator, options)` | Create filter with optimal parameters |
| `initWithParams(allocator, num_bits, num_hashes)` | Create filter with explicit parameters |
| `deinit()` | Free memory |
| `add(item)` | Add item to filter |
| `addU64(value)` | Add u64 integer to filter |
| `mightContain(item)` | Check if item might be in filter |
| `mightContainU64(value)` | Check if u64 might be in filter |
| `clear()` | Remove all items |
| `isEmpty()` | Check if filter is empty |
| `itemCount()` | Get number of items inserted |
| `bitCount()` | Get number of bits used |
| `hashFunctionCount()` | Get number of hash functions |
| `estimateFalsePositiveRate()` | Estimate current false positive probability |
| `unionWith(other)` | Union with another filter |
| `intersectWith(other)` | Intersection with another filter |
| `serialize(allocator)` | Serialize to bytes |
| `deserialize(allocator, data)` | Deserialize from bytes |

### CountingBloomFilter

| Method | Description |
|--------|-------------|
| `init(allocator, options)` | Create counting filter |
| `deinit()` | Free memory |
| `add(item)` | Add item |
| `remove(item)` | Remove item (returns true if successful) |
| `mightContain(item)` | Check membership |

### ScalableBloomFilter

| Method | Description |
|--------|-------------|
| `init(allocator, initial_fp_rate)` | Create scalable filter |
| `deinit()` | Free memory |
| `add(item)` | Add item (auto-expands if needed) |
| `mightContain(item)` | Check membership |
| `itemCount()` | Get total item count estimate |
| `clear()` | Clear all filters |

## Mathematical Details

The optimal number of bits (m) and hash functions (k) are calculated as:

- `m = -n × ln(p) / (ln(2))²` where n is expected items, p is false positive rate
- `k = m × ln(2) / n`

## Building

```bash
zig build
```

## Testing

```bash
zig build test
```

## Running Example

```bash
zig build run
```

## License

MIT License - Part of AllToolkit