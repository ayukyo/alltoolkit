/**
 * Rate Limiter 测试文件
 * 
 * 运行方式：npx ts-node rate_limiter_test.ts
 * 或者编译后：node rate_limiter_test.js
 */

// @ts-nocheck
const {
  TokenBucket,
  LeakyBucket,
  FixedWindowCounter,
  SlidingWindowCounter,
  MultiRateLimiter,
  RateLimitError,
  rateLimit,
  wrapRateLimit,
  rateLimitedBatch
} = require('./mod.ts');

// 测试结果统计
let passed = 0;
let failed = 0;

function assert(condition, message) {
  if (condition) {
    passed++;
    console.log(`  ✓ ${message}`);
  } else {
    failed++;
    console.log(`  ✗ ${message}`);
  }
}

function assertThrows(fn, errorType, message) {
  try {
    fn();
    failed++;
    console.log(`  ✗ ${message} (expected to throw)`);
  } catch (e) {
    if (e instanceof errorType) {
      passed++;
      console.log(`  ✓ ${message}`);
    } else {
      failed++;
      console.log(`  ✗ ${message} (wrong error type)`);
    }
  }
}

// ==================== TokenBucket Tests ====================

console.log('\n=== TokenBucket Tests ===');

(function testTokenBucketBasicAcquire() {
  const bucket = new TokenBucket({ capacity: 5, refillRate: 1 });
  
  // 应该能连续获取5个令牌
  for (let i = 0; i < 5; i++) {
    const result = bucket.acquire();
    assert(result.allowed, `TokenBucket: 第${i + 1}次获取应该成功`);
  }
  
  // 第6次应该失败
  const result = bucket.acquire();
  assert(!result.allowed, 'TokenBucket: 超过容量应该失败');
  assert(result.retryAfter !== undefined, 'TokenBucket: 失败时应返回重试时间');
})();

(function testTokenBucketRemaining() {
  const bucket = new TokenBucket({ capacity: 10, refillRate: 1 });
  
  const result1 = bucket.acquire(3);
  assert(result1.remaining === 7, 'TokenBucket: 获取3个后剩余7个');
  
  const result2 = bucket.acquire(7);
  assert(result2.remaining === 0, 'TokenBucket: 获取剩余后应为0');
})();

(function testTokenBucketRefill() {
  const bucket = new TokenBucket({ capacity: 10, refillRate: 100 }); // 每秒100个令牌
  
  bucket.acquire(10); // 清空
  
  // 等待10ms，应该填充1个令牌
  // 这里只检查获取令牌后剩余数量正确
  setTimeout(() => {
    const result = bucket.acquire(1);
    assert(result.allowed, 'TokenBucket: 令牌应该被填充');
  }, 15);
})();

(function testTokenBucketReset() {
  const bucket = new TokenBucket({ capacity: 5, refillRate: 1 });
  
  bucket.acquire(5);
  bucket.reset();
  
  assert(bucket.getTokens() === 5, 'TokenBucket: 重置后令牌数应为容量');
})();

// ==================== LeakyBucket Tests ====================

console.log('\n=== LeakyBucket Tests ===');

(function testLeakyBucketBasicAcquire() {
  const bucket = new LeakyBucket({ capacity: 5, leakRate: 10 });
  
  // 应该能连续添加5个请求
  for (let i = 0; i < 5; i++) {
    const result = bucket.tryAcquire();
    assert(result.allowed, `LeakyBucket: 第${i + 1}次添加应该成功`);
  }
  
  // 第6次应该失败
  const result = bucket.tryAcquire();
  assert(!result.allowed, 'LeakyBucket: 超过容量应该失败');
})();

(function testLeakyBucketQueueSize() {
  const bucket = new LeakyBucket({ capacity: 3, leakRate: 100 });
  
  bucket.tryAcquire();
  bucket.tryAcquire();
  
  assert(bucket.getQueueSize() === 2, 'LeakyBucket: 队列大小应为2');
})();

(function testLeakyBucketReset() {
  const bucket = new LeakyBucket({ capacity: 5, leakRate: 10 });
  
  bucket.tryAcquire();
  bucket.tryAcquire();
  bucket.reset();
  
  assert(bucket.getQueueSize() === 0, 'LeakyBucket: 重置后队列应为空');
})();

// ==================== FixedWindowCounter Tests ====================

console.log('\n=== FixedWindowCounter Tests ===');

(function testFixedWindowBasicAcquire() {
  const counter = new FixedWindowCounter({ maxRequests: 5, windowMs: 1000 });
  
  for (let i = 0; i < 5; i++) {
    const result = counter.tryAcquire();
    assert(result.allowed, `FixedWindow: 第${i + 1}次请求应该成功`);
  }
  
  const result = counter.tryAcquire();
  assert(!result.allowed, 'FixedWindow: 超过限制应该失败');
  assert(result.remaining === 0, 'FixedWindow: 剩余应为0');
})();

(function testFixedWindowRemaining() {
  const counter = new FixedWindowCounter({ maxRequests: 10, windowMs: 1000 });
  
  counter.tryAcquire();
  counter.tryAcquire();
  counter.tryAcquire();
  
  const result = counter.tryAcquire();
  assert(result.remaining === 6, 'FixedWindow: 4次请求后剩余6');
})();

(function testFixedWindowReset() {
  const counter = new FixedWindowCounter({ maxRequests: 5, windowMs: 1000 });
  
  for (let i = 0; i < 5; i++) {
    counter.tryAcquire();
  }
  
  counter.reset();
  assert(counter.getCount() === 0, 'FixedWindow: 重置后计数应为0');
})();

// ==================== SlidingWindowCounter Tests ====================

console.log('\n=== SlidingWindowCounter Tests ===');

(function testSlidingWindowBasicAcquire() {
  const counter = new SlidingWindowCounter({ 
    maxRequests: 5, 
    windowMs: 1000,
    precision: 10
  });
  
  for (let i = 0; i < 5; i++) {
    const result = counter.tryAcquire();
    assert(result.allowed, `SlidingWindow: 第${i + 1}次请求应该成功`);
  }
  
  const result = counter.tryAcquire();
  assert(!result.allowed, 'SlidingWindow: 超过限制应该失败');
})();

(function testSlidingWindowCount() {
  const counter = new SlidingWindowCounter({ 
    maxRequests: 10, 
    windowMs: 1000 
  });
  
  counter.tryAcquire();
  counter.tryAcquire();
  counter.tryAcquire();
  
  assert(counter.getCount() === 3, 'SlidingWindow: 3次请求后计数应为3');
})();

(function testSlidingWindowReset() {
  const counter = new SlidingWindowCounter({ 
    maxRequests: 5, 
    windowMs: 1000 
  });
  
  for (let i = 0; i < 5; i++) {
    counter.tryAcquire();
  }
  
  counter.reset();
  assert(counter.getCount() === 0, 'SlidingWindow: 重置后计数应为0');
})();

// ==================== MultiRateLimiter Tests ====================

console.log('\n=== MultiRateLimiter Tests ===');

(function testMultiRateLimiterDifferentKeys() {
  const limiter = new MultiRateLimiter({ maxRequests: 2, windowMs: 1000 });
  
  // 用户A
  const resultA1 = limiter.tryAcquire('userA');
  const resultA2 = limiter.tryAcquire('userA');
  const resultA3 = limiter.tryAcquire('userA');
  
  assert(resultA1.allowed, 'MultiRateLimiter: userA第1次应成功');
  assert(resultA2.allowed, 'MultiRateLimiter: userA第2次应成功');
  assert(!resultA3.allowed, 'MultiRateLimiter: userA第3次应失败');
  
  // 用户B应该独立
  const resultB1 = limiter.tryAcquire('userB');
  assert(resultB1.allowed, 'MultiRateLimiter: userB应该独立计数');
})();

(function testMultiRateLimiterStatus() {
  const limiter = new MultiRateLimiter({ maxRequests: 5, windowMs: 1000 });
  
  limiter.tryAcquire('user1');
  limiter.tryAcquire('user1');
  limiter.tryAcquire('user1');
  
  const status = limiter.getStatus('user1');
  assert(status !== null, 'MultiRateLimiter: 应返回状态');
  assert(status?.count === 3, 'MultiRateLimiter: 计数应为3');
  assert(status?.remaining === 2, 'MultiRateLimiter: 剩余应为2');
})();

(function testMultiRateLimiterReset() {
  const limiter = new MultiRateLimiter({ maxRequests: 2, windowMs: 1000 });
  
  limiter.tryAcquire('userX');
  limiter.tryAcquire('userX');
  limiter.reset('userX');
  
  const result = limiter.tryAcquire('userX');
  assert(result.allowed, 'MultiRateLimiter: 重置后应该能重新请求');
})();

(function testMultiRateLimiterSize() {
  const limiter = new MultiRateLimiter({ maxRequests: 5, windowMs: 1000 });
  
  limiter.tryAcquire('user1');
  limiter.tryAcquire('user2');
  limiter.tryAcquire('user3');
  
  assert(limiter.size() === 3, 'MultiRateLimiter: 应有3个活跃键');
  
  limiter.resetAll();
  assert(limiter.size() === 0, 'MultiRateLimiter: 重置所有后应为0');
})();

// ==================== RateLimitError Tests ====================

console.log('\n=== RateLimitError Tests ===');

(function testRateLimitError() {
  const error = new RateLimitError('Test error', 1000);
  
  assert(error instanceof Error, 'RateLimitError: 应继承Error');
  assert(error.name === 'RateLimitError', 'RateLimitError: 名称应正确');
  assert(error.message === 'Test error', 'RateLimitError: 消息应正确');
  assert(error.retryAfter === 1000, 'RateLimitError: retryAfter应正确');
})();

// ==================== wrapRateLimit Tests ====================

console.log('\n=== wrapRateLimit Tests ===');

(async function testWrapRateLimit() {
  let callCount = 0;
  const originalFn = async (x) => {
    callCount++;
    return x * 2;
  };
  
  const limitedFn = wrapRateLimit(originalFn, { maxRequests: 3, windowMs: 1000 });
  
  const r1 = await limitedFn(1);
  const r2 = await limitedFn(2);
  const r3 = await limitedFn(3);
  
  assert(r1 === 2, 'wrapRateLimit: 第1次调用应正确');
  assert(r2 === 4, 'wrapRateLimit: 第2次调用应正确');
  assert(r3 === 6, 'wrapRateLimit: 第3次调用应正确');
  assert(callCount === 3, 'wrapRateLimit: 应调用3次');
})();

// ==================== rateLimitedBatch Tests ====================

console.log('\n=== rateLimitedBatch Tests ===');

(async function testRateLimitedBatch() {
  const items = [1, 2, 3, 4, 5];
  const processed = [];
  
  const results = await rateLimitedBatch(
    items,
    async (item) => {
      processed.push(item);
      return item * 10;
    },
    { maxRequests: 100, windowMs: 1000 } // 高限制，测试基本功能
  );
  
  assert(results.length === 5, 'rateLimitedBatch: 应返回5个结果');
  assert(results[0] === 10, 'rateLimitedBatch: 第1个结果应为10');
  assert(results[4] === 50, 'rateLimitedBatch: 第5个结果应为50');
})();

// ==================== Async Tests ====================

console.log('\n=== Async Tests ===');

(async function testTokenBucketAcquireAsync() {
  const bucket = new TokenBucket({ capacity: 1, refillRate: 10 });
  
  // 先消耗掉令牌
  bucket.acquire(1);
  
  // 异步等待
  const start = Date.now();
  const result = await bucket.acquireAsync(1, 200);
  const elapsed = Date.now() - start;
  
  assert(result.allowed, 'TokenBucket: 异步获取应该成功');
  assert(elapsed >= 50, `TokenBucket: 应等待约100ms，实际${elapsed}ms`);
})();

(async function testLeakyBucketAcquireAsync() {
  const bucket = new LeakyBucket({ capacity: 1, leakRate: 10 });
  
  // 先填满
  bucket.tryAcquire();
  
  // 第2次应该失败
  const result1 = bucket.tryAcquire();
  assert(!result1.allowed, 'LeakyBucket: 填满后应该拒绝');
  
  // 异步等待应该成功
  const result2 = await bucket.acquireAsync(200);
  assert(result2.allowed, 'LeakyBucket: 异步获取应该成功');
})();

// ==================== Edge Cases ====================

console.log('\n=== Edge Cases ===');

(function testTokenBucketZeroCapacity() {
  const bucket = new TokenBucket({ capacity: 0, refillRate: 1 });
  const result = bucket.acquire(1);
  assert(!result.allowed, 'Edge: 容量为0应该总是拒绝');
})();

(function testFixedWindowOneRequest() {
  const counter = new FixedWindowCounter({ maxRequests: 1, windowMs: 100 });
  
  const r1 = counter.tryAcquire();
  const r2 = counter.tryAcquire();
  
  assert(r1.allowed, 'Edge: 单请求限制第1次应成功');
  assert(!r2.allowed, 'Edge: 单请求限制第2次应失败');
})();

(function testSlidingWindowPrecision() {
  const counter = new SlidingWindowCounter({ 
    maxRequests: 10, 
    windowMs: 1000,
    precision: 100 // 高精度
  });
  
  for (let i = 0; i < 10; i++) {
    counter.tryAcquire();
  }
  
  assert(counter.getCount() === 10, 'Edge: 高精度计数应准确');
})();

// ==================== Summary ====================

setTimeout(() => {
  console.log('\n===========================================');
  console.log(`测试完成: ${passed} 通过, ${failed} 失败`);
  console.log('===========================================');
  
  if (failed > 0) {
    process.exit(1);
  }
}, 200);