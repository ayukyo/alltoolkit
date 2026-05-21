"""
Backoff Utils 使用示例

演示各种退避策略、重试机制、限流器和断路器的实际应用。
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
    FAST_RETRY,
    CONSERVATIVE_RETRY
)


def example_basic_backoff():
    """基本退避策略示例"""
    print("\n" + "=" * 50)
    print("基本退避策略示例")
    print("=" * 50)
    
    strategies = [
        ("固定退避", BackoffStrategy.FIXED),
        ("线性退避", BackoffStrategy.LINEAR),
        ("指数退避", BackoffStrategy.EXPONENTIAL),
        ("多项式退避", BackoffStrategy.POLYNOMIAL)
    ]
    
    for name, strategy in strategies:
        calc = BackoffCalculator(
            strategy=strategy,
            base_delay=1.0,
            multiplier=2.0,
            jitter_type=JitterType.NONE,
            seed=42
        )
        delays = calc.get_delays(5)
        print(f"\n{name}:")
        print(f"  尝试次数 -> 延迟时间: {delays}")
    
    # 指数退避 + 抖动（推荐用于分布式系统）
    print("\n指数退避 + 抖动（推荐）:")
    calc = BackoffCalculator(
        strategy=BackoffStrategy.EXPONENTIAL_JITTER,
        base_delay=1.0,
        multiplier=2.0,
        jitter_range=(0, 1.0),
        seed=42
    )
    delays = calc.get_delays(5)
    print(f"  {delays}")


def example_retry_with_backoff():
    """重试示例"""
    print("\n" + "=" * 50)
    print("重试示例")
    print("=" * 50)
    
    # 模拟不稳定的服务
    class UnstableService:
        def __init__(self, failure_rate=0.5):
            self.failure_rate = failure_rate
            self.call_count = 0
        
        def fetch_data(self):
            self.call_count += 1
            # 前3次模拟失败
            if self.call_count <= 3:
                raise ConnectionError("服务暂时不可用")
            return {"data": "success", "call_count": self.call_count}
    
    # 使用 RetryExecutor
    service = UnstableService()
    
    def on_retry(attempt, exc, delay):
        print(f"  重试 #{attempt + 1}: 等待 {delay:.2f}s 后重试 ({exc})")
    
    executor = RetryExecutor(
        max_retries=5,
        strategy=BackoffStrategy.EXPONENTIAL_JITTER,
        base_delay=0.1,
        on_retry=on_retry
    )
    
    print("\n使用 RetryExecutor:")
    try:
        result = executor.execute(service.fetch_data)
        print(f"  成功: {result}")
    except ConnectionError as e:
        print(f"  最终失败: {e}")


def example_retry_decorator():
    """重试装饰器示例"""
    print("\n" + "=" * 50)
    print("重试装饰器示例")
    print("=" * 50)
    
    # 使用装饰器自动重试
    call_count = 0
    
    @retry(max_retries=3, base_delay=0.1)
    def unreliable_api_call():
        call_count += 1
        print(f"  调用 API (第 {call_count} 次)")
        if call_count < 3:
            raise RuntimeError("API 调用失败")
        return "API 响应数据"
    
    print("\n使用 @retry 装饰器:")
    result = unreliable_api_call()
    print(f"  最终结果: {result}")


def example_rate_limiter():
    """限流器示例"""
    print("\n" + "=" * 50)
    print("限流器示例")
    print("=" * 50)
    
    # 创建限流器：每秒最多 5 个请求
    limiter = RateLimiter(rate=5, period=1.0)
    
    print("\n模拟 API 请求:")
    for i in range(10):
        if limiter.acquire():
            print(f"  请求 #{i + 1}: 成功 ✓")
        else:
            print(f"  请求 #{i + 1}: 被限流 ✗")
    
    # 等待并获取令牌
    print("\n等待并获取令牌:")
    wait_time = limiter.wait_and_acquire()
    print(f"  等待 {wait_time:.2f}s 后成功获取令牌")


def example_circuit_breaker():
    """断路器示例"""
    print("\n" + "=" * 50)
    print("断路器示例")
    print("=" * 50)
    
    class ExternalService:
        def __init__(self):
            self.fail_count = 0
            self.mode = "fail"
        
        def set_mode(self, mode):
            self.mode = mode
            self.fail_count = 0
        
        def call(self):
            if self.mode == "fail":
                self.fail_count += 1
                raise RuntimeError("服务故障")
            return "服务响应"
    
    # 创建断路器
    breaker = CircuitBreaker(
        failure_threshold=3,
        recovery_timeout=0.5,
        half_open_requests=3,
        success_threshold=2
    )
    
    service = ExternalService()
    
    print("\n阶段 1: 触发断路")
    for i in range(5):
        try:
            result = breaker.call(service.call)
            print(f"  调用 #{i + 1}: 成功 - {result}")
        except RuntimeError as e:
            print(f"  调用 #{i + 1}: 失败 - {e}")
        except RuntimeError as e:
            print(f"  调用 #{i + 1}: 被断路 - {e}")
        
        state = breaker.state.value
        print(f"    状态: {state}")
    
    print("\n阶段 2: 等待恢复")
    time.sleep(0.6)
    
    # 切换服务模式为正常
    service.set_mode("normal")
    
    print("\n阶段 3: 测试恢复")
    for i in range(5):
        try:
            result = breaker.call(service.call)
            print(f"  调用 #{i + 1}: 成功 - {result}")
        except RuntimeError as e:
            print(f"  调用 #{i + 1}: 失败 - {e}")
        
        state = breaker.state.value
        print(f"    状态: {state}")
    
    print("\n断路器最终状态:", breaker.state.value)


def example_timeout_retry():
    """超时重试示例"""
    print("\n" + "=" * 50)
    print("超时重试示例")
    print("=" * 50)
    
    class SlowService:
        def __init__(self):
            self.call_count = 0
        
        def slow_call(self, delay):
            self.call_count += 1
            time.sleep(delay)
            return f"延迟 {delay}s 的响应"
    
    service = SlowService()
    
    tr = TimeoutRetry(max_retries=3, timeout=0.5, base_delay=0.1)
    
    print("\n测试快速响应:")
    try:
        result = tr.execute(service.slow_call, 0.1)
        print(f"  成功: {result}")
    except TimeoutError as e:
        print(f"  超时: {e}")
    
    print("\n测试超时响应:")
    try:
        result = tr.execute(service.slow_call, 1.0)
        print(f"  成功: {result}")
    except TimeoutError as e:
        print(f"  超时: {e}")


def example_quick_calculate():
    """快捷计算示例"""
    print("\n" + "=" * 50)
    print("快捷退避计算示例")
    print("=" * 50)
    
    # 快速计算退避时间
    print("\n计算不同策略的退避时间:")
    
    for attempt in range(5):
        strategies = {
            "固定": calculate_backoff(attempt, "fixed", 1.0),
            "线性": calculate_backoff(attempt, "linear", 1.0),
            "指数": calculate_backoff(attempt, "exponential", 1.0)
        }
        print(f"  尝试 {attempt}: 固定={strategies['固定']}s, "
              f"线性={strategies['线性']}s, 指数={strategies['指数']}s")


def example_generator():
    """生成器示例"""
    print("\n" + "=" * 50)
    print("重试延迟生成器示例")
    print("=" * 50)
    
    print("\n使用生成器模拟重试循环:")
    for delay in create_retry_generator(5, strategy=BackoffStrategy.EXPONENTIAL_JITTER, base_delay=0.5):
        print(f"  下一次重试前等待 {delay:.2f}s")
        # time.sleep(delay)  # 实际使用时这里会真的等待


def example_predefined_configs():
    """预定义配置示例"""
    print("\n" + "=" * 50)
    print("预定义配置示例")
    print("=" * 50)
    
    configs = {
        "EXPONENTIAL_BACKOFF": EXPONENTIAL_BACKOFF,
        "FAST_RETRY": FAST_RETRY,
        "CONSERVATIVE_RETRY": CONSERVATIVE_RETRY
    }
    
    for name, config in configs.items():
        print(f"\n{name}:")
        for key, value in config.items():
            print(f"  {key}: {value}")
        
        # 使用配置创建计算器
        calc = BackoffCalculator(**config, jitter_type=JitterType.NONE, seed=42)
        delays = calc.get_delays(3)
        print(f"  示例延迟序列: {delays}")


def example_jitter_comparison():
    """抖动类型对比示例"""
    print("\n" + "=" * 50)
    print("抖动类型对比示例")
    print("=" * 50)
    
    jitter_types = [
        ("无抖动", JitterType.NONE),
        ("完全抖动", JitterType.FULL),
        ("等分抖动", JitterType.EQUAL),
        ("装饰抖动", JitterType.DECORRELATED)
    ]
    
    for name, jitter in jitter_types:
        calc = BackoffCalculator(
            strategy=BackoffStrategy.EXPONENTIAL,
            base_delay=4.0,
            multiplier=2.0,
            jitter_type=jitter,
            seed=42
        )
        delays = calc.get_delays(5)
        print(f"\n{name}:")
        print(f"  延迟序列: {[f'{d:.2f}' for d in delays]}")


def example_real_world_api():
    """真实 API 调用场景示例"""
    print("\n" + "=" * 50)
    print("真实 API 调用场景示例")
    print("=" * 50)
    
    # 模拟 HTTP API 客户端
    class MockApiClient:
        def __init__(self):
            self.failures = 0
            self.total_calls = 0
        
        def get_user(self, user_id):
            """模拟获取用户信息"""
            self.total_calls += 1
            
            # 模拟偶发性失败
            if self.failures < 2 and random.random() < 0.3:
                self.failures += 1
                raise ConnectionError("网络连接失败")
            
            return {"id": user_id, "name": f"用户{user_id}", "calls": self.total_calls}
    
    # 组合使用限流器 + 断路器 + 重试
    rate_limiter = RateLimiter(rate=10, period=1.0)
    circuit_breaker = CircuitBreaker(failure_threshold=5, recovery_timeout=5.0)
    
    retry_executor = RetryExecutor(
        max_retries=3,
        strategy=BackoffStrategy.EXPONENTIAL_JITTER,
        base_delay=0.5,
        exceptions=(ConnectionError,)
    )
    
    client = MockApiClient()
    
    print("\n组合使用限流 + 断路 + 重试:")
    
    def fetch_user_with_protection(user_id):
        """带保护的用户获取"""
        # 1. 检查限流
        if not rate_limiter.acquire():
            wait_time = rate_limiter.wait_and_acquire()
            print(f"  被限流，等待 {wait_time:.2f}s")
        
        # 2. 通过断路器
        def api_call():
            return client.get_user(user_id)
        
        return circuit_breaker.call(api_call)
    
    # 模拟多次调用
    for i in range(5):
        try:
            # 3. 自动重试
            user = retry_executor.execute(fetch_user_with_protection, i + 1)
            print(f"  调用 #{i + 1}: 成功获取用户 {user['name']}")
        except ConnectionError as e:
            print(f"  调用 #{i + 1}: 失败 - {e}")
        except RuntimeError as e:
            print(f"  调用 #{i + 1}: 断路拒绝 - {e}")
        
        print(f"    断路器状态: {circuit_breaker.state.value}")


def run_all_examples():
    """运行所有示例"""
    print("\n" + "=" * 60)
    print("Backoff Utils 使用示例")
    print("=" * 60)
    
    example_basic_backoff()
    example_retry_with_backoff()
    example_retry_decorator()
    example_rate_limiter()
    example_circuit_breaker()
    example_timeout_retry()
    example_quick_calculate()
    example_generator()
    example_predefined_configs()
    example_jitter_comparison()
    example_real_world_api()
    
    print("\n" + "=" * 60)
    print("所有示例演示完成!")
    print("=" * 60)


if __name__ == "__main__":
    run_all_examples()