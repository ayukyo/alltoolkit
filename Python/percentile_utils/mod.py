"""
百分位数计算工具模块 (Percentile Utils)

提供多种百分位数计算方法和相关统计功能。
零外部依赖，纯 Python 实现。

核心功能：
- 多种百分位数计算方法（线性插值、最近邻等）
- 四分位数计算（Q1, Q2, Q3, IQR）
- 百分位排名计算
- 箱线图数据计算
- 分组百分位数计算

作者: AllToolkit
日期: 2026-05-02
"""

from typing import List, Optional, Union, Tuple, Dict
from enum import Enum
import math


class InterpolationMethod(Enum):
    """百分位数插值方法"""
    LINEAR = "linear"           # 线性插值（默认）
    LOWER = "lower"            # 取下界值
    HIGHER = "higher"          # 取上界值
    NEAREST = "nearest"        # 取最近值
    MIDPOINT = "midpoint"      # 取中点值
    EXCLUSIVE = "exclusive"    # 排除法（Excel PERCENTILE.EXC）
    INCLUSIVE = "inclusive"    # 包含法（Excel PERCENTILE.INC）


def _validate_data(data: List[Union[int, float]]) -> List[float]:
    """验证并转换数据"""
    if not data:
        raise ValueError("数据列表不能为空")
    
    result = []
    for i, val in enumerate(data):
        if not isinstance(val, (int, float)):
            raise TypeError(f"数据必须是数值类型，位置 {i} 发现 {type(val).__name__}")
        if math.isnan(val) or math.isinf(val):
            raise ValueError(f"数据包含无效值（NaN或无穷大），位置 {i}")
        result.append(float(val))
    
    return result


def _validate_percentile(p: float) -> None:
    """验证百分位数范围"""
    if not isinstance(p, (int, float)):
        raise TypeError(f"百分位数值必须是数值类型，发现 {type(p).__name__}")
    if not 0 <= p <= 100:
        raise ValueError(f"百分位数必须在 0-100 之间，发现 {p}")


def percentile(
    data: List[Union[int, float]],
    p: float,
    method: InterpolationMethod = InterpolationMethod.LINEAR,
    sorted_data: bool = False
) -> float:
    """
    计算数据的第 p 百分位数
    
    Args:
        data: 数值数据列表
        p: 百分位数（0-100）
        method: 插值方法
        sorted_data: 数据是否已排序（True可提升性能）
    
    Returns:
        第 p 百分位数的值
    
    Examples:
        >>> percentile([1, 2, 3, 4, 5], 50)
        3.0
        >>> percentile([1, 2, 3, 4, 5], 25, InterpolationMethod.LINEAR)
        2.0
        >>> percentile([1, 2, 3, 4, 5], 75, InterpolationMethod.NEAREST)
        4.0
    """
    validated_data = _validate_data(data)
    _validate_percentile(p)
    
    if len(validated_data) == 1:
        return validated_data[0]
    
    # 排序数据
    if not sorted_data:
        validated_data = sorted(validated_data)
    
    n = len(validated_data)
    
    # 特殊情况处理
    if p == 0:
        return validated_data[0]
    if p == 100:
        return validated_data[-1]
    
    if method == InterpolationMethod.LINEAR:
        # 线性插值：最常用的方法
        # numpy.percentile 默认方法
        rank = (p / 100) * (n - 1)
        lower_idx = int(rank)
        upper_idx = lower_idx + 1
        
        if upper_idx >= n:
            return validated_data[-1]
        
        fraction = rank - lower_idx
        return validated_data[lower_idx] + fraction * (validated_data[upper_idx] - validated_data[lower_idx])
    
    elif method == InterpolationMethod.LOWER:
        # 取下界值
        idx = int(math.floor((p / 100) * (n - 1)))
        return validated_data[idx]
    
    elif method == InterpolationMethod.HIGHER:
        # 取上界值
        idx = int(math.ceil((p / 100) * (n - 1)))
        return validated_data[min(idx, n - 1)]
    
    elif method == InterpolationMethod.NEAREST:
        # 取最近值
        idx = round((p / 100) * (n - 1))
        return validated_data[idx]
    
    elif method == InterpolationMethod.MIDPOINT:
        # 取中点值
        rank = (p / 100) * (n - 1)
        lower_idx = int(rank)
        upper_idx = min(lower_idx + 1, n - 1)
        return (validated_data[lower_idx] + validated_data[upper_idx]) / 2
    
    elif method == InterpolationMethod.EXCLUSIVE:
        # Excel PERCENTILE.EXC 方法
        # 排除端点，需要 n >= 4
        if n < 4:
            raise ValueError(f"exclusive 方法需要至少 4 个数据点，发现 {n} 个")
        
        rank = (p / 100) * (n + 1)
        
        if rank < 1 or rank > n:
            raise ValueError(f"exclusive 方法下，百分位数 p 必须在 {100/(n+1):.1f} 到 {100*n/(n+1):.1f} 之间")
        
        idx = rank - 1
        lower_idx = int(idx)
        upper_idx = lower_idx + 1
        fraction = idx - lower_idx
        
        return validated_data[lower_idx] + fraction * (validated_data[upper_idx] - validated_data[lower_idx])
    
    elif method == InterpolationMethod.INCLUSIVE:
        # Excel PERCENTILE.INC 方法
        # 与 linear 类似
        rank = (p / 100) * (n - 1)
        lower_idx = int(rank)
        upper_idx = min(lower_idx + 1, n - 1)
        fraction = rank - lower_idx
        
        return validated_data[lower_idx] + fraction * (validated_data[upper_idx] - validated_data[lower_idx])
    
    else:
        raise ValueError(f"未知的插值方法: {method}")


def quartiles(
    data: List[Union[int, float]],
    method: InterpolationMethod = InterpolationMethod.LINEAR,
    sorted_data: bool = False
) -> Dict[str, float]:
    """
    计算四分位数
    
    Args:
        data: 数值数据列表
        method: 插值方法
        sorted_data: 数据是否已排序
    
    Returns:
        包含 Q1, Q2 (中位数), Q3 和 IQR 的字典
    
    Examples:
        >>> quartiles([1, 2, 3, 4, 5, 6, 7, 8, 9])
        {'Q1': 2.5, 'Q2': 5.0, 'Q3': 7.5, 'IQR': 5.0}
    """
    validated_data = _validate_data(data)
    
    if not sorted_data:
        validated_data = sorted(validated_data)
    
    q1 = percentile(validated_data, 25, method, sorted_data=True)
    q2 = percentile(validated_data, 50, method, sorted_data=True)
    q3 = percentile(validated_data, 75, method, sorted_data=True)
    
    return {
        'Q1': q1,
        'Q2': q2,
        'Q3': q3,
        'IQR': q3 - q1
    }


def percentile_rank(
    data: List[Union[int, float]],
    value: Union[int, float],
    method: InterpolationMethod = InterpolationMethod.LINEAR,
    sorted_data: bool = False
) -> float:
    """
    计算某个值在数据集中的百分位排名
    
    Args:
        data: 数值数据列表
        value: 要计算排名的值
        method: 插值方法
        sorted_data: 数据是否已排序
    
    Returns:
        该值的百分位排名（0-100）
    
    Examples:
        >>> percentile_rank([1, 2, 3, 4, 5], 3)
        50.0
        >>> percentile_rank([1, 2, 3, 4, 5], 2.5)
        37.5
    """
    validated_data = _validate_data(data)
    
    if not isinstance(value, (int, float)):
        raise TypeError(f"value 必须是数值类型，发现 {type(value).__name__}")
    
    if not sorted_data:
        validated_data = sorted(validated_data)
    
    n = len(validated_data)
    
    # 统计小于和等于该值的数量
    count_below = 0
    count_equal = 0
    
    for val in validated_data:
        if val < value:
            count_below += 1
        elif val == value:
            count_equal += 1
    
    if count_equal == 0:
        # 值不在数据中，使用线性插值
        for i in range(n - 1):
            if validated_data[i] < value < validated_data[i + 1]:
                fraction = (value - validated_data[i]) / (validated_data[i + 1] - validated_data[i])
                rank = ((count_below + fraction) / n) * 100
                return round(rank, 2)
        # 超出范围
        if value < validated_data[0]:
            return 0.0
        return 100.0
    
    # 使用公式：(小于的数量 + 0.5 * 等于的数量) / 总数 * 100
    rank = ((count_below + 0.5 * count_equal) / n) * 100
    return round(rank, 2)


def boxplot_stats(
    data: List[Union[int, float]],
    method: InterpolationMethod = InterpolationMethod.LINEAR,
    sorted_data: bool = False,
    whisker_multiplier: float = 1.5
) -> Dict[str, Union[float, List[float]]]:
    """
    计算箱线图统计数据
    
    Args:
        data: 数值数据列表
        method: 插值方法
        sorted_data: 数据是否已排序
        whisker_multiplier: 须长乘数（默认 1.5，用于识别异常值）
    
    Returns:
        包含 min, Q1, median, Q3, max, IQR, lower_whisker, upper_whisker, outliers
    
    Examples:
        >>> boxplot_stats([1, 2, 3, 4, 5, 6, 7, 8, 9, 100])
        {'min': 1, 'Q1': 2.5, 'median': 5.5, 'Q3': 8.5, 'max': 100, 'IQR': 6.0, 
         'lower_whisker': 1, 'upper_whisker': 9, 'outliers': [100]}
    """
    validated_data = _validate_data(data)
    
    if not sorted_data:
        validated_data = sorted(validated_data)
    
    qs = quartiles(validated_data, method, sorted_data=True)
    q1, q3, iqr = qs['Q1'], qs['Q3'], qs['IQR']
    median = qs['Q2']
    
    # 计算须长边界
    lower_bound = q1 - whisker_multiplier * iqr
    upper_bound = q3 + whisker_multiplier * iqr
    
    # 找到实际的须长端点
    lower_whisker = validated_data[0]
    upper_whisker = validated_data[-1]
    
    for val in validated_data:
        if lower_bound <= val <= upper_bound:
            if val < lower_whisker:
                lower_whisker = val
            if val > upper_whisker:
                upper_whisker = val
    
    # 找异常值
    outliers = [val for val in validated_data if val < lower_bound or val > upper_bound]
    
    return {
        'min': validated_data[0],
        'Q1': q1,
        'median': median,
        'Q3': q3,
        'max': validated_data[-1],
        'IQR': iqr,
        'lower_whisker': lower_whisker,
        'upper_whisker': upper_whisker,
        'lower_bound': lower_bound,
        'upper_bound': upper_bound,
        'outliers': outliers
    }


def deciles(
    data: List[Union[int, float]],
    method: InterpolationMethod = InterpolationMethod.LINEAR,
    sorted_data: bool = False
) -> List[float]:
    """
    计算十分位数（将数据分为10等份）
    
    Args:
        data: 数值数据列表
        method: 插值方法
        sorted_data: 数据是否已排序
    
    Returns:
        10个十分位数值的列表（D0=0% 到 D9=90%）
    
    Examples:
        >>> deciles(list(range(1, 101)))
        [10.0, 20.0, 30.0, 40.0, 50.0, 60.0, 70.0, 80.0, 90.0, 100.0]
    """
    validated_data = _validate_data(data)
    
    if not sorted_data:
        validated_data = sorted(validated_data)
    
    return [percentile(validated_data, i * 10, method, sorted_data=True) for i in range(10)]


def percentiles(
    data: List[Union[int, float]],
    p_list: List[float],
    method: InterpolationMethod = InterpolationMethod.LINEAR,
    sorted_data: bool = False
) -> Dict[float, float]:
    """
    批量计算多个百分位数
    
    Args:
        data: 数值数据列表
        p_list: 百分位数列表（0-100）
        method: 插值方法
        sorted_data: 数据是否已排序
    
    Returns:
        百分位数到对应值的映射字典
    
    Examples:
        >>> percentiles([1, 2, 3, 4, 5], [10, 25, 50, 75, 90])
        {10: 1.4, 25: 2.0, 50: 3.0, 75: 4.0, 90: 4.6}
    """
    validated_data = _validate_data(data)
    
    for p in p_list:
        _validate_percentile(p)
    
    if not sorted_data:
        validated_data = sorted(validated_data)
    
    return {p: percentile(validated_data, p, method, sorted_data=True) for p in p_list}


def grouped_percentile(
    groups: Dict[str, List[Union[int, float]]],
    p: float,
    method: InterpolationMethod = InterpolationMethod.LINEAR
) -> Dict[str, float]:
    """
    计算分组数据的百分位数
    
    Args:
        groups: 分组名称到数据列表的映射
        p: 百分位数（0-100）
        method: 插值方法
    
    Returns:
        每个组的百分位数值
    
    Examples:
        >>> grouped_percentile({
        ...     'A': [1, 2, 3, 4, 5],
        ...     'B': [10, 20, 30, 40, 50]
        ... }, 50)
        {'A': 3.0, 'B': 30.0}
    """
    if not groups:
        raise ValueError("分组数据不能为空")
    
    result = {}
    for group_name, group_data in groups.items():
        result[group_name] = percentile(group_data, p, method)
    
    return result


def percentile_summary(
    data: List[Union[int, float]],
    method: InterpolationMethod = InterpolationMethod.LINEAR
) -> Dict[str, Union[float, Dict[str, float]]]:
    """
    生成完整的百分位数统计摘要
    
    Args:
        data: 数值数据列表
        method: 插值方法
    
    Returns:
        完整的统计摘要，包括基本统计量和各种百分位数
    
    Examples:
        >>> summary = percentile_summary([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
        >>> summary['count']
        10
        >>> summary['percentiles']['50']
        5.5
    """
    validated_data = _validate_data(data)
    sorted_data = sorted(validated_data)
    n = len(sorted_data)
    
    # 计算基本统计量
    total = sum(sorted_data)
    mean = total / n
    
    # 计算方差和标准差
    variance = sum((x - mean) ** 2 for x in sorted_data) / n
    std_dev = math.sqrt(variance)
    
    # 计算百分位数
    percentile_values = percentiles(
        sorted_data,
        [5, 10, 25, 50, 75, 90, 95],
        method,
        sorted_data=True
    )
    
    qs = quartiles(sorted_data, method, sorted_data=True)
    
    return {
        'count': n,
        'min': sorted_data[0],
        'max': sorted_data[-1],
        'sum': total,
        'mean': mean,
        'variance': variance,
        'std_dev': std_dev,
        'quartiles': qs,
        'percentiles': percentile_values,
        'range': sorted_data[-1] - sorted_data[0],
        'median': percentile_values[50]
    }


def is_outlier(
    value: Union[int, float],
    data: List[Union[int, float]],
    whisker_multiplier: float = 1.5,
    method: InterpolationMethod = InterpolationMethod.LINEAR
) -> bool:
    """
    判断某个值是否为异常值
    
    Args:
        value: 要判断的值
        data: 数据集
        whisker_multiplier: 须长乘数（默认 1.5）
        method: 插值方法
    
    Returns:
        是否为异常值
    
    Examples:
        >>> is_outlier(100, [1, 2, 3, 4, 5, 6, 7, 8, 9])
        True
        >>> is_outlier(5, [1, 2, 3, 4, 5, 6, 7, 8, 9])
        False
    """
    stats = boxplot_stats(data, method, whisker_multiplier=whisker_multiplier)
    return value < stats['lower_bound'] or value > stats['upper_bound']


def normalize_by_percentile(
    data: List[Union[int, float]],
    lower_percentile: float = 25,
    upper_percentile: float = 75,
    method: InterpolationMethod = InterpolationMethod.LINEAR
) -> List[float]:
    """
    使用百分位数范围归一化数据
    
    Args:
        data: 数值数据列表
        lower_percentile: 下界百分位数（默认 25，即 Q1）
        upper_percentile: 上界百分位数（默认 75，即 Q3）
        method: 插值方法
    
    Returns:
        归一化后的数据列表
    
    Examples:
        >>> normalize_by_percentile([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
        [-1.0, -0.667, -0.333, 0.0, 0.333, 0.667, 1.0, 1.333, 1.667, 2.0]
    """
    validated_data = _validate_data(data)
    
    lower_val = percentile(validated_data, lower_percentile, method)
    upper_val = percentile(validated_data, upper_percentile, method)
    
    iqr = upper_val - lower_val
    
    if iqr == 0:
        # 如果 IQR 为 0，返回零均值数据
        mean = sum(validated_data) / len(validated_data)
        return [x - mean for x in validated_data]
    
    return [(x - lower_val) / iqr for x in validated_data]


def winsorize(
    data: List[Union[int, float]],
    lower_percentile: float = 5,
    upper_percentile: float = 95,
    method: InterpolationMethod = InterpolationMethod.LINEAR
) -> List[float]:
    """
    缩尾处理：将极端值替换为百分位数值
    
    Args:
        data: 数值数据列表
        lower_percentile: 下界百分位数（默认 5）
        upper_percentile: 上界百分位数（默认 95）
        method: 插值方法
    
    Returns:
        缩尾处理后的数据列表
    
    Examples:
        >>> winsorize([1, 2, 3, 4, 5, 6, 7, 8, 9, 100], 10, 90)
        [1.9, 2, 3, 4, 5, 6, 7, 8, 9, 9.1]
    """
    validated_data = _validate_data(data)
    
    lower_val = percentile(validated_data, lower_percentile, method)
    upper_val = percentile(validated_data, upper_percentile, method)
    
    result = []
    for x in validated_data:
        if x < lower_val:
            result.append(lower_val)
        elif x > upper_val:
            result.append(upper_val)
        else:
            result.append(x)
    
    return result


if __name__ == "__main__":
    # 简单测试
    test_data = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    
    print("=== 百分位数工具测试 ===\n")
    
    # 基本百分位数
    print(f"数据: {test_data}")
    print(f"P50 (中位数): {percentile(test_data, 50)}")
    print(f"P25: {percentile(test_data, 25)}")
    print(f"P75: {percentile(test_data, 75)}")
    
    # 四分位数
    print(f"\n四分位数: {quartiles(test_data)}")
    
    # 百分位排名
    print(f"\n值 5.5 的百分位排名: {percentile_rank(test_data, 5.5)}")
    
    # 箱线图统计
    test_data_with_outlier = [1, 2, 3, 4, 5, 6, 7, 8, 9, 100]
    print(f"\n含异常值的数据: {test_data_with_outlier}")
    stats = boxplot_stats(test_data_with_outlier)
    print(f"箱线图统计: {stats}")
    
    # 十分位数
    print(f"\n十分位数: {deciles(test_data)}")
    
    # 缩尾处理
    print(f"\n缩尾处理: {winsorize(test_data_with_outlier, 10, 90)}")
    
    # 完整摘要
    summary = percentile_summary(test_data)
    print(f"\n完整摘要:")
    for key, value in summary.items():
        if isinstance(value, dict):
            print(f"  {key}:")
            for k, v in value.items():
                print(f"    {k}: {v}")
        else:
            print(f"  {key}: {value}")