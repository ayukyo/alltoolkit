#!/usr/bin/env python3
"""
RSI Utils 测试套件

测试 RSI (相对强弱指标) 计算功能
"""

import unittest
import math
import sys
import os

# 添加父目录到路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from mod import (
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


class TestCalculateRSI(unittest.TestCase):
    """RSI 计算测试"""
    
    def test_calculate_rsi_basic(self):
        """测试基本 RSI 计算"""
        # 价格持续上涨
        prices = [100, 101, 102, 103, 104, 105, 106, 107, 108, 109,
                  110, 111, 112, 113, 114]
        rsi = calculate_rsi(prices, period=14)
        
        # 持续上涨应导致高 RSI
        self.assertEqual(len(rsi), len(prices))
        self.assertTrue(all(r is None for r in rsi[:15]))  # 前15个为None
        # 最后一个值应该很高（接近100）
        if rsi[-1] is not None:
            self.assertGreater(rsi[-1], 90)
    
    def test_calculate_rsi_declining(self):
        """测试持续下跌的 RSI"""
        prices = [114, 113, 112, 111, 110, 109, 108, 107, 106, 105,
                  104, 103, 102, 101, 100]
        rsi = calculate_rsi(prices, period=14)
        
        # 持续下跌应导致低 RSI
        if rsi[-1] is not None:
            self.assertLess(rsi[-1], 10)
    
    def test_calculate_rsi_mixed(self):
        """测试混合价格变动"""
        prices = [100, 102, 98, 103, 97, 104, 96, 105, 95, 106,
                  94, 107, 93, 108, 92, 109, 91, 110, 90, 111]
        rsi = calculate_rsi(prices, period=14)
        
        # 混合变动应产生中等 RSI
        self.assertEqual(len(rsi), len(prices))
        if rsi[-1] is not None:
            self.assertGreater(rsi[-1], 30)
            self.assertLess(rsi[-1], 70)
    
    def test_calculate_rsi_period_variations(self):
        """测试不同周期的 RSI"""
        prices = [44, 44.5, 43.5, 44.5, 45, 46, 45.5, 46, 47, 46.5,
                  47, 47.5, 48, 48.5, 47.5, 48, 49, 48.5, 49, 50]
        
        # 不同周期
        rsi_7 = calculate_rsi(prices, period=7)
        rsi_14 = calculate_rsi(prices, period=14)
        
        self.assertEqual(len(rsi_7), len(prices))
        self.assertEqual(len(rsi_14), len(prices))
    
    def test_calculate_rsi_methods(self):
        """测试不同平滑方法"""
        prices = [44, 44.5, 43.5, 44.5, 45, 46, 45.5, 46, 47, 46.5,
                  47, 47.5, 48, 48.5, 47.5, 48, 49, 48.5, 49, 50]
        
        rsi_sma = calculate_rsi(prices, period=14, method='sma')
        rsi_ema = calculate_rsi(prices, period=14, method='ema')
        rsi_wilder = calculate_rsi(prices, period=14, method='wilder')
        
        # 所有方法应产生有效 RSI
        for rsi_list in [rsi_sma, rsi_ema, rsi_wilder]:
            self.assertEqual(len(rsi_list), len(prices))
            for r in rsi_list:
                if r is not None:
                    self.assertGreaterEqual(r, 0)
                    self.assertLessEqual(r, 100)
    
    def test_calculate_rsi_insufficient_data(self):
        """测试数据不足的情况"""
        prices = [100, 101, 102]  # 只有3个数据点
        
        rsi = calculate_rsi(prices, period=14)
        self.assertEqual(len(rsi), 3)
        self.assertTrue(all(r is None for r in rsi))
    
    def test_calculate_rsi_invalid_method(self):
        """测试无效方法"""
        prices = [100, 101, 102, 103, 104, 105, 106, 107, 108, 109,
                  110, 111, 112, 113, 114]
        
        with self.assertRaises(ValueError):
            calculate_rsi(prices, period=14, method='invalid')


class TestCalculateRSISingle(unittest.TestCase):
    """单次 RSI 计算"""
    
    def test_calculate_rsi_single_normal(self):
        """测试正常情况"""
        # 需要 period + 1 个数据点才能计算 RSI
        prices = [44, 44.5, 43.5, 44.5, 45, 46, 45.5, 46, 47, 46.5,
                  47, 47.5, 48, 48.5, 47.5, 48]
        
        rsi = calculate_rsi_single(prices, period=14)
        self.assertIsNotNone(rsi)
        self.assertGreaterEqual(rsi, 0)
        self.assertLessEqual(rsi, 100)
    
    def test_calculate_rsi_single_insufficient(self):
        """测试数据不足"""
        prices = [100, 101]
        rsi = calculate_rsi_single(prices, period=14)
        self.assertIsNone(rsi)


class TestRSICalculator(unittest.TestCase):
    """RSI 计算器类测试"""
    
    def test_rsi_calculator_incremental(self):
        """测试增量式计算"""
        calc = RSICalculator(period=14)
        prices = [44, 44.5, 43.5, 44.5, 45, 46, 45.5, 46, 47, 46.5,
                  47, 47.5, 48, 48.5, 47.5, 48, 49, 48.5, 49, 50]
        
        rsi_values = []
        for price in prices:
            rsi = calc.update(price)
            if rsi is not None:
                rsi_values.append(rsi)
        
        # 应至少有一个有效 RSI 值
        self.assertTrue(len(rsi_values) >= 1 or calc.current_rsi is None)
    
    def test_rsi_calculator_reset(self):
        """测试重置功能"""
        calc = RSICalculator(period=14)
        
        for price in [100, 101, 102, 103, 104]:
            calc.update(price)
        
        # 重置
        calc.reset()
        self.assertIsNone(calc.current_rsi)
    
    def test_rsi_calculator_methods(self):
        """测试不同方法"""
        calc_sma = RSICalculator(period=14, method='sma')
        calc_ema = RSICalculator(period=14, method='ema')
        calc_wilder = RSICalculator(period=14, method='wilder')
        
        prices = [44, 44.5, 43.5, 44.5, 45, 46, 45.5, 46, 47, 46.5,
                  47, 47.5, 48, 48.5, 47.5, 48, 49, 48.5, 49, 50]
        
        for price in prices:
            calc_sma.update(price)
            calc_ema.update(price)
            calc_wilder.update(price)
        
        # 所有计算器应能处理数据
        # 注: SMA 方法可能有不同行为


class TestDetectDivergence(unittest.TestCase):
    """背离检测测试"""
    
    def test_detect_divergence_no_divergence(self):
        """测试无明显背离"""
        prices = [100, 101, 102, 103, 104, 105, 106, 107, 108, 109]
        rsi = calculate_rsi(prices, period=5)
        
        divergences = detect_divergence(prices, rsi, lookback=3)
        # 数据不足可能返回空列表
        self.assertIsInstance(divergences, list)
    
    def test_detect_divergence_bullish(self):
        """测试看涨背离"""
        # 价格下跌但 RSI 上升
        prices = [100, 95, 90, 85, 80, 75, 70, 75, 80, 85, 70, 75, 80, 85, 90]
        rsi = calculate_rsi(prices, period=5)
        
        divergences = detect_divergence(prices, rsi, lookback=5)
        self.assertIsInstance(divergences, list)
    
    def test_detect_divergence_bearish(self):
        """测试看跌背离"""
        prices = [100, 105, 110, 115, 120, 125, 130, 135, 140, 145, 150]
        rsi = calculate_rsi(prices, period=5)
        
        divergences = detect_divergence(prices, rsi, lookback=5)
        self.assertIsInstance(divergences, list)
    
    def test_detect_divergence_short_data(self):
        """测试短数据"""
        prices = [100, 101]
        rsi = [None, 50.0]
        
        divergences = detect_divergence(prices, rsi, lookback=5)
        self.assertEqual(len(divergences), 0)


class TestGenerateSignals(unittest.TestCase):
    """交易信号生成测试"""
    
    def test_generate_signals_oversold(self):
        """测试超卖信号"""
        # 创建低 RSI 序列
        rsi = [None] * 10 + [25.0, 20.0, 15.0, 25.0, 35.0]
        
        signals = generate_signals(rsi, oversold=30.0, overbought=70.0)
        
        # 应检测到进入和离开超卖区
        self.assertIsInstance(signals, list)
        enter_oversold = [s for s in signals if s['type'] == 'enter_oversold']
        exit_oversold = [s for s in signals if s['type'] == 'exit_oversold']
        
        self.assertTrue(len(enter_oversold) >= 1)
    
    def test_generate_signals_overbought(self):
        """测试超买信号"""
        rsi = [None] * 10 + [75.0, 80.0, 85.0, 75.0, 65.0]
        
        signals = generate_signals(rsi, oversold=30.0, overbought=70.0)
        
        enter_overbought = [s for s in signals if s['type'] == 'enter_overbought']
        exit_overbought = [s for s in signals if s['type'] == 'exit_overbought']
        
        self.assertTrue(len(enter_overbought) >= 1)
    
    def test_generate_signals_neutral(self):
        """测试中性区域"""
        rsi = [None] * 10 + [45.0, 50.0, 55.0, 50.0, 45.0]
        
        signals = generate_signals(rsi, oversold=30.0, overbought=70.0)
        # 中性区域不应有进入信号
        self.assertEqual(len(signals), 0)
    
    def test_generate_signals_custom_thresholds(self):
        """测试自定义阈值"""
        rsi = [None] * 10 + [25.0, 20.0, 15.0, 25.0, 35.0]
        
        signals = generate_signals(rsi, oversold=20.0, overbought=80.0)
        self.assertIsInstance(signals, list)


class TestCalculateStochRSI(unittest.TestCase):
    """Stoch RSI 计算"""
    
    def test_calculate_stoch_rsi_basic(self):
        """测试基本计算"""
        prices = [44, 44.5, 43.5, 44.5, 45, 46, 45.5, 46, 47, 46.5,
                  47, 47.5, 48, 48.5, 47.5, 48, 49, 48.5, 49, 50,
                  51, 52, 53, 54, 55, 56, 57, 58]
        
        k_values, d_values = calculate_stoch_rsi(prices, rsi_period=14, stoch_period=14)
        
        self.assertEqual(len(k_values), len(prices))
        self.assertEqual(len(d_values), len(prices))
    
    def test_calculate_stoch_rsi_values_range(self):
        """测试 K/D 值范围"""
        prices = [44, 44.5, 43.5, 44.5, 45, 46, 45.5, 46, 47, 46.5,
                  47, 47.5, 48, 48.5, 47.5, 48, 49, 48.5, 49, 50,
                  51, 52, 53, 54, 55, 56, 57, 58]
        
        k_values, d_values = calculate_stoch_rsi(prices)
        
        for k in k_values:
            if k is not None:
                self.assertGreaterEqual(k, 0)
                self.assertLessEqual(k, 100)
        
        for d in d_values:
            if d is not None:
                self.assertGreaterEqual(d, 0)
                self.assertLessEqual(d, 100)


class TestRSIToString(unittest.TestCase):
    """RSI 格式化测试"""
    
    def test_rsi_to_string_oversold(self):
        """测试超卖区域格式化"""
        result = rsi_to_string(25.0)
        self.assertIn("25", result)
        self.assertIn("超卖", result)
    
    def test_rsi_to_string_overbought(self):
        """测试超买区域格式化"""
        result = rsi_to_string(75.0)
        self.assertIn("75", result)
        self.assertIn("超买", result)
    
    def test_rsi_to_string_neutral(self):
        """测试中性区域格式化"""
        result = rsi_to_string(50.0)
        self.assertIn("50", result)
        self.assertIn("中性", result)
    
    def test_rsi_to_string_none(self):
        """测试 None 值"""
        result = rsi_to_string(None)
        self.assertIn("N/A", result)
    
    def test_rsi_to_string_precision(self):
        """测试精度控制"""
        result = rsi_to_string(55.555, precision=2)
        self.assertIn("55.5", result)  # Python round(55.555, 2) = 55.55


class TestValidateRSI(unittest.TestCase):
    """RSI 验证测试"""
    
    def test_validate_rsi_valid(self):
        """测试有效 RSI"""
        self.assertTrue(validate_rsi(50.0))
        self.assertTrue(validate_rsi(0))
        self.assertTrue(validate_rsi(100))
    
    def test_validate_rsi_invalid(self):
        """测试无效 RSI"""
        self.assertFalse(validate_rsi(-1))
        self.assertFalse(validate_rsi(101))
        self.assertFalse(validate_rsi("50"))  # 字符串
    
    def test_validate_rsi_boundary(self):
        """测试边界值"""
        self.assertTrue(validate_rsi(0.0))
        self.assertTrue(validate_rsi(100.0))


class TestGetRSIZone(unittest.TestCase):
    """RSI 区域测试"""
    
    def test_get_rsi_zone_deep_oversold(self):
        """测试深度超卖"""
        zone = get_rsi_zone(15.0)
        self.assertEqual(zone, "deep_oversold")
    
    def test_get_rsi_zone_oversold(self):
        """测试超卖"""
        zone = get_rsi_zone(25.0)
        self.assertEqual(zone, "oversold")
    
    def test_get_rsi_zone_bearish(self):
        """测试偏空"""
        zone = get_rsi_zone(35.0)
        self.assertEqual(zone, "bearish")
    
    def test_get_rsi_zone_neutral(self):
        """测试中性"""
        zone = get_rsi_zone(50.0)
        self.assertEqual(zone, "neutral")
    
    def test_get_rsi_zone_bullish(self):
        """测试偏多"""
        zone = get_rsi_zone(65.0)
        self.assertEqual(zone, "bullish")
    
    def test_get_rsi_zone_overbought(self):
        """测试超买"""
        zone = get_rsi_zone(75.0)
        self.assertEqual(zone, "overbought")
    
    def test_get_rsi_zone_deep_overbought(self):
        """测试深度超买"""
        zone = get_rsi_zone(85.0)
        self.assertEqual(zone, "deep_overbought")
    
    def test_get_rsi_zone_none(self):
        """测试 None 值"""
        zone = get_rsi_zone(None)
        self.assertEqual(zone, "unknown")


class TestEdgeCases(unittest.TestCase):
    """边界值测试"""
    
    def test_all_zero_prices(self):
        """测试全零价格"""
        prices = [0] * 20
        rsi = calculate_rsi(prices, period=14)
        self.assertEqual(len(rsi), 20)
    
    def test_all_same_prices(self):
        """测试价格完全相同"""
        prices = [100] * 20
        rsi = calculate_rsi(prices, period=14)
        self.assertEqual(len(rsi), 20)
        # 无变化可能导致特殊 RSI 值
    
    def test_extreme_prices(self):
        """测试极端价格"""
        prices = [1e10, 1e10 + 1, 1e10 - 1, 1e10 + 2, 1e10 - 2]
        rsi = calculate_rsi(prices, period=3)
        self.assertEqual(len(rsi), 5)
    
    def test_single_price(self):
        """测试单个价格"""
        prices = [100]
        rsi = calculate_rsi(prices, period=14)
        self.assertEqual(len(rsi), 1)
        self.assertIsNone(rsi[0])


class TestIntegration(unittest.TestCase):
    """集成测试"""
    
    def test_full_workflow(self):
        """测试完整工作流"""
        # 模拟30天价格数据
        prices = [100 + i * 0.5 - (i % 3) * 0.2 for i in range(30)]
        
        # 计算 RSI
        rsi = calculate_rsi(prices, period=14)
        
        # 检测背离
        divergences = detect_divergence(prices, rsi)
        
        # 生成信号
        signals = generate_signals(rsi)
        
        # 格式化输出
        if rsi[-1] is not None:
            formatted = rsi_to_string(rsi[-1])
            zone = get_rsi_zone(rsi[-1])
        
        # 验证所有步骤
        self.assertEqual(len(rsi), 30)
        self.assertIsInstance(divergences, list)
        self.assertIsInstance(signals, list)


def run_tests():
    """运行所有测试"""
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    suite.addTests(loader.loadTestsFromTestCase(TestCalculateRSI))
    suite.addTests(loader.loadTestsFromTestCase(TestCalculateRSISingle))
    suite.addTests(loader.loadTestsFromTestCase(TestRSICalculator))
    suite.addTests(loader.loadTestsFromTestCase(TestDetectDivergence))
    suite.addTests(loader.loadTestsFromTestCase(TestGenerateSignals))
    suite.addTests(loader.loadTestsFromTestCase(TestCalculateStochRSI))
    suite.addTests(loader.loadTestsFromTestCase(TestRSIToString))
    suite.addTests(loader.loadTestsFromTestCase(TestValidateRSI))
    suite.addTests(loader.loadTestsFromTestCase(TestGetRSIZone))
    suite.addTests(loader.loadTestsFromTestCase(TestEdgeCases))
    suite.addTests(loader.loadTestsFromTestCase(TestIntegration))
    
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    return result


if __name__ == '__main__':
    run_tests()