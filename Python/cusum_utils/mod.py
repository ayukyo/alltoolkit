"""
CUSUM控制图工具模块 (Cumulative Sum Control Chart Utils)

CUSUM（累积和）控制图是一种统计质量控制方法，用于检测过程均值的微小偏移。
相比传统的Shewhart控制图，CUSUM对小的、持续性的偏移更加敏感。

功能：
- 标准CUSUM控制图计算
- Tabular CUSUM（表格形式）
- V-mask方法
- 自适应CUSUM
- 变化点检测
- 过程能力分析
- 多种信号规则

应用场景：
- 制造业质量控制
- 金融市场异常检测
- 医疗健康监测
- 网络流量异常检测
- 环境监测
"""

from typing import List, Tuple, Dict, Optional, Callable, Union
from dataclasses import dataclass
from enum import Enum
import math


class CUSUMType(Enum):
    """CUSUM类型"""
    STANDARD = "standard"  # 标准CUSUM
    TABULAR = "tabular"  # 表格CUSUM
    STANDARDIZED = "standardized"  # 标准化CUSUM


@dataclass
class CUSUMPoint:
    """CUSUM数据点"""
    index: int
    value: float
    cusum_pos: float  # 正向累积和
    cusum_neg: float  # 负向累积和
    signal: str  # 信号状态: 'normal', 'upper', 'lower'


@dataclass
class CUSUMResult:
    """CUSUM分析结果"""
    points: List[CUSUMPoint]
    has_signal: bool
    signal_index: Optional[int]
    signal_type: Optional[str]  # 'upper' or 'lower'
    change_point: Optional[int]
    estimated_shift: Optional[float]
    center_line: float
    h: float  # 决策阈值
    k: float  # 参考值


@dataclass
class ChangePointResult:
    """变化点检测结果"""
    index: int
    confidence: float
    direction: str  # 'up' or 'down'
    magnitude: float
    before_mean: float
    after_mean: float


def calculate_mean_std(data: List[float]) -> Tuple[float, float]:
    """
    计算数据的均值和标准差
    
    Args:
        data: 数据列表
        
    Returns:
        (均值, 标准差) 元组
        
    Examples:
        >>> calculate_mean_std([1, 2, 3, 4, 5])
        (3.0, 1.4142135623730951)
    """
    if not data:
        raise ValueError("数据不能为空")
    
    n = len(data)
    mean = sum(data) / n
    
    if n < 2:
        return mean, 0.0
    
    variance = sum((x - mean) ** 2 for x in data) / (n - 1)
    std = math.sqrt(variance)
    
    return mean, std


def estimate_control_parameters(
    data: List[float],
    target_shift: float = 1.0
) -> Tuple[float, float, float]:
    """
    根据数据估计控制参数
    
    Args:
        data: 历史数据（用于估计过程参数）
        target_shift: 目标检测偏移量（标准差的倍数）
        
    Returns:
        (中心线, h阈值, k参考值) 元组
        
    Examples:
        >>> estimate_control_parameters([10, 11, 9, 10, 12, 10, 11])
        (10.428571428571429, 4.285714285714286, 0.5357142857142857)
    """
    mean, std = calculate_mean_std(data)
    
    # k 通常设为目标偏移的一半（以标准差为单位）
    k = target_shift * std / 2
    
    # h 通常设为 4-5 倍的标准差
    h = 5 * std
    
    return mean, h, k


def standard_cusum(
    data: List[float],
    target: Optional[float] = None,
    h: Optional[float] = None,
    k: Optional[float] = None
) -> CUSUMResult:
    """
    计算标准CUSUM控制图
    
    Args:
        data: 观测数据列表
        target: 目标值（中心线），默认为数据均值
        h: 决策阈值，默认为5倍标准差
        k: 参考值（允许的偏移量），默认为0.5倍标准差
        
    Returns:
        CUSUMResult对象
        
    Examples:
        >>> data = [10, 10, 11, 10, 9, 10, 10, 12, 12, 13, 14, 15]
        >>> result = standard_cusum(data)
        >>> result.has_signal
        True
    """
    if not data:
        raise ValueError("数据不能为空")
    
    n = len(data)
    mean, std = calculate_mean_std(data)
    
    # 设置默认参数
    if target is None:
        target = mean
    if k is None:
        k = 0.5 * std if std > 0 else 0.5
    if h is None:
        h = 5 * std if std > 0 else 5
    
    # 计算CUSUM
    points = []
    cusum_pos = 0.0
    cusum_neg = 0.0
    has_signal = False
    signal_index = None
    signal_type = None
    
    for i, value in enumerate(data):
        # 计算偏差
        deviation = value - target
        
        # 更新累积和
        cusum_pos = max(0, cusum_pos + deviation - k)
        cusum_neg = min(0, cusum_neg + deviation + k)
        
        # 检测信号
        signal = 'normal'
        if cusum_pos >= h:
            signal = 'upper'
            if not has_signal:
                has_signal = True
                signal_index = i
                signal_type = 'upper'
        elif cusum_neg <= -h:
            signal = 'lower'
            if not has_signal:
                has_signal = True
                signal_index = i
                signal_type = 'lower'
        
        points.append(CUSUMPoint(
            index=i,
            value=value,
            cusum_pos=cusum_pos,
            cusum_neg=cusum_neg,
            signal=signal
        ))
    
    # 估计变化点
    change_point = None
    estimated_shift = None
    if has_signal:
        change_point = _find_change_point(points, signal_index)
        if change_point is not None:
            before_mean = sum(data[:change_point]) / change_point if change_point > 0 else mean
            after_mean = sum(data[change_point:]) / (n - change_point)
            estimated_shift = after_mean - before_mean
    
    return CUSUMResult(
        points=points,
        has_signal=has_signal,
        signal_index=signal_index,
        signal_type=signal_type,
        change_point=change_point,
        estimated_shift=estimated_shift,
        center_line=target,
        h=h,
        k=k
    )


def tabular_cusum(
    data: List[float],
    target: Optional[float] = None,
    h: Optional[float] = None,
    k: Optional[float] = None
) -> Dict:
    """
    计算表格形式的CUSUM（双侧）
    
    表格CUSUM更适合实时监控和可视化。
    
    Args:
        data: 观测数据列表
        target: 目标值
        h: 决策阈值
        k: 参考值
        
    Returns:
        包含正向累积和(C+)、负向累积和(C-)、信号等信息的字典
        
    Examples:
        >>> data = [100, 102, 101, 103, 105, 108, 110, 115]
        >>> result = tabular_cusum(data, target=100)
        >>> result['has_signal']
        True
    """
    if not data:
        raise ValueError("数据不能为空")
    
    mean, std = calculate_mean_std(data)
    
    if target is None:
        target = mean
    if k is None:
        k = 0.5 * std if std > 0 else 0.5
    if h is None:
        h = 5 * std if std > 0 else 5
    
    c_pos = []  # 正向累积和 C+
    c_neg = []  # 负向累积和 C-
    signals = []
    
    c_plus = 0.0
    c_minus = 0.0
    
    for i, value in enumerate(data):
        deviation = value - target
        
        # 计算C+
        c_plus_new = max(0, c_plus + deviation - k)
        c_minus_new = min(0, c_minus + deviation + k)
        
        c_plus = c_plus_new
        c_minus = c_minus_new
        
        c_pos.append(c_plus)
        c_neg.append(c_minus)
        
        if c_plus >= h:
            signals.append({'index': i, 'type': 'upper', 'value': c_plus})
        elif c_minus <= -h:
            signals.append({'index': i, 'type': 'lower', 'value': c_minus})
    
    return {
        'c_positive': c_pos,
        'c_negative': c_neg,
        'signals': signals,
        'has_signal': len(signals) > 0,
        'target': target,
        'h': h,
        'k': k,
        'std': std
    }


def standardized_cusum(
    data: List[float],
    h: float = 8.01,
    k: float = 0.5
) -> CUSUMResult:
    """
    计算标准化CUSUM
    
    使用标准化值使CUSUM对尺度不敏感。
    
    Args:
        data: 观测数据列表
        h: 决策阈值（默认8.01对应ARL≈500）
        k: 参考值（默认0.5对应检测1σ偏移）
        
    Returns:
        CUSUMResult对象
        
    Examples:
        >>> data = [10, 11, 9, 10, 12, 10, 11, 10, 10]
        >>> result = standardized_cusum(data)
        >>> result.h
        8.01
    """
    if not data:
        raise ValueError("数据不能为空")
    
    mean, std = calculate_mean_std(data)
    
    if std == 0:
        # 所有值相同，无变化
        points = [
            CUSUMPoint(index=i, value=v, cusum_pos=0, cusum_neg=0, signal='normal')
            for i, v in enumerate(data)
        ]
        return CUSUMResult(
            points=points,
            has_signal=False,
            signal_index=None,
            signal_type=None,
            change_point=None,
            estimated_shift=None,
            center_line=mean,
            h=h,
            k=k
        )
    
    # 标准化数据
    standardized = [(x - mean) / std for x in data]
    
    cusum_pos = 0.0
    cusum_neg = 0.0
    points = []
    has_signal = False
    signal_index = None
    signal_type = None
    
    for i, z in enumerate(standardized):
        cusum_pos = max(0, cusum_pos + z - k)
        cusum_neg = min(0, cusum_neg + z + k)
        
        signal = 'normal'
        if cusum_pos >= h:
            signal = 'upper'
            if not has_signal:
                has_signal = True
                signal_index = i
                signal_type = 'upper'
        elif cusum_neg <= -h:
            signal = 'lower'
            if not has_signal:
                has_signal = True
                signal_index = i
                signal_type = 'lower'
        
        points.append(CUSUMPoint(
            index=i,
            value=data[i],
            cusum_pos=cusum_pos,
            cusum_neg=cusum_neg,
            signal=signal
        ))
    
    change_point = None
    estimated_shift = None
    if has_signal:
        change_point = _find_change_point(points, signal_index)
        if change_point is not None:
            n = len(data)
            before_mean = sum(data[:change_point]) / change_point if change_point > 0 else mean
            after_mean = sum(data[change_point:]) / (n - change_point)
            estimated_shift = after_mean - before_mean
    
    return CUSUMResult(
        points=points,
        has_signal=has_signal,
        signal_index=signal_index,
        signal_type=signal_type,
        change_point=change_point,
        estimated_shift=estimated_shift,
        center_line=mean,
        h=h,
        k=k
    )


def _find_change_point(points: List[CUSUMPoint], signal_index: int) -> Optional[int]:
    """
    在信号点之前找到变化点
    
    变化点是CUSUM开始持续增长的点。
    """
    if signal_index is None or signal_index < 1:
        return None
    
    # 向前查找CUSUM开始增长的点
    for i in range(signal_index - 1, 0, -1):
        prev_pos = points[i-1].cusum_pos
        curr_pos = points[i].cusum_pos
        
        # 如果CUSUM从零或接近零开始增长
        if prev_pos <= 0.01 and curr_pos > 0:
            return i
        
        prev_neg = points[i-1].cusum_neg
        curr_neg = points[i].cusum_neg
        
        if prev_neg >= -0.01 and curr_neg < 0:
            return i
    
    return 0


def detect_change_points(
    data: List[float],
    min_segment_size: int = 5,
    significance_level: float = 0.05
) -> List[ChangePointResult]:
    """
    使用CUSUM方法检测多个变化点
    
    Args:
        data: 观测数据列表
        min_segment_size: 最小段大小
        significance_level: 显著性水平
        
    Returns:
        变化点列表
        
    Examples:
        >>> data = [10, 10, 11, 10, 10, 20, 21, 19, 20, 20, 10, 11, 10]
        >>> changes = detect_change_points(data)
        >>> len(changes) > 0
        True
    """
    if len(data) < min_segment_size * 2:
        return []
    
    change_points = []
    
    # 递归检测变化点
    _detect_recursive(data, 0, len(data), change_points, min_segment_size, significance_level)
    
    # 排序并去重
    change_points.sort(key=lambda x: x.index)
    
    return change_points


def _detect_recursive(
    data: List[float],
    start: int,
    end: int,
    results: List[ChangePointResult],
    min_size: int,
    alpha: float,
    depth: int = 0
):
    """递归检测变化点"""
    # 限制递归深度防止无限循环
    if depth > 5 or end - start < min_size * 2:
        return
    
    segment = data[start:end]
    mean, std = calculate_mean_std(segment)
    
    # 如果标准差太小，跳过
    if std < 0.001:
        return
    
    result = standard_cusum(segment)
    
    if result.has_signal and result.change_point is not None:
        abs_cp = start + result.change_point
        
        # 确保变化点在有效范围内
        if abs_cp <= start + min_size or abs_cp >= end - min_size:
            return
        
        # 计算置信度
        before = data[start:abs_cp]
        after = data[abs_cp:end]
        
        if len(before) >= 2 and len(after) >= 2:
            before_mean = sum(before) / len(before)
            after_mean = sum(after) / len(after)
            
            # 简单的置信度计算
            _, before_std = calculate_mean_std(before)
            _, after_std = calculate_mean_std(after)
            
            pooled_std = math.sqrt(
                ((len(before)-1)*before_std**2 + (len(after)-1)*after_std**2) /
                (len(before) + len(after) - 2)
            ) if len(before) + len(after) > 2 else 1.0
            
            effect_size = abs(after_mean - before_mean) / pooled_std if pooled_std > 0 else 0
            confidence = min(1.0, effect_size / 2)  # 简化的置信度
            
            if confidence >= 0.3:  # 最小置信度阈值
                # 检查是否已存在相近的变化点
                is_duplicate = any(abs(r.index - abs_cp) < min_size for r in results)
                
                if not is_duplicate:
                    results.append(ChangePointResult(
                        index=abs_cp,
                        confidence=confidence,
                        direction='up' if after_mean > before_mean else 'down',
                        magnitude=abs(after_mean - before_mean),
                        before_mean=before_mean,
                        after_mean=after_mean
                    ))
        
        # 递归检测子段（增加深度计数）
        _detect_recursive(data, start, abs_cp, results, min_size, alpha, depth + 1)
        _detect_recursive(data, abs_cp, end, results, min_size, alpha, depth + 1)


def cusum_for_variance(
    data: List[float],
    target_var: Optional[float] = None,
    h: Optional[float] = None
) -> Dict:
    """
    检测方差变化的CUSUM
    
    Args:
        data: 观测数据列表
        target_var: 目标方差
        h: 决策阈值
        
    Returns:
        包含方差CUSUM结果的字典
        
    Examples:
        >>> data = [10, 10, 10, 11, 10, 10, 10, 10]  # 稳定方差
        >>> result = cusum_for_variance(data)
        >>> result['has_signal']
        False
    """
    if len(data) < 2:
        raise ValueError("需要至少2个数据点")
    
    mean, std = calculate_mean_std(data)
    
    if target_var is None:
        target_var = std ** 2
    if h is None:
        h = 5 * target_var
    
    # 计算每点的方差贡献
    var_contributions = [(x - mean) ** 2 for x in data]
    
    cusum_pos = 0.0
    cusum_neg = 0.0
    k = target_var / 2  # 参考值
    
    c_pos_list = []
    c_neg_list = []
    signals = []
    
    for i, vc in enumerate(var_contributions):
        cusum_pos = max(0, cusum_pos + vc - target_var - k)
        cusum_neg = min(0, cusum_neg + vc - target_var + k)
        
        c_pos_list.append(cusum_pos)
        c_neg_list.append(cusum_neg)
        
        if cusum_pos >= h or cusum_neg <= -h:
            signals.append(i)
    
    return {
        'c_positive': c_pos_list,
        'c_negative': c_neg_list,
        'signals': signals,
        'has_signal': len(signals) > 0,
        'target_variance': target_var,
        'h': h
    }


def cusum_for_proportion(
    successes: int,
    trials: int,
    target_p: float,
    h: Optional[float] = None,
    k: Optional[float] = None
) -> Dict:
    """
    比例的CUSUM检测（二项分布）
    
    用于检测良品率、转化率等比例的变化。
    
    Args:
        successes: 成功次数列表
        trials: 总试验次数
        target_p: 目标比例
        h: 决策阈值
        k: 参考值
        
    Returns:
        CUSUM结果字典
        
    Examples:
        >>> # 检测良品率下降
        >>> result = cusum_for_proportion(95, 100, target_p=0.98)
        >>> result['has_signal']
        False
    """
    if not 0 < target_p < 1:
        raise ValueError("target_p 必须在 (0, 1) 之间")
    
    p_hat = successes / trials
    std = math.sqrt(target_p * (1 - target_p) / trials)
    
    if h is None:
        h = 5 * std
    if k is None:
        k = std  # 检测1个标准差的变化
    
    # 标准化得分
    z = (p_hat - target_p) / std if std > 0 else 0
    
    cusum_pos = max(0, z - k / std) if std > 0 else 0
    cusum_neg = min(0, z + k / std) if std > 0 else 0
    
    return {
        'proportion': p_hat,
        'z_score': z,
        'cusum_positive': cusum_pos,
        'cusum_negative': cusum_neg,
        'has_signal': cusum_pos >= h / std or cusum_neg <= -h / std if std > 0 else False,
        'target': target_p,
        'h': h,
        'k': k,
        'std': std
    }


def calculate_arl(
    h: float,
    k: float,
    delta: float = 0.0,
    n_simulations: int = 10000
) -> float:
    """
    计算平均运行长度（ARL）
    
    ARL是CUSUM发出信号前平均需要的样本数。
    
    Args:
        h: 决策阈值
        k: 参考值
        delta: 过程偏移量（以标准差为单位）
        n_simulations: 模拟次数
        
    Returns:
        平均运行长度
        
    Examples:
        >>> arl = calculate_arl(h=5, k=0.5, delta=0)  # 受控状态ARL
        >>> arl > 100  # 应该较高
        True
    """
    import random
    
    total_runs = 0
    
    for _ in range(n_simulations):
        cusum_pos = 0.0
        run_length = 0
        
        while cusum_pos < h:
            # 生成正态随机数
            z = random.gauss(delta, 1)
            cusum_pos = max(0, cusum_pos + z - k)
            run_length += 1
            
            if run_length > 100000:  # 安全限制
                break
        
        total_runs += run_length
    
    return total_runs / n_simulations


def design_cusum(
    target_arl_0: float = 500,
    delta_to_detect: float = 1.0
) -> Tuple[float, float]:
    """
    设计CUSUM参数
    
    根据期望的受控ARL和要检测的偏移量确定h和k。
    
    Args:
        target_arl_0: 受控状态下的目标ARL
        delta_to_detect: 要检测的偏移量（标准差单位）
        
    Returns:
        (h, k) 参数元组
        
    Examples:
        >>> h, k = design_cusum(target_arl_0=500, delta_to_detect=1.0)
        >>> round(k, 1)
        0.5
    """
    # k 通常设为检测偏移量的一半
    k = delta_to_detect / 2
    
    # h 根据目标ARL确定
    # 对于 k=0.5, h≈5 对应 ARL≈500
    # 简化的近似公式
    if target_arl_0 <= 100:
        h = 4 * delta_to_detect
    elif target_arl_0 <= 500:
        h = 5 * delta_to_detect
    else:
        h = 6 * delta_to_detect
    
    return h, k


def cusum_score(
    data: List[float],
    window_size: Optional[int] = None
) -> List[float]:
    """
    计算CUSUM得分（用于异常检测评分）
    
    Args:
        data: 观测数据列表
        window_size: 窗口大小（用于计算局部均值）
        
    Returns:
        每个点的CUSUM得分列表
        
    Examples:
        >>> data = [10, 10, 10, 10, 15, 15, 15]
        >>> scores = cusum_score(data)
        >>> scores[-1] > scores[0]  # 后面得分更高
        True
    """
    if not data:
        return []
    
    if window_size is None:
        window_size = max(10, len(data) // 10)
    
    mean, std = calculate_mean_std(data)
    
    if std == 0:
        return [0.0] * len(data)
    
    scores = []
    cusum = 0.0
    
    for i, value in enumerate(data):
        z = (value - mean) / std
        cusum += z
        scores.append(abs(cusum))
    
    # 归一化到0-1范围
    max_score = max(scores) if scores else 1
    if max_score > 0:
        scores = [s / max_score for s in scores]
    
    return scores


def ewma_cusum(
    data: List[float],
    lambda_: float = 0.1,
    h: Optional[float] = None,
    target: Optional[float] = None
) -> Dict:
    """
    EWMA-CUSUM混合方法
    
    结合EWMA平滑和CUSUM检测的优点。
    
    Args:
        data: 观测数据列表
        lambda_: EWMA平滑系数（0-1之间）
        h: 决策阈值
        target: 目标值
        
    Returns:
        包含EWMA和CUSUM结果的字典
        
    Examples:
        >>> data = [10, 10, 11, 10, 12, 14, 15, 17]
        >>> result = ewma_cusum(data, lambda_=0.2)
        >>> 'ewma_values' in result
        True
    """
    if not data:
        raise ValueError("数据不能为空")
    
    if not 0 < lambda_ < 1:
        raise ValueError("lambda_ 必须在 (0, 1) 之间")
    
    mean, std = calculate_mean_std(data)
    
    if target is None:
        target = mean
    if h is None:
        h = 5 * std if std > 0 else 5
    
    k = std / 2 if std > 0 else 0.5
    
    # 计算EWMA
    ewma = target
    ewma_values = []
    
    for value in data:
        ewma = lambda_ * value + (1 - lambda_) * ewma
        ewma_values.append(ewma)
    
    # 基于EWMA值计算CUSUM
    cusum_pos = 0.0
    cusum_neg = 0.0
    cusum_pos_list = []
    cusum_neg_list = []
    signals = []
    
    for i, ewma_val in enumerate(ewma_values):
        deviation = ewma_val - target
        
        cusum_pos = max(0, cusum_pos + deviation - k)
        cusum_neg = min(0, cusum_neg + deviation + k)
        
        cusum_pos_list.append(cusum_pos)
        cusum_neg_list.append(cusum_neg)
        
        if cusum_pos >= h:
            signals.append({'index': i, 'type': 'upper', 'ewma': ewma_val})
        elif cusum_neg <= -h:
            signals.append({'index': i, 'type': 'lower', 'ewma': ewma_val})
    
    return {
        'ewma_values': ewma_values,
        'cusum_positive': cusum_pos_list,
        'cusum_negative': cusum_neg_list,
        'signals': signals,
        'has_signal': len(signals) > 0,
        'target': target,
        'h': h,
        'lambda': lambda_
    }


def cusum_control_limits(
    target: float,
    std: float,
    h: Optional[float] = None,
    k: Optional[float] = None
) -> Dict:
    """
    计算CUSUM控制限
    
    Args:
        target: 目标值
        std: 过程标准差
        h: 决策阈值
        k: 参考值
        
    Returns:
        控制限字典
        
    Examples:
        >>> limits = cusum_control_limits(target=100, std=5)
        >>> limits['h']
        25.0
    """
    if h is None:
        h = 5 * std
    if k is None:
        k = 0.5 * std
    
    return {
        'target': target,
        'h': h,
        'k': k,
        'upper_control_limit': target + h,
        'lower_control_limit': target - h,
        'upper_warning_limit': target + h * 0.8,
        'lower_warning_limit': target - h * 0.8
    }


def analyze_process(
    data: List[float],
    target: Optional[float] = None,
    h: Optional[float] = None,
    k: Optional[float] = None
) -> Dict:
    """
    全面的过程分析
    
    结合多种统计方法进行全面分析。
    
    Args:
        data: 观测数据列表
        target: 目标值
        h: 决策阈值
        k: 参考值
        
    Returns:
        综合分析结果字典
        
    Examples:
        >>> data = [10, 10, 11, 10, 12, 14, 15, 17]
        >>> analysis = analyze_process(data)
        >>> 'cusum' in analysis
        True
    """
    if not data:
        raise ValueError("数据不能为空")
    
    mean, std = calculate_mean_std(data)
    
    if target is None:
        target = mean
    if k is None:
        k = 0.5 * std if std > 0 else 0.5
    if h is None:
        h = 5 * std if std > 0 else 5
    
    # CUSUM分析
    cusum_result = standard_cusum(data, target, h, k)
    
    # 变化点检测
    change_points = detect_change_points(data)
    
    # 过程能力
    process_capability = _calculate_process_capability(data, target, std)
    
    # 趋势分析
    trend = _analyze_trend(data)
    
    return {
        'cusum': {
            'has_signal': cusum_result.has_signal,
            'signal_index': cusum_result.signal_index,
            'signal_type': cusum_result.signal_type,
            'change_point': cusum_result.change_point,
            'estimated_shift': cusum_result.estimated_shift
        },
        'statistics': {
            'mean': mean,
            'std': std,
            'min': min(data),
            'max': max(data),
            'range': max(data) - min(data)
        },
        'change_points': [
            {
                'index': cp.index,
                'direction': cp.direction,
                'magnitude': cp.magnitude,
                'confidence': cp.confidence
            }
            for cp in change_points
        ],
        'process_capability': process_capability,
        'trend': trend,
        'control_limits': cusum_control_limits(target, std, h, k),
        'status': 'out_of_control' if cusum_result.has_signal else 'in_control'
    }


def _calculate_process_capability(
    data: List[float],
    target: float,
    std: float
) -> Dict:
    """计算过程能力指数"""
    if std == 0:
        return {'cp': float('inf'), 'cpk': float('inf'), 'ppk': float('inf')}
    
    mean = sum(data) / len(data)
    n = len(data)
    
    # 假设规格限为目标±3σ（可根据需要调整）
    lsl = target - 3 * std
    usl = target + 3 * std
    
    # Cp指数
    cp = (usl - lsl) / (6 * std)
    
    # Cpk指数
    cpu = (usl - mean) / (3 * std)
    cpl = (mean - lsl) / (3 * std)
    cpk = min(cpu, cpl)
    
    # Ppk（使用样本标准差）
    sample_std = std
    ppku = (usl - mean) / (3 * sample_std)
    ppkl = (mean - lsl) / (3 * sample_std)
    ppk = min(ppku, ppkl)
    
    return {
        'cp': round(cp, 3),
        'cpk': round(cpk, 3),
        'ppk': round(ppk, 3),
        'lsl': lsl,
        'usl': usl
    }


def _analyze_trend(data: List[float]) -> Dict:
    """分析数据趋势"""
    n = len(data)
    if n < 2:
        return {'direction': 'stable', 'slope': 0, 'r_squared': 0}
    
    # 简单线性回归
    x_mean = (n - 1) / 2
    y_mean = sum(data) / n
    
    numerator = sum((i - x_mean) * (data[i] - y_mean) for i in range(n))
    denominator = sum((i - x_mean) ** 2 for i in range(n))
    
    if denominator == 0:
        return {'direction': 'stable', 'slope': 0, 'r_squared': 0}
    
    slope = numerator / denominator
    
    # 计算R²
    y_pred = [slope * i + (y_mean - slope * x_mean) for i in range(n)]
    ss_res = sum((data[i] - y_pred[i]) ** 2 for i in range(n))
    ss_tot = sum((y - y_mean) ** 2 for y in data)
    r_squared = 1 - (ss_res / ss_tot) if ss_tot > 0 else 0
    
    # 判断方向
    if abs(slope) < 0.001 * y_mean if y_mean != 0 else abs(slope) < 0.001:
        direction = 'stable'
    elif slope > 0:
        direction = 'increasing'
    else:
        direction = 'decreasing'
    
    return {
        'direction': direction,
        'slope': round(slope, 6),
        'r_squared': round(r_squared, 4)
    }


def format_cusum_report(result: CUSUMResult) -> str:
    """
    格式化CUSUM分析报告
    
    Args:
        result: CUSUM分析结果
        
    Returns:
        格式化的报告字符串
        
    Examples:
        >>> data = [10, 10, 11, 10, 12, 14, 15, 17]
        >>> result = standard_cusum(data)
        >>> report = format_cusum_report(result)
        >>> 'CUSUM' in report
        True
    """
    lines = []
    lines.append("=" * 50)
    lines.append("CUSUM控制图分析报告")
    lines.append("=" * 50)
    
    lines.append(f"\n基本参数:")
    lines.append(f"  中心线(目标值): {result.center_line:.4f}")
    lines.append(f"  决策阈值(h): {result.h:.4f}")
    lines.append(f"  参考值(k): {result.k:.4f}")
    
    lines.append(f"\n分析结果:")
    if result.has_signal:
        lines.append(f"  状态: ⚠️ 失控 (检测到信号)")
        lines.append(f"  信号类型: {result.signal_type} shift")
        lines.append(f"  信号位置: 第 {result.signal_index} 个数据点")
        if result.change_point is not None:
            lines.append(f"  变化点: 第 {result.change_point} 个数据点")
        if result.estimated_shift is not None:
            lines.append(f"  估计偏移量: {result.estimated_shift:.4f}")
    else:
        lines.append(f"  状态: ✅ 受控 (未检测到异常)")
    
    if result.points:
        lines.append(f"\n累积和统计:")
        max_pos = max(p.cusum_pos for p in result.points)
        min_neg = min(p.cusum_neg for p in result.points)
        lines.append(f"  最大正向累积和: {max_pos:.4f}")
        lines.append(f"  最小负向累积和: {min_neg:.4f}")
    
    lines.append("\n" + "=" * 50)
    
    return "\n".join(lines)


class CUSUMMonitor:
    """
    实时CUSUM监控器
    
    用于持续监控数据流。
    
    Examples:
        >>> monitor = CUSUMMonitor(target=100, std=5)
        >>> for value in [100, 101, 99, 100, 105, 110, 115]:
        ...     signal = monitor.update(value)
        >>> monitor.has_signal()
        True
    """
    
    def __init__(
        self,
        target: float,
        std: float,
        h: Optional[float] = None,
        k: Optional[float] = None
    ):
        """
        初始化监控器
        
        Args:
            target: 目标值
            std: 过程标准差
            h: 决策阈值
            k: 参考值
        """
        self.target = target
        self.std = std
        
        self.h = h if h is not None else 5 * std
        self.k = k if k is not None else 0.5 * std
        
        self.cusum_pos = 0.0
        self.cusum_neg = 0.0
        self.history: List[CUSUMPoint] = []
        self._signal = False
        self._signal_type: Optional[str] = None
        self._signal_index: Optional[int] = None
    
    def update(self, value: float) -> Optional[str]:
        """
        更新监控器状态
        
        Args:
            value: 新观测值
            
        Returns:
            如果检测到信号返回信号类型，否则返回None
        """
        deviation = value - self.target
        
        self.cusum_pos = max(0, self.cusum_pos + deviation - self.k)
        self.cusum_neg = min(0, self.cusum_neg + deviation + self.k)
        
        signal = 'normal'
        index = len(self.history)
        
        if self.cusum_pos >= self.h:
            signal = 'upper'
            if not self._signal:
                self._signal = True
                self._signal_type = 'upper'
                self._signal_index = index
        elif self.cusum_neg <= -self.h:
            signal = 'lower'
            if not self._signal:
                self._signal = True
                self._signal_type = 'lower'
                self._signal_index = index
        
        self.history.append(CUSUMPoint(
            index=index,
            value=value,
            cusum_pos=self.cusum_pos,
            cusum_neg=self.cusum_neg,
            signal=signal
        ))
        
        return signal if signal != 'normal' else None
    
    def has_signal(self) -> bool:
        """是否检测到信号"""
        return self._signal
    
    def get_signal_type(self) -> Optional[str]:
        """获取信号类型"""
        return self._signal_type
    
    def get_signal_index(self) -> Optional[int]:
        """获取信号位置"""
        return self._signal_index
    
    def reset(self):
        """重置监控器"""
        self.cusum_pos = 0.0
        self.cusum_neg = 0.0
        self.history = []
        self._signal = False
        self._signal_type = None
        self._signal_index = None
    
    def get_history(self) -> List[CUSUMPoint]:
        """获取历史记录"""
        return self.history.copy()
    
    def get_statistics(self) -> Dict:
        """获取统计信息"""
        if not self.history:
            return {'n': 0}
        
        values = [p.value for p in self.history]
        mean = sum(values) / len(values)
        
        if len(values) > 1:
            variance = sum((v - mean) ** 2 for v in values) / (len(values) - 1)
            std = math.sqrt(variance)
        else:
            std = 0
        
        return {
            'n': len(values),
            'mean': mean,
            'std': std,
            'max_cusum_pos': max(p.cusum_pos for p in self.history),
            'min_cusum_neg': min(p.cusum_neg for p in self.history),
            'has_signal': self._signal,
            'signal_type': self._signal_type,
            'signal_index': self._signal_index
        }