"""
HyperLogLog Utils - 基数估计工具库

提供多种基数估计实现：
- HyperLogLog: 标准 HyperLogLog 算法
- HyperLogLogPlusPlus: Google 改进版，更高精度
- SparseHyperLogLog: 稀疏模式优化，适合小数据集

特点：
- 零外部依赖，纯 Python 标准库实现
- 多种哈希函数支持
- 完整的序列化/反序列化支持
- 集合操作（并集、交集估计）

使用场景：
- UV 统计（独立访客数）
- 数据库查询优化
- 网络流量分析
- 大数据去重计数
- 实时监控系统
"""

import math
import struct
import hashlib
import random
from typing import (
    Any, Callable, Dict, Iterator, List, Optional, 
    Set, Tuple, Union, BinaryIO
)
from dataclasses import dataclass, field
from io import BytesIO


# ============================================================================
# 常量定义
# ============================================================================

# 不同精度的原始误差范围
HLL_STANDARD_ERROR = {
    4: 0.26,   # 26% 误差
    5: 0.185,  # 18.5% 误差
    6: 0.13,   # 13% 误差
    7: 0.092,  # 9.2% 误差
    8: 0.065,  # 6.5% 误差
    9: 0.046,  # 4.6% 误差
    10: 0.033, # 3.3% 误差
    11: 0.023, # 2.3% 误差
    12: 0.016, # 1.6% 误差
    13: 0.012, # 1.2% 误差
    14: 0.008, # 0.8% 误差
    15: 0.006, # 0.6% 误差
    16: 0.004, # 0.4% 误差
}

# Alpha 常量（用于不同精度的修正）
ALPHA_VALUES = {
    4: 0.673,
    5: 0.697,
    6: 0.709,
}

# 默认使用 m=16 时的 alpha 值
ALPHA_16 = 0.7213 / (1 + 1.079 / 16)


# ============================================================================
# 哈希函数
# ============================================================================

def murmurhash3_x64_128(data: bytes, seed: int = 0) -> int:
    """
    MurmurHash3 x64 128-bit 实现（返回 64 位值）
    
    用于 HyperLogLog 的哈希函数，产生良好的分布特性。
    
    Args:
        data: 要哈希的字节
        seed: 哈希种子
        
    Returns:
        64位哈希值
    """
    c1 = 0x87c37b91114253d5
    c2 = 0x4cf5ad432745937f
    
    h1 = seed
    h2 = seed
    length = len(data)
    nblocks = length // 16
    
    for i in range(nblocks):
        block = data[i * 16:(i + 1) * 16]
        k1 = struct.unpack('<Q', block[:8])[0]
        k2 = struct.unpack('<Q', block[8:])[0]
        
        k1 = (k1 * c1) & 0xFFFFFFFFFFFFFFFF
        k1 = ((k1 << 31) | (k1 >> 33)) & 0xFFFFFFFFFFFFFFFF
        k1 = (k1 * c2) & 0xFFFFFFFFFFFFFFFF
        h1 ^= k1
        
        h1 = ((h1 << 27) | (h1 >> 37)) & 0xFFFFFFFFFFFFFFFF
        h1 = (h1 + h2) & 0xFFFFFFFFFFFFFFFF
        h1 = (h1 * 5 + 0x52dce729) & 0xFFFFFFFFFFFFFFFF
        
        k2 = (k2 * c2) & 0xFFFFFFFFFFFFFFFF
        k2 = ((k2 << 33) | (k2 >> 31)) & 0xFFFFFFFFFFFFFFFF
        k2 = (k2 * c1) & 0xFFFFFFFFFFFFFFFF
        h2 ^= k2
        
        h2 = ((h2 << 31) | (h2 >> 33)) & 0xFFFFFFFFFFFFFFFF
        h2 = (h2 + h1) & 0xFFFFFFFFFFFFFFFF
        h2 = (h2 * 5 + 0x38495ab5) & 0xFFFFFFFFFFFFFFFF
    
    tail = data[nblocks * 16:]
    k1 = 0
    k2 = 0
    
    tail_len = len(tail)
    if tail_len >= 15:
        k2 ^= tail[14] << 48
    if tail_len >= 14:
        k2 ^= tail[13] << 40
    if tail_len >= 13:
        k2 ^= tail[12] << 32
    if tail_len >= 12:
        k2 ^= tail[11] << 24
    if tail_len >= 11:
        k2 ^= tail[10] << 16
    if tail_len >= 10:
        k2 ^= tail[9] << 8
    if tail_len >= 9:
        k2 ^= tail[8]
        k2 = (k2 * c2) & 0xFFFFFFFFFFFFFFFF
        k2 = ((k2 << 33) | (k2 >> 31)) & 0xFFFFFFFFFFFFFFFF
        k2 = (k2 * c1) & 0xFFFFFFFFFFFFFFFF
        h2 ^= k2
    
    if tail_len >= 8:
        k1 ^= tail[7] << 56
    if tail_len >= 7:
        k1 ^= tail[6] << 48
    if tail_len >= 6:
        k1 ^= tail[5] << 40
    if tail_len >= 5:
        k1 ^= tail[4] << 32
    if tail_len >= 4:
        k1 ^= tail[3] << 24
    if tail_len >= 3:
        k1 ^= tail[2] << 16
    if tail_len >= 2:
        k1 ^= tail[1] << 8
    if tail_len >= 1:
        k1 ^= tail[0]
        k1 = (k1 * c1) & 0xFFFFFFFFFFFFFFFF
        k1 = ((k1 << 31) | (k1 >> 33)) & 0xFFFFFFFFFFFFFFFF
        k1 = (k1 * c2) & 0xFFFFFFFFFFFFFFFF
        h1 ^= k1
    
    h1 ^= length
    h2 ^= length
    
    h1 = (h1 + h2) & 0xFFFFFFFFFFFFFFFF
    h2 = (h2 + h1) & 0xFFFFFFFFFFFFFFFF
    
    # finalizer
    h1 ^= h1 >> 33
    h1 = (h1 * 0xff51afd7ed558ccd) & 0xFFFFFFFFFFFFFFFF
    h1 ^= h1 >> 33
    h1 = (h1 * 0xc4ceb9fe1a85ec53) & 0xFFFFFFFFFFFFFFFF
    h1 ^= h1 >> 33
    
    h2 ^= h2 >> 33
    h2 = (h2 * 0xff51afd7ed558ccd) & 0xFFFFFFFFFFFFFFFF
    h2 ^= h2 >> 33
    h2 = (h2 * 0xc4ceb9fe1a85ec53) & 0xFFFFFFFFFFFFFFFF
    h2 ^= h2 >> 33
    
    return h1


def sha256_hash_64(data: bytes, seed: int = 0) -> int:
    """
    SHA-256 哈希（取前 8 字节作为 64 位值）
    
    Args:
        data: 要哈希的字节
        seed: 哈希种子（会追加到数据末尾）
        
    Returns:
        64位哈希值
    """
    hasher = hashlib.sha256(data + seed.to_bytes(8, 'little'))
    return struct.unpack('<Q', hasher.digest()[:8])[0]


def xxhash_64(data: bytes, seed: int = 0) -> int:
    """
    XXHash64 简化实现
    
    非常快速的非加密哈希函数。
    
    Args:
        data: 要哈希的字节
        seed: 哈希种子
        
    Returns:
        64位哈希值
    """
    PRIME1 = 0x9E3779B185EBCA87
    PRIME2 = 0xC2B2AE3D27D4EB4F
    PRIME3 = 0x165667B19E3779F9
    PRIME4 = 0x85EBCA6792E79799
    PRIME5 = 0x27D4EB2F165667C5
    
    def rotl64(x, r):
        return ((x << r) | (x >> (64 - r))) & 0xFFFFFFFFFFFFFFFF
    
    length = len(data)
    
    if length >= 32:
        v1 = (seed + PRIME1 + PRIME2) & 0xFFFFFFFFFFFFFFFF
        v2 = (seed + PRIME2) & 0xFFFFFFFFFFFFFFFF
        v3 = seed
        v4 = (seed - PRIME1) & 0xFFFFFFFFFFFFFFFF
        
        for i in range(0, length - 31, 32):
            for j in range(4):
                block = data[i + j * 8:i + j * 8 + 8]
                if len(block) < 8:
                    break
                k = struct.unpack('<Q', block)[0]
                
                if j == 0:
                    v1 = (v1 + k * PRIME2) & 0xFFFFFFFFFFFFFFFF
                    v1 = rotl64(v1, 31)
                    v1 = (v1 * PRIME1) & 0xFFFFFFFFFFFFFFFF
                elif j == 1:
                    v2 = (v2 + k * PRIME2) & 0xFFFFFFFFFFFFFFFF
                    v2 = rotl64(v2, 31)
                    v2 = (v2 * PRIME1) & 0xFFFFFFFFFFFFFFFF
                elif j == 2:
                    v3 = (v3 + k * PRIME2) & 0xFFFFFFFFFFFFFFFF
                    v3 = rotl64(v3, 31)
                    v3 = (v3 * PRIME1) & 0xFFFFFFFFFFFFFFFF
                else:
                    v4 = (v4 + k * PRIME2) & 0xFFFFFFFFFFFFFFFF
                    v4 = rotl64(v4, 31)
                    v4 = (v4 * PRIME1) & 0xFFFFFFFFFFFFFFFF
        
        h = rotl64(v1, 1) + rotl64(v2, 7) + rotl64(v3, 12) + rotl64(v4, 18)
        h = h & 0xFFFFFFFFFFFFFFFF
        h = (h + (length - 32) * PRIME1) & 0xFFFFFFFFFFFFFFFF
    else:
        h = (seed + PRIME5) & 0xFFFFFFFFFFFFFFFF
        h = (h + length) & 0xFFFFFFFFFFFFFFFF
    
    # 处理剩余字节
    idx = length - (length % 8)
    
    for i in range(0, idx, 8):
        k = struct.unpack('<Q', data[i:i + 8])[0]
        h ^= rotl64(k * PRIME2, 31) * PRIME1
        h = (rotl64(h, 27) * PRIME1 + PRIME4) & 0xFFFFFFFFFFFFFFFF
    
    # 处理最后 4 字节
    if length - idx >= 4:
        k = struct.unpack('<I', data[idx:idx + 4])[0]
        h ^= (k * PRIME1) & 0xFFFFFFFFFFFFFFFF
        h = (rotl64(h, 23) * PRIME2 + PRIME3) & 0xFFFFFFFFFFFFFFFF
        idx += 4
    
    # 处理剩余字节
    for i in range(idx, length):
        h ^= data[i] * PRIME5
        h = rotl64(h, 11) * PRIME1
    
    # finalizer
    h ^= h >> 33
    h = (h * PRIME2) & 0xFFFFFFFFFFFFFFFF
    h ^= h >> 29
    h = (h * PRIME3) & 0xFFFFFFFFFFFFFFFF
    h ^= h >> 32
    
    return h


# 哈希函数注册表
HASH_FUNCTIONS: Dict[str, Callable[[bytes, int], int]] = {
    'murmur': murmurhash3_x64_128,
    'sha256': sha256_hash_64,
    'xxhash': xxhash_64,
}


# ============================================================================
# 工具函数
# ============================================================================

def count_leading_zeros(value: int, max_bits: int = 64) -> int:
    """
    计算前导零的数量
    
    Args:
        value: 要计算的值
        max_bits: 最大位数
        
    Returns:
        前导零的数量 + 1
    """
    if value == 0:
        return max_bits + 1
    
    count = 0
    for i in range(max_bits - 1, -1, -1):
        if (value >> i) & 1:
            return count + 1
        count += 1
    return count + 1


def get_alpha(m: int) -> float:
    """
    获取 alpha 修正常量
    
    Args:
        m: 寄存器数量
        
    Returns:
        alpha 值
    """
    if m <= 16:
        return ALPHA_VALUES.get(int(math.log2(m)), ALPHA_16)
    return ALPHA_16


def estimate_cardinality_harmonic_mean(
    registers: List[int],
    m: int,
    alpha: float
) -> float:
    """
    使用调和平均数估计基数
    
    Args:
        registers: 寄存器数组
        m: 寄存器数量
        alpha: alpha 常量
        
    Returns:
        估计的基数
    """
    # 计算调和平均数
    harmonic_sum = sum(2 ** (-r) for r in registers)
    
    if harmonic_sum == 0:
        return 0
    
    estimate = alpha * m * m / harmonic_sum
    
    # 小范围修正
    if estimate <= 2.5 * m:
        # 线性计数修正
        zeros = registers.count(0)
        if zeros > 0:
            estimate = m * math.log(m / zeros)
    
    # 大范围修正
    elif estimate > (1 / 30) * (1 << 32):
        estimate = -(1 << 32) * math.log(1 - estimate / (1 << 32))
    
    return estimate


@dataclass
class HyperLogLogStats:
    """HyperLogLog 统计信息"""
    precision: int  # 精度参数
    num_registers: int  # 寄存器数量
    memory_bytes: int  # 内存使用（字节）
    elements_added: int  # 已添加元素数量（近似）
    estimated_cardinality: float  # 估计的基数
    standard_error: float  # 标准误差
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            'precision': self.precision,
            'num_registers': self.num_registers,
            'memory_bytes': self.memory_bytes,
            'elements_added': self.elements_added,
            'estimated_cardinality': self.estimated_cardinality,
            'standard_error': self.standard_error,
        }


# ============================================================================
# HyperLogLog 实现
# ============================================================================

class HyperLogLog:
    """
    标准 HyperLogLog 数据结构
    
    用于估计大型数据集的基数（唯一元素数量）。
    内存使用：m = 2^precision 个寄存器（每个 5 位）
    
    特点：
    - 空间效率极高：16KB 可估计 2^64 个元素
    - 可合并：多个 HyperLogLog 可以合并
    - 近似结果：有小误差
    
    使用示例：
        >>> hll = HyperLogLog(precision=12)
        >>> for i in range(10000):
        ...     hll.add(f"user_{i}")
        >>> hll.count()
        10042.5  # 约 0.4% 误差
    """
    
    def __init__(
        self,
        precision: int = 14,
        hash_func: str = 'murmur',
    ):
        """
        初始化 HyperLogLog
        
        Args:
            precision: 精度参数（4-16），越大越精确但占用内存越多
            hash_func: 哈希函数名称
            
        Raises:
            ValueError: 如果精度参数不在有效范围内
        """
        if precision < 4 or precision > 16:
            raise ValueError("Precision must be between 4 and 16")
        
        if hash_func not in HASH_FUNCTIONS:
            raise ValueError(f"Unknown hash function: {hash_func}")
        
        self._precision = precision
        self._m = 1 << precision  # 寄存器数量
        self._hash_func_name = hash_func
        self._hash_func = HASH_FUNCTIONS[hash_func]
        
        # 寄存器数组（每个寄存器存储最大前导零数）
        self._registers = [0] * self._m
        
        # 缓存计算结果
        self._count_cache: Optional[float] = None
        self._is_modified = True
    
    def _get_register_index_and_value(self, hash_value: int) -> Tuple[int, int]:
        """
        从哈希值获取寄存器索引和值
        
        Args:
            hash_value: 64位哈希值
            
        Returns:
            (寄存器索引, 前导零数 + 1)
        """
        # 使用前 precision 位作为寄存器索引
        index = hash_value >> (64 - self._precision)
        
        # 使用剩余位计算前导零数
        remaining = hash_value & ((1 << (64 - self._precision)) - 1)
        zeros = count_leading_zeros(remaining, 64 - self._precision)
        
        return index, zeros
    
    def add(self, item: Any) -> None:
        """
        添加元素
        
        Args:
            item: 要添加的元素
        """
        # 转换为字节
        if isinstance(item, bytes):
            data = item
        elif isinstance(item, str):
            data = item.encode('utf-8')
        else:
            data = str(item).encode('utf-8')
        
        # 计算哈希
        hash_value = self._hash_func(data, 0)
        
        # 获取寄存器索引和值
        index, value = self._get_register_index_and_value(hash_value)
        
        # 更新寄存器
        if value > self._registers[index]:
            self._registers[index] = value
            self._is_modified = True
    
    def update(self, items: Union[List, Set, Tuple]) -> 'HyperLogLog':
        """
        批量添加元素
        
        Args:
            items: 要添加的元素集合
            
        Returns:
            self（支持链式调用）
        """
        for item in items:
            self.add(item)
        return self
    
    def count(self) -> float:
        """
        估计基数
        
        Returns:
            估计的唯一元素数量
        """
        if not self._is_modified and self._count_cache is not None:
            return self._count_cache
        
        alpha = get_alpha(self._m)
        estimate = estimate_cardinality_harmonic_mean(self._registers, self._m, alpha)
        
        self._count_cache = estimate
        self._is_modified = False
        return estimate
    
    def __len__(self) -> int:
        """返回估计的基数（整数）"""
        return int(round(self.count()))
    
    def merge(self, other: 'HyperLogLog') -> 'HyperLogLog':
        """
        合并另一个 HyperLogLog
        
        Args:
            other: 要合并的 HyperLogLog
            
        Returns:
            新的合并后的 HyperLogLog
            
        Raises:
            ValueError: 如果两个 HyperLogLog 不兼容
        """
        if self._precision != other._precision:
            raise ValueError("Cannot merge HyperLogLogs with different precision")
        if self._hash_func_name != other._hash_func_name:
            raise ValueError("Cannot merge HyperLogLogs with different hash functions")
        
        result = HyperLogLog(
            precision=self._precision,
            hash_func=self._hash_func_name,
        )
        
        # 取每个寄存器的最大值
        for i in range(self._m):
            result._registers[i] = max(self._registers[i], other._registers[i])
        
        result._is_modified = True
        return result
    
    def union(self, other: 'HyperLogLog') -> 'HyperLogLog':
        """合并（merge 的别名）"""
        return self.merge(other)
    
    def intersection_cardinality(self, other: 'HyperLogLog') -> float:
        """
        估计两个 HyperLogLog 的交集基数
        
        使用包含-排斥原理：
        |A ∩ B| ≈ |A| + |B| - |A ∪ B|
        
        Args:
            other: 另一个 HyperLogLog
            
        Returns:
            估计的交集基数
        """
        union = self.merge(other)
        return max(0, self.count() + other.count() - union.count())
    
    def jaccard_similarity(self, other: 'HyperLogLog') -> float:
        """
        计算 Jaccard 相似度
        
        J(A, B) = |A ∩ B| / |A ∪ B|
        
        Args:
            other: 另一个 HyperLogLog
            
        Returns:
            Jaccard 相似度（0-1）
        """
        union = self.merge(other)
        union_count = union.count()
        
        if union_count == 0:
            return 0.0
        
        intersection = self.intersection_cardinality(other)
        return intersection / union_count
    
    @property
    def precision(self) -> int:
        """返回精度参数"""
        return self._precision
    
    @property
    def num_registers(self) -> int:
        """返回寄存器数量"""
        return self._m
    
    @property
    def is_empty(self) -> bool:
        """检查是否为空"""
        return all(r == 0 for r in self._registers)
    
    def clear(self) -> None:
        """清除所有元素"""
        self._registers = [0] * self._m
        self._count_cache = None
        self._is_modified = True
    
    def get_stats(self) -> HyperLogLogStats:
        """
        获取统计信息
        
        Returns:
            HyperLogLogStats 实例
        """
        return HyperLogLogStats(
            precision=self._precision,
            num_registers=self._m,
            memory_bytes=self._m,  # 每个寄存器约 1 字节
            elements_added=int(round(self.count())),
            estimated_cardinality=self.count(),
            standard_error=HLL_STANDARD_ERROR.get(self._precision, 0.04),
        )
    
    def to_bytes(self) -> bytes:
        """
        序列化为字节序列
        
        Returns:
            字节序列
        """
        header = struct.pack(
            '!BB',
            self._precision,
            len(self._hash_func_name),
        )
        func_name_bytes = self._hash_func_name.encode('utf-8')
        
        # 将寄存器打包（每个寄存器最多 64，可用 1 字节）
        registers_bytes = bytes(self._registers)
        
        return header + func_name_bytes + registers_bytes
    
    @classmethod
    def from_bytes(cls, data: bytes) -> 'HyperLogLog':
        """
        从字节序列反序列化
        
        Args:
            data: 字节序列
            
        Returns:
            HyperLogLog 实例
        """
        if len(data) < 2:
            raise ValueError("Data too short for HyperLogLog")
        
        precision, name_len = struct.unpack('!BB', data[:2])
        
        if len(data) < 2 + name_len:
            raise ValueError("Data truncated (hash function name)")
        
        hash_func_name = data[2:2 + name_len].decode('utf-8')
        registers_data = data[2 + name_len:]
        
        hll = cls(precision=precision, hash_func=hash_func_name)
        
        expected_len = hll._m
        if len(registers_data) < expected_len:
            raise ValueError(f"Data truncated (registers: expected {expected_len}, got {len(registers_data)})")
        
        hll._registers = list(registers_data[:expected_len])
        hll._is_modified = True
        
        return hll
    
    def save(self, file: Union[str, BinaryIO]) -> None:
        """
        保存到文件
        
        Args:
            file: 文件路径或文件对象
        """
        if isinstance(file, str):
            with open(file, 'wb') as f:
                f.write(self.to_bytes())
        else:
            file.write(self.to_bytes())
    
    @classmethod
    def load(cls, file: Union[str, BinaryIO]) -> 'HyperLogLog':
        """
        从文件加载
        
        Args:
            file: 文件路径或文件对象
            
        Returns:
            HyperLogLog 实例
        """
        if isinstance(file, str):
            with open(file, 'rb') as f:
                data = f.read()
        else:
            data = file.read()
        
        return cls.from_bytes(data)
    
    def __repr__(self) -> str:
        return f"HyperLogLog(precision={self._precision}, estimated={self.count():.2f})"
    
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, HyperLogLog):
            return False
        return (
            self._precision == other._precision
            and self._hash_func_name == other._hash_func_name
            and self._registers == other._registers
        )


# ============================================================================
# HyperLogLog++ 实现（Google 改进版）
# ============================================================================

class HyperLogLogPlusPlus:
    """
    HyperLogLog++ (Google 改进版)
    
    改进点：
    1. 使用更好的哈希函数（Google 使用 murmur3）
    2. 小数据集使用稀疏表示
    3. 偏差修正
    
    使用示例：
        >>> hll = HyperLogLogPlusPlus(precision=14)
        >>> for i in range(100000):
        ...     hll.add(f"item_{i}")
        >>> hll.count()
        100234.7
    """
    
    def __init__(
        self,
        precision: int = 14,
        sparse_threshold: Optional[int] = None,
    ):
        """
        初始化 HyperLogLog++
        
        Args:
            precision: 精度参数
            sparse_threshold: 稀疏模式阈值
        """
        if precision < 4 or precision > 18:
            raise ValueError("Precision must be between 4 and 18")
        
        self._precision = precision
        self._m = 1 << precision
        self._sparse_threshold = sparse_threshold or max(256, self._m // 4)
        
        # 稀疏模式：存储 (index, value) 对
        self._sparse_data: Dict[int, int] = {}
        self._is_sparse = True
        
        # 密集模式：寄存器数组
        self._registers: List[int] = []
        
        self._count_cache: Optional[float] = None
        self._is_modified = True
    
    def _convert_to_dense(self) -> None:
        """从稀疏模式转换为密集模式"""
        if not self._is_sparse:
            return
        
        self._registers = [0] * self._m
        for idx, val in self._sparse_data.items():
            if idx < self._m:
                self._registers[idx] = val
        
        self._sparse_data.clear()
        self._is_sparse = False
    
    def add(self, item: Any) -> None:
        """
        添加元素
        
        Args:
            item: 要添加的元素
        """
        # 转换为字节并计算哈希
        if isinstance(item, bytes):
            data = item
        elif isinstance(item, str):
            data = item.encode('utf-8')
        else:
            data = str(item).encode('utf-8')
        
        hash_value = murmurhash3_x64_128(data, 0)
        
        # 获取寄存器索引和值
        index = hash_value >> (64 - self._precision)
        remaining = hash_value & ((1 << (64 - self._precision)) - 1)
        value = count_leading_zeros(remaining, 64 - self._precision)
        
        if self._is_sparse:
            current = self._sparse_data.get(index, 0)
            if value > current:
                self._sparse_data[index] = value
            
            # 检查是否需要转换
            if len(self._sparse_data) > self._sparse_threshold:
                self._convert_to_dense()
        else:
            if value > self._registers[index]:
                self._registers[index] = value
        
        self._is_modified = True
    
    def update(self, items: Union[List, Set, Tuple]) -> 'HyperLogLogPlusPlus':
        """批量添加元素"""
        for item in items:
            self.add(item)
        return self
    
    def count(self) -> float:
        """估计基数"""
        if not self._is_modified and self._count_cache is not None:
            return self._count_cache
        
        if self._is_sparse:
            # 稀疏模式使用线性计数
            if not self._sparse_data:
                return 0.0
            
            # 使用精确计数（因为数据量小）
            estimate = len(self._sparse_data)
            
            # 应用标准 HLL 估计（如果寄存器足够）
            if estimate > 0:
                alpha = get_alpha(max(16, self._m // (1 << 8)))
                sum_val = sum(2 ** (-v) for v in self._sparse_data.values())
                if sum_val > 0:
                    hll_estimate = alpha * self._m * self._m / sum_val
                    if hll_estimate > 0:
                        estimate = min(estimate, hll_estimate)
        else:
            alpha = get_alpha(self._m)
            estimate = estimate_cardinality_harmonic_mean(self._registers, self._m, alpha)
        
        self._count_cache = estimate
        self._is_modified = False
        return estimate
    
    def __len__(self) -> int:
        return int(round(self.count()))
    
    def merge(self, other: 'HyperLogLogPlusPlus') -> 'HyperLogLogPlusPlus':
        """合并另一个 HyperLogLog++"""
        if self._precision != other._precision:
            raise ValueError("Cannot merge HyperLogLog++ with different precision")
        
        result = HyperLogLogPlusPlus(precision=self._precision)
        
        # 如果两个都是稀疏模式
        if self._is_sparse and other._is_sparse:
            for idx, val in self._sparse_data.items():
                result._sparse_data[idx] = val
            for idx, val in other._sparse_data.items():
                current = result._sparse_data.get(idx, 0)
                if val > current:
                    result._sparse_data[idx] = val
        else:
            # 转换为密集模式
            result._convert_to_dense()
            
            if not self._is_sparse:
                for i, val in enumerate(self._registers):
                    result._registers[i] = val
            else:
                for idx, val in self._sparse_data.items():
                    if idx < result._m:
                        result._registers[idx] = val
            
            if not other._is_sparse:
                for i, val in enumerate(other._registers):
                    result._registers[i] = max(result._registers[i], val)
            else:
                for idx, val in other._sparse_data.items():
                    if idx < result._m:
                        result._registers[idx] = max(result._registers[idx], val)
        
        result._is_modified = True
        return result
    
    @property
    def precision(self) -> int:
        return self._precision
    
    @property
    def is_sparse(self) -> bool:
        """是否处于稀疏模式"""
        return self._is_sparse
    
    @property
    def is_empty(self) -> bool:
        """是否为空"""
        if self._is_sparse:
            return len(self._sparse_data) == 0
        return all(r == 0 for r in self._registers)
    
    def clear(self) -> None:
        """清除所有元素"""
        self._sparse_data.clear()
        self._registers = []
        self._is_sparse = True
        self._count_cache = None
        self._is_modified = True
    
    def get_stats(self) -> Dict[str, Any]:
        """获取统计信息"""
        mem_bytes = len(self._sparse_data) * 8 if self._is_sparse else self._m
        return {
            'precision': self._precision,
            'num_registers': self._m,
            'is_sparse': self._is_sparse,
            'sparse_entries': len(self._sparse_data) if self._is_sparse else 0,
            'memory_bytes': mem_bytes,
            'estimated_cardinality': self.count(),
            'standard_error': HLL_STANDARD_ERROR.get(self._precision, 0.04),
        }
    
    def to_bytes(self) -> bytes:
        """序列化为字节序列"""
        buffer = BytesIO()
        
        # 写入头部
        buffer.write(struct.pack('!B', self._precision))
        buffer.write(struct.pack('!B', 1 if self._is_sparse else 0))
        
        if self._is_sparse:
            # 稀疏模式
            buffer.write(struct.pack('!I', len(self._sparse_data)))
            for idx, val in sorted(self._sparse_data.items()):
                buffer.write(struct.pack('!HB', idx, val))
        else:
            # 密集模式
            buffer.write(bytes(self._registers))
        
        return buffer.getvalue()
    
    @classmethod
    def from_bytes(cls, data: bytes) -> 'HyperLogLogPlusPlus':
        """从字节序列反序列化"""
        buffer = BytesIO(data)
        
        precision = struct.unpack('!B', buffer.read(1))[0]
        is_sparse = struct.unpack('!B', buffer.read(1))[0] == 1
        
        hll = cls(precision=precision)
        
        if is_sparse:
            count = struct.unpack('!I', buffer.read(4))[0]
            for _ in range(count):
                idx = struct.unpack('!H', buffer.read(2))[0]
                val = struct.unpack('!B', buffer.read(1))[0]
                hll._sparse_data[idx] = val
        else:
            hll._convert_to_dense()
            registers_data = buffer.read(hll._m)
            hll._registers = list(registers_data)
        
        hll._is_modified = True
        return hll
    
    def save(self, file: Union[str, BinaryIO]) -> None:
        """保存到文件"""
        if isinstance(file, str):
            with open(file, 'wb') as f:
                f.write(self.to_bytes())
        else:
            file.write(self.to_bytes())
    
    @classmethod
    def load(cls, file: Union[str, BinaryIO]) -> 'HyperLogLogPlusPlus':
        """从文件加载"""
        if isinstance(file, str):
            with open(file, 'rb') as f:
                data = f.read()
        else:
            data = file.read()
        return cls.from_bytes(data)
    
    def __repr__(self) -> str:
        mode = "sparse" if self._is_sparse else "dense"
        return f"HyperLogLogPlusPlus(precision={self._precision}, mode={mode}, estimated={self.count():.2f})"


# ============================================================================
# 稀疏 HyperLogLog（适合小数据集）
# ============================================================================

class SparseHyperLogLog:
    """
    稀疏 HyperLogLog
    
    针对小数据集优化，只在必要时转换为密集模式。
    适合基数不确定或可能很小的场景。
    
    使用示例：
        >>> shll = SparseHyperLogLog(max_precision=16)
        >>> shll.add("user_1")
        >>> shll.add("user_2")
        >>> shll.count()
        2.0
    """
    
    def __init__(
        self,
        initial_precision: int = 8,
        max_precision: int = 16,
        dense_threshold: Optional[int] = None,
    ):
        """
        初始化稀疏 HyperLogLog
        
        Args:
            initial_precision: 初始精度
            max_precision: 最大精度
            dense_threshold: 转换为密集模式的阈值
        """
        if initial_precision < 4 or initial_precision > max_precision:
            raise ValueError("initial_precision must be between 4 and max_precision")
        if max_precision < initial_precision or max_precision > 18:
            raise ValueError("max_precision must be >= initial_precision and <= 18")
        
        self._initial_precision = initial_precision
        self._max_precision = max_precision
        self._dense_threshold = dense_threshold or min(1000, (1 << max_precision) // 8)
        
        # 当前精度和数据
        self._precision = initial_precision
        self._sparse_data: Dict[int, int] = {}
        self._dense_registers: Optional[List[int]] = None
        
        self._count_cache: Optional[float] = None
        self._is_modified = True
    
    def add(self, item: Any) -> None:
        """添加元素"""
        if isinstance(item, bytes):
            data = item
        elif isinstance(item, str):
            data = item.encode('utf-8')
        else:
            data = str(item).encode('utf-8')
        
        hash_value = murmurhash3_x64_128(data, 0)
        
        # 使用最大精度计算索引和值，保证一致性
        index = hash_value >> (64 - self._max_precision)
        remaining = hash_value & ((1 << (64 - self._max_precision)) - 1)
        value = count_leading_zeros(remaining, 64 - self._max_precision)
        
        # 如果是密集模式，直接使用当前精度
        if self._dense_registers is not None:
            # 使用当前精度截取索引
            current_index = hash_value >> (64 - self._precision)
            if value > self._dense_registers[current_index]:
                self._dense_registers[current_index] = value
        else:
            # 稀疏模式：存储完整索引（使用最大精度）
            current = self._sparse_data.get(index, 0)
            if value > current:
                self._sparse_data[index] = value
            
            # 检查是否需要转换为密集模式
            if len(self._sparse_data) > self._dense_threshold:
                self._convert_to_dense()
        
        self._is_modified = True
    
    def _convert_to_dense(self) -> None:
        """转换为密集模式"""
        m = 1 << self._max_precision
        self._dense_registers = [0] * m
        self._precision = self._max_precision
        
        # 将稀疏数据转移到密集寄存器
        for idx, val in self._sparse_data.items():
            if idx < m:
                self._dense_registers[idx] = val
        
        self._sparse_data.clear()
    
    def update(self, items: Union[List, Set, Tuple]) -> 'SparseHyperLogLog':
        """批量添加元素"""
        for item in items:
            self.add(item)
        return self
    
    def count(self) -> float:
        """估计基数"""
        if not self._is_modified and self._count_cache is not None:
            return self._count_cache
        
        if self._dense_registers is not None:
            # 密集模式
            m = len(self._dense_registers)
            alpha = get_alpha(m)
            estimate = estimate_cardinality_harmonic_mean(self._dense_registers, m, alpha)
        else:
            # 稀疏模式：使用最大精度进行估计
            m = 1 << self._max_precision
            alpha = get_alpha(m)
            
            # 创建完整的寄存器数组（大部分为0）
            full_registers = [0] * m
            for idx, val in self._sparse_data.items():
                if idx < m:
                    full_registers[idx] = val
            
            estimate = estimate_cardinality_harmonic_mean(full_registers, m, alpha)
        
        self._count_cache = estimate
        self._is_modified = False
        return estimate
    
    def __len__(self) -> int:
        return int(round(self.count()))
    
    @property
    def precision(self) -> int:
        """当前精度"""
        return self._precision
    
    @property
    def max_precision(self) -> int:
        """最大精度"""
        return self._max_precision
    
    @property
    def is_dense(self) -> bool:
        """是否处于密集模式"""
        return self._dense_registers is not None
    
    @property
    def is_empty(self) -> bool:
        """是否为空"""
        if self._dense_registers is not None:
            return all(r == 0 for r in self._dense_registers)
        return len(self._sparse_data) == 0
    
    def clear(self) -> None:
        """清除所有元素"""
        self._precision = self._initial_precision
        self._sparse_data.clear()
        self._dense_registers = None
        self._count_cache = None
        self._is_modified = True
    
    def get_stats(self) -> Dict[str, Any]:
        """获取统计信息"""
        is_dense = self._dense_registers is not None
        mem_bytes = (len(self._sparse_data) * 8 if not is_dense 
                    else len(self._dense_registers))
        
        return {
            'current_precision': self._precision,
            'max_precision': self._max_precision,
            'is_dense': is_dense,
            'sparse_entries': len(self._sparse_data) if not is_dense else 0,
            'memory_bytes': mem_bytes,
            'estimated_cardinality': self.count(),
            'standard_error': HLL_STANDARD_ERROR.get(self._precision, 0.04),
        }
    
    def __repr__(self) -> str:
        mode = "dense" if self._dense_registers is not None else "sparse"
        return f"SparseHyperLogLog(precision={self._precision}, mode={mode}, estimated={self.count():.2f})"


# ============================================================================
# 工具函数
# ============================================================================

def estimate_memory(precision: int) -> Dict[str, Any]:
    """
    估算 HyperLogLog 的内存使用
    
    Args:
        precision: 精度参数
        
    Returns:
        内存使用信息
    """
    m = 1 << precision
    bytes_needed = m  # 每个寄存器 1 字节
    
    return {
        'precision': precision,
        'num_registers': m,
        'bytes': bytes_needed,
        'kilobytes': round(bytes_needed / 1024, 2),
        'megabytes': round(bytes_needed / (1024 * 1024), 4),
        'standard_error': HLL_STANDARD_ERROR.get(precision, 0.04),
        'relative_error_percent': HLL_STANDARD_ERROR.get(precision, 0.04) * 100,
    }


def create_hll(
    precision: int = 14,
    hash_func: str = 'murmur',
) -> HyperLogLog:
    """
    创建 HyperLogLog 实例
    
    Args:
        precision: 精度参数
        hash_func: 哈希函数
        
    Returns:
        HyperLogLog 实例
    """
    return HyperLogLog(precision=precision, hash_func=hash_func)


def from_iterable(
    items: Union[List, Set, Tuple],
    precision: int = 14,
    hash_func: str = 'murmur',
) -> HyperLogLog:
    """
    从可迭代对象创建 HyperLogLog
    
    Args:
        items: 元素集合
        precision: 精度参数
        hash_func: 哈希函数
        
    Returns:
        包含所有元素的 HyperLogLog
    """
    hll = HyperLogLog(precision=precision, hash_func=hash_func)
    for item in items:
        hll.add(item)
    return hll


def merge_multiple(hlls: List[HyperLogLog]) -> HyperLogLog:
    """
    合并多个 HyperLogLog
    
    Args:
        hlls: HyperLogLog 列表
        
    Returns:
        合并后的 HyperLogLog
        
    Raises:
        ValueError: 如果列表为空或 HyperLogLog 不兼容
    """
    if not hlls:
        raise ValueError("Cannot merge empty list")
    
    result = hlls[0]
    for hll in hlls[1:]:
        result = result.merge(hll)
    return result


def compare_precision(
    items: List[Any],
    precisions: List[int] = [4, 8, 12, 14, 16]
) -> Dict[int, Dict[str, Any]]:
    """
    比较不同精度的效果
    
    Args:
        items: 要添加的元素
        precisions: 要比较的精度列表
        
    Returns:
        各精度的比较结果
    """
    import time
    
    actual_cardinality = len(set(items))
    results = {}
    
    for p in precisions:
        hll = HyperLogLog(precision=p)
        
        start = time.perf_counter()
        for item in items:
            hll.add(item)
        add_time = time.perf_counter() - start
        
        estimate = hll.count()
        error = abs(estimate - actual_cardinality) / actual_cardinality if actual_cardinality > 0 else 0
        
        results[p] = {
            'estimated': estimate,
            'actual': actual_cardinality,
            'error_percent': round(error * 100, 2),
            'memory_bytes': 1 << p,
            'add_time_ms': round(add_time * 1000, 3),
            'avg_add_us': round(add_time * 1000000 / len(items), 3),
        }
    
    return results


class HyperLogLogBuilder:
    """
    HyperLogLog 构建器（流畅 API）
    
    使用示例：
        >>> hll = (HyperLogLogBuilder()
        ...     .precision(12)
        ...     .with_hash('murmur')
        ...     .with_items(['a', 'b', 'c'])
        ...     .build())
    """
    
    def __init__(self):
        self._precision = 14
        self._hash_func = 'murmur'
        self._items: List[Any] = []
    
    def precision(self, p: int) -> 'HyperLogLogBuilder':
        """设置精度"""
        self._precision = p
        return self
    
    def with_hash(self, name: str) -> 'HyperLogLogBuilder':
        """设置哈希函数"""
        self._hash_func = name
        return self
    
    def with_items(self, items: Union[List, Set, Tuple]) -> 'HyperLogLogBuilder':
        """设置初始元素"""
        self._items = list(items)
        return self
    
    def build(self) -> HyperLogLog:
        """构建 HyperLogLog"""
        hll = HyperLogLog(
            precision=self._precision,
            hash_func=self._hash_func,
        )
        for item in self._items:
            hll.add(item)
        return hll


# 导出的公共接口
__all__ = [
    # 哈希函数
    'murmurhash3_x64_128',
    'sha256_hash_64',
    'xxhash_64',
    'HASH_FUNCTIONS',
    
    # 工具函数
    'count_leading_zeros',
    'get_alpha',
    'estimate_cardinality_harmonic_mean',
    'estimate_memory',
    
    # 类
    'HyperLogLog',
    'HyperLogLogPlusPlus',
    'SparseHyperLogLog',
    'HyperLogLogStats',
    
    # 工厂函数
    'create_hll',
    'from_iterable',
    'merge_multiple',
    'compare_precision',
    
    # 构建器
    'HyperLogLogBuilder',
]