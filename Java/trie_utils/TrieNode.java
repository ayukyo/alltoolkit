package trie_utils;

import java.util.HashMap;
import java.util.Map;

/**
 * 前缀树节点
 * 
 * 每个节点存储:
 * - 子节点映射 (字符 -> TrieNode)
 * - 是否为单词结尾标志
 * - 单词计数 (用于统计和排名)
 */
public class TrieNode {
    private Map<Character, TrieNode> children;
    private boolean isEndOfWord;
    private int wordCount;
    
    public TrieNode() {
        this.children = new HashMap<>();
        this.isEndOfWord = false;
        this.wordCount = 0;
    }
    
    public Map<Character, TrieNode> getChildren() {
        return children;
    }
    
    public TrieNode getChild(char ch) {
        return children.get(ch);
    }
    
    public void setChild(char ch, TrieNode node) {
        children.put(ch, node);
    }
    
    public boolean hasChild(char ch) {
        return children.containsKey(ch);
    }
    
    public boolean isEndOfWord() {
        return isEndOfWord;
    }
    
    public void setEndOfWord(boolean endOfWord) {
        this.isEndOfWord = endOfWord;
    }
    
    public int getWordCount() {
        return wordCount;
    }
    
    public void setWordCount(int count) {
        this.wordCount = count;
    }
    
    public void incrementWordCount() {
        this.wordCount++;
    }
    
    public void decrementWordCount() {
        this.wordCount = Math.max(0, this.wordCount - 1);
    }
    
    public int getChildrenCount() {
        return children.size();
    }
}