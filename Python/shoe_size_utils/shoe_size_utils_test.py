"""
鞋码转换工具测试模块
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import unittest
from shoe_size_utils.mod import (
    ShoeSizeConverter,
    ShoeSize,
    SizeSystem,
    Gender,
    convert_shoe_size,
    get_all_sizes,
    get_foot_length_info,
    recommend_shoe_size,
    validate_shoe_size,
    compare_sizes,
    find_closest_size,
    COMMON_SIZE_CHART
)


class TestShoeSizeConverter(unittest.TestCase):
    """鞋码转换器测试"""
    
    def test_cm_to_eu(self):
        """厘米转欧洲码"""
        # 26.5cm ≈ EU 42
        result = ShoeSizeConverter.cm_to_eu(26.5)
        self.assertAlmostEqual(result, 42.0, delta=1.0)  # 放宽容差
        
        # 25cm ≈ EU 39.5
        result = ShoeSizeConverter.cm_to_eu(25)
        self.assertAlmostEqual(result, 39.5, delta=1.0)
    
    def test_eu_to_cm(self):
        """欧洲码转厘米"""
        # EU 42 ≈ 26.5cm
        result = ShoeSizeConverter.eu_to_cm(42)
        self.assertAlmostEqual(result, 26.5, delta=0.5)
        
        # EU 39 ≈ 25cm
        result = ShoeSizeConverter.eu_to_cm(39)
        self.assertAlmostEqual(result, 25.0, delta=0.5)
    
    def test_cm_to_us_men(self):
        """厘米转美国男码"""
        # 26.5cm ≈ US Men 8.5
        result = ShoeSizeConverter.cm_to_us_men(26.5)
        self.assertAlmostEqual(result, 8.5, delta=0.5)
    
    def test_us_men_to_cm(self):
        """美国男码转厘米"""
        result = ShoeSizeConverter.us_men_to_cm(8.5)
        self.assertAlmostEqual(result, 26.5, delta=0.5)
    
    def test_cm_to_us_women(self):
        """厘米转美国女码"""
        # 女码比男码大约1码
        result = ShoeSizeConverter.cm_to_us_women(26.5)
        self.assertAlmostEqual(result, 10.0, delta=0.5)
    
    def test_cm_to_uk(self):
        """厘米转英国码"""
        result = ShoeSizeConverter.cm_to_uk(26.5)
        self.assertAlmostEqual(result, 8.0, delta=0.5)
    
    def test_uk_to_cm(self):
        """英国码转厘米"""
        result = ShoeSizeConverter.uk_to_cm(8)
        self.assertAlmostEqual(result, 26.5, delta=0.5)
    
    def test_cm_to_cn(self):
        """厘米转中国码"""
        # 26.5cm = 265mm
        result = ShoeSizeConverter.cm_to_cn(26.5)
        self.assertEqual(result, 265)
    
    def test_cn_to_cm(self):
        """中国码转厘米"""
        result = ShoeSizeConverter.cn_to_cm(265)
        self.assertEqual(result, 26.5)
    
    def test_convert_eu_to_us_men(self):
        """欧洲码转美国男码"""
        result = ShoeSizeConverter.convert(42, SizeSystem.EU, SizeSystem.US_MEN)
        self.assertAlmostEqual(result, 8.5, delta=0.5)
    
    def test_convert_us_men_to_uk(self):
        """美国男码转英国码"""
        result = ShoeSizeConverter.convert(8.5, SizeSystem.US_MEN, SizeSystem.UK)
        self.assertAlmostEqual(result, 8.0, delta=0.5)
    
    def test_convert_all(self):
        """转换所有鞋码系统"""
        result = ShoeSizeConverter.convert_all(42, SizeSystem.EU)
        
        # 验证所有字段存在
        self.assertIn("cm", result)
        self.assertIn("jp", result)
        self.assertIn("eu", result)
        self.assertIn("us_men", result)
        self.assertIn("us_women", result)
        self.assertIn("uk", result)
        self.assertIn("cn", result)
        
        # 验证EU码保留
        self.assertEqual(result["eu"], 42.0)
        
        # 验证CM和JP相同
        self.assertEqual(result["cm"], result["jp"])
        
        # 验证中国码是整数
        self.assertIsInstance(result["cn"], int)
    
    def test_get_size_info(self):
        """获取鞋码详细信息"""
        info = ShoeSizeConverter.get_size_info(42, SizeSystem.EU)
        
        self.assertIn("脚长", info)
        self.assertIn("类型", info)
        self.assertIn("所有码", info)
        self.assertIn("购鞋建议", info)


class TestConvenienceFunctions(unittest.TestCase):
    """便捷函数测试"""
    
    def test_convert_shoe_size(self):
        """便捷转换函数"""
        result = convert_shoe_size(42, "EU", "US_MEN")
        self.assertAlmostEqual(result, 8.5, delta=0.5)
        
        result = convert_shoe_size(42, "EU", "UK")
        self.assertAlmostEqual(result, 8.0, delta=0.5)
    
    def test_get_all_sizes(self):
        """获取所有尺码"""
        result = get_all_sizes(42, "EU")
        self.assertIn("cm", result)
        self.assertEqual(result["eu"], 42.0)
    
    def test_get_foot_length_info(self):
        """根据脚长获取信息"""
        result = get_foot_length_info(26.5)
        self.assertIn("eu", result)
        self.assertIn("us_men", result)
        self.assertIn("uk", result)
    
    def test_recommend_shoe_size(self):
        """推荐鞋码"""
        # 标准鞋
        rec = recommend_shoe_size(26.5, "normal")
        self.assertIn("推荐EU码", rec)
        self.assertIn("调整原因", rec)
        
        # 跑步鞋 - 应该大半码
        rec_running = recommend_shoe_size(26.5, "running")
        self.assertEqual(rec_running["推荐EU码"], rec["推荐EU码"] + 0.5)
        
        # 高跟鞋 - 应该小半码
        rec_heel = recommend_shoe_size(26.5, "high_heel")
        self.assertEqual(rec_heel["推荐EU码"], rec["推荐EU码"] - 0.5)
    
    def test_validate_shoe_size_valid(self):
        """有效鞋码验证"""
        valid, msg = validate_shoe_size(42, "EU")
        self.assertTrue(valid)
        self.assertIsNone(msg)
        
        valid, msg = validate_shoe_size(8.5, "US_MEN")
        self.assertTrue(valid)
    
    def test_validate_shoe_size_invalid(self):
        """无效鞋码验证"""
        valid, msg = validate_shoe_size(100, "EU")
        self.assertFalse(valid)
        self.assertIn("15-52", msg)
        
        valid, msg = validate_shoe_size(-1, "UK")
        self.assertFalse(valid)
    
    def test_compare_sizes_equal(self):
        """比较相等尺码"""
        result = compare_sizes(42, "EU", 8.5, "US_MEN")
        # EU 42 ≈ US Men 8.5
        self.assertTrue(result["equal"] or abs(result["difference_cm"]) < 1)
    
    def test_compare_sizes_different(self):
        """比较不同尺码"""
        result = compare_sizes(45, "EU", 39, "EU")
        self.assertFalse(result["equal"])
        self.assertEqual(result["larger"], "size1")
        self.assertGreater(result["difference_cm"], 0)
    
    def test_find_closest_size(self):
        """查找最接近尺码"""
        size, diff = find_closest_size(26.5, "EU")
        self.assertIsNotNone(size)
        self.assertLess(diff, 1.0)  # 差值小于1cm
        
        # 精确匹配
        size, diff = find_closest_size(26.5, "CM")
        self.assertEqual(size, 26.5)


class TestSizeSystem(unittest.TestCase):
    """鞋码系统测试"""
    
    def test_size_system_values(self):
        """鞋码系统枚举值"""
        self.assertEqual(SizeSystem.EU.value, "EU")
        self.assertEqual(SizeSystem.US_MEN.value, "US_MEN")
        self.assertEqual(SizeSystem.UK.value, "UK")
        self.assertEqual(SizeSystem.CN.value, "CN")
    
    def test_gender_values(self):
        """性别枚举值"""
        self.assertEqual(Gender.MEN.value, "men")
        self.assertEqual(Gender.WOMEN.value, "women")
        self.assertEqual(Gender.CHILD.value, "child")


class TestShoeSize(unittest.TestCase):
    """鞋码数据结构测试"""
    
    def test_shoe_size_str(self):
        """鞋码字符串表示"""
        size = ShoeSize(42, SizeSystem.EU)
        self.assertEqual(str(size), "EU 42")
        
        size_with_gender = ShoeSize(8.5, SizeSystem.US_MEN, Gender.MEN)
        self.assertEqual(str(size_with_gender), "US_MEN 8.5 (men)")


class TestRoundTrip(unittest.TestCase):
    """往返转换测试"""
    
    def test_eu_roundtrip(self):
        """EU码往返转换"""
        original = 42.0
        cm = ShoeSizeConverter.eu_to_cm(original)
        back = ShoeSizeConverter.cm_to_eu(cm)
        self.assertAlmostEqual(original, back, delta=0.1)
    
    def test_us_men_roundtrip(self):
        """US男码往返转换"""
        original = 9.5
        cm = ShoeSizeConverter.us_men_to_cm(original)
        back = ShoeSizeConverter.cm_to_us_men(cm)
        self.assertAlmostEqual(original, back, delta=0.1)
    
    def test_us_women_roundtrip(self):
        """US女码往返转换"""
        original = 10.0
        cm = ShoeSizeConverter.us_women_to_cm(original)
        back = ShoeSizeConverter.cm_to_us_women(cm)
        self.assertAlmostEqual(original, back, delta=0.1)
    
    def test_uk_roundtrip(self):
        """UK码往返转换"""
        original = 8.0
        cm = ShoeSizeConverter.uk_to_cm(original)
        back = ShoeSizeConverter.cm_to_uk(cm)
        self.assertAlmostEqual(original, back, delta=0.1)
    
    def test_cn_roundtrip(self):
        """CN码往返转换"""
        original = 265
        cm = ShoeSizeConverter.cn_to_cm(original)
        back = ShoeSizeConverter.cm_to_cn(cm)
        self.assertEqual(original, back)


class TestCommonSizeChart(unittest.TestCase):
    """常用尺码表测试"""
    
    def test_chart_not_empty(self):
        """尺码表不为空"""
        self.assertTrue(len(COMMON_SIZE_CHART) > 0)
    
    def test_chart_consistency(self):
        """尺码表一致性"""
        for entry in COMMON_SIZE_CHART:
            # 每个条目应包含所有关键字段
            self.assertIn("EU", entry)
            self.assertIn("US_MEN", entry)
            self.assertIn("US_WOMEN", entry)
            self.assertIn("UK", entry)
            self.assertIn("CM", entry)
            self.assertIn("CN", entry)
            
            # 女码应比男码大约1-2码
            self.assertGreaterEqual(entry["US_WOMEN"] - entry["US_MEN"], 1)
            self.assertLessEqual(entry["US_WOMEN"] - entry["US_MEN"], 2)
            
            # CN码应为CM*10
            self.assertEqual(entry["CN"], entry["CM"] * 10)


class TestEdgeCases(unittest.TestCase):
    """边界情况测试"""
    
    def test_very_small_size(self):
        """婴儿鞋码"""
        # EU 15 (婴儿)
        all_sizes = get_all_sizes(15, "EU")
        self.assertLess(all_sizes["cm"], 15)
    
    def test_very_large_size(self):
        """大尺码"""
        # EU 52 (大码)
        all_sizes = get_all_sizes(52, "EU")
        self.assertGreater(all_sizes["cm"], 30)
    
    def test_half_sizes(self):
        """半码处理"""
        # EU 42.5
        result = convert_shoe_size(42.5, "EU", "US_MEN")
        self.assertIsInstance(result, float)
        
        # US Men 8.5
        result = convert_shoe_size(8.5, "US_MEN", "EU")
        self.assertIsInstance(result, float)


class TestInternationalSizes(unittest.TestCase):
    """国际尺码测试"""
    
    def test_brazil_size(self):
        """巴西码转换"""
        # EU 42 ≈ BR 38
        br = ShoeSizeConverter.convert(42, SizeSystem.EU, SizeSystem.BR)
        self.assertIsInstance(br, float)
        self.assertGreater(br, 30)
        self.assertLess(br, 45)
    
    def test_mexico_size(self):
        """墨西哥码转换"""
        mex = ShoeSizeConverter.convert(42, SizeSystem.EU, SizeSystem.MEX)
        self.assertIsInstance(mex, float)
    
    def test_korea_size(self):
        """韩国码转换"""
        kr = ShoeSizeConverter.convert(42, SizeSystem.EU, SizeSystem.KR)
        # 韩国码是毫米，应与CN码相同
        cn = ShoeSizeConverter.convert(42, SizeSystem.EU, SizeSystem.CN)
        self.assertEqual(kr, cn)


if __name__ == "__main__":
    unittest.main(verbosity=2)