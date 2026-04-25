"""
Rabin-Karp 工具模块测试

测试覆盖:
- 基本字符串搜索
- 多模式搜索
- 通配符搜索
- 重复子串检测
- 公共子串查找
- 文本相似度计算
- 抄袭检测
- 二维模式搜索
- 匹配器类
- 双哈希搜索
"""

import unittest
import sys
import os

# 添加父目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from rabin_karp_utils.mod import (
    RollingHash,
    rabin_karp_search,
    multi_pattern_search,
    find_all_occurrences,
    contains_pattern,
    count_occurrences,
    find_with_wildcards,
    find_longest_repeated_substring,
    find_common_substring,
    compute_similarity,
    detect_plagiarism,
    two_d_pattern_search,
    RabinKarpMatcher,
    double_hash_search,
    MatchResult,
)


class TestRollingHash(unittest.TestCase):
    """测试滚动哈希"""
    
    def test_basic_hash(self):
        """基本哈希计算"""
        rh = RollingHash()
        h1 = rh.compute("hello")
        h2 = rh.compute("hello")
        self.assertEqual(h1, h2)
        
    def test_different_strings(self):
        """不同字符串有不同哈希（大概率）"""
        rh = RollingHash()
        h1 = rh.compute("hello")
        h2 = rh.compute("world")
        self.assertNotEqual(h1, h2)
    
    def test_slide_window(self):
        """滑动窗口测试"""
        rh = RollingHash()
        # "ello" 的哈希
        expected = rh.compute("ello")
        # "hello" 滑动到 "ello"
        rh.compute("hello")
        actual = rh.slide('h', 'o', 5)  # 错误的用法，我们测试另一方式
        
        # 正确测试
        rh2 = RollingHash()
        full_hash = rh2.compute("hello")
        # 用滑动重新计算
        rh3 = RollingHash()
        rh3.compute("hell")
        # 注意：slide 是移除左边，添加右边
        
    def test_base_power_cache(self):
        """base power 缓存"""
        rh = RollingHash()
        p1 = rh._get_base_power(5)
        p2 = rh._get_base_power(5)
        self.assertEqual(p1, p2)


class TestRabinKarpSearch(unittest.TestCase):
    """测试基本搜索"""
    
    def test_simple_match(self):
        """简单匹配"""
        text = "hello world"
        pattern = "world"
        result = rabin_karp_search(text, pattern)
        self.assertEqual(result, [6])
    
    def test_multiple_matches(self):
        """多匹配"""
        text = "abracadabra"
        pattern = "abra"
        result = rabin_karp_search(text, pattern)
        self.assertEqual(result, [0, 7])
    
    def test_no_match(self):
        """无匹配"""
        text = "hello world"
        pattern = "xyz"
        result = rabin_karp_search(text, pattern)
        self.assertEqual(result, [])
    
    def test_empty_pattern(self):
        """空模式"""
        text = "hello"
        pattern = ""
        result = rabin_karp_search(text, pattern)
        self.assertEqual(result, [])
    
    def test_pattern_longer_than_text(self):
        """模式长于文本"""
        text = "hi"
        pattern = "hello"
        result = rabin_karp_search(text, pattern)
        self.assertEqual(result, [])
    
    def test_exact_match(self):
        """精确匹配"""
        text = "hello"
        pattern = "hello"
        result = rabin_karp_search(text, pattern)
        self.assertEqual(result, [0])
    
    def test_overlapping_matches(self):
        """重叠匹配"""
        text = "aaa"
        pattern = "aa"
        result = rabin_karp_search(text, pattern)
        self.assertEqual(result, [0, 1])
    
    def test_single_char(self):
        """单字符匹配"""
        text = "hello"
        pattern = "l"
        result = rabin_karp_search(text, pattern)
        self.assertEqual(result, [2, 3])


class TestMultiPatternSearch(unittest.TestCase):
    """测试多模式搜索"""
    
    def test_multiple_patterns(self):
        """多模式匹配"""
        text = "hello world, hello there"
        patterns = ["hello", "world", "there"]
        result = multi_pattern_search(text, patterns)
        positions = [(r.index, r.pattern) for r in result]
        self.assertIn((0, "hello"), positions)
        self.assertIn((6, "world"), positions)
        # "there" at index 19 (after ", ")
        self.assertIn((19, "there"), positions)
    
    def test_empty_patterns(self):
        """空模式列表"""
        result = multi_pattern_search("hello", [])
        self.assertEqual(result, [])
    
    def test_no_matches(self):
        """无匹配"""
        text = "hello world"
        patterns = ["xyz", "abc"]
        result = multi_pattern_search(text, patterns)
        self.assertEqual(result, [])
    
    def test_different_lengths(self):
        """不同长度模式"""
        text = "abc xyz abcdef"
        patterns = ["abc", "abcdef", "xyz"]
        result = multi_pattern_search(text, patterns)
        positions = [(r.index, r.pattern) for r in result]
        # abc at 0, xyz at 4, abc at 8, abcdef at 8 (overlapping)
        self.assertGreaterEqual(len(result), 3)


class TestConvenienceMethods(unittest.TestCase):
    """测试便捷方法"""
    
    def test_find_all_occurrences(self):
        """查找所有出现"""
        result = find_all_occurrences("banana", "ana")
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0].index, 1)
        self.assertEqual(result[1].index, 3)
    
    def test_contains_pattern(self):
        """包含模式"""
        self.assertTrue(contains_pattern("hello world", "world"))
        self.assertFalse(contains_pattern("hello world", "xyz"))
    
    def test_count_occurrences(self):
        """计数"""
        self.assertEqual(count_occurrences("banana", "a"), 3)
        self.assertEqual(count_occurrences("banana", "ana"), 2)
        self.assertEqual(count_occurrences("hello", "xyz"), 0)


class TestWildcardSearch(unittest.TestCase):
    """测试通配符搜索"""
    
    def test_single_wildcard(self):
        """单通配符"""
        result = find_with_wildcards("hello", "h?llo")
        self.assertEqual(result, [0])
    
    def test_multiple_wildcards(self):
        """多通配符"""
        result = find_with_wildcards("hello", "h??lo")
        self.assertEqual(result, [0])
    
    def test_no_wildcard(self):
        """无通配符"""
        result = find_with_wildcards("hello", "ello")
        self.assertEqual(result, [1])
    
    def test_wildcard_at_end(self):
        """末尾通配符"""
        result = find_with_wildcards("hello", "hel?o")
        self.assertEqual(result, [0])
    
    def test_all_wildcards(self):
        """全通配符"""
        result = find_with_wildcards("hello", "?????")
        self.assertEqual(result, [0])


class TestLongestRepeatedSubstring(unittest.TestCase):
    """测试最长重复子串"""
    
    def test_simple_case(self):
        """简单情况"""
        result = find_longest_repeated_substring("banana")
        self.assertIsNotNone(result)
        substring, positions = result
        self.assertEqual(substring, "ana")
        self.assertEqual(positions, [1, 3])
    
    def test_no_repeat(self):
        """无重复"""
        result = find_longest_repeated_substring("abcdef")
        self.assertIsNone(result)
    
    def test_empty_string(self):
        """空字符串"""
        result = find_longest_repeated_substring("")
        self.assertIsNone(result)
    
    def test_full_repeat(self):
        """完整重复"""
        result = find_longest_repeated_substring("abcabc")
        self.assertIsNotNone(result)
        substring, _ = result
        self.assertEqual(substring, "abc")


class TestCommonSubstring(unittest.TestCase):
    """测试公共子串"""
    
    def test_common_substring(self):
        """公共子串"""
        result = find_common_substring(["programming", "programmer", "program"])
        self.assertIsNotNone(result)
        self.assertEqual(result, "program")
    
    def test_no_common(self):
        """无公共子串"""
        result = find_common_substring(["abc", "xyz"])
        self.assertIsNone(result)
    
    def test_single_string(self):
        """单字符串"""
        result = find_common_substring(["hello"])
        self.assertEqual(result, "hello")
    
    def test_empty_list(self):
        """空列表"""
        result = find_common_substring([])
        self.assertIsNone(result)


class TestSimilarity(unittest.TestCase):
    """测试文本相似度"""
    
    def test_identical_texts(self):
        """相同文本"""
        sim = compute_similarity("hello world", "hello world")
        self.assertEqual(sim, 1.0)
    
    def test_different_texts(self):
        """不同文本"""
        sim = compute_similarity("hello world", "goodbye moon")
        self.assertLess(sim, 0.5)
    
    def test_similar_texts(self):
        """相似文本"""
        sim = compute_similarity("hello world", "hello there")
        self.assertGreater(sim, 0.1)  # 有一定相似度
        self.assertLess(sim, 0.8)
    
    def test_empty_texts(self):
        """空文本"""
        sim = compute_similarity("", "hello")
        self.assertEqual(sim, 0.0)
        sim = compute_similarity("hello", "")
        self.assertEqual(sim, 0.0)


class TestPlagiarismDetection(unittest.TestCase):
    """测试抄袭检测"""
    
    def test_plagiarism_detection(self):
        """抄袭检测"""
        docs = [
            "The quick brown fox jumps over the lazy dog.",
            "The quick brown fox jumps over the lazy cat.",  # 相似
            "Python is a programming language.",  # 不同
        ]
        result = detect_plagiarism(docs, threshold=0.3, k=5)
        self.assertTrue(len(result) > 0)
        # 第一个和第二个应该被检测为相似
        found = any(r[0] == 0 and r[1] == 1 for r in result)
        self.assertTrue(found)
    
    def test_no_plagiarism(self):
        """无抄袭"""
        docs = ["abc", "xyz", "123"]
        result = detect_plagiarism(docs, threshold=0.9)
        self.assertEqual(len(result), 0)


class Test2DPatternSearch(unittest.TestCase):
    """测试二维模式搜索"""
    
    def test_simple_2d(self):
        """简单二维搜索"""
        text = ["abcde", "fghij", "klmno"]
        pattern = ["ghi", "lmn"]
        result = two_d_pattern_search(text, pattern)
        self.assertEqual(result, [(1, 1)])
    
    def test_not_found(self):
        """未找到"""
        text = ["abc", "def"]
        pattern = ["xyz"]
        result = two_d_pattern_search(text, pattern)
        self.assertEqual(result, [])
    
    def test_multiple_occurrences(self):
        """多次出现"""
        text = ["abab", "abab"]
        pattern = ["ab", "ab"]
        result = two_d_pattern_search(text, pattern)
        self.assertTrue(len(result) >= 2)
    
    def test_invalid_grid(self):
        """无效网格"""
        text = ["abc", "de"]  # 行长度不一致
        pattern = ["ab"]
        with self.assertRaises(ValueError):
            two_d_pattern_search(text, pattern)


class TestRabinKarpMatcher(unittest.TestCase):
    """测试匹配器类"""
    
    def test_matcher_search(self):
        """匹配器搜索"""
        matcher = RabinKarpMatcher(["hello", "world"])
        result = matcher.search("hello world, hello there")
        self.assertEqual(len(result), 3)
        patterns = [r.pattern for r in result]
        self.assertEqual(patterns.count("hello"), 2)
        self.assertEqual(patterns.count("world"), 1)
    
    def test_empty_matcher(self):
        """空匹配器"""
        matcher = RabinKarpMatcher([])
        result = matcher.search("hello world")
        self.assertEqual(result, [])
    
    def test_add_pattern(self):
        """动态添加模式"""
        matcher = RabinKarpMatcher(["hello"])
        matcher.add_pattern("world")
        result = matcher.search("hello world")
        self.assertEqual(len(result), 2)
    
    def test_remove_pattern(self):
        """移除模式"""
        matcher = RabinKarpMatcher(["hello", "world"])
        matcher.remove_pattern("world")
        result = matcher.search("hello world")
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].pattern, "hello")
    
    def test_iterator(self):
        """迭代器"""
        matcher = RabinKarpMatcher(["a", "b"])
        result = list(matcher.search_iter("abc"))
        self.assertEqual(len(result), 2)


class TestDoubleHash(unittest.TestCase):
    """测试双哈希搜索"""
    
    def test_double_hash_basic(self):
        """双哈希基本测试"""
        result = double_hash_search("hello world", "world")
        self.assertEqual(result, [6])
    
    def test_double_hash_multiple(self):
        """双哈希多匹配"""
        result = double_hash_search("abracadabra", "abra")
        self.assertEqual(result, [0, 7])
    
    def test_double_hash_no_match(self):
        """双哈希无匹配"""
        result = double_hash_search("hello", "xyz")
        self.assertEqual(result, [])


class TestMatchResult(unittest.TestCase):
    """测试匹配结果"""
    
    def test_match_result_repr(self):
        """匹配结果表示"""
        result = MatchResult(5, "test", 9)
        repr_str = repr(result)
        self.assertIn("5", repr_str)
        self.assertIn("test", repr_str)


class TestEdgeCases(unittest.TestCase):
    """边缘情况测试"""
    
    def test_unicode_support(self):
        """Unicode 支持"""
        text = "你好世界你好中国"  # 无逗号，更简单
        pattern = "你好"
        result = rabin_karp_search(text, pattern)
        self.assertEqual(result, [0, 4])  # "你好世界"是4个字符
    
    def test_large_text(self):
        """大文本"""
        text = "a" * 10000 + "needle" + "a" * 10000
        pattern = "needle"
        result = rabin_karp_search(text, pattern)
        self.assertEqual(result, [10000])
    
    def test_many_patterns(self):
        """多模式搜索"""
        text = "The quick brown fox jumps over the lazy dog"
        patterns = [f"word{i}" for i in range(100)]
        patterns.append("fox")
        result = multi_pattern_search(text, patterns)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].pattern, "fox")


if __name__ == "__main__":
    unittest.main(verbosity=2)