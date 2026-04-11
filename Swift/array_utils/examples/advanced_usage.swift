/**
 * Array Utils - Advanced Usage Examples
 * 
 * 演示数组工具类的高级用法和实际应用场景
 */

import Foundation

print("=" .padding(toLength: 60, withPad: "=", startingAt: 0))
print("ARRAY UTILS - ADVANCED USAGE EXAMPLES")
print("=" .padding(toLength: 60, withPad: "=", startingAt: 0))

// -----------------------------------------------------------------------------
// 1. 数据分析管道
// -----------------------------------------------------------------------------
print("\n1. DATA ANALYSIS PIPELINE")
print("-" .padding(toLength: 40, withPad: "-", startingAt: 0))

// 模拟销售数据
struct Sale {
    let product: String
    let category: String
    let price: Double
    let quantity: Int
}

let sales = [
    Sale(product: "Laptop", category: "Electronics", price: 999.99, quantity: 5),
    Sale(product: "Mouse", category: "Electronics", price: 29.99, quantity: 20),
    Sale(product: "Desk", category: "Furniture", price: 299.99, quantity: 3),
    Sale(product: "Chair", category: "Furniture", price: 199.99, quantity: 8),
    Sale(product: "Monitor", category: "Electronics", price: 399.99, quantity: 7),
    Sale(product: "Keyboard", category: "Electronics", price: 79.99, quantity: 15),
    Sale(product: "Bookshelf", category: "Furniture", price: 149.99, quantity: 4),
]

// 按类别分组
let byCategory = sales.groupBy { $0.category }
print("Sales by category:")
for (category, items) in byCategory {
    let total = items.map { $0.price * Double($0.quantity) }.sum
    print("  \(category): \(items.count) items, total: $\(String(format: "%.2f", total))")
}

// 查找高价值订单（> $500）
let highValue = sales.findAll { $0.price * Double($0.quantity) > 500 }
print("\nHigh value orders (>$500):")
for sale in highValue {
    let total = sale.price * Double(sale.quantity)
    print("  \(sale.product): $\(String(format: "%.2f", total))")
}

// -----------------------------------------------------------------------------
// 2. 字符串处理管道
// -----------------------------------------------------------------------------
print("\n2. STRING PROCESSING PIPELINE")
print("-" .padding(toLength: 40, withPad: "-", startingAt: 0))

let rawTexts = [
    "  Hello World  ",
    "SWIFT PROGRAMMING",
    "data   science",
    "  MACHINE learning",
    "ARTIFICIAL intelligence",
    "",
    "   ",
    nil,
    "valid text"
]

// 清理和转换管道
let cleaned = rawTexts
    .compactMap { $0 }                              // 移除 nil
    .filter { !$0.trimmingCharacters(in: .whitespaces).isEmpty }  // 移除空字符串
    .map { $0.trimmingCharacters(in: .whitespaces) }  // 去除两端空白
    .map { $0.lowercased() }                        // 转小写
    .unique                                         // 去重

print("Original count: \(rawTexts.count)")
print("Cleaned count: \(cleaned.count)")
print("Cleaned texts: \(cleaned)")

// -----------------------------------------------------------------------------
// 3. 时间序列分析
// -----------------------------------------------------------------------------
print("\n3. TIME SERIES ANALYSIS")
print("-" .padding(toLength: 40, withPad: "-", startingAt: 0))

// 模拟每日温度数据
let temperatures: [Double] = [
    22.5, 23.0, 21.8, 24.5, 25.2,  // Week 1
    26.0, 27.5, 25.8, 24.0, 23.5,  // Week 2
    22.0, 21.5, 20.8, 22.0, 23.5,  // Week 3
    24.0, 25.5, 26.8, 27.0, 28.5,  // Week 4
]

print("Temperature data (20 days):")
print("  Average: \(String(format: "%.1f", temperatures.average))°C")
print("  Min: \(temperatures.min() ?? 0)°C")
print("  Max: \(temperatures.max() ?? 0)°C")
print("  Std Dev: \(String(format: "%.2f", temperatures.standardDeviation))°C")

// 查找高温天（> 26°C）
let hotDays = temperatures.findAll { $0 > 26.0 }
print("  Hot days (>26°C): \(hotDays.count)")

// 周平均温度
let weeklyAverages = stride(from: 0, to: temperatures.count, by: 7).map { start -> Double in
    let week = temperatures.slice(from: start, to: min(start + 7, temperatures.count))
    return week.average
}

print("  Weekly averages: \(weeklyAverages.map { String(format: "%.1f", $0) })")

// -----------------------------------------------------------------------------
// 4. 用户权限管理
// -----------------------------------------------------------------------------
print("\n4. USER PERMISSION MANAGEMENT")
print("-" .padding(toLength: 40, withPad: "-", startingAt: 0))

enum Permission: String, CaseIterable {
    case read, write, delete, admin, export, import
}

struct User {
    let id: Int
    let name: String
    let permissions: [Permission]
}

let users = [
    User(id: 1, name: "Alice", permissions: [.read, .write]),
    User(id: 2, name: "Bob", permissions: [.read]),
    User(id: 3, name: "Charlie", permissions: [.read, .write, .delete]),
    User(id: 4, name: "Diana", permissions: [.read, .write, .admin]),
    User(id: 5, name: "Eve", permissions: [.read, .export]),
]

// 按权限分组用户
let usersByPermission: [Permission: [User]] = Permission.allCases.reduce(into: [:]) { result, perm in
    result[perm] = users.filter { $0.permissions.contains(perm) }
}

print("Users by permission:")
for perm in Permission.allCases {
    if let users = usersByPermission[perm] {
        print("  \(perm.rawValue): \(users.map { $0.name }.join(separator: ", "))")
    }
}

// 查找有 admin 权限的用户
let admins = users.findAll { $0.permissions.contains(.admin) }
print("\nAdmins: \(admins.map { $0.name }.join())")

// 查找只有 read 权限的用户
let readOnly = users.filter { $0.permissions == [.read] }
print("Read-only users: \(readOnly.map { $0.name }.join())")

// -----------------------------------------------------------------------------
// 5. 购物车计算
// -----------------------------------------------------------------------------
print("\n5. SHOPPING CART CALCULATION")
print("-" .padding(toLength: 40, withPad: "-", startingAt: 0))

struct CartItem {
    let name: String
    let price: Double
    let quantity: Int
    let discount: Double  // 0.0 - 1.0
}

let cart = [
    CartItem(name: "Laptop", price: 999.99, quantity: 1, discount: 0.1),
    CartItem(name: "Mouse", price: 29.99, quantity: 2, discount: 0.0),
    CartItem(name: "Keyboard", price: 79.99, quantity: 1, discount: 0.15),
    CartItem(name: "Monitor", price: 399.99, quantity: 1, discount: 0.05),
    CartItem(name: "USB Hub", price: 25.99, quantity: 3, discount: 0.0),
]

// 计算每项小计
let subtotals = cart.map { item -> (name: String, subtotal: Double) in
    let original = item.price * Double(item.quantity)
    let discounted = original * (1 - item.discount)
    return (item.name, discounted)
}

print("Cart items:")
for item in subtotals {
    print("  \(item.name): $\(String(format: "%.2f", item.subtotal))")
}

// 计算总计
let total = subtotals.map { $0.subtotal }.sum
print("\nSubtotal: $\(String(format: "%.2f", total))")

// 应用满减优惠
let finalTotal = total > 1000 ? total * 0.95 : total  // 满$1000 打 95 折
if total > 1000 {
    print("Bulk discount (5%): -$\(String(format: "%.2f", total - finalTotal))")
}
print("Final Total: $\(String(format: "%.2f", finalTotal))")

// -----------------------------------------------------------------------------
// 6. 任务调度器
// -----------------------------------------------------------------------------
print("\n6. TASK SCHEDULER")
print("-" .padding(toLength: 40, withPad: "-", startingAt: 0))

enum TaskPriority: Int, Comparable {
    case low = 1, medium = 2, high = 3, urgent = 4
    
    static func < (lhs: TaskPriority, rhs: TaskPriority) -> Bool {
        return lhs.rawValue < rhs.rawValue
    }
}

struct Task {
    let id: Int
    let name: String
    let priority: TaskPriority
    let estimatedHours: Double
}

let tasks = [
    Task(id: 1, name: "Fix critical bug", priority: .urgent, estimatedHours: 2),
    Task(id: 2, name: "Write documentation", priority: .low, estimatedHours: 4),
    Task(id: 3, name: "Code review", priority: .medium, estimatedHours: 1),
    Task(id: 4, name: "Deploy to production", priority: .high, estimatedHours: 3),
    Task(id: 5, name: "Update dependencies", priority: .low, estimatedHours: 2),
    Task(id: 6, name: "Performance optimization", priority: .high, estimatedHours: 5),
]

// 按优先级排序
let sortedTasks = tasks.sortBy { $0.priority }, ascending: false)
print("Tasks sorted by priority:")
for task in sortedTasks {
    print("  [\(task.priority.rawValue)] \(task.name) (\(task.estimatedHours)h)")
}

// 按优先级分组
let byPriority = tasks.groupBy { $0.priority }
print("\nTasks by priority:")
for priority in [TaskPriority.urgent, .high, .medium, .low] {
    if let tasks = byPriority[priority] {
        let names = tasks.map { $0.name }.join(separator: ", ")
        print("  \(priority.rawValue): \(names)")
    }
}

// 计算总工时
let totalHours = tasks.map { $0.estimatedHours }.sum
print("\nTotal estimated hours: \(totalHours)h")

// 高优先级任务工时
let urgentHours = tasks
    .findAll { $0.priority == .urgent || $0.priority == .high }
    .map { $0.estimatedHours }
    .sum
print("High priority hours: \(urgentHours)h")

// -----------------------------------------------------------------------------
// 7. 矩阵运算
// -----------------------------------------------------------------------------
print("\n7. MATRIX OPERATIONS")
print("-" .padding(toLength: 40, withPad: "-", startingAt: 0))

// 3x3 矩阵
let matrix1: [[Double]] = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9]
]

print("Original matrix:")
for row in matrix1 {
    print("  \(row)")
}

// 转置
let transposed = transpose(matrix1)
print("\nTransposed:")
for row in transposed {
    print("  \(row)")
}

// 提取列
let columns = transposed
print("\nColumns:")
for (i, col) in columns.enumerated() {
    print("  Column \(i): \(col)")
}

// 计算每行总和
let rowSums = matrix1.map { $0.sum }
print("\nRow sums: \(rowSums)")

// 计算每列平均值
let colAverages = transposed.map { $0.average }
print("Column averages: \(colAverages.map { String(format: "%.1f", $0) })")

// -----------------------------------------------------------------------------
// 8. A/B 测试分析
// -----------------------------------------------------------------------------
print("\n8. A/B TEST ANALYSIS")
print("-" .padding(toLength: 40, withPad: "-", startingAt: 0))

// 模拟 A/B 测试转化率数据
let groupA: [Double] = [0.12, 0.15, 0.11, 0.14, 0.13, 0.16, 0.12, 0.14]
let groupB: [Double] = [0.18, 0.17, 0.19, 0.16, 0.18, 0.20, 0.17, 0.19]

print("A/B Test Conversion Rates:")
print("  Group A (control):")
print("    Mean: \(String(format: "%.3f", groupA.average))")
print("    Std Dev: \(String(format: "%.3f", groupA.standardDeviation))")
print("    Range: [\(String(format: "%.2f", groupA.min() ?? 0)), \(String(format: "%.2f", groupA.max() ?? 0))]")

print("  Group B (variant):")
print("    Mean: \(String(format: "%.3f", groupB.average))")
print("    Std Dev: \(String(format: "%.3f", groupB.standardDeviation))")
print("    Range: [\(String(format: "%.2f", groupB.min() ?? 0)), \(String(format: "%.2f", groupB.max() ?? 0))]")

// 计算提升
let lift = (groupB.average - groupA.average) / groupA.average * 100
print("\n  Lift: \(String(format: "+%.1f", lift))%")

// 检查 B 组是否始终优于 A 组
let allBetter = groupB.min() ?? 0 > groupA.max() ?? 1
print("  B always better than A: \(allBetter)")

print("\n" + "=" .padding(toLength: 60, withPad: "=", startingAt: 0))
print("ADVANCED EXAMPLES COMPLETED")
print("=" .padding(toLength: 60, withPad: "=", startingAt: 0))
