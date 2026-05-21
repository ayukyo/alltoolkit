"""
前缀和与差分数组工具模块 (prefix_sum_utils)

提供高效的前缀和与差分数组数据结构，用于区间查询和区间更新操作。

特性:
- 一维前缀和: O(1) 区间求和
- 二维前缀和: O(1) 矩阵区域求和
- 一维差分数组: O(1) 区间更新, O(n) 还原数组
- 二维差分数组: O(1) 矩阵区域更新, O(n*m) 还原矩阵
- 零外部依赖，纯 Python 实现

应用场景:
- 区间求和查询
- 频繁区间更新
- 图像处理（积分图）
- 二维矩阵区域统计
- 算法竞赛

作者: AllToolkit
日期: 2026-05-21
"""

from typing import List, Optional, Tuple, Union, Iterator, Any
from dataclasses import dataclass
import copy


# =============================================================================
# 异常类
# =============================================================================

class PrefixSumError(Exception):
    """前缀和操作异常"""
    pass


class DifferenceArrayError(Exception):
    """差分数组操作异常"""
    pass


# =============================================================================
# 一维前缀和
# =============================================================================

class PrefixSum:
    """
    一维前缀和
    
    用于高效计算区间和。构建时间 O(n)，查询时间 O(1)。
    
    示例:
        >>> ps = PrefixSum([1, 2, 3, 4, 5])
        >>> ps.range_sum(0, 2)  # 1 + 2 + 3
        6
        >>> ps.range_sum(1, 4)  # 2 + 3 + 4 + 5
        14
        >>> ps.prefix_sum(3)  # 1 + 2 + 3 + 4
        10
    """
    
    def __init__(self, arr: List[Union[int, float]]):
        """
        初始化前缀和数组
        
        Args:
            arr: 原始数组
        """
        if not arr:
            self._original = []
            self._prefix = [0]
            return
        
        self._original = list(arr)
        self._prefix = [0] * (len(arr) + 1)
        
        # 构建前缀和数组
        for i, val in enumerate(arr):
            self._prefix[i + 1] = self._prefix[i] + val
    
    @property
    def length(self) -> int:
        """返回原始数组长度"""
        return len(self._original)
    
    @property
    def original(self) -> List[Union[int, float]]:
        """返回原始数组的副本"""
        return self._original.copy()
    
    @property
    def prefix_array(self) -> List[Union[int, float]]:
        """返回前缀和数组（长度为 n+1）"""
        return self._prefix.copy()
    
    def prefix_sum(self, index: int) -> Union[int, float]:
        """
        计算 [0, index] 区间的和
        
        Args:
            index: 结束索引（包含）
            
        Returns:
            区间 [0, index] 的和
        """
        if index < 0 or index >= len(self._original):
            raise PrefixSumError(f"索引越界: {index}, 有效范围 [0, {len(self._original) - 1}]")
        return self._prefix[index + 1]
    
    def range_sum(self, left: int, right: int) -> Union[int, float]:
        """
        计算 [left, right] 区间的和
        
        Args:
            left: 左边界索引（包含）
            right: 右边界索引（包含）
            
        Returns:
            区间 [left, right] 的和
        """
        if left < 0 or right >= len(self._original):
            raise PrefixSumError(f"索引越界: [{left}, {right}], 有效范围 [0, {len(self._original) - 1}]")
        if left > right:
            raise PrefixSumError(f"左边界不能大于右边界: left={left}, right={right}")
        
        return self._prefix[right + 1] - self._prefix[left]
    
    def total(self) -> Union[int, float]:
        """计算整个数组的和"""
        return self._prefix[-1] if self._prefix else 0
    
    def __len__(self) -> int:
        return self.length
    
    def __repr__(self) -> str:
        return f"PrefixSum(length={self.length}, total={self.total()})"
    
    def __getitem__(self, index: int) -> Union[int, float]:
        """获取原始数组指定位置的值"""
        return self._original[index]
    
    def to_dict(self) -> dict:
        """转换为字典"""
        return {
            'original': self._original.copy(),
            'prefix': self._prefix.copy()
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'PrefixSum':
        """从字典创建"""
        return cls(data['original'])


# =============================================================================
# 二维前缀和
# =============================================================================

class PrefixSum2D:
    """
    二维前缀和（积分图）
    
    用于高效计算矩阵区域和。构建时间 O(n*m)，查询时间 O(1)。
    
    示例:
        >>> matrix = [
        ...     [1, 2, 3],
        ...     [4, 5, 6],
        ...     [7, 8, 9]
        ... ]
        >>> ps2d = PrefixSum2D(matrix)
        >>> ps2d.region_sum(0, 0, 1, 1)  # [[1,2],[4,5]] = 1+2+4+5
        12
        >>> ps2d.region_sum(1, 1, 2, 2)  # [[5,6],[8,9]] = 5+6+8+9
        28
    """
    
    def __init__(self, matrix: List[List[Union[int, float]]]):
        """
        初始化二维前缀和
        
        Args:
            matrix: 二维矩阵
        """
        if not matrix or not matrix[0]:
            self._original = []
            self._prefix = [[0]]
            self._rows = 0
            self._cols = 0
            return
        
        self._rows = len(matrix)
        self._cols = len(matrix[0])
        
        # 验证矩阵形状
        for row in matrix:
            if len(row) != self._cols:
                raise PrefixSumError("矩阵必须为矩形（所有行长度相同）")
        
        # 深拷贝原始矩阵
        self._original = [row.copy() for row in matrix]
        
        # 构建二维前缀和数组（大小为 (rows+1) x (cols+1)）
        self._prefix = [[0] * (self._cols + 1) for _ in range(self._rows + 1)]
        
        for i in range(self._rows):
            for j in range(self._cols):
                self._prefix[i + 1][j + 1] = (
                    self._prefix[i][j + 1] +
                    self._prefix[i + 1][j] -
                    self._prefix[i][j] +
                    matrix[i][j]
                )
    
    @property
    def rows(self) -> int:
        """返回矩阵行数"""
        return self._rows
    
    @property
    def cols(self) -> int:
        """返回矩阵列数"""
        return self._cols
    
    @property
    def shape(self) -> Tuple[int, int]:
        """返回矩阵形状 (rows, cols)"""
        return (self._rows, self._cols)
    
    def prefix_sum(self, row: int, col: int) -> Union[int, float]:
        """
        计算 [0,0] 到 [row, col] 区域的和
        
        Args:
            row: 行索引（包含）
            col: 列索引（包含）
            
        Returns:
            区域和
        """
        if row < 0 or row >= self._rows or col < 0 or col >= self._cols:
            raise PrefixSumError(f"索引越界: ({row}, {col}), 有效范围 (0-{self._rows-1}, 0-{self._cols-1})")
        return self._prefix[row + 1][col + 1]
    
    def region_sum(
        self,
        row1: int, col1: int,
        row2: int, col2: int
    ) -> Union[int, float]:
        """
        计算矩形区域 [row1, col1] 到 [row2, col2] 的和
        
        Args:
            row1: 左上角行索引
            col1: 左上角列索引
            row2: 右下角行索引
            col2: 右下角列索引
            
        Returns:
            矩形区域的和
        """
        if row1 < 0 or row2 >= self._rows or col1 < 0 or col2 >= self._cols:
            raise PrefixSumError(
                f"索引越界: ({row1},{col1})-({row2},{col2}), "
                f"有效范围 (0-{self._rows-1}, 0-{self._cols-1})"
            )
        if row1 > row2 or col1 > col2:
            raise PrefixSumError(f"左上角坐标必须小于等于右下角坐标")
        
        # 使用容斥原理计算区域和
        return (
            self._prefix[row2 + 1][col2 + 1] -
            self._prefix[row1][col2 + 1] -
            self._prefix[row2 + 1][col1] +
            self._prefix[row1][col1]
        )
    
    def row_sum(self, row: int) -> Union[int, float]:
        """计算指定行的和"""
        if row < 0 or row >= self._rows:
            raise PrefixSumError(f"行索引越界: {row}, 有效范围 [0, {self._rows - 1}]")
        return self.region_sum(row, 0, row, self._cols - 1)
    
    def col_sum(self, col: int) -> Union[int, float]:
        """计算指定列的和"""
        if col < 0 or col >= self._cols:
            raise PrefixSumError(f"列索引越界: {col}, 有效范围 [0, {self._cols - 1}]")
        return self.region_sum(0, col, self._rows - 1, col)
    
    def total(self) -> Union[int, float]:
        """计算整个矩阵的和"""
        return self._prefix[self._rows][self._cols] if self._rows > 0 and self._cols > 0 else 0
    
    def __len__(self) -> int:
        return self._rows
    
    def __getitem__(self, index: int) -> List[Union[int, float]]:
        """获取原始矩阵指定行"""
        return self._original[index].copy()
    
    def __repr__(self) -> str:
        return f"PrefixSum2D(shape={self.shape}, total={self.total()})"
    
    def to_dict(self) -> dict:
        """转换为字典"""
        return {
            'original': [row.copy() for row in self._original],
            'prefix': [row.copy() for row in self._prefix]
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'PrefixSum2D':
        """从字典创建"""
        return cls(data['original'])


# =============================================================================
# 一维差分数组
# =============================================================================

class DifferenceArray:
    """
    一维差分数组
    
    用于高效的区间更新。更新时间 O(1)，还原时间 O(n)。
    
    示例:
        >>> da = DifferenceArray([1, 2, 3, 4, 5])
        >>> da.range_add(1, 3, 10)  # 在 [1, 3] 区间每个元素加 10
        >>> da.range_add(0, 4, 5)   # 在 [0, 4] 区间每个元素加 5
        >>> da.to_array()  # 还原后的数组
        [6, 17, 18, 19, 10]
    """
    
    def __init__(self, arr: Optional[List[Union[int, float]]] = None, size: Optional[int] = None):
        """
        初始化差分数组
        
        Args:
            arr: 原始数组（可选）
            size: 数组大小（如果 arr 为 None）
        """
        if arr is not None:
            self._size = len(arr)
            self._diff = [0] * (self._size + 1)  # 多一个元素用于边界处理
            
            # 从原始数组构建差分数组
            if self._size > 0:
                self._diff[0] = arr[0]
                for i in range(1, self._size):
                    self._diff[i] = arr[i] - arr[i - 1]
        elif size is not None and size > 0:
            self._size = size
            self._diff = [0] * (self._size + 1)
        else:
            raise DifferenceArrayError("必须提供 arr 或 size 参数")
    
    @property
    def size(self) -> int:
        """返回数组大小"""
        return self._size
    
    def range_add(self, left: int, right: int, value: Union[int, float]) -> 'DifferenceArray':
        """
        在 [left, right] 区间内所有元素加上 value
        
        Args:
            left: 左边界索引（包含）
            right: 右边界索引（包含）
            value: 要加的值
            
        Returns:
            self（支持链式调用）
        """
        if left < 0 or right >= self._size:
            raise DifferenceArrayError(f"索引越界: [{left}, {right}], 有效范围 [0, {self._size - 1}]")
        if left > right:
            raise DifferenceArrayError(f"左边界不能大于右边界: left={left}, right={right}")
        
        self._diff[left] += value
        self._diff[right + 1] -= value
        
        return self  # 支持链式调用
    
    def point_add(self, index: int, value: Union[int, float]) -> 'DifferenceArray':
        """
        在指定位置加 value（等价于 range_add(index, index, value)）
        
        Args:
            index: 索引
            value: 要加的值
            
        Returns:
            self（支持链式调用）
        """
        return self.range_add(index, index, value)
    
    def range_assign(self, left: int, right: int, value: Union[int, float]) -> 'DifferenceArray':
        """
        将 [left, right] 区间内所有元素设置为 value（需要先还原再操作）
        
        注意：此方法会还原数组并重建差分数组
        
        Args:
            left: 左边界索引（包含）
            right: 右边界索引（包含）
            value: 要设置的值
            
        Returns:
            self（支持链式调用）
        """
        arr = self.to_array()
        for i in range(left, right + 1):
            arr[i] = value
        
        # 重建差分数组
        self._diff = [0] * (self._size + 1)
        if self._size > 0:
            self._diff[0] = arr[0]
            for i in range(1, self._size):
                self._diff[i] = arr[i] - arr[i - 1]
        
        return self
    
    def to_array(self) -> List[Union[int, float]]:
        """
        还原为数组
        
        Returns:
            还原后的数组
        """
        result = [0] * self._size
        if self._size > 0:
            result[0] = self._diff[0]
            for i in range(1, self._size):
                result[i] = result[i - 1] + self._diff[i]
        
        return result
    
    def reset(self, arr: Optional[List[Union[int, float]]] = None) -> 'DifferenceArray':
        """
        重置差分数组
        
        Args:
            arr: 新的原始数组（可选，默认重置为全零）
            
        Returns:
            self（支持链式调用）
        """
        if arr is not None:
            if len(arr) != self._size:
                raise DifferenceArrayError(f"数组大小不匹配: 期望 {self._size}, 得到 {len(arr)}")
            self._diff = [0] * (self._size + 1)
            if self._size > 0:
                self._diff[0] = arr[0]
                for i in range(1, self._size):
                    self._diff[i] = arr[i] - arr[i - 1]
        else:
            self._diff = [0] * (self._size + 1)
        
        return self
    
    def get_diff(self) -> List[Union[int, float]]:
        """获取差分数组（用于调试）"""
        return self._diff[:-1].copy() if self._size > 0 else []
    
    def __len__(self) -> int:
        return self._size
    
    def __repr__(self) -> str:
        return f"DifferenceArray(size={self._size})"
    
    def to_dict(self) -> dict:
        """转换为字典"""
        return {
            'size': self._size,
            'diff': self._diff.copy()
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'DifferenceArray':
        """从字典创建"""
        instance = cls.__new__(cls)
        instance._size = data['size']
        instance._diff = data['diff'].copy()
        return instance


# =============================================================================
# 二维差分数组
# =============================================================================

class DifferenceArray2D:
    """
    二维差分数组
    
    用于高效的矩阵区域更新。更新时间 O(1)，还原时间 O(n*m)。
    
    示例:
        >>> da2d = DifferenceArray2D(3, 3)
        >>> da2d.region_add(0, 0, 1, 1, 5)  # 左上角 2x2 区域加 5
        >>> da2d.region_add(1, 1, 2, 2, 10)  # 右下角 2x2 区域加 10
        >>> da2d.to_matrix()
        [[5, 5, 0], [5, 15, 10], [0, 10, 10]]
    """
    
    def __init__(
        self,
        matrix: Optional[List[List[Union[int, float]]]] = None,
        rows: Optional[int] = None,
        cols: Optional[int] = None
    ):
        """
        初始化二维差分数组
        
        Args:
            matrix: 原始矩阵（可选）
            rows: 矩阵行数（如果 matrix 为 None）
            cols: 矩阵列数（如果 matrix 为 None）
        """
        if matrix is not None:
            if not matrix or not matrix[0]:
                raise DifferenceArrayError("矩阵不能为空")
            
            self._rows = len(matrix)
            self._cols = len(matrix[0])
            
            # 验证矩阵形状
            for row in matrix:
                if len(row) != self._cols:
                    raise DifferenceArrayError("矩阵必须为矩形（所有行长度相同）")
            
            # 差分数组大小为 (rows+1) x (cols+1)
            self._diff = [[0] * (self._cols + 2) for _ in range(self._rows + 2)]
            
            # 从原始矩阵构建差分数组
            for i in range(self._rows):
                for j in range(self._cols):
                    # 标准的二维差分初始化
                    val = matrix[i][j]
                    self._diff[i + 1][j + 1] += val
                    self._diff[i + 1][j + 2] -= val
                    self._diff[i + 2][j + 1] -= val
                    self._diff[i + 2][j + 2] += val
            
        elif rows is not None and cols is not None and rows > 0 and cols > 0:
            self._rows = rows
            self._cols = cols
            self._diff = [[0] * (self._cols + 2) for _ in range(self._rows + 2)]
        else:
            raise DifferenceArrayError("必须提供 matrix 或 (rows, cols) 参数")
    
    @property
    def rows(self) -> int:
        """返回矩阵行数"""
        return self._rows
    
    @property
    def cols(self) -> int:
        """返回矩阵列数"""
        return self._cols
    
    @property
    def shape(self) -> Tuple[int, int]:
        """返回矩阵形状 (rows, cols)"""
        return (self._rows, self._cols)
    
    def region_add(
        self,
        row1: int, col1: int,
        row2: int, col2: int,
        value: Union[int, float]
    ) -> 'DifferenceArray2D':
        """
        在矩形区域 [row1, col1] 到 [row2, col2] 内所有元素加上 value
        
        Args:
            row1: 左上角行索引（包含）
            col1: 左上角列索引（包含）
            row2: 右下角行索引（包含）
            col2: 右下角列索引（包含）
            value: 要加的值
            
        Returns:
            self（支持链式调用）
        """
        if (row1 < 0 or row2 >= self._rows or 
            col1 < 0 or col2 >= self._cols):
            raise DifferenceArrayError(
                f"索引越界: ({row1},{col1})-({row2},{col2}), "
                f"有效范围 (0-{self._rows-1}, 0-{self._cols-1})"
            )
        if row1 > row2 or col1 > col2:
            raise DifferenceArrayError("左上角坐标必须小于等于右下角坐标")
        
        # 二维差分的四个角更新
        row1, col1, row2, col2 = row1 + 1, col1 + 1, row2 + 1, col2 + 1  # 调整到 1-indexed
        
        self._diff[row1][col1] += value
        self._diff[row1][col2 + 1] -= value
        self._diff[row2 + 1][col1] -= value
        self._diff[row2 + 1][col2 + 1] += value
        
        return self
    
    def point_add(self, row: int, col: int, value: Union[int, float]) -> 'DifferenceArray2D':
        """
        在指定位置加 value（等价于 region_add(row, col, row, col, value)）
        
        Args:
            row: 行索引
            col: 列索引
            value: 要加的值
            
        Returns:
            self（支持链式调用）
        """
        return self.region_add(row, col, row, col, value)
    
    def to_matrix(self) -> List[List[Union[int, float]]]:
        """
        还原为矩阵
        
        Returns:
            还原后的矩阵
        """
        # 先对差分数组求前缀和
        result = [[0] * self._cols for _ in range(self._rows)]
        
        # 计算前缀和
        for i in range(1, self._rows + 1):
            for j in range(1, self._cols + 1):
                self._diff[i][j] += (
                    self._diff[i - 1][j] +
                    self._diff[i][j - 1] -
                    self._diff[i - 1][j - 1]
                )
                result[i - 1][j - 1] = self._diff[i][j]
        
        # 还原差分数组（以便后续继续操作）
        for i in range(self._rows, 0, -1):
            for j in range(self._cols, 0, -1):
                self._diff[i][j] -= (
                    self._diff[i - 1][j] +
                    self._diff[i][j - 1] -
                    self._diff[i - 1][j - 1]
                )
        
        return result
    
    def reset(self) -> 'DifferenceArray2D':
        """
        重置差分数组为全零
        
        Returns:
            self（支持链式调用）
        """
        self._diff = [[0] * (self._cols + 2) for _ in range(self._rows + 2)]
        return self
    
    def __len__(self) -> int:
        return self._rows
    
    def __repr__(self) -> str:
        return f"DifferenceArray2D(shape={self.shape})"
    
    def to_dict(self) -> dict:
        """转换为字典"""
        return {
            'rows': self._rows,
            'cols': self._cols,
            'diff': [row.copy() for row in self._diff]
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'DifferenceArray2D':
        """从字典创建"""
        instance = cls.__new__(cls)
        instance._rows = data['rows']
        instance._cols = data['cols']
        instance._diff = [row.copy() for row in data['diff']]
        return instance


# =============================================================================
# 便捷函数
# =============================================================================

def build_prefix_sum(arr: List[Union[int, float]]) -> List[Union[int, float]]:
    """
    快速构建前缀和数组
    
    Args:
        arr: 原始数组
        
    Returns:
        前缀和数组（长度为 n+1，prefix[0]=0）
    """
    prefix = [0]
    for val in arr:
        prefix.append(prefix[-1] + val)
    return prefix


def range_sum(prefix: List[Union[int, float]], left: int, right: int) -> Union[int, float]:
    """
    使用前缀和数组快速计算区间和
    
    Args:
        prefix: 前缀和数组（长度为 n+1）
        left: 左边界索引（包含）
        right: 右边界索引（包含）
        
    Returns:
        区间 [left, right] 的和
    """
    return prefix[right + 1] - prefix[left]


def build_difference_array(arr: List[Union[int, float]]) -> List[Union[int, float]]:
    """
    从数组构建差分数组
    
    Args:
        arr: 原始数组
        
    Returns:
        差分数组（长度为 n）
    """
    if not arr:
        return []
    
    diff = [arr[0]]
    for i in range(1, len(arr)):
        diff.append(arr[i] - arr[i - 1])
    
    return diff


def restore_from_difference(diff: List[Union[int, float]]) -> List[Union[int, float]]:
    """
    从差分数组还原原数组
    
    Args:
        diff: 差分数组
        
    Returns:
        原数组
    """
    if not diff:
        return []
    
    arr = [diff[0]]
    for i in range(1, len(diff)):
        arr.append(arr[-1] + diff[i])
    
    return arr


# =============================================================================
# 导出
# =============================================================================

__all__ = [
    'PrefixSumError',
    'DifferenceArrayError',
    'PrefixSum',
    'PrefixSum2D',
    'DifferenceArray',
    'DifferenceArray2D',
    'build_prefix_sum',
    'range_sum',
    'build_difference_array',
    'restore_from_difference',
]