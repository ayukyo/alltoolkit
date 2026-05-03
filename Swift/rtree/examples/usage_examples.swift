#!/usr/bin/env swift
// usage_examples.swift
// R-tree 空间索引使用示例
//
// 展示 R-tree 的各种应用场景：
// 1. 地理位置索引
// 2. 游戏碰撞检测
// 3. 空间范围查询
// 4. 最近邻查找
// 5. 地图标注
//
// Author: AllToolkit
// Version: 1.0.0

import Foundation

// MARK: - Example 1: Geographic Location Index

print("\n" + String(repeating: "=", count: 50))
print("示例 1: 地理位置索引")
print(String(repeating: "=", count: 50))

// 创建存储城市位置的 R-tree
let cityTree = RTree<String>(config: RTreeConfig(maxEntries: 8))

// 添加城市（使用经纬度坐标）
let cities = [
    (name: "北京", x: 116.4, y: 39.9),
    (name: "上海", x: 121.5, y: 31.2),
    (name: "广州", x: 113.3, y: 23.1),
    (name: "深圳", x: 114.1, y: 22.5),
    (name: "杭州", x: 120.2, y: 30.3),
    (name: "南京", x: 118.8, y: 32.1),
    (name: "成都", x: 104.1, y: 30.7),
    (name: "武汉", x: 114.3, y: 30.6),
    (name: "西安", x: 108.9, y: 34.3),
    (name: "重庆", x: 106.5, y: 29.6)
]

for city in cities {
    cityTree.insert(x: city.x, y: city.y, data: city.name)
}

print("已索引 \(cityTree.count) 个城市")
print("树高度: \(cityTree.height)")
print("边界范围: \(cityTree.bounds)")

// 查找长三角区域的城市
let yangtzeDelta = Rectangle(minX: 118, minY: 29, maxX: 122, maxY: 33)
let deltaCities = cityTree.search(yangtzeDelta)

print("\n长三角区域城市:")
for entry in deltaCities {
    print("  - \(entry.data) (\(entry.rect.centerX), \(entry.rect.centerY))")
}

// MARK: - Example 2: Collision Detection

print("\n" + String(repeating: "=", count: 50))
print("示例 2: 游戏碰撞检测")
print(String(repeating: "=", count: 50))

// 创建存储游戏对象的 R-tree
struct GameEntity: Equatable {
    let id: Int
    let name: String
    let width: Double
    let height: Double
}

let entityTree = RTree<GameEntity>(config: RTreeConfig.highPerformance)

// 添加游戏实体
let entities = [
    GameEntity(id: 1, name: "Player", width: 2, height: 2),
    GameEntity(id: 2, name: "Enemy1", width: 1, height: 1),
    GameEntity(id: 3, name: "Enemy2", width: 1, height: 1),
    GameEntity(id: 4, name: "NPC", width: 1, height: 1),
    GameEntity(id: 5, name: "Tree", width: 3, height: 3),
    GameEntity(id: 6, name: "Building", width: 5, height: 5)
]

let positions = [
    (x: 10, y: 10),  // Player
    (x: 15, y: 12),  // Enemy1
    (x: 20, y: 15),  // Enemy2
    (x: 5, y: 5),    // NPC
    (x: 25, y: 20),  // Tree
    (x: 30, y: 30)   // Building
]

for i in 0..<entities.count {
    let entity = entities[i]
    let pos = positions[i]
    let rect = Rectangle(centerX: Double(pos.x), centerY: Double(pos.y), 
                          width: entity.width, height: entity.height)
    entityTree.insert(RTreeEntry(rect: rect, data: entity))
}

print("已索引 \(entityTree.count) 个游戏实体")

// 检测玩家周围的碰撞
let playerArea = Rectangle(minX: 8, minY: 8, maxX: 12, maxY: 12)
let nearbyEntities = entityTree.searchIntersecting(playerArea)

print("\n玩家周围实体:")
for entry in nearbyEntities {
    print("  - \(entry.data.name) (ID: \(entry.data.id))")
}

// 检测特定区域的碰撞
let projectilePath = Rectangle(minX: 14, minY: 10, maxX: 16, maxY: 14)
let hitEntities = entityTree.searchIntersecting(projectilePath)

print("\n投射物路径上的实体:")
for entry in hitEntities {
    print("  - \(entry.data.name)")
}

// MARK: - Example 3: Spatial Range Queries

print("\n" + String(repeating: "=", count: 50))
print("示例 3: 空间范围查询")
print(String(repeating: "=", count: 50))

// 创建存储商店位置的 R-tree
struct Store: Equatable {
    let name: String
    let category: String
    let rating: Double
}

let storeTree = RTree<Store>()

// 添加商店
let stores = [
    (Store(name: "超市A", category: "超市", rating: 4.5), x: 100, y: 200),
    (Store(name: "超市B", category: "超市", rating: 4.2), x: 300, y: 400),
    (Store(name: "餐厅A", category: "餐厅", rating: 4.8), x: 150, y: 250),
    (Store(name: "餐厅B", category: "餐厅", rating: 3.9), x: 350, y: 450),
    (Store(name: "药店A", category: "药店", rating: 4.0), x: 200, y: 300),
    (Store(name: "书店A", category: "书店", rating: 4.3), x: 250, y: 350)
]

for (store, x, y) in stores {
    storeTree.insert(x: Double(x), y: Double(y), data: store)
}

print("已索引 \(storeTree.count) 家商店")

// 使用 SpatialQuery 进行查询
let storeQuery = SpatialQuery(storeTree)

// 查找指定范围内的商店
let area1 = Rectangle(minX: 100, minY: 200, maxX: 200, maxY: 300)
let storesInArea1 = storeQuery.within(area1)

print("\n区域 1 内的商店:")
for entry in storesInArea1 {
    print("  - \(entry.data.name) (\(entry.data.category)) 评分: \(entry.data.rating)")
}

// 查找半径范围内的商店（模拟用户附近）
let userLocation = (x: 200, y: 300)
let searchRadius = 150.0
let nearbyStores = storeQuery.withinRadius(x: Double(userLocation.x), y: Double(userLocation.y), radius: searchRadius)

print("\n用户附近 \(searchRadius) 米内的商店:")
for entry in nearbyStores {
    let distance = entry.rect.distance(x: Double(userLocation.x), y: Double(userLocation.y))
    print("  - \(entry.data.name) 距离: \(String(format: "%.1f", distance))")
}

// MARK: - Example 4: Nearest Neighbor Search

print("\n" + String(repeating: "=", count: 50))
print("示例 4: 最近邻查找")
print(String(repeating: "=", count: 50))

// 创建存储兴趣点的 R-tree
struct POI: Equatable {
    let name: String
    let type: String
}

let poiTree = RTree<POI>()

// 添加兴趣点
let pois = [
    (POI(name: "公园A", type: "公园"), x: 50, y: 50),
    (POI(name: "公园B", type: "公园"), x: 200, y: 200),
    (POI(name: "博物馆", type: "博物馆"), x: 100, y: 100),
    (POI(name: "图书馆", type: "图书馆"), x: 150, y: 150),
    (POI(name: "体育馆", type: "体育馆"), x: 250, y: 250),
    (POI(name: "电影院", type: "电影院"), x: 300, y: 300)
]

for (poi, x, y) in pois {
    poiTree.insert(x: Double(x), y: Double(y), data: poi)
}

print("已索引 \(poiTree.count) 个兴趣点")

// 查找最近的兴趣点
let userPos = (x: 120, y: 120)
let nearest = poiTree.nearest(x: Double(userPos.x), y: Double(userPos.y), k: 1)

print("\n最近的兴趣点:")
if let first = nearest.first {
    let distance = first.rect.distance(x: Double(userPos.x), y: Double(userPos.y))
    print("  - \(first.data.name) (\(first.data.type)) 距离: \(String(format: "%.1f", distance))")
}

// 查找最近的 3 个兴趣点
let nearest3 = poiTree.nearest(x: Double(userPos.x), y: Double(userPos.y), k: 3)

print("\n最近的 3 个兴趣点:")
for entry in nearest3 {
    let distance = entry.rect.distance(x: Double(userPos.x), y: Double(userPos.y))
    print("  - \(entry.data.name) (\(entry.data.type)) 距离: \(String(format: "%.1f", distance))")
}

// MARK: - Example 5: Map Annotation Management

print("\n" + String(repeating: "=", count: 50))
print("示例 5: 地图标注管理")
print(String(repeating: "=", count: 50))

// 创建存储地图标注的 R-tree
struct MapAnnotation: Equatable {
    let id: Int
    let title: String
    let description: String
    let importance: Int  // 1-5
}

let annotationTree = RTree<MapAnnotation>(config: RTreeConfig.highPerformance)

// 添加地图标注
for i in 0..<50 {
    let importance = (i % 5) + 1
    let annotation = MapAnnotation(
        id: i,
        title: "标注 \(i)",
        description: "这是第 \(i) 号标注",
        importance: importance
    )
    
    let x = Double.random(in: 0...1000)
    let y = Double.random(in: 0...1000)
    
    annotationTree.insert(x: x, y: y, data: annotation)
}

print("已索引 \(annotationTree.count) 个地图标注")
print("树高度: \(annotationTree.height)")

// 查找视口内的标注（模拟地图滚动）
let viewport = Rectangle(minX: 200, minY: 200, maxX: 400, maxY: 400)
let visibleAnnotations = annotationTree.search(viewport)

print("\n当前视口内的标注数量: \(visibleAnnotations.count)")
print("显示前 5 个:")
for entry in visibleAnnotations.prefix(5) {
    print("  - \(entry.data.title) (重要性: \(entry.data.importance))")
}

// 根据重要性筛选高优先级标注
let highPriority = visibleAnnotations.filter { $0.data.importance >= 4 }
print("\n高优先级标注数量: \(highPriority.count)")

// 查找视口中心最近的标注
let viewportCenter = (x: 300, y: 300)
let nearestAnnotation = annotationTree.nearest(x: viewportCenter.x, y: viewportCenter.y, k: 3)

print("\n视口中心最近的 3 个标注:")
for entry in nearestAnnotation {
    print("  - \(entry.data.title)")
}

// MARK: - Example 6: Dynamic Updates

print("\n" + String(repeating: "=", count: 50))
print("示例 6: 动态更新")
print(String(repeating: "=", count: 50))

// 创建动态实体树
let dynamicTree = RTree<String>()

// 添加初始实体
dynamicTree.insert(x: 10, y: 10, data: "Entity1")
dynamicTree.insert(x: 20, y: 20, data: "Entity2")
dynamicTree.insert(x: 30, y: 30, data: "Entity3")

print("初始状态:")
print("  - 条目数: \(dynamicTree.count)")
print("  - 边界: \(dynamicTree.bounds)")

// 移除一个实体
let toRemove = RTreeEntry(x: 20, y: 20, data: "Entity2")
dynamicTree.remove(toRemove)

print("\n移除 Entity2 后:")
print("  - 条目数: \(dynamicTree.count)")

// 添加新实体
dynamicTree.insert(x: 40, y: 40, data: "Entity4")
print("\n添加 Entity4 后:")
print("  - 条目数: \(dynamicTree.count)")

// 清空树
dynamicTree.clear()
print("\n清空后:")
print("  - 条目数: \(dynamicTree.count)")
print("  - 是否为空: \(dynamicTree.isEmpty)")

// MARK: - Example 7: Performance Comparison

print("\n" + String(repeating: "=", count: 50))
print("示例 7: 不同分裂策略对比")
print(String(repeating: "=", count: 50))

// 创建测试数据
let testCount = 200
let testEntries = (0..<testCount).map { i in
    RTreeEntry(x: Double.random(in: 0...100), y: Double.random(in: 0...100), data: i)
}

// 线性分裂
let linearTree = RTree<Int>(entries: testEntries, config: RTreeConfig(maxEntries: 8, splitStrategy: .linear))
print("线性分裂:")
print("  - 高度: \(linearTree.height)")
print("  - 节点数: \(linearTree.nodeCount())")
print("  - 叶子数: \(linearTree.leafCount())")
print("  - 平均填充率: \(String(format: "%.2f", linearTree.averageFillRatio() * 100))%")

// 二次分裂
let quadraticTree = RTree<Int>(entries: testEntries, config: RTreeConfig(maxEntries: 8, splitStrategy: .quadratic))
print("\n二次分裂:")
print("  - 高度: \(quadraticTree.height)")
print("  - 节点数: \(quadraticTree.nodeCount())")
print("  - 叶子数: \(quadraticTree.leafCount())")
print("  - 平均填充率: \(String(format: "%.2f", quadraticTree.averageFillRatio() * 100))%")

// R* 分裂
let rstarTree = RTree<Int>(entries: testEntries, config: RTreeConfig(maxEntries: 8, splitStrategy: .rstar))
print("\nR* 分裂:")
print("  - 高度: \(rstarTree.height)")
print("  - 节点数: \(rstarTree.nodeCount())")
print("  - 叶子数: \(rstarTree.leafCount())")
print("  - 平均填充率: \(String(format: "%.2f", rstarTree.averageFillRatio() * 100))%")

print("\n✅ 示例运行完成")