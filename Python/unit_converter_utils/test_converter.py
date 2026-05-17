"""
Unit Converter 测试文件
"""

import unittest
import math
from converter import UnitConverter, convert, convert_length, convert_weight
from converter import convert_temperature, convert_volume, convert_area
from converter import convert_time, convert_speed, convert_data, convert_pressure, convert_angle


class TestUnitConverter(unittest.TestCase):
    """UnitConverter 测试类"""
    
    def setUp(self):
        self.converter = UnitConverter(precision=6)
    
    # ============ 长度转换测试 ============
    def test_length_meter_to_km(self):
        result = self.converter.convert_length(1000, 'm', 'km')
        self.assertAlmostEqual(result, 1.0, places=5)
    
    def test_length_km_to_m(self):
        result = self.converter.convert_length(1, 'km', 'm')
        self.assertAlmostEqual(result, 1000.0, places=5)
    
    def test_length_mile_to_km(self):
        result = self.converter.convert_length(1, 'mi', 'km')
        self.assertAlmostEqual(result, 1.609344, places=5)
    
    def test_length_feet_to_meter(self):
        result = self.converter.convert_length(1, 'ft', 'm')
        self.assertAlmostEqual(result, 0.3048, places=5)
    
    def test_length_inch_to_cm(self):
        result = self.converter.convert_length(1, 'in', 'cm')
        self.assertAlmostEqual(result, 2.54, places=5)
    
    def test_length_nautical_mile(self):
        result = self.converter.convert_length(1, 'nmi', 'km')
        self.assertAlmostEqual(result, 1.852, places=5)
    
    def test_length_light_year(self):
        result = self.converter.convert_length(1, 'ly', 'km')
        self.assertTrue(result > 9e12)  # 光年约9.46万亿公里
    
    # ============ 重量转换测试 ============
    def test_weight_kg_to_g(self):
        result = self.converter.convert_weight(1, 'kg', 'g')
        self.assertAlmostEqual(result, 1000.0, places=5)
    
    def test_weight_lb_to_kg(self):
        result = self.converter.convert_weight(1, 'lb', 'kg')
        self.assertAlmostEqual(result, 0.45359237, places=5)
    
    def test_weight_oz_to_g(self):
        result = self.converter.convert_weight(1, 'oz', 'g')
        self.assertAlmostEqual(result, 28.349523125, places=4)
    
    def test_weight_ton_to_kg(self):
        result = self.converter.convert_weight(1, 't', 'kg')
        self.assertAlmostEqual(result, 1000.0, places=5)
    
    def test_weight_jin_to_kg(self):
        result = self.converter.convert_weight(1, 'jin', 'kg')
        self.assertAlmostEqual(result, 0.5, places=5)
    
    def test_weight_carat_to_g(self):
        result = self.converter.convert_weight(1, 'ct', 'g')
        self.assertAlmostEqual(result, 0.2, places=5)
    
    # ============ 温度转换测试 ============
    def test_temperature_c_to_f(self):
        result = self.converter.convert_temperature(0, 'C', 'F')
        self.assertAlmostEqual(result, 32.0, places=5)
    
    def test_temperature_f_to_c(self):
        result = self.converter.convert_temperature(32, 'F', 'C')
        self.assertAlmostEqual(result, 0.0, places=5)
    
    def test_temperature_c_to_k(self):
        result = self.converter.convert_temperature(0, 'C', 'K')
        self.assertAlmostEqual(result, 273.15, places=5)
    
    def test_temperature_k_to_c(self):
        result = self.converter.convert_temperature(273.15, 'K', 'C')
        self.assertAlmostEqual(result, 0.0, places=5)
    
    def test_temperature_f_to_k(self):
        result = self.converter.convert_temperature(32, 'F', 'K')
        self.assertAlmostEqual(result, 273.15, places=4)
    
    def test_temperature_boiling_point(self):
        result = self.converter.convert_temperature(100, 'C', 'F')
        self.assertAlmostEqual(result, 212.0, places=5)
    
    # ============ 体积转换测试 ============
    def test_volume_l_to_ml(self):
        result = self.converter.convert_volume(1, 'L', 'mL')
        self.assertAlmostEqual(result, 1000.0, places=5)
    
    def test_volume_gal_to_l(self):
        result = self.converter.convert_volume(1, 'gal', 'L')
        self.assertAlmostEqual(result, 3.785411784, places=4)
    
    def test_volume_m3_to_l(self):
        result = self.converter.convert_volume(1, 'm3', 'L')
        self.assertAlmostEqual(result, 1000.0, places=5)
    
    def test_volume_cup_to_ml(self):
        result = self.converter.convert_volume(1, 'cup', 'mL')
        self.assertAlmostEqual(result, 236.5882365, places=4)
    
    def test_volume_fl_oz_to_ml(self):
        result = self.converter.convert_volume(1, 'fl_oz', 'mL')
        self.assertAlmostEqual(result, 29.573529563, places=4)
    
    # ============ 面积转换测试 ============
    def test_area_km2_to_m2(self):
        result = self.converter.convert_area(1, 'km2', 'm2')
        self.assertAlmostEqual(result, 1000000.0, places=5)
    
    def test_area_hectare_to_m2(self):
        result = self.converter.convert_area(1, 'ha', 'm2')
        self.assertAlmostEqual(result, 10000.0, places=5)
    
    def test_area_acre_to_m2(self):
        result = self.converter.convert_area(1, 'acre', 'm2')
        self.assertAlmostEqual(result, 4046.8564224, places=4)
    
    def test_area_mu_to_m2(self):
        result = self.converter.convert_area(1, 'mu', 'm2')
        self.assertAlmostEqual(result, 666.6666667, places=4)
    
    # ============ 时间转换测试 ============
    def test_time_hour_to_min(self):
        result = self.converter.convert_time(1, 'h', 'min')
        self.assertAlmostEqual(result, 60.0, places=5)
    
    def test_time_day_to_hour(self):
        result = self.converter.convert_time(1, 'd', 'h')
        self.assertAlmostEqual(result, 24.0, places=5)
    
    def test_time_week_to_day(self):
        result = self.converter.convert_time(1, 'w', 'd')
        self.assertAlmostEqual(result, 7.0, places=5)
    
    def test_time_year_to_day(self):
        result = self.converter.convert_time(1, 'y', 'd')
        self.assertTrue(365 <= result <= 366)
    
    def test_time_ms_to_s(self):
        result = self.converter.convert_time(1000, 'ms', 's')
        self.assertAlmostEqual(result, 1.0, places=5)
    
    # ============ 速度转换测试 ============
    def test_speed_kmh_to_ms(self):
        result = self.converter.convert_speed(3.6, 'km/h', 'm/s')
        self.assertAlmostEqual(result, 1.0, places=5)
    
    def test_speed_mph_to_kmh(self):
        result = self.converter.convert_speed(1, 'mph', 'km/h')
        self.assertAlmostEqual(result, 1.609344, places=4)
    
    def test_speed_knot_to_kmh(self):
        result = self.converter.convert_speed(1, 'knot', 'km/h')
        self.assertAlmostEqual(result, 1.852, places=4)
    
    def test_speed_mach_to_ms(self):
        result = self.converter.convert_speed(1, 'mach', 'm/s')
        self.assertAlmostEqual(result, 340.29, places=1)
    
    # ============ 数据转换测试 ============
    def test_data_kb_to_mb(self):
        result = self.converter.convert_data(1024, 'KB', 'MB')
        self.assertAlmostEqual(result, 1.024, places=5)
    
    def test_data_gib_to_gib(self):
        result = self.converter.convert_data(1, 'GiB', 'MiB')
        self.assertAlmostEqual(result, 1024.0, places=5)
    
    def test_data_mb_to_gb(self):
        result = self.converter.convert_data(1000, 'MB', 'GB')
        self.assertAlmostEqual(result, 1.0, places=5)
    
    def test_data_bit_to_byte(self):
        result = self.converter.convert_data(8, 'bit', 'B')
        self.assertAlmostEqual(result, 1.0, places=5)
    
    def test_data_tb_to_pb(self):
        result = self.converter.convert_data(1000, 'TB', 'PB')
        self.assertAlmostEqual(result, 1.0, places=5)
    
    # ============ 压力转换测试 ============
    def test_pressure_kpa_to_pa(self):
        result = self.converter.convert_pressure(1, 'kPa', 'Pa')
        self.assertAlmostEqual(result, 1000.0, places=5)
    
    def test_pressure_bar_to_pa(self):
        result = self.converter.convert_pressure(1, 'bar', 'Pa')
        self.assertAlmostEqual(result, 100000.0, places=5)
    
    def test_pressure_atm_to_pa(self):
        result = self.converter.convert_pressure(1, 'atm', 'Pa')
        self.assertAlmostEqual(result, 101325.0, places=3)
    
    def test_pressure_psi_to_kpa(self):
        result = self.converter.convert_pressure(1, 'psi', 'kPa')
        self.assertAlmostEqual(result, 6.894757, places=4)
    
    # ============ 角度转换测试 ============
    def test_angle_deg_to_rad(self):
        result = self.converter.convert_angle(180, 'deg', 'rad')
        self.assertAlmostEqual(result, math.pi, places=5)
    
    def test_angle_rad_to_deg(self):
        result = self.converter.convert_angle(math.pi, 'rad', 'deg')
        self.assertAlmostEqual(result, 180.0, places=5)
    
    def test_angle_deg_to_grad(self):
        result = self.converter.convert_angle(90, 'deg', 'grad')
        self.assertAlmostEqual(result, 100.0, places=5)
    
    def test_angle_deg_to_arcmin(self):
        result = self.converter.convert_angle(1, 'deg', 'arcmin')
        self.assertAlmostEqual(result, 60.0, places=5)
    
    # ============ 自动检测类型测试 ============
    def test_auto_detect_length(self):
        result = self.converter.convert(1, 'km', 'm', 'auto')
        self.assertAlmostEqual(result, 1000.0, places=5)
    
    def test_auto_detect_weight(self):
        result = self.converter.convert(1, 'kg', 'g', 'auto')
        self.assertAlmostEqual(result, 1000.0, places=5)
    
    def test_auto_detect_temperature(self):
        result = self.converter.convert(0, 'C', 'F', 'auto')
        self.assertAlmostEqual(result, 32.0, places=5)
    
    def test_auto_detect_speed(self):
        result = self.converter.convert(100, 'km/h', 'm/s', 'auto')
        self.assertAlmostEqual(result, 27.777778, places=4)
    
    # ============ 错误处理测试 ============
    def test_invalid_unit(self):
        with self.assertRaises(ValueError):
            self.converter.convert(1, 'invalid', 'm')
    
    def test_mismatched_units(self):
        with self.assertRaises(ValueError):
            self.converter.convert(1, 'kg', 'm', 'auto')
    
    # ============ 便捷函数测试 ============
    def test_convenience_length(self):
        result = convert_length(1, 'km', 'm')
        self.assertAlmostEqual(result, 1000.0, places=5)
    
    def test_convenience_weight(self):
        result = convert_weight(1, 'lb', 'kg')
        self.assertAlmostEqual(result, 0.45359237, places=5)
    
    def test_convenience_temperature(self):
        result = convert_temperature(100, 'C', 'F')
        self.assertAlmostEqual(result, 212.0, places=5)
    
    def test_convenience_convert(self):
        result = convert(1000, 'm', 'km')
        self.assertAlmostEqual(result, 1.0, places=5)
    
    # ============ 批量转换测试 ============
    def test_batch_convert(self):
        conversions = [
            (1000, 'm', 'km'),
            (1, 'kg', 'g'),
            (0, 'C', 'F'),
        ]
        results = self.converter.batch_convert(conversions)
        self.assertAlmostEqual(results[0], 1.0, places=5)
        self.assertAlmostEqual(results[1], 1000.0, places=5)
        self.assertAlmostEqual(results[2], 32.0, places=5)
    
    # ============ 全量转换测试 ============
    def test_convert_all(self):
        results = self.converter.convert_all(1, 'km', 'length')
        self.assertIn('m', results)
        self.assertIn('mi', results)
        self.assertAlmostEqual(results['m'], 1000.0, places=4)
    
    # ============ 支持单位测试 ============
    def test_get_supported_units(self):
        units = self.converter.get_supported_units()
        self.assertIn('length', units)
        self.assertIn('m', units['length'])
        self.assertIn('temperature', units)
    
    def test_get_supported_units_single(self):
        units = self.converter.get_supported_units('weight')
        self.assertIn('weight', units)
        self.assertIn('kg', units['weight'])


class TestEdgeCases(unittest.TestCase):
    """边界情况测试"""
    
    def setUp(self):
        self.converter = UnitConverter(precision=6)
    
    def test_zero_value(self):
        result = self.converter.convert(0, 'm', 'km')
        self.assertEqual(result, 0.0)
    
    def test_negative_value(self):
        result = self.converter.convert(-100, 'C', 'F')
        self.assertAlmostEqual(result, -148.0, places=5)
    
    def test_very_large_value(self):
        result = self.converter.convert(1e15, 'm', 'km')
        self.assertAlmostEqual(result, 1e12, places=0)
    
    def test_very_small_value(self):
        # 使用更高精度的转换器测试极小值
        converter = UnitConverter(precision=15)
        result = converter.convert(1e-9, 'km', 'm')
        self.assertAlmostEqual(result, 1e-6, places=12)
    
    def test_case_insensitive_temperature(self):
        result1 = self.converter.convert(0, 'c', 'f')
        result2 = self.converter.convert(0, 'C', 'F')
        self.assertAlmostEqual(result1, result2, places=5)
    
    def test_precision_setting(self):
        converter = UnitConverter(precision=2)
        result = converter.convert(100, 'mi', 'km')
        self.assertAlmostEqual(result, 160.93, places=2)


if __name__ == '__main__':
    unittest.main()