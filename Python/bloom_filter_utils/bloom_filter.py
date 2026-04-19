"""
布隆过滤器工具集 (Bloom Filter Utilities)

布隆过滤器是一种空间效率极高的概率数据结构，用于判断元素是否"可能存在"于集合中。
特点：
- 空间效率极高：使用位数组存储
- 时间效率高：O(k) 时间复杂度，k为哈希函数数量
- 无假阴性：如果判断不存在，则一定不存在
- 有假阳性：判断存在时，可能实际不存在
- 不支持删除：标准布隆过滤器不支持删除元素

适用场景：
- 缓存穿透防护
- 垃圾邮件/黑名单过滤
- 爬虫URL去重
- 数据库查询优化
- 推荐系统去重

零外部依赖，纯 Python 标准库实现
"""

import math
import struct
from abc import ABC, abstractmethod
from dataclasses import dataclass
from functools import lru_cache
from typing import (
    Any,
    Callable,
    Dict,
    Iterator,
    List,
    Optional,
    Set,
    Tuple,
    Union,
)


def _mmh3_like_hash(data: bytes, seed: int = 0) -> int:
    """
    MurmurHash3 风格的哈希函数（纯 Python 实现）
    不依赖外部库，实现类似 MurmurHash3 的哈希效果
    """
    c1 = 0xcc9e2d51
    c2 = 0x1b873593
    
    h = seed
    length = len(data)
    
    # 处理 4 字节块
    nblocks = length // 4
    for i in range(nblocks):
        k = struct.unpack('<I', data[i*4:(i+1)*4])[0]
        k = (k * c1) & 0xFFFFFFFF
        k = ((k << 15) | (k >> 17)) & 0xFFFFFFFF  # ROTL32(k, 15)
        k = (k * c2) & 0xFFFFFFFF
        h ^= k
        h = ((h << 13) | (h >> 19)) & 0xFFFFFFFF  # ROTL32(h, 13)
        h = ((h * 5) + 0xe6546b64) & 0xFFFFFFFF
    
    # 处理剩余字节
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
        h ^= k1
    
    # 最终混合
    h ^= length
    h ^= (h >> 16)
    h = (h * 0x85ebca6b) & 0xFFFFFFFF
    h ^= (h >> 13)
    h = (h * 0xc2b2ae35) & 0xFFFFFFFF
    h ^= (h >> 16)
    
    return h


def _fnv1a_hash(data: bytes, seed: int = 0) -> int:
    """FNV-1a 哈希函数"""
    h = seed ^ 2166136261
    for byte in data:
        h ^= byte
        h = (h * 16777619) & 0xFFFFFFFF
    return h


@dataclass
class BloomFilterStats:
    """布隆过滤器统计信息"""
    capacity: int          # 设计容量
    error_rate: float      # 设计假阳性率
    size_bits: int         # 位数组大小
    num_hashes: int        # 哈希函数数量
    num_elements: int      # 已添加元素数量
    fill_ratio: float      # 填充率
    estimated_error_rate: float  # 估算当前假阳性率
    
    def __repr__(self) -> str:
        return (
            f"BloomFilterStats(\n"
            f"  capacity={self.capacity},\n"
            f"  error_rate={self.error_rate:.4%},\n"
            f"  size_bits={self.size_bits} ({self.size_bits / 8 / 1024:.2f} KB),\n"
            f"  num_hashes={self.num_hashes},\n"
            f"  num_elements={self.num_elements},\n"
            f"  fill_ratio={self.fill_ratio:.2%},\n"
            f"  estimated_error_rate={self.estimated_error_rate:.4%}\n"
            f")"
        )


def optimal_num_bits(n: int, p: float) -> int:
    """
    计算最优位数组大小
    
    Args:
        n: 预期元素数量
        p: 期望假阳性率
        
    Returns:
        最优位数组大小
        
    公式: m = -n * ln(p) / (ln(2)^2)
    """
    if n <= 0:
        return 1
    if p <= 0:
        p = 1e-10
    if p >= 1:
        return 1
    m = -n * math.log(p) / (math.log(2) ** 2)
    return int(math.ceil(m))


def optimal_num_hashes(m: int, n: int) -> int:
    """
    计算最优哈希函数数量
    
    Args:
        m: 位数组大小
        n: 预期元素数量
        
    Returns:
        最优哈希函数数量
        
    公式: k = (m / n) * ln(2)
    """
    if n <= 0 or m <= 0:
        return 1
    k = (m / n) * math.log(2)
    return max(1, int(round(k)))


def estimate_false_positive_rate(m: int, n: int, k: int) -> float:
    """
    估算假阳性率
    
    Args:
        m: 位数组大小
        n: 已添加元素数量
        k: 哈希函数数量
        
    Returns:
        估算的假阳性率
        
    公式: p ≈ (1 - e^(-kn/m))^k
    """
    if m <= 0 or k <= 0:
        return 1.0
    if n <= 0:
        return 0.0
    
    # 避免数值溢出
    exponent = -k * n / m
    if exponent < -700:
        return 0.0
    
    p = (1 - math.exp(exponent)) ** k
    return min(1.0, max(0.0, p))


class BloomFilter:
    """
    标准布隆过滤器
    
    高效的概率数据结构，用于判断元素是否"可能存在"于集合中。
    
    Examples:
        >>> bf = BloomFilter(capacity=10000, error_rate=0.01)
        >>> bf.add("hello")
        >>> bf.add("world")
        >>> "hello" in bf
        True
        >>> "foo" in bf
        False
    """
    
    def __init__(
        self,
        capacity: int,
        error_rate: float = 0.01,
        num_hashes: Optional[int] = None,
        size_bits: Optional[int] = None,
    ):
        """
        初始化布隆过滤器
        
        Args:
            capacity: 预期元素数量
            error_rate: 期望假阳性率（默认 1%）
            num_hashes: 哈希函数数量（自动计算最优值）
            size_bits: 位数组大小（自动计算最优值）
        """
        if capacity <= 0:
            raise ValueError("capacity must be positive")
        if error_rate <= 0 or error_rate >= 1:
            raise ValueError("error_rate must be between 0 and 1 (exclusive)")
        
        self._capacity = capacity
        self._error_rate = error_rate
        
        # 计算最优参数
        self._size_bits = size_bits or optimal_num_bits(capacity, error_rate)
        self._num_hashes = num_hashes or optimal_num_hashes(self._size_bits, capacity)
        
        # 初始化位数组（使用 bytearray 存储位）
        self._bit_array = bytearray((self._size_bits + 7) // 8)
        self._count = 0
    
    def _set_bit(self, index: int) -> bool:
        """设置位，返回是否是新设置的"""
        byte_index = index // 8
        bit_offset = index % 8
        mask = 1 << bit_offset
        
        was_set = bool(self._bit_array[byte_index] & mask)
        self._bit_array[byte_index] |= mask
        return not was_set
    
    def _get_bit(self, index: int) -> bool:
        """获取位状态"""
        byte_index = index // 8
        bit_offset = index % 8
        mask = 1 << bit_offset
        return bool(self._bit_array[byte_index] & mask)
    
    def _hashes(self, item: Any) -> Iterator[int]:
        """
        生成 k 个哈希值
        使用双哈希技术：h(i) = h1 + i * h2
        """
        # 序列化元素
        if isinstance(item, bytes):
            data = item
        elif isinstance(item, str):
            data = item.encode('utf-8')
        else:
            data = str(item).encode('utf-8')
        
        # 使用两个不同的哈希函数
        h1 = _mmh3_like_hash(data, 0)
        h2 = _fnv1a_hash(data, h1)
        
        # 生成 k 个哈希值
        for i in range(self._num_hashes):
            # 双哈希技术
            combined = (h1 + i * h2) % self._size_bits
            if combined < 0:
                combined += self._size_bits
            yield combined
    
    def add(self, item: Any) -> None:
        """
        添加元素到布隆过滤器
        
        Args:
            item: 要添加的元素
        """
        for index in self._hashes(item):
            self._set_bit(index)
        self._count += 1
    
    def __contains__(self, item: Any) -> bool:
        """
        检查元素是否可能在集合中
        
        Args:
            item: 要检查的元素
            
        Returns:
            True 如果元素可能在集合中（可能有假阳性）
            False 如果元素一定不在集合中（无假阴性）
        """
        return all(self._get_bit(index) for index in self._hashes(item))
    
    def contains(self, item: Any) -> bool:
        """检查元素是否可能在集合中"""
        return item in self
    
    def might_contain(self, item: Any) -> bool:
        """检查元素是否可能在集合中（语义更清晰的别名）"""
        return item in self
    
    def __len__(self) -> int:
        """返回已添加元素数量"""
        return self._count
    
    def __repr__(self) -> str:
        return (
            f"BloomFilter(capacity={self._capacity}, "
            f"error_rate={self._error_rate}, "
            f"size_bits={self._size_bits}, "
            f"num_hashes={self._num_hashes}, "
            f"count={self._count})"
        )
    
    @property
    def capacity(self) -> int:
        """设计容量"""
        return self._capacity
    
    @property
    def error_rate(self) -> float:
        """设计假阳性率"""
        return self._error_rate
    
    @property
    def size_bits(self) -> int:
        """位数组大小"""
        return self._size_bits
    
    @property
    def num_hashes(self) -> int:
        """哈希函数数量"""
        return self._num_hashes
    
    @property
    def is_empty(self) -> bool:
        """是否为空"""
        return self._count == 0
    
    @property
    def fill_ratio(self) -> float:
        """填充率"""
        if self._size_bits == 0:
            return 0.0
        # 统计设置位数
        set_bits = sum(bin(byte).count('1') for byte in self._bit_array)
        return set_bits / self._size_bits
    
    def estimated_error_rate(self) -> float:
        """估算当前假阳性率"""
        return estimate_false_positive_rate(
            self._size_bits, self._count, self._num_hashes
        )
    
    def stats(self) -> BloomFilterStats:
        """获取统计信息"""
        return BloomFilterStats(
            capacity=self._capacity,
            error_rate=self._error_rate,
            size_bits=self._size_bits,
            num_hashes=self._num_hashes,
            num_elements=self._count,
            fill_ratio=self.fill_ratio,
            estimated_error_rate=self.estimated_error_rate(),
        )
    
    def clear(self) -> None:
        """清空布隆过滤器"""
        self._bit_array = bytearray((self._size_bits + 7) // 8)
        self._count = 0
    
    def union(self, other: 'BloomFilter') -> 'BloomFilter':
        """
        计算两个布隆过滤器的并集
        
        Args:
            other: 另一个布隆过滤器
            
        Returns:
            新的布隆过滤器，包含两个集合的并集
            
        Note:
            两个布隆过滤器必须具有相同的参数
        """
        if self._size_bits != other._size_bits:
            raise ValueError("Bloom filters must have the same size")
        if self._num_hashes != other._num_hashes:
            raise ValueError("Bloom filters must have the same number of hashes")
        
        result = BloomFilter(
            capacity=max(self._capacity, other._capacity),
            error_rate=min(self._error_rate, other._error_rate),
            num_hashes=self._num_hashes,
            size_bits=self._size_bits,
        )
        
        # 按位或合并
        for i in range(len(self._bit_array)):
            result._bit_array[i] = self._bit_array[i] | other._bit_array[i]
        
        # 估算元素数量（近似）
        result._count = max(self._count, other._count)
        
        return result
    
    def intersect_approx(self, other: 'BloomFilter') -> 'BloomFilter':
        """
        近似计算两个布隆过滤器的交集
        
        Args:
            other: 另一个布隆过滤器
            
        Returns:
            新的布隆过滤器，近似包含两个集合的交集
            
        Note:
            这是一个近似操作，结果可能不准确
        """
        if self._size_bits != other._size_bits:
            raise ValueError("Bloom filters must have the same size")
        if self._num_hashes != other._num_hashes:
            raise ValueError("Bloom filters must have the same number of hashes")
        
        result = BloomFilter(
            capacity=min(self._capacity, other._capacity),
            error_rate=max(self._error_rate, other._error_rate),
            num_hashes=self._num_hashes,
            size_bits=self._size_bits,
        )
        
        # 按位与合并
        for i in range(len(self._bit_array)):
            result._bit_array[i] = self._bit_array[i] & other._bit_array[i]
        
        # 估算元素数量（非常近似）
        result._count = min(self._count, other._count) // 2
        
        return result
    
    def to_bytes(self) -> bytes:
        """
        序列化布隆过滤器为字节数据
        
        Returns:
            字节表示
        """
        # 格式: capacity(4) + error_rate(8) + num_hashes(4) + size_bits(4) + count(4) + bit_array
        # Total header size: 24 bytes
        header = struct.pack(
            '<I d I I I',
            self._capacity,
            self._error_rate,
            self._num_hashes,
            self._size_bits,
            self._count,
        )
        return header + bytes(self._bit_array)
    
    @classmethod
    def from_bytes(cls, data: bytes) -> 'BloomFilter':
        """
        从字节数据反序列化布隆过滤器
        
        Args:
            data: 字节表示
            
        Returns:
            布隆过滤器实例
        """
        HEADER_SIZE = 24  # capacity(4) + error_rate(8) + num_hashes(4) + size_bits(4) + count(4)
        if len(data) < HEADER_SIZE:
            raise ValueError("Invalid bloom filter data")
        
        capacity, error_rate, num_hashes, size_bits, count = struct.unpack(
            '<I d I I I', data[:HEADER_SIZE]
        )
        
        bf = cls(
            capacity=capacity,
            error_rate=error_rate,
            num_hashes=num_hashes,
            size_bits=size_bits,
        )
        
        bf._bit_array = bytearray(data[HEADER_SIZE:])
        bf._count = count
        
        return bf
    
    def copy(self) -> 'BloomFilter':
        """创建布隆过滤器的副本"""
        bf = BloomFilter(
            capacity=self._capacity,
            error_rate=self._error_rate,
            num_hashes=self._num_hashes,
            size_bits=self._size_bits,
        )
        bf._bit_array = self._bit_array.copy()
        bf._count = self._count
        return bf
    
    def update(self, items: Union[List[Any], Set[Any], Tuple[Any, ...]]) -> None:
        """
        批量添加元素
        
        Args:
            items: 要添加的元素集合
        """
        for item in items:
            self.add(item)


class CountingBloomFilter:
    """
    计数布隆过滤器
    
    支持删除操作的布隆过滤器。使用计数器代替位数组。
    每个"位"使用一个计数器，删除时减 1。
    
    Examples:
        >>> cbf = CountingBloomFilter(capacity=10000, error_rate=0.01)
        >>> cbf.add("hello")
        >>> "hello" in cbf
        True
        >>> cbf.remove("hello")
        >>> "hello" in cbf
        False
    """
    
    def __init__(
        self,
        capacity: int,
        error_rate: float = 0.01,
        num_hashes: Optional[int] = None,
        size_bits: Optional[int] = None,
        counter_bits: int = 4,
    ):
        """
        初始化计数布隆过滤器
        
        Args:
            capacity: 预期元素数量
            error_rate: 期望假阳性率
            num_hashes: 哈希函数数量
            size_bits: 计数器数量
            counter_bits: 每个计数器的位数（默认 4 位，最大值 15）
        """
        if capacity <= 0:
            raise ValueError("capacity must be positive")
        if error_rate <= 0 or error_rate >= 1:
            raise ValueError("error_rate must be between 0 and 1 (exclusive)")
        
        self._capacity = capacity
        self._error_rate = error_rate
        self._counter_bits = counter_bits
        self._max_count = (1 << counter_bits) - 1
        
        # 计算最优参数
        self._size_bits = size_bits or optimal_num_bits(capacity, error_rate)
        self._num_hashes = num_hashes or optimal_num_hashes(self._size_bits, capacity)
        
        # 使用列表存储计数器
        self._counters = [0] * self._size_bits
        self._count = 0
    
    def _hashes(self, item: Any) -> Iterator[int]:
        """生成哈希值"""
        if isinstance(item, bytes):
            data = item
        elif isinstance(item, str):
            data = item.encode('utf-8')
        else:
            data = str(item).encode('utf-8')
        
        h1 = _mmh3_like_hash(data, 0)
        h2 = _fnv1a_hash(data, h1)
        
        for i in range(self._num_hashes):
            combined = (h1 + i * h2) % self._size_bits
            if combined < 0:
                combined += self._size_bits
            yield combined
    
    def add(self, item: Any) -> bool:
        """
        添加元素
        
        Args:
            item: 要添加的元素
            
        Returns:
            True 如果成功添加，False 如果计数器溢出
        """
        success = True
        indices = list(self._hashes(item))
        
        # 检查是否会溢出
        for index in indices:
            if self._counters[index] >= self._max_count:
                success = False
                break
        
        if not success:
            return False
        
        # 增加计数器
        for index in indices:
            self._counters[index] += 1
        
        self._count += 1
        return True
    
    def remove(self, item: Any) -> bool:
        """
        删除元素
        
        Args:
            item: 要删除的元素
            
        Returns:
            True 如果成功删除，False 如果元素不在集合中
        """
        indices = list(self._hashes(item))
        
        # 检查元素是否存在
        if not all(self._counters[index] > 0 for index in indices):
            return False
        
        # 减少计数器
        for index in indices:
            self._counters[index] -= 1
        
        self._count -= 1
        return True
    
    def __contains__(self, item: Any) -> bool:
        """检查元素是否可能在集合中"""
        return all(self._counters[index] > 0 for index in self._hashes(item))
    
    def contains(self, item: Any) -> bool:
        """检查元素是否可能在集合中"""
        return item in self
    
    def __len__(self) -> int:
        """返回已添加元素数量"""
        return self._count
    
    def clear(self) -> None:
        """清空计数布隆过滤器"""
        self._counters = [0] * self._size_bits
        self._count = 0
    
    def stats(self) -> BloomFilterStats:
        """获取统计信息"""
        fill_ratio = sum(1 for c in self._counters if c > 0) / self._size_bits
        
        return BloomFilterStats(
            capacity=self._capacity,
            error_rate=self._error_rate,
            size_bits=self._size_bits,
            num_hashes=self._num_hashes,
            num_elements=self._count,
            fill_ratio=fill_ratio,
            estimated_error_rate=estimate_false_positive_rate(
                self._size_bits, self._count, self._num_hashes
            ),
        )
    
    def __repr__(self) -> str:
        return (
            f"CountingBloomFilter(capacity={self._capacity}, "
            f"error_rate={self._error_rate}, "
            f"count={self._count})"
        )


class ScalableBloomFilter:
    """
    可扩展布隆过滤器
    
    当元素数量超过当前容量时自动扩容，添加新的布隆过滤器。
    可以无限添加元素而不会显著增加假阳性率。
    
    Examples:
        >>> sbf = ScalableBloomFilter(initial_capacity=1000, error_rate=0.01)
        >>> for i in range(100000):
        ...     sbf.add(f"item_{i}")
        >>> "item_50000" in sbf
        True
    """
    
    def __init__(
        self,
        initial_capacity: int = 1000,
        error_rate: float = 0.01,
        growth_factor: float = 2.0,
        error_tightening: float = 0.5,
    ):
        """
        初始化可扩展布隆过滤器
        
        Args:
            initial_capacity: 初始容量
            error_rate: 初始假阳性率
            growth_factor: 每次扩容的增长因子
            error_tightening: 每次扩容时假阳性率的收紧因子
        """
        if initial_capacity <= 0:
            raise ValueError("initial_capacity must be positive")
        if error_rate <= 0 or error_rate >= 1:
            raise ValueError("error_rate must be between 0 and 1 (exclusive)")
        
        self._initial_capacity = initial_capacity
        self._initial_error_rate = error_rate
        self._growth_factor = growth_factor
        self._error_tightening = error_tightening
        
        self._filters: List[BloomFilter] = []
        self._count = 0
        
        # 下一个过滤器的参数
        self._next_capacity = initial_capacity
        self._next_error_rate = error_rate
        
        # 添加第一个过滤器
        self._add_filter()
    
    def _add_filter(self) -> None:
        """添加一个新的布隆过滤器"""
        bf = BloomFilter(
            capacity=self._next_capacity,
            error_rate=self._next_error_rate,
        )
        self._filters.append(bf)
        
        # 更新下一个过滤器的参数
        self._next_capacity = int(self._next_capacity * self._growth_factor)
        self._next_error_rate *= self._error_tightening
    
    def add(self, item: Any) -> None:
        """
        添加元素
        
        Args:
            item: 要添加的元素
            
        Note:
            不进行存在性检查，因为布隆过滤器的假阳性可能导致
            新元素被误判为已存在而跳过。
        """
        # 添加到最后一个过滤器
        current_filter = self._filters[-1]
        current_filter.add(item)
        self._count += 1
        
        # 检查是否需要扩容（当前过滤器达到其容量）
        if len(current_filter) >= current_filter.capacity:
            self._add_filter()
    
    def __contains__(self, item: Any) -> bool:
        """检查元素是否可能在集合中"""
        return any(item in bf for bf in self._filters)
    
    def contains(self, item: Any) -> bool:
        """检查元素是否可能在集合中"""
        return item in self
    
    def __len__(self) -> int:
        """返回已添加元素数量"""
        return self._count
    
    @property
    def num_filters(self) -> int:
        """布隆过滤器数量"""
        return len(self._filters)
    
    @property
    def total_bits(self) -> int:
        """总位数"""
        return sum(bf.size_bits for bf in self._filters)
    
    def estimated_error_rate(self) -> float:
        """估算当前假阳性率"""
        # 整体假阳性率是各层假阳性率的并集
        # P_total = 1 - prod(1 - P_i)
        p_total = 0.0
        for bf in self._filters:
            p_i = bf.estimated_error_rate()
            p_total = p_total + p_i - p_total * p_i
        return p_total
    
    def clear(self) -> None:
        """清空布隆过滤器"""
        self._filters = []
        self._count = 0
        self._next_capacity = self._initial_capacity
        self._next_error_rate = self._initial_error_rate
        self._add_filter()
    
    def __repr__(self) -> str:
        return (
            f"ScalableBloomFilter("
            f"num_filters={len(self._filters)}, "
            f"count={self._count}, "
            f"estimated_error_rate={self.estimated_error_rate():.4%})"
        )


class DeletableBloomFilter:
    """
    可删除布隆过滤器（d-left Counting Bloom Filter 简化版）
    
    通过存储元素指纹来支持删除操作。
    空间效率低于标准布隆过滤器，但支持精确删除。
    
    Examples:
        >>> dbf = DeletableBloomFilter(capacity=1000, error_rate=0.01)
        >>> dbf.add("hello")
        >>> "hello" in dbf
        True
        >>> dbf.remove("hello")
        >>> "hello" in dbf
        False
    """
    
    def __init__(
        self,
        capacity: int,
        error_rate: float = 0.01,
        fingerprint_bits: int = 8,
    ):
        """
        初始化可删除布隆过滤器
        
        Args:
            capacity: 预期元素数量
            error_rate: 期望假阳性率
            fingerprint_bits: 指纹位数（默认 8 位）
        """
        if capacity <= 0:
            raise ValueError("capacity must be positive")
        
        self._capacity = capacity
        self._error_rate = error_rate
        self._fingerprint_bits = fingerprint_bits
        self._fingerprint_mask = (1 << fingerprint_bits) - 1
        
        # 计算参数
        self._size_bits = optimal_num_bits(capacity, error_rate)
        self._num_hashes = optimal_num_hashes(self._size_bits, capacity)
        
        # 存储指纹（使用字典模拟）
        self._fingerprints: Dict[int, Set[int]] = {}
        self._count = 0
    
    def _get_fingerprint(self, item: Any) -> int:
        """计算元素指纹"""
        if isinstance(item, bytes):
            data = item
        elif isinstance(item, str):
            data = item.encode('utf-8')
        else:
            data = str(item).encode('utf-8')
        
        return _mmh3_like_hash(data, 0xDEADBEEF) & self._fingerprint_mask
    
    def _hashes(self, item: Any) -> Iterator[int]:
        """生成哈希值"""
        if isinstance(item, bytes):
            data = item
        elif isinstance(item, str):
            data = item.encode('utf-8')
        else:
            data = str(item).encode('utf-8')
        
        h1 = _mmh3_like_hash(data, 0)
        h2 = _fnv1a_hash(data, h1)
        
        for i in range(self._num_hashes):
            combined = (h1 + i * h2) % self._size_bits
            if combined < 0:
                combined += self._size_bits
            yield combined
    
    def add(self, item: Any) -> None:
        """添加元素"""
        fingerprint = self._get_fingerprint(item)
        
        for index in self._hashes(item):
            if index not in self._fingerprints:
                self._fingerprints[index] = set()
            self._fingerprints[index].add(fingerprint)
        
        self._count += 1
    
    def remove(self, item: Any) -> bool:
        """
        删除元素
        
        Returns:
            True 如果成功删除，False 如果元素不存在
        """
        fingerprint = self._get_fingerprint(item)
        indices = list(self._hashes(item))
        
        # 检查元素是否存在
        if not all(
            index in self._fingerprints and fingerprint in self._fingerprints[index]
            for index in indices
        ):
            return False
        
        # 删除指纹
        for index in indices:
            self._fingerprints[index].discard(fingerprint)
            if not self._fingerprints[index]:
                del self._fingerprints[index]
        
        self._count -= 1
        return True
    
    def __contains__(self, item: Any) -> bool:
        """检查元素是否可能在集合中"""
        fingerprint = self._get_fingerprint(item)
        return all(
            index in self._fingerprints and fingerprint in self._fingerprints[index]
            for index in self._hashes(item)
        )
    
    def contains(self, item: Any) -> bool:
        """检查元素是否可能在集合中"""
        return item in self
    
    def __len__(self) -> int:
        """返回已添加元素数量"""
        return self._count
    
    def clear(self) -> None:
        """清空"""
        self._fingerprints.clear()
        self._count = 0
    
    def __repr__(self) -> str:
        return (
            f"DeletableBloomFilter(capacity={self._capacity}, "
            f"count={self._count})"
        )


class BloomFilterBuilder:
    """
    布隆过滤器构建器
    
    提供流畅的 API 来创建和配置布隆过滤器。
    
    Examples:
        >>> bf = (BloomFilterBuilder()
        ...     .with_capacity(10000)
        ...     .with_error_rate(0.001)
        ...     .build())
        >>> bf.add("hello")
    """
    
    def __init__(self):
        self._capacity = 1000
        self._error_rate = 0.01
        self._num_hashes = None
        self._size_bits = None
        self._items: List[Any] = []
        self._type = 'standard'
    
    def with_capacity(self, capacity: int) -> 'BloomFilterBuilder':
        """设置容量"""
        self._capacity = capacity
        return self
    
    def with_error_rate(self, error_rate: float) -> 'BloomFilterBuilder':
        """设置假阳性率"""
        self._error_rate = error_rate
        return self
    
    def with_num_hashes(self, num_hashes: int) -> 'BloomFilterBuilder':
        """设置哈希函数数量"""
        self._num_hashes = num_hashes
        return self
    
    def with_size_bits(self, size_bits: int) -> 'BloomFilterBuilder':
        """设置位数组大小"""
        self._size_bits = size_bits
        return self
    
    def with_items(self, items: Union[List[Any], Set[Any], Tuple[Any, ...]]) -> 'BloomFilterBuilder':
        """设置初始元素"""
        self._items = list(items)
        return self
    
    def as_counting(self) -> 'BloomFilterBuilder':
        """设置为计数布隆过滤器"""
        self._type = 'counting'
        return self
    
    def as_scalable(self) -> 'BloomFilterBuilder':
        """设置为可扩展布隆过滤器"""
        self._type = 'scalable'
        return self
    
    def as_deletable(self) -> 'BloomFilterBuilder':
        """设置为可删除布隆过滤器"""
        self._type = 'deletable'
        return self
    
    def build(self) -> Union[BloomFilter, CountingBloomFilter, ScalableBloomFilter, DeletableBloomFilter]:
        """构建布隆过滤器"""
        if self._type == 'counting':
            bf = CountingBloomFilter(
                capacity=self._capacity,
                error_rate=self._error_rate,
                num_hashes=self._num_hashes,
                size_bits=self._size_bits,
            )
        elif self._type == 'scalable':
            bf = ScalableBloomFilter(
                initial_capacity=self._capacity,
                error_rate=self._error_rate,
            )
        elif self._type == 'deletable':
            bf = DeletableBloomFilter(
                capacity=self._capacity,
                error_rate=self._error_rate,
            )
        else:
            bf = BloomFilter(
                capacity=self._capacity,
                error_rate=self._error_rate,
                num_hashes=self._num_hashes,
                size_bits=self._size_bits,
            )
        
        # 添加初始元素
        for item in self._items:
            bf.add(item)
        
        return bf


# 便捷函数
def create_bloom_filter(
    capacity: int,
    error_rate: float = 0.01,
) -> BloomFilter:
    """
    创建布隆过滤器的便捷函数
    
    Args:
        capacity: 预期元素数量
        error_rate: 期望假阳性率
        
    Returns:
        布隆过滤器实例
    """
    return BloomFilter(capacity=capacity, error_rate=error_rate)


def create_optimal_bloom_filter(
    expected_items: int,
    acceptable_false_positives: int = 1,
) -> BloomFilter:
    """
    创建最优布隆过滤器（基于可接受的假阳性数量）
    
    Args:
        expected_items: 预期元素数量
        acceptable_false_positives: 可接受的假阳性数量
        
    Returns:
        最优配置的布隆过滤器
    """
    if expected_items <= 0:
        raise ValueError("expected_items must be positive")
    
    # 计算假阳性率
    error_rate = acceptable_false_positives / expected_items
    error_rate = min(0.5, max(1e-10, error_rate))
    
    return BloomFilter(capacity=expected_items, error_rate=error_rate)