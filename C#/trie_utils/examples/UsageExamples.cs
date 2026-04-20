using System;
using System.Collections.Generic;
using System.Linq;
using AllToolkit.TrieUtils;

namespace AllToolkit.TrieUtils.Examples
{
    /// <summary>
    /// Trie 工具使用示例
    /// </summary>
    class UsageExamples
    {
        static void Main(string[] args)
        {
            Console.WriteLine("=== TrieUtils 使用示例 ===\n");

            Example1_BasicUsage();
            Example2_AutoComplete();
            Example3_SpellChecker();
            Example4_WordFrequency();
            Example5_PatternMatching();
            Example6_GenericTrie();
            Example7_DictionaryLookup();

            Console.WriteLine("\n示例演示完成！");
        }

        /// <summary>
        /// 示例1: 基础用法 - 插入、搜索、删除
        /// </summary>
        static void Example1_BasicUsage()
        {
            Console.WriteLine("\n--- 示例1: 基础用法 ---");

            using (var trie = new Trie())
            {
                // 插入单词
                Console.WriteLine("插入单词: apple, banana, cherry, app, application");
                trie.Insert("apple");
                trie.Insert("banana");
                trie.Insert("cherry");
                trie.Insert("app");
                trie.Insert("application");

                Console.WriteLine($"Trie 大小: {trie.Size} 个单词");

                // 搜索单词
                Console.WriteLine($"搜索 'apple': {trie.Search("apple")}");
                Console.WriteLine($"搜索 'app': {trie.Search("app")}");
                Console.WriteLine($"搜索 'appl' (前缀): {trie.Search("appl")}");

                // 前缀搜索
                Console.WriteLine($"是否存在 'app' 开头的单词: {trie.StartsWith("app")}");

                // 删除单词
                Console.WriteLine("删除 'app'");
                trie.Delete("app");
                Console.WriteLine($"搜索 'app': {trie.Search("app")}");
                Console.WriteLine($"搜索 'apple': {trie.Search("apple")}");
            }
        }

        /// <summary>
        /// 示例2: 自动补全
        /// </summary>
        static void Example2_AutoComplete()
        {
            Console.WriteLine("\n--- 示例2: 自动补全 ---");

            using (var trie = new Trie())
            {
                // 添加编程语言关键词
                var keywords = new[] {
                    "abstract", "as", "base", "bool", "break", "byte",
                    "case", "catch", "char", "checked", "class", "const",
                    "continue", "decimal", "default", "delegate", "do", "double",
                    "else", "enum", "event", "explicit", "extern", "false",
                    "finally", "fixed", "float", "for", "foreach", "goto",
                    "if", "implicit", "in", "int", "interface", "internal",
                    "is", "lock", "long", "namespace", "new", "null",
                    "object", "operator", "out", "override", "params", "private",
                    "protected", "public", "readonly", "ref", "return", "sbyte",
                    "sealed", "short", "sizeof", "stackalloc", "static", "string",
                    "struct", "switch", "this", "throw", "true", "try",
                    "typeof", "uint", "ulong", "unchecked", "unsafe", "ushort",
                    "using", "virtual", "void", "volatile", "while"
                };

                trie.BatchInsert(keywords);
                Console.WriteLine($"添加了 {trie.Size} 个 C# 关键词");

                // 自动补全演示
                Console.WriteLine("\n自动补全建议:");
                ShowSuggestions(trie, "c", 5);
                ShowSuggestions(trie, "st", 5);
                ShowSuggestions(trie, "in", 5);
                ShowSuggestions(trie, "pub", 5);
            }
        }

        static void ShowSuggestions(Trie trie, string prefix, int limit)
        {
            var suggestions = trie.AutoComplete(prefix, limit);
            Console.WriteLine($"  输入 '{prefix}' -> 建议: {string.Join(", ", suggestions)}");
        }

        /// <summary>
        /// 示例3: 拼写检查器
        /// </summary>
        static void Example3_SpellChecker()
        {
            Console.WriteLine("\n--- 示例3: 拼写检查器 ---");

            using (var dictionary = new Trie())
            {
                // 加载字典
                var words = new[] {
                    "hello", "world", "programming", "computer", "algorithm",
                    "data", "structure", "trie", "search", "insert",
                    "delete", "prefix", "autocomplete", "dictionary",
                    "spelling", "check", "word", "letter", "character"
                };

                dictionary.BatchInsert(words);
                Console.WriteLine($"字典大小: {dictionary.Size} 个单词");

                // 检查拼写
                var testWords = new[] { "hello", "hallo", "trie", "trei", "word", "wrd" };
                Console.WriteLine("\n拼写检查:");
                foreach (var word in testWords)
                {
                    var isValid = dictionary.Search(word);
                    var suggestions = isValid ? new List<string>() : 
                        dictionary.AutoComplete(word.Substring(0, Math.Min(2, word.Length)), 3);
                    
                    Console.WriteLine($"  '{word}' - {isValid ? "正确 ✓" : "错误 ✗"}");
                    if (!isValid && suggestions.Count > 0)
                    {
                        Console.WriteLine($"    建议: {string.Join(", ", suggestions)}");
                    }
                }
            }
        }

        /// <summary>
        /// 示例4: 单词频率统计
        /// </summary>
        static void Example4_WordFrequency()
        {
            Console.WriteLine("\n--- 示例4: 单词频率统计 ---");

            using (var trie = new Trie())
            {
                // 模拟文本分析 - 插入单词并统计频率
                var text = "the quick brown fox jumps over the lazy dog the fox is quick";
                var words = text.Split(' ');

                Console.WriteLine($"分析文本: \"{text}\"");
                foreach (var word in words)
                {
                    trie.Insert(word);
                }

                Console.WriteLine($"不同单词数: {trie.Size}");
                Console.WriteLine("\n单词频率:");
                var freqList = trie.GetWordsByFrequency();
                foreach (var wf in freqList.Take(5))
                {
                    Console.WriteLine($"  '{wf.Word}' - {wf.Count} 次");
                }
            }
        }

        /// <summary>
        /// 示例5: 模式匹配
        /// </summary>
        static void Example5_PatternMatching()
        {
            Console.WriteLine("\n--- 示例5: 模式匹配 ---");

            using (var trie = new Trie())
            {
                var words = new[] {
                    "cat", "bat", "rat", "car", "bar", "cart", "card",
                    "care", "careful", "carefully", "bark", "barn"
                };

                trie.BatchInsert(words);
                Console.WriteLine($"添加了 {trie.Size} 个单词");

                // 模式匹配
                Console.WriteLine("\n模式匹配:");
                Console.WriteLine($"  '?at' (任意字符 + at): {string.Join(", ", trie.PatternMatch("?at"))}");
                Console.WriteLine($"  'ca?' (ca + 任意字符): {string.Join(", ", trie.PatternMatch("ca?"))}");
                Console.WriteLine($"  'ca*' (ca + 任意): {string.Join(", ", trie.PatternMatch("ca*"))}");
                Console.WriteLine($"  'bar*' (bar + 任意): {string.Join(", ", trie.PatternMatch("bar*"))}");
            }
        }

        /// <summary>
        /// 示例6: 泛型 Trie - 存储自定义值
        /// </summary>
        static void Example6_GenericTrie()
        {
            Console.WriteLine("\n--- 示例6: 泛型 Trie ---");

            using (var trie = new Trie<ProductInfo>())
            {
                // 存储产品信息
                trie.Insert("laptop", new ProductInfo { Name = "笔记本电脑", Price = 999.99 });
                trie.Insert("mouse", new ProductInfo { Name = "鼠标", Price = 29.99 });
                trie.Insert("monitor", new ProductInfo { Name = "显示器", Price = 299.99 });
                trie.Insert("keyboard", new ProductInfo { Name = "键盘", Price = 79.99 });

                Console.WriteLine($"产品数据库大小: {trie.Size}");

                // 搜索产品
                Console.WriteLine("\n产品搜索:");
                ProductInfo product;
                if (trie.Search("laptop", out product))
                {
                    Console.WriteLine($"  'laptop' -> {product.Name}, $${product.Price}");
                }

                // 自动补全产品名
                Console.WriteLine("\n产品自动补全:");
                var suggestions = trie.AutoComplete("m", 10);
                foreach (var s in suggestions)
                {
                    if (trie.Search(s, out product))
                    {
                        Console.WriteLine($"  '{s}' -> {product.Name}");
                    }
                }
            }
        }

        class ProductInfo
        {
            public string Name { get; set; }
            public double Price { get; set; }
        }

        /// <summary>
        /// 示例7: 字典查找与最长前缀匹配
        /// </summary>
        static void Example7_DictionaryLookup()
        {
            Console.WriteLine("\n--- 示例7: 字典查找与最长前缀匹配 ---");

            using (var trie = new Trie<string>())
            {
                // 简易词典
                trie.Insert("hello", "你好");
                trie.Insert("help", "帮助");
                trie.Insert("helper", "助手");
                trie.Insert("helicopter", "直升机");
                trie.Insert("world", "世界");

                Console.WriteLine($"词典大小: {trie.Size}");

                // 查找翻译
                Console.WriteLine("\n翻译查找:");
                string translation;
                if (trie.Search("hello", out translation))
                {
                    Console.WriteLine($"  hello -> {translation}");
                }
                if (trie.Search("helicopter", out translation))
                {
                    Console.WriteLine($"  helicopter -> {translation}");
                }

                // 最长公共前缀
                Console.WriteLine($"最长公共前缀: '{trie.LongestCommonPrefix()}'");

                // 最长前缀匹配 - 用于 URL 路由等场景
                trie.Clear();
                trie.Insert("/api/users", "用户接口");
                trie.Insert("/api/users/profile", "用户资料接口");
                trie.Insert("/api/products", "产品接口");
                trie.Insert("/api", "API 根路由");

                Console.WriteLine("\n路由匹配:");
                Console.WriteLine($"  URL '/api/users/profile/edit' 最长匹配: '{trie.LongestPrefixOf("/api/users/profile/edit")}'");
                if (trie.Search(trie.LongestPrefixOf("/api/users/profile/edit"), out translation))
                {
                    Console.WriteLine($"    -> {translation}");
                }

                Console.WriteLine($"  URL '/api/orders' 最长匹配: '{trie.LongestPrefixOf("/api/orders")}'");
                if (trie.Search(trie.LongestPrefixOf("/api/orders"), out translation))
                {
                    Console.WriteLine($"    -> {translation}");
                }
            }
        }
    }
}