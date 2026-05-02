"""
自动补全工具模块测试
Autocomplete Utilities Test Suite
"""

import unittest
import json
from mod import (
    TrieAutocomplete, NGramAutocomplete, HybridAutocomplete,
    Suggestion, TrieNode,
    create_autocomplete, levenshtein_distance, jaccard_similarity
)


class TestTrieAutocompleteBasic(unittest.TestCase):
    """Trie 自动补全基础测试"""
    
    def test_create_trie(self):
        """测试创建 Trie"""
        trie = TrieAutocomplete()
        self.assertEqual(len(trie), 0)
        self.assertEqual(trie.word_count, 0)
    
    def test_create_trie_case_sensitive(self):
        """测试区分大小写的 Trie"""
        trie = TrieAutocomplete(case_sensitive=True)
        trie.insert("Hello")
        trie.insert("hello")
        
        self.assertEqual(len(trie), 2)
        self.assertIn("Hello", trie)
        self.assertIn("hello", trie)
    
    def test_insert_single(self):
        """测试插入单个单词"""
        trie = TrieAutocomplete()
        trie.insert("hello")
        
        self.assertEqual(len(trie), 1)
        self.assertTrue(trie.contains("hello"))
        self.assertFalse(trie.contains("world"))
    
    def test_insert_multiple(self):
        """测试插入多个单词"""
        trie = TrieAutocomplete()
        words = ["apple", "application", "apply", "app"]
        
        for word in words:
            trie.insert(word)
        
        self.assertEqual(len(trie), 4)
        for word in words:
            self.assertTrue(trie.contains(word))
    
    def test_insert_with_frequency(self):
        """测试带频率插入"""
        trie = TrieAutocomplete()
        trie.insert("hello", frequency=5)
        
        info = trie.get_word_info("hello")
        self.assertIsNotNone(info)
        self.assertEqual(info['frequency'], 5)
    
    def test_insert_with_metadata(self):
        """测试带元数据插入"""
        trie = TrieAutocomplete()
        trie.insert("hello", metadata={"category": "greeting", "lang": "en"})
        
        info = trie.get_word_info("hello")
        self.assertIsNotNone(info)
        self.assertEqual(info['metadata']['category'], "greeting")
        self.assertEqual(info['metadata']['lang'], "en")
    
    def test_insert_duplicate(self):
        """测试重复插入"""
        trie = TrieAutocomplete()
        trie.insert("hello")
        trie.insert("hello")
        trie.insert("hello")
        
        self.assertEqual(len(trie), 1)
        info = trie.get_word_info("hello")
        self.assertEqual(info['frequency'], 3)
    
    def test_insert_batch(self):
        """测试批量插入"""
        trie = TrieAutocomplete()
        words = ["one", "two", "three"]
        frequencies = [1, 2, 3]
        
        trie.insert_batch(words, frequencies)
        
        self.assertEqual(len(trie), 3)
        self.assertEqual(trie.get_word_info("one")['frequency'], 1)
        self.assertEqual(trie.get_word_info("two")['frequency'], 2)
        self.assertEqual(trie.get_word_info("three")['frequency'], 3)
    
    def test_contains_case_insensitive(self):
        """测试不区分大小写包含"""
        trie = TrieAutocomplete(case_sensitive=False)
        trie.insert("Hello")
        
        self.assertTrue(trie.contains("Hello"))
        self.assertTrue(trie.contains("hello"))
        self.assertTrue(trie.contains("HELLO"))


class TestTrieAutocompleteSearch(unittest.TestCase):
    """Trie 自动补全搜索测试"""
    
    def setUp(self):
        """设置测试数据"""
        self.trie = TrieAutocomplete()
        words = [
            "apple", "application", "apply", "app",
            "banana", "band", "bandana",
            "cat", "caterpillar", "category"
        ]
        for word in words:
            self.trie.insert(word, frequency=len(word))
    
    def test_prefix_search_basic(self):
        """测试基本前缀搜索"""
        results = self.trie.search("app")
        
        self.assertEqual(len(results), 4)
        texts = [r.text for r in results]
        self.assertIn("apple", texts)
        self.assertIn("application", texts)
        self.assertIn("apply", texts)
        self.assertIn("app", texts)
    
    def test_prefix_search_no_match(self):
        """测试无匹配的前缀搜索"""
        results = self.trie.search("xyz")
        self.assertEqual(len(results), 0)
    
    def test_prefix_search_single_result(self):
        """测试单个结果的前缀搜索"""
        results = self.trie.search("banan")
        
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].text, "banana")
    
    def test_prefix_search_empty(self):
        """测试空前缀搜索"""
        results = self.trie.search("")
        
        # 应该返回所有单词
        self.assertGreater(len(results), 0)
    
    def test_frequency_sorting(self):
        """测试按频率排序"""
        results = self.trie.search("app")
        
        # 更长的单词频率更高
        texts = [r.text for r in results]
        # "application" (11 chars) should have higher frequency than "app" (3 chars)
        app_result = next(r for r in results if r.text == "app")
        application_result = next(r for r in results if r.text == "application")
        self.assertGreater(application_result.frequency, app_result.frequency)
    
    def test_max_suggestions(self):
        """测试最大建议数限制"""
        trie = TrieAutocomplete(max_suggestions=2)
        for word in ["apple", "application", "apply", "app"]:
            trie.insert(word)
        
        results = trie.search("app")
        self.assertLessEqual(len(results), 2)
    
    def test_fuzzy_search(self):
        """测试模糊搜索"""
        results = self.trie.fuzzy_search("aple", max_distance=2)
        
        # 应该匹配 "apple"
        texts = [r.text for r in results]
        self.assertIn("apple", texts)
    
    def test_fuzzy_search_no_match(self):
        """测试无匹配的模糊搜索"""
        results = self.trie.fuzzy_search("xyzabc", max_distance=1)
        self.assertEqual(len(results), 0)


class TestTrieAutocompleteOperations(unittest.TestCase):
    """Trie 自动补全操作测试"""
    
    def test_remove(self):
        """测试删除单词"""
        trie = TrieAutocomplete()
        trie.insert("hello")
        trie.insert("help")
        
        self.assertTrue(trie.remove("hello"))
        self.assertFalse(trie.contains("hello"))
        self.assertTrue(trie.contains("help"))
    
    def test_remove_nonexistent(self):
        """测试删除不存在的单词"""
        trie = TrieAutocomplete()
        trie.insert("hello")
        
        self.assertFalse(trie.remove("world"))
        self.assertEqual(len(trie), 1)
    
    def test_clear(self):
        """测试清空"""
        trie = TrieAutocomplete()
        trie.insert("hello")
        trie.insert("world")
        
        trie.clear()
        
        self.assertEqual(len(trie), 0)
        self.assertFalse(trie.contains("hello"))
        self.assertFalse(trie.contains("world"))
    
    def test_get_all_words(self):
        """测试获取所有单词"""
        trie = TrieAutocomplete()
        words = ["apple", "banana", "cherry"]
        for word in words:
            trie.insert(word)
        
        all_words = trie.get_all_words()
        self.assertEqual(set(all_words), set(words))
    
    def test_starts_with(self):
        """测试前缀存在检查"""
        trie = TrieAutocomplete()
        trie.insert("hello")
        
        self.assertTrue(trie.starts_with("he"))
        self.assertTrue(trie.starts_with("hello"))
        self.assertFalse(trie.starts_with("ha"))
    
    def test_increment_frequency(self):
        """测试增加频率"""
        trie = TrieAutocomplete()
        trie.insert("hello", frequency=5)
        
        trie.increment_frequency("hello", 3)
        
        info = trie.get_word_info("hello")
        self.assertEqual(info['frequency'], 8)
    
    def test_longest_common_prefix(self):
        """测试最长公共前缀"""
        trie = TrieAutocomplete()
        trie.insert("apple")
        trie.insert("application")
        trie.insert("apply")
        
        lcp = trie.longest_common_prefix()
        self.assertEqual(lcp, "appl")
    
    def test_longest_common_prefix_single_word(self):
        """测试单个单词的最长公共前缀"""
        trie = TrieAutocomplete()
        trie.insert("hello")
        
        lcp = trie.longest_common_prefix()
        self.assertEqual(lcp, "hello")


class TestTrieAutocompleteSerialization(unittest.TestCase):
    """Trie 自动补全序列化测试"""
    
    def test_to_dict(self):
        """测试转换为字典"""
        trie = TrieAutocomplete(case_sensitive=True, max_suggestions=5)
        trie.insert("hello", frequency=3)
        trie.insert("world", frequency=2)
        
        data = trie.to_dict()
        
        self.assertEqual(data['case_sensitive'], True)
        self.assertEqual(data['max_suggestions'], 5)
        self.assertEqual(len(data['words']), 2)
    
    def test_from_dict(self):
        """测试从字典创建"""
        data = {
            'case_sensitive': False,
            'max_suggestions': 10,
            'words': [
                {'text': 'hello', 'frequency': 3},
                {'text': 'world', 'frequency': 2}
            ]
        }
        
        trie = TrieAutocomplete.from_dict(data)
        
        self.assertEqual(len(trie), 2)
        self.assertTrue(trie.contains('hello'))
        self.assertEqual(trie.get_word_info('hello')['frequency'], 3)
    
    def test_to_json(self):
        """测试 JSON 序列化"""
        trie = TrieAutocomplete()
        trie.insert("hello")
        trie.insert("world")
        
        json_str = trie.to_json()
        data = json.loads(json_str)
        
        self.assertEqual(len(data['words']), 2)
    
    def test_from_json(self):
        """测试 JSON 反序列化"""
        trie = TrieAutocomplete()
        trie.insert("hello", frequency=5)
        
        json_str = trie.to_json()
        restored = TrieAutocomplete.from_json(json_str)
        
        self.assertEqual(len(restored), 1)
        self.assertTrue(restored.contains("hello"))
        self.assertEqual(restored.get_word_info("hello")['frequency'], 5)


class TestNGramAutocomplete(unittest.TestCase):
    """N-gram 自动补全测试"""
    
    def test_create_ngram(self):
        """测试创建 N-gram 自动补全器"""
        ngram = NGramAutocomplete(n=2)
        self.assertEqual(len(ngram), 0)
    
    def test_insert_single(self):
        """测试插入单词"""
        ngram = NGramAutocomplete()
        ngram.insert("hello")
        
        self.assertEqual(len(ngram), 1)
        self.assertTrue(ngram.contains("hello"))
    
    def test_insert_batch(self):
        """测试批量插入"""
        ngram = NGramAutocomplete()
        words = ["apple", "application", "apply"]
        ngram.insert_batch(words)
        
        self.assertEqual(len(ngram), 3)
    
    def test_search_basic(self):
        """测试基本搜索"""
        ngram = NGramAutocomplete()
        words = ["hello", "help", "helicopter", "world"]
        ngram.insert_batch(words)
        
        results = ngram.search("hel")
        texts = [r.text for r in results]
        
        # 应该匹配以 hel 开头的单词
        self.assertIn("hello", texts)
        self.assertIn("help", texts)
        self.assertIn("helicopter", texts)
    
    def test_prefix_search(self):
        """测试前缀搜索"""
        ngram = NGramAutocomplete()
        words = ["apple", "application", "apply", "apricot"]
        ngram.insert_batch(words)
        
        results = ngram.prefix_search("app")
        texts = [r.text for r in results]
        
        self.assertIn("apple", texts)
        self.assertIn("application", texts)
        self.assertIn("apply", texts)
        self.assertNotIn("apricot", texts)
    
    def test_remove(self):
        """测试删除单词"""
        ngram = NGramAutocomplete()
        ngram.insert("hello")
        
        self.assertTrue(ngram.remove("hello"))
        self.assertFalse(ngram.contains("hello"))
    
    def test_clear(self):
        """测试清空"""
        ngram = NGramAutocomplete()
        ngram.insert("hello")
        ngram.insert("world")
        
        ngram.clear()
        
        self.assertEqual(len(ngram), 0)
    
    def test_get_stats(self):
        """测试获取统计信息"""
        ngram = NGramAutocomplete(n=3)
        ngram.insert("hello")
        ngram.insert("world")
        
        stats = ngram.get_stats()
        
        self.assertEqual(stats['word_count'], 2)
        self.assertEqual(stats['n'], 3)
    
    def test_serialization(self):
        """测试序列化"""
        ngram = NGramAutocomplete()
        ngram.insert("hello", frequency=5)
        ngram.insert("world", frequency=3)
        
        data = ngram.to_dict()
        restored = NGramAutocomplete.from_dict(data)
        
        self.assertEqual(len(restored), 2)
        self.assertTrue(restored.contains("hello"))


class TestHybridAutocomplete(unittest.TestCase):
    """混合自动补全测试"""
    
    def test_create_hybrid(self):
        """测试创建混合自动补全器"""
        hybrid = HybridAutocomplete()
        self.assertEqual(len(hybrid), 0)
    
    def test_insert(self):
        """测试插入单词"""
        hybrid = HybridAutocomplete()
        hybrid.insert("hello")
        
        self.assertEqual(len(hybrid), 1)
        self.assertTrue(hybrid.contains("hello"))
    
    def test_search_fuzzy_disabled(self):
        """测试禁用模糊搜索"""
        hybrid = HybridAutocomplete()
        words = ["apple", "application", "apply"]
        hybrid.insert_batch(words)
        
        results = hybrid.search("app", fuzzy=False)
        texts = [r.text for r in results]
        
        self.assertIn("apple", texts)
        self.assertIn("application", texts)
    
    def test_search_fuzzy_enabled(self):
        """测试启用模糊搜索"""
        hybrid = HybridAutocomplete(fuzzy_weight=0.3)
        words = ["apple", "application", "banana"]
        hybrid.insert_batch(words)
        
        results = hybrid.search("aple", fuzzy=True)
        
        # 应该通过模糊匹配找到 "apple"
        self.assertGreater(len(results), 0)
    
    def test_remove(self):
        """测试删除单词"""
        hybrid = HybridAutocomplete()
        hybrid.insert("hello")
        
        self.assertTrue(hybrid.remove("hello"))
        self.assertFalse(hybrid.contains("hello"))
    
    def test_get_stats(self):
        """测试获取统计信息"""
        hybrid = HybridAutocomplete()
        hybrid.insert("hello")
        
        stats = hybrid.get_stats()
        
        self.assertEqual(stats['word_count'], 1)
        self.assertIn('trie_stats', stats)
        self.assertIn('ngram_stats', stats)
    
    def test_serialization(self):
        """测试序列化"""
        hybrid = HybridAutocomplete()
        hybrid.insert("hello", frequency=5)
        
        data = hybrid.to_dict()
        restored = HybridAutocomplete.from_dict(data)
        
        self.assertEqual(len(restored), 1)
        self.assertTrue(restored.contains("hello"))


class TestUtilityFunctions(unittest.TestCase):
    """工具函数测试"""
    
    def test_create_autocomplete(self):
        """测试创建自动补全器"""
        words = ["apple", "banana", "cherry"]
        ac = create_autocomplete(words)
        
        self.assertEqual(len(ac), 3)
        self.assertTrue(ac.contains("apple"))
    
    def test_create_autocomplete_ngram(self):
        """测试创建 N-gram 自动补全器"""
        words = ["apple", "banana", "cherry"]
        ac = create_autocomplete(words, use_ngram=True)
        
        self.assertEqual(len(ac), 3)
        self.assertIsInstance(ac, NGramAutocomplete)
    
    def test_levenshtein_distance_same(self):
        """测试相同字符串的编辑距离"""
        dist = levenshtein_distance("hello", "hello")
        self.assertEqual(dist, 0)
    
    def test_levenshtein_distance_different(self):
        """测试不同字符串的编辑距离"""
        dist = levenshtein_distance("kitten", "sitting")
        self.assertEqual(dist, 3)
    
    def test_levenshtein_distance_empty(self):
        """测试空字符串的编辑距离"""
        dist = levenshtein_distance("", "hello")
        self.assertEqual(dist, 5)
    
    def test_jaccard_similarity_same(self):
        """测试相同字符串的相似度"""
        sim = jaccard_similarity("hello", "hello")
        self.assertEqual(sim, 1.0)
    
    def test_jaccard_similarity_different(self):
        """测试不同字符串的相似度"""
        sim = jaccard_similarity("hello", "world")
        self.assertLess(sim, 1.0)
    
    def test_jaccard_similarity_empty(self):
        """测试空字符串的相似度"""
        sim = jaccard_similarity("", "")
        self.assertEqual(sim, 1.0)


class TestSuggestion(unittest.TestCase):
    """建议类测试"""
    
    def test_create_suggestion(self):
        """测试创建建议"""
        s = Suggestion(text="hello", score=0.9, frequency=5)
        
        self.assertEqual(s.text, "hello")
        self.assertEqual(s.score, 0.9)
        self.assertEqual(s.frequency, 5)
    
    def test_suggestion_with_metadata(self):
        """测试带元数据的建议"""
        s = Suggestion(
            text="hello",
            score=0.9,
            frequency=5,
            metadata={"lang": "en"}
        )
        
        self.assertEqual(s.metadata["lang"], "en")
    
    def test_suggestion_repr(self):
        """测试建议的字符串表示"""
        s = Suggestion(text="hello", score=0.9, frequency=5)
        repr_str = repr(s)
        
        self.assertIn("hello", repr_str)
        self.assertIn("0.90", repr_str)


class TestEdgeCases(unittest.TestCase):
    """边界情况测试"""
    
    def test_empty_trie(self):
        """测试空 Trie"""
        trie = TrieAutocomplete()
        
        self.assertEqual(len(trie), 0)
        self.assertEqual(trie.search("hello"), [])
        self.assertFalse(trie.contains("hello"))
    
    def test_single_word(self):
        """测试单个单词"""
        trie = TrieAutocomplete()
        trie.insert("hello")
        
        results = trie.search("he")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].text, "hello")
    
    def test_very_long_word(self):
        """测试很长的单词"""
        trie = TrieAutocomplete()
        long_word = "a" * 1000
        trie.insert(long_word)
        
        self.assertTrue(trie.contains(long_word))
        results = trie.search("a" * 100)
        self.assertEqual(len(results), 1)
    
    def test_unicode_words(self):
        """测试 Unicode 单词"""
        trie = TrieAutocomplete()
        words = ["你好", "世界", "日本語", "한국어", "العربية"]
        
        for word in words:
            trie.insert(word)
        
        self.assertEqual(len(trie), 5)
        for word in words:
            self.assertTrue(trie.contains(word))
    
    def test_special_characters(self):
        """测试特殊字符"""
        trie = TrieAutocomplete()
        words = ["hello-world", "test_case", "foo.bar", "a/b/c"]
        
        for word in words:
            trie.insert(word)
        
        self.assertEqual(len(trie), 4)
        for word in words:
            self.assertTrue(trie.contains(word))
    
    def test_numeric_words(self):
        """测试数字单词"""
        trie = TrieAutocomplete()
        words = ["123", "test123", "123test", "test-123"]
        
        for word in words:
            trie.insert(word)
        
        results = trie.search("123")
        self.assertGreater(len(results), 0)
    
    def test_concurrent_prefixes(self):
        """测试共享前缀的单词"""
        trie = TrieAutocomplete()
        words = ["a", "aa", "aaa", "aaaa"]
        
        for word in words:
            trie.insert(word)
        
        results = trie.search("a")
        self.assertEqual(len(results), 4)
        
        results = trie.search("aa")
        self.assertEqual(len(results), 3)
        
        results = trie.search("aaa")
        self.assertEqual(len(results), 2)
    
    def test_zero_frequency(self):
        """测试零频率"""
        trie = TrieAutocomplete()
        trie.insert("hello", frequency=0)
        
        info = trie.get_word_info("hello")
        self.assertEqual(info['frequency'], 0)
    
    def test_negative_frequency(self):
        """测试负频率（实际上会增加，因为累加）"""
        trie = TrieAutocomplete()
        trie.insert("hello", frequency=-1)
        
        info = trie.get_word_info("hello")
        self.assertEqual(info['frequency'], -1)


if __name__ == '__main__':
    unittest.main()