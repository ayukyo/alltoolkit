"""
Reservoir Sampling Utils - 水库采样工具集

提供多种水库采样算法实现，用于从未知大小或大数据流中进行随机采样。
所有算法均为 O(n) 时间复杂度和 O(k) 空间复杂度，其中 k 为采样大小。

核心算法:
- Algorithm R (经典水库采样)
- Algorithm L (高效水库采样)
- Weighted Reservoir Sampling (加权水库采样)
- Reservoir Sampling with Replacement (有放回采样)
"""

import random
import math
from typing import TypeVar, Generic, List, Iterator, Optional, Callable, Any, Tuple
from dataclasses import dataclass, field
from collections import defaultdict

T = TypeVar('T')


class ReservoirSampler(Generic[T]):
    """
    经典水库采样算法 (Algorithm R)
    
    适用场景:
    - 从数据流中均匀随机采样 k 个元素
    - 数据量未知或无法全部加载到内存
    
    时间复杂度: O(n)
    空间复杂度: O(k)
    
    示例:
        >>> sampler = ReservoirSampler(3)
        >>> for item in range(10):
        ...     sampler.add(item)
        >>> sample = sampler.sample()
        >>> len(sample) == 3
        True
    """
    
    def __init__(self, k: int, seed: Optional[int] = None):
        """
        初始化采样器
        
        Args:
            k: 采样大小
            seed: 随机种子（可选，用于复现结果）
        """
        if k <= 0:
            raise ValueError("采样大小 k 必须大于 0")
        self._k = k
        self._reservoir: List[T] = []
        self._count = 0
        self._rng = random.Random(seed)
    
    def add(self, item: T) -> None:
        """
        添加一个元素到采样器
        
        Args:
            item: 待添加的元素
        """
        self._count += 1
        
        if self._count <= self._k:
            self._reservoir.append(item)
        else:
            # 以 k/n 的概率替换水库中的元素
            j = self._rng.randint(1, self._count)
            if j <= self._k:
                self._reservoir[j - 1] = item
    
    def add_all(self, items: Iterator[T]) -> None:
        """
        批量添加元素
        
        Args:
            items: 元素迭代器
        """
        for item in items:
            self.add(item)
    
    def sample(self) -> List[T]:
        """
        获取当前采样结果
        
        Returns:
            采样结果的列表（副本）
        """
        return list(self._reservoir)
    
    def reset(self, seed: Optional[int] = None) -> None:
        """
        重置采样器
        
        Args:
            seed: 新的随机种子
        """
        self._reservoir.clear()
        self._count = 0
        self._rng = random.Random(seed)
    
    @property
    def size(self) -> int:
        """采样大小"""
        return self._k
    
    @property
    def count(self) -> int:
        """已处理的元素数量"""
        return self._count
    
    @property
    def is_ready(self) -> bool:
        """是否已收集足够样本"""
        return len(self._reservoir) == self._k


class FastReservoirSampler(Generic[T]):
    """
    高效水库采样算法 (Algorithm L)
    
    由 Li (1994) 提出，比 Algorithm R 更高效。
    使用跳跃技术减少随机数生成次数。
    
    时间复杂度: O(n) 但实际操作更少
    空间复杂度: O(k)
    """
    
    def __init__(self, k: int, seed: Optional[int] = None):
        if k <= 0:
            raise ValueError("采样大小 k 必须大于 0")
        self._k = k
        self._reservoir: List[T] = []
        self._count = 0
        self._next_jump = 0
        self._rng = random.Random(seed)
        self._initialized = False
    
    def _compute_next_jump(self) -> int:
        """计算下一个跳跃距离"""
        u = self._rng.random()
        while u == 0:
            u = self._rng.random()
        
        # 使用几何分布计算跳跃距离
        n = self._count
        k = self._k
        
        # jump = floor(log(u) / log(1 - k/(n+1)))
        ratio = 1 - k / (n + 1)
        if ratio <= 0:
            return 1
        
        jump = int(math.log(u) / math.log(ratio))
        return max(1, jump)
    
    def add(self, item: T) -> None:
        """添加一个元素"""
        self._count += 1
        
        if self._count <= self._k:
            self._reservoir.append(item)
            if self._count == self._k:
                self._next_jump = self._compute_next_jump()
        else:
            if self._next_jump == 0:
                self._next_jump = self._compute_next_jump()
            
            self._next_jump -= 1
            
            if self._next_jump == 0:
                # 替换一个随机位置
                replace_idx = self._rng.randint(0, self._k - 1)
                self._reservoir[replace_idx] = item
                self._next_jump = self._compute_next_jump()
    
    def add_all(self, items: Iterator[T]) -> None:
        """批量添加元素"""
        for item in items:
            self.add(item)
    
    def sample(self) -> List[T]:
        """获取采样结果"""
        return list(self._reservoir)
    
    def reset(self, seed: Optional[int] = None) -> None:
        """重置采样器"""
        self._reservoir.clear()
        self._count = 0
        self._next_jump = 0
        self._rng = random.Random(seed)
        self._initialized = False
    
    @property
    def size(self) -> int:
        return self._k
    
    @property
    def count(self) -> int:
        return self._count


class WeightedReservoirSampler(Generic[T]):
    """
    加权水库采样 (Weighted Random Sampling)
    
    每个元素有对应的权重，采样概率与权重成正比。
    使用 Efraimidis & Spirakis (2006) 算法。
    
    示例:
        >>> sampler = WeightedReservoirSampler(2)
        >>> sampler.add('a', weight=1.0)
        >>> sampler.add('b', weight=2.0)
        >>> sampler.add('c', weight=3.0)
        >>> len(sampler.sample()) == 2
        True
    """
    
    def __init__(self, k: int, seed: Optional[int] = None):
        if k <= 0:
            raise ValueError("采样大小 k 必须大于 0")
        self._k = k
        self._weighted_items: List[Tuple[float, T]] = []
        self._rng = random.Random(seed)
    
    def add(self, item: T, weight: float) -> None:
        """
        添加带权重的元素
        
        Args:
            item: 元素
            weight: 权重（必须 > 0）
        """
        if weight <= 0:
            raise ValueError("权重必须大于 0")
        
        # 计算 key = r^(1/w)，其中 r 是 (0,1] 上的随机数
        r = self._rng.random()
        while r == 0:
            r = self._rng.random()
        
        key = math.pow(r, 1.0 / weight)
        
        if len(self._weighted_items) < self._k:
            self._weighted_items.append((key, item))
            self._weighted_items.sort(reverse=True)
        else:
            # 如果新 key 大于最小 key，替换
            if key > self._weighted_items[-1][0]:
                self._weighted_items[-1] = (key, item)
                self._weighted_items.sort(reverse=True)
    
    def add_all(self, items: Iterator[Tuple[T, float]]) -> None:
        """
        批量添加带权重的元素
        
        Args:
            items: (元素, 权重) 元组迭代器
        """
        for item, weight in items:
            self.add(item, weight)
    
    def sample(self) -> List[T]:
        """获取采样结果"""
        return [item for _, item in self._weighted_items]
    
    def reset(self, seed: Optional[int] = None) -> None:
        """重置采样器"""
        self._weighted_items.clear()
        self._rng = random.Random(seed)
    
    @property
    def size(self) -> int:
        return self._k
    
    @property
    def count(self) -> int:
        return len(self._weighted_items)


class ReservoirSamplerWithReplacement(Generic[T]):
    """
    有放回水库采样
    
    每个位置独立采样，允许重复元素。
    适用于需要独立采样的场景。
    """
    
    def __init__(self, k: int, seed: Optional[int] = None):
        if k <= 0:
            raise ValueError("采样大小 k 必须大于 0")
        self._k = k
        self._samples: List[Optional[T]] = [None] * k
        self._count = 0
        self._rng = random.Random(seed)
    
    def add(self, item: T) -> None:
        """添加一个元素"""
        self._count += 1
        
        if self._count <= self._k:
            # 初始填充阶段：前 k 个元素直接放入
            self._samples[self._count - 1] = item
        else:
            # 对每个采样位置独立决定是否替换
            for i in range(self._k):
                if self._rng.random() < 1.0 / self._count:
                    self._samples[i] = item
    
    def add_all(self, items: Iterator[T]) -> None:
        """
        批量添加元素
        
        Args:
            items: 元素迭代器
        """
        for item in items:
            self.add(item)
    
    def sample(self) -> List[T]:
        """获取采样结果"""
        return [s for s in self._samples if s is not None]
    
    def reset(self, seed: Optional[int] = None) -> None:
        """重置采样器"""
        self._samples = [None] * self._k
        self._count = 0
        self._rng = random.Random(seed)
    
    @property
    def size(self) -> int:
        return self._k
    
    @property
    def count(self) -> int:
        return self._count


@dataclass
class SamplingStats:
    """采样统计信息"""
    total_items: int
    sample_size: int
    unique_items: int
    duplicates: int
    
    def to_dict(self) -> dict:
        return {
            'total_items': self.total_items,
            'sample_size': self.sample_size,
            'unique_items': self.unique_items,
            'duplicates': self.duplicates
        }


def analyze_sample_distribution(sample: List[Any]) -> dict:
    """
    分析采样结果的分布
    
    Args:
        sample: 采样结果列表
    
    Returns:
        分布统计字典
    """
    if not sample:
        return {'empty': True}
    
    counts = defaultdict(int)
    for item in sample:
        key = str(item) if not isinstance(item, (int, float, str, tuple)) else item
        counts[key] += 1
    
    unique = len(counts)
    total = len(sample)
    duplicates = total - unique
    max_count = max(counts.values())
    min_count = min(counts.values())
    
    return {
        'total': total,
        'unique': unique,
        'duplicates': duplicates,
        'duplicate_ratio': duplicates / total if total > 0 else 0,
        'max_frequency': max_count,
        'min_frequency': min_count,
        'frequency_std': math.sqrt(sum((c - total/unique)**2 for c in counts.values()) / unique) if unique > 0 else 0
    }


def stratified_reservoir_sample(
    items: Iterator[T],
    k: int,
    strata_func: Callable[[T], int],
    seed: Optional[int] = None
) -> dict:
    """
    分层水库采样
    
    每个层级独立进行水库采样，确保各层级都有代表性样本。
    
    Args:
        items: 元素迭代器
        k: 每层采样大小
        strata_func: 分层函数，返回元素的层级ID
        seed: 随机种子
    
    Returns:
        字典 {层级ID: [样本列表]}
    """
    rng = random.Random(seed)
    samplers: dict = defaultdict(lambda: ReservoirSampler(k, rng.randint(0, 2**31)))
    
    for item in items:
        stratum = strata_func(item)
        samplers[stratum].add(item)
    
    return {s: samplers[s].sample() for s in samplers}


def two_pass_reservoir_sample(
    items: List[T],
    k: int,
    seed: Optional[int] = None
) -> List[T]:
    """
    两遍扫描水库采样
    
    第一遍统计总数，第二遍进行采样。
    适用于可以多次迭代的数据。
    
    Args:
        items: 元素列表
        k: 采样大小
        seed: 随机种子
    
    Returns:
        采样结果
    """
    n = len(items)
    if n <= k:
        return list(items)
    
    rng = random.Random(seed)
    
    # Fisher-Yates 采样
    indices = list(range(n))
    for i in range(k):
        j = rng.randint(i, n - 1)
        indices[i], indices[j] = indices[j], indices[i]
    
    return [items[i] for i in indices[:k]]


# 便捷函数
def reservoir_sample(items: Iterator[T], k: int, seed: Optional[int] = None) -> List[T]:
    """
    从迭代器中采样的便捷函数
    
    Args:
        items: 元素迭代器
        k: 采样大小
        seed: 随机种子
    
    Returns:
        采样结果列表
    """
    sampler = ReservoirSampler(k, seed)
    sampler.add_all(items)
    return sampler.sample()


def weighted_sample(
    items: Iterator[Tuple[T, float]],
    k: int,
    seed: Optional[int] = None
) -> List[T]:
    """
    加权采样的便捷函数
    
    Args:
        items: (元素, 权重) 元组迭代器
        k: 采样大小
        seed: 随机种子
    
    Returns:
        采样结果列表
    """
    sampler = WeightedReservoirSampler(k, seed)
    sampler.add_all(items)
    return sampler.sample()