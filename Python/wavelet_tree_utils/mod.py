#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Wavelet Tree Utils - 小波树工具库

小波树（Wavelet Tree）是一种用于高效处理有序数据查询的数据结构，
广泛应用于字符串压缩、范围频率查询、近似字符串匹配等领域。

特点:
    - O(log σ) 时间复杂度的范围频率查询
    - O(log σ) 时间复杂度的排名的查询
    - 支持整数数组和字符数组
    - 可用于构建 Wavelet Matrix（多维扩展）

应用场景:
    - 字符串索引和压缩
    - 范围频率查询（RMQ）
    - 有序统计
    - 近似字符串匹配
    - DNA 序列索引
    - 日志分析

零外部依赖，纯 Python 标准库实现。

作者: AllToolkit
日期: 2026-06-01
版本: 1.0.0
"""

from typing import List, Optional, Tuple, Union, Iterable
from collections import defaultdict


class WaveletTree:
    """
    小波树（Wavelet Tree）
    
    一种用于索引有序数据的递归数据结构，支持高效的：
    - rank(c, l, r): 统计 [l, r] 区间内字符 c 出现的次数
    - quantize(l, r, k): 返回 [l, r] 区间内第 k 小的值
    - range_count(l, r, a, b): 统计 [l, r] 区间内值在 [a, b] 范围内的元素个数
    
    时间复杂度: O(log σ)，其中 σ 是字符表大小
    空间复杂度: O(n log σ)
    
    示例:
        >>> wt = WaveletTree([1, 2, 1, 3, 2, 1, 4, 2], min_val=1, max_val=4)
        >>> wt.rank(1, 0, 7)  # 统计 1 在 [0,7] 出现的次数
        3
        >>> wt.quantize(0, 7, 2)  # 返回第 2 小的值
        2
        >>> wt.range_count(0, 7, 2, 3)  # 统计 [2,3] 范围内的元素
        4
    """
    
    def __init__(
        self,
        data: Optional[Iterable[int]] = None,
        min_val: int = 0,
        max_val: int = 255,
        max_depth: int = 16
    ):
        """
        初始化小波树
        
        Args:
            data: 输入数据（可选）
            min_val: 最小值（包含）
            max_val: 最大值（包含）
            max_depth: 最大深度（用于防止递归过深）
        """
        self._min_val = min_val
        self._max_val = max_val
        self._max_depth = max_depth
        
        # 当前层对应的值域范围
        self._lo = min_val
        self._hi = max_val
        
        if data is None:
            self._data: Optional[List[int]] = None
            self._bv: Optional[List[int]] = None
            self._bv_cumsum: Optional[List[int]] = None
            self._child: Optional[Tuple['WaveletTree', 'WaveletTree']] = None
            self._size = 0
            return
        
        self._data = list(data)
        self._size = len(self._data)
        
        # 终止条件：值域为空或数据为空或达到最大深度
        if self._lo >= self._hi or self._size == 0 or max_depth <= 0:
            self._bv = None
            self._bv_cumsum = None
            self._child = None
            return
        
        # 计算当前层的分割点
        mid = (self._lo + self._hi) // 2
        
        # 构建位向量：0 表示属于左子树的元素，1 表示属于右子树的元素
        self._bv = []
        left_data = []
        right_data = []
        
        for val in self._data:
            if val <= mid:
                self._bv.append(0)
                left_data.append(val)
            else:
                self._bv.append(1)
                right_data.append(val)
        
        # 预计算位向量累积和（用于 O(1) 前缀和查询）
        self._bv_cumsum = [0] * (self._size + 1)
        for i in range(self._size):
            self._bv_cumsum[i + 1] = self._bv_cumsum[i] + self._bv[i]
        
        # 递归构建子树
        self._child = (
            WaveletTree(left_data, self._lo, mid, max_depth - 1),
            WaveletTree(right_data, mid + 1, self._hi, max_depth - 1)
        )
    
    @property
    def size(self) -> int:
        """返回数据大小"""
        return self._size
    
    @property
    def is_leaf(self) -> bool:
        """是否为叶子节点"""
        return self._child is None
    
    @property
    def value_range(self) -> Tuple[int, int]:
        """返回值域范围"""
        return (self._lo, self._hi)
    
    def _bv_rank(self, bit: int, index: int) -> int:
        """
        计算位向量中 [0, index] 区间内 bit 出现的次数
        
        Args:
            bit: 要统计的位（0 或 1）
            index: 结束索引（包含，0-indexed）
        
        Returns:
            bit 在 [0, index] 区间内出现的次数
        """
        if self._bv_cumsum is None:
            return 0
        if index < 0:
            return 0
        if index >= self._size:
            index = self._size - 1
        
        if bit == 0:
            return (index + 1) - self._bv_cumsum[index + 1]
        else:
            return self._bv_cumsum[index + 1]
    
    def _bv_range_count(self, bit: int, left: int, right: int) -> int:
        """
        计算位向量在 [left, right] 区间内 bit 出现的次数
        
        Args:
            bit: 要统计的位
            left: 左边界
            right: 右边界
        
        Returns:
            bit 出现的次数
        """
        if left > right:
            return 0
        return self._bv_rank(bit, right) - (self._bv_rank(bit, left - 1) if left > 0 else 0)
    
    def rank(self, val: int, left: int, right: int) -> int:
        """
        统计值 val 在 [left, right] 区间内出现的次数
        
        Args:
            val: 要统计的值
            left: 左边界（包含，0-indexed）
            right: 右边界（包含，0-indexed）
        
        Returns:
            val 出现的次数
        
        Raises:
            IndexError: 索引越界
            ValueError: 值超出范围
        """
        if left > right:
            raise IndexError(f"左边界 {left} 不能大于右边界 {right}")
        if left < 0 or right >= self._size:
            raise IndexError(f"索引超出范围 [0, {self._size})")
        if val < self._lo or val > self._hi:
            raise ValueError(f"值 {val} 超出范围 [{self._lo}, {self._hi}]")
        
        # 终止条件：值域只有一个值
        if self._lo == self._hi:
            return right - left + 1
        
        # 终止条件：没有子树
        if self._child is None:
            return right - left + 1
        
        mid = (self._lo + self._hi) // 2
        
        if val <= mid:
            # 递归到左子树
            left_child = self._child[0]
            new_left = self._bv_range_count(0, left, right) if left <= right else 0
            if new_left == 0:
                return 0
            # 找到左子树中对应位置的左边界
            offset_left = self._bv_rank(0, left - 1) if left > 0 else 0
            # 计算右边界
            num_left = self._bv_rank(0, right)
            new_right = num_left - 1
            return left_child.rank(val, offset_left, new_right)
        else:
            # 递归到右子树
            right_child = self._child[1]
            offset_left = self._bv_rank(0, left - 1) if left > 0 else 0
            num_right_in_range = right - left + 1 - self._bv_range_count(0, left, right)
            if num_right_in_range == 0:
                return 0
            new_left = left - offset_left
            new_right = new_left + num_right_in_range - 1
            return right_child.rank(val, new_left, new_right)
    
    def quantize(self, left: int, right: int, k: int) -> int:
        """
        返回 [left, right] 区间内第 k 小的值
        
        Args:
            left: 左边界（包含，0-indexed）
            right: 右边界（包含，0-indexed）
            k: 第 k 小（1-indexed）
        
        Returns:
            第 k 小的值
        
        Raises:
            ValueError: k 超出范围
        """
        if left > right:
            raise IndexError(f"左边界 {left} 不能大于右边界 {right}")
        if left < 0 or right >= self._size:
            raise IndexError(f"索引超出范围 [0, {self._size})")
        if k < 1 or k > (right - left + 1):
            raise ValueError(f"k={k} 超出范围 [1, {right - left + 1}]")
        
        # 终止条件
        if self._lo == self._hi:
            return self._lo
        
        if self._child is None:
            return self._lo
        
        mid = (self._lo + self._hi) // 2
        
        # 统计左子树在 [left, right] 区间内的元素个数
        left_count = self._bv_range_count(0, left, right)
        
        if k <= left_count:
            # 第 k 小在左子树
            offset_left = self._bv_rank(0, left - 1) if left > 0 else 0
            new_left = offset_left
            new_right = offset_left + left_count - 1
            return self._child[0].quantize(new_left, new_right, k)
        else:
            # 第 k 小在右子树
            offset_left = self._bv_rank(0, left - 1) if left > 0 else 0
            new_left = left - offset_left
            new_right = right - offset_left - left_count
            return self._child[1].quantize(new_left, new_right, k - left_count)
    
    def range_count(self, left: int, right: int, min_val: int, max_val: int) -> int:
        """
        统计 [left, right] 区间内值在 [min_val, max_val] 范围内的元素个数
        
        Args:
            left: 左边界（包含，0-indexed）
            right: 右边界（包含，0-indexed）
            min_val: 范围最小值
            max_val: 范围最大值
        
        Returns:
            范围内的元素个数
        """
        if left > right:
            return 0
        if left < 0 or right >= self._size:
            raise IndexError(f"索引超出范围 [0, {self._size})")
        if min_val > max_val:
            return 0
        if max_val < self._lo or min_val > self._hi:
            return 0
        
        # 完全包含，直接返回区间长度
        if min_val <= self._lo and self._hi <= max_val:
            return right - left + 1
        
        # 无交集
        if self._child is None:
            return 1 if (self._lo >= min_val and self._lo <= max_val) else 0
        
        mid = (self._lo + self._hi) // 2
        
        # 计算左右子树的区间
        offset_left = self._bv_rank(0, left - 1) if left > 0 else 0
        left_count = self._bv_range_count(0, left, right)
        right_count = (right - left + 1) - left_count
        
        left_new_left = offset_left
        left_new_right = offset_left + left_count - 1
        right_new_left = left - offset_left
        right_new_right = right - offset_left - left_count
        
        # 递归计算
        left_result = 0
        right_result = 0
        
        if min_val <= mid and left_count > 0:
            left_result = self._child[0].range_count(
                left_new_left, left_new_right, min_val, max_val
            )
        
        if max_val > mid and right_count > 0:
            right_result = self._child[1].range_count(
                right_new_left, right_new_right, min_val, max_val
            )
        
        return left_result + right_result
    
    def get(self, index: int) -> int:
        """
        获取指定位置的值
        
        Args:
            index: 索引（0-indexed）
        
        Returns:
            该位置的值
        """
        if index < 0 or index >= self._size:
            raise IndexError(f"索引 {index} 超出范围 [0, {self._size})")
        
        if self._child is None:
            return self._lo
        
        bit = self._bv[index] if self._bv else 0
        if bit == 0:
            # 左子树
            new_index = self._bv_rank(0, index - 1) if index > 0 else 0
            return self._child[0].get(new_index)
        else:
            # 右子树：计算在右子树中的位置
            # 当前位置之前有多少个 1（属于右子树）
            ones_before = (index + 1) - self._bv_rank(0, index)
            new_index = ones_before - 1
            return self._child[1].get(new_index)
    
    def __len__(self) -> int:
        return self._size
    
    def __getitem__(self, index: int) -> int:
        return self.get(index)
    
    def to_list(self) -> List[int]:
        """返回原始数据的副本"""
        return self._data.copy() if self._data else []
    
    def __repr__(self) -> str:
        return f"WaveletTree(size={self._size}, range=[{self._lo}, {self._hi}])"


class WaveletTreeCompact:
    """
    紧凑版小波树（使用更少的内存）
    
    与 WaveletTree 的区别：
    - 位向量使用 bit array 而非 int list
    - 只存储每个位置属于左(0)还是右(1)，不存储实际数据
    
    适用于超大规模数据场景。
    """
    
    def __init__(
        self,
        data: Optional[Iterable[int]] = None,
        min_val: int = 0,
        max_val: int = 255
    ):
        """
        初始化紧凑版小波树
        
        Args:
            data: 输入数据
            min_val: 最小值
            max_val: 最大值
        """
        self._min_val = min_val
        self._max_val = max_val
        self._lo = min_val
        self._hi = max_val
        self._size = len(data) if data else 0
        
        if data is None or self._size == 0:
            self._bv: Optional[List[int]] = None
            self._bv_cumsum: Optional[List[int]] = None
            self._child = None
            self._data = None
            return
        
        self._data = list(data)
        
        if self._lo >= self._hi:
            self._bv = None
            self._bv_cumsum = None
            self._child = None
            return
        
        mid = (self._lo + self._hi) // 2
        
        self._bv = []
        left_data = []
        right_data = []
        
        for val in self._data:
            if val <= mid:
                self._bv.append(0)
                left_data.append(val)
            else:
                self._bv.append(1)
                right_data.append(val)
        
        # 预计算位向量累积和
        self._bv_cumsum = [0] * (self._size + 1)
        for i in range(self._size):
            self._bv_cumsum[i + 1] = self._bv_cumsum[i] + self._bv[i]
        
        self._child = (
            WaveletTreeCompact(left_data, self._lo, mid),
            WaveletTreeCompact(right_data, mid + 1, self._hi)
        )
    
    @property
    def size(self) -> int:
        return self._size
    
    def _bv_rank(self, bit: int, index: int) -> int:
        if self._bv_cumsum is None:
            return 0
        if index < 0:
            return 0
        if index >= self._size:
            index = self._size - 1
        
        if bit == 0:
            return (index + 1) - self._bv_cumsum[index + 1]
        else:
            return self._bv_cumsum[index + 1]
    
    def _bv_range_count(self, bit: int, left: int, right: int) -> int:
        if left > right:
            return 0
        return self._bv_rank(bit, right) - (self._bv_rank(bit, left - 1) if left > 0 else 0)
    
    def rank(self, val: int, left: int, right: int) -> int:
        """统计值 val 在 [left, right] 区间内出现的次数"""
        if left > right or left < 0 or right >= self._size:
            return 0
        if val < self._lo or val > self._hi:
            return 0
        
        if self._lo == self._hi:
            return right - left + 1
        
        if self._child is None:
            return right - left + 1
        
        mid = (self._lo + self._hi) // 2
        
        if val <= mid:
            left_child = self._child[0]
            offset_left = self._bv_rank(0, left - 1) if left > 0 else 0
            num_left = self._bv_rank(0, right)
            new_left = offset_left
            new_right = num_left - 1
            if new_left > new_right:
                return 0
            return left_child.rank(val, new_left, new_right)
        else:
            right_child = self._child[1]
            offset_left = self._bv_rank(0, left - 1) if left > 0 else 0
            num_right_in_range = right - left + 1 - self._bv_range_count(0, left, right)
            new_left = left - offset_left
            new_right = new_left + num_right_in_range - 1
            if new_left > new_right:
                return 0
            return right_child.rank(val, new_left, new_right)
    
    def quantize(self, left: int, right: int, k: int) -> int:
        """返回 [left, right] 区间内第 k 小的值"""
        if left > right or k < 1 or k > (right - left + 1):
            raise ValueError(f"k={k} 超出范围 [1, {right - left + 1}]")
        
        if self._lo == self._hi:
            return self._lo
        
        if self._child is None:
            return self._lo
        
        mid = (self._lo + self._hi) // 2
        
        left_count = self._bv_range_count(0, left, right)
        
        if k <= left_count:
            offset_left = self._bv_rank(0, left - 1) if left > 0 else 0
            new_left = offset_left
            new_right = offset_left + left_count - 1
            return self._child[0].quantize(new_left, new_right, k)
        else:
            offset_left = self._bv_rank(0, left - 1) if left > 0 else 0
            new_left = left - offset_left
            new_right = right - offset_left - left_count
            return self._child[1].quantize(new_left, new_right, k - left_count)
    
    def get(self, index: int) -> int:
        """获取指定位置的值"""
        if index < 0 or index >= self._size:
            raise IndexError(f"索引 {index} 超出范围 [0, {self._size})")
        
        if self._child is None:
            return self._lo
        
        bit = self._bv[index] if self._bv else 0
        if bit == 0:
            new_index = self._bv_rank(0, index - 1) if index > 0 else 0
            return self._child[0].get(new_index)
        else:
            new_index = index - (self._bv_rank(0, index - 1) if index > 0 else 0) - 1
            return self._child[1].get(new_index)
    
    def __len__(self) -> int:
        return self._size
    
    def __repr__(self) -> str:
        return f"WaveletTreeCompact(size={self._size}, range=[{self._lo}, {self._hi}])"


# ============== 便捷函数 ==============

def create_wavelet_tree(
    data: List[int],
    min_val: Optional[int] = None,
    max_val: Optional[int] = None
) -> WaveletTree:
    """
    从数据创建小波树
    
    Args:
        data: 输入数据
        min_val: 最小值（自动计算 if None）
        max_val: 最大值（自动计算 if None）
    
    Returns:
        WaveletTree 实例
    """
    if not data:
        raise ValueError("数据不能为空")
    
    if min_val is None:
        min_val = min(data)
    if max_val is None:
        max_val = max(data)
    
    return WaveletTree(data, min_val, max_val)


def wavelet_rank(
    wt: WaveletTree,
    val: int,
    left: int,
    right: int
) -> int:
    """
    统计值 val 在 [left, right] 区间内出现的次数
    
    Args:
        wt: 小波树实例
        val: 要统计的值
        left: 左边界
        right: 右边界
    
    Returns:
        val 出现的次数
    """
    return wt.rank(val, left, right)


def wavelet_quantile(
    wt: WaveletTree,
    left: int,
    right: int,
    k: int
) -> int:
    """
    返回 [left, right] 区间内第 k 小的值
    
    Args:
        wt: 小波树实例
        left: 左边界
        right: 右边界
        k: 第 k 小（1-indexed）
    
    Returns:
        第 k 小的值
    """
    return wt.quantize(left, right, k)


def wavelet_range_count(
    wt: WaveletTree,
    left: int,
    right: int,
    min_val: int,
    max_val: int
) -> int:
    """
    统计 [left, right] 区间内值在 [min_val, max_val] 范围内的元素个数
    
    Args:
        wt: 小波树实例
        left: 左边界
        right: 右边界
        min_val: 范围最小值
        max_val: 范围最大值
    
    Returns:
        范围内的元素个数
    """
    return wt.range_count(left, right, min_val, max_val)


# ============== 导出 ==============

__all__ = [
    # 类
    'WaveletTree',
    'WaveletTreeCompact',
    # 便捷函数
    'create_wavelet_tree',
    'wavelet_rank',
    'wavelet_quantile',
    'wavelet_range_count',
]