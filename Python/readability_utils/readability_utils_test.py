"""
readability_utils 测试套件

测试文本可读性分析功能
"""

import unittest
from mod import (
    ReadabilityResult,
    TextStats,
    ReadabilityAnalyzer,
    ChineseReadabilityAnalyzer,
    analyze_readability,
    get_grade_level,
    count_syllables
)


class TestTextStats(unittest.TestCase):
    """TextStats 测试"""
    
    def test_sentence_splitting(self):
        """测试句子分割"""
        text = "Hello world. This is a test. How are you?"
        stats = TextStats(text)
        self.assertEqual(stats.total_sentences, 3)
    
    def test_word_extraction(self):
        """测试单词提取"""
        text = "The quick brown fox jumps over the lazy dog."
        stats = TextStats(text)
        self.assertEqual(stats.total_words, 9)
    
    def test_syllable_counting(self):
        """测试音节计数"""
        # 测试简单单词
        self.assertEqual(count_syllables('cat'), 1)
        self.assertEqual(count_syllables('dog'), 1)
        self.assertEqual(count_syllables('hello'), 2)
        self.assertEqual(count_syllables('beautiful'), 3)
        self.assertEqual(count_syllables('information'), 4)
    
    def test_syllable_exceptions(self):
        """测试音节例外"""
        self.assertEqual(count_syllables('the'), 1)
        self.assertEqual(count_syllables('eye'), 1)
        self.assertEqual(count_syllables('science'), 2)
    
    def test_complex_words(self):
        """测试复杂单词计数"""
        text = "The beautiful information technology industry."
        stats = TextStats(text)
        # beautiful(3), information(4), technology(4), industry(3) = 4 complex words
        self.assertEqual(stats.complex_words, 4)
    
    def test_empty_text(self):
        """测试空文本"""
        stats = TextStats('')
        self.assertEqual(stats.total_sentences, 0)
        self.assertEqual(stats.total_words, 0)
        self.assertEqual(stats.total_syllables, 0)


class TestReadabilityAnalyzer(unittest.TestCase):
    """ReadabilityAnalyzer 测试"""
    
    def test_flesch_reading_ease_simple(self):
        """测试简单文本的 Flesch Reading Ease"""
        # 简单文本应该有较高的分数
        text = "The cat sat on the mat. The dog ran fast."
        analyzer = ReadabilityAnalyzer(text)
        score = analyzer.flesch_reading_ease()
        self.assertGreater(score, 80)
    
    def test_flesch_reading_ease_complex(self):
        """测试复杂文本的 Flesch Reading Ease"""
        # 复杂文本应该有较低的分数
        text = "The implementation of sophisticated algorithmic methodologies necessitates comprehensive understanding of computational complexity."
        analyzer = ReadabilityAnalyzer(text)
        score = analyzer.flesch_reading_ease()
        self.assertLess(score, 50)
    
    def test_flesch_kincaid_grade(self):
        """测试 Flesch-Kincaid 年级水平"""
        text = "The quick brown fox jumps over the lazy dog. This is a simple sentence."
        analyzer = ReadabilityAnalyzer(text)
        grade = analyzer.flesch_kincaid_grade()
        self.assertGreaterEqual(grade, 0)
        self.assertLess(grade, 12)  # 应该在高中以下
    
    def test_gunning_fog_index(self):
        """测试 Gunning Fog Index"""
        text = "The cat sat on the mat. It was a sunny day."
        analyzer = ReadabilityAnalyzer(text)
        fog = analyzer.gunning_fog_index()
        self.assertGreaterEqual(fog, 0)
    
    def test_smog_index(self):
        """测试 SMOG Index"""
        # 需要较长的文本
        text = " ".join([
            "The cat sat on the mat.",
            "The dog ran in the park.",
            "Birds fly high in the sky.",
            "Fish swim in the deep sea.",
            "Trees grow tall and strong.",
            "Children play in the yard.",
            "Students study at school.",
            "Workers build new houses.",
            "Farmers grow fresh food.",
            "Doctors help sick people.",
        ])
        analyzer = ReadabilityAnalyzer(text)
        smog = analyzer.smog_index()
        self.assertGreaterEqual(smog, 0)
    
    def test_coleman_liau_index(self):
        """测试 Coleman-Liau Index"""
        text = "The cat sat on the mat. The dog ran fast."
        analyzer = ReadabilityAnalyzer(text)
        cli = analyzer.coleman_liau_index()
        self.assertGreaterEqual(cli, 0)
    
    def test_automated_readability_index(self):
        """测试 Automated Readability Index"""
        text = "The cat sat on the mat. The dog ran fast."
        analyzer = ReadabilityAnalyzer(text)
        ari = analyzer.automated_readability_index()
        self.assertGreaterEqual(ari, 0)
    
    def test_full_analysis(self):
        """测试完整分析"""
        text = "The quick brown fox jumps over the lazy dog. " \
               "This is a simple test of the readability analyzer."
        analyzer = ReadabilityAnalyzer(text)
        result = analyzer.analyze()
        
        self.assertIsInstance(result, ReadabilityResult)
        self.assertIsInstance(result.flesch_reading_ease, float)
        self.assertIsInstance(result.flesch_kincaid_grade, float)
        self.assertIsInstance(result.grade_level, str)
        self.assertGreater(result.total_words, 0)
    
    def test_empty_text_analysis(self):
        """测试空文本分析"""
        analyzer = ReadabilityAnalyzer('')
        score = analyzer.flesch_reading_ease()
        self.assertEqual(score, 0)


class TestChineseReadabilityAnalyzer(unittest.TestCase):
    """ChineseReadabilityAnalyzer 测试"""
    
    def test_simple_chinese(self):
        """测试简单中文文本"""
        text = "小猫坐在垫子上。小狗跑得很快。今天天气很好。"
        analyzer = ChineseReadabilityAnalyzer(text)
        score, desc = analyzer.get_difficulty()
        
        self.assertGreaterEqual(score, 0)
        self.assertLessEqual(score, 100)
        self.assertIn('水平', desc)
    
    def test_complex_chinese(self):
        """测试复杂中文文本"""
        text = "人工智能技术的快速发展对社会经济结构产生了深远影响，" \
               "其复杂性涉及哲学、伦理学、认知科学等多个学科领域的交叉融合。"
        analyzer = ChineseReadabilityAnalyzer(text)
        score, desc = analyzer.get_difficulty()
        
        self.assertGreater(score, 50)  # 复杂文本得分应该较高
    
    def test_chinese_statistics(self):
        """测试中文统计"""
        text = "这是第一句话。这是第二句话。这是第三句话。"
        analyzer = ChineseReadabilityAnalyzer(text)
        result = analyzer.analyze()
        
        self.assertEqual(result['sentence_count'], 3)
        self.assertGreater(result['chinese_chars'], 0)


class TestConvenienceFunctions(unittest.TestCase):
    """便捷函数测试"""
    
    def test_analyze_readability_english(self):
        """测试英文可读性分析"""
        text = "The quick brown fox jumps over the lazy dog."
        result = analyze_readability(text, 'en')
        
        self.assertIn('flesch_reading_ease', result)
        self.assertIn('flesch_kincaid_grade', result)
        self.assertIn('grade_level', result)
    
    def test_analyze_readability_chinese(self):
        """测试中文可读性分析"""
        text = "小猫坐在垫子上。小狗跑得很快。"
        result = analyze_readability(text, 'zh')
        
        self.assertIn('difficulty_score', result)
        self.assertIn('difficulty_level', result)
        self.assertIn('chinese_chars', result)
    
    def test_get_grade_level_english(self):
        """测试获取英文年级水平"""
        text = "The cat sat on the mat."
        level = get_grade_level(text, 'en')
        
        self.assertIsInstance(level, str)
        self.assertIn('年级', level)
    
    def test_get_grade_level_chinese(self):
        """测试获取中文难度水平"""
        text = "小猫坐在垫子上。"
        level = get_grade_level(text, 'zh')
        
        self.assertIsInstance(level, str)
        self.assertIn('水平', level)


class TestEdgeCases(unittest.TestCase):
    """边界情况测试"""
    
    def test_single_word(self):
        """测试单个单词"""
        text = "hello"
        analyzer = ReadabilityAnalyzer(text)
        result = analyzer.analyze()
        self.assertEqual(result.total_words, 1)
    
    def test_numbers_in_text(self):
        """测试包含数字的文本"""
        text = "There are 123 apples and 456 oranges."
        analyzer = ReadabilityAnalyzer(text)
        result = analyzer.analyze()
        self.assertGreater(result.total_words, 0)
    
    def test_special_characters(self):
        """测试特殊字符"""
        text = "Hello!!! How are you??? This is great..."
        analyzer = ReadabilityAnalyzer(text)
        result = analyzer.analyze()
        self.assertGreater(result.total_sentences, 0)
    
    def test_mixed_language(self):
        """测试混合语言文本"""
        text = "Hello 你好 World 世界"
        # 默认按英文处理
        result = analyze_readability(text, 'en')
        self.assertGreater(result['total_words'], 0)
    
    def test_very_long_text(self):
        """测试长文本"""
        text = "The cat sat on the mat. " * 100
        analyzer = ReadabilityAnalyzer(text)
        result = analyzer.analyze()
        
        self.assertGreater(result.total_sentences, 0)
        self.assertGreater(result.total_words, 0)


if __name__ == '__main__':
    unittest.main()