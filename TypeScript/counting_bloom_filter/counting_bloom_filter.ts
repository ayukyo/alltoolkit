/**
 * Counting Bloom Filter - A probabilistic data structure that supports:
 * - Adding elements
 * - Checking membership (with possible false positives)
 * - Removing elements (unlike standard Bloom Filter)
 * 
 * Time Complexity: O(k) for all operations where k is the number of hash functions
 * Space Complexity: O(m * c) where m is array size and c is counter bits
 * 
 * @author AllToolkit
 * @date 2026-04-27
 */

/**
 * MurmurHash3 implementation for consistent hashing
 */
function murmurhash3(key: string, seed: number): number {
  let h1 = seed >>> 0;
  const c1 = 0xcc9e2d51;
  const c2 = 0x1b873593;
  
  for (let i = 0; i < key.length; i++) {
    let k1 = key.charCodeAt(i);
    k1 = Math.imul(k1, c1) >>> 0;
    k1 = ((k1 << 15) | (k1 >>> 17)) >>> 0;
    k1 = Math.imul(k1, c2) >>> 0;
    h1 ^= k1;
    h1 = ((h1 << 13) | (h1 >>> 19)) >>> 0;
    h1 = (Math.imul(h1, 5) + 0xe6546b64) >>> 0;
  }
  
  h1 ^= key.length;
  h1 ^= h1 >>> 16;
  h1 = Math.imul(h1, 0x85ebca6b) >>> 0;
  h1 ^= h1 >>> 13;
  h1 = Math.imul(h1, 0xc2b2ae35) >>> 0;
  h1 ^= h1 >>> 16;
  
  return h1 >>> 0;
}

/**
 * Configuration options for the Counting Bloom Filter
 */
export interface CountingBloomFilterOptions {
  /** Expected number of elements */
  expectedItems: number;
  /** Desired false positive rate (0 < fpr < 1) */
  falsePositiveRate?: number;
  /** Number of hash functions (auto-calculated if not provided) */
  hashCount?: number;
  /** Size of the filter in bits (auto-calculated if not provided) */
  size?: number;
  /** Maximum value for each counter (default: 255 for uint8) */
  maxCounterValue?: number;
}

/**
 * Statistics for the Counting Bloom Filter
 */
export interface CountingBloomFilterStats {
  /** Total size of the filter */
  size: number;
  /** Number of hash functions */
  hashCount: number;
  /** Number of elements added */
  itemCount: number;
  /** Current load factor */
  loadFactor: number;
  /** Estimated current false positive rate */
  estimatedFPR: number;
  /** Total count across all counters */
  totalCount: number;
  /** Number of non-zero counters */
  nonZeroCounters: number;
}

/**
 * Counting Bloom Filter implementation
 * 
 * @example
 * ```typescript
 * const filter = new CountingBloomFilter({
 *   expectedItems: 1000,
 *   falsePositiveRate: 0.01
 * });
 * 
 * filter.add('hello');
 * console.log(filter.contains('hello')); // true
 * console.log(filter.contains('world')); // false (probably)
 * 
 * filter.remove('hello');
 * console.log(filter.contains('hello')); // false
 * ```
 */
export class CountingBloomFilter {
  private readonly counters: Uint8Array;
  private readonly size: number;
  private readonly hashCount: number;
  private readonly maxCounterValue: number;
  private _itemCount: number = 0;
  
  /**
   * Creates a new Counting Bloom Filter
   */
  constructor(options: CountingBloomFilterOptions) {
    if (options.expectedItems <= 0) {
      throw new Error('Expected items must be positive');
    }
    
    if (options.falsePositiveRate !== undefined) {
      if (options.falsePositiveRate <= 0 || options.falsePositiveRate >= 1) {
        throw new Error('False positive rate must be between 0 and 1 (exclusive)');
      }
    }
    
    // Calculate optimal size and hash count if not provided
    const n = options.expectedItems;
    const p = options.falsePositiveRate ?? 0.01;
    
    this.size = options.size ?? Math.ceil(-n * Math.log(p) / (Math.LN2 * Math.LN2));
    this.hashCount = options.hashCount ?? Math.ceil((this.size / n) * Math.LN2);
    this.maxCounterValue = options.maxCounterValue ?? 255;
    
    this.counters = new Uint8Array(this.size);
  }
  
  /**
   * Generates hash values for an item
   */
  private getHashIndices(item: string): number[] {
    const indices: number[] = [];
    const hash1 = murmurhash3(item, 0);
    const hash2 = murmurhash3(item, hash1);
    
    for (let i = 0; i < this.hashCount; i++) {
      // Double hashing to generate multiple hash values
      const combinedHash = (hash1 + i * hash2) >>> 0;
      indices.push(combinedHash % this.size);
    }
    
    return indices;
  }
  
  /**
   * Adds an item to the filter
   * @returns true if the item was added, false if any counter would overflow
   */
  add(item: string): boolean {
    const indices = this.getHashIndices(item);
    
    // Check for potential overflow first
    for (const index of indices) {
      if (this.counters[index] >= this.maxCounterValue) {
        return false;
      }
    }
    
    // Increment all counters
    for (const index of indices) {
      this.counters[index]++;
    }
    
    this._itemCount++;
    return true;
  }
  
  /**
   * Adds an item multiple times
   * @returns true if all additions succeeded
   */
  addMultiple(item: string, count: number): boolean {
    for (let i = 0; i < count; i++) {
      if (!this.add(item)) {
        return false;
      }
    }
    return true;
  }
  
  /**
   * Checks if an item might be in the filter
   * @returns true if the item might be present, false if definitely not present
   */
  contains(item: string): boolean {
    const indices = this.getHashIndices(item);
    
    for (const index of indices) {
      if (this.counters[index] === 0) {
        return false;
      }
    }
    
    return true;
  }
  
  /**
   * Gets the approximate count of an item
   * This returns the minimum counter value at the item's hash indices
   */
  approximateCount(item: string): number {
    const indices = this.getHashIndices(item);
    let minCount = this.maxCounterValue;
    
    for (const index of indices) {
      if (this.counters[index] < minCount) {
        minCount = this.counters[index];
      }
    }
    
    return minCount;
  }
  
  /**
   * Removes an item from the filter
   * @returns true if the item was removed, false if the item was not present
   */
  remove(item: string): boolean {
    if (!this.contains(item)) {
      return false;
    }
    
    const indices = this.getHashIndices(item);
    
    for (const index of indices) {
      this.counters[index]--;
    }
    
    this._itemCount--;
    return true;
  }
  
  /**
   * Removes all occurrences of an item
   * @returns the number of times the item was removed
   */
  removeAll(item: string): number {
    let removed = 0;
    while (this.remove(item)) {
      removed++;
    }
    return removed;
  }
  
  /**
   * Clears all items from the filter
   */
  clear(): void {
    this.counters.fill(0);
    this._itemCount = 0;
  }
  
  /**
   * Gets the number of items currently in the filter
   */
  get itemCount(): number {
    return this._itemCount;
  }
  
  /**
   * Gets the size of the filter
   */
  get getSize(): number {
    return this.size;
  }
  
  /**
   * Gets the number of hash functions used
   */
  get getHashCount(): number {
    return this.hashCount;
  }
  
  /**
   * Gets statistics about the filter
   */
  getStats(): CountingBloomFilterStats {
    let totalCount = 0;
    let nonZeroCounters = 0;
    
    for (let i = 0; i < this.size; i++) {
      totalCount += this.counters[i];
      if (this.counters[i] > 0) {
        nonZeroCounters++;
      }
    }
    
    const loadFactor = nonZeroCounters / this.size;
    
    // Estimate current false positive rate
    // P(false positive) ≈ (1 - e^(-kn/m))^k
    const n = this.itemCount;
    const k = this.hashCount;
    const m = this.size;
    const exponent = -k * n / m;
    const estimatedFPR = Math.pow(1 - Math.exp(exponent), k);
    
    return {
      size: this.size,
      hashCount: this.hashCount,
      itemCount: this.itemCount,
      loadFactor,
      estimatedFPR,
      totalCount,
      nonZeroCounters
    };
  }
  
  /**
   * Serializes the filter to a JSON-compatible object
   */
  toJSON(): object {
    return {
      size: this.size,
      hashCount: this.hashCount,
      maxCounterValue: this.maxCounterValue,
      itemCount: this.itemCount,
      counters: Array.from(this.counters)
    };
  }
  
  /**
   * Creates a filter from a JSON object
   */
  static fromJSON(json: any): CountingBloomFilter {
    const filter = new CountingBloomFilter({
      expectedItems: json.itemCount || 1000,
      size: json.size,
      hashCount: json.hashCount,
      maxCounterValue: json.maxCounterValue
    });
    
    filter._itemCount = json.itemCount;
    
    for (let i = 0; i < json.counters.length; i++) {
      filter.counters[i] = json.counters[i];
    }
    
    return filter;
  }
  
  /**
   * Merges two Counting Bloom Filters
   * Both filters must have the same size and hash count
   */
  merge(other: CountingBloomFilter): CountingBloomFilter {
    if (this.size !== other.size || this.hashCount !== other.hashCount) {
      throw new Error('Cannot merge filters with different configurations');
    }
    
    const merged = new CountingBloomFilter({
      expectedItems: this.itemCount + other.itemCount,
      size: this.size,
      hashCount: this.hashCount,
      maxCounterValue: this.maxCounterValue
    });
    
    for (let i = 0; i < this.size; i++) {
      const sum = this.counters[i] + other.counters[i];
      merged.counters[i] = Math.min(sum, this.maxCounterValue);
    }
    
    merged._itemCount = this.itemCount + other.itemCount;
    
    return merged;
  }
  
  /**
   * Estimates the union size of two Counting Bloom Filters
   */
  estimateUnionSize(other: CountingBloomFilter): number {
    if (this.size !== other.size) {
      throw new Error('Filters must have the same size');
    }
    
    let unionCount = 0;
    for (let i = 0; i < this.size; i++) {
      unionCount += Math.max(this.counters[i], other.counters[i]);
    }
    
    // This is an approximation
    return Math.round(unionCount / this.hashCount);
  }
  
  /**
   * Estimates the intersection size of two Counting Bloom Filters
   */
  estimateIntersectionSize(other: CountingBloomFilter): number {
    if (this.size !== other.size) {
      throw new Error('Filters must have the same size');
    }
    
    let intersectionCount = 0;
    for (let i = 0; i < this.size; i++) {
      intersectionCount += Math.min(this.counters[i], other.counters[i]);
    }
    
    // This is an approximation
    return Math.round(intersectionCount / this.hashCount);
  }
  
  /**
   * Estimates the Jaccard similarity between two Counting Bloom Filters
   */
  estimateJaccardSimilarity(other: CountingBloomFilter): number {
    const intersection = this.estimateIntersectionSize(other);
    const union = this.estimateUnionSize(other);
    
    if (union === 0) {
      return 0;
    }
    
    return intersection / union;
  }
}

/**
 * Creates a Counting Bloom Filter with default settings
 */
export function createCountingBloomFilter(
  expectedItems: number = 1000,
  falsePositiveRate: number = 0.01
): CountingBloomFilter {
  return new CountingBloomFilter({
    expectedItems,
    falsePositiveRate
  });
}

export default CountingBloomFilter;