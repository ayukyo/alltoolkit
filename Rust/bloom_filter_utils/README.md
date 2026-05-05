# Bloom Filter Utils (Rust)

A space-efficient probabilistic data structure for membership testing.

## Features

- **Classic Bloom Filter**: Space-efficient membership testing with configurable false positive rate
- **Counting Bloom Filter**: Supports removal operations
- **Zero external dependencies**: Uses only Rust standard library
- **Generic support**: Works with any hashable type
- **Serialization**: Export/import filter state as bytes
- **Merge support**: Combine two filters (union operation)

## Usage

```rust
use bloom_filter_utils::{BloomFilter, BloomFilterConfig, CountingBloomFilter};

// Create a bloom filter for 1000 items with 1% false positive rate
let config = BloomFilterConfig {
    expected_items: 1000,
    false_positive_rate: 0.01,
};
let mut filter = BloomFilter::new(config);

// Add items
filter.add(&"hello");
filter.add(&"world");
filter.add(&42i32);

// Check membership
assert!(filter.contains(&"hello"));    // true
assert!(filter.contains(&42i32));      // true
assert!(!filter.contains(&"missing")); // false

// Get stats
println!("Items: {}", filter.len());
println!("Fill ratio: {:.2}%", filter.fill_ratio() * 100.0);
```

### Counting Bloom Filter (with removal)

```rust
let mut filter = CountingBloomFilter::new(BloomFilterConfig::default());

filter.add(&"item");
assert!(filter.contains(&"item"));

filter.remove(&"item");
assert!(!filter.contains(&"item")); // Now returns false
```

### Merge Filters

```rust
let mut filter1 = BloomFilter::with_size(1024, 3);
let mut filter2 = BloomFilter::with_size(1024, 3);

filter1.add(&"a");
filter2.add(&"b");

filter1.merge(&filter2).unwrap();
// filter1 now contains both "a" and "b"
```

## API Reference

### BloomFilter

| Method | Description |
|--------|-------------|
| `new(config)` | Create filter with config |
| `with_size(bits, hashes)` | Create filter with custom size |
| `add(item)` | Add item to filter |
| `contains(item)` | Check if item might be in filter |
| `clear()` | Remove all items |
| `merge(other)` | Merge another filter (union) |
| `to_bytes()` | Export filter state |
| `from_bytes(...)` | Import filter state |
| `len()` | Number of items added |
| `fill_ratio()` | Fraction of bits set |
| `current_false_positive_rate()` | Current estimated FPR |

### CountingBloomFilter

| Method | Description |
|--------|-------------|
| `new(config)` | Create counting filter |
| `add(item)` | Add item |
| `remove(item)` | Remove item (if present) |
| `contains(item)` | Check membership |

## How It Works

A Bloom filter uses multiple hash functions to set bits in a bit array. When checking membership:
- If all corresponding bits are set → item might be present (may be false positive)
- If any bit is unset → item is definitely not present (never false negative)

The false positive rate depends on:
- Number of bits (m)
- Number of hash functions (k)
- Number of items added (n)

Optimal values are calculated automatically from your configuration.

## Running Tests

```bash
rustc --edition 2021 --test mod.rs -o bloom_test && ./bloom_test
```

## Running Example

```bash
rustc --edition 2021 mod.rs --crate-type lib -o libbloom_filter_utils.rlib
rustc --edition 2021 main.rs --extern bloom_filter_utils=libbloom_filter_utils.rlib -o example
./example
```

## Created

2026-05-06 by AllToolkit automation