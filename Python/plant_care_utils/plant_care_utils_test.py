"""
plant_care_utils 测试文件
"""

import unittest
import sys
import os
from datetime import datetime, timedelta

# 添加模块路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from plant_care_utils.mod import (
    Plant,
    PlantCareScheduler,
    PlantType,
    Season,
    LightLevel,
    WaterFrequency,
    HealthStatus,
    GrowthStage,
    PLANT_DATABASE,
    calculate_water_needs,
    analyze_light_requirements,
    get_seasonal_fertilizer_recommendation,
    diagnose_plant_issue,
    create_plant_care_calendar,
    quick_water_check,
    get_plant_database_info,
    list_all_plant_types
)


class TestPlantType(unittest.TestCase):
    """测试 PlantType 枚举"""
    
    def test_plant_types_exist(self):
        """测试植物类型存在"""
        self.assertEqual(PlantType.SUCCULENT.value, "succulent")
        self.assertEqual(PlantType.TROPICAL.value, "tropical")
        self.assertEqual(PlantType.FERN.value, "fern")
        self.assertEqual(PlantType.CACTUS.value, "cactus")
    
    def test_all_plant_types_in_database(self):
        """测试所有植物类型都在数据库中"""
        for plant_type in PlantType:
            info = PLANT_DATABASE.get(plant_type)
            self.assertIsNotNone(info)
            self.assertIn("name", info)
            self.assertIn("water_frequency", info)


class TestSeason(unittest.TestCase):
    """测试 Season 枚举"""
    
    def test_seasons_exist(self):
        """测试季节存在"""
        self.assertEqual(Season.SPRING.value, "spring")
        self.assertEqual(Season.SUMMER.value, "summer")
        self.assertEqual(Season.AUTUMN.value, "autumn")
        self.assertEqual(Season.WINTER.value, "winter")


class TestPlant(unittest.TestCase):
    """测试 Plant 类"""
    
    def setUp(self):
        """设置测试"""
        self.plant = Plant(
            name="测试植物",
            plant_type=PlantType.TROPICAL,
            location="客厅",
            purchase_date=datetime(2025, 1, 1)
        )
    
    def test_create_plant(self):
        """测试创建植物"""
        self.assertEqual(self.plant.name, "测试植物")
        self.assertEqual(self.plant.plant_type, PlantType.TROPICAL)
        self.assertEqual(self.plant.location, "客厅")
    
    def test_get_info(self):
        """测试获取植物信息"""
        info = self.plant.get_info()
        
        self.assertEqual(info["name"], "测试植物")
        self.assertEqual(info["type"], "tropical")
        self.assertEqual(info["type_name"], "热带植物")
        self.assertEqual(info["location"], "客厅")
        self.assertIn("age_days", info)
    
    def test_record_watering(self):
        """测试记录浇水"""
        self.assertIsNone(self.plant.last_watered)
        
        self.plant.record_watering()
        self.assertIsNotNone(self.plant.last_watered)
        
        # 记录多次浇水
        self.plant.record_watering(amount_ml=200)
        self.assertEqual(len(self.plant.care_log), 2)
    
    def test_record_fertilizing(self):
        """测试记录施肥"""
        self.assertIsNone(self.plant.last_fertilized)
        
        self.plant.record_fertilizing(fertilizer_type="氮肥")
        self.assertIsNotNone(self.plant.last_fertilized)
        self.assertEqual(len(self.plant.care_log), 1)
    
    def test_record_health_check(self):
        """测试记录健康检查"""
        self.plant.record_health_check(HealthStatus.GOOD, "状态良好")
        self.assertEqual(len(self.plant.health_history), 1)
        self.assertEqual(self.plant.health_history[0]["status"], "good")
    
    def test_get_care_history(self):
        """测试获取养护历史"""
        self.plant.record_watering()
        self.plant.record_fertilizing()
        
        history = self.plant.get_care_history(days=30)
        self.assertEqual(len(history), 2)


class TestPlantCareScheduler(unittest.TestCase):
    """测试 PlantCareScheduler 类"""
    
    def setUp(self):
        """设置测试"""
        self.scheduler = PlantCareScheduler()
        
        self.plant1 = Plant(
            name="龟背竹",
            plant_type=PlantType.TROPICAL,
            location="客厅"
        )
        self.plant2 = Plant(
            name="仙人掌",
            plant_type=PlantType.CACTUS,
            location="阳台"
        )
        
        self.scheduler.add_plant(self.plant1)
        self.scheduler.add_plant(self.plant2)
    
    def test_add_plant(self):
        """测试添加植物"""
        self.assertEqual(len(self.scheduler.plants), 2)
    
    def test_remove_plant(self):
        """测试移除植物"""
        result = self.scheduler.remove_plant("龟背竹")
        self.assertTrue(result)
        self.assertEqual(len(self.scheduler.plants), 1)
        
        result = self.scheduler.remove_plant("不存在的植物")
        self.assertFalse(result)
    
    def test_get_plant(self):
        """测试获取植物"""
        plant = self.scheduler.get_plant("龟背竹")
        self.assertIsNotNone(plant)
        self.assertEqual(plant.name, "龟背竹")
        
        plant = self.scheduler.get_plant("不存在的植物")
        self.assertIsNone(plant)
    
    def test_get_watering_schedule(self):
        """测试获取浇水计划"""
        schedule = self.scheduler.get_watering_schedule(
            season=Season.SPRING,
            indoor_temperature=22,
            humidity=50
        )
        
        self.assertEqual(len(schedule), 2)
        self.assertIn("龟背竹", [s["plant_name"] for s in schedule])
        self.assertIn("仙人掌", [s["plant_name"] for s in schedule])
        
        # 检查仙人掌浇水频率更低（间隔更长）
        cactus_schedule = [s for s in schedule if s["plant_name"] == "仙人掌"][0]
        monstera_schedule = [s for s in schedule if s["plant_name"] == "龟背竹"][0]
        
        self.assertGreaterEqual(cactus_schedule["days_until_watering"], 
                               monstera_schedule["days_until_watering"])
    
    def test_get_watering_schedule_with_last_watered(self):
        """测试有上次浇水记录的浇水计划"""
        self.plant1.record_watering(datetime.now() - timedelta(days=5))
        self.plant2.record_watering(datetime.now() - timedelta(days=20))
        
        schedule = self.scheduler.get_watering_schedule(season=Season.SUMMER)
        
        # 仙人掌应该更紧急（上次浇水时间更早）
        cactus_schedule = [s for s in schedule if s["plant_name"] == "仙人掌"][0]
        self.assertEqual(cactus_schedule["urgency"], "high")
    
    def test_get_fertilizing_schedule(self):
        """测试获取施肥计划"""
        schedule = self.scheduler.get_fertilizing_schedule()
        
        self.assertEqual(len(schedule), 2)
        self.assertIn("龟背竹", [s["plant_name"] for s in schedule])
        self.assertIn("仙人掌", [s["plant_name"] for s in schedule])
    
    def test_get_seasonal_care_tips(self):
        """测试获取季节性养护建议"""
        for season in [Season.SPRING, Season.SUMMER, Season.AUTUMN, Season.WINTER]:
            tips = self.scheduler.get_seasonal_care_tips(season)
            self.assertIn("title", tips)
            self.assertIn("general_tips", tips)
            self.assertIsInstance(tips["general_tips"], list)
            self.assertGreater(len(tips["general_tips"]), 0)


class TestCalculateWaterNeeds(unittest.TestCase):
    """测试计算需水量"""
    
    def test_calculate_water_needs_spring(self):
        """测试春季需水量"""
        result = calculate_water_needs(
            PlantType.TROPICAL,
            pot_diameter_cm=20,
            season=Season.SPRING,
            temperature=22,
            humidity=50
        )
        
        self.assertIn("water_amount_ml", result)
        self.assertIn("watering_frequency_days", result)
        self.assertIn("recommendations", result)
        self.assertGreater(result["water_amount_ml"], 0)
    
    def test_calculate_water_needs_seasonal_variation(self):
        """测试季节变化对需水量的影响"""
        spring_result = calculate_water_needs(
            PlantType.TROPICAL,
            pot_diameter_cm=20,
            season=Season.SPRING
        )
        
        summer_result = calculate_water_needs(
            PlantType.TROPICAL,
            pot_diameter_cm=20,
            season=Season.SUMMER
        )
        
        winter_result = calculate_water_needs(
            PlantType.TROPICAL,
            pot_diameter_cm=20,
            season=Season.WINTER
        )
        
        # 夏季需水量应该最大，冬季最小
        self.assertGreater(summer_result["water_amount_ml"], spring_result["water_amount_ml"])
        self.assertLess(winter_result["water_amount_ml"], spring_result["water_amount_ml"])
    
    def test_calculate_water_needs_temperature_effect(self):
        """测试温度对需水量的影响"""
        cool_result = calculate_water_needs(
            PlantType.TROPICAL,
            pot_diameter_cm=20,
            temperature=15
        )
        
        hot_result = calculate_water_needs(
            PlantType.TROPICAL,
            pot_diameter_cm=20,
            temperature=30
        )
        
        # 高温时需水量应该更大
        self.assertGreater(hot_result["water_amount_ml"], cool_result["water_amount_ml"])
    
    def test_calculate_water_needs_pot_size(self):
        """测试花盆大小对需水量的影响"""
        small_pot = calculate_water_needs(
            PlantType.TROPICAL,
            pot_diameter_cm=10
        )
        
        large_pot = calculate_water_needs(
            PlantType.TROPICAL,
            pot_diameter_cm=30
        )
        
        # 大花盆需要更多水
        self.assertGreater(large_pot["water_amount_ml"], small_pot["water_amount_ml"])


class TestAnalyzeLightRequirements(unittest.TestCase):
    """测试光照需求分析"""
    
    def test_adequate_light(self):
        """测试适宜光照"""
        result = analyze_light_requirements(
            PlantType.FERN,
            LightLevel.LOW
        )
        
        self.assertEqual(result["status"], "适宜")
        self.assertEqual(len(result["suggestions"]), 3)
    
    def test_insufficient_light(self):
        """测试光照不足"""
        result = analyze_light_requirements(
            PlantType.CACTUS,
            LightLevel.LOW
        )
        
        self.assertEqual(result["status"], "不足")
        self.assertIn("将植物移至更明亮的位置", result["suggestions"])
    
    def test_excessive_light(self):
        """测试光照过强"""
        result = analyze_light_requirements(
            PlantType.FERN,
            LightLevel.DIRECT
        )
        
        self.assertEqual(result["status"], "过强")
        self.assertIn("移至稍阴的位置", result["suggestions"])


class TestGetSeasonalFertilizerRecommendation(unittest.TestCase):
    """测试季节性施肥建议"""
    
    def test_spring_fertilizer(self):
        """测试春季施肥"""
        result = get_seasonal_fertilizer_recommendation(
            PlantType.TROPICAL,
            Season.SPRING,
            GrowthStage.VEGETATIVE
        )
        
        self.assertEqual(result["season"], "spring")
        self.assertIn("seasonal_advice", result)
        self.assertIn("stage_formula", result)
    
    def test_winter_fertilizer(self):
        """测试冬季施肥"""
        result = get_seasonal_fertilizer_recommendation(
            PlantType.CACTUS,
            Season.WINTER,
            GrowthStage.DORMANT
        )
        
        self.assertEqual(result["season"], "winter")
        # 冬季应该减少或停止施肥
        advice = result["seasonal_advice"]
        self.assertIn("停止", advice["type"])


class TestDiagnosePlantIssue(unittest.TestCase):
    """测试植物问题诊断"""
    
    def test_diagnose_single_symptom(self):
        """测试单一症状诊断"""
        result = diagnose_plant_issue(
            PlantType.TROPICAL,
            ["叶尖枯黄"]
        )
        
        self.assertEqual(len(result["diagnoses"]), 1)
        self.assertEqual(result["diagnoses"][0]["symptom"], "叶尖枯黄")
        self.assertIn("possible_causes", result["diagnoses"][0])
        self.assertIn("solutions", result["diagnoses"][0])
    
    def test_diagnose_multiple_symptoms(self):
        """测试多症状诊断"""
        result = diagnose_plant_issue(
            PlantType.CACTUS,
            ["根部腐烂", "叶片发黄", "生长缓慢"]
        )
        
        self.assertEqual(len(result["diagnoses"]), 3)
        
        # 检查是否按严重程度排序
        severity_order = {"severe": 0, "moderate": 1, "minor": 2}
        severities = [d["severity"] for d in result["diagnoses"]]
        self.assertEqual(severities, sorted(severities, key=lambda x: severity_order[x]))
    
    def test_diagnose_includes_plant_type_info(self):
        """测试诊断包含植物类型信息"""
        result = diagnose_plant_issue(
            PlantType.SUCCULENT,
            ["叶片脱落"]
        )
        
        self.assertIn("common_issues_for_type", result)
        self.assertIn("general_care_tips", result)


class TestCreatePlantCareCalendar(unittest.TestCase):
    """测试植物养护日历"""
    
    def test_create_calendar(self):
        """测试创建日历"""
        plant = Plant(
            name="测试植物",
            plant_type=PlantType.TROPICAL,
            location="客厅"
        )
        
        calendar = create_plant_care_calendar(
            year=2026,
            month=5,
            plants=[plant],
            location="north"
        )
        
        self.assertEqual(calendar["year"], 2026)
        self.assertEqual(calendar["month"], 5)
        self.assertEqual(calendar["season"], "spring")
        self.assertIn("tasks", calendar)
        self.assertIn("monthly_summary", calendar)
    
    def test_calendar_seasons_north(self):
        """测试北半球季节"""
        for month, expected_season in [
            (3, "spring"), (6, "summer"), 
            (9, "autumn"), (12, "winter")
        ]:
            calendar = create_plant_care_calendar(
                year=2026,
                month=month,
                plants=[],
                location="north"
            )
            self.assertEqual(calendar["season"], expected_season)
    
    def test_calendar_seasons_south(self):
        """测试南半球季节"""
        for month, expected_season in [
            (9, "spring"), (12, "summer"), 
            (3, "autumn"), (6, "winter")
        ]:
            calendar = create_plant_care_calendar(
                year=2026,
                month=month,
                plants=[],
                location="south"
            )
            self.assertEqual(calendar["season"], expected_season)


class TestQuickWaterCheck(unittest.TestCase):
    """测试快速浇水检查"""
    
    def test_needs_water(self):
        """测试需要浇水"""
        result = quick_water_check(
            PlantType.TROPICAL,
            days_since_watering=10,
            season=Season.SPRING
        )
        
        self.assertTrue(result["needs_water"])
        self.assertIn("立即浇水", result["urgency"])
    
    def test_doesnt_need_water(self):
        """测试不需要浇水"""
        result = quick_water_check(
            PlantType.TROPICAL,
            days_since_watering=1,
            season=Season.SPRING
        )
        
        self.assertFalse(result["needs_water"])
        self.assertEqual(result["urgency"], "暂不需要")
    
    def test_seasonal_adjustment(self):
        """测试季节调整"""
        spring_result = quick_water_check(
            PlantType.CACTUS,
            days_since_watering=14,
            season=Season.SPRING
        )
        
        summer_result = quick_water_check(
            PlantType.CACTUS,
            days_since_watering=14,
            season=Season.SUMMER
        )
        
        # 夏季应该更早需要浇水
        self.assertLess(summer_result["next_watering_in_days"], 
                       spring_result["next_watering_in_days"])


class TestUtilityFunctions(unittest.TestCase):
    """测试工具函数"""
    
    def test_get_plant_database_info(self):
        """测试获取植物信息"""
        info = get_plant_database_info(PlantType.ORCHID)
        
        self.assertEqual(info["name"], "兰花")
        self.assertIn("water_frequency", info)
        self.assertIn("light_requirement", info)
    
    def test_list_all_plant_types(self):
        """测试列出所有植物类型"""
        types = list_all_plant_types()
        
        self.assertGreater(len(types), 0)
        self.assertEqual(len(types), len(PlantType))
        
        for t in types:
            self.assertIn("type", t)
            self.assertIn("name", t)


if __name__ == "__main__":
    unittest.main()