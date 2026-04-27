# Ngram Utils


N-gram Utilities Module

Provides comprehensive N-gram generation and analysis utilities for text processing.
N-grams are contiguous sequences of n items (characters, words, or tokens) from a given text.

Features:
- Character N-grams (for spell checking, language detection)
- Word N-grams (for text prediction, similarity)
- Token N-grams (custom tokenization)
- N-gram frequency analysis
- N-gram similarity scoring (Jaccard, Dice, Cosine)
- Language detection using N-gram profiles
- Text prediction based on N-gram frequencies
- Zero external dependencies

Use Cases:
- Spelling correction
- Language identification
- Text classification
- Search autocomplete
- Plagiarism detection
- Text similarity comparison
- Word prediction


## 功能

### 类

- **NGramAnalyzer**: A class for comprehensive N-gram analysis of text
  方法: char_ngrams, word_ngrams, frequencies, most_common, unique ... (9 个方法)

### 函数

- **char_ngrams(text, n, pad**, ...) - Generate character N-grams from text.
- **word_ngrams(text, n, tokenizer**) - Generate word N-grams from text.
- **token_ngrams(tokens, n**) - Generate N-grams from a list of tokens.
- **ngram_frequencies(ngrams, normalize**) - Calculate frequency distribution of N-grams.
- **all_ngrams(text, min_n, max_n**, ...) - Generate all N-grams within a size range.
- **jaccard_similarity(ngrams1, ngrams2**) - Calculate Jaccard similarity between two sets of N-grams.
- **dice_similarity(ngrams1, ngrams2**) - Calculate Dice similarity (Sørensen–Dice coefficient) between two sets of N-grams.
- **cosine_similarity(freq1, freq2**) - Calculate Cosine similarity between two N-gram frequency vectors.
- **ngram_profile(text, n, top_k**) - Create an N-gram profile for a text (useful for language detection).
- **language_distance(profile1, profile2**) - Calculate out-of-place distance between two N-gram profiles.

... 共 31 个函数

## 使用示例

```python
from mod import char_ngrams

# 使用 char_ngrams
result = char_ngrams()
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
