/**
 * Tests for Rate Limiter Utilities
 * Run with: node rate_limiter.test.js
 */

const assert = require('assert');
const {
  TokenBucket,
  SlidingWindow,
  FixedWindow,
  LeakyBucket,
  MultiKeyRateLimiter
} = require('./rate_limiter.js');

// Test utilities
let testsPassed = 0;
let testsFailed = 0;

function test(name, fn) {
  try {
    fn();
    console.log(`✓ ${name}`);
    testsPassed++;
  } catch (error) {
    console.log(`✗ ${name}`);
    console.log(`  Error: ${error.message}`);
    testsFailed++;
  }
}

async function asyncTest(name, fn) {
  try {
    await fn();
    console.log(`✓ ${name}`);
    testsPassed++;
  } catch (error) {
    console.log(`✗ ${name}`);
    console.log(`  Error: ${error.message}`);
    testsFailed++;
  }
}

function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

console.log('\n=== TokenBucket Tests ===\n');

test('TokenBucket: should initialize with correct capacity', () => {
  const bucket = new TokenBucket({ capacity: 10, refillRate: 1 });
  assert.strictEqual(bucket.capacity, 10);
  assert.strictEqual(bucket.getTokens(), 10);
});

test('TokenBucket: should consume tokens', () => {
  const bucket = new TokenBucket({ capacity: 10, refillRate: 1 });
  assert.strictEqual(bucket.tryConsume(3), true);
  assert.strictEqual(bucket.getTokens(), 7);
});

test('TokenBucket: should reject when insufficient tokens', () => {
  const bucket = new TokenBucket({ capacity: 5, refillRate: 1 });
  assert.strictEqual(bucket.tryConsume(3), true);
  assert.strictEqual(bucket.tryConsume(3), false);
  assert.strictEqual(bucket.getTokens(), 2);
});

test('TokenBucket: should refill tokens over time', async () => {
  const bucket = new TokenBucket({ capacity: 10, refillRate: 5 });
  bucket.tryConsume(10);
  assert.strictEqual(bucket.getTokens(), 0);
  
  await sleep(200); // 0.2 seconds * 5 tokens/sec = 1 token
  const tokens = bucket.getTokens();
  assert(tokens >= 0.9 && tokens <= 1.5, `Expected ~1 token, got ${tokens}`);
});

test('TokenBucket: should not exceed capacity', async () => {
  const bucket = new TokenBucket({ capacity: 5, refillRate: 10 });
  await sleep(100);
  assert.strictEqual(bucket.getTokens(), 5);
});

test('TokenBucket: should reset to full capacity', () => {
  const bucket = new TokenBucket({ capacity: 10, refillRate: 1 });
  bucket.tryConsume(5);
  bucket.reset();
  assert.strictEqual(bucket.getTokens(), 10);
});

test('TokenBucket: should throw on invalid params', () => {
  assert.throws(() => new TokenBucket({ capacity: 0, refillRate: 1 }), /positive/);
  assert.throws(() => new TokenBucket({ capacity: 10, refillRate: 0 }), /positive/);
});

test('TokenBucket: timeUntilAvailable should return 0 if tokens available', () => {
  const bucket = new TokenBucket({ capacity: 10, refillRate: 1 });
  assert.strictEqual(bucket.timeUntilAvailable(5), 0);
});

console.log('\n=== SlidingWindow Tests ===\n');

test('SlidingWindow: should initialize correctly', () => {
  const window = new SlidingWindow({ maxRequests: 10, windowMs: 1000 });
  assert.strictEqual(window.maxRequests, 10);
  assert.strictEqual(window.getCount(), 0);
});

test('SlidingWindow: should allow requests up to limit', () => {
  const window = new SlidingWindow({ maxRequests: 3, windowMs: 1000 });
  assert.strictEqual(window.tryRequest(), true);
  assert.strictEqual(window.tryRequest(), true);
  assert.strictEqual(window.tryRequest(), true);
  assert.strictEqual(window.getCount(), 3);
});

test('SlidingWindow: should reject over limit', () => {
  const window = new SlidingWindow({ maxRequests: 2, windowMs: 1000 });
  window.tryRequest();
  window.tryRequest();
  assert.strictEqual(window.tryRequest(), false);
});

test('SlidingWindow: should slide window and allow new requests', async () => {
  const window = new SlidingWindow({ maxRequests: 2, windowMs: 100 });
  window.tryRequest();
  window.tryRequest();
  assert.strictEqual(window.tryRequest(), false);
  
  await sleep(150);
  assert.strictEqual(window.tryRequest(), true);
});

test('SlidingWindow: getRemaining should return correct count', () => {
  const window = new SlidingWindow({ maxRequests: 5, windowMs: 1000 });
  assert.strictEqual(window.getRemaining(), 5);
  window.tryRequest();
  assert.strictEqual(window.getRemaining(), 4);
});

test('SlidingWindow: reset should clear all requests', () => {
  const window = new SlidingWindow({ maxRequests: 5, windowMs: 1000 });
  window.tryRequest();
  window.tryRequest();
  window.reset();
  assert.strictEqual(window.getCount(), 0);
});

console.log('\n=== FixedWindow Tests ===\n');

test('FixedWindow: should initialize correctly', () => {
  const window = new FixedWindow({ maxRequests: 10, windowMs: 1000 });
  assert.strictEqual(window.maxRequests, 10);
  assert.strictEqual(window.getCount(), 0);
});

test('FixedWindow: should allow requests up to limit', () => {
  const window = new FixedWindow({ maxRequests: 3, windowMs: 1000 });
  assert.strictEqual(window.tryRequest(), true);
  assert.strictEqual(window.tryRequest(), true);
  assert.strictEqual(window.tryRequest(), true);
  assert.strictEqual(window.getCount(), 3);
});

test('FixedWindow: should reject over limit', () => {
  const window = new FixedWindow({ maxRequests: 2, windowMs: 1000 });
  window.tryRequest();
  window.tryRequest();
  assert.strictEqual(window.tryRequest(), false);
});

test('FixedWindow: should reset count in new window', async () => {
  const window = new FixedWindow({ maxRequests: 1, windowMs: 50 });
  assert.strictEqual(window.tryRequest(), true);
  assert.strictEqual(window.tryRequest(), false);
  
  await sleep(60);
  assert.strictEqual(window.tryRequest(), true);
});

test('FixedWindow: getRemaining should return correct count', () => {
  const window = new FixedWindow({ maxRequests: 5, windowMs: 1000 });
  assert.strictEqual(window.getRemaining(), 5);
  window.tryRequest();
  assert.strictEqual(window.getRemaining(), 4);
});

console.log('\n=== LeakyBucket Tests ===\n');

test('LeakyBucket: should initialize correctly', () => {
  const bucket = new LeakyBucket({ capacity: 10, leakRate: 1 });
  assert.strictEqual(bucket.capacity, 10);
  assert.strictEqual(bucket.getLevel(), 0);
});

test('LeakyBucket: should add requests', () => {
  const bucket = new LeakyBucket({ capacity: 5, leakRate: 1 });
  assert.strictEqual(bucket.tryAdd(), true);
  assert.strictEqual(bucket.tryAdd(), true);
  assert.strictEqual(bucket.getLevel(), 2);
});

test('LeakyBucket: should reject when full', () => {
  const bucket = new LeakyBucket({ capacity: 2, leakRate: 1 });
  bucket.tryAdd();
  bucket.tryAdd();
  assert.strictEqual(bucket.tryAdd(), false);
});

test('LeakyBucket: should leak over time', async () => {
  const bucket = new LeakyBucket({ capacity: 10, leakRate: 5 });
  bucket.tryAdd();
  bucket.tryAdd();
  bucket.tryAdd();
  assert.strictEqual(bucket.getLevel(), 3);
  
  await sleep(200); // 0.2s * 5 leaks/sec = 1 leak
  const level = bucket.getLevel();
  assert(level >= 1.8 && level <= 2.2, `Expected ~2 level, got ${level}`);
});

test('LeakyBucket: getRemaining should return correct value', () => {
  const bucket = new LeakyBucket({ capacity: 5, leakRate: 1 });
  assert.strictEqual(bucket.getRemaining(), 5);
  bucket.tryAdd();
  assert.strictEqual(bucket.getRemaining(), 4);
});

console.log('\n=== MultiKeyRateLimiter Tests ===\n');

test('MultiKeyRateLimiter: should track multiple keys independently', () => {
  const limiter = new MultiKeyRateLimiter({ maxRequests: 2, windowMs: 1000 });
  
  assert.strictEqual(limiter.tryRequest('user1'), true);
  assert.strictEqual(limiter.tryRequest('user1'), true);
  assert.strictEqual(limiter.tryRequest('user1'), false);
  
  assert.strictEqual(limiter.tryRequest('user2'), true);
  assert.strictEqual(limiter.tryRequest('user2'), true);
  assert.strictEqual(limiter.tryRequest('user2'), false);
});

test('MultiKeyRateLimiter: getRemaining should work per key', () => {
  const limiter = new MultiKeyRateLimiter({ maxRequests: 5, windowMs: 1000 });
  
  assert.strictEqual(limiter.getRemaining('user1'), 5);
  limiter.tryRequest('user1');
  assert.strictEqual(limiter.getRemaining('user1'), 4);
  assert.strictEqual(limiter.getRemaining('user2'), 5);
});

test('MultiKeyRateLimiter: resetKey should clear only that key', () => {
  const limiter = new MultiKeyRateLimiter({ maxRequests: 2, windowMs: 1000 });
  
  limiter.tryRequest('user1');
  limiter.tryRequest('user2');
  
  limiter.resetKey('user1');
  
  assert.strictEqual(limiter.getRemaining('user1'), 2);
  assert.strictEqual(limiter.getRemaining('user2'), 1);
});

test('MultiKeyRateLimiter: resetAll should clear all keys', () => {
  const limiter = new MultiKeyRateLimiter({ maxRequests: 2, windowMs: 1000 });
  
  limiter.tryRequest('user1');
  limiter.tryRequest('user2');
  
  limiter.resetAll();
  
  assert.strictEqual(limiter.getRemaining('user1'), 2);
  assert.strictEqual(limiter.getRemaining('user2'), 2);
});

// Async integration tests
console.log('\n=== Integration Tests ===\n');

(async () => {
  await asyncTest('TokenBucket: async consume should wait for tokens', async () => {
    const bucket = new TokenBucket({ capacity: 1, refillRate: 10 });
    bucket.tryConsume(1);
    
    const start = Date.now();
    await bucket.consume(1);
    const elapsed = Date.now() - start;
    
    assert(elapsed >= 80, `Expected wait time, got ${elapsed}ms`);
  });

  await asyncTest('SlidingWindow: async request should wait', async () => {
    const window = new SlidingWindow({ maxRequests: 1, windowMs: 50 });
    window.tryRequest();
    
    const start = Date.now();
    await window.request();
    const elapsed = Date.now() - start;
    
    assert(elapsed >= 40, `Expected wait time, got ${elapsed}ms`);
  });

  await asyncTest('LeakyBucket: async add should wait when full', async () => {
    const bucket = new LeakyBucket({ capacity: 1, leakRate: 1 });
    bucket.tryAdd();
    
    // The add will need to wait for the bucket to leak before it can add
    const start = Date.now();
    await bucket.add();
    const elapsed = Date.now() - start;
    
    // At leakRate=1, after ~50ms, level drops enough to allow add
    // Verify it actually waited (should be >= 40ms)
    assert(elapsed >= 40, `Expected wait time, got ${elapsed}ms`);
    
    // After add, bucket should have a request queued
    const level = bucket.getLevel();
    assert(level > 0, `Expected level > 0, got ${level}`);
  });

  // Summary
  console.log('\n=== Test Summary ===\n');
  console.log(`Passed: ${testsPassed}`);
  console.log(`Failed: ${testsFailed}`);
  console.log(`Total:  ${testsPassed + testsFailed}`);
  
  process.exit(testsFailed > 0 ? 1 : 0);
})();