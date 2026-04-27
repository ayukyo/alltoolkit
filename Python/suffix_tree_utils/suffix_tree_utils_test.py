"""
Suffix Tree Utils 测试文件

测试后缀树的各项功能
"""

import sys
import os
import unittest

# Add module directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mod import (
    SuffixTree, GeneralizedSuffixTree,
    build_suffix_tree,
    find_all_occurrences,
    longest_repeated_substring,
    longest_common_substring,
    count_occurrences,
    build_suffix_array
)


class TestSuffixTreeBasic(unittest.TestCase):
    """基本功能测试"""
    
    def test_build_simple(self):
        """测试简单字符串构建"""
        st = SuffixTree("abc")
        self.assertIsNotNone(st.root)
    
    def test_build_empty(self):
        """测试空字符串"""
        st = SuffixTree("")
        self.assertIsNotNone(st.root)
    
    def test_build_single_char(self):
        """测试单字符"""
        st = SuffixTree("a")
        self.assertIsNotNone(st.root)
    
    def test_build_repeated(self):
        """测试重复字符"""
        st = SuffixTree("aaa")
        self.assertIsNotNone(st.root)


class TestPatternSearch(unittest.TestCase):
    """模式搜索测试"""
    
    def test_search_simple(self):
        """测试简单搜索"""
        st = SuffixTree("banana")
        self.assertEqual(sorted(st.search("ana")), [1, 3])
    
    def test_search_prefix(self):
        """测试前缀搜索"""
        st = SuffixTree("banana")
        self.assertEqual(st.search("ban"), [0])
    
    def test_search_not_found(self):
        """测试未找到"""
        st = SuffixTree("banana")
        self.assertEqual(st.search("xyz"), [])
    
    def test_search_full_string(self):
        """测试完整字符串搜索"""
        st = SuffixTree("banana")
        self.assertEqual(st.search("banana"), [0])
    
    def test_search_single_char(self):
        """测试单字符搜索"""
        st = SuffixTree("banana")
        self.assertEqual(sorted(st.search("a")), [1, 3, 5])
    
    def test_search_overlapping(self):
        """测试重叠模式"""
        st = SuffixTree("aaaaa")
        # "aa" 在位置 0, 1, 2, 3 出现
        self.assertEqual(sorted(st.search("aa")), [0, 1, 2, 3])
    
    def test_search_empty_pattern(self):
        """测试空模式"""
        st = SuffixTree("abc")
        # 空模式匹配所有位置（不包括 $ 终止符）
        result = st.search("")
        self.assertEqual(len(result), 3)


class TestContainsAndCount(unittest.TestCase):
    """包含检查和计数测试"""
    
    def test_contains_true(self):
        """测试包含 - True"""
        st = SuffixTree("hello world")
        self.assertTrue(st.contains("hello"))
        self.assertTrue(st.contains("world"))
        self.assertTrue(st.contains("o w"))
    
    def test_contains_false(self):
        """测试包含 - False"""
        st = SuffixTree("hello world")
        self.assertFalse(st.contains("helloo"))
        self.assertFalse(st.contains("world!"))
    
    def test_count_occurrences(self):
        """测试计数"""
        st = SuffixTree("ababab")
        self.assertEqual(st.count_occurrences("ab"), 3)
        self.assertEqual(st.count_occurrences("aba"), 2)
        self.assertEqual(st.count_occurrences("xyz"), 0)


class TestLongestRepeatedSubstring(unittest.TestCase):
    """最长重复子串测试"""
    
    def test_longest_repeated_simple(self):
        """测试简单最长重复子串"""
        st = SuffixTree("banana")
        lrs = st.longest_repeated_substring()
        self.assertEqual(lrs, "ana")
    
    def test_longest_repeated_none(self):
        """测试无重复子串"""
        st = SuffixTree("abcdef")
        lrs = st.longest_repeated_substring()
        self.assertEqual(lrs, "")
    
    def test_longest_repeated_all_same(self):
        """测试全部相同字符"""
        st = SuffixTree("aaaaaa")
        lrs = st.longest_repeated_substring()
        self.assertEqual(lrs, "aaaaa")
    
    def test_longest_repeated_multiple(self):
        """测试多个重复子串"""
        st = SuffixTree("abcabcabc")
        lrs = st.longest_repeated_substring()
        self.assertEqual(lrs, "abcabc")


class TestAllRepeatedSubstrings(unittest.TestCase):
    """所有重复子串测试"""
    
    def test_all_repeated(self):
        """测试获取所有重复子串"""
        st = SuffixTree("banana")
        repeated = st.all_repeated_substrings(min_length=2)
        self.assertIn("ana", repeated)
        self.assertIn("an", repeated)
        self.assertIn("na", repeated)
    
    def test_all_repeated_min_length(self):
        """测试最小长度过滤"""
        st = SuffixTree("banana")
        repeated = st.all_repeated_substrings(min_length=3)
        for s in repeated:
            self.assertGreaterEqual(len(s), 3)


class TestGeneralizedSuffixTree(unittest.TestCase):
    """广义后缀树测试"""
    
    def test_build_two_strings(self):
        """测试构建两个字符串"""
        gst = GeneralizedSuffixTree(["hello", "world"])
        self.assertIsNotNone(gst.root)
    
    def test_longest_common_simple(self):
        """测试最长公共子串"""
        gst = GeneralizedSuffixTree(["abcdef", "defghi"])
        lcs = gst.longest_common_substring()
        self.assertEqual(lcs, "def")
    
    def test_longest_common_none(self):
        """测试无公共子串"""
        gst = GeneralizedSuffixTree(["abc", "xyz"])
        lcs = gst.longest_common_substring()
        self.assertEqual(lcs, "")
    
    def test_longest_common_multiple(self):
        """测试多个公共子串"""
        gst = GeneralizedSuffixTree(["abcXYZdef", "XYZ123"])
        lcs = gst.longest_common_substring()
        self.assertEqual(lcs, "XYZ")
    
    def test_all_common_substrings(self):
        """测试所有公共子串"""
        gst = GeneralizedSuffixTree(["abcdef", "abcxyz"])
        common = gst.all_common_substrings(min_length=2)
        self.assertIn("abc", common)
    
    def test_three_strings(self):
        """测试三个字符串"""
        gst = GeneralizedSuffixTree(["hello world", "world peace", "worldwide"])
        lcs = gst.longest_common_substring()
        self.assertEqual(lcs, "world")


class TestConvenienceFunctions(unittest.TestCase):
    """便捷函数测试"""
    
    def test_find_all_occurrences(self):
        """测试查找所有出现"""
        result = find_all_occurrences("banana", "ana")
        self.assertEqual(sorted(result), [1, 3])
    
    def test_longest_repeated_substring_func(self):
        """测试最长重复子串函数"""
        result = longest_repeated_substring("mississippi")
        self.assertEqual(result, "issi")
    
    def test_longest_common_substring_func(self):
        """测试最长公共子串函数"""
        result = longest_common_substring("programming", "programmer")
        self.assertEqual(result, "programm")
    
    def test_count_occurrences_func(self):
        """测试计数函数"""
        result = count_occurrences("test test test", "test")
        self.assertEqual(result, 3)


class TestSuffixArray(unittest.TestCase):
    """后缀数组测试"""
    
    def test_build_suffix_array(self):
        """测试构建后缀数组"""
        sa = build_suffix_array("banana")
        self.assertEqual(len(sa), 7)  # 包括 $
    
    def test_suffix_array_sorted(self):
        """测试后缀数组排序正确性"""
        text = "banana"
        sa = build_suffix_array(text)
        suffixes = [text[i:] for i in sa]
        # 验证后缀按字典序排列
        self.assertEqual(suffixes, sorted(suffixes))


class TestEdgeCases(unittest.TestCase):
    """边界情况测试"""
    
    def test_unicode(self):
        """测试 Unicode 字符"""
        st = SuffixTree("你好世界你好")
        self.assertEqual(sorted(st.search("你好")), [0, 4])
    
    def test_special_chars(self):
        """测试特殊字符"""
        st = SuffixTree("a$b$c$a$")
        self.assertTrue(st.contains("a$"))
    
    def test_numbers(self):
        """测试数字"""
        st = SuffixTree("123456123")
        self.assertEqual(sorted(st.search("123")), [0, 6])
    
    def test_long_string(self):
        """测试长字符串"""
        text = "abc" * 1000
        st = SuffixTree(text)
        self.assertEqual(st.count_occurrences("abc"), 1000)
    
    def test_longest_palindromic_substring(self):
        """测试最长回文子串"""
        st = SuffixTree("babad")
        lps = st.longest_palindromic_substring()
        self.assertIn(lps, ["bab", "aba"])


class TestPerformance(unittest.TestCase):
    """性能测试"""
    
    def test_search_performance(self):
        """测试搜索性能"""
        import time
        
        # 构建一个较长的字符串
        text = "abcdefghij" * 1000
        st = SuffixTree(text)
        
        start = time.time()
        for _ in range(100):
            st.search("cdef")
        elapsed = time.time() - start
        
        # 应该在合理时间内完成
        self.assertLess(elapsed, 1.0)
    
    def test_build_performance(self):
        """测试构建性能"""
        import time
        
        text = "abcdefghij" * 1000
        
        start = time.time()
        st = SuffixTree(text)
        elapsed = time.time() - start
        
        # 应该在合理时间内完成
        self.assertLess(elapsed, 5.0)
        self.assertIsNotNone(st.root)


if __name__ == "__main__":
    unittest.main(verbosity=2)