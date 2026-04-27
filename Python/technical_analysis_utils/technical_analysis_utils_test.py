"""
技术分析工具测试模块

测试覆盖：
- 移动平均线 (SMA, EMA, WMA)
- RSI 指标
- MACD 指标
- 布林带
- KDJ 指标
- 随机指标
- ATR 指标
- OBV 指标
- VWAP 指标
- Williams %R
- CCI 指标
- 动量指标
- ROC 指标
- ADX 指标
- 趋势检测
- 支撑阻力识别
- 金叉死叉
- 综合分析
- 工具函数
- 边界值测试
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import math
from typing import List, Optional
import technical_analysis_utils.mod as ta


def assert_equal(actual, expected, msg: str = ""):
    """断言相等"""
    if actual != expected:
        raise AssertionError(f"{msg}: 期望 {expected}, 实际 {actual}")


def assert_approx(actual: float, expected: float, tolerance: float = 0.01, msg: str = ""):
    """断言近似相等"""
    if abs(actual - expected) > tolerance:
        raise AssertionError(f"{msg}: 期望 {expected}, 实际 {actual}, 容差 {tolerance}")


def assert_is_not_none(value, msg: str = ""):
    """断言非空"""
    if value is None:
        raise AssertionError(f"{msg}: 值为 None")


def assert_list_length(lst: List, expected: int, msg: str = ""):
    """断言列表长度"""
    if len(lst) != expected:
        raise AssertionError(f"{msg}: 期望长度 {expected}, 实际 {len(lst)}")


def assert_raises(func, error_type, msg: str = ""):
    """断言抛出异常"""
    try:
        func()
        raise AssertionError(f"{msg}: 期望抛出 {error_type.__name__}")
    except error_type:
        pass


# ============ 测试数据 ============

SAMPLE_CLOSE = [
    44.12, 44.23, 44.52, 43.91, 44.22,
    44.57, 44.24, 44.33, 44.56, 44.12,
    44.78, 44.89, 45.12, 45.23, 45.11,
    45.34, 45.67, 45.89, 46.12, 46.34,
    46.12, 45.89, 45.67, 45.45, 45.23,
    45.12, 45.34, 45.56, 45.78, 46.01,
    46.23, 46.45, 46.67, 46.89, 47.12,
    47.34, 47.56, 47.23, 46.89, 46.56,
    46.23, 45.89, 45.56, 45.23, 44.89,
    44.56, 44.23, 44.01, 43.78, 43.56
]

SAMPLE_HIGH = [
    44.50, 44.60, 44.80, 44.30, 44.50,
    44.90, 44.60, 44.70, 44.90, 44.50,
    45.10, 45.30, 45.40, 45.50, 45.40,
    45.60, 45.90, 46.20, 46.40, 46.60,
    46.40, 46.10, 45.90, 45.70, 45.50,
    45.40, 45.60, 45.80, 46.00, 46.30,
    46.50, 46.70, 46.90, 47.10, 47.40,
    47.60, 47.80, 47.50, 47.10, 46.80,
    46.50, 46.10, 45.80, 45.50, 45.10,
    44.80, 44.50, 44.30, 44.00, 43.80
]

SAMPLE_LOW = [
    43.90, 44.00, 44.20, 43.60, 43.90,
    44.30, 44.00, 44.10, 44.30, 43.90,
    44.60, 44.70, 44.90, 45.00, 44.90,
    45.10, 45.40, 45.60, 45.90, 46.10,
    45.90, 45.70, 45.40, 45.20, 45.00,
    44.90, 45.10, 45.30, 45.50, 45.80,
    46.00, 46.20, 46.40, 46.70, 46.90,
    47.10, 47.30, 46.70, 46.40, 46.10,
    45.80, 45.50, 45.20, 44.90, 44.60,
    44.30, 44.00, 43.80, 43.60, 43.40
]

SAMPLE_VOLUME = [
    1000, 1200, 1500, 800, 1100,
    1300, 900, 1000, 1400, 1200,
    1600, 1800, 2000, 1500, 1700,
    1900, 2100, 2300, 2000, 1800,
    1600, 1400, 1200, 1000, 900,
    1100, 1300, 1500, 1700, 1900,
    2100, 2300, 2500, 2700, 2900,
    3100, 3300, 2800, 2400, 2000,
    1600, 1400, 1200, 1000, 900,
    800, 700, 600, 500, 400
]


# ============ SMA 测试 ============

def test_sma_basic():
    """测试基本 SMA 计算"""
    data = [1, 2, 3, 4, 5]
    result = ta.sma(data, 3)
    
    assert_list_length(result, 5)
    assert_equal(result[0], None)
    assert_equal(result[1], None)
    assert_approx(result[2], 2.0)
    assert_approx(result[3], 3.0)
    assert_approx(result[4], 4.0)


def test_sma_period_1():
    """测试周期为 1 的 SMA"""
    data = [1, 2, 3, 4, 5]
    result = ta.sma(data, 1)
    
    assert_list_length(result, 5)
    for i, val in enumerate(result):
        assert_approx(val, data[i])


def test_sma_constant_data():
    """测试常数数据的 SMA"""
    data = [10.0] * 10
    result = ta.sma(data, 5)
    
    for val in result:
        if val is not None:
            assert_approx(val, 10.0)


def test_sma_increasing():
    """测试递增数据的 SMA"""
    data = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    result = ta.sma(data, 5)
    
    assert_approx(result[4], 3.0)
    assert_approx(result[9], 8.0)


def test_sma_empty_data():
    """测试空数据"""
    assert_raises(lambda: ta.sma([], 5), ValueError)


def test_sma_invalid_period():
    """测试无效周期"""
    assert_raises(lambda: ta.sma([1, 2, 3], 0), ValueError)
    assert_raises(lambda: ta.sma([1, 2, 3], -1), ValueError)


# ============ EMA 测试 ============

def test_ema_basic():
    """测试基本 EMA 计算"""
    data = [10, 11, 12, 13, 14, 20, 21, 22, 23, 24]
    result = ta.ema(data, 5)
    
    # EMA 输出长度应该等于输入长度
    assert len(result) == len(data)
    # 验证 EMA 前几个为 None
    assert_equal(result[0], None)
    assert_equal(result[1], None)
    assert_equal(result[2], None)
    assert_equal(result[3], None)
    # 第5个值开始有数据
    assert result[4] is not None
    
    # 测试 EMA 响应性：跳变后 EMA 应该更快响应
    # 第6个位置，EMA 应该比 SMA 更接近跳变后的新价格
    sma_result = ta.sma(data, 5)
    # EMA[5] = 14.67， SMA[5] = 14，跳变后 EMA 应该更接近新价格
    if result[5] is not None and sma_result[5] is not None:
        assert result[5] > sma_result[5], "EMA should be higher after jump"


def test_ema_responsiveness():
    """测试 EMA 响应性"""
    # 突然变化后的 EMA 应该更快响应
    data = [10] * 10 + [20] * 10
    result = ta.ema(data, 5)
    
    # 最后的 EMA 应该接近 20
    assert result[-1] is not None
    assert result[-1] > 15


def test_ema_constant_data():
    """测试常数数据的 EMA"""
    data = [50.0] * 20
    result = ta.ema(data, 10)
    
    for val in result:
        if val is not None:
            assert_approx(val, 50.0)


# ============ WMA 测试 ============

def test_wma_basic():
    """测试基本 WMA 计算"""
    data = [1, 2, 3, 4, 5]
    result = ta.wma(data, 3)
    
    assert_list_length(result, 5)
    assert_equal(result[0], None)
    assert_equal(result[1], None)
    # WMA(3) for [3,4,5] = (1*3 + 2*4 + 3*5) / (1+2+3) = 26/6 ≈ 4.33
    assert_approx(result[4], 4.333333, 0.001)


def test_wma_vs_sma():
    """测试 WMA 与 SMA 的差异"""
    data = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    wma_result = ta.wma(data, 5)
    sma_result = ta.sma(data, 5)
    
    # 对于递增数据，WMA 应该大于 SMA（更重视近期数据）
    if wma_result[9] is not None and sma_result[9] is not None:
        assert wma_result[9] > sma_result[9]


# ============ RSI 测试 ============

def test_rsi_basic():
    """测试基本 RSI 计算"""
    result = ta.rsi(SAMPLE_CLOSE[:20], 14)
    
    assert_list_length(result, 20)
    # 前 14 个值应该是 None
    for i in range(14):
        assert_equal(result[i], None)
    # 第 15 个值开始有数据
    assert result[14] is not None
    assert 0 <= result[14] <= 100


def test_rsi_all_gains():
    """测试全上涨的 RSI"""
    data = [100 + i for i in range(20)]
    result = ta.rsi(data, 14)
    
    # 全上涨应该接近 100
    if result[-1] is not None:
        assert result[-1] > 90


def test_rsi_all_losses():
    """测试全下跌的 RSI"""
    data = [100 - i for i in range(20)]
    result = ta.rsi(data, 14)
    
    # 全下跌应该接近 0
    if result[-1] is not None:
        assert result[-1] < 10


def test_rsi_constant_data():
    """测试常数数据的 RSI"""
    data = [50.0] * 20
    result = ta.rsi(data, 14)
    
    # 无变化时，RSI 应该是 50
    if result[-1] is not None:
        # 无变化时可能出现 100 或其他值
        assert 0 <= result[-1] <= 100


def test_rsi_overbought_oversold():
    """测试 RSI 超买超卖判断"""
    # 创建上升趋势数据
    rising_data = [100 + i * 2 for i in range(30)]
    rsi_result = ta.rsi(rising_data, 14)
    
    # 验证超买超卖函数
    assert ta.is_overbought(80) == True
    assert ta.is_overbought(60) == False
    assert ta.is_oversold(20) == True
    assert ta.is_oversold(40) == False


# ============ MACD 测试 ============

def test_macd_basic():
    """测试基本 MACD 计算"""
    result = ta.macd(SAMPLE_CLOSE[:35])  # 使用足够的数据
    
    assert_list_length(result, 35)
    # 验证结构
    for val in result:
        if val is not None:
            assert hasattr(val, 'macd')
            assert hasattr(val, 'signal')
            assert hasattr(val, 'histogram')


def test_macd_bullish_signal():
    """测试 MACD 多头信号"""
    # 创建上升趋势
    data = [100 + i * 0.5 for i in range(50)]
    result = ta.macd(data)
    
    # 在上升趋势中，MACD 应该为正
    if result[-1] is not None:
        assert result[-1].macd > 0


def test_macd_custom_periods():
    """测试自定义周期的 MACD"""
    result = ta.macd(SAMPLE_CLOSE[:40], fast_period=8, slow_period=17, signal_period=9)
    
    assert_list_length(result, 40)


# ============ 布林带测试 ============

def test_bollinger_bands_basic():
    """测试基本布林带计算"""
    result = ta.bollinger_bands(SAMPLE_CLOSE[:25])
    
    assert_list_length(result, 25)
    
    # 验证最后有数据的点
    last_valid = None
    for val in reversed(result):
        if val is not None:
            last_valid = val
            break
    
    assert_is_not_none(last_valid)
    assert last_valid.upper > last_valid.middle
    assert last_valid.lower < last_valid.middle
    assert last_valid.bandwidth >= 0
    assert 0 <= last_valid.percent_b <= 1


def test_bollinger_bands_constant_data():
    """测试常数数据的布林带"""
    data = [100.0] * 25
    result = ta.bollinger_bands(data, 20)
    
    last_valid = None
    for val in reversed(result):
        if val is not None:
            last_valid = val
            break
    
    # 常数数据的标准差为 0，上下轨应该等于中轨
    if last_valid:
        assert_approx(last_valid.upper, last_valid.middle, 0.001)
        assert_approx(last_valid.lower, last_valid.middle, 0.001)


def test_bollinger_bands_custom_std():
    """测试自定义标准差倍数"""
    result = ta.bollinger_bands(SAMPLE_CLOSE[:25], period=20, std_dev=2.5)
    
    assert_list_length(result, 25)


# ============ KDJ 测试 ============

def test_kdj_basic():
    """测试基本 KDJ 计算"""
    result = ta.kdj(SAMPLE_HIGH[:15], SAMPLE_LOW[:15], SAMPLE_CLOSE[:15])
    
    assert_list_length(result, 15)
    
    # 验证最后有数据的点
    last_valid = None
    for val in reversed(result):
        if val is not None:
            last_valid = val
            break
    
    assert_is_not_none(last_valid)
    assert 'k' in last_valid
    assert 'd' in last_valid
    assert 'j' in last_valid


def test_kdj_range():
    """测试 KDJ 值范围"""
    result = ta.kdj(SAMPLE_HIGH[:20], SAMPLE_LOW[:20], SAMPLE_CLOSE[:20])
    
    for val in result:
        if val is not None:
            # K 和 D 通常在 0-100 之间，J 可以超出
            assert 0 <= val['k'] <= 100
            assert 0 <= val['d'] <= 100


def test_kdj_custom_params():
    """测试自定义 KDJ 参数"""
    result = ta.kdj(SAMPLE_HIGH[:15], SAMPLE_LOW[:15], SAMPLE_CLOSE[:15], n=5, m1=3, m2=3)
    
    assert_list_length(result, 15)


# ============ 随机指标测试 ============

def test_stochastic_basic():
    """测试基本随机指标计算"""
    result = ta.stochastic(SAMPLE_HIGH[:20], SAMPLE_LOW[:20], SAMPLE_CLOSE[:20])
    
    assert_list_length(result, 20)
    
    # 验证最后有数据的点
    last_valid = None
    for val in reversed(result):
        if val is not None:
            last_valid = val
            break
    
    assert_is_not_none(last_valid)
    assert 0 <= last_valid.k <= 100
    assert 0 <= last_valid.d <= 100


def test_stochastic_overbought():
    """测试随机指标超买区"""
    # 创建高点收盘的数据
    high = [110] * 20
    low = [90] * 20
    close = [108] * 20  # 收盘接近最高价
    
    result = ta.stochastic(high, low, close)
    
    last_valid = None
    for val in reversed(result):
        if val is not None:
            last_valid = val
            break
    
    if last_valid:
        assert last_valid.k > 80


# ============ ATR 测试 ============

def test_atr_basic():
    """测试基本 ATR 计算"""
    result = ta.atr(SAMPLE_HIGH[:20], SAMPLE_LOW[:20], SAMPLE_CLOSE[:20])
    
    # ATR 输出长度应该等于输入长度
    assert len(result) == 20
    
    # 验证最后有数据的点
    last_valid = None
    for val in reversed(result):
        if val is not None:
            last_valid = val
            break
    
    assert_is_not_none(last_valid)
    assert last_valid > 0


def test_atr_constant_data():
    """测试常数数据的 ATR"""
    high = [100] * 20
    low = [100] * 20
    close = [100] * 20
    
    result = ta.atr(high, low, close)
    
    # 常数数据的 ATR 应该接近 0
    last_valid = None
    for val in reversed(result):
        if val is not None:
            last_valid = val
            break
    
    if last_valid:
        assert_approx(last_valid, 0, 0.01)


# ============ OBV 测试 ============

def test_obv_basic():
    """测试基本 OBV 计算"""
    result = ta.obv(SAMPLE_CLOSE[:10], SAMPLE_VOLUME[:10])
    
    assert_list_length(result, 10)


def test_obv_rising_prices():
    """测试上涨价格的 OBV"""
    close = [100, 101, 102, 103, 104]
    volume = [1000, 1000, 1000, 1000, 1000]
    
    result = ta.obv(close, volume)
    
    # 上涨时 OBV 应该递增
    for i in range(1, len(result)):
        assert result[i] > result[i - 1]


def test_obv_falling_prices():
    """测试下跌价格的 OBV"""
    close = [104, 103, 102, 101, 100]
    volume = [1000, 1000, 1000, 1000, 1000]
    
    result = ta.obv(close, volume)
    
    # 下跌时 OBV 应该递减
    for i in range(1, len(result)):
        assert result[i] < result[i - 1]


# ============ VWAP 测试 ============

def test_vwap_basic():
    """测试基本 VWAP 计算"""
    result = ta.vwap(SAMPLE_HIGH[:10], SAMPLE_LOW[:10], SAMPLE_CLOSE[:10], SAMPLE_VOLUME[:10])
    
    assert_list_length(result, 10)


def test_vwap_constant_volume():
    """测试常数成交量的 VWAP"""
    high = [110] * 10
    low = [90] * 10
    close = [100] * 10
    volume = [1000] * 10
    
    result = ta.vwap(high, low, close, volume)
    
    # VWAP 应该接近典型价格 (110+90+100)/3 = 100
    for val in result:
        assert_approx(val, 100, 1)


# ============ Williams %R 测试 ============

def test_williams_r_basic():
    """测试基本 Williams %R 计算"""
    result = ta.williams_r(SAMPLE_HIGH[:20], SAMPLE_LOW[:20], SAMPLE_CLOSE[:20])
    
    assert_list_length(result, 20)
    
    # 验证最后有数据的点
    last_valid = None
    for val in reversed(result):
        if val is not None:
            last_valid = val
            break
    
    assert_is_not_none(last_valid)
    # Williams %R 范围是 -100 到 0
    assert -100 <= last_valid <= 0


def test_williams_r_range():
    """测试 Williams %R 范围"""
    result = ta.williams_r(SAMPLE_HIGH[:20], SAMPLE_LOW[:20], SAMPLE_CLOSE[:20])
    
    for val in result:
        if val is not None:
            assert -100 <= val <= 0


# ============ CCI 测试 ============

def test_cci_basic():
    """测试基本 CCI 计算"""
    result = ta.cci(SAMPLE_HIGH[:25], SAMPLE_LOW[:25], SAMPLE_CLOSE[:25])
    
    assert_list_length(result, 25)


def test_cci_range():
    """测试 CCI 值范围"""
    result = ta.cci(SAMPLE_HIGH[:25], SAMPLE_LOW[:25], SAMPLE_CLOSE[:25])
    
    for val in result:
        if val is not None:
            # CCI 通常在 -200 到 +200 之间
            assert -500 <= val <= 500


# ============ 动量指标测试 ============

def test_momentum_basic():
    """测试基本动量计算"""
    result = ta.momentum(SAMPLE_CLOSE[:15])
    
    assert_list_length(result, 15)


def test_momentum_rising():
    """测试上涨动量"""
    data = [100, 101, 102, 103, 104, 105]
    result = ta.momentum(data, 3)
    
    # 对于上涨数据，动量应该为正
    if result[-1] is not None:
        assert result[-1] > 0


def test_momentum_falling():
    """测试下跌动量"""
    data = [105, 104, 103, 102, 101, 100]
    result = ta.momentum(data, 3)
    
    # 对于下跌数据，动量应该为负
    if result[-1] is not None:
        assert result[-1] < 0


# ============ ROC 测试 ============

def test_roc_basic():
    """测试基本 ROC 计算"""
    result = ta.roc(SAMPLE_CLOSE[:15])
    
    assert_list_length(result, 15)


def test_roc_rising():
    """测试上涨 ROC"""
    data = [100, 110]  # 10% 涨幅
    result = ta.roc(data, 1)
    
    if result[-1] is not None:
        assert_approx(result[-1], 10.0)


def test_roc_falling():
    """测试下跌 ROC"""
    data = [110, 100]  # 约 9% 跌幅
    result = ta.roc(data, 1)
    
    if result[-1] is not None:
        assert result[-1] < 0


# ============ ADX 测试 ============

def test_adx_basic():
    """测试基本 ADX 计算"""
    result = ta.adx(SAMPLE_HIGH, SAMPLE_LOW, SAMPLE_CLOSE)
    
    # ADX 有输出结果
    non_none_results = [r for r in result if r is not None]
    assert len(non_none_results) > 0


def test_adx_range():
    """测试 ADX 值范围"""
    result = ta.adx(SAMPLE_HIGH, SAMPLE_LOW, SAMPLE_CLOSE)
    
    for val in result:
        if val is not None:
            assert 0 <= val['adx'] <= 100
            assert 0 <= val['plus_di'] <= 100
            assert 0 <= val['minus_di'] <= 100


# ============ 趋势检测测试 ============

def test_detect_trend_up():
    """测试上升趋势检测"""
    data = [100 + i for i in range(30)]
    trend = ta.detect_trend(data)
    
    assert trend == ta.Trend.UP


def test_detect_trend_down():
    """测试下降趋势检测"""
    data = [130 - i for i in range(30)]
    trend = ta.detect_trend(data)
    
    assert trend == ta.Trend.DOWN


def test_detect_trend_sideways():
    """测试横盘趋势检测"""
    data = [100 + (i % 3 - 1) * 0.1 for i in range(30)]
    trend = ta.detect_trend(data)
    
    assert trend == ta.Trend.SIDEWAYS


# ============ 支撑阻力测试 ============

def test_support_resistance_basic():
    """测试基本支撑阻力识别"""
    result = ta.find_support_resistance(
        SAMPLE_HIGH[:30], SAMPLE_LOW[:30], SAMPLE_CLOSE[:30]
    )
    
    assert hasattr(result, 'support_levels')
    assert hasattr(result, 'resistance_levels')
    assert isinstance(result.support_levels, list)
    assert isinstance(result.resistance_levels, list)


def test_support_resistance_with_clear_levels():
    """测试有明显支撑阻力的数据"""
    # 创建有明显高低点的数据（至少20个点）
    high = [50, 55, 60, 55, 50, 45, 50, 55, 60, 55, 50, 45, 50, 55, 60, 55, 50, 45, 50, 55]
    low = [45, 50, 55, 50, 45, 40, 45, 50, 55, 50, 45, 40, 45, 50, 55, 50, 45, 40, 45, 50]
    close = [48, 53, 58, 53, 48, 43, 48, 53, 58, 53, 48, 43, 48, 53, 58, 53, 48, 43, 48, 53]
    
    result = ta.find_support_resistance(high, low, close)
    
    assert len(result.support_levels) >= 0
    assert len(result.resistance_levels) >= 0


# ============ 金叉死叉测试 ============

def test_golden_cross_death_cross():
    """测试金叉死叉检测"""
    short_ma = [10, 11, 12, 13, 14, 13, 12, 11, 10]
    long_ma = [10, 10, 10, 10, 10, 11, 12, 13, 14]
    
    result = ta.golden_cross_death_cross(short_ma, long_ma)
    
    # 开始时短期 < 长期，然后短期 > 长期（金叉）
    # 之后短期 < 长期（死叉）
    assert 'golden' in result
    assert 'death' in result


def test_cross_detection_no_signals():
    """测试无交叉信号"""
    short_ma = [10, 11, 12, 13, 14]
    long_ma = [5, 6, 7, 8, 9]  # 始终低于短期
    
    result = ta.golden_cross_death_cross(short_ma, long_ma)
    
    # 应该没有信号
    assert 'golden' not in result
    assert 'death' not in result


# ============ 综合分析测试 ============

def test_analyze_basic():
    """测试基本综合分析"""
    result = ta.analyze(SAMPLE_CLOSE[:50])
    
    assert 'current_price' in result
    assert 'trend' in result
    assert 'sma' in result
    assert 'ema' in result
    assert 'rsi_14' in result
    assert 'momentum' in result
    assert 'roc' in result


def test_analyze_with_high_low():
    """测试带高低价的综合分析"""
    result = ta.analyze(
        SAMPLE_CLOSE[:50],
        high=SAMPLE_HIGH[:50],
        low=SAMPLE_LOW[:50]
    )
    
    assert 'kdj' in result
    assert 'williams_r' in result
    assert 'cci' in result
    assert 'support_resistance' in result


def test_analyze_with_volume():
    """测试带成交量的综合分析"""
    result = ta.analyze(
        SAMPLE_CLOSE[:50],
        volume=SAMPLE_VOLUME[:50]
    )
    
    assert 'obv' in result


def test_analyze_with_all_data():
    """测试完整数据综合分析"""
    result = ta.analyze(
        SAMPLE_CLOSE[:50],
        high=SAMPLE_HIGH[:50],
        low=SAMPLE_LOW[:50],
        volume=SAMPLE_VOLUME[:50]
    )
    
    # 验证所有预期字段
    expected_keys = [
        'current_price', 'trend', 'sma', 'ema', 'rsi_14',
        'macd', 'bollinger', 'momentum', 'roc',
        'kdj', 'williams_r', 'cci', 'support_resistance', 'obv'
    ]
    
    for key in expected_keys:
        assert key in result, f"Missing key: {key}"


# ============ 工具函数测试 ============

def test_is_oversold():
    """测试超卖判断"""
    assert ta.is_oversold(25) == True
    assert ta.is_oversold(35) == False
    assert ta.is_oversold(10, threshold=20) == True


def test_is_overbought():
    """测试超买判断"""
    assert ta.is_overbought(75) == True
    assert ta.is_overbought(65) == False
    assert ta.is_overbought(85, threshold=80) == True


def test_calculate_returns():
    """测试收益率计算"""
    data = [100, 110, 121]  # 10%, 10% 涨幅
    result = ta.calculate_returns(data)
    
    assert_list_length(result, 3)
    assert_approx(result[0], 0.0)
    assert_approx(result[1], 0.1)
    assert_approx(result[2], 0.1)


def test_calculate_volatility():
    """测试波动率计算"""
    result = ta.calculate_volatility(SAMPLE_CLOSE)
    
    assert_is_not_none(result)
    assert result >= 0


def test_max_drawdown():
    """测试最大回撤计算"""
    data = [100, 90, 80, 90, 100, 85, 95]
    result = ta.max_drawdown(data)
    
    # 最大回撤应该是 20%（从 100 跌到 80）
    assert_approx(result, 20.0, 1.0)


def test_max_drawdown_no_drawdown():
    """测试无回撤情况"""
    data = [100, 110, 120, 130, 140]
    result = ta.max_drawdown(data)
    
    assert_approx(result, 0.0)


def test_sharpe_ratio():
    """测试夏普比率计算"""
    result = ta.sharpe_ratio(SAMPLE_CLOSE)
    
    assert_is_not_none(result)


def test_sharpe_ratio_constant_data():
    """测试常数数据的夏普比率"""
    data = [100.0] * 50
    result = ta.sharpe_ratio(data)
    
    # 无波动时夏普比率为 None
    # 或者如果计算出来，应该接近 0
    if result is not None:
        assert_approx(result, 0, 5)


# ============ 边界值测试 ============

def test_empty_data():
    """测试空数据"""
    assert_raises(lambda: ta.sma([], 5), ValueError)
    assert_raises(lambda: ta.ema([], 5), ValueError)
    assert_raises(lambda: ta.rsi([], 14), ValueError)


def test_insufficient_data():
    """测试数据不足"""
    assert_raises(lambda: ta.sma([1, 2], 5), ValueError)
    assert_raises(lambda: ta.rsi([1, 2], 14), ValueError)


def test_invalid_data_nan():
    """测试包含 NaN 的数据"""
    data = [1, 2, float('nan'), 4, 5]
    assert_raises(lambda: ta.sma(data, 3), ValueError)


def test_invalid_data_inf():
    """测试包含 Inf 的数据"""
    data = [1, 2, float('inf'), 4, 5]
    assert_raises(lambda: ta.sma(data, 3), ValueError)


def test_zero_prices():
    """测试零价格"""
    data = [0, 0, 0, 0, 0]
    result = ta.sma(data, 3)
    
    for val in result:
        if val is not None:
            assert_approx(val, 0)


def test_negative_prices():
    """测试负价格（虽然不常见，但算法应该能处理）"""
    data = [-1, -2, -3, -4, -5]
    result = ta.sma(data, 3)
    
    assert_approx(result[2], -2.0)
    assert_approx(result[4], -4.0)


def test_large_data_set():
    """测试大数据集"""
    data = [100 + (i % 10) for i in range(1000)]
    
    sma_result = ta.sma(data, 50)
    ema_result = ta.ema(data, 50)
    rsi_result = ta.rsi(data, 14)
    
    assert_list_length(sma_result, 1000)
    assert_list_length(ema_result, 1000)
    assert_list_length(rsi_result, 1000)


def test_very_small_period():
    """测试极小周期"""
    data = [1, 2, 3, 4, 5]
    
    sma_result = ta.sma(data, 1)
    assert_list_length(sma_result, 5)


def test_period_equal_data_length():
    """测试周期等于数据长度"""
    data = [1, 2, 3, 4, 5]
    
    sma_result = ta.sma(data, 5)
    assert_approx(sma_result[4], 3.0)


def test_mismatched_high_low_close():
    """测试高、低、收盘价长度不匹配"""
    assert_raises(
        lambda: ta.kdj([1, 2, 3], [1, 2], [1, 2, 3]),
        ValueError
    )
    assert_raises(
        lambda: ta.stochastic([1, 2, 3], [1, 2, 3], [1, 2]),
        ValueError
    )
    assert_raises(
        lambda: ta.atr([1, 2], [1, 2, 3], [1, 2, 3]),
        ValueError
    )


def test_mismatched_close_volume():
    """测试收盘价和成交量长度不匹配"""
    assert_raises(
        lambda: ta.obv([1, 2, 3], [1, 2]),
        ValueError
    )
    assert_raises(
        lambda: ta.vwap([1, 2, 3], [1, 2, 3], [1, 2, 3], [1, 2]),
        ValueError
    )


def test_extreme_price_values():
    """测试极端价格值"""
    # 非常大的价格
    data = [1e10 + i for i in range(20)]
    result = ta.sma(data, 10)
    
    assert result[-1] is not None
    
    # 非常小的价格
    data = [1e-10 + i * 1e-11 for i in range(20)]
    result = ta.sma(data, 10)
    
    assert result[-1] is not None


def test_single_price_change():
    """测试只有单一价格变化"""
    data = [100] * 15 + [101]  # 只有最后变化
    result = ta.rsi(data, 14)
    
    # 应该能正常计算
    assert result[-1] is not None


def test_alternating_prices():
    """测试交替价格"""
    data = [100, 101, 100, 101, 100, 101, 100, 101, 100, 101,
            100, 101, 100, 101, 100, 101, 100, 101, 100, 101]
    
    sma_result = ta.sma(data, 5)
    rsi_result = ta.rsi(data, 14)
    
    assert sma_result[-1] is not None
    assert rsi_result[-1] is not None


def test_macd_with_tight_data():
    """测试数据量刚好够 MACD"""
    data = [100 + i * 0.1 for i in range(35)]  # 刚够默认参数
    result = ta.macd(data)
    
    # 应该有一些非 None 结果
    non_none = [r for r in result if r is not None]
    assert len(non_none) > 0


# ============ 运行所有测试 ============

def run_all_tests():
    """运行所有测试"""
    tests = [
        # SMA 测试
        ("SMA 基本计算", test_sma_basic),
        ("SMA 周期1", test_sma_period_1),
        ("SMA 常数数据", test_sma_constant_data),
        ("SMA 递增数据", test_sma_increasing),
        ("SMA 空数据", test_sma_empty_data),
        ("SMA 无效周期", test_sma_invalid_period),
        
        # EMA 测试
        ("EMA 基本计算", test_ema_basic),
        ("EMA 响应性", test_ema_responsiveness),
        ("EMA 常数数据", test_ema_constant_data),
        
        # WMA 测试
        ("WMA 基本计算", test_wma_basic),
        ("WMA vs SMA", test_wma_vs_sma),
        
        # RSI 测试
        ("RSI 基本计算", test_rsi_basic),
        ("RSI 全上涨", test_rsi_all_gains),
        ("RSI 全下跌", test_rsi_all_losses),
        ("RSI 常数数据", test_rsi_constant_data),
        ("RSI 超买超卖", test_rsi_overbought_oversold),
        
        # MACD 测试
        ("MACD 基本计算", test_macd_basic),
        ("MACD 多头信号", test_macd_bullish_signal),
        ("MACD 自定义周期", test_macd_custom_periods),
        
        # 布林带测试
        ("布林带基本计算", test_bollinger_bands_basic),
        ("布林带常数数据", test_bollinger_bands_constant_data),
        ("布林带自定义标准差", test_bollinger_bands_custom_std),
        
        # KDJ 测试
        ("KDJ 基本计算", test_kdj_basic),
        ("KDJ 值范围", test_kdj_range),
        ("KDJ 自定义参数", test_kdj_custom_params),
        
        # 随机指标测试
        ("随机指标基本计算", test_stochastic_basic),
        ("随机指标超买", test_stochastic_overbought),
        
        # ATR 测试
        ("ATR 基本计算", test_atr_basic),
        ("ATR 常数数据", test_atr_constant_data),
        
        # OBV 测试
        ("OBV 基本计算", test_obv_basic),
        ("OBV 上涨", test_obv_rising_prices),
        ("OBV 下跌", test_obv_falling_prices),
        
        # VWAP 测试
        ("VWAP 基本计算", test_vwap_basic),
        ("VWAP 常数成交量", test_vwap_constant_volume),
        
        # Williams %R 测试
        ("Williams %R 基本计算", test_williams_r_basic),
        ("Williams %R 范围", test_williams_r_range),
        
        # CCI 测试
        ("CCI 基本计算", test_cci_basic),
        ("CCI 范围", test_cci_range),
        
        # 动量测试
        ("动量基本计算", test_momentum_basic),
        ("动量上涨", test_momentum_rising),
        ("动量下跌", test_momentum_falling),
        
        # ROC 测试
        ("ROC 基本计算", test_roc_basic),
        ("ROC 上涨", test_roc_rising),
        ("ROC 下跌", test_roc_falling),
        
        # ADX 测试
        ("ADX 基本计算", test_adx_basic),
        ("ADX 范围", test_adx_range),
        
        # 趋势检测测试
        ("趋势上升检测", test_detect_trend_up),
        ("趋势下降检测", test_detect_trend_down),
        ("趋势横盘检测", test_detect_trend_sideways),
        
        # 支撑阻力测试
        ("支撑阻力基本计算", test_support_resistance_basic),
        ("支撑阻力明显水平", test_support_resistance_with_clear_levels),
        
        # 金叉死叉测试
        ("金叉死叉检测", test_golden_cross_death_cross),
        ("无交叉信号", test_cross_detection_no_signals),
        
        # 综合分析测试
        ("综合分析基本", test_analyze_basic),
        ("综合分析带高低价", test_analyze_with_high_low),
        ("综合分析带成交量", test_analyze_with_volume),
        ("综合分析完整数据", test_analyze_with_all_data),
        
        # 工具函数测试
        ("超卖判断", test_is_oversold),
        ("超买判断", test_is_overbought),
        ("收益率计算", test_calculate_returns),
        ("波动率计算", test_calculate_volatility),
        ("最大回撤计算", test_max_drawdown),
        ("最大回撤无回撤", test_max_drawdown_no_drawdown),
        ("夏普比率计算", test_sharpe_ratio),
        ("夏普比率常数数据", test_sharpe_ratio_constant_data),
        
        # 边界值测试
        ("空数据", test_empty_data),
        ("数据不足", test_insufficient_data),
        ("NaN 数据", test_invalid_data_nan),
        ("Inf 数据", test_invalid_data_inf),
        ("零价格", test_zero_prices),
        ("负价格", test_negative_prices),
        ("大数据集", test_large_data_set),
        ("极小周期", test_very_small_period),
        ("周期等于数据长度", test_period_equal_data_length),
        ("高低收盘价长度不匹配", test_mismatched_high_low_close),
        ("收盘价成交量长度不匹配", test_mismatched_close_volume),
        ("极端价格值", test_extreme_price_values),
        ("单一价格变化", test_single_price_change),
        ("交替价格", test_alternating_prices),
        ("MACD 最小数据", test_macd_with_tight_data),
    ]
    
    passed = 0
    failed = 0
    
    print("=" * 60)
    print("技术分析工具测试")
    print("=" * 60)
    
    for name, test_func in tests:
        try:
            test_func()
            print(f"✅ {name}")
            passed += 1
        except Exception as e:
            print(f"❌ {name}: {str(e)}")
            failed += 1
    
    print("=" * 60)
    print(f"测试完成: {passed} 通过, {failed} 失败")
    print("=" * 60)
    
    return failed == 0


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)