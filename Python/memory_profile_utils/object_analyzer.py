"""
对象分析模块 - Object Analyzer Module

提供对象大小分析、引用分析等功能。
"""

import sys
import gc
from typing import Any, Dict, List, Optional, Set, Tuple
from dataclasses import dataclass, field
from collections import defaultdict
from functools import singledispatch


def get_object_size(obj: Any, seen: Optional[Set[int]] = None) -> int:
    """
    获取对象的浅层内存大小
    
    Args:
        obj: 要分析的对象
        seen: 已访问对象ID集合（防止循环引用）
    
    Returns:
        对象大小（字节）
    """
    size = sys.getsizeof(obj)
    
    if seen is None:
        seen = set()
    
    obj_id = id(obj)
    if obj_id in seen:
        return 0
    
    seen.add(obj_id)
    
    # 处理内置容器类型
    if isinstance(obj, dict):
        size += sum(get_object_size(k, seen) + get_object_size(v, seen) for k, v in obj.items())
    elif isinstance(obj, (list, tuple, set, frozenset)):
        size += sum(get_object_size(item, seen) for item in obj)
    elif isinstance(obj, (str, bytes, bytearray)):
        # 这些类型已经包含在 getsizeof 中
        pass
    elif hasattr(obj, "__dict__"):
        size += get_object_size(obj.__dict__, seen)
    elif hasattr(obj, "__slots__"):
        for slot in obj.__slots__:
            if hasattr(obj, slot):
                size += get_object_size(getattr(obj, slot), seen)
    
    return size


def get_object_size_deep(obj: Any, max_depth: int = 10) -> Dict[str, Any]:
    """
    深度分析对象内存大小
    
    Args:
        obj: 要分析的对象
        max_depth: 最大递归深度
    
    Returns:
        详细的分析结果字典
    """
    visited: Dict[int, int] = {}
    
    def analyze(o: Any, depth: int) -> int:
        if depth > max_depth:
            return 0
        
        obj_id = id(o)
        if obj_id in visited:
            return visited[obj_id]
        
        size = sys.getsizeof(o)
        visited[obj_id] = size
        
        if isinstance(o, dict):
            for k, v in o.items():
                size += analyze(k, depth + 1)
                size += analyze(v, depth + 1)
        elif isinstance(o, (list, tuple, set, frozenset)):
            for item in o:
                size += analyze(item, depth + 1)
        elif hasattr(o, "__dict__"):
            size += analyze(o.__dict__, depth + 1)
        elif hasattr(o, "__slots__"):
            for slot in o.__slots__:
                if hasattr(o, slot):
                    size += analyze(getattr(o, slot), depth + 1)
        
        return size
    
    total_size = analyze(obj, 0)
    
    return {
        "total_size_bytes": total_size,
        "total_size_kb": total_size / 1024,
        "total_size_mb": total_size / 1024 / 1024,
        "unique_objects": len(visited),
        "object_type": type(obj).__name__,
        "is_container": isinstance(obj, (dict, list, tuple, set, frozenset)),
    }


@dataclass
class ObjectAnalysis:
    """对象分析结果"""
    object_type: str
    shallow_size: int
    deep_size: int
    reference_count: int
    attributes: Dict[str, int] = field(default_factory=dict)
    container_items: int = 0
    is_circular: bool = False
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            "object_type": self.object_type,
            "shallow_size": self.shallow_size,
            "shallow_size_human": _format_size(self.shallow_size),
            "deep_size": self.deep_size,
            "deep_size_human": _format_size(self.deep_size),
            "reference_count": self.reference_count,
            "attributes_count": len(self.attributes),
            "container_items": self.container_items,
            "is_circular": self.is_circular,
        }


def analyze_object(obj: Any, max_depth: int = 5) -> ObjectAnalysis:
    """
    全面分析对象
    
    Args:
        obj: 要分析的对象
        max_depth: 最大分析深度
    
    Returns:
        ObjectAnalysis 实例
    """
    obj_type = type(obj).__name__
    shallow_size = sys.getsizeof(obj)
    
    # 分析深层大小
    deep_info = get_object_size_deep(obj, max_depth)
    deep_size = deep_info["total_size_bytes"]
    
    # 引用计数（减去我们自己的引用）
    ref_count = sys.getrefcount(obj) - 1
    
    # 分析属性
    attributes = {}
    if hasattr(obj, "__dict__"):
        for attr_name, attr_value in obj.__dict__.items():
            try:
                attributes[attr_name] = get_object_size(attr_value)
            except Exception:
                attributes[attr_name] = 0
    
    # 容器元素计数
    container_items = 0
    if isinstance(obj, dict):
        container_items = len(obj)
    elif isinstance(obj, (list, tuple, set, frozenset)):
        container_items = len(obj)
    
    # 检测循环引用
    is_circular = deep_info["unique_objects"] < len(gc.get_referents(obj))
    
    return ObjectAnalysis(
        object_type=obj_type,
        shallow_size=shallow_size,
        deep_size=deep_size,
        reference_count=ref_count,
        attributes=attributes,
        container_items=container_items,
        is_circular=is_circular,
    )


def get_referents(obj: Any, max_depth: int = 3) -> List[Dict[str, Any]]:
    """
    获取对象引用的所有对象
    
    Args:
        obj: 要分析的对象
        max_depth: 最大递归深度
    
    Returns:
        引用对象列表
    """
    result = []
    visited: Set[int] = set()
    
    def collect(o: Any, depth: int):
        if depth > max_depth:
            return
        
        obj_id = id(o)
        if obj_id in visited:
            return
        visited.add(obj_id)
        
        for ref in gc.get_referents(o):
            ref_id = id(ref)
            if ref_id not in visited:
                result.append({
                    "type": type(ref).__name__,
                    "size": sys.getsizeof(ref),
                    "id": ref_id,
                    "depth": depth,
                })
                collect(ref, depth + 1)
    
    collect(obj, 0)
    return result


def get_referrers(obj: Any) -> List[Dict[str, Any]]:
    """
    获取引用该对象的所有对象
    
    Args:
        obj: 要分析的对象
    
    Returns:
        引用源对象列表
    """
    result = []
    obj_id = id(obj)
    
    for ref in gc.get_referrers(obj):
        ref_type = type(ref).__name__
        
        # 跳过帧对象和追踪对象
        if ref_type in ("frame", "traceback"):
            continue
        
        result.append({
            "type": ref_type,
            "size": sys.getsizeof(ref),
            "id": id(ref),
        })
    
    return result


class ObjectSizeAnalyzer:
    """
    对象大小分析器
    
    用于批量分析多个对象的内存使用情况。
    
    Example:
        analyzer = ObjectSizeAnalyzer()
        analyzer.add("list1", [1, 2, 3, 4, 5])
        analyzer.add("dict1", {"a": 1, "b": 2})
        report = analyzer.get_report()
    """
    
    def __init__(self):
        self._objects: Dict[str, Tuple[Any, ObjectAnalysis]] = {}
    
    def add(self, name: str, obj: Any) -> "ObjectSizeAnalyzer":
        """
        添加对象进行分析
        
        Args:
            name: 对象名称
            obj: 对象实例
        
        Returns:
            self（链式调用）
        """
        analysis = analyze_object(obj)
        self._objects[name] = (obj, analysis)
        return self
    
    def remove(self, name: str) -> "ObjectSizeAnalyzer":
        """移除对象"""
        if name in self._objects:
            del self._objects[name]
        return self
    
    def clear(self) -> "ObjectSizeAnalyzer":
        """清空所有对象"""
        self._objects.clear()
        return self
    
    def get_total_size(self) -> int:
        """获取总大小"""
        return sum(analysis.deep_size for _, analysis in self._objects.values())
    
    def get_report(self) -> Dict[str, Any]:
        """生成分析报告"""
        items = []
        total_size = 0
        
        for name, (obj, analysis) in self._objects.items():
            items.append({
                "name": name,
                "type": analysis.object_type,
                "shallow_size": analysis.shallow_size,
                "deep_size": analysis.deep_size,
                "reference_count": analysis.reference_count,
                "container_items": analysis.container_items,
            })
            total_size += analysis.deep_size
        
        # 按大小排序
        items.sort(key=lambda x: x["deep_size"], reverse=True)
        
        return {
            "total_objects": len(items),
            "total_size_bytes": total_size,
            "total_size_human": _format_size(total_size),
            "items": items,
        }
    
    def find_largest(self, n: int = 5) -> List[Dict[str, Any]]:
        """
        找出最大的对象
        
        Args:
            n: 返回数量
        
        Returns:
            最大的对象列表
        """
        sorted_items = sorted(
            self._objects.items(),
            key=lambda x: x[1][1].deep_size,
            reverse=True,
        )
        
        return [
            {
                "name": name,
                "type": analysis.object_type,
                "size": analysis.deep_size,
                "size_human": _format_size(analysis.deep_size),
            }
            for name, (_, analysis) in sorted_items[:n]
        ]


def top_objects_by_size(objects: List[Any], limit: int = 10) -> List[Dict[str, Any]]:
    """
    从对象列表中找出占用内存最大的对象
    
    Args:
        objects: 对象列表
        limit: 返回数量限制
    
    Returns:
        排序后的对象信息列表
    """
    analyzed = [(obj, get_object_size_deep(obj)) for obj in objects]
    analyzed.sort(key=lambda x: x[1]["total_size_bytes"], reverse=True)
    
    return [
        {
            "index": i,
            "type": info["object_type"],
            "size_bytes": info["total_size_bytes"],
            "size_human": _format_size(info["total_size_bytes"]),
        }
        for i, (obj, info) in enumerate(analyzed[:limit])
    ]


def _format_size(size_bytes: int) -> str:
    """格式化大小为人类可读格式"""
    for unit in ["B", "KB", "MB", "GB", "TB"]:
        if size_bytes < 1024:
            return f"{size_bytes:.2f} {unit}"
        size_bytes /= 1024
    return f"{size_bytes:.2f} PB"