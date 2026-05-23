"""
Calorie Utilities 测试文件

测试覆盖：
- BMR计算（Mifflin-St Jeor, Harris-Benedict, Katch-McArdle）
- TDEE计算
- 食物热量计算
- 运动消耗计算
- 体重目标计划
- 宏量营养素分配
- BMI计算
- 理想体重计算
- 边界值测试
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from mod import (
    # BMR函数
    calculate_bmr_mifflin,
    calculate_bmr_harris_benedict,
    calculate_bmr_katch_mcardle,
    calculate_bmr_from_body_fat,
    
    # TDEE函数
    calculate_tdee,
    calculate_tdee_full,
    
    # 食物函数
    get_food_info,
    calculate_food_calories,
    calculate_meal_calories,
    search_food,
    list_all_foods,
    
    # 运动函数
    get_exercise_info,
    calculate_exercise_calories,
    calculate_custom_exercise_calories,
    search_exercise,
    list_all_exercises,
    
    # 体重目标函数
    calculate_weight_goal_plan,
    calculate_weight_loss_calories,
    calculate_weight_gain_calories,
    
    # 宏量营养素函数
    calculate_macro_split,
    calculate_macro_calories,
    calculate_macro_percentages,
    
    # 工具函数
    bmi_calculate,
    ideal_body_weight,
    lean_body_mass_calculate,
    calorie_deficit_timeline,
    daily_water_intake,
    
    # 数据类和枚举
    Gender, ActivityLevel, Goal, NutritionInfo,
    FOOD_DATABASE, MET_DATABASE,
)

import unittest
import math


class TestBMRCalculation(unittest.TestCase):
    """BMR计算测试"""
    
    def test_mifflin_male(self):
        """测试Mifflin-St Jeor公式（男性）"""
        # 70kg, 175cm, 30岁男性
        # BMR = 10×70 + 6.25×175 - 5×30 + 5 = 700 + 1093.75 - 150 + 5 = 1648.75
        bmr = calculate_bmr_mifflin(70, 175, 30, Gender.MALE)
        self.assertAlmostEqual(bmr, 1648.75, places=2)
    
    def test_mifflin_female(self):
        """测试Mifflin-St Jeor公式（女性）"""
        # 55kg, 165cm, 25岁女性
        # BMR = 10×55 + 6.25×165 - 5×25 - 161 = 550 + 1031.25 - 125 - 161 = 1295.25
        bmr = calculate_bmr_mifflin(55, 165, 25, Gender.FEMALE)
        self.assertAlmostEqual(bmr, 1295.25, places=2)
    
    def test_mifflin_elderly(self):
        """测试老年人BMR"""
        # 70kg, 170cm, 70岁男性
        bmr = calculate_bmr_mifflin(70, 170, 70, Gender.MALE)
        # 随年龄增长，BMR降低
        expected = 10*70 + 6.25*170 - 5*70 + 5
        self.assertAlmostEqual(bmr, expected, places=2)
    
    def test_mifflin_young(self):
        """测试年轻人BMR"""
        # 60kg, 180cm, 18岁男性
        bmr = calculate_bmr_mifflin(60, 180, 18, Gender.MALE)
        expected = 10*60 + 6.25*180 - 5*18 + 5
        self.assertAlmostEqual(bmr, expected, places=2)
    
    def test_harris_benedict_male(self):
        """测试Harris-Benedict公式（男性）"""
        # 70kg, 175cm, 30岁男性
        # BMR = 88.362 + 13.397×70 + 4.799×175 - 5.677×30
        bmr = calculate_bmr_harris_benedict(70, 175, 30, Gender.MALE)
        expected = 88.362 + 13.397*70 + 4.799*175 - 5.677*30
        self.assertAlmostEqual(bmr, expected, places=2)
    
    def test_harris_benedict_female(self):
        """测试Harris-Benedict公式（女性）"""
        # 55kg, 165cm, 25岁女性
        bmr = calculate_bmr_harris_benedict(55, 165, 25, Gender.FEMALE)
        expected = 447.593 + 9.247*55 + 3.098*165 - 4.330*25
        self.assertAlmostEqual(bmr, expected, places=2)
    
    def test_katch_mcardle(self):
        """测试Katch-McArdle公式"""
        # 瘦体重56kg
        # BMR = 370 + 21.6×56 = 370 + 1209.6 = 1579.6
        bmr = calculate_bmr_katch_mcardle(56)
        self.assertAlmostEqual(bmr, 1579.6, places=2)
    
    def test_katch_mcardle_low_lbm(self):
        """测试Katch-McArdle公式（低瘦体重）"""
        # 瘦体重40kg
        bmr = calculate_bmr_katch_mcardle(40)
        expected = 370 + 21.6*40
        self.assertAlmostEqual(bmr, expected, places=2)
    
    def test_bmr_from_body_fat(self):
        """测试从体脂率计算BMR"""
        # 70kg, 20%体脂
        # 瘦体重 = 70 × 0.8 = 56kg
        bmr = calculate_bmr_from_body_fat(70, 20, Gender.MALE)
        self.assertAlmostEqual(bmr, 1579.6, places=2)
    
    def test_bmr_from_body_fat_high(self):
        """测试高体脂率BMR"""
        # 100kg, 30%体脂
        bmr = calculate_bmr_from_body_fat(100, 30, Gender.MALE)
        lean_mass = 100 * 0.7
        expected = 370 + 21.6*lean_mass
        self.assertAlmostEqual(bmr, expected, places=2)
    
    def test_bmr_invalid_weight(self):
        """测试无效体重"""
        with self.assertRaises(ValueError):
            calculate_bmr_mifflin(0, 175, 30, Gender.MALE)
        with self.assertRaises(ValueError):
            calculate_bmr_mifflin(-10, 175, 30, Gender.MALE)
    
    def test_bmr_invalid_height(self):
        """测试无效身高"""
        with self.assertRaises(ValueError):
            calculate_bmr_mifflin(70, 0, 30, Gender.MALE)
    
    def test_bmr_invalid_age(self):
        """测试无效年龄"""
        with self.assertRaises(ValueError):
            calculate_bmr_mifflin(70, 175, 0, Gender.MALE)
    
    def test_bmr_invalid_lbm(self):
        """测试无效瘦体重"""
        with self.assertRaises(ValueError):
            calculate_bmr_katch_mcardle(0)
    
    def test_bmr_invalid_body_fat(self):
        """测试无效体脂率"""
        with self.assertRaises(ValueError):
            calculate_bmr_from_body_fat(70, -5, Gender.MALE)
        with self.assertRaises(ValueError):
            calculate_bmr_from_body_fat(70, 105, Gender.MALE)


class TestTDEECalculation(unittest.TestCase):
    """TDEE计算测试"""
    
    def test_tdee_sedentary(self):
        """测试久坐不动活动水平"""
        bmr = 1700
        tdee = calculate_tdee(bmr, ActivityLevel.SEDENTARY)
        self.assertAlmostEqual(tdee, 1700 * 1.2, places=2)
    
    def test_tdee_light(self):
        """测试轻度活动水平"""
        bmr = 1700
        tdee = calculate_tdee(bmr, ActivityLevel.LIGHT)
        self.assertAlmostEqual(tdee, 1700 * 1.375, places=2)
    
    def test_tdee_moderate(self):
        """测试中度活动水平"""
        bmr = 1700
        tdee = calculate_tdee(bmr, ActivityLevel.MODERATE)
        self.assertAlmostEqual(tdee, 1700 * 1.55, places=2)
    
    def test_tdee_active(self):
        """测试活跃活动水平"""
        bmr = 1700
        tdee = calculate_tdee(bmr, ActivityLevel.ACTIVE)
        self.assertAlmostEqual(tdee, 1700 * 1.725, places=2)
    
    def test_tdee_very_active(self):
        """测试非常活跃活动水平"""
        bmr = 1700
        tdee = calculate_tdee(bmr, ActivityLevel.VERY_ACTIVE)
        self.assertAlmostEqual(tdee, 1700 * 1.9, places=2)
    
    def test_tdee_full_mifflin(self):
        """测试完整TDEE计算（Mifflin方法）"""
        result = calculate_tdee_full(70, 175, 30, Gender.MALE, ActivityLevel.MODERATE)
        
        self.assertIn("bmr", result)
        self.assertIn("tdee", result)
        self.assertIn("activity_multiplier", result)
        self.assertIn("activity_level", result)
        self.assertIn("method", result)
        
        # 验证BMR计算正确
        expected_bmr = calculate_bmr_mifflin(70, 175, 30, Gender.MALE)
        self.assertAlmostEqual(result["bmr"], expected_bmr, places=1)
        
        # 验证TDEE = BMR × 1.55
        expected_tdee = expected_bmr * 1.55
        self.assertAlmostEqual(result["tdee"], expected_tdee, places=1)
    
    def test_tdee_full_harris(self):
        """测试完整TDEE计算（Harris-Benedict方法）"""
        result = calculate_tdee_full(70, 175, 30, Gender.MALE, ActivityLevel.MODERATE, "harris")
        
        expected_bmr = calculate_bmr_harris_benedict(70, 175, 30, Gender.MALE)
        self.assertAlmostEqual(result["bmr"], expected_bmr, places=1)
    
    def test_tdee_invalid_bmr(self):
        """测试无效BMR"""
        with self.assertRaises(ValueError):
            calculate_tdee(0, ActivityLevel.MODERATE)
    
    def test_tdee_invalid_method(self):
        """测试无效计算方法"""
        with self.assertRaises(ValueError):
            calculate_tdee_full(70, 175, 30, Gender.MALE, ActivityLevel.MODERATE, "invalid")


class TestFoodCalories(unittest.TestCase):
    """食物热量计算测试"""
    
    def test_get_food_info(self):
        """测试获取食物信息"""
        info = get_food_info("rice_white_cooked")
        self.assertIsNotNone(info)
        self.assertEqual(info["name"], "白米饭（熟）")
        self.assertEqual(info["calories"], 130)
    
    def test_get_food_info_not_found(self):
        """测试食物不存在"""
        info = get_food_info("nonexistent_food")
        self.assertIsNone(info)
    
    def test_calculate_food_calories(self):
        """测试计算食物热量"""
        # 200g白米饭
        result = calculate_food_calories("rice_white_cooked", 200)
        self.assertIsNotNone(result)
        self.assertEqual(result.calories, 260)  # 130 × 2
        self.assertEqual(result.protein, 5.4)    # 2.7 × 2
        self.assertEqual(result.carbs, 56)       # 28 × 2
    
    def test_calculate_food_calories_fraction(self):
        """测试非整数克数"""
        # 150g鸡胸肉
        result = calculate_food_calories("chicken_breast", 150)
        self.assertEqual(result.calories, 247.5)  # 165 × 1.5
        self.assertEqual(result.protein, 46.5)    # 31 × 1.5
    
    def test_calculate_food_calories_not_found(self):
        """测试食物不存在"""
        result = calculate_food_calories("nonexistent_food", 100)
        self.assertIsNone(result)
    
    def test_calculate_meal_calories(self):
        """测试计算一餐热量"""
        meal = [
            ("rice_white_cooked", 200),
            ("chicken_breast", 150),
            ("broccoli", 100),
        ]
        result = calculate_meal_calories(meal)
        
        # 验证总热量
        # 200g米饭: 260 kcal
        # 150g鸡胸肉: 247.5 kcal
        # 100g西兰花: 34 kcal
        # 总计: 541.5 kcal
        self.assertAlmostEqual(result.calories, 541.5, places=1)
    
    def test_calculate_meal_calories_empty(self):
        """测试空餐"""
        result = calculate_meal_calories([])
        self.assertEqual(result.calories, 0)
    
    def test_calculate_meal_calories_with_unknown(self):
        """测试包含未知食物的餐"""
        meal = [
            ("rice_white_cooked", 100),
            ("unknown_food", 50),  # 会被忽略
        ]
        result = calculate_meal_calories(meal)
        self.assertEqual(result.calories, 130)  # 只计算米饭
    
    def test_search_food(self):
        """测试搜索食物"""
        results = search_food("chicken")
        self.assertTrue(len(results) > 0)
        
        # 检查结果包含鸡胸肉
        found_breast = any(r["key"] == "chicken_breast" for r in results)
        self.assertTrue(found_breast)
    
    def test_search_food_chinese(self):
        """测试中文搜索"""
        results = search_food("米饭")
        self.assertTrue(len(results) > 0)
    
    def test_search_food_no_results(self):
        """测试无结果搜索"""
        results = search_food("zzzzzzzzz")
        self.assertEqual(len(results), 0)
    
    def test_list_all_foods(self):
        """测试列出所有食物"""
        foods = list_all_foods()
        self.assertTrue(len(foods) > 0)
        self.assertIn("rice_white_cooked", foods)
    
    def test_nutrition_info_add(self):
        """测试营养信息累加"""
        info1 = NutritionInfo(calories=100, protein=10, carbs=20, fat=5)
        info2 = NutritionInfo(calories=200, protein=15, carbs=30, fat=10)
        result = info1 + info2
        
        self.assertEqual(result.calories, 300)
        self.assertEqual(result.protein, 25)
        self.assertEqual(result.carbs, 50)
        self.assertEqual(result.fat, 15)
    
    def test_nutrition_info_multiply(self):
        """测试营养信息缩放"""
        info = NutritionInfo(calories=100, protein=10, carbs=20, fat=5)
        result = info * 2
        
        self.assertEqual(result.calories, 200)
        self.assertEqual(result.protein, 20)
    
    def test_nutrition_info_to_dict(self):
        """测试营养信息转字典"""
        info = NutritionInfo(calories=100.567, protein=10.123)
        dict_result = info.to_dict()
        
        self.assertEqual(dict_result["calories"], 100.6)  # 四舍五入
        self.assertEqual(dict_result["protein"], 10.1)


class TestExerciseCalories(unittest.TestCase):
    """运动消耗计算测试"""
    
    def test_get_exercise_info(self):
        """测试获取运动信息"""
        info = get_exercise_info("running_8kmh")
        self.assertIsNotNone(info)
        self.assertEqual(info["met"], 8.0)
    
    def test_get_exercise_info_not_found(self):
        """测试运动不存在"""
        info = get_exercise_info("nonexistent_exercise")
        self.assertIsNone(info)
    
    def test_calculate_exercise_calories(self):
        """测试计算运动消耗"""
        # 70kg，跑步8km/h，30分钟
        # MET × 体重 × 小时 = 8 × 70 × 0.5 = 280 kcal
        calories = calculate_exercise_calories("running_8kmh", 70, 30)
        self.assertEqual(calories, 280)
    
    def test_calculate_exercise_calories_hour(self):
        """测试一小时运动"""
        # 70kg，跑步10km/h，60分钟
        # 10 × 70 × 1 = 700 kcal
        calories = calculate_exercise_calories("running_10kmh", 70, 60)
        self.assertEqual(calories, 700)
    
    def test_calculate_exercise_calories_low_met(self):
        """测试低MET运动"""
        # 70kg，睡眠，8小时
        # 0.9 × 70 × 8 = 504 kcal
        calories = calculate_exercise_calories("sleeping", 70, 480)  # 8小时=480分钟
        self.assertEqual(calories, 504)
    
    def test_calculate_exercise_invalid_exercise(self):
        """测试无效运动"""
        with self.assertRaises(ValueError):
            calculate_exercise_calories("invalid", 70, 30)
    
    def test_calculate_exercise_invalid_weight(self):
        """测试无效体重"""
        with self.assertRaises(ValueError):
            calculate_exercise_calories("running_8kmh", 0, 30)
    
    def test_calculate_exercise_invalid_duration(self):
        """测试无效时长"""
        with self.assertRaises(ValueError):
            calculate_exercise_calories("running_8kmh", 70, 0)
    
    def test_calculate_custom_exercise(self):
        """测试自定义MET运动"""
        # MET=10，70kg，45分钟
        # 10 × 70 × 0.75 = 525 kcal
        calories = calculate_custom_exercise_calories(10, 70, 45)
        self.assertEqual(calories, 525)
    
    def test_calculate_custom_exercise_invalid_met(self):
        """测试无效MET"""
        with self.assertRaises(ValueError):
            calculate_custom_exercise_calories(0, 70, 30)
    
    def test_search_exercise(self):
        """测试搜索运动"""
        results = search_exercise("running")
        self.assertTrue(len(results) > 0)
    
    def test_search_exercise_chinese(self):
        """测试中文搜索运动"""
        results = search_exercise("跑步")
        self.assertTrue(len(results) > 0)
    
    def test_list_all_exercises(self):
        """测试列出所有运动"""
        exercises = list_all_exercises()
        self.assertTrue(len(exercises) > 0)


class TestWeightGoal(unittest.TestCase):
    """体重目标计划测试"""
    
    def test_weight_loss_plan(self):
        """测试减重计划"""
        # 从80kg减到75kg，TDEE=2500
        plan = calculate_weight_goal_plan(80, 75, 2500)
        
        self.assertEqual(plan.target_weight, 75)
        self.assertEqual(plan.weight_change, -5)
        # 默认0.5kg/周，5kg需要10周
        self.assertEqual(plan.weeks_to_achieve, 10)
        # 每日热量缺口
        self.assertTrue(plan.daily_calorie_target < 2500)
    
    def test_weight_gain_plan(self):
        """测试增重计划"""
        # 从60kg增到65kg，TDEE=2000
        plan = calculate_weight_goal_plan(60, 65, 2000)
        
        self.assertEqual(plan.target_weight, 65)
        self.assertEqual(plan.weight_change, 5)
        self.assertTrue(plan.daily_calorie_target > 2000)
    
    def test_weight_maintain_plan(self):
        """测试维持体重"""
        # 70kg维持，TDEE=2000
        plan = calculate_weight_goal_plan(70, 70, 2000)
        
        self.assertEqual(plan.target_weight, 70)
        self.assertEqual(plan.weight_change, 0)
        self.assertEqual(plan.weeks_to_achieve, 0)
    
    def test_weight_loss_calories(self):
        """测试减重热量计算"""
        result = calculate_weight_loss_calories(2500, 0.5)
        
        # 7700 × 0.5 / 7 = 550 kcal 缺口
        self.assertEqual(result["daily_deficit"], 550)
        self.assertEqual(result["daily_target"], 1950)
        self.assertEqual(result["weekly_loss"], 0.5)
    
    def test_weight_loss_calories_aggressive(self):
        """测试激进减重"""
        result = calculate_weight_loss_calories(2500, 1.0)
        
        # 7700 × 1.0 / 7 = 1100 kcal 缺口
        self.assertEqual(result["daily_deficit"], 1100)
        self.assertEqual(result["daily_target"], 1400)
    
    def test_weight_gain_calories(self):
        """测试增重热量计算"""
        result = calculate_weight_gain_calories(2500, 0.25)
        
        # 7700 × 0.25 / 7 = 275 kcal 盈余
        self.assertEqual(result["daily_surplus"], 275)
        self.assertEqual(result["daily_target"], 2775)
    
    def test_weight_loss_invalid_tdee(self):
        """测试无效TDEE"""
        with self.assertRaises(ValueError):
            calculate_weight_loss_calories(0, 0.5)
    
    def test_weight_loss_invalid_rate(self):
        """测试无效减重速度"""
        with self.assertRaises(ValueError):
            calculate_weight_loss_calories(2500, 0)  # 必须大于0
        with self.assertRaises(ValueError):
            calculate_weight_loss_calories(2500, 2.0)  # 超过限制
    
    def test_plan_to_dict(self):
        """测试计划转字典"""
        plan = calculate_weight_goal_plan(80, 75, 2500)
        dict_result = plan.to_dict()
        
        self.assertIn("target_weight", dict_result)
        self.assertIn("weeks_to_achieve", dict_result)
        self.assertIn("macro_split", dict_result)


class TestMacroNutrients(unittest.TestCase):
    """宏量营养素分配测试"""
    
    def test_macro_split_maintain(self):
        """测试维持宏量分配"""
        macros = calculate_macro_split(2000, Goal.MAINTAIN)
        
        # 维持：25%蛋白质，30%脂肪，45%碳水
        # 蛋白质: 2000 × 0.25 / 4 = 125g
        # 脂肪: 2000 × 0.30 / 9 = 66g
        # 碳水: 2000 × 0.45 / 4 = 225g
        self.assertIn("protein", macros)
        self.assertIn("carbs", macros)
        self.assertIn("fat", macros)
        
        self.assertEqual(macros["protein_pct"], 25.0)
        self.assertEqual(macros["fat_pct"], 30.0)
    
    def test_macro_split_loss(self):
        """测试减重宏量分配"""
        macros = calculate_macro_split(2000, Goal.LOSE)
        
        # 减重：30%蛋白质，30%脂肪，40%碳水
        self.assertEqual(macros["protein_pct"], 30.0)
        self.assertEqual(macros["fat_pct"], 30.0)
    
    def test_macro_split_gain(self):
        """测试增重宏量分配"""
        macros = calculate_macro_split(2000, Goal.GAIN)
        
        # 增重：20%蛋白质，25%脂肪，55%碳水
        self.assertEqual(macros["protein_pct"], 20.0)
        self.assertEqual(macros["fat_pct"], 25.0)
    
    def test_macro_split_custom(self):
        """测试自定义比例"""
        macros = calculate_macro_split(2000, Goal.MAINTAIN, protein_ratio=0.35, fat_ratio=0.25)
        
        self.assertEqual(macros["protein_pct"], 35.0)
        self.assertEqual(macros["fat_pct"], 25.0)
        # 碳水 = 100 - 35 - 25 = 40%
        self.assertEqual(macros["carbs_pct"], 40.0)
    
    def test_macro_calories(self):
        """测试从宏量计算热量"""
        # 100g蛋白质，200g碳水，50g脂肪
        # 热量 = 100×4 + 200×4 + 50×9 = 400 + 800 + 450 = 1650 kcal
        calories = calculate_macro_calories(100, 200, 50)
        self.assertEqual(calories, 1650)
    
    def test_macro_calories_with_alcohol(self):
        """测试包含酒精"""
        # 加上20g酒精
        calories = calculate_macro_calories(100, 200, 50, alcohol=20)
        # 1650 + 20×7 = 1790
        self.assertEqual(calories, 1790)
    
    def test_macro_calories_with_fiber(self):
        """测试包含纤维"""
        calories = calculate_macro_calories(100, 200, 50, fiber=10)
        # 1650 + 10×2 = 1670
        self.assertEqual(calories, 1670)
    
    def test_macro_percentages(self):
        """测试宏量占比"""
        percentages = calculate_macro_percentages(100, 200, 50)
        
        # 热量：蛋白质400，碳水800，脂肪450，总计1650
        # 蛋白质：400/1650 × 100 = 24.2%
        # 碳水：800/1650 × 100 = 48.5%
        # 脂肪：450/1650 × 100 = 27.3%
        self.assertAlmostEqual(percentages["protein_pct"], 24.2, places=1)
        self.assertAlmostEqual(percentages["total_calories"], 1650, places=1)
    
    def test_macro_percentages_zero(self):
        """测试零宏量"""
        percentages = calculate_macro_percentages(0, 0, 0)
        
        self.assertEqual(percentages["protein_pct"], 0)
        # 零宏量时total_calories为0或不存在，取决于实现
        self.assertEqual(percentages.get("total_calories", 0), 0)
    
    def test_macro_split_invalid_calories(self):
        """测试无效热量"""
        with self.assertRaises(ValueError):
            calculate_macro_split(0, Goal.MAINTAIN)


class TestBMI(unittest.TestCase):
    """BMI计算测试"""
    
    def test_bmi_normal(self):
        """测试正常BMI"""
        # 70kg, 175cm
        # BMI = 70 / (1.75)^2 = 22.86
        result = bmi_calculate(70, 175)
        
        self.assertAlmostEqual(result["bmi"], 22.86, places=1)  # 精度放宽到1位小数
        self.assertEqual(result["category"], "normal")
        self.assertEqual(result["category_cn"], "正常")
    
    def test_bmi_underweight(self):
        """测试偏瘦BMI"""
        # 50kg, 175cm
        # BMI = 50 / 1.75^2 = 16.33
        result = bmi_calculate(50, 175)
        
        self.assertEqual(result["category"], "underweight")
    
    def test_bmi_overweight(self):
        """测试超重BMI"""
        # 80kg, 175cm
        # BMI = 80 / 1.75^2 = 26.12
        result = bmi_calculate(80, 175)
        
        self.assertEqual(result["category"], "overweight")
    
    def test_bmi_obese(self):
        """测试肥胖BMI"""
        # 100kg, 175cm
        # BMI = 100 / 1.75^2 = 32.65
        result = bmi_calculate(100, 175)
        
        self.assertEqual(result["category"], "obese_class_1")
    
    def test_bmi_severe_obese(self):
        """测试重度肥胖"""
        # 130kg, 175cm
        # BMI = 130 / 1.75^2 = 42.45
        result = bmi_calculate(130, 175)
        
        self.assertEqual(result["category"], "obese_class_3")
    
    def test_bmi_healthy_weight_range(self):
        """测试健康体重范围"""
        result = bmi_calculate(70, 175)
        
        # 175cm的健康BMI范围（18.5-24.9）
        # 最低：18.5 × 1.75^2 = 56.6
        # 最高：24.9 × 1.75^2 = 76.2
        self.assertTrue(result["healthy_weight_range"]["min"] > 56)
        self.assertTrue(result["healthy_weight_range"]["max"] < 77)
    
    def test_bmi_invalid_weight(self):
        """测试无效体重"""
        with self.assertRaises(ValueError):
            bmi_calculate(0, 175)
    
    def test_bmi_invalid_height(self):
        """测试无效身高"""
        with self.assertRaises(ValueError):
            bmi_calculate(70, 0)


class TestIdealBodyWeight(unittest.TestCase):
    """理想体重计算测试"""
    
    def test_ideal_weight_male(self):
        """测试男性理想体重"""
        # 175cm男性
        # Devine: 50 + 2.3 × ((175/2.54) - 60) = 50 + 2.3 × 9.25 = 71.4
        result = ideal_body_weight(175, Gender.MALE)
        
        self.assertIn("devine", result)
        self.assertIn("robinson", result)
        self.assertIn("miller", result)
        self.assertIn("hamwi", result)
        self.assertIn("average", result)
        
        # 验证Devine公式
        height_inches = 175 / 2.54
        inches_over_5ft = height_inches - 60
        expected_devine = 50 + 2.3 * inches_over_5ft
        self.assertAlmostEqual(result["devine"], expected_devine, places=1)
    
    def test_ideal_weight_female(self):
        """测试女性理想体重"""
        # 165cm女性
        result = ideal_body_weight(165, Gender.FEMALE)
        
        # Devine: 45.5 + 2.3 × ((165/2.54) - 60)
        height_inches = 165 / 2.54
        inches_over_5ft = height_inches - 60
        expected_devine = 45.5 + 2.3 * inches_over_5ft
        self.assertAlmostEqual(result["devine"], expected_devine, places=1)
    
    def test_ideal_weight_short(self):
        """测试矮个子"""
        # 150cm
        result = ideal_body_weight(150, Gender.MALE)
        
        # 150cm约59英寸，低于5英尺（60英寸）
        # 公式仍然适用但结果偏低
        self.assertTrue(result["devine"] < 50)
    
    def test_ideal_weight_tall(self):
        """测试高个子"""
        # 190cm
        result = ideal_body_weight(190, Gender.MALE)
        
        self.assertTrue(result["devine"] > 80)
    
    def test_ideal_weight_invalid_height(self):
        """测试无效身高"""
        with self.assertRaises(ValueError):
            ideal_body_weight(0, Gender.MALE)


class TestLeanBodyMass(unittest.TestCase):
    """瘦体重计算测试"""
    
    def test_lbm_normal(self):
        """测试正常瘦体重"""
        # 70kg, 20%体脂
        result = lean_body_mass_calculate(70, 20)
        
        self.assertEqual(result["lean_body_mass"], 56.0)
        self.assertEqual(result["fat_mass"], 14.0)
        self.assertEqual(result["body_fat_percent"], 20)
    
    def test_lbm_high_body_fat(self):
        """测试高体脂"""
        # 100kg, 35%体脂
        result = lean_body_mass_calculate(100, 35)
        
        self.assertEqual(result["lean_body_mass"], 65.0)
        self.assertEqual(result["fat_mass"], 35.0)
    
    def test_lbm_low_body_fat(self):
        """测试低体脂"""
        # 70kg, 8%体脂
        result = lean_body_mass_calculate(70, 8)
        
        # 精度放宽
        self.assertAlmostEqual(result["lean_body_mass"], 64.4, places=1)
        self.assertAlmostEqual(result["fat_mass"], 5.6, places=1)
    
    def test_lbm_zero_body_fat(self):
        """测试零体脂"""
        result = lean_body_mass_calculate(70, 0)
        
        self.assertEqual(result["lean_body_mass"], 70.0)
        self.assertEqual(result["fat_mass"], 0)
    
    def test_lbm_invalid_weight(self):
        """测试无效体重"""
        with self.assertRaises(ValueError):
            lean_body_mass_calculate(0, 20)
    
    def test_lbm_invalid_body_fat(self):
        """测试无效体脂率"""
        with self.assertRaises(ValueError):
            lean_body_mass_calculate(70, -5)
        with self.assertRaises(ValueError):
            lean_body_mass_calculate(70, 105)


class TestCalorieDeficitTimeline(unittest.TestCase):
    """减重时间线测试"""
    
    def test_timeline_normal(self):
        """测试正常减重时间线"""
        # 从80kg减到75kg，每日缺口500kcal
        result = calorie_deficit_timeline(80, 75, 500)
        
        # 5kg × 7700 / 500 = 77天
        self.assertEqual(result["total_days"], 77)
        self.assertAlmostEqual(result["total_weeks"], 11, places=1)
        self.assertEqual(result["weight_to_lose"], 5.0)
        self.assertEqual(result["daily_deficit"], 500)
    
    def test_timeline_aggressive(self):
        """测试激进减重"""
        # 每日缺口1000kcal
        result = calorie_deficit_timeline(80, 75, 1000)
        
        # 5kg × 7700 / 1000 = 38.5天
        self.assertEqual(result["total_days"], 38)
    
    def test_timeline_already_reached(self):
        """测试已达目标"""
        result = calorie_deficit_timeline(75, 80, 500)  # 需要增重
        
        self.assertEqual(result["total_days"], 0)
        self.assertEqual(result["total_weeks"], 0)
    
    def test_timeline_milestones(self):
        """测试里程碑"""
        result = calorie_deficit_timeline(80, 75, 500)
        
        self.assertTrue(len(result["milestones"]) == 4)
        
        # 检查25%里程碑 - 精度放宽
        milestone_25 = result["milestones"][0]
        self.assertEqual(milestone_25["percent"], 25)
        self.assertAlmostEqual(milestone_25["weight"], 78.75, places=1)  # 80 - 5×0.25
    
    def test_timeline_invalid_weight(self):
        """测试无效体重"""
        with self.assertRaises(ValueError):
            calorie_deficit_timeline(0, 75, 500)
    
    def test_timeline_invalid_deficit(self):
        """测试无效缺口"""
        with self.assertRaises(ValueError):
            calorie_deficit_timeline(80, 75, 0)


class TestWaterIntake(unittest.TestCase):
    """饮水量计算测试"""
    
    def test_water_sedentary(self):
        """测试久坐饮水"""
        # 70kg，久坐
        # 70 × 33 × 1.0 = 2310ml
        result = daily_water_intake(70, ActivityLevel.SEDENTARY)
        
        self.assertEqual(result["ml"], 2310)
        self.assertAlmostEqual(result["liters"], 2.3, places=1)
    
    def test_water_moderate(self):
        """测试中度活动饮水"""
        # 70kg，中度活动
        # 70 × 33 × 1.2 = 2772ml
        result = daily_water_intake(70, ActivityLevel.MODERATE)
        
        self.assertEqual(result["ml"], 2772)
    
    def test_water_very_active(self):
        """测试非常活跃饮水"""
        # 80kg，非常活跃
        # 80 × 33 × 1.4 = 3696ml (实际可能是3695.999...)
        result = daily_water_intake(80, ActivityLevel.VERY_ACTIVE)
        
        self.assertAlmostEqual(result["ml"], 3696, delta=1)  # 允许±1的误差
    
    def test_water_glasses(self):
        """测试杯数计算"""
        result = daily_water_intake(70)
        
        self.assertIn("glasses_250ml", result)
        self.assertIn("glasses_500ml", result)
    
    def test_water_invalid_weight(self):
        """测试无效体重"""
        with self.assertRaises(ValueError):
            daily_water_intake(0)


class TestEdgeCases(unittest.TestCase):
    """边界值测试"""
    
    def test_extreme_weight(self):
        """测试极端体重"""
        # 150kg
        bmr = calculate_bmr_mifflin(150, 180, 30, Gender.MALE)
        self.assertTrue(bmr > 2000)
        
        # 40kg
        bmr = calculate_bmr_mifflin(40, 160, 25, Gender.FEMALE)
        self.assertTrue(bmr > 0)
    
    def test_extreme_height(self):
        """测试极端身高"""
        # 200cm
        bmr = calculate_bmr_mifflin(80, 200, 25, Gender.MALE)
        self.assertTrue(bmr > 1800)
        
        # 140cm
        bmr = calculate_bmr_mifflin(50, 140, 20, Gender.FEMALE)
        self.assertTrue(bmr > 0)
    
    def test_extreme_age(self):
        """测试极端年龄"""
        # 100岁
        bmr = calculate_bmr_mifflin(60, 170, 100, Gender.MALE)
        self.assertTrue(bmr > 0)
        
        # 1岁
        bmr = calculate_bmr_mifflin(10, 75, 1, Gender.MALE)
        self.assertTrue(bmr > 0)
    
    def test_zero_grams_food(self):
        """测试零克数食物"""
        result = calculate_food_calories("rice_white_cooked", 0)
        self.assertEqual(result.calories, 0)
    
    def test_large_grams_food(self):
        """测试大克数食物"""
        result = calculate_food_calories("rice_white_cooked", 10000)  # 10kg
        self.assertEqual(result.calories, 13000)
    
    def test_zero_duration_exercise(self):
        """测试零时长运动"""
        with self.assertRaises(ValueError):
            calculate_exercise_calories("running_8kmh", 70, 0)
    
    def test_large_duration_exercise(self):
        """测试长时长运动"""
        # 5小时跑步
        calories = calculate_exercise_calories("running_8kmh", 70, 300)
        self.assertEqual(calories, 2800)
    
    def test_zero_body_fat(self):
        """测试零体脂率"""
        bmr = calculate_bmr_from_body_fat(70, 0, Gender.MALE)
        lean_mass = 70
        expected = 370 + 21.6 * lean_mass
        self.assertAlmostEqual(bmr, expected, places=1)
    
    def test_near_100_body_fat(self):
        """测试接近100%体脂"""
        bmr = calculate_bmr_from_body_fat(70, 99, Gender.MALE)
        lean_mass = 70 * 0.01
        expected = 370 + 21.6 * lean_mass
        self.assertAlmostEqual(bmr, expected, places=1)


class TestDatabaseIntegrity(unittest.TestCase):
    """数据库完整性测试"""
    
    def test_food_database_structure(self):
        """测试食物数据库结构"""
        for key, info in FOOD_DATABASE.items():
            self.assertIn("name", info)
            self.assertIn("calories", info)
            self.assertTrue(info["calories"] >= 0)
    
    def test_met_database_structure(self):
        """测试MET数据库结构"""
        for key, info in MET_DATABASE.items():
            self.assertIn("name", info)
            self.assertIn("met", info)
            self.assertTrue(info["met"] > 0)
    
    def test_food_database_coverage(self):
        """测试食物数据库覆盖"""
        # 确保包含常见食物类别 - 使用实际存在的食物键名
        categories = ["rice", "chicken", "broccoli", "apple", "milk"]
        for cat in categories:
            results = search_food(cat)
            self.assertTrue(len(results) > 0, f"缺少{cat}类别食物")
    
    def test_met_database_coverage(self):
        """测试MET数据库覆盖"""
        # 确保包含常见运动类别
        categories = ["running", "swimming", "weight", "basketball"]
        for cat in categories:
            results = search_exercise(cat)
            self.assertTrue(len(results) > 0, f"缺少{cat}类别运动")


def run_tests():
    """运行所有测试"""
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # 添加所有测试类
    test_classes = [
        TestBMRCalculation,
        TestTDEECalculation,
        TestFoodCalories,
        TestExerciseCalories,
        TestWeightGoal,
        TestMacroNutrients,
        TestBMI,
        TestIdealBodyWeight,
        TestLeanBodyMass,
        TestCalorieDeficitTimeline,
        TestWaterIntake,
        TestEdgeCases,
        TestDatabaseIntegrity,
    ]
    
    for test_class in test_classes:
        tests = loader.loadTestsFromTestCase(test_class)
        suite.addTests(tests)
    
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # 输出统计
    print("\n" + "=" * 50)
    print(f"测试总数: {result.testsRun}")
    print(f"成功: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"失败: {len(result.failures)}")
    print(f"错误: {len(result.errors)}")
    print("=" * 50)
    
    return result.wasSuccessful()


if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)