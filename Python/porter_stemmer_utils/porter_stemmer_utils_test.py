"""
Porter Stemmer 工具测试

测试 Porter Stemmer 算法的正确性和各种边界情况。
"""

import unittest
import sys
import os

# 添加模块路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from mod import PorterStemmer, stem, stem_words, stem_text


class TestPorterStemmer(unittest.TestCase):
    """PorterStemmer 类测试"""
    
    def setUp(self):
        """设置测试环境"""
        self.stemmer = PorterStemmer()
    
    def test_basic_stemming(self):
        """测试基本词干提取"""
        test_cases = [
            # (input, expected_stem)
            ('running', 'run'),
            ('runs', 'run'),
            ('runner', 'runner'),  # 注意：Porter 算法的特定输出
            ('happiness', 'happi'),
            ('happy', 'happi'),
            ('cats', 'cat'),
            ('boxes', 'box'),
            ('easily', 'easili'),
            ('agreed', 'agre'),
            ('plastered', 'plaster'),
            ('motoring', 'motor'),
            ('sing', 'sing'),
            ('conflated', 'conflat'),
            ('troubled', 'troubl'),
            ('sized', 'size'),
            ('hopping', 'hop'),
            ('tanned', 'tan'),
            ('falling', 'fall'),
            ('hissing', 'hiss'),
            ('fizzed', 'fizz'),
            ('failing', 'fail'),
            ('filing', 'file'),
        ]
        
        for word, expected in test_cases:
            with self.subTest(word=word):
                result = self.stemmer.stem(word)
                self.assertEqual(result, expected,
                    f"stem('{word}') = '{result}', expected '{expected}'")
    
    def test_plurals(self):
        """测试复数形式处理"""
        test_cases = [
            ('caresses', 'caress'),
            ('ponies', 'poni'),
            ('ties', 'ti'),
            ('caress', 'caress'),
            ('cats', 'cat'),
            ('dogs', 'dog'),
            ('churches', 'church'),
            ('classes', 'class'),
        ]
        
        for word, expected in test_cases:
            with self.subTest(word=word):
                result = self.stemmer.stem(word)
                self.assertEqual(result, expected)
    
    def test_past_tense_and_ing(self):
        """测试过去时和进行时处理"""
        test_cases = [
            ('agreed', 'agre'),
            ('plastered', 'plaster'),
            ('bled', 'bled'),
            ('motoring', 'motor'),
            ('sing', 'sing'),
            ('conflated', 'conflat'),
            ('troubled', 'troubl'),
            ('sized', 'size'),
            ('hopping', 'hop'),
            ('tanned', 'tan'),
            ('falling', 'fall'),
            ('hissing', 'hiss'),
            ('fizzed', 'fizz'),
            ('failing', 'fail'),
            ('filing', 'file'),
        ]
        
        for word, expected in test_cases:
            with self.subTest(word=word):
                result = self.stemmer.stem(word)
                self.assertEqual(result, expected)
    
    def test_y_to_i(self):
        """测试 y 到 i 的转换"""
        test_cases = [
            ('happy', 'happi'),
            ('sky', 'sky'),  # 无元音词干
            # 注意: relaying/traying 经过 -ing 处理后词干不含元音时会有不同行为
        ]
        
        for word, expected in test_cases:
            with self.subTest(word=word):
                result = self.stemmer.stem(word)
                self.assertEqual(result, expected)
    
    def test_double_consonant(self):
        """测试双辅音处理"""
        test_cases = [
            ('hopping', 'hop'),  # pp -> p
            ('tanned', 'tan'),    # nn -> n
            ('falling', 'fall'),  # ll 保持不变
            ('hissing', 'hiss'),  # ss 保持不变
            ('fizzed', 'fizz'),   # zz 保持不变
        ]
        
        for word, expected in test_cases:
            with self.subTest(word=word):
                result = self.stemmer.stem(word)
                self.assertEqual(result, expected)
    
    def test_step2_suffixes(self):
        """测试步骤 2 的各种后缀"""
        test_cases = [
            ('relational', 'relat'),
            ('conditional', 'condit'),
            ('rational', 'ration'),
            ('valenci', 'valenc'),
            ('hesitanci', 'hesit'),
            ('digitizer', 'digit'),
            ('conformabli', 'conform'),
            ('radicalli', 'radic'),
            ('differentli', 'differ'),
            ('vileli', 'vile'),
            ('analogousli', 'analog'),
            ('vietnamization', 'vietnam'),
            ('predication', 'predic'),
            ('operator', 'oper'),
            ('feudalism', 'feudal'),
            ('decisiveness', 'decis'),
            ('hopefulness', 'hope'),
            ('callousness', 'callous'),
            ('formaliti', 'formal'),
            ('sensitiviti', 'sensit'),
            ('sensibiliti', 'sensibl'),
        ]
        
        for word, expected in test_cases:
            with self.subTest(word=word):
                result = self.stemmer.stem(word)
                self.assertEqual(result, expected)
    
    def test_step3_suffixes(self):
        """测试步骤 3 的后缀"""
        test_cases = [
            ('triplicate', 'triplic'),
            ('formative', 'form'),
            ('formalize', 'formal'),
            ('electriciti', 'electr'),
            ('electrical', 'electr'),
            ('hopeful', 'hope'),
            ('goodness', 'good'),
        ]
        
        for word, expected in test_cases:
            with self.subTest(word=word):
                result = self.stemmer.stem(word)
                self.assertEqual(result, expected)
    
    def test_step4_suffixes(self):
        """测试步骤 4 的后缀"""
        test_cases = [
            ('revival', 'reviv'),
            ('allowance', 'allow'),
            ('inference', 'infer'),
            ('airliner', 'airlin'),
            ('gyroscopic', 'gyroscop'),
            ('adjustable', 'adjust'),
            ('defensible', 'defens'),
            ('irritant', 'irrit'),
            ('replacement', 'replac'),
            ('adjustment', 'adjust'),
            ('dependent', 'depend'),
            ('adoption', 'adopt'),
            ('homologou', 'homolog'),
            ('communism', 'commun'),
            ('activate', 'activ'),
            ('angulariti', 'angular'),
            ('homologous', 'homolog'),
            ('effective', 'effect'),
            ('bowdlerize', 'bowdler'),
        ]
        
        for word, expected in test_cases:
            with self.subTest(word=word):
                result = self.stemmer.stem(word)
                self.assertEqual(result, expected)
    
    def test_step5(self):
        """测试步骤 5"""
        test_cases = [
            ('probate', 'probat'),
            ('rate', 'rate'),
            ('cease', 'ceas'),
            ('controll', 'control'),
            ('roll', 'roll'),
        ]
        
        for word, expected in test_cases:
            with self.subTest(word=word):
                result = self.stemmer.stem(word)
                self.assertEqual(result, expected)
    
    def test_short_words(self):
        """测试短单词"""
        test_cases = [
            ('a', 'a'),
            ('an', 'an'),
            ('to', 'to'),
            ('in', 'in'),
            ('is', 'is'),
            ('it', 'it'),
            ('be', 'be'),
        ]
        
        for word, expected in test_cases:
            with self.subTest(word=word):
                result = self.stemmer.stem(word)
                self.assertEqual(result, expected)
    
    def test_case_insensitive(self):
        """测试大小写处理"""
        # Porter 算法应该将输入转换为小写
        test_cases = [
            ('Running', 'run'),
            ('RUNNING', 'run'),
            ('RuNnInG', 'run'),
            ('Happiness', 'happi'),
            ('HAPPINESS', 'happi'),
        ]
        
        for word, expected in test_cases:
            with self.subTest(word=word):
                result = self.stemmer.stem(word)
                self.assertEqual(result, expected)
    
    def test_whitespace_handling(self):
        """测试空白字符处理"""
        self.assertEqual(self.stemmer.stem('  running  '), 'run')
        self.assertEqual(self.stemmer.stem('\thappy\n'), 'happi')
    
    def test_stem_words_batch(self):
        """测试批量词干提取"""
        words = ['running', 'jumps', 'happiness', 'cats', 'boxes']
        result = self.stemmer.stem_words(words)
        
        self.assertEqual(len(result), len(words))
        self.assertEqual(result[0], 'run')
        self.assertEqual(result[1], 'jump')
        self.assertEqual(result[2], 'happi')
        self.assertEqual(result[3], 'cat')
        self.assertEqual(result[4], 'box')
    
    def test_stem_text(self):
        """测试文本词干提取"""
        text = "The cats are running and jumping"
        result = self.stemmer.stem_text(text)
        
        self.assertIn('cat', result)
        self.assertIn('run', result)
        self.assertIn('jump', result)
    
    def test_stem_text_with_punctuation(self):
        """测试带标点的文本词干提取"""
        text = "Hello, world! How are you doing?"
        result = self.stemmer.stem_text(text)
        
        self.assertIn(',', result)
        self.assertIn('!', result)
        self.assertIn('?', result)
    
    def test_get_unique_stems(self):
        """测试获取唯一词干集合"""
        words = ['running', 'runs', 'ran', 'jumping', 'jumps', 'jumped']
        stems = self.stemmer.get_unique_stems(words)
        
        self.assertIsInstance(stems, set)
        # ran 的词干可能不是 run，取决于具体实现
    
    def test_group_by_stem(self):
        """测试按词干分组"""
        words = ['running', 'runs', 'jumping', 'jumps', 'happiness', 'happy']
        groups = self.stemmer.group_by_stem(words)
        
        self.assertIsInstance(groups, dict)
        # happiness 和 happy 应该在同一组
        happi_group = groups.get('happi', [])
        self.assertIn('happiness', happi_group)
        self.assertIn('happy', happi_group)
    
    def test_empty_input(self):
        """测试空输入"""
        self.assertEqual(self.stemmer.stem(''), '')
        self.assertEqual(self.stemmer.stem_words([]), [])
        self.assertEqual(self.stemmer.stem_text(''), '')
    
    def test_convenience_functions(self):
        """测试便捷函数"""
        self.assertEqual(stem('running'), 'run')
        self.assertEqual(stem_words(['cats', 'dogs']), ['cat', 'dog'])
        
        text_result = stem_text('The happy cats')
        self.assertIn('happi', text_result)
        self.assertIn('cat', text_result)
    
    def test_measure_calculation(self):
        """测试 measure (m) 计算"""
        # 测试内部方法
        self.assertEqual(self.stemmer._measure('tr'), 0)
        self.assertEqual(self.stemmer._measure('ee'), 0)
        self.assertEqual(self.stemmer._measure('tree'), 0)
        self.assertEqual(self.stemmer._measure('y'), 0)
        self.assertEqual(self.stemmer._measure('by'), 0)
        self.assertEqual(self.stemmer._measure('trouble'), 1)
        self.assertEqual(self.stemmer._measure('oats'), 1)
        self.assertEqual(self.stemmer._measure('trees'), 1)
        self.assertEqual(self.stemmer._measure('ivy'), 1)
        # 注意：troubles 的实际 measure 是 2（trou-bles）
        self.assertEqual(self.stemmer._measure('private'), 2)
        self.assertEqual(self.stemmer._measure('oaten'), 2)
        self.assertEqual(self.stemmer._measure('orrery'), 2)
    
    def test_has_vowel(self):
        """测试元音检测"""
        self.assertTrue(self.stemmer._has_vowel('apple'))
        self.assertTrue(self.stemmer._has_vowel('tree'))
        self.assertTrue(self.stemmer._has_vowel('happy'))  # y 是元音
        # 注意：在 Porter 算法中，y 在特定位置是元音
        # rhythm 中的 y 被视为元音
        self.assertFalse(self.stemmer._has_vowel('bcdfg'))  # 无元音
        self.assertFalse(self.stemmer._has_vowel('rhythm') == False)  # rhythm 中 y 是元音
    
    def test_ends_double_consonant(self):
        """测试双辅音结尾检测"""
        # 注意：这个函数检查单词的最后两个字符是否相同且为辅音
        self.assertFalse(self.stemmer._ends_double_consonant('running'))  # 结尾是 ng
        self.assertFalse(self.stemmer._ends_double_consonant('hopped'))  # 结尾是 ed
        self.assertFalse(self.stemmer._ends_double_consonant('happy'))  # 结尾是 py
        self.assertTrue(self.stemmer._ends_double_consonant('hiss'))  # 结尾是 ss
        self.assertTrue(self.stemmer._ends_double_consonant('fizz'))  # 结尾是 zz
        self.assertTrue(self.stemmer._ends_double_consonant('hopp'))  # 结尾是 pp
        self.assertTrue(self.stemmer._ends_double_consonant('fitt'))  # 结尾是 tt
        self.assertFalse(self.stemmer._ends_double_consonant('single'))
    
    def test_ends_cvc(self):
        """测试 CVC 结尾检测"""
        self.assertTrue(self.stemmer._ends_cvc('hop'))
        self.assertTrue(self.stemmer._ends_cvc('top'))
        self.assertFalse(self.stemmer._ends_cvc('how'))
        self.assertFalse(self.stemmer._ends_cvc('tray'))
        self.assertFalse(self.stemmer._ends_cvc('box'))
        self.assertFalse(self.stemmer._ends_cvc('ab'))
    
    def test_real_world_words(self):
        """测试真实世界单词"""
        # 常见单词测试
        test_cases = [
            ('information', 'inform'),
            ('retrieval', 'retriev'),
            ('computer', 'comput'),
            ('programming', 'program'),
            ('algorithm', 'algorithm'),
            ('database', 'databas'),
            ('software', 'softwar'),
            ('hardware', 'hardwar'),
            ('network', 'network'),
            ('security', 'secur'),
            ('application', 'applic'),
            ('development', 'develop'),
            ('management', 'manag'),
            ('technology', 'technologi'),  # 实际 Porter 输出
            ('engineering', 'engin'),
            ('science', 'scienc'),
            ('research', 'research'),
            ('analysis', 'analysi'),
            ('processing', 'process'),
            ('communication', 'commun'),
        ]
        
        for word, expected in test_cases:
            with self.subTest(word=word):
                result = self.stemmer.stem(word)
                self.assertEqual(result, expected,
                    f"stem('{word}') = '{result}', expected '{expected}'")


class TestPorterStemmerEdgeCases(unittest.TestCase):
    """边缘情况测试"""
    
    def setUp(self):
        self.stemmer = PorterStemmer()
    
    def test_non_alpha_characters(self):
        """测试非字母字符"""
        # 数字应该被保留（但词干提取主要针对字母）
        self.assertEqual(self.stemmer.stem('123'), '123')
        self.assertEqual(self.stemmer.stem('abc123'), 'abc123')
    
    def test_unicode_handling(self):
        """测试 Unicode 字符处理"""
        # Porter 算法针对英语设计
        # 中文、日文等应该被保留（虽然没有词干）
        self.assertEqual(self.stemmer.stem('测试'), '测试')
        self.assertEqual(self.stemmer.stem('こんにちは'), 'こんにちは')
    
    def test_mixed_case_with_whitespace(self):
        """测试混合大小写和空白"""
        self.assertEqual(self.stemmer.stem('  RUNNING  '), 'run')
        self.assertEqual(self.stemmer.stem('\nJumping\t'), 'jump')
    
    def test_very_long_word(self):
        """测试超长单词"""
        long_word = 'supercalifragilisticexpialidocious'
        result = self.stemmer.stem(long_word)
        # 应该返回一个有效结果而不崩溃
        self.assertIsInstance(result, str)
        self.assertGreater(len(result), 0)
    
    def test_repeated_calls_consistency(self):
        """测试重复调用的一致性"""
        word = 'running'
        result1 = self.stemmer.stem(word)
        result2 = self.stemmer.stem(word)
        result3 = self.stemmer.stem(word)
        
        self.assertEqual(result1, result2)
        self.assertEqual(result2, result3)


if __name__ == '__main__':
    unittest.main(verbosity=2)