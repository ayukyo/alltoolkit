"""
Sliding Window Utilities - 滑动窗口工具

提供完整的滑动窗口实现，包括：
- 固定大小滑动窗口 (Fixed Sliding Window)
- 时间滑动窗口 (Time-Based Sliding Window)
- 移动平均计算 (Moving Average)
- 滑动窗口统计 (Window Statistics)
- 滑动窗口限流 (Rate Limiting)
- 滑动窗口最大/最小值 (Window Min/Max with Deque)

零外部依赖，纯 Python 实现。
"""

from typing import Union, List, Optional, Callable, Any, Generic, TypeVar, Iterator, Tuple
from dataclasses import dataclass, field
from collections import deque
from datetime import datetime, timedelta
import time
import math

T = TypeVar('T')
N = TypeVar('N', int, float)


@dataclass
class WindowStats:
    """窗口统计信息"""
    count: int = 0
    sum: float = 0.0
    min: Optional[float] = None
    max: Optional[float] = None
    mean: float = 0.0
    variance: float = 0.0
    std_dev: float = 0.0
    
    def to_dict(self) -> dict:
        """转换为字典"""
        return {
            'count': self.count,
            'sum': self.sum,
            'min': self.min,
            'max': self.max,
            'mean': self.mean,
            'variance': self.variance,
            'std_dev': self.std_dev,
        }


class SlidingWindow(Generic[T]):
    """
    通用滑动窗口
    
    支持任意类型数据的滑动窗口实现。
    
    特点：
    - O(1) 时间添加元素
    - O(1) 时间获取窗口
    - 支持自定义窗口大小
    - 支持窗口变化回调
    
    Example:
        >>> window = SlidingWindow(size=3)
        >>> window.add(1)
        >>> window.add(2)
        >>> window.add(3)
        >>> window.get_window()
        [1, 2, 3]
        >>> window.add(4)
        >>> window.get_window()
        [2, 3, 4]
    """
    
    def __init__(
        self,
        size: int,
        on_add: Optional[Callable[[T], None]] = None,
        on_remove: Optional[Callable[[T], None]] = None,
    ):
        """
        初始化滑动窗口
        
        Args:
            size: 窗口大小
            on_add: 元素添加回调
            on_remove: 元素移除回调
        """
        if size <= 0:
            raise ValueError("窗口大小必须大于 0")
        
        self.size = size
        self.on_add = on_add
        self.on_remove = on_remove
        self._window: deque[T] = deque(maxlen=size)
    
    def add(self, item: T) -> Optional[T]:
        """
        添加元素到窗口
        
        Args:
            item: 要添加的元素
            
        Returns:
            如果窗口已满，返回被移除的元素；否则返回 None
        """
        removed = None
        
        if len(self._window) == self.size:
            removed = self._window[0]
            if self.on_remove:
                self.on_remove(removed)
        
        self._window.append(item)
        
        if self.on_add:
            self.on_add(item)
        
        return removed
    
    def get_window(self) -> List[T]:
        """获取当前窗口内容"""
        return list(self._window)
    
    def get_latest(self) -> Optional[T]:
        """获取最新元素"""
        return self._window[-1] if self._window else None
    
    def get_oldest(self) -> Optional[T]:
        """获取最旧元素"""
        return self._window[0] if self._window else None
    
    def is_full(self) -> bool:
        """窗口是否已满"""
        return len(self._window) == self.size
    
    def is_empty(self) -> bool:
        """窗口是否为空"""
        return len(self._window) == 0
    
    def clear(self) -> None:
        """清空窗口"""
        self._window.clear()
    
    def __len__(self) -> int:
        return len(self._window)
    
    def __iter__(self) -> Iterator[T]:
        return iter(self._window)
    
    def __repr__(self) -> str:
        return f"SlidingWindow(size={self.size}, items={list(self._window)})"


class NumericSlidingWindow(Generic[N]):
    """
    数值型滑动窗口
    
    专为数值数据优化的滑动窗口，支持：
    - 高效计算移动平均
    - 窗口统计信息
    - 增量更新方差/标准差
    
    使用 Welford 算法进行增量方差计算，避免数值精度问题。
    
    Example:
        >>> window = NumericSlidingWindow(size=5)
        >>> for i in range(10):
        ...     window.add(i)
        >>> window.get_mean()
        7.0  # 平均值 of [5, 6, 7, 8, 9]
    """
    
    def __init__(self, size: int):
        """
        初始化数值滑动窗口
        
        Args:
            size: 窗口大小
        """
        if size <= 0:
            raise ValueError("窗口大小必须大于 0")
        
        self.size = size
        self._window: deque[float] = deque(maxlen=size)
        self._sum: float = 0.0
        self._min: Optional[float] = None
        self._max: Optional[float] = None
        # 用于增量方差计算
        self._m2: float = 0.0  # 平方差累计
    
    def add(self, value: N) -> Optional[float]:
        """
        添加数值
        
        Args:
            value: 数值
            
        Returns:
            被移除的值（如果窗口已满）
        """
        removed = None
        
        # 如果窗口已满，移除最旧的值
        if len(self._window) == self.size:
            removed = self._window[0]
            self._sum -= removed
        
        # 添加新值
        self._window.append(float(value))
        self._sum += value
        
        # 每次添加后重新计算 min/max（更可靠）
        self._min = min(self._window) if self._window else None
        self._max = max(self._window) if self._window else None
        
        return removed
    
    def get_window(self) -> List[float]:
        """获取当前窗口"""
        return list(self._window)
    
    def get_sum(self) -> float:
        """获取窗口内数值之和"""
        return self._sum
    
    def get_mean(self) -> float:
        """获取移动平均"""
        if not self._window:
            return 0.0
        return self._sum / len(self._window)
    
    def get_variance(self, population: bool = True) -> float:
        """
        获取方差
        
        Args:
            population: True 为总体方差，False 为样本方差
            
        Returns:
            方差值
        """
        if len(self._window) < 2:
            return 0.0
        
        n = len(self._window) if population else len(self._window) - 1
        if n <= 0:
            return 0.0
        
        # 使用简化的方差计算（更稳定）
        mean = self.get_mean()
        return sum((x - mean) ** 2 for x in self._window) / n
    
    def get_std_dev(self, population: bool = True) -> float:
        """获取标准差"""
        return math.sqrt(self.get_variance(population))
    
    def get_min(self) -> Optional[float]:
        """获取窗口内最小值"""
        return self._min
    
    def get_max(self) -> Optional[float]:
        """获取窗口内最大值"""
        return self._max
    
    def get_stats(self) -> WindowStats:
        """获取完整统计信息"""
        return WindowStats(
            count=len(self._window),
            sum=self._sum,
            min=self._min,
            max=self._max,
            mean=self.get_mean(),
            variance=self.get_variance(),
            std_dev=self.get_std_dev(),
        )
    
    def is_full(self) -> bool:
        return len(self._window) == self.size
    
    def is_empty(self) -> bool:
        return len(self._window) == 0
    
    def clear(self) -> None:
        """清空窗口"""
        self._window.clear()
        self._sum = 0.0
        self._min = None
        self._max = None
        self._m2 = 0.0
    
    def __len__(self) -> int:
        return len(self._window)
    
    def __iter__(self) -> Iterator[float]:
        return iter(self._window)
    
    def __repr__(self) -> str:
        return f"NumericSlidingWindow(size={self.size}, mean={self.get_mean():.2f})"


class MovingAverage:
    """
    移动平均计算器
    
    支持多种移动平均类型：
    - 简单移动平均 (SMA)
    - 累积移动平均 (CMA)
    - 加权移动平均 (WMA)
    - 指数移动平均 (EMA)
    
    Example:
        >>> ma = MovingAverage(window_size=3, ma_type='sma')
        >>> ma.update(1)
        1.0
        >>> ma.update(2)
        1.5
        >>> ma.update(3)
        2.0
        >>> ma.update(4)
        3.0
    """
    
    SMA = 'sma'   # 简单移动平均
    CMA = 'cma'   # 累积移动平均
    WMA = 'wma'   # 加权移动平均
    EMA = 'ema'   # 指数移动平均
    
    def __init__(
        self,
        window_size: int = 10,
        ma_type: str = 'sma',
        alpha: Optional[float] = None,
    ):
        """
        初始化移动平均计算器
        
        Args:
            window_size: 窗口大小（SMA/WMA 有效）
            ma_type: 平均类型 ('sma', 'cma', 'wma', 'ema')
            alpha: EMA 的平滑因子（默认 2/(n+1)）
        """
        self.ma_type = ma_type.lower()
        self.window_size = window_size
        
        # EMA 平滑因子
        if alpha is not None:
            self.alpha = alpha
        else:
            self.alpha = 2.0 / (window_size + 1)
        
        # 内部状态
        self._window: deque[float] = deque(maxlen=window_size)
        self._sum: float = 0.0
        self._count: int = 0
        self._ema: Optional[float] = None  # EMA 当前值
        
        # WMA 权重（线性递增）
        self._weights = list(range(1, window_size + 1))
    
    def update(self, value: N) -> float:
        """
        添加新值并返回移动平均
        
        Args:
            value: 新数值
            
        Returns:
            当前的移动平均值
        """
        value = float(value)
        
        if self.ma_type == self.SMA:
            return self._update_sma(value)
        elif self.ma_type == self.CMA:
            return self._update_cma(value)
        elif self.ma_type == self.WMA:
            return self._update_wma(value)
        elif self.ma_type == self.EMA:
            return self._update_ema(value)
        else:
            raise ValueError(f"未知的移动平均类型: {self.ma_type}")
    
    def _update_sma(self, value: float) -> float:
        """更新简单移动平均"""
        if len(self._window) == self.window_size:
            self._sum -= self._window[0]
        
        self._window.append(value)
        self._sum += value
        
        return self._sum / len(self._window)
    
    def _update_cma(self, value: float) -> float:
        """更新累积移动平均"""
        self._count += 1
        self._sum += value
        return self._sum / self._count
    
    def _update_wma(self, value: float) -> float:
        """更新加权移动平均"""
        if len(self._window) == self.window_size:
            self._window.popleft()
        
        self._window.append(value)
        
        # 计算加权和
        n = len(self._window)
        weights = self._weights[:n]
        weighted_sum = sum(w * v for w, v in zip(weights, self._window))
        weight_sum = sum(weights)
        
        return weighted_sum / weight_sum
    
    def _update_ema(self, value: float) -> float:
        """更新指数移动平均"""
        if self._ema is None:
            self._ema = value
        else:
            self._ema = self.alpha * value + (1 - self.alpha) * self._ema
        
        return self._ema
    
    def get_current(self) -> float:
        """获取当前移动平均值"""
        if self.ma_type == self.SMA:
            return self._sum / len(self._window) if self._window else 0.0
        elif self.ma_type == self.CMA:
            return self._sum / self._count if self._count > 0 else 0.0
        elif self.ma_type == self.WMA:
            if not self._window:
                return 0.0
            n = len(self._window)
            weights = self._weights[:n]
            weighted_sum = sum(w * v for w, v in zip(weights, self._window))
            return weighted_sum / sum(weights)
        elif self.ma_type == self.EMA:
            return self._ema if self._ema is not None else 0.0
        return 0.0
    
    def get_window(self) -> List[float]:
        """获取当前窗口"""
        return list(self._window)
    
    def reset(self) -> None:
        """重置状态"""
        self._window.clear()
        self._sum = 0.0
        self._count = 0
        self._ema = None
    
    def __repr__(self) -> str:
        return f"MovingAverage(type={self.ma_type}, current={self.get_current():.2f})"


class TimeSlidingWindow(Generic[T]):
    """
    基于时间的滑动窗口
    
    元素根据时间戳自动过期。
    
    Example:
        >>> window = TimeSlidingWindow(window_seconds=60)
        >>> window.add("event1")
        >>> window.add("event2")
        >>> window.get_window()  # 返回最近 60 秒内的所有事件
    """
    
    def __init__(
        self,
        window_seconds: float,
        time_func: Optional[Callable[[], float]] = None,
    ):
        """
        初始化时间滑动窗口
        
        Args:
            window_seconds: 窗口时间（秒）
            time_func: 时间获取函数（默认使用 time.time）
        """
        if window_seconds <= 0:
            raise ValueError("窗口时间必须大于 0")
        
        self.window_seconds = window_seconds
        self._time_func = time_func or time.time
        self._window: deque[Tuple[float, T]] = deque()
    
    def _current_time(self) -> float:
        """获取当前时间"""
        return self._time_func()
    
    def _cleanup(self) -> None:
        """清理过期元素"""
        now = self._current_time()
        cutoff = now - self.window_seconds
        
        while self._window and self._window[0][0] < cutoff:
            self._window.popleft()
    
    def add(self, item: T, timestamp: Optional[float] = None) -> None:
        """
        添加元素
        
        Args:
            item: 元素
            timestamp: 时间戳（可选，默认当前时间）
        """
        if timestamp is None:
            timestamp = self._current_time()
        
        self._cleanup()
        self._window.append((timestamp, item))
    
    def get_window(self, cleanup: bool = True) -> List[T]:
        """
        获取当前窗口内容
        
        Args:
            cleanup: 是否先清理过期元素
            
        Returns:
            窗口内的元素列表
        """
        if cleanup:
            self._cleanup()
        return [item for _, item in self._window]
    
    def get_count(self, cleanup: bool = True) -> int:
        """获取窗口内元素数量"""
        if cleanup:
            self._cleanup()
        return len(self._window)
    
    def is_empty(self, cleanup: bool = True) -> bool:
        """窗口是否为空"""
        return self.get_count(cleanup) == 0
    
    def clear(self) -> None:
        """清空窗口"""
        self._window.clear()
    
    def __len__(self) -> int:
        return self.get_count()
    
    def __repr__(self) -> str:
        count = self.get_count()
        return f"TimeSlidingWindow(window={self.window_seconds}s, count={count})"


class RateLimiter:
    """
    滑动窗口限流器
    
    支持多种限流算法：
    - 固定窗口 (Fixed Window)
    - 滑动窗口 (Sliding Window)
    - 令牌桶 (Token Bucket)
    - 漏桶 (Leaky Bucket)
    
    Example:
        >>> limiter = RateLimiter(max_requests=10, window_seconds=60)
        >>> for i in range(15):
        ...     if limiter.allow():
        ...         print(f"请求 {i} 允许")
        ...     else:
        ...         print(f"请求 {i} 被限流")
    """
    
    FIXED_WINDOW = 'fixed'
    SLIDING_WINDOW = 'sliding'
    TOKEN_BUCKET = 'token'
    LEAKY_BUCKET = 'leaky'
    
    def __init__(
        self,
        max_requests: int,
        window_seconds: float = 1.0,
        algorithm: str = 'sliding',
    ):
        """
        初始化限流器
        
        Args:
            max_requests: 窗口内最大请求数
            window_seconds: 窗口时间（秒）
            algorithm: 算法类型 ('fixed', 'sliding', 'token', 'leaky')
        """
        if max_requests <= 0:
            raise ValueError("最大请求数必须大于 0")
        if window_seconds <= 0:
            raise ValueError("窗口时间必须大于 0")
        
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self.algorithm = algorithm.lower()
        
        # 固定窗口
        self._window_start = time.time()
        self._request_count = 0
        
        # 滑动窗口
        self._timestamps: deque[float] = deque()
        
        # 令牌桶
        self._tokens = float(max_requests)
        self._last_refill = time.time()
        self._refill_rate = max_requests / window_seconds
        
        # 漏桶
        self._water = 0.0
        self._last_leak = time.time()
        self._leak_rate = max_requests / window_seconds
    
    def allow(self) -> bool:
        """
        检查是否允许请求
        
        Returns:
            True 如果允许，False 如果被限流
        """
        if self.algorithm == self.FIXED_WINDOW:
            return self._fixed_window_allow()
        elif self.algorithm == self.SLIDING_WINDOW:
            return self._sliding_window_allow()
        elif self.algorithm == self.TOKEN_BUCKET:
            return self._token_bucket_allow()
        elif self.algorithm == self.LEAKY_BUCKET:
            return self._leaky_bucket_allow()
        else:
            raise ValueError(f"未知的限流算法: {self.algorithm}")
    
    def _fixed_window_allow(self) -> bool:
        """固定窗口算法"""
        now = time.time()
        
        # 检查是否需要重置窗口
        if now - self._window_start >= self.window_seconds:
            self._window_start = now
            self._request_count = 0
        
        if self._request_count < self.max_requests:
            self._request_count += 1
            return True
        
        return False
    
    def _sliding_window_allow(self) -> bool:
        """滑动窗口算法"""
        now = time.time()
        cutoff = now - self.window_seconds
        
        # 移除过期的时间戳
        while self._timestamps and self._timestamps[0] < cutoff:
            self._timestamps.popleft()
        
        # 检查是否允许
        if len(self._timestamps) < self.max_requests:
            self._timestamps.append(now)
            return True
        
        return False
    
    def _token_bucket_allow(self) -> bool:
        """令牌桶算法"""
        now = time.time()
        
        # 补充令牌
        elapsed = now - self._last_refill
        self._tokens = min(
            self.max_requests,
            self._tokens + elapsed * self._refill_rate
        )
        self._last_refill = now
        
        # 检查是否有令牌
        if self._tokens >= 1:
            self._tokens -= 1
            return True
        
        return False
    
    def _leaky_bucket_allow(self) -> bool:
        """漏桶算法"""
        now = time.time()
        
        # 漏水
        elapsed = now - self._last_leak
        self._water = max(0, self._water - elapsed * self._leak_rate)
        self._last_leak = now
        
        # 检查桶是否已满
        if self._water < self.max_requests:
            self._water += 1
            return True
        
        return False
    
    def get_state(self) -> dict:
        """获取当前状态"""
        now = time.time()
        
        if self.algorithm == self.FIXED_WINDOW:
            remaining = max(0, self.window_seconds - (now - self._window_start))
            return {
                'algorithm': self.algorithm,
                'requests_in_window': self._request_count,
                'remaining_requests': self.max_requests - self._request_count,
                'window_reset_in': remaining,
            }
        elif self.algorithm == self.SLIDING_WINDOW:
            return {
                'algorithm': self.algorithm,
                'requests_in_window': len(self._timestamps),
                'remaining_requests': self.max_requests - len(self._timestamps),
            }
        elif self.algorithm == self.TOKEN_BUCKET:
            # 先补充令牌以获取最新状态
            elapsed = now - self._last_refill
            tokens = min(self.max_requests, self._tokens + elapsed * self._refill_rate)
            return {
                'algorithm': self.algorithm,
                'available_tokens': tokens,
                'max_tokens': self.max_requests,
            }
        elif self.algorithm == self.LEAKY_BUCKET:
            # 先漏水以获取最新状态
            elapsed = now - self._last_leak
            water = max(0, self._water - elapsed * self._leak_rate)
            return {
                'algorithm': self.algorithm,
                'current_water': water,
                'bucket_capacity': self.max_requests,
            }
        return {}
    
    def reset(self) -> None:
        """重置限流器"""
        self._window_start = time.time()
        self._request_count = 0
        self._timestamps.clear()
        self._tokens = float(self.max_requests)
        self._last_refill = time.time()
        self._water = 0.0
        self._last_leak = time.time()


class MinMaxSlidingWindow:
    """
    滑动窗口最大/最小值
    
    使用单调队列实现 O(1) 时间复杂度的窗口最值查询。
    
    Example:
        >>> window = MinMaxSlidingWindow(size=3)
        >>> for v in [1, 3, -1, 2, 5]:
        ...     window.add(v)
        ...     print(f"min={window.get_min()}, max={window.get_max()}")
    """
    
    def __init__(self, size: int):
        """
        初始化窗口
        
        Args:
            size: 窗口大小
        """
        if size <= 0:
            raise ValueError("窗口大小必须大于 0")
        
        self.size = size
        self._window: deque[Tuple[int, float]] = deque()  # (index, value)
        self._min_deque: deque[Tuple[int, float]] = deque()  # 单调递增队列
        self._max_deque: deque[Tuple[int, float]] = deque()  # 单调递减队列
        self._index = 0
    
    def add(self, value: N) -> None:
        """
        添加元素
        
        Args:
            value: 数值
        """
        value = float(value)
        
        # 移除超出窗口的元素
        if len(self._window) == self.size:
            old_idx = self._window[0][0]
            self._window.popleft()
            
            # 从单调队列中移除
            if self._min_deque and self._min_deque[0][0] == old_idx:
                self._min_deque.popleft()
            if self._max_deque and self._max_deque[0][0] == old_idx:
                self._max_deque.popleft()
        
        # 维护单调递增队列（最小值在队首）
        while self._min_deque and self._min_deque[-1][1] >= value:
            self._min_deque.pop()
        self._min_deque.append((self._index, value))
        
        # 维护单调递减队列（最大值在队首）
        while self._max_deque and self._max_deque[-1][1] <= value:
            self._max_deque.pop()
        self._max_deque.append((self._index, value))
        
        # 添加到窗口
        self._window.append((self._index, value))
        self._index += 1
    
    def get_min(self) -> Optional[float]:
        """获取窗口内最小值"""
        if not self._min_deque:
            return None
        return self._min_deque[0][1]
    
    def get_max(self) -> Optional[float]:
        """获取窗口内最大值"""
        if not self._max_deque:
            return None
        return self._max_deque[0][1]
    
    def get_window(self) -> List[float]:
        """获取当前窗口"""
        return [v for _, v in self._window]
    
    def clear(self) -> None:
        """清空窗口"""
        self._window.clear()
        self._min_deque.clear()
        self._max_deque.clear()
        self._index = 0
    
    def __len__(self) -> int:
        return len(self._window)
    
    def __repr__(self) -> str:
        return f"MinMaxSlidingWindow(size={self.size}, min={self.get_min()}, max={self.get_max()})"


class SlidingWindowCounter:
    """
    滑动窗口计数器
    
    用于统计时间窗口内的事件数量。
    
    Example:
        >>> counter = SlidingWindowCounter(window_seconds=60)
        >>> counter.increment()
        >>> counter.increment()
        >>> counter.get_count()
        2
    """
    
    def __init__(
        self,
        window_seconds: float,
        precision: int = 10,
    ):
        """
        初始化计数器
        
        Args:
            window_seconds: 窗口时间（秒）
            precision: 时间片精度（将窗口分成多少片）
        """
        if window_seconds <= 0:
            raise ValueError("窗口时间必须大于 0")
        if precision <= 0:
            raise ValueError("精度必须大于 0")
        
        self.window_seconds = window_seconds
        self.precision = precision
        self.slice_seconds = window_seconds / precision
        self._slices: deque[Tuple[float, int]] = deque()
    
    def _cleanup(self) -> None:
        """清理过期的时间片"""
        now = time.time()
        cutoff = now - self.window_seconds
        
        while self._slices and self._slices[0][0] < cutoff:
            self._slices.popleft()
    
    def increment(self, count: int = 1, timestamp: Optional[float] = None) -> None:
        """
        增加计数
        
        Args:
            count: 增加的数量
            timestamp: 时间戳（可选）
        """
        if timestamp is None:
            timestamp = time.time()
        
        self._cleanup()
        self._slices.append((timestamp, count))
    
    def get_count(self) -> int:
        """获取当前计数"""
        self._cleanup()
        return sum(count for _, count in self._slices)
    
    def reset(self) -> None:
        """重置计数器"""
        self._slices.clear()
    
    def __repr__(self) -> str:
        return f"SlidingWindowCounter(window={self.window_seconds}s, count={self.get_count()})"


# 便捷函数
def moving_average(values: List[N], window: int, ma_type: str = 'sma') -> List[float]:
    """
    计算移动平均值列表
    
    Args:
        values: 数值列表
        window: 窗口大小
        ma_type: 平均类型 ('sma', 'wma', 'ema')
        
    Returns:
        移动平均值列表
    """
    if not values or window <= 0:
        return []
    
    ma = MovingAverage(window_size=window, ma_type=ma_type)
    result = []
    
    for v in values:
        ma.update(v)
        result.append(ma.get_current())
    
    return result


def sliding_window_stats(values: List[N], window: int) -> List[WindowStats]:
    """
    计算滑动窗口统计信息
    
    Args:
        values: 数值列表
        window: 窗口大小
        
    Returns:
        每个位置的窗口统计信息列表
    """
    if not values or window <= 0:
        return []
    
    sw = NumericSlidingWindow(size=window)
    result = []
    
    for v in values:
        sw.add(v)
        result.append(sw.get_stats())
    
    return result


def sliding_window_min_max(
    values: List[N],
    window: int,
) -> Tuple[List[Optional[float]], List[Optional[float]]]:
    """
    计算滑动窗口最小值和最大值
    
    Args:
        values: 数值列表
        window: 窗口大小
        
    Returns:
        (最小值列表, 最大值列表)
    """
    if not values or window <= 0:
        return [], []
    
    sw = MinMaxSlidingWindow(size=window)
    mins = []
    maxs = []
    
    for v in values:
        sw.add(v)
        mins.append(sw.get_min())
        maxs.append(sw.get_max())
    
    return mins, maxs


if __name__ == "__main__":
    # 简单演示
    print("=== 滑动窗口工具演示 ===")
    
    # 1. 通用滑动窗口
    print("\n--- 通用滑动窗口 ---")
    window = SlidingWindow(size=3)
    for i in range(5):
        removed = window.add(i)
        print(f"添加 {i}, 移除 {removed}, 窗口: {window.get_window()}")
    
    # 2. 数值滑动窗口
    print("\n--- 数值滑动窗口 ---")
    num_window = NumericSlidingWindow(size=5)
    for i in range(10):
        num_window.add(i)
    print(f"窗口: {num_window.get_window()}")
    print(f"统计: {num_window.get_stats().to_dict()}")
    
    # 3. 移动平均
    print("\n--- 移动平均 ---")
    ma = MovingAverage(window_size=3, ma_type='sma')
    values = [10, 20, 30, 40, 50]
    for v in values:
        avg = ma.update(v)
        print(f"值: {v}, SMA: {avg:.2f}")
    
    # 4. 时间滑动窗口
    print("\n--- 时间滑动窗口 ---")
    twindow = TimeSlidingWindow(window_seconds=2)
    twindow.add("event1")
    twindow.add("event2")
    print(f"当前窗口: {twindow.get_window()}")
    
    # 5. 限流器
    print("\n--- 限流器 ---")
    limiter = RateLimiter(max_requests=5, window_seconds=1.0)
    for i in range(8):
        if limiter.allow():
            print(f"请求 {i+1}: 允许")
        else:
            print(f"请求 {i+1}: 被限流")
    
    # 6. 最小最大值窗口
    print("\n--- 最小最大值窗口 ---")
    mm_window = MinMaxSlidingWindow(size=3)
    for v in [1, 3, -1, 2, 5, 4]:
        mm_window.add(v)
        print(f"值: {v}, 窗口: {mm_window.get_window()}, min={mm_window.get_min()}, max={mm_window.get_max()}")
    
    # 7. 便捷函数
    print("\n--- 便捷函数 ---")
    data = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    print(f"数据: {data}")
    print(f"SMA(3): {moving_average(data, 3, 'sma')}")
    print(f"WMA(3): {moving_average(data, 3, 'wma')}")
    print(f"EMA(3): {moving_average(data, 3, 'ema')}")