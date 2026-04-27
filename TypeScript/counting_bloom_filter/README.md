# Counting Bloom Filter

A **Counting Bloom Filter** is a probabilistic data structure that extends the standard Bloom Filter to support **deletion** of elements. This makes it suitable for applications where elements need to be dynamically added and removed.

## Features

- ✅ **Add elements** - Add items to the filter
- ✅ **Check membership** - Test if an item might be in the set
- ✅ **Remove elements** - Delete items (unlike standard Bloom Filter!)
- ✅ **Count occurrences** - Get approximate count of an item
- ✅ **Merge filters** - Combine two filters
- ✅ **Similarity estimation** - Estimate Jaccard similarity between filters
- ✅ **Serialization** - Save and restore filter state
- ✅ **Zero dependencies** - Pure TypeScript implementation

## Installation

Simply copy the `counting_bloom_filter.ts` file to your project.

## Quick Start

```typescript
import { CountingBloomFilter, createCountingBloomFilter } from './counting_bloom_filter';

// Create a filter for ~1000 items with 1% false positive rate
const filter = createCountingBloomFilter(1000, 0.01);

// Add items
filter.add('apple');
filter.add('banana');
filter.add('cherry');

// Check membership
console.log(filter.contains('apple'));  // true
console.log(filter.contains('grape'));  // false (probably)

// Remove items
filter.remove('banana');
console.log(filter.contains('banana')); // false
```

## API Reference

### Constructor

```typescript
const filter = new CountingBloomFilter({
  expectedItems: 1000,      // Expected number of items
  falsePositiveRate: 0.01,  // Desired false positive rate (default: 0.01)
  hashCount: 7,             // Number of hash functions (auto-calculated if omitted)
  size: 9586,               // Filter size in bits (auto-calculated if omitted)
  maxCounterValue: 255      // Maximum counter value (default: 255)
});
```

### Factory Function

```typescript
const filter = createCountingBloomFilter(1000, 0.01);
```

### Methods

#### `add(item: string): boolean`
Adds an item to the filter. Returns `false` if any counter would overflow.

```typescript
filter.add('hello');  // true
```

#### `contains(item: string): boolean`
Checks if an item might be in the filter. Returns `true` if the item might be present (may have false positives), `false` if definitely not present (no false negatives).

```typescript
if (filter.contains('hello')) {
  console.log('Might be in the filter');
}
```

#### `remove(item: string): boolean`
Removes an item from the filter. Returns `true` if the item was removed, `false` if not present.

```typescript
filter.remove('hello');  // true if was present
```

#### `removeAll(item: string): number`
Removes all occurrences of an item. Returns the count removed.

```typescript
filter.add('test');
filter.add('test');
filter.add('test');
const removed = filter.removeAll('test');  // 3
```

#### `approximateCount(item: string): number`
Gets the approximate count of an item in the filter.

```typescript
filter.add('item');
filter.add('item');
console.log(filter.approximateCount('item'));  // ≈ 2
```

#### `clear(): void`
Removes all items from the filter.

```typescript
filter.clear();
```

#### `getStats(): CountingBloomFilterStats`
Returns statistics about the filter.

```typescript
const stats = filter.getStats();
console.log(stats.itemCount);        // Number of items
console.log(stats.loadFactor);       // Fraction of non-zero counters
console.log(stats.estimatedFPR);    // Estimated false positive rate
```

#### `toJSON(): object`
Serializes the filter to a JSON-compatible object.

```typescript
const data = filter.toJSON();
const restored = CountingBloomFilter.fromJSON(data);
```

#### `merge(other: CountingBloomFilter): CountingBloomFilter`
Merges two filters (must have same size and hash count).

```typescript
const merged = filter1.merge(filter2);
```

#### `estimateJaccardSimilarity(other: CountingBloomFilter): number`
Estimates the Jaccard similarity coefficient between two filters.

```typescript
const similarity = filter1.estimateJaccardSimilarity(filter2);
// 0 = no overlap, 1 = identical sets
```

## How It Works

### Standard Bloom Filter vs Counting Bloom Filter

| Feature | Bloom Filter | Counting Bloom Filter |
|---------|--------------|----------------------|
| Add | ✅ | ✅ |
| Check | ✅ | ✅ |
| Remove | ❌ | ✅ |
| Memory | Less | More (counters) |

A Counting Bloom Filter uses an array of counters instead of bits. When adding an element, all corresponding counters are incremented. When removing, they're decremented. This allows deletion but uses more memory.

### Hash Functions

This implementation uses **MurmurHash3** with double hashing to generate `k` hash values from a single seed, providing good distribution and performance.

## Time & Space Complexity

| Operation | Time Complexity |
|-----------|-----------------|
| Add | O(k) |
| Contains | O(k) |
| Remove | O(k) |
| Clear | O(m) |

Where `k` = number of hash functions, `m` = filter size.

## Example Use Cases

### Web Cache Filtering
```typescript
const cacheFilter = createCountingBloomFilter(100000, 0.01);

// Add URLs to cache
cacheFilter.add('https://example.com/page1');
cacheFilter.add('https://example.com/page2');

// Quick check before expensive lookup
if (!cacheFilter.contains(url)) {
  // Definitely not in cache, skip lookup
  return null;
}
// Might be in cache, do actual lookup
```

### Rate Limiting
```typescript
const requestFilter = createCountingBloomFilter(10000);

function checkRateLimit(userId: string): boolean {
  const count = requestFilter.approximateCount(userId);
  if (count >= 100) return false;  // Rate limited
  
  requestFilter.add(userId);
  return true;
}
```

### Distributed Set Membership
```typescript
// Each node maintains its own filter
const localFilter = createCountingBloomFilter(1000);

// Merge filters from other nodes
const mergedFilter = localFilter.merge(remoteFilter);

// Check if item exists anywhere in the cluster
if (mergedFilter.contains('item')) {
  // Item might exist somewhere
}
```

## Running Tests

```bash
npx ts-node counting_bloom_filter.test.ts
```

## License

MIT License - Part of AllToolkit