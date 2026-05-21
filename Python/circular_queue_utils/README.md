# Circular Queue Utils

循环队列实现，零依赖的高效固定大小队列。

## 功能特性

- **循环队列**: 固定大小、自动循环
- **高效操作**: O(1) 入队/出队
- **满/空检测**: 自动检测队列状态
- **统计功能**: 大小、容量、使用率
- **线程安全**: 可选的线程安全版本

## 快速开始

```python
from circular_queue_utils.mod import CircularQueue

# 创建容量为 5 的循环队列
queue = CircularQueue(capacity=5)

# 入队
queue.enqueue(1)
queue.enqueue(2)
queue.enqueue(3)

# 出队
item = queue.dequeue()  # 1

# 查看队首
front = queue.peek()  # 2
```

## 使用示例

### 基础操作

```python
from circular_queue_utils.mod import CircularQueue

queue = CircularQueue(capacity=10)

# 入队
queue.enqueue("item1")
queue.enqueue("item2")
queue.enqueue("item3")

# 出队
print(queue.dequeue())  # "item1"
print(queue.dequeue())  # "item2"

# 查看队首（不移除）
print(queue.peek())  # "item3"

# 查看队尾
print(queue.peek_tail())  # "item3"

# 清空
queue.clear()
```

### 容量管理

```python
# 创建队列
queue = CircularQueue(capacity=5)

# 填满
for i in range(5):
    queue.enqueue(i)

# 检查状态
print(queue.is_full())  # True
print(queue.is_empty())  # False
print(queue.size())  # 5
print(queue.capacity())  # 5
print(queue.utilization())  # 1.0 (100% 使用)

# 满时入队会失败或覆盖（取决于配置）
success = queue.enqueue(6)  # False（默认不覆盖）
```

### 强制入队（覆盖）

```python
# 创建覆盖模式的队列
queue = CircularQueue(capacity=5, overwrite=True)

# 填满
for i in range(5):
    queue.enqueue(i)

# 强制入队会覆盖最旧元素
queue.enqueue(10)  # 覆盖队首元素 0

print(queue.dequeue())  # 1（原队首被覆盖）
print(queue.dequeue())  # 2
print(queue.peek_tail())  # 10（新入队元素）
```

### 批量操作

```python
# 批量入队
queue = CircularQueue(capacity=10)
queue.enqueue_batch([1, 2, 3, 4, 5])

# 批量出队
items = queue.dequeue_batch(3)  # [1, 2, 3]

# 获取所有元素
all_items = queue.to_list()
```

### 遍历

```python
# 遍历队列元素
for item in queue:
    print(item)

# 或使用迭代器
for item in queue.iterate():
    print(item)
```

### 线程安全版本

```python
from circular_queue_utils.mod import ThreadSafeCircularQueue

# 创建线程安全的循环队列
queue = ThreadSafeCircularQueue(capacity=100)

# 多线程安全使用
queue.enqueue(item)
item = queue.dequeue()
```

### 统计信息

```python
stats = queue.get_stats()
print(stats['size'])        # 当前大小
print(stats['capacity'])    # 容量
print(stats['is_full'])     # 是否满
print(stats['is_empty'])    # 是否空
print(stats['total_enqueued'])  # 总入队数
print(stats['total_dequeued'])  # 总出队数
```

## API 参考

### CircularQueue

| 方法 | 说明 |
|------|------|
| `enqueue(item)` | 入队（返回是否成功） |
| `dequeue()` | 出队（返回元素或 None） |
| `peek()` | 查看队首 |
| `peek_tail()` | 查看队尾 |
| `is_empty()` | 是否空 |
| `is_full()` | 是否满 |
| `size()` | 当前大小 |
| `capacity()` | 容量 |
| `clear()` | 清空 |
| `to_list()` | 转为列表 |

### ThreadSafeCircularQueue

同 CircularQueue，但支持多线程安全访问。

## 应用场景

- **缓冲区**: 固定大小数据缓冲
- **事件队列**: 事件处理队列
- **滑动窗口**: 数据流滑动窗口
- **日志系统**: 日志缓冲区
- **音频处理**: 音频数据缓冲

---

**测试覆盖**: 完整测试套件，覆盖入队、出队、满/空检测、覆盖模式等