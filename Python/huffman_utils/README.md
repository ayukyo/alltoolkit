# Huffman Utils


AllToolkit - Huffman Coding Utilities Module
=============================================
A comprehensive Huffman encoding/decoding utility module with zero external dependencies.

Features:
    - Huffman tree construction from frequency data
    - Text and binary data encoding/decoding
    - Adaptive Huffman coding support
    - Canonical Huffman codes generation
    - Frequency analysis and visualization
    - Compression ratio calculation
    - Bit-level operations for efficient storage
    - Support for custom symbol alphabets

Author: AllToolkit Contributors
License: MIT


## 功能

### 类

- **HuffmanNode**: Node in a Huffman tree
  方法: is_leaf
- **HuffmanTree**: Huffman tree container with root node
  方法: build_from_frequencies, get_code, decode_symbol

### 函数

- **build_frequency_table(data, byte_mode**) - Build frequency table from input data.
- **build_huffman_tree(frequencies**) - Build Huffman tree from frequency dictionary.
- **encode_text(text, tree**) - Encode text using Huffman coding.
- **decode_text(encoded, tree**) - Decode Huffman-encoded binary string back to text.
- **encode_bytes(data, tree**) - Encode bytes using Huffman coding.
- **decode_bytes(encoded, tree, padding**) - Decode Huffman-encoded bytes back to original data.
- **generate_canonical_codes(code_lengths**) - Generate canonical Huffman codes from code lengths.
- **calculate_compression_ratio(original_size, compressed_size**) - Calculate compression ratio.
- **calculate_compression_percentage(original_size, compressed_size**) - Calculate compression percentage.
- **get_code_statistics(tree**) - Get statistics about the Huffman codes.

... 共 27 个函数

## 使用示例

```python
from mod import build_frequency_table

# 使用 build_frequency_table
result = build_frequency_table()
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
