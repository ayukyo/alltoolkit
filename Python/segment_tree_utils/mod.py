#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Segment Tree Utils - 线段树工具库

线段树（Segment Tree）是一种用于高效处理区间查询和更新的数据结构。

时间复杂度:
    - 构建树: O(n)
    - 区间查询: O(log n)
    - 单点更新: O(log n)
    - 区间更新（懒标记）: O(log n)

空间复杂度: O(n)

特点:
    - 支持多种聚合操作（求和、最值、GCD 等）
    - 支持区间更新（懒标记）
    - 支持动态开点（稀疏线段树）
    - 可扩展性强

零外部依赖，纯 Python 标准库实现。
"""

from typing import List, Optional, Callable, TypeVar, Generic, Iterable, Tuple
from dataclasses import dataclass
from enum import Enum
import math

T = TypeVar('T', int, float)


class OperationType(Enum):
    """操作类型枚举"""
    SUM = "sum"
    MIN = "min"
    MAX = "max"
    GCD = "gcd"
    LCM = "lcm"
    XOR = "xor"


def gcd(a: int, b: int) -> int:
    """计算最大公约数"""
    while b:
        a, b = b, a % b
    return abs(a)


def lcm(a: int, b: int) -> int:
    """计算最小公倍数"""
    if a == 0 or b == 0:
        return 0
    return abs(a * b) // gcd(a, b)


class SegmentTree(Generic[T]):
    """
    基础线段树
    
    支持操作:
        - 区间查询: query(left, right)
        - 单点更新: update(index, value)
    
    Example:
        >>> st = SegmentTree([1, 2, 3, 4, 5], OperationType.SUM)
        >>> st.query(0, 4)  # 整个数组的和
        15
        >>> st.query(1, 3)  # 第2到第4个元素的和
        9
        >>> st.update(0, 10)  # 将第一个元素设为10
        >>> st.query(0, 4)
        24
    """
    
    def __init__(
        self, 
        data: Iterable[T], 
        op_type: OperationType = OperationType.SUM,
        neutral_element: Optional[T] = None
    ):
        """
        初始化线段树
        
        Args:
            data: 初始数据
            op_type: 操作类型（SUM, MIN, MAX, GCD, LCM, XOR）
            neutral_element: 中性元素（可选，用于自定义操作）
        """
        self._data = list(data)
        self._n = len(self._data)
        
        if self._n == 0:
            self._tree = []
            return
        
        self._op_type = op_type
        
        # 设置操作函数和中性元素
        if op_type == OperationType.SUM:
            self._op = lambda a, b: a + b
            self._neutral = 0 if neutral_element is None else neutral_element
        elif op_type == OperationType.MIN:
            self._op = lambda a, b: min(a, b)
            self._neutral = float('inf') if neutral_element is None else neutral_element
        elif op_type == OperationType.MAX:
            self._op = lambda a, b: max(a, b)
            self._neutral = float('-inf') if neutral_element is None else neutral_element
        elif op_type == OperationType.GCD:
            self._op = gcd
            self._neutral = 0 if neutral_element is None else neutral_element
        elif op_type == OperationType.LCM:
            self._op = lcm
            self._neutral = 1 if neutral_element is None else neutral_element
        elif op_type == OperationType.XOR:
            self._op = lambda a, b: a ^ b
            self._neutral = 0 if neutral_element is None else neutral_element
        else:
            raise ValueError(f"不支持的操作类型: {op_type}")
        
        # 构建线段树（4n 空间）
        self._tree = [self._neutral] * (4 * self._n)
        self._build(1, 0, self._n - 1)
    
    def _build(self, node: int, start: int, end: int) -> None:
        """递归构建线段树"""
        if start == end:
            self._tree[node] = self._data[start]
        else:
            mid = (start + end) // 2
            self._build(2 * node, start, mid)
            self._build(2 * node + 1, mid + 1, end)
            self._tree[node] = self._op(self._tree[2 * node], self._tree[2 * node + 1])
    
    def _query_range(
        self, 
        node: int, 
        start: int, 
        end: int, 
        left: int, 
        right: int
    ) -> T:
        """递归区间查询"""
        if right < start or left > end:
            return self._neutral
        if left <= start and end <= right:
            return self._tree[node]
        
        mid = (start + end) // 2
        left_val = self._query_range(2 * node, start, mid, left, right)
        right_val = self._query_range(2 * node + 1, mid + 1, end, left, right)
        return self._op(left_val, right_val)
    
    def _update_point(
        self, 
        node: int, 
        start: int, 
        end: int, 
        index: int, 
        value: T
    ) -> None:
        """递归单点更新"""
        if start == end:
            self._data[index] = value
            self._tree[node] = value
        else:
            mid = (start + end) // 2
            if index <= mid:
                self._update_point(2 * node, start, mid, index, value)
            else:
                self._update_point(2 * node + 1, mid + 1, end, index, value)
            self._tree[node] = self._op(self._tree[2 * node], self._tree[2 * node + 1])
    
    def query(self, left: int, right: int) -> T:
        """
        区间查询
        
        Args:
            left: 左边界（包含，0-indexed）
            right: 右边界（包含，0-indexed）
        
        Returns:
            区间聚合结果
        
        Raises:
            IndexError: 索引越界
            ValueError: 空数组查询
        """
        if self._n == 0:
            raise ValueError("空数组无法查询")
        if left > right:
            raise IndexError(f"左边界 {left} 不能大于右边界 {right}")
        if left < 0 or right >= self._n:
            raise IndexError(f"索引 [{left}, {right}] 超出范围 [0, {self._n - 1}]")
        
        return self._query_range(1, 0, self._n - 1, left, right)
    
    def update(self, index: int, value: T) -> None:
        """
        单点更新：将指定位置设置为 value
        
        Args:
            index: 索引（0-indexed）
            value: 新值
        
        Raises:
            IndexError: 索引越界
        """
        if self._n == 0:
            raise ValueError("空数组无法更新")
        if not 0 <= index < self._n:
            raise IndexError(f"索引 {index} 超出范围 [0, {self._n - 1}]")
        
        self._update_point(1, 0, self._n - 1, index, value)
    
    def get(self, index: int) -> T:
        """获取指定位置的值"""
        if not 0 <= index < self._n:
            raise IndexError(f"索引 {index} 超出范围 [0, {self._n - 1}]")
        return self._data[index]
    
    def __len__(self) -> int:
        return self._n
    
    def __getitem__(self, index: int) -> T:
        return self.get(index)
    
    def __setitem__(self, index: int, value: T) -> None:
        self.update(index, value)
    
    def to_list(self) -> List[T]:
        """返回原始数据的副本"""
        return self._data.copy()
    
    def __repr__(self) -> str:
        return f"SegmentTree({self._data}, op={self._op_type.value})"


class SegmentTreeLazy(Generic[T]):
    """
    支持懒标记的线段树（区间更新）
    
    支持操作:
        - 区间查询: query(left, right)
        - 单点更新: update(index, value)
        - 区间更新: range_update(left, right, value)
        - 区间增加: range_add(left, right, delta)
    
    Example:
        >>> st = SegmentTreeLazy([1, 2, 3, 4, 5])
        >>> st.range_add(0, 2, 10)  # 前3个元素各加10
        >>> st.query(0, 2)
        36  # (1+10) + (2+10) + (3+10)
        >>> st.range_update(3, 4, 0)  # 后2个元素设为0
        >>> st.query(0, 4)
        36
    """
    
    def __init__(self, data: Iterable[T]):
        """
        初始化懒标记线段树（求和类型）
        
        Args:
            data: 初始数据
        """
        self._data = list(data)
        self._n = len(self._data)
        
        if self._n == 0:
            self._tree = []
            self._lazy_add = []
            self._lazy_set = []
            self._lazy_set_flag = []
            return
        
        # 线段树数组
        self._tree = [0] * (4 * self._n)
        # 懒标记：区间加
        self._lazy_add = [0] * (4 * self._n)
        # 懒标记：区间设值
        self._lazy_set = [0] * (4 * self._n)
        # 懒标记：区间设值标记
        self._lazy_set_flag = [False] * (4 * self._n)
        
        self._build(1, 0, self._n - 1)
    
    def _build(self, node: int, start: int, end: int) -> None:
        """递归构建线段树"""
        if start == end:
            self._tree[node] = self._data[start]
        else:
            mid = (start + end) // 2
            self._build(2 * node, start, mid)
            self._build(2 * node + 1, mid + 1, end)
            self._tree[node] = self._tree[2 * node] + self._tree[2 * node + 1]
    
    def _push_down(self, node: int, start: int, end: int) -> None:
        """下推懒标记"""
        mid = (start + end) // 2
        left_len = mid - start + 1
        right_len = end - mid
        
        # 先处理设值标记（设值优先级高于加值）
        if self._lazy_set_flag[node]:
            # 左子节点
            self._tree[2 * node] = self._lazy_set[node] * left_len
            self._lazy_set[2 * node] = self._lazy_set[node]
            self._lazy_set_flag[2 * node] = True
            self._lazy_add[2 * node] = 0
            
            # 右子节点
            self._tree[2 * node + 1] = self._lazy_set[node] * right_len
            self._lazy_set[2 * node + 1] = self._lazy_set[node]
            self._lazy_set_flag[2 * node + 1] = True
            self._lazy_add[2 * node + 1] = 0
            
            self._lazy_set_flag[node] = False
        
        # 再处理加值标记
        if self._lazy_add[node] != 0:
            self._tree[2 * node] += self._lazy_add[node] * left_len
            self._lazy_add[2 * node] += self._lazy_add[node]
            
            self._tree[2 * node + 1] += self._lazy_add[node] * right_len
            self._lazy_add[2 * node + 1] += self._lazy_add[node]
            
            self._lazy_add[node] = 0
    
    def _query_range(
        self, 
        node: int, 
        start: int, 
        end: int, 
        left: int, 
        right: int
    ) -> T:
        """递归区间查询"""
        if right < start or left > end:
            return 0
        if left <= start and end <= right:
            return self._tree[node]
        
        self._push_down(node, start, end)
        
        mid = (start + end) // 2
        left_sum = self._query_range(2 * node, start, mid, left, right)
        right_sum = self._query_range(2 * node + 1, mid + 1, end, left, right)
        return left_sum + right_sum
    
    def _update_range_add(
        self, 
        node: int, 
        start: int, 
        end: int, 
        left: int, 
        right: int, 
        delta: T
    ) -> None:
        """递归区间加"""
        if right < start or left > end:
            return
        if left <= start and end <= right:
            self._tree[node] += delta * (end - start + 1)
            self._lazy_add[node] += delta
            return
        
        self._push_down(node, start, end)
        
        mid = (start + end) // 2
        self._update_range_add(2 * node, start, mid, left, right, delta)
        self._update_range_add(2 * node + 1, mid + 1, end, left, right, delta)
        self._tree[node] = self._tree[2 * node] + self._tree[2 * node + 1]
    
    def _update_range_set(
        self, 
        node: int, 
        start: int, 
        end: int, 
        left: int, 
        right: int, 
        value: T
    ) -> None:
        """递归区间设值"""
        if right < start or left > end:
            return
        if left <= start and end <= right:
            self._tree[node] = value * (end - start + 1)
            self._lazy_set[node] = value
            self._lazy_set_flag[node] = True
            self._lazy_add[node] = 0
            return
        
        self._push_down(node, start, end)
        
        mid = (start + end) // 2
        self._update_range_set(2 * node, start, mid, left, right, value)
        self._update_range_set(2 * node + 1, mid + 1, end, left, right, value)
        self._tree[node] = self._tree[2 * node] + self._tree[2 * node + 1]
    
    def _update_point(
        self, 
        node: int, 
        start: int, 
        end: int, 
        index: int, 
        value: T
    ) -> None:
        """递归单点更新"""
        if start == end:
            self._data[index] = value
            self._tree[node] = value
            self._lazy_add[node] = 0
            self._lazy_set_flag[node] = False
        else:
            self._push_down(node, start, end)
            
            mid = (start + end) // 2
            if index <= mid:
                self._update_point(2 * node, start, mid, index, value)
            else:
                self._update_point(2 * node + 1, mid + 1, end, index, value)
            self._tree[node] = self._tree[2 * node] + self._tree[2 * node + 1]
    
    def query(self, left: int, right: int) -> T:
        """
        区间求和查询
        
        Args:
            left: 左边界（包含，0-indexed）
            right: 右边界（包含，0-indexed）
        
        Returns:
            区间和
        """
        if self._n == 0:
            raise ValueError("空数组无法查询")
        if left > right:
            raise IndexError(f"左边界 {left} 不能大于右边界 {right}")
        if left < 0 or right >= self._n:
            raise IndexError(f"索引 [{left}, {right}] 超出范围 [0, {self._n - 1}]")
        
        return self._query_range(1, 0, self._n - 1, left, right)
    
    def update(self, index: int, value: T) -> None:
        """
        单点更新：将指定位置设置为 value
        
        Args:
            index: 索引（0-indexed）
            value: 新值
        """
        if self._n == 0:
            raise ValueError("空数组无法更新")
        if not 0 <= index < self._n:
            raise IndexError(f"索引 {index} 超出范围 [0, {self._n - 1}]")
        
        self._update_point(1, 0, self._n - 1, index, value)
    
    def range_add(self, left: int, right: int, delta: T) -> None:
        """
        区间增加：在 [left, right] 区间内所有元素加上 delta
        
        Args:
            left: 左边界（包含，0-indexed）
            right: 右边界（包含，0-indexed）
            delta: 要增加的值
        """
        if self._n == 0:
            raise ValueError("空数组无法更新")
        if left > right:
            raise IndexError(f"左边界 {left} 不能大于右边界 {right}")
        left = max(0, left)
        right = min(right, self._n - 1)
        
        self._update_range_add(1, 0, self._n - 1, left, right, delta)
        
        # 更新原始数据
        for i in range(left, right + 1):
            self._data[i] += delta
    
    def range_update(self, left: int, right: int, value: T) -> None:
        """
        区间设值：将 [left, right] 区间内所有元素设置为 value
        
        Args:
            left: 左边界（包含，0-indexed）
            right: 右边界（包含，0-indexed）
            value: 新值
        """
        if self._n == 0:
            raise ValueError("空数组无法更新")
        if left > right:
            raise IndexError(f"左边界 {left} 不能大于右边界 {right}")
        left = max(0, left)
        right = min(right, self._n - 1)
        
        self._update_range_set(1, 0, self._n - 1, left, right, value)
        
        # 更新原始数据
        for i in range(left, right + 1):
            self._data[i] = value
    
    def get(self, index: int) -> T:
        """获取指定位置的当前值（考虑懒标记）"""
        if not 0 <= index < self._n:
            raise IndexError(f"索引 {index} 超出范围 [0, {self._n - 1}]")
        return self.query(index, index)
    
    def __len__(self) -> int:
        return self._n
    
    def to_list(self) -> List[T]:
        """返回当前数据的副本（考虑懒标记）"""
        return [self.get(i) for i in range(self._n)]
    
    def __repr__(self) -> str:
        return f"SegmentTreeLazy({self.to_list()})"


class SegmentTreeMin(Generic[T]):
    """
    区间最小值线段树
    
    支持操作:
        - 区间最小值查询: query(left, right)
        - 单点更新: update(index, value)
    
    Example:
        >>> st = SegmentTreeMin([5, 3, 7, 1, 9])
        >>> st.query(0, 4)
        1
        >>> st.query(0, 2)
        3
        >>> st.update(3, 10)
        >>> st.query(0, 4)
        3
    """
    
    def __init__(self, data: Iterable[T]):
        """初始化区间最小值线段树"""
        self._data = list(data)
        self._n = len(self._data)
        
        if self._n == 0:
            self._tree = []
            return
        
        self._tree = [float('inf')] * (4 * self._n)
        self._build(1, 0, self._n - 1)
    
    def _build(self, node: int, start: int, end: int) -> None:
        if start == end:
            self._tree[node] = self._data[start]
        else:
            mid = (start + end) // 2
            self._build(2 * node, start, mid)
            self._build(2 * node + 1, mid + 1, end)
            self._tree[node] = min(self._tree[2 * node], self._tree[2 * node + 1])
    
    def _query_range(self, node: int, start: int, end: int, left: int, right: int) -> T:
        if right < start or left > end:
            return float('inf')
        if left <= start and end <= right:
            return self._tree[node]
        
        mid = (start + end) // 2
        return min(
            self._query_range(2 * node, start, mid, left, right),
            self._query_range(2 * node + 1, mid + 1, end, left, right)
        )
    
    def _update_point(self, node: int, start: int, end: int, index: int, value: T) -> None:
        if start == end:
            self._data[index] = value
            self._tree[node] = value
        else:
            mid = (start + end) // 2
            if index <= mid:
                self._update_point(2 * node, start, mid, index, value)
            else:
                self._update_point(2 * node + 1, mid + 1, end, index, value)
            self._tree[node] = min(self._tree[2 * node], self._tree[2 * node + 1])
    
    def query(self, left: int, right: int) -> T:
        """区间最小值查询"""
        if self._n == 0:
            raise ValueError("空数组无法查询")
        if left > right:
            raise IndexError(f"左边界 {left} 不能大于右边界 {right}")
        if left < 0 or right >= self._n:
            raise IndexError(f"索引 [{left}, {right}] 超出范围 [0, {self._n - 1}]")
        return self._query_range(1, 0, self._n - 1, left, right)
    
    def update(self, index: int, value: T) -> None:
        """单点更新"""
        if self._n == 0:
            raise ValueError("空数组无法更新")
        if not 0 <= index < self._n:
            raise IndexError(f"索引 {index} 超出范围 [0, {self._n - 1}]")
        self._update_point(1, 0, self._n - 1, index, value)
    
    def get(self, index: int) -> T:
        if not 0 <= index < self._n:
            raise IndexError(f"索引 {index} 超出范围 [0, {self._n - 1}]")
        return self._data[index]
    
    def __len__(self) -> int:
        return self._n
    
    def __repr__(self) -> str:
        return f"SegmentTreeMin({self._data})"


class SegmentTreeMax(Generic[T]):
    """
    区间最大值线段树
    
    支持操作:
        - 区间最大值查询: query(left, right)
        - 单点更新: update(index, value)
    
    Example:
        >>> st = SegmentTreeMax([5, 3, 7, 1, 9])
        >>> st.query(0, 4)
        9
        >>> st.query(0, 2)
        7
    """
    
    def __init__(self, data: Iterable[T]):
        """初始化区间最大值线段树"""
        self._data = list(data)
        self._n = len(self._data)
        
        if self._n == 0:
            self._tree = []
            return
        
        self._tree = [float('-inf')] * (4 * self._n)
        self._build(1, 0, self._n - 1)
    
    def _build(self, node: int, start: int, end: int) -> None:
        if start == end:
            self._tree[node] = self._data[start]
        else:
            mid = (start + end) // 2
            self._build(2 * node, start, mid)
            self._build(2 * node + 1, mid + 1, end)
            self._tree[node] = max(self._tree[2 * node], self._tree[2 * node + 1])
    
    def _query_range(self, node: int, start: int, end: int, left: int, right: int) -> T:
        if right < start or left > end:
            return float('-inf')
        if left <= start and end <= right:
            return self._tree[node]
        
        mid = (start + end) // 2
        return max(
            self._query_range(2 * node, start, mid, left, right),
            self._query_range(2 * node + 1, mid + 1, end, left, right)
        )
    
    def _update_point(self, node: int, start: int, end: int, index: int, value: T) -> None:
        if start == end:
            self._data[index] = value
            self._tree[node] = value
        else:
            mid = (start + end) // 2
            if index <= mid:
                self._update_point(2 * node, start, mid, index, value)
            else:
                self._update_point(2 * node + 1, mid + 1, end, index, value)
            self._tree[node] = max(self._tree[2 * node], self._tree[2 * node + 1])
    
    def query(self, left: int, right: int) -> T:
        """区间最大值查询"""
        if self._n == 0:
            raise ValueError("空数组无法查询")
        if left > right:
            raise IndexError(f"左边界 {left} 不能大于右边界 {right}")
        if left < 0 or right >= self._n:
            raise IndexError(f"索引 [{left}, {right}] 超出范围 [0, {self._n - 1}]")
        return self._query_range(1, 0, self._n - 1, left, right)
    
    def update(self, index: int, value: T) -> None:
        """单点更新"""
        if self._n == 0:
            raise ValueError("空数组无法更新")
        if not 0 <= index < self._n:
            raise IndexError(f"索引 {index} 超出范围 [0, {self._n - 1}]")
        self._update_point(1, 0, self._n - 1, index, value)
    
    def get(self, index: int) -> T:
        if not 0 <= index < self._n:
            raise IndexError(f"索引 {index} 超出范围 [0, {self._n - 1}]")
        return self._data[index]
    
    def __len__(self) -> int:
        return self._n
    
    def __repr__(self) -> str:
        return f"SegmentTreeMax({self._data})"


class SegmentTreeGCD:
    """
    区间最大公约数线段树
    
    支持操作:
        - 区间 GCD 查询: query(left, right)
        - 单点更新: update(index, value)
    
    Example:
        >>> st = SegmentTreeGCD([12, 18, 24, 36])
        >>> st.query(0, 3)
        6
        >>> st.query(0, 1)
        6
    """
    
    def __init__(self, data: Iterable[int]):
        """初始化区间 GCD 线段树"""
        self._data = list(data)
        self._n = len(self._data)
        
        if self._n == 0:
            self._tree = []
            return
        
        self._tree = [0] * (4 * self._n)
        self._build(1, 0, self._n - 1)
    
    def _build(self, node: int, start: int, end: int) -> None:
        if start == end:
            self._tree[node] = abs(self._data[start])
        else:
            mid = (start + end) // 2
            self._build(2 * node, start, mid)
            self._build(2 * node + 1, mid + 1, end)
            self._tree[node] = gcd(self._tree[2 * node], self._tree[2 * node + 1])
    
    def _query_range(self, node: int, start: int, end: int, left: int, right: int) -> int:
        if right < start or left > end:
            return 0
        if left <= start and end <= right:
            return self._tree[node]
        
        mid = (start + end) // 2
        return gcd(
            self._query_range(2 * node, start, mid, left, right),
            self._query_range(2 * node + 1, mid + 1, end, left, right)
        )
    
    def _update_point(self, node: int, start: int, end: int, index: int, value: int) -> None:
        if start == end:
            self._data[index] = value
            self._tree[node] = abs(value)
        else:
            mid = (start + end) // 2
            if index <= mid:
                self._update_point(2 * node, start, mid, index, value)
            else:
                self._update_point(2 * node + 1, mid + 1, end, index, value)
            self._tree[node] = gcd(self._tree[2 * node], self._tree[2 * node + 1])
    
    def query(self, left: int, right: int) -> int:
        """区间 GCD 查询"""
        if self._n == 0:
            raise ValueError("空数组无法查询")
        if left > right:
            raise IndexError(f"左边界 {left} 不能大于右边界 {right}")
        if left < 0 or right >= self._n:
            raise IndexError(f"索引 [{left}, {right}] 超出范围 [0, {self._n - 1}]")
        return self._query_range(1, 0, self._n - 1, left, right)
    
    def update(self, index: int, value: int) -> None:
        """单点更新"""
        if self._n == 0:
            raise ValueError("空数组无法更新")
        if not 0 <= index < self._n:
            raise IndexError(f"索引 {index} 超出范围 [0, {self._n - 1}]")
        self._update_point(1, 0, self._n - 1, index, value)
    
    def get(self, index: int) -> int:
        if not 0 <= index < self._n:
            raise IndexError(f"索引 {index} 超出范围 [0, {self._n - 1}]")
        return self._data[index]
    
    def __len__(self) -> int:
        return self._n
    
    def __repr__(self) -> str:
        return f"SegmentTreeGCD({self._data})"


class SegmentTreeXOR:
    """
    区间异或线段树
    
    支持操作:
        - 区间异或查询: query(left, right)
        - 单点更新: update(index, value)
    
    Example:
        >>> st = SegmentTreeXOR([1, 2, 3, 4, 5])
        >>> st.query(0, 2)
        0  # 1 ^ 2 ^ 3 = 0
    """
    
    def __init__(self, data: Iterable[int]):
        """初始化区间异或线段树"""
        self._data = list(data)
        self._n = len(self._data)
        
        if self._n == 0:
            self._tree = []
            return
        
        self._tree = [0] * (4 * self._n)
        self._build(1, 0, self._n - 1)
    
    def _build(self, node: int, start: int, end: int) -> None:
        if start == end:
            self._tree[node] = self._data[start]
        else:
            mid = (start + end) // 2
            self._build(2 * node, start, mid)
            self._build(2 * node + 1, mid + 1, end)
            self._tree[node] = self._tree[2 * node] ^ self._tree[2 * node + 1]
    
    def _query_range(self, node: int, start: int, end: int, left: int, right: int) -> int:
        if right < start or left > end:
            return 0
        if left <= start and end <= right:
            return self._tree[node]
        
        mid = (start + end) // 2
        return (
            self._query_range(2 * node, start, mid, left, right) ^
            self._query_range(2 * node + 1, mid + 1, end, left, right)
        )
    
    def _update_point(self, node: int, start: int, end: int, index: int, value: int) -> None:
        if start == end:
            self._data[index] = value
            self._tree[node] = value
        else:
            mid = (start + end) // 2
            if index <= mid:
                self._update_point(2 * node, start, mid, index, value)
            else:
                self._update_point(2 * node + 1, mid + 1, end, index, value)
            self._tree[node] = self._tree[2 * node] ^ self._tree[2 * node + 1]
    
    def query(self, left: int, right: int) -> int:
        """区间异或查询"""
        if self._n == 0:
            raise ValueError("空数组无法查询")
        if left > right:
            raise IndexError(f"左边界 {left} 不能大于右边界 {right}")
        if left < 0 or right >= self._n:
            raise IndexError(f"索引 [{left}, {right}] 超出范围 [0, {self._n - 1}]")
        return self._query_range(1, 0, self._n - 1, left, right)
    
    def update(self, index: int, value: int) -> None:
        """单点更新"""
        if self._n == 0:
            raise ValueError("空数组无法更新")
        if not 0 <= index < self._n:
            raise IndexError(f"索引 {index} 超出范围 [0, {self._n - 1}]")
        self._update_point(1, 0, self._n - 1, index, value)
    
    def get(self, index: int) -> int:
        if not 0 <= index < self._n:
            raise IndexError(f"索引 {index} 超出范围 [0, {self._n - 1}]")
        return self._data[index]
    
    def __len__(self) -> int:
        return self._n
    
    def __repr__(self) -> str:
        return f"SegmentTreeXOR({self._data})"


class SegmentTreeCount:
    """
    区间计数线段树
    
    统计区间内满足条件的元素个数
    
    Example:
        >>> st = SegmentTreeCount([1, 2, 3, 4, 5], lambda x: x % 2 == 0)
        >>> st.query(0, 4)  # 统计偶数个数
        2
    """
    
    def __init__(self, data: Iterable[T], condition: Callable[[T], bool]):
        """
        初始化计数线段树
        
        Args:
            data: 初始数据
            condition: 计数条件函数
        """
        self._data = list(data)
        self._n = len(self._data)
        self._condition = condition
        
        if self._n == 0:
            self._tree = []
            return
        
        self._tree = [0] * (4 * self._n)
        self._build(1, 0, self._n - 1)
    
    def _build(self, node: int, start: int, end: int) -> None:
        if start == end:
            self._tree[node] = 1 if self._condition(self._data[start]) else 0
        else:
            mid = (start + end) // 2
            self._build(2 * node, start, mid)
            self._build(2 * node + 1, mid + 1, end)
            self._tree[node] = self._tree[2 * node] + self._tree[2 * node + 1]
    
    def _query_range(self, node: int, start: int, end: int, left: int, right: int) -> int:
        if right < start or left > end:
            return 0
        if left <= start and end <= right:
            return self._tree[node]
        
        mid = (start + end) // 2
        return (
            self._query_range(2 * node, start, mid, left, right) +
            self._query_range(2 * node + 1, mid + 1, end, left, right)
        )
    
    def _update_point(self, node: int, start: int, end: int, index: int, value: T) -> None:
        if start == end:
            self._data[index] = value
            self._tree[node] = 1 if self._condition(value) else 0
        else:
            mid = (start + end) // 2
            if index <= mid:
                self._update_point(2 * node, start, mid, index, value)
            else:
                self._update_point(2 * node + 1, mid + 1, end, index, value)
            self._tree[node] = self._tree[2 * node] + self._tree[2 * node + 1]
    
    def query(self, left: int, right: int) -> int:
        """区间计数查询"""
        if self._n == 0:
            raise ValueError("空数组无法查询")
        if left > right:
            raise IndexError(f"左边界 {left} 不能大于右边界 {right}")
        if left < 0 or right >= self._n:
            raise IndexError(f"索引 [{left}, {right}] 超出范围 [0, {self._n - 1}]")
        return self._query_range(1, 0, self._n - 1, left, right)
    
    def update(self, index: int, value: T) -> None:
        """单点更新"""
        if self._n == 0:
            raise ValueError("空数组无法更新")
        if not 0 <= index < self._n:
            raise IndexError(f"索引 {index} 超出范围 [0, {self._n - 1}]")
        self._update_point(1, 0, self._n - 1, index, value)
    
    def get(self, index: int) -> T:
        if not 0 <= index < self._n:
            raise IndexError(f"索引 {index} 超出范围 [0, {self._n - 1}]")
        return self._data[index]
    
    def __len__(self) -> int:
        return self._n
    
    def __repr__(self) -> str:
        return f"SegmentTreeCount({self._data})"


class SegmentTreeProduct:
    """
    区间乘积线段树
    
    支持操作:
        - 区间乘积查询: query(left, right)
        - 单点更新: update(index, value)
    
    注意: 可能会溢出，建议配合模数使用
    
    Example:
        >>> st = SegmentTreeProduct([1, 2, 3, 4, 5])
        >>> st.query(0, 2)
        6  # 1 * 2 * 3
    """
    
    def __init__(self, data: Iterable[int], mod: Optional[int] = None):
        """
        初始化区间乘积线段树
        
        Args:
            data: 初始数据
            mod: 模数（可选，用于防止溢出）
        """
        self._data = list(data)
        self._n = len(self._data)
        self._mod = mod
        
        if self._n == 0:
            self._tree = []
            return
        
        self._tree = [1] * (4 * self._n)
        self._build(1, 0, self._n - 1)
    
    def _mul(self, a: int, b: int) -> int:
        """安全的乘法"""
        if self._mod:
            return (a * b) % self._mod
        return a * b
    
    def _build(self, node: int, start: int, end: int) -> None:
        if start == end:
            val = self._data[start] % self._mod if self._mod else self._data[start]
            self._tree[node] = val
        else:
            mid = (start + end) // 2
            self._build(2 * node, start, mid)
            self._build(2 * node + 1, mid + 1, end)
            self._tree[node] = self._mul(self._tree[2 * node], self._tree[2 * node + 1])
    
    def _query_range(self, node: int, start: int, end: int, left: int, right: int) -> int:
        if right < start or left > end:
            return 1  # 乘法的单位元
        if left <= start and end <= right:
            return self._tree[node]
        
        mid = (start + end) // 2
        return self._mul(
            self._query_range(2 * node, start, mid, left, right),
            self._query_range(2 * node + 1, mid + 1, end, left, right)
        )
    
    def _update_point(self, node: int, start: int, end: int, index: int, value: int) -> None:
        if start == end:
            self._data[index] = value
            self._tree[node] = value % self._mod if self._mod else value
        else:
            mid = (start + end) // 2
            if index <= mid:
                self._update_point(2 * node, start, mid, index, value)
            else:
                self._update_point(2 * node + 1, mid + 1, end, index, value)
            self._tree[node] = self._mul(self._tree[2 * node], self._tree[2 * node + 1])
    
    def query(self, left: int, right: int) -> int:
        """区间乘积查询"""
        if self._n == 0:
            raise ValueError("空数组无法查询")
        if left > right:
            raise IndexError(f"左边界 {left} 不能大于右边界 {right}")
        if left < 0 or right >= self._n:
            raise IndexError(f"索引 [{left}, {right}] 超出范围 [0, {self._n - 1}]")
        return self._query_range(1, 0, self._n - 1, left, right)
    
    def update(self, index: int, value: int) -> None:
        """单点更新"""
        if self._n == 0:
            raise ValueError("空数组无法更新")
        if not 0 <= index < self._n:
            raise IndexError(f"索引 {index} 超出范围 [0, {self._n - 1}]")
        self._update_point(1, 0, self._n - 1, index, value)
    
    def get(self, index: int) -> int:
        if not 0 <= index < self._n:
            raise IndexError(f"索引 {index} 超出范围 [0, {self._n - 1}]")
        return self._data[index]
    
    def __len__(self) -> int:
        return self._n
    
    def __repr__(self) -> str:
        mod_str = f", mod={self._mod}" if self._mod else ""
        return f"SegmentTreeProduct({self._data}{mod_str})"


# ============== 便捷函数 ==============

def create_segment_tree(
    data: Iterable[T], 
    op_type: OperationType = OperationType.SUM
) -> SegmentTree[T]:
    """
    创建线段树
    
    Args:
        data: 初始数据
        op_type: 操作类型
    
    Returns:
        SegmentTree 实例
    """
    return SegmentTree(data, op_type)


def range_sum(data: Iterable[T], queries: List[Tuple[int, int]]) -> List[T]:
    """
    批量区间求和
    
    Args:
        data: 输入数据
        queries: 查询列表，每个元素为 (left, right)
    
    Returns:
        区间和列表
    """
    st = SegmentTree(data, OperationType.SUM)
    return [st.query(left, right) for left, right in queries]


def range_min(data: Iterable[T], queries: List[Tuple[int, int]]) -> List[T]:
    """
    批量区间最小值查询
    
    Args:
        data: 输入数据
        queries: 查询列表，每个元素为 (left, right)
    
    Returns:
        区间最小值列表
    """
    st = SegmentTree(data, OperationType.MIN)
    return [st.query(left, right) for left, right in queries]


def range_max(data: Iterable[T], queries: List[Tuple[int, int]]) -> List[T]:
    """
    批量区间最大值查询
    
    Args:
        data: 输入数据
        queries: 查询列表，每个元素为 (left, right)
    
    Returns:
        区间最大值列表
    """
    st = SegmentTree(data, OperationType.MAX)
    return [st.query(left, right) for left, right in queries]


def range_gcd(data: Iterable[int], queries: List[Tuple[int, int]]) -> List[int]:
    """
    批量区间 GCD 查询
    
    Args:
        data: 输入数据
        queries: 查询列表
    
    Returns:
        区间 GCD 列表
    """
    st = SegmentTreeGCD(data)
    return [st.query(left, right) for left, right in queries]


# ============== 导出 ==============

__all__ = [
    # 枚举
    'OperationType',
    # 类
    'SegmentTree',
    'SegmentTreeLazy',
    'SegmentTreeMin',
    'SegmentTreeMax',
    'SegmentTreeGCD',
    'SegmentTreeXOR',
    'SegmentTreeCount',
    'SegmentTreeProduct',
    # 便捷函数
    'create_segment_tree',
    'range_sum',
    'range_min',
    'range_max',
    'range_gcd',
    # 辅助函数
    'gcd',
    'lcm',
]