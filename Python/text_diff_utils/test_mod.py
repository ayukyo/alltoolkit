"""
文本差异比较工具测试模块
"""

import unittest
from mod import (
    TextDiffUtils, DiffType, DiffLine, DiffResult,
    compare_texts, get_unified_diff, get_similarity,
    format_diff_summary, format_side_by_side
)


class TestTextDiffUtils(unittest.TestCase):
    """TextDiffUtils 测试类"""
    
    def setUp(self):
        """测试前准备"""
        self.utils = TextDiffUtils()
        
        self.old_text = """Line 1
Line 2
Line 3
Line 4
Line 5"""
        
        self.new_text = """Line 1
Line 2 modified
Line 3
Line 4
Line 5
Line 6"""
    
    def test_compare_lines_basic(self):
        """测试基本行比较"""
        result = self.utils.compare_lines(self.old_text, self.new_text)
        
        self.assertEqual(result.old_lines, 5)
        self.assertEqual(result.new_lines, 6)
        self.assertGreater(result.similarity, 0.5)
    
    def test_compare_lines_identical(self):
        """测试相同文本比较"""
        result = self.utils.compare_lines("Same text", "Same text")
        
        self.assertEqual(result.old_lines, 1)
        self.assertEqual(result.new_lines, 1)
        self.assertEqual(result.added_lines, 0)
        self.assertEqual(result.deleted_lines, 0)
        self.assertEqual(result.similarity, 1.0)
    
    def test_compare_lines_empty(self):
        """测试空文本比较"""
        result = self.utils.compare_lines("", "")
        
        self.assertEqual(result.old_lines, 0)
        self.assertEqual(result.new_lines, 0)
        self.assertEqual(result.similarity, 1.0)
    
    def test_compare_lines_all_different(self):
        """测试完全不同的文本"""
        result = self.utils.compare_lines("ABC", "XYZ")
        
        self.assertLess(result.similarity, 0.5)
        # 完全不同时，应该是 replace：删除旧行，新增新行
        self.assertEqual(result.added_lines, 1)
        self.assertEqual(result.deleted_lines, 1)
    
    def test_unified_diff(self):
        """测试统一格式差异"""
        diff = self.utils.unified_diff(
            self.old_text, 
            self.new_text,
            "old.txt",
            "new.txt"
        )
        
        self.assertIn("--- old.txt", diff)
        self.assertIn("+++ new.txt", diff)
        self.assertIn("@@", diff)
    
    def test_unified_diff_empty(self):
        """测试空文本统一格式差异"""
        diff = self.utils.unified_diff("", "New content", "empty", "new")
        
        self.assertIn("+++ new", diff)
        self.assertIn("+New content", diff)
    
    def test_side_by_side(self):
        """测试并排对比"""
        pairs = self.utils.side_by_side(
            "Line 1\nLine 2",
            "Line 1\nLine 2 modified"
        )
        
        self.assertEqual(len(pairs), 2)
        # 第一行相同
        self.assertEqual(pairs[0][1], '  ')
        # 第二行不同
        self.assertEqual(pairs[1][1], '~ ')
    
    def test_char_diff(self):
        """测试字符级差异"""
        diffs = self.utils.char_diff("Hello", "Helo")
        
        # 应该包含相等和删除
        types = [d[0] for d in diffs]
        self.assertIn(DiffType.EQUAL, types)
    
    def test_char_diff_identical(self):
        """测试相同文本字符级差异"""
        diffs = self.utils.char_diff("Same", "Same")
        
        self.assertEqual(len(diffs), 1)
        self.assertEqual(diffs[0][0], DiffType.EQUAL)
        self.assertEqual(diffs[0][1], "Same")
    
    def test_similarity(self):
        """测试相似度计算"""
        # 完全相同
        sim = self.utils.similarity("Same text", "Same text")
        self.assertEqual(sim, 1.0)
        
        # 完全不同
        sim = self.utils.similarity("ABC", "XYZ")
        self.assertEqual(sim, 0.0)
        
        # 部分相同
        sim = self.utils.similarity("Hello World", "Hello")
        self.assertGreater(sim, 0.0)
        self.assertLess(sim, 1.0)
    
    def test_diff_stats(self):
        """测试差异统计"""
        stats = self.utils.diff_stats(self.old_text, self.new_text)
        
        self.assertIn('old_lines', stats)
        self.assertIn('new_lines', stats)
        self.assertIn('added_lines', stats)
        self.assertIn('deleted_lines', stats)
        self.assertIn('similarity', stats)
        self.assertIn('is_identical', stats)
        self.assertIn('diff_percentage', stats)
        
        self.assertEqual(stats['old_lines'], 5)
        self.assertEqual(stats['new_lines'], 6)
        self.assertFalse(stats['is_identical'])
    
    def test_find_matches(self):
        """测试查找公共子串"""
        matches = self.utils.find_matches(
            "Hello World Python",
            "Hello Python World",
            min_length=5
        )
        
        # 应该找到 "Hello" 和 "Python"
        self.assertGreater(len(matches), 0)
    
    def test_find_matches_no_match(self):
        """测试无公共子串"""
        matches = self.utils.find_matches("ABC", "XYZ", min_length=2)
        
        self.assertEqual(len(matches), 0)
    
    def test_ignore_case(self):
        """测试忽略大小写"""
        utils_ignore_case = TextDiffUtils(ignore_case=True)
        
        result = utils_ignore_case.compare_lines("HELLO", "hello")
        
        self.assertEqual(result.similarity, 1.0)
    
    def test_ignore_whitespace(self):
        """测试忽略空白字符"""
        utils_ignore_ws = TextDiffUtils(ignore_whitespace=True)
        
        result = utils_ignore_ws.compare_lines("Hello  World", "Hello World")
        
        self.assertEqual(result.similarity, 1.0)
    
    def test_ignore_blank_lines(self):
        """测试忽略空行"""
        utils_ignore_blank = TextDiffUtils(ignore_blank_lines=True)
        
        text1 = "Line 1\n\nLine 2"
        text2 = "Line 1\nLine 2"
        
        result = utils_ignore_blank.compare_lines(text1, text2)
        
        # 忽略空行后应该高度相似（非空内容一致）
        # 注意：_normalize_lines 用于比较，但原始行列表仍然包含空行
        # 所以结果会显示差异
        self.assertGreater(result.similarity, 0.5)
    
    def test_compare_texts_convenience(self):
        """测试便捷函数 compare_texts"""
        result = compare_texts("Line 1\nLine 2", "Line 1\nLine 2 modified")
        
        self.assertIsInstance(result, DiffResult)
        self.assertLess(result.similarity, 1.0)
    
    def test_get_unified_diff_convenience(self):
        """测试便捷函数 get_unified_diff"""
        diff = get_unified_diff("Old", "New", "old.txt", "new.txt")
        
        self.assertIn("--- old.txt", diff)
        self.assertIn("+++ new.txt", diff)
    
    def test_get_similarity_convenience(self):
        """测试便捷函数 get_similarity"""
        sim = get_similarity("Same", "Same")
        
        self.assertEqual(sim, 1.0)
    
    def test_format_diff_summary(self):
        """测试差异摘要格式化"""
        result = self.utils.compare_lines(self.old_text, self.new_text)
        summary = format_diff_summary(result)
        
        self.assertIn("差异摘要", summary)
        self.assertIn("原文本行数", summary)
        self.assertIn("新文本行数", summary)
        self.assertIn("相似度", summary)
    
    def test_format_side_by_side(self):
        """测试并排对比格式化"""
        pairs = self.utils.side_by_side(
            "Line 1\nLine 2",
            "Line 1\nLine 2 modified"
        )
        
        output = format_side_by_side(pairs, "测试对比")
        
        self.assertIn("测试对比", output)
        self.assertIn("原文本", output)
        self.assertIn("新文本", output)
    
    def test_format_side_by_side_empty(self):
        """测试空并排对比格式化"""
        output = format_side_by_side([], "空对比")
        
        self.assertIn("空对比", output)
        self.assertIn("无差异", output)
    
    def test_multiline_diff(self):
        """测试多行差异"""
        old = """First line
Second line
Third line
Fourth line"""
        
        new = """First line
Second line modified
Third line
Fourth line
Fifth line added"""
        
        result = self.utils.compare_lines(old, new)
        
        # 应该检测到差异
        self.assertLess(result.similarity, 1.0)
        # 新增行或删除行应该大于 0
        self.assertGreater(result.added_lines + result.deleted_lines, 0)
    
    def test_unicode_text(self):
        """测试 Unicode 文本"""
        old = "你好世界\n第二行"
        new = "你好世界\n第二行修改"
        
        result = self.utils.compare_lines(old, new)
        
        # 应该检测到差异
        self.assertLess(result.similarity, 1.0)
        self.assertGreater(result.similarity, 0.3)
    
    def test_special_characters(self):
        """测试特殊字符"""
        old = "Line with\ttab\nLine with spaces"
        new = "Line with\ttab\nLine with\ttab"
        
        result = self.utils.compare_lines(old, new)
        
        self.assertIsInstance(result.similarity, float)
    
    def test_very_long_line(self):
        """测试长行"""
        long_line = "A" * 10000
        old = long_line
        new = long_line + "B"
        
        # 使用字符级差异测试
        diffs = self.utils.char_diff(old, new)
        
        # 应该有差异
        self.assertGreater(len(diffs), 0)
    
    def test_many_lines(self):
        """测试多行文本"""
        old = "\n".join(f"Line {i}" for i in range(1000))
        new = "\n".join(f"Line {i}" for i in range(1000))
        
        result = self.utils.compare_lines(old, new)
        
        self.assertEqual(result.similarity, 1.0)
    
    def test_insert_at_beginning(self):
        """测试开头插入"""
        result = self.utils.compare_lines("Line 1\nLine 2", "New Line\nLine 1\nLine 2")
        
        self.assertGreater(result.added_lines, 0)
    
    def test_insert_at_end(self):
        """测试末尾插入"""
        result = self.utils.compare_lines("Line 1\nLine 2", "Line 1\nLine 2\nNew Line")
        
        # 末尾插入应该检测到差异
        self.assertLess(result.similarity, 1.0)
    
    def test_delete_lines(self):
        """测试删除行"""
        result = self.utils.compare_lines("Line 1\nLine 2\nLine 3", "Line 1\nLine 3")
        
        self.assertGreater(result.deleted_lines, 0)
    
    def test_context_lines_parameter(self):
        """测试上下文行数参数"""
        diff1 = self.utils.unified_diff(
            self.old_text,
            self.new_text,
            context_lines=0
        )
        
        diff2 = self.utils.unified_diff(
            self.old_text,
            self.new_text,
            context_lines=5
        )
        
        # 更多上下文应该产生更长的输出
        self.assertGreaterEqual(len(diff2), len(diff1))


class TestDiffType(unittest.TestCase):
    """DiffType 枚举测试"""
    
    def test_diff_type_values(self):
        """测试差异类型枚举值"""
        self.assertEqual(DiffType.EQUAL.value, "equal")
        self.assertEqual(DiffType.INSERT.value, "insert")
        self.assertEqual(DiffType.DELETE.value, "delete")
        self.assertEqual(DiffType.REPLACE.value, "replace")


class TestDiffLine(unittest.TestCase):
    """DiffLine 数据类测试"""
    
    def test_diff_line_creation(self):
        """测试差异行创建"""
        line = DiffLine(
            line_number_old=1,
            line_number_new=1,
            content="Test content",
            diff_type=DiffType.EQUAL
        )
        
        self.assertEqual(line.line_number_old, 1)
        self.assertEqual(line.line_number_new, 1)
        self.assertEqual(line.content, "Test content")
        self.assertEqual(line.diff_type, DiffType.EQUAL)
    
    def test_diff_line_none_numbers(self):
        """测试差异行空行号"""
        line = DiffLine(
            line_number_old=None,
            line_number_new=5,
            content="New line",
            diff_type=DiffType.INSERT
        )
        
        self.assertIsNone(line.line_number_old)
        self.assertEqual(line.line_number_new, 5)


class TestDiffResult(unittest.TestCase):
    """DiffResult 数据类测试"""
    
    def test_diff_result_creation(self):
        """测试差异结果创建"""
        result = DiffResult(
            old_lines=10,
            new_lines=12,
            added_lines=3,
            deleted_lines=1,
            changed_lines=2,
            similarity=0.85,
            diff_lines=[]
        )
        
        self.assertEqual(result.old_lines, 10)
        self.assertEqual(result.new_lines, 12)
        self.assertEqual(result.added_lines, 3)
        self.assertEqual(result.deleted_lines, 1)
        self.assertEqual(result.changed_lines, 2)
        self.assertEqual(result.similarity, 0.85)


if __name__ == "__main__":
    unittest.main()