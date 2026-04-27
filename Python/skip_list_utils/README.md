# Skip List Utils


AllToolkit - Python Skip List Utilities

A zero-dependency, production-ready skip list implementation.
Skip list is a probabilistic data structure that provides O(log n) average
time complexity for search, insert, and delete operations.

Features:
- SkipList: Probabilistic sorted data structure
- ConcurrentSkipList: Thread-safe version with fine-grained locking
- Range queries and iteration support
- Memory-efficient node representation
- Configurable probability parameter

Author: AllToolkit
License: MIT


## 功能

### 类

- **SkipListError**: Base exception for skip list operations
- **DuplicateKeyError**: Raised when inserting a duplicate key in a unique skip list
- **KeyNotFoundError**: Raised when a key is not found
- **SkipListNode**: A node in the skip list
  方法: level
- **SkipList**: A skip list implementation with O(log n) average time complexity
  方法: size, is_empty, max_level, current_level, seed ... (26 个方法)
- **ConcurrentSkipList**: A thread-safe skip list implementation
  方法: size, is_empty, search, get, insert ... (14 个方法)
- **SkipListSet**: A skip list based set implementation
  方法: size, is_empty, add, remove, discard ... (17 个方法)

### 函数

- **create_skip_list(items, max_level, probability**, ...) - Create a skip list, optionally with initial items.
- **create_sorted_dict(items, max_level, probability**) - Create a sorted dictionary using skip list.
- **level(self**) - Return the level of this node (number of forward pointers).
- **size(self**) - Return the number of elements in the skip list.
- **is_empty(self**) - Check if the skip list is empty.
- **max_level(self**) - Return the maximum level of the skip list.
- **current_level(self**) - Return the current highest level with nodes.
- **seed(self, seed**) - Set random seed for deterministic behavior (useful for testing).
- **search(self, key**) - Search for a value by key.
- **get(self, key, default**) - Get value by key with default.

... 共 60 个函数

## 使用示例

```python
from mod import create_skip_list

# 使用 create_skip_list
result = create_skip_list()
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
