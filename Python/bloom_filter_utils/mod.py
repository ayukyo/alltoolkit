"""
Bloom Filter Utils - 布隆过滤器工具集

零依赖实现的高效概率数据结构，用于快速判断元素是否在集合中。

特点：
- 空间效率极高：比传统集合节省 90%+ 内存
- 查询时间复杂度 O(k)，k 为哈希函数数量
- 可配置的误判率
- 支持序列化/反序列化
- 线程安全

使用场景：
- URL 去重（爬虫）
- 缓存穿透防护
- 垃圾邮件过滤
- 推荐系统内容去重
"""

import math
import struct
from typing import Optional, Union, List
from threading import Lock
import hashlib


class BloomFilter:
    """
    布隆过滤器实现
    
    一种空间高效的概率数据结构，用于测试元素是否为集合成员。
    可能产生假阳性（误判存在），但不会产生假阴性（不会漏判）。
    
    示例:
        >>> bf = BloomFilter(expected_items=10000, false_positive_rate=0.01)
        >>> bf.add("example.com")
        >>> "example.com" in bf
        True
        >>> "unknown.com" in bf
        False
    """
    
    def __init__(
        self,
        expected_items: int = 10000,
        false_positive_rate: float = 0.01,
        bit_size: Optional[int] = None,
        hash_count: Optional[int] = None
    ):
        """
        初始化布隆过滤器
        
        Args:
            expected_items: 预期存储的元素数量
            false_positive_rate: 可接受的误判率 (0-1)
            bit_size: 比特数组大小（可选，自动计算）
            hash_count: 哈希函数数量（可选，自动计算）
        """
        if expected_items <= 0:
            raise ValueError("expected_items must be positive")
        if not 0 < false_positive_rate < 1:
            raise ValueError("false_positive_rate must be between 0 and 1")
        
        self._n = expected_items
        self._p = false_positive_rate
        
        # 自动计算最优参数
        if bit_size is None:
            # m = -n * ln(p) / (ln(2))^2
            self._m = int(-expected_items * math.log(false_positive_rate) / (math.log(2) ** 2))
        else:
            self._m = bit_size
        
        if hash_count is None:
            # k = m / n * ln(2)
            self._k = max(1, int(self._m / expected_items * math.log(2)))
        else:
            self._k = hash_count
        
        # 初始化比特数组（使用整数数组提高效率）
        self._bits = [0] * ((self._m + 31) // 32)
        self._count = 0  # 设置的 bit 数量
        self._item_count = 0  # 添加的元素数量
        self._lock = Lock()
    
    def _hashes(self, item: Union[str, bytes]) -> List[int]:
        """
        生成 k 个哈希值
        
        使用双重哈希技术，通过两个基础哈希函数生成 k 个哈希值
        h(i) = h1 + i * h2
        """
        if isinstance(item, str):
            item = item.encode('utf-8')
        
        # 使用 MD5 和 SHA1 作为两个基础哈希函数
        h1 = int(hashlib.md5(item).hexdigest(), 16)
        h2 = int(hashlib.sha1(item).hexdigest(), 16)
        
        hashes = []
        for i in range(self._k):
            # 双重哈希组合
            h = (h1 + i * h2) % self._m
            hashes.append(h)
        return hashes
    
    def _set_bit(self, index: int) -> bool:
        """设置比特位，返回是否为新设置的位"""
        word_idx = index // 32
        bit_idx = index % 32
        mask = 1 << bit_idx
        
        old_value = self._bits[word_idx]
        self._bits[word_idx] |= mask
        return (old_value & mask) == 0
    
    def _get_bit(self, index: int) -> bool:
        """获取比特位状态"""
        word_idx = index // 32
        bit_idx = index % 32
        return bool(self._bits[word_idx] & (1 << bit_idx))
    
    def add(self, item: Union[str, bytes]) -> None:
        """
        向布隆过滤器添加元素
        
        Args:
            item: 要添加的元素（字符串或字节）
        """
        with self._lock:
            for h in self._hashes(item):
                self._set_bit(h)
            self._item_count += 1
    
    def __contains__(self, item: Union[str, bytes]) -> bool:
        """
        检查元素是否可能在集合中
        
        Args:
            item: 要检查的元素
            
        Returns:
            True: 元素可能在集合中（可能有误判）
            False: 元素一定不在集合中
        """
        for h in self._hashes(item):
            if not self._get_bit(h):
                return False
        return True
    
    def __len__(self) -> int:
        """返回已添加元素的数量"""
        return self._item_count
    
    def __repr__(self) -> str:
        return (
            f"BloomFilter(items={self._item_count}, "
            f"capacity={self._n}, "
            f"bits={self._m}, "
            f"hashes={self._k}, "
            f"fp_rate={self._p:.4f})"
        )
    
    @property
    def bit_size(self) -> int:
        """比特数组大小"""
        return self._m
    
    @property
    def hash_count(self) -> int:
        """哈希函数数量"""
        return self._k
    
    @property
    def estimated_false_positive_rate(self) -> float:
        """估算当前误判率"""
        if self._count == 0:
            return 0.0
        # p = (1 - e^(-kn/m))^k
        ratio = self._k * self._count / self._m
        return (1 - math.exp(-ratio)) ** self._k
    
    @property
    def load_factor(self) -> float:
        """负载因子（已设置比特位比例）"""
        total_bits = sum(bin(word).count('1') for word in self._bits)
        return total_bits / self._m
    
    def clear(self) -> None:
        """清空布隆过滤器"""
        with self._lock:
            self._bits = [0] * ((self._m + 31) // 32)
            self._count = 0
            self._item_count = 0
    
    def serialize(self) -> bytes:
        """
        序列化布隆过滤器为字节
        
        格式: [n(4)] [p(8)] [m(4)] [k(4)] [item_count(4)] [bits...]
        """
        with self._lock:
            header = struct.pack(
                '>IfIII',
                self._n,          # expected items
                self._p,          # false positive rate
                self._m,          # bit size
                self._k,          # hash count
                self._item_count  # actual item count
            )
            bits_data = struct.pack(f'>{len(self._bits)}I', *self._bits)
            return header + bits_data
    
    @classmethod
    def deserialize(cls, data: bytes) -> 'BloomFilter':
        """从字节反序列化布隆过滤器"""
        header_size = struct.calcsize('>IfIII')
        n, p, m, k, item_count = struct.unpack('>IfIII', data[:header_size])
        
        bf = cls(expected_items=n, false_positive_rate=p, bit_size=m, hash_count=k)
        bf._item_count = item_count
        
        bits_count = (m + 31) // 32
        bf._bits = list(struct.unpack(f'>{bits_count}I', data[header_size:header_size + bits_count * 4]))
        
        return bf
    
    def union(self, other: 'BloomFilter') -> 'BloomFilter':
        """
        合并两个布隆过滤器
        
        Args:
            other: 另一个布隆过滤器
            
        Returns:
            新的布隆过滤器，包含两个过滤器的并集
            
        Raises:
            ValueError: 如果两个过滤器参数不兼容
        """
        if self._m != other._m or self._k != other._k:
            raise ValueError("Cannot union bloom filters with different sizes or hash counts")
        
        result = BloomFilter(
            expected_items=self._n,
            false_positive_rate=self._p,
            bit_size=self._m,
            hash_count=self._k
        )
        
        for i in range(len(self._bits)):
            result._bits[i] = self._bits[i] | other._bits[i]
        
        result._item_count = min(self._item_count + other._item_count, self._n)
        return result
    
    def intersection(self, other: 'BloomFilter') -> 'BloomFilter':
        """
        计算两个布隆过滤器的交集
        
        Args:
            other: 另一个布隆过滤器
            
        Returns:
            新的布隆过滤器，包含两个过滤器的交集
        """
        if self._m != other._m or self._k != other._k:
            raise ValueError("Cannot intersect bloom filters with different sizes or hash counts")
        
        result = BloomFilter(
            expected_items=self._n,
            false_positive_rate=self._p,
            bit_size=self._m,
            hash_count=self._k
        )
        
        for i in range(len(self._bits)):
            result._bits[i] = self._bits[i] & other._bits[i]
        
        # 交集的计数是估计值
        result._item_count = min(self._item_count, other._item_count)
        return result


class ScalableBloomFilter:
    """
    可扩展布隆过滤器
    
    当元素数量超过预期时自动扩展容量，
    同时保持较低的误判率。
    
    示例:
        >>> sbf = ScalableBloomFilter(initial_capacity=1000)
        >>> for i in range(10000):
        ...     sbf.add(f"item_{i}")
        >>> "item_5000" in sbf
        True
    """
    
    def __init__(
        self,
        initial_capacity: int = 1000,
        false_positive_rate: float = 0.01,
        growth_factor: int = 2
    ):
        """
        初始化可扩展布隆过滤器
        
        Args:
            initial_capacity: 初始容量
            false_positive_rate: 目标误判率
            growth_factor: 扩展因子
        """
        self._filters: List[BloomFilter] = []
        self._initial_capacity = initial_capacity
        self._fp_rate = false_positive_rate
        self._growth_factor = growth_factor
        self._lock = Lock()
        self._total_count = 0
        
        self._add_filter()
    
    def _add_filter(self) -> None:
        """添加新的布隆过滤器层"""
        # 每层的误判率递减，确保总体误判率不变
        layer = len(self._filters)
        capacity = self._initial_capacity * (self._growth_factor ** layer)
        fp_rate = self._fp_rate / (self._growth_factor ** layer)
        
        self._filters.append(BloomFilter(
            expected_items=capacity,
            false_positive_rate=fp_rate
        ))
    
    def add(self, item: Union[str, bytes]) -> None:
        """添加元素"""
        with self._lock:
            # 检查是否已存在
            for bf in self._filters:
                if item in bf:
                    return
            
            # 添加到当前活跃过滤器
            active = self._filters[-1]
            active.add(item)
            self._total_count += 1
            
            # 如果活跃过滤器接近容量，创建新的
            if len(active) >= active._n * 0.8:
                self._add_filter()
    
    def __contains__(self, item: Union[str, bytes]) -> bool:
        """检查元素是否存在"""
        for bf in self._filters:
            if item in bf:
                return True
        return False
    
    def __len__(self) -> int:
        return self._total_count
    
    def __repr__(self) -> str:
        return (
            f"ScalableBloomFilter(items={self._total_count}, "
            f"layers={len(self._filters)})"
        )


class CountingBloomFilter:
    """
    计数布隆过滤器
    
    支持删除操作的布隆过滤器变体，
    每个比特位使用计数器。
    
    示例:
        >>> cbf = CountingBloomFilter(expected_items=1000)
        >>> cbf.add("test")
        >>> "test" in cbf
        True
        >>> cbf.remove("test")
        >>> "test" in cbf
        False
    """
    
    def __init__(
        self,
        expected_items: int = 10000,
        false_positive_rate: float = 0.01,
        counter_bits: int = 4
    ):
        """
        初始化计数布隆过滤器
        
        Args:
            expected_items: 预期元素数量
            false_positive_rate: 误判率
            counter_bits: 每个计数器的位数（默认4位，最大值15）
        """
        self._n = expected_items
        self._p = false_positive_rate
        self._counter_bits = counter_bits
        self._max_count = (1 << counter_bits) - 1
        
        # 计算参数
        self._m = int(-expected_items * math.log(false_positive_rate) / (math.log(2) ** 2))
        self._k = max(1, int(self._m / expected_items * math.log(2)))
        
        # 计数器数组
        self._counters = [0] * self._m
        self._item_count = 0
        self._lock = Lock()
    
    def _hashes(self, item: Union[str, bytes]) -> List[int]:
        """生成哈希值"""
        if isinstance(item, str):
            item = item.encode('utf-8')
        
        h1 = int(hashlib.md5(item).hexdigest(), 16)
        h2 = int(hashlib.sha1(item).hexdigest(), 16)
        
        return [(h1 + i * h2) % self._m for i in range(self._k)]
    
    def add(self, item: Union[str, bytes], count: int = 1) -> bool:
        """
        添加元素
        
        Args:
            item: 元素
            count: 添加次数
            
        Returns:
            是否成功添加（计数器溢出返回False）
        """
        with self._lock:
            for h in self._hashes(item):
                if self._counters[h] + count > self._max_count:
                    return False
                self._counters[h] += count
            self._item_count += 1
            return True
    
    def remove(self, item: Union[str, bytes]) -> bool:
        """
        删除元素
        
        Args:
            item: 要删除的元素
            
        Returns:
            是否成功删除
        """
        with self._lock:
            # 先检查是否存在
            hashes = self._hashes(item)
            for h in hashes:
                if self._counters[h] == 0:
                    return False
            
            # 执行删除
            for h in hashes:
                self._counters[h] -= 1
            self._item_count -= 1
            return True
    
    def __contains__(self, item: Union[str, bytes]) -> bool:
        """检查元素是否存在"""
        for h in self._hashes(item):
            if self._counters[h] == 0:
                return False
        return True
    
    def __len__(self) -> int:
        return self._item_count
    
    def count(self, item: Union[str, bytes]) -> int:
        """
        估计元素的出现次数
        
        返回所有计数器中的最小值
        """
        hashes = self._hashes(item)
        return min(self._counters[h] for h in hashes)
    
    def clear(self) -> None:
        """清空过滤器"""
        with self._lock:
            self._counters = [0] * self._m
            self._item_count = 0


# ============ 便捷函数 ============

def create_filter(
    expected_items: int = 10000,
    false_positive_rate: float = 0.01
) -> BloomFilter:
    """
    创建布隆过滤器的便捷函数
    
    Args:
        expected_items: 预期元素数量
        false_positive_rate: 误判率
        
    Returns:
        配置好的布隆过滤器
    """
    return BloomFilter(expected_items, false_positive_rate)


def create_scalable(
    initial_capacity: int = 1000,
    false_positive_rate: float = 0.01
) -> ScalableBloomFilter:
    """
    创建可扩展布隆过滤器
    """
    return ScalableBloomFilter(initial_capacity, false_positive_rate)


def estimate_size(
    expected_items: int,
    false_positive_rate: float
) -> dict:
    """
    估算布隆过滤器所需资源
    
    Args:
        expected_items: 预期元素数量
        false_positive_rate: 误判率
        
    Returns:
        包含 bits, bytes, hash_functions 的字典
    """
    m = int(-expected_items * math.log(false_positive_rate) / (math.log(2) ** 2))
    k = max(1, int(m / expected_items * math.log(2)))
    
    return {
        'bits': m,
        'bytes': m // 8,
        'kb': round(m / 8 / 1024, 2),
        'mb': round(m / 8 / 1024 / 1024, 4),
        'hash_functions': k
    }


if __name__ == "__main__":
    # 简单演示
    bf = BloomFilter(10000, 0.01)
    
    # 添加元素
    urls = ["http://example.com", "http://test.com", "http://demo.com"]
    for url in urls:
        bf.add(url)
    
    # 检查存在
    print(f"'http://example.com' in filter: {'http://example.com' in bf}")
    print(f"'http://unknown.com' in filter: {'http://unknown.com' in bf}")
    print(f"\nFilter stats: {bf}")
    print(f"Estimated FP rate: {bf.estimated_false_positive_rate:.6f}")
    
    # 序列化测试
    data = bf.serialize()
    bf2 = BloomFilter.deserialize(data)
    print(f"\nDeserialized filter works: {'http://example.com' in bf2}")