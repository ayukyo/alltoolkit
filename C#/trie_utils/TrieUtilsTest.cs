using System;
using System.Collections.Generic;
using System.Linq;
using AllToolkit.TrieUtils;

namespace AllToolkit.Tests
{
    /// <summary>
    /// TrieUtils 单元测试
    /// </summary>
    class TrieUtilsTest
    {
        private static int passed = 0;
        private static int failed = 0;

        static void Main(string[] args)
        {
            Console.WriteLine("Running TrieUtils tests...\n");

            TestBasicOperations();
            TestSearchOperations();
            TestPrefixOperations();
            TestDeleteOperations();
            TestAutoComplete();
            TestAdvancedFeatures();
            TestGenericTrie();
            TestUnicodeSupport();
            TestConcurrency();
            TestEdgeCases();

            Console.WriteLine("\n========================================");
            Console.WriteLine($"Results: {passed} passed, {failed} failed");
            Console.WriteLine("========================================");

            Environment.Exit(failed > 0 ? 1 : 0);
        }

        static void Assert(bool condition, string testName)
        {
            if (condition)
            {
                Console.WriteLine($"  ✓ {testName}");
                passed++;
            }
            else
            {
                Console.WriteLine($"  ✗ {testName}");
                failed++;
            }
        }

        static void TestBasicOperations()
        {
            Console.WriteLine("\nBasic Operations Tests:");

            using (var trie = new Trie())
            {
                Assert(trie.Size == 0, "New trie has size 0");
                Assert(trie.IsEmpty, "New trie is empty");

                Assert(trie.Insert("hello"), "Insert new word returns true");
                Assert(trie.Size == 1, "Size is 1 after insert");

                Assert(!trie.Insert("hello"), "Insert duplicate returns false");
                Assert(trie.Size == 1, "Size unchanged after duplicate");

                Assert(trie.Insert("help"), "Insert another word");
                Assert(trie.Size == 2, "Size is 2");

                Assert(!trie.Insert(""), "Insert empty string returns false");
                Assert(!trie.Insert(null), "Insert null returns false");
            }
        }

        static void TestSearchOperations()
        {
            Console.WriteLine("\nSearch Operations Tests:");

            using (var trie = new Trie())
            {
                trie.Insert("hello");
                trie.Insert("help");
                trie.Insert("world");

                Assert(trie.Search("hello"), "Search existing word");
                Assert(trie.Search("help"), "Search another existing word");
                Assert(!trie.Search("hel"), "Search prefix not word");
                Assert(!trie.Search("helloworld"), "Search non-existing word");
                Assert(!trie.Search(""), "Search empty string");

                // Search with value
                trie.Insert("apple", 1);
                trie.Insert("banana", "fruit");

                object value;
                Assert(trie.SearchWithValue("apple", out value) && (int)value == 1, "SearchWithValue int");
                Assert(trie.SearchWithValue("banana", out value) && (string)value == "fruit", "SearchWithValue string");
                Assert(!trie.SearchWithValue("missing", out value), "SearchWithValue not found");

                // Generic version
                int intVal;
                Assert(trie.SearchWithValue<int>("apple", out intVal) && intVal == 1, "SearchWithValue<T> int");
                string strVal;
                Assert(trie.SearchWithValue<string>("banana", out strVal) && strVal == "fruit", "SearchWithValue<T> string");

                // GetCount
                trie.Insert("freq");
                trie.Insert("freq");
                trie.Insert("freq");
                Assert(trie.GetCount("freq") == 3, "GetCount returns frequency");
                Assert(trie.GetCount("missing") == 0, "GetCount for missing word");
            }
        }

        static void TestPrefixOperations()
        {
            Console.WriteLine("\nPrefix Operations Tests:");

            using (var trie = new Trie())
            {
                trie.Insert("hello");
                trie.Insert("help");
                trie.Insert("helper");
                trie.Insert("helicopter");
                trie.Insert("world");

                Assert(trie.StartsWith("hel"), "StartsWith existing prefix");
                Assert(trie.StartsWith("hello"), "StartsWith full word");
                Assert(trie.StartsWith(""), "StartsWith empty prefix");
                Assert(!trie.StartsWith("xyz"), "StartsWith non-existing prefix");

                var words = trie.WordsWithPrefix("hel");
                Assert(words.Count == 4, "WordsWithPrefix returns 4 words");
                Assert(words.Contains("hello") && words.Contains("help"), "WordsWithPrefix contains expected words");

                words = trie.WordsWithPrefix("xyz");
                Assert(words.Count == 0, "WordsWithPrefix non-existing returns empty");

                words = trie.WordsWithPrefixLimit("hel", 2);
                Assert(words.Count == 2, "WordsWithPrefixLimit respects limit");

                words = trie.AllWords();
                Assert(words.Count == 5, "AllWords returns all 5 words");
            }
        }

        static void TestDeleteOperations()
        {
            Console.WriteLine("\nDelete Operations Tests:");

            using (var trie = new Trie())
            {
                trie.Insert("hello");
                trie.Insert("help");
                trie.Insert("world");

                Assert(trie.Delete("hello"), "Delete existing word");
                Assert(trie.Size == 2, "Size decreased after delete");
                Assert(!trie.Search("hello"), "Deleted word not found");
                Assert(trie.Search("help"), "Other words still exist");

                Assert(!trie.Delete("hello"), "Delete non-existing word returns false");
                Assert(!trie.Delete(""), "Delete empty string returns false");
                Assert(!trie.Delete(null), "Delete null returns false");

                trie.Delete("help");
                trie.Delete("world");
                Assert(trie.Size == 0, "All deleted, size is 0");

                // Test cleanup of intermediate nodes
                trie.Insert("cat");
                trie.Insert("car");
                trie.Delete("cat");
                Assert(trie.Search("car"), "car still exists after cat deleted");
            }
        }

        static void TestAutoComplete()
        {
            Console.WriteLine("\nAutoComplete Tests:");

            using (var trie = new Trie())
            {
                trie.Insert("apple");
                trie.Insert("app");
                trie.Insert("application");
                trie.Insert("apply");
                trie.Insert("approach");
                trie.Insert("banana");

                var suggestions = trie.AutoComplete("app", 3);
                Assert(suggestions.Count <= 3, "AutoComplete respects limit");
                Assert(suggestions.All(s => s.StartsWith("app")), "All suggestions start with prefix");

                suggestions = trie.AutoComplete("app", 10);
                Assert(suggestions.Count == 5, "AutoComplete returns all matching words");

                suggestions = trie.AutoComplete("xyz", 5);
                Assert(suggestions.Count == 0, "AutoComplete non-existing prefix");

                // Batch insert
                var batchWords = new List<string> { "dog", "door", "dorm" };
                var count = trie.BatchInsert(batchWords);
                Assert(count == 3, "BatchInsert returns count of new words");

                suggestions = trie.AutoComplete("do", 5);
                Assert(suggestions.Count == 3, "AutoComplete finds batch inserted words");
            }
        }

        static void TestAdvancedFeatures()
        {
            Console.WriteLine("\nAdvanced Features Tests:");

            using (var trie = new Trie())
            {
                // LongestCommonPrefix
                trie.Insert("flower");
                trie.Insert("flow");
                trie.Insert("flight");
                Assert(trie.LongestCommonPrefix() == "fl", "LongestCommonPrefix");

                trie.Clear();
                trie.Insert("cat");
                trie.Insert("dog");
                Assert(trie.LongestCommonPrefix() == "", "LongestCommonPrefix no common");

                trie.Clear();
                trie.Insert("single");
                Assert(trie.LongestCommonPrefix() == "single", "LongestCommonPrefix single word");

                // MinPrefix
                trie.Clear();
                trie.Insert("cat");
                trie.Insert("car");
                trie.Insert("dog");
                Assert(trie.MinPrefix("cat") == "c", "MinPrefix for cat");
                Assert(trie.MinPrefix("dog") == "d", "MinPrefix for dog");

                // ContainsAnyPrefixOf
                trie.Clear();
                trie.Insert("car");
                trie.Insert("hello");
                Assert(trie.ContainsAnyPrefixOf("carpet"), "ContainsAnyPrefixOf finds car in carpet");
                Assert(!trie.ContainsAnyPrefixOf("xyz"), "ContainsAnyPrefixOf no match");

                // LongestPrefixOf
                trie.Insert("carpet");
                Assert(trie.LongestPrefixOf("carpets") == "carpet", "LongestPrefixOf");

                // PatternMatch
                trie.Clear();
                trie.Insert("cat");
                trie.Insert("bat");
                trie.Insert("rat");
                trie.Insert("car");
                trie.Insert("bar");

                var matches = trie.PatternMatch("?at");
                Assert(matches.Count == 3, "PatternMatch ?at finds 3 words");
                Assert(matches.Contains("cat") && matches.Contains("bat"), "PatternMatch contains expected");

                matches = trie.PatternMatch("ca?");
                Assert(matches.Count == 2, "PatternMatch ca? finds 2 words");

                matches = trie.PatternMatch("ca*");
                Assert(matches.Count >= 2, "PatternMatch ca* finds matching words");

                // GetWordsByFrequency
                trie.Clear();
                trie.Insert("apple");
                trie.Insert("apple");
                trie.Insert("apple");
                trie.Insert("banana");
                trie.Insert("banana");
                trie.Insert("cherry");

                var freq = trie.GetWordsByFrequency();
                Assert(freq.Count == 3, "GetWordsByFrequency returns 3 words");
                Assert(freq[0].Word == "apple" && freq[0].Count == 3, "GetWordsByFrequency sorted by freq");

                // ToMap
                trie.Clear();
                trie.Insert("a", 1);
                trie.Insert("b", 2);
                var map = trie.ToMap();
                Assert(map.Count == 2 && (int)map["a"] == 1, "ToMap works");

                // BatchInsertWithValues
                trie.Clear();
                var pairs = new Dictionary<string, object> { { "x", 10 }, { "y", 20 } };
                count = trie.BatchInsertWithValues(pairs);
                Assert(count == 2, "BatchInsertWithValues returns count");
                Assert(trie.SearchWithValue("x", out value) && (int)value == 10, "BatchInsertWithValues stored values");
            }
        }

        static void TestGenericTrie()
        {
            Console.WriteLine("\nGeneric Trie Tests:");

            using (var trie = new Trie<int>())
            {
                Assert(trie.Size == 0, "Generic trie empty");

                trie.Insert("score1", 100);
                trie.Insert("score2", 200);

                Assert(trie.Size == 2, "Generic trie size");

                int value;
                Assert(trie.Search("score1", out value) && value == 100, "Generic Search with value");
                Assert(trie.Search("score1"), "Generic Search without value");
                Assert(trie.StartsWith("score"), "Generic StartsWith");

                Assert(trie.Delete("score1"), "Generic Delete");
                Assert(!trie.Search("score1"), "Generic Delete verified");

                var words = trie.AutoComplete("sc", 5);
                Assert(words.Count == 1, "Generic AutoComplete");

                trie.Clear();
                Assert(trie.Size == 0, "Generic Clear");
            }
        }

        static void TestUnicodeSupport()
        {
            Console.WriteLine("\nUnicode Support Tests:");

            using (var trie = new Trie())
            {
                // Chinese
                trie.Insert("你好");
                trie.Insert("你好吗");
                trie.Insert("你们好");

                Assert(trie.Search("你好"), "Chinese word search");
                var words = trie.WordsWithPrefix("你好");
                Assert(words.Count == 2, "Chinese prefix search");

                // Japanese
                trie.Insert("こんにちは");
                Assert(trie.Search("こんにちは"), "Japanese word search");

                // Emoji
                trie.Insert("😀🎉");
                Assert(trie.Search("😀🎉"), "Emoji search");

                trie.Clear();
                Assert(trie.Size == 0, "Clear after Unicode test");
            }
        }

        static void TestConcurrency()
        {
            Console.WriteLine("\nConcurrency Tests:");

            using (var trie = new Trie())
            {
                var tasks = new List<System.Threading.Tasks.Task>();

                // Concurrent inserts
                for (int i = 0; i < 100; i++)
                {
                    tasks.Add(System.Threading.Tasks.Task.Run(() =>
                    {
                        trie.Insert("word" + Guid.NewGuid().ToString().Substring(0, 8));
                    }));
                }

                // Concurrent searches
                for (int i = 0; i < 50; i++)
                {
                    tasks.Add(System.Threading.Tasks.Task.Run(() =>
                    {
                        trie.Search("test");
                        trie.StartsWith("word");
                    }));
                }

                System.Threading.Tasks.Task.WaitAll(tasks.ToArray());
                Assert(trie.Size >= 100, "Concurrent inserts successful");

                // Concurrent reads and writes
                var finalSize = trie.Size;
                Assert(finalSize >= 100, "Concurrent operations completed");
            }
        }

        static void TestEdgeCases()
        {
            Console.WriteLine("\nEdge Cases Tests:");

            using (var trie = new Trie())
            {
                // Single character
                trie.Insert("a");
                Assert(trie.Search("a"), "Single character search");

                // Very long word
                var longWord = "abcdefghijklmnopqrstuvwxyz";
                trie.Insert(longWord);
                Assert(trie.Search(longWord), "Long word search");

                // Words with same prefix
                trie.Clear();
                trie.Insert("a");
                trie.Insert("aa");
                trie.Insert("aaa");
                Assert(trie.Search("a") && trie.Search("aa") && trie.Search("aaa"), "Nested prefixes");

                // Delete leaf
                trie.Delete("aaa");
                Assert(!trie.Search("aaa") && trie.Search("aa"), "Delete leaf preserves parent");

                // Empty trie operations
                trie.Clear();
                Assert(trie.AllWords().Count == 0, "AllWords on empty trie");
                Assert(trie.WordsWithPrefix("x").Count == 0, "WordsWithPrefix on empty trie");
                Assert(trie.LongestCommonPrefix() == "", "LongestCommonPrefix on empty trie");

                // Pattern match edge cases
                trie.Insert("a");
                trie.Insert("b");
                trie.Insert("c");
                var matches = trie.PatternMatch("*");
                Assert(matches.Count == 3, "PatternMatch * matches all");

                trie.Clear();
                trie.Insert("cat");
                trie.Insert("car");
                trie.Insert("card");
                trie.Insert("care");
                trie.Insert("careful");

                Assert(trie.LongestPrefixOf("carefully") == "careful", "LongestPrefixOf complex");
                Assert(trie.ContainsAnyPrefixOf("cardboard"), "ContainsAnyPrefixOf complex");
            }
        }
    }
}