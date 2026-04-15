"""
内存监控模块 - Memory Monitor Module

提供内存使用监控、快照和持续监控功能。
"""

import os
import sys
import time
import tracemalloc
from contextlib import contextmanager
from dataclasses import dataclass, field
from typing import Optional, List, Dict, Any, Callable
from functools import wraps


def get_memory_usage() -> Dict[str, float]:
    """
    获取当前进程的内存使用情况
    
    Returns:
        包含内存使用信息的字典 (单位: MB)
        - rss: 常驻内存集大小
        - vms: 虚拟内存大小
        - percent: 内存使用百分比
        - available: 可用内存
        - total: 总内存
    """
    try:
        import psutil
        process = psutil.Process(os.getpid())
        mem_info = process.memory_info()
        vm = psutil.virtual_memory()
        
        return {
            "rss": mem_info.rss / 1024 / 1024,
            "vms": mem_info.vms / 1024 / 1024,
            "percent": process.memory_percent(),
            "available": vm.available / 1024 / 1024,
            "total": vm.total / 1024 / 1024,
        }
    except ImportError:
        # 如果没有 psutil，使用 resource 模块（Unix）
        try:
            import resource
            rusage = resource.getrusage(resource.RUSAGE_SELF)
            return {
                "rss": rusage.ru_maxrss / 1024,  # Linux: KB, macOS: bytes
                "vms": 0,
                "percent": 0,
                "available": 0,
                "total": 0,
            }
        except ImportError:
            return {
                "rss": 0,
                "vms": 0,
                "percent": 0,
                "available": 0,
                "total": 0,
            }


def get_process_memory_info(pid: Optional[int] = None) -> Dict[str, Any]:
    """
    获取指定进程的内存信息
    
    Args:
        pid: 进程ID，默认为当前进程
    
    Returns:
        进程内存信息字典
    """
    pid = pid or os.getpid()
    try:
        import psutil
        process = psutil.Process(pid)
        mem_info = process.memory_info()
        
        return {
            "pid": pid,
            "name": process.name(),
            "rss_mb": mem_info.rss / 1024 / 1024,
            "vms_mb": mem_info.vms / 1024 / 1024,
            "percent": process.memory_percent(),
            "num_threads": process.num_threads(),
            "num_handles": getattr(process, "num_handles", lambda: 0)(),
            "create_time": process.create_time(),
        }
    except ImportError:
        return {
            "pid": pid,
            "name": "unknown",
            "rss_mb": 0,
            "vms_mb": 0,
            "percent": 0,
            "num_threads": 0,
            "num_handles": 0,
            "create_time": 0,
        }


@dataclass
class MemorySnapshot:
    """内存快照"""
    timestamp: float
    rss_mb: float
    vms_mb: float
    percent: float
    traceback_limit: int = 25
    tracemalloc_snapshot: Optional[Any] = None
    gc_objects: int = 0
    gc_collections: tuple = field(default_factory=tuple)
    
    def __post_init__(self):
        if not self.gc_collections:
            import gc
            self.gc_collections = tuple(gc.get_count())
    
    @classmethod
    def capture(cls, traceback_limit: int = 25, use_tracemalloc: bool = False) -> "MemorySnapshot":
        """
        捕获当前内存快照
        
        Args:
            traceback_limit: 回溯深度限制
            use_tracemalloc: 是否使用 tracemalloc
        
        Returns:
            MemorySnapshot 实例
        """
        mem = get_memory_usage()
        tracemalloc_snapshot = None
        
        if use_tracemalloc:
            if not tracemalloc.is_tracing():
                tracemalloc.start(traceback_limit)
            tracemalloc_snapshot = tracemalloc.take_snapshot()
        
        import gc
        gc_objects = len(gc.get_objects())
        
        return cls(
            timestamp=time.time(),
            rss_mb=mem["rss"],
            vms_mb=mem["vms"],
            percent=mem["percent"],
            traceback_limit=traceback_limit,
            tracemalloc_snapshot=tracemalloc_snapshot,
            gc_objects=gc_objects,
        )
    
    def diff(self, other: "MemorySnapshot") -> Dict[str, float]:
        """
        计算与另一个快照的差异
        
        Args:
            other: 另一个 MemorySnapshot
        
        Returns:
            差异字典
        """
        return {
            "time_diff_sec": self.timestamp - other.timestamp,
            "rss_diff_mb": self.rss_mb - other.rss_mb,
            "vms_diff_mb": self.vms_mb - other.vms_mb,
            "percent_diff": self.percent - other.percent,
            "gc_objects_diff": self.gc_objects - other.gc_objects,
        }
    
    def get_top_allocations(self, limit: int = 10) -> List[Dict[str, Any]]:
        """
        获取内存分配最多的位置（需要 tracemalloc）
        
        Args:
            limit: 返回数量限制
        
        Returns:
            分配位置列表
        """
        if not self.tracemalloc_snapshot:
            return []
        
        top_stats = self.tracemalloc_snapshot.statistics("lineno")
        result = []
        
        for stat in top_stats[:limit]:
            frame = stat.traceback[0]
            result.append({
                "file": frame.filename,
                "line": frame.lineno,
                "size_kb": stat.size / 1024,
                "count": stat.count,
            })
        
        return result
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            "timestamp": self.timestamp,
            "rss_mb": self.rss_mb,
            "vms_mb": self.vms_mb,
            "percent": self.percent,
            "gc_objects": self.gc_objects,
            "gc_collections": self.gc_collections,
        }


class MemoryMonitor:
    """
    内存监控器
    
    用于持续监控内存使用情况，记录变化并检测异常。
    
    Example:
        monitor = MemoryMonitor()
        monitor.start()
        
        # ... 你的代码 ...
        
        monitor.stop()
        report = monitor.get_report()
    """
    
    def __init__(
        self,
        interval: float = 1.0,
        max_samples: int = 1000,
        threshold_mb: float = 100.0,
        callback: Optional[Callable[[Dict], None]] = None,
    ):
        """
        初始化内存监控器
        
        Args:
            interval: 采样间隔（秒）
            max_samples: 最大样本数
            threshold_mb: 内存警告阈值（MB）
            callback: 超过阈值时的回调函数
        """
        self.interval = interval
        self.max_samples = max_samples
        self.threshold_mb = threshold_mb
        self.callback = callback
        
        self._samples: List[MemorySnapshot] = []
        self._running = False
        self._start_time: Optional[float] = None
    
    def start(self) -> "MemoryMonitor":
        """开始监控"""
        if self._running:
            return self
        
        self._running = True
        self._start_time = time.time()
        self._samples = []
        
        return self
    
    def stop(self) -> "MemoryMonitor":
        """停止监控"""
        self._running = False
        return self
    
    def sample(self) -> MemorySnapshot:
        """采集一个样本"""
        snapshot = MemorySnapshot.capture()
        
        if len(self._samples) >= self.max_samples:
            self._samples.pop(0)
        
        self._samples.append(snapshot)
        
        # 检查阈值
        if snapshot.rss_mb > self.threshold_mb and self.callback:
            self.callback({
                "type": "threshold_exceeded",
                "current_mb": snapshot.rss_mb,
                "threshold_mb": self.threshold_mb,
                "timestamp": snapshot.timestamp,
            })
        
        return snapshot
    
    def get_samples(self) -> List[MemorySnapshot]:
        """获取所有样本"""
        return self._samples.copy()
    
    def get_statistics(self) -> Dict[str, Any]:
        """获取统计信息"""
        if not self._samples:
            return {}
        
        rss_values = [s.rss_mb for s in self._samples]
        vms_values = [s.vms_mb for s in self._samples]
        
        return {
            "count": len(self._samples),
            "duration_sec": self._samples[-1].timestamp - self._samples[0].timestamp if len(self._samples) > 1 else 0,
            "rss": {
                "min": min(rss_values),
                "max": max(rss_values),
                "avg": sum(rss_values) / len(rss_values),
                "last": rss_values[-1],
                "delta": rss_values[-1] - rss_values[0],
            },
            "vms": {
                "min": min(vms_values),
                "max": max(vms_values),
                "avg": sum(vms_values) / len(vms_values),
                "last": vms_values[-1],
                "delta": vms_values[-1] - vms_values[0],
            },
        }
    
    def get_report(self) -> Dict[str, Any]:
        """生成监控报告"""
        return {
            "start_time": self._start_time,
            "end_time": time.time() if not self._running else None,
            "running": self._running,
            "interval": self.interval,
            "threshold_mb": self.threshold_mb,
            "samples_count": len(self._samples),
            "statistics": self.get_statistics(),
        }


@contextmanager
def memory_context(
    label: str = "memory_context",
    threshold_mb: Optional[float] = None,
    callback: Optional[Callable[[Dict], None]] = None,
):
    """
    内存监控上下文管理器
    
    Args:
        label: 标签名称
        threshold_mb: 内存增长警告阈值
        callback: 超过阈值时的回调
    
    Yields:
        MemoryMonitor 实例
    
    Example:
        with memory_context("heavy_operation", threshold_mb=50) as monitor:
            # 执行内存密集操作
            data = [i for i in range(1000000)]
        # 退出时自动生成报告
    """
    monitor = MemoryMonitor(threshold_mb=threshold_mb or float("inf"), callback=callback)
    monitor.start()
    monitor.sample()  # 初始样本
    
    try:
        yield monitor
    finally:
        monitor.sample()  # 最终样本
        monitor.stop()
        
        stats = monitor.get_statistics()
        if stats:
            delta = stats["rss"]["delta"]
            
            report = {
                "label": label,
                "rss_delta_mb": delta,
                "rss_final_mb": stats["rss"]["last"],
                "rss_peak_mb": stats["rss"]["max"],
            }
            
            if threshold_mb and abs(delta) > threshold_mb:
                report["warning"] = f"内存变化 {delta:.2f}MB 超过阈值 {threshold_mb}MB"
                if callback:
                    callback(report)
            
            print(f"[{label}] 内存报告: RSS 变化 {delta:+.2f}MB, 峰值 {stats['rss']['max']:.2f}MB")


def track_memory(func: Callable) -> Callable:
    """
    内存追踪装饰器
    
    装饰函数以追踪其内存使用情况。
    
    Example:
        @track_memory
        def process_large_data():
            return [i for i in range(1000000)]
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        with memory_context(f"func:{func.__name__}"):
            return func(*args, **kwargs)
    return wrapper