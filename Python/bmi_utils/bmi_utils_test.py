#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AllToolkit - BMI Utilities Test Suite
======================================
Comprehensive tests for the bmi_utils module.

Author: AllToolkit Contributors
License: MIT
"""

import unittest
import sys
import os

# Add module path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from bmi_utils.mod import (
    calculate_bmi,
    get_bmi_category,
    get_bmi_category_info,
    calculate_bmi_prime,
    calculate_ideal_weight_range,
    calculate_weight_difference,
    calculate_full_bmi,
    estimate_body_fat_bmi,
    estimate_body_fat_bmi_alternative,
    get_body_fat_category,
    estimate_full_body_fat,
    calculate_child_bmi_percentile,
    get_child_bmi_category,
    calculate_child_full_bmi,
    calculate_bmr_mifflin,
    calculate_bmr_harris_benedict,
    calculate_tdee,
    calculate_full_bmr,
    calculate_waist_height_ratio,
    get_waist_height_category,
    calculate_weight_recommendation,
    convert_weight,
    convert_height,
    get_bmi_summary,
    UnitSystem,
    Gender,
    RiskLevel,
)


class TestBMICalculation(unittest.TestCase):
    """BMI 计算核心功能测试"""
    
    def test_calculate_bmi_metric(self):
        """测试 metric 单位 BMI 计算"""
        # 正常体重
        bmi = calculate_bmi(70, 1.75)
        self.assertAlmostEqual(bmi, 22.86, places=1)
        
        # 偏瘦
        bmi = calculate_bmi(50, 1.75)
        self.assertAlmostEqual(bmi, 16.33, places=1)
        
        # 超重
        bmi = calculate_bmi(90, 1.75)
        self.assertAlmostEqual(bmi, 29.39, places=1)
        
        # 肥胖
        bmi = calculate_bmi(100, 1.75)
        self.assertAlmostEqual(bmi, 32.65, places=1)
    
    def test_calculate_bmi_imperial(self):
        """测试 imperial 单位 BMI 计算"""
        # 154 lb, 5'10" ≈ 70 kg, 1.78 m
        bmi = calculate_bmi(154, 5, UnitSystem.IMPERIAL, 10)
        self.assertAlmostEqual(bmi, 22.0, places=0)
        
        # 无额外英寸
        bmi = calculate_bmi(180, 6, UnitSystem.IMPERIAL)
        self.assertAlmostEqual(bmi, 24.5, places=0)
    
    def test_calculate_bmi_edge_cases(self):
        """测试边界情况"""
        # 非常高的人
        bmi = calculate_bmi(100, 2.0)
        self.assertAlmostEqual(bmi, 25.0, places=1)
        
        # 非常轻的人
        bmi = calculate_bmi(40, 1.60)
        self.assertAlmostEqual(bmi, 15.62, places=1)
    
    def test_calculate_bmi_invalid_inputs(self):
        """测试无效输入"""
        # 零体重
        with self.assertRaises(ValueError):
            calculate_bmi(0, 1.75)
        
        # 零身高
        with self.assertRaises(ValueError):
            calculate_bmi(70, 0)
        
        # 负体重
        with self.assertRaises(ValueError):
            calculate_bmi(-70, 1.75)
        
        # 负身高
        with self.assertRaises(ValueError):
            calculate_bmi(70, -1.75)


class TestBMICategory(unittest.TestCase):
    """BMI 分类测试"""
    
    def test_get_bmi_category(self):
        """测试 BMI 分类获取"""
        self.assertEqual(get_bmi_category(15.0), 'severe_underweight')
        self.assertEqual(get_bmi_category(17.0), 'underweight')
        self.assertEqual(get_bmi_category(22.0), 'normal')
        self.assertEqual(get_bmi_category(27.0), 'overweight')
        self.assertEqual(get_bmi_category(32.0), 'obese_class_I')
        self.assertEqual(get_bmi_category(37.0), 'obese_class_II')
        self.assertEqual(get_bmi_category(45.0), 'obese_class_III')
    
    def test_get_bmi_category_boundary(self):
        """测试分类边界值"""
        # 精确边界
        self.assertEqual(get_bmi_category(16.0), 'underweight')
        self.assertEqual(get_bmi_category(18.5), 'normal')
        self.assertEqual(get_bmi_category(25.0), 'overweight')
        self.assertEqual(get_bmi_category(30.0), 'obese_class_I')
        self.assertEqual(get_bmi_category(35.0), 'obese_class_II')
        self.assertEqual(get_bmi_category(40.0), 'obese_class_III')
    
    def test_get_bmi_category_info(self):
        """测试分类详细信息"""
        category, label, label_en, risk_desc = get_bmi_category_info(22.0)
        self.assertEqual(category, 'normal')
        self.assertEqual(label, '正常')
        self.assertEqual(label_en, 'Normal')
        self.assertIn('健康', risk_desc)


class TestBMIPrime(unittest.TestCase):
    """BMI Prime 计算测试"""
    
    def test_calculate_bmi_prime(self):
        """测试 BMI Prime 计算"""
        self.assertAlmostEqual(calculate_bmi_prime(18.5), 0.74, places=2)
        self.assertAlmostEqual(calculate_bmi_prime(22.5), 0.90, places=2)
        self.assertAlmostEqual(calculate_bmi_prime(25.0), 1.00, places=2)
        self.assertAlmostEqual(calculate_bmi_prime(30.0), 1.20, places=2)


class TestIdealWeightRange(unittest.TestCase):
    """理想体重范围计算测试"""
    
    def test_calculate_ideal_weight_range_metric(self):
        """测试 metric 单位理想体重范围"""
        min_w, max_w = calculate_ideal_weight_range(1.75)
        # BMI 18.5-25 for 1.75m: min = 18.5 * 3.0625 = 56.6, max = 25 * 3.0625 = 76.6
        self.assertAlmostEqual(min_w, 56.6, places=0)
        self.assertAlmostEqual(max_w, 76.6, places=0)
    
    def test_calculate_ideal_weight_range_imperial(self):
        """测试 imperial 单位理想体重范围"""
        min_w, max_w = calculate_ideal_weight_range(5, UnitSystem.IMPERIAL, 10)
        # 5'10" ≈ 1.78 m
        self.assertGreater(min_w, 100)  # lb
        self.assertLess(max_w, 180)     # lb
    
    def test_ideal_weight_range_various_heights(self):
        """测试不同身高"""
        # 矮个子
        min_w, max_w = calculate_ideal_weight_range(1.50)
        self.assertGreater(min_w, 40)
        self.assertLess(max_w, 60)
        
        # 高个子
        min_w, max_w = calculate_ideal_weight_range(1.90)
        self.assertGreater(min_w, 65)
        self.assertLess(max_w, 95)


class TestWeightDifference(unittest.TestCase):
    """体重差距计算测试"""
    
    def test_calculate_weight_difference_normal(self):
        """测试正常范围体重"""
        diff, status = calculate_weight_difference(70, 1.75)
        self.assertEqual(diff, 0.0)
        self.assertEqual(status, 'normal')
    
    def test_calculate_weight_difference_underweight(self):
        """测试偏瘦体重"""
        diff, status = calculate_weight_difference(50, 1.75)
        self.assertGreater(diff, 0)
        self.assertEqual(status, 'under')
    
    def test_calculate_weight_difference_overweight(self):
        """测试超重体重"""
        diff, status = calculate_weight_difference(90, 1.75)
        self.assertGreater(diff, 0)
        self.assertEqual(status, 'over')


class TestFullBMI(unittest.TestCase):
    """完整 BMI 计算测试"""
    
    def test_calculate_full_bmi(self):
        """测试完整 BMI 计算"""
        result = calculate_full_bmi(70, 1.75)
        
        self.assertAlmostEqual(result.bmi, 22.86, places=1)
        self.assertEqual(result.category, 'normal')
        self.assertEqual(result.category_label, '正常')
        self.assertEqual(result.risk_level, 'low')
        self.assertAlmostEqual(result.bmi_prime, 0.91, places=2)
        self.assertEqual(result.weight_status, 'normal')
    
    def test_calculate_full_bmi_obese(self):
        """测试肥胖情况"""
        result = calculate_full_bmi(100, 1.75)
        
        self.assertGreater(result.bmi, 30)
        self.assertIn('obese', result.category)
        self.assertIn('high', result.risk_level)


class TestBodyFatEstimation(unittest.TestCase):
    """体脂率估算测试"""
    
    def test_estimate_body_fat_bmi_male(self):
        """测试男性体脂率估算"""
        # 30岁男性，BMI 25
        fat = estimate_body_fat_bmi(25.0, 30, Gender.MALE)
        self.assertGreater(fat, 15)
        self.assertLess(fat, 30)
    
    def test_estimate_body_fat_bmi_female(self):
        """测试女性体脂率估算"""
        # 30岁女性，BMI 25
        fat = estimate_body_fat_bmi(25.0, 30, Gender.FEMALE)
        self.assertGreater(fat, 20)
        self.assertLess(fat, 35)
    
    def test_body_fat_gender_difference(self):
        """测试性别差异"""
        male_fat = estimate_body_fat_bmi(25.0, 30, Gender.MALE)
        female_fat = estimate_body_fat_bmi(25.0, 30, Gender.FEMALE)
        
        # 女性体脂率通常高于男性
        self.assertGreater(female_fat, male_fat)
    
    def test_estimate_body_fat_alternative(self):
        """测试替代公式"""
        fat1 = estimate_body_fat_bmi(25.0, 30, Gender.MALE)
        fat2 = estimate_body_fat_bmi_alternative(25.0, 30, Gender.MALE)
        
        # 两种公式结果应相近
        self.assertLess(abs(fat1 - fat2), 5)
    
    def test_get_body_fat_category(self):
        """测试体脂分类"""
        # 健美水平
        cat, label = get_body_fat_category(15.0, Gender.MALE, 30)
        self.assertEqual(cat, 'fitness')
        
        # 运动员水平
        cat, label = get_body_fat_category(12.0, Gender.MALE, 25)
        self.assertEqual(cat, 'athletes')
    
    def test_estimate_full_body_fat(self):
        """测试完整体脂估算"""
        result = estimate_full_body_fat(25.0, 30, Gender.MALE)
        
        self.assertGreater(result.body_fat_percent, 0)
        self.assertEqual(result.method, 'deurenberg')
        self.assertIsNotNone(result.healthy_range)


class TestChildBMI(unittest.TestCase):
    """儿童 BMI 计算测试"""
    
    def test_calculate_child_bmi_percentile(self):
        """测试儿童 BMI 百分位数"""
        # 10岁男孩，BMI 18
        percentile = calculate_child_bmi_percentile(18.0, 10, Gender.MALE)
        self.assertGreater(percentile, 50)
        self.assertLess(percentile, 95)
        
        # 低 BMI
        percentile = calculate_child_bmi_percentile(14.0, 10, Gender.MALE)
        self.assertLess(percentile, 50)
    
    def test_calculate_child_bmi_percentile_invalid_age(self):
        """测试无效年龄"""
        with self.assertRaises(ValueError):
            calculate_child_bmi_percentile(18.0, 1, Gender.MALE)
        
        with self.assertRaises(ValueError):
            calculate_child_bmi_percentile(18.0, 25, Gender.MALE)
    
    def test_get_child_bmi_category(self):
        """测试儿童 BMI 分类"""
        # 正常范围
        cat, label, label_en, risk = get_child_bmi_category(50)
        self.assertEqual(cat, 'normal')
        
        # 偏瘦
        cat, label, label_en, risk = get_child_bmi_category(3)
        self.assertEqual(cat, 'underweight')
        
        # 超重
        cat, label, label_en, risk = get_child_bmi_category(90)
        self.assertEqual(cat, 'overweight')
        
        # 肥胖
        cat, label, label_en, risk = get_child_bmi_category(97)
        self.assertEqual(cat, 'obese')
    
    def test_calculate_child_full_bmi(self):
        """测试完整儿童 BMI 计算"""
        result = calculate_child_full_bmi(35, 1.4, 10, Gender.MALE)
        
        self.assertGreater(result.bmi, 0)
        self.assertGreater(result.percentile, 0)
        self.assertIsNotNone(result.percentile_category)


class TestBMR(unittest.TestCase):
    """基础代谢率测试"""
    
    def test_calculate_bmr_mifflin_male(self):
        """测试男性 Mifflin 公式"""
        # 70kg, 175cm, 30岁男性
        bmr = calculate_bmr_mifflin(70, 1.75, 30, Gender.MALE)
        self.assertGreater(bmr, 1500)
        self.assertLess(bmr, 2000)
    
    def test_calculate_bmr_mifflin_female(self):
        """测试女性 Mifflin 公式"""
        # 60kg, 165cm, 30岁女性
        bmr = calculate_bmr_mifflin(60, 1.65, 30, Gender.FEMALE)
        self.assertGreater(bmr, 1200)
        self.assertLess(bmr, 1600)
    
    def test_bmr_gender_difference(self):
        """测试 BMR 性别差异"""
        male_bmr = calculate_bmr_mifflin(70, 1.75, 30, Gender.MALE)
        female_bmr = calculate_bmr_mifflin(70, 1.75, 30, Gender.FEMALE)
        
        # 男性 BMR 通常高于女性
        self.assertGreater(male_bmr, female_bmr)
    
    def test_calculate_bmr_harris_benedict(self):
        """测试 Harris-Benedict 公式"""
        bmr = calculate_bmr_harris_benedict(70, 1.75, 30, Gender.MALE)
        self.assertGreater(bmr, 1500)
        self.assertLess(bmr, 2000)
    
    def test_calculate_tdee(self):
        """测试 TDEE 计算"""
        bmr = 1700
        
        # 久坐
        tdee = calculate_tdee(bmr, 'sedentary')
        self.assertAlmostEqual(tdee, bmr * 1.2, places=0)
        
        # 中度活动
        tdee = calculate_tdee(bmr, 'moderate')
        self.assertAlmostEqual(tdee, bmr * 1.55, places=0)
        
        # 高度活动
        tdee = calculate_tdee(bmr, 'very_active')
        self.assertAlmostEqual(tdee, bmr * 1.9, places=0)
    
    def test_calculate_full_bmr(self):
        """测试完整 BMR 计算"""
        result = calculate_full_bmr(70, 1.75, 30, Gender.MALE, 'moderate')
        
        self.assertGreater(result.bmr, 0)
        self.assertGreater(result.tdee, result.bmr)
        self.assertEqual(result.method, 'mifflin')


class TestWaistHeightRatio(unittest.TestCase):
    """腰围身高比测试"""
    
    def test_calculate_waist_height_ratio(self):
        """测试 WHtR 计算"""
        ratio = calculate_waist_height_ratio(80, 175)
        self.assertAlmostEqual(ratio, 0.46, places=2)
        
        ratio = calculate_waist_height_ratio(90, 180)
        self.assertAlmostEqual(ratio, 0.50, places=2)
    
    def test_get_waist_height_category(self):
        """测试 WHtR 分类"""
        # 健康
        cat, label, advice = get_waist_height_category(0.45, Gender.MALE)
        self.assertEqual(cat, 'healthy')
        
        # 风险增加
        cat, label, advice = get_waist_height_category(0.55, Gender.MALE)
        self.assertEqual(cat, 'increased_risk')
        
        # 高风险
        cat, label, advice = get_waist_height_category(0.65, Gender.MALE)
        self.assertEqual(cat, 'high_risk')


class TestWeightRecommendation(unittest.TestCase):
    """减重建议测试"""
    
    def test_calculate_weight_recommendation_overweight(self):
        """测试超重者减重建议"""
        rec = calculate_weight_recommendation(80, 1.75)
        
        self.assertLess(rec['target_weight'], 80)
        self.assertLess(rec['weight_change'], 0)
        self.assertEqual(rec['recommendation'], '减重')
    
    def test_calculate_weight_recommendation_normal(self):
        """测试正常体重建议"""
        rec = calculate_weight_recommendation(70, 1.75)
        
        # 应接近目标
        self.assertAlmostEqual(rec['target_weight'], 67.4, places=0)
    
    def test_calculate_weight_recommendation_underweight(self):
        """测试偏瘦者增重建议"""
        rec = calculate_weight_recommendation(50, 1.75)
        
        self.assertGreater(rec['target_weight'], 50)
        self.assertGreater(rec['weight_change'], 0)
        self.assertEqual(rec['recommendation'], '增重')


class TestUnitConversion(unittest.TestCase):
    """单位转换测试"""
    
    def test_convert_weight_kg_to_lb(self):
        """测试 kg 转 lb"""
        lb = convert_weight(70, UnitSystem.METRIC, UnitSystem.IMPERIAL)
        self.assertAlmostEqual(lb, 154.32, places=1)
    
    def test_convert_weight_lb_to_kg(self):
        """测试 lb 转 kg"""
        kg = convert_weight(154.32, UnitSystem.IMPERIAL, UnitSystem.METRIC)
        self.assertAlmostEqual(kg, 70, places=0)
    
    def test_convert_weight_same_system(self):
        """测试同系统转换"""
        kg = convert_weight(70, UnitSystem.METRIC, UnitSystem.METRIC)
        self.assertEqual(kg, 70)
    
    def test_convert_height_m_to_ft_in(self):
        """测试 m 转 ft, in"""
        ft, in_ = convert_height(1.75, UnitSystem.METRIC, UnitSystem.IMPERIAL)
        self.assertEqual(ft, 5)
        self.assertEqual(in_, 9)
    
    def test_convert_height_ft_in_to_m(self):
        """测试 ft, in 转 m"""
        m = convert_height(5, UnitSystem.IMPERIAL, UnitSystem.METRIC, 9)
        self.assertAlmostEqual(m, 1.75, places=2)


class TestUtilityFunctions(unittest.TestCase):
    """辅助函数测试"""
    
    def test_get_bmi_summary(self):
        """测试 BMI 概要"""
        summary = get_bmi_summary(22.5)
        self.assertIn('22.5', summary)
        self.assertIn('正常', summary)
        
        summary = get_bmi_summary(30.0)
        self.assertIn('30', summary)
        self.assertIn('肥胖', summary)


class TestEdgeCases(unittest.TestCase):
    """边界情况测试"""
    
    def test_extreme_height(self):
        """测试极端身高"""
        # 矮个子
        bmi = calculate_bmi(40, 1.20)
        self.assertAlmostEqual(bmi, 27.78, places=1)
        
        # 高个子
        bmi = calculate_bmi(100, 2.10)
        self.assertAlmostEqual(bmi, 22.68, places=1)
    
    def test_extreme_weight(self):
        """测试极端体重"""
        # 极轻
        bmi = calculate_bmi(30, 1.60)
        self.assertAlmostEqual(bmi, 11.72, places=1)
        self.assertEqual(get_bmi_category(bmi), 'severe_underweight')
        
        # 极重
        bmi = calculate_bmi(150, 1.80)
        self.assertAlmostEqual(bmi, 46.30, places=1)
        self.assertEqual(get_bmi_category(bmi), 'obese_class_III')
    
    def test_age_boundaries_for_body_fat(self):
        """测试体脂估算年龄边界"""
        # 年轻
        young_fat = estimate_body_fat_bmi(25, 20, Gender.MALE)
        
        # 年长
        old_fat = estimate_body_fat_bmi(25, 60, Gender.MALE)
        
        # 年龄越大体脂越高
        self.assertGreater(old_fat, young_fat)


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