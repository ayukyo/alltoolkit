"""
edit_distance_utils 单元测试
"""

import unittest
import sys
import os

# 添加父目录到路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from mod import (
    levenshtein_distance,
    damerau_levenshtein_distance,
    hamming_distance,
    jaro_similarity,
    jaro_winkler_similarity,
    lcs_length,
    lcs_string,
    normalized_levenshtein,
    similarity_ratio,
    fuzzy_match,
    spell_suggest,
    edit_operations,
    diff_ratio,
    soundex_distance,
    ngram_similarity,
    EditDistanceCalculator,
)


class TestLevenshteinDistance(unittest.TestCase):
    """Levenshtein 距离测试"""
    
    def test_basic_cases(self):
        self.assertEqual(levenshtein_distance("", ""), 0)
        self.assertEqual(levenshtein_distance("a", ""), 1)
        self.assertEqual(levenshtein_distance("", "a"), 1)
        self.assertEqual(levenshtein_distance("a", "a"), 0)
    
    def test_substitution(self):
        self.assertEqual(levenshtein_distance("a", "b"), 1)
        self.assertEqual(levenshtein_distance("kitten", "sitten"), 1)
    
    def test_insertion(self):
        self.assertEqual(levenshtein_distance("a", "ab"), 1)
        self.assertEqual(levenshtein_distance("", "abc"), 3)
    
    def test_deletion(self):
        self.assertEqual(levenshtein_distance("ab", "a"), 1)
        self.assertEqual(levenshtein_distance("abc", ""), 3)
    
    def test_complex_cases(self):
        self.assertEqual(levenshtein_distance("kitten", "sitting"), 3)
        self.assertEqual(levenshtein_distance("saturday", "sunday"), 3)
        self.assertEqual(levenshtein_distance("algorithm", "altruistic"), 6)
    
    def test_same_strings(self):
        self.assertEqual(levenshtein_distance("hello", "hello"), 0)
        self.assertEqual(levenshtein_distance("世界", "世界"), 0)
    
    def test_unicode(self):
        self.assertEqual(levenshtein_distance("你好", "你好吗"), 1)
        self.assertEqual(levenshtein_distance("日本語", "日本語"), 0)


class TestDamerauLevenshteinDistance(unittest.TestCase):
    """Damerau-Levenshtein 距离测试"""
    
    def test_basic_cases(self):
        self.assertEqual(damerau_levenshtein_distance("", ""), 0)
        self.assertEqual(damerau_levenshtein_distance("a", "b"), 1)
    
    def test_transposition(self):
        # 相邻字符交换只需要 1 次操作
        self.assertEqual(damerau_levenshtein_distance("ab", "ba"), 1)
        self.assertEqual(damerau_levenshtein_distance("abc", "acb"), 1)
        # ca -> abc 需要插入 'b' 和调整位置，但标准 Damerau-Levenshtein 是 3
        self.assertEqual(damerau_levenshtein_distance("ca", "abc"), 3)
    
    def test_vs_levenshtein(self):
        # Damerau-Levenshtein 距离应该 <= Levenshtein 距离
        self.assertLessEqual(
            damerau_levenshtein_distance("ab", "ba"),
            levenshtein_distance("ab", "ba")
        )


class TestHammingDistance(unittest.TestCase):
    """Hamming 距离测试"""
    
    def test_equal_strings(self):
        self.assertEqual(hamming_distance("", ""), 0)
        self.assertEqual(hamming_distance("hello", "hello"), 0)
    
    def test_different_strings(self):
        self.assertEqual(hamming_distance("karolin", "kathrin"), 3)
        self.assertEqual(hamming_distance("1011101", "1001001"), 2)
        self.assertEqual(hamming_distance("2173896", "2233796"), 3)
    
    def test_unequal_length_raises(self):
        with self.assertRaises(ValueError):
            hamming_distance("abc", "abcd")


class TestJaroSimilarity(unittest.TestCase):
    """Jaro 相似度测试"""
    
    def test_identical_strings(self):
        self.assertEqual(jaro_similarity("", ""), 1.0)
        self.assertEqual(jaro_similarity("hello", "hello"), 1.0)
    
    def test_no_similarity(self):
        self.assertEqual(jaro_similarity("abc", "xyz"), 0.0)
    
    def test_partial_similarity(self):
        # MARTHA vs MARHTA
        result = jaro_similarity("MARTHA", "MARHTA")
        self.assertAlmostEqual(result, 0.944, places=2)
    
    def test_empty_strings(self):
        self.assertEqual(jaro_similarity("", "abc"), 0.0)
        self.assertEqual(jaro_similarity("abc", ""), 0.0)


class TestJaroWinklerSimilarity(unittest.TestCase):
    """Jaro-Winkler 相似度测试"""
    
    def test_identical_strings(self):
        self.assertEqual(jaro_winkler_similarity("", ""), 1.0)
        self.assertEqual(jaro_winkler_similarity("test", "test"), 1.0)
    
    def test_prefix_bonus(self):
        # Jaro-Winkler 对相同前缀给予额外分数
        jw = jaro_winkler_similarity("MARTHA", "MARHTA")
        jaro_sim = jaro_similarity("MARTHA", "MARHTA")
        self.assertGreater(jw, jaro_sim)
    
    def test_vs_jaro(self):
        # Jaro-Winkler 应该 >= Jaro
        pairs = [
            ("hello", "hallo"),
            ("test", "best"),
            ("apple", "apply"),
        ]
        for s1, s2 in pairs:
            self.assertGreaterEqual(
                jaro_winkler_similarity(s1, s2),
                jaro_similarity(s1, s2)
            )


class TestLCS(unittest.TestCase):
    """最长公共子序列测试"""
    
    def test_lcs_length(self):
        self.assertEqual(lcs_length("", ""), 0)
        self.assertEqual(lcs_length("abc", ""), 0)
        self.assertEqual(lcs_length("", "abc"), 0)
        self.assertEqual(lcs_length("abc", "abc"), 3)
        self.assertEqual(lcs_length("ABCDGH", "AEDFHR"), 3)  # "ADH"
        self.assertEqual(lcs_length("AGGTAB", "GXTXAYB"), 4)  # "GTAB"
    
    def test_lcs_string(self):
        self.assertEqual(lcs_string("", ""), "")
        self.assertEqual(lcs_string("abc", "abc"), "abc")
        
        result = lcs_string("ABCDGH", "AEDFHR")
        self.assertEqual(len(result), 3)
        self.assertIn(result, ["ADH", "ADH"])
        
        result = lcs_string("AGGTAB", "GXTXAYB")
        self.assertEqual(len(result), 4)


class TestNormalizedLevenshtein(unittest.TestCase):
    """归一化 Levenshtein 相似度测试"""
    
    def test_identical_strings(self):
        self.assertEqual(normalized_levenshtein("", ""), 1.0)
        self.assertEqual(normalized_levenshtein("hello", "hello"), 1.0)
    
    def test_different_strings(self):
        result = normalized_levenshtein("hello", "hallo")
        self.assertAlmostEqual(result, 0.8, places=1)
    
    def test_range(self):
        # 结果应在 [0, 1] 范围内
        test_pairs = [
            ("hello", "world"),
            ("test", "testing"),
            ("", "something"),
        ]
        for s1, s2 in test_pairs:
            result = normalized_levenshtein(s1, s2)
            self.assertGreaterEqual(result, 0.0)
            self.assertLessEqual(result, 1.0)


class TestSimilarityRatio(unittest.TestCase):
    """相似度计算测试"""
    
    def test_different_methods(self):
        methods = ['jaro_winkler', 'jaro', 'levenshtein', 'lcs']
        
        for method in methods:
            result = similarity_ratio("hello", "hallo", method=method)
            self.assertGreaterEqual(result, 0.0)
            self.assertLessEqual(result, 1.0)
    
    def test_invalid_method(self):
        with self.assertRaises(ValueError):
            similarity_ratio("a", "b", method='invalid')


class TestFuzzyMatch(unittest.TestCase):
    """模糊匹配测试"""
    
    def test_basic_matching(self):
        candidates = ["hello", "help", "held", "halo", "hero"]
        results = fuzzy_match("helo", candidates, threshold=0.6)
        
        self.assertGreater(len(results), 0)
        # 结果应按相似度降序排列
        for i in range(len(results) - 1):
            self.assertGreaterEqual(results[i][1], results[i + 1][1])
    
    def test_threshold(self):
        candidates = ["apple", "banana", "cherry"]
        results = fuzzy_match("zzz", candidates, threshold=0.9)
        self.assertEqual(len(results), 0)
    
    def test_limit(self):
        candidates = ["test1", "test2", "test3", "test4", "test5"]
        results = fuzzy_match("test", candidates, threshold=0.0, limit=2)
        self.assertLessEqual(len(results), 2)


class TestSpellSuggest(unittest.TestCase):
    """拼写建议测试"""
    
    def test_basic_suggestion(self):
        dictionary = ["apple", "apply", "ape", "appeal", "app"]
        results = spell_suggest("appel", dictionary, max_distance=2)
        
        self.assertGreater(len(results), 0)
        # 第一个结果应该是编辑距离最小的（升序排列）
        if len(results) > 0:
            min_dist = results[0][1]
            for word, dist in results:
                self.assertLessEqual(min_dist, dist)
    
    def test_exact_match(self):
        dictionary = ["hello", "world"]
        results = spell_suggest("hello", dictionary, max_distance=0)
        
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0], ("hello", 0))
    
    def test_max_distance(self):
        dictionary = ["apple", "banana", "cherry"]
        results = spell_suggest("xyz", dictionary, max_distance=1)
        self.assertEqual(len(results), 0)
    
    def test_different_methods(self):
        dictionary = ["apple", "apply"]
        
        results1 = spell_suggest("appel", dictionary, method='levenshtein')
        results2 = spell_suggest("appel", dictionary, method='damerau_levenshtein')
        
        self.assertGreaterEqual(len(results1), 0)
        self.assertGreaterEqual(len(results2), 0)


class TestEditOperations(unittest.TestCase):
    """编辑操作序列测试"""
    
    def test_identical_strings(self):
        ops = edit_operations("", "")
        self.assertEqual(len(ops), 0)
        
        ops = edit_operations("abc", "abc")
        self.assertEqual(len([op for op in ops if op[0] == 'keep']), 3)
    
    def test_insertion(self):
        ops = edit_operations("", "abc")
        insert_ops = [op for op in ops if op[0] == 'insert']
        self.assertEqual(len(insert_ops), 3)
    
    def test_deletion(self):
        ops = edit_operations("abc", "")
        delete_ops = [op for op in ops if op[0] == 'delete']
        self.assertEqual(len(delete_ops), 3)
    
    def test_substitution(self):
        ops = edit_operations("abc", "adc")
        replace_ops = [op for op in ops if op[0] == 'replace']
        self.assertEqual(len(replace_ops), 1)
        self.assertEqual(replace_ops[0][1], 1)  # 位置 1


class TestDiffRatio(unittest.TestCase):
    """差异比率测试"""
    
    def test_identical_strings(self):
        self.assertEqual(diff_ratio("", ""), 1.0)
        self.assertEqual(diff_ratio("hello", "hello"), 1.0)
    
    def test_different_strings(self):
        result = diff_ratio("hello world", "hello earth")
        self.assertGreater(result, 0.0)
        self.assertLess(result, 1.0)
    
    def test_empty_strings(self):
        self.assertEqual(diff_ratio("", "abc"), 0.0)
        self.assertEqual(diff_ratio("abc", ""), 0.0)


class TestSoundexDistance(unittest.TestCase):
    """Soundex 语音距离测试"""
    
    def test_similar_sounding(self):
        # 相似发音的单词
        self.assertEqual(soundex_distance("Robert", "Rupert"), 0)
        self.assertEqual(soundex_distance("Smith", "Smythe"), 0)
    
    def test_different_sounding(self):
        self.assertEqual(soundex_distance("Robert", "Albert"), 1)
    
    def test_empty_strings(self):
        # 空字符串处理
        result = soundex_distance("", "test")
        self.assertIn(result, [0, 1])


class TestNgramSimilarity(unittest.TestCase):
    """N-gram 相似度测试"""
    
    def test_identical_strings(self):
        self.assertEqual(ngram_similarity("", "", n=2), 1.0)
        self.assertEqual(ngram_similarity("hello", "hello", n=2), 1.0)
    
    def test_different_strings(self):
        result = ngram_similarity("hello", "hallo", n=2)
        self.assertGreater(result, 0.0)
        self.assertLess(result, 1.0)
    
    def test_different_n_values(self):
        for n in [1, 2, 3, 4]:
            result = ngram_similarity("test", "best", n=n)
            self.assertGreaterEqual(result, 0.0)
            self.assertLessEqual(result, 1.0)


class TestEditDistanceCalculator(unittest.TestCase):
    """编辑距离计算器类测试"""
    
    def setUp(self):
        self.calc = EditDistanceCalculator()
    
    def test_similarity(self):
        result = self.calc.similarity("hello", "hallo")
        self.assertGreaterEqual(result, 0.0)
        self.assertLessEqual(result, 1.0)
    
    def test_caching(self):
        # 第一次计算
        result1 = self.calc.similarity("test", "best")
        
        # 第二次计算（应该从缓存获取）
        result2 = self.calc.similarity("test", "best")
        
        self.assertEqual(result1, result2)
        self.assertGreater(len(self.calc._cache), 0)
    
    def test_different_methods(self):
        for method in ['jaro_winkler', 'jaro', 'levenshtein', 'lcs']:
            result = self.calc.similarity("abc", "abd", method=method)
            self.assertGreaterEqual(result, 0.0)
    
    def test_batch_similarity(self):
        candidates = ["apple", "apply", "ape", "appeal"]
        results = self.calc.batch_similarity("appel", candidates)
        
        self.assertEqual(len(results), len(candidates))
        # 结果应按相似度降序排列
        for i in range(len(results) - 1):
            self.assertGreaterEqual(results[i][1], results[i + 1][1])
    
    def test_clear_cache(self):
        self.calc.similarity("a", "b")
        self.assertGreater(len(self.calc._cache), 0)
        
        self.calc.clear_cache()
        self.assertEqual(len(self.calc._cache), 0)


class TestEdgeCases(unittest.TestCase):
    """边界情况测试"""
    
    def test_unicode_strings(self):
        # 中文字符串
        self.assertEqual(levenshtein_distance("你好", "你好"), 0)
        self.assertEqual(levenshtein_distance("你好", "你好吗"), 1)
        
        # 表情符号
        self.assertEqual(levenshtein_distance("🎉🎊", "🎉🎊"), 0)
        self.assertEqual(levenshtein_distance("🎉", "🎊"), 1)
    
    def test_long_strings(self):
        # 长字符串性能测试
        s1 = "a" * 1000
        s2 = "b" * 1000 + "a" * 10
        
        # 应该能在合理时间内完成
        result = levenshtein_distance(s1, s2)
        self.assertGreater(result, 0)
    
    def test_special_characters(self):
        # 特殊字符
        s1 = "a\tb\nc"
        s2 = "a\tb\nc"
        self.assertEqual(levenshtein_distance(s1, s2), 0)
        # 转义字符串 vs 实际字符字符串（长度不同）
        # "a\\nb" 是 4 字符，"a\nb" 是 3 字符
        self.assertEqual(levenshtein_distance("a\\nb", "a\nb"), 2)


if __name__ == '__main__':
    unittest.main(verbosity=2)