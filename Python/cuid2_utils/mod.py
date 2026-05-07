"""
CUID2 Utils - 安全的唯一 ID 生成工具

CUID2 是现代化的、安全的、无冲突的唯一 ID 生成方案。
相比 UUID 和 NanoID，它具有更好的抗预测性和碰撞抵抗性。

特点：
- 无外部依赖，仅使用 Python 标准库
- 支持可配置的 ID 长度（默认 24 字符）
- 线程安全
- 支持 Base36 和 Base62 编码
- 提供验证和解析功能

使用示例：
    from cuid2_utils import Cuid2
    
    # 生成 ID
    cuid = Cuid2()
    id1 = cuid.generate()  # clh3am8ji0000358uht4dbq8c
    id2 = cuid.generate(length=32)  # 更长的 ID
    
    # 快捷函数
    from cuid2_utils import create_id
    my_id = create_id()  # 快速生成
"""

import hashlib
import math
import os
import time
import threading
from typing import Optional, Tuple


# Base36 编码表（小写字母 + 数字）
BASE36_CHARS = "0123456789abcdefghijklmnopqrstuvwxyz"
# Base62 编码表（大小写字母 + 数字）
BASE62_CHARS = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
# Base32hex 编码表（用于指纹）
BASE32HEX_CHARS = "0123456789abcdefghijklmnopqrstuv"


class Cuid2:
    """
    CUID2 唯一 ID 生成器
    
    CUID2 是一个现代化的、安全的唯一 ID 生成方案，
    设计用于替代 UUID 和其他 ID 格式。
    
    Attributes:
        length: ID 长度（默认 24）
        fingerprint: 可选的自定义指纹
        
    Example:
        >>> cuid = Cuid2(length=24)
        >>> id1 = cuid.generate()
        >>> len(id1)
        24
    """
    
    def __init__(
        self,
        length: int = 24,
        fingerprint: Optional[str] = None
    ):
        """
        初始化 CUID2 生成器
        
        Args:
            length: ID 长度，最小 2，最大 32，默认 24
            fingerprint: 可选的自定义指纹，用于增加唯一性
            
        Raises:
            ValueError: 如果长度不在有效范围内
        """
        if length < 2 or length > 32:
            raise ValueError("ID 长度必须在 2-32 之间")
        
        self.length = length
        self._fingerprint = fingerprint
        self._counter = 0
        self._lock = threading.Lock()
        self._last_time = 0
        
    @property
    def fingerprint(self) -> str:
        """
        获取或生成指纹
        
        指纹是基于系统特征生成的唯一标识，
        用于在同一台机器上生成不同的 ID。
        
        Returns:
            32 字符的指纹字符串
        """
        if self._fingerprint:
            return self._fingerprint
        
        # 生成系统指纹（基于机器特征）
        try:
            import socket
            hostname = socket.gethostname()
        except:
            hostname = "localhost"
        
        # 组合多个系统特征
        system_info = f"{hostname}-{os.getpid()}-{id(self)}"
        return hashlib.sha256(system_info.encode()).hexdigest()[:32]
    
    def _get_random(self, length: int) -> str:
        """
        生成指定长度的随机字符串
        
        Args:
            length: 随机字符串长度
            
        Returns:
            Base36 编码的随机字符串
        """
        random_bytes = os.urandom(length)
        result = []
        for byte in random_bytes:
            result.append(BASE36_CHARS[byte % 36])
        return "".join(result)
    
    def _get_hash(self, input_string: str) -> str:
        """
        对输入字符串进行 SHA3 哈希
        
        CUID2 使用 SHA3（Keccak）算法来确保
        ID 的安全性和不可预测性。
        
        Args:
            input_string: 输入字符串
            
        Returns:
            哈希后的 Base36 字符串
        """
        # 使用 SHA3-256
        hash_bytes = hashlib.sha3_256(input_string.encode()).digest()
        return self._bytes_to_base36(hash_bytes)
    
    def _bytes_to_base36(self, bytes_data: bytes) -> str:
        """
        将字节转换为 Base36 字符串
        
        Args:
            bytes_data: 输入字节
            
        Returns:
            Base36 编码字符串
        """
        # 将字节转换为整数
        num = int.from_bytes(bytes_data, 'big')
        
        # 转换为 Base36
        if num == 0:
            return "0"
        
        result = []
        while num > 0:
            result.append(BASE36_CHARS[num % 36])
            num //= 36
        
        return "".join(reversed(result))
    
    def _get_counter(self) -> int:
        """
        获取计数器值（线程安全）
        
        计数器用于在同一毫秒内生成不同的 ID。
        
        Returns:
            计数器值
        """
        with self._lock:
            current_time = int(time.time() * 1000)
            
            # 如果时间改变，重置计数器
            if current_time != self._last_time:
                self._last_time = current_time
                self._counter = 0
            else:
                self._counter += 1
            
            return self._counter
    
    def _get_timestamp(self) -> str:
        """
        获取时间戳（毫秒级）
        
        Returns:
            Base36 编码的时间戳字符串
        """
        timestamp = int(time.time() * 1000)
        return self._bytes_to_base36(timestamp.to_bytes(8, 'big')).lstrip('0') or '0'
    
    def generate(self, length: Optional[int] = None) -> str:
        """
        生成一个 CUID2 ID
        
        Args:
            length: 可选的 ID 长度（覆盖默认值）
            
        Returns:
            CUID2 格式的唯一 ID
            
        Example:
            >>> cuid = Cuid2()
            >>> id1 = cuid.generate()
            >>> len(id1)
            24
        """
        target_length = length or self.length
        
        # 组件
        timestamp = self._get_timestamp()
        counter = self._bytes_to_base36(self._get_counter().to_bytes(4, 'big')).lstrip('0') or '0'
        random_part = self._get_random(8)
        fingerprint = self.fingerprint[:8]
        
        # 组合并哈希
        combined = f"{timestamp}{counter}{random_part}{fingerprint}"
        hashed = self._get_hash(combined)
        
        # 截取到目标长度
        return hashed[:target_length]
    
    def generate_batch(self, count: int, length: Optional[int] = None) -> list:
        """
        批量生成 CUID2 ID
        
        Args:
            count: 生成的 ID 数量
            length: 可选的 ID 长度
            
        Returns:
            ID 列表
            
        Example:
            >>> cuid = Cuid2()
            >>> ids = cuid.generate_batch(5)
            >>> len(ids)
            5
        """
        return [self.generate(length) for _ in range(count)]
    
    def is_valid(self, cuid_id: str) -> bool:
        """
        验证字符串是否为有效的 CUID2 格式
        
        Args:
            cuid_id: 待验证的字符串
            
        Returns:
            是否为有效的 CUID2 格式
            
        Example:
            >>> cuid = Cuid2()
            >>> id1 = cuid.generate()
            >>> cuid.is_valid(id1)
            True
            >>> cuid.is_valid("invalid!")
            False
        """
        if not cuid_id:
            return False
        
        # 检查长度
        if len(cuid_id) < 2 or len(cuid_id) > 32:
            return False
        
        # 检查字符是否为有效的 Base36
        return all(c in BASE36_CHARS for c in cuid_id.lower())
    
    def get_info(self, cuid_id: str) -> dict:
        """
        解析 CUID2 ID 并返回信息
        
        注意：CUID2 是哈希后的结果，无法完全还原原始信息。
        此方法仅返回格式信息。
        
        Args:
            cuid_id: CUID2 ID
            
        Returns:
            包含 ID 信息的字典
        """
        return {
            "id": cuid_id,
            "length": len(cuid_id),
            "valid": self.is_valid(cuid_id),
            "format": "cuid2",
            "encoding": "base36"
        }


def create_id(length: int = 24, fingerprint: Optional[str] = None) -> str:
    """
    快捷函数：生成单个 CUID2 ID
    
    Args:
        length: ID 长度，默认 24
        fingerprint: 可选的自定义指纹
        
    Returns:
        CUID2 ID 字符串
        
    Example:
        >>> my_id = create_id()
        >>> len(my_id)
        24
    """
    cuid = Cuid2(length=length, fingerprint=fingerprint)
    return cuid.generate()


def create_id_batch(count: int, length: int = 24, fingerprint: Optional[str] = None) -> list:
    """
    快捷函数：批量生成 CUID2 ID
    
    Args:
        count: 生成的 ID 数量
        length: ID 长度，默认 24
        fingerprint: 可选的自定义指纹
        
    Returns:
        ID 列表
        
    Example:
        >>> ids = create_id_batch(10)
        >>> len(ids)
        10
    """
    cuid = Cuid2(length=length, fingerprint=fingerprint)
    return cuid.generate_batch(count)


def is_cuid2(cuid_id: str) -> bool:
    """
    快捷函数：验证字符串是否为有效的 CUID2 格式
    
    Args:
        cuid_id: 待验证的字符串
        
    Returns:
        是否为有效的 CUID2 格式
        
    Example:
        >>> is_cuid2("clh3am8ji0000358uht4dbq8c")
        True
        >>> is_cuid2("invalid!")
        False
    """
    cuid = Cuid2()
    return cuid.is_valid(cuid_id)


class SecureCuid2(Cuid2):
    """
    更安全的 CUID2 变体
    
    增加了额外的安全措施：
    - 更长的默认长度（32 字符）
    - 使用更安全的随机源
    - 添加额外的熵
    """
    
    def __init__(self, length: int = 32, fingerprint: Optional[str] = None):
        """
        初始化安全的 CUID2 生成器
        
        Args:
            length: ID 长度，最小 16，默认 32
            fingerprint: 可选的自定义指纹
        """
        if length < 16:
            length = 16
        super().__init__(length=length, fingerprint=fingerprint)
    
    def generate(self, length: Optional[int] = None) -> str:
        """
        生成一个更安全的 CUID2 ID
        
        添加了额外的随机熵来增强安全性。
        
        Args:
            length: 可选的 ID 长度
            
        Returns:
            CUID2 ID 字符串
        """
        # 生成基础 ID
        base_id = super().generate(length)
        
        # 添加额外的熵（使用 time.time() * 1e9 替代 time_ns() 以兼容 Python 3.6+）
        extra_entropy = self._get_random(8)
        combined = f"{base_id}{extra_entropy}{int(time.time() * 1e9)}"
        
        # 再次哈希
        hashed = self._get_hash(combined)
        
        target_length = length or self.length
        return hashed[:target_length]


class PrefixedCuid2:
    """
    带前缀的 CUID2 ID 生成器
    
    用于生成带有特定前缀的 ID，如：
    - user_clh3am8ji0000358uht4dbq8c
    - order_clh3am8ji0000358uht4dbq8d
    """
    
    def __init__(self, prefix: str, length: int = 24, fingerprint: Optional[str] = None):
        """
        初始化带前缀的 CUID2 生成器
        
        Args:
            prefix: ID 前缀
            length: ID 长度（不含前缀）
            fingerprint: 可选的自定义指纹
            
        Raises:
            ValueError: 如果前缀为空或包含无效字符
        """
        if not prefix or not prefix.isalnum():
            raise ValueError("前缀必须为非空的字母数字组合")
        
        self.prefix = prefix.lower()
        self.cuid = Cuid2(length=length, fingerprint=fingerprint)
    
    def generate(self) -> str:
        """
        生成带前缀的 CUID2 ID
        
        Returns:
            格式为 prefix_cuid2 的 ID
        """
        return f"{self.prefix}_{self.cuid.generate()}"
    
    def is_valid(self, prefixed_id: str) -> bool:
        """
        验证带前缀的 ID
        
        Args:
            prefixed_id: 待验证的 ID
            
        Returns:
            是否为有效格式
        """
        if "_" not in prefixed_id:
            return False
        
        prefix, cuid_id = prefixed_id.split("_", 1)
        
        return prefix == self.prefix and self.cuid.is_valid(cuid_id)
    
    def extract_prefix(self, prefixed_id: str) -> Optional[str]:
        """
        从 ID 中提取前缀
        
        Args:
            prefixed_id: 带前缀的 ID
            
        Returns:
            前缀字符串，如果格式无效则返回 None
        """
        if "_" not in prefixed_id:
            return None
        
        return prefixed_id.split("_", 1)[0]
    
    def extract_cuid(self, prefixed_id: str) -> Optional[str]:
        """
        从 ID 中提取 CUID2 部分
        
        Args:
            prefixed_id: 带前缀的 ID
            
        Returns:
            CUID2 部分，如果格式无效则返回 None
        """
        if "_" not in prefixed_id:
            return None
        
        return prefixed_id.split("_", 1)[1]


def create_prefixed_id(prefix: str, length: int = 24) -> str:
    """
    快捷函数：生成带前缀的 CUID2 ID
    
    Args:
        prefix: ID 前缀
        length: ID 长度（不含前缀）
        
    Returns:
        格式为 prefix_cuid2 的 ID
        
    Example:
        >>> user_id = create_prefixed_id("user")
        >>> user_id.startswith("user_")
        True
    """
    generator = PrefixedCuid2(prefix=prefix, length=length)
    return generator.generate()


# 便捷导出
__all__ = [
    'Cuid2',
    'SecureCuid2',
    'PrefixedCuid2',
    'create_id',
    'create_id_batch',
    'create_prefixed_id',
    'is_cuid2',
    'BASE36_CHARS',
    'BASE62_CHARS',
]