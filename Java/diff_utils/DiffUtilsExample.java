package diff_utils;

/**
 * DiffUtils 示例程序
 * 
 * @author AllToolkit
 */
public class DiffUtilsExample {
    
    public static void main(String[] args) {
        System.out.println("=".repeat(60));
        System.out.println("DiffUtils 示例程序");
        System.out.println("=".repeat(60));
        
        // 示例1: 基本文本比较
        System.out.println("\n【示例1】基本文本比较");
        System.out.println("-".repeat(40));
        example1();
        
        // 示例2: 字符级别比较
        System.out.println("\n【示例2】字符级别比较");
        System.out.println("-".repeat(40));
        example2();
        
        // 示例3: 编辑距离和相似度
        System.out.println("\n【示例3】编辑距离和相似度");
        System.out.println("-".repeat(40));
        example3();
        
        // 示例4: LCS算法
        System.out.println("\n【示例4】最长公共子序列/子串");
        System.out.println("-".repeat(40));
        example4();
        
        // 示例5: Unified Diff格式
        System.out.println("\n【示例5】Unified Diff格式");
        System.out.println("-".repeat(40));
        example5();
        
        // 示例6: 数组比较
        System.out.println("\n【示例6】数组比较");
        System.out.println("-".repeat(40));
        example6();
        
        // 运行测试
        System.out.println("\n【测试】运行单元测试");
        System.out.println("=".repeat(60));
        runTests();
    }
    
    private static void example1() {
        String oldText = "Hello\nWorld\nJava";
        String newText = "Hello\nJava\nWorld";
        
        DiffUtils.DiffResult result = DiffUtils.diff(oldText, newText);
        
        System.out.println("旧文本:");
        System.out.println("  " + oldText.replace("\n", "\n  "));
        System.out.println("新文本:");
        System.out.println("  " + newText.replace("\n", "\n  "));
        System.out.println("\n差异结果:");
        
        for (DiffUtils.DiffItem item : result.items) {
            String[] lines = item.content.split("\n");
            for (String line : lines) {
                switch (item.type) {
                    case INSERT:
                        System.out.println("  \033[32m+ " + line + "\033[0m");
                        break;
                    case DELETE:
                        System.out.println("  \033[31m- " + line + "\033[0m");
                        break;
                    case EQUAL:
                        System.out.println("    " + line);
                        break;
                }
            }
        }
        
        System.out.println("\n" + DiffUtils.getSummary(result));
    }
    
    private static void example2() {
        String s1 = "kitten";
        String s2 = "sitting";
        
        System.out.println("字符串1: " + s1);
        System.out.println("字符串2: " + s2);
        
        DiffUtils.DiffResult result = DiffUtils.diff(s1, s2, false);
        
        System.out.print("字符级差异: ");
        for (DiffUtils.DiffItem item : result.items) {
            switch (item.type) {
                case INSERT:
                    System.out.print("\033[32m+" + item.content + "\033[0m");
                    break;
                case DELETE:
                    System.out.print("\033[31m-" + item.content + "\033[0m");
                    break;
                case EQUAL:
                    System.out.print(item.content);
                    break;
            }
        }
        System.out.println();
    }
    
    private static void example3() {
        String[] pairs = {
            "kitten", "sitting",
            "book", "back",
            "algorithm", "altruistic",
            "hello", "hello"
        };
        
        for (int i = 0; i < pairs.length; i += 2) {
            String s1 = pairs[i];
            String s2 = pairs[i + 1];
            int dist = DiffUtils.levenshteinDistance(s1, s2);
            double sim = DiffUtils.similarity(s1, s2);
            System.out.printf("'%s' vs '%s'%n", s1, s2);
            System.out.printf("  编辑距离: %d, 相似度: %.1f%%%n", dist, sim * 100);
        }
    }
    
    private static void example4() {
        String s1 = "ABCBDAB";
        String s2 = "BDCABA";
        
        System.out.println("字符串1: " + s1);
        System.out.println("字符串2: " + s2);
        
        String lcsStr = DiffUtils.longestCommonSubstring(s1, s2);
        String lcsSeq = DiffUtils.longestCommonSubsequence(s1, s2);
        
        System.out.println("最长公共子串 (连续): " + lcsStr);
        System.out.println("最长公共子序列 (可非连续): " + lcsSeq);
    }
    
    private static void example5() {
        String oldText = "Line 1\nLine 2\nLine 3\nLine 4\nLine 5";
        String newText = "Line 1\nLine 2 modified\nLine 3\nLine 4 new\nLine 5";
        
        String unified = DiffUtils.toUnifiedDiff(oldText, newText, "original.txt", "modified.txt", 1);
        System.out.println(unified);
    }
    
    private static void example6() {
        String[] oldArr = {"apple", "banana", "cherry", "date"};
        String[] newArr = {"apple", "blueberry", "cherry", "elderberry"};
        
        System.out.println("旧数组: " + String.join(", ", oldArr));
        System.out.println("新数组: " + String.join(", ", newArr));
        
        DiffUtils.DiffResult result = DiffUtils.diffArrays(oldArr, newArr);
        
        System.out.println("\n差异:");
        for (DiffUtils.DiffItem item : result.items) {
            String[] lines = item.content.split("\n");
            for (String line : lines) {
                System.out.println("  " + item.toString().charAt(0) + " " + line);
            }
        }
        
        System.out.println("\n" + DiffUtils.getSummary(result));
    }
    
    private static void runTests() {
        int passed = 0;
        int failed = 0;
        
        // 测试1: 相同文本
        if (!DiffUtils.diff("test", "test").hasChanges()) {
            passed++;
            System.out.println("✓ 测试1: 相同文本检测");
        } else {
            failed++;
            System.out.println("✗ 测试1 失败");
        }
        
        // 测试2: 不同文本
        if (DiffUtils.diff("hello", "world").hasChanges()) {
            passed++;
            System.out.println("✓ 测试2: 不同文本检测");
        } else {
            failed++;
            System.out.println("✗ 测试2 失败");
        }
        
        // 测试3: 编辑距离
        if (DiffUtils.levenshteinDistance("kitten", "sitting") == 3) {
            passed++;
            System.out.println("✓ 测试3: 编辑距离计算");
        } else {
            failed++;
            System.out.println("✗ 测试3 失败");
        }
        
        // 测试4: 相似度
        double sim = DiffUtils.similarity("hello", "hello");
        if (sim == 1.0) {
            passed++;
            System.out.println("✓ 测试4: 相似度计算");
        } else {
            failed++;
            System.out.println("✗ 测试4 失败");
        }
        
        // 测试5: LCS
        String lcs = DiffUtils.longestCommonSubsequence("ABCBDAB", "BDCABA");
        if (lcs.length() == 4) {
            passed++;
            System.out.println("✓ 测试5: 最长公共子序列");
        } else {
            failed++;
            System.out.println("✗ 测试5 失败: " + lcs);
        }
        
        // 测试6: 最长公共子串
        String substr = DiffUtils.longestCommonSubstring("ABABC", "ABCBA");
        if (substr.equals("ABC") || substr.equals("BAB")) {
            passed++;
            System.out.println("✓ 测试6: 最长公共子串");
        } else {
            failed++;
            System.out.println("✗ 测试6 失败: " + substr);
        }
        
        // 测试7: 空文本处理
        if (!DiffUtils.diff("", "").hasChanges()) {
            passed++;
            System.out.println("✓ 测试7: 空文本处理");
        } else {
            failed++;
            System.out.println("✗ 测试7 失败");
        }
        
        // 测试8: null处理
        if (!DiffUtils.diff(null, null).hasChanges()) {
            passed++;
            System.out.println("✓ 测试8: null处理");
        } else {
            failed++;
            System.out.println("✗ 测试8 失败");
        }
        
        // 测试9: 快速比较
        if (DiffUtils.quickCompare("test", "test") && !DiffUtils.quickCompare("test", "test2")) {
            passed++;
            System.out.println("✓ 测试9: 快速比较");
        } else {
            failed++;
            System.out.println("✗ 测试9 失败");
        }
        
        // 测试10: 数组比较
        String[] arr1 = {"a", "b", "c"};
        String[] arr2 = {"a", "x", "c"};
        DiffUtils.DiffResult arrResult = DiffUtils.diffArrays(arr1, arr2);
        if (arrResult.hasChanges() && arrResult.unchanged == 2) {
            passed++;
            System.out.println("✓ 测试10: 数组比较");
        } else {
            failed++;
            System.out.println("✗ 测试10 失败");
        }
        
        // 测试11: Unicode支持
        DiffUtils.DiffResult unicodeResult = DiffUtils.diff("你好", "世界");
        if (unicodeResult.hasChanges()) {
            passed++;
            System.out.println("✓ 测试11: Unicode支持");
        } else {
            failed++;
            System.out.println("✗ 测试11 失败");
        }
        
        // 测试12: 统计信息
        DiffUtils.DiffResult statResult = DiffUtils.diff("a\nb\nc", "a\nx\nc");
        String summary = DiffUtils.getSummary(statResult);
        if (summary.contains("变更统计") && summary.contains("相似度")) {
            passed++;
            System.out.println("✓ 测试12: 统计信息");
        } else {
            failed++;
            System.out.println("✗ 测试12 失败");
        }
        
        System.out.println("\n" + "=".repeat(60));
        System.out.printf("测试结果: %d 通过, %d 失败%n", passed, failed);
        System.out.println("=".repeat(60));
    }
}