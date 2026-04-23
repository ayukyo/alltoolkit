"""
Base58 编码/解码工具

Base58 是一种二进制到文本的编码方式，移除了容易混淆的字符：
- 数字 0 (零)
- 大写字母 O (哦)
- 大写字母 I (艾)
- 小写字母 l (艾欧)
- 符号 + 和 /

常用于：
- 比特币地址编码
- IPFS 内容标识符
- 短链接服务
- 种子文件 Info Hash

零外部依赖，纯 Python 实现。
"""

from typing import Optional, Tuple, List
import hashlib

# Base58 字符表 (比特币风格)
BASE58_ALPHABET = "123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"
BASE58_ALPHABET_MAP = {char: i for i, char in enumerate(BASE58_ALPHABET)}


class Base58Error(Exception):
    """Base58 编码/解码错误"""
    pass


class Base58Encoder:
    """Base58 编码器"""
    
    def __init__(self, alphabet: str = BASE58_ALPHABET):
        """
        初始化编码器
        
        Args:
            alphabet: 自定义 Base58 字符表
        """
        if len(alphabet) != 58:
            raise ValueError("字符表必须包含 58 个字符")
        self.alphabet = alphabet
        self.alphabet_map = {char: i for i, char in enumerate(alphabet)}
    
    def encode(self, data: bytes) -> str:
        """
        将字节数据编码为 Base58 字符串
        
        Args:
            data: 要编码的字节数据
            
        Returns:
            Base58 编码字符串
        """
        if not data:
            return ""
        
        # 计算前导零的数量
        leading_zeros = 0
        for byte in data:
            if byte == 0:
                leading_zeros += 1
            else:
                break
        
        # 将字节数组转换为大整数
        num = int.from_bytes(data, 'big')
        
        # Base58 编码
        result = []
        while num > 0:
            num, remainder = divmod(num, 58)
            result.append(self.alphabet[remainder])
        
        # 添加前导 '1' (对应前导零)
        result.extend([self.alphabet[0]] * leading_zeros)
        
        return ''.join(reversed(result))
    
    def encode_check(self, data: bytes) -> str:
        """
        编码并添加校验和 (Base58Check)
        
        校验和为前 4 字节的 SHA256(SHA256(data))
        
        Args:
            data: 要编码的字节数据
            
        Returns:
            带校验和的 Base58 编码字符串
        """
        checksum = self._double_sha256(data)[:4]
        return self.encode(data + checksum)
    
    def decode(self, encoded: str) -> bytes:
        """
        将 Base58 字符串解码为字节数据
        
        Args:
            encoded: Base58 编码字符串
            
        Returns:
            解码后的字节数据
            
        Raises:
            Base58Error: 如果包含无效字符
        """
        if not encoded:
            return b""
        
        # 验证字符
        for char in encoded:
            if char not in self.alphabet_map:
                raise Base58Error(f"无效的 Base58 字符: {char}")
        
        # 计算前导 '1' 的数量 (对应前导零)
        leading_ones = 0
        for char in encoded:
            if char == self.alphabet[0]:
                leading_ones += 1
            else:
                break
        
        # 将 Base58 字符串转换为大整数
        num = 0
        for char in encoded:
            num = num * 58 + self.alphabet_map[char]
        
        # 转换为字节数组
        if num == 0:
            result = []
        else:
            result = []
            while num > 0:
                result.append(num & 0xff)
                num >>= 8
        
        # 添加前导零
        result = bytes([0] * leading_ones) + bytes(reversed(result))
        
        return result
    
    def decode_check(self, encoded: str) -> bytes:
        """
        解码带校验和的 Base58 字符串
        
        Args:
            encoded: 带校验和的 Base58 编码字符串
            
        Returns:
            解码后的字节数据 (不含校验和)
            
        Raises:
            Base58Error: 如果校验和不匹配
        """
        data = self.decode(encoded)
        if len(data) < 4:
            raise Base58Error("数据太短，无法包含校验和")
        
        payload = data[:-4]
        checksum = data[-4:]
        
        expected_checksum = self._double_sha256(payload)[:4]
        if checksum != expected_checksum:
            raise Base58Error("校验和不匹配")
        
        return payload
    
    @staticmethod
    def _double_sha256(data: bytes) -> bytes:
        """计算双重 SHA256 哈希"""
        return hashlib.sha256(hashlib.sha256(data).digest()).digest()


class Base58Validator:
    """Base58 验证器"""
    
    def __init__(self, alphabet: str = BASE58_ALPHABET):
        self.alphabet = alphabet
        self.encoder = Base58Encoder(alphabet)
    
    def is_valid(self, encoded: str) -> bool:
        """
        验证字符串是否为有效的 Base58 编码
        
        Args:
            encoded: 待验证的字符串
            
        Returns:
            是否有效
        """
        if not encoded:
            return False
        return all(char in self.alphabet for char in encoded)
    
    def is_valid_check(self, encoded: str) -> bool:
        """
        验证带校验和的 Base58 字符串
        
        Args:
            encoded: 待验证的字符串
            
        Returns:
            校验和是否正确
        """
        try:
            self.encoder.decode_check(encoded)
            return True
        except Base58Error:
            return False


class BitcoinAddress:
    """比特币地址工具"""
    
    # 比特币地址版本前缀
    VERSION_PREFIXES = {
        'p2pkh_mainnet': b'\x00',      # 1 开头
        'p2sh_mainnet': b'\x05',       # 3 开头
        'p2pkh_testnet': b'\x6f',      # m 或 n 开头
        'p2sh_testnet': b'\xc4',       # 2 开头
    }
    
    def __init__(self):
        self.encoder = Base58Encoder()
    
    def encode_address(self, public_key_hash: bytes, version: bytes = b'\x00') -> str:
        """
        生成比特币地址
        
        Args:
            public_key_hash: 公钥哈希 (20 字节)
            version: 版本前缀 (默认主网 P2PKH)
            
        Returns:
            比特币地址
        """
        if len(public_key_hash) != 20:
            raise ValueError("公钥哈希必须为 20 字节")
        
        payload = version + public_key_hash
        return self.encoder.encode_check(payload)
    
    def decode_address(self, address: str) -> Tuple[bytes, bytes]:
        """
        解析比特币地址
        
        Args:
            address: 比特币地址
            
        Returns:
            (版本前缀, 公钥哈希)
            
        Raises:
            Base58Error: 如果地址无效
        """
        payload = self.encoder.decode_check(address)
        
        if len(payload) != 21:
            raise Base58Error(f"无效的比特币地址长度: {len(payload)}")
        
        version = payload[0:1]
        public_key_hash = payload[1:]
        
        return version, public_key_hash
    
    def get_address_type(self, address: str) -> Optional[str]:
        """
        获取比特币地址类型
        
        Args:
            address: 比特币地址
            
        Returns:
            地址类型描述，如果无效则返回 None
        """
        try:
            version, _ = self.decode_address(address)
            
            for name, prefix in self.VERSION_PREFIXES.items():
                if version == prefix:
                    return name
            
            return f"未知版本: {version.hex()}"
        except Base58Error:
            return None
    
    def is_valid_bitcoin_address(self, address: str) -> bool:
        """
        验证比特币地址是否有效
        
        Args:
            address: 比特币地址
            
        Returns:
            是否有效
        """
        try:
            self.decode_address(address)
            return True
        except Base58Error:
            return False


class IPFSHash:
    """IPFS CID 编码工具"""
    
    def __init__(self):
        self.encoder = Base58Encoder()
    
    def encode_cid(self, content_hash: bytes, version: int = 0, codec: int = 0x55) -> str:
        """
        生成 IPFS CID
        
        Args:
            content_hash: 内容哈希 (通常为 SHA256，32 字节)
            version: CID 版本 (0 或 1)
            codec: 内容编解码器 (0x55 = raw, 0x70 = dag-pb)
            
        Returns:
            IPFS CID 字符串
        """
        if version == 0:
            # CIDv0: Base58 编码的 multihash
            multihash = bytes([0x12, 0x20]) + content_hash  # SHA2-256, 32 bytes
            return self.encoder.encode(multihash)
        else:
            # CIDv1: 变长编码的版本+编解码器+multihash
            import struct
            varint_codec = self._encode_varint(codec)
            varint_hash_type = self._encode_varint(0x12)  # SHA2-256
            varint_hash_len = self._encode_varint(len(content_hash))
            
            cid = bytes([version]) + varint_codec + varint_hash_type + varint_hash_len + content_hash
            return 'b' + self.encoder.encode(cid)
    
    def decode_cid(self, cid: str) -> Tuple[int, int, bytes]:
        """
        解析 IPFS CID
        
        Args:
            cid: IPFS CID 字符串
            
        Returns:
            (版本号, 编解码器, 内容哈希)
        """
        if cid.startswith('Qm'):
            # CIDv0
            data = self.encoder.decode(cid)
            if data[0] != 0x12 or data[1] != 0x20:
                raise Base58Error("无效的 CIDv0 multihash")
            return 0, 0x70, data[2:]  # dag-pb codec for v0
        elif cid.startswith('b'):
            # CIDv1
            data = self.encoder.decode(cid[1:])
            version, pos = self._decode_varint(data, 0)
            codec, pos = self._decode_varint(data, pos)
            hash_type, pos = self._decode_varint(data, pos)
            hash_len, pos = self._decode_varint(data, pos)
            content_hash = data[pos:pos + hash_len]
            
            return version, codec, content_hash
        else:
            raise Base58Error("无法识别的 CID 格式")
    
    @staticmethod
    def _encode_varint(value: int) -> bytes:
        """编码变长整数"""
        result = []
        while value >= 0x80:
            result.append((value & 0x7f) | 0x80)
            value >>= 7
        result.append(value)
        return bytes(result)
    
    @staticmethod
    def _decode_varint(data: bytes, offset: int) -> Tuple[int, int]:
        """解码变长整数"""
        value = 0
        shift = 0
        pos = offset
        
        while True:
            if pos >= len(data):
                raise Base58Error("变长整数解码越界")
            byte = data[pos]
            value |= (byte & 0x7f) << shift
            pos += 1
            if not (byte & 0x80):
                break
            shift += 7
        
        return value, pos


class Base58Converter:
    """Base58 进制转换工具"""
    
    def __init__(self, alphabet: str = BASE58_ALPHABET):
        self.alphabet = alphabet
        self.encoder = Base58Encoder(alphabet)
    
    def from_hex(self, hex_string: str) -> str:
        """
        将十六进制字符串转换为 Base58
        
        Args:
            hex_string: 十六进制字符串 (可以有 0x 前缀)
            
        Returns:
            Base58 编码字符串
        """
        if hex_string.startswith('0x') or hex_string.startswith('0X'):
            hex_string = hex_string[2:]
        
        data = bytes.fromhex(hex_string)
        return self.encoder.encode(data)
    
    def to_hex(self, encoded: str, prefix: bool = True) -> str:
        """
        将 Base58 字符串转换为十六进制
        
        Args:
            encoded: Base58 编码字符串
            prefix: 是否添加 0x 前缀
            
        Returns:
            十六进制字符串
        """
        data = self.encoder.decode(encoded)
        hex_string = data.hex()
        return '0x' + hex_string if prefix else hex_string
    
    def from_base64(self, base64_string: str) -> str:
        """
        将 Base64 字符串转换为 Base58
        
        Args:
            base64_string: Base64 编码字符串
            
        Returns:
            Base58 编码字符串
        """
        import base64
        data = base64.b64decode(base64_string)
        return self.encoder.encode(data)
    
    def to_base64(self, encoded: str) -> str:
        """
        将 Base58 字符串转换为 Base64
        
        Args:
            encoded: Base58 编码字符串
            
        Returns:
            Base64 编码字符串
        """
        import base64
        data = self.encoder.decode(encoded)
        return base64.b64encode(data).decode('ascii')
    
    def from_int(self, number: int) -> str:
        """
        将整数转换为 Base58
        
        Args:
            number: 非负整数
            
        Returns:
            Base58 编码字符串
        """
        if number < 0:
            raise ValueError("只支持非负整数")
        
        if number == 0:
            return self.alphabet[0]
        
        result = []
        while number > 0:
            number, remainder = divmod(number, 58)
            result.append(self.alphabet[remainder])
        
        return ''.join(reversed(result))
    
    def to_int(self, encoded: str) -> int:
        """
        将 Base58 字符串转换为整数
        
        Args:
            encoded: Base58 编码字符串
            
        Returns:
            整数值
        """
        alphabet_map = {char: i for i, char in enumerate(self.alphabet)}
        
        result = 0
        for char in encoded:
            if char not in alphabet_map:
                raise Base58Error(f"无效的 Base58 字符: {char}")
            result = result * 58 + alphabet_map[char]
        
        return result


def encode(data: bytes) -> str:
    """
    便捷函数：编码字节为 Base58
    
    Args:
        data: 要编码的字节数据
        
    Returns:
        Base58 编码字符串
    """
    return Base58Encoder().encode(data)


def decode(encoded: str) -> bytes:
    """
    便捷函数：解码 Base58 为字节
    
    Args:
        encoded: Base58 编码字符串
        
    Returns:
        解码后的字节数据
    """
    return Base58Encoder().decode(encoded)


def encode_check(data: bytes) -> str:
    """
    便捷函数：编码字节为 Base58Check
    
    Args:
        data: 要编码的字节数据
        
    Returns:
        带校验和的 Base58 编码字符串
    """
    return Base58Encoder().encode_check(data)


def decode_check(encoded: str) -> bytes:
    """
    便捷函数：解码 Base58Check 为字节
    
    Args:
        encoded: 带校验和的 Base58 编码字符串
        
    Returns:
        解码后的字节数据 (不含校验和)
    """
    return Base58Encoder().decode_check(encoded)


def is_valid(encoded: str) -> bool:
    """
    便捷函数：验证 Base58 字符串
    
    Args:
        encoded: 待验证的字符串
        
    Returns:
        是否有效
    """
    return Base58Validator().is_valid(encoded)


# 预定义的 Base58 字母表变体
FLICKR_ALPHABET = "123456789abcdefghijkmnopqrstuvwxyzABCDEFGHJKLMNPQRSTUVWXYZ"
RIPPLE_ALPHABET = "rpshnaf39wBUDNEGHJKLM4PQRST7VWXYZ2bcdeCg65jkm8oFqi1tuvAxyz"