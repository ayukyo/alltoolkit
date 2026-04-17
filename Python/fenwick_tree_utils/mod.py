#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Fenwick Tree Utils - 树状数组工具库

树状数组（Fenwick Tree，又称 Binary Indexed Tree）是一种用于高效处理
前缀和查询和单点更新的数据结构。

时间复杂度:
    - 构建树: O(n)
    - 前缀和查询: O(log n)
    - 单点更新: O(log n)
    - 区间和查询: O(log n)
    - 区间更新 + 单点查询: O(log n) (差分树状数组)

空间复杂度: O(n)

特点:
    - 代码简洁，常数因子小
    - 适合动态前缀和场景
    - 可扩展支持区间更新

零外部依赖，纯 Python 标准库实现。
"""

from typing import List, Optional, Callable, TypeVar, Generic, Iterable
from dataclasses import dataclass

T = TypeVar('T', int, float)


class FenwickTree(Generic[T]):
    """
    树状数组（Fenwick Tree / Binary Indexed Tree）
    
    支持操作:
        - 单点更新: add(index, delta)
        - 前缀和查询: prefix_sum(index)
        - 区间和查询: range_sum(left, right)
    
    Example:
        >>> ft = FenwickTree([1, 2, 3, 4, 5])
        >>> ft.prefix_sum(2)  # 前三个元素的和
        6
        >>> ft.range_sum(1, 3)  # 第2到第4个元素的和
        9
        >>> ft.add(0, 10)  # 第一个元素加10
        >>> ft.prefix_sum(0)
        11
    """
    
    def __init__(self, data: Optional[Iterable[T]] = None, size: int = 0):
        """
        初始化树状数组
        
        Args:
            data: 初始数据（可选）
            size: 数组大小（当 data 为 None 时使用）
        """
        if data is not None:
            self._data = list(data)
            self._size = len(self._data)
        else:
            self._data = [0] * size
            self._size = size
        
        # 树状数组（1-indexed）
        self._tree = [0] * (self._size + 1)
        
        # 从原始数据构建树
        if data is not None:
            for i in range(self._size):
                self._add_to_tree(i, self._data[i])
    
    def _lsb(self, index: int) -> int:
        """
        计算 least significant bit（最低有效位）
        即 index 的二进制表示中最低的 1 及其后面的 0 组成的数
        
        Example:
            _lsb(6) = 2  (6 = 110b, lsb = 10b = 2)
            _lsb(8) = 8  (8 = 1000b, lsb = 1000b = 8)
        """
        return index & (-index)
    
    def _add_to_tree(self, index: int, delta: T) -> None:
        """
        在树状数组中添加 delta
        
        Args:
            index: 原始数组索引（0-indexed）
            delta: 要添加的值
        """
        i = index + 1  # 转换为 1-indexed
        while i <= self._size:
            self._tree[i] += delta
            i += self._lsb(i)
    
    def add(self, index: int, delta: T) -> None:
        """
        单点更新：将 delta 加到指定位置
        
        Args:
            index: 索引（0-indexed）
            delta: 要添加的值
        
        Raises:
            IndexError: 索引越界
        """
        if not 0 <= index < self._size:
            raise IndexError(f"索引 {index} 超出范围 [0, {self._size})")
        
        self._data[index] += delta
        self._add_to_tree(index, delta)
    
    def set(self, index: int, value: T) -> None:
        """
        单点设置：将指定位置设置为 value
        
        Args:
            index: 索引（0-indexed）
            value: 新值
        """
        if not 0 <= index < self._size:
            raise IndexError(f"索引 {index} 超出范围 [0, {self._size})")
        
        delta = value - self._data[index]
        self._data[index] = value
        self._add_to_tree(index, delta)
    
    def prefix_sum(self, index: int) -> T:
        """
        前缀和查询：计算 [0, index] 区间的和
        
        Args:
            index: 结束索引（包含，0-indexed）
        
        Returns:
            前缀和
        
        Raises:
            IndexError: 索引越界
        """
        if index < 0:
            return 0
        if index >= self._size:
            index = self._size - 1
        
        result = 0
        i = index + 1  # 转换为 1-indexed
        while i > 0:
            result += self._tree[i]
            i -= self._lsb(i)
        return result
    
    def range_sum(self, left: int, right: int) -> T:
        """
        区间和查询：计算 [left, right] 区间的和
        
        Args:
            left: 左边界（包含，0-indexed）
            right: 右边界（包含，0-indexed）
        
        Returns:
            区间和
        
        Raises:
            IndexError: 索引越界或 left > right
        """
        if left > right:
            raise IndexError(f"左边界 {left} 不能大于右边界 {right}")
        if left < 0 or right >= self._size:
            raise IndexError(f"索引超出范围 [0, {self._size})")
        
        if left == 0:
            return self.prefix_sum(right)
        return self.prefix_sum(right) - self.prefix_sum(left - 1)
    
    def get(self, index: int) -> T:
        """
        获取指定位置的值
        
        Args:
            index: 索引（0-indexed）
        
        Returns:
            该位置的值
        """
        if not 0 <= index < self._size:
            raise IndexError(f"索引 {index} 超出范围 [0, {self._size})")
        return self._data[index]
    
    def __len__(self) -> int:
        return self._size
    
    def __getitem__(self, index: int) -> T:
        return self.get(index)
    
    def __setitem__(self, index: int, value: T) -> None:
        self.set(index, value)
    
    def to_list(self) -> List[T]:
        """返回原始数据的副本"""
        return self._data.copy()
    
    def __repr__(self) -> str:
        return f"FenwickTree({self._data})"


class FenwickTreeRangeUpdate(Generic[T]):
    """
    支持区间更新的树状数组（使用差分数组）
    
    支持操作:
        - 区间更新: range_add(left, right, delta)
        - 单点查询: get(index)
        - 前缀和查询: prefix_sum(index)
    
    原理:
        使用两个树状数组维护差分数组，实现区间更新 O(log n)，单点查询 O(log n)
    
    Example:
        >>> ft = FenwickTreeRangeUpdate(5)
        >>> ft.range_add(0, 2, 10)  # [10, 10, 10, 0, 0]
        >>> ft.range_add(1, 3, 5)   # [10, 15, 15, 5, 0]
        >>> ft.get(1)
        15
        >>> ft.prefix_sum(3)
        45
    """
    
    def __init__(self, size: int):
        """
        初始化区间更新树状数组
        
        Args:
            size: 数组大小
        """
        self._size = size
        self._tree1 = [0] * (size + 1)  # 维护 D[i]
        self._tree2 = [0] * (size + 1)  # 维护 (i-1) * D[i]
    
    def _lsb(self, index: int) -> int:
        """计算 least significant bit"""
        return index & (-index)
    
    def _add(self, tree: List[T], index: int, delta: T) -> None:
        """在指定树中添加 delta"""
        i = index
        while i <= self._size:
            tree[i] += delta
            i += self._lsb(i)
    
    def _prefix_sum_tree(self, tree: List[T], index: int) -> T:
        """计算指定树的前缀和"""
        result = 0
        i = index
        while i > 0:
            result += tree[i]
            i -= self._lsb(i)
        return result
    
    def _internal_add(self, left: int, right: int, delta: T) -> None:
        """
        内部方法：在 [left, right] 区间添加 delta
        使用差分技术
        """
        # 对于差分数组 D，区间 [l, r] 加 x 等价于:
        # D[l] += x, D[r+1] -= x
        self._add(self._tree1, left, delta)
        self._add(self._tree1, right + 1, -delta)
        self._add(self._tree2, left, delta * (left - 1))
        self._add(self._tree2, right + 1, -delta * right)
    
    def range_add(self, left: int, right: int, delta: T) -> None:
        """
        区间更新：在 [left, right] 区间内所有元素加上 delta
        
        Args:
            left: 左边界（包含，0-indexed）
            right: 右边界（包含，0-indexed）
            delta: 要添加的值
        
        Raises:
            IndexError: 索引越界
        """
        if not 0 <= left <= right < self._size:
            raise IndexError(f"索引 [{left}, {right}] 超出范围 [0, {self._size})")
        
        # 转换为 1-indexed
        l = left + 1
        r = right + 1
        self._internal_add(l, r, delta)
    
    def prefix_sum(self, index: int) -> T:
        """
        前缀和查询：计算 [0, index] 区间的和
        
        Args:
            index: 结束索引（包含，0-indexed）
        
        Returns:
            前缀和
        """
        if index < 0:
            return 0
        if index >= self._size:
            index = self._size - 1
        
        i = index + 1  # 转换为 1-indexed
        return (self._prefix_sum_tree(self._tree1, i) * i - 
                self._prefix_sum_tree(self._tree2, i))
    
    def range_sum(self, left: int, right: int) -> T:
        """
        区间和查询：计算 [left, right] 区间的和
        
        Args:
            left: 左边界（包含，0-indexed）
            right: 右边界（包含，0-indexed）
        
        Returns:
            区间和
        """
        if left == 0:
            return self.prefix_sum(right)
        return self.prefix_sum(right) - self.prefix_sum(left - 1)
    
    def get(self, index: int) -> T:
        """
        单点查询：获取指定位置的值
        
        Args:
            index: 索引（0-indexed）
        
        Returns:
            该位置的值
        """
        if not 0 <= index < self._size:
            raise IndexError(f"索引 {index} 超出范围 [0, {self._size})")
        
        return self.prefix_sum(index) - (self.prefix_sum(index - 1) if index > 0 else 0)
    
    def __len__(self) -> int:
        return self._size
    
    def __repr__(self) -> str:
        return f"FenwickTreeRangeUpdate(size={self._size})"


class FenwickTree2D(Generic[T]):
    """
    二维树状数组
    
    支持操作:
        - 单点更新: add(row, col, delta)
        - 前缀和查询: prefix_sum(row, col)
        - 区间和查询: range_sum(r1, c1, r2, c2)
    
    时间复杂度: O(log(m) * log(n))，其中 m x n 是矩阵大小
    
    Example:
        >>> ft = FenwickTree2D(3, 3)
        >>> ft.add(1, 1, 10)
        >>> ft.prefix_sum(2, 2)
        10
        >>> ft.range_sum(0, 0, 2, 2)
        10
    """
    
    def __init__(self, rows: int, cols: int):
        """
        初始化二维树状数组
        
        Args:
            rows: 行数
            cols: 列数
        """
        self._rows = rows
        self._cols = cols
        # 原始数据
        self._data = [[0] * cols for _ in range(rows)]
        # 树状数组（1-indexed）
        self._tree = [[0] * (cols + 1) for _ in range(rows + 1)]
    
    def _lsb(self, index: int) -> int:
        """计算 least significant bit"""
        return index & (-index)
    
    def add(self, row: int, col: int, delta: T) -> None:
        """
        单点更新：将 delta 加到指定位置
        
        Args:
            row: 行索引（0-indexed）
            col: 列索引（0-indexed）
            delta: 要添加的值
        """
        if not (0 <= row < self._rows and 0 <= col < self._cols):
            raise IndexError(f"索引 ({row}, {col}) 超出范围")
        
        self._data[row][col] += delta
        
        r = row + 1  # 转换为 1-indexed
        while r <= self._rows:
            c = col + 1
            while c <= self._cols:
                self._tree[r][c] += delta
                c += self._lsb(c)
            r += self._lsb(r)
    
    def set(self, row: int, col: int, value: T) -> None:
        """
        单点设置：将指定位置设置为 value
        
        Args:
            row: 行索引（0-indexed）
            col: 列索引（0-indexed）
            value: 新值
        """
        if not (0 <= row < self._rows and 0 <= col < self._cols):
            raise IndexError(f"索引 ({row}, {col}) 超出范围")
        
        delta = value - self._data[row][col]
        self.add(row, col, delta)
    
    def prefix_sum(self, row: int, col: int) -> T:
        """
        前缀和查询：计算 [0,0] 到 [row,col] 的矩形和
        
        Args:
            row: 行索引（包含，0-indexed）
            col: 列索引（包含，0-indexed）
        
        Returns:
            前缀和
        """
        if row < 0 or col < 0:
            return 0
        row = min(row, self._rows - 1)
        col = min(col, self._cols - 1)
        
        result = 0
        r = row + 1
        while r > 0:
            c = col + 1
            while c > 0:
                result += self._tree[r][c]
                c -= self._lsb(c)
            r -= self._lsb(r)
        return result
    
    def range_sum(self, r1: int, c1: int, r2: int, c2: int) -> T:
        """
        区间和查询：计算 [r1,c1] 到 [r2,c2] 的矩形和
        
        Args:
            r1: 左上行索引（包含）
            c1: 左上列索引（包含）
            r2: 右下行索引（包含）
            c2: 右下列索引（包含）
        
        Returns:
            区间和
        """
        if r1 > r2 or c1 > c2:
            raise IndexError("无效的区间范围")
        
        # 使用容斥原理
        return (self.prefix_sum(r2, c2)
                - self.prefix_sum(r1 - 1, c2)
                - self.prefix_sum(r2, c1 - 1)
                + self.prefix_sum(r1 - 1, c1 - 1))
    
    def get(self, row: int, col: int) -> T:
        """获取指定位置的值"""
        if not (0 <= row < self._rows and 0 <= col < self._cols):
            raise IndexError(f"索引 ({row}, {col}) 超出范围")
        return self._data[row][col]
    
    @property
    def shape(self) -> tuple:
        """返回矩阵形状"""
        return (self._rows, self._cols)
    
    def __repr__(self) -> str:
        return f"FenwickTree2D(rows={self._rows}, cols={self._cols})"


class FenwickTreeMax(Generic[T]):
    """
    支持前缀最大值的树状数组
    
    支持操作:
        - 单点更新（只能增大）: update(index, value)
        - 前缀最大值查询: prefix_max(index)
    
    注意: 只能更新为更大的值，不能减小
    
    Example:
        >>> ft = FenwickTreeMax(5)
        >>> ft.update(0, 3)
        >>> ft.update(2, 5)
        >>> ft.prefix_max(4)
        5
    """
    
    def __init__(self, size: int, initial: T = 0):
        """
        初始化最大值树状数组
        
        Args:
            size: 数组大小
            initial: 初始值（用于比较）
        """
        self._size = size
        self._initial = initial
        self._data = [initial] * size
        self._tree = [initial] * (size + 1)
    
    def _lsb(self, index: int) -> int:
        """计算 least significant bit"""
        return index & (-index)
    
    def update(self, index: int, value: T) -> bool:
        """
        单点更新：将指定位置更新为 value（只有当 value 更大时才更新）
        
        Args:
            index: 索引（0-indexed）
            value: 新值
        
        Returns:
            是否更新成功（value 是否大于原值）
        """
        if not 0 <= index < self._size:
            raise IndexError(f"索引 {index} 超出范围 [0, {self._size})")
        
        if value <= self._data[index]:
            return False
        
        self._data[index] = value
        
        i = index + 1
        while i <= self._size:
            if value > self._tree[i]:
                self._tree[i] = value
            i += self._lsb(i)
        
        return True
    
    def prefix_max(self, index: int) -> T:
        """
        前缀最大值查询：计算 [0, index] 区间的最大值
        
        Args:
            index: 结束索引（包含，0-indexed）
        
        Returns:
            前缀最大值
        """
        if index < 0:
            return self._initial
        if index >= self._size:
            index = self._size - 1
        
        result = self._initial
        i = index + 1
        while i > 0:
            if self._tree[i] > result:
                result = self._tree[i]
            i -= self._lsb(i)
        return result
    
    def get(self, index: int) -> T:
        """获取指定位置的值"""
        if not 0 <= index < self._size:
            raise IndexError(f"索引 {index} 超出范围 [0, {self._size})")
        return self._data[index]
    
    def __len__(self) -> int:
        return self._size
    
    def __repr__(self) -> str:
        return f"FenwickTreeMax(size={self._size})"


class FenwickTreeMin(Generic[T]):
    """
    支持前缀最小值的树状数组
    
    支持操作:
        - 单点更新（只能减小）: update(index, value)
        - 前缀最小值查询: prefix_min(index)
    
    注意: 只能更新为更小的值，不能增大
    
    Example:
        >>> ft = FenwickTreeMin(5, initial=float('inf'))
        >>> ft.update(0, 3)
        >>> ft.update(2, 1)
        >>> ft.prefix_min(4)
        1
    """
    
    def __init__(self, size: int, initial: T = float('inf')):
        """
        初始化最小值树状数组
        
        Args:
            size: 数组大小
            initial: 初始值（用于比较，默认为正无穷）
        """
        self._size = size
        self._initial = initial
        self._data = [initial] * size
        self._tree = [initial] * (size + 1)
    
    def _lsb(self, index: int) -> int:
        """计算 least significant bit"""
        return index & (-index)
    
    def update(self, index: int, value: T) -> bool:
        """
        单点更新：将指定位置更新为 value（只有当 value 更小时才更新）
        
        Args:
            index: 索引（0-indexed）
            value: 新值
        
        Returns:
            是否更新成功（value 是否小于原值）
        """
        if not 0 <= index < self._size:
            raise IndexError(f"索引 {index} 超出范围 [0, {self._size})")
        
        if value >= self._data[index]:
            return False
        
        self._data[index] = value
        
        i = index + 1
        while i <= self._size:
            if value < self._tree[i]:
                self._tree[i] = value
            i += self._lsb(i)
        
        return True
    
    def prefix_min(self, index: int) -> T:
        """
        前缀最小值查询：计算 [0, index] 区间的最小值
        
        Args:
            index: 结束索引（包含，0-indexed）
        
        Returns:
            前缀最小值
        """
        if index < 0:
            return self._initial
        if index >= self._size:
            index = self._size - 1
        
        result = self._initial
        i = index + 1
        while i > 0:
            if self._tree[i] < result:
                result = self._tree[i]
            i -= self._lsb(i)
        return result
    
    def get(self, index: int) -> T:
        """获取指定位置的值"""
        if not 0 <= index < self._size:
            raise IndexError(f"索引 {index} 超出范围 [0, {self._size})")
        return self._data[index]
    
    def __len__(self) -> int:
        return self._size
    
    def __repr__(self) -> str:
        return f"FenwickTreeMin(size={self._size})"


# ============== 便捷函数 ==============

def create_fenwick_tree(data: Iterable[T]) -> FenwickTree[T]:
    """
    从数据创建树状数组
    
    Args:
        data: 初始数据
    
    Returns:
        FenwickTree 实例
    """
    return FenwickTree(data)


def fenwick_prefix_sums(data: Iterable[T]) -> List[T]:
    """
    使用树状数组计算所有前缀和
    
    Args:
        data: 输入数据
    
    Returns:
        前缀和列表
    """
    ft = FenwickTree(data)
    return [ft.prefix_sum(i) for i in range(len(ft))]


def fenwick_range_sums(data: Iterable[T], queries: List[tuple]) -> List[T]:
    """
    批量计算区间和
    
    Args:
        data: 输入数据
        queries: 查询列表，每个元素为 (left, right)
    
    Returns:
        区间和列表
    """
    ft = FenwickTree(data)
    return [ft.range_sum(left, right) for left, right in queries]


def count_inversions(arr: List[T]) -> int:
    """
    使用树状数组计算逆序对数量
    
    时间复杂度: O(n log n)
    
    Args:
        arr: 输入数组
    
    Returns:
        逆序对数量
    """
    if not arr:
        return 0
    
    # 离散化
    sorted_unique = sorted(set(arr))
    rank = {v: i + 1 for i, v in enumerate(sorted_unique)}
    
    # 使用树状数组统计
    size = len(sorted_unique)
    ft = FenwickTree(size=size)
    inversions = 0
    
    # 从右向左遍历
    for i in range(len(arr) - 1, -1, -1):
        r = rank[arr[i]]
        # 统计比当前元素小的元素数量
        if r > 1:
            inversions += ft.prefix_sum(r - 2) if r > 1 else 0
            # 实际上是 prefix_sum(r - 1) 但我们的索引是 0-indexed
            inversions += ft.prefix_sum(r - 1 - 1) if r > 1 else 0
        # 更新树状数组
        ft.add(r - 1, 1)
    
    # 重新计算（修正上面的逻辑）
    ft2 = FenwickTree(size=size)
    inversions = 0
    for i in range(len(arr) - 1, -1, -1):
        r = rank[arr[i]] - 1  # 0-indexed
        # 统计已经出现过的、比当前元素小的元素数量
        if r > 0:
            inversions += ft2.prefix_sum(r - 1)
        ft2.add(r, 1)
    
    return inversions


def find_kth_element(ft: FenwickTree[T], k: int) -> int:
    """
    在树状数组中找到第 k 小的元素索引
    
    前提: 树状数组存储的是计数（每个位置存储该位置元素出现的次数）
    
    Args:
        ft: 树状数组（存储计数）
        k: 第 k 小（1-indexed）
    
    Returns:
        元素索引（0-indexed）
    
    Raises:
        ValueError: k 超出范围
    """
    total = ft.prefix_sum(len(ft) - 1)
    if k < 1 or k > total:
        raise ValueError(f"k={k} 超出范围 [1, {total}]")
    
    # 二分查找
    left, right = 0, len(ft) - 1
    while left < right:
        mid = (left + right) // 2
        if ft.prefix_sum(mid) < k:
            left = mid + 1
        else:
            right = mid
    
    return left


# ============== 导出 ==============

__all__ = [
    # 类
    'FenwickTree',
    'FenwickTreeRangeUpdate',
    'FenwickTree2D',
    'FenwickTreeMax',
    'FenwickTreeMin',
    # 便捷函数
    'create_fenwick_tree',
    'fenwick_prefix_sums',
    'fenwick_range_sums',
    'count_inversions',
    'find_kth_element',
]