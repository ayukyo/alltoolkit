# Simhash Utils


AllToolkit - SimHash Utilities Module
=====================================
A comprehensive SimHash (Similarity Hash) utility module with zero external dependencies.

SimHash is a locality-sensitive hashing technique used for:
    - Near-duplicate document detection
    - Web page deduplication
    - Code similarity detection
    - Quick document fingerprinting

Features:
    - SimHash generation from text using various tokenization strategies
    - Hamming distance calculation for fingerprint comparison
    - Similarity threshold detection
    - Multiple hash algorithms support (built-in)
    - Chinese text support with character/word tokenization
    - N-gram based tokenization
    - Batch processing capabilities
    - Index-based similarity search

Author: AllToolkit Contributors
License: MIT


## 功能

### 类

- **SimHashIndex**: An index for fast similarity search using SimHash
  方法: add, add_batch, remove, query, get_duplicates ... (7 个方法)

### 函数

- **hash_token(token, algorithm, size**) - Hash a token to a fixed-size integer.
- **tokenize_words(text, lowercase, remove_punctuation**, ...) - Tokenize text into words.
- **tokenize_chars(text, lowercase, remove_whitespace**) - Tokenize text into characters.
- **tokenize_ngrams(text, n, lowercase**, ...) - Tokenize text into n-grams.
- **tokenize_chinese(text, mode, ngram_size**) - Tokenize Chinese text.
- **compute_simhash(tokens, fingerprint_size, hash_algorithm**, ...) - Compute SimHash fingerprint from a list of tokens.
- **compute_simhash_text(text, tokenizer, ngram_size**, ...) - Compute SimHash fingerprint directly from text.
- **hamming_distance(fp1, fp2, size**) - Calculate Hamming distance between two fingerprints.
- **hamming_distance_normalized(fp1, fp2, size**) - Calculate normalized Hamming distance (0 to 1).
- **similarity(fp1, fp2, size**) - Calculate similarity between two fingerprints.

... 共 31 个函数

## 使用示例

```python
from mod import hash_token

# 使用 hash_token
result = hash_token()
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
