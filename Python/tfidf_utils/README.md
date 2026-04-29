# tfidf_utils - TF-IDF 文本分析工具

[![Test Coverage](https://img.shields.io/badge/coverage-100%25-brightgreen)](./tfidf_utils_test.py)

零依赖的 TF-IDF（词频-逆文档频率）文本分析工具。

## 特性

- **TF 计算**: 多种词频计算方式（原始、归一化、对数、增强）
- **IDF 计算**: 多种逆文档频率计算方式（标准、平滑、概率）
- **关键词提取**: 从文档中提取重要关键词
- **相似度计算**: 余弦相似度、欧氏距离、Jaccard 相似度
- **BM25 排序**: 文档搜索排序算法
- **文档索引**: 高效的 TF-IDF 索引构建
- **中文支持**: 中文分词和停用词处理
- **零依赖**: 纯 Python 实现

## 安装

```python
from tfidf_utils import (
    tokenize,
    compute_tf,
    compute_idf,
    compute_tfidf,
    extract_keywords,
    cosine_similarity,
    TFIDFIndex,
    quick_keywords
)
```

## 快速开始

### 基础 TF-IDF 计算

```python
from tfidf_utils import compute_tfidf

# 计算单个词的 TF-IDF
tfidf = compute_tfidf("python", tf=0.05, doc_count=10, total_docs=100)
print(f"TF-IDF: {tfidf}")
```

### 关键词提取

```python
from tfidf_utils import extract_keywords, quick_keywords

# 文档集合
documents = [
    "Python is a popular programming language",
    "Machine learning uses Python extensively",
    "Natural language processing with Python"
]

# 提取关键词
keywords = extract_keywords(documents[0], documents, top_n=5)
print(keywords)  # [('python', 0.42), ('language', 0.28), ...]

# 快速提取
keywords = quick_keywords(documents[0], documents, top_n=3)
```

### 文档相似度

```python
from tfidf_utils import cosine_similarity, document_similarity

doc1 = "Python programming language"
doc2 = "Python is great for coding"

# 计算相似度
similarity = cosine_similarity(doc1, doc2)
print(f"相似度: {similarity}")

# 使用 TF-IDF 向量计算
similarity = document_similarity(doc1, doc2, corpus=[doc1, doc2])
```

### 构建 TF-IDF 索引

```python
from tfidf_utils import TFIDFIndex, build_index_from_texts

# 从文本构建索引
documents = {
    "doc1": "Python programming tutorial",
    "doc2": "Machine learning basics",
    "doc3": "Natural language processing"
}

index = build_index_from_texts(documents)

# 搜索相关文档
results = index.search("Python tutorial", top_k=2)
for result in results:
    print(f"{result.doc_id}: {result.score}")
```

### BM25 搜索

```python
from tfidf_utils import search_bm25

# 文档集合
documents = [
    "Python programming guide",
    "Learn Python from basics",
    "Advanced Python techniques"
]

# BM25 搜索
results = search_bm25("Python basics", documents, top_k=2)
for doc_id, score in results:
    print(f"文档 {doc_id}: 得分 {score}")
```

### 中文文本处理

```python
from tfidf_utils import tokenize_chinese, get_chinese_stopwords

text = "自然语言处理是人工智能的重要分支"

# 中文分词
tokens = tokenize_chinese(text)
print(tokens)

# 获取中文停用词
stopwords = get_chinese_stopwords()
```

## API 参考

### 文本预处理

| 函数 | 说明 |
|-----|------|
| `tokenize(text, ...)` | 英文分词 |
| `tokenize_chinese(text)` | 中文分词 |
| `remove_stopwords(tokens, stopwords)` | 移除停用词 |
| `get_english_stopwords()` | 获取英文停用词列表 |
| `get_chinese_stopwords()` | 获取中文停用词列表 |

### TF-IDF 计算

| 函数 | 说明 |
|-----|------|
| `compute_tf(term_freq, total_terms)` | 计算归一化词频 |
| `compute_tf_raw(term_freq)` | 计算原始词频 |
| `compute_tf_log(term_freq)` | 计算对数词频 |
| `compute_idf(doc_count, total_docs)` | 计算逆文档频率 |
| `compute_idf_smooth(doc_count, total_docs)` | 计算平滑 IDF |
| `compute_tfidf(term, tf, doc_count, total_docs)` | 计算 TF-IDF |
| `compute_tfidf_vector(document, corpus)` | 计算 TF-IDF 向量 |
| `compute_tfidf_matrix(corpus)` | 计算 TF-IDF 矩阵 |

### 关键词提取

| 函数 | 说明 |
|-----|------|
| `extract_keywords(document, corpus, top_n)` | 提取关键词 |
| `extract_keywords_batch documents, top_n)` | 批量提取关键词 |
| `quick_keywords(document, corpus, top_n)` | 快速关键词提取 |

### 相似度计算

| 函数 | 说明 |
|-----|------|
| `cosine_similarity(vec1, vec2)` | 余弦相似度 |
| `euclidean_distance(vec1, vec2)` | 欧氏距离 |
| `jaccard_similarity(set1, set2)` | Jaccard 相似度 |
| `document_similarity(doc1, doc2, corpus)` | 文档相似度 |
| `find_similar_documents(query, corpus, top_k)` | 查找相似文档 |

### BM25 相关

| 函数 | 说明 |
|-----|------|
| `compute_bm25(term, doc, corpus, k1, b)` | 计算 BM25 得分 |
| `search_bm25(query, documents, top_k)` | BM25 搜索 |

### TFIDFIndex 类

```python
TFIDFIndex()
index.add_document(doc_id, document)
index.search(query, top_k)
index.get_keywords(doc_id, top_n)
```

## 理论背景

### TF-IDF 公式

- **TF**: 词频 = 词出现次数 / 文档总词数
- **IDF**: 逆文档频率 = log(总文档数 / 包含该词的文档数)
- **TF-IDF**: TF × IDF

### BM25 公式

```
BM25(D, Q) = Σ IDF(qi) × (f(qi, D) × (k1 + 1)) / (f(qi, D) + k1 × (1 - b + b × |D|/avgdl))
```

其中：
- `k1`: 通常 1.2-2.0
- `b`: 通常 0.75

## 测试

```bash
python -m pytest tfidf_utils_test.py -v
```

## 许可证

MIT License