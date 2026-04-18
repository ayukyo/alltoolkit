# Queue Utils - Kotlin 队列工具模块

**零依赖的队列工具库，仅使用 Kotlin/Java 标准库**

提供多种队列实现：循环队列、线程安全队列、优先级队列、双端队列、延迟队列。

## 📦 模块特性

- ✅ **零依赖** - 仅使用 Kotlin/Java 标准库
- ✅ **线程安全** - 支持多线程并发访问
- ✅ **阻塞操作** - 支持 put/take 和超时操作
- ✅ **优先级支持** - 按优先级处理元素
- ✅ **延迟队列** - 任务延迟执行
- ✅ **丰富工具函数** - 过滤、映射、归约、分组等

## 🚀 快速开始

### 导入模块

```kotlin
import queue_utils.*
```

### 循环队列 (固定容量)

```kotlin
val buffer = CircularQueue<String>(5)

buffer.enqueue("A")
buffer.enqueue("B")
buffer.enqueue("C")

println(buffer.size)      // 3
println(buffer.available()) // 2
println(buffer.isFull())  // false

println(buffer.dequeue()) // "A"
println(buffer.peek())    // "B"
```

### 线程安全队列

```kotlin
val queue = ThreadSafeQueue<Int>(100)

// 基本操作
queue.enqueue(1)
val item = queue.dequeue()

// 阻塞操作（无限等待）
queue.put(2)
val item2 = queue.take()

// 超时操作
val offered = queue.offer(3, 1000) // 1秒超时
val polled = queue.poll(500)       // 500ms超时

// 批量转移
val target = mutableListOf<Int>()
queue.drainTo(target)
```

### 优先级队列

```kotlin
val taskQueue = PriorityAwareQueue<String>()

// 数值越小优先级越高
taskQueue.enqueue("Normal", 5)
taskQueue.enqueue("Urgent", 1)   // 最高优先级
taskQueue.enqueue("High", 2)

println(taskQueue.peek())  // "Urgent"
println(taskQueue.peekWithPriority())  // ("Urgent", 1)

// 按优先级出队
println(taskQueue.dequeue())  // "Urgent"
println(taskQueue.dequeue())  // "High"
println(taskQueue.dequeue())  // "Normal"
```

### 双端队列

```kotlin
val deque = ArrayDequeImpl<Int>()

deque.addFirst(1)
deque.addLast(2)
deque.addFirst(0)  // 头部插入

println(deque.peekFirst())  // 0
println(deque.peekLast())   // 2

deque.rotate(1)  // 向右旋转
println(deque.toList())     // [2, 0, 1]
```

### 延迟队列

```kotlin
val delayQueue = DelayQueue<DelayedTask>()

// 添加延迟任务
delayQueue.put(DelayedTask({ 
    println("Task executed!") 
}, 1000)) // 1秒后执行

// 等待任务到期
val task = delayQueue.take()
task.execute()

// 超时获取
val taskOrNull = delayQueue.poll(500) // 500ms超时
```

### 工具函数

```kotlin
import queue_utils.QueueUtils

val queue = CircularQueue<Int>(10)
QueueUtils.enqueueAll(queue, listOf(1, 2, 3, 4, 5))

// 过滤
val evens = QueueUtils.filter(queue) { it % 2 == 0 }

// 映射
val squared = QueueUtils.map(queue) { it * it }

// 归约
val sum = QueueUtils.reduce(queue, 0) { acc, it -> acc + it }

// 查找
val found = QueueUtils.find(queue) { it > 3 }

// 分区
val (less, greater) = QueueUtils.partition(queue) { it < 3 }

// 分组
val groups = QueueUtils.groupBy(queue) { it % 2 }

// 去重
val unique = QueueUtils.distinct(queue)

// 统计
val counts = QueueUtils.countOccurrences(queue)
```

## 📚 API 文档

### CircularQueue<T>

| 方法 | 描述 |
|------|------|
| `enqueue(item: T)` | 入队，返回是否成功 |
| `dequeue(): T?` | 出队 |
| `peek(): T?` | 查看队首 |
| `size: Int` | 当前大小 |
| `isEmpty: Boolean` | 是否为空 |
| `isFull(): Boolean` | 是否已满 |
| `available(): Int` | 剩余容量 |
| `clear()` | 清空队列 |
| `toList(): List<T>` | 转为列表 |

### ThreadSafeQueue<T> (BlockingQueue)

| 方法 | 描述 |
|------|------|
| `put(item: T)` | 阻塞入队（无限等待） |
| `take(): T` | 阻塞出队（无限等待） |
| `offer(item: T, timeoutMs: Long)` | 超时入队 |
| `poll(timeoutMs: Long): T?` | 超时出队 |
| `remainingCapacity(): Int` | 剩余容量 |
| `drainTo(collection, maxElements)` | 批量转移 |

### PriorityAwareQueue<T>

| 方法 | 描述 |
|------|------|
| `enqueue(item: T, priority: Int)` | 按优先级入队 |
| `dequeue(): T?` | 出队最高优先级元素 |
| `peekWithPriority(): Pair<T, Int>?` | 查看队首及优先级 |
| `toListWithPriority(): List<Pair<T, Int>>` | 转为带优先级列表 |

### ArrayDequeImpl<T> (Deque)

| 方法 | 描述 |
|------|------|
| `addFirst(item: T)` | 头部添加 |
| `addLast(item: T)` | 尾部添加 |
| `removeFirst(): T?` | 头部移除 |
| `removeLast(): T?` | 尾部移除 |
| `peekFirst(): T?` | 查看头部 |
| `peekLast(): T?` | 查看尾部 |
| `rotate(n: Int)` | 旋转队列 |

### DelayQueue<T : Delayed>

| 方法 | 描述 |
|------|------|
| `put(item: T)` | 入队延迟元素 |
| `take(): T` | 阻塞等待到期元素 |
| `poll(timeoutMs: Long): T?` | 超时获取到期元素 |
| `peek(): T?` | 查看最早到期元素 |

### QueueUtils 工具函数

| 函数 | 描述 |
|------|------|
| `circular(capacity)` | 创建循环队列 |
| `threadSafe(capacity)` | 创建线程安全队列 |
| `priority(capacity)` | 创建优先级队列 |
| `deque()` | 创建双端队列 |
| `enqueueAll(queue, items)` | 批量入队 |
| `dequeueAll(queue)` | 批量出队 |
| `dequeueN(queue, n)` | 出队指定数量 |
| `contains(queue, item)` | 包含检查 |
| `find(queue, predicate)` | 查找元素 |
| `filter(queue, predicate)` | 过滤元素 |
| `map(queue, transform)` | 映射转换 |
| `reverse(queue)` | 反转队列 |
| `reduce(queue, initial, op)` | 归约 |
| `all(queue, predicate)` | 全部满足检查 |
| `any(queue, predicate)` | 存在满足检查 |
| `merge(q1, q2)` | 合并队列 |
| `partition(queue, predicate)` | 分区 |
| `distinct(queue)` | 去重 |
| `groupBy(queue, keySelector)` | 分组 |
| `countOccurrences(queue)` | 统计出现次数 |

## 🧪 测试

```bash
# 编译并运行测试
kotlinc Kotlin/queue_utils/mod.kt Kotlin/queue_utils/queue_utils_test.kt -include-runtime -d queue_test.jar
java -jar queue_test.jar
```

测试覆盖：
- 循环队列：基本操作、环形特性、容量管理
- 线程安全队列：并发访问、阻塞操作、超时操作
- 优先级队列：优先级排序、负优先级、相同优先级
- 双端队列：两端操作、旋转、边界值
- 延迟队列：延迟到期、超时获取
- 工具函数：所有辅助函数
- 边界值：空队列、单元素、大队列

## 📁 文件结构

```
Kotlin/queue_utils/
├── mod.kt               # 主模块（队列实现）
├── queue_utils_test.kt  # 测试套件
├── README.md            # 文档
└── examples/
    └── usage_examples.kt # 使用示例
```

## 💡 使用场景

1. **消息缓冲** - 循环队列用于固定容量缓冲
2. **任务队列** - 线程安全队列用于生产者-消费者模式
3. **优先级调度** - 优先级队列用于任务调度器
4. **延迟执行** - 延迟队列用于定时任务
5. **滑动窗口** - 双端队列用于滑动窗口算法

## 📄 许可证

MIT License - AllToolkit 项目的一部分

---

**作者**: AllToolkit  
**版本**: 1.0.0  
**日期**: 2026-04-18