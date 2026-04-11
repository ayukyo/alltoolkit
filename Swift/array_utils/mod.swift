/**
 * AllToolkit - Swift Array Utilities
 *
 * 通用数组/集合工具类，提供常用的数组处理、转换、统计和搜索功能。
 * 零依赖，仅使用 Swift 标准库。
 * 支持 iOS 13.0+, macOS 10.15+, watchOS 6.0+, tvOS 13.0+
 *
 * @author AllToolkit
 * @version 1.0.0
 */

import Foundation

// MARK: - Array 扩展

public extension Array {
    
    // MARK: 空值与安全访问
    
    /**
     * 检查数组是否为空
     *
     * @return true 如果数组为空
     */
    var isEmpty: Bool {
        return self.count == 0
    }
    
    /**
     * 检查数组是否不为空
     *
     * @return true 如果数组有元素
     */
    var isNotEmpty: Bool {
        return !isEmpty
    }
    
    /**
     * 安全地获取第一个元素
     *
     * @return 第一个元素，如果数组为空则返回 nil
     */
    var firstSafe: Element? {
        return self.first
    }
    
    /**
     * 安全地获取最后一个元素
     *
     * @return 最后一个元素，如果数组为空则返回 nil
     */
    var lastSafe: Element? {
        return self.last
    }
    
    /**
     * 安全地获取指定索引的元素
     *
     * @param index 索引位置
     * @return 元素，如果索引越界则返回 nil
     */
    func safeGet(at index: Int) -> Element? {
        guard index >= 0, index < self.count else { return nil }
        return self[index]
    }
    
    /**
     * 获取第一个元素或默认值
     *
     * @param defaultValue 默认值
     * @return 第一个元素或默认值
     */
    func firstOr(_ defaultValue: Element) -> Element {
        return self.first ?? defaultValue
    }
    
    // MARK: 切片操作
    
    /**
     * 获取前 n 个元素
     *
     * @param count 元素数量
     * @return 前 n 个元素组成的数组
     */
    func take(_ count: Int) -> [Element] {
        guard count > 0 else { return [] }
        return Array(self.prefix(count))
    }
    
    /**
     * 跳过前 n 个元素
     *
     * @param count 跳过的元素数量
     * @return 剩余元素组成的数组
     */
    func skip(_ count: Int) -> [Element] {
        guard count > 0 else { return self }
        return Array(self.dropFirst(count))
    }
    
    /**
     * 获取后 n 个元素
     *
     * @param count 元素数量
     * @return 后 n 个元素组成的数组
     */
    func takeLast(_ count: Int) -> [Element] {
        guard count > 0 else { return [] }
        return Array(self.suffix(count))
    }
    
    /**
     * 获取指定范围的元素
     *
     * @param start 起始索引（包含）
     * @param end 结束索引（不包含）
     * @return 范围内的元素组成的数组
     */
    func slice(from start: Int, to end: Int) -> [Element] {
        guard start >= 0, end <= self.count, start < end else { return [] }
        return Array(self[start..<end])
    }
    
    // MARK: 去重与过滤
    
    /**
     * 去除重复元素（要求元素符合 Hashable）
     *
     * @return 去重后的数组
     */
    func unique<T: Hashable>() -> [Element] {
        guard let elements = self as? [T] else { return self }
        var seen = Set<T>()
        return elements.filter { seen.insert($0).inserted } as! [Element]
    }
    
    /**
     * 根据条件过滤元素
     *
     * @param predicate 过滤条件
     * @return 符合条件的元素组成的数组
     */
    func filterNot(_ predicate: (Element) -> Bool) -> [Element] {
        return self.filter { !predicate($0) }
    }
    
    /**
     * 移除 nil 值（要求元素为 Optional 类型）
     *
     * @return 非 nil 元素组成的数组
     */
    func compacted<T>() -> [T] {
        return self.compactMap { $0 as? T }
    }
    
    // MARK: 转换与映射
    
    /**
     * 映射并过滤 nil 值
     *
     * @param transform 转换函数
     * @return 转换后的非 nil 元素组成的数组
     */
    func compactMapNotNull<T>(_ transform: (Element) -> T?) -> [T] {
        return self.compactMap(transform)
    }
    
    /**
     * 扁平化嵌套数组（要求元素为数组类型）
     *
     * @return 扁平化后的数组
     */
    func flattened<T>() -> [T] {
        var result: [T] = []
        for element in self {
            if let array = element as? [T] {
                result.append(contentsOf: array)
            }
        }
        return result
    }
    
    /**
     * 深度扁平化嵌套数组
     *
     * @return 完全扁平化后的数组
     */
    func flattenedDeep<T>() -> [T] {
        var result: [T] = []
        for element in self {
            if let array = element as? [T] {
                result.append(contentsOf: array.flattenedDeep())
            } else if let value = element as? T {
                result.append(value)
            }
        }
        return result
    }
    
    // MARK: 统计与聚合
    
    /**
     * 计算元素总和（要求元素为 Numeric）
     *
     * @return 总和
     */
    func sum<T: Numeric>() -> T {
        guard let numbers = self as? [T] else { return 0 as! T }
        return numbers.reduce(0, +)
    }
    
    /**
     * 计算平均值（要求元素为 BinaryFloatingPoint）
     *
     * @return 平均值，如果数组为空则返回 0
     */
    func average<T: BinaryFloatingPoint>() -> T {
        guard let numbers = self as? [T], !numbers.isEmpty else { return 0 }
        return numbers.reduce(0, +) / T(numbers.count)
    }
    
    /**
     * 获取最大值（要求元素为 Comparable）
     *
     * @return 最大值，如果数组为空则返回 nil
     */
    func max<T: Comparable>() -> T? {
        guard let elements = self as? [T], !elements.isEmpty else { return nil }
        return elements.max()
    }
    
    /**
     * 获取最小值（要求元素为 Comparable）
     *
     * @return 最小值，如果数组为空则返回 nil
     */
    func min<T: Comparable>() -> T? {
        guard let elements = self as? [T], !elements.isEmpty else { return nil }
        return elements.min()
    }
    
    // MARK: 搜索与查找
    
    /**
     * 查找第一个符合条件的元素索引
     *
     * @param predicate 查找条件
     * @return 索引，如果未找到则返回 nil
     */
    func index(where predicate: (Element) -> Bool) -> Int? {
        for (index, element) in self.enumerated() {
            if predicate(element) {
                return index
            }
        }
        return nil
    }
    
    /**
     * 检查是否包含符合条件的元素
     *
     * @param predicate 检查条件
     * @return true 如果存在符合条件的元素
     */
    func contains(where predicate: (Element) -> Bool) -> Bool {
        return self.contains(where: predicate)
    }
    
    /**
     * 查找所有符合条件的元素
     *
     * @param predicate 查找条件
     * @return 符合条件的元素组成的数组
     */
    func findAll(where predicate: (Element) -> Bool) -> [Element] {
        return self.filter(predicate)
    }
    
    // MARK: 分组与分区
    
    /**
     * 按条件分组
     *
     * @param keySelector 分组键选择器
     * @return 分组后的字典
     */
    func groupBy<K: Hashable>(_ keySelector: (Element) -> K) -> [K: [Element]] {
        var groups: [K: [Element]] = [:]
        for element in self {
            let key = keySelector(element)
            if groups[key] == nil {
                groups[key] = []
            }
            groups[key]?.append(element)
        }
        return groups
    }
    
    /**
     * 按条件分区
     *
     * @param predicate 分区条件
     * @return (符合条件的元素，不符合条件的元素) 元组
     */
    func partition(by predicate: (Element) -> Bool) -> ([Element], [Element]) {
        var matches: [Element] = []
        var nonMatches: [Element] = []
        for element in self {
            if predicate(element) {
                matches.append(element)
            } else {
                nonMatches.append(element)
            }
        }
        return (matches, nonMatches)
    }
    
    // MARK: 排序
    
    /**
     * 按指定键排序
     *
     * @param keySelector 排序键选择器
     * @param ascending 是否升序
     * @return 排序后的数组
     */
    func sortBy<T: Comparable>(_ keySelector: (Element) -> T, ascending: Bool = true) -> [Element] {
        return self.sorted {
            ascending ? keySelector($0) < keySelector($1) : keySelector($0) > keySelector($1)
        }
    }
    
    // MARK: 组合与连接
    
    /**
     * 与另一个数组合并
     *
     * @param other 另一个数组
     * @return 合并后的数组
     */
    func concat(_ other: [Element]) -> [Element] {
        return self + other
    }
    
    /**
     * 用指定分隔符连接元素（要求元素为 CustomStringConvertible）
     *
     * @param separator 分隔符
     * @return 连接后的字符串
     */
    func join<S: StringProtocol>(separator: S = ", ") -> String {
        return self.map { String(describing: $0) }.joined(separator: separator)
    }
    
    // MARK: 随机与打乱
    
    /**
     * 随机获取一个元素
     *
     * @return 随机元素，如果数组为空则返回 nil
     */
    func randomElement() -> Element? {
        guard !isEmpty else { return nil }
        return self.randomElement()
    }
    
    /**
     * 随机获取 n 个不重复元素
     *
     * @param count 元素数量
     * @return 随机元素组成的数组
     */
    func sample(_ count: Int) -> [Element] {
        guard count > 0 else { return [] }
        guard count < self.count else { return self.shuffled() }
        var result: [Element] = []
        var indices = Set(0..<self.count)
        for _ in 0..<count {
            guard let randomIndex = indices.randomElement() else { break }
            indices.remove(randomIndex)
            result.append(self[randomIndex])
        }
        return result
    }
}

// MARK: - Array 扩展 (Element: Comparable)

public extension Array where Element: Comparable {
    
    /**
     * 检查数组是否已排序（升序）
     *
     * @return true 如果数组已升序排序
     */
    var isSortedAscending: Bool {
        for i in 1..<self.count {
            if self[i] < self[i - 1] {
                return false
            }
        }
        return true
    }
    
    /**
     * 检查数组是否已排序（降序）
     *
     * @return true 如果数组已降序排序
     */
    var isSortedDescending: Bool {
        for i in 1..<self.count {
            if self[i] > self[i - 1] {
                return false
            }
        }
        return true
    }
    
    /**
     * 获取中位数
     *
     * @return 中位数，如果数组为空则返回 nil
     */
    var median: Element? {
        guard !isEmpty else { return nil }
        let sorted = self.sorted()
        let mid = sorted.count / 2
        if sorted.count % 2 == 0 {
            return sorted[mid - 1] < sorted[mid] ? sorted[mid - 1] : sorted[mid]
        }
        return sorted[mid]
    }
}

// MARK: - Array 扩展 (Element: Hashable)

public extension Array where Element: Hashable {
    
    /**
     * 去除重复元素
     *
     * @return 去重后的数组
     */
    var unique: [Element] {
        var seen = Set<Element>()
        return self.filter { seen.insert($0).inserted }
    }
    
    /**
     * 获取重复的元素
     *
     * @return 重复元素组成的数组
     */
    var duplicates: [Element] {
        var seen = Set<Element>()
        var duplicates = Set<Element>()
        for element in self {
            if !seen.insert(element).inserted {
                duplicates.insert(element)
            }
        }
        return Array(duplicates)
    }
    
    /**
     * 检查是否有重复元素
     *
     * @return true 如果有重复元素
     */
    var hasDuplicates: Bool {
        let set = Set(self)
        return set.count != self.count
    }
}

// MARK: - Array 扩展 (Element: Numeric)

public extension Array where Element: Numeric {
    
    /**
     * 计算元素总和
     *
     * @return 总和
     */
    var sum: Element {
        return self.reduce(0, +)
    }
    
    /**
     * 计算乘积
     *
     * @return 乘积
     */
    var product: Element {
        return self.reduce(1, *)
    }
}

// MARK: - Array 扩展 (Element: BinaryFloatingPoint)

public extension Array where Element: BinaryFloatingPoint {
    
    /**
     * 计算平均值
     *
     * @return 平均值，如果数组为空则返回 0
     */
    var average: Element {
        guard !isEmpty else { return 0 }
        return self.reduce(0, +) / Element(count)
    }
    
    /**
     * 计算标准差
     *
     * @return 标准差
     */
    var standardDeviation: Element {
        guard count > 1 else { return 0 }
        let avg = average
        let variance = self.map { pow($0 - avg, 2) }.average
        return sqrt(variance)
    }
}

// MARK: - 工具函数

/**
 * 创建指定范围的数组
 *
 * @param start 起始值
 * @param end 结束值（不包含）
 * @param step 步长
 * @return 范围内的数组
 */
public func range<T: Strideable>(_ start: T, _ end: T, step: T.Stride = 1) -> [T] {
    var result: [T] = []
    var current = start
    while current < end {
        result.append(current)
        current = current.advanced(by: step)
    }
    return result
}

/**
 * 创建等差数列
 *
 * @param start 起始值
 * @param count 元素数量
 * @param step 公差
 * @return 等差数列
 */
public func arithmeticSequence<T: Numeric & Comparable>(_ start: T, count: Int, step: T) -> [T] {
    var result: [T] = []
    var current = start
    for _ in 0..<count {
        result.append(current)
        current = current + step
    }
    return result
}

/**
 * 创建等比数列
 *
 * @param start 起始值
 * @param count 元素数量
 * @param ratio 公比
 * @return 等比数列
 */
public func geometricSequence<T: BinaryFloatingPoint>(_ start: T, count: Int, ratio: T) -> [T] {
    var result: [T] = []
    var current = start
    for _ in 0..<count {
        result.append(current)
        current = current * ratio
    }
    return result
}

/**
 * 合并多个数组
 *
 * @param arrays 多个数组
 * @return 合并后的数组
 */
public func merge<T>(_ arrays: [T]...) -> [T] {
    return arrays.flatMap { $0 }
}

/**
 * 交错合并两个数组
 *
 * @param array1 第一个数组
 * @param array2 第二个数组
 * @return 交错合并后的数组
 */
public func interleave<T>(_ array1: [T], _ array2: [T]) -> [T] {
    var result: [T] = []
    let count = max(array1.count, array2.count)
    for i in 0..<count {
        if i < array1.count {
            result.append(array1[i])
        }
        if i < array2.count {
            result.append(array2[i])
        }
    }
    return result
}

/**
 * 转置二维数组
 *
 * @param matrix 二维数组
 * @return 转置后的二维数组
 */
public func transpose<T>(_ matrix: [[T]]) -> [[T]] {
    guard let firstRow = matrix.first, !firstRow.isEmpty else { return [] }
    let columns = firstRow.count
    var result: [[T]] = []
    for col in 0..<columns {
        var newRow: [T] = []
        for row in matrix {
            if col < row.count {
                newRow.append(row[col])
            }
        }
        result.append(newRow)
    }
    return result
}

/**
 * 创建填充数组
 *
 * @param count 元素数量
 * @param value 填充值
 * @return 填充后的数组
 */
public func filled<T>(count: Int, with value: T) -> [T] {
    return Array(repeating: value, count: count)
}

/**
 * 创建递增数组
 *
 * @param count 元素数量
 * @param start 起始值
 * @return 递增数组
 */
public func incrementingArray(count: Int, start: Int = 0) -> [Int] {
    return Array(start..<(start + count))
}
