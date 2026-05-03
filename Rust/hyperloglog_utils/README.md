# HyperLogLog Utils

A memory-efficient cardinality estimation data structure implementation in Rust with zero external dependencies.

## Overview

HyperLogLog is a probabilistic algorithm for estimating the cardinality (number of distinct elements) of a multiset. It uses significantly less memory than exact methods while providing a controllable error rate.

### Error Rate

The standard error is approximately `1.04 / sqrt(m)` where `m` is the number of registers:
- precision 4: 16 registers, ~26% error
- precision 12: 4096 registers, ~1.6% error  
- precision 16: 65536 registers, ~0.4% error

## Features

- **Zero dependencies** - Uses only Rust standard library
- **Configurable precision** (4-16 bits for register indexing)
- **Standard FNV-1a hash** - No external hasher required
- **Merge support** - Combine multiple HyperLogLog instances
- **Serialization** - Convert to/from bytes
- **Sparse variant** - Memory-efficient for small cardinalities

## Installation

Add to your `Cargo.toml`:

```toml
[dependencies]
hyperloglog_utils = { path = "." }
```

## Usage

### Basic Usage

```rust
use hyperloglog_utils::HyperLogLog;

fn main() {
    // Create with precision 12 (4096 registers, ~1.6% error)
    let mut hll = HyperLogLog::new(12).unwrap();
    
    // Insert elements
    hll.insert(b"hello");
    hll.insert(b"world");
    hll.insert(b"hello"); // duplicate - won't significantly affect count
    
    // Get estimated cardinality
    println!("Unique elements: {}", hll.count());
}
```

### Create with Target Error Rate

```rust
use hyperloglog_utils::HyperLogLog;

fn main() {
    // Create a HyperLogLog with ~1% error rate
    let hll = HyperLogLog::with_error_rate(0.01).unwrap();
    println!("Precision: {}", hll.precision()); // Will be ~12-14
}
```

### Merge Multiple HyperLogLogs

```rust
use hyperloglog_utils::HyperLogLog;

fn main() {
    let mut hll1 = HyperLogLog::new(12).unwrap();
    let mut hll2 = HyperLogLog::new(12).unwrap();
    
    // Add different elements to each
    for i in 0..500 {
        hll1.insert(&i.to_be_bytes());
    }
    for i in 500..1000 {
        hll2.insert(&i.to_be_bytes());
    }
    
    // Merge hll2 into hll1
    hll1.merge(&hll2).unwrap();
    
    println!("Total unique: {}", hll1.count()); // ~1000
}
```

### Serialization

```rust
use hyperloglog_utils::HyperLogLog;

fn main() {
    let mut hll = HyperLogLog::new(12).unwrap();
    for i in 0..1000 {
        hll.insert(&i.to_be_bytes());
    }
    
    // Serialize to bytes
    let bytes = hll.to_bytes();
    
    // Deserialize from bytes
    let hll2 = HyperLogLog::from_bytes(&bytes).unwrap();
    
    assert_eq!(hll.count(), hll2.count());
}
```

### Sparse HyperLogLog (Memory Efficient)

```rust
use hyperloglog_utils::SparseHyperLogLog;

fn main() {
    let mut hll = SparseHyperLogLog::new(12).unwrap();
    
    // Uses hash map for small cardinalities
    for i in 0..100 {
        hll.insert(&i.to_be_bytes());
    }
    
    println!("Count: {}", hll.count());
}
```

## API Reference

### HyperLogLog

| Method | Description |
|--------|-------------|
| `new(precision)` | Create with specified precision (4-16) |
| `with_error_rate(rate)` | Create with target error rate |
| `insert(data)` | Insert a byte slice |
| `insert_hashable(value)` | Insert any hashable value |
| `count()` | Estimate cardinality |
| `merge(other)` | Merge another HyperLogLog |
| `is_empty()` | Check if empty |
| `clear()` | Clear all registers |
| `to_bytes()` | Serialize to bytes |
| `from_bytes(bytes)` | Deserialize from bytes |
| `register_count()` | Get number of registers |
| `precision()` | Get precision value |

### SparseHyperLogLog

| Method | Description |
|--------|-------------|
| `new(precision)` | Create sparse variant |
| `insert(data)` | Insert a byte slice |
| `count()` | Estimate cardinality |
| `merge(other)` | Merge another sparse HyperLogLog |

## Performance

Memory usage: `m = 2^precision` bytes for register storage.

| Precision | Registers | Memory | Error |
|-----------|-----------|--------|-------|
| 4 | 16 | 16 bytes | ~26% |
| 8 | 256 | 256 bytes | ~6.5% |
| 12 | 4,096 | 4 KB | ~1.6% |
| 14 | 16,384 | 16 KB | ~0.8% |
| 16 | 65,536 | 64 KB | ~0.4% |

## Algorithm

HyperLogLog works by:
1. Hashing each element to a 64-bit value
2. Using the first `precision` bits to select a register
3. Counting leading zeros in the remaining bits
4. Storing the maximum leading zeros seen for each register
5. Estimating cardinality using the harmonic mean of `2^(-register_value)`

## License

MIT License