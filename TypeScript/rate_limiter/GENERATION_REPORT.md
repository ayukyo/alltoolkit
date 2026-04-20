# Rate Limiter 工具模块生成报告

## 模块信息

- **模块名称**: rate_limiter
- **语言**: TypeScript
- **位置**: TypeScript/rate_limiter/
- **生成日期**: 2026-04-20

## 核心功能

### 1. 令牌桶算法 (TokenBucket)
- 支持突发流量
- 可配置容量和填充速率
- 支持异步等待获取令牌

### 2. 漏桶算法 (LeakyBucket)
- 恒定速率输出
- 适合流量整形
- 队列容量控制

### 3. 固定窗口计数器 (FixedWindowCounter)
- 简单高效的限流实现
- 基于时间窗口的请求计数

### 4. 滑动窗口计数器 (SlidingWindowCounter)
- 更精确的限流控制
- 可配置精度参数
- 避免窗口边界问题

### 5. 多用户限流器 (MultiRateLimiter)
- 为不同用户/API Key独立限流
- 支持状态查询和重置

### 6. 工具函数
- `rateLimit` 装饰器：为类方法添加限流
- `wrapRateLimit`：包装函数添加限流
- `rateLimitedBatch`：批量任务限流执行

## 文件结构

```
TypeScript/rate_limiter/
├── mod.ts                    # 主模块（零外部依赖）
├── rate_limiter_test.ts      # 完整测试文件
├── README.md                 # 使用文档
├── GENERATION_REPORT.md      # 本报告
└── examples/
    └── usage_examples.ts     # 使用示例
```

## 测试覆盖

- TokenBucket 测试 (基本获取、剩余计数、填充、重置)
- LeakyBucket 测试 (基本获取、队列大小、重置)
- FixedWindowCounter 测试 (基本获取、剩余、重置)
- SlidingWindowCounter 测试 (基本获取、计数、重置)
- MultiRateLimiter 测试 (多键、状态、重置)
- RateLimitError 测试
- wrapRateLimit 测试
- rateLimitedBatch 测试
- 异步获取测试
- 边界情况测试

## 使用示例

### 基础用法

```typescript
import { TokenBucket } from './rate_limiter/mod';

const limiter = new TokenBucket({
  capacity: 100,
  refillRate: 10
});

if (limiter.acquire().allowed) {
  // 处理请求
} else {
  // 被限流
}
```

### 多用户限流

```typescript
import { MultiRateLimiter } from './rate_limiter/mod';

const limiter = new MultiRateLimiter({
  maxRequests: 100,
  windowMs: 60000
});

limiter.tryAcquire('user-123');
```

### 装饰器模式

```typescript
import { rateLimit } from './rate_limiter/mod';

class ApiService {
  @rateLimit({ maxRequests: 10, windowMs: 1000 })
  async fetchData(url: string) {
    // 自动限流
  }
}
```

## 特性

- ✅ 零外部依赖
- ✅ TypeScript 原生类型支持
- ✅ 同步和异步 API
- ✅ 完整的测试覆盖
- ✅ 详细的文档和示例
- ✅ 支持多种限流算法
- ✅ 装饰器支持

## 适用场景

| 场景 | 推荐算法 |
|------|----------|
| API 网关 | TokenBucket |
| 消息队列 | LeakyBucket |
| 简单限流 | FixedWindowCounter |
| 精确限流 | SlidingWindowCounter |
| 多租户系统 | MultiRateLimiter |