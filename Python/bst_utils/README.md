# Bst Utils


Binary Search Tree (BST) Utilities
===================================
A comprehensive, zero-dependency implementation of Binary Search Tree operations.

Features:
- Core BST operations: insert, delete, search
- Multiple traversal methods: in-order, pre-order, post-order, level-order
- Tree analysis: height, size, min/max, validation
- Serialization/Deserialization to/from various formats
- Balanced BST operations with AVL-style rotations
- Range queries and predecessor/successor finding


## 功能

### 类

- **BSTNode**: A node in the Binary Search Tree
  方法: is_leaf, has_one_child, has_two_children
- **BST**: Binary Search Tree implementation with comprehensive operations
  方法: root, size, is_empty, insert, insert_many ... (31 个方法)

### 函数

- **create_bst(values**) - Create a BST from a list of values.
- **create_balanced_bst(values**) - Create a balanced BST from a list of values.
- **merge_bsts(bst1, bst2**) - Merge two BSTs into a new balanced BST.
- **are_identical(bst1, bst2**) - Check if two BSTs have identical structure and values.
- **lowest_common_ancestor(bst, value1, value2**) - Find the lowest common ancestor of two values in a BST.
- **is_leaf(self**) - Check if this node is a leaf (no children).
- **has_one_child(self**) - Check if this node has exactly one child.
- **has_two_children(self**) - Check if this node has two children.
- **root(self**) - Get the root node.
- **size(self**) - Get the number of nodes in the tree.

... 共 39 个函数

## 使用示例

```python
from mod import create_bst

# 使用 create_bst
result = create_bst()
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
