/**
 * Tests for Counting Bloom Filter
 * Run with: npx ts-node counting_bloom_filter.test.ts
 */

import { CountingBloomFilter, createCountingBloomFilter, CountingBloomFilterOptions } from './counting_bloom_filter';

// Simple test framework
let passed = 0;
let failed = 0;

function test(name: string, fn: () => void): void {
  try {
    fn();
    console.log(`✓ ${name}`);
    passed++;
  } catch (error: any) {
    console.log(`✗ ${name}`);
    console.log(`  Error: ${error.message}`);
    failed++;
  }
}

function assertEqual<T>(actual: T, expected: T, message?: string): void {
  if (actual !== expected) {
    throw new Error(`Expected ${expected} but got ${actual}.${message ? ` ${message}` : ''}`);
  }
}

function assertTrue(value: boolean, message?: string): void {
  if (!value) {
    throw new Error(`Expected true but got false.${message ? ` ${message}` : ''}`);
  }
}

function assertFalse(value: boolean, message?: string): void {
  if (value) {
    throw new Error(`Expected false but got true.${message ? ` ${message}` : ''}`);
  }
}

// Tests
console.log('\n=== Counting Bloom Filter Tests ===\n');

// Basic functionality tests
test('should create a filter with default settings', () => {
  const filter = createCountingBloomFilter();
  assertTrue(filter.getSize > 0, 'Size should be positive');
  assertTrue(filter.getHashCount > 0, 'Hash count should be positive');
  assertEqual(filter.itemCount, 0, 'Initial item count should be 0');
});

test('should create a filter with custom settings', () => {
  const filter = new CountingBloomFilter({
    expectedItems: 10000,
    falsePositiveRate: 0.001,
    hashCount: 10,
    size: 100000
  });
  assertEqual(filter.getSize, 100000, 'Size should match');
  assertEqual(filter.getHashCount, 10, 'Hash count should match');
});

test('should add and check single item', () => {
  const filter = createCountingBloomFilter();
  filter.add('hello');
  assertTrue(filter.contains('hello'), 'Should contain added item');
  assertFalse(filter.contains('world'), 'Should not contain unadded item');
});

test('should add and check multiple items', () => {
  const filter = createCountingBloomFilter(1000);
  const items = ['apple', 'banana', 'cherry', 'date', 'elderberry'];
  
  for (const item of items) {
    filter.add(item);
  }
  
  for (const item of items) {
    assertTrue(filter.contains(item), `Should contain ${item}`);
  }
  
  assertEqual(filter.itemCount, 5, 'Item count should be 5');
});

test('should remove item', () => {
  const filter = createCountingBloomFilter();
  filter.add('test');
  assertTrue(filter.contains('test'), 'Should contain added item');
  
  const removed = filter.remove('test');
  assertTrue(removed, 'Remove should return true');
  assertFalse(filter.contains('test'), 'Should not contain removed item');
  assertEqual(filter.itemCount, 0, 'Item count should be 0');
});

test('should return false when removing non-existent item', () => {
  const filter = createCountingBloomFilter();
  filter.add('exists');
  
  const removed = filter.remove('nonexistent');
  assertFalse(removed, 'Remove should return false for non-existent item');
  assertEqual(filter.itemCount, 1, 'Item count should remain 1');
});

test('should handle adding same item multiple times', () => {
  const filter = createCountingBloomFilter();
  
  filter.add('test');
  filter.add('test');
  filter.add('test');
  
  assertTrue(filter.contains('test'), 'Should contain the item');
  assertEqual(filter.itemCount, 3, 'Item count should be 3');
  
  // Should need to remove 3 times
  filter.remove('test');
  assertTrue(filter.contains('test'), 'Should still contain after 1 removal');
  filter.remove('test');
  assertTrue(filter.contains('test'), 'Should still contain after 2 removals');
  filter.remove('test');
  assertFalse(filter.contains('test'), 'Should not contain after 3 removals');
});

test('should get approximate count', () => {
  const filter = createCountingBloomFilter();
  
  filter.add('item');
  assertEqual(filter.approximateCount('item'), 1, 'Count should be approximately 1');
  
  filter.add('item');
  filter.add('item');
  assertEqual(filter.approximateCount('item'), 3, 'Count should be approximately 3');
  
  assertEqual(filter.approximateCount('nonexistent'), 0, 'Non-existent item should have count 0');
});

test('should clear all items', () => {
  const filter = createCountingBloomFilter();
  
  filter.add('a');
  filter.add('b');
  filter.add('c');
  
  assertEqual(filter.itemCount, 3, 'Should have 3 items');
  
  filter.clear();
  
  assertEqual(filter.itemCount, 0, 'Should have 0 items after clear');
  assertFalse(filter.contains('a'), 'Should not contain a after clear');
  assertFalse(filter.contains('b'), 'Should not contain b after clear');
  assertFalse(filter.contains('c'), 'Should not contain c after clear');
});

test('should serialize and deserialize', () => {
  const filter = createCountingBloomFilter();
  filter.add('item1');
  filter.add('item2');
  filter.add('item3');
  
  const json = filter.toJSON();
  const restored = CountingBloomFilter.fromJSON(json);
  
  assertTrue(restored.contains('item1'), 'Restored filter should contain item1');
  assertTrue(restored.contains('item2'), 'Restored filter should contain item2');
  assertTrue(restored.contains('item3'), 'Restored filter should contain item3');
  assertFalse(restored.contains('item4'), 'Restored filter should not contain item4');
  assertEqual(restored.itemCount, 3, 'Restored item count should match');
});

test('should get statistics', () => {
  const filter = createCountingBloomFilter(1000, 0.01);
  filter.add('item1');
  filter.add('item2');
  
  const stats = filter.getStats();
  
  assertEqual(stats.size, filter.getSize, 'Stats size should match filter size');
  assertEqual(stats.hashCount, filter.getHashCount, 'Stats hash count should match');
  assertEqual(stats.itemCount, 2, 'Stats item count should be 2');
  assertTrue(stats.loadFactor > 0, 'Load factor should be positive');
  assertTrue(stats.estimatedFPR >= 0 && stats.estimatedFPR < 1, 'FPR should be valid probability');
});

test('should merge two filters', () => {
  const filter1 = new CountingBloomFilter({ expectedItems: 100, size: 1000, hashCount: 5 });
  const filter2 = new CountingBloomFilter({ expectedItems: 100, size: 1000, hashCount: 5 });
  
  filter1.add('a');
  filter1.add('b');
  filter2.add('c');
  filter2.add('d');
  
  const merged = filter1.merge(filter2);
  
  assertTrue(merged.contains('a'), 'Merged should contain a');
  assertTrue(merged.contains('b'), 'Merged should contain b');
  assertTrue(merged.contains('c'), 'Merged should contain c');
  assertTrue(merged.contains('d'), 'Merged should contain d');
  assertEqual(merged.itemCount, 4, 'Merged item count should be 4');
});

test('should throw when merging incompatible filters', () => {
  const filter1 = new CountingBloomFilter({ expectedItems: 100, size: 1000, hashCount: 5 });
  const filter2 = new CountingBloomFilter({ expectedItems: 100, size: 2000, hashCount: 5 });
  
  let error: Error | null = null;
  try {
    filter1.merge(filter2);
  } catch (e) {
    error = e as Error;
  }
  
  assertTrue(error !== null, 'Should throw error for incompatible merge');
});

test('should estimate Jaccard similarity', () => {
  const filter1 = new CountingBloomFilter({ expectedItems: 100, size: 10000, hashCount: 7 });
  const filter2 = new CountingBloomFilter({ expectedItems: 100, size: 10000, hashCount: 7 });
  
  // Add common items
  filter1.add('common1');
  filter1.add('common2');
  filter2.add('common1');
  filter2.add('common2');
  
  // Add unique items
  filter1.add('unique1');
  filter2.add('unique2');
  
  const similarity = filter1.estimateJaccardSimilarity(filter2);
  assertTrue(similarity >= 0 && similarity <= 1, 'Similarity should be between 0 and 1');
  assertTrue(similarity > 0, 'Similarity should be positive for overlapping sets');
});

test('should handle remove all', () => {
  const filter = createCountingBloomFilter();
  
  filter.add('item');
  filter.add('item');
  filter.add('item');
  
  assertEqual(filter.approximateCount('item'), 3, 'Should have 3 counts');
  
  const removed = filter.removeAll('item');
  assertEqual(removed, 3, 'Should have removed 3 times');
  assertFalse(filter.contains('item'), 'Should not contain item after removeAll');
});

test('should handle addMultiple', () => {
  const filter = createCountingBloomFilter();
  
  const success = filter.addMultiple('item', 5);
  assertTrue(success, 'addMultiple should succeed');
  assertEqual(filter.approximateCount('item'), 5, 'Should have 5 counts');
});

test('should validate constructor parameters', () => {
  let error: Error | null = null;
  
  try {
    new CountingBloomFilter({ expectedItems: 0 });
  } catch (e) {
    error = e as Error;
  }
  assertTrue(error !== null, 'Should throw for zero expectedItems');
  
  error = null;
  try {
    new CountingBloomFilter({ expectedItems: 100, falsePositiveRate: 0 });
  } catch (e) {
    error = e as Error;
  }
  assertTrue(error !== null, 'Should throw for zero falsePositiveRate');
  
  error = null;
  try {
    new CountingBloomFilter({ expectedItems: 100, falsePositiveRate: 1 });
  } catch (e) {
    error = e as Error;
  }
  assertTrue(error !== null, 'Should throw for falsePositiveRate of 1');
});

test('should handle large dataset', () => {
  const filter = createCountingBloomFilter(10000, 0.01);
  
  // Add 10000 items
  for (let i = 0; i < 10000; i++) {
    filter.add(`item-${i}`);
  }
  
  assertEqual(filter.itemCount, 10000, 'Should have 10000 items');
  
  // Check all items are present
  let allPresent = true;
  for (let i = 0; i < 10000; i++) {
    if (!filter.contains(`item-${i}`)) {
      allPresent = false;
      break;
    }
  }
  assertTrue(allPresent, 'All added items should be present');
  
  // Check false positive rate
  let falsePositives = 0;
  for (let i = 0; i < 1000; i++) {
    if (filter.contains(`nonexistent-${i}`)) {
      falsePositives++;
    }
  }
  
  const actualFPR = falsePositives / 1000;
  assertTrue(actualFPR < 0.05, `False positive rate should be below 5%, got ${(actualFPR * 100).toFixed(2)}%`);
});

// Summary
console.log('\n=== Test Summary ===');
console.log(`Passed: ${passed}`);
console.log(`Failed: ${failed}`);
console.log(`Total: ${passed + failed}`);

if (failed > 0) {
  process.exit(1);
}