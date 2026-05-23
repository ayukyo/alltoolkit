"""
Trie Utilities 测试套件

包含完整的单元测试，覆盖所有功能。
"""

import unittest
import sys
import os

# 添加父目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from trie_utils.mod import (
    Trie, TrieNode, CompactTrie, SuffixTrie,
    build_trie, build_word_trie, autocomplete_from_list
)


class TestTrieNode(unittest.TestCase):
    """TrieNode 测试"""
    
    def test_create_node(self):
        """测试创建节点"""
        node = TrieNode()
        self.assertFalse(node.is_end)
        self.assertEqual(node.count, 0)
        self.assertIsNone(node.data)
        self.assertEqual(len(node.children), 0)
    
    def test_add_child(self):
        """测试添加子节点"""
        node = TrieNode()
        child = node.add_child('a')
        self.assertIsNotNone(child)
        self.assertTrue(node.has_child('a'))
        self.assertEqual(node.get_child('a'), child)
    
    def test_remove_child(self):
        """测试移除子节点"""
        node = TrieNode()
        node.add_child('a')
        self.assertTrue(node.remove_child('a'))
        self.assertFalse(node.has_child('a'))
        self.assertFalse(node.remove_child('b'))  # 不存在
    
    def test_is_leaf(self):
        """测试叶子节点判断"""
        node = TrieNode()
        self.assertTrue(node.is_leaf())
        node.add_child('a')
        self.assertFalse(node.is_leaf())
    
    def test_to_dict_from_dict(self):
        """测试序列化和反序列化"""
        node = TrieNode()
        node.is_end = True
        node.count = 5
        node.data = {"key": "value"}
        node.add_child('a')
        
        data = node.to_dict()
        restored = TrieNode.from_dict(data)
        
        self.assertEqual(restored.is_end, node.is_end)
        self.assertEqual(restored.count, node.count)
        self.assertEqual(restored.data, node.data)
        self.assertTrue(restored.has_child('a'))


class TestTrie(unittest.TestCase):
    """Trie 测试"""
    
    def setUp(self):
        """测试前准备"""
        self.trie = Trie()
        self.words = ["apple", "app", "application", "apply", "banana", "band"]
    
    def test_insert_and_search(self):
        """测试插入和搜索"""
        for word in self.words:
            self.assertTrue(self.trie.insert(word))
        
        for word in self.words:
            self.assertTrue(self.trie.search(word))
        
        # 搜索不存在的单词
        self.assertFalse(self.trie.search("orange"))
        self.assertFalse(self.trie.search("apples"))
        self.assertFalse(self.trie.search(""))
    
    def test_insert_duplicate(self):
        """测试重复插入"""
        self.assertTrue(self.trie.insert("hello"))
        self.assertFalse(self.trie.insert("hello"))  # 重复
        self.assertEqual(len(self.trie), 1)
    
    def test_insert_empty(self):
        """测试插入空字符串"""
        self.assertFalse(self.trie.insert(""))
    
    def test_starts_with(self):
        """测试前缀匹配"""
        for word in self.words:
            self.trie.insert(word)
        
        # 测试各种前缀
        self.assertEqual(set(self.trie.starts_with("app")), 
                        {"apple", "app", "application", "apply"})
        self.assertEqual(set(self.trie.starts_with("ban")), 
                        {"banana", "band"})
        self.assertEqual(self.trie.starts_with("or"), [])
        
        # 空前缀返回所有
        all_words = self.trie.starts_with("")
        self.assertEqual(set(all_words), set(self.words))
    
    def test_delete(self):
        """测试删除"""
        for word in self.words:
            self.trie.insert(word)
        
        # 删除存在的单词
        self.assertTrue(self.trie.delete("apple"))
        self.assertFalse(self.trie.search("apple"))
        self.assertTrue(self.trie.search("app"))  # 共享前缀应保留
        
        # 删除不存在的单词
        self.assertFalse(self.trie.delete("orange"))
        self.assertFalse(self.trie.delete(""))  # 空字符串
    
    def test_update_and_get_data(self):
        """测试更新和获取数据"""
        self.trie.insert("test", data={"value": 1})
        self.assertEqual(self.trie.get_data("test"), {"value": 1})
        
        self.assertTrue(self.trie.update("test", {"value": 2}))
        self.assertEqual(self.trie.get_data("test"), {"value": 2})
        
        # 更新不存在的单词
        self.assertFalse(self.trie.update("notexist", data={}))
    
    def test_count(self):
        """测试词频计数"""
        self.trie.insert("hello", count=5)
        self.trie.insert("hello", count=3)  # 累加
        self.trie.insert("world", count=10)
        
        self.assertEqual(self.trie.get_count("hello"), 8)
        self.assertEqual(self.trie.get_count("world"), 10)
        self.assertEqual(self.trie.get_count("notexist"), 0)
    
    def test_list_all(self):
        """测试列出所有单词"""
        for word in self.words:
            self.trie.insert(word)
        
        all_words = self.trie.list_all()
        self.assertEqual(set(all_words), set(self.words))
    
    def test_list_with_counts(self):
        """测试列出单词和词频"""
        self.trie.insert("a", count=1)
        self.trie.insert("b", count=2)
        
        result = self.trie.list_with_counts()
        self.assertEqual(dict(result), {"a": 1, "b": 2})
    
    def test_autocomplete(self):
        """测试自动补全"""
        for word, count in [("apple", 10), ("app", 5), ("application", 8), 
                           ("apply", 3), ("apricot", 1)]:
            self.trie.insert(word, count=count)
        
        # 按词频排序
        suggestions = self.trie.autocomplete("app", limit=3)
        self.assertEqual(suggestions, ["apple", "application", "app"])
        
        # 空前缀返回最高频
        all_suggestions = self.trie.autocomplete("", limit=3)
        self.assertEqual(all_suggestions, ["apple", "application", "app"])
    
    def test_fuzzy_search(self):
        """测试模糊搜索"""
        for word in ["cat", "dog", "car", "cart", "care", "careful"]:
            self.trie.insert(word)
        
        # "cta" 和 "cat" 的编辑距离是 2（交换 't' 和 'a'）
        result = self.trie.fuzzy_search("cta", max_distance=2)
        matches = [word for word, dist in result]
        self.assertIn("cat", matches)
        
        # "ct" 和 "cat" 的编辑距离是 1（删除 'a'）
        result = self.trie.fuzzy_search("ct", max_distance=1)
        matches = [word for word, dist in result]
        self.assertIn("cat", matches)
        
        # 精确匹配
        result = self.trie.fuzzy_search("cat", max_distance=0)
        self.assertEqual(result, [("cat", 0)])
    
    def test_longest_prefix(self):
        """测试最长匹配前缀"""
        for word in ["apple", "app", "application"]:
            self.trie.insert(word)
        
        self.assertEqual(self.trie.longest_prefix("apples"), "apple")
        self.assertEqual(self.trie.longest_prefix("applicable"), "app")
        self.assertEqual(self.trie.longest_prefix("orange"), "")
    
    def test_longest_common_prefix(self):
        """测试最长公共前缀"""
        for word in ["flower", "flow", "flight"]:
            self.trie.insert(word)
        
        self.assertEqual(self.trie.longest_common_prefix(), "fl")
    
    def test_count_prefix(self):
        """测试前缀计数"""
        for word in ["app", "apple", "application", "banana"]:
            self.trie.insert(word)
        
        self.assertEqual(self.trie.count_prefix("app"), 3)
        self.assertEqual(self.trie.count_prefix("ban"), 1)
        self.assertEqual(self.trie.count_prefix("or"), 0)
    
    def test_clear(self):
        """测试清空"""
        for word in self.words:
            self.trie.insert(word)
        
        self.trie.clear()
        self.assertEqual(len(self.trie), 0)
        self.assertEqual(self.trie.list_all(), [])
    
    def test_contains(self):
        """测试 __contains__"""
        self.trie.insert("hello")
        self.assertIn("hello", self.trie)
        self.assertNotIn("world", self.trie)
    
    def test_iter(self):
        """测试迭代"""
        for word in self.words:
            self.trie.insert(word)
        
        words_from_iter = list(self.trie)
        self.assertEqual(set(words_from_iter), set(self.words))
    
    def test_json_serialization(self):
        """测试 JSON 序列化"""
        for word in self.words:
            self.trie.insert(word)
        
        json_str = self.trie.to_json()
        restored = Trie.from_json(json_str)
        
        self.assertEqual(len(restored), len(self.trie))
        for word in self.words:
            self.assertTrue(restored.search(word))
    
    def test_get_stats(self):
        """测试统计信息"""
        for word in self.words:
            self.trie.insert(word)
        
        stats = self.trie.get_stats()
        self.assertEqual(stats['word_count'], len(self.words))
        self.assertGreater(stats['node_count'], 0)
        self.assertGreater(stats['max_depth'], 0)
    
    def test_large_dataset(self):
        """测试大数据集"""
        import random
        import string
        
        # 生成 1000 个随机单词
        words = []
        for _ in range(1000):
            length = random.randint(3, 10)
            word = ''.join(random.choices(string.ascii_lowercase, k=length))
            words.append(word)
        
        trie = Trie()
        for word in words:
            trie.insert(word)
        
        # 验证
        for word in words:
            self.assertTrue(trie.search(word))
        
        stats = trie.get_stats()
        self.assertEqual(stats['word_count'], len(set(words)))


class TestCompactTrie(unittest.TestCase):
    """压缩字典树测试"""
    
    def setUp(self):
        """测试前准备"""
        self.trie = CompactTrie()
        self.words = ["apple", "app", "application", "banana", "band"]
    
    def test_insert_and_search(self):
        """测试插入和搜索"""
        for word in self.words:
            self.trie.insert(word)
        
        for word in self.words:
            self.assertTrue(self.trie.search(word))
        
        # 搜索不存在的单词
        self.assertFalse(self.trie.search("orange"))
        self.assertFalse(self.trie.search(""))
    
    def test_starts_with(self):
        """测试前缀匹配"""
        for word in self.words:
            self.trie.insert(word)
        
        app_words = self.trie.starts_with("app")
        self.assertEqual(set(app_words), {"apple", "app", "application"})
    
    def test_list_all(self):
        """测试列出所有单词"""
        for word in self.words:
            self.trie.insert(word)
        
        all_words = self.trie.list_all()
        self.assertEqual(set(all_words), set(self.words))
    
    def test_duplicate_insert(self):
        """测试重复插入"""
        self.assertTrue(self.trie.insert("hello"))
        self.assertFalse(self.trie.insert("hello"))
        self.assertEqual(len(self.trie), 1)
    
    def test_contains(self):
        """测试 __contains__"""
        self.trie.insert("test")
        self.assertIn("test", self.trie)
        self.assertNotIn("nothere", self.trie)
    
    def test_space_efficiency(self):
        """测试空间效率（相比普通 Trie）"""
        # 对于共享前缀的单词，压缩 Trie 应更高效
        words = ["abc", "abcd", "abcde", "abcdef"]
        
        compact = CompactTrie()
        for word in words:
            compact.insert(word)
        
        # 所有单词都能找到
        for word in words:
            self.assertTrue(compact.search(word))


class TestSuffixTrie(unittest.TestCase):
    """后缀字典树测试"""
    
    def setUp(self):
        """测试前准备"""
        self.trie = SuffixTrie()
    
    def test_build(self):
        """测试构建"""
        self.trie.build("banana")
        self.assertGreater(len(self.trie), 0)
    
    def test_contains_substring(self):
        """测试子串查找"""
        self.trie.build("banana")
        
        self.assertTrue(self.trie.contains_substring("ana"))
        self.assertTrue(self.trie.contains_substring("ban"))
        self.assertTrue(self.trie.contains_substring("nana"))
        self.assertTrue(self.trie.contains_substring("banana"))
        self.assertTrue(self.trie.contains_substring(""))  # 空串
        
        self.assertFalse(self.trie.contains_substring("xyz"))
        self.assertFalse(self.trie.contains_substring("bananana"))
    
    def test_count_occurrences(self):
        """测试出现次数统计"""
        self.trie.build("banana")
        
        self.assertEqual(self.trie.count_occurrences("ana"), 2)
        self.assertEqual(self.trie.count_occurrences("an"), 2)
        self.assertEqual(self.trie.count_occurrences("na"), 2)
        self.assertEqual(self.trie.count_occurrences("a"), 3)
        self.assertEqual(self.trie.count_occurrences("n"), 2)
        self.assertEqual(self.trie.count_occurrences("banana"), 1)
        self.assertEqual(self.trie.count_occurrences("xyz"), 0)
    
    def test_find_all_occurrences(self):
        """测试查找所有出现位置"""
        self.trie.build("banana")
        
        self.assertEqual(self.trie.find_all_occurrences("ana"), [1, 3])
        self.assertEqual(self.trie.find_all_occurrences("ban"), [0])
        self.assertEqual(self.trie.find_all_occurrences("xyz"), [])
    
    def test_longest_repeated_substring(self):
        """测试最长重复子串"""
        self.trie.build("banana")
        lrs = self.trie.longest_repeated_substring()
        # "ana" 或 "na" 或 "an" 都是重复子串
        self.assertIn(lrs, ["ana", "na", "an"])
        
        # 无重复
        self.trie.build("abcde")
        self.assertEqual(self.trie.longest_repeated_substring(), "")
    
    def test_clear(self):
        """测试清空"""
        self.trie.build("test")
        self.trie.clear()
        self.assertEqual(len(self.trie), 0)


class TestConvenienceFunctions(unittest.TestCase):
    """便捷函数测试"""
    
    def test_build_trie(self):
        """测试 build_trie"""
        words = ["apple", "app", "banana"]
        trie = build_trie(words)
        
        for word in words:
            self.assertTrue(trie.search(word))
    
    def test_build_word_trie(self):
        """测试 build_word_trie"""
        words_with_counts = [("apple", 5), ("app", 3), ("banana", 10)]
        trie = build_word_trie(words_with_counts)
        
        self.assertEqual(trie.get_count("apple"), 5)
        self.assertEqual(trie.get_count("app"), 3)
        self.assertEqual(trie.get_count("banana"), 10)
    
    def test_autocomplete_from_list(self):
        """测试 autocomplete_from_list"""
        words = ["apple", "app", "application", "apply", "banana"]
        suggestions = autocomplete_from_list(words, "app", limit=3)
        
        self.assertEqual(len(suggestions), 3)
        for word in suggestions:
            self.assertTrue(word.startswith("app"))


class TestEdgeCases(unittest.TestCase):
    """边界情况测试"""
    
    def test_single_character(self):
        """测试单字符"""
        trie = Trie()
        trie.insert("a")
        self.assertTrue(trie.search("a"))
        self.assertEqual(trie.starts_with("a"), ["a"])
    
    def test_unicode(self):
        """测试 Unicode"""
        trie = Trie()
        words = ["你好", "你好世界", "世界"]
        for word in words:
            trie.insert(word)
        
        self.assertTrue(trie.search("你好"))
        self.assertEqual(set(trie.starts_with("你好")), {"你好", "你好世界"})
    
    def test_special_characters(self):
        """测试特殊字符"""
        trie = Trie()
        words = ["hello-world", "hello_world", "hello.world", "hello world"]
        for word in words:
            trie.insert(word)
        
        for word in words:
            self.assertTrue(trie.search(word))
    
    def test_very_long_word(self):
        """测试超长单词"""
        trie = Trie()
        long_word = "a" * 10000
        trie.insert(long_word)
        self.assertTrue(trie.search(long_word))
    
    def test_many_similar_words(self):
        """测试大量相似单词"""
        trie = Trie()
        # 插入 100 个只在最后一个字符不同的单词
        base = "abcdefghijklmnopqrstuvwxy"
        words = [base + chr(ord('a') + i) for i in range(26)]
        
        for word in words:
            trie.insert(word)
        
        self.assertEqual(len(trie), 26)
        for word in words:
            self.assertTrue(trie.search(word))
    
    def test_empty_trie(self):
        """测试空字典树"""
        trie = Trie()
        
        self.assertEqual(len(trie), 0)
        self.assertEqual(trie.list_all(), [])
        self.assertEqual(trie.starts_with("anything"), [])
        self.assertFalse(trie.search("anything"))
    
    def test_deep_nesting(self):
        """测试深层嵌套"""
        trie = Trie()
        # 创建深度为 100 的单词
        word = ""
        for i in range(100):
            word += chr(ord('a') + (i % 26))
            trie.insert(word)
        
        # 验证所有单词
        test_word = ""
        for i in range(100):
            test_word += chr(ord('a') + (i % 26))
            self.assertTrue(trie.search(test_word))


class TestPerformance(unittest.TestCase):
    """性能测试"""
    
    def test_insert_performance(self):
        """测试插入性能"""
        import time
        import random
        import string
        
        # 生成 10000 个单词
        words = []
        for _ in range(10000):
            length = random.randint(5, 15)
            word = ''.join(random.choices(string.ascii_lowercase, k=length))
            words.append(word)
        
        trie = Trie()
        start = time.time()
        for word in words:
            trie.insert(word)
        elapsed = time.time() - start
        
        # 10000 次插入应该在 1 秒内完成
        self.assertLess(elapsed, 1.0)
        print(f"\n插入 10000 个单词耗时: {elapsed:.4f} 秒")
    
    def test_search_performance(self):
        """测试搜索性能"""
        import time
        import random
        import string
        
        # 构建字典树
        trie = Trie()
        words = []
        for _ in range(10000):
            length = random.randint(5, 15)
            word = ''.join(random.choices(string.ascii_lowercase, k=length))
            words.append(word)
            trie.insert(word)
        
        # 搜索测试
        start = time.time()
        for word in words:
            trie.search(word)
        elapsed = time.time() - start
        
        # 10000 次搜索应该在 0.5 秒内完成
        self.assertLess(elapsed, 0.5)
        print(f"\n搜索 10000 个单词耗时: {elapsed:.4f} 秒")
    
    def test_autocomplete_performance(self):
        """测试自动补全性能"""
        import time
        import random
        import string
        
        # 构建字典树
        trie = Trie()
        for _ in range(10000):
            length = random.randint(5, 15)
            word = ''.join(random.choices(string.ascii_lowercase, k=length))
            trie.insert(word)
        
        # 自动补全测试
        prefixes = ['a', 'ab', 'abc', 'abcd']
        start = time.time()
        for prefix in prefixes * 100:  # 400 次补全
            trie.autocomplete(prefix, limit=10)
        elapsed = time.time() - start
        
        print(f"\n400 次自动补全耗时: {elapsed:.4f} 秒")


if __name__ == "__main__":
    # 运行测试
    unittest.main(verbosity=2)