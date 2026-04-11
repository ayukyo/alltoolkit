# Swift Array Utils 📦

Swift 数组/集合工具类，提供常用的数组处理、转换、统计和搜索功能。

## ✨ 特性

- **零依赖** - 仅使用 Swift 标准库
- **类型安全** - 充分利用 Swift 泛型和类型系统
- **功能丰富** - 50+ 个实用函数
- **生产就绪** - 完整测试覆盖，包含边界值测试
- **高性能** - 优化的算法实现

## 📦 安装

将 `mod.swift` 添加到您的项目中：

```bash
cp Swift/array_utils/mod.swift YourProject/
```

或在 Package.swift 中添加：

```swift
dependencies: [
    .package(url: "https://github.com/ayukyo/alltoolkit.git", from: "1.0.0")
]
```

## 🚀 快速开始

```swift
import Foundation

// 导入模块（如果在同一项目）
// import AllToolkitArrayUtils

let numbers = [1, 2, 3, 4, 5]

// 安全访问
let first = numbers.firstSafe       // 1
let last = numbers.lastSafe         // 5
let safe = numbers.safeGet(at: 10)  // nil (不会崩溃)

// 切片操作
let take3 = numbers.take(3)         // [1, 2, 3]
let skip2 = numbers.skip(2)         // [3, 4, 5]
let last2 = numbers.takeLast(2)     // [4, 5]

// 去重
let withDupes = [1, 2, 2, 3, 3, 3]
let unique = withDupes.unique       // [1, 2, 3]

// 统计
let sum = numbers.sum               // 15
let avg = numbers.average           // 3.0
let max = numbers.max()             // 5
let min = numbers.min()             // 1

// 搜索
let index = numbers.index { $0 > 3 }    // 3
let contains = numbers.contains { $0 == 3 }  // true

// 分组
let grouped = numbers.groupBy { $0 % 2 }
// [0: [2, 4], 1: [1, 3, 5]]

// 排序
let unsorted = [3, 1, 4, 1, 5]
let sorted = unsorted.sortBy { $0 }  // [1, 1, 3, 4, 5]

// 随机
let random = numbers.randomElement()     // 随机一个
let sample = numbers.sample(3)           // 随机 3 个不重复
```

## 📚 API 文档

### 空值与安全访问

| 方法 | 描述 | 返回 |
|------|------|------|
| `isEmpty` | 检查数组是否为空 | `Bool` |
| `isNotEmpty` | 检查数组是否不为空 | `Bool` |
| `firstSafe` | 安全获取第一个元素 | `Element?` |
| `lastSafe` | 安全获取最后一个元素 | `Element?` |
| `safeGet(at:)` | 安全获取指定索引元素 | `Element?` |
| `firstOr(_:)` | 获取第一个元素或默认值 | `Element` |

### 切片操作

| 方法 | 描述 | 参数 |
|------|------|------|
| `take(_:)` | 获取前 n 个元素 | `count: Int` |
| `skip(_:)` | 跳过前 n 个元素 | `count: Int` |
| `takeLast(_:)` | 获取后 n 个元素 | `count: Int` |
| `slice(from:to:)` | 获取指定范围元素 | `start: Int, end: Int` |

### 去重与过滤

| 方法 | 描述 | 返回 |
|------|------|------|
| `unique()` / `unique` | 去除重复元素 | `[Element]` |
| `filterNot(_:)` | 过滤不符合条件的元素 | `[Element]` |
| `compacted()` | 移除 nil 值 | `[T]` |
| `hasDuplicates` | 检查是否有重复 | `Bool` |
| `duplicates` | 获取重复的元素 | `[Element]` |

### 转换与映射

| 方法 | 描述 | 参数 |
|------|------|------|
| `compactMapNotNull(_:)` | 映射并过滤 nil | `transform: (Element) -> T?` |
| `join(separator:)` | 连接元素为字符串 | `separator: String` |

### 统计与聚合

| 方法 | 描述 | 返回类型 |
|------|------|------|
| `sum` | 元素总和 | `Element` |
| `average` | 平均值 | `Element` |
| `max()` | 最大值 | `Element?` |
| `min()` | 最小值 | `Element?` |
| `product` | 乘积 | `Element` |
| `standardDeviation` | 标准差 | `Element` |
| `median` | 中位数 | `Element?` |

### 搜索与查找

| 方法 | 描述 | 返回 |
|------|------|------|
| `index(where:)` | 查找第一个符合条件的索引 | `Int?` |
| `contains(where:)` | 检查是否包含符合条件的元素 | `Bool` |
| `findAll(where:)` | 查找所有符合条件的元素 | `[Element]` |

### 分组与分区

| 方法 | 描述 | 参数 |
|------|------|------|
| `groupBy(_:)` | 按条件分组 | `keySelector: (Element) -> K` |
| `partition(by:)` | 按条件分区 | `predicate: (Element) -> Bool` |

### 排序

| 方法 | 描述 | 参数 |
|------|------|------|
| `sortBy(_:ascending:)` | 按指定键排序 | `keySelector, ascending` |
| `isSortedAscending` | 检查是否升序 | - |
| `isSortedDescending` | 检查是否降序 | - |

### 组合与连接

| 方法 | 描述 | 参数 |
|------|------|------|
| `concat(_:)` | 合并另一个数组 | `other: [Element]` |

### 随机与打乱

| 方法 | 描述 | 参数 |
|------|------|------|
| `randomElement()` | 随机获取一个元素 | - |
| `sample(_:)` | 随机获取 n 个不重复元素 | `count: Int` |

### 工具函数

| 函数 | 描述 | 示例 |
|------|------|------|
| `range(_:_:step:)` | 创建范围数组 | `range(0, 5)` → `[0,1,2,3,4]` |
| `arithmeticSequence(_:count:step:)` | 等差数列 | `arithmeticSequence(1, count: 5, step: 2)` → `[1,3,5,7,9]` |
| `geometricSequence(_:count:ratio:)` | 等比数列 | `geometricSequence(1, count: 5, ratio: 2)` → `[1,2,4,8,16]` |
| `merge(_:)` | 合并多个数组 | `merge([1,2], [3,4])` → `[1,2,3,4]` |
| `interleave(_:_:)` | 交错合并 | `interleave([1,3], [2,4])` → `[1,2,3,4]` |
| `transpose(_:)` | 转置二维数组 | `transpose([[1,2],[3,4]])` → `[[1,3],[2,4]]` |
| `filled(count:with:)` | 创建填充数组 | `filled(count: 3, with: 0)` → `[0,0,0]` |
| `incrementingArray(count:start:)` | 递增数组 | `incrementingArray(count: 5, start: 10)` → `[10,11,12,13,14]` |

## 📝 使用示例

### 数据处理

```swift
// 清理和转换数据
let rawData: [String?] = ["1", nil, "2", "abc", "3"]
let numbers = rawData.compactMapNotNull { Int($0) }
// [1, 2, 3]

// 分组统计
let users = [("A", 25), ("B", 30), ("C", 25), ("D", 35)]
let byAge = users.groupBy { $0.1 }
// [25: [("A", 25), ("C", 25)], 30: [("B", 30)], 35: [("D", 35)]]
```

### 数学计算

```swift
let scores: [Double] = [85.5, 92.0, 78.5, 88.0, 95.5]

let average = scores.average           // 87.9
let stdDev = scores.standardDeviation  // 6.09
let median = scores.median             // 88.0
let maxScore = scores.max()            // 95.5
```

### 集合操作

```swift
let evens = [2, 4, 6, 8]
let odds = [1, 3, 5, 7]

// 合并
let all = evens.concat(odds)           // [2, 4, 6, 8, 1, 3, 5, 7]

// 交错
let interleaved = interleave(evens, odds)  // [2, 1, 4, 3, 6, 5, 8, 7]

// 去重
let withDupes = [1, 2, 2, 3, 3, 3]
let unique = withDupes.unique          // [1, 2, 3]
```

### 随机抽样

```swift
let lottery = Array(1...49)

// 随机选 6 个不重复号码
let luckyNumbers = lottery.sample(6)
// e.g., [7, 23, 15, 42, 3, 38]

// 随机一个
let single = lottery.randomElement()
```

## 🧪 测试

运行测试：

```bash
# 使用 Swift Package Manager
swift test

# 或直接编译运行
swiftc Swift/array_utils/mod.swift Swift/array_utils/ArrayUtilsTest.swift -o array_test
./array_test
```

测试覆盖：
- ✅ 空值与安全访问 (6 个测试)
- ✅ 切片操作 (4 个测试)
- ✅ 去重与过滤 (5 个测试)
- ✅ 转换与映射 (2 个测试)
- ✅ 统计与聚合 (6 个测试)
- ✅ 搜索与查找 (3 个测试)
- ✅ 分组与分区 (2 个测试)
- ✅ 排序 (4 个测试)
- ✅ 组合与连接 (1 个测试)
- ✅ 随机与打乱 (2 个测试)
- ✅ 工具函数 (8 个测试)
- ✅ 边界值测试 (4 个测试)

**总计：47 个测试用例**

## 📋 系统要求

- iOS 13.0+
- macOS 10.15+
- watchOS 6.0+
- tvOS 13.0+

## 📄 许可证

MIT License - 详见 [LICENSE](../../LICENSE)

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

---

**最后更新**: 2026-04-12
**版本**: 1.0.0
