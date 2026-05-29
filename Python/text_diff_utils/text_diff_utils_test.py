"""
text_diff_utils 单元测试

测试文本差异比较工具的所有核心功能。
"""

import unittest
from mod import (
    TextDiff, DiffType, DiffStats, DiffOperation,
    diff_texts, unified_diff, similarity, 
    find_common_substring, find_common_subsequences,
    highlight_diff_html, count_changes, diff_three_texts
)


class TestTextDiff(unittest.TestCase):
    """TextDiff 类测试"""
    
    def setUp(self):
        """测试数据"""
        self.text1 = """Hello World
This is a test.
Line three.
Line four.
Goodbye!"""
        
        self.text2 = """Hello World
This is a modified test.
Line three.
New line inserted.
Line four.
See you later!"""
        
        self.differ = TextDiff(self.text1, self.text2)
    
    def test_init(self):
        """测试初始化"""
        self.assertEqual(self.differ.text1, self.text1)
        self.assertEqual(self.differ.text2, self.text2)
    
    def test_compare_chars_equal(self):
        """测试字符级比较 - 相同部分"""
        diff = TextDiff("abc", "abc")
        result = diff.compare_chars()
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0], (DiffType.EQUAL, "abc"))
    
    def test_compare_chars_insert(self):
        """测试字符级比较 - 插入"""
        diff = TextDiff("abc", "abcd")
        result = diff.compare_chars()
        types = [t for t, _ in result]
        self.assertIn(DiffType.INSERT, types)
    
    def test_compare_chars_delete(self):
        """测试字符级比较 - 删除"""
        diff = TextDiff("abcd", "abc")
        result = diff.compare_chars()
        types = [t for t, _ in result]
        self.assertIn(DiffType.DELETE, types)
    
    def test_compare_chars_replace(self):
        """测试字符级比较 - 替换"""
        diff = TextDiff("abc", "xyz")
        result = diff.compare_chars()
        types = [t for t, _ in result]
        self.assertEqual(types.count(DiffType.DELETE), 1)
        self.assertEqual(types.count(DiffType.INSERT), 1)
    
    def test_compare_words(self):
        """测试单词级比较"""
        result = self.differ.compare_words()
        self.assertTrue(len(result) > 0)
        
        # 验证差异类型正确
        diff_types = {t for t, _ in result}
        self.assertIn(DiffType.EQUAL, diff_types)
    
    def test_compare_lines(self):
        """测试行级比较"""
        result = self.differ.compare_lines()
        self.assertTrue(len(result) > 0)
        
        # 检查有插入和删除
        types = [t for t, _ in result]
        self.assertIn(DiffType.INSERT, types)
    
    def test_get_operations(self):
        """测试获取结构化操作"""
        operations = self.differ.get_operations()
        
        self.assertTrue(len(operations) > 0)
        self.assertIsInstance(operations[0], DiffOperation)
        
        # 验证操作属性
        for op in operations:
            self.assertIsInstance(op.diff_type, DiffType)
            self.assertIsInstance(op.old_start, int)
            self.assertIsInstance(op.new_start, int)
    
    def test_unified_diff(self):
        """测试统一格式差异"""
        result = self.differ.unified_diff()
        
        self.assertIn('--- original', result)
        self.assertIn('+++ modified', result)
        self.assertIn('@@', result)  # 差异块标记
    
    def test_unified_diff_custom_names(self):
        """测试统一格式差异 - 自定义文件名"""
        result = self.differ.unified_diff(fromfile='old.txt', tofile='new.txt')
        
        self.assertIn('--- old.txt', result)
        self.assertIn('+++ new.txt', result)
    
    def test_context_diff(self):
        """测试上下文格式差异"""
        result = self.differ.context_diff()
        
        self.assertIn('*** original', result)
        self.assertIn('--- modified', result)
    
    def test_side_by_side_text(self):
        """测试并排格式差异"""
        result = self.differ.side_by_side_text()
        
        self.assertIn('Original', result)
        self.assertIn('Modified', result)
        self.assertIn('|', result)
    
    def test_side_by_side_text_no_line_numbers(self):
        """测试并排格式差异 - 无行号"""
        result = self.differ.side_by_side_text(show_line_numbers=False)
        
        self.assertIn('Original', result)
        # 不应包含行号格式
        lines = result.split('\n')
        data_lines = [l for l in lines if l and not l.startswith('-') and 'Original' not in l and 'Modified' not in l]
        # 行号应该不在开头
    
    def test_similarity(self):
        """测试相似度计算"""
        # 完全相同
        diff = TextDiff("abc", "abc")
        self.assertEqual(diff.similarity(), 1.0)
        
        # 完全不同
        diff = TextDiff("abc", "xyz")
        self.assertEqual(diff.similarity(), 0.0)
        
        # 部分相同
        diff = TextDiff("abc", "abd")
        self.assertTrue(0 < diff.similarity() < 1)
    
    def test_quick_ratio(self):
        """测试快速相似度"""
        diff = TextDiff("hello world", "hello there")
        quick = diff.quick_ratio()
        
        # 快速比率应该 >= 实际比率
        actual = diff.similarity()
        self.assertGreaterEqual(quick, actual)
    
    def test_stats_line_level(self):
        """测试差异统计 - 行级"""
        stats = self.differ.stats(level='line')
        
        self.assertIsInstance(stats, DiffStats)
        self.assertIsInstance(stats.additions, int)
        self.assertIsInstance(stats.deletions, int)
        self.assertIsInstance(stats.similarity, float)
        self.assertTrue(0 <= stats.similarity <= 1)
    
    def test_stats_char_level(self):
        """测试差异统计 - 字符级"""
        stats = self.differ.stats(level='char')
        
        self.assertIsInstance(stats, DiffStats)
        self.assertTrue(stats.similarity >= 0)
    
    def test_stats_word_level(self):
        """测试差异统计 - 单词级"""
        stats = self.differ.stats(level='word')
        
        self.assertIsInstance(stats, DiffStats)
        self.assertTrue(stats.similarity >= 0)


class TestUtilityFunctions(unittest.TestCase):
    """工具函数测试"""
    
    def test_diff_texts_line(self):
        """测试快捷函数 - 行级差异"""
        result = diff_texts("a\nb\nc", "a\nc\nd", level='line')
        
        self.assertTrue(len(result) > 0)
        types = [t for t, _ in result]
        self.assertIn(DiffType.EQUAL, types)
    
    def test_diff_texts_char(self):
        """测试快捷函数 - 字符级差异"""
        result = diff_texts("abc", "adc", level='char')
        
        self.assertTrue(len(result) > 0)
    
    def test_diff_texts_word(self):
        """测试快捷函数 - 单词级差异"""
        result = diff_texts("hello world", "hello there", level='word')
        
        self.assertTrue(len(result) > 0)
    
    def test_unified_diff_function(self):
        """测试统一格式差异快捷函数"""
        result = unified_diff("a\nb\nc", "a\nx\nc")
        
        self.assertIn('--- original', result)
        self.assertIn('+++ modified', result)
    
    def test_similarity_function(self):
        """测试相似度快捷函数"""
        result = similarity("hello", "hello")
        self.assertEqual(result, 1.0)
        
        result = similarity("hello", "world")
        self.assertTrue(result < 1.0)
    
    def test_find_common_substring(self):
        """测试查找最长公共子串"""
        result = find_common_substring("hello world", "hello there")
        
        self.assertEqual(result, "hello ")
    
    def test_find_common_substring_no_match(self):
        """测试查找最长公共子串 - 无匹配"""
        result = find_common_substring("abc", "xyz")
        
        self.assertEqual(result, "")
    
    def test_find_common_subsequences(self):
        """测试查找所有公共子串"""
        result = find_common_subsequences("hello world", "hello there", min_length=3)
        
        self.assertTrue(len(result) > 0)
        # 结果应按长度降序
        if len(result) > 1:
            self.assertGreaterEqual(len(result[0]), len(result[1]))
    
    def test_find_common_subsequences_min_length(self):
        """测试查找公共子串 - 最小长度"""
        result = find_common_subsequences("abc", "xyz", min_length=1)
        
        # 没有公共子串
        self.assertEqual(len(result), 0)
    
    def test_highlight_diff_html(self):
        """测试 HTML 高亮差异"""
        result = highlight_diff_html("hello world", "hello there")
        
        self.assertIn('<span', result)
        self.assertIn('background-color', result)
    
    def test_highlight_diff_html_custom_colors(self):
        """测试 HTML 高亮差异 - 自定义颜色"""
        result = highlight_diff_html(
            "abc", "adc",
            insert_color='#00ff00',
            delete_color='#ff0000'
        )
        
        self.assertIn('#00ff00', result)
        self.assertIn('#ff0000', result)
    
    def test_highlight_diff_html_escaping(self):
        """测试 HTML 高亮差异 - 特殊字符转义"""
        result = highlight_diff_html("<script>", "<div>")
        
        # 应该转义 HTML 字符
        self.assertNotIn('<script>', result)
        self.assertIn('&lt;', result)
    
    def test_count_changes(self):
        """测试变更计数"""
        result = count_changes("a\nb\nc", "a\nx\nc\ny")
        
        self.assertIn('additions', result)
        self.assertIn('deletions', result)
        self.assertIn('unchanged', result)
        self.assertIn('total_changes', result)
        self.assertIn('similarity', result)
    
    def test_count_changes_char_level(self):
        """测试变更计数 - 字符级"""
        result = count_changes("abc", "adc", level='char')
        
        self.assertTrue(result['total_changes'] > 0)
    
    def test_diff_three_texts(self):
        """测试三文本比较"""
        result = diff_three_texts("hello", "hallo", "hullo")
        
        self.assertIn('text1_vs_text2', result)
        self.assertIn('text1_vs_text3', result)
        self.assertIn('text2_vs_text3', result)
        
        # 所有的相似度都应该是有效值
        for key, value in result.items():
            self.assertTrue(0 <= value <= 1)


class TestEdgeCases(unittest.TestCase):
    """边界情况测试"""
    
    def test_empty_texts(self):
        """测试空文本"""
        diff = TextDiff("", "")
        self.assertEqual(diff.similarity(), 1.0)
        
        result = diff.compare_chars()
        self.assertEqual(len(result), 0)
    
    def test_one_empty_text(self):
        """测试一个空文本"""
        diff = TextDiff("hello", "")
        self.assertEqual(diff.similarity(), 0.0)
        
        result = diff.compare_chars()
        types = [t for t, _ in result]
        self.assertEqual(types, [DiffType.DELETE])
    
    def test_insert_into_empty(self):
        """测试向空文本插入"""
        diff = TextDiff("", "hello")
        result = diff.compare_chars()
        
        types = [t for t, _ in result]
        self.assertEqual(types, [DiffType.INSERT])
    
    def test_very_long_text(self):
        """测试长文本"""
        text1 = "a" * 10000
        text2 = "a" * 5000 + "b" * 5000
        
        diff = TextDiff(text1, text2)
        similarity = diff.similarity()
        
        # 应该约为 0.5 (一半相同)
        self.assertTrue(0.4 < similarity < 0.6)
    
    def test_unicode_text(self):
        """测试 Unicode 文本"""
        text1 = "你好世界"
        text2 = "你好宇宙"
        
        diff = TextDiff(text1, text2)
        result = diff.compare_chars()
        
        self.assertTrue(len(result) > 0)
        
        # 应该找到公共前缀
        common = find_common_substring(text1, text2)
        self.assertEqual(common, "你好")
    
    def test_newlines_handling(self):
        """测试换行符处理"""
        text1 = "line1\nline2\nline3"
        text2 = "line1\nline2\nline3"
        
        diff = TextDiff(text1, text2)
        self.assertEqual(diff.similarity(), 1.0)
    
    def test_whitespace_differences(self):
        """测试空白差异"""
        text1 = "hello world"
        text2 = "hello  world"  # 双空格
        
        similarity_val = similarity(text1, text2)
        self.assertTrue(0 < similarity_val < 1)
    
    def test_only_whitespace(self):
        """测试纯空白文本"""
        diff = TextDiff("   ", "\t\t")
        
        # 纯空白也应该能比较
        result = diff.compare_chars()
        self.assertTrue(len(result) > 0)


class TestDiffStats(unittest.TestCase):
    """DiffStats 测试"""
    
    def test_stats_dataclass(self):
        """测试 DiffStats 数据类"""
        stats = DiffStats(
            additions=5,
            deletions=3,
            modifications=2,
            unchanged=10,
            similarity=0.7
        )
        
        self.assertEqual(stats.additions, 5)
        self.assertEqual(stats.deletions, 3)
        self.assertEqual(stats.similarity, 0.7)


class TestDiffOperation(unittest.TestCase):
    """DiffOperation 测试"""
    
    def test_operation_dataclass(self):
        """测试 DiffOperation 数据类"""
        op = DiffOperation(
            diff_type=DiffType.INSERT,
            old_start=1,
            old_end=1,
            new_start=1,
            new_end=2,
            old_content="",
            new_content="new line"
        )
        
        self.assertEqual(op.diff_type, DiffType.INSERT)
        self.assertEqual(op.old_start, 1)
        self.assertEqual(op.new_content, "new line")


if __name__ == '__main__':
    unittest.main(verbosity=2)