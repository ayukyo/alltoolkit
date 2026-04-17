# Rate Limiter - Zig 限流器工具库

一个完整的 Zig 限流器实现，包含四种经典算法，零外部依赖，适合 API 限流、带宽控制、请求频率管理等场景。

## 功能特性

### 四种限流算法

| 算法 | 特点 | 适用场景 |
|------|------|----------|
| **Token Bucket** | 允许突发流量，平滑限流 | API 限流、带宽控制 |
| **Fixed Window** | 简单计数器，固定时间窗口 | 简单限流、统计报表 |
| **Sliding Window** | 精确控制，无边界突发 | 精确限流、金融交易 |
| **Leaky Bucket** | 恒定流出速率，平滑流量 | 流量整形、消息队列 |

### 核心功能

- ✅ 令牌桶（Token Bucket）- 突发流量支持
- ✅ 固定窗口（Fixed Window）- 简单高效
- ✅ 滑动窗口（Sliding Window）- 精确限流
- ✅ 漏桶（Leaky Bucket）- 流量整形
- ✅ 时间单位转换（秒/分/时）
- ✅ 批量请求支持
- ✅ 等待时间计算
- ✅ 零外部依赖

## 快速开始

### 基本用法

```zig
const rate_limiter = @import("rate_limiter");

// Token Bucket - 允许突发
var bucket = rate_limiter.TokenBucket.init(100, 10, std.time.ns_per_s);
if (bucket.tryAcquire()) {
    // 请求允许
} else {
    // 超过限制
}

// Fixed Window - 简单计数
var window = rate_limiter.FixedWindow.init(60, std.time.ns_per_min);
window.tryAcquire(); // 尝试请求

// Sliding Window - 精确控制
var sliding = rate_limiter.SlidingWindow.init(allocator, 100, std.time.ns_per_s);
defer sliding.deinit();
sliding.tryAcquire();

// Leaky Bucket - 流量整形
var leaky = rate_limiter.LeakyBucket.init(10, 3, std.time.ns_per_s);
leaky.tryPour(5); // 添加5个请求
```

### 便捷函数

```zig
// 快速创建常见配置
var per_second = rate_limiter.tokenBucketPerSecond(100, 10);
var per_minute = rate_limiter.fixedWindowPerMinute(60);
var sliding_per_sec = rate_limiter.slidingWindowPerSecond(allocator, 50);
var leaky_per_sec = rate_limiter.leakyBucketPerSecond(100, 10);
```

## API 文档

### TokenBucket

令牌桶限流器，支持突发流量。

```zig
// 初始化
var bucket = TokenBucket.init(capacity, refill_amount, interval_ns);

// 方法
bucket.tryAcquire() -> bool           // 尝试获取1个令牌
bucket.tryConsume(tokens) -> bool     // 尝试获取N个令牌
bucket.consume(tokens) -> error!void  // 获取令牌（错误方式）
bucket.availableTokens() -> u64       // 当前可用令牌
bucket.timeUntilAvailable(tokens) -> u64  // 等待时间（纳秒）
bucket.reset()                        // 重置为满桶
```

### FixedWindow

固定窗口计数限流器。

```zig
// 初始化
var window = FixedWindow.init(max_requests, window_ns);

// 方法
window.tryAcquire() -> bool           // 尝试请求
window.tryAcquireN(count) -> bool     // 批量请求
window.acquire() -> error!void        // 请求（错误方式）
window.currentCount() -> u64          // 当前计数
window.remaining() -> u64             // 剩余配额
window.timeUntilReset() -> u64        // 窗口重置时间
window.reset()                        // 重置计数
```

### SlidingWindow

滑动窗口限流器，精确控制。

```zig
// 初始化
var window = SlidingWindow.init(allocator, max_requests, window_ns);
defer window.deinit();  // 需要释放

// 方法
window.tryAcquire() -> bool
window.tryAcquireN(count) -> bool
window.acquire() -> error!void
window.currentCount() -> u64
window.remaining() -> u64
window.timeUntilAvailable() -> u64
window.reset()
```

### LeakyBucket

漏桶限流器，恒定流出。

```zig
// 初始化
var bucket = LeakyBucket.init(capacity, leak_amount, interval_ns);

// 方法
bucket.tryAcquire() -> bool           // 添加1个水滴
bucket.tryPour(drops) -> bool         // 添加N个水滴
bucket.pour(drops) -> error!void      // 添加水滴（错误方式）
bucket.currentLevel() -> u64          // 当前水位
bucket.remainingCapacity() -> u64     // 剩余容量
bucket.timeUntilAvailable(drops) -> u64
bucket.reset()
```

### TimeUnit

时间单位转换。

```zig
const TimeUnit = enum {
    milliseconds,
    seconds,
    minutes,
    hours,
};

// 使用
var bucket = TokenBucket.initWithUnit(100, 10, 1, .minutes);
```

## 构建和测试

### 构建

```bash
cd rate-limiter
zig build
```

### 运行测试

```bash
zig build test
```

### 运行示例

```bash
zig build basic    # 基础示例
zig build advanced # 高级示例
```

## 使用场景

### 1. API 限流

```zig
// API 端点：100次/分钟突发，10次/秒平均
var api_limiter = TokenBucket.initWithUnit(100, 10, 1, .seconds);

// 每次请求前检查
if (api_limiter.tryAcquire()) {
    handleRequest();
} else {
    return error.RateLimitExceeded;
}
```

### 2. 多层级限流

```zig
// 同时限制秒级和分钟级
var second_limit = FixedWindow.init(10, std.time.ns_per_s);
var minute_limit = FixedWindow.init(100, std.time.ns_per_min);

if (second_limit.tryAcquire() and minute_limit.tryAcquire()) {
    processRequest();
}
```

### 3. 带宽控制

```zig
// 500KB突发，100KB/100ms填充（1MB/s）
var bandwidth = TokenBucket.init(500_000, 100_000, 100_000_000);

if (bandwidth.tryConsume(file_size)) {
    transferFile(file);
}
```

### 4. 批量请求

```zig
var batch_limiter = FixedWindow.init(1000, std.time.ns_per_min);

// 批量处理50个请求
if (batch_limiter.tryAcquireN(50)) {
    processBatch(batch);
}
```

## 算法对比

| 特性 | Token Bucket | Fixed Window | Sliding Window | Leaky Bucket |
|------|-------------|--------------|----------------|--------------|
| 突发支持 | ✓ 强 | ✗ 无 | ✓ 弱 | ✗ 无 |
| 内存占用 | 低 | 低 | 中 | 低 |
| 精确度 | 高 | 低 | 最高 | 高 |
| 实现复杂度 | 中 | 低 | 高 | 中 |
| 适用场景 | API限流 | 统计报表 | 金融交易 | 流量整形 |

## 性能特点

- 零外部依赖，纯 Zig 标准库
- 编译时类型安全
- 低内存占用
- 适合嵌入式和高性能场景

## 文件结构

```
rate-limiter/
├── build.zig           # 构建配置
├── build.zig.zon       # 项目依赖
├── src/
│   └── rate_limiter.zig # 主模块
├── examples/
│   ├── basic.zig       # 基础示例
│   └── advanced.zig    # 高级示例
└── README.md           # 文档
```

## 许可证

MIT License

## 贡献

欢迎提交 Issue 和 Pull Request！