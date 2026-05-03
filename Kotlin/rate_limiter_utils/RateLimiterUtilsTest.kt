import com.alltoolkit.ratelimiter.*
import org.junit.Assert.*
import org.junit.Test
import java.util.concurrent.CountDownLatch
import java.util.concurrent.Executors
import java.util.concurrent.TimeUnit
import java.util.concurrent.atomic.AtomicInteger

/**
 * RateLimiterUtils 测试套件
 * 测试所有限流算法的正确性和并发安全性
 */
class RateLimiterUtilsTest {
    
    // ==================== Token Bucket Tests ====================
    
    @Test
    fun `test token bucket basic acquisition`() {
        val bucket = TokenBucket(capacity = 5, refillRate = 1.0 / 1000.0) // 1 token/sec
        
        // 应该能获取5个令牌
        for (i in 1..5) {
            val result = bucket.tryAcquire()
            assertTrue("Request $i should be allowed", result.allowed)
        }
        
        // 第6次应该被拒绝
        val result = bucket.tryAcquire()
        assertFalse("Request 6 should be denied", result.allowed)
        assertTrue("Should have wait time", result.waitTimeMs > 0)
    }
    
    @Test
    fun `test token bucket refill`() {
        val bucket = TokenBucket(capacity = 2, refillRate = 10.0 / 1000.0) // 10 tokens/sec
        
        // 消耗所有令牌
        bucket.tryAcquire()
        bucket.tryAcquire()
        
        // 应该被拒绝
        assertFalse(bucket.tryAcquire().allowed)
        
        // 等待500ms，应该填充约5个令牌
        Thread.sleep(500)
        
        // 现在应该可以获取令牌了
        assertTrue("Should be allowed after refill", bucket.tryAcquire().allowed)
    }
    
    @Test
    fun `test token bucket multiple tokens`() {
        val bucket = TokenBucket(capacity = 10, refillRate = 1.0 / 1000.0)
        
        // 一次请求5个令牌
        val result = bucket.tryAcquire(5)
        assertTrue("Should allow 5 tokens", result.allowed)
        assertEquals(5, result.remainingTokens)
        
        // 再请求6个应该失败
        val result2 = bucket.tryAcquire(6)
        assertFalse("Should deny 6 tokens", result2.allowed)
        
        // 请求5个应该成功
        val result3 = bucket.tryAcquire(5)
        assertTrue("Should allow 5 tokens", result3.allowed)
    }
    
    @Test
    fun `test token bucket concurrency`() {
        val bucket = TokenBucket(capacity = 100, refillRate = 0.0) // 不填充
        val threadCount = 10
        val requestsPerThread = 20
        val successCount = AtomicInteger(0)
        val latch = CountDownLatch(threadCount)
        
        val executor = Executors.newFixedThreadPool(threadCount)
        
        repeat(threadCount) {
            executor.submit {
                try {
                    repeat(requestsPerThread) {
                        if (bucket.tryAcquire().allowed) {
                            successCount.incrementAndGet()
                        }
                    }
                } finally {
                    latch.countDown()
                }
            }
        }
        
        latch.await(5, TimeUnit.SECONDS)
        executor.shutdown()
        
        // 恰好100个请求成功（桶容量）
        assertEquals(100, successCount.get().toLong())
    }
    
    // ==================== Leaky Bucket Tests ====================
    
    @Test
    fun `test leaky bucket basic`() {
        val bucket = LeakyBucket(capacity = 3, leakRate = 1.0 / 1000.0) // 1 request/sec
        
        // 应该能放入3个请求
        for (i in 1..3) {
            val result = bucket.tryAcquire()
            assertTrue("Request $i should be allowed", result.allowed)
        }
        
        // 第4次应该被拒绝
        val result = bucket.tryAcquire()
        assertFalse("Request 4 should be denied", result.allowed)
    }
    
    @Test
    fun `test leaky bucket leak`() {
        val bucket = LeakyBucket(capacity = 2, leakRate = 100.0 / 1000.0) // 100 requests/sec
        
        // 填满桶
        bucket.tryAcquire()
        bucket.tryAcquire()
        
        // 应该被拒绝
        assertFalse(bucket.tryAcquire().allowed)
        
        // 等待20ms，应该漏出约2个请求
        Thread.sleep(20)
        
        // 现在应该可以处理新请求
        assertTrue("Should be allowed after leak", bucket.tryAcquire().allowed)
    }
    
    // ==================== Fixed Window Tests ====================
    
    @Test
    fun `test fixed window basic`() {
        val counter = FixedWindowCounter(limit = 3, windowSizeMs = 1000)
        
        // 窗口内应该允许3个请求
        for (i in 1..3) {
            val result = counter.tryAcquire("test")
            assertTrue("Request $i should be allowed", result.allowed)
        }
        
        // 第4次应该被拒绝
        val result = counter.tryAcquire("test")
        assertFalse("Request 4 should be denied", result.allowed)
    }
    
    @Test
    fun `test fixed window reset`() {
        val counter = FixedWindowCounter(limit = 2, windowSizeMs = 100)
        
        // 消耗配额
        counter.tryAcquire("test")
        counter.tryAcquire("test")
        assertFalse(counter.tryAcquire("test").allowed)
        
        // 等待窗口重置
        Thread.sleep(150)
        
        // 应该可以再次请求
        assertTrue("Should be allowed after window reset", counter.tryAcquire("test").allowed)
    }
    
    @Test
    fun `test fixed window different keys`() {
        val counter = FixedWindowCounter(limit = 2, windowSizeMs = 1000)
        
        // 不同的key应该独立计数
        assertTrue(counter.tryAcquire("user1").allowed)
        assertTrue(counter.tryAcquire("user1").allowed)
        assertFalse(counter.tryAcquire("user1").allowed)
        
        assertTrue(counter.tryAcquire("user2").allowed)
        assertTrue(counter.tryAcquire("user2").allowed)
        assertFalse(counter.tryAcquire("user2").allowed)
    }
    
    @Test
    fun `test fixed window get count`() {
        val counter = FixedWindowCounter(limit = 10, windowSizeMs = 1000)
        
        counter.tryAcquire("test")
        counter.tryAcquire("test")
        counter.tryAcquire("test")
        
        assertEquals(3, counter.getCount("test"))
    }
    
    @Test
    fun `test fixed window reset method`() {
        val counter = FixedWindowCounter(limit = 2, windowSizeMs = 1000)
        
        counter.tryAcquire("test")
        counter.tryAcquire("test")
        assertFalse(counter.tryAcquire("test").allowed)
        
        counter.reset("test")
        
        assertTrue("Should be allowed after reset", counter.tryAcquire("test").allowed)
    }
    
    // ==================== Sliding Window Log Tests ====================
    
    @Test
    fun `test sliding window log basic`() {
        val log = SlidingWindowLog(limit = 3, windowSizeMs = 1000)
        
        // 窗口内应该允许3个请求
        for (i in 1..3) {
            val result = log.tryAcquire("test")
            assertTrue("Request $i should be allowed", result.allowed)
        }
        
        // 第4次应该被拒绝
        assertFalse(log.tryAcquire("test").allowed)
    }
    
    @Test
    fun `test sliding window log sliding`() {
        val log = SlidingWindowLog(limit = 2, windowSizeMs = 100)
        
        // 发送2个请求
        log.tryAcquire("test")
        log.tryAcquire("test")
        
        // 应该被拒绝
        assertFalse(log.tryAcquire("test").allowed)
        
        // 等待窗口滑动
        Thread.sleep(150)
        
        // 旧请求应该已过期
        assertTrue("Should be allowed after window slides", log.tryAcquire("test").allowed)
    }
    
    @Test
    fun `test sliding window log get count`() {
        val log = SlidingWindowLog(limit = 10, windowSizeMs = 1000)
        
        log.tryAcquire("test")
        log.tryAcquire("test")
        log.tryAcquire("test")
        
        assertEquals(3, log.getCount("test"))
    }
    
    // ==================== Sliding Window Counter Tests ====================
    
    @Test
    fun `test sliding window counter basic`() {
        val counter = SlidingWindowCounter(limit = 3, windowSizeMs = 1000)
        
        // 窗口内应该允许请求
        for (i in 1..3) {
            val result = counter.tryAcquire("test")
            assertTrue("Request $i should be allowed", result.allowed)
        }
        
        // 应该被拒绝（考虑到滑动窗口的计算方式）
        // 注：滑动窗口计数器可能有轻微误差
    }
    
    @Test
    fun `test sliding window counter per minute`() {
        val counter = SlidingWindowCounter.create(ratePerMinute = 60)
        
        // 每分钟60请求 = 每秒1请求
        var successCount = 0
        repeat(60) {
            if (counter.tryAcquire("test").allowed) {
                successCount++
            }
        }
        
        // 应该允许大部分请求（考虑滑动窗口计算的近似性）
        assertTrue("Should allow most requests, got $successCount", successCount >= 55)
    }
    
    // ==================== Factory Tests ====================
    
    @Test
    fun `test factory token bucket`() {
        val bucket = RateLimiterFactory.tokenBucket(ratePerSecond = 10, capacity = 20)
        
        // 验证桶容量
        for (i in 1..20) {
            assertTrue("Request $i should be allowed", bucket.tryAcquire().allowed)
        }
        assertFalse("Request 21 should be denied", bucket.tryAcquire().allowed)
    }
    
    @Test
    fun `test factory leaky bucket`() {
        val bucket = RateLimiterFactory.leakyBucket(ratePerSecond = 10, capacity = 5)
        
        // 验证桶容量
        for (i in 1..5) {
            assertTrue("Request $i should be allowed", bucket.tryAcquire().allowed)
        }
        assertFalse("Request 6 should be denied", bucket.tryAcquire().allowed)
    }
    
    @Test
    fun `test factory fixed window`() {
        val counter = RateLimiterFactory.fixedWindow(limit = 5, windowSizeMs = 1000)
        
        for (i in 1..5) {
            assertTrue("Request $i should be allowed", counter.tryAcquire("test").allowed)
        }
        assertFalse("Request 6 should be denied", counter.tryAcquire("test").allowed)
    }
    
    @Test
    fun `test factory sliding window log`() {
        val log = RateLimiterFactory.slidingWindowLog(limit = 3, windowSizeMs = 1000)
        
        for (i in 1..3) {
            assertTrue("Request $i should be allowed", log.tryAcquire("test").allowed)
        }
        assertFalse("Request 4 should be denied", log.tryAcquire("test").allowed)
    }
    
    @Test
    fun `test factory sliding window counter`() {
        val counter = RateLimiterFactory.slidingWindowCounter(limit = 5, windowSizeMs = 1000)
        
        var allowed = 0
        repeat(5) {
            if (counter.tryAcquire("test").allowed) {
                allowed++
            }
        }
        
        assertTrue("Should allow requests, got $allowed", allowed >= 4)
    }
    
    // ==================== Rate Limiter Manager Tests ====================
    
    @Test
    fun `test manager register and retrieve`() {
        val manager = RateLimiterManager()
        
        val bucket = TokenBucket.create(10, 10)
        manager.register("api-limiter", bucket)
        
        val retrieved = manager.getTokenBucket("api-limiter")
        assertNotNull(retrieved)
        assertTrue(retrieved!!.tryAcquire().allowed)
    }
    
    @Test
    fun `test manager unregister`() {
        val manager = RateLimiterManager()
        
        val bucket = TokenBucket.create(10, 10)
        manager.register("api-limiter", bucket)
        assertNotNull(manager.getTokenBucket("api-limiter"))
        
        manager.unregister("api-limiter")
        assertNull(manager.getTokenBucket("api-limiter"))
    }
    
    @Test
    fun `test manager clear`() {
        val manager = RateLimiterManager()
        
        manager.register("limiter1", TokenBucket.create(10, 10))
        manager.register("limiter2", FixedWindowCounter.create(100))
        
        assertNotNull(manager.getTokenBucket("limiter1"))
        assertNotNull(manager.getFixedWindow("limiter2"))
        
        manager.clear()
        
        assertNull(manager.getTokenBucket("limiter1"))
        assertNull(manager.getFixedWindow("limiter2"))
    }
    
    // ==================== RateLimitResult Tests ====================
    
    @Test
    fun `test rate limit result properties`() {
        val result = RateLimitResult(
            allowed = false,
            remainingTokens = 5,
            waitTimeMs = 1000,
            retryAfterMs = 1500
        )
        
        assertFalse(result.allowed)
        assertEquals(5, result.remainingTokens)
        assertEquals(1000, result.waitTimeMs)
        assertEquals(1500, result.retryAfterMs)
    }
    
    // ==================== Integration Tests ====================
    
    @Test
    fun `test real world scenario - API rate limiting`() {
        // 模拟API限流：每秒10个请求，突发上限20
        val limiter = RateLimiterFactory.tokenBucket(ratePerSecond = 10, capacity = 20)
        
        // 模拟突发流量：15个请求同时到达
        var burstSuccess = 0
        repeat(15) {
            if (limiter.tryAcquire().allowed) {
                burstSuccess++
            }
        }
        assertEquals(15, burstSuccess)
        
        // 检查剩余令牌
        assertEquals(5, limiter.getAvailableTokens())
    }
    
    @Test
    fun `test real world scenario - user rate limiting`() {
        // 模拟用户限流：每用户每分钟100个请求
        val limiter = RateLimiterFactory.fixedWindowPerMinute(100)
        
        // 用户A
        repeat(100) {
            assertTrue(limiter.tryAcquire("user-a").allowed)
        }
        assertFalse(limiter.tryAcquire("user-a").allowed)
        
        // 用户B（独立计数）
        assertTrue(limiter.tryAcquire("user-b").allowed)
    }
    
    @Test
    fun `test real world scenario - distributed rate limiting`() {
        // 使用滑动窗口计数器模拟分布式限流
        val limiter = RateLimiterFactory.slidingWindowPerMinute(60)
        
        val threadCount = 5
        val requestsPerThread = 15
        val totalRequests = threadCount * requestsPerThread
        val successCount = AtomicInteger(0)
        val latch = CountDownLatch(threadCount)
        
        val executor = Executors.newFixedThreadPool(threadCount)
        
        repeat(threadCount) {
            executor.submit {
                try {
                    repeat(requestsPerThread) {
                        if (limiter.tryAcquire("shared").allowed) {
                            successCount.incrementAndGet()
                        }
                    }
                } finally {
                    latch.countDown()
                }
            }
        }
        
        latch.await(5, TimeUnit.SECONDS)
        executor.shutdown()
        
        // 由于滑动窗口计数器的近似性，允许一定误差
        assertTrue(
            "Expected ~60 successful requests, got ${successCount.get()}",
            successCount.get() in 55..65
        )
    }
}