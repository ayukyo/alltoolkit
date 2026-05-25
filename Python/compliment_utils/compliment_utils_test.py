"""
Compliment Utils 测试文件

测试称赞生成工具的各项功能
"""

import unittest
from mod import (
    ComplimentUtils,
    ComplimentCategory,
    ComplimentStrength,
    Language,
    get_compliment,
    get_personalized_compliment,
    get_daily_compliment,
    get_motivational_compliment,
    get_batch_compliments,
    random_compliment,
)


class TestComplimentEnums(unittest.TestCase):
    """测试枚举类型"""

    def test_category_values(self):
        """测试类别枚举值"""
        self.assertEqual(ComplimentCategory.WORK.value, "工作")
        self.assertEqual(ComplimentCategory.APPEARANCE.value, "外貌")
        self.assertEqual(ComplimentCategory.GENERAL.value, "通用")

    def test_strength_values(self):
        """测试强度枚举值"""
        self.assertEqual(ComplimentStrength.LIGHT.value, "轻度")
        self.assertEqual(ComplimentStrength.MEDIUM.value, "中度")
        self.assertEqual(ComplimentStrength.STRONG.value, "强力")

    def test_language_values(self):
        """测试语言枚举值"""
        self.assertEqual(Language.CHINESE.value, "zh")
        self.assertEqual(Language.ENGLISH.value, "en")


class TestComplimentUtils(unittest.TestCase):
    """测试 ComplimentUtils 类"""

    def test_get_compliment_basic(self):
        """测试基本称赞获取"""
        result = ComplimentUtils.get_compliment()
        self.assertIsInstance(result, str)
        self.assertTrue(len(result) > 0)

    def test_get_compliment_with_category(self):
        """测试指定类别称赞"""
        result = ComplimentUtils.get_compliment(category=ComplimentCategory.WORK)
        self.assertIsInstance(result, str)
        self.assertTrue(len(result) > 0)

    def test_get_compliment_with_strength(self):
        """测试指定强度称赞"""
        for strength in ComplimentStrength:
            result = ComplimentUtils.get_compliment(strength=strength)
            self.assertIsInstance(result, str)
            self.assertTrue(len(result) > 0)

    def test_get_compliment_chinese(self):
        """测试中文称赞"""
        result = ComplimentUtils.get_compliment(language=Language.CHINESE)
        self.assertIsInstance(result, str)
        # 验证是中文字符
        self.assertTrue(any('\u4e00' <= c <= '\u9fff' for c in result))

    def test_get_compliment_english(self):
        """测试英文称赞"""
        result = ComplimentUtils.get_compliment(language=Language.ENGLISH)
        self.assertIsInstance(result, str)
        # 验证主要是英文字符
        self.assertTrue(any(c.isalpha() and ord(c) < 128 for c in result))

    def test_get_compliment_with_prefix(self):
        """测试带前缀称赞"""
        result = ComplimentUtils.get_compliment(include_prefix=True)
        self.assertIsInstance(result, str)
        self.assertTrue(len(result) > 0)

    def test_get_compliment_with_suffix(self):
        """测试带后缀称赞"""
        result = ComplimentUtils.get_compliment(include_suffix=True)
        self.assertIsInstance(result, str)
        self.assertTrue(len(result) > 0)

    def test_get_compliment_with_prefix_suffix(self):
        """测试同时带前缀和后缀"""
        result = ComplimentUtils.get_compliment(include_prefix=True, include_suffix=True)
        self.assertIsInstance(result, str)
        self.assertTrue(len(result) > 0)


class TestPersonalizedCompliment(unittest.TestCase):
    """测试个性化称赞"""

    def test_personalized_chinese(self):
        """测试中文个性化称赞"""
        result = ComplimentUtils.get_personalized_compliment(name="小明")
        self.assertIsInstance(result, str)
        self.assertIn("小明", result)

    def test_personalized_english(self):
        """测试英文个性化称赞"""
        result = ComplimentUtils.get_personalized_compliment(name="John", language=Language.ENGLISH)
        self.assertIsInstance(result, str)
        self.assertIn("John", result)

    def test_personalized_with_category(self):
        """测试指定类别的个性化称赞"""
        result = ComplimentUtils.get_personalized_compliment(
            name="小明",
            category=ComplimentCategory.WORK,
        )
        self.assertIsInstance(result, str)
        self.assertIn("小明", result)


class TestBatchCompliments(unittest.TestCase):
    """测试批量称赞"""

    def test_batch_compliments_count(self):
        """测试批量称赞数量"""
        results = ComplimentUtils.get_batch_compliments(count=5)
        self.assertEqual(len(results), 5)
        for result in results:
            self.assertIsInstance(result, str)

    def test_batch_compliments_unique(self):
        """测试批量称赞唯一性"""
        results = ComplimentUtils.get_batch_compliments(count=10, unique=True)
        self.assertTrue(len(set(results)) == len(results))

    def test_batch_compliments_with_category(self):
        """测试指定类别的批量称赞"""
        results = ComplimentUtils.get_batch_compliments(
            count=3,
            category=ComplimentCategory.KINDNESS,
        )
        self.assertEqual(len(results), 3)


class TestContextCompliment(unittest.TestCase):
    """测试上下文称赞"""

    def test_context_work(self):
        """测试工作相关上下文"""
        result = ComplimentUtils.get_compliment_for_context("完成了项目")
        self.assertIsInstance(result, str)

    def test_context_kindness(self):
        """测试善良相关上下文"""
        result = ComplimentUtils.get_compliment_for_context("帮助了同事")
        self.assertIsInstance(result, str)

    def test_context_english(self):
        """测试英文上下文"""
        result = ComplimentUtils.get_compliment_for_context("finished the work", language=Language.ENGLISH)
        self.assertIsInstance(result, str)


class TestUtilityMethods(unittest.TestCase):
    """测试工具方法"""

    def test_get_categories(self):
        """测试获取类别列表"""
        categories_cn = ComplimentUtils.get_categories(Language.CHINESE)
        categories_en = ComplimentUtils.get_categories(Language.ENGLISH)
        
        self.assertTrue("工作" in categories_cn)
        self.assertTrue("WORK" in categories_en)

    def test_get_strengths(self):
        """测试获取强度列表"""
        strengths_cn = ComplimentUtils.get_strengths(Language.CHINESE)
        strengths_en = ComplimentUtils.get_strengths(Language.ENGLISH)
        
        self.assertTrue("轻度" in strengths_cn)
        self.assertTrue("LIGHT" in strengths_en)

    def test_get_compliment_count(self):
        """测试获取称赞数量"""
        total_count = ComplimentUtils.get_compliment_count()
        self.assertTrue(total_count > 100)
        
        work_count = ComplimentUtils.get_compliment_count(category=ComplimentCategory.WORK)
        self.assertTrue(work_count > 0)


class TestDailyCompliment(unittest.TestCase):
    """测试每日称赞"""

    def test_daily_compliment_chinese(self):
        """测试中文每日称赞"""
        result = ComplimentUtils.get_daily_compliment(Language.CHINESE)
        self.assertIsInstance(result, str)
        self.assertIn("每日称赞", result)

    def test_daily_compliment_english(self):
        """测试英文每日称赞"""
        result = ComplimentUtils.get_daily_compliment(Language.ENGLISH)
        self.assertIsInstance(result, str)
        self.assertIn("Daily Compliment", result)


class TestMotivationalCompliment(unittest.TestCase):
    """测试激励性称赞"""

    def test_motivational_chinese(self):
        """测试中文激励性称赞"""
        result = ComplimentUtils.get_motivational_compliment(Language.CHINESE)
        self.assertIsInstance(result, str)
        self.assertTrue(len(result) > 0)

    def test_motivational_english(self):
        """测试英文激励性称赞"""
        result = ComplimentUtils.get_motivational_compliment(Language.ENGLISH)
        self.assertIsInstance(result, str)
        self.assertTrue(len(result) > 0)


class TestConvenienceFunctions(unittest.TestCase):
    """测试便捷函数"""

    def test_get_compliment_function(self):
        """测试便捷获取称赞函数"""
        result = get_compliment()
        self.assertIsInstance(result, str)

    def test_get_compliment_with_params(self):
        """测试带参数的便捷函数"""
        result = get_compliment(category="工作", strength="中度", language="zh")
        self.assertIsInstance(result, str)

        result = get_compliment(category="WORK", strength="MEDIUM", language="en")
        self.assertIsInstance(result, str)

    def test_get_personalized_compliment_function(self):
        """测试便捷个性化称赞函数"""
        result = get_personalized_compliment(name="小明")
        self.assertIsInstance(result, str)
        self.assertIn("小明", result)

    def test_get_daily_compliment_function(self):
        """测试便捷每日称赞函数"""
        result = get_daily_compliment()
        self.assertIsInstance(result, str)

    def test_get_motivational_compliment_function(self):
        """测试便捷激励性称赞函数"""
        result = get_motivational_compliment()
        self.assertIsInstance(result, str)

    def test_get_batch_compliments_function(self):
        """测试便捷批量称赞函数"""
        results = get_batch_compliments(count=3)
        self.assertEqual(len(results), 3)

    def test_random_compliment_function(self):
        """测试随机称赞函数"""
        result = random_compliment()
        self.assertIsInstance(result, str)


class TestAllCategories(unittest.TestCase):
    """测试所有类别"""

    def test_all_categories_have_compliments(self):
        """测试所有类别都有称赞"""
        for category in ComplimentCategory:
            for strength in ComplimentStrength:
                for language in Language:
                    result = ComplimentUtils.get_compliment(
                        category=category,
                        strength=strength,
                        language=language,
                    )
                    self.assertTrue(len(result) > 0, 
                        f"Empty compliment for {category.value}/{strength.value}/{language.value}")


class TestEdgeCases(unittest.TestCase):
    """测试边缘情况"""

    def test_empty_name(self):
        """测试空名字"""
        result = ComplimentUtils.get_personalized_compliment(name="")
        self.assertIsInstance(result, str)

    def test_large_batch_request(self):
        """测试大量批量请求"""
        results = ComplimentUtils.get_batch_compliments(count=1000)
        # 应该返回有限数量的称赞
        self.assertTrue(len(results) <= 200)

    def test_unknown_context(self):
        """测试未知上下文"""
        result = ComplimentUtils.get_compliment_for_context("这是未知的上下文内容")
        self.assertIsInstance(result, str)  # 应返回通用称赞


if __name__ == "__main__":
    unittest.main(verbosity=2)