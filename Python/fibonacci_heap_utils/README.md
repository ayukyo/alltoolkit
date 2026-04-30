# Fibonacci Heap Utils

斐波那契堆工具模块 - 提供高效的斐波那契堆数据结构实现。

## 功能特性

- **斐波那契堆**: O(1) 摊还插入、合并、减小键操作
- **最小堆/最大堆模式**: 支持最小堆和最大堆两种模式
- **泛型支持**: 支持任意可比较的数据类型
- **优先队列操作**: insert, extract_min/max, decrease_key, merge, delete
- **序列化**: 支持序列化与反序列化
- **零外部依赖**: 仅使用 Python 标准库

## 时间复杂度

| 操作 | 摊还时间复杂度 |
|------|---------------|
| insert | O(1) |
| find_min | O(1) |
| extract_min | O(log n) |
| decrease_key | O(1) |
| merge | O(1) |
| delete | O(log n) |

斐波那契堆在需要频繁执行 decrease_key 操作的场景（如 Dijkstra 算法、Prim 算法）中表现优异。

## 快速开始

```python
from fibonacci_heap_utils.mod import FibonacciHeap, MaxFibonacciHeap

# 创建最小堆
heap = FibonacciHeap[int]()

# 插入元素
heap.insert(5, "task_low")
heap.insert(1, "task_high")
heap.insert(3, "task_medium")

# 获取最小元素
print(heap.peek())           # "task_high"
print(heap.peek_key())       # 1

# 删除最小元素
min_val = heap.extract_min()
print(min_val)               # "task_high"

# 查看堆大小
print(len(heap))             # 2
```

## 核心类

### FibonacciHeap

最小斐波那契堆实现。

```python
from fibonacci_heap_utils.mod import FibonacciHeap

heap = FibonacciHeap[int]()  # 最小堆

# 插入元素（返回节点，用于后续decrease_key）
node = heap.insert(key=10, value="data")

# 查询操作
heap.peek()                  # 查看最小值
heap.peek_key()              # 查看最小键
heap.find_min()              # 获取最小键
heap.find_min_value()        # 获取最小值
heap.is_empty()              # 是否为空
len(heap)                    # 元素数量
heap.size                    # 元素数量

# 提取操作
heap.extract_min()           # 删除并返回最小值
heap.extract_min_with_key()  # 删除并返回 (key, value)

# 键值操作
heap.decrease_key(node, new_key)  # 减小键值
heap.delete(node)            # 删除指定节点

# 合并操作
heap.merge(other_heap)       # 合并另一个堆（other堆会被清空）

# 查找操作
heap.contains(value)         # 检查是否包含值
heap.find_node(value)        # 查找节点（返回Node或None）
heap.get_all_values()        # 获取所有值
heap.get_all_keys()          # 获取所有键

# 转换操作
heap.to_list()               # 提取所有元素并排序
heap.clear()                 # 清空堆
heap.copy()                  # 创建副本

# 序列化
heap.to_dict()               # 转为字典
heap.to_json()               # 转为JSON字符串
FibonacciHeap.from_dict(d)   # 从字典创建
FibonacciHeap.from_json(s)   # 从JSON创建
```

### MaxFibonacciHeap

最大斐波那契堆实现。

```python
from fibonacci_heap_utils.mod import MaxFibonacciHeap

heap = MaxFibonacciHeap[int]()

heap.insert(5, "five")
heap.insert(10, "ten")
heap.insert(1, "one")

heap.find_max()              # 10
heap.find_max_value()        # "ten"
heap.extract_max()           # "ten"
heap.increase_key(node, 15)  # 增大键值
```

### FibonacciHeapUtils

静态工具方法集合。

```python
from fibonacci_heap_utils.mod import FibonacciHeapUtils

# 创建堆
FibonacciHeapUtils.create_min_heap()
FibonacciHeapUtils.create_max_heap()

# 合并多个堆
merged = FibonacciHeapUtils.merge_heaps(h1, h2, h3)

# 堆排序
sorted_list = FibonacciHeapUtils.heap_sort([5, 2, 8, 1])

# Top K
top_3 = FibonacciHeapUtils.top_k(items, k=3, largest=True)

# 找中位数
median = FibonacciHeapUtils.find_median([1, 2, 3, 4, 5])
```

### 便捷函数

```python
from fibonacci_heap_utils.mod import (
    create_min_heap, create_max_heap,
    heap_sort, top_k
)

# 快速创建堆
heap = create_min_heap()
max_heap = create_max_heap()

# 堆排序
result = heap_sort([5, 2, 8, 1], reverse=False)
# [1, 2, 5, 8]

# Top K
largest_3 = top_k([5, 2, 8, 1, 9], k=3, largest=True)
# [7, 8, 9] 或类似
```

## 使用场景

### 1. Dijkstra 最短路径算法

斐波那契堆在 Dijkstra 算法中显著优于普通堆，因为频繁需要 decrease_key 操作。

```python
def dijkstra_fibonacci(graph, source):
    """使用斐波那契堆优化的Dijkstra算法"""
    from fibonacci_heap_utils.mod import FibonacciHeap
    
    dist = {v: float('inf') for v in graph}
    dist[source] = 0
    
    nodes = {}
    heap = FibonacciHeap[float]()
    
    for v in graph:
        nodes[v] = heap.insert(dist[v], v)
    
    while not heap.is_empty():
        d, u = heap.extract_min_with_key()
        
        for v, weight in graph[u].items():
            new_dist = d + weight
            if new_dist < dist[v]:
                dist[v] = new_dist
                heap.decrease_key(nodes[v], new_dist)
    
    return dist
```

### 2. Prim 最小生成树算法

```python
def prim_fibonacci(graph):
    """使用斐波那契堆优化的Prim算法"""
    from fibonacci_heap_utils.mod import FibonacciHeap
    
    start = next(iter(graph))
    in_mst = {start}
    heap = FibonacciHeap[float]()
    nodes = {}
    
    for v, w in graph[start].items():
        nodes[v] = heap.insert(w, v)
    
    mst_edges = []
    
    while not heap.is_empty():
        weight, v = heap.extract_min_with_key()
        in_mst.add(v)
        
        # 找到连接v到MST的边（实际实现需记录）
        mst_edges.append((v, weight))
        
        for u, w in graph[v].items():
            if u not in in_mst:
                if u in nodes and w < nodes[u].key:
                    heap.decrease_key(nodes[u], w)
                elif u not in nodes:
                    nodes[u] = heap.insert(w, u)
    
    return mst_edges
```

### 3. 优先队列任务调度

```python
from fibonacci_heap_utils.mod import FibonacciHeap

class TaskScheduler:
    def __init__(self):
        self.heap = FibonacciHeap[str]()
        self.tasks = {}
    
    def add_task(self, priority, task_id):
        node = self.heap.insert(priority, task_id)
        self.tasks[task_id] = node
    
    def get_next_task(self):
        return self.heap.extract_min()
    
    def update_priority(self, task_id, new_priority):
        if task_id in self.tasks:
            self.heap.decrease_key(self.tasks[task_id], new_priority)
    
    def cancel_task(self, task_id):
        if task_id in self.tasks:
            self.heap.delete(self.tasks[task_id])
            del self.tasks[task_id]
```

### 4. Top K 问题

```python
from fibonacci_heap_utils.mod import top_k

# 找最大的K个元素
numbers = [5, 2, 8, 1, 9, 3, 7, 4, 6]
top_3 = top_k(numbers, k=3, largest=True)
print(top_3)  # [9, 8, 7]

# 找最小的K个元素
bottom_3 = top_k(numbers, k=3, largest=False)
print(bottom_3)  # [1, 2, 3]

# 带自定义键函数
words = ["apple", "banana", "cherry", "pie", "hi"]
longest_2 = top_k(words, k=2, key_func=len, largest=True)
print(longest_2)  # ["banana", "cherry"]
```

## 实现细节

### 斐波那契堆结构

斐波那契堆由一组堆有序树组成：

- **根链表**: 所有树的根节点通过循环双向链表连接
- **子链表**: 每个节点的子节点也通过循环双向链表连接
- **度数**: 每个节点的子节点数量
- **标记**: 用于级联剪切操作

### 关键操作原理

**Insert (O(1))**: 
- 创建新节点，添加到根链表
- 如果新键值小于最小节点，更新最小指针

**Extract Min (O(log n))**: 
- 将最小节点的子节点添加到根链表
- 移除最小节点
- Consolidate: 合并相同度数的树

**Decrease Key (O(1))**: 
- 如果新键值违反堆性质，剪切节点到根链表
- 级联剪切被标记的父节点

**Merge (O(1))**: 
- 简单连接两个堆的根链表
- 更新最小指针

## 与普通堆的比较

| 操作 | 普通二叉堆 | 斐波那契堆 |
|------|-----------|-----------|
| insert | O(log n) | O(1) |
| find_min | O(1) | O(1) |
| extract_min | O(log n) | O(log n) |
| decrease_key | O(log n) | O(1) |
| delete | O(log n) | O(log n) |
| merge | O(n) | O(1) |

斐波那契堆在 decrease_key 和 merge 操作上有显著优势。

## 测试

运行测试:

```bash
cd Python/fibonacci_heap_utils
python fibonacci_heap_utils_test.py
```

测试覆盖:
- 基本操作（插入、提取、查找）
- 最大堆功能
- decrease_key/increase_key
- delete 操作
- merge 合并
- 查询操作
- 序列化/反序列化
- 边界情况（负数、浮点、重复键）
- 压力测试（大量元素）
- 工具类方法

## API 参考

详细 API 文档请参考源代码注释。

## 许可证

MIT License