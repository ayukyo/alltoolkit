"""
Span Utils - 区间操作工具库

提供区间（范围）的各种操作，包括合并、交集、差集、分割等。
支持整数区间和浮点数区间，支持开区间和闭区间。

零外部依赖，纯 Python 标准库实现。
"""

from typing import List, Tuple, Optional, Union, Iterable
from dataclasses import dataclass
from enum import Enum


class BoundType(Enum):
    """区间边界类型"""
    OPEN = "open"      # 开区间 (a, b)
    CLOSED = "closed"  # 闭区间 [a, b]
    LEFT_OPEN = "left_open"  # 左开右闭 (a, b]
    RIGHT_OPEN = "right_open"  # 左闭右开 [a, b)


@dataclass
class Span:
    """
    区间类，表示一个数值区间
    
    Attributes:
        start: 区间起始值
        end: 区间结束值
        left_bound: 左边界类型
        right_bound: 右边界类型
    """
    start: float
    end: float
    left_bound: BoundType = BoundType.CLOSED
    right_bound: BoundType = BoundType.CLOSED
    
    def __post_init__(self):
        if self.start > self.end:
            raise ValueError(f"区间起始值 {self.start} 不能大于结束值 {self.end}")
    
    def __repr__(self) -> str:
        left = "(" if self.left_bound == BoundType.OPEN else "["
        right = ")" if self.right_bound == BoundType.OPEN else "]"
        return f"{left}{self.start}, {self.end}{right}"
    
    def __eq__(self, other) -> bool:
        if not isinstance(other, Span):
            return False
        return (self.start == other.start and 
                self.end == other.end and
                self.left_bound == other.left_bound and
                self.right_bound == other.right_bound)
    
    def __hash__(self) -> int:
        return hash((self.start, self.end, self.left_bound, self.right_bound))
    
    def __contains__(self, value: Union[int, float]) -> bool:
        """检查值是否在区间内"""
        left_ok = (value > self.start if self.left_bound == BoundType.OPEN 
                   else value >= self.start)
        right_ok = (value < self.end if self.right_bound == BoundType.OPEN 
                    else value <= self.end)
        return left_ok and right_ok
    
    def length(self) -> float:
        """返回区间长度"""
        return self.end - self.start
    
    def is_empty(self) -> bool:
        """检查是否为空区间"""
        if self.start == self.end:
            return self.left_bound == BoundType.OPEN or self.right_bound == BoundType.OPEN
        return False
    
    def is_point(self) -> bool:
        """检查是否为单点区间（起点等于终点且为闭区间）"""
        return (self.start == self.end and 
                self.left_bound == BoundType.CLOSED and 
                self.right_bound == BoundType.CLOSED)
    
    def overlaps(self, other: 'Span') -> bool:
        """检查两个区间是否重叠"""
        # 完全不重叠的情况
        if self.end < other.start or other.end < self.start:
            return False
        # 边界接触的情况
        if self.end == other.start:
            return (self.right_bound == BoundType.CLOSED and 
                    other.left_bound == BoundType.CLOSED)
        if other.end == self.start:
            return (other.right_bound == BoundType.CLOSED and 
                    self.left_bound == BoundType.CLOSED)
        return True
    
    def intersection(self, other: 'Span') -> Optional['Span']:
        """返回与另一个区间的交集，无交集返回 None"""
        if not self.overlaps(other):
            return None
        
        start = max(self.start, other.start)
        end = min(self.end, other.end)
        
        # 确定边界类型
        if start == self.start:
            left_bound = self.left_bound
        else:
            left_bound = other.left_bound
        
        if start == self.start == other.start:
            left_bound = (BoundType.CLOSED if 
                         self.left_bound == BoundType.CLOSED and 
                         other.left_bound == BoundType.CLOSED 
                         else BoundType.OPEN)
        
        if end == self.end:
            right_bound = self.right_bound
        else:
            right_bound = other.right_bound
        
        if end == self.end == other.end:
            right_bound = (BoundType.CLOSED if 
                          self.right_bound == BoundType.CLOSED and 
                          other.right_bound == BoundType.CLOSED 
                          else BoundType.OPEN)
        
        return Span(start, end, left_bound, right_bound)
    
    def to_tuple(self) -> Tuple[float, float]:
        """转换为元组 (start, end)"""
        return (self.start, self.end)
    
    def clamp(self, value: Union[int, float]) -> float:
        """将值限制在区间内"""
        if value in self:
            return value
        if value < self.start:
            return self.start
        return self.end
    
    def expand(self, amount: float, both_sides: bool = True) -> 'Span':
        """
        扩展区间
        
        Args:
            amount: 扩展量
            both_sides: 是否两边都扩展，False 则只扩展右边界
        
        Returns:
            新的扩展后的区间（闭区间）
        """
        if both_sides:
            return Span(self.start - amount, self.end + amount)
        return Span(self.start, self.end + amount)
    
    def shrink(self, amount: float, both_sides: bool = True) -> Optional['Span']:
        """
        收缩区间
        
        Args:
            amount: 收缩量
            both_sides: 是否两边都收缩
        
        Returns:
            收缩后的区间，如果收缩后无效则返回 None
        """
        if both_sides:
            new_start = self.start + amount
            new_end = self.end - amount
        else:
            new_start = self.start
            new_end = self.end - amount
        
        if new_start > new_end:
            return None
        return Span(new_start, new_end)


# ============== 工具函数 ==============

def span(start: float, end: float, closed: bool = True) -> Span:
    """
    快速创建闭区间或开区间
    
    Args:
        start: 起始值
        end: 结束值
        closed: True 为闭区间 [a, b]，False 为开区间 (a, b)
    
    Returns:
        Span 对象
    """
    bound = BoundType.CLOSED if closed else BoundType.OPEN
    return Span(start, end, bound, bound)


def closed_span(start: float, end: float) -> Span:
    """创建闭区间 [a, b]"""
    return Span(start, end, BoundType.CLOSED, BoundType.CLOSED)


def open_span(start: float, end: float) -> Span:
    """创建开区间 (a, b)"""
    return Span(start, end, BoundType.OPEN, BoundType.OPEN)


def point_span(value: float) -> Span:
    """创建单点区间 [a, a]"""
    return Span(value, value, BoundType.CLOSED, BoundType.CLOSED)


def merge_spans(spans: Iterable[Span]) -> List[Span]:
    """
    合并重叠的区间
    
    Args:
        spans: 区间列表
    
    Returns:
        合并后的不重叠区间列表（闭区间）
    """
    spans_list = list(spans)
    if not spans_list:
        return []
    
    # 按起始值排序
    sorted_spans = sorted(spans_list, key=lambda s: s.start)
    
    result = []
    current = sorted_spans[0]
    
    for next_span in sorted_spans[1:]:
        # 检查是否重叠或相邻（闭区间情况下）
        if (next_span.start < current.end or 
            (next_span.start == current.end and 
             current.right_bound == BoundType.CLOSED and 
             next_span.left_bound == BoundType.CLOSED)):
            # 合并
            if next_span.end > current.end:
                current = Span(current.start, next_span.end)
            elif next_span.end == current.end:
                # 保持更宽的边界
                right = (BoundType.CLOSED if 
                        current.right_bound == BoundType.CLOSED or 
                        next_span.right_bound == BoundType.CLOSED 
                        else BoundType.OPEN)
                current = Span(current.start, current.end, current.left_bound, right)
        else:
            result.append(current)
            current = next_span
    
    result.append(current)
    return result


def intersection_of(spans: Iterable[Span]) -> Optional[Span]:
    """
    计算多个区间的交集
    
    Args:
        spans: 区间列表
    
    Returns:
        所有区间的交集，无交集返回 None
    """
    spans_list = list(spans)
    if not spans_list:
        return None
    
    result = spans_list[0]
    for s in spans_list[1:]:
        result = result.intersection(s)
        if result is None:
            return None
    return result


def subtract_span(source: Span, subtractor: Span) -> List[Span]:
    """
    从源区间中减去另一个区间
    
    Args:
        source: 源区间
        subtractor: 要减去的区间
    
    Returns:
        减去后的区间列表（可能有 0、1 或 2 个区间）
    """
    if not source.overlaps(subtractor):
        return [source]
    
    intersection = source.intersection(subtractor)
    if intersection is None:
        return [source]
    
    # 判断是否完全包含
    if (intersection.start <= source.start and 
        intersection.end >= source.end):
        return []  # 完全被减去
    
    result = []
    
    # 左边剩余部分
    if intersection.start > source.start:
        left_span = Span(
            source.start, intersection.start,
            source.left_bound,
            BoundType.OPEN if intersection.left_bound == BoundType.CLOSED 
            else BoundType.CLOSED
        )
        result.append(left_span)
    
    # 右边剩余部分
    if intersection.end < source.end:
        right_span = Span(
            intersection.end, source.end,
            BoundType.OPEN if intersection.right_bound == BoundType.CLOSED 
            else BoundType.CLOSED,
            source.right_bound
        )
        result.append(right_span)
    
    return result


def subtract_spans(source: Span, subtractors: Iterable[Span]) -> List[Span]:
    """
    从源区间中减去多个区间
    
    Args:
        source: 源区间
        subtractors: 要减去的区间列表
    
    Returns:
        减去后的区间列表
    """
    result = [source]
    for subtractor in subtractors:
        new_result = []
        for r in result:
            new_result.extend(subtract_span(r, subtractor))
        result = new_result
    return result


def union_spans(spans: Iterable[Span]) -> List[Span]:
    """
    计算多个区间的并集
    
    Args:
        spans: 区间列表
    
    Returns:
        并集区间列表（合并后）
    """
    return merge_spans(spans)


def span_difference(spans1: Iterable[Span], spans2: Iterable[Span]) -> List[Span]:
    """
    计算两组区间的差集（spans1 - spans2）
    
    Args:
        spans1: 第一组区间
        spans2: 第二组区间（要减去的）
    
    Returns:
        差集区间列表
    """
    merged1 = merge_spans(spans1)
    merged2 = merge_spans(spans2)
    
    result = []
    for s in merged1:
        result.extend(subtract_spans(s, merged2))
    
    return result


def span_union_all(spans: Iterable[Span]) -> Optional[Span]:
    """
    计算所有区间的总合并范围
    
    Args:
        spans: 区间列表
    
    Returns:
        包含所有区间的最小单一区间（闭区间）
    """
    spans_list = list(spans)
    if not spans_list:
        return None
    
    min_start = min(s.start for s in spans_list)
    max_end = max(s.end for s in spans_list)
    
    return Span(min_start, max_end)


def find_gaps(spans: Iterable[Span], overall_range: Optional[Span] = None) -> List[Span]:
    """
    找出区间之间的间隙
    
    Args:
        spans: 区间列表
        overall_range: 可选的总体范围，间隙将被限制在此范围内
    
    Returns:
        间隙区间列表
    """
    merged = merge_spans(spans)
    if not merged:
        if overall_range:
            return [overall_range]
        return []
    
    gaps = []
    
    # 第一个间隙
    if overall_range and merged[0].start > overall_range.start:
        gaps.append(Span(overall_range.start, merged[0].start))
    
    # 中间的间隙
    for i in range(len(merged) - 1):
        current = merged[i]
        next_span = merged[i + 1]
        if current.end < next_span.start:
            gaps.append(Span(current.end, next_span.start))
    
    # 最后一个间隙
    if overall_range and merged[-1].end < overall_range.end:
        gaps.append(Span(merged[-1].end, overall_range.end))
    
    return gaps


def cover_spans(spans: Iterable[Span]) -> Optional[Span]:
    """
    计算覆盖所有区间的最小闭区间
    
    Args:
        spans: 区间列表
    
    Returns:
        覆盖所有区间的最小闭区间
    """
    spans_list = list(spans)
    if not spans_list:
        return None
    
    min_start = min(s.start for s in spans_list)
    max_end = max(s.end for s in spans_list)
    
    return closed_span(min_start, max_end)


def split_span(span: Span, at: float) -> List[Span]:
    """
    在指定点分割区间
    
    Args:
        span: 要分割的区间
        at: 分割点
    
    Returns:
        分割后的区间列表（可能为空、1个或2个）
    """
    if at <= span.start or at >= span.end:
        return [span]
    
    if at in span:
        # 在区间内分割
        left = Span(span.start, at, span.left_bound, BoundType.CLOSED)
        right = Span(at, span.end, BoundType.CLOSED, span.right_bound)
        return [left, right]
    
    return [span]


def split_span_into_chunks(span: Span, chunk_size: float) -> List[Span]:
    """
    将区间分割成等大小的块
    
    Args:
        span: 要分割的区间
        chunk_size: 每块大小
    
    Returns:
        分割后的区间列表
    """
    if chunk_size <= 0:
        raise ValueError("块大小必须为正数")
    
    chunks = []
    current = span.start
    
    while current < span.end:
        end = min(current + chunk_size, span.end)
        chunks.append(Span(current, end))
        current = end
    
    return chunks


def span_to_integers(span: Span) -> List[int]:
    """
    将区间转换为其中包含的所有整数
    
    Args:
        span: 区间
    
    Returns:
        整数列表（只包含真正在区间内的整数）
    """
    from math import ceil, floor
    
    # 找出第一个在区间内的整数
    if span.left_bound == BoundType.CLOSED:
        # 闭区间：第一个整数是 ceil(start)（确保 >= start）
        start_int = ceil(span.start)
    else:
        # 开区间：第一个整数是 floor(start) + 1（确保 > start）
        start_int = floor(span.start) + 1
    
    # 找出最后一个在区间内的整数
    if span.right_bound == BoundType.CLOSED:
        # 闭区间：最后一个整数是 floor(end)（确保 <= end）
        end_int = floor(span.end)
    else:
        # 开区间：最后一个整数是 ceil(end) - 1（确保 < end）
        end_int = ceil(span.end) - 1
    
    # 如果区间内没有整数，返回空列表
    if start_int > end_int:
        return []
    
    return list(range(start_int, end_int + 1))


def normalize_spans(spans: Iterable[Span]) -> List[Span]:
    """
    规范化区间列表：合并重叠区间，排序
    
    Args:
        spans: 区间列表
    
    Returns:
        规范化后的区间列表
    """
    return merge_spans(spans)


def count_overlapping(spans: Iterable[Span], point: float) -> int:
    """
    计算覆盖某点的区间数量
    
    Args:
        spans: 区间列表
        point: 要检查的点
    
    Returns:
        覆盖该点的区间数量
    """
    return sum(1 for s in spans if point in s)


def max_overlap_count(spans: Iterable[Span]) -> Tuple[int, Optional[Span]]:
    """
    找出最大重叠区间及其重叠数
    
    Args:
        spans: 区间列表
    
    Returns:
        (最大重叠数, 最大重叠区间)
    """
    spans_list = list(spans)
    if not spans_list:
        return (0, None)
    
    # 收集所有关键点
    events = []
    for s in spans_list:
        events.append((s.start, 1, s.left_bound))  # 1 表示进入
        events.append((s.end, -1, s.right_bound))  # -1 表示离开
    
    # 排序：先按位置，再按类型（离开优先于进入，以正确处理边界）
    def event_key(e):
        pos, delta, bound = e
        if delta == 1:  # 进入事件
            # 闭区间进入优先级低，开区间进入优先级更低
            priority = 1 if bound == BoundType.CLOSED else 0
        else:  # 离开事件
            # 闭区间离开优先级高，开区间离开优先级低
            priority = 2 if bound == BoundType.CLOSED else 0
        return (pos, priority, delta)
    
    events.sort(key=event_key)
    
    max_count = 0
    current_count = 0
    max_start = None
    max_end = None
    
    for pos, delta, _ in events:
        current_count += delta
        if current_count > max_count:
            max_count = current_count
            max_start = pos
            max_end = pos
    
    if max_count > 0 and max_start is not None:
        # 简化处理，返回一个点区间
        return (max_count, point_span(max_start))
    
    return (max_count, None)


# ============== 常用区间 ==============

def empty_span() -> Span:
    """创建空区间"""
    return Span(0, 0, BoundType.OPEN, BoundType.OPEN)


def infinite_span() -> Span:
    """创建无限区间（使用 float 极值）"""
    return Span(float('-inf'), float('inf'), BoundType.OPEN, BoundType.OPEN)


def positive_span() -> Span:
    """创建正数区间 (0, +∞)"""
    return Span(0, float('inf'), BoundType.OPEN, BoundType.OPEN)


def negative_span() -> Span:
    """创建负数区间 (-∞, 0)"""
    return Span(float('-inf'), 0, BoundType.OPEN, BoundType.OPEN)


def non_negative_span() -> Span:
    """创建非负区间 [0, +∞)"""
    return Span(0, float('inf'), BoundType.CLOSED, BoundType.OPEN)


# ============== 导出 ==============

__all__ = [
    # 类和枚举
    'Span',
    'BoundType',
    # 工厂函数
    'span',
    'closed_span',
    'open_span',
    'point_span',
    'empty_span',
    'infinite_span',
    'positive_span',
    'negative_span',
    'non_negative_span',
    # 操作函数
    'merge_spans',
    'intersection_of',
    'subtract_span',
    'subtract_spans',
    'union_spans',
    'span_difference',
    'span_union_all',
    'find_gaps',
    'cover_spans',
    'split_span',
    'split_span_into_chunks',
    'span_to_integers',
    'normalize_spans',
    'count_overlapping',
    'max_overlap_count',
]