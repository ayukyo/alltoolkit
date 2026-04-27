# Bloom Filter - C++ Implementation

A space-efficient probabilistic data structure for set membership testing.

## Features

- **Zero external dependencies** - Pure C++17 standard library
- **Three filter types**:
  - `BloomFilter` - Standard bloom filter
  - `CountingBloomFilter` - Supports element removal
  - `ScalableBloomFilter` - Automatically grows as needed
- **Automatic parameter optimization** - Calculates optimal size and hash function count
- **Serialization support** - Save and restore filter state
- **High performance** - 100k+ operations per second

## Quick Start

```cpp
#include "bloom_filter.hpp"

using namespace bloom_filter;

// Create a filter for 1000 elements with 1% false positive rate
BloomFilter<std::string> filter(1000, 0.01);

// Insert elements
filter.insert("apple");
filter.insert("banana");

// Check membership
if (filter.might_contain("apple")) {
    // Probably in the set
}

if (!filter.might_contain("orange")) {
    // Definitely NOT in the set
}
```

## API Reference

### BloomFilter<T>

#### Constructors

```cpp
// Automatic parameter calculation
BloomFilter(size_t expected_elements, double false_positive_rate)

// Manual parameters
BloomFilter(size_t num_bits, size_t num_hash_functions)
```

#### Methods

| Method | Description |
|--------|-------------|
| `insert(element)` | Add element to filter |
| `might_contain(element)` | Check if element might be in filter |
| `contains(element)` | Alias for might_contain |
| `clear()` | Remove all elements |
| `size()` | Get number of bits |
| `hash_functions()` | Get number of hash functions |
| `count()` | Get number of inserted elements |
| `bits_set()` | Get number of bits set to 1 |
| `current_false_positive_rate()` | Estimate current FPR |
| `memory_usage()` | Get memory usage in bytes |
| `serialize_to_string()` | Serialize to hex string |
| `deserialize_from_string(str)` | Restore from string (static) |

### CountingBloomFilter<T>

Same API as BloomFilter, plus:

| Method | Description |
|--------|-------------|
| `remove(element)` | Remove element (returns false if not found) |

### ScalableBloomFilter<T>

```cpp
// Constructor
ScalableBloomFilter(double false_positive_rate = 0.01, size_t initial_capacity = 1000)

// Additional methods
num_filters()  // Number of internal filters
```

## False Positive Rate

The bloom filter can produce false positives but **never** false negatives:

- If `might_contain()` returns `false`: Element is **definitely not** in the set
- If `might_contain()` returns `true`: Element is **probably** in the set (small chance of false positive)

Lower false positive rate → Larger memory usage

| Expected Elements | FPR 1% | FPR 0.1% | FPR 0.01% |
|------------------|-------|---------|----------|
| 1,000 | 1.2 KB | 1.8 KB | 2.4 KB |
| 10,000 | 12 KB | 18 KB | 24 KB |
| 100,000 | 120 KB | 180 KB | 240 KB |
| 1,000,000 | 1.2 MB | 1.8 MB | 2.4 MB |

## Use Cases

### Web Crawlers
Track visited URLs without storing all URLs in memory.

### Cache Filtering
Quickly reject requests for items not in cache.

### Username Availability
Check if username might be taken before database lookup.

### Spell Checking
Reject definitely misspelled words quickly.

### Database Query Optimization
Skip database queries for non-existent keys.

## Building

```bash
# Run tests
make test

# Run examples
make examples

# Build all
make all

# Clean
make clean
```

## License

Part of AllToolkit - MIT License