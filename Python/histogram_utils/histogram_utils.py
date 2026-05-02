"""
Histogram Utils - 零依赖直方图生成工具

功能:
- 数值数据直方图生成
- 自动或手动设置分组数量
- 多种输出格式 (文本、ASCII 图、数据结构)
- 频率密度计算
- 累积频率计算
- 统计信息输出

作者: AllToolkit 自动生成
日期: 2026-05-02
"""

from typing import List, Dict, Tuple, Optional, Union
from collections import Counter
import math


class HistogramBin:
    """直方图单个分组"""
    
    def __init__(self, lower: float, upper: float, count: int):
        self.lower = lower
        self.upper = upper
        self.count = count
        self.width = upper - lower
    
    @property
    def frequency(self) -> float:
        """频率 (相对频率)"""
        return self.count
    
    @property
    def midpoint(self) -> float:
        """组中值"""
        return (self.lower + self.upper) / 2
    
    def __repr__(self) -> str:
        return f"HistogramBin([{self.lower:.2f}, {self.upper:.2f}), count={self.count})"


class Histogram:
    """直方图生成器"""
    
    def __init__(self, data: List[float], bins: Optional[int] = None,
                 bin_width: Optional[float] = None,
                 range_min: Optional[float] = None,
                 range_max: Optional[float] = None):
        """
        初始化直方图
        
        Args:
            data: 数值数据列表
            bins: 分组数量 (自动计算若为 None)
            bin_width: 分组宽度 (优先于 bins)
            range_min: 数据范围最小值
            range_max: 数据范围最大值
        """
        if not data:
            raise ValueError("数据不能为空")
        
        self.data = data
        self._bins: List[HistogramBin] = []
        self._total_count = len(data)
        
        # 计算范围
        self.min_val = range_min if range_min is not None else min(data)
        self.max_val = range_max if range_max is not None else max(data)
        
        # 范围必须包含所有数据
        actual_min = min(data)
        actual_max = max(data)
        if self.min_val > actual_min:
            self.min_val = actual_min
        if self.max_val < actual_max:
            self.max_val = actual_max
        
        # 计算分组
        if bin_width is not None:
            self.bin_width = bin_width
            self.num_bins = int(math.ceil((self.max_val - self.min_val) / bin_width))
        elif bins is not None:
            self.num_bins = bins
            self.bin_width = (self.max_val - self.min_val) / bins
        else:
            # 自动计算分组数 (使用 Sturges 规则)
            self.num_bins = self._sturges_bins()
            self.bin_width = (self.max_val - self.min_val) / self.num_bins
        
        # 确保至少有一个分组
        if self.num_bins < 1:
            self.num_bins = 1
            self.bin_width = self.max_val - self.min_val
            if self.bin_width == 0:
                self.bin_width = 1
        
        self._build_histogram()
    
    def _sturges_bins(self) -> int:
        """Sturges 规则计算分组数"""
        n = len(self.data)
        if n <= 1:
            return 1
        return int(math.ceil(1 + 3.322 * math.log10(n)))
    
    def _build_histogram(self):
        """构建直方图分组"""
        # 初始化分组计数
        bin_counts = [0] * self.num_bins
        
        # 统计每个数据点
        for value in self.data:
            if value < self.min_val or value > self.max_val:
                continue
            
            # 计算分组索引
            if value == self.max_val:
                idx = self.num_bins - 1
            else:
                idx = int((value - self.min_val) / self.bin_width)
            
            if 0 <= idx < self.num_bins:
                bin_counts[idx] += 1
        
        # 创建分组对象
        self._bins = []
        for i in range(self.num_bins):
            lower = self.min_val + i * self.bin_width
            upper = lower + self.bin_width
            self._bins.append(HistogramBin(lower, upper, bin_counts[i]))
    
    @property
    def bins(self) -> List[HistogramBin]:
        """获取所有分组"""
        return self._bins
    
    @property
    def max_count(self) -> int:
        """最大分组计数"""
        return max(bin.count for bin in self._bins) if self._bins else 0
    
    @property
    def min_count(self) -> int:
        """最小分组计数"""
        return min(bin.count for bin in self._bins) if self._bins else 0
    
    def frequencies(self) -> List[float]:
        """获取相对频率列表"""
        return [bin.count / self._total_count for bin in self._bins]
    
    def densities(self) -> List[float]:
        """获取密度列表 (频率/宽度)"""
        total = self._total_count
        return [bin.count / (total * bin.width) if bin.width > 0 else 0 
                for bin in self._bins]
    
    def cumulative_counts(self) -> List[int]:
        """获取累积计数"""
        cumulative = []
        total = 0
        for bin in self._bins:
            total += bin.count
            cumulative.append(total)
        return cumulative
    
    def cumulative_frequencies(self) -> List[float]:
        """获取累积频率"""
        return [count / self._total_count for count in self.cumulative_counts()]
    
    def statistics(self) -> Dict[str, float]:
        """获取统计信息"""
        if not self.data:
            return {}
        
        n = len(self.data)
        mean = sum(self.data) / n
        
        # 计算方差和标准差
        variance = sum((x - mean) ** 2 for x in self.data) / n
        std_dev = math.sqrt(variance)
        
        # 中位数
        sorted_data = sorted(self.data)
        if n % 2 == 0:
            median = (sorted_data[n // 2 - 1] + sorted_data[n // 2]) / 2
        else:
            median = sorted_data[n // 2]
        
        # 众数 (使用分组)
        mode_bin = max(self._bins, key=lambda b: b.count)
        
        return {
            'count': n,
            'min': self.min_val,
            'max': self.max_val,
            'range': self.max_val - self.min_val,
            'mean': mean,
            'median': median,
            'variance': variance,
            'std_dev': std_dev,
            'mode_bin_midpoint': mode_bin.midpoint,
            'mode_count': mode_bin.count
        }
    
    def to_dict(self) -> Dict:
        """转换为字典格式"""
        return {
            'bins': [
                {
                    'lower': bin.lower,
                    'upper': bin.upper,
                    'count': bin.count,
                    'frequency': bin.count / self._total_count,
                    'midpoint': bin.midpoint
                }
                for bin in self._bins
            ],
            'statistics': self.statistics(),
            'config': {
                'num_bins': self.num_bins,
                'bin_width': self.bin_width,
                'range': [self.min_val, self.max_val]
            }
        }
    
    def to_text(self, max_bar_width: int = 50) -> str:
        """生成文本格式直方图"""
        lines = []
        lines.append("=" * 60)
        lines.append("直方图统计报告")
        lines.append("=" * 60)
        
        # 统计信息
        stats = self.statistics()
        lines.append(f"\n数据统计:")
        lines.append(f"  数据量: {stats['count']}")
        lines.append(f"  最小值: {stats['min']:.4f}")
        lines.append(f"  最大值: {stats['max']:.4f}")
        lines.append(f"  范围:   {stats['range']:.4f}")
        lines.append(f"  平均值: {stats['mean']:.4f}")
        lines.append(f"  中位数: {stats['median']:.4f}")
        lines.append(f"  标准差: {stats['std_dev']:.4f}")
        
        # 直方图
        lines.append(f"\n分组数量: {self.num_bins}")
        lines.append(f"分组宽度: {self.bin_width:.4f}")
        lines.append("\n直方图:")
        lines.append("-" * 60)
        
        max_count = self.max_count
        if max_count == 0:
            max_count = 1
        
        for bin in self._bins:
            bar_length = int(bin.count / max_count * max_bar_width)
            bar = '█' * bar_length
            
            # 格式化分组范围
            lower_str = f"{bin.lower:.2f}"
            upper_str = f"{bin.upper:.2f}"
            range_str = f"[{lower_str}, {upper_str})"
            
            lines.append(f"{range_str:20} | {bin.count:6} | {bar}")
        
        lines.append("-" * 60)
        lines.append(f"\nX轴: 分组范围")
        lines.append(f"Y轴: 计数 (█ 每个单位代表约 {max_count / max_bar_width:.1f})")
        
        return '\n'.join(lines)
    
    def to_ascii_chart(self, height: int = 10, width: int = 60) -> str:
        """生成 ASCII 直方图"""
        if not self._bins or self.max_count == 0:
            return "无数据"
        
        # 创建画布
        canvas = [[' ' for _ in range(width)] for _ in range(height)]
        
        # 绘制柱状图
        bin_width_chars = max(1, width // self.num_bins)
        
        for i, bin in enumerate(self._bins):
            # 计算柱高度
            bar_height = int(bin.count / self.max_count * height)
            if bar_height == 0 and bin.count > 0:
                bar_height = 1
            
            # 绘制柱
            start_col = i * bin_width_chars
            for row in range(height - bar_height, height):
                for col in range(start_col, min(start_col + bin_width_chars - 1, width)):
                    if col < width:
                        canvas[row][col] = '█'
        
        # 构建输出
        lines = []
        
        # Y轴标签
        max_label = self.max_count
        for row in range(height):
            y_value = int(max_label * (height - row) / height)
            line = f"{y_value:5} │ {''.join(canvas[row][:width])}"
            lines.append(line)
        
        # X轴
        lines.append(f"     └{'─' * width}")
        
        # X轴标签
        x_labels = []
        step = max(1, self.num_bins // 5)
        for i in range(0, self.num_bins, step):
            x_labels.append(f"{self._bins[i].lower:.1f}")
        x_label_str = ' '.join(x_labels)
        lines.append(f"       {x_label_str}")
        
        return '\n'.join(lines)


def create_histogram(data: List[float], bins: Optional[int] = None,
                     bin_width: Optional[float] = None) -> Histogram:
    """便捷函数: 创建直方图"""
    return Histogram(data, bins=bins, bin_width=bin_width)


def frequency_table(data: List[float], bins: Optional[int] = None) -> List[Tuple[float, float, int]]:
    """便捷函数: 生成频率表
    
    Returns:
        List of (lower, upper, count) tuples
    """
    hist = Histogram(data, bins=bins)
    return [(bin.lower, bin.upper, bin.count) for bin in hist.bins]


def ascii_histogram(data: List[float], bins: Optional[int] = None,
                    height: int = 10, width: int = 50) -> str:
    """便捷函数: 快速生成 ASCII 直方图"""
    hist = Histogram(data, bins=bins)
    return hist.to_ascii_chart(height, width)


def text_histogram(data: List[float], bins: Optional[int] = None) -> str:
    """便捷函数: 快速生成文本直方图"""
    hist = Histogram(data, bins=bins)
    return hist.to_text()


# 示例数据生成
def generate_sample_data(n: int = 100, distribution: str = 'normal',
                         mean: float = 50, std_dev: float = 10) -> List[float]:
    """生成示例数据 (零依赖实现)
    
    Args:
        n: 数据量
        distribution: 分布类型 ('normal', 'uniform', 'exponential')
        mean: 正态分布均值
        std_dev: 正态分布标准差
    
    Returns:
        生成的数据列表
    """
    import random
    
    data = []
    
    if distribution == 'uniform':
        # 均匀分布: [0, 2*mean]
        for _ in range(n):
            data.append(random.uniform(0, 2 * mean))
    
    elif distribution == 'exponential':
        # 指数分布近似
        for _ in range(n):
            # 使用 -ln(U) 生成指数分布
            u = random.random()
            if u > 0:
                data.append(-math.log(u) * mean)
            else:
                data.append(0)
    
    elif distribution == 'normal':
        # Box-Muller 变换生成正态分布
        for _ in range(n // 2):
            u1 = random.random()
            u2 = random.random()
            
            if u1 > 0 and u2 > 0:
                z0 = math.sqrt(-2 * math.log(u1)) * math.cos(2 * math.pi * u2)
                z1 = math.sqrt(-2 * math.log(u1)) * math.sin(2 * math.pi * u2)
                data.append(mean + std_dev * z0)
                data.append(mean + std_dev * z1)
        
        # 如果 n 是奇数，补一个
        if len(data) < n:
            u1 = random.random()
            u2 = random.random()
            if u1 > 0:
                z0 = math.sqrt(-2 * math.log(u1)) * math.cos(2 * math.pi * u2)
                data.append(mean + std_dev * z0)
    
    else:
        raise ValueError(f"未知分布类型: {distribution}")
    
    return data[:n]


if __name__ == '__main__':
    # 演示
    print("Histogram Utils 演示")
    print("=" * 60)
    
    # 生成示例数据
    data = generate_sample_data(100, 'normal', mean=50, std_dev=10)
    
    # 创建直方图
    hist = Histogram(data, bins=10)
    
    # 输出文本报告
    print(hist.to_text())
    
    # 输出 ASCII 图
    print("\nASCII 直方图:")
    print(hist.to_ascii_chart(height=8, width=40))