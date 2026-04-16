# Bloom Filter

A space-efficient probabilistic data structure for set membership testing.

## Features

- 🚀 **Zero external dependencies** - Pure Rust implementation
- ⚡ **Configurable precision** - Set your desired false positive rate
- 📈 **Scalable variant** - Grows automatically as needed
- 💾 **Serialization** - Save and load filters from bytes
- 🔀 **Merge support** - Combine multiple filters
- 🔒 **Thread-safe** - Uses only atomic operations internally

## Quick Start

```rust
use bloom_filter::BloomFilter;

// Create a filter for ~1000 items with 1% false positive rate
let mut filter = BloomFilter::<&str>::with_rate(1000, 0.01);

// Insert items
filter.insert(&"hello");
filter.insert(&"world");

// Check membership
assert!(filter.contains(&"hello"));  // true
assert!(filter.contains(&"world"));  // true
assert!(!filter.contains(&"missing")); // false (definitely not present)
```

## API

### BloomFilter

```rust
// Create with optimal settings
let filter = BloomFilter::<T>::with_rate(expected_items, false_positive_rate);

// Create with custom config
let config = BloomConfig { size: 10000, hash_count: 7 };
let filter = BloomFilter::<T>::new(config);

// Basic operations
filter.insert(&item);           // Insert an item
filter.contains(&item);        // Check membership
filter.check_and_insert(&item); // Check and insert atomically
filter.clear();                 // Clear all items
filter.len();                   // Number of items inserted
filter.is_empty();              // Check if empty

// Statistics
filter.current_false_positive_rate(); // Current estimated FPR
filter.fill_ratio();                   // Proportion of bits set
filter.bit_count();                    // Number of bits set

// Serialization
let bytes = filter.to_bytes();
let restored = BloomFilter::<T>::from_bytes(&bytes).unwrap();

// Merge filters (same config required)
filter1.merge(&filter2).unwrap();
```

### ScalableBloomFilter

For unknown or growing datasets:

```rust
use bloom_filter::ScalableBloomFilter;

let mut filter = ScalableBloomFilter::<i32>::new(1000, 0.01);

// Automatically grows as needed
for i in 0..1_000_000 {
    filter.insert(&i);
}

// All items still findable
assert!(filter.contains(&500000));
```

## How It Works

A Bloom filter uses:
1. A bit array of size `m`
2. `k` independent hash functions

For each item:
- Compute `k` hash values
- Set `k` bits in the array

To check membership:
- Compute `k` hash values
- If all `k` bits are set → item might be present
- If any bit is unset → item definitely not present

### False Positives

Bloom filters can produce false positives but never false negatives:
- **Contains returns true** → Item might be present (could be false positive)
- **Contains returns false** → Item definitely not present

The false positive rate depends on:
- Number of bits per item (`m/n` ratio)
- Number of hash functions (`k`)

### Optimal Parameters

```
m = -n * ln(p) / ln(2)²
k = m/n * ln(2)
```

Where:
- `n` = expected number of items
- `p` = desired false positive rate
- `m` = number of bits
- `k` = number of hash functions

## Performance

| Operation | Time Complexity | Space Complexity |
|-----------|-----------------|------------------|
| Insert    | O(k)            | O(m) bits        |
| Contains  | O(k)            | -                |
| Clear     | O(m/word_size)  | -                |

## Example: Duplicate Detection

```rust
use bloom_filter::BloomFilter;

fn find_duplicates(urls: &[String]) -> Vec<&String> {
    let mut seen = BloomFilter::<String>::with_rate(urls.len(), 0.001);
    let mut duplicates = Vec::new();
    
    for url in urls {
        if seen.contains(url) {
            duplicates.push(url);
        } else {
            seen.insert(url);
        }
    }
    
    duplicates
}
```

## Example: Cache Filter

```rust
use bloom_filter::BloomFilter;

struct CacheFilter {
    filter: BloomFilter<String>,
}

impl CacheFilter {
    fn new(capacity: usize) -> Self {
        Self {
            filter: BloomFilter::with_rate(capacity, 0.01),
        }
    }
    
    fn might_have(&self, key: &str) -> bool {
        self.filter.contains(&key.to_string())
    }
    
    fn mark_cached(&mut self, key: &str) {
        self.filter.insert(&key.to_string());
    }
}
```

## License

MIT