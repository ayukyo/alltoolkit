/**
 * Array Utils - Basic Usage Examples
 * 
 * 演示数组工具类的基本用法
 */

import Foundation

// 导入模块（如果在同一项目）
// import AllToolkitArrayUtils

print("=" .padding(toLength: 60, withPad: "=", startingAt: 0))
print("ARRAY UTILS - BASIC USAGE EXAMPLES")
print("=" .padding(toLength: 60, withPad: "=", startingAt: 0))

// -----------------------------------------------------------------------------
// 1. 安全访问
// -----------------------------------------------------------------------------
print("\n1. SAFE ACCESS")
print("-" .padding(toLength: 40, withPad: "-", startingAt: 0))

let numbers = [1, 2, 3, 4, 5]
let empty: [Int] = []

print("Array: \(numbers)")
print("First: \(numbers.firstSafe ?? -1)")
print("Last: \(numbers.lastSafe ?? -1)")
print("Safe get at 2: \(numbers.safeGet(at: 2) ?? -1)")
print("Safe get at 10: \(numbers.safeGet(at: 10) ?? -1) (nil, no crash!)")
print("First or default: \(empty.firstOr(999))")

// -----------------------------------------------------------------------------
// 2. 切片操作
// -----------------------------------------------------------------------------
print("\n2. SLICE OPERATIONS")
print("-" .padding(toLength: 40, withPad: "-", startingAt: 0))

let data = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]

print("Original: \(data)")
print("Take 3:   \(data.take(3))")
print("Skip 3:   \(data.skip(3))")
print("Last 3:   \(data.takeLast(3))")
print("Slice 2-5: \(data.slice(from: 2, to: 5))")

// -----------------------------------------------------------------------------
// 3. 去重与过滤
// -----------------------------------------------------------------------------
print("\n3. DEDUPLICATION & FILTERING")
print("-" .padding(toLength: 40, withPad: "-", startingAt: 0))

let withDupes = [1, 2, 2, 3, 3, 3, 4, 4, 4, 4]
print("Original: \(withDupes)")
print("Unique:   \(withDupes.unique)")
print("Has duplicates: \(withDupes.hasDuplicates)")
print("Duplicates: \(withDupes.duplicates)")

let allNumbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
let evens = allNumbers.filter { $0 % 2 == 0 }
let odds = allNumbers.filterNot { $0 % 2 == 0 }
print("Evens: \(evens)")
print("Odds:  \(odds)")

// -----------------------------------------------------------------------------
// 4. 统计与聚合
// -----------------------------------------------------------------------------
print("\n4. STATISTICS & AGGREGATION")
print("-" .padding(toLength: 40, withPad: "-", startingAt: 0))

let scores: [Double] = [85.5, 92.0, 78.5, 88.0, 95.5, 72.0, 90.0]
print("Scores: \(scores)")
print("Sum:    \(scores.sum)")
print("Average: \(scores.average)")
print("Min:    \(scores.min() ?? 0)")
print("Max:    \(scores.max() ?? 0)")
print("Median: \(scores.median ?? 0)")
print("Std Dev: \(scores.standardDeviation)")

// -----------------------------------------------------------------------------
// 5. 搜索与查找
// -----------------------------------------------------------------------------
print("\n5. SEARCH & FIND")
print("-" .padding(toLength: 40, withPad: "-", startingAt: 0))

let products = ["Apple", "Banana", "Cherry", "Date", "Elderberry"]

print("Products: \(products)")

if let index = products.index(where: { $0.hasPrefix("C") }) {
    print("First starts with 'C' at index: \(index)")
}

let containsLong = products.contains { $0.count > 5 }
print("Contains name > 5 chars: \(containsLong)")

let longNames = products.findAll { $0.count > 5 }
print("All names > 5 chars: \(longNames)")

// -----------------------------------------------------------------------------
// 6. 分组与分区
// -----------------------------------------------------------------------------
print("\n6. GROUPING & PARTITIONING")
print("-" .padding(toLength: 40, withPad: "-", startingAt: 0))

let words = ["apple", "bat", "cat", "door", "egg", "fish"]
let groupedByLength = words.groupBy { $0.count }

print("Words: \(words)")
print("Grouped by length:")
for (length, group) in groupedByLength.sorted(by: { $0.key < $1.key }) {
    print("  \(length) chars: \(group)")
}

let (short, long) = words.partition { $0.count <= 3 }
print("Short (≤3): \(short)")
print("Long (>3):  \(long)")

// -----------------------------------------------------------------------------
// 7. 排序
// -----------------------------------------------------------------------------
print("\n7. SORTING")
print("-" .padding(toLength: 40, withPad: "-", startingAt: 0))

let unsorted = [3, 1, 4, 1, 5, 9, 2, 6, 5, 3]
print("Original: \(unsorted)")
print("Ascending:  \(unsorted.sortBy { $0 })")
print("Descending: \(unsorted.sortBy({ $0 }, ascending: false))")

let isSorted = [1, 2, 3, 4, 5].isSortedAscending
let isNotSorted = [1, 3, 2, 4, 5].isSortedAscending
print("[1,2,3,4,5] is sorted ascending: \(isSorted)")
print("[1,3,2,4,5] is sorted ascending: \(isNotSorted)")

// -----------------------------------------------------------------------------
// 8. 随机与抽样
// -----------------------------------------------------------------------------
print("\n8. RANDOM & SAMPLING")
print("-" .padding(toLength: 40, withPad: "-", startingAt: 0))

let lottery = Array(1...49)
let luckyNumbers = lottery.sample(6)
print("Lottery numbers (1-49): \(luckyNumbers)")

let deck = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]
let randomCard = deck.randomElement()
print("Random card: \(randomCard ?? "none")")

// -----------------------------------------------------------------------------
// 9. 工具函数
// -----------------------------------------------------------------------------
print("\n9. UTILITY FUNCTIONS")
print("-" .padding(toLength: 40, withPad: "-", startingAt: 0))

let r1 = range(0, 5)
print("range(0, 5): \(r1)")

let r2 = range(0, 10, step: 2)
print("range(0, 10, step: 2): \(r2)")

let arithmetic = arithmeticSequence(1, count: 5, step: 3)
print("arithmeticSequence(1, count: 5, step: 3): \(arithmetic)")

let geometric = geometricSequence(1.0, count: 5, ratio: 2.0)
print("geometricSequence(1, count: 5, ratio: 2): \(geometric)")

let merged = merge([1, 2], [3, 4], [5, 6])
print("merge([1,2], [3,4], [5,6]): \(merged)")

let interleaved = interleave([1, 3, 5], [2, 4, 6])
print("interleave([1,3,5], [2,4,6]): \(interleaved)")

let matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
let transposed = transpose(matrix)
print("Original matrix: \(matrix)")
print("Transposed:      \(transposed)")

let filled = filled(count: 5, with: 0)
print("filled(count: 5, with: 0): \(filled)")

let incrementing = incrementingArray(count: 5, start: 10)
print("incrementingArray(count: 5, start: 10): \(incrementing)")

// -----------------------------------------------------------------------------
// 10. 实际应用场景
// -----------------------------------------------------------------------------
print("\n10. REAL-WORLD SCENARIOS")
print("-" .padding(toLength: 40, withPad: "-", startingAt: 0))

// 场景 1: 数据清理
let rawData: [String?] = ["100", nil, "200", "invalid", "300", nil, "400"]
let cleanNumbers = rawData.compactMapNotNull { Int($0) }
print("Data cleaning:")
print("  Raw: \(rawData)")
print("  Clean: \(cleanNumbers)")

// 场景 2: 分页
let allItems = Array(1...100)
let pageSize = 10
let page1 = allItems.take(pageSize)
let page2 = allItems.skip(pageSize).take(pageSize)
print("\nPagination (page size: 10):")
print("  Page 1: \(page1)")
print("  Page 2: \(page2)")

// 场景 3: 排行榜
let players = [("Alice", 95), ("Bob", 87), ("Charlie", 92), ("Diana", 88), ("Eve", 91)]
let sortedPlayers = players.sortBy { $0.1 }, ascending: false)
print("\nLeaderboard:")
for (i, player) in sortedPlayers.enumerated() {
    print("  \(i + 1). \(player.0): \(player.1) points")
}

// 场景 4: 批量处理
let batchSize = 3
let items = Array(1...10)
var batches: [[Int]] = []
var i = 0
while i < items.count {
    batches.append(items.slice(from: i, to: min(i + batchSize, items.count)))
    i += batchSize
}
print("\nBatch processing (batch size: 3):")
for (i, batch) in batches.enumerated() {
    print("  Batch \(i + 1): \(batch)")
}

print("\n" + "=" .padding(toLength: 60, withPad: "=", startingAt: 0))
print("EXAMPLES COMPLETED")
print("=" .padding(toLength: 60, withPad: "=", startingAt: 0))
