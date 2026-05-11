"""
Rate Limiter Utils - 速率限制器工具库

提供多种速率限制算法的实现，用于 API 限流、防止滥用、流量控制等场景。

包含的算法：
- TokenBucket: 令牌桶算法 - 平滑限流，允许突发流量
- LeakyBucket: 漏桶算法 - 恒定速率输出
- SlidingWindow: 滑动窗口算法 - 精确计数，无边界问题
- FixedWindow: 固定窗口算法 - 简单高效，有边界突发问题

零外部依赖，仅使用 Python 标准库
"""

from .token_bucket import TokenBucket
from .leaky_bucket import LeakyBucket
from .sliding_window import SlidingWindow
from .fixed_window import FixedWindow
from .rate_limiter import RateLimiter, MultiRateLimiter, Algorithm
from .decorators import rate_limit, RateLimitExceeded

__all__ = [
    # 核心类
    'TokenBucket',
    'LeakyBucket',
    'SlidingWindow',
    'FixedWindow',
    'RateLimiter',
    'MultiRateLimiter',
    # 枚举
    'Algorithm',
    # 装饰器
    'rate_limit',
    # 异常
    'RateLimitExceeded',
]

__version__ = '1.0.0'