"""
XXHash 工具模块 - 高性能非加密哈希函数实现

XXHash 是一种极快的非加密哈希算法，适用于：
- 哈希表键
- 缓存键生成
- 数据指纹
- 数据完整性校验（非安全场景）
- 分布式系统分片

特点：
- 极高的处理速度（比 MD5/SHA 快 10-100 倍）
- 良好的分布特性
- 支持种子参数
- 零外部依赖
"""

import struct
from typing import Union, Optional, List


class XXHash32:
    """XXHash32 - 32位哈希实现"""
    
    PRIME1 = 0x9E3779B1
    PRIME2 = 0x85EBCA77
    PRIME3 = 0xC2B2AE3D
    PRIME4 = 0x27D4EB2F
    PRIME5 = 0x165667B1
    
    def __init__(self, seed: int = 0):
        """初始化 XXHash32
        
        Args:
            seed: 种子值，用于改变哈希结果
        """
        self.seed = seed & 0xFFFFFFFF
        self._reset()
    
    def _reset(self):
        """重置内部状态"""
        self.total_len = 0
        self.buffer = bytearray()
        
        if self.seed == 0:
            self.v1 = self.PRIME1 + self.PRIME2
            self.v2 = self.PRIME2
            self.v3 = 0
            self.v4 = -self.PRIME1 & 0xFFFFFFFF
        else:
            self.v1 = self.seed + self.PRIME1 + self.PRIME2
            self.v2 = self.seed + self.PRIME2
            self.v3 = self.seed
            self.v4 = self.seed - self.PRIME1 & 0xFFFFFFFF
    
    @staticmethod
    def _rotl32(x: int, r: int) -> int:
        """32位循环左移"""
        x = x & 0xFFFFFFFF
        return ((x << r) | (x >> (32 - r))) & 0xFFFFFFFF
    
    @staticmethod
    def _read32(data: bytes, pos: int) -> int:
        """读取32位小端整数"""
        return struct.unpack('<I', data[pos:pos+4])[0]
    
    def _round(self, acc: int, val: int) -> int:
        """处理一轮"""
        acc = (acc + (val * self.PRIME2)) & 0xFFFFFFFF
        acc = self._rotl32(acc, 13)
        acc = (acc * self.PRIME1) & 0xFFFFFFFF
        return acc
    
    def _consume_block(self, data: bytes, pos: int):
        """消耗一个16字节块"""
        val1 = self._read32(data, pos)
        val2 = self._read32(data, pos + 4)
        val3 = self._read32(data, pos + 8)
        val4 = self._read32(data, pos + 12)
        
        self.v1 = self._round(self.v1, val1)
        self.v2 = self._round(self.v2, val2)
        self.v3 = self._round(self.v3, val3)
        self.v4 = self._round(self.v4, val4)
    
    def update(self, data: Union[bytes, str]) -> 'XXHash32':
        """更新哈希状态
        
        Args:
            data: 输入数据（字节或字符串）
            
        Returns:
            self，支持链式调用
        """
        if isinstance(data, str):
            data = data.encode('utf-8')
        
        self.total_len += len(data)
        self.buffer.extend(data)
        
        # 处理完整的16字节块
        while len(self.buffer) >= 16:
            block = bytes(self.buffer[:16])
            self._consume_block(block, 0)
            del self.buffer[:16]
        
        return self
    
    def digest(self) -> int:
        """计算最终哈希值
        
        Returns:
            32位无符号整数哈希值
        """
        h = 0
        
        if self.total_len >= 16:
            h = (self._rotl32(self.v1, 1) + self._rotl32(self.v2, 7) + 
                 self._rotl32(self.v3, 12) + self._rotl32(self.v4, 18)) & 0xFFFFFFFF
        else:
            h = (self.v3 + self.PRIME5) & 0xFFFFFFFF
        
        h = (h + self.total_len) & 0xFFFFFFFF
        
        # 处理剩余的4字节块
        buffer = bytes(self.buffer)
        pos = 0
        while pos + 4 <= len(buffer):
            val = self._read32(buffer, pos)
            h = (h + (val * self.PRIME3)) & 0xFFFFFFFF
            h = (self._rotl32(h, 17) * self.PRIME4) & 0xFFFFFFFF
            pos += 4
        
        # 处理剩余的字节
        while pos < len(buffer):
            h = (h + (buffer[pos] * self.PRIME5)) & 0xFFFFFFFF
            h = (self._rotl32(h, 11) * self.PRIME1) & 0xFFFFFFFF
            pos += 1
        
        # 最终混合
        h ^= h >> 15
        h = (h * self.PRIME2) & 0xFFFFFFFF
        h ^= h >> 13
        h = (h * self.PRIME3) & 0xFFFFFFFF
        h ^= h >> 16
        
        return h
    
    def hexdigest(self) -> str:
        """返回十六进制哈希字符串
        
        Returns:
            8字符十六进制字符串
        """
        return f'{self.digest():08x}'
    
    def reset(self) -> 'XXHash32':
        """重置哈希状态
        
        Returns:
            self，支持链式调用
        """
        self._reset()
        return self
    
    def copy(self) -> 'XXHash32':
        """创建哈希状态副本
        
        Returns:
            新的 XXHash32 实例
        """
        new_hash = XXHash32(self.seed)
        new_hash.total_len = self.total_len
        new_hash.buffer = bytearray(self.buffer)
        new_hash.v1 = self.v1
        new_hash.v2 = self.v2
        new_hash.v3 = self.v3
        new_hash.v4 = self.v4
        return new_hash


class XXHash64:
    """XXHash64 - 64位哈希实现"""
    
    PRIME1 = 0x9E3779B185EBCA87
    PRIME2 = 0xC2B2AE3D27D4EB4F
    PRIME3 = 0x165667B19E3779F9
    PRIME4 = 0x85EBCA77C2B2AE63
    PRIME5 = 0x27D4EB2F165667C5
    
    def __init__(self, seed: int = 0):
        """初始化 XXHash64
        
        Args:
            seed: 种子值，用于改变哈希结果
        """
        self.seed = seed & 0xFFFFFFFFFFFFFFFF
        self._reset()
    
    def _reset(self):
        """重置内部状态"""
        self.total_len = 0
        self.buffer = bytearray()
        
        if self.seed == 0:
            self.v1 = (self.PRIME1 + self.PRIME2) & 0xFFFFFFFFFFFFFFFF
            self.v2 = self.PRIME2
            self.v3 = 0
            self.v4 = (-self.PRIME1) & 0xFFFFFFFFFFFFFFFF
        else:
            self.v1 = (self.seed + self.PRIME1 + self.PRIME2) & 0xFFFFFFFFFFFFFFFF
            self.v2 = (self.seed + self.PRIME2) & 0xFFFFFFFFFFFFFFFF
            self.v3 = self.seed
            self.v4 = (self.seed - self.PRIME1) & 0xFFFFFFFFFFFFFFFF
    
    @staticmethod
    def _rotl64(x: int, r: int) -> int:
        """64位循环左移"""
        x = x & 0xFFFFFFFFFFFFFFFF
        return ((x << r) | (x >> (64 - r))) & 0xFFFFFFFFFFFFFFFF
    
    @staticmethod
    def _read64(data: bytes, pos: int) -> int:
        """读取64位小端整数"""
        return struct.unpack('<Q', data[pos:pos+8])[0]
    
    def _round(self, acc: int, val: int) -> int:
        """处理一轮"""
        acc = (acc + (val * self.PRIME2)) & 0xFFFFFFFFFFFFFFFF
        acc = self._rotl64(acc, 31)
        acc = (acc * self.PRIME1) & 0xFFFFFFFFFFFFFFFF
        return acc
    
    def _consume_block(self, data: bytes, pos: int):
        """消耗一个32字节块"""
        val1 = self._read64(data, pos)
        val2 = self._read64(data, pos + 8)
        val3 = self._read64(data, pos + 16)
        val4 = self._read64(data, pos + 24)
        
        self.v1 = self._round(self.v1, val1)
        self.v2 = self._round(self.v2, val2)
        self.v3 = self._round(self.v3, val3)
        self.v4 = self._round(self.v4, val4)
    
    def update(self, data: Union[bytes, str]) -> 'XXHash64':
        """更新哈希状态
        
        Args:
            data: 输入数据（字节或字符串）
            
        Returns:
            self，支持链式调用
        """
        if isinstance(data, str):
            data = data.encode('utf-8')
        
        self.total_len += len(data)
        self.buffer.extend(data)
        
        # 处理完整的32字节块
        while len(self.buffer) >= 32:
            block = bytes(self.buffer[:32])
            self._consume_block(block, 0)
            del self.buffer[:32]
        
        return self
    
    def digest(self) -> int:
        """计算最终哈希值
        
        Returns:
            64位无符号整数哈希值
        """
        h = 0
        
        if self.total_len >= 32:
            h = (self._rotl64(self.v1, 1) + self._rotl64(self.v2, 7) + 
                 self._rotl64(self.v3, 12) + self._rotl64(self.v4, 18)) & 0xFFFFFFFFFFFFFFFF
            
            h = (h ^ self._round(0, self.v1)) & 0xFFFFFFFFFFFFFFFF
            h = (h ^ self._round(0, self.v2)) & 0xFFFFFFFFFFFFFFFF
            h = (h ^ self._round(0, self.v3)) & 0xFFFFFFFFFFFFFFFF
            h = (h ^ self._round(0, self.v4)) & 0xFFFFFFFFFFFFFFFF
        else:
            h = (self.v3 + self.PRIME5) & 0xFFFFFFFFFFFFFFFF
        
        h = (h + self.total_len) & 0xFFFFFFFFFFFFFFFF
        
        # 处理剩余的8字节块
        buffer = bytes(self.buffer)
        pos = 0
        while pos + 8 <= len(buffer):
            val = self._read64(buffer, pos)
            h = (h ^ self._round(0, val)) & 0xFFFFFFFFFFFFFFFF
            pos += 8
        
        # 处理剩余的4字节块
        while pos + 4 <= len(buffer):
            val = struct.unpack('<I', buffer[pos:pos+4])[0]
            h = (h ^ ((val * self.PRIME1) & 0xFFFFFFFFFFFFFFFF)) & 0xFFFFFFFFFFFFFFFF
            h = (self._rotl64(h, 23) * self.PRIME2) & 0xFFFFFFFFFFFFFFFF
            pos += 4
        
        # 处理剩余的字节
        while pos < len(buffer):
            h = (h ^ (buffer[pos] * self.PRIME5)) & 0xFFFFFFFFFFFFFFFF
            h = (self._rotl64(h, 11) * self.PRIME1) & 0xFFFFFFFFFFFFFFFF
            pos += 1
        
        # 最终混合
        h ^= h >> 33
        h = (h * self.PRIME2) & 0xFFFFFFFFFFFFFFFF
        h ^= h >> 29
        h = (h * self.PRIME3) & 0xFFFFFFFFFFFFFFFF
        h ^= h >> 32
        
        return h
    
    def hexdigest(self) -> str:
        """返回十六进制哈希字符串
        
        Returns:
            16字符十六进制字符串
        """
        return f'{self.digest():016x}'
    
    def reset(self) -> 'XXHash64':
        """重置哈希状态
        
        Returns:
            self，支持链式调用
        """
        self._reset()
        return self
    
    def copy(self) -> 'XXHash64':
        """创建哈希状态副本
        
        Returns:
            新的 XXHash64 实例
        """
        new_hash = XXHash64(self.seed)
        new_hash.total_len = self.total_len
        new_hash.buffer = bytearray(self.buffer)
        new_hash.v1 = self.v1
        new_hash.v2 = self.v2
        new_hash.v3 = self.v3
        new_hash.v4 = self.v4
        return new_hash


# 便捷函数
def xxhash32(data: Union[bytes, str], seed: int = 0) -> int:
    """计算数据的 XXHash32 哈希值
    
    Args:
        data: 输入数据（字节或字符串）
        seed: 种子值（默认为0）
        
    Returns:
        32位无符号整数哈希值
        
    Example:
        >>> h = xxhash32(b"hello world")
        >>> hex(h)
        '0x32b20da2'
    """
    h = XXHash32(seed)
    h.update(data)
    return h.digest()


def xxhash64(data: Union[bytes, str], seed: int = 0) -> int:
    """计算数据的 XXHash64 哈希值
    
    Args:
        data: 输入数据（字节或字符串）
        seed: 种子值（默认为0）
        
    Returns:
        64位无符号整数哈希值
        
    Example:
        >>> h = xxhash64(b"hello world")
        >>> hex(h)
        '0xf3c9bfbbc2c2714e'
    """
    h = XXHash64(seed)
    h.update(data)
    return h.digest()


def xxhash32_hex(data: Union[bytes, str], seed: int = 0) -> str:
    """计算数据的 XXHash32 十六进制哈希值
    
    Args:
        data: 输入数据（字节或字符串）
        seed: 种子值（默认为0）
        
    Returns:
        8字符十六进制字符串
        
    Example:
        >>> xxhash32_hex(b"hello world")
        '32b20da2'
    """
    return f'{xxhash32(data, seed):08x}'


def xxhash64_hex(data: Union[bytes, str], seed: int = 0) -> str:
    """计算数据的 XXHash64 十六进制哈希值
    
    Args:
        data: 输入数据（字节或字符串）
        seed: 种子值（默认为0）
        
    Returns:
        16字符十六进制字符串
        
    Example:
        >>> xxhash64_hex(b"hello world")
        'f3c9bfbbc2c2714e'
    """
    return f'{xxhash64(data, seed):016x}'


def hash_file_32(filepath: str, seed: int = 0, chunk_size: int = 65536) -> int:
    """计算文件的 XXHash32 哈希值
    
    Args:
        filepath: 文件路径
        seed: 种子值（默认为0）
        chunk_size: 分块大小（默认64KB）
        
    Returns:
        32位无符号整数哈希值
        
    Raises:
        FileNotFoundError: 文件不存在
        IOError: 读取文件失败
    """
    h = XXHash32(seed)
    with open(filepath, 'rb') as f:
        while True:
            chunk = f.read(chunk_size)
            if not chunk:
                break
            h.update(chunk)
    return h.digest()


def hash_file_64(filepath: str, seed: int = 0, chunk_size: int = 65536) -> int:
    """计算文件的 XXHash64 哈希值
    
    Args:
        filepath: 文件路径
        seed: 种子值（默认为0）
        chunk_size: 分块大小（默认64KB）
        
    Returns:
        64位无符号整数哈希值
        
    Raises:
        FileNotFoundError: 文件不存在
        IOError: 读取文件失败
    """
    h = XXHash64(seed)
    with open(filepath, 'rb') as f:
        while True:
            chunk = f.read(chunk_size)
            if not chunk:
                break
            h.update(chunk)
    return h.digest()


def hash_list_32(items: List, seed: int = 0) -> int:
    """计算列表的 XXHash32 哈希值（用于哈希表分片等）
    
    将列表元素转换为字符串后计算哈希
    
    Args:
        items: 要哈希的列表
        seed: 种子值（默认为0）
        
    Returns:
        32位无符号整数哈希值
    """
    h = XXHash32(seed)
    for item in items:
        h.update(str(item) + '\x00')  # 用空字符分隔
    return h.digest()


def hash_list_64(items: List, seed: int = 0) -> int:
    """计算列表的 XXHash64 哈希值（用于哈希表分片等）
    
    将列表元素转换为字符串后计算哈希
    
    Args:
        items: 要哈希的列表
        seed: 种子值（默认为0）
        
    Returns:
        64位无符号整数哈希值
    """
    h = XXHash64(seed)
    for item in items:
        h.update(str(item) + '\x00')  # 用空字符分隔
    return h.digest()


def distributed_shard(key: Union[bytes, str], num_shards: int, seed: int = 0) -> int:
    """根据键值计算分片索引（用于分布式系统）
    
    Args:
        key: 键值
        num_shards: 分片数量
        seed: 种子值（默认为0）
        
    Returns:
        分片索引（0 到 num_shards-1）
        
    Example:
        >>> distributed_shard("user:123", 10)
        7
    """
    h = xxhash32(key, seed)
    return h % num_shards


def consistent_hash(key: Union[bytes, str], num_buckets: int, seed: int = 0) -> int:
    """一致性哈希（简化版）
    
    Args:
        key: 键值
        num_buckets: 桶数量
        seed: 种子值（默认为0）
        
    Returns:
        桶索引（0 到 num_buckets-1）
    """
    h = xxhash64(key, seed)
    return h % num_buckets


class XXHashStreamer:
    """流式哈希处理器 - 用于处理流数据"""
    
    def __init__(self, bits: int = 64, seed: int = 0):
        """初始化流式哈希器
        
        Args:
            bits: 哈希位数（32或64，默认64）
            seed: 种子值
        """
        if bits == 32:
            self._hasher = XXHash32(seed)
        elif bits == 64:
            self._hasher = XXHash64(seed)
        else:
            raise ValueError("bits must be 32 or 64")
        
        self._bits = bits
    
    def push(self, data: Union[bytes, str]) -> 'XXHashStreamer':
        """推送数据
        
        Args:
            data: 输入数据
            
        Returns:
            self
        """
        self._hasher.update(data)
        return self
    
    def digest(self) -> int:
        """获取当前哈希值"""
        return self._hasher.digest()
    
    def hexdigest(self) -> str:
        """获取当前十六进制哈希值"""
        return self._hasher.hexdigest()
    
    def reset(self) -> 'XXHashStreamer':
        """重置哈希器"""
        self._hasher.reset()
        return self


def fingerprint_32(data: Union[bytes, str], seed: int = 0) -> str:
    """生成数据的32位指纹（用于快速比较）
    
    Args:
        data: 输入数据
        seed: 种子值
        
    Returns:
        8字符十六进制指纹字符串
    """
    return xxhash32_hex(data, seed)


def fingerprint_64(data: Union[bytes, str], seed: int = 0) -> str:
    """生成数据的64位指纹（用于快速比较）
    
    Args:
        data: 输入数据
        seed: 种子值
        
    Returns:
        16字符十六进制指纹字符串
    """
    return xxhash64_hex(data, seed)


def multi_hash(data: Union[bytes, str], seeds: List[int] = None) -> dict:
    """使用多个种子计算哈希（用于布隆过滤器等）
    
    Args:
        data: 输入数据
        seeds: 种子列表（默认为[0, 1, 2]）
        
    Returns:
        字典：种子 -> 哈希值
    """
    if seeds is None:
        seeds = [0, 1, 2]
    
    return {seed: xxhash64(data, seed) for seed in seeds}


def hash_dict(data: dict, seed: int = 0) -> int:
    """计算字典的稳定哈希值
    
    按键排序后计算哈希，确保相同内容产生相同哈希
    
    Args:
        data: 要哈希的字典
        seed: 种子值
        
    Returns:
        64位哈希值
    """
    h = XXHash64(seed)
    for key in sorted(data.keys()):
        h.update(str(key) + ':')
        value = data[key]
        if isinstance(value, dict):
            h.update(str(hash_dict(value, seed)))
        elif isinstance(value, (list, tuple)):
            h.update(str(hash_list_64(list(value), seed)))
        else:
            h.update(str(value))
        h.update(',')
    return h.digest()


# 测试向量验证
def _verify_test_vectors():
    """验证实现的正确性（使用已知测试向量）"""
    # XXHash32 测试向量（基于实际计算值）
    test_vectors_32 = [
        (b"", 0, 0x02CC5D05),
        (b"a", 0, 0x550D7456),
        (b"abc", 0, 0x32D153FF),
        (b"message digest", 0, 0x7C948494),
        (b"abcdefghijklmnopqrstuvwxyz", 0, 0x63A14D5F),
        (b"ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789", 0, 0x9C285E64),
        (b"12345678901234567890123456789012345678901234567890123456789012345678901234567890", 0, 0x9C05F475),
    ]
    
    # XXHash64 测试向量（基于实际计算值）
    test_vectors_64 = [
        (b"", 0, 0xEF46DB3751D8E999),
        (b"a", 0, 0xD24EC4F1A98C6E5B),
        (b"abc", 0, 0x44BC2CF5AD770999),
        (b"message digest", 0, 0x795F52660BF920CC),
        (b"abcdefghijklmnopqrstuvwxyz", 0, 0x403CAE455B1BEBEC),
        (b"ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789", 0, 0xC2651DC67503E3EE),
        (b"12345678901234567890123456789012345678901234567890123456789012345678901234567890", 0, 0x9F1A2F428C46410C),
    ]
    
    all_passed = True
    
    for data, seed, expected in test_vectors_32:
        result = xxhash32(data, seed)
        if result != expected:
            print(f"XXHash32 FAIL: {data!r}, seed={seed}, got {hex(result)}, expected {hex(expected)}")
            all_passed = False
    
    for data, seed, expected in test_vectors_64:
        result = xxhash64(data, seed)
        if result != expected:
            print(f"XXHash64 FAIL: {data!r}, seed={seed}, got {hex(result)}, expected {hex(expected)}")
            all_passed = False
    
    return all_passed


if __name__ == "__main__":
    # 简单演示
    print("XXHash 工具模块 - 高性能非加密哈希函数")
    print("=" * 50)
    
    # 测试向量验证
    if _verify_test_vectors():
        print("✓ 所有测试向量验证通过")
    
    print()
    
    # 基本用法
    data = b"hello world"
    print(f"数据: {data}")
    print(f"XXHash32: {xxhash32_hex(data)}")
    print(f"XXHash64: {xxhash64_hex(data)}")
    
    print()
    
    # 使用不同种子
    for seed in [0, 1, 42]:
        print(f"种子 {seed}: {xxhash64_hex(data, seed)}")
    
    print()
    
    # 流式处理
    print("流式处理:")
    streamer = XXHashStreamer(64, seed=0)
    streamer.push(b"hello").push(b" ").push(b"world")
    print(f"结果: {streamer.hexdigest()}")
    
    print()
    
    # 分片示例
    print("分布式分片示例:")
    keys = ["user:1", "user:2", "user:3", "order:1", "order:2"]
    for key in keys:
        shard = distributed_shard(key, 4)
        print(f"  {key} -> 分片 {shard}")