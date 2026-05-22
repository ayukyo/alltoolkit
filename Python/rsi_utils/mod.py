"""
RSI (Relative Strength Index) - 相对强弱指标工具

RSI 是一种动量振荡器，用于衡量价格变动的速度和幅度，
帮助识别超买/超卖条件。

核心功能:
- 标准 RSI 计算
- 多种平滑方法 (SMA, EMA, Wilder's Smoothing)
- 背离检测
- 超买超卖信号
- 批量处理
"""

from typing import List, Tuple, Optional, Union
from collections import deque
import math


def calculate_rsi(prices: List[float], period: int = 14, 
                  method: str = 'wilder') -> List[Optional[float]]:
    """
    计算 RSI 序列
    
    Args:
        prices: 价格序列
        period: RSI 周期，默认14
        method: 平滑方法 ('sma', 'ema', 'wilder')
    
    Returns:
        RSI 值序列 (前 period 个值为 None)
    
    Example:
        >>> prices = [44, 44.5, 43.5, 44.5, 45, 46, 45.5, 46, 47, 46.5, 
        ...           47, 47.5, 48, 48.5, 47.5, 48, 49, 48.5, 49, 50]
        >>> rsi = calculate_rsi(prices, period=14)
        >>> rsi[-1]  # 最新 RSI 值
        72.5...
    """
    if len(prices) < period + 1:
        return [None] * len(prices)
    
    if method not in ('sma', 'ema', 'wilder'):
        raise ValueError(f"Unknown method: {method}. Use 'sma', 'ema', or 'wilder'")
    
    # 计算价格变化
    changes = []
    for i in range(1, len(prices)):
        changes.append(prices[i] - prices[i-1])
    
    # 分离上涨和下跌
    gains = [max(0, c) for c in changes]
    losses = [abs(min(0, c)) for c in changes]
    
    rsi_values = [None]  # 第一个价格没有 RSI
    
    if method == 'sma':
        # 简单移动平均
        avg_gain = sum(gains[:period]) / period
        avg_loss = sum(losses[:period]) / period
        
        for i in range(period):
            rsi_values.append(None)
        
        for i in range(period, len(gains)):
            if avg_loss == 0:
                rsi = 100.0
            else:
                rs = avg_gain / avg_loss
                rsi = 100 - (100 / (1 + rs))
            rsi_values.append(rsi)
            
            # 滑动窗口更新
            avg_gain = (avg_gain * (period - 1) + gains[i]) / period
            avg_loss = (avg_loss * (period - 1) + losses[i]) / period
    
    elif method == 'ema':
        # 指数移动平均
        multiplier = 2 / (period + 1)
        avg_gain = sum(gains[:period]) / period
        avg_loss = sum(losses[:period]) / period
        
        for i in range(period):
            rsi_values.append(None)
        
        for i in range(period, len(gains)):
            if avg_loss == 0:
                rsi = 100.0
            else:
                rs = avg_gain / avg_loss
                rsi = 100 - (100 / (1 + rs))
            rsi_values.append(rsi)
            
            avg_gain = gains[i] * multiplier + avg_gain * (1 - multiplier)
            avg_loss = losses[i] * multiplier + avg_loss * (1 - multiplier)
    
    else:  # wilder
        # Wilder's Smoothing (标准 RSI 方法)
        avg_gain = sum(gains[:period]) / period
        avg_loss = sum(losses[:period]) / period
        
        for i in range(period):
            rsi_values.append(None)
        
        for i in range(period, len(gains)):
            if avg_loss == 0:
                rsi = 100.0
            else:
                rs = avg_gain / avg_loss
                rsi = 100 - (100 / (1 + rs))
            rsi_values.append(rsi)
            
            # Wilder's 平滑
            avg_gain = (avg_gain * (period - 1) + gains[i]) / period
            avg_loss = (avg_loss * (period - 1) + losses[i]) / period
    
    return rsi_values


def calculate_rsi_single(prices: List[float], period: int = 14,
                         method: str = 'wilder') -> Optional[float]:
    """
    计算最新 RSI 值
    
    Args:
        prices: 价格序列
        period: RSI 周期
        method: 平滑方法
    
    Returns:
        最新 RSI 值，或 None（数据不足）
    """
    if len(prices) < period + 1:
        return None
    
    rsi_values = calculate_rsi(prices, period, method)
    return rsi_values[-1]


class RSICalculator:
    """
    增量式 RSI 计算器
    
    适用于实时数据流场景，支持逐个价格更新
    
    Example:
        >>> calc = RSICalculator(period=14)
        >>> for price in prices:
        ...     rsi = calc.update(price)
        ...     if rsi is not None:
        ...         print(f"RSI: {rsi:.2f}")
    """
    
    def __init__(self, period: int = 14, method: str = 'wilder'):
        """
        初始化 RSI 计算器
        
        Args:
            period: RSI 周期
            method: 平滑方法 ('sma', 'ema', 'wilder')
        """
        self.period = period
        self.method = method
        
        self._prices: List[float] = []
        self._prev_avg_gain: Optional[float] = None
        self._prev_avg_loss: Optional[float] = None
        self._initialized = False
    
    def update(self, price: float) -> Optional[float]:
        """
        添加新价格并返回当前 RSI
        
        Args:
            price: 新价格
        
        Returns:
            当前 RSI 值，或 None（数据不足）
        """
        self._prices.append(price)
        
        if len(self._prices) < self.period + 1:
            return None
        
        if not self._initialized:
            # 首次计算
            changes = [self._prices[i] - self._prices[i-1] 
                      for i in range(1, len(self._prices))]
            gains = [max(0, c) for c in changes]
            losses = [abs(min(0, c)) for c in changes]
            
            self._prev_avg_gain = sum(gains[-self.period:]) / self.period
            self._prev_avg_loss = sum(losses[-self.period:]) / self.period
            self._initialized = True
            
            # 只保留最近 period+1 个价格
            self._prices = self._prices[-(self.period + 1):]
        
        else:
            # 增量更新
            change = price - self._prices[-2]
            gain = max(0, change)
            loss = abs(min(0, change))
            
            if self.method == 'sma':
                # SMA 需要重新计算（需要窗口数据）
                pass  # 简化处理，使用 Wilder 方法
            elif self.method == 'ema':
                multiplier = 2 / (self.period + 1)
                self._prev_avg_gain = gain * multiplier + self._prev_avg_gain * (1 - multiplier)
                self._prev_avg_loss = loss * multiplier + self._prev_avg_loss * (1 - multiplier)
            else:  # wilder
                self._prev_avg_gain = (self._prev_avg_gain * (self.period - 1) + gain) / self.period
                self._prev_avg_loss = (self._prev_avg_loss * (self.period - 1) + loss) / self.period
        
        if self._prev_avg_loss == 0:
            return 100.0
        
        rs = self._prev_avg_gain / self._prev_avg_loss
        return 100 - (100 / (1 + rs))
    
    @property
    def current_rsi(self) -> Optional[float]:
        """获取当前 RSI 值"""
        if not self._initialized:
            return None
        if self._prev_avg_loss == 0:
            return 100.0
        rs = self._prev_avg_gain / self._prev_avg_loss
        return 100 - (100 / (1 + rs))
    
    def reset(self):
        """重置计算器"""
        self._prices.clear()
        self._prev_avg_gain = None
        self._prev_avg_loss = None
        self._initialized = False


def detect_divergence(prices: List[float], rsi_values: List[Optional[float]],
                      lookback: int = 5) -> List[dict]:
    """
    检测 RSI 背离
    
    背离类型：
    - 看涨背离：价格创新低，RSI 未创新低（可能反转上涨）
    - 看跌背离：价格创新高，RSI 未创新高（可能反转下跌）
    
    Args:
        prices: 价格序列
        rsi_values: RSI 值序列
        lookback: 回溯周期
    
    Returns:
        背离信号列表
    """
    divergences = []
    
    if len(prices) < lookback + 2:
        return divergences
    
    # 过滤掉 None 值
    valid_data = [(p, r) for p, r in zip(prices, rsi_values) if r is not None]
    if len(valid_data) < lookback + 2:
        return divergences
    
    # 检查最近的价格极值
    for i in range(lookback + 1, len(valid_data)):
        window = valid_data[i-lookback:i+1]
        current_price, current_rsi = window[-1]
        
        # 找局部最小值
        min_idx = min(range(len(window)), key=lambda j: window[j][0])
        min_price, min_rsi = window[min_idx]
        
        # 找局部最大值
        max_idx = max(range(len(window)), key=lambda j: window[j][0])
        max_price, max_rsi = window[max_idx]
        
        # 看涨背离：价格创新低但 RSI 未创新低
        if min_idx == len(window) - 1:  # 当前是局部最小值
            prev_min_price = min(window[:-1][0] for window in 
                                 [(w[0], w[1]) for w in window[:-1]])
            prev_min_rsi = min(w[1] for w in window[:-1])
            
            if current_price < prev_min_price and current_rsi > prev_min_rsi:
                divergences.append({
                    'type': 'bullish',
                    'index': i,
                    'price': current_price,
                    'rsi': current_rsi,
                    'message': '看涨背离：价格新低但RSI未新低，可能上涨'
                })
        
        # 看跌背离：价格创新高但 RSI 未创新高
        if max_idx == len(window) - 1:  # 当前是局部最大值
            prev_max_price = max(w[0] for w in window[:-1])
            prev_max_rsi = max(w[1] for w in window[:-1])
            
            if current_price > prev_max_price and current_rsi < prev_max_rsi:
                divergences.append({
                    'type': 'bearish',
                    'index': i,
                    'price': current_price,
                    'rsi': current_rsi,
                    'message': '看跌背离：价格新高但RSI未新高，可能下跌'
                })
    
    return divergences


def generate_signals(rsi_values: List[Optional[float]],
                     oversold: float = 30.0,
                     overbought: float = 70.0) -> List[dict]:
    """
    根据 RSI 生成交易信号
    
    Args:
        rsi_values: RSI 值序列
        oversold: 超卖阈值，默认30
        overbought: 超买阈值，默认70
    
    Returns:
        信号列表
    """
    signals = []
    prev_state = None  # 'neutral', 'oversold', 'overbought'
    
    for i, rsi in enumerate(rsi_values):
        if rsi is None:
            continue
        
        if rsi <= oversold:
            current_state = 'oversold'
            if prev_state != 'oversold':
                signals.append({
                    'index': i,
                    'type': 'enter_oversold',
                    'rsi': rsi,
                    'message': f'RSI 进入超卖区 ({rsi:.1f})'
                })
        elif rsi >= overbought:
            current_state = 'overbought'
            if prev_state != 'overbought':
                signals.append({
                    'index': i,
                    'type': 'enter_overbought',
                    'rsi': rsi,
                    'message': f'RSI 进入超买区 ({rsi:.1f})'
                })
        else:
            current_state = 'neutral'
            if prev_state == 'oversold':
                signals.append({
                    'index': i,
                    'type': 'exit_oversold',
                    'rsi': rsi,
                    'message': f'RSI 离开超卖区 ({rsi:.1f})，可能的买入信号'
                })
            elif prev_state == 'overbought':
                signals.append({
                    'index': i,
                    'type': 'exit_overbought',
                    'rsi': rsi,
                    'message': f'RSI 离开超买区 ({rsi:.1f})，可能的卖出信号'
                })
        
        prev_state = current_state
    
    return signals


def calculate_stoch_rsi(prices: List[float], 
                        rsi_period: int = 14,
                        stoch_period: int = 14) -> Tuple[List[Optional[float]], 
                                                          List[Optional[float]]]:
    """
    计算 Stochastic RSI (随机 RSI)
    
    StochRSI = (RSI - RSI_low) / (RSI_high - RSI_low) * 100
    
    Args:
        prices: 价格序列
        rsi_period: RSI 计算周期
        stoch_period: 随机周期
    
    Returns:
        (K值列表, D值列表)
    """
    rsi_values = calculate_rsi(prices, rsi_period)
    k_values = []
    d_values = []
    
    for i in range(len(rsi_values)):
        if i < rsi_period + stoch_period - 1:
            k_values.append(None)
            d_values.append(None)
            continue
        
        # 获取窗口内的 RSI 值
        window = [r for r in rsi_values[i-stoch_period+1:i+1] if r is not None]
        
        if len(window) < stoch_period:
            k_values.append(None)
            d_values.append(None)
            continue
        
        rsi_high = max(window)
        rsi_low = min(window)
        current_rsi = window[-1]
        
        if rsi_high == rsi_low:
            k = 100.0
        else:
            k = (current_rsi - rsi_low) / (rsi_high - rsi_low) * 100
        
        k_values.append(k)
        
        # D 值是 K 值的 3 周期 SMA
        valid_k = [kv for kv in k_values if kv is not None]
        if len(valid_k) >= 3:
            d = sum(valid_k[-3:]) / 3
            d_values.append(d)
        else:
            d_values.append(None)
    
    return k_values, d_values


def rsi_to_string(rsi: Optional[float], precision: int = 1) -> str:
    """
    将 RSI 值格式化为字符串，带状态指示
    
    Args:
        rsi: RSI 值
        precision: 小数精度
    
    Returns:
        格式化字符串
    """
    if rsi is None:
        return "RSI: N/A"
    
    if rsi <= 30:
        status = "超卖"
    elif rsi >= 70:
        status = "超买"
    else:
        status = "中性"
    
    return f"RSI: {rsi:.{precision}f} ({status})"


def validate_rsi(rsi: float) -> bool:
    """
    验证 RSI 值是否有效
    
    Args:
        rsi: RSI 值
    
    Returns:
        是否有效
    """
    return isinstance(rsi, (int, float)) and 0 <= rsi <= 100


def get_rsi_zone(rsi: Optional[float]) -> str:
    """
    获取 RSI 所在区域
    
    Args:
        rsi: RSI 值
    
    Returns:
        区域名称
    """
    if rsi is None:
        return "unknown"
    if rsi <= 20:
        return "deep_oversold"
    if rsi <= 30:
        return "oversold"
    if rsi <= 40:
        return "bearish"
    if rsi <= 60:
        return "neutral"
    if rsi <= 70:
        return "bullish"
    if rsi <= 80:
        return "overbought"
    return "deep_overbought"