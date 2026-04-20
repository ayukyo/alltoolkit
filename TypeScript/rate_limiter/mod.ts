/**
 * Rate Limiter Utilities for TypeScript
 * 
 * 零外部依赖的限流工具集，支持多种限流算法：
 * - 令牌桶算法 (Token Bucket)
 * - 漏桶算法 (Leaky Bucket)
 * - 滑动窗口计数器 (Sliding Window)
 * - 固定窗口计数器 (Fixed Window)
 * 
 * @author AllToolkit Generator
 * @date 2026-04-20
 */

// ==================== Types ====================

export interface RateLimiterConfig {
  /** 最大请求数 */
  maxRequests: number;
  /** 时间窗口（毫秒） */
  windowMs: number;
  /** 可选的等待超时（毫秒） */
  timeout?: number;
}

export interface TokenBucketConfig {
  /** 桶容量 */
  capacity: number;
  /** 令牌填充速率（每秒） */
  refillRate: number;
  /** 初始令牌数 */
  initialTokens?: number;
}

export interface LeakyBucketConfig {
  /** 桶容量 */
  capacity: number;
  /** 漏出速率（每秒） */
  leakRate: number;
}

export interface SlidingWindowConfig extends RateLimiterConfig {
  /** 精度（子窗口数） */
  precision?: number;
}

export interface RateLimitResult {
  /** 是否允许 */
  allowed: boolean;
  /** 剩余配额 */
  remaining: number;
  /** 重置时间（毫秒） */
  resetMs: number;
  /** 重试等待时间（毫秒） */
  retryAfter?: number;
}

export interface RequestRecord {
  timestamp: number;
  count: number;
}

// ==================== Token Bucket ====================

/**
 * 令牌桶限流器
 * 
 * 特点：允许突发流量，平滑限流
 */
export class TokenBucket {
  private tokens: number;
  private lastRefill: number;
  private readonly capacity: number;
  private readonly refillRate: number;

  constructor(config: TokenBucketConfig) {
    this.capacity = config.capacity;
    this.refillRate = config.refillRate;
    this.tokens = config.initialTokens ?? config.capacity;
    this.lastRefill = Date.now();
  }

  /**
   * 尝试消费令牌
   */
  acquire(tokens: number = 1): RateLimitResult {
    this.refill();
    
    if (this.tokens >= tokens) {
      this.tokens -= tokens;
      return {
        allowed: true,
        remaining: Math.floor(this.tokens),
        resetMs: Math.ceil((this.capacity - this.tokens) / this.refillRate * 1000)
      };
    }

    const needed = tokens - this.tokens;
    const waitTime = Math.ceil(needed / this.refillRate * 1000);

    return {
      allowed: false,
      remaining: 0,
      resetMs: waitTime,
      retryAfter: waitTime
    };
  }

  /**
   * 等待并消费令牌（异步）
   */
  async acquireAsync(tokens: number = 1, timeout?: number): Promise<RateLimitResult> {
    const result = this.acquire(tokens);
    
    if (result.allowed) {
      return result;
    }

    if (timeout !== undefined && result.retryAfter! > timeout) {
      return { ...result, allowed: false };
    }

    await this.sleep(result.retryAfter!);
    return this.acquire(tokens);
  }

  /**
   * 获取当前令牌数
   */
  getTokens(): number {
    this.refill();
    return this.tokens;
  }

  /**
   * 重置桶
   */
  reset(): void {
    this.tokens = this.capacity;
    this.lastRefill = Date.now();
  }

  private refill(): void {
    const now = Date.now();
    const elapsed = (now - this.lastRefill) / 1000;
    const refill = elapsed * this.refillRate;
    
    this.tokens = Math.min(this.capacity, this.tokens + refill);
    this.lastRefill = now;
  }

  private sleep(ms: number): Promise<void> {
    return new Promise(resolve => setTimeout(resolve, ms));
  }
}

// ==================== Leaky Bucket ====================

/**
 * 漏桶限流器
 * 
 * 特点：恒定速率输出，适合流量整形
 */
export class LeakyBucket {
  private queue: number = 0;
  private lastLeak: number;
  private readonly capacity: number;
  private readonly leakRate: number;

  constructor(config: LeakyBucketConfig) {
    this.capacity = config.capacity;
    this.leakRate = config.leakRate;
    this.lastLeak = Date.now();
  }

  /**
   * 尝试添加请求
   */
  tryAcquire(): RateLimitResult {
    this.leak();

    if (this.queue < this.capacity) {
      this.queue++;
      return {
        allowed: true,
        remaining: this.capacity - this.queue,
        resetMs: Math.ceil(this.queue / this.leakRate * 1000)
      };
    }

    return {
      allowed: false,
      remaining: 0,
      resetMs: Math.ceil(this.queue / this.leakRate * 1000),
      retryAfter: Math.ceil(1000 / this.leakRate)
    };
  }

  /**
   * 等待并添加请求（异步）
   */
  async acquireAsync(timeout?: number): Promise<RateLimitResult> {
    const result = this.tryAcquire();
    
    if (result.allowed) {
      return result;
    }

    if (timeout !== undefined && result.retryAfter! > timeout) {
      return { ...result, allowed: false };
    }

    await new Promise(resolve => setTimeout(resolve, result.retryAfter!));
    return this.tryAcquire();
  }

  /**
   * 获取当前队列大小
   */
  getQueueSize(): number {
    this.leak();
    return this.queue;
  }

  /**
   * 重置桶
   */
  reset(): void {
    this.queue = 0;
    this.lastLeak = Date.now();
  }

  private leak(): void {
    const now = Date.now();
    const elapsed = (now - this.lastLeak) / 1000;
    const leaked = elapsed * this.leakRate;
    
    this.queue = Math.max(0, this.queue - leaked);
    this.lastLeak = now;
  }
}

// ==================== Fixed Window Counter ====================

/**
 * 固定窗口计数器
 * 
 * 特点：简单高效，但可能在窗口边界出现突发
 */
export class FixedWindowCounter {
  private count: number = 0;
  private windowStart: number;
  private readonly maxRequests: number;
  private readonly windowMs: number;

  constructor(config: RateLimiterConfig) {
    this.maxRequests = config.maxRequests;
    this.windowMs = config.windowMs;
    this.windowStart = Date.now();
  }

  /**
   * 尝试通过
   */
  tryAcquire(): RateLimitResult {
    this.updateWindow();

    if (this.count < this.maxRequests) {
      this.count++;
      return {
        allowed: true,
        remaining: this.maxRequests - this.count,
        resetMs: this.windowMs - (Date.now() - this.windowStart)
      };
    }

    return {
      allowed: false,
      remaining: 0,
      resetMs: this.windowMs - (Date.now() - this.windowStart),
      retryAfter: this.windowMs - (Date.now() - this.windowStart)
    };
  }

  /**
   * 等待并通过（异步）
   */
  async acquireAsync(timeout?: number): Promise<RateLimitResult> {
    const result = this.tryAcquire();
    
    if (result.allowed) {
      return result;
    }

    if (timeout !== undefined && result.retryAfter! > timeout) {
      return { ...result, allowed: false };
    }

    await new Promise(resolve => setTimeout(resolve, result.retryAfter!));
    return this.tryAcquire();
  }

  /**
   * 获取当前计数
   */
  getCount(): number {
    this.updateWindow();
    return this.count;
  }

  /**
   * 重置计数器
   */
  reset(): void {
    this.count = 0;
    this.windowStart = Date.now();
  }

  private updateWindow(): void {
    const now = Date.now();
    if (now - this.windowStart >= this.windowMs) {
      this.windowStart = now;
      this.count = 0;
    }
  }
}

// ==================== Sliding Window Counter ====================

/**
 * 滑动窗口计数器
 * 
 * 特点：更精确的限流，避免窗口边界问题
 */
export class SlidingWindowCounter {
  private records: RequestRecord[] = [];
  private readonly maxRequests: number;
  private readonly windowMs: number;
  private readonly precision: number;

  constructor(config: SlidingWindowConfig) {
    this.maxRequests = config.maxRequests;
    this.windowMs = config.windowMs;
    this.precision = config.precision ?? 10;
  }

  /**
   * 尝试通过
   */
  tryAcquire(): RateLimitResult {
    this.cleanExpired();
    
    const currentCount = this.getCount();
    
    if (currentCount < this.maxRequests) {
      const now = Date.now();
      // 查找最近的记录并增加计数
      const lastRecord = this.records[this.records.length - 1];
      if (lastRecord && now - lastRecord.timestamp < this.windowMs / this.precision) {
        lastRecord.count++;
      } else {
        this.records.push({ timestamp: now, count: 1 });
      }
      
      return {
        allowed: true,
        remaining: this.maxRequests - currentCount - 1,
        resetMs: this.windowMs
      };
    }

    const oldestRecord = this.records[0];
    const resetMs = oldestRecord 
      ? this.windowMs - (Date.now() - oldestRecord.timestamp)
      : this.windowMs;

    return {
      allowed: false,
      remaining: 0,
      resetMs,
      retryAfter: resetMs
    };
  }

  /**
   * 等待并通过（异步）
   */
  async acquireAsync(timeout?: number): Promise<RateLimitResult> {
    const result = this.tryAcquire();
    
    if (result.allowed) {
      return result;
    }

    if (timeout !== undefined && result.retryAfter! > timeout) {
      return { ...result, allowed: false };
    }

    await new Promise(resolve => setTimeout(resolve, result.retryAfter!));
    return this.tryAcquire();
  }

  /**
   * 获取当前窗口内的请求数
   */
  getCount(): number {
    this.cleanExpired();
    return this.records.reduce((sum, r) => sum + r.count, 0);
  }

  /**
   * 重置计数器
   */
  reset(): void {
    this.records = [];
  }

  private cleanExpired(): void {
    const cutoff = Date.now() - this.windowMs;
    this.records = this.records.filter(r => r.timestamp > cutoff);
  }
}

// ==================== Multi-User Rate Limiter ====================

/**
 * 多用户限流器
 * 
 * 为不同用户/键分别维护限流状态
 */
export class MultiRateLimiter<T extends string = string> {
  private limiters: Map<T, FixedWindowCounter> = new Map();
  private readonly config: RateLimiterConfig;

  constructor(config: RateLimiterConfig) {
    this.config = config;
  }

  /**
   * 尝试为指定键通过
   */
  tryAcquire(key: T): RateLimitResult {
    let limiter = this.limiters.get(key);
    
    if (!limiter) {
      limiter = new FixedWindowCounter(this.config);
      this.limiters.set(key, limiter);
    }
    
    return limiter.tryAcquire();
  }

  /**
   * 等待并通过（异步）
   */
  async acquireAsync(key: T, timeout?: number): Promise<RateLimitResult> {
    let limiter = this.limiters.get(key);
    
    if (!limiter) {
      limiter = new FixedWindowCounter(this.config);
      this.limiters.set(key, limiter);
    }
    
    return limiter.acquireAsync(timeout);
  }

  /**
   * 获取指定键的状态
   */
  getStatus(key: T): { count: number; remaining: number } | null {
    const limiter = this.limiters.get(key);
    if (!limiter) return null;
    return {
      count: limiter.getCount(),
      remaining: this.config.maxRequests - limiter.getCount()
    };
  }

  /**
   * 重置指定键
   */
  reset(key: T): void {
    const limiter = this.limiters.get(key);
    if (limiter) {
      limiter.reset();
    }
  }

  /**
   * 重置所有限流器
   */
  resetAll(): void {
    this.limiters.clear();
  }

  /**
   * 获取当前活跃的键数量
   */
  size(): number {
    return this.limiters.size;
  }
}

// ==================== Decorator Factory ====================

/**
 * 创建限流装饰器（用于类方法）
 */
export function rateLimit(config: RateLimiterConfig) {
  const limiter = new FixedWindowCounter(config);
  
  return function (
    _target: unknown,
    _propertyKey: string,
    descriptor: PropertyDescriptor
  ): PropertyDescriptor {
    const originalMethod = descriptor.value;
    
    descriptor.value = async function (...args: unknown[]): Promise<unknown> {
      const result = limiter.tryAcquire();
      
      if (!result.allowed) {
        throw new RateLimitError(
          `Rate limit exceeded. Retry after ${result.retryAfter}ms`,
          result.retryAfter
        );
      }
      
      return originalMethod.apply(this, args);
    };
    
    return descriptor;
  };
}

/**
 * 限流错误类
 */
export class RateLimitError extends Error {
  public readonly retryAfter: number;

  constructor(message: string, retryAfter: number) {
    super(message);
    this.name = 'RateLimitError';
    this.retryAfter = retryAfter;
  }
}

// ==================== Utility Functions ====================

/**
 * 创建简单的限流函数包装器
 */
export function wrapRateLimit<T extends any[], R>(
  fn: (...args: T) => Promise<R>,
  config: RateLimiterConfig
): (...args: T) => Promise<R> {
  const limiter = new FixedWindowCounter(config);
  
  return async (...args: T): Promise<R> => {
    const result = limiter.tryAcquire();
    
    if (!result.allowed) {
      await new Promise(resolve => setTimeout(resolve, result.retryAfter));
      return wrapRateLimit(fn, config)(...args);
    }
    
    return fn(...args);
  };
}

/**
 * 批量执行带限流的任务
 */
export async function rateLimitedBatch<T, R>(
  items: T[],
  fn: (item: T) => Promise<R>,
  config: RateLimiterConfig
): Promise<R[]> {
  const limiter = new FixedWindowCounter(config);
  const results: R[] = [];

  for (const item of items) {
    const result = limiter.tryAcquire();
    
    if (!result.allowed) {
      await new Promise(resolve => setTimeout(resolve, result.retryAfter!));
    }
    
    results.push(await fn(item));
  }

  return results;
}

// ==================== Exports ====================

export default {
  TokenBucket,
  LeakyBucket,
  FixedWindowCounter,
  SlidingWindowCounter,
  MultiRateLimiter,
  RateLimitError,
  rateLimit,
  wrapRateLimit,
  rateLimitedBatch
};