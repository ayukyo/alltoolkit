package diff_utils;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;

/**
 * DiffUtils - 文本差异比较工具类
 * 
 * 实现 Myers 差异算法，用于比较两个文本或列表的差异。
 * 支持：
 * - 行级别比较
 * - 字符级别比较
 * - 统一格式输出 (unified diff format)
 * - 差异统计
 * - 差异应用 (patch/apply)
 * 
 * 零外部依赖，纯 Java 实现。
 * 
 * @author AllToolkit
 * @version 1.0.0
 */
public class DiffUtils {

    /**
     * 差异类型枚举
     */
    public enum DiffType {
        EQUAL,      // 相同
        INSERT,     // 插入
        DELETE      // 删除
    }

    /**
     * 差异项
     */
    public static class DiffItem {
        public final DiffType type;
        public final String content;

        public DiffItem(DiffType type, String content) {
            this.type = type;
            this.content = content;
        }

        @Override
        public String toString() {
            String prefix;
            switch (type) {
                case INSERT: prefix = "+"; break;
                case DELETE: prefix = "-"; break;
                default:     prefix = " "; break;
            }
            return prefix + content;
        }

        @Override
        public boolean equals(Object obj) {
            if (this == obj) return true;
            if (obj == null || getClass() != obj.getClass()) return false;
            DiffItem other = (DiffItem) obj;
            return type == other.type && content.equals(other.content);
        }

        @Override
        public int hashCode() {
            return 31 * type.hashCode() + content.hashCode();
        }
    }

    /**
     * 差异结果
     */
    public static class DiffResult {
        public final List<DiffItem> items;
        public final int insertions;
        public final int deletions;
        public final int unchanged;

        public DiffResult(List<DiffItem> items) {
            this.items = items;
            int ins = 0, del = 0, equ = 0;
            for (DiffItem item : items) {
                switch (item.type) {
                    case INSERT: ins++; break;
                    case DELETE: del++; break;
                    case EQUAL:  equ++; break;
                }
            }
            this.insertions = ins;
            this.deletions = del;
            this.unchanged = equ;
        }

        /**
         * 获取相似度 (0.0 - 1.0)
         */
        public double getSimilarity() {
            int total = insertions + deletions + unchanged;
            if (total == 0) return 1.0;
            return (double) unchanged / total;
        }

        /**
         * 获取变化率 (0.0 - 1.0)
         */
        public double getChangeRate() {
            return 1.0 - getSimilarity();
        }

        /**
         * 判断是否有差异
         */
        public boolean hasChanges() {
            return insertions > 0 || deletions > 0;
        }
    }

    /**
     * 比较两个文本 (按行)
     * 
     * @param oldText 旧文本
     * @param newText 新文本
     * @return 差异结果
     */
    public static DiffResult diff(String oldText, String newText) {
        return diff(oldText, newText, true);
    }

    /**
     * 比较两个文本
     * 
     * @param oldText 旧文本
     * @param newText 新文本
     * @param byLine  true=按行比较, false=按字符比较
     * @return 差异结果
     */
    public static DiffResult diff(String oldText, String newText, boolean byLine) {
        if (byLine) {
            String[] oldLines = oldText == null ? new String[0] : splitLines(oldText);
            String[] newLines = newText == null ? new String[0] : splitLines(newText);
            return diffArrays(oldLines, newLines);
        } else {
            char[] oldChars = oldText == null ? new char[0] : oldText.toCharArray();
            char[] newChars = newText == null ? new char[0] : newText.toCharArray();
            String[] oldStrs = charArrayToStringArray(oldChars);
            String[] newStrs = charArrayToStringArray(newChars);
            return diffArrays(oldStrs, newStrs);
        }
    }

    /**
     * 比较两个数组
     * 
     * @param oldArray 旧数组
     * @param newArray 新数组
     * @return 差异结果
     */
    public static <T> DiffResult diffArrays(T[] oldArray, T[] newArray) {
        List<DiffItem> items = new ArrayList<>();
        int[][] lcs = computeLCS(oldArray, newArray);
        
        int i = oldArray.length;
        int j = newArray.length;
        
        // 回溯构建差异
        List<DiffItem> reversed = new ArrayList<>();
        
        while (i > 0 || j > 0) {
            if (i > 0 && j > 0 && oldArray[i-1].equals(newArray[j-1])) {
                reversed.add(new DiffItem(DiffType.EQUAL, oldArray[i-1].toString()));
                i--;
                j--;
            } else if (j > 0 && (i == 0 || lcs[i][j-1] >= lcs[i-1][j])) {
                reversed.add(new DiffItem(DiffType.INSERT, newArray[j-1].toString()));
                j--;
            } else if (i > 0) {
                reversed.add(new DiffItem(DiffType.DELETE, oldArray[i-1].toString()));
                i--;
            }
        }
        
        // 反转得到正确顺序
        for (int k = reversed.size() - 1; k >= 0; k--) {
            items.add(reversed.get(k));
        }
        
        // 合并相邻的相同类型
        items = mergeConsecutive(items);
        
        return new DiffResult(items);
    }

    /**
     * 计算最长公共子序列 (LCS) 表
     */
    private static <T> int[][] computeLCS(T[] a, T[] b) {
        int m = a.length;
        int n = b.length;
        int[][] dp = new int[m + 1][n + 1];
        
        for (int i = 1; i <= m; i++) {
            for (int j = 1; j <= n; j++) {
                if (a[i-1].equals(b[j-1])) {
                    dp[i][j] = dp[i-1][j-1] + 1;
                } else {
                    dp[i][j] = Math.max(dp[i-1][j], dp[i][j-1]);
                }
            }
        }
        
        return dp;
    }

    /**
     * 合并相邻相同类型的差异项
     */
    private static List<DiffItem> mergeConsecutive(List<DiffItem> items) {
        if (items.isEmpty()) return items;
        
        List<DiffItem> merged = new ArrayList<>();
        DiffItem current = items.get(0);
        StringBuilder sb = new StringBuilder(current.content);
        
        for (int i = 1; i < items.size(); i++) {
            DiffItem next = items.get(i);
            if (next.type == current.type) {
                sb.append("\n").append(next.content);
            } else {
                merged.add(new DiffItem(current.type, sb.toString()));
                current = next;
                sb = new StringBuilder(next.content);
            }
        }
        merged.add(new DiffItem(current.type, sb.toString()));
        
        return merged;
    }

    /**
     * 分割文本为行数组
     */
    private static String[] splitLines(String text) {
        // 保留换行符以便精确还原
        List<String> lines = new ArrayList<>();
        StringBuilder sb = new StringBuilder();
        
        for (char c : text.toCharArray()) {
            sb.append(c);
            if (c == '\n') {
                lines.add(sb.toString());
                sb = new StringBuilder();
            }
        }
        
        if (sb.length() > 0) {
            lines.add(sb.toString());
        }
        
        // 如果文本为空，返回空数组
        if (lines.isEmpty()) {
            return new String[0];
        }
        
        return lines.toArray(new String[0]);
    }

    /**
     * 字符数组转字符串数组
     */
    private static String[] charArrayToStringArray(char[] chars) {
        String[] result = new String[chars.length];
        for (int i = 0; i < chars.length; i++) {
            result[i] = String.valueOf(chars[i]);
        }
        return result;
    }

    /**
     * 生成统一格式差异 (unified diff)
     * 
     * @param oldText    旧文本
     * @param newText    新文本
     * @param oldFile    旧文件名
     * @param newFile    新文件名
     * @param contextLines 上下文行数
     * @return unified diff 格式字符串
     */
    public static String toUnifiedDiff(String oldText, String newText, 
                                        String oldFile, String newFile,
                                        int contextLines) {
        StringBuilder result = new StringBuilder();
        String[] oldLines = oldText == null ? new String[0] : oldText.split("\n");
        String[] newLines = newText == null ? new String[0] : newText.split("\n");
        
        // 头部信息
        result.append("--- ").append(oldFile).append("\n");
        result.append("+++ ").append(newFile).append("\n");
        
        DiffResult diff = diffArrays(oldLines, newLines);
        
        // 生成 hunk
        int oldLine = 1;
        int newLine = 1;
        
        List<Hunk> hunks = new ArrayList<>();
        Hunk currentHunk = null;
        int contextStart = 0;
        
        for (int i = 0; i < diff.items.size(); i++) {
            DiffItem item = diff.items.get(i);
            String[] lines = item.content.split("\n");
            
            if (item.type != DiffType.EQUAL) {
                if (currentHunk == null) {
                    // 开始新的 hunk
                    currentHunk = new Hunk();
                    currentHunk.oldStart = Math.max(1, oldLine - contextLines);
                    currentHunk.newStart = Math.max(1, newLine - contextLines);
                }
            }
            
            for (String line : lines) {
                switch (item.type) {
                    case EQUAL:
                        if (currentHunk != null) {
                            currentHunk.lines.add(" " + line);
                            currentHunk.oldCount++;
                            currentHunk.newCount++;
                        }
                        oldLine++;
                        newLine++;
                        break;
                    case DELETE:
                        currentHunk.lines.add("-" + line);
                        currentHunk.oldCount++;
                        oldLine++;
                        break;
                    case INSERT:
                        currentHunk.lines.add("+" + line);
                        currentHunk.newCount++;
                        newLine++;
                        break;
                }
            }
            
            // 检查是否结束当前 hunk
            if (item.type == DiffType.EQUAL && currentHunk != null) {
                int equalCount = lines.length;
                if (equalCount > contextLines * 2) {
                    // 足够的上下文，结束当前 hunk
                    hunks.add(currentHunk);
                    currentHunk = null;
                }
            }
        }
        
        // 添加最后一个 hunk
        if (currentHunk != null) {
            hunks.add(currentHunk);
        }
        
        // 输出 hunks
        for (Hunk hunk : hunks) {
            result.append("@@ -")
                  .append(hunk.oldStart).append(",").append(hunk.oldCount)
                  .append(" +")
                  .append(hunk.newStart).append(",").append(hunk.newCount)
                  .append(" @@\n");
            
            for (String line : hunk.lines) {
                result.append(line).append("\n");
            }
        }
        
        return result.toString();
    }

    /**
     * Hunk 辅助类
     */
    private static class Hunk {
        int oldStart;
        int newStart;
        int oldCount = 0;
        int newCount = 0;
        List<String> lines = new ArrayList<>();
    }

    /**
     * 生成带颜色标记的差异 (用于终端显示)
     * 
     * @param diff 差异结果
     * @return 带 ANSI 颜色码的字符串
     */
    public static String toColoredString(DiffResult diff) {
        StringBuilder sb = new StringBuilder();
        for (DiffItem item : diff.items) {
            String[] lines = item.content.split("\n");
            for (String line : lines) {
                switch (item.type) {
                    case EQUAL:
                        sb.append("\u001B[0m").append("  ").append(line).append("\n");
                        break;
                    case DELETE:
                        sb.append("\u001B[31m").append("- ").append(line).append("\n");
                        break;
                    case INSERT:
                        sb.append("\u001B[32m").append("+ ").append(line).append("\n");
                        break;
                }
            }
        }
        sb.append("\u001B[0m"); // 重置颜色
        return sb.toString();
    }

    /**
     * 生成差异统计摘要
     * 
     * @param diff 差异结果
     * @return 统计摘要字符串
     */
    public static String getSummary(DiffResult diff) {
        return String.format("变更统计: +%d -%d (相似度: %.1f%%)",
            diff.insertions, diff.deletions, diff.getSimilarity() * 100);
    }

    /**
     * 应用差异到原文本 (patch)
     * 
     * @param original 原始文本
     * @param patch    差异结果
     * @return 应用差异后的文本
     */
    public static String applyPatch(String original, DiffResult patch) {
        StringBuilder result = new StringBuilder();
        for (DiffItem item : patch.items) {
            switch (item.type) {
                case EQUAL:
                case INSERT:
                    result.append(item.content);
                    break;
                case DELETE:
                    // 跳过删除的内容
                    break;
            }
        }
        return result.toString();
    }

    /**
     * 判断两个文本是否相同
     * 
     * @param text1 文本1
     * @param text2 文本2
     * @return 是否相同
     */
    public static boolean isIdentical(String text1, String text2) {
        if (text1 == null && text2 == null) return true;
        if (text1 == null || text2 == null) return false;
        return text1.equals(text2);
    }

    /**
     * 快速比较 (不生成详细差异)
     * 
     * @param text1 文本1
     * @param text2 文本2
     * @return 是否相同
     */
    public static boolean quickCompare(String text1, String text2) {
        return isIdentical(text1, text2);
    }

    /**
     * 计算编辑距离 (Levenshtein Distance)
     * 
     * @param s1 字符串1
     * @param s2 字符串2
     * @return 编辑距离
     */
    public static int levenshteinDistance(String s1, String s2) {
        if (s1 == null || s2 == null) {
            return (s1 == null ? 0 : s1.length()) + (s2 == null ? 0 : s2.length());
        }
        
        int m = s1.length();
        int n = s2.length();
        
        int[] prev = new int[n + 1];
        int[] curr = new int[n + 1];
        
        // 初始化第一行
        for (int j = 0; j <= n; j++) {
            prev[j] = j;
        }
        
        for (int i = 1; i <= m; i++) {
            curr[0] = i;
            for (int j = 1; j <= n; j++) {
                if (s1.charAt(i-1) == s2.charAt(j-1)) {
                    curr[j] = prev[j-1];
                } else {
                    curr[j] = 1 + Math.min(
                        Math.min(prev[j], curr[j-1]),
                        prev[j-1]
                    );
                }
            }
            int[] temp = prev;
            prev = curr;
            curr = temp;
        }
        
        return prev[n];
    }

    /**
     * 计算文本相似度 (基于编辑距离)
     * 
     * @param s1 字符串1
     * @param s2 字符串2
     * @return 相似度 (0.0 - 1.0)
     */
    public static double similarity(String s1, String s2) {
        if (s1 == null && s2 == null) return 1.0;
        if (s1 == null || s2 == null) return 0.0;
        if (s1.isEmpty() && s2.isEmpty()) return 1.0;
        
        int distance = levenshteinDistance(s1, s2);
        int maxLen = Math.max(s1.length(), s2.length());
        return 1.0 - (double) distance / maxLen;
    }

    /**
     * 查找最长公共子串
     * 
     * @param s1 字符串1
     * @param s2 字符串2
     * @return 最长公共子串
     */
    public static String longestCommonSubstring(String s1, String s2) {
        if (s1 == null || s2 == null || s1.isEmpty() || s2.isEmpty()) {
            return "";
        }
        
        int m = s1.length();
        int n = s2.length();
        int[][] dp = new int[m + 1][n + 1];
        
        int maxLen = 0;
        int endIndex = 0;
        
        for (int i = 1; i <= m; i++) {
            for (int j = 1; j <= n; j++) {
                if (s1.charAt(i-1) == s2.charAt(j-1)) {
                    dp[i][j] = dp[i-1][j-1] + 1;
                    if (dp[i][j] > maxLen) {
                        maxLen = dp[i][j];
                        endIndex = i;
                    }
                }
            }
        }
        
        return s1.substring(endIndex - maxLen, endIndex);
    }

    /**
     * 查找最长公共子序列
     * 
     * @param s1 字符串1
     * @param s2 字符串2
     * @return 最长公共子序列
     */
    public static String longestCommonSubsequence(String s1, String s2) {
        if (s1 == null || s2 == null || s1.isEmpty() || s2.isEmpty()) {
            return "";
        }
        
        int m = s1.length();
        int n = s2.length();
        int[][] dp = new int[m + 1][n + 1];
        
        // 构建 DP 表
        for (int i = 1; i <= m; i++) {
            for (int j = 1; j <= n; j++) {
                if (s1.charAt(i-1) == s2.charAt(j-1)) {
                    dp[i][j] = dp[i-1][j-1] + 1;
                } else {
                    dp[i][j] = Math.max(dp[i-1][j], dp[i][j-1]);
                }
            }
        }
        
        // 回溯找 LCS
        StringBuilder lcs = new StringBuilder();
        int i = m, j = n;
        while (i > 0 && j > 0) {
            if (s1.charAt(i-1) == s2.charAt(j-1)) {
                lcs.insert(0, s1.charAt(i-1));
                i--;
                j--;
            } else if (dp[i-1][j] > dp[i][j-1]) {
                i--;
            } else {
                j--;
            }
        }
        
        return lcs.toString();
    }

    /**
     * 查找所有差异位置
     * 
     * @param s1 字符串1
     * @param s2 字符串2
     * @return 差异位置列表 (开始位置, 结束位置)
     */
    public static List<int[]> findDiffRanges(String s1, String s2) {
        List<int[]> ranges = new ArrayList<>();
        if (s1 == null) s1 = "";
        if (s2 == null) s2 = "";
        
        int i = 0;
        int maxLen = Math.max(s1.length(), s2.length());
        
        while (i < maxLen) {
            // 找到不同的起始位置
            while (i < maxLen && 
                   i < s1.length() && i < s2.length() && 
                   s1.charAt(i) == s2.charAt(i)) {
                i++;
            }
            
            if (i >= maxLen) break;
            
            int start = i;
            
            // 找到相同的结束位置
            while (i < maxLen) {
                boolean s1End = i >= s1.length();
                boolean s2End = i >= s2.length();
                if (s1End || s2End) {
                    i++;
                    continue;
                }
                if (s1.charAt(i) == s2.charAt(i)) break;
                i++;
            }
            
            ranges.add(new int[]{start, i});
        }
        
        return ranges;
    }
}