#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TF-IDF Utils 使用示例
====================
展示 TF-IDF 工具模块的各种用法。

运行方式: python examples/usage_examples.py
"""

import sys
import os

# Add module directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from mod import (
    tokenize, tokenize_chinese, remove_stopwords,
    get_english_stopwords, get_chinese_stopwords,
    compute_tf, compute_tf_raw, compute_tf_log, compute_tf_augmented,
    compute_idf, compute_idf_smooth, compute_idf_probabilistic,
    compute_tfidf, compute_tfidf_vector, compute_tfidf_matrix,
    extract_keywords, extract_keywords_batch,
    cosine_similarity, jaccard_similarity,
    document_similarity, find_similar_documents,
    compute_bm25, search_bm25,
    TFIDFIndex,
    quick_keywords, quick_similarity, build_index_from_texts
)


def example_1_tokenize():
    """示例 1: 文本分词"""
    print("\n" + "=" * 50)
    print("示例 1: 文本分词")
    print("=" * 50)
    
    # 基本分词
    text = "Python is a great programming language!"
    tokens = tokenize(text)
    print(f"原文: {text}")
    print(f"分词结果: {tokens}")
    
    # 保留大小写
    tokens_upper = tokenize(text, lowercase=False)
    print(f"保留大小写: {tokens_upper}")
    
    # 设置最小词长
    tokens_long = tokenize("a an the cat dog bird", min_length=3)
    print(f"最小长度 3: {tokens_long}")
    
    # 中文分词（简单字符切分）
    chinese_text = "我爱编程Python"
    chinese_tokens = tokenize_chinese(chinese_text)
    print(f"中文 '{chinese_text}' → {chinese_tokens}")
    
    # 移除停用词
    tokens_with_stopwords = ['the', 'cat', 'is', 'on', 'the', 'mat']
    stopwords = get_english_stopwords()
    filtered = remove_stopwords(tokens_with_stopwords, stopwords)
    print(f"移除停用词: {tokens_with_stopwords} → {filtered}")


def example_2_tf():
    """示例 2: 词频计算"""
    print("\n" + "=" * 50)
    print("示例 2: 词频计算")
    print("=" * 50)
    
    tokens = ['python', 'python', 'code', 'data', 'python', 'code']
    
    # 原始词频
    tf_raw = compute_tf_raw(tokens)
    print(f"原始词频: {tf_raw}")
    
    # 归一化词频
    tf_normalized = compute_tf(tokens, normalize=True)
    print(f"归一化词频: {tf_normalized}")
    
    # 对数词频
    tf_log = compute_tf_log(tokens)
    print(f"对数词频: {tf_log}")
    
    # 增强词频
    tf_augmented = compute_tf_augmented(tokens)
    print(f"增强词频: {tf_augmented}")


def example_3_idf():
    """示例 3: 逆文档频率"""
    print("\n" + "=" * 50)
    print("示例 3: 逆文档频率计算")
    print("=" * 50)
    
    # 示例文档集
    documents = [
        ['python', 'is', 'a', 'programming', 'language'],
        ['python', 'is', 'great', 'for', 'data', 'science'],
        ['java', 'is', 'also', 'a', 'programming', 'language'],
        ['machine', 'learning', 'uses', 'python', 'and', 'data'],
    ]
    
    print("文档集:")
    for i, doc in enumerate(documents):
        print(f"  文档 {i}: {' '.join(doc)}")
    
    # 计算单个词的 IDF
    idf_python = compute_idf(documents, 'python')
    idf_java = compute_idf(documents, 'java')
    idf_machine = compute_idf(documents, 'machine')
    
    print(f"\n单词 IDF:")
    print(f"  'python' IDF: {idf_python:.4f} (出现在 3/4 文档)")
    print(f"  'java' IDF: {idf_java:.4f} (出现在 1/4 文档)")
    print(f"  'machine' IDF: {idf_machine:.4f} (出现在 1/4 文档)")
    
    # 计算所有词的 IDF
    idf_dict = compute_idf_smooth(documents)
    print(f"\n完整 IDF 字典 (前 5 个):")
    for term, idf in sorted(idf_dict.items(), key=lambda x: x[1], reverse=True)[:5]:
        print(f"  '{term}': {idf:.4f}")
    
    # 概率 IDF
    idf_prob = compute_idf_probabilistic(documents)
    print(f"\n概率 IDF (前 3 个):")
    for term, idf in sorted(idf_prob.items(), key=lambda x: x[1], reverse=True)[:3]:
        print(f"  '{term}': {idf:.4f}")


def example_4_tfidf():
    """示例 4: TF-IDF 计算"""
    print("\n" + "=" * 50)
    print("示例 4: TF-IDF 计算")
    print("=" * 50)
    
    documents = [
        ['python', 'code', 'programming'],
        ['python', 'data', 'science'],
        ['java', 'code', 'programming'],
    ]
    
    # 计算 IDF
    idf_dict = compute_idf_smooth(documents)
    
    # 计算文档 0 的 TF-IDF
    doc0 = documents[0]
    tfidf = compute_tfidf(doc0, idf_dict)
    print(f"文档 0: {' '.join(doc0)}")
    print(f"TF-IDF: {tfidf}")
    
    # TF-IDF 向量
    vocabulary = sorted(set(term for doc in documents for term in doc))
    vector = compute_tfidf_vector(doc0, vocabulary, idf_dict)
    print(f"\n词汇表: {vocabulary}")
    print(f"TF-IDF 向量: {vector}")
    
    # TF-IDF 矩阵
    vocab, matrix = compute_tfidf_matrix(documents)
    print(f"\nTF-IDF 矩阵:")
    print(f"  词汇表: {vocab}")
    for i, row in enumerate(matrix):
        print(f"  文档 {i}: {row}")


def example_5_keywords():
    """示例 5: 关键词提取"""
    print("\n" + "=" * 50)
    print("示例 5: 关键词提取")
    print("=" * 50)
    
    documents = [
        ['python', 'is', 'a', 'popular', 'programming', 'language', 'for', 'data', 'science'],
        ['machine', 'learning', 'algorithms', 'often', 'use', 'python', 'for', 'implementation'],
        ['data', 'analysis', 'and', 'visualization', 'are', 'key', 'python', 'use', 'cases'],
    ]
    
    print("文档集:")
    for i, doc in enumerate(documents):
        print(f"  文档 {i}: {' '.join(doc)}")
    
    # 计算 IDF
    idf_dict = compute_idf_smooth(documents)
    
    # 提取每篇文档的关键词
    print(f"\n关键词提取:")
    for i, doc in enumerate(documents):
        keywords = extract_keywords(doc, idf_dict, top_n=5)
        print(f"  文档 {i}: {keywords}")
    
    # 批量提取
    print(f"\n批量提取:")
    keywords_batch = extract_keywords_batch(documents, top_n=3)
    for i, kw in enumerate(keywords_batch):
        print(f"  文档 {i}: {kw}")
    
    # 快速关键词提取
    text = "Python programming is essential for machine learning and data science applications"
    quick_kw = quick_keywords(text, top_n=5)
    print(f"\n快速提取 '{text[:30]}...':")
    print(f"  {quick_kw}")


def example_6_similarity():
    """示例 6: 文档相似度"""
    print("\n" + "=" * 50)
    print("示例 6: 文档相似度计算")
    print("=" * 50)
    
    documents = [
        ['python', 'code', 'programming', 'development'],
        ['python', 'data', 'science', 'analysis'],
        ['java', 'code', 'programming', 'backend'],
        ['cooking', 'recipe', 'food', 'kitchen'],
    ]
    
    print("文档集:")
    for i, doc in enumerate(documents):
        print(f"  文档 {i}: {' '.join(doc)}")
    
    # 计算文档相似度
    print(f"\n相似度矩阵 (余弦):")
    idf_dict = compute_idf_smooth(documents)
    
    for i in range(len(documents)):
        for j in range(i + 1, len(documents)):
            sim = document_similarity(documents[i], documents[j], idf_dict)
            print(f"  文档 {i} vs {j}: {sim:.4f}")
    
    # Jaccard 相似度
    print(f"\nJaccard 相似度:")
    for i in range(min(3, len(documents))):
        for j in range(i + 1, min(3, len(documents))):
            sim = jaccard_similarity(set(documents[i]), set(documents[j]))
            print(f"  文档 {i} vs {j}: {sim:.4f}")
    
    # 快速相似度
    text1 = "Python machine learning data science"
    text2 = "Java backend development programming"
    sim = quick_similarity(text1, text2)
    print(f"\n快速相似度:")
    print(f"  '{text1}' vs '{text2}' = {sim:.4f}")


def example_7_search():
    """示例 7: 文档搜索"""
    print("\n" + "=" * 50)
    print("示例 7: 文档搜索")
    print("=" * 50)
    
    documents = [
        ['python', 'web', 'development', 'django', 'flask'],
        ['python', 'data', 'science', 'pandas', 'numpy'],
        ['java', 'spring', 'boot', 'backend', 'api'],
        ['javascript', 'react', 'frontend', 'web', 'ui'],
        ['python', 'machine', 'learning', 'tensorflow', 'scikit'],
    ]
    
    doc_ids = ['python_web', 'python_data', 'java_backend', 'js_frontend', 'python_ml']
    
    print("文档集:")
    for i, (id_, doc) in enumerate(zip(doc_ids, documents)):
        print(f"  {id_}: {' '.join(doc)}")
    
    # 搜索相似文档
    query = ['python', 'web', 'application']
    print(f"\n查询: {' '.join(query)}")
    
    results = find_similar_documents(query, documents, doc_ids, top_n=3)
    print(f"搜索结果:")
    for r in results:
        print(f"  {r.doc_id}: 得分={r.score:.4f}, 匹配={r.matched_terms}")
    
    # BM25 搜索
    print(f"\nBM25 搜索:")
    bm25_results = search_bm25(query, documents, doc_ids, top_n=3)
    for r in bm25_results:
        print(f"  {r.doc_id}: 得分={r.score:.4f}, 匹配={r.matched_terms}")


def example_8_bm25():
    """示例 8: BM25 排序"""
    print("\n" + "=" * 50)
    print("示例 8: BM25 排序算法")
    print("=" * 50)
    
    documents = [
        ['python', 'python', 'python', 'programming', 'code'],
        ['python', 'programming', 'language'],
        ['java', 'programming', 'language', 'backend'],
        ['python', 'code', 'tutorial'],
    ]
    
    print("文档集:")
    for i, doc in enumerate(documents):
        print(f"  文档 {i}: {' '.join(doc)} (长度={len(doc)})")
    
    query = ['python', 'programming']
    print(f"\n查询: {' '.join(query)}")
    
    # BM25 搜索（调整参数）
    print(f"\nBM25 结果 (k1=1.5, b=0.75):")
    results = search_bm25(query, documents, top_n=4, k1=1.5, b=0.75)
    for r in results:
        print(f"  {r.doc_id}: 得分={r.score:.4f}")
    
    # 更高的 k1 值会更重视词频
    print(f"\nBM25 结果 (k1=2.5, b=0.75):")
    results2 = search_bm25(query, documents, top_n=4, k1=2.5, b=0.75)
    for r in results2:
        print(f"  {r.doc_id}: 得分={r.score:.4f}")
    
    # 更低的 b 值会减少文档长度的影响
    print(f"\nBM25 结果 (k1=1.5, b=0.25):")
    results3 = search_bm25(query, documents, top_n=4, k1=1.5, b=0.25)
    for r in results3:
        print(f"  {r.doc_id}: 得分={r.score:.4f}")


def example_9_index():
    """示例 9: TF-IDF 索引"""
    print("\n" + "=" * 50)
    print("示例 9: TF-IDF 索引使用")
    print("=" * 50)
    
    # 创建索引
    index = TFIDFIndex()
    
    # 添加文档
    texts = {
        'doc1': "Python is a versatile programming language",
        'doc2': "Machine learning uses Python extensively",
        'doc3': "Java is popular for enterprise applications",
        'doc4': "Data science requires Python skills",
    }
    
    for doc_id, text in texts.items():
        index.add_document_text(doc_id, text)
    
    print("文档集:")
    for doc_id, text in texts.items():
        print(f"  {doc_id}: {text}")
    
    # 搜索
    query = "Python programming"
    print(f"\n搜索 '{query}':")
    results = index.search_text(query, top_n=3)
    for r in results:
        print(f"  {r.doc_id}: 得分={r.score:.4f}")
    
    # BM25 搜索
    print(f"\nBM25 搜索 '{query}':")
    bm25_results = index.search_bm25(['python', 'programming'], top_n=3)
    for r in bm25_results:
        print(f"  {r.doc_id}: 得分={r.score:.4f}")
    
    # 获取关键词
    print(f"\n文档 'doc1' 关键词:")
    keywords = index.get_keywords('doc1', top_n=5)
    for kw, score in keywords:
        print(f"  '{kw}': {score:.4f}")
    
    # 获取相似文档
    print(f"\n与 'doc1' 相似的文档:")
    similar = index.get_similar_documents('doc1', top_n=3)
    for r in similar:
        print(f"  {r.doc_id}: 得分={r.score:.4f}")
    
    # 统计信息
    stats = index.get_stats()
    print(f"\n索引统计:")
    print(f"  文档数: {stats['document_count']}")
    print(f"  词汇表大小: {stats['vocabulary_size']}")
    print(f"  平均文档长度: {stats['average_doc_length']:.2f}")


def example_10_build_index():
    """示例 10: 快速构建索引"""
    print("\n" + "=" * 50)
    print("示例 10: 快速构建索引")
    print("=" * 50)
    
    # 从文本字典快速构建
    articles = {
        'article1': "Python web development with Django framework",
        'article2': "Data analysis using Python pandas numpy",
        'article3': "Machine learning algorithms in Python",
        'article4': "Java enterprise development Spring Boot",
    }
    
    print("文章集:")
    for id_, text in articles.items():
        print(f"  {id_}: {text}")
    
    # 构建索引
    index = build_index_from_texts(articles)
    
    # 搜索
    query = "Python data analysis"
    print(f"\n搜索 '{query}':")
    results = index.search_text(query, top_n=3)
    for r in results:
        print(f"  {r.doc_id}: 得分={r.score:.4f}, 匹配词={list(r.matched_terms)}")
    
    # 添加新文档
    index.add_document_text('article5', "Python machine learning tensorflow")
    print(f"\n添加新文档后搜索:")
    results = index.search_text(query, top_n=4)
    for r in results:
        print(f"  {r.doc_id}: 得分={r.score:.4f}")


def example_11_chinese():
    """示例 11: 中文文本处理"""
    print("\n" + "=" * 50)
    print("示例 11: 中文文本处理")
    print("=" * 50)
    
    # 中文文档
    texts = {
        'doc1': "Python是一种流行的编程语言",
        'doc2': "机器学习使用Python进行数据分析",
        'doc3': "Java在企业级应用中很流行",
        'doc4': "数据科学需要Python技能",
    }
    
    print("中文文档集:")
    for doc_id, text in texts.items():
        print(f"  {doc_id}: {text}")
    
    # 创建索引（使用中文停用词）
    index = TFIDFIndex(stopwords=get_chinese_stopwords())
    
    for doc_id, text in texts.items():
        # 中文分词
        tokens = tokenize_chinese(text)
        index.add_document(doc_id, tokens)
    
    # 搜索
    query_tokens = tokenize_chinese("Python数据分析")
    print(f"\n查询: {' '.join(query_tokens)}")
    
    results = index.search(query_tokens, top_n=3)
    for r in results:
        print(f"  {r.doc_id}: 得分={r.score:.4f}")


def main():
    """运行所有示例"""
    print("\n" + "=" * 60)
    print("TF-IDF Utils 使用示例集合")
    print("=" * 60)
    
    example_1_tokenize()
    example_2_tf()
    example_3_idf()
    example_4_tfidf()
    example_5_keywords()
    example_6_similarity()
    example_7_search()
    example_8_bm25()
    example_9_index()
    example_10_build_index()
    example_11_chinese()
    
    print("\n" + "=" * 60)
    print("所有示例完成!")
    print("=" * 60)


if __name__ == "__main__":
    main()