/**
 * AllToolkit - Swift Rate Limiter Utilities
 *
 * 提供多种限流算法实现，支持高并发场景。
 * 零依赖，仅使用 Swift 标准库和 Foundation。
 * 支持 iOS 13.0+, macOS 10.15+, watchOS 6.0+, tvOS 13.0+
 *
 * 包含算法:
 * - TokenBucket: 令牌桶算法，允许突发流量
 * - SlidingWindow: 滑动窗口算法，精确限流
 * - FixedWindow: 固定窗口算法，简单高效
 * - LeakyBucket: 漏桶算法，平滑流量
 *
 * @author AllToolkit
 * @version 1.0.0
 */

import Foundation
import Dispatch

// MARK: - 限流结果

/// 限流检查结果
public struct RateLimitResult {
    /// 是否允许通过
    public let allowed: Bool
    /// 当前剩余配额
    public let remaining: Int
    /// 需要等待的时间（秒），如果不允许通过
    public let waitTime: TimeInterval
    /// 限制总数
    public let limit: Int
    /// 重置时间（Unix 时间戳）
    public let resetTime: TimeInterval
    
    public init(allowed: Bool, remaining: Int, waitTime: TimeInterval = 0, limit: Int, resetTime: TimeInterval) {
        self.allowed = allowed
        self.remaining = remaining
        self.waitTime = waitTime
        self.limit = limit
        self.resetTime = resetTime
    }
}

// MARK: - 令牌桶算法

/// 令牌桶限流器
/// 允许一定程度的突发流量，适合 API 限流场景
public class TokenBucket {
    private let capacity: Int           // 桶容量
    private let refillRate: Double      // 每秒补充的令牌数
    private var tokens: Double          // 当前令牌数
    private var lastRefillTime: Date
    private let lock = DispatchSemaphore(value: 1)
    
    /// 初始化令牌桶
    /// - Parameters:
    ///   - capacity: 桶容量（最大令牌数）
    ///   - refillRate: 每秒补充的令牌数
    public init(capacity: Int, refillRate: Double) {
        self.capacity = capacity
        self.refillRate = refillRate
        self.tokens = Double(capacity)
        self.lastRefillTime = Date()
    }
    
    /// 尝试获取令牌
    /// - Parameter tokens: 需要获取的令牌数，默认为 1
    /// - Returns: 限流结果
    public func tryAcquire(tokens requested: Int = 1) -> RateLimitResult {
        lock.wait()
        defer { lock.signal() }
        
        // 补充令牌
        let now = Date()
        let elapsed = now.timeIntervalSince(lastRefillTime)
        let tokensToAdd = elapsed * refillRate
        tokens = min(Double(capacity), tokens + tokensToAdd)
        lastRefillTime = now
        
        let remaining = Int(tokens)
        
        if tokens >= Double(requested) {
            tokens -= Double(requested)
            return RateLimitResult(
                allowed: true,
                remaining: Int(tokens),
                waitTime: 0,
                limit: capacity,
                resetTime: now.timeIntervalSince1970 + (Double(capacity) - tokens) / refillRate
            )
        } else {
            let tokensNeeded = Double(requested) - tokens
            let waitTime = tokensNeeded / refillRate
            return RateLimitResult(
                allowed: false,
                remaining: remaining,
                waitTime: waitTime,
                limit: capacity,
                resetTime: now.timeIntervalSince1970 + waitTime
            )
        }
    }
    
    /// 获取当前令牌数
    public var currentTokens: Int {
        lock.wait()
        defer { lock.signal() }
        return Int(tokens)
    }
    
    /// 重置令牌桶
    public func reset() {
        lock.wait()
        defer { lock.signal() }
        tokens = Double(capacity)
        lastRefillTime = Date()
    }
}

// MARK: - 滑动窗口算法

/// 滑动窗口限流器
/// 基于时间窗口的精确限流，适合需要严格控制请求频率的场景
public class SlidingWindow {
    private let limit: Int              // 窗口内最大请求数
    private let windowSize: TimeInterval // 窗口大小（秒）
    private var requests: [Date] = []   // 请求时间戳列表
    private let lock = DispatchSemaphore(value: 1)
    
    /// 初始化滑动窗口限流器
    /// - Parameters:
    ///   - limit: 窗口内最大请求数
    ///   - windowSize: 窗口大小（秒）
    public init(limit: Int, windowSize: TimeInterval) {
        self.limit = limit
        self.windowSize = windowSize
    }
    
    /// 尝试通过限流
    /// - Returns: 限流结果
    public func tryAcquire() -> RateLimitResult {
        lock.wait()
        defer { lock.signal() }
        
        let now = Date()
        let windowStart = now.addingTimeInterval(-windowSize)
        
        // 移除窗口外的请求
        requests = requests.filter { $0 > windowStart }
        
        let currentCount = requests.count
        let remaining = max(0, limit - currentCount - 1)
        
        if currentCount < limit {
            requests.append(now)
            
            // 计算重置时间（最早请求过期时间）
            let resetTime: TimeInterval
            if let oldestRequest = requests.first {
                resetTime = oldestRequest.addingTimeInterval(windowSize).timeIntervalSince1970
            } else {
                resetTime = now.addingTimeInterval(windowSize).timeIntervalSince1970
            }
            
            return RateLimitResult(
                allowed: true,
                remaining: remaining,
                waitTime: 0,
                limit: limit,
                resetTime: resetTime
            )
        } else {
            // 计算需要等待的时间
            let waitTime: TimeInterval
            if let oldestRequest = requests.first {
                waitTime = oldestRequest.addingTimeInterval(windowSize).timeIntervalSince(now)
            } else {
                waitTime = windowSize
            }
            
            return RateLimitResult(
                allowed: false,
                remaining: 0,
                waitTime: max(0, waitTime),
                limit: limit,
                resetTime: now.addingTimeInterval(max(0, waitTime)).timeIntervalSince1970
            )
        }
    }
    
    /// 获取当前窗口内的请求数
    public var currentCount: Int {
        lock.wait()
        defer { lock.signal() }
        let now = Date()
        let windowStart = now.addingTimeInterval(-windowSize)
        return requests.filter { $0 > windowStart }.count
    }
    
    /// 重置滑动窗口
    public func reset() {
        lock.wait()
        defer { lock.signal() }
        requests.removeAll()
    }
}

// MARK: - 固定窗口算法

/// 固定窗口限流器
/// 简单高效，适合对精度要求不高的场景
public class FixedWindow {
    private let limit: Int              // 窗口内最大请求数
    private let windowSize: TimeInterval // 窗口大小（秒）
    private var count: Int = 0          // 当前窗口计数
    private var windowStart: Date       // 当前窗口开始时间
    private let lock = DispatchSemaphore(value: 1)
    
    /// 初始化固定窗口限流器
    /// - Parameters:
    ///   - limit: 窗口内最大请求数
    ///   - windowSize: 窗口大小（秒）
    public init(limit: Int, windowSize: TimeInterval) {
        self.limit = limit
        self.windowSize = windowSize
        self.windowStart = Date()
    }
    
    /// 尝试通过限流
    /// - Returns: 限流结果
    public func tryAcquire() -> RateLimitResult {
        lock.wait()
        defer { lock.signal() }
        
        let now = Date()
        
        // 检查是否需要重置窗口
        if now.timeIntervalSince(windowStart) >= windowSize {
            windowStart = now
            count = 0
        }
        
        let remaining = max(0, limit - count - 1)
        let resetTime = windowStart.addingTimeInterval(windowSize).timeIntervalSince1970
        
        if count < limit {
            count += 1
            return RateLimitResult(
                allowed: true,
                remaining: remaining,
                waitTime: 0,
                limit: limit,
                resetTime: resetTime
            )
        } else {
            let waitTime = windowStart.addingTimeInterval(windowSize).timeIntervalSince(now)
            return RateLimitResult(
                allowed: false,
                remaining: 0,
                waitTime: max(0, waitTime),
                limit: limit,
                resetTime: resetTime
            )
        }
    }
    
    /// 获取当前窗口计数
    public var currentCount: Int {
        lock.wait()
        defer { lock.signal() }
        let now = Date()
        if now.timeIntervalSince(windowStart) >= windowSize {
            return 0
        }
        return count
    }
    
    /// 重置固定窗口
    public func reset() {
        lock.wait()
        defer { lock.signal() }
        count = 0
        windowStart = Date()
    }
}

// MARK: - 漏桶算法

/// 漏桶限流器
/// 以固定速率处理请求，平滑流量输出
public class LeakyBucket {
    private let capacity: Int           // 桶容量
    private let leakRate: Double        // 每秒漏出的请求数
    private var water: Int = 0          // 当前桶中水量（请求数）
    private var lastLeakTime: Date      // 上次漏水时间
    private let lock = DispatchSemaphore(value: 1)
    
    /// 初始化漏桶限流器
    /// - Parameters:
    ///   - capacity: 桶容量
    ///   - leakRate: 每秒漏出的请求数（处理速率）
    public init(capacity: Int, leakRate: Double) {
        self.capacity = capacity
        self.leakRate = leakRate
        self.lastLeakTime = Date()
    }
    
    /// 尝试添加请求到桶中
    /// - Returns: 限流结果
    public func tryAcquire() -> RateLimitResult {
        lock.wait()
        defer { lock.signal() }
        
        // 漏水
        let now = Date()
        let elapsed = now.timeIntervalSince(lastLeakTime)
        let leaked = Int(elapsed * leakRate)
        water = max(0, water - leaked)
        lastLeakTime = now
        
        let remaining = capacity - water - 1
        
        if water < capacity {
            water += 1
            
            // 计算完全排空的时间
            let drainTime = Double(water) / leakRate
            let resetTime = now.addingTimeInterval(drainTime).timeIntervalSince1970
            
            return RateLimitResult(
                allowed: true,
                remaining: max(0, remaining),
                waitTime: 0,
                limit: capacity,
                resetTime: resetTime
            )
        } else {
            // 计算需要等待的时间（漏出 1 个请求的时间）
            let waitTime = 1.0 / leakRate
            
            return RateLimitResult(
                allowed: false,
                remaining: 0,
                waitTime: waitTime,
                limit: capacity,
                resetTime: now.addingTimeInterval(waitTime).timeIntervalSince1970
            )
        }
    }
    
    /// 获取当前桶中水量
    public var currentWater: Int {
        lock.wait()
        defer { lock.signal() }
        return water
    }
    
    /// 重置漏桶
    public func reset() {
        lock.wait()
        defer { lock.signal() }
        water = 0
        lastLeakTime = Date()
    }
}

// MARK: - 并发限流器

/// 并发数限流器
/// 限制同时进行的请求数量
public class ConcurrencyLimiter {
    private let maxConcurrency: Int      // 最大并发数
    private var currentCount: Int = 0    // 当前并发数
    private let lock = DispatchSemaphore(value: 1)
    private let semaphore: DispatchSemaphore
    
    /// 初始化并发限流器
    /// - Parameter maxConcurrency: 最大并发数
    public init(maxConcurrency: Int) {
        self.maxConcurrency = maxConcurrency
        self.semaphore = DispatchSemaphore(value: maxConcurrency)
    }
    
    /// 获取执行许可
    /// - Parameter timeout: 超时时间（秒），nil 表示无限等待
    /// - Returns: 是否成功获取许可
    @discardableResult
    public func acquire(timeout: TimeInterval? = nil) -> Bool {
        let result: DispatchTimeoutResult
        if let timeout = timeout {
            result = semaphore.wait(timeout: .now() + timeout)
        } else {
            semaphore.wait()
            result = .success
        }
        
        if result == .success {
            lock.wait()
            currentCount += 1
            lock.signal()
            return true
        }
        return false
    }
    
    /// 释放执行许可
    public func release() {
        lock.wait()
        if currentCount > 0 {
            currentCount -= 1
        }
        lock.signal()
        semaphore.signal()
    }
    
    /// 获取当前并发数
    public var currentConcurrency: Int {
        lock.wait()
        defer { lock.signal() }
        return currentCount
    }
    
    /// 获取剩余可用并发数
    public var availableConcurrency: Int {
        lock.wait()
        defer { lock.signal() }
        return maxConcurrency - currentCount
    }
}

// MARK: - 限流器组合

/// 限流器组合策略
public enum RateLimiterStrategy {
    /// 全部通过：所有限流器都必须允许
    case allPass
    /// 任一通过：任一限流器允许即可
    case anyPass
}

/// 组合限流器
/// 支持组合多个限流器，按策略判断
public class CompositeRateLimiter {
    private let limiters: [AnyRateLimiter]
    private let strategy: RateLimiterStrategy
    
    /// 初始化组合限流器
    /// - Parameters:
    ///   - limiters: 限流器列表
    ///   - strategy: 组合策略
    public init(_ limiters: [AnyRateLimiter], strategy: RateLimiterStrategy = .allPass) {
        self.limiters = limiters
        self.strategy = strategy
    }
    
    /// 尝试通过限流
    /// - Returns: 组合后的限流结果
    public func tryAcquire() -> RateLimitResult {
        var results: [RateLimitResult] = []
        
        for limiter in limiters {
            results.append(limiter.tryAcquire())
        }
        
        switch strategy {
        case .allPass:
            let allAllowed = results.allSatisfy { $0.allowed }
            let minRemaining = results.map { $0.remaining }.min() ?? 0
            let maxWaitTime = results.map { $0.waitTime }.max() ?? 0
            let minLimit = results.map { $0.limit }.min() ?? 0
            let maxResetTime = results.map { $0.resetTime }.max() ?? 0
            
            return RateLimitResult(
                allowed: allAllowed,
                remaining: minRemaining,
                waitTime: maxWaitTime,
                limit: minLimit,
                resetTime: maxResetTime
            )
            
        case .anyPass:
            let anyAllowed = results.contains { $0.allowed }
            let maxRemaining = results.map { $0.remaining }.max() ?? 0
            let minWaitTime = results.map { $0.waitTime }.min() ?? 0
            let maxLimit = results.map { $0.limit }.max() ?? 0
            let minResetTime = results.map { $0.resetTime }.min() ?? 0
            
            return RateLimitResult(
                allowed: anyAllowed,
                remaining: maxRemaining,
                waitTime: minWaitTime,
                limit: maxLimit,
                resetTime: minResetTime
            )
        }
    }
}

// MARK: - 类型擦除包装器

/// 用于组合限流器的类型擦除包装
public struct AnyRateLimiter {
    private let _tryAcquire: () -> RateLimitResult
    
    public init<L: RateLimiterProtocol>(_ limiter: L) {
        _tryAcquire = limiter.tryAcquire
    }
    
    public func tryAcquire() -> RateLimitResult {
        return _tryAcquire()
    }
}

// MARK: - 协议定义

/// 限流器协议
public protocol RateLimiterProtocol {
    func tryAcquire() -> RateLimitResult
}

// 扩展各限流器遵循协议
extension TokenBucket: RateLimiterProtocol {
    public func tryAcquire() -> RateLimitResult {
        return tryAcquire(tokens: 1)
    }
}

extension SlidingWindow: RateLimiterProtocol {}
extension FixedWindow: RateLimiterProtocol {}
extension LeakyBucket: RateLimiterProtocol {}

// MARK: - 便捷扩展

public extension TokenBucket {
    /// 便捷创建：每秒限制
    /// - Parameter requestsPerSecond: 每秒请求数
    static func perSecond(_ requestsPerSecond: Int) -> TokenBucket {
        return TokenBucket(capacity: requestsPerSecond, refillRate: Double(requestsPerSecond))
    }
    
    /// 便捷创建：每分钟限制
    /// - Parameter requestsPerMinute: 每分钟请求数
    static func perMinute(_ requestsPerMinute: Int) -> TokenBucket {
        return TokenBucket(capacity: requestsPerMinute, refillRate: Double(requestsPerMinute) / 60.0)
    }
    
    /// 便捷创建：每小时限制
    /// - Parameter requestsPerHour: 每小时请求数
    static func perHour(_ requestsPerHour: Int) -> TokenBucket {
        return TokenBucket(capacity: requestsPerHour, refillRate: Double(requestsPerHour) / 3600.0)
    }
}

public extension SlidingWindow {
    /// 便捷创建：每秒限制
    /// - Parameter requestsPerSecond: 每秒请求数
    static func perSecond(_ requestsPerSecond: Int) -> SlidingWindow {
        return SlidingWindow(limit: requestsPerSecond, windowSize: 1.0)
    }
    
    /// 便捷创建：每分钟限制
    /// - Parameter requestsPerMinute: 每分钟请求数
    static func perMinute(_ requestsPerMinute: Int) -> SlidingWindow {
        return SlidingWindow(limit: requestsPerMinute, windowSize: 60.0)
    }
    
    /// 便捷创建：每小时限制
    /// - Parameter requestsPerHour: 每小时请求数
    static func perHour(_ requestsPerHour: Int) -> SlidingWindow {
        return SlidingWindow(limit: requestsPerHour, windowSize: 3600.0)
    }
}

public extension FixedWindow {
    /// 便捷创建：每秒限制
    /// - Parameter requestsPerSecond: 每秒请求数
    static func perSecond(_ requestsPerSecond: Int) -> FixedWindow {
        return FixedWindow(limit: requestsPerSecond, windowSize: 1.0)
    }
    
    /// 便捷创建：每分钟限制
    /// - Parameter requestsPerMinute: 每分钟请求数
    static func perMinute(_ requestsPerMinute: Int) -> FixedWindow {
        return FixedWindow(limit: requestsPerMinute, windowSize: 60.0)
    }
    
    /// 便捷创建：每小时限制
    /// - Parameter requestsPerHour: 每小时请求数
    static func perHour(_ requestsPerHour: Int) -> FixedWindow {
        return FixedWindow(limit: requestsPerHour, windowSize: 3600.0)
    }
}

// MARK: - 异步支持（iOS 13.0+ 兼容）

/// 带异步等待的限流器扩展
public extension RateLimiterProtocol {
    /// 异步等待获取许可
    /// - Parameters:
    ///   - maxWait: 最大等待时间（秒）
    ///   - completion: 完成回调，返回是否成功获取
    func acquireAsync(maxWait: TimeInterval, completion: @escaping (Bool) -> Void) {
        let startTime = Date()
        
        func attempt() {
            let result = tryAcquire()
            if result.allowed {
                completion(true)
            } else if Date().timeIntervalSince(startTime) >= maxWait {
                completion(false)
            } else {
                let waitTime = min(result.waitTime, maxWait - Date().timeIntervalSince(startTime))
                if waitTime > 0 {
                    DispatchQueue.global().asyncAfter(deadline: .now() + waitTime, execute: attempt)
                } else {
                    attempt()
                }
            }
        }
        
        attempt()
    }
    
    /// 使用 Result 类型的异步获取
    /// - Parameters:
    ///   - maxWait: 最大等待时间（秒）
    ///   - completion: 完成回调
    func acquireAsync(maxWait: TimeInterval, completion: @escaping (Result<RateLimitResult, Error>) -> Void) {
        acquireAsync(maxWait: maxWait) { success in
            if success {
                let result = self.tryAcquire()
                completion(.success(result))
            } else {
                let error = NSError(domain: "RateLimiter", code: -1, userInfo: [NSLocalizedDescriptionKey: "Timeout waiting for rate limit"])
                completion(.failure(error))
            }
        }
    }
}