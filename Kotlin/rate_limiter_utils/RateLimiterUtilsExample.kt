import com.alltoolkit.ratelimiter.*

/**
 * RateLimiterUtils 使用示例
 * 
 * 展示如何使用各种限流算法：
 * - Token Bucket (令牌桶)
 * - Leaky Bucket (漏桶)
 * - Fixed Window Counter (固定窗口计数器)
 * - Sliding Window Log (滑动窗口日志)
 * - Sliding Window Counter (滑动窗口计数器)
 */
fun main() {
    println("=== RateLimiterUtils 示例 ===\n")
    
    // 示例1：令牌桶限流
    tokenBucketExample()
    
    // 示例2：漏桶限流
    leakyBucketExample()
    
    // 示例3：固定窗口计数器
    fixedWindowExample()
    
    // 示例4：滑动窗口日志
    slidingWindowLogExample()
    
    // 示例5：滑动窗口计数器
    slidingWindowCounterExample()
    
    // 示例6：使用工厂方法
    factoryExample()
    
    // 示例7：多用户限流
    multiUserRateLimitingExample()
    
    // 示例8：限流器管理器
    rateLimiterManagerExample()
    
    // 示例9：模拟API保护
    apiProtectionExample()
    
    // 示例10：令牌桶批量获取
    batchTokenAcquisitionExample()
}

/**
 * 示例1：令牌桶限流
 * 
 * 特点：
 * - 允许突发流量
 * - 平滑限流
 * - 适合API限流场景
 */
fun tokenBucketExample() {
    println("--- 令牌桶示例 ---")
    
    // 创建一个容量为10，每秒填充5个令牌的桶
    val bucket = TokenBucket(
        capacity = 10,
        refillRate = 5.0 / 1000.0,  // 每毫秒填充0.005个令牌 = 每秒5个
        initialTokens = 10
    )
    
    println("初始状态：桶容量10，每秒填充5个令牌")
    
    // 突发请求
    println("\n突发请求测试（连续请求10次）：")
    for (i in 1..10) {
        val result = bucket.tryAcquire()
        println("请求 $i: ${if (result.allowed) "✓ 通过" else "✗ 拒绝"} (剩余令牌: ${result.remainingTokens})")
    }
    
    // 第11次请求
    val result = bucket.tryAcquire()
    println("请求 11: ${if (result.allowed) "✓ 通过" else "✗ 拒绝"} (需要等待: ${result.waitTimeMs}ms)")
    
    // 等待令牌填充
    println("\n等待500ms，令牌填充中...")
    Thread.sleep(500)
    
    println("再次尝试请求：")
    val afterWait = bucket.tryAcquire()
    println("请求: ${if (afterWait.allowed) "✓ 通过" else "✗ 拒绝"} (剩余令牌: ${afterWait.remainingTokens})")
    
    println()
}

/**
 * 示例2：漏桶限流
 * 
 * 特点：
 * - 严格控制流出速率
 * - 适合流量整形
 * - 适合消息队列处理
 */
fun leakyBucketExample() {
    println("--- 漏桶示例 ---")
    
    // 创建一个容量为5，每秒处理10个请求的漏桶
    val bucket = LeakyBucket(
        capacity = 5,
        leakRate = 10.0 / 1000.0  // 每毫秒漏出0.01个请求 = 每秒10个
    )
    
    println("桶容量5，处理速率10请求/秒")
    
    // 连续请求
    println("\n连续请求测试：")
    for (i in 1..7) {
        val result = bucket.tryAcquire()
        println("请求 $i: ${if (result.allowed) "✓ 通过" else "✗ 拒绝"}")
    }
    
    println()
}

/**
 * 示例3：固定窗口计数器
 * 
 * 特点：
 * - 实现简单
 * - 内存占用小
 * - 可能有窗口边界问题
 * - 适合简单限流场景
 */
fun fixedWindowExample() {
    println("--- 固定窗口计数器示例 ---")
    
    // 创建一个每秒最多5个请求的限流器
    val counter = FixedWindowCounter(
        limit = 5,
        windowSizeMs = 1000
    )
    
    println("窗口大小1秒，限制5请求/秒")
    
    // 连续请求
    println("\n连续请求测试：")
    for (i in 1..7) {
        val result = counter.tryAcquire("api")
        println("请求 $i: ${if (result.allowed) "✓ 通过" else "✗ 拒绝"} (剩余: ${result.remainingTokens}, 重试等待: ${result.retryAfterMs}ms)")
    }
    
    println("\n当前计数: ${counter.getCount("api")}")
    
    // 重置计数器
    counter.reset("api")
    println("重置后计数: ${counter.getCount("api")}")
    
    println()
}

/**
 * 示例4：滑动窗口日志
 * 
 * 特点：
 * - 精确控制
 * - 无边界突刺问题
 * - 内存占用较大
 */
fun slidingWindowLogExample() {
    println("--- 滑动窗口日志示例 ---")
    
    // 创建一个500ms窗口内最多3个请求的限流器
    val log = SlidingWindowLog(
        limit = 3,
        windowSizeMs = 500
    )
    
    println("窗口大小500ms，限制3请求/窗口")
    
    // 第一批请求
    println("\n第一批请求：")
    for (i in 1..3) {
        val result = log.tryAcquire("user")
        println("请求 $i: ${if (result.allowed) "✓ 通过" else "✗ 拒绝"}")
    }
    
    // 超限请求
    println("\n超限请求：")
    val rejected = log.tryAcquire("user")
    println("请求: ${if (rejected.allowed) "✓ 通过" else "✗ 拒绝"} (重试等待: ${rejected.retryAfterMs}ms)")
    
    // 等待窗口滑动
    println("\n等待600ms...")
    Thread.sleep(600)
    
    // 新窗口
    println("新窗口请求：")
    for (i in 1..2) {
        val result = log.tryAcquire("user")
        println("请求 $i: ${if (result.allowed) "✓ 通过" else "✗ 拒绝"}")
    }
    
    println()
}

/**
 * 示例5：滑动窗口计数器
 * 
 * 特点：
 * - 内存占用小
 * - 近似滑动窗口
 * - 适合分布式限流
 */
fun slidingWindowCounterExample() {
    println("--- 滑动窗口计数器示例 ---")
    
    // 创建一个每分钟最多10个请求的限流器
    val counter = SlidingWindowCounter(
        limit = 10,
        windowSizeMs = 1000  // 使用1秒便于演示
    )
    
    println("窗口大小1秒，限制10请求/窗口")
    
    // 连续请求
    println("\n连续请求测试：")
    var successCount = 0
    for (i in 1..12) {
        val result = counter.tryAcquire("api")
        if (result.allowed) successCount++
        println("请求 $i: ${if (result.allowed) "✓ 通过" else "✗ 拒绝"}")
    }
    
    println("成功请求数: $successCount")
    println()
}

/**
 * 示例6：使用工厂方法
 */
fun factoryExample() {
    println("--- 工厂方法示例 ---")
    
    // 令牌桶：每秒100请求，突发上限200
    val tokenBucket = RateLimiterFactory.tokenBucket(ratePerSecond = 100, capacity = 200)
    println("令牌桶：100请求/秒，突发上限200")
    
    // 漏桶：每秒50请求处理能力，队列上限50
    val leakyBucket = RateLimiterFactory.leakyBucket(ratePerSecond = 50, capacity = 50)
    println("漏桶：50请求/秒处理，队列上限50")
    
    // 固定窗口：每分钟60请求
    val fixedWindow = RateLimiterFactory.fixedWindowPerMinute(60)
    println("固定窗口：60请求/分钟")
    
    // 滑动窗口：每分钟100请求
    val slidingWindow = RateLimiterFactory.slidingWindowPerMinute(100)
    println("滑动窗口：100请求/分钟")
    
    // 测试令牌桶
    println("\n测试令牌桶（请求10次）：")
    for (i in 1..10) {
        val result = tokenBucket.tryAcquire()
        println("请求 $i: ${if (result.allowed) "✓" else "✗"} 剩余: ${result.remainingTokens}")
    }
    
    println()
}

/**
 * 示例7：多用户限流
 */
fun multiUserRateLimitingExample() {
    println("--- 多用户限流示例 ---")
    
    // 创建一个每用户每分钟10请求的限流器
    val limiter = FixedWindowCounter(limit = 10, windowSizeMs = 60_000)
    
    val users = listOf("alice", "bob", "charlie")
    
    for (user in users) {
        println("\n用户 $user 的请求：")
        for (i in 1..12) {
            val result = limiter.tryAcquire(user)
            if (i <= 5 || !result.allowed) {
                println("  请求 $i: ${if (result.allowed) "✓ 通过" else "✗ 拒绝"} (剩余: ${result.remainingTokens})")
            }
        }
        println("  用户 $user 总计数: ${limiter.getCount(user)}")
    }
    
    println()
}

/**
 * 示例8：限流器管理器
 */
fun rateLimiterManagerExample() {
    println("--- 限流器管理器示例 ---")
    
    val manager = RateLimiterManager()
    
    // 注册不同类型的限流器
    manager.register("api-global", TokenBucket.create(1000, 2000))
    manager.register("api-per-user", FixedWindowCounter.create(100))
    manager.register("upload", SlidingWindowLog(10, 60_000))
    
    println("已注册限流器：api-global, api-per-user, upload")
    
    // 使用限流器
    val globalLimiter = manager.getTokenBucket("api-global")
    val userLimiter = manager.getFixedWindow("api-per-user")
    val uploadLimiter = manager.getSlidingWindowLog("upload")
    
    println("\n测试全局API限流器：")
    val result1 = globalLimiter?.tryAcquire()
    println("请求: ${if (result1?.allowed == true) "✓ 通过" else "✗ 拒绝"}")
    
    println("\n测试用户限流器：")
    val result2 = userLimiter?.tryAcquire("user123")
    println("请求: ${if (result2?.allowed == true) "✓ 通过" else "✗ 拒绝"}")
    
    println("\n测试上传限流器：")
    val result3 = uploadLimiter?.tryAcquire("upload-1")
    println("请求: ${if (result3?.allowed == true) "✓ 通过" else "✗ 拒绝"}")
    
    // 移除限流器
    manager.unregister("upload")
    println("\n移除 upload 限流器后: ${manager.getSlidingWindowLog("upload")}")
    
    println()
}

/**
 * 示例9：模拟API保护
 */
fun apiProtectionExample() {
    println("--- API保护示例 ---")
    
    // 模拟一个API服务器的限流保护
    class ApiServer {
        private val globalLimiter = TokenBucket.create(100, 150)  // 全局限流
        private val userLimiters = FixedWindowCounter(limit = 20, windowSizeMs = 60_000)  // 用户限流
        private val ipLimiters = SlidingWindowLog(50, 60_000)  // IP限流
        
        fun handleRequest(userId: String, ip: String): String {
            // 1. 检查全局限流
            val globalResult = globalLimiter.tryAcquire()
            if (!globalResult.allowed) {
                return "503 Service Unavailable - Global rate limit exceeded. Retry after ${globalResult.retryAfterMs}ms"
            }
            
            // 2. 检查用户限流
            val userResult = userLimiters.tryAcquire(userId)
            if (!userResult.allowed) {
                return "429 Too Many Requests - User rate limit exceeded. Retry after ${userResult.retryAfterMs}ms"
            }
            
            // 3. 检查IP限流
            val ipResult = ipLimiters.tryAcquire(ip)
            if (!ipResult.allowed) {
                return "429 Too Many Requests - IP rate limit exceeded. Retry after ${ipResult.retryAfterMs}ms"
            }
            
            // 4. 处理请求
            return "200 OK - Request processed for user $userId from $ip"
        }
    }
    
    val api = ApiServer()
    
    println("模拟API服务器（全局100请求/秒，每用户20请求/分钟，每IP 50请求/分钟）")
    
    println("\n正常请求：")
    for (i in 1..3) {
        println("  ${api.handleRequest("user1", "192.168.1.1")}")
    }
    
    println("\n模拟用户限流：")
    for (i in 1..25) {
        val result = api.handleRequest("user2", "192.168.1.2")
        if (i <= 2 || i > 20) {
            println("  请求 $i: $result")
        }
    }
    
    println()
}

/**
 * 示例10：令牌桶批量获取
 */
fun batchTokenAcquisitionExample() {
    println("--- 令牌桶批量获取示例 ---")
    
    // 创建一个大容量令牌桶
    val bucket = TokenBucket.create(10, 100)
    
    println("令牌桶容量：100，速率：10请求/秒")
    
    // 批量获取令牌
    println("\n批量获取测试：")
    
    // 获取30个令牌
    val result1 = bucket.tryAcquire(30)
    println("获取30个令牌: ${if (result1.allowed) "✓ 成功" else "✗ 失败"} (剩余: ${result1.remainingTokens})")
    
    // 再获取50个令牌
    val result2 = bucket.tryAcquire(50)
    println("获取50个令牌: ${if (result2.allowed) "✓ 成功" else "✗ 失败"} (剩余: ${result2.remainingTokens})")
    
    // 尝试获取30个令牌（应该失败，只剩20个）
    val result3 = bucket.tryAcquire(30)
    println("获取30个令牌: ${if (result3.allowed) "✓ 成功" else "✗ 失败"} (需要等待: ${result3.waitTimeMs}ms)")
    
    // 只获取剩余的20个
    val result4 = bucket.tryAcquire(20)
    println("获取20个令牌: ${if (result4.allowed) "✓ 成功" else "✗ 失败"} (剩余: ${result4.remainingTokens})")
    
    println()
}