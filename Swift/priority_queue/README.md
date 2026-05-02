# PriorityQueue（优先队列/堆）

Swift 实现的优先队列数据结构，支持最小堆和最大堆，零外部依赖。

## 特性

- ✅ **最小堆 / 最大堆** - 两种模式切换
- ✅ **完整 CRUD** - 入队、出队、查询、删除
- ✅ **线程安全版本** - `ConcurrentPriorityQueue`
- ✅ **自定义比较器** - `CustomPriorityQueue`
- ✅ **堆排序算法** - `HeapSort` 工具类
- ✅ **Codable 支持** - 可序列化/反序列化
- ✅ **Equatable/Hashable** - 可比较、可哈希
- ✅ **Collection 协议** - 支持遍历和索引访问

## 快速开始

### 基本使用

```swift
// 创建最小堆（默认）
var minHeap = PriorityQueue<Int>()
minHeap.enqueue(5)
minHeap.enqueue(3)
minHeap.enqueue(8)
minHeap.enqueue(1)

// 出队 - 总是返回最小值
print(minHeap.dequeue())  // 1
print(minHeap.dequeue())  // 3
print(minHeap.dequeue())  // 5
print(minHeap.dequeue())  // 8

// 创建最大堆
var maxHeap = PriorityQueue<Int>(.max)
maxHeap.enqueue(5)
maxHeap.enqueue(3)
maxHeap.enqueue(8)
maxHeap.enqueue(1)

// 出队 - 总是返回最大值
print(maxHeap.dequeue())  // 8
print(maxHeap.dequeue())  // 5
```

### 从数组创建

```swift
// 从数组创建最小堆
let minPQ = PriorityQueue([5, 3, 8, 1, 9], heapType: .min)
print(minPQ.peek)  // 1

// 从数组创建最大堆
let maxPQ = PriorityQueue([5, 3, 8, 1, 9], heapType: .max)
print(maxPQ.peek)  // 9
```

### 工厂方法

```swift
// 使用静态工厂方法
let minHeap = PriorityQueue<Int>.minHeap()
let maxHeap = PriorityQueue<Int>.maxHeap()

let minFromArr = PriorityQueue<Int>.minHeap([3, 1, 4, 1, 5])
let maxFromArr = PriorityQueue<Int>.maxHeap([3, 1, 4, 1, 5])
```

### 数组字面量

```swift
// 使用数组字面量创建（默认最小堆）
let pq: PriorityQueue<Int> = [3, 1, 4, 1, 5]
```

## API 参考

### 属性

| 属性 | 类型 | 描述 |
|------|------|------|
| `count` | `Int` | 元素数量 |
| `isEmpty` | `Bool` | 是否为空 |
| `isNotEmpty` | `Bool` | 是否非空 |
| `peek` | `Element?` | 查看堆顶元素（不移除） |

### 方法

| 方法 | 返回值 | 描述 |
|------|--------|------|
| `enqueue(_:)` | `Bool` | 入队 |
| `push(_:)` | `Bool` | 入队（别名） |
| `dequeue()` | `Element` | 出队（抛出异常） |
| `pop()` | `Element?` | 出队（返回可选值） |
| `popFirst(_:)` | `[Element]` | 出队前 N 个元素 |
| `clear()` | `Void` | 清空队列 |
| `remove(_:)` | `Bool` | 移除指定元素 |
| `remove(at:)` | `Element` | 移除指定索引元素 |
| `contains(_:)` | `Bool` | 检查是否包含 |
| `indexOf(_:)` | `Int?` | 查找元素索引 |
| `sorted()` | `[Element]` | 返回排序数组 |
| `toArray()` | `[Element]` | 转为数组 |

## 高级用法

### 堆排序

```swift
// 升序排序
let asc = HeapSort.ascending([5, 3, 8, 1, 9])
// [1, 3, 5, 8, 9]

// 降序排序
let desc = HeapSort.descending([5, 3, 8, 1, 9])
// [9, 8, 5, 3, 1]

// 查找第 K 大/小
let kthLargest = HeapSort.kthLargest([3, 2, 1, 5, 6, 4], 2)  // 5
let kthSmallest = HeapSort.kthSmallest([3, 2, 1, 5, 6, 4], 3)  // 3

// Top K 元素
let topLargest = HeapSort.topKLargest([3, 2, 1, 5, 6, 4], 3)  // [6, 5, 4]
let topSmallest = HeapSort.topKSmallest([3, 2, 1, 5, 6, 4], 3)  // [1, 2, 3]
```

### 自定义优先级

```swift
// 自定义比较器：偶数优先，同奇偶时按值排序
var customPQ = CustomPriorityQueue<Int>(comparator: { a, b in
    let aEven = a % 2 == 0
    let bEven = b % 2 == 0
    if aEven && !bEven { return true }
    if !aEven && bEven { return false }
    return a < b
})

customPQ.enqueue(3)
customPQ.enqueue(4)
customPQ.enqueue(1)
customPQ.enqueue(2)

print(customPQ.dequeue())  // 2 (偶数最小)
print(customPQ.dequeue())  // 4 (偶数次小)
print(customPQ.dequeue())  // 1 (奇数最小)
print(customPQ.dequeue())  // 3 (奇数次小)
```

### 自定义对象

```swift
struct Task {
    let name: String
    let priority: Int
}

var taskQueue = CustomPriorityQueue<Task>(comparator: { $0.priority > $1.priority })
taskQueue.enqueue(Task(name: "Low", priority: 1))
taskQueue.enqueue(Task(name: "High", priority: 10))
taskQueue.enqueue(Task(name: "Medium", priority: 5))

print(taskQueue.dequeue()?.name)  // "High"
print(taskQueue.dequeue()?.name)  // "Medium"
print(taskQueue.dequeue()?.name)  // "Low"
```

### 线程安全版本

```swift
let concurrentPQ = ConcurrentPriorityQueue<Int>()

// 多线程安全访问
DispatchQueue.concurrentPerform(iterations: 100) { i in
    concurrentPQ.enqueue(i)
}

let batch = concurrentPQ.dequeue(10)  // 批量出队
```

### 序列化

```swift
// 编码
let pq = PriorityQueue([5, 3, 8, 1], heapType: .min)
let data = try JSONEncoder().encode(pq)

// 解码
let decoded = try JSONDecoder().decode(PriorityQueue<Int>.self, from: data)
```

### 遍历

```swift
let pq = PriorityQueue([1, 2, 3, 4, 5])

// 作为 Sequence 遍历
for element in pq {
    print(element)
}

// 作为 Collection 访问
print(pq[pq.startIndex])  // 堆顶元素
```

## 时间复杂度

| 操作 | 时间复杂度 |
|------|------------|
| 入队 (enqueue) | O(log n) |
| 出队 (dequeue) | O(log n) |
| 查看堆顶 (peek) | O(1) |
| 堆化 (heapify) | O(n) |
| 查找 (contains) | O(n) |
| 删除 (remove) | O(n) |

## 典型应用场景

### 1. 任务调度

```swift
struct Task {
    let id: String
    let priority: Int
}

var scheduler = CustomPriorityQueue<Task>(comparator: { $0.priority > $1.priority })
scheduler.enqueue(Task(id: "A", priority: 1))
scheduler.enqueue(Task(id: "B", priority: 10))
scheduler.enqueue(Task(id: "C", priority: 5))

while let task = scheduler.dequeue() {
    print("Executing: \(task.id)")
}
// B, C, A
```

### 2. 合并 K 个有序链表

```swift
func mergeKLists(_ lists: [[Int]]) -> [Int] {
    var minHeap = PriorityQueue<Int>()
    
    for list in lists {
        for val in list {
            minHeap.enqueue(val)
        }
    }
    
    var result: [Int] = []
    while let val = minHeap.pop() {
        result.append(val)
    }
    
    return result
}

let lists = [[1, 4, 5], [1, 3, 4], [2, 6]]
print(mergeKLists(lists))  // [1, 1, 2, 3, 4, 4, 5, 6]
```

### 3. 中位数查找

```swift
class MedianFinder {
    var maxHeap = PriorityQueue<Int>(.max)  // 存储较小的一半
    var minHeap = PriorityQueue<Int>(.min)  // 存储较大的一半
    
    func addNum(_ num: Int) {
        if maxHeap.isEmpty || num <= maxHeap.peek! {
            maxHeap.enqueue(num)
        } else {
            minHeap.enqueue(num)
        }
        
        // 平衡两个堆
        if maxHeap.count > minHeap.count + 1 {
            minHeap.enqueue(maxHeap.pop()!)
        } else if minHeap.count > maxHeap.count {
            maxHeap.enqueue(minHeap.pop()!)
        }
    }
    
    func findMedian() -> Double {
        if maxHeap.count > minHeap.count {
            return Double(maxHeap.peek!)
        }
        return Double(maxHeap.peek! + minHeap.peek!) / 2.0
    }
}
```

### 4. 滑动窗口最大值

```swift
func maxSlidingWindow(_ nums: [Int], _ k: Int) -> [Int] {
    var result: [Int] = []
    var maxHeap = PriorityQueue<(value: Int, index: Int)>(comparator: { $0.value > $1.value })
    
    for i in 0..<nums.count {
        maxHeap.enqueue((nums[i], i))
        
        // 移除窗口外的元素
        while let top = maxHeap.peek, top.index <= i - k {
            _ = maxHeap.pop()
        }
        
        if i >= k - 1 {
            result.append(maxHeap.peek!.value)
        }
    }
    
    return result
}
```

## 测试

运行测试文件：

```bash
swift PriorityQueueTest.swift
```

测试覆盖：
- ✅ 基本入队/出队操作
- ✅ 最小堆/最大堆模式
- ✅ 空队列处理
- ✅ 元素查找/删除
- ✅ 批量操作
- ✅ 堆排序算法
- ✅ 自定义比较器
- ✅ 线程安全测试
- ✅ 序列化/反序列化
- ✅ 边界情况（单元素、重复、负数）
- ✅ 性能测试（10000 次操作）

## 文件结构

```
priority_queue/
├── mod.swift              # 主要实现
├── PriorityQueueTest.swift # 测试套件
├── README.md              # 本文档
└── examples/
    └── example.swift      # 使用示例
```

## 许可证

MIT License