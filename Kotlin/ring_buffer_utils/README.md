# Ring Buffer - 环形缓冲区工具模块

[![Kotlin](https://img.shields.io/badge/Kotlin-1.9+-purple.svg)](https://kotlinlang.org/)
[![License](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

一个高效的固定大小循环缓冲区实现，零外部依赖，纯 Kotlin 实现。

## 特性

- **O(1) 时间复杂度** - 入队、出队操作都是常数时间
- **线程安全选项** - 可选的线程安全模式，支持并发访问
- **阻塞版本** - `BlockingRingBuffer` 支持生产者-消费者模式
- **泛型支持** - 可存储任意类型元素
- **丰富的 API** - 迭代、过滤、查找、索引访问等
- **覆盖模式** - 可选择满时覆盖或拒绝写入

## 适用场景

- 日志系统（保留最近 N 条记录）
- 事件流处理
- 音频/视频缓冲
- 滑动窗口计算
- 撤销/重做历史
- 生产者-消费者队列

## 快速开始

### 基本使用

```kotlin
import ring_buffer_utils.RingBuffer

fun main() {
    // 创建容量为 5 的环形缓冲区
    val buffer = RingBuffer<Int>(5)
    
    // 添加元素
    buffer.push(1)
    buffer.push(2)
    buffer.push(3)
    
    // 查看元素
    println(buffer.peek())      // 1 (最老)
    println(buffer.peekLast())  // 3 (最新)
    
    // 取出元素 (FIFO)
    println(buffer.pop())  // 1
    println(buffer.pop())  // 2
    
    // 检查状态
    println(buffer.size)       // 1
    println(buffer.isEmpty())  // false
    println(buffer.isFull())   // false
}
```

### 覆盖模式

```kotlin
val buffer = RingBuffer<Int>(3)
buffer.overwriteMode = true  // 默认为 true

buffer.push(1)
buffer.push(2)
buffer.push(3)
buffer.push(4)  // 覆盖 1

println(buffer.toList())  // [2, 3, 4]
```

### 批量操作

```kotlin
val buffer = RingBuffer<Int>(10)

// 批量添加
buffer.pushAll(listOf(1, 2, 3, 4, 5))

// 转换为列表
val list = buffer.toList()

// 获取最近/最早的元素
val last3 = buffer.takeLast(3)
val first3 = buffer.takeFirst(3)
```

### 查询和过滤

```kotlin
val buffer = RingBuffer<Int>(10)
buffer.pushAll((1..10).toList())

// 查找元素
val found = buffer.find { it > 5 }  // 6

// 过滤元素
val evens = buffer.filter { it % 2 == 0 }  // [2, 4, 6, 8, 10]

// 包含检查
buffer.contains(5)  // true
```

### 线程安全

```kotlin
val buffer = RingBuffer<Int>(100, threadSafe = true)

// 现在可以安全地在多线程环境中使用
Thread { buffer.push(1) }.start()
Thread { buffer.pop() }.start()
```

### 阻塞环形缓冲区

```kotlin
import ring_buffer_utils.BlockingRingBuffer

val buffer = BlockingRingBuffer<Int>(10)

// 生产者线程
Thread {
    buffer.put(42)  // 如果满则阻塞
}.start()

// 消费者线程
Thread {
    val item = buffer.take()  // 如果空则阻塞
}.start()
```

### 扩展函数

```kotlin
import ring_buffer_utils.toRingBuffer
import ring_buffer_utils.emptyRingBuffer

// 从列表创建
val buffer = listOf(1, 2, 3).toRingBuffer()

// 创建空缓冲区
val empty = emptyRingBuffer<String>(10)
```

## API 参考

### RingBuffer<T>

#### 构造函数

| 参数 | 类型 | 默认值 | 描述 |
|------|------|--------|------|
| capacity | Int | - | 缓冲区容量 |
| threadSafe | Boolean | false | 是否线程安全 |

#### 属性

| 属性 | 类型 | 描述 |
|------|------|------|
| size | Int | 当前元素数量 |
| capacity | Int | 缓冲区容量 |
| overwriteMode | Boolean | 满时是否覆盖 |

#### 方法

| 方法 | 返回类型 | 描述 |
|------|----------|------|
| push(element) | Boolean | 添加元素 |
| pop() | T? | 取出最老元素 |
| peek() | T? | 查看最老元素 |
| peekLast() | T? | 查看最新元素 |
| isFull() | Boolean | 是否已满 |
| isEmpty() | Boolean | 是否为空 |
| available() | Int | 剩余空间 |
| clear() | Unit | 清空缓冲区 |
| toList() | List\<T\> | 转换为列表 |
| get(index) | T | 索引访问 |
| contains(element) | Boolean | 包含检查 |
| find(predicate) | T? | 查找元素 |
| filter(predicate) | List\<T\> | 过滤元素 |
| takeFirst(n) | List\<T\> | 获取前 n 个 |
| takeLast(n) | List\<T\> | 获取后 n 个 |

### BlockingRingBuffer<T>

| 方法 | 描述 |
|------|------|
| put(element) | 添加元素（满时阻塞） |
| take() | 取出元素（空时阻塞） |
| offer(element) | 尝试添加（立即返回） |
| poll() | 尝试取出（立即返回） |

## 文件结构

```
ring_buffer_utils/
├── RingBuffer.kt          # 主要实现
├── RingBufferTest.kt      # 单元测试
├── RingBufferExample.kt   # 使用示例
└── README.md              # 文档
```

## 运行测试

```bash
# 使用 kotlinc 编译
kotlinc RingBuffer.kt -include-runtime -d RingBuffer.jar

# 使用 Gradle
./gradlew test

# 使用 Maven
mvn test
```

## 运行示例

```bash
kotlinc RingBuffer.kt RingBufferExample.kt -include-runtime -d example.jar
kotlin -jar example.jar
```

## 性能特点

- **入队 (push)**: O(1)
- **出队 (pop)**: O(1)
- **索引访问**: O(1)
- **查找**: O(n)
- **内存占用**: O(capacity)

## 许可证

MIT License

## 作者

AllToolkit Auto-Generator