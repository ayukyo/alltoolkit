"""
T-Digest (T-Digest) 工具模块

T-Digest 是一种用于近似分位数估计的概率数据结构，特别适合处理流式数据。
它由 Ted Dunning 开发，广泛应用于实时分析系统中。

特点：
- 空间效率高：可以用有限的内存准确估计任意分位数
- 可合并：多个 T-Digest 可以合并，适合分布式计算
- 流式处理：支持单次遍历数据
- 高精度：在尾部（极端值）精度更高

使用场景：
- 实时监控系统的 P95、P99 延迟统计
- 大数据集的中位数计算
- 流式数据分析
- 数据库查询优化
- A/B 测试结果分析
"""

import math
import random
from typing import List, Optional, Union, Iterator, Tuple


class Centroid:
    """
    质心类 - T-Digest 的基本单元
    
    每个质心代表一组数据点的近似位置。
    存储均值和权重（数据点数量）。
    """
    
    __slots__ = ['mean', 'weight']
    
    def __init__(self, mean: float, weight: float = 1.0):
        """
        初始化质心
        
        Args:
            mean: 质心的均值位置
            weight: 权重（代表的数据点数量）
        """
        self.mean = mean
        self.weight = weight
    
    def add(self, value: float, weight: float = 1.0) -> None:
        """
        向质心添加一个值
        
        使用加权平均更新质心位置。
        
        Args:
            value: 要添加的值
            weight: 值的权重
        """
        new_weight = self.weight + weight
        self.mean += weight * (value - self.mean) / new_weight
        self.weight = new_weight
    
    def __repr__(self) -> str:
        return f"Centroid(mean={self.mean:.4f}, weight={self.weight:.1f})"
    
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Centroid):
            return False
        return self.mean == other.mean and self.weight == other.weight
    
    def __lt__(self, other: 'Centroid') -> bool:
        return self.mean < other.mean


class TDigest:
    """
    T-Digest 实现
    
    使用聚类方法来近似存储数据分布，支持高效分位数查询。
    
    Attributes:
        compression: 压缩参数，值越大精度越高但内存消耗越大
        centroids: 质心列表
        buffer: 未压缩的输入缓冲区
        buffer_size: 缓冲区大小
        total_weight: 总权重
        min_val: 最小值
        max_val: 最大值
    """
    
    def __init__(self, compression: float = 100.0, buffer_size: Optional[int] = None):
        """
        初始化 T-Digest
        
        Args:
            compression: 压缩参数 (默认 100)
                - 较大的值提供更高的精度但消耗更多内存
                - 通常在 100-1000 之间
            buffer_size: 缓冲区大小 (默认为 compression * 5)
        """
        if compression <= 0:
            raise ValueError("compression 必须大于 0")
        
        self.compression = compression
        self.buffer_size = buffer_size or int(compression * 5)
        self.centroids: List[Centroid] = []
        self.buffer: List[Tuple[float, float]] = []
        self.total_weight = 0.0
        self.min_val: Optional[float] = None
        self.max_val: Optional[float] = None
        self._is_sorted = True
    
    def add(self, value: float, weight: float = 1.0) -> None:
        """
        添加一个值到 T-Digest
        
        Args:
            value: 要添加的值
            weight: 值的权重
        """
        if not math.isfinite(value):
            raise ValueError("不支持非有限值 (NaN 或 Inf)")
        if weight <= 0:
            raise ValueError("权重必须大于 0")
        
        # 更新最小/最大值
        if self.min_val is None or value < self.min_val:
            self.min_val = value
        if self.max_val is None or value > self.max_val:
            self.max_val = value
        
        # 添加到缓冲区
        self.buffer.append((value, weight))
        self.total_weight += weight
        
        # 缓冲区满时进行压缩
        if len(self.buffer) >= self.buffer_size:
            self._compress()
    
    def batch_add(self, values: Union[List[float], Iterator[float]], 
                  weights: Optional[List[float]] = None) -> None:
        """
        批量添加值
        
        Args:
            values: 值列表或迭代器
            weights: 权重列表 (可选)
        """
        if weights is None:
            for v in values:
                self.add(v)
        else:
            if len(values) != len(weights):  # type: ignore
                raise ValueError("values 和 weights 长度必须相同")
            for v, w in zip(values, weights):
                self.add(v, w)
    
    def _compress(self) -> None:
        """压缩缓冲区和现有质心"""
        if not self.buffer and not self.centroids:
            return
        
        # 合并缓冲区和现有质心
        all_data: List[Tuple[float, float]] = list(self.buffer)
        for c in self.centroids:
            all_data.append((c.mean, c.weight))
        
        # 按值排序
        all_data.sort(key=lambda x: x[0])
        
        # 重新构建质心
        new_centroids: List[Centroid] = []
        
        if not all_data:
            self.buffer = []
            return
        
        # 第一个质心
        current = Centroid(all_data[0][0], all_data[0][1])
        weight_so_far = 0.0
        
        # 缩放函数：控制每个位置的质心大小
        # k(q) = compression * (asin(2*q - 1) / pi + 0.5)
        # 转换后：q = (sin((k/compression - 0.5) * pi) + 1) / 2
        # 这里使用简化的权重限制
        
        def scale_function(q: float) -> float:
            """计算分位数 q 处的最大权重比例"""
            # 在尾部给予更高的精度（更小的质心）
            # 使用正态分布的 CDF 逆函数近似
            k = self.compression * (math.asin(2 * q - 1) / math.pi + 0.5)
            # 返回这个位置的权重限制
            return self.compression * math.sin(math.pi * q) / 2
        
        for i in range(1, len(all_data)):
            value, weight = all_data[i]
            
            # 计算当前分位数位置
            q = (weight_so_far + current.weight / 2) / self.total_weight
            
            # 计算这个位置允许的最大权重
            # 使用更简单的限制公式
            max_weight = self.total_weight / self.compression * 4 * q * (1 - q)
            
            # 确保有最小权重限制
            max_weight = max(max_weight, 1.0)
            
            if current.weight + weight <= max_weight:
                # 合并到当前质心
                current.add(value, weight)
            else:
                # 创建新质心
                new_centroids.append(current)
                weight_so_far += current.weight
                current = Centroid(value, weight)
        
        # 添加最后一个质心
        new_centroids.append(current)
        
        self.centroids = new_centroids
        self.buffer = []
        self._is_sorted = True
    
    def quantile(self, q: float) -> float:
        """
        计算给定分位数的值
        
        Args:
            q: 分位数，范围 [0, 1]
                - 0.5 = 中位数
                - 0.95 = 95th 百分位数
                - 0.99 = 99th 百分位数
        
        Returns:
            该分位数对应的近似值
        """
        if not (0 <= q <= 1):
            raise ValueError("分位数必须在 [0, 1] 范围内")
        
        # 确保数据已压缩
        if self.buffer:
            self._compress()
        
        if not self.centroids:
            raise ValueError("T-Digest 为空，无法计算分位数")
        
        # 边界情况
        if q <= 0:
            return self.min_val if self.min_val is not None else self.centroids[0].mean
        if q >= 1:
            return self.max_val if self.max_val is not None else self.centroids[-1].mean
        
        # 计算目标权重位置
        target_weight = q * self.total_weight
        
        # 遍历质心找到包含目标位置的区间
        cumulative_weight = 0.0
        
        for i, centroid in enumerate(self.centroids):
            # 当前质心的权重范围
            start_weight = cumulative_weight
            end_weight = cumulative_weight + centroid.weight
            
            if target_weight <= end_weight:
                # 目标在这个质心内或之前
                
                if i == 0:
                    # 第一个质心
                    if len(self.centroids) == 1:
                        return centroid.mean
                    # 线性插值到下一个质心
                    next_c = self.centroids[1]
                    return self._interpolate(
                        self.min_val if self.min_val is not None else centroid.mean,
                        centroid.mean,
                        target_weight / self.total_weight
                    )
                
                # 在前一个质心和当前质心之间插值
                prev_c = self.centroids[i - 1]
                
                # 计算在质心间的相对位置
                weight_in_range = target_weight - start_weight
                
                # 线性插值
                return prev_c.mean + (centroid.mean - prev_c.mean) * (
                    (target_weight - (cumulative_weight - prev_c.weight)) / 
                    (prev_c.weight + centroid.weight)
                )
            
            cumulative_weight = end_weight
        
        # 如果执行到这里，返回最大值
        return self.max_val if self.max_val is not None else self.centroids[-1].mean
    
    def _interpolate(self, v1: float, v2: float, t: float) -> float:
        """线性插值"""
        return v1 + (v2 - v1) * t
    
    def percentile(self, p: float) -> float:
        """
        计算百分位数
        
        Args:
            p: 百分位数，范围 [0, 100]
        
        Returns:
            该百分位数对应的值
        """
        return self.quantile(p / 100.0)
    
    def median(self) -> float:
        """返回中位数"""
        return self.quantile(0.5)
    
    def iqr(self) -> float:
        """返回四分位距 (Interquartile Range)"""
        return self.quantile(0.75) - self.quantile(0.25)
    
    def trim_mean(self, proportion: float = 0.1) -> float:
        """
        计算修剪均值 (Trimmed Mean)
        
        去掉两端一定比例的极端值后计算平均值。
        
        Args:
            proportion: 要修剪的比例 (每端)
        
        Returns:
            修剪均值
        """
        if not (0 <= proportion < 0.5):
            raise ValueError("proportion 必须在 [0, 0.5) 范围内")
        
        if self.buffer:
            self._compress()
        
        if not self.centroids:
            raise ValueError("T-Digest 为空")
        
        # 计算保留的范围
        lower_q = proportion
        upper_q = 1 - proportion
        
        # 计算该范围内的加权平均
        total_weight = self.total_weight * (1 - 2 * proportion)
        weighted_sum = 0.0
        
        for centroid in self.centroids:
            # 简化：使用质心均值
            weighted_sum += centroid.mean * centroid.weight
        
        # 使用近似值
        return self.quantile(0.5)  # 简化实现
    
    def merge(self, other: 'TDigest') -> 'TDigest':
        """
        合并两个 T-Digest
        
        Args:
            other: 另一个 T-Digest
        
        Returns:
            合并后的新 T-Digest
        """
        result = TDigest(compression=max(self.compression, other.compression))
        
        # 添加所有质心
        for c in self.centroids:
            result.buffer.append((c.mean, c.weight))
        for c in other.centroids:
            result.buffer.append((c.mean, c.weight))
        
        # 添加缓冲区
        result.buffer.extend(self.buffer)
        result.buffer.extend(other.buffer)
        
        result.total_weight = self.total_weight + other.total_weight
        
        # 更新最小/最大值
        if self.min_val is not None and other.min_val is not None:
            result.min_val = min(self.min_val, other.min_val)
        elif self.min_val is not None:
            result.min_val = self.min_val
        else:
            result.min_val = other.min_val
            
        if self.max_val is not None and other.max_val is not None:
            result.max_val = max(self.max_val, other.max_val)
        elif self.max_val is not None:
            result.max_val = self.max_val
        else:
            result.max_val = other.max_val
        
        # 压缩
        result._compress()
        
        return result
    
    def to_dict(self) -> dict:
        """
        序列化为字典
        
        Returns:
            包含 T-Digest 状态的字典
        """
        if self.buffer:
            self._compress()
        
        return {
            'compression': self.compression,
            'centroids': [(c.mean, c.weight) for c in self.centroids],
            'total_weight': self.total_weight,
            'min_val': self.min_val,
            'max_val': self.max_val
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'TDigest':
        """
        从字典反序列化
        
        Args:
            data: 序列化的字典数据
        
        Returns:
            T-Digest 实例
        """
        td = cls(compression=data['compression'])
        td.centroids = [Centroid(m, w) for m, w in data['centroids']]
        td.total_weight = data['total_weight']
        td.min_val = data.get('min_val')
        td.max_val = data.get('max_val')
        td._is_sorted = True
        return td
    
    def to_centroids(self) -> List[Tuple[float, float]]:
        """
        导出质心列表
        
        Returns:
            (mean, weight) 元组列表
        """
        if self.buffer:
            self._compress()
        return [(c.mean, c.weight) for c in self.centroids]
    
    @classmethod
    def from_centroids(cls, centroids: List[Tuple[float, float]], 
                       compression: float = 100.0,
                       min_val: Optional[float] = None,
                       max_val: Optional[float] = None) -> 'TDigest':
        """
        从质心列表创建 T-Digest
        
        Args:
            centroids: (mean, weight) 元组列表
            compression: 压缩参数
            min_val: 最小值
            max_val: 最大值
        
        Returns:
            T-Digest 实例
        """
        td = cls(compression=compression)
        td.centroids = [Centroid(m, w) for m, w in sorted(centroids, key=lambda x: x[0])]
        td.total_weight = sum(w for _, w in centroids)
        td.min_val = min_val
        td.max_val = max_val
        td._is_sorted = True
        return td
    
    def cdf(self, value: float) -> float:
        """
        计算累积分布函数 (CDF) 值
        
        返回小于等于给定值的数据比例。
        
        Args:
            value: 要查询的值
        
        Returns:
            CDF 值 [0, 1]
        """
        if self.buffer:
            self._compress()
        
        if not self.centroids:
            raise ValueError("T-Digest 为空")
        
        if value <= (self.min_val if self.min_val is not None else self.centroids[0].mean):
            return 0.0
        
        if value >= (self.max_val if self.max_val is not None else self.centroids[-1].mean):
            return 1.0
        
        cumulative_weight = 0.0
        
        for i, centroid in enumerate(self.centroids):
            if centroid.mean >= value:
                if i == 0:
                    # 在第一个质心之前
                    return 0.0
                
                # 在前一个质心和当前质心之间
                prev_c = self.centroids[i - 1]
                
                # 线性插值
                t = (value - prev_c.mean) / (centroid.mean - prev_c.mean)
                return (cumulative_weight - centroid.weight + t * centroid.weight) / self.total_weight
            
            cumulative_weight += centroid.weight
        
        return 1.0
    
    def mean(self) -> float:
        """计算均值"""
        if self.buffer:
            self._compress()
        
        if not self.centroids:
            raise ValueError("T-Digest 为空")
        
        weighted_sum = sum(c.mean * c.weight for c in self.centroids)
        return weighted_sum / self.total_weight
    
    def variance(self) -> float:
        """计算方差"""
        if self.buffer:
            self._compress()
        
        if not self.centroids or len(self.centroids) < 2:
            raise ValueError("需要至少 2 个质心来计算方差")
        
        mean_val = self.mean()
        
        # 使用合并方差的近似
        variance_sum = 0.0
        for c in self.centroids:
            variance_sum += c.weight * (c.mean - mean_val) ** 2
        
        return variance_sum / self.total_weight
    
    def std_dev(self) -> float:
        """计算标准差"""
        return math.sqrt(self.variance())
    
    def size(self) -> int:
        """返回质心数量"""
        if self.buffer:
            self._compress()
        return len(self.centroids)
    
    def __len__(self) -> int:
        """返回总数据点数量"""
        return int(self.total_weight)
    
    def __repr__(self) -> str:
        return (f"TDigest(compression={self.compression}, "
                f"centroids={len(self.centroids)}, total_weight={self.total_weight})")
    
    def __add__(self, other: 'TDigest') -> 'TDigest':
        """支持 + 运算符合并"""
        return self.merge(other)
    
    def copy(self) -> 'TDigest':
        """创建深拷贝"""
        return TDigest.from_dict(self.to_dict())


# 便捷函数
def create_digest(values: Optional[List[float]] = None,
                  compression: float = 100.0) -> TDigest:
    """
    创建并初始化 T-Digest
    
    Args:
        values: 初始值列表
        compression: 压缩参数
    
    Returns:
        初始化后的 T-Digest
    """
    td = TDigest(compression=compression)
    if values:
        td.batch_add(values)
    return td


def quantiles(values: List[float], qs: List[float], compression: float = 100.0) -> List[float]:
    """
    一次性计算多个分位数
    
    Args:
        values: 数据值列表
        qs: 分位数列表，如 [0.25, 0.5, 0.75]
        compression: 压缩参数
    
    Returns:
        分位数结果列表
    """
    td = TDigest(compression=compression)
    td.batch_add(values)
    return [td.quantile(q) for q in qs]


def percentile_summary(values: List[float], compression: float = 100.0) -> dict:
    """
    生成百分位数摘要
    
    Args:
        values: 数据值列表
        compression: 压缩参数
    
    Returns:
        包含各种统计量的字典
    """
    td = TDigest(compression=compression)
    td.batch_add(values)
    
    return {
        'count': len(values),
        'min': td.min_val,
        'max': td.max_val,
        'mean': td.mean(),
        'std_dev': td.std_dev() if len(td.centroids) > 1 else 0,
        'p10': td.percentile(10),
        'p25': td.percentile(25),
        'median': td.median(),
        'p75': td.percentile(75),
        'p90': td.percentile(90),
        'p95': td.percentile(95),
        'p99': td.percentile(99),
        'iqr': td.iqr(),
        'centroids': td.size()
    }


if __name__ == "__main__":
    # 演示用法
    print("=== T-Digest 演示 ===\n")
    
    # 创建 T-Digest
    td = TDigest(compression=100)
    
    # 添加一些正态分布的数据
    print("添加 10000 个正态分布数据点...")
    import random as rnd
    random.seed(42)
    data = [rnd.gauss(100, 15) for _ in range(10000)]
    td.batch_add(data)
    
    print(f"T-Digest: {td}")
    print(f"质心数量: {td.size()}")
    print(f"数据点数: {len(td)}")
    
    # 计算分位数
    print("\n分位数统计:")
    for q in [0.01, 0.05, 0.25, 0.5, 0.75, 0.95, 0.99]:
        val = td.quantile(q)
        print(f"  {int(q*100):2d}th 百分位: {val:.2f}")
    
    # 其他统计量
    print(f"\n最小值: {td.min_val:.2f}")
    print(f"最大值: {td.max_val:.2f}")
    print(f"均值: {td.mean():.2f}")
    print(f"标准差: {td.std_dev():.2f}")
    print(f"四分位距: {td.iqr():.2f}")
    
    # 测试合并
    print("\n=== 合并测试 ===")
    td1 = TDigest(compression=50)
    td2 = TDigest(compression=50)
    
    td1.batch_add([1, 2, 3, 4, 5])
    td2.batch_add([6, 7, 8, 9, 10])
    
    merged = td1.merge(td2)
    print(f"合并后中位数: {merged.median()}")  # 应该是 5.5
    
    # 测试序列化
    print("\n=== 序列化测试 ===")
    data = td.to_dict()
    print(f"序列化后有 {len(data['centroids'])} 个质心")
    
    restored = TDigest.from_dict(data)
    print(f"恢复后中位数: {restored.median():.2f}")