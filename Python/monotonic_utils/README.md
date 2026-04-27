# Monotonic Utils


单调栈和单调队列工具模块

单调栈：栈内元素保持单调递增或单调递减，用于求解下一个更大/更小元素等问题
单调队列：队列内元素保持单调性，用于滑动窗口最大/最小值等问题

零外部依赖，纯 Python 实现


## 功能

### 类

- **MonotonicStackResult**: 单调栈操作结果
- **MonotonicStack**: 单调栈实现

支持：
- 单调递增栈（栈底到栈顶递增）
- 单调递减栈（栈底到栈顶递减）
- 查找下一个更大/更小元素
- 查找上一个更大/更小元素
  方法: is_empty, size, top, top_index, push ... (8 个方法)
- **MonotonicQueue**: 单调队列实现

支持：
- 单调递增队列（队首到队尾递增）
- 单调递减队列（队首到队尾递减）
- 滑动窗口最大/最小值查询
  方法: is_empty, size, front, back, push ... (9 个方法)

### 函数

- **next_greater_element(nums**) - 找出每个元素右边第一个更大的元素
- **next_greater_element_index(nums**) - 找出每个元素右边第一个更大元素的索引
- **next_smaller_element(nums**) - 找出每个元素右边第一个更小的元素
- **prev_greater_element(nums**) - 找出每个元素左边第一个更大的元素
- **prev_smaller_element(nums**) - 找出每个元素左边第一个更小的元素
- **compute_all_monotonic_relations(nums**) - 一次性计算所有单调栈关系
- **largest_rectangle_in_histogram(heights**) - 柱状图中最大的矩形面积
- **maximal_rectangle(matrix**) - 最大矩形
- **sliding_window_max(nums, k**) - 滑动窗口最大值
- **sliding_window_min(nums, k**) - 滑动窗口最小值

... 共 35 个函数

## 使用示例

```python
from mod import next_greater_element

# 使用 next_greater_element
result = next_greater_element()
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
