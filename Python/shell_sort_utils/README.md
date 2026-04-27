# Shell Sort Utils


Shell Sort Utils - 希尔排序工具库

希尔排序（Shell Sort）是插入排序的优化版本，通过使用递减的间隔序列，
使元素能够大跨度移动，从而提高排序效率。

时间复杂度:
    - 最好: O(n log n)
    - 平均: O(n^1.3) 到 O(n log²n)（取决于间隔序列）
    - 最坏: O(n²)（某些间隔序列）

空间复杂度: O(1)

特点:
    - 原地排序，空间效率高
    - 对中等规模数据效率较高
    - 不稳定排序
    - 对部分有序数据效率更高

零外部依赖，纯 Python 标准库实现。


## 功能

### 类

- **GapSequence**: 间隔序列类型
- **SortResult**: 排序结果

### 函数

- **generate_shell_gaps(n**) - 生成原始 Shell 间隔序列
- **generate_knuth_gaps(n**) - 生成 Knuth 间隔序列
- **generate_hibbard_gaps(n**) - 生成 Hibbard 间隔序列
- **generate_sedgewick_gaps(n**) - 生成 Sedgewick 间隔序列
- **generate_ciura_gaps(n**) - 生成 Ciura 间隔序列
- **generate_tokuda_gaps(n**) - 生成 Tokuda 间隔序列
- **generate_pratt_gaps(n**) - 生成 Pratt 间隔序列（3-smooth 数）
- **get_gap_sequence(n, sequence**) - 获取指定类型的间隔序列
- **shell_sort(data, gap_sequence, reverse**, ...) - 希尔排序
- **shell_sort_with_trace(data, gap_sequence, reverse**, ...) - 带跟踪的希尔排序

... 共 24 个函数

## 使用示例

```python
from mod import generate_shell_gaps

# 使用 generate_shell_gaps
result = generate_shell_gaps()
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
