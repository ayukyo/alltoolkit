"""
Reading Statistics Utilities - 测试套件

测试阅读统计分析工具的所有功能。
"""

import unittest
import sys
import os

# 添加模块路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from mod import (
    count_syllables_word,
    is_chinese_char,
    is_japanese_char,
    is_korean_char,
    detect_language,
    extract_words,
    count_words,
    count_sentences,
    count_paragraphs,
    count_syllables,
    count_complex_words,
    count_difficult_words,
    count_unique_words,
    reading_time,
    speaking_time,
    flesch_reading_ease,
    flesch_kincaid_grade,
    gunning_fog_index,
    coleman_liau_index,
    automated_readability_index,
    get_readability_level,
    analyze_text,
    format_time,
    get_reading_suggestions,
    compare_texts,
    estimate_audience,
    classify_text_type,
    ReadingStats,
    READING_SPEED_AVERAGE,
    SPEAKING_SPEED
)


class TestSyllableCount(unittest.TestCase):
    """音节计数测试"""
    
    def test_single_syllable_words(self):
        """测试单音节词"""
        self.assertEqual(count_syllables_word("the"), 1)
        self.assertEqual(count_syllables_word("cat"), 1)
        self.assertEqual(count_syllables_word("dog"), 1)
        self.assertEqual(count_syllables_word("a"), 1)
    
    def test_two_syllable_words(self):
        """测试双音节词"""
        self.assertEqual(count_syllables_word("hello"), 2)
        self.assertEqual(count_syllables_word("water"), 2)
        self.assertEqual(count_syllables_word("happy"), 2)
    
    def test_multi_syllable_words(self):
        """测试多音节词"""
        self.assertEqual(count_syllables_word("beautiful"), 3)
        self.assertEqual(count_syllables_word("information"), 4)
        self.assertEqual(count_syllables_word("development"), 4)
    
    def test_silent_e(self):
        """测试静音e"""
        self.assertEqual(count_syllables_word("make"), 1)
        self.assertEqual(count_syllables_word("take"), 1)
    
    def test_empty_string(self):
        """测试空字符串"""
        self.assertEqual(count_syllables_word(""), 0)
        self.assertEqual(count_syllables_word(" "), 0)


class TestLanguageDetection(unittest.TestCase):
    """语言检测测试"""
    
    def test_chinese_char(self):
        """测试中文字符识别"""
        self.assertTrue(is_chinese_char('中'))
        self.assertTrue(is_chinese_char('文'))
        self.assertTrue(is_chinese_char('你'))
        self.assertFalse(is_chinese_char('a'))
        self.assertFalse(is_chinese_char('1'))
    
    def test_japanese_char(self):
        """测试日文字符识别"""
        self.assertTrue(is_japanese_char('あ'))  # 平假名
        self.assertTrue(is_japanese_char('ア'))  # 片假名
        self.assertFalse(is_japanese_char('a'))
    
    def test_korean_char(self):
        """测试韩文字符识别"""
        self.assertTrue(is_korean_char('한'))
        self.assertTrue(is_korean_char('국'))
        self.assertFalse(is_korean_char('a'))
    
    def test_detect_language(self):
        """测试语言检测"""
        lang = detect_language("Hello World")
        self.assertGreater(lang['english'], 0.8)
        
        lang = detect_language("你好世界")
        self.assertGreater(lang['chinese'], 0.8)
        
        lang = detect_language("Hello 世界")
        self.assertGreater(lang['english'], 0)
        self.assertGreater(lang['chinese'], 0)
    
    def test_detect_language_empty(self):
        """测试空文本的语言检测"""
        lang = detect_language("")
        self.assertEqual(lang['chinese'], 0.0)
        self.assertEqual(lang['english'], 0.0)


class TestWordCount(unittest.TestCase):
    """单词计数测试"""
    
    def test_english_words(self):
        """测试英文单词计数"""
        self.assertEqual(count_words("hello world"), 2)
        self.assertEqual(count_words("one two three four"), 4)
        self.assertEqual(count_words("Hello, World!"), 2)
    
    def test_chinese_words(self):
        """测试中文计数"""
        self.assertEqual(count_words("你好世界"), 4)
        self.assertEqual(count_words("中文测试"), 4)
    
    def test_mixed_words(self):
        """测试中英文混合计数"""
        self.assertEqual(count_words("Hello 世界"), 3)  # Hello + 世 + 界
        self.assertEqual(count_words("Python 是好的"), 4)  # Python + 是 + 好 + 的
    
    def test_extract_words(self):
        """测试单词提取"""
        words = extract_words("Hello world!")
        self.assertEqual(words, ["Hello", "world"])
        
        words = extract_words("你好 世界")
        self.assertEqual(words, ["你", "好", "世", "界"])


class TestSentenceCount(unittest.TestCase):
    """句子计数测试"""
    
    def test_english_sentences(self):
        """测试英文句子计数"""
        self.assertEqual(count_sentences("Hello world."), 1)
        self.assertEqual(count_sentences("Hello! How are you?"), 2)
        self.assertEqual(count_sentences("One. Two. Three."), 3)
    
    def test_chinese_sentences(self):
        """测试中文句子计数"""
        self.assertEqual(count_sentences("你好世界。"), 1)
        self.assertEqual(count_sentences("你好！你好吗？"), 2)
    
    def test_mixed_sentences(self):
        """测试中英文混合句子计数"""
        self.assertEqual(count_sentences("Hello world。你好！"), 2)
    
    def test_no_punctuation(self):
        """测试无标点的文本"""
        self.assertEqual(count_sentences("hello world"), 1)


class TestParagraphCount(unittest.TestCase):
    """段落计数测试"""
    
    def test_single_paragraph(self):
        """测试单段落"""
        self.assertEqual(count_paragraphs("Hello world."), 1)
        self.assertEqual(count_paragraphs("One line.\nAnother line."), 1)
    
    def test_multiple_paragraphs(self):
        """测试多段落"""
        text = "First paragraph.\n\nSecond paragraph."
        self.assertEqual(count_paragraphs(text), 2)
        
        text = "Para one.\n\nPara two.\n\nPara three."
        self.assertEqual(count_paragraphs(text), 3)


class TestSyllablesInText(unittest.TestCase):
    """文本音节计数测试"""
    
    def test_count_syllables(self):
        """测试文本音节计数"""
        self.assertEqual(count_syllables("hello"), 2)
        self.assertEqual(count_syllables("hello world"), 3)
        self.assertEqual(count_syllables("The cat"), 2)
    
    def test_complex_words(self):
        """测试复杂词计数"""
        self.assertEqual(count_complex_words("hello"), 0)
        self.assertEqual(count_complex_words("beautiful"), 1)
        self.assertEqual(count_complex_words("beautiful amazing"), 2)
    
    def test_difficult_words(self):
        """测试生僻词计数"""
        self.assertEqual(count_difficult_words("hello"), 0)
        self.assertEqual(count_difficult_words("international"), 1)
    
    def test_difficult_words_with_known(self):
        """测试带已知词表的生僻词计数"""
        known = {"hello", "world"}
        self.assertEqual(count_difficult_words("hello world", known), 0)
        self.assertEqual(count_difficult_words("hello test", known), 1)


class TestUniqueWords(unittest.TestCase):
    """不重复词计数测试"""
    
    def test_unique_words(self):
        """测试不重复词计数"""
        self.assertEqual(count_unique_words("hello"), 1)
        self.assertEqual(count_unique_words("hello world"), 2)
        self.assertEqual(count_unique_words("hello hello world"), 2)
        self.assertEqual(count_unique_words("Hello hello"), 1)  # 不区分大小写


class TestReadingTime(unittest.TestCase):
    """阅读时间测试"""
    
    def test_reading_time_english(self):
        """测试英文阅读时间"""
        # 200词 / 200词每分钟 = 1分钟
        text = "word " * 200
        time = reading_time(text, wpm=200)
        self.assertAlmostEqual(time, 1.0, places=1)
    
    def test_reading_time_chinese(self):
        """测试中文阅读时间"""
        text = "测" * 300  # 300字 / 300字每分钟 = 1分钟
        time = reading_time(text)
        self.assertAlmostEqual(time, 1.0, places=1)
    
    def test_speaking_time(self):
        """测试朗读时间"""
        text = "word " * 150  # 150词 / 150词每分钟 = 1分钟
        time = speaking_time(text)
        self.assertAlmostEqual(time, 1.0, places=1)


class TestReadabilityScores(unittest.TestCase):
    """可读性分数测试"""
    
    def test_flesch_reading_ease_simple(self):
        """测试简单文本的 Flesch Reading Ease"""
        # 简单文本应该有较高的分数
        score = flesch_reading_ease("The cat sat on the mat.")
        self.assertGreater(score, 70)
    
    def test_flesch_reading_ease_complex(self):
        """测试复杂文本的 Flesch Reading Ease"""
        # 复杂文本应该有较低的分数
        complex_text = "The implementation of sophisticated algorithms necessitates comprehensive understanding."
        score = flesch_reading_ease(complex_text)
        self.assertLess(score, 60)
    
    def test_flesch_kincaid_grade(self):
        """测试 Flesch-Kincaid 年级水平"""
        # 简单文本应该是低年级
        score = flesch_kincaid_grade("The cat sat on the mat.")
        self.assertGreaterEqual(score, 0)
        self.assertLess(score, 10)
    
    def test_gunning_fog_index(self):
        """测试 Gunning Fog 指数"""
        score = gunning_fog_index("The cat sat on the mat.")
        self.assertGreater(score, 0)
    
    def test_coleman_liau_index(self):
        """测试 Coleman-Liau 指数"""
        score = coleman_liau_index("The cat sat on the mat.")
        self.assertGreaterEqual(score, 0)
    
    def test_automated_readability_index(self):
        """测试自动化可读性指数"""
        score = automated_readability_index("The cat sat on the mat.")
        self.assertGreaterEqual(score, 0)
    
    def test_empty_text(self):
        """测试空文本"""
        self.assertEqual(flesch_reading_ease(""), 0.0)
        self.assertEqual(flesch_kincaid_grade(""), 0.0)
        self.assertEqual(gunning_fog_index(""), 0.0)


class TestReadabilityLevel(unittest.TestCase):
    """可读性等级测试"""
    
    def test_very_easy(self):
        """测试非常容易"""
        self.assertIn("5年级", get_readability_level(95))
    
    def test_easy(self):
        """测试容易"""
        self.assertIn("6年级", get_readability_level(85))
    
    def test_standard(self):
        """测试标准"""
        self.assertIn("9年级", get_readability_level(65))
    
    def test_difficult(self):
        """测试困难"""
        self.assertIn("大学", get_readability_level(40))
    
    def test_very_difficult(self):
        """测试非常困难"""
        self.assertIn("专业", get_readability_level(20))


class TestAnalyzeText(unittest.TestCase):
    """综合分析测试"""
    
    def test_basic_analysis(self):
        """测试基本分析"""
        text = "Hello world!"
        stats = analyze_text(text)
        
        self.assertEqual(stats.word_count, 2)
        self.assertEqual(stats.sentence_count, 1)
        self.assertGreater(stats.character_count, 0)
    
    def test_longer_analysis(self):
        """测试较长文本分析"""
        text = """
        The quick brown fox jumps over the lazy dog.
        This sentence contains every letter of the alphabet.
        """
        stats = analyze_text(text)
        
        self.assertGreater(stats.word_count, 10)
        self.assertGreater(stats.reading_time_minutes, 0)
        self.assertGreater(stats.flesch_reading_ease, 0)
    
    def test_analysis_with_known_words(self):
        """测试带已知词表的分析"""
        known_words = {"the", "cat", "sat", "on", "mat"}
        text = "The cat sat on the mat."
        stats = analyze_text(text, known_words)
        
        self.assertEqual(stats.word_count, 6)
    
    def test_stats_dataclass(self):
        """测试统计数据结构"""
        text = "Hello world."
        stats = analyze_text(text)
        
        # 验证所有字段都存在
        self.assertIsInstance(stats.character_count, int)
        self.assertIsInstance(stats.word_count, int)
        self.assertIsInstance(stats.sentence_count, int)
        self.assertIsInstance(stats.reading_time_minutes, float)
        self.assertIsInstance(stats.flesch_reading_ease, float)


class TestFormatTime(unittest.TestCase):
    """时间格式化测试"""
    
    def test_seconds(self):
        """测试秒"""
        self.assertEqual(format_time(0.5), "30秒")
        self.assertEqual(format_time(0.1), "6秒")
    
    def test_minutes(self):
        """测试分钟"""
        self.assertEqual(format_time(5), "5分钟")
        self.assertEqual(format_time(5.5), "5分钟30秒")
    
    def test_hours(self):
        """测试小时"""
        self.assertEqual(format_time(60), "1小时")
        self.assertEqual(format_time(90), "1小时30分钟")
    
    def test_exact_hour(self):
        """测试整小时"""
        self.assertEqual(format_time(120), "2小时")


class TestReadingSuggestions(unittest.TestCase):
    """阅读建议测试"""
    
    def test_simple_text_suggestions(self):
        """测试简单文本的建议"""
        text = "The cat sat on the mat."
        stats = analyze_text(text)
        suggestions = get_reading_suggestions(stats)
        
        self.assertGreater(len(suggestions), 0)
    
    def test_complex_text_suggestions(self):
        """测试复杂文本的建议"""
        text = "The implementation of sophisticated algorithms necessitates comprehensive understanding of computational complexity."
        stats = analyze_text(text)
        suggestions = get_reading_suggestions(stats)
        
        # 复杂文本应该有改进建议
        self.assertGreater(len(suggestions), 0)


class TestCompareTexts(unittest.TestCase):
    """文本比较测试"""
    
    def test_compare_similar_texts(self):
        """测试相似文本比较"""
        text1 = "The cat sat on the mat."
        text2 = "A dog ran in the park."
        
        comparison = compare_texts(text1, text2)
        
        self.assertIn('word_count', comparison)
        self.assertIn('flesch_reading_ease', comparison)
        self.assertEqual(len(comparison['word_count']), 2)
    
    def test_compare_different_lengths(self):
        """测试不同长度文本比较"""
        text1 = "Hello."
        text2 = "Hello world. How are you? I am fine."
        
        comparison = compare_texts(text1, text2)
        
        self.assertGreater(comparison['word_count'][1], comparison['word_count'][0])


class TestEstimateAudience(unittest.TestCase):
    """受众估算测试"""
    
    def test_children_audience(self):
        """测试儿童受众"""
        text = "The cat sat. The dog ran. It was fun."
        stats = analyze_text(text)
        audience = estimate_audience(stats)
        
        self.assertIn("小学生", audience)
    
    def test_adult_audience(self):
        """测试成人受众"""
        text = "The implementation of sophisticated algorithms necessitates comprehensive understanding of computational complexity and mathematical foundations."
        stats = analyze_text(text)
        audience = estimate_audience(stats)
        
        # 成人受众应该是大学生或专业人士
        self.assertTrue("大学" in audience or "专业" in audience or "研究生" in audience)


class TestClassifyTextType(unittest.TestCase):
    """文本类型分类测试"""
    
    def test_classify_simple_text(self):
        """测试简单文本分类"""
        text = "The cat sat on the mat. It was happy."
        stats = analyze_text(text)
        types = classify_text_type(stats)
        
        self.assertIsInstance(types, list)
        self.assertGreater(len(types), 0)
    
    def test_classify_complex_text(self):
        """测试复杂文本分类"""
        text = "The implementation of sophisticated algorithms necessitates comprehensive understanding."
        stats = analyze_text(text)
        types = classify_text_type(stats)
        
        self.assertIsInstance(types, list)


class TestEdgeCases(unittest.TestCase):
    """边界情况测试"""
    
    def test_empty_text(self):
        """测试空文本"""
        stats = analyze_text("")
        
        self.assertEqual(stats.word_count, 0)
        self.assertEqual(stats.sentence_count, 0)
        self.assertEqual(stats.reading_time_minutes, 0)
    
    def test_whitespace_only(self):
        """测试仅空白文本"""
        stats = analyze_text("   \n\t   ")
        
        self.assertEqual(stats.word_count, 0)
    
    def test_numbers_and_punctuation(self):
        """测试数字和标点"""
        stats = analyze_text("123, 456! 789?")
        
        self.assertGreaterEqual(stats.word_count, 0)
    
    def test_very_long_word(self):
        """测试非常长的单词"""
        long_word = "supercalifragilisticexpialidocious"
        stats = analyze_text(long_word)
        
        self.assertEqual(stats.word_count, 1)
        self.assertGreater(stats.avg_word_length, 20)
    
    def test_single_character(self):
        """测试单个字符"""
        stats = analyze_text("A")
        
        self.assertEqual(stats.word_count, 1)
        self.assertEqual(stats.sentence_count, 1)


if __name__ == '__main__':
    unittest.main(verbosity=2)