import java.util.ArrayList;
import java.util.Comparator;
import java.util.List;

/**
 * Levenshtein 距离工具类
 * 
 * 提供字符串编辑距离计算、相似度分析、模糊搜索等功能
 * 零外部依赖，纯 Java 标准库实现
 */
public class LevenshteinDistanceUtils {
    
    /**
     * 计算两个字符串之间的 Levenshtein 距离
     * 
     * @param s1 第一个字符串
     * @param s2 第二个字符串
     * @return 编辑距离（插入、删除、替换的最小操作数）
     */
    public static int distance(String s1, String s2) {
        if (s1 == null) s1 = "";
        if (s2 == null) s2 = "";
        
        int len1 = s1.length();
        int len2 = s2.length();
        
        // 空字符串情况
        if (len1 == 0) return len2;
        if (len2 == 0) return len1;
        
        // 使用动态规划，优化空间复杂度为 O(min(m,n))
        // 确保 len1 <= len2，优化空间
        if (len1 > len2) {
            return distance(s2, s1);
        }
        
        // 只保存两行
        int[] prev = new int[len1 + 1];
        int[] curr = new int[len1 + 1];
        
        // 初始化第一行
        for (int i = 0; i <= len1; i++) {
            prev[i] = i;
        }
        
        for (int j = 1; j <= len2; j++) {
            curr[0] = j;
            char c2 = s2.charAt(j - 1);
            
            for (int i = 1; i <= len1; i++) {
                int cost = (s1.charAt(i - 1) == c2) ? 0 : 1;
                curr[i] = Math.min(
                    Math.min(prev[i] + 1,      // 删除
                             curr[i - 1] + 1),  // 插入
                    prev[i - 1] + cost           // 替换或匹配
                );
            }
            
            // 交换行
            int[] temp = prev;
            prev = curr;
            curr = temp;
        }
        
        return prev[len1];
    }
    
    /**
     * 计算两个字符串的相似度（0.0 - 1.0）
     * 1.0 表示完全相同，0.0 表示完全不同
     * 
     * @param s1 第一个字符串
     * @param s2 第二个字符串
     * @return 相似度比例
     */
    public static double similarity(String s1, String s2) {
        if (s1 == null && s2 == null) return 1.0;
        if (s1 == null || s2 == null) return 0.0;
        
        int maxLen = Math.max(s1.length(), s2.length());
        if (maxLen == 0) return 1.0;
        
        int dist = distance(s1, s2);
        return 1.0 - (double) dist / maxLen;
    }
    
    /**
     * 计算相似度百分比
     * 
     * @param s1 第一个字符串
     * @param s2 第二个字符串
     * @return 相似度百分比（0-100）
     */
    public static double similarityPercent(String s1, String s2) {
        return similarity(s1, s2) * 100;
    }
    
    /**
     * 计算编辑距离并返回详细的编辑操作序列
     * 
     * @param s1 源字符串
     * @param s2 目标字符串
     * @return 编辑操作列表
     */
    public static List<EditOperation> getEditOperations(String s1, String s2) {
        List<EditOperation> operations = new ArrayList<>();
        
        if (s1 == null) s1 = "";
        if (s2 == null) s2 = "";
        
        int len1 = s1.length();
        int len2 = s2.length();
        
        // 构建完整的 DP 矩阵用于回溯
        int[][] dp = new int[len1 + 1][len2 + 1];
        
        // 初始化
        for (int i = 0; i <= len1; i++) dp[i][0] = i;
        for (int j = 0; j <= len2; j++) dp[0][j] = j;
        
        // 填充矩阵
        for (int i = 1; i <= len1; i++) {
            for (int j = 1; j <= len2; j++) {
                int cost = (s1.charAt(i - 1) == s2.charAt(j - 1)) ? 0 : 1;
                dp[i][j] = Math.min(
                    Math.min(dp[i - 1][j] + 1, dp[i][j - 1] + 1),
                    dp[i - 1][j - 1] + cost
                );
            }
        }
        
        // 回溯获取操作序列
        int i = len1, j = len2;
        while (i > 0 || j > 0) {
            if (i > 0 && j > 0 && s1.charAt(i - 1) == s2.charAt(j - 1)) {
                // 匹配
                operations.add(0, new EditOperation(OperationType.MATCH, i - 1, j - 1, s1.charAt(i - 1)));
                i--;
                j--;
            } else if (i > 0 && j > 0 && dp[i][j] == dp[i - 1][j - 1] + 1) {
                // 替换
                operations.add(0, new EditOperation(OperationType.REPLACE, i - 1, j - 1, 
                    s1.charAt(i - 1), s2.charAt(j - 1)));
                i--;
                j--;
            } else if (j > 0 && dp[i][j] == dp[i][j - 1] + 1) {
                // 插入
                operations.add(0, new EditOperation(OperationType.INSERT, i, j - 1, s2.charAt(j - 1)));
                j--;
            } else if (i > 0 && dp[i][j] == dp[i - 1][j] + 1) {
                // 删除
                operations.add(0, new EditOperation(OperationType.DELETE, i - 1, j, s1.charAt(i - 1)));
                i--;
            }
        }
        
        return operations;
    }
    
    /**
     * 格式化编辑操作序列为可读字符串
     * 
     * @param s1 源字符串
     * @param s2 目标字符串
     * @return 格式化的操作描述
     */
    public static String formatEditScript(String s1, String s2) {
        List<EditOperation> ops = getEditOperations(s1, s2);
        StringBuilder result = new StringBuilder();
        result.append("从 \"").append(s1).append("\" 到 \"").append(s2).append("\" 的编辑序列:\n");
        
        int step = 1;
        for (EditOperation op : ops) {
            result.append(String.format("  步骤 %d: ", step++));
            switch (op.type) {
                case MATCH:
                    result.append(String.format("匹配 '%c' (位置 %d)", op.fromChar, op.position1));
                    break;
                case INSERT:
                    result.append(String.format("插入 '%c' (位置 %d)", op.toChar, op.position2));
                    break;
                case DELETE:
                    result.append(String.format("删除 '%c' (位置 %d)", op.fromChar, op.position1));
                    break;
                case REPLACE:
                    result.append(String.format("替换 '%c' -> '%c' (位置 %d)", 
                        op.fromChar, op.toChar, op.position1));
                    break;
            }
            result.append("\n");
        }
        
        return result.toString();
    }
    
    /**
     * 在候选列表中找到与目标字符串最相似的字符串
     * 
     * @param target 目标字符串
     * @param candidates 候选字符串列表
     * @return 最匹配的结果
     */
    public static FuzzyMatchResult findBestMatch(String target, List<String> candidates) {
        if (candidates == null || candidates.isEmpty()) {
            return null;
        }
        
        String bestMatch = null;
        double bestSimilarity = -1;
        int bestDistance = Integer.MAX_VALUE;
        
        for (String candidate : candidates) {
            double sim = similarity(target, candidate);
            if (sim > bestSimilarity) {
                bestSimilarity = sim;
                bestMatch = candidate;
                bestDistance = distance(target, candidate);
            }
        }
        
        return new FuzzyMatchResult(bestMatch, bestDistance, bestSimilarity, target);
    }
    
    /**
     * 查找所有相似度超过阈值的候选字符串
     * 
     * @param target 目标字符串
     * @param candidates 候选字符串列表
     * @param threshold 相似度阈值（0.0 - 1.0）
     * @return 匹配结果列表，按相似度降序排列
     */
    public static List<FuzzyMatchResult> findMatchesAboveThreshold(String target, 
            List<String> candidates, double threshold) {
        List<FuzzyMatchResult> results = new ArrayList<>();
        
        if (candidates == null) return results;
        
        for (String candidate : candidates) {
            double sim = similarity(target, candidate);
            if (sim >= threshold) {
                int dist = distance(target, candidate);
                results.add(new FuzzyMatchResult(candidate, dist, sim, target));
            }
        }
        
        // 按相似度降序排列
        results.sort(Comparator.comparingDouble(FuzzyMatchResult::getSimilarity).reversed());
        
        return results;
    }
    
    /**
     * 查找前 N 个最相似的候选字符串
     * 
     * @param target 目标字符串
     * @param candidates 候选字符串列表
     * @param topN 返回数量
     * @return 匹配结果列表，按相似度降序排列
     */
    public static List<FuzzyMatchResult> findTopMatches(String target, 
            List<String> candidates, int topN) {
        List<FuzzyMatchResult> allResults = new ArrayList<>();
        
        if (candidates == null) return allResults;
        
        for (String candidate : candidates) {
            double sim = similarity(target, candidate);
            int dist = distance(target, candidate);
            allResults.add(new FuzzyMatchResult(candidate, dist, sim, target));
        }
        
        // 排序并取前 N 个
        allResults.sort(Comparator.comparingDouble(FuzzyMatchResult::getSimilarity).reversed());
        
        return allResults.subList(0, Math.min(topN, allResults.size()));
    }
    
    /**
     * 检查两个字符串是否相似度达到阈值
     * 
     * @param s1 第一个字符串
     * @param s2 第二个字符串
     * @param threshold 相似度阈值
     * @return 是否达到阈值
     */
    public static boolean isSimilar(String s1, String s2, double threshold) {
        return similarity(s1, s2) >= threshold;
    }
    
    /**
     * 计算 Damerau-Levenshtein 距离（支持相邻字符交换操作）
     * 
     * @param s1 第一个字符串
     * @param s2 第二个字符串
     * @return 编辑距离
     */
    public static int damerauLevenshteinDistance(String s1, String s2) {
        if (s1 == null) s1 = "";
        if (s2 == null) s2 = "";
        
        int len1 = s1.length();
        int len2 = s2.length();
        
        if (len1 == 0) return len2;
        if (len2 == 0) return len1;
        
        int[][] dp = new int[len1 + 1][len2 + 1];
        
        for (int i = 0; i <= len1; i++) dp[i][0] = i;
        for (int j = 0; j <= len2; j++) dp[0][j] = j;
        
        for (int i = 1; i <= len1; i++) {
            for (int j = 1; j <= len2; j++) {
                int cost = (s1.charAt(i - 1) == s2.charAt(j - 1)) ? 0 : 1;
                dp[i][j] = Math.min(
                    Math.min(dp[i - 1][j] + 1, dp[i][j - 1] + 1),
                    dp[i - 1][j - 1] + cost
                );
                
                // 检查交换操作
                if (i > 1 && j > 1 && 
                    s1.charAt(i - 1) == s2.charAt(j - 2) && 
                    s1.charAt(i - 2) == s2.charAt(j - 1)) {
                    dp[i][j] = Math.min(dp[i][j], dp[i - 2][j - 2] + 1);
                }
            }
        }
        
        return dp[len1][len2];
    }
    
    /**
     * 计算最长公共子序列长度
     * 
     * @param s1 第一个字符串
     * @param s2 第二个字符串
     * @return LCS 长度
     */
    public static int longestCommonSubsequenceLength(String s1, String s2) {
        if (s1 == null || s2 == null) return 0;
        
        int len1 = s1.length();
        int len2 = s2.length();
        
        if (len1 == 0 || len2 == 0) return 0;
        
        int[] prev = new int[len2 + 1];
        int[] curr = new int[len2 + 1];
        
        for (int i = 1; i <= len1; i++) {
            for (int j = 1; j <= len2; j++) {
                if (s1.charAt(i - 1) == s2.charAt(j - 1)) {
                    curr[j] = prev[j - 1] + 1;
                } else {
                    curr[j] = Math.max(prev[j], curr[j - 1]);
                }
            }
            int[] temp = prev;
            prev = curr;
            curr = temp;
        }
        
        return prev[len2];
    }
    
    /**
     * 基于最长公共子序列的相似度
     * 
     * @param s1 第一个字符串
     * @param s2 第二个字符串
     * @return LCS 相似度
     */
    public static double lcsSimilarity(String s1, String s2) {
        if (s1 == null && s2 == null) return 1.0;
        if (s1 == null || s2 == null) return 0.0;
        
        int maxLen = Math.max(s1.length(), s2.length());
        if (maxLen == 0) return 1.0;
        
        int lcs = longestCommonSubsequenceLength(s1, s2);
        return (double) lcs / maxLen;
    }
    
    // ==================== 内部类定义 ====================
    
    /**
     * 编辑操作类型
     */
    public enum OperationType {
        MATCH,    // 匹配
        INSERT,   // 插入
        DELETE,   // 删除
        REPLACE   // 替换
    }
    
    /**
     * 编辑操作
     */
    public static class EditOperation {
        public final OperationType type;
        public final int position1;  // 在 s1 中的位置
        public final int position2;  // 在 s2 中的位置
        public final char fromChar;  // 原字符
        public final char toChar;    // 目标字符
        
        public EditOperation(OperationType type, int pos1, int pos2, char c) {
            this.type = type;
            this.position1 = pos1;
            this.position2 = pos2;
            this.fromChar = c;
            this.toChar = c;
        }
        
        public EditOperation(OperationType type, int pos1, int pos2, char from, char to) {
            this.type = type;
            this.position1 = pos1;
            this.position2 = pos2;
            this.fromChar = from;
            this.toChar = to;
        }
        
        @Override
        public String toString() {
            switch (type) {
                case MATCH: return String.format("MATCH '%c' at %d", fromChar, position1);
                case INSERT: return String.format("INSERT '%c' at %d", toChar, position2);
                case DELETE: return String.format("DELETE '%c' at %d", fromChar, position1);
                case REPLACE: return String.format("REPLACE '%c' -> '%c' at %d", fromChar, toChar, position1);
                default: return type.toString();
            }
        }
    }
    
    /**
     * 模糊匹配结果
     */
    public static class FuzzyMatchResult {
        public final String matchedString;
        public final int distance;
        public final double similarity;
        public final String targetString;
        
        public FuzzyMatchResult(String matched, int dist, double sim, String target) {
            this.matchedString = matched;
            this.distance = dist;
            this.similarity = sim;
            this.targetString = target;
        }
        
        public String getMatchedString() { return matchedString; }
        public int getDistance() { return distance; }
        public double getSimilarity() { return similarity; }
        public String getTargetString() { return targetString; }
        
        @Override
        public String toString() {
            return String.format("FuzzyMatchResult{matched='%s', distance=%d, similarity=%.2f%%, target='%s'}",
                matchedString, distance, similarity * 100, targetString);
        }
    }
}