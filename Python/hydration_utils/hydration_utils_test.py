"""
Hydration Utils Tests - 水分摄入追踪工具测试

Author: AllToolkit
License: MIT
"""

import unittest
from datetime import datetime, date, timedelta
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mod import (
    ActivityLevel,
    ClimateType,
    BeverageType,
    HydrationStatus,
    Beverage,
    DailyLog,
    HydrationTracker,
    HydrationError,
    InvalidInputError,
    calculate_daily_water_needs,
    calculate_hydration_status,
    get_drinking_schedule,
    calculate_beverage_hydration,
    estimate_water_from_foods,
    get_exercise_hydration_plan,
    calculate_caffeine_impact,
    assess_dehydration_risk,
    generate_hydration_report,
    calculate_oral_rehydration_solution,
    get_weather_adjusted_target,
    FOOD_WATER_CONTENT,
)


class TestCalculateDailyWaterNeeds(unittest.TestCase):
    """测试每日水需求计算"""
    
    def test_basic_calculation(self):
        """测试基础计算"""
        result = calculate_daily_water_needs(weight_kg=70)
        self.assertIn("total_need_ml", result)
        self.assertIn("base_need_ml", result)
        self.assertEqual(result["base_need_ml"], 70 * 32)
        self.assertEqual(result["base_need_ml"], 2240)
    
    def test_activity_level_adjustment(self):
        """测试活动量调整"""
        sedentary = calculate_daily_water_needs(weight_kg=70, activity_level=ActivityLevel.SEDENTARY)
        active = calculate_daily_water_needs(weight_kg=70, activity_level=ActivityLevel.ACTIVE)
        
        # 活跃状态应该比久坐状态需要更多水分
        self.assertGreater(active["total_need_ml"], sedentary["total_need_ml"])
    
    def test_climate_adjustment(self):
        """测试气候调整"""
        cool = calculate_daily_water_needs(weight_kg=70, climate=ClimateType.COOL)
        hot = calculate_daily_water_needs(weight_kg=70, climate=ClimateType.HOT)
        
        # 炎热天气应该需要更多水分
        self.assertGreater(hot["total_need_ml"], cool["total_need_ml"])
    
    def test_exercise_adjustment(self):
        """测试运动调整"""
        no_exercise = calculate_daily_water_needs(weight_kg=70, exercise_minutes=0)
        with_exercise = calculate_daily_water_needs(weight_kg=70, exercise_minutes=60)
        
        # 有运动应该需要更多水分
        self.assertGreater(with_exercise["total_need_ml"], no_exercise["total_need_ml"])
        # 60分钟运动额外600ml
        self.assertEqual(with_exercise["exercise_addition_ml"], 600)
    
    def test_pregnancy_adjustment(self):
        """测试孕期调整"""
        normal = calculate_daily_water_needs(weight_kg=70, gender="female")
        pregnant = calculate_daily_water_needs(weight_kg=70, gender="female", is_pregnant=True)
        breastfeeding = calculate_daily_water_needs(weight_kg=70, gender="female", is_breastfeeding=True)
        
        # 孕期和哺乳期应该需要更多水分
        self.assertGreater(pregnant["total_need_ml"], normal["total_need_ml"])
        self.assertGreater(breastfeeding["total_need_ml"], pregnant["total_need_ml"])
        self.assertEqual(breastfeeding["pregnancy_addition_ml"], 700)
    
    def test_invalid_weight(self):
        """测试无效体重"""
        with self.assertRaises(InvalidInputError):
            calculate_daily_water_needs(weight_kg=0)
        with self.assertRaises(InvalidInputError):
            calculate_daily_water_needs(weight_kg=-10)
    
    def test_complete_result_structure(self):
        """测试返回结果结构完整性"""
        result = calculate_daily_water_needs(weight_kg=70)
        
        required_keys = [
            "base_need_ml",
            "activity_adjusted_ml",
            "exercise_addition_ml",
            "pregnancy_addition_ml",
            "total_need_ml",
            "recommended_glasses",
            "hourly_target_ml"
        ]
        
        for key in required_keys:
            self.assertIn(key, result)


class TestCalculateHydrationStatus(unittest.TestCase):
    """测试水分状态计算"""
    
    def test_optimal_status(self):
        """测试最佳状态"""
        status, completion = calculate_hydration_status(2000, 2000, hours_elapsed=12)
        self.assertEqual(status, HydrationStatus.OPTIMAL)
        self.assertEqual(completion, 100.0)
    
    def test_mild_dehydration(self):
        """测试轻度脱水"""
        status, completion = calculate_hydration_status(1500, 2000, hours_elapsed=12)
        self.assertEqual(status, HydrationStatus.DEHYDRATED_MILD)
        self.assertEqual(completion, 75.0)
    
    def test_moderate_dehydration(self):
        """测试中度脱水"""
        status, completion = calculate_hydration_status(1000, 2000, hours_elapsed=12)
        self.assertEqual(status, HydrationStatus.DEHYDRATED_MODERATE)
        self.assertEqual(completion, 50.0)
    
    def test_severe_dehydration(self):
        """测试严重脱水"""
        status, completion = calculate_hydration_status(500, 2000, hours_elapsed=12)
        self.assertEqual(status, HydrationStatus.DEHYDRATED_SEVERE)
        self.assertEqual(completion, 25.0)
    
    def test_overhydrated(self):
        """测试过度补水"""
        status, completion = calculate_hydration_status(2500, 2000, hours_elapsed=12)
        self.assertEqual(status, HydrationStatus.OVERHYDRATED)
        # completion is capped at 100 in calculate_hydration_status
        self.assertEqual(completion, 100.0)
    
    def test_progress_considered(self):
        """测试进度影响"""
        # 早上6点开始，现在是9点（3小时），目标2000ml，已喝500ml
        # 预期进度 3/12 = 25%, 已喝500/2000 = 25%，应该是最优状态
        status1, completion1 = calculate_hydration_status(500, 2000, hours_elapsed=3)
        
        # 同样的摄入量，但是到了中午12点（6小时）
        # 预期进度 50%，实际 25%，应该是中度脱水
        status2, completion2 = calculate_hydration_status(500, 2000, hours_elapsed=6)
        
        self.assertEqual(status1, HydrationStatus.OPTIMAL)
        self.assertEqual(status2, HydrationStatus.DEHYDRATED_MODERATE)


class TestGetDrinkingSchedule(unittest.TestCase):
    """测试饮水时间表生成"""
    
    def test_basic_schedule(self):
        """测试基础时间表"""
        schedule = get_drinking_schedule(2400, "07:00", "23:00", intervals=12)
        
        self.assertEqual(len(schedule), 12)
        self.assertEqual(schedule[0]["time"], "07:00")
        self.assertEqual(schedule[0]["amount_ml"], 200)
        self.assertEqual(schedule[-1]["percentage"], 100.0)
    
    def test_cumulative_tracking(self):
        """测试累计追踪"""
        schedule = get_drinking_schedule(2000, "08:00", "20:00", intervals=10)
        
        for i, entry in enumerate(schedule):
            expected_cumulative = 200 * (i + 1)
            self.assertEqual(entry["cumulative_ml"], expected_cumulative)
    
    def test_custom_intervals(self):
        """测试自定义间隔次数"""
        schedule = get_drinking_schedule(3000, "06:00", "22:00", intervals=8)
        self.assertEqual(len(schedule), 8)
        self.assertEqual(schedule[0]["amount_ml"], 375)  # 3000/8


class TestCalculateBeverageHydration(unittest.TestCase):
    """测试饮料补水效果计算"""
    
    def test_water_hydration(self):
        """测试纯水补水效果"""
        result = calculate_beverage_hydration(BeverageType.WATER, 500)
        
        self.assertEqual(result["volume_ml"], 500)
        self.assertEqual(result["effective_hydration_ml"], 500)  # 纯水100%有效
        self.assertEqual(result["caffeine_mg"], 0)
        self.assertEqual(result["hydration_efficiency"], 100)
    
    def test_coffee_hydration(self):
        """测试咖啡补水效果"""
        result = calculate_beverage_hydration(BeverageType.COFFEE, 300)
        
        self.assertEqual(result["volume_ml"], 300)
        # 咖啡含有咖啡因，补水效果略低
        self.assertLess(result["effective_hydration_ml"], 300)
        self.assertGreater(result["caffeine_mg"], 0)
        self.assertLess(result["hydration_efficiency"], 100)
    
    def test_alcohol_hydration(self):
        """测试酒精饮料补水效果"""
        result = calculate_beverage_hydration(BeverageType.ALCOHOL_BEER, 500)
        
        self.assertEqual(result["volume_ml"], 500)
        # 啤酒有酒精，补水效果降低
        self.assertLess(result["effective_hydration_ml"], 500)
        self.assertGreater(result["alcohol_percent"], 0)
    
    def test_sports_drink(self):
        """测试运动饮料"""
        result = calculate_beverage_hydration(BeverageType.SPORTS_DRINK, 500)
        
        # 运动饮料通常不含咖啡因或酒精
        self.assertEqual(result["effective_hydration_ml"], 500)
        self.assertEqual(result["caffeine_mg"], 0)
        self.assertEqual(result["alcohol_percent"], 0)


class TestEstimateWaterFromFoods(unittest.TestCase):
    """测试食物水分估算"""
    
    def test_single_food(self):
        """测试单个食物"""
        water = estimate_water_from_foods([
            {"name": "watermelon", "weight_g": 100, "water_percent": 92}
        ])
        self.assertEqual(water, 92)
    
    def test_multiple_foods(self):
        """测试多种食物"""
        water = estimate_water_from_foods([
            {"name": "watermelon", "weight_g": 200, "water_percent": 92},
            {"name": "soup", "weight_g": 300, "water_percent": 90}
        ])
        expected = 200 * 0.92 + 300 * 0.90
        self.assertEqual(water, expected)
    
    def test_default_water_percent(self):
        """测试默认含水量"""
        water = estimate_water_from_foods([
            {"name": "unknown", "weight_g": 100}
        ])
        self.assertEqual(water, 70)  # 默认70%


class TestGetExerciseHydrationPlan(unittest.TestCase):
    """测试运动补水计划"""
    
    def test_moderate_exercise(self):
        """测试中等强度运动"""
        plan = get_exercise_hydration_plan("running", duration_minutes=60, intensity="moderate")
        
        self.assertIn("estimated_sweat_loss_ml", plan)
        self.assertIn("pre_exercise", plan)
        self.assertIn("during_exercise", plan)
        self.assertIn("post_exercise", plan)
        
        # 验证运动前补水建议
        self.assertEqual(plan["pre_exercise"]["2_hours_before_ml"], 500)
        self.assertEqual(plan["pre_exercise"]["30_min_before_ml"], 250)
    
    def test_high_intensity_exercise(self):
        """测试高强度运动"""
        plan = get_exercise_hydration_plan("cycling", duration_minutes=90, intensity="high")
        
        # 高强度运动出汗更多
        self.assertIn("electrolyte_needed", plan)
        self.assertIn("sports_drink_recommended", plan)
    
    def test_temperature_adjustment(self):
        """测试温度调整"""
        cool = get_exercise_hydration_plan("running", 30, "moderate", temperature_celsius=10)
        hot = get_exercise_hydration_plan("running", 30, "moderate", temperature_celsius=35)
        
        # 炎热环境下出汗更多
        self.assertGreater(hot["estimated_sweat_loss_ml"], cool["estimated_sweat_loss_ml"])
    
    def test_weight_adjustment(self):
        """测试体重调整"""
        light = get_exercise_hydration_plan("running", 30, "moderate", weight_kg=50)
        heavy = get_exercise_hydration_plan("running", 30, "moderate", weight_kg=90)
        
        # 体重更重出汗更多
        self.assertGreater(heavy["estimated_sweat_loss_ml"], light["estimated_sweat_loss_ml"])


class TestCalculateCaffeineImpact(unittest.TestCase):
    """测试咖啡因影响计算"""
    
    def test_caffeine_decay(self):
        """测试咖啡因衰减"""
        impact0 = calculate_caffeine_impact(100, hours_since_intake=0)
        impact5 = calculate_caffeine_impact(100, hours_since_intake=5.5)
        impact11 = calculate_caffeine_impact(100, hours_since_intake=11)
        
        # 5.5小时后剩余约一半
        self.assertAlmostEqual(impact5["remaining_caffeine_mg"], 50, places=0)
        # 11小时后剩余约四分之一
        self.assertAlmostEqual(impact11["remaining_caffeine_mg"], 25, places=0)
    
    def test_diuretic_effect(self):
        """测试利尿效果"""
        impact = calculate_caffeine_impact(200)
        # 每100mg咖啡因约100ml利尿效果
        self.assertEqual(impact["diuretic_effect_ml"], 200)
    
    def test_sleep_impact(self):
        """测试睡眠影响"""
        low_caffeine = calculate_caffeine_impact(50)
        high_caffeine = calculate_caffeine_impact(200)
        
        # 低咖啡因不影响睡眠
        self.assertFalse(low_caffeine["sleep_disruption_risk"])
        self.assertTrue(low_caffeine["safe_to_sleep"])
        
        # 高咖啡因影响睡眠
        self.assertTrue(high_caffeine["sleep_disruption_risk"])
    
    def test_metabolized_percentage(self):
        """测试代谢百分比"""
        impact = calculate_caffeine_impact(100, hours_since_intake=5.5)
        self.assertAlmostEqual(impact["metabolized_percent"], 50, places=0)


class TestAssessDehydrationRisk(unittest.TestCase):
    """测试脱水风险评估"""
    
    def test_optimal_intake(self):
        """测试最优摄入"""
        log = DailyLog(date=date.today())
        log.beverages.append(Beverage(BeverageType.WATER, 2000))
        
        risk = assess_dehydration_risk(log, 2000)
        
        self.assertEqual(risk["risk_level"], "low")
        # Check that recommendation mentions hydration is good or sufficient
        self.assertTrue(
            "水分摄入良好" in risk["recommendations"][0] or 
            "水分摄入充足" in risk["recommendations"][0]
        )
    
    def test_severe_dehydration(self):
        """测试严重脱水"""
        log = DailyLog(date=date.today())
        log.beverages.append(Beverage(BeverageType.WATER, 200))
        
        risk = assess_dehydration_risk(log, 2000)
        
        self.assertEqual(risk["risk_level"], "critical")
        self.assertIn("严重脱水", risk["recommendations"][0])
    
    def test_caffeine_warning(self):
        """测试咖啡因警告"""
        log = DailyLog(date=date.today())
        log.beverages.append(Beverage(BeverageType.COFFEE, 500, caffeine_mg=200))
        
        risk = assess_dehydration_risk(log, 2000)
        
        # 高咖啡因应该触发警告
        self.assertGreater(risk["caffeine_remaining_mg"], 0)


class TestGenerateHydrationReport(unittest.TestCase):
    """测试水分报告生成"""
    
    def test_complete_report(self):
        """测试完整报告"""
        log = DailyLog(date=date.today())
        log.beverages.extend([
            Beverage(BeverageType.WATER, 500),
            Beverage(BeverageType.TEA, 300, caffeine_mg=60),
            Beverage(BeverageType.WATER, 400),
        ])
        
        report = generate_hydration_report(log, 2000)
        
        self.assertIn("summary", report)
        self.assertIn("by_beverage_type", report)
        self.assertIn("hourly_distribution", report)
        self.assertIn("risk_assessment", report)
        
        self.assertEqual(report["summary"]["total_intake_ml"], 1200)
    
    def test_beverage_type_grouping(self):
        """测试饮料类型分组"""
        log = DailyLog(date=date.today())
        log.beverages.extend([
            Beverage(BeverageType.WATER, 500),
            Beverage(BeverageType.WATER, 300),
            Beverage(BeverageType.COFFEE, 200, caffeine_mg=80),
        ])
        
        report = generate_hydration_report(log, 2000)
        
        by_type = report["by_beverage_type"]
        self.assertEqual(by_type["water"]["volume_ml"], 800)
        self.assertEqual(by_type["water"]["count"], 2)
        self.assertEqual(by_type["coffee"]["volume_ml"], 200)


class TestHydrationTracker(unittest.TestCase):
    """测试水分追踪器"""
    
    def test_log_water(self):
        """测试记录水分"""
        tracker = HydrationTracker(weight_kg=70)
        tracker.log_water(500)
        tracker.log_water(300)
        
        status = tracker.get_current_status()
        self.assertEqual(status["current_intake_ml"], 800)
    
    def test_log_coffee(self):
        """测试记录咖啡"""
        tracker = HydrationTracker(weight_kg=70)
        tracker.log_coffee(300)
        
        # 咖啡应该有咖啡因记录
        log = tracker.daily_logs[date.today()]
        coffee = log.beverages[0]
        self.assertGreater(coffee.caffeine_mg, 0)
    
    def test_daily_target(self):
        """测试每日目标"""
        tracker = HydrationTracker(weight_kg=70)
        target = tracker.get_daily_target()
        
        # 70kg的基础目标应该在2240左右
        self.assertGreater(target, 2000)
        self.assertLess(target, 3000)
    
    def test_weekly_summary(self):
        """测试周总结"""
        tracker = HydrationTracker(weight_kg=70)
        
        # 添加几天的记录
        today = date.today()
        for i in range(3):
            d = today - timedelta(days=i)
            tracker.log_water(1000, log_date=d)
        
        summary = tracker.get_weekly_summary()
        
        self.assertIn("days_logged", summary)
        self.assertIn("average_completion", summary)
    
    def test_drinking_reminder(self):
        """测试饮水提醒"""
        tracker = HydrationTracker(weight_kg=70)
        
        # 没喝水时应该提醒
        reminder = tracker.get_drinking_reminder()
        self.assertTrue(reminder["should_remind"])
        
        # 喝够水后不应该提醒
        tracker.log_water(3000)
        reminder = tracker.get_drinking_reminder()
        self.assertFalse(reminder["should_remind"])
    
    def test_invalid_volume(self):
        """测试无效容量"""
        tracker = HydrationTracker(weight_kg=70)
        
        with self.assertRaises(InvalidInputError):
            tracker.log_water(0)
        
        with self.assertRaises(InvalidInputError):
            tracker.log_water(-100)


class TestCalculateOralRehydrationSolution(unittest.TestCase):
    """测试口服补液盐计算"""
    
    def test_mild_dehydration(self):
        """测试轻度脱水"""
        ors = calculate_oral_rehydration_solution(weight_kg=70, dehydration_level="mild")
        
        self.assertIn("standard_ors_per_liter", ors)
        self.assertIn("simplified_home_recipe", ors)
        self.assertIn("administration", ors)
        
        # 轻度脱水：50ml/kg
        self.assertEqual(ors["recommended_total_ml"], 70 * 50)
    
    def test_moderate_dehydration(self):
        """测试中度脱水"""
        ors = calculate_oral_rehydration_solution(weight_kg=70, dehydration_level="moderate")
        
        # 中度脱水：100ml/kg
        self.assertEqual(ors["recommended_total_ml"], 70 * 100)
    
    def test_recipe_structure(self):
        """测试配方结构"""
        ors = calculate_oral_rehydration_solution(weight_kg=70)
        
        recipe = ors["simplified_home_recipe"]
        self.assertEqual(recipe["water_ml"], 1000)
        self.assertGreater(recipe["salt_g"], 0)
        self.assertGreater(recipe["sugar_g"], 0)


class TestGetWeatherAdjustedTarget(unittest.TestCase):
    """测试天气调整目标"""
    
    def test_cool_weather(self):
        """测试凉爽天气"""
        adjusted = get_weather_adjusted_target(2000, temperature_celsius=5)
        self.assertLess(adjusted, 2000)
    
    def test_hot_weather(self):
        """测试炎热天气"""
        adjusted = get_weather_adjusted_target(2000, temperature_celsius=35)
        self.assertGreater(adjusted, 2000)
    
    def test_humidity_adjustment(self):
        """测试湿度调整"""
        low_humidity = get_weather_adjusted_target(2000, 30, humidity_percent=20)
        high_humidity = get_weather_adjusted_target(2000, 30, humidity_percent=90)
        
        # 高湿度需要更多水分
        self.assertGreater(high_humidity, low_humidity)
    
    def test_sunny_adjustment(self):
        """测试阳光调整"""
        cloudy = get_weather_adjusted_target(2000, 25, is_sunny=False)
        sunny = get_weather_adjusted_target(2000, 25, is_sunny=True)
        
        # 晴天需要略多水分
        self.assertGreater(sunny, cloudy)


class TestBeverageClass(unittest.TestCase):
    """测试饮料类"""
    
    def test_hydration_value_calculation(self):
        """测试补水值计算"""
        # 纯水
        water = Beverage(BeverageType.WATER, 500)
        self.assertEqual(water.hydration_value, 500)
        
        # 含咖啡因饮料
        coffee = Beverage(BeverageType.COFFEE, 300, caffeine_mg=120)
        # 120mg咖啡因减少12%效果
        self.assertAlmostEqual(coffee.hydration_value, 300 * 0.88, places=0)
    
    def test_alcohol_impact(self):
        """测试酒精影响"""
        beer = Beverage(BeverageType.ALCOHOL_BEER, 500, alcohol_percent=5)
        # 5%酒精减少15%效果
        self.assertLess(beer.hydration_value, 500)


class TestDailyLogClass(unittest.TestCase):
    """测试每日日志类"""
    
    def test_total_intake(self):
        """测试总摄入量"""
        log = DailyLog(date=date.today())
        log.beverages.extend([
            Beverage(BeverageType.WATER, 500),
            Beverage(BeverageType.TEA, 300),
        ])
        
        self.assertEqual(log.total_intake_ml, 800)
    
    def test_effective_hydration(self):
        """测试有效补水量"""
        log = DailyLog(date=date.today())
        log.beverages.extend([
            Beverage(BeverageType.WATER, 500),
            Beverage(BeverageType.COFFEE, 300, caffeine_mg=120),
        ])
        
        # 水完全有效，咖啡因饮料效果降低
        self.assertLess(log.effective_hydration_ml, log.total_intake_ml)
    
    def test_water_intake(self):
        """测试纯水摄入"""
        log = DailyLog(date=date.today())
        log.beverages.extend([
            Beverage(BeverageType.WATER, 500),
            Beverage(BeverageType.COFFEE, 300),
            Beverage(BeverageType.WATER, 200),
        ])
        
        self.assertEqual(log.water_intake_ml, 700)


class TestConstants(unittest.TestCase):
    """测试常量定义"""
    
    def test_food_water_content(self):
        """测试食物含水量"""
        self.assertEqual(FOOD_WATER_CONTENT["watermelon"], 92)
        self.assertEqual(FOOD_WATER_CONTENT["cucumber"], 96)
        self.assertGreater(FOOD_WATER_CONTENT["soup"], 80)
    
    def test_constants_values(self):
        """测试常量值合理性"""
        from mod import (
            BASE_WATER_PER_KG,
            ACTIVITY_MULTIPLIERS,
            CLIMATE_MULTIPLIERS,
            EXERCISE_WATER_PER_MINUTE,
        )
        
        self.assertEqual(BASE_WATER_PER_KG, 32)
        self.assertGreater(ACTIVITY_MULTIPLIERS[ActivityLevel.ACTIVE], 1.0)
        self.assertGreater(CLIMATE_MULTIPLIERS[ClimateType.HOT], 1.0)
        self.assertEqual(EXERCISE_WATER_PER_MINUTE, 10)


def run_tests():
    """运行所有测试"""
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    suite.addTests(loader.loadTestsFromTestCase(TestCalculateDailyWaterNeeds))
    suite.addTests(loader.loadTestsFromTestCase(TestCalculateHydrationStatus))
    suite.addTests(loader.loadTestsFromTestCase(TestGetDrinkingSchedule))
    suite.addTests(loader.loadTestsFromTestCase(TestCalculateBeverageHydration))
    suite.addTests(loader.loadTestsFromTestCase(TestEstimateWaterFromFoods))
    suite.addTests(loader.loadTestsFromTestCase(TestGetExerciseHydrationPlan))
    suite.addTests(loader.loadTestsFromTestCase(TestCalculateCaffeineImpact))
    suite.addTests(loader.loadTestsFromTestCase(TestAssessDehydrationRisk))
    suite.addTests(loader.loadTestsFromTestCase(TestGenerateHydrationReport))
    suite.addTests(loader.loadTestsFromTestCase(TestHydrationTracker))
    suite.addTests(loader.loadTestsFromTestCase(TestCalculateOralRehydrationSolution))
    suite.addTests(loader.loadTestsFromTestCase(TestGetWeatherAdjustedTarget))
    suite.addTests(loader.loadTestsFromTestCase(TestBeverageClass))
    suite.addTests(loader.loadTestsFromTestCase(TestDailyLogClass))
    suite.addTests(loader.loadTestsFromTestCase(TestConstants))
    
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    return result


if __name__ == "__main__":
    run_tests()