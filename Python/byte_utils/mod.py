"""
字节操作工具模块 (Byte Utilities)

提供零外部依赖的字节操作功能，包括：
- 字节序转换（大端/小端）
- 字节数组操作（拼接、切片、填充）
- 位操作（设置、清除、翻转、测试）
- 十六进制转换
- 字节模式匹配
- 字节对齐

适用于底层编程、协议实现、数据处理等场景。
"""

from typing import List, Optional, Tuple, Union


class ByteUtils:
    """字节操作工具类"""
    
    # ==================== 字节序转换 ====================
    
    @staticmethod
    def to_little_endian(value: int, size: int = 4) -> bytes:
        """
        将整数转换为小端字节序
        
        Args:
            value: 要转换的整数值
            size: 字节数（1, 2, 4, 8）
        
        Returns:
            小端字节序的字节串
        
        Example:
            >>> ByteUtils.to_little_endian(0x12345678, 4)
            b'xV4\\x12'
        """
        if size not in (1, 2, 4, 8):
            raise ValueError(f"Size must be 1, 2, 4, or 8, got {size}")
        max_val = (1 << (size * 8)) - 1
        if not (0 <= value <= max_val):
            raise ValueError(f"Value {value} out of range for {size} bytes")
        return value.to_bytes(size, byteorder='little')
    
    @staticmethod
    def to_big_endian(value: int, size: int = 4) -> bytes:
        """
        将整数转换为大端字节序
        
        Args:
            value: 要转换的整数值
            size: 字节数（1, 2, 4, 8）
        
        Returns:
            大端字节序的字节串
        
        Example:
            >>> ByteUtils.to_big_endian(0x12345678, 4)
            b'\\x124Vx'
        """
        if size not in (1, 2, 4, 8):
            raise ValueError(f"Size must be 1, 2, 4, or 8, got {size}")
        max_val = (1 << (size * 8)) - 1
        if not (0 <= value <= max_val):
            raise ValueError(f"Value {value} out of range for {size} bytes")
        return value.to_bytes(size, byteorder='big')
    
    @staticmethod
    def from_little_endian(data: bytes) -> int:
        """
        从小端字节序解析整数
        
        Args:
            data: 小端字节序的字节串
        
        Returns:
            解析后的整数值
        
        Example:
            >>> ByteUtils.from_little_endian(b'\\x78\\x56\\x34\\x12')
            305419896
        """
        return int.from_bytes(data, byteorder='little')
    
    @staticmethod
    def from_big_endian(data: bytes) -> int:
        """
        从大端字节序解析整数
        
        Args:
            data: 大端字节序的字节串
        
        Returns:
            解析后的整数值
        
        Example:
            >>> ByteUtils.from_big_endian(b'\\x12\\x34\\x56\\x78')
            305419896
        """
        return int.from_bytes(data, byteorder='big')
    
    @staticmethod
    def swap_endian(data: bytes) -> bytes:
        """
        交换字节序（大端转小端或反之）
        
        Args:
            data: 原始字节串
        
        Returns:
            字节序交换后的字节串
        
        Example:
            >>> ByteUtils.swap_endian(b'\\x12\\x34\\x56\\x78')
            b'xV4\\x12'
        """
        return data[::-1]
    
    # ==================== 字节数组操作 ====================
    
    @staticmethod
    def concat(*byte_arrays: bytes) -> bytes:
        """
        拼接多个字节数组
        
        Args:
            *byte_arrays: 要拼接的字节数组
        
        Returns:
            拼接后的字节串
        
        Example:
            >>> ByteUtils.concat(b'hello', b' ', b'world')
            b'hello world'
        """
        return b''.join(byte_arrays)
    
    @staticmethod
    def slice_with_padding(data: bytes, start: int, length: int, 
                           pad: bytes = b'\x00') -> bytes:
        """
        切片并自动填充
        
        Args:
            data: 原始字节串
            start: 起始位置
            length: 目标长度
            pad: 填充字节（默认为 \\x00）
        
        Returns:
            切片后的字节串，不足部分用填充字节补齐
        
        Example:
            >>> ByteUtils.slice_with_padding(b'hello', 2, 10)
            b'llo\\x00\\x00\\x00\\x00\\x00\\x00\\x00'
        """
        if len(pad) != 1:
            raise ValueError("Pad must be a single byte")
        
        end = start + length
        result = data[start:end]
        
        if len(result) < length:
            result += pad * (length - len(result))
        
        return result
    
    @staticmethod
    def align_to_boundary(data: bytes, boundary: int, 
                          pad: bytes = b'\x00') -> bytes:
        """
        对齐到指定边界
        
        Args:
            data: 原始字节串
            boundary: 边界大小（如 4, 8, 16 等）
            pad: 填充字节
        
        Returns:
            对齐后的字节串
        
        Example:
            >>> ByteUtils.align_to_boundary(b'hello', 4)
            b'hello\\x00\\x00\\x00'
        """
        if boundary <= 0:
            raise ValueError("Boundary must be positive")
        if len(pad) != 1:
            raise ValueError("Pad must be a single byte")
        
        remainder = len(data) % boundary
        if remainder == 0:
            return data
        
        padding_needed = boundary - remainder
        return data + pad * padding_needed
    
    @staticmethod
    def pad_left(data: bytes, length: int, pad: bytes = b'\x00') -> bytes:
        """
        左侧填充
        
        Args:
            data: 原始字节串
            length: 目标长度
            pad: 填充字节
        
        Returns:
            填充后的字节串
        
        Example:
            >>> ByteUtils.pad_left(b'hello', 10, b'\\xff')
            b'\\xff\\xff\\xff\\xff\\xffhello'
        """
        if len(data) >= length:
            return data
        return pad * (length - len(data)) + data
    
    @staticmethod
    def pad_right(data: bytes, length: int, pad: bytes = b'\x00') -> bytes:
        """
        右侧填充
        
        Args:
            data: 原始字节串
            length: 目标长度
            pad: 填充字节
        
        Returns:
            填充后的字节串
        
        Example:
            >>> ByteUtils.pad_right(b'hello', 10, b'\\xff')
            b'hello\\xff\\xff\\xff\\xff\\xff'
        """
        if len(data) >= length:
            return data
        return data + pad * (length - len(data))
    
    @staticmethod
    def trim_left(data: bytes, trim: bytes = b'\x00') -> bytes:
        """
        去除左侧填充字节
        
        Args:
            data: 原始字节串
            trim: 要去除的字节
        
        Returns:
            去除填充后的字节串
        
        Example:
            >>> ByteUtils.trim_left(b'\\x00\\x00hello', b'\\x00')
            b'hello'
        """
        return data.lstrip(trim)
    
    @staticmethod
    def trim_right(data: bytes, trim: bytes = b'\x00') -> bytes:
        """
        去除右侧填充字节
        
        Args:
            data: 原始字节串
            trim: 要去除的字节
        
        Returns:
            去除填充后的字节串
        
        Example:
            >>> ByteUtils.trim_right(b'hello\\x00\\x00', b'\\x00')
            b'hello'
        """
        return data.rstrip(trim)
    
    # ==================== 位操作 ====================
    
    @staticmethod
    def set_bit(value: int, bit_position: int) -> int:
        """
        设置指定位为 1
        
        Args:
            value: 原始值
            bit_position: 位位置（从右往左，0 开始）
        
        Returns:
            设置后的值
        
        Example:
            >>> ByteUtils.set_bit(0b00001010, 0)
            11
        """
        return value | (1 << bit_position)
    
    @staticmethod
    def clear_bit(value: int, bit_position: int) -> int:
        """
        清除指定位（设为 0）
        
        Args:
            value: 原始值
            bit_position: 位位置（从右往左，0 开始）
        
        Returns:
            清除后的值
        
        Example:
            >>> ByteUtils.clear_bit(0b00001011, 0)
            10
        """
        return value & ~(1 << bit_position)
    
    @staticmethod
    def toggle_bit(value: int, bit_position: int) -> int:
        """
        翻转指定位
        
        Args:
            value: 原始值
            bit_position: 位位置（从右往左，0 开始）
        
        Returns:
            翻转后的值
        
        Example:
            >>> ByteUtils.toggle_bit(0b00001010, 0)
            11
        """
        return value ^ (1 << bit_position)
    
    @staticmethod
    def test_bit(value: int, bit_position: int) -> bool:
        """
        测试指定位是否为 1
        
        Args:
            value: 原始值
            bit_position: 位位置（从右往左，0 开始）
        
        Returns:
            该位是否为 1
        
        Example:
            >>> ByteUtils.test_bit(0b00001010, 1)
            True
        """
        return bool(value & (1 << bit_position))
    
    @staticmethod
    def get_bits(value: int, start: int, count: int) -> int:
        """
        提取连续位
        
        Args:
            value: 原始值
            start: 起始位位置（从右往左，0 开始）
            count: 要提取的位数
        
        Returns:
            提取的值
        
        Example:
            >>> ByteUtils.get_bits(0b11011010, 2, 3)
            6
        """
        mask = (1 << count) - 1
        return (value >> start) & mask
    
    @staticmethod
    def set_bits(value: int, start: int, count: int, new_bits: int) -> int:
        """
        设置连续位
        
        Args:
            value: 原始值
            start: 起始位位置（从右往左，0 开始）
            count: 要设置的位数
            new_bits: 新的位值
        
        Returns:
            设置后的值
        
        Example:
            >>> ByteUtils.set_bits(0b11011010, 2, 3, 0b111)
            222
        """
        mask = (1 << count) - 1
        # 清除原位
        value_cleared = value & ~(mask << start)
        # 设置新位
        return value_cleared | ((new_bits & mask) << start)
    
    @staticmethod
    def reverse_bits(value: int, bit_count: int = 8) -> int:
        """
        反转位顺序
        
        Args:
            value: 原始值
            bit_count: 位数量（默认 8）
        
        Returns:
            位反转后的值
        
        Example:
            >>> ByteUtils.reverse_bits(0b10110001, 8)
            139
        """
        result = 0
        for i in range(bit_count):
            if value & (1 << i):
                result |= 1 << (bit_count - 1 - i)
        return result
    
    @staticmethod
    def count_set_bits(value: int) -> int:
        """
        计算设置为 1 的位数
        
        Args:
            value: 原始值
        
        Returns:
            设置为 1 的位数
        
        Example:
            >>> ByteUtils.count_set_bits(0b10110001)
            4
        """
        count = 0
        while value:
            count += value & 1
            value >>= 1
        return count
    
    @staticmethod
    def count_leading_zeros(value: int, bit_count: int = 8) -> int:
        """
        计算前导零的数量
        
        Args:
            value: 原始值
            bit_count: 总位数（默认 8）
        
        Returns:
            前导零的数量
        
        Example:
            >>> ByteUtils.count_leading_zeros(0b00101000, 8)
            2
        """
        count = 0
        for i in range(bit_count - 1, -1, -1):
            if value & (1 << i):
                break
            count += 1
        return count
    
    @staticmethod
    def count_trailing_zeros(value: int) -> int:
        """
        计算尾随零的数量
        
        Args:
            value: 原始值
        
        Returns:
            尾随零的数量
        
        Example:
            >>> ByteUtils.count_trailing_zeros(0b1011000)
            3
        """
        if value == 0:
            return 0
        count = 0
        while not (value & 1):
            count += 1
            value >>= 1
        return count
    
    # ==================== 十六进制操作 ====================
    
    @staticmethod
    def to_hex(data: bytes, uppercase: bool = False, 
               separator: str = '') -> str:
        """
        字节串转十六进制字符串
        
        Args:
            data: 字节串
            uppercase: 是否使用大写字母
            separator: 字节间的分隔符
        
        Returns:
            十六进制字符串
        
        Example:
            >>> ByteUtils.to_hex(b'\\x12\\x34\\xab', separator=' ')
            '12 34 ab'
        """
        hex_str = data.hex()
        if uppercase:
            hex_str = hex_str.upper()
        
        if separator:
            # 每两个字符插入分隔符
            parts = [hex_str[i:i+2] for i in range(0, len(hex_str), 2)]
            return separator.join(parts)
        
        return hex_str
    
    @staticmethod
    def from_hex(hex_str: str) -> bytes:
        """
        十六进制字符串转字节串
        
        Args:
            hex_str: 十六进制字符串（可包含空格、连字符等）
        
        Returns:
            字节串
        
        Example:
            >>> ByteUtils.from_hex('12 34 ab')
            b'\\x124\\xab'
        """
        # 移除常见分隔符
        clean_hex = hex_str.replace(' ', '').replace('-', '').replace(':', '')
        return bytes.fromhex(clean_hex)
    
    @staticmethod
    def is_hex(s: str) -> bool:
        """
        检查字符串是否为有效的十六进制
        
        Args:
            s: 要检查的字符串
        
        Returns:
            是否为有效十六进制
        
        Example:
            >>> ByteUtils.is_hex('deadbeef')
            True
        """
        try:
            # 移除可能的前缀和分隔符
            clean = s.replace('0x', '').replace('0X', '').replace(' ', '').replace('-', '').replace(':', '')
            int(clean, 16)
            return len(clean) > 0
        except ValueError:
            return False
    
    # ==================== 字节模式操作 ====================
    
    @staticmethod
    def find_pattern(data: bytes, pattern: bytes, 
                     start: int = 0) -> int:
        """
        查找字节模式
        
        Args:
            data: 要搜索的字节串
            pattern: 要查找的模式
            start: 起始位置
        
        Returns:
            模式的起始位置，未找到返回 -1
        
        Example:
            >>> ByteUtils.find_pattern(b'hello world', b'wor')
            6
        """
        return data.find(pattern, start)
    
    @staticmethod
    def find_all_patterns(data: bytes, pattern: bytes) -> List[int]:
        """
        查找所有匹配位置
        
        Args:
            data: 要搜索的字节串
            pattern: 要查找的模式
        
        Returns:
            所有匹配位置的列表
        
        Example:
            >>> ByteUtils.find_all_patterns(b'ababab', b'ab')
            [0, 2, 4]
        """
        positions = []
        start = 0
        while True:
            pos = data.find(pattern, start)
            if pos == -1:
                break
            positions.append(pos)
            start = pos + 1
        return positions
    
    @staticmethod
    def replace_pattern(data: bytes, old_pattern: bytes, 
                        new_pattern: bytes, count: int = -1) -> bytes:
        """
        替换字节模式
        
        Args:
            data: 原始字节串
            old_pattern: 要替换的模式
            new_pattern: 新模式
            count: 最大替换次数（-1 表示全部）
        
        Returns:
            替换后的字节串
        
        Example:
            >>> ByteUtils.replace_pattern(b'hello world', b'world', b'Python')
            b'hello Python'
        """
        return data.replace(old_pattern, new_pattern, count)
    
    @staticmethod
    def count_pattern(data: bytes, pattern: bytes) -> int:
        """
        计算模式出现次数
        
        Args:
            data: 要搜索的字节串
            pattern: 要计数的模式
        
        Returns:
            出现次数
        
        Example:
            >>> ByteUtils.count_pattern(b'ababab', b'ab')
            3
        """
        count = 0
        start = 0
        while True:
            pos = data.find(pattern, start)
            if pos == -1:
                break
            count += 1
            start = pos + 1
        return count
    
    @staticmethod
    def find_pattern_with_wildcard(data: bytes, pattern: str, 
                                    wildcard: str = '?') -> List[int]:
        """
        使用通配符查找模式
        
        Args:
            data: 要搜索的字节串
            pattern: 模式字符串（十六进制，可使用通配符）
                     例如: "12??ab" 匹配 12xxab
            wildcard: 通配符字符
        
        Returns:
            所有匹配位置的列表
        
        Example:
            >>> ByteUtils.find_pattern_with_wildcard(b'\\x12\\x34\\xab', '12??ab')
            [0]
        """
        # 将模式转换为字节和通配符掩码
        pattern = pattern.replace(' ', '').replace('-', '')
        if len(pattern) % 2 != 0:
            raise ValueError("Pattern length must be even")
        
        # 构建模式字节和掩码
        pattern_bytes = []
        mask = []
        for i in range(0, len(pattern), 2):
            hex_pair = pattern[i:i+2]
            if hex_pair[0] == wildcard:
                # 第一个字符是通配符
                if hex_pair[1] == wildcard:
                    pattern_bytes.append(0)
                    mask.append(0)  # 完全忽略
                else:
                    pattern_bytes.append(int(hex_pair[1], 16))
                    mask.append(0x0F)  # 只匹配低四位
            elif hex_pair[1] == wildcard:
                pattern_bytes.append(int(hex_pair[0], 16) << 4)
                mask.append(0xF0)  # 只匹配高四位
            else:
                pattern_bytes.append(int(hex_pair, 16))
                mask.append(0xFF)  # 完全匹配
        
        # 搜索
        matches = []
        for i in range(len(data) - len(pattern_bytes) + 1):
            match = True
            for j, (pb, m) in enumerate(zip(pattern_bytes, mask)):
                if (data[i + j] & m) != (pb & m):
                    match = False
                    break
            if match:
                matches.append(i)
        
        return matches
    
    # ==================== 字节变换 ====================
    
    @staticmethod
    def xor_bytes(data: bytes, key: bytes) -> bytes:
        """
        字节 XOR 操作
        
        Args:
            data: 原始字节串
            key: XOR 密钥（循环使用）
        
        Returns:
            XOR 后的字节串
        
        Example:
            >>> ByteUtils.xor_bytes(b'hello', b'key')
            b'\\x03\\x00\\x06\\x03\\x00'
        """
        if not key:
            return data
        
        result = bytearray(len(data))
        key_len = len(key)
        for i, byte in enumerate(data):
            result[i] = byte ^ key[i % key_len]
        return bytes(result)
    
    @staticmethod
    def rotate_left(value: int, bits: int, bit_count: int = 8) -> int:
        """
        循环左移
        
        Args:
            value: 原始值
            bits: 移动位数
            bit_count: 总位数
        
        Returns:
            移位后的值
        
        Example:
            >>> ByteUtils.rotate_left(0b10110001, 3, 8)
            139
        """
        bits %= bit_count
        mask = (1 << bit_count) - 1
        return ((value << bits) | (value >> (bit_count - bits))) & mask
    
    @staticmethod
    def rotate_right(value: int, bits: int, bit_count: int = 8) -> int:
        """
        循环右移
        
        Args:
            value: 原始值
            bits: 移动位数
            bit_count: 总位数
        
        Returns:
            移位后的值
        
        Example:
            >>> ByteUtils.rotate_right(0b10110001, 3, 8)
            225
        """
        bits %= bit_count
        mask = (1 << bit_count) - 1
        return ((value >> bits) | (value << (bit_count - bits))) & mask
    
    @staticmethod
    def reverse_byte_order(data: bytes, group_size: int = 1) -> bytes:
        """
        按组反转字节顺序
        
        Args:
            data: 原始字节串
            group_size: 分组大小
        
        Returns:
            反转后的字节串
        
        Example:
            >>> ByteUtils.reverse_byte_order(b'\\x12\\x34\\x56\\x78', 2)
            b'\\x56\\x78\\x12\\x34'
        """
        if group_size <= 0:
            raise ValueError("Group size must be positive")
        
        # 补齐到 group_size 的倍数
        remainder = len(data) % group_size
        if remainder:
            data = data + b'\x00' * (group_size - remainder)
        
        # 按组反转
        groups = [data[i:i+group_size] for i in range(0, len(data), group_size)]
        return b''.join(reversed(groups))
    
    # ==================== 校验和计算 ====================
    
    @staticmethod
    def checksum_8bit(data: bytes) -> int:
        """
        计算 8 位校验和（简单求和取补码）
        
        Args:
            data: 字节串
        
        Returns:
            8 位校验和
        
        Example:
            >>> ByteUtils.checksum_8bit(b'\\x01\\x02\\x03')
            250
        """
        return (~sum(data)) & 0xFF
    
    @staticmethod
    def checksum_xor(data: bytes, initial: int = 0) -> int:
        """
        计算 XOR 校验和
        
        Args:
            data: 字节串
            initial: 初始值
        
        Returns:
            XOR 校验和
        
        Example:
            >>> ByteUtils.checksum_xor(b'\\x01\\x02\\x03')
            0
        """
        result = initial
        for byte in data:
            result ^= byte
        return result
    
    @staticmethod
    def checksum_fletcher16(data: bytes) -> int:
        """
        计算 Fletcher-16 校验和
        
        Args:
            data: 字节串
        
        Returns:
            16 位 Fletcher 校验和
        
        Example:
            >>> ByteUtils.checksum_fletcher16(b'hello')
            29216
        """
        sum1 = 0
        sum2 = 0
        for byte in data:
            sum1 = (sum1 + byte) % 255
            sum2 = (sum2 + sum1) % 255
        return (sum2 << 8) | sum1
    
    @staticmethod
    def crc8(data: bytes, polynomial: int = 0x07, 
             initial: int = 0) -> int:
        """
        计算 CRC-8
        
        Args:
            data: 字节串
            polynomial: 多项式（默认 CRC-8）
            initial: 初始值
        
        Returns:
            CRC-8 值
        
        Example:
            >>> ByteUtils.crc8(b'123456789')
            244
        """
        crc = initial
        for byte in data:
            crc ^= byte
            for _ in range(8):
                if crc & 0x80:
                    crc = ((crc << 1) ^ polynomial) & 0xFF
                else:
                    crc = (crc << 1) & 0xFF
        return crc
    
    # ==================== 字节分析 ====================
    
    @staticmethod
    def byte_frequency(data: bytes) -> dict:
        """
        计算字节频率分布
        
        Args:
            data: 字节串
        
        Returns:
            字节值到出现次数的字典
        
        Example:
            >>> ByteUtils.byte_frequency(b'aabbcc')
            {97: 2, 98: 2, 99: 2}
        """
        freq = {}
        for byte in data:
            freq[byte] = freq.get(byte, 0) + 1
        return freq
    
    @staticmethod
    def entropy(data: bytes) -> float:
        """
        计算字节串的熵（信息量）
        
        Args:
            data: 字节串
        
        Returns:
            熵值（0-8）
        
        Example:
            >>> ByteUtils.entropy(b'aaaa')
            0.0
        """
        import math
        
        if not data:
            return 0.0
        
        freq = ByteUtils.byte_frequency(data)
        length = len(data)
        
        entropy_val = 0.0
        for count in freq.values():
            if count > 0:
                p = count / length
                entropy_val -= p * math.log2(p)
        
        return entropy_val
    
    @staticmethod
    def find_repeating_patterns(data: bytes, 
                                 min_length: int = 2,
                                 min_occurrences: int = 2) -> List[Tuple[bytes, List[int]]]:
        """
        查找重复模式
        
        Args:
            data: 字节串
            min_length: 最小模式长度
            min_occurrences: 最小出现次数
        
        Returns:
            (模式, 位置列表) 的列表
        
        Example:
            >>> ByteUtils.find_repeating_patterns(b'ababab', 2)
            [(b'ab', [0, 2, 4])]
        """
        patterns = {}
        
        # 查找所有长度 >= min_length 的模式
        for length in range(min_length, len(data) // 2 + 1):
            for start in range(len(data) - length + 1):
                pattern = data[start:start + length]
                if pattern not in patterns:
                    patterns[pattern] = []
                patterns[pattern].append(start)
        
        # 过滤出现次数足够的模式
        result = []
        for pattern, positions in patterns.items():
            if len(positions) >= min_occurrences:
                # 检查是否有重叠
                unique_positions = [positions[0]]
                for pos in positions[1:]:
                    if pos >= unique_positions[-1] + len(pattern):
                        unique_positions.append(pos)
                
                if len(unique_positions) >= min_occurrences:
                    result.append((pattern, unique_positions))
        
        return sorted(result, key=lambda x: (-len(x[0]), -len(x[1])))


# ==================== 便捷函数 ====================

def to_little_endian(value: int, size: int = 4) -> bytes:
    """便捷函数：转换为小端字节序"""
    return ByteUtils.to_little_endian(value, size)

def to_big_endian(value: int, size: int = 4) -> bytes:
    """便捷函数：转换为大端字节序"""
    return ByteUtils.to_big_endian(value, size)

def from_little_endian(data: bytes) -> int:
    """便捷函数：从小端字节序解析"""
    return ByteUtils.from_little_endian(data)

def from_big_endian(data: bytes) -> int:
    """便捷函数：从大端字节序解析"""
    return ByteUtils.from_big_endian(data)

def to_hex(data: bytes, uppercase: bool = False, separator: str = '') -> str:
    """便捷函数：字节串转十六进制"""
    return ByteUtils.to_hex(data, uppercase, separator)

def from_hex(hex_str: str) -> bytes:
    """便捷函数：十六进制转字节串"""
    return ByteUtils.from_hex(hex_str)

def xor_bytes(data: bytes, key: bytes) -> bytes:
    """便捷函数：字节 XOR"""
    return ByteUtils.xor_bytes(data, key)


if __name__ == '__main__':
    # 简单演示
    print("=== 字节操作工具演示 ===")
    
    # 字节序转换
    value = 0x12345678
    print(f"\n原始值: 0x{value:08X}")
    print(f"小端序: {ByteUtils.to_little_endian(value, 4).hex()}")
    print(f"大端序: {ByteUtils.to_big_endian(value, 4).hex()}")
    
    # 位操作
    print(f"\n设置位 0: {bin(ByteUtils.set_bit(0b1010, 0))}")
    print(f"清除位 1: {bin(ByteUtils.clear_bit(0b1011, 1))}")
    print(f"翻转位 0: {bin(ByteUtils.toggle_bit(0b1010, 0))}")
    print(f"测试位 1: {ByteUtils.test_bit(0b1010, 1)}")
    
    # 十六进制
    data = b'\x12\x34\xab\xcd'
    print(f"\n字节串: {data}")
    print(f"十六进制: {ByteUtils.to_hex(data, uppercase=True, separator=' ')}")
    
    # 校验和
    test_data = b'hello world'
    print(f"\n测试数据: {test_data}")
    print(f"8位校验和: {ByteUtils.checksum_8bit(test_data)}")
    print(f"XOR校验: {ByteUtils.checksum_xor(test_data)}")
    print(f"Fletcher-16: {ByteUtils.checksum_fletcher16(test_data)}")
    print(f"CRC-8: {ByteUtils.crc8(test_data)}")
    
    # 熵计算
    print(f"\n'aaaa' 的熵: {ByteUtils.entropy(b'aaaa'):.2f}")
    print(f"'abcd' 的熵: {ByteUtils.entropy(b'abcd'):.2f}")