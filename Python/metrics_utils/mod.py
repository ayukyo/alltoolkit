"""
Metrics Utilities - 应用程序指标收集工具模块

提供 Counter、Gauge、Histogram、Summary 等核心指标类型，
支持指标注册、导出、时间窗口统计等功能。
零依赖，仅使用 Python 标准库。

Author: AllToolkit
Version: 1.0.0
"""

from typing import Optional, Union, List, Dict, Callable, Any
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from collections import defaultdict
import time
import threading
import math
import random


# ============================================================================
# 数据类
# ============================================================================

@dataclass
class MetricPoint:
    """指标数据点"""
    value: float
    timestamp: float  # Unix timestamp
    labels: Dict[str, str] = field(default_factory=dict)


@dataclass
class MetricSnapshot:
    """指标快照"""
    name: str
    metric_type: str
    value: float
    labels: Dict[str, str] = field(default_factory=dict)
    timestamp: float = field(default_factory=time.time)
    
    # Histogram/Summary 额外字段
    count: int = 0
    sum_value: float = 0.0
    buckets: Dict[str, int] = field(default_factory=dict)
    quantiles: Dict[float, float] = field(default_factory=dict)


# ============================================================================
# Counter - 计数器
# ============================================================================

class Counter:
    """
    计数器 - 只增不减的累计值
    
    用于记录只会增加的值，如请求数、错误数、任务完成数等。
    
    示例:
        counter = Counter('http_requests_total', 'Total HTTP requests')
        counter.inc()
        counter.inc(5)
        counter.with_labels(method='GET', path='/api').inc()
    """
    
    def __init__(self, name: str, description: str = "", 
                 labels: Optional[Dict[str, str]] = None):
        """
        初始化计数器
        
        Args:
            name: 指标名称
            description: 指标描述
            labels: 标签键值对
        """
        self._name = name
        self._description = description
        self._value = 0.0
        self._labels = labels or {}
        self._created_at = time.time()
        self._lock = threading.Lock()
    
    @property
    def name(self) -> str:
        return self._name
    
    @property
    def description(self) -> str:
        return self._description
    
    @property
    def value(self) -> float:
        with self._lock:
            return self._value
    
    @property
    def labels(self) -> Dict[str, str]:
        return self._labels.copy()
    
    def inc(self, amount: float = 1.0) -> 'Counter':
        """
        增加计数
        
        Args:
            amount: 增加的值（必须为正）
            
        Returns:
            self，支持链式调用
        """
        if amount < 0:
            raise ValueError("Counter can only be incremented by non-negative values")
        
        with self._lock:
            self._value += amount
        
        return self
    
    def with_labels(self, **kwargs: str) -> 'Counter':
        """
        创建带标签的计数器实例
        
        Returns:
            带标签的新 Counter 实例
        """
        new_labels = {**self._labels, **kwargs}
        counter = Counter(self._name, self._description, new_labels)
        counter._value = self._value  # 共享值
        return counter
    
    def reset(self) -> None:
        """重置计数器"""
        with self._lock:
            self._value = 0.0
    
    def snapshot(self) -> MetricSnapshot:
        """获取快照"""
        return MetricSnapshot(
            name=self._name,
            metric_type='counter',
            value=self._value,
            labels=self._labels.copy()
        )
    
    def __repr__(self) -> str:
        return f"Counter({self._name}={self._value})"


# ============================================================================
# Gauge - 仪表盘
# ============================================================================

class Gauge:
    """
    仪表盘 - 可增可减的瞬时值
    
    用于记录可增可减的值，如温度、内存使用、并发数等。
    
    示例:
        gauge = Gauge('memory_usage_bytes', 'Current memory usage')
        gauge.set(1024)
        gauge.inc(100)
        gauge.dec(50)
        gauge.with_labels(host='server1').set(2048)
    """
    
    def __init__(self, name: str, description: str = "",
                 labels: Optional[Dict[str, str]] = None):
        """
        初始化仪表盘
        
        Args:
            name: 指标名称
            description: 指标描述
            labels: 标签键值对
        """
        self._name = name
        self._description = description
        self._value = 0.0
        self._labels = labels or {}
        self._lock = threading.Lock()
        self._history: List[MetricPoint] = []
        self._max_history = 1000  # 最大历史记录数
    
    @property
    def name(self) -> str:
        return self._name
    
    @property
    def description(self) -> str:
        return self._description
    
    @property
    def value(self) -> float:
        with self._lock:
            return self._value
    
    @property
    def labels(self) -> Dict[str, str]:
        return self._labels.copy()
    
    def set(self, value: float) -> 'Gauge':
        """
        设置值
        
        Args:
            value: 要设置的值
            
        Returns:
            self，支持链式调用
        """
        with self._lock:
            self._value = value
            self._record_history(value)
        
        return self
    
    def inc(self, amount: float = 1.0) -> 'Gauge':
        """
        增加值
        
        Args:
            amount: 增加的值
            
        Returns:
            self，支持链式调用
        """
        with self._lock:
            self._value += amount
            self._record_history(self._value)
        
        return self
    
    def dec(self, amount: float = 1.0) -> 'Gauge':
        """
        减少值
        
        Args:
            amount: 减少的值
            
        Returns:
            self，支持链式调用
        """
        with self._lock:
            self._value -= amount
            self._record_history(self._value)
        
        return self
    
    def set_to_current_time(self) -> 'Gauge':
        """设置为当前 Unix 时间戳"""
        return self.set(time.time())
    
    def track_inprogress(self) -> 'GaugeContext':
        """
        跟踪进行中的操作数量
        
        使用 with 语句自动增减：
            with gauge.track_inprogress():
                do_something()
        """
        return GaugeContext(self)
    
    def time(self) -> 'GaugeTimer':
        """
        计时装饰器/上下文管理器
        
        记录执行时间：
            with gauge.time():
                do_something()
        """
        return GaugeTimer(self)
    
    def with_labels(self, **kwargs: str) -> 'Gauge':
        """创建带标签的仪表盘实例"""
        new_labels = {**self._labels, **kwargs}
        gauge = Gauge(self._name, self._description, new_labels)
        gauge._value = self._value
        gauge._history = self._history
        return gauge
    
    def _record_history(self, value: float) -> None:
        """记录历史"""
        self._history.append(MetricPoint(
            value=value,
            timestamp=time.time(),
            labels=self._labels.copy()
        ))
        if len(self._history) > self._max_history:
            self._history = self._history[-self._max_history:]
    
    def get_history(self, since: Optional[float] = None) -> List[MetricPoint]:
        """
        获取历史记录
        
        Args:
            since: 起始时间戳（Unix），None 表示全部
            
        Returns:
            历史记录列表
        """
        with self._lock:
            if since is None:
                return self._history.copy()
            return [p for p in self._history if p.timestamp >= since]
    
    def reset(self) -> None:
        """重置仪表盘"""
        with self._lock:
            self._value = 0.0
            self._history.clear()
    
    def snapshot(self) -> MetricSnapshot:
        """获取快照"""
        return MetricSnapshot(
            name=self._name,
            metric_type='gauge',
            value=self._value,
            labels=self._labels.copy()
        )
    
    def __repr__(self) -> str:
        return f"Gauge({self._name}={self._value})"


class GaugeContext:
    """Gauge 的上下文管理器，用于跟踪进行中的操作"""
    
    def __init__(self, gauge: Gauge):
        self.gauge = gauge
    
    def __enter__(self):
        self.gauge.inc()
        return self
    
    def __exit__(self, *args):
        self.gauge.dec()
        return False


class GaugeTimer:
    """Gauge 的计时器"""
    
    def __init__(self, gauge: Gauge):
        self.gauge = gauge
        self._start_time = None
    
    def __enter__(self):
        self._start_time = time.time()
        return self
    
    def __exit__(self, *args):
        if self._start_time:
            elapsed = time.time() - self._start_time
            self.gauge.set(elapsed)
        return False


# ============================================================================
# Histogram - 直方图
# ============================================================================

class Histogram:
    """
    直方图 - 观测值的分布统计
    
    将观测值分配到预定义的桶中，用于计算分位数。
    
    示例:
        hist = Histogram('request_duration_seconds', 
                        'Request duration',
                        buckets=[0.1, 0.5, 1.0, 2.0, 5.0])
        hist.observe(0.42)
        hist.observe(1.23)
        hist.with_labels(method='GET').observe(0.5)
    """
    
    # 默认桶边界
    DEFAULT_BUCKETS = (0.005, 0.01, 0.025, 0.05, 0.075, 0.1, 0.25, 0.5,
                      0.75, 1.0, 2.5, 5.0, 7.5, 10.0, float('inf'))
    
    def __init__(self, name: str, description: str = "",
                 buckets: Optional[List[float]] = None,
                 labels: Optional[Dict[str, str]] = None):
        """
        初始化直方图
        
        Args:
            name: 指标名称
            description: 指标描述
            buckets: 桶边界列表（必须升序，最后一个应为 inf）
            labels: 标签键值对
        """
        self._name = name
        self._description = description
        self._labels = labels or {}
        
        # 设置桶
        if buckets is None:
            self._buckets = list(self.DEFAULT_BUCKETS)
        else:
            self._buckets = sorted(buckets)
            if self._buckets[-1] != float('inf'):
                self._buckets.append(float('inf'))
        
        # 初始化统计
        self._counts = [0] * len(self._buckets)
        self._sum = 0.0
        self._count = 0
        self._observations: List[float] = []
        self._max_observations = 10000  # 最大观测数（用于精确分位数计算）
        
        self._lock = threading.Lock()
    
    @property
    def name(self) -> str:
        return self._name
    
    @property
    def description(self) -> str:
        return self._description
    
    @property
    def labels(self) -> Dict[str, str]:
        return self._labels.copy()
    
    def observe(self, value: float) -> 'Histogram':
        """
        记录观测值
        
        Args:
            value: 观测值
            
        Returns:
            self，支持链式调用
        """
        with self._lock:
            self._sum += value
            self._count += 1
            
            # 更新桶计数（累积计数：每个桶包含所有 <= 边界的观测值）
            for i, boundary in enumerate(self._buckets):
                if value <= boundary:
                    self._counts[i] += 1
            
            # 记录观测值（用于精确分位数计算）
            self._observations.append(value)
            if len(self._observations) > self._max_observations:
                self._observations = self._observations[-self._max_observations:]
        
        return self
    
    def time(self) -> 'HistogramTimer':
        """
        计时装饰器/上下文管理器
        
        记录执行时间：
            with hist.time():
                do_something()
        """
        return HistogramTimer(self)
    
    def with_labels(self, **kwargs: str) -> 'Histogram':
        """创建带标签的直方图实例"""
        new_labels = {**self._labels, **kwargs}
        hist = Histogram(self._name, self._description, self._buckets.copy(), new_labels)
        # 注意：标签实例独立统计
        return hist
    
    def get_count(self) -> int:
        """获取观测次数"""
        with self._lock:
            return self._count
    
    def get_sum(self) -> float:
        """获取观测值总和"""
        with self._lock:
            return self._sum
    
    def get_mean(self) -> float:
        """获取平均值"""
        with self._lock:
            if self._count == 0:
                return 0.0
            return self._sum / self._count
    
    def get_bucket_counts(self) -> Dict[str, int]:
        """获取各桶计数"""
        with self._lock:
            return {
                f'le_{b}' if b != float('inf') else 'le_inf': c
                for b, c in zip(self._buckets, self._counts)
            }
    
    def get_quantile(self, q: float) -> float:
        """
        获取分位数
        
        Args:
            q: 分位数（0-1）
            
        Returns:
            分位数值
        """
        if not 0 <= q <= 1:
            raise ValueError("Quantile must be between 0 and 1")
        
        with self._lock:
            if not self._observations:
                return 0.0
            
            # 精确分位数计算（Nearest rank method）
            sorted_obs = sorted(self._observations)
            n = len(sorted_obs)
            
            if q == 0:
                return sorted_obs[0]
            if q == 1:
                return sorted_obs[-1]
            
            # Nearest rank: ceil(n * q) - 1 (索引从0开始)
            idx = max(0, min(int(math.ceil(n * q)) - 1, n - 1))
            return sorted_obs[idx]
    
    def get_percentiles(self, percentiles: List[float] = None) -> Dict[str, float]:
        """
        获取多个百分位数
        
        Args:
            percentiles: 百分位列表（如 [50, 90, 95, 99]）
            
        Returns:
            百分位字典
        """
        if percentiles is None:
            percentiles = [50, 90, 95, 99]
        
        return {
            f'p{p}': self.get_quantile(p / 100)
            for p in percentiles
        }
    
    def reset(self) -> None:
        """重置直方图"""
        with self._lock:
            self._counts = [0] * len(self._buckets)
            self._sum = 0.0
            self._count = 0
            self._observations.clear()
    
    def snapshot(self) -> MetricSnapshot:
        """获取快照"""
        with self._lock:
            return MetricSnapshot(
                name=self._name,
                metric_type='histogram',
                value=self._sum / self._count if self._count > 0 else 0.0,
                labels=self._labels.copy(),
                count=self._count,
                sum_value=self._sum,
                buckets=self.get_bucket_counts()
            )
    
    def __repr__(self) -> str:
        return f"Histogram({self._name}, count={self._count}, mean={self.get_mean():.3f})"


class HistogramTimer:
    """Histogram 的计时器"""
    
    def __init__(self, histogram: Histogram):
        self.histogram = histogram
        self._start_time = None
    
    def __enter__(self):
        self._start_time = time.time()
        return self
    
    def __exit__(self, *args):
        if self._start_time:
            elapsed = time.time() - self._start_time
            self.histogram.observe(elapsed)
        return False


# ============================================================================
# Summary - 摘要
# ============================================================================

class Summary:
    """
    摘要 - 流式分位数计算
    
    类似 Histogram，但支持可配置的分位数和滑动时间窗口。
    
    示例:
        summary = Summary('request_duration_seconds',
                         'Request duration',
                         quantiles=[0.5, 0.9, 0.95, 0.99])
        summary.observe(0.42)
        summary.with_labels(method='GET').observe(0.5)
    """
    
    def __init__(self, name: str, description: str = "",
                 quantiles: Optional[List[float]] = None,
                 max_age: Optional[float] = None,
                 age_buckets: int = 5,
                 labels: Optional[Dict[str, str]] = None):
        """
        初始化摘要
        
        Args:
            name: 指标名称
            description: 指标描述
            quantiles: 要计算的分位数（默认 [0.5, 0.9, 0.95, 0.99]）
            max_age: 观测值的最大年龄（秒），None 表示不过期
            age_buckets: 时间窗口桶数
            labels: 标签键值对
        """
        self._name = name
        self._description = description
        self._labels = labels or {}
        self._quantiles = quantiles or [0.5, 0.9, 0.95, 0.99]
        self._max_age = max_age
        self._age_buckets = age_buckets
        
        self._sum = 0.0
        self._count = 0
        self._observations: List[tuple] = []  # (timestamp, value)
        self._max_observations = 10000
        
        self._lock = threading.Lock()
    
    @property
    def name(self) -> str:
        return self._name
    
    @property
    def description(self) -> str:
        return self._description
    
    @property
    def labels(self) -> Dict[str, str]:
        return self._labels.copy()
    
    def observe(self, value: float) -> 'Summary':
        """
        记录观测值
        
        Args:
            value: 观测值
            
        Returns:
            self，支持链式调用
        """
        with self._lock:
            now = time.time()
            self._sum += value
            self._count += 1
            
            self._observations.append((now, value))
            if len(self._observations) > self._max_observations:
                self._observations = self._observations[-self._max_observations:]
            
            # 清理过期观测值
            if self._max_age:
                cutoff = now - self._max_age
                self._observations = [
                    (ts, v) for ts, v in self._observations
                    if ts >= cutoff
                ]
        
        return self
    
    def time(self) -> 'SummaryTimer':
        """计时装饰器/上下文管理器"""
        return SummaryTimer(self)
    
    def with_labels(self, **kwargs: str) -> 'Summary':
        """创建带标签的摘要实例"""
        new_labels = {**self._labels, **kwargs}
        return Summary(
            self._name, self._description, self._quantiles,
            self._max_age, self._age_buckets, new_labels
        )
    
    def get_count(self) -> int:
        """获取观测次数"""
        with self._lock:
            return self._count
    
    def get_sum(self) -> float:
        """获取观测值总和"""
        with self._lock:
            return self._sum
    
    def get_mean(self) -> float:
        """获取平均值"""
        with self._lock:
            if self._count == 0:
                return 0.0
            return self._sum / self._count
    
    def get_quantile(self, q: float) -> float:
        """
        获取分位数
        
        Args:
            q: 分位数（0-1）
            
        Returns:
            分位数值
        """
        if not 0 <= q <= 1:
            raise ValueError("Quantile must be between 0 and 1")
        
        with self._lock:
            if not self._observations:
                return 0.0
            
            values = [v for _, v in self._observations]
            sorted_values = sorted(values)
            n = len(sorted_values)
            idx = int(n * q)
            idx = min(idx, n - 1)
            return sorted_values[idx]
    
    def get_quantiles(self) -> Dict[float, float]:
        """获取所有配置的分位数"""
        return {q: self.get_quantile(q) for q in self._quantiles}
    
    def reset(self) -> None:
        """重置摘要"""
        with self._lock:
            self._sum = 0.0
            self._count = 0
            self._observations.clear()
    
    def snapshot(self) -> MetricSnapshot:
        """获取快照"""
        with self._lock:
            return MetricSnapshot(
                name=self._name,
                metric_type='summary',
                value=self._sum / self._count if self._count > 0 else 0.0,
                labels=self._labels.copy(),
                count=self._count,
                sum_value=self._sum,
                quantiles=self.get_quantiles()
            )
    
    def __repr__(self) -> str:
        return f"Summary({self._name}, count={self._count}, mean={self.get_mean():.3f})"


class SummaryTimer:
    """Summary 的计时器"""
    
    def __init__(self, summary: Summary):
        self.summary = summary
        self._start_time = None
    
    def __enter__(self):
        self._start_time = time.time()
        return self
    
    def __exit__(self, *args):
        if self._start_time:
            elapsed = time.time() - self._start_time
            self.summary.observe(elapsed)
        return False


# ============================================================================
# Meter - 计量器（速率测量）
# ============================================================================

class Meter:
    """
    计量器 - 测量事件发生的速率
    
    用于测量 QPS、TPS 等速率指标。
    
    示例:
        meter = Meter('requests_per_second', 'Request rate')
        meter.mark()  # 记录一次事件
        meter.mark(5)  # 记录 5 次事件
        print(meter.get_rate())  # 获取当前速率
    """
    
    def __init__(self, name: str, description: str = "",
                 window_size: float = 60.0,
                 labels: Optional[Dict[str, str]] = None):
        """
        初始化计量器
        
        Args:
            name: 指标名称
            description: 指标描述
            window_size: 时间窗口大小（秒）
            labels: 标签键值对
        """
        self._name = name
        self._description = description
        self._window_size = window_size
        self._labels = labels or {}
        
        self._events: List[float] = []  # 时间戳列表
        self._total = 0
        self._lock = threading.Lock()
    
    @property
    def name(self) -> str:
        return self._name
    
    @property
    def description(self) -> str:
        return self._description
    
    @property
    def labels(self) -> Dict[str, str]:
        return self._labels.copy()
    
    def mark(self, count: int = 1) -> 'Meter':
        """
        记录事件
        
        Args:
            count: 事件次数
            
        Returns:
            self，支持链式调用
        """
        now = time.time()
        
        with self._lock:
            for _ in range(count):
                self._events.append(now)
            self._total += count
            
            # 清理过期事件
            cutoff = now - self._window_size
            self._events = [e for e in self._events if e >= cutoff]
        
        return self
    
    def get_rate(self) -> float:
        """
        获取当前速率（事件/秒）
        
        Returns:
            当前速率
        """
        now = time.time()
        
        with self._lock:
            # 清理过期事件
            cutoff = now - self._window_size
            self._events = [e for e in self._events if e >= cutoff]
            
            if not self._events:
                return 0.0
            
            # 计算速率
            duration = now - self._events[0]
            if duration <= 0:
                return float(len(self._events))
            
            return len(self._events) / duration
    
    def get_count(self) -> int:
        """获取总事件数"""
        with self._lock:
            return self._total
    
    def get_window_count(self) -> int:
        """获取时间窗口内的事件数"""
        now = time.time()
        
        with self._lock:
            cutoff = now - self._window_size
            self._events = [e for e in self._events if e >= cutoff]
            return len(self._events)
    
    def with_labels(self, **kwargs: str) -> 'Meter':
        """创建带标签的计量器实例"""
        new_labels = {**self._labels, **kwargs}
        meter = Meter(self._name, self._description, self._window_size, new_labels)
        meter._total = self._total
        meter._events = self._events.copy()
        return meter
    
    def reset(self) -> None:
        """重置计量器"""
        with self._lock:
            self._events.clear()
            self._total = 0
    
    def snapshot(self) -> MetricSnapshot:
        """获取快照"""
        return MetricSnapshot(
            name=self._name,
            metric_type='meter',
            value=self.get_rate(),
            labels=self._labels.copy(),
            count=self._total
        )
    
    def __repr__(self) -> str:
        return f"Meter({self._name}, rate={self.get_rate():.2f}/s)"


# ============================================================================
# MetricsRegistry - 指标注册表
# ============================================================================

class MetricsRegistry:
    """
    指标注册表 - 管理所有指标
    
    集中管理和导出所有指标。
    
    示例:
        registry = MetricsRegistry()
        
        # 注册指标
        counter = registry.counter('requests_total', 'Total requests')
        gauge = registry.gauge('memory_usage', 'Memory usage')
        hist = registry.histogram('latency_seconds', 'Request latency')
        
        # 导出指标
        print(registry.export_prometheus())
    """
    
    def __init__(self, namespace: str = "", subsystem: str = ""):
        """
        初始化注册表
        
        Args:
            namespace: 命名空间（前缀）
            subsystem: 子系统（前缀）
        """
        self._namespace = namespace
        self._subsystem = subsystem
        self._metrics: Dict[str, Any] = {}
        self._lock = threading.Lock()
    
    def _make_name(self, name: str) -> str:
        """生成完整指标名"""
        parts = [p for p in [self._namespace, self._subsystem, name] if p]
        return '_'.join(parts)
    
    def counter(self, name: str, description: str = "",
                labels: Optional[Dict[str, str]] = None) -> Counter:
        """
        注册计数器
        
        Args:
            name: 指标名称
            description: 描述
            labels: 标签
            
        Returns:
            Counter 实例
        """
        full_name = self._make_name(name)
        
        with self._lock:
            if full_name in self._metrics:
                return self._metrics[full_name]
            
            counter = Counter(full_name, description, labels)
            self._metrics[full_name] = counter
            return counter
    
    def gauge(self, name: str, description: str = "",
              labels: Optional[Dict[str, str]] = None) -> Gauge:
        """注册仪表盘"""
        full_name = self._make_name(name)
        
        with self._lock:
            if full_name in self._metrics:
                return self._metrics[full_name]
            
            gauge = Gauge(full_name, description, labels)
            self._metrics[full_name] = gauge
            return gauge
    
    def histogram(self, name: str, description: str = "",
                  buckets: Optional[List[float]] = None,
                  labels: Optional[Dict[str, str]] = None) -> Histogram:
        """注册直方图"""
        full_name = self._make_name(name)
        
        with self._lock:
            if full_name in self._metrics:
                return self._metrics[full_name]
            
            hist = Histogram(full_name, description, buckets, labels)
            self._metrics[full_name] = hist
            return hist
    
    def summary(self, name: str, description: str = "",
                quantiles: Optional[List[float]] = None,
                labels: Optional[Dict[str, str]] = None) -> Summary:
        """注册摘要"""
        full_name = self._make_name(name)
        
        with self._lock:
            if full_name in self._metrics:
                return self._metrics[full_name]
            
            summary = Summary(full_name, description, quantiles, labels=labels)
            self._metrics[full_name] = summary
            return summary
    
    def meter(self, name: str, description: str = "",
              window_size: float = 60.0,
              labels: Optional[Dict[str, str]] = None) -> Meter:
        """注册计量器"""
        full_name = self._make_name(name)
        
        with self._lock:
            if full_name in self._metrics:
                return self._metrics[full_name]
            
            meter = Meter(full_name, description, window_size, labels)
            self._metrics[full_name] = meter
            return meter
    
    def get_metric(self, name: str) -> Optional[Any]:
        """获取指标"""
        full_name = self._make_name(name)
        return self._metrics.get(full_name)
    
    def get_all_metrics(self) -> Dict[str, Any]:
        """获取所有指标"""
        return self._metrics.copy()
    
    def get_all_snapshots(self) -> List[MetricSnapshot]:
        """获取所有指标快照"""
        return [m.snapshot() for m in self._metrics.values()]
    
    def export_prometheus(self) -> str:
        """
        导出为 Prometheus 格式
        
        Returns:
            Prometheus 文本格式的指标数据
        """
        lines = []
        
        for name, metric in self._metrics.items():
            snapshot = metric.snapshot()
            
            # 添加帮助和类型
            if metric.description:
                lines.append(f"# HELP {name} {metric.description}")
            
            metric_type = snapshot.metric_type
            if metric_type == 'meter':
                metric_type = 'gauge'  # Prometheus 没有 meter 类型
            
            lines.append(f"# TYPE {name} {metric_type}")
            
            # 添加指标值
            labels_str = ""
            if snapshot.labels:
                labels_str = "{" + ", ".join(
                    f'{k}="{v}"' for k, v in snapshot.labels.items()
                ) + "}"
            
            if metric_type == 'histogram':
                # 直方图格式
                lines.append(f"{name}_count{labels_str} {snapshot.count}")
                lines.append(f"{name}_sum{labels_str} {snapshot.sum_value}")
                
                # 桶
                cumsum = 0
                for bucket, count in snapshot.buckets.items():
                    cumsum += count
                    bucket_val = bucket.replace('le_', '')
                    lines.append(f'{name}_bucket{labels_str.rstrip("}") if labels_str else ""}{{le="{bucket_val}"}} {cumsum}')
            
            elif metric_type == 'summary':
                # 摘要格式
                lines.append(f"{name}_count{labels_str} {snapshot.count}")
                lines.append(f"{name}_sum{labels_str} {snapshot.sum_value}")
                
                # 分位数
                for q, v in snapshot.quantiles.items():
                    lines.append(f'{name}{labels_str.rstrip("}") if labels_str else ""}{{quantile="{q}"}} {v}')
            
            else:
                # Counter/Gauge/Meter
                lines.append(f"{name}{labels_str} {snapshot.value}")
            
            lines.append("")  # 空行分隔
        
        return "\n".join(lines)
    
    def export_json(self) -> Dict[str, Any]:
        """
        导出为 JSON 格式
        
        Returns:
            JSON 格式的指标数据
        """
        return {
            'timestamp': time.time(),
            'metrics': {
                name: {
                    'type': metric.snapshot().metric_type,
                    'value': metric.snapshot().value,
                    'labels': metric.snapshot().labels,
                    'count': metric.snapshot().count,
                    'sum': metric.snapshot().sum_value,
                    'buckets': metric.snapshot().buckets,
                    'quantiles': metric.snapshot().quantiles,
                }
                for name, metric in self._metrics.items()
            }
        }
    
    def reset_all(self) -> None:
        """重置所有指标"""
        for metric in self._metrics.values():
            if hasattr(metric, 'reset'):
                metric.reset()
    
    def __repr__(self) -> str:
        return f"MetricsRegistry(metrics={len(self._metrics)})"


# ============================================================================
# 全局默认注册表
# ============================================================================

_default_registry: Optional[MetricsRegistry] = None
_registry_lock = threading.Lock()


def get_default_registry() -> MetricsRegistry:
    """获取全局默认注册表"""
    global _default_registry
    
    with _registry_lock:
        if _default_registry is None:
            _default_registry = MetricsRegistry()
        return _default_registry


def set_default_registry(registry: MetricsRegistry) -> None:
    """设置全局默认注册表"""
    global _default_registry
    
    with _registry_lock:
        _default_registry = registry


# ============================================================================
# 便捷函数
# ============================================================================

def counter(name: str, description: str = "",
            labels: Optional[Dict[str, str]] = None) -> Counter:
    """在默认注册表中注册计数器"""
    return get_default_registry().counter(name, description, labels)


def gauge(name: str, description: str = "",
          labels: Optional[Dict[str, str]] = None) -> Gauge:
    """在默认注册表中注册仪表盘"""
    return get_default_registry().gauge(name, description, labels)


def histogram(name: str, description: str = "",
              buckets: Optional[List[float]] = None,
              labels: Optional[Dict[str, str]] = None) -> Histogram:
    """在默认注册表中注册直方图"""
    return get_default_registry().histogram(name, description, buckets, labels)


def summary(name: str, description: str = "",
            quantiles: Optional[List[float]] = None,
            labels: Optional[Dict[str, str]] = None) -> Summary:
    """在默认注册表中注册摘要"""
    return get_default_registry().summary(name, description, quantiles, labels)


def meter(name: str, description: str = "",
          window_size: float = 60.0,
          labels: Optional[Dict[str, str]] = None) -> Meter:
    """在默认注册表中注册计量器"""
    return get_default_registry().meter(name, description, window_size, labels)


def export_prometheus() -> str:
    """导出默认注册表的所有指标为 Prometheus 格式"""
    return get_default_registry().export_prometheus()


def export_json() -> Dict[str, Any]:
    """导出默认注册表的所有指标为 JSON 格式"""
    return get_default_registry().export_json()


# ============================================================================
# 模块元数据
# ============================================================================

__version__ = "1.0.0"
__author__ = "AllToolkit"
__all__ = [
    # 数据类
    'MetricPoint',
    'MetricSnapshot',
    
    # 指标类型
    'Counter',
    'Gauge',
    'Histogram',
    'Summary',
    'Meter',
    
    # 上下文管理器
    'GaugeContext',
    'GaugeTimer',
    'HistogramTimer',
    'SummaryTimer',
    
    # 注册表
    'MetricsRegistry',
    
    # 便捷函数
    'counter',
    'gauge',
    'histogram',
    'summary',
    'meter',
    'export_prometheus',
    'export_json',
    'get_default_registry',
    'set_default_registry',
]