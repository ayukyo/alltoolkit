"""
Bloom Filter Utils - 布隆过滤器工具库

提供多种布隆过滤器实现：
- BloomFilter: 标准布隆过滤器
- ScalableBloomFilter: 可扩展布隆过滤器（自动扩容）
- CountingBloomFilter: 计数布隆过滤器（支持删除）

特点：
- 零外部依赖，纯 Python 标准库实现
- 支持多种哈希函数（MurmurHash、FNV、djb2）
- 完整的序列化/反序列化支持
- 统计信息和性能分析工具

使用场景：
- 缓存过滤（避免缓存穿透）
- 垃圾邮件过滤
- URL 去重
- 数据库查询优化
- 推荐系统去重
"""

import math
import struct
import hashlib
import pickle
from typing import (
    Any, Callable, Dict, Iterator, List, Optional, 
    Set, Tuple, Union, BinaryIO
)
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from io import BytesIO


# ============================================================================
# 哈希函数实现
# ============================================================================

def murmurhash3_x86_32(data: bytes, seed: int = 0) -> int:
    """
    MurmurHash3 x86 32-bit 实现
    
    Args:
        data: 要哈希的字节
        seed: 哈希种子
        
    Returns:
        32位哈希值
    """
    c1 = 0xcc9e2d51
    c2 = 0x1b873593
    
    h1 = seed
    length = len(data)
    nblocks = length // 4
    
    # 处理 4 字节块
    for i in range(nblocks):
        k1 = struct.unpack('<I', data[i*4:(i+1)*4])[0]
        k1 = (k1 * c1) & 0xFFFFFFFF
        k1 = ((k1 << 15) | (k1 >> 17)) & 0xFFFFFFFF
        k1 = (k1 * c2) & 0xFFFFFFFF
        
        h1 ^= k1
        h1 = ((h1 << 13) | (h1 >> 19)) & 0xFFFFFFFF
        h1 = ((h1 * 5) + 0xe6546b64) & 0xFFFFFFFF
    
    # 处理尾部字节
    tail = data[nblocks * 4:]
    k1 = 0
    
    if len(tail) >= 3:
        k1 ^= tail[2] << 16
    if len(tail) >= 2:
        k1 ^= tail[1] << 8
    if len(tail) >= 1:
        k1 ^= tail[0]
        k1 = (k1 * c1) & 0xFFFFFFFF
        k1 = ((k1 << 15) | (k1 >> 17)) & 0xFFFFFFFF
        k1 = (k1 * c2) & 0xFFFFFFFF
        h1 ^= k1
    
    h1 ^= length
    h1 ^= h1 >> 16
    h1 = (h1 * 0x85ebca6b) & 0xFFFFFFFF
    h1 ^= h1 >> 13
    h1 = (h1 * 0xc2b2ae35) & 0xFFFFFFFF
    h1 ^= h1 >> 16
    
    return h1


def fnv_hash_32(data: bytes, seed: int = 0) -> int:
    """
    FNV-1a 32-bit 哈希
    
    Args:
        data: 要哈希的字节
        seed: 哈希种子（会混入初始值）
        
    Returns:
        32位哈希值
    """
    FNV_32_PRIME = 0x01000193
    FNV1_32A_INIT = 0x811c9dc5
    
    h = (FNV1_32A_INIT ^ seed) & 0xFFFFFFFF
    for byte in data:
        h ^= byte
        h = (h * FNV_32_PRIME) & 0xFFFFFFFF
    return h


def djb2_hash(data: bytes, seed: int = 0) -> int:
    """
    DJB2 哈希算法
    
    Args:
        data: 要哈希的字节
        seed: 哈希种子
        
    Returns:
        32位哈希值
    """
    h = (5381 + seed) & 0xFFFFFFFF
    for byte in data:
        h = (((h << 5) + h) + byte) & 0xFFFFFFFF
    return h


def sha256_hash(data: bytes, seed: int = 0) -> int:
    """
    SHA-256 哈希（取前 4 字节作为 32 位值）
    
    Args:
        data: 要哈希的字节
        seed: 哈希种子（会追加到数据末尾）
        
    Returns:
        32位哈希值
    """
    hasher = hashlib.sha256(data + seed.to_bytes(4, 'little'))
    return struct.unpack('<I', hasher.digest()[:4])[0]


# 哈希函数注册表
HASH_FUNCTIONS: Dict[str, Callable[[bytes, int], int]] = {
    'murmur': murmurhash3_x86_32,
    'fnv': fnv_hash_32,
    'djb2': djb2_hash,
    'sha256': sha256_hash,
}


# ============================================================================
# 工具函数
# ============================================================================

def optimal_size(n: int, p: float) -> Tuple[int, int]:
    """
    计算最优的位数组大小和哈希函数数量
    
    Args:
        n: 预期元素数量
        p: 期望的假阳性率
        
    Returns:
        (位数组大小, 哈希函数数量)
        
    Raises:
        ValueError: 如果参数无效
    """
    if n <= 0:
        raise ValueError("Expected number of elements must be positive")
    if p <= 0 or p >= 1:
        raise ValueError("False positive rate must be between 0 and 1")
    
    # m = -n * ln(p) / (ln(2)^2)
    m = int(math.ceil(-n * math.log(p) / (math.log(2) ** 2)))
    # k = (m / n) * ln(2)
    k = int(round((m / n) * math.log(2)))
    
    # 确保至少有 1 个哈希函数
    k = max(1, k)
    
    return m, k


def false_positive_rate(n: int, m: int, k: int) -> float:
    """
    计算假阳性率
    
    Args:
        n: 元素数量
        m: 位数组大小
        k: 哈希函数数量
        
    Returns:
        假阳性率
    """
    if m <= 0 or k <= 0:
        return 1.0
    
    # p = (1 - e^(-kn/m))^k
    return (1 - math.exp(-k * n / m)) ** k


class BitArray:
    """
    紧凑位数组实现
    
    使用字节数组存储位，支持高效的位操作
    """
    
    def __init__(self, size: int):
        """
        初始化位数组
        
        Args:
            size: 位数组大小（位数）
            
        Raises:
            ValueError: 如果大小为负
        """
        if size < 0:
            raise ValueError("Size must be non-negative")
        
        self._size = size
        self._bytes = bytearray((size + 7) // 8)
    
    def __len__(self) -> int:
        """返回位数组大小"""
        return self._size
    
    def __getitem__(self, index: int) -> bool:
        """
        获取指定位置的位值
        
        Args:
            index: 位索引
            
        Returns:
            位值（True/False）
            
        Raises:
            IndexError: 如果索引越界
        """
        if index < 0 or index >= self._size:
            raise IndexError(f"Index {index} out of range [0, {self._size})")
        return bool(self._bytes[index >> 3] & (1 << (index & 7)))
    
    def __setitem__(self, index: int, value: bool) -> None:
        """
        设置指定位置的位值
        
        Args:
            index: 位索引
            value: 位值（True/False）
            
        Raises:
            IndexError: 如果索引越界
        """
        if index < 0 or index >= self._size:
            raise IndexError(f"Index {index} out of range [0, {self._size})")
        
        byte_index = index >> 3
        bit_mask = 1 << (index & 7)
        
        if value:
            self._bytes[byte_index] |= bit_mask
        else:
            self._bytes[byte_index] &= ~bit_mask
    
    def set(self, index: int) -> None:
        """设置位为 1"""
        self[index] = True
    
    def clear(self, index: int) -> None:
        """清除位为 0"""
        self[index] = False
    
    def toggle(self, index: int) -> bool:
        """
        翻转位值
        
        Returns:
            翻转后的值
        """
        old_value = self[index]
        self[index] = not old_value
        return not old_value
    
    def count_set_bits(self) -> int:
        """计算已设置的位数"""
        count = 0
        for byte in self._bytes:
            count += bin(byte).count('1')
        return count
    
    def clear_all(self) -> None:
        """清除所有位"""
        for i in range(len(self._bytes)):
            self._bytes[i] = 0
    
    def set_all(self) -> None:
        """设置所有位"""
        for i in range(len(self._bytes)):
            self._bytes[i] = 0xFF
        # 清除超出实际大小的位
        if self._size % 8 != 0:
            last_byte_bits = self._size % 8
            mask = (1 << last_byte_bits) - 1
            self._bytes[-1] &= mask
    
    def to_bytes(self) -> bytes:
        """转换为字节序列"""
        return bytes(self._bytes)
    
    @classmethod
    def from_bytes(cls, data: bytes, size: int) -> 'BitArray':
        """
        从字节序列创建位数组
        
        Args:
            data: 字节序列
            size: 位数组大小
            
        Returns:
            BitArray 实例
        """
        arr = cls(size)
        arr._bytes = bytearray(data)
        return arr
    
    def __repr__(self) -> str:
        return f"BitArray(size={self._size}, set_bits={self.count_set_bits()})"


# ============================================================================
# 标准布隆过滤器
# ============================================================================

@dataclass
class BloomFilterStats:
    """布隆过滤器统计信息"""
    size: int  # 位数组大小
    hash_count: int  # 哈希函数数量
    elements_added: int  # 已添加元素数量
    set_bits: int  # 已设置的位数
    fill_ratio: float  # 填充率
    estimated_fp_rate: float  # 估计的假阳性率
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            'size': self.size,
            'hash_count': self.hash_count,
            'elements_added': self.elements_added,
            'set_bits': self.set_bits,
            'fill_ratio': self.fill_ratio,
            'estimated_fp_rate': self.estimated_fp_rate,
        }


class BloomFilter:
    """
    标准布隆过滤器
    
    特点：
    - 空间效率高
    - 查询时间 O(k)，k 为哈希函数数量
    - 无假阴性
    - 可能存在假阳性
    
    使用示例：
        >>> bf = BloomFilter(expected_elements=1000, false_positive_rate=0.01)
        >>> bf.add("hello")
        >>> bf.add("world")
        >>> "hello" in bf
        True
        >>> "foo" in bf
        False
    """
    
    def __init__(
        self,
        expected_elements: int = 10000,
        false_positive_rate: float = 0.01,
        hash_func: str = 'murmur',
        size: Optional[int] = None,
        hash_count: Optional[int] = None,
    ):
        """
        初始化布隆过滤器
        
        Args:
            expected_elements: 预期元素数量
            false_positive_rate: 期望的假阳性率
            hash_func: 哈希函数名称 ('murmur', 'fnv', 'djb2', 'sha256')
            size: 位数组大小（可选，覆盖自动计算）
            hash_count: 哈希函数数量（可选，覆盖自动计算）
            
        Raises:
            ValueError: 如果参数无效
        """
        if expected_elements <= 0:
            raise ValueError("Expected elements must be positive")
        if false_positive_rate <= 0 or false_positive_rate >= 1:
            raise ValueError("False positive rate must be between 0 and 1")
        if hash_func not in HASH_FUNCTIONS:
            raise ValueError(f"Unknown hash function: {hash_func}")
        
        self._hash_func_name = hash_func
        self._hash_func = HASH_FUNCTIONS[hash_func]
        self._expected_elements = expected_elements
        self._target_fp_rate = false_positive_rate
        
        # 计算或使用指定的大小和哈希数量
        if size is not None and hash_count is not None:
            self._size = size
            self._hash_count = hash_count
        else:
            self._size, self._hash_count = optimal_size(expected_elements, false_positive_rate)
        
        self._bit_array = BitArray(self._size)
        self._elements_added = 0
    
    def _get_hash_indices(self, item: Any) -> Iterator[int]:
        """
        获取项目的所有哈希索引
        
        使用双哈希技术生成多个哈希值：
        h(i) = h1 + i * h2
        
        Args:
            item: 要哈希的项目
            
        Yields:
            哈希索引
        """
        # 将项目转换为字节
        if isinstance(item, bytes):
            data = item
        elif isinstance(item, str):
            data = item.encode('utf-8')
        else:
            data = str(item).encode('utf-8')
        
        # 计算两个基础哈希值
        h1 = self._hash_func(data, 0)
        h2 = self._hash_func(data, h1)
        
        # 生成 k 个哈希索引
        for i in range(self._hash_count):
            index = (h1 + i * h2) % self._size
            yield index
    
    def add(self, item: Any) -> None:
        """
        添加元素到布隆过滤器
        
        Args:
            item: 要添加的元素
        """
        for index in self._get_hash_indices(item):
            self._bit_array.set(index)
        self._elements_added += 1
    
    def __contains__(self, item: Any) -> bool:
        """
        检查元素是否可能在布隆过滤器中
        
        Args:
            item: 要检查的元素
            
        Returns:
            True 如果元素可能存在（可能有假阳性）
            False 如果元素肯定不存在
        """
        return all(self._bit_array[index] for index in self._get_hash_indices(item))
    
    def might_contain(self, item: Any) -> bool:
        """检查元素是否可能存在（等同于 __contains__）"""
        return item in self
    
    def __len__(self) -> int:
        """返回已添加的元素数量"""
        return self._elements_added
    
    @property
    def size(self) -> int:
        """位数组大小"""
        return self._size
    
    @property
    def hash_count(self) -> int:
        """哈希函数数量"""
        return self._hash_count
    
    @property
    def is_empty(self) -> bool:
        """检查布隆过滤器是否为空"""
        return self._elements_added == 0
    
    def clear(self) -> None:
        """清除所有元素"""
        self._bit_array.clear_all()
        self._elements_added = 0
    
    def get_stats(self) -> BloomFilterStats:
        """
        获取布隆过滤器统计信息
        
        Returns:
            BloomFilterStats 实例
        """
        set_bits = self._bit_array.count_set_bits()
        fill_ratio = set_bits / self._size if self._size > 0 else 0
        estimated_fp = false_positive_rate(self._elements_added, self._size, self._hash_count)
        
        return BloomFilterStats(
            size=self._size,
            hash_count=self._hash_count,
            elements_added=self._elements_added,
            set_bits=set_bits,
            fill_ratio=fill_ratio,
            estimated_fp_rate=estimated_fp,
        )
    
    def update(self, items: Union[List, Set, Tuple]) -> 'BloomFilter':
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
    
    def union(self, other: 'BloomFilter') -> 'BloomFilter':
        """
        返回两个布隆过滤器的并集
        
        Args:
            other: 另一个布隆过滤器
            
        Returns:
            新的布隆过滤器
            
        Raises:
            ValueError: 如果两个过滤器不兼容
        """
        if self._size != other._size or self._hash_count != other._hash_count:
            raise ValueError("Cannot union bloom filters with different sizes or hash counts")
        
        result = BloomFilter(
            size=self._size,
            hash_count=self._hash_count,
            hash_func=self._hash_func_name,
            expected_elements=self._expected_elements,
        )
        
        # 按位或合并
        for i in range(len(self._bit_array._bytes)):
            result._bit_array._bytes[i] = self._bit_array._bytes[i] | other._bit_array._bytes[i]
        
        result._elements_added = self._elements_added + other._elements_added
        return result
    
    def intersect(self, other: 'BloomFilter') -> 'BloomFilter':
        """
        返回两个布隆过滤器的交集
        
        注意：交集的结果可能包含假阴性
        
        Args:
            other: 另一个布隆过滤器
            
        Returns:
            新的布隆过滤器
            
        Raises:
            ValueError: 如果两个过滤器不兼容
        """
        if self._size != other._size or self._hash_count != other._hash_count:
            raise ValueError("Cannot intersect bloom filters with different sizes or hash counts")
        
        result = BloomFilter(
            size=self._size,
            hash_count=self._hash_count,
            hash_func=self._hash_func_name,
            expected_elements=self._expected_elements,
        )
        
        # 按位与合并
        for i in range(len(self._bit_array._bytes)):
            result._bit_array._bytes[i] = self._bit_array._bytes[i] & other._bit_array._bytes[i]
        
        # 估计元素数量
        result._elements_added = min(self._elements_added, other._elements_added)
        return result
    
    def to_bytes(self) -> bytes:
        """
        序列化为字节序列
        
        Returns:
            字节序列
        """
        header = struct.pack(
            '!IIdI',
            self._size,
            self._hash_count,
            self._elements_added,
            len(self._hash_func_name),
        )
        func_name_bytes = self._hash_func_name.encode('utf-8')
        return header + func_name_bytes + self._bit_array.to_bytes()
    
    @classmethod
    def from_bytes(cls, data: bytes) -> 'BloomFilter':
        """
        从字节序列反序列化
        
        Args:
            data: 字节序列
            
        Returns:
            BloomFilter 实例
            
        Raises:
            ValueError: 如果数据格式无效
        """
        if len(data) < 20:  # 最小头部大小
            raise ValueError("Data too short for bloom filter")
        
        size, hash_count, elements_added, name_len = struct.unpack('!IIdI', data[:20])
        
        if len(data) < 20 + name_len:
            raise ValueError("Data truncated (hash function name)")
        
        hash_func_name = data[20:20 + name_len].decode('utf-8')
        
        bits_data = data[20 + name_len:]
        expected_bytes = (size + 7) // 8
        if len(bits_data) < expected_bytes:
            raise ValueError(f"Data truncated (bits: expected {expected_bytes}, got {len(bits_data)})")
        
        bf = cls(
            expected_elements=1000,  # 临时值，会被覆盖
            hash_func=hash_func_name,
            size=size,
            hash_count=hash_count,
        )
        bf._bit_array = BitArray.from_bytes(bits_data[:expected_bytes], size)
        bf._elements_added = int(elements_added)
        
        return bf
    
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
    def load(cls, file: Union[str, BinaryIO]) -> 'BloomFilter':
        """
        从文件加载
        
        Args:
            file: 文件路径或文件对象
            
        Returns:
            BloomFilter 实例
        """
        if isinstance(file, str):
            with open(file, 'rb') as f:
                data = f.read()
        else:
            data = file.read()
        
        return cls.from_bytes(data)
    
    def __repr__(self) -> str:
        stats = self.get_stats()
        return (
            f"BloomFilter(size={self._size}, hash_count={self._hash_count}, "
            f"elements={self._elements_added}, fp_rate={stats.estimated_fp_rate:.6f})"
        )
    
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, BloomFilter):
            return False
        return (
            self._size == other._size
            and self._hash_count == other._hash_count
            and self._hash_func_name == other._hash_func_name
            and self._bit_array.to_bytes() == other._bit_array.to_bytes()
        )


# ============================================================================
# 可扩展布隆过滤器
# ============================================================================

@dataclass
class ScalableBloomFilterConfig:
    """可扩展布隆过滤器配置"""
    initial_capacity: int = 10000
    false_positive_rate: float = 0.01
    growth_factor: float = 2.0  # 容量增长因子
    fp_rate_factor: float = 0.9  # 假阳性率衰减因子
    hash_func: str = 'murmur'
    max_filters: int = 32  # 最大过滤器数量


class ScalableBloomFilter:
    """
    可扩展布隆过滤器
    
    当元素数量超过容量时自动扩容，创建新的布隆过滤器。
    假阳性率随过滤器数量增加而降低。
    
    使用示例：
        >>> sbf = ScalableBloomFilter(initial_capacity=100, false_positive_rate=0.01)
        >>> for i in range(1000):
        ...     sbf.add(f"item_{i}")
        >>> "item_500" in sbf
        True
    """
    
    def __init__(self, config: Optional[ScalableBloomFilterConfig] = None, **kwargs):
        """
        初始化可扩展布隆过滤器
        
        Args:
            config: 配置对象
            **kwargs: 配置参数（会覆盖 config）
        """
        if config is None:
            config = ScalableBloomFilterConfig()
        
        # 允许通过 kwargs 覆盖配置
        self._initial_capacity = kwargs.get('initial_capacity', config.initial_capacity)
        self._base_fp_rate = kwargs.get('false_positive_rate', config.false_positive_rate)
        self._growth_factor = kwargs.get('growth_factor', config.growth_factor)
        self._fp_rate_factor = kwargs.get('fp_rate_factor', config.fp_rate_factor)
        self._hash_func = kwargs.get('hash_func', config.hash_func)
        self._max_filters = kwargs.get('max_filters', config.max_filters)
        
        self._filters: List[BloomFilter] = []
        self._total_elements = 0
        self._current_capacity = self._initial_capacity
        self._current_fp_rate = self._base_fp_rate / 2  # 第一个过滤器用更严格的假阳性率
        
        # 创建第一个过滤器
        self._add_new_filter()
    
    def _add_new_filter(self) -> None:
        """添加新的布隆过滤器"""
        if len(self._filters) >= self._max_filters:
            raise RuntimeError(f"Maximum number of filters ({self._max_filters}) reached")
        
        bf = BloomFilter(
            expected_elements=self._current_capacity,
            false_positive_rate=self._current_fp_rate,
            hash_func=self._hash_func,
        )
        self._filters.append(bf)
        
        # 更新下一个过滤器的参数
        self._current_capacity = int(self._current_capacity * self._growth_factor)
        self._current_fp_rate *= self._fp_rate_factor
    
    def add(self, item: Any) -> None:
        """
        添加元素
        
        Args:
            item: 要添加的元素
        """
        # 检查是否需要新过滤器
        if len(self._filters[-1]) >= self._current_capacity // self._growth_factor:
            try:
                self._add_new_filter()
            except RuntimeError:
                pass  # 已达最大过滤器数量，继续使用当前过滤器
        
        self._filters[-1].add(item)
        self._total_elements += 1
    
    def __contains__(self, item: Any) -> bool:
        """检查元素是否可能存在"""
        return any(item in bf for bf in self._filters)
    
    def might_contain(self, item: Any) -> bool:
        """检查元素是否可能存在"""
        return item in self
    
    def __len__(self) -> int:
        """返回已添加的元素数量"""
        return self._total_elements
    
    @property
    def filter_count(self) -> int:
        """返回内部过滤器数量"""
        return len(self._filters)
    
    @property
    def is_empty(self) -> bool:
        """检查是否为空"""
        return self._total_elements == 0
    
    def clear(self) -> None:
        """清除所有元素"""
        self._filters.clear()
        self._total_elements = 0
        self._current_capacity = self._initial_capacity
        self._current_fp_rate = self._base_fp_rate / 2
        self._add_new_filter()
    
    def get_stats(self) -> Dict[str, Any]:
        """
        获取统计信息
        
        Returns:
            统计信息字典
        """
        filter_stats = [bf.get_stats().to_dict() for bf in self._filters]
        total_size = sum(s['size'] for s in filter_stats)
        total_set_bits = sum(s['set_bits'] for s in filter_stats)
        
        # 估计整体假阳性率
        # P = 1 - ∏(1 - p_i)
        estimated_fp = 1.0
        for s in filter_stats:
            estimated_fp *= (1 - s['estimated_fp_rate'])
        estimated_fp = 1 - estimated_fp
        
        return {
            'filter_count': len(self._filters),
            'total_elements': self._total_elements,
            'total_size_bits': total_size,
            'total_size_bytes': total_size // 8,
            'total_set_bits': total_set_bits,
            'overall_fill_ratio': total_set_bits / total_size if total_size > 0 else 0,
            'estimated_fp_rate': estimated_fp,
            'filters': filter_stats,
        }
    
    def to_bytes(self) -> bytes:
        """序列化为字节序列"""
        buffer = BytesIO()
        
        # 写入元数据
        buffer.write(struct.pack('!I', len(self._filters)))
        buffer.write(struct.pack('!I', self._initial_capacity))
        buffer.write(struct.pack('!d', self._base_fp_rate))
        buffer.write(struct.pack('!d', self._growth_factor))
        buffer.write(struct.pack('!d', self._fp_rate_factor))
        buffer.write(struct.pack('!I', len(self._hash_func)))
        buffer.write(self._hash_func.encode('utf-8'))
        buffer.write(struct.pack('!I', self._max_filters))
        buffer.write(struct.pack('!I', self._total_elements))
        
        # 写入各个过滤器
        for bf in self._filters:
            bf_bytes = bf.to_bytes()
            buffer.write(struct.pack('!I', len(bf_bytes)))
            buffer.write(bf_bytes)
        
        return buffer.getvalue()
    
    @classmethod
    def from_bytes(cls, data: bytes) -> 'ScalableBloomFilter':
        """从字节序列反序列化"""
        buffer = BytesIO(data)
        
        # 读取元数据
        filter_count = struct.unpack('!I', buffer.read(4))[0]
        initial_capacity = struct.unpack('!I', buffer.read(4))[0]
        base_fp_rate = struct.unpack('!d', buffer.read(8))[0]
        growth_factor = struct.unpack('!d', buffer.read(8))[0]
        fp_rate_factor = struct.unpack('!d', buffer.read(8))[0]
        hash_func_len = struct.unpack('!I', buffer.read(4))[0]
        hash_func = buffer.read(hash_func_len).decode('utf-8')
        max_filters = struct.unpack('!I', buffer.read(4))[0]
        total_elements = struct.unpack('!I', buffer.read(4))[0]
        
        # 创建实例
        sbf = cls(
            initial_capacity=initial_capacity,
            false_positive_rate=base_fp_rate,
            growth_factor=growth_factor,
            fp_rate_factor=fp_rate_factor,
            hash_func=hash_func,
            max_filters=max_filters,
        )
        
        # 读取过滤器
        sbf._filters.clear()
        for _ in range(filter_count):
            bf_len = struct.unpack('!I', buffer.read(4))[0]
            bf_bytes = buffer.read(bf_len)
            sbf._filters.append(BloomFilter.from_bytes(bf_bytes))
        
        sbf._total_elements = total_elements
        return sbf
    
    def save(self, file: Union[str, BinaryIO]) -> None:
        """保存到文件"""
        if isinstance(file, str):
            with open(file, 'wb') as f:
                f.write(self.to_bytes())
        else:
            file.write(self.to_bytes())
    
    @classmethod
    def load(cls, file: Union[str, BinaryIO]) -> 'ScalableBloomFilter':
        """从文件加载"""
        if isinstance(file, str):
            with open(file, 'rb') as f:
                data = f.read()
        else:
            data = file.read()
        return cls.from_bytes(data)
    
    def __repr__(self) -> str:
        stats = self.get_stats()
        return (
            f"ScalableBloomFilter(filters={len(self._filters)}, "
            f"elements={self._total_elements}, fp_rate={stats['estimated_fp_rate']:.6f})"
        )


# ============================================================================
# 计数布隆过滤器
# ============================================================================

class CountingBloomFilter:
    """
    计数布隆过滤器
    
    使用计数器代替单个位，支持删除操作。
    每个位置使用 4 位计数器（0-15）。
    
    使用示例：
        >>> cbf = CountingBloomFilter(expected_elements=1000, false_positive_rate=0.01)
        >>> cbf.add("hello")
        >>> cbf.add("hello")  # 添加相同元素多次
        >>> "hello" in cbf
        True
        >>> cbf.remove("hello")
        >>> "hello" in cbf  # 还有一次添加
        True
        >>> cbf.remove("hello")
        >>> "hello" in cbf
        False
    """
    
    def __init__(
        self,
        expected_elements: int = 10000,
        false_positive_rate: float = 0.01,
        hash_func: str = 'murmur',
        counter_bits: int = 4,
    ):
        """
        初始化计数布隆过滤器
        
        Args:
            expected_elements: 预期元素数量
            false_positive_rate: 期望的假阳性率
            hash_func: 哈希函数
            counter_bits: 每个计数器的位数（默认 4 位，范围 0-15）
        """
        if counter_bits not in (4, 8, 16):
            raise ValueError("counter_bits must be 4, 8, or 16")
        
        size, hash_count = optimal_size(expected_elements, false_positive_rate)
        
        self._size = size
        self._hash_count = hash_count
        self._hash_func_name = hash_func
        self._hash_func = HASH_FUNCTIONS[hash_func]
        self._counter_bits = counter_bits
        self._max_count = (1 << counter_bits) - 1
        
        # 使用数组存储计数器
        self._counters = [0] * size
        self._elements_added = 0
    
    def _get_hash_indices(self, item: Any) -> Iterator[int]:
        """获取项目的所有哈希索引"""
        if isinstance(item, bytes):
            data = item
        elif isinstance(item, str):
            data = item.encode('utf-8')
        else:
            data = str(item).encode('utf-8')
        
        h1 = self._hash_func(data, 0)
        h2 = self._hash_func(data, h1)
        
        for i in range(self._hash_count):
            index = (h1 + i * h2) % self._size
            yield index
    
    def add(self, item: Any) -> bool:
        """
        添加元素
        
        Args:
            item: 要添加的元素
            
        Returns:
            True 如果添加成功，False 如果计数器溢出
        """
        indices = list(self._get_hash_indices(item))
        
        # 检查是否会溢出
        for index in indices:
            if self._counters[index] >= self._max_count:
                return False
        
        # 增加计数器
        for index in indices:
            self._counters[index] += 1
        
        self._elements_added += 1
        return True
    
    def remove(self, item: Any) -> bool:
        """
        删除元素
        
        Args:
            item: 要删除的元素
            
        Returns:
            True 如果删除成功，False 如果元素不存在
        """
        # 首先检查元素是否存在
        indices = list(self._get_hash_indices(item))
        
        if not all(self._counters[index] > 0 for index in indices):
            return False
        
        # 减少计数器
        for index in indices:
            self._counters[index] -= 1
        
        self._elements_added -= 1
        return True
    
    def __contains__(self, item: Any) -> bool:
        """检查元素是否可能存在"""
        return all(self._counters[index] > 0 for index in self._get_hash_indices(item))
    
    def might_contain(self, item: Any) -> bool:
        """检查元素是否可能存在"""
        return item in self
    
    def count(self, item: Any) -> int:
        """
        估计元素的出现次数
        
        Args:
            item: 要检查的元素
            
        Returns:
            估计的出现次数（最小计数器值）
        """
        indices = list(self._get_hash_indices(item))
        return min(self._counters[index] for index in indices)
    
    def __len__(self) -> int:
        """返回已添加的元素数量"""
        return self._elements_added
    
    @property
    def size(self) -> int:
        """返回过滤器大小"""
        return self._size
    
    @property
    def hash_count(self) -> int:
        """返回哈希函数数量"""
        return self._hash_count
    
    @property
    def is_empty(self) -> bool:
        """检查是否为空"""
        return self._elements_added == 0
    
    def clear(self) -> None:
        """清除所有元素"""
        self._counters = [0] * self._size
        self._elements_added = 0
    
    def get_stats(self) -> Dict[str, Any]:
        """获取统计信息"""
        non_zero = sum(1 for c in self._counters if c > 0)
        total_count = sum(self._counters)
        fill_ratio = non_zero / self._size if self._size > 0 else 0
        estimated_fp = false_positive_rate(self._elements_added, self._size, self._hash_count)
        
        return {
            'size': self._size,
            'hash_count': self._hash_count,
            'elements_added': self._elements_added,
            'non_zero_counters': non_zero,
            'total_count': total_count,
            'fill_ratio': fill_ratio,
            'counter_bits': self._counter_bits,
            'max_count': self._max_count,
            'estimated_fp_rate': estimated_fp,
        }
    
    def to_bytes(self) -> bytes:
        """序列化为字节序列"""
        header = struct.pack(
            '!IIIIII',
            self._size,
            self._hash_count,
            int(self._elements_added),
            len(self._hash_func_name),
            self._counter_bits,
            self._max_count,
        )
        func_name_bytes = self._hash_func_name.encode('utf-8')
        
        # 将计数器序列化
        if self._counter_bits == 4:
            # 每 2 个计数器打包成 1 个字节
            counter_bytes = bytearray()
            for i in range(0, len(self._counters), 2):
                c1 = self._counters[i]
                c2 = self._counters[i + 1] if i + 1 < len(self._counters) else 0
                counter_bytes.append((c2 << 4) | c1)
        elif self._counter_bits == 8:
            counter_bytes = bytes(self._counters)
        else:  # 16 bits
            counter_bytes = b''.join(struct.pack('!H', c) for c in self._counters)
        
        return header + func_name_bytes + bytes(counter_bytes)
    
    @classmethod
    def from_bytes(cls, data: bytes) -> 'CountingBloomFilter':
        """从字节序列反序列化"""
        if len(data) < 24:
            raise ValueError("Data too short for counting bloom filter")
        
        size, hash_count, elements_added, name_len, counter_bits, max_count = struct.unpack(
            '!IIIIII', data[:24]
        )
        
        if len(data) < 24 + name_len:
            raise ValueError("Data truncated (hash function name)")
        
        hash_func_name = data[24:24 + name_len].decode('utf-8')
        counter_data = data[24 + name_len:]
        
        cbf = cls(
            expected_elements=1000,
            hash_func=hash_func_name,
            counter_bits=counter_bits,
        )
        cbf._size = size
        cbf._hash_count = hash_count
        cbf._elements_added = int(elements_added)
        cbf._max_count = max_count
        cbf._counters = [0] * size
        
        # 反序列化计数器
        if counter_bits == 4:
            for i, byte in enumerate(counter_data):
                cbf._counters[i * 2] = byte & 0x0F
                if i * 2 + 1 < size:
                    cbf._counters[i * 2 + 1] = (byte >> 4) & 0x0F
        elif counter_bits == 8:
            cbf._counters = list(counter_data[:size])
        else:  # 16 bits
            for i in range(size):
                offset = i * 2
                if offset + 2 <= len(counter_data):
                    cbf._counters[i] = struct.unpack('!H', counter_data[offset:offset + 2])[0]
        
        return cbf
    
    def save(self, file: Union[str, BinaryIO]) -> None:
        """保存到文件"""
        if isinstance(file, str):
            with open(file, 'wb') as f:
                f.write(self.to_bytes())
        else:
            file.write(self.to_bytes())
    
    @classmethod
    def load(cls, file: Union[str, BinaryIO]) -> 'CountingBloomFilter':
        """从文件加载"""
        if isinstance(file, str):
            with open(file, 'rb') as f:
                data = f.read()
        else:
            data = file.read()
        return cls.from_bytes(data)
    
    def __repr__(self) -> str:
        return (
            f"CountingBloomFilter(size={self._size}, hash_count={self._hash_count}, "
            f"elements={self._elements_added}, counter_bits={self._counter_bits})"
        )


# ============================================================================
# 布隆过滤器工具函数
# ============================================================================

def create_optimal_filter(
    expected_elements: int,
    false_positive_rate: float,
    hash_func: str = 'murmur'
) -> BloomFilter:
    """
    创建最优配置的布隆过滤器
    
    Args:
        expected_elements: 预期元素数量
        false_positive_rate: 期望的假阳性率
        hash_func: 哈希函数
        
    Returns:
        配置最优的布隆过滤器
    """
    return BloomFilter(
        expected_elements=expected_elements,
        false_positive_rate=false_positive_rate,
        hash_func=hash_func,
    )


def from_iterable(
    items: Union[List, Set, Tuple],
    false_positive_rate: float = 0.01,
    hash_func: str = 'murmur'
) -> BloomFilter:
    """
    从可迭代对象创建布隆过滤器
    
    Args:
        items: 元素集合
        false_positive_rate: 期望的假阳性率
        hash_func: 哈希函数
        
    Returns:
        包含所有元素的布隆过滤器
    """
    items_list = list(items)
    bf = BloomFilter(
        expected_elements=len(items_list),
        false_positive_rate=false_positive_rate,
        hash_func=hash_func,
    )
    for item in items_list:
        bf.add(item)
    return bf


def estimate_memory_usage(
    expected_elements: int,
    false_positive_rate: float
) -> Dict[str, Any]:
    """
    估算布隆过滤器的内存使用
    
    Args:
        expected_elements: 预期元素数量
        false_positive_rate: 期望的假阳性率
        
    Returns:
        内存使用估算信息
    """
    m, k = optimal_size(expected_elements, false_positive_rate)
    bytes_needed = (m + 7) // 8
    kb = bytes_needed / 1024
    mb = kb / 1024
    
    return {
        'expected_elements': expected_elements,
        'false_positive_rate': false_positive_rate,
        'bits_needed': m,
        'bytes_needed': bytes_needed,
        'kilobytes': round(kb, 2),
        'megabytes': round(mb, 4),
        'hash_functions': k,
        'bits_per_element': round(m / expected_elements, 2),
    }


def compare_hash_functions(
    items: List[Any],
    test_queries: List[Any],
    expected_elements: int,
    false_positive_rate: float = 0.01
) -> Dict[str, Dict[str, Any]]:
    """
    比较不同哈希函数的性能
    
    Args:
        items: 要添加的元素
        test_queries: 测试查询（包含一些不在集合中的元素）
        expected_elements: 预期元素数量
        false_positive_rate: 期望的假阳性率
        
    Returns:
        各哈希函数的性能比较结果
    """
    import time
    
    results = {}
    
    for hash_name in HASH_FUNCTIONS:
        bf = BloomFilter(
            expected_elements=expected_elements,
            false_positive_rate=false_positive_rate,
            hash_func=hash_name,
        )
        
        # 测试添加性能
        start = time.perf_counter()
        for item in items:
            bf.add(item)
        add_time = time.perf_counter() - start
        
        # 测试查询性能
        start = time.perf_counter()
        for query in test_queries:
            _ = query in bf
        query_time = time.perf_counter() - start
        
        # 计算假阳性
        false_positives = sum(1 for q in test_queries if q not in items and q in bf)
        actual_queries = len([q for q in test_queries if q not in items])
        actual_fp_rate = false_positives / actual_queries if actual_queries > 0 else 0
        
        results[hash_name] = {
            'add_time_ms': round(add_time * 1000, 3),
            'query_time_ms': round(query_time * 1000, 3),
            'avg_add_us': round(add_time * 1000000 / len(items), 3),
            'avg_query_us': round(query_time * 1000000 / len(test_queries), 3),
            'actual_fp_rate': round(actual_fp_rate, 6),
            'false_positives': false_positives,
        }
    
    return results


class BloomFilterBuilder:
    """
    布隆过滤器构建器（流畅 API）
    
    使用示例：
        >>> bf = (BloomFilterBuilder()
        ...     .expected_elements(1000)
        ...     .false_positive_rate(0.01)
        ...     .with_hash('murmur')
        ...     .build())
    """
    
    def __init__(self):
        self._expected_elements = 10000
        self._false_positive_rate = 0.01
        self._hash_func = 'murmur'
        self._items: List[Any] = []
    
    def expected_elements(self, n: int) -> 'BloomFilterBuilder':
        """设置预期元素数量"""
        self._expected_elements = n
        return self
    
    def false_positive_rate(self, rate: float) -> 'BloomFilterBuilder':
        """设置假阳性率"""
        self._false_positive_rate = rate
        return self
    
    def with_hash(self, name: str) -> 'BloomFilterBuilder':
        """设置哈希函数"""
        self._hash_func = name
        return self
    
    def with_items(self, items: Union[List, Set, Tuple]) -> 'BloomFilterBuilder':
        """设置初始元素"""
        self._items = list(items)
        if len(self._items) > self._expected_elements:
            self._expected_elements = len(self._items)
        return self
    
    def build(self) -> BloomFilter:
        """构建布隆过滤器"""
        bf = BloomFilter(
            expected_elements=self._expected_elements,
            false_positive_rate=self._false_positive_rate,
            hash_func=self._hash_func,
        )
        for item in self._items:
            bf.add(item)
        return bf


# 导出的公共接口
__all__ = [
    # 哈希函数
    'murmurhash3_x86_32',
    'fnv_hash_32',
    'djb2_hash',
    'sha256_hash',
    'HASH_FUNCTIONS',
    
    # 工具函数
    'optimal_size',
    'false_positive_rate',
    'BitArray',
    
    # 布隆过滤器类
    'BloomFilter',
    'BloomFilterStats',
    'ScalableBloomFilter',
    'ScalableBloomFilterConfig',
    'CountingBloomFilter',
    
    # 工具
    'create_optimal_filter',
    'from_iterable',
    'estimate_memory_usage',
    'compare_hash_functions',
    'BloomFilterBuilder',
]