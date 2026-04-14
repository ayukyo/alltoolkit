# Priority Queue Utils (优先队列工具模块)

[English](#english) | [中文](#chinese)

---

<a name="chinese"></a>
## 中文文档

### 概述

`priority_queue_utils` 是一个完整的优先队列工具模块，提供多种优先队列实现，支持零外部依赖。

### 功能特性

- **PriorityQueue** - 基于二叉堆的基本优先队列
  - 最小堆/最大堆模式
  - 查看、更新、移除元素
  - 队列合并
  - 稳定排序（相同优先级保持插入顺序）

- **UpdatablePriorityQueue** - 支持高效优先级更新
  - O(log n) 优先级更新
  - 自动检测重复元素
  - 快速查询元素优先级

- **ThreadSafePriorityQueue** - 线程安全优先队列
  - 多线程生产者-消费者模式
  - 阻塞等待和非阻塞弹出
  - 内置锁和条件变量

- **BoundedPriorityQueue** - 有界优先队列
  - 最大容量限制
  - 低优先级元素自动拒绝
  - 高优先级元素替换机制

- **TaskScheduler** - 任务调度器
  - 任务优先级管理
  - 动态更新优先级
  - 任务附加数据存储

- **工具函数**
  - `merge_sorted_lists()` - 合并有序列表
  - `top_k()` - 获取前 K 个元素
  - `create_min_heap()` / `create_max_heap()` - 工厂函数

### 时间复杂度

| 操作 | PriorityQueue | UpdatablePriorityQueue |
|------|---------------|------------------------|
| 插入 | O(log n) | O(log n) |
| 弹出 | O(log n) | O(log n) |
| 查看堆顶 | O(1) | O(1) |
| 更新优先级 | O(n) | O(log n) |
| 检查存在 | O(n) | O(1) |

### 安装

无需安装，直接导入使用：

```python
from priority_queue_utils.mod import PriorityQueue
```

### 快速开始

#### 基本使用

```python
from priority_queue_utils.mod import PriorityQueue

# 创建最小堆（优先级值越小越优先）
pq = PriorityQueue[str]()
pq.push("低优先级任务", 10)
pq.push("高优先级任务", 1)
pq.push("中等优先级任务", 5)

# 按优先级弹出
while pq:
    print(pq.pop())
# 输出: 高优先级任务, 中等优先级任务, 低优先级任务
```

#### 最大堆模式

```python
from priority_queue_utils.mod import PriorityQueue

# 创建最大堆（优先级值越大越优先）
pq = PriorityQueue[int](max_heap=True)
pq.push(10, 10)
pq.push(50, 50)
pq.push(30, 30)

while pq:
    print(pq.pop())
# 输出: 50, 30, 10
```

#### 可更新优先级队列

```python
from priority_queue_utils.mod import UpdatablePriorityQueue

pq = UpdatablePriorityQueue[str]()
pq.push("任务A", 3)
pq.push("任务B", 1)

# 高效更新优先级（O(log n)）
pq.update_priority("任务A", 0)

print(pq.pop())  # 输出: 任务A（优先级最高）
```

#### 线程安全队列

```python
from priority_queue_utils.mod import ThreadSafePriorityQueue
import threading

queue = ThreadSafePriorityQueue[int]()

# 生产者线程
def producer():
    for i in range(10):
        queue.push(i, i)

# 消费者线程
def consumer():
    while True:
        item = queue.pop(timeout=1.0)
        if item is None:
            break
        print(f"处理: {item}")

# 启动线程
threading.Thread(target=producer).start()
threading.Thread(target=consumer).start()
```

#### 有界队列

```python
from priority_queue_utils.mod import BoundedPriorityQueue

pq = BoundedPriorityQueue[int](max_size=3)

pq.push(1, 1)  # True
pq.push(2, 2)  # True
pq.push(3, 3)  # True

# 队列已满，低优先级元素被拒绝
pq.push(10, 10)  # False

# 高优先级元素会替换低优先级元素
pq.push(0, 0)  # True（替换了优先级为 3 的元素）
```

#### 任务调度器

```python
from priority_queue_utils.mod import TaskScheduler

scheduler = TaskScheduler()

# 添加带数据的任务
scheduler.add_task("紧急任务", priority=1, data={"type": "critical"})
scheduler.add_task("普通任务", priority=5, data={"type": "normal"})

# 动态更新优先级
scheduler.update_task_priority("普通任务", 2)

# 取消任务
scheduler.cancel_task("紧急任务")

# 执行任务
while scheduler:
    task = scheduler.get_next_task()
    data = scheduler.get_task_data(task)
    print(f"执行: {task}, 数据: {data}")
```

#### 合并有序列表

```python
from priority_queue_utils.mod import merge_sorted_lists

list1 = [("a", 1), ("c", 3)]
list2 = [("b", 2), ("d", 4)]

merged = merge_sorted_lists([list1, list2])
print(merged)  # [('a', 1), ('b', 2), ('c', 3), ('d', 4)]
```

#### Top K

```python
from priority_queue_utils.mod import top_k

items = [("a", 5), ("b", 3), ("c", 8), ("d", 1), ("e", 6)]

# 最大的 3 个
top3 = top_k(items, 3, largest=True)
print(top3)  # [('c', 8), ('e', 6), ('a', 5)]

# 最小的 3 个
bottom3 = top_k(items, 3, largest=False)
print(bottom3)  # [('d', 1), ('b', 3), ('a', 5)]
```

### 使用场景

1. **任务调度系统** - 按优先级执行任务
2. **事件驱动模拟** - 按时间顺序处理事件
3. **图算法** - Dijkstra 最短路径、A* 搜索
4. **数据流处理** - 合并多个有序数据流
5. **排行榜** - Top K 排名
6. **消息队列** - 优先级消息处理

### API 文档

#### PriorityQueue

```python
class PriorityQueue(Generic[T]):
    def __init__(self, max_heap: bool = False)
    def push(self, item: T, priority: float) -> None
    def pop(self) -> Optional[T]
    def peek(self) -> Optional[T]
    def peek_priority(self) -> Optional[float]
    def update_priority(self, item: T, new_priority: float) -> bool
    def remove(self, item: T) -> bool
    def merge(self, other: PriorityQueue) -> None
    def clear(self) -> None
    def to_list(self, sorted_: bool = True) -> List[Tuple[T, float]]
    
    @classmethod
    def from_list(cls, items: List[Tuple[T, float]], max_heap: bool = False) -> PriorityQueue
```

#### UpdatablePriorityQueue

```python
class UpdatablePriorityQueue(Generic[T]):
    def __init__(self, max_heap: bool = False)
    def push(self, item: T, priority: float) -> None
    def pop(self) -> Optional[T]
    def peek(self) -> Optional[T]
    def update_priority(self, item: T, new_priority: float) -> bool
    def remove(self, item: T) -> bool
    def contains(self, item: T) -> bool
    def get_priority(self, item: T) -> Optional[float]
    def clear(self) -> None
```

#### ThreadSafePriorityQueue

```python
class ThreadSafePriorityQueue(Generic[T]):
    def __init__(self, max_heap: bool = False)
    def push(self, item: T, priority: float) -> None
    def pop(self, timeout: Optional[float] = None) -> Optional[T]
    def try_pop(self) -> Optional[T]
    def peek(self) -> Optional[T]
    def clear(self) -> None
```

#### BoundedPriorityQueue

```python
class BoundedPriorityQueue(Generic[T]):
    def __init__(self, max_size: int, max_heap: bool = False)
    def push(self, item: T, priority: float) -> bool
    def pop(self) -> Optional[T]
    def peek(self) -> Optional[T]
    def is_full(self) -> bool
    def max_size(self) -> int
```

#### TaskScheduler

```python
class TaskScheduler:
    def __init__(self, max_heap: bool = False)
    def add_task(self, task_id: str, priority: float, data: Optional[Any] = None) -> None
    def get_next_task(self) -> Optional[str]
    def update_task_priority(self, task_id: str, new_priority: float) -> bool
    def cancel_task(self, task_id: str) -> bool
    def get_task_data(self, task_id: str) -> Optional[Any]
    def peek_next_task(self) -> Optional[str]
    def has_task(self, task_id: str) -> bool
    def clear(self) -> None
```

### 测试

运行测试：

```bash
cd Python/priority_queue_utils
python priority_queue_utils_test.py
```

### 示例

查看更多示例：

```bash
cd Python/priority_queue_utils/examples
python basic_usage.py        # 基本使用
python task_scheduler.py     # 任务调度器
python thread_safe.py        # 线程安全队列
python advanced_features.py  # 高级功能
```

---

<a name="english"></a>
## English Documentation

### Overview

`priority_queue_utils` is a complete priority queue toolkit providing multiple priority queue implementations with zero external dependencies.

### Features

- **PriorityQueue** - Binary heap-based priority queue
  - Min heap / Max heap modes
  - Peek, update, remove elements
  - Queue merging
  - Stable sorting (same priority preserves insertion order)

- **UpdatablePriorityQueue** - Efficient priority updates
  - O(log n) priority updates
  - Automatic duplicate detection
  - Quick priority queries

- **ThreadSafePriorityQueue** - Thread-safe priority queue
  - Multi-threaded producer-consumer pattern
  - Blocking wait and non-blocking pop
  - Built-in locks and condition variables

- **BoundedPriorityQueue** - Bounded priority queue
  - Maximum capacity limit
  - Auto-reject low priority elements
  - High priority replacement mechanism

- **TaskScheduler** - Task scheduler
  - Task priority management
  - Dynamic priority updates
  - Task data storage

- **Utility Functions**
  - `merge_sorted_lists()` - Merge sorted lists
  - `top_k()` - Get top K elements
  - `create_min_heap()` / `create_max_heap()` - Factory functions

### Time Complexity

| Operation | PriorityQueue | UpdatablePriorityQueue |
|-----------|---------------|------------------------|
| Insert | O(log n) | O(log n) |
| Pop | O(log n) | O(log n) |
| Peek | O(1) | O(1) |
| Update Priority | O(n) | O(log n) |
| Contains | O(n) | O(1) |

### Quick Start

```python
from priority_queue_utils.mod import PriorityQueue

# Create min heap (lower priority value = higher priority)
pq = PriorityQueue[str]()
pq.push("low priority", 10)
pq.push("high priority", 1)

while pq:
    print(pq.pop())
# Output: high priority, low priority
```

### Use Cases

1. **Task scheduling systems** - Execute tasks by priority
2. **Event-driven simulation** - Process events by time
3. **Graph algorithms** - Dijkstra, A* search
4. **Data stream processing** - Merge sorted streams
5. **Rankings** - Top K ranking
6. **Message queues** - Priority message processing

### Testing

```bash
cd Python/priority_queue_utils
python priority_queue_utils_test.py
```

### License

MIT License

### Author

AllToolkit Automation Assistant

### Created

2026-04-14