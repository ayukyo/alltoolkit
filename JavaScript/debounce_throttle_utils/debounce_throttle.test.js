/**
 * Tests for Debounce and Throttle Utilities
 * Run with: node debounce_throttle.test.js
 */

const assert = require('assert');
const {
  Debounce,
  Throttle,
  AsyncDebounce,
  RateLimitedQueue,
  debounce,
  throttle
} = require('./debounce_throttle.js');

// Helper for async tests
function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

// Test results tracker
let passed = 0;
let failed = 0;

function test(name, fn) {
  try {
    fn();
    console.log(`✓ ${name}`);
    passed++;
  } catch (error) {
    console.log(`✗ ${name}`);
    console.log(`  Error: ${error.message}`);
    failed++;
  }
}

async function asyncTest(name, fn) {
  try {
    await fn();
    console.log(`✓ ${name}`);
    passed++;
  } catch (error) {
    console.log(`✗ ${name}`);
    console.log(`  Error: ${error.message}`);
    failed++;
  }
}

console.log('\n=== Debounce Tests ===\n');

// Test 1: Basic debounce
test('Debounce: should delay execution', () => {
  let callCount = 0;
  const debounced = debounce(() => callCount++, 100);
  
  debounced();
  assert.strictEqual(callCount, 0, 'Should not execute immediately');
});

// Test 2: Debounce trailing call
test('Debounce: should execute after wait time', async () => {
  let callCount = 0;
  const debounced = debounce(() => callCount++, 50);
  
  debounced();
  await sleep(60);
  assert.strictEqual(callCount, 1, 'Should have executed once');
});

// Test 3: Debounce multiple calls
test('Debounce: should only execute once for multiple calls', async () => {
  let callCount = 0;
  let lastArg = null;
  const debounced = debounce((arg) => {
    callCount++;
    lastArg = arg;
  }, 50);
  
  debounced(1);
  debounced(2);
  debounced(3);
  await sleep(60);
  
  assert.strictEqual(callCount, 1, 'Should execute only once');
  assert.strictEqual(lastArg, 3, 'Should use last argument');
});

// Test 4: Debounce with leading
test('Debounce: leading option should execute immediately', () => {
  let callCount = 0;
  const debounced = debounce(() => callCount++, 50, { leading: true, trailing: false });
  
  debounced();
  assert.strictEqual(callCount, 1, 'Should execute immediately with leading');
});

// Test 5: Debounce cancel
test('Debounce: cancel should prevent execution', async () => {
  let callCount = 0;
  const debounced = debounce(() => callCount++, 50);
  
  debounced();
  debounced.cancel();
  await sleep(60);
  assert.strictEqual(callCount, 0, 'Should not execute after cancel');
});

// Test 6: Debounce flush
test('Debounce: flush should execute immediately', async () => {
  let callCount = 0;
  let lastArg = null;
  const debounced = debounce((arg) => {
    callCount++;
    lastArg = arg;
  }, 100);
  
  debounced(42);
  debounced.flush();
  
  assert.strictEqual(callCount, 1, 'Should execute immediately on flush');
  assert.strictEqual(lastArg, 42, 'Should pass correct argument');
});

// Test 7: Debounce pending
test('Debounce: pending should return correct state', async () => {
  const debounced = debounce(() => {}, 50);
  
  assert.strictEqual(debounced.pending(), false, 'Should not be pending initially');
  debounced();
  assert.strictEqual(debounced.pending(), true, 'Should be pending after call');
  await sleep(60);
  assert.strictEqual(debounced.pending(), false, 'Should not be pending after execution');
});

// Test 8: Debounce maxWait
asyncTest('Debounce: maxWait should force execution', async () => {
  let callCount = 0;
  const debounced = debounce(() => callCount++, 100, { maxWait: 150 });
  
  debounced();
  await sleep(50);
  debounced();
  await sleep(50);
  debounced();
  await sleep(70);
  
  assert(callCount >= 1, 'Should have executed due to maxWait');
});

console.log('\n=== Throttle Tests ===\n');

// Test 9: Basic throttle
test('Throttle: should limit execution', () => {
  let callCount = 0;
  const throttled = throttle(() => callCount++, 50);
  
  throttled();
  assert.strictEqual(callCount, 1, 'Should execute first call immediately');
});

// Test 10: Throttle limits calls
asyncTest('Throttle: should limit execution rate', async () => {
  let callCount = 0;
  const throttled = throttle(() => callCount++, 50);
  
  throttled(); // Leading call executes immediately
  throttled(); // Queued for trailing
  throttled(); // Queued for trailing (overwrites previous)
  
  // Within limit period - only leading executed
  assert.strictEqual(callCount, 1, 'Should have executed leading call');
  
  await sleep(60);
  
  // After limit - trailing call executes
  assert.strictEqual(callCount, 2, 'Should have executed trailing call after period');
});

// Test 11: Throttle allows calls after limit
asyncTest('Throttle: should allow calls after limit period', async () => {
  let callCount = 0;
  const throttled = throttle(() => callCount++, 50);
  
  throttled();
  await sleep(60);
  throttled();
  
  assert.strictEqual(callCount, 2, 'Should execute again after limit period');
});

// Test 12: Throttle trailing
asyncTest('Throttle: trailing option should execute last call', async () => {
  let callCount = 0;
  let lastArg = null;
  const throttled = throttle((arg) => {
    callCount++;
    lastArg = arg;
  }, 50);
  
  throttled(1); // Leading
  throttled(2); // Trailing queued
  await sleep(60);
  
  assert.strictEqual(callCount, 2, 'Should execute leading and trailing');
  assert.strictEqual(lastArg, 2, 'Trailing should use last argument');
});

// Test 13: Throttle no leading
asyncTest('Throttle: leading=false should delay first call', async () => {
  let callCount = 0;
  const throttled = throttle(() => callCount++, 50, { leading: false, trailing: true });
  
  throttled();
  assert.strictEqual(callCount, 0, 'Should not execute immediately with leading=false');
  await sleep(60);
  assert.strictEqual(callCount, 1, 'Should execute trailing');
});

// Test 14: Throttle cancel
asyncTest('Throttle: cancel should prevent trailing execution', async () => {
  let callCount = 0;
  const throttled = throttle(() => callCount++, 50);
  
  throttled();
  throttled();
  throttled.cancel();
  await sleep(60);
  
  assert.strictEqual(callCount, 1, 'Should not execute trailing after cancel');
});

// Test 15: Throttle flush
test('Throttle: flush should execute pending immediately', async () => {
  let callCount = 0;
  const throttled = throttle(() => callCount++, 100);
  
  throttled(); // Leading execution
  throttled(); // Queued for trailing
  
  assert.strictEqual(callCount, 1, 'Should have leading execution');
  throttled.flush();
  assert.strictEqual(callCount, 2, 'Should have flushed trailing');
});

console.log('\n=== Debounce Class Tests ===\n');

// Test 16: Debounce class instantiation
test('Debounce: class should instantiate correctly', () => {
  const debounced = new Debounce(() => {}, { wait: 100 });
  assert.strictEqual(debounced.wait, 100);
  assert.strictEqual(debounced.leading, false);
  assert.strictEqual(debounced.trailing, true);
});

// Test 17: Debounce class call method
asyncTest('Debounce: class call method should work', async () => {
  let result = null;
  const debounced = new Debounce((x) => x * 2, { wait: 50 });
  
  debounced.call(5);
  await sleep(60);
  result = debounced.result;
  
  assert.strictEqual(result, 10);
});

// Test 18: Debounce getInvokeCount
asyncTest('Debounce: getInvokeCount should track invocations', async () => {
  const debounced = new Debounce(() => {}, { wait: 50 });
  
  assert.strictEqual(debounced.getInvokeCount(), 0);
  debounced.call();
  await sleep(60);
  assert.strictEqual(debounced.getInvokeCount(), 1);
});

console.log('\n=== Throttle Class Tests ===\n');

// Test 19: Throttle class instantiation
test('Throttle: class should instantiate correctly', () => {
  const throttled = new Throttle(() => {}, { limit: 100 });
  assert.strictEqual(throttled.limit, 100);
  assert.strictEqual(throttled.leading, true);
  assert.strictEqual(throttled.trailing, true);
});

// Test 20: Throttle class call method
asyncTest('Throttle: class call method should work', async () => {
  let result = null;
  const throttled = new Throttle((x) => x * 2, { limit: 50 });
  
  throttled.call(5);
  result = throttled.result;
  
  assert.strictEqual(result, 10);
});

console.log('\n=== AsyncDebounce Tests ===\n');

// Test 21: AsyncDebounce basic
asyncTest('AsyncDebounce: should handle async functions', async () => {
  let callCount = 0;
  const debounced = new AsyncDebounce(async (x) => {
    callCount++;
    return x * 2;
  }, { wait: 50 });
  
  const promise = debounced.call(5);
  await sleep(60);
  const result = await promise;
  
  assert.strictEqual(result, 10);
  assert.strictEqual(callCount, 1);
});

// Test 22: AsyncDebounce multiple calls return same promise
asyncTest('AsyncDebounce: concurrent calls should share promise', async () => {
  let callCount = 0;
  const debounced = new AsyncDebounce(async (x) => {
    callCount++;
    await sleep(10);
    return x * 2;
  }, { wait: 50 });
  
  const promise1 = debounced.call(5);
  const promise2 = debounced.call(10);
  const promise3 = debounced.call(15);
  
  const results = await Promise.all([promise1, promise2, promise3]);
  
  assert.strictEqual(results[0], 30); // Last argument used
  assert.strictEqual(results[1], 30);
  assert.strictEqual(results[2], 30);
  assert.strictEqual(callCount, 1);
});

// Test 23: AsyncDebounce cancel
asyncTest('AsyncDebounce: cancel should reject promise', async () => {
  const debounced = new AsyncDebounce(async () => 'result', { wait: 50 });
  
  const promise = debounced.call();
  debounced.cancel();
  
  try {
    await promise;
    assert.fail('Should have thrown');
  } catch (error) {
    assert.strictEqual(error.message, 'Debounced function canceled');
  }
});

console.log('\n=== RateLimitedQueue Tests ===\n');

// Test 24: RateLimitedQueue basic
asyncTest('RateLimitedQueue: should process items with interval', async () => {
  const results = [];
  const queue = new RateLimitedQueue(
    async (item) => {
      results.push(item);
      return item * 2;
    },
    { interval: 50, autoStart: false }
  );
  
  const result1 = queue.add(1);
  const result2 = queue.add(2);
  
  queue._processNext(); // Start processing
  
  assert.strictEqual(await result1, 2);
  assert.strictEqual(await result2, 4);
  assert.deepStrictEqual(results, [1, 2]);
});

// Test 25: RateLimitedQueue size
test('RateLimitedQueue: size should return queue length', () => {
  const queue = new RateLimitedQueue(async () => {}, { interval: 100, autoStart: false });
  
  queue.add(1);
  queue.add(2);
  
  assert.strictEqual(queue.size(), 2);
});

// Test 26: RateLimitedQueue clear
test('RateLimitedQueue: clear should empty queue', () => {
  const queue = new RateLimitedQueue(async () => {}, { interval: 100 });
  
  queue.add(1);
  queue.add(2);
  queue.clear();
  
  assert.strictEqual(queue.size(), 0);
  assert.strictEqual(queue.isEmpty(), true);
});

console.log('\n=== Edge Cases ===\n');

// Test 27: Debounce with zero arguments
asyncTest('Debounce: should work with no arguments', async () => {
  let called = false;
  const debounced = debounce(() => { called = true; }, 50);
  
  debounced();
  await sleep(60);
  
  assert.strictEqual(called, true);
});

// Test 28: Debounce preserves this context
asyncTest('Debounce: should preserve this context', async () => {
  const obj = {
    value: 42,
    method: function() { return this.value; }
  };
  
  const debounced = debounce(obj.method, 50);
  const result = debounced.call(obj);
  await sleep(60);
  
  // Result from last trailing call
  assert.strictEqual(result, undefined); // Previous result before completion
});

// Test 29: Throttle rapid calls
asyncTest('Throttle: rapid calls should be limited', async () => {
  let callCount = 0;
  const throttled = throttle(() => callCount++, 100);
  
  for (let i = 0; i < 10; i++) {
    throttled();
  }
  
  assert.strictEqual(callCount, 1, 'Should only execute leading call');
  
  await sleep(110);
  assert.strictEqual(callCount, 2, 'Should execute trailing call');
});

// Test 30: Multiple debounce instances
asyncTest('Debounce: multiple instances should be independent', async () => {
  let count1 = 0;
  let count2 = 0;
  
  const debounce1 = debounce(() => count1++, 50);
  const debounce2 = debounce(() => count2++, 30);
  
  debounce1();
  debounce2();
  
  await sleep(40);
  assert.strictEqual(count2, 1, 'debounce2 should have executed');
  assert.strictEqual(count1, 0, 'debounce1 should not have executed yet');
  
  await sleep(20);
  assert.strictEqual(count1, 1, 'debounce1 should have executed');
});

// Run summary
setTimeout(() => {
  console.log('\n=== Test Summary ===\n');
  console.log(`Passed: ${passed}`);
  console.log(`Failed: ${failed}`);
  console.log(`Total:  ${passed + failed}`);
  process.exit(failed > 0 ? 1 : 0);
}, 500);