/**
 * RateLimiterUtils - 多种限流算法的零依赖实现
 * 
 * 支持的算法：
 * - Token Bucket (令牌桶)
 * - Leaky Bucket (漏桶)
 * - Fixed Window Counter (固定窗口计数器)
 * - Sliding Window Log (滑动窗口日志)
 * - Sliding Window Counter (滑动窗口计数器)
 * 
 * @author AllToolkit
 * @date 2026-05-03
 */

package com.alltoolkit.ratelimiter

import java.util.concurrent.ConcurrentHashMap
import java.util.concurrent.ConcurrentLinkedQueue
import java.util.concurrent.atomic.AtomicLong
import java.util.concurrent.atomic.AtomicReference
import java.util.concurrent.locks.ReentrantLock
import kotlin.concurrent.withLock

/**
 * 限流结果
 */
data class RateLimitResult(
    val allowed: Boolean,
    val remainingTokens: Long = 0,
    val waitTimeMs: Long = 0,
    val retryAfterMs: Long = 0
)

/**
 * 令牌桶限流器 (Token Bucket)
 * 
 * 原理：以固定速率向桶中添加令牌，请求消耗令牌，桶满则拒绝
 * 优点：允许突发流量，平滑限流
 * 适用场景：API限流、网络流量控制
 */
class TokenBucket(
    private val capacity: Long,        // 桶容量
    private val refillRate: Double,    // 每毫秒填充令牌数
    private val initialTokens: Long = capacity
) {
    private var tokens = AtomicLong(initialTokens)
    private var lastRefillTime = AtomicLong(System.currentTimeMillis())
    private val lock = ReentrantLock()
    
    fun tryAcquire(tokensRequested: Long = 1): RateLimitResult {
        return lock.withLock {
            refill()
            
            if (tokens.get() >= tokensRequested) {
                tokens.addAndGet(-tokensRequested)
                RateLimitResult(
                    allowed = true,
                    remainingTokens = tokens.get()
                )
            } else {
                val needed = tokensRequested - tokens.get()
                val waitTimeMs = (needed / refillRate).toLong()
                RateLimitResult(
                    allowed = false,
                    remainingTokens = tokens.get(),
                    waitTimeMs = waitTimeMs,
                    retryAfterMs = waitTimeMs
                )
            }
        }
    }
    
    private fun refill() {
        val now = System.currentTimeMillis()
        val elapsedTime = now - lastRefillTime.get()
        
        if (elapsedTime > 0) {
            val tokensToAdd = (elapsedTime * refillRate).toLong()
            if (tokensToAdd > 0) {
                val newTokens = minOf(capacity, tokens.get() + tokensToAdd)
                tokens.set(newTokens)
                lastRefillTime.set(now)
            }
        }
    }
    
    fun getAvailableTokens(): Long {
        lock.withLock { refill() }
        return tokens.get()
    }
    
    companion object {
        /**
         * 创建每秒填充指定令牌数的桶
         */
        fun create(ratePerSecond: Long, capacity: Long): TokenBucket {
            return TokenBucket(capacity, ratePerSecond / 1000.0)
        }
    }
}

/**
 * 漏桶限流器 (Leaky Bucket)
 * 
 * 原理：请求进入队列，以固定速率处理，队列满则拒绝
 * 优点：严格控制流出速率
 * 适用场景：流量整形、消息队列处理
 */
class LeakyBucket(
    private val capacity: Long,        // 桶容量
    private val leakRate: Double       // 每毫秒漏出请求数
) {
    private var water = AtomicLong(0)
    private var lastLeakTime = AtomicLong(System.currentTimeMillis())
    private val lock = ReentrantLock()
    
    fun tryAcquire(): RateLimitResult {
        return lock.withLock {
            leak()
            
            if (water.get() < capacity) {
                water.incrementAndGet()
                RateLimitResult(
                    allowed = true,
                    remainingTokens = capacity - water.get() - 1
                )
            } else {
                val waitTimeMs = (1.0 / leakRate).toLong()
                RateLimitResult(
                    allowed = false,
                    waitTimeMs = waitTimeMs,
                    retryAfterMs = waitTimeMs
                )
            }
        }
    }
    
    private fun leak() {
        val now = System.currentTimeMillis()
        val elapsedTime = now - lastLeakTime.get()
        
        if (elapsedTime > 0) {
            val leaked = (elapsedTime * leakRate).toLong()
            if (leaked > 0) {
                water.set(maxOf(0, water.get() - leaked))
                lastLeakTime.set(now)
            }
        }
    }
    
    companion object {
        fun create(ratePerSecond: Long, capacity: Long): LeakyBucket {
            return LeakyBucket(capacity, ratePerSecond / 1000.0)
        }
    }
}

/**
 * 固定窗口计数器限流器 (Fixed Window Counter)
 * 
 * 原理：在固定时间窗口内计数，超限则拒绝
 * 优点：实现简单，内存占用小
 * 缺点：窗口边界可能存在突刺问题
 * 适用场景：简单限流场景
 */
class FixedWindowCounter(
    private val limit: Long,           // 窗口内最大请求数
    private val windowSizeMs: Long     // 窗口大小（毫秒）
) {
    private val counters = ConcurrentHashMap<String, WindowCounter>()
    
    private data class WindowCounter(
        val count: AtomicLong = AtomicLong(0),
        val windowStart: AtomicLong = AtomicLong(System.currentTimeMillis())
    )
    
    fun tryAcquire(key: String = "default"): RateLimitResult {
        val now = System.currentTimeMillis()
        val counter = counters.computeIfAbsent(key) { WindowCounter() }
        
        synchronized(counter) {
            // 检查是否需要重置窗口
            if (now - counter.windowStart.get() >= windowSizeMs) {
                counter.count.set(0)
                counter.windowStart.set(now)
            }
            
            val currentCount = counter.count.get()
            
            return if (currentCount < limit) {
                counter.count.incrementAndGet()
                RateLimitResult(
                    allowed = true,
                    remainingTokens = limit - currentCount - 1
                )
            } else {
                val windowEnd = counter.windowStart.get() + windowSizeMs
                val retryAfter = windowEnd - now
                RateLimitResult(
                    allowed = false,
                    remainingTokens = 0,
                    retryAfterMs = retryAfter
                )
            }
        }
    }
    
    fun getCount(key: String = "default"): Long {
        return counters[key]?.count?.get() ?: 0
    }
    
    fun reset(key: String = "default") {
        counters.remove(key)
    }
    
    companion object {
        fun create(ratePerMinute: Long): FixedWindowCounter {
            return FixedWindowCounter(ratePerMinute, 60_000L)
        }
    }
}

/**
 * 滑动窗口日志限流器 (Sliding Window Log)
 * 
 * 原理：记录每个请求的时间戳，统计窗口内请求数
 * 优点：精确控制，无边界突刺问题
 * 缺点：内存占用较大（存储所有请求时间戳）
 * 适用场景：需要精确限流的场景
 */
class SlidingWindowLog(
    private val limit: Long,           // 窗口内最大请求数
    private val windowSizeMs: Long     // 窗口大小（毫秒）
) {
    private val logs = ConcurrentHashMap<String, ConcurrentLinkedQueue<Long>>()
    private val lock = ReentrantLock()
    
    fun tryAcquire(key: String = "default"): RateLimitResult {
        val now = System.currentTimeMillis()
        val windowStart = now - windowSizeMs
        
        return lock.withLock {
            val queue = logs.computeIfAbsent(key) { ConcurrentLinkedQueue() }
            
            // 清理过期的请求记录
            while (queue.isNotEmpty() && queue.peek() < windowStart) {
                queue.poll()
            }
            
            val currentCount = queue.size.toLong()
            
            return if (currentCount < limit) {
                queue.add(now)
                RateLimitResult(
                    allowed = true,
                    remainingTokens = limit - currentCount - 1
                )
            } else {
                val oldestInWindow = queue.peek()
                val retryAfter = oldestInWindow + windowSizeMs - now
                RateLimitResult(
                    allowed = false,
                    remainingTokens = 0,
                    retryAfterMs = maxOf(0, retryAfter)
                )
            }
        }
    }
    
    fun getCount(key: String = "default"): Long {
        val now = System.currentTimeMillis()
        val windowStart = now - windowSizeMs
        val queue = logs[key] ?: return 0
        
        return queue.count { it >= windowStart }.toLong()
    }
    
    fun clear(key: String = "default") {
        logs.remove(key)
    }
}

/**
 * 滑动窗口计数器限流器 (Sliding Window Counter)
 * 
 * 原理：使用当前窗口和前一窗口的加权计数
 * 优点：内存占用小，近似滑动窗口效果
 * 适用场景：分布式限流、高性能场景
 */
class SlidingWindowCounter(
    private val limit: Long,           // 窗口内最大请求数
    private val windowSizeMs: Long     // 窗口大小（毫秒）
) {
    private val windows = ConcurrentHashMap<String, SlidingWindow>()
    
    private data class SlidingWindow(
        val count: AtomicLong = AtomicLong(0),
        val windowStart: AtomicLong = AtomicLong(System.currentTimeMillis())
    )
    
    private data class WindowState(
        val currentWindow: SlidingWindow,
        val previousWindow: SlidingWindow
    )
    
    fun tryAcquire(key: String = "default"): RateLimitResult {
        val now = System.currentTimeMillis()
        val currentWindowStart = (now / windowSizeMs) * windowSizeMs
        
        val state = getState(key, currentWindowStart)
        
        synchronized(state) {
            // 计算滑动窗口内的请求数
            val previousWeight = (windowSizeMs - (now - currentWindowStart)) / windowSizeMs.toDouble()
            val estimatedCount = state.currentWindow.count.get() + 
                                previousWeight * state.previousWindow.count.get()
            
            return if (estimatedCount < limit) {
                state.currentWindow.count.incrementAndGet()
                RateLimitResult(
                    allowed = true,
                    remainingTokens = (limit - estimatedCount.toLong() - 1).coerceAtLeast(0)
                )
            } else {
                val waitTime = windowSizeMs - (now - currentWindowStart)
                RateLimitResult(
                    allowed = false,
                    remainingTokens = 0,
                    retryAfterMs = waitTime
                )
            }
        }
    }
    
    private fun getState(key: String, currentWindowStart: Long): WindowState {
        // 简化实现，使用当前窗口
        val current = windows.computeIfAbsent("$key:current") { 
            SlidingWindow(windowStart = AtomicLong(currentWindowStart))
        }
        val previous = windows.computeIfAbsent("$key:previous") {
            SlidingWindow(windowStart = AtomicLong(currentWindowStart - windowSizeMs))
        }
        
        // 检查是否需要切换窗口
        synchronized(current) {
            if (current.windowStart.get() < currentWindowStart) {
                // 当前窗口变为前一窗口
                previous.count.set(current.count.get())
                previous.windowStart.set(current.windowStart.get())
                // 重置当前窗口
                current.count.set(0)
                current.windowStart.set(currentWindowStart)
            }
        }
        
        return WindowState(current, previous)
    }
    
    companion object {
        fun create(ratePerMinute: Long): SlidingWindowCounter {
            return SlidingWindowCounter(limit = ratePerMinute, windowSizeMs = 60_000L)
        }
    }
}

/**
 * 限流器工厂
 */
object RateLimiterFactory {
    
    /**
     * 创建令牌桶限流器
     * @param ratePerSecond 每秒令牌数
     * @param capacity 桶容量
     */
    fun tokenBucket(ratePerSecond: Long, capacity: Long = ratePerSecond): TokenBucket {
        return TokenBucket.create(ratePerSecond, capacity)
    }
    
    /**
     * 创建漏桶限流器
     * @param ratePerSecond 每秒处理请求数
     * @param capacity 桶容量
     */
    fun leakyBucket(ratePerSecond: Long, capacity: Long = ratePerSecond): LeakyBucket {
        return LeakyBucket.create(ratePerSecond, capacity)
    }
    
    /**
     * 创建固定窗口计数器限流器
     * @param limit 窗口内最大请求数
     * @param windowSizeMs 窗口大小（毫秒）
     */
    fun fixedWindow(limit: Long, windowSizeMs: Long): FixedWindowCounter {
        return FixedWindowCounter(limit, windowSizeMs)
    }
    
    /**
     * 创建每分钟限流的固定窗口计数器
     * @param ratePerMinute 每分钟最大请求数
     */
    fun fixedWindowPerMinute(ratePerMinute: Long): FixedWindowCounter {
        return FixedWindowCounter.create(ratePerMinute)
    }
    
    /**
     * 创建滑动窗口日志限流器
     * @param limit 窗口内最大请求数
     * @param windowSizeMs 窗口大小（毫秒）
     */
    fun slidingWindowLog(limit: Long, windowSizeMs: Long): SlidingWindowLog {
        return SlidingWindowLog(limit, windowSizeMs)
    }
    
    /**
     * 创建滑动窗口计数器限流器
     * @param limit 窗口内最大请求数
     * @param windowSizeMs 窗口大小（毫秒）
     */
    fun slidingWindowCounter(limit: Long, windowSizeMs: Long): SlidingWindowCounter {
        return SlidingWindowCounter(limit, windowSizeMs)
    }
    
    /**
     * 创建每分钟限流的滑动窗口计数器
     * @param ratePerMinute 每分钟最大请求数
     */
    fun slidingWindowPerMinute(ratePerMinute: Long): SlidingWindowCounter {
        return SlidingWindowCounter.create(ratePerMinute)
    }
}

/**
 * 限流器类型枚举
 */
enum class RateLimiterType {
    TOKEN_BUCKET,
    LEAKY_BUCKET,
    FIXED_WINDOW,
    SLIDING_WINDOW_LOG,
    SLIDING_WINDOW_COUNTER
}

/**
 * 通用限流器接口
 */
interface RateLimiter {
    fun tryAcquire(tokens: Long): RateLimitResult
}

/**
 * 分布式友好的限流器管理器
 */
class RateLimiterManager {
    private val limiters = ConcurrentHashMap<String, Any>()
    
    fun getTokenBucket(name: String): TokenBucket? {
        return limiters[name] as? TokenBucket
    }
    
    fun getLeakyBucket(name: String): LeakyBucket? {
        return limiters[name] as? LeakyBucket
    }
    
    fun getFixedWindow(name: String): FixedWindowCounter? {
        return limiters[name] as? FixedWindowCounter
    }
    
    fun getSlidingWindowLog(name: String): SlidingWindowLog? {
        return limiters[name] as? SlidingWindowLog
    }
    
    fun getSlidingWindowCounter(name: String): SlidingWindowCounter? {
        return limiters[name] as? SlidingWindowCounter
    }
    
    fun register(name: String, limiter: Any) {
        limiters[name] = limiter
    }
    
    fun unregister(name: String) {
        limiters.remove(name)
    }
    
    fun clear() {
        limiters.clear()
    }
}