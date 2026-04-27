"""
Emoji Utils 测试文件

测试所有 emoji_utils 功能
"""

import sys
import os
import unittest

# Add module directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mod import (
    detect_emoji,
    extract_emoji,
    remove_emoji,
    replace_emoji,
    count_emoji,
    get_emoji_frequency,
    get_emoji_description,
    categorize_emoji,
    group_emoji_by_category,
    extract_unique_emoji,
    is_only_emoji,
    get_text_emoji_ratio,
    sanitize_text,
    analyze,
    EmojiUtils,
    EmojiCategory,
)


class TestDetectEmoji(unittest.TestCase):
    """测试 detect_emoji 函数"""
    
    def test_detect_emoji_with_emoji(self):
        """测试包含 emoji 的文本"""
        self.assertTrue(detect_emoji("Hello! 👋"))
        self.assertTrue(detect_emoji("😊😊😊"))
        self.assertTrue(detect_emoji("Test 🚀 test"))
    
    def test_detect_emoji_without_emoji(self):
        """测试不包含 emoji 的文本"""
        self.assertFalse(detect_emoji("Hello World"))
        self.assertFalse(detect_emoji("测试文本"))
        self.assertFalse(detect_emoji("123456"))
    
    def test_detect_emoji_empty_string(self):
        """测试空字符串"""
        self.assertFalse(detect_emoji(""))
    
    def test_detect_emoji_multiple_emoji(self):
        """测试多个 emoji"""
        self.assertTrue(detect_emoji("👋😊🌍🚀❤️"))


class TestExtractEmoji(unittest.TestCase):
    """测试 extract_emoji 函数"""
    
    def test_extract_single_emoji(self):
        """测试提取单个 emoji"""
        result = extract_emoji("Hello! 👋")
        self.assertEqual(result, ["👋"])
    
    def test_extract_multiple_emoji(self):
        """测试提取多个 emoji"""
        result = extract_emoji("Hello! 👋😊 World! 🌍")
        self.assertEqual(result, ["👋", "😊", "🌍"])
    
    def test_extract_no_emoji(self):
        """测试无 emoji 的文本"""
        result = extract_emoji("Hello World")
        self.assertEqual(result, [])
    
    def test_extract_only_emoji(self):
        """测试只有 emoji 的文本"""
        result = extract_emoji("👋😊🌍")
        self.assertEqual(result, ["👋", "😊", "🌍"])
    
    def test_extract_empty_string(self):
        """测试空字符串"""
        result = extract_emoji("")
        self.assertEqual(result, [])


class TestRemoveEmoji(unittest.TestCase):
    """测试 remove_emoji 函数"""
    
    def test_remove_single_emoji(self):
        """测试移除单个 emoji"""
        result = remove_emoji("Hello! 👋")
        self.assertEqual(result, "Hello! ")
    
    def test_remove_multiple_emoji(self):
        """测试移除多个 emoji"""
        result = remove_emoji("Hello! 👋😊 World! 🌍")
        self.assertEqual(result, "Hello!  World! ")
    
    def test_remove_with_replacement(self):
        """测试使用替换文本"""
        result = remove_emoji("Hello! 👋", "[X]")
        self.assertEqual(result, "Hello! [X]")
    
    def test_remove_no_emoji(self):
        """测试无 emoji 的文本"""
        result = remove_emoji("Hello World")
        self.assertEqual(result, "Hello World")
    
    def test_remove_empty_string(self):
        """测试空字符串"""
        result = remove_emoji("")
        self.assertEqual(result, "")


class TestReplaceEmoji(unittest.TestCase):
    """测试 replace_emoji 函数"""
    
    def test_replace_with_default(self):
        """测试默认替换"""
        result = replace_emoji("Hello! 👋")
        self.assertEqual(result, "Hello! [waving hand]")
    
    def test_replace_multiple_emoji(self):
        """测试替换多个 emoji"""
        result = replace_emoji("Hi! 😊❤️")
        self.assertTrue("[smiling face with smiling eyes]" in result)
        self.assertTrue("[red heart]" in result)
    
    def test_replace_with_custom_map(self):
        """测试自定义替换映射"""
        custom_map = {"👋": "HELLO"}
        result = replace_emoji("Hi! 👋", replacement_map=custom_map)
        self.assertEqual(result, "Hi! [HELLO]")
    
    def test_replace_unknown_emoji(self):
        """测试未知 emoji 的替换"""
        # 使用一个常见 emoji
        result = replace_emoji("Test 😊", default_replacement="<EMOJI>")
        self.assertTrue("[smiling face with smiling eyes]" in result or "<EMOJI>" in result)


class TestCountEmoji(unittest.TestCase):
    """测试 count_emoji 函数"""
    
    def test_count_single_emoji(self):
        """测试计数单个 emoji"""
        result = count_emoji("Hello! 👋")
        self.assertEqual(result, 1)
    
    def test_count_multiple_emoji(self):
        """测试计数多个 emoji"""
        result = count_emoji("Hello! 👋😊🌍")
        self.assertEqual(result, 3)
    
    def test_count_repeated_emoji(self):
        """测试计数重复 emoji"""
        result = count_emoji("👋👋👋")
        self.assertEqual(result, 3)
    
    def test_count_no_emoji(self):
        """测试无 emoji"""
        result = count_emoji("Hello World")
        self.assertEqual(result, 0)


class TestGetEmojiFrequency(unittest.TestCase):
    """测试 get_emoji_frequency 函数"""
    
    def test_frequency_single_emoji(self):
        """测试单个 emoji 频率"""
        result = get_emoji_frequency("Hello! 👋")
        self.assertEqual(result, {"👋": 1})
    
    def test_frequency_multiple_unique(self):
        """测试多个不同 emoji"""
        result = get_emoji_frequency("👋😊🌍")
        self.assertEqual(result, {"👋": 1, "😊": 1, "🌍": 1})
    
    def test_frequency_repeated(self):
        """测试重复 emoji"""
        result = get_emoji_frequency("👋😊👋😊👋")
        self.assertEqual(result, {"👋": 3, "😊": 2})
    
    def test_frequency_no_emoji(self):
        """测试无 emoji"""
        result = get_emoji_frequency("Hello World")
        self.assertEqual(result, {})


class TestGetEmojiDescription(unittest.TestCase):
    """测试 get_emoji_description 函数"""
    
    def test_description_known_emoji(self):
        """测试已知 emoji 描述"""
        self.assertEqual(get_emoji_description("👋"), "waving hand")
        self.assertEqual(get_emoji_description("❤️"), "red heart")
        self.assertEqual(get_emoji_description("😊"), "smiling face with smiling eyes")
    
    def test_description_unknown_emoji(self):
        """测试未知 emoji"""
        # 使用一个可能在映射中的 emoji
        result = get_emoji_description("😀")
        self.assertIn(result, ["grinning face", "unknown emoji"])


class TestCategorizeEmoji(unittest.TestCase):
    """测试 categorize_emoji 函数"""
    
    def test_categorize_face(self):
        """测试表情脸类别"""
        self.assertEqual(categorize_emoji("😊"), EmojiCategory.FACES)
        self.assertEqual(categorize_emoji("😀"), EmojiCategory.FACES)
    
    def test_categorize_animal(self):
        """测试动物类别"""
        self.assertEqual(categorize_emoji("🐶"), EmojiCategory.ANIMALS)
        self.assertEqual(categorize_emoji("🐱"), EmojiCategory.ANIMALS)
    
    def test_categorize_symbol(self):
        """测试符号类别"""
        # 心形通常属于符号类
        category = categorize_emoji("❤️")
        self.assertIn(category, [EmojiCategory.SYMBOLS, EmojiCategory.FACES])


class TestGroupEmojiByCategory(unittest.TestCase):
    """测试 group_emoji_by_category 函数"""
    
    def test_group_mixed_emoji(self):
        """测试混合 emoji 分组"""
        emojis = ["😊", "🐶", "🍎"]
        result = group_emoji_by_category(emojis)
        
        self.assertIn(EmojiCategory.FACES, result)
        self.assertIn(EmojiCategory.ANIMALS, result)
        self.assertIn("😊", result[EmojiCategory.FACES])
        self.assertIn("🐶", result[EmojiCategory.ANIMALS])
    
    def test_group_empty_list(self):
        """测试空列表"""
        result = group_emoji_by_category([])
        self.assertEqual(result, {})


class TestExtractUniqueEmoji(unittest.TestCase):
    """测试 extract_unique_emoji 函数"""
    
    def test_unique_with_duplicates(self):
        """测试有重复的情况"""
        result = extract_unique_emoji("👋😊👋😊🌍")
        self.assertEqual(result, {"👋", "😊", "🌍"})
    
    def test_unique_no_duplicates(self):
        """测试无重复的情况"""
        result = extract_unique_emoji("👋😊🌍")
        self.assertEqual(result, {"👋", "😊", "🌍"})
    
    def test_unique_no_emoji(self):
        """测试无 emoji"""
        result = extract_unique_emoji("Hello World")
        self.assertEqual(result, set())


class TestIsOnlyEmoji(unittest.TestCase):
    """测试 is_only_emoji 函数"""
    
    def test_only_emoji_true(self):
        """测试只有 emoji"""
        self.assertTrue(is_only_emoji("👋😊🌍"))
        self.assertTrue(is_only_emoji("❤️"))
    
    def test_only_emoji_false(self):
        """测试包含其他字符"""
        self.assertFalse(is_only_emoji("Hello 👋"))
        self.assertFalse(is_only_emoji("Test 123"))
    
    def test_only_emoji_empty(self):
        """测试空字符串"""
        self.assertFalse(is_only_emoji(""))
    
    def test_only_emoji_whitespace(self):
        """测试只有空白"""
        self.assertFalse(is_only_emoji("   "))


class TestGetTextEmojiRatio(unittest.TestCase):
    """测试 get_text_emoji_ratio 函数"""
    
    def test_ratio_half(self):
        """测试比例"""
        # "Hi👋" = 2个字母 + 1个emoji = 3个字符，比例是 1/3 ≈ 0.333
        # 使用 "A👋" = 1个字母 + 1个emoji = 2个字符，比例是 0.5
        result = get_text_emoji_ratio("A👋")
        self.assertEqual(result, 0.5)
    
    def test_ratio_all_emoji(self):
        """测试 100% emoji"""
        result = get_text_emoji_ratio("👋😊🌍")
        self.assertEqual(result, 1.0)
    
    def test_ratio_no_emoji(self):
        """测试 0% emoji"""
        result = get_text_emoji_ratio("Hello")
        self.assertEqual(result, 0.0)
    
    def test_ratio_empty(self):
        """测试空字符串"""
        result = get_text_emoji_ratio("")
        self.assertEqual(result, 0.0)


class TestSanitizeText(unittest.TestCase):
    """测试 sanitize_text 函数"""
    
    def test_sanitize_within_limit(self):
        """测试在限制内"""
        result = sanitize_text("Hello! 👋", max_emoji_ratio=0.3)
        self.assertEqual(result, "Hello! 👋")
    
    def test_sanitize_exceeds_limit(self):
        """测试超过限制"""
        result = sanitize_text("👋👋👋👋👋", max_emoji_ratio=0.3)
        self.assertEqual(result, "")
    
    def test_sanitize_empty(self):
        """测试空字符串"""
        result = sanitize_text("")
        self.assertEqual(result, "")


class TestAnalyze(unittest.TestCase):
    """测试 analyze 函数"""
    
    def test_analyze_complete(self):
        """测试完整分析"""
        result = analyze("Hello! 👋😊👋")
        
        self.assertTrue(result['has_emoji'])
        self.assertEqual(result['emoji_count'], 3)
        self.assertEqual(result['unique_count'], 2)
        self.assertIn('frequency', result)
        self.assertIn('ratio', result)
        self.assertIn('categories', result)
    
    def test_analyze_no_emoji(self):
        """测试无 emoji 分析"""
        result = analyze("Hello World")
        
        self.assertFalse(result['has_emoji'])
        self.assertEqual(result['emoji_count'], 0)
        self.assertEqual(result['unique_count'], 0)


class TestEmojiUtilsClass(unittest.TestCase):
    """测试 EmojiUtils 类"""
    
    def test_emoji_utils_basic(self):
        """测试基本功能"""
        utils = EmojiUtils("Hello! 👋😊")
        
        self.assertTrue(utils.has_emoji)
        self.assertEqual(utils.emoji_count, 2)
        self.assertEqual(len(utils.emojis), 2)
    
    def test_emoji_utils_unique(self):
        """测试唯一 emoji"""
        utils = EmojiUtils("👋😊👋")
        
        self.assertEqual(len(utils.unique_emojis), 2)
    
    def test_emoji_utils_remove(self):
        """测试移除 emoji"""
        utils = EmojiUtils("Hello! 👋")
        
        result = utils.remove_emoji()
        self.assertEqual(result, "Hello! ")
    
    def test_emoji_utils_replace(self):
        """测试替换 emoji"""
        utils = EmojiUtils("Hello! 👋")
        
        result = utils.replace_emoji()
        self.assertTrue("[waving hand]" in result)
    
    def test_emoji_utils_text_update(self):
        """测试更新文本"""
        utils = EmojiUtils("Hello! 👋")
        self.assertEqual(utils.emoji_count, 1)
        
        utils.text = "Hi! 👋😊🌍"
        self.assertEqual(utils.emoji_count, 3)
    
    def test_emoji_utils_ratio(self):
        """测试 emoji 比例"""
        # "A👋" = 1个字母 + 1个emoji，比例是 0.5
        utils = EmojiUtils("A👋")
        
        self.assertEqual(utils.emoji_ratio(), 0.5)
    
    def test_emoji_utils_sanitize(self):
        """测试清理"""
        utils = EmojiUtils("👋👋👋")
        
        result = utils.sanitize(max_ratio=0.3)
        self.assertEqual(result, "")


class TestEdgeCases(unittest.TestCase):
    """测试边界情况"""
    
    def test_combining_characters(self):
        """测试组合字符（肤色修饰符等）"""
        # 带肤色修饰符的 emoji
        text = "👋🏻👋🏿"
        result = extract_emoji(text)
        self.assertGreaterEqual(len(result), 1)
    
    def test_zwj_sequences(self):
        """测试零宽连接符序列"""
        # 家庭 emoji 等复杂组合
        text = "👨‍👩‍👧‍👦"
        self.assertTrue(detect_emoji(text))
    
    def test_long_text(self):
        """测试长文本"""
        text = "Hello " * 1000 + "👋"
        self.assertTrue(detect_emoji(text))
        self.assertEqual(count_emoji(text), 1)
    
    def test_only_emoji_long(self):
        """测试长 emoji 序列"""
        text = "👋" * 100
        self.assertTrue(is_only_emoji(text))
        self.assertEqual(count_emoji(text), 100)
    
    def test_mixed_languages(self):
        """测试混合语言"""
        text = "你好 👋 こんにちは 😊 안녕하세요 🌍"
        self.assertTrue(detect_emoji(text))
        self.assertEqual(count_emoji(text), 3)


if __name__ == "__main__":
    unittest.main(verbosity=2)