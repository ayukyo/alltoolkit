"""
文本差异比较工具集测试
Text Diff Utilities Test Suite
"""

import sys
import os
import unittest

# Add module directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mod import (
    diff_lines, diff_words, diff_chars,
    unified_diff, context_diff, html_diff, inline_diff,
    similarity_ratio, levenshtein_distance, normalized_levenshtein,
    lcs, lcs_length, create_patch, apply_patch,
    find_matching_blocks, get_diff_summary, text_diff_summary,
    TextDiffer, batch_diff, find_duplicate_blocks,
    DiffType, DiffOp, DiffResult
)


class TestDiffLines(unittest.TestCase):
    """测试行级差异比较"""
    
    def test_identical_texts(self):
        """测试相同文本"""
        text = "line1\nline2\nline3"
        result = diff_lines(text, text)
        
        self.assertFalse(result.has_changes())
        self.assertEqual(result.stats["total_changes"], 0)
        self.assertEqual(len(result.old_lines), 3)
        self.assertEqual(len(result.new_lines), 3)
    
    def test_add_lines(self):
        """测试添加行"""
        old = "line1\nline2"
        new = "line1\nline2\nline3"
        result = diff_lines(old, new)
        
        self.assertTrue(result.has_changes())
        self.assertEqual(result.stats["added"], 1)
        changes = result.get_changes()
        self.assertEqual(len(changes), 1)
        self.assertEqual(changes[0].type, DiffType.INSERT)
    
    def test_delete_lines(self):
        """测试删除行"""
        old = "line1\nline2\nline3"
        new = "line1\nline3"
        result = diff_lines(old, new)
        
        self.assertTrue(result.has_changes())
        self.assertEqual(result.stats["deleted"], 1)
    
    def test_replace_lines(self):
        """测试替换行"""
        old = "line1\nline2\nline3"
        new = "line1\nmodified\nline3"
        result = diff_lines(old, new)
        
        self.assertTrue(result.has_changes())
        self.assertEqual(result.stats["replaced"], 1)
    
    def test_ignore_whitespace(self):
        """测试忽略空白"""
        old = "line1\n  line2\nline3"
        new = "line1\nline2\nline3"
        result = diff_lines(old, new, ignore_whitespace=True)
        
        self.assertFalse(result.has_changes())
    
    def test_ignore_case(self):
        """测试忽略大小写"""
        old = "Hello\nWorld"
        new = "hello\nworld"
        result = diff_lines(old, new, ignore_case=True)
        
        self.assertFalse(result.has_changes())
    
    def test_empty_texts(self):
        """测试空文本"""
        old = ""
        new = "new line"
        result = diff_lines(old, new)
        
        self.assertTrue(result.has_changes())
        self.assertEqual(result.stats["added"], 1)


class TestDiffWords(unittest.TestCase):
    """测试单词级差异比较"""
    
    def test_word_diff_identical(self):
        """测试相同文本的单词差异"""
        text = "hello world"
        result = diff_words(text, text)
        
        self.assertEqual(len(result), 2)
        for word, diff_type in result:
            self.assertEqual(diff_type, DiffType.EQUAL)
    
    def test_word_diff_add(self):
        """测试添加单词"""
        old = "hello world"
        new = "hello beautiful world"
        result = diff_words(old, new)
        
        insert_count = sum(1 for _, dt in result if dt == DiffType.INSERT)
        self.assertEqual(insert_count, 1)
    
    def test_word_diff_delete(self):
        """测试删除单词"""
        old = "hello beautiful world"
        new = "hello world"
        result = diff_words(old, new)
        
        delete_count = sum(1 for _, dt in result if dt == DiffType.DELETE)
        self.assertEqual(delete_count, 1)
    
    def test_word_diff_ignore_case(self):
        """测试忽略大小写"""
        old = "Hello World"
        new = "hello world"
        result = diff_words(old, new, ignore_case=True)
        
        equal_count = sum(1 for _, dt in result if dt == DiffType.EQUAL)
        self.assertEqual(equal_count, 2)


class TestDiffChars(unittest.TestCase):
    """测试字符级差异比较"""
    
    def test_char_diff_identical(self):
        """测试相同文本的字符差异"""
        text = "hello"
        result = diff_chars(text, text)
        
        self.assertEqual(len(result), 5)
        for char, diff_type in result:
            self.assertEqual(diff_type, DiffType.EQUAL)
    
    def test_char_diff_add(self):
        """测试添加字符"""
        old = "abc"
        new = "abcd"
        result = diff_chars(old, new)
        
        insert_count = sum(1 for _, dt in result if dt == DiffType.INSERT)
        self.assertEqual(insert_count, 1)
    
    def test_char_diff_modify(self):
        """测试修改字符"""
        old = "hello"
        new = "hallo"
        result = diff_chars(old, new)
        
        # 应该有删除和插入
        delete_count = sum(1 for _, dt in result if dt == DiffType.DELETE)
        insert_count = sum(1 for _, dt in result if dt == DiffType.INSERT)
        self.assertTrue(delete_count > 0 or insert_count > 0)


class TestUnifiedDiff(unittest.TestCase):
    """测试统一差异格式"""
    
    def test_unified_diff_header(self):
        """测试差异头"""
        old = "line1\nline2"
        new = "line1\nline3"
        result = unified_diff(old, new, "old.txt", "new.txt")
        
        self.assertIn("--- old.txt", result)
        self.assertIn("+++ new.txt", result)
    
    def test_unified_diff_changes(self):
        """测试差异变更"""
        old = "line1\nline2\nline3"
        new = "line1\nmodified\nline3"
        result = unified_diff(old, new)
        
        self.assertIn("-line2", result)
        self.assertIn("+modified", result)
    
    def test_unified_diff_add(self):
        """测试添加行"""
        old = "line1"
        new = "line1\nline2"
        result = unified_diff(old, new)
        
        self.assertIn("+line2", result)
    
    def test_unified_diff_delete(self):
        """测试删除行"""
        old = "line1\nline2"
        new = "line1"
        result = unified_diff(old, new)
        
        self.assertIn("-line2", result)


class TestContextDiff(unittest.TestCase):
    """测试上下文差异格式"""
    
    def test_context_diff_header(self):
        """测试差异头"""
        old = "line1\nline2"
        new = "line1\nline3"
        result = context_diff(old, new, "old.txt", "new.txt")
        
        self.assertIn("*** old.txt", result)
        self.assertIn("--- new.txt", result)
    
    def test_context_diff_changes(self):
        """测试差异变更"""
        old = "line1\nline2\nline3"
        new = "line1\nmodified\nline3"
        result = context_diff(old, new)
        
        self.assertIn("- line2", result)
        self.assertIn("+ modified", result)


class TestHtmlDiff(unittest.TestCase):
    """测试 HTML 差异格式"""
    
    def test_html_diff_structure(self):
        """测试 HTML 结构"""
        old = "line1\nline2"
        new = "line1\nline3"
        result = html_diff(old, new)
        
        self.assertIn("<!DOCTYPE html>", result)
        self.assertIn("<table>", result)
        self.assertIn("</table>", result)
        self.assertIn("</html>", result)
    
    def test_html_diff_classes(self):
        """测试 CSS 类"""
        # 使用删除和插入的场景，而不是替换
        old = "line1\nline2"
        new = "line1\nline3\nline4"
        result = html_diff(old, new)
        
        # 检查 CSS 类定义存在
        self.assertIn(".delete", result)
        self.assertIn(".insert", result)
        # 检查实际使用了差异类
        self.assertTrue("class=\"replace\"" in result or "class=\"delete\"" in result or "class=\"insert\"" in result)
    
    def test_html_diff_custom_titles(self):
        """测试自定义标题"""
        old = "line1"
        new = "line2"
        result = html_diff(old, new, "Original", "Modified")
        
        self.assertIn("Original", result)
        self.assertIn("Modified", result)


class TestInlineDiff(unittest.TestCase):
    """测试内联差异格式"""
    
    def test_inline_diff_prefixes(self):
        """测试行前缀"""
        old = "line1\nline2"
        new = "line1\nline3"
        result = inline_diff(old, new)
        
        lines = result.split('\n')
        self.assertTrue(any(line.startswith('  ') for line in lines))  # equal
        self.assertTrue(any(line.startswith('- ') for line in lines))  # delete
        self.assertTrue(any(line.startswith('+ ') for line in lines))  # insert
    
    def test_inline_diff_custom_prefixes(self):
        """测试自定义前缀"""
        old = "line1"
        new = "line2"
        result = inline_diff(old, new, "ADD ", "DEL ", "EQ ")
        
        self.assertIn("DEL line1", result)
        self.assertIn("ADD line2", result)


class TestSimilarity(unittest.TestCase):
    """测试相似度计算"""
    
    def test_identical_texts(self):
        """测试相同文本"""
        text = "hello world"
        similarity = similarity_ratio(text, text)
        
        self.assertEqual(similarity, 1.0)
    
    def test_completely_different(self):
        """测试完全不同的文本"""
        old = "abc"
        new = "xyz"
        similarity = similarity_ratio(old, new)
        
        self.assertEqual(similarity, 0.0)
    
    def test_partial_similarity(self):
        """测试部分相似"""
        old = "hello world"
        new = "hello there"
        similarity = similarity_ratio(old, new)
        
        self.assertGreater(similarity, 0.0)
        self.assertLess(similarity, 1.0)
    
    def test_similarity_empty(self):
        """测试空文本"""
        self.assertEqual(similarity_ratio("", ""), 1.0)
        self.assertEqual(similarity_ratio("abc", ""), 0.0)


class TestLevenshtein(unittest.TestCase):
    """测试 Levenshtein 距离"""
    
    def test_identical_strings(self):
        """测试相同字符串"""
        self.assertEqual(levenshtein_distance("hello", "hello"), 0)
    
    def test_one_insertion(self):
        """测试一次插入"""
        self.assertEqual(levenshtein_distance("hello", "hellos"), 1)
    
    def test_one_deletion(self):
        """测试一次删除"""
        self.assertEqual(levenshtein_distance("hello", "hell"), 1)
    
    def test_one_replacement(self):
        """测试一次替换"""
        self.assertEqual(levenshtein_distance("hello", "hallo"), 1)
    
    def test_multiple_operations(self):
        """测试多次操作"""
        self.assertEqual(levenshtein_distance("kitten", "sitting"), 3)
    
    def test_empty_strings(self):
        """测试空字符串"""
        self.assertEqual(levenshtein_distance("", ""), 0)
        self.assertEqual(levenshtein_distance("abc", ""), 3)
        self.assertEqual(levenshtein_distance("", "xyz"), 3)
    
    def test_normalized_levenshtein(self):
        """测试归一化距离"""
        self.assertEqual(normalized_levenshtein("", ""), 0.0)
        self.assertEqual(normalized_levenshtein("abc", "abc"), 0.0)
        self.assertEqual(normalized_levenshtein("abc", "xyz"), 1.0)


class TestLCS(unittest.TestCase):
    """测试最长公共子序列"""
    
    def test_identical_strings(self):
        """测试相同字符串"""
        self.assertEqual(lcs("hello", "hello"), "hello")
    
    def test_no_common(self):
        """测试无公共子序列"""
        self.assertEqual(lcs("abc", "xyz"), "")
    
    def test_partial_common(self):
        """测试部分公共"""
        result = lcs("abcde", "ace")
        self.assertEqual(result, "ace")
    
    def test_lcs_length(self):
        """测试 LCS 长度"""
        self.assertEqual(lcs_length("abcde", "ace"), 3)
        self.assertEqual(lcs_length("hello", "world"), 1)  # 'l' 或 'o'（顺序不同，只能取一个）
        self.assertEqual(lcs_length("abcdef", "abcdef"), 6)


class TestPatch(unittest.TestCase):
    """测试补丁功能"""
    
    def test_create_patch(self):
        """测试创建补丁"""
        old = "line1\nline2\nline3"
        new = "line1\nmodified\nline3"
        patch = create_patch(old, new)
        
        self.assertIn("--- old", patch)
        self.assertIn("+++ new", patch)
        self.assertIn("-line2", patch)
        self.assertIn("+modified", patch)
    
    def test_create_patch_empty(self):
        """测试空文本的补丁"""
        old = ""
        new = "new content"
        patch = create_patch(old, new)
        
        self.assertIn("+new content", patch)


class TestDiffSummary(unittest.TestCase):
    """测试差异摘要"""
    
    def test_summary_no_changes(self):
        """测试无变化摘要"""
        text = "line1\nline2"
        summary = get_diff_summary(text, text)
        
        self.assertEqual(summary["old_lines"], 2)
        self.assertEqual(summary["new_lines"], 2)
        self.assertEqual(summary["total_changes"], 0)
        self.assertFalse(summary["has_changes"])
        self.assertEqual(summary["similarity"], 1.0)
    
    def test_summary_with_changes(self):
        """测试有变化的摘要"""
        old = "line1\nline2"
        new = "line1\nline3\nline4"
        summary = get_diff_summary(old, new)
        
        self.assertEqual(summary["old_lines"], 2)
        self.assertEqual(summary["new_lines"], 3)
        self.assertTrue(summary["has_changes"])
        self.assertLess(summary["similarity"], 1.0)
    
    def test_text_summary_format(self):
        """测试文本摘要格式"""
        old = "line1\nline2"
        new = "line1\nline3"
        summary = text_diff_summary(old, new)
        
        self.assertIn("lines", summary)
        self.assertIn("similarity", summary)


class TestTextDifferClass(unittest.TestCase):
    """测试 TextDiffer 类"""
    
    def test_differ_basic(self):
        """测试基本差异"""
        differ = TextDiffer()
        result = differ.diff("hello\nworld", "hello\nthere")
        
        self.assertTrue(result.has_changes())
    
    def test_differ_with_options(self):
        """测试带选项的差异"""
        differ = TextDiffer(ignore_whitespace=True)
        result = differ.diff("hello\n  world", "hello\nworld")
        
        self.assertFalse(result.has_changes())
    
    def test_differ_unified(self):
        """测试统一差异"""
        differ = TextDiffer()
        result = differ.unified_diff("line1", "line2")
        
        self.assertIn("---", result)
        self.assertIn("+++", result)
    
    def test_differ_html(self):
        """测试 HTML 差异"""
        differ = TextDiffer()
        result = differ.html_diff("line1", "line2")
        
        self.assertIn("<table>", result)
    
    def test_differ_similarity(self):
        """测试相似度"""
        differ = TextDiffer()
        similarity = differ.similarity("hello", "hallo")
        
        self.assertGreater(similarity, 0.5)


class TestAdvancedFeatures(unittest.TestCase):
    """测试高级功能"""
    
    def test_batch_diff(self):
        """测试批量差异"""
        texts = [
            ("hello", "hallo"),
            ("world", "world"),
            ("test", "testing")
        ]
        results = batch_diff(texts)
        
        self.assertEqual(len(results), 3)
        self.assertTrue(results[0].has_changes())
        self.assertFalse(results[1].has_changes())
        self.assertTrue(results[2].has_changes())
    
    def test_find_matching_blocks(self):
        """测试查找匹配块"""
        blocks = find_matching_blocks("hello world", "hello there")
        
        self.assertTrue(len(blocks) > 0)
        # 第一个块应该是 "hello "
        self.assertEqual(blocks[0][2], 6)  # 长度为 6
    
    def test_find_duplicate_blocks(self):
        """测试查找重复块"""
        text = "line1\nline2\nline1\nline3"
        duplicates = find_duplicate_blocks(text, min_length=1)
        
        self.assertTrue(len(duplicates) > 0)


class TestEdgeCases(unittest.TestCase):
    """测试边缘情况"""
    
    def test_single_line(self):
        """测试单行文本"""
        old = "single line"
        new = "modified line"
        result = diff_lines(old, new)
        
        self.assertTrue(result.has_changes())
    
    def test_large_text(self):
        """测试大文本"""
        lines = 1000
        old = '\n'.join([f"line{i}" for i in range(lines)])
        new = '\n'.join([f"line{i}" for i in range(lines)] + ["extra"])
        
        result = diff_lines(old, new)
        self.assertEqual(result.stats["added"], 1)
    
    def test_unicode(self):
        """测试 Unicode"""
        old = "你好世界"
        new = "你好宇宙"
        result = diff_lines(old, new)
        
        self.assertTrue(result.has_changes())
    
    def test_special_characters(self):
        """测试特殊字符"""
        old = "line\twith\ttabs"
        new = "line with spaces"
        result = diff_lines(old, new)
        
        self.assertTrue(result.has_changes())


class TestDiffOps(unittest.TestCase):
    """测试差异操作"""
    
    def test_diff_op_repr(self):
        """测试 DiffOp 表示"""
        op = DiffOp(
            type=DiffType.EQUAL,
            old_start=0, old_end=1,
            new_start=0, new_end=1,
            old_content="test",
            new_content="test"
        )
        self.assertIn("EQUAL", repr(op))
    
    def test_diff_result_stats(self):
        """测试 DiffResult 统计"""
        result = diff_lines("a\nb\nc", "a\nd\nc")
        stats = result.stats
        
        self.assertIn("added", stats)
        self.assertIn("deleted", stats)
        self.assertIn("replaced", stats)
        self.assertIn("unchanged", stats)
        self.assertIn("total_changes", stats)


def run_tests():
    """运行所有测试"""
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # 添加所有测试类
    test_classes = [
        TestDiffLines,
        TestDiffWords,
        TestDiffChars,
        TestUnifiedDiff,
        TestContextDiff,
        TestHtmlDiff,
        TestInlineDiff,
        TestSimilarity,
        TestLevenshtein,
        TestLCS,
        TestPatch,
        TestDiffSummary,
        TestTextDifferClass,
        TestAdvancedFeatures,
        TestEdgeCases,
        TestDiffOps,
    ]
    
    for test_class in test_classes:
        tests = loader.loadTestsFromTestCase(test_class)
        suite.addTests(tests)
    
    # 运行测试
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # 返回测试结果
    return result.wasSuccessful()


if __name__ == '__main__':
    success = run_tests()
    exit(0 if success else 1)