// PriorityQueueTest.swift
// 优先队列（堆）测试套件
// 零外部依赖，纯 Swift 实现

import Foundation

// 测试结果追踪
struct TestResult {
    var passed = 0
    var failed = 0
    var errors: [String] = []
    
    mutating func pass(_ name: String) {
        passed += 1
        print("✅ \(name)")
    }
    
    mutating func fail(_ name: String, _ reason: String) {
        failed += 1
        errors.append("\(name): \(reason)")
        print("❌ \(name) - \(reason)")
    }
}

var result = TestResult()

// MARK: - PriorityQueue Tests

print("=" * 60)
print("PriorityQueue Tests")
print("=" * 60)

// Test 1: 基本入队出队（最小堆）
do {
    var pq = PriorityQueue<Int>()
    pq.enqueue(5)
    pq.enqueue(3)
    pq.enqueue(8)
    pq.enqueue(1)
    
    let first = try pq.dequeue()
    let second = try pq.dequeue()
    let third = try pq.dequeue()
    let fourth = try pq.dequeue()
    
    if first == 1 && second == 3 && third == 5 && fourth == 8 {
        result.pass("MinHeap Basic Enqueue/Dequeue")
    } else {
        result.fail("MinHeap Basic Enqueue/Dequeue", "Wrong order: \(first), \(second), \(third), \(fourth)")
    }
} catch {
    result.fail("MinHeap Basic Enqueue/Dequeue", error.localizedDescription)
}

// Test 2: 基本入队出队（最大堆）
do {
    var pq = PriorityQueue<Int>(.max)
    pq.enqueue(5)
    pq.enqueue(3)
    pq.enqueue(8)
    pq.enqueue(1)
    
    let first = try pq.dequeue()
    let second = try pq.dequeue()
    let third = try pq.dequeue()
    let fourth = try pq.dequeue()
    
    if first == 8 && second == 5 && third == 3 && fourth == 1 {
        result.pass("MaxHeap Basic Enqueue/Dequeue")
    } else {
        result.fail("MaxHeap Basic Enqueue/Dequeue", "Wrong order: \(first), \(second), \(third), \(fourth)")
    }
} catch {
    result.fail("MaxHeap Basic Enqueue/Dequeue", error.localizedDescription)
}

// Test 3: 从数组创建
do {
    let pq = PriorityQueue([5, 3, 8, 1, 9, 2], heapType: .min)
    
    if pq.count == 6 && pq.peek == 1 {
        result.pass("Create from Array")
    } else {
        result.fail("Create from Array", "count: \(pq.count), peek: \(pq.peek ?? -1)")
    }
} catch {
    result.fail("Create from Array", error.localizedDescription)
}

// Test 4: 空队列操作
do {
    var pq = PriorityQueue<Int>()
    
    if !pq.isEmpty {
        result.fail("Empty Check", "Should be empty")
    } else if pq.peek != nil {
        result.fail("Empty Check", "Peek should be nil")
    } else if pq.pop() != nil {
        result.fail("Empty Check", "Pop should be nil")
    } else {
        result.pass("Empty Queue Operations")
    }
} catch {
    result.fail("Empty Queue Operations", error.localizedDescription)
}

// Test 5: Peek 不移除元素
do {
    var pq = PriorityQueue([3, 1, 2])
    let firstPeek = pq.peek
    let secondPeek = pq.peek
    
    if firstPeek == 1 && secondPeek == 1 && pq.count == 3 {
        result.pass("Peek Does Not Remove")
    } else {
        result.fail("Peek Does Not Remove", "peek: \(firstPeek ?? -1), count: \(pq.count)")
    }
} catch {
    result.fail("Peek Does Not Remove", error.localizedDescription)
}

// Test 6: Count 和 isEmpty
do {
    var pq = PriorityQueue<Int>()
    
    if pq.count != 0 || !pq.isEmpty {
        result.fail("Count/IsEmpty", "Initial state wrong")
    } else {
        pq.enqueue(1)
        pq.enqueue(2)
        
        if pq.count != 2 || pq.isEmpty {
            result.fail("Count/IsEmpty", "After enqueue wrong")
        } else {
            _ = pq.pop()
            _ = pq.pop()
            
            if pq.count != 0 || !pq.isEmpty {
                result.fail("Count/IsEmpty", "After dequeue wrong")
            } else {
                result.pass("Count and IsEmpty")
            }
        }
    }
} catch {
    result.fail("Count and IsEmpty", error.localizedDescription)
}

// Test 7: Contains
do {
    let pq = PriorityQueue([5, 3, 8, 1])
    
    if pq.contains(3) && pq.contains(8) && !pq.contains(100) {
        result.pass("Contains")
    } else {
        result.fail("Contains", "Wrong contains results")
    }
} catch {
    result.fail("Contains", error.localizedDescription)
}

// Test 8: IndexOf
do {
    let pq = PriorityQueue([5, 3, 8, 1])
    
    if let idx = pq.indexOf(5), idx >= 0 && idx < pq.count {
        result.pass("IndexOf")
    } else {
        result.fail("IndexOf", "Index not found or invalid")
    }
} catch {
    result.fail("IndexOf", error.localizedDescription)
}

// Test 9: Remove
do {
    var pq = PriorityQueue([5, 3, 8, 1, 9])
    let removed = pq.remove(8)
    
    if removed && pq.count == 4 && !pq.contains(8) {
        result.pass("Remove Element")
    } else {
        result.fail("Remove Element", "removed: \(removed), count: \(pq.count)")
    }
} catch {
    result.fail("Remove Element", error.localizedDescription)
}

// Test 10: Clear
do {
    var pq = PriorityQueue([1, 2, 3, 4, 5])
    pq.clear()
    
    if pq.isEmpty && pq.count == 0 {
        result.pass("Clear")
    } else {
        result.fail("Clear", "count: \(pq.count)")
    }
} catch {
    result.fail("Clear", error.localizedDescription)
}

// Test 11: Pop First N
do {
    var pq = PriorityQueue([5, 3, 8, 1, 9, 2], heapType: .min)
    let first3 = pq.popFirst(3)
    
    if first3 == [1, 2, 3] && pq.count == 3 {
        result.pass("Pop First N")
    } else {
        result.fail("Pop First N", "first3: \(first3), remaining: \(pq.count)")
    }
} catch {
    result.fail("Pop First N", error.localizedDescription)
}

// Test 12: To Array
do {
    let pq = PriorityQueue([5, 3, 8, 1])
    let arr = pq.toArray()
    
    if arr.count == 4 && arr.contains(5) && arr.contains(1) {
        result.pass("ToArray")
    } else {
        result.fail("ToArray", "array: \(arr)")
    }
} catch {
    result.fail("ToArray", error.localizedDescription)
}

// Test 13: Sorted
do {
    let pq = PriorityQueue([5, 3, 8, 1, 9, 2], heapType: .min)
    let sorted = pq.sorted()
    
    if sorted == [1, 2, 3, 5, 8, 9] {
        result.pass("Sorted")
    } else {
        result.fail("Sorted", "result: \(sorted)")
    }
} catch {
    result.fail("Sorted", error.localizedDescription)
}

// Test 14: Push Alias
do {
    var pq = PriorityQueue<Int>()
    pq.push(1)
    pq.push(2)
    
    if pq.count == 2 {
        result.pass("Push Alias")
    } else {
        result.fail("Push Alias", "count: \(pq.count)")
    }
} catch {
    result.fail("Push Alias", error.localizedDescription)
}

// Test 15: Factory Methods
do {
    let minPQ = PriorityQueue<Int>.minHeap()
    let maxPQ = PriorityQueue<Int>.maxHeap()
    
    let minPQ2 = PriorityQueue<Int>.minHeap([3, 1, 2])
    let maxPQ2 = PriorityQueue<Int>.maxHeap([3, 1, 2])
    
    if minPQ.isEmpty && maxPQ.isEmpty && minPQ2.peek == 1 && maxPQ2.peek == 3 {
        result.pass("Factory Methods")
    } else {
        result.fail("Factory Methods", "minPQ: \(minPQ.isEmpty), maxPQ: \(maxPQ.isEmpty)")
    }
} catch {
    result.fail("Factory Methods", error.localizedDescription)
}

// Test 16: String Type
do {
    var pq = PriorityQueue<String>()
    pq.enqueue("charlie")
    pq.enqueue("alpha")
    pq.enqueue("bravo")
    
    let first = try pq.dequeue()
    let second = try pq.dequeue()
    let third = try pq.dequeue()
    
    if first == "alpha" && second == "bravo" && third == "charlie" {
        result.pass("String Type MinHeap")
    } else {
        result.fail("String Type MinHeap", "order: \(first), \(second), \(third)")
    }
} catch {
    result.fail("String Type MinHeap", error.localizedDescription)
}

// Test 17: Double Type
do {
    var pq = PriorityQueue<Double>(.max)
    pq.enqueue(3.14)
    pq.enqueue(2.71)
    pq.enqueue(1.41)
    
    let first = try pq.dequeue()
    
    if first == 3.14 {
        result.pass("Double Type MaxHeap")
    } else {
        result.fail("Double Type MaxHeap", "first: \(first)")
    }
} catch {
    result.fail("Double Type MaxHeap", error.localizedDescription)
}

// Test 18: Large Scale Test
do {
    var pq = PriorityQueue<Int>()
    let count = 1000
    
    // 入队随机数
    for i in 0..<count {
        pq.enqueue(i)
    }
    
    // 验证出队顺序
    var prev = -1
    var valid = true
    while !pq.isEmpty {
        guard let current = pq.pop() else { valid = false; break }
        if current < prev { valid = false; break }
        prev = current
    }
    
    if valid {
        result.pass("Large Scale (1000 elements)")
    } else {
        result.fail("Large Scale (1000 elements)", "Order validation failed")
    }
} catch {
    result.fail("Large Scale (1000 elements)", error.localizedDescription)
}

// Test 19: Sequence Conformance
do {
    let pq = PriorityQueue([1, 2, 3, 4, 5])
    var sum = 0
    for element in pq {
        sum += element
    }
    
    if sum == 15 {
        result.pass("Sequence Conformance")
    } else {
        result.fail("Sequence Conformance", "sum: \(sum)")
    }
} catch {
    result.fail("Sequence Conformance", error.localizedDescription)
}

// Test 20: Collection Conformance
do {
    let pq = PriorityQueue([5, 3, 8, 1])
    
    if pq.count == 4 && pq[pq.startIndex] == pq.peek {
        result.pass("Collection Conformance")
    } else {
        result.fail("Collection Conformance", "count: \(pq.count)")
    }
} catch {
    result.fail("Collection Conformance", error.localizedDescription)
}

// Test 21: Array Literal
do {
    let pq: PriorityQueue<Int> = [3, 1, 4, 1, 5]
    
    if pq.count == 5 {
        result.pass("Array Literal Initialization")
    } else {
        result.fail("Array Literal Initialization", "count: \(pq.count)")
    }
} catch {
    result.fail("Array Literal Initialization", error.localizedDescription)
}

// Test 22: Description
do {
    let pq = PriorityQueue([1, 2, 3])
    let desc = pq.description
    
    if desc.contains("MinHeap") && desc.contains("[") {
        result.pass("CustomStringConvertible")
    } else {
        result.fail("CustomStringConvertible", "description: \(desc)")
    }
} catch {
    result.fail("CustomStringConvertible", error.localizedDescription)
}

// MARK: - HeapSort Tests

print("\n" + "=" * 60)
print("HeapSort Tests")
print("=" * 60)

// Test 23: HeapSort Ascending
do {
    let arr = [5, 3, 8, 1, 9, 2, 7, 4, 6]
    let sorted = HeapSort.ascending(arr)
    
    if sorted == [1, 2, 3, 4, 5, 6, 7, 8, 9] {
        result.pass("HeapSort Ascending")
    } else {
        result.fail("HeapSort Ascending", "result: \(sorted)")
    }
} catch {
    result.fail("HeapSort Ascending", error.localizedDescription)
}

// Test 24: HeapSort Descending
do {
    let arr = [5, 3, 8, 1, 9, 2, 7, 4, 6]
    let sorted = HeapSort.descending(arr)
    
    if sorted == [9, 8, 7, 6, 5, 4, 3, 2, 1] {
        result.pass("HeapSort Descending")
    } else {
        result.fail("HeapSort Descending", "result: \(sorted)")
    }
} catch {
    result.fail("HeapSort Descending", error.localizedDescription)
}

// Test 25: Kth Largest
do {
    let arr = [3, 2, 1, 5, 6, 4]
    let kthLargest = HeapSort.kthLargest(arr, 2)
    
    if kthLargest == 5 {
        result.pass("Kth Largest")
    } else {
        result.fail("Kth Largest", "result: \(kthLargest ?? -1)")
    }
} catch {
    result.fail("Kth Largest", error.localizedDescription)
}

// Test 26: Kth Smallest
do {
    let arr = [3, 2, 1, 5, 6, 4]
    let kthSmallest = HeapSort.kthSmallest(arr, 3)
    
    if kthSmallest == 3 {
        result.pass("Kth Smallest")
    } else {
        result.fail("Kth Smallest", "result: \(kthSmallest ?? -1)")
    }
} catch {
    result.fail("Kth Smallest", error.localizedDescription)
}

// Test 27: Top K Largest
do {
    let arr = [3, 2, 1, 5, 6, 4]
    let topK = HeapSort.topKLargest(arr, 3)
    
    if topK == [6, 5, 4] {
        result.pass("Top K Largest")
    } else {
        result.fail("Top K Largest", "result: \(topK)")
    }
} catch {
    result.fail("Top K Largest", error.localizedDescription)
}

// Test 28: Top K Smallest
do {
    let arr = [3, 2, 1, 5, 6, 4]
    let topK = HeapSort.topKSmallest(arr, 3)
    
    if topK == [1, 2, 3] {
        result.pass("Top K Smallest")
    } else {
        result.fail("Top K Smallest", "result: \(topK)")
    }
} catch {
    result.fail("Top K Smallest", error.localizedDescription)
}

// MARK: - CustomPriorityQueue Tests

print("\n" + "=" * 60)
print("CustomPriorityQueue Tests")
print("=" * 60)

// Test 29: Custom Comparator
do {
    // 自定义：偶数优先于奇数，同奇偶时按值排序
    var pq = CustomPriorityQueue<Int>(comparator: { a, b in
        let aEven = a % 2 == 0
        let bEven = b % 2 == 0
        if aEven && !bEven { return true }
        if !aEven && bEven { return false }
        return a < b
    })
    
    pq.enqueue(3)
    pq.enqueue(4)
    pq.enqueue(1)
    pq.enqueue(2)
    
    let first = pq.dequeue()
    let second = pq.dequeue()
    let third = pq.dequeue()
    let fourth = pq.dequeue()
    
    // 偶数优先，同奇偶按值排
    if first == 2 && second == 4 && third == 1 && fourth == 3 {
        result.pass("Custom Comparator")
    } else {
        result.fail("Custom Comparator", "order: \(first ?? -1), \(second ?? -1), \(third ?? -1), \(fourth ?? -1)")
    }
} catch {
    result.fail("Custom Comparator", error.localizedDescription)
}

// Test 30: Custom with Objects
do {
    struct Task {
        let name: String
        let priority: Int
    }
    
    var pq = CustomPriorityQueue<Task>(comparator: { $0.priority > $1.priority })
    pq.enqueue(Task(name: "Low", priority: 1))
    pq.enqueue(Task(name: "High", priority: 10))
    pq.enqueue(Task(name: "Medium", priority: 5))
    
    let first = pq.dequeue()
    
    if first?.priority == 10 && first?.name == "High" {
        result.pass("Custom with Struct Objects")
    } else {
        result.fail("Custom with Struct Objects", "priority: \(first?.priority ?? -1)")
    }
} catch {
    result.fail("Custom with Struct Objects", error.localizedDescription)
}

// MARK: - ConcurrentPriorityQueue Tests

print("\n" + "=" * 60)
print("ConcurrentPriorityQueue Tests")
print("=" * 60)

// Test 31: Thread-Safe Basic Operations
do {
    let pq = ConcurrentPriorityQueue<Int>()
    
    pq.enqueue(5)
    pq.enqueue(3)
    pq.enqueue(8)
    pq.enqueue(1)
    
    let first = pq.dequeue()
    let second = pq.dequeue()
    
    if first == 1 && second == 3 && pq.count == 2 {
        result.pass("Concurrent Basic Operations")
    } else {
        result.fail("Concurrent Basic Operations", "first: \(first ?? -1), second: \(second ?? -1)")
    }
} catch {
    result.fail("Concurrent Basic Operations", error.localizedDescription)
}

// Test 32: Concurrent Access
do {
    let pq = ConcurrentPriorityQueue<Int>()
    let iterations = 100
    var success = true
    
    // 并发写入
    DispatchQueue.concurrentPerform(iterations: iterations) { i in
        pq.enqueue(i)
    }
    
    // 并发读取
    DispatchQueue.concurrentPerform(iterations: iterations / 2) { _ in
        _ = pq.dequeue()
    }
    
    // 验证最终状态一致
    if pq.count == iterations - iterations / 2 {
        result.pass("Concurrent Access")
    } else {
        result.fail("Concurrent Access", "count: \(pq.count), expected: \(iterations - iterations / 2)")
    }
} catch {
    result.fail("Concurrent Access", error.localizedDescription)
}

// Test 33: Batch Operations
do {
    let pq = ConcurrentPriorityQueue<Int>()
    pq.enqueue([5, 3, 8, 1])
    
    let batch = pq.dequeue(2)
    
    if batch == [1, 3] && pq.count == 2 {
        result.pass("Concurrent Batch Operations")
    } else {
        result.fail("Concurrent Batch Operations", "batch: \(batch)")
    }
} catch {
    result.fail("Concurrent Batch Operations", error.localizedDescription)
}

// MARK: - Codable Tests

print("\n" + "=" * 60)
print("Codable Tests")
print("=" * 60)

// Test 34: Encode/Decode MinHeap
do {
    let original = PriorityQueue([5, 3, 8, 1], heapType: .min)
    let data = try JSONEncoder().encode(original)
    let decoded = try JSONDecoder().decode(PriorityQueue<Int>.self, from: data)
    
    if decoded.count == 4 && decoded.peek == 1 {
        result.pass("Codable MinHeap")
    } else {
        result.fail("Codable MinHeap", "count: \(decoded.count), peek: \(decoded.peek ?? -1)")
    }
} catch {
    result.fail("Codable MinHeap", error.localizedDescription)
}

// Test 35: Encode/Decode MaxHeap
do {
    let original = PriorityQueue([5, 3, 8, 1], heapType: .max)
    let data = try JSONEncoder().encode(original)
    let decoded = try JSONDecoder().decode(PriorityQueue<Int>.self, from: data)
    
    if decoded.count == 4 && decoded.peek == 8 {
        result.pass("Codable MaxHeap")
    } else {
        result.fail("Codable MaxHeap", "count: \(decoded.count), peek: \(decoded.peek ?? -1)")
    }
} catch {
    result.fail("Codable MaxHeap", error.localizedDescription)
}

// MARK: - Equatable Tests

print("\n" + "=" * 60)
print("Equatable Tests")
print("=" * 60)

// Test 36: Equality
do {
    let pq1 = PriorityQueue([1, 2, 3])
    let pq2 = PriorityQueue([1, 2, 3])
    let pq3 = PriorityQueue([1, 2, 3, 4])
    let pq4 = PriorityQueue([1, 2, 3], heapType: .max)
    
    if pq1 == pq2 && pq1 != pq3 && pq1 != pq4 {
        result.pass("Equatable")
    } else {
        result.fail("Equatable", "Equality comparison failed")
    }
} catch {
    result.fail("Equatable", error.localizedDescription)
}

// MARK: - Edge Cases Tests

print("\n" + "=" * 60)
print("Edge Cases Tests")
print("=" * 60)

// Test 37: Single Element
do {
    var pq = PriorityQueue<Int>()
    pq.enqueue(42)
    
    if pq.count == 1 && pq.peek == 42 {
        let elem = try pq.dequeue()
        if elem == 42 && pq.isEmpty {
            result.pass("Single Element")
        } else {
            result.fail("Single Element", "Dequeue failed")
        }
    } else {
        result.fail("Single Element", "Enqueue failed")
    }
} catch {
    result.fail("Single Element", error.localizedDescription)
}

// Test 38: Duplicate Elements
do {
    var pq = PriorityQueue<Int>()
    pq.enqueue(5)
    pq.enqueue(5)
    pq.enqueue(5)
    
    let first = try pq.dequeue()
    let second = try pq.dequeue()
    let third = try pq.dequeue()
    
    if first == 5 && second == 5 && third == 5 && pq.isEmpty {
        result.pass("Duplicate Elements")
    } else {
        result.fail("Duplicate Elements", "Elements: \(first), \(second), \(third)")
    }
} catch {
    result.fail("Duplicate Elements", error.localizedDescription)
}

// Test 39: Negative Numbers
do {
    var pq = PriorityQueue<Int>()
    pq.enqueue(-5)
    pq.enqueue(3)
    pq.enqueue(-10)
    pq.enqueue(0)
    
    let first = try pq.dequeue()
    let second = try pq.dequeue()
    
    if first == -10 && second == -5 {
        result.pass("Negative Numbers")
    } else {
        result.fail("Negative Numbers", "first: \(first), second: \(second)")
    }
} catch {
    result.fail("Negative Numbers", error.localizedDescription)
}

// Test 40: Remove at Index
do {
    var pq = PriorityQueue([5, 3, 8, 1, 9])
    
    // 找到元素8的索引并移除
    if let idx = pq.indexOf(8) {
        let removed = try pq.remove(at: idx)
        if removed == 8 && !pq.contains(8) && pq.count == 4 {
            result.pass("Remove at Index")
        } else {
            result.fail("Remove at Index", "removed: \(removed)")
        }
    } else {
        result.fail("Remove at Index", "Index not found")
    }
} catch {
    result.fail("Remove at Index", error.localizedDescription)
}

// MARK: - Performance Test

print("\n" + "=" * 60)
print("Performance Test")
print("=" * 60)

// Test 41: Large Scale Performance
do {
    let startTime = Date()
    var pq = PriorityQueue<Int>()
    let count = 10000
    
    for i in 0..<count {
        pq.enqueue(Int.random(in: 0..<100000))
    }
    
    while !pq.isEmpty {
        _ = pq.pop()
    }
    
    let elapsed = Date().timeIntervalSince(startTime) * 1000
    
    if elapsed < 5000 {  // 应该在5秒内完成
        result.pass("Performance (10000 ops in \(String(format: "%.2f", elapsed))ms)")
    } else {
        result.fail("Performance", "Too slow: \(elapsed)ms")
    }
} catch {
    result.fail("Performance", error.localizedDescription)
}

// MARK: - Summary

print("\n" + "=" * 60)
print("Test Summary")
print("=" * 60)
print("✅ Passed: \(result.passed)")
print("❌ Failed: \(result.failed)")
print("📊 Total:  \(result.passed + result.failed)")

if !result.errors.isEmpty {
    print("\nFailed Tests:")
    for error in result.errors {
        print("  • \(error)")
    }
}

print("\n" + "=" * 60)

// Exit with appropriate code
exit(result.failed > 0 ? 1 : 0)

// Helper extension
extension String {
    static func *(lhs: String, rhs: Int) -> String {
        return String(repeating: lhs, count: rhs)
    }
}