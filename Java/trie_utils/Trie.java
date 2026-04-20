package trie_utils;

import java.util.ArrayList;
import java.util.Collections;
import java.util.Comparator;
import java.util.LinkedList;
import java.util.List;
import java.util.Map;
import java.util.Queue;

/**
 * 前缀树 (Trie / 前缀树 / 字典树)
 * 
 * 高效的字符串存储和检索数据结构，适用于:
 * - 自动补全 / 输入建议
 * - 拼写检查
 * - 前缀搜索
 * - 词频统计
 * 
 * 时间复杂度:
 * - 插入: O(m), m 为单词长度
 * - 搜索: O(m)
 * - 前缀搜索: O(m + k*p), k 为结果数, p 为平均词长
 * - 删除: O(m)
 * 
 * 空间复杂度: O(n*m), n 为单词数, m 为平均词长
 */
public class Trie {
    private final TrieNode root;
    private int totalWords;
    
    public Trie() {
        this.root = new TrieNode();
        this.totalWords = 0;
    }
    
    // ==================== 基本操作 ====================
    
    /**
     * 插入单词
     * @param word 要插入的单词
     * @return 插入成功返回 true, 单词为空或 null 返回 false
     */
    public boolean insert(String word) {
        if (word == null || word.isEmpty()) {
            return false;
        }
        
        TrieNode current = root;
        for (char ch : word.toCharArray()) {
            current.getChildren().putIfAbsent(ch, new TrieNode());
            current = current.getChildren().get(ch);
        }
        
        if (!current.isEndOfWord()) {
            current.setEndOfWord(true);
            current.setWordCount(1);
            totalWords++;
        } else {
            current.incrementWordCount();
        }
        
        return true;
    }
    
    /**
     * 搜索完整单词
     * @param word 要搜索的单词
     * @return 存在返回 true, 否则返回 false
     */
    public boolean search(String word) {
        TrieNode node = searchNode(word);
        return node != null && node.isEndOfWord();
    }
    
    /**
     * 检查是否存在以指定前缀开头的单词
     * @param prefix 前缀
     * @return 存在返回 true, 否则返回 false
     */
    public boolean startsWith(String prefix) {
        return searchNode(prefix) != null;
    }
    
    /**
     * 删除单词
     * @param word 要删除的单词
     * @return 删除成功返回 true, 单词不存在返回 false
     */
    public boolean delete(String word) {
        if (word == null || word.isEmpty()) {
            return false;
        }
        // 先检查单词是否存在
        TrieNode node = searchNode(word);
        if (node == null || !node.isEndOfWord()) {
            return false;
        }
        // 执行删除
        deleteNode(root, word, 0);
        totalWords--;
        return true;
    }
    
    private boolean deleteNode(TrieNode current, String word, int index) {
        if (index == word.length()) {
            current.setEndOfWord(false);
            return current.getChildrenCount() == 0;
        }
        
        char ch = word.charAt(index);
        TrieNode node = current.getChild(ch);
        if (node == null) {
            return false;
        }
        
        boolean shouldDeleteChild = deleteNode(node, word, index + 1);
        
        if (shouldDeleteChild) {
            current.getChildren().remove(ch);
            return !current.isEndOfWord() && current.getChildrenCount() == 0;
        }
        
        return false;
    }
    
    /**
     * 清空 Trie
     */
    public void clear() {
        root.getChildren().clear();
        root.setEndOfWord(false);
        root.setWordCount(0);
        totalWords = 0;
    }
    
    // ==================== 辅助方法 ====================
    
    /**
     * 搜索节点
     */
    private TrieNode searchNode(String str) {
        if (str == null) {
            return null;
        }
        
        TrieNode current = root;
        for (char ch : str.toCharArray()) {
            if (!current.hasChild(ch)) {
                return null;
            }
            current = current.getChild(ch);
        }
        return current;
    }
    
    /**
     * 获取单词的出现次数
     * @param word 单词
     * @return 出现次数, 不存在返回 0
     */
    public int getWordCount(String word) {
        TrieNode node = searchNode(word);
        return (node != null && node.isEndOfWord()) ? node.getWordCount() : 0;
    }
    
    /**
     * 获取 Trie 中的总单词数
     * @return 总单词数
     */
    public int size() {
        return totalWords;
    }
    
    /**
     * 检查 Trie 是否为空
     * @return 为空返回 true
     */
    public boolean isEmpty() {
        return totalWords == 0;
    }
    
    // ==================== 自动补全 ====================
    
    /**
     * 获取自动补全建议
     * @param prefix 前缀
     * @param maxSuggestions 最大建议数
     * @return 建议列表, 按词频降序排列
     */
    public List<String> autocomplete(String prefix, int maxSuggestions) {
        if (prefix == null || maxSuggestions <= 0) {
            return Collections.emptyList();
        }
        
        TrieNode prefixNode = searchNode(prefix);
        if (prefixNode == null) {
            return Collections.emptyList();
        }
        
        List<WordWithCount> words = new ArrayList<>();
        collectWords(prefixNode, new StringBuilder(prefix), words);
        
        // 按词频降序排列
        words.sort(Comparator.comparingInt(WordWithCount::count).reversed());
        
        List<String> result = new ArrayList<>();
        for (int i = 0; i < Math.min(maxSuggestions, words.size()); i++) {
            result.add(words.get(i).word());
        }
        
        return result;
    }
    
    /**
     * 获取所有自动补全建议
     * @param prefix 前缀
     * @return 建议列表
     */
    public List<String> autocomplete(String prefix) {
        return autocomplete(prefix, Integer.MAX_VALUE);
    }
    
    /**
     * 收集从指定节点开始的所有单词
     */
    private void collectWords(TrieNode node, StringBuilder prefix, List<WordWithCount> words) {
        if (node.isEndOfWord()) {
            words.add(new WordWithCount(prefix.toString(), node.getWordCount()));
        }
        
        for (Map.Entry<Character, TrieNode> entry : node.getChildren().entrySet()) {
            prefix.append(entry.getKey());
            collectWords(entry.getValue(), prefix, words);
            prefix.deleteCharAt(prefix.length() - 1);
        }
    }
    
    // ==================== 统计功能 ====================
    
    /**
     * 获取所有单词
     * @return 所有单词列表
     */
    public List<String> getAllWords() {
        List<String> words = new ArrayList<>();
        collectAllWords(root, new StringBuilder(), words);
        return words;
    }
    
    private void collectAllWords(TrieNode node, StringBuilder prefix, List<String> words) {
        if (node.isEndOfWord()) {
            words.add(prefix.toString());
        }
        
        for (Map.Entry<Character, TrieNode> entry : node.getChildren().entrySet()) {
            prefix.append(entry.getKey());
            collectAllWords(entry.getValue(), prefix, words);
            prefix.deleteCharAt(prefix.length() - 1);
        }
    }
    
    /**
     * 获取指定前缀开头的所有单词
     * @param prefix 前缀
     * @return 匹配的单词列表
     */
    public List<String> getWordsWithPrefix(String prefix) {
        TrieNode prefixNode = searchNode(prefix);
        if (prefixNode == null) {
            return Collections.emptyList();
        }
        
        List<String> words = new ArrayList<>();
        collectAllWords(prefixNode, new StringBuilder(prefix), words);
        return words;
    }
    
    /**
     * 计算最长公共前缀
     * @return 最长公共前缀
     */
    public String getLongestCommonPrefix() {
        if (isEmpty()) {
            return "";
        }
        
        StringBuilder lcp = new StringBuilder();
        TrieNode current = root;
        
        while (current.getChildrenCount() == 1 && !current.isEndOfWord()) {
            // 获取唯一子节点
            Map.Entry<Character, TrieNode> entry = current.getChildren().entrySet().iterator().next();
            lcp.append(entry.getKey());
            current = entry.getValue();
        }
        
        return lcp.toString();
    }
    
    /**
     * 统计以指定前缀开头的单词数量
     * @param prefix 前缀
     * @return 单词数量
     */
    public int countWordsWithPrefix(String prefix) {
        TrieNode prefixNode = searchNode(prefix);
        if (prefixNode == null) {
            return 0;
        }
        
        int[] count = {0};
        countWords(prefixNode, count);
        return count[0];
    }
    
    private void countWords(TrieNode node, int[] count) {
        if (node.isEndOfWord()) {
            count[0]++;
        }
        for (TrieNode child : node.getChildren().values()) {
            countWords(child, count);
        }
    }
    
    // ==================== 高级功能 ====================
    
    /**
     * 模糊搜索 (支持一个字符的缺失/替换/交换)
     * @param word 要搜索的单词
     * @param maxDistance 最大编辑距离
     * @return 匹配的单词列表
     */
    public List<String> fuzzySearch(String word, int maxDistance) {
        if (word == null || maxDistance < 0) {
            return Collections.emptyList();
        }
        
        List<String> results = new ArrayList<>();
        fuzzySearchDFS(root, word, 0, maxDistance, new StringBuilder(), results);
        return results;
    }
    
    private void fuzzySearchDFS(TrieNode node, String word, int index, 
                                int remainingDistance, StringBuilder current, List<String> results) {
        if (remainingDistance < 0) {
            return;
        }
        
        if (index == word.length()) {
            if (node.isEndOfWord() && remainingDistance >= 0) {
                results.add(current.toString());
            }
            // 继续搜索更长但接近的单词
            for (Map.Entry<Character, TrieNode> entry : node.getChildren().entrySet()) {
                current.append(entry.getKey());
                if (remainingDistance > 0) {
                    fuzzySearchDFS(entry.getValue(), word, index, remainingDistance - 1, current, results);
                }
                current.deleteCharAt(current.length() - 1);
            }
            return;
        }
        
        char ch = word.charAt(index);
        
        // 精确匹配
        if (node.hasChild(ch)) {
            current.append(ch);
            fuzzySearchDFS(node.getChild(ch), word, index + 1, remainingDistance, current, results);
            current.deleteCharAt(current.length() - 1);
        }
        
        if (remainingDistance > 0) {
            // 跳过当前字符 (删除)
            fuzzySearchDFS(node, word, index + 1, remainingDistance - 1, current, results);
            
            // 插入一个字符
            for (Map.Entry<Character, TrieNode> entry : node.getChildren().entrySet()) {
                if (entry.getKey() != ch) {
                    current.append(entry.getKey());
                    fuzzySearchDFS(entry.getValue(), word, index, remainingDistance - 1, current, results);
                    current.deleteCharAt(current.length() - 1);
                }
            }
            
            // 替换当前字符
            for (Map.Entry<Character, TrieNode> entry : node.getChildren().entrySet()) {
                if (entry.getKey() != ch) {
                    current.append(entry.getKey());
                    fuzzySearchDFS(entry.getValue(), word, index + 1, remainingDistance - 1, current, results);
                    current.deleteCharAt(current.length() - 1);
                }
            }
        }
    }
    
    /**
     * 打印 Trie 结构 (用于调试)
     */
    public void printTrie() {
        printTrie(root, "", true);
    }
    
    private void printTrie(TrieNode node, String prefix, boolean isLast) {
        if (node.isEndOfWord()) {
            System.out.println(prefix + (isLast ? "└── " : "├── ") + "(word)");
        }
        
        List<Character> keys = new ArrayList<>(node.getChildren().keySet());
        for (int i = 0; i < keys.size(); i++) {
            char ch = keys.get(i);
            boolean last = (i == keys.size() - 1);
            System.out.println(prefix + (isLast ? "    " : "│   ") + 
                              (last ? "└── " : "├── ") + ch);
            printTrie(node.getChild(ch), prefix + (isLast ? "    " : "│   "), last);
        }
    }
    
    // 内部记录类
    private record WordWithCount(String word, int count) {}
}