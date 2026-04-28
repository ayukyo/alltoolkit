/**
 * AllToolkit - Swift Rate Limiter 使用示例
 *
 * 展示如何使用各种限流算法
 *
 * @author AllToolkit
 * @version 1.0.0
 */

import Foundation

// MARK: - 示例 1: API 请求限流

/// API 客户端示例
class APIClient {
    private let rateLimiter: TokenBucket
    
    init(requestsPerSecond: Int) {
        // 每秒最多 requestsPerSecond 个请求
        rateLimiter = TokenBucket.perSecond(requestsPerSecond)
    }
    
    func request(url: String, completion: @escaping (Result<Data, Error>) -> Void) {
        let result = rateLimiter.tryAcquire()
        
        if result.allowed {
            print("✅ 请求通过: \(url)")
            // 执行实际请求...
            completion(.success(Data()))
        } else {
            print("⏳ 请求被限流，需等待 \(String(format: "%.2f", result.waitTime)) 秒")
            let error = NSError(domain: "RateLimiter", code: 429, 
                              userInfo: [NSLocalizedDescriptionKey: "Too many requests"])
            completion(.failure(error))
        }
    }
}

// 使用示例
func exampleAPIClient() {
    print("\n📡 === API 客户端限流示例 ===")
    
    let client = APIClient(requestsPerSecond: 3)
    
    for i in 1...5 {
        client.request(url: "https://api.example.com/data/\(i)") { result in
            switch result {
            case .success:
                print("   请求 \(i) 成功")
            case .failure(let error):
                print("   请求 \(i) 失败: \(error.localizedDescription)")
            }
        }
    }
}

// MARK: - 示例 2: 用户操作限制

/// 用户操作限流器
class UserActionLimiter {
    private let actionLimiter: SlidingWindow
    
    init(maxActionsPerMinute: Int) {
        actionLimiter = SlidingWindow.perMinute(maxActionsPerMinute)
    }
    
    func performAction(_ action: String) -> Bool {
        let result = actionLimiter.tryAcquire()
        
        if result.allowed {
            print("✅ 操作允许: \(action), 剩余 \(result.remaining) 次")
            return true
        } else {
            print("⚠️ 操作被限流: \(action), 请等待 \(String(format: "%.1f", result.waitTime)) 秒")
            return false
        }
    }
    
    func getRemainingActions() -> Int {
        return actionLimiter.currentCount
    }
}

func exampleUserActions() {
    print("\n👤 === 用户操作限流示例 ===")
    
    let limiter = UserActionLimiter(maxActionsPerMinute: 5)
    
    // 模拟用户操作
    let actions = ["点赞", "评论", "分享", "收藏", "关注", "举报"]
    for action in actions {
        _ = limiter.performAction(action)
    }
}

// MARK: - 示例 3: 后台任务调度

/// 后台任务调度器
class BackgroundTaskScheduler {
    private let taskLimiter: FixedWindow
    private let concurrencyLimiter: ConcurrencyLimiter
    
    init(maxTasksPerHour: Int, maxConcurrentTasks: Int) {
        taskLimiter = FixedWindow.perHour(maxTasksPerHour)
        concurrencyLimiter = ConcurrencyLimiter(maxConcurrency: maxConcurrentTasks)
    }
    
    func scheduleTask(_ taskName: String, action: @escaping () -> Void) {
        let result = taskLimiter.tryAcquire()
        
        guard result.allowed else {
            print("⏳ 任务 '\(taskName)' 被限流，需等待 \(String(format: "%.0f", result.waitTime)) 秒")
            return
        }
        
        guard concurrencyLimiter.acquire(timeout: 0) else {
            print("🔒 任务 '\(taskName)' 等待并发槽位...")
            // 可以选择排队或放弃
            return
        }
        
        print("🚀 执行任务: \(taskName)")
        
        // 模拟异步执行
        DispatchQueue.global().async {
            action()
            self.concurrencyLimiter.release()
            print("✅ 任务完成: \(taskName)")
        }
    }
    
    func getStatus() -> (remaining: Int, concurrent: Int) {
        return (taskLimiter.currentCount, concurrencyLimiter.currentConcurrency)
    }
}

func exampleBackgroundTasks() {
    print("\n⚙️ === 后台任务调度示例 ===")
    
    let scheduler = BackgroundTaskScheduler(maxTasksPerHour: 10, maxConcurrentTasks: 2)
    
    // 模拟多个任务
    for i in 1...5 {
        scheduler.scheduleTask("数据同步 \(i)") {
            Thread.sleep(forTimeInterval: 0.5) // 模拟工作
        }
    }
    
    // 等待任务完成
    Thread.sleep(forTimeInterval: 2)
}

// MARK: - 示例 4: 多级限流

/// 多级限流配置
class MultiLevelRateLimiter {
    private let compositeLimiter: CompositeRateLimiter
    
    /// 配置多级限流
    /// - Parameters:
    ///   - perSecond: 每秒限制
    ///   - perMinute: 每分钟限制
    ///   - perHour: 每小时限制
    init(perSecond: Int, perMinute: Int, perHour: Int) {
        compositeLimiter = CompositeRateLimiter([
            AnyRateLimiter(TokenBucket.perSecond(perSecond)),
            AnyRateLimiter(SlidingWindow.perMinute(perMinute)),
            AnyRateLimiter(FixedWindow.perHour(perHour))
        ], strategy: .allPass)
    }
    
    func check() -> RateLimitResult {
        return compositeLimiter.tryAcquire()
    }
}

func exampleMultiLevelRateLimiting() {
    print("\n🎚️ === 多级限流示例 ===")
    
    // 每秒 10 个，每分钟 100 个，每小时 1000 个
    let limiter = MultiLevelRateLimiter(perSecond: 10, perMinute: 100, perHour: 1000)
    
    // 快速发送 15 个请求
    for i in 1...15 {
        let result = limiter.check()
        let status = result.allowed ? "✅ 通过" : "❌ 限流"
        print("请求 \(i): \(status), 剩余: \(result.remaining)")
        
        if !result.allowed {
            break
        }
    }
}

// MARK: - 示例 5: 突发流量处理

/// 突发流量处理器（使用令牌桶）
class BurstTrafficHandler {
    private let tokenBucket: TokenBucket
    
    /// 初始化
    /// - Parameters:
    ///   - burstCapacity: 突发容量（最大突发）
    ///   - averageRate: 平均速率（每秒）
    init(burstCapacity: Int, averageRate: Double) {
        tokenBucket = TokenBucket(capacity: burstCapacity, refillRate: averageRate)
    }
    
    func handleRequest(_ requestId: Int) {
        let result = tokenBucket.tryAcquire()
        
        if result.allowed {
            print("✅ 请求 \(requestId) 处理中 (令牌剩余: \(result.remaining))")
        } else {
            print("⏳ 请求 \(requestId) 需等待 \(String(format: "%.3f", result.waitTime)) 秒")
        }
    }
    
    func getAvailableBurst() -> Int {
        return tokenBucket.currentTokens
    }
}

func exampleBurstTraffic() {
    print("\n💥 === 突发流量处理示例 ===")
    
    // 允许 10 个突发请求，但平均每秒只能处理 2 个
    let handler = BurstTrafficHandler(burstCapacity: 10, averageRate: 2.0)
    
    print("初始突发容量: \(handler.getAvailableBurst())")
    
    // 突发 15 个请求
    print("\n突发 15 个请求:")
    for i in 1...15 {
        handler.handleRequest(i)
    }
    
    // 等待令牌恢复
    print("\n等待 1 秒后（恢复约 2 个令牌）:")
    Thread.sleep(forTimeInterval: 1.0)
    print("可用突发容量: \(handler.getAvailableBurst())")
    
    handler.handleRequest(16)
}

// MARK: - 示例 6: 异步限流等待

/// 异步限流示例
class AsyncRateLimiterDemo {
    private let rateLimiter: SlidingWindow
    
    init() {
        rateLimiter = SlidingWindow(limit: 2, windowSize: 1.0)
    }
    
    func performRequest(_ requestId: Int) {
        rateLimiter.acquireAsync(maxWait: 5.0) { success in
            if success {
                print("✅ 请求 \(requestId) 获取许可，开始处理...")
                // 模拟处理
                Thread.sleep(forTimeInterval: 0.1)
                print("   请求 \(requestId) 处理完成")
            } else {
                print("❌ 请求 \(requestId) 等待超时")
            }
        }
    }
}

func exampleAsyncRateLimiting() {
    print("\n⏱️ === 异步限流等待示例 ===")
    
    let demo = AsyncRateLimiterDemo()
    
    // 发送 5 个请求，但每秒只能处理 2 个
    for i in 1...5 {
        demo.performRequest(i)
    }
    
    // 等待所有请求完成
    Thread.sleep(forTimeInterval: 3.0)
}

// MARK: - 示例 7: 流量平滑（漏桶）

/// 流量平滑处理器
class TrafficSmoother {
    private let leakyBucket: LeakyBucket
    
    /// 初始化
    /// - Parameters:
    ///   - queueSize: 队列大小（桶容量）
    ///   - outputRate: 输出速率（每秒处理的请求数）
    init(queueSize: Int, outputRate: Double) {
        leakyBucket = LeakyBucket(capacity: queueSize, leakRate: outputRate)
    }
    
    func submitRequest(_ requestId: Int) -> Bool {
        let result = leakyBucket.tryAcquire()
        
        if result.allowed {
            print("📥 请求 \(requestId) 已入队")
            return true
        } else {
            print("🚫 请求 \(requestId) 被拒绝（队列已满）")
            return false
        }
    }
    
    func getQueueLength() -> Int {
        return leakyBucket.currentWater
    }
}

func exampleTrafficSmoothing() {
    print("\n🌊 === 流量平滑示例 ===")
    
    // 队列大小 5，每秒处理 2 个请求
    let smoother = TrafficSmoother(queueSize: 5, outputRate: 2.0)
    
    // 快速提交 10 个请求
    print("快速提交 10 个请求:")
    for i in 1...10 {
        let accepted = smoother.submitRequest(i)
        if !accepted {
            break
        }
    }
    
    print("\n当前队列长度: \(smoother.getQueueLength())")
    
    // 等待处理
    print("\n等待 2 秒（处理约 4 个请求）:")
    Thread.sleep(forTimeInterval: 2.0)
    print("处理后队列长度: \(smoother.getQueueLength())")
}

// MARK: - 主函数

func runAllExamples() {
    print("╔════════════════════════════════════════════╗")
    print("║   Swift Rate Limiter 使用示例              ║")
    print("╚════════════════════════════════════════════╝")
    
    exampleAPIClient()
    exampleUserActions()
    exampleBackgroundTasks()
    exampleMultiLevelRateLimiting()
    exampleBurstTraffic()
    exampleAsyncRateLimiting()
    exampleTrafficSmoothing()
    
    print("\n✅ 所有示例执行完成")
}

// 如果直接运行此文件
// runAllExamples()