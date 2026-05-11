"""
Ohm's Law Utilities 测试用例
"""

import unittest
import math
from mod import (
    OhmLawCalculator, OhmLawResult, ResistorCalculator,
    VoltageDivider, CurrentDivider, PowerCalculator,
    ResistorColorCode, calculate, series_resistance, parallel_resistance,
    Prefix
)


class TestOhmLawResult(unittest.TestCase):
    """测试 OhmLawResult 数据类"""
    
    def test_to_dict(self):
        result = OhmLawResult(12.0, 3.0, 4.0, 36.0)
        d = result.to_dict()
        self.assertEqual(d['voltage'], 12.0)
        self.assertEqual(d['current'], 3.0)
        self.assertEqual(d['resistance'], 4.0)
        self.assertEqual(d['power'], 36.0)
    
    def test_format_value_large(self):
        # 大数值应该使用适当前缀
        self.assertIn('k', OhmLawResult.format_value(12000, 'Ω'))
        self.assertIn('M', OhmLawResult.format_value(1200000, 'Ω'))
    
    def test_format_value_small(self):
        # 小数值应该使用适当前缀
        self.assertIn('m', OhmLawResult.format_value(0.001, 'A'))
        self.assertIn('μ', OhmLawResult.format_value(0.000001, 'A'))


class TestOhmLawCalculator(unittest.TestCase):
    """测试欧姆定律计算器"""
    
    def test_from_voltage_current(self):
        result = OhmLawCalculator.from_voltage_current(12.0, 3.0)
        self.assertEqual(result.voltage, 12.0)
        self.assertEqual(result.current, 3.0)
        self.assertEqual(result.resistance, 4.0)
        self.assertEqual(result.power, 36.0)
    
    def test_from_voltage_resistance(self):
        result = OhmLawCalculator.from_voltage_resistance(12.0, 4.0)
        self.assertEqual(result.voltage, 12.0)
        self.assertEqual(result.current, 3.0)
        self.assertEqual(result.resistance, 4.0)
        self.assertEqual(result.power, 36.0)
    
    def test_from_current_resistance(self):
        result = OhmLawCalculator.from_current_resistance(3.0, 4.0)
        self.assertEqual(result.voltage, 12.0)
        self.assertEqual(result.current, 3.0)
        self.assertEqual(result.resistance, 4.0)
        self.assertEqual(result.power, 36.0)
    
    def test_from_voltage_power(self):
        result = OhmLawCalculator.from_voltage_power(12.0, 36.0)
        self.assertEqual(result.voltage, 12.0)
        self.assertEqual(result.current, 3.0)
        self.assertEqual(result.resistance, 4.0)
        self.assertEqual(result.power, 36.0)
    
    def test_from_current_power(self):
        result = OhmLawCalculator.from_current_power(3.0, 36.0)
        self.assertEqual(result.voltage, 12.0)
        self.assertEqual(result.current, 3.0)
        self.assertEqual(result.resistance, 4.0)
        self.assertEqual(result.power, 36.0)
    
    def test_from_resistance_power(self):
        result = OhmLawCalculator.from_resistance_power(4.0, 36.0)
        self.assertAlmostEqual(result.voltage, 12.0, places=5)
        self.assertAlmostEqual(result.current, 3.0, places=5)
        self.assertEqual(result.resistance, 4.0)
        self.assertEqual(result.power, 36.0)
    
    def test_zero_current_error(self):
        with self.assertRaises(ValueError):
            OhmLawCalculator.from_voltage_current(12.0, 0.0)
    
    def test_zero_resistance_error(self):
        with self.assertRaises(ValueError):
            OhmLawCalculator.from_voltage_resistance(12.0, 0.0)


class TestResistorCalculator(unittest.TestCase):
    """测试电阻计算器"""
    
    def test_series(self):
        self.assertEqual(ResistorCalculator.series([100, 200, 300]), 600)
        self.assertEqual(ResistorCalculator.series([50]), 50)
    
    def test_series_empty_error(self):
        with self.assertRaises(ValueError):
            ResistorCalculator.series([])
    
    def test_series_negative_error(self):
        with self.assertRaises(ValueError):
            ResistorCalculator.series([100, -50, 200])
    
    def test_parallel_two_equal(self):
        # 两个相同电阻并联 = 一半阻值
        result = ResistorCalculator.parallel([100, 100])
        self.assertEqual(result, 50)
    
    def test_parallel_different(self):
        # 100Ω || 200Ω = 66.67Ω
        result = ResistorCalculator.parallel([100, 200])
        self.assertAlmostEqual(result, 66.666666, places=4)
    
    def test_parallel_three(self):
        # 100Ω || 100Ω || 100Ω = 33.33Ω
        result = ResistorCalculator.parallel([100, 100, 100])
        self.assertAlmostEqual(result, 33.333333, places=4)
    
    def test_parallel_empty_error(self):
        with self.assertRaises(ValueError):
            ResistorCalculator.parallel([])
    
    def test_parallel_zero_error(self):
        with self.assertRaises(ValueError):
            ResistorCalculator.parallel([100, 0, 200])
    
    def test_mixed(self):
        # 10 + (20||30) + 40 = 10 + 12 + 40 = 62
        config = [10, [20, 30], 40]
        result = ResistorCalculator.mixed(config)
        self.assertAlmostEqual(result, 62.0, places=4)
    
    def test_find_combination_series(self):
        available = [10, 22, 47, 100, 220, 470]
        combos = ResistorCalculator.find_combination(100, available, max_count=2, mode='series')
        # 应该找到一些组合
        self.assertTrue(len(combos) > 0)
        # 第一个应该最接近目标
        total = sum(combos[0][0])
        self.assertAlmostEqual(total, combos[0][1], places=5)


class TestVoltageDivider(unittest.TestCase):
    """测试分压器"""
    
    def test_calculate(self):
        # 12V 分压: R1=10k, R2=2k
        # Vout = 12 * 2000 / 12000 = 2V
        vout = VoltageDivider.calculate(12, 10000, 2000)
        self.assertEqual(vout, 2.0)
    
    def test_equal_resistors(self):
        # 相等电阻分压一半
        vout = VoltageDivider.calculate(10, 100, 100)
        self.assertEqual(vout, 5.0)
    
    def test_find_resistors(self):
        available = [1000, 2000, 4700, 10000, 22000]
        combos = VoltageDivider.find_resistors(12, 3, available)
        self.assertTrue(len(combos) > 0)
        # 应该接近3V
        actual = combos[0][2]
        self.assertTrue(abs(actual - 3) < 1)


class TestCurrentDivider(unittest.TestCase):
    """测试分流器"""
    
    def test_calculate(self):
        # 总电流1A，两个100Ω电阻并联
        # 每个支路应该分到0.5A
        i1, i2 = CurrentDivider.calculate(1.0, 100, 100)
        self.assertEqual(i1, 0.5)
        self.assertEqual(i2, 0.5)
    
    def test_different_resistors(self):
        # 总电流1A，100Ω和200Ω并联
        # 小电阻分到大电流
        i1, i2 = CurrentDivider.calculate(1.0, 100, 200)
        self.assertTrue(i1 > i2)  # R1小，I1大
        self.assertAlmostEqual(i1 + i2, 1.0, places=5)  # 总和为总电流


class TestPowerCalculator(unittest.TestCase):
    """测试功率计算器"""
    
    def test_ac_power_unity_pf(self):
        result = PowerCalculator.ac_power(220, 10, 1.0)
        self.assertEqual(result['apparent_power'], 2200)
        self.assertEqual(result['real_power'], 2200)
        self.assertAlmostEqual(result['reactive_power'], 0, places=5)
    
    def test_ac_power_lagging_pf(self):
        result = PowerCalculator.ac_power(220, 10, 0.8)
        self.assertEqual(result['apparent_power'], 2200)
        self.assertEqual(result['real_power'], 1760)
        self.assertAlmostEqual(result['reactive_power'], 1320, places=0)
    
    def test_energy_cost(self):
        result = PowerCalculator.energy_cost(1000, 10, 0.5)
        self.assertEqual(result['energy_kwh'], 10)
        self.assertEqual(result['cost'], 5.0)
    
    def test_battery_life(self):
        result = PowerCalculator.battery_life(3000, 500, 1.0)
        self.assertEqual(result['hours'], 6.0)
        self.assertEqual(result['minutes'], 360.0)
    
    def test_battery_life_with_efficiency(self):
        result = PowerCalculator.battery_life(3000, 500, 0.9)
        self.assertEqual(result['hours'], 5.4)
    
    def test_invalid_power_factor(self):
        with self.assertRaises(ValueError):
            PowerCalculator.ac_power(220, 10, 1.5)
    
    def test_zero_current_battery(self):
        with self.assertRaises(ValueError):
            PowerCalculator.battery_life(3000, 0, 1.0)


class TestResistorColorCode(unittest.TestCase):
    """测试电阻色环"""
    
    def test_decode_4band(self):
        # 红-紫-黄-金 = 270kΩ ±5%
        result = ResistorColorCode.decode_4band('red', 'violet', 'yellow', 'gold')
        self.assertEqual(result['resistance'], 270000)
        self.assertEqual(result['tolerance'], 5)
    
    def test_decode_4band_brown_black_red(self):
        # 棕-黑-红-金 = 1kΩ ±5%
        result = ResistorColorCode.decode_4band('brown', 'black', 'red', 'gold')
        self.assertEqual(result['resistance'], 1000)
        self.assertEqual(result['tolerance'], 5)
    
    def test_decode_5band(self):
        # 红-红-黑-橙-棕 = 220kΩ ±1%
        result = ResistorColorCode.decode_5band('red', 'red', 'black', 'orange', 'brown')
        self.assertEqual(result['resistance'], 220000)
        self.assertEqual(result['tolerance'], 1)
    
    def test_decode_range(self):
        # 100Ω ±5%
        result = ResistorColorCode.decode_4band('brown', 'black', 'brown', 'gold')
        self.assertEqual(result['range'][0], 95)  # 100 * 0.95
        self.assertEqual(result['range'][1], 105)  # 100 * 1.05
    
    def test_encode(self):
        colors = ResistorColorCode.encode(1000, 5)
        self.assertEqual(colors[0], 'brown')
        self.assertEqual(colors[1], 'black')
        self.assertEqual(colors[2], 'red')
        self.assertEqual(colors[3], 'gold')
    
    def test_encode_decode_roundtrip(self):
        # 测试编码后解码应该得到相同值
        original = 4700
        colors = ResistorColorCode.encode(original, 5)
        decoded = ResistorColorCode.decode_4band(*colors)
        self.assertEqual(decoded['resistance'], original)


class TestConvenienceFunctions(unittest.TestCase):
    """测试便捷函数"""
    
    def test_calculate_voltage_resistance(self):
        result = calculate(voltage=12, resistance=4)
        self.assertEqual(result.current, 3.0)
        self.assertEqual(result.power, 36.0)
    
    def test_calculate_current_power(self):
        result = calculate(current=3, power=36)
        self.assertEqual(result.voltage, 12.0)
        self.assertEqual(result.resistance, 4.0)
    
    def test_calculate_invalid_params(self):
        with self.assertRaises(ValueError):
            calculate(voltage=12)  # 只提供一个参数
        
        with self.assertRaises(ValueError):
            calculate(voltage=12, current=3, resistance=4)  # 三个参数
    
    def test_series_resistance(self):
        self.assertEqual(series_resistance(100, 200, 300), 600)
    
    def test_parallel_resistance(self):
        result = parallel_resistance(100, 100)
        self.assertEqual(result, 50)


if __name__ == '__main__':
    unittest.main(verbosity=2)