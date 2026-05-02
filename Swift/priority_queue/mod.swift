// PriorityQueue.swift
// 优先队列（堆）实现 - 支持最小堆和最大堆
// 零外部依赖，纯 Swift 实现

import Foundation

// MARK: - PriorityQueueError

/// 优先队列错误类型
public enum PriorityQueueError: Error, LocalizedError {
    case empty
    case indexOutOfRange
    
    public var errorDescription: String? {
        switch self {
        case .empty:
            return "PriorityQueue is empty"
        case .indexOutOfRange:
            return "Index out of range"
        }
    }
}

// MARK: - HeapType

/// 堆类型
public enum HeapType {
    case min  // 最小堆
    case max  // 最大堆
}

// MARK: - PriorityQueue

/// 优先队列 - 基于二叉堆实现
/// 支持最小堆和最大堆两种模式
public struct PriorityQueue<Element: Comparable> {
    
    // MARK: - Properties
    
    /// 内部存储数组
    private var heap: [Element]
    
    /// 堆类型
    private let heapType: HeapType
    
    /// 比较函数
    private var compare: (Element, Element) -> Bool {
        switch heapType {
        case .min:
            return <  // 最小堆：父节点小于子节点
        case .max:
            return >  // 最大堆：父节点大于子节点
        }
    }
    
    /// 队列元素数量
    public var count: Int {
        return heap.count
    }
    
    /// 队列是否为空
    public var isEmpty: Bool {
        return heap.isEmpty
    }
    
    /// 队列是否非空
    public var isNotEmpty: Bool {
        return !heap.isEmpty
    }
    
    /// 获取堆顶元素（不移除）
    public var peek: Element? {
        return heap.first
    }
    
    // MARK: - Initialization
    
    /// 创建空优先队列
    /// - Parameter heapType: 堆类型，默认最小堆
    public init(_ heapType: HeapType = .min) {
        self.heap = []
        self.heapType = heapType
    }
    
    /// 从数组创建优先队列
    /// - Parameters:
    ///   - elements: 初始元素数组
    ///   - heapType: 堆类型，默认最小堆
    public init(_ elements: [Element], heapType: HeapType = .min) {
        self.heap = elements
        self.heapType = heapType
        heapify()
    }
    
    /// 从序列创建优先队列
    /// - Parameters:
    ///   - elements: 初始元素序列
    ///   - heapType: 堆类型，默认最小堆
    public init<S: Sequence>(_ elements: S, heapType: HeapType = .min) where S.Element == Element {
        self.heap = Array(elements)
        self.heapType = heapType
        heapify()
    }
    
    // MARK: - Heap Operations
    
    /// 堆化 - 将数组调整为堆
    private mutating func heapify() {
        // 从最后一个非叶子节点开始，自底向上调整
        for i in stride(from: (heap.count / 2) - 1, through: 0, by: -1) {
            siftDown(from: i)
        }
    }
    
    /// 上浮操作
    /// - Parameter index: 需要上浮的元素索引
    private mutating func siftUp(from index: Int) {
        var childIndex = index
        let child = heap[childIndex]
        var parentIndex = (childIndex - 1) / 2
        
        while childIndex > 0 && compare(child, heap[parentIndex]) {
            heap[childIndex] = heap[parentIndex]
            childIndex = parentIndex
            parentIndex = (childIndex - 1) / 2
        }
        
        heap[childIndex] = child
    }
    
    /// 下沉操作
    /// - Parameter index: 需要下沉的元素索引
    private mutating func siftDown(from index: Int) {
        var parentIndex = index
        
        while true {
            let leftChildIndex = 2 * parentIndex + 1
            let rightChildIndex = 2 * parentIndex + 2
            var candidateIndex = parentIndex
            
            // 找到子节点中优先级最高的
            if leftChildIndex < heap.count && compare(heap[leftChildIndex], heap[candidateIndex]) {
                candidateIndex = leftChildIndex
            }
            
            if rightChildIndex < heap.count && compare(heap[rightChildIndex], heap[candidateIndex]) {
                candidateIndex = rightChildIndex
            }
            
            if candidateIndex == parentIndex {
                return
            }
            
            heap.swapAt(parentIndex, candidateIndex)
            parentIndex = candidateIndex
        }
    }
    
    // MARK: - Public Methods
    
    /// 入队
    /// - Parameter element: 要添加的元素
    @discardableResult
    public mutating func enqueue(_ element: Element) -> Bool {
        heap.append(element)
        siftUp(from: heap.count - 1)
        return true
    }
    
    /// 入队（push 别名）
    /// - Parameter element: 要添加的元素
    @discardableResult
    public mutating func push(_ element: Element) -> Bool {
        return enqueue(element)
    }
    
    /// 出队
    /// - Returns: 堆顶元素
    /// - Throws: 队列为空时抛出 PriorityQueueError.empty
    public mutating func dequeue() throws -> Element {
        guard !heap.isEmpty else {
            throw PriorityQueueError.empty
        }
        
        if heap.count == 1 {
            return heap.removeFirst()
        }
        
        let result = heap[0]
        heap[0] = heap.removeLast()
        siftDown(from: 0)
        
        return result
    }
    
    /// 出队（pop 别名）
    /// - Returns: 堆顶元素，队列为空返回 nil
    public mutating func pop() -> Element? {
        return try? dequeue()
    }
    
    /// 移除并返回前 N 个元素
    /// - Parameter n: 元素数量
    /// - Returns: 排序后的元素数组
    public mutating func popFirst(_ n: Int) -> [Element] {
        let count = min(n, heap.count)
        var result: [Element] = []
        result.reserveCapacity(count)
        
        for _ in 0..<count {
            if let element = pop() {
                result.append(element)
            }
        }
        
        return result
    }
    
    /// 清空队列
    public mutating func clear() {
        heap.removeAll(keepingCapacity: false)
    }
    
    /// 移除指定元素
    /// - Parameter element: 要移除的元素
    /// - Returns: 是否成功移除
    @discardableResult
    public mutating func remove(_ element: Element) -> Bool {
        guard let index = heap.firstIndex(of: element) else {
            return false
        }
        return remove(at: index) != nil
    }
    
    /// 移除指定索引的元素
    /// - Parameter index: 元素索引
    /// - Returns: 被移除的元素
    /// - Throws: 索引越界时抛出 PriorityQueueError.indexOutOfRange
    public mutating func remove(at index: Int) throws -> Element {
        guard index >= 0 && index < heap.count else {
            throw PriorityQueueError.indexOutOfRange
        }
        
        if index == heap.count - 1 {
            return heap.removeLast()
        }
        
        let removed = heap[index]
        heap[index] = heap.removeLast()
        
        // 需要判断是上浮还是下沉
        let parentIndex = (index - 1) / 2
        if index > 0 && compare(heap[index], heap[parentIndex]) {
            siftUp(from: index)
        } else {
            siftDown(from: index)
        }
        
        return removed
    }
    
    /// 检查是否包含指定元素
    /// - Parameter element: 要查找的元素
    /// - Returns: 是否包含
    public func contains(_ element: Element) -> Bool {
        return heap.contains(element)
    }
    
    /// 查找指定元素的索引
    /// - Parameter element: 要查找的元素
    /// - Returns: 元素索引，不存在返回 nil
    public func indexOf(_ element: Element) -> Int? {
        return heap.firstIndex(of: element)
    }
    
    /// 将队列转换为排序数组（不移除元素）
    /// - Returns: 排序后的数组
    public func sorted() -> [Element] {
        return heap.sorted(usingComparator())
    }
    
    /// 将队列转换为数组
    /// - Returns: 元素数组（堆顺序）
    public func toArray() -> [Element] {
        return heap
    }
    
    // MARK: - Private Helpers
    
    /// 获取比较器
    private func usingComparator() -> (Element, Element) -> Bool {
        switch heapType {
        case .min:
            return (<)
        case .max:
            return (>)
        }
    }
    
    // MARK: - Static Factory Methods
    
    /// 创建最小堆
    public static func minHeap() -> PriorityQueue {
        return PriorityQueue(.min)
    }
    
    /// 创建最大堆
    public static func maxHeap() -> PriorityQueue {
        return PriorityQueue(.max)
    }
    
    /// 从数组创建最小堆
    public static func minHeap(_ elements: [Element]) -> PriorityQueue {
        return PriorityQueue(elements, heapType: .min)
    }
    
    /// 从数组创建最大堆
    public static func maxHeap(_ elements: [Element]) -> PriorityQueue {
        return PriorityQueue(elements, heapType: .max)
    }
}

// MARK: - Sequence Conformance

extension PriorityQueue: Sequence {
    public typealias Iterator = IndexingIterator<[Element]>
    
    public func makeIterator() -> Iterator {
        return heap.makeIterator()
    }
}

// MARK: - Collection Conformance

extension PriorityQueue: Collection {
    public typealias Index = Int
    
    public var startIndex: Index { return heap.startIndex }
    public var endIndex: Index { return heap.endIndex }
    
    public subscript(position: Index) -> Element {
        return heap[position]
    }
    
    public func index(after i: Index) -> Index {
        return heap.index(after: i)
    }
}

// MARK: - ExpressibleByArrayLiteral

extension PriorityQueue: ExpressibleByArrayLiteral {
    public init(arrayLiteral elements: Element...) {
        self.init(elements, heapType: .min)
    }
}

// MARK: - CustomStringConvertible

extension PriorityQueue: CustomStringConvertible {
    public var description: String {
        let typeStr = heapType == .min ? "MinHeap" : "MaxHeap"
        return "\(typeStr)(\(heap))"
    }
}

// MARK: - Equatable (where Element: Equatable)

extension PriorityQueue: Equatable where Element: Equatable {
    public static func == (lhs: PriorityQueue, rhs: PriorityQueue) -> Bool {
        guard lhs.heapType == rhs.heapType else { return false }
        return lhs.heap == rhs.heap
    }
}

// MARK: - Hashable (where Element: Hashable)

extension PriorityQueue: Hashable where Element: Hashable {
    public func hash(into hasher: inout Hasher) {
        hasher.combine(heapType)
        hasher.combine(heap)
    }
}

// MARK: - Codable (where Element: Codable)

extension PriorityQueue: Codable where Element: Codable {
    private enum CodingKeys: String, CodingKey {
        case heap
        case heapType
    }
    
    public init(from decoder: Decoder) throws {
        let container = try decoder.container(keyedBy: CodingKeys.self)
        self.heap = try container.decode([Element].self, forKey: .heap)
        
        let typeString = try container.decode(String.self, forKey: .heapType)
        self.heapType = typeString == "max" ? .max : .min
        
        heapify()
    }
    
    public func encode(to encoder: Encoder) throws {
        var container = encoder.container(keyedBy: CodingKeys.self)
        try container.encode(heap, forKey: .heap)
        try container.encode(heapType == .max ? "max" : "min", forKey: .heapType)
    }
}

// MARK: - HeapSort Algorithm

/// 堆排序算法
public struct HeapSort {
    
    /// 堆排序（升序）
    /// - Parameter array: 待排序数组
    /// - Returns: 排序后的数组
    public static func ascending<T: Comparable>(_ array: [T]) -> [T] {
        var pq = PriorityQueue(array, heapType: .max)
        var result: [T] = []
        result.reserveCapacity(array.count)
        
        while let element = pq.pop() {
            result.append(element)
        }
        
        return result
    }
    
    /// 堆排序（降序）
    /// - Parameter array: 待排序数组
    /// - Returns: 排序后的数组
    public static func descending<T: Comparable>(_ array: [T]) -> [T] {
        var pq = PriorityQueue(array, heapType: .min)
        var result: [T] = []
        result.reserveCapacity(array.count)
        
        while let element = pq.pop() {
            result.append(element)
        }
        
        return result
    }
    
    /// 原地堆排序（升序）
    /// - Parameter array: 待排序数组（会被修改）
    public static func sortAscending<T: Comparable>(_ array: inout [T]) {
        array = ascending(array)
    }
    
    /// 原地堆排序（降序）
    /// - Parameter array: 待排序数组（会被修改）
    public static func sortDescending<T: Comparable>(_ array: inout [T]) {
        array = descending(array)
    }
    
    /// 查找数组中第 K 大的元素
    /// - Parameters:
    ///   - array: 源数组
    ///   - k: 第 K 大
    /// - Returns: 第 K 大的元素
    public static func kthLargest<T: Comparable>(_ array: [T], _ k: Int) -> T? {
        guard k > 0 && k <= array.count else { return nil }
        
        var pq = PriorityQueue(array, heapType: .min)
        
        // 维护一个大小为 k 的最小堆
        var heap: [T] = []
        for element in array {
            heap.append(element)
            // 自定义最小堆逻辑
            heap.sort()
            if heap.count > k {
                heap.removeFirst()
            }
        }
        
        return heap.first
    }
    
    /// 查找数组中第 K 小的元素
    /// - Parameters:
    ///   - array: 源数组
    ///   - k: 第 K 小
    /// - Returns: 第 K 小的元素
    public static func kthSmallest<T: Comparable>(_ array: [T], _ k: Int) -> T? {
        guard k > 0 && k <= array.count else { return nil }
        
        var pq = PriorityQueue(array, heapType: .max)
        
        // 维护一个大小为 k 的最大堆
        var heap: [T] = []
        for element in array {
            heap.append(element)
            heap.sort(by: >)
            if heap.count > k {
                heap.removeFirst()
            }
        }
        
        return heap.first
    }
    
    /// 获取数组中前 K 大的元素
    /// - Parameters:
    ///   - array: 源数组
    ///   - k: 元素数量
    /// - Returns: 前 K 大的元素数组（降序）
    public static func topKLargest<T: Comparable>(_ array: [T], _ k: Int) -> [T] {
        guard k > 0 else { return [] }
        
        var result: [T] = []
        var pq = PriorityQueue(array, heapType: .max)
        
        for _ in 0..<min(k, array.count) {
            if let element = pq.pop() {
                result.append(element)
            }
        }
        
        return result
    }
    
    /// 获取数组中前 K 小的元素
    /// - Parameters:
    ///   - array: 源数组
    ///   - k: 元素数量
    /// - Returns: 前 K 小的元素数组（升序）
    public static func topKSmallest<T: Comparable>(_ array: [T], _ k: Int) -> [T] {
        guard k > 0 else { return [] }
        
        var result: [T] = []
        var pq = PriorityQueue(array, heapType: .min)
        
        for _ in 0..<min(k, array.count) {
            if let element = pq.pop() {
                result.append(element)
            }
        }
        
        return result
    }
}

// MARK: - PriorityQueue with Custom Comparator

/// 支持自定义比较器的优先队列
public struct CustomPriorityQueue<Element> {
    private var heap: [Element]
    private let comparator: (Element, Element) -> Bool
    
    /// 元素数量
    public var count: Int { heap.count }
    
    /// 是否为空
    public var isEmpty: Bool { heap.isEmpty }
    
    /// 堆顶元素
    public var peek: Element? { heap.first }
    
    /// 创建自定义优先队列
    /// - Parameters:
    ///   - elements: 初始元素
    ///   - comparator: 比较器，返回 true 表示第一个元素优先级更高
    public init(_ elements: [Element] = [], comparator: @escaping (Element, Element) -> Bool) {
        self.heap = elements
        self.comparator = comparator
        heapify()
    }
    
    /// 从序列创建
    public init<S: Sequence>(_ elements: S, comparator: @escaping (Element, Element) -> Bool) where S.Element == Element {
        self.heap = Array(elements)
        self.comparator = comparator
        heapify()
    }
    
    private mutating func heapify() {
        for i in stride(from: (heap.count / 2) - 1, through: 0, by: -1) {
            siftDown(from: i)
        }
    }
    
    private mutating func siftUp(from index: Int) {
        var childIndex = index
        let child = heap[childIndex]
        var parentIndex = (childIndex - 1) / 2
        
        while childIndex > 0 && comparator(child, heap[parentIndex]) {
            heap[childIndex] = heap[parentIndex]
            childIndex = parentIndex
            parentIndex = (childIndex - 1) / 2
        }
        
        heap[childIndex] = child
    }
    
    private mutating func siftDown(from index: Int) {
        var parentIndex = index
        
        while true {
            let leftChildIndex = 2 * parentIndex + 1
            let rightChildIndex = 2 * parentIndex + 2
            var candidateIndex = parentIndex
            
            if leftChildIndex < heap.count && comparator(heap[leftChildIndex], heap[candidateIndex]) {
                candidateIndex = leftChildIndex
            }
            
            if rightChildIndex < heap.count && comparator(heap[rightChildIndex], heap[candidateIndex]) {
                candidateIndex = rightChildIndex
            }
            
            if candidateIndex == parentIndex {
                return
            }
            
            heap.swapAt(parentIndex, candidateIndex)
            parentIndex = candidateIndex
        }
    }
    
    /// 入队
    @discardableResult
    public mutating func enqueue(_ element: Element) -> Bool {
        heap.append(element)
        siftUp(from: heap.count - 1)
        return true
    }
    
    /// 出队
    public mutating func dequeue() -> Element? {
        guard !heap.isEmpty else { return nil }
        
        if heap.count == 1 {
            return heap.removeFirst()
        }
        
        let result = heap[0]
        heap[0] = heap.removeLast()
        siftDown(from: 0)
        
        return result
    }
    
    /// 清空
    public mutating func clear() {
        heap.removeAll()
    }
    
    /// 转为数组
    public func toArray() -> [Element] {
        return heap
    }
}

// MARK: - Thread-Safe PriorityQueue Wrapper

import Foundation

/// 线程安全的优先队列
public final class ConcurrentPriorityQueue<Element: Comparable> {
    private var queue: PriorityQueue<Element>
    private let lock = NSLock()
    
    /// 元素数量
    public var count: Int {
        lock.lock()
        defer { lock.unlock() }
        return queue.count
    }
    
    /// 是否为空
    public var isEmpty: Bool {
        lock.lock()
        defer { lock.unlock() }
        return queue.isEmpty
    }
    
    /// 堆顶元素
    public var peek: Element? {
        lock.lock()
        defer { lock.unlock() }
        return queue.peek
    }
    
    /// 创建线程安全优先队列
    public init(_ heapType: HeapType = .min) {
        self.queue = PriorityQueue(heapType)
    }
    
    /// 从数组创建
    public init(_ elements: [Element], heapType: HeapType = .min) {
        self.queue = PriorityQueue(elements, heapType: heapType)
    }
    
    /// 入队
    @discardableResult
    public func enqueue(_ element: Element) -> Bool {
        lock.lock()
        defer { lock.unlock() }
        return queue.enqueue(element)
    }
    
    /// 出队
    public func dequeue() -> Element? {
        lock.lock()
        defer { lock.unlock() }
        return queue.pop()
    }
    
    /// 清空
    public func clear() {
        lock.lock()
        defer { lock.unlock() }
        queue.clear()
    }
    
    /// 批量入队
    public func enqueue(_ elements: [Element]) {
        lock.lock()
        defer { lock.unlock() }
        for element in elements {
            _ = queue.enqueue(element)
        }
    }
    
    /// 批量出队
    public func dequeue(_ count: Int) -> [Element] {
        lock.lock()
        defer { lock.unlock() }
        return queue.popFirst(count)
    }
}