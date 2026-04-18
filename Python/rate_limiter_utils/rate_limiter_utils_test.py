"""
rate_limiter_utils 测试套件

测试所有速率限制算法的正确性和边界情况。
"""

import unittest
import time
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed

from mod import (
    RateLimitResult,
    RateLimiterBase,
    FixedWindowRateLimiter,
    SlidingWindowRateLimiter,
    TokenBucketRateLimiter,
    LeakyBucketRateLimiter,
    RateLimiterRegistry,
    RateLimitExceeded,
    rate_limit,
    create_limiter,
)


class TestRateLimitResult(unittest.TestCase):
    """测试 RateLimitResult 类"""
    
    def test_allowed_result(self):
        """测试允许的结果"""
        result = RateLimitResult(True, 5, 100.0)
        self.assertTrue(result.allowed)
        self.assertEqual(result.remaining, 5)
        self.assertEqual(result.reset_time, 100.0)
        self.assertEqual(result.retry_after, 0)
    
    def test_rejected_result(self):
        """测试拒绝的结果"""
        result = RateLimitResult(False, 0, 100.0, 5.5)
        self.assertFalse(result.allowed)
        self.assertEqual(result.remaining, 0)
        self.assertEqual(result.retry_after, 5.5)
    
    def test_to_dict(self):
        """测试转换为字典"""
        result = RateLimitResult(True, 3, 100.0, 0)
        d = result.to_dict()
        self.assertIsInstance(d, dict)
        self.assertEqual(d['allowed'], True)
        self.assertEqual(d['remaining'], 3)
    
    def test_repr(self):
        """测试字符串表示"""
        result = RateLimitResult(True, 5, 100.0, 2.5)
        s = repr(result)
        self.assertIn('RateLimitResult', s)
        self.assertIn('allowed=True', s)


class TestFixedWindowRateLimiter(unittest.TestCase):
    """测试固定窗口算法"""
    
    def test_basic_allow(self):
        """测试基本允许功能"""
        limiter = FixedWindowRateLimiter(5, 10)
        for i in range(5):
            result = limiter.try_acquire()
            self.assertTrue(result.allowed, f"请求 {i+1} 应该被允许")
            self.assertEqual(result.remaining, 4 - i)
    
    def test_limit_exceeded(self):
        """测试超限拒绝"""
        limiter = FixedWindowRateLimiter(3, 10)
        for _ in range(3):
            limiter.try_acquire()
        
        result = limiter.try_acquire()
        self.assertFalse(result.allowed)
        self.assertEqual(result.remaining, 0)
        self.assertGreater(result.retry_after, 0)
    
    def test_window_reset(self):
        """测试窗口重置"""
        limiter = FixedWindowRateLimiter(2, 0.1)  # 100ms 窗口
        
        # 消耗配额
        limiter.try_acquire()
        limiter.try_acquire()
        
        # 应该被拒绝
        result = limiter.try_acquire()
        self.assertFalse(result.allowed)
        
        # 等待窗口重置
        time.sleep(0.15)
        
        # 应该被允许
        result = limiter.try_acquire()
        self.assertTrue(result.allowed)
    
    def test_reset(self):
        """测试手动重置"""
        limiter = FixedWindowRateLimiter(3, 10)
        
        limiter.try_acquire()
        limiter.try_acquire()
        
        limiter.reset()
        
        # 重置后应该有完整配额
        for i in range(3):
            result = limiter.try_acquire()
            self.assertTrue(result.allowed)
    
    def test_get_state(self):
        """测试获取状态"""
        limiter = FixedWindowRateLimiter(5, 10)
        limiter.try_acquire()
        
        state = limiter.get_state()
        
        self.assertEqual(state['type'], 'fixed_window')
        self.assertEqual(state['count'], 1)
        self.assertEqual(state['max_requests'], 5)
    
    def test_multi_tokens(self):
        """测试多令牌请求"""
        limiter = FixedWindowRateLimiter(10, 10)
        
        result = limiter.try_acquire(5)  # 一次请求5个
        self.assertTrue(result.allowed)
        self.assertEqual(result.remaining, 5)
        
        result = limiter.try_acquire(6)  # 请求6个，超过剩余
        self.assertFalse(result.allowed)


class TestSlidingWindowRateLimiter(unittest.TestCase):
    """测试滑动窗口算法"""
    
    def test_basic_allow(self):
        """测试基本允许功能"""
        limiter = SlidingWindowRateLimiter(5, 10)
        for i in range(5):
            result = limiter.try_acquire()
            self.assertTrue(result.allowed)
    
    def test_limit_exceeded(self):
        """测试超限拒绝"""
        limiter = SlidingWindowRateLimiter(3, 10)
        
        for _ in range(3):
            limiter.try_acquire()
        
        result = limiter.try_acquire()
        self.assertFalse(result.allowed)
    
    def test_sliding_expiration(self):
        """测试滑动过期"""
        limiter = SlidingWindowRateLimiter(2, 0.2)  # 200ms 窗口
        
        limiter.try_acquire()  # t=0
        time.sleep(0.1)
        limiter.try_acquire()  # t=100ms
        
        # 应该被拒绝
        result = limiter.try_acquire()
        self.assertFalse(result.allowed)
        
        time.sleep(0.15)  # t=250ms，第一个请求已过期
        
        # 应该被允许（第一个请求已滑出窗口）
        result = limiter.try_acquire()
        self.assertTrue(result.allowed)
    
    def test_reset(self):
        """测试重置"""
        limiter = SlidingWindowRateLimiter(5, 10)
        
        for _ in range(5):
            limiter.try_acquire()
        
        limiter.reset()
        
        result = limiter.try_acquire()
        self.assertTrue(result.allowed)
    
    def test_get_state(self):
        """测试获取状态"""
        limiter = SlidingWindowRateLimiter(5, 10)
        limiter.try_acquire()
        
        state = limiter.get_state()
        
        self.assertEqual(state['type'], 'sliding_window')
        self.assertEqual(state['count'], 1)
        self.assertIsNotNone(state['oldest_request'])


class TestTokenBucketRateLimiter(unittest.TestCase):
    """测试令牌桶算法"""
    
    def test_basic_allow(self):
        """测试基本允许功能"""
        limiter = TokenBucketRateLimiter(5, 10)
        for i in range(5):
            result = limiter.try_acquire()
            self.assertTrue(result.allowed)
    
    def test_bucket_exhausted(self):
        """测试令牌耗尽"""
        limiter = TokenBucketRateLimiter(3, 10)
        
        for _ in range(3):
            limiter.try_acquire()
        
        result = limiter.try_acquire()
        self.assertFalse(result.allowed)
    
    def test_token_refill(self):
        """测试令牌补充"""
        # 每秒补充10个令牌
        limiter = TokenBucketRateLimiter(10, 1)  # 10个令牌，1秒填满
        
        # 耗尽令牌
        for _ in range(10):
            limiter.try_acquire()
        
        result = limiter.try_acquire()
        self.assertFalse(result.allowed)
        
        # 等待补充
        time.sleep(0.5)  # 应该补充约5个令牌
        
        result = limiter.try_acquire()
        self.assertTrue(result.allowed, "应该有补充的令牌")
    
    def test_burst_traffic(self):
        """测试突发流量"""
        limiter = TokenBucketRateLimiter(10, 1)
        
        # 允许突发：桶满时可以连续请求
        results = [limiter.try_acquire() for _ in range(10)]
        self.assertTrue(all(r.allowed for r in results))
    
    def test_initial_tokens(self):
        """测试初始令牌数"""
        limiter = TokenBucketRateLimiter(10, 10, initial_tokens=5)
        
        state = limiter.get_state()
        # 允许微小的时间误差
        self.assertAlmostEqual(state['tokens'], 5, places=1)
    
    def test_reset(self):
        """测试重置"""
        limiter = TokenBucketRateLimiter(5, 10)
        
        for _ in range(5):
            limiter.try_acquire()
        
        limiter.reset()
        
        result = limiter.try_acquire()
        self.assertTrue(result.allowed)


class TestLeakyBucketRateLimiter(unittest.TestCase):
    """测试漏桶算法"""
    
    def test_basic_allow(self):
        """测试基本允许功能"""
        limiter = LeakyBucketRateLimiter(5, 10)  # 容量5，每秒漏10个
        for i in range(5):
            result = limiter.try_acquire()
            self.assertTrue(result.allowed)
    
    def test_bucket_full(self):
        """测试桶满拒绝"""
        limiter = LeakyBucketRateLimiter(3, 10)
        
        for _ in range(3):
            limiter.try_acquire()
        
        result = limiter.try_acquire()
        self.assertFalse(result.allowed)
    
    def test_constant_leak_rate(self):
        """测试恒定漏出速率"""
        limiter = LeakyBucketRateLimiter(10, 5)  # 容量10，每秒漏5个
        
        # 填满桶
        for _ in range(10):
            limiter.try_acquire()
        
        time.sleep(0.2)  # 漏出1个
        
        # 应该有空间了
        result = limiter.try_acquire()
        self.assertTrue(result.allowed)
    
    def test_get_state(self):
        """测试获取状态"""
        limiter = LeakyBucketRateLimiter(10, 5)
        limiter.try_acquire()
        
        state = limiter.get_state()
        
        self.assertEqual(state['type'], 'leaky_bucket')
        self.assertEqual(state['capacity'], 10)
        self.assertEqual(state['leak_rate'], 5)


class TestRateLimiterRegistry(unittest.TestCase):
    """测试速率限制器注册表"""
    
    def test_different_keys(self):
        """测试不同 key 独立计数"""
        registry = RateLimiterRegistry(FixedWindowRateLimiter, 2, 10)
        
        # user1 消耗配额
        registry.try_acquire('user1')
        registry.try_acquire('user1')
        
        # user1 应该被拒绝
        result = registry.try_acquire('user1')
        self.assertFalse(result.allowed)
        
        # user2 应该有独立配额
        result = registry.try_acquire('user2')
        self.assertTrue(result.allowed)
    
    def test_reset_specific_key(self):
        """测试重置特定 key"""
        registry = RateLimiterRegistry(FixedWindowRateLimiter, 2, 10)
        
        registry.try_acquire('user1')
        registry.try_acquire('user1')
        registry.try_acquire('user2')
        
        registry.reset('user1')
        
        # user1 重置后应该可用
        result = registry.try_acquire('user1')
        self.assertTrue(result.allowed)
        
        # user2 不受影响，仍有1个配额
        result = registry.try_acquire('user2')
        self.assertTrue(result.allowed)
    
    def test_get_state(self):
        """测试获取状态"""
        registry = RateLimiterRegistry(SlidingWindowRateLimiter, 5, 10)
        
        registry.try_acquire('user1')
        registry.try_acquire('user1')
        
        state = registry.get_state('user1')
        self.assertEqual(state['count'], 2)


class TestRateLimitDecorator(unittest.TestCase):
    """测试速率限制装饰器"""
    
    def test_decorator_allows(self):
        """测试装饰器允许请求"""
        limiter = TokenBucketRateLimiter(5, 10)
        
        @rate_limit(limiter)
        def my_func():
            return "success"
        
        result = my_func()
        self.assertEqual(result, "success")
    
    def test_decorator_rejects(self):
        """测试装饰器拒绝请求"""
        limiter = TokenBucketRateLimiter(1, 10)
        
        @rate_limit(limiter)
        def my_func():
            return "success"
        
        my_func()  # 消耗配额
        
        with self.assertRaises(RateLimitExceeded):
            my_func()
    
    def test_decorator_with_callback(self):
        """测试装饰器使用回调"""
        limiter = TokenBucketRateLimiter(1, 10)
        
        def on_reject(result):
            return f"rejected: retry after {result.retry_after:.2f}s"
        
        @rate_limit(limiter, on_reject=on_reject)
        def my_func():
            return "success"
        
        my_func()  # 消耗配额
        
        result = my_func()
        self.assertIn("rejected", result)


class TestCreateLimiter(unittest.TestCase):
    """测试便捷函数"""
    
    def test_create_fixed_window(self):
        limiter = create_limiter('fixed_window', 10, 60)
        self.assertIsInstance(limiter, FixedWindowRateLimiter)
    
    def test_create_sliding_window(self):
        limiter = create_limiter('sliding_window', 10, 60)
        self.assertIsInstance(limiter, SlidingWindowRateLimiter)
    
    def test_create_token_bucket(self):
        limiter = create_limiter('token_bucket', 10, 60)
        self.assertIsInstance(limiter, TokenBucketRateLimiter)
    
    def test_create_leaky_bucket(self):
        limiter = create_limiter('leaky_bucket', 10, 60)
        self.assertIsInstance(limiter, LeakyBucketRateLimiter)
    
    def test_invalid_algorithm(self):
        with self.assertRaises(ValueError):
            create_limiter('invalid', 10, 60)


class TestThreadSafety(unittest.TestCase):
    """测试线程安全性"""
    
    def test_concurrent_access(self):
        """测试并发访问"""
        limiter = TokenBucketRateLimiter(100, 1)
        results = []
        
        def make_request():
            result = limiter.try_acquire()
            results.append(result.allowed)
        
        threads = [threading.Thread(target=make_request) for _ in range(100)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()
        
        # 所有请求都应该成功（桶初始满）
        self.assertEqual(sum(results), 100)
    
    def test_concurrent_exceeded(self):
        """测试并发超限"""
        limiter = SlidingWindowRateLimiter(50, 1)
        allowed_count = 0
        lock = threading.Lock()
        
        def make_request():
            nonlocal allowed_count
            result = limiter.try_acquire()
            if result.allowed:
                with lock:
                    allowed_count += 1
        
        threads = [threading.Thread(target=make_request) for _ in range(100)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()
        
        # 应该恰好有50个成功
        self.assertEqual(allowed_count, 50)
    
    def test_registry_concurrent(self):
        """测试注册表并发访问"""
        registry = RateLimiterRegistry(TokenBucketRateLimiter, 10, 1)
        results = []
        
        def make_request(user_id):
            result = registry.try_acquire(f"user{user_id % 5}")
            results.append(result.allowed)
        
        with ThreadPoolExecutor(max_workers=20) as executor:
            futures = [executor.submit(make_request, i) for i in range(50)]
            for f in as_completed(futures):
                pass
        
        # 验证没有竞争条件导致的错误
        self.assertEqual(len(results), 50)


class TestEdgeCases(unittest.TestCase):
    """测试边界情况"""
    
    def test_zero_max_requests(self):
        """测试零配额"""
        limiter = FixedWindowRateLimiter(0, 10)
        result = limiter.try_acquire()
        self.assertFalse(result.allowed)
    
    def test_single_request_window(self):
        """测试单请求窗口"""
        limiter = FixedWindowRateLimiter(1, 10)
        
        result = limiter.try_acquire()
        self.assertTrue(result.allowed)
        
        result = limiter.try_acquire()
        self.assertFalse(result.allowed)
    
    def test_large_window(self):
        """测试大时间窗口"""
        limiter = SlidingWindowRateLimiter(1000, 3600)  # 1小时
        
        for _ in range(1000):
            result = limiter.try_acquire()
            self.assertTrue(result.allowed)
        
        result = limiter.try_acquire()
        self.assertFalse(result.allowed)
    
    def test_very_small_window(self):
        """测试极小时间窗口"""
        limiter = TokenBucketRateLimiter(10, 0.01)  # 10ms
        
        # 快速消耗配额
        for _ in range(10):
            limiter.try_acquire()
        
        result = limiter.try_acquire()
        self.assertFalse(result.allowed)
        
        time.sleep(0.02)  # 等待补充
        
        result = limiter.try_acquire()
        self.assertTrue(result.allowed)


if __name__ == '__main__':
    unittest.main(verbosity=2)