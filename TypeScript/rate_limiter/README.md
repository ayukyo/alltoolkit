# Rate Limiter 工具模块

零外部依赖的 TypeScript 限流工具集，支持多种限流算法。

## 安装

```bash
# 复制 mod.ts 到你的项目中
# 或者直接导入使用
```

## 功能特性

- ✅ **令牌桶算法 (Token Bucket)** - 允许突发流量，平滑限流
- ✅ **漏桶算法 (Leaky Bucket)** - 恒定速率输出，适合流量整形
- ✅ **固定窗口计数器 (Fixed Window)** - 简单高效
- ✅ **滑动窗口计数器 (Sliding Window)** - 更精确的限流
- ✅ **多用户限流器** - 为不同用户独立限流
- ✅ **装饰器支持** - 轻松为方法添加限流
- ✅ **异步等待** - 自动等待并重试

## 快速开始

### 令牌桶 (Token Bucket)

适合需要允许一定突发流量的场景，如 API 网关。

```typescript
import { TokenBucket } from './mod';

// 创建桶：容量10，每秒填充5个令牌
const bucket = new TokenBucket({
  capacity: 10,
  refillRate: 5
});

// 尝试获取1个令牌
const result = bucket.acquire(1);

if (result.allowed) {
  console.log(`请求通过，剩余配额: ${result.remaining}`);
} else {
  console.log(`被限流，${result.retryAfter}ms后重试`);
}

// 异步等待
const asyncResult = await bucket.acquireAsync(1);
```

### 漏桶 (Leaky Bucket)

适合需要恒定输出的场景，如消息队列消费。

```typescript
import { LeakyBucket } from './mod';

// 创建桶：容量100，每秒漏出10个请求
const bucket = new LeakyBucket({
  capacity: 100,
  leakRate: 10
});

if (bucket.tryAcquire().allowed) {
  // 处理请求
}

// 异步等待
await bucket.acquireAsync();
```

### 固定窗口 (Fixed Window)

最简单的限流方式，适合基础限流需求。

```typescript
import { FixedWindowCounter } from './mod';

// 限制：每秒最多10个请求
const limiter = new FixedWindowCounter({
  maxRequests: 10,
  windowMs: 1000
});

for (let i = 0; i < 15; i++) {
  const result = limiter.tryAcquire();
  console.log(`请求${i + 1}: ${result.allowed ? '通过' : '被拒绝'}`);
}
```

### 滑动窗口 (Sliding Window)

更精确的限流，避免窗口边界问题。

```typescript
import { SlidingWindowCounter } from './mod';

const limiter = new SlidingWindowCounter({
  maxRequests: 100,
  windowMs: 60000, // 1分钟
  precision: 10    // 10个子窗口
});
```

### 多用户限流

为不同用户/API Key分别限流。

```typescript
import { MultiRateLimiter } from './mod';

// 每个用户每分钟100次请求
const limiter = new MultiRateLimiter({
  maxRequests: 100,
  windowMs: 60000
});

// 用户A
limiter.tryAcquire('user-a');

// 用户B（独立计数）
limiter.tryAcquire('user-b');

// 获取状态
const status = limiter.getStatus('user-a');
console.log(`已用: ${status?.count}, 剩余: ${status?.remaining}`);
```

### 装饰器模式

为类方法添加限流。

```typescript
import { rateLimit, RateLimitError } from './mod';

class ApiService {
  @rateLimit({ maxRequests: 10, windowMs: 1000 })
  async fetchData(url: string): Promise<string> {
    const response = await fetch(url);
    return response.text();
  }
}

const api = new ApiService();
try {
  const data = await api.fetchData('https://api.example.com');
} catch (e) {
  if (e instanceof RateLimitError) {
    console.log(`被限流，${e.retryAfter}ms后重试`);
  }
}
```

### 函数包装器

包装现有函数添加限流。

```typescript
import { wrapRateLimit } from './mod';

async function callApi(id: number): Promise<string> {
  // ... API调用
  return `result-${id}`;
}

// 创建限流版本
const limitedCallApi = wrapRateLimit(callApi, {
  maxRequests: 5,
  windowMs: 1000
});

// 会自动等待并重试
const result = await limitedCallApi(1);
```

### 批量执行

对批量任务进行限流。

```typescript
import { rateLimitedBatch } from './mod';

const items = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10];

const results = await rateLimitedBatch(
  items,
  async (item) => {
    // 处理每个item
    return processItem(item);
  },
  { maxRequests: 3, windowMs: 1000 } // 每秒3个
);
```

## API 参考

### TokenBucket

| 方法 | 参数 | 返回值 | 说明 |
|------|------|--------|------|
| `constructor(config)` | capacity, refillRate, initialTokens? | - | 创建令牌桶 |
| `acquire(tokens?)` | tokens?: number | RateLimitResult | 同步获取令牌 |
| `acquireAsync(tokens?, timeout?)` | tokens?: number, timeout?: number | Promise\<RateLimitResult\> | 异步等待获取 |
| `getTokens()` | - | number | 获取当前令牌数 |
| `reset()` | - | void | 重置桶 |

### LeakyBucket

| 方法 | 参数 | 返回值 | 说明 |
|------|------|--------|------|
| `constructor(config)` | capacity, leakRate | - | 创建漏桶 |
| `tryAcquire()` | - | RateLimitResult | 尝试添加请求 |
| `acquireAsync(timeout?)` | timeout?: number | Promise\<RateLimitResult\> | 异步等待添加 |
| `getQueueSize()` | - | number | 获取当前队列大小 |
| `reset()` | - | void | 重置桶 |

### FixedWindowCounter

| 方法 | 参数 | 返回值 | 说明 |
|------|------|--------|------|
| `constructor(config)` | maxRequests, windowMs | - | 创建计数器 |
| `tryAcquire()` | - | RateLimitResult | 尝试通过 |
| `acquireAsync(timeout?)` | timeout?: number | Promise\<RateLimitResult\> | 异步等待通过 |
| `getCount()` | - | number | 获取当前计数 |
| `reset()` | - | void | 重置计数器 |

### SlidingWindowCounter

| 方法 | 参数 | 返回值 | 说明 |
|------|------|--------|------|
| `constructor(config)` | maxRequests, windowMs, precision? | - | 创建滑动窗口 |
| `tryAcquire()` | - | RateLimitResult | 尝试通过 |
| `acquireAsync(timeout?)` | timeout?: number | Promise\<RateLimitResult\> | 异步等待通过 |
| `getCount()` | - | number | 获取当前计数 |
| `reset()` | - | void | 重置计数器 |

### MultiRateLimiter

| 方法 | 参数 | 返回值 | 说明 |
|------|------|--------|------|
| `constructor(config)` | maxRequests, windowMs | - | 创建多用户限流器 |
| `tryAcquire(key)` | key: string | RateLimitResult | 尝试为指定键通过 |
| `acquireAsync(key, timeout?)` | key, timeout? | Promise\<RateLimitResult\> | 异步等待通过 |
| `getStatus(key)` | key: string | {count, remaining} \| null | 获取状态 |
| `reset(key)` | key: string | void | 重置指定键 |
| `resetAll()` | - | void | 重置所有键 |
| `size()` | - | number | 获取活跃键数量 |

### RateLimitResult

```typescript
interface RateLimitResult {
  allowed: boolean;     // 是否允许
  remaining: number;     // 剩余配额
  resetMs: number;       // 重置时间（毫秒）
  retryAfter?: number;   // 重试等待时间（毫秒）
}
```

## 使用场景

| 场景 | 推荐算法 | 原因 |
|------|----------|------|
| API 网关 | Token Bucket | 允许突发流量，用户体验好 |
| 消息队列 | Leaky Bucket | 恒定消费速率，防止下游过载 |
| 简单限流 | Fixed Window | 实现简单，内存占用小 |
| 精确限流 | Sliding Window | 避免窗口边界突发 |
| 多租户系统 | MultiRateLimiter | 用户隔离，独立限流 |

## 运行测试

```bash
# 使用 ts-node
npx ts-node rate_limiter_test.ts

# 或编译后运行
tsc rate_limiter_test.ts
node rate_limiter_test.js
```

## License

MIT