"""
Count-Min Sketch 工具模块

Count-Min Sketch 是一种概率数据结构，用于估计数据流中元素的频率。
它使用固定的内存空间，提供 O(1) 的更新和查询操作。

特点:
- 空间效率高：使用固定的内存空间
- 时间效率高：O(1) 的更新和查询
- 可合并：多个 sketch 可以合并
- 支持多种哈希函数

应用场景:
- 网络流量分析（Top-K 元素）
- 热点检测
- 频繁项集挖掘
- 流式数据处理
- 大数据近似统计

作者: AllToolkit
日期: 2026-04-19
"""

import hashlib
import math
from typing import Callable, List, Optional, Union, Any
import json


class CountMinSketch:
    """
    Count-Min Sketch 数据结构实现
    
    用于估计元素在数据流中出现频率的概率数据结构。
    提供上界估计，误差取决于宽度参数。
    
    示例:
        >>> cms = CountMinSketch(width=1000, depth=5)
        >>> cms.add("hello")
        >>> cms.add("hello")
        >>> cms.estimate("hello")
        2
        >>> cms.estimate("world")
        0
    """
    
    def __init__(
        self,
        width: int = 1000,
        depth: int = 5,
        seed: int = 42,
        hash_func: Optional[Callable[[bytes], int]] = None
    ):
        """
        初始化 Count-Min Sketch
        
        参数:
            width: 每行的宽度（桶数），影响误差范围
            depth: 行数（哈希函数数），影响置信度
            seed: 随机种子，用于生成不同的哈希函数
            hash_func: 自定义哈希函数，默认使用 MurmurHash3 风格的哈希
        """
        if width <= 0 or depth <= 0:
            raise ValueError("width 和 depth 必须为正整数")
        
        self._width = width
        self._depth = depth
        self._seed = seed
        self._hash_func = hash_func
        self._count = 0  # 总元素计数
        self._matrix: List[List[int]] = [[0] * width for _ in range(depth)]
        
        # 预计算每行的哈希种子
        self._seeds = [seed + i * 31 for i in range(depth)]
    
    @property
    def width(self) -> int:
        """返回每行的宽度"""
        return self._width
    
    @property
    def depth(self) -> int:
        """返回行数"""
        return self._depth
    
    @property
    def total_count(self) -> int:
        """返回已添加的元素总数"""
        return self._count
    
    @property
    def memory_usage(self) -> int:
        """返回内存使用量（字节数）"""
        return self._width * self._depth * 8  # 假设 int 为 8 字节
    
    def _hash(self, item: Any, row: int) -> int:
        """
        计算元素在第 row 行的哈希值
        
        使用双哈希技术生成多个独立的哈希函数
        """
        # 将元素转换为字节
        if isinstance(item, bytes):
            data = item
        elif isinstance(item, str):
            data = item.encode('utf-8')
        else:
            data = str(item).encode('utf-8')
        
        if self._hash_func:
            return self._hash_func(data) % self._width
        
        # 使用 MurmurHash3 风格的哈希
        h = self._seeds[row]
        
        # 双哈希技术
        h1 = int(hashlib.md5(data + bytes([row])).hexdigest(), 16)
        h2 = int(hashlib.sha1(data + bytes([row])).hexdigest(), 16)
        
        return (h1 + row * h2) % self._width
    
    def add(self, item: Any, count: int = 1) -> int:
        """
        添加元素到 sketch
        
        参数:
            item: 要添加的元素
            count: 添加的次数（默认 1）
        
        返回:
            添加后该元素的估计频率（上界）
        
        示例:
            >>> cms = CountMinSketch(100, 5)
            >>> cms.add("apple", 3)
            3
        """
        if count < 0:
            raise ValueError("count 不能为负数")
        
        min_count = float('inf')
        for i in range(self._depth):
            idx = self._hash(item, i)
            self._matrix[i][idx] += count
            min_count = min(min_count, self._matrix[i][idx])
        
        self._count += count
        return min_count
    
    def estimate(self, item: Any) -> int:
        """
        估计元素的频率
        
        返回元素出现次数的上界估计。
        
        参数:
            item: 要查询的元素
        
        返回:
            估计的出现次数
        
        示例:
            >>> cms = CountMinSketch(100, 5)
            >>> cms.add("apple", 5)
            5
            >>> cms.estimate("apple")
            5
        """
        min_count = float('inf')
        for i in range(self._depth):
            idx = self._hash(item, i)
            min_count = min(min_count, self._matrix[i][idx])
        return min_count
    
    def estimate_error(self, confidence: float = 0.95) -> float:
        """
        计算误差范围
        
        参数:
            confidence: 置信度 (0-1)
        
        返回:
            误差范围 ε，真实值在 [估计值 - ε, 估计值] 的概率为 confidence
        """
        # ε = e * n，其中 n 是总元素数，e = e / width
        epsilon = 2.718281828 / self._width  # 自然常数 e / width
        return epsilon * self._count
    
    def heavy_hitters(self, threshold: float) -> List[Any]:
        """
        查找频繁元素（需要配合外部候选集使用）
        
        注意：Count-Min Sketch 本身不支持直接枚举元素，
        此方法需要提供一个候选集来检查。
        
        参数:
            threshold: 频率阈值（占总数的比例）
        
        返回:
            空列表（需要使用 check_heavy_hitters 方法）
        """
        return []
    
    def check_heavy_hitters(self, candidates: List[Any], threshold: float) -> List[tuple]:
        """
        从候选集中筛选频繁元素
        
        参数:
            candidates: 候选元素列表
            threshold: 频率阈值（占总数的比例，0-1）
        
        返回:
            超过阈值的元素及其估计频率列表 [(item, count), ...]
        
        示例:
            >>> cms = CountMinSketch(100, 5)
            >>> for i in range(100):
            ...     cms.add("a")
            >>> for i in range(50):
            ...     cms.add("b")
            >>> cms.check_heavy_hitters(["a", "b", "c"], 0.3)
            [('a', 100), ('b', 50)]
        """
        if threshold <= 0 or threshold > 1:
            raise ValueError("threshold 必须在 (0, 1] 范围内")
        
        min_count = int(self._count * threshold)
        result = []
        
        for item in candidates:
            est = self.estimate(item)
            if est >= min_count:
                result.append((item, est))
        
        return sorted(result, key=lambda x: -x[1])
    
    def merge(self, other: 'CountMinSketch') -> 'CountMinSketch':
        """
        合并两个 Count-Min Sketch
        
        参数:
            other: 另一个 Count-Min Sketch
        
        返回:
            合并后的新 Count-Min Sketch
        
        注意:
            两个 sketch 必须有相同的 width 和 depth
        
        示例:
            >>> cms1 = CountMinSketch(100, 5)
            >>> cms2 = CountMinSketch(100, 5)
            >>> cms1.add("a", 10)
            10
            >>> cms2.add("a", 5)
            5
            >>> merged = cms1.merge(cms2)
            >>> merged.estimate("a")
            15
        """
        if self._width != other._width or self._depth != other._depth:
            raise ValueError("只能合并相同参数的 Count-Min Sketch")
        
        result = CountMinSketch(self._width, self._depth, self._seed)
        result._count = self._count + other._count
        
        for i in range(self._depth):
            for j in range(self._width):
                result._matrix[i][j] = self._matrix[i][j] + other._matrix[i][j]
        
        return result
    
    def clear(self) -> None:
        """清空 sketch"""
        self._matrix = [[0] * self._width for _ in range(self._depth)]
        self._count = 0
    
    def __contains__(self, item: Any) -> bool:
        """检查元素是否存在（估计频率 > 0）"""
        return self.estimate(item) > 0
    
    def __len__(self) -> int:
        """返回总元素计数"""
        return self._count
    
    def __repr__(self) -> str:
        return f"CountMinSketch(width={self._width}, depth={self._depth}, count={self._count})"
    
    def to_dict(self) -> dict:
        """转换为字典以便序列化"""
        return {
            'width': self._width,
            'depth': self._depth,
            'seed': self._seed,
            'count': self._count,
            'matrix': self._matrix
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'CountMinSketch':
        """从字典恢复 Count-Min Sketch"""
        cms = cls(width=data['width'], depth=data['depth'], seed=data['seed'])
        cms._count = data['count']
        cms._matrix = data['matrix']
        return cms
    
    def to_json(self) -> str:
        """转换为 JSON 字符串"""
        return json.dumps(self.to_dict())
    
    @classmethod
    def from_json(cls, json_str: str) -> 'CountMinSketch':
        """从 JSON 字符串恢复"""
        return cls.from_dict(json.loads(json_str))


class CountMinSketchBuilder:
    """
    Count-Min Sketch 构建器
    
    根据期望的误差和置信度自动计算最优参数。
    
    示例:
        >>> builder = CountMinSketchBuilder()
        >>> builder.with_error_rate(0.01).with_confidence(0.99)
        >>> cms = builder.build()
    """
    
    def __init__(self):
        self._error_rate: float = 0.01  # 误差率 ε
        self._confidence: float = 0.95   # 置信度
        self._seed: int = 42
    
    def with_error_rate(self, error_rate: float) -> 'CountMinSketchBuilder':
        """
        设置期望误差率
        
        参数:
            error_rate: 误差率 (0-1)，越小越精确但占用更多内存
        
        返回:
            self
        """
        if error_rate <= 0 or error_rate >= 1:
            raise ValueError("error_rate 必须在 (0, 1) 范围内")
        self._error_rate = error_rate
        return self
    
    def with_confidence(self, confidence: float) -> 'CountMinSketchBuilder':
        """
        设置置信度
        
        参数:
            confidence: 置信度 (0-1)，越大越可靠
        
        返回:
            self
        """
        if confidence <= 0 or confidence >= 1:
            raise ValueError("confidence 必须在 (0, 1) 范围内")
        self._confidence = confidence
        return self
    
    def with_seed(self, seed: int) -> 'CountMinSketchBuilder':
        """设置随机种子"""
        self._seed = seed
        return self
    
    def build(self) -> CountMinSketch:
        """
        构建 Count-Min Sketch
        
        根据 error_rate 和 confidence 自动计算最优的 width 和 depth
        
        width = e / ε
        depth = ln(1 / (1 - confidence))
        """
        import math
        
        # width = e / error_rate (e 是自然常数)
        width = int(math.ceil(2.718281828 / self._error_rate))
        
        # depth = ln(1 / (1 - confidence)) = -ln(1 - confidence)
        depth = int(math.ceil(-math.log(1 - self._confidence)))
        
        return CountMinSketch(width=width, depth=depth, seed=self._seed)


class TopKTracker:
    """
    Top-K 频繁元素追踪器
    
    结合 Count-Min Sketch 和最小堆来追踪数据流中的 Top-K 元素。
    
    示例:
        >>> tracker = TopKTracker(k=5)
        >>> for word in ["a", "b", "a", "c", "a", "b", "d"]:
        ...     tracker.add(word)
        >>> tracker.get_top_k()
        [('a', 3), ('b', 2), ('c', 1), ('d', 1)]
    """
    
    def __init__(self, k: int = 10, sketch_width: int = 1000, sketch_depth: int = 5):
        """
        初始化 Top-K 追踪器
        
        参数:
            k: 追踪的 Top-K 数量
            sketch_width: Count-Min Sketch 的宽度
            sketch_depth: Count-Min Sketch 的深度
        """
        if k <= 0:
            raise ValueError("k 必须为正整数")
        
        self._k = k
        self._cms = CountMinSketch(width=sketch_width, depth=sketch_depth)
        self._candidates: dict = {}  # 候选集：{item: estimated_count}
    
    @property
    def k(self) -> int:
        return self._k
    
    @property
    def total_count(self) -> int:
        return self._cms.total_count
    
    def add(self, item: Any, count: int = 1) -> None:
        """
        添加元素
        
        参数:
            item: 元素
            count: 添加次数
        """
        self._cms.add(item, count)
        
        # 如果已在候选集中，更新
        if item in self._candidates:
            self._candidates[item] = self._cms.estimate(item)
        else:
            # 如果候选集未满，添加
            if len(self._candidates) < self._k:
                self._candidates[item] = self._cms.estimate(item)
            else:
                # 找出最小元素，如果新元素可能更大，则替换
                min_item = min(self._candidates, key=self._candidates.get)
                new_estimate = self._cms.estimate(item)
                if new_estimate > self._candidates[min_item]:
                    del self._candidates[min_item]
                    self._candidates[item] = new_estimate
    
    def estimate(self, item: Any) -> int:
        """估计元素频率"""
        if item in self._candidates:
            return self._candidates[item]
        return self._cms.estimate(item)
    
    def get_top_k(self) -> List[tuple]:
        """
        获取 Top-K 元素
        
        返回:
            按频率降序排列的 [(item, count), ...] 列表
        """
        return sorted(self._candidates.items(), key=lambda x: -x[1])
    
    def clear(self) -> None:
        """清空追踪器"""
        self._cms.clear()
        self._candidates.clear()
    
    def __repr__(self) -> str:
        top = self.get_top_k()[:3]
        top_str = ", ".join(f"('{k}', {v})" for k, v in top)
        return f"TopKTracker(k={self._k}, top=[{top_str}...])"


def create_optimal_sketch(
    expected_items: int,
    max_error: float = 0.01,
    confidence: float = 0.95
) -> CountMinSketch:
    """
    创建最优参数的 Count-Min Sketch
    
    参数:
        expected_items: 预期元素数量
        max_error: 最大相对误差
        confidence: 置信度
    
    返回:
        配置好的 CountMinSketch 实例
    
    示例:
        >>> cms = create_optimal_sketch(expected_items=1000000, max_error=0.001)
        >>> cms.width, cms.depth
        (2719, 3)
    """
    # 误差参数：ε = max_error / expected_items
    error_rate = max_error
    
    builder = CountMinSketchBuilder()
    builder.with_error_rate(error_rate).with_confidence(confidence)
    
    return builder.build()


def frequency_analysis(
    items: List[Any],
    width: int = 1000,
    depth: int = 5,
    threshold: Optional[float] = None,
    top_k: Optional[int] = None
) -> dict:
    """
    对数据列表进行频率分析
    
    参数:
        items: 数据列表
        width: Count-Min Sketch 宽度
        depth: Count-Min Sketch 深度
        threshold: 频率阈值（可选）
        top_k: 返回前 K 个（可选）
    
    返回:
        包含统计信息的字典
    
    示例:
        >>> items = ["a", "b", "a", "c", "a", "b"]
        >>> result = frequency_analysis(items)
        >>> result['unique_estimate']
        3
    """
    cms = CountMinSketch(width=width, depth=depth)
    seen = set()
    
    for item in items:
        cms.add(item)
        seen.add(item)
    
    result = {
        'total_count': cms.total_count,
        'unique_count': len(seen),  # Count-Min Sketch 不支持精确计数
        'sketch': cms,
        'error_bound': cms.estimate_error()
    }
    
    if threshold and seen:
        result['heavy_hitters'] = cms.check_heavy_hitters(list(seen), threshold)
    
    if top_k:
        tracker = TopKTracker(k=top_k, sketch_width=width, sketch_depth=depth)
        for item in items:
            tracker.add(item)
        result['top_k'] = tracker.get_top_k()
    
    return result


# 便捷函数
def count_min_sketch(width: int = 1000, depth: int = 5, seed: int = 42) -> CountMinSketch:
    """创建 Count-Min Sketch 的便捷函数"""
    return CountMinSketch(width=width, depth=depth, seed=seed)


if __name__ == "__main__":
    # 简单演示
    print("Count-Min Sketch 示例")
    print("=" * 50)
    
    # 创建 sketch
    cms = CountMinSketch(width=1000, depth=5)
    
    # 添加一些元素
    for _ in range(100):
        cms.add("apple")
    for _ in range(50):
        cms.add("banana")
    for _ in range(25):
        cms.add("cherry")
    
    # 查询频率
    print(f"apple: {cms.estimate('apple')}")   # 应该接近 100
    print(f"banana: {cms.estimate('banana')}") # 应该接近 50
    print(f"cherry: {cms.estimate('cherry')}")  # 应该接近 25
    print(f"grape: {cms.estimate('grape')}")    # 应该为 0
    
    print(f"\n总计数: {cms.total_count}")
    print(f"内存使用: {cms.memory_usage} 字节")
    
    # 使用 Builder 创建最优 sketch
    print("\n使用 Builder 创建最优 sketch:")
    builder = CountMinSketchBuilder()
    builder.with_error_rate(0.01).with_confidence(0.99)
    optimal_cms = builder.build()
    print(f"width={optimal_cms.width}, depth={optimal_cms.depth}")
    
    # Top-K 追踪
    print("\nTop-K 追踪:")
    tracker = TopKTracker(k=3)
    words = ["a", "b", "a", "c", "a", "b", "d", "a", "b", "e"]
    for word in words:
        tracker.add(word)
    print(f"Top-3: {tracker.get_top_k()}")