"""
区间树（Interval Tree）实现
================================

一种用于高效处理区间查询的增强二叉搜索树。

时间复杂度：
- 插入：O(log n) 平均
- 删除：O(log n) 平均
- 点查询：O(log n + k)，k 为结果数量
- 区间重叠查询：O(log n + k)，k 为结果数量

空间复杂度：O(n)
"""

from typing import Generic, TypeVar, List, Optional, Iterator, Callable
from dataclasses import dataclass
import random

from .interval import Interval
from .node import IntervalNode

T = TypeVar('T', int, float)


class IntervalTree(Generic[T]):
    """
    区间树
    
    用于高效查询区间重叠的数据结构。
    
    示例:
        >>> tree = IntervalTree()
        >>> tree.insert(Interval(1, 5))
        >>> tree.insert(Interval(3, 8))
        >>> tree.query_point(4)  # 查找包含点 4 的区间
        [Interval(1, 5), Interval(3, 8)]
        >>> tree.query_overlaps(Interval(4, 6))  # 查找与区间 [4,6] 重叠的区间
        [Interval(1, 5), Interval(3, 8)]
    """
    
    def __init__(self, intervals: Optional[List[Interval[T]]] = None):
        """
        初始化区间树
        
        参数:
            intervals: 可选的初始区间列表
        """
        self._root: Optional[IntervalNode[T]] = None
        self._size: int = 0
        
        if intervals:
            for interval in intervals:
                self.insert(interval)
    
    def insert(self, interval: Interval[T]) -> None:
        """
        插入一个区间
        
        参数:
            interval: 要插入的区间
        """
        if self._root is None:
            center = self._compute_center([interval])
            self._root = IntervalNode(center=center)
            self._root.add_interval(interval)
        else:
            self._insert_node(self._root, interval)
        self._size += 1
    
    def _compute_center(self, intervals: List[Interval[T]]) -> T:
        """计算区间的中心点"""
        if not intervals:
            return 0
        starts = [i.start for i in intervals]
        ends = [i.end for i in intervals]
        center = (min(starts) + max(ends)) / 2.0
        # 如果输入是整数，返回整数中心
        if all(isinstance(i.start, int) and isinstance(i.end, int) for i in intervals):
            return int(center)
        return center
    
    def _insert_node(self, node: IntervalNode[T], interval: Interval[T]) -> None:
        """递归插入区间到合适的位置"""
        # 区间与中心点重叠
        if interval.start <= node.center <= interval.end:
            node.add_interval(interval)
            return
        
        # 区间完全在中心点左侧
        if interval.end < node.center:
            if node.left is None:
                node.left = IntervalNode(center=self._compute_center([interval]))
                node.left.add_interval(interval)
                node.left.update_bounds()
            else:
                self._insert_node(node.left, interval)
            node.update_bounds()
            return
        
        # 区间完全在中心点右侧
        if interval.start > node.center:
            if node.right is None:
                node.right = IntervalNode(center=self._compute_center([interval]))
                node.right.add_interval(interval)
                node.right.update_bounds()
            else:
                self._insert_node(node.right, interval)
            node.update_bounds()
            return
    
    def remove(self, interval: Interval[T]) -> bool:
        """
        移除一个区间
        
        参数:
            interval: 要移除的区间
            
        返回:
            是否成功移除
        """
        if self._root is None:
            return False
        
        result = self._remove_node(self._root, interval)
        if result:
            self._size -= 1
        return result
    
    def _remove_node(self, node: IntervalNode[T], interval: Interval[T]) -> bool:
        """递归移除区间"""
        # 检查当前节点的重叠区间列表
        if interval in node.overlapping:
            node.remove_interval(interval)
            # 如果节点变空且有子节点，可能需要重建
            if not node.overlapping and node.is_leaf():
                # 叶节点且无区间，可以安全删除
                pass  # 简单处理，保留空节点
            return True
        
        # 递归搜索
        if interval.end < node.center and node.left:
            return self._remove_node(node.left, interval)
        elif interval.start > node.center and node.right:
            return self._remove_node(node.right, interval)
        else:
            # 需要搜索两边
            found = False
            if node.left:
                found = self._remove_node(node.left, interval)
            if not found and node.right:
                found = self._remove_node(node.right, interval)
            return found
    
    def query_point(self, point: T) -> List[Interval[T]]:
        """
        查询包含指定点的所有区间
        
        参数:
            point: 查询点
            
        返回:
            包含该点的区间列表
        """
        if self._root is None:
            return []
        
        result: List[Interval[T]] = []
        self._query_point_node(self._root, point, result)
        return result
    
    def _query_point_node(self, node: IntervalNode[T], point: T, result: List[Interval[T]]) -> None:
        """递归查询包含指定点的区间"""
        # 检查当前节点的区间
        for interval in node.overlapping:
            if interval.contains_point(point):
                result.append(interval)
        
        # 检查是否需要搜索左子树
        if node.left and point <= node.center:
            self._query_point_node(node.left, point, result)
        
        # 检查是否需要搜索右子树
        if node.right and point >= node.center:
            self._query_point_node(node.right, point, result)
    
    def query_overlaps(self, interval: Interval[T]) -> List[Interval[T]]:
        """
        查询与指定区间重叠的所有区间
        
        参数:
            interval: 查询区间
            
        返回:
            与该区间重叠的区间列表
        """
        if self._root is None:
            return []
        
        result: List[Interval[T]] = []
        self._query_overlaps_node(self._root, interval, result)
        return result
    
    def _query_overlaps_node(self, node: IntervalNode[T], interval: Interval[T], result: List[Interval[T]]) -> None:
        """递归查询重叠区间"""
        # 检查当前节点的区间
        for iv in node.overlapping:
            if iv.overlaps(interval):
                result.append(iv)
        
        # 检查是否需要搜索左子树
        if node.left and interval.start <= node.center:
            self._query_overlaps_node(node.left, interval, result)
        
        # 检查是否需要搜索右子树
        if node.right and interval.end >= node.center:
            self._query_overlaps_node(node.right, interval, result)
    
    def query_contains(self, interval: Interval[T]) -> List[Interval[T]]:
        """
        查询完全包含指定区间的区间
        
        参数:
            interval: 查询区间
            
        返回:
            完全包含该区间的区间列表
        """
        if self._root is None:
            return []
        
        result: List[Interval[T]] = []
        self._query_contains_node(self._root, interval, result)
        return result
    
    def _query_contains_node(self, node: IntervalNode[T], interval: Interval[T], result: List[Interval[T]]) -> None:
        """递归查询包含指定区间的区间"""
        for iv in node.overlapping:
            if iv.contains(interval):
                result.append(iv)
        
        # 搜索左子树（包含区间可能在左边）
        if node.left and node.left.max_end is not None and node.left.max_end >= interval.end:
            self._query_contains_node(node.left, interval, result)
        
        # 搜索右子树
        if node.right and node.right.min_start is not None and node.right.min_start <= interval.start:
            self._query_contains_node(node.right, interval, result)
    
    def query_contained_by(self, interval: Interval[T]) -> List[Interval[T]]:
        """
        查询被指定区间完全包含的区间
        
        参数:
            interval: 查询区间
            
        返回:
            被该区间完全包含的区间列表
        """
        if self._root is None:
            return []
        
        result: List[Interval[T]] = []
        self._query_contained_by_node(self._root, interval, result)
        return result
    
    def _query_contained_by_node(self, node: IntervalNode[T], interval: Interval[T], result: List[Interval[T]]) -> None:
        """递归查询被指定区间包含的区间"""
        for iv in node.overlapping:
            if interval.contains(iv):
                result.append(iv)
        
        # 搜索左子树
        if node.left and node.left.min_start is not None and node.left.min_start >= interval.start:
            self._query_contained_by_node(node.left, interval, result)
        
        # 搜索右子树
        if node.right and node.right.max_end is not None and node.right.max_end <= interval.end:
            self._query_contained_by_node(node.right, interval, result)
    
    def find_first_overlapping(self, interval: Interval[T]) -> Optional[Interval[T]]:
        """查找第一个与指定区间重叠的区间"""
        results = self.query_overlaps(interval)
        return results[0] if results else None
    
    def find_all_gaps(self, start: T, end: T) -> List[Interval[T]]:
        """
        找出指定范围内未被任何区间覆盖的空白区域
        
        参数:
            start: 范围起点
            end: 范围终点
            
        返回:
            空白区间列表
        """
        # 收集范围内所有区间并排序
        all_intervals = sorted(self.query_overlaps(Interval(start, end)), key=lambda x: x.start)
        
        gaps: List[Interval[T]] = []
        current = start
        
        for interval in all_intervals:
            if interval.start > current:
                gaps.append(Interval(current, interval.start - 1))
            current = max(current, interval.end + 1)
        
        if current <= end:
            gaps.append(Interval(current, end))
        
        return gaps
    
    def __len__(self) -> int:
        """返回区间数量"""
        return self._size
    
    def __bool__(self) -> bool:
        """检查树是否非空"""
        return self._size > 0
    
    def __contains__(self, interval: Interval[T]) -> bool:
        """检查区间是否在树中"""
        results = self.query_overlaps(interval)
        return interval in results
    
    def __iter__(self) -> Iterator[Interval[T]]:
        """迭代所有区间"""
        if self._root:
            yield from self._root.collect_all()
    
    def clear(self) -> None:
        """清空区间树"""
        self._root = None
        self._size = 0
    
    def height(self) -> int:
        """返回树的高度"""
        return self._root.height() if self._root else 0
    
    def is_empty(self) -> bool:
        """检查树是否为空"""
        return self._size == 0
    
    def to_list(self) -> List[Interval[T]]:
        """将所有区间转为列表"""
        return list(self) if self._root else []
    
    def get_statistics(self) -> dict:
        """获取树的统计信息"""
        return {
            'size': self._size,
            'height': self.height(),
            'is_empty': self.is_empty(),
            'node_count': self._root.size() if self._root else 0
        }
    
    def balance(self) -> None:
        """重建平衡的区间树"""
        if self._size <= 1:
            return
        
        intervals = self.to_list()
        self.clear()
        
        # 使用中位数分割策略重建
        self._build_balanced(intervals)
    
    def _build_balanced(self, intervals: List[Interval[T]]) -> None:
        """使用中位数分割构建平衡树"""
        if not intervals:
            return
        
        intervals.sort()
        self._build_balanced_recursive(intervals)
    
    def _build_balanced_recursive(self, intervals: List[Interval[T]]) -> None:
        """递归构建平衡树"""
        if not intervals:
            return
        
        mid = len(intervals) // 2
        center_interval = intervals[mid]
        
        # 收集与中心区间重叠的所有区间
        overlapping = [center_interval]
        left_intervals = []
        right_intervals = []
        
        for interval in intervals:
            if interval == center_interval:
                continue
            if interval.end < center_interval.start:
                left_intervals.append(interval)
            elif interval.start > center_interval.end:
                right_intervals.append(interval)
            else:
                overlapping.append(interval)
        
        # 插入重叠区间
        for interval in overlapping:
            self.insert(interval)
        
        # 递归处理左右区间
        self._build_balanced_recursive(left_intervals)
        self._build_balanced_recursive(right_intervals)
    
    @classmethod
    def from_tuples(cls, intervals: List[tuple]) -> 'IntervalTree[T]':
        """
        从元组列表创建区间树
        
        参数:
            intervals: 元组列表，每个元组为 (start, end) 或 (start, end, value)
            
        返回:
            新的区间树实例
        """
        tree = cls()
        for t in intervals:
            if len(t) == 2:
                tree.insert(Interval(t[0], t[1]))
            else:
                tree.insert(Interval(t[0], t[1], t[2]))
        return tree
    
    def __repr__(self) -> str:
        return f"IntervalTree(size={self._size}, height={self.height()})"