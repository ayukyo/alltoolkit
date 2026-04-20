package trie_utils;

import java.util.List;

/**
 * Trie 测试类
 * 包含完整的单元测试
 */
public class TrieTest {
    private int testsRun = 0;
    private int testsPassed = 0;
    private int testsFailed = 0;
    
    public static void main(String[] args) {
        TrieTest test = new TrieTest();
        test.runAllTests();
        test.printSummary();
    }
    
    public void runAllTests() {
        System.out.println("=== Trie 工具模块测试 ===\n");
        
        // 基本操作测试
        testInsert();
        testSearch();
        testStartsWith();
        testDelete();
        testClear();
        testEmpty();
        
        // 词频统计测试
        testWordCount();
        testSize();
        
        // 自动补全测试
        testAutocomplete();
        testGetWordsWithPrefix();
        
        // 高级功能测试
        testGetAllWords();
        testLongestCommonPrefix();
        testCountWordsWithPrefix();
        testFuzzySearch();
        
        // 边界情况测试
        testNullAndEmpty();
        testUnicode();
    }
    
    // ==================== 基本操作测试 ====================
    
    private void testInsert() {
        System.out.println("测试: insert() - 插入单词");
        
        Trie trie = new Trie();
        assertTrue("插入非空单词应返回 true", trie.insert("hello"));
        assertTrue("插入非空单词应返回 true", trie.insert("world"));
        assertFalse("插入空字符串应返回 false", trie.insert(""));
        assertFalse("插入 null 应返回 false", trie.insert(null));
        
        testsRun += 4;
        System.out.println();
    }
    
    private void testSearch() {
        System.out.println("测试: search() - 搜索单词");
        
        Trie trie = new Trie();
        trie.insert("apple");
        trie.insert("app");
        trie.insert("application");
        
        assertTrue("应找到 'apple'", trie.search("apple"));
        assertTrue("应找到 'app'", trie.search("app"));
        assertTrue("应找到 'application'", trie.search("application"));
        assertFalse("不应找到 'appl'", trie.search("appl"));
        assertFalse("不应找到 'orange'", trie.search("orange"));
        assertFalse("搜索 null 应返回 false", trie.search(null));
        
        testsRun += 6;
        System.out.println();
    }
    
    private void testStartsWith() {
        System.out.println("测试: startsWith() - 前缀检查");
        
        Trie trie = new Trie();
        trie.insert("apple");
        trie.insert("application");
        trie.insert("app");
        
        assertTrue("应有以 'app' 开头的单词", trie.startsWith("app"));
        assertTrue("应有以 'apple' 开头的单词", trie.startsWith("apple"));
        assertFalse("不应有以 'banana' 开头的单词", trie.startsWith("banana"));
        assertFalse("检查 null 前缀应返回 false", trie.startsWith(null));
        
        testsRun += 4;
        System.out.println();
    }
    
    private void testDelete() {
        System.out.println("测试: delete() - 删除单词");
        
        Trie trie = new Trie();
        trie.insert("apple");
        trie.insert("app");
        trie.insert("application");
        
        assertTrue("删除 'apple' 应成功", trie.delete("apple"));
        assertFalse("删除后不应找到 'apple'", trie.search("apple"));
        assertTrue("'app' 应仍然存在", trie.search("app"));
        assertTrue("'application' 应仍然存在", trie.search("application"));
        
        assertFalse("再次删除 'apple' 应失败", trie.delete("apple"));
        assertFalse("删除不存在的单词应返回 false", trie.delete("orange"));
        assertFalse("删除 null 应返回 false", trie.delete(null));
        assertFalse("删除空字符串应返回 false", trie.delete(""));
        
        testsRun += 7;
        System.out.println();
    }
    
    private void testClear() {
        System.out.println("测试: clear() - 清空 Trie");
        
        Trie trie = new Trie();
        trie.insert("one");
        trie.insert("two");
        trie.insert("three");
        
        trie.clear();
        assertEquals("清空后 size 应为 0", 0, trie.size());
        assertFalse("清空后不应找到 'one'", trie.search("one"));
        assertTrue("清空后应为空", trie.isEmpty());
        
        testsRun += 3;
        System.out.println();
    }
    
    private void testEmpty() {
        System.out.println("测试: isEmpty() - 空检查");
        
        Trie trie = new Trie();
        assertTrue("新 Trie 应为空", trie.isEmpty());
        assertEquals("新 Trie 大小应为 0", 0, trie.size());
        
        trie.insert("test");
        assertFalse("插入后不应为空", trie.isEmpty());
        assertEquals("插入后大小应为 1", 1, trie.size());
        
        trie.delete("test");
        assertTrue("删除全部后应为空", trie.isEmpty());
        assertEquals("删除后大小应为 0", 0, trie.size());
        
        testsRun += 5;
        System.out.println();
    }
    
    // ==================== 词频统计测试 ====================
    
    private void testWordCount() {
        System.out.println("测试: getWordCount() - 词频统计");
        
        Trie trie = new Trie();
        trie.insert("hello");
        trie.insert("hello");
        trie.insert("hello");
        trie.insert("world");
        
        assertEquals("'hello' 计数应为 3", 3, trie.getWordCount("hello"));
        assertEquals("'world' 计数应为 1", 1, trie.getWordCount("world"));
        assertEquals("不存在单词计数应为 0", 0, trie.getWordCount("nonexistent"));
        
        testsRun += 3;
        System.out.println();
    }
    
    private void testSize() {
        System.out.println("测试: size() - 总单词数");
        
        Trie trie = new Trie();
        assertEquals("空 Trie 大小为 0", 0, trie.size());
        
        trie.insert("one");
        trie.insert("two");
        trie.insert("three");
        // 注意: 重复插入会更新计数但不增加总词数
        trie.insert("one"); 
        
        assertEquals("应有 3 个不同单词", 3, trie.size());
        
        testsRun += 2;
        System.out.println();
    }
    
    // ==================== 自动补全测试 ====================
    
    private void testAutocomplete() {
        System.out.println("测试: autocomplete() - 自动补全");
        
        Trie trie = new Trie();
        trie.insert("apple");
        trie.insert("app"); // 插入两次, 词频更高
        trie.insert("app");
        trie.insert("application");
        trie.insert("append");
        trie.insert("banana");
        trie.insert("band");
        
        List<String> suggestions = trie.autocomplete("app", 3);
        assertEquals("应有 3 个建议", 3, suggestions.size());
        assertTrue("应包含 'app'", suggestions.contains("app"));
        assertTrue("应包含 'apple'", suggestions.contains("apple"));
        
        // 词频最高的应排在前面
        assertEquals("'app' (词频2) 应排第一", "app", suggestions.get(0));
        
        // 测试限制
        List<String> limited = trie.autocomplete("app", 2);
        assertEquals("限制后应有 2 个建议", 2, limited.size());
        
        // 测试不存在的前缀
        List<String> empty = trie.autocomplete("xyz");
        assertTrue("不存在前缀应返回空", empty.isEmpty());
        
        // 测试 null 和负数
        assertTrue("null 前缀应返回空", trie.autocomplete(null).isEmpty());
        assertTrue("maxSuggestions <= 0 应返回空", trie.autocomplete("app", 0).isEmpty());
        
        testsRun += 6;
        System.out.println();
    }
    
    private void testGetWordsWithPrefix() {
        System.out.println("测试: getWordsWithPrefix() - 获取前缀单词");
        
        Trie trie = new Trie();
        trie.insert("cat");
        trie.insert("category");
        trie.insert("catalog");
        trie.insert("dog");
        
        List<String> catWords = trie.getWordsWithPrefix("cat");
        assertEquals("应有 3 个以 'cat' 开头的单词", 3, catWords.size());
        assertTrue("应包含 'cat'", catWords.contains("cat"));
        assertTrue("应包含 'category'", catWords.contains("category"));
        assertTrue("应包含 'catalog'", catWords.contains("catalog"));
        
        List<String> empty = trie.getWordsWithPrefix("xyz");
        assertTrue("不存在前缀应返回空", empty.isEmpty());
        
        testsRun += 3;
        System.out.println();
    }
    
    // ==================== 高级功能测试 ====================
    
    private void testGetAllWords() {
        System.out.println("测试: getAllWords() - 获取所有单词");
        
        Trie trie = new Trie();
        trie.insert("red");
        trie.insert("green");
        trie.insert("blue");
        
        List<String> allWords = trie.getAllWords();
        assertEquals("应有 3 个单词", 3, allWords.size());
        assertTrue("应包含 'red'", allWords.contains("red"));
        assertTrue("应包含 'green'", allWords.contains("green"));
        assertTrue("应包含 'blue'", allWords.contains("blue"));
        
        testsRun += 4;
        System.out.println();
    }
    
    private void testLongestCommonPrefix() {
        System.out.println("测试: getLongestCommonPrefix() - 最长公共前缀");
        
        Trie trie = new Trie();
        trie.insert("flower");
        trie.insert("flow");
        trie.insert("flight");
        
        assertEquals("最长公共前缀应为 'fl'", "fl", trie.getLongestCommonPrefix());
        
        Trie trie2 = new Trie();
        trie2.insert("dog");
        trie2.insert("cat");
        trie2.insert("bird");
        
        assertEquals("无公共前缀应为空字符串", "", trie2.getLongestCommonPrefix());
        
        Trie trie3 = new Trie();
        assertEquals("空 Trie 最长公共前缀应为空", "", trie3.getLongestCommonPrefix());
        
        testsRun += 3;
        System.out.println();
    }
    
    private void testCountWordsWithPrefix() {
        System.out.println("测试: countWordsWithPrefix() - 统计前缀单词数");
        
        Trie trie = new Trie();
        trie.insert("pre");
        trie.insert("prefix");
        trie.insert("prepare");
        trie.insert("prevent");
        trie.insert("preflight");
        trie.insert("other");
        
        assertEquals("以 'pre' 开头的单词应有 5 个", 5, trie.countWordsWithPrefix("pre"));
        assertEquals("以 'pref' 开头的单词应有 2 个", 2, trie.countWordsWithPrefix("pref"));
        assertEquals("不存在的前缀应为 0", 0, trie.countWordsWithPrefix("xyz"));
        
        testsRun += 3;
        System.out.println();
    }
    
    private void testFuzzySearch() {
        System.out.println("测试: fuzzySearch() - 模糊搜索");
        
        Trie trie = new Trie();
        trie.insert("hello");
        trie.insert("hallo");
        trie.insert("help");
        trie.insert("held");
        trie.insert("world");
        
        // 编辑距离为 1
        List<String> results = trie.fuzzySearch("helo", 1);
        assertTrue("应找到 'hello' (插入 l)", results.contains("hello"));
        // hallo 编辑距离为 2, 不应在距离 1 内找到
        assertTrue("应找到 'help' (替换 o->p)", results.contains("help"));
        assertTrue("应找到 'held' (替换 o->d)", results.contains("held"));
        
        // 编辑距离为 2 应找到更多
        List<String> results2 = trie.fuzzySearch("helo", 2);
        assertTrue("距离 2 应找到 'hallo'", results2.contains("hallo"));
        
        // 编辑距离为 0 应等于精确匹配
        List<String> exact = trie.fuzzySearch("hello", 0);
        assertTrue("编辑距离 0 应等于精确匹配", exact.contains("hello"));
        
        // null 和负数测试
        assertTrue("null 应返回空", trie.fuzzySearch(null, 1).isEmpty());
        assertTrue("负距离应返回空", trie.fuzzySearch("hello", -1).isEmpty());
        
        testsRun += 7;
        System.out.println();
    }
    
    // ==================== 边界情况测试 ====================
    
    private void testNullAndEmpty() {
        System.out.println("测试: 边界情况 - null 和空值处理");
        
        Trie trie = new Trie();
        
        // null 操作
        assertFalse("插入 null 应返回 false", trie.insert(null));
        assertFalse("搜索 null 应返回 false", trie.search(null));
        assertFalse("删除 null 应返回 false", trie.delete(null));
        assertFalse("null 前缀检查应返回 false", trie.startsWith(null));
        
        // 空字符串操作
        assertFalse("插入空字符串应返回 false", trie.insert(""));
        assertFalse("搜索空字符串应返回 false", trie.search(""));
        
        testsRun += 6;
        System.out.println();
    }
    
    private void testUnicode() {
        System.out.println("测试: Unicode 支持");
        
        Trie trie = new Trie();
        
        trie.insert("你好");
        trie.insert("你好吗");
        trie.insert("你们好");
        trie.insert("こんにちは");
        trie.insert("안녕하세요");
        
        assertTrue("应找到中文 '你好'", trie.search("你好"));
        assertTrue("应有 '你好' 前缀", trie.startsWith("你好"));
        
        List<String> suggestions = trie.autocomplete("你好");
        assertEquals("应有 2 个中文建议", 2, suggestions.size());
        
        assertTrue("应找到日文", trie.search("こんにちは"));
        assertTrue("应找到韩文", trie.search("안녕하세요"));
        
        testsRun += 5;
        System.out.println();
    }
    
    // ==================== 断言辅助方法 ====================
    
    private void assertTrue(String message, boolean condition) {
        if (condition) {
            System.out.println("  ✓ " + message);
            testsPassed++;
        } else {
            System.out.println("  ✗ " + message);
            testsFailed++;
        }
    }
    
    private void assertFalse(String message, boolean condition) {
        assertTrue(message, !condition);
    }
    
    private void assertEquals(String message, Object expected, Object actual) {
        boolean passed = (expected == null && actual == null) || 
                        (expected != null && expected.equals(actual));
        if (passed) {
            System.out.println("  ✓ " + message + " (期望: " + expected + ", 实际: " + actual + ")");
            testsPassed++;
        } else {
            System.out.println("  ✗ " + message + " (期望: " + expected + ", 实际: " + actual + ")");
            testsFailed++;
        }
    }
    
    private void printSummary() {
        System.out.println("\n=== 测试总结 ===");
        System.out.println("总计: " + testsRun + " 个测试");
        System.out.println("通过: " + testsPassed);
        System.out.println("失败: " + testsFailed);
        
        if (testsFailed == 0) {
            System.out.println("\n✅ 所有测试通过!");
        } else {
            System.out.println("\n❌ 有 " + testsFailed + " 个测试失败");
        }
    }
}