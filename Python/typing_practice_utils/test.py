"""
Tests for typing_practice_utils
打字练习工具测试模块
"""

import unittest
import time
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from mod import (
    TextGenerator, TypingAnalyzer, TypingPractice,
    Difficulty, TextType, TypingResult,
    generate_practice_text, analyze_typing, quick_practice
)


class TestTextGenerator(unittest.TestCase):
    """测试文本生成器"""
    
    def test_generate_easy_words(self):
        """测试生成简单单词"""
        text = TextGenerator.generate_words(10, Difficulty.EASY)
        words = text.split()
        self.assertEqual(len(words), 10)
        # 所有单词应该来自 EASY_WORDS
        for word in words:
            self.assertIn(word.lower(), [w.lower() for w in TextGenerator.EASY_WORDS])
    
    def test_generate_hard_words(self):
        """测试生成困难单词"""
        text = TextGenerator.generate_words(5, Difficulty.HARD)
        words = text.split()
        self.assertEqual(len(words), 5)
    
    def test_generate_sentence(self):
        """测试生成句子"""
        text = TextGenerator.generate_sentence(Difficulty.MEDIUM)
        self.assertIsInstance(text, str)
        self.assertTrue(len(text) > 0)
    
    def test_generate_paragraph(self):
        """测试生成段落"""
        text = TextGenerator.generate_paragraph(3)
        self.assertIsInstance(text, str)
        # 应该包含多个句子
        self.assertTrue("." in text)
    
    def test_generate_code(self):
        """测试生成代码"""
        text = TextGenerator.generate_code(3)
        self.assertIsInstance(text, str)
        self.assertTrue(len(text) > 0)
    
    def test_generate_numbers(self):
        """测试生成数字"""
        text = TextGenerator.generate_numbers(5)
        parts = text.split()
        self.assertEqual(len(parts), 5)
    
    def test_generate_mixed(self):
        """测试生成混合文本"""
        text = TextGenerator.generate_mixed(30)
        self.assertGreaterEqual(len(text), 30)
    
    def test_generate_with_type_parameter(self):
        """测试通过类型参数生成"""
        # 测试所有类型
        for text_type in TextType:
            text = TextGenerator.generate(text_type)
            self.assertIsInstance(text, str)
            self.assertTrue(len(text) > 0)


class TestTypingAnalyzer(unittest.TestCase):
    """测试打字分析器"""
    
    def test_calculate_wpm(self):
        """测试 WPM 计算"""
        # 50 个字符 = 10 个单词，用时 30 秒 = 0.5 分钟
        # WPM = 10 / 0.5 = 20
        text = "a" * 50
        wpm = TypingAnalyzer.calculate_wpm(text, 30)
        self.assertAlmostEqual(wpm, 20.0, places=1)
    
    def test_calculate_wpm_zero_time(self):
        """测试零时间 WPM"""
        wpm = TypingAnalyzer.calculate_wpm("test", 0)
        self.assertEqual(wpm, 0.0)
    
    def test_calculate_cpm(self):
        """测试 CPM 计算"""
        # 100 个字符，用时 60 秒 = 1 分钟
        # CPM = 100 / 1 = 100
        text = "a" * 100
        cpm = TypingAnalyzer.calculate_cpm(text, 60)
        self.assertAlmostEqual(cpm, 100.0, places=1)
    
    def test_calculate_accuracy_perfect(self):
        """测试完美准确率"""
        original = "hello world"
        typed = "hello world"
        accuracy, correct, total, errors = TypingAnalyzer.calculate_accuracy(original, typed)
        
        self.assertEqual(accuracy, 100.0)
        self.assertEqual(correct, 11)
        self.assertEqual(total, 11)
        self.assertEqual(len(errors), 0)
    
    def test_calculate_accuracy_with_errors(self):
        """测试有错误的准确率"""
        original = "hello world"
        typed = "hallo world"  # 'e' 被 'a' 替换
        accuracy, correct, total, errors = TypingAnalyzer.calculate_accuracy(original, typed)
        
        self.assertLess(accuracy, 100.0)
        self.assertEqual(correct, 10)
        self.assertEqual(total, 11)
        self.assertEqual(len(errors), 1)
        self.assertEqual(errors[0], (1, 'e', 'a'))
    
    def test_calculate_accuracy_extra_chars(self):
        """测试多输入字符的情况"""
        original = "hello"
        typed = "hello!"
  # 多了一个 !
        accuracy, correct, total, errors = TypingAnalyzer.calculate_accuracy(original, typed)
        
        self.assertLess(accuracy, 100.0)
        self.assertEqual(correct, 5)
        self.assertEqual(total, 6)
        self.assertEqual(len(errors), 1)
    
    def test_calculate_accuracy_missing_chars(self):
        """测试少输字符的情况"""
        original = "hello world"
        typed = "hello worl"  # 少了 'd'
        accuracy, correct, total, errors = TypingAnalyzer.calculate_accuracy(original, typed)
        
        self.assertLess(accuracy, 100.0)
        self.assertEqual(correct, 10)
        self.assertEqual(total, 11)
    
    def test_analyze_full(self):
        """测试完整分析"""
        original = "test text"
        typed = "test text"
        time_sec = 10.0
        
        result = TypingAnalyzer.analyze(original, typed, time_sec)
        
        self.assertIsInstance(result, TypingResult)
        self.assertEqual(result.original_text, original)
        self.assertEqual(result.typed_text, typed)
        self.assertEqual(result.time_seconds, time_sec)
        self.assertEqual(result.accuracy, 100.0)
        self.assertEqual(len(result.errors), 0)
        self.assertGreater(result.wpm, 0)
        self.assertGreater(result.cpm, 0)


class TestTypingPractice(unittest.TestCase):
    """测试打字练习主类"""
    
    def test_start_session(self):
        """测试开始会话"""
        practice = TypingPractice()
        text = practice.start_session(TextType.WORDS, Difficulty.EASY, count=10)
        
        self.assertIsInstance(text, str)
        words = text.split()
        self.assertEqual(len(words), 10)
    
    def test_begin_typing(self):
        """测试开始计时"""
        practice = TypingPractice()
        practice.start_session()
        practice.begin_typing()
        
        self.assertIsNotNone(practice._start_time)
    
    def test_finish_typing(self):
        """测试结束输入"""
        practice = TypingPractice()
        text = practice.start_session(TextType.WORDS, Difficulty.EASY, count=5)
        practice.begin_typing()
        time.sleep(0.1)  # 模拟输入时间
        result = practice.finish_typing(text)
        
        self.assertIsInstance(result, TypingResult)
        self.assertEqual(len(practice.history), 1)
    
    def test_finish_without_begin(self):
        """测试未开始计时就结束"""
        practice = TypingPractice()
        practice.start_session()
        
        with self.assertRaises(ValueError):
            practice.finish_typing("test")
    
    def test_get_statistics_empty(self):
        """测试空历史统计"""
        practice = TypingPractice()
        stats = practice.get_statistics()
        
        self.assertEqual(stats["total_sessions"], 0)
        self.assertEqual(stats["average_wpm"], 0)
        self.assertEqual(stats["average_accuracy"], 0)
    
    def test_get_statistics_with_history(self):
        """测试有历史的统计"""
        practice = TypingPractice()
        
        # 添加一些模拟结果
        for _ in range(3):
            text = practice.start_session(TextType.WORDS, Difficulty.EASY, count=5)
            practice.begin_typing()
            time.sleep(0.05)
            practice.finish_typing(text)
        
        stats = practice.get_statistics()
        
        self.assertEqual(stats["total_sessions"], 3)
        self.assertGreater(stats["average_wpm"], 0)
        self.assertEqual(stats["average_accuracy"], 100.0)
    
    def test_clear_history(self):
        """测试清除历史"""
        practice = TypingPractice()
        
        text = practice.start_session(TextType.WORDS, Difficulty.EASY, count=5)
        practice.begin_typing()
        practice.finish_typing(text)
        
        self.assertEqual(len(practice.history), 1)
        
        practice.clear_history()
        self.assertEqual(len(practice.history), 0)
    
    def test_get_performance_level(self):
        """测试性能等级"""
        levels = [
            (10, "初级"),
            (25, "入门"),
            (35, "中级"),
            (45, "熟练"),
            (55, "精通"),
            (70, "专家"),
            (90, "大师"),
        ]
        
        for wpm, expected_keyword in levels:
            level = TypingPractice.get_performance_level(wpm)
            self.assertIn(expected_keyword, level)


class TestConvenienceFunctions(unittest.TestCase):
    """测试便捷函数"""
    
    def test_generate_practice_text(self):
        """测试便捷生成函数"""
        text = generate_practice_text(TextType.WORDS, Difficulty.EASY, count=10)
        self.assertIsInstance(text, str)
        self.assertEqual(len(text.split()), 10)
    
    def test_analyze_typing(self):
        """测试便捷分析函数"""
        result = analyze_typing("hello", "hello", 5.0)
        self.assertIsInstance(result, TypingResult)
        self.assertEqual(result.accuracy, 100.0)
    
    def test_quick_practice(self):
        """测试快速练习"""
        text, finish = quick_practice(Difficulty.EASY, 5)
        
        self.assertIsInstance(text, str)
        self.assertEqual(len(text.split()), 5)
        
        result = finish(text)
        self.assertIsInstance(result, TypingResult)
        self.assertEqual(result.accuracy, 100.0)


class TestTypingResult(unittest.TestCase):
    """测试 TypingResult 数据类"""
    
    def test_str_representation(self):
        """测试字符串表示"""
        result = TypingResult(
            original_text="test",
            typed_text="test",
            time_seconds=5.0,
            correct_chars=4,
            total_chars=4,
            errors=[],
            wpm=24.0,
            cpm=48.0,
            accuracy=100.0
        )
        
        result_str = str(result)
        self.assertIn("WPM", result_str)
        self.assertIn("准确率", result_str)
        self.assertIn("100.0%", result_str)


if __name__ == "__main__":
    unittest.main()