"""
Backoff Utils - 退避算法工具模块

提供各种退避算法实现，用于重试策略、限流等场景。
零外部依赖，纯 Python 实现。

支持的退避策略：
- 固定退避 (Fixed Backoff)
- 线性退避 (Linear Backoff)
- 指数退避 (Exponential Backoff)
- 指数退避 + 抖动 (Exponential Backoff with Jitter)
- 装饰退避 (Decorrelated Backoff)
- 多项式退避 (Polynomial Backoff)
"""

import random
import time
from typing import Callable, Generator, Optional, Tuple
from functools import wraps
from enum import Enum


class BackoffStrategy(Enum):
    """退避策略枚举"""
    FIXED = "fixed"
    LINEAR = "linear"
    EXPONENTIAL = "exponential"
    EXPONENTIAL_JITTER = "exponential_jitter"
    DECORRELATED = "decorrelated"
    POLYNOMIAL = "polynomial"


class JitterType(Enum):
    """抖动类型枚举"""
    NONE = "none"
    FULL = "full"
    EQUAL = "equal"
    DECORRELATED = "decorrelated"


class BackoffCalculator:
    """
    退避计算器
    
    计算重试等待时间，支持多种退避策略和抖动方式。
    
    示例:
        >>> calc = BackoffCalculator(strategy=BackoffStrategy.EXPONENTIAL_JITTER)
        >>> for delay in calc.delays(max_retries=5):
        ...     print(f"等待 {delay:.2f} 秒")
    """
    
    def __init__(
        self,
        strategy: BackoffStrategy = BackoffStrategy.EXPONENTIAL_JITTER,
        base_delay: float = 1.0,
        max_delay: float = 300.0,
        multiplier: float = 2.0,
        jitter_type: JitterType = JitterType.FULL,
        jitter_range: Tuple[float, float] = (0.0, 1.0),
        polynomial_degree: float = 2.0,
        seed: Optional[int] = None
    ):
        """
        初始化退避计算器
        
        Args:
            strategy: 退避策略
            base_delay: 基础延迟时间（秒）
            max_delay: 最大延迟时间（秒）
            multiplier: 乘数因子（用于指数退避）
            jitter_type: 抖动类型
            jitter_range: 抖动范围 (最小, 最大)
            polynomial_degree: 多项式次数（用于多项式退避）
            seed: 随机种子（用于测试）
        """
        self.strategy = strategy
        self.base_delay = base_delay
        self.max_delay = max_delay
        self.multiplier = multiplier
        self.jitter_type = jitter_type
        self.jitter_range = jitter_range
        self.polynomial_degree = polynomial_degree
        
        if seed is not None:
            random.seed(seed)
    
    def calculate(self, attempt: int) -> float:
        """
        计算指定尝试次数的延迟时间
        
        Args:
            attempt: 尝试次数（从 0 开始）
        
        Returns:
            延迟时间（秒）
        """
        if attempt < 0:
            raise ValueError("尝试次数不能为负数")
        
        delay = self._calculate_base_delay(attempt)
        delay = self._apply_jitter(delay, attempt)
        return min(delay, self.max_delay)
    
    def _calculate_base_delay(self, attempt: int) -> float:
        """计算基础延迟"""
        if self.strategy == BackoffStrategy.FIXED:
            return self._fixed_delay()
        elif self.strategy == BackoffStrategy.LINEAR:
            return self._linear_delay(attempt)
        elif self.strategy == BackoffStrategy.EXPONENTIAL:
            return self._exponential_delay(attempt)
        elif self.strategy == BackoffStrategy.EXPONENTIAL_JITTER:
            return self._exponential_delay(attempt)
        elif self.strategy == BackoffStrategy.DECORRELATED:
            return self._decorrelated_delay(attempt)
        elif self.strategy == BackoffStrategy.POLYNOMIAL:
            return self._polynomial_delay(attempt)
        else:
            raise ValueError(f"未知的退避策略: {self.strategy}")
    
    def _fixed_delay(self) -> float:
        """固定延迟"""
        return self.base_delay
    
    def _linear_delay(self, attempt: int) -> float:
        """线性延迟: delay = base * (attempt + 1)"""
        return self.base_delay * (attempt + 1)
    
    def _exponential_delay(self, attempt: int) -> float:
        """指数延迟: delay = base * multiplier^attempt"""
        return self.base_delay * (self.multiplier ** attempt)
    
    def _decorrelated_delay(self, attempt: int) -> float:
        """装饰延迟（与 AWS SDK 使用相同的算法）"""
        # decorrelated jitter 的基础计算
        return self.base_delay * random.random() * (self.multiplier ** attempt)
    
    def _polynomial_delay(self, attempt: int) -> float:
        """多项式延迟: delay = base * (attempt + 1)^degree"""
        return self.base_delay * ((attempt + 1) ** self.polynomial_degree)
    
    def _apply_jitter(self, delay: float, attempt: int) -> float:
        """应用抖动"""
        if self.jitter_type == JitterType.NONE or self.strategy == BackoffStrategy.EXPONENTIAL_JITTER:
            if self.strategy == BackoffStrategy.EXPONENTIAL_JITTER:
                # 指数退避 + 抖动策略，使用专门的抖动计算
                return self._exponential_jitter_delay(attempt)
            return delay
        
        if self.jitter_type == JitterType.FULL:
            return self._full_jitter(delay)
        elif self.jitter_type == JitterType.EQUAL:
            return self._equal_jitter(delay)
        elif self.jitter_type == JitterType.DECORRELATED:
            return self._decorrelated_jitter(delay, attempt)
        
        return delay
    
    def _exponential_jitter_delay(self, attempt: int) -> float:
        """指数退避 + 随机抖动（经典实现）"""
        base = self.base_delay * (self.multiplier ** attempt)
        jitter_min, jitter_max = self.jitter_range
        jitter = random.uniform(jitter_min, jitter_max)
        return base + jitter
    
    def _full_jitter(self, delay: float) -> float:
        """完全抖动: [0, delay]"""
        return random.uniform(0, delay)
    
    def _equal_jitter(self, delay: float) -> float:
        """等分抖动: [delay/2, delay]"""
        return delay / 2 + random.uniform(0, delay / 2)
    
    def _decorrelated_jitter(self, delay: float, attempt: int) -> float:
        """装饰抖动"""
        # 计算装饰抖动
        return random.uniform(self.base_delay, min(delay, self.max_delay))
    
    def delays(self, max_retries: int) -> Generator[float, None, None]:
        """
        生成延迟序列的生成器
        
        Args:
            max_retries: 最大重试次数
        
        Yields:
            每次重试的延迟时间
        """
        for attempt in range(max_retries):
            yield self.calculate(attempt)
    
    def get_delays(self, max_retries: int) -> list:
        """获取延迟序列列表"""
        return list(self.delays(max_retries))


class RetryExecutor:
    """
    重试执行器
    
    使用退避策略自动重试失败的函数调用。
    
    示例:
        >>> executor = RetryExecutor(max_retries=3, strategy=BackoffStrategy.EXPONENTIAL_JITTER)
        >>> result = executor.execute(some_function, arg1, arg2)
    """
    
    def __init__(
        self,
        max_retries: int = 3,
        strategy: BackoffStrategy = BackoffStrategy.EXPONENTIAL_JITTER,
        base_delay: float = 1.0,
        max_delay: float = 300.0,
        multiplier: float = 2.0,
        jitter_type: JitterType = JitterType.FULL,
        exceptions: Tuple = (Exception,),
        on_retry: Optional[Callable[[int, Exception, float], None]] = None,
        on_success: Optional[Callable[[int], None]] = None,
        on_failure: Optional[Callable[[Exception], None]] = None
    ):
        """
        初始化重试执行器
        
        Args:
            max_retries: 最大重试次数
            strategy: 退避策略
            base_delay: 基础延迟时间（秒）
            max_delay: 最大延迟时间（秒）
            multiplier: 乘数因子
            jitter_type: 抖动类型
            exceptions: 触发重试的异常类型
            on_retry: 重试回调 (attempt, exception, delay)
            on_success: 成功回调 (attempt)
            on_failure: 最终失败回调 (exception)
        """
        self.max_retries = max_retries
        self.calculator = BackoffCalculator(
            strategy=strategy,
            base_delay=base_delay,
            max_delay=max_delay,
            multiplier=multiplier,
            jitter_type=jitter_type
        )
        self.exceptions = exceptions
        self.on_retry = on_retry
        self.on_success = on_success
        self.on_failure = on_failure
    
    def execute(self, func: Callable, *args, **kwargs):
        """
        执行函数，失败时自动重试
        
        Args:
            func: 要执行的函数
            *args: 位置参数
            **kwargs: 关键字参数
        
        Returns:
            函数返回值
        
        Raises:
            最后一次失败的异常
        """
        last_exception = None
        
        for attempt in range(self.max_retries + 1):
            try:
                result = func(*args, **kwargs)
                if self.on_success and attempt > 0:
                    self.on_success(attempt)
                return result
            except self.exceptions as e:
                last_exception = e
                
                if attempt < self.max_retries:
                    delay = self.calculator.calculate(attempt)
                    
                    if self.on_retry:
                        self.on_retry(attempt, e, delay)
                    
                    time.sleep(delay)
        
        if self.on_failure and last_exception:
            self.on_failure(last_exception)
        
        raise last_exception
    
    def __call__(self, func: Callable) -> Callable:
        """作为装饰器使用"""
        @wraps(func)
        def wrapper(*args, **kwargs):
            return self.execute(func, *args, **kwargs)
        return wrapper


def retry(
    max_retries: int = 3,
    strategy: BackoffStrategy = BackoffStrategy.EXPONENTIAL_JITTER,
    base_delay: float = 1.0,
    max_delay: float = 300.0,
    multiplier: float = 2.0,
    jitter_type: JitterType = JitterType.FULL,
    exceptions: Tuple = (Exception,)
):
    """
    重试装饰器
    
    示例:
        >>> @retry(max_retries=3, strategy=BackoffStrategy.EXPONENTIAL)
        ... def unstable_function():
        ...     # 可能失败的操作
        ...     pass
    """
    def decorator(func: Callable) -> Callable:
        executor = RetryExecutor(
            max_retries=max_retries,
            strategy=strategy,
            base_delay=base_delay,
            max_delay=max_delay,
            multiplier=multiplier,
            jitter_type=jitter_type,
            exceptions=exceptions
        )
        return executor(func)
    return decorator


class RateLimiter:
    """
    基于令牌桶算法的限流器
    
    使用退避策略控制请求速率。
    
    示例:
        >>> limiter = RateLimiter(rate=10, period=1.0)  # 每秒 10 个请求
        >>> if limiter.acquire():
        ...     # 执行请求
        ...     pass
    """
    
    def __init__(
        self,
        rate: float = 10.0,
        period: float = 1.0,
        max_tokens: Optional[float] = None
    ):
        """
        初始化限流器
        
        Args:
            rate: 时间周期内允许的请求数
            period: 时间周期（秒）
            max_tokens: 最大令牌数（默认等于 rate）
        """
        self.rate = rate
        self.period = period
        self.max_tokens = max_tokens if max_tokens is not None else rate
        self.tokens = self.max_tokens
        self.last_update = time.time()
    
    def acquire(self, tokens: float = 1.0) -> bool:
        """
        尝试获取令牌
        
        Args:
            tokens: 需要的令牌数
        
        Returns:
            是否成功获取
        """
        self._refill()
        
        if self.tokens >= tokens:
            self.tokens -= tokens
            return True
        
        return False
    
    def wait_and_acquire(self, tokens: float = 1.0) -> float:
        """
        等待并获取令牌
        
        Args:
            tokens: 需要的令牌数
        
        Returns:
            等待的时间（秒）
        """
        self._refill()
        
        if self.tokens >= tokens:
            self.tokens -= tokens
            return 0.0
        
        # 计算需要等待的时间
        needed = tokens - self.tokens
        wait_time = (needed / self.rate) * self.period
        
        time.sleep(wait_time)
        self.tokens = 0
        self.last_update = time.time()
        
        return wait_time
    
    def _refill(self):
        """补充令牌"""
        now = time.time()
        elapsed = now - self.last_update
        refill = (elapsed / self.period) * self.rate
        self.tokens = min(self.max_tokens, self.tokens + refill)
        self.last_update = now


class CircuitBreaker:
    """
    断路器
    
    防止故障服务持续重试，支持开路、半开、闭路三种状态。
    
    状态转换：
    - 闭路(CLOSED): 正常执行
    - 开路(OPEN): 拒绝执行
    - 半开(HALF_OPEN): 允许测试性执行
    
    示例:
        >>> breaker = CircuitBreaker(failure_threshold=5, recovery_timeout=30)
        >>> result = breaker.call(some_function, arg1, arg2)
    """
    
    class State(Enum):
        CLOSED = "closed"
        OPEN = "open"
        HALF_OPEN = "half_open"
    
    def __init__(
        self,
        failure_threshold: int = 5,
        recovery_timeout: float = 30.0,
        half_open_requests: int = 3,
        success_threshold: int = 2,
        backoff_strategy: BackoffStrategy = BackoffStrategy.EXPONENTIAL_JITTER,
        base_delay: float = 1.0
    ):
        """
        初始化断路器
        
        Args:
            failure_threshold: 触发断路的失败次数阈值
            recovery_timeout: 恢复超时时间（秒）
            half_open_requests: 半开状态下允许的测试请求数
            success_threshold: 半开状态成功恢复阈值
            backoff_strategy: 退避策略
            base_delay: 基础延迟
        """
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        self.half_open_requests = half_open_requests
        self.success_threshold = success_threshold
        self.state = self.State.CLOSED
        self.failure_count = 0
        self.success_count = 0
        self.half_open_count = 0
        self.last_failure_time: Optional[float] = None
        self.calculator = BackoffCalculator(
            strategy=backoff_strategy,
            base_delay=base_delay
        )
    
    def call(self, func: Callable, *args, **kwargs):
        """
        通过断路器执行函数
        
        Args:
            func: 要执行的函数
            *args: 位置参数
            **kwargs: 关键字参数
        
        Returns:
            函数返回值
        
        Raises:
            RuntimeError: 断路器处于开路状态
            Exception: 函数执行失败
        """
        if self.state == self.State.OPEN:
            if self._should_attempt_recovery():
                self._transition_to_half_open()
            else:
                raise RuntimeError("断路器处于开路状态，拒绝请求")
        
        try:
            result = func(*args, **kwargs)
            self._on_success()
            return result
        except Exception as e:
            self._on_failure()
            raise
    
    def _should_attempt_recovery(self) -> bool:
        """检查是否应该尝试恢复"""
        if self.last_failure_time is None:
            return True
        return time.time() - self.last_failure_time >= self.recovery_timeout
    
    def _transition_to_half_open(self):
        """转换到半开状态"""
        self.state = self.State.HALF_OPEN
        self.half_open_count = 0
        self.success_count = 0
    
    def _on_success(self):
        """成功回调"""
        self.failure_count = 0
        
        if self.state == self.State.HALF_OPEN:
            self.success_count += 1
            self.half_open_count += 1
            
            if self.success_count >= self.success_threshold:
                self.state = self.State.CLOSED
                self.success_count = 0
                self.half_open_count = 0
    
    def _on_failure(self):
        """失败回调"""
        self.failure_count += 1
        self.last_failure_time = time.time()
        
        if self.state == self.State.HALF_OPEN:
            self.half_open_count += 1
            if self.half_open_count >= self.half_open_requests:
                self.state = self.State.OPEN
        elif self.failure_count >= self.failure_threshold:
            self.state = self.State.OPEN
    
    def reset(self):
        """重置断路器"""
        self.state = self.State.CLOSED
        self.failure_count = 0
        self.success_count = 0
        self.half_open_count = 0
        self.last_failure_time = None
    
    @property
    def is_open(self) -> bool:
        """断路器是否处于开路状态"""
        return self.state == self.State.OPEN
    
    @property
    def is_closed(self) -> bool:
        """断路器是否处于闭路状态"""
        return self.state == self.State.CLOSED
    
    @property
    def is_half_open(self) -> bool:
        """断路器是否处于半开状态"""
        return self.state == self.State.HALF_OPEN


class TimeoutRetry:
    """
    超时重试
    
    结合超时和重试机制。
    
    示例:
        >>> tr = TimeoutRetry(max_retries=3, timeout=5.0)
        >>> result = tr.execute(slow_function, arg1)
    """
    
    def __init__(
        self,
        max_retries: int = 3,
        timeout: float = 30.0,
        strategy: BackoffStrategy = BackoffStrategy.EXPONENTIAL_JITTER,
        base_delay: float = 1.0,
        max_delay: float = 300.0
    ):
        """
        初始化超时重试
        
        Args:
            max_retries: 最大重试次数
            timeout: 每次操作的超时时间（秒）
            strategy: 退避策略
            base_delay: 基础延迟
            max_delay: 最大延迟
        """
        self.max_retries = max_retries
        self.timeout = timeout
        self.calculator = BackoffCalculator(
            strategy=strategy,
            base_delay=base_delay,
            max_delay=max_delay
        )
    
    def execute(self, func: Callable, *args, **kwargs):
        """
        执行带超时的函数
        
        使用简单的超时检测，不依赖 threading 或 signal。
        """
        last_exception = None
        
        for attempt in range(self.max_retries + 1):
            try:
                start = time.time()
                
                # 注意：这里不使用真正的超时机制（需要 threading/signal）
                # 而是依赖调用者提供可中断的函数
                result = func(*args, **kwargs)
                
                elapsed = time.time() - start
                if elapsed > self.timeout:
                    raise TimeoutError(f"操作超时: {elapsed:.2f}秒 > {self.timeout}秒")
                
                return result
            except (Exception, TimeoutError) as e:
                last_exception = e
                
                if attempt < self.max_retries:
                    delay = self.calculator.calculate(attempt)
                    time.sleep(delay)
        
        raise last_exception


def calculate_backoff(
    attempt: int,
    strategy: str = "exponential",
    base_delay: float = 1.0,
    max_delay: float = 300.0,
    multiplier: float = 2.0,
    jitter_type: JitterType = JitterType.NONE,
    seed: Optional[int] = 42
) -> float:
    """
    快捷函数：计算退避时间
    
    Args:
        attempt: 尝试次数（从 0 开始）
        strategy: 策略名称 ("fixed", "linear", "exponential", "polynomial")
        base_delay: 基础延迟
        max_delay: 最大延迟
        multiplier: 乘数因子
        jitter_type: 抖动类型（默认为无抖动）
        seed: 随机种子
    
    Returns:
        延迟时间（秒）
    
    示例:
        >>> delay = calculate_backoff(2, "exponential", base_delay=0.5)
        >>> print(f"等待 {delay} 秒")
    """
    strategy_map = {
        "fixed": BackoffStrategy.FIXED,
        "linear": BackoffStrategy.LINEAR,
        "exponential": BackoffStrategy.EXPONENTIAL,
        "polynomial": BackoffStrategy.POLYNOMIAL
    }
    
    calc = BackoffCalculator(
        strategy=strategy_map.get(strategy, BackoffStrategy.EXPONENTIAL),
        base_delay=base_delay,
        max_delay=max_delay,
        multiplier=multiplier,
        jitter_type=jitter_type,
        seed=seed
    )
    
    return calc.calculate(attempt)


def create_retry_generator(
    max_retries: int,
    strategy: BackoffStrategy = BackoffStrategy.EXPONENTIAL_JITTER,
    base_delay: float = 1.0,
    max_delay: float = 300.0,
    multiplier: float = 2.0,
    jitter_type: JitterType = JitterType.FULL,
    seed: Optional[int] = None
) -> Generator[float, None, None]:
    """
    创建重试延迟生成器
    
    示例:
        >>> for delay in create_retry_generator(5):
        ...     print(f"重试前等待 {delay:.2f} 秒")
        ...     time.sleep(delay)
    """
    calc = BackoffCalculator(
        strategy=strategy,
        base_delay=base_delay,
        max_delay=max_delay,
        multiplier=multiplier,
        jitter_type=jitter_type,
        seed=seed
    )
    
    yield from calc.delays(max_retries)


# 预定义的常用配置
EXPONENTIAL_BACKOFF = {
    "strategy": BackoffStrategy.EXPONENTIAL,
    "base_delay": 1.0,
    "max_delay": 300.0,
    "multiplier": 2.0
}

LINEAR_BACKOFF = {
    "strategy": BackoffStrategy.LINEAR,
    "base_delay": 1.0,
    "max_delay": 60.0
}

FIXED_BACKOFF = {
    "strategy": BackoffStrategy.FIXED,
    "base_delay": 1.0
}

FAST_RETRY = {
    "strategy": BackoffStrategy.EXPONENTIAL_JITTER,
    "base_delay": 0.1,
    "max_delay": 10.0,
    "multiplier": 2.0
}

CONSERVATIVE_RETRY = {
    "strategy": BackoffStrategy.EXPONENTIAL_JITTER,
    "base_delay": 2.0,
    "max_delay": 600.0,
    "multiplier": 3.0
}