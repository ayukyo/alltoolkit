/**
 * Backoff Utilities for TypeScript
 * 
 * 零外部依赖的退避策略工具集，支持多种重试退避算法：
 * - 指数退避 (Exponential Backoff)
 * - 线性退避 (Linear Backoff)
 * - 恒定退避 (Constant Backoff)
 * - 装饰退避 (Decorrelated Jitter)
 * - 完全抖动 (Full Jitter)
 * - 等抖动 (Equal Jitter)
 * 
 * @author AllToolkit Generator
 * @date 2026-05-03
 */

// ==================== Types ====================

export interface BackoffConfig {
  /** 初始延迟（毫秒） */
  initialDelay: number;
  /** 最大延迟（毫秒） */
  maxDelay: number;
  /** 最大重试次数 */
  maxRetries?: number;
  /** 是否添加抖动 */
  jitter?: boolean;
  /** 抖动因子 (0-1) */
  jitterFactor?: number;
}

export interface BackoffResult {
  /** 是否应该重试 */
  shouldRetry: boolean;
  /** 下次重试延迟（毫秒） */
  delay: number;
  /** 当前重试次数 */
  attempt: number;
  /** 是否已达最大重试次数 */
  maxRetriesReached: boolean;
}

export interface RetryConfig extends BackoffConfig {
  /** 重试前的检查函数 */
  shouldRetryOn?: (error: Error) => boolean;
  /** 总超时时间（毫秒） */
  timeout?: number;
}

export interface RetryResult<T> {
  /** 结果 */
  result?: T;
  /** 错误 */
  error?: Error;
  /** 总重试次数 */
  attempts: number;
  /** 总延迟时间（毫秒） */
  totalDelay: number;
  /** 是否成功 */
  success: boolean;
}

// ==================== Base Backoff Class ====================

/**
 * 退避策略基类
 */
export abstract class BackoffStrategy {
  protected readonly initialDelay: number;
  protected readonly maxDelay: number;
  protected readonly maxRetries: number;
  protected readonly jitter: boolean;
  protected readonly jitterFactor: number;
  
  protected attempt: number = 0;

  constructor(config: BackoffConfig) {
    this.initialDelay = config.initialDelay;
    this.maxDelay = config.maxDelay;
    this.maxRetries = config.maxRetries ?? Infinity;
    this.jitter = config.jitter ?? false;
    this.jitterFactor = config.jitterFactor ?? 0.5;
  }

  /**
   * 获取下次退避延迟
   */
  abstract next(): BackoffResult;

  /**
   * 重置退避状态
   */
  reset(): void {
    this.attempt = 0;
  }

  /**
   * 获取当前尝试次数
   */
  getAttempt(): number {
    return this.attempt;
  }

  /**
   * 检查是否还能重试
   */
  canRetry(): boolean {
    return this.attempt < this.maxRetries;
  }

  /**
   * 应用抖动
   */
  protected applyJitter(delay: number): number {
    if (!this.jitter) return delay;
    
    const jitter = delay * this.jitterFactor;
    return delay - jitter + Math.random() * jitter * 2;
  }

  /**
   * 限制延迟在最大值范围内
   */
  protected clampDelay(delay: number): number {
    return Math.min(delay, this.maxDelay);
  }
}

// ==================== Exponential Backoff ====================

export interface ExponentialBackoffConfig extends BackoffConfig {
  /** 增长因子（默认2） */
  multiplier?: number;
  /** 随机化因子 (0-1) */
  randomizationFactor?: number;
}

/**
 * 指数退避策略
 * 
 * 延迟按指数增长: delay = initialDelay * multiplier^attempt
 * 最常用的退避策略，适合大多数分布式系统场景
 */
export class ExponentialBackoff extends BackoffStrategy {
  private readonly multiplier: number;
  private readonly randomizationFactor: number;

  constructor(config: ExponentialBackoffConfig) {
    super(config);
    this.multiplier = config.multiplier ?? 2;
    this.randomizationFactor = config.randomizationFactor ?? 0;
  }

  next(): BackoffResult {
    const canRetry = this.canRetry();
    this.attempt++;

    if (!canRetry) {
      return {
        shouldRetry: false,
        delay: 0,
        attempt: this.attempt,
        maxRetriesReached: true
      };
    }

    let delay = this.initialDelay * Math.pow(this.multiplier, this.attempt - 1);
    
    // 应用随机化因子
    if (this.randomizationFactor > 0) {
      const random = 1 - this.randomizationFactor + Math.random() * this.randomizationFactor * 2;
      delay *= random;
    }

    delay = this.clampDelay(delay);
    delay = this.applyJitter(delay);

    return {
      shouldRetry: true,
      delay: Math.floor(delay),
      attempt: this.attempt,
      maxRetriesReached: this.attempt >= this.maxRetries
    };
  }
}

// ==================== Linear Backoff ====================

export interface LinearBackoffConfig extends BackoffConfig {
  /** 每次增加的延迟（毫秒） */
  increment?: number;
}

/**
 * 线性退避策略
 * 
 * 延迟线性增长: delay = initialDelay + increment * attempt
 * 适合需要稳定可预测延迟增长的场景
 */
export class LinearBackoff extends BackoffStrategy {
  private readonly increment: number;

  constructor(config: LinearBackoffConfig) {
    super(config);
    this.increment = config.increment ?? config.initialDelay;
  }

  next(): BackoffResult {
    const canRetry = this.canRetry();
    this.attempt++;

    if (!canRetry) {
      return {
        shouldRetry: false,
        delay: 0,
        attempt: this.attempt,
        maxRetriesReached: true
      };
    }

    let delay = this.initialDelay + this.increment * (this.attempt - 1);
    delay = this.clampDelay(delay);
    delay = this.applyJitter(delay);

    return {
      shouldRetry: true,
      delay: Math.floor(delay),
      attempt: this.attempt,
      maxRetriesReached: this.attempt >= this.maxRetries
    };
  }
}

// ==================== Constant Backoff ====================

/**
 * 恒定退避策略
 * 
 * 每次延迟相同的时间
 * 适合简单的重试场景或已知的固定间隔轮询
 */
export class ConstantBackoff extends BackoffStrategy {
  next(): BackoffResult {
    const canRetry = this.canRetry();
    this.attempt++;

    if (!canRetry) {
      return {
        shouldRetry: false,
        delay: 0,
        attempt: this.attempt,
        maxRetriesReached: true
      };
    }

    let delay = this.clampDelay(this.initialDelay);
    delay = this.applyJitter(delay);

    return {
      shouldRetry: true,
      delay: Math.floor(delay),
      attempt: this.attempt,
      maxRetriesReached: this.attempt >= this.maxRetries
    };
  }
}

// ==================== Full Jitter Backoff ====================

/**
 * 完全抖动退避策略
 * 
 * Amazon AWS 推荐的策略
 * delay = random(0, min(cap, base * 2^attempt))
 * 有效避免"惊群效应"，适合高并发分布式系统
 */
export class FullJitterBackoff extends BackoffStrategy {
  next(): BackoffResult {
    const canRetry = this.canRetry();
    this.attempt++;

    if (!canRetry) {
      return {
        shouldRetry: false,
        delay: 0,
        attempt: this.attempt,
        maxRetriesReached: true
      };
    }

    const exponentialDelay = this.initialDelay * Math.pow(2, this.attempt - 1);
    const cappedDelay = this.clampDelay(exponentialDelay);
    
    // 完全随机：[0, cappedDelay]
    const delay = Math.random() * cappedDelay;

    return {
      shouldRetry: true,
      delay: Math.floor(delay),
      attempt: this.attempt,
      maxRetriesReached: this.attempt >= this.maxRetries
    };
  }
}

// ==================== Equal Jitter Backoff ====================

/**
 * 等抖动退避策略
 * 
 * Google Cloud 推荐的策略
 * delay = min(cap, base * 2^attempt) / 2 + random(0, min(cap, base * 2^attempt) / 2)
 * 平衡了延迟的一致性和随机性
 */
export class EqualJitterBackoff extends BackoffStrategy {
  next(): BackoffResult {
    const canRetry = this.canRetry();
    this.attempt++;

    if (!canRetry) {
      return {
        shouldRetry: false,
        delay: 0,
        attempt: this.attempt,
        maxRetriesReached: true
      };
    }

    const exponentialDelay = this.initialDelay * Math.pow(2, this.attempt - 1);
    const cappedDelay = this.clampDelay(exponentialDelay);
    
    // 一半固定 + 一半随机
    const half = cappedDelay / 2;
    const delay = half + Math.random() * half;

    return {
      shouldRetry: true,
      delay: Math.floor(delay),
      attempt: this.attempt,
      maxRetriesReached: this.attempt >= this.maxRetries
    };
  }
}

// ==================== Decorrelated Jitter Backoff ====================

/**
 * 装饰抖动退避策略
 * 
 * delay = min(cap, random(base, delay * 3))
 * 比指数退避更不可预测，进一步减少冲突
 */
export class DecorrelatedJitterBackoff extends BackoffStrategy {
  private lastDelay: number;

  constructor(config: BackoffConfig) {
    super(config);
    this.lastDelay = config.initialDelay;
  }

  next(): BackoffResult {
    const canRetry = this.canRetry();
    this.attempt++;

    if (!canRetry) {
      return {
        shouldRetry: false,
        delay: 0,
        attempt: this.attempt,
        maxRetriesReached: true
      };
    }

    // delay = min(cap, random(base, lastDelay * 3))
    const upper = this.lastDelay * 3;
    const randomDelay = this.initialDelay + Math.random() * (upper - this.initialDelay);
    const delay = this.clampDelay(randomDelay);
    
    this.lastDelay = delay;

    return {
      shouldRetry: true,
      delay: Math.floor(delay),
      attempt: this.attempt,
      maxRetriesReached: this.attempt >= this.maxRetries
    };
  }

  reset(): void {
    super.reset();
    this.lastDelay = this.initialDelay;
  }
}

// ==================== Fibonacci Backoff ====================

/**
 * 斐波那契退避策略
 * 
 * 延迟按斐波那契数列增长
 * 比指数退避增长更平缓，适合不需要太激进退避的场景
 */
export class FibonacciBackoff extends BackoffStrategy {
  private fibIndex: number = 1;

  next(): BackoffResult {
    const canRetry = this.canRetry();
    this.attempt++;

    if (!canRetry) {
      return {
        shouldRetry: false,
        delay: 0,
        attempt: this.attempt,
        maxRetriesReached: true
      };
    }

    // 计算当前斐波那契数
    const fibNum = this.fibonacci(this.fibIndex);
    this.fibIndex++;

    let delay = this.initialDelay * fibNum;
    delay = this.clampDelay(delay);
    delay = this.applyJitter(delay);

    return {
      shouldRetry: true,
      delay: Math.floor(delay),
      attempt: this.attempt,
      maxRetriesReached: this.attempt >= this.maxRetries
    };
  }

  reset(): void {
    super.reset();
    this.fibIndex = 1;
  }

  /**
   * 计算斐波那契数
   */
  private fibonacci(n: number): number {
    if (n <= 2) return 1;
    let a = 1, b = 1;
    for (let i = 3; i <= n; i++) {
      const temp = a + b;
      a = b;
      b = temp;
    }
    return b;
  }
}

// ==================== Polynomial Backoff ====================

export interface PolynomialBackoffConfig extends BackoffConfig {
  /** 多项式指数（默认2） */
  power?: number;
}

/**
 * 多项式退避策略
 * 
 * delay = initialDelay * attempt^power
 * 可配置增长曲线的陡峭程度
 */
export class PolynomialBackoff extends BackoffStrategy {
  private readonly power: number;

  constructor(config: PolynomialBackoffConfig) {
    super(config);
    this.power = config.power ?? 2;
  }

  next(): BackoffResult {
    const canRetry = this.canRetry();
    this.attempt++;

    if (!canRetry) {
      return {
        shouldRetry: false,
        delay: 0,
        attempt: this.attempt,
        maxRetriesReached: true
      };
    }

    let delay = this.initialDelay * Math.pow(this.attempt, this.power);
    delay = this.clampDelay(delay);
    delay = this.applyJitter(delay);

    return {
      shouldRetry: true,
      delay: Math.floor(delay),
      attempt: this.attempt,
      maxRetriesReached: this.attempt >= this.maxRetries
    };
  }
}

// ==================== Retry Executor ====================

/**
 * 退避重试执行器
 */
export class RetryExecutor<T = unknown> {
  private strategy: BackoffStrategy;
  private shouldRetryOn: (error: Error) => boolean;
  private timeout: number | undefined;
  private startTime: number = 0;

  constructor(
    strategy: BackoffStrategy,
    config?: Partial<RetryConfig>
  ) {
    this.strategy = strategy;
    this.shouldRetryOn = config?.shouldRetryOn ?? (() => true);
    this.timeout = config?.timeout;
  }

  /**
   * 执行带重试的异步函数
   */
  async execute(fn: () => Promise<T>): Promise<RetryResult<T>> {
    this.startTime = Date.now();
    let totalDelay = 0;

    while (true) {
      try {
        const result = await fn();
        return {
          result,
          attempts: this.strategy.getAttempt() + 1,
          totalDelay,
          success: true
        };
      } catch (error) {
        const err = error as Error;
        const backoff = this.strategy.next();

        // 检查是否应该重试
        if (!backoff.shouldRetry || 
            !this.shouldRetryOn(err) ||
            (this.timeout && Date.now() - this.startTime + backoff.delay > this.timeout)) {
          return {
            error: err,
            attempts: this.strategy.getAttempt(),
            totalDelay,
            success: false
          };
        }

        // 等待退避时间
        await this.sleep(backoff.delay);
        totalDelay += backoff.delay;
      }
    }
  }

  private sleep(ms: number): Promise<void> {
    return new Promise(resolve => setTimeout(resolve, ms));
  }
}

// ==================== Utility Functions ====================

/**
 * 创建带重试的函数包装器
 */
export function withRetry<T extends any[], R>(
  fn: (...args: T) => Promise<R>,
  config: RetryConfig
): (...args: T) => Promise<R> {
  const strategy = createStrategy(config);
  const executor = new RetryExecutor<R>(strategy, config);

  return async (...args: T): Promise<R> => {
    const result = await executor.execute(() => fn(...args));
    if (result.success) {
      return result.result!;
    }
    throw result.error;
  };
}

/**
 * 批量执行带重试的任务
 */
export async function retryBatch<T, R>(
  items: T[],
  fn: (item: T) => Promise<R>,
  config: RetryConfig
): Promise<Array<RetryResult<R>>> {
  return Promise.all(items.map(async (item) => {
    const strategy = createStrategy(config);
    const executor = new RetryExecutor<R>(strategy, config);
    return executor.execute(() => fn(item));
  }));
}

/**
 * 创建退避策略实例
 */
export function createStrategy(config: BackoffConfig & { type?: BackoffType }): BackoffStrategy {
  const type = (config as any).type ?? 'exponential';
  
  switch (type) {
    case 'linear':
      return new LinearBackoff(config);
    case 'constant':
      return new ConstantBackoff(config);
    case 'fullJitter':
      return new FullJitterBackoff(config);
    case 'equalJitter':
      return new EqualJitterBackoff(config);
    case 'decorrelatedJitter':
      return new DecorrelatedJitterBackoff(config);
    case 'fibonacci':
      return new FibonacciBackoff(config);
    case 'polynomial':
      return new PolynomialBackoff(config);
    default:
      return new ExponentialBackoff(config);
  }
}

/**
 * 计算退避延迟序列（用于预览）
 */
export function calculateBackoffSequence(
  config: BackoffConfig & { type?: BackoffType },
  count: number
): number[] {
  const strategy = createStrategy({ ...config, type: (config as any).type, maxRetries: count });
  const delays: number[] = [];

  for (let i = 0; i < count; i++) {
    const result = strategy.next();
    if (!result.shouldRetry) break;
    delays.push(result.delay);
  }

  return delays;
}

/**
 * 等待指定退避时间
 */
export async function backoffWait(
  strategy: BackoffStrategy
): Promise<BackoffResult> {
  const result = strategy.next();
  if (result.shouldRetry && result.delay > 0) {
    await new Promise(resolve => setTimeout(resolve, result.delay));
  }
  return result;
}

// ==================== Backoff Type ====================

export type BackoffType = 
  | 'exponential'
  | 'linear'
  | 'constant'
  | 'fullJitter'
  | 'equalJitter'
  | 'decorrelatedJitter'
  | 'fibonacci'
  | 'polynomial';

// ==================== Exports ====================

export default {
  // Strategy Classes
  BackoffStrategy,
  ExponentialBackoff,
  LinearBackoff,
  ConstantBackoff,
  FullJitterBackoff,
  EqualJitterBackoff,
  DecorrelatedJitterBackoff,
  FibonacciBackoff,
  PolynomialBackoff,
  
  // Executor
  RetryExecutor,
  
  // Utility Functions
  withRetry,
  retryBatch,
  createStrategy,
  calculateBackoffSequence,
  backoffWait
};