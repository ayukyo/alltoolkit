// PriorityQueue 示例代码
// 展示优先队列的各种使用场景

import Foundation

print("=" * 60)
print("PriorityQueue 使用示例")
print("=" * 60)

// MARK: - 示例 1: 基本操作

print("\n【示例 1】基本操作")
print("-" * 40)

var minHeap = PriorityQueue<Int>()
print("创建空的最小堆: \(minHeap)")

minHeap.enqueue(5)
minHeap.enqueue(3)
minHeap.enqueue(8)
minHeap.enqueue(1)
minHeap.enqueue(9)
print("入队 5, 3, 8, 1, 9: \(minHeap)")

print("peek: \(minHeap.peek!)")
print("count: \(minHeap.count)")

while let val = minHeap.pop() {
    print("出队: \(val)")
}

// MARK: - 示例 2: 最大堆

print("\n【示例 2】最大堆 - 任务优先级")
print("-" * 40)

struct Task: Comparable {
    let name: String
    let priority: Int
    
    static func < (lhs: Task, rhs: Task) -> Bool {
        return lhs.priority < rhs.priority
    }
}

var taskQueue = PriorityQueue<Task>(.max)
taskQueue.enqueue(Task(name: "写报告", priority: 3))
taskQueue.enqueue(Task(name: "修复Bug", priority: 10))
taskQueue.enqueue(Task(name: "代码审查", priority: 5))
taskQueue.enqueue(Task(name: "紧急部署", priority: 20))

print("任务按优先级执行:")
while let task = taskQueue.pop() {
    print("  [优先级 \(task.priority)] \(task.name)")
}

// MARK: - 示例 3: 堆排序

print("\n【示例 3】堆排序")
print("-" * 40)

let unsorted = [64, 34, 25, 12, 22, 11, 90]
print("原始数组: \(unsorted)")

let ascending = HeapSort.ascending(unsorted)
print("升序排序: \(ascending)")

let descending = HeapSort.descending(unsorted)
print("降序排序: \(descending)")

// MARK: - 示例 4: Top K 问题

print("\n【示例 4】Top K 问题")
print("-" * 40)

let scores = [95, 87, 92, 78, 88, 96, 82, 91, 85, 90]
print("成绩: \(scores)")

let top3 = HeapSort.topKLargest(scores, 3)
print("前三名: \(top3)")

let bottom3 = HeapSort.topKSmallest(scores, 3)
print("后三名: \(bottom3)")

let kthLargest = HeapSort.kthLargest(scores, 3)!
print("第三高分: \(kthLargest)")

// MARK: - 示例 5: 合并有序数组

print("\n【示例 5】合并有序数组")
print("-" * 40)

func mergeSortedArrays(_ arrays: [[Int]]) -> [Int] {
    var minHeap = PriorityQueue<Int>()
    
    for arr in arrays {
        for val in arr {
            minHeap.enqueue(val)
        }
    }
    
    var result: [Int] = []
    result.reserveCapacity(minHeap.count)
    
    while let val = minHeap.pop() {
        result.append(val)
    }
    
    return result
}

let sortedArrays = [[1, 4, 7], [2, 5, 8], [3, 6, 9]]
print("输入: \(sortedArrays)")
let merged = mergeSortedArrays(sortedArrays)
print("合并结果: \(merged)")

// MARK: - 示例 6: 滑动窗口中位数

print("\n【示例 6】滑动窗口中位数")
print("-" * 40)

class SlidingWindowMedian {
    private var maxHeap = PriorityQueue<Int>(.max)  // 较小的一半
    private var minHeap = PriorityQueue<Int>(.min)  // 较大的一半
    
    func findMedians(_ nums: [Int], windowSize: Int) -> [Double] {
        var result: [Double] = []
        
        for i in 0..<nums.count {
            addNumber(nums[i])
            
            if i >= windowSize {
                removeNumber(nums[i - windowSize])
                balance()
            }
            
            if i >= windowSize - 1 {
                result.append(getMedian())
            }
        }
        
        return result
    }
    
    private func addNumber(_ num: Int) {
        if maxHeap.isEmpty || num <= maxHeap.peek! {
            maxHeap.enqueue(num)
        } else {
            minHeap.enqueue(num)
        }
        balance()
    }
    
    private func removeNumber(_ num: Int) {
        if num <= maxHeap.peek! {
            _ = maxHeap.remove(num)
        } else {
            _ = minHeap.remove(num)
        }
    }
    
    private func balance() {
        if maxHeap.count > minHeap.count + 1 {
            minHeap.enqueue(maxHeap.pop()!)
        } else if minHeap.count > maxHeap.count {
            maxHeap.enqueue(minHeap.pop()!)
        }
    }
    
    private func getMedian() -> Double {
        if maxHeap.count > minHeap.count {
            return Double(maxHeap.peek!)
        }
        return Double(maxHeap.peek! + minHeap.peek!) / 2.0
    }
}

let nums = [1, 3, -1, -3, 5, 3, 6, 7]
let windowSize = 3
let medianFinder = SlidingWindowMedian()
let medians = medianFinder.findMedians(nums, windowSize: windowSize)
print("数组: \(nums)")
print("窗口大小: \(windowSize)")
print("中位数: \(medians)")

// MARK: - 示例 7: 数据流第 K 大元素

print("\n【示例 7】数据流第 K 大元素")
print("-" * 40)

class KthLargest {
    private var minHeap = PriorityQueue<Int>()
    private let k: Int
    
    init(_ k: Int, _ nums: [Int]) {
        self.k = k
        for num in nums {
            add(num)
        }
    }
    
    func add(_ val: Int) -> Int {
        minHeap.enqueue(val)
        if minHeap.count > k {
            _ = minHeap.pop()
        }
        return minHeap.peek!
    }
}

let kthLargestObj = KthLargest(3, [4, 5, 8, 2])
print("初始数组 [4,5,8,2]，K=3")
print("添加 3: 第3大 = \(kthLargestObj.add(3))")
print("添加 5: 第3大 = \(kthLargestObj.add(5))")
print("添加 10: 第3大 = \(kthLargestObj.add(10))")
print("添加 9: 第3大 = \(kthLargestObj.add(9))")
print("添加 4: 第3大 = \(kthLargestObj.add(4))")

// MARK: - 示例 8: 自定义比较器 - 按字符串长度

print("\n【示例 8】自定义比较器 - 字符串长度优先")
print("-" * 40)

var lengthPQ = CustomPriorityQueue<String>(comparator: { $0.count > $1.count })
lengthPQ.enqueue("Hello")
lengthPQ.enqueue("World")
lengthPQ.enqueue("Swift")
lengthPQ.enqueue("PriorityQueue")
lengthPQ.enqueue("Hi")

print("按字符串长度降序出队:")
while let str = lengthPQ.dequeue() {
    print("  [长度 \(str.count)] \(str)")
}

// MARK: - 示例 9: 线程安全队列 - 并发任务处理

print("\n【示例 9】线程安全队列 - 并发处理")
print("-" * 40)

let concurrentQueue = ConcurrentPriorityQueue<Int>()

// 模拟并发入队
DispatchQueue.concurrentPerform(iterations: 100) { i in
    concurrentQueue.enqueue(i)
}

print("并发入队 100 个数字")
print("队列大小: \(concurrentQueue.count)")

// 出队前 10 个
let top10 = concurrentQueue.dequeue(10)
print("最小的 10 个数字: \(top10)")

// MARK: - 示例 10: 序列化

print("\n【示例 10】序列化 - JSON 编解码")
print("-" * 40)

let original = PriorityQueue([10, 20, 5, 15, 30], heapType: .min)
print("原始队列: \(original)")

let encoder = JSONEncoder()
encoder.outputFormatting = .prettyPrinted
let jsonData = try encoder.encode(original)
let jsonString = String(data: jsonData, encoding: .utf8)!
print("JSON 编码: \(jsonString)")

let decoder = JSONDecoder()
let decoded = try decoder.decode(PriorityQueue<Int>.self, from: jsonData)
print("解码后: \(decoded)")

// MARK: - 示例 11: 数组字面量初始化

print("\n【示例 11】数组字面量初始化")
print("-" * 40)

let pqLiteral: PriorityQueue<Int> = [3, 1, 4, 1, 5, 9, 2, 6]
print("使用数组字面量创建: \(pqLiteral)")

// MARK: - 示例 12: 集合操作

print("\n【示例 12】集合操作")
print("-" * 40)

let pq = PriorityQueue([5, 3, 8, 1, 9])
print("队列: \(pq)")
print("包含 3: \(pq.contains(3))")
print("包含 100: \(pq.contains(100))")

if let index = pq.indexOf(8) {
    print("元素 8 的索引: \(index)")
}

print("转为数组: \(pq.toArray())")
print("排序输出: \(pq.sorted())")

print("\n" + "=" * 60)
print("示例完成")
print("=" * 60)

// Helper extension
extension String {
    static func *(lhs: String, rhs: Int) -> String {
        return String(repeating: lhs, count: rhs)
    }
}