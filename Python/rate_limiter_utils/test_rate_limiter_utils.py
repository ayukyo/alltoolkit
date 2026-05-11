"""
Rate Limiter Utils 测试

测试所有速率限制算法的实现。
"""

import time
import threading
import unittest
from unittest.mock import patch
import sys
import os

# 添加父目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# 导入所有模块
from rate_limiter_utils import (
    TokenBucket, LeakyBucket, SlidingWindow, FixedWindow,
    RateLimiter, MultiRateLimiter, rate_limit, RateLimitExceeded,
    Algorithm
)
from rate_limiter_utils.token_bucket import AsyncTokenBucket
from rate_limiter_utils.sliding_window import SlidingWindowCounter
from rate_limiter_utils.fixed_window import FixedWindowKeyed
from rate_limiter_utils.leaky_bucket import LeakyBucketQueue
from rate_limiter_utils.decorators import (
    RateLimiterContext, async_rate_limit,
    rate_limit_per_argument, clear_limiters, list_limiters
)


class TestTokenBucket(unittest.TestCase):
    """令牌桶测试"""

    def setUp(self):
        # 使用固定时间，避免 mock 时间导致补充问题
        self.fixed_time = 1000.0
        self.bucket = TokenBucket(
            rate=10, capacity=20,
            time_func=lambda: self.fixed_time
        )

    def test_initial_tokens(self):
        """测试初始令牌数"""
        self.assertEqual(self.bucket.get_tokens(), 20)

    def test_consume_success(self):
        """测试成功消耗令牌"""
        self.assertTrue(self.bucket.consume(5))
        self.assertEqual(self.bucket.get_tokens(), 15)

    def test_consume_fail(self):
        """测试令牌不足"""
        self.assertFalse(self.bucket.consume(25))

    def test_token_refill(self):
        """测试令牌补充"""
        bucket = TokenBucket(rate=10, capacity=20)
        bucket.consume(20)  # 清空桶

        # 等待1秒，应该补充10个令牌
        time.sleep(1.1)
        self.assertGreaterEqual(bucket.get_tokens(), 10)

    def test_consume_or_wait(self):
        """测试等待消耗"""
        bucket = TokenBucket(rate=100, capacity=10, time_func=time.time)
        bucket.consume(10)  # 清空桶

        start = time.time()
        bucket.consume_or_wait(1, max_wait=0.5)
        elapsed = time.time() - start

        self.assertLess(elapsed, 1)

    def test_capacity_not_exceeded(self):
        """测试令牌数不超过容量"""
        bucket = TokenBucket(rate=100, capacity=10)
        time.sleep(0.5)  # 等待补充
        self.assertLessEqual(bucket.get_tokens(), 10)

    def test_reset(self):
        """测试重置"""
        self.bucket.consume(10)
        self.bucket.reset()
        self.assertEqual(self.bucket.get_tokens(), 20)

    def test_invalid_params(self):
        """测试无效参数"""
        with self.assertRaises(ValueError):
            TokenBucket(rate=0, capacity=10)
        with self.assertRaises(ValueError):
            TokenBucket(rate=10, capacity=0)

    def test_get_state(self):
        """测试获取状态"""
        state = self.bucket.get_state()
        self.assertEqual(state.tokens, 20)
        self.assertEqual(state.capacity, 20)
        self.assertEqual(state.rate, 10)

    def test_try_consume(self):
        """测试尝试消耗并返回等待时间"""
        success, wait = self.bucket.try_consume(5)
        self.assertTrue(success)
        self.assertEqual(wait, 0)

        success, wait = self.bucket.try_consume(25)
        self.assertFalse(success)
        self.assertGreater(wait, 0)


class TestLeakyBucket(unittest.TestCase):
    """漏桶测试"""

    def setUp(self):
        # 使用固定时间，避免 mock 时间导致漏水问题
        self.fixed_time = 1000.0
        self.bucket = LeakyBucket(
            rate=10, capacity=20,
            time_func=lambda: self.fixed_time
        )

    def test_initial_level(self):
        """测试初始水位"""
        self.assertEqual(self.bucket.get_level(), 0)

    def test_add_success(self):
        """测试成功添加请求"""
        self.assertTrue(self.bucket.try_add(10))
        self.assertEqual(self.bucket.get_level(), 10)

    def test_add_fail(self):
        """测试桶满拒绝"""
        self.assertTrue(self.bucket.try_add(20))
        self.assertFalse(self.bucket.try_add(1))

    def test_leak(self):
        """测试漏水"""
        bucket = LeakyBucket(rate=10, capacity=20)
        bucket.try_add(20)

        # 等待1秒，应该漏掉约10个
        time.sleep(1.1)
        level = bucket.get_level()
        self.assertLessEqual(level, 12)

    def test_get_available_capacity(self):
        """测试剩余容量"""
        self.bucket.try_add(10)
        self.assertEqual(self.bucket.get_available_capacity(), 10)

    def test_reset(self):
        """测试重置"""
        self.bucket.try_add(10)
        self.bucket.reset()
        self.assertEqual(self.bucket.get_level(), 0)

    def test_invalid_params(self):
        """测试无效参数"""
        with self.assertRaises(ValueError):
            LeakyBucket(rate=0, capacity=10)
        with self.assertRaises(ValueError):
            LeakyBucket(rate=10, capacity=0)


class TestLeakyBucketQueue(unittest.TestCase):
    """带队列的漏桶测试"""

    def test_enqueue_dequeue(self):
        """测试入队出队"""
        queue = LeakyBucketQueue(rate=10, capacity=5)

        self.assertTrue(queue.try_enqueue('item1'))
        self.assertTrue(queue.try_enqueue('item2'))
        self.assertEqual(queue.queue_size, 2)

    def test_enqueue_full(self):
        """测试队列满"""
        queue = LeakyBucketQueue(rate=10, capacity=3)

        self.assertTrue(queue.try_enqueue('item1'))
        self.assertTrue(queue.try_enqueue('item2'))
        self.assertTrue(queue.try_enqueue('item3'))
        self.assertFalse(queue.try_enqueue('item4'))

    def test_clear(self):
        """测试清空队列"""
        queue = LeakyBucketQueue(rate=10, capacity=5)
        queue.try_enqueue('item1')
        queue.try_enqueue('item2')
        queue.clear()

        self.assertEqual(queue.queue_size, 0)


class TestSlidingWindow(unittest.TestCase):
    """滑动窗口测试"""

    def setUp(self):
        self.window = SlidingWindow(limit=10, window_size=1.0)

    def test_initial_count(self):
        """测试初始计数"""
        self.assertEqual(self.window.get_count(), 0)

    def test_acquire_success(self):
        """测试成功获取"""
        for _ in range(10):
            self.assertTrue(self.window.try_acquire())
        self.assertEqual(self.window.get_count(), 10)

    def test_acquire_fail(self):
        """测试超过限制"""
        for _ in range(10):
            self.window.try_acquire()
        self.assertFalse(self.window.try_acquire())

    def test_window_sliding(self):
        """测试窗口滑动"""
        window = SlidingWindow(limit=5, window_size=0.5)

        for _ in range(5):
            self.assertTrue(window.try_acquire())

        # 等待窗口过期
        time.sleep(0.6)

        self.assertEqual(window.get_count(), 0)
        self.assertTrue(window.try_acquire())

    def test_get_remaining(self):
        """测试剩余配额"""
        for _ in range(5):
            self.window.try_acquire()
        self.assertEqual(self.window.get_remaining(), 5)

    def test_reset(self):
        """测试重置"""
        for _ in range(5):
            self.window.try_acquire()
        self.window.reset()
        self.assertEqual(self.window.get_count(), 0)

    def test_invalid_params(self):
        """测试无效参数"""
        with self.assertRaises(ValueError):
            SlidingWindow(limit=0, window_size=1)
        with self.assertRaises(ValueError):
            SlidingWindow(limit=10, window_size=0)

    def test_get_timestamps(self):
        """测试获取时间戳"""
        window = SlidingWindow(limit=3, window_size=1.0)
        window.try_acquire()
        window.try_acquire()

        timestamps = window.get_timestamps()
        self.assertEqual(len(timestamps), 2)


class TestSlidingWindowCounter(unittest.TestCase):
    """滑动窗口计数器测试"""

    def setUp(self):
        self.counter = SlidingWindowCounter(limit=10, window_size=1.0, sub_windows=10)

    def test_initial_count(self):
        """测试初始计数"""
        self.assertEqual(self.counter.get_count(), 0)

    def test_acquire_success(self):
        """测试成功获取"""
        for _ in range(10):
            self.assertTrue(self.counter.try_acquire())
        self.assertEqual(self.counter.get_count(), 10)

    def test_acquire_fail(self):
        """测试超过限制"""
        for _ in range(10):
            self.counter.try_acquire()
        self.assertFalse(self.counter.try_acquire())

    def test_approximation(self):
        """测试近似计算"""
        counter = SlidingWindowCounter(limit=100, window_size=1.0, sub_windows=10)

        # 快速发送请求
        for _ in range(100):
            self.assertTrue(counter.try_acquire())

        # 由于近似，实际可能略微超过限制
        # 但应该在合理范围内

    def test_reset(self):
        """测试重置"""
        for _ in range(5):
            self.counter.try_acquire()
        self.counter.reset()
        self.assertEqual(self.counter.get_count(), 0)


class TestFixedWindow(unittest.TestCase):
    """固定窗口测试"""

    def setUp(self):
        self.window = FixedWindow(limit=10, window_size=1.0)

    def test_initial_count(self):
        """测试初始计数"""
        self.assertEqual(self.window.get_count(), 0)

    def test_acquire_success(self):
        """测试成功获取"""
        for _ in range(10):
            self.assertTrue(self.window.try_acquire())
        self.assertEqual(self.window.get_count(), 10)

    def test_acquire_fail(self):
        """测试超过限制"""
        for _ in range(10):
            self.window.try_acquire()
        self.assertFalse(self.window.try_acquire())

    def test_window_reset(self):
        """测试窗口重置"""
        window = FixedWindow(limit=5, window_size=0.5)

        for _ in range(5):
            self.assertTrue(window.try_acquire())

        # 等待新窗口
        time.sleep(0.6)

        self.assertEqual(window.get_count(), 0)
        self.assertTrue(window.try_acquire())

    def test_get_state(self):
        """测试获取状态"""
        for _ in range(5):
            self.window.try_acquire()

        state = self.window.get_state()
        self.assertEqual(state.request_count, 5)
        self.assertEqual(state.limit, 10)
        self.assertEqual(state.window_size, 1.0)

    def test_reset(self):
        """测试重置"""
        for _ in range(5):
            self.window.try_acquire()
        self.window.reset()
        self.assertEqual(self.window.get_count(), 0)


class TestFixedWindowKeyed(unittest.TestCase):
    """多键固定窗口测试"""

    def setUp(self):
        self.limiter = FixedWindowKeyed(limit=5, window_size=1.0)

    def test_different_keys(self):
        """测试不同键独立计数"""
        for _ in range(5):
            self.assertTrue(self.limiter.try_acquire('key1'))
        self.assertFalse(self.limiter.try_acquire('key1'))
        self.assertTrue(self.limiter.try_acquire('key2'))

    def test_get_count(self):
        """测试获取计数"""
        for _ in range(3):
            self.limiter.try_acquire('test')

        self.assertEqual(self.limiter.get_count('test'), 3)
        self.assertEqual(self.limiter.get_count('other'), 0)

    def test_reset_key(self):
        """测试重置特定键"""
        self.limiter.try_acquire('key1')
        self.limiter.try_acquire('key2')
        self.limiter.reset('key1')

        self.assertEqual(self.limiter.get_count('key1'), 0)
        self.assertEqual(self.limiter.get_count('key2'), 1)

    def test_reset_all(self):
        """测试重置所有"""
        self.limiter.try_acquire('key1')
        self.limiter.try_acquire('key2')
        self.limiter.reset()

        self.assertEqual(self.limiter.get_count('key1'), 0)
        self.assertEqual(self.limiter.get_count('key2'), 0)

    def test_keys(self):
        """测试获取活跃键"""
        self.limiter.try_acquire('key1')
        self.limiter.try_acquire('key2')

        keys = self.limiter.keys()
        self.assertIn('key1', keys)
        self.assertIn('key2', keys)


class TestRateLimiter(unittest.TestCase):
    """统一速率限制器测试"""

    def test_token_bucket(self):
        """测试令牌桶算法"""
        limiter = RateLimiter(
            algorithm=Algorithm.TOKEN_BUCKET,
            rate=10,
            capacity=20
        )

        for _ in range(20):
            self.assertTrue(limiter.try_acquire())
        self.assertFalse(limiter.try_acquire())

    def test_sliding_window(self):
        """测试滑动窗口算法"""
        limiter = RateLimiter(
            algorithm=Algorithm.SLIDING_WINDOW,
            limit=10,
            window_size=1.0
        )

        for _ in range(10):
            self.assertTrue(limiter.try_acquire())
        self.assertFalse(limiter.try_acquire())

    def test_fixed_window(self):
        """测试固定窗口算法"""
        limiter = RateLimiter(
            algorithm=Algorithm.FIXED_WINDOW,
            limit=10,
            window_size=1.0
        )

        for _ in range(10):
            self.assertTrue(limiter.try_acquire())
        self.assertFalse(limiter.try_acquire())

    def test_get_state(self):
        """测试获取状态"""
        limiter = RateLimiter(
            algorithm=Algorithm.TOKEN_BUCKET,
            rate=10,
            capacity=20
        )

        state = limiter.get_state()
        self.assertEqual(state['algorithm'], 'token_bucket')
        self.assertIn('tokens', state)

    def test_reset(self):
        """测试重置"""
        limiter = RateLimiter(
            algorithm=Algorithm.SLIDING_WINDOW,
            limit=10,
            window_size=1.0
        )

        for _ in range(5):
            limiter.try_acquire()

        limiter.reset()
        state = limiter.get_state()
        self.assertEqual(state['count'], 0)


class TestMultiRateLimiter(unittest.TestCase):
    """多层速率限制器测试"""

    def test_multiple_limits(self):
        """测试多层限制"""
        limiter = MultiRateLimiter()
        limiter.add_limit('per_second', Algorithm.SLIDING_WINDOW, limit=10, window_size=1)
        limiter.add_limit('per_minute', Algorithm.SLIDING_WINDOW, limit=100, window_size=60)

        # 应该通过所有限制
        for _ in range(10):
            success, failed = limiter.try_acquire()
            self.assertTrue(success)

        # 秒限制应该失败
        success, failed = limiter.try_acquire()
        self.assertFalse(success)
        self.assertEqual(failed, 'per_second')

    def test_remove_limit(self):
        """测试移除限制"""
        limiter = MultiRateLimiter()
        limiter.add_limit('limit1', Algorithm.SLIDING_WINDOW, limit=5, window_size=1)

        self.assertTrue(limiter.remove_limit('limit1'))
        self.assertFalse(limiter.remove_limit('nonexistent'))

    def test_get_state(self):
        """测试获取状态"""
        limiter = MultiRateLimiter()
        limiter.add_limit('test', Algorithm.SLIDING_WINDOW, limit=10, window_size=1)

        state = limiter.get_state()
        self.assertIn('test', state)


class TestDecorators(unittest.TestCase):
    """装饰器测试"""

    def setUp(self):
        clear_limiters()

    def test_rate_limit_decorator(self):
        """测试限流装饰器"""
        @rate_limit(rate=2, capacity=2)
        def limited_func():
            return "success"

        # 前两次应该成功
        self.assertEqual(limited_func(), "success")
        self.assertEqual(limited_func(), "success")

        # 第三次应该失败
        with self.assertRaises(RateLimitExceeded):
            limited_func()

    def test_rate_limit_no_raise(self):
        """测试不抛异常的限流装饰器"""
        @rate_limit(rate=1, capacity=1, raise_on_limit=False)
        def limited_func():
            return "success"

        self.assertEqual(limited_func(), "success")
        self.assertIsNone(limited_func())

    def test_rate_limit_shared(self):
        """测试共享限流器"""
        @rate_limit(name='shared', rate=2, capacity=2)
        def func1():
            return "func1"

        @rate_limit(name='shared', rate=2, capacity=2)
        def func2():
            return "func2"

        # 两个函数共享同一个限流器
        self.assertEqual(func1(), "func1")
        self.assertEqual(func2(), "func2")
        # 已经消耗了2个，应该都失败
        with self.assertRaises(RateLimitExceeded):
            func1()
        with self.assertRaises(RateLimitExceeded):
            func2()

    def test_rate_limit_per_argument(self):
        """测试基于参数的限流"""
        @rate_limit_per_argument(
            key_func=lambda user_id: f"user_{user_id}",
            limit=2,
            window_size=60
        )
        def user_api(user_id):
            return f"Hello, {user_id}"

        # 不同参数独立计数
        self.assertEqual(user_api(1), "Hello, 1")
        self.assertEqual(user_api(1), "Hello, 1")
        with self.assertRaises(RateLimitExceeded):
            user_api(1)

        # user_id=2 还有配额
        self.assertEqual(user_api(2), "Hello, 2")

    def test_list_limiters(self):
        """测试列出限流器"""
        @rate_limit(name='test_limiter', rate=10, capacity=10)
        def func():
            pass

        limiters = list_limiters()
        self.assertIn('test_limiter', limiters)


class TestRateLimiterContext(unittest.TestCase):
    """上下文管理器测试"""

    def test_context_success(self):
        """测试成功获取"""
        limiter = RateLimiterContext(
            algorithm=Algorithm.TOKEN_BUCKET,
            rate=10,
            capacity=5
        )

        # 普通上下文只创建，不自动消耗
        with limiter:
            pass

    def test_context_acquire_or_raise(self):
        """测试抛异常获取"""
        limiter = RateLimiterContext(
            algorithm=Algorithm.TOKEN_BUCKET,
            rate=10,
            capacity=2
        )

        # 直接测试 acquire_or_raise 的逻辑（不使用 with 语法）
        # 第一次应该成功
        limiter.acquire_or_raise()
        self.assertTrue(limiter.acquired)

        # 第二次应该成功
        limiter._acquired = False  # 重置状态
        limiter.acquire_or_raise()
        self.assertTrue(limiter.acquired)

        # 第三次应该失败（容量只有2）
        limiter._acquired = False
        with self.assertRaises(RateLimitExceeded):
            limiter.acquire_or_raise()


class TestThreadSafety(unittest.TestCase):
    """线程安全测试"""

    def test_token_bucket_concurrent(self):
        """测试令牌桶并发"""
        bucket = TokenBucket(rate=100, capacity=100)
        success_count = [0]
        lock = threading.Lock()

        def worker():
            for _ in range(100):
                if bucket.consume():
                    with lock:
                        success_count[0] += 1

        threads = [threading.Thread(target=worker) for _ in range(10)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        # 总共只有100个令牌
        self.assertEqual(success_count[0], 100)

    def test_sliding_window_concurrent(self):
        """测试滑动窗口并发"""
        window = SlidingWindow(limit=100, window_size=1.0)
        success_count = [0]
        lock = threading.Lock()

        def worker():
            for _ in range(100):
                if window.try_acquire():
                    with lock:
                        success_count[0] += 1

        threads = [threading.Thread(target=worker) for _ in range(10)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        # 应该精确限制在100
        self.assertEqual(success_count[0], 100)

    def test_fixed_window_keyed_concurrent(self):
        """测试多键固定窗口并发"""
        limiter = FixedWindowKeyed(limit=10, window_size=1.0)
        results = {}

        def worker(key):
            count = 0
            for _ in range(20):
                if limiter.try_acquire(key):
                    count += 1
            results[key] = count

        threads = [threading.Thread(target=worker, args=(f'key{i}',)) for i in range(5)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        # 每个键应该限制在10
        for key, count in results.items():
            self.assertEqual(count, 10)


if __name__ == '__main__':
    unittest.main(verbosity=2)