"""
Rate Limiter Utils 测试套件

测试覆盖：
- TokenBucket: 令牌桶限流器
- LeakyBucket: 漏桶限流器
- SlidingWindow: 滑动窗口限流器
- FixedWindow: 固定窗口限流器
- RateLimiterRegistry: 限流器注册表
- rate_limit 装饰器
"""

import time
import threading
import sys
import os

# 添加父目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from rate_limiter_utils.mod import (
    TokenBucket,
    LeakyBucket,
    SlidingWindow,
    FixedWindow,
    RateLimiterRegistry,
    RateLimitResult,
    rate_limit,
    create_token_bucket,
    create_sliding_window,
)


class TestRunner:
    """简单测试运行器"""
    
    def __init__(self):
        self.passed = 0
        self.failed = 0
        self.tests = []
    
    def test(self, name: str, func):
        """运行单个测试"""
        self.tests.append((name, func))
        try:
            func()
            self.passed += 1
            print(f"  ✓ {name}")
        except AssertionError as e:
            self.failed += 1
            print(f"  ✗ {name}: {e}")
        except Exception as e:
            self.failed += 1
            print(f"  ✗ {name}: {type(e).__name__}: {e}")
    
    def summary(self):
        """输出测试摘要"""
        total = self.passed + self.failed
        print(f"\n{'=' * 50}")
        print(f"测试结果: {self.passed}/{total} 通过")
        if self.failed > 0:
            print(f"失败: {self.failed}")
            return False
        return True


def test_rate_limit_result():
    """测试 RateLimitResult 类"""
    # 测试允许结果
    result = RateLimitResult(allowed=True, remaining=5, retry_after=0)
    assert result.allowed == True
    assert result.remaining == 5
    assert bool(result) == True
    
    # 测试拒绝结果
    result = RateLimitResult(allowed=False, remaining=0, retry_after=2.5)
    assert result.allowed == False
    assert result.remaining == 0
    assert bool(result) == False
    
    # 测试 repr
    repr_str = repr(result)
    assert "拒绝" in repr_str or "✗" in repr_str


def test_token_bucket_basic():
    """测试令牌桶基本功能"""
    # 创建容量为5的令牌桶
    tb = TokenBucket(max_requests=5, window_seconds=1.0, refill_rate=5)
    
    # 初始应该有5个令牌
    status = tb.get_status()
    assert status["tokens"] == 5.0
    assert status["capacity"] == 5
    
    # 消耗令牌
    result = tb.acquire()
    assert result.allowed == True
    assert result.remaining == 4
    
    # 消耗多个令牌
    result = tb.acquire(3)
    assert result.allowed == True
    assert result.remaining == 1
    
    # 令牌不足
    result = tb.acquire(2)
    assert result.allowed == False
    assert result.retry_after > 0


def test_token_bucket_refill():
    """测试令牌桶补充"""
    tb = TokenBucket(max_requests=5, window_seconds=1.0, refill_rate=10)
    
    # 消耗所有令牌
    for _ in range(5):
        tb.acquire()
    
    # 应该被拒绝
    result = tb.acquire()
    assert result.allowed == False
    
    # 等待补充
    time.sleep(0.3)  # 应该补充约3个令牌
    
    result = tb.acquire()
    assert result.allowed == True
    
    status = tb.get_status()
    assert status["tokens"] >= 1  # 至少剩余1个


def test_token_bucket_reset():
    """测试令牌桶重置"""
    tb = TokenBucket(max_requests=5, window_seconds=1.0)
    
    # 消耗令牌
    for _ in range(5):
        tb.acquire()
    
    # 重置
    tb.reset()
    
    status = tb.get_status()
    assert status["tokens"] == 5.0


def test_leaky_bucket_basic():
    """测试漏桶基本功能"""
    lb = LeakyBucket(max_requests=5, window_seconds=1.0, leak_rate=5)
    
    # 初始应该可以入队
    result = lb.acquire()
    assert result.allowed == True
    
    status = lb.get_status()
    assert status["queue_size"] == 1
    
    # 填满队列
    for _ in range(4):
        lb.acquire()
    
    # 队列已满
    result = lb.acquire()
    assert result.allowed == False
    
    status = lb.get_status()
    assert status["utilization"] >= 0.8


def test_leaky_bucket_leak():
    """测试漏桶泄漏"""
    lb = LeakyBucket(max_requests=10, window_seconds=1.0, leak_rate=10)
    
    # 入队10个请求
    for _ in range(10):
        lb.acquire()
    
    status = lb.get_status()
    assert status["queue_size"] == 10
    
    # 等待泄漏
    time.sleep(0.5)  # 应该泄漏约5个
    
    status = lb.get_status()
    assert status["queue_size"] <= 6


def test_sliding_window_basic():
    """测试滑动窗口基本功能"""
    sw = SlidingWindow(max_requests=5, window_seconds=1.0)
    
    # 应该允许前5个请求
    for i in range(5):
        result = sw.acquire()
        assert result.allowed == True, f"请求 {i+1} 应该被允许"
    
    # 第6个应该被拒绝
    result = sw.acquire()
    assert result.allowed == False
    assert result.retry_after > 0
    
    status = sw.get_status()
    assert status["current_count"] == 5
    assert status["utilization"] == 1.0


def test_sliding_window_expire():
    """测试滑动窗口过期"""
    sw = SlidingWindow(max_requests=2, window_seconds=0.5)
    
    # 发送2个请求
    sw.acquire()
    sw.acquire()
    
    # 应该被拒绝
    result = sw.acquire()
    assert result.allowed == False
    
    # 等待窗口过期
    time.sleep(0.6)
    
    # 应该可以再次请求
    result = sw.acquire()
    assert result.allowed == True
    
    status = sw.get_status()
    assert status["current_count"] == 1


def test_sliding_window_reset():
    """测试滑动窗口重置"""
    sw = SlidingWindow(max_requests=5, window_seconds=1.0)
    
    for _ in range(5):
        sw.acquire()
    
    sw.reset()
    
    status = sw.get_status()
    assert status["current_count"] == 0


def test_fixed_window_basic():
    """测试固定窗口基本功能"""
    fw = FixedWindow(max_requests=5, window_seconds=1.0)
    
    # 应该允许前5个请求
    for i in range(5):
        result = fw.acquire()
        assert result.allowed == True, f"请求 {i+1} 应该被允许"
    
    # 第6个应该被拒绝
    result = fw.acquire()
    assert result.allowed == False
    
    status = fw.get_status()
    assert status["current_count"] == 5


def test_fixed_window_natural_alignment():
    """测试固定窗口自然对齐"""
    fw = FixedWindow(max_requests=10, window_seconds=1.0, window_alignment="natural")
    
    status = fw.get_status()
    # 窗口开始时间应该是整数秒
    assert status["window_start"] % 1.0 < 0.001 or status["window_start"] == 0


def test_fixed_window_reset():
    """测试固定窗口重置"""
    fw = FixedWindow(max_requests=5, window_seconds=1.0)
    
    for _ in range(5):
        fw.acquire()
    
    fw.reset()
    
    result = fw.acquire()
    assert result.allowed == True


def test_rate_limiter_registry():
    """测试限流器注册表"""
    registry = RateLimiterRegistry(
        TokenBucket,
        max_requests=5,
        window_seconds=1.0
    )
    
    # 为不同用户创建限流器
    result1 = registry.acquire("user_1")
    assert result1.allowed == True
    
    result2 = registry.acquire("user_2")
    assert result2.allowed == True
    
    # 检查状态
    all_status = registry.get_all_status()
    assert "user_1" in all_status
    assert "user_2" in all_status
    
    # 统计信息
    stats = registry.get_stats()
    assert stats["limiter_count"] == 2
    assert stats["limiter_class"] == "TokenBucket"
    
    # 移除限流器
    assert registry.remove_limiter("user_1") == True
    assert registry.remove_limiter("unknown") == False


def test_rate_limit_decorator():
    """测试限流装饰器"""
    call_count = 0
    reject_count = 0
    
    limiter = TokenBucket(max_requests=2, window_seconds=1.0)
    
    def on_reject(result):
        nonlocal reject_count
        reject_count += 1
        return f"rejected: {result.message}"
    
    @rate_limit(limiter, on_reject=on_reject)
    def api_call():
        nonlocal call_count
        call_count += 1
        return "success"
    
    # 前两次应该成功
    assert api_call() == "success"
    assert api_call() == "success"
    assert call_count == 2
    
    # 第三次应该被限流
    result = api_call()
    assert "rejected" in result
    assert reject_count == 1


def test_rate_limit_decorator_exception():
    """测试限流装饰器异常"""
    limiter = TokenBucket(max_requests=1, window_seconds=1.0)
    
    @rate_limit(limiter)  # 没有 on_reject
    def protected_func():
        return "ok"
    
    # 第一次成功
    assert protected_func() == "ok"
    
    # 第二次应该抛出异常
    try:
        protected_func()
        assert False, "应该抛出异常"
    except Exception as e:
        assert "Rate limit exceeded" in str(e)


def test_create_token_bucket():
    """测试便捷函数创建令牌桶"""
    tb = create_token_bucket(qps=100, burst=200)
    
    status = tb.get_status()
    assert status["capacity"] == 200
    assert status["refill_rate"] == 100


def test_create_sliding_window():
    """测试便捷函数创建滑动窗口"""
    sw = create_sliding_window(100, 60)
    
    status = sw.get_status()
    assert status["max_requests"] == 100
    assert status["window_seconds"] == 60


def test_thread_safety():
    """测试线程安全性"""
    limiter = TokenBucket(max_requests=100, window_seconds=1.0, refill_rate=100)
    
    success_count = 0
    fail_count = 0
    lock = threading.Lock()
    
    def worker():
        nonlocal success_count, fail_count
        for _ in range(20):
            result = limiter.acquire()
            with lock:
                if result.allowed:
                    success_count += 1
                else:
                    fail_count += 1
            time.sleep(0.001)  # 小延迟
    
    threads = [threading.Thread(target=worker) for _ in range(5)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    
    # 应该有成功有失败
    assert success_count > 0
    # 总请求数应该是100
    assert success_count + fail_count == 100


def test_context_manager():
    """测试上下文管理器"""
    with TokenBucket(max_requests=5, window_seconds=1.0) as limiter:
        for _ in range(5):
            limiter.acquire()
        status = limiter.get_status()
        assert status["tokens"] < 5
    
    # 退出后应该重置
    status = limiter.get_status()
    assert status["tokens"] == 5.0


def test_multiple_tokens():
    """测试多令牌请求"""
    tb = TokenBucket(max_requests=10, window_seconds=1.0, refill_rate=10)
    
    # 请求5个令牌
    result = tb.acquire(5)
    assert result.allowed == True
    assert result.remaining == 5
    
    # 再请求6个（只有5个可用）
    result = tb.acquire(6)
    assert result.allowed == False
    
    # 请求5个
    result = tb.acquire(5)
    assert result.allowed == True
    assert result.remaining == 0


def run_all_tests():
    """运行所有测试"""
    runner = TestRunner()
    
    print("\n" + "=" * 50)
    print("Rate Limiter Utils 测试套件")
    print("=" * 50)
    
    print("\n[RateLimitResult]")
    runner.test("RateLimitResult 基本功能", test_rate_limit_result)
    
    print("\n[TokenBucket]")
    runner.test("TokenBucket 基本功能", test_token_bucket_basic)
    runner.test("TokenBucket 令牌补充", test_token_bucket_refill)
    runner.test("TokenBucket 重置", test_token_bucket_reset)
    
    print("\n[LeakyBucket]")
    runner.test("LeakyBucket 基本功能", test_leaky_bucket_basic)
    runner.test("LeakyBucket 泄漏", test_leaky_bucket_leak)
    
    print("\n[SlidingWindow]")
    runner.test("SlidingWindow 基本功能", test_sliding_window_basic)
    runner.test("SlidingWindow 过期", test_sliding_window_expire)
    runner.test("SlidingWindow 重置", test_sliding_window_reset)
    
    print("\n[FixedWindow]")
    runner.test("FixedWindow 基本功能", test_fixed_window_basic)
    runner.test("FixedWindow 自然对齐", test_fixed_window_natural_alignment)
    runner.test("FixedWindow 重置", test_fixed_window_reset)
    
    print("\n[RateLimiterRegistry]")
    runner.test("RateLimiterRegistry 基本功能", test_rate_limiter_registry)
    
    print("\n[装饰器]")
    runner.test("rate_limit 装饰器", test_rate_limit_decorator)
    runner.test("rate_limit 装饰器异常", test_rate_limit_decorator_exception)
    
    print("\n[便捷函数]")
    runner.test("create_token_bucket", test_create_token_bucket)
    runner.test("create_sliding_window", test_create_sliding_window)
    
    print("\n[高级功能]")
    runner.test("线程安全", test_thread_safety)
    runner.test("上下文管理器", test_context_manager)
    runner.test("多令牌请求", test_multiple_tokens)
    
    return runner.summary()


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)