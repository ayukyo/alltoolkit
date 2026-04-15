"""
Memory Profile Utils - 内存分析工具集

功能:
- 内存使用监控和快照
- 对象大小分析
- 内存泄漏检测
- 内存优化辅助工具
- 内存使用报告生成

零外部依赖，仅使用 Python 标准库
"""

from .memory_monitor import (
    get_memory_usage,
    get_process_memory_info,
    MemorySnapshot,
    MemoryMonitor,
    memory_context,
    track_memory,
)

from .object_analyzer import (
    get_object_size,
    get_object_size_deep,
    analyze_object,
    get_referents,
    get_referrers,
    ObjectSizeAnalyzer,
    top_objects_by_size,
)

from .leak_detector import (
    MemoryLeakDetector,
    LeakReport,
    detect_leak,
    compare_snapshots,
    find_growing_types,
)

from .optimizer import (
    MemoryOptimizer,
    optimize_intern,
    optimize_slots,
    get_memory_recommendations,
    clear_caches,
    memory_efficient,
    memory_efficient_class,
)

__version__ = "1.0.0"
__all__ = [
    # Memory Monitor
    "get_memory_usage",
    "get_process_memory_info",
    "MemorySnapshot",
    "MemoryMonitor",
    "memory_context",
    "track_memory",
    # Object Analyzer
    "get_object_size",
    "get_object_size_deep",
    "analyze_object",
    "get_referents",
    "get_referrers",
    "ObjectSizeAnalyzer",
    "top_objects_by_size",
    # Leak Detector
    "MemoryLeakDetector",
    "LeakReport",
    "detect_leak",
    "compare_snapshots",
    "find_growing_types",
    # Optimizer
    "MemoryOptimizer",
    "optimize_intern",
    "optimize_slots",
    "get_memory_recommendations",
    "clear_caches",
    "memory_efficient",
    "memory_efficient_class",
]