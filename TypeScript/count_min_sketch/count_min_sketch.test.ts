/**
 * Count-Min Sketch Test Suite
 * Comprehensive tests for probabilistic frequency estimation
 */

import {
  CountMinSketch,
  CountMinConfig,
  runTests
} from './src/index';

// ==================== Test Utilities ====================

let passedTests = 0;
let failedTests = 0;

function assert(condition: boolean, message: string): void {
  if (condition) {
    passedTests++;
    console.log(`✅ PASS: ${message}`);
  } else {
    failedTests++;
    console.log(`❌ FAIL: ${message}`);
  }
}

function assertEqual<T>(actual: T, expected: T, message: string): void {
  if (actual === expected) {
    passedTests++;
    console.log(`✅ PASS: ${message}`);
  } else {
    failedTests++;
    console.log(`❌ FAIL: ${message} (actual: ${actual}, expected: ${expected})`);
  }
}

function assertApprox(actual: number, expected: number, tolerance: number, message: string): void {
  const diff = Math.abs(actual - expected);
  if (diff <= tolerance) {
    passedTests++;
    console.log(`✅ PASS: ${message} (actual: ${actual}, expected: ${expected})`);
  } else {
    failedTests++;
    console.log(`❌ FAIL: ${message} (actual: ${actual}, expected: ${expected}, diff: ${diff})`);
  }
}

function assertGreaterOrEqual(actual: number, min: number, message: string): void {
  if (actual >= min) {
    passedTests++;
    console.log(`✅ PASS: ${message}`);
  } else {
    failedTests++;
    console.log(`❌ FAIL: ${message} (actual: ${actual}, expected: >= ${min})`);
  }
}

function describe(name: string, fn: () => void): void {
  console.log(`\n📋 ${name}`);
  console.log('─'.repeat(50));
  fn();
}

// ==================== Constructor Tests ====================

describe('CountMinSketch Constructor', () => {
  const sketch = new CountMinSketch<string>(5, 100);

  assertEqual(sketch.dimensions()[0], 5, 'Depth should be 5');
  assertEqual(sketch.dimensions()[1], 100, 'Width should be 100');
  assertEqual(sketch.totalCount(), 0, 'Initial total count should be 0');
  assertEqual(sketch.estimate('anything'), 0, 'Initial estimate should be 0');
});

// ==================== Increment Tests ====================

describe('CountMinSketch Increment', () => {
  const sketch = new CountMinSketch<string>(5, 100);

  sketch.increment('hello');
  sketch.increment('hello');
  sketch.increment('world');

  assertGreaterOrEqual(sketch.estimate('hello'), 2, 'hello estimated >= 2');
  assertGreaterOrEqual(sketch.estimate('world'), 1, 'world estimated >= 1');
  assertEqual(sketch.estimate('missing'), 0, 'unknown item should be 0');
  assertEqual(sketch.totalCount(), 3, 'Total count should be 3');
});

// ==================== Update Tests ====================

describe('CountMinSketch Update', () => {
  const sketch = new CountMinSketch<string>(5, 100);

  sketch.update('item', 5);
  assertGreaterOrEqual(sketch.estimate('item'), 5, 'update with delta=5 should give estimate >= 5');

  sketch.update('item', 3);
  assertGreaterOrEqual(sketch.estimate('item'), 8, 'update with additional delta=3 should give estimate >= 8');

  assertEqual(sketch.totalCount(), 8, 'Total count should be 8');
});

// ==================== Total Count Tests ====================

describe('CountMinSketch Total Count', () => {
  const sketch = new CountMinSketch<string>(5, 100);

  sketch.increment('a');
  sketch.update('b', 3);
  sketch.increment('c');

  assertEqual(sketch.totalCount(), 5, 'Total count should be 5');
});

// ==================== Merge Tests ====================

describe('CountMinSketch Merge', () => {
  const sketch1 = new CountMinSketch<string>(5, 100);
  const sketch2 = new CountMinSketch<string>(5, 100);

  sketch1.increment('hello');
  sketch2.increment('world');
  sketch2.increment('world');

  const totalBefore = sketch1.totalCount();
  sketch1.merge(sketch2);

  assertGreaterOrEqual(sketch1.estimate('hello'), 1, 'hello should have at least 1 count after merge');
  assertGreaterOrEqual(sketch1.estimate('world'), 2, 'world should have at least 2 count after merge');
  assertEqual(sketch1.totalCount(), totalBefore + sketch2.totalCount(), 'Total count should be sum of both');
});

// ==================== Merge Dimension Mismatch Tests ====================

describe('CountMinSketch Merge Dimension Mismatch', () => {
  const sketch1 = new CountMinSketch<string>(5, 100);
  const sketch2 = new CountMinSketch<string>(5, 200);

  sketch1.increment('test');

  let threw = false;
  try {
    sketch1.merge(sketch2);
  } catch (e) {
    threw = (e as Error).message === 'Dimension mismatch';
  }

  assert(threw, 'Should throw Dimension mismatch error');
});

// ==================== Clear Tests ====================

describe('CountMinSketch Clear', () => {
  const sketch = new CountMinSketch<string>(5, 100);

  sketch.increment('test');
  sketch.update('other', 3);

  sketch.clear();

  assertEqual(sketch.estimate('test'), 0, 'Estimate should be 0 after clear');
  assertEqual(sketch.estimate('other'), 0, 'Estimate for other should be 0 after clear');
  assertEqual(sketch.totalCount(), 0, 'Total count should be 0 after clear');
});

// ==================== Optimal Config Tests ====================

describe('CountMinSketch Optimal Config', () => {
  const config = CountMinSketch.optimal(0.01, 0.01);

  assert(config.depth >= 1, 'Depth should be >= 1');
  assert(config.width >= 2, 'Width should be >= 2');
  assertEqual(typeof config.seed, 'number', 'Seed should be a number');

  // Verify epsilon/delta relationship
  const width = Math.ceil(Math.E / 0.01);
  const depth = Math.ceil(-Math.log(0.01));
  assertEqual(config.width, width, 'Width should match Math.E / epsilon');
  assertEqual(config.depth, depth, 'Depth should match -Math.log(delta)');
});

// ==================== withRate Factory Tests ====================

describe('CountMinSketch withRate', () => {
  const sketch = CountMinSketch.withRate<string>(0.01, 0.01);

  sketch.increment('apple');
  sketch.increment('banana');
  sketch.increment('apple');

  assertGreaterOrEqual(sketch.estimate('apple'), 2, 'apple should have at least 2 count');
  assertGreaterOrEqual(sketch.estimate('banana'), 1, 'banana should have at least 1 count');
  assertEqual(sketch.totalCount(), 3, 'Total count should be 3');
});

// ==================== Serialization Tests ====================

describe('CountMinSketch Serialization (toBytes)', () => {
  const sketch = new CountMinSketch<string>(7, 200);

  sketch.increment('test');

  const bytes = sketch.toBytes();

  assert(bytes.length > 0, 'Bytes array should not be empty');
  assert(bytes instanceof Uint8Array, 'Should return Uint8Array');
  assertGreaterOrEqual(bytes.length, 32, 'Minimum size should be at least 32 bytes');
});

// ==================== Dimensions Tests ====================

describe('CountMinSketch Dimensions', () => {
  const sketch = new CountMinSketch<string>(7, 200);
  const [d, w] = sketch.dimensions();

  assertEqual(d, 7, 'Depth should match constructor');
  assertEqual(w, 200, 'Width should match constructor');
});

// ==================== Numeric Keys Tests ====================

describe('CountMinSketch Numeric Keys', () => {
  const sketch = new CountMinSketch<number>(5, 100);

  sketch.increment(1);
  sketch.increment(1);
  sketch.increment(2);

  assertGreaterOrEqual(sketch.estimate(1), 2, 'Key 1 estimated >= 2');
  assertGreaterOrEqual(sketch.estimate(2), 1, 'Key 2 estimated >= 1');
  assertEqual(sketch.estimate(999), 0, 'Unknown numeric key should be 0');
});

// ==================== Empty Sketch Tests ====================

describe('CountMinSketch Empty Operations', () => {
  const sketch = new CountMinSketch<string>(3, 50);

  assertEqual(sketch.estimate('nothing'), 0, 'Empty sketch should return 0 for any key');
  assertEqual(sketch.totalCount(), 0, 'Empty sketch should have total count 0');
  assertEqual(sketch.dimensions()[0], 3, 'Empty sketch should have correct depth');
  assertEqual(sketch.dimensions()[1], 50, 'Empty sketch should have correct width');
});

// ==================== Large Delta Update Tests ====================

describe('CountMinSketch Large Delta Update', () => {
  const sketch = new CountMinSketch<string>(5, 100);

  sketch.update('big', 10000);

  assertGreaterOrEqual(sketch.estimate('big'), 10000, 'Large delta update should be estimable');
  assertEqual(sketch.totalCount(), 10000, 'Total count should reflect large delta');
});

// ==================== Reset After Merge Tests ====================

describe('CountMinSketch Merge Then Clear', () => {
  const sketch1 = new CountMinSketch<string>(5, 100);
  const sketch2 = new CountMinSketch<string>(5, 100);

  sketch1.increment('a');
  sketch2.increment('b');
  sketch1.merge(sketch2);
  sketch1.clear();

  assertEqual(sketch1.estimate('a'), 0, 'After clear, estimate should be 0');
  assertEqual(sketch1.estimate('b'), 0, 'After clear, estimate should be 0 for merged items');
  assertEqual(sketch1.totalCount(), 0, 'Total count should be 0 after clear');
});

// ==================== Summary ====================

console.log('\n' + '='.repeat(50));
console.log(`📊 Test Results: ${passedTests} passed, ${failedTests} failed`);
console.log('='.repeat(50));

if (failedTests > 0) {
  process.exit(1);
}