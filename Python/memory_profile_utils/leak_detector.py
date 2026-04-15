"""
内存泄漏检测模块 - Memory Leak Detector Module

提供内存泄漏检测、快照对比等功能。
"""

import gc
import sys
import time
import tracemalloc
from typing import Optional, List, Dict, Any, Set, Tuple
from dataclasses import dataclass, field
from collections import defaultdict
from contextlib import contextmanager

from .memory_monitor import MemorySnapshot


@dataclass
class LeakReport:
    """内存泄漏报告"""
    potential_leaks: List[Dict[str, Any]] = field(default_factory=list)
    memory_growth_mb: float = 0.0
    object_growth: int = 0
    duration_sec: float = 0.0
    severity: str = "none"  # none, low, medium, high, critical
    recommendations: List[str] = field(default_factory=list)
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            "potential_leaks": self.potential_leaks,
            "memory_growth_mb": self.memory_growth_mb,
            "object_growth": self.object_growth,
            "duration_sec": self.duration_sec,
            "severity": self.severity,
            "recommendations": self.recommendations,
        }
    
    def __str__(self) -> str:
        """字符串表示"""
        lines = [
            f"=== 内存泄漏报告 ===",
            f"严重程度: {self.severity.upper()}",
            f"内存增长: {self.memory_growth_mb:.2f} MB",
            f"对象增长: {self.object_growth}",
            f"持续时间: {self.duration_sec:.2f} 秒",
            "",
            "潜在泄漏点:",
        ]
        
        for i, leak in enumerate(self.potential_leaks[:5], 1):
            lines.append(f"  {i}. {leak.get('type', 'unknown')}: {leak.get('size_kb', 0):.2f} KB")
            if "file" in leak:
                lines.append(f"     文件: {leak['file']}:{leak.get('line', '?')}")
        
        if self.recommendations:
            lines.append("")
            lines.append("建议:")
            for rec in self.recommendations:
                lines.append(f"  - {rec}")
        
        return "\n".join(lines)


class MemoryLeakDetector:
    """
    内存泄漏检测器
    
    用于检测Python程序中的内存泄漏。
    
    Example:
        detector = MemoryLeakDetector()
        detector.start()
        
        # 执行可能泄漏内存的代码
        for i in range(1000):
            create_objects()
        
        report = detector.stop()
        print(report)
    """
    
    def __init__(
        self,
        threshold_mb: float = 1.0,
        growth_rate_threshold: float = 0.1,
        traceback_limit: int = 25,
    ):
        """
        初始化泄漏检测器
        
        Args:
            threshold_mb: 内存增长阈值（MB）
            growth_rate_threshold: 增长率阈值（百分比）
            traceback_limit: 回溯深度限制
        """
        self.threshold_mb = threshold_mb
        self.growth_rate_threshold = growth_rate_threshold
        self.traceback_limit = traceback_limit
        
        self._start_snapshot: Optional[MemorySnapshot] = None
        self._end_snapshot: Optional[MemorySnapshot] = None
        self._tracemalloc_started_by_us = False
        self._object_history: List[Dict[str, int]] = []
    
    def start(self) -> "MemoryLeakDetector":
        """开始监控"""
        # 启动 tracemalloc
        if not tracemalloc.is_tracing():
            tracemalloc.start(self.traceback_limit)
            self._tracemalloc_started_by_us = True
        
        # 强制垃圾回收
        gc.collect()
        
        # 捕获初始快照
        self._start_snapshot = MemorySnapshot.capture(
            traceback_limit=self.traceback_limit,
            use_tracemalloc=True,
        )
        
        # 记录初始对象
        self._record_objects()
        
        return self
    
    def checkpoint(self) -> Dict[str, Any]:
        """
        创建检查点
        
        Returns:
            检查点信息
        """
        gc.collect()
        snapshot = MemorySnapshot.capture(use_tracemalloc=True)
        self._record_objects()
        
        if self._start_snapshot:
            diff = snapshot.diff(self._start_snapshot)
        else:
            diff = {}
        
        return {
            "timestamp": snapshot.timestamp,
            "rss_mb": snapshot.rss_mb,
            "gc_objects": snapshot.gc_objects,
            "diff_from_start": diff,
        }
    
    def _record_objects(self):
        """记录对象类型统计"""
        type_counts: Dict[str, int] = defaultdict(int)
        for obj in gc.get_objects():
            type_counts[type(obj).__name__] += 1
        self._object_history.append(dict(type_counts))
    
    def stop(self) -> LeakReport:
        """停止监控并生成报告"""
        # 强制垃圾回收
        gc.collect()
        
        # 捕获结束快照
        self._end_snapshot = MemorySnapshot.capture(
            traceback_limit=self.traceback_limit,
            use_tracemalloc=True,
        )
        
        # 如果是我们启动的 tracemalloc，停止它
        if self._tracemalloc_started_by_us:
            tracemalloc.stop()
        
        return self._generate_report()
    
    def _generate_report(self) -> LeakReport:
        """生成泄漏报告"""
        if not self._start_snapshot or not self._end_snapshot:
            return LeakReport(severity="error", recommendations=["无法生成报告：缺少快照"])
        
        # 计算内存增长
        diff = self._end_snapshot.diff(self._start_snapshot)
        memory_growth = diff["rss_diff_mb"]
        
        # 分析内存分配
        potential_leaks = self._analyze_allocations()
        
        # 分析对象增长
        object_growth = self._analyze_object_growth()
        
        # 确定严重程度
        severity = self._determine_severity(memory_growth, len(potential_leaks))
        
        # 生成建议
        recommendations = self._generate_recommendations(
            memory_growth, potential_leaks, object_growth
        )
        
        return LeakReport(
            potential_leaks=potential_leaks,
            memory_growth_mb=memory_growth,
            object_growth=object_growth,
            duration_sec=diff["time_diff_sec"],
            severity=severity,
            recommendations=recommendations,
        )
    
    def _analyze_allocations(self) -> List[Dict[str, Any]]:
        """分析内存分配"""
        if not self._start_snapshot or not self._end_snapshot:
            return []
        
        if not self._start_snapshot.tracemalloc_snapshot:
            return []
        
        if not self._end_snapshot.tracemalloc_snapshot:
            return []
        
        # 比较快照
        stat_diff = self._end_snapshot.tracemalloc_snapshot.compare_to(
            self._start_snapshot.tracemalloc_snapshot,
            "lineno",
        )
        
        potential_leaks = []
        for stat in stat_diff[:20]:
            if stat.size_diff > 1024:  # 只显示增长超过 1KB 的
                frame = stat.traceback[0] if stat.traceback else None
                leak_info = {
                    "size_kb": stat.size_diff / 1024,
                    "count": stat.count_diff,
                    "type": "memory_allocation",
                }
                if frame:
                    leak_info["file"] = frame.filename
                    leak_info["line"] = frame.lineno
                potential_leaks.append(leak_info)
        
        return potential_leaks
    
    def _analyze_object_growth(self) -> int:
        """分析对象增长"""
        if len(self._object_history) < 2:
            return 0
        
        first = self._object_history[0]
        last = self._object_history[-1]
        
        total_growth = 0
        for obj_type, count in last.items():
            initial_count = first.get(obj_type, 0)
            if count > initial_count:
                total_growth += count - initial_count
        
        return total_growth
    
    def _determine_severity(self, memory_growth: float, leak_count: int) -> str:
        """确定严重程度"""
        if memory_growth < 0:
            return "none"
        
        if memory_growth < self.threshold_mb and leak_count < 3:
            return "low"
        
        if memory_growth < self.threshold_mb * 5 and leak_count < 10:
            return "medium"
        
        if memory_growth < self.threshold_mb * 20:
            return "high"
        
        return "critical"
    
    def _generate_recommendations(
        self,
        memory_growth: float,
        potential_leaks: List[Dict],
        object_growth: int,
    ) -> List[str]:
        """生成建议"""
        recommendations = []
        
        if memory_growth > self.threshold_mb:
            recommendations.append(
                f"内存增长 {memory_growth:.2f}MB 超过阈值，检查是否正确释放大对象"
            )
        
        if object_growth > 100:
            recommendations.append(
                f"对象数量增长 {object_growth}，可能存在循环引用或缓存未清理"
            )
        
        # 检查常见问题类型
        leak_types = set()
        for leak in potential_leaks:
            if "file" in leak:
                file = leak["file"]
                if "cache" in file.lower():
                    leak_types.add("cache")
                if "callback" in file.lower() or "handler" in file.lower():
                    leak_types.add("callback")
        
        if "cache" in leak_types:
            recommendations.append("缓存对象可能未正确清理，考虑使用 LRU 缓存或设置过期时间")
        
        if "callback" in leak_types:
            recommendations.append("回调或处理器可能持有对象引用，确保在不需要时取消注册")
        
        if not recommendations:
            recommendations.append("未检测到明显的内存泄漏问题")
        
        return recommendations


@contextmanager
def detect_leak(
    threshold_mb: float = 1.0,
    auto_report: bool = True,
):
    """
    内存泄漏检测上下文管理器
    
    Args:
        threshold_mb: 内存增长警告阈值
        auto_report: 是否自动打印报告
    
    Yields:
        MemoryLeakDetector 实例
    
    Example:
        with detect_leak(threshold_mb=5.0) as detector:
            # 执行可能泄漏内存的代码
            for i in range(1000):
                create_objects()
    """
    detector = MemoryLeakDetector(threshold_mb=threshold_mb)
    detector.start()
    
    try:
        yield detector
    finally:
        report = detector.stop()
        if auto_report:
            print(report)


def compare_snapshots(
    snapshot1: MemorySnapshot,
    snapshot2: MemorySnapshot,
) -> Dict[str, Any]:
    """
    比较两个内存快照
    
    Args:
        snapshot1: 第一个快照
        snapshot2: 第二个快照
    
    Returns:
        比较结果字典
    """
    diff = snapshot2.diff(snapshot1)
    
    result = {
        "time_diff_sec": diff["time_diff_sec"],
        "rss_diff_mb": diff["rss_diff_mb"],
        "vms_diff_mb": diff["vms_diff_mb"],
        "percent_diff": diff["percent_diff"],
        "gc_objects_diff": diff["gc_objects_diff"],
        "snapshot1": snapshot1.to_dict(),
        "snapshot2": snapshot2.to_dict(),
    }
    
    # 分析内存分配变化（如果有 tracemalloc 数据）
    if snapshot1.tracemalloc_snapshot and snapshot2.tracemalloc_snapshot:
        stat_diff = snapshot2.tracemalloc_snapshot.compare_to(
            snapshot1.tracemalloc_snapshot, "lineno"
        )
        
        allocations = []
        for stat in stat_diff[:10]:
            frame = stat.traceback[0] if stat.traceback else None
            alloc_info = {
                "size_diff_kb": stat.size_diff / 1024,
                "count_diff": stat.count_diff,
            }
            if frame:
                alloc_info["file"] = frame.filename
                alloc_info["line"] = frame.lineno
            allocations.append(alloc_info)
        
        result["allocation_changes"] = allocations
    
    return result


def find_growing_types(
    iterations: int = 10,
    interval: float = 1.0,
    threshold: int = 100,
) -> List[Dict[str, Any]]:
    """
    查找增长中的对象类型
    
    Args:
        iterations: 迭代次数
        interval: 每次迭代间隔（秒）
        threshold: 增长阈值
    
    Returns:
        增长中的类型列表
    
    Example:
        # 查找增长的对象类型
        growing = find_growing_types(iterations=5, interval=0.5)
        for item in growing:
            print(f"{item['type']}: +{item['growth']}")
    """
    type_counts_history: List[Dict[str, int]] = []
    
    for _ in range(iterations):
        gc.collect()
        
        type_counts: Dict[str, int] = defaultdict(int)
        for obj in gc.get_objects():
            type_counts[type(obj).__name__] += 1
        
        type_counts_history.append(type_counts)
        time.sleep(interval)
    
    # 分析增长趋势
    growing_types = []
    if len(type_counts_history) >= 2:
        first = type_counts_history[0]
        last = type_counts_history[-1]
        
        for obj_type, count in last.items():
            initial = first.get(obj_type, 0)
            growth = count - initial
            
            if growth > threshold:
                growing_types.append({
                    "type": obj_type,
                    "initial": initial,
                    "final": count,
                    "growth": growth,
                    "growth_rate": (growth / initial * 100) if initial > 0 else float("inf"),
                })
    
    # 按增长排序
    growing_types.sort(key=lambda x: x["growth"], reverse=True)
    
    return growing_types