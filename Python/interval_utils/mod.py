"""
区间操作工具模块 (Interval Utilities)

提供高效的区间数据结构操作，包括：
- 区间合并、交集、差集
- 区间插入、删除
- 区间查找（点查询、范围查询）
- 区间覆盖检测

零外部依赖，纯 Python 实现。

作者: AllToolkit
日期: 2026-04-18
"""

from typing import List, Tuple, Optional, Iterable, Set
from dataclasses import dataclass
from bisect import bisect_left, bisect_right


@dataclass
class Interval:
    """
    区间类，表示一个闭区间 [start, end]
    
    属性:
        start: 区间起始值（包含）
        end: 区间结束值（包含）
    """
    start: int
    end: int
    
    def __post_init__(self):
        if self.start > self.end:
            raise ValueError(f"区间起始值 {self.start} 不能大于结束值 {self.end}")
    
    def __contains__(self, value: int) -> bool:
        """检查值是否在区间内"""
        return self.start <= value <= self.end
    
    def __len__(self) -> int:
        """返回区间长度"""
        return self.end - self.start + 1
    
    def __repr__(self) -> str:
        return f"[{self.start}, {self.end}]"
    
    def __eq__(self, other) -> bool:
        if not isinstance(other, Interval):
            return False
        return self.start == other.start and self.end == other.end
    
    def __hash__(self) -> int:
        return hash((self.start, self.end))
    
    def __lt__(self, other) -> bool:
        if not isinstance(other, Interval):
            return NotImplemented
        return (self.start, self.end) < (other.start, other.end)
    
    @property
    def length(self) -> int:
        """区间长度（元素个数）"""
        return self.end - self.start + 1
    
    def overlaps(self, other: 'Interval') -> bool:
        """检查两个区间是否重叠"""
        return self.start <= other.end and other.start <= self.end
    
    def adjacent(self, other: 'Interval') -> bool:
        """检查两个区间是否相邻（可合并）"""
        return self.start == other.end + 1 or other.start == self.end + 1
    
    def merge(self, other: 'Interval') -> 'Interval':
        """合并两个重叠或相邻的区间"""
        if not self.overlaps(other) and not self.adjacent(other):
            raise ValueError(f"区间 {self} 和 {other} 无法合并")
        return Interval(min(self.start, other.start), max(self.end, other.end))
    
    def intersection(self, other: 'Interval') -> Optional['Interval']:
        """返回两个区间的交集，无交集则返回 None"""
        if not self.overlaps(other):
            return None
        return Interval(max(self.start, other.start), min(self.end, other.end))
    
    def difference(self, other: 'Interval') -> List['Interval']:
        """
        返回当前区间减去另一区间后的结果
        结果可能是 0、1 或 2 个区间
        """
        if not self.overlaps(other):
            return [Interval(self.start, self.end)]
        
        result = []
        if self.start < other.start:
            result.append(Interval(self.start, other.start - 1))
        if self.end > other.end:
            result.append(Interval(other.end + 1, self.end))
        return result
    
    def to_tuple(self) -> Tuple[int, int]:
        """转换为元组"""
        return (self.start, self.end)
    
    @classmethod
    def from_tuple(cls, t: Tuple[int, int]) -> 'Interval':
        """从元组创建区间"""
        return cls(t[0], t[1])


class IntervalSet:
    """
    区间集合类
    
    维护一组不相交的有序区间，支持高效的各种区间操作。
    使用基于排序数组的实现，适合中等规模的区间集合。
    """
    
    def __init__(self, intervals: Optional[Iterable[Interval]] = None):
        """
        初始化区间集合
        
        参数:
            intervals: 初始区间列表
        """
        self._intervals: List[Interval] = []
        if intervals:
            for interval in intervals:
                self.add(interval)
    
    def __len__(self) -> int:
        """返回区间数量"""
        return len(self._intervals)
    
    def __bool__(self) -> bool:
        """是否非空"""
        return len(self._intervals) > 0
    
    def __iter__(self):
        """迭代所有区间"""
        return iter(self._intervals)
    
    def __repr__(self) -> str:
        intervals_str = ", ".join(str(i) for i in self._intervals)
        return f"IntervalSet({{{intervals_str}}})"
    
    def __eq__(self, other) -> bool:
        if not isinstance(other, IntervalSet):
            return False
        return self._intervals == other._intervals
    
    @property
    def total_length(self) -> int:
        """所有区间的总长度"""
        return sum(i.length for i in self._intervals)
    
    @property
    def is_empty(self) -> bool:
        """是否为空"""
        return len(self._intervals) == 0
    
    @property
    def min_value(self) -> Optional[int]:
        """最小值"""
        return self._intervals[0].start if self._intervals else None
    
    @property
    def max_value(self) -> Optional[int]:
        """最大值"""
        return self._intervals[-1].end if self._intervals else None
    
    def _find_insert_position(self, start: int) -> int:
        """找到新区间的插入位置"""
        return bisect_left(self._intervals, Interval(start, start))
    
    def _find_overlapping_range(self, interval: Interval) -> Tuple[int, int]:
        """找到与指定区间重叠的所有区间的索引范围"""
        left = bisect_left(self._intervals, Interval(interval.start, interval.start))
        # 向左扩展，找到可能重叠的区间
        while left > 0 and self._intervals[left - 1].overlaps(interval):
            left -= 1
        
        right = bisect_right(self._intervals, Interval(interval.end, interval.end))
        # 向右扩展，找到可能重叠的区间
        while right < len(self._intervals) and self._intervals[right].overlaps(interval):
            right += 1
        
        return left, right
    
    def add(self, interval: Interval) -> None:
        """
        添加区间，自动合并重叠或相邻的区间
        
        参数:
            interval: 要添加的区间
        """
        if not isinstance(interval, Interval):
            interval = Interval(interval[0], interval[1])
        
        if not self._intervals:
            self._intervals.append(interval)
            return
        
        left, right = self._find_overlapping_range(interval)
        
        if left < right:
            # 有重叠的区间，合并它们
            merged = Interval(
                min(self._intervals[left].start, interval.start),
                max(self._intervals[right - 1].end, interval.end)
            )
            # 检查是否可以向相邻的区间扩展
            if left > 0 and self._intervals[left - 1].adjacent(merged):
                merged = self._intervals[left - 1].merge(merged)
                left -= 1
            if right < len(self._intervals) and self._intervals[right].adjacent(merged):
                merged = merged.merge(self._intervals[right])
                right += 1
            self._intervals[left:right] = [merged]
        else:
            # 无重叠，检查是否与相邻区间可以合并
            insert_pos = left
            merged = interval
            merge_left = False
            merge_right = False
            
            if insert_pos > 0 and self._intervals[insert_pos - 1].adjacent(merged):
                merged = self._intervals[insert_pos - 1].merge(merged)
                merge_left = True
            
            if insert_pos < len(self._intervals) and self._intervals[insert_pos].adjacent(merged):
                merged = merged.merge(self._intervals[insert_pos])
                merge_right = True
            
            if merge_left and merge_right:
                self._intervals[insert_pos - 1:insert_pos + 1] = [merged]
            elif merge_left:
                self._intervals[insert_pos - 1] = merged
            elif merge_right:
                self._intervals[insert_pos] = merged
            else:
                self._intervals.insert(insert_pos, merged)
    
    def remove(self, interval: Interval) -> None:
        """
        移除区间（从现有区间中减去指定区间）
        
        参数:
            interval: 要移除的区间
        """
        if not isinstance(interval, Interval):
            interval = Interval(interval[0], interval[1])
        
        if not self._intervals:
            return
        
        left, right = self._find_overlapping_range(interval)
        
        if left >= right:
            return
        
        new_intervals = []
        for i in range(left, right):
            new_intervals.extend(self._intervals[i].difference(interval))
        
        self._intervals[left:right] = new_intervals
    
    def contains(self, value: int) -> bool:
        """
        检查值是否在任意区间内
        
        参数:
            value: 要检查的值
        
        返回:
            如果值在某个区间内则返回 True
        """
        if not self._intervals:
            return False
        
        # 使用只比较 start 的方式查找
        starts = [i.start for i in self._intervals]
        idx = bisect_right(starts, value)
        if idx == 0:
            return False
        
        # 检查 idx-1 的区间是否包含 value
        candidate = self._intervals[idx - 1]
        return value >= candidate.start and value <= candidate.end
    
    def contains_interval(self, interval: Interval) -> bool:
        """
        检查整个区间是否被完全覆盖
        
        参数:
            interval: 要检查的区间
        
        返回:
            如果整个区间都被覆盖则返回 True
        """
        if not isinstance(interval, Interval):
            interval = Interval(interval[0], interval[1])
        
        if not self._intervals:
            return False
        
        starts = [i.start for i in self._intervals]
        idx = bisect_right(starts, interval.start)
        if idx == 0:
            return False
        
        candidate = self._intervals[idx - 1]
        return interval.start >= candidate.start and interval.end <= candidate.end
    
    def find_containing(self, value: int) -> Optional[Interval]:
        """
        找到包含指定值的区间
        
        参数:
            value: 要查找的值
        
        返回:
            包含该值的区间，如果不存在则返回 None
        """
        if not self._intervals:
            return None
        
        starts = [i.start for i in self._intervals]
        idx = bisect_right(starts, value)
        if idx == 0:
            return None
        
        candidate = self._intervals[idx - 1]
        if value >= candidate.start and value <= candidate.end:
            return candidate
        return None
        return candidate if value in candidate else None
    
    def find_overlapping(self, interval: Interval) -> List[Interval]:
        """
        找到所有与指定区间重叠的区间
        
        参数:
            interval: 查询区间
        
        返回:
            重叠的区间列表
        """
        if not isinstance(interval, Interval):
            interval = Interval(interval[0], interval[1])
        
        if not self._intervals:
            return []
        
        left, right = self._find_overlapping_range(interval)
        return self._intervals[left:right]
    
    def union(self, other: 'IntervalSet') -> 'IntervalSet':
        """
        返回与另一区间集合并集
        
        参数:
            other: 另一个区间集合
        
        返回:
            并集区间集合
        """
        result = IntervalSet(self._intervals)
        for interval in other:
            result.add(interval)
        return result
    
    def intersection(self, other: 'IntervalSet') -> 'IntervalSet':
        """
        返回与另一区间集合交集
        
        参数:
            other: 另一个区间集合
        
        返回:
            交集区间集合
        """
        result = IntervalSet()
        for interval in self._intervals:
            for other_interval in other.find_overlapping(interval):
                inter = interval.intersection(other_interval)
                if inter:
                    result.add(inter)
        return result
    
    def difference(self, other: 'IntervalSet') -> 'IntervalSet':
        """
        返回与另一区间集合差集（当前集合减去另一集合）
        
        参数:
            other: 另一个区间集合
        
        返回:
            差集区间集合
        """
        result = IntervalSet(self._intervals)
        for interval in other:
            result.remove(interval)
        return result
    
    def symmetric_difference(self, other: 'IntervalSet') -> 'IntervalSet':
        """
        返回与另一区间集合的对称差集
        
        参数:
            other: 另一个区间集合
        
        返回:
            对称差集区间集合
        """
        return self.union(other).difference(self.intersection(other))
    
    def gaps(self) -> 'IntervalSet':
        """
        返回区间之间的空隙
        
        返回:
            空隙区间集合
        """
        if len(self._intervals) < 2:
            return IntervalSet()
        
        gaps = IntervalSet()
        for i in range(len(self._intervals) - 1):
            current = self._intervals[i]
            next_interval = self._intervals[i + 1]
            gap_start = current.end + 1
            gap_end = next_interval.start - 1
            if gap_start <= gap_end:
                gaps.add(Interval(gap_start, gap_end))
        return gaps
    
    def cover_range(self, start: int, end: int) -> 'IntervalSet':
        """
        返回指定范围内被覆盖的部分
        
        参数:
            start: 范围起始
            end: 范围结束
        
        返回:
            被覆盖的区间集合
        """
        query_range = Interval(start, end)
        result = IntervalSet()
        for interval in self._intervals:
            inter = interval.intersection(query_range)
            if inter:
                result.add(inter)
        return result
    
    def uncovered_range(self, start: int, end: int) -> 'IntervalSet':
        """
        返回指定范围内未被覆盖的部分
        
        参数:
            start: 范围起始
            end: 范围结束
        
        返回:
            未被覆盖的区间集合
        """
        query_range = Interval(start, end)
        covered = self.cover_range(start, end)
        result = IntervalSet([query_range])
        for interval in covered:
            result.remove(interval)
        return result
    
    def to_list(self) -> List[Interval]:
        """转换为区间列表"""
        return list(self._intervals)
    
    def to_tuples(self) -> List[Tuple[int, int]]:
        """转换为元组列表"""
        return [i.to_tuple() for i in self._intervals]
    
    @classmethod
    def from_tuples(cls, tuples: Iterable[Tuple[int, int]]) -> 'IntervalSet':
        """从元组列表创建区间集合"""
        return cls(Interval(t[0], t[1]) for t in tuples)
    
    def copy(self) -> 'IntervalSet':
        """创建副本"""
        return IntervalSet(self._intervals)
    
    def clear(self) -> None:
        """清空所有区间"""
        self._intervals.clear()


# ==================== 便捷函数 ====================

def merge_intervals(intervals: Iterable[Tuple[int, int]]) -> List[Tuple[int, int]]:
    """
    合并重叠或相邻的区间
    
    参数:
        intervals: 区间元组列表
    
    返回:
        合并后的区间元组列表
    """
    if not intervals:
        return []
    
    sorted_intervals = sorted((Interval(t[0], t[1]) for t in intervals), key=lambda x: x.start)
    result = [sorted_intervals[0]]
    
    for interval in sorted_intervals[1:]:
        if interval.overlaps(result[-1]) or interval.adjacent(result[-1]):
            result[-1] = result[-1].merge(interval)
        else:
            result.append(interval)
    
    return [i.to_tuple() for i in result]


def interval_intersection(intervals1: Iterable[Tuple[int, int]], 
                          intervals2: Iterable[Tuple[int, int]]) -> List[Tuple[int, int]]:
    """
    计算两组区间的交集
    
    参数:
        intervals1: 第一组区间
        intervals2: 第二组区间
    
    返回:
        交集区间列表
    """
    set1 = IntervalSet.from_tuples(intervals1)
    set2 = IntervalSet.from_tuples(intervals2)
    return set1.intersection(set2).to_tuples()


def interval_difference(intervals1: Iterable[Tuple[int, int]], 
                        intervals2: Iterable[Tuple[int, int]]) -> List[Tuple[int, int]]:
    """
    计算两组区间的差集
    
    参数:
        intervals1: 第一组区间
        intervals2: 第二组区间
    
    返回:
        差集区间列表
    """
    set1 = IntervalSet.from_tuples(intervals1)
    set2 = IntervalSet.from_tuples(intervals2)
    return set1.difference(set2).to_tuples()


def interval_union(intervals1: Iterable[Tuple[int, int]], 
                   intervals2: Iterable[Tuple[int, int]]) -> List[Tuple[int, int]]:
    """
    计算两组区间的并集
    
    参数:
        intervals1: 第一组区间
        intervals2: 第二组区间
    
    返回:
        并集区间列表
    """
    set1 = IntervalSet.from_tuples(intervals1)
    set2 = IntervalSet.from_tuples(intervals2)
    return set1.union(set2).to_tuples()


def find_gaps(intervals: Iterable[Tuple[int, int]]) -> List[Tuple[int, int]]:
    """
    找出区间之间的空隙
    
    参数:
        intervals: 区间列表
    
    返回:
        空隙区间列表
    """
    interval_set = IntervalSet.from_tuples(intervals)
    return interval_set.gaps().to_tuples()


def is_covered(intervals: Iterable[Tuple[int, int]], value: int) -> bool:
    """
    检查值是否被区间覆盖
    
    参数:
        intervals: 区间列表
        value: 要检查的值
    
    返回:
        如果被覆盖则返回 True
    """
    interval_set = IntervalSet.from_tuples(intervals)
    return interval_set.contains(value)


def find_containing_interval(intervals: Iterable[Tuple[int, int]], 
                             value: int) -> Optional[Tuple[int, int]]:
    """
    找到包含指定值的区间
    
    参数:
        intervals: 区间列表
        value: 要查找的值
    
    返回:
        包含该值的区间，如果不存在则返回 None
    """
    interval_set = IntervalSet.from_tuples(intervals)
    result = interval_set.find_containing(value)
    return result.to_tuple() if result else None


def get_total_coverage(intervals: Iterable[Tuple[int, int]]) -> int:
    """
    计算区间覆盖的总长度
    
    参数:
        intervals: 区间列表
    
    返回:
        总覆盖长度
    """
    interval_set = IntervalSet.from_tuples(intervals)
    return interval_set.total_length


# ==================== 高级功能 ====================

class IntervalMap:
    """
    区间映射类
    
    将值映射到区间，支持区间作为键存储任意值。
    """
    
    def __init__(self):
        """初始化区间映射"""
        self._intervals: List[Interval] = []
        self._values: List[any] = []
    
    def __len__(self) -> int:
        return len(self._intervals)
    
    def __bool__(self) -> bool:
        return len(self._intervals) > 0
    
    def set(self, start: int, end: int, value: any) -> None:
        """
        设置区间的值
        
        参数:
            start: 区间起始
            end: 区间结束
            value: 要设置的值
        """
        interval = Interval(start, end)
        
        # 先移除重叠部分
        idx = 0
        while idx < len(self._intervals):
            if self._intervals[idx].overlaps(interval):
                # 分割被重叠的区间
                existing = self._intervals[idx]
                existing_value = self._values[idx]
                
                parts = existing.difference(interval)
                del self._intervals[idx]
                del self._values[idx]
                
                for part in parts:
                    self._intervals.insert(idx, part)
                    self._values.insert(idx, existing_value)
                    idx += 1
            else:
                idx += 1
        
        # 插入新区间
        insert_pos = bisect_left([i.start for i in self._intervals], start)
        self._intervals.insert(insert_pos, interval)
        self._values.insert(insert_pos, value)
    
    def get(self, value: int) -> any:
        """
        获取值对应的区间值
        
        参数:
            value: 要查找的值
        
        返回:
            区间对应的值，如果不存在则返回 None
        """
        for i, interval in enumerate(self._intervals):
            if value in interval:
                return self._values[i]
        return None
    
    def get_range(self, start: int, end: int) -> List[Tuple[int, int, any]]:
        """
        获取范围内的所有区间及其值
        
        参数:
            start: 范围起始
            end: 范围结束
        
        返回:
            (区间起始, 区间结束, 值) 元组列表
        """
        result = []
        query = Interval(start, end)
        for i, interval in enumerate(self._intervals):
            if interval.overlaps(query):
                result.append((interval.start, interval.end, self._values[i]))
        return result
    
    def remove(self, start: int, end: int) -> None:
        """
        移除区间
        
        参数:
            start: 区间起始
            end: 区间结束
        """
        interval = Interval(start, end)
        idx = 0
        while idx < len(self._intervals):
            if self._intervals[idx].overlaps(interval):
                existing = self._intervals[idx]
                existing_value = self._values[idx]
                
                parts = existing.difference(interval)
                del self._intervals[idx]
                del self._values[idx]
                
                for part in parts:
                    self._intervals.insert(idx, part)
                    self._values.insert(idx, existing_value)
                    idx += 1
            else:
                idx += 1
    
    def items(self) -> List[Tuple[int, int, any]]:
        """返回所有 (起始, 结束, 值) 元组"""
        return [(i.start, i.end, v) for i, v in zip(self._intervals, self._values)]
    
    def clear(self) -> None:
        """清空所有映射"""
        self._intervals.clear()
        self._values.clear()


class RangeSet:
    """
    范围集合类
    
    专为快速成员检测优化的整数集合实现。
    使用区间存储连续值，空间效率高。
    """
    
    def __init__(self, values: Optional[Iterable[int]] = None):
        """
        初始化范围集合
        
        参数:
            values: 初始值列表
        """
        self._interval_set = IntervalSet()
        if values:
            self.update(values)
    
    def __len__(self) -> int:
        return self._interval_set.total_length
    
    def __contains__(self, value: int) -> bool:
        return self._interval_set.contains(value)
    
    def __iter__(self):
        """迭代所有元素"""
        for interval in self._interval_set:
            for value in range(interval.start, interval.end + 1):
                yield value
    
    def __repr__(self) -> str:
        return f"RangeSet({list(self._interval_set.to_tuples())})"
    
    def __eq__(self, other) -> bool:
        if not isinstance(other, RangeSet):
            return False
        return self._interval_set == other._interval_set
    
    def add(self, value: int) -> None:
        """添加单个值"""
        self._interval_set.add(Interval(value, value))
    
    def add_range(self, start: int, end: int) -> None:
        """添加范围"""
        self._interval_set.add(Interval(start, end))
    
    def update(self, values: Iterable[int]) -> None:
        """添加多个值"""
        for value in values:
            self.add(value)
    
    def remove(self, value: int) -> None:
        """移除值"""
        self._interval_set.remove(Interval(value, value))
    
    def discard(self, value: int) -> None:
        """移除值（不存在时不报错）"""
        if value in self:
            self.remove(value)
    
    def remove_range(self, start: int, end: int) -> None:
        """移除范围"""
        self._interval_set.remove(Interval(start, end))
    
    def union(self, other: 'RangeSet') -> 'RangeSet':
        """返回并集"""
        result = RangeSet()
        result._interval_set = self._interval_set.union(other._interval_set)
        return result
    
    def intersection(self, other: 'RangeSet') -> 'RangeSet':
        """返回交集"""
        result = RangeSet()
        result._interval_set = self._interval_set.intersection(other._interval_set)
        return result
    
    def difference(self, other: 'RangeSet') -> 'RangeSet':
        """返回差集"""
        result = RangeSet()
        result._interval_set = self._interval_set.difference(other._interval_set)
        return result
    
    def symmetric_difference(self, other: 'RangeSet') -> 'RangeSet':
        """返回对称差集"""
        result = RangeSet()
        result._interval_set = self._interval_set.symmetric_difference(other._interval_set)
        return result
    
    def issubset(self, other: 'RangeSet') -> bool:
        """是否为子集"""
        return self._interval_set.difference(other._interval_set).is_empty
    
    def issuperset(self, other: 'RangeSet') -> bool:
        """是否为超集"""
        return other._interval_set.difference(self._interval_set).is_empty
    
    def isdisjoint(self, other: 'RangeSet') -> bool:
        """是否无交集"""
        return self._interval_set.intersection(other._interval_set).is_empty
    
    def copy(self) -> 'RangeSet':
        """创建副本"""
        result = RangeSet()
        result._interval_set = self._interval_set.copy()
        return result
    
    def clear(self) -> None:
        """清空集合"""
        self._interval_set.clear()
    
    @property
    def intervals(self) -> List[Tuple[int, int]]:
        """返回区间列表"""
        return self._interval_set.to_tuples()
    
    @property
    def min_value(self) -> Optional[int]:
        """最小值"""
        return self._interval_set.min_value
    
    @property
    def max_value(self) -> Optional[int]:
        """最大值"""
        return self._interval_set.max_value
    
    @classmethod
    def from_range(cls, start: int, end: int) -> 'RangeSet':
        """从范围创建集合"""
        result = cls()
        result.add_range(start, end)
        return result


if __name__ == "__main__":
    # 简单演示
    print("=== 区间工具演示 ===\n")
    
    # 创建区间
    i1 = Interval(1, 5)
    i2 = Interval(3, 8)
    print(f"区间1: {i1}")
    print(f"区间2: {i2}")
    print(f"重叠: {i1.overlaps(i2)}")
    print(f"交集: {i1.intersection(i2)}")
    print(f"合并: {i1.merge(i2)}")
    
    # 区间集合
    print("\n=== 区间集合演示 ===")
    intervals = IntervalSet()
    intervals.add(Interval(1, 5))
    intervals.add(Interval(10, 15))
    intervals.add(Interval(3, 7))  # 会合并
    print(f"添加后: {intervals}")
    print(f"总长度: {intervals.total_length}")
    print(f"包含 4: {intervals.contains(4)}")
    print(f"包含 8: {intervals.contains(8)}")
    print(f"空隙: {intervals.gaps()}")
    
    # 便捷函数
    print("\n=== 便捷函数演示 ===")
    data = [(1, 3), (2, 6), (8, 10), (9, 12)]
    print(f"原始区间: {data}")
    print(f"合并后: {merge_intervals(data)}")
    
    # RangeSet 演示
    print("\n=== RangeSet 演示 ===")
    rs = RangeSet()
    rs.add_range(1, 10)
    rs.add_range(20, 30)
    rs.add(15)
    print(f"RangeSet: {rs.intervals}")
    print(f"元素数量: {len(rs)}")
    print(f"包含 5: {5 in rs}")
    print(f"包含 16: {16 in rs}")