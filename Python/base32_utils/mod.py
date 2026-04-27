"""
Base32 工具模块

提供多种 Base32 编码方案的实现：
- RFC 4648 标准 Base32 (A-Z, 2-7)
- Base32Hex (0-9, A-V)
- Crockford's Base32 (0-9, A-H, J-K, M-N, P-T, V-Z，排除 I, L, O, U)

零外部依赖，纯 Python 实现。
"""

from typing import Optional, Tuple, List


class Base32Encoder:
    """标准 Base32 编码器 (RFC 4648)"""
    
    # RFC 4648 标准 Base32 字符表
    ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ234567"
    PADDING = "="
    
    def __init__(self):
        self._char_to_index = {c: i for i, c in enumerate(self.ALPHABET)}
    
    def encode(self, data: bytes) -> str:
        """
        将字节数据编码为 Base32 字符串
        
        Args:
            data: 要编码的字节数据
            
        Returns:
            Base32 编码字符串
            
        Example:
            >>> encoder = Base32Encoder()
            >>> encoder.encode(b"hello")
            'NBSWY3DP'
        """
        if not data:
            return ""
        
        result = []
        bits = 0
        bit_buffer = 0
        
        for byte in data:
            bit_buffer = (bit_buffer << 8) | byte
            bits += 8
            
            while bits >= 5:
                bits -= 5
                index = (bit_buffer >> bits) & 0x1F
                result.append(self.ALPHABET[index])
                bit_buffer &= (1 << bits) - 1
        
        # 处理剩余位
        if bits > 0:
            index = (bit_buffer << (5 - bits)) & 0x1F
            result.append(self.ALPHABET[index])
        
        # 添加填充
        padding_needed = (8 - len(result) % 8) % 8
        result.extend(self.PADDING * padding_needed)
        
        return "".join(result)
    
    def decode(self, encoded: str) -> bytes:
        """
        将 Base32 字符串解码为字节数据
        
        Args:
            encoded: Base32 编码字符串
            
        Returns:
            解码后的字节数据
            
        Raises:
            ValueError: 如果输入包含无效字符
            
        Example:
            >>> encoder = Base32Encoder()
            >>> encoder.decode('NBSWY3DP')
            b'hello'
        """
        # 移除填充和空白字符
        encoded = encoded.strip().rstrip(self.PADDING).upper()
        
        if not encoded:
            return b""
        
        # 验证字符
        for char in encoded:
            if char not in self._char_to_index:
                raise ValueError(f"Invalid Base32 character: {char}")
        
        # 计算原始数据长度
        total_bits = len(encoded) * 5
        byte_length = total_bits // 8
        
        result = []
        bits = 0
        bit_buffer = 0
        
        for char in encoded:
            bit_buffer = (bit_buffer << 5) | self._char_to_index[char]
            bits += 5
            
            while bits >= 8:
                bits -= 8
                byte = (bit_buffer >> bits) & 0xFF
                result.append(byte)
                bit_buffer &= (1 << bits) - 1
        
        return bytes(result)


class Base32HexEncoder:
    """Base32Hex 编码器 (RFC 4648)"""
    
    # Base32Hex 字符表 (0-9, A-V)
    ALPHABET = "0123456789ABCDEFGHIJKLMNOPQRSTUV"
    PADDING = "="
    
    def __init__(self):
        self._char_to_index = {c: i for i, c in enumerate(self.ALPHABET)}
        self._lower_char_to_index = {c.lower(): i for i, c in enumerate(self.ALPHABET)}
    
    def encode(self, data: bytes) -> str:
        """
        将字节数据编码为 Base32Hex 字符串
        
        Args:
            data: 要编码的字节数据
            
        Returns:
            Base32Hex 编码字符串
            
        Example:
            >>> encoder = Base32HexEncoder()
            >>> encoder.encode(b"hello")
            'D1IMM7D5'
        """
        if not data:
            return ""
        
        result = []
        bits = 0
        bit_buffer = 0
        
        for byte in data:
            bit_buffer = (bit_buffer << 8) | byte
            bits += 8
            
            while bits >= 5:
                bits -= 5
                index = (bit_buffer >> bits) & 0x1F
                result.append(self.ALPHABET[index])
                bit_buffer &= (1 << bits) - 1
        
        if bits > 0:
            index = (bit_buffer << (5 - bits)) & 0x1F
            result.append(self.ALPHABET[index])
        
        padding_needed = (8 - len(result) % 8) % 8
        result.extend(self.PADDING * padding_needed)
        
        return "".join(result)
    
    def decode(self, encoded: str) -> bytes:
        """
        将 Base32Hex 字符串解码为字节数据
        
        Args:
            encoded: Base32Hex 编码字符串
            
        Returns:
            解码后的字节数据
            
        Raises:
            ValueError: 如果输入包含无效字符
        """
        encoded = encoded.strip().rstrip(self.PADDING)
        
        if not encoded:
            return b""
        
        for char in encoded:
            if char not in self._char_to_index and char not in self._lower_char_to_index:
                raise ValueError(f"Invalid Base32Hex character: {char}")
        
        total_bits = len(encoded) * 5
        byte_length = total_bits // 8
        
        result = []
        bits = 0
        bit_buffer = 0
        
        for char in encoded:
            index = self._char_to_index.get(char) or self._lower_char_to_index.get(char.lower())
            bit_buffer = (bit_buffer << 5) | index
            bits += 5
            
            while bits >= 8:
                bits -= 8
                byte = (bit_buffer >> bits) & 0xFF
                result.append(byte)
                bit_buffer &= (1 << bits) - 1
        
        return bytes(result)


class CrockfordBase32Encoder:
    """
    Crockford's Base32 编码器
    
    特点：
    - 排除易混淆字符 (I, L, O, U)
    - 可选校验位
    - 大小写不敏感
    - 允许可选连字符用于分隔
    
    常用于：URL 友好的 ID、产品序列号等
    """
    
    # Crockford's Base32 字符表
    ALPHABET = "0123456789ABCDEFGHJKMNPQRSTVWXYZ"
    # 完整的校验字符表（37个字符：0-9, A-Z excluding I/L/O/U, *~$=U）
    CHECK_CHARS = "0123456789ABCDEFGHJKMNPQRSTVWXYZ*~$=U"
    
    def __init__(self):
        self._char_to_index = {c: i for i, c in enumerate(self.ALPHABET)}
        # 添加常见混淆字符的映射
        self._char_to_index['O'] = 0  # O -> 0
        self._char_to_index['o'] = 0
        self._char_to_index['I'] = 1  # I -> 1
        self._char_to_index['i'] = 1
        self._char_to_index['L'] = 1  # L -> 1
        self._char_to_index['l'] = 1
        # U 在字母表中存在，索引为 28
    
    def encode(self, data: bytes, checksum: bool = False) -> str:
        """
        将字节数据编码为 Crockford's Base32 字符串
        
        Args:
            data: 要编码的字节数据
            checksum: 是否添加校验位
            
        Returns:
            Crockford's Base32 编码字符串
            
        Example:
            >>> encoder = CrockfordBase32Encoder()
            >>> encoder.encode(b"hello")
            'D1IMM7D5'
            >>> encoder.encode(b"hello", checksum=True)
            'D1IMM7D5A'
        """
        if not data:
            return ""
        
        # 使用位操作方式编码，保留前导零
        result = []
        bits = 0
        bit_buffer = 0
        
        for byte in data:
            bit_buffer = (bit_buffer << 8) | byte
            bits += 8
            
            while bits >= 5:
                bits -= 5
                index = (bit_buffer >> bits) & 0x1F
                result.append(self.ALPHABET[index])
                bit_buffer &= (1 << bits) - 1
        
        # 处理剩余位
        if bits > 0:
            index = (bit_buffer << (5 - bits)) & 0x1F
            result.append(self.ALPHABET[index])
        
        # 添加校验位
        if checksum:
            check_value = self._calculate_checksum(data)
            result.append(self.CHECK_CHARS[check_value])
        
        return "".join(result)
    
    def decode(self, encoded: str, verify_checksum: bool = False) -> bytes:
        """
        将 Crockford's Base32 字符串解码为字节数据
        
        Args:
            encoded: Crockford's Base32 编码字符串
            verify_checksum: 是否验证校验位
            
        Returns:
            解码后的字节数据
            
        Raises:
            ValueError: 如果输入无效或校验失败
        """
        # 移除连字符和空白
        encoded = encoded.strip().replace("-", "").upper()
        
        if not encoded:
            return b""
        
        # 检查校验位
        checksum_char = None
        if len(encoded) > 0 and encoded[-1] in "*~$=":
            # 这些是校验字符（U 可能是数据字符也可能是校验字符）
            # 只有在验证校验时才将其视为校验位
            if verify_checksum:
                checksum_char = encoded[-1]
                encoded = encoded[:-1]
            # 如果不验证校验，我们尝试判断
            elif encoded[-1] in "*~$=":
                # 这些一定是校验字符
                checksum_char = encoded[-1]
                encoded = encoded[:-1]
        
        # 验证并解码
        bits = 0
        bit_buffer = 0
        result = []
        
        for char in encoded:
            if char not in self._char_to_index:
                raise ValueError(f"Invalid Crockford Base32 character: {char}")
            bit_buffer = (bit_buffer << 5) | self._char_to_index[char]
            bits += 5
            
            while bits >= 8:
                bits -= 8
                byte = (bit_buffer >> bits) & 0xFF
                result.append(byte)
                bit_buffer &= (1 << bits) - 1
        
        # 验证校验位
        if verify_checksum and checksum_char:
            data = bytes(result)
            expected_index = self._calculate_checksum(data)
            expected = self.CHECK_CHARS[expected_index]
            if checksum_char != expected:
                raise ValueError(f"Checksum mismatch: expected {expected}, got {checksum_char}")
        
        return bytes(result)
    
    def _calculate_checksum(self, data: bytes) -> int:
        """计算校验值"""
        num = int.from_bytes(data, 'big')
        return num % 37


class Base32Utils:
    """
    Base32 工具集
    
    提供便捷的静态方法访问各种 Base32 编码方案
    """
    
    # 标准 RFC 4648 Base32
    STANDARD = Base32Encoder()
    
    # Base32Hex
    HEX = Base32HexEncoder()
    
    # Crockford's Base32
    CROCKFORD = CrockfordBase32Encoder()
    
    @staticmethod
    def encode(data: bytes, variant: str = "standard") -> str:
        """
        Base32 编码
        
        Args:
            data: 要编码的字节数据
            variant: 编码变体 ("standard", "hex", "crockford")
            
        Returns:
            编码后的字符串
        """
        variant = variant.lower()
        if variant == "standard":
            return Base32Utils.STANDARD.encode(data)
        elif variant == "hex":
            return Base32Utils.HEX.encode(data)
        elif variant == "crockford":
            return Base32Utils.CROCKFORD.encode(data)
        else:
            raise ValueError(f"Unknown variant: {variant}")
    
    @staticmethod
    def decode(encoded: str, variant: str = "standard") -> bytes:
        """
        Base32 解码
        
        Args:
            encoded: 编码字符串
            variant: 编码变体 ("standard", "hex", "crockford")
            
        Returns:
            解码后的字节数据
        """
        variant = variant.lower()
        if variant == "standard":
            return Base32Utils.STANDARD.decode(encoded)
        elif variant == "hex":
            return Base32Utils.HEX.decode(encoded)
        elif variant == "crockford":
            return Base32Utils.CROCKFORD.decode(encoded)
        else:
            raise ValueError(f"Unknown variant: {variant}")
    
    @staticmethod
    def encode_string(text: str, encoding: str = "utf-8", variant: str = "standard") -> str:
        """
        将字符串编码为 Base32
        
        Args:
            text: 要编码的字符串
            encoding: 字符编码
            variant: Base32 变体
            
        Returns:
            Base32 编码字符串
        """
        return Base32Utils.encode(text.encode(encoding), variant)
    
    @staticmethod
    def decode_string(encoded: str, encoding: str = "utf-8", variant: str = "standard") -> str:
        """
        将 Base32 解码为字符串
        
        Args:
            encoded: Base32 编码字符串
            encoding: 字符编码
            variant: Base32 变体
            
        Returns:
            解码后的字符串
        """
        return Base32Utils.decode(encoded, variant).decode(encoding)
    
    @staticmethod
    def is_valid_base32(encoded: str, variant: str = "standard") -> bool:
        """
        检查字符串是否为有效的 Base32 编码
        
        Args:
            encoded: 要检查的字符串
            variant: Base32 变体
            
        Returns:
            是否有效
        """
        try:
            Base32Utils.decode(encoded, variant)
            return True
        except (ValueError, Exception):
            return False
    
    @staticmethod
    def compare(encoded1: str, encoded2: str, variant: str = "standard") -> bool:
        """
        比较两个 Base32 编码字符串（解码后比较）
        
        Args:
            encoded1: 第一个编码字符串
            encoded2: 第二个编码字符串
            variant: Base32 变体
            
        Returns:
            解码后的数据是否相同
        """
        try:
            data1 = Base32Utils.decode(encoded1, variant)
            data2 = Base32Utils.decode(encoded2, variant)
            return data1 == data2
        except Exception:
            return False
    
    @staticmethod
    def crockford_encode_with_checksum(data: bytes) -> str:
        """
        使用 Crockford Base32 编码并添加校验位
        
        Args:
            data: 要编码的数据
            
        Returns:
            带校验位的编码字符串
        """
        return Base32Utils.CROCKFORD.encode(data, checksum=True)
    
    @staticmethod
    def crockford_decode_with_verify(encoded: str) -> bytes:
        """
        解码 Crockford Base32 并验证校验位
        
        Args:
            encoded: 带校验位的编码字符串
            
        Returns:
            解码后的数据
            
        Raises:
            ValueError: 如果校验失败
        """
        return Base32Utils.CROCKFORD.decode(encoded, verify_checksum=True)
    
    @staticmethod
    def generate_id(length: int = 8) -> str:
        """
        生成随机的 Crockford Base32 ID（适合作为 URL 友好的标识符）
        
        Args:
            length: ID 长度（不包括可选校验位）
            
        Returns:
            随机 ID 字符串
        """
        import secrets
        
        # 计算需要的字节数（每5位 = 1字符）
        byte_length = (length * 5 + 7) // 8
        random_bytes = secrets.token_bytes(byte_length)
        
        # 编码并截取到指定长度
        encoded = Base32Utils.CROCKFORD.encode(random_bytes)
        return encoded[:length]
    
    @staticmethod
    def format_with_separator(encoded: str, group_size: int = 4, separator: str = "-") -> str:
        """
        为 Base32 字符串添加分隔符，提高可读性
        
        Args:
            encoded: Base32 编码字符串
            group_size: 每组字符数
            separator: 分隔符
            
        Returns:
            带分隔符的字符串
        """
        # 移除现有分隔符和填充
        encoded = encoded.replace(separator, "").replace("=", "")
        
        # 分组
        groups = [encoded[i:i+group_size] for i in range(0, len(encoded), group_size)]
        return separator.join(groups)
    
    @staticmethod
    def strip_separator(encoded: str, separator: str = "-") -> str:
        """
        移除分隔符
        
        Args:
            encoded: 带分隔符的编码字符串
            separator: 分隔符
            
        Returns:
            不带分隔符的字符串
        """
        return encoded.replace(separator, "")


# 便捷函数
def encode(data: bytes, variant: str = "standard") -> str:
    """Base32 编码便捷函数"""
    return Base32Utils.encode(data, variant)


def decode(encoded: str, variant: str = "standard") -> bytes:
    """Base32 解码便捷函数"""
    return Base32Utils.decode(encoded, variant)


def encode_string(text: str, encoding: str = "utf-8", variant: str = "standard") -> str:
    """字符串编码便捷函数"""
    return Base32Utils.encode_string(text, encoding, variant)


def decode_string(encoded: str, encoding: str = "utf-8", variant: str = "standard") -> str:
    """字符串解码便捷函数"""
    return Base32Utils.decode_string(encoded, encoding, variant)


def generate_id(length: int = 8) -> str:
    """生成随机 ID 便捷函数"""
    return Base32Utils.generate_id(length)


if __name__ == "__main__":
    # 快速演示
    print("=== Base32 工具模块演示 ===")
    print()
    
    # 标准 Base32
    print("标准 Base32:")
    data = b"Hello, World!"
    encoded = Base32Utils.encode(data, "standard")
    decoded = Base32Utils.decode(encoded, "standard")
    print(f"  原始: {data}")
    print(f"  编码: {encoded}")
    print(f"  解码: {decoded}")
    print(f"  验证: {data == decoded}")
    print()
    
    # Base32Hex
    print("Base32Hex:")
    encoded_hex = Base32Utils.encode(data, "hex")
    decoded_hex = Base32Utils.decode(encoded_hex, "hex")
    print(f"  编码: {encoded_hex}")
    print(f"  解码: {decoded_hex}")
    print(f"  验证: {data == decoded_hex}")
    print()
    
    # Crockford Base32
    print("Crockford Base32:")
    encoded_crock = Base32Utils.encode(data, "crockford")
    decoded_crock = Base32Utils.decode(encoded_crock, "crockford")
    print(f"  编码: {encoded_crock}")
    print(f"  解码: {decoded_crock}")
    print(f"  验证: {data == decoded_crock}")
    print()
    
    # 带校验位
    print("带校验位的 Crockford:")
    encoded_checksum = Base32Utils.crockford_encode_with_checksum(data)
    print(f"  编码: {encoded_checksum}")
    decoded_checksum = Base32Utils.crockford_decode_with_verify(encoded_checksum)
    print(f"  解码: {decoded_checksum}")
    print()
    
    # 生成随机 ID
    print("随机 ID 生成:")
    for i in range(5):
        random_id = Base32Utils.generate_id(12)
        formatted = Base32Utils.format_with_separator(random_id, 4, "-")
        print(f"  ID {i+1}: {random_id} (格式化: {formatted})")