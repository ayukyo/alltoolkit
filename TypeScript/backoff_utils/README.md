# Backoff Utils - TypeScript

零外部依赖的退避策略工具集，支持多种重试退避算法。

## 功能特性

- **指数退避 (Exponential Backoff)** - 延迟按指数增长，最常用的策略
- **线性退避 (Linear Backoff)** - 延迟线性增长，稳定可预测
- **恒定退避 (Constant Backoff)** - 固定延迟间隔
- **完全抖动 (Full Jitter)** - AWS 推荐，有效避免惊群效应
- **等抖动 (Equal Jitter)** - Google Cloud 推荐，平衡一致性和随机性
- **装饰抖动 (Decorrelated Jitter)** - 更不可预测，减少冲突
- **斐波那契退避 (Fibonacci Backoff)** - 比指数退避增长更平缓
- **多项式退避 (Polynomial Backoff)** - 可配置增长曲线

## 安装

```typescript
import {
  ExponentialBackoff,
  RetryExecutor,
  withRetry
} from './backoff_utils/mod';
```

## 快速使用

### 基础指数退避

```typescript
const backoff = new ExponentialBackoff({
  initialDelay: 100,    // 初始延迟 100ms
  maxDelay: 10000,      // 最大延迟 10s
  maxRetries: 5         // 最多重试 5 次
});

while (true) {
  const result = backoff.next();
  if (!result.shouldRetry) break;
  
  console.log(`等待 ${result.delay}ms 后重试...`);
  await sleep(result.delay);
  // 执行重试逻辑
}
```

### 使用 RetryExecutor

```typescript
const strategy = new ExponentialBackoff({
  initialDelay: 100,
  maxDelay: 5000,
  maxRetries: 5
});

const executor = new RetryExecutor(strategy);

const result = await executor.execute(async () => {
  return await fetch('https://api.example.com/data');
});

if (result.success) {
  console.log('成功:', result.result);
} else {
  console.log('失败:', result.error);
}
```

### 函数包装器

```typescript
const fetchWithRetry = withRetry(
  fetchData,
  { initialDelay: 100, maxDelay: 2000, maxRetries: 3 }
);

const data = await fetchWithRetry('https://api.example.com');
```

### 批量重试

```typescript
const results = await retryBatch(
  items,
  processItem,
  { initialDelay: 100, maxDelay: 2000, maxRetries: 3 }
);
```

## API 文档

### BackoffStrategy (基类)

所有退避策略继承自 `BackoffStrategy`，提供以下方法：

- `next(): BackoffResult` - 获取下次退避延迟
- `reset(): void` - 重置退避状态
- `getAttempt(): number` - 获取当前尝试次数
- `canRetry(): boolean` - 检查是否还能重试

### BackoffResult

```typescript
interface BackoffResult {
  shouldRetry: boolean;    // 是否应该重试
  delay: number;           // 下次重试延迟（毫秒）
  attempt: number;         // 当前重试次数
  maxRetriesReached: boolean;  // 是否已达最大重试次数
}
```

### ExponentialBackoff

```typescript
interface ExponentialBackoffConfig {
  initialDelay: number;    // 初始延迟（毫秒）
  maxDelay: number;        // 最大延迟（毫秒）
  maxRetries?: number;     // 最大重试次数
  multiplier?: number;     // 增长因子（默认2）
  jitter?: boolean;        // 是否添加抖动
  jitterFactor?: number;   // 抖动因子 (0-1)
}
```

### RetryExecutor

```typescript
interface RetryConfig extends BackoffConfig {
  shouldRetryOn?: (error: Error) => boolean;  // 重试条件
  timeout?: number;                          // 总超时时间
}
```

### 工具函数

- `withRetry(fn, config)` - 创建带重试的函数包装器
- `retryBatch(items, fn, config)` - 批量执行带重试
- `createStrategy(config)` - 工厂方法创建策略
- `calculateBackoffSequence(config, count)` - 预览退避序列

## 最佳实践

### API 请求重试

推荐使用 `FullJitterBackoff` 或 `DecorrelatedJitterBackoff`：

```typescript
const strategy = new FullJitterBackoff({
  initialDelay: 100,
  maxDelay: 30000,
  maxRetries: 10
});
```

### 数据库重连

推荐使用 `DecorrelatedJitterBackoff`：

```typescript
const strategy = new DecorrelatedJitterBackoff({
  initialDelay: 500,
  maxDelay: 30000,
  maxRetries: 20
});
```

### 限流场景

推荐使用 `ConstantBackoff` 或 `LinearBackoff`：

```typescript
const strategy = new ConstantBackoff({
  initialDelay: 1000,
  maxDelay: 60000,
  maxRetries: 60
});
```

## 作者

AllToolkit Generator

## 日期

2026-05-03