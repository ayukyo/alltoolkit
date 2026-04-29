package diff_utils;

import org.junit.Test;
import static org.junit.Assert.*;
import java.util.List;

/**
 * DiffUtils 测试类
 * 
 * @author AllToolkit
 * @version 1.0.0
 */
public class DiffUtilsTest {

    // ==================== 基础比较测试 ====================

    @Test
    public void testIdenticalTexts() {
        String text = "Hello\nWorld\nTest";
        DiffUtils.DiffResult result = DiffUtils.diff(text, text);
        
        assertFalse("应该检测到无变化", result.hasChanges());
        assertEquals("相似度应为100%", 1.0, result.getSimilarity(), 0.001);
        assertEquals("插入数应为0", 0, result.insertions);
        assertEquals("删除数应为0", 0, result.deletions);
    }

    @Test
    public void testEmptyTexts() {
        DiffUtils.DiffResult result = DiffUtils.diff("", "");
        assertFalse("两个空文本应无差异", result.hasChanges());
    }

    @Test
    public void testNullTexts() {
        DiffUtils.DiffResult result = DiffUtils.diff(null, null);
        assertFalse("两个null应无差异", result.hasChanges());
    }

    @Test
    public void testNullVsEmpty() {
        DiffUtils.DiffResult result1 = DiffUtils.diff(null, "");
        DiffUtils.DiffResult result2 = DiffUtils.diff("", null);
        
        assertFalse("null与空字符串应无差异", result1.hasChanges());
        assertFalse("空字符串与null应无差异", result2.hasChanges());
    }

    // ==================== 行级别差异测试 ====================

    @Test
    public void testSingleLineInsert() {
        String oldText = "Line 1\nLine 3";
        String newText = "Line 1\nLine 2\nLine 3";
        
        DiffUtils.DiffResult result = DiffUtils.diff(oldText, newText);
        
        assertTrue("应该检测到变化", result.hasChanges());
        assertTrue("应该有插入", result.insertions > 0);
    }

    @Test
    public void testSingleLineDelete() {
        String oldText = "Line 1\nLine 2\nLine 3";
        String newText = "Line 1\nLine 3";
        
        DiffUtils.DiffResult result = DiffUtils.diff(oldText, newText);
        
        assertTrue("应该检测到变化", result.hasChanges());
        assertTrue("应该有删除", result.deletions > 0);
    }

    @Test
    public void testLineModification() {
        String oldText = "Hello World";
        String newText = "Hello Java";
        
        DiffUtils.DiffResult result = DiffUtils.diff(oldText, newText);
        
        assertTrue("应该检测到变化", result.hasChanges());
        assertTrue("应该有插入", result.insertions > 0);
        assertTrue("应该有删除", result.deletions > 0);
    }

    @Test
    public void testMultipleChanges() {
        String oldText = "A\nB\nC\nD\nE";
        String newText = "A\nX\nC\nY\nE";
        
        DiffUtils.DiffResult result = DiffUtils.diff(oldText, newText);
        
        assertTrue("应该检测到变化", result.hasChanges());
        // B->X 和 D->Y 各有一次删除和插入
        assertTrue("应该有多次变化", result.insertions >= 2);
    }

    // ==================== 字符级别差异测试 ====================

    @Test
    public void testCharacterDiff() {
        String oldText = "kitten";
        String newText = "sitting";
        
        DiffUtils.DiffResult result = DiffUtils.diff(oldText, newText, false);
        
        assertTrue("应该检测到变化", result.hasChanges());
    }

    // ==================== 数组比较测试 ====================

    @Test
    public void testArrayDiff() {
        String[] oldArr = {"a", "b", "c", "d"};
        String[] newArr = {"a", "x", "c", "y"};
        
        DiffUtils.DiffResult result = DiffUtils.diffArrays(oldArr, newArr);
        
        assertTrue("应该检测到变化", result.hasChanges());
        assertEquals("插入数应为2", 2, result.insertions);
        assertEquals("删除数应为2", 2, result.deletions);
    }

    @Test
    public void testEmptyArrayDiff() {
        String[] empty = {};
        String[] arr = {"a", "b", "c"};
        
        DiffUtils.DiffResult result1 = DiffUtils.diffArrays(empty, arr);
        assertTrue("空数组变非空应有插入", result1.insertions > 0);
        
        DiffUtils.DiffResult result2 = DiffUtils.diffArrays(arr, empty);
        assertTrue("非空变空应有删除", result2.deletions > 0);
    }

    // ==================== 编辑距离测试 ====================

    @Test
    public void testLevenshteinDistance() {
        assertEquals("kitten->sitting的距离应为3", 
            3, DiffUtils.levenshteinDistance("kitten", "sitting"));
        
        assertEquals("相同字符串距离应为0", 
            0, DiffUtils.levenshteinDistance("hello", "hello"));
        
        assertEquals("空字符串距离应为字符串长度", 
            5, DiffUtils.levenshteinDistance("", "hello"));
        
        assertEquals("完全不同字符的距离", 
            3, DiffUtils.levenshteinDistance("abc", "xyz"));
    }

    @Test
    public void testLevenshteinDistanceNull() {
        assertEquals("null与字符串的距离", 
            5, DiffUtils.levenshteinDistance(null, "hello"));
        assertEquals("字符串与null的距离", 
            5, DiffUtils.levenshteinDistance("hello", null));
        assertEquals("两个null的距离", 
            0, DiffUtils.levenshteinDistance(null, null));
    }

    // ==================== 相似度测试 ====================

    @Test
    public void testSimilarity() {
        assertEquals("相同字符串相似度应为1.0", 
            1.0, DiffUtils.similarity("hello", "hello"), 0.001);
        
        assertEquals("完全不同字符串相似度应为0.0", 
            0.0, DiffUtils.similarity("abc", "xyz"), 0.001);
        
        assertTrue("部分相似应在0-1之间", 
            DiffUtils.similarity("hello", "hallo") > 0.5);
    }

    @Test
    public void testSimilarityNull() {
        assertEquals("两个null相似度应为1.0", 
            1.0, DiffUtils.similarity(null, null), 0.001);
        assertEquals("null与字符串相似度应为0.0", 
            0.0, DiffUtils.similarity(null, "hello"), 0.001);
    }

    // ==================== LCS 测试 ====================

    @Test
    public void testLongestCommonSubstring() {
        assertEquals("最长公共子串", 
            "ABC", DiffUtils.longestCommonSubstring("ABABC", "ABCBA"));
        
        assertEquals("无公共子串", 
            "", DiffUtils.longestCommonSubstring("abc", "xyz"));
        
        assertEquals("完全相同", 
            "hello", DiffUtils.longestCommonSubstring("hello", "hello"));
    }

    @Test
    public void testLongestCommonSubsequence() {
        assertEquals("最长公共子序列", 
            "ABC", DiffUtils.longestCommonSubsequence("ABCBDAB", "BDCABA"));
        
        assertEquals("完全相同", 
            "hello", DiffUtils.longestCommonSubsequence("hello", "hello"));
        
        assertEquals("无公共子序列", 
            "", DiffUtils.longestCommonSubsequence("abc", "xyz"));
    }

    // ==================== 快速比较测试 ====================

    @Test
    public void testQuickCompare() {
        assertTrue("相同文本应返回true", 
            DiffUtils.quickCompare("test", "test"));
        assertFalse("不同文本应返回false", 
            DiffUtils.quickCompare("test1", "test2"));
    }

    @Test
    public void testIsIdentical() {
        assertTrue("相同文本", 
            DiffUtils.isIdentical("hello", "hello"));
        assertFalse("不同文本", 
            DiffUtils.isIdentical("hello", "world"));
        assertTrue("两个null", 
            DiffUtils.isIdentical(null, null));
        assertFalse("一个null", 
            DiffUtils.isIdentical(null, "test"));
    }

    // ==================== 统一格式输出测试 ====================

    @Test
    public void testUnifiedDiff() {
        String oldText = "Line 1\nLine 2\nLine 3";
        String newText = "Line 1\nLine 2 modified\nLine 3";
        
        String unified = DiffUtils.toUnifiedDiff(oldText, newText, "old.txt", "new.txt", 3);
        
        assertTrue("应包含旧文件标记", unified.contains("--- old.txt"));
        assertTrue("应包含新文件标记", unified.contains("+++ new.txt"));
        assertTrue("应包含hunk标记", unified.contains("@@"));
    }

    @Test
    public void testUnifiedDiffEmpty() {
        String unified = DiffUtils.toUnifiedDiff("", "", "a.txt", "b.txt", 3);
        assertTrue("空文本差异应包含文件标记", unified.contains("--- a.txt"));
    }

    // ==================== 差异项测试 ====================

    @Test
    public void testDiffItemToString() {
        DiffUtils.DiffItem insert = new DiffUtils.DiffItem(DiffUtils.DiffType.INSERT, "test");
        DiffUtils.DiffItem delete = new DiffUtils.DiffItem(DiffUtils.DiffType.DELETE, "test");
        DiffUtils.DiffItem equal = new DiffUtils.DiffItem(DiffUtils.DiffType.EQUAL, "test");
        
        assertEquals("插入项前缀应为+", "+test", insert.toString());
        assertEquals("删除项前缀应为-", "-test", delete.toString());
        assertEquals("相同项前缀应为空格", " test", equal.toString());
    }

    @Test
    public void testDiffItemEquals() {
        DiffUtils.DiffItem item1 = new DiffUtils.DiffItem(DiffUtils.DiffType.INSERT, "test");
        DiffUtils.DiffItem item2 = new DiffUtils.DiffItem(DiffUtils.DiffType.INSERT, "test");
        DiffUtils.DiffItem item3 = new DiffUtils.DiffItem(DiffUtils.DiffType.DELETE, "test");
        
        assertEquals("相同项应相等", item1, item2);
        assertNotEquals("不同类型应不等", item1, item3);
    }

    // ==================== 差异结果统计测试 ====================

    @Test
    public void testDiffResultStats() {
        String[] oldArr = {"a", "b", "c"};
        String[] newArr = {"a", "x", "y"};
        
        DiffUtils.DiffResult result = DiffUtils.diffArrays(oldArr, newArr);
        
        assertEquals("不变行数应为1", 1, result.unchanged);
        assertTrue("相似度应小于1", result.getSimilarity() < 1.0);
        assertTrue("变化率应大于0", result.getChangeRate() > 0);
    }

    @Test
    public void testGetSummary() {
        String oldText = "a\nb\nc";
        String newText = "a\nx\ny";
        
        DiffUtils.DiffResult result = DiffUtils.diff(oldText, newText);
        String summary = DiffUtils.getSummary(result);
        
        assertTrue("摘要应包含变更统计", summary.contains("变更统计"));
        assertTrue("摘要应包含相似度", summary.contains("相似度"));
    }

    // ==================== 差异位置查找测试 ====================

    @Test
    public void testFindDiffRanges() {
        List<int[]> ranges = DiffUtils.findDiffRanges("hello world", "hello java");
        
        assertFalse("应该找到差异范围", ranges.isEmpty());
        assertTrue("差异应在正确位置", ranges.get(0)[0] >= 0);
    }

    @Test
    public void testFindDiffRangesIdentical() {
        List<int[]> ranges = DiffUtils.findDiffRanges("test", "test");
        assertTrue("相同字符串应无差异范围", ranges.isEmpty());
    }

    @Test
    public void testFindDiffRangesNull() {
        List<int[]> ranges1 = DiffUtils.findDiffRanges(null, "test");
        List<int[]> ranges2 = DiffUtils.findDiffRanges("test", null);
        
        // 应该能处理null
        assertNotNull(ranges1);
        assertNotNull(ranges2);
    }

    // ==================== Patch应用测试 ====================

    @Test
    public void testApplyPatch() {
        String oldText = "Hello\nWorld";
        String newText = "Hello\nJava";
        
        DiffUtils.DiffResult diff = DiffUtils.diff(oldText, newText);
        String patched = DiffUtils.applyPatch(oldText, diff);
        
        assertEquals("应用patch后应等于新文本", newText, patched);
    }

    // ==================== 颜色输出测试 ====================

    @Test
    public void testColoredString() {
        String oldText = "a\nb";
        String newText = "a\nc";
        
        DiffUtils.DiffResult result = DiffUtils.diff(oldText, newText);
        String colored = DiffUtils.toColoredString(result);
        
        assertTrue("颜色输出应包含ANSI码", colored.contains("\u001B"));
        assertTrue("颜色输出应包含减号", colored.contains("-"));
        assertTrue("颜色输出应包含加号", colored.contains("+"));
    }

    // ==================== 复杂场景测试 ====================

    @Test
    public void testLargeTextDiff() {
        StringBuilder oldSb = new StringBuilder();
        StringBuilder newSb = new StringBuilder();
        
        for (int i = 0; i < 100; i++) {
            oldSb.append("Line ").append(i).append("\n");
            if (i % 2 == 0) {
                newSb.append("Line ").append(i).append("\n");
            } else {
                newSb.append("Modified Line ").append(i).append("\n");
            }
        }
        
        DiffUtils.DiffResult result = DiffUtils.diff(oldSb.toString(), newSb.toString());
        assertTrue("大文本应能正确比较", result.hasChanges());
    }

    @Test
    public void testUnicodeText() {
        String oldText = "你好\n世界";
        String newText = "你好\n宇宙";
        
        DiffUtils.DiffResult result = DiffUtils.diff(oldText, newText);
        assertTrue("Unicode文本应能正确比较", result.hasChanges());
    }

    @Test
    public void testMixedEndings() {
        String oldText = "Line1\nLine2\nLine3";
        String newText = "Line1\r\nLine2\r\nLine3";
        
        DiffUtils.DiffResult result = DiffUtils.diff(oldText, newText);
        // 不同换行符应检测到差异
        assertTrue("不同换行符应检测到差异", result.hasChanges() || result.getSimilarity() < 1.0);
    }
}