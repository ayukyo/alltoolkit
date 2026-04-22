"""
Moving Average Utils - 移动平均工具模块

提供多种移动平均算法实现，用于时间序列分析、信号处理、趋势预测等场景。

支持的移动平均类型：
- SMA (Simple Moving Average) - 简单移动平均
- EMA (Exponential Moving Average) - 指数移动平均
- WMA (Weighted Moving Average) - 加权移动平均
- CMA (Cumulative Moving Average) - 累积移动平均
- TMA (Triangular Moving Average) - 三角移动平均
- VMA (Variable Moving Average) - 可变移动平均
- HMA (Hull Moving Average) - Hull移动平均
- KAMA (Kaufman's Adaptive Moving Average) - Kaufman自适应移动平均

零外部依赖，纯Python实现。
"""

from typing import List, Optional, Tuple, Union
import math


def simple_moving_average(data: List[float], window: int) -> List[Optional[float]]:
    """
    简单移动平均 (SMA)
    
    对指定窗口内的数据取算术平均值，是最基础的移动平均方法。
    
    Args:
        data: 输入数据序列
        window: 窗口大小（周期）
    
    Returns:
        移动平均值列表，前 window-1 个元素为 None
        
    Example:
        >>> simple_moving_average([1, 2, 3, 4, 5], 3)
        [None, None, 2.0, 3.0, 4.0]
    """
    if window <= 0:
        raise ValueError("Window size must be positive")
    if window > len(data):
        return [None] * len(data)
    
    result = [None] * (window - 1)
    
    for i in range(window - 1, len(data)):
        avg = sum(data[i - window + 1:i + 1]) / window
        result.append(avg)
    
    return result


def exponential_moving_average(
    data: List[float], 
    window: int,
    smoothing: Optional[float] = None
) -> List[Optional[float]]:
    """
    指数移动平均 (EMA)
    
    对近期数据赋予更大权重，公式：EMA = α * 当前值 + (1-α) * 前一EMA
    其中 α = 2 / (window + 1)
    
    Args:
        data: 输入数据序列
        window: 窗口大小（周期）
        smoothing: 平滑因子（可选，默认为 2/(window+1)）
    
    Returns:
        移动平均值列表，第一个元素为 SMA，后续为 EMA
        
    Example:
        >>> exponential_moving_average([1, 2, 3, 4, 5], 3)
        [None, None, 2.0, 2.75, 3.625]
    """
    if window <= 0:
        raise ValueError("Window size must be positive")
    if len(data) < window:
        return [None] * len(data)
    
    # 默认平滑因子
    if smoothing is None:
        smoothing = 2.0 / (window + 1)
    
    result = [None] * (window - 1)
    
    # 第一个EMA值使用SMA
    first_ema = sum(data[:window]) / window
    result.append(first_ema)
    
    # 后续使用EMA公式
    ema = first_ema
    for i in range(window, len(data)):
        ema = smoothing * data[i] + (1 - smoothing) * ema
        result.append(ema)
    
    return result


def weighted_moving_average(data: List[float], window: int) -> List[Optional[float]]:
    """
    加权移动平均 (WMA)
    
    线性加权，近期数据权重更大。
    权重从 1 到 window 线性递增。
    
    Args:
        data: 输入数据序列
        window: 窗口大小（周期）
    
    Returns:
        移动平均值列表
        
    Example:
        >>> weighted_moving_average([1, 2, 3, 4, 5], 3)
        [None, None, 2.3333333333333335, 3.3333333333333335, 4.333333333333333]
    """
    if window <= 0:
        raise ValueError("Window size must be positive")
    if window > len(data):
        return [None] * len(data)
    
    result = [None] * (window - 1)
    
    # 权重总和: 1 + 2 + ... + window = window * (window + 1) / 2
    weight_sum = window * (window + 1) / 2
    
    for i in range(window - 1, len(data)):
        weighted_sum = sum(
            data[i - window + 1 + j] * (j + 1) 
            for j in range(window)
        )
        result.append(weighted_sum / weight_sum)
    
    return result


def cumulative_moving_average(data: List[float]) -> List[float]:
    """
    累积移动平均 (CMA)
    
    从开始到当前位置的所有数据的平均值。
    
    Args:
        data: 输入数据序列
    
    Returns:
        累积移动平均值列表
        
    Example:
        >>> cumulative_moving_average([1, 2, 3, 4, 5])
        [1.0, 1.5, 2.0, 2.5, 3.0]
    """
    if not data:
        return []
    
    result = []
    cumsum = 0
    
    for i, val in enumerate(data):
        cumsum += val
        result.append(cumsum / (i + 1))
    
    return result


def triangular_moving_average(data: List[float], window: int) -> List[Optional[float]]:
    """
    三角移动平均 (TMA)
    
    对SMA再次取SMA，相当于双重平滑，更加平滑但对趋势变化反应更慢。
    
    Args:
        data: 输入数据序列
        window: 窗口大小（周期）
    
    Returns:
        三角移动平均值列表
        
    Example:
        >>> triangular_moving_average([1, 2, 3, 4, 5, 6, 7], 3)
        [None, None, None, None, 3.0, 4.0, 5.0]
    """
    if window <= 0:
        raise ValueError("Window size must be positive")
    
    # 先计算SMA
    sma = simple_moving_average(data, window)
    
    # 将None替换为用于计算的值（这里用第一个有效值，但实际不会被用到）
    # 再对SMA取SMA
    half_window = (window + 1) // 2
    
    result = [None] * (window + half_window - 2) if window > 1 else [None] * (window - 1)
    
    # 找到SMA中第一个有效值的索引
    first_valid = window - 1
    
    # 对SMA的有效部分再取SMA
    valid_sma = [s for s in sma if s is not None]
    if len(valid_sma) < half_window:
        return [None] * len(data)
    
    second_sma = simple_moving_average(valid_sma, half_window)
    
    # 组合结果
    result = [None] * (len(data) - len(second_sma))
    result.extend([v for v in second_sma if v is not None])
    
    # 确保长度正确
    while len(result) < len(data):
        result.insert(0, None)
    while len(result) > len(data):
        result.pop(0)
    
    return result


def hull_moving_average(data: List[float], window: int) -> List[Optional[float]]:
    """
    Hull移动平均 (HMA)
    
    由Alan Hull开发，旨在减少滞后同时保持平滑。
    公式：WMA(2*WMA(n/2) - WMA(n), sqrt(n))
    
    Args:
        data: 输入数据序列
        window: 窗口大小（周期）
    
    Returns:
        Hull移动平均值列表
        
    Example:
        >>> hull_moving_average([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], 5)
    """
    if window <= 0:
        raise ValueError("Window size must be positive")
    
    sqrt_window = int(math.sqrt(window))
    if sqrt_window < 1:
        sqrt_window = 1
    
    half_window = window // 2
    
    if len(data) < window:
        return [None] * len(data)
    
    # 计算 WMA(n/2)
    wma_half = weighted_moving_average(data, half_window)
    
    # 计算 WMA(n)
    wma_full = weighted_moving_average(data, window)
    
    # 计算 2*WMA(n/2) - WMA(n)
    diff = []
    for i in range(len(data)):
        if wma_half[i] is None or wma_full[i] is None:
            diff.append(None)
        else:
            diff.append(2 * wma_half[i] - wma_full[i])
    
    # 计算最终的 WMA(sqrt(n))
    result = weighted_moving_average(
        [d for d in diff if d is not None],
        sqrt_window
    )
    
    # 对齐结果长度
    none_count = len(data) - len([r for r in result if r is not None])
    final_result = [None] * none_count + [r for r in result if r is not None]
    
    return final_result


def kaufman_adaptive_moving_average(
    data: List[float], 
    window: int = 10,
    fast_period: int = 2,
    slow_period: int = 30
) -> List[Optional[float]]:
    """
    Kaufman自适应移动平均 (KAMA)
    
    根据市场波动性自适应调整平滑系数。
    趋势明显时快速反应，震荡时慢速平滑。
    
    Args:
        data: 输入数据序列
        window: 效率比率计算周期（默认10）
        fast_period: 快速EMA周期（默认2）
        slow_period: 慢速EMA周期（默认30）
    
    Returns:
        KAMA值列表
        
    Example:
        >>> kaufman_adaptive_moving_average([1, 2, 3, 4, 5, 4, 3, 2, 1], 3)
    """
    if window <= 0:
        raise ValueError("Window size must be positive")
    if len(data) < window + 1:
        return [None] * len(data)
    
    # 计算平滑常数
    fast_sc = 2.0 / (fast_period + 1)
    slow_sc = 2.0 / (slow_period + 1)
    
    result = [None] * window
    
    # 第一个KAMA值使用SMA
    first_kama = sum(data[:window + 1]) / (window + 1)
    result.append(first_kama)
    
    kama = first_kama
    
    for i in range(window + 1, len(data)):
        # 计算方向变化
        direction = abs(data[i] - data[i - window])
        
        # 计算波动性
        volatility = sum(
            abs(data[j] - data[j - 1]) 
            for j in range(i - window + 1, i + 1)
        )
        
        # 计算效率比率
        if volatility == 0:
            er = 0
        else:
            er = direction / volatility
        
        # 计算平滑系数
        sc = er * (fast_sc - slow_sc) + slow_sc
        sc = sc * sc  # 平方
        
        # 计算KAMA
        kama = kama + sc * (data[i] - kama)
        result.append(kama)
    
    return result


def volume_weighted_moving_average(
    prices: List[float], 
    volumes: List[float], 
    window: int
) -> List[Optional[float]]:
    """
    成交量加权移动平均 (VWMA)
    
    以成交量为权重计算加权平均价格。
    
    Args:
        prices: 价格序列
        volumes: 成交量序列
        window: 窗口大小
    
    Returns:
        VWMA值列表
        
    Example:
        >>> volume_weighted_moving_average([10, 11, 12], [100, 200, 150], 2)
    """
    if len(prices) != len(volumes):
        raise ValueError("Prices and volumes must have same length")
    if window <= 0:
        raise ValueError("Window size must be positive")
    if window > len(prices):
        return [None] * len(prices)
    
    result = [None] * (window - 1)
    
    for i in range(window - 1, len(prices)):
        weighted_sum = sum(
            prices[i - window + 1 + j] * volumes[i - window + 1 + j]
            for j in range(window)
        )
        volume_sum = sum(volumes[i - window + 1:i + 1])
        
        if volume_sum == 0:
            result.append(None)
        else:
            result.append(weighted_sum / volume_sum)
    
    return result


def moving_average_convergence_divergence(
    data: List[float],
    fast_period: int = 12,
    slow_period: int = 26,
    signal_period: int = 9
) -> Tuple[List[Optional[float]], List[Optional[float]], List[Optional[float]]]:
    """
    MACD (移动平均收敛发散指标)
    
    Args:
        data: 输入数据序列
        fast_period: 快线周期（默认12）
        slow_period: 慢线周期（默认26）
        signal_period: 信号线周期（默认9）
    
    Returns:
        (MACD线, 信号线, 柱状图) 三元组
        
    Example:
        >>> macd_line, signal, hist = moving_average_convergence_divergence(data, 12, 26, 9)
    """
    if fast_period <= 0 or slow_period <= 0 or signal_period <= 0:
        raise ValueError("All periods must be positive")
    if fast_period >= slow_period:
        raise ValueError("Fast period must be less than slow period")
    
    # 计算快慢EMA
    fast_ema = exponential_moving_average(data, fast_period)
    slow_ema = exponential_moving_average(data, slow_period)
    
    # 计算MACD线（快EMA - 慢EMA）
    macd_line = []
    first_valid = slow_period - 1
    
    for i in range(len(data)):
        if i < first_valid or fast_ema[i] is None or slow_ema[i] is None:
            macd_line.append(None)
        else:
            macd_line.append(fast_ema[i] - slow_ema[i])
    
    # 计算信号线（MACD的EMA）
    valid_macd = [m for m in macd_line if m is not None]
    if len(valid_macd) < signal_period:
        return macd_line, [None] * len(data), [None] * len(data)
    
    signal_ema = exponential_moving_average(valid_macd, signal_period)
    
    # 对齐信号线
    signal_line = [None] * (len(data) - len(signal_ema)) + signal_ema
    
    # 计算柱状图
    histogram = []
    for i in range(len(data)):
        if macd_line[i] is None or signal_line[i] is None:
            histogram.append(None)
        else:
            histogram.append(macd_line[i] - signal_line[i])
    
    return macd_line, signal_line, histogram


def average_true_range(
    highs: List[float],
    lows: List[float],
    closes: List[float],
    window: int = 14
) -> List[Optional[float]]:
    """
    平均真实波幅 (ATR)
    
    用于衡量市场波动性的指标。
    
    Args:
        highs: 最高价序列
        lows: 最低价序列
        closes: 收盘价序列
        window: 窗口大小（默认14）
    
    Returns:
        ATR值列表
    """
    if not (len(highs) == len(lows) == len(closes)):
        raise ValueError("All price series must have same length")
    if window <= 0:
        raise ValueError("Window size must be positive")
    
    n = len(highs)
    if n < 2:
        return [None] * n
    
    # 计算真实波幅
    true_ranges = []
    for i in range(n):
        if i == 0:
            tr = highs[i] - lows[i]
        else:
            tr = max(
                highs[i] - lows[i],
                abs(highs[i] - closes[i - 1]),
                abs(lows[i] - closes[i - 1])
            )
        true_ranges.append(tr)
    
    # 计算ATR（使用EMA）
    if n < window:
        return [None] * n
    
    result = [None] * (window - 1)
    
    # 第一个ATR使用SMA
    first_atr = sum(true_ranges[:window]) / window
    result.append(first_atr)
    
    # 后续使用EMA风格的计算
    atr = first_atr
    for i in range(window, n):
        atr = (atr * (window - 1) + true_ranges[i]) / window
        result.append(atr)
    
    return result


def bollinger_bands(
    data: List[float],
    window: int = 20,
    num_std: float = 2.0
) -> Tuple[List[Optional[float]], List[Optional[float]], List[Optional[float]]]:
    """
    布林带 (Bollinger Bands)
    
    Args:
        data: 输入数据序列
        window: 窗口大小（默认20）
        num_std: 标准差倍数（默认2）
    
    Returns:
        (上轨, 中轨, 下轨) 三元组
        
    Example:
        >>> upper, middle, lower = bollinger_bands(data, 20, 2.0)
    """
    if window <= 0:
        raise ValueError("Window size must be positive")
    if num_std < 0:
        raise ValueError("Standard deviation multiplier must be non-negative")
    
    n = len(data)
    if n < window:
        return [None] * n, [None] * n, [None] * n
    
    middle_band = simple_moving_average(data, window)
    upper_band = [None] * (window - 1)
    lower_band = [None] * (window - 1)
    
    for i in range(window - 1, n):
        # 计算标准差
        window_data = data[i - window + 1:i + 1]
        mean = middle_band[i]
        variance = sum((x - mean) ** 2 for x in window_data) / window
        std = math.sqrt(variance)
        
        upper_band.append(mean + num_std * std)
        lower_band.append(mean - num_std * std)
    
    return upper_band, middle_band, lower_band


def rolling_statistics(
    data: List[float],
    window: int,
    stats: List[str] = ['mean', 'std', 'min', 'max']
) -> dict:
    """
    滚动统计量计算
    
    一次性计算多种滚动统计量。
    
    Args:
        data: 输入数据序列
        window: 窗口大小
        stats: 需要计算的统计量列表
               支持: 'mean', 'std', 'var', 'min', 'max', 'sum', 'median'
    
    Returns:
        字典，键为统计量名称，值为结果列表
        
    Example:
        >>> stats = rolling_statistics([1, 2, 3, 4, 5], 3, ['mean', 'std', 'min', 'max'])
    """
    valid_stats = {'mean', 'std', 'var', 'min', 'max', 'sum', 'median'}
    
    for s in stats:
        if s not in valid_stats:
            raise ValueError(f"Invalid stat: {s}. Must be one of {valid_stats}")
    
    if window <= 0:
        raise ValueError("Window size must be positive")
    
    n = len(data)
    result = {s: [None] * (window - 1) for s in stats}
    
    for i in range(window - 1, n):
        window_data = data[i - window + 1:i + 1]
        
        if 'mean' in stats:
            result['mean'].append(sum(window_data) / window)
        
        if 'std' in stats or 'var' in stats:
            mean = sum(window_data) / window
            variance = sum((x - mean) ** 2 for x in window_data) / window
            
            if 'var' in stats:
                result['var'].append(variance)
            if 'std' in stats:
                result['std'].append(math.sqrt(variance))
        
        if 'min' in stats:
            result['min'].append(min(window_data))
        
        if 'max' in stats:
            result['max'].append(max(window_data))
        
        if 'sum' in stats:
            result['sum'].append(sum(window_data))
        
        if 'median' in stats:
            sorted_data = sorted(window_data)
            mid = window // 2
            if window % 2 == 0:
                result['median'].append((sorted_data[mid - 1] + sorted_data[mid]) / 2)
            else:
                result['median'].append(sorted_data[mid])
    
    return result


# 便捷类封装
class MovingAverage:
    """
    移动平均计算器类
    
    提供面向对象的接口，支持流式数据更新。
    
    Example:
        >>> ma = MovingAverage(window=5, method='sma')
        >>> for val in [1, 2, 3, 4, 5]:
        ...     result = ma.update(val)
        ...     print(result)
    """
    
    METHODS = {
        'sma': simple_moving_average,
        'ema': exponential_moving_average,
        'wma': weighted_moving_average,
        'tma': triangular_moving_average,
        'hma': hull_moving_average,
        'kama': kaufman_adaptive_moving_average,
    }
    
    def __init__(self, window: int, method: str = 'sma', **kwargs):
        """
        初始化移动平均计算器
        
        Args:
            window: 窗口大小
            method: 方法名称 ('sma', 'ema', 'wma', 'tma', 'hma', 'kama')
            **kwargs: 传递给底层函数的额外参数
        """
        if method not in self.METHODS:
            raise ValueError(f"Unknown method: {method}. Valid: {list(self.METHODS.keys())}")
        
        self.window = window
        self.method = method
        self.kwargs = kwargs
        self._data: List[float] = []
        self._func = self.METHODS[method]
    
    def update(self, value: float) -> Optional[float]:
        """
        添加新值并返回当前移动平均值
        
        Args:
            value: 新数据点
            
        Returns:
            当前移动平均值，如果数据不足则返回None
        """
        self._data.append(value)
        result = self._func(self._data, self.window, **self.kwargs)
        return result[-1] if result else None
    
    @property
    def current(self) -> Optional[float]:
        """获取当前移动平均值"""
        if not self._data:
            return None
        result = self._func(self._data, self.window, **self.kwargs)
        return result[-1] if result and result[-1] is not None else None
    
    @property
    def data(self) -> List[float]:
        """获取已存储的数据"""
        return self._data.copy()
    
    def reset(self) -> None:
        """重置计算器"""
        self._data.clear()
    
    def compute(self, data: List[float]) -> List[Optional[float]]:
        """
        一次性计算整组数据的移动平均
        
        Args:
            data: 数据序列
            
        Returns:
            移动平均值列表
        """
        return self._func(data, self.window, **self.kwargs)


if __name__ == "__main__":
    # 简单演示
    test_data = [10, 12, 14, 13, 15, 17, 16, 18, 20, 19]
    
    print("=== Moving Average Utils Demo ===\n")
    
    print(f"Input data: {test_data}\n")
    
    print(f"SMA(3): {simple_moving_average(test_data, 3)}")
    print(f"EMA(3): {exponential_moving_average(test_data, 3)}")
    print(f"WMA(3): {weighted_moving_average(test_data, 3)}")
    print(f"CMA: {cumulative_moving_average(test_data)}")
    
    print(f"\nBollinger Bands(5): {bollinger_bands(test_data, 5)}")
    
    print(f"\nRolling Stats(3): {rolling_statistics(test_data, 3)}")
    
    # 类方式使用
    print("\n=== OOP Interface ===")
    ma = MovingAverage(window=3, method='ema')
    for val in test_data[:5]:
        result = ma.update(val)
        print(f"  Value: {val}, EMA: {result}")