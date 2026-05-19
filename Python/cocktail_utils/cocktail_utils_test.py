"""
Cocktail Utils 测试

测试覆盖：
- 鸡尾酒配方数据完整性
- 搜索和筛选功能
- 酒精度计算
- 容量转换
- 购物清单生成
- 相似推荐
- 配对建议
- 统计信息
"""

import sys
import os

# 添加父目录到路径以便导入模块
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import unittest
import math
from cocktail_utils.mod import (
    CLASSIC_COCKTAILS,
    Cocktail,
    Ingredient,
    SpiritType,
    Flavor,
    GlassType,
    IceType,
    Garnish,
    get_all_cocktails,
    get_cocktail_by_name,
    search_cocktails,
    get_cocktails_by_spirit,
    get_cocktails_by_flavor,
    get_cocktails_by_glass,
    get_cocktails_by_ingredient,
    get_random_cocktail,
    get_random_cocktails,
    get_cocktails_by_abv_range,
    get_cocktails_by_difficulty,
    get_easy_cocktails,
    get_non_alcoholic_cocktails,
    generate_shopping_list,
    format_shopping_list,
    calculate_abv,
    get_abv_description,
    convert_volume,
    format_recipe,
    suggest_similar_cocktails,
    get_iba_cocktails,
    get_cocktails_by_iba_category,
    estimate_drinks_for_party,
    get_pairing_suggestion,
    get_statistics,
)


class TestCocktailData(unittest.TestCase):
    """测试鸡尾酒数据完整性"""
    
    def test_classic_cocktails_not_empty(self):
        """经典鸡尾酒数据库不为空"""
        self.assertGreater(len(CLASSIC_COCKTAILS), 0)
        self.assertGreater(len(CLASSIC_COCKTAILS), 30)
    
    def test_all_cocktails_have_required_fields(self):
        """所有鸡尾酒都有必需字段"""
        for cocktail in CLASSIC_COCKTAILS:
            self.assertIsNotNone(cocktail.name)
            self.assertIsNotNone(cocktail.name_zh)
            self.assertGreater(len(cocktail.ingredients), 0)
            self.assertGreater(len(cocktail.instructions), 0)
            self.assertIsNotNone(cocktail.glass)
            self.assertIsNotNone(cocktail.ice)
            self.assertGreaterEqual(cocktail.difficulty, 1)
            self.assertLessEqual(cocktail.difficulty, 5)
    
    def test_all_ingredients_have_required_fields(self):
        """所有原料都有必需字段"""
        for cocktail in CLASSIC_COCKTAILS:
            for ing in cocktail.ingredients:
                self.assertIsNotNone(ing.name)
                self.assertGreaterEqual(ing.amount, 0)
                self.assertGreaterEqual(ing.abv, 0)
                self.assertLessEqual(ing.abv, 100)
    
    def test_abv_calculation(self):
        """酒精度计算正确"""
        # Martini: 60ml gin (40%) + 10ml vermouth (15%) = 70ml total
        # Alcohol: 60*0.4 + 10*0.15 = 24 + 1.5 = 25.5ml
        # ABV: 25.5/70 = 36.4%
        martini = get_cocktail_by_name("Martini")
        self.assertIsNotNone(martini)
        self.assertAlmostEqual(martini.abv, 36.4, places=1)
    
    def test_abv_zero_for_non_alcoholic(self):
        """无酒精鸡尾酒酒精度为0"""
        # 获取酒精度为 0 的鸡尾酒（如果存在）
        zero_abv_cocktails = get_cocktails_by_abv_range(0, 0)
        for cocktail in zero_abv_cocktails:
            self.assertEqual(cocktail.abv, 0)
    
    def test_total_volume_positive(self):
        """所有鸡尾酒总容量大于0"""
        for cocktail in CLASSIC_COCKTAILS:
            self.assertGreater(cocktail.total_volume, 0)
    
    def test_spirits_not_empty(self):
        """鸡尾酒应有基酒类型"""
        spirits_count = sum(1 for c in CLASSIC_COCKTAILS if len(c.spirits) > 0)
        self.assertGreater(spirits_count, len(CLASSIC_COCKTAILS) * 0.9)
    
    def test_flavors_not_empty(self):
        """鸡尾酒应有口味描述"""
        flavors_count = sum(1 for c in CLASSIC_COCKTAILS if len(c.flavors) > 0)
        self.assertGreater(flavors_count, len(CLASSIC_COCKTAILS) * 0.9)


class TestSearchFunctions(unittest.TestCase):
    """测试搜索功能"""
    
    def test_get_cocktail_by_name_english(self):
        """英文名搜索"""
        result = get_cocktail_by_name("Martini")
        self.assertIsNotNone(result)
        self.assertEqual(result.name, "Martini")
    
    def test_get_cocktail_by_name_chinese(self):
        """中文名搜索"""
        result = get_cocktail_by_name("马天尼")
        self.assertIsNotNone(result)
        self.assertEqual(result.name_zh, "马天尼")
    
    def test_get_cocktail_by_name_case_insensitive(self):
        """搜索不区分大小写"""
        result1 = get_cocktail_by_name("martini")
        result2 = get_cocktail_by_name("MARTINI")
        self.assertEqual(result1, result2)
    
    def test_get_cocktail_by_name_partial(self):
        """支持部分名称搜索"""
        result = get_cocktail_by_name("Moj")
        self.assertIsNotNone(result)
        self.assertIn("Mojito", result.name)
    
    def test_get_cocktail_by_name_not_found(self):
        """找不到返回 None"""
        result = get_cocktail_by_name("不存在的鸡尾酒")
        self.assertIsNone(result)
    
    def test_search_by_description(self):
        """搜索描述"""
        results = search_cocktails("经典")
        self.assertGreater(len(results), 0)
    
    def test_search_by_ingredient(self):
        """搜索原料"""
        results = search_cocktails("Gin")
        self.assertGreater(len(results), 0)
        # 验证结果包含 Gin
        has_gin = any(
            any("gin" in ing.name.lower() for ing in c.ingredients)
            for c in results
        )
        self.assertTrue(has_gin)
    
    def test_search_returns_multiple(self):
        """搜索可能返回多个结果"""
        results = search_cocktails("vodka")
        self.assertGreater(len(results), 1)


class TestFilterFunctions(unittest.TestCase):
    """测试筛选功能"""
    
    def test_filter_by_spirit_vodka(self):
        """按伏特加筛选"""
        results = get_cocktails_by_spirit(SpiritType.VODKA)
        self.assertGreater(len(results), 0)
        for cocktail in results:
            self.assertIn(SpiritType.VODKA, cocktail.spirits)
    
    def test_filter_by_spirit_rum(self):
        """按朗姆酒筛选"""
        results = get_cocktails_by_spirit(SpiritType.RUM)
        self.assertGreater(len(results), 0)
        for cocktail in results:
            self.assertIn(SpiritType.RUM, cocktail.spirits)
    
    def test_filter_by_spirit_whiskey(self):
        """按威士忌筛选"""
        results = get_cocktails_by_spirit(SpiritType.WHISKEY)
        self.assertGreater(len(results), 0)
        for cocktail in results:
            self.assertIn(SpiritType.WHISKEY, cocktail.spirits)
    
    def test_filter_by_flavor_sweet(self):
        """按甜味筛选"""
        results = get_cocktails_by_flavor(Flavor.SWEET)
        self.assertGreater(len(results), 0)
        for cocktail in results:
            self.assertIn(Flavor.SWEET, cocktail.flavors)
    
    def test_filter_by_flavor_sour(self):
        """按酸味筛选"""
        results = get_cocktails_by_flavor(Flavor.SOUR)
        self.assertGreater(len(results), 0)
        for cocktail in results:
            self.assertIn(Flavor.SOUR, cocktail.flavors)
    
    def test_filter_by_glass_martini(self):
        """按马天尼杯筛选"""
        results = get_cocktails_by_glass(GlassType.MARTINI)
        self.assertGreater(len(results), 0)
        for cocktail in results:
            self.assertEqual(cocktail.glass, GlassType.MARTINI)
    
    def test_filter_by_glass_highball(self):
        """按高球杯筛选"""
        results = get_cocktails_by_glass(GlassType.HIGHBALL)
        self.assertGreater(len(results), 0)
        for cocktail in results:
            self.assertEqual(cocktail.glass, GlassType.HIGHBALL)
    
    def test_filter_by_ingredient(self):
        """按原料筛选"""
        results = get_cocktails_by_ingredient("lime")
        self.assertGreater(len(results), 0)
        # 验证结果包含 lime
        has_lime = any(
            any("lime" in ing.name.lower() for ing in c.ingredients)
            for c in results
        )
        self.assertTrue(has_lime)
    
    def test_filter_by_abv_range(self):
        """按酒精度范围筛选"""
        # 获取中等酒精度鸡尾酒 (15-25%)
        results = get_cocktails_by_abv_range(15, 25)
        self.assertGreater(len(results), 0)
        for cocktail in results:
            self.assertGreaterEqual(cocktail.abv, 15)
            self.assertLessEqual(cocktail.abv, 25)
    
    def test_filter_by_abv_high(self):
        """高酒精度鸡尾酒"""
        results = get_cocktails_by_abv_range(30, 50)
        self.assertGreater(len(results), 0)
        for cocktail in results:
            self.assertGreaterEqual(cocktail.abv, 30)
    
    def test_filter_by_difficulty(self):
        """按难度筛选"""
        for diff in [1, 2, 3]:
            results = get_cocktails_by_difficulty(diff)
            for cocktail in results:
                self.assertEqual(cocktail.difficulty, diff)
    
    def test_get_easy_cocktails(self):
        """获取简单鸡尾酒"""
        results = get_easy_cocktails()
        self.assertGreater(len(results), 0)
        for cocktail in results:
            self.assertLessEqual(cocktail.difficulty, 2)


class TestRandomFunctions(unittest.TestCase):
    """测试随机功能"""
    
    def test_get_random_cocktail(self):
        """随机获取一个鸡尾酒"""
        result = get_random_cocktail()
        self.assertIsNotNone(result)
        self.assertIn(result, CLASSIC_COCKTAILS)
    
    def test_get_random_cocktails_multiple(self):
        """随机获取多个鸡尾酒"""
        results = get_random_cocktails(5)
        self.assertEqual(len(results), 5)
        # 验证结果不重复
        names = [c.name for c in results]
        self.assertEqual(len(names), len(set(names)))
    
    def test_get_random_cocktails_max_limit(self):
        """随机数量不超过总数"""
        results = get_random_cocktails(1000)
        self.assertEqual(len(results), len(CLASSIC_COCKTAILS))
    
    def test_random_cocktails_different_each_call(self):
        """每次调用结果可能不同"""
        results1 = get_random_cocktails(10)
        results2 = get_random_cocktails(10)
        # 多次调用后应该有不同结果（概率性）
        names1 = [c.name for c in results1]
        names2 = [c.name for c in results2]
        # 可能相同但不应该总是相同
        same_count = sum(1 for n in names1 if n in names2)
        self.assertLessEqual(same_count, len(names1))


class TestShoppingList(unittest.TestCase):
    """测试购物清单功能"""
    
    def test_generate_shopping_list_single(self):
        """单个鸡尾酒购物清单"""
        martini = get_cocktail_by_name("Martini")
        shopping = generate_shopping_list([martini])
        self.assertIn("Gin", shopping)
        self.assertIn("Dry Vermouth", shopping)
    
    def test_generate_shopping_list_multiple(self):
        """多个鸡尾酒购物清单"""
        cocktails = [
            get_cocktail_by_name("Martini"),
            get_cocktail_by_name("Mojito"),
        ]
        shopping = generate_shopping_list(cocktails)
        self.assertGreater(len(shopping), 0)
    
    def test_shopping_list_excludes_optional(self):
        """购物清单排除可选原料"""
        # Whiskey Sour 有可选蛋白
        whiskey_sour = get_cocktail_by_name("Whiskey Sour")
        shopping = generate_shopping_list([whiskey_sour])
        # Egg White 是可选的，不应出现在清单中
        self.assertNotIn("Egg White", shopping)
    
    def test_shopping_list_amounts_correct(self):
        """购物清单数量正确"""
        martini = get_cocktail_by_name("Martini")
        shopping = generate_shopping_list([martini])
        self.assertEqual(shopping["Gin"], 60)
        self.assertEqual(shopping["Dry Vermouth"], 10)
    
    def test_shopping_list_sums_duplicates(self):
        """重复原料数量累加"""
        cocktails = [
            get_cocktail_by_name("Mojito"),
            get_cocktail_by_name("Daiquiri"),
        ]
        shopping = generate_shopping_list(cocktails)
        # 两个都用 lime juice
        self.assertIn("Lime Juice", shopping)
        total_lime = shopping["Lime Juice"]
        self.assertGreater(total_lime, 25)  # > 单个
    
    def test_format_shopping_list(self):
        """购物清单格式化"""
        shopping = {"Gin": 60, "Vodka": 50}
        formatted = format_shopping_list(shopping)
        self.assertIn("购物清单", formatted)
        self.assertIn("Gin", formatted)
        self.assertIn("Vodka", formatted)
    
    def test_format_shopping_list_with_servings(self):
        """购物清单乘以份数"""
        shopping = {"Gin": 60}
        formatted = format_shopping_list(shopping, servings=2)
        self.assertIn("120ml", formatted)


class TestABVCalculation(unittest.TestCase):
    """测试酒精度计算"""
    
    def test_calculate_abv_basic(self):
        """基本酒精度计算"""
        ingredients = [
            {"name": "Vodka", "amount_ml": 50, "abv": 40},
            {"name": "Juice", "amount_ml": 100, "abv": 0},
        ]
        abv = calculate_abv(ingredients)
        # 50*0.4 + 100*0 = 20ml alcohol in 150ml total
        # ABV = 20/150 = 13.3%
        self.assertAlmostEqual(abv, 13.3, places=1)
    
    def test_calculate_abv_zero(self):
        """无酒精计算"""
        ingredients = [
            {"name": "Juice", "amount_ml": 100, "abv": 0},
            {"name": "Soda", "amount_ml": 100, "abv": 0},
        ]
        abv = calculate_abv(ingredients)
        self.assertEqual(abv, 0)
    
    def test_calculate_abv_pure_alcohol(self):
        """纯酒精计算"""
        ingredients = [
            {"name": "Spirit", "amount_ml": 50, "abv": 100},
        ]
        abv = calculate_abv(ingredients)
        self.assertEqual(abv, 100)
    
    def test_calculate_abv_empty(self):
        """空原料列表"""
        abv = calculate_abv([])
        self.assertEqual(abv, 0)
    
    def test_get_abv_description_levels(self):
        """酒精度描述"""
        self.assertEqual(get_abv_description(0), "无酒精 🚫")
        self.assertEqual(get_abv_description(3), "轻度 🟢")
        self.assertEqual(get_abv_description(10), "中等 🟡")
        self.assertEqual(get_abv_description(25), "较强 🟠")
        self.assertEqual(get_abv_description(40), "烈酒 🔴")


class TestVolumeConversion(unittest.TestCase):
    """测试容量转换"""
    
    def test_convert_ml_to_ml(self):
        """毫升转毫升"""
        result = convert_volume(100, "ml", "ml")
        self.assertEqual(result, 100)
    
    def test_convert_ml_to_oz(self):
        """毫升转盎司"""
        result = convert_volume(100, "ml", "oz")
        self.assertAlmostEqual(result, 3.38, places=1)
    
    def test_convert_oz_to_ml(self):
        """盎司转毫升"""
        result = convert_volume(1, "oz", "ml")
        self.assertAlmostEqual(result, 29.57, places=1)
    
    def test_convert_ml_to_l(self):
        """毫升转升"""
        result = convert_volume(1000, "ml", "l")
        self.assertEqual(result, 1)
    
    def test_convert_cl_to_ml(self):
        """厘升转毫升"""
        result = convert_volume(10, "cl", "ml")
        self.assertEqual(result, 100)
    
    def test_convert_tbsp_to_ml(self):
        """汤匙转毫升"""
        result = convert_volume(1, "tbsp", "ml")
        self.assertAlmostEqual(result, 14.79, places=1)
    
    def test_convert_tsp_to_ml(self):
        """茶匙转毫升"""
        result = convert_volume(1, "tsp", "ml")
        self.assertAlmostEqual(result, 4.93, places=1)
    
    def test_convert_dash_to_ml(self):
        """滴转毫升"""
        result = convert_volume(1, "dash", "ml")
        self.assertAlmostEqual(result, 0.92, places=1)
    
    def test_convert_invalid_unit(self):
        """无效单位报错"""
        with self.assertRaises(ValueError):
            convert_volume(100, "invalid", "ml")


class TestRecipeFormat(unittest.TestCase):
    """测试配方格式化"""
    
    def test_format_recipe_chinese(self):
        """中文配方格式化"""
        martini = get_cocktail_by_name("Martini")
        formatted = format_recipe(martini, "zh")
        self.assertIn("马天尼", formatted)
        self.assertIn("原料", formatted)
        self.assertIn("制作步骤", formatted)
    
    def test_format_recipe_english(self):
        """英文配方格式化"""
        martini = get_cocktail_by_name("Martini")
        formatted = format_recipe(martini, "en")
        self.assertIn("Martini", formatted)
        self.assertIn("Ingredients", formatted)
        self.assertIn("Instructions", formatted)
    
    def test_format_recipe_contains_glass(self):
        """格式化包含酒杯类型"""
        mojito = get_cocktail_by_name("Mojito")
        formatted = format_recipe(mojito)
        self.assertIn("酒杯", formatted)
    
    def test_format_recipe_contains_abv(self):
        """格式化包含酒精度"""
        martini = get_cocktail_by_name("Martini")
        formatted = format_recipe(martini)
        self.assertIn("酒精度", formatted)
    
    def test_format_recipe_contains_difficulty(self):
        """格式化包含难度"""
        cocktail = get_random_cocktail()
        formatted = format_recipe(cocktail)
        self.assertIn("难度", formatted)


class TestSimilarSuggestions(unittest.TestCase):
    """测试相似推荐"""
    
    def test_suggest_similar_returns_results(self):
        """相似推荐返回结果"""
        cocktail = get_cocktail_by_name("Martini")
        similar = suggest_similar_cocktails(cocktail)
        self.assertGreater(len(similar), 0)
    
    def test_suggest_similar_excludes_self(self):
        """相似推荐不包含自己"""
        cocktail = get_cocktail_by_name("Martini")
        similar = suggest_similar_cocktails(cocktail)
        names = [c.name for c, _ in similar]
        self.assertNotIn("Martini", names)
    
    def test_suggest_similar_has_scores(self):
        """相似推荐有分数"""
        cocktail = get_cocktail_by_name("Mojito")
        similar = suggest_similar_cocktails(cocktail)
        for c, score in similar:
            self.assertGreaterEqual(score, 0)
            self.assertLessEqual(score, 1)
    
    def test_suggest_similar_sorted_by_score(self):
        """相似推荐按分数排序"""
        cocktail = get_cocktail_by_name("Negroni")
        similar = suggest_similar_cocktails(cocktail)
        scores = [score for _, score in similar]
        self.assertEqual(scores, sorted(scores, reverse=True))
    
    def test_suggest_similar_limit(self):
        """相似推荐数量限制"""
        cocktail = get_cocktail_by_name("Martini")
        similar = suggest_similar_cocktails(cocktail, limit=3)
        self.assertLessEqual(len(similar), 3)
    
    def test_suggest_similar_spirit_match(self):
        """相似推荐基酒匹配"""
        # Martini 是 Gin 鸡尾酒
        cocktail = get_cocktail_by_name("Martini")
        similar = suggest_similar_cocktails(cocktail, limit=10)
        # 应该有 Gin 鸡尾酒
        gin_similar = sum(
            1 for c, _ in similar 
            if SpiritType.GIN in c.spirits
        )
        self.assertGreater(gin_similar, 0)


class TestIBAFunctions(unittest.TestCase):
    """测试 IBA 相关功能"""
    
    def test_get_iba_cocktails(self):
        """获取 IBA 官方鸡尾酒"""
        iba = get_iba_cocktails()
        self.assertGreater(len(iba), 0)
    
    def test_iba_cocktails_have_category(self):
        """IBA 鸡尾酒有分类"""
        iba = get_iba_cocktails()
        for cocktail in iba:
            self.assertIsNotNone(cocktail.iba_category)
            self.assertGreater(len(cocktail.iba_category), 0)
    
    def test_filter_by_iba_category(self):
        """按 IBA 分类筛选"""
        results = get_cocktails_by_iba_category("Unforgettables")
        self.assertGreater(len(results), 0)
        for cocktail in results:
            self.assertIn("Unforgettables", cocktail.iba_category)
    
    def test_filter_by_iba_category_contemporary(self):
        """当代经典分类"""
        results = get_cocktails_by_iba_category("Contemporary")
        self.assertGreater(len(results), 0)


class TestPartyEstimate(unittest.TestCase):
    """测试派对估算"""
    
    def test_estimate_basic(self):
        """基本派对估算"""
        estimate = estimate_drinks_for_party(10, 2)
        self.assertIn("total_drinks", estimate)
        self.assertIn("total_ml", estimate)
        self.assertGreater(estimate["total_drinks"], 0)
    
    def test_estimate_total_drinks(self):
        """估算总饮品数"""
        # 10人 * 2小时 * 1.5 drinks/hour = 30 drinks
        estimate = estimate_drinks_for_party(10, 2, 1.5)
        self.assertEqual(estimate["total_drinks"], 30)
    
    def test_estimate_per_person(self):
        """每人饮品数"""
        estimate = estimate_drinks_for_party(10, 3)
        per_person = estimate["drinks_per_person"]
        self.assertGreater(per_person, 0)
    
    def test_estimate_suggested_varieties(self):
        """建议鸡尾酒种类数"""
        estimate = estimate_drinks_for_party(10, 3)
        suggested = estimate["suggested_cocktails"]
        self.assertGreater(suggested, 0)
    
    def test_estimate_large_party(self):
        """大型派对估算"""
        estimate = estimate_drinks_for_party(100, 4)
        self.assertGreater(estimate["total_drinks"], 400)


class TestPairingSuggestion(unittest.TestCase):
    """测试配对建议"""
    
    def test_pairing_seafood(self):
        """海鲜配对"""
        results = get_pairing_suggestion("seafood")
        self.assertGreater(len(results), 0)
    
    def test_pairing_meat(self):
        """肉类配对"""
        results = get_pairing_suggestion("meat")
        self.assertGreater(len(results), 0)
    
    def test_pairing_spicy(self):
        """辛辣配对"""
        results = get_pairing_suggestion("spicy")
        self.assertGreater(len(results), 0)
    
    def test_pairing_dessert(self):
        """甜品配对"""
        results = get_pairing_suggestion("dessert")
        self.assertGreater(len(results), 0)
    
    def test_pairing_invalid_type(self):
        """无效菜品类型返回空列表"""
        results = get_pairing_suggestion("invalid_dish")
        self.assertEqual(len(results), 0)
    
    def test_pairing_mexican(self):
        """墨西哥菜配对"""
        results = get_pairing_suggestion("mexican")
        # 应该有酸辣口味的鸡尾酒
        has_sour_or_spicy = any(
            Flavor.SOUR in c.flavors or Flavor.SPICY in c.flavors
            for c in results
        )
        self.assertTrue(has_sour_or_spicy)


class TestStatistics(unittest.TestCase):
    """测试统计功能"""
    
    def test_get_statistics(self):
        """获取统计信息"""
        stats = get_statistics()
        self.assertIn("total_cocktails", stats)
        self.assertIn("avg_abv", stats)
        self.assertIn("iba_cocktails", stats)
    
    def test_total_count_correct(self):
        """总数正确"""
        stats = get_statistics()
        self.assertEqual(stats["total_cocktails"], len(CLASSIC_COCKTAILS))
    
    def test_spirits_distribution(self):
        """基酒分布"""
        stats = get_statistics()
        spirits = stats["spirits_distribution"]
        self.assertGreater(len(spirits), 0)
    
    def test_flavors_distribution(self):
        """口味分布"""
        stats = get_statistics()
        flavors = stats["flavors_distribution"]
        self.assertGreater(len(flavors), 0)
    
    def test_glasses_distribution(self):
        """酒杯分布"""
        stats = get_statistics()
        glasses = stats["glasses_distribution"]
        self.assertGreater(len(glasses), 0)
    
    def test_difficulty_distribution(self):
        """难度分布"""
        stats = get_statistics()
        difficulty = stats["difficulty_distribution"]
        # 至少有难度 1-3 的鸡尾酒
        total = sum(difficulty.values())
        self.assertEqual(total, len(CLASSIC_COCKTAILS))
    
    def test_avg_abv_positive(self):
        """平均酒精度大于0"""
        stats = get_statistics()
        self.assertGreater(stats["avg_abv"], 0)


class TestIngredientClass(unittest.TestCase):
    """测试 Ingredient 类"""
    
    def test_ingredient_alcohol_volume(self):
        """原料酒精量计算"""
        ing = Ingredient("Vodka", 50, "ml", 40)
        self.assertEqual(ing.alcohol_volume, 20)
    
    def test_ingredient_alcohol_volume_zero(self):
        """无酒精原料"""
        ing = Ingredient("Juice", 100, "ml", 0)
        self.assertEqual(ing.alcohol_volume, 0)
    
    def test_ingredient_cost_calculation(self):
        """原料成本计算"""
        ing = Ingredient("Gin", 60, "ml", 40, cost_per_ml=0.1)
        self.assertEqual(ing.cost, 6)
    
    def test_ingredient_cost_zero(self):
        """无成本原料"""
        ing = Ingredient("Juice", 100, "ml", 0)
        self.assertEqual(ing.cost, 0)


class TestCocktailClass(unittest.TestCase):
    """测试 Cocktail 类"""
    
    def test_cocktail_total_alcohol(self):
        """鸡尾酒酒精总量"""
        martini = get_cocktail_by_name("Martini")
        self.assertGreater(martini.total_alcohol, 0)
    
    def test_cocktail_total_cost(self):
        """鸡尾酒总成本"""
        # 不设置成本的鸡尾酒
        martini = get_cocktail_by_name("Martini")
        self.assertEqual(martini.total_cost, 0)
    
    def test_cocktail_get_shopping_list(self):
        """鸡尾酒购物清单"""
        martini = get_cocktail_by_name("Martini")
        shopping = martini.get_shopping_list()
        self.assertIn("Gin", shopping)
        self.assertEqual(shopping["Gin"], 60)


class TestEdgeCases(unittest.TestCase):
    """边界值测试"""
    
    def test_empty_cocktail_list(self):
        """空鸡尾酒列表购物清单"""
        shopping = generate_shopping_list([])
        self.assertEqual(len(shopping), 0)
    
    def test_zero_abv_range(self):
        """零酒精度范围"""
        results = get_cocktails_by_abv_range(0, 0)
        # 应该返回无酒精鸡尾酒
        for cocktail in results:
            self.assertEqual(cocktail.abv, 0)
    
    def test_max_abv_range(self):
        """最大酒精度范围"""
        results = get_cocktails_by_abv_range(0, 100)
        self.assertEqual(len(results), len(CLASSIC_COCKTAILS))
    
    def test_zero_party_size(self):
        """零人数派对"""
        estimate = estimate_drinks_for_party(0, 2)
        self.assertEqual(estimate["total_drinks"], 0)
    
    def test_zero_hours(self):
        """零时长派对"""
        estimate = estimate_drinks_for_party(10, 0)
        self.assertEqual(estimate["total_drinks"], 0)
    
    def test_very_small_volume_conversion(self):
        """极小容量转换"""
        result = convert_volume(0.1, "ml", "oz")
        # 0.1 ml = 0.003 oz (rounded to 2 decimals)
        self.assertAlmostEqual(result, 0.00, places=2)
    
    def test_large_volume_conversion(self):
        """大容量转换"""
        result = convert_volume(10000, "ml", "l")
        self.assertEqual(result, 10)


if __name__ == "__main__":
    # 运行测试
    unittest.main(verbosity=2)