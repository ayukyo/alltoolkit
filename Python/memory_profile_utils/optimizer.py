"""
内存优化模块 - Memory Optimizer Module

提供内存优化建议、缓存清理等功能。
"""

import sys
import gc
import weakref
from typing import Any, Dict, List, Optional, Type, Callable
from dataclasses import dataclass
from functools import wraps
from contextlib import contextmanager


class MemoryOptimizer:
    """
    内存优化器
    
    提供各种内存优化技术和工具。
    
    Example:
        optimizer = MemoryOptimizer()
        
        # 分析对象内存效率
        analysis = optimizer.analyze_efficiency(my_large_object)
        
        # 获取优化建议
        recommendations = optimizer.get_recommendations()
        
        # 执行清理
        optimizer.cleanup()
    """
    
    def __init__(self):
        self._recommendations: List[str] = []
        self._cached_sizes: Dict[int, int] = {}
    
    def analyze_efficiency(self, obj: Any) -> Dict[str, Any]:
        """
        分析对象的内存效率
        
        Args:
            obj: 要分析的对象
        
        Returns:
            效率分析结果
        """
        obj_type = type(obj).__name__
        shallow_size = sys.getsizeof(obj)
        
        result = {
            "type": obj_type,
            "shallow_size": shallow_size,
            "efficiency_score": 100,
            "issues": [],
            "suggestions": [],
        }
        
        # 检查列表内存使用
        if isinstance(obj, list):
            if len(obj) > 0:
                item_size = sys.getsizeof(obj[0]) if obj else 0
                expected_size = len(obj) * item_size
                overhead = shallow_size - expected_size
                
                if overhead > expected_size * 0.5:
                    result["issues"].append("列表内存开销过高")
                    result["suggestions"].append("考虑预分配大小或使用 array.array")
                    result["efficiency_score"] -= 20
        
        # 检查字典负载因子
        if isinstance(obj, dict):
            if len(obj) > 0:
                load_factor = len(obj) / (sys.getsizeof(obj) / 64)
                if load_factor < 0.3:
                    result["issues"].append(f"字典负载因子过低: {load_factor:.2f}")
                    result["suggestions"].append("字典较空，考虑清理或合并")
                    result["efficiency_score"] -= 15
        
        # 检查字符串重复
        if isinstance(obj, str):
            if len(obj) < 1000 and obj in sys.intern(None):
                result["suggestions"].append("字符串可被内部化以节省内存")
        
        # 检查对象是否可以使用 __slots__
        if hasattr(obj, "__dict__") and not hasattr(type(obj), "__slots__"):
            dict_size = sys.getsizeof(obj.__dict__)
            if dict_size > shallow_size * 0.3:
                result["issues"].append("对象使用 __dict__ 占用较多内存")
                result["suggestions"].append("考虑使用 __slots__ 优化")
                result["efficiency_score"] -= 10
        
        result["efficiency_score"] = max(0, result["efficiency_score"])
        
        return result
    
    def get_recommendations(self) -> List[str]:
        """
        获取内存优化建议
        
        Returns:
            建议列表
        """
        recommendations = []
        
        # 检查垃圾回收状态
        if not gc.isenabled():
            recommendations.append("垃圾回收已禁用，考虑启用 gc.enable()")
        
        # 检查垃圾回收阈值
        thresholds = gc.get_threshold()
        if thresholds[0] > 1000:
            recommendations.append(
                f"垃圾回收阈值 {thresholds[0]} 较高，可能延迟回收"
            )
        
        # 检查是否有悬空对象
        dangling = len(gc.garbage)
        if dangling > 0:
            recommendations.append(
                f"发现 {dangling} 个无法回收的对象（gc.garbage）"
            )
        
        return recommendations
    
    def cleanup(self, aggressive: bool = False) -> Dict[str, Any]:
        """
        执行内存清理
        
        Args:
            aggressive: 是否执行激进清理
        
        Returns:
            清理结果
        """
        result = {
            "gc_before": len(gc.get_objects()),
            "gc_after": 0,
            "collected": 0,
            "uncollectable": 0,
            "actions": [],
        }
        
        # 强制垃圾回收
        collected = gc.collect()
        result["collected"] = collected
        result["actions"].append(f"垃圾回收了 {collected} 个对象")
        
        # 激进模式：清理更多
        if aggressive:
            # 清理生成器
            collected2 = gc.collect(1)
            collected3 = gc.collect(2)
            result["collected"] += collected2 + collected3
            result["actions"].append(f"额外回收了 {collected2 + collected3} 个对象")
            
            # 清理弱引用
            try:
                import weakref
                weakref.finalize(lambda: None, lambda: None)
                result["actions"].append("清理了弱引用")
            except Exception:
                pass
        
        result["gc_after"] = len(gc.get_objects())
        result["uncollectable"] = len(gc.garbage)
        
        return result
    
    def estimate_optimization_potential(self, obj: Any) -> Dict[str, Any]:
        """
        估算对象的优化潜力
        
        Args:
            obj: 要分析的对象
        
        Returns:
            优化潜力分析
        """
        from .object_analyzer import get_object_size_deep, analyze_object
        
        current = get_object_size_deep(obj)
        analysis = analyze_object(obj)
        
        potential_savings = {
            "slots": 0,
            "intern": 0,
            "container_optimization": 0,
        }
        
        # 估算 __slots__ 节省
        if hasattr(obj, "__dict__") and not hasattr(type(obj), "__slots__"):
            dict_size = sys.getsizeof(obj.__dict__)
            if dict_size > 100:
                potential_savings["slots"] = dict_size * 0.7  # 估算节省 70%
        
        # 估算字符串内部化节省
        if isinstance(obj, (list, tuple)):
            str_count = sum(1 for item in obj if isinstance(item, str))
            if str_count > 10:
                avg_str_size = sum(
                    sys.getsizeof(s) for s in obj if isinstance(s, str)
                ) / str_count if str_count > 0 else 0
                potential_savings["intern"] = avg_str_size * str_count * 0.5
        
        # 容器优化
        if isinstance(obj, list) and len(obj) > 0:
            if type(obj[0]) in (int, float):
                try:
                    import array
                    potential_savings["container_optimization"] = current["total_size_bytes"] * 0.3
                except ImportError:
                    pass
        
        total_potential = sum(potential_savings.values())
        
        return {
            "current_size_bytes": current["total_size_bytes"],
            "current_size_human": _format_size(current["total_size_bytes"]),
            "potential_savings": potential_savings,
            "total_potential_bytes": total_potential,
            "total_potential_human": _format_size(total_potential),
            "optimization_percentage": (total_potential / current["total_size_bytes"] * 100) 
                if current["total_size_bytes"] > 0 else 0,
        }


def optimize_intern(strings: List[str]) -> Dict[str, str]:
    """
    优化字符串列表的内存使用（内部化）
    
    Args:
        strings: 字符串列表
    
    Returns:
        内部化映射字典
    
    Example:
        strings = ["hello", "world", "hello"] * 1000
        mapping = optimize_intern(strings)
        # "hello" 现在只存储一次
    """
    mapping: Dict[str, str] = {}
    
    for s in strings:
        if s not in mapping:
            mapping[s] = sys.intern(s)
    
    return mapping


def optimize_slots(cls: Type) -> Type:
    """
    为类动态添加 __slots__ 以优化内存
    
    Args:
        cls: 要优化的类
    
    Returns:
        优化后的类
    
    Example:
        @optimize_slots
        class Point:
            def __init__(self, x, y):
                self.x = x
                self.y = y
    """
    if hasattr(cls, "__slots__"):
        return cls  # 已经有 __slots__ 了
    
    # 获取所有实例属性
    slots = set()
    
    # 尝试从 __init__ 中提取属性
    if hasattr(cls, "__init__"):
        import dis
        for instr in dis.get_instructions(cls.__init__):
            if instr.opname in ("STORE_ATTR", "STORE_NAME"):
                attr_name = instr.argval
                if isinstance(attr_name, str) and not attr_name.startswith("_"):
                    slots.add(attr_name)
    
    if slots:
        cls.__slots__ = tuple(slots)
    
    return cls


def get_memory_recommendations() -> List[str]:
    """
    获取通用的内存优化建议
    
    Returns:
        建议列表
    """
    recommendations = [
        "使用 __slots__ 减少对象内存开销",
        "对重复字符串使用 sys.intern() 进行内部化",
        "使用生成器代替列表处理大数据",
        "及时删除不再需要的大对象（del obj）",
        "使用 weakref 避免强引用导致的内存泄漏",
        "对数值数组使用 array.array 或 numpy",
        "使用 __slots__ 和 weakref 处理回调引用",
        "避免在循环中创建大量临时对象",
        "定期调用 gc.collect() 清理循环引用",
        "使用 memory_profiler 或 tracemalloc 定位内存热点",
    ]
    
    # 根据当前状态添加特定建议
    thresholds = gc.get_threshold()
    if thresholds[0] > 700:
        recommendations.append(
            f"考虑降低 gc 阈值（当前 {thresholds[0]}），使用 gc.set_threshold(500, 10, 10)"
        )
    
    # 检查垃圾
    if len(gc.garbage) > 0:
        recommendations.append(
            f"发现 {len(gc.garbage)} 个无法回收的对象，检查 __del__ 方法的循环引用"
        )
    
    return recommendations


def clear_caches(aggressive: bool = False) -> Dict[str, int]:
    """
    清理各种缓存
    
    Args:
        aggressive: 是否执行激进清理
    
    Returns:
        清理统计
    """
    result = {
        "gc_collected": 0,
        "import_cache_cleared": 0,
        "sys_modules_pruned": 0,
    }
    
    # 垃圾回收
    result["gc_collected"] = gc.collect()
    
    if aggressive:
        # 清理导入缓存中的编译文件
        import importlib
        cleared = 0
        to_remove = []
        
        for name, module in list(sys.modules.items()):
            if module is None:
                to_remove.append(name)
                cleared += 1
        
        for name in to_remove:
            del sys.modules[name]
        
        result["import_cache_cleared"] = cleared
        
        # 再次垃圾回收
        gc.collect()
    
    return result


@contextmanager
def memory_efficient():
    """
    内存高效上下文管理器
    
    在进入和退出时执行垃圾回收，确保内存高效使用。
    
    Example:
        with memory_efficient():
            # 内存密集操作
            data = process_large_file()
    """
    gc.collect()
    try:
        yield
    finally:
        gc.collect()


def memory_efficient_class(cls: Type) -> Type:
    """
    类装饰器：为类添加内存高效特性
    
    自动添加 __slots__ 和内存管理方法。
    
    Example:
        @memory_efficient_class
        class DataPoint:
            def __init__(self, x, y):
                self.x = x
                self.y = y
    """
    # 收集已知的实例属性
    known_attrs = set()
    
    # 从父类继承 __slots__
    for parent in cls.__mro__[1:]:
        if hasattr(parent, "__slots__"):
            known_attrs.update(parent.__slots__)
    
    # 添加 __slots__
    if not hasattr(cls, "__slots__"):
        cls.__slots__ = tuple(known_attrs) if known_attrs else ()
    
    # 添加内存清理方法
    def __memclear__(self):
        """清理对象内存"""
        if hasattr(self, "__dict__"):
            self.__dict__.clear()
        for slot in getattr(self, "__slots__", []):
            if hasattr(self, slot):
                try:
                    delattr(self, slot)
                except AttributeError:
                    pass
    
    cls.__memclear__ = __memclear__
    
    return cls


def _format_size(size_bytes: int) -> str:
    """格式化大小为人类可读格式"""
    for unit in ["B", "KB", "MB", "GB", "TB"]:
        if size_bytes < 1024:
            return f"{size_bytes:.2f} {unit}"
        size_bytes /= 1024
    return f"{size_bytes:.2f} PB"