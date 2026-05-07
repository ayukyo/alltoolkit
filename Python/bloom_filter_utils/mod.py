"""
Bloom Filter Utils - 布隆过滤器工具模块

布隆过滤器是一种空间高效的概率数据结构，用于判断元素是否在集合中。
特点：
- 空间效率极高：相比哈希表，占用空间极小
- 查询时间恒定：O(k)，k为哈希函数数量
- 可能产生假阳性（误判存在），但不会假阴性（不会漏判）
- 不支持删除操作（标准版本）

应用场景：
- 数据库查询优化（避免不必要的磁盘查找）
- 缓存穿透防护
- 网页爬虫URL去重
- 垃圾邮件/恶意网站过滤
- 拼写检查器
- 分布式系统数据同步

零外部依赖，仅使用 Python 标准库。
"""

import math
import struct
import hashlib
from typing import Any, Optional, Iterator, List
from dataclasses import dataclass


@dataclass
class BloomFilterStats:
    """布隆过滤器统计信息"""
    capacity: int           # 设计容量
    error_rate: float       # 设计错误率
    num_bits: int          # 位数组大小
    num_hashes: int        # 哈希函数数量
    num_elements: int      # 已插入元素数量
    fill_ratio: float      # 填充率
    current_error_rate: float  # 当前估计错误率


class BloomFilter:
    """
    布隆过滤器实现
    
    使用示例：
        >>> bf = BloomFilter(capacity=10000, error_rate=0.01)
        >>> bf.add("hello")
        >>> bf.add("world")
        >>> "hello" in bf
        True
        >>> "unknown" in bf
        False
    """
    
    def __init__(
        self,
        capacity: int = 10000,
        error_rate: float = 0.01,
        hash_algorithm: str = 'sha256'
    ):
        """
        初始化布隆过滤器
        
        Args:
            capacity: 预期存储的元素数量
            error_rate: 可接受的假阳性率（0-1之间）
            hash_algorithm: 哈希算法（md5, sha1, sha256, sha512）
        """
        if capacity <= 0:
            raise ValueError("capacity 必须大于 0")
        if not 0 < error_rate < 1:
            raise ValueError("error_rate 必须在 0 和 1 之间")
        if hash_algorithm not in ('md5', 'sha1', 'sha256', 'sha512'):
            raise ValueError(f"不支持的哈希算法: {hash_algorithm}")
        
        self._capacity = capacity
        self._error_rate = error_rate
        self._hash_algorithm = hash_algorithm
        
        # 计算最优参数
        # m = -n * ln(p) / (ln(2)^2)
        # k = m * ln(2) / n
        self._num_bits = self._calculate_optimal_bits(capacity, error_rate)
        self._num_hashes = self._calculate_optimal_hashes(self._num_bits, capacity)
        
        # 位数组（使用整数列表模拟）
        self._bit_array = [0] * ((self._num_bits + 31) // 32)  # 每32位一个整数
        self._count = 0
    
    @staticmethod
    def _calculate_optimal_bits(n: int, p: float) -> int:
        """计算最优位数组大小"""
        return int(-n * math.log(p) / (math.log(2) ** 2))
    
    @staticmethod
    def _calculate_optimal_hashes(m: int, n: int) -> int:
        """计算最优哈希函数数量"""
        return max(1, int(m * math.log(2) / n))
    
    def _hash(self, item: Any, seed: int) -> int:
        """
        使用双重哈希生成第 seed 个哈希值
        
        双重哈希技术：h_i(x) = (h1(x) + i * h2(x)) % m
        这样只需两次哈希计算就能生成 k 个哈希值
        """
        # 序列化对象为字节
        if isinstance(item, bytes):
            data = item
        elif isinstance(item, str):
            data = item.encode('utf-8')
        else:
            data = str(item).encode('utf-8')
        
        # 计算基础哈希值
        h1 = int(hashlib.new(self._hash_algorithm, data).hexdigest(), 16)
        
        # 使用不同的种子计算第二个哈希值
        h2 = int(hashlib.new(
            self._hash_algorithm, 
            data + seed.to_bytes(4, 'big')
        ).hexdigest(), 16)
        
        # 双重哈希公式
        return (h1 + seed * h2) % self._num_bits
    
    def _set_bit(self, index: int) -> bool:
        """设置位，返回是否是新设置的"""
        array_index = index // 32
        bit_offset = index % 32
        mask = 1 << bit_offset
        
        old_value = self._bit_array[array_index] & mask
        self._bit_array[array_index] |= mask
        return old_value == 0
    
    def _get_bit(self, index: int) -> bool:
        """获取位值"""
        array_index = index // 32
        bit_offset = index % 32
        return bool(self._bit_array[array_index] & (1 << bit_offset))
    
    def add(self, item: Any) -> None:
        """
        添加元素到布隆过滤器
        
        Args:
            item: 要添加的元素（可以是任何可哈希的对象）
        """
        for i in range(self._num_hashes):
            index = self._hash(item, i)
            self._set_bit(index)
        self._count += 1
    
    def __contains__(self, item: Any) -> bool:
        """
        检查元素可能在集合中
        
        Args:
            item: 要检查的元素
            
        Returns:
            True 如果元素可能在集合中（可能有假阳性）
            False 如果元素一定不在集合中（不会假阴性）
        """
        for i in range(self._num_hashes):
            index = self._hash(item, i)
            if not self._get_bit(index):
                return False
        return True
    
    def might_contain(self, item: Any) -> bool:
        """检查元素可能存在（__contains__ 的别名）"""
        return item in self
    
    def __len__(self) -> int:
        """返回已插入元素数量"""
        return self._count
    
    def __repr__(self) -> str:
        return (
            f"BloomFilter(capacity={self._capacity}, error_rate={self._error_rate}, "
            f"bits={self._num_bits}, hashes={self._num_hashes}, elements={self._count})"
        )
    
    def get_stats(self) -> BloomFilterStats:
        """获取统计信息"""
        # 计算当前填充率
        filled_bits = sum(
            bin(word).count('1') 
            for word in self._bit_array
        )
        fill_ratio = filled_bits / self._num_bits if self._num_bits > 0 else 0
        
        # 估计当前错误率：(1 - e^(-kn/m))^k
        if self._count == 0:
            current_error_rate = 0.0
        else:
            current_error_rate = (1 - math.exp(
                -self._num_hashes * self._count / self._num_bits
            )) ** self._num_hashes
        
        return BloomFilterStats(
            capacity=self._capacity,
            error_rate=self._error_rate,
            num_bits=self._num_bits,
            num_hashes=self._num_hashes,
            num_elements=self._count,
            fill_ratio=fill_ratio,
            current_error_rate=current_error_rate
        )
    
    def to_bytes(self) -> bytes:
        """
        序列化为字节
        
        Returns:
            字节表示，可用于持久化存储
        """
        # 格式：版本(1) + capacity(8) + error_rate(8) + hash_algorithm_len(1) + hash_algorithm + num_bits(8) + count(8) + bit_array
        algo_bytes = self._hash_algorithm.encode('utf-8')
        header = (
            b'\x01' +  # 版本
            self._capacity.to_bytes(8, 'big') +
            struct.pack('>d', self._error_rate) +
            len(algo_bytes).to_bytes(1, 'big') +
            algo_bytes +
            self._num_bits.to_bytes(8, 'big') +
            self._count.to_bytes(8, 'big')
        )
        
        # 压缩位数组
        bit_bytes = b''.join(
            word.to_bytes(4, 'big') 
            for word in self._bit_array
        )
        
        return header + bit_bytes
    
    @classmethod
    def from_bytes(cls, data: bytes) -> 'BloomFilter':
        """
        从字节反序列化
        
        Args:
            data: to_bytes() 方法产生的字节数据
            
        Returns:
            反序列化的 BloomFilter 实例
        """
        import struct
        
        if len(data) < 26:
            raise ValueError("数据太短，无法解析")
        
        version = data[0]
        if version != 1:
            raise ValueError(f"不支持的版本: {version}")
        
        offset = 1
        capacity = int.from_bytes(data[offset:offset+8], 'big')
        offset += 8
        
        error_rate = struct.unpack('>d', data[offset:offset+8])[0]
        offset += 8
        
        algo_len = data[offset]
        offset += 1
        
        hash_algorithm = data[offset:offset+algo_len].decode('utf-8')
        offset += algo_len
        
        num_bits = int.from_bytes(data[offset:offset+8], 'big')
        offset += 8
        
        count = int.from_bytes(data[offset:offset+8], 'big')
        offset += 8
        
        # 创建实例
        bf = cls(capacity=capacity, error_rate=error_rate, hash_algorithm=hash_algorithm)
        bf._count = count
        
        # 恢复位数组
        num_words = (num_bits + 31) // 32
        bf._bit_array = [
            int.from_bytes(data[offset+i*4:offset+i*4+4], 'big')
            for i in range(num_words)
        ]
        
        return bf
    
    def clear(self) -> None:
        """清空布隆过滤器"""
        self._bit_array = [0] * ((self._num_bits + 31) // 32)
        self._count = 0
    
    @property
    def capacity(self) -> int:
        """设计容量"""
        return self._capacity
    
    @property
    def error_rate(self) -> float:
        """设计错误率"""
        return self._error_rate
    
    @property
    def num_bits(self) -> int:
        """位数组大小"""
        return self._num_bits
    
    @property
    def num_hashes(self) -> int:
        """哈希函数数量"""
        return self._num_hashes


class ScalableBloomFilter:
    """
    可扩展布隆过滤器
    
    当元素数量超过预期时自动扩展，保持假阳性率在控制范围内。
    
    使用示例：
        >>> sbf = ScalableBloomFilter(initial_capacity=1000, error_rate=0.01)
        >>> for i in range(10000):
        ...     sbf.add(f"item_{i}")
        >>> "item_5" in sbf
        True
    """
    
    def __init__(
        self,
        initial_capacity: int = 1000,
        error_rate: float = 0.01,
        growth_factor: int = 2
    ):
        """
        初始化可扩展布隆过滤器
        
        Args:
            initial_capacity: 初始容量
            error_rate: 目标假阳性率
            growth_factor: 扩展因子（新过滤器容量是当前的多少倍）
        """
        if initial_capacity <= 0:
            raise ValueError("initial_capacity 必须大于 0")
        if not 0 < error_rate < 1:
            raise ValueError("error_rate 必须在 0 和 1 之间")
        if growth_factor < 2:
            raise ValueError("growth_factor 必须至少为 2")
        
        self._initial_capacity = initial_capacity
        self._error_rate = error_rate
        self._growth_factor = growth_factor
        
        self._filters: List[BloomFilter] = []
        self._total_count = 0
        
        # 创建第一个过滤器
        self._add_filter(initial_capacity)
    
    def _add_filter(self, capacity: int) -> None:
        """添加新的布隆过滤器层"""
        # 每层的错误率逐渐降低，以保持整体错误率
        layer_error_rate = self._error_rate / (2 ** len(self._filters))
        bf = BloomFilter(capacity=capacity, error_rate=layer_error_rate)
        self._filters.append(bf)
    
    def add(self, item: Any) -> None:
        """添加元素"""
        # 如果当前过滤器满了，创建新的
        if len(self._filters[-1]) >= self._filters[-1].capacity:
            new_capacity = self._filters[-1].capacity * self._growth_factor
            self._add_filter(new_capacity)
        
        self._filters[-1].add(item)
        self._total_count += 1
    
    def __contains__(self, item: Any) -> bool:
        """检查元素是否存在"""
        return any(item in bf for bf in self._filters)
    
    def might_contain(self, item: Any) -> bool:
        """检查元素可能存在"""
        return item in self
    
    def __len__(self) -> int:
        """返回总元素数量"""
        return self._total_count
    
    def get_stats(self) -> dict:
        """获取统计信息"""
        return {
            'total_elements': self._total_count,
            'num_layers': len(self._filters),
            'layers': [
                {
                    'layer': i,
                    'capacity': bf.capacity,
                    'elements': len(bf),
                    'error_rate': bf.error_rate,
                    'fill_ratio': bf.get_stats().fill_ratio
                }
                for i, bf in enumerate(self._filters)
            ]
        }
    
    def __repr__(self) -> str:
        return (
            f"ScalableBloomFilter(layers={len(self._filters)}, "
            f"total_elements={self._total_count})"
        )


class CountingBloomFilter:
    """
    计数布隆过滤器
    
    支持删除操作的布隆过滤器变体，使用计数器代替位数组。
    
    使用示例：
        >>> cbf = CountingBloomFilter(capacity=1000, error_rate=0.01)
        >>> cbf.add("hello")
        >>> "hello" in cbf
        True
        >>> cbf.remove("hello")
        >>> "hello" in cbf
        False
    """
    
    def __init__(
        self,
        capacity: int = 10000,
        error_rate: float = 0.01,
        max_count: int = 15
    ):
        """
        初始化计数布隆过滤器
        
        Args:
            capacity: 预期容量
            error_rate: 目标错误率
            max_count: 每个位置的最大计数值（默认15，用4位表示）
        """
        if capacity <= 0:
            raise ValueError("capacity 必须大于 0")
        if not 0 < error_rate < 1:
            raise ValueError("error_rate 必须在 0 和 1 之间")
        
        self._capacity = capacity
        self._error_rate = error_rate
        self._max_count = max_count
        
        # 计算最优参数
        self._num_bits = BloomFilter._calculate_optimal_bits(capacity, error_rate)
        self._num_hashes = BloomFilter._calculate_optimal_hashes(self._num_bits, capacity)
        
        # 计数器数组（每个计数器用4位，所以每字节存2个计数器）
        self._counters = [0] * self._num_bits
        self._count = 0
    
    def _hash(self, item: Any, seed: int) -> int:
        """计算哈希值"""
        if isinstance(item, bytes):
            data = item
        elif isinstance(item, str):
            data = item.encode('utf-8')
        else:
            data = str(item).encode('utf-8')
        
        h1 = int(hashlib.sha256(data).hexdigest(), 16)
        h2 = int(hashlib.sha256(data + seed.to_bytes(4, 'big')).hexdigest(), 16)
        
        return (h1 + seed * h2) % self._num_bits
    
    def add(self, item: Any) -> bool:
        """
        添加元素
        
        Returns:
            True 如果成功添加，False 如果计数器已满
        """
        success = True
        for i in range(self._num_hashes):
            index = self._hash(item, i)
            if self._counters[index] < self._max_count:
                self._counters[index] += 1
            else:
                success = False  # 计数器溢出
        
        if success:
            self._count += 1
        return success
    
    def remove(self, item: Any) -> bool:
        """
        删除元素
        
        Returns:
            True 如果成功删除，False 如果元素不存在
        """
        # 先检查是否存在
        if item not in self:
            return False
        
        for i in range(self._num_hashes):
            index = self._hash(item, i)
            if self._counters[index] > 0:
                self._counters[index] -= 1
        
        self._count -= 1
        return True
    
    def __contains__(self, item: Any) -> bool:
        """检查元素是否存在"""
        for i in range(self._num_hashes):
            index = self._hash(item, i)
            if self._counters[index] == 0:
                return False
        return True
    
    def __len__(self) -> int:
        """返回元素数量"""
        return self._count
    
    def __repr__(self) -> str:
        return (
            f"CountingBloomFilter(capacity={self._capacity}, "
            f"error_rate={self._error_rate}, elements={self._count})"
        )


# 便捷函数
def create_filter(
    capacity: int = 10000,
    error_rate: float = 0.01
) -> BloomFilter:
    """创建标准布隆过滤器"""
    return BloomFilter(capacity=capacity, error_rate=error_rate)


def create_scalable_filter(
    initial_capacity: int = 1000,
    error_rate: float = 0.01
) -> ScalableBloomFilter:
    """创建可扩展布隆过滤器"""
    return ScalableBloomFilter(
        initial_capacity=initial_capacity,
        error_rate=error_rate
    )


def create_counting_filter(
    capacity: int = 10000,
    error_rate: float = 0.01
) -> CountingBloomFilter:
    """创建计数布隆过滤器"""
    return CountingBloomFilter(capacity=capacity, error_rate=error_rate)


if __name__ == "__main__":
    # 简单演示
    print("=== Bloom Filter 演示 ===")
    
    # 创建过滤器
    bf = BloomFilter(capacity=1000, error_rate=0.01)
    print(f"创建: {bf}")
    
    # 添加元素
    words = ["apple", "banana", "cherry", "date", "elderberry"]
    for word in words:
        bf.add(word)
    
    print(f"\n添加 {len(words)} 个元素后:")
    print(f"  'apple' 存在: {'apple' in bf}")
    print(f"  'grape' 存在: {'grape' in bf}")
    
    # 统计信息
    stats = bf.get_stats()
    print(f"\n统计信息:")
    print(f"  容量: {stats.capacity}")
    print(f"  位数: {stats.num_bits}")
    print(f"  哈希数: {stats.num_hashes}")
    print(f"  元素数: {stats.num_elements}")
    print(f"  填充率: {stats.fill_ratio:.4f}")
    print(f"  当前错误率: {stats.current_error_rate:.6f}")