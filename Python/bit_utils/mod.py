"""
位操作工具集 (Bit Utilities)
============================

提供全面的位操作功能，包括：
- 位运算基础操作
- 位掩码操作
- 位计数与位反转
- 位旋转
- 位字段操作
- 位集操作
- 位向量

零外部依赖，纯 Python 实现。

作者: AllToolkit
日期: 2026-04-16
版本: 1.0.0
"""

from typing import List, Optional, Tuple, Iterator, Union
from functools import reduce


class BitVector:
    """
    位向量类 - 高效的位数组实现
    
    支持动态大小的位数组操作，包括设置、清除、翻转、查询等。
    """
    
    def __init__(self, size: int, initial_value: int = 0):
        """
        初始化位向量
        
        Args:
            size: 位数组的大小（位数）
            initial_value: 初始值（整数）
        """
        if size < 0:
            raise ValueError("Size must be non-negative")
        self._size = size
        self._bits = initial_value & ((1 << size) - 1) if size > 0 else 0
    
    def __len__(self) -> int:
        return self._size
    
    def __getitem__(self, index: int) -> int:
        """获取指定位置的位值"""
        if index < 0:
            index = self._size + index
        if not 0 <= index < self._size:
            raise IndexError(f"Index {index} out of range")
        return (self._bits >> index) & 1
    
    def __setitem__(self, index: int, value: int):
        """设置指定位置的位值"""
        if index < 0:
            index = self._size + index
        if not 0 <= index < self._size:
            raise IndexError(f"Index {index} out of range")
        if value:
            self._bits |= (1 << index)
        else:
            self._bits &= ~(1 << index)
    
    def __str__(self) -> str:
        return self.to_binary_string()
    
    def __repr__(self) -> str:
        return f"BitVector(size={self._size}, bits={self._bits})"
    
    def __and__(self, other: 'BitVector') -> 'BitVector':
        if len(self) != len(other):
            raise ValueError("BitVectors must have the same size")
        return BitVector(self._size, self._bits & other._bits)
    
    def __or__(self, other: 'BitVector') -> 'BitVector':
        if len(self) != len(other):
            raise ValueError("BitVectors must have the same size")
        return BitVector(self._size, self._bits | other._bits)
    
    def __xor__(self, other: 'BitVector') -> 'BitVector':
        if len(self) != len(other):
            raise ValueError("BitVectors must have the same size")
        return BitVector(self._size, self._bits ^ other._bits)
    
    def __invert__(self) -> 'BitVector':
        mask = (1 << self._size) - 1
        return BitVector(self._size, (~self._bits) & mask)
    
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, BitVector):
            return False
        return self._size == other._size and self._bits == other._bits
    
    def set(self, index: int):
        """设置指定位为1"""
        self[index] = 1
    
    def clear(self, index: int):
        """清除指定位（设为0）"""
        self[index] = 0
    
    def flip(self, index: int):
        """翻转指定位"""
        if index < 0:
            index = self._size + index
        if not 0 <= index < self._size:
            raise IndexError(f"Index {index} out of range")
        self._bits ^= (1 << index)
    
    def flip_all(self):
        """翻转所有位"""
        mask = (1 << self._size) - 1
        self._bits = (~self._bits) & mask
    
    def count_set_bits(self) -> int:
        """统计1的个数"""
        return count_bits(self._bits)
    
    def count_clear_bits(self) -> int:
        """统计0的个数"""
        return self._size - self.count_set_bits()
    
    def to_int(self) -> int:
        """转换为整数"""
        return self._bits
    
    def to_binary_string(self, pad: bool = True) -> str:
        """
        转换为二进制字符串
        
        Args:
            pad: 是否用0填充到完整长度
        
        Returns:
            二进制字符串表示
        """
        if pad and self._size > 0:
            return format(self._bits, f'0{self._size}b')
        return bin(self._bits)[2:]
    
    def to_list(self) -> List[int]:
        """转换为位列表"""
        return [self[i] for i in range(self._size)]
    
    @classmethod
    def from_binary_string(cls, s: str) -> 'BitVector':
        """从二进制字符串创建"""
        size = len(s)
        value = int(s, 2) if size > 0 else 0
        return cls(size, value)
    
    @classmethod
    def from_list(cls, bits: List[int]) -> 'BitVector':
        """从位列表创建"""
        size = len(bits)
        value = 0
        for i, bit in enumerate(bits):
            if bit:
                value |= (1 << i)
        return cls(size, value)
    
    def find_first_set(self) -> int:
        """找到第一个设置为1的位索引，返回-1如果没有"""
        if self._bits == 0:
            return -1
        return find_first_set_bit(self._bits)
    
    def find_last_set(self) -> int:
        """找到最后一个设置为1的位索引，返回-1如果没有"""
        if self._bits == 0:
            return -1
        return find_last_set_bit(self._bits)
    
    def all_set(self) -> bool:
        """检查是否所有位都设置为1"""
        mask = (1 << self._size) - 1
        return self._bits == mask
    
    def any_set(self) -> bool:
        """检查是否有任何位设置为1"""
        return self._bits != 0
    
    def none_set(self) -> bool:
        """检查是否所有位都是0"""
        return self._bits == 0


class BitField:
    """
    位字段操作类 - 用于提取和设置整数的位字段
    """
    
    @staticmethod
    def extract(value: int, start: int, end: int) -> int:
        """
        从整数中提取位字段
        
        Args:
            value: 源整数
            start: 起始位（包含，从0开始）
            end: 结束位（不包含）
        
        Returns:
            提取的位字段值
        
        Example:
            >>> BitField.extract(0b10110100, 2, 5)
            0b110 (6)
        """
        if start < 0 or end < start:
            raise ValueError("Invalid bit range")
        width = end - start
        mask = (1 << width) - 1
        return (value >> start) & mask
    
    @staticmethod
    def insert(value: int, start: int, end: int, field_value: int) -> int:
        """
        将位字段插入整数
        
        Args:
            value: 目标整数
            start: 起始位（包含，从0开始）
            end: 结束位（不包含）
            field_value: 要插入的位字段值
        
        Returns:
            插入后的整数值
        
        Example:
            >>> BitField.insert(0b10110100, 2, 5, 0b111)
            0b10111100 (188)
        """
        if start < 0 or end < start:
            raise ValueError("Invalid bit range")
        width = end - start
        mask = (1 << width) - 1
        if field_value > mask:
            raise ValueError(f"Field value {field_value} exceeds {width} bits")
        # 清除目标位
        value &= ~(mask << start)
        # 插入新值
        value |= (field_value & mask) << start
        return value
    
    @staticmethod
    def get_bit(value: int, position: int) -> int:
        """获取指定位置的位值"""
        if position < 0:
            raise ValueError("Position must be non-negative")
        return (value >> position) & 1
    
    @staticmethod
    def set_bit(value: int, position: int) -> int:
        """设置指定位置的位为1"""
        if position < 0:
            raise ValueError("Position must be non-negative")
        return value | (1 << position)
    
    @staticmethod
    def clear_bit(value: int, position: int) -> int:
        """清除指定位置的位（设为0）"""
        if position < 0:
            raise ValueError("Position must be non-negative")
        return value & ~(1 << position)
    
    @staticmethod
    def toggle_bit(value: int, position: int) -> int:
        """翻转指定位置的位"""
        if position < 0:
            raise ValueError("Position must be non-negative")
        return value ^ (1 << position)


class BitMask:
    """
    位掩码工具类 - 创建和操作位掩码
    """
    
    @staticmethod
    def create_mask(bits: List[int]) -> int:
        """
        从位位置列表创建掩码
        
        Args:
            bits: 位位置列表（从0开始）
        
        Returns:
            掩码值
        
        Example:
            >>> BitMask.create_mask([0, 2, 4])
            0b10101 (21)
        """
        mask = 0
        for bit in bits:
            if bit < 0:
                raise ValueError("Bit position must be non-negative")
            mask |= (1 << bit)
        return mask
    
    @staticmethod
    def create_range_mask(start: int, end: int) -> int:
        """
        创建指定范围的连续掩码
        
        Args:
            start: 起始位（包含）
            end: 结束位（不包含）
        
        Returns:
            掩码值
        
        Example:
            >>> BitMask.create_range_mask(2, 6)
            0b111100 (60)
        """
        if start < 0 or end < start:
            raise ValueError("Invalid range")
        return ((1 << (end - start)) - 1) << start
    
    @staticmethod
    def get_set_positions(mask: int) -> List[int]:
        """
        获取掩码中所有设置为1的位位置
        
        Args:
            mask: 掩码值
        
        Returns:
            位位置列表
        
        Example:
            >>> BitMask.get_set_positions(0b10101)
            [0, 2, 4]
        """
        positions = []
        pos = 0
        while mask:
            if mask & 1:
                positions.append(pos)
            mask >>= 1
            pos += 1
        return positions
    
    @staticmethod
    def apply_mask(value: int, mask: int) -> int:
        """应用掩码（与操作）"""
        return value & mask
    
    @staticmethod
    def combine_masks(*masks: int) -> int:
        """组合多个掩码（或操作）"""
        return reduce(lambda a, b: a | b, masks, 0)
    
    @staticmethod
    def invert_mask(mask: int, width: int) -> int:
        """
        反转掩码
        
        Args:
            mask: 原始掩码
            width: 位数
        
        Returns:
            反转后的掩码
        """
        return (~mask) & ((1 << width) - 1)


# ==================== 位计数函数 ====================

def count_bits(value: int) -> int:
    """
    计算整数中1的个数（汉明重量/人口计数）
    
    使用 Brian Kernighan 算法优化
    
    Args:
        value: 要计算的整数
    
    Returns:
        1的个数
    
    Example:
        >>> count_bits(0b10110101)
        5
    """
    if value < 0:
        raise ValueError("Value must be non-negative")
    count = 0
    while value:
        value &= value - 1  # 清除最低位的1
        count += 1
    return count


def count_zeros(value: int, width: int) -> int:
    """
    计算整数中0的个数
    
    Args:
        value: 要计算的整数
        width: 总位数
    
    Returns:
        0的个数
    """
    if value < 0:
        raise ValueError("Value must be non-negative")
    if width < 0:
        raise ValueError("Width must be non-negative")
    return width - count_bits(value)


def parity(value: int) -> int:
    """
    计算奇偶校验位
    
    Args:
        value: 要计算的整数
    
    Returns:
        0表示偶数个1，1表示奇数个1
    
    Example:
        >>> parity(0b1011)
        1
        >>> parity(0b1010)
        0
    """
    if value < 0:
        raise ValueError("Value must be non-negative")
    # 使用 XOR 折叠技术
    value ^= value >> 32
    value ^= value >> 16
    value ^= value >> 8
    value ^= value >> 4
    value ^= value >> 2
    value ^= value >> 1
    return value & 1


# ==================== 位查找函数 ====================

def find_first_set_bit(value: int) -> int:
    """
    找到第一个设置为1的位索引（从最低位开始）
    
    Args:
        value: 要搜索的整数
    
    Returns:
        位索引，如果没有则返回-1
    
    Example:
        >>> find_first_set_bit(0b10100000)
        5
        >>> find_first_set_bit(0)
        -1
    """
    if value < 0:
        raise ValueError("Value must be non-negative")
    if value == 0:
        return -1
    
    # 使用内置方法
    # 找到最低位的1，通过 value & -value 得到只有最低位1的值
    # 然后 bit_length() - 1 得到位置
    lowest_bit = value & -value
    return lowest_bit.bit_length() - 1


def find_last_set_bit(value: int) -> int:
    """
    找到最后一个设置为1的位索引（从最高有效位开始）
    
    Args:
        value: 要搜索的整数
    
    Returns:
        位索引，如果没有则返回-1
    
    Example:
        >>> find_last_set_bit(0b10100000)
        7
        >>> find_last_set_bit(0)
        -1
    """
    if value < 0:
        raise ValueError("Value must be non-negative")
    if value == 0:
        return -1
    
    # 使用 bit_length() 获取最高位位置
    # bit_length() 返回表示该数所需的最少位数
    # 最高位位置 = bit_length() - 1
    return value.bit_length() - 1


def find_nth_set_bit(value: int, n: int) -> int:
    """
    找到第n个设置为1的位索引
    
    Args:
        value: 要搜索的整数
        n: 第n个1（从1开始计数）
    
    Returns:
        位索引，如果不够则返回-1
    
    Example:
        >>> find_nth_set_bit(0b10110100, 3)
        4
    """
    if value < 0:
        raise ValueError("Value must be non-negative")
    if n < 1:
        raise ValueError("n must be positive")
    
    count = 0
    pos = 0
    while value:
        if value & 1:
            count += 1
            if count == n:
                return pos
        value >>= 1
        pos += 1
    return -1


# ==================== 位反转函数 ====================

def reverse_bits(value: int, width: int) -> int:
    """
    反转整数的所有位
    
    Args:
        value: 要反转的整数
        width: 总位数
    
    Returns:
        反转后的整数
    
    Example:
        >>> bin(reverse_bits(0b10110010, 8))
        '0b01001101'
    """
    if value < 0:
        raise ValueError("Value must be non-negative")
    if width < 0:
        raise ValueError("Width must be non-negative")
    
    result = 0
    for _ in range(width):
        result = (result << 1) | (value & 1)
        value >>= 1
    return result


def reverse_bytes(value: int) -> int:
    """
    反转整数的字节顺序（字节序转换）
    
    Args:
        value: 要反转的整数
    
    Returns:
        反转字节序后的整数
    
    Example:
        >>> hex(reverse_bytes(0x12345678))
        '0x78563412'
    """
    if value < 0:
        raise ValueError("Value must be non-negative")
    
    result = 0
    while value:
        result = (result << 8) | (value & 0xFF)
        value >>= 8
    return result


# ==================== 位旋转函数 ====================

def rotate_left(value: int, shift: int, width: int) -> int:
    """
    循环左移
    
    Args:
        value: 要旋转的整数
        shift: 旋转位数
        width: 总位数
    
    Returns:
        旋转后的整数
    
    Example:
        >>> bin(rotate_left(0b10110001, 3, 8))
        '0b10001101'
    """
    if value < 0:
        raise ValueError("Value must be non-negative")
    if width <= 0:
        raise ValueError("Width must be positive")
    
    shift = shift % width
    if shift == 0:
        return value
    
    mask = (1 << width) - 1
    return ((value << shift) | (value >> (width - shift))) & mask


def rotate_right(value: int, shift: int, width: int) -> int:
    """
    循环右移
    
    Args:
        value: 要旋转的整数
        shift: 旋转位数
        width: 总位数
    
    Returns:
        旋转后的整数
    
    Example:
        >>> bin(rotate_right(0b10110001, 3, 8))
        '0b00110110'
    """
    if value < 0:
        raise ValueError("Value must be non-negative")
    if width <= 0:
        raise ValueError("Width must be positive")
    
    shift = shift % width
    if shift == 0:
        return value
    
    mask = (1 << width) - 1
    return ((value >> shift) | (value << (width - shift))) & mask


# ==================== 位操作辅助函数 ====================

def is_power_of_two(value: int) -> bool:
    """
    检查是否是2的幂
    
    Args:
        value: 要检查的整数
    
    Returns:
        是否是2的幂
    
    Example:
        >>> is_power_of_two(16)
        True
        >>> is_power_of_two(15)
        False
    """
    if value <= 0:
        return False
    return (value & (value - 1)) == 0


def next_power_of_two(value: int) -> int:
    """
    获取大于等于value的最小2的幂
    
    Args:
        value: 输入整数
    
    Returns:
        最小的2的幂
    
    Example:
        >>> next_power_of_two(15)
        16
        >>> next_power_of_two(16)
        16
    """
    if value <= 0:
        return 1
    value -= 1
    value |= value >> 1
    value |= value >> 2
    value |= value >> 4
    value |= value >> 8
    value |= value >> 16
    value |= value >> 32
    return value + 1


def previous_power_of_two(value: int) -> int:
    """
    获取小于等于value的最大2的幂
    
    Args:
        value: 输入整数
    
    Returns:
        最大的2的幂
    
    Example:
        >>> previous_power_of_two(17)
        16
        >>> previous_power_of_two(16)
        16
    """
    if value <= 1:
        return 1
    return 1 << (value.bit_length() - 1)


def gray_code(value: int) -> int:
    """
    将二进制转换为格雷码
    
    Args:
        value: 二进制值
    
    Returns:
        格雷码值
    
    Example:
        >>> bin(gray_code(5))
        '0b111'
    """
    if value < 0:
        raise ValueError("Value must be non-negative")
    return value ^ (value >> 1)


def gray_to_binary(value: int) -> int:
    """
    将格雷码转换为二进制
    
    Args:
        value: 格雷码值
    
    Returns:
        二进制值
    
    Example:
        >>> gray_to_binary(0b111)
        5
    """
    if value < 0:
        raise ValueError("Value must be non-negative")
    result = value
    value >>= 1
    while value:
        result ^= value
        value >>= 1
    return result


def sign_extend(value: int, from_width: int, to_width: int) -> int:
    """
    符号扩展
    
    Args:
        value: 要扩展的值
        from_width: 原始位数
        to_width: 目标位数
    
    Returns:
        符号扩展后的值
    
    Example:
        >>> bin(sign_extend(0b101, 3, 8))
        '0b11111101'
    """
    if value < 0:
        raise ValueError("Value must be non-negative")
    if from_width <= 0 or to_width < from_width:
        raise ValueError("Invalid width parameters")
    
    # 检查符号位
    sign_bit = (value >> (from_width - 1)) & 1
    if sign_bit == 0:
        return value
    
    # 创建符号扩展掩码
    mask = ((1 << to_width) - 1) ^ ((1 << from_width) - 1)
    return value | mask


def swap_bits(value: int, i: int, j: int) -> int:
    """
    交换两个位的值
    
    Args:
        value: 原始值
        i: 第一个位位置
        j: 第二个位位置
    
    Returns:
        交换后的值
    
    Example:
        >>> bin(swap_bits(0b10100001, 0, 5))
        '0b10000101'
    """
    if i < 0 or j < 0:
        raise ValueError("Bit positions must be non-negative")
    
    # 如果两个位相同，无需交换
    bit_i = (value >> i) & 1
    bit_j = (value >> j) & 1
    if bit_i == bit_j:
        return value
    
    # 翻转两个位
    return value ^ ((1 << i) | (1 << j))


def align_up(value: int, alignment: int) -> int:
    """
    向上对齐到指定边界
    
    Args:
        value: 原始值
        alignment: 对齐值（必须是2的幂）
    
    Returns:
        对齐后的值
    
    Example:
        >>> align_up(100, 16)
        112
    """
    if value < 0:
        raise ValueError("Value must be non-negative")
    if not is_power_of_two(alignment):
        raise ValueError("Alignment must be power of 2")
    return (value + alignment - 1) & ~(alignment - 1)


def align_down(value: int, alignment: int) -> int:
    """
    向下对齐到指定边界
    
    Args:
        value: 原始值
        alignment: 对齐值（必须是2的幂）
    
    Returns:
        对齐后的值
    
    Example:
        >>> align_down(100, 16)
        96
    """
    if value < 0:
        raise ValueError("Value must be non-negative")
    if not is_power_of_two(alignment):
        raise ValueError("Alignment must be power of 2")
    return value & ~(alignment - 1)


def to_binary_string(value: int, width: Optional[int] = None, 
                     group_size: Optional[int] = None, 
                     separator: str = ' ') -> str:
    """
    将整数转换为格式化的二进制字符串
    
    Args:
        value: 要转换的整数
        width: 最小宽度（用0填充）
        group_size: 分组大小（用于可读性）
        separator: 分组分隔符
    
    Returns:
        格式化的二进制字符串
    
    Example:
        >>> to_binary_string(0xABCD, width=16, group_size=4)
        '1010 1011 1100 1101'
    """
    if value < 0:
        raise ValueError("Value must be non-negative")
    
    if width is None:
        width = max(1, value.bit_length())
    
    binary = format(value, f'0{width}b')
    
    if group_size is not None and group_size > 0:
        groups = [binary[i:i+group_size] for i in range(0, len(binary), group_size)]
        binary = separator.join(groups)
    
    return binary


def from_binary_string(s: str) -> int:
    """
    从二进制字符串解析整数
    
    Args:
        s: 二进制字符串（可以包含空格、下划线、0b前缀）
    
    Returns:
        整数值
    
    Example:
        >>> from_binary_string('1010 1011 1100 1101')
        43981
    """
    # 移除前缀和分隔符
    s = s.replace('0b', '').replace(' ', '').replace('_', '')
    return int(s, 2) if s else 0


def to_hex_string(value: int, width: Optional[int] = None,
                  prefix: bool = True, uppercase: bool = False) -> str:
    """
    将整数转换为格式化的十六进制字符串
    
    Args:
        value: 要转换的整数
        width: 最小宽度（用0填充）
        prefix: 是否添加0x前缀
        uppercase: 是否使用大写字母
    
    Returns:
        格式化的十六进制字符串
    
    Example:
        >>> to_hex_string(255, width=4, uppercase=True)
        '0x00FF'
    """
    if value < 0:
        raise ValueError("Value must be non-negative")
    
    if width is None:
        width = 1
    else:
        width = max(1, width)
    
    hex_str = format(value, f'0{width}{"X" if uppercase else "x"}')
    return f'0x{hex_str}' if prefix else hex_str


# ==================== 位集合操作 ====================

def create_bitset(elements: List[int]) -> int:
    """
    从整数列表创建位集合
    
    Args:
        elements: 元素列表
    
    Returns:
        位集合（掩码）
    
    Example:
        >>> bin(create_bitset([0, 2, 4]))
        '0b10101'
    """
    return BitMask.create_mask(elements)


def bitset_union(*bitsets: int) -> int:
    """
    位集合并集
    
    Args:
        *bitsets: 位集合
    
    Returns:
        并集
    
    Example:
        >>> bin(bitset_union(0b101, 0b011))
        '0b111'
    """
    return reduce(lambda a, b: a | b, bitsets, 0)


def bitset_intersection(*bitsets: int) -> int:
    """
    位集合交集
    
    Args:
        *bitsets: 位集合
    
    Returns:
        交集
    
    Example:
        >>> bin(bitset_intersection(0b101, 0b011))
        '0b001'
    """
    if not bitsets:
        return 0
    return reduce(lambda a, b: a & b, bitsets)


def bitset_difference(a: int, b: int) -> int:
    """
    位集合差集 (a - b)
    
    Args:
        a: 第一个位集合
        b: 第二个位集合
    
    Returns:
        差集
    
    Example:
        >>> bin(bitset_difference(0b111, 0b011))
        '0b100'
    """
    return a & ~b


def bitset_symmetric_difference(a: int, b: int) -> int:
    """
    位集合对称差（异或）
    
    Args:
        a: 第一个位集合
        b: 第二个位集合
    
    Returns:
        对称差
    
    Example:
        >>> bin(bitset_symmetric_difference(0b101, 0b011))
        '0b110'
    """
    return a ^ b


def bitset_is_subset(a: int, b: int) -> bool:
    """
    检查a是否是b的子集
    
    Args:
        a: 第一个位集合
        b: 第二个位集合
    
    Returns:
        是否是子集
    
    Example:
        >>> bitset_is_subset(0b101, 0b111)
        True
    """
    return (a & b) == a


def bitset_is_superset(a: int, b: int) -> bool:
    """
    检查a是否是b的超集
    
    Args:
        a: 第一个位集合
        b: 第二个位集合
    
    Returns:
        是否是超集
    
    Example:
        >>> bitset_is_superset(0b111, 0b101)
        True
    """
    return (a & b) == b


def bitset_to_list(bitset: int) -> List[int]:
    """
    将位集合转换为元素列表
    
    Args:
        bitset: 位集合
    
    Returns:
        元素列表
    
    Example:
        >>> bitset_to_list(0b10101)
        [0, 2, 4]
    """
    return BitMask.get_set_positions(bitset)


def iterate_bits(value: int, width: int) -> Iterator[Tuple[int, int]]:
    """
    迭代整数的每一位，返回 (位置, 值) 元组
    
    Args:
        value: 要迭代的整数
        width: 总位数
    
    Yields:
        (位置, 值) 元组
    
    Example:
        >>> list(iterate_bits(0b101, 4))
        [(0, 1), (1, 0), (2, 1), (3, 0)]
    """
    for i in range(width):
        yield (i, (value >> i) & 1)


def most_significant_bit(value: int) -> int:
    """
    获取最高有效位的位置
    
    Args:
        value: 整数值
    
    Returns:
        最高有效位位置（从0开始），如果是0则返回-1
    
    Example:
        >>> most_significant_bit(0b10000)
        4
    """
    return find_last_set_bit(value)


def least_significant_bit(value: int) -> int:
    """
    获取最低有效位的位置
    
    Args:
        value: 整数值
    
    Returns:
        最低有效位位置（从0开始），如果是0则返回-1
    
    Example:
        >>> least_significant_bit(0b10100)
        2
    """
    return find_first_set_bit(value)


# 导出公共API
__all__ = [
    # 类
    'BitVector',
    'BitField',
    'BitMask',
    # 位计数
    'count_bits',
    'count_zeros',
    'parity',
    # 位查找
    'find_first_set_bit',
    'find_last_set_bit',
    'find_nth_set_bit',
    'most_significant_bit',
    'least_significant_bit',
    # 位反转
    'reverse_bits',
    'reverse_bytes',
    # 位旋转
    'rotate_left',
    'rotate_right',
    # 位操作
    'is_power_of_two',
    'next_power_of_two',
    'previous_power_of_two',
    'gray_code',
    'gray_to_binary',
    'sign_extend',
    'swap_bits',
    'align_up',
    'align_down',
    # 格式化
    'to_binary_string',
    'from_binary_string',
    'to_hex_string',
    # 位集合
    'create_bitset',
    'bitset_union',
    'bitset_intersection',
    'bitset_difference',
    'bitset_symmetric_difference',
    'bitset_is_subset',
    'bitset_is_superset',
    'bitset_to_list',
    # 迭代
    'iterate_bits',
]