"""
Rate Limiter Utils 测试用例
"""

import time
import threading
import unittest
from mod import (
    TokenBucket,
    LeakyBucket,
    SlidingWindow,
    FixedWindow,
    RateLimiter,
    MultiRateLimiter,
    create_token_bucket,
    create_leaky_bucket,
    create_sliding_window,
    create_fixed_window,
)


class TestTokenBucket(unittest.TestCase):
    """令牌桶测试"""
    
    def test_initial_state(self):
        """测试初始状态"""
        bucket = TokenBucket(10, 2.0)
        self.assertEqual(bucket.capacity, 10)
        self.assertEqual(bucket.refill_rate, 2.0)
        self.assertEqual(bucket.available, 10.0)
    
    def test_acquire_success(self):
        """测试成功获取令牌"""
        bucket = TokenBucket(10, 2.0)
        self.assertTrue(bucket.acquire(5))
        self.assertAlmostEqual(bucket.available, 5.0, places=1)
    
    def test_acquire_fail(self):
        """测试获取令牌失败"""
        bucket = TokenBucket(5, 1.0)
        self.assertFalse(bucket.acquire(10))
    
    def test_refill(self):
        """测试令牌填充"""
        bucket = TokenBucket(10, 10.0)  # 每秒10个
        bucket.acquire(10)
        # 由于执行时间可能有微小填充，使用 assertLess
        self.assertLess(bucket.available, 1.0)
        time.sleep(0.5)  # 应该填充约5个
        self.assertGreaterEqual(bucket.available, 4.0)
    
    def test_wait_for_success(self):
        """测试等待获取成功"""
        bucket = TokenBucket(10, 100.0)  # 快速填充
        self.assertTrue(bucket.wait_for(5, timeout=1.0))
    
    def test_wait_for_timeout(self):
        """测试等待超时"""
        bucket = TokenBucket(1, 0.1)  # 非常慢的填充
        bucket.acquire(1)  # 消耗唯一的令牌
        start = time.time()
        result = bucket.wait_for(5, timeout=0.2)
        elapsed = time.time() - start
        self.assertFalse(result)
        self.assertLess(elapsed, 0.5)
    
    def test_invalid_parameters(self):
        """测试无效参数"""
        with self.assertRaises(ValueError):
            TokenBucket(0, 1.0)
        with self.assertRaises(ValueError):
            TokenBucket(10, 0)
        with self.assertRaises(ValueError):
            TokenBucket(-1, 1.0)
    
    def test_thread_safety(self):
        """测试线程安全"""
        bucket = TokenBucket(100, 1000.0)
        success_count = [0]
        lock = threading.Lock()
        
        def worker():
            for _ in range(10):
                if bucket.acquire(1):
                    with lock:
                        success_count[0] += 1
        
        threads = [threading.Thread(target=worker) for _ in range(10)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()
        
        self.assertEqual(success_count[0], 100)


class TestLeakyBucket(unittest.TestCase):
    """漏桶测试"""
    
    def test_initial_state(self):
        """测试初始状态"""
        bucket = LeakyBucket(10, 2.0)
        self.assertEqual(bucket.capacity, 10)
        self.assertEqual(bucket.leak_rate, 2.0)
        self.assertEqual(bucket.available, 10.0)
    
    def test_acquire_success(self):
        """测试成功获取"""
        bucket = LeakyBucket(10, 2.0)
        self.assertTrue(bucket.acquire(5))
        self.assertAlmostEqual(bucket.available, 5.0, places=1)
    
    def test_acquire_fail(self):
        """测试获取失败"""
        bucket = LeakyBucket(5, 1.0)
        self.assertFalse(bucket.acquire(10))
    
    def test_leak(self):
        """测试漏水"""
        bucket = LeakyBucket(10, 10.0)  # 每秒漏10个
        bucket.acquire(10)
        time.sleep(0.5)  # 应该漏掉5个
        self.assertGreaterEqual(bucket.available, 4.0)
    
    def test_wait_for(self):
        """测试等待"""
        bucket = LeakyBucket(10, 100.0)
        self.assertTrue(bucket.wait_for(5, timeout=1.0))
    
    def test_invalid_parameters(self):
        """测试无效参数"""
        with self.assertRaises(ValueError):
            LeakyBucket(0, 1.0)
        with self.assertRaises(ValueError):
            LeakyBucket(10, 0)


class TestSlidingWindow(unittest.TestCase):
    """滑动窗口测试"""
    
    def test_initial_state(self):
        """测试初始状态"""
        window = SlidingWindow(10, 1.0)
        self.assertEqual(window.max_requests, 10)
        self.assertEqual(window.window_seconds, 1.0)
        self.assertEqual(window.current_count, 0)
        self.assertEqual(window.available, 10.0)
    
    def test_acquire_success(self):
        """测试成功获取"""
        window = SlidingWindow(10, 1.0)
        self.assertTrue(window.acquire(5))
        self.assertEqual(window.current_count, 5)
    
    def test_acquire_fail(self):
        """测试获取失败"""
        window = SlidingWindow(5, 1.0)
        self.assertFalse(window.acquire(10))
    
    def test_window_slide(self):
        """测试窗口滑动"""
        window = SlidingWindow(10, 0.3)
        window.acquire(10)
        self.assertEqual(window.available, 0)
        time.sleep(0.4)  # 等待窗口过期
        self.assertTrue(window.acquire(1))
    
    def test_wait_for(self):
        """测试等待"""
        window = SlidingWindow(10, 0.5)
        self.assertTrue(window.wait_for(5, timeout=1.0))
    
    def test_invalid_parameters(self):
        """测试无效参数"""
        with self.assertRaises(ValueError):
            SlidingWindow(0, 1.0)
        with self.assertRaises(ValueError):
            SlidingWindow(10, 0)


class TestFixedWindow(unittest.TestCase):
    """固定窗口测试"""
    
    def test_initial_state(self):
        """测试初始状态"""
        window = FixedWindow(10, 1.0)
        self.assertEqual(window.max_requests, 10)
        self.assertEqual(window.window_seconds, 1.0)
        self.assertEqual(window.current_count, 0)
        self.assertEqual(window.available, 10.0)
    
    def test_acquire_success(self):
        """测试成功获取"""
        window = FixedWindow(10, 1.0)
        self.assertTrue(window.acquire(5))
        self.assertEqual(window.current_count, 5)
    
    def test_acquire_fail(self):
        """测试获取失败"""
        window = FixedWindow(5, 1.0)
        self.assertFalse(window.acquire(10))
    
    def test_window_reset(self):
        """测试窗口重置"""
        window = FixedWindow(10, 0.3)
        window.acquire(10)
        self.assertEqual(window.current_count, 10)
        time.sleep(0.4)  # 等待窗口重置
        self.assertTrue(window.acquire(1))
    
    def test_time_until_reset(self):
        """测试重置时间"""
        window = FixedWindow(10, 1.0)
        time_until_reset = window.time_until_reset
        self.assertGreater(time_until_reset, 0)
        self.assertLessEqual(time_until_reset, 1.0)
    
    def test_invalid_parameters(self):
        """测试无效参数"""
        with self.assertRaises(ValueError):
            FixedWindow(0, 1.0)
        with self.assertRaises(ValueError):
            FixedWindow(10, 0)


class TestRateLimiter(unittest.TestCase):
    """综合速率限制器测试"""
    
    def test_token_bucket_algorithm(self):
        """测试令牌桶算法"""
        limiter = RateLimiter(10, 1.0, RateLimiter.ALGORITHM_TOKEN_BUCKET)
        self.assertEqual(limiter.algorithm, 'token_bucket')
        self.assertTrue(limiter.acquire(5))
    
    def test_leaky_bucket_algorithm(self):
        """测试漏桶算法"""
        limiter = RateLimiter(10, 1.0, RateLimiter.ALGORITHM_LEAKY_BUCKET)
        self.assertEqual(limiter.algorithm, 'leaky_bucket')
        self.assertTrue(limiter.acquire(5))
    
    def test_sliding_window_algorithm(self):
        """测试滑动窗口算法"""
        limiter = RateLimiter(10, 1.0, RateLimiter.ALGORITHM_SLIDING_WINDOW)
        self.assertEqual(limiter.algorithm, 'sliding_window')
        self.assertTrue(limiter.acquire(5))
    
    def test_fixed_window_algorithm(self):
        """测试固定窗口算法"""
        limiter = RateLimiter(10, 1.0, RateLimiter.ALGORITHM_FIXED_WINDOW)
        self.assertEqual(limiter.algorithm, 'fixed_window')
        self.assertTrue(limiter.acquire(5))
    
    def test_invalid_algorithm(self):
        """测试无效算法"""
        with self.assertRaises(ValueError):
            RateLimiter(10, 1.0, 'invalid')
    
    def test_decorator(self):
        """测试装饰器"""
        # 使用滑动窗口确保精确限流
        limiter = RateLimiter(5, 10.0, RateLimiter.ALGORITHM_SLIDING_WINDOW)
        
        @limiter.limit(on_limit=lambda: "limited")
        def api_call():
            return "success"
        
        results = [api_call() for _ in range(10)]
        success_count = sum(1 for r in results if r == "success")
        limited_count = sum(1 for r in results if r == "limited")
        
        self.assertEqual(success_count, 5)
        self.assertEqual(limited_count, 5)
    
    def test_decorator_with_timeout(self):
        """测试带超时的装饰器"""
        limiter = RateLimiter(1, 10.0)  # 非常慢
        
        @limiter.limit(timeout=0.1, on_limit=lambda: "timeout")
        def slow_call():
            return "success"
        
        # 第一次应该成功
        self.assertEqual(slow_call(), "success")
        # 第二次应该超时
        self.assertEqual(slow_call(), "timeout")


class TestMultiRateLimiter(unittest.TestCase):
    """多键速率限制器测试"""
    
    def test_different_keys(self):
        """测试不同键独立限制"""
        limiter = MultiRateLimiter(5, 1.0)
        
        # 用户A的请求
        for _ in range(5):
            self.assertTrue(limiter.acquire("user_a"))
        self.assertFalse(limiter.acquire("user_a"))
        
        # 用户B应该还有配额
        self.assertTrue(limiter.acquire("user_b"))
    
    def test_reset(self):
        """测试重置"""
        limiter = MultiRateLimiter(5, 1.0)
        
        for _ in range(5):
            limiter.acquire("user_a")
        
        self.assertFalse(limiter.acquire("user_a"))
        limiter.reset("user_a")
        self.assertTrue(limiter.acquire("user_a"))
    
    def test_reset_all(self):
        """测试重置所有"""
        limiter = MultiRateLimiter(5, 1.0)
        
        limiter.acquire("user_a")
        limiter.acquire("user_b")
        
        self.assertEqual(limiter.key_count, 2)
        limiter.reset_all()
        self.assertEqual(limiter.key_count, 0)
    
    def test_max_keys(self):
        """测试最大键数限制"""
        limiter = MultiRateLimiter(5, 1.0, max_keys=5)
        
        for i in range(10):
            limiter.acquire(f"key_{i}")
        
        # 超过限制后，应该清空旧键
        self.assertLessEqual(limiter.key_count, 5)


class TestConvenienceFunctions(unittest.TestCase):
    """便捷函数测试"""
    
    def test_create_token_bucket(self):
        bucket = create_token_bucket(10, 5.0)
        self.assertIsInstance(bucket, TokenBucket)
        self.assertEqual(bucket.capacity, 10)
    
    def test_create_leaky_bucket(self):
        bucket = create_leaky_bucket(10, 5.0)
        self.assertIsInstance(bucket, LeakyBucket)
        self.assertEqual(bucket.capacity, 10)
    
    def test_create_sliding_window(self):
        window = create_sliding_window(10, 1.0)
        self.assertIsInstance(window, SlidingWindow)
        self.assertEqual(window.max_requests, 10)
    
    def test_create_fixed_window(self):
        window = create_fixed_window(10, 1.0)
        self.assertIsInstance(window, FixedWindow)
        self.assertEqual(window.max_requests, 10)


class TestConcurrency(unittest.TestCase):
    """并发测试"""
    
    def test_high_concurrency_token_bucket(self):
        """高并发令牌桶测试"""
        bucket = TokenBucket(1000, 1000.0)
        results = []
        lock = threading.Lock()
        
        def worker():
            success = bucket.acquire(1)
            with lock:
                results.append(success)
        
        threads = [threading.Thread(target=worker) for _ in range(2000)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()
        
        success_count = sum(results)
        self.assertGreater(success_count, 900)  # 允许一些竞争
        self.assertLessEqual(success_count, 2000)
    
    def test_high_concurrency_sliding_window(self):
        """高并发滑动窗口测试"""
        window = SlidingWindow(100, 1.0)
        results = []
        lock = threading.Lock()
        
        def worker():
            success = window.acquire(1)
            with lock:
                results.append(success)
        
        threads = [threading.Thread(target=worker) for _ in range(200)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()
        
        success_count = sum(results)
        self.assertGreater(success_count, 90)
        self.assertLessEqual(success_count, 100)


if __name__ == '__main__':
    unittest.main()