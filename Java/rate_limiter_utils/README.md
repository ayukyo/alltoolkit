# Rate Limiter Utils - 限流器工具集

[![Java](https://img.shields.io/badge/Java-8%2B-orange)](https://www.java.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

提供多种限流算法实现，用于 API 限流、请求控制、系统资源保护等场景。零外部依赖，纯 Java 标准库实现。

## ✨ 特性

- **零依赖** - 仅使用 Java 标准库
- **线程安全** - 所有实现都支持并发访问
- **多种算法** - 令牌桶、漏桶、滑动窗口、固定窗口
- **分布式支持** - 为不同键（IP、用户）提供独立限流
- **生产就绪** - 完整测试覆盖，详细文档

## 📦 支持的算法

### 1. 令牌桶 (Token Bucket)

```
原理：以恒定速率往桶中放入令牌，请求需要获取令牌才能通过。
特点：
  ✅ 允许突发流量（桶中有存量令牌时）
  ✅ 平滑限流
  ✅ 适合有波动的流量场景

适用场景：
  - API 网关限流
  - 流量整形
  - 允许一定突发的业务场景
```

### 2. 漏桶 (Leaky Bucket)

```
原理：请求以任意速率进入桶中，桶以恒定速率漏出请求。
特点：
  ✅ 恒定输出速率
  ✅ 削峰填谷
  ✅ 适合需要稳定输出的场景

适用场景：
  - 数据库访问控制
  - 外部 API 调用
  - 消息队列消费
```

### 3. 滑动窗口 (Sliding Window)

```
原理：维护一个时间窗口内的请求记录，精确统计当前窗口内的请求数。
特点：
  ✅ 精确限流
  ✅ 无边界问题
  ⚠️ 内存占用较高

适用场景：
  - 需要精确控制的场景
  - 实时监控系统
```

### 4. 固定窗口 (Fixed Window)

```
原理：在固定时间窗口内计数，窗口结束时重置计数器。
特点：
  ✅ 简单高效
  ✅ 内存占用低
  ⚠️ 可能有边界问题

适用场景：
  - 简单限流场景
  - 对边界不敏感的业务
```

## 🚀 快速开始

### 创建限流器

```java
import ratelimiter.*;

// 令牌桶 - 允许突发
TokenBucket tokenBucket = RateLimiterFactory.createTokenBucket(100, 10);
// 容量: 100, 补充速率: 10/秒

// 漏桶 - 恒定速率
LeakyBucket leakyBucket = RateLimiterFactory.createLeakyBucket(50, 10);
// 容量: 50, 漏出速率: 10/秒

// 滑动窗口 - 精确限流
SlidingWindow slidingWindow = RateLimiterFactory.createSlidingWindow(100, 1000);
// 最大请求: 100, 窗口: 1000ms

// 固定窗口 - 简单高效
FixedWindow fixedWindow = RateLimiterFactory.createFixedWindow(100, 1000);
// 最大请求: 100, 窗口: 1000ms

// 分布式限流器 - 按键限流
DistributedRateLimiter distributed = RateLimiterFactory.createDistributed(10, 1000);
// 每个键最大请求: 10, 窗口: 1000ms
```

### 基本使用

```java
// 尝试通过请求
if (limiter.tryAcquire()) {
    // 请求通过，处理业务逻辑
    processRequest();
} else {
    // 被限流，返回错误
    return ResponseEntity.status(429).body("Too Many Requests");
}

// 尝试通过多个请求
if (limiter.tryAcquire(5)) {
    // 5 个请求都通过
}

// 获取当前状态
long current = limiter.getCurrentCount(); // 或 getAvailableTokens()

// 重置限流器
limiter.reset();
```

## 📚 实际应用示例

### 1. API 限流

```java
// 创建 API 限流器：每秒 100 个请求
TokenBucket apiLimiter = RateLimiterFactory.createApiLimiter(100);

// 在请求处理前检查
if (!apiLimiter.tryAcquire()) {
    return ResponseEntity.status(429).body("Too Many Requests");
}
// 处理请求...
```

### 2. 用户请求控制

```java
// 每个用户每分钟最多 60 个请求
DistributedRateLimiter userLimiter = RateLimiterFactory.createDistributed(60, 60000);

// 检查用户请求
String userId = getCurrentUserId();
if (!userLimiter.tryAcquire(userId)) {
    return "Rate limit exceeded for user: " + userId;
}
// 处理请求...
```

### 3. IP 限流

```java
// 每个 IP 每秒最多 10 个请求
DistributedRateLimiter ipLimiter = RateLimiterFactory.createDistributed(10, 1000);

// 检查 IP 请求
String clientIp = getClientIp();
if (!ipLimiter.tryAcquire(clientIp)) {
    return "Rate limit exceeded for IP: " + clientIp;
}
// 处理请求...
```

### 4. 突发流量处理

```java
// 允许突发 50 个请求，平均 10 个/秒
TokenBucket burstLimiter = RateLimiterFactory.createBurstLimiter(50, 10);

// 处理突发请求
if (burstLimiter.tryAcquire(30)) {
    // 突发 30 个请求通过
}
```

### 5. 多级限流

```java
// 全局限流：1000/秒
TokenBucket globalLimiter = RateLimiterFactory.createApiLimiter(1000);

// 用户限流：10/秒
DistributedRateLimiter userLimiter = RateLimiterFactory.createDistributed(10, 1000);

// 检查全局
if (!globalLimiter.tryAcquire()) {
    return "Global rate limit exceeded";
}

// 检查用户
String userId = getCurrentUserId();
if (!userLimiter.tryAcquire(userId)) {
    return "User rate limit exceeded";
}
// 处理请求...
```

### 6. Web 服务中间件

```java
public class RateLimitMiddleware {
    private final TokenBucket globalLimiter;
    private final DistributedRateLimiter ipLimiter;
    private final DistributedRateLimiter userLimiter;
    
    public RateLimitMiddleware() {
        this.globalLimiter = RateLimiterFactory.createApiLimiter(10000);
        this.ipLimiter = RateLimiterFactory.createDistributed(100, 1000);
        this.userLimiter = RateLimiterFactory.createDistributed(50, 1000);
    }
    
    public boolean allowRequest(String ip, String userId) {
        // 全局限流
        if (!globalLimiter.tryAcquire()) {
            return false;
        }
        
        // IP 限流
        if (!ipLimiter.tryAcquire(ip)) {
            return false;
        }
        
        // 用户限流
        if (!userLimiter.tryAcquire(userId)) {
            return false;
        }
        
        return true;
    }
}
```

## 🔧 工厂方法

```java
// 创建令牌桶限流器
TokenBucket createTokenBucket(long capacity, long refillRate);

// 创建漏桶限流器
LeakyBucket createLeakyBucket(long capacity, long leakRate);

// 创建滑动窗口限流器
SlidingWindow createSlidingWindow(long maxRequests, long windowSizeMillis);

// 创建固定窗口限流器
FixedWindow createFixedWindow(long maxRequests, long windowSizeMillis);

// 创建分布式限流器
DistributedRateLimiter createDistributed(long maxRequests, long windowSizeMillis);

// 创建 API 限流器（预设配置）
TokenBucket createApiLimiter(long requestsPerSecond);

// 创建突发流量限流器
TokenBucket createBurstLimiter(long burstSize, long averageRate);
```

## 📊 算法对比

| 算法 | 突发流量 | 精确度 | 内存占用 | 适用场景 |
|------|---------|--------|---------|---------|
| 令牌桶 | ✅ 允许 | 高 | 低 | API 网关、流量整形 |
| 漏桶 | ❌ 不允许 | 高 | 低 | 数据库访问、外部 API |
| 滑动窗口 | ❌ 不允许 | 最高 | 高 | 精确控制、实时监控 |
| 固定窗口 | ⚠️ 边界突发 | 低 | 最低 | 简单限流 |

## 🧪 测试

```bash
# 编译测试
javac -d out Java/rate_limiter_utils/mod.java Java/rate_limiter_utils/RateLimiterTest.java

# 运行测试
java -cp out ratelimiter.RateLimiterTest
```

测试覆盖：
- ✅ 基本功能测试
- ✅ 参数验证测试
- ✅ 并发安全测试
- ✅ 时间窗口测试
- ✅ 边界值测试
- ✅ 分布式限流测试

## 📖 API 文档

### TokenBucket

```java
// 构造函数
TokenBucket(long capacity, long refillRate)

// 方法
boolean tryAcquire()                    // 获取 1 个令牌
boolean tryAcquire(long tokens)         // 获取多个令牌
long getAvailableTokens()               // 获取可用令牌数
void reset()                            // 重置令牌桶
```

### LeakyBucket

```java
// 构造函数
LeakyBucket(long capacity, long leakRate)

// 方法
boolean tryAcquire()                    // 添加 1 个请求
boolean tryAcquire(long requests)       // 添加多个请求
long getCurrentWater()                   // 获取当前水量
void reset()                            // 重置漏桶
```

### SlidingWindow

```java
// 构造函数
SlidingWindow(long maxRequests, long windowSizeMillis)

// 方法
boolean tryAcquire()                    // 通过 1 个请求
boolean tryAcquire(long requests)       // 通过多个请求
long getCurrentCount()                  // 获取当前请求数
void reset()                            // 重置窗口
```

### FixedWindow

```java
// 构造函数
FixedWindow(long maxRequests, long windowSizeMillis)

// 方法
boolean tryAcquire()                    // 通过 1 个请求
boolean tryAcquire(long requests)       // 通过多个请求
int getCurrentCount()                   // 获取当前请求数
long getRemainingTime()                 // 获取窗口剩余时间
void reset()                            // 重置窗口
```

### DistributedRateLimiter

```java
// 构造函数
DistributedRateLimiter(long maxRequests, long windowSizeMillis)

// 方法
boolean tryAcquire(String key)          // 为指定键通过请求
long getCurrentCount(String key)        // 获取指定键的请求数
void reset(String key)                  // 重置指定键
void resetAll()                         // 重置所有键
int getActiveKeyCount()                 // 获取活跃键数量
```

## 📋 最佳实践

1. **选择合适的算法**
   - 需要允许突发：令牌桶
   - 需要恒定输出：漏桶
   - 需要精确控制：滑动窗口
   - 简单场景：固定窗口

2. **多级限流**
   - 全局限流 → 防止系统过载
   - IP 限流 → 防止单 IP 攻击
   - 用户限流 → 防止单用户滥用

3. **合理配置参数**
   - 根据系统容量设置限流阈值
   - 考虑业务峰值和正常流量
   - 留有一定的安全余量

4. **监控和告警**
   - 记录限流事件
   - 监控限流比例
   - 设置告警阈值

## 📄 许可证

MIT License - 详见 [LICENSE](../LICENSE)

## 🔗 相关链接

- [GitHub](https://github.com/ayukyo/alltoolkit)
- [问题反馈](https://github.com/ayukyo/alltoolkit/issues)