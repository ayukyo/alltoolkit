# Backoff Utils 🔄

退避算法工具模块，提供各种重试策略、限流和熔断器实现。

## 功能特性

- **多种退避策略** - 固定、线性、指数、指数+抖动、装饰相关、多项式
- **RetryExecutor** - 通用重试执行器，支持异常过滤和回调
- **RateLimiter** - 令牌桶限流器
- **CircuitBreaker** - 熔断器模式，防止级联故障
- **TimeoutRetry** - 超时控制的重试包装器
- **零外部依赖** - 纯 Python 实现

## 快速开始

```python
from backoff_utils import (
    BackoffCalculator, BackoffStrategy, JitterType,
    retry, RateLimiter, CircuitBreaker, TimeoutRetry
)

# 基础指数退避
calc = BackoffCalculator(strategy=BackoffStrategy.EXPONENTIAL_JITTER)
for attempt in range(5):
    delay = calc.calculate(attempt)
    print(f"尝试 {attempt}: 等待 {delay:.2f}s")
```

## 退避计算器

### 基本用法

```python
from backoff_utils import BackoffCalculator, BackoffStrategy, JitterType

# 指数退避 + 完全抖动（推荐生产环境）
calc = BackoffCalculator(
    strategy=BackoffStrategy.EXPONENTIAL_JITTER,
    base_delay=1.0,
    max_delay=60.0,
    jitter_type=JitterType.FULL
)

for attempt in range(10):
    delay = calc.calculate(attempt)
    print(f"Attempt {attempt}: backoff {delay:.2f}s")
```

### 退避策略

```python
from backoff_utils import BackoffCalculator, BackoffStrategy

# 固定延迟
calc = BackoffCalculator(strategy=BackoffStrategy.FIXED, base_delay=1.0)

# 线性延迟
calc = BackoffCalculator(strategy=BackoffStrategy.LINEAR, base_delay=1.0)

# 指数延迟（无抖动）
calc = BackoffCalculator(strategy=BackoffStrategy.EXPONENTIAL, base_delay=1.0, multiplier=2.0)

# 装饰延迟（AWS SDK 风格）
calc = BackoffCalculator(strategy=BackoffStrategy.DECORRELATED, base_delay=1.0, multiplier=3.0)

# 多项式延迟
calc = BackoffCalculator(strategy=BackoffStrategy.POLYNOMIAL, base_delay=0.5, polynomial_degree=2.0)
```

### 生成器模式

```python
from backoff_utils import create_retry_generator

for delay in create_retry_generator(max_retries=5, base_delay=1.0):
    print(f"等待 {delay:.2f}s")
```

## RetryExecutor

```python
from backoff_utils import RetryExecutor, BackoffStrategy

executor = RetryExecutor(
    max_retries=3,
    base_delay=1.0,
    strategy=BackoffStrategy.EXPONENTIAL_JITTER
)

def unreliable_operation():
    import random
    if random.random() < 0.7:
        raise ConnectionError("网络错误")
    return "成功!"

# 执行重试
result = executor.execute(unreliable_operation)
```

### 带异常过滤

```python
from backoff_utils import RetryExecutor

executor = RetryExecutor(max_retries=3)

# 只对特定异常重试
result = executor.execute(
    unreliable_operation,
    retry_on=(ConnectionError, TimeoutError),  # 只对这些异常重试
    give_up_on=(ValueError, TypeError)          # 这些异常直接放弃
)
```

### 回调函数

```python
from backoff_utils import RetryExecutor

executor = RetryExecutor(max_retries=3)

result = executor.execute(
    risky_operation,
    on_retry=lambda attempt, delay: print(f"重试 #{attempt}, 等待 {delay:.1f}s"),
    on_success=lambda result: print(f"成功: {result}"),
    on_failure=lambda e: print(f"最终失败: {e}")
)
```

## RateLimiter（令牌桶限流）

```python
from backoff_utils import RateLimiter
import time

# 每秒 10 个请求，桶容量 20
limiter = RateLimiter(rate=10, capacity=20)

# 阻塞等待获取令牌
for i in range(25):
    limiter.acquire()
    print(f"请求 {i} 被处理")
```

### 非阻塞检查

```python
from backoff_utils import RateLimiter

limiter = RateLimiter(rate=5, capacity=10)

# 检查是否能获取令牌（不阻塞）
if limiter.try_acquire():
    print("允许执行")
else:
    print("被限流")
```

## CircuitBreaker（熔断器）

```python
from backoff_utils import CircuitBreaker
import random

breaker = CircuitBreaker(
    failure_threshold=3,    # 3 次失败后打开
    recovery_timeout=10.0,   # 10 秒后尝试半开
    expected_exception=ConnectionError
)

def unreliable_call():
    if random.random() < 0.7:
        raise ConnectionError("连接失败")
    return "OK"

# 正常调用
for i in range(10):
    try:
        result = breaker.call(unreliable_call)
        print(f"请求 {i}: {result}")
    except CircuitBreaker.OpenCircuitError:
        print(f"请求 {i}: 熔断器打开，拒绝请求")
```

### 状态管理

```python
breaker = CircuitBreaker(failure_threshold=3)

print(breaker.state)  # 'closed'
breaker.open()
print(breaker.state)  # 'open'
breaker.reset()
print(breaker.state)  # 'closed'
```

## TimeoutRetry

```python
from backoff_utils import TimeoutRetry
import time

wrapper = TimeoutRetry(timeout=2.0, max_retries=3)

def slow_operation():
    time.sleep(1.5)
    return "完成"

result = wrapper.execute(slow_operation)  # 2 秒超时限制
```

## 预定义配置

```python
from backoff_utils import (
    QUICK_RETRY, NORMAL_RETRY, AGGRESSIVE_RETRY,
    create_retry_generator
)

# 快速重试（API 调用）
for delay in QUICK_RETRY.delays(max_retries=5):
    print(f"等待 {delay:.2f}s")

# 普通重试（数据库操作）
for delay in NORMAL_RETRY.delays(max_retries=3):
    print(f"等待 {delay:.2f}s")

# 激进重试（关键操作）
for delay in AGGRESSIVE_RETRY.delays(max_retries=10):
    print(f"等待 {delay:.2f}s")
```

## calculate_backoff 便捷函数

```python
from backoff_utils import calculate_backoff

# 计算单次退避时间
delay = calculate_backoff(attempt=3, base_delay=1.0, strategy='exponential_jitter')
print(f"延迟: {delay:.2f}s")
```

## 策略对比

| 策略 | 描述 | 适用场景 |
|------|------|----------|
| FIXED | 固定延迟 | 简单的定时重试 |
| LINEAR | 线性增长 | 需要稳定增长的场景 |
| EXPONENTIAL | 指数增长 | 网络请求、API 调用 |
| EXPONENTIAL_JITTER | 指数+随机抖动 | **生产环境推荐**，防止雷鸣羊群 |
| DECORRELATED | 装饰延迟 | AWS SDK 默认策略 |
| POLYNOMIAL | 多项式增长 | 需要更平滑的增长曲线 |

## 测试

```bash
python -m pytest Python/backoff_utils/ -v
```

## 许可证

MIT License