#!/usr/bin/env swift
// RTreeTest.swift
// R-tree 空间索引测试套件
//
// 测试覆盖：
// - 矩形操作（创建、相交、合并、扩展）
// - 条目插入和查询
// - 范围搜索
// - 最近邻搜索
// - 条目移除
// - 树统计
// - 边界情况
//
// Author: AllToolkit
// Version: 1.0.0

import Foundation

// 加载模块
// 注意：实际测试时需要正确设置模块路径

// MARK: - Test Framework

var testsRun = 0
var testsPassed = 0
var testsFailed = 0
var failures: [String] = []

func assertEqual<T: Equatable>(_ actual: T, _ expected: T, _ message: String) -> Bool {
    testsRun += 1
    if actual == expected {
        testsPassed += 1
        return true
    } else {
        testsFailed += 1
        failures.append("\(message): expected \(expected), got \(actual)")
        print("  ❌ FAIL: \(message)")
        return false
    }
}

func assertTrue(_ condition: Bool, _ message: String) -> Bool {
    testsRun += 1
    if condition {
        testsPassed += 1
        return true
    } else {
        testsFailed += 1
        failures.append(message)
        print("  ❌ FAIL: \(message)")
        return false
    }
}

func assertFalse(_ condition: Bool, _ message: String) -> Bool {
    return assertTrue(!condition, message)
}

func assertApproxEqual(_ actual: Double, _ expected: Double, _ tolerance: Double = 0.001, _ message: String) -> Bool {
    testsRun += 1
    if abs(actual - expected) <= tolerance {
        testsPassed += 1
        return true
    } else {
        testsFailed += 1
        failures.append("\(message): expected ~\(expected), got \(actual)")
        print("  ❌ FAIL: \(message)")
        return false
    }
}

func testGroup(_ name: String) {
    print("\n📋 \(name)")
    print(String(repeating: "-", count: 50))
}

// MARK: - Rectangle Tests

testGroup("Rectangle (矩形操作)")

// 创建矩形
let rect1 = Rectangle(minX: 0, minY: 0, maxX: 10, maxY: 10)
assertApproxEqual(rect1.width, 10, "矩形宽度")
assertApproxEqual(rect1.height, 10, "矩形高度")
assertApproxEqual(rect1.area, 100, "矩形面积")
assertApproxEqual(rect1.centerX, 5, "中心点 X")
assertApproxEqual(rect1.centerY, 5, "中心点 Y")
assertTrue(rect1.isValid, "矩形有效")
assertFalse(rect1.isPoint, "非点矩形")

// 点矩形
let pointRect = Rectangle(x: 5, y: 5)
assertApproxEqual(pointRect.width, 0, "点矩形宽度")
assertApproxEqual(pointRect.area, 0, "点矩形面积")
assertTrue(pointRect.isPoint, "点矩形标记")

// 从中心点创建
let rectFromCenter = Rectangle(centerX: 10, centerY: 10, width: 20, height: 20)
assertApproxEqual(rectFromCenter.minX, 0, "中心创建 minX")
assertApproxEqual(rectFromCenter.maxX, 20, "中心创建 maxX")

// 包含检测
assertTrue(rect1.contains(x: 5, y: 5), "包含内部点")
assertTrue(rect1.contains(x: 0, y: 0), "包含边界点")
assertFalse(rect1.contains(x: 11, y: 5), "不包含外部点")

let rect2 = Rectangle(minX: 2, minY: 2, maxX: 8, maxY: 8)
assertTrue(rect1.contains(rect2), "包含内部矩形")

let rect3 = Rectangle(minX: -5, minY: -5, maxX: 5, maxY: 5)
assertFalse(rect1.contains(rect3), "不包含部分外部矩形")

// 相交检测
assertTrue(rect1.intersects(rect2), "相交 - 内部矩形")
assertTrue(rect1.intersects(rect3), "相交 - 部分重叠")

let rect4 = Rectangle(minX: 15, minY: 15, maxX: 20, maxY: 20)
assertFalse(rect1.intersects(rect4), "不相交 - 完全分离")

// 交集计算
let intersection = rect1.intersection(rect3)
assertTrue(intersection != nil, "存在交集")
if let inter = intersection {
    assertApproxEqual(inter.minX, 0, "交集 minX")
    assertApproxEqual(inter.maxX, 5, "交集 maxX")
    assertApproxEqual(inter.area, 25, "交集面积")
}

// 合并矩形
let union = rect1.union(rect4)
assertApproxEqual(union.minX, 0, "合并 minX")
assertApproxEqual(union.maxX, 20, "合并 maxX")
assertApproxEqual(union.area, 400, "合并面积")

// 扩展矩形
var mutableRect = Rectangle(minX: 0, minY: 0, maxX: 10, maxY: 10)
mutableRect.expand(x: 15, y: 5)
assertApproxEqual(mutableRect.maxX, 15, "扩展后 maxX")

// 距离计算
assertApproxEqual(rect1.distance(rect4), 14.142, tolerance: 0.01, "矩形距离")

// MARK: - RTree Entry Tests

testGroup("RTreeEntry (条目操作)")

let entry1 = RTreeEntry(rect: rect1, data: "Entry1")
assertEqual(entry1.rect, rect1, "条目矩形")
assertEqual(entry1.data, "Entry1", "条目数据")

let pointEntry = RTreeEntry(x: 5, y: 5, data: "Point")
assertTrue(pointEntry.rect.isPoint, "点条目矩形")

let centerEntry = RTreeEntry(centerX: 10, centerY: 10, width: 4, height: 4, data: "Center")
assertApproxEqual(centerEntry.rect.width, 4, "中心条目宽度")

// MARK: - RTree Insert Tests

testGroup("RTree Insert (插入操作)")

let rtree = RTree<String>(config: RTreeConfig(maxEntries: 4))

assertTrue(rtree.isEmpty, "空树")
assertEqual(rtree.count, 0, "初始数量")

// 插入点
rtree.insert(x: 5, y: 5, data: "Point1")
assertFalse(rtree.isEmpty, "插入后非空")
assertEqual(rtree.count, 1, "插入后数量")

// 插入更多点
rtree.insert(x: 10, y: 10, data: "Point2")
rtree.insert(x: 15, y: 15, data: "Point3")
rtree.insert(x: 20, y: 20, data: "Point4")
rtree.insert(x: 25, y: 25, data: "Point5")

assertEqual(rtree.count, 5, "5个条目")
assertTrue(rtree.height >= 1, "树高度")

// 批量插入
let batchEntries = [
    RTreeEntry(x: 30, y: 30, data: "Batch1"),
    RTreeEntry(x: 35, y: 35, data: "Batch2"),
    RTreeEntry(x: 40, y: 40, data: "Batch3")
]
rtree.insert(batchEntries)
assertEqual(rtree.count, 8, "批量插入后数量")

// MARK: - RTree Search Tests

testGroup("RTree Search (搜索操作)")

// 创建测试树
let searchTree = RTree<String>(config: RTreeConfig(maxEntries: 4))

// 插入网格数据
for i in 0..<10 {
    for j in 0..<10 {
        searchTree.insert(x: Double(i * 10), y: Double(j * 10), data: "P\(i)_\(j)")
    }
}

assertEqual(searchTree.count, 100, "100个网格点")

// 范围搜索
let searchRect = Rectangle(minX: 20, minY: 20, maxX: 40, maxY: 40)
let results = searchTree.search(searchRect)
assertTrue(results.count >= 9, "范围搜索结果数量")  // 应包含 (2,2) 到 (4,4)

// 检查包含的点
let pointResults = searchTree.searchContaining(x: 30, y: 30)
assertTrue(pointResults.count >= 1, "包含点搜索")

// 相交搜索
let intersectResults = searchTree.searchIntersecting(searchRect)
assertTrue(intersectResults.count >= 9, "相交搜索结果")

// 获取数据
let dataResults = searchTree.searchData(searchRect)
assertTrue(dataResults.contains("P3_3"), "搜索数据包含期望值")

// MARK: - Nearest Neighbor Tests

testGroup("Nearest Neighbor (最近邻搜索)")

let nearestTree = RTree<String>(config: .defaultConfig)
nearestTree.insert(x: 0, y: 0, data: "Origin")
nearestTree.insert(x: 10, y: 0, data: "Right")
nearestTree.insert(x: 0, y: 10, data: "Up")
nearestTree.insert(x: 10, y: 10, data: "Diagonal")
nearestTree.insert(x: 50, y: 50, data: "Far")

// 查找最近的 1 个
let nearest1 = nearestTree.nearest(x: 5, y: 5, k: 1)
assertEqual(nearest1.count, 1, "最近 1 个数量")
assertEqual(nearest1.first?.data, "Origin", "最近 1 个是 Origin")  // 距离 sqrt(50) ≈ 7.07

// 查找最近的 3 个
let nearest3 = nearestTree.nearest(x: 5, y: 5, k: 3)
assertEqual(nearest3.count, 3, "最近 3 个数量")

// 获取最近数据
let nearestData = nearestTree.nearestData(x: 5, y: 5, k: 2)
assertEqual(nearestData.count, 2, "最近数据数量")

// MARK: - Remove Tests

testGroup("RTree Remove (移除操作)")

let removeTree = RTree<String>(config: RTreeConfig(maxEntries: 4))
removeTree.insert(x: 5, y: 5, data: "ToRemove")
removeTree.insert(x: 10, y: 10, data: "Keep1")
removeTree.insert(x: 15, y: 15, data: "Keep2")

assertEqual(removeTree.count, 3, "移除前数量")

// 移除条目
let toRemove = RTreeEntry(x: 5, y: 5, data: "ToRemove")
let removed = removeTree.remove(toRemove)
assertTrue(removed, "成功移除")
assertEqual(removeTree.count, 2, "移除后数量")

// 搜索不应包含移除的条目
let searchAfterRemove = removeTree.search(Rectangle.infinite)
assertFalse(searchAfterRemove.contains { $0.data == "ToRemove" }, "移除后搜索不含该条目")

// 移除不存在的条目
let notExist = RTreeEntry(x: 100, y: 100, data: "NotExist")
assertFalse(removeTree.remove(notExist), "移除不存在条目返回 false")

// MARK: - Statistics Tests

testGroup("Statistics (统计信息)")

let statsTree = RTree<Int>(config: RTreeConfig(maxEntries: 4))
for i in 0..<50 {
    statsTree.insert(x: Double(i), y: Double(i), data: i)
}

assertTrue(statsTree.nodeCount() > 0, "节点数量")
assertTrue(statsTree.leafCount() > 0, "叶子节点数量")
assertTrue(statsTree.averageFillRatio() > 0, "平均填充率")

let bounds = statsTree.bounds
assertTrue(bounds.isValid, "边界有效")
assertApproxEqual(bounds.minX, 0, "边界 minX")
assertApproxEqual(bounds.maxX, 49, "边界 maxX")

// MARK: - Builder Tests

testGroup("RTree Builder (构建器)")

let builderTree = RTreeBuilder<Int>()
    .add(x: 0, y: 0, data: 0)
    .add(x: 10, y: 10, data: 10)
    .add(x: 20, y: 20, data: 20)
    .withConfig(RTreeConfig(maxEntries: 4))
    .build()

assertEqual(builderTree.count, 3, "构建器创建树数量")

let builderResults = builderTree.search(Rectangle(minX: 5, minY: 5, maxX: 25, maxY: 25))
assertTrue(builderResults.count >= 2, "构建器树搜索结果")

// MARK: - Spatial Query Tests

testGroup("Spatial Query (空间查询)")

let queryTree = RTree<String>()
queryTree.insert(x: 5, y: 5, data: "Center")
queryTree.insert(x: 15, y: 15, data: "Outer")
queryTree.insert(x: 25, y: 25, data: "Far")

let query = SpatialQuery(queryTree)

// 圆内查询
let radiusResults = query.withinRadius(x: 10, y: 10, radius: 10)
assertTrue(radiusResults.count >= 2, "圆内查询包含 Center 和 Outer")

let radiusData = query.withinRadiusData(x: 10, y: 10, radius: 5)
assertTrue(radiusData.count >= 1, "小半径查询")

// MARK: - Traversal Tests

testGroup("Traversal (遍历)")

let traversalTree = RTree<Int>()
for i in 0..<20 {
    traversalTree.insert(x: Double(i), y: Double(i), data: i)
}

var traversalCount = 0
traversalTree.forEach { _ in traversalCount += 1 }
assertEqual(traversalCount, 20, "遍历计数")

let allEntries = traversalTree.allEntries()
assertEqual(allEntries.count, 20, "所有条目数量")

let allData = traversalTree.allData()
assertEqual(allData.count, 20, "所有数据数量")

// MARK: - Clear Tests

testGroup("Clear (清空)")

let clearTree = RTree<String>()
clearTree.insert(x: 5, y: 5, data: "Test")
clearTree.insert(x: 10, y: 10, data: "Test2")

clearTree.clear()
assertTrue(clearTree.isEmpty, "清空后为空")
assertEqual(clearTree.count, 0, "清空后数量")
assertEqual(clearTree.root, nil, "清空后无根节点")

// MARK: - Edge Cases Tests

testGroup("Edge Cases (边界情况)")

// 空树操作
let emptyTree = RTree<String>()
assertEqual(emptyTree.search(Rectangle.infinite).count, 0, "空树搜索")
assertEqual(emptyTree.nearest(x: 0, y: 0, k: 5).count, 0, "空树最近邻")
assertEqual(emptyTree.nodeCount(), 0, "空树节点数")
assertEqual(emptyTree.height, 0, "空树高度")

// 大量数据
let largeTree = RTree<Int>(config: RTreeConfig(maxEntries: 8))
for i in 0..<500 {
    largeTree.insert(x: Double.random(in: 0...100), y: Double.random(in: 0...100), data: i)
}
assertEqual(largeTree.count, 500, "大量数据插入")
assertTrue(largeTree.height >= 3, "大量数据树高度")

// 相同位置多个条目
let samePosTree = RTree<String>()
samePosTree.insert(x: 5, y: 5, data: "A")
samePosTree.insert(x: 5, y: 5, data: "B")
samePosTree.insert(x: 5, y: 5, data: "C")
let samePosResults = samePosTree.searchContaining(x: 5, y: 5)
assertEqual(samePosResults.count, 3, "相同位置多个条目")

// MARK: - Split Strategy Tests

testGroup("Split Strategies (分裂策略)")

// 线性分裂
let linearTree = RTree<Int>(config: RTreeConfig(maxEntries: 4, splitStrategy: .linear))
for i in 0..<20 {
    linearTree.insert(x: Double(i), y: Double(i), data: i)
}
assertEqual(linearTree.count, 20, "线性分裂树")

// 二次分裂
let quadraticTree = RTree<Int>(config: RTreeConfig(maxEntries: 4, splitStrategy: .quadratic))
for i in 0..<20 {
    quadraticTree.insert(x: Double(i), y: Double(i), data: i)
}
assertEqual(quadraticTree.count, 20, "二次分裂树")

// R* 分裂
let rstarTree = RTree<Int>(config: RTreeConfig(maxEntries: 4, splitStrategy: .rstar))
for i in 0..<20 {
    rstarTree.insert(x: Double(i), y: Double(i), data: i)
}
assertEqual(rstarTree.count, 20, "R*分裂树")

// MARK: - Print Results

print("\n" + String(repeating: "=", count: 50))
print("📊 测试结果")
print(String(repeating: "=", count: 50))
print("总测试数：\(testsRun)")
print("✅ 通过：\(testsPassed)")
print("❌ 失败：\(testsFailed)")

if testsFailed > 0 {
    print("\n📝 失败详情:")
    for (index, failure) in failures.enumerated() {
        print("  \(index + 1). \(failure)")
    }
} else {
    print("\n🎉 所有测试通过!")
}