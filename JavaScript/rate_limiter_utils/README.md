# Rate Limiter Utilities

Zero-dependency rate limiting implementations for Node.js and browsers. Supports multiple algorithms for different use cases.

## Installation

```bash
# No dependencies required - just copy the file
cp rate_limiter.js ./your-project/
```

## Features

- **Token Bucket** - Allows bursts, good for API rate limiting
- **Sliding Window** - Accurate, prevents boundary issues
- **Fixed Window** - Simple and memory-efficient
- **Leaky Bucket** - Smooths traffic, ideal for queues
- **Multi-Key Limiter** - Track rate limits per user/IP

## Quick Start

```javascript
const {
  TokenBucket,
  SlidingWindow,
  FixedWindow,
  LeakyBucket,
  MultiKeyRateLimiter,
  createMiddleware
} = require('./rate_limiter.js');
```

## Token Bucket

Best for: API rate limiting where bursts should be allowed.

```javascript
// 10 requests capacity, refills at 2 requests/second
const limiter = new TokenBucket({
  capacity: 10,
  refillRate: 2  // tokens per second
});

// Non-blocking check
if (limiter.tryConsume()) {
  // Request allowed
  makeApiCall();
} else {
  // Rate limited
  const waitTime = limiter.timeUntilAvailable();
  console.log(`Wait ${waitTime}ms`);
}

// Async version - waits if needed
await limiter.consume();  // Resolves when tokens available
```

## Sliding Window

Best for: User action limits (login attempts, form submissions).

```javascript
// Max 5 requests per 10 seconds
const limiter = new SlidingWindow({
  maxRequests: 5,
  windowMs: 10000
});

if (limiter.tryRequest()) {
  // Allowed
  console.log(`${limiter.getRemaining()} requests remaining`);
} else {
  // Blocked
  console.log(`Wait ${limiter.timeUntilAvailable()}ms`);
}
```

## Fixed Window

Best for: Daily/hourly limits where precision isn't critical.

```javascript
// 100 requests per hour
const limiter = new FixedWindow({
  maxRequests: 100,
  windowMs: 3600000  // 1 hour
});

if (limiter.tryRequest()) {
  console.log(`Remaining: ${limiter.getRemaining()}`);
}

// Time until window resets
const secondsLeft = Math.floor(limiter.timeUntilNextWindow() / 1000);
```

## Leaky Bucket

Best for: Smoothing traffic, processing queues at constant rate.

```javascript
// Process 10 requests/second, queue up to 5
const bucket = new LeakyBucket({
  capacity: 5,
  leakRate: 10  // requests per second
});

// Non-blocking
if (bucket.tryAdd()) {
  // Added to queue
  processRequest();
}

// Async - waits until space available
await bucket.add();
```

## Multi-Key Rate Limiter

Best for: Per-user or per-IP rate limiting.

```javascript
const limiter = new MultiKeyRateLimiter({
  maxRequests: 100,    // per key
  windowMs: 60000,     // 1 minute
  maxKeys: 10000        // max tracked keys
});

// Different limits per user
if (limiter.tryRequest('user:123')) {
  // User 123 can proceed
}

if (limiter.tryRequest('user:456')) {
  // User 456 can proceed (independent limit)
}

// Check remaining for a user
const remaining = limiter.getRemaining('user:123');

// Reset specific user
limiter.resetKey('user:123');

// Reset all
limiter.resetAll();
```

## Express/Connect Middleware

```javascript
const express = require('express');
const app = express();

// Rate limit all API routes
const apiLimiter = createMiddleware({
  maxRequests: 100,
  windowMs: 60000,  // 1 minute
  keyGenerator: (req) => req.user?.id || req.ip,
  onLimited: (req, res) => {
    res.status(429).json({
      error: 'Too many requests',
      message: 'Please try again later'
    });
  }
});

app.use('/api/', apiLimiter);

// Stricter limit for auth endpoints
const authLimiter = createMiddleware({
  maxRequests: 5,
  windowMs: 60000,  // 5 attempts per minute
  onLimited: (req, res) => {
    res.status(429).json({
      error: 'Too many attempts',
      retryAfter: 60
    });
  }
});

app.post('/login', authLimiter, handleLogin);
```

## Algorithm Comparison

| Algorithm | Burst | Accuracy | Memory | Use Case |
|-----------|-------|----------|--------|----------|
| Token Bucket | ✓ Yes | High | O(1) | APIs with burst allowance |
| Sliding Window | ✗ No | Highest | O(n) | Precise user limits |
| Fixed Window | ✗ No | Lower | O(1) | Daily/hourly quotas |
| Leaky Bucket | ✗ No | High | O(1) | Traffic smoothing |

## API Reference

### TokenBucket

```javascript
const bucket = new TokenBucket({
  capacity: number,      // Max tokens
  refillRate: number,    // Tokens per second
  initialTokens: number  // Optional starting tokens
});

bucket.tryConsume(tokens?)      // boolean
bucket.consume(tokens?)        // Promise<void>
bucket.timeUntilAvailable(tokens?)  // ms
bucket.getTokens()              // number
bucket.reset()                 // void
```

### SlidingWindow

```javascript
const window = new SlidingWindow({
  maxRequests: number,  // Max requests per window
  windowMs: number     // Window duration in ms
});

window.tryRequest()       // boolean
window.request()          // Promise<void>
window.timeUntilAvailable()  // ms
window.getCount()         // number
window.getRemaining()     // number
window.reset()            // void
```

### FixedWindow

```javascript
const window = new FixedWindow({
  maxRequests: number,
  windowMs: number
});

window.tryRequest()       // boolean
window.request()          // Promise<void>
window.timeUntilNextWindow()  // ms
window.getCount()         // number
window.getRemaining()     // number
window.reset()            // void
```

### LeakyBucket

```javascript
const bucket = new LeakyBucket({
  capacity: number,   // Max queue size
  leakRate: number    // Requests processed per second
});

bucket.tryAdd()        // boolean
bucket.add()           // Promise<void>
bucket.getLevel()      // number
bucket.getRemaining()  // number
bucket.reset()         // void
```

### MultiKeyRateLimiter

```javascript
const limiter = new MultiKeyRateLimiter({
  maxRequests: number,
  windowMs: number,
  maxKeys?: number     // Default: 10000
});

limiter.tryRequest(key)      // boolean
limiter.getRemaining(key)    // number
limiter.resetKey(key)        // void
limiter.resetAll()           // void
```

## Running Tests

```bash
node rate_limiter.test.js
```

## Running Examples

```bash
node examples.js
```

## License

MIT