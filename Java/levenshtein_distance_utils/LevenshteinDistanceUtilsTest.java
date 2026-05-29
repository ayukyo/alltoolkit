import java.util.Arrays;
import java.util.List;

/**
 * LevenshteinDistanceUtils 测试类
 */
public class LevenshteinDistanceUtilsTest {
    
    private static int testsPassed = 0;
    private static int testsFailed = 0;
    
    public static void main(String[] args) {
        System.out.println("=== LevenshteinDistanceUtils 测试套件 ===\n");
        
        // 基本距离测试
        testDistance();
        
        // 相似度测试
        testSimilarity();
        
        // 编辑操作测试
        testEditOperations();
        
        // 模糊匹配测试
        testFuzzyMatch();
        
        // Damerau-Levenshtein 测试
        testDamerauLevenshtein();
        
        // LCS 测试
        testLCS();
        
        // 边界情况测试
        testEdgeCases();
        
        // 输出结果
        System.out.println("\n=== 测试结果 ===");
        System.out.println("通过: " + testsPassed);
        System.out.println("失败: " + testsFailed);
        System.out.println("总计: " + (testsPassed + testsFailed));
        
        if (testsFailed > 0) {
            System.exit(1);
        }
    }
    
    private static void testDistance() {
        System.out.println("--- 距离计算测试 ---");
        
        // 基本测试
        assertEquals(3, LevenshteinDistanceUtils.distance("kitten", "sitting"), 
            "kitten -> sitting 应该为 3");
        assertEquals(3, LevenshteinDistanceUtils.distance("sitting", "kitten"), 
            "sitting -> kitten 应该为 3");
        
        // 空字符串
        assertEquals(0, LevenshteinDistanceUtils.distance("", ""), 
            "空字符串距离应为 0");
        assertEquals(5, LevenshteinDistanceUtils.distance("hello", ""), 
            "hello -> 空 应该为 5");
        assertEquals(5, LevenshteinDistanceUtils.distance("", "world"), 
            "空 -> world 应该为 5");
        
        // 相同字符串
        assertEquals(0, LevenshteinDistanceUtils.distance("same", "same"), 
            "相同字符串距离应为 0");
        
        // 单字符操作
        assertEquals(1, LevenshteinDistanceUtils.distance("cat", "cats"), 
            "插入一个字符距离应为 1");
        assertEquals(1, LevenshteinDistanceUtils.distance("cats", "cat"), 
            "删除一个字符距离应为 1");
        assertEquals(1, LevenshteinDistanceUtils.distance("cat", "bat"), 
            "替换一个字符距离应为 1");
        
        // 完全不同
        assertEquals(3, LevenshteinDistanceUtils.distance("abc", "xyz"), 
            "完全不同的字符串");
        
        // 中文测试
        assertEquals(1, LevenshteinDistanceUtils.distance("你好", "你好吗"), 
            "中文插入测试");
        assertEquals(1, LevenshteinDistanceUtils.distance("世界", "世杰"), 
            "中文替换测试");
        
        // null 测试
        assertEquals(0, LevenshteinDistanceUtils.distance(null, null), 
            "两个 null 距离应为 0");
        assertEquals(4, LevenshteinDistanceUtils.distance(null, "test"), 
            "null -> test 应为 4");
        assertEquals(4, LevenshteinDistanceUtils.distance("test", null), 
            "test -> null 应为 4");
        
        System.out.println("距离计算测试通过!\n");
    }
    
    private static void testSimilarity() {
        System.out.println("--- 相似度计算测试 ---");
        
        // 完全相同
        assertEquals(1.0, LevenshteinDistanceUtils.similarity("hello", "hello"), 
            "相同字符串相似度应为 1.0");
        
        // 完全不同
        assertEquals(0.0, LevenshteinDistanceUtils.similarity("abc", "xyz"), 
            "完全不同字符串相似度应为 0.0");
        
        // 部分相似
        assertApproxEquals(0.571, LevenshteinDistanceUtils.similarity("kitten", "sitting"), 0.01,
            "kitten/sitting 相似度约为 0.571");
        
        // 百分比测试
        assertApproxEquals(57.14, LevenshteinDistanceUtils.similarityPercent("kitten", "sitting"), 1.0,
            "kitten/sitting 相似度百分比约为 57.14%");
        
        // 空字符串
        assertEquals(1.0, LevenshteinDistanceUtils.similarity("", ""), 
            "两个空字符串相似度应为 1.0");
        assertEquals(0.0, LevenshteinDistanceUtils.similarity("test", ""), 
            "非空和空字符串相似度应为 0.0");
        
        // null 测试
        assertEquals(1.0, LevenshteinDistanceUtils.similarity(null, null), 
            "两个 null 相似度应为 1.0");
        assertEquals(0.0, LevenshteinDistanceUtils.similarity(null, "test"), 
            "null 和非空相似度应为 0.0");
        
        System.out.println("相似度计算测试通过!\n");
    }
    
    private static void testEditOperations() {
        System.out.println("--- 编辑操作测试 ---");
        
        List<LevenshteinDistanceUtils.EditOperation> ops = 
            LevenshteinDistanceUtils.getEditOperations("kitten", "sitting");
        
        assertNotNull(ops, "编辑操作列表不应为 null");
        assertEquals(7, ops.size(), "kitten -> sitting 应有 7 个操作");
        
        // 验证编辑距离等于操作中的非匹配操作数
        int nonMatchOps = 0;
        for (LevenshteinDistanceUtils.EditOperation op : ops) {
            if (op.type != LevenshteinDistanceUtils.OperationType.MATCH) {
                nonMatchOps++;
            }
        }
        assertEquals(3, nonMatchOps, "非匹配操作数应为 3");
        
        // 格式化输出测试
        String formatted = LevenshteinDistanceUtils.formatEditScript("cat", "bat");
        assertNotNull(formatted, "格式化输出不应为 null");
        assertTrue(formatted.contains("替换"), "应包含替换操作");
        
        // 空操作测试
        ops = LevenshteinDistanceUtils.getEditOperations("", "");
        assertEquals(0, ops.size(), "空字符串编辑操作应为 0");
        
        // 纯插入测试
        ops = LevenshteinDistanceUtils.getEditOperations("", "abc");
        assertEquals(3, ops.size(), "空 -> abc 应有 3 个插入操作");
        for (LevenshteinDistanceUtils.EditOperation op : ops) {
            assertEquals(LevenshteinDistanceUtils.OperationType.INSERT, op.type, 
                "应全为插入操作");
        }
        
        // 纯删除测试
        ops = LevenshteinDistanceUtils.getEditOperations("abc", "");
        assertEquals(3, ops.size(), "abc -> 空应有 3 个删除操作");
        for (LevenshteinDistanceUtils.EditOperation op : ops) {
            assertEquals(LevenshteinDistanceUtils.OperationType.DELETE, op.type, 
                "应全为删除操作");
        }
        
        System.out.println("编辑操作测试通过!\n");
    }
    
    private static void testFuzzyMatch() {
        System.out.println("--- 模糊匹配测试 ---");
        
        List<String> candidates = Arrays.asList("apple", "banana", "orange", "grape", "pineapple");
        
        // 最佳匹配测试
        LevenshteinDistanceUtils.FuzzyMatchResult bestMatch = 
            LevenshteinDistanceUtils.findBestMatch("aple", candidates);
        
        assertNotNull(bestMatch, "最佳匹配不应为 null");
        assertEquals("apple", bestMatch.matchedString, "aple 的最佳匹配应为 apple");
        assertEquals(1, bestMatch.distance, "aple -> apple 距离应为 1");
        
        // 阈值匹配测试
        List<LevenshteinDistanceUtils.FuzzyMatchResult> matches = 
            LevenshteinDistanceUtils.findMatchesAboveThreshold("appl", candidates, 0.5);
        
        assertTrue(matches.size() > 0, "应有匹配结果");
        for (LevenshteinDistanceUtils.FuzzyMatchResult match : matches) {
            assertTrue(match.similarity >= 0.5, "所有匹配相似度应 >= 0.5");
        }
        
        // Top N 匹配测试
        List<LevenshteinDistanceUtils.FuzzyMatchResult> topMatches = 
            LevenshteinDistanceUtils.findTopMatches("bnnna", candidates, 3);
        
        assertEquals(3, topMatches.size(), "应返回 3 个结果");
        assertEquals("banana", topMatches.get(0).matchedString, "bnnna 最佳匹配应为 banana");
        
        // 相似度判断测试
        assertTrue(LevenshteinDistanceUtils.isSimilar("hello", "hallo", 0.6), 
            "hello/hallo 相似度应 >= 0.6");
        assertFalse(LevenshteinDistanceUtils.isSimilar("hello", "xyz", 0.6), 
            "hello/xyz 相似度应 < 0.6");
        
        // 空候选列表测试
        bestMatch = LevenshteinDistanceUtils.findBestMatch("test", Arrays.asList());
        assertNull(bestMatch, "空候选列表应返回 null");
        
        matches = LevenshteinDistanceUtils.findMatchesAboveThreshold("test", null, 0.5);
        assertEquals(0, matches.size(), "null 候选列表应返回空结果");
        
        System.out.println("模糊匹配测试通过!\n");
    }
    
    private static void testDamerauLevenshtein() {
        System.out.println("--- Damerau-Levenshtein 测试 ---");
        
        // 普通情况，与标准距离相同
        assertEquals(3, LevenshteinDistanceUtils.damerauLevenshteinDistance("kitten", "sitting"), 
            "kitten -> sitting D-L 距离应为 3");
        
        // 交换操作测试：ab -> ba
        // 标准 Levenshtein: 2 (替换 a->b, 替换 b->a)
        // Damerau-Levenshtein: 1 (交换)
        assertEquals(2, LevenshteinDistanceUtils.distance("ab", "ba"), 
            "标准距离 ab->ba 应为 2");
        assertEquals(1, LevenshteinDistanceUtils.damerauLevenshteinDistance("ab", "ba"), 
            "D-L 距离 ab->ba 应为 1 (交换)");
        
        // 更复杂的交换
        assertEquals(1, LevenshteinDistanceUtils.damerauLevenshteinDistance("abc", "acb"), 
            "D-L 距离 abc->acb 应为 1 (交换 bc)");
        
        // 多次交换
        assertEquals(2, LevenshteinDistanceUtils.damerauLevenshteinDistance("abcd", "badc"), 
            "D-L 距离 abcd->badc 应为 2 (两次交换)");
        
        System.out.println("Damerau-Levenshtein 测试通过!\n");
    }
    
    private static void testLCS() {
        System.out.println("--- 最长公共子序列测试 ---");
        
        // 基本 LCS 测试
        assertEquals(3, LevenshteinDistanceUtils.longestCommonSubsequenceLength("ABCD", "ACBD"), 
            "ABCD/ACBD LCS 长度应为 3 (ABD 或 ACD)");
        
        assertEquals(4, LevenshteinDistanceUtils.longestCommonSubsequenceLength("ABCDEF", "AEBDF"), 
            "ABCDEF/AEBDF LCS 长度应为 4 (ABDF)");
        
        // 完全相同
        assertEquals(5, LevenshteinDistanceUtils.longestCommonSubsequenceLength("hello", "hello"), 
            "相同字符串 LCS 长度应为 5");
        
        // 无公共子序列
        assertEquals(0, LevenshteinDistanceUtils.longestCommonSubsequenceLength("abc", "xyz"), 
            "无公共子序列时 LCS 长度应为 0");
        
        // 空字符串
        assertEquals(0, LevenshteinDistanceUtils.longestCommonSubsequenceLength("", "test"), 
            "空字符串 LCS 长度应为 0");
        assertEquals(0, LevenshteinDistanceUtils.longestCommonSubsequenceLength(null, "test"), 
            "null LCS 长度应为 0");
        
        // LCS 相似度测试
        assertApproxEquals(1.0, LevenshteinDistanceUtils.lcsSimilarity("hello", "hello"), 0.01, 
            "相同字符串 LCS 相似度应为 1.0");
        assertApproxEquals(0.0, LevenshteinDistanceUtils.lcsSimilarity("abc", "xyz"), 0.01, 
            "无公共子序列 LCS 相似度应为 0.0");
        
        System.out.println("最长公共子序列测试通过!\n");
    }
    
    private static void testEdgeCases() {
        System.out.println("--- 边界情况测试 ---");
        
        // 大字符串测试
        StringBuilder sb1 = new StringBuilder();
        StringBuilder sb2 = new StringBuilder();
        for (int i = 0; i < 1000; i++) {
            sb1.append("a");
            sb2.append(i % 100 == 0 ? "b" : "a");
        }
        long start = System.currentTimeMillis();
        int dist = LevenshteinDistanceUtils.distance(sb1.toString(), sb2.toString());
        long elapsed = System.currentTimeMillis() - start;
        assertTrue(dist >= 0, "大字符串距离计算应成功");
        assertTrue(elapsed < 1000, "大字符串距离计算应在 1 秒内完成");
        System.out.println("大字符串(1000字符)距离计算耗时: " + elapsed + "ms, 距离: " + dist);
        
        // Unicode 测试
        assertEquals(1, LevenshteinDistanceUtils.distance("日本", "日本人"), 
            "Unicode 插入测试");
        assertEquals(2, LevenshteinDistanceUtils.distance("🎉🎊", "🎉🎈🎊"), 
            "Emoji 测试");
        
        // 空格和特殊字符
        assertEquals(0, LevenshteinDistanceUtils.distance("  ", "  "), 
            "空格字符串测试");
        assertEquals(1, LevenshteinDistanceUtils.distance("\n", "\r\n"), 
            "换行符测试");
        
        // 单个字符
        assertEquals(0, LevenshteinDistanceUtils.distance("a", "a"), 
            "单字符相同测试");
        assertEquals(1, LevenshteinDistanceUtils.distance("a", "b"), 
            "单字符不同测试");
        
        System.out.println("边界情况测试通过!\n");
    }
    
    // ==================== 辅助断言方法 ====================
    
    private static void assertEquals(Object expected, Object actual, String message) {
        if (expected == null && actual == null) {
            testsPassed++;
            return;
        }
        if (expected != null && expected.equals(actual)) {
            testsPassed++;
            return;
        }
        testsFailed++;
        System.err.println("失败: " + message);
        System.err.println("  期望: " + expected);
        System.err.println("  实际: " + actual);
    }
    
    private static void assertEquals(int expected, int actual, String message) {
        if (expected == actual) {
            testsPassed++;
            return;
        }
        testsFailed++;
        System.err.println("失败: " + message);
        System.err.println("  期望: " + expected);
        System.err.println("  实际: " + actual);
    }
    
    private static void assertEquals(double expected, double actual, String message) {
        if (Double.compare(expected, actual) == 0) {
            testsPassed++;
            return;
        }
        testsFailed++;
        System.err.println("失败: " + message);
        System.err.println("  期望: " + expected);
        System.err.println("  实际: " + actual);
    }
    
    private static void assertApproxEquals(double expected, double actual, double delta, String message) {
        if (Math.abs(expected - actual) <= delta) {
            testsPassed++;
            return;
        }
        testsFailed++;
        System.err.println("失败: " + message);
        System.err.println("  期望: " + expected + " (±" + delta + ")");
        System.err.println("  实际: " + actual);
    }
    
    private static void assertTrue(boolean condition, String message) {
        if (condition) {
            testsPassed++;
            return;
        }
        testsFailed++;
        System.err.println("失败: " + message);
    }
    
    private static void assertFalse(boolean condition, String message) {
        if (!condition) {
            testsPassed++;
            return;
        }
        testsFailed++;
        System.err.println("失败: " + message);
    }
    
    private static void assertNotNull(Object obj, String message) {
        if (obj != null) {
            testsPassed++;
            return;
        }
        testsFailed++;
        System.err.println("失败: " + message);
    }
    
    private static void assertNull(Object obj, String message) {
        if (obj == null) {
            testsPassed++;
            return;
        }
        testsFailed++;
        System.err.println("失败: " + message);
    }
}