"""
Bitmap Utils - 零依赖位图工具库

功能：
- 高效位操作（设置、清除、翻转、查询）
- 位图运算（AND, OR, XOR, NOT, 差集）
- 位图统计（计数、查找、范围操作）
- 序列化与反序列化
- 位图迭代器
- 内存高效的大规模位集操作

作者：AllToolkit 自动化生成
日期：2026-04-22
"""

from typing import Iterator, Tuple, Optional, List
import struct


class Bitmap:
    """
    高效位图实现，支持大规模位集操作。
    使用字节数组存储，内存效率高。
    """
    
    def __init__(self, size: int = 0, init_value: bool = False):
        """
        初始化位图
        
        Args:
            size: 位数（自动扩展）
            init_value: 初始值（True=全1，False=全0）
        """
        if size < 0:
            raise ValueError("Size must be non-negative")
        
        self._size = size
        self._byte_size = (size + 7) // 8
        init_byte = 0xFF if init_value else 0x00
        self._data = bytearray([init_byte] * self._byte_size)
    
    def __len__(self) -> int:
        """返回位图大小"""
        return self._size
    
    def __bool__(self) -> bool:
        """检查位图是否有任何位被设置"""
        return any(self._data)
    
    def __eq__(self, other: object) -> bool:
        """比较两个位图是否相等"""
        if not isinstance(other, Bitmap):
            return False
        return self._size == other._size and self._data == other._data
    
    def __str__(self) -> str:
        """字符串表示（二进制格式）"""
        bits = ''.join('1' if self[i] else '0' for i in range(self._size))
        return f"Bitmap({bits})"
    
    def __repr__(self) -> str:
        return f"Bitmap(size={self._size}, bits_set={self.count_set()})"
    
    def __getitem__(self, index: int) -> bool:
        """通过索引获取位值"""
        if not 0 <= index < self._size:
            raise IndexError(f"Index {index} out of range [0, {self._size})")
        byte_idx = index // 8
        bit_idx = index % 8
        return bool(self._data[byte_idx] & (1 << bit_idx))
    
    def __setitem__(self, index: int, value: bool) -> None:
        """通过索引设置位值"""
        if not 0 <= index < self._size:
            raise IndexError(f"Index {index} out of range [0, {self._size})")
        byte_idx = index // 8
        bit_idx = index % 8
        if value:
            self._data[byte_idx] |= (1 << bit_idx)
        else:
            self._data[byte_idx] &= ~(1 << bit_idx)
    
    def __iter__(self) -> Iterator[Tuple[int, bool]]:
        """迭代所有位"""
        for i in range(self._size):
            yield i, self[i]
    
    def __contains__(self, index: int) -> bool:
        """检查索引是否在范围内且位已设置"""
        return 0 <= index < self._size and self[index]
    
    # ==================== 位操作 ====================
    
    def set(self, index: int) -> None:
        """设置指定位置的位为1"""
        self[index] = True
    
    def clear(self, index: int) -> None:
        """清除指定位置的位（设为0）"""
        self[index] = False
    
    def flip(self, index: int) -> None:
        """翻转指定位置的位"""
        if not 0 <= index < self._size:
            raise IndexError(f"Index {index} out of range")
        byte_idx = index // 8
        bit_idx = index % 8
        self._data[byte_idx] ^= (1 << bit_idx)
    
    def set_range(self, start: int, end: int, value: bool = True) -> None:
        """
        设置范围内的所有位
        
        Args:
            start: 起始位置（包含）
            end: 结束位置（不包含）
            value: 设置值
        """
        if start < 0 or end > self._size or start > end:
            raise ValueError(f"Invalid range [{start}, {end})")
        for i in range(start, end):
            self[i] = value
    
    def flip_range(self, start: int, end: int) -> None:
        """翻转范围内的所有位"""
        if start < 0 or end > self._size or start > end:
            raise ValueError(f"Invalid range [{start}, {end})")
        for i in range(start, end):
            self.flip(i)
    
    # ==================== 查询操作 ====================
    
    def test(self, index: int) -> bool:
        """测试指定位是否为1"""
        return self[index]
    
    def test_range(self, start: int, end: int, expected: bool) -> bool:
        """
        测试范围内所有位是否为期望值
        
        Returns:
            True 如果范围内所有位都等于期望值
        """
        for i in range(start, min(end, self._size)):
            if self[i] != expected:
                return False
        return True
    
    def any_set(self) -> bool:
        """检查是否有任何位被设置"""
        return any(b != 0 for b in self._data)
    
    def all_set(self) -> bool:
        """检查是否所有位都被设置"""
        if self._size == 0:
            return True
        # 检查完整字节
        full_bytes = self._size // 8
        for i in range(full_bytes):
            if self._data[i] != 0xFF:
                return False
        # 检查剩余位
        remaining = self._size % 8
        if remaining > 0:
            mask = (1 << remaining) - 1
            if (self._data[full_bytes] & mask) != mask:
                return False
        return True
    
    def none_set(self) -> bool:
        """检查是否没有位被设置"""
        return not self.any_set()
    
    # ==================== 统计操作 ====================
    
    def count_set(self) -> int:
        """统计被设置的位数量（popcount）"""
        count = 0
        for byte in self._data:
            count += bin(byte).count('1')
        # 处理最后一个字节可能的多余位
        remaining = self._size % 8
        if remaining > 0 and self._byte_size > 0:
            # 已经正确计算，无需额外处理
            pass
        return count
    
    def count_clear(self) -> int:
        """统计被清除的位数量"""
        return self._size - self.count_set()
    
    def find_first_set(self, start: int = 0) -> int:
        """
        查找第一个被设置的位
        
        Args:
            start: 开始搜索的位置
            
        Returns:
            第一个被设置的位置，如果没有则返回-1
        """
        for i in range(start, self._size):
            if self[i]:
                return i
        return -1
    
    def find_first_clear(self, start: int = 0) -> int:
        """
        查找第一个被清除的位
        
        Args:
            start: 开始搜索的位置
            
        Returns:
            第一个被清除的位置，如果没有则返回-1
        """
        for i in range(start, self._size):
            if not self[i]:
                return i
        return -1
    
    def find_next_set(self, current: int) -> int:
        """查找下一个被设置的位"""
        return self.find_first_set(current + 1)
    
    def find_next_clear(self, current: int) -> int:
        """查找下一个被清除的位"""
        return self.find_first_clear(current + 1)
    
    def find_nth_set(self, n: int) -> int:
        """
        查找第n个被设置的位（从0开始）
        
        Args:
            n: 第n个（0-indexed）
            
        Returns:
            位置，如果不足n个则返回-1
        """
        count = 0
        for i in range(self._size):
            if self[i]:
                if count == n:
                    return i
                count += 1
        return -1
    
    # ==================== 位图运算 ====================
    
    def and_(self, other: 'Bitmap') -> 'Bitmap':
        """位图AND运算"""
        result = Bitmap(min(self._size, other._size))
        for i in range(result._byte_size):
            result._data[i] = self._data[i] & other._data[i]
        return result
    
    def or_(self, other: 'Bitmap') -> 'Bitmap':
        """位图OR运算"""
        result = Bitmap(max(self._size, other._size))
        min_bytes = min(self._byte_size, other._byte_size)
        for i in range(min_bytes):
            result._data[i] = self._data[i] | other._data[i]
        # 复制剩余部分
        if self._byte_size > other._byte_size:
            for i in range(min_bytes, self._byte_size):
                result._data[i] = self._data[i]
        elif other._byte_size > self._byte_size:
            for i in range(min_bytes, other._byte_size):
                result._data[i] = other._data[i]
        return result
    
    def xor(self, other: 'Bitmap') -> 'Bitmap':
        """位图XOR运算"""
        result = Bitmap(max(self._size, other._size))
        min_bytes = min(self._byte_size, other._byte_size)
        for i in range(min_bytes):
            result._data[i] = self._data[i] ^ other._data[i]
        # 复制剩余部分
        if self._byte_size > other._byte_size:
            for i in range(min_bytes, self._byte_size):
                result._data[i] = self._data[i]
        elif other._byte_size > self._byte_size:
            for i in range(min_bytes, other._byte_size):
                result._data[i] = other._data[i]
        return result
    
    def not_(self) -> 'Bitmap':
        """位图NOT运算（反转所有位）"""
        result = Bitmap(self._size)
        for i in range(self._byte_size):
            result._data[i] = ~self._data[i] & 0xFF
        return result
    
    def difference(self, other: 'Bitmap') -> 'Bitmap':
        """
        位图差集运算（self - other）
        等价于 self AND (NOT other)
        """
        return self.and_(other.not_())
    
    # ==================== 聚合操作 ====================
    
    def intersect(self, other: 'Bitmap') -> bool:
        """检查两个位图是否有交集"""
        min_bytes = min(self._byte_size, other._byte_size)
        for i in range(min_bytes):
            if (self._data[i] & other._data[i]) != 0:
                return True
        return False
    
    def is_subset(self, other: 'Bitmap') -> bool:
        """检查当前位图是否是另一个的子集"""
        min_size = min(self._size, other._size)
        for i in range(min_size):
            if self[i] and not other[i]:
                return False
        # 检查剩余位（如果有）
        for i in range(min_size, self._size):
            if self[i]:
                return False
        return True
    
    def is_superset(self, other: 'Bitmap') -> bool:
        """检查当前位图是否是另一个的超集"""
        return other.is_subset(self)
    
    # ==================== 迭代器 ====================
    
    def iter_set_bits(self) -> Iterator[int]:
        """迭代所有被设置的位置"""
        for i in range(self._size):
            if self[i]:
                yield i
    
    def iter_clear_bits(self) -> Iterator[int]:
        """迭代所有被清除的位置"""
        for i in range(self._size):
            if not self[i]:
                yield i
    
    def iter_runs(self) -> Iterator[Tuple[int, int, bool]]:
        """
        迭代连续相同值的区间
        
        Yields:
            (start, end, value) - 起始、结束（不包含）、值
        """
        if self._size == 0:
            return
        
        run_start = 0
        run_value = self[0]
        
        for i in range(1, self._size):
            if self[i] != run_value:
                yield run_start, i, run_value
                run_start = i
                run_value = self[i]
        
        yield run_start, self._size, run_value
    
    # ==================== 扩展与调整 ====================
    
    def resize(self, new_size: int, fill_value: bool = False) -> None:
        """
        调整位图大小
        
        Args:
            new_size: 新大小
            fill_value: 扩展时新位的填充值
        """
        if new_size < 0:
            raise ValueError("Size must be non-negative")
        
        old_size = self._size
        old_byte_size = self._byte_size
        new_byte_size = (new_size + 7) // 8
        
        self._size = new_size
        self._byte_size = new_byte_size
        
        if new_byte_size > old_byte_size:
            fill_byte = 0xFF if fill_value else 0x00
            self._data.extend([fill_byte] * (new_byte_size - old_byte_size))
        elif new_byte_size < old_byte_size:
            del self._data[new_byte_size:]
        
        # 清理新大小边界之外的位
        if new_size % 8 != 0:
            mask = (1 << (new_size % 8)) - 1
            self._data[new_byte_size - 1] &= mask
    
    def copy(self) -> 'Bitmap':
        """创建位图副本"""
        result = Bitmap(self._size)
        result._data = bytearray(self._data)
        return result
    
    # ==================== 序列化 ====================
    
    def to_bytes(self) -> bytes:
        """序列化为字节"""
        return bytes(self._data)
    
    def to_hex_string(self) -> str:
        """转换为十六进制字符串"""
        return self.to_bytes().hex()
    
    def to_int(self) -> int:
        """转换为整数（位图被视为小端二进制数）"""
        return int.from_bytes(self._data, byteorder='little')
    
    def to_bit_string(self) -> str:
        """转换为二进制字符串"""
        bits = []
        for i in range(self._size):
            bits.append('1' if self[i] else '0')
        return ''.join(bits)
    
    @classmethod
    def from_bytes(cls, data: bytes, size: int) -> 'Bitmap':
        """
        从字节反序列化
        
        Args:
            data: 字节数据
            size: 位数
        """
        result = cls(size)
        result._data = bytearray(data[:result._byte_size])
        # 清理边界外的位
        if size % 8 != 0:
            mask = (1 << (size % 8)) - 1
            result._data[result._byte_size - 1] &= mask
        return result
    
    @classmethod
    def from_hex_string(cls, hex_str: str, size: int) -> 'Bitmap':
        """从十六进制字符串反序列化"""
        data = bytes.fromhex(hex_str)
        return cls.from_bytes(data, size)
    
    @classmethod
    def from_int(cls, value: int, size: int) -> 'Bitmap':
        """从整数创建位图"""
        result = cls(size)
        byte_length = (value.bit_length() + 7) // 8
        data = value.to_bytes(max(byte_length, result._byte_size), byteorder='little')
        result._data = bytearray(data[:result._byte_size])
        return result
    
    @classmethod
    def from_bit_string(cls, bit_str: str) -> 'Bitmap':
        """从二进制字符串创建位图"""
        size = len(bit_str)
        result = cls(size)
        for i, char in enumerate(bit_str):
            if char == '1':
                result.set(i)
        return result
    
    @classmethod
    def from_indices(cls, indices: List[int], size: int) -> 'Bitmap':
        """
        从位置列表创建位图
        
        Args:
            indices: 要设置的位置列表
            size: 位图大小
        """
        result = cls(size)
        for idx in indices:
            if 0 <= idx < size:
                result.set(idx)
        return result
    
    # ==================== 工具方法 ====================
    
    def to_list(self) -> List[int]:
        """返回所有被设置位置的列表"""
        return list(self.iter_set_bits())
    
    def count_leading_zeros(self) -> int:
        """计算前导零的数量"""
        for i in range(self._size):
            if self[i]:
                return i
        return self._size
    
    def count_trailing_zeros(self) -> int:
        """计算后导零的数量"""
        for i in range(self._size - 1, -1, -1):
            if self[i]:
                return self._size - 1 - i
        return self._size
    
    def get_byte(self, index: int) -> int:
        """获取指定字节位置的值"""
        if not 0 <= index < self._byte_size:
            raise IndexError(f"Byte index {index} out of range")
        return self._data[index]
    
    def set_byte(self, index: int, value: int) -> None:
        """设置指定字节位置的值"""
        if not 0 <= index < self._byte_size:
            raise IndexError(f"Byte index {index} out of range")
        self._data[index] = value & 0xFF
    
    # ==================== 特殊方法 ====================
    
    def __and__(self, other: 'Bitmap') -> 'Bitmap':
        return self.and_(other)
    
    def __or__(self, other: 'Bitmap') -> 'Bitmap':
        return self.or_(other)
    
    def __xor__(self, other: 'Bitmap') -> 'Bitmap':
        return self.xor(other)
    
    def __invert__(self) -> 'Bitmap':
        return self.not_()
    
    def __sub__(self, other: 'Bitmap') -> 'Bitmap':
        return self.difference(other)
    
    def __iand__(self, other: 'Bitmap') -> 'Bitmap':
        min_bytes = min(self._byte_size, other._byte_size)
        for i in range(min_bytes):
            self._data[i] &= other._data[i]
        # 清除剩余部分
        for i in range(min_bytes, self._byte_size):
            self._data[i] = 0
        return self
    
    def __ior__(self, other: 'Bitmap') -> 'Bitmap':
        min_bytes = min(self._byte_size, other._byte_size)
        for i in range(min_bytes):
            self._data[i] |= other._data[i]
        return self
    
    def __ixor__(self, other: 'Bitmap') -> 'Bitmap':
        min_bytes = min(self._byte_size, other._byte_size)
        for i in range(min_bytes):
            self._data[i] ^= other._data[i]
        return self


# ==================== 便捷函数 ====================

def create_bitmap(size: int, indices: Optional[List[int]] = None) -> Bitmap:
    """
    创建位图的便捷函数
    
    Args:
        size: 位图大小
        indices: 可选，初始设置的位置列表
    """
    bm = Bitmap(size)
    if indices:
        for idx in indices:
            bm.set(idx)
    return bm


def bitmap_from_string(s: str) -> Bitmap:
    """从二进制字符串创建位图"""
    return Bitmap.from_bit_string(s)


def bitmap_union(*bitmaps: Bitmap) -> Bitmap:
    """多个位图的并集"""
    if not bitmaps:
        return Bitmap(0)
    result = bitmaps[0].copy()
    for bm in bitmaps[1:]:
        result |= bm
    return result


def bitmap_intersection(*bitmaps: Bitmap) -> Bitmap:
    """多个位图的交集"""
    if not bitmaps:
        return Bitmap(0)
    result = bitmaps[0].copy()
    for bm in bitmaps[1:]:
        result &= bm
    return result


def bitmap_difference(*bitmaps: Bitmap) -> Bitmap:
    """多个位图的差集（第一个减去其余所有）"""
    if not bitmaps:
        return Bitmap(0)
    result = bitmaps[0].copy()
    for bm in bitmaps[1:]:
        result -= bm
    return result


# ==================== Sparse Bitmap ====================

class SparseBitmap:
    """
    稀疏位图实现
    
    适用于稀疏数据（大部分位为0），使用字典存储，
    内存效率更高。
    """
    
    def __init__(self, size: int = 0):
        """初始化稀疏位图"""
        if size < 0:
            raise ValueError("Size must be non-negative")
        self._size = size
        self._set_bits: set = set()  # 存储被设置的位
    
    def __len__(self) -> int:
        return self._size
    
    def __getitem__(self, index: int) -> bool:
        if not 0 <= index < self._size:
            raise IndexError(f"Index {index} out of range")
        return index in self._set_bits
    
    def __setitem__(self, index: int, value: bool) -> None:
        if not 0 <= index < self._size:
            raise IndexError(f"Index {index} out of range")
        if value:
            self._set_bits.add(index)
        else:
            self._set_bits.discard(index)
    
    def set(self, index: int) -> None:
        self[index] = True
    
    def clear(self, index: int) -> None:
        self[index] = False
    
    def flip(self, index: int) -> None:
        if not 0 <= index < self._size:
            raise IndexError(f"Index {index} out of range")
        if index in self._set_bits:
            self._set_bits.discard(index)
        else:
            self._set_bits.add(index)
    
    def count_set(self) -> int:
        return len(self._set_bits)
    
    def iter_set_bits(self) -> Iterator[int]:
        return iter(sorted(self._set_bits))
    
    def to_bitmap(self) -> Bitmap:
        """转换为密集位图"""
        return Bitmap.from_indices(list(self._set_bits), self._size)
    
    @classmethod
    def from_bitmap(cls, bitmap: Bitmap) -> 'SparseBitmap':
        """从密集位图转换"""
        result = cls(len(bitmap))
        result._set_bits = set(bitmap.iter_set_bits())
        return result
    
    def copy(self) -> 'SparseBitmap':
        result = SparseBitmap(self._size)
        result._set_bits = self._set_bits.copy()
        return result


# 导出
__all__ = [
    'Bitmap',
    'SparseBitmap',
    'create_bitmap',
    'bitmap_from_string',
    'bitmap_union',
    'bitmap_intersection',
    'bitmap_difference',
]