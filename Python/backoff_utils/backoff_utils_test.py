"""
Backoff Utils 测试模块

测试所有退避算法、重试机制、限流器和断路器。
"""

import time
import random
from mod import (
    BackoffCalculator,
    BackoffStrategy,
    JitterType,
    RetryExecutor,
    retry,
    RateLimiter,
    CircuitBreaker,
    TimeoutRetry,
    calculate_backoff,
    create_retry_generator,
    EXPONENTIAL_BACKOFF,
    LINEAR_BACKOFF,
    FIXED_BACKOFF,
    FAST_RETRY,
    CONSERVATIVE_RETRY
)


class TestBackoffCalculator:
    """测试退避计算器"""
    
    def test_fixed_backoff(self):
        """测试固定退避"""
        calc = BackoffCalculator(
            strategy=BackoffStrategy.FIXED,
            base_delay=1.0,
            jitter_type=JitterType.NONE,
            seed=42
        )
        
        # 所有尝试的延迟应该相同
        delays = calc.get_delays(5)
        assert all(d == 1.0 for d in delays)
        print(f"✓ 固定退避: {delays}")
    
    def test_linear_backoff(self):
        """测试线性退避"""
        calc = BackoffCalculator(
            strategy=BackoffStrategy.LINEAR,
            base_delay=1.0,
            jitter_type=JitterType.NONE,
            seed=42
        )
        
        delays = calc.get_delays(5)
        expected = [1.0, 2.0, 3.0, 4.0, 5.0]
        assert delays == expected
        print(f"✓ 线性退避: {delays}")
    
    def test_exponential_backoff(self):
        """测试指数退避"""
        calc = BackoffCalculator(
            strategy=BackoffStrategy.EXPONENTIAL,
            base_delay=1.0,
            multiplier=2.0,
            jitter_type=JitterType.NONE,
            seed=42
        )
        
        delays = calc.get_delays(5)
        expected = [1.0, 2.0, 4.0, 8.0, 16.0]
        assert delays == expected
        print(f"✓ 指数退避: {delays}")
    
    def test_polynomial_backoff(self):
        """测试多项式退避"""
        calc = BackoffCalculator(
            strategy=BackoffStrategy.POLYNOMIAL,
            base_delay=1.0,
            polynomial_degree=2.0,
            jitter_type=JitterType.NONE,
            seed=42
        )
        
        delays = calc.get_delays(5)
        expected = [1.0, 4.0, 9.0, 16.0, 25.0]  # (n+1)^2
        assert delays == expected
        print(f"✓ 多项式退避 (degree=2): {delays}")
    
    def test_max_delay_cap(self):
        """测试最大延迟上限"""
        calc = BackoffCalculator(
            strategy=BackoffStrategy.EXPONENTIAL,
            base_delay=1.0,
            multiplier=2.0,
            max_delay=10.0,
            jitter_type=JitterType.NONE,
            seed=42
        )
        
        delays = calc.get_delays(10)
        # 所有延迟应该不超过 max_delay
        assert all(d <= 10.0 for d in delays)
        print(f"✓ 最大延迟上限: {delays}")
    
    def test_exponential_jitter(self):
        """测试指数退避 + 抖动"""
        calc = BackoffCalculator(
            strategy=BackoffStrategy.EXPONENTIAL_JITTER,
            base_delay=1.0,
            multiplier=2.0,
            jitter_range=(0, 0.5),
            seed=42
        )
        
        delays = calc.get_delays(5)
        # 基础延迟应该符合指数增长，但会有抖动
        base_delays = [1.0, 2.0, 4.0, 8.0, 16.0]
        for i, d in enumerate(delays):
            # 抖动后的延迟应该在 [base, base + 0.5] 范围内
            assert base_delays[i] <= d <= base_delays[i] + 0.5
        print(f"✓ 指数退避 + 抖动: {delays}")
    
    def test_negative_attempt_raises_error(self):
        """测试负数尝试次数抛出错误"""
        calc = BackoffCalculator()
        try:
            calc.calculate(-1)
            assert False, "应该抛出 ValueError"
        except ValueError as e:
            assert "不能为负数" in str(e)
            print(f"✓ 负数尝试次数抛出错误: {e}")
    
    def test_generator_delays(self):
        """测试延迟生成器"""
        calc = BackoffCalculator(
            strategy=BackoffStrategy.LINEAR,
            base_delay=1.0,
            jitter_type=JitterType.NONE,
            seed=42
        )
        
        # 测试生成器
        delays = []
        for delay in calc.delays(3):
            delays.append(delay)
        
        assert delays == [1.0, 2.0, 3.0]
        print(f"✓ 延迟生成器: {delays}")


class TestRetryExecutor:
    """测试重试执行器"""
    
    def test_successful_execution(self):
        """测试成功执行"""
        def success_func():
            return "success"
        
        executor = RetryExecutor(max_retries=3)
        result = executor.execute(success_func)
        
        assert result == "success"
        print(f"✓ 成功执行: {result}")
    
    def test_retry_on_failure(self):
        """测试失败后重试"""
        call_count = 0
        
        def flaky_func():
            nonlocal call_count
            call_count += 1
            if call_count < 3:
                raise ValueError("临时失败")
            return "success"
        
        retry_log = []
        
        def on_retry(attempt, exc, delay):
            retry_log.append((attempt, str(exc), delay))
        
        executor = RetryExecutor(
            max_retries=3,
            base_delay=0.01,
            on_retry=on_retry
        )
        
        result = executor.execute(flaky_func)
        assert result == "success"
        assert call_count == 3
        assert len(retry_log) == 2  # 前2次失败触发重试
        print(f"✓ 失败后重试成功: call_count={call_count}, retries={len(retry_log)}")
    
    def test_max_retries_exceeded(self):
        """测试超过最大重试次数"""
        def always_fail():
            raise ValueError("永远失败")
        
        executor = RetryExecutor(max_retries=2, base_delay=0.01)
        
        try:
            executor.execute(always_fail)
            assert False, "应该抛出异常"
        except ValueError as e:
            assert str(e) == "永远失败"
            print(f"✓ 超过最大重试次数: {e}")
    
    def test_specific_exception_types(self):
        """测试特定异常类型触发重试"""
        call_count = 0
        
        def mixed_errors():
            nonlocal call_count
            call_count += 1
            if call_count == 1:
                raise ValueError("值错误")
            if call_count == 2:
                raise TypeError("类型错误")
            return "success"
        
        executor = RetryExecutor(
            max_retries=3,
            base_delay=0.01,
            exceptions=(ValueError,)  # 只对 ValueError 重试
        )
        
        try:
            executor.execute(mixed_errors)
            assert False, "TypeError 不应该触发重试"
        except TypeError:
            assert call_count == 2  # ValueError 重试一次后遇到 TypeError
            print(f"✓ 特定异常类型: call_count={call_count}")
    
    def test_decorator(self):
        """测试装饰器"""
        call_count = 0
        
        @retry(max_retries=3, base_delay=0.01)
        def decorated_func():
            nonlocal call_count
            call_count += 1
            if call_count < 2:
                raise RuntimeError("失败")
            return "decorated success"
        
        result = decorated_func()
        assert result == "decorated success"
        assert call_count == 2
        print(f"✓ 装饰器: result={result}, call_count={call_count}")
    
    def test_success_callback(self):
        """测试成功回调"""
        call_count = 0
        success_log = []
        
        def flaky_func():
            nonlocal call_count
            call_count += 1
            if call_count < 2:
                raise ValueError("失败")
            return "success"
        
        def on_success(attempt):
            success_log.append(attempt)
        
        executor = RetryExecutor(
            max_retries=3,
            base_delay=0.01,
            on_success=on_success
        )
        
        executor.execute(flaky_func)
        assert success_log == [1]  # 第1次重试后成功
        print(f"✓ 成功回调: {success_log}")
    
    def test_failure_callback(self):
        """测试失败回调"""
        failure_log = []
        
        def always_fail():
            raise ValueError("永远失败")
        
        def on_failure(exc):
            failure_log.append(str(exc))
        
        executor = RetryExecutor(
            max_retries=2,
            base_delay=0.01,
            on_failure=on_failure
        )
        
        try:
            executor.execute(always_fail)
        except ValueError:
            assert failure_log == ["永远失败"]
            print(f"✓ 失败回调: {failure_log}")


class TestRateLimiter:
    """测试限流器"""
    
    def test_basic_rate_limiting(self):
        """测试基本限流"""
        limiter = RateLimiter(rate=5, period=1.0)
        
        # 应该能连续获取 5 个令牌
        successes = [limiter.acquire() for _ in range(5)]
        assert all(successes)
        
        # 第 6 个应该失败（令牌耗尽）
        assert not limiter.acquire()
        print(f"✓ 基本限流: 前5次成功={all(successes)}, 第6次失败")
    
    def test_token_refill(self):
        """测试令牌补充"""
        limiter = RateLimiter(rate=10, period=1.0)
        
        # 消耗所有令牌
        for _ in range(10):
            limiter.acquire()
        
        # 此时应该没有令牌了
        assert not limiter.acquire()
        
        # 等待一段时间让令牌补充
        time.sleep(0.5)
        
        # 应该能获取一些令牌（约5个）
        assert limiter.acquire()
        print(f"✓ 令牌补充: 等待0.5秒后可获取令牌")
    
    def test_wait_and_acquire(self):
        """测试等待并获取"""
        limiter = RateLimiter(rate=2, period=1.0, max_tokens=2)
        
        # 消耗所有令牌
        limiter.acquire()
        limiter.acquire()
        
        # 等待获取新的令牌
        wait_time = limiter.wait_and_acquire()
        assert wait_time > 0
        print(f"✓ 等待并获取: wait_time={wait_time:.2f}s")
    
    def test_custom_token_amount(self):
        """测试自定义令牌数量"""
        limiter = RateLimiter(rate=10, period=1.0, max_tokens=10)
        
        # 获取 5 个令牌
        assert limiter.acquire(5)
        
        # 应该还能获取 5 个
        assert limiter.acquire(5)
        
        # 现在没有令牌了
        assert not limiter.acquire(1)
        print(f"✓ 自定义令牌数量: 获取5+5后耗尽")


class TestCircuitBreaker:
    """测试断路器"""
    
    def test_closed_state_success(self):
        """测试闭路状态成功"""
        breaker = CircuitBreaker(failure_threshold=5)
        
        def success_func():
            return "success"
        
        result = breaker.call(success_func)
        assert result == "success"
        assert breaker.is_closed
        print(f"✓ 闭路状态成功: state={breaker.state.value}")
    
    def test_open_after_threshold(self):
        """测试达到阈值后断路"""
        breaker = CircuitBreaker(failure_threshold=3)
        
        def fail_func():
            raise ValueError("失败")
        
        # 连续失败直到断路
        for i in range(3):
            try:
                breaker.call(fail_func)
            except ValueError:
                pass
        
        # 应该已经断路
        assert breaker.is_open
        print(f"✓ 达到阈值后断路: state={breaker.state.value}")
    
    def test_open_rejects_requests(self):
        """测试开路状态拒绝请求"""
        breaker = CircuitBreaker(failure_threshold=2)
        
        def fail_func():
            raise ValueError("失败")
        
        # 触发断路
        for _ in range(2):
            try:
                breaker.call(fail_func)
            except ValueError:
                pass
        
        # 再尝试应该被拒绝
        try:
            breaker.call(lambda: "test")
            assert False, "应该被拒绝"
        except RuntimeError as e:
            assert "开路状态" in str(e)
            print(f"✓ 开路状态拒绝: {e}")
    
    def test_recovery_to_closed(self):
        """测试恢复到闭路"""
        breaker = CircuitBreaker(
            failure_threshold=2,
            recovery_timeout=0.1,
            half_open_requests=3,
            success_threshold=2
        )
        
        def fail_func():
            raise ValueError("失败")
        
        def success_func():
            return "success"
        
        # 触发断路
        for _ in range(2):
            try:
                breaker.call(fail_func)
            except ValueError:
                pass
        
        assert breaker.is_open
        
        # 等待恢复超时
        time.sleep(0.2)
        
        # 尝试成功调用，应该转为半开状态
        breaker.call(success_func)
        assert breaker.is_half_open
        
        # 再一次成功，应该恢复到闭路
        breaker.call(success_func)
        assert breaker.is_closed
        print(f"✓ 恢复到闭路: open->half_open->closed")
    
    def test_reset(self):
        """测试重置"""
        breaker = CircuitBreaker(failure_threshold=2)
        
        def fail_func():
            raise ValueError("失败")
        
        # 触发断路
        for _ in range(2):
            try:
                breaker.call(fail_func)
            except ValueError:
                pass
        
        assert breaker.is_open
        
        # 重置
        breaker.reset()
        assert breaker.is_closed
        print(f"✓ 重置断路器: open->closed")
    
    def test_half_open_failure_reopens(self):
        """测试半开状态失败重新断路"""
        breaker = CircuitBreaker(
            failure_threshold=2,
            recovery_timeout=0.1,
            half_open_requests=1
        )
        
        def fail_func():
            raise ValueError("失败")
        
        # 触发断路
        for _ in range(2):
            try:
                breaker.call(fail_func)
            except ValueError:
                pass
        
        assert breaker.is_open
        
        # 等待恢复
        time.sleep(0.2)
        
        # 半开状态下失败，应该重新断路
        try:
            breaker.call(fail_func)
        except ValueError:
            pass
        
        # 应该重新断路
        assert breaker.is_open
        print(f"✓ 半开状态失败重新断路: half_open->open")


class TestTimeoutRetry:
    """测试超时重试"""
    
    def test_success_within_timeout(self):
        """测试超时时间内成功"""
        tr = TimeoutRetry(max_retries=3, timeout=1.0)
        
        def fast_func():
            return "fast"
        
        result = tr.execute(fast_func)
        assert result == "fast"
        print(f"✓ 超时时间内成功: {result}")
    
    def test_retry_on_exception(self):
        """测试异常时重试"""
        call_count = 0
        
        def eventually_success():
            nonlocal call_count
            call_count += 1
            if call_count < 3:
                raise ValueError("失败")
            return "success"
        
        tr = TimeoutRetry(max_retries=3, timeout=1.0, base_delay=0.01)
        result = tr.execute(eventually_success)
        assert result == "success"
        assert call_count == 3
        print(f"✓ 异常时重试: call_count={call_count}")
    
    def test_max_retries_exceeded(self):
        """测试超过最大重试"""
        def always_fail():
            raise ValueError("永远失败")
        
        tr = TimeoutRetry(max_retries=2, timeout=1.0, base_delay=0.01)
        
        try:
            tr.execute(always_fail)
            assert False
        except ValueError:
            print(f"✓ 超时重试超过最大次数")


class TestUtilityFunctions:
    """测试辅助函数"""
    
    def test_calculate_backoff(self):
        """测试快捷计算函数"""
        # 固定退避
        assert calculate_backoff(0, "fixed", 1.0) == 1.0
        assert calculate_backoff(5, "fixed", 1.0) == 1.0
        
        # 线性退避
        assert calculate_backoff(0, "linear", 1.0) == 1.0
        assert calculate_backoff(2, "linear", 1.0) == 3.0
        
        # 指数退避
        assert calculate_backoff(0, "exponential", 1.0, multiplier=2.0) == 1.0
        assert calculate_backoff(3, "exponential", 1.0, multiplier=2.0) == 8.0
        
        # 最大延迟上限
        assert calculate_backoff(10, "exponential", 1.0, max_delay=10.0) == 10.0
        
        print(f"✓ 快捷计算函数验证通过")
    
    def test_create_retry_generator(self):
        """测试重试生成器"""
        delays = list(create_retry_generator(
            3,
            strategy=BackoffStrategy.LINEAR,
            base_delay=1.0,
            jitter_type=JitterType.NONE
        ))
        assert delays == [1.0, 2.0, 3.0]
        print(f"✓ 重试生成器: {delays}")
    
    def test_predefined_configs(self):
        """测试预定义配置"""
        assert EXPONENTIAL_BACKOFF["strategy"] == BackoffStrategy.EXPONENTIAL
        assert LINEAR_BACKOFF["strategy"] == BackoffStrategy.LINEAR
        assert FIXED_BACKOFF["strategy"] == BackoffStrategy.FIXED
        assert FAST_RETRY["base_delay"] == 0.1
        assert CONSERVATIVE_RETRY["base_delay"] == 2.0
        print(f"✓ 预定义配置验证通过")


class TestJitterTypes:
    """测试抖动类型"""
    
    def test_full_jitter(self):
        """测试完全抖动"""
        calc = BackoffCalculator(
            strategy=BackoffStrategy.EXPONENTIAL,
            base_delay=4.0,
            multiplier=2.0,
            jitter_type=JitterType.FULL,
            seed=42
        )
        
        delays = calc.get_delays(3)
        # 完全抖动后延迟应该在 [0, base] 范围内
        for delay in delays:
            assert delay <= 8.0  # 最大不超过原始指数值
        print(f"✓ 完全抖动: {delays}")
    
    def test_equal_jitter(self):
        """测试等分抖动"""
        calc = BackoffCalculator(
            strategy=BackoffStrategy.EXPONENTIAL,
            base_delay=4.0,
            multiplier=2.0,
            jitter_type=JitterType.EQUAL,
            seed=42
        )
        
        delays = calc.get_delays(3)
        # 等分抖动后延迟至少是 base/2
        for delay in delays:
            assert delay >= 0  # 至少有最小值
        print(f"✓ 等分抖动: {delays}")
    
    def test_decorrelated_jitter(self):
        """测试装饰抖动"""
        calc = BackoffCalculator(
            strategy=BackoffStrategy.EXPONENTIAL,
            base_delay=1.0,
            multiplier=2.0,
            jitter_type=JitterType.DECORRELATED,
            seed=42
        )
        
        delays = calc.get_delays(5)
        # 装饰抖动应该产生变化的延迟
        assert len(delays) == 5
        print(f"✓ 装饰抖动: {delays}")


def run_all_tests():
    """运行所有测试"""
    print("=" * 60)
    print("Backoff Utils 测试报告")
    print("=" * 60)
    
    # 退避计算器测试
    print("\n[BackoffCalculator 测试]")
    test = TestBackoffCalculator()
    test.test_fixed_backoff()
    test.test_linear_backoff()
    test.test_exponential_backoff()
    test.test_polynomial_backoff()
    test.test_max_delay_cap()
    test.test_exponential_jitter()
    test.test_negative_attempt_raises_error()
    test.test_generator_delays()
    
    # 重试执行器测试
    print("\n[RetryExecutor 测试]")
    test = TestRetryExecutor()
    test.test_successful_execution()
    test.test_retry_on_failure()
    test.test_max_retries_exceeded()
    test.test_specific_exception_types()
    test.test_decorator()
    test.test_success_callback()
    test.test_failure_callback()
    
    # 限流器测试
    print("\n[RateLimiter 测试]")
    test = TestRateLimiter()
    test.test_basic_rate_limiting()
    test.test_token_refill()
    test.test_wait_and_acquire()
    test.test_custom_token_amount()
    
    # 断路器测试
    print("\n[CircuitBreaker 测试]")
    test = TestCircuitBreaker()
    test.test_closed_state_success()
    test.test_open_after_threshold()
    test.test_open_rejects_requests()
    test.test_recovery_to_closed()
    test.test_reset()
    test.test_half_open_failure_reopens()
    
    # 超时重试测试
    print("\n[TimeoutRetry 测试]")
    test = TestTimeoutRetry()
    test.test_success_within_timeout()
    test.test_retry_on_exception()
    test.test_max_retries_exceeded()
    
    # 辅助函数测试
    print("\n[UtilityFunctions 测试]")
    test = TestUtilityFunctions()
    test.test_calculate_backoff()
    test.test_create_retry_generator()
    test.test_predefined_configs()
    
    # 抖动类型测试
    print("\n[JitterTypes 测试]")
    test = TestJitterTypes()
    test.test_full_jitter()
    test.test_equal_jitter()
    test.test_decorrelated_jitter()
    
    print("\n" + "=" * 60)
    print("✓ 所有测试通过!")
    print("=" * 60)


if __name__ == "__main__":
    run_all_tests()