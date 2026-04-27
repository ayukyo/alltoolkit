# Rope Utils


AllToolkit - Rope Data Structure Utilities Module
==================================================
A comprehensive Rope data structure implementation for efficient string manipulation.
Zero external dependencies - pure Python implementation.

Features:
    - Rope data structure for efficient string operations
    - O(log n) insert, delete, split, and concatenate operations
    - Lazy evaluation with automatic rebalancing
    - Support for large text files (millions of characters)
    - Index-based access and iteration
    - String-like interface for familiar usage
    - Memory-efficient with reference sharing

The Rope data structure is ideal for:
    - Text editors and IDEs
    - Large file manipulation
    - String processing pipelines
    - Undo/redo implementations

Author: AllToolkit Contributors
License: MIT


## 功能

### 类

- **RopeNode**: Abstract base class for rope nodes
  方法: length, char_at, substring, insert, delete ... (9 个方法)
- **LeafNode**: Leaf node containing actual string data
  方法: length, char_at, substring, insert, delete ... (9 个方法)
- **InternalNode**: Internal node with left and right children
  方法: length, char_at, substring, insert, delete ... (9 个方法)
- **Rope**: Rope data structure for efficient string manipulation
  方法: length, depth, char_at, insert, delete ... (29 个方法)
- **BatchEditor**: Batch editor for efficient multiple operations on a rope
  方法: insert, delete, replace, apply, clear
- **RopeIterator**: Iterator for traversing rope nodes

### 函数

- **concat(left, right, leaf_max**) - Concatenate two rope nodes.
- **concat_ropes(left, right, leaf_max**) - Concatenate two ropes.
- **from_lines(lines, leaf_max**) - Create rope from list of lines.
- **from_file(filepath, leaf_max**) - Create rope from file contents.
- **to_file(rope, filepath**) - Write rope contents to file.
- **build_balanced(text, leaf_max**) - Build a balanced rope from text.
- **length(self**) - Return total length of rope.
- **char_at(self, index**) - Get character at index.
- **substring(self, start, end**) - Extract substring [start, end).
- **insert(self, index, text**) - Insert text at index.

... 共 67 个函数

## 使用示例

```python
from mod import concat

# 使用 concat
result = concat()
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
