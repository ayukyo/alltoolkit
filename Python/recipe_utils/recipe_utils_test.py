"""
recipe_utils 测试文件
"""

import unittest
import sys
import os

# 添加模块路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from recipe_utils.mod import (
    Recipe,
    Ingredient,
    RecipeStep,
    NutritionInfo,
    UnitType,
    IngredientCategory,
    DietaryRestriction,
    DifficultyLevel,
    MealType,
    RecipeScaler,
    UnitConverter,
    NutritionCalculator,
    IngredientSubstitutor,
    ShoppingListGenerator,
    RecipeParser,
    CostCalculator,
    RecipeAnalyzer,
    scale_recipe,
    convert_unit,
    get_nutrition,
    get_substitutions,
    analyze_recipe,
    generate_shopping_list,
    parse_ingredient,
    estimate_recipe_cost,
    get_common_conversions,
    get_example_recipe,
    UNIT_CONVERSIONS,
    INGREDIENT_DENSITY,
    NUTRITION_DATABASE,
    INGREDIENT_SUBSTITUTIONS,
)


class TestUnitType(unittest.TestCase):
    """测试 UnitType 枚举"""
    
    def test_volume_units(self):
        """测试体积单位"""
        self.assertEqual(UnitType.MILLILITER.value, "ml")
        self.assertEqual(UnitType.CUP.value, "cup")
        self.assertEqual(UnitType.TABLESPOON.value, "tbsp")
        self.assertEqual(UnitType.TEASPOON.value, "tsp")
    
    def test_weight_units(self):
        """测试重量单位"""
        self.assertEqual(UnitType.GRAM.value, "g")
        self.assertEqual(UnitType.KILOGRAM.value, "kg")
        self.assertEqual(UnitType.OUNCE.value, "oz")
        self.assertEqual(UnitType.POUND.value, "lb")


class TestIngredient(unittest.TestCase):
    """测试 Ingredient 类"""
    
    def test_create_ingredient(self):
        """测试创建配料"""
        ing = Ingredient("面粉", 100, UnitType.GRAM)
        self.assertEqual(ing.name, "面粉")
        self.assertEqual(ing.amount, 100)
        self.assertEqual(ing.unit, UnitType.GRAM)
    
    def test_to_grams(self):
        """测试转换为克"""
        # 重量单位
        ing1 = Ingredient("测试", 100, UnitType.GRAM)
        self.assertEqual(ing1.to_grams(), 100)
        
        ing2 = Ingredient("测试", 1, UnitType.KILOGRAM)
        self.assertEqual(ing2.to_grams(), 1000)
        
        ing3 = Ingredient("测试", 1, UnitType.POUND)
        self.assertAlmostEqual(ing3.to_grams(), 453.592, places=1)
    
    def test_to_milliliters(self):
        """测试转换为毫升"""
        ing1 = Ingredient("水", 100, UnitType.MILLILITER)
        self.assertEqual(ing1.to_milliliters(), 100)
        
        ing2 = Ingredient("水", 1, UnitType.LITER)
        self.assertEqual(ing2.to_milliliters(), 1000)
        
        ing3 = Ingredient("水", 1, UnitType.CUP)
        self.assertAlmostEqual(ing3.to_milliliters(), 236.588, places=1)


class TestRecipe(unittest.TestCase):
    """测试 Recipe 类"""
    
    def test_create_recipe(self):
        """测试创建食谱"""
        recipe = get_example_recipe()
        self.assertEqual(recipe.name, "番茄炒蛋")
        self.assertEqual(recipe.servings, 2)
        self.assertEqual(len(recipe.ingredients), 6)
        self.assertEqual(len(recipe.steps), 6)
    
    def test_total_time(self):
        """测试总时间计算"""
        recipe = Recipe(
            name="测试",
            servings=1,
            ingredients=[],
            steps=[],
            prep_time_minutes=15,
            cook_time_minutes=30
        )
        self.assertEqual(recipe.total_time_minutes, 45)
    
    def test_scale_recipe(self):
        """测试缩放食谱"""
        recipe = Recipe(
            name="测试",
            servings=2,
            ingredients=[
                Ingredient("面粉", 100, UnitType.GRAM),
                Ingredient("鸡蛋", 2, UnitType.PIECE),
            ],
            steps=[]
        )
        scaled = recipe.scale(4)
        self.assertEqual(scaled.servings, 4)
        self.assertEqual(scaled.ingredients[0].amount, 200)
        self.assertEqual(scaled.ingredients[1].amount, 4)


class TestRecipeScaler(unittest.TestCase):
    """测试 RecipeScaler 类"""
    
    def test_scale_recipe(self):
        """测试缩放食谱"""
        recipe = get_example_recipe()
        scaled = RecipeScaler.scale_recipe(recipe, 4)
        self.assertEqual(scaled.servings, 4)
        # 鸡蛋从3个变成6个
        self.assertEqual(scaled.ingredients[0].amount, 6)
    
    def test_scale_ingredient(self):
        """测试缩放单个配料"""
        ing = Ingredient("面粉", 100, UnitType.GRAM)
        scaled = RecipeScaler.scale_ingredient(ing, 1.5)
        self.assertEqual(scaled.amount, 150)
    
    def test_smart_round(self):
        """测试智能舍入"""
        # 整数单位
        self.assertEqual(RecipeScaler.smart_round(3.7, UnitType.PIECE), 4)
        
        # 大于1的数值
        self.assertEqual(RecipeScaler.smart_round(1.3, UnitType.GRAM), 1.25)
        
        # 小于0.25的数值
        self.assertAlmostEqual(RecipeScaler.smart_round(0.12, UnitType.TEASPOON), 0.12, places=2)


class TestUnitConverter(unittest.TestCase):
    """测试 UnitConverter 类"""
    
    def test_convert_volume_units(self):
        """测试体积单位转换"""
        # 杯到毫升
        result, success = UnitConverter.convert(1, UnitType.CUP, UnitType.MILLILITER)
        self.assertTrue(success)
        self.assertAlmostEqual(result, 236.588, places=1)
        
        # 大匙到小匙
        result, success = UnitConverter.convert(1, UnitType.TABLESPOON, UnitType.TEASPOON)
        self.assertTrue(success)
        self.assertAlmostEqual(result, 3, places=0)
    
    def test_convert_weight_units(self):
        """测试重量单位转换"""
        # 公斤到克
        result, success = UnitConverter.convert(1, UnitType.KILOGRAM, UnitType.GRAM)
        self.assertTrue(success)
        self.assertEqual(result, 1000)
        
        # 磅到克
        result, success = UnitConverter.convert(1, UnitType.POUND, UnitType.GRAM)
        self.assertTrue(success)
        self.assertAlmostEqual(result, 453.592, places=1)
    
    def test_convert_volume_to_weight(self):
        """测试体积到重量转换"""
        # 1杯水约236克
        result, success = UnitConverter.convert(1, UnitType.CUP, UnitType.GRAM, "水")
        self.assertTrue(success)
        self.assertAlmostEqual(result, 236.588, places=0)
    
    def test_convert_temperature(self):
        """测试温度转换"""
        # 摄氏转华氏
        result = UnitConverter.convert_temperature(100, "celsius", "fahrenheit")
        self.assertEqual(result, 212)
        
        # 华氏转摄氏
        result = UnitConverter.convert_temperature(350, "fahrenheit", "celsius")
        self.assertAlmostEqual(result, 176.67, places=1)
    
    def test_get_common_conversions(self):
        """测试获取常用转换"""
        conversions = UnitConverter.get_common_conversions()
        self.assertIn("体积", conversions)
        self.assertIn("重量", conversions)
        self.assertIn("温度", conversions)


class TestNutritionCalculator(unittest.TestCase):
    """测试 NutritionCalculator 类"""
    
    def test_get_ingredient_nutrition(self):
        """测试获取配料营养信息"""
        ing = Ingredient("鸡蛋", 100, UnitType.GRAM)
        nutrition = NutritionCalculator.get_ingredient_nutrition(ing)
        self.assertEqual(nutrition.calories, 155)
        self.assertEqual(nutrition.protein, 12.6)
    
    def test_get_recipe_nutrition(self):
        """测试获取食谱营养信息"""
        recipe = get_example_recipe()
        nutrition = NutritionCalculator.get_recipe_nutrition(recipe)
        self.assertGreater(nutrition.calories, 0)
        self.assertGreater(nutrition.protein, 0)
    
    def test_get_nutrition_per_serving(self):
        """测试每份营养信息"""
        recipe = get_example_recipe()
        nutrition = NutritionCalculator.get_nutrition_per_serving(recipe)
        total = NutritionCalculator.get_recipe_nutrition(recipe)
        self.assertAlmostEqual(nutrition.calories, total.calories / 2, places=1)


class TestNutritionInfo(unittest.TestCase):
    """测试 NutritionInfo 类"""
    
    def test_add_nutrition(self):
        """测试营养信息相加"""
        n1 = NutritionInfo(calories=100, protein=10, carbs=20, fat=5, fiber=2, sodium=100)
        n2 = NutritionInfo(calories=50, protein=5, carbs=10, fat=2, fiber=1, sodium=50)
        total = n1 + n2
        self.assertEqual(total.calories, 150)
        self.assertEqual(total.protein, 15)
    
    def test_multiply_nutrition(self):
        """测试营养信息乘法"""
        n = NutritionInfo(calories=100, protein=10, carbs=20, fat=5, fiber=2, sodium=100)
        doubled = n * 2
        self.assertEqual(doubled.calories, 200)
        self.assertEqual(doubled.protein, 20)
    
    def test_to_dict(self):
        """测试转换为字典"""
        n = NutritionInfo(calories=100.5, protein=10.36, carbs=20.75, fat=5, fiber=2, sodium=100)
        d = n.to_dict()
        self.assertEqual(d["calories"], 100.5)
        self.assertEqual(d["protein"], 10.4)  # rounded


class TestIngredientSubstitutor(unittest.TestCase):
    """测试 IngredientSubstitutor 类"""
    
    def test_get_substitutions(self):
        """测试获取替代建议"""
        subs = IngredientSubstitutor.get_substitutions("鸡蛋")
        self.assertGreater(len(subs), 0)
        self.assertIn("substitute", subs[0])
        self.assertIn("ratio", subs[0])
    
    def test_get_substitutions_unknown(self):
        """测试未知配料的替代建议"""
        subs = IngredientSubstitutor.get_substitutions("未知食材")
        self.assertEqual(len(subs), 0)
    
    def test_find_vegan_alternative(self):
        """测试查找素食替代品"""
        alt = IngredientSubstitutor.find_vegan_alternative("鸡蛋")
        self.assertIsNotNone(alt)
        self.assertIn("豆腐", alt)
    
    def test_find_gluten_free_alternative(self):
        """测试查找无麸质替代品"""
        alt = IngredientSubstitutor.find_gluten_free_alternative("面粉")
        self.assertIsNotNone(alt)
        self.assertIn("杏仁粉", alt)


class TestShoppingListGenerator(unittest.TestCase):
    """测试 ShoppingListGenerator 类"""
    
    def test_generate_single_recipe(self):
        """测试生成单食谱购物清单"""
        recipe = get_example_recipe()
        shopping_list = ShoppingListGenerator.generate([recipe])
        
        self.assertEqual(shopping_list["total_ingredients"], 6)
        self.assertIn("by_category", shopping_list)
    
    def test_generate_multiple_recipes(self):
        """测试生成多食谱购物清单"""
        recipe1 = get_example_recipe()
        recipe2 = Recipe(
            name="煎蛋",
            servings=1,
            ingredients=[
                Ingredient("鸡蛋", 2, UnitType.PIECE),
                Ingredient("盐", 0.5, UnitType.TEASPOON),
            ],
            steps=[]
        )
        shopping_list = ShoppingListGenerator.generate([recipe1, recipe2])
        
        self.assertGreater(shopping_list["total_ingredients"], 0)
    
    def test_generate_with_servings(self):
        """测试缩放后生成购物清单"""
        recipe = get_example_recipe()
        shopping_list = ShoppingListGenerator.generate([recipe], [4])  # 4人份
        
        # 鸡蛋应该从3个变成6个
        for item in shopping_list["flat_list"]:
            if item["name"] == "鸡蛋":
                self.assertEqual(len(item["amounts"]), 1)
                self.assertEqual(item["amounts"][0]["amount"], 6)


class TestRecipeParser(unittest.TestCase):
    """测试 RecipeParser 类"""
    
    def test_parse_simple_ingredient(self):
        """测试解析简单配料"""
        ing = RecipeParser.parse_ingredient_line("100g 面粉")
        self.assertIsNotNone(ing)
        self.assertEqual(ing.amount, 100)
        self.assertEqual(ing.unit, UnitType.GRAM)
        self.assertEqual(ing.name, "面粉")
    
    def test_parse_ingredient_with_chinese_unit(self):
        """测试解析中文单位"""
        ing = RecipeParser.parse_ingredient_line("2个鸡蛋")
        self.assertIsNotNone(ing)
        self.assertEqual(ing.amount, 2)
        self.assertIn("鸡蛋", ing.name)
    
    def test_parse_fraction_ingredient(self):
        """测试解析分数配料"""
        ing = RecipeParser.parse_ingredient_line("1/2杯牛奶")
        self.assertIsNotNone(ing)
        self.assertEqual(ing.amount, 0.5)
    
    def test_parse_empty_line(self):
        """测试解析空行"""
        ing = RecipeParser.parse_ingredient_line("")
        self.assertIsNone(ing)


class TestCostCalculator(unittest.TestCase):
    """测试 CostCalculator 类"""
    
    def test_estimate_cost(self):
        """测试估算成本"""
        recipe = get_example_recipe()
        cost = CostCalculator.estimate_cost(recipe)
        
        self.assertIn("total_cost", cost)
        self.assertIn("cost_per_serving", cost)
        self.assertIn("ingredient_costs", cost)
        self.assertGreater(cost["total_cost"], 0)
    
    def test_cost_per_serving(self):
        """测试每份成本"""
        recipe = get_example_recipe()
        cost = CostCalculator.estimate_cost(recipe)
        
        expected_per_serving = cost["total_cost"] / recipe.servings
        self.assertEqual(cost["cost_per_serving"], round(expected_per_serving, 2))


class TestRecipeAnalyzer(unittest.TestCase):
    """测试 RecipeAnalyzer 类"""
    
    def test_analyze(self):
        """测试分析食谱"""
        recipe = get_example_recipe()
        analysis = RecipeAnalyzer.analyze(recipe)
        
        self.assertEqual(analysis["recipe_name"], "番茄炒蛋")
        self.assertEqual(analysis["servings"], 2)
        self.assertIn("total_nutrition", analysis)
        self.assertIn("nutrition_per_serving", analysis)
        self.assertIn("health_score", analysis)
        self.assertIn("time_analysis", analysis)
    
    def test_dietary_compatibility(self):
        """测试饮食兼容性检测"""
        # 无麸质食谱
        recipe = get_example_recipe()
        analysis = RecipeAnalyzer.analyze(recipe)
        self.assertIn("gluten_free", analysis["compatible_diets"])
    
    def test_health_score(self):
        """测试健康评分"""
        recipe = get_example_recipe()
        analysis = RecipeAnalyzer.analyze(recipe)
        health_score = analysis["health_score"]
        
        self.assertIn("score", health_score)
        self.assertIn("grade", health_score)
        self.assertGreaterEqual(health_score["score"], 0)
        self.assertLessEqual(health_score["score"], 100)
    
    def test_time_categorization(self):
        """测试时间分类"""
        analysis = RecipeAnalyzer.analyze(get_example_recipe())
        time_cat = analysis["time_analysis"]["time_category"]
        self.assertIn(time_cat, ["快手菜", "简单快手", "中等时长", "需要耐心", "复杂料理"])


class TestConvenienceFunctions(unittest.TestCase):
    """测试便捷函数"""
    
    def test_scale_recipe_function(self):
        """测试缩放食谱函数"""
        recipe = get_example_recipe()
        scaled = scale_recipe(recipe, 6)
        self.assertEqual(scaled.servings, 6)
    
    def test_convert_unit_function(self):
        """测试单位转换函数"""
        result, success = convert_unit(1, UnitType.CUP, UnitType.MILLILITER)
        self.assertTrue(success)
        self.assertAlmostEqual(result, 236.588, places=1)
    
    def test_get_nutrition_function(self):
        """测试获取营养信息函数"""
        ing = Ingredient("米饭", 100, UnitType.GRAM)
        nutrition = get_nutrition(ing)
        self.assertEqual(nutrition.calories, 130)
    
    def test_get_substitutions_function(self):
        """测试获取替代建议函数"""
        subs = get_substitutions("牛奶")
        self.assertGreater(len(subs), 0)
    
    def test_analyze_recipe_function(self):
        """测试分析食谱函数"""
        recipe = get_example_recipe()
        analysis = analyze_recipe(recipe)
        self.assertIn("recipe_name", analysis)
    
    def test_generate_shopping_list_function(self):
        """测试生成购物清单函数"""
        recipe = get_example_recipe()
        shopping_list = generate_shopping_list([recipe])
        self.assertIn("total_ingredients", shopping_list)
    
    def test_parse_ingredient_function(self):
        """测试解析配料函数"""
        ing = parse_ingredient("50克糖")
        self.assertIsNotNone(ing)
        self.assertEqual(ing.amount, 50)
    
    def test_estimate_recipe_cost_function(self):
        """测试估算成本函数"""
        recipe = get_example_recipe()
        cost = estimate_recipe_cost(recipe)
        self.assertIn("total_cost", cost)
    
    def test_get_common_conversions_function(self):
        """测试获取常用转换函数"""
        conversions = get_common_conversions()
        self.assertIn("体积", conversions)
        self.assertIn("重量", conversions)


class TestRecipeStep(unittest.TestCase):
    """测试 RecipeStep 类"""
    
    def test_create_step(self):
        """测试创建步骤"""
        step = RecipeStep(
            step_number=1,
            instruction="将鸡蛋打散",
            duration_minutes=2,
            temperature=180,
            temperature_unit="celsius",
            tips=["加盐调味"]
        )
        self.assertEqual(step.step_number, 1)
        self.assertEqual(step.duration_minutes, 2)
        self.assertEqual(step.temperature, 180)
        self.assertIn("加盐调味", step.tips)


class TestEnums(unittest.TestCase):
    """测试枚举类"""
    
    def test_dietary_restriction(self):
        """测试饮食限制枚举"""
        self.assertEqual(DietaryRestriction.VEGETARIAN.value, "vegetarian")
        self.assertEqual(DietaryRestriction.VEGAN.value, "vegan")
        self.assertEqual(DietaryRestriction.GLUTEN_FREE.value, "gluten_free")
    
    def test_difficulty_level(self):
        """测试难度枚举"""
        self.assertEqual(DifficultyLevel.EASY.value, "easy")
        self.assertEqual(DifficultyLevel.MEDIUM.value, "medium")
        self.assertEqual(DifficultyLevel.HARD.value, "hard")
    
    def test_meal_type(self):
        """测试餐食类型枚举"""
        self.assertEqual(MealType.BREAKFAST.value, "breakfast")
        self.assertEqual(MealType.LUNCH.value, "lunch")
        self.assertEqual(MealType.DINNER.value, "dinner")
    
    def test_ingredient_category(self):
        """测试配料分类枚举"""
        self.assertEqual(IngredientCategory.PROTEIN.value, "protein")
        self.assertEqual(IngredientCategory.VEGETABLE.value, "vegetable")
        self.assertEqual(IngredientCategory.DAIRY.value, "dairy")


class TestUnitConversionData(unittest.TestCase):
    """测试单位转换数据"""
    
    def test_volume_conversions(self):
        """测试体积转换数据"""
        self.assertEqual(UNIT_CONVERSIONS[UnitType.MILLILITER], 1)
        self.assertEqual(UNIT_CONVERSIONS[UnitType.LITER], 1000)
        self.assertEqual(UNIT_CONVERSIONS[UnitType.CUP], 236.588)
    
    def test_weight_conversions(self):
        """测试重量转换数据"""
        self.assertEqual(UNIT_CONVERSIONS[UnitType.GRAM], 1)
        self.assertEqual(UNIT_CONVERSIONS[UnitType.KILOGRAM], 1000)


class TestIngredientDensity(unittest.TestCase):
    """测试食材密度数据"""
    
    def test_density_exists(self):
        """测试密度数据存在"""
        self.assertIn("水", INGREDIENT_DENSITY)
        self.assertIn("面粉", INGREDIENT_DENSITY)
        self.assertIn("糖", INGREDIENT_DENSITY)


class TestNutritionDatabase(unittest.TestCase):
    """测试营养数据库"""
    
    def test_nutrition_data_exists(self):
        """测试营养数据存在"""
        self.assertIn("鸡蛋", NUTRITION_DATABASE)
        self.assertIn("米饭", NUTRITION_DATABASE)
        self.assertIn("牛肉", NUTRITION_DATABASE)
    
    def test_nutrition_data_structure(self):
        """测试营养数据结构"""
        egg_data = NUTRITION_DATABASE["鸡蛋"]
        self.assertIn("calories", egg_data)
        self.assertIn("protein", egg_data)
        self.assertIn("carbs", egg_data)
        self.assertIn("fat", egg_data)


class TestSubstitutionDatabase(unittest.TestCase):
    """测试替代数据库"""
    
    def test_substitution_data_exists(self):
        """测试替代数据存在"""
        self.assertIn("鸡蛋", INGREDIENT_SUBSTITUTIONS)
        self.assertIn("牛奶", INGREDIENT_SUBSTITUTIONS)
        self.assertIn("黄油", INGREDIENT_SUBSTITUTIONS)
    
    def test_substitution_structure(self):
        """测试替代数据结构"""
        egg_subs = INGREDIENT_SUBSTITUTIONS["鸡蛋"]
        self.assertIsInstance(egg_subs, list)
        self.assertGreater(len(egg_subs), 0)
        self.assertIn("substitute", egg_subs[0])
        self.assertIn("ratio", egg_subs[0])


if __name__ == "__main__":
    unittest.main(verbosity=2)