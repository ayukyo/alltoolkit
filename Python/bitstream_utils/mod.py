"""
Bitstream Utils - 位流操作工具库

提供高效的位级别数据操作功能，包括：
- 位流读写器
- 位级别序列化/反序列化
- 变长整数编码（Varint, LEB128）
- 位操作工具函数
- 位图操作

零外部依赖，纯Python实现
"""

from typing import Optional, Union, Iterator


class BitReader:
    """
    位流读取器 - 从字节数据中按位读取
    
    支持读取任意位数的整数、变长整数、布尔值等
    适用于解析压缩数据、网络协议、文件格式等
    """
    
    def __init__(self, data: bytes):
        """
        初始化位读取器
        
        Args:
            data: 要读取的字节数据
        """
        self._data = data
        self._byte_pos = 0
        self._bit_pos = 0
    
    @property
    def data(self) -> bytes:
        """返回原始数据"""
        return self._data
    
    @property
    def byte_position(self) -> int:
        """当前字节位置"""
        return self._byte_pos
    
    @property
    def bit_position(self) -> int:
        """当前位位置（在当前字节内，0-7）"""
        return self._bit_pos
    
    @property
    def total_bits(self) -> int:
        """总位数"""
        return len(self._data) * 8
    
    @property
    def remaining_bits(self) -> int:
        """剩余可读位数"""
        return self.total_bits - (self._byte_pos * 8 + self._bit_pos)
    
    @property
    def remaining_bytes(self) -> int:
        """剩余可读字节数"""
        return len(self._data) - self._byte_pos
    
    @property
    def is_empty(self) -> bool:
        """是否已读完"""
        return self.remaining_bits <= 0
    
    def read_bit(self) -> int:
        """
        读取单个位
        
        Returns:
            0 或 1
            
        Raises:
            EOFError: 数据已读完
        """
        if self._byte_pos >= len(self._data):
            raise EOFError("No more data to read")
        
        # 从高位到低位读取
        bit = (self._data[self._byte_pos] >> (7 - self._bit_pos)) & 1
        
        self._bit_pos += 1
        if self._bit_pos >= 8:
            self._bit_pos = 0
            self._byte_pos += 1
        
        return bit
    
    def read_bits(self, n: int) -> int:
        """
        读取指定位数的整数（大端序，高位在前）
        
        Args:
            n: 要读取的位数（1-64）
            
        Returns:
            读取的整数值
            
        Raises:
            ValueError: 位数无效
            EOFError: 数据不足
        """
        if n < 0 or n > 64:
            raise ValueError(f"Invalid bit count: {n}, must be 0-64")
        
        if n == 0:
            return 0
        
        result = 0
        for _ in range(n):
            result = (result << 1) | self.read_bit()
        
        return result
    
    def read_bits_le(self, n: int) -> int:
        """
        读取指定位数的整数（小端序，低位在前）
        
        Args:
            n: 要读取的位数（1-64）
            
        Returns:
            读取的整数值
        """
        if n < 0 or n > 64:
            raise ValueError(f"Invalid bit count: {n}, must be 0-64")
        
        if n == 0:
            return 0
        
        result = 0
        for i in range(n):
            result |= self.read_bit() << i
        
        return result
    
    def read_byte(self) -> int:
        """读取一个字节"""
        return self.read_bits(8)
    
    def read_bytes(self, n: int) -> bytes:
        """
        读取指定数量的字节
        
        Args:
            n: 要读取的字节数
            
        Returns:
            读取的字节数据
        """
        result = bytearray()
        for _ in range(n):
            result.append(self.read_byte())
        return bytes(result)
    
    def read_bool(self) -> bool:
        """读取一个布尔值（1位）"""
        return self.read_bit() == 1
    
    def read_uint8(self) -> int:
        """读取无符号8位整数"""
        return self.read_bits(8)
    
    def read_uint16_be(self) -> int:
        """读取大端序无符号16位整数"""
        return self.read_bits(16)
    
    def read_uint16_le(self) -> int:
        """读取小端序无符号16位整数"""
        return self.read_bits_le(16)
    
    def read_uint32_be(self) -> int:
        """读取大端序无符号32位整数"""
        return self.read_bits(32)
    
    def read_uint32_le(self) -> int:
        """读取小端序无符号32位整数"""
        return self.read_bits_le(32)
    
    def read_uint64_be(self) -> int:
        """读取大端序无符号64位整数"""
        return self.read_bits(64)
    
    def read_uint64_le(self) -> int:
        """读取小端序无符号64位整数"""
        return self.read_bits_le(64)
    
    def read_varint(self) -> int:
        """
        读取变长整数（Varint格式）
        
        每字节的最高位表示是否还有后续字节，
        低7位为实际数据。小端序存储。
        
        Returns:
            解码后的整数
        """
        result = 0
        shift = 0
        
        while True:
            byte = self.read_byte()
            result |= (byte & 0x7F) << shift
            
            if (byte & 0x80) == 0:
                break
            
            shift += 7
            if shift > 63:
                raise ValueError("Varint too long")
        
        return result
    
    def read_leb128_unsigned(self) -> int:
        """
        读取LEB128编码的无符号整数
        
        LEB128 (Little Endian Base 128)
        常用于 DWARF 调试格式、WebAssembly 等
        
        Returns:
            解码后的整数
        """
        return self.read_varint()  # 与 varint 格式相同
    
    def read_leb128_signed(self) -> int:
        """
        读取LEB128编码的有符号整数
        
        Returns:
            解码后的有符号整数
        """
        result = 0
        shift = 0
        
        while True:
            byte = self.read_byte()
            result |= (byte & 0x7F) << shift
            shift += 7
            
            if (byte & 0x80) == 0:
                # 如果最高有效位为1，则扩展符号位
                if shift < 64 and (byte & 0x40):
                    result |= -(1 << shift)
                break
        
        return result
    
    def read_unary(self) -> int:
        """
        读取一元编码的整数
        
        格式：n个1后跟一个0，表示数值n
        例如：000 = 0, 100 = 1, 1100 = 2
        
        Returns:
            解码后的整数
        """
        count = 0
        while self.read_bit() == 1:
            count += 1
        return count
    
    def read_rice(self, k: int) -> int:
        """
        读取 Rice 编码的整数
        
        Args:
            k: Rice参数，表示尾数的位数
            
        Returns:
            解码后的整数
        """
        q = self.read_unary()
        r = self.read_bits(k)
        return (q << k) | r
    
    def read_gamma(self) -> int:
        """
        读取 Elias Gamma 编码的整数
        
        Returns:
            解码后的整数
        """
        # 计算前导零的数量
        n = 0
        while self.read_bit() == 0:
            n += 1
        
        if n == 0:
            return 1
        
        # 读取剩余的n位
        remaining = self.read_bits(n)
        return (1 << n) | remaining
    
    def read_delta(self) -> int:
        """
        读取 Elias Delta 编码的整数
        
        Returns:
            解码后的整数
        """
        # 先用Gamma解码得到L+1
        length = self.read_gamma()
        
        # L = length - 1
        n = length - 1
        
        if n == 0:
            return 1
        
        # 读取M（低n位）
        m = self.read_bits(n)
        
        # N = 2^n + M
        return (1 << n) + m
    
    def align_to_byte(self) -> None:
        """对齐到下一个字节边界"""
        if self._bit_pos > 0:
            self._bit_pos = 0
            self._byte_pos += 1
    
    def seek(self, bit_position: int) -> None:
        """
        跳转到指定位位置
        
        Args:
            bit_position: 目标位位置（从数据开始计算）
            
        Raises:
            ValueError: 位置超出范围
        """
        if bit_position < 0 or bit_position > self.total_bits:
            raise ValueError(f"Invalid position: {bit_position}")
        
        self._byte_pos = bit_position // 8
        self._bit_pos = bit_position % 8
    
    def peek_bits(self, n: int) -> int:
        """
        预览接下来的n位（不移动位置）
        
        Args:
            n: 要预览的位数
            
        Returns:
            预览的整数值
        """
        saved_byte_pos = self._byte_pos
        saved_bit_pos = self._bit_pos
        
        try:
            return self.read_bits(n)
        finally:
            self._byte_pos = saved_byte_pos
            self._bit_pos = saved_bit_pos
    
    def __repr__(self) -> str:
        return f"BitReader(pos={self._byte_pos * 8 + self._bit_pos}/{self.total_bits}, remaining={self.remaining_bits})"


class BitWriter:
    """
    位流写入器 - 按位写入数据
    
    支持写入任意位数的整数、变长整数、布尔值等
    """
    
    def __init__(self):
        """初始化位写入器"""
        self._buffer = bytearray()
        self._current_byte = 0
        self._bit_pos = 0
    
    @property
    def bit_length(self) -> int:
        """已写入的总位数"""
        return len(self._buffer) * 8 + self._bit_pos
    
    @property
    def byte_length(self) -> int:
        """已写入的总字节数（向上取整）"""
        return len(self._buffer) + (1 if self._bit_pos > 0 else 0)
    
    def write_bit(self, bit: int) -> None:
        """
        写入单个位
        
        Args:
            bit: 0 或 1
        """
        if bit:
            self._current_byte |= (1 << (7 - self._bit_pos))
        
        self._bit_pos += 1
        
        if self._bit_pos >= 8:
            self._buffer.append(self._current_byte)
            self._current_byte = 0
            self._bit_pos = 0
    
    def write_bits(self, value: int, n: int) -> None:
        """
        写入指定位数的整数（大端序，高位在前）
        
        Args:
            value: 要写入的值
            n: 要写入的位数
        """
        if n < 0 or n > 64:
            raise ValueError(f"Invalid bit count: {n}")
        
        for i in range(n - 1, -1, -1):
            self.write_bit((value >> i) & 1)
    
    def write_bits_le(self, value: int, n: int) -> None:
        """
        写入指定位数的整数（小端序，低位在前）
        
        Args:
            value: 要写入的值
            n: 要写入的位数
        """
        if n < 0 or n > 64:
            raise ValueError(f"Invalid bit count: {n}")
        
        for i in range(n):
            self.write_bit((value >> i) & 1)
    
    def write_byte(self, value: int) -> None:
        """写入一个字节"""
        self.write_bits(value, 8)
    
    def write_bytes(self, data: bytes) -> None:
        """写入字节数据"""
        for byte in data:
            self.write_byte(byte)
    
    def write_bool(self, value: bool) -> None:
        """写入布尔值"""
        self.write_bit(1 if value else 0)
    
    def write_uint8(self, value: int) -> None:
        """写入无符号8位整数"""
        self.write_bits(value, 8)
    
    def write_uint16_be(self, value: int) -> None:
        """写入大端序无符号16位整数"""
        self.write_bits(value, 16)
    
    def write_uint16_le(self, value: int) -> None:
        """写入小端序无符号16位整数"""
        self.write_bits_le(value, 16)
    
    def write_uint32_be(self, value: int) -> None:
        """写入大端序无符号32位整数"""
        self.write_bits(value, 32)
    
    def write_uint32_le(self, value: int) -> None:
        """写入小端序无符号32位整数"""
        self.write_bits_le(value, 32)
    
    def write_uint64_be(self, value: int) -> None:
        """写入大端序无符号64位整数"""
        self.write_bits(value, 64)
    
    def write_uint64_le(self, value: int) -> None:
        """写入小端序无符号64位整数"""
        self.write_bits_le(value, 64)
    
    def write_varint(self, value: int) -> None:
        """
        写入变长整数（Varint格式）
        
        Args:
            value: 要编码的整数
        """
        if value < 0:
            raise ValueError("Varint only supports non-negative integers")
        
        while value >= 0x80:
            self.write_byte((value & 0x7F) | 0x80)
            value >>= 7
        
        self.write_byte(value)
    
    def write_leb128_unsigned(self, value: int) -> None:
        """写入LEB128编码的无符号整数"""
        self.write_varint(value)
    
    def write_leb128_signed(self, value: int) -> None:
        """
        写入LEB128编码的有符号整数
        
        Args:
            value: 要编码的有符号整数
        """
        more = True
        while more:
            byte = value & 0x7F
            value >>= 7
            
            # 检查是否需要更多字节
            if (value == 0 and (byte & 0x40) == 0) or (value == -1 and (byte & 0x40) != 0):
                more = False
            else:
                byte |= 0x80
            
            self.write_byte(byte)
    
    def write_unary(self, value: int) -> None:
        """
        写入一元编码
        
        Args:
            value: 要编码的非负整数
        """
        for _ in range(value):
            self.write_bit(1)
        self.write_bit(0)
    
    def write_rice(self, value: int, k: int) -> None:
        """
        写入 Rice 编码
        
        Args:
            value: 要编码的整数
            k: Rice参数
        """
        q = value >> k
        r = value & ((1 << k) - 1)
        self.write_unary(q)
        self.write_bits(r, k)
    
    def write_gamma(self, value: int) -> None:
        """
        写入 Elias Gamma 编码
        
        Args:
            value: 要编码的正整数
        """
        if value < 1:
            raise ValueError("Gamma encoding requires positive integers")
        
        # 计算最高有效位的位置
        n = value.bit_length() - 1
        
        # 写入n个零
        for _ in range(n):
            self.write_bit(0)
        
        # 写入n位值
        self.write_bits(value, n + 1)
    
    def write_delta(self, value: int) -> None:
        """
        写入 Elias Delta 编码
        
        Args:
            value: 要编码的正整数
        """
        if value < 1:
            raise ValueError("Delta encoding requires positive integers")
        
        # 计算L = floor(log2(N))
        n = value.bit_length() - 1
        
        # 用Gamma编码L+1
        self.write_gamma(n + 1)
        
        # 写入剩余的n位（M = N - 2^n）
        if n > 0:
            self.write_bits(value & ((1 << n) - 1), n)
    
    def align_to_byte(self, padding: int = 0) -> None:
        """
        对齐到字节边界
        
        Args:
            padding: 填充位的值（0或1）
        """
        while self._bit_pos > 0:
            self.write_bit(padding)
    
    def get_bytes(self) -> bytes:
        """
        获取写入的字节数据
        
        Returns:
            完整的字节数据
        """
        if self._bit_pos > 0:
            return bytes(self._buffer) + bytes([self._current_byte])
        return bytes(self._buffer)
    
    def reset(self) -> None:
        """重置写入器"""
        self._buffer.clear()
        self._current_byte = 0
        self._bit_pos = 0
    
    def __repr__(self) -> str:
        return f"BitWriter(bits={self.bit_length}, bytes={self.byte_length})"


# ============ 工具函数 ============

def count_bits(value: int) -> int:
    """
    计算整数需要的最少位数
    
    Args:
        value: 非负整数
        
    Returns:
        所需位数
    """
    if value == 0:
        return 1
    return value.bit_length()


def count_set_bits(value: int) -> int:
    """
    计算整数中1的个数（popcount）
    
    Args:
        value: 整数
        
    Returns:
        1的个数
    """
    return bin(value).count('1')


def reverse_bits(value: int, width: int) -> int:
    """
    反转指定位数的整数
    
    Args:
        value: 要反转的值
        width: 位数
        
    Returns:
        反转后的值
    """
    result = 0
    for i in range(width):
        if value & (1 << i):
            result |= 1 << (width - 1 - i)
    return result


def rotate_left(value: int, shift: int, width: int) -> int:
    """
    循环左移
    
    Args:
        value: 要移位的值
        shift: 移位次数
        width: 数据宽度（位数）
        
    Returns:
        移位后的值
    """
    shift %= width
    return ((value << shift) | (value >> (width - shift))) & ((1 << width) - 1)


def rotate_right(value: int, shift: int, width: int) -> int:
    """
    循环右移
    
    Args:
        value: 要移位的值
        shift: 移位次数
        width: 数据宽度（位数）
        
    Returns:
        移位后的值
    """
    shift %= width
    return ((value >> shift) | (value << (width - shift))) & ((1 << width) - 1)


def get_bit(value: int, position: int) -> int:
    """
    获取指定位置的位值
    
    Args:
        value: 整数值
        position: 位位置（从低位开始，0起始）
        
    Returns:
        0 或 1
    """
    return (value >> position) & 1


def set_bit(value: int, position: int) -> int:
    """
    设置指定位置的位为1
    
    Args:
        value: 整数值
        position: 位位置
        
    Returns:
        设置后的值
    """
    return value | (1 << position)


def clear_bit(value: int, position: int) -> int:
    """
    清除指定位置的位（设为0）
    
    Args:
        value: 整数值
        position: 位位置
        
    Returns:
        清除后的值
    """
    return value & ~(1 << position)


def toggle_bit(value: int, position: int) -> int:
    """
    翻转指定位置的位
    
    Args:
        value: 整数值
        position: 位位置
        
    Returns:
        翻转后的值
    """
    return value ^ (1 << position)


def create_bitmask(start: int, end: int) -> int:
    """
    创建位掩码
    
    Args:
        start: 起始位（包含）
        end: 结束位（不包含）
        
    Returns:
        位掩码
    """
    return ((1 << (end - start)) - 1) << start


def extract_bits(value: int, start: int, length: int) -> int:
    """
    提取指定位段
    
    Args:
        value: 整数值
        start: 起始位
        length: 位长度
        
    Returns:
        提取的值
    """
    return (value >> start) & ((1 << length) - 1)


def insert_bits(target: int, source: int, start: int, length: int) -> int:
    """
    将源值的位插入目标值的指定位置
    
    Args:
        target: 目标值
        source: 源值
        start: 起始位置
        length: 位长度
        
    Returns:
        插入后的值
    """
    mask = ((1 << length) - 1) << start
    return (target & ~mask) | ((source << start) & mask)


def parity(value: int) -> int:
    """
    计算奇偶校验位
    
    Args:
        value: 整数值
        
    Returns:
        奇偶校验位（0或1）
    """
    return count_set_bits(value) % 2


def gray_encode(value: int) -> int:
    """
    将二进制转换为格雷码
    
    Args:
        value: 二进制值
        
    Returns:
        格雷码值
    """
    return value ^ (value >> 1)


def gray_decode(value: int) -> int:
    """
    将格雷码转换为二进制
    
    Args:
        value: 格雷码值
        
    Returns:
        二进制值
    """
    result = 0
    while value:
        result ^= value
        value >>= 1
    return result


# ============ 位图操作 ============

class BitArray:
    """
    位数组 - 高效的位集合操作
    """
    
    def __init__(self, size: int, initial: int = 0):
        """
        初始化位数组
        
        Args:
            size: 位数组大小（位数）
            initial: 初始值（0或1）
        """
        self._size = size
        self._data = bytearray((size + 7) // 8)
        if initial:
            for i in range(len(self._data)):
                self._data[i] = 0xFF
    
    def __len__(self) -> int:
        return self._size
    
    def __getitem__(self, index: int) -> int:
        if index < 0 or index >= self._size:
            raise IndexError(f"Index {index} out of range")
        return (self._data[index // 8] >> (7 - index % 8)) & 1
    
    def __setitem__(self, index: int, value: int) -> None:
        if index < 0 or index >= self._size:
            raise IndexError(f"Index {index} out of range")
        if value:
            self._data[index // 8] |= (1 << (7 - index % 8))
        else:
            self._data[index // 8] &= ~(1 << (7 - index % 8))
    
    def set(self, index: int) -> None:
        """设置位为1"""
        self[index] = 1
    
    def clear(self, index: int) -> None:
        """清除位（设为0）"""
        self[index] = 0
    
    def toggle(self, index: int) -> None:
        """翻转位"""
        self._data[index // 8] ^= (1 << (7 - index % 8))
    
    def count_set(self) -> int:
        """统计1的个数"""
        return sum(bin(byte).count('1') for byte in self._data)
    
    def find_first_set(self) -> int:
        """找到第一个设置为1的位"""
        for i in range(self._size):
            if self[i]:
                return i
        return -1
    
    def find_first_clear(self) -> int:
        """找到第一个清除的位"""
        for i in range(self._size):
            if not self[i]:
                return i
        return -1
    
    def to_bytes(self) -> bytes:
        """转换为字节"""
        return bytes(self._data)
    
    @classmethod
    def from_bytes(cls, data: bytes, size: int) -> 'BitArray':
        """从字节创建位数组"""
        arr = cls(size)
        arr._data = bytearray(data[: (size + 7) // 8])
        return arr
    
    def __repr__(self) -> str:
        return f"BitArray(size={self._size}, set_bits={self.count_set()})"


# ============ 便捷函数 ============

def encode_varint(value: int) -> bytes:
    """编码变长整数为字节"""
    writer = BitWriter()
    writer.write_varint(value)
    return writer.get_bytes()


def decode_varint(data: bytes) -> tuple:
    """
    解码变长整数
    
    Args:
        data: 字节数据
        
    Returns:
        (value, bytes_consumed) 元组
    """
    reader = BitReader(data)
    value = reader.read_varint()
    return value, reader.byte_position


def encode_leb128_signed(value: int) -> bytes:
    """编码有符号LEB128"""
    writer = BitWriter()
    writer.write_leb128_signed(value)
    return writer.get_bytes()


def decode_leb128_signed(data: bytes) -> tuple:
    """解码有符号LEB128"""
    reader = BitReader(data)
    value = reader.read_leb128_signed()
    return value, reader.byte_position