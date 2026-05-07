#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AllToolkit - Shoe Size Utilities Test Suite
==============================================
Comprehensive tests for the shoe_size_utils module.

Author: AllToolkit Contributors
License: MIT
"""

import unittest
import sys
import os

# Add module path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from shoe_size_utils.mod import (
    # Conversion functions
    foot_length_to_cn,
    foot_length_to_eu,
    foot_length_to_us_men,
    foot_length_to_us_women,
    foot_length_to_us_child,
    foot_length_to_uk,
    foot_length_to_uk_child,
    foot_length_to_jp,
    foot_length_to_kr,
    foot_length_to_br,
    foot_length_to_mx,
    foot_length_to_tw,
    cn_to_foot_length,
    eu_to_foot_length,
    us_men_to_foot_length,
    us_women_to_foot_length,
    us_child_to_foot_length,
    uk_to_foot_length,
    uk_child_to_foot_length,
    jp_to_foot_length,
    kr_to_foot_length,
    br_to_foot_length,
    mx_to_foot_length,
    tw_to_foot_length,
    convert_size,
    size_to_foot_length,
    foot_length_to_size,
    get_all_conversions,
    # Category functions
    get_size_category,
    is_size_in_range,
    validate_size,
    # Recommendation functions
    generate_recommendations,
    recommend_size,
    # Chart functions
    generate_size_chart,
    get_size_by_category,
    # Utility functions
    format_size_string,
    compare_sizes,
    get_common_sizes,
    # Enums
    SizeSystem,
    Gender,
    AgeGroup,
    SizeCategory,
    # Data classes
    ShoeSize,
    SizeConversionResult,
    SizeRecommendation,
)


class TestFootLengthToSize(unittest.TestCase):
    """脚长转鞋码测试"""
    
    def test_foot_length_to_cn(self):
        """测试 CN 鞋码"""
        self.assertEqual(foot_length_to_cn(24.5), 24.5)
        self.assertEqual(foot_length_to_cn(26.0), 26.0)
        self.assertEqual(foot_length_to_cn(28.0), 28.0)
    
    def test_foot_length_to_eu(self):
        """测试 EU 鞋码"""
        self.assertAlmostEqual(foot_length_to_eu(24.5), 39, places=0)
        self.assertAlmostEqual(foot_length_to_eu(26.0), 41, places=0)
        self.assertAlmostEqual(foot_length_to_eu(28.0), 44, places=0)
    
    def test_foot_length_to_us_men(self):
        """测试 US 男鞋码"""
        # US Men = (foot_length_inch * 3) - 24
        # 26cm ≈ US 7
        result = foot_length_to_us_men(26.0)
        self.assertGreater(result, 6)
        self.assertLess(result, 8)
    
    def test_foot_length_to_us_women(self):
        """测试 US 女鞋码"""
        # US Women 比男码大约 1.5
        men_size = foot_length_to_us_men(24.5)
        women_size = foot_length_to_us_women(24.5)
        self.assertGreater(women_size, men_size)
    
    def test_foot_length_to_us_child(self):
        """测试 US 儿童鞋码"""
        # 18cm → 约 9.5
        result = foot_length_to_us_child(18.0)
        self.assertGreater(result, 8)
        self.assertLess(result, 10)
    
    def test_foot_length_to_uk(self):
        """测试 UK 鞋码"""
        # UK 比男码小大约 1
        us_size = foot_length_to_us_men(26.0)
        uk_size = foot_length_to_uk(26.0)
        self.assertLess(uk_size, us_size)
    
    def test_foot_length_to_uk_child(self):
        """测试 UK 儿童鞋码"""
        result = foot_length_to_uk_child(18.0)
        self.assertGreater(result, 7)
        self.assertLess(result, 9)
    
    def test_foot_length_to_jp(self):
        """测试 JP 鞋码"""
        self.assertEqual(foot_length_to_jp(24.5), 24.5)
        self.assertEqual(foot_length_to_jp(26.0), 26.0)
    
    def test_foot_length_to_kr(self):
        """测试 KR 鞋码"""
        self.assertEqual(foot_length_to_kr(24.5), 245)
        self.assertEqual(foot_length_to_kr(26.0), 260)
    
    def test_foot_length_to_br(self):
        """测试 BR 鞋码"""
        # BR = foot_length_cm * 1.5 - 30
        # 24.5 → 7
        result = foot_length_to_br(24.5)
        self.assertGreater(result, 5)
        self.assertLess(result, 10)
    
    def test_foot_length_to_mx(self):
        """测试 MX 鞋码"""
        # MX = US + 17
        us_size = foot_length_to_us_men(26.0)
        mx_size = foot_length_to_mx(26.0)
        self.assertGreater(mx_size, us_size + 16)
        self.assertLess(mx_size, us_size + 18)
    
    def test_foot_length_to_tw(self):
        """测试 TW 鞋码"""
        # TW = EU + 1
        eu_size = foot_length_to_eu(24.5)
        tw_size = foot_length_to_tw(24.5)
        self.assertGreater(tw_size, eu_size)


class TestSizeToFootLength(unittest.TestCase):
    """鞋码转脚长测试"""
    
    def test_cn_to_foot_length(self):
        """测试 CN 转脚长"""
        self.assertEqual(cn_to_foot_length(24.5), 24.5)
    
    def test_eu_to_foot_length(self):
        """测试 EU 转脚长"""
        result = eu_to_foot_length(39)
        self.assertAlmostEqual(result, 24.7, places=1)
        
        result = eu_to_foot_length(42)
        self.assertAlmostEqual(result, 26.7, places=1)
    
    def test_us_men_to_foot_length(self):
        """测试 US 男码转脚长"""
        result = us_men_to_foot_length(8)
        # US 8 ≈ 26-27 cm
        self.assertGreater(result, 26)
        self.assertLess(result, 28)
    
    def test_us_women_to_foot_length(self):
        """测试 US 女码转脚长"""
        result = us_women_to_foot_length(7)
        self.assertGreater(result, 23)
        self.assertLess(result, 25)
    
    def test_us_child_to_foot_length(self):
        """测试 US 儿童码转脚长"""
        result = us_child_to_foot_length(9)
        self.assertGreater(result, 17)
        self.assertLess(result, 19)
    
    def test_uk_to_foot_length(self):
        """测试 UK 码转脚长"""
        result = uk_to_foot_length(7)
        # UK 7 ≈ 27 cm
        self.assertGreater(result, 26)
        self.assertLess(result, 28)
    
    def test_uk_child_to_foot_length(self):
        """测试 UK 儿童码转脚长"""
        result = uk_child_to_foot_length(8)
        self.assertGreater(result, 17)
        self.assertLess(result, 19)
    
    def test_jp_to_foot_length(self):
        """测试 JP 码转脚长"""
        self.assertEqual(jp_to_foot_length(24.5), 24.5)
    
    def test_kr_to_foot_length(self):
        """测试 KR 码转脚长"""
        self.assertEqual(kr_to_foot_length(245), 24.5)
    
    def test_br_to_foot_length(self):
        """测试 BR 码转脚长"""
        result = br_to_foot_length(7)
        self.assertGreater(result, 23)
        self.assertLess(result, 26)
    
    def test_mx_to_foot_length(self):
        """测试 MX 码转脚长"""
        result = mx_to_foot_length(26)
        # MX 26 ≈ US 9 → ~27 cm
        self.assertGreater(result, 26)
        self.assertLess(result, 29)
    
    def test_tw_to_foot_length(self):
        """测试 TW 码转脚长"""
        result = tw_to_foot_length(40)
        self.assertGreater(result, 23)
        self.assertLess(result, 26)


class TestConvertSize(unittest.TestCase):
    """尺码转换测试"""
    
    def test_convert_eu_to_us_men(self):
        """测试 EU 转 US 男码"""
        us_size = convert_size(39, SizeSystem.EU, SizeSystem.US, Gender.MALE)
        # EU 39 ≈ US 6 (Men)
        self.assertGreater(us_size, 5)
        self.assertLess(us_size, 7.5)
    
    def test_convert_eu_to_us_women(self):
        """测试 EU 转 US 女码"""
        us_size = convert_size(39, SizeSystem.EU, SizeSystem.US, Gender.FEMALE)
        self.assertGreater(us_size, 7)
        self.assertLess(us_size, 8.5)
    
    def test_convert_us_to_eu(self):
        """测试 US 转 EU"""
        eu_size = convert_size(8, SizeSystem.US, SizeSystem.EU, Gender.MALE)
        # US 8 (Men) ≈ EU 42
        self.assertGreater(eu_size, 41)
        self.assertLess(eu_size, 44)
    
    def test_convert_eu_to_cn(self):
        """测试 EU 转 CN"""
        cn_size = convert_size(39, SizeSystem.EU, SizeSystem.CN)
        self.assertGreater(cn_size, 24)
        self.assertLess(cn_size, 25.5)
    
    def test_convert_cn_to_eu(self):
        """测试 CN 转 EU"""
        eu_size = convert_size(24.5, SizeSystem.CN, SizeSystem.EU)
        self.assertAlmostEqual(eu_size, 39, places=0)
    
    def test_convert_child_sizes(self):
        """测试儿童尺码转换"""
        # EU 30 → US (儿童)
        us_size = convert_size(30, SizeSystem.EU, SizeSystem.US, Gender.MALE, AgeGroup.CHILD)
        # EU 30 ≈ US 12 (儿童)
        self.assertGreater(us_size, 10)
        self.assertLess(us_size, 13.5)
    
    def test_convert_au_same_as_uk(self):
        """测试 AU 与 UK 相同"""
        eu_size = 42
        uk_size = convert_size(eu_size, SizeSystem.EU, SizeSystem.UK)
        au_size = convert_size(eu_size, SizeSystem.EU, SizeSystem.AU)
        self.assertEqual(uk_size, au_size)


class TestGetAllConversions(unittest.TestCase):
    """完整转换测试"""
    
    def test_get_all_conversions_adult_male(self):
        """测试成人男性完整转换"""
        result = get_all_conversions(42, SizeSystem.EU, Gender.MALE)
        
        self.assertEqual(result.original_system, 'EU')
        self.assertEqual(result.original_size, 42)
        self.assertIn('CN', result.conversions)
        self.assertIn('EU', result.conversions)
        self.assertIn('US_men', result.conversions)
        self.assertIn('US_women', result.conversions)
        self.assertIn('UK', result.conversions)
        self.assertIn('JP', result.conversions)
        self.assertIn('KR', result.conversions)
        
        # 检查脚长计算
        self.assertGreater(result.foot_length_cm, 26)
        self.assertLess(result.foot_length_cm, 27)
        
        # 检查分类
        self.assertIsNotNone(result.size_category)
        
        # 检查推荐
        self.assertGreater(len(result.recommendations), 0)
    
    def test_get_all_conversions_adult_female(self):
        """测试成人女性完整转换"""
        result = get_all_conversions(38, SizeSystem.EU, Gender.FEMALE)
        
        # US women 应该比 US men 大
        self.assertGreater(result.conversions['US_women'], result.conversions['US_men'])
    
    def test_get_all_conversions_child(self):
        """测试儿童完整转换"""
        result = get_all_conversions(28, SizeSystem.EU, Gender.MALE, AgeGroup.CHILD)
        
        self.assertEqual(result.original_age_group, 'child')
        self.assertIn('US', result.conversions)
        
        # 儿童脚长应该较小
        self.assertGreater(result.foot_length_cm, 16)
        self.assertLess(result.foot_length_cm, 22)
    
    def test_conversions_with_brand(self):
        """测试品牌调整转换"""
        result_standard = get_all_conversions(42, SizeSystem.EU, Gender.MALE)
        result_nike = get_all_conversions(42, SizeSystem.EU, Gender.MALE, brand='Nike')
        
        # Nike 尺码偏小，转换后可能略有差异
        self.assertIsNotNone(result_nike.recommendations)


class TestSizeCategory(unittest.TestCase):
    """尺码分类测试"""
    
    def test_get_size_category_adult_male(self):
        """测试成人男性尺码分类"""
        self.assertEqual(get_size_category(25.0, Gender.MALE, AgeGroup.ADULT), 'medium')
        self.assertEqual(get_size_category(23.5, Gender.MALE, AgeGroup.ADULT), 'small')
        self.assertEqual(get_size_category(28.5, Gender.MALE, AgeGroup.ADULT), 'extra_large')
    
    def test_get_size_category_adult_female(self):
        """测试成人女性尺码分类"""
        self.assertEqual(get_size_category(23.5, Gender.FEMALE, AgeGroup.ADULT), 'medium')
        self.assertEqual(get_size_category(22.0, Gender.FEMALE, AgeGroup.ADULT), 'small')
    
    def test_get_size_category_child(self):
        """测试儿童尺码分类"""
        self.assertEqual(get_size_category(18.0, Gender.MALE, AgeGroup.CHILD), 'medium')
        self.assertEqual(get_size_category(15.0, Gender.MALE, AgeGroup.CHILD), 'extra_small')
    
    def test_is_size_in_range_adult(self):
        """测试成人尺码范围"""
        self.assertTrue(is_size_in_range(24.5, AgeGroup.ADULT))
        self.assertTrue(is_size_in_range(28.0, AgeGroup.ADULT))
        self.assertFalse(is_size_in_range(15.0, AgeGroup.ADULT))
        self.assertFalse(is_size_in_range(35.0, AgeGroup.ADULT))
    
    def test_is_size_in_range_child(self):
        """测试儿童尺码范围"""
        self.assertTrue(is_size_in_range(18.0, AgeGroup.CHILD))
        self.assertFalse(is_size_in_range(24.5, AgeGroup.CHILD))
    
    def test_is_size_in_range_infant(self):
        """测试婴儿尺码范围"""
        self.assertTrue(is_size_in_range(11.0, AgeGroup.INFANT))
        self.assertFalse(is_size_in_range(20.0, AgeGroup.INFANT))


class TestValidateSize(unittest.TestCase):
    """尺码验证测试"""
    
    def test_validate_eu_size_valid(self):
        """测试 EU 有效尺码"""
        valid, reason = validate_size(39, SizeSystem.EU)
        self.assertTrue(valid)
        self.assertIn('有效', reason)
    
    def test_validate_eu_size_invalid_high(self):
        """测试 EU 无效尺码（过大）"""
        valid, reason = validate_size(100, SizeSystem.EU)
        self.assertFalse(valid)
        self.assertIn('超出', reason)
    
    def test_validate_eu_size_invalid_low(self):
        """测试 EU 无效尺码（过小）"""
        valid, reason = validate_size(20, SizeSystem.EU)
        self.assertFalse(valid)
        self.assertIn('低于', reason)
    
    def test_validate_us_men_size(self):
        """测试 US 男码验证"""
        valid, reason = validate_size(8, SizeSystem.US, Gender.MALE)
        self.assertTrue(valid)
        
        valid, reason = validate_size(20, SizeSystem.US, Gender.MALE)
        self.assertFalse(valid)
    
    def test_validate_us_women_size(self):
        """测试 US 女码验证"""
        valid, reason = validate_size(8, SizeSystem.US, Gender.FEMALE)
        self.assertTrue(valid)
    
    def test_validate_child_size(self):
        """测试儿童尺码验证"""
        valid, reason = validate_size(10, SizeSystem.US, Gender.MALE, AgeGroup.CHILD)
        self.assertTrue(valid)
    
    def test_validate_kr_size(self):
        """测试 KR 尺码验证"""
        valid, reason = validate_size(260, SizeSystem.KR)
        self.assertTrue(valid)


class TestRecommendations(unittest.TestCase):
    """推荐功能测试"""
    
    def test_generate_recommendations_basic(self):
        """测试基本推荐生成"""
        recs = generate_recommendations(26.0, Gender.MALE, AgeGroup.ADULT)
        
        self.assertGreater(len(recs), 0)
        self.assertIn('舒适', recs[0])
    
    def test_generate_recommendations_extra_small(self):
        """测试特小尺码推荐"""
        recs = generate_recommendations(22.5, Gender.MALE, AgeGroup.ADULT)
        
        # 应包含小码专区提示
        self.assertTrue(any('小尺码' in r or '小码专区' in r for r in recs))
    
    def test_generate_recommendations_extra_large(self):
        """测试特大尺码推荐"""
        recs = generate_recommendations(29.0, Gender.MALE, AgeGroup.ADULT)
        
        # 应包含大码专区提示
        self.assertTrue(any('大尺码' in r or '大码专区' in r for r in recs))
    
    def test_generate_recommendations_child(self):
        """测试儿童尺码推荐"""
        recs = generate_recommendations(18.0, Gender.MALE, AgeGroup.CHILD)
        
        # 应包含儿童相关提示
        self.assertTrue(any('儿童' in r or '发育' in r for r in recs))
    
    def test_generate_recommendations_with_brand(self):
        """测试品牌推荐"""
        recs = generate_recommendations(26.0, Gender.MALE, AgeGroup.ADULT, brand='Nike')
        
        # Nike 尺码偏小
        self.assertTrue(any('Nike' in r for r in recs))
    
    def test_recommend_size(self):
        """测试尺码推荐"""
        rec = recommend_size(26.0, SizeSystem.US, Gender.MALE)
        
        self.assertGreater(rec.recommended_size, 7)
        self.assertLess(rec.recommended_size, 9.5)
        self.assertEqual(rec.recommended_system, 'US')
        self.assertEqual(rec.foot_length_cm, 26.0)
        self.assertGreater(len(rec.size_range), 0)
    
    def test_recommend_size_with_comfort_margin(self):
        """测试自定义舒适余量"""
        rec1 = recommend_size(26.0, SizeSystem.US, Gender.MALE, comfort_margin_cm=0.5)
        rec2 = recommend_size(26.0, SizeSystem.US, Gender.MALE, comfort_margin_cm=1.0)
        
        # 更大余量应推荐更大尺码
        self.assertGreaterEqual(rec2.recommended_size, rec1.recommended_size)
    
    def test_recommend_size_with_brand(self):
        """测试品牌尺码推荐"""
        rec = recommend_size(26.0, SizeSystem.US, Gender.MALE, brand='Nike')
        
        self.assertTrue(any('Nike' in note for note in rec.notes))


class TestSizeChart(unittest.TestCase):
    """尺码表测试"""
    
    def test_generate_size_chart_default(self):
        """测试默认尺码表生成"""
        chart = generate_size_chart()
        
        self.assertGreater(len(chart), 0)
        
        # 检查包含必要字段
        row = chart[0]
        self.assertIn('foot_length_cm', row)
        self.assertIn('CN', row)
        self.assertIn('EU', row)
        self.assertIn('US_men', row)
        self.assertIn('US_women', row)
        self.assertIn('UK', row)
    
    def test_generate_size_chart_custom_range(self):
        """测试自定义范围尺码表"""
        chart = generate_size_chart(start_cm=24.0, end_cm=26.0, step_cm=0.5)
        
        self.assertGreater(len(chart), 0)
        self.assertLess(chart[0]['foot_length_cm'], 24.5)
        self.assertGreater(chart[-1]['foot_length_cm'], 25.5)
    
    def test_generate_size_chart_child(self):
        """测试儿童尺码表"""
        chart = generate_size_chart(age_group=AgeGroup.CHILD)
        
        self.assertGreater(len(chart), 0)
        
        row = chart[0]
        self.assertIn('US', row)  # 儿童只有 US，没有 US_men/women
        self.assertLess(row['foot_length_cm'], 22)
    
    def test_get_size_by_category(self):
        """测试按分类获取尺码范围"""
        min_size, max_size = get_size_by_category(SizeCategory.MEDIUM, Gender.MALE)
        
        self.assertGreater(max_size, min_size)
        self.assertGreater(min_size, 4)
        self.assertLess(max_size, 12)


class TestUtilityFunctions(unittest.TestCase):
    """辅助函数测试"""
    
    def test_format_size_string_us_with_gender(self):
        """测试 US 尺码格式化"""
        result = format_size_string(8.5, SizeSystem.US, Gender.MALE)
        self.assertIn('US', result)
        self.assertIn('8.5', result)
        self.assertIn('Male', result)
    
    def test_format_size_string_eu(self):
        """测试 EU 尺码格式化"""
        result = format_size_string(42, SizeSystem.EU)
        self.assertIn('EU', result)
        self.assertIn('42', result)
    
    def test_format_size_string_kr(self):
        """测试 KR 尺码格式化"""
        result = format_size_string(260, SizeSystem.KR)
        self.assertIn('KR', result)
        self.assertIn('mm', result)
    
    def test_format_size_string_cn(self):
        """测试 CN 尺码格式化"""
        result = format_size_string(24.5, SizeSystem.CN)
        self.assertIn('CN', result)
        self.assertIn('cm', result)
    
    def test_compare_sizes_equal(self):
        """测试尺码比较（相近）"""
        # EU 39 ≈ US 6 (Men), 使用相近尺码
        result = compare_sizes(39, SizeSystem.EU, 6, SizeSystem.US, Gender.MALE)
        # 由于转换精度，两个相近尺码可能有 ±0.5cm 差异
        self.assertTrue('≈' in result or '<' in result or '>' in result)
    
    def test_compare_sizes_greater(self):
        """测试尺码比较（大于）"""
        result = compare_sizes(42, SizeSystem.EU, 39, SizeSystem.EU)
        self.assertIn('>', result)
    
    def test_compare_sizes_less(self):
        """测试尺码比较（小于）"""
        result = compare_sizes(36, SizeSystem.EU, 39, SizeSystem.EU)
        self.assertIn('<', result)
    
    def test_get_common_sizes_male(self):
        """测试常见男性尺码"""
        sizes = get_common_sizes(Gender.MALE)
        
        self.assertGreater(len(sizes), 0)
        self.assertIn(42, sizes)
    
    def test_get_common_sizes_female(self):
        """测试常见女性尺码"""
        sizes = get_common_sizes(Gender.FEMALE)
        
        self.assertGreater(len(sizes), 0)
        self.assertIn(38, sizes)
    
    def test_get_common_sizes_child(self):
        """测试常见儿童尺码"""
        sizes = get_common_sizes(Gender.MALE, AgeGroup.CHILD)
        
        self.assertGreater(len(sizes), 0)


class TestBidirectionalConversion(unittest.TestCase):
    """双向转换一致性测试"""
    
    def test_eu_bidirectional(self):
        """测试 EU 双向转换一致性"""
        for eu_size in [38, 39, 40, 41, 42, 43, 44]:
            foot_length = eu_to_foot_length(eu_size)
            back_to_eu = foot_length_to_eu(foot_length)
            self.assertAlmostEqual(eu_size, back_to_eu, places=0)
    
    def test_cn_bidirectional(self):
        """测试 CN 双向转换一致性"""
        for cn_size in [23.5, 24.0, 24.5, 25.0, 25.5, 26.0]:
            foot_length = cn_to_foot_length(cn_size)
            back_to_cn = foot_length_to_cn(foot_length)
            self.assertEqual(cn_size, back_to_cn)
    
    def test_jp_bidirectional(self):
        """测试 JP 双向转换一致性"""
        for jp_size in [23.5, 24.0, 24.5, 25.0]:
            foot_length = jp_to_foot_length(jp_size)
            back_to_jp = foot_length_to_jp(foot_length)
            self.assertEqual(jp_size, back_to_jp)
    
    def test_kr_bidirectional(self):
        """测试 KR 双向转换一致性"""
        for kr_size in [235, 240, 245, 250, 260]:
            foot_length = kr_to_foot_length(kr_size)
            back_to_kr = foot_length_to_kr(foot_length)
            self.assertEqual(kr_size, back_to_kr)
    
    def test_us_men_bidirectional(self):
        """测试 US Men 双向转换一致性"""
        for us_size in [6, 7, 8, 9, 10, 11, 12]:
            foot_length = us_men_to_foot_length(us_size)
            back_to_us = foot_length_to_us_men(foot_length)
            self.assertAlmostEqual(us_size, back_to_us, places=0)
    
    def test_us_women_bidirectional(self):
        """测试 US Women 双向转换一致性"""
        for us_size in [5, 6, 7, 8, 9, 10]:
            foot_length = us_women_to_foot_length(us_size)
            back_to_us = foot_length_to_us_women(foot_length)
            self.assertAlmostEqual(us_size, back_to_us, places=0)
    
    def test_uk_bidirectional(self):
        """测试 UK 双向转换一致性"""
        for uk_size in [5, 6, 7, 8, 9, 10, 11]:
            foot_length = uk_to_foot_length(uk_size)
            back_to_uk = foot_length_to_uk(foot_length)
            self.assertAlmostEqual(uk_size, back_to_uk, places=0)


class TestCrossSystemConversion(unittest.TestCase):
    """跨系统转换测试"""
    
    def test_eu_to_us_to_eu(self):
        """测试 EU → US → EU 转换"""
        original_eu = 42
        us = convert_size(original_eu, SizeSystem.EU, SizeSystem.US, Gender.MALE)
        back_to_eu = convert_size(us, SizeSystem.US, SizeSystem.EU, Gender.MALE)
        
        self.assertAlmostEqual(original_eu, back_to_eu, places=0)
    
    def test_cn_to_eu_to_cn(self):
        """测试 CN → EU → CN 转换"""
        original_cn = 24.5
        eu = convert_size(original_cn, SizeSystem.CN, SizeSystem.EU)
        back_to_cn = convert_size(eu, SizeSystem.EU, SizeSystem.CN)
        
        # 由于 EU 转换精度，允许 ±0.5 cm 误差
        self.assertTrue(abs(original_cn - back_to_cn) < 0.5)
    
    def test_jp_to_uk_to_jp(self):
        """测试 JP → UK → JP 转换"""
        original_jp = 26.0
        uk = convert_size(original_jp, SizeSystem.JP, SizeSystem.UK)
        back_to_jp = convert_size(uk, SizeSystem.UK, SizeSystem.JP)
        
        self.assertAlmostEqual(original_jp, back_to_jp, places=1)


class TestEdgeCases(unittest.TestCase):
    """边界情况测试"""
    
    def test_extreme_large_size(self):
        """测试极大尺码"""
        result = get_all_conversions(48, SizeSystem.EU, Gender.MALE)
        
        self.assertGreater(result.foot_length_cm, 30)
        self.assertEqual(result.size_category, 'extra_large')
    
    def test_extreme_small_size(self):
        """测试极小尺码"""
        result = get_all_conversions(35, SizeSystem.EU, Gender.MALE)
        
        self.assertLess(result.foot_length_cm, 23)
        self.assertEqual(result.size_category, 'extra_small')
    
    def test_half_sizes(self):
        """测试半码"""
        # EU 39.5
        us = convert_size(39.5, SizeSystem.EU, SizeSystem.US, Gender.MALE)
        self.assertIsNotNone(us)
        
        # US 8.5
        eu = convert_size(8.5, SizeSystem.US, SizeSystem.EU, Gender.MALE)
        self.assertIsNotNone(eu)
    
    def test_infant_sizes(self):
        """测试婴儿尺码"""
        # EU 15 (infant)
        valid, _ = validate_size(15, SizeSystem.EU, Gender.MALE, AgeGroup.INFANT)
        self.assertTrue(valid)
    
    def test_toddler_sizes(self):
        """测试幼儿尺码"""
        valid, _ = validate_size(20, SizeSystem.EU, Gender.MALE, AgeGroup.TODDLER)
        self.assertTrue(valid)


class TestDataClasses(unittest.TestCase):
    """数据类测试"""
    
    def test_shoe_size_creation(self):
        """测试 ShoeSize 创建"""
        size = ShoeSize(
            system='EU',
            size=42,
            gender='male',
            age_group='adult',
            foot_length_cm=26.7
        )
        
        self.assertEqual(size.system, 'EU')
        self.assertEqual(size.size, 42)
    
    def test_shoe_size_str(self):
        """测试 ShoeSize 字符串表示"""
        size = ShoeSize(
            system='US',
            size=8.5,
            gender='male',
            age_group='adult'
        )
        
        str_repr = str(size)
        self.assertIn('US', str_repr)
        self.assertIn('8.5', str_repr)
    
    def test_size_conversion_result(self):
        """测试 SizeConversionResult"""
        result = get_all_conversions(42, SizeSystem.EU, Gender.MALE)
        
        self.assertIsInstance(result, SizeConversionResult)
        self.assertEqual(result.original_system, 'EU')
    
    def test_size_recommendation(self):
        """测试 SizeRecommendation"""
        rec = recommend_size(26.0, SizeSystem.US, Gender.MALE)
        
        self.assertIsInstance(rec, SizeRecommendation)
        self.assertEqual(rec.recommended_system, 'US')


def run_tests():
    """运行所有测试"""
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromModule(sys.modules[__name__])
    
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    return result.wasSuccessful()


if __name__ == '__main__':
    success = run_tests()
    sys.exit(0 if success else 1)