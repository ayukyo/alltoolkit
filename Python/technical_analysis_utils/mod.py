"""
技术分析工具模块
提供股票/金融数据技术分析指标计算

功能：
- 移动平均线 (SMA, EMA, WMA)
- 相对强弱指数 (RSI)
- MACD 指标
- 布林带 (Bollinger Bands)
- KDJ 指标
- 随机指标 (Stochastic)
- ATR (平均真实波幅)
- 支撑/阻力位识别
- 趋势线识别

零依赖，纯 Python 实现
"""

from typing import List, Tuple, Optional, Dict, Any
from dataclasses import dataclass
from enum import Enum
import math


class Trend(Enum):
    """趋势方向"""
    UP = "up"
    DOWN = "down"
    SIDEWAYS = "sideways"


@dataclass
class MACDResult:
    """MACD 结果"""
    macd: float
    signal: float
    histogram: float


@dataclass
class BollingerBands:
    """布林带结果"""
    upper: float
    middle: float
    lower: float
    bandwidth: float
    percent_b: float


@dataclass
class StochasticResult:
    """随机指标结果"""
    k: float
    d: float


@dataclass
class SupportResistance:
    """支撑阻力位"""
    support_levels: List[float]
    resistance_levels: List[float]


# ============ 基础计算函数 ============

def validate_data(data: List[float], min_length: int = 1) -> None:
    """验证输入数据"""
    if not data:
        raise ValueError("数据列表不能为空")
    if len(data) < min_length:
        raise ValueError(f"数据长度至少需要 {min_length}，当前 {len(data)}")
    if any(math.isnan(x) or math.isinf(x) for x in data):
        raise ValueError("数据包含无效值 (NaN 或 Inf)")


def sma(data: List[float], period: int) -> List[Optional[float]]:
    """
    简单移动平均线 (Simple Moving Average)
    
    Args:
        data: 价格数据列表
        period: 周期
        
    Returns:
        移动平均线列表，前 period-1 个值为 None
    """
    validate_data(data, period)
    if period < 1:
        raise ValueError("周期必须 >= 1")
    
    result: List[Optional[float]] = [None] * (period - 1)
    
    for i in range(period - 1, len(data)):
        avg = sum(data[i - period + 1:i + 1]) / period
        result.append(round(avg, 6))
    
    return result


def ema(data: List[float], period: int) -> List[Optional[float]]:
    """
    指数移动平均线 (Exponential Moving Average)
    
    Args:
        data: 价格数据列表
        period: 周期
        
    Returns:
        EMA 列表，前 period-1 个值为 None
    """
    validate_data(data, period)
    if period < 1:
        raise ValueError("周期必须 >= 1")
    
    result: List[Optional[float]] = [None] * (period - 1)
    multiplier = 2 / (period + 1)
    
    # 第一个 EMA 值使用 SMA
    first_ema = sum(data[:period]) / period
    result.append(round(first_ema, 6))
    
    # 后续使用 EMA 公式
    prev_ema = first_ema
    for i in range(period, len(data)):
        current_ema = (data[i] - prev_ema) * multiplier + prev_ema
        result.append(round(current_ema, 6))
        prev_ema = current_ema
    
    return result


def wma(data: List[float], period: int) -> List[Optional[float]]:
    """
    加权移动平均线 (Weighted Moving Average)
    
    近期数据权重更大
    
    Args:
        data: 价格数据列表
        period: 周期
        
    Returns:
        WMA 列表，前 period-1 个值为 None
    """
    validate_data(data, period)
    if period < 1:
        raise ValueError("周期必须 >= 1")
    
    result: List[Optional[float]] = [None] * (period - 1)
    weight_sum = period * (period + 1) // 2
    
    for i in range(period - 1, len(data)):
        weighted_sum = sum((j + 1) * data[i - period + 1 + j] for j in range(period))
        result.append(round(weighted_sum / weight_sum, 6))
    
    return result


def rsi(data: List[float], period: int = 14) -> List[Optional[float]]:
    """
    相对强弱指数 (Relative Strength Index)
    
    RSI > 70: 超买区
    RSI < 30: 超卖区
    
    Args:
        data: 价格数据列表
        period: 周期，默认 14
        
    Returns:
        RSI 列表，前 period 个值为 None
    """
    validate_data(data, period + 1)
    if period < 1:
        raise ValueError("周期必须 >= 1")
    
    result: List[Optional[float]] = [None] * period
    
    # 计算价格变化
    changes = [data[i] - data[i - 1] for i in range(1, len(data))]
    
    # 分离涨跌
    gains = [max(0, c) for c in changes]
    losses = [abs(min(0, c)) for c in changes]
    
    # 初始平均涨跌
    avg_gain = sum(gains[:period]) / period
    avg_loss = sum(losses[:period]) / period
    
    # 第一个 RSI
    if avg_loss == 0:
        result.append(100.0)
    else:
        rs = avg_gain / avg_loss
        result.append(round(100 - 100 / (1 + rs), 2))
    
    # 后续使用平滑方法
    for i in range(period, len(changes)):
        avg_gain = (avg_gain * (period - 1) + gains[i]) / period
        avg_loss = (avg_loss * (period - 1) + losses[i]) / period
        
        if avg_loss == 0:
            result.append(100.0)
        else:
            rs = avg_gain / avg_loss
            result.append(round(100 - 100 / (1 + rs), 2))
    
    return result


def macd(data: List[float], fast_period: int = 12, slow_period: int = 26, 
         signal_period: int = 9) -> List[Optional[MACDResult]]:
    """
    MACD 指标 (Moving Average Convergence Divergence)
    
    Args:
        data: 价格数据列表
        fast_period: 快线周期，默认 12
        slow_period: 慢线周期，默认 26
        signal_period: 信号线周期，默认 9
        
    Returns:
        MACDResult 列表，前 slow_period + signal_period - 2 个值为 None
    """
    validate_data(data, slow_period + signal_period)
    
    # 计算快慢 EMA
    fast_ema = ema(data, fast_period)
    slow_ema = ema(data, slow_period)
    
    # 计算 MACD 线 (DIF)
    macd_line: List[Optional[float]] = []
    for i in range(len(data)):
        if fast_ema[i] is None or slow_ema[i] is None:
            macd_line.append(None)
        else:
            macd_line.append(fast_ema[i] - slow_ema[i])
    
    # 过滤 None 值，计算信号线
    valid_macd = [m for m in macd_line if m is not None]
    signal_line = ema(valid_macd, signal_period)
    
    # 构建结果
    result: List[Optional[MACDResult]] = []
    signal_idx = 0
    
    none_count = 0
    for m in macd_line:
        if m is None:
            result.append(None)
            none_count += 1
        else:
            if signal_idx < len(signal_line) and signal_line[signal_idx] is not None:
                sig = signal_line[signal_idx]
                hist = m - sig
                result.append(MACDResult(
                    macd=round(m, 6),
                    signal=round(sig, 6),
                    histogram=round(hist, 6)
                ))
            else:
                result.append(None)
            signal_idx += 1
    
    return result


def bollinger_bands(data: List[float], period: int = 20, 
                    std_dev: float = 2.0) -> List[Optional[BollingerBands]]:
    """
    布林带 (Bollinger Bands)
    
    Args:
        data: 价格数据列表
        period: 周期，默认 20
        std_dev: 标准差倍数，默认 2
        
    Returns:
        BollingerBands 列表
    """
    validate_data(data, period)
    
    result: List[Optional[BollingerBands]] = [None] * (period - 1)
    
    for i in range(period - 1, len(data)):
        window = data[i - period + 1:i + 1]
        middle = sum(window) / period
        
        # 计算标准差
        variance = sum((x - middle) ** 2 for x in window) / period
        std = math.sqrt(variance)
        
        upper = middle + std_dev * std
        lower = middle - std_dev * std
        
        # 带宽和 %B
        bandwidth = (upper - lower) / middle * 100 if middle != 0 else 0
        percent_b = (data[i] - lower) / (upper - lower) if upper != lower else 0.5
        
        result.append(BollingerBands(
            upper=round(upper, 6),
            middle=round(middle, 6),
            lower=round(lower, 6),
            bandwidth=round(bandwidth, 2),
            percent_b=round(percent_b, 4)
        ))
    
    return result


def kdj(high: List[float], low: List[float], close: List[float],
        n: int = 9, m1: int = 3, m2: int = 3) -> List[Optional[Dict[str, float]]]:
    """
    KDJ 指标
    
    Args:
        high: 最高价列表
        low: 最低价列表
        close: 收盘价列表
        n: RSV 周期，默认 9
        m1: K 值平滑周期，默认 3
        m2: D 值平滑周期，默认 3
        
    Returns:
        包含 k, d, j 值的字典列表
    """
    if not (len(high) == len(low) == len(close)):
        raise ValueError("高、低、收盘价列表长度必须相同")
    validate_data(high, n)
    
    result: List[Optional[Dict[str, float]]] = [None] * (n - 1)
    
    # 计算 RSV
    rsv_list: List[float] = []
    for i in range(n - 1, len(close)):
        highest = max(high[i - n + 1:i + 1])
        lowest = min(low[i - n + 1:i + 1])
        
        if highest == lowest:
            rsv = 50.0
        else:
            rsv = (close[i] - lowest) / (highest - lowest) * 100
        rsv_list.append(rsv)
    
    # 计算 K、D、J
    k = 50.0  # 初始 K 值
    d = 50.0  # 初始 D 值
    
    for rsv in rsv_list:
        k = (m1 - 1) / m1 * k + 1 / m1 * rsv
        d = (m2 - 1) / m2 * d + 1 / m2 * k
        j = 3 * k - 2 * d
        
        result.append({
            'k': round(k, 2),
            'd': round(d, 2),
            'j': round(j, 2)
        })
    
    return result


def stochastic(high: List[float], low: List[float], close: List[float],
               k_period: int = 14, d_period: int = 3) -> List[Optional[StochasticResult]]:
    """
    随机指标 (Stochastic Oscillator)
    
    Args:
        high: 最高价列表
        low: 最低价列表
        close: 收盘价列表
        k_period: %K 周期，默认 14
        d_period: %D 周期，默认 3
        
    Returns:
        StochasticResult 列表
    """
    if not (len(high) == len(low) == len(close)):
        raise ValueError("高、低、收盘价列表长度必须相同")
    validate_data(high, k_period)
    
    # 计算 %K
    k_values: List[Optional[float]] = [None] * (k_period - 1)
    
    for i in range(k_period - 1, len(close)):
        highest = max(high[i - k_period + 1:i + 1])
        lowest = min(low[i - k_period + 1:i + 1])
        
        if highest == lowest:
            k_values.append(50.0)
        else:
            k_values.append((close[i] - lowest) / (highest - lowest) * 100)
    
    # 计算 %D (K 的 SMA)
    d_values = sma([k for k in k_values if k is not None], d_period)
    
    # 构建结果
    result: List[Optional[StochasticResult]] = [None] * (k_period - 1)
    d_idx = 0
    
    for i, k in enumerate(k_values):
        if k is None:
            continue
        if d_idx < len(d_values) and d_values[d_idx] is not None:
            result.append(StochasticResult(
                k=round(k, 2),
                d=round(d_values[d_idx], 2)
            ))
        else:
            result.append(None)
        d_idx += 1
    
    return result


def atr(high: List[float], low: List[float], close: List[float],
        period: int = 14) -> List[Optional[float]]:
    """
    平均真实波幅 (Average True Range)
    
    Args:
        high: 最高价列表
        low: 最低价列表
        close: 收盘价列表
        period: 周期，默认 14
        
    Returns:
        ATR 列表
    """
    if not (len(high) == len(low) == len(close)):
        raise ValueError("高、低、收盘价列表长度必须相同")
    validate_data(high, period + 1)
    
    # 计算真实波幅
    tr_list: List[float] = []
    for i in range(len(close)):
        if i == 0:
            tr = high[i] - low[i]
        else:
            tr = max(
                high[i] - low[i],
                abs(high[i] - close[i - 1]),
                abs(low[i] - close[i - 1])
            )
        tr_list.append(tr)
    
    # 计算初始 ATR（从第 period 个位置开始）
    result: List[Optional[float]] = [None] * (period - 1)
    atr_value = sum(tr_list[:period]) / period
    result.append(round(atr_value, 6))
    
    # 平滑 ATR
    for i in range(period, len(tr_list)):
        atr_value = (atr_value * (period - 1) + tr_list[i]) / period
        result.append(round(atr_value, 6))
    
    return result


def obv(close: List[float], volume: List[float]) -> List[float]:
    """
    能量潮指标 (On Balance Volume)
    
    Args:
        close: 收盘价列表
        volume: 成交量列表
        
    Returns:
        OBV 列表
    """
    if len(close) != len(volume):
        raise ValueError("收盘价和成交量列表长度必须相同")
    validate_data(close, 2)
    
    result: List[float] = [0.0]
    
    for i in range(1, len(close)):
        if close[i] > close[i - 1]:
            result.append(result[-1] + volume[i])
        elif close[i] < close[i - 1]:
            result.append(result[-1] - volume[i])
        else:
            result.append(result[-1])
    
    return result


def vwap(high: List[float], low: List[float], close: List[float],
        volume: List[float]) -> List[float]:
    """
    成交量加权平均价 (Volume Weighted Average Price)
    
    Args:
        high: 最高价列表
        low: 最低价列表
        close: 收盘价列表
        volume: 成交量列表
        
    Returns:
        VWAP 列表
    """
    if not (len(high) == len(low) == len(close) == len(volume)):
        raise ValueError("所有价格列表长度必须相同")
    validate_data(high, 1)
    
    result: List[float] = []
    cum_tp_vol = 0.0
    cum_vol = 0.0
    
    for i in range(len(close)):
        typical_price = (high[i] + low[i] + close[i]) / 3
        cum_tp_vol += typical_price * volume[i]
        cum_vol += volume[i]
        
        if cum_vol == 0:
            result.append(typical_price)
        else:
            result.append(round(cum_tp_vol / cum_vol, 6))
    
    return result


def williams_r(high: List[float], low: List[float], close: List[float],
               period: int = 14) -> List[Optional[float]]:
    """
    威廉指标 (Williams %R)
    
    Args:
        high: 最高价列表
        low: 最低价列表
        close: 收盘价列表
        period: 周期，默认 14
        
    Returns:
        Williams %R 列表，范围 -100 到 0
    """
    if not (len(high) == len(low) == len(close)):
        raise ValueError("高、低、收盘价列表长度必须相同")
    validate_data(high, period)
    
    result: List[Optional[float]] = [None] * (period - 1)
    
    for i in range(period - 1, len(close)):
        highest = max(high[i - period + 1:i + 1])
        lowest = min(low[i - period + 1:i + 1])
        
        if highest == lowest:
            result.append(-50.0)
        else:
            wr = (highest - close[i]) / (highest - lowest) * -100
            result.append(round(wr, 2))
    
    return result


def cci(high: List[float], low: List[float], close: List[float],
       period: int = 20) -> List[Optional[float]]:
    """
    顺势指标 (Commodity Channel Index)
    
    Args:
        high: 最高价列表
        low: 最低价列表
        close: 收盘价列表
        period: 周期，默认 20
        
    Returns:
        CCI 列表
    """
    if not (len(high) == len(low) == len(close)):
        raise ValueError("高、低、收盘价列表长度必须相同")
    validate_data(high, period)
    
    result: List[Optional[float]] = [None] * (period - 1)
    
    for i in range(period - 1, len(close)):
        # 典型价格
        tp_list = []
        for j in range(i - period + 1, i + 1):
            tp_list.append((high[j] + low[j] + close[j]) / 3)
        
        sma_tp = sum(tp_list) / period
        
        # 平均绝对偏差
        mad = sum(abs(tp - sma_tp) for tp in tp_list) / period
        
        if mad == 0:
            result.append(0.0)
        else:
            cci_value = (tp_list[-1] - sma_tp) / (0.015 * mad)
            result.append(round(cci_value, 2))
    
    return result


def momentum(data: List[float], period: int = 10) -> List[Optional[float]]:
    """
    动量指标 (Momentum)
    
    Args:
        data: 价格数据列表
        period: 周期，默认 10
        
    Returns:
        动量值列表
    """
    validate_data(data, period + 1)
    
    result: List[Optional[float]] = [None] * period
    
    for i in range(period, len(data)):
        result.append(round(data[i] - data[i - period], 6))
    
    return result


def roc(data: List[float], period: int = 10) -> List[Optional[float]]:
    """
    变动率指标 (Rate of Change)
    
    Args:
        data: 价格数据列表
        period: 周期，默认 10
        
    Returns:
        ROC 列表（百分比）
    """
    validate_data(data, period + 1)
    
    result: List[Optional[float]] = [None] * period
    
    for i in range(period, len(data)):
        if data[i - period] == 0:
            result.append(0.0)
        else:
            result.append(round((data[i] - data[i - period]) / data[i - period] * 100, 2))
    
    return result


def adx(high: List[float], low: List[float], close: List[float],
       period: int = 14) -> List[Optional[Dict[str, float]]]:
    """
    平均趋向指数 (Average Directional Index)
    
    Args:
        high: 最高价列表
        low: 最低价列表
        close: 收盘价列表
        period: 周期，默认 14
        
    Returns:
        包含 adx, plus_di, minus_di 的字典列表
    """
    if not (len(high) == len(low) == len(close)):
        raise ValueError("高、低、收盘价列表长度必须相同")
    validate_data(high, period * 2)
    
    n = len(close)
    
    # 计算 +DM 和 -DM
    plus_dm: List[float] = [0.0]
    minus_dm: List[float] = [0.0]
    
    for i in range(1, n):
        up_move = high[i] - high[i - 1]
        down_move = low[i - 1] - low[i]
        
        if up_move > down_move and up_move > 0:
            plus_dm.append(up_move)
        else:
            plus_dm.append(0.0)
        
        if down_move > up_move and down_move > 0:
            minus_dm.append(down_move)
        else:
            minus_dm.append(0.0)
    
    # 计算 TR
    tr_list: List[float] = [high[0] - low[0]]
    for i in range(1, n):
        tr = max(
            high[i] - low[i],
            abs(high[i] - close[i - 1]),
            abs(low[i] - close[i - 1])
        )
        tr_list.append(tr)
    
    # 平滑
    def smooth(values: List[float], period: int) -> List[float]:
        smoothed: List[float] = [sum(values[:period])]
        for i in range(period, len(values)):
            smoothed.append(smoothed[-1] - smoothed[-1] / period + values[i])
        return smoothed
    
    smooth_tr = smooth(tr_list, period)
    smooth_plus_dm = smooth(plus_dm, period)
    smooth_minus_dm = smooth(minus_dm, period)
    
    # 计算 +DI 和 -DI
    plus_di: List[float] = []
    minus_di: List[float] = []
    
    for i in range(len(smooth_tr)):
        if smooth_tr[i] == 0:
            plus_di.append(0.0)
            minus_di.append(0.0)
        else:
            plus_di.append(smooth_plus_dm[i] / smooth_tr[i] * 100)
            minus_di.append(smooth_minus_dm[i] / smooth_tr[i] * 100)
    
    # 计算 DX
    dx_list: List[float] = []
    for i in range(len(plus_di)):
        di_sum = plus_di[i] + minus_di[i]
        if di_sum == 0:
            dx_list.append(0.0)
        else:
            dx_list.append(abs(plus_di[i] - minus_di[i]) / di_sum * 100)
    
    # 计算 ADX
    result: List[Optional[Dict[str, float]]] = [None] * (period * 2 - 1)
    
    if len(dx_list) >= period:
        adx_value = sum(dx_list[:period]) / period
        result.append({
            'adx': round(adx_value, 2),
            'plus_di': round(plus_di[period - 1], 2),
            'minus_di': round(minus_di[period - 1], 2)
        })
        
        for i in range(period, len(dx_list)):
            adx_value = (adx_value * (period - 1) + dx_list[i]) / period
            idx = i + period
            if idx < len(plus_di):
                result.append({
                    'adx': round(adx_value, 2),
                    'plus_di': round(plus_di[idx], 2),
                    'minus_di': round(minus_di[idx], 2)
                })
    
    return result


# ============ 趋势分析 ============

def detect_trend(data: List[float], period: int = 20) -> Trend:
    """
    检测趋势方向
    
    Args:
        data: 价格数据列表
        period: 分析周期
        
    Returns:
        趋势方向 (UP, DOWN, SIDEWAYS)
    """
    validate_data(data, period)
    
    if len(data) < period:
        period = len(data)
    
    recent = data[-period:]
    ma = sma(recent, period)
    
    if ma[-1] is None:
        return Trend.SIDEWAYS
    
    current_ma = ma[-1]
    
    # 计算斜率
    if period >= 5:
        first_half = sum(recent[:period // 2]) / (period // 2)
        second_half = sum(recent[-(period // 2):]) / (period // 2)
        change_pct = (second_half - first_half) / first_half * 100 if first_half != 0 else 0
        
        if change_pct > 2:
            return Trend.UP
        elif change_pct < -2:
            return Trend.DOWN
    
    return Trend.SIDEWAYS


def find_support_resistance(high: List[float], low: List[float], close: List[float],
                            period: int = 20, tolerance: float = 0.02) -> SupportResistance:
    """
    识别支撑位和阻力位
    
    Args:
        high: 最高价列表
        low: 最低价列表
        close: 收盘价列表
        period: 分析周期
        tolerance: 容差百分比
        
    Returns:
        支撑位和阻力位
    """
    if not (len(high) == len(low) == len(close)):
        raise ValueError("高、低、收盘价列表长度必须相同")
    validate_data(high, period)
    
    supports: List[float] = []
    resistances: List[float] = []
    
    # 寻找局部极值
    for i in range(1, len(low) - 1):
        # 局部低点（支撑）
        if low[i] < low[i - 1] and low[i] < low[i + 1]:
            supports.append(low[i])
        
        # 局部高点（阻力）
        if high[i] > high[i - 1] and high[i] > high[i + 1]:
            resistances.append(high[i])
    
    # 聚合相近的水平
    def cluster_levels(levels: List[float], current_price: float) -> List[float]:
        if not levels:
            return []
        
        sorted_levels = sorted(levels)
        clusters: List[List[float]] = [[sorted_levels[0]]]
        
        for level in sorted_levels[1:]:
            if level - clusters[-1][-1] <= current_price * tolerance:
                clusters[-1].append(level)
            else:
                clusters.append([level])
        
        return [round(sum(c) / len(c), 2) for c in clusters]
    
    current_price = close[-1]
    
    return SupportResistance(
        support_levels=cluster_levels(supports, current_price)[-5:],  # 最近5个支撑
        resistance_levels=cluster_levels(resistances, current_price)[-5:]  # 最近5个阻力
    )


def golden_cross_death_cross(short_ma: List[Optional[float]], 
                               long_ma: List[Optional[float]]) -> List[str]:
    """
    检测金叉和死叉信号
    
    Args:
        short_ma: 短期移动平均线
        long_ma: 长期移动平均线
        
    Returns:
        信号列表 ('golden', 'death', 或 '')
    """
    if len(short_ma) != len(long_ma):
        raise ValueError("移动平均线列表长度必须相同")
    
    result: List[str] = []
    
    for i in range(len(short_ma)):
        if short_ma[i] is None or long_ma[i] is None:
            result.append('')
        elif i > 0 and short_ma[i - 1] is not None and long_ma[i - 1] is not None:
            # 金叉：短期上穿长期
            if short_ma[i - 1] <= long_ma[i - 1] and short_ma[i] > long_ma[i]:
                result.append('golden')
            # 死叉：短期下穿长期
            elif short_ma[i - 1] >= long_ma[i - 1] and short_ma[i] < long_ma[i]:
                result.append('death')
            else:
                result.append('')
        else:
            result.append('')
    
    return result


# ============ 综合分析 ============

def analyze(data: List[float], high: Optional[List[float]] = None,
            low: Optional[List[float]] = None,
            volume: Optional[List[float]] = None) -> Dict[str, Any]:
    """
    综合技术分析
    
    Args:
        data: 收盘价列表
        high: 最高价列表（可选）
        low: 最低价列表（可选）
        volume: 成交量列表（可选）
        
    Returns:
        综合分析结果字典
    """
    validate_data(data, 50)
    
    result: Dict[str, Any] = {
        'current_price': data[-1],
        'trend': detect_trend(data).value,
        'sma': {
            'sma_5': sma(data, 5)[-1],
            'sma_10': sma(data, 10)[-1],
            'sma_20': sma(data, 20)[-1],
        },
        'ema': {
            'ema_12': ema(data, 12)[-1],
            'ema_26': ema(data, 26)[-1],
        },
        'rsi_14': rsi(data, 14)[-1],
        'macd': None,
        'bollinger': None,
    }
    
    # MACD
    macd_result = macd(data)
    if macd_result[-1] is not None:
        result['macd'] = {
            'macd': macd_result[-1].macd,
            'signal': macd_result[-1].signal,
            'histogram': macd_result[-1].histogram,
        }
    
    # 布林带
    bb_result = bollinger_bands(data)
    if bb_result[-1] is not None:
        result['bollinger'] = {
            'upper': bb_result[-1].upper,
            'middle': bb_result[-1].middle,
            'lower': bb_result[-1].lower,
            'bandwidth': bb_result[-1].bandwidth,
            'percent_b': bb_result[-1].percent_b,
        }
    
    # 动量
    result['momentum'] = momentum(data)[-1]
    result['roc'] = roc(data)[-1]
    
    # 如果有高低价
    if high and low and len(high) == len(low) == len(data):
        result['kdj'] = kdj(high, low, data)[-1]
        result['williams_r'] = williams_r(high, low, data)[-1]
        result['cci'] = cci(high, low, data)[-1]
        
        # 支撑阻力
        sr = find_support_resistance(high, low, data)
        result['support_resistance'] = {
            'supports': sr.support_levels,
            'resistances': sr.resistance_levels,
        }
    
    # 如果有成交量
    if volume and len(volume) == len(data):
        result['obv'] = obv(data, volume)[-1]
    
    return result


# ============ 工具函数 ============

def is_oversold(rsi_value: float, threshold: float = 30) -> bool:
    """判断是否超卖"""
    return rsi_value < threshold


def is_overbought(rsi_value: float, threshold: float = 70) -> bool:
    """判断是否超买"""
    return rsi_value > threshold


def calculate_returns(data: List[float]) -> List[float]:
    """计算收益率序列"""
    validate_data(data, 2)
    
    returns: List[float] = [0.0]
    for i in range(1, len(data)):
        if data[i - 1] == 0:
            returns.append(0.0)
        else:
            returns.append((data[i] - data[i - 1]) / data[i - 1])
    
    return returns


def calculate_volatility(data: List[float], period: int = 20) -> Optional[float]:
    """计算波动率（标准差年化）"""
    validate_data(data, period)
    
    returns = calculate_returns(data[-period:])
    mean_return = sum(returns) / len(returns)
    variance = sum((r - mean_return) ** 2 for r in returns) / len(returns)
    
    # 年化（假设 252 个交易日）
    return round(math.sqrt(variance * 252) * 100, 2)


def max_drawdown(data: List[float]) -> float:
    """计算最大回撤"""
    validate_data(data, 2)
    
    peak = data[0]
    max_dd = 0.0
    
    for price in data:
        if price > peak:
            peak = price
        dd = (peak - price) / peak
        if dd > max_dd:
            max_dd = dd
    
    return round(max_dd * 100, 2)


def sharpe_ratio(data: List[float], risk_free_rate: float = 0.02) -> Optional[float]:
    """计算夏普比率"""
    validate_data(data, 20)
    
    returns = calculate_returns(data)
    mean_return = sum(returns[1:]) / len(returns[1:])
    
    variance = sum((r - mean_return) ** 2 for r in returns[1:]) / len(returns[1:])
    std = math.sqrt(variance)
    
    if std == 0:
        return None
    
    # 年化
    annual_return = mean_return * 252
    annual_std = std * math.sqrt(252)
    
    return round((annual_return - risk_free_rate) / annual_std, 2)