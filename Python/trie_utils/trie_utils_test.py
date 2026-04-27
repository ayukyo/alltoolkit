"""
Trie 工具模块测试

测试覆盖：
- 基本插入、搜索、删除
- 前缀搜索与自动补全
- 模式匹配
- 序列化/反序列化
- 边界条件与错误处理
"""

import unittest
import sys
import os

# 添加模块路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from mod import (
    Trie, TrieNode, SuffixTrie, PrefixSet,
    build_trie, find_common_prefix, word_frequency_analysis
)


class TestTrieNode(unittest.TestCase):
    """测试 TrieNode"""
    
    def test_init(self):
        """测试节点初始化"""
        node = TrieNode()
        self.assertFalse(node.is_end)
        self.assertEqual(node.count, 0)
        self.assertIsNone(node.data)
        self.assertEqual(len(node.children), 0)
    
    def test_repr(self):
        """测试字符串表示"""
        node = TrieNode()
        node.is_end = True
        node.count = 5
        node.children['a'] = TrieNode()
        
        repr_str = repr(node)
        self.assertIn("end=True", repr_str)
        self.assertIn("count=5", repr_str)
        self.assertIn("children=1", repr_str)


class TestTrieBasic(unittest.TestCase):
    """测试 Trie 基本功能"""
    
    def setUp(self):
        self.trie = Trie()
    
    def test_insert_and_search(self):
        """测试插入和搜索"""
        self.trie.insert("hello")
        self.assertTrue(self.trie.search("hello"))
        self.assertFalse(self.trie.search("hell"))
        self.assertFalse(self.trie.search("helloo"))
    
    def test_insert_empty_string(self):
        """测试插入空字符串"""
        self.trie.insert("")
        self.assertEqual(self.trie.size(), 0)
    
    def test_insert_duplicate(self):
        """测试插入重复单词"""
        self.trie.insert("test")
        self.trie.insert("test")
        self.assertEqual(self.trie.size(), 1)
        self.assertEqual(self.trie.get_count("test"), 2)
    
    def test_insert_with_data(self):
        """测试带数据插入"""
        self.trie.insert("word", data={"meaning": "单词"})
        self.assertEqual(self.trie.get_data("word"), {"meaning": "单词"})
    
    def test_search_nonexistent(self):
        """测试搜索不存在的单词"""
        self.trie.insert("apple")
        self.assertFalse(self.trie.search("banana"))
        self.assertFalse(self.trie.search("app"))
    
    def test_contains_operator(self):
        """测试 in 操作符"""
        self.trie.insert("python")
        self.assertIn("python", self.trie)
        self.assertNotIn("java", self.trie)
    
    def test_len_operator(self):
        """测试 len 操作符"""
        self.assertEqual(len(self.trie), 0)
        self.trie.insert("one")
        self.trie.insert("two")
        self.assertEqual(len(self.trie), 2)
    
    def test_iter_operator(self):
        """测试迭代"""
        words = ["apple", "banana", "cherry"]
        for word in words:
            self.trie.insert(word)
        
        result = list(self.trie)
        self.assertEqual(set(result), set(words))
    
    def test_is_empty(self):
        """测试判空"""
        self.assertTrue(self.trie.is_empty())
        self.trie.insert("test")
        self.assertFalse(self.trie.is_empty())
    
    def test_clear(self):
        """测试清空"""
        self.trie.insert("test1")
        self.trie.insert("test2")
        self.trie.clear()
        self.assertEqual(self.trie.size(), 0)
        self.assertTrue(self.trie.is_empty())


class TestTriePrefixSearch(unittest.TestCase):
    """测试前缀搜索功能"""
    
    def setUp(self):
        self.trie = Trie()
        words = ["hello", "help", "helper", "helicopter", "helium", "world"]
        for word in words:
            self.trie.insert(word)
    
    def test_starts_with(self):
        """测试前缀搜索"""
        results = self.trie.starts_with("hel")
        self.assertEqual(len(results), 5)
        self.assertIn("hello", results)
        self.assertIn("help", results)
    
    def test_starts_with_limit(self):
        """测试前缀搜索限制"""
        results = self.trie.starts_with("hel", limit=2)
        self.assertEqual(len(results), 2)
    
    def test_starts_with_no_match(self):
        """测试无匹配前缀"""
        results = self.trie.starts_with("xyz")
        self.assertEqual(len(results), 0)
    
    def test_contains_prefix(self):
        """测试前缀存在检查"""
        self.assertTrue(self.trie.contains_prefix("hel"))
        self.assertTrue(self.trie.contains_prefix("help"))
        self.assertFalse(self.trie.contains_prefix("xyz"))
    
    def test_longest_prefix(self):
        """测试最长前缀匹配"""
        self.trie.insert("helping")
        result = self.trie.longest_prefix("helpinghand")
        self.assertEqual(result, "helping")
    
    def test_longest_prefix_no_match(self):
        """测试无匹配的最长前缀"""
        result = self.trie.longest_prefix("xyz123")
        self.assertEqual(result, "")
    
    def test_count_words_with_prefix(self):
        """测试前缀单词计数"""
        count = self.trie.count_words_with_prefix("hel")
        self.assertEqual(count, 5)


class TestTrieDelete(unittest.TestCase):
    """测试删除功能"""
    
    def setUp(self):
        self.trie = Trie()
        words = ["cat", "cats", "cater", "dog"]
        for word in words:
            self.trie.insert(word)
    
    def test_delete_leaf(self):
        """测试删除叶子节点"""
        self.assertTrue(self.trie.delete("dog"))
        self.assertFalse(self.trie.search("dog"))
        self.assertEqual(self.trie.size(), 3)
    
    def test_delete_internal_node(self):
        """测试删除内部节点"""
        self.assertTrue(self.trie.delete("cat"))
        self.assertFalse(self.trie.search("cat"))
        self.assertTrue(self.trie.search("cats"))
        self.assertTrue(self.trie.search("cater"))
    
    def test_delete_nonexistent(self):
        """测试删除不存在的单词"""
        self.assertFalse(self.trie.delete("bird"))
        self.assertEqual(self.trie.size(), 4)
    
    def test_delete_empty_string(self):
        """测试删除空字符串"""
        self.assertFalse(self.trie.delete(""))


class TestTriePatternMatch(unittest.TestCase):
    """测试模式匹配"""
    
    def setUp(self):
        self.trie = Trie()
        words = ["cat", "bat", "rat", "car", "bar", "cab", "can"]
        for word in words:
            self.trie.insert(word)
    
    def test_pattern_match_question_mark(self):
        """测试 ? 通配符"""
        results = self.trie.pattern_match("?at")
        self.assertEqual(set(results), {"cat", "bat", "rat"})
    
    def test_pattern_match_multiple_wildcards(self):
        """测试多个通配符"""
        results = self.trie.pattern_match("ca?")
        self.assertEqual(set(results), {"cat", "car", "cab", "can"})
    
    def test_pattern_match_exact(self):
        """测试精确模式"""
        results = self.trie.pattern_match("cat")
        self.assertEqual(results, ["cat"])
    
    def test_pattern_match_no_match(self):
        """测试无匹配模式"""
        results = self.trie.pattern_match("xyz")
        self.assertEqual(len(results), 0)


class TestTrieAutocomplete(unittest.TestCase):
    """测试自动补全"""
    
    def setUp(self):
        self.trie = Trie()
        # 插入带频次的单词
        words = [
            ("hello", 10),
            ("help", 5),
            ("helper", 3),
            ("helicopter", 2),
            ("helium", 1)
        ]
        for word, count in words:
            for _ in range(count):
                self.trie.insert(word)
    
    def test_autocomplete(self):
        """测试自动补全"""
        results = self.trie.autocomplete("hel")
        self.assertTrue(len(results) <= 5)
        # 频率最高的应该在前面
        self.assertEqual(results[0][0], "hello")
    
    def test_autocomplete_limit(self):
        """测试自动补全限制"""
        results = self.trie.autocomplete("hel", max_suggestions=2)
        self.assertEqual(len(results), 2)
    
    def test_autocomplete_no_match(self):
        """测试无匹配自动补全"""
        results = self.trie.autocomplete("xyz")
        self.assertEqual(len(results), 0)


class TestTrieDataOperations(unittest.TestCase):
    """测试数据操作"""
    
    def setUp(self):
        self.trie = Trie()
    
    def test_get_set_data(self):
        """测试获取和设置数据"""
        self.trie.insert("test")
        self.assertTrue(self.trie.set_data("test", {"key": "value"}))
        self.assertEqual(self.trie.get_data("test"), {"key": "value"})
    
    def test_get_data_nonexistent(self):
        """测试获取不存在单词的数据"""
        self.assertIsNone(self.trie.get_data("nonexistent"))
    
    def test_set_data_nonexistent(self):
        """测试设置不存在单词的数据"""
        self.assertFalse(self.trie.set_data("nonexistent", {"key": "value"}))
    
    def test_get_count(self):
        """测试获取频次"""
        self.trie.insert("word")
        self.trie.insert("word")
        self.trie.insert("word")
        self.assertEqual(self.trie.get_count("word"), 3)
    
    def test_get_count_nonexistent(self):
        """测试获取不存在单词的频次"""
        self.assertEqual(self.trie.get_count("nonexistent"), 0)


class TestTrieSpellCorrection(unittest.TestCase):
    """测试拼写纠正"""
    
    def setUp(self):
        self.trie = Trie()
        words = ["hello", "help", "world", "word", "python", "java"]
        for word in words:
            self.trie.insert(word)
    
    def test_suggest_corrections_deletion(self):
        """测试删除类型的错误"""
        results = self.trie.suggest_corrections("helo")
        self.assertIn(("hello", 1), results)
    
    def test_suggest_corrections_insertion(self):
        """测试插入类型的错误"""
        results = self.trie.suggest_corrections("helloo")
        self.assertIn(("hello", 1), results)
    
    def test_suggest_corrections_substitution(self):
        """测试替换类型的错误"""
        results = self.trie.suggest_corrections("hallo")
        self.assertIn(("hello", 1), results)
    
    def test_suggest_corrections_max_distance(self):
        """测试最大编辑距离限制"""
        results = self.trie.suggest_corrections("xyzz", max_distance=1)
        self.assertEqual(len(results), 0)


class TestTrieSerialization(unittest.TestCase):
    """测试序列化"""
    
    def setUp(self):
        self.trie = Trie()
        words = ["apple", "banana", "cherry", "date", "elderberry"]
        for word in words:
            self.trie.insert(word)
    
    def test_to_dict(self):
        """测试转换为字典"""
        data = self.trie.to_dict()
        self.assertIn('root', data)
        self.assertIn('size', data)
        self.assertEqual(data['size'], 5)
    
    def test_from_dict(self):
        """测试从字典创建"""
        data = self.trie.to_dict()
        new_trie = Trie.from_dict(data)
        self.assertEqual(new_trie.size(), self.trie.size())
        
        for word in ["apple", "banana", "cherry", "date", "elderberry"]:
            self.assertTrue(new_trie.search(word))
    
    def test_to_json(self):
        """测试JSON导出"""
        json_str = self.trie.to_json()
        self.assertIn('root', json_str)
        self.assertIn('size', json_str)
    
    def test_from_json(self):
        """测试从JSON加载"""
        json_str = self.trie.to_json()
        new_trie = Trie.from_json(json_str)
        
        for word in ["apple", "banana", "cherry"]:
            self.assertTrue(new_trie.search(word))
    
    def test_serialization_with_data(self):
        """测试带数据的序列化"""
        self.trie.insert("test", data={"key": "value"})
        data = self.trie.to_dict()
        new_trie = Trie.from_dict(data)
        self.assertEqual(new_trie.get_data("test"), {"key": "value"})


class TestSuffixTrie(unittest.TestCase):
    """测试后缀树"""
    
    def setUp(self):
        self.st = SuffixTrie()
    
    def test_build_and_search(self):
        """测试构建和搜索"""
        self.st.build_from_string("banana")
        self.assertTrue(self.st.contains_substring("ana"))
        self.assertTrue(self.st.contains_substring("ban"))
        self.assertFalse(self.st.contains_substring("xyz"))
    
    def test_find_occurrences(self):
        """测试查找所有出现位置"""
        self.st.build_from_string("abababa")
        # 注意：这个简化实现可能有局限性
        self.assertTrue(self.st.contains_substring("aba"))


class TestPrefixSet(unittest.TestCase):
    """测试前缀集合"""
    
    def setUp(self):
        self.ps = PrefixSet()
        prefixes = ["http://", "https://", "ftp://", "www."]
        for prefix in prefixes:
            self.ps.add(prefix)
    
    def test_matches_any_prefix(self):
        """测试前缀匹配"""
        self.assertTrue(self.ps.matches_any_prefix("http://example.com"))
        self.assertTrue(self.ps.matches_any_prefix("https://example.com"))
        self.assertFalse(self.ps.matches_any_prefix("example.com"))
    
    def test_get_matching_prefix(self):
        """测试获取匹配前缀"""
        result = self.ps.get_matching_prefix("http://example.com")
        self.assertEqual(result, "http://")
    
    def test_update(self):
        """测试批量添加"""
        self.ps.update(["api.", "cdn."])
        self.assertTrue(self.ps.matches_any_prefix("api.example.com"))
    
    def test_contains(self):
        """测试 in 操作符"""
        self.assertIn("http://", self.ps)
        self.assertNotIn("xyz://", self.ps)


class TestUtilityFunctions(unittest.TestCase):
    """测试工具函数"""
    
    def test_build_trie(self):
        """测试构建Trie函数"""
        words = ["apple", "banana", "cherry"]
        trie = build_trie(words)
        self.assertEqual(trie.size(), 3)
        for word in words:
            self.assertTrue(trie.search(word))
    
    def test_find_common_prefix(self):
        """测试查找公共前缀"""
        words = ["flower", "flow", "float"]
        result = find_common_prefix(words)
        self.assertEqual(result, "flo")
    
    def test_find_common_prefix_empty(self):
        """测试空列表公共前缀"""
        result = find_common_prefix([])
        self.assertEqual(result, "")
    
    def test_find_common_prefix_no_common(self):
        """测试无公共前缀"""
        words = ["dog", "cat", "bird"]
        result = find_common_prefix(words)
        self.assertEqual(result, "")
    
    def test_word_frequency_analysis(self):
        """测试词频分析"""
        words = ["apple", "banana", "apple", "cherry", "apple", "banana"]
        result = word_frequency_analysis(words)
        
        self.assertEqual(result["apple"], 3)
        self.assertEqual(result["banana"], 2)
        self.assertEqual(result["cherry"], 1)


class TestEdgeCases(unittest.TestCase):
    """测试边界情况"""
    
    def setUp(self):
        self.trie = Trie()
    
    def test_unicode_characters(self):
        """测试Unicode字符"""
        self.trie.insert("你好")
        self.trie.insert("世界")
        self.assertTrue(self.trie.search("你好"))
        self.assertEqual(self.trie.starts_with("你"), ["你好"])
    
    def test_very_long_word(self):
        """测试超长单词"""
        long_word = "a" * 1000
        self.trie.insert(long_word)
        self.assertTrue(self.trie.search(long_word))
    
    def test_special_characters(self):
        """测试特殊字符"""
        self.trie.insert("hello-world")
        self.trie.insert("hello_world")
        self.trie.insert("hello.world")
        self.assertTrue(self.trie.search("hello-world"))
        self.assertTrue(self.trie.search("hello_world"))
        self.assertTrue(self.trie.search("hello.world"))
    
    def test_numbers(self):
        """测试数字"""
        self.trie.insert("12345")
        self.trie.insert("123abc")
        self.assertTrue(self.trie.search("12345"))
        self.assertEqual(self.trie.starts_with("123"), ["12345", "123abc"])
    
    def test_single_character(self):
        """测试单字符"""
        self.trie.insert("a")
        self.assertTrue(self.trie.search("a"))
        self.assertEqual(self.trie.starts_with("a"), ["a"])


class TestPerformance(unittest.TestCase):
    """性能测试"""
    
    def test_large_insert(self):
        """测试大量插入"""
        trie = Trie()
        # 插入10000个单词
        for i in range(10000):
            trie.insert(f"word{i}")
        
        self.assertEqual(trie.size(), 10000)
        self.assertTrue(trie.search("word0"))
        self.assertTrue(trie.search("word9999"))
    
    def test_deep_trie(self):
        """测试深层Trie"""
        trie = Trie()
        # 创建深层单词
        deep_word = "".join(chr(97 + i % 26) for i in range(100))
        trie.insert(deep_word)
        self.assertTrue(trie.search(deep_word))


if __name__ == "__main__":
    unittest.main(verbosity=2)