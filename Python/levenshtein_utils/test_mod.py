"""
测试 Levenshtein Distance Utils
"""

import pytest
from mod import (
    levenshtein_distance,
    similarity,
    find_closest,
    find_all_closest,
    edit_sequence,
    apply_edits,
    normalized_distance,
    ratio,
    hamming_distance,
    damerau_levenshtein_distance
)


class TestLevenshteinDistance:
    """测试编辑距离计算"""
    
    def test_identical_strings(self):
        """测试相同字符串"""
        assert levenshtein_distance("", "") == 0
        assert levenshtein_distance("abc", "abc") == 0
        assert levenshtein_distance("hello", "hello") == 0
    
    def test_empty_strings(self):
        """测试空字符串"""
        assert levenshtein_distance("", "abc") == 3
        assert levenshtein_distance("abc", "") == 3
        assert levenshtein_distance("", "") == 0
    
    def test_basic_cases(self):
        """测试基本案例"""
        assert levenshtein_distance("kitten", "sitting") == 3
        assert levenshtein_distance("book", "back") == 2
        assert levenshtein_distance("abc", "ab") == 1
        assert levenshtein_distance("ab", "abc") == 1
    
    def test_substitution_only(self):
        """测试仅替换操作"""
        assert levenshtein_distance("abc", "abd") == 1
        assert levenshtein_distance("abc", "xyz") == 3
    
    def test_insertion_only(self):
        """测试仅插入操作"""
        assert levenshtein_distance("ac", "abc") == 1
        assert levenshtein_distance("", "abc") == 3
    
    def test_deletion_only(self):
        """测试仅删除操作"""
        assert levenshtein_distance("abc", "ac") == 1
        assert levenshtein_distance("abc", "") == 3
    
    def test_custom_costs(self):
        """测试自定义操作成本"""
        # 插入成本更高
        dist = levenshtein_distance("abc", "ab", insert_cost=2, delete_cost=1)
        # 删除一个字符的成本是 1
        assert dist == 1
        
        # 替换成本更高时，算法会选择插入+删除（成本 2）而不是替换（成本 3）
        dist = levenshtein_distance("abc", "abd", replace_cost=3)
        # 插入+删除 = 2 < 替换 = 3
        assert dist == 2
    
    def test_unicode_strings(self):
        """测试 Unicode 字符串"""
        assert levenshtein_distance("你好", "你好世界") == 2
        assert levenshtein_distance("こんにちは", "こんばんは") == 2


class TestSimilarity:
    """测试相似度计算"""
    
    def test_identical_strings(self):
        """测试相同字符串"""
        assert similarity("abc", "abc") == 1.0
        assert similarity("", "") == 1.0
    
    def test_empty_strings(self):
        """测试空字符串"""
        assert similarity("", "abc") == 0.0
        assert similarity("abc", "") == 0.0
    
    def test_partial_similarity(self):
        """测试部分相似"""
        sim = similarity("kitten", "sitting")
        # 距离 3，最长 7，相似度 = 1 - 3/7 ≈ 0.57
        assert 0.5 < sim < 0.6
    
    def test_no_similarity(self):
        """测试无相似"""
        assert similarity("abc", "xyz") == 0.0
        assert similarity("123", "abc") == 0.0


class TestFindClosest:
    """测试查找最相似字符串"""
    
    def test_exact_match(self):
        """测试精确匹配"""
        candidates = ["apple", "banana", "orange"]
        assert find_closest("apple", candidates) == "apple"
    
    def test_closest_match(self):
        """测试最相似匹配"""
        candidates = ["apple", "banana", "orange"]
        result = find_closest("appel", candidates)
        assert result == "apple"
    
    def test_with_threshold(self):
        """测试阈值过滤"""
        candidates = ["apple", "banana", "orange"]
        result = find_closest("xyz", candidates, threshold=0.5)
        assert result is None
    
    def test_return_distance(self):
        """测试返回距离"""
        candidates = ["apple", "banana", "orange"]
        result = find_closest("appel", candidates, return_distance=True)
        # "appel" -> "apple": 替换 'e' 为 'l'，替换 'l' 为 'e' = 2次
        assert result == ("apple", 2)
    
    def test_empty_candidates(self):
        """测试空候选列表"""
        assert find_closest("test", []) is None
    
    def test_single_candidate(self):
        """测试单个候选"""
        assert find_closest("test", ["test"]) == "test"


class TestFindAllClosest:
    """测试查找所有相似字符串"""
    
    def test_basic_search(self):
        """测试基本搜索"""
        candidates = ["apple", "application", "applet", "appeal"]
        results = find_all_closest("appel", candidates, top_n=3)
        
        assert len(results) <= 3
        # 第一个应该是最相似的（appeal 和 apple 距离相同，都是 2）
        assert results[0][0] in ["apple", "appeal"]
    
    def test_with_threshold(self):
        """测试阈值过滤"""
        candidates = ["apple", "xyz", "abc"]
        results = find_all_closest("test", candidates, threshold=0.9)
        # 没有满足高阈值的候选
        assert len(results) == 0
    
    def test_empty_candidates(self):
        """测试空候选列表"""
        assert find_all_closest("test", []) == []
    
    def test_sorted_by_similarity(self):
        """测试按相似度排序"""
        candidates = ["color", "colour", "colors", "column"]
        results = find_all_closest("color", candidates, top_n=4)
        
        # 检查是否按相似度降序排列
        similarities = [r[1] for r in results]
        assert similarities == sorted(similarities, reverse=True)


class TestEditSequence:
    """测试编辑操作序列"""
    
    def test_basic_sequence(self):
        """测试基本序列"""
        dist, ops = edit_sequence("kitten", "sitting")
        assert dist == 3
    
    def test_identical_strings(self):
        """测试相同字符串"""
        dist, ops = edit_sequence("abc", "abc")
        assert dist == 0
        # 所有操作都应该是 equal
        for op, _ in ops:
            assert op == "equal"
    
    def test_empty_strings(self):
        """测试空字符串"""
        dist, ops = edit_sequence("", "abc")
        assert dist == 3
        
        dist, ops = edit_sequence("abc", "")
        assert dist == 3
    
    def test_single_operations(self):
        """测试单个操作"""
        # 替换
        dist, ops = edit_sequence("abc", "abd")
        assert dist == 1
        
        # 插入
        dist, ops = edit_sequence("ac", "abc")
        assert dist == 1
        
        # 删除
        dist, ops = edit_sequence("abc", "ac")
        assert dist == 1


class TestApplyEdits:
    """测试应用编辑操作"""
    
    def test_basic_edit(self):
        """测试基本编辑"""
        s1, s2 = "kitten", "sitting"
        dist, ops = edit_sequence(s1, s2)
        result = apply_edits(s1, ops)
        assert result == s2
    
    def test_identical_strings(self):
        """测试相同字符串"""
        dist, ops = edit_sequence("abc", "abc")
        result = apply_edits("abc", ops)
        assert result == "abc"
    
    def test_empty_to_content(self):
        """测试空字符串到有内容"""
        dist, ops = edit_sequence("", "hello")
        result = apply_edits("", ops)
        assert result == "hello"
    
    def test_content_to_empty(self):
        """测试有内容到空字符串"""
        dist, ops = edit_sequence("hello", "")
        result = apply_edits("hello", ops)
        assert result == ""


class TestNormalizedDistance:
    """测试归一化距离"""
    
    def test_identical_strings(self):
        """测试相同字符串"""
        assert normalized_distance("abc", "abc") == 0.0
        assert normalized_distance("", "") == 0.0
    
    def test_partial_distance(self):
        """测试部分距离"""
        dist = normalized_distance("abc", "abd")
        # 距离 1，总长度 6，归一化 = 1/6 ≈ 0.167
        assert 0.1 < dist < 0.2
    
    def test_completely_different(self):
        """测试完全不同"""
        dist = normalized_distance("", "abc")
        # 距离 3，总长度 3，归一化 = 1.0
        assert dist == 1.0


class TestRatio:
    """测试匹配比率"""
    
    def test_identical_strings(self):
        """测试相同字符串"""
        assert ratio("abc", "abc") == 100.0
    
    def test_partial_match(self):
        """测试部分匹配"""
        r = ratio("hello world", "hello")
        # (16-6)/16 * 100 = 62.5
        assert 50 < r < 70
    
    def test_no_match(self):
        """测试无匹配"""
        r = ratio("", "abc")
        assert r == 0.0


class TestHammingDistance:
    """测试汉明距离"""
    
    def test_basic_cases(self):
        """测试基本案例"""
        assert hamming_distance("karolin", "kathrin") == 3
        assert hamming_distance("1011101", "1001001") == 2
        assert hamming_distance("abc", "abc") == 0
    
    def test_unequal_length_error(self):
        """测试不等长字符串报错"""
        with pytest.raises(ValueError):
            hamming_distance("abc", "ab")
        
        with pytest.raises(ValueError):
            hamming_distance("ab", "abc")


class TestDamerauLevenshteinDistance:
    """测试 Damerau-Levenshtein 距离"""
    
    def test_basic_cases(self):
        """测试基本案例"""
        # 相邻字符交换
        assert damerau_levenshtein_distance("abcd", "acbd") == 1
        # 普通编辑
        assert damerau_levenshtein_distance("kitten", "sitting") == 3
    
    def test_empty_strings(self):
        """测试空字符串"""
        assert damerau_levenshtein_distance("", "abc") == 3
        assert damerau_levenshtein_distance("abc", "") == 3
        assert damerau_levenshtein_distance("", "") == 0
    
    def test_vs_levenshtein(self):
        """对比 Levenshtein 距离"""
        # 对于非相邻交换的情况，两者应该相同
        s1, s2 = "book", "back"
        assert damerau_levenshtein_distance(s1, s2) == levenshtein_distance(s1, s2)
        
        # 对于相邻交换，Damerau-Levenshtein 可能更小
        s1, s2 = "abcd", "acbd"
        dl = damerau_levenshtein_distance(s1, s2)
        l = levenshtein_distance(s1, s2)
        assert dl <= l


class TestIntegration:
    """集成测试"""
    
    def test_fuzzy_search_workflow(self):
        """测试模糊搜索工作流"""
        # 模拟拼写纠正场景
        dictionary = ["apple", "application", "applet", "appeal", "applepie"]
        misspelled = "appel"
        
        # 找到最相似的词（appeal 距离为 1，比 apple 的 2 更小）
        closest = find_closest(misspelled, dictionary)
        assert closest == "appeal"
        
        # 找到所有相似度 > 50% 的词
        similar = find_all_closest(misspelled, dictionary, threshold=0.5)
        assert len(similar) > 0
        
        # 获取编辑距离和操作序列
        dist, ops = edit_sequence(misspelled, closest)
        assert dist == 1
    
    def test_string_comparison_workflow(self):
        """测试字符串比较工作流"""
        s1, s2 = "algorithm", "logarithm"
        
        # 计算各种距离度量
        l_dist = levenshtein_distance(s1, s2)
        dl_dist = damerau_levenshtein_distance(s1, s2)
        sim = similarity(s1, s2)
        r = ratio(s1, s2)
        
        # 验证一致性
        assert dl_dist <= l_dist
        assert sim == 1.0 - (l_dist / max(len(s1), len(s2)))
        assert r > 0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])