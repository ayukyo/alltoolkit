"""
Suffix Array Utils 测试模块

测试后缀数组工具的所有核心功能。
"""

import unittest
from mod import (
    SuffixArray,
    SuffixArrayAdvanced,
    build_suffix_array,
    build_lcp_array,
    find_all_occurrences,
    longest_repeated_substring,
    longest_common_substring,
    count_distinct_substrings,
    pattern_exists,
)


class TestSuffixArray(unittest.TestCase):
    """测试后缀数组基本功能"""
    
    def test_build_suffix_array(self):
        """测试后缀数组构建"""
        text = "banana"
        sa = SuffixArray(text)
        
        # 后缀排序后应该是:
        # 5: a
        # 3: ana
        # 1: anana
        # 0: banana
        # 4: na
        # 2: nana
        expected = [5, 3, 1, 0, 4, 2]
        self.assertEqual(sa.suffix_array, expected)
    
    def test_build_suffix_array_empty(self):
        """测试空字符串"""
        sa = SuffixArray("")
        self.assertEqual(sa.suffix_array, [])
        self.assertEqual(sa.lcp_array, [])
    
    def test_build_suffix_array_single(self):
        """测试单字符"""
        sa = SuffixArray("a")
        self.assertEqual(sa.suffix_array, [0])
        self.assertEqual(sa.lcp_array, [0])
    
    def test_build_suffix_array_repeated(self):
        """测试重复字符"""
        sa = SuffixArray("aaaa")
        self.assertEqual(sa.suffix_array, [3, 2, 1, 0])
    
    def test_build_lcp_array(self):
        """测试LCP数组构建"""
        text = "banana"
        sa = SuffixArray(text)
        
        # LCP数组
        # SA[0]=5: "a", LCP[0]=0
        # SA[1]=3: "ana", LCP[1]=1 (与"a"的LCP)
        # SA[2]=1: "anana", LCP[2]=3 (与"ana"的LCP)
        # SA[3]=0: "banana", LCP[3]=0
        # SA[4]=4: "na", LCP[4]=0
        # SA[5]=2: "nana", LCP[5]=2 (与"na"的LCP)
        expected = [0, 1, 3, 0, 0, 2]
        self.assertEqual(sa.lcp_array, expected)
    
    def test_search_pattern(self):
        """测试模式匹配"""
        sa = SuffixArray("banana")
        
        # 查找 "ana"
        result = sa.search("ana")
        self.assertIn(1, result)  # "banana" 位置1
        self.assertIn(3, result)  # "banana" 位置3
        
        # 查找 "a"
        result = sa.search("a")
        self.assertEqual(len(result), 3)  # 位置1, 3, 5
        
        # 查找不存在
        result = sa.search("xyz")
        self.assertEqual(result, [])
    
    def test_search_pattern_full(self):
        """测试完全匹配"""
        sa = SuffixArray("banana")
        result = sa.search("banana")
        self.assertEqual(result, [0])
    
    def test_search_pattern_prefix(self):
        """测试前缀匹配"""
        sa = SuffixArray("banana")
        result = sa.search("ban")
        self.assertEqual(result, [0])
    
    def test_search_pattern_suffix(self):
        """测试后缀匹配"""
        sa = SuffixArray("banana")
        result = sa.search("nana")
        self.assertEqual(result, [2])
    
    def test_contains(self):
        """测试存在性检查"""
        sa = SuffixArray("hello world")
        self.assertTrue(sa.contains("hello"))
        self.assertTrue(sa.contains("world"))
        self.assertTrue(sa.contains("o w"))
        self.assertFalse(sa.contains("xyz"))
    
    def test_count_occurrences(self):
        """测试出现次数统计"""
        sa = SuffixArray("abababa")
        self.assertEqual(sa.count_occurrences("aba"), 3)
        self.assertEqual(sa.count_occurrences("b"), 3)
        self.assertEqual(sa.count_occurrences("a"), 4)
        self.assertEqual(sa.count_occurrences("xyz"), 0)
    
    def test_longest_repeated_substring(self):
        """测试最长重复子串"""
        sa = SuffixArray("banana")
        substring, positions = sa.longest_repeated_substring()
        self.assertEqual(substring, "ana")
        # 应该有2个不同的位置
        self.assertEqual(len(positions), 2)
        
        # 检查位置包含正确的起始点
        starts = sorted([p[0] for p in positions])
        self.assertEqual(starts, [1, 3])
    
    def test_longest_repeated_substring_no_repeat(self):
        """测试无重复子串的情况"""
        sa = SuffixArray("abcdefg")
        substring, positions = sa.longest_repeated_substring()
        self.assertEqual(substring, "")
        self.assertEqual(positions, [])
    
    def test_all_repeated_substrings(self):
        """测试所有重复子串"""
        sa = SuffixArray("abababa")
        repeats = sa.all_repeated_substrings(min_length=2)
        
        # 应该找到多个重复子串
        self.assertTrue(len(repeats) > 0)
        
        # "aba" 至少出现3次
        for substring, positions in repeats:
            if substring == "aba":
                self.assertGreaterEqual(len(positions), 3)
    
    def test_longest_common_substring(self):
        """测试最长公共子串"""
        sa = SuffixArray("programming")
        substring, positions = sa.longest_common_substring("grammatical")
        
        # "gramming" 和 "grammatical" 的公共前缀是 "gramm"
        self.assertEqual(substring, "gramm")
        self.assertEqual(positions[0], 3)  # 在 "programming" 中的位置
    
    def test_longest_common_substring_no_common(self):
        """测试无公共子串"""
        sa = SuffixArray("abcdef")
        substring, positions = sa.longest_common_substring("xyz")
        self.assertEqual(substring, "")
    
    def test_distinct_substrings_count(self):
        """测试不同子串数量"""
        # "aab" 的子串: a, a, b, aa, ab, aab
        # 不同子串: a, b, aa, ab, aab = 5
        sa = SuffixArray("aab")
        count = sa.distinct_substrings_count()
        self.assertEqual(count, 5)
    
    def test_distinct_substrings_count_no_repeat(self):
        """测试无重复字符的不同子串数量"""
        # "abc" 的子串: a, b, c, ab, bc, abc = 6
        sa = SuffixArray("abc")
        count = sa.distinct_substrings_count()
        self.assertEqual(count, 6)
    
    def test_kth_substring(self):
        """测试第k小子串"""
        sa = SuffixArray("abc")
        
        # 按字典序，前几个子串
        # a, ab, abc, b, bc, c
        self.assertEqual(sa.kth_substring(1), "a")
        self.assertEqual(sa.kth_substring(2), "ab")
        self.assertEqual(sa.kth_substring(3), "abc")
        self.assertEqual(sa.kth_substring(4), "b")
    
    def test_kth_substring_out_of_range(self):
        """测试超出范围的k"""
        sa = SuffixArray("abc")
        self.assertEqual(sa.kth_substring(0), "")
        self.assertEqual(sa.kth_substring(100), "")
    
    def test_get_suffix(self):
        """测试获取指定排名的后缀"""
        sa = SuffixArray("banana")
        
        self.assertEqual(sa.get_suffix(0), "a")
        self.assertEqual(sa.get_suffix(1), "ana")
        self.assertEqual(sa.get_suffix(5), "nana")
    
    def test_get_suffix_invalid(self):
        """测试无效排名"""
        sa = SuffixArray("abc")
        self.assertEqual(sa.get_suffix(-1), "")
        self.assertEqual(sa.get_suffix(10), "")
    
    def test_get_rank(self):
        """测试获取排名"""
        sa = SuffixArray("banana")
        
        # "a" 排名0, 起始位置5
        self.assertEqual(sa.get_rank(5), 0)
        # "ana" 排名1, 起始位置3
        self.assertEqual(sa.get_rank(3), 1)
    
    def test_compare_substrings(self):
        """测试子串比较"""
        sa = SuffixArray("banana")
        
        # "an" vs "ba"
        self.assertEqual(sa.compare_substrings(1, 0, 2), -1)  # "an" < "ba"
        # "na" vs "na"
        self.assertEqual(sa.compare_substrings(2, 4, 2), 0)
    
    def test_complex_text(self):
        """测试复杂文本"""
        text = "mississippi"
        sa = SuffixArray(text)
        
        # 查找 "issi"
        result = sa.search("issi")
        self.assertEqual(len(result), 2)
        self.assertIn(1, result)  # mississippi
        self.assertIn(4, result)  # mississippi
    
    def test_unicode_support(self):
        """测试Unicode支持"""
        text = "你好世界你好"
        sa = SuffixArray(text)
        
        result = sa.search("你好")
        self.assertEqual(len(result), 2)


class TestSuffixArrayAdvanced(unittest.TestCase):
    """测试后缀数组高级功能"""
    
    def test_lcp_between_suffixes(self):
        """测试两个后缀的LCP计算"""
        sa = SuffixArrayAdvanced("banana")
        
        # "banana" 和 "anana" 的 LCP = 0
        self.assertEqual(sa.lcp_between_suffixes(0, 1), 0)
        
        # "anana" 和 "ana" 的 LCP = 3
        self.assertEqual(sa.lcp_between_suffixes(1, 3), 3)
        
        # 相同后缀
        self.assertEqual(sa.lcp_between_suffixes(0, 0), 6)
    
    def test_advanced_search(self):
        """测试高级搜索功能"""
        sa = SuffixArrayAdvanced("abracadabra")
        
        self.assertEqual(sa.count_substring_occurrences("abra"), 2)
        self.assertEqual(sa.count_substring_occurrences("cad"), 1)
        self.assertEqual(sa.count_substring_occurrences("xyz"), 0)
    
    def test_longest_repeated_complex(self):
        """测试复杂文本的最长重复子串"""
        sa = SuffixArrayAdvanced("ABABABA")
        substring, positions = sa.longest_repeated_substring()
        
        # "ABABA" 中最长重复子串是 "ABABA"（位置0和2）或 "BABA"（位置1和3）
        # 实际最长是 "ABABA"，长度5，但 LCP 计算会给出实际的重复长度
        self.assertGreaterEqual(len(substring), 4)
        self.assertEqual(len(positions), 2)
    
    def test_pattern_edge_cases(self):
        """测试模式匹配边界情况"""
        sa = SuffixArrayAdvanced("aaa")
        
        # search 返回的结果是按后缀字典序排序的位置
        # 对于 "aaa"，后缀排序后位置顺序是 [2, 1, 0] (a, aa, aaa)
        self.assertEqual(sorted(sa.search("a")), [0, 1, 2])
        self.assertEqual(sorted(sa.search("aa")), [0, 1])
        self.assertEqual(sa.search("aaa"), [0])
        self.assertEqual(sa.search("aaaa"), [])


class TestConvenienceFunctions(unittest.TestCase):
    """测试便捷函数"""
    
    def test_build_suffix_array_func(self):
        """测试build_suffix_array函数"""
        result = build_suffix_array("banana")
        self.assertEqual(result, [5, 3, 1, 0, 4, 2])
    
    def test_build_lcp_array_func(self):
        """测试build_lcp_array函数"""
        result = build_lcp_array("banana")
        self.assertEqual(result, [0, 1, 3, 0, 0, 2])
    
    def test_find_all_occurrences_func(self):
        """测试find_all_occurrences函数"""
        result = find_all_occurrences("banana", "ana")
        self.assertIn(1, result)
        self.assertIn(3, result)
    
    def test_longest_repeated_substring_func(self):
        """测试longest_repeated_substring函数"""
        substring, positions = longest_repeated_substring("banana")
        self.assertEqual(substring, "ana")
    
    def test_longest_common_substring_func(self):
        """测试longest_common_substring函数"""
        substring, positions = longest_common_substring("programming", "grammatical")
        # "gramming" 和 "grammatical" 的公共前缀是 "gramm"
        self.assertEqual(substring, "gramm")
    
    def test_count_distinct_substrings_func(self):
        """测试count_distinct_substrings函数"""
        count = count_distinct_substrings("aab")
        self.assertEqual(count, 5)
    
    def test_pattern_exists_func(self):
        """测试pattern_exists函数"""
        self.assertTrue(pattern_exists("hello world", "world"))
        self.assertFalse(pattern_exists("hello world", "xyz"))


class TestEdgeCases(unittest.TestCase):
    """测试边界情况"""
    
    def test_empty_string(self):
        """测试空字符串"""
        sa = SuffixArray("")
        
        self.assertEqual(sa.search("a"), [])
        self.assertEqual(sa.longest_repeated_substring(), ("", []))
        self.assertEqual(sa.distinct_substrings_count(), 0)
    
    def test_single_character(self):
        """测试单字符"""
        sa = SuffixArray("a")
        
        self.assertEqual(sa.search("a"), [0])
        self.assertTrue(sa.contains("a"))
        self.assertEqual(sa.distinct_substrings_count(), 1)
    
    def test_all_same_characters(self):
        """测试全相同字符"""
        sa = SuffixArray("aaaaa")
        
        self.assertEqual(sa.search("a"), [4, 3, 2, 1, 0])
        self.assertEqual(sa.search("aaa"), [2, 1, 0])
        self.assertEqual(sa.distinct_substrings_count(), 5)  # a, aa, aaa, aaaa, aaaaa
    
    def test_very_long_string(self):
        """测试长字符串"""
        # 创建一个较长的字符串
        text = "abc" * 100
        sa = SuffixArray(text)
        
        self.assertEqual(sa.count_occurrences("abc"), 100)
        self.assertTrue(sa.contains("abcabc"))
    
    def test_special_characters(self):
        """测试特殊字符"""
        text = "a\nb\tc"
        sa = SuffixArray(text)
        
        self.assertTrue(sa.contains("\n"))
        self.assertTrue(sa.contains("\t"))
    
    def test_numbers_in_string(self):
        """测试包含数字的字符串"""
        text = "abc123abc456"
        sa = SuffixArray(text)
        
        self.assertEqual(sa.search("abc"), [0, 6])
        self.assertEqual(sa.search("123"), [3])
        # "456" 在位置 9（abc123abc 是 9 个字符）
        self.assertEqual(sorted(sa.search("456")), [9])
    
    def test_mixed_case(self):
        """测试大小写混合"""
        text = "AbCabcABC"
        sa = SuffixArray(text)
        
        # 大小写敏感
        self.assertEqual(sa.search("abc"), [3])
        self.assertEqual(sa.search("ABC"), [6])
        self.assertEqual(sa.search("AbC"), [0])


class TestPerformance(unittest.TestCase):
    """测试性能相关"""
    
    def test_large_text(self):
        """测试较大文本"""
        # 创建一个包含重复模式的文本
        text = "abcdefghij" * 100
        sa = SuffixArray(text)
        
        # 应该能正确处理
        self.assertEqual(sa.count_occurrences("abcdefghij"), 100)
        self.assertTrue(sa.contains("cdefghijab"))
    
    def test_multiple_searches(self):
        """测试多次搜索"""
        text = "the quick brown fox jumps over the lazy dog"
        sa = SuffixArray(text)
        
        patterns = ["the", "quick", "brown", "fox", "dog", "cat"]
        results = [sa.search(p) for p in patterns]
        
        self.assertEqual(len(results[0]), 2)  # "the" 出现2次
        self.assertTrue(sa.contains("fox"))
        self.assertFalse(sa.contains("cat"))


if __name__ == "__main__":
    unittest.main(verbosity=2)