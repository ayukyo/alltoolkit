# RateLimiterUtils - Kotlin 限流器工具库

多种限流算法的零依赖 Kotlin 实现，适用于 API 限流、流量控制、资源保护等场景。

## 特性

- **零外部依赖** - 仅使用 Kotlin 标准库和 Java 并发工具
- **线程安全** - 所有实现都支持并发访问
- **多种算法** - 5 种常用限流算法可选
- **易于使用** - 简洁的 API 设计
- **工厂模式** - 快速创建限流器实例

## 支持的算法

| 算法 | 特点 | 适用场景 |
|------|------|----------|
| Token Bucket (令牌桶) | 允许突发流量，平滑限流 | API 限流、网络流量控制 |
| Leaky Bucket (漏桶) | 严格控制流出速率 | 流量整形、消息队列处理 |
| Fixed Window Counter (固定窗口) | 实现简单，内存占用小 | 简单限流场景 |
| Sliding Window Log (滑动窗口日志) | 精确控制，无边界问题 | 需要精确限流的场景 |
| Sliding Window Counter (滑动窗口计数器) | 内存占用小，近似滑动窗口 | 分布式限流、高性能场景 |

## 安装

将 `RateLimiterUtils.kt` 文件复制到您的 Kotlin 项目中即可使用。

## 快速开始

### 令牌桶限流器

```kotlin
import com.alltoolkit.ratelimiter.*

// 创建容量为 100，每秒填充 10 个令牌的桶
val bucket = TokenBucket.create(ratePerSecond = 10, capacity = 100)

// 尝试获取 1 个令牌
val result = bucket.tryAcquire()
if (result.allowed) {
    // 处理请求
} else {
    // 拒绝请求，告知客户端等待
    println("Rate limited. Retry after ${result.retryAfterMs}ms")
}
```

### 固定窗口限流器

```kotlin
// 创建每分钟 60 请求的限流器
val limiter = FixedWindowCounter.create(ratePerMinute = 60)

// 按 IP 地址限流
val result = limiter.tryAcquire("192.168.1.1")
if (result.allowed) {
    // 处理请求
}
```

### 滑动窗口限流器

```kotlin
// 创建 1 秒窗口内最多 10 请求的限流器
val limiter = SlidingWindowLog(limit = 10, windowSizeMs = 1000)

// 按用户 ID 限流
val result = limiter.tryAcquire("user-123")
```

## 使用工厂方法

```kotlin
// 令牌桶：每秒 100 请求，突发上限 200
val tokenBucket = RateLimiterFactory.tokenBucket(100, 200)

// 漏桶：每秒 50 请求处理能力
val leakyBucket = RateLimiterFactory.leakyBucket(50, 50)

// 固定窗口：每分钟 60 请求
val fixedWindow = RateLimiterFactory.fixedWindowPerMinute(60)

// 滑动窗口：每分钟 100 请求
val slidingWindow = RateLimiterFactory.slidingWindowPerMinute(100)
```

## 限流器管理器

统一管理多个限流器实例：

```kotlin
val manager = RateLimiterManager()

// 注册限流器
manager.register("api-global", TokenBucket.create(1000, 2000))
manager.register("api-per-user", FixedWindowCounter.create(100))
manager.register("upload", SlidingWindowLog(10, 60_000))

// 获取并使用
val limiter = manager.getTokenBucket("api-global")
limiter?.tryAcquire()

// 移除
manager.unregister("upload")
```

## API 保护示例

```kotlin
class ApiServer {
    private val globalLimiter = TokenBucket.create(100, 150)
    private val userLimiters = FixedWindowCounter(limit = 20, windowSizeMs = 60_000)
    private val ipLimiters = SlidingWindowLog(50, 60_000)
    
    fun handleRequest(userId: String, ip: String): String {
        // 1. 全局限流
        if (!globalLimiter.tryAcquire().allowed) {
            return "503 Service Unavailable"
        }
        
        // 2. 用户限流
        if (!userLimiters.tryAcquire(userId).allowed) {
            return "429 Too Many Requests"
        }
        
        // 3. IP 限流
        if (!ipLimiters.tryAcquire(ip).allowed) {
            return "429 Too Many Requests"
        }
        
        return "200 OK"
    }
}
```

## 批量获取令牌

```kotlin
val bucket = TokenBucket.create(10, 100)

// 一次获取多个令牌（适用于批量操作）
val result = bucket.tryAcquire(30)
if (result.allowed) {
    // 处理批量请求
    println("Remaining tokens: ${result.remainingTokens}")
} else {
    println("Need to wait ${result.waitTimeMs}ms")
}
```

## RateLimitResult 说明

所有限流器的 `tryAcquire()` 方法返回 `RateLimitResult` 对象：

```kotlin
data class RateLimitResult(
    val allowed: Boolean,        // 是否允许请求
    val remainingTokens: Long,   // 剩余令牌数
    val waitTimeMs: Long,        // 建议等待时间（毫秒）
    val retryAfterMs: Long       // 重试等待时间（毫秒）
)
```

## 运行测试

```bash
# 使用 Gradle
gradle test

# 或使用 Kotlin 命令行
kotlinc RateLimiterUtils.kt RateLimiterUtilsTest.kt -include-runtime -d test.jar
kotlin -cp test.jar org.junit.runner.JUnitCore RateLimiterUtilsTest
```

## 算法对比

### 令牌桶 vs 漏桶

- **令牌桶**：允许突发流量，适合需要处理突发请求的场景
- **漏桶**：严格限制流出速率，适合需要平滑流量的场景

### 固定窗口 vs 滑动窗口

- **固定窗口**：实现简单，但可能在窗口边界出现突刺
- **滑动窗口**：精确控制，但内存/计算开销较大

## 性能建议

1. **高并发场景**：使用 `TokenBucket` 或 `SlidingWindowCounter`
2. **精确控制**：使用 `SlidingWindowLog`
3. **简单场景**：使用 `FixedWindowCounter`
4. **流量整形**：使用 `LeakyBucket`

## 线程安全

所有限流器实现都是线程安全的，可以在多线程环境中直接使用。

## 许可证

MIT License