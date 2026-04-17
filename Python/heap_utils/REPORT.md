# heap_utils 模块开发报告

## 模块信息

- **模块名称**: heap_utils (堆工具集)
- **位置**: Python/heap_utils/
- **语言**: Python 3
- **日期**: 2026-04-17
- **版本**: 1.0.0

## 核心功能

### 数据结构

1. **MinHeap** - 最小堆实现
   - 支持动态扩容
   - push、pop、peek、replace、pushpop 操作
   - 自定义比较键函数 (key parameter)
   - O(log n) 时间复杂度

2. **MaxHeap** - 最大堆实现
   - 与 MinHeap 接口对称
   - 堆顶始终是最大元素

3. **MinMaxHeap** - 双端堆
   - 同时支持 O(1) 获取最小和最大元素
   - O(log n) 弹出最小/最大元素
   - 适用于需要同时访问极值的场景

4. **PriorityQueue** - 优先队列
   - 支持自定义优先级
   - 相同优先级时遵循 FIFO 顺序
   - 支持最大优先队列模式

### 工具函数

1. `heap_sort(data, reverse, key)` - 堆排序算法
2. `nth_smallest(data, n, key)` - 查找第 n 小元素
3. `nth_largest(data, n, key)` - 查找第 n 大元素
4. `k_smallest(data, k, key)` - 返回最小 k 个元素
5. `k_largest(data, k, key)` - 返回最大 k 个元素
6. `merge_sorted_lists(*lists)` - 合并多个有序列表
7. `is_valid_heap(data, min_heap)` - 验证堆性质
8. `heapify(data, min_heap)` - 原地堆化
9. `median_of_data(data)` - 计算中位数

## 测试结果

```
----------------------------------------------------------------------
Ran 65 tests in 0.050s

OK
```

### 测试覆盖

- HeapItem 类: 3 测试
- MinHeap 类: 12 测试
- MaxHeap 类: 4 测试
- MinMaxHeap 类: 5 测试
- PriorityQueue 类: 6 测试
- heap_sort: 5 测试
- nth_smallest/nth_largest: 4 测试
- k_smallest/k_largest: 4 测试
- merge_sorted_lists: 4 测试
- is_valid_heap: 6 测试
- heapify: 3 测试
- median_of_data: 5 测试
- 大数据量测试: 2 测试
- 边界情况测试: 4 测试

## 使用示例

### 基本用法

```python
from heap_utils.mod import MinHeap, heap_sort

# 最小堆
heap = MinHeap([3, 1, 4, 1, 5, 9, 2, 6])
print(heap.pop())  # 1

# 堆排序
sorted_list = heap_sort([3, 1, 4, 1, 5])
print(sorted_list)  # [1, 1, 3, 4, 5]

# 第 K 小元素
print(nth_smallest([3, 1, 4, 1, 5], 3))  # 2
```

### 优先队列

```python
from heap_utils.mod import PriorityQueue

pq = PriorityQueue()
pq.push("低优先级", priority=10)
pq.push("高优先级", priority=1)
print(pq.pop())  # 高优先级
```

### 双端堆

```python
from heap_utils.mod import MinMaxHeap

heap = MinMaxHeap([3, 1, 4, 1, 5, 9, 2, 6])
print(heap.get_min())  # 1
print(heap.get_max())  # 9
```

## 特点

- **零外部依赖**: 纯 Python 标准库实现
- **类型安全**: 使用 Generic 类型参数
- **完整文档**: 每个函数和类都有详细文档
- **测试覆盖**: 65 个单元测试，覆盖各种场景
- **示例代码**: 包含完整使用示例