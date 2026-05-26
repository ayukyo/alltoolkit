#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Sparse Table Utils - 稀疏表工具库
================================

稀疏表（Sparse Table）是一种用于高效处理静态区间查询的数据结构。

时间复杂度:
    - 预处理: O(n log n)
    - 区间查询: O(1)
    - 不支持更新（静态数据结构）

空间复杂度: O(n log n)

特点:
    - 支持多种可重复贡献操作（min, max, gcd, lcm, and, or）
    - 查询时间 O(1)，比线段树更快
    - 适用于静态数据（构建后不修改）
    - 零外部依赖，纯 Python 标准库实现

注意: Sparse Table 只适用于可重复贡献的操作（幂等操作）。
      对于求和、XOR 等非幂等操作，请使用 DisjointSparseTable。

作者: AllToolkit 自动化生成
日期: 2026-05-26
"""

from typing import List, Optional, Callable, TypeVar, Generic, Iterable, Tuple, Any
from dataclasses import dataclass
from enum import Enum
import math

T = TypeVar('T', int, float)


class OperationType(Enum):
    """操作类型枚举 - 仅支持可重复贡献的操作（幂等操作）"""
    MIN = "min"
    MAX = "max"
    GCD = "gcd"
    LCM = "lcm"
    AND = "and"
    OR = "or"


def _gcd(a: int, b: int) -> int:
    """计算最大公约数"""
    a, b = abs(a), abs(b)
    while b:
        a, b = b, a % b
    return a


def _lcm(a: int, b: int) -> int:
    """计算最小公倍数"""
    if a == 0 or b == 0:
        return 0
    return abs(a * b) // _gcd(a, b)


def _bit_length(n: int) -> int:
    """计算整数的二进制位数"""
    if n <= 0:
        return 0
    return n.bit_length()


def _log2_floor(n: int) -> int:
    """计算 floor(log2(n))"""
    if n <= 0:
        return 0
    return n.bit_length() - 1


class SparseTable(Generic[T]):
    """
    稀疏表（Sparse Table）
    
    支持静态区间查询，查询时间 O(1)。
    仅适用于可重复贡献的操作（幂等操作）。
    
    Example:
        >>> st = SparseTable([3, 1, 4, 1, 5, 9, 2, 6], OperationType.MIN)
        >>> st.query(0, 7)  # 整个数组的最小值
        1
        >>> st.query(2, 5)  # [4, 1, 5, 9] 的最小值
        1
        
        >>> st_max = SparseTable([3, 1, 4, 1, 5, 9, 2, 6], OperationType.MAX)
        >>> st_max.query(0, 7)
        9
        
        >>> st_gcd = SparseTable([12, 18, 24, 36], OperationType.GCD)
        >>> st_gcd.query(0, 3)
        6
    """
    
    def __init__(
        self, 
        data: Iterable[T], 
        op_type: OperationType = OperationType.MIN
    ):
        """
        初始化稀疏表
        
        Args:
            data: 初始数据
            op_type: 操作类型（MIN, MAX, GCD, LCM, AND, OR）
        """
        self._data = list(data)
        self._n = len(self._data)
        self._op_type = op_type
        
        if self._n == 0:
            self._log = []
            self._table = []
            return
        
        # 预计算 log 值
        self._log = [0] * (self._n + 1)
        for i in range(2, self._n + 1):
            self._log[i] = self._log[i // 2] + 1
        
        # 构建 sparse table
        self._build()
    
    def _get_op_func(self) -> Callable[[T, T], T]:
        """获取操作函数"""
        ops = {
            OperationType.MIN: min,
            OperationType.MAX: max,
            OperationType.GCD: _gcd,
            OperationType.LCM: _lcm,
            OperationType.AND: lambda a, b: a & b,
            OperationType.OR: lambda a, b: a | b,
        }
        return ops[self._op_type]
    
    def _build(self):
        """构建稀疏表"""
        op = self._get_op_func()
        k = self._log[self._n] + 1
        
        # table[j][i] 表示从位置 i 开始，长度为 2^j 的区间的查询结果
        self._table: List[List[T]] = []
        
        # j = 0, 长度为 1 的区间
        self._table.append(self._data[:])
        
        # j = 1, 2, ... 逐层构建
        for j in range(1, k):
            prev = self._table[j - 1]
            curr = []
            length = 1 << j
            half = 1 << (j - 1)
            
            for i in range(self._n - length + 1):
                curr.append(op(prev[i], prev[i + half]))
            
            self._table.append(curr)
    
    def query(self, left: int, right: int) -> T:
        """
        区间查询 [left, right]
        
        Args:
            left: 左边界（包含）
            right: 右边界（包含）
        
        Returns:
            区间查询结果
        
        Raises:
            ValueError: 索引无效或数据为空
        
        Example:
            >>> st = SparseTable([3, 1, 4, 1, 5], OperationType.MIN)
            >>> st.query(1, 3)
            1
        """
        if self._n == 0:
            raise ValueError("Sparse table is empty")
        
        if left < 0 or right >= self._n or left > right:
            raise ValueError(f"Invalid range: [{left}, {right}] for array of length {self._n}")
        
        length = right - left + 1
        j = self._log[length]
        
        op = self._get_op_func()
        
        # 使用两个重叠的区间覆盖 [left, right]
        # 区间长度为 2^j
        # 第一个区间: [left, left + 2^j - 1]
        # 第二个区间: [right - 2^j + 1, right]
        # 由于操作是幂等的，重叠部分不影响结果
        return op(
            self._table[j][left],
            self._table[j][right - (1 << j) + 1]
        )
    
    def __len__(self) -> int:
        """返回数据长度"""
        return self._n
    
    def __getitem__(self, index: int) -> T:
        """获取单个元素"""
        return self._data[index]
    
    @property
    def data(self) -> List[T]:
        """返回原始数据的副本"""
        return self._data[:]
    
    @property
    def op_type(self) -> OperationType:
        """返回操作类型"""
        return self._op_type
    
    def range_min(self, left: int, right: int) -> T:
        """区间最小值（便捷方法）"""
        if self._op_type != OperationType.MIN:
            raise ValueError("This sparse table is not configured for MIN operations")
        return self.query(left, right)
    
    def range_max(self, left: int, right: int) -> T:
        """区间最大值（便捷方法）"""
        if self._op_type != OperationType.MAX:
            raise ValueError("This sparse table is not configured for MAX operations")
        return self.query(left, right)
    
    def range_gcd(self, left: int, right: int) -> T:
        """区间最大公约数（便捷方法）"""
        if self._op_type != OperationType.GCD:
            raise ValueError("This sparse table is not configured for GCD operations")
        return self.query(left, right)
    
    def to_dict(self) -> dict:
        """导出为字典格式"""
        return {
            'data': self._data[:],
            'op_type': self._op_type.value,
            'n': self._n
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'SparseTable':
        """从字典创建"""
        return cls(
            data['data'],
            OperationType(data['op_type'])
        )


class SparseTable2D(Generic[T]):
    """
    二维稀疏表
    
    支持静态二维区间查询，查询时间 O(1)。
    
    Example:
        >>> matrix = [
        ...     [1, 2, 3, 4],
        ...     [5, 6, 7, 8],
        ...     [9, 10, 11, 12],
        ...     [13, 14, 15, 16]
        ... ]
        >>> st = SparseTable2D(matrix, OperationType.MAX)
        >>> st.query(0, 0, 2, 2)  # 左上角 3x3 子矩阵的最大值
        11
    """
    
    def __init__(
        self, 
        data: List[List[T]], 
        op_type: OperationType = OperationType.MIN
    ):
        """
        初始化二维稀疏表
        
        Args:
            data: 二维数组
            op_type: 操作类型
        """
        if not data or not data[0]:
            self._data = []
            self._rows = 0
            self._cols = 0
            self._log_r = []
            self._log_c = []
            self._table = []
            self._op_type = op_type
            return
        
        self._data = [row[:] for row in data]
        self._rows = len(data)
        self._cols = len(data[0])
        self._op_type = op_type
        
        # 预计算 log 值
        self._log_r = [0] * (self._rows + 1)
        self._log_c = [0] * (self._cols + 1)
        
        for i in range(2, self._rows + 1):
            self._log_r[i] = self._log_r[i // 2] + 1
        for i in range(2, self._cols + 1):
            self._log_c[i] = self._log_c[i // 2] + 1
        
        self._build()
    
    def _get_op_func(self) -> Callable[[T, T], T]:
        """获取操作函数"""
        ops = {
            OperationType.MIN: min,
            OperationType.MAX: max,
            OperationType.GCD: _gcd,
            OperationType.LCM: _lcm,
            OperationType.AND: lambda a, b: a & b,
            OperationType.OR: lambda a, b: a | b,
        }
        return ops[self._op_type]
    
    def _build(self):
        """构建二维稀疏表"""
        op = self._get_op_func()
        kr = self._log_r[self._rows] + 1
        kc = self._log_c[self._cols] + 1
        
        # table[jr][jc][r][c] 表示从 (r, c) 开始，大小为 2^jr x 2^jc 的矩形
        self._table: List[List[List[List[T]]]] = []
        
        # 初始化第一层 (jr=0)
        self._table.append([])
        
        # jc=0, jr=0: 大小 1x1
        self._table[0].append([row[:] for row in self._data])
        
        # 先扩展列方向 (jc 从 1 到 kc-1)，jr=0
        for jc in range(1, kc):
            prev = self._table[0][jc - 1]
            width = 1 << jc
            half = 1 << (jc - 1)
            
            curr: List[List[T]] = []
            for r in range(self._rows):
                row_vals: List[T] = []
                for c in range(self._cols - width + 1):
                    row_vals.append(op(prev[r][c], prev[r][c + half]))
                curr.append(row_vals)
            self._table[0].append(curr)
        
        # 然后扩展行方向 (jr 从 1 到 kr-1)
        for jr in range(1, kr):
            self._table.append([])
            
            for jc in range(kc):
                prev = self._table[jr - 1][jc]
                height = 1 << jr
                half = 1 << (jr - 1)
                
                curr: List[List[T]] = []
                for r in range(self._rows - height + 1):
                    row_vals: List[T] = []
                    # 需要考虑 jc 对应的宽度
                    if jc == 0:
                        width = 1
                    else:
                        width = 1 << jc
                    
                    for c in range(len(prev[r])):
                        row_vals.append(op(prev[r][c], prev[r + half][c]))
                    curr.append(row_vals)
                self._table[jr].append(curr)
    
    def query(self, r1: int, c1: int, r2: int, c2: int) -> T:
        """
        二维区间查询
        
        Args:
            r1: 左上角行索引
            c1: 左上角列索引
            r2: 右下角行索引
            c2: 右下角列索引
        
        Returns:
            二维区间查询结果
        """
        if self._rows == 0 or self._cols == 0:
            raise ValueError("Sparse table is empty")
        
        if (r1 < 0 or c1 < 0 or r2 >= self._rows or c2 >= self._cols or
            r1 > r2 or c1 > c2):
            raise ValueError(f"Invalid range: [({r1},{c1}), ({r2},{c2})]")
        
        jr = self._log_r[r2 - r1 + 1]
        jc = self._log_c[c2 - c1 + 1]
        
        op = self._get_op_func()
        
        # 使用 4 个矩形覆盖目标区域
        hr = 1 << jr
        hc = 1 << jc
        
        # 四个角的位置
        v1 = self._table[jr][jc][r1][c1]
        v2 = self._table[jr][jc][r1][c2 - hc + 1]
        v3 = self._table[jr][jc][r2 - hr + 1][c1]
        v4 = self._table[jr][jc][r2 - hr + 1][c2 - hc + 1]
        
        return op(op(v1, v2), op(v3, v4))
    
    @property
    def rows(self) -> int:
        """返回行数"""
        return self._rows
    
    @property
    def cols(self) -> int:
        """返回列数"""
        return self._cols


class PrefixSumTable(Generic[T]):
    """
    前缀和表（支持任意可结合操作）
    
    支持求和、乘积、XOR 等操作，查询时间 O(1)。
    
    Example:
        >>> st = PrefixSumTable([1, 2, 3, 4, 5], lambda a, b: a + b, 0)
        >>> st.query(1, 3)  # 2 + 3 + 4
        9
    """
    
    def __init__(
        self, 
        data: Iterable[T], 
        op: Callable[[T, T], T],
        identity: T,
        inv_op: Optional[Callable[[T, T], T]] = None
    ):
        """
        初始化前缀和表
        
        Args:
            data: 初始数据
            op: 二元操作函数（可结合）
            identity: 恒等元素
            inv_op: 逆操作函数（可选，用于 O(1) 查询）
        """
        self._data = list(data)
        self._n = len(self._data)
        self._op = op
        self._identity = identity
        self._inv_op = inv_op
        
        if self._n == 0:
            self._prefix = []
            return
        
        self._build()
    
    def _build(self):
        """构建前缀和数组"""
        self._prefix = [self._identity] * (self._n + 1)
        for i in range(self._n):
            self._prefix[i + 1] = self._op(self._prefix[i], self._data[i])
    
    def query(self, left: int, right: int) -> T:
        """
        区间查询 [left, right]
        
        Args:
            left: 左边界（包含）
            right: 右边界（包含）
        
        Returns:
            区间查询结果
        """
        if self._n == 0:
            raise ValueError("Table is empty")
        
        if left < 0 or right >= self._n or left > right:
            raise ValueError(f"Invalid range: [{left}, {right}]")
        
        if self._inv_op is not None:
            # 使用逆操作进行 O(1) 查询
            return self._inv_op(self._prefix[right + 1], self._prefix[left])
        else:
            # 没有逆操作，需要 O(n) 查询
            result = self._identity
            for i in range(left, right + 1):
                result = self._op(result, self._data[i])
            return result
    
    def prefix_query(self, index: int) -> T:
        """查询 [0, index] 的前缀结果"""
        if index < 0 or index >= self._n:
            raise ValueError(f"Invalid index: {index}")
        return self._prefix[index + 1]
    
    def __len__(self) -> int:
        return self._n
    
    @property
    def data(self) -> List[T]:
        return self._data[:]


@dataclass
class RangeInfo:
    """区间信息"""
    left: int
    right: int
    value: Any
    operation: str
    
    def __str__(self) -> str:
        return f"RangeInfo([{self.left}, {self.right}], {self.operation}={self.value})"


class SparseTableBuilder:
    """
    稀疏表构建器（流式 API）
    
    Example:
        >>> st = (SparseTableBuilder()
        ...       .with_data([1, 2, 3, 4, 5])
        ...       .with_operation(OperationType.MAX)
        ...       .build())
        >>> st.query(0, 4)
        5
    """
    
    def __init__(self):
        self._data: List[T] = []
        self._op_type: OperationType = OperationType.MIN
    
    def with_data(self, data: Iterable[T]) -> 'SparseTableBuilder':
        """设置数据"""
        self._data = list(data)
        return self
    
    def with_operation(self, op_type: OperationType) -> 'SparseTableBuilder':
        """设置操作类型"""
        self._op_type = op_type
        return self
    
    def for_min(self) -> 'SparseTableBuilder':
        """设置为最小值查询"""
        self._op_type = OperationType.MIN
        return self
    
    def for_max(self) -> 'SparseTableBuilder':
        """设置为最大值查询"""
        self._op_type = OperationType.MAX
        return self
    
    def for_gcd(self) -> 'SparseTableBuilder':
        """设置为最大公约数查询"""
        self._op_type = OperationType.GCD
        return self
    
    def for_lcm(self) -> 'SparseTableBuilder':
        """设置为最小公倍数查询"""
        self._op_type = OperationType.LCM
        return self
    
    def build(self) -> SparseTable:
        """构建稀疏表"""
        return SparseTable(self._data, self._op_type)


# 便捷函数
def build_min_sparse_table(data: Iterable[T]) -> SparseTable:
    """构建最小值稀疏表"""
    return SparseTable(data, OperationType.MIN)


def build_max_sparse_table(data: Iterable[T]) -> SparseTable:
    """构建最大值稀疏表"""
    return SparseTable(data, OperationType.MAX)


def build_gcd_sparse_table(data: Iterable[T]) -> SparseTable:
    """构建 GCD 稀疏表"""
    return SparseTable(data, OperationType.GCD)


def range_min(data: List[T], left: int, right: int) -> T:
    """
    一次性区间最小值查询
    
    对于多次查询，建议构建 SparseTable 对象。
    
    Example:
        >>> range_min([3, 1, 4, 1, 5, 9, 2, 6], 2, 5)
        1
    """
    st = SparseTable(data, OperationType.MIN)
    return st.query(left, right)


def range_max(data: List[T], left: int, right: int) -> T:
    """
    一次性区间最大值查询
    
    Example:
        >>> range_max([3, 1, 4, 1, 5, 9, 2, 6], 2, 5)
        9
    """
    st = SparseTable(data, OperationType.MAX)
    return st.query(left, right)


def range_gcd(data: List[T], left: int, right: int) -> T:
    """
    一次性区间 GCD 查询
    
    Example:
        >>> range_gcd([12, 18, 24, 36, 60], 0, 4)
        6
    """
    st = SparseTable(data, OperationType.GCD)
    return st.query(left, right)


def batch_queries(
    data: List[T], 
    queries: List[Tuple[int, int]], 
    op_type: OperationType = OperationType.MIN
) -> List[T]:
    """
    批量查询
    
    一次性处理多个区间查询，比逐个调用更高效。
    
    Args:
        data: 数据数组
        queries: 查询列表，每个元素为 (left, right) 元组
        op_type: 操作类型
    
    Returns:
        查询结果列表
    
    Example:
        >>> batch_queries([3, 1, 4, 1, 5, 9], [(0, 2), (1, 4), (3, 5)], OperationType.MIN)
        [1, 1, 1]
    """
    st = SparseTable(data, op_type)
    return [st.query(left, right) for left, right in queries]


if __name__ == "__main__":
    # 简单演示
    print("=== Sparse Table 演示 ===")
    
    # 最小值查询
    data = [3, 1, 4, 1, 5, 9, 2, 6, 5, 3, 5]
    st_min = SparseTable(data, OperationType.MIN)
    print(f"数据: {data}")
    print(f"区间 [0, 10] 最小值: {st_min.query(0, 10)}")
    print(f"区间 [2, 5] 最小值: {st_min.query(2, 5)}")
    
    # 最大值查询
    st_max = SparseTable(data, OperationType.MAX)
    print(f"区间 [0, 10] 最大值: {st_max.query(0, 10)}")
    print(f"区间 [2, 5] 最大值: {st_max.query(2, 5)}")
    
    # GCD 查询
    data2 = [12, 18, 24, 36, 60, 90]
    st_gcd = SparseTable(data2, OperationType.GCD)
    print(f"\nGCD 数据: {data2}")
    print(f"区间 [0, 5] GCD: {st_gcd.query(0, 5)}")
    print(f"区间 [2, 4] GCD: {st_gcd.query(2, 4)}")
    
    # 使用构建器
    print("\n=== 使用构建器 ===")
    st = (SparseTableBuilder()
          .with_data([5, 2, 8, 1, 9, 3])
          .for_min()
          .build())
    print(f"最小值: {st.query(0, 5)}")
    
    # 二维稀疏表
    print("\n=== 二维稀疏表 ===")
    matrix = [
        [1, 2, 3, 4],
        [5, 6, 7, 8],
        [9, 10, 11, 12],
        [13, 14, 15, 16]
    ]
    st2d = SparseTable2D(matrix, OperationType.MAX)
    print(f"子矩阵 [0,0] 到 [2,2] 最大值: {st2d.query(0, 0, 2, 2)}")
    
    # 前缀和表（求和）
    print("\n=== 前缀和表 ===")
    st_sum = PrefixSumTable([1, 2, 3, 4, 5], lambda a, b: a + b, 0, lambda a, b: a - b)
    print(f"区间 [0, 4] 和: {st_sum.query(0, 4)}")
    print(f"区间 [1, 3] 和: {st_sum.query(1, 3)}")
    
    # 批量查询
    print("\n=== 批量查询 ===")
    results = batch_queries(
        [3, 1, 4, 1, 5, 9, 2, 6],
        [(0, 3), (2, 5), (4, 7)],
        OperationType.MIN
    )
    print(f"批量查询结果: {results}")
    
    print("\n所有演示完成!")