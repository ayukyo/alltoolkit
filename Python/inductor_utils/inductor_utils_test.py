#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Inductor Utilities Test Module
"""

import unittest
import sys
import os
import math

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from inductor_utils.mod import (
    convert_inductance, format_inductance, parse_inductance_string,
    decode_smd_inductor, encode_smd_inductor,
    decode_inductor_colors,
    inductor_energy, rl_time_constant,
    inductive_reactance, inductive_impedance,
    inductor_current_rise, inductor_current_fall,
    series_inductance, parallel_inductance,
    q_factor, q_factor_bandwidth,
    resonant_frequency, resonant_inductance, resonant_capacitance,
    self_resonant_frequency,
    mutual_inductance, coupling_coefficient,
    coupled_inductance_series, coupled_inductance_parallel,
    air_core_inductance, toroid_inductance, turns_needed,
    get_inductor_series, find_nearest_standard,
    is_valid_smd_code, get_inductor_info,
    inductor_saturation_current,
    INDUCTANCE_UNITS, E_SERIES, COLOR_VALUES, COLOR_MULTIPLIERS, COLOR_TOLERANCES
)


class TestUnitConversion(unittest.TestCase):
    """测试单位转换"""
    
    def test_convert_inductance_basic(self):
        """测试基本单位转换"""
        self.assertEqual(convert_inductance(1, 'H', 'H'), 1.0)
        self.assertAlmostEqual(convert_inductance(1, 'mH', 'µH'), 1000.0)
        self.assertAlmostEqual(convert_inductance(1000, 'µH', 'mH'), 1.0)
        self.assertAlmostEqual(convert_inductance(1, 'µH', 'nH'), 1000.0)
        self.assertAlmostEqual(convert_inductance(1000, 'nH', 'µH'), 1.0)
        self.assertAlmostEqual(convert_inductance(1, 'nH', 'pH'), 1000.0)
    
    def test_convert_inductance_with_alternate_names(self):
        """测试备用单位名称"""
        self.assertEqual(convert_inductance(1, 'millihenry', 'mH'), 1.0)
        self.assertEqual(convert_inductance(1, 'microhenry', 'µH'), 1.0)
        self.assertEqual(convert_inductance(1, 'nanohenry', 'nH'), 1.0)
    
    def test_convert_inductance_invalid_unit(self):
        """测试无效单位"""
        with self.assertRaises(ValueError):
            convert_inductance(1, 'invalid', 'H')
        with self.assertRaises(ValueError):
            convert_inductance(1, 'H', 'invalid')
    
    def test_format_inductance(self):
        """测试格式化"""
        self.assertEqual(format_inductance(1), '1 H')
        self.assertEqual(format_inductance(1e-3), '1 mH')
        self.assertEqual(format_inductance(1e-6), '1 µH')
        self.assertEqual(format_inductance(1e-9), '1 nH')
        self.assertEqual(format_inductance(1e-12), '1 pH')
    
    def test_parse_inductance_string(self):
        """测试解析电感字符串"""
        self.assertAlmostEqual(parse_inductance_string('100nH'), 1e-7)
        self.assertAlmostEqual(parse_inductance_string('10µH'), 1e-5)
        self.assertAlmostEqual(parse_inductance_string('1mH'), 1e-3)
        self.assertAlmostEqual(parse_inductance_string('4R7'), 4.7e-6)


class TestSMDInductorCodes(unittest.TestCase):
    """测试 SMD 电感代码"""
    
    def test_decode_3digit(self):
        """测试 3 位数字代码解码"""
        result = decode_smd_inductor('103')
        self.assertAlmostEqual(result['inductance_henries'], 10e-6)
        self.assertEqual(result['code_type'], '3-digit-SMD')
        
        result = decode_smd_inductor('470')
        self.assertAlmostEqual(result['inductance_henries'], 47e-9)
    
    def test_decode_4digit(self):
        """测试 4 位数字代码解码"""
        result = decode_smd_inductor('1002')
        self.assertAlmostEqual(result['inductance_henries'], 10e-6)
        self.assertEqual(result['code_type'], '4-digit-SMD')
    
    def test_decode_r_notation(self):
        """测试 R 标记代码解码"""
        result = decode_smd_inductor('4R7')
        self.assertAlmostEqual(result['inductance_henries'], 4.7e-6)
        self.assertEqual(result['code_type'], 'R-notation')
        
        result = decode_smd_inductor('R47')
        self.assertAlmostEqual(result['inductance_henries'], 0.47e-6)
    
    def test_decode_unit_notation(self):
        """测试带单位的代码解码"""
        result = decode_smd_inductor('100n')
        self.assertAlmostEqual(result['inductance_henries'], 100e-9)
        self.assertEqual(result['code_type'], 'unit_notation')
    
    def test_encode_3digit(self):
        """测试 3 位数字代码编码"""
        code = encode_smd_inductor(10e-6)
        self.assertEqual(code, '103')
        
        # 1µH 在 nH 单位下是 1000nH，需要特殊处理
        code = encode_smd_inductor(1e-6)
        # 对于小于10nH的值使用R notation，否则返回3位代码
        self.assertTrue(code in ['1001', '100', '1R0'] or code.startswith('1R'))
    
    def test_encode_r_notation(self):
        """测试 R 标记代码编码"""
        code = encode_smd_inductor(4.7e-6, 'R-notation')
        self.assertEqual(code, '4R7')
    
    def test_invalid_code(self):
        """测试无效代码"""
        with self.assertRaises(ValueError):
            decode_smd_inductor('invalid')


class TestInductorColorCodes(unittest.TestCase):
    """测试电感色码"""
    
    def test_decode_4band(self):
        """测试 4 色环解码"""
        # brown-black-red-gold = 10 * 100 µH = 1000 µH = 1 mH
        result = decode_inductor_colors(['brown', 'black', 'red', 'gold'])
        self.assertAlmostEqual(result['inductance_henries'], 1e-3)
        self.assertEqual(result['tolerance_percent'], 5.0)
    
    def test_decode_5band(self):
        """测试 5 色环解码"""
        # brown-black-black-red-gold = 100 * 100 µH
        result = decode_inductor_colors(['brown', 'black', 'black', 'red', 'gold'])
        self.assertAlmostEqual(result['inductance_henries'], 10e-3)
        self.assertEqual(result['tolerance_percent'], 5.0)
    
    def test_invalid_colors(self):
        """测试无效颜色"""
        with self.assertRaises(ValueError):
            decode_inductor_colors(['invalid', 'black', 'red'])
    
    def test_insufficient_colors(self):
        """测试颜色不足"""
        with self.assertRaises(ValueError):
            decode_inductor_colors(['brown', 'black'])


class TestElectricalCalculations(unittest.TestCase):
    """测试电气计算"""
    
    def test_inductor_energy(self):
        """测试电感储能"""
        result = inductor_energy(1e-3, 10)  # 1mH, 10A
        self.assertAlmostEqual(result['energy_joules'], 0.05)
        self.assertAlmostEqual(result['energy_watthours'], 0.05 / 3600)
    
    def test_rl_time_constant(self):
        """测试 RL 时间常数"""
        result = rl_time_constant(1000, 1e-3)  # 1kΩ, 1mH
        self.assertAlmostEqual(result['tau_seconds'], 1e-6)
        self.assertAlmostEqual(result['tau_us'], 1.0)
        self.assertAlmostEqual(result['five_tau_seconds'], 5e-6)
    
    def test_inductive_reactance(self):
        """测试感抗"""
        result = inductive_reactance(1e-3, 1000)  # 1mH at 1kHz
        expected = 2 * math.pi * 1000 * 1e-3
        self.assertAlmostEqual(result['reactance_ohms'], expected)
    
    def test_inductive_impedance(self):
        """测试复阻抗"""
        z = inductive_impedance(1e-3, 1000, 0.1)  # 1mH at 1kHz, 0.1Ω DCR
        self.assertAlmostEqual(z.real, 0.1)
        self.assertAlmostEqual(z.imag, 2 * math.pi * 1000 * 1e-3)
    
    def test_current_rise(self):
        """测试电流上升"""
        i = inductor_current_rise(1e-3, 1000, 0, 0.01, 1e-6)
        # 1τ 后应达到约 63.2%
        self.assertAlmostEqual(i, 0.01 * (1 - math.exp(-1)), places=4)
    
    def test_current_fall(self):
        """测试电流下降"""
        i = inductor_current_fall(1e-3, 1000, 0.01, 1e-6)
        # 1τ 后应降至约 36.8%
        self.assertAlmostEqual(i, 0.01 * math.exp(-1), places=4)


class TestSeriesParallel(unittest.TestCase):
    """测试串联并联计算"""
    
    def test_series_inductance(self):
        """测试串联"""
        result = series_inductance([1e-3, 2e-3, 3e-3])
        self.assertAlmostEqual(result, 6e-3)
    
    def test_parallel_inductance(self):
        """测试并联"""
        result = parallel_inductance([1e-3, 1e-3])
        self.assertAlmostEqual(result, 0.5e-3)
        
        result = parallel_inductance([1e-3, 2e-3])
        expected = 1 / (1/1e-3 + 1/2e-3)
        self.assertAlmostEqual(result, expected)
    
    def test_empty_lists(self):
        """测试空列表"""
        self.assertEqual(series_inductance([]), 0)
        self.assertEqual(parallel_inductance([]), 0)


class TestQFactor(unittest.TestCase):
    """测试 Q 值计算"""
    
    def test_q_factor(self):
        """测试 Q 值"""
        result = q_factor(1e-3, 1e6, 0.1)  # 1mH, 1MHz, 0.1Ω
        expected = (2 * math.pi * 1e6 * 1e-3) / 0.1
        self.assertAlmostEqual(result['q_factor'], expected)
    
    def test_q_factor_bandwidth(self):
        """测试带宽计算"""
        result = q_factor_bandwidth(100, 1e6)
        self.assertEqual(result['bandwidth_hz'], 10000)
        self.assertEqual(result['lower_cutoff_hz'], 995000)
        self.assertEqual(result['upper_cutoff_hz'], 1005000)


class TestResonantFrequency(unittest.TestCase):
    """测试谐振频率"""
    
    def test_resonant_frequency(self):
        """测试谐振频率计算"""
        freq = resonant_frequency(1e-3, 1e-6)  # 1mH, 1µF
        expected = 1 / (2 * math.pi * math.sqrt(1e-3 * 1e-6))
        self.assertAlmostEqual(freq, expected)
    
    def test_resonant_inductance(self):
        """测试谐振电感"""
        L = resonant_inductance(1000, 1e-6)  # 1kHz, 1µF
        expected = 1 / (4 * math.pi ** 2 * 1000 ** 2 * 1e-6)
        self.assertAlmostEqual(L, expected)
    
    def test_resonant_capacitance(self):
        """测试谐振电容"""
        C = resonant_capacitance(1000, 1e-3)  # 1kHz, 1mH
        expected = 1 / (4 * math.pi ** 2 * 1000 ** 2 * 1e-3)
        self.assertAlmostEqual(C, expected)
    
    def test_self_resonant_frequency(self):
        """测试自谐振频率"""
        f = self_resonant_frequency(1e-3, 10e-12)  # 1mH, 10pF parasitic
        expected = 1 / (2 * math.pi * math.sqrt(1e-3 * 10e-12))
        self.assertAlmostEqual(f, expected)


class TestMutualInductance(unittest.TestCase):
    """测试互感"""
    
    def test_mutual_inductance(self):
        """测试互感计算"""
        M = mutual_inductance(1e-3, 1e-3, 0.9)
        expected = 0.9 * math.sqrt(1e-3 * 1e-3)
        self.assertAlmostEqual(M, expected)
    
    def test_coupling_coefficient(self):
        """测试耦合系数"""
        k = coupling_coefficient(1e-3, 1e-3, 0.9e-3)
        self.assertAlmostEqual(k, 0.9)
    
    def test_coupled_series_additive(self):
        """测试串联耦合（加性）"""
        L = coupled_inductance_series(1e-3, 1e-3, 0.5e-3, 'additive')
        expected = 1e-3 + 1e-3 + 2 * 0.5e-3
        self.assertAlmostEqual(L, expected)
    
    def test_coupled_series_subtractive(self):
        """测试串联耦合（减性）"""
        L = coupled_inductance_series(1e-3, 1e-3, 0.5e-3, 'subtractive')
        expected = 1e-3 + 1e-3 - 2 * 0.5e-3
        self.assertAlmostEqual(L, expected)
    
    def test_coupled_parallel(self):
        """测试并联耦合"""
        L = coupled_inductance_parallel(1e-3, 1e-3, 0.5e-3)
        # (L1*L2 - M^2) / (L1 + L2 - 2M)
        expected = (1e-3 * 1e-3 - 0.5e-3 ** 2) / (1e-3 + 1e-3 - 2 * 0.5e-3)
        self.assertAlmostEqual(L, expected)


class TestPhysicalInductors(unittest.TestCase):
    """测试物理电感器计算"""
    
    def test_air_core_inductance(self):
        """测试空芯电感"""
        result = air_core_inductance(0.01, 0.05, 100)  # 1cm radius, 5cm length, 100 turns
        self.assertIn('inductance_henries', result)
        self.assertIn('inductance_str', result)
        self.assertTrue(result['inductance_henries'] > 0)
    
    def test_toroid_inductance(self):
        """测试环形电感"""
        result = toroid_inductance(2000, 1e-4, 0.05, 50)
        self.assertIn('inductance_henries', result)
        self.assertTrue(result['inductance_henries'] > 0)
    
    def test_turns_needed(self):
        """测试所需匝数"""
        turns = turns_needed(1e-3, 2000, 1e-4, 0.05)
        self.assertTrue(turns >= 1)
        self.assertIsInstance(turns, int)


class TestESeries(unittest.TestCase):
    """测试 E 系列"""
    
    def test_get_inductor_series(self):
        """测试获取 E 系列"""
        e3 = get_inductor_series('E3')
        self.assertEqual(e3, [10, 22, 47])
        
        e6 = get_inductor_series('E6')
        self.assertEqual(e6, [10, 15, 22, 33, 47, 68])
        
        e12 = get_inductor_series('E12')
        self.assertEqual(len(e12), 12)
    
    def test_invalid_series(self):
        """测试无效系列"""
        with self.assertRaises(ValueError):
            get_inductor_series('E100')
    
    def test_find_nearest_standard(self):
        """测试查找最近标准值"""
        result = find_nearest_standard(8.5e-6, 'E12')
        self.assertIn('nearest', result)
        self.assertIn('nearest_str', result)
        self.assertIn('error_percent', result)


class TestUtilityFunctions(unittest.TestCase):
    """测试工具函数"""
    
    def test_is_valid_smd_code(self):
        """测试代码有效性验证"""
        self.assertTrue(is_valid_smd_code('103'))
        self.assertTrue(is_valid_smd_code('4R7'))
        self.assertTrue(is_valid_smd_code('100n'))
        self.assertFalse(is_valid_smd_code('invalid'))
    
    def test_get_inductor_info(self):
        """测试获取电感信息"""
        info = get_inductor_info(1e-6)
        self.assertEqual(info['henries'], 1e-6)
        self.assertEqual(info['microhenries'], 1)
        self.assertIn('formatted', info)
    
    def test_saturation_current(self):
        """测试饱和电流"""
        i_sat = inductor_saturation_current(
            1e-3, 1e-4, 0.05, 50, 0.3  # 1mH, core params, 0.3T saturation
        )
        self.assertTrue(i_sat > 0)


if __name__ == '__main__':
    unittest.main(verbosity=2)