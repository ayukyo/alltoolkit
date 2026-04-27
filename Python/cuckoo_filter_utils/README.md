# Cuckoo Filter Utils


Cuckoo Filter - A probabilistic data structure for testing set membership.

Cuckoo filters are similar to Bloom filters but offer:
- Support for deletion (unlike Bloom filters)
- Better space efficiency
- Lower false positive rates for the same memory usage
- Constant time operations (O(1) average)

Reference: "Cuckoo Filter: Practically Better Than Bloom" by Fan et al.


## 功能

### 类

- **CuckooFilter**: A Cuckoo filter data structure for approximate set membership queries
  方法: count, capacity, load_factor, insert, insert_string ... (16 个方法)

### 函数

- **create_optimal_filter(expected_items, fp_rate**) - Create a Cuckoo filter optimized for given parameters.
- **calculate_false_positive_rate(fp_bits, bucket_size**) - Calculate the theoretical false positive rate.
- **count(self**) - Number of items currently stored.
- **capacity(self**) - Total capacity of the filter.
- **load_factor(self**) - Load factor (fraction of slots used).
- **insert(self, data**) - Insert an item into the filter.
- **insert_string(self, s**) - Insert a string into the filter.
- **contains(self, data**) - Check if an item might be in the filter.
- **contains_string(self, s**) - Check if a string might be in the filter.
- **delete(self, data**) - Remove an item from the filter.

... 共 18 个函数

## 使用示例

```python
from mod import create_optimal_filter

# 使用 create_optimal_filter
result = create_optimal_filter()
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
