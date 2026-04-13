"""
Trie 工具模块测试

测试覆盖所有核心功能：
- Trie 基本操作
- SpellChecker 拼写检查
- WordDictionary 通配符匹配
- SuffixTrie 后缀搜索
- TrieSet 集合操作
"""

import unittest
from mod import (
    Trie, TrieNode, SpellChecker, WordDictionary,
    SuffixTrie, TrieSet, build_trie_from_words,
    find_common_prefix, group_by_prefix, autocomplete_suggestions
)


class TestTrieNode(unittest.TestCase):
    """TrieNode 测试"""
    
    def test_init(self):
        """测试节点初始化"""
        node = TrieNode()
        self.assertEqual(node.children, {})
        self.assertFalse(node.is_end)
        self.assertEqual(node.count, 0)
        self.assertIsNone(node.data)


class TestTrie(unittest.TestCase):
    """Trie 基本功能测试"""
    
    def setUp(self):
        self.trie = Trie()
    
    def test_insert_and_search(self):
        """测试插入和查找"""
        self.trie.insert("hello")
        self.assertTrue(self.trie.search("hello"))
        self.assertFalse(self.trie.search("world"))
        self.assertFalse(self.trie.search("hel"))
    
    def test_insert_empty(self):
        """测试插入空字符串"""
        self.trie.insert("")
        self.assertEqual(len(self.trie), 0)
    
    def test_insert_with_data(self):
        """测试插入带数据的单词"""
        self.trie.insert("test", {"meaning": "a procedure intended to establish quality"})
        data = self.trie.get_data("test")
        self.assertIsNotNone(data)
        self.assertEqual(data["meaning"], "a procedure intended to establish quality")
    
    def test_starts_with(self):
        """测试前缀搜索"""
        words = ["apple", "application", "apply", "banana", "band"]
        for word in words:
            self.trie.insert(word)
        
        result = self.trie.starts_with("app")
        self.assertEqual(set(result), {"apple", "application", "apply"})
        
        result = self.trie.starts_with("ban")
        self.assertEqual(set(result), {"banana", "band"})
        
        result = self.trie.starts_with("xyz")
        self.assertEqual(result, [])
    
    def test_starts_with_limit(self):
        """测试前缀搜索限制数量"""
        words = ["apple", "application", "apply", "app"]
        for word in words:
            self.trie.insert(word)
        
        result = self.trie.starts_with("app", limit=2)
        self.assertEqual(len(result), 2)
    
    def test_delete(self):
        """测试删除"""
        self.trie.insert("hello")
        self.assertTrue(self.trie.search("hello"))
        
        self.assertTrue(self.trie.delete("hello"))
        self.assertFalse(self.trie.search("hello"))
        self.assertEqual(len(self.trie), 0)
    
    def test_delete_nonexistent(self):
        """测试删除不存在的单词"""
        self.assertFalse(self.trie.delete("notexist"))
    
    def test_count(self):
        """测试单词计数"""
        self.assertEqual(len(self.trie), 0)
        self.trie.insert("hello")
        self.assertEqual(len(self.trie), 1)
        self.trie.insert("world")
        self.assertEqual(len(self.trie), 2)
        self.trie.insert("hello")  # 重复插入
        self.assertEqual(len(self.trie), 2)  # 数量不变
    
    def test_contains(self):
        """测试 in 操作符"""
        self.trie.insert("hello")
        self.assertIn("hello", self.trie)
        self.assertNotIn("world", self.trie)
    
    def test_iter(self):
        """测试迭代"""
        words = ["apple", "banana", "cherry"]
        for word in words:
            self.trie.insert(word)
        
        result = list(self.trie)
        self.assertEqual(set(result), set(words))
    
    def test_get_count(self):
        """测试词频获取"""
        self.trie.insert("hello")
        self.assertEqual(self.trie.get_count("hello"), 1)
        self.trie.insert("hello")
        self.assertEqual(self.trie.get_count("hello"), 2)
        self.assertEqual(self.trie.get_count("world"), 0)
    
    def test_count_prefix(self):
        """测试前缀单词数量统计"""
        words = ["app", "apple", "application", "apply"]
        for word in words:
            self.trie.insert(word)
        
        self.assertEqual(self.trie.count_prefix("app"), 4)
        self.assertEqual(self.trie.count_prefix("appl"), 3)
        self.assertEqual(self.trie.count_prefix("xyz"), 0)
    
    def test_longest_common_prefix(self):
        """测试最长公共前缀"""
        words = ["flower", "flow", "flight"]
        for word in words:
            self.trie.insert(word)
        
        self.assertEqual(self.trie.longest_common_prefix(), "fl")
    
    def test_longest_common_prefix_single_word(self):
        """测试单个单词的最长公共前缀"""
        self.trie.insert("hello")
        self.assertEqual(self.trie.longest_common_prefix(), "hello")
    
    def test_longest_common_prefix_empty(self):
        """测试空 Trie 的最长公共前缀"""
        self.assertEqual(self.trie.longest_common_prefix(), "")
    
    def test_contains_prefix(self):
        """测试前缀存在检查"""
        self.trie.insert("hello")
        self.assertTrue(self.trie.contains_prefix("hel"))
        self.assertTrue(self.trie.contains_prefix("hello"))
        self.assertFalse(self.trie.contains_prefix("world"))
    
    def test_autocomplete_alphabetical(self):
        """测试按字母顺序自动补全"""
        words = ["apple", "application", "apply", "appetite"]
        for word in words:
            self.trie.insert(word)
        
        result = self.trie.autocomplete("app", limit=3, sort_by='alphabetical')
        self.assertEqual(result, sorted(result)[:3])
    
    def test_autocomplete_frequency(self):
        """测试按词频自动补全"""
        words = ["apple", "apple", "apple", "apply", "apply", "app"]
        for word in words:
            self.trie.insert(word)
        
        result = self.trie.autocomplete("app", limit=10, sort_by='frequency')
        # apple 出现 3 次，应该排在前面
        self.assertEqual(result[0], "apple")


class TestSpellChecker(unittest.TestCase):
    """SpellChecker 测试"""
    
    def setUp(self):
        self.checker = SpellChecker()
        self.checker.load_words(["hello", "world", "help", "held", "helder", "worlds"])
    
    def test_is_correct(self):
        """测试拼写检查"""
        self.assertTrue(self.checker.is_correct("hello"))
        self.assertTrue(self.checker.is_correct("HELLO"))  # 大小写不敏感
        self.assertFalse(self.checker.is_correct("helo"))
    
    def test_suggest_exact_match(self):
        """测试精确匹配的建议"""
        result = self.checker.suggest("hello")
        self.assertEqual(result, ["hello"])
    
    def test_suggest_edit_distance_1(self):
        """测试编辑距离为 1 的建议"""
        result = self.checker.suggest("helo")
        self.assertIn("hello", result)
        self.assertIn("help", result)
    
    def test_suggest_edit_distance_2(self):
        """测试编辑距离为 2 的建议"""
        result = self.checker.suggest("worls")
        self.assertIn("worlds", result)
    
    def test_autocomplete(self):
        """测试拼写检查器的自动补全"""
        result = self.checker.autocomplete("hel", limit=5)
        self.assertEqual(set(result), {"hello", "help", "held", "helder"})


class TestWordDictionary(unittest.TestCase):
    """WordDictionary 测试"""
    
    def setUp(self):
        self.wd = WordDictionary()
        self.wd.add_word("hello")
        self.wd.add_word("help")
        self.wd.add_word("held")
    
    def test_search_exact(self):
        """测试精确搜索"""
        self.assertTrue(self.wd.search("hello"))
        self.assertFalse(self.wd.search("world"))
    
    def test_search_dot_wildcard(self):
        """测试点号通配符"""
        self.assertTrue(self.wd.search("h.llo"))  # hello
        self.assertTrue(self.wd.search("h.lp"))   # help
        self.assertTrue(self.wd.search("h.ld"))   # held
        self.assertFalse(self.wd.search("h.l.p"))  # 无匹配
    
    def test_search_star_wildcard(self):
        """测试星号通配符"""
        self.assertTrue(self.wd.search("h*"))      # 匹配所有 h 开头的词
        self.assertTrue(self.wd.search("he*"))     # 匹配所有 he 开头的词
        self.assertTrue(self.wd.search("hel*"))    # 匹配 hel 开头的词
        self.assertFalse(self.wd.search("x*"))     # 无匹配
    
    def test_find_all_matches(self):
        """测试查找所有匹配"""
        result = self.wd.find_all_matches("h.l*")
        self.assertEqual(set(result), {"hello", "help", "held"})


class TestSuffixTrie(unittest.TestCase):
    """SuffixTrie 测试"""
    
    def test_contains(self):
        """测试子串包含"""
        st = SuffixTrie("banana")
        self.assertTrue(st.contains("ana"))
        self.assertTrue(st.contains("ban"))
        self.assertTrue(st.contains("nana"))
        self.assertFalse(st.contains("xyz"))
    
    def test_find_all(self):
        """测试查找所有出现位置"""
        st = SuffixTrie("banana")
        result = st.find_all("ana")
        self.assertEqual(result, [1, 3])
        
        result = st.find_all("an")
        self.assertEqual(result, [1, 3])
        
        result = st.find_all("xyz")
        self.assertEqual(result, [])
    
    def test_count_occurrences(self):
        """测试出现次数统计"""
        st = SuffixTrie("banana")
        self.assertEqual(st.count_occurrences("ana"), 2)
        self.assertEqual(st.count_occurrences("a"), 3)
        self.assertEqual(st.count_occurrences("banana"), 1)
    
    def test_longest_repeated_substring(self):
        """测试最长重复子串"""
        st = SuffixTrie("banana")
        result = st.longest_repeated_substring()
        self.assertIn(result, ["ana", "an", "na"])  # 可能的结果
    
    def test_longest_repeated_substring_no_repeat(self):
        """测试无重复子串"""
        st = SuffixTrie("abc")
        self.assertEqual(st.longest_repeated_substring(), "")


class TestTrieSet(unittest.TestCase):
    """TrieSet 测试"""
    
    def test_basic_operations(self):
        """测试基本操作"""
        ts = TrieSet()
        ts.add("hello")
        ts.add("world")
        
        self.assertIn("hello", ts)
        self.assertIn("world", ts)
        self.assertNotIn("test", ts)
        self.assertEqual(len(ts), 2)
    
    def test_remove(self):
        """测试删除"""
        ts = TrieSet(["hello", "world"])
        self.assertTrue(ts.remove("hello"))
        self.assertNotIn("hello", ts)
        self.assertEqual(len(ts), 1)
    
    def test_starts_with(self):
        """测试前缀搜索"""
        ts = TrieSet(["apple", "application", "banana"])
        result = ts.starts_with("app")
        self.assertEqual(set(result), {"apple", "application"})
    
    def test_union(self):
        """测试并集"""
        ts1 = TrieSet(["a", "b"])
        ts2 = TrieSet(["b", "c"])
        result = ts1.union(ts2)
        
        self.assertIn("a", result)
        self.assertIn("b", result)
        self.assertIn("c", result)
        self.assertEqual(len(result), 3)
    
    def test_intersection(self):
        """测试交集"""
        ts1 = TrieSet(["a", "b", "c"])
        ts2 = TrieSet(["b", "c", "d"])
        result = ts1.intersection(ts2)
        
        self.assertIn("b", result)
        self.assertIn("c", result)
        self.assertEqual(len(result), 2)
    
    def test_difference(self):
        """测试差集"""
        ts1 = TrieSet(["a", "b", "c"])
        ts2 = TrieSet(["b", "c"])
        result = ts1.difference(ts2)
        
        self.assertIn("a", result)
        self.assertEqual(len(result), 1)
    
    def test_isdisjoint(self):
        """测试是否不相交"""
        ts1 = TrieSet(["a", "b"])
        ts2 = TrieSet(["c", "d"])
        ts3 = TrieSet(["b", "c"])
        
        self.assertTrue(ts1.isdisjoint(ts2))
        self.assertFalse(ts1.isdisjoint(ts3))
    
    def test_issubset_issuperset(self):
        """测试子集和超集"""
        ts1 = TrieSet(["a", "b"])
        ts2 = TrieSet(["a", "b", "c"])
        
        self.assertTrue(ts1.issubset(ts2))
        self.assertTrue(ts2.issuperset(ts1))
        self.assertFalse(ts2.issubset(ts1))


class TestUtilityFunctions(unittest.TestCase):
    """工具函数测试"""
    
    def test_build_trie_from_words(self):
        """测试从单词列表构建 Trie"""
        words = ["apple", "banana", "cherry"]
        trie = build_trie_from_words(words)
        
        for word in words:
            self.assertTrue(trie.search(word))
    
    def test_find_common_prefix(self):
        """测试查找公共前缀"""
        words = ["flower", "flow", "flight"]
        result = find_common_prefix(words)
        self.assertEqual(result, "fl")
    
    def test_find_common_prefix_empty(self):
        """测试空列表的公共前缀"""
        result = find_common_prefix([])
        self.assertEqual(result, "")
    
    def test_find_common_prefix_no_common(self):
        """测试无公共前缀"""
        words = ["apple", "banana", "cherry"]
        result = find_common_prefix(words)
        self.assertEqual(result, "")
    
    def test_group_by_prefix(self):
        """测试按前缀分组"""
        words = ["apple", "application", "banana", "band", "cherry"]
        result = group_by_prefix(words, prefix_len=2)
        
        self.assertIn("ap", result)
        self.assertIn("ba", result)
        self.assertIn("ch", result)
        self.assertEqual(set(result["ap"]), {"apple", "application"})
        self.assertEqual(set(result["ba"]), {"banana", "band"})
    
    def test_autocomplete_suggestions(self):
        """测试自动补全建议函数"""
        trie = build_trie_from_words(["apple", "application", "apply"])
        result = autocomplete_suggestions(trie, "app", limit=10)
        
        self.assertEqual(set(result), {"apple", "application", "apply"})


class TestEdgeCases(unittest.TestCase):
    """边缘情况测试"""
    
    def test_unicode_support(self):
        """测试 Unicode 支持"""
        trie = Trie()
        trie.insert("你好")
        trie.insert("世界")
        trie.insert("你好吗")
        
        self.assertTrue(trie.search("你好"))
        self.assertTrue(trie.search("世界"))
        self.assertEqual(set(trie.starts_with("你")), {"你好", "你好吗"})
    
    def test_numbers_in_words(self):
        """测试数字在单词中"""
        trie = Trie()
        trie.insert("test123")
        trie.insert("test456")
        
        self.assertTrue(trie.search("test123"))
        result = trie.starts_with("test")
        self.assertEqual(set(result), {"test123", "test456"})
    
    def test_special_characters(self):
        """测试特殊字符"""
        trie = Trie()
        trie.insert("hello-world")
        trie.insert("hello_world")
        trie.insert("hello.world")
        
        self.assertTrue(trie.search("hello-world"))
        result = trie.starts_with("hello")
        self.assertEqual(set(result), {"hello-world", "hello_world", "hello.world"})
    
    def test_very_long_word(self):
        """测试超长单词"""
        trie = Trie()
        long_word = "a" * 10000
        trie.insert(long_word)
        
        self.assertTrue(trie.search(long_word))
        self.assertEqual(len(trie), 1)
    
    def test_many_words(self):
        """测试大量单词"""
        trie = Trie()
        words = [f"word{i}" for i in range(10000)]
        
        for word in words:
            trie.insert(word)
        
        self.assertEqual(len(trie), 10000)
        for word in words[:100]:  # 抽样检查
            self.assertTrue(trie.search(word))


if __name__ == '__main__':
    unittest.main(verbosity=2)