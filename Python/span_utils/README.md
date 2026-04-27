# Span Utils


Span Utils - 区间操作工具库

提供区间（范围）的各种操作，包括合并、交集、差集、分割等。
支持整数区间和浮点数区间，支持开区间和闭区间。

零外部依赖，纯 Python 标准库实现。


## 功能

### 类

- **BoundType**: 区间边界类型
- **Span**: 区间类，表示一个数值区间

Attributes:
    start: 区间起始值
    end: 区间结束值
    left_bound: 左边界类型
    right_bound: 右边界类型
  方法: length, is_empty, is_point, overlaps, intersection ... (9 个方法)

### 函数

- **span(start, end, closed**) - 快速创建闭区间或开区间
- **closed_span(start, end**) - 创建闭区间 [a, b]
- **open_span(start, end**) - 创建开区间 (a, b)
- **point_span(value**) - 创建单点区间 [a, a]
- **merge_spans(spans**) - 合并重叠的区间
- **intersection_of(spans**) - 计算多个区间的交集
- **subtract_span(source, subtractor**) - 从源区间中减去另一个区间
- **subtract_spans(source, subtractors**) - 从源区间中减去多个区间
- **union_spans(spans**) - 计算多个区间的并集
- **span_difference(spans1, spans2**) - 计算两组区间的差集（spans1 - spans2）

... 共 34 个函数

## 使用示例

```python
from mod import span

# 使用 span
result = span()
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
