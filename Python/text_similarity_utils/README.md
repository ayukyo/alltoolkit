# Text Similarity Utils


AllToolkit - Text Similarity Utilities Module
==============================================
A comprehensive text similarity utility module with zero external dependencies.

Features:
    - Levenshtein distance (edit distance)
    - Damerau-Levenshtein distance (with transpositions)
    - Hamming distance (for equal-length strings)
    - Jaro similarity and Jaro-Winkler similarity
    - Cosine similarity (vector-based)
    - Jaccard similarity (set-based)
    - Dice coefficient (Sorensen-Dice)
    - N-gram similarity
    - Longest Common Subsequence (LCS)
    - Soundex and Metaphone phonetic algorithms
    - TF-IDF similarity (basic implementation)
    - Fuzzy matching utilities

Author: AllToolkit Contributors
License: MIT


## 功能

### 类

- **TFIDFCalculator**: TF-IDF (Term Frequency-Inverse Document Frequency) calculator
  方法: add_document, similarity, clear

### 函数

- **levenshtein_distance(s1, s2, case_sensitive**) - Calculate the Levenshtein (edit) distance between two strings.
- **levenshtein_ratio(s1, s2, case_sensitive**) - Calculate Levenshtein similarity ratio (0.0 to 1.0).
- **damerau_levenshtein_distance(s1, s2, case_sensitive**) - Calculate Damerau-Levenshtein distance (includes transpositions).
- **hamming_distance(s1, s2, case_sensitive**) - Calculate Hamming distance between two equal-length strings.
- **hamming_ratio(s1, s2, case_sensitive**) - Calculate Hamming similarity ratio.
- **jaro_similarity(s1, s2, case_sensitive**) - Calculate Jaro similarity between two strings.
- **jaro_winkler_similarity(s1, s2, p**, ...) - Calculate Jaro-Winkler similarity.
- **jaccard_similarity(s1, s2, ngram**, ...) - Calculate Jaccard similarity between two strings.
- **dice_coefficient(s1, s2, ngram**, ...) - Calculate Dice coefficient (Sorensen-Dice) between two strings.
- **overlap_coefficient(s1, s2, ngram**, ...) - Calculate Overlap coefficient (Szymkiewicz-Simpson).

... 共 29 个函数

## 使用示例

```python
from mod import levenshtein_distance

# 使用 levenshtein_distance
result = levenshtein_distance()
```

## 测试

运行测试：

```bash
python *_test.py
```

## 文件结构

```
{module_name}/
├── mod.py              # 主模块
├── *_test.py           # 测试文件
├── README.md           # 本文档
└── examples/           # 示例代码
    └── usage_examples.py
```

---

**Last updated**: 2026-04-28
