#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Levenshtein Utils 测试模块
=========================
全面测试编辑距离工具的所有功能。

测试覆盖:
- 基础 Levenshtein 距离计算
- 空间优化版距离计算
- 阈值优化距离计算
- 相似度计算（比率、Jaro、Jaro-Winkler）
- 编辑操作序列回溯
- Damerau-Levenshtein 距离
- 最长公共子序列（LCS）
- 模糊匹配搜索
- 批量计算
- 工具函数
- 边界值处理

作者: AllToolkit
日期: 2026-05-20
"""

import unittest
from typing import List
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from mod import (
    levenshtein_distance,
    levenshtein_distance_optimized,
    levenshtein_distance_threshold,
    similarity_ratio,
    similarity_result,
    SimilarityResult,
    jaro_similarity,
    jaro_winkler_similarity,
    levenshtein_operations,
    apply_operations,
    EditOperation,
    EditStep,
    damerau_levenshtein_distance,
    longest_common_subsequence,
    lcs_length,
    find_similar,
    find_nearest,
    fuzzy_search,
    batch_similarity,
    batch_distance,
    similarity_matrix,
    normalized_levenshtein,
    hamming_distance,
    is_one_edit_away,
    spell_check_suggestions,
    align_strings
)


class TestBasicLevenshtein(unittest.TestCase):
    """测试基础 Levenshtein 距离计算"""
    
    def test_identical_strings(self):
        """相同字符串距离为 0"""
        self.assertEqual(levenshtein_distance("hello", "hello"), 0)
        self.assertEqual(levenshtein_distance("", ""), 0)
        self.assertEqual(levenshtein_distance("a", "a"), 0)
    
    def test_empty_strings(self):
        """空字符串测试"""
        self.assertEqual(levenshtein_distance("", "abc"), 3)
        self.assertEqual(levenshtein_distance("abc", ""), 3)
        self.assertEqual(levenshtein_distance("", ""), 0)
    
    def test_classic_example(self):
        """经典例子 kitten -> sitting"""
        self.assertEqual(levenshtein_distance("kitten", "sitting"), 3)
    
    def test_single_operations(self):
        """单次编辑操作"""
        # 单次插入
        self.assertEqual(levenshtein_distance("hello", "helloo"), 1)
        # 单次删除
        self.assertEqual(levenshtein_distance("helloo", "hello"), 1)
        # 单次替换
        self.assertEqual(levenshtein_distance("hello", "hallo"), 1)
    
    def test_multiple_operations(self):
        """多次编辑操作"""
        self.assertEqual(levenshtein_distance("sunday", "saturday"), 3)
        self.assertEqual(levenshtein_distance("book", "back"), 2)
    
    def test_unicode_strings(self):
        """Unicode 字符串测试"""
        self.assertEqual(levenshtein_distance("你好", "你好"), 0)
        self.assertEqual(levenshtein_distance("你好", "您好"), 1)
        self.assertEqual(levenshtein_distance("中文", "英文"), 1)
    
    def test_long_strings(self):
        """长字符串测试"""
        s1 = "The quick brown fox jumps over the lazy dog"
        s2 = "The quick brown fox jumps over lazy dog"  # 删除 "the "
        self.assertEqual(levenshtein_distance(s1, s2), 4)


class TestOptimizedLevenshtein(unittest.TestCase):
    """测试空间优化版 Levenshtein"""
    
    def test_consistency_with_basic(self):
        """与基础版本结果一致性"""
        test_cases = [
            ("kitten", "sitting"),
            ("", "abc"),
            ("abc", ""),
            ("hello", "hello"),
            ("sunday", "saturday"),
        ]
        for s1, s2 in test_cases:
            basic = levenshtein_distance(s1, s2)
            opt = levenshtein_distance_optimized(s1, s2)
            self.assertEqual(basic, opt, f"不一致: {s1}, {s2}")
    
    def test_symmetry(self):
        """距离对称性"""
        self.assertEqual(
            levenshtein_distance_optimized("abc", "def"),
            levenshtein_distance_optimized("def", "abc")
        )


class TestThresholdLevenshtein(unittest.TestCase):
    """测试带阈值的距离计算"""
    
    def test_within_threshold(self):
        """距离在阈值内"""
        self.assertEqual(levenshtein_distance_threshold("hello", "hallo", 2), 1)
        self.assertEqual(levenshtein_distance_threshold("hello", "hello", 0), 0)
    
    def test_exceeds_threshold(self):
        """距离超过阈值"""
        result = levenshtein_distance_threshold("hello", "world", 2)
        self.assertEqual(result, 3)  # threshold + 1
    
    def test_threshold_zero(self):
        """阈值为 0"""
        self.assertEqual(levenshtein_distance_threshold("hello", "hello", 0), 0)
        result = levenshtein_distance_threshold("hello", "hallo", 0)
        self.assertEqual(result, 1)  # threshold + 1
    
    def test_length_difference_exceeds(self):
        """长度差异超过阈值"""
        result = levenshtein_distance_threshold("a", "abcdefgh", 2)
        self.assertEqual(result, 3)  # threshold + 1


class TestSimilarityRatio(unittest.TestCase):
    """测试相似度比率计算"""
    
    def test_identical_strings(self):
        """相同字符串相似度为 1"""
        self.assertEqual(similarity_ratio("hello", "hello"), 1.0)
        self.assertEqual(similarity_ratio("", ""), 1.0)
    
    def test_completely_different(self):
        """完全不同的字符串"""
        sim = similarity_ratio("abc", "xyz")
        self.assertEqual(sim, 0.0)
    
    def test_partial_similarity(self):
        """部分相似"""
        sim = similarity_ratio("kitten", "sitting")
        self.assertAlmostEqual(sim, 1 - 3/7, places=3)
    
    def test_empty_vs_nonempty(self):
        """空字符串与非空字符串"""
        self.assertEqual(similarity_ratio("", "abc"), 0.0)
        self.assertEqual(similarity_ratio("abc", ""), 0.0)


class TestSimilarityResult(unittest.TestCase):
    """测试完整相似度结果"""
    
    def test_result_properties(self):
        """结果属性测试"""
        result = similarity_result("kitten", "sitting")
        self.assertEqual(result.distance, 3)
        self.assertEqual(result.max_length, 7)
        self.assertAlmostEqual(result.similarity, 1 - 3/7, places=3)
    
    def test_is_similar_method(self):
        """相似判断方法"""
        result = similarity_result("hello", "hallo")
        self.assertTrue(result.is_similar(0.5))
        self.assertTrue(result.is_similar(0.8))
        self.assertFalse(result.is_similar(0.9))
    
    def test_empty_strings(self):
        """空字符串结果"""
        result = similarity_result("", "")
        self.assertEqual(result.distance, 0)
        self.assertEqual(result.max_length, 0)
        self.assertEqual(result.similarity, 1.0)


class TestJaroSimilarity(unittest.TestCase):
    """测试 Jaro 相似度"""
    
    def test_identical_strings(self):
        """相同字符串"""
        self.assertEqual(jaro_similarity("hello", "hello"), 1.0)
    
    def test_classic_example(self):
        """经典例子"""
        # MARTHA vs MARHTA
        jaro = jaro_similarity("MARTHA", "MARHTA")
        self.assertAlmostEqual(jaro, 0.944, places=2)
    
    def test_empty_strings(self):
        """空字符串"""
        self.assertEqual(jaro_similarity("", ""), 1.0)
        self.assertEqual(jaro_similarity("", "abc"), 0.0)
    
    def test_no_matches(self):
        """无匹配"""
        self.assertEqual(jaro_similarity("abc", "xyz"), 0.0)


class TestJaroWinklerSimilarity(unittest.TestCase):
    """测试 Jaro-Winkler 相似度"""
    
    def test_prefix_bonus(self):
        """公共前缀加分"""
        jw = jaro_winkler_similarity("MARTHA", "MARHTA")
        jaro = jaro_similarity("MARTHA", "MARHTA")
        self.assertGreater(jw, jaro)  # Jaro-Winkler 应更高
    
    def test_identical_strings(self):
        """相同字符串"""
        self.assertEqual(jaro_winkler_similarity("hello", "hello"), 1.0)
    
    def test_long_prefix(self):
        """长公共前缀"""
        jw = jaro_winkler_similarity("abcdefgh", "abcdefxy")
        self.assertGreater(jw, 0.8)


class TestEditOperations(unittest.TestCase):
    """测试编辑操作序列"""
    
    def test_basic_operations(self):
        """基础操作序列"""
        ops = levenshtein_operations("kitten", "sitting")
        # 应包含操作
        self.assertGreater(len(ops), 0)
        
        # 验证可以应用操作得到目标字符串
        result = apply_operations("kitten", ops)
        self.assertEqual(result, "sitting")
    
    def test_identical_strings(self):
        """相同字符串只有 MATCH 操作"""
        ops = levenshtein_operations("hello", "hello")
        for op in ops:
            self.assertEqual(op.operation, EditOperation.MATCH)
    
    def test_empty_to_string(self):
        """空字符串到非空"""
        ops = levenshtein_operations("", "abc")
        self.assertEqual(len(ops), 3)
        for op in ops:
            self.assertEqual(op.operation, EditOperation.INSERT)
    
    def test_string_to_empty(self):
        """非空到空字符串"""
        ops = levenshtein_operations("abc", "")
        self.assertEqual(len(ops), 3)
        for op in ops:
            self.assertEqual(op.operation, EditOperation.DELETE)
    
    def test_edit_step_description(self):
        """编辑步骤描述"""
        step = EditStep(EditOperation.REPLACE, 0, "a", "b")
        desc = step.describe()
        self.assertIn("替换", desc)


class TestDamerauLevenshtein(unittest.TestCase):
    """测试 Damerau-Levenshtein 距离"""
    
    def test_transpose_benefit(self):
        """交换操作的优势"""
        # ab -> ba: Damerau 只需 1 次，普通需要 2 次
        dl = damerau_levenshtein_distance("ab", "ba")
        l = levenshtein_distance("ab", "ba")
        self.assertEqual(dl, 1)
        self.assertEqual(l, 2)
    
    def test_regular_cases(self):
        """常规情况与普通版本相同"""
        self.assertEqual(
            damerau_levenshtein_distance("kitten", "sitting"),
            levenshtein_distance("kitten", "sitting")
        )
    
    def test_identical_strings(self):
        """相同字符串"""
        self.assertEqual(damerau_levenshtein_distance("hello", "hello"), 0)
    
    def test_empty_strings(self):
        """空字符串"""
        self.assertEqual(damerau_levenshtein_distance("", "abc"), 3)
    
    def test_complex_transpose(self):
        """复杂交换场景"""
        # 多处相邻交换
        dl = damerau_levenshtein_distance("abcd", "badc")
        self.assertLess(dl, levenshtein_distance("abcd", "badc"))


class TestLCS(unittest.TestCase):
    """测试最长公共子序列"""
    
    def test_classic_example(self):
        """经典例子"""
        lcs = longest_common_subsequence("ABCBDAB", "BDCABA")
        self.assertEqual(len(lcs), 4)  # LCS 长度为 4，具体结果可能有多种
    
    def test_lcs_length(self):
        """LCS 长度"""
        self.assertEqual(lcs_length("ABCBDAB", "BDCABA"), 4)
    
    def test_identical_strings(self):
        """相同字符串"""
        self.assertEqual(longest_common_subsequence("hello", "hello"), "hello")
        self.assertEqual(lcs_length("hello", "hello"), 5)
    
    def test_no_common(self):
        """无公共子序列"""
        self.assertEqual(longest_common_subsequence("abc", "xyz"), "")
        self.assertEqual(lcs_length("abc", "xyz"), 0)
    
    def test_empty_strings(self):
        """空字符串"""
        self.assertEqual(longest_common_subsequence("", "abc"), "")
        self.assertEqual(lcs_length("abc", ""), 0)
    
    def test_partial_common(self):
        """部分公共"""
        lcs = longest_common_subsequence("abcdef", "ace")
        self.assertEqual(lcs, "ace")


class TestFuzzySearch(unittest.TestCase):
    """测试模糊搜索"""
    
    def test_find_similar(self):
        """查找相似字符串"""
        candidates = ["hallo", "helloo", "world", "hell"]
        results = find_similar("hello", candidates, threshold=0.5)
        
        # 应返回相似度 >= 0.5 的结果
        for word, sim in results:
            self.assertGreaterEqual(sim, 0.5)
        
        # 按相似度降序
        sims = [sim for _, sim in results]
        self.assertEqual(sims, sorted(sims, reverse=True))
    
    def test_find_similar_limit(self):
        """限制返回数量"""
        candidates = ["a", "b", "c", "d", "e", "f", "g"]
        results = find_similar("a", candidates, threshold=0.0, limit=3)
        self.assertLessEqual(len(results), 3)
    
    def test_find_nearest(self):
        """查找最近字符串"""
        candidates = ["hallo", "world", "help"]
        word, dist = find_nearest("hello", candidates)
        self.assertEqual(word, "hallo")
        self.assertEqual(dist, 1)
    
    def test_find_nearest_empty_candidates(self):
        """空候选列表"""
        word, dist = find_nearest("hello", [])
        self.assertEqual(dist, 5)
    
    def test_fuzzy_search_in_text(self):
        """文本中模糊搜索"""
        text = "hallo world helloo"
        results = fuzzy_search("hello", text, max_distance=2)
        
        # 应找到相似片段
        self.assertGreater(len(results), 0)
        
        # 每个结果的距离应在阈值内
        for pos, dist, substr in results:
            self.assertLessEqual(dist, 2)


class TestBatchOperations(unittest.TestCase):
    """测试批量操作"""
    
    def test_batch_similarity(self):
        """批量相似度"""
        pairs = [("hello", "hallo"), ("world", "word")]
        sims = batch_similarity(pairs)
        
        self.assertEqual(len(sims), 2)
        for sim in sims:
            self.assertGreater(sim, 0.0)
    
    def test_batch_distance(self):
        """批量距离"""
        pairs = [("kitten", "sitting"), ("hello", "hello")]
        dists = batch_distance(pairs)
        
        self.assertEqual(dists, [3, 0])
    
    def test_similarity_matrix(self):
        """相似度矩阵"""
        strings = ["hello", "hallo", "world"]
        matrix = similarity_matrix(strings)
        
        # 对角线应为 1.0
        for i in range(3):
            self.assertEqual(matrix[i][i], 1.0)
        
        # 矩阵对称
        for i in range(3):
            for j in range(3):
                self.assertEqual(matrix[i][j], matrix[j][i])


class TestUtilityFunctions(unittest.TestCase):
    """测试工具函数"""
    
    def test_normalized_levenshtein(self):
        """归一化距离"""
        self.assertEqual(normalized_levenshtein("hello", "hello"), 0.0)
        self.assertEqual(normalized_levenshtein("", "abc"), 1.0)
    
    def test_hamming_distance(self):
        """汉明距离"""
        self.assertEqual(hamming_distance("karolin", "kathrin"), 3)
        self.assertEqual(hamming_distance("hello", "hello"), 0)
    
    def test_hamming_distance_unequal_length(self):
        """不等长汉明距离应报错"""
        with self.assertRaises(ValueError):
            hamming_distance("abc", "abcd")
    
    def test_is_one_edit_away(self):
        """一次编辑判断"""
        self.assertTrue(is_one_edit_away("hello", "hallo"))  # 替换
        self.assertTrue(is_one_edit_away("hello", "helo"))   # 删除
        self.assertTrue(is_one_edit_away("helo", "hello"))   # 插入
        self.assertFalse(is_one_edit_away("hello", "world"))
        self.assertFalse(is_one_edit_away("hello", "hellaoo"))
    
    def test_spell_check_suggestions(self):
        """拼写建议"""
        dictionary = ["hello", "help", "held", "hero", "helmet"]
        suggestions = spell_check_suggestions("helo", dictionary, max_distance=1)
        
        self.assertGreater(len(suggestions), 0)
        
        # 所有建议距离应在阈值内
        for word, dist in suggestions:
            self.assertLessEqual(dist, 1)
    
    def test_align_strings(self):
        """字符串对齐"""
        a1, a2 = align_strings("kitten", "sitting")
        
        # 对齐后应有合理的填充
        self.assertEqual(len(a1), len(a2))


class TestEdgeCases(unittest.TestCase):
    """测试边界情况"""
    
    def test_single_character(self):
        """单字符"""
        self.assertEqual(levenshtein_distance("a", "a"), 0)
        self.assertEqual(levenshtein_distance("a", "b"), 1)
        self.assertEqual(levenshtein_distance("a", ""), 1)
    
    def test_very_long_strings(self):
        """非常长的字符串"""
        s1 = "a" * 1000
        s2 = "a" * 1000
        self.assertEqual(levenshtein_distance_optimized(s1, s2), 0)
        
        s2 = "b" * 1000
        self.assertEqual(levenshtein_distance_optimized(s1, s2), 1000)
    
    def test_threshold_efficiency(self):
        """阈值优化效率"""
        # 长字符串但阈值很小，应快速返回
        s1 = "a" * 1000
        s2 = "b" * 1000
        result = levenshtein_distance_threshold(s1, s2, 5)
        self.assertEqual(result, 6)  # threshold + 1


class TestIntegration(unittest.TestCase):
    """综合测试"""
    
    def test_workflow(self):
        """完整工作流程"""
        # 模拟拼写检查工作流程
        word = "typoo"
        dictionary = ["type", "typo", "typical", "typing", "top"]
        
        # 找相似词
        similar = find_similar(word, dictionary, threshold=0.5)
        self.assertGreater(len(similar), 0)
        
        # 获取拼写建议
        suggestions = spell_check_suggestions(word, dictionary, max_distance=2)
        self.assertGreater(len(suggestions), 0)
        
        # 找最近词
        nearest, dist = find_nearest(word, dictionary)
        self.assertLess(dist, 3)
    
    def test_distance_operations_consistency(self):
        """距离与操作序列一致性"""
        test_pairs = [
            ("kitten", "sitting"),
            ("sunday", "saturday"),
            ("hello", "hallo"),
        ]
        
        for s1, s2 in test_pairs:
            # 计算距离
            dist = levenshtein_distance(s1, s2)
            
            # 获取操作
            ops = levenshtein_operations(s1, s2)
            
            # 验证非匹配操作数量等于距离
            non_match_ops = [op for op in ops 
                           if op.operation != EditOperation.MATCH]
            self.assertEqual(len(non_match_ops), dist)


if __name__ == "__main__":
    unittest.main(verbosity=2)