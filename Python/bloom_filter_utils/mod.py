"""
布隆过滤器 (Bloom Filter) 工具模块

布隆过滤器是一种空间效率很高的概率数据结构，用于判断一个元素是否在集合中。
特点：
- 空间效率高：使用位数组存储，空间占用小
- 查询速度快：O(k) 时间复杂度，k 是哈希函数数量
- 可能存在假阳性 (False Positive)，但不存在假阴性
- 不支持删除操作（标准布隆过滤器）

使用场景：
- 缓存穿透防护
- 垃圾邮件过滤
- URL去重
- 推荐系统去重
"""

import math
from typing import List, Optional, Tuple


class BloomFilter:
    """
    布隆过滤器实现
    
    Attributes:
        size: 位数组大小
        hash_count: 哈希函数数量
        bit_array: 位数组
        item_count: 已添加元素数量
    """
    
    def __init__(self, expected_items: int = 10000, false_positive_rate: float = 0.01):
        """
        初始化布隆过滤器
        
        Args:
            expected_items: 预期元素数量
            false_positive_rate: 期望的假阳性率 (0-1之间)
        """
        if expected_items <= 0:
            raise ValueError("预期元素数量必须大于0")
        if not 0 < false_positive_rate < 1:
            raise ValueError("假阳性率必须在0和1之间")
        
        # 计算最优位数组大小和哈希函数数量
        self.size = self._calculate_optimal_size(expected_items, false_positive_rate)
        self.hash_count = self._calculate_optimal_hash_count(expected_items, self.size)
        self.bit_array = [False] * self.size
        self.item_count = 0
    
    @staticmethod
    def _calculate_optimal_size(n: int, p: float) -> int:
        """
        计算最优位数组大小
        
        公式: m = -n * ln(p) / (ln(2))^2
        
        Args:
            n: 预期元素数量
            p: 假阳性率
            
        Returns:
            位数组大小
        """
        m = -n * math.log(p) / (math.log(2) ** 2)
        return int(math.ceil(m))
    
    @staticmethod
    def _calculate_optimal_hash_count(n: int, m: int) -> int:
        """
        计算最优哈希函数数量
        
        公式: k = (m/n) * ln(2)
        
        Args:
            n: 预期元素数量
            m: 位数组大小
            
        Returns:
            哈希函数数量
        """
        k = (m / n) * math.log(2)
        return int(math.ceil(k))
    
    def _hash_functions(self, item: str) -> List[int]:
        """
        生成多个哈希值
        
        使用双重哈希技术：h(i) = hash1(item) + i * hash2(item)
        
        Args:
            item: 要哈希的元素
            
        Returns:
            哈希值列表
        """
        hash_values = []
        
        # 使用内置hash函数和字符串的哈希
        hash1 = hash(str(item))
        hash2 = hash(str(item) + "_salt_" + str(hash1))
        
        for i in range(self.hash_count):
            # 确保哈希值为正数并在范围内
            combined = abs(hash1 + i * hash2) % self.size
            hash_values.append(combined)
        
        return hash_values
    
    def add(self, item: str) -> None:
        """
        添加元素到布隆过滤器
        
        Args:
            item: 要添加的元素
        """
        hash_values = self._hash_functions(item)
        for pos in hash_values:
            self.bit_array[pos] = True
        self.item_count += 1
    
    def contains(self, item: str) -> bool:
        """
        检查元素是否可能在集合中
        
        Args:
            item: 要检查的元素
            
        Returns:
            True 表示元素可能在集合中（可能假阳性）
            False 表示元素一定不在集合中
        """
        hash_values = self._hash_functions(item)
        return all(self.bit_array[pos] for pos in hash_values)
    
    def __contains__(self, item: str) -> bool:
        """支持 `item in bloom_filter` 语法"""
        return self.contains(item)
    
    def current_false_positive_rate(self) -> float:
        """
        计算当前假阳性率
        
        基于已添加的元素数量计算实际假阳性率
        
        Returns:
            当前假阳性率
        """
        if self.item_count == 0:
            return 0.0
        
        # p = (1 - e^(-k*n/m))^k
        ratio = self.item_count * self.hash_count / self.size
        return (1 - math.exp(-ratio)) ** self.hash_count
    
    def load_factor(self) -> float:
        """
        计算位数组的负载因子
        
        Returns:
            已设置位占总位的比例
        """
        set_bits = sum(self.bit_array)
        return set_bits / self.size
    
    def clear(self) -> None:
        """清空布隆过滤器"""
        self.bit_array = [False] * self.size
        self.item_count = 0
    
    def get_stats(self) -> dict:
        """
        获取布隆过滤器统计信息
        
        Returns:
            包含各种统计信息的字典
        """
        return {
            "size": self.size,
            "hash_count": self.hash_count,
            "item_count": self.item_count,
            "load_factor": self.load_factor(),
            "current_false_positive_rate": self.current_false_positive_rate(),
            "bits_per_item": self.size / max(self.item_count, 1)
        }
    
    def union(self, other: 'BloomFilter') -> 'BloomFilter':
        """
        合并两个布隆过滤器
        
        Args:
            other: 另一个布隆过滤器
            
        Returns:
            新的布隆过滤器
            
        Raises:
            ValueError: 如果两个过滤器大小或哈希数量不匹配
        """
        if self.size != other.size or self.hash_count != other.hash_count:
            raise ValueError("只能合并大小和哈希数量相同的布隆过滤器")
        
        result = BloomFilter.__new__(BloomFilter)
        result.size = self.size
        result.hash_count = self.hash_count
        result.bit_array = [a or b for a, b in zip(self.bit_array, other.bit_array)]
        result.item_count = -1  # 合并后无法准确知道元素数量
        
        return result
    
    def intersection(self, other: 'BloomFilter') -> 'BloomFilter':
        """
        计算两个布隆过滤器的交集
        
        Args:
            other: 另一个布隆过滤器
            
        Returns:
            新的布隆过滤器
        """
        if self.size != other.size or self.hash_count != other.hash_count:
            raise ValueError("只能对大小和哈希数量相同的布隆过滤器求交集")
        
        result = BloomFilter.__new__(BloomFilter)
        result.size = self.size
        result.hash_count = self.hash_count
        result.bit_array = [a and b for a, b in zip(self.bit_array, other.bit_array)]
        result.item_count = -1
        
        return result
    
    def to_bytes(self) -> bytes:
        """
        将布隆过滤器序列化为字节
        
        Returns:
            字节表示
        """
        # 头部: size(4字节) + hash_count(4字节) + item_count(4字节)
        header = (
            self.size.to_bytes(4, 'big') +
            self.hash_count.to_bytes(4, 'big') +
            self.item_count.to_bytes(4, 'big')
        )
        
        # 位数组转换为字节
        byte_count = (self.size + 7) // 8
        byte_array = bytearray(byte_count)
        
        for i, bit in enumerate(self.bit_array):
            if bit:
                byte_array[i // 8] |= (1 << (7 - (i % 8)))
        
        return header + bytes(byte_array)
    
    @classmethod
    def from_bytes(cls, data: bytes) -> 'BloomFilter':
        """
        从字节反序列化布隆过滤器
        
        Args:
            data: 字节数据
            
        Returns:
            布隆过滤器实例
        """
        if len(data) < 12:
            raise ValueError("数据太短，无法反序列化")
        
        # 解析头部
        size = int.from_bytes(data[0:4], 'big')
        hash_count = int.from_bytes(data[4:8], 'big')
        item_count = int.from_bytes(data[8:12], 'big')
        
        # 创建实例
        result = cls.__new__(cls)
        result.size = size
        result.hash_count = hash_count
        result.item_count = item_count
        result.bit_array = [False] * size
        
        # 解析位数组
        byte_array = data[12:]
        for i in range(size):
            byte_index = i // 8
            bit_index = 7 - (i % 8)
            if byte_index < len(byte_array):
                result.bit_array[i] = bool((byte_array[byte_index] >> bit_index) & 1)
        
        return result
    
    def __len__(self) -> int:
        """返回已添加元素数量"""
        return self.item_count
    
    def __repr__(self) -> str:
        return f"BloomFilter(size={self.size}, hash_count={self.hash_count}, items={self.item_count})"


class CountingBloomFilter:
    """
    计数布隆过滤器
    
    支持删除操作，每个位置存储计数而非布尔值
    """
    
    def __init__(self, expected_items: int = 10000, false_positive_rate: float = 0.01, max_count: int = 255):
        """
        初始化计数布隆过滤器
        
        Args:
            expected_items: 预期元素数量
            false_positive_rate: 假阳性率
            max_count: 每个位置的最大计数值
        """
        self.size = BloomFilter._calculate_optimal_size(expected_items, false_positive_rate)
        self.hash_count = BloomFilter._calculate_optimal_hash_count(expected_items, self.size)
        self.count_array = [0] * self.size
        self.max_count = max_count
        self.item_count = 0
    
    def _hash_functions(self, item: str) -> List[int]:
        """生成哈希值"""
        hash_values = []
        hash1 = hash(str(item))
        hash2 = hash(str(item) + "_salt_" + str(hash1))
        
        for i in range(self.hash_count):
            combined = abs(hash1 + i * hash2) % self.size
            hash_values.append(combined)
        
        return hash_values
    
    def add(self, item: str) -> bool:
        """
        添加元素
        
        Returns:
            是否成功添加（如果计数器已满则返回False）
        """
        hash_values = self._hash_functions(item)
        
        # 先检查是否会溢出
        for pos in hash_values:
            if self.count_array[pos] >= self.max_count:
                return False
        
        for pos in hash_values:
            self.count_array[pos] += 1
        
        self.item_count += 1
        return True
    
    def remove(self, item: str) -> bool:
        """
        移除元素
        
        Args:
            item: 要移除的元素
            
        Returns:
            是否成功移除（如果元素不存在则返回False）
        """
        if not self.contains(item):
            return False
        
        hash_values = self._hash_functions(item)
        for pos in hash_values:
            self.count_array[pos] -= 1
        
        self.item_count -= 1
        return True
    
    def contains(self, item: str) -> bool:
        """检查元素是否可能在集合中"""
        hash_values = self._hash_functions(item)
        return all(self.count_array[pos] > 0 for pos in hash_values)
    
    def __contains__(self, item: str) -> bool:
        return self.contains(item)
    
    def clear(self) -> None:
        """清空过滤器"""
        self.count_array = [0] * self.size
        self.item_count = 0
    
    def get_stats(self) -> dict:
        """获取统计信息"""
        active_positions = sum(1 for c in self.count_array if c > 0)
        total_count = sum(self.count_array)
        avg_count = total_count / max(active_positions, 1)
        
        return {
            "size": self.size,
            "hash_count": self.hash_count,
            "item_count": self.item_count,
            "active_positions": active_positions,
            "total_count": total_count,
            "average_count": avg_count
        }
    
    def __len__(self) -> int:
        return self.item_count
    
    def __repr__(self) -> str:
        return f"CountingBloomFilter(size={self.size}, hash_count={self.hash_count}, items={self.item_count})"


class ScalableBloomFilter:
    """
    可扩展布隆过滤器
    
    当填充率达到阈值时自动扩展，适用于不确定数据量的场景
    """
    
    def __init__(self, initial_size: int = 1000, growth_factor: float = 2.0, 
                 false_positive_rate: float = 0.01, fill_threshold: float = 0.75):
        """
        初始化可扩展布隆过滤器
        
        Args:
            initial_size: 初始预期元素数量
            growth_factor: 增长因子
            false_positive_rate: 假阳性率
            fill_threshold: 触发扩展的填充阈值
        """
        self.initial_size = initial_size
        self.growth_factor = growth_factor
        self.base_fp_rate = false_positive_rate
        self.fill_threshold = fill_threshold
        
        self.filters: List[BloomFilter] = []
        self.current_capacity = initial_size
        self.item_count = 0
        
        # 添加第一个过滤器
        self._add_filter()
    
    def _add_filter(self) -> None:
        """添加新的布隆过滤器"""
        # 每个新过滤器的假阳性率递减
        fp_rate = self.base_fp_rate / (2 ** len(self.filters))
        bf = BloomFilter(expected_items=self.current_capacity, false_positive_rate=fp_rate)
        self.filters.append(bf)
        self.current_capacity = int(self.current_capacity * self.growth_factor)
    
    def add(self, item: str) -> None:
        """添加元素"""
        # 检查最后一个过滤器是否需要扩展
        last_filter = self.filters[-1]
        if last_filter.load_factor() >= self.fill_threshold:
            self._add_filter()
            last_filter = self.filters[-1]
        
        last_filter.add(item)
        self.item_count += 1
    
    def contains(self, item: str) -> bool:
        """检查元素是否存在"""
        return any(bf.contains(item) for bf in self.filters)
    
    def __contains__(self, item: str) -> bool:
        return self.contains(item)
    
    def get_stats(self) -> dict:
        """获取统计信息"""
        return {
            "filter_count": len(self.filters),
            "total_item_count": self.item_count,
            "current_capacity": self.current_capacity,
            "filter_stats": [bf.get_stats() for bf in self.filters]
        }
    
    def __len__(self) -> int:
        return self.item_count
    
    def __repr__(self) -> str:
        return f"ScalableBloomFilter(filters={len(self.filters)}, items={self.item_count})"


# 便捷函数
def create_bloom_filter(items: Optional[List[str]] = None, 
                        expected_items: int = 10000,
                        false_positive_rate: float = 0.01) -> BloomFilter:
    """
    创建并初始化布隆过滤器
    
    Args:
        items: 初始元素列表
        expected_items: 预期元素数量
        false_positive_rate: 假阳性率
        
    Returns:
        初始化后的布隆过滤器
    """
    bf = BloomFilter(expected_items=expected_items, false_positive_rate=false_positive_rate)
    if items:
        for item in items:
            bf.add(item)
    return bf


def calculate_optimal_params(expected_items: int, 
                              false_positive_rate: float) -> Tuple[int, int]:
    """
    计算布隆过滤器的最优参数
    
    Args:
        expected_items: 预期元素数量
        false_positive_rate: 假阳性率
        
    Returns:
        (位数组大小, 哈希函数数量)
    """
    size = BloomFilter._calculate_optimal_size(expected_items, false_positive_rate)
    hash_count = BloomFilter._calculate_optimal_hash_count(expected_items, size)
    return size, hash_count


def estimate_memory_usage(expected_items: int, 
                          false_positive_rate: float) -> int:
    """
    估算布隆过滤器的内存使用量（字节）
    
    Args:
        expected_items: 预期元素数量
        false_positive_rate: 假阳性率
        
    Returns:
        预计内存使用量（字节）
    """
    size, _ = calculate_optimal_params(expected_items, false_positive_rate)
    return (size + 7) // 8  # 位转字节


if __name__ == "__main__":
    # 演示用法
    print("=== 布隆过滤器演示 ===\n")
    
    # 创建布隆过滤器
    bf = BloomFilter(expected_items=100, false_positive_rate=0.01)
    print(f"创建过滤器: {bf}")
    print(f"参数: 大小={bf.size}, 哈希函数数={bf.hash_count}")
    
    # 添加元素
    test_items = ["apple", "banana", "cherry", "date", "elderberry"]
    for item in test_items:
        bf.add(item)
    print(f"\n添加了 {len(test_items)} 个元素")
    
    # 检查元素
    print("\n检查结果:")
    for item in test_items:
        print(f"  '{item}': {item in bf}")
    
    # 检查不存在的元素
    print("\n检查不存在的元素:")
    for item in ["grape", "fig", "kiwi"]:
        result = item in bf
        status = "(假阳性!)" if result else ""
        print(f"  '{item}': {result} {status}")
    
    # 统计信息
    print(f"\n统计信息:")
    stats = bf.get_stats()
    for key, value in stats.items():
        print(f"  {key}: {value}")
    
    # 序列化演示
    print("\n=== 序列化演示 ===")
    data = bf.to_bytes()
    print(f"序列化大小: {len(data)} 字节")
    
    restored = BloomFilter.from_bytes(data)
    print(f"反序列化: {restored}")
    print(f"验证 'apple' 在恢复的过滤器中: {'apple' in restored}")