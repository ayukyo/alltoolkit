"""
Coffee Utils 测试文件

测试咖啡冲泡工具库的所有功能
"""

import unittest
from mod import (
    BrewMethod, GrindSize, RoastLevel, CoffeeOrigin,
    CoffeeCalculator, CaffeineCalculator, BrewRecommender,
    WaterQualityAnalyzer, RoastAnalyzer, OriginInfo,
    calculate_ratio, estimate_caffeine, get_brew_recipe,
    golden_cup_check, search_coffee_by_flavor,
    BREW_PARAMETERS, GRIND_SIZES, ROAST_CHARACTERISTICS, COFFEE_ORIGINS,
)


class TestCoffeeCalculator(unittest.TestCase):
    """测试咖啡计算器"""
    
    def test_calculate_ratio(self):
        """测试比例计算"""
        self.assertEqual(CoffeeCalculator.calculate_ratio(15, 225), "1:15.0")
        self.assertEqual(CoffeeCalculator.calculate_ratio(18, 36), "1:2.0")
        self.assertEqual(CoffeeCalculator.calculate_ratio(20, 300), "1:15.0")
    
    def test_calculate_ratio_zero_coffee(self):
        """测试咖啡量为0的情况"""
        self.assertEqual(CoffeeCalculator.calculate_ratio(0, 225), "1:0")
    
    def test_calculate_coffee_for_water(self):
        """测试根据水量计算咖啡量"""
        self.assertAlmostEqual(CoffeeCalculator.calculate_coffee_for_water(225, "1:15"), 15.0, places=1)
        self.assertAlmostEqual(CoffeeCalculator.calculate_coffee_for_water(300, "1:15"), 20.0, places=1)
        self.assertAlmostEqual(CoffeeCalculator.calculate_coffee_for_water(36, "1:2"), 18.0, places=1)
    
    def test_calculate_water_for_coffee(self):
        """测试根据咖啡量计算水量"""
        self.assertEqual(CoffeeCalculator.calculate_water_for_coffee(15, "1:15"), 225.0)
        self.assertEqual(CoffeeCalculator.calculate_water_for_coffee(18, "1:2"), 36.0)
        self.assertEqual(CoffeeCalculator.calculate_water_for_coffee(20, "1:16"), 320.0)
    
    def test_calculate_extraction_yield(self):
        """测试萃取率计算"""
        # 典型手冲参数
        extraction = CoffeeCalculator.calculate_extraction_yield(15, 225, 1.25)
        self.assertAlmostEqual(extraction, 18.75, places=2)
        
        # 浓缩咖啡
        extraction = CoffeeCalculator.calculate_extraction_yield(18, 36, 10.0)
        self.assertAlmostEqual(extraction, 20.0, places=2)
    
    def test_calculate_extraction_yield_zero_coffee(self):
        """测试咖啡量为0的萃取率计算"""
        extraction = CoffeeCalculator.calculate_extraction_yield(0, 225, 1.25)
        self.assertEqual(extraction, 0.0)
    
    def test_calculate_tds(self):
        """测试TDS计算"""
        tds = CoffeeCalculator.calculate_tds(15, 225, 19.0)
        self.assertAlmostEqual(tds, 1.27, places=2)
        
        tds = CoffeeCalculator.calculate_tds(18, 36, 20.0)
        self.assertAlmostEqual(tds, 10.0, places=2)
    
    def test_is_golden_cup(self):
        """测试金杯标准检查"""
        # 在金杯范围内
        result = CoffeeCalculator.is_golden_cup(19.0, 1.25)
        self.assertTrue(result["is_golden_cup"])
        self.assertTrue(result["extraction"]["in_range"])
        self.assertTrue(result["tds"]["in_range"])
        
        # 萃取不足
        result = CoffeeCalculator.is_golden_cup(16.0, 1.25)
        self.assertFalse(result["is_golden_cup"])
        self.assertFalse(result["extraction"]["in_range"])
        self.assertEqual(result["extraction"]["status"], "under")
        
        # 过度萃取
        result = CoffeeCalculator.is_golden_cup(24.0, 1.25)
        self.assertFalse(result["is_golden_cup"])
        self.assertEqual(result["extraction"]["status"], "over")
        
        # 浓度太低
        result = CoffeeCalculator.is_golden_cup(19.0, 1.0)
        self.assertFalse(result["is_golden_cup"])
        self.assertEqual(result["tds"]["status"], "weak")
        
        # 浓度太高
        result = CoffeeCalculator.is_golden_cup(19.0, 1.5)
        self.assertFalse(result["is_golden_cup"])
        self.assertEqual(result["tds"]["status"], "strong")
    
    def test_calculate_bloom_water(self):
        """测试闷蒸水量计算"""
        self.assertEqual(CoffeeCalculator.calculate_bloom_water(15), 30.0)
        self.assertEqual(CoffeeCalculator.calculate_bloom_water(18, 3), 54.0)
    
    def test_calculate_bloom_time(self):
        """测试闷蒸时间建议"""
        self.assertEqual(CoffeeCalculator.calculate_bloom_time(RoastLevel.LIGHT), 45)
        self.assertEqual(CoffeeCalculator.calculate_bloom_time(RoastLevel.MEDIUM), 35)
        self.assertEqual(CoffeeCalculator.calculate_bloom_time(RoastLevel.DARK), 25)


class TestCaffeineCalculator(unittest.TestCase):
    """测试咖啡因计算器"""
    
    def test_estimate_caffeine(self):
        """测试咖啡因估算"""
        # 手冲咖啡
        info = CaffeineCalculator.estimate_caffeine(15, BrewMethod.POUR_OVER)
        self.assertGreater(info.mg_per_cup, 100)
        self.assertLess(info.mg_per_cup, 200)
        
        # 浓缩咖啡
        info = CaffeineCalculator.estimate_caffeine(18, BrewMethod.ESPRESSO)
        self.assertGreater(info.mg_per_cup, 150)
        
        # 冷萃咖啡（咖啡因含量最高）
        info = CaffeineCalculator.estimate_caffeine(30, BrewMethod.COLD_BREW)
        self.assertGreater(info.mg_per_cup, 300)
    
    def test_estimate_caffeine_by_roast(self):
        """测试不同烘焙程度对咖啡因的影响"""
        light = CaffeineCalculator.estimate_caffeine(15, BrewMethod.POUR_OVER, RoastLevel.LIGHT)
        dark = CaffeineCalculator.estimate_caffeine(15, BrewMethod.POUR_OVER, RoastLevel.DARK)
        # 浅烘咖啡因含量应该高于深烘
        self.assertGreater(light.mg_per_cup, dark.mg_per_cup)
    
    def test_daily_limit_check(self):
        """测试每日咖啡因限制检查"""
        # 安全范围
        result = CaffeineCalculator.daily_limit_check(200)
        self.assertEqual(result["status"], "safe")
        self.assertGreater(result["remaining_mg"], 100)
        
        # 接近限制
        result = CaffeineCalculator.daily_limit_check(350)
        self.assertEqual(result["status"], "caution")
        
        # 超过限制
        result = CaffeineCalculator.daily_limit_check(450)
        self.assertEqual(result["status"], "exceeded")
    
    def test_half_life_hours(self):
        """测试咖啡因半衰期计算"""
        # 从100mg降到50mg需要约5小时
        hours = CaffeineCalculator.half_life_hours(100, 50, 5.0)
        self.assertAlmostEqual(hours, 5.0, places=1)
        
        # 从200mg降到50mg需要约10小时
        hours = CaffeineCalculator.half_life_hours(200, 50, 5.0)
        self.assertAlmostEqual(hours, 10.0, places=1)
        
        # 已经低于目标
        hours = CaffeineCalculator.half_life_hours(30, 50, 5.0)
        self.assertEqual(hours, 0.0)


class TestBrewRecommender(unittest.TestCase):
    """测试冲泡推荐器"""
    
    def test_get_brew_parameters(self):
        """测试获取冲泡参数"""
        params = BrewRecommender.get_brew_parameters(BrewMethod.ESPRESSO)
        self.assertEqual(params.method, BrewMethod.ESPRESSO)
        self.assertEqual(params.grind_size, GrindSize.FINE)
        self.assertEqual(params.ratio, "1:2")
        
        params = BrewRecommender.get_brew_parameters(BrewMethod.FRENCH_PRESS)
        self.assertEqual(params.grind_size, GrindSize.COARSE)
    
    def test_get_grind_recommendation(self):
        """测试获取研磨建议"""
        rec = BrewRecommender.get_grind_recommendation(GrindSize.MEDIUM_FINE)
        self.assertEqual(rec.size, GrindSize.MEDIUM_FINE)
        self.assertIn("砂糖", rec.description)
        self.assertIsInstance(rec.particle_size_um, tuple)
        self.assertEqual(len(rec.particle_size_um), 2)
    
    def test_recommend_for_cups(self):
        """测试多杯推荐"""
        result = BrewRecommender.recommend_for_cups(BrewMethod.POUR_OVER, 2, 240)
        self.assertEqual(result["cups"], 2)
        self.assertEqual(result["total_water_ml"], 480)
        self.assertGreater(result["total_coffee_g"], 30)
    
    def test_adjust_for_taste(self):
        """测试口味调整"""
        base = BrewRecommender.get_brew_parameters(BrewMethod.POUR_OVER)
        
        # 更浓
        stronger = BrewRecommender.adjust_for_taste(BrewMethod.POUR_OVER, "stronger")
        self.assertGreater(stronger["coffee_grams"], base.coffee_grams)
        
        # 更淡
        weaker = BrewRecommender.adjust_for_taste(BrewMethod.POUR_OVER, "weaker")
        self.assertLess(weaker["coffee_grams"], base.coffee_grams)
        
        # 平衡
        balanced = BrewRecommender.adjust_for_taste(BrewMethod.POUR_OVER, "balanced")
        self.assertEqual(balanced["coffee_grams"], base.coffee_grams)


class TestWaterQualityAnalyzer(unittest.TestCase):
    """测试水质分析器"""
    
    def test_assess_water_ideal(self):
        """测试理想水质评估"""
        result = WaterQualityAnalyzer.assess_water(100, 7.0, 50)
        self.assertEqual(result["hardness"]["status"], "ideal")
        self.assertEqual(result["ph"]["status"], "ideal")
        self.assertEqual(result["alkalinity"]["status"], "ideal")
        self.assertEqual(result["overall"], "good")
    
    def test_assess_water_soft_acidic(self):
        """测试软水和酸性水评估"""
        result = WaterQualityAnalyzer.assess_water(30, 6.0)
        self.assertEqual(result["hardness"]["status"], "soft")
        self.assertEqual(result["ph"]["status"], "acidic")
        self.assertIn("adjustment", result["overall"])
    
    def test_assess_water_hard_alkaline(self):
        """测试硬水和碱性水评估"""
        result = WaterQualityAnalyzer.assess_water(250, 8.0)
        self.assertEqual(result["hardness"]["status"], "hard")
        self.assertEqual(result["ph"]["status"], "alkaline")
    
    def test_magnesium_benefit(self):
        """测试镁含量评估"""
        result = WaterQualityAnalyzer.magnesium_benefit(30)
        self.assertEqual(result["magnesium_level"], "optimal")
        
        result = WaterQualityAnalyzer.magnesium_benefit(10)
        self.assertEqual(result["magnesium_level"], "low")
        
        result = WaterQualityAnalyzer.magnesium_benefit(150)
        self.assertEqual(result["magnesium_level"], "high")


class TestRoastAnalyzer(unittest.TestCase):
    """测试烘焙分析器"""
    
    def test_get_roast_characteristics(self):
        """测试获取烘焙特性"""
        chars = RoastAnalyzer.get_roast_characteristics(RoastLevel.LIGHT)
        self.assertIn("高", chars["acidity"])
        self.assertIn("清淡", chars["body"])
        
        chars = RoastAnalyzer.get_roast_characteristics(RoastLevel.DARK)
        self.assertIn("低", chars["acidity"])
        self.assertIn("厚重", chars["body"])
    
    def test_recommend_brew_temp(self):
        """测试烘焙程度推荐水温"""
        temp = RoastAnalyzer.recommend_brew_temp(RoastLevel.LIGHT)
        self.assertEqual(temp, (88, 93))
        
        temp = RoastAnalyzer.recommend_brew_temp(RoastLevel.DARK)
        self.assertEqual(temp, (93, 96))
    
    def test_suggest_origin_for_roast(self):
        """测试烘焙程度推荐产地"""
        origins = RoastAnalyzer.suggest_origin_for_roast(RoastLevel.LIGHT)
        self.assertIn(CoffeeOrigin.ETHIOPIA, origins)
        self.assertIn(CoffeeOrigin.KENYA, origins)
        
        origins = RoastAnalyzer.suggest_origin_for_roast(RoastLevel.DARK)
        self.assertIn(CoffeeOrigin.SUMATRA, origins)


class TestOriginInfo(unittest.TestCase):
    """测试产地信息查询"""
    
    def test_get_origin_info(self):
        """测试获取产地信息"""
        info = OriginInfo.get_origin_info(CoffeeOrigin.ETHIOPIA)
        self.assertEqual(info.name, "埃塞俄比亚")
        self.assertIn("花香", info.flavor_notes)
        self.assertEqual(info.acidity, "高")
        
        info = OriginInfo.get_origin_info(CoffeeOrigin.BRAZIL)
        self.assertEqual(info.name, "巴西")
        self.assertIn("坚果", info.flavor_notes)
        self.assertEqual(info.acidity, "低")
    
    def test_search_by_flavor(self):
        """测试风味搜索"""
        origins = OriginInfo.search_by_flavor("巧克力")
        self.assertIn(CoffeeOrigin.BRAZIL, origins)
        self.assertIn(CoffeeOrigin.COLOMBIA, origins)
        
        origins = OriginInfo.search_by_flavor("花香")
        self.assertIn(CoffeeOrigin.ETHIOPIA, origins)
        self.assertIn(CoffeeOrigin.PANAMA, origins)
    
    def test_search_by_acidity(self):
        """测试酸度搜索"""
        origins = OriginInfo.search_by_acidity("high")
        self.assertIn(CoffeeOrigin.ETHIOPIA, origins)
        self.assertIn(CoffeeOrigin.KENYA, origins)
        
        origins = OriginInfo.search_by_acidity("low")
        self.assertIn(CoffeeOrigin.BRAZIL, origins)
        self.assertIn(CoffeeOrigin.SUMATRA, origins)
    
    def test_search_by_body(self):
        """测试醇厚度搜索"""
        origins = OriginInfo.search_by_body("full")
        self.assertIn(CoffeeOrigin.SUMATRA, origins)
        
        origins = OriginInfo.search_by_body("light")
        self.assertIn(CoffeeOrigin.ETHIOPIA, origins)


class TestConvenienceFunctions(unittest.TestCase):
    """测试便捷函数"""
    
    def test_calculate_ratio_function(self):
        """测试比例计算便捷函数"""
        self.assertEqual(calculate_ratio(15, 225), "1:15.0")
        self.assertEqual(calculate_ratio(18, 36), "1:2.0")
    
    def test_estimate_caffeine_function(self):
        """测试咖啡因估算便捷函数"""
        info = estimate_caffeine(15, "pour_over")
        self.assertGreater(info.mg_per_cup, 100)
        
        info = estimate_caffeine(18, "espresso")
        self.assertGreater(info.mg_per_cup, 150)
    
    def test_get_brew_recipe_function(self):
        """测试冲泡配方便捷函数"""
        recipe = get_brew_recipe("french_press", 2)
        self.assertEqual(recipe["cups"], 2)
        self.assertIn("total_coffee_g", recipe)
    
    def test_golden_cup_check_function(self):
        """测试金杯检查便捷函数"""
        result = golden_cup_check(15, 225, 1.25)
        self.assertIn("is_golden_cup", result)
    
    def test_search_coffee_by_flavor_function(self):
        """测试风味搜索便捷函数"""
        origins = search_coffee_by_flavor("巧克力")
        self.assertIsInstance(origins, list)
        self.assertGreater(len(origins), 0)


class TestBrewParameters(unittest.TestCase):
    """测试冲泡参数常量"""
    
    def test_all_brew_methods_have_parameters(self):
        """测试所有冲泡方式都有参数"""
        for method in BrewMethod:
            self.assertIn(method, BREW_PARAMETERS, f"{method} missing from BREW_PARAMETERS")
    
    def test_brew_parameters_structure(self):
        """测试冲泡参数结构"""
        required_keys = ["grind", "ratio", "water_ml", 
                        "temperature", "time", "extraction", "tds"]
        # coffee_per_cup_g 或 coffee_per_shot_g 都可接受
        coffee_key_options = ["coffee_per_cup_g", "coffee_per_shot_g"]
        for method, params in BREW_PARAMETERS.items():
            for key in required_keys:
                self.assertIn(key, params, f"{key} missing in {method}")
            # 至少有一个咖啡量键存在
            has_coffee_key = any(k in params for k in coffee_key_options)
            self.assertTrue(has_coffee_key, f"coffee_per_cup_g or coffee_per_shot_g missing in {method}")


class TestGrindSizes(unittest.TestCase):
    """测试研磨度常量"""
    
    def test_all_grind_sizes_defined(self):
        """测试所有研磨度都已定义"""
        for size in GrindSize:
            self.assertIn(size, GRIND_SIZES, f"{size} missing from GRIND_SIZES")
    
    def test_grind_size_structure(self):
        """测试研磨度结构"""
        for size, rec in GRIND_SIZES.items():
            self.assertEqual(rec.size, size)
            self.assertIsInstance(rec.description, str)
            self.assertIsInstance(rec.particle_size_um, tuple)
            self.assertEqual(len(rec.particle_size_um), 2)
            self.assertIsInstance(rec.mesh_size, tuple)
            self.assertEqual(len(rec.mesh_size), 2)


class TestRoastCharacteristics(unittest.TestCase):
    """测试烘焙特性常量"""
    
    def test_all_roast_levels_defined(self):
        """测试所有烘焙程度都已定义"""
        for level in RoastLevel:
            self.assertIn(level, ROAST_CHARACTERISTICS, f"{level} missing")
    
    def test_roast_characteristics_structure(self):
        """测试烘焙特性结构"""
        required_keys = ["color", "surface", "flavor", "acidity", "body", 
                        "caffeine", "brew_temp", "notes"]
        for level, chars in ROAST_CHARACTERISTICS.items():
            for key in required_keys:
                self.assertIn(key, chars, f"{key} missing in {level}")


class TestCoffeeOrigins(unittest.TestCase):
    """测试咖啡产地常量"""
    
    def test_all_origins_defined(self):
        """测试所有产地都已定义"""
        for origin in CoffeeOrigin:
            self.assertIn(origin, COFFEE_ORIGINS, f"{origin} missing")
    
    def test_coffee_origin_structure(self):
        """测试产地信息结构"""
        for origin, bean in COFFEE_ORIGINS.items():
            self.assertEqual(bean.origin, origin)
            self.assertIsInstance(bean.name, str)
            self.assertIsInstance(bean.altitude_range, tuple)
            self.assertEqual(len(bean.altitude_range), 2)
            self.assertIsInstance(bean.flavor_notes, list)
            self.assertGreater(len(bean.flavor_notes), 0)


if __name__ == "__main__":
    unittest.main(verbosity=2)