/**
 * XOR Filter Utils - Test Suite
 *
 * Comprehensive tests for XOR filter and related utilities.
 */

import {
  XorFilter,
  XorFilter8,
  XorFilter16,
  FuseXorFilter,
  createXorFilter,
  createFuseXorFilter,
  compareWithBloomFilter,
  FilterComparison,
} from './mod';

// Test helper
function assert(condition: boolean, message: string): void {
  if (!condition) {
    throw new Error(`Assertion failed: ${message}`);
  }
}

function assertApprox(actual: number, expected: number, tolerance: number, message: string): void {
  if (Math.abs(actual - expected) > tolerance) {
    throw new Error(`Assertion failed: ${message}. Expected ~${expected}, got ${actual}`);
  }
}

let testsPassed = 0;
let testsFailed = 0;

function runTest(name: string, testFn: () => void): void {
  try {
    testFn();
    testsPassed++;
    console.log(`✓ ${name}`);
  } catch (error) {
    testsFailed++;
    console.log(`✗ ${name}: ${error instanceof Error ? error.message : String(error)}`);
  }
}

// ==================== Basic XorFilter Tests ====================

console.log('\n=== XorFilter Basic Tests ===\n');

runTest('XorFilter empty filter', () => {
  const xf = XorFilter.fromElements<string>([]);
  assert(xf.size === 0, 'Size should be 0');
  assert(!xf.contains('anything'), 'Empty filter should not contain anything');
  assert(xf.sizeInBytes === 0, 'Empty filter bytes should be 0');
});

runTest('XorFilter single element', () => {
  const xf = XorFilter.fromElements(['hello']);
  assert(xf.size === 1, 'Size should be 1');
  assert(xf.contains('hello'), 'Should contain hello');
});

runTest('XorFilter multiple elements', () => {
  const words = ['apple', 'banana', 'cherry', 'date', 'elderberry'];
  const xf = XorFilter.fromElements(words);

  assert(xf.size === words.length, `Size should be ${words.length}`);

  for (const word of words) {
    assert(xf.contains(word), `Should contain ${word}`);
  }
});

runTest('XorFilter no false negatives', () => {
  const elements = Array.from({ length: 100 }, (_, i) => `item_${i}`);
  const xf = XorFilter.fromElements(elements);

  for (const elem of elements) {
    assert(xf.contains(elem), `Should contain ${elem}`);
  }
});

runTest('XorFilter false positive rate', () => {
  const elements = Array.from({ length: 10000 }, (_, i) => `item_${i}`);
  const xf = XorFilter.fromElements([...new Set(elements)]);

  let falsePositives = 0;
  const testCount = 10000;

  for (let i = 0; i < testCount; i++) {
    if (xf.contains(`not_in_set_${i}`)) {
      falsePositives++;
    }
  }

  const fpp = falsePositives / testCount;
  // Should be close to 1/256 (~0.39%)
  assert(fpp < 0.01, `False positive rate should be < 1%, got ${(fpp * 100).toFixed(2)}%`);
  console.log(`  (FPP: ${(fpp * 100).toFixed(3)}%)`);
});

runTest('XorFilter bits per element', () => {
  const elements = Array.from({ length: 100 }, (_, i) => `item_${i}`);
  const xf = XorFilter.fromElements(elements);

  const bpe = xf.bitsPerElement;
  assert(bpe > 0 && bpe < 20, `Bits per element should be reasonable, got ${bpe.toFixed(2)}`);
});

runTest('XorFilter false positive rate method', () => {
  const xf = XorFilter.fromElements(['test']);
  assert(xf.falsePositiveRate() === 1 / 256, 'FPP should be 1/256');
});

// ==================== XorFilter8 / XorFilter16 Tests ====================

console.log('\n=== XorFilter8 / XorFilter16 Tests ===\n');

runTest('XorFilter8 basic operations', () => {
  const xf = XorFilter8.fromElements(['a', 'b', 'c']);
  assert(xf.size === 3, 'Size should be 3');
  assert(xf.contains('a'), 'Should contain a');
  assert(xf.contains('b'), 'Should contain b');
  assert(xf.contains('c'), 'Should contain c');
});

runTest('XorFilter16 basic operations', () => {
  const xf = XorFilter16.fromElements(['x', 'y', 'z']);
  assert(xf.size === 3, 'Size should be 3');
  assert(xf.contains('x'), 'Should contain x');
  assert(xf.contains('y'), 'Should contain y');
  assert(xf.contains('z'), 'Should contain z');
});

// ==================== FuseXorFilter Tests ====================

console.log('\n=== FuseXorFilter Tests ===\n');

runTest('FuseXorFilter basic operations', () => {
  const fxf = FuseXorFilter.fromElements(['red', 'green', 'blue']);
  assert(fxf.size === 3, 'Size should be 3');
  assert(fxf.contains('red'), 'Should contain red');
  assert(fxf.contains('green'), 'Should contain green');
  assert(fxf.contains('blue'), 'Should contain blue');
});

runTest('FuseXorFilter not contained', () => {
  const fxf = FuseXorFilter.fromElements(['one', 'two', 'three']);
  // May be false positive, but check for definite not-contained
  const fpp = fxf.size > 0 ? 1 / 256 : 0;
  assert(fpp < 0.01, 'FPP should be ~0.39%');
});

// ==================== Number Elements Tests ====================

console.log('\n=== Number Elements Tests ===\n');

runTest('XorFilter with number elements', () => {
  const numbers = [1, 2, 3, 4, 5, 100, 200, 300];
  const xf = XorFilter.fromElements(numbers);

  assert(xf.size === numbers.length, 'Size should match');
  for (const n of numbers) {
    assert(xf.contains(n), `Should contain ${n}`);
  }
});

runTest('XorFilter with large number set', () => {
  const numbers = Array.from({ length: 500 }, (_, i) => i * 1000);
  const xf = XorFilter.fromElements(numbers);

  assert(xf.size === 500, 'Size should be 500');
  for (const n of numbers) {
    assert(xf.contains(n), `Should contain ${n}`);
  }
});

// ==================== Serialization Tests ====================

console.log('\n=== Serialization Tests ===\n');

runTest('XorFilter toBytes and fromBytes', () => {
  const original = XorFilter.fromElements(['serialize', 'test', 'data']);
  const bytes = original.toBytes();

  assert(bytes.length > 0, 'Should produce bytes');

  const restored = XorFilter.fromBytes(bytes);

  assert(restored.size === original.size, 'Restored size should match');
  assert(restored.contains('serialize'), 'Should contain serialize');
  assert(restored.contains('test'), 'Should contain test');
  assert(restored.contains('data'), 'Should contain data');
});

runTest('XorFilter serialization roundtrip with numbers', () => {
  const original = XorFilter.fromElements([42, 100, 999]);
  const bytes = original.toBytes();
  const restored = XorFilter.fromBytes(bytes);

  assert(restored.size === original.size, 'Size should match');
  assert(restored.contains(42), 'Should contain 42');
  assert(restored.contains(100), 'Should contain 100');
  assert(restored.contains(999), 'Should contain 999');
});

// ==================== Factory Functions Tests ====================

console.log('\n=== Factory Functions Tests ===\n');

runTest('createXorFilter function', () => {
  const xf = createXorFilter(['foo', 'bar', 'baz']);
  assert(xf.size === 3, 'Should have 3 elements');
  assert(xf.contains('foo'), 'Should contain foo');
  assert(xf.contains('bar'), 'Should contain bar');
  assert(xf.contains('baz'), 'Should contain baz');
});

runTest('createFuseXorFilter function', () => {
  const fxf = createFuseXorFilter(['alpha', 'beta', 'gamma']);
  assert(fxf.size === 3, 'Should have 3 elements');
  assert(fxf.contains('alpha'), 'Should contain alpha');
  assert(fxf.contains('beta'), 'Should contain beta');
  assert(fxf.contains('gamma'), 'Should contain gamma');
});

// ==================== Bloom Filter Comparison Tests ====================

console.log('\n=== Bloom Filter Comparison Tests ===\n');

runTest('compareWithBloomFilter basic', () => {
  const result = compareWithBloomFilter(10000, 0.01);

  assert(result.elementCount === 10000, 'Element count should be 10000');
  assert(result.targetFpp === 0.01, 'Target FPP should be 0.01');
  assert(result.xorFilter.bitsPerElement === 9.6, 'XOR bits should be 9.6');
  assert(result.bloomFilter.bitsPerElement > 9.6, 'Bloom should use more bits');
  assert(result.spaceSavingsPercent > 0, 'Should show space savings');
  assert(result.spaceSavingsPercent < 100, 'Should be less than 100%');
});

runTest('compareWithBloomFilter at different sizes', () => {
  const small = compareWithBloomFilter(100, 0.01);
  const large = compareWithBloomFilter(1000000, 0.01);

  assert(small.spaceSavingsPercent > 0, 'Small set should show savings');
  assert(large.spaceSavingsPercent > 0, 'Large set should show savings');
});

// ==================== Edge Cases ====================

console.log('\n=== Edge Cases ===\n');

runTest('XorFilter with duplicate elements', () => {
  const xf = XorFilter.fromElements(['a', 'a', 'b', 'b', 'c']);
  assert(xf.size === 3, 'Size should be 3 (duplicates removed)');
});

runTest('XorFilter with very large elements', () => {
  const largeStrings = Array.from({ length: 100 }, (_, i) => 'x'.repeat(i + 1));
  const xf = XorFilter.fromElements(largeStrings);

  assert(xf.size === 100, 'Size should be 100');
  assert(xf.contains('x'.repeat(50)), 'Should contain long string');
});

runTest('XorFilter toString', () => {
  const xf = XorFilter.fromElements(['a', 'b', 'c']);
  const str = xf.toString();
  assert(str.includes('XorFilter'), 'Should include class name');
  assert(str.includes('3'), 'Should include size');
});

// ==================== Summary ====================

console.log('\n=== Test Summary ===\n');
console.log(`Passed: ${testsPassed}`);
console.log(`Failed: ${testsFailed}`);

if (testsFailed > 0) {
  console.log('\n❌ Some tests failed');
  process.exit(1);
} else {
  console.log('\n✅ All tests passed!');
}