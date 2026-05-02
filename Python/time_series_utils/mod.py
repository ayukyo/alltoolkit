"""
时间序列分析工具模块
Time Series Analysis Utilities

提供常用的时间序列分析功能，包括：
- 滚动统计（移动平均、标准差、最大最小值）
- 指数平滑（单次、二次、三次）
- 趋势检测
- 季节性检测
- 异常检测
- 时间序列分解

零外部依赖，仅使用 Python 标准库
"""

import math
from typing import List, Tuple, Optional, Dict, Any, Callable
from collections import deque
from dataclasses import dataclass
from enum import Enum


class TrendDirection(Enum):
    """趋势方向枚举"""
    UP = "up"
    DOWN = "down"
    FLAT = "flat"


@dataclass
class RollingStats:
    """滚动统计数据结构"""
    mean: float
    std: float
    min: float
    max: float
    count: int
    sum: float


@dataclass
class DecompositionResult:
    """时间序列分解结果"""
    trend: List[float]
    seasonal: List[float]
    residual: List[float]


@dataclass
class AnomalyResult:
    """异常检测结果"""
    index: int
    value: float
    score: float
    is_anomaly: bool


# ============================================================================
# 滚动窗口统计
# ============================================================================

class RollingWindow:
    """
    滚动窗口统计计算器
    
    高效计算滚动窗口内的统计量，支持增量更新
    使用带索引的单调队列正确处理滑动窗口的最值问题
    """
    
    def __init__(self, window_size: int):
        """
        初始化滚动窗口
        
        Args:
            window_size: 窗口大小
        """
        if window_size < 1:
            raise ValueError("窗口大小必须至少为 1")
        self.window_size = window_size
        self._window: deque = deque(maxlen=window_size)
        self._sum = 0.0
        self._sum_sq = 0.0
        self._index = 0  # 全局索引
        # 最小值单调队列：存储 (index, value)
        self._min_deque: deque = deque()
        # 最大值单调队列：存储 (index, value)
        self._max_deque: deque = deque()
    
    def add(self, value: float) -> RollingStats:
        """
        添加新值并返回当前窗口统计
        
        Args:
            value: 新数据点
            
        Returns:
            当前窗口的统计信息
        """
        # 如果窗口满了，移除最旧的值（计算统计）
        if len(self._window) == self.window_size:
            old_value = self._window[0]
            self._sum -= old_value
            self._sum_sq -= old_value * old_value
        
        # 添加新值
        self._window.append(value)
        self._sum += value
        self._sum_sq += value * value
        
        # 计算当前窗口的起始索引
        start_idx = self._index - self.window_size + 1 if self._index >= self.window_size - 1 else 0
        
        # 更新最小值单调队列
        while self._min_deque and self._min_deque[-1][1] > value:
            self._min_deque.pop()
        self._min_deque.append((self._index, value))
        # 移除窗口外的元素
        while self._min_deque and self._min_deque[0][0] < start_idx:
            self._min_deque.popleft()
        
        # 更新最大值单调队列
        while self._max_deque and self._max_deque[-1][1] < value:
            self._max_deque.pop()
        self._max_deque.append((self._index, value))
        # 移除窗口外的元素
        while self._max_deque and self._max_deque[0][0] < start_idx:
            self._max_deque.popleft()
        
        self._index += 1
        
        return self.get_stats()
    
    def get_stats(self) -> RollingStats:
        """
        获取当前窗口统计信息
        
        Returns:
            当前窗口的统计信息
        """
        n = len(self._window)
        if n == 0:
            return RollingStats(0.0, 0.0, 0.0, 0.0, 0, 0.0)
        
        mean = self._sum / n
        variance = (self._sum_sq / n) - (mean * mean)
        std = math.sqrt(max(0, variance))
        
        # 从单调队列获取当前窗口的最值
        min_val = self._min_deque[0][1] if self._min_deque else float('inf')
        max_val = self._max_deque[0][1] if self._max_deque else float('-inf')
        
        return RollingStats(
            mean=mean,
            std=std,
            min=min_val,
            max=max_val,
            count=n,
            sum=self._sum
        )
    
    def clear(self) -> None:
        """清空窗口"""
        self._window.clear()
        self._min_deque.clear()
        self._max_deque.clear()
        self._sum = 0.0
        self._sum_sq = 0.0
        self._index = 0


def rolling_mean(data: List[float], window_size: int) -> List[float]:
    """
    计算滚动平均值
    
    Args:
        data: 输入数据序列
        window_size: 窗口大小
        
    Returns:
        滚动平均值列表
    """
    if not data or window_size < 1:
        return []
    
    result = []
    roller = RollingWindow(window_size)
    
    for value in data:
        roller.add(value)
        result.append(roller.get_stats().mean)
    
    return result


def rolling_std(data: List[float], window_size: int) -> List[float]:
    """
    计算滚动标准差
    
    Args:
        data: 输入数据序列
        window_size: 窗口大小
        
    Returns:
        滚动标准差列表
    """
    if not data or window_size < 1:
        return []
    
    result = []
    roller = RollingWindow(window_size)
    
    for value in data:
        roller.add(value)
        result.append(roller.get_stats().std)
    
    return result


def rolling_min(data: List[float], window_size: int) -> List[float]:
    """
    计算滚动最小值
    
    Args:
        data: 输入数据序列
        window_size: 窗口大小
        
    Returns:
        滚动最小值列表
    """
    if not data or window_size < 1:
        return []
    
    result = []
    roller = RollingWindow(window_size)
    
    for value in data:
        roller.add(value)
        result.append(roller.get_stats().min)
    
    return result


def rolling_max(data: List[float], window_size: int) -> List[float]:
    """
    计算滚动最大值
    
    Args:
        data: 输入数据序列
        window_size: 窗口大小
        
    Returns:
        滚动最大值列表
    """
    if not data or window_size < 1:
        return []
    
    result = []
    roller = RollingWindow(window_size)
    
    for value in data:
        roller.add(value)
        result.append(roller.get_stats().max)
    
    return result


# ============================================================================
# 移动平均
# ============================================================================

def simple_moving_average(data: List[float], window_size: int) -> List[float]:
    """
    简单移动平均 (SMA)
    
    Args:
        data: 输入数据序列
        window_size: 窗口大小
        
    Returns:
        SMA 值列表
    """
    return rolling_mean(data, window_size)


def weighted_moving_average(data: List[float], window_size: int, 
                           weights: Optional[List[float]] = None) -> List[float]:
    """
    加权移动平均 (WMA)
    
    Args:
        data: 输入数据序列
        window_size: 窗口大小
        weights: 权重列表，默认为线性递增权重 [1, 2, ..., n]
        
    Returns:
        WMA 值列表
    """
    if not data or window_size < 1:
        return []
    
    if weights is None:
        weights = list(range(1, window_size + 1))
    
    if len(weights) != window_size:
        raise ValueError("权重列表长度必须等于窗口大小")
    
    weight_sum = sum(weights)
    result = []
    
    for i in range(len(data)):
        if i < window_size - 1:
            # 窗口未满时，使用部分数据和对应权重
            partial_weights = weights[:i+1]
            partial_data = data[:i+1]
            wma = sum(d * w for d, w in zip(partial_data, partial_weights)) / sum(partial_weights)
        else:
            window_data = data[i - window_size + 1:i + 1]
            wma = sum(d * w for d, w in zip(window_data, weights)) / weight_sum
        result.append(wma)
    
    return result


def exponential_moving_average(data: List[float], alpha: float = 0.1) -> List[float]:
    """
    指数移动平均 (EMA)
    
    EMA(t) = alpha * data(t) + (1 - alpha) * EMA(t-1)
    
    Args:
        data: 输入数据序列
        alpha: 平滑因子 (0 < alpha < 1)，值越大越重视近期数据
        
    Returns:
        EMA 值列表
    """
    if not data:
        return []
    
    if not 0 < alpha < 1:
        raise ValueError("alpha 必须在 (0, 1) 范围内")
    
    result = [data[0]]  # 第一个值作为初始 EMA
    
    for i in range(1, len(data)):
        ema = alpha * data[i] + (1 - alpha) * result[-1]
        result.append(ema)
    
    return result


def ema_from_period(data: List[float], period: int) -> List[float]:
    """
    从周期计算 EMA
    
    alpha = 2 / (period + 1)
    
    Args:
        data: 输入数据序列
        period: 周期长度
        
    Returns:
        EMA 值列表
    """
    alpha = 2 / (period + 1)
    return exponential_moving_average(data, alpha)


# ============================================================================
# 指数平滑
# ============================================================================

def single_exponential_smoothing(data: List[float], alpha: float = 0.3) -> List[float]:
    """
    单次指数平滑 (SES) - 适用于无趋势、无季节性的数据
    
    F(t+1) = alpha * Y(t) + (1 - alpha) * F(t)
    
    Args:
        data: 输入数据序列
        alpha: 平滑因子 (0 < alpha < 1)
        
    Returns:
        平滑后的值列表
    """
    return exponential_moving_average(data, alpha)


def double_exponential_smoothing(data: List[float], alpha: float = 0.3, 
                                  beta: float = 0.1) -> List[float]:
    """
    双重指数平滑 (Holt 方法) - 适用于有趋势、无季节性的数据
    
    Level(t) = alpha * Y(t) + (1 - alpha) * (Level(t-1) + Trend(t-1))
    Trend(t) = beta * (Level(t) - Level(t-1)) + (1 - beta) * Trend(t-1)
    Forecast(t+1) = Level(t) + Trend(t)
    
    Args:
        data: 输入数据序列
        alpha: 水平平滑因子
        beta: 趋势平滑因子
        
    Returns:
        平滑后的值列表
    """
    if len(data) < 2:
        return data.copy()
    
    level = [data[0]]
    trend = [data[1] - data[0]]
    result = [data[0]]
    
    for i in range(1, len(data)):
        new_level = alpha * data[i] + (1 - alpha) * (level[-1] + trend[-1])
        new_trend = beta * (new_level - level[-1]) + (1 - beta) * trend[-1]
        
        level.append(new_level)
        trend.append(new_trend)
        result.append(new_level)
    
    return result


def triple_exponential_smoothing(data: List[float], period: int, 
                                 alpha: float = 0.3, beta: float = 0.1, 
                                 gamma: float = 0.1) -> List[float]:
    """
    三次指数平滑 (Holt-Winters 方法) - 适用于有趋势和季节性的数据
    
    Args:
        data: 输入数据序列
        period: 季节周期长度
        alpha: 水平平滑因子
        beta: 趋势平滑因子
        gamma: 季节平滑因子
        
    Returns:
        平滑后的值列表
    """
    if len(data) < 2 * period:
        return data.copy()
    
    # 初始化
    level = [sum(data[:period]) / period]
    trend = [(sum(data[period:2*period]) - sum(data[:period])) / period / period]
    seasonal = []
    
    # 计算初始季节因子
    for i in range(period):
        seasonal.append(data[i] - level[0])
    
    result = [data[0]]
    
    for i in range(1, len(data)):
        # 更新水平
        if i >= period:
            new_level = alpha * (data[i] - seasonal[i - period]) + \
                        (1 - alpha) * (level[-1] + trend[-1])
        else:
            new_level = alpha * data[i] + (1 - alpha) * (level[-1] + trend[-1])
        
        # 更新趋势
        new_trend = beta * (new_level - level[-1]) + (1 - beta) * trend[-1]
        
        # 更新季节因子
        if i >= period:
            new_seasonal = gamma * (data[i] - new_level) + \
                          (1 - gamma) * seasonal[i - period]
            seasonal.append(new_seasonal)
        
        level.append(new_level)
        trend.append(new_trend)
        result.append(new_level)
    
    return result


# ============================================================================
# 趋势检测
# ============================================================================

def detect_trend(data: List[float], window_size: Optional[int] = None) -> TrendDirection:
    """
    检测数据趋势方向
    
    使用 Mann-Kendall 趋势检验的简化版本
    
    Args:
        data: 输入数据序列
        window_size: 用于检测的窗口大小，默认为全部数据
        
    Returns:
        趋势方向
    """
    if len(data) < 2:
        return TrendDirection.FLAT
    
    if window_size:
        data = data[-window_size:]
    
    # 计算趋势：比较所有点对
    n = len(data)
    increasing = 0
    decreasing = 0
    
    for i in range(n - 1):
        for j in range(i + 1, n):
            if data[j] > data[i]:
                increasing += 1
            elif data[j] < data[i]:
                decreasing += 1
    
    # 标准化统计量
    total = increasing + decreasing
    if total == 0:
        return TrendDirection.FLAT
    
    s = increasing - decreasing
    # 简化的显著性检验
    threshold = n * (n - 1) / 4 * 0.3  # 约等于 0.5 * sqrt(var)
    
    if s > threshold:
        return TrendDirection.UP
    elif s < -threshold:
        return TrendDirection.DOWN
    else:
        return TrendDirection.FLAT


def calculate_trend_slope(data: List[float]) -> float:
    """
    计算线性趋势斜率（使用最小二乘法）
    
    Args:
        data: 输入数据序列
        
    Returns:
        趋势斜率
    """
    if len(data) < 2:
        return 0.0
    
    n = len(data)
    x_mean = (n - 1) / 2
    y_mean = sum(data) / n
    
    numerator = sum((i - x_mean) * (data[i] - y_mean) for i in range(n))
    denominator = sum((i - x_mean) ** 2 for i in range(n))
    
    if denominator == 0:
        return 0.0
    
    return numerator / denominator


def linear_regression(data: List[float]) -> Tuple[float, float, float]:
    """
    线性回归
    
    Args:
        data: 输入数据序列
        
    Returns:
        (斜率, 截距, R²) 元组
    """
    if len(data) < 2:
        return 0.0, data[0] if data else 0.0, 0.0
    
    n = len(data)
    x = list(range(n))
    
    x_mean = sum(x) / n
    y_mean = sum(data) / n
    
    # 计算斜率和截距
    ss_xy = sum((x[i] - x_mean) * (data[i] - y_mean) for i in range(n))
    ss_xx = sum((xi - x_mean) ** 2 for xi in x)
    
    if ss_xx == 0:
        return 0.0, y_mean, 0.0
    
    slope = ss_xy / ss_xx
    intercept = y_mean - slope * x_mean
    
    # 计算 R²
    y_pred = [slope * xi + intercept for xi in x]
    ss_tot = sum((y - y_mean) ** 2 for y in data)
    ss_res = sum((data[i] - y_pred[i]) ** 2 for i in range(n))
    
    r_squared = 1 - (ss_res / ss_tot) if ss_tot != 0 else 0.0
    
    return slope, intercept, r_squared


# ============================================================================
# 季节性检测
# ============================================================================

def detect_seasonality(data: List[float], max_period: int = 12) -> Optional[int]:
    """
    检测季节性周期
    
    使用自相关方法检测最佳周期
    
    Args:
        data: 输入数据序列
        max_period: 最大检测周期
        
    Returns:
        检测到的周期长度，如果没有则返回 None
    """
    if len(data) < max_period * 2:
        max_period = len(data) // 2
    
    if max_period < 2:
        return None
    
    best_period = None
    best_correlation = 0.0
    
    mean = sum(data) / len(data)
    variance = sum((x - mean) ** 2 for x in data) / len(data)
    
    if variance == 0:
        return None
    
    for period in range(2, max_period + 1):
        if len(data) <= period:
            break
        
        # 计算自相关
        n = len(data) - period
        if n <= 0:
            continue
        
        autocorr = sum((data[i] - mean) * (data[i + period] - mean) 
                       for i in range(n)) / (n * variance)
        
        if autocorr > best_correlation:
            best_correlation = autocorr
            best_period = period
    
    # 如果相关性足够高，返回周期
    if best_correlation > 0.3:
        return best_period
    
    return None


def autocorrelation(data: List[float], lag: int) -> float:
    """
    计算自相关系数
    
    Args:
        data: 输入数据序列
        lag: 滞后阶数
        
    Returns:
        自相关系数
    """
    n = len(data)
    if n <= lag or lag < 0:
        return 0.0
    
    mean = sum(data) / n
    variance = sum((x - mean) ** 2 for x in data) / n
    
    if variance == 0:
        return 0.0
    
    autocorr = sum((data[i] - mean) * (data[i + lag] - mean) 
                   for i in range(n - lag)) / (n * variance)
    
    return autocorr


# ============================================================================
# 异常检测
# ============================================================================

def zscore_anomaly_detection(data: List[float], threshold: float = 3.0) -> List[AnomalyResult]:
    """
    Z-Score 异常检测
    
    Args:
        data: 输入数据序列
        threshold: Z-Score 阈值
        
    Returns:
        异常检测结果列表
    """
    if len(data) < 2:
        return []
    
    mean = sum(data) / len(data)
    variance = sum((x - mean) ** 2 for x in data) / len(data)
    std = math.sqrt(variance) if variance > 0 else 1.0
    
    results = []
    for i, value in enumerate(data):
        zscore = abs(value - mean) / std
        results.append(AnomalyResult(
            index=i,
            value=value,
            score=zscore,
            is_anomaly=zscore > threshold
        ))
    
    return results


def iqr_anomaly_detection(data: List[float], k: float = 1.5) -> List[AnomalyResult]:
    """
    IQR (四分位距) 异常检测
    
    Args:
        data: 输入数据序列
        k: IQR 系数，默认 1.5
        
    Returns:
        异常检测结果列表
    """
    if len(data) < 4:
        return []
    
    sorted_data = sorted(data)
    n = len(sorted_data)
    
    # 计算四分位数
    q1_idx = n // 4
    q3_idx = 3 * n // 4
    
    q1 = sorted_data[q1_idx]
    q3 = sorted_data[q3_idx]
    iqr = q3 - q1
    
    lower_bound = q1 - k * iqr
    upper_bound = q3 + k * iqr
    
    results = []
    for i, value in enumerate(data):
        is_anomaly = value < lower_bound or value > upper_bound
        score = max(abs(value - lower_bound), abs(value - upper_bound)) if is_anomaly else 0.0
        results.append(AnomalyResult(
            index=i,
            value=value,
            score=score,
            is_anomaly=is_anomaly
        ))
    
    return results


def moving_average_anomaly_detection(data: List[float], window_size: int, 
                                      threshold: float = 2.0) -> List[AnomalyResult]:
    """
    移动平均异常检测
    
    基于偏离移动平均的程度检测异常
    
    Args:
        data: 输入数据序列
        window_size: 移动平均窗口大小
        threshold: 标准差阈值
        
    Returns:
        异常检测结果列表
    """
    if len(data) < window_size:
        return []
    
    ma = simple_moving_average(data, window_size)
    std = rolling_std(data, window_size)
    
    results = []
    for i, value in enumerate(data):
        if std[i] == 0:
            score = 0.0
            is_anomaly = False
        else:
            score = abs(value - ma[i]) / std[i]
            is_anomaly = score > threshold
        
        results.append(AnomalyResult(
            index=i,
            value=value,
            score=score,
            is_anomaly=is_anomaly
        ))
    
    return results


# ============================================================================
# 时间序列分解
# ============================================================================

def decompose_time_series(data: List[float], period: int) -> DecompositionResult:
    """
    时间序列分解（加法模型）
    
    将时间序列分解为趋势、季节性和残差成分
    
    Args:
        data: 输入数据序列
        period: 季节周期长度
        
    Returns:
        分解结果
    """
    if len(data) < period * 2:
        # 数据不足，返回简单分解
        trend = simple_moving_average(data, min(len(data), 3))
        seasonal = [0.0] * len(data)
        residual = [data[i] - trend[i] if i < len(trend) else 0.0 
                    for i in range(len(data))]
        return DecompositionResult(trend=trend, seasonal=seasonal, residual=residual)
    
    n = len(data)
    
    # 1. 提取趋势（使用周期长度的移动平均）
    trend = []
    half_period = period // 2
    
    for i in range(n):
        start = max(0, i - half_period)
        end = min(n, i + half_period + 1)
        trend.append(sum(data[start:end]) / (end - start))
    
    # 2. 计算去趋势数据
    detrended = [data[i] - trend[i] for i in range(n)]
    
    # 3. 计算季节性成分
    seasonal = []
    for i in range(n):
        # 收集同一季节位置的所有值
        season_idx = i % period
        season_values = [detrended[j] for j in range(season_idx, n, period)]
        seasonal.append(sum(season_values) / len(season_values) if season_values else 0.0)
    
    # 4. 计算残差
    residual = [data[i] - trend[i] - seasonal[i] for i in range(n)]
    
    return DecompositionResult(trend=trend, seasonal=seasonal, residual=residual)


# ============================================================================
# 预测
# ============================================================================

def forecast_ses(data: List[float], alpha: float, horizon: int) -> List[float]:
    """
    使用单次指数平滑进行预测
    
    Args:
        data: 历史数据
        alpha: 平滑因子
        horizon: 预测期数
        
    Returns:
        预测值列表
    """
    if not data:
        return []
    
    # SES 预测是常数（最后一个平滑值）
    smoothed = single_exponential_smoothing(data, alpha)
    last_value = smoothed[-1]
    
    return [last_value] * horizon


def forecast_holt(data: List[float], alpha: float, beta: float, 
                  horizon: int) -> List[float]:
    """
    使用 Holt 方法进行预测
    
    Args:
        data: 历史数据
        alpha: 水平平滑因子
        beta: 趋势平滑因子
        horizon: 预测期数
        
    Returns:
        预测值列表
    """
    if len(data) < 2:
        return []
    
    # 获取最后的水平和趋势
    smoothed = double_exponential_smoothing(data, alpha, beta)
    
    # 重新计算最后的水平和趋势
    level = smoothed[-1]
    
    # 估算趋势
    if len(smoothed) >= 2:
        trend = smoothed[-1] - smoothed[-2]
    else:
        trend = 0.0
    
    # 预测
    forecasts = []
    for h in range(1, horizon + 1):
        forecasts.append(level + h * trend)
    
    return forecasts


def forecast_holt_winters(data: List[float], period: int, alpha: float, 
                          beta: float, gamma: float, horizon: int) -> List[float]:
    """
    使用 Holt-Winters 方法进行预测
    
    Args:
        data: 历史数据
        period: 季节周期
        alpha: 水平平滑因子
        beta: 趋势平滑因子
        gamma: 季节平滑因子
        horizon: 预测期数
        
    Returns:
        预测值列表
    """
    if len(data) < period * 2:
        return forecast_holt(data, alpha, beta, horizon)
    
    # 分解获取成分
    result = decompose_time_series(data, period)
    
    # 获取最后的趋势和季节性
    last_level = result.trend[-1]
    
    if len(result.trend) >= 2:
        last_trend = result.trend[-1] - result.trend[-2]
    else:
        last_trend = 0.0
    
    # 预测
    forecasts = []
    for h in range(1, horizon + 1):
        seasonal_idx = (len(data) + h - 1) % period
        seasonal = result.seasonal[seasonal_idx] if seasonal_idx < len(result.seasonal) else 0.0
        forecasts.append(last_level + h * last_trend + seasonal)
    
    return forecasts


# ============================================================================
# 差分与平稳性
# ============================================================================

def difference(data: List[float], order: int = 1) -> List[float]:
    """
    差分运算
    
    Args:
        data: 输入数据序列
        order: 差分阶数
        
    Returns:
        差分后的序列
    """
    if order < 1:
        return data.copy()
    
    result = data.copy()
    for _ in range(order):
        result = [result[i] - result[i-1] for i in range(1, len(result))]
    
    return result


def is_stationary(data: List[float], window_size: Optional[int] = None) -> bool:
    """
    简单的平稳性检验（基于滚动统计）
    
    Args:
        data: 输入数据序列
        window_size: 窗口大小
        
    Returns:
        是否平稳
    """
    if len(data) < 10:
        return True
    
    if window_size is None:
        window_size = max(5, len(data) // 4)
    
    # 计算前半部分和后半部分的统计量
    mid = len(data) // 2
    
    mean1 = sum(data[:mid]) / mid
    mean2 = sum(data[mid:]) / (len(data) - mid)
    
    var1 = sum((x - mean1) ** 2 for x in data[:mid]) / mid
    var2 = sum((x - mean2) ** 2 for x in data[mid:]) / (len(data) - mid)
    
    # 检验均值和方差是否相似
    mean_diff = abs(mean1 - mean2)
    var_avg = (var1 + var2) / 2
    
    if var_avg == 0:
        return True
    
    # 宽松的标准差比较
    std_threshold = math.sqrt(var_avg) * 2
    
    return mean_diff < std_threshold


# ============================================================================
# 其他实用函数
# ============================================================================

def find_peaks(data: List[float], min_height: Optional[float] = None,
               min_distance: int = 1) -> List[int]:
    """
    寻找峰值点
    
    Args:
        data: 输入数据序列
        min_height: 最小高度阈值
        min_distance: 峰值之间的最小距离
        
    Returns:
        峰值点的索引列表
    """
    if len(data) < 3:
        return []
    
    # 找到所有局部最大值
    peaks = []
    for i in range(1, len(data) - 1):
        if data[i] > data[i-1] and data[i] > data[i+1]:
            if min_height is None or data[i] >= min_height:
                peaks.append(i)
    
    # 应用最小距离约束
    if min_distance <= 1:
        return peaks
    
    filtered_peaks = []
    last_peak = -min_distance - 1
    
    for peak in peaks:
        if peak - last_peak >= min_distance:
            filtered_peaks.append(peak)
            last_peak = peak
    
    return filtered_peaks


def find_valleys(data: List[float], min_depth: Optional[float] = None,
                 min_distance: int = 1) -> List[int]:
    """
    寻找谷值点
    
    Args:
        data: 输入数据序列
        min_depth: 最小深度阈值
        min_distance: 谷值之间的最小距离
        
    Returns:
        谷值点的索引列表
    """
    # 谷值是负数据的峰值
    negated = [-x for x in data]
    min_height = -min_depth if min_depth is not None else None
    return find_peaks(negated, min_height, min_distance)


def calculate_volatility(data: List[float], window_size: int = 20) -> List[float]:
    """
    计算波动率（滚动标准差）
    
    Args:
        data: 输入数据序列
        window_size: 窗口大小
        
    Returns:
        波动率列表
    """
    return rolling_std(data, window_size)


def percentage_change(data: List[float]) -> List[float]:
    """
    计算百分比变化
    
    Args:
        data: 输入数据序列
        
    Returns:
        百分比变化列表（第一个值为 0）
    """
    if len(data) < 2:
        return [0.0] * len(data)
    
    result = [0.0]
    for i in range(1, len(data)):
        if data[i-1] != 0:
            change = (data[i] - data[i-1]) / data[i-1] * 100
        else:
            change = 0.0
        result.append(change)
    
    return result


def cumulative_return(data: List[float]) -> float:
    """
    计算累计收益率
    
    Args:
        data: 输入数据序列（价格或指数）
        
    Returns:
        累计收益率
    """
    if len(data) < 2 or data[0] == 0:
        return 0.0
    
    return (data[-1] - data[0]) / data[0] * 100


def resample(data: List[float], factor: int, method: str = 'mean') -> List[float]:
    """
    重采样时间序列
    
    Args:
        data: 输入数据序列
        factor: 重采样因子（如 2 表示每 2 个点合并为 1 个）
        method: 聚合方法 ('mean', 'sum', 'min', 'max', 'first', 'last')
        
    Returns:
        重采样后的序列
    """
    if factor < 1:
        raise ValueError("重采样因子必须 >= 1")
    
    if factor == 1:
        return data.copy()
    
    methods = {
        'mean': lambda x: sum(x) / len(x),
        'sum': sum,
        'min': min,
        'max': max,
        'first': lambda x: x[0],
        'last': lambda x: x[-1]
    }
    
    if method not in methods:
        raise ValueError(f"未知方法: {method}")
    
    agg_func = methods[method]
    result = []
    
    for i in range(0, len(data), factor):
        chunk = data[i:i+factor]
        result.append(agg_func(chunk))
    
    return result


def fill_missing(data: List[Optional[float]], method: str = 'linear') -> List[float]:
    """
    填充缺失值
    
    Args:
        data: 输入数据序列（可能包含 None）
        method: 填充方法 ('linear', 'forward', 'backward', 'mean')
        
    Returns:
        填充后的序列
    """
    if not data:
        return []
    
    result = []
    last_valid = None
    last_valid_idx = None
    valid_values = [x for x in data if x is not None]
    mean_value = sum(valid_values) / len(valid_values) if valid_values else 0.0
    
    for i, value in enumerate(data):
        if value is not None:
            result.append(value)
            last_valid = value
            last_valid_idx = i
        else:
            if method == 'forward':
                filled = last_valid if last_valid is not None else mean_value
            elif method == 'backward':
                # 找下一个有效值
                next_valid = None
                for j in range(i + 1, len(data)):
                    if data[j] is not None:
                        next_valid = data[j]
                        break
                filled = next_valid if next_valid is not None else last_valid if last_valid is not None else mean_value
            elif method == 'linear':
                # 线性插值
                next_valid = None
                next_idx = None
                for j in range(i + 1, len(data)):
                    if data[j] is not None:
                        next_valid = data[j]
                        next_idx = j
                        break
                
                if last_valid is not None and next_valid is not None and next_idx is not None and last_valid_idx is not None:
                    # 线性插值: 在 last_valid_idx 和 next_idx 之间插值
                    total_gap = next_idx - last_valid_idx
                    position_in_gap = i - last_valid_idx
                    filled = last_valid + (next_valid - last_valid) * position_in_gap / total_gap
                elif last_valid is not None:
                    filled = last_valid
                elif next_valid is not None:
                    filled = next_valid
                else:
                    filled = mean_value
            else:  # mean
                filled = mean_value
            
            result.append(filled)
    
    return result