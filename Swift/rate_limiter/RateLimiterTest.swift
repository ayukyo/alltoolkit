/**
 * AllToolkit - Swift Rate Limiter Test
 *
 * 限流器测试类
 * 覆盖: 令牌桶、滑动窗口、固定窗口、漏桶算法
 *
 * @author AllToolkit
 * @version 1.0.0
 */

import Foundation
import XCTest

// MARK: - 令牌桶测试

class TokenBucketTest: XCTestCase {
    
    // MARK: 基础功能测试
    
    func testBasicAcquire() {
        let bucket = TokenBucket(capacity: 10, refillRate: 1.0)
        
        // 应该能获取令牌
        for _ in 0..<10 {
            let result = bucket.tryAcquire()
            XCTAssertTrue(result.allowed, "Should be allowed")
        }
        
        // 第 11 次应该被限制
        let result = bucket.tryAcquire()
        XCTAssertFalse(result.allowed, "Should be limited")
        XCTAssertGreaterThan(result.waitTime, 0, "Should have wait time")
    }
    
    func testTokenRefill() {
        let bucket = TokenBucket(capacity: 5, refillRate: 10.0) // 每秒补充 10 个令牌
        
        // 消耗所有令牌
        for _ in 0..<5 {
            _ = bucket.tryAcquire()
        }
        
        // 等待令牌补充
        Thread.sleep(forTimeInterval: 0.3) // 应该补充 3 个令牌
        
        // 应该能获取新令牌
        let result = bucket.tryAcquire()
        XCTAssertTrue(result.allowed, "Should be allowed after refill")
    }
    
    func testRemainingCount() {
        let bucket = TokenBucket(capacity: 5, refillRate: 1.0)
        
        XCTAssertEqual(bucket.currentTokens, 5, "Should start with full bucket")
        
        _ = bucket.tryAcquire()
        XCTAssertEqual(bucket.currentTokens, 4, "Should have 4 tokens left")
        
        _ = bucket.tryAcquire(tokens: 2)
        XCTAssertEqual(bucket.currentTokens, 2, "Should have 2 tokens left")
    }
    
    func testReset() {
        let bucket = TokenBucket(capacity: 10, refillRate: 1.0)
        
        // 消耗所有令牌
        for _ in 0..<10 {
            _ = bucket.tryAcquire()
        }
        
        bucket.reset()
        XCTAssertEqual(bucket.currentTokens, 10, "Should be reset to full")
        
        let result = bucket.tryAcquire()
        XCTAssertTrue(result.allowed, "Should be allowed after reset")
    }
    
    // MARK: 便捷方法测试
    
    func testPerSecondConvenience() {
        let bucket = TokenBucket.perSecond(10)
        
        for _ in 0..<10 {
            let result = bucket.tryAcquire()
            XCTAssertTrue(result.allowed, "Should allow 10 per second")
        }
        
        XCTAssertFalse(bucket.tryAcquire().allowed, "Should be limited after 10")
    }
    
    func testPerMinuteConvenience() {
        let bucket = TokenBucket.perMinute(60) // 每分钟 60 个 = 每秒 1 个
        XCTAssertEqual(bucket.currentTokens, 60, "Should have capacity of 60")
    }
    
    func testPerHourConvenience() {
        let bucket = TokenBucket.perHour(3600) // 每小时 3600 个 = 每秒 1 个
        XCTAssertEqual(bucket.currentTokens, 3600, "Should have capacity of 3600")
    }
}

// MARK: - 滑动窗口测试

class SlidingWindowTest: XCTestCase {
    
    func testBasicAcquire() {
        let window = SlidingWindow(limit: 5, windowSize: 1.0)
        
        // 应该能通过 5 次
        for _ in 0..<5 {
            let result = window.tryAcquire()
            XCTAssertTrue(result.allowed, "Should be allowed")
        }
        
        // 第 6 次应该被限制
        let result = window.tryAcquire()
        XCTAssertFalse(result.allowed, "Should be limited")
    }
    
    func testWindowSliding() {
        let window = SlidingWindow(limit: 3, windowSize: 1.0)
        
        // 发送 3 个请求
        for _ in 0..<3 {
            _ = window.tryAcquire()
        }
        
        // 应该被限制
        XCTAssertFalse(window.tryAcquire().allowed, "Should be limited")
        
        // 等待窗口滑动
        Thread.sleep(forTimeInterval: 1.1)
        
        // 应该能通过
        let result = window.tryAcquire()
        XCTAssertTrue(result.allowed, "Should be allowed after window slides")
    }
    
    func testCurrentCount() {
        let window = SlidingWindow(limit: 5, windowSize: 1.0)
        
        XCTAssertEqual(window.currentCount, 0, "Should start with 0")
        
        _ = window.tryAcquire()
        XCTAssertEqual(window.currentCount, 1, "Should have 1 request")
        
        _ = window.tryAcquire()
        _ = window.tryAcquire()
        XCTAssertEqual(window.currentCount, 3, "Should have 3 requests")
    }
    
    func testReset() {
        let window = SlidingWindow(limit: 5, windowSize: 1.0)
        
        for _ in 0..<5 {
            _ = window.tryAcquire()
        }
        
        window.reset()
        XCTAssertEqual(window.currentCount, 0, "Should be reset to 0")
        
        let result = window.tryAcquire()
        XCTAssertTrue(result.allowed, "Should be allowed after reset")
    }
    
    func testWaitTimeCalculation() {
        let window = SlidingWindow(limit: 2, windowSize: 2.0)
        
        _ = window.tryAcquire()
        _ = window.tryAcquire()
        
        let result = window.tryAcquire()
        XCTAssertFalse(result.allowed, "Should be limited")
        XCTAssertGreaterThan(result.waitTime, 0, "Should have wait time")
        XCTAssertLessThanOrEqual(result.waitTime, 2.0, "Wait time should not exceed window")
    }
    
    // MARK: 便捷方法测试
    
    func testPerSecondConvenience() {
        let window = SlidingWindow.perSecond(5)
        
        for _ in 0..<5 {
            XCTAssertTrue(window.tryAcquire().allowed, "Should allow 5 per second")
        }
        
        XCTAssertFalse(window.tryAcquire().allowed, "Should be limited")
    }
    
    func testPerMinuteConvenience() {
        let window = SlidingWindow.perMinute(60)
        XCTAssertEqual(window.currentCount, 0, "Should start with 0")
    }
    
    func testPerHourConvenience() {
        let window = SlidingWindow.perHour(3600)
        XCTAssertEqual(window.currentCount, 0, "Should start with 0")
    }
}

// MARK: - 固定窗口测试

class FixedWindowTest: XCTestCase {
    
    func testBasicAcquire() {
        let window = FixedWindow(limit: 5, windowSize: 1.0)
        
        for _ in 0..<5 {
            let result = window.tryAcquire()
            XCTAssertTrue(result.allowed, "Should be allowed")
        }
        
        let result = window.tryAcquire()
        XCTAssertFalse(result.allowed, "Should be limited")
    }
    
    func testWindowReset() {
        let window = FixedWindow(limit: 3, windowSize: 1.0)
        
        // 发送 3 个请求
        for _ in 0..<3 {
            _ = window.tryAcquire()
        }
        
        XCTAssertFalse(window.tryAcquire().allowed, "Should be limited")
        
        // 等待窗口重置
        Thread.sleep(forTimeInterval: 1.1)
        
        // 应该能通过
        let result = window.tryAcquire()
        XCTAssertTrue(result.allowed, "Should be allowed after window reset")
    }
    
    func testCurrentCount() {
        let window = FixedWindow(limit: 5, windowSize: 1.0)
        
        XCTAssertEqual(window.currentCount, 0, "Should start with 0")
        
        _ = window.tryAcquire()
        XCTAssertEqual(window.currentCount, 1, "Should have 1 request")
    }
    
    func testReset() {
        let window = FixedWindow(limit: 5, windowSize: 1.0)
        
        for _ in 0..<5 {
            _ = window.tryAcquire()
        }
        
        window.reset()
        XCTAssertEqual(window.currentCount, 0, "Should be reset to 0")
        
        let result = window.tryAcquire()
        XCTAssertTrue(result.allowed, "Should be allowed after reset")
    }
    
    func testResultProperties() {
        let window = FixedWindow(limit: 10, windowSize: 1.0)
        
        let result = window.tryAcquire()
        
        XCTAssertEqual(result.limit, 10, "Limit should be 10")
        XCTAssertEqual(result.remaining, 9, "Should have 9 remaining")
        XCTAssertEqual(result.waitTime, 0, "Wait time should be 0 when allowed")
        XCTAssertGreaterThan(result.resetTime, 0, "Should have reset time")
    }
    
    // MARK: 便捷方法测试
    
    func testPerSecondConvenience() {
        let window = FixedWindow.perSecond(5)
        
        for _ in 0..<5 {
            XCTAssertTrue(window.tryAcquire().allowed, "Should allow 5 per second")
        }
        
        XCTAssertFalse(window.tryAcquire().allowed, "Should be limited")
    }
    
    func testPerMinuteConvenience() {
        let window = FixedWindow.perMinute(60)
        XCTAssertEqual(window.currentCount, 0, "Should start with 0")
    }
    
    func testPerHourConvenience() {
        let window = FixedWindow.perHour(3600)
        XCTAssertEqual(window.currentCount, 0, "Should start with 0")
    }
}

// MARK: - 漏桶测试

class LeakyBucketTest: XCTestCase {
    
    func testBasicAcquire() {
        let bucket = LeakyBucket(capacity: 5, leakRate: 1.0)
        
        for _ in 0..<5 {
            let result = bucket.tryAcquire()
            XCTAssertTrue(result.allowed, "Should be allowed")
        }
        
        let result = bucket.tryAcquire()
        XCTAssertFalse(result.allowed, "Should be limited")
    }
    
    func testLeakRate() {
        let bucket = LeakyBucket(capacity: 5, leakRate: 10.0) // 每秒漏出 10 个
        
        // 填满桶
        for _ in 0..<5 {
            _ = bucket.tryAcquire()
        }
        
        // 等待漏出
        Thread.sleep(forTimeInterval: 0.5) // 应该漏出 5 个
        
        // 应该能通过
        let result = bucket.tryAcquire()
        XCTAssertTrue(result.allowed, "Should be allowed after leak")
    }
    
    func testCurrentWater() {
        let bucket = LeakyBucket(capacity: 5, leakRate: 1.0)
        
        XCTAssertEqual(bucket.currentWater, 0, "Should start empty")
        
        _ = bucket.tryAcquire()
        XCTAssertEqual(bucket.currentWater, 1, "Should have 1 water")
        
        _ = bucket.tryAcquire()
        XCTAssertEqual(bucket.currentWater, 2, "Should have 2 water")
    }
    
    func testReset() {
        let bucket = LeakyBucket(capacity: 5, leakRate: 1.0)
        
        for _ in 0..<5 {
            _ = bucket.tryAcquire()
        }
        
        bucket.reset()
        XCTAssertEqual(bucket.currentWater, 0, "Should be reset to 0")
        
        let result = bucket.tryAcquire()
        XCTAssertTrue(result.allowed, "Should be allowed after reset")
    }
}

// MARK: - 并发限流器测试

class ConcurrencyLimiterTest: XCTestCase {
    
    func testBasicAcquireRelease() {
        let limiter = ConcurrencyLimiter(maxConcurrency: 3)
        
        XCTAssertEqual(limiter.availableConcurrency, 3, "Should have 3 available")
        
        XCTAssertTrue(limiter.acquire(timeout: 0.1), "Should acquire")
        XCTAssertEqual(limiter.currentConcurrency, 1, "Should have 1 current")
        XCTAssertEqual(limiter.availableConcurrency, 2, "Should have 2 available")
        
        limiter.release()
        XCTAssertEqual(limiter.currentConcurrency, 0, "Should have 0 after release")
        XCTAssertEqual(limiter.availableConcurrency, 3, "Should have 3 available")
    }
    
    func testMaxConcurrency() {
        let limiter = ConcurrencyLimiter(maxConcurrency: 2)
        
        XCTAssertTrue(limiter.acquire(timeout: 0.1), "Should acquire 1")
        XCTAssertTrue(limiter.acquire(timeout: 0.1), "Should acquire 2")
        XCTAssertFalse(limiter.acquire(timeout: 0.1), "Should fail for 3")
        
        limiter.release()
        XCTAssertEqual(limiter.availableConcurrency, 1, "Should have 1 available after release")
        
        XCTAssertTrue(limiter.acquire(timeout: 0.1), "Should acquire after release")
    }
    
    func testTimeout() {
        let limiter = ConcurrencyLimiter(maxConcurrency: 1)
        
        XCTAssertTrue(limiter.acquire(timeout: 0.1), "Should acquire first")
        
        // 第二次应该超时
        let startTime = Date()
        let result = limiter.acquire(timeout: 0.2)
        let elapsed = Date().timeIntervalSince(startTime)
        
        XCTAssertFalse(result, "Should timeout")
        XCTAssertGreaterThanOrEqual(elapsed, 0.2, "Should wait at least timeout duration")
    }
}

// MARK: - 组合限流器测试

class CompositeRateLimiterTest: XCTestCase {
    
    func testAllPassStrategy() {
        let limiter1 = FixedWindow(limit: 3, windowSize: 1.0)
        let limiter2 = FixedWindow(limit: 5, windowSize: 1.0)
        
        let composite = CompositeRateLimiter([
            AnyRateLimiter(limiter1),
            AnyRateLimiter(limiter2)
        ], strategy: .allPass)
        
        // 前 3 次应该都通过
        for i in 0..<3 {
            let result = composite.tryAcquire()
            XCTAssertTrue(result.allowed, "Should pass on request \(i + 1)")
        }
        
        // 第 4 次应该被限制（因为 limiter1 限制 3 个）
        let result = composite.tryAcquire()
        XCTAssertFalse(result.allowed, "Should be limited by limiter1")
    }
    
    func testAnyPassStrategy() {
        // 创建一个已满的限流器和一个未满的限流器
        let limiter1 = FixedWindow(limit: 1, windowSize: 10.0)
        let limiter2 = FixedWindow(limit: 5, windowSize: 1.0)
        
        // 先消耗 limiter1 的配额
        _ = limiter1.tryAcquire()
        
        let composite = CompositeRateLimiter([
            AnyRateLimiter(limiter1),
            AnyRateLimiter(limiter2)
        ], strategy: .anyPass)
        
        // 应该通过，因为 limiter2 还有配额
        let result = composite.tryAcquire()
        XCTAssertTrue(result.allowed, "Should pass because limiter2 allows")
    }
    
    func testEmptyLimiters() {
        let composite = CompositeRateLimiter([], strategy: .allPass)
        
        let result = composite.tryAcquire()
        XCTAssertTrue(result.allowed, "Empty limiters should allow by default")
    }
}

// MARK: - 异步测试

class AsyncRateLimiterTest: XCTestCase {
    
    func testAsyncAcquire() {
        let bucket = TokenBucket(capacity: 1, refillRate: 10.0)
        
        // 先消耗配额
        XCTAssertTrue(bucket.tryAcquire().allowed, "First should succeed")
        
        let expectation = XCTestExpectation(description: "Async acquire")
        
        bucket.acquireAsync(maxWait: 0.5) { success in
            XCTAssertTrue(success, "Should acquire after waiting")
            expectation.fulfill()
        }
        
        wait(for: [expectation], timeout: 1.0)
    }
    
    func testAsyncAcquireTimeout() {
        let window = SlidingWindow(limit: 1, windowSize: 10.0)
        
        // 先消耗配额
        XCTAssertTrue(window.tryAcquire().allowed, "First should succeed")
        
        let expectation = XCTestExpectation(description: "Async timeout")
        
        window.acquireAsync(maxWait: 0.1) { success in
            XCTAssertFalse(success, "Should timeout")
            expectation.fulfill()
        }
        
        wait(for: [expectation], timeout: 0.5)
    }
}

// MARK: - 结果测试

class RateLimitResultTest: XCTestCase {
    
    func testResultProperties() {
        let result = RateLimitResult(
            allowed: true,
            remaining: 5,
            waitTime: 0,
            limit: 10,
            resetTime: Date().timeIntervalSince1970 + 60
        )
        
        XCTAssertTrue(result.allowed, "Should be allowed")
        XCTAssertEqual(result.remaining, 5, "Should have 5 remaining")
        XCTAssertEqual(result.waitTime, 0, "Should have 0 wait time")
        XCTAssertEqual(result.limit, 10, "Should have limit of 10")
        XCTAssertGreaterThan(result.resetTime, 0, "Should have valid reset time")
    }
    
    func testDeniedResult() {
        let result = RateLimitResult(
            allowed: false,
            remaining: 0,
            waitTime: 2.5,
            limit: 10,
            resetTime: Date().timeIntervalSince1970 + 2.5
        )
        
        XCTAssertFalse(result.allowed, "Should be denied")
        XCTAssertEqual(result.remaining, 0, "Should have 0 remaining")
        XCTAssertEqual(result.waitTime, 2.5, "Should have correct wait time")
    }
}