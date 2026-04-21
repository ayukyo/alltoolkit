# PriorityQueueUtils - C# 优先队列工具类

零依赖的优先队列实现，提供最小堆和最大堆两种模式。

## 特性

- **零依赖**: 仅使用 .NET 标准库
- **两种模式**: 支持最小堆（优先级值越小越先出队）和最大堆（优先级值越大越先出队）
- **泛型支持**: 支持任意元素类型
- **完整API**: 入队、出队、查看、查找、清空等操作
- **高效实现**: 所有操作时间复杂度 O(log n)

## API

### MinPriorityQueue<T> - 最小堆优先队列

| 方法 | 描述 | 时间复杂度 |
|------|------|-----------|
| `Enqueue(T value, int priority)` | 入队 | O(log n) |
| `Dequeue()` | 出队（返回值） | O(log n) |
| `DequeueWithPriority()` | 出队（返回值和优先级） | O(log n) |
| `Peek()` | 查看队首（不移除） | O(1) |
| `PeekWithPriority()` | 查看队首（含优先级） | O(1) |
| `TryPeek(out T, out int)` | 尝试查看队首 | O(1) |
| `TryDequeue(out T, out int)` | 尝试出队 | O(log n) |
| `Contains(T value)` | 检查是否包含值 | O(n) |
| `Contains(T value, int priority)` | 检查是否包含值和优先级 | O(n) |
| `Clear()` | 清空队列 | O(1) |
| `GetAll()` | 获取所有元素（不移除） | O(n) |
| `Count` | 元素数量 | O(1) |
| `IsEmpty` | 是否为空 | O(1) |

### MaxPriorityQueue<T> - 最大堆优先队列

API 与 MinPriorityQueue 相同，但优先级值越大越先出队。

### PriorityQueue 工厂方法

| 方法 | 描述 |
|------|------|
| `CreateMinQueue<T>()` | 创建最小堆优先队列 |
| `CreateMinQueue<T>(int capacity)` | 创建指定容量最小堆队列 |
| `CreateMaxQueue<T>()` | 创建最大堆优先队列 |
| `CreateMaxQueue<T>(int capacity)` | 创建指定容量最大堆队列 |
| `FromCollection(IEnumerable)` | 从集合创建最小堆队列 |
| `FromCollectionMax(IEnumerable)` | 从集合创建最大堆队列 |
| `Merge(params queues)` | 合并多个最小堆队列 |
| `MergeMax(params queues)` | 合并多个最大堆队列 |

## 使用示例

### 基本使用

```csharp
using AllToolkit.PriorityQueueUtils;

// 创建最小堆优先队列
var queue = new MinPriorityQueue<string>();

// 入队
queue.Enqueue("低优先级", 3);
queue.Enqueue("高优先级", 1);
queue.Enqueue("中优先级", 2);

// 出队（按优先级）
while (!queue.IsEmpty)
{
    var item = queue.Dequeue();
    Console.WriteLine(item);  // 输出: 高优先级, 中优先级, 低优先级
}
```

### 任务调度

```csharp
var scheduler = new MinPriorityQueue<Task>();
scheduler.Enqueue(new Task { Name = "紧急任务" }, 1);
scheduler.Enqueue(new Task { Name = "普通任务" }, 5);
scheduler.Enqueue(new Task { Name = "重要任务" }, 2);

// 按优先级执行
var nextTask = scheduler.Dequeue();  // 紧急任务最先执行
```

### Dijkstra 最短路径

```csharp
var distances = new MinPriorityQueue<string>();
distances.Enqueue("起点", 0);

while (!distances.IsEmpty)
{
    var node = distances.DequeueWithPriority();
    // 处理节点...
}
```

### Top K 问题

```csharp
// 找最大的5个数：使用大小为5的最小堆
var minHeap = new MinPriorityQueue<int>();
foreach (var num in data)
{
    minHeap.Enqueue(num, num);
    if (minHeap.Count > 5)
        minHeap.Dequeue();  // 移除最小的
}
// minHeap中剩下的就是最大的5个
```

### 最大堆使用

```csharp
var maxQueue = new MaxPriorityQueue<int>();
maxQueue.Enqueue(1, 10);  // 优先级10
maxQueue.Enqueue(2, 30);  // 优先级30
maxQueue.Enqueue(3, 20);  // 优先级20

// 出队顺序: 2(优先级30) -> 3(优先级20) -> 1(优先级10)
```

## 时间复杂度

| 操作 | 时间复杂度 |
|------|-----------|
| 入队 (Enqueue) | O(log n) |
| 出队 (Dequeue) | O(log n) |
| 查看队首 (Peek) | O(1) |
| 查找 (Contains) | O(n) |
| 清空 (Clear) | O(1) |

## 测试

```bash
# 编译测试
csc PriorityQueueUtils.cs PriorityQueueUtilsTest.cs

# 运行测试
./PriorityQueueUtilsTest.exe
```

测试覆盖:
- 基本入队出队
- 相同优先级处理
- Peek/PeekWithPriority
- TryPeek/TryDequeue
- Contains
- Clear
- 负数优先级
- 极端优先级值 (int.MinValue/MaxValue)
- 大量元素测试
- 空队列异常处理
- 工厂方法
- 合并队列
- 性能测试

## 文件结构

```
C#/priority_queue_utils/
├── PriorityQueueUtils.cs       # 主模块
├── PriorityQueueUtilsTest.cs   # 测试
├── README.md                   # 文档
└── examples/
    └── usage_examples.cs       # 使用示例
```

## 许可证

MIT License

---

**创建日期**: 2026-04-21
**语言**: C# (.NET)
**依赖**: 无（仅使用标准库）