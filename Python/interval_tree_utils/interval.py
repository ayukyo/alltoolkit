"""
区间类定义
"""

from typing import Any, Generic, TypeVar, Optional
from dataclasses import dataclass

T = TypeVar('T', int, float)


@dataclass
class Interval(Generic[T]):
    """
    区间类，表示一个闭区间 [start, end]
    
    属性:
        start: 区间起点
        end: 区间终点
        value: 区间关联的值（可选）
    """
    start: T
    end: T
    value: Any = None
    
    def __post_init__(self):
        """验证区间有效性"""
        if self.start > self.end:
            raise ValueError(f"区间起点({self.start})不能大于终点({self.end})")
    
    def overlaps(self, other: 'Interval[T]') -> bool:
        """检查两个区间是否重叠"""
        return self.start <= other.end and other.start <= self.end
    
    def contains(self, other: 'Interval[T]') -> bool:
        """检查当前区间是否完全包含另一个区间"""
        return self.start <= other.start and self.end >= other.end
    
    def contains_point(self, point: T) -> bool:
        """检查区间是否包含指定点"""
        return self.start <= point <= self.end
    
    def intersection(self, other: 'Interval[T]') -> Optional['Interval[T]']:
        """返回两个区间的交集，如果不相交则返回 None"""
        if not self.overlaps(other):
            return None
        return Interval(
            max(self.start, other.start),
            min(self.end, other.end)
        )
    
    def union(self, other: 'Interval[T]') -> Optional['Interval[T]']:
        """
        返回两个区间的并集
        如果区间不相邻或重叠，返回 None
        """
        if not self.overlaps(other) and self.end + 1 != other.start and other.end + 1 != self.start:
            return None
        return Interval(
            min(self.start, other.start),
            max(self.end, other.end)
        )
    
    def __len__(self) -> T:
        """返回区间长度"""
        return self.end - self.start
    
    def __contains__(self, item) -> bool:
        """支持 `x in interval` 语法"""
        if isinstance(item, Interval):
            return self.contains(item)
        return self.contains_point(item)
    
    def __repr__(self) -> str:
        if self.value is not None:
            return f"Interval({self.start}, {self.end}, value={self.value!r})"
        return f"Interval({self.start}, {self.end})"
    
    def __eq__(self, other) -> bool:
        if not isinstance(other, Interval):
            return False
        return self.start == other.start and self.end == other.end and self.value == other.value
    
    def __hash__(self) -> int:
        return hash((self.start, self.end, self.value))
    
    def __lt__(self, other: 'Interval[T]') -> bool:
        """按起点排序"""
        if self.start != other.start:
            return self.start < other.start
        return self.end < other.end
    
    @property
    def length(self) -> T:
        """区间长度"""
        return self.end - self.start
    
    @property
    def center(self) -> float:
        """区间中心点"""
        return (self.start + self.end) / 2.0