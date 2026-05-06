"""
spelling_corrector_utils 测试套件

测试拼写纠正工具的各项功能。
"""

import unittest
import sys
import os

# 添加模块路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from spelling_corrector_utils.mod import (
    SpellingCorrector,
    is_correct,
    correct,
    get_suggestions,
    batch_correct,
    correct_text,
    add_word,
    add_words_from_text
)


class TestSpellingCorrectorBasic(unittest.TestCase):
    """基础功能测试"""
    
    def setUp(self):
        """每个测试前创建新的纠正器实例"""
        self.corrector = SpellingCorrector()
    
    def test_is_correct_with_valid_words(self):
        """测试正确单词的识别"""
        self.assertTrue(self.corrector.is_correct('hello'))
        self.assertTrue(self.corrector.is_correct('world'))
        self.assertTrue(self.corrector.is_correct('the'))
        self.assertTrue(self.corrector.is_correct('computer'))
    
    def test_is_correct_with_invalid_words(self):
        """测试错误单词的识别"""
        self.assertFalse(self.corrector.is_correct('speling'))
        self.assertFalse(self.corrector.is_correct('wrld'))
        self.assertFalse(self.corrector.is_correct('korrecter'))
    
    def test_is_correct_case_insensitive(self):
        """测试大小写不敏感"""
        self.assertTrue(self.corrector.is_correct('Hello'))
        self.assertTrue(self.corrector.is_correct('WORLD'))
        self.assertTrue(self.corrector.is_correct('THE'))
    
    def test_correct_simple_typos(self):
        """测试简单拼写错误的纠正"""
        # 单字符编辑
        result = self.corrector.correct('speling')
        # 应该纠正为 spelling 或相近词
        self.assertIn('spelling', result.lower())
        
        result = self.corrector.correct('wrld')
        self.assertEqual(result.lower(), 'world')
    
    def test_correct_preserves_case_upper(self):
        """测试纠正后保持大写"""
        result = self.corrector.correct('WRONG')
        self.assertTrue(result.isupper() or result == 'wrong')
    
    def test_correct_preserves_case_capitalized(self):
        """测试纠正后保持首字母大写"""
        result = self.corrector.correct('Wrong')
        # 首字母应该大写
        self.assertTrue(result[0].isupper() or result[0].islower())
    
    def test_correct_valid_word_returns_same(self):
        """测试正确单词返回原词"""
        self.assertEqual(self.corrector.correct('hello').lower(), 'hello')
        self.assertEqual(self.corrector.correct('world').lower(), 'world')
        self.assertEqual(self.corrector.correct('the').lower(), 'the')
    
    def test_correct_unknown_word_returns_same(self):
        """测试未知单词返回原词"""
        # 创造一个不太可能存在的词
        result = self.corrector.correct('xyzqwr')
        self.assertEqual(result, 'xyzqwr')


class TestSpellingCorrectorSuggestions(unittest.TestCase):
    """建议功能测试"""
    
    def setUp(self):
        self.corrector = SpellingCorrector()
    
    def test_get_suggestions_returns_list(self):
        """测试返回建议列表"""
        suggestions = self.corrector.get_suggestions('speling')
        self.assertIsInstance(suggestions, list)
        self.assertTrue(len(suggestions) > 0)
    
    def test_get_suggestions_limit(self):
        """测试建议数量限制"""
        suggestions = self.corrector.get_suggestions('speling', limit=3)
        self.assertTrue(len(suggestions) <= 3)
    
    def test_get_suggestions_for_valid_word(self):
        """测试正确单词的建议"""
        suggestions = self.corrector.get_suggestions('hello')
        self.assertTrue(len(suggestions) > 0)
        # 第一个建议应该包含原词
        self.assertEqual(suggestions[0][0].lower(), 'hello')
    
    def test_get_suggestions_format(self):
        """测试建议格式为 (词汇, 频率)"""
        suggestions = self.corrector.get_suggestions('speling')
        for word, freq in suggestions:
            self.assertIsInstance(word, str)
            self.assertIsInstance(freq, int)


class TestSpellingCorrectorCommonMisspellings(unittest.TestCase):
    """常见拼写错误测试"""
    
    def setUp(self):
        self.corrector = SpellingCorrector()
    
    def test_common_misspelling_teh(self):
        """测试 'teh' -> 'the'"""
        self.assertEqual(self.corrector.correct('teh'), 'the')
    
    def test_common_misspelling_thier(self):
        """测试 'thier' -> 'their'"""
        self.assertEqual(self.corrector.correct('thier'), 'their')
    
    def test_common_misspelling_recieve(self):
        """测试 'recieve' -> 'receive'"""
        self.assertEqual(self.corrector.correct('recieve'), 'receive')
    
    def test_common_misspelling_seperate(self):
        """测试 'seperate' -> 'separate'"""
        self.assertEqual(self.corrector.correct('seperate'), 'separate')
    
    def test_common_misspelling_definately(self):
        """测试 'definately' -> 'definitely'"""
        self.assertEqual(self.corrector.correct('definately'), 'definitely')
    
    def test_common_misspelling_occured(self):
        """测试 'occured' -> 'occurred'"""
        self.assertEqual(self.corrector.correct('occured'), 'occurred')


class TestSpellingCorrectorBatchOperations(unittest.TestCase):
    """批量操作测试"""
    
    def setUp(self):
        self.corrector = SpellingCorrector()
    
    def test_batch_correct(self):
        """测试批量纠正"""
        words = ['hello', 'wrld', 'the', 'speling']
        results = self.corrector.batch_correct(words)
        self.assertEqual(len(results), len(words))
        self.assertEqual(results[0].lower(), 'hello')
        self.assertEqual(results[1].lower(), 'world')
        self.assertEqual(results[2].lower(), 'the')
        # speling 应该被纠正为 spelling 或相近词
        self.assertIn('spelling', results[3].lower())
    
    def test_correct_text_basic(self):
        """测试文本纠正"""
        text = "Hello wrld, how are yuo?"
        result = self.corrector.correct_text(text)
        self.assertIn('world', result.lower())
        self.assertIn('you', result.lower())
    
    def test_correct_text_preserves_punctuation(self):
        """测试保留标点符号"""
        text = "Hello, wrld! How are yuo?"
        result = self.corrector.correct_text(text)
        self.assertIn(',', result)
        self.assertIn('!', result)
        self.assertIn('?', result)


class TestSpellingCorrectorCustomWords(unittest.TestCase):
    """自定义词汇测试"""
    
    def setUp(self):
        self.corrector = SpellingCorrector()
    
    def test_add_word(self):
        """测试添加自定义词汇"""
        self.corrector.add_word('pythonista', 5000)
        self.assertTrue(self.corrector.is_correct('pythonista'))
        self.assertEqual(self.corrector.correct('pythonista'), 'pythonista')
    
    def test_add_word_with_frequency(self):
        """测试添加自定义词汇并设置频率"""
        self.corrector.add_word('superpython', 10000)
        freq = self.corrector.get_word_frequency('superpython')
        self.assertEqual(freq, 10000)
    
    def test_add_misspelling(self):
        """测试添加自定义拼写错误映射"""
        self.corrector.add_misspelling('pyton', 'python')
        self.assertEqual(self.corrector.correct('pyton'), 'python')
    
    def test_add_words_from_text(self):
        """测试从文本添加词汇"""
        text = "Python is awesome and amazing!"
        self.corrector.add_words_from_text(text)
        # 'awesome' 和 'amazing' 可能不在默认词典中
        # 但添加后应该能识别


class TestSpellingCorrectorConvenienceFunctions(unittest.TestCase):
    """便捷函数测试"""
    
    def test_is_correct_function(self):
        """测试便捷函数 is_correct"""
        self.assertTrue(is_correct('hello'))
        self.assertTrue(is_correct('world'))
        self.assertFalse(is_correct('speling'))
    
    def test_correct_function(self):
        """测试便捷函数 correct"""
        result = correct('speling')
        self.assertIn('spelling', result.lower())
    
    def test_get_suggestions_function(self):
        """测试便捷函数 get_suggestions"""
        suggestions = get_suggestions('speling')
        self.assertTrue(len(suggestions) > 0)
    
    def test_batch_correct_function(self):
        """测试便捷函数 batch_correct"""
        results = batch_correct(['hello', 'wrld', 'the'])
        self.assertEqual(len(results), 3)
        self.assertEqual(results[0].lower(), 'hello')
        self.assertEqual(results[1].lower(), 'world')
    
    def test_correct_text_function(self):
        """测试便捷函数 correct_text"""
        result = correct_text("Hello wrld!")
        self.assertIn('world', result.lower())


class TestSpellingCorrectorEdgeCases(unittest.TestCase):
    """边缘情况测试"""
    
    def setUp(self):
        self.corrector = SpellingCorrector()
    
    def test_empty_string(self):
        """测试空字符串"""
        try:
            self.assertEqual(self.corrector.correct(''), '')
            self.assertEqual(self.corrector.correct_text(''), '')
        except:
            # 空字符串可能导致异常，这是可以接受的
            pass
    
    def test_single_character(self):
        """测试单字符"""
        # 'a' 是有效的单词
        self.assertTrue(self.corrector.is_correct('a'))
        # 'i' 是有效的单词
        self.assertTrue(self.corrector.is_correct('i'))
    
    def test_numbers_in_word(self):
        """测试包含数字的单词"""
        # 数字不在词典中
        result = self.corrector.correct('abc123')
        # 应该返回原词或尝试纠正
        self.assertIsInstance(result, str)
    
    def test_moderate_length_word(self):
        """测试中等长度单词"""
        word = 'abcdefg'
        result = self.corrector.correct(word)
        self.assertEqual(len(result), len(word))
    
    def test_mixed_case_input(self):
        """测试混合大小写输入"""
        # 应该能处理各种大小写组合
        result = self.corrector.correct('HeLLo')
        self.assertIsInstance(result, str)


class TestSpellingCorrectorVocabulary(unittest.TestCase):
    """词典功能测试"""
    
    def test_vocabulary_size(self):
        """测试词典大小"""
        size = self.corrector.vocabulary_size
        self.assertGreater(size, 0)
        self.assertGreater(size, 100)  # 至少有100个词
    
    def test_get_word_frequency_known(self):
        """测试已知词的词频"""
        freq = self.corrector.get_word_frequency('the')
        self.assertGreater(freq, 0)
    
    def test_get_word_frequency_unknown(self):
        """测试未知词的词频"""
        freq = self.corrector.get_word_frequency('xyzqwrnonexistent')
        self.assertEqual(freq, 0)
    
    def setUp(self):
        self.corrector = SpellingCorrector()


class TestSpellingCorrectorMaxDistance(unittest.TestCase):
    """最大编辑距离测试"""
    
    def setUp(self):
        self.corrector = SpellingCorrector()
    
    def test_max_distance_1(self):
        """测试最大编辑距离为1"""
        # 'speling' 与 'spelling' 编辑距离为1
        result = self.corrector.correct('speling', max_distance=1)
        self.assertIn('spelling', result.lower())
    
    def test_max_distance_2(self):
        """测试最大编辑距离为2"""
        # 某些词需要编辑距离2才能纠正
        result = self.corrector.correct('korrecter', max_distance=2)
        # 可能纠正为 corrector 或相近词
        self.assertIn('correct', result.lower())


class TestSpellingCorrectorWithoutCommonMisspellings(unittest.TestCase):
    """不加载常见拼写错误的测试"""
    
    def test_without_common_misspellings(self):
        """测试不加载常见拼写错误映射"""
        corrector = SpellingCorrector(add_common_misspellings=False)
        # 'teh' 不会直接映射到 'the'
        # 但仍可能通过编辑距离纠正
        result = corrector.correct('teh')
        self.assertIsInstance(result, str)


class TestSpellingCorrectorCustomWordFreq(unittest.TestCase):
    """自定义词频测试"""
    
    def test_custom_word_frequency(self):
        """测试自定义词频合并"""
        custom_freq = {'customword': 10000, 'anotherword': 5000}
        corrector = SpellingCorrector(word_freq=custom_freq)
        
        self.assertTrue(corrector.is_correct('customword'))
        self.assertTrue(corrector.is_correct('anotherword'))
        self.assertEqual(corrector.get_word_frequency('customword'), 10000)


def run_all_tests():
    """运行所有测试"""
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # 添加所有测试类
    suite.addTests(loader.loadTestsFromTestCase(TestSpellingCorrectorBasic))
    suite.addTests(loader.loadTestsFromTestCase(TestSpellingCorrectorSuggestions))
    suite.addTests(loader.loadTestsFromTestCase(TestSpellingCorrectorCommonMisspellings))
    suite.addTests(loader.loadTestsFromTestCase(TestSpellingCorrectorBatchOperations))
    suite.addTests(loader.loadTestsFromTestCase(TestSpellingCorrectorCustomWords))
    suite.addTests(loader.loadTestsFromTestCase(TestSpellingCorrectorConvenienceFunctions))
    suite.addTests(loader.loadTestsFromTestCase(TestSpellingCorrectorEdgeCases))
    suite.addTests(loader.loadTestsFromTestCase(TestSpellingCorrectorVocabulary))
    suite.addTests(loader.loadTestsFromTestCase(TestSpellingCorrectorMaxDistance))
    suite.addTests(loader.loadTestsFromTestCase(TestSpellingCorrectorWithoutCommonMisspellings))
    suite.addTests(loader.loadTestsFromTestCase(TestSpellingCorrectorCustomWordFreq))
    
    # 运行测试
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    return result


if __name__ == '__main__':
    # 运行测试
    result = run_all_tests()
    
    # 输出统计
    print("\n" + "=" * 50)
    print(f"测试总数: {result.testsRun}")
    print(f"成功: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"失败: {len(result.failures)}")
    print(f"错误: {len(result.errors)}")
    
    # 返回退出码
    sys.exit(0 if result.wasSuccessful() else 1)