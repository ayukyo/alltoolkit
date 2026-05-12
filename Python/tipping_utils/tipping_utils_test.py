"""
Tipping Utils 测试套件

测试小费计算工具的各种功能
"""

import sys
import os
import unittest

# 添加父目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from tipping_utils.mod import (
    Country,
    ServiceType,
    TipRecommendation,
    BillSplit,
    TipCalculation,
    TIPPING_DATA,
    get_tip_recommendation,
    calculate_tip,
    calculate_tip_with_tax,
    split_bill,
    split_by_items,
    round_tip,
    suggest_tip,
    calculate_percentage,
    calculate_quick_tips,
    is_tipping_customary,
    get_countries_by_tipping_culture,
    convert_tip_for_currency,
    calculate_tip_range,
    calculate_tip_with_rounding,
    format_tip_summary,
    calculate_shared_tip,
    tip,
    split,
)


class TestCountryEnum(unittest.TestCase):
    """测试国家枚举"""
    
    def test_country_exists(self):
        """测试国家存在"""
        self.assertEqual(Country.USA.value, "USA")
        self.assertEqual(Country.JAPAN.value, "Japan")
        self.assertEqual(Country.CHINA.value, "China")
    
    def test_all_countries_have_value(self):
        """测试所有国家都有值"""
        for country in Country:
            self.assertTrue(len(country.value) > 0)


class TestServiceTypeEnum(unittest.TestCase):
    """测试服务类型枚举"""
    
    def test_service_type_exists(self):
        """测试服务类型存在"""
        self.assertEqual(ServiceType.RESTAURANT.value, "restaurant")
        self.assertEqual(ServiceType.TAXI.value, "taxi")
        self.assertEqual(ServiceType.HOTEL.value, "hotel")


class TestTipRecommendation(unittest.TestCase):
    """测试小费建议"""
    
    def test_tip_recommendation_creation(self):
        """测试创建小费建议"""
        rec = TipRecommendation(
            country=Country.USA,
            service_type=ServiceType.RESTAURANT,
            min_percent=15.0,
            max_percent=25.0,
            standard_percent=18.0,
            is_customary=True,
            is_expected=True,
            is_included=False,
            notes="测试说明"
        )
        self.assertEqual(rec.country, Country.USA)
        self.assertEqual(rec.standard_percent, 18.0)
    
    def test_get_tip_recommendation_usa_restaurant(self):
        """测试获取美国餐厅小费建议"""
        rec = get_tip_recommendation(Country.USA, ServiceType.RESTAURANT)
        self.assertIsNotNone(rec)
        self.assertEqual(rec.min_percent, 15.0)
        self.assertEqual(rec.max_percent, 25.0)
        self.assertTrue(rec.is_expected)
    
    def test_get_tip_recommendation_japan_restaurant(self):
        """测试获取日本餐厅小费建议"""
        rec = get_tip_recommendation(Country.JAPAN, ServiceType.RESTAURANT)
        self.assertIsNotNone(rec)
        self.assertEqual(rec.min_percent, 0.0)
        self.assertEqual(rec.max_percent, 0.0)
        self.assertFalse(rec.is_customary)
    
    def test_get_tip_recommendation_missing_country(self):
        """测试缺失国家数据"""
        # 测试有国家但没有特定服务的情况
        rec = get_tip_recommendation(Country.FINLAND, ServiceType.RESTAURANT)
        self.assertIsNone(rec)  # Finland 不在 TIPPING_DATA 中
    
    def test_get_tip_recommendation_missing_service(self):
        """测试缺失服务类型数据"""
        rec = get_tip_recommendation(Country.UK, ServiceType.SPA)
        self.assertIsNone(rec)  # UK 没有 SPA 数据


class TestCalculateTip(unittest.TestCase):
    """测试小费计算"""
    
    def test_basic_tip_calculation(self):
        """测试基本小费计算"""
        calc = calculate_tip(100.0, 18.0)
        self.assertEqual(calc.bill_amount, 100.0)
        self.assertEqual(calc.tip_percent, 18.0)
        self.assertEqual(calc.tip_amount, 18.0)
        self.assertEqual(calc.total, 118.0)
    
    def test_tip_calculation_with_included_tax(self):
        """测试含税计算（税已包含）"""
        calc = calculate_tip(100.0, 18.0, tax=8.25, tax_included=True)
        self.assertEqual(calc.bill_amount, 100.0)
        self.assertEqual(calc.tip_amount, 18.0)
        self.assertEqual(calc.tax, 8.25)
        self.assertEqual(calc.tax_included, True)
        # 税已包含，grand_total 应该等于 total
        self.assertEqual(calc.grand_total, 118.0)
    
    def test_tip_calculation_with_extra_tax(self):
        """测试含税计算（税未包含）"""
        calc = calculate_tip(100.0, 18.0, tax=8.25, tax_included=False)
        self.assertEqual(calc.bill_amount, 100.0)
        self.assertEqual(calc.tip_amount, 18.0)
        # 税未包含，grand_total 应该包含税
        self.assertEqual(calc.grand_total, 126.25)  # 100 + 18 + 8.25
    
    def test_zero_tip(self):
        """测试零小费"""
        calc = calculate_tip(100.0, 0.0)
        self.assertEqual(calc.tip_amount, 0.0)
        self.assertEqual(calc.total, 100.0)
    
    def test_high_tip(self):
        """测试高小费比例"""
        calc = calculate_tip(100.0, 50.0)
        self.assertEqual(calc.tip_amount, 50.0)
        self.assertEqual(calc.total, 150.0)
    
    def test_decimal_bill(self):
        """测试小数账单"""
        calc = calculate_tip(99.99, 18.0)
        self.assertAlmostEqual(calc.tip_amount, 17.9982, places=2)
        self.assertAlmostEqual(calc.total, 117.9882, places=2)
    
    def test_zero_tax(self):
        """测试零税金"""
        calc = calculate_tip(100.0, 18.0, tax=0.0)
        self.assertIsNone(calc.tax)
        self.assertIsNone(calc.grand_total)


class TestCalculateTipWithTax(unittest.TestCase):
    """测试含税小费计算"""
    
    def test_tip_on_pre_tax(self):
        """测试税前计算小费"""
        calc = calculate_tip_with_tax(100.0, 18.0, 8.25, tip_on_pre_tax=True)
        self.assertEqual(calc.tax, 8.25)
        self.assertEqual(calc.tip_amount, 18.0)  # 基于税前
        self.assertEqual(calc.grand_total, 126.25)
    
    def test_tip_on_post_tax(self):
        """测试税后计算小费"""
        calc = calculate_tip_with_tax(100.0, 18.0, 8.25, tip_on_pre_tax=False)
        self.assertEqual(calc.tax, 8.25)
        # 基于税后: (100 + 8.25) * 0.18 = 19.485 → round to 19.48
        self.assertAlmostEqual(calc.tip_amount, 19.485, places=2)
    
    def test_zero_tax_percent(self):
        """测试零税率"""
        calc = calculate_tip_with_tax(100.0, 18.0, 0.0)
        self.assertEqual(calc.tax, 0.0)
        self.assertEqual(calc.tip_amount, 18.0)


class TestSplitBill(unittest.TestCase):
    """测试账单分割"""
    
    def test_basic_split(self):
        """测试基本分割"""
        result = split_bill(100.0, 4)
        self.assertEqual(result.subtotal, 100.0)
        self.assertEqual(result.tip, 0.0)
        self.assertEqual(result.total, 100.0)
        self.assertEqual(result.per_person, 25.0)
        self.assertEqual(result.people_count, 4)
    
    def test_split_with_tip(self):
        """测试含小费分割"""
        result = split_bill(100.0, 4, tip_percent=20.0)
        self.assertEqual(result.tip, 20.0)
        self.assertEqual(result.total, 120.0)
        self.assertEqual(result.per_person, 30.0)
    
    def test_split_with_tax(self):
        """测试含税分割"""
        result = split_bill(100.0, 4, tip_percent=18.0, tax=8.25, tax_included=False)
        self.assertEqual(result.tax, 8.25)
        # 总计 = 100 + 18 + 8.25 = 126.25
        self.assertEqual(result.total, 126.25)
        self.assertAlmostEqual(result.per_person, 31.5625, places=2)
    
    def test_split_individual_amounts(self):
        """测试不均等分割"""
        individual = [30.0, 40.0, 30.0]
        result = split_bill(100.0, 3, tip_percent=18.0, individual_amounts=individual)
        self.assertEqual(result.people_count, 3)
        # 检查每个人按比例分摊
        self.assertIsNotNone(result.individual_amounts)
        # 总小费是 18，按比例分摊
        # 30 -> 30 + 30/100*18 = 35.4
        # 40 -> 40 + 40/100*18 = 47.2
        # 30 -> 30 + 30/100*18 = 35.4
        self.assertAlmostEqual(result.individual_amounts[0], 35.4, places=2)
        self.assertAlmostEqual(result.individual_amounts[1], 47.2, places=2)
        self.assertAlmostEqual(result.individual_amounts[2], 35.4, places=2)
    
    def test_split_round_up(self):
        """测试向上取整"""
        result = split_bill(100.0, 3, tip_percent=18.0, round_up=True)
        # 118 / 3 = 39.333..., 向上取整
        self.assertGreaterEqual(result.per_person, 39.33)
    
    def test_split_invalid_people_count(self):
        """测试无效人数"""
        with self.assertRaises(ValueError):
            split_bill(100.0, 0)
        
        with self.assertRaises(ValueError):
            split_bill(100.0, -1)
    
    def test_split_invalid_bill(self):
        """测试无效账单金额"""
        with self.assertRaises(ValueError):
            split_bill(-100.0, 4)
    
    def test_split_mismatched_individual_amounts(self):
        """测试个人金额数量不匹配"""
        with self.assertRaises(ValueError):
            split_bill(100.0, 4, individual_amounts=[25.0, 25.0, 25.0])
    
    def test_split_wrong_individual_total(self):
        """测试个人金额总和错误"""
        with self.assertRaises(ValueError):
            split_bill(100.0, 3, individual_amounts=[20.0, 30.0, 40.0])


class TestSplitByItems(unittest.TestCase):
    """测试按项目分摊"""
    
    def test_split_by_items_basic(self):
        """测试基本项目分摊"""
        items = [("Alice", 50.0), ("Bob", 30.0), ("Charlie", 20.0)]
        result = split_by_items(items, tip_percent=20.0)
        
        self.assertEqual(len(result), 3)
        # Alice: 50 + 50/100*20 = 60
        # Bob: 30 + 30/100*20 = 36
        # Charlie: 20 + 20/100*20 = 24
        self.assertAlmostEqual(result["Alice"], 60.0, places=2)
        self.assertAlmostEqual(result["Bob"], 36.0, places=2)
        self.assertAlmostEqual(result["Charlie"], 24.0, places=2)
    
    def test_split_by_items_with_tax(self):
        """测试含税项目分摊"""
        items = [("Alice", 100.0)]
        result = split_by_items(items, tip_percent=18.0, tax=8.25, tax_included=False)
        # Alice: 100 + 18 (tip) + 8.25 (tax) = 126.25
        self.assertAlmostEqual(result["Alice"], 126.25, places=2)
    
    def test_split_by_items_with_tax_percent(self):
        """测试含税率项目分摊"""
        items = [("Alice", 100.0)]
        result = split_by_items(items, tip_percent=18.0, tax_percent=8.25, tax_included=False)
        # Alice: 100 + 18 (tip) + 8.25 (tax) = 126.25
        self.assertAlmostEqual(result["Alice"], 126.25, places=2)
    
    def test_split_by_items_empty(self):
        """测试空项目列表"""
        result = split_by_items([])
        self.assertEqual(result, {})


class TestRoundTip(unittest.TestCase):
    """测试小费四舍五入"""
    
    def test_round_nearest(self):
        """测试四舍五入到最近"""
        result = round_tip(3.73, method="nearest", precision=0.25)
        self.assertEqual(result, 3.75)
    
    def test_round_up(self):
        """测试向上取整"""
        result = round_tip(3.51, method="up", precision=0.50)
        self.assertEqual(result, 4.0)
    
    def test_round_down(self):
        """测试向下取整"""
        result = round_tip(3.99, method="down", precision=0.50)
        self.assertEqual(result, 3.5)
    
    def test_round_to_nearest_dollar(self):
        """测试四舍五入到整美元"""
        result = round_tip(3.25, method="nearest", precision=1.0)
        self.assertEqual(result, 3.0)
    
    def test_round_exact(self):
        """测试精确值"""
        result = round_tip(3.50, method="nearest", precision=0.50)
        self.assertEqual(result, 3.50)


class TestSuggestTip(unittest.TestCase):
    """测试小费建议"""
    
    def test_suggest_tip_usa_good(self):
        """测试美国优质服务建议"""
        tip_amt, note = suggest_tip(100.0, Country.USA, ServiceType.RESTAURANT, "good")
        self.assertEqual(tip_amt, 18.0)  # 18% 标准
        self.assertIn("15", note)
    
    def test_suggest_tip_usa_excellent(self):
        """测试美国卓越服务建议"""
        tip_amt, note = suggest_tip(100.0, Country.USA, ServiceType.RESTAURANT, "excellent")
        self.assertEqual(tip_amt, 25.0)  # 25% 最高
    
    def test_suggest_tip_usa_poor(self):
        """测试美国差服务建议"""
        tip_amt, note = suggest_tip(100.0, Country.USA, ServiceType.RESTAURANT, "poor")
        self.assertEqual(tip_amt, 15.0)  # 15% 最低
    
    def test_suggest_tip_japan(self):
        """测试日本小费建议"""
        tip_amt, note = suggest_tip(100.0, Country.JAPAN, ServiceType.RESTAURANT, "good")
        self.assertEqual(tip_amt, 0.0)  # 日本不期望小费
        self.assertIn("无礼", note)
    
    def test_suggest_tip_unknown_country(self):
        """测试未知国家小费建议"""
        tip_amt, note = suggest_tip(100.0, Country.FINLAND, ServiceType.RESTAURANT, "good")
        self.assertEqual(tip_amt, 0.0)
        self.assertIn("无", note)
    
    def test_suggest_tip_unknown_quality(self):
        """测试未知服务质量"""
        tip_amt, note = suggest_tip(100.0, Country.USA, ServiceType.RESTAURANT, "unknown")
        # 应该返回标准小费
        self.assertEqual(tip_amt, 18.0)


class TestCalculatePercentage(unittest.TestCase):
    """测试小费百分比计算"""
    
    def test_calculate_percentage_basic(self):
        """测试基本百分比计算"""
        percent = calculate_percentage(100.0, 18.0)
        self.assertEqual(percent, 18.0)
    
    def test_calculate_percentage_decimal(self):
        """测试小数百分比计算"""
        percent = calculate_percentage(100.0, 15.5)
        self.assertEqual(percent, 15.5)
    
    def test_calculate_percentage_reverse(self):
        """测试反向百分比计算"""
        percent = calculate_percentage(50.0, 10.0)
        self.assertEqual(percent, 20.0)
    
    def test_calculate_percentage_zero_bill(self):
        """测试零账单"""
        percent = calculate_percentage(0.0, 10.0)
        self.assertEqual(percent, 0.0)


class TestCalculateQuickTips(unittest.TestCase):
    """测试快速小费计算"""
    
    def test_quick_tips_basic(self):
        """测试基本快速计算"""
        result = calculate_quick_tips(100.0)
        self.assertEqual(result["10%"].tip_amount, 10.0)
        self.assertEqual(result["15%"].tip_amount, 15.0)
        self.assertEqual(result["18%"].tip_amount, 18.0)
        self.assertEqual(result["20%"].tip_amount, 20.0)
        self.assertEqual(result["25%"].tip_amount, 25.0)
    
    def test_quick_tips_decimal(self):
        """测试小数账单"""
        result = calculate_quick_tips(33.33)
        self.assertAlmostEqual(result["18%"].tip_amount, 6.0, places=2)


class TestIsTippingCustomary(unittest.TestCase):
    """测试小费文化判断"""
    
    def test_usa_customary(self):
        """测试美国小费文化"""
        self.assertTrue(is_tipping_customary(Country.USA, ServiceType.RESTAURANT))
    
    def test_japan_not_customary(self):
        """测试日本无小费文化"""
        self.assertFalse(is_tipping_customary(Country.JAPAN, ServiceType.RESTAURANT))
    
    def test_china_not_customary(self):
        """测试中国无小费文化"""
        self.assertFalse(is_tipping_customary(Country.CHINA, ServiceType.RESTAURANT))


class TestGetCountriesByTippingCulture(unittest.TestCase):
    """测试国家小费文化分类"""
    
    def test_classify_countries(self):
        """测试国家分类"""
        result = get_countries_by_tipping_culture()
        
        self.assertIn(Country.USA, result["strong"])
        self.assertIn(Country.JAPAN, result["none"])
        self.assertIn(Country.CHINA, result["none"])
    
    def test_all_countries_classified(self):
        """测试所有国家都被分类"""
        result = get_countries_by_tipping_culture()
        
        total = sum(len(countries) for countries in result.values())
        self.assertEqual(total, len(Country))


class TestConvertTipForCurrency(unittest.TestCase):
    """测试货币换算"""
    
    def test_currency_conversion_basic(self):
        """测试基本货币换算"""
        result = convert_tip_for_currency(10.0, "USD", "EUR", 0.85)
        self.assertEqual(result, 8.5)
    
    def test_currency_conversion_high_rate(self):
        """测试高汇率换算"""
        result = convert_tip_for_currency(10.0, "USD", "JPY", 110.0)
        self.assertEqual(result, 1100.0)
    
    def test_currency_conversion_rounding(self):
        """测试换算舍入"""
        result = convert_tip_for_currency(10.0, "USD", "EUR", 0.856789)
        self.assertEqual(result, 8.57)


class TestCalculateTipRange(unittest.TestCase):
    """测试小费范围计算"""
    
    def test_tip_range_basic(self):
        """测试基本范围计算"""
        min_tip, max_tip = calculate_tip_range(100.0, 15.0, 25.0)
        self.assertEqual(min_tip, 15.0)
        self.assertEqual(max_tip, 25.0)
    
    def test_tip_range_decimal(self):
        """测试小数范围计算"""
        min_tip, max_tip = calculate_tip_range(99.99, 15.0, 20.0)
        self.assertAlmostEqual(min_tip, 14.9985, places=2)
        self.assertAlmostEqual(max_tip, 19.998, places=2)
    
    def test_tip_range_custom(self):
        """测试自定义范围"""
        min_tip, max_tip = calculate_tip_range(100.0, 10.0, 30.0)
        self.assertEqual(min_tip, 10.0)
        self.assertEqual(max_tip, 30.0)


class TestCalculateTipWithRounding(unittest.TestCase):
    """测试四舍五入小费计算"""
    
    def test_rounding_nearest(self):
        """测试四舍五入"""
        raw, rounded, total = calculate_tip_with_rounding(100.0, 18.0, 0.50, "nearest")
        self.assertEqual(raw, 18.0)
        self.assertEqual(rounded, 18.0)
        self.assertEqual(total, 118.0)
    
    def test_rounding_up(self):
        """测试向上取整"""
        raw, rounded, total = calculate_tip_with_rounding(100.0, 17.6, 0.50, "up")
        self.assertEqual(raw, 17.6)
        self.assertEqual(rounded, 18.0)  # 17.6 向上取整到 18
        self.assertEqual(total, 118.0)
    
    def test_rounding_down(self):
        """测试向下取整"""
        raw, rounded, total = calculate_tip_with_rounding(100.0, 18.4, 0.50, "down")
        self.assertEqual(raw, 18.4)
        self.assertEqual(rounded, 18.0)  # 18.4 向下取整到 18
        self.assertEqual(total, 118.0)


class TestFormatTipSummary(unittest.TestCase):
    """测试格式化小费摘要"""
    
    def test_format_basic(self):
        """测试基本格式化"""
        summary = format_tip_summary(100.0, 18.0)
        self.assertIn("$100.00", summary)
        self.assertIn("$18.00", summary)
        self.assertIn("$118.00", summary)
    
    def test_format_with_included_tax(self):
        """测试含已含税格式化"""
        summary = format_tip_summary(100.0, 18.0, tax=8.25, tax_included=True, currency_symbol="€")
        self.assertIn("€", summary)
        self.assertIn("税金", summary)
    
    def test_format_with_extra_tax(self):
        """测试含额外税格式化"""
        summary = format_tip_summary(100.0, 18.0, tax=8.25, tax_included=False)
        self.assertIn("额外", summary)
    
    def test_format_custom_currency(self):
        """测试自定义货币符号"""
        summary = format_tip_summary(100.0, 18.0, currency_symbol="¥")
        self.assertIn("¥", summary)


class TestCalculateSharedTip(unittest.TestCase):
    """测试分摊小费计算"""
    
    def test_shared_tip_equal(self):
        """测试均等分摊"""
        result = calculate_shared_tip(100.0, 20.0, 4)
        self.assertEqual(result["person_1"], 30.0)
        self.assertEqual(result["person_2"], 30.0)
        self.assertEqual(result["person_3"], 30.0)
        self.assertEqual(result["person_4"], 30.0)
    
    def test_shared_tip_individual(self):
        """测试个人分摊"""
        individual = [40.0, 30.0, 30.0]
        result = calculate_shared_tip(100.0, 20.0, 3, individual)
        # 每人按比例分摊小费
        self.assertAlmostEqual(result["person_1"], 48.0, places=2)  # 40 + 8
        self.assertAlmostEqual(result["person_2"], 36.0, places=2)  # 30 + 6
        self.assertAlmostEqual(result["person_3"], 36.0, places=2)  # 30 + 6
    
    def test_shared_tip_invalid_individual_count(self):
        """测试无效个人数量"""
        with self.assertRaises(ValueError):
            calculate_shared_tip(100.0, 20.0, 4, [25.0, 25.0, 25.0])


class TestConvenienceFunctions(unittest.TestCase):
    """测试便捷函数"""
    
    def test_tip_function(self):
        """测试 tip() 便捷函数"""
        tip_amt, total = tip(100.0, 18.0)
        self.assertEqual(tip_amt, 18.0)
        self.assertEqual(total, 118.0)
    
    def test_tip_default_percent(self):
        """测试默认小费比例"""
        tip_amt, total = tip(100.0)
        self.assertEqual(tip_amt, 18.0)
    
    def test_split_function(self):
        """测试 split() 便捷函数"""
        result = split(100.0, 4, 20.0)
        self.assertEqual(result, 30.0)
    
    def test_split_default_percent(self):
        """测试默认分割比例"""
        result = split(100.0, 4)
        self.assertEqual(result, 29.5)  # 118 / 4


class TestEdgeCases(unittest.TestCase):
    """测试边界情况"""
    
    def test_zero_bill(self):
        """测试零账单"""
        calc = calculate_tip(0.0, 18.0)
        self.assertEqual(calc.tip_amount, 0.0)
        self.assertEqual(calc.total, 0.0)
    
    def test_large_bill(self):
        """测试大额账单"""
        calc = calculate_tip(10000.0, 18.0)
        self.assertEqual(calc.tip_amount, 1800.0)
        self.assertEqual(calc.total, 11800.0)
    
    def test_very_small_bill(self):
        """测试极小账单"""
        calc = calculate_tip(0.01, 18.0)
        # 0.01 * 0.18 = 0.0018, rounded to 0.00
        self.assertEqual(calc.tip_amount, 0.00)
    
    def test_one_person_split(self):
        """测试单人分割"""
        result = split_bill(100.0, 1, 18.0)
        self.assertEqual(result.per_person, 118.0)
    
    def test_many_people_split(self):
        """测试多人分割"""
        result = split_bill(100.0, 100, 18.0)
        self.assertAlmostEqual(result.per_person, 1.18, places=2)


class TestTippingData(unittest.TestCase):
    """测试小费数据库"""
    
    def test_data_integrity(self):
        """测试数据完整性"""
        for country, services in TIPPING_DATA.items():
            for service_type, rec in services.items():
                self.assertEqual(rec.country, country)
                self.assertEqual(rec.service_type, service_type)
                self.assertGreaterEqual(rec.min_percent, 0)
                self.assertGreaterEqual(rec.max_percent, rec.min_percent)
                self.assertGreaterEqual(rec.standard_percent, rec.min_percent)
                self.assertLessEqual(rec.standard_percent, rec.max_percent)
    
    def test_usa_data_completeness(self):
        """测试美国数据完整性"""
        usa_data = TIPPING_DATA.get(Country.USA, {})
        # 应该有餐厅、出租车、酒店等服务
        self.assertIn(ServiceType.RESTAURANT, usa_data)
        self.assertIn(ServiceType.TAXI, usa_data)


if __name__ == "__main__":
    unittest.main(verbosity=2)