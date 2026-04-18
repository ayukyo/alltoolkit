"""
Rolling Hash Utils 测试模块

测试覆盖：
- RollingHash 基础操作
- DoubleRollingHash 双重哈希
- RabinKarp 字符串匹配
- MultiPatternMatcher 多模式匹配
- RollingHashIterator 迭代器
- DuplicateDetector 重复检测
- FileFingerprint 文件指纹
- 便捷函数
- 边界情况
"""

import unittest
from mod import (
    RollingHash,
    DoubleRollingHash,
    RabinKarp,
    MultiPatternMatcher,
    RollingHashIterator,
    DuplicateDetector,
    FileFingerprint,
    find_all_occurrences,
    find_first_occurrence,
    compute_rolling_hash,
    longest_repeated_substring,
)


class TestRollingHash(unittest.TestCase):
    """RollingHash 类测试"""
    
    def test_basic_hash(self):
        """测试基础哈希计算"""
        rh = RollingHash(3)
        rh.extend("abc")
        self.assertTrue(rh.is_full())
        self.assertEqual(rh.get_window(), "abc")
    
    def test_append_single(self):
        """测试单字符添加"""
        rh = RollingHash(3)
        h1 = rh.append('a')
        self.assertFalse(rh.is_full())
        h2 = rh.append('b')
        h3 = rh.append('c')
        self.assertTrue(rh.is_full())
        
        # 添加第四个字符后，窗口应该滑动
        h4 = rh.append('d')
        self.assertEqual(rh.get_window(), "bcd")
    
    def test_window_slide(self):
        """测试窗口滑动"""
        rh = RollingHash(4)
        rh.extend("abcd")
        self.assertEqual(rh.get_window(), "abcd")
        
        rh.append('e')
        self.assertEqual(rh.get_window(), "bcde")
        
        rh.append('f')
        self.assertEqual(rh.get_window(), "cdef")
    
    def test_consistent_hash(self):
        """测试相同内容产生相同哈希"""
        rh1 = RollingHash(5)
        rh2 = RollingHash(5)
        
        rh1.extend("hello")
        rh2.extend("hello")
        
        self.assertEqual(rh1.get_hash(), rh2.get_hash())
    
    def test_different_content_different_hash(self):
        """测试不同内容产生不同哈希"""
        rh1 = RollingHash(5)
        rh2 = RollingHash(5)
        
        rh1.extend("hello")
        rh2.extend("world")
        
        self.assertNotEqual(rh1.get_hash(), rh2.get_hash())
    
    def test_reset(self):
        """测试重置功能"""
        rh = RollingHash(3)
        rh.extend("abc")
        self.assertTrue(rh.is_full())
        
        rh.reset()
        self.assertFalse(rh.is_full())
        self.assertEqual(rh.get_hash(), 0)
        self.assertEqual(rh.get_window(), "")
    
    def test_invalid_window_size(self):
        """测试无效窗口大小"""
        with self.assertRaises(ValueError):
            RollingHash(0)
        
        with self.assertRaises(ValueError):
            RollingHash(-1)
    
    def test_unicode_support(self):
        """测试 Unicode 支持"""
        rh = RollingHash(3)
        rh.extend("你好世")
        self.assertEqual(rh.get_window(), "你好世")
        
        rh.append('界')
        self.assertEqual(rh.get_window(), "好世界")
    
    def test_empty_append(self):
        """测试空字符串扩展"""
        rh = RollingHash(3)
        result = rh.extend("")
        self.assertEqual(rh.get_window(), "")
        self.assertEqual(result, 0)


class TestDoubleRollingHash(unittest.TestCase):
    """DoubleRollingHash 类测试"""
    
    def test_basic(self):
        """测试双重哈希基础功能"""
        drh = DoubleRollingHash(3)
        h = drh.extend("abc")
        
        self.assertIsInstance(h, tuple)
        self.assertEqual(len(h), 2)
        self.assertTrue(drh.is_full())
    
    def test_consistency(self):
        """测试一致性"""
        drh1 = DoubleRollingHash(4)
        drh2 = DoubleRollingHash(4)
        
        drh1.extend("test")
        drh2.extend("test")
        
        self.assertEqual(drh1.get_hash(), drh2.get_hash())
    
    def test_collision_resistance(self):
        """测试碰撞抵抗"""
        drh1 = DoubleRollingHash(5)
        drh2 = DoubleRollingHash(5)
        
        drh1.extend("hello")
        drh2.extend("world")
        
        # 双重哈希几乎不可能同时碰撞
        self.assertNotEqual(drh1.get_hash(), drh2.get_hash())
    
    def test_reset(self):
        """测试重置"""
        drh = DoubleRollingHash(3)
        drh.extend("abc")
        drh.reset()
        
        self.assertEqual(drh.get_hash(), (0, 0))
    
    def test_window_slide(self):
        """测试窗口滑动"""
        drh = DoubleRollingHash(3)
        drh.extend("abc")
        drh.append('d')
        
        self.assertEqual(drh.get_window(), "bcd")


class TestRabinKarp(unittest.TestCase):
    """RabinKarp 类测试"""
    
    def test_find_all(self):
        """测试查找所有匹配"""
        rk = RabinKarp("ab")
        text = "abcabdabeab"  # "ab" 在位置 0, 3, 6, 9
        
        matches = rk.find_all(text)
        self.assertEqual(matches, [0, 3, 6, 9])
    
    def test_find_first(self):
        """测试查找第一个匹配"""
        rk = RabinKarp("world")
        text = "hello world"
        
        pos = rk.find_first(text)
        self.assertEqual(pos, 6)
    
    def test_find_first_not_found(self):
        """测试未找到"""
        rk = RabinKarp("xyz")
        text = "hello world"
        
        pos = rk.find_first(text)
        self.assertIsNone(pos)
    
    def test_count(self):
        """测试计数"""
        rk = RabinKarp("aa")
        text = "aaaa"
        
        # "aaaa" 中 "aa" 出现在位置 0, 1, 2
        count = rk.count(text)
        self.assertEqual(count, 3)
    
    def test_contains(self):
        """测试包含检查"""
        rk = RabinKarp("test")
        
        self.assertTrue(rk.contains("this is a test"))
        self.assertFalse(rk.contains("no match here"))
    
    def test_empty_pattern(self):
        """测试空模式"""
        with self.assertRaises(ValueError):
            RabinKarp("")
    
    def test_pattern_longer_than_text(self):
        """测试模式比文本长"""
        rk = RabinKarp("hello world")
        matches = rk.find_all("hi")
        self.assertEqual(matches, [])
    
    def test_exact_match(self):
        """测试完全匹配"""
        rk = RabinKarp("exact")
        matches = rk.find_all("exact")
        self.assertEqual(matches, [0])
    
    def test_overlapping_patterns(self):
        """测试重叠模式"""
        rk = RabinKarp("aa")
        matches = rk.find_all("aaa")
        self.assertEqual(matches, [0, 1])
    
    def test_unicode_pattern(self):
        """测试 Unicode 模式"""
        rk = RabinKarp("世界")
        text = "你好世界，世界和平"
        
        matches = rk.find_all(text)
        self.assertEqual(matches, [2, 5])
    
    def test_long_text(self):
        """测试长文本"""
        rk = RabinKarp("needle")
        text = "haystack" * 1000 + "needle" + "haystack" * 1000
        
        matches = rk.find_all(text)
        self.assertEqual(len(matches), 1)
        self.assertEqual(text[matches[0]:matches[0] + 6], "needle")


class TestMultiPatternMatcher(unittest.TestCase):
    """MultiPatternMatcher 类测试"""
    
    def test_find_all(self):
        """测试多模式查找"""
        matcher = MultiPatternMatcher(["cat", "dog", "bird"])
        text = "cat and dog are friends, but bird is alone"
        
        results = matcher.find_all(text)
        
        self.assertIn("cat", results)
        self.assertIn("dog", results)
        self.assertIn("bird", results)
        self.assertEqual(results["cat"], [0])
        self.assertEqual(results["dog"], [8])
        self.assertEqual(results["bird"], [29])  # bird 在位置 29
    
    def test_find_any(self):
        """测试任意匹配"""
        matcher = MultiPatternMatcher(["apple", "banana", "cherry"])
        
        result = matcher.find_any("I like banana")
        self.assertIsNotNone(result)
        self.assertEqual(result[0], "banana")
        self.assertEqual(result[1], 7)
    
    def test_find_any_none(self):
        """测试无匹配"""
        matcher = MultiPatternMatcher(["apple", "banana"])
        
        result = matcher.find_any("orange juice")
        self.assertIsNone(result)
    
    def test_count_all(self):
        """测试计数"""
        matcher = MultiPatternMatcher(["a", "b"])
        text = "ababab"
        
        counts = matcher.count_all(text)
        self.assertEqual(counts["a"], 3)
        self.assertEqual(counts["b"], 3)
    
    def test_empty_patterns(self):
        """测试空模式列表"""
        with self.assertRaises(ValueError):
            MultiPatternMatcher([])
    
    def test_empty_pattern_in_list(self):
        """测试列表中包含空模式"""
        with self.assertRaises(ValueError):
            MultiPatternMatcher(["a", "", "b"])
    
    def test_different_lengths(self):
        """测试不同长度的模式"""
        matcher = MultiPatternMatcher(["a", "ab", "abc"])
        text = "abc"  # "a" 在位置 0，"ab" 在位置 0，"abc" 在位置 0
        
        results = matcher.find_all(text)
        self.assertEqual(results["a"], [0])  # 只有位置 0
        self.assertEqual(results["ab"], [0])
        self.assertEqual(results["abc"], [0])
    
    def test_no_matches(self):
        """测试无匹配情况"""
        matcher = MultiPatternMatcher(["xyz", "uvw"])
        text = "hello world"
        
        results = matcher.find_all(text)
        self.assertEqual(results, {})


class TestRollingHashIterator(unittest.TestCase):
    """RollingHashIterator 类测试"""
    
    def test_iteration(self):
        """测试迭代"""
        text = "abcdef"
        window_size = 3
        iterator = RollingHashIterator(text, window_size, double_hash=False)
        
        results = list(iterator)
        self.assertEqual(len(results), 4)  # 6 - 3 + 1 = 4
        
        # 验证窗口内容
        windows = [r[2] for r in results]
        self.assertEqual(windows, ["abc", "bcd", "cde", "def"])
    
    def test_double_hash_iteration(self):
        """测试双重哈希迭代"""
        text = "hello"
        window_size = 2
        iterator = RollingHashIterator(text, window_size, double_hash=True)
        
        results = list(iterator)
        self.assertEqual(len(results), 4)
        
        # 哈希值应该是元组
        for pos, hash_val, window in results:
            self.assertIsInstance(hash_val, tuple)
            self.assertEqual(len(hash_val), 2)
    
    def test_text_shorter_than_window(self):
        """测试文本比窗口短"""
        text = "ab"
        window_size = 5
        iterator = RollingHashIterator(text, window_size)
        
        results = list(iterator)
        self.assertEqual(results, [])
    
    def test_exact_window_size(self):
        """测试文本长度等于窗口大小"""
        text = "abc"
        window_size = 3
        iterator = RollingHashIterator(text, window_size, double_hash=False)
        
        results = list(iterator)
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0][2], "abc")


class TestDuplicateDetector(unittest.TestCase):
    """DuplicateDetector 类测试"""
    
    def test_find_duplicates(self):
        """测试查找重复"""
        detector = DuplicateDetector(min_length=3)
        text = "abcabcxyz"
        
        duplicates = detector.find_duplicates(text)
        
        self.assertIn("abc", duplicates)
        self.assertEqual(duplicates["abc"], [0, 3])
    
    def test_no_duplicates(self):
        """测试无重复"""
        detector = DuplicateDetector(min_length=3)
        text = "abcdefgh"
        
        duplicates = detector.find_duplicates(text)
        self.assertEqual(duplicates, {})
    
    def test_has_duplicates(self):
        """测试重复检测"""
        detector = DuplicateDetector(min_length=3)
        
        self.assertTrue(detector.has_duplicates("abcabc"))
        self.assertFalse(detector.has_duplicates("abcdef"))
    
    def test_count_unique_substrings(self):
        """测试唯一子串计数"""
        detector = DuplicateDetector(min_length=3)
        
        # "abcabc" 长度为 3 的子串: "abc", "bca", "cab", "abc"
        # 唯一的: "abc", "bca", "cab"
        count = detector.count_unique_substrings("abcabc")
        self.assertEqual(count, 3)
    
    def test_invalid_min_length(self):
        """测试无效最小长度"""
        with self.assertRaises(ValueError):
            DuplicateDetector(min_length=0)
        
        with self.assertRaises(ValueError):
            DuplicateDetector(min_length=-1)
    
    def test_overlapping_duplicates(self):
        """测试重叠重复"""
        detector = DuplicateDetector(min_length=2)
        text = "aaaa"  # "aa" 出现在位置 0, 1, 2
        
        duplicates = detector.find_duplicates(text)
        self.assertIn("aa", duplicates)
        self.assertEqual(duplicates["aa"], [0, 1, 2])
    
    def test_short_text(self):
        """测试短文本"""
        detector = DuplicateDetector(min_length=5)
        text = "abc"
        
        duplicates = detector.find_duplicates(text)
        self.assertEqual(duplicates, {})


class TestFileFingerprint(unittest.TestCase):
    """FileFingerprint 类测试"""
    
    def test_fingerprint_string(self):
        """测试字符串指纹"""
        fp = FileFingerprint(chunk_size=4)
        
        fingerprint1 = fp.fingerprint_string("hello world")
        fingerprint2 = fp.fingerprint_string("hello world")
        
        self.assertEqual(fingerprint1, fingerprint2)
    
    def test_fingerprint_bytes(self):
        """测试字节指纹"""
        fp = FileFingerprint(chunk_size=4)
        
        fingerprint1 = fp.fingerprint_bytes(b"hello world")
        fingerprint2 = fp.fingerprint_bytes(b"hello world")
        
        self.assertEqual(fingerprint1, fingerprint2)
    
    def test_different_fingerprints(self):
        """测试不同内容产生不同指纹"""
        fp = FileFingerprint(chunk_size=4)
        
        fp1 = fp.fingerprint_string("hello world")
        fp2 = fp.fingerprint_string("goodbye world")
        
        self.assertNotEqual(fp1, fp2)
    
    def test_similarity_identical(self):
        """测试完全相同的相似度"""
        fp = FileFingerprint(chunk_size=4)
        
        fp1 = fp.fingerprint_string("hello world hello")
        similarity = fp.similarity(fp1, fp1)
        
        self.assertEqual(similarity, 1.0)
    
    def test_similarity_different(self):
        """测试不同内容的相似度"""
        fp = FileFingerprint(chunk_size=4)
        
        fp1 = fp.fingerprint_string("hello world")
        fp2 = fp.fingerprint_string("goodbye world")
        similarity = fp.similarity(fp1, fp2)
        
        # 不完全相同，但可能有部分相似
        self.assertGreaterEqual(similarity, 0.0)
        self.assertLessEqual(similarity, 1.0)
    
    def test_jaccard_distance(self):
        """测试 Jaccard 距离"""
        fp = FileFingerprint(chunk_size=4)
        
        fp1 = fp.fingerprint_string("hello world")
        fp2 = fp.fingerprint_string("hello world")
        distance = fp.jaccard_distance(fp1, fp2)
        
        self.assertEqual(distance, 0.0)  # 完全相同
    
    def test_short_content(self):
        """测试短内容"""
        fp = FileFingerprint(chunk_size=100)
        fingerprint = fp.fingerprint_string("hi")
        
        # 短于块大小的内容返回单个哈希
        self.assertEqual(len(fingerprint), 1)


class TestConvenienceFunctions(unittest.TestCase):
    """便捷函数测试"""
    
    def test_find_all_occurrences(self):
        """测试查找所有出现位置"""
        text = "ababab"
        pattern = "ab"
        
        matches = find_all_occurrences(text, pattern)
        self.assertEqual(matches, [0, 2, 4])
    
    def test_find_first_occurrence(self):
        """测试查找第一个出现位置"""
        text = "hello world"
        pattern = "world"
        
        pos = find_first_occurrence(text, pattern)
        self.assertEqual(pos, 6)
    
    def test_find_first_occurrence_not_found(self):
        """测试未找到第一个出现"""
        pos = find_first_occurrence("hello", "xyz")
        self.assertIsNone(pos)
    
    def test_compute_rolling_hash(self):
        """测试计算滚动哈希"""
        text = "abcd"
        window_size = 2
        
        results = compute_rolling_hash(text, window_size)
        
        self.assertEqual(len(results), 3)
        windows = [r[1] for r in results]
        self.assertEqual(windows, ["ab", "bc", "cd"])
    
    def test_longest_repeated_substring(self):
        """测试最长重复子串"""
        text = "abcdefabcdef"
        
        result = longest_repeated_substring(text, min_length=3)
        self.assertEqual(result, "abcdef")
    
    def test_longest_repeated_substring_none(self):
        """测试无重复子串"""
        text = "abcdefgh"
        
        result = longest_repeated_substring(text)
        self.assertIsNone(result)


class TestEdgeCases(unittest.TestCase):
    """边界情况测试"""
    
    def test_single_char_window(self):
        """测试单字符窗口"""
        rh = RollingHash(1)
        rh.append('a')
        self.assertEqual(rh.get_window(), "a")
        rh.append('b')
        self.assertEqual(rh.get_window(), "b")
    
    def test_large_window(self):
        """测试大窗口"""
        rh = RollingHash(10000)
        text = "a" * 10000
        rh.extend(text)
        self.assertTrue(rh.is_full())
    
    def test_repeated_chars(self):
        """测试重复字符"""
        rk = RabinKarp("aaa")
        text = "aaaaaaaa"
        
        matches = rk.find_all(text)
        self.assertEqual(len(matches), 6)  # 位置 0-5
    
    def test_special_chars(self):
        """测试特殊字符"""
        rk = RabinKarp("\n\t\r")
        text = "line1\n\t\rline2"
        
        matches = rk.find_all(text)
        self.assertEqual(len(matches), 1)
    
    def test_binary_data_fingerprint(self):
        """测试二进制数据指纹"""
        fp = FileFingerprint(chunk_size=4)
        
        data = bytes(range(256))
        fingerprint = fp.fingerprint_bytes(data)
        
        self.assertIsInstance(fingerprint, list)
        self.assertGreater(len(fingerprint), 0)
    
    def test_consecutive_appends(self):
        """测试连续添加"""
        rh = RollingHash(5)
        
        for char in "hello":
            rh.append(char)
        
        self.assertEqual(rh.get_window(), "hello")
        
        for char in "world":
            rh.append(char)
        
        self.assertEqual(rh.get_window(), "world")


class TestPerformance(unittest.TestCase):
    """性能相关测试"""
    
    def test_large_text_search(self):
        """测试大文本搜索"""
        # 生成大文本
        text = "ab" * 50000 + "needle" + "cd" * 50000
        
        rk = RabinKarp("needle")
        matches = rk.find_all(text)
        
        self.assertEqual(len(matches), 1)
    
    def test_multiple_patterns_search(self):
        """测试多模式搜索"""
        patterns = ["pattern1", "pattern2", "pattern3", "pattern4", "pattern5"]
        matcher = MultiPatternMatcher(patterns)
        
        text = "some text pattern2 in the middle pattern4 at the end"
        results = matcher.find_all(text)
        
        self.assertIn("pattern2", results)
        self.assertIn("pattern4", results)
    
    def test_duplicate_detection_large(self):
        """测试大文本重复检测"""
        # 生成有重复的大文本
        text = "unique_prefix_" + ("repeat" * 1000) + "_unique_suffix"
        
        detector = DuplicateDetector(min_length=6)
        duplicates = detector.find_duplicates(text)
        
        self.assertIn("repeat", duplicates)


if __name__ == '__main__':
    unittest.main(verbosity=2)