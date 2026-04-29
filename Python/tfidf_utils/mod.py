#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TF-IDF Utils - TF-IDF 文本分析工具模块
======================================
提供 TF-IDF（词频-逆文档频率）文本分析功能。
零外部依赖，仅使用 Python 标准库。

主要功能:
- TF（词频）计算
- IDF（逆文档频率）计算
- TF-IDF 向量计算
- 关键词提取
- 文档相似度计算
- 文档聚类辅助
- BM25 排序算法
- 文本预处理工具

作者: AllToolkit
日期: 2026-04-29
"""

from typing import List, Dict, Tuple, Optional, Set, Union, Callable
from dataclasses import dataclass, field
from math import log, sqrt
from collections import Counter
import re


@dataclass
class DocumentStats:
    """文档统计信息"""
    doc_id: str                    # 文档 ID
    term_frequencies: Dict[str, int]  # 词频统计
    total_terms: int               # 总词数
    unique_terms: int              # 唯一词数
    
    def get_tf(self, term: str) -> float:
        """获取词的归一化词频"""
        if self.total_terms == 0:
            return 0.0
        return self.term_frequencies.get(term, 0) / self.total_terms


@dataclass
class TFIDFResult:
    """TF-IDF 计算结果"""
    term: str                      # 词
    tf: float                      # 词频
    idf: float                     # 逆文档频率
    tfidf: float                   # TF-IDF 值
    doc_count: int                 # 包含该词的文档数
    
    def to_dict(self) -> Dict:
        """转换为字典"""
        return {
            'term': self.term,
            'tf': self.tf,
            'idf': self.idf,
            'tfidf': self.tfidf,
            'doc_count': self.doc_count
        }


@dataclass
class SearchResult:
    """搜索结果"""
    doc_id: str                    # 文档 ID
    score: float                   # 相关性得分
    matched_terms: Set[str]        # 匹配的词
    
    def to_dict(self) -> Dict:
        """转换为字典"""
        return {
            'doc_id': self.doc_id,
            'score': self.score,
            'matched_terms': list(self.matched_terms)
        }


# ==================== 文本预处理工具 ====================

def tokenize(text: str, 
             lowercase: bool = True,
             remove_punctuation: bool = True,
             min_length: int = 1,
             max_length: int = 50,
             split_pattern: str = r'\s+') -> List[str]:
    """
    将文本分词
    
    Args:
        text: 输入文本
        lowercase: 是否转换为小写
        remove_punctuation: 是否移除标点符号
        min_length: 最小词长度
        max_length: 最大词长度
        split_pattern: 分词正则表达式
    
    Returns:
        词列表
    
    Examples:
        >>> tokenize("Hello World!")
        ['hello', 'world']
        >>> tokenize("Python  is  great", lowercase=False)
        ['Python', 'is', 'great']
    """
    if lowercase:
        text = text.lower()
    
    if remove_punctuation:
        # 保留字母、数字、中文字符
        text = re.sub(r'[^\w\u4e00-\u9fff\s]', ' ', text)
    
    # 分词
    tokens = re.split(split_pattern, text)
    
    # 过滤
    tokens = [t.strip() for t in tokens if t.strip()]
    tokens = [t for t in tokens if min_length <= len(t) <= max_length]
    
    return tokens


def tokenize_chinese(text: str) -> List[str]:
    """
    简单中文分词（基于字符切分，适用于 TF-IDF）
    
    对于更精确的中文分词，建议使用专业分词库。
    这里提供一个简单的基于字符的切分方案。
    
    Args:
        text: 中文文本
    
    Returns:
        词列表
    
    Examples:
        >>> tokenize_chinese("我爱编程")
        ['我', '爱', '编', '程']
    """
    # 简单字符切分（实际应用应使用专业分词库）
    result = []
    current_word = ""
    
    for char in text:
        if '\u4e00' <= char <= '\u9fff':
            # 中文字符
            if current_word:
                result.append(current_word)
                current_word = ""
            result.append(char)
        elif char.isalnum():
            current_word += char.lower()
        else:
            if current_word:
                result.append(current_word)
                current_word = ""
    
    if current_word:
        result.append(current_word)
    
    return [t for t in result if t.strip()]


def remove_stopwords(tokens: List[str], 
                     stopwords: Set[str],
                     min_length: int = 2) -> List[str]:
    """
    移除停用词
    
    Args:
        tokens: 词列表
        stopwords: 停用词集合
        min_length: 最小词长度
    
    Returns:
        过滤后的词列表
    
    Examples:
        >>> remove_stopwords(['the', 'cat', 'is', 'on'], {'the', 'is', 'on'})
        ['cat']
    """
    return [t for t in tokens if t not in stopwords and len(t) >= min_length]


def get_english_stopwords() -> Set[str]:
    """
    获取常见英文停用词
    
    Returns:
        停用词集合
    
    Examples:
        >>> 'the' in get_english_stopwords()
        True
    """
    return {
        'a', 'an', 'the', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for',
        'of', 'with', 'by', 'from', 'as', 'is', 'was', 'are', 'were', 'been',
        'be', 'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would',
        'could', 'should', 'may', 'might', 'must', 'shall', 'can', 'need',
        'it', 'its', 'this', 'that', 'these', 'those', 'i', 'you', 'he',
        'she', 'we', 'they', 'what', 'which', 'who', 'whom', 'when', 'where',
        'why', 'how', 'all', 'each', 'every', 'both', 'few', 'more', 'most',
        'other', 'some', 'such', 'no', 'nor', 'not', 'only', 'own', 'same',
        'so', 'than', 'too', 'very', 'just', 'also', 'now', 'here', 'there',
        'then', 'once', 'if', 'because', 'until', 'while', 'about', 'against',
        'between', 'into', 'through', 'during', 'before', 'after', 'above',
        'below', 'up', 'down', 'out', 'off', 'over', 'under', 'again',
        'further', 'any', 'am'
    }


def get_chinese_stopwords() -> Set[str]:
    """
    获取常见中文停用词
    
    Returns:
        停用词集合
    
    Examples:
        >>> '的' in get_chinese_stopwords()
        True
    """
    return {
        '的', '了', '和', '是', '就', '都', '而', '及', '与', '着',
        '或', '一个', '没有', '我们', '你们', '他们', '她们', '它们',
        '这个', '那个', '这些', '那些', '之', '在', '有', '上', '中',
        '大', '为', '也', '要', '会', '着', '不', '但', '可以', '以',
        '这', '那', '他', '她', '它', '我', '你', '啊', '吧', '呢',
        '吗', '呀', '哦', '哈', '嗯', '很', '多', '最', '更', '很',
        '能', '把', '让', '被', '给', '到', '从', '来', '去', '说',
        '看', '想', '做', '用', '对', '把', '跟', '比', '等', '但'
    }


# ==================== TF 计算 ====================

def compute_tf(tokens: List[str], 
               normalize: bool = True) -> Dict[str, float]:
    """
    计算词频 (TF - Term Frequency)
    
    Args:
        tokens: 词列表
        normalize: 是否归一化（除以总词数）
    
    Returns:
        词频字典 {term: frequency}
    
    Examples:
        >>> compute_tf(['cat', 'cat', 'dog'])
        {'cat': 0.666..., 'dog': 0.333...}
        >>> compute_tf(['cat', 'cat', 'dog'], normalize=False)
        {'cat': 2, 'dog': 1}
    """
    if not tokens:
        return {}
    
    counter = Counter(tokens)
    
    if normalize:
        total = len(tokens)
        return {term: count / total for term, count in counter.items()}
    else:
        return dict(counter)


def compute_tf_raw(tokens: List[str]) -> Dict[str, int]:
    """
    计算原始词频计数
    
    Args:
        tokens: 词列表
    
    Returns:
        词频计数字典 {term: count}
    
    Examples:
        >>> compute_tf_raw(['cat', 'cat', 'dog'])
        {'cat': 2, 'dog': 1}
    """
    return dict(Counter(tokens))


def compute_tf_log(tokens: List[str], base: float = 10) -> Dict[str, float]:
    """
    计算对数词频 (Logarithmic TF)
    
    TF_log = 1 + log(tf) if tf > 0 else 0
    
    Args:
        tokens: 词列表
        base: 对数底数
    
    Returns:
        对数词频字典
    
    Examples:
        >>> compute_tf_log(['cat', 'cat', 'dog'])
        {'cat': 1.301..., 'dog': 1.0}
    """
    counter = Counter(tokens)
    result = {}
    
    for term, count in counter.items():
        if count > 0:
            result[term] = 1 + log(count, base)
        else:
            result[term] = 0
    
    return result


def compute_tf_augmented(tokens: List[str]) -> Dict[str, float]:
    """
    计算增强词频 (Augmented TF)
    
    TF_aug = 0.5 + 0.5 * (tf / max_tf)
    
    防止长文档 bias。
    
    Args:
        tokens: 词列表
    
    Returns:
        增强词频字典
    
    Examples:
        >>> compute_tf_augmented(['cat', 'cat', 'cat', 'dog'])
        {'cat': 1.0, 'dog': 0.666...}
    """
    counter = Counter(tokens)
    if not counter:
        return {}
    
    max_tf = max(counter.values())
    result = {}
    
    for term, count in counter.items():
        result[term] = 0.5 + 0.5 * (count / max_tf)
    
    return result


# ==================== IDF 计算 ====================

def compute_idf(documents: List[List[str]],
                term: str,
                smooth: bool = True,
                base: float = 10) -> float:
    """
    计算逆文档频率 (IDF - Inverse Document Frequency)
    
    IDF = log(N / df) 或 log((N + 1) / (df + 1)) (smooth)
    
    Args:
        documents: 文档列表（每个文档是词列表）
        term: 目标词
        smooth: 是否平滑（防止除零）
        base: 对数底数
    
    Returns:
        IDF 值
    
    Examples:
        >>> docs = [['cat', 'dog'], ['cat', 'bird'], ['dog', 'fish']]
        >>> compute_idf(docs, 'cat')
        0.176...
    """
    n = len(documents)
    if n == 0:
        return 0.0
    
    # 计算文档频率 (df)
    df = sum(1 for doc in documents if term in doc)
    
    if smooth:
        return log((n + 1) / (df + 1), base)
    else:
        if df == 0:
            return 0.0
        return log(n / df, base)


def compute_idf_smooth(documents: List[List[str]],
                       base: float = 10) -> Dict[str, float]:
    """
    计算所有词的平滑 IDF
    
    Args:
        documents: 文档列表（每个文档是词列表）
        base: 对数底数
    
    Returns:
        IDF 字典 {term: idf}
    
    Examples:
        >>> docs = [['cat', 'dog'], ['cat', 'bird']]
        >>> idf = compute_idf_smooth(docs)
        >>> 'cat' in idf
        True
    """
    n = len(documents)
    if n == 0:
        return {}
    
    # 收集所有词
    all_terms = set()
    for doc in documents:
        all_terms.update(doc)
    
    # 计算每个词的文档频率
    df = Counter()
    for doc in documents:
        unique_terms = set(doc)
        for term in unique_terms:
            df[term] += 1
    
    # 计算 IDF
    result = {}
    for term in all_terms:
        result[term] = log((n + 1) / (df[term] + 1), base)
    
    return result


def compute_idf_probabilistic(documents: List[List[str]],
                               base: float = 10) -> Dict[str, float]:
    """
    计算概率 IDF
    
    IDF_prob = log((N - df) / df)
    
    基于 Robertson 的概率模型。
    
    Args:
        documents: 文档列表
        base: 对数底数
    
    Returns:
        概率 IDF 字典
    
    Examples:
        >>> docs = [['cat', 'dog'], ['cat', 'bird'], ['dog', 'fish']]
        >>> idf = compute_idf_probabilistic(docs)
        >>> len(idf) > 0
        True
    """
    n = len(documents)
    if n == 0:
        return {}
    
    # 收集所有词并计算 df
    all_terms = set()
    for doc in documents:
        all_terms.update(doc)
    
    df = Counter()
    for doc in documents:
        unique_terms = set(doc)
        for term in unique_terms:
            df[term] += 1
    
    # 计算概率 IDF
    result = {}
    for term in all_terms:
        d = df[term]
        if d < n:  # 防止 log(负数)
            result[term] = log((n - d) / d, base) if d > 0 else log(n, base)
        else:
            result[term] = 0.0
    
    return result


# ==================== TF-IDF 计算 ====================

def compute_tfidf(tokens: List[str],
                  idf_dict: Dict[str, float],
                  tf_method: str = 'raw') -> Dict[str, float]:
    """
    计算 TF-IDF 值
    
    Args:
        tokens: 词列表
        idf_dict: IDF 字典
        tf_method: TF 计算方法 ('raw', 'normalize', 'log', 'augmented')
    
    Returns:
        TF-IDF 字典 {term: tfidf}
    
    Examples:
        >>> idf = {'cat': 0.5, 'dog': 1.0}
        >>> compute_tfidf(['cat', 'cat', 'dog'], idf)
        {'cat': 1.0, 'dog': 1.0}
    """
    if not tokens:
        return {}
    
    # 计算 TF
    if tf_method == 'normalize':
        tf = compute_tf(tokens, normalize=True)
    elif tf_method == 'log':
        tf = compute_tf_log(tokens)
    elif tf_method == 'augmented':
        tf = compute_tf_augmented(tokens)
    else:  # raw
        tf = compute_tf(tokens, normalize=False)
    
    # 计算 TF-IDF
    result = {}
    for term, tf_value in tf.items():
        idf_value = idf_dict.get(term, 0.0)
        result[term] = tf_value * idf_value
    
    return result


def compute_tfidf_vector(tokens: List[str],
                         vocabulary: List[str],
                         idf_dict: Dict[str, float]) -> List[float]:
    """
    计算 TF-IDF 向量（按词汇表顺序）
    
    Args:
        tokens: 词列表
        vocabulary: 词汇表
        idf_dict: IDF 字典
    
    Returns:
        TF-IDF 向量
    
    Examples:
        >>> vocab = ['cat', 'dog', 'bird']
        >>> idf = {'cat': 0.5, 'dog': 1.0, 'bird': 0.3}
        >>> compute_tfidf_vector(['cat', 'dog'], vocab, idf)
        [0.5, 1.0, 0.0]
    """
    tfidf = compute_tfidf(tokens, idf_dict)
    return [tfidf.get(term, 0.0) for term in vocabulary]


def compute_tfidf_matrix(documents: List[List[str]],
                          tf_method: str = 'normalize',
                          idf_method: str = 'smooth') -> Tuple[List[str], List[List[float]]]:
    """
    计算 TF-IDF 矩阵
    
    Args:
        documents: 文档列表
        tf_method: TF 计算方法
        idf_method: IDF 计算方法
    
    Returns:
        (词汇表, TF-IDF 矩阵)
    
    Examples:
        >>> docs = [['cat', 'dog'], ['cat', 'bird']]
        >>> vocab, matrix = compute_tfidf_matrix(docs)
        >>> len(vocab) == 3
        True
    """
    if not documents:
        return [], []
    
    # 构建词汇表
    vocabulary = sorted(set(term for doc in documents for term in doc))
    
    # 计算 IDF
    if idf_method == 'probabilistic':
        idf_dict = compute_idf_probabilistic(documents)
    else:  # smooth
        idf_dict = compute_idf_smooth(documents)
    
    # 计算每篇文档的 TF-IDF 向量
    matrix = []
    for doc in documents:
        vector = compute_tfidf_vector(doc, vocabulary, idf_dict)
        matrix.append(vector)
    
    return vocabulary, matrix


# ==================== 关键词提取 ====================

def extract_keywords(tokens: List[str],
                     idf_dict: Dict[str, float],
                     top_n: int = 10,
                     min_tf: int = 1,
                     min_idf: float = 0.0) -> List[Tuple[str, float]]:
    """
    提取关键词
    
    Args:
        tokens: 词列表
        idf_dict: IDF 字典
        top_n: 返回前 N 个关键词
        min_tf: 最小词频
        min_idf: 最小 IDF
    
    Returns:
        [(词, TF-IDF 值), ...] 按值排序
    
    Examples:
        >>> idf = {'python': 2.0, 'code': 1.5, 'the': 0.1}
        >>> extract_keywords(['python', 'code', 'the', 'python'], idf, top_n=2)
        [('python', 4.0), ('code', 1.5)]
    """
    if not tokens:
        return []
    
    # 计算 TF
    tf = compute_tf_raw(tokens)
    
    # 计算 TF-IDF 并过滤
    tfidf = {}
    for term, tf_value in tf.items():
        if tf_value < min_tf:
            continue
        idf_value = idf_dict.get(term, 0.0)
        if idf_value < min_idf:
            continue
        tfidf[term] = tf_value * idf_value
    
    # 排序
    sorted_tfidf = sorted(tfidf.items(), key=lambda x: x[1], reverse=True)
    return sorted_tfidf[:top_n]


def extract_keywords_batch(documents: List[List[str]],
                           top_n: int = 10,
                           idf_dict: Optional[Dict[str, float]] = None) -> List[List[Tuple[str, float]]]:
    """
    批量提取关键词
    
    Args:
        documents: 文档列表
        top_n: 每篇文档返回前 N 个关键词
        idf_dict: 预计算的 IDF 字典（可选）
    
    Returns:
        每篇文档的关键词列表
    
    Examples:
        >>> docs = [['python', 'code'], ['java', 'code']]
        >>> results = extract_keywords_batch(docs, top_n=2)
        >>> len(results) == 2
        True
    """
    if not documents:
        return []
    
    # 如果未提供 IDF，计算
    if idf_dict is None:
        idf_dict = compute_idf_smooth(documents)
    
    results = []
    for doc in documents:
        keywords = extract_keywords(doc, idf_dict, top_n=top_n)
        results.append(keywords)
    
    return results


# ==================== 文档相似度 ====================

def cosine_similarity(vec1: List[float], vec2: List[float]) -> float:
    """
    计算余弦相似度
    
    Args:
        vec1: 向量 1
        vec2: 向量 2
    
    Returns:
        余弦相似度 (0-1)
    
    Examples:
        >>> cosine_similarity([1, 0, 1], [1, 0, 1])
        1.0
        >>> cosine_similarity([1, 0], [0, 1])
        0.0
    """
    if len(vec1) != len(vec2):
        min_len = min(len(vec1), len(vec2))
        vec1 = vec1[:min_len]
        vec2 = vec2[:min_len]
    
    if not vec1 or not vec2:
        return 0.0
    
    # 计算点积
    dot_product = sum(a * b for a, b in zip(vec1, vec2))
    
    # 计算模长
    norm1 = sqrt(sum(a * a for a in vec1))
    norm2 = sqrt(sum(b * b for b in vec2))
    
    if norm1 == 0 or norm2 == 0:
        return 0.0
    
    return dot_product / (norm1 * norm2)


def euclidean_distance(vec1: List[float], vec2: List[float]) -> float:
    """
    计算欧几里得距离
    
    Args:
        vec1: 向量 1
        vec2: 向量 2
    
    Returns:
        欧几里得距离
    
    Examples:
        >>> euclidean_distance([0, 0], [3, 4])
        5.0
    """
    if len(vec1) != len(vec2):
        min_len = min(len(vec1), len(vec2))
        vec1 = vec1[:min_len]
        vec2 = vec2[:min_len]
    
    return sqrt(sum((a - b) ** 2 for a, b in zip(vec1, vec2)))


def jaccard_similarity(set1: Set[str], set2: Set[str]) -> float:
    """
    计算 Jaccard 相似度
    
    Args:
        set1: 集合 1
        set2: 集合 2
    
    Returns:
        Jaccard 相似度 (0-1)
    
    Examples:
        >>> jaccard_similarity({'a', 'b'}, {'b', 'c'})
        0.333...
    """
    if not set1 and not set2:
        return 1.0
    
    intersection = len(set1 & set2)
    union = len(set1 | set2)
    
    if union == 0:
        return 0.0
    
    return intersection / union


def document_similarity(doc1: List[str],
                        doc2: List[str],
                        idf_dict: Optional[Dict[str, float]] = None,
                        method: str = 'cosine') -> float:
    """
    计算文档相似度
    
    Args:
        doc1: 文档 1（词列表）
        doc2: 文档 2（词列表）
        idf_dict: IDF 字典（可选）
        method: 相似度方法 ('cosine', 'jaccard', 'euclidean')
    
    Returns:
        相似度值
    
    Examples:
        >>> document_similarity(['cat', 'dog'], ['cat', 'bird'], method='jaccard')
        0.333...
    """
    if method == 'jaccard':
        return jaccard_similarity(set(doc1), set(doc2))
    
    # 需要计算 TF-IDF 向量
    if idf_dict is None:
        idf_dict = compute_idf_smooth([doc1, doc2])
    
    vocabulary = sorted(set(doc1) | set(doc2))
    vec1 = compute_tfidf_vector(doc1, vocabulary, idf_dict)
    vec2 = compute_tfidf_vector(doc2, vocabulary, idf_dict)
    
    if method == 'cosine':
        return cosine_similarity(vec1, vec2)
    elif method == 'euclidean':
        # 转换为相似度 (0-1)
        dist = euclidean_distance(vec1, vec2)
        max_dist = sqrt(len(vocabulary))  # 最大可能距离
        return 1 - (dist / max_dist) if max_dist > 0 else 1.0
    else:
        raise ValueError(f"Unknown method: {method}")


def find_similar_documents(query: List[str],
                           documents: List[List[str]],
                           doc_ids: Optional[List[str]] = None,
                           top_n: int = 5,
                           method: str = 'cosine') -> List[SearchResult]:
    """
    查找相似文档
    
    Args:
        query: 查询文档（词列表）
        documents: 文档列表
        doc_ids: 文档 ID 列表
        top_n: 返回前 N 个
        method: 相似度方法
    
    Returns:
        搜索结果列表，按相似度排序
    
    Examples:
        >>> docs = [['cat', 'dog'], ['cat', 'bird'], ['dog', 'fish']]
        >>> results = find_similar_documents(['cat'], docs, top_n=2)
        >>> len(results) == 2
        True
    """
    if not documents:
        return []
    
    if doc_ids is None:
        doc_ids = [f"doc_{i}" for i in range(len(documents))]
    
    # 预计算 IDF
    all_docs = [query] + documents
    idf_dict = compute_idf_smooth(all_docs)
    
    # 计算相似度
    results = []
    for i, doc in enumerate(documents):
        sim = document_similarity(query, doc, idf_dict, method=method)
        matched = set(query) & set(doc)
        results.append(SearchResult(
            doc_id=doc_ids[i],
            score=sim,
            matched_terms=matched
        ))
    
    # 排序
    results.sort(key=lambda x: x.score, reverse=True)
    return results[:top_n]


# ==================== BM25 排序 ====================

def compute_bm25(query: List[str],
                 doc_tokens: List[str],
                 doc_lengths: List[int],
                 avg_doc_length: float,
                 k1: float = 1.5,
                 b: float = 0.75,
                 idf_dict: Optional[Dict[str, float]] = None) -> float:
    """
    计算 BM25 相关性得分
    
    BM25 = IDF(qi) * (f(qi, D) * (k1 + 1)) / (f(qi, D) + k1 * (1 - b + b * |D| / avgdl))
    
    Args:
        query: 查询词列表
        doc_tokens: 文档词列表
        doc_lengths: 所有文档长度列表
        avg_doc_length: 平均文档长度
        k1: 词频饱和参数
        b: 文档长度归一化参数
        idf_dict: IDF 字典
    
    Returns:
        BM25 得分
    
    Examples:
        >>> docs = [['cat', 'dog'], ['cat', 'bird']]
        >>> lengths = [2, 2]
        >>> compute_bm25(['cat'], ['cat', 'dog'], lengths, 2.0)
        0.5...
    """
    if not query or not doc_tokens:
        return 0.0
    
    doc_length = len(doc_tokens)
    doc_tf = Counter(doc_tokens)
    
    # 计算查询词的 IDF
    if idf_dict is None:
        # 简化的 IDF 计算
        n = len(doc_lengths) + 1  # +1 for query
        query_df = Counter()
        # 假设所有词至少出现一次
        for q in set(query):
            if q in doc_tokens:
                query_df[q] = 1
        idf_dict = {q: log((n - query_df.get(q, 0) + 0.5) / 
                          (query_df.get(q, 0) + 0.5) + 1) for q in query}
    
    score = 0.0
    for q in query:
        tf = doc_tf.get(q, 0)
        if tf == 0:
            continue
        
        idf = idf_dict.get(q, 0.0)
        
        # BM25 公式
        numerator = tf * (k1 + 1)
        denominator = tf + k1 * (1 - b + b * doc_length / avg_doc_length)
        score += idf * numerator / denominator
    
    return score


def search_bm25(query: List[str],
                documents: List[List[str]],
                doc_ids: Optional[List[str]] = None,
                k1: float = 1.5,
                b: float = 0.75,
                top_n: int = 10) -> List[SearchResult]:
    """
    BM25 搜索
    
    Args:
        query: 查询词列表
        documents: 文档列表
        doc_ids: 文档 ID 列表
        k1: 词频饱和参数
        b: 文档长度归一化参数
        top_n: 返回前 N 个结果
    
    Returns:
        搜索结果列表
    
    Examples:
        >>> docs = [['python', 'code'], ['java', 'code'], ['python', 'java']]
        >>> results = search_bm25(['python'], docs, top_n=2)
        >>> len(results) == 2
        True
    """
    if not documents:
        return []
    
    if doc_ids is None:
        doc_ids = [f"doc_{i}" for i in range(len(documents))]
    
    # 计算文档长度
    doc_lengths = [len(doc) for doc in documents]
    avg_doc_length = sum(doc_lengths) / len(doc_lengths) if doc_lengths else 1
    
    # 计算 IDF
    all_docs = documents + [query]
    idf_dict = compute_idf_smooth(all_docs)
    
    # 计算每篇文档的 BM25 得分
    results = []
    for i, doc in enumerate(documents):
        score = compute_bm25(
            query, doc, doc_lengths, avg_doc_length,
            k1=k1, b=b, idf_dict=idf_dict
        )
        matched = set(query) & set(doc)
        results.append(SearchResult(
            doc_id=doc_ids[i],
            score=score,
            matched_terms=matched
        ))
    
    # 排序
    results.sort(key=lambda x: x.score, reverse=True)
    return results[:top_n]


# ==================== TF-IDF 索引 ====================

class TFIDFIndex:
    """
    TF-IDF 索引类
    
    用于构建和管理文档索引，支持高效搜索。
    
    示例:
        >>> index = TFIDFIndex()
        >>> index.add_document('doc1', ['python', 'code'])
        >>> index.add_document('doc2', ['java', 'code'])
        >>> results = index.search(['python'], top_n=2)
    """
    
    def __init__(self, 
                 stopwords: Optional[Set[str]] = None,
                 tokenizer: Optional[Callable[[str], List[str]]] = None):
        """
        初始化 TF-IDF 索引
        
        Args:
            stopwords: 停用词集合
            tokenizer: 自定义分词函数
        """
        self.documents: Dict[str, List[str]] = {}
        self.doc_ids: List[str] = []
        self.vocabulary: Set[str] = set()
        self.idf_dict: Dict[str, float] = {}
        self.stopwords = stopwords or get_english_stopwords()
        self.tokenizer = tokenizer or tokenize
        self._needs_update = True
    
    def add_document(self, doc_id: str, tokens: List[str]) -> None:
        """
        添加文档
        
        Args:
            doc_id: 文档 ID
            tokens: 词列表
        """
        # 过滤停用词
        filtered = [t for t in tokens if t not in self.stopwords]
        self.documents[doc_id] = filtered
        self.doc_ids.append(doc_id)
        self.vocabulary.update(filtered)
        self._needs_update = True
    
    def add_document_text(self, doc_id: str, text: str) -> None:
        """
        添加文档（文本形式）
        
        Args:
            doc_id: 文档 ID
            text: 文档文本
        """
        tokens = self.tokenizer(text)
        self.add_document(doc_id, tokens)
    
    def remove_document(self, doc_id: str) -> bool:
        """
        移除文档
        
        Args:
            doc_id: 文档 ID
        
        Returns:
            是否成功移除
        """
        if doc_id not in self.documents:
            return False
        
        del self.documents[doc_id]
        self.doc_ids.remove(doc_id)
        self._needs_update = True
        
        # 重建词汇表
        self.vocabulary = set()
        for tokens in self.documents.values():
            self.vocabulary.update(tokens)
        
        return True
    
    def update_index(self) -> None:
        """更新索引（重新计算 IDF）"""
        if not self.documents:
            self.idf_dict = {}
            self._needs_update = False
            return
        
        docs = list(self.documents.values())
        self.idf_dict = compute_idf_smooth(docs)
        self._needs_update = False
    
    def search(self, query: List[str], 
               top_n: int = 10,
               method: str = 'cosine') -> List[SearchResult]:
        """
        搜索文档
        
        Args:
            query: 查询词列表
            top_n: 返回前 N 个结果
            method: 相似度方法
        
        Returns:
            搜索结果列表
        """
        if self._needs_update:
            self.update_index()
        
        if not self.documents:
            return []
        
        # 过滤查询中的停用词
        query = [t for t in query if t not in self.stopwords]
        
        documents = list(self.documents.values())
        return find_similar_documents(
            query, documents, self.doc_ids, top_n=top_n, method=method
        )
    
    def search_text(self, text: str, 
                    top_n: int = 10,
                    method: str = 'cosine') -> List[SearchResult]:
        """
        搜索文档（文本形式）
        
        Args:
            text: 查询文本
            top_n: 返回前 N 个结果
            method: 相似度方法
        
        Returns:
            搜索结果列表
        """
        query = self.tokenizer(text)
        return self.search(query, top_n=top_n, method=method)
    
    def search_bm25(self, query: List[str],
                    top_n: int = 10,
                    k1: float = 1.5,
                    b: float = 0.75) -> List[SearchResult]:
        """
        BM25 搜索
        
        Args:
            query: 查询词列表
            top_n: 返回前 N 个结果
            k1: 词频饱和参数
            b: 文档长度归一化参数
        
        Returns:
            搜索结果列表
        """
        if self._needs_update:
            self.update_index()
        
        if not self.documents:
            return []
        
        # 过滤查询中的停用词
        query = [t for t in query if t not in self.stopwords]
        
        documents = list(self.documents.values())
        return search_bm25(query, documents, self.doc_ids, k1=k1, b=b, top_n=top_n)
    
    def get_keywords(self, doc_id: str, top_n: int = 10) -> List[Tuple[str, float]]:
        """
        获取文档关键词
        
        Args:
            doc_id: 文档 ID
            top_n: 返回前 N 个关键词
        
        Returns:
            [(词, TF-IDF 值), ...]
        """
        if self._needs_update:
            self.update_index()
        
        if doc_id not in self.documents:
            return []
        
        tokens = self.documents[doc_id]
        return extract_keywords(tokens, self.idf_dict, top_n=top_n)
    
    def get_document_vector(self, doc_id: str) -> List[float]:
        """
        获取文档的 TF-IDF 向量
        
        Args:
            doc_id: 文档 ID
        
        Returns:
            TF-IDF 向量
        """
        if self._needs_update:
            self.update_index()
        
        if doc_id not in self.documents:
            return []
        
        vocab_list = sorted(self.vocabulary)
        tokens = self.documents[doc_id]
        return compute_tfidf_vector(tokens, vocab_list, self.idf_dict)
    
    def get_similar_documents(self, doc_id: str, top_n: int = 5) -> List[SearchResult]:
        """
        查找相似文档
        
        Args:
            doc_id: 文档 ID
            top_n: 返回前 N 个结果
        
        Returns:
            相似文档列表
        """
        if doc_id not in self.documents:
            return []
        
        query = self.documents[doc_id]
        
        # 排除自己
        other_docs = []
        other_ids = []
        for did, tokens in self.documents.items():
            if did != doc_id:
                other_docs.append(tokens)
                other_ids.append(did)
        
        if not other_docs:
            return []
        
        if self._needs_update:
            self.update_index()
        
        all_docs = [query] + other_docs
        idf_dict = compute_idf_smooth(all_docs)
        
        results = []
        for i, doc in enumerate(other_docs):
            sim = document_similarity(query, doc, idf_dict)
            matched = set(query) & set(doc)
            results.append(SearchResult(
                doc_id=other_ids[i],
                score=sim,
                matched_terms=matched
            ))
        
        results.sort(key=lambda x: x.score, reverse=True)
        return results[:top_n]
    
    def get_stats(self) -> Dict:
        """
        获取索引统计信息
        
        Returns:
            统计信息字典
        """
        total_terms = sum(len(tokens) for tokens in self.documents.values())
        avg_doc_length = total_terms / len(self.documents) if self.documents else 0
        
        return {
            'document_count': len(self.documents),
            'vocabulary_size': len(self.vocabulary),
            'total_terms': total_terms,
            'average_doc_length': avg_doc_length,
            'stopwords_count': len(self.stopwords)
        }


# ==================== 便捷函数 ====================

def quick_keywords(text: str, 
                   top_n: int = 10,
                   stopwords: Optional[Set[str]] = None) -> List[Tuple[str, float]]:
    """
    快速提取文本关键词
    
    Args:
        text: 输入文本
        top_n: 返回前 N 个关键词
        stopwords: 停用词集合
    
    Returns:
        [(词, 得分), ...]
    
    Examples:
        >>> quick_keywords("python is great for coding python", top_n=2)
        [('python', ...), ('coding', ...)]
    """
    tokens = tokenize(text)
    
    if stopwords is None:
        stopwords = get_english_stopwords()
    
    tokens = [t for t in tokens if t not in stopwords]
    
    if not tokens:
        return []
    
    # 使用增强 TF（不需要 IDF，单文档）
    tf = compute_tf_augmented(tokens)
    
    sorted_terms = sorted(tf.items(), key=lambda x: x[1], reverse=True)
    return sorted_terms[:top_n]


def quick_similarity(text1: str, text2: str, method: str = 'cosine') -> float:
    """
    快速计算文本相似度
    
    Args:
        text1: 文本 1
        text2: 文本 2
        method: 相似度方法
    
    Returns:
        相似度值
    
    Examples:
        >>> quick_similarity("cat dog", "cat bird")
        0.333...
    """
    tokens1 = tokenize(text1)
    tokens2 = tokenize(text2)
    
    stopwords = get_english_stopwords()
    tokens1 = [t for t in tokens1 if t not in stopwords]
    tokens2 = [t for t in tokens2 if t not in stopwords]
    
    return document_similarity(tokens1, tokens2, method=method)


def build_index_from_texts(texts: Dict[str, str],
                           stopwords: Optional[Set[str]] = None) -> TFIDFIndex:
    """
    从文本字典构建索引
    
    Args:
        texts: {doc_id: text} 字典
        stopwords: 停用词集合
    
    Returns:
        TF-IDF 索引
    
    Examples:
        >>> texts = {'doc1': 'python code', 'doc2': 'java code'}
        >>> index = build_index_from_texts(texts)
        >>> len(index.documents) == 2
        True
    """
    index = TFIDFIndex(stopwords=stopwords)
    for doc_id, text in texts.items():
        index.add_document_text(doc_id, text)
    index.update_index()
    return index


if __name__ == "__main__":
    # 简单演示
    print("TF-IDF Utils 演示")
    print("=" * 50)
    
    # 示例文档
    documents = [
        ['python', 'is', 'a', 'programming', 'language'],
        ['python', 'is', 'great', 'for', 'data', 'science'],
        ['java', 'is', 'also', 'a', 'programming', 'language'],
        ['machine', 'learning', 'uses', 'python', 'and', 'data'],
    ]
    
    print("\n1. TF-IDF 计算:")
    idf = compute_idf_smooth(documents)
    print(f"   IDF 字典: {dict(list(idf.items())[:5])}")
    
    print("\n2. 关键词提取:")
    keywords = extract_keywords(documents[1], idf, top_n=3)
    print(f"   文档 2 关键词: {keywords}")
    
    print("\n3. 文档相似度:")
    sim = document_similarity(documents[0], documents[1])
    print(f"   文档 0 和 1 的相似度: {sim:.4f}")
    
    print("\n4. BM25 搜索:")
    results = search_bm25(['python', 'data'], documents, top_n=2)
    for r in results:
        print(f"   {r.doc_id}: {r.score:.4f}")
    
    print("\n5. 索引类演示:")
    index = TFIDFIndex()
    index.add_document('doc1', ['python', 'code', 'programming'])
    index.add_document('doc2', ['java', 'code', 'programming'])
    index.add_document('doc3', ['python', 'data', 'science'])
    
    results = index.search(['python'], top_n=2)
    print(f"   搜索 'python': {[r.doc_id for r in results]}")
    
    stats = index.get_stats()
    print(f"   索引统计: {stats}")
    
    print("\n" + "=" * 50)
    print("演示完成")