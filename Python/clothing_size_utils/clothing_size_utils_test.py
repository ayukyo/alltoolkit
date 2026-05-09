"""
Clothing Size Utils 测试文件
"""

import unittest
from mod import (
    SizeRegion, ClothingType, SizeInfo, ShoeSize,
    convert_top_size, convert_pants_size, convert_shoe_size,
    convert_shoe_size_by_cm, calculate_bra_size,
    recommend_size_by_measurements, get_size_chart,
    list_all_regions, list_all_clothing_types, quick_size_guide,
    TOP_SIZE_CN, SHOE_SIZES, CUP_SIZES
)


class TestSizeRegion(unittest.TestCase):
    """测试地区枚举"""

    def test_all_regions_exist(self):
        """测试所有地区都已定义"""
        regions = list_all_regions()
        self.assertIn("中国", regions)
        self.assertIn("美国", regions)
        self.assertIn("欧洲", regions)
        self.assertIn("英国", regions)
        self.assertIn("日本", regions)
        self.assertEqual(len(regions), 10)


class TestClothingType(unittest.TestCase):
    """测试服装类型枚举"""

    def test_all_types_exist(self):
        """测试所有服装类型都已定义"""
        types = list_all_clothing_types()
        self.assertIn("上装", types)
        self.assertIn("裤装", types)
        self.assertIn("鞋子", types)
        self.assertIn("文胸", types)


class TestTopSizeConversion(unittest.TestCase):
    """测试上装尺码转换"""

    def test_cn_to_eu(self):
        """中国码转欧洲码"""
        self.assertEqual(convert_top_size("M", SizeRegion.CN, SizeRegion.EU), "38")
        self.assertEqual(convert_top_size("S", SizeRegion.CN, SizeRegion.EU), "36")
        self.assertEqual(convert_top_size("L", SizeRegion.CN, SizeRegion.EU), "40")

    def test_cn_to_us(self):
        """中国码转美国码"""
        self.assertEqual(convert_top_size("M", SizeRegion.CN, SizeRegion.US), "M")
        self.assertEqual(convert_top_size("XL", SizeRegion.CN, SizeRegion.US), "XL")

    def test_cn_to_uk(self):
        """中国码转英国码"""
        self.assertEqual(convert_top_size("M", SizeRegion.CN, SizeRegion.UK), "10")
        self.assertEqual(convert_top_size("S", SizeRegion.CN, SizeRegion.UK), "8")

    def test_cn_to_jp(self):
        """中国码转日本码"""
        self.assertEqual(convert_top_size("M", SizeRegion.CN, SizeRegion.JP), "9")
        self.assertEqual(convert_top_size("L", SizeRegion.CN, SizeRegion.JP), "11")

    def test_cn_to_kr(self):
        """中国码转韩国码"""
        self.assertEqual(convert_top_size("M", SizeRegion.CN, SizeRegion.KR), "66")
        self.assertEqual(convert_top_size("L", SizeRegion.CN, SizeRegion.KR), "77")

    def test_eu_to_cn(self):
        """欧洲码转中国码"""
        self.assertEqual(convert_top_size("38", SizeRegion.EU, SizeRegion.CN), "M")
        self.assertEqual(convert_top_size("36", SizeRegion.EU, SizeRegion.CN), "S")

    def test_uk_to_cn(self):
        """英国码转中国码"""
        self.assertEqual(convert_top_size("10", SizeRegion.UK, SizeRegion.CN), "M")
        self.assertEqual(convert_top_size("8", SizeRegion.UK, SizeRegion.CN), "S")

    def test_invalid_size(self):
        """无效尺码"""
        self.assertIsNone(convert_top_size("XXXL", SizeRegion.US, SizeRegion.CN))

    def test_case_insensitive(self):
        """大小写不敏感"""
        self.assertEqual(convert_top_size("m", SizeRegion.CN, SizeRegion.EU), "38")
        self.assertEqual(convert_top_size("M", SizeRegion.CN, SizeRegion.EU), "38")


class TestPantsSizeConversion(unittest.TestCase):
    """测试裤装尺码转换"""

    def test_waist_to_us(self):
        """腰围转美国码"""
        self.assertEqual(convert_pants_size(68, SizeRegion.US), "2")
        self.assertEqual(convert_pants_size(72, SizeRegion.US), "4")

    def test_waist_to_eu(self):
        """腰围转欧洲码"""
        self.assertEqual(convert_pants_size(68, SizeRegion.EU), "36")
        self.assertEqual(convert_pants_size(72, SizeRegion.EU), "38")

    def test_waist_to_uk(self):
        """腰围转英国码"""
        self.assertEqual(convert_pants_size(68, SizeRegion.UK), "6")
        self.assertEqual(convert_pants_size(72, SizeRegion.UK), "8")

    def test_waist_to_jp(self):
        """腰围转日本码"""
        self.assertEqual(convert_pants_size(68, SizeRegion.JP), "7")
        self.assertEqual(convert_pants_size(72, SizeRegion.JP), "9")

    def test_waist_to_cn(self):
        """腰围转中国码"""
        self.assertEqual(convert_pants_size(64, SizeRegion.CN), "S")
        self.assertEqual(convert_pants_size(68, SizeRegion.CN), "M")

    def test_large_waist(self):
        """大腰围"""
        self.assertEqual(convert_pants_size(85, SizeRegion.US), "8")  # 返回最大尺码


class TestShoeSizeConversion(unittest.TestCase):
    """测试鞋码转换"""

    def test_cn_to_us_women(self):
        """中国码转美国女码"""
        self.assertEqual(convert_shoe_size(38, SizeRegion.CN, SizeRegion.US, "women"), 7.5)
        self.assertEqual(convert_shoe_size(40, SizeRegion.CN, SizeRegion.US, "women"), 8.5)

    def test_cn_to_us_men(self):
        """中国码转美国男码"""
        self.assertEqual(convert_shoe_size(42, SizeRegion.CN, SizeRegion.US, "men"), 9)
        self.assertEqual(convert_shoe_size(44, SizeRegion.CN, SizeRegion.US, "men"), 11)

    def test_cn_to_eu(self):
        """中国码转欧洲码"""
        self.assertEqual(convert_shoe_size(38, SizeRegion.CN, SizeRegion.EU, "unisex"), 38)
        self.assertEqual(convert_shoe_size(40, SizeRegion.CN, SizeRegion.EU, "unisex"), 40)

    def test_cn_to_uk(self):
        """中国码转英国码"""
        self.assertEqual(convert_shoe_size(38, SizeRegion.CN, SizeRegion.UK, "unisex"), 5)
        self.assertEqual(convert_shoe_size(42, SizeRegion.CN, SizeRegion.UK, "unisex"), 8)

    def test_cn_to_jp(self):
        """中国码转日本码"""
        self.assertEqual(convert_shoe_size(38, SizeRegion.CN, SizeRegion.JP, "unisex"), 24)
        self.assertEqual(convert_shoe_size(42, SizeRegion.CN, SizeRegion.JP, "unisex"), 27)

    def test_us_to_cn(self):
        """美国码转中国码"""
        self.assertEqual(convert_shoe_size(8, SizeRegion.US, SizeRegion.CN, "men"), 41)
        self.assertEqual(convert_shoe_size(7.5, SizeRegion.US, SizeRegion.CN, "women"), 38)

    def test_eu_to_cn(self):
        """欧洲码转中国码"""
        self.assertEqual(convert_shoe_size(40, SizeRegion.EU, SizeRegion.CN, "unisex"), 40)
        self.assertEqual(convert_shoe_size(42, SizeRegion.EU, SizeRegion.CN, "unisex"), 42)

    def test_invalid_shoe_size(self):
        """无效鞋码"""
        self.assertIsNone(convert_shoe_size(99, SizeRegion.CN, SizeRegion.US, "women"))

    def test_foot_length_to_shoe(self):
        """脚长转鞋码"""
        self.assertEqual(convert_shoe_size_by_cm(25.0), 40)
        self.assertEqual(convert_shoe_size_by_cm(23.0), 36)
        self.assertEqual(convert_shoe_size_by_cm(27.0), 42)

    def test_foot_length_edge(self):
        """边界脚长"""
        self.assertEqual(convert_shoe_size_by_cm(21.5), 34)
        self.assertEqual(convert_shoe_size_by_cm(31.0), 46)


class TestBraSizeCalculation(unittest.TestCase):
    """测试文胸尺码计算"""

    def test_basic_bra_size(self):
        """基本文胸尺码计算"""
        # 胸围差 88-75=13cm, 约B罩杯
        size = calculate_bra_size(75, 88, SizeRegion.CN)
        self.assertEqual(size, "75B")

    def test_cup_sizes(self):
        """不同罩杯计算"""
        # A罩杯 (差约11cm)
        self.assertEqual(calculate_bra_size(75, 86, SizeRegion.CN), "75A")
        # B罩杯 (差约13cm)
        self.assertEqual(calculate_bra_size(75, 88, SizeRegion.CN), "75B")
        # C罩杯 (差约16cm)
        self.assertEqual(calculate_bra_size(75, 91, SizeRegion.CN), "75C")
        # D罩杯 (差约19cm)
        self.assertEqual(calculate_bra_size(75, 94, SizeRegion.CN), "75D")

    def test_bra_size_to_us(self):
        """转换为美国码"""
        # CN 75 = US 34
        size_us = calculate_bra_size(75, 88, SizeRegion.US)
        self.assertEqual(size_us, "34B")

    def test_bra_size_to_eu(self):
        """转换为欧洲码"""
        size_eu = calculate_bra_size(75, 88, SizeRegion.EU)
        self.assertEqual(size_eu, "75B")

    def test_different_band_sizes(self):
        """不同下胸围"""
        self.assertEqual(calculate_bra_size(70, 83, SizeRegion.CN), "70B")
        self.assertEqual(calculate_bra_size(80, 93, SizeRegion.CN), "80B")
        self.assertEqual(calculate_bra_size(85, 98, SizeRegion.CN), "85B")


class TestSizeRecommendation(unittest.TestCase):
    """测试尺码推荐"""

    def test_perfect_fit(self):
        """完美匹配"""
        result = recommend_size_by_measurements(86, 70, 92, ClothingType.TOP, SizeRegion.CN)
        self.assertEqual(result["size"], "M")
        self.assertTrue(result["bust_fit"])
        self.assertTrue(result["waist_fit"])
        self.assertTrue(result["hip_fit"])

    def test_partial_fit(self):
        """部分匹配"""
        result = recommend_size_by_measurements(90, 70, 92, ClothingType.TOP, SizeRegion.CN)
        self.assertIsNotNone(result["size"])
        self.assertTrue(result["bust_fit"] or result["waist_fit"] or result["hip_fit"])

    def test_measurements_returned(self):
        """测量值返回"""
        result = recommend_size_by_measurements(88, 72, 94, ClothingType.TOP, SizeRegion.CN)
        self.assertEqual(result["measurements"]["bust"], 88)
        self.assertEqual(result["measurements"]["waist"], 72)
        self.assertEqual(result["measurements"]["hip"], 94)

    def test_pants_recommendation(self):
        """裤装推荐"""
        result = recommend_size_by_measurements(82, 66, 90, ClothingType.PANTS, SizeRegion.CN)
        self.assertIsNotNone(result["size"])


class TestSizeChart(unittest.TestCase):
    """测试尺码表获取"""

    def test_top_size_chart_cn(self):
        """中国上装尺码表"""
        chart = get_size_chart(ClothingType.TOP, SizeRegion.CN)
        self.assertIn("M", chart)
        self.assertEqual(chart["M"], "M")

    def test_top_size_chart_eu(self):
        """欧洲上装尺码表"""
        chart = get_size_chart(ClothingType.TOP, SizeRegion.EU)
        self.assertIn("M", chart)
        self.assertEqual(chart["M"], "38")

    def test_shoe_size_chart(self):
        """鞋码表"""
        chart = get_size_chart(ClothingType.SHOES, SizeRegion.CN)
        self.assertIn("38", chart)
        self.assertIn("cn", chart["38"])
        self.assertIn("us_men", chart["38"])
        self.assertIn("us_women", chart["38"])

    def test_bra_size_chart(self):
        """文胸尺码表"""
        chart = get_size_chart(ClothingType.BRA, SizeRegion.CN)
        self.assertIn("bands", chart)
        self.assertIn("cups", chart)
        self.assertIn("A", chart["cups"])

    def test_hat_size_chart(self):
        """帽子尺码表"""
        chart = get_size_chart(ClothingType.HAT, SizeRegion.CN)
        self.assertIn(54, chart)
        self.assertEqual(chart[54], "S")

    def test_ring_size_chart(self):
        """戒指尺码表"""
        chart = get_size_chart(ClothingType.RING, SizeRegion.CN)
        self.assertIn(52, chart)

    def test_gloves_size_chart(self):
        """手套尺码表"""
        chart = get_size_chart(ClothingType.GLOVES, SizeRegion.CN)
        self.assertIn(17, chart)


class TestQuickSizeGuide(unittest.TestCase):
    """测试快速尺码指南"""

    def test_complete_measurements(self):
        """完整测量值"""
        result = quick_size_guide({
            "bust": 88,
            "waist": 72,
            "hip": 94,
            "foot_length": 25,
            "underbust": 75,
            "overbust": 88
        })
        self.assertIn("top", result)
        self.assertIn("pants", result)
        self.assertIn("shoes", result)
        self.assertIn("bra", result)

    def test_partial_measurements(self):
        """部分测量值"""
        result = quick_size_guide({
            "bust": 88,
            "waist": 72,
            "hip": 94
        })
        self.assertIn("top", result)
        self.assertIn("pants", result)
        self.assertNotIn("shoes", result)
        self.assertNotIn("bra", result)

    def test_foot_only(self):
        """只有脚长"""
        result = quick_size_guide({
            "foot_length": 25
        })
        self.assertIn("shoes", result)
        self.assertEqual(result["shoes"], "40")


class TestDataStructures(unittest.TestCase):
    """测试数据结构"""

    def test_top_size_cn_structure(self):
        """上装尺码结构"""
        self.assertIn("M", TOP_SIZE_CN)
        size_info = TOP_SIZE_CN["M"]
        self.assertIsInstance(size_info, SizeInfo)
        self.assertEqual(size_info.label, "M")
        self.assertGreater(size_info.bust_min, 0)
        self.assertGreater(size_info.bust_max, size_info.bust_min)

    def test_shoe_sizes_structure(self):
        """鞋码数据结构"""
        self.assertGreater(len(SHOE_SIZES), 0)
        for shoe in SHOE_SIZES:
            self.assertIsInstance(shoe, ShoeSize)
            self.assertGreater(shoe.cn, 0)
            self.assertGreater(shoe.cm, 0)

    def test_cup_sizes_structure(self):
        """罩杯数据结构"""
        self.assertIn("A", CUP_SIZES)
        self.assertIn("B", CUP_SIZES)
        self.assertIn("D", CUP_SIZES)

        min_diff, max_diff, desc = CUP_SIZES["A"]
        self.assertGreater(max_diff, min_diff)


class TestEdgeCases(unittest.TestCase):
    """测试边界情况"""

    def test_large_size(self):
        """大尺码"""
        result = convert_top_size("XXXL", SizeRegion.CN, SizeRegion.EU)
        self.assertEqual(result, "46")

    def test_small_foot(self):
        """小脚"""
        size = convert_shoe_size_by_cm(21.0)
        self.assertEqual(size, 34)

    def test_large_foot(self):
        """大脚"""
        size = convert_shoe_size_by_cm(30.0)
        self.assertEqual(size, 45)

    def test_zero_measurements(self):
        """零测量值"""
        result = recommend_size_by_measurements(0, 0, 0, ClothingType.TOP, SizeRegion.CN)
        # 应该返回某种结果，即使是错误情况
        self.assertIsInstance(result, dict)


if __name__ == "__main__":
    unittest.main(verbosity=2)