/**
 * Rate Limiter Utilities
 * Zero-dependency rate limiting implementations for Node.js and browsers
 * 
 * Supports:
 * - Token Bucket Algorithm
 * - Sliding Window Algorithm
 * - Fixed Window Algorithm
 * - Leaky Bucket Algorithm
 */

// ============================================
// Token Bucket Rate Limiter
// ============================================

/**
 * Token Bucket Rate Limiter
 * Allows bursts up to bucket capacity, then limits to refill rate
 */
class TokenBucket {
  /**
   * @param {Object} options
   * @param {number} options.capacity - Maximum tokens in bucket
   * @param {number} options.refillRate - Tokens added per second
   * @param {number} [options.initialTokens] - Starting tokens (default: capacity)
   */
  constructor({ capacity, refillRate, initialTokens }) {
    if (capacity <= 0) throw new Error('Capacity must be positive');
    if (refillRate <= 0) throw new Error('Refill rate must be positive');

    this.capacity = capacity;
    this.refillRate = refillRate;
    this.tokens = initialTokens !== undefined ? initialTokens : capacity;
    this.lastRefill = Date.now();
  }

  /**
   * Refill tokens based on elapsed time
   * @private
   */
  _refill() {
    const now = Date.now();
    const elapsed = (now - this.lastRefill) / 1000;
    const tokensToAdd = elapsed * this.refillRate;
    
    this.tokens = Math.min(this.capacity, this.tokens + tokensToAdd);
    this.lastRefill = now;
  }

  /**
   * Try to consume tokens
   * @param {number} [tokens=1] - Number of tokens to consume
   * @returns {boolean} True if tokens were consumed
   */
  tryConsume(tokens = 1) {
    this._refill();
    
    if (this.tokens >= tokens) {
      this.tokens -= tokens;
      return true;
    }
    return false;
  }

  /**
   * Consume tokens, waiting if necessary
   * @param {number} [tokens=1] - Number of tokens to consume
   * @returns {Promise<void>}
   */
  async consume(tokens = 1) {
    while (!this.tryConsume(tokens)) {
      const needed = tokens - this.tokens;
      const waitTime = (needed / this.refillRate) * 1000;
      await this._sleep(Math.min(waitTime, 100));
    }
  }

  /**
   * Get time until tokens are available
   * @param {number} [tokens=1] - Number of tokens needed
   * @returns {number} Milliseconds until available (0 if available now)
   */
  timeUntilAvailable(tokens = 1) {
    this._refill();
    if (this.tokens >= tokens) return 0;
    
    const needed = tokens - this.tokens;
    return Math.ceil((needed / this.refillRate) * 1000);
  }

  /**
   * Get current token count
   * @returns {number}
   */
  getTokens() {
    this._refill();
    return this.tokens;
  }

  /**
   * Reset bucket to full capacity
   */
  reset() {
    this.tokens = this.capacity;
    this.lastRefill = Date.now();
  }

  _sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
  }
}

// ============================================
// Sliding Window Rate Limiter
// ============================================

/**
 * Sliding Window Rate Limiter
 * More accurate than fixed window, prevents boundary issues
 */
class SlidingWindow {
  /**
   * @param {Object} options
   * @param {number} options.maxRequests - Maximum requests allowed
   * @param {number} options.windowMs - Window duration in milliseconds
   */
  constructor({ maxRequests, windowMs }) {
    if (maxRequests <= 0) throw new Error('Max requests must be positive');
    if (windowMs <= 0) throw new Error('Window duration must be positive');

    this.maxRequests = maxRequests;
    this.windowMs = windowMs;
    this.requests = [];
  }

  /**
   * Clean up old requests
   * @private
   */
  _cleanup() {
    const cutoff = Date.now() - this.windowMs;
    this.requests = this.requests.filter(t => t > cutoff);
  }

  /**
   * Check if request is allowed
   * @returns {boolean}
   */
  tryRequest() {
    this._cleanup();
    
    if (this.requests.length < this.maxRequests) {
      this.requests.push(Date.now());
      return true;
    }
    return false;
  }

  /**
   * Make a request, waiting if necessary
   * @returns {Promise<void>}
   */
  async request() {
    while (!this.tryRequest()) {
      const waitTime = this.timeUntilAvailable();
      await this._sleep(Math.min(waitTime, 100));
    }
  }

  /**
   * Get time until next request is allowed
   * @returns {number} Milliseconds
   */
  timeUntilAvailable() {
    this._cleanup();
    
    if (this.requests.length < this.maxRequests) return 0;
    
    // Time until oldest request exits the window
    return this.requests[0] + this.windowMs - Date.now() + 1;
  }

  /**
   * Get current request count in window
   * @returns {number}
   */
  getCount() {
    this._cleanup();
    return this.requests.length;
  }

  /**
   * Get remaining requests allowed
   * @returns {number}
   */
  getRemaining() {
    return Math.max(0, this.maxRequests - this.getCount());
  }

  /**
   * Reset the window
   */
  reset() {
    this.requests = [];
  }

  _sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
  }
}

// ============================================
// Fixed Window Rate Limiter
// ============================================

/**
 * Fixed Window Rate Limiter
 * Simple and memory-efficient, but can allow burst at window boundaries
 */
class FixedWindow {
  /**
   * @param {Object} options
   * @param {number} options.maxRequests - Maximum requests per window
   * @param {number} options.windowMs - Window duration in milliseconds
   */
  constructor({ maxRequests, windowMs }) {
    if (maxRequests <= 0) throw new Error('Max requests must be positive');
    if (windowMs <= 0) throw new Error('Window duration must be positive');

    this.maxRequests = maxRequests;
    this.windowMs = windowMs;
    this.count = 0;
    this.windowStart = this._currentWindow();
  }

  /**
   * Get current window start time
   * @private
   */
  _currentWindow() {
    return Math.floor(Date.now() / this.windowMs) * this.windowMs;
  }

  /**
   * Check and reset window if needed
   * @private
   */
  _checkWindow() {
    const currentWindow = this._currentWindow();
    if (currentWindow !== this.windowStart) {
      this.windowStart = currentWindow;
      this.count = 0;
    }
  }

  /**
   * Check if request is allowed
   * @returns {boolean}
   */
  tryRequest() {
    this._checkWindow();
    
    if (this.count < this.maxRequests) {
      this.count++;
      return true;
    }
    return false;
  }

  /**
   * Make a request, waiting if necessary
   * @returns {Promise<void>}
   */
  async request() {
    while (!this.tryRequest()) {
      const waitTime = this.timeUntilNextWindow();
      await this._sleep(Math.min(waitTime, 100));
    }
  }

  /**
   * Get time until next window starts
   * @returns {number} Milliseconds
   */
  timeUntilNextWindow() {
    this._checkWindow();
    return this.windowStart + this.windowMs - Date.now();
  }

  /**
   * Get current count in window
   * @returns {number}
   */
  getCount() {
    this._checkWindow();
    return this.count;
  }

  /**
   * Get remaining requests
   * @returns {number}
   */
  getRemaining() {
    return Math.max(0, this.maxRequests - this.getCount());
  }

  /**
   * Reset counter
   */
  reset() {
    this.count = 0;
    this.windowStart = this._currentWindow();
  }

  _sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
  }
}

// ============================================
// Leaky Bucket Rate Limiter
// ============================================

/**
 * Leaky Bucket Rate Limiter
 * Smooths out request rate, good for APIs
 */
class LeakyBucket {
  /**
   * @param {Object} options
   * @param {number} options.capacity - Maximum bucket size
   * @param {number} options.leakRate - Requests processed per second
   */
  constructor({ capacity, leakRate }) {
    if (capacity <= 0) throw new Error('Capacity must be positive');
    if (leakRate <= 0) throw new Error('Leak rate must be positive');

    this.capacity = capacity;
    this.leakRate = leakRate;
    this.level = 0;
    this.lastLeak = Date.now();
  }

  /**
   * Leak requests based on elapsed time
   * @private
   */
  _leak() {
    const now = Date.now();
    const elapsed = (now - this.lastLeak) / 1000;
    const leaked = elapsed * this.leakRate;
    
    this.level = Math.max(0, this.level - leaked);
    this.lastLeak = now;
  }

  /**
   * Try to add a request to the bucket
   * @returns {boolean} True if request was added
   */
  tryAdd() {
    this._leak();
    
    if (this.level < this.capacity) {
      this.level += 1;
      return true;
    }
    return false;
  }

  /**
   * Add a request, waiting if necessary
   * @returns {Promise<void>}
   */
  async add() {
    while (!this.tryAdd()) {
      await this._sleep(50);
    }
  }

  /**
   * Get current bucket level
   * @returns {number}
   */
  getLevel() {
    this._leak();
    return this.level;
  }

  /**
   * Get remaining capacity
   * @returns {number}
   */
  getRemaining() {
    return Math.max(0, this.capacity - this.getLevel());
  }

  /**
   * Reset bucket
   */
  reset() {
    this.level = 0;
    this.lastLeak = Date.now();
  }

  _sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
  }
}

// ============================================
// Distributed Rate Limiter (for multiple keys)
// ============================================

/**
 * Multi-key Rate Limiter
 * Uses fixed window algorithm for memory efficiency
 */
class MultiKeyRateLimiter {
  /**
   * @param {Object} options
   * @param {number} options.maxRequests - Maximum requests per key
   * @param {number} options.windowMs - Window duration in milliseconds
   * @param {number} [options.maxKeys=10000] - Maximum keys to track
   */
  constructor({ maxRequests, windowMs, maxKeys = 10000 }) {
    this.maxRequests = maxRequests;
    this.windowMs = windowMs;
    this.maxKeys = maxKeys;
    this.keys = new Map();
  }

  /**
   * Get or create a key entry
   * @private
   */
  _getKey(key) {
    let entry = this.keys.get(key);
    const windowStart = Math.floor(Date.now() / this.windowMs) * this.windowMs;
    
    if (!entry || entry.windowStart !== windowStart) {
      // Cleanup if at max keys
      if (this.keys.size >= this.maxKeys) {
        this._cleanup();
      }
      
      entry = { windowStart, count: 0 };
      this.keys.set(key, entry);
    }
    
    return entry;
  }

  /**
   * Remove old entries
   * @private
   */
  _cleanup() {
    const currentWindow = Math.floor(Date.now() / this.windowMs) * this.windowMs;
    for (const [key, entry] of this.keys) {
      if (entry.windowStart < currentWindow) {
        this.keys.delete(key);
      }
    }
  }

  /**
   * Check if request is allowed for a key
   * @param {string} key - Unique identifier (e.g., user ID, IP)
   * @returns {boolean}
   */
  tryRequest(key) {
    const entry = this._getKey(key);
    
    if (entry.count < this.maxRequests) {
      entry.count++;
      return true;
    }
    return false;
  }

  /**
   * Get remaining requests for a key
   * @param {string} key
   * @returns {number}
   */
  getRemaining(key) {
    const entry = this._getKey(key);
    return Math.max(0, this.maxRequests - entry.count);
  }

  /**
   * Reset a specific key
   * @param {string} key
   */
  resetKey(key) {
    this.keys.delete(key);
  }

  /**
   * Reset all keys
   */
  resetAll() {
    this.keys.clear();
  }
}

// ============================================
// Express/Connect Middleware Factory
// ============================================

/**
 * Create rate limiting middleware for Express/Connect
 * @param {Object} options
 * @param {number} options.maxRequests - Maximum requests per window
 * @param {number} options.windowMs - Window duration in milliseconds
 * @param {Function} [options.keyGenerator] - Function to extract key from request
 * @param {Function} [options.onLimited] - Handler when rate limited
 * @returns {Function} Middleware function
 */
function createMiddleware({
  maxRequests,
  windowMs,
  keyGenerator = (req) => req.ip || req.connection.remoteAddress,
  onLimited = (req, res) => {
    res.status(429).json({ error: 'Too many requests' });
  }
}) {
  const limiter = new MultiKeyRateLimiter({ maxRequests, windowMs });

  return (req, res, next) => {
    const key = keyGenerator(req);
    
    if (limiter.tryRequest(key)) {
      // Set rate limit headers
      res.setHeader('X-RateLimit-Limit', maxRequests);
      res.setHeader('X-RateLimit-Remaining', limiter.getRemaining(key));
      next();
    } else {
      res.setHeader('X-RateLimit-Limit', maxRequests);
      res.setHeader('X-RateLimit-Remaining', 0);
      res.setHeader('Retry-After', Math.ceil(windowMs / 1000));
      onLimited(req, res);
    }
  };
}

// ============================================
// Exports
// ============================================

module.exports = {
  TokenBucket,
  SlidingWindow,
  FixedWindow,
  LeakyBucket,
  MultiKeyRateLimiter,
  createMiddleware
};

// ES Module support
if (typeof module !== 'undefined' && module.exports) {
  module.exports.default = module.exports;
}