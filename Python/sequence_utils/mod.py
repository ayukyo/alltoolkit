"""
Sequence Utilities - 序列分析工具模块

提供全面的序列分析和处理功能，包括统计分析、变换操作、模式检测、生成器等。
零依赖，仅使用 Python 标准库。

Author: AllToolkit
Version: 1.0.0
"""

from typing import (
    Optional, Union, List, Tuple, Callable, 
    Iterable, Iterator, Generator, Any, Dict
)
from collections import Counter
from functools import reduce
from itertools import islice, cycle, accumulate, chain
import math
import random


# ============================================================================
# 类型别名
# ============================================================================

Number = Union[int, float]
SequenceLike = Union[List[Number], Tuple[Number, ...]]


# ============================================================================
# 异常类
# ============================================================================

class SequenceError(Exception):
    """序列操作异常基类"""
    pass


class EmptySequenceError(SequenceError):
    """序列为空异常"""
    pass


class InvalidSequenceError(SequenceError):
    """序列无效异常"""
    pass


# ============================================================================
# 统计分析
# ============================================================================

def mean(seq: SequenceLike) -> float:
    """
    计算序列的算术平均值
    
    Args:
        seq: 数字序列
        
    Returns:
        算术平均值
        
    Raises:
        EmptySequenceError: 序列为空时
    """
    if not seq:
        raise EmptySequenceError("序列不能为空")
    return sum(seq) / len(seq)


def median(seq: SequenceLike) -> float:
    """
    计算序列的中位数
    
    Args:
        seq: 数字序列
        
    Returns:
        中位数
    """
    if not seq:
        raise EmptySequenceError("序列不能为空")
    
    sorted_seq = sorted(seq)
    n = len(sorted_seq)
    mid = n // 2
    
    if n % 2 == 0:
        return (sorted_seq[mid - 1] + sorted_seq[mid]) / 2
    return float(sorted_seq[mid])


def mode(seq: SequenceLike) -> List[Number]:
    """
    计算序列的众数（可能出现多个）
    
    Args:
        seq: 数字序列
        
    Returns:
        众数列表
    """
    if not seq:
        raise EmptySequenceError("序列不能为空")
    
    counter = Counter(seq)
    max_count = counter.most_common(1)[0][1]
    return sorted([k for k, v in counter.items() if v == max_count])


def variance(seq: SequenceLike, population: bool = True) -> float:
    """
    计算序列的方差
    
    Args:
        seq: 数字序列
        population: True 为总体方差，False 为样本方差
        
    Returns:
        方差
    """
    if not seq:
        raise EmptySequenceError("序列不能为空")
    
    n = len(seq)
    if not population and n < 2:
        raise InvalidSequenceError("样本方差需要至少两个数据点")
    
    m = mean(seq)
    divisor = n if population else n - 1
    return sum((x - m) ** 2 for x in seq) / divisor


def std_dev(seq: SequenceLike, population: bool = True) -> float:
    """
    计算序列的标准差
    
    Args:
        seq: 数字序列
        population: True 为总体标准差，False 为样本标准差
        
    Returns:
        标准差
    """
    return math.sqrt(variance(seq, population))


def skewness(seq: SequenceLike) -> float:
    """
    计算序列的偏度（衡量分布的不对称性）
    
    Args:
        seq: 数字序列
        
    Returns:
        偏度（正值为右偏，负值为左偏）
    """
    if not seq:
        raise EmptySequenceError("序列不能为空")
    
    n = len(seq)
    m = mean(seq)
    s = std_dev(seq, population=False)
    
    if s == 0:
        return 0.0
    
    return (sum((x - m) ** 3 for x in seq) / n) / (s ** 3)


def kurtosis(seq: SequenceLike) -> float:
    """
    计算序列的峰度（衡量分布的尖锐程度）
    
    Args:
        seq: 数字序列
        
    Returns:
        峰度（正态分布为3，大于3为尖峰，小于3为平峰）
    """
    if not seq:
        raise EmptySequenceError("序列不能为空")
    
    n = len(seq)
    m = mean(seq)
    s = std_dev(seq, population=True)
    
    if s == 0:
        return 0.0
    
    return (sum((x - m) ** 4 for x in seq) / n) / (s ** 4)


def quantile(seq: SequenceLike, q: float) -> float:
    """
    计算序列的分位数
    
    Args:
        seq: 数字序列
        q: 分位数 (0-1)
        
    Returns:
        分位数值
    """
    if not seq:
        raise EmptySequenceError("序列不能为空")
    
    if not 0 <= q <= 1:
        raise ValueError("分位数必须在 0 到 1 之间")
    
    sorted_seq = sorted(seq)
    n = len(sorted_seq)
    
    if q == 0:
        return float(sorted_seq[0])
    if q == 1:
        return float(sorted_seq[-1])
    
    pos = (n - 1) * q
    lower = int(pos)
    upper = lower + 1
    
    if upper >= n:
        return float(sorted_seq[-1])
    
    weight = pos - lower
    return sorted_seq[lower] * (1 - weight) + sorted_seq[upper] * weight


def quartiles(seq: SequenceLike) -> Tuple[float, float, float]:
    """
    计算序列的四分位数
    
    Args:
        seq: 数字序列
        
    Returns:
        (Q1, Q2, Q3) 第一四分位数、中位数、第三四分位数
    """
    return (quantile(seq, 0.25), quantile(seq, 0.5), quantile(seq, 0.75))


def iqr(seq: SequenceLike) -> float:
    """
    计算序列的四分位距 (Interquartile Range)
    
    Args:
        seq: 数字序列
        
    Returns:
        IQR = Q3 - Q1
    """
    q1, _, q3 = quartiles(seq)
    return q3 - q1


def range_value(seq: SequenceLike) -> float:
    """
    计算序列的极差（范围）
    
    Args:
        seq: 数字序列
        
    Returns:
        最大值 - 最小值
    """
    if not seq:
        raise EmptySequenceError("序列不能为空")
    return float(max(seq) - min(seq))


def coefficient_of_variation(seq: SequenceLike) -> float:
    """
    计算序列的变异系数（CV）
    
    Args:
        seq: 数字序列
        
    Returns:
        CV = 标准差 / 均值
    """
    if not seq:
        raise EmptySequenceError("序列不能为空")
    
    m = mean(seq)
    if m == 0:
        return float('inf')
    
    return std_dev(seq) / abs(m)


def descriptive_stats(seq: SequenceLike) -> Dict[str, float]:
    """
    计算序列的描述性统计量
    
    Args:
        seq: 数字序列
        
    Returns:
        包含各种统计量的字典
    """
    if not seq:
        raise EmptySequenceError("序列不能为空")
    
    q1, q2, q3 = quartiles(seq)
    
    return {
        'count': len(seq),
        'mean': mean(seq),
        'median': q2,
        'mode': mode(seq),
        'std_dev': std_dev(seq, population=False),
        'variance': variance(seq, population=False),
        'min': float(min(seq)),
        'max': float(max(seq)),
        'range': range_value(seq),
        'q1': q1,
        'q3': q3,
        'iqr': iqr(seq),
        'skewness': skewness(seq),
        'kurtosis': kurtosis(seq),
        'cv': coefficient_of_variation(seq),
    }


# ============================================================================
# 序列变换
# ============================================================================

def normalize(seq: SequenceLike, 
              method: str = 'minmax',
              a: float = 0, b: float = 1) -> List[float]:
    """
    归一化序列
    
    Args:
        seq: 数字序列
        method: 归一化方法 ('minmax' 或 'zscore')
        a: minmax 方法的目标区间下界
        b: minmax 方法的目标区间上界
        
    Returns:
        归一化后的序列
    """
    if not seq:
        raise EmptySequenceError("序列不能为空")
    
    if method == 'minmax':
        min_val, max_val = min(seq), max(seq)
        if min_val == max_val:
            return [a] * len(seq)
        return [a + (x - min_val) * (b - a) / (max_val - min_val) for x in seq]
    
    elif method == 'zscore':
        m = mean(seq)
        s = std_dev(seq, population=False)
        if s == 0:
            return [0.0] * len(seq)
        return [(x - m) / s for x in seq]
    
    else:
        raise ValueError(f"未知的归一化方法: {method}")


def standardize(seq: SequenceLike) -> List[float]:
    """
    标准化序列（Z-score 标准化）
    
    Args:
        seq: 数字序列
        
    Returns:
        标准化后的序列
    """
    return normalize(seq, method='zscore')


def differentiate(seq: SequenceLike, n: int = 1) -> List[float]:
    """
    计算序列的差分
    
    Args:
        seq: 数字序列
        n: 差分阶数
        
    Returns:
        差分后的序列
    """
    if n < 1:
        raise ValueError("差分阶数必须大于 0")
    
    if not seq:
        raise EmptySequenceError("序列不能为空")
    
    result = [float(x) for x in seq]
    for _ in range(n):
        if len(result) < 2:
            raise InvalidSequenceError(f"序列太短，无法进行 {n} 阶差分")
        result = [result[i + 1] - result[i] for i in range(len(result) - 1)]
    
    return result


def cumulative_sum(seq: SequenceLike) -> List[float]:
    """
    计算序列的累积和
    
    Args:
        seq: 数字序列
        
    Returns:
        累积和序列
    """
    if not seq:
        raise EmptySequenceError("序列不能为空")
    return list(accumulate(seq))


def cumulative_product(seq: SequenceLike) -> List[float]:
    """
    计算序列的累积积
    
    Args:
        seq: 数字序列
        
    Returns:
        累积积序列
    """
    if not seq:
        raise EmptySequenceError("序列不能为空")
    return list(accumulate(seq, lambda x, y: x * y))


def exponential_smoothing(seq: SequenceLike, alpha: float = 0.3) -> List[float]:
    """
    指数平滑
    
    Args:
        seq: 数字序列
        alpha: 平滑系数 (0-1)
        
    Returns:
        平滑后的序列
    """
    if not seq:
        raise EmptySequenceError("序列不能为空")
    
    if not 0 < alpha < 1:
        raise ValueError("平滑系数必须在 0 到 1 之间")
    
    result = [float(seq[0])]
    for x in seq[1:]:
        result.append(alpha * x + (1 - alpha) * result[-1])
    
    return result


def moving_average(seq: SequenceLike, window: int, 
                   weights: Optional[List[float]] = None) -> List[float]:
    """
    移动平均
    
    Args:
        seq: 数字序列
        window: 窗口大小
        weights: 可选权重列表（长度必须等于 window）
        
    Returns:
        移动平均序列
    """
    if not seq:
        raise EmptySequenceError("序列不能为空")
    
    if window < 1:
        raise ValueError("窗口大小必须大于 0")
    
    if len(seq) < window:
        raise InvalidSequenceError("序列长度必须大于等于窗口大小")
    
    if weights is not None:
        if len(weights) != window:
            raise ValueError("权重长度必须等于窗口大小")
        weight_sum = sum(weights)
        weights = [w / weight_sum for w in weights]
    else:
        weights = [1.0 / window] * window
    
    result = []
    for i in range(len(seq) - window + 1):
        window_sum = sum(seq[i + j] * weights[j] for j in range(window))
        result.append(window_sum)
    
    return result


def log_transform(seq: SequenceLike, base: float = math.e) -> List[float]:
    """
    对数变换
    
    Args:
        seq: 数字序列
        base: 对数底数
        
    Returns:
        对数变换后的序列
    """
    if not seq:
        raise EmptySequenceError("序列不能为空")
    
    if any(x <= 0 for x in seq):
        raise InvalidSequenceError("对数变换要求所有值必须大于 0")
    
    if base == math.e:
        return [math.log(x) for x in seq]
    return [math.log(x, base) for x in seq]


def power_transform(seq: SequenceLike, exponent: float) -> List[float]:
    """
    幂变换
    
    Args:
        seq: 数字序列
        exponent: 指数
        
    Returns:
        幂变换后的序列
    """
    if not seq:
        raise EmptySequenceError("序列不能为空")
    
    return [x ** exponent for x in seq]


def box_cox_transform(seq: SequenceLike, lambda_param: float) -> List[float]:
    """
    Box-Cox 变换
    
    Args:
        seq: 数字序列（必须全为正数）
        lambda_param: 变换参数
        
    Returns:
        Box-Cox 变换后的序列
    """
    if not seq:
        raise EmptySequenceError("序列不能为空")
    
    if any(x <= 0 for x in seq):
        raise InvalidSequenceError("Box-Cox 变换要求所有值必须大于 0")
    
    if lambda_param == 0:
        return [math.log(x) for x in seq]
    
    return [(x ** lambda_param - 1) / lambda_param for x in seq]


# ============================================================================
# 序列生成器
# ============================================================================

def arange(start: Number, stop: Optional[Number] = None, 
           step: Number = 1) -> List[float]:
    """
    生成等差数列
    
    Args:
        start: 起始值
        stop: 结束值（不包含），若为 None 则 start 为结束值，起始值为 0
        step: 步长
        
    Returns:
        等差数列
    """
    if stop is None:
        start, stop = 0, start
    
    result = []
    current = start
    
    if step > 0:
        while current < stop:
            result.append(float(current))
            current += step
    elif step < 0:
        while current > stop:
            result.append(float(current))
            current += step
    else:
        raise ValueError("步长不能为 0")
    
    return result


def linspace(start: Number, stop: Number, num: int = 50) -> List[float]:
    """
    生成等间隔数列
    
    Args:
        start: 起始值
        stop: 结束值（包含）
        num: 点数
        
    Returns:
        等间隔数列
    """
    if num < 1:
        raise ValueError("点数必须大于 0")
    
    if num == 1:
        return [float(start)]
    
    step = (stop - start) / (num - 1)
    return [start + i * step for i in range(num)]


def logspace(start: Number, stop: Number, num: int = 50, 
             base: float = 10.0) -> List[float]:
    """
    生成对数等间隔数列
    
    Args:
        start: 起始指数
        stop: 结束指数
        num: 点数
        base: 对数底数
        
    Returns:
        对数等间隔数列
    """
    linear = linspace(start, stop, num)
    return [base ** x for x in linear]


def geometric_sequence(start: Number, ratio: Number, 
                       length: int) -> List[float]:
    """
    生成等比数列
    
    Args:
        start: 首项
        ratio: 公比
        length: 长度
        
    Returns:
        等比数列
    """
    if length < 1:
        raise ValueError("长度必须大于 0")
    
    return [start * (ratio ** i) for i in range(length)]


def fibonacci(n: int) -> List[int]:
    """
    生成斐波那契数列
    
    Args:
        n: 数列长度
        
    Returns:
        斐波那契数列
    """
    if n < 0:
        raise ValueError("长度不能为负数")
    
    if n == 0:
        return []
    if n == 1:
        return [0]
    if n == 2:
        return [0, 1]
    
    result = [0, 1]
    for _ in range(n - 2):
        result.append(result[-1] + result[-2])
    
    return result


def tribonacci(n: int) -> List[int]:
    """
    生成三波那契数列（每位是前三位之和）
    
    Args:
        n: 数列长度
        
    Returns:
        三波那契数列
    """
    if n < 0:
        raise ValueError("长度不能为负数")
    
    if n == 0:
        return []
    if n == 1:
        return [0]
    if n == 2:
        return [0, 0]
    if n == 3:
        return [0, 0, 1]
    
    result = [0, 0, 1]
    for _ in range(n - 3):
        result.append(result[-1] + result[-2] + result[-3])
    
    return result


def lucas_numbers(n: int) -> List[int]:
    """
    生成卢卡斯数列（类似斐波那契，但起始值为 2, 1）
    
    Args:
        n: 数列长度
        
    Returns:
        卢卡斯数列
    """
    if n < 0:
        raise ValueError("长度不能为负数")
    
    if n == 0:
        return []
    if n == 1:
        return [2]
    if n == 2:
        return [2, 1]
    
    result = [2, 1]
    for _ in range(n - 2):
        result.append(result[-1] + result[-2])
    
    return result


def prime_numbers(n: int) -> List[int]:
    """
    生成前 n 个质数
    
    Args:
        n: 质数个数
        
    Returns:
        质数列表
    """
    if n < 0:
        raise ValueError("数量不能为负数")
    
    if n == 0:
        return []
    
    def is_prime(num: int) -> bool:
        if num < 2:
            return False
        if num == 2:
            return True
        if num % 2 == 0:
            return False
        for i in range(3, int(math.sqrt(num)) + 1, 2):
            if num % i == 0:
                return False
        return True
    
    result = []
    candidate = 2
    while len(result) < n:
        if is_prime(candidate):
            result.append(candidate)
        candidate += 1
    
    return result


def triangular_numbers(n: int) -> List[int]:
    """
    生成三角形数列
    
    Args:
        n: 数列长度
        
    Returns:
        三角形数列
    """
    if n < 0:
        raise ValueError("长度不能为负数")
    
    return [i * (i + 1) // 2 for i in range(1, n + 1)]


def square_numbers(n: int) -> List[int]:
    """
    生成平方数列
    
    Args:
        n: 数列长度
        
    Returns:
        平方数列
    """
    if n < 0:
        raise ValueError("长度不能为负数")
    
    return [i ** 2 for i in range(1, n + 1)]


def cube_numbers(n: int) -> List[int]:
    """
    生成立方数列
    
    Args:
        n: 数列长度
        
    Returns:
        立方数列
    """
    if n < 0:
        raise ValueError("长度不能为负数")
    
    return [i ** 3 for i in range(1, n + 1)]


def factorial_sequence(n: int) -> List[int]:
    """
    生成阶乘数列
    
    Args:
        n: 数列长度
        
    Returns:
        阶乘数列
    """
    if n < 0:
        raise ValueError("长度不能为负数")
    
    if n == 0:
        return []
    
    result = [1]
    for i in range(1, n):
        result.append(result[-1] * (i + 1))
    
    return result


# ============================================================================
# 滑动窗口操作
# ============================================================================

def sliding_window(seq: SequenceLike, window_size: int, 
                   step: int = 1) -> List[List[Number]]:
    """
    滑动窗口
    
    Args:
        seq: 数字序列
        window_size: 窗口大小
        step: 步长
        
    Returns:
        窗口列表
    """
    if not seq:
        raise EmptySequenceError("序列不能为空")
    
    if window_size < 1:
        raise ValueError("窗口大小必须大于 0")
    
    if step < 1:
        raise ValueError("步长必须大于 0")
    
    if len(seq) < window_size:
        return []
    
    return [[seq[i + j] for j in range(window_size)] 
            for i in range(0, len(seq) - window_size + 1, step)]


def rolling_max(seq: SequenceLike, window: int) -> List[float]:
    """
    滚动最大值
    
    Args:
        seq: 数字序列
        window: 窗口大小
        
    Returns:
        滚动最大值序列
    """
    windows = sliding_window(seq, window)
    return [float(max(w)) for w in windows]


def rolling_min(seq: SequenceLike, window: int) -> List[float]:
    """
    滚动最小值
    
    Args:
        seq: 数字序列
        window: 窗口大小
        
    Returns:
        滚动最小值序列
    """
    windows = sliding_window(seq, window)
    return [float(min(w)) for w in windows]


def rolling_sum(seq: SequenceLike, window: int) -> List[float]:
    """
    滚动求和
    
    Args:
        seq: 数字序列
        window: 窗口大小
        
    Returns:
        滚动求和序列
    """
    windows = sliding_window(seq, window)
    return [float(sum(w)) for w in windows]


def rolling_std(seq: SequenceLike, window: int) -> List[float]:
    """
    滚动标准差
    
    Args:
        seq: 数字序列
        window: 窗口大小
        
    Returns:
        滚动标准差序列
    """
    windows = sliding_window(seq, window)
    return [std_dev(w, population=False) for w in windows]


# ============================================================================
# 插值与填充
# ============================================================================

def linear_interpolate(x: List[Number], y: List[Number], 
                       x_new: Number) -> float:
    """
    线性插值
    
    Args:
        x: x 值序列
        y: y 值序列
        x_new: 新的 x 值
        
    Returns:
        插值结果
    """
    if len(x) != len(y):
        raise ValueError("x 和 y 长度必须相同")
    
    if len(x) < 2:
        raise InvalidSequenceError("至少需要两个数据点")
    
    # 找到 x_new 所在的区间
    for i in range(len(x) - 1):
        if x[i] <= x_new <= x[i + 1]:
            # 线性插值公式
            t = (x_new - x[i]) / (x[i + 1] - x[i])
            return y[i] + t * (y[i + 1] - y[i])
    
    # 外推
    if x_new < x[0]:
        t = (x_new - x[0]) / (x[1] - x[0])
        return y[0] + t * (y[1] - y[0])
    else:
        t = (x_new - x[-2]) / (x[-1] - x[-2])
        return y[-2] + t * (y[-1] - y[-2])


def fill_missing(seq: List[Optional[Number]], 
                 method: str = 'linear') -> List[Number]:
    """
    填充缺失值
    
    Args:
        seq: 可能包含 None 的序列
        method: 填充方法 ('linear', 'forward', 'backward', 'mean', 'median')
        
    Returns:
        填充后的序列
    """
    if not seq:
        raise EmptySequenceError("序列不能为空")
    
    result = list(seq)
    
    if method == 'forward':
        last_val = None
        for i in range(len(result)):
            if result[i] is None:
                if last_val is not None:
                    result[i] = last_val
            else:
                last_val = result[i]
    
    elif method == 'backward':
        next_val = None
        for i in range(len(result) - 1, -1, -1):
            if result[i] is None:
                if next_val is not None:
                    result[i] = next_val
            else:
                next_val = result[i]
    
    elif method == 'linear':
        # 首先用前后值填充边界
        result = fill_missing(result, 'forward')
        result = fill_missing(result, 'backward')
    
    elif method == 'mean':
        valid_vals = [x for x in result if x is not None]
        if valid_vals:
            m = mean(valid_vals)
            result = [x if x is not None else m for x in result]
    
    elif method == 'median':
        valid_vals = [x for x in result if x is not None]
        if valid_vals:
            med = median(valid_vals)
            result = [x if x is not None else med for x in result]
    
    else:
        raise ValueError(f"未知的填充方法: {method}")
    
    # 类型转换
    return [float(x) if x is not None else 0.0 for x in result]


# ============================================================================
# 重采样
# ============================================================================

def downsample(seq: SequenceLike, factor: int, 
               method: str = 'mean') -> List[float]:
    """
    下采样
    
    Args:
        seq: 数字序列
        factor: 下采样因子
        method: 聚合方法 ('mean', 'sum', 'max', 'min', 'first', 'last')
        
    Returns:
        下采样后的序列
    """
    if not seq:
        raise EmptySequenceError("序列不能为空")
    
    if factor < 1:
        raise ValueError("下采样因子必须大于 0")
    
    result = []
    for i in range(0, len(seq), factor):
        window = seq[i:i + factor]
        if method == 'mean':
            result.append(mean(window))
        elif method == 'sum':
            result.append(float(sum(window)))
        elif method == 'max':
            result.append(float(max(window)))
        elif method == 'min':
            result.append(float(min(window)))
        elif method == 'first':
            result.append(float(window[0]))
        elif method == 'last':
            result.append(float(window[-1]))
        else:
            raise ValueError(f"未知的聚合方法: {method}")
    
    return result


def upsample(seq: SequenceLike, factor: int, 
             method: str = 'linear') -> List[float]:
    """
    上采样
    
    Args:
        seq: 数字序列
        factor: 上采样因子
        method: 插值方法 ('linear', 'nearest', 'previous', 'next')
        
    Returns:
        上采样后的序列
    """
    if not seq:
        raise EmptySequenceError("序列不能为空")
    
    if factor < 1:
        raise ValueError("上采样因子必须大于 0")
    
    result = []
    for i in range(len(seq) - 1):
        result.append(float(seq[i]))
        
        if method == 'linear':
            for j in range(1, factor):
                t = j / factor
                result.append(float(seq[i] + t * (seq[i + 1] - seq[i])))
        
        elif method == 'nearest':
            for j in range(1, factor):
                result.append(float(seq[i]))
        
        elif method == 'previous':
            for j in range(1, factor):
                result.append(float(seq[i]))
        
        elif method == 'next':
            for j in range(1, factor):
                result.append(float(seq[i + 1]))
        
        else:
            raise ValueError(f"未知的插值方法: {method}")
    
    result.append(float(seq[-1]))
    return result


# ============================================================================
# 序列操作
# ============================================================================

def reverse(seq: SequenceLike) -> List[Number]:
    """
    反转序列
    
    Args:
        seq: 数字序列
        
    Returns:
        反转后的序列
    """
    return list(reversed(seq))


def shuffle(seq: SequenceLike, seed: Optional[int] = None) -> List[Number]:
    """
    随机打乱序列
    
    Args:
        seq: 数字序列
        seed: 随机种子
        
    Returns:
        打乱后的序列
    """
    result = list(seq)
    if seed is not None:
        random.seed(seed)
    random.shuffle(result)
    return result


def sample(seq: SequenceLike, n: int, 
           replace: bool = False, seed: Optional[int] = None) -> List[Number]:
    """
    从序列中抽样
    
    Args:
        seq: 数字序列
        n: 样本数量
        replace: 是否放回抽样
        seed: 随机种子
        
    Returns:
        样本列表
    """
    if not seq:
        raise EmptySequenceError("序列不能为空")
    
    if seed is not None:
        random.seed(seed)
    
    if replace:
        return [random.choice(seq) for _ in range(n)]
    else:
        if n > len(seq):
            raise ValueError("不放回抽样数量不能超过序列长度")
        return random.sample(list(seq), n)


def split(seq: SequenceLike, ratio: float = 0.5, 
          shuffle_data: bool = False, seed: Optional[int] = None) -> Tuple[List[Number], List[Number]]:
    """
    分割序列
    
    Args:
        seq: 数字序列
        ratio: 分割比例（第一部分的比例）
        shuffle_data: 是否打乱
        seed: 随机种子
        
    Returns:
        (第一部分, 第二部分)
    """
    if not seq:
        raise EmptySequenceError("序列不能为空")
    
    if not 0 < ratio < 1:
        raise ValueError("分割比例必须在 0 和 1 之间")
    
    data = list(seq)
    if shuffle_data:
        if seed is not None:
            random.seed(seed)
        random.shuffle(data)
    
    split_idx = int(len(data) * ratio)
    return data[:split_idx], data[split_idx:]


def chunk(seq: SequenceLike, size: int) -> List[List[Number]]:
    """
    分块
    
    Args:
        seq: 数字序列
        size: 块大小
        
    Returns:
        分块后的列表
    """
    if size < 1:
        raise ValueError("块大小必须大于 0")
    
    return [list(seq[i:i + size]) for i in range(0, len(seq), size)]


def flatten(seqs: List[SequenceLike]) -> List[Number]:
    """
    展平嵌套序列
    
    Args:
        seqs: 嵌套序列列表
        
    Returns:
        展平后的序列
    """
    return list(chain.from_iterable(seqs))


def unique(seq: SequenceLike, preserve_order: bool = True) -> List[Number]:
    """
    获取唯一元素
    
    Args:
        seq: 数字序列
        preserve_order: 是否保持原始顺序
        
    Returns:
        唯一元素列表
    """
    if preserve_order:
        seen = set()
        result = []
        for x in seq:
            if x not in seen:
                seen.add(x)
                result.append(x)
        return result
    else:
        return list(set(seq))


def difference(seq1: SequenceLike, seq2: SequenceLike) -> List[Number]:
    """
    序列差集（seq1 - seq2）
    
    Args:
        seq1: 第一个序列
        seq2: 第二个序列
        
    Returns:
        差集
    """
    set2 = set(seq2)
    return [x for x in seq1 if x not in set2]


def intersection(seq1: SequenceLike, seq2: SequenceLike) -> List[Number]:
    """
    序列交集
    
    Args:
        seq1: 第一个序列
        seq2: 第二个序列
        
    Returns:
        交集
    """
    set2 = set(seq2)
    seen = set()
    result = []
    for x in seq1:
        if x in set2 and x not in seen:
            seen.add(x)
            result.append(x)
    return result


def union(seq1: SequenceLike, seq2: SequenceLike) -> List[Number]:
    """
    序列并集
    
    Args:
        seq1: 第一个序列
        seq2: 第二个序列
        
    Returns:
        并集
    """
    return unique(list(seq1) + list(seq2))


# ============================================================================
# 异常值检测
# ============================================================================

def zscore_outliers(seq: SequenceLike, threshold: float = 3.0) -> List[int]:
    """
    使用 Z-score 检测异常值索引
    
    Args:
        seq: 数字序列
        threshold: Z-score 阈值
        
    Returns:
        异常值索引列表
    """
    if not seq:
        raise EmptySequenceError("序列不能为空")
    
    m = mean(seq)
    s = std_dev(seq, population=False)
    
    if s == 0:
        return []
    
    zscores = [(x - m) / s for x in seq]
    return [i for i, z in enumerate(zscores) if abs(z) > threshold]


def iqr_outliers(seq: SequenceLike, k: float = 1.5) -> List[int]:
    """
    使用 IQR 方法检测异常值索引
    
    Args:
        seq: 数字序列
        k: IQR 倍数阈值（通常 1.5 或 3.0）
        
    Returns:
        异常值索引列表
    """
    if not seq:
        raise EmptySequenceError("序列不能为空")
    
    q1, _, q3 = quartiles(seq)
    iqr_val = q3 - q1
    lower = q1 - k * iqr_val
    upper = q3 + k * iqr_val
    
    return [i for i, x in enumerate(seq) if x < lower or x > upper]


def remove_outliers(seq: SequenceLike, method: str = 'iqr', 
                    **kwargs) -> List[Number]:
    """
    移除异常值
    
    Args:
        seq: 数字序列
        method: 检测方法 ('iqr' 或 'zscore')
        **kwargs: 传递给检测函数的参数
        
    Returns:
        移除异常值后的序列
    """
    if method == 'iqr':
        outlier_indices = set(iqr_outliers(seq, **kwargs))
    elif method == 'zscore':
        outlier_indices = set(zscore_outliers(seq, **kwargs))
    else:
        raise ValueError(f"未知的检测方法: {method}")
    
    return [x for i, x in enumerate(seq) if i not in outlier_indices]


# ============================================================================
# 趋势与周期检测
# ============================================================================

def is_monotonic(seq: SequenceLike, strict: bool = False) -> bool:
    """
    检查序列是否单调
    
    Args:
        seq: 数字序列
        strict: 是否严格单调
        
    Returns:
        是否单调
    """
    if len(seq) < 2:
        return True
    
    if strict:
        increasing = all(seq[i] < seq[i + 1] for i in range(len(seq) - 1))
        decreasing = all(seq[i] > seq[i + 1] for i in range(len(seq) - 1))
    else:
        increasing = all(seq[i] <= seq[i + 1] for i in range(len(seq) - 1))
        decreasing = all(seq[i] >= seq[i + 1] for i in range(len(seq) - 1))
    
    return increasing or decreasing


def is_increasing(seq: SequenceLike, strict: bool = False) -> bool:
    """
    检查序列是否递增
    
    Args:
        seq: 数字序列
        strict: 是否严格递增
        
    Returns:
        是否递增
    """
    if len(seq) < 2:
        return True
    
    if strict:
        return all(seq[i] < seq[i + 1] for i in range(len(seq) - 1))
    return all(seq[i] <= seq[i + 1] for i in range(len(seq) - 1))


def is_decreasing(seq: SequenceLike, strict: bool = False) -> bool:
    """
    检查序列是否递减
    
    Args:
        seq: 数字序列
        strict: 是否严格递减
        
    Returns:
        是否递减
    """
    if len(seq) < 2:
        return True
    
    if strict:
        return all(seq[i] > seq[i + 1] for i in range(len(seq) - 1))
    return all(seq[i] >= seq[i + 1] for i in range(len(seq) - 1))


def trend_direction(seq: SequenceLike) -> str:
    """
    判断序列趋势方向
    
    Args:
        seq: 数字序列
        
    Returns:
        'increasing', 'decreasing', 或 'flat'
    """
    if len(seq) < 2:
        return 'flat'
    
    diff = differentiate(seq)
    pos_count = sum(1 for d in diff if d > 0)
    neg_count = sum(1 for d in diff if d < 0)
    
    if pos_count > neg_count:
        return 'increasing'
    elif neg_count > pos_count:
        return 'decreasing'
    else:
        return 'flat'


def find_peaks(seq: SequenceLike, prominence: float = 0.0) -> List[int]:
    """
    查找峰值索引
    
    Args:
        seq: 数字序列
        prominence: 最小突出度阈值
        
    Returns:
        峰值索引列表
    """
    if len(seq) < 3:
        return []
    
    peaks = []
    for i in range(1, len(seq) - 1):
        if seq[i] > seq[i - 1] and seq[i] > seq[i + 1]:
            peaks.append(i)
    
    if prominence > 0:
        # 过滤掉突出度不够的峰值
        result = []
        for peak in peaks:
            # 计算左右最低点
            left_min = min(seq[:peak])
            right_min = min(seq[peak + 1:])
            prom = seq[peak] - max(left_min, right_min)
            if prom >= prominence:
                result.append(peak)
        return result
    
    return peaks


def find_valleys(seq: SequenceLike, prominence: float = 0.0) -> List[int]:
    """
    查找谷值索引
    
    Args:
        seq: 数字序列
        prominence: 最小突出度阈值
        
    Returns:
        谷值索引列表
    """
    # 反转序列并查找峰值
    inverted = [-x for x in seq]
    return find_peaks(inverted, prominence)


def detect_seasonality(seq: SequenceLike, max_period: int = 0) -> Optional[int]:
    """
    检测序列的周期性
    
    Args:
        seq: 数字序列
        max_period: 最大周期检测范围（默认为 len(seq) // 2）
        
    Returns:
        检测到的周期长度，若未检测到返回 None
    """
    if len(seq) < 4:
        return None
    
    if max_period == 0:
        max_period = len(seq) // 2
    
    max_period = min(max_period, len(seq) // 2)
    
    # 使用自相关方法
    m = mean(seq)
    variance = sum((x - m) ** 2 for x in seq)
    
    if variance == 0:
        return None
    
    best_period = None
    best_corr = 0
    
    for period in range(2, max_period + 1):
        # 计算自相关
        numerator = sum((seq[i] - m) * (seq[i + period] - m) 
                       for i in range(len(seq) - period))
        corr = numerator / variance
        
        if corr > best_corr and corr > 0.5:
            best_corr = corr
            best_period = period
    
    return best_period


# ============================================================================
# 自相关与滞后
# ============================================================================

def autocorrelation(seq: SequenceLike, lag: int) -> float:
    """
    计算自相关系数
    
    Args:
        seq: 数字序列
        lag: 滞后阶数
        
    Returns:
        自相关系数
    """
    if not seq:
        raise EmptySequenceError("序列不能为空")
    
    if lag < 0 or lag >= len(seq):
        raise ValueError(f"滞后阶数必须在 0 和 {len(seq) - 1} 之间")
    
    if lag == 0:
        return 1.0
    
    n = len(seq)
    m = mean(seq)
    variance = sum((x - m) ** 2 for x in seq)
    
    if variance == 0:
        return 0.0
    
    numerator = sum((seq[i] - m) * (seq[i + lag] - m) 
                   for i in range(n - lag))
    
    return numerator / variance


def autocorrelation_function(seq: SequenceLike, 
                              max_lag: int = 0) -> List[float]:
    """
    计算自相关函数（ACF）
    
    Args:
        seq: 数字序列
        max_lag: 最大滞后阶数
        
    Returns:
        ACF 值列表
    """
    if not seq:
        raise EmptySequenceError("序列不能为空")
    
    if max_lag == 0:
        max_lag = len(seq) - 1
    
    return [autocorrelation(seq, lag) for lag in range(max_lag + 1)]


def lag(seq: SequenceLike, n: int, fill: Optional[Number] = None) -> List[Optional[Number]]:
    """
    滞后序列
    
    Args:
        seq: 数字序列
        n: 滞后阶数
        fill: 填充值
        
    Returns:
        滞后后的序列
    """
    if not seq:
        raise EmptySequenceError("序列不能为空")
    
    if n < 0:
        raise ValueError("滞后阶数不能为负")
    
    if n == 0:
        return list(seq)
    
    return [fill] * n + list(seq[:-n])


def lead(seq: SequenceLike, n: int, fill: Optional[Number] = None) -> List[Optional[Number]]:
    """
    领先序列
    
    Args:
        seq: 数字序列
        n: 领先阶数
        fill: 填充值
        
    Returns:
        领先后的序列
    """
    if not seq:
        raise EmptySequenceError("序列不能为空")
    
    if n < 0:
        raise ValueError("领先阶数不能为负")
    
    if n == 0:
        return list(seq)
    
    return list(seq[n:]) + [fill] * n


# ============================================================================
# 序列相似度
# ============================================================================

def euclidean_distance(seq1: SequenceLike, seq2: SequenceLike) -> float:
    """
    欧几里得距离
    
    Args:
        seq1: 第一个序列
        seq2: 第二个序列
        
    Returns:
        欧几里得距离
    """
    if len(seq1) != len(seq2):
        raise ValueError("序列长度必须相同")
    
    return math.sqrt(sum((a - b) ** 2 for a, b in zip(seq1, seq2)))


def manhattan_distance(seq1: SequenceLike, seq2: SequenceLike) -> float:
    """
    曼哈顿距离
    
    Args:
        seq1: 第一个序列
        seq2: 第二个序列
        
    Returns:
        曼哈顿距离
    """
    if len(seq1) != len(seq2):
        raise ValueError("序列长度必须相同")
    
    return sum(abs(a - b) for a, b in zip(seq1, seq2))


def cosine_similarity(seq1: SequenceLike, seq2: SequenceLike) -> float:
    """
    余弦相似度
    
    Args:
        seq1: 第一个序列
        seq2: 第二个序列
        
    Returns:
        余弦相似度
    """
    if len(seq1) != len(seq2):
        raise ValueError("序列长度必须相同")
    
    dot_product = sum(a * b for a, b in zip(seq1, seq2))
    norm1 = math.sqrt(sum(a ** 2 for a in seq1))
    norm2 = math.sqrt(sum(b ** 2 for b in seq2))
    
    if norm1 == 0 or norm2 == 0:
        return 0.0
    
    return dot_product / (norm1 * norm2)


def pearson_correlation(seq1: SequenceLike, seq2: SequenceLike) -> float:
    """
    皮尔逊相关系数
    
    Args:
        seq1: 第一个序列
        seq2: 第二个序列
        
    Returns:
        皮尔逊相关系数
    """
    if len(seq1) != len(seq2):
        raise ValueError("序列长度必须相同")
    
    n = len(seq1)
    if n < 2:
        raise InvalidSequenceError("至少需要两个数据点")
    
    m1, m2 = mean(seq1), mean(seq2)
    
    numerator = sum((a - m1) * (b - m2) for a, b in zip(seq1, seq2))
    denominator = math.sqrt(
        sum((a - m1) ** 2 for a in seq1) * 
        sum((b - m2) ** 2 for b in seq2)
    )
    
    if denominator == 0:
        return 0.0
    
    return numerator / denominator


def spearman_correlation(seq1: SequenceLike, seq2: SequenceLike) -> float:
    """
    斯皮尔曼相关系数
    
    Args:
        seq1: 第一个序列
        seq2: 第二个序列
        
    Returns:
        斯皮尔曼相关系数
    """
    if len(seq1) != len(seq2):
        raise ValueError("序列长度必须相同")
    
    n = len(seq1)
    if n < 2:
        raise InvalidSequenceError("至少需要两个数据点")
    
    # 计算秩
    def rank(seq):
        sorted_indices = sorted(range(len(seq)), key=lambda i: seq[i])
        ranks = [0] * len(seq)
        i = 0
        while i < len(seq):
            j = i
            while j < len(seq) - 1 and seq[sorted_indices[j]] == seq[sorted_indices[j + 1]]:
                j += 1
            avg_rank = (i + j) / 2 + 1
            for k in range(i, j + 1):
                ranks[sorted_indices[k]] = avg_rank
            i = j + 1
        return ranks
    
    ranks1 = rank(list(seq1))
    ranks2 = rank(list(seq2))
    
    return pearson_correlation(ranks1, ranks2)


def dtw_distance(seq1: SequenceLike, seq2: SequenceLike) -> float:
    """
    动态时间规整（DTW）距离
    
    Args:
        seq1: 第一个序列
        seq2: 第二个序列
        
    Returns:
        DTW 距离
    """
    n, m = len(seq1), len(seq2)
    
    if n == 0 or m == 0:
        raise EmptySequenceError("序列不能为空")
    
    # 创建距离矩阵
    dtw_matrix = [[float('inf')] * (m + 1) for _ in range(n + 1)]
    dtw_matrix[0][0] = 0
    
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            cost = abs(seq1[i - 1] - seq2[j - 1])
            dtw_matrix[i][j] = cost + min(
                dtw_matrix[i - 1][j],
                dtw_matrix[i][j - 1],
                dtw_matrix[i - 1][j - 1]
            )
    
    return dtw_matrix[n][m]


# ============================================================================
# 实用工具
# ============================================================================

def apply(seq: SequenceLike, func: Callable[[Number], Number]) -> List[Number]:
    """
    对序列应用函数
    
    Args:
        seq: 数字序列
        func: 映射函数
        
    Returns:
        应用函数后的序列
    """
    return [func(x) for x in seq]


def filter_seq(seq: SequenceLike, 
               predicate: Callable[[Number], bool]) -> List[Number]:
    """
    过滤序列
    
    Args:
        seq: 数字序列
        predicate: 过滤谓词
        
    Returns:
        过滤后的序列
    """
    return [x for x in seq if predicate(x)]


def reduce_seq(seq: SequenceLike, 
               func: Callable[[Number, Number], Number], 
               initial: Optional[Number] = None) -> Number:
    """
    归约序列
    
    Args:
        seq: 数字序列
        func: 归约函数
        initial: 初始值
        
    Returns:
        归约结果
    """
    if initial is not None:
        return reduce(func, seq, initial)
    return reduce(func, seq)


def compose(*funcs: Callable[[Number], Number]) -> Callable[[Number], Number]:
    """
    函数组合
    
    Args:
        *funcs: 要组合的函数
        
    Returns:
        组合后的函数
    """
    def composed(x: Number) -> Number:
        result = x
        for func in reversed(funcs):
            result = func(result)
        return result
    return composed


# ============================================================================
# 常用常量
# ============================================================================

GOLDEN_RATIO = (1 + math.sqrt(5)) / 2
EULER_NUMBER = math.e
PI = math.pi


def golden_sequence(n: int) -> List[float]:
    """
    生成黄金比例序列
    
    Args:
        n: 序列长度
        
    Returns:
        黄金比例序列
    """
    if n < 0:
        raise ValueError("长度不能为负数")
    
    return [GOLDEN_RATIO ** i for i in range(n)]


# ============================================================================
# 示例与测试
# ============================================================================

if __name__ == "__main__":
    # 基本统计测试
    data = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    
    print("=== 基本统计 ===")
    print(f"数据: {data}")
    print(f"均值: {mean(data)}")
    print(f"中位数: {median(data)}")
    print(f"众数: {mode(data)}")
    print(f"方差: {variance(data)}")
    print(f"标准差: {std_dev(data)}")
    print(f"四分位数: {quartiles(data)}")
    print(f"IQR: {iqr(data)}")
    print(f"偏度: {skewness(data)}")
    print(f"峰度: {kurtosis(data)}")
    
    print("\n=== 描述性统计 ===")
    stats = descriptive_stats(data)
    for key, value in stats.items():
        print(f"{key}: {value}")
    
    # 序列生成测试
    print("\n=== 序列生成 ===")
    print(f"等差数列: {arange(0, 10, 2)}")
    print(f"等间隔数列: {linspace(0, 1, 5)}")
    print(f"对数等间隔数列: {logspace(0, 2, 5)}")
    print(f"等比数列: {geometric_sequence(1, 2, 5)}")
    print(f"斐波那契数列: {fibonacci(10)}")
    print(f"质数: {prime_numbers(10)}")
    print(f"三角形数: {triangular_numbers(5)}")
    print(f"平方数: {square_numbers(5)}")
    print(f"立方数: {cube_numbers(5)}")
    
    # 变换测试
    print("\n=== 变换 ===")
    data2 = [10, 20, 30, 40, 50]
    print(f"原始数据: {data2}")
    print(f"归一化(minmax): {normalize(data2)}")
    print(f"标准化(zscore): {standardize(data2)}")
    print(f"差分: {differentiate(data2)}")
    print(f"累积和: {cumulative_sum(data2)}")
    print(f"指数平滑: {exponential_smoothing(data2, 0.3)}")
    print(f"移动平均: {moving_average(data2, 3)}")
    
    # 滑动窗口测试
    print("\n=== 滑动窗口 ===")
    print(f"滑动窗口: {sliding_window(data, 3)}")
    print(f"滚动最大值: {rolling_max(data, 3)}")
    print(f"滚动最小值: {rolling_min(data, 3)}")
    print(f"滚动求和: {rolling_sum(data, 3)}")
    
    # 异常值检测测试
    print("\n=== 异常值检测 ===")
    outlier_data = [1, 2, 3, 4, 5, 100, 6, 7, 8, 9, 10]
    print(f"含异常值的数据: {outlier_data}")
    print(f"Z-score 异常值索引: {zscore_outliers(outlier_data)}")
    print(f"IQR 异常值索引: {iqr_outliers(outlier_data)}")
    print(f"移除异常值后: {remove_outliers(outlier_data)}")
    
    # 相似度测试
    print("\n=== 序列相似度 ===")
    seq_a = [1, 2, 3, 4, 5]
    seq_b = [1.1, 2.1, 3.1, 4.1, 5.1]
    print(f"序列 A: {seq_a}")
    print(f"序列 B: {seq_b}")
    print(f"欧几里得距离: {euclidean_distance(seq_a, seq_b):.4f}")
    print(f"曼哈顿距离: {manhattan_distance(seq_a, seq_b):.4f}")
    print(f"余弦相似度: {cosine_similarity(seq_a, seq_b):.4f}")
    print(f"皮尔逊相关系数: {pearson_correlation(seq_a, seq_b):.4f}")
    
    # 趋势检测测试
    print("\n=== 趋势检测 ===")
    trend_data = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    print(f"单调递增: {is_monotonic(trend_data)}")
    print(f"严格递增: {is_increasing(trend_data, strict=True)}")
    print(f"趋势方向: {trend_direction(trend_data)}")
    
    # 峰值检测
    peak_data = [1, 3, 2, 4, 1, 5, 2, 3, 1]
    print(f"数据: {peak_data}")
    print(f"峰值索引: {find_peaks(peak_data)}")
    print(f"谷值索引: {find_valleys(peak_data)}")
    
    print("\n=== 测试完成 ===")