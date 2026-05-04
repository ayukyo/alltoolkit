/**
 * 限流器工具集测试
 * 
 * 测试覆盖：
 * 1. 令牌桶限流器 - 基本功能、边界值、并发
 * 2. 漏桶限流器 - 基本功能、边界值
 * 3. 滑动窗口限流器 - 基本功能、窗口滚动
 * 4. 固定窗口限流器 - 基本功能、窗口重置
 * 5. 分布式限流器 - 多键限流
 * 6. 工厂方法 - 创建各种限流器
 * 7. 边界值测试 - 空值、极值、异常情况
 */

package ratelimiter;

import java.util.concurrent.CountDownLatch;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.util.concurrent.atomic.AtomicInteger;

public class RateLimiterTest {
    
    private static int passedTests = 0;
    private static int totalTests = 0;
    
    // ==================== 测试工具方法 ====================
    
    private static void test(String name, boolean condition) {
        totalTests++;
        if (condition) {
            passedTests++;
            System.out.println("  ✅ " + name);
        } else {
            System.out.println("  ❌ " + name);
        }
    }
    
    private static void testGroup(String name) {
        System.out.println("\n" + name);
    }
    
    // ==================== 令牌桶测试 ====================
    
    private static void testTokenBucket() {
        testGroup("=== 令牌桶限流器测试 ===");
        
        // 基本功能测试
        TokenBucket bucket = new TokenBucket(10, 5);
        test("初始令牌数为容量", bucket.getAvailableTokens() == 10);
        
        test("获取单个令牌成功", bucket.tryAcquire());
        test("获取后令牌数减少", bucket.getAvailableTokens() == 9);
        
        test("获取多个令牌成功", bucket.tryAcquire(5));
        test("获取后令牌数正确", bucket.getAvailableTokens() == 4);
        
        test("获取过多令牌失败", !bucket.tryAcquire(10));
        test("获取失败后令牌数不变", bucket.getAvailableTokens() == 4);
        
        // 重置测试
        bucket.reset();
        test("重置后令牌数为容量", bucket.getAvailableTokens() == 10);
        
        // 边界值测试
        TokenBucket smallBucket = new TokenBucket(1, 1);
        test("容量1的桶初始令牌为1", smallBucket.getAvailableTokens() == 1);
        test("获取1个令牌成功", smallBucket.tryAcquire());
        test("获取失败（无令牌）", !smallBucket.tryAcquire());
    }
    
    // ==================== 令牌桶参数验证测试 ====================
    
    private static void testTokenBucketValidation() {
        testGroup("=== 令牌桶参数验证测试 ===");
        
        boolean caught = false;
        try {
            new TokenBucket(0, 5);
        } catch (IllegalArgumentException e) {
            caught = true;
        }
        test("容量为0抛出异常", caught);
        
        caught = false;
        try {
            new TokenBucket(-1, 5);
        } catch (IllegalArgumentException e) {
            caught = true;
        }
        test("容量为负抛出异常", caught);
        
        caught = false;
        try {
            new TokenBucket(10, 0);
        } catch (IllegalArgumentException e) {
            caught = true;
        }
        test("补充速率为0抛出异常", caught);
        
        caught = false;
        try {
            new TokenBucket(10, -1);
        } catch (IllegalArgumentException e) {
            caught = true;
        }
        test("补充速率为负抛出异常", caught);
        
        TokenBucket bucket = new TokenBucket(10, 5);
        
        caught = false;
        try {
            bucket.tryAcquire(0);
        } catch (IllegalArgumentException e) {
            caught = true;
        }
        test("获取0个令牌抛出异常", caught);
        
        caught = false;
        try {
            bucket.tryAcquire(-1);
        } catch (IllegalArgumentException e) {
            caught = true;
        }
        test("获取负数令牌抛出异常", caught);
    }
    
    // ==================== 令牌桶并发测试 ====================
    
    private static void testTokenBucketConcurrency() throws InterruptedException {
        testGroup("=== 令牌桶并发测试 ===");
        
        // 低补充速率确保测试期间令牌不会被大量补充
        TokenBucket bucket = new TokenBucket(100, 1);
        int threadCount = 10;
        int requestsPerThread = 20;
        
        ExecutorService executor = Executors.newFixedThreadPool(threadCount);
        CountDownLatch latch = new CountDownLatch(threadCount);
        AtomicInteger successCount = new AtomicInteger(0);
        AtomicInteger failCount = new AtomicInteger(0);
        
        for (int i = 0; i < threadCount; i++) {
            executor.submit(() -> {
                try {
                    for (int j = 0; j < requestsPerThread; j++) {
                        if (bucket.tryAcquire()) {
                            successCount.incrementAndGet();
                        } else {
                            failCount.incrementAndGet();
                        }
                    }
                } finally {
                    latch.countDown();
                }
            });
        }
        
        latch.await();
        executor.shutdown();
        
        test("并发请求后成功数+失败数=总请求数", 
             successCount.get() + failCount.get() == threadCount * requestsPerThread);
        test("成功数不超过容量", successCount.get() <= 100);
    }
    
    // ==================== 漏桶测试 ====================
    
    private static void testLeakyBucket() {
        testGroup("=== 漏桶限流器测试 ===");
        
        // 基本功能测试
        LeakyBucket bucket = new LeakyBucket(10, 5);
        test("初始水量为0", bucket.getCurrentWater() == 0);
        
        test("添加单个请求成功", bucket.tryAcquire());
        test("添加后水量增加", bucket.getCurrentWater() == 1);
        
        test("添加多个请求成功", bucket.tryAcquire(5));
        test("水量正确", bucket.getCurrentWater() == 6);
        
        test("添加过多请求失败", !bucket.tryAcquire(10));
        test("水量不变", bucket.getCurrentWater() == 6);
        
        // 重置测试
        bucket.reset();
        test("重置后水量为0", bucket.getCurrentWater() == 0);
        
        // 边界值测试
        LeakyBucket smallBucket = new LeakyBucket(1, 1);
        test("容量1的桶初始水量为0", smallBucket.getCurrentWater() == 0);
        test("添加1个请求成功", smallBucket.tryAcquire());
        test("添加失败（桶满）", !smallBucket.tryAcquire());
    }
    
    // ==================== 漏桶参数验证测试 ====================
    
    private static void testLeakyBucketValidation() {
        testGroup("=== 漏桶参数验证测试 ===");
        
        boolean caught = false;
        try {
            new LeakyBucket(0, 5);
        } catch (IllegalArgumentException e) {
            caught = true;
        }
        test("容量为0抛出异常", caught);
        
        caught = false;
        try {
            new LeakyBucket(-1, 5);
        } catch (IllegalArgumentException e) {
            caught = true;
        }
        test("容量为负抛出异常", caught);
        
        caught = false;
        try {
            new LeakyBucket(10, 0);
        } catch (IllegalArgumentException e) {
            caught = true;
        }
        test("漏出速率为0抛出异常", caught);
        
        caught = false;
        try {
            new LeakyBucket(10, -1);
        } catch (IllegalArgumentException e) {
            caught = true;
        }
        test("漏出速率为负抛出异常", caught);
        
        LeakyBucket bucket = new LeakyBucket(10, 5);
        
        caught = false;
        try {
            bucket.tryAcquire(0);
        } catch (IllegalArgumentException e) {
            caught = true;
        }
        test("添加0个请求抛出异常", caught);
        
        caught = false;
        try {
            bucket.tryAcquire(-1);
        } catch (IllegalArgumentException e) {
            caught = true;
        }
        test("添加负数请求抛出异常", caught);
    }
    
    // ==================== 滑动窗口测试 ====================
    
    private static void testSlidingWindow() {
        testGroup("=== 滑动窗口限流器测试 ===");
        
        // 基本功能测试
        SlidingWindow window = new SlidingWindow(5, 1000);
        test("初始请求数为0", window.getCurrentCount() == 0);
        
        test("请求1通过", window.tryAcquire());
        test("请求2通过", window.tryAcquire());
        test("请求3通过", window.tryAcquire());
        test("请求4通过", window.tryAcquire());
        test("请求5通过", window.tryAcquire());
        test("当前请求数为5", window.getCurrentCount() == 5);
        
        test("请求6被限流", !window.tryAcquire());
        test("请求7被限流", !window.tryAcquire());
        
        // 重置测试
        window.reset();
        test("重置后请求数为0", window.getCurrentCount() == 0);
        test("重置后请求通过", window.tryAcquire());
    }
    
    // ==================== 滑动窗口参数验证测试 ====================
    
    private static void testSlidingWindowValidation() {
        testGroup("=== 滑动窗口参数验证测试 ===");
        
        boolean caught = false;
        try {
            new SlidingWindow(0, 1000);
        } catch (IllegalArgumentException e) {
            caught = true;
        }
        test("最大请求数为0抛出异常", caught);
        
        caught = false;
        try {
            new SlidingWindow(-1, 1000);
        } catch (IllegalArgumentException e) {
            caught = true;
        }
        test("最大请求数为负抛出异常", caught);
        
        caught = false;
        try {
            new SlidingWindow(10, 0);
        } catch (IllegalArgumentException e) {
            caught = true;
        }
        test("窗口大小为0抛出异常", caught);
        
        caught = false;
        try {
            new SlidingWindow(10, -1);
        } catch (IllegalArgumentException e) {
            caught = true;
        }
        test("窗口大小为负抛出异常", caught);
        
        SlidingWindow window = new SlidingWindow(10, 1000);
        
        caught = false;
        try {
            window.tryAcquire(0);
        } catch (IllegalArgumentException e) {
            caught = true;
        }
        test("请求0次抛出异常", caught);
        
        caught = false;
        try {
            window.tryAcquire(-1);
        } catch (IllegalArgumentException e) {
            caught = true;
        }
        test("请求负数次抛出异常", caught);
    }
    
    // ==================== 滑动窗口时间测试 ====================
    
    private static void testSlidingWindowTime() throws InterruptedException {
        testGroup("=== 滑动窗口时间测试 ===");
        
        SlidingWindow window = new SlidingWindow(3, 200); // 200ms 窗口
        
        test("请求1通过", window.tryAcquire());
        test("请求2通过", window.tryAcquire());
        test("请求3通过", window.tryAcquire());
        test("请求4被限流", !window.tryAcquire());
        
        // 等待窗口过期
        Thread.sleep(250);
        
        test("窗口过期后请求通过", window.tryAcquire());
        test("请求数正确", window.getCurrentCount() == 1);
    }
    
    // ==================== 固定窗口测试 ====================
    
    private static void testFixedWindow() {
        testGroup("=== 固定窗口限流器测试 ===");
        
        // 基本功能测试
        FixedWindow window = new FixedWindow(5, 1000);
        test("初始请求数为0", window.getCurrentCount() == 0);
        
        test("请求1通过", window.tryAcquire());
        test("请求2通过", window.tryAcquire());
        test("请求3通过", window.tryAcquire());
        test("请求4通过", window.tryAcquire());
        test("请求5通过", window.tryAcquire());
        test("当前请求数为5", window.getCurrentCount() == 5);
        
        test("请求6被限流", !window.tryAcquire());
        test("请求7被限流", !window.tryAcquire());
        
        // 剩余时间测试
        test("剩余时间大于0", window.getRemainingTime() > 0);
        test("剩余时间小于等于窗口大小", window.getRemainingTime() <= 1000);
        
        // 重置测试
        window.reset();
        test("重置后请求数为0", window.getCurrentCount() == 0);
        test("重置后请求通过", window.tryAcquire());
    }
    
    // ==================== 固定窗口参数验证测试 ====================
    
    private static void testFixedWindowValidation() {
        testGroup("=== 固定窗口参数验证测试 ===");
        
        boolean caught = false;
        try {
            new FixedWindow(0, 1000);
        } catch (IllegalArgumentException e) {
            caught = true;
        }
        test("最大请求数为0抛出异常", caught);
        
        caught = false;
        try {
            new FixedWindow(-1, 1000);
        } catch (IllegalArgumentException e) {
            caught = true;
        }
        test("最大请求数为负抛出异常", caught);
        
        caught = false;
        try {
            new FixedWindow(10, 0);
        } catch (IllegalArgumentException e) {
            caught = true;
        }
        test("窗口大小为0抛出异常", caught);
        
        caught = false;
        try {
            new FixedWindow(10, -1);
        } catch (IllegalArgumentException e) {
            caught = true;
        }
        test("窗口大小为负抛出异常", caught);
        
        FixedWindow window = new FixedWindow(10, 1000);
        
        caught = false;
        try {
            window.tryAcquire(0);
        } catch (IllegalArgumentException e) {
            caught = true;
        }
        test("请求0次抛出异常", caught);
        
        caught = false;
        try {
            window.tryAcquire(-1);
        } catch (IllegalArgumentException e) {
            caught = true;
        }
        test("请求负数次抛出异常", caught);
    }
    
    // ==================== 固定窗口时间测试 ====================
    
    private static void testFixedWindowTime() throws InterruptedException {
        testGroup("=== 固定窗口时间测试 ===");
        
        FixedWindow window = new FixedWindow(3, 200); // 200ms 窗口
        
        test("请求1通过", window.tryAcquire());
        test("请求2通过", window.tryAcquire());
        test("请求3通过", window.tryAcquire());
        test("请求4被限流", !window.tryAcquire());
        
        // 等待窗口过期
        Thread.sleep(250);
        
        test("窗口过期后请求通过", window.tryAcquire());
        test("请求数重置为1", window.getCurrentCount() == 1);
    }
    
    // ==================== 分布式限流器测试 ====================
    
    private static void testDistributedRateLimiter() {
        testGroup("=== 分布式限流器测试 ===");
        
        DistributedRateLimiter limiter = new DistributedRateLimiter(3, 1000);
        
        // 测试不同键
        test("IP1请求1通过", limiter.tryAcquire("192.168.1.1"));
        test("IP1请求2通过", limiter.tryAcquire("192.168.1.1"));
        test("IP1请求3通过", limiter.tryAcquire("192.168.1.1"));
        test("IP1请求4被限流", !limiter.tryAcquire("192.168.1.1"));
        
        test("IP2请求1通过", limiter.tryAcquire("192.168.1.2"));
        test("IP2请求2通过", limiter.tryAcquire("192.168.1.2"));
        test("IP2请求3通过", limiter.tryAcquire("192.168.1.2"));
        test("IP2请求4被限流", !limiter.tryAcquire("192.168.1.2"));
        
        // 活跃键数
        test("活跃键数为2", limiter.getActiveKeyCount() == 2);
        
        // 获取计数
        test("IP1当前请求数为3", limiter.getCurrentCount("192.168.1.1") == 3);
        test("IP2当前请求数为3", limiter.getCurrentCount("192.168.1.2") == 3);
        test("未知IP请求数为0", limiter.getCurrentCount("192.168.1.3") == 0);
        
        // 重置单个键
        limiter.reset("192.168.1.1");
        test("重置IP1后请求数为0", limiter.getCurrentCount("192.168.1.1") == 0);
        test("IP2请求数不变", limiter.getCurrentCount("192.168.1.2") == 3);
        
        // 重置所有
        limiter.resetAll();
        test("重置所有后活跃键数为0", limiter.getActiveKeyCount() == 0);
    }
    
    // ==================== 工厂方法测试 ====================
    
    private static void testFactory() {
        testGroup("=== 限流器工厂测试 ===");
        
        TokenBucket tokenBucket = RateLimiterFactory.createTokenBucket(10, 5);
        test("创建令牌桶成功", tokenBucket != null);
        test("令牌桶容量正确", tokenBucket.getAvailableTokens() == 10);
        
        LeakyBucket leakyBucket = RateLimiterFactory.createLeakyBucket(10, 5);
        test("创建漏桶成功", leakyBucket != null);
        test("漏桶水量正确", leakyBucket.getCurrentWater() == 0);
        
        SlidingWindow slidingWindow = RateLimiterFactory.createSlidingWindow(10, 1000);
        test("创建滑动窗口成功", slidingWindow != null);
        test("滑动窗口计数正确", slidingWindow.getCurrentCount() == 0);
        
        FixedWindow fixedWindow = RateLimiterFactory.createFixedWindow(10, 1000);
        test("创建固定窗口成功", fixedWindow != null);
        test("固定窗口计数正确", fixedWindow.getCurrentCount() == 0);
        
        DistributedRateLimiter distributed = RateLimiterFactory.createDistributed(10, 1000);
        test("创建分布式限流器成功", distributed != null);
        test("分布式限流器活跃键数为0", distributed.getActiveKeyCount() == 0);
        
        TokenBucket apiLimiter = RateLimiterFactory.createApiLimiter(100);
        test("创建API限流器成功", apiLimiter != null);
        test("API限流器容量正确", apiLimiter.getAvailableTokens() == 100);
        
        TokenBucket burstLimiter = RateLimiterFactory.createBurstLimiter(50, 10);
        test("创建突发限流器成功", burstLimiter != null);
        test("突发限流器容量正确", burstLimiter.getAvailableTokens() == 50);
    }
    
    // ==================== toString 测试 ====================
    
    private static void testToString() {
        testGroup("=== toString 测试 ===");
        
        TokenBucket tokenBucket = new TokenBucket(10, 5);
        String str = tokenBucket.toString();
        test("令牌桶toString包含容量", str.contains("capacity=10"));
        test("令牌桶toString包含速率", str.contains("rate=5"));
        
        LeakyBucket leakyBucket = new LeakyBucket(10, 5);
        str = leakyBucket.toString();
        test("漏桶toString包含容量", str.contains("capacity=10"));
        test("漏桶toString包含速率", str.contains("rate=5"));
        
        SlidingWindow slidingWindow = new SlidingWindow(5, 1000);
        str = slidingWindow.toString();
        test("滑动窗口toString包含最大值", str.contains("max=5"));
        test("滑动窗口toString包含窗口大小", str.contains("window=1000"));
        
        FixedWindow fixedWindow = new FixedWindow(5, 1000);
        str = fixedWindow.toString();
        test("固定窗口toString包含最大值", str.contains("max=5"));
        test("固定窗口toString包含窗口大小", str.contains("window=1000"));
    }
    
    // ==================== 边界值测试 ====================
    
    private static void testBoundaryValues() {
        testGroup("=== 边界值测试 ===");
        
        // 大容量测试
        TokenBucket bigBucket = new TokenBucket(1000000, 1000000);
        test("大容量令牌桶初始令牌正确", bigBucket.getAvailableTokens() == 1000000);
        test("大容量令牌桶获取成功", bigBucket.tryAcquire(999999));
        
        // 小窗口测试
        SlidingWindow smallWindow = new SlidingWindow(1, 1);
        test("1ms窗口请求通过", smallWindow.tryAcquire());
        test("1ms窗口第二请求被限流", !smallWindow.tryAcquire());
        
        // 大窗口测试
        FixedWindow bigWindow = new FixedWindow(1, Long.MAX_VALUE / 2);
        test("极大窗口请求通过", bigWindow.tryAcquire());
        test("极大窗口第二请求被限流", !bigWindow.tryAcquire());
        
        // 极速令牌桶
        TokenBucket fastBucket = new TokenBucket(1, Long.MAX_VALUE / 2);
        test("极速令牌桶初始正确", fastBucket.getAvailableTokens() == 1);
        test("极速令牌桶获取成功", fastBucket.tryAcquire());
    }
    
    // ==================== 主测试方法 ====================
    
    public static void main(String[] args) throws InterruptedException {
        System.out.println("╔════════════════════════════════════════════╗");
        System.out.println("║     限流器工具集测试 - Rate Limiter Test     ║");
        System.out.println("╚════════════════════════════════════════════╝");
        
        // 令牌桶测试
        testTokenBucket();
        testTokenBucketValidation();
        testTokenBucketConcurrency();
        
        // 漏桶测试
        testLeakyBucket();
        testLeakyBucketValidation();
        
        // 滑动窗口测试
        testSlidingWindow();
        testSlidingWindowValidation();
        testSlidingWindowTime();
        
        // 固定窗口测试
        testFixedWindow();
        testFixedWindowValidation();
        testFixedWindowTime();
        
        // 分布式限流器测试
        testDistributedRateLimiter();
        
        // 工厂方法测试
        testFactory();
        
        // toString 测试
        testToString();
        
        // 边界值测试
        testBoundaryValues();
        
        // 输出结果
        System.out.println("\n╔════════════════════════════════════════════╗");
        System.out.printf ("║  测试结果: %d/%d 通过", passedTests, totalTests);
        int spaces = 27 - String.format("%d/%d", passedTests, totalTests).length();
        for (int i = 0; i < spaces; i++) System.out.print(" ");
        System.out.println("║");
        System.out.println("╚════════════════════════════════════════════╝");
        
        if (passedTests == totalTests) {
            System.out.println("🎉 所有测试通过！");
        } else {
            System.out.println("⚠️ 有 " + (totalTests - passedTests) + " 个测试失败");
            System.exit(1);
        }
    }
}