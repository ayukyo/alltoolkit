import java.util.Arrays;
import java.util.List;

/**
 * LevenshteinDistanceUtils 使用示例
 * 
 * 展示编辑距离计算、相似度分析、模糊搜索等功能
 */
public class LevenshteinDistanceExamples {
    
    public static void main(String[] args) {
        System.out.println("╔══════════════════════════════════════════════════════════╗");
        System.out.println("║     Levenshtein 距离工具 - 使用示例                      ║");
        System.out.println("╚══════════════════════════════════════════════════════════╝\n");
        
        // 示例 1: 基本距离计算
        example1_BasicDistance();
        
        // 示例 2: 相似度计算
        example2_Similarity();
        
        // 示例 3: 编辑操作序列
        example3_EditOperations();
        
        // 示例 4: 拼写检查/建议
        example4_SpellCheck();
        
        // 示例 5: 模糊搜索
        example5_FuzzySearch();
        
        // 示例 6: Damerau-Levenshtein（支持交换）
        example6_DamerauLevenshtein();
        
        // 示例 7: 最长公共子序列
        example7_LCS();
        
        // 示例 8: 实际应用场景
        example8_RealWorldScenarios();
    }
    
    /**
     * 示例 1: 基本距离计算
     */
    private static void example1_BasicDistance() {
        System.out.println("━━━ 示例 1: 基本距离计算 ━━━");
        
        String[][] pairs = {
            {"kitten", "sitting"},
            {"algorithm", "logarithm"},
            {"flaw", "lawn"},
            {"saturday", "sunday"},
            {"book", "back"},
            {"Python", "Java"},
            {"你好世界", "你好吗世界"}
        };
        
        System.out.println("\n字符串对\t\t\t编辑距离");
        System.out.println("─────────────────────────────────────");
        
        for (String[] pair : pairs) {
            int dist = LevenshteinDistanceUtils.distance(pair[0], pair[1]);
            System.out.printf("%-15s → %-15s  %d%n", pair[0], pair[1], dist);
        }
        
        System.out.println();
    }
    
    /**
     * 示例 2: 相似度计算
     */
    private static void example2_Similarity() {
        System.out.println("━━━ 示例 2: 相似度计算 ━━━");
        
        String[][] pairs = {
            {"hello", "hello"},      // 完全相同
            {"hello", "hallo"},      // 高度相似
            {"hello", "hi"},         // 低相似度
            {"hello", "world"},      // 完全不同
            {"数据科学家", "数据分析师"}  // 中文
        };
        
        System.out.println("\n字符串对\t\t\t相似度");
        System.out.println("─────────────────────────────────────────");
        
        for (String[] pair : pairs) {
            double sim = LevenshteinDistanceUtils.similarity(pair[0], pair[1]);
            double percent = LevenshteinDistanceUtils.similarityPercent(pair[0], pair[1]);
            String bar = generateBar(sim, 20);
            System.out.printf("%-12s → %-12s  %.2f%%  %s%n", 
                pair[0], pair[1], percent, bar);
        }
        
        System.out.println();
    }
    
    /**
     * 示例 3: 编辑操作序列
     */
    private static void example3_EditOperations() {
        System.out.println("━━━ 示例 3: 编辑操作序列 ━━━");
        
        String source = "intention";
        String target = "execution";
        
        System.out.println("\n转换 \"" + source + "\" → \"" + target + "\"\n");
        
        int distance = LevenshteinDistanceUtils.distance(source, target);
        System.out.println("编辑距离: " + distance);
        System.out.println();
        
        String editScript = LevenshteinDistanceUtils.formatEditScript(source, target);
        System.out.println(editScript);
        
        // 详细操作列表
        System.out.println("操作详情:");
        List<LevenshteinDistanceUtils.EditOperation> ops = 
            LevenshteinDistanceUtils.getEditOperations(source, target);
        
        int step = 1;
        for (LevenshteinDistanceUtils.EditOperation op : ops) {
            String icon = "";
            switch (op.type) {
                case MATCH: icon = "✓"; break;
                case INSERT: icon = "+"; break;
                case DELETE: icon = "-"; break;
                case REPLACE: icon = "↔"; break;
            }
            System.out.printf("  %d. [%s] %s%n", step++, icon, op.toString());
        }
        
        System.out.println();
    }
    
    /**
     * 示例 4: 拼写检查/建议
     */
    private static void example4_SpellCheck() {
        System.out.println("━━━ 示例 4: 拼写检查建议 ━━━");
        
        // 模拟字典
        List<String> dictionary = Arrays.asList(
            "apple", "application", "applet", "appliance", "apply",
            "banana", "bandana", "balance", "base",
            "computer", "compute", "commute", "compact",
            "developer", "develop", "development", "device"
        );
        
        String[] misspelledWords = {"aple", "banan", "compter", "devloper"};
        
        System.out.println("\n拼写检查建议 (阈值 >= 0.5):");
        System.out.println("─────────────────────────────────────────────");
        
        for (String word : misspelledWords) {
            System.out.println("\n输入: \"" + word + "\"");
            
            List<LevenshteinDistanceUtils.FuzzyMatchResult> suggestions = 
                LevenshteinDistanceUtils.findMatchesAboveThreshold(word, dictionary, 0.5);
            
            if (suggestions.isEmpty()) {
                System.out.println("  未找到建议");
            } else {
                for (int i = 0; i < Math.min(3, suggestions.size()); i++) {
                    LevenshteinDistanceUtils.FuzzyMatchResult match = suggestions.get(i);
                    System.out.printf("  %d. %s (相似度: %.1f%%, 距离: %d)%n",
                        i + 1, match.matchedString, 
                        match.similarity * 100, match.distance);
                }
            }
        }
        
        System.out.println();
    }
    
    /**
     * 示例 5: 模糊搜索
     */
    private static void example5_FuzzySearch() {
        System.out.println("━━━ 示例 5: 模糊搜索 ━━━");
        
        List<String> products = Arrays.asList(
            "iPhone 15 Pro Max", "iPhone 15 Pro", "iPhone 15", "iPhone 14",
            "Samsung Galaxy S24", "Samsung Galaxy Z Fold", "Samsung Galaxy A54",
            "Google Pixel 8 Pro", "Google Pixel 8",
            "OnePlus 12", "OnePlus Open"
        );
        
        String[] queries = {"iphone", "samsang", "pixel pro", "oneplus"};
        
        for (String query : queries) {
            System.out.println("\n搜索: \"" + query + "\"");
            System.out.println("────────────────────────────");
            
            List<LevenshteinDistanceUtils.FuzzyMatchResult> results = 
                LevenshteinDistanceUtils.findTopMatches(query, products, 3);
            
            for (int i = 0; i < results.size(); i++) {
                LevenshteinDistanceUtils.FuzzyMatchResult result = results.get(i);
                System.out.printf("  %d. %-25s 相似度: %5.1f%%%n",
                    i + 1, result.matchedString, result.similarity * 100);
            }
        }
        
        System.out.println();
    }
    
    /**
     * 示例 6: Damerau-Levenshtein（支持相邻字符交换）
     */
    private static void example6_DamerauLevenshtein() {
        System.out.println("━━━ 示例 6: Damerau-Levenshtein（支持交换操作） ━━━");
        
        String[][] pairs = {
            {"ab", "ba"},           // 单次交换
            {"abc", "acb"},         // 单次交换
            {"abcd", "badc"},       // 两次交换
            {"receive", "recieve"}, // 常见拼写错误
            {"the", "hte"}          // 打字交换
        };
        
        System.out.println("\n字符串对\t\t标准L距离\tD-L距离\t\t说明");
        System.out.println("─────────────────────────────────────────────────────");
        
        for (String[] pair : pairs) {
            int standard = LevenshteinDistanceUtils.distance(pair[0], pair[1]);
            int damerau = LevenshteinDistanceUtils.damerauLevenshteinDistance(pair[0], pair[1]);
            String note = standard == damerau ? "" : "交换节省 " + (standard - damerau) + " 步";
            
            System.out.printf("%-10s → %-10s  %d\t\t%d\t\t%s%n",
                pair[0], pair[1], standard, damerau, note);
        }
        
        System.out.println("\n💡 Damerau-Levenshtein 将相邻字符交换视为单次操作，");
        System.out.println("   更适合检测打字错误场景。");
        System.out.println();
    }
    
    /**
     * 示例 7: 最长公共子序列
     */
    private static void example7_LCS() {
        System.out.println("━━━ 示例 7: 最长公共子序列 (LCS) ━━━");
        
        String[][] pairs = {
            {"ABCDEF", "AEBDF"},
            {"XMJYAUZ", "MZJAWXU"},
            {"这是测试文本", "这是示例文本"},
            {"programming", "gaming"}
        };
        
        System.out.println("\n字符串对\t\t\tLCS长度\tLCS相似度");
        System.out.println("─────────────────────────────────────────");
        
        for (String[] pair : pairs) {
            int lcsLen = LevenshteinDistanceUtils.longestCommonSubsequenceLength(pair[0], pair[1]);
            double lcsSim = LevenshteinDistanceUtils.lcsSimilarity(pair[0], pair[1]);
            
            System.out.printf("%-12s → %-12s  %d\t%.2f%%%n",
                pair[0], pair[1], lcsLen, lcsSim * 100);
        }
        
        System.out.println();
    }
    
    /**
     * 示例 8: 实际应用场景
     */
    private static void example8_RealWorldScenarios() {
        System.out.println("━━━ 示例 8: 实际应用场景 ━━━");
        
        // 场景 1: DNA 序列比较
        System.out.println("\n[场景 1] DNA 序列比较:");
        String dna1 = "ACGTACGT";
        String dna2 = "ACGATCGT";
        int dnaDist = LevenshteinDistanceUtils.distance(dna1, dna2);
        double dnaSim = LevenshteinDistanceUtils.similarity(dna1, dna2);
        System.out.println("  " + dna1 + " vs " + dna2);
        System.out.println("  变异数: " + dnaDist + ", 相似度: " + String.format("%.1f%%", dnaSim * 100));
        
        // 场景 2: 版本号比较
        System.out.println("\n[场景 2] 命令行工具名纠错:");
        List<String> commands = Arrays.asList(
            "git", "grep", "find", "sort", "awk", "sed", 
            "docker", "kubectl", "npm", "yarn", "pip"
        );
        String typo = "gut";
        LevenshteinDistanceUtils.FuzzyMatchResult best = 
            LevenshteinDistanceUtils.findBestMatch(typo, commands);
        System.out.println("  输入: \"" + typo + "\" → 您是否想输入: \"" + best.matchedString + "\"?");
        
        // 场景 3: 重复检测
        System.out.println("\n[场景 3] 数据重复检测:");
        List<String> names = Arrays.asList(
            "John Smith", "Jon Smith", "John Smit", "Jane Smith"
        );
        System.out.println("  检测重复姓名:");
        for (int i = 0; i < names.size(); i++) {
            for (int j = i + 1; j < names.size(); j++) {
                double sim = LevenshteinDistanceUtils.similarity(names.get(i), names.get(j));
                if (sim > 0.8) {
                    System.out.println("  ⚠ \"" + names.get(i) + "\" ≈ \"" + 
                        names.get(j) + "\" (" + String.format("%.1f%%", sim * 100) + ")");
                }
            }
        }
        
        // 场景 4: 自动补全排序
        System.out.println("\n[场景 4] 搜索建议排序:");
        String prefix = "prog";
        List<String> suggestions = Arrays.asList(
            "program", "programming", "programmer", "progress", 
            "progressive", "project", "programmatic"
        );
        List<LevenshteinDistanceUtils.FuzzyMatchResult> ranked = 
            LevenshteinDistanceUtils.findTopMatches(prefix, suggestions, 5);
        
        System.out.println("  输入: \"" + prefix + "\"");
        System.out.println("  建议:");
        for (int i = 0; i < ranked.size(); i++) {
            System.out.println("    " + (i+1) + ". " + ranked.get(i).matchedString);
        }
        
        System.out.println();
    }
    
    /**
     * 生成进度条
     */
    private static String generateBar(double percent, int length) {
        int filled = (int) (percent * length);
        StringBuilder bar = new StringBuilder();
        for (int i = 0; i < length; i++) {
            bar.append(i < filled ? "█" : "░");
        }
        return bar.toString();
    }
}