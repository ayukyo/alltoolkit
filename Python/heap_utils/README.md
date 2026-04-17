# 堆工具集 (Heap Utilities)

提供全面的堆数据结构和操作功能，零外部依赖，纯 Python 实现。

## 功能特性

### 数据结构

- **MinHeap** - 最小堆，堆顶始终是最小元素
- **MaxHeap** - 最大堆，堆顶始终是最大元素
- **MinMaxHeap** - 双端堆，同时支持 O(log n) 获取最小和最大元素
- **PriorityQueue** - 优先队列，支持自定义优先级和 FIFO 顺序

### 工具函数

- `heap_sort()` - 堆排序算法
- `nth_smallest()` - 找出第 n 小的元素
- `nth_largest()` - 找出第 n 大的元素
- `k_smallest()` - 找出最小的 k 个元素
- `k_largest()` - 找出最大的 k 个元素
- `merge_sorted_lists()` - 合并多个已排序列表
- `is_valid_heap()` - 检查列表是否满足堆性质
- `heapify()` - 将列表原地转换为堆
- `median_of_data()` - 使用堆计算中位数

## 快速开始

```python
from heap_utils.mod import MinHeap, MaxHeap, heap_sort, k_smallest

# 最小堆
heap = MinHeap([3, 1, 4, 1, 5, 9, 2, 6])
print(heap.pop())  # 1 (最小元素)
print(heap.peek())  # 1 (查看堆顶，不移除)

# 堆排序
sorted_list = heap_sort([3, 1, 4, 1, 5, 9, 2, 6])
print(sorted_list)  # [1, 1, 2, 3, 4, 5, 6, 9]

# 找出最小的3个元素
print(k_smallest([3, 1, 4, 1, 5, 9, 2, 6], 3))  # [1, 1, 2]

# 最大堆
max_heap = MaxHeap([3, 1, 4, 1, 5, 9, 2, 6])
print(max_heap.pop())  # 9 (最大元素)
```

## 使用示例

### 优先队列

```python
from heap_utils.mod import PriorityQueue

pq = PriorityQueue()
pq.push("低优先级任务", priority=10)
pq.push("高优先级任务", priority=1)
pq.push("中优先级任务", priority=5)

print(pq.pop())  # 高优先级任务
print(pq.pop())  # 中优先级任务
print(pq.pop())  # 低优先级任务
```

### 自定义比较键

```python
from heap_utils.mod import MinHeap

# 按对象的某个属性排序
tasks = [
    {"name": "task1", "priority": 3},
    {"name": "task2", "priority": 1},
    {"name": "task3", "priority": 2},
]

heap = MinHeap(tasks, key=lambda x: x["priority"])
print(heap.pop()["name"])  # task2
```

### 双端堆

```python
from heap_utils.mod import MinMaxHeap

heap = MinMaxHeap([3, 1, 4, 1, 5, 9, 2, 6])
print(heap.get_min())  # 1
print(heap.get_max())  # 9
print(heap.pop_min())  # 1
print(heap.pop_max())  # 9
```

### 第K大/小元素

```python
from heap_utils.mod import nth_smallest, nth_largest

data = [3, 1, 4, 1, 5, 9, 2, 6]

print(nth_smallest(data, 3))  # 第3小: 2
print(nth_largest(data, 2))  # 第2大: 6
```

### 计算中位数

```python
from heap_utils.mod import median_of_data

print(median_of_data([1, 2, 3, 4, 5]))  # 3.0
print(median_of_data([1, 2, 3, 4]))  # 2.5
```

## API 参考

### MinHeap 类

| 方法 | 描述 | 时间复杂度 |
|------|------|----------|
| `push(item)` | 添加元素 | O(log n) |
| `pop()` | 弹出堆顶 | O(log n) |
| `peek()` | 查看堆顶 | O(1) |
| `replace(item)` | 替换堆顶 | O(log n) |
| `pushpop(item)` | 先入后出 | O(log n) |
| `clear()` | 清空堆 | O(1) |
| `to_list(sorted_)` | 转换列表 | O(n log n) |
| `update(index, item)` | 更新元素 | O(log n) |

### MaxHeap 类

与 MinHeap 接口相同，但堆顶是最大元素。

### MinMaxHeap 类

| 方法 | 描述 | 时间复杂度 |
|------|------|----------|
| `push(item)` | 添加元素 | O(log n) |
| `get_min()` | 获取最小元素 | O(1) |
| `get_max()` | 获取最大元素 | O(1) |
| `pop_min()` | 弹出最小元素 | O(log n) |
| `pop_max()` | 弹出最大元素 | O(log n) |

### PriorityQueue 类

| 方法 | 描述 | 时间复杂度 |
|------|------|----------|
| `push(item, priority)` | 入队 | O(log n) |
| `pop()` | 出队 | O(log n) |
| `peek()` | 查看队首 | O(1) |
| `clear()` | 清空队列 | O(1) |

## 测试

```bash
# 运行所有测试
python -m pytest heap_utils_test.py -v

# 或直接运行
python heap_utils_test.py
```

## 许可证

MIT License