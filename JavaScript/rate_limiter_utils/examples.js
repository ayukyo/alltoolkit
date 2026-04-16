/**
 * Rate Limiter Examples
 * Demonstrates various use cases for the rate limiter utilities
 */

const {
  TokenBucket,
  SlidingWindow,
  FixedWindow,
  LeakyBucket,
  MultiKeyRateLimiter,
  createMiddleware
} = require('./rate_limiter.js');

// ============================================
// Example 1: Token Bucket for API Rate Limiting
// ============================================

console.log('\n--- Example 1: Token Bucket for API Rate Limiting ---\n');

async function apiRateLimitExample() {
  // Allow 10 requests with bursts, refill at 2 requests/second
  const limiter = new TokenBucket({ 
    capacity: 10, 
    refillRate: 2 
  });

  console.log('Initial tokens:', limiter.getTokens());

  // Burst of 5 requests
  for (let i = 1; i <= 5; i++) {
    const allowed = limiter.tryConsume();
    console.log(`Request ${i}: ${allowed ? 'Allowed' : 'Denied'}`);
  }

  console.log('Remaining tokens:', limiter.getTokens());

  // Try to make more requests than available
  for (let i = 6; i <= 12; i++) {
    const allowed = limiter.tryConsume();
    console.log(`Request ${i}: ${allowed ? 'Allowed' : 'Denied'}`);
  }

  console.log('Final tokens:', limiter.getTokens());
}

apiRateLimitExample();

// ============================================
// Example 2: Sliding Window for User Actions
// ============================================

console.log('\n--- Example 2: Sliding Window for User Actions ---\n');

function slidingWindowExample() {
  // Limit to 5 actions per 10 seconds
  const limiter = new SlidingWindow({ 
    maxRequests: 5, 
    windowMs: 10000 
  });

  console.log('User action limiter (5 per 10 seconds)');

  for (let i = 1; i <= 7; i++) {
    const allowed = limiter.tryRequest();
    const remaining = limiter.getRemaining();
    console.log(`Action ${i}: ${allowed ? 'Allowed' : 'Blocked'} (${remaining} remaining)`);
  }
}

slidingWindowExample();

// ============================================
// Example 3: Fixed Window for Daily Limits
// ============================================

console.log('\n--- Example 3: Fixed Window for Daily Limits ---\n');

function fixedWindowExample() {
  // Limit to 100 requests per hour
  const limiter = new FixedWindow({ 
    maxRequests: 100, 
    windowMs: 3600000 // 1 hour
  });

  console.log('Hourly API limit (100 per hour)');

  // Simulate some usage
  for (let i = 0; i < 5; i++) {
    limiter.tryRequest();
  }

  console.log(`Current count: ${limiter.getCount()}`);
  console.log(`Remaining: ${limiter.getRemaining()}`);
  console.log(`Seconds until next window: ${Math.floor(limiter.timeUntilNextWindow() / 1000)}`);
}

fixedWindowExample();

// ============================================
// Example 4: Leaky Bucket for Smooth Traffic
// ============================================

console.log('\n--- Example 4: Leaky Bucket for Smooth Traffic ---\n');

function leakyBucketExample() {
  // Process at 10 requests/second, queue up to 5
  const bucket = new LeakyBucket({ 
    capacity: 5, 
    leakRate: 10 
  });

  console.log('API queue (processes 10/sec, max queue 5)');

  // Rapidly add requests
  for (let i = 1; i <= 7; i++) {
    const accepted = bucket.tryAdd();
    console.log(`Request ${i}: ${accepted ? 'Queued' : 'Rejected (queue full)'}`);
  }

  console.log(`Queue level: ${bucket.getLevel().toFixed(2)}`);
  console.log(`Queue remaining: ${bucket.getRemaining()}`);
}

leakyBucketExample();

// ============================================
// Example 5: Multi-Key for User Rate Limiting
// ============================================

console.log('\n--- Example 5: Multi-Key for User Rate Limiting ---\n');

function multiKeyExample() {
  // 10 requests per minute per user
  const limiter = new MultiKeyRateLimiter({ 
    maxRequests: 10, 
    windowMs: 60000,
    maxKeys: 1000
  });

  const users = ['alice', 'bob', 'charlie'];

  console.log('Per-user rate limiting (10/min)');

  users.forEach(user => {
    // Simulate different usage patterns
    const requests = Math.floor(Math.random() * 12) + 1;
    let allowed = 0;
    let blocked = 0;

    for (let i = 0; i < requests; i++) {
      if (limiter.tryRequest(user)) {
        allowed++;
      } else {
        blocked++;
      }
    }

    console.log(`${user}: ${allowed} allowed, ${blocked} blocked, ${limiter.getRemaining(user)} remaining`);
  });
}

multiKeyExample();

// ============================================
// Example 6: Express Middleware
// ============================================

console.log('\n--- Example 6: Express Middleware Setup ---\n');

function expressMiddlewareExample() {
  // Create middleware with custom key extractor
  const rateLimitMiddleware = createMiddleware({
    maxRequests: 100,
    windowMs: 60000, // 1 minute
    keyGenerator: (req) => req.user?.id || req.ip,
    onLimited: (req, res) => {
      res.status(429).json({
        error: 'Rate limit exceeded',
        retryAfter: 60
      });
    }
  });

  // Usage in Express:
  // app.use('/api/', rateLimitMiddleware);

  console.log('Middleware created successfully');
  console.log('Usage: app.use("/api/", rateLimitMiddleware)');
}

expressMiddlewareExample();

// ============================================
// Example 7: Async Waiting for Requests
// ============================================

console.log('\n--- Example 7: Async Waiting for Requests ---\n');

async function asyncWaitExample() {
  // Token bucket that allows bursting
  const limiter = new TokenBucket({ 
    capacity: 3, 
    refillRate: 1 
  });

  console.log('Making 5 requests with only 3 tokens...');

  for (let i = 1; i <= 5; i++) {
    const start = Date.now();
    await limiter.consume(1);
    const elapsed = Date.now() - start;
    console.log(`Request ${i}: Completed (waited ${elapsed}ms)`);
  }
}

asyncWaitExample().then(() => {
  console.log('\n=== All examples completed ===\n');
});