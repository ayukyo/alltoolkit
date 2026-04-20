package trie_utils;

import java.util.List;

/**
 * Trie (前缀树) 使用示例
 * 
 * 展示各种实际应用场景:
 * 1. 自动补全系统
 * 2. 搜索建议
 * 3. 拼写检查
 * 4. 词汇统计
 */
public class TrieExample {
    
    public static void main(String[] args) {
        System.out.println("╔════════════════════════════════════════════╗");
        System.out.println("║     Trie (前缀树) 使用示例                ║");
        System.out.println("╚════════════════════════════════════════════╝\n");
        
        // 示例 1: 基本操作
        basicOperations();
        
        // 示例 2: 自动补全系统
        autocompleteDemo();
        
        // 示例 3: 搜索建议
        searchSuggestions();
        
        // 示例 4: 拼写检查
        spellCheck();
        
        // 示例 5: 词汇统计
        vocabularyStats();
        
        // 示例 6: 最长公共前缀
        longestPrefixDemo();
    }
    
    /**
     * 示例 1: 基本操作
     */
    private static void basicOperations() {
        System.out.println("【示例 1】基本操作");
        System.out.println("─".repeat(40));
        
        Trie trie = new Trie();
        
        // 插入单词
        System.out.println("插入单词: apple, app, application, apply, banana");
        String[] words = {"apple", "app", "application", "apply", "banana"};
        for (String word : words) {
            trie.insert(word);
        }
        
        // 搜索
        System.out.println("\n搜索单词:");
        System.out.println("  search(\"apple\") -> " + trie.search("apple"));
        System.out.println("  search(\"app\") -> " + trie.search("app"));
        System.out.println("  search(\"appl\") -> " + trie.search("appl"));
        System.out.println("  search(\"orange\") -> " + trie.search("orange"));
        
        // 前缀检查
        System.out.println("\n前缀检查:");
        System.out.println("  startsWith(\"app\") -> " + trie.startsWith("app"));
        System.out.println("  startsWith(\"ban\") -> " + trie.startsWith("ban"));
        System.out.println("  startsWith(\"ora\") -> " + trie.startsWith("ora"));
        
        // 删除
        System.out.println("\n删除 'apple':");
        trie.delete("apple");
        System.out.println("  search(\"apple\") -> " + trie.search("apple"));
        System.out.println("  startsWith(\"app\") -> " + trie.startsWith("app"));
        
        System.out.println("\n");
    }
    
    /**
     * 示例 2: 自动补全系统
     */
    private static void autocompleteDemo() {
        System.out.println("【示例 2】自动补全系统");
        System.out.println("─".repeat(40));
        
        Trie trie = new Trie();
        
        // 模拟搜索词汇库
        System.out.println("加载搜索词汇库...");
        String[] searchTerms = {
            "apple", "app", "application", "apply", "app store",
            "banana", "band", "bank", "baseball",
            "computer", "coding", "code", "coffee"
        };
        
        for (String term : searchTerms) {
            trie.insert(term);
            // 模拟热词, 多次插入增加权重
            if (term.equals("apple") || term.equals("app")) {
                trie.insert(term);
                trie.insert(term);
            }
        }
        
        // 自动补全演示
        System.out.println("\n用户输入 'app', 推荐建议:");
        List<String> suggestions = trie.autocomplete("app", 5);
        for (int i = 0; i < suggestions.size(); i++) {
            int count = trie.getWordCount(suggestions.get(i));
            System.out.println("  " + (i + 1) + ". " + suggestions.get(i) + " (热度: " + count + ")");
        }
        
        System.out.println("\n用户输入 'ba', 推荐建议:");
        suggestions = trie.autocomplete("ba", 5);
        for (int i = 0; i < suggestions.size(); i++) {
            System.out.println("  " + (i + 1) + ". " + suggestions.get(i));
        }
        
        System.out.println("\n");
    }
    
    /**
     * 示例 3: 搜索建议
     */
    private static void searchSuggestions() {
        System.out.println("【示例 3】搜索建议");
        System.out.println("─".repeat(40));
        
        Trie trie = new Trie();
        
        // 产品名称
        String[] products = {
            "iPhone 15", "iPhone 15 Pro", "iPhone 14", "iPad Pro", "iPad Air",
            "MacBook Pro", "MacBook Air", "Mac mini", "Apple Watch", "AirPods"
        };
        
        System.out.println("加载产品目录...");
        for (String product : products) {
            trie.insert(product.toLowerCase());
        }
        
        // 搜索建议
        String query = "iphone";
        System.out.println("\n用户搜索: '" + query + "'");
        System.out.println("相关产品:");
        List<String> results = trie.getWordsWithPrefix(query);
        for (String result : results) {
            System.out.println("  → " + result);
        }
        
        query = "mac";
        System.out.println("\n用户搜索: '" + query + "'");
        System.out.println("相关产品:");
        results = trie.getWordsWithPrefix(query);
        for (String result : results) {
            System.out.println("  → " + result);
        }
        
        System.out.println("\n");
    }
    
    /**
     * 示例 4: 拼写检查
     */
    private static void spellCheck() {
        System.out.println("【示例 4】拼写检查");
        System.out.println("─".repeat(40));
        
        Trie dictionary = new Trie();
        
        // 英文词典
        String[] words = {
            "hello", "help", "held", "hallo", "hollow",
            "world", "word", "would", "should",
            "programming", "program", "programmer", "progress"
        };
        
        System.out.println("加载词典 (" + words.length + " 个单词)...");
        for (String word : words) {
            dictionary.insert(word);
        }
        
        // 检查拼写
        String[] testWords = {"hello", "helo", "wrld", "prgram"};
        
        for (String word : testWords) {
            System.out.println("\n检查单词: '" + word + "'");
            if (dictionary.search(word)) {
                System.out.println("  ✓ 拼写正确");
            } else {
                System.out.println("  ✗ 拼写错误, 您是否想输入:");
                List<String> suggestions = dictionary.fuzzySearch(word, 2);
                for (String suggestion : suggestions.subList(0, Math.min(5, suggestions.size()))) {
                    System.out.println("    → " + suggestion);
                }
            }
        }
        
        System.out.println("\n");
    }
    
    /**
     * 示例 5: 词汇统计
     */
    private static void vocabularyStats() {
        System.out.println("【示例 5】词汇统计");
        System.out.println("─".repeat(40));
        
        Trie trie = new Trie();
        
        // 模拟文章词汇
        String[] article = {
            "the", "quick", "brown", "fox", "jumps", "over", "the", "lazy", "dog",
            "the", "dog", "barks", "at", "the", "fox", "the", "fox", "runs", "away",
            "the", "dog", "is", "happy", "the", "fox", "is", "sad"
        };
        
        System.out.println("分析文章词汇...");
        for (String word : article) {
            trie.insert(word);
        }
        
        System.out.println("\n词汇统计:");
        System.out.println("  总词数 (含重复): " + article.length);
        System.out.println("  不同单词数: " + trie.size());
        
        System.out.println("\n词频统计 (前 5 高频词):");
        List<String> allWords = trie.getAllWords();
        allWords.sort((a, b) -> trie.getWordCount(b) - trie.getWordCount(a));
        
        for (int i = 0; i < Math.min(5, allWords.size()); i++) {
            String word = allWords.get(i);
            System.out.println("  " + (i + 1) + ". '" + word + "': " + trie.getWordCount(word) + " 次");
        }
        
        System.out.println("\n");
    }
    
    /**
     * 示例 6: 最长公共前缀
     */
    private static void longestPrefixDemo() {
        System.out.println("【示例 6】最长公共前缀");
        System.out.println("─".repeat(40));
        
        // 场景 1: 有公共前缀
        Trie trie1 = new Trie();
        String[] words1 = {"flower", "flow", "flight", "float"};
        
        System.out.println("单词组: " + String.join(", ", words1));
        for (String word : words1) {
            trie1.insert(word);
        }
        System.out.println("最长公共前缀: '" + trie1.getLongestCommonPrefix() + "'");
        
        // 场景 2: 无公共前缀
        Trie trie2 = new Trie();
        String[] words2 = {"dog", "cat", "bird", "fish"};
        
        System.out.println("\n单词组: " + String.join(", ", words2));
        for (String word : words2) {
            trie2.insert(word);
        }
        System.out.println("最长公共前缀: '" + trie2.getLongestCommonPrefix() + "'");
        
        // 场景 3: URL 前缀
        Trie trie3 = new Trie();
        String[] urls = {"https://api.example.com/users", 
                        "https://api.example.com/products",
                        "https://api.example.com/orders"};
        
        System.out.println("\nURL 组:");
        for (String url : urls) {
            System.out.println("  " + url);
            trie3.insert(url);
        }
        System.out.println("公共 API 基础 URL: '" + trie3.getLongestCommonPrefix() + "'");
        
        System.out.println("\n");
    }
}