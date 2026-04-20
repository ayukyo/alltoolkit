/**
 * Rate Limiter 使用示例
 * 
 * 展示各种限流场景的实际应用
 */

import {
  TokenBucket,
  LeakyBucket,
  FixedWindowCounter,
  SlidingWindowCounter,
  MultiRateLimiter,
  wrapRateLimit,
  rateLimitedBatch
} from '../mod';

// ==================== 示例1: API 网关限流 ====================

console.log('=== 示例1: API 网关限流 ===\n');

async function apiGatewayExample() {
  // 使用令牌桶：允许突发，但总体速率受控
  const rateLimiter = new TokenBucket({
    capacity: 100,    // 允许100个请求的突发
    refillRate: 10    // 每秒补充10个令牌
  });

  console.log('模拟API网关：每秒10个请求，允许突发到100');

  // 模拟一批请求
  for (let i = 0; i < 15; i++) {
    const result = rateLimiter.acquire();
    const status = result.allowed ? '✓ 通过' : `✗ 拒绝 (等待${result.retryAfter}ms)`;
    console.log(`  请求 ${i + 1}: ${status}`);
  }
}

apiGatewayExample().then(() => {
  console.log('\n');

  // ==================== 示例2: 消息队列消费 ====================

  console.log('=== 示例2: 消息队列消费限流 ===\n');

  async function messageQueueExample() {
    // 使用漏桶：恒定消费速率
    const bucket = new LeakyBucket({
      capacity: 50,    // 最多缓存50条消息
      leakRate: 5       // 每秒处理5条
    });

    console.log('模拟消息队列：每秒处理5条消息，最多缓存50条');

    // 模拟消息到达
    const messages = ['msg1', 'msg2', 'msg3', 'msg4', 'msg5', 'msg6', 'msg7', 'msg8'];
    
    for (const msg of messages) {
      const result = bucket.tryAcquire();
      if (result.allowed) {
        console.log(`  ✓ ${msg} 已加入队列 (队列大小: ${bucket.getQueueSize()})`);
      } else {
        console.log(`  ✗ ${msg} 被拒绝，队列已满`);
      }
    }
  }

  return messageQueueExample();
}).then(() => {
  console.log('\n');

  // ==================== 示例3: 多用户API限流 ====================

  console.log('=== 示例3: 多用户独立限流 ===\n');

  async function multiUserExample() {
    // 每个用户独立限流
    const limiter = new MultiRateLimiter({
      maxRequests: 3,
      windowMs: 10000  // 10秒内最多3次
    });

    console.log('模拟多用户API：每用户10秒内最多3次请求');

    const users = ['alice', 'bob', 'alice', 'charlie', 'alice', 'bob'];

    for (const user of users) {
      const result = limiter.tryAcquire(user);
      const status = limiter.getStatus(user);
      const allowed = result.allowed ? '✓' : '✗';
      console.log(`  ${allowed} ${user.padEnd(8)} | 剩余: ${status?.remaining ?? 'N/A'}`);
    }

    console.log(`\n  活跃用户数: ${limiter.size()}`);
  }

  return multiUserExample();
}).then(() => {
  console.log('\n');

  // ==================== 示例4: 滑动窗口精确限流 ====================

  console.log('=== 示例4: 滑动窗口精确限流 ===\n');

  async function slidingWindowExample() {
    const limiter = new SlidingWindowCounter({
      maxRequests: 5,
      windowMs: 1000,
      precision: 10
    });

    console.log('滑动窗口：1秒内最多5次请求，精度10');

    // 快速发送10个请求
    for (let i = 0; i < 10; i++) {
      const result = limiter.tryAcquire();
      console.log(`  请求 ${i + 1}: ${result.allowed ? '✓ 通过' : '✗ 拒绝'} | 当前计数: ${limiter.getCount()}`);
    }
  }

  return slidingWindowExample();
}).then(() => {
  console.log('\n');

  // ==================== 示例5: 函数包装限流 ====================

  console.log('=== 示例5: 函数包装限流 ===\n');

  async function wrapFunctionExample() {
    // 模拟第三方API
    async function fetchUserData(userId: string): Promise<string> {
      // 模拟网络延迟
      await new Promise(r => setTimeout(r, 100));
      return `用户数据: ${userId}`;
    }

    // 包装为限流版本：每秒最多2次
    const limitedFetch = wrapRateLimit(fetchUserData, {
      maxRequests: 2,
      windowMs: 1000
    });

    console.log('模拟第三方API调用：每秒最多2次');

    const userIds = ['u1', 'u2', 'u3', 'u4'];
    
    const start = Date.now();
    for (const userId of userIds) {
      const data = await limitedFetch(userId);
      const elapsed = Date.now() - start;
      console.log(`  [${elapsed}ms] ${data}`);
    }
  }

  return wrapFunctionExample();
}).then(() => {
  console.log('\n');

  // ==================== 示例6: 批量任务限流 ====================

  console.log('=== 示例6: 批量任务限流 ===\n');

  async function batchExample() {
    // 模拟数据处理
    async function processItem(item: number): Promise<number> {
      await new Promise(r => setTimeout(r, 50));
      return item * 2;
    }

    const items = [1, 2, 3, 4, 5, 6, 7, 8];

    console.log('批量处理8个项目，每秒最多3个');

    const start = Date.now();
    const results = await rateLimitedBatch(
      items,
      processItem,
      { maxRequests: 3, windowMs: 1000 }
    );

    console.log('  结果:', results);
    console.log(`  总耗时: ${Date.now() - start}ms`);
  }

  return batchExample();
}).then(() => {
  console.log('\n');

  // ==================== 示例7: 异步等待限流 ====================

  console.log('=== 示例7: 异步等待限流 ===\n');

  async function asyncWaitExample() {
    const limiter = new FixedWindowCounter({
      maxRequests: 2,
      windowMs: 1000
    });

    console.log('固定窗口：每秒2次，演示异步等待');

    // 快速消耗配额
    limiter.tryAcquire();
    limiter.tryAcquire();
    console.log('  配额已用完');

    // 异步等待
    console.log('  开始异步等待...');
    const start = Date.now();
    const result = await limiter.acquireAsync(2000);
    const elapsed = Date.now() - start;

    console.log(`  等待 ${elapsed}ms 后，请求${result.allowed ? '成功' : '失败'}`);
  }

  return asyncWaitExample();
}).then(() => {
  console.log('\n');

  // ==================== 示例8: 实际应用 - 第三方API调用 ====================

  console.log('=== 示例8: 实际应用 - 第三方API调用 ===\n');

  async function realWorldExample() {
    // 模拟调用GitHub API（每分钟60次限制）
    const githubLimiter = new TokenBucket({
      capacity: 60,
      refillRate: 1   // 每秒1个令牌
    });

    async function callGitHubApi(endpoint: string): Promise<string> {
      const result = await githubLimiter.acquireAsync(1, 5000);
      
      if (!result.allowed) {
        throw new Error('API调用超时');
      }

      // 模拟API调用
      return `GitHub API响应: ${endpoint}`;
    }

    console.log('模拟GitHub API调用（每分钟60次限制）');

    const endpoints = ['/users', '/repos', '/issues', '/pulls', '/commits'];
    
    for (const endpoint of endpoints) {
      try {
        const response = await callGitHubApi(endpoint);
        console.log(`  ✓ ${endpoint} - ${response}`);
      } catch (e) {
        console.log(`  ✗ ${endpoint} - ${(e as Error).message}`);
      }
    }

    console.log(`  当前令牌数: ${githubLimiter.getTokens().toFixed(2)}`);
  }

  return realWorldExample();
}).then(() => {
  console.log('\n=== 所有示例完成 ===');
}).catch(console.error);