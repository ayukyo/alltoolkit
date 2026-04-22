"""
区间树节点
"""

from typing import Generic, TypeVar, List, Optional, Any
from dataclasses import dataclass, field

from .interval import Interval

T = TypeVar('T', int, float)


@dataclass
class IntervalNode(Generic[T]):
    """
    区间树节点
    
    使用增强的二叉搜索树结构，每个节点存储：
    - center: 分割点
    - overlapping: 与分割点重叠的区间列表
    - left: 左子树（区间终点 < center）
    - right: 右子树（区间起点 > center）
    - max_end: 子树中最大的区间终点
    - min_start: 子树中最小的区间起点
    """
    center: T
    overlapping: List[Interval[T]] = field(default_factory=list)
    left: Optional['IntervalNode[T]'] = None
    right: Optional['IntervalNode[T]'] = None
    max_end: Optional[T] = None
    min_start: Optional[T] = None
    
    def __post_init__(self):
        """初始化 max_end 和 min_start"""
        if self.overlapping:
            self.max_end = max(i.end for i in self.overlapping)
            self.min_start = min(i.start for i in self.overlapping)
        else:
            self.max_end = None
            self.min_start = None
    
    def update_bounds(self):
        """更新节点的边界值"""
        if self.overlapping:
            self.max_end = max(i.end for i in self.overlapping)
            self.min_start = min(i.start for i in self.overlapping)
        else:
            self.max_end = None
            self.min_start = None
        
        if self.left:
            left_max = self.left.get_max_end()
            left_min = self.left.get_min_start()
            if left_max is not None:
                self.max_end = max(self.max_end or left_max, left_max)
            if left_min is not None:
                self.min_start = min(self.min_start or left_min, left_min)
        
        if self.right:
            right_max = self.right.get_max_end()
            right_min = self.right.get_min_start()
            if right_max is not None:
                self.max_end = max(self.max_end or right_max, right_max)
            if right_min is not None:
                self.min_start = min(self.min_start or right_min, right_min)
    
    def get_max_end(self) -> Optional[T]:
        """获取子树中最大的区间终点"""
        return self.max_end
    
    def get_min_start(self) -> Optional[T]:
        """获取子树中最小的区间起点"""
        return self.min_start
    
    def add_interval(self, interval: Interval[T]):
        """向节点添加区间"""
        self.overlapping.append(interval)
        self.update_bounds()
    
    def remove_interval(self, interval: Interval[T]) -> bool:
        """从节点移除区间，返回是否成功"""
        try:
            self.overlapping.remove(interval)
            self.update_bounds()
            return True
        except ValueError:
            return False
    
    def is_leaf(self) -> bool:
        """检查是否为叶节点"""
        return self.left is None and self.right is None
    
    def height(self) -> int:
        """计算节点高度"""
        left_height = self.left.height() if self.left else 0
        right_height = self.right.height() if self.right else 0
        return 1 + max(left_height, right_height)
    
    def size(self) -> int:
        """计算子树中的节点数"""
        count = 1
        count += self.left.size() if self.left else 0
        count += self.right.size() if self.right else 0
        return count
    
    def interval_count(self) -> int:
        """计算子树中的区间总数"""
        count = len(self.overlapping)
        count += self.left.interval_count() if self.left else 0
        count += self.right.interval_count() if self.right else 0
        return count
    
    def collect_all(self) -> List[Interval[T]]:
        """收集子树中的所有区间"""
        result = list(self.overlapping)
        if self.left:
            result.extend(self.left.collect_all())
        if self.right:
            result.extend(self.right.collect_all())
        return result
    
    def __repr__(self) -> str:
        return f"IntervalNode(center={self.center}, intervals={len(self.overlapping)})"