# Fuzzy Search Utils


AllToolkit - Python Fuzzy Search Utilities

A zero-dependency, production-ready fuzzy string matching utility module.
Supports multiple algorithms: Levenshtein distance, n-gram similarity, soundex,
metaphone, Jaro-Winkler distance, and more.

Author: AllToolkit
License: MIT


## 功能

### 类

- **FuzzyMatch**: Represents a fuzzy match result
- **FuzzyMatcher**: A configurable fuzzy matcher for repeated searches
  方法: add_candidates, add_candidate, remove_candidate, search, find ... (8 个方法)

### 函数

- **levenshtein_distance(s1, s2**) - Calculate the Levenshtein (edit) distance between two strings.
- **levenshtein_ratio(s1, s2**) - Calculate the similarity ratio based on Levenshtein distance.
- **damerau_levenshtein_distance(s1, s2**) - Calculate the Damerau-Levenshtein distance.
- **hamming_distance(s1, s2**) - Calculate the Hamming distance between two strings of equal length.
- **jaro_distance(s1, s2**) - Calculate the Jaro distance between two strings.
- **jaro_winkler_distance(s1, s2, scaling_factor**) - Calculate the Jaro-Winkler distance between two strings.
- **get_ngrams(s, n**) - Generate n-grams from a string.
- **ngram_similarity(s1, s2, n**) - Calculate n-gram based similarity between two strings.
- **dice_coefficient(s1, s2, n**) - Calculate Sørensen-Dice coefficient using n-grams.
- **soundex(s**) - Generate Soundex code for a string.

... 共 31 个函数

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
