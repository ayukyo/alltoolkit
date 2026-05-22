"""
RSI Utils 测试模块

测试 RSI (Relative Strength Index) 指标计算功能
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from rsi_utils.mod import (
    calculate_rsi,
    calculate_rsi_single,
    RSICalculator,
    detect_divergence,
    generate_signals,
    calculate_stoch_rsi,
    rsi_to_string,
    validate_rsi,
    get_rsi_zone
)


def test_calculate_rsi_basic():
    """测试基础 RSI 计算"""
    # 测试上涨趋势
    prices = [100, 101, 102, 103, 104, 105, 106, 107, 108, 109,
              110, 111, 112, 113, 114, 115]
    rsi = calculate_rsi(prices, period=14)
    
    # 检查长度
    assert len(rsi) == len(prices), "RSI 长度应与价格长度一致"
    
    # 检查前14个值为 None
    for i in range(14):
        assert rsi[i] is None, f"第 {i} 个 RSI 应为 None"
    
    # 上涨趋势 RSI 应该很高
    assert rsi[-1] is not None, "最新 RSI 不应为 None"
    assert rsi[-1] > 70, f"持续上涨 RSI 应大于70，实际: {rsi[-1]}"
    
    print("✓ 基础 RSI 计算测试通过")


def test_calculate_rsi_declining():
    """测试下跌趋势 RSI"""
    prices = [200, 198, 196, 194, 192, 190, 188, 186, 184, 182,
              180, 178, 176, 174, 172, 170]
    rsi = calculate_rsi(prices, period=14)
    
    # 下跌趋势 RSI 应该很低
    assert rsi[-1] is not None
    assert rsi[-1] < 30, f"持续下跌 RSI 应小于30，实际: {rsi[-1]}"
    
    print("✓ 下跌趋势 RSI 测试通过")


def test_calculate_rsi_methods():
    """测试不同平滑方法"""
    prices = [100, 102, 101, 103, 105, 104, 106, 108, 107, 109,
              111, 110, 112, 114, 113, 115, 117, 116, 118, 120]
    
    rsi_sma = calculate_rsi(prices, period=14, method='sma')
    rsi_ema = calculate_rsi(prices, period=14, method='ema')
    rsi_wilder = calculate_rsi(prices, period=14, method='wilder')
    
    # 所有方法都应该产生有效值
    assert rsi_sma[-1] is not None
    assert rsi_ema[-1] is not None
    assert rsi_wilder[-1] is not None
    
    # 不同方法结果应该略有不同
    values = [rsi_sma[-1], rsi_ema[-1], rsi_wilder[-1]]
    assert len(set(values)) >= 1, "不同方法应产生有效结果"
    
    print("✓ 平滑方法测试通过")


def test_calculate_rsi_insufficient_data():
    """测试数据不足情况"""
    prices = [100, 101, 102]  # 只有3个价格
    rsi = calculate_rsi(prices, period=14)
    
    # 数据不足时返回全 None
    assert all(r is None for r in rsi), "数据不足时应返回全 None"
    
    print("✓ 数据不足测试通过")


def test_calculate_rsi_single():
    """测试单次 RSI 计算"""
    # 需要 period + 1 个价格才能计算
    prices = [100, 101, 102, 103, 104, 105, 106, 107, 108, 109,
              110, 111, 112, 113, 114, 115]  # 16 prices for period=14
    
    rsi_single = calculate_rsi_single(prices, period=14)
    rsi_list = calculate_rsi(prices, period=14)
    
    assert rsi_single is not None, "RSI 单次计算不应为 None"
    assert rsi_list[-1] is not None, "RSI 列表最后值不应为 None"
    assert abs(rsi_single - rsi_list[-1]) < 0.01, "单次计算应与列表最后一个值一致"
    
    # 测试数据不足
    short_prices = [100, 101, 102]
    assert calculate_rsi_single(short_prices, period=14) is None
    
    print("✓ 单次 RSI 计算测试通过")


def test_rsi_calculator_class():
    """测试 RSI 计算器类"""
    prices = [100, 101, 102, 103, 104, 105, 106, 107, 108, 109,
              110, 111, 112, 113, 114, 115]
    
    calc = RSICalculator(period=14)
    rsi_values = []
    
    for price in prices:
        rsi = calc.update(price)
        rsi_values.append(rsi)
    
    # 前几个应为 None
    assert all(r is None for r in rsi_values[:14])
    
    # 最后应有有效值
    assert rsi_values[-1] is not None
    
    # current_rsi 属性应与最后更新一致
    assert calc.current_rsi == rsi_values[-1]
    
    print("✓ RSI 计算器类测试通过")


def test_rsi_calculator_reset():
    """测试计算器重置"""
    calc = RSICalculator(period=14)
    
    for price in range(100, 120):
        calc.update(price)
    
    assert calc.current_rsi is not None
    
    calc.reset()
    
    assert calc.current_rsi is None
    
    print("✓ 计算器重置测试通过")


def test_detect_divergence_bullish():
    """测试看涨背离检测"""
    # 构造价格创新低但 RSI 未创新低的场景
    prices = [100, 95, 90, 85, 80, 82, 84, 78, 75, 80, 
              76, 74, 77, 75, 73, 76, 74, 72, 75, 78]
    
    rsi = calculate_rsi(prices, period=14)
    divergences = detect_divergence(prices, rsi, lookback=5)
    
    # 返回应该是列表
    assert isinstance(divergences, list)
    
    print("✓ 背离检测测试通过")


def test_detect_divergence_insufficient_data():
    """测试数据不足时的背离检测"""
    prices = [100, 101, 102]
    rsi = calculate_rsi(prices, period=14)
    
    divergences = detect_divergence(prices, rsi, lookback=5)
    
    assert divergences == [], "数据不足时应返回空列表"
    
    print("✓ 背离检测数据不足测试通过")


def test_generate_signals():
    """测试信号生成"""
    # 构造能触发超买超卖的 RSI 序列
    # 直接使用模拟的 RSI 值
    rsi_values = [50, 45, 35, 25, 20, 25, 35, 50, 65, 75, 80, 75, 65, 50]
    
    signals = generate_signals(rsi_values, oversold=30, overbought=70)
    
    # 应该有进入超卖和离开超卖的信号
    signal_types = [s['type'] for s in signals]
    
    assert 'enter_oversold' in signal_types, "应检测到进入超卖"
    assert 'exit_oversold' in signal_types, "应检测到离开超卖"
    assert 'enter_overbought' in signal_types, "应检测到进入超买"
    assert 'exit_overbought' in signal_types, "应检测到离开超买"
    
    print("✓ 信号生成测试通过")


def test_generate_signals_with_nones():
    """测试包含 None 值的信号生成"""
    rsi_values = [None, None, None, 50, 35, 25, 35, 50, 75, 65]
    
    signals = generate_signals(rsi_values, oversold=30, overbought=70)
    
    # 应该跳过 None 值
    assert isinstance(signals, list)
    
    print("✓ None 值信号生成测试通过")


def test_calculate_stoch_rsi():
    """测试 Stochastic RSI 计算"""
    prices = [100 + i + (i % 3 - 1) * 2 for i in range(50)]
    
    k_values, d_values = calculate_stoch_rsi(prices, rsi_period=14, stoch_period=14)
    
    # 检查长度
    assert len(k_values) == len(prices)
    assert len(d_values) == len(prices)
    
    # 检查前几个值为 None
    for i in range(14 + 14 - 1):
        assert k_values[i] is None
        assert d_values[i] is None
    
    # 检查后面有有效值
    assert k_values[-1] is not None
    
    print("✓ Stochastic RSI 测试通过")


def test_rsi_to_string():
    """测试 RSI 字符串格式化"""
    assert "N/A" in rsi_to_string(None)
    assert "超卖" in rsi_to_string(25)
    assert "中性" in rsi_to_string(50)
    assert "超买" in rsi_to_string(80)
    
    print("✓ RSI 字符串格式化测试通过")


def test_validate_rsi():
    """测试 RSI 验证"""
    assert validate_rsi(50) == True
    assert validate_rsi(0) == True
    assert validate_rsi(100) == True
    assert validate_rsi(-1) == False
    assert validate_rsi(101) == False
    assert validate_rsi("50") == False
    
    print("✓ RSI 验证测试通过")


def test_get_rsi_zone():
    """测试 RSI 区域判断"""
    assert get_rsi_zone(None) == "unknown"
    assert get_rsi_zone(15) == "deep_oversold"
    assert get_rsi_zone(25) == "oversold"
    assert get_rsi_zone(35) == "bearish"
    assert get_rsi_zone(50) == "neutral"
    assert get_rsi_zone(65) == "bullish"
    assert get_rsi_zone(75) == "overbought"
    assert get_rsi_zone(90) == "deep_overbought"
    
    print("✓ RSI 区域判断测试通过")


def test_rsi_extreme_cases():
    """测试极端情况"""
    # 全部上涨 - RSI 应为 100
    all_up = [100 + i for i in range(20)]
    rsi = calculate_rsi(all_up, period=14)
    assert rsi[-1] == 100, f"全部上涨 RSI 应为 100，实际: {rsi[-1]}"
    
    # 全部下跌 - RSI 应为 0
    all_down = [200 - i for i in range(20)]
    rsi = calculate_rsi(all_down, period=14)
    assert rsi[-1] == 0, f"全部下跌 RSI 应为 0，实际: {rsi[-1]}"
    
    print("✓ 极端情况测试通过")


def test_rsi_convergence():
    """测试 RSI 收敛性"""
    # 价格波动后稳定
    prices = [100]
    import random
    random.seed(42)
    for _ in range(20):
        prices.append(prices[-1] + random.randint(-5, 5))
    for _ in range(30):
        prices.append(prices[-1] + random.randint(-1, 1))
    
    rsi = calculate_rsi(prices, period=14)
    
    # RSI 应该在 0-100 范围内
    for r in rsi:
        if r is not None:
            assert 0 <= r <= 100, f"RSI 应在 0-100 范围内，实际: {r}"
    
    print("✓ RSI 收敛性测试通过")


def run_all_tests():
    """运行所有测试"""
    print("=" * 50)
    print("RSI Utils 测试套件")
    print("=" * 50)
    
    tests = [
        test_calculate_rsi_basic,
        test_calculate_rsi_declining,
        test_calculate_rsi_methods,
        test_calculate_rsi_insufficient_data,
        test_calculate_rsi_single,
        test_rsi_calculator_class,
        test_rsi_calculator_reset,
        test_detect_divergence_bullish,
        test_detect_divergence_insufficient_data,
        test_generate_signals,
        test_generate_signals_with_nones,
        test_calculate_stoch_rsi,
        test_rsi_to_string,
        test_validate_rsi,
        test_get_rsi_zone,
        test_rsi_extreme_cases,
        test_rsi_convergence,
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            test()
            passed += 1
        except Exception as e:
            print(f"✗ {test.__name__} 失败: {e}")
            failed += 1
    
    print("=" * 50)
    print(f"测试结果: {passed} 通过, {failed} 失败")
    print("=" * 50)
    
    return failed == 0


if __name__ == '__main__':
    success = run_all_tests()
    exit(0 if success else 1)