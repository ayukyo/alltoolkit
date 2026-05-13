#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AllToolkit - Nutrition Utilities Test Module
==============================================
Unit tests for nutrition_utils module.
"""

import unittest
from mod import (
    get_food_info,
    search_foods,
    get_foods_by_category,
    calculate_food_nutrition,
    calculate_meal_nutrition,
    calculate_calories_from_macros,
    calculate_macros_from_calories,
    calculate_bmr,
    calculate_tdee,
    calculate_daily_needs,
    calculate_protein_needs,
    analyze_nutrition,
    get_meal_suggestion,
    get_all_foods,
    get_all_categories,
    format_nutrition_label,
    format_meal_summary,
    ActivityLevel,
    Goal,
    Gender,
    FoodItem,
    NutritionSummary,
    DailyNeeds,
    NutrientAnalysis,
)


class TestFoodDatabase(unittest.TestCase):
    """测试食物数据库功能"""
    
    def test_get_food_info_exists(self):
        """测试获取存在的食物"""
        info = get_food_info('米饭')
        self.assertIsNotNone(info)
        self.assertIn('calories', info)
        self.assertIn('protein', info)
        self.assertEqual(info['calories'], 116)
    
    def test_get_food_info_not_exists(self):
        """测试获取不存在的食物"""
        info = get_food_info('不存在')
        self.assertIsNone(info)
    
    def test_search_foods_basic(self):
        """测试基本食物搜索"""
        results = search_foods('鸡')
        self.assertTrue(len(results) > 0)
        self.assertIn('鸡胸肉', results)
    
    def test_search_foods_limit(self):
        """测试搜索结果数量限制"""
        results = search_foods('a', limit=3)
        self.assertTrue(len(results) <= 3)
    
    def test_get_foods_by_category(self):
        """测试按分类获取食物"""
        meat_foods = get_foods_by_category('meat')
        self.assertTrue(len(meat_foods) > 0)
        self.assertIn('鸡胸肉', meat_foods)
    
    def test_get_all_foods(self):
        """测试获取所有食物"""
        foods = get_all_foods()
        self.assertTrue(len(foods) > 50)
    
    def test_get_all_categories(self):
        """测试获取所有分类"""
        categories = get_all_categories()
        self.assertIn('meat', categories)
        self.assertIn('vegetables', categories)


class TestFoodNutritionCalculation(unittest.TestCase):
    """测试食物营养计算"""
    
    def test_calculate_food_nutrition_basic(self):
        """测试基本食物营养计算"""
        item = calculate_food_nutrition('米饭', 100)
        self.assertIsNotNone(item)
        self.assertEqual(item.name, '米饭')
        self.assertEqual(item.amount, 100)
        self.assertEqual(item.calories, 116)
        self.assertEqual(item.protein, 2.6)
    
    def test_calculate_food_nutrition_multiplier(self):
        """测试不同数量的营养计算"""
        item_200 = calculate_food_nutrition('米饭', 200)
        self.assertIsNotNone(item_200)
        self.assertEqual(item_200.calories, 232)  # 116 * 2
        self.assertEqual(item_200.protein, 5.2)   # 2.6 * 2
    
    def test_calculate_food_nutrition_not_exists(self):
        """测试不存在的食物"""
        item = calculate_food_nutrition('不存在', 100)
        self.assertIsNone(item)
    
    def test_calculate_food_nutrition_zero_amount(self):
        """测试零数量"""
        item = calculate_food_nutrition('米饭', 0)
        self.assertIsNotNone(item)
        self.assertEqual(item.calories, 0)


class TestMealNutrition(unittest.TestCase):
    """测试餐饮营养计算"""
    
    def test_calculate_meal_nutrition_single(self):
        """测试单一食物餐饮"""
        summary = calculate_meal_nutrition([('米饭', 100)])
        self.assertEqual(summary.food_count, 1)
        self.assertEqual(summary.total_calories, 116)
    
    def test_calculate_meal_nutrition_multiple(self):
        """测试多食物餐饮"""
        foods = [('米饭', 200), ('鸡胸肉', 100)]
        summary = calculate_meal_nutrition(foods)
        self.assertEqual(summary.food_count, 2)
        # 米饭 232 kcal + 鸡胸肉 165 kcal = 397 kcal
        self.assertAlmostEqual(summary.total_calories, 397, places=0)
    
    def test_calculate_meal_nutrition_ratios(self):
        """测试营养比例计算"""
        foods = [('鸡胸肉', 200), ('米饭', 100)]
        summary = calculate_meal_nutrition(foods)
        # 验证比例在合理范围
        self.assertTrue(summary.protein_ratio > 0)
        self.assertTrue(summary.carbs_ratio > 0)
        self.assertTrue(summary.fat_ratio > 0)
        # 总比例应该接近 100%
        total_ratio = summary.protein_ratio + summary.carbs_ratio + summary.fat_ratio
        self.assertAlmostEqual(total_ratio, 100, places=0)
    
    def test_calculate_meal_nutrition_empty(self):
        """测试空餐饮"""
        summary = calculate_meal_nutrition([])
        self.assertEqual(summary.food_count, 0)
        self.assertEqual(summary.total_calories, 0)


class TestMacroCalculations(unittest.TestCase):
    """测试宏量营养素计算"""
    
    def test_calculate_calories_from_macros(self):
        """测试从宏量营养素计算热量"""
        calories = calculate_calories_from_macros(30, 50, 20)
        # 30*4 + 50*4 + 20*9 = 120 + 200 + 180 = 500
        self.assertEqual(calories, 500)
    
    def test_calculate_macros_from_calories_default(self):
        """测试从热量计算宏量营养素（默认比例）"""
        protein, carbs, fat = calculate_macros_from_calories(2000)
        # 30% protein: 600/4 = 150g
        # 40% carbs: 800/4 = 200g
        # 30% fat: 600/9 = 66.7g
        self.assertEqual(protein, 150.0)
        self.assertEqual(carbs, 200.0)
        self.assertAlmostEqual(fat, 66.7, places=1)
    
    def test_calculate_macros_from_calories_custom(self):
        """测试自定义比例"""
        protein, carbs, fat = calculate_macros_from_calories(
            2000, 0.25, 0.50, 0.25
        )
        self.assertEqual(protein, 125.0)
        self.assertEqual(carbs, 250.0)
        self.assertAlmostEqual(fat, 55.6, places=1)


class TestBMRCalculations(unittest.TestCase):
    """测试基础代谢率计算"""
    
    def test_calculate_bmr_male(self):
        """测试男性 BMR"""
        bmr = calculate_bmr(70, 175, 30, Gender.MALE)
        # (10 * 70) + (6.25 * 175) - (5 * 30) + 5 = 700 + 1093.75 - 150 + 5 = 1648.75
        self.assertAlmostEqual(bmr, 1649, places=0)
    
    def test_calculate_bmr_female(self):
        """测试女性 BMR"""
        bmr = calculate_bmr(60, 165, 25, Gender.FEMALE)
        # (10 * 60) + (6.25 * 165) - (5 * 25) - 161 = 600 + 1031.25 - 125 - 161 = 1345.25
        self.assertAlmostEqual(bmr, 1345, places=0)
    
    def test_calculate_tdee(self):
        """测试 TDEE 计算"""
        bmr = 1700
        tdee = calculate_tdee(bmr, ActivityLevel.MODERATE)
        # 1700 * 1.55 = 2635
        self.assertEqual(tdee, 2635)


class TestDailyNeeds(unittest.TestCase):
    """测试每日营养需求计算"""
    
    def test_calculate_daily_needs_maintain(self):
        """测试维持期需求"""
        needs = calculate_daily_needs(
            70, 175, 30, Gender.MALE, 
            ActivityLevel.MODERATE, Goal.MAINTAIN
        )
        self.assertTrue(needs.calories > 2000)
        self.assertTrue(needs.protein > 100)
    
    def test_calculate_daily_needs_weight_loss(self):
        """测试减脂期需求"""
        needs_maintain = calculate_daily_needs(
            70, 175, 30, Gender.MALE,
            ActivityLevel.MODERATE, Goal.MAINTAIN
        )
        needs_loss = calculate_daily_needs(
            70, 175, 30, Gender.MALE,
            ActivityLevel.MODERATE, Goal.LOSE_WEIGHT
        )
        # 减脂期热量应该低于维持期
        self.assertTrue(needs_loss.calories < needs_maintain.calories)
    
    def test_calculate_daily_needs_gain_muscle(self):
        """测试增肌期需求"""
        needs_maintain = calculate_daily_needs(
            70, 175, 30, Gender.MALE,
            ActivityLevel.MODERATE, Goal.MAINTAIN
        )
        needs_gain = calculate_daily_needs(
            70, 175, 30, Gender.MALE,
            ActivityLevel.MODERATE, Goal.GAIN_MUSCLE
        )
        # 增肌期热量应该高于维持期
        self.assertTrue(needs_gain.calories > needs_maintain.calories)
    
    def test_calculate_protein_needs(self):
        """测试蛋白质需求计算"""
        protein = calculate_protein_needs(70, ActivityLevel.ACTIVE, Goal.GAIN_MUSCLE)
        # Active: 1.6g/kg, 增肌调整: * 1.2 = 134.4
        self.assertTrue(protein > 100)


class TestNutrientAnalysis(unittest.TestCase):
    """测试营养分析"""
    
    def test_analyze_nutrition_basic(self):
        """测试基本营养分析"""
        needs = calculate_daily_needs(70, 175, 30, Gender.MALE)
        foods = [('米饭', 200), ('鸡胸肉', 150)]
        analysis = analyze_nutrition(foods, needs)
        
        self.assertTrue(analysis.calories_percent > 0)
        self.assertTrue(analysis.protein_percent > 0)
        self.assertTrue(len(analysis.recommendations) > 0)
    
    def test_analyze_nutrition_under_target(self):
        """测试摄入不足情况"""
        needs = calculate_daily_needs(70, 175, 30, Gender.MALE, ActivityLevel.ACTIVE)
        foods = [('米饭', 50)]  # 少量食物
        analysis = analyze_nutrition(foods, needs)
        
        # 应该有不足的建议
        self.assertTrue(analysis.calories_percent < 50)
    
    def test_analyze_nutrition_balance_score(self):
        """测试营养平衡分数"""
        needs = calculate_daily_needs(70, 175, 30, Gender.MALE)
        foods = [('鸡胸肉', 200), ('米饭', 200), ('西兰花', 100)]
        analysis = analyze_nutrition(foods, needs)
        
        # 分数应该在合理范围
        self.assertTrue(0 <= analysis.balance_score <= 100)


class TestMealSuggestions(unittest.TestCase):
    """测试饮食建议"""
    
    def test_get_meal_suggestion_basic(self):
        """测试基本饮食建议"""
        suggestions = get_meal_suggestion(500, 30)
        self.assertTrue(len(suggestions) > 0)
        
        # 计算建议食物的总热量
        summary = calculate_meal_nutrition(suggestions)
        # 应该接近目标热量
        self.assertTrue(summary.total_calories > 300)
    
    def test_get_meal_suggestion_high_protein(self):
        """测试高蛋白建议"""
        suggestions = get_meal_suggestion(600, 50)
        summary = calculate_meal_nutrition(suggestions)
        # 应包含较多蛋白质
        self.assertTrue(summary.total_protein > 30)


class TestFormatting(unittest.TestCase):
    """测试格式化输出"""
    
    def test_format_nutrition_label(self):
        """测试营养标签格式化"""
        label = format_nutrition_label('鸡胸肉', 100)
        self.assertIn('鸡胸肉', label)
        self.assertIn('165', label)  # 热量值
        self.assertIn('31.0g', label)
    
    def test_format_nutrition_label_not_exists(self):
        """测试不存在食物的格式化"""
        label = format_nutrition_label('不存在', 100)
        self.assertIn('未找到', label)
    
    def test_format_meal_summary(self):
        """测试餐饮摘要格式化"""
        foods = [('米饭', 100), ('鸡胸肉', 100)]
        summary = format_meal_summary(foods)
        self.assertIn('餐饮营养摘要', summary)
        self.assertIn('米饭', summary)
        self.assertIn('鸡胸肉', summary)


class TestDataClasses(unittest.TestCase):
    """测试数据类"""
    
    def test_food_item(self):
        """测试 FoodItem 数据类"""
        item = FoodItem(
            name='test',
            amount=100,
            calories=100,
            protein=10,
            carbs=20,
            fat=5,
            fiber=2,
            category='test'
        )
        self.assertEqual(item.name, 'test')
        self.assertEqual(item.calories, 100)
    
    def test_nutrition_summary(self):
        """测试 NutritionSummary 数据类"""
        summary = NutritionSummary(
            total_calories=1000,
            total_protein=50,
            total_carbs=100,
            total_fat=30,
            total_fiber=10,
            protein_calories=200,
            carbs_calories=400,
            fat_calories=270,
            protein_ratio=25.0,
            carbs_ratio=50.0,
            fat_ratio=25.0,
            food_count=3,
            food_items=[]
        )
        self.assertEqual(summary.total_calories, 1000)


class TestEdgeCases(unittest.TestCase):
    """测试边缘情况"""
    
    def test_empty_food_list(self):
        """测试空食物列表"""
        summary = calculate_meal_nutrition([])
        self.assertEqual(summary.total_calories, 0)
    
    def test_nonexistent_food_in_meal(self):
        """测试餐饮中包含不存在的食物"""
        summary = calculate_meal_nutrition([('不存在', 100), ('米饭', 100)])
        # 应忽略不存在的食物
        self.assertEqual(summary.food_count, 1)
    
    def test_very_small_amount(self):
        """测试极小数量"""
        item = calculate_food_nutrition('米饭', 1)
        self.assertAlmostEqual(item.calories, 1.16, places=1)
    
    def test_very_large_amount(self):
        """测试极大数量"""
        item = calculate_food_nutrition('米饭', 10000)
        self.assertEqual(item.calories, 11600)


def run_tests():
    """运行所有测试"""
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromModule(__import__(__name__))
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    return result.wasSuccessful()


if __name__ == '__main__':
    success = run_tests()
    print(f"\n{'=' * 60}")
    print(f"Tests {'PASSED' if success else 'FAILED'}")
    print(f"{'=' * 60}")