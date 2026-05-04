/**
 * 限流器工具集 - Rate Limiter Utils
 * 
 * 提供多种限流算法实现，用于 API 限流、请求控制等场景。
 * 零外部依赖，纯 Java 标准库实现。
 * 
 * 支持的算法：
 * 1. 令牌桶 (Token Bucket) - 允许突发流量，平滑限流
 * 2. 漏桶 (Leaky Bucket) - 恒定速率输出，削峰填谷
 * 3. 滑动窗口 (Sliding Window) - 精确限流，无边界问题
 * 4. 固定窗口 (Fixed Window) - 简单高效，可能有边界问题
 * 
 * @author AllToolkit
 * @version 1.0.0
 */

package ratelimiter;

import java.util.concurrent.ConcurrentHashMap;
import java.util.concurrent.ConcurrentLinkedQueue;
import java.util.concurrent.atomic.AtomicInteger;
import java.util.concurrent.atomic.AtomicLong;
import java.util.concurrent.locks.ReentrantLock;

// ==================== 令牌桶限流器 ====================

/**
 * 令牌桶限流器
 * 
 * 原理：以恒定速率往桶中放入令牌，请求需要获取令牌才能通过。
 * 允许一定程度的突发流量（桶中有存量令牌时）。
 * 
 * 特点：
 * - 平滑限流
 * - 允许突发流量
 * - 适合有波动的流量场景
 */
class TokenBucket {
    private final long capacity;           // 桶容量
    private final long refillRate;          // 令牌补充速率（令牌/秒）
    private final AtomicLong tokens;        // 当前令牌数
    private final AtomicLong lastRefillTime; // 上次补充时间
    private final ReentrantLock lock = new ReentrantLock();
    
    /**
     * 创建令牌桶限流器
     * 
     * @param capacity 桶容量（最大令牌数）
     * @param refillRate 令牌补充速率（令牌/秒）
     */
    public TokenBucket(long capacity, long refillRate) {
        if (capacity <= 0) {
            throw new IllegalArgumentException("容量必须大于 0");
        }
        if (refillRate <= 0) {
            throw new IllegalArgumentException("补充速率必须大于 0");
        }
        
        this.capacity = capacity;
        this.refillRate = refillRate;
        this.tokens = new AtomicLong(capacity);
        this.lastRefillTime = new AtomicLong(System.nanoTime());
    }
    
    /**
     * 尝试获取令牌
     * 
     * @return true 如果获取成功，false 如果被限流
     */
    public boolean tryAcquire() {
        return tryAcquire(1);
    }
    
    /**
     * 尝试获取指定数量的令牌
     * 
     * @param requestedTokens 请求的令牌数
     * @return true 如果获取成功，false 如果被限流
     */
    public boolean tryAcquire(long requestedTokens) {
        if (requestedTokens <= 0) {
            throw new IllegalArgumentException("请求令牌数必须大于 0");
        }
        
        lock.lock();
        try {
            refill();
            
            if (tokens.get() >= requestedTokens) {
                tokens.addAndGet(-requestedTokens);
                return true;
            }
            return false;
        } finally {
            lock.unlock();
        }
    }
    
    /**
     * 补充令牌
     */
    private void refill() {
        long now = System.nanoTime();
        long elapsedTime = now - lastRefillTime.get();
        
        if (elapsedTime > 0) {
            // 计算应该补充的令牌数
            long tokensToAdd = (elapsedTime * refillRate) / 1_000_000_000L;
            
            if (tokensToAdd > 0) {
                long newTokens = Math.min(capacity, tokens.get() + tokensToAdd);
                tokens.set(newTokens);
                lastRefillTime.set(now);
            }
        }
    }
    
    /**
     * 获取当前可用令牌数
     */
    public long getAvailableTokens() {
        lock.lock();
        try {
            refill();
            return tokens.get();
        } finally {
            lock.unlock();
        }
    }
    
    /**
     * 重置令牌桶
     */
    public void reset() {
        lock.lock();
        try {
            tokens.set(capacity);
            lastRefillTime.set(System.nanoTime());
        } finally {
            lock.unlock();
        }
    }
    
    @Override
    public String toString() {
        return String.format("TokenBucket[capacity=%d, rate=%d/s, available=%d]",
                capacity, refillRate, getAvailableTokens());
    }
}

// ==================== 漏桶限流器 ====================

/**
 * 漏桶限流器
 * 
 * 原理：请求以任意速率进入桶中，桶以恒定速率漏出请求。
 * 桶满时新请求被拒绝。
 * 
 * 特点：
 * - 恒定输出速率
 * - 削峰填谷
 * - 适合需要稳定输出的场景
 */
class LeakyBucket {
    private final long capacity;           // 桶容量
    private final long leakRate;            // 漏出速率（请求/秒）
    private final AtomicLong water;         // 当前水量（待处理请求数）
    private final AtomicLong lastLeakTime;  // 上次漏出时间
    private final ReentrantLock lock = new ReentrantLock();
    
    /**
     * 创建漏桶限流器
     * 
     * @param capacity 桶容量
     * @param leakRate 漏出速率（请求/秒）
     */
    public LeakyBucket(long capacity, long leakRate) {
        if (capacity <= 0) {
            throw new IllegalArgumentException("容量必须大于 0");
        }
        if (leakRate <= 0) {
            throw new IllegalArgumentException("漏出速率必须大于 0");
        }
        
        this.capacity = capacity;
        this.leakRate = leakRate;
        this.water = new AtomicLong(0);
        this.lastLeakTime = new AtomicLong(System.nanoTime());
    }
    
    /**
     * 尝试添加请求
     * 
     * @return true 如果添加成功，false 如果桶已满
     */
    public boolean tryAcquire() {
        return tryAcquire(1);
    }
    
    /**
     * 尝试添加指定数量的请求
     * 
     * @param requests 请求数量
     * @return true 如果添加成功，false 如果桶已满
     */
    public boolean tryAcquire(long requests) {
        if (requests <= 0) {
            throw new IllegalArgumentException("请求数必须大于 0");
        }
        
        lock.lock();
        try {
            leak();
            
            if (water.get() + requests <= capacity) {
                water.addAndGet(requests);
                return true;
            }
            return false;
        } finally {
            lock.unlock();
        }
    }
    
    /**
     * 漏出请求
     */
    private void leak() {
        long now = System.nanoTime();
        long elapsedTime = now - lastLeakTime.get();
        
        if (elapsedTime > 0) {
            // 计算应该漏出的请求数
            long leaked = (elapsedTime * leakRate) / 1_000_000_000L;
            
            if (leaked > 0) {
                long newWater = Math.max(0, water.get() - leaked);
                water.set(newWater);
                lastLeakTime.set(now);
            }
        }
    }
    
    /**
     * 获取当前水量（待处理请求数）
     */
    public long getCurrentWater() {
        lock.lock();
        try {
            leak();
            return water.get();
        } finally {
            lock.unlock();
        }
    }
    
    /**
     * 重置漏桶
     */
    public void reset() {
        lock.lock();
        try {
            water.set(0);
            lastLeakTime.set(System.nanoTime());
        } finally {
            lock.unlock();
        }
    }
    
    @Override
    public String toString() {
        return String.format("LeakyBucket[capacity=%d, rate=%d/s, water=%d]",
                capacity, leakRate, getCurrentWater());
    }
}

// ==================== 滑动窗口限流器 ====================

/**
 * 滑动窗口限流器
 * 
 * 原理：维护一个时间窗口内的请求记录，精确统计当前窗口内的请求数。
 * 
 * 特点：
 * - 精确限流
 * - 无边界问题
 * - 内存占用较高
 */
class SlidingWindow {
    private final long maxRequests;        // 最大请求数
    private final long windowSizeMillis;   // 窗口大小（毫秒）
    private final ConcurrentLinkedQueue<Long> timestamps; // 请求时间戳队列
    private final ReentrantLock lock = new ReentrantLock();
    
    /**
     * 创建滑动窗口限流器
     * 
     * @param maxRequests 窗口内最大请求数
     * @param windowSizeMillis 窗口大小（毫秒）
     */
    public SlidingWindow(long maxRequests, long windowSizeMillis) {
        if (maxRequests <= 0) {
            throw new IllegalArgumentException("最大请求数必须大于 0");
        }
        if (windowSizeMillis <= 0) {
            throw new IllegalArgumentException("窗口大小必须大于 0");
        }
        
        this.maxRequests = maxRequests;
        this.windowSizeMillis = windowSizeMillis;
        this.timestamps = new ConcurrentLinkedQueue<>();
    }
    
    /**
     * 尝试通过请求
     * 
     * @return true 如果通过，false 如果被限流
     */
    public boolean tryAcquire() {
        return tryAcquire(1);
    }
    
    /**
     * 尝试通过指定数量的请求
     * 
     * @param requests 请求数量
     * @return true 如果通过，false 如果被限流
     */
    public boolean tryAcquire(long requests) {
        if (requests <= 0) {
            throw new IllegalArgumentException("请求数必须大于 0");
        }
        
        lock.lock();
        try {
            long now = System.currentTimeMillis();
            long windowStart = now - windowSizeMillis;
            
            // 移除过期的请求记录
            while (!timestamps.isEmpty() && timestamps.peek() < windowStart) {
                timestamps.poll();
            }
            
            // 检查是否可以添加新请求
            if (timestamps.size() + requests <= maxRequests) {
                for (long i = 0; i < requests; i++) {
                    timestamps.offer(now);
                }
                return true;
            }
            return false;
        } finally {
            lock.unlock();
        }
    }
    
    /**
     * 获取当前窗口内的请求数
     */
    public long getCurrentCount() {
        lock.lock();
        try {
            long now = System.currentTimeMillis();
            long windowStart = now - windowSizeMillis;
            
            // 移除过期的请求记录
            while (!timestamps.isEmpty() && timestamps.peek() < windowStart) {
                timestamps.poll();
            }
            
            return timestamps.size();
        } finally {
            lock.unlock();
        }
    }
    
    /**
     * 重置滑动窗口
     */
    public void reset() {
        lock.lock();
        try {
            timestamps.clear();
        } finally {
            lock.unlock();
        }
    }
    
    @Override
    public String toString() {
        return String.format("SlidingWindow[max=%d, window=%dms, current=%d]",
                maxRequests, windowSizeMillis, getCurrentCount());
    }
}

// ==================== 固定窗口限流器 ====================

/**
 * 固定窗口限流器
 * 
 * 原理：在固定时间窗口内计数，窗口结束时重置计数器。
 * 
 * 特点：
 * - 简单高效
 * - 可能有边界问题（窗口边界突发）
 * - 内存占用低
 */
class FixedWindow {
    private final long maxRequests;        // 最大请求数
    private final long windowSizeMillis;   // 窗口大小（毫秒）
    private final AtomicInteger counter;    // 请求计数器
    private final AtomicLong windowStart;   // 窗口开始时间
    
    /**
     * 创建固定窗口限流器
     * 
     * @param maxRequests 窗口内最大请求数
     * @param windowSizeMillis 窗口大小（毫秒）
     */
    public FixedWindow(long maxRequests, long windowSizeMillis) {
        if (maxRequests <= 0) {
            throw new IllegalArgumentException("最大请求数必须大于 0");
        }
        if (windowSizeMillis <= 0) {
            throw new IllegalArgumentException("窗口大小必须大于 0");
        }
        
        this.maxRequests = maxRequests;
        this.windowSizeMillis = windowSizeMillis;
        this.counter = new AtomicInteger(0);
        this.windowStart = new AtomicLong(System.currentTimeMillis());
    }
    
    /**
     * 尝试通过请求
     * 
     * @return true 如果通过，false 如果被限流
     */
    public boolean tryAcquire() {
        return tryAcquire(1);
    }
    
    /**
     * 尝试通过指定数量的请求
     * 
     * @param requests 请求数量
     * @return true 如果通过，false 如果被限流
     */
    public boolean tryAcquire(long requests) {
        if (requests <= 0) {
            throw new IllegalArgumentException("请求数必须大于 0");
        }
        
        long now = System.currentTimeMillis();
        
        // 检查是否需要重置窗口
        synchronized (this) {
            if (now - windowStart.get() >= windowSizeMillis) {
                windowStart.set(now);
                counter.set(0);
            }
            
            // 检查是否可以添加新请求
            if (counter.get() + requests <= maxRequests) {
                counter.addAndGet((int) requests);
                return true;
            }
            return false;
        }
    }
    
    /**
     * 获取当前窗口内的请求数
     */
    public int getCurrentCount() {
        long now = System.currentTimeMillis();
        
        synchronized (this) {
            if (now - windowStart.get() >= windowSizeMillis) {
                return 0;
            }
            return counter.get();
        }
    }
    
    /**
     * 重置固定窗口
     */
    public void reset() {
        synchronized (this) {
            counter.set(0);
            windowStart.set(System.currentTimeMillis());
        }
    }
    
    /**
     * 获取当前窗口剩余时间（毫秒）
     */
    public long getRemainingTime() {
        long elapsed = System.currentTimeMillis() - windowStart.get();
        return Math.max(0, windowSizeMillis - elapsed);
    }
    
    @Override
    public String toString() {
        return String.format("FixedWindow[max=%d, window=%dms, current=%d]",
                maxRequests, windowSizeMillis, getCurrentCount());
    }
}

// ==================== 分布式限流器（基于 IP/用户） ====================

/**
 * 分布式限流器
 * 
 * 为不同的键（如 IP 地址、用户 ID）提供独立的限流实例。
 */
class DistributedRateLimiter {
    private final ConcurrentHashMap<String, SlidingWindow> limiters;
    private final long maxRequests;
    private final long windowSizeMillis;
    
    /**
     * 创建分布式限流器
     * 
     * @param maxRequests 每个键的最大请求数
     * @param windowSizeMillis 窗口大小（毫秒）
     */
    public DistributedRateLimiter(long maxRequests, long windowSizeMillis) {
        this.limiters = new ConcurrentHashMap<>();
        this.maxRequests = maxRequests;
        this.windowSizeMillis = windowSizeMillis;
    }
    
    /**
     * 尝试为指定键通过请求
     * 
     * @param key 限流键（如 IP 地址、用户 ID）
     * @return true 如果通过，false 如果被限流
     */
    public boolean tryAcquire(String key) {
        SlidingWindow limiter = limiters.computeIfAbsent(key,
                k -> new SlidingWindow(maxRequests, windowSizeMillis));
        return limiter.tryAcquire();
    }
    
    /**
     * 获取指定键的当前请求数
     */
    public long getCurrentCount(String key) {
        SlidingWindow limiter = limiters.get(key);
        return limiter != null ? limiter.getCurrentCount() : 0;
    }
    
    /**
     * 重置指定键的限流器
     */
    public void reset(String key) {
        SlidingWindow limiter = limiters.get(key);
        if (limiter != null) {
            limiter.reset();
        }
    }
    
    /**
     * 重置所有限流器
     */
    public void resetAll() {
        limiters.clear();
    }
    
    /**
     * 获取活跃键数量
     */
    public int getActiveKeyCount() {
        return limiters.size();
    }
    
    /**
     * 清理不活跃的限流器
     * 
     * @param maxInactiveMillis 最大不活跃时间（毫秒）
     */
    public void cleanup(long maxInactiveMillis) {
        // 注意：这里简化实现，实际应用中需要记录每个键的最后访问时间
        // 当前实现仅作为示例
    }
}

// ==================== 限流器工厂 ====================

/**
 * 限流器工厂
 * 
 * 提供便捷的限流器创建方法。
 */
class RateLimiterFactory {
    
    /**
     * 创建令牌桶限流器
     * 
     * @param capacity 桶容量
     * @param refillRate 补充速率（令牌/秒）
     */
    public static TokenBucket createTokenBucket(long capacity, long refillRate) {
        return new TokenBucket(capacity, refillRate);
    }
    
    /**
     * 创建漏桶限流器
     * 
     * @param capacity 桶容量
     * @param leakRate 漏出速率（请求/秒）
     */
    public static LeakyBucket createLeakyBucket(long capacity, long leakRate) {
        return new LeakyBucket(capacity, leakRate);
    }
    
    /**
     * 创建滑动窗口限流器
     * 
     * @param maxRequests 最大请求数
     * @param windowSizeMillis 窗口大小（毫秒）
     */
    public static SlidingWindow createSlidingWindow(long maxRequests, long windowSizeMillis) {
        return new SlidingWindow(maxRequests, windowSizeMillis);
    }
    
    /**
     * 创建固定窗口限流器
     * 
     * @param maxRequests 最大请求数
     * @param windowSizeMillis 窗口大小（毫秒）
     */
    public static FixedWindow createFixedWindow(long maxRequests, long windowSizeMillis) {
        return new FixedWindow(maxRequests, windowSizeMillis);
    }
    
    /**
     * 创建分布式限流器
     * 
     * @param maxRequests 每个键的最大请求数
     * @param windowSizeMillis 窗口大小（毫秒）
     */
    public static DistributedRateLimiter createDistributed(long maxRequests, long windowSizeMillis) {
        return new DistributedRateLimiter(maxRequests, windowSizeMillis);
    }
    
    /**
     * 创建 API 限流器（预设配置）
     * 
     * @param requestsPerSecond 每秒请求数
     */
    public static TokenBucket createApiLimiter(long requestsPerSecond) {
        return new TokenBucket(requestsPerSecond, requestsPerSecond);
    }
    
    /**
     * 创建突发流量限流器（允许突发）
     * 
     * @param burstSize 突发大小
     * @param averageRate 平均速率（请求/秒）
     */
    public static TokenBucket createBurstLimiter(long burstSize, long averageRate) {
        return new TokenBucket(burstSize, averageRate);
    }
}

// ==================== 主类 ====================

/**
 * 限流器工具集主类
 */
public class mod {
    
    /**
     * 演示各种限流器的使用
     */
    public static void main(String[] args) throws InterruptedException {
        System.out.println("=== 限流器工具集演示 ===\n");
        
        // 1. 令牌桶限流器
        System.out.println("1. 令牌桶限流器 (Token Bucket)");
        System.out.println("   容量: 10, 补充速率: 5/秒");
        TokenBucket tokenBucket = RateLimiterFactory.createTokenBucket(10, 5);
        
        System.out.println("   初始令牌: " + tokenBucket.getAvailableTokens());
        System.out.println("   尝试获取 3 个令牌: " + tokenBucket.tryAcquire(3));
        System.out.println("   剩余令牌: " + tokenBucket.getAvailableTokens());
        System.out.println("   尝试获取 8 个令牌: " + tokenBucket.tryAcquire(8));
        System.out.println("   剩余令牌: " + tokenBucket.getAvailableTokens());
        System.out.println();
        
        // 2. 漏桶限流器
        System.out.println("2. 漏桶限流器 (Leaky Bucket)");
        System.out.println("   容量: 10, 漏出速率: 3/秒");
        LeakyBucket leakyBucket = RateLimiterFactory.createLeakyBucket(10, 3);
        
        System.out.println("   初始水量: " + leakyBucket.getCurrentWater());
        System.out.println("   添加 5 个请求: " + leakyBucket.tryAcquire(5));
        System.out.println("   当前水量: " + leakyBucket.getCurrentWater());
        System.out.println("   添加 6 个请求: " + leakyBucket.tryAcquire(6));
        System.out.println("   当前水量: " + leakyBucket.getCurrentWater());
        System.out.println();
        
        // 3. 滑动窗口限流器
        System.out.println("3. 滑动窗口限流器 (Sliding Window)");
        System.out.println("   最大请求: 5, 窗口: 1秒");
        SlidingWindow slidingWindow = RateLimiterFactory.createSlidingWindow(5, 1000);
        
        for (int i = 1; i <= 7; i++) {
            boolean allowed = slidingWindow.tryAcquire();
            System.out.println("   请求 " + i + ": " + (allowed ? "通过" : "被限流") + 
                             " (当前: " + slidingWindow.getCurrentCount() + ")");
        }
        System.out.println();
        
        // 4. 固定窗口限流器
        System.out.println("4. 固定窗口限流器 (Fixed Window)");
        System.out.println("   最大请求: 5, 窗口: 1秒");
        FixedWindow fixedWindow = RateLimiterFactory.createFixedWindow(5, 1000);
        
        for (int i = 1; i <= 7; i++) {
            boolean allowed = fixedWindow.tryAcquire();
            System.out.println("   请求 " + i + ": " + (allowed ? "通过" : "被限流") + 
                             " (当前: " + fixedWindow.getCurrentCount() + 
                             ", 剩余时间: " + fixedWindow.getRemainingTime() + "ms)");
        }
        System.out.println();
        
        // 5. 分布式限流器
        System.out.println("5. 分布式限流器 (按 IP 限流)");
        System.out.println("   每个IP最大请求: 3, 窗口: 1秒");
        DistributedRateLimiter distributed = RateLimiterFactory.createDistributed(3, 1000);
        
        String[] ips = {"192.168.1.1", "192.168.1.2", "192.168.1.1"};
        for (int i = 0; i < ips.length; i++) {
            for (int j = 1; j <= 4; j++) {
                boolean allowed = distributed.tryAcquire(ips[i]);
                System.out.println("   IP " + ips[i] + " 请求 " + j + 
                                 ": " + (allowed ? "通过" : "被限流"));
            }
            System.out.println("   ---");
        }
        System.out.println("   活跃IP数: " + distributed.getActiveKeyCount());
        System.out.println();
        
        // 6. 突发流量限流器
        System.out.println("6. 突发流量限流器");
        System.out.println("   突发容量: 20, 平均速率: 5/秒");
        TokenBucket burstLimiter = RateLimiterFactory.createBurstLimiter(20, 5);
        
        System.out.println("   初始令牌: " + burstLimiter.getAvailableTokens());
        System.out.println("   突发 15 个请求: " + burstLimiter.tryAcquire(15));
        System.out.println("   剩余令牌: " + burstLimiter.getAvailableTokens());
        System.out.println("   再突发 10 个请求: " + burstLimiter.tryAcquire(10));
        System.out.println("   剩余令牌: " + burstLimiter.getAvailableTokens());
        
        System.out.println("\n=== 演示完成 ===");
    }
}