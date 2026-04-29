#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TF-IDF Utils 测试文件
====================
测试 TF-IDF 工具模块的所有功能。

运行方式: python tfidf_utils_test.py
"""

import sys
import os
import unittest
from math import log, sqrt

# Add module directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mod import (
    tokenize, tokenize_chinese, remove_stopwords,
    get_english_stopwords, get_chinese_stopwords,
    compute_tf, compute_tf_raw, compute_tf_log, compute_tf_augmented,
    compute_idf, compute_idf_smooth, compute_idf_probabilistic,
    compute_tfidf, compute_tfidf_vector, compute_tfidf_matrix,
    extract_keywords, extract_keywords_batch,
    cosine_similarity, euclidean_distance, jaccard_similarity,
    document_similarity, find_similar_documents,
    compute_bm25, search_bm25,
    TFIDFIndex, DocumentStats, TFIDFResult, SearchResult,
    quick_keywords, quick_similarity, build_index_from_texts
)


class TestTokenize(unittest.TestCase):
    """分词测试"""
    
    def test_tokenize_basic(self):
        """测试基本分词"""
        text = "Hello World"
        tokens = tokenize(text)
        self.assertEqual(tokens, ['hello', 'world'])
    
    def test_tokenize_lowercase(self):
        """测试大小写转换"""
        text = "Python IS Great"
        tokens = tokenize(text, lowercase=False)
        self.assertEqual(tokens, ['Python', 'IS', 'Great'])
    
    def test_tokenize_punctuation(self):
        """测试标点符号移除"""
        text = "Hello, World!"
        tokens = tokenize(text)
        self.assertEqual(tokens, ['hello', 'world'])
    
    def test_tokenize_min_length(self):
        """测试最小词长度"""
        text = "a an the cat dog"
        tokens = tokenize(text, min_length=3)
        self.assertEqual(tokens, ['the', 'cat', 'dog'])
    
    def test_tokenize_empty(self):
        """测试空文本"""
        self.assertEqual(tokenize(""), [])
    
    def test_tokenize_chinese(self):
        """测试中文分词"""
        text = "我爱编程"
        tokens = tokenize_chinese(text)
        self.assertEqual(tokens, ['我', '爱', '编', '程'])
    
    def test_tokenize_chinese_mixed(self):
        """测试中英混合"""
        text = "Python是好的"
        tokens = tokenize_chinese(text)
        self.assertIn('python', tokens)
        self.assertIn('是', tokens)


class TestStopwords(unittest.TestCase):
    """停用词测试"""
    
    def test_english_stopwords(self):
        """测试英文停用词"""
        stopwords = get_english_stopwords()
        self.assertIn('the', stopwords)
        self.assertIn('is', stopwords)
        self.assertNotIn('python', stopwords)
    
    def test_chinese_stopwords(self):
        """测试中文停用词"""
        stopwords = get_chinese_stopwords()
        self.assertIn('的', stopwords)
        self.assertIn('了', stopwords)
        self.assertNotIn('好', stopwords)
    
    def test_remove_stopwords(self):
        """测试移除停用词"""
        tokens = ['the', 'cat', 'is', 'on', 'the', 'mat']
        stopwords = {'the', 'is', 'on'}
        result = remove_stopwords(tokens, stopwords)
        self.assertEqual(result, ['cat', 'mat'])


class TestTF(unittest.TestCase):
    """词频测试"""
    
    def test_compute_tf_normalize(self):
        """测试归一化词频"""
        tokens = ['cat', 'cat', 'dog']
        tf = compute_tf(tokens)
        self.assertAlmostEqual(tf['cat'], 2/3)
        self.assertAlmostEqual(tf['dog'], 1/3)
    
    def test_compute_tf_raw(self):
        """测试原始词频"""
        tokens = ['cat', 'cat', 'dog']
        tf = compute_tf_raw(tokens)
        self.assertEqual(tf['cat'], 2)
        self.assertEqual(tf['dog'], 1)
    
    def test_compute_tf_log(self):
        """测试对数词频"""
        tokens = ['cat', 'cat', 'dog']
        tf = compute_tf_log(tokens, base=10)
        self.assertAlmostEqual(tf['cat'], 1 + log(2, 10))
        self.assertAlmostEqual(tf['dog'], 1.0)
    
    def test_compute_tf_augmented(self):
        """测试增强词频"""
        tokens = ['cat', 'cat', 'cat', 'dog']
        tf = compute_tf_augmented(tokens)
        self.assertEqual(tf['cat'], 1.0)  # 最大词频
        self.assertAlmostEqual(tf['dog'], 0.5 + 0.5 * (1/3))
    
    def test_compute_tf_empty(self):
        """测试空列表"""
        self.assertEqual(compute_tf([]), {})
        self.assertEqual(compute_tf_raw([]), {})


class TestIDF(unittest.TestCase):
    """逆文档频率测试"""
    
    def test_compute_idf(self):
        """测试 IDF 计算"""
        docs = [['cat', 'dog'], ['cat', 'bird'], ['dog', 'fish']]
        idf = compute_idf(docs, 'cat', smooth=True)
        # cat 出现在 2/3 文档
        self.assertAlmostEqual(idf, log(4/3, 10))
    
    def test_compute_idf_rare_term(self):
        """测试稀有词 IDF"""
        docs = [['cat', 'dog'], ['cat', 'bird'], ['dog', 'fish']]
        idf = compute_idf(docs, 'fish', smooth=True)
        # fish 只在 1/3 文档
        self.assertAlmostEqual(idf, log(4/2, 10))
    
    def test_compute_idf_smooth_dict(self):
        """测试平滑 IDF 字典"""
        docs = [['cat', 'dog'], ['cat', 'bird']]
        idf_dict = compute_idf_smooth(docs)
        self.assertIn('cat', idf_dict)
        self.assertIn('dog', idf_dict)
        self.assertIn('bird', idf_dict)
    
    def test_compute_idf_probabilistic(self):
        """测试概率 IDF"""
        docs = [['cat', 'dog'], ['cat', 'bird'], ['dog', 'fish']]
        idf_dict = compute_idf_probabilistic(docs)
        self.assertTrue(len(idf_dict) > 0)
    
    def test_compute_idf_empty(self):
        """测试空文档列表"""
        self.assertEqual(compute_idf([], 'term'), 0.0)
        self.assertEqual(compute_idf_smooth([]), {})


class TestTFIDF(unittest.TestCase):
    """TF-IDF 测试"""
    
    def test_compute_tfidf(self):
        """测试 TF-IDF 计算"""
        tokens = ['cat', 'cat', 'dog']
        idf_dict = {'cat': 0.5, 'dog': 1.0}
        tfidf = compute_tfidf(tokens, idf_dict)
        self.assertEqual(tfidf['cat'], 2 * 0.5)  # raw TF
        self.assertEqual(tfidf['dog'], 1 * 1.0)
    
    def test_compute_tfidf_normalize(self):
        """测试归一化 TF-IDF"""
        tokens = ['cat', 'cat', 'dog']
        idf_dict = {'cat': 0.5, 'dog': 1.0}
        tfidf = compute_tfidf(tokens, idf_dict, tf_method='normalize')
        self.assertAlmostEqual(tfidf['cat'], (2/3) * 0.5)
        self.assertAlmostEqual(tfidf['dog'], (1/3) * 1.0)
    
    def test_compute_tfidf_vector(self):
        """测试 TF-IDF 向量"""
        tokens = ['cat', 'dog']
        vocab = ['cat', 'dog', 'bird']
        idf_dict = {'cat': 0.5, 'dog': 1.0, 'bird': 0.3}
        vector = compute_tfidf_vector(tokens, vocab, idf_dict)
        self.assertEqual(len(vector), 3)
        self.assertEqual(vector[0], 0.5)  # cat
        self.assertEqual(vector[1], 1.0)  # dog
        self.assertEqual(vector[2], 0.0)  # bird (不在文档中)
    
    def test_compute_tfidf_matrix(self):
        """测试 TF-IDF 矩阵"""
        docs = [['cat', 'dog'], ['cat', 'bird']]
        vocab, matrix = compute_tfidf_matrix(docs)
        self.assertEqual(len(matrix), 2)
        self.assertEqual(len(matrix[0]), len(vocab))
    
    def test_compute_tfidf_empty(self):
        """测试空输入"""
        self.assertEqual(compute_tfidf([], {'cat': 0.5}), {})
        self.assertEqual(compute_tfidf_vector([], ['cat'], {'cat': 0.5}), [0.0])


class TestKeywords(unittest.TestCase):
    """关键词提取测试"""
    
    def test_extract_keywords(self):
        """测试关键词提取"""
        tokens = ['python', 'code', 'the', 'python', 'code', 'code']
        idf_dict = {'python': 2.0, 'code': 1.5, 'the': 0.1}
        keywords = extract_keywords(tokens, idf_dict, top_n=3)
        self.assertEqual(len(keywords), 3)
        self.assertEqual(keywords[0][0], 'code')  # TF=3, TF-IDF=4.5
        self.assertEqual(keywords[1][0], 'python')  # TF=2, TF-IDF=4
    
    def test_extract_keywords_min_tf(self):
        """测试最小词频过滤"""
        tokens = ['python', 'code', 'once']
        idf_dict = {'python': 2.0, 'code': 1.5, 'once': 1.0}
        keywords = extract_keywords(tokens, idf_dict, min_tf=2)
        self.assertEqual(len(keywords), 0)  # 所有词频都 < 2
    
    def test_extract_keywords_batch(self):
        """测试批量提取"""
        docs = [['python', 'code'], ['java', 'code']]
        results = extract_keywords_batch(docs, top_n=2)
        self.assertEqual(len(results), 2)
    
    def test_extract_keywords_empty(self):
        """测试空文档"""
        self.assertEqual(extract_keywords([], {'cat': 0.5}), [])


class TestSimilarity(unittest.TestCase):
    """相似度测试"""
    
    def test_cosine_similarity(self):
        """测试余弦相似度"""
        vec1 = [1, 0, 1]
        vec2 = [1, 0, 1]
        sim = cosine_similarity(vec1, vec2)
        self.assertAlmostEqual(sim, 1.0)
    
    def test_cosine_similarity_orthogonal(self):
        """测试正交向量"""
        vec1 = [1, 0]
        vec2 = [0, 1]
        sim = cosine_similarity(vec1, vec2)
        self.assertAlmostEqual(sim, 0.0)
    
    def test_cosine_similarity_partial(self):
        """测试部分相似"""
        vec1 = [1, 1, 0]
        vec2 = [1, 0, 0]
        sim = cosine_similarity(vec1, vec2)
        self.assertAlmostEqual(sim, 1/sqrt(2))
    
    def test_cosine_similarity_empty(self):
        """测试空向量"""
        self.assertEqual(cosine_similarity([], []), 0.0)
    
    def test_euclidean_distance(self):
        """测试欧几里得距离"""
        vec1 = [0, 0]
        vec2 = [3, 4]
        dist = euclidean_distance(vec1, vec2)
        self.assertAlmostEqual(dist, 5.0)
    
    def test_jaccard_similarity(self):
        """测试 Jaccard 相似度"""
        set1 = {'a', 'b', 'c'}
        set2 = {'b', 'c', 'd'}
        sim = jaccard_similarity(set1, set2)
        self.assertAlmostEqual(sim, 2/4)  # 交集2，并集4
    
    def test_jaccard_similarity_empty(self):
        """测试空集合"""
        self.assertAlmostEqual(jaccard_similarity(set(), set()), 1.0)
    
    def test_document_similarity_cosine(self):
        """测试文档相似度（余弦）"""
        doc1 = ['cat', 'dog']
        doc2 = ['cat', 'bird']
        sim = document_similarity(doc1, doc2, method='cosine')
        self.assertTrue(0 <= sim <= 1)
    
    def test_document_similarity_jaccard(self):
        """测试文档相似度（Jaccard）"""
        doc1 = ['cat', 'dog']
        doc2 = ['cat', 'bird']
        sim = document_similarity(doc1, doc2, method='jaccard')
        self.assertAlmostEqual(sim, 1/3)


class TestSearch(unittest.TestCase):
    """搜索测试"""
    
    def test_find_similar_documents(self):
        """测试查找相似文档"""
        query = ['cat']
        docs = [['cat', 'dog'], ['cat', 'bird'], ['dog', 'fish']]
        results = find_similar_documents(query, docs, top_n=2)
        self.assertEqual(len(results), 2)
        # 前两个应该都包含 'cat'
        self.assertTrue(all('cat' in r.matched_terms for r in results[:2]))
    
    def test_find_similar_documents_with_ids(self):
        """测试带 ID 的搜索"""
        query = ['python']
        docs = [['python', 'code'], ['java', 'code'], ['python', 'java']]
        doc_ids = ['doc1', 'doc2', 'doc3']
        results = find_similar_documents(query, docs, doc_ids=doc_ids, top_n=2)
        self.assertEqual(len(results), 2)
        self.assertIn(results[0].doc_id, ['doc1', 'doc3'])


class TestBM25(unittest.TestCase):
    """BM25 测试"""
    
    def test_compute_bm25(self):
        """测试 BM25 计算"""
        query = ['python']
        doc = ['python', 'code', 'python']
        lengths = [3, 3, 3, 3]  # 4 篇文档
        avg_len = 3.0
        score = compute_bm25(query, doc, lengths, avg_len)
        self.assertTrue(score > 0)
    
    def test_search_bm25(self):
        """测试 BM25 搜索"""
        query = ['python']
        docs = [
            ['python', 'code', 'programming'],
            ['java', 'code', 'programming'],
            ['python', 'python', 'data'],
        ]
        results = search_bm25(query, docs, top_n=2)
        self.assertEqual(len(results), 2)
        # 第三篇文档 'python' 出现两次，应该得分更高
        self.assertEqual(results[0].doc_id, 'doc_2')
    
    def test_bm25_no_match(self):
        """测试无匹配"""
        query = ['ruby']
        docs = [['python', 'code'], ['java', 'code']]
        results = search_bm25(query, docs, top_n=2)
        self.assertEqual(len(results), 2)
        self.assertTrue(all(r.score == 0 for r in results))


class TestTFIDFIndex(unittest.TestCase):
    """TF-IDF 索引类测试"""
    
    def test_add_document(self):
        """测试添加文档"""
        index = TFIDFIndex()
        index.add_document('doc1', ['python', 'code'])
        self.assertEqual(len(index.documents), 1)
        self.assertIn('doc1', index.documents)
    
    def test_add_document_text(self):
        """测试添加文本文档"""
        index = TFIDFIndex()
        index.add_document_text('doc1', 'Python code')
        self.assertEqual(len(index.documents), 1)
    
    def test_remove_document(self):
        """测试移除文档"""
        index = TFIDFIndex()
        index.add_document('doc1', ['python', 'code'])
        index.add_document('doc2', ['java', 'code'])
        result = index.remove_document('doc1')
        self.assertTrue(result)
        self.assertEqual(len(index.documents), 1)
    
    def test_remove_nonexistent(self):
        """测试移除不存在文档"""
        index = TFIDFIndex()
        self.assertFalse(index.remove_document('doc_x'))
    
    def test_search(self):
        """测试搜索"""
        index = TFIDFIndex()
        index.add_document('doc1', ['python', 'code', 'programming'])
        index.add_document('doc2', ['java', 'code', 'programming'])
        index.add_document('doc3', ['python', 'data', 'science'])
        
        results = index.search(['python'], top_n=2)
        self.assertEqual(len(results), 2)
        self.assertIn(results[0].doc_id, ['doc1', 'doc3'])
    
    def test_search_text(self):
        """测试文本搜索"""
        index = TFIDFIndex()
        index.add_document_text('doc1', 'Python programming')
        index.add_document_text('doc2', 'Java programming')
        
        results = index.search_text('Python', top_n=2)
        self.assertEqual(len(results), 2)
    
    def test_search_bm25(self):
        """测试 BM25 搜索"""
        index = TFIDFIndex()
        index.add_document('doc1', ['python', 'python', 'code'])
        index.add_document('doc2', ['python', 'code'])
        
        results = index.search_bm25(['python'], top_n=2)
        self.assertEqual(len(results), 2)
    
    def test_get_keywords(self):
        """测试获取关键词"""
        index = TFIDFIndex()
        index.add_document('doc1', ['python', 'code', 'python', 'programming'])
        index.add_document('doc2', ['java', 'code', 'java'])
        
        keywords = index.get_keywords('doc1', top_n=3)
        self.assertEqual(len(keywords), 3)
    
    def test_get_document_vector(self):
        """测试获取文档向量"""
        index = TFIDFIndex()
        index.add_document('doc1', ['python', 'code'])
        index.add_document('doc2', ['java', 'code'])
        
        vector = index.get_document_vector('doc1')
        self.assertTrue(len(vector) > 0)
    
    def test_get_similar_documents(self):
        """测试获取相似文档"""
        index = TFIDFIndex()
        index.add_document('doc1', ['python', 'code', 'programming'])
        index.add_document('doc2', ['python', 'code', 'data'])
        index.add_document('doc3', ['java', 'programming'])
        
        similar = index.get_similar_documents('doc1', top_n=2)
        self.assertEqual(len(similar), 2)
    
    def test_get_stats(self):
        """测试统计信息"""
        index = TFIDFIndex()
        index.add_document('doc1', ['python', 'code'])
        index.add_document('doc2', ['java', 'code', 'programming'])
        
        stats = index.get_stats()
        self.assertEqual(stats['document_count'], 2)
        self.assertEqual(stats['total_terms'], 5)
    
    def test_custom_stopwords(self):
        """测试自定义停用词"""
        index = TFIDFIndex(stopwords={'code', 'programming'})
        index.add_document('doc1', ['python', 'code', 'programming'])
        
        # code 和 programming 应被过滤
        self.assertNotIn('code', index.documents['doc1'])
        self.assertNotIn('programming', index.documents['doc1'])


class TestQuickFunctions(unittest.TestCase):
    """便捷函数测试"""
    
    def test_quick_keywords(self):
        """测试快速关键词"""
        text = "Python is great for coding Python is amazing"
        keywords = quick_keywords(text, top_n=3)
        self.assertEqual(len(keywords), 3)
        # 'python' 出现两次，应该在首位
        self.assertEqual(keywords[0][0], 'python')
    
    def test_quick_keywords_chinese(self):
        """测试中文快速关键词"""
        text = "编程很好 编程有用 学习编程"
        stopwords = get_chinese_stopwords()
        keywords = quick_keywords(text, top_n=3, stopwords=stopwords)
        self.assertEqual(len(keywords), 3)
    
    def test_quick_similarity(self):
        """测试快速相似度"""
        sim = quick_similarity("cat dog", "cat bird")
        self.assertTrue(0 <= sim <= 1)
    
    def test_build_index_from_texts(self):
        """测试从文本构建索引"""
        texts = {
            'doc1': 'Python code',
            'doc2': 'Java code',
        }
        index = build_index_from_texts(texts)
        self.assertEqual(len(index.documents), 2)


class TestDocumentStats(unittest.TestCase):
    """文档统计类测试"""
    
    def test_document_stats_get_tf(self):
        """测试获取归一化词频"""
        stats = DocumentStats(
            doc_id='test',
            term_frequencies={'cat': 2, 'dog': 1},
            total_terms=3,
            unique_terms=2
        )
        self.assertAlmostEqual(stats.get_tf('cat'), 2/3)
        self.assertAlmostEqual(stats.get_tf('dog'), 1/3)
    
    def test_document_stats_empty(self):
        """测试空文档统计"""
        stats = DocumentStats(
            doc_id='empty',
            term_frequencies={},
            total_terms=0,
            unique_terms=0
        )
        self.assertEqual(stats.get_tf('any'), 0.0)


class TestTFIDFResult(unittest.TestCase):
    """TF-IDF 结果类测试"""
    
    def test_tfidf_result_to_dict(self):
        """测试转换为字典"""
        result = TFIDFResult(
            term='python',
            tf=0.5,
            idf=2.0,
            tfidf=1.0,
            doc_count=5
        )
        d = result.to_dict()
        self.assertEqual(d['term'], 'python')
        self.assertEqual(d['tfidf'], 1.0)


class TestSearchResult(unittest.TestCase):
    """搜索结果类测试"""
    
    def test_search_result_to_dict(self):
        """测试转换为字典"""
        result = SearchResult(
            doc_id='doc1',
            score=0.95,
            matched_terms={'python', 'code'}
        )
        d = result.to_dict()
        self.assertEqual(d['doc_id'], 'doc1')
        self.assertEqual(d['score'], 0.95)
        self.assertIn('python', d['matched_terms'])


class TestEdgeCases(unittest.TestCase):
    """边界值测试"""
    
    def test_empty_documents(self):
        """测试空文档列表"""
        vocab, matrix = compute_tfidf_matrix([])
        self.assertEqual(vocab, [])
        self.assertEqual(matrix, [])
    
    def test_single_term_document(self):
        """测试单词文档"""
        tokens = ['python']
        tf = compute_tf(tokens)
        self.assertEqual(tf['python'], 1.0)
    
    def test_all_stopwords(self):
        """测试全部是停用词"""
        tokens = ['the', 'is', 'a']
        stopwords = get_english_stopwords()
        result = remove_stopwords(tokens, stopwords)
        self.assertEqual(result, [])
    
    def test_long_document(self):
        """测试长文档"""
        tokens = ['word'] * 1000 + ['rare']
        tf = compute_tf(tokens)
        self.assertAlmostEqual(tf['word'], 1000/1001)
        self.assertAlmostEqual(tf['rare'], 1/1001)
    
    def test_unicode_terms(self):
        """测试 Unicode 词"""
        tokens = ['编程', '代码', '编程']
        tf = compute_tf(tokens)
        self.assertEqual(tf['编程'], 2/3)
    
    def test_zero_vector_similarity(self):
        """测试零向量"""
        self.assertEqual(cosine_similarity([0, 0], [0, 0]), 0.0)
    
    def test_different_length_vectors(self):
        """测试不同长度向量"""
        vec1 = [1, 2, 3]
        vec2 = [1, 2]
        sim = cosine_similarity(vec1, vec2)
        # 应截断到相同长度
        self.assertTrue(sim > 0)


if __name__ == "__main__":
    unittest.main(verbosity=2)