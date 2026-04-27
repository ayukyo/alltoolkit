# Segment Tree Utils


Segment Tree Utils - 线段树工具库

线段树（Segment Tree）是一种用于高效处理区间查询和更新的数据结构。

时间复杂度:
    - 构建树: O(n)
    - 区间查询: O(log n)
    - 单点更新: O(log n)
    - 区间更新（懒标记）: O(log n)

空间复杂度: O(n)

特点:
    - 支持多种聚合操作（求和、最值、GCD 等）
    - 支持区间更新（懒标记）
    - 支持动态开点（稀疏线段树）
    - 可扩展性强

零外部依赖，纯 Python 标准库实现。


## 功能

### 类

- **OperationType**: 操作类型枚举
- **SegmentTree**: 基础线段树

支持操作:
    - 区间查询: query(left, right)
    - 单点更新: update(index, value)

Example:
    >>> st = SegmentTree([1, 2, 3, 4, 5], OperationType
  方法: query, update, get, to_list
- **SegmentTreeLazy**: 支持懒标记的线段树（区间更新）

支持操作:
    - 区间查询: query(left, right)
    - 单点更新: update(index, value)
    - 区间更新: range_update(left, right, value)
    - 区间增加: range_add(left, right, delta)

Example:
    >>> st = SegmentTreeLazy([1, 2, 3, 4, 5])
    >>> st
  方法: query, update, range_add, range_update, get ... (6 个方法)
- **SegmentTreeMin**: 区间最小值线段树

支持操作:
    - 区间最小值查询: query(left, right)
    - 单点更新: update(index, value)

Example:
    >>> st = SegmentTreeMin([5, 3, 7, 1, 9])
    >>> st
  方法: query, update, get
- **SegmentTreeMax**: 区间最大值线段树

支持操作:
    - 区间最大值查询: query(left, right)
    - 单点更新: update(index, value)

Example:
    >>> st = SegmentTreeMax([5, 3, 7, 1, 9])
    >>> st
  方法: query, update, get
- **SegmentTreeGCD**: 区间最大公约数线段树

支持操作:
    - 区间 GCD 查询: query(left, right)
    - 单点更新: update(index, value)

Example:
    >>> st = SegmentTreeGCD([12, 18, 24, 36])
    >>> st
  方法: query, update, get
- **SegmentTreeXOR**: 区间异或线段树

支持操作:
    - 区间异或查询: query(left, right)
    - 单点更新: update(index, value)

Example:
    >>> st = SegmentTreeXOR([1, 2, 3, 4, 5])
    >>> st
  方法: query, update, get
- **SegmentTreeCount**: 区间计数线段树

统计区间内满足条件的元素个数

Example:
    >>> st = SegmentTreeCount([1, 2, 3, 4, 5], lambda x: x % 2 == 0)
    >>> st
  方法: query, update, get
- **SegmentTreeProduct**: 区间乘积线段树

支持操作:
    - 区间乘积查询: query(left, right)
    - 单点更新: update(index, value)

注意: 可能会溢出，建议配合模数使用

Example:
    >>> st = SegmentTreeProduct([1, 2, 3, 4, 5])
    >>> st
  方法: query, update, get

### 函数

- **gcd(a, b**) - 计算最大公约数
- **lcm(a, b**) - 计算最小公倍数
- **create_segment_tree(data, op_type**) - 创建线段树
- **range_sum(data, queries**) - 批量区间求和
- **range_min(data, queries**) - 批量区间最小值查询
- **range_max(data, queries**) - 批量区间最大值查询
- **range_gcd(data, queries**) - 批量区间 GCD 查询
- **query(self, left, right**) - 区间查询
- **update(self, index, value**) - 单点更新：将指定位置设置为 value
- **get(self, index**) - 获取指定位置的值

... 共 35 个函数

## 使用示例

```python
from mod import gcd

# 使用 gcd
result = gcd()
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
