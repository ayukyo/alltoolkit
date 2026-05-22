"""
Base62 Utilities - Base62 编码工具

提供完整的 Base62 编解码实现，包括：
- 数字 ↔ Base62 字符串转换
- 字节流 ↔ Base62 字符串转换
- UUID/GUID 转 Base62 短字符串
- 雪花 ID 转 Base62
- 自定义字符集支持
- URL 安全的短 ID 生成

Base62 使用字符集: 0-9, A-Z, a-z (共62个字符)
常用于：URL 短链接、唯一 ID 编码、友好的字符串表示

零外部依赖，纯 Python 实现。
"""

from typing import Union, Optional, Tuple
import os
import time


# 默认 Base62 字符集: 0-9, A-Z, a-z
DEFAULT_CHARSET = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"

# URL 友好字符集: 0-9, a-z, A-Z (小写字母在前，更易读)
URL_FRIENDLY_CHARSET = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"

# 反转字符集: a-z, A-Z, 0-9
REVERSED_CHARSET = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"


class Base62Encoder:
    """
    Base62 编码器
    
    支持自定义字符集和编码选项。
    """
    
    def __init__(self, charset: Optional[str] = None):
        """
        初始化编码器
        
        Args:
            charset: 自定义字符集 (长度必须为62)
            
        Raises:
            ValueError: 字符集长度不为62或包含重复字符
        """
        self.charset = charset or DEFAULT_CHARSET
        
        if len(self.charset) != 62:
            raise ValueError(f"字符集长度必须为62，当前为 {len(self.charset)}")
        
        if len(set(self.charset)) != 62:
            raise ValueError("字符集包含重复字符")
        
        # 构建反向查找表
        self._char_map = {c: i for i, c in enumerate(self.charset)}
    
    def encode_int(self, num: int) -> str:
        """
        将整数编码为 Base62 字符串
        
        Args:
            num: 非负整数
            
        Returns:
            Base62 编码字符串
            
        Raises:
            ValueError: 输入为负数
            
        Example:
            >>> encoder = Base62Encoder()
            >>> encoder.encode_int(123456789)
            '8M0kX'
        """
        if num < 0:
            raise ValueError("只能编码非负整数")
        
        if num == 0:
            return self.charset[0]
        
        result = []
        base = 62
        
        while num > 0:
            num, remainder = divmod(num, base)
            result.append(self.charset[remainder])
        
        return ''.join(reversed(result))
    
    def decode_int(self, encoded: str) -> int:
        """
        将 Base62 字符串解码为整数
        
        Args:
            encoded: Base62 编码字符串
            
        Returns:
            解码后的整数
            
        Raises:
            ValueError: 字符串包含非法字符
            
        Example:
            >>> encoder = Base62Encoder()
            >>> encoder.decode_int('8M0kX')
            123456789
        """
        if not encoded:
            return 0
        
        result = 0
        base = 62
        
        for char in encoded:
            if char not in self._char_map:
                raise ValueError(f"非法字符: '{char}'")
            result = result * base + self._char_map[char]
        
        return result
    
    def encode_bytes(self, data: bytes) -> str:
        """
        将字节流编码为 Base62 字符串
        
        Args:
            data: 字节流
            
        Returns:
            Base62 编码字符串
            
        Example:
            >>> encoder = Base62Encoder()
            >>> encoder.encode_bytes(b'hello')
            'D9PnQf'
        """
        if not data:
            return self.charset[0]
        
        # 将字节流转为大整数
        num = int.from_bytes(data, byteorder='big')
        return self.encode_int(num)
    
    def decode_bytes(self, encoded: str, output_length: Optional[int] = None) -> bytes:
        """
        将 Base62 字符串解码为字节流
        
        Args:
            encoded: Base62 编码字符串
            output_length: 期望输出字节长度 (可选)
            
        Returns:
            解码后的字节流
            
        Example:
            >>> encoder = Base62Encoder()
            >>> encoder.decode_bytes('D9PnQf')
            b'hello'
        """
        num = self.decode_int(encoded)
        
        if num == 0:
            return b'\x00' if output_length is None else b'\x00' * output_length
        
        # 计算需要的字节长度
        byte_length = (num.bit_length() + 7) // 8
        
        if output_length is not None:
            byte_length = max(byte_length, output_length)
        
        return num.to_bytes(byte_length, byteorder='big')
    
    def encode_uuid(self, uuid_hex: str) -> str:
        """
        将 UUID 编码为 Base62 短字符串
        
        Args:
            uuid_hex: UUID 十六进制字符串 (带或不带连字符)
            
        Returns:
            22字符的 Base62 编码 (UUID 128位 = 22字符 Base62)
            
        Example:
            >>> encoder = Base62Encoder()
            >>> encoder.encode_uuid('550e8400-e29b-41d4-a716-446655440000')
            '2l7vQmRwMvE1sBqKz3G9Kx'
        """
        # 移除连字符
        clean_hex = uuid_hex.replace('-', '')
        
        if len(clean_hex) != 32:
            raise ValueError(f"UUID 必须是32个十六进制字符，当前为 {len(clean_hex)}")
        
        data = bytes.fromhex(clean_hex)
        return self.encode_bytes(data)
    
    def decode_uuid(self, encoded: str) -> str:
        """
        将 Base62 字符串解码为 UUID 格式
        
        Args:
            encoded: Base62 编码字符串
            
        Returns:
            UUID 字符串 (带连字符)
            
        Example:
            >>> encoder = Base62Encoder()
            >>> encoder.decode_uuid('2l7vQmRwMvE1sBqKz3G9Kx')
            '550e8400-e29b-41d4-a716-446655440000'
        """
        data = self.decode_bytes(encoded, 16)
        hex_str = data.hex()
        
        # 格式化为 UUID
        return f"{hex_str[:8]}-{hex_str[8:12]}-{hex_str[12:16]}-{hex_str[16:20]}-{hex_str[20:]}"
    
    def encode_snowflake(self, snowflake_id: int) -> str:
        """
        将雪花 ID 编码为 Base62 短字符串
        
        Args:
            snowflake_id: 雪花 ID (通常是64位整数)
            
        Returns:
            Base62 编码字符串 (通常最多11字符)
            
        Example:
            >>> encoder = Base62Encoder()
            >>> encoder.encode_snowflake(1234567890123456789)
            '1A2b3C4d5E6f'
        """
        return self.encode_int(snowflake_id)
    
    def decode_snowflake(self, encoded: str) -> int:
        """
        将 Base62 字符串解码为雪花 ID
        
        Args:
            encoded: Base62 编码字符串
            
        Returns:
            雪花 ID
            
        Example:
            >>> encoder = Base62Encoder()
            >>> encoder.decode_snowflake('1A2b3C4d5E6f')
            1234567890123456789
        """
        return self.decode_int(encoded)
    
    def generate_short_id(self, length: int = 8) -> str:
        """
        生成随机的 Base62 短 ID
        
        Args:
            length: ID 长度
            
        Returns:
            随机的 Base62 字符串
            
        Example:
            >>> encoder = Base62Encoder()
            >>> encoder.generate_short_id(8)
            'aB3xY9zQ'
        """
        if length <= 0:
            raise ValueError("长度必须大于0")
        
        return ''.join(
            self.charset[b % 62] 
            for b in os.urandom(length)
        )
    
    def generate_time_based_id(self, length: int = 8) -> str:
        """
        生成基于时间戳的 Base62 ID
        
        时间戳部分在前，随机部分在后，确保 ID 有序且唯一性高。
        
        Args:
            length: ID 总长度 (最小6)
            
        Returns:
            Base62 ID
            
        Example:
            >>> encoder = Base62Encoder()
            >>> encoder.generate_time_based_id(12)
            '1A2b3C4d5E6f'
        """
        if length < 6:
            length = 6
        
        # 当前时间戳 (毫秒)
        timestamp_ms = int(time.time() * 1000)
        
        # 时间戳编码
        time_encoded = self.encode_int(timestamp_ms)
        
        # 如果时间戳部分超过指定长度，截取后面的部分
        if len(time_encoded) >= length:
            return time_encoded[-length:]
        
        # 补充随机字符
        random_length = length - len(time_encoded)
        random_part = self.generate_short_id(random_length)
        
        return time_encoded + random_part
    
    def encode_with_prefix(self, num: int, prefix: str = '') -> str:
        """
        编码整数并添加前缀
        
        适用于生成带类型的 ID，如 'user_xYz123'
        
        Args:
            num: 非负整数
            prefix: 前缀字符串
            
        Returns:
            带前缀的 Base62 编码
            
        Example:
            >>> encoder = Base62Encoder()
            >>> encoder.encode_with_prefix(12345, 'user_')
            'user_4d9'
        """
        encoded = self.encode_int(num)
        return f"{prefix}{encoded}" if prefix else encoded
    
    def decode_with_prefix(self, encoded: str, prefix: Optional[str] = None) -> Tuple[Optional[str], int]:
        """
        解码带前缀的 Base62 字符串
        
        Args:
            encoded: 带前缀的字符串
            prefix: 期望的前缀 (None 表示自动提取)
            
        Returns:
            (前缀, 解码整数) 元组
            
        Raises:
            ValueError: 前缀不匹配
            
        Example:
            >>> encoder = Base62Encoder()
            >>> encoder.decode_with_prefix('user_3D7', 'user_')
            ('user_', 12345)
        """
        if prefix is not None:
            if prefix:
                if not encoded.startswith(prefix):
                    raise ValueError(f"期望前缀 '{prefix}'，但字符串以 '{encoded[:len(prefix)]}' 开头")
                actual_prefix = prefix
                encoded = encoded[len(prefix):]
            else:
                # 用户明确指定无前缀，不尝试自动提取
                actual_prefix = ''
        else:
            # 自动提取前缀：找到第一个连续的纯 Base62 部分
            actual_prefix = ''
            # 找到最长的不含非法字符的尾部部分
            for i in range(len(encoded)):
                candidate = encoded[i:]
                if all(c in self._char_map for c in candidate):
                    actual_prefix = encoded[:i]
                    encoded = candidate
                    break
            
            if not encoded:
                encoded = ''
        
        num = self.decode_int(encoded) if encoded else 0
        return (actual_prefix, num)
    
    def is_valid(self, encoded: str) -> bool:
        """
        检查字符串是否是有效的 Base62 编码
        
        Args:
            encoded: 待检查字符串
            
        Returns:
            是否有效
            
        Example:
            >>> encoder = Base62Encoder()
            >>> encoder.is_valid('aB3xY9zQ')
            True
            >>> encoder.is_valid('hello!')  # 包含非法字符 '!'
            False
        """
        return all(char in self._char_map for char in encoded)


# 默认编码器实例
_default_encoder = Base62Encoder()
_url_friendly_encoder = Base62Encoder(URL_FRIENDLY_CHARSET)


# 便捷函数
def encode(num: int) -> str:
    """将整数编码为 Base62 (默认字符集)"""
    return _default_encoder.encode_int(num)


def decode(encoded: str) -> int:
    """将 Base62 字符串解码为整数 (默认字符集)"""
    return _default_encoder.decode_int(encoded)


def encode_bytes(data: bytes) -> str:
    """将字节流编码为 Base62"""
    return _default_encoder.encode_bytes(data)


def decode_bytes(encoded: str, output_length: Optional[int] = None) -> bytes:
    """将 Base62 字符串解码为字节流"""
    return _default_encoder.decode_bytes(encoded, output_length)


def encode_uuid(uuid_hex: str) -> str:
    """将 UUID 编码为 Base62 短字符串"""
    return _default_encoder.encode_uuid(uuid_hex)


def decode_uuid(encoded: str) -> str:
    """将 Base62 字符串解码为 UUID"""
    return _default_encoder.decode_uuid(encoded)


def encode_snowflake(snowflake_id: int) -> str:
    """将雪花 ID 编码为 Base62"""
    return _default_encoder.encode_snowflake(snowflake_id)


def decode_snowflake(encoded: str) -> int:
    """将 Base62 字符串解码为雪花 ID"""
    return _default_encoder.decode_snowflake(encoded)


def generate_short_id(length: int = 8) -> str:
    """生成随机 Base62 短 ID"""
    return _default_encoder.generate_short_id(length)


def generate_time_based_id(length: int = 8) -> str:
    """生成基于时间戳的 Base62 ID"""
    return _default_encoder.generate_time_based_id(length)


def is_valid(encoded: str) -> bool:
    """检查字符串是否是有效的 Base62 编码"""
    return _default_encoder.is_valid(encoded)


# URL 友好编码函数
def encode_url_friendly(num: int) -> str:
    """使用 URL 友好字符集编码 (小写字母优先)"""
    return _url_friendly_encoder.encode_int(num)


def decode_url_friendly(encoded: str) -> int:
    """解码 URL 友好字符集编码的字符串"""
    return _url_friendly_encoder.decode_int(encoded)


def generate_url_friendly_id(length: int = 8) -> str:
    """生成 URL 友好的随机 ID"""
    return _url_friendly_encoder.generate_short_id(length)


if __name__ == "__main__":
    print("=== Base62 编码工具演示 ===")
    
    encoder = Base62Encoder()
    
    # 1. 整数编码
    print("\n--- 整数编码 ---")
    num = 1234567890123456789
    encoded = encoder.encode_int(num)
    decoded = encoder.decode_int(encoded)
    print(f"原数: {num}")
    print(f"编码: {encoded}")
    print(f"解码: {decoded}")
    print(f"验证: {num == decoded}")
    
    # 2. 字节流编码
    print("\n--- 字节流编码 ---")
    data = b'Hello, Base62!'
    encoded = encoder.encode_bytes(data)
    decoded = encoder.decode_bytes(encoded)
    print(f"原文: {data}")
    print(f"编码: {encoded}")
    print(f"解码: {decoded}")
    print(f"验证: {data == decoded}")
    
    # 3. UUID 编码
    print("\n--- UUID 编码 ---")
    uuid_str = "550e8400-e29b-41d4-a716-446655440000"
    encoded = encoder.encode_uuid(uuid_str)
    decoded = encoder.decode_uuid(encoded)
    print(f"原 UUID: {uuid_str}")
    print(f"编码: {encoded} ({len(encoded)} 字符)")
    print(f"解码: {decoded}")
    
    # 4. 雪花 ID 编码
    print("\n--- 雪花 ID 编码 ---")
    snowflake = 1234567890123456789
    encoded = encoder.encode_snowflake(snowflake)
    decoded = encoder.decode_snowflake(encoded)
    print(f"雪花 ID: {snowflake}")
    print(f"编码: {encoded} ({len(encoded)} 字符)")
    print(f"解码: {decoded}")
    
    # 5. 短 ID 生成
    print("\n--- 短 ID 生成 ---")
    for i in range(3):
        print(f"随机 ID: {encoder.generate_short_id(8)}")
    
    for i in range(3):
        print(f"时间 ID: {encoder.generate_time_based_id(12)}")
    
    # 6. 带前缀编码
    print("\n--- 带前缀编码 ---")
    prefixed = encoder.encode_with_prefix(12345, "user_")
    prefix, num = encoder.decode_with_prefix(prefixed)
    print(f"编码: {prefixed}")
    print(f"解码: 前缀={prefix}, 数={num}")
    
    # 7. URL 友好编码
    print("\n--- URL 友好编码 ---")
    url_encoder = Base62Encoder(URL_FRIENDLY_CHARSET)
    encoded = url_encoder.encode_int(123456789)
    print(f"URL 友好编码: {encoded}")
    
    # 8. 验证
    print("\n--- 验证 ---")
    print(f"'aB3xY9zQ' 有效: {encoder.is_valid('aB3xY9zQ')}")
    print(f"'hello!' 有效: {encoder.is_valid('hello!')}")