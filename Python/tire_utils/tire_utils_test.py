"""
Tire Utilities 测试模块

测试轮胎计算工具的各项功能
"""

import unittest
import sys
import os
from datetime import datetime

# Ensure the module directory is in sys.path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from mod import (
    TireSpec, TireDimensions,
    parse_tire_spec, calculate_dimensions, convert_pressure,
    parse_dot_code, get_tire_age, get_speed_rating_info, get_load_index_info,
    compare_tire_sizes, recommend_tire_pressure, evaluate_tire_wear,
    find_compatible_sizes, calculate_plus_sizing, tire_info,
    SPEED_RATINGS, LOAD_INDEX
)


class TestParseTireSpec(unittest.TestCase):
    """轮胎规格解析测试"""
    
    def test_standard_spec(self):
        """测试标准规格解析"""
        spec = parse_tire_spec("225/50R17")
        self.assertIsNotNone(spec)
        self.assertEqual(spec.width, 225)
        self.assertEqual(spec.aspect_ratio, 50)
        self.assertEqual(spec.construction, 'R')
        self.assertEqual(spec.rim_diameter, 17)
        self.assertIsNone(spec.load_index)
        self.assertIsNone(spec.speed_rating)
    
    def test_full_spec(self):
        """测试完整规格解析"""
        spec = parse_tire_spec("225/50R17 94V")
        self.assertIsNotNone(spec)
        self.assertEqual(spec.width, 225)
        self.assertEqual(spec.aspect_ratio, 50)
        self.assertEqual(spec.construction, 'R')
        self.assertEqual(spec.rim_diameter, 17)
        self.assertEqual(spec.load_index, 94)
        self.assertEqual(spec.speed_rating, 'V')
    
    def test_zr_spec(self):
        """测试ZR规格解析"""
        spec = parse_tire_spec("225/45ZR17")
        self.assertIsNotNone(spec)
        self.assertEqual(spec.aspect_ratio, 45)
        self.assertEqual(spec.construction, 'R')
    
    def test_with_prefix(self):
        """测试带前缀的规格"""
        spec = parse_tire_spec("P225/50R17")
        self.assertIsNotNone(spec)
        self.assertEqual(spec.width, 225)
        
        spec = parse_tire_spec("LT265/70R17")
        self.assertIsNotNone(spec)
        self.assertEqual(spec.width, 265)
    
    def test_bias_ply(self):
        """测试斜交胎规格"""
        spec = parse_tire_spec("225/50-17")
        # 斜交胎应该不被解析或返回不同的结构类型
        self.assertIsNotNone(spec)
    
    def test_string_representation(self):
        """测试字符串表示"""
        spec = parse_tire_spec("225/50R17 94V")
        self.assertEqual(str(spec), "225/50R17 94V")
        
        spec2 = parse_tire_spec("225/50R17")
        self.assertEqual(str(spec2), "225/50R17")
    
    def test_invalid_spec(self):
        """测试无效规格"""
        self.assertIsNone(parse_tire_spec("invalid"))
        self.assertIsNone(parse_tire_spec(""))
        self.assertIsNone(parse_tire_spec("225/50"))


class TestCalculateDimensions(unittest.TestCase):
    """轮胎尺寸计算测试"""
    
    def test_standard_calculation(self):
        """测试标准尺寸计算"""
        spec = TireSpec(width=225, aspect_ratio=50, construction='R', rim_diameter=17)
        dims = calculate_dimensions(spec)
        
        # 断面高度 = 225 * 0.5 = 112.5 mm
        self.assertAlmostEqual(dims.section_height_mm, 112.5, places=1)
        
        # 轮辋直径 = 17 * 25.4 = 431.8 mm
        self.assertAlmostEqual(dims.rim_diameter_mm, 431.8, places=1)
        
        # 外直径 = 431.8 + 2 * 112.5 = 656.8 mm
        self.assertAlmostEqual(dims.overall_diameter_mm, 656.8, places=1)
        
        # 周长
        expected_circumference = 656.8 * 3.14159265359
        self.assertAlmostEqual(dims.circumference_mm, expected_circumference, places=1)
    
    def test_high_profile_tire(self):
        """测试高扁平比轮胎"""
        spec = TireSpec(width=265, aspect_ratio=70, construction='R', rim_diameter=17)
        dims = calculate_dimensions(spec)
        
        # 断面高度 = 265 * 0.7 = 185.5 mm
        self.assertAlmostEqual(dims.section_height_mm, 185.5, places=1)
        
        # 外直径 = 431.8 + 2 * 185.5 = 802.8 mm
        self.assertAlmostEqual(dims.overall_diameter_mm, 802.8, places=1)
    
    def test_low_profile_tire(self):
        """测试低扁平比轮胎"""
        spec = TireSpec(width=275, aspect_ratio=35, construction='R', rim_diameter=20)
        dims = calculate_dimensions(spec)
        
        # 断面高度 = 275 * 0.35 = 96.25 mm
        self.assertAlmostEqual(dims.section_height_mm, 96.25, places=1)
    
    def test_revolutions(self):
        """测试转速计算"""
        spec = TireSpec(width=225, aspect_ratio=50, construction='R', rim_diameter=17)
        dims = calculate_dimensions(spec)
        
        # 每公里转速应该约为 500-550 转
        self.assertGreater(dims.revolutions_per_km, 450)
        self.assertLess(dims.revolutions_per_km, 600)


class TestConvertPressure(unittest.TestCase):
    """胎压转换测试"""
    
    def test_psi_to_kpa(self):
        """测试 PSI 到 kPa"""
        result = convert_pressure(32, 'psi', 'kpa')
        self.assertAlmostEqual(result, 220.6, places=1)
    
    def test_psi_to_bar(self):
        """测试 PSI 到 bar"""
        result = convert_pressure(32, 'psi', 'bar')
        self.assertAlmostEqual(result, 2.2, places=1)
    
    def test_kpa_to_psi(self):
        """测试 kPa 到 PSI"""
        result = convert_pressure(220, 'kpa', 'psi')
        self.assertAlmostEqual(result, 31.9, places=1)
    
    def test_bar_to_psi(self):
        """测试 bar 到 PSI"""
        result = convert_pressure(2.5, 'bar', 'psi')
        self.assertAlmostEqual(result, 36.3, places=1)
    
    def test_kg_cm2_conversion(self):
        """测试 kg/cm² 转换"""
        result = convert_pressure(2.3, 'kg_cm2', 'psi')
        self.assertAlmostEqual(result, 32.7, places=1)
    
    def test_invalid_unit(self):
        """测试无效单位"""
        with self.assertRaises(ValueError):
            convert_pressure(32, 'psi', 'invalid')
        with self.assertRaises(ValueError):
            convert_pressure(32, 'invalid', 'kpa')


class TestDotCode(unittest.TestCase):
    """DOT 编码解析测试"""
    
    def test_standard_dot(self):
        """测试标准 DOT 编码"""
        week, year = parse_dot_code("DOT U2LL LMLR 3519")
        self.assertEqual(week, 35)
        self.assertEqual(year, 2019)
    
    def test_short_dot(self):
        """测试短 DOT 编码"""
        week, year = parse_dot_code("3519")
        self.assertEqual(week, 35)
        self.assertEqual(year, 2019)
    
    def test_year_2000s(self):
        """测试 2000 年代"""
        week, year = parse_dot_code("0523")
        self.assertEqual(week, 5)
        self.assertEqual(year, 2023)
    
    def test_year_transition(self):
        """测试年份边界"""
        week, year = parse_dot_code("5200")
        self.assertEqual(week, 52)
        self.assertEqual(year, 2000)
    
    def test_invalid_dot(self):
        """测试无效 DOT"""
        self.assertIsNone(parse_dot_code("invalid"))
        self.assertIsNone(parse_dot_code("9999"))  # 周数超过范围


class TestTireAge(unittest.TestCase):
    """轮胎年龄计算测试"""
    
    def test_tire_age(self):
        """测试轮胎年龄计算"""
        age = get_tire_age("3519", datetime(2025, 1, 1))
        self.assertEqual(age, 5)
    
    def test_recent_tire(self):
        """测试新轮胎"""
        age = get_tire_age("2524", datetime(2025, 1, 1))
        self.assertEqual(age, 0)
    
    def test_old_tire(self):
        """测试旧轮胎"""
        age = get_tire_age("3505", datetime(2025, 1, 1))
        self.assertEqual(age, 19)
    
    def test_invalid_dot_for_age(self):
        """测试无效 DOT 的年龄计算"""
        self.assertIsNone(get_tire_age("invalid"))


class TestSpeedRating(unittest.TestCase):
    """速度等级测试"""
    
    def test_standard_ratings(self):
        """测试标准速度等级"""
        v_info = get_speed_rating_info('V')
        self.assertIsNotNone(v_info)
        self.assertEqual(v_info['max_speed_kmh'], 240)
        self.assertEqual(v_info['rating'], 'V')
    
    def test_h_rating(self):
        """测试 H 等级"""
        h_info = get_speed_rating_info('H')
        self.assertIsNotNone(h_info)
        self.assertEqual(h_info['max_speed_kmh'], 210)
    
    def test_zr_rating(self):
        """测试 ZR 等级"""
        zr_info = get_speed_rating_info('ZR')
        self.assertIsNotNone(zr_info)
        self.assertEqual(zr_info['max_speed_kmh'], 300)
    
    def test_invalid_rating(self):
        """测试无效速度等级"""
        self.assertIsNone(get_speed_rating_info('X'))


class TestLoadIndex(unittest.TestCase):
    """载重指数测试"""
    
    def test_standard_index(self):
        """测试标准载重指数"""
        info = get_load_index_info(94)
        self.assertIsNotNone(info)
        self.assertEqual(info['max_load_kg'], 670)
    
    def test_heavy_load(self):
        """测试高载重指数"""
        info = get_load_index_info(120)
        self.assertIsNotNone(info)
        self.assertEqual(info['max_load_kg'], 1400)
    
    def test_invalid_index(self):
        """测试无效载重指数"""
        self.assertIsNone(get_load_index_info(50))  # 太低
        self.assertIsNone(get_load_index_info(150))  # 太高


class TestCompareTireSizes(unittest.TestCase):
    """轮胎尺寸比较测试"""
    
    def test_similar_sizes(self):
        """测试相似尺寸"""
        spec1 = parse_tire_spec("225/50R17")
        spec2 = parse_tire_spec("235/50R17")
        
        diff = compare_tire_sizes(spec1, spec2)
        
        # 更宽的轮胎，直径也应该更大
        self.assertGreater(diff['width_diff_percent'], 0)
        self.assertLess(abs(diff['diameter_diff_percent']), 10)
    
    def test_plus_one_sizing(self):
        """测试 Plus One 改装"""
        spec1 = parse_tire_spec("225/50R17")
        spec2 = parse_tire_spec("225/45R18")
        
        diff = compare_tire_sizes(spec1, spec2)
        
        # Plus One 应该保持直径接近
        self.assertLess(abs(diff['diameter_diff_percent']), 5)


class TestRecommendTirePressure(unittest.TestCase):
    """胎压推荐测试"""
    
    def test_sedan_pressure(self):
        """测试轿车胎压推荐"""
        rec = recommend_tire_pressure(225, 'sedan')
        
        self.assertIn('front_psi', rec)
        self.assertIn('rear_psi', rec)
        self.assertIn('front_kpa', rec)
        self.assertIn('rear_kpa', rec)
        
        # 轿车胎压通常在 30-40 psi
        self.assertGreaterEqual(rec['front_psi'], 30)
        self.assertLessEqual(rec['front_psi'], 40)
    
    def test_suv_pressure(self):
        """测试 SUV 胎压推荐"""
        rec = recommend_tire_pressure(265, 'suv')
        
        # SUV 胎压通常更高
        self.assertGreaterEqual(rec['front_psi'], 33)
    
    def test_sports_pressure(self):
        """测试运动型车胎压推荐"""
        rec = recommend_tire_pressure(255, 'sports')
        
        # 运动型车胎压通常较高
        self.assertGreaterEqual(rec['front_psi'], 35)


class TestEvaluateTireWear(unittest.TestCase):
    """轮胎磨损评估测试"""
    
    def test_new_tire(self):
        """测试新轮胎"""
        result = evaluate_tire_wear(8.0)
        
        self.assertEqual(result['status'], 'good')
        self.assertEqual(result['wear_percent'], 0)
        self.assertEqual(result['remaining_percent'], 100)
        self.assertIn('良好', result['recommendation'])
    
    def test_half_worn(self):
        """测试半磨损轮胎"""
        result = evaluate_tire_wear(5.0)
        
        self.assertIn(result['status'], ['good', 'worn'])
        self.assertGreater(result['wear_percent'], 0)
        self.assertLess(result['remaining_percent'], 100)
    
    def test_critical_wear(self):
        """测试严重磨损"""
        result = evaluate_tire_wear(2.5)
        
        self.assertIn(result['status'], ['critical', 'worn'])
        self.assertGreater(result['wear_percent'], 50)
    
    def test_dangerous_wear(self):
        """测试危险磨损"""
        result = evaluate_tire_wear(1.5)
        
        self.assertEqual(result['status'], 'dangerous')
        self.assertIn('立即更换', result['recommendation'])
    
    def test_custom_minimum_depth(self):
        """测试自定义最小深度"""
        result = evaluate_tire_wear(2.0, minimum_safe_depth_mm=3.0)
        
        # 2.0mm 小于 3.0mm 最小安全深度
        self.assertEqual(result['status'], 'dangerous')


class TestFindCompatibleSizes(unittest.TestCase):
    """查找兼容尺寸测试"""
    
    def test_find_compatible(self):
        """测试查找兼容尺寸"""
        spec = parse_tire_spec("225/50R17")
        compatible = find_compatible_sizes(spec, tolerance_percent=2.0)
        
        # 应该找到一些兼容尺寸
        self.assertGreater(len(compatible), 0)
        
        # 所有兼容尺寸的直径应该接近原尺寸
        orig_dims = calculate_dimensions(spec)
        for c_spec in compatible[:5]:  # 检查前5个
            c_dims = calculate_dimensions(c_spec)
            diff_percent = abs(c_dims.overall_diameter_mm - orig_dims.overall_diameter_mm) / orig_dims.overall_diameter_mm * 100
            self.assertLessEqual(diff_percent, 2.0)


class TestCalculatePlusSizing(unittest.TestCase):
    """Plus Sizing 计算测试"""
    
    def test_plus_one(self):
        """测试 Plus One (17寸到18寸)"""
        spec = parse_tire_spec("225/50R17")
        options = calculate_plus_sizing(spec, 18)
        
        self.assertGreater(len(options), 0)
        
        # 所有选项应该保持相近直径
        orig_dims = calculate_dimensions(spec)
        for opt in options[:5]:
            opt_dims = calculate_dimensions(opt)
            diff_percent = abs(opt_dims.overall_diameter_mm - orig_dims.overall_diameter_mm) / orig_dims.overall_diameter_mm * 100
            self.assertLessEqual(diff_percent, 3.0)
    
    def test_plus_two(self):
        """测试 Plus Two (17寸到19寸)"""
        spec = parse_tire_spec("225/50R17")
        options = calculate_plus_sizing(spec, 19)
        
        self.assertGreater(len(options), 0)


class TestTireInfo(unittest.TestCase):
    """完整轮胎信息测试"""
    
    def test_full_info(self):
        """测试完整信息获取"""
        info = tire_info("225/50R17 94V")
        
        self.assertIn('spec', info)
        self.assertIn('width_mm', info)
        self.assertIn('dimensions', info)
        self.assertIn('speed_rating', info)
        self.assertIn('load_index', info)
        self.assertIn('recommended_pressure', info)
        
        self.assertEqual(info['width_mm'], 225)
        self.assertEqual(info['speed_rating']['max_speed_kmh'], 240)
        self.assertEqual(info['load_index']['max_load_kg'], 670)
    
    def test_info_without_rating(self):
        """测试无速度/载重等级的信息"""
        info = tire_info("225/50R17")
        
        self.assertIn('spec', info)
        self.assertNotIn('speed_rating', info)
        self.assertNotIn('load_index', info)
    
    def test_invalid_info(self):
        """测试无效规格"""
        info = tire_info("invalid")
        
        self.assertIn('error', info)


class TestEdgeCases(unittest.TestCase):
    """边界情况测试"""
    
    def test_very_low_profile(self):
        """测试极低扁平比"""
        spec = parse_tire_spec("335/25R20")
        self.assertIsNotNone(spec)
        self.assertEqual(spec.aspect_ratio, 25)
        
        dims = calculate_dimensions(spec)
        self.assertGreater(dims.overall_diameter_mm, 0)
    
    def test_very_high_profile(self):
        """测试极高扁平比"""
        spec = parse_tire_spec("195/80R15")
        self.assertIsNotNone(spec)
        self.assertEqual(spec.aspect_ratio, 80)
        
        dims = calculate_dimensions(spec)
        self.assertGreater(dims.overall_diameter_mm, 0)
    
    def test_small_tire(self):
        """测试小轮胎"""
        spec = parse_tire_spec("145/70R13")
        self.assertIsNotNone(spec)
        
        dims = calculate_dimensions(spec)
        self.assertGreater(dims.overall_diameter_mm, 400)
        self.assertLess(dims.overall_diameter_mm, 700)
    
    def test_large_tire(self):
        """测试大轮胎"""
        spec = parse_tire_spec("315/35R22")
        self.assertIsNotNone(spec)
        
        dims = calculate_dimensions(spec)
        self.assertGreater(dims.overall_diameter_mm, 700)


if __name__ == '__main__':
    unittest.main()