"""
Quote Utilities - 测试文件

测试名言警句工具的所有功能。
"""

import unittest
from datetime import date, timedelta
import sys
import os
import json

# 添加父目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from quote_utils.mod import (
    QuoteManager,
    Quote,
    QuoteCategory,
    QuoteStyle,
    QuoteFormatter,
    QuoteUtils,
    get_quote,
    get_daily_quote,
    search_quotes,
    format_quote,
    list_categories,
)


class TestQuote(unittest.TestCase):
    """测试 Quote 类"""
    
    def test_create_quote(self):
        """测试创建名言"""
        quote = Quote(
            text="测试名言",
            author="测试作者",
            category=QuoteCategory.WISDOM,
            language="zh",
        )
        
        self.assertEqual(quote.text, "测试名言")
        self.assertEqual(quote.author, "测试作者")
        self.assertEqual(quote.category, QuoteCategory.WISDOM)
        self.assertEqual(quote.language, "zh")
        self.assertEqual(quote.rating, 5)
        self.assertFalse(quote.is_favorite)
    
    def test_quote_id(self):
        """测试名言ID生成"""
        quote1 = Quote(text="相同内容", author="相同作者")
        quote2 = Quote(text="相同内容", author="相同作者")
        quote3 = Quote(text="不同内容", author="相同作者")
        
        self.assertEqual(quote1.get_id(), quote2.get_id())
        self.assertNotEqual(quote1.get_id(), quote3.get_id())
    
    def test_to_dict(self):
        """测试转换为字典"""
        quote = Quote(
            text="测试名言",
            author="测试作者",
            category=QuoteCategory.SUCCESS,
            language="zh",
            source="测试出处",
            tags=["测试", "示例"],
            rating=4,
            is_favorite=True,
        )
        
        data = quote.to_dict()
        
        self.assertEqual(data['text'], "测试名言")
        self.assertEqual(data['author'], "测试作者")
        self.assertEqual(data['category'], "success")
        self.assertEqual(data['language'], "zh")
        self.assertEqual(data['source'], "测试出处")
        self.assertEqual(data['tags'], ["测试", "示例"])
        self.assertEqual(data['rating'], 4)
        self.assertTrue(data['is_favorite'])
    
    def test_from_dict(self):
        """测试从字典创建"""
        data = {
            'text': '测试名言',
            'author': '测试作者',
            'category': 'motivation',
            'language': 'zh',
            'source': '测试出处',
            'tags': ['测试'],
            'rating': 3,
            'created_at': '2024-01-15',
            'is_favorite': True,
        }
        
        quote = Quote.from_dict(data)
        
        self.assertEqual(quote.text, "测试名言")
        self.assertEqual(quote.author, "测试作者")
        self.assertEqual(quote.category, QuoteCategory.MOTIVATION)
        self.assertEqual(quote.created_at, date(2024, 1, 15))
        self.assertTrue(quote.is_favorite)
    
    def test_format_simple(self):
        """测试简洁格式"""
        quote = Quote(text="测试名言", author="测试作者")
        formatted = quote.format(QuoteStyle.SIMPLE)
        
        self.assertIn("测试名言", formatted)
        self.assertIn("测试作者", formatted)
        self.assertIn('"', formatted)
    
    def test_format_card(self):
        """测试卡片格式"""
        quote = Quote(text="短名言", author="作者")
        formatted = quote.format(QuoteStyle.CARD)
        
        self.assertIn("短名言", formatted)
        self.assertIn("作者", formatted)
        self.assertIn("┌", formatted)
        self.assertIn("└", formatted)
    
    def test_format_banner(self):
        """测试横幅格式"""
        quote = Quote(text="测试名言", author="测试作者")
        formatted = quote.format(QuoteStyle.BANNER)
        
        self.assertIn("=", formatted)
        self.assertIn("测试名言", formatted)
        self.assertIn("测试作者", formatted)
    
    def test_format_minimal(self):
        """测试极简格式"""
        quote = Quote(text="测试名言", author="测试作者")
        formatted = quote.format(QuoteStyle.MINIMAL)
        
        self.assertEqual(formatted, "测试名言\n—测试作者")
    
    def test_format_decorated(self):
        """测试装饰格式"""
        quote = Quote(text="测试名言", author="测试作者")
        formatted = quote.format(QuoteStyle.DECORATED)
        
        self.assertIn("✨", formatted)
        self.assertIn("📖", formatted)


class TestQuoteManager(unittest.TestCase):
    """测试 QuoteManager 类"""
    
    def setUp(self):
        """每个测试前创建新管理器"""
        self.manager = QuoteManager()
    
    def test_builtin_quotes_loaded(self):
        """测试内置名言已加载"""
        stats = self.manager.get_stats()
        
        self.assertGreater(stats['total_quotes'], 0)
        self.assertGreater(stats['language_counts']['zh'], 0)
        self.assertGreater(stats['language_counts']['en'], 0)
    
    def test_add_quote(self):
        """测试添加名言"""
        quote = self.manager.add_quote(
            text="新添加的名言",
            author="新作者",
            category=QuoteCategory.MOTIVATION,
            language="zh",
        )
        
        self.assertEqual(quote.text, "新添加的名言")
        self.assertIn(quote, self.manager.quotes)
    
    def test_remove_quote(self):
        """测试删除名言"""
        quote = self.manager.add_quote("要删除的名言", "作者")
        quote_id = quote.get_id()
        
        result = self.manager.remove_quote(quote_id)
        
        self.assertTrue(result)
        self.assertNotIn(quote, self.manager.quotes)
    
    def test_remove_nonexistent_quote(self):
        """测试删除不存在的名言"""
        result = self.manager.remove_quote("nonexistent_id")
        self.assertFalse(result)
    
    def test_get_random_quote(self):
        """测试获取随机名言"""
        quote = self.manager.get_random_quote()
        
        self.assertIsNotNone(quote)
        self.assertIsInstance(quote, Quote)
    
    def test_get_random_quote_by_category(self):
        """测试按类别获取随机名言"""
        quote = self.manager.get_random_quote(category=QuoteCategory.SUCCESS)
        
        self.assertIsNotNone(quote)
        self.assertEqual(quote.category, QuoteCategory.SUCCESS)
    
    def test_get_random_quote_by_language(self):
        """测试按语言获取随机名言"""
        quote = self.manager.get_random_quote(language="en")
        
        self.assertIsNotNone(quote)
        self.assertEqual(quote.language, "en")
    
    def test_get_quote_by_id(self):
        """测试根据ID获取名言"""
        quote = self.manager.add_quote("测试", "作者")
        quote_id = quote.get_id()
        
        found = self.manager.get_quote_by_id(quote_id)
        
        self.assertIsNotNone(found)
        self.assertEqual(found.text, "测试")
    
    def test_get_quotes_by_author(self):
        """测试根据作者获取名言"""
        quotes = self.manager.get_quotes_by_author("孔子")
        
        self.assertGreater(len(quotes), 0)
        for q in quotes:
            self.assertIn("孔子", q.author)
    
    def test_get_quotes_by_category(self):
        """测试根据类别获取名言"""
        quotes = self.manager.get_quotes_by_category(QuoteCategory.LIFE)
        
        self.assertGreater(len(quotes), 0)
        for q in quotes:
            self.assertEqual(q.category, QuoteCategory.LIFE)
    
    def test_search_quotes(self):
        """测试搜索名言"""
        results = self.manager.search_quotes("成功")
        
        self.assertGreater(len(results), 0)
        for q in results:
            self.assertIn("成功", q.text.lower() + q.author.lower())
    
    def test_get_daily_quote(self):
        """测试获取每日名言"""
        quote1 = self.manager.get_daily_quote()
        quote2 = self.manager.get_daily_quote()
        
        # 同一天应该返回相同的名言
        self.assertEqual(quote1.get_id(), quote2.get_id())
    
    def test_get_daily_quote_different_days(self):
        """测试不同天的每日名言"""
        # 获取今天的
        today_quote = self.manager.get_daily_quote()
        
        # 模拟昨天的
        self.manager._daily_quote = None
        self.manager._daily_quote_date = None
        
        # 由于种子不同，名言可能不同（但不一定，因为随机）
        # 这里主要测试功能正常工作
        yesterday_quote = self.manager.get_daily_quote()
        
        self.assertIsNotNone(yesterday_quote)
    
    def test_add_to_favorites(self):
        """测试添加收藏"""
        quote = self.manager.add_quote("收藏测试", "作者")
        quote_id = quote.get_id()
        
        result = self.manager.add_to_favorites(quote_id)
        
        self.assertTrue(result)
        self.assertIn(quote_id, self.manager.favorites)
        self.assertTrue(quote.is_favorite)
    
    def test_remove_from_favorites(self):
        """测试移除收藏"""
        quote = self.manager.add_quote("收藏测试", "作者")
        quote_id = quote.get_id()
        self.manager.add_to_favorites(quote_id)
        
        result = self.manager.remove_from_favorites(quote_id)
        
        self.assertTrue(result)
        self.assertNotIn(quote_id, self.manager.favorites)
        self.assertFalse(quote.is_favorite)
    
    def test_get_favorites(self):
        """测试获取收藏列表"""
        quote1 = self.manager.add_quote("收藏1", "作者1")
        quote2 = self.manager.add_quote("收藏2", "作者2")
        
        self.manager.add_to_favorites(quote1.get_id())
        self.manager.add_to_favorites(quote2.get_id())
        
        favorites = self.manager.get_favorites()
        
        self.assertEqual(len(favorites), 2)
    
    def test_get_top_quotes(self):
        """测试获取高评分名言"""
        # 添加不同评分的名言
        self.manager.add_quote("低评分", "作者", rating=1)
        self.manager.add_quote("中评分", "作者", rating=3)
        self.manager.add_quote("高评分", "作者", rating=5)
        
        top = self.manager.get_top_quotes(n=2)
        
        self.assertEqual(len(top), 2)
        # 所有返回的评分应该 >= 最高评分
        for q in top:
            self.assertGreaterEqual(q.rating, 3)
    
    def test_get_stats(self):
        """测试获取统计信息"""
        stats = self.manager.get_stats()
        
        self.assertIn('total_quotes', stats)
        self.assertIn('favorites_count', stats)
        self.assertIn('category_counts', stats)
        self.assertIn('language_counts', stats)
        
        # 验证类别统计
        for cat in QuoteCategory:
            self.assertIn(cat.value, stats['category_counts'])
    
    def test_export_import(self):
        """测试导出导入"""
        # 添加一些名言
        quote1 = self.manager.add_quote("导出测试1", "作者1")
        quote2 = self.manager.add_quote("导出测试2", "作者2")
        self.manager.add_to_favorites(quote1.get_id())
        
        # 导出
        json_data = self.manager.export_data()
        
        # 导入到新管理器
        new_manager = QuoteManager()
        count = new_manager.import_data(json_data)
        
        self.assertGreater(count, 0)
        # 验证收藏也导入
        self.assertGreater(len(new_manager.favorites), 0)


class TestQuoteFormatter(unittest.TestCase):
    """测试 QuoteFormatter 类"""
    
    def setUp(self):
        self.quote = Quote(
            text="测试名言内容",
            author="测试作者",
            tags=["测试", "示例"],
            source="测试出处",
        )
    
    def test_format_simple(self):
        """测试简洁格式"""
        formatted = QuoteFormatter.format_simple(self.quote)
        self.assertIn("测试名言内容", formatted)
    
    def test_format_card(self):
        """测试卡片格式"""
        formatted = QuoteFormatter.format_card(self.quote)
        self.assertIn("┌", formatted)
        self.assertIn("└", formatted)
    
    def test_format_banner(self):
        """测试横幅格式"""
        formatted = QuoteFormatter.format_banner(self.quote)
        self.assertIn("=", formatted)
    
    def test_format_twitter(self):
        """测试Twitter格式"""
        formatted = QuoteFormatter.format_twitter(self.quote)
        self.assertIn("#测试", formatted)
        self.assertIn("#示例", formatted)
    
    def test_format_markdown(self):
        """测试Markdown格式"""
        formatted = QuoteFormatter.format_markdown(self.quote)
        self.assertIn(">", formatted)
        self.assertIn("*", formatted)
    
    def test_format_html(self):
        """测试HTML格式"""
        formatted = QuoteFormatter.format_html(self.quote)
        self.assertIn("<blockquote>", formatted)
        self.assertIn("</blockquote>", formatted)
    
    def test_format_with_translation(self):
        """测试带翻译格式"""
        formatted = QuoteFormatter.format_with_translation(
            self.quote, "Test translation"
        )
        self.assertIn("Test translation", formatted)
    
    def test_format_list(self):
        """测试列表格式"""
        quotes = [
            Quote(text="名言1", author="作者1"),
            Quote(text="名言2", author="作者2"),
        ]
        
        formatted = QuoteFormatter.format_list(quotes)
        
        self.assertIn("1.", formatted)
        self.assertIn("2.", formatted)
        self.assertIn("名言1", formatted)
        self.assertIn("名言2", formatted)


class TestQuoteUtils(unittest.TestCase):
    """测试 QuoteUtils 类"""
    
    def test_random_quote(self):
        """测试随机名言便捷方法"""
        quote = QuoteUtils.random_quote()
        
        self.assertIsNotNone(quote)
        self.assertIsInstance(quote, Quote)
    
    def test_random_quote_by_category(self):
        """测试按类别获取随机名言"""
        quote = QuoteUtils.random_quote(category="success")
        
        if quote:  # 可能没有该类别的名言
            self.assertEqual(quote.category.value, "success")
    
    def test_daily_quote(self):
        """测试每日名言"""
        quote = QuoteUtils.daily_quote()
        
        self.assertIsNotNone(quote)
        self.assertIsInstance(quote, Quote)
    
    def test_search(self):
        """测试搜索"""
        results = QuoteUtils.search("人生")
        
        self.assertIsInstance(results, list)
        self.assertGreater(len(results), 0)
    
    def test_by_author(self):
        """测试按作者获取"""
        results = QuoteUtils.by_author("孔子")
        
        self.assertIsInstance(results, list)
        self.assertGreater(len(results), 0)
    
    def test_by_category(self):
        """测试按类别获取"""
        results = QuoteUtils.by_category("wisdom")
        
        self.assertIsInstance(results, list)
        self.assertGreater(len(results), 0)
    
    def test_format(self):
        """测试格式化"""
        quote = Quote(text="测试", author="作者")
        formatted = QuoteUtils.format(quote, "simple")
        
        self.assertIn("测试", formatted)
    
    def test_categories(self):
        """测试获取类别列表"""
        categories = QuoteUtils.categories()
        
        self.assertIsInstance(categories, list)
        self.assertIn("wisdom", categories)
        self.assertIn("success", categories)
    
    def test_add_custom_quote(self):
        """测试添加自定义名言"""
        quote = QuoteUtils.add_custom_quote(
            text="自定义名言",
            author="自定义作者",
            category="motivation",
        )
        
        self.assertEqual(quote.text, "自定义名言")
        self.assertEqual(quote.author, "自定义作者")


class TestConvenienceFunctions(unittest.TestCase):
    """测试便捷函数"""
    
    def test_get_quote(self):
        """测试 get_quote 函数"""
        quote = get_quote()
        
        self.assertIsNotNone(quote)
        self.assertIsInstance(quote, Quote)
    
    def test_get_quote_with_category(self):
        """测试带类别的 get_quote"""
        quote = get_quote(category="life")
        
        if quote:
            self.assertEqual(quote.category.value, "life")
    
    def test_get_daily_quote(self):
        """测试 get_daily_quote 函数"""
        quote = get_daily_quote()
        
        self.assertIsNotNone(quote)
    
    def test_search_quotes(self):
        """测试 search_quotes 函数"""
        results = search_quotes("学习")
        
        self.assertIsInstance(results, list)
    
    def test_format_quote(self):
        """测试 format_quote 函数"""
        quote = Quote(text="测试", author="作者")
        formatted = format_quote(quote)
        
        self.assertIn("测试", formatted)
    
    def test_format_quote_with_style(self):
        """测试带样式的 format_quote"""
        quote = Quote(text="测试", author="作者")
        formatted = format_quote(quote, style="card")
        
        self.assertIn("┌", formatted)
    
    def test_list_categories(self):
        """测试 list_categories 函数"""
        categories = list_categories()
        
        self.assertIsInstance(categories, list)
        self.assertGreater(len(categories), 0)


class TestQuoteCategory(unittest.TestCase):
    """测试 QuoteCategory 枚举"""
    
    def test_all_categories_exist(self):
        """测试所有类别存在"""
        expected = [
            'life', 'success', 'wisdom', 'love', 'courage',
            'motivation', 'learning', 'work', 'health', 'friendship',
            'time', 'happiness', 'philosophy', 'nature', 'humor', 'chinese',
        ]
        
        for cat in expected:
            self.assertIn(cat, [c.value for c in QuoteCategory])
    
    def test_category_from_string(self):
        """测试从字符串创建类别"""
        cat = QuoteCategory("wisdom")
        self.assertEqual(cat, QuoteCategory.WISDOM)


class TestQuoteStyle(unittest.TestCase):
    """测试 QuoteStyle 枚举"""
    
    def test_all_styles_exist(self):
        """测试所有样式存在"""
        expected = ['simple', 'card', 'banner', 'signature', 'minimal', 'decorated']
        
        for style in expected:
            self.assertIn(style, [s.value for s in QuoteStyle])


class TestEdgeCases(unittest.TestCase):
    """测试边界情况"""
    
    def setUp(self):
        self.manager = QuoteManager()
    
    def test_empty_search(self):
        """测试空搜索"""
        results = self.manager.search_quotes("不存在的关键词xyz123")
        
        self.assertIsInstance(results, list)
        self.assertEqual(len(results), 0)
    
    def test_empty_category_quotes(self):
        """测试空类别名言"""
        # 使用一个可能没有名言的类别
        quotes = self.manager.get_quotes_by_category(QuoteCategory.NATURE)
        
        self.assertIsInstance(quotes, list)
    
    def test_min_rating_filter(self):
        """测试最低评分筛选"""
        # 添加低评分名言
        self.manager.add_quote("低评分", "作者", rating=1)
        
        quotes = self.manager.get_random_quote(min_rating=5)
        
        if quotes:
            self.assertGreaterEqual(quotes.rating, 5)
    
    def test_very_long_quote_text(self):
        """测试很长的名言文本"""
        long_text = "这是一个非常长的名言内容" * 10
        quote = Quote(text=long_text, author="作者")
        
        # 格式化应该正常工作
        formatted = quote.format(QuoteStyle.SIMPLE)
        self.assertIn(long_text, formatted)
    
    def test_special_characters_in_quote(self):
        """测试名言中的特殊字符"""
        quote = Quote(
            text="名言包含特殊字符：\n\t\"'",
            author="作者"
        )
        
        # 应该正常处理
        data = quote.to_dict()
        restored = Quote.from_dict(data)
        
        self.assertEqual(restored.text, quote.text)


if __name__ == "__main__":
    unittest.main(verbosity=2)