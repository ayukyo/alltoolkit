"""
速率限制器工具库测试

测试覆盖：
- TokenBucket: 令牌桶算法
- SlidingWindow: 滑动窗口算法
- FixedWindow: 固定窗口算法
- LeakyBucket: 漏桶算法
- MultiLimiter: 多维度限制器
- 装饰器和上下文管理器
"""

import time
import threading
import pytest
from mod import (
    TokenBucket,
    SlidingWindow,
    FixedWindow,
    LeakyBucket,
    MultiLimiter,
    RateLimiterRegistry,
    RateLimitResult,
    RateLimitExceeded,
    rate_limit,
    rate_limit_context,
    create_token_bucket,
    create_sliding_window,
    create_fixed_window,
    create_leaky_bucket,
)


class TestTokenBucket:
    """令牌桶算法测试"""
    
    def test_initialization(self):
        """测试初始化"""
        bucket = TokenBucket(rate=10, capacity=100)
        assert bucket.rate == 10
        assert bucket.capacity == 100
        assert bucket.tokens == 100.0
    
    def test_initialization_with_custom_tokens(self):
        """测试自定义初始令牌数"""
        bucket = TokenBucket(rate=10, capacity=100, initial_tokens=50)
        # 允许微小的浮点数误差（refill 会造成极小变化）
        assert bucket.tokens >= 50.0 and bucket.tokens <= 50.1
    
    def test_invalid_parameters(self):
        """测试无效参数"""
        with pytest.raises(ValueError):
            TokenBucket(rate=0, capacity=100)
        with pytest.raises(ValueError):
            TokenBucket(rate=-5, capacity=100)
        with pytest.raises(ValueError):
            TokenBucket(rate=10, capacity=0)
        with pytest.raises(ValueError):
            TokenBucket(rate=10, capacity=-10)
    
    def test_acquire_success(self):
        """测试成功获取令牌"""
        bucket = TokenBucket(rate=10, capacity=100)
        result = bucket.acquire(1)
        assert result.allowed is True
        assert result.remaining == 99
        assert result.retry_after == 0.0
    
    def test_acquire_multiple_tokens(self):
        """测试获取多个令牌"""
        bucket = TokenBucket(rate=10, capacity=100)
        result = bucket.acquire(10)
        assert result.allowed is True
        assert result.remaining == 90
    
    def test_acquire_exceeds_capacity(self):
        """测试请求超过容量"""
        bucket = TokenBucket(rate=10, capacity=100)
        with pytest.raises(ValueError):
            bucket.acquire(150)
    
    def test_acquire_empty_bucket(self):
        """测试空桶获取令牌"""
        bucket = TokenBucket(rate=10, capacity=10, initial_tokens=0)
        result = bucket.acquire(1)
        assert result.allowed is False
        assert result.retry_after > 0
    
    def test_token_refill(self):
        """测试令牌补充"""
        bucket = TokenBucket(rate=100, capacity=100, initial_tokens=0)
        
        # 等待一些令牌生成
        time.sleep(0.05)  # 生成约 5 个令牌
        
        # 应该能获取到令牌
        result = bucket.try_acquire(1)
        assert result.allowed is True
    
    def test_try_acquire_non_blocking(self):
        """测试非阻塞获取"""
        bucket = TokenBucket(rate=10, capacity=10, initial_tokens=0)
        result = bucket.try_acquire(1)
        assert result.allowed is False
    
    def test_reset(self):
        """测试重置"""
        bucket = TokenBucket(rate=10, capacity=100)
        bucket.acquire(50)
        bucket.reset()
        assert bucket.tokens == 100.0
    
    def test_concurrent_access(self):
        """测试并发访问"""
        bucket = TokenBucket(rate=1000, capacity=1000)
        success_count = [0]
        lock = threading.Lock()
        
        def worker():
            result = bucket.acquire(1)
            if result.allowed:
                with lock:
                    success_count[0] += 1
        
        # 减少线程数量避免资源耗尽
        threads = [threading.Thread(target=worker) for _ in range(1100)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()
        
        # 应该大约有 1000+ 个成功（初始令牌数 + 等待期间生成的令牌）
        # 因为 rate=1000，在约1秒内会生成额外令牌
        assert success_count[0] >= 1000 and success_count[0] <= 1200


class TestSlidingWindow:
    """滑动窗口算法测试"""
    
    def test_initialization(self):
        """测试初始化"""
        window = SlidingWindow(max_requests=100, window_size=1.0)
        assert window.max_requests == 100
        assert window.window_size == 1.0
        assert window.current_count == 0
    
    def test_invalid_parameters(self):
        """测试无效参数"""
        with pytest.raises(ValueError):
            SlidingWindow(max_requests=0, window_size=1.0)
        with pytest.raises(ValueError):
            SlidingWindow(max_requests=100, window_size=0)
    
    def test_acquire_success(self):
        """测试成功获取许可"""
        window = SlidingWindow(max_requests=10, window_size=1.0)
        result = window.acquire(1)
        assert result.allowed is True
        assert result.remaining == 9
        assert result.retry_after == 0.0
    
    def test_acquire_multiple(self):
        """测试获取多个许可"""
        window = SlidingWindow(max_requests=10, window_size=1.0)
        result = window.acquire(5)
        assert result.allowed is True
        assert result.remaining == 5
    
    def test_acquire_exceeds_limit(self):
        """测试超过限制"""
        window = SlidingWindow(max_requests=5, window_size=1.0)
        # 先用 5 个
        window.acquire(5)
        # 再请求应该失败
        result = window.acquire(1)
        assert result.allowed is False
        assert result.retry_after > 0
    
    def test_window_sliding(self):
        """测试窗口滑动"""
        window = SlidingWindow(max_requests=5, window_size=0.2)
        
        # 用完所有配额
        for _ in range(5):
            result = window.acquire(1)
            assert result.allowed is True
        
        # 现在应该被限制
        result = window.acquire(1)
        assert result.allowed is False
        
        # 等待窗口过期
        time.sleep(0.3)
        
        # 应该能获取新的许可
        result = window.acquire(1)
        assert result.allowed is True
    
    def test_reset(self):
        """测试重置"""
        window = SlidingWindow(max_requests=10, window_size=1.0)
        for _ in range(5):
            window.acquire(1)
        window.reset()
        assert window.current_count == 0
    
    def test_concurrent_access(self):
        """测试并发访问"""
        window = SlidingWindow(max_requests=100, window_size=1.0)
        success_count = [0]
        lock = threading.Lock()
        
        def worker():
            result = window.acquire(1)
            if result.allowed:
                with lock:
                    success_count[0] += 1
        
        threads = [threading.Thread(target=worker) for _ in range(150)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()
        
        assert success_count[0] == 100


class TestFixedWindow:
    """固定窗口算法测试"""
    
    def test_initialization(self):
        """测试初始化"""
        window = FixedWindow(max_requests=100, window_size=1.0)
        assert window.max_requests == 100
        assert window.window_size == 1.0
        assert window.current_count == 0
    
    def test_invalid_parameters(self):
        """测试无效参数"""
        with pytest.raises(ValueError):
            FixedWindow(max_requests=0, window_size=1.0)
        with pytest.raises(ValueError):
            FixedWindow(max_requests=100, window_size=-1)
    
    def test_acquire_success(self):
        """测试成功获取许可"""
        window = FixedWindow(max_requests=10, window_size=1.0)
        result = window.acquire(1)
        assert result.allowed is True
        assert result.remaining == 9
    
    def test_acquire_multiple(self):
        """测试获取多个许可"""
        window = FixedWindow(max_requests=10, window_size=1.0)
        result = window.acquire(3)
        assert result.allowed is True
        assert result.remaining == 7
    
    def test_acquire_exceeds_limit(self):
        """测试超过限制"""
        window = FixedWindow(max_requests=5, window_size=1.0)
        window.acquire(5)
        result = window.acquire(1)
        assert result.allowed is False
    
    def test_window_reset(self):
        """测试窗口重置"""
        window = FixedWindow(max_requests=5, window_size=0.2)
        
        # 用完配额
        for _ in range(5):
            result = window.acquire(1)
            assert result.allowed is True
        
        # 应该被限制
        result = window.acquire(1)
        assert result.allowed is False
        
        # 等待窗口过期
        time.sleep(0.3)
        
        # 应该能获取新的许可
        result = window.acquire(1)
        assert result.allowed is True
    
    def test_manual_reset(self):
        """测试手动重置"""
        window = FixedWindow(max_requests=10, window_size=1.0)
        for _ in range(5):
            window.acquire(1)
        window.reset()
        assert window.current_count == 0


class TestLeakyBucket:
    """漏桶算法测试"""
    
    def test_initialization(self):
        """测试初始化"""
        bucket = LeakyBucket(rate=10, capacity=100)
        assert bucket.rate == 10
        assert bucket.capacity == 100
        assert bucket.water_level == 0.0
    
    def test_invalid_parameters(self):
        """测试无效参数"""
        with pytest.raises(ValueError):
            LeakyBucket(rate=0, capacity=100)
        with pytest.raises(ValueError):
            LeakyBucket(rate=10, capacity=0)
    
    def test_acquire_success(self):
        """测试成功获取许可"""
        bucket = LeakyBucket(rate=10, capacity=100)
        result = bucket.acquire(1)
        assert result.allowed is True
        assert result.remaining >= 0
    
    def test_acquire_multiple(self):
        """测试获取多个许可"""
        bucket = LeakyBucket(rate=10, capacity=100)
        result = bucket.acquire(10)
        assert result.allowed is True
        # 允许微小的时间误差导致漏水
        assert bucket.water_level >= 9.0 and bucket.water_level <= 10.1
    
    def test_acquire_exceeds_capacity(self):
        """测试超过容量"""
        bucket = LeakyBucket(rate=10, capacity=10)
        # 先填满桶
        bucket.acquire(10)
        # 再请求超过容量应该报错
        with pytest.raises(ValueError):
            bucket.acquire(20)
    
    def test_bucket_full(self):
        """测试桶满"""
        bucket = LeakyBucket(rate=10, capacity=5)
        
        # 填满桶
        result = bucket.acquire(5)
        assert result.allowed is True
        
        # 再请求应该失败
        result = bucket.acquire(1)
        assert result.allowed is False
    
    def test_leak(self):
        """测试漏水"""
        bucket = LeakyBucket(rate=100, capacity=100)
        
        # 添加水
        bucket.acquire(50)
        initial_level = bucket.water_level
        assert initial_level >= 49.0 and initial_level <= 50.1
        
        # 等待漏水
        time.sleep(0.15)  # 应该漏掉约 15 个
        
        # 检查水量减少
        current_level = bucket.water_level
        assert current_level < initial_level
        assert current_level <= 35.1  # 约 50 - 15 = 35
    
    def test_reset(self):
        """测试重置"""
        bucket = LeakyBucket(rate=10, capacity=100)
        bucket.acquire(50)
        bucket.reset()
        assert bucket.water_level == 0.0


class TestMultiLimiter:
    """多维度限制器测试"""
    
    def test_initialization(self):
        """测试初始化"""
        config = {
            "ip": (TokenBucket, {"rate": 10, "capacity": 100}),
            "user": (SlidingWindow, {"max_requests": 50, "window_size": 60}),
        }
        multi = MultiLimiter(config)
        assert "ip" in multi._limiters
        assert "user" in multi._limiters
    
    def test_acquire_all_dimensions(self):
        """测试获取所有维度的许可"""
        config = {
            "ip": (TokenBucket, {"rate": 10, "capacity": 100}),
            "user": (SlidingWindow, {"max_requests": 50, "window_size": 60}),
        }
        multi = MultiLimiter(config)
        results = multi.acquire(1)
        
        assert "ip" in results
        assert "user" in results
        assert results["ip"].allowed is True
        assert results["user"].allowed is True
    
    def test_acquire_specific_dimensions(self):
        """测试获取指定维度的许可"""
        config = {
            "ip": (TokenBucket, {"rate": 10, "capacity": 100}),
            "user": (SlidingWindow, {"max_requests": 50, "window_size": 60}),
        }
        multi = MultiLimiter(config)
        results = multi.acquire(1, dimensions=["ip"])
        
        assert "ip" in results
        assert "user" not in results
    
    def test_is_allowed(self):
        """测试检查是否允许"""
        config = {
            "ip": (TokenBucket, {"rate": 10, "capacity": 100}),
            "user": (SlidingWindow, {"max_requests": 50, "window_size": 60}),
        }
        multi = MultiLimiter(config)
        assert multi.is_allowed(1) is True
    
    def test_is_allowed_partial_block(self):
        """测试部分维度阻止"""
        config = {
            "ip": (TokenBucket, {"rate": 10, "capacity": 1}),
            "user": (SlidingWindow, {"max_requests": 50, "window_size": 60}),
        }
        multi = MultiLimiter(config)
        
        # 用完 IP 配额
        multi.acquire(1)
        
        assert multi.is_allowed(1) is False
    
    def test_get_retry_after(self):
        """测试获取重试等待时间"""
        config = {
            "ip": (TokenBucket, {"rate": 10, "capacity": 1}),
        }
        multi = MultiLimiter(config)
        
        # 用完配额
        multi.acquire(1)
        
        retry_after = multi.get_retry_after()
        assert retry_after > 0
    
    def test_reset(self):
        """测试重置"""
        config = {
            "ip": (TokenBucket, {"rate": 10, "capacity": 100}),
        }
        multi = MultiLimiter(config)
        multi.acquire(50)
        multi.reset()
        
        results = multi.try_acquire(1)
        assert results["ip"].remaining == 99


class TestRateLimiterRegistry:
    """限制器注册表测试"""
    
    def test_singleton(self):
        """测试单例模式"""
        registry1 = RateLimiterRegistry()
        registry2 = RateLimiterRegistry()
        assert registry1 is registry2
    
    def test_register_and_get(self):
        """测试注册和获取"""
        registry = RateLimiterRegistry()
        registry.clear()
        
        limiter = TokenBucket(rate=10, capacity=100)
        registry.register("test", limiter)
        
        assert registry.get("test") is limiter
        assert registry.get("nonexistent") is None
    
    def test_unregister(self):
        """测试注销"""
        registry = RateLimiterRegistry()
        registry.clear()
        
        limiter = TokenBucket(rate=10, capacity=100)
        registry.register("test", limiter)
        
        assert registry.unregister("test") is True
        assert registry.get("test") is None
        assert registry.unregister("nonexistent") is False
    
    def test_names(self):
        """测试获取名称列表"""
        registry = RateLimiterRegistry()
        registry.clear()
        
        registry.register("limiter1", TokenBucket(rate=10, capacity=100))
        registry.register("limiter2", SlidingWindow(max_requests=10, window_size=1.0))
        
        names = registry.names()
        assert "limiter1" in names
        assert "limiter2" in names


class TestDecorators:
    """装饰器测试"""
    
    def test_rate_limit_decorator_success(self):
        """测试速率限制装饰器成功"""
        limiter = TokenBucket(rate=10, capacity=100)
        
        @rate_limit(limiter, tokens=1)
        def api_call():
            return "success"
        
        assert api_call() == "success"
    
    def test_rate_limit_decorator_reject(self):
        """测试速率限制装饰器拒绝"""
        limiter = TokenBucket(rate=10, capacity=1)
        
        @rate_limit(limiter, tokens=1)
        def api_call():
            return "success"
        
        # 第一次成功
        assert api_call() == "success"
        
        # 第二次应该失败
        with pytest.raises(RateLimitExceeded):
            api_call()
    
    def test_rate_limit_decorator_with_callback(self):
        """测试带回调的装饰器"""
        limiter = TokenBucket(rate=10, capacity=1)
        callback_called = [False]
        
        def on_reject(result):
            callback_called[0] = True
            return "rejected"
        
        @rate_limit(limiter, tokens=1, on_reject=on_reject)
        def api_call():
            return "success"
        
        # 第一次成功
        assert api_call() == "success"
        
        # 第二次调用回调
        assert api_call() == "rejected"
        assert callback_called[0] is True
    
    def test_rate_limit_context_success(self):
        """测试上下文管理器成功"""
        limiter = TokenBucket(rate=10, capacity=100)
        
        with rate_limit_context(limiter) as result:
            assert result.allowed is True
    
    def test_rate_limit_context_reject(self):
        """测试上下文管理器拒绝"""
        limiter = TokenBucket(rate=10, capacity=1)
        
        with rate_limit_context(limiter):
            pass
        
        with pytest.raises(RateLimitExceeded):
            with rate_limit_context(limiter):
                pass


class TestRateLimitResult:
    """速率限制结果测试"""
    
    def test_allowed_true(self):
        """测试允许结果"""
        result = RateLimitResult(allowed=True, remaining=10, reset_time=100.0)
        assert result.allowed is True
        assert result.remaining == 10
        assert bool(result) is True
    
    def test_allowed_false(self):
        """测试拒绝结果"""
        result = RateLimitResult(allowed=False, remaining=0, reset_time=100.0, retry_after=5.0)
        assert result.allowed is False
        assert result.remaining == 0
        assert result.retry_after == 5.0
        assert bool(result) is False


class TestConvenienceFunctions:
    """便捷函数测试"""
    
    def test_create_token_bucket(self):
        """测试创建令牌桶"""
        limiter = create_token_bucket(rate=10, capacity=100)
        assert isinstance(limiter, TokenBucket)
        assert limiter.rate == 10
        assert limiter.capacity == 100
    
    def test_create_sliding_window(self):
        """测试创建滑动窗口"""
        limiter = create_sliding_window(max_requests=100, window_size=60.0)
        assert isinstance(limiter, SlidingWindow)
        assert limiter.max_requests == 100
        assert limiter.window_size == 60.0
    
    def test_create_fixed_window(self):
        """测试创建固定窗口"""
        limiter = create_fixed_window(max_requests=100, window_size=60.0)
        assert isinstance(limiter, FixedWindow)
        assert limiter.max_requests == 100
        assert limiter.window_size == 60.0
    
    def test_create_leaky_bucket(self):
        """测试创建漏桶"""
        limiter = create_leaky_bucket(rate=10, capacity=100)
        assert isinstance(limiter, LeakyBucket)
        assert limiter.rate == 10
        assert limiter.capacity == 100


class TestWaitForToken:
    """等待令牌测试"""
    
    def test_wait_for_token_success(self):
        """测试成功等待令牌"""
        limiter = TokenBucket(rate=100, capacity=100, initial_tokens=0)
        
        # 等待令牌生成
        start = time.time()
        success = limiter.wait_for_token(1, timeout=0.1)
        elapsed = time.time() - start
        
        assert success is True
        assert elapsed >= 0.01  # 应该等待了一些时间
    
    def test_wait_for_token_timeout(self):
        """测试等待令牌超时"""
        limiter = TokenBucket(rate=1, capacity=1, initial_tokens=0)
        
        # 立即超时
        success = limiter.wait_for_token(1, timeout=0.001)
        assert success is False


if __name__ == "__main__":
    pytest.main([__file__, "-v"])