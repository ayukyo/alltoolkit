"""
Levenshtein 工具模块单元测试
"""

import unittest
from mod import (
    levenshtein_distance,
    levenshtein_distance_optimized,
    similarity_ratio,
    normalized_levenshtein,
    damerau_levenshtein_distance,
    fuzzy_search,
    fuzzy_match_one,
    edit_sequence,
    jaro_winkler_similarity,
    hamming_distance,
    longest_common_subsequence,
    longest_common_substring,
    fuzzy_replace,
    spell_check_suggestions,
    FuzzyMatcher,
    distance,
    similarity,
    is_similar
)


class TestLevenshteinDistance(unittest.TestCase):
    """Levenshtein 距离测试"""
    
    def test_basic_distances(self):
        """测试基本距离计算"""
        self.assertEqual(levenshtein_distance("kitten", "sitting"), 3)
        self.assertEqual(levenshtein_distance("", "abc"), 3)
        self.assertEqual(levenshtein_distance("abc", ""), 3)
        self.assertEqual(levenshtein_distance("", ""), 0)
        self.assertEqual(levenshtein_distance("same", "same"), 0)
    
    def test_single_operations(self):
        """测试单个操作"""
        # 单个插入
        self.assertEqual(levenshtein_distance("abc", "abcd"), 1)
        # 单个删除
        self.assertEqual(levenshtein_distance("abcd", "abc"), 1)
        # 单个替换
        self.assertEqual(levenshtein_distance("abc", "axc"), 1)
    
    def test_unicode_strings(self):
        """测试 Unicode 字符串"""
        self.assertEqual(levenshtein_distance("你好", "你好世界"), 2)
        self.assertEqual(levenshtein_distance("中文", "英文"), 1)
    
    def test_long_strings(self):
        """测试长字符串"""
        s1 = "a" * 100
        s2 = "a" * 50 + "b" * 50
        self.assertEqual(levenshtein_distance(s1, s2), 50)


class TestLevenshteinDistanceOptimized(unittest.TestCase):
    """优化版 Levenshtein 距离测试"""
    
    def test_consistency_with_standard(self):
        """测试与标准版本结果一致"""
        test_cases = [
            ("kitten", "sitting"),
            ("hello", "hallo"),
            ("", "test"),
            ("same", "same"),
            ("abc", "xyz"),
        ]
        for s1, s2 in test_cases:
            with self.subTest(s1=s1, s2=s2):
                self.assertEqual(
                    levenshtein_distance(s1, s2),
                    levenshtein_distance_optimized(s1, s2)
                )


class TestSimilarityRatio(unittest.TestCase):
    """相似度比率测试"""
    
    def test_identical_strings(self):
        """测试完全相同的字符串"""
        self.assertEqual(similarity_ratio("hello", "hello"), 1.0)
        self.assertEqual(similarity_ratio("", ""), 1.0)
    
    def test_completely_different(self):
        """测试完全不同的字符串"""
        self.assertEqual(similarity_ratio("abc", "xyz"), 0.0)
    
    def test_partial_similarity(self):
        """测试部分相似"""
        ratio = similarity_ratio("hello", "hallo")
        self.assertAlmostEqual(ratio, 0.8, places=2)
    
    def test_case_sensitivity(self):
        """测试大小写敏感"""
        ratio = similarity_ratio("Hello", "hello")
        self.assertLess(ratio, 1.0)


class TestNormalizedLevenshtein(unittest.TestCase):
    """归一化 Levenshtein 距离测试"""
    
    def test_complement_of_similarity(self):
        """测试与相似度互补"""
        s1, s2 = "hello", "hallo"
        self.assertAlmostEqual(
            normalized_levenshtein(s1, s2),
            1 - similarity_ratio(s1, s2),
            places=10
        )


class TestDamerauLevenshtein(unittest.TestCase):
    """Damerau-Levenshtein 距离测试"""
    
    def test_with_transposition(self):
        """测试交换操作"""
        # abcd -> acbd: 交换 b 和 c，Damerau 距离为 1
        self.assertEqual(damerau_levenshtein_distance("abcd", "acbd"), 1)
        # 标准 Levenshtein 需要两次替换，Damerau 只需一次交换
        self.assertLess(
            damerau_levenshtein_distance("abcd", "acbd"),
            levenshtein_distance("abcd", "acbd")
        )
    
    def test_basic_distances(self):
        """测试基本距离"""
        self.assertEqual(damerau_levenshtein_distance("", ""), 0)
        self.assertEqual(damerau_levenshtein_distance("test", "test"), 0)


class TestFuzzySearch(unittest.TestCase):
    """模糊搜索测试"""
    
    def setUp(self):
        self.candidates = ["apple", "apply", "application", "banana", "orange"]
    
    def test_basic_search(self):
        """测试基本搜索"""
        results = fuzzy_search("aple", self.candidates, threshold=0.5)
        self.assertTrue(len(results) > 0)
        # 检查结果按相似度排序
        if len(results) > 1:
            self.assertGreaterEqual(results[0][1], results[1][1])
    
    def test_threshold(self):
        """测试阈值过滤"""
        results = fuzzy_search("xyz", self.candidates, threshold=0.5)
        self.assertEqual(len(results), 0)
    
    def test_limit(self):
        """测试结果数量限制"""
        results = fuzzy_search("ap", self.candidates, threshold=0.3, limit=2)
        self.assertLessEqual(len(results), 2)
    
    def test_exact_match(self):
        """测试精确匹配"""
        results = fuzzy_search("apple", self.candidates, threshold=0.9)
        self.assertTrue(any(r[0] == "apple" and r[1] == 1.0 for r in results))


class TestFuzzyMatchOne(unittest.TestCase):
    """单个模糊匹配测试"""
    
    def test_best_match(self):
        """测试最佳匹配"""
        candidates = ["hello", "hallo", "hell"]
        result = fuzzy_match_one("helo", candidates, threshold=0.7)
        self.assertIsNotNone(result)
        self.assertIn(result[0], candidates)
        self.assertGreaterEqual(result[1], 0.7)
    
    def test_no_match(self):
        """测试无匹配"""
        result = fuzzy_match_one("xyz", ["abc", "def"], threshold=0.8)
        self.assertIsNone(result)


class TestEditSequence(unittest.TestCase):
    """编辑序列测试"""
    
    def test_basic_sequence(self):
        """测试基本编辑序列"""
        ops = edit_sequence("kitten", "sitting")
        self.assertTrue(len(ops) > 0)
        # 验证操作类型
        for op in ops:
            self.assertIn(op[0], ['insert', 'delete', 'replace', 'match'])
    
    def test_empty_strings(self):
        """测试空字符串"""
        ops = edit_sequence("", "abc")
        self.assertTrue(all(op[0] == 'insert' for op in ops))
        
        ops = edit_sequence("abc", "")
        self.assertTrue(all(op[0] == 'delete' for op in ops))
    
    def test_identical_strings(self):
        """测试相同字符串"""
        ops = edit_sequence("same", "same")
        self.assertTrue(all(op[0] == 'match' for op in ops))


class TestJaroWinklerSimilarity(unittest.TestCase):
    """Jaro-Winkler 相似度测试"""
    
    def test_identical_strings(self):
        """测试完全相同"""
        self.assertEqual(jaro_winkler_similarity("test", "test"), 1.0)
    
    def test_empty_strings(self):
        """测试空字符串"""
        self.assertEqual(jaro_winkler_similarity("", ""), 1.0)
        self.assertEqual(jaro_winkler_similarity("test", ""), 0.0)
    
    def test_typo_detection(self):
        """测试拼写错误检测"""
        # Jaro-Winkler 对交换字母更宽容
        sim = jaro_winkler_similarity("MARTHA", "MARHTA")
        self.assertGreater(sim, 0.9)
    
    def test_prefix_bonus(self):
        """测试前缀加分"""
        # 前缀相同应该得分更高
        sim1 = jaro_winkler_similarity("crate", "trace")
        sim2 = jaro_winkler_similarity("crate", "crane")
        # crane 与 crate 前缀相同，相似度应更高
        self.assertGreater(sim2, sim1)


class TestHammingDistance(unittest.TestCase):
    """Hamming 距离测试"""
    
    def test_basic_distances(self):
        """测试基本距离"""
        self.assertEqual(hamming_distance("karolin", "kathrin"), 3)
        self.assertEqual(hamming_distance("1011101", "1001001"), 2)
    
    def test_identical_strings(self):
        """测试相同字符串"""
        self.assertEqual(hamming_distance("same", "same"), 0)
    
    def test_length_mismatch(self):
        """测试长度不匹配"""
        with self.assertRaises(ValueError):
            hamming_distance("abc", "abcd")


class TestLongestCommonSubsequence(unittest.TestCase):
    """最长公共子序列测试"""
    
    def test_basic_lcs(self):
        """测试基本 LCS"""
        # LCS 可以有多种等价结果，检查长度即可
        result = longest_common_subsequence("ABCBDAB", "BDCABA")
        self.assertEqual(len(result), 4)  # LCS 长度为 4
        self.assertIn(result, ["BCBA", "BDAB", "BCAB"])  # 都是有效的 LCS
    
    def test_no_common(self):
        """测试无公共子序列"""
        result = longest_common_subsequence("abc", "xyz")
        self.assertEqual(result, "")
    
    def test_complete_match(self):
        """测试完全匹配"""
        self.assertEqual(longest_common_subsequence("abc", "abc"), "abc")


class TestLongestCommonSubstring(unittest.TestCase):
    """最长公共子串测试"""
    
    def test_basic_substring(self):
        """测试基本子串"""
        result = longest_common_substring("ABABC", "BABCA")
        self.assertEqual(result, "BABC")
    
    def test_no_common(self):
        """测试无公共子串"""
        result = longest_common_substring("abc", "xyz")
        self.assertEqual(result, "")
    
    def test_complete_match(self):
        """测试完全匹配"""
        self.assertEqual(longest_common_substring("abc", "abc"), "abc")


class TestFuzzyReplace(unittest.TestCase):
    """模糊替换测试"""
    
    def test_basic_replace(self):
        """测试基本替换"""
        text, count = fuzzy_replace("I have an aplpe", "apple", "orange", 0.6)
        self.assertGreater(count, 0)
    
    def test_case_sensitivity(self):
        """测试大小写敏感"""
        # "Apple" 和 "apple" 相似度为 0.8（只有一个字符不同）
        # 所以会被匹配，这是正确行为
        text, count = fuzzy_replace("Apple", "apple", "orange", 0.8)
        self.assertEqual(count, 1)  # 会匹配
        
        # 测试真正不匹配的情况
        text, count = fuzzy_replace("Apple", "apple", "orange", 0.99)
        self.assertEqual(count, 0)  # 阈值太高，不匹配
    
    def test_empty_strings(self):
        """测试空字符串"""
        text, count = fuzzy_replace("", "apple", "orange")
        self.assertEqual(count, 0)
        
        text, count = fuzzy_replace("some text", "", "orange")
        self.assertEqual(count, 0)


class TestSpellCheckSuggestions(unittest.TestCase):
    """拼写检查建议测试"""
    
    def setUp(self):
        self.dictionary = ["apple", "banana", "orange", "grape", "application"]
    
    def test_typo_correction(self):
        """测试拼写纠错"""
        suggestions = spell_check_suggestions("aple", self.dictionary)
        self.assertTrue(len(suggestions) > 0)
        # apple 应该是首选
        self.assertEqual(suggestions[0][0], "apple")
    
    def test_threshold(self):
        """测试阈值"""
        suggestions = spell_check_suggestions("xyz", self.dictionary, threshold=0.8)
        self.assertEqual(len(suggestions), 0)
    
    def test_limit(self):
        """测试建议数量限制"""
        suggestions = spell_check_suggestions("aple", self.dictionary, max_suggestions=2)
        self.assertLessEqual(len(suggestions), 2)


class TestFuzzyMatcher(unittest.TestCase):
    """FuzzyMatcher 类测试"""
    
    def setUp(self):
        self.matcher = FuzzyMatcher(["apple", "banana", "orange", "grape"])
    
    def test_find_best(self):
        """测试查找最佳匹配"""
        result = self.matcher.find_best("aple", threshold=0.7)
        self.assertIsNotNone(result)
        self.assertEqual(result[0], "apple")
    
    def test_find_all(self):
        """测试查找所有匹配"""
        results = self.matcher.find_all("ap", threshold=0.3)
        self.assertTrue(len(results) > 0)
    
    def test_cache(self):
        """测试缓存功能"""
        # 第一次查询
        result1 = self.matcher.find_best("aple")
        # 第二次应该从缓存读取
        result2 = self.matcher.find_best("aple")
        self.assertEqual(result1, result2)
        
        # 清除缓存后
        self.matcher.clear_cache()
        result3 = self.matcher.find_best("aple")
        self.assertEqual(result1, result3)
    
    def test_add_remove_candidate(self):
        """测试添加和移除候选"""
        self.matcher.add_candidate("apricot")
        result = self.matcher.find_best("apricot", threshold=0.9)
        self.assertIsNotNone(result)
        
        self.assertTrue(self.matcher.remove_candidate("apricot"))
        self.assertFalse(self.matcher.remove_candidate("nonexistent"))
    
    def test_custom_similarity_func(self):
        """测试自定义相似度函数"""
        custom_matcher = FuzzyMatcher(
            ["abc", "def"],
            similarity_func=lambda a, b: 1.0 if a == b else 0.0
        )
        result = custom_matcher.find_best("abc", threshold=0.5)
        self.assertIsNotNone(result)
        self.assertEqual(result[0], "abc")


class TestConvenienceFunctions(unittest.TestCase):
    """便捷函数测试"""
    
    def test_distance_alias(self):
        """测试 distance 别名"""
        self.assertEqual(distance("abc", "abc"), 0)
        self.assertEqual(distance("abc", "abcd"), 1)
    
    def test_similarity_alias(self):
        """测试 similarity 别名"""
        self.assertEqual(similarity("same", "same"), 1.0)
    
    def test_is_similar(self):
        """测试 is_similar 函数"""
        self.assertTrue(is_similar("hello", "hallo", threshold=0.7))
        self.assertFalse(is_similar("hello", "world", threshold=0.7))


class TestEdgeCases(unittest.TestCase):
    """边界情况测试"""
    
    def test_large_strings(self):
        """测试大字符串"""
        s1 = "a" * 1000
        s2 = "a" * 500 + "b" * 500
        distance = levenshtein_distance(s1, s2)
        self.assertEqual(distance, 500)
    
    def test_special_characters(self):
        """测试特殊字符"""
        self.assertEqual(levenshtein_distance("!@#", "!@#$"), 1)
        self.assertEqual(levenshtein_distance("\n\t", "\n"), 1)
    
    def test_unicode_emoji(self):
        """测试 Unicode 和 Emoji"""
        self.assertEqual(levenshtein_distance("😀😁", "😀"), 1)
        self.assertEqual(similarity_ratio("中文测试", "中文"), 0.5)


if __name__ == "__main__":
    unittest.main(verbosity=2)