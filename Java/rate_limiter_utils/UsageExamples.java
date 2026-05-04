/**
 * 限流器工具集使用示例
 * 
 * 展示各种实际应用场景：
 * 1. API 限流
 * 2. 用户请求控制
 * 3. IP 黑白名单
 * 4. 突发流量处理
 * 5. 系统资源保护
 */

package ratelimiter;

import java.util.concurrent.CountDownLatch;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.util.concurrent.atomic.AtomicInteger;

public class UsageExamples {
    
    /**
     * 示例 1: API 限流
     * 保护 API 不被过载请求
     */
    public static void apiRateLimiting() {
        System.out.println("\n=== 示例 1: API 限流 ===");
        System.out.println("场景: 限制 API 每秒最多 100 个请求\n");
        
        // 创建限流器：每秒 100 个请求
        TokenBucket apiLimiter = RateLimiterFactory.createApiLimiter(100);
        
        // 模拟 150 个请求
        int allowedCount = 0;
        int deniedCount = 0;
        
        for (int i = 1; i <= 150; i++) {
            if (apiLimiter.tryAcquire()) {
                allowedCount++;
                System.out.println("  请求 " + i + ": ✅ 通过");
            } else {
                deniedCount++;
                System.out.println("  请求 " + i + ": ❌ 被限流 (429 Too Many Requests)");
            }
        }
        
        System.out.println("\n  统计:");
        System.out.println("    - 通过: " + allowedCount + " 个请求");
        System.out.println("    - 拒绝: " + deniedCount + " 个请求");
        System.out.println("    - 剩余令牌: " + apiLimiter.getAvailableTokens());
    }
    
    /**
     * 示例 2: 用户请求控制
     * 防止单个用户过度使用资源
     */
    public static void userRateLimiting() {
        System.out.println("\n=== 示例 2: 用户请求控制 ===");
        System.out.println("场景: 每个用户每分钟最多 60 个请求\n");
        
        // 创建分布式限流器：每分钟 60 个请求
        DistributedRateLimiter userLimiter = RateLimiterFactory.createDistributed(60, 60000);
        
        String[] users = {"alice", "bob", "alice", "charlie", "alice"};
        
        for (int i = 0; i < users.length; i++) {
            String user = users[i];
            boolean allowed = userLimiter.tryAcquire(user);
            long count = userLimiter.getCurrentCount(user);
            
            System.out.printf("  用户 %-8s 请求: %s (当前计数: %d)%n",
                    user, allowed ? "✅ 通过" : "❌ 被限流", count);
        }
        
        System.out.println("\n  用户统计:");
        System.out.println("    - 活跃用户数: " + userLimiter.getActiveKeyCount());
        System.out.println("    - Alice 请求数: " + userLimiter.getCurrentCount("alice"));
    }
    
    /**
     * 示例 3: IP 限流
     * 防止恶意 IP 攻击
     */
    public static void ipRateLimiting() {
        System.out.println("\n=== 示例 3: IP 限流 ===");
        System.out.println("场景: 每个 IP 每秒最多 10 个请求\n");
        
        // 创建分布式限流器：每秒 10 个请求
        DistributedRateLimiter ipLimiter = RateLimiterFactory.createDistributed(10, 1000);
        
        // 模拟多个 IP 的请求
        String[] ips = {
            "192.168.1.100",
            "192.168.1.100",
            "192.168.1.100",
            "10.0.0.50",
            "192.168.1.100",
            "10.0.0.50",
            "192.168.1.100",
            "172.16.0.1"
        };
        
        for (int i = 0; i < ips.length; i++) {
            String ip = ips[i];
            boolean allowed = ipLimiter.tryAcquire(ip);
            long count = ipLimiter.getCurrentCount(ip);
            
            System.out.printf("  IP %-15s 请求: %s (计数: %d)%n",
                    ip, allowed ? "✅ 通过" : "❌ 被限流", count);
        }
        
        System.out.println("\n  安全统计:");
        System.out.println("    - 活跃 IP 数: " + ipLimiter.getActiveKeyCount());
    }
    
    /**
     * 示例 4: 突发流量处理
     * 允许一定程度的突发流量
     */
    public static void burstTrafficHandling() {
        System.out.println("\n=== 示例 4: 突发流量处理 ===");
        System.out.println("场景: 允许突发 50 个请求，平均 10 个/秒\n");
        
        // 创建突发限流器：突发容量 50，平均速率 10/秒
        TokenBucket burstLimiter = RateLimiterFactory.createBurstLimiter(50, 10);
        
        System.out.println("  初始令牌: " + burstLimiter.getAvailableTokens());
        
        // 模拟突发流量
        System.out.println("\n  突发 30 个请求...");
        int success1 = 0;
        for (int i = 0; i < 30; i++) {
            if (burstLimiter.tryAcquire()) success1++;
        }
        System.out.println("  成功: " + success1 + " 个");
        System.out.println("  剩余令牌: " + burstLimiter.getAvailableTokens());
        
        // 继续请求
        System.out.println("\n  继续请求 25 个...");
        int success2 = 0;
        for (int i = 0; i < 25; i++) {
            if (burstLimiter.tryAcquire()) success2++;
        }
        System.out.println("  成功: " + success2 + " 个");
        System.out.println("  剩余令牌: " + burstLimiter.getAvailableTokens());
    }
    
    /**
     * 示例 5: 系统资源保护
     * 保护数据库、外部服务等
     */
    public static void resourceProtection() {
        System.out.println("\n=== 示例 5: 系统资源保护 ===");
        System.out.println("场景: 数据库查询限制每秒 50 次\n");
        
        // 创建漏桶限流器：恒定速率输出
        LeakyBucket dbLimiter = RateLimiterFactory.createLeakyBucket(100, 50);
        
        System.out.println("  数据库限流器配置:");
        System.out.println("    - 队列容量: 100");
        System.out.println("    - 处理速率: 50/秒");
        
        // 模拟请求
        System.out.println("\n  处理请求...");
        for (int i = 1; i <= 5; i++) {
            boolean accepted = dbLimiter.tryAcquire();
            System.out.printf("    请求 %d: %s (队列: %d)%n",
                    i, accepted ? "✅ 接受" : "❌ 拒绝", dbLimiter.getCurrentWater());
        }
        
        // 模拟大量请求
        System.out.println("\n  批量请求 120 个...");
        int accepted = 0, rejected = 0;
        for (int i = 0; i < 120; i++) {
            if (dbLimiter.tryAcquire()) {
                accepted++;
            } else {
                rejected++;
            }
        }
        System.out.println("    - 接受: " + accepted);
        System.out.println("    - 拒绝: " + rejected);
        System.out.println("    - 当前队列: " + dbLimiter.getCurrentWater());
    }
    
    /**
     * 示例 6: 多级限流
     * 全局 + 用户级别限流
     */
    public static void multiLevelRateLimiting() {
        System.out.println("\n=== 示例 6: 多级限流 ===");
        System.out.println("场景: 全局 1000/秒 + 单用户 10/秒\n");
        
        // 全局限流器
        TokenBucket globalLimiter = RateLimiterFactory.createApiLimiter(1000);
        
        // 用户限流器
        DistributedRateLimiter userLimiter = RateLimiterFactory.createDistributed(10, 1000);
        
        // 模拟请求
        String[] users = {"alice", "bob", "alice", "alice", "bob", "charlie"};
        
        for (String user : users) {
            // 先检查全局限流
            if (!globalLimiter.tryAcquire()) {
                System.out.println("  " + user + ": ❌ 全局限流");
                continue;
            }
            
            // 再检查用户限流
            if (!userLimiter.tryAcquire(user)) {
                System.out.println("  " + user + ": ❌ 用户限流");
                continue;
            }
            
            System.out.println("  " + user + ": ✅ 通过");
        }
        
        System.out.println("\n  状态:");
        System.out.println("    - 全局剩余令牌: " + globalLimiter.getAvailableTokens());
        System.out.println("    - 活跃用户数: " + userLimiter.getActiveKeyCount());
    }
    
    /**
     * 示例 7: 并发场景
     * 高并发下的限流测试
     */
    public static void concurrentRateLimiting() throws InterruptedException {
        System.out.println("\n=== 示例 7: 并发限流 ===");
        System.out.println("场景: 100 并发请求，限流 20/秒\n");
        
        // 创建限流器
        SlidingWindow limiter = RateLimiterFactory.createSlidingWindow(20, 1000);
        
        int threadCount = 10;
        int requestsPerThread = 10;
        
        ExecutorService executor = Executors.newFixedThreadPool(threadCount);
        CountDownLatch latch = new CountDownLatch(threadCount);
        AtomicInteger successCount = new AtomicInteger(0);
        AtomicInteger failCount = new AtomicInteger(0);
        
        long startTime = System.currentTimeMillis();
        
        for (int i = 0; i < threadCount; i++) {
            executor.submit(() -> {
                try {
                    for (int j = 0; j < requestsPerThread; j++) {
                        if (limiter.tryAcquire()) {
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
        long endTime = System.currentTimeMillis();
        executor.shutdown();
        
        System.out.println("  结果:");
        System.out.println("    - 总请求数: " + (threadCount * requestsPerThread));
        System.out.println("    - 通过: " + successCount.get());
        System.out.println("    - 拒绝: " + failCount.get());
        System.out.println("    - 耗时: " + (endTime - startTime) + "ms");
        System.out.println("    - 通过率: " + 
                String.format("%.2f%%", successCount.get() * 100.0 / (threadCount * requestsPerThread)));
    }
    
    /**
     * 示例 8: 算法对比
     * 展示不同算法的特点
     */
    public static void algorithmComparison() throws InterruptedException {
        System.out.println("\n=== 示例 8: 算法对比 ===\n");
        
        // 令牌桶：允许突发
        System.out.println("  1. 令牌桶 (Token Bucket):");
        System.out.println("     - 允许突发流量");
        System.out.println("     - 平滑限流");
        System.out.println("     - 适合: API 网关、流量整形");
        TokenBucket tokenBucket = new TokenBucket(100, 10);
        System.out.println("     示例: 容量100, 速率10/s, 突发50: " + tokenBucket.tryAcquire(50));
        
        // 漏桶：恒定速率
        System.out.println("\n  2. 漏桶 (Leaky Bucket):");
        System.out.println("     - 恒定输出速率");
        System.out.println("     - 削峰填谷");
        System.out.println("     - 适合: 数据库访问、外部API调用");
        LeakyBucket leakyBucket = new LeakyBucket(50, 10);
        System.out.println("     示例: 容量50, 速率10/s, 添加30: " + leakyBucket.tryAcquire(30));
        
        // 滑动窗口：精确
        System.out.println("\n  3. 滑动窗口 (Sliding Window):");
        System.out.println("     - 精确限流");
        System.out.println("     - 无边界问题");
        System.out.println("     - 适合: 精确控制场景");
        SlidingWindow slidingWindow = new SlidingWindow(100, 1000);
        System.out.println("     示例: 100/秒, 当前计数: " + slidingWindow.getCurrentCount());
        
        // 固定窗口：简单高效
        System.out.println("\n  4. 固定窗口 (Fixed Window):");
        System.out.println("     - 简单高效");
        System.out.println("     - 可能有边界问题");
        System.out.println("     - 适合: 简单限流场景");
        FixedWindow fixedWindow = new FixedWindow(100, 1000);
        System.out.println("     示例: 100/秒, 当前计数: " + fixedWindow.getCurrentCount());
    }
    
    /**
     * 示例 9: 实际应用 - Web 服务限流中间件
     */
    public static void webServiceMiddleware() {
        System.out.println("\n=== 示例 9: Web 服务限流中间件 ===\n");
        
        // 创建多级限流器
        TokenBucket globalLimiter = RateLimiterFactory.createApiLimiter(10000);
        DistributedRateLimiter ipLimiter = RateLimiterFactory.createDistributed(100, 1000);
        DistributedRateLimiter userLimiter = RateLimiterFactory.createDistributed(50, 1000);
        
        // 模拟请求处理
        String[][] requests = {
            {"GET", "/api/users", "192.168.1.1", "alice"},
            {"POST", "/api/orders", "192.168.1.1", "alice"},
            {"GET", "/api/products", "192.168.1.2", "bob"},
            {"DELETE", "/api/users/1", "192.168.1.1", "alice"},
            {"GET", "/api/users", "192.168.1.3", "charlie"},
        };
        
        System.out.println("  处理请求:\n");
        
        for (String[] req : requests) {
            String method = req[0];
            String path = req[1];
            String ip = req[2];
            String user = req[3];
            
            System.out.println("  " + method + " " + path);
            System.out.println("    IP: " + ip + ", User: " + user);
            
            // 检查全局限流
            if (!globalLimiter.tryAcquire()) {
                System.out.println("    ❌ 503 Service Unavailable (全局过载)");
                continue;
            }
            
            // 检查 IP 限流
            if (!ipLimiter.tryAcquire(ip)) {
                System.out.println("    ❌ 429 Too Many Requests (IP 限流)");
                continue;
            }
            
            // 检查用户限流
            if (!userLimiter.tryAcquire(user)) {
                System.out.println("    ❌ 429 Too Many Requests (用户限流)");
                continue;
            }
            
            System.out.println("    ✅ 200 OK");
        }
        
        System.out.println("\n  状态:");
        System.out.println("    - 全局剩余: " + globalLimiter.getAvailableTokens());
        System.out.println("    - 活跃 IP: " + ipLimiter.getActiveKeyCount());
        System.out.println("    - 活跃用户: " + userLimiter.getActiveKeyCount());
    }
    
    // ==================== 主方法 ====================
    
    public static void main(String[] args) throws InterruptedException {
        System.out.println("╔══════════════════════════════════════════════════════╗");
        System.out.println("║       限流器工具集使用示例 - Usage Examples           ║");
        System.out.println("║       Rate Limiter Utils - Usage Examples             ║");
        System.out.println("╚══════════════════════════════════════════════════════╝");
        
        // 运行所有示例
        apiRateLimiting();
        userRateLimiting();
        ipRateLimiting();
        burstTrafficHandling();
        resourceProtection();
        multiLevelRateLimiting();
        concurrentRateLimiting();
        algorithmComparison();
        webServiceMiddleware();
        
        System.out.println("\n╔══════════════════════════════════════════════════════╗");
        System.out.println("║                  所有示例运行完成                      ║");
        System.out.println("╚══════════════════════════════════════════════════════╝");
    }
}