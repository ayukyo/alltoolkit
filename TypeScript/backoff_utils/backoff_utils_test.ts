/**
 * Backoff Utilities Test Suite
 * 
 * 全面测试各种退避策略
 * 
 * @author AllToolkit Generator
 * @date 2026-05-03
 */

import {
  ExponentialBackoff,
  LinearBackoff,
  ConstantBackoff,
  FullJitterBackoff,
  EqualJitterBackoff,
  DecorrelatedJitterBackoff,
  FibonacciBackoff,
  PolynomialBackoff,
  RetryExecutor,
  withRetry,
  createStrategy,
  calculateBackoffSequence,
  BackoffResult
} from './mod';

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

function describe(name: string, fn: () => void): void {
  console.log(`\n📋 ${name}`);
  console.log('─'.repeat(50));
  fn();
}

// ==================== Exponential Backoff Tests ====================

describe('ExponentialBackoff', () => {
  const backoff1 = new ExponentialBackoff({
    initialDelay: 100,
    maxDelay: 10000,
    maxRetries: 5
  });

  const delays1: number[] = [];
  for (let i = 0; i < 5; i++) {
    const result = backoff1.next();
    if (result.shouldRetry) delays1.push(result.delay);
  }

  assert(delays1.length === 5, 'Should have 5 retries');
  assertApprox(delays1[0], 100, 10, 'First delay ~100ms');
  assertApprox(delays1[1], 200, 10, 'Second delay ~200ms');
  assertApprox(delays1[2], 400, 10, 'Third delay ~400ms');
  assertApprox(delays1[3], 800, 10, 'Fourth delay ~800ms');
  assertApprox(delays1[4], 1600, 10, 'Fifth delay ~1600ms');

  // Test max delay cap
  const backoff2 = new ExponentialBackoff({
    initialDelay: 100,
    maxDelay: 500,
    maxRetries: 10
  });

  const delays2: number[] = [];
  for (let i = 0; i < 10; i++) {
    const result = backoff2.next();
    if (result.shouldRetry) delays2.push(result.delay);
  }

  const maxDelay = Math.max(...delays2);
  assert(maxDelay <= 500, `Max delay should be capped at 500ms (was ${maxDelay})`);

  // Test max retries limit
  const backoff3 = new ExponentialBackoff({
    initialDelay: 100,
    maxDelay: 10000,
    maxRetries: 3
  });

  let count = 0;
  while (backoff3.next().shouldRetry) {
    count++;
    if (count > 10) break; // Safety
  }

  assert(count === 3, `Should stop after 3 retries (got ${count})`);

  // Test reset
  const backoff4 = new ExponentialBackoff({
    initialDelay: 100,
    maxDelay: 10000,
    maxRetries: 5
  });

  backoff4.next();
  backoff4.next();
  backoff4.reset();

  assert(backoff4.getAttempt() === 0, 'Attempt should be 0 after reset');

  // Test custom multiplier
  const backoff5 = new ExponentialBackoff({
    initialDelay: 100,
    maxDelay: 10000,
    multiplier: 3
  });

  const delays5 = [backoff5.next().delay, backoff5.next().delay, backoff5.next().delay];
  
  assertApprox(delays5[0], 100, 10, 'First delay with multiplier 3');
  assertApprox(delays5[1], 300, 10, 'Second delay with multiplier 3');
  assertApprox(delays5[2], 900, 10, 'Third delay with multiplier 3');
});

// ==================== Linear Backoff Tests ====================

describe('LinearBackoff', () => {
  const backoff1 = new LinearBackoff({
    initialDelay: 100,
    maxDelay: 10000,
    increment: 50
  });

  const delays1 = [
    backoff1.next().delay,
    backoff1.next().delay,
    backoff1.next().delay,
    backoff1.next().delay
  ];

  assertApprox(delays1[0], 100, 10, 'First delay: 100');
  assertApprox(delays1[1], 150, 10, 'Second delay: 100 + 50');
  assertApprox(delays1[2], 200, 10, 'Third delay: 100 + 100');
  assertApprox(delays1[3], 250, 10, 'Fourth delay: 100 + 150');

  // Test default increment
  const backoff2 = new LinearBackoff({
    initialDelay: 200,
    maxDelay: 10000
  });

  const delays2 = [backoff2.next().delay, backoff2.next().delay, backoff2.next().delay];
  
  assertApprox(delays2[0], 200, 10, 'First delay');
  assertApprox(delays2[1], 400, 10, 'Second delay (increment defaults to initial)');
  assertApprox(delays2[2], 600, 10, 'Third delay');
});

// ==================== Constant Backoff Tests ====================

describe('ConstantBackoff', () => {
  const backoff = new ConstantBackoff({
    initialDelay: 500,
    maxDelay: 10000,
    maxRetries: 5
  });

  const delays: number[] = [];
  for (let i = 0; i < 5; i++) {
    delays.push(backoff.next().delay);
  }

  const allSame = delays.every(d => d === delays[0]);
  assert(allSame, 'All delays should be the same');
  assertApprox(delays[0], 500, 10, 'Delay should be 500ms');
});

// ==================== Full Jitter Backoff Tests ====================

describe('FullJitterBackoff', () => {
  const backoff1 = new FullJitterBackoff({
    initialDelay: 100,
    maxDelay: 10000,
    maxRetries: 10
  });

  for (let i = 0; i < 10; i++) {
    const result = backoff1.next();
    assert(result.delay >= 0, `Delay should be >= 0 (got ${result.delay})`);
    assert(result.delay <= 10000, `Delay should be <= maxDelay (got ${result.delay})`);
  }

  // Test randomness
  const delays1: number[] = [];
  const delays2: number[] = [];
  
  for (let i = 0; i < 5; i++) {
    const b1 = new FullJitterBackoff({ initialDelay: 100, maxDelay: 10000 });
    const b2 = new FullJitterBackoff({ initialDelay: 100, maxDelay: 10000 });
    delays1.push(b1.next().delay);
    delays2.push(b2.next().delay);
  }

  const someDifferent = delays1.some((d, i) => d !== delays2[i]);
  assert(someDifferent, 'Delays should vary due to randomness');
});

// ==================== Equal Jitter Backoff Tests ====================

describe('EqualJitterBackoff', () => {
  const backoff = new EqualJitterBackoff({
    initialDelay: 100,
    maxDelay: 10000
  });

  for (let i = 0; i < 5; i++) {
    const result = backoff.next();
    const base = Math.min(100 * Math.pow(2, i), 10000);
    assert(result.delay >= base / 2, `Delay should be >= half of base (${base})`);
  }
});

// ==================== Decorrelated Jitter Backoff Tests ====================

describe('DecorrelatedJitterBackoff', () => {
  const backoff1 = new DecorrelatedJitterBackoff({
    initialDelay: 100,
    maxDelay: 1000,
    maxRetries: 10
  });

  for (let i = 0; i < 10; i++) {
    const result = backoff1.next();
    assert(result.delay >= 0, `Delay should be >= 0 (got ${result.delay})`);
    assert(result.delay <= 1000, `Delay should be <= maxDelay (got ${result.delay})`);
  }

  // Test reset
  const backoff2 = new DecorrelatedJitterBackoff({
    initialDelay: 100,
    maxDelay: 10000
  });

  backoff2.next();
  backoff2.next();
  backoff2.reset();

  const result = backoff2.next();
  assertApprox(result.delay, 100, 300, 'First delay after reset should be around initialDelay');
});

// ==================== Fibonacci Backoff Tests ====================

describe('FibonacciBackoff', () => {
  const backoff = new FibonacciBackoff({
    initialDelay: 100,
    maxDelay: 10000,
    maxRetries: 7
  });

  const delays: number[] = [];
  for (let i = 0; i < 7; i++) {
    delays.push(backoff.next().delay);
  }

  // Fibonacci: 1, 1, 2, 3, 5, 8, 13
  assertApprox(delays[0], 100, 10, 'Fib(1) = 1 -> 100ms');
  assertApprox(delays[1], 100, 10, 'Fib(2) = 1 -> 100ms');
  assertApprox(delays[2], 200, 10, 'Fib(3) = 2 -> 200ms');
  assertApprox(delays[3], 300, 10, 'Fib(4) = 3 -> 300ms');
  assertApprox(delays[4], 500, 10, 'Fib(5) = 5 -> 500ms');
  assertApprox(delays[5], 800, 10, 'Fib(6) = 8 -> 800ms');
  assertApprox(delays[6], 1300, 10, 'Fib(7) = 13 -> 1300ms');

  // Test reset
  const backoff2 = new FibonacciBackoff({
    initialDelay: 100,
    maxDelay: 10000
  });

  backoff2.next();
  backoff2.next();
  backoff2.next();
  backoff2.reset();

  const result = backoff2.next();
  assertApprox(result.delay, 100, 10, 'After reset, should start from Fib(1)');
});

// ==================== Polynomial Backoff Tests ====================

describe('PolynomialBackoff', () => {
  const backoff1 = new PolynomialBackoff({
    initialDelay: 100,
    maxDelay: 10000,
    power: 2
  });

  const delays1 = [
    backoff1.next().delay,
    backoff1.next().delay,
    backoff1.next().delay,
    backoff1.next().delay
  ];

  assertApprox(delays1[0], 100, 10, '1^2 * 100 = 100');
  assertApprox(delays1[1], 400, 10, '2^2 * 100 = 400');
  assertApprox(delays1[2], 900, 10, '3^2 * 100 = 900');
  assertApprox(delays1[3], 1600, 10, '4^2 * 100 = 1600');

  // Test cubic
  const backoff2 = new PolynomialBackoff({
    initialDelay: 10,
    maxDelay: 10000,
    power: 3
  });

  const delays2 = [
    backoff2.next().delay,
    backoff2.next().delay,
    backoff2.next().delay
  ];

  assertApprox(delays2[0], 10, 5, '1^3 * 10 = 10');
  assertApprox(delays2[1], 80, 5, '2^3 * 10 = 80');
  assertApprox(delays2[2], 270, 5, '3^3 * 10 = 270');
});

// ==================== Jitter Tests ====================

describe('Jitter', () => {
  const delays: number[] = [];
  for (let i = 0; i < 10; i++) {
    const b = new ExponentialBackoff({
      initialDelay: 1000,
      maxDelay: 10000,
      jitter: true,
      jitterFactor: 0.5
    });
    delays.push(b.next().delay);
  }

  const uniqueDelays = new Set(delays);
  assert(uniqueDelays.size > 1, 'Jitter should create varying delays');

  // Test no jitter
  const backoff1 = new ExponentialBackoff({
    initialDelay: 100,
    maxDelay: 10000,
    jitter: false
  });

  const backoff2 = new ExponentialBackoff({
    initialDelay: 100,
    maxDelay: 10000,
    jitter: false
  });

  const delay1 = backoff1.next().delay;
  const delay2 = backoff2.next().delay;

  assert(delay1 === delay2, 'Without jitter, delays should be identical');
});

// ==================== Utility Functions Tests ====================

describe('Utility Functions', () => {
  const exponential = createStrategy({ initialDelay: 100, maxDelay: 1000, type: 'exponential' as any });
  const linear = createStrategy({ initialDelay: 100, maxDelay: 1000, type: 'linear' as any });
  const constant = createStrategy({ initialDelay: 100, maxDelay: 1000, type: 'constant' as any });

  assert(exponential instanceof ExponentialBackoff, 'Should create ExponentialBackoff');
  assert(linear instanceof LinearBackoff, 'Should create LinearBackoff');
  assert(constant instanceof ConstantBackoff, 'Should create ConstantBackoff');

  const seq = calculateBackoffSequence(
    { initialDelay: 100, maxDelay: 10000, type: 'exponential' as any, maxRetries: 5 },
    5
  );

  assert(seq.length === 5, `Should have 5 delays (got ${seq.length})`);
  assert(seq[0] < seq[4], 'Sequence should be increasing');
});

// ==================== Edge Cases ====================

describe('Edge Cases', () => {
  // Zero max retries
  const backoff1 = new ExponentialBackoff({
    initialDelay: 100,
    maxDelay: 1000,
    maxRetries: 0
  });

  const result1 = backoff1.next();
  assert(!result1.shouldRetry, 'Should not retry with maxRetries=0');
  assert(result1.maxRetriesReached, 'Should indicate max retries reached');

  // Very small delay
  const backoff2 = new ConstantBackoff({
    initialDelay: 1,
    maxDelay: 10
  });

  const result2 = backoff2.next();
  assert(result2.delay >= 0, 'Delay should be >= 0');
  assert(result2.delay <= 10, 'Delay should be <= maxDelay');

  // maxDelay smaller than initialDelay
  const backoff3 = new ExponentialBackoff({
    initialDelay: 1000,
    maxDelay: 100
  });

  const result3 = backoff3.next();
  assert(result3.delay <= 100, `Delay should be capped at maxDelay (was ${result3.delay})`);
});

// ==================== Async Tests ====================

async function runAsyncTests() {
  console.log(`\n📋 RetryExecutor Tests`);
  console.log('─'.repeat(50));

  // Test success on first try
  const strategy1 = new ExponentialBackoff({
    initialDelay: 10,
    maxDelay: 1000,
    maxRetries: 3
  });

  const executor1 = new RetryExecutor(strategy1);
  const result1 = await executor1.execute(async () => 'success');

  assert(result1.success, 'Should succeed');
  assert(result1.result === 'success', 'Should return result');
  assert(result1.attempts === 1, 'Should be 1 attempt');
  assert(result1.totalDelay === 0, 'Should have no delay');

  // Test success after retries
  const strategy2 = new ConstantBackoff({
    initialDelay: 10,
    maxDelay: 100,
    maxRetries: 5
  });

  let attempts2 = 0;
  const executor2 = new RetryExecutor(strategy2);
  const result2 = await executor2.execute(async () => {
    attempts2++;
    if (attempts2 < 3) throw new Error('Not yet');
    return 'done';
  });

  assert(result2.success, 'Should eventually succeed');
  assert(result2.attempts === 3, `Should be 3 attempts (was ${result2.attempts})`);
  assert(result2.result === 'done', 'Should return result');

  // Test max retries exceeded
  const strategy3 = new ConstantBackoff({
    initialDelay: 10,
    maxDelay: 100,
    maxRetries: 3
  });

  const executor3 = new RetryExecutor(strategy3);
  const result3 = await executor3.execute(async () => {
    throw new Error('Always fails');
  });

  assert(!result3.success, 'Should fail');
  assert(result3.error?.message === 'Always fails', 'Should have error');
  assert(result3.attempts === 4, `Should be 4 attempts (first + 3 retries) (was ${result3.attempts})`);

  // Test withRetry
  console.log(`\n📋 withRetry Tests`);
  console.log('─'.repeat(50));

  let attempts4 = 0;
  const fn = withRetry(
    async () => {
      attempts4++;
      if (attempts4 < 2) throw new Error('Fail');
      return 'success';
    },
    { initialDelay: 10, maxDelay: 100, maxRetries: 5 }
  );

  const result4 = await fn();
  assert(result4 === 'success', 'Should return success after retry');
  assert(attempts4 === 2, `Should have 2 attempts (was ${attempts4})`);
}

// ==================== Main ====================

async function main() {
  console.log('🚀 Starting Backoff Utils Tests\n');
  console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
  console.log('         SYNCHRONOUS TESTS');
  console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');

  // Async tests
  await runAsyncTests();

  // Summary
  console.log('\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
  console.log('         TEST SUMMARY');
  console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
  console.log(`✅ Passed: ${passedTests}`);
  console.log(`❌ Failed: ${failedTests}`);
  console.log(`📊 Total: ${passedTests + failedTests}`);
  
  if (failedTests === 0) {
    console.log('\n🎉 All tests passed!');
  } else {
    console.log(`\n⚠️ ${failedTests} test(s) failed!`);
    process.exit(1);
  }
}

main();