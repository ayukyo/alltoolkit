// RTree.swift
// R-tree 空间索引数据结构实现
// 零外部依赖，纯 Swift 实现

import Foundation

// MARK: - Rectangle (Bounding Box)

/// 二维矩形（边界框）
public struct Rectangle: Equatable, Hashable, Codable {
    /// 最小 X 坐标
    public var minX: Double
    /// 最小 Y 坐标
    public var minY: Double
    /// 最大 X 坐标
    public var maxX: Double
    /// 最大 Y 坐标
    public var maxY: Double
    
    /// 创建矩形
    public init(minX: Double, minY: Double, maxX: Double, maxY: Double) {
        self.minX = minX
        self.minY = minY
        self.maxX = maxX
        self.maxY = maxY
    }
    
    /// 创建点矩形（点被视为零面积的矩形）
    public init(x: Double, y: Double) {
        self.minX = x
        self.minY = y
        self.maxX = x
        self.maxY = y
    }
    
    /// 从中心点和尺寸创建矩形
    public init(centerX: Double, centerY: Double, width: Double, height: Double) {
        self.minX = centerX - width / 2
        self.minY = centerY - height / 2
        self.maxX = centerX + width / 2
        self.maxY = centerY + height / 2
    }
    
    /// 宽度
    public var width: Double {
        return maxX - minX
    }
    
    /// 高度
    public var height: Double {
        return maxY - minY
    }
    
    /// 面积
    public var area: Double {
        return width * height
    }
    
    /// 中心点 X
    public var centerX: Double {
        return (minX + maxX) / 2
    }
    
    /// 中心点 Y
    public var centerY: Double {
        return (minY + maxY) / 2
    }
    
    /// 半宽度
    public var halfWidth: Double {
        return width / 2
    }
    
    /// 半高度
    public var halfHeight: Double {
        return height / 2
    }
    
    /// 是否为点（零面积）
    public var isPoint: Bool {
        return minX == maxX && minY == maxY
    }
    
    /// 是否有效（最小坐标小于等于最大坐标）
    public var isValid: Bool {
        return minX <= maxX && minY <= maxY
    }
    
    /// 检查是否包含另一个矩形
    public func contains(_ other: Rectangle) -> Bool {
        return minX <= other.minX && maxX >= other.maxX &&
               minY <= other.minY && maxY >= other.maxY
    }
    
    /// 检查是否包含点
    public func contains(x: Double, y: Double) -> Bool {
        return minX <= x && maxX >= x && minY <= y && maxY >= y
    }
    
    /// 检查是否与另一个矩形相交
    public func intersects(_ other: Rectangle) -> Bool {
        return minX <= other.maxX && maxX >= other.minX &&
               minY <= other.maxY && maxY >= other.minY
    }
    
    /// 计算与另一个矩形的交集
    public func intersection(_ other: Rectangle) -> Rectangle? {
        if !intersects(other) { return nil }
        
        return Rectangle(
            minX: max(minX, other.minX),
            minY: max(minY, other.minY),
            maxX: min(maxX, other.maxX),
            maxY: min(maxY, other.maxY)
        )
    }
    
    /// 计算与另一个矩形的交集面积
    public func intersectionArea(_ other: Rectangle) -> Double {
        return intersection(other)?.area ?? 0
    }
    
    /// 计算与另一个矩形的合并矩形
    public func union(_ other: Rectangle) -> Rectangle {
        return Rectangle(
            minX: min(minX, other.minX),
            minY: min(minY, other.minY),
            maxX: max(maxX, other.maxX),
            maxY: max(maxY, other.maxY)
        )
    }
    
    /// 计算合并后增加的面积
    public func enlargement(_ other: Rectangle) -> Double {
        return union(other).area - area
    }
    
    /// 计算两个矩形中心之间的距离
    public func distance(_ other: Rectangle) -> Double {
        let dx = centerX - other.centerX
        let dy = centerY - other.centerY
        return sqrt(dx * dx + dy * dy)
    }
    
    /// 计算到点的距离
    public func distance(x: Double, y: Double) -> Double {
        let dx = centerX - x
        let dy = centerY - y
        return sqrt(dx * dx + dy * dy)
    }
    
    /// 扩展矩形以包含另一个矩形
    public mutating func expand(_ other: Rectangle) {
        minX = min(minX, other.minX)
        minY = min(minY, other.minY)
        maxX = max(maxX, other.maxX)
        maxY = max(maxY, other.maxY)
    }
    
    /// 扩展矩形以包含点
    public mutating func expand(x: Double, y: Double) {
        minX = min(minX, x)
        minY = min(minY, y)
        maxX = max(maxX, x)
        maxY = max(maxY, y)
    }
    
    /// 创建空矩形（无效矩形）
    public static var empty: Rectangle {
        return Rectangle(minX: Double.infinity, minY: Double.infinity, 
                         maxX: -Double.infinity, maxY: -Double.infinity)
    }
    
    /// 创建全范围矩形
    public static var infinite: Rectangle {
        return Rectangle(minX: -Double.infinity, minY: -Double.infinity,
                         maxX: Double.infinity, maxY: Double.infinity)
    }
}

// MARK: - RTree Entry

/// R-tree 条目
public struct RTreeEntry<T>: Equatable where T: Equatable {
    /// 边界矩形
    public let rect: Rectangle
    /// 数据
    public let data: T
    
    public init(rect: Rectangle, data: T) {
        self.rect = rect
        self.data = data
    }
    
    /// 创建点条目
    public init(x: Double, y: Double, data: T) {
        self.rect = Rectangle(x: x, y: y)
        self.data = data
    }
    
    /// 从中心点和尺寸创建条目
    public init(centerX: Double, centerY: Double, width: Double, height: Double, data: T) {
        self.rect = Rectangle(centerX: centerX, centerY: centerY, width: width, height: height)
        self.data = data
    }
}

// MARK: - RTree Node

/// R-tree 节点
public class RTreeNode<T>: CustomStringConvertible where T: Equatable {
    /// 节点的边界矩形
    public private(set) var rect: Rectangle
    
    /// 子节点（内部节点）
    public private(set) var children: [RTreeNode<T>]?
    
    /// 数据条目（叶子节点）
    public private(set) var entries: [RTreeEntry<T>]?
    
    /// 是否为叶子节点
    public var isLeaf: Bool {
        return children == nil
    }
    
    /// 条目数量
    public var count: Int {
        return entries?.count ?? children?.count ?? 0
    }
    
    /// 父节点
    public weak var parent: RTreeNode<T>?
    
    /// 节点层级
    public var level: Int = 0
    
    /// 创建叶子节点
    public init(entries: [RTreeEntry<T>] = []) {
        self.rect = Rectangle.empty
        self.entries = entries
        self.children = nil
        
        updateRect()
    }
    
    /// 创建内部节点
    public init(children: [RTreeNode<T>] = []) {
        self.rect = Rectangle.empty
        self.entries = nil
        self.children = children
        
        for child in children {
            child.parent = self
        }
        
        updateRect()
    }
    
    /// 更新边界矩形
    public func updateRect() {
        if isLeaf {
            rect = entries?.reduce(Rectangle.empty) { $0.union($1.rect) } ?? Rectangle.empty
        } else {
            rect = children?.reduce(Rectangle.empty) { $0.union($1.rect) } ?? Rectangle.empty
        }
    }
    
    /// 添加条目（叶子节点）
    public func addEntry(_ entry: RTreeEntry<T>) {
        guard isLeaf else { return }
        entries?.append(entry)
        updateRect()
    }
    
    /// 添加子节点（内部节点）
    public func addChild(_ child: RTreeNode<T>) {
        guard !isLeaf else { return }
        child.parent = self
        child.level = level + 1
        children?.append(child)
        updateRect()
    }
    
    /// 移除条目
    public func removeEntry(at index: Int) -> RTreeEntry<T>? {
        guard isLeaf, let entries = entries, index < entries.count else { return nil }
        let removed = entries.remove(at: index)
        self.entries = entries
        updateRect()
        return removed
    }
    
    /// 移除子节点
    public func removeChild(at index: Int) -> RTreeNode<T>? {
        guard !isLeaf, let children = children, index < children.count else { return nil }
        let removed = children.remove(at: index)
        removed.parent = nil
        self.children = children
        updateRect()
        return removed
    }
    
    /// 清空节点
    public func clear() {
        if isLeaf {
            entries?.removeAll()
        } else {
            children?.forEach { $0.parent = nil }
            children?.removeAll()
        }
        rect = Rectangle.empty
    }
    
    /// 检查是否包含条目
    public func contains(_ entry: RTreeEntry<T>) -> Bool {
        return entries?.contains(entry) ?? false
    }
    
    /// 检查是否包含子节点
    public func contains(_ child: RTreeNode<T>) -> Bool {
        return children?.contains(child) ?? false
    }
    
    /// 查找条目索引
    public func indexOf(_ entry: RTreeEntry<T>) -> Int? {
        return entries?.firstIndex(of: entry)
    }
    
    /// 查找子节点索引
    public func indexOf(_ child: RTreeNode<T>) -> Int? {
        return children?.firstIndex(of: child)
    }
    
    public var description: String {
        if isLeaf {
            return "Leaf[level: \(level), entries: \(count), rect: \(rect)]"
        } else {
            return "Internal[level: \(level), children: \(count), rect: \(rect)]"
        }
    }
}

// MARK: - RTree Configuration

/// R-tree 配置参数
public struct RTreeConfig {
    /// 每个节点的最大条目数
    public let maxEntries: Int
    
    /// 每个节点的最小条目数
    public let minEntries: Int
    
    /// 分裂策略
    public let splitStrategy: SplitStrategy
    
    /// 创建配置
    public init(maxEntries: Int = 9, minEntries: Int? = nil, splitStrategy: SplitStrategy = .rstar) {
        self.maxEntries = max(2, maxEntries)
        self.minEntries = minEntries ?? max(1, maxEntries / 2)
        self.splitStrategy = splitStrategy
    }
    
    /// 默认配置
    public static var defaultConfig: RTreeConfig {
        return RTreeConfig()
    }
    
    /// 高性能配置（更大的节点）
    public static var highPerformance: RTreeConfig {
        return RTreeConfig(maxEntries: 16)
    }
    
    /// 低内存配置（更小的节点）
    public static var lowMemory: RTreeConfig {
        return RTreeConfig(maxEntries: 4)
    }
}

// MARK: - Split Strategy

/// 分裂策略
public enum SplitStrategy {
    /// 线性分裂（简单快速）
    case linear
    /// 二次分裂（更优的分组）
    case quadratic
    /// R*-tree 分裂（最优）
    case rstar
}

// MARK: - RTree

/// R-tree 空间索引
public final class RTree<T>: CustomStringConvertible where T: Equatable {
    /// 根节点
    public private(set) var root: RTreeNode<T>?
    
    /// 配置
    public let config: RTreeConfig
    
    /// 条目总数
    public private(set) var count: Int = 0
    
    /// 树的高度
    public var height: Int {
        return root?.level + 1
    }
    
    /// 是否为空
    public var isEmpty: Bool {
        return count == 0
    }
    
    /// 整体边界矩形
    public var bounds: Rectangle {
        return root?.rect ?? Rectangle.empty
    }
    
    /// 创建 R-tree
    public init(config: RTreeConfig = .defaultConfig) {
        self.config = config
    }
    
    /// 从条目数组创建 R-tree
    public init(entries: [RTreeEntry<T>], config: RTreeConfig = .defaultConfig) {
        self.config = config
        for entry in entries {
            insert(entry)
        }
    }
    
    // MARK: - Insert
    
    /// 插入条目
    public func insert(_ entry: RTreeEntry<T>) {
        if root == nil {
            root = RTreeNode<T>(entries: [])
        }
        
        let leaf = chooseLeaf(entry.rect)
        leaf.addEntry(entry)
        count += 1
        
        if leaf.count > config.maxEntries {
            split(leaf)
        } else {
            adjustBounds(leaf)
        }
    }
    
    /// 插入点数据
    public func insert(x: Double, y: Double, data: T) {
        insert(RTreeEntry(x: x, y: y, data: data))
    }
    
    /// 批量插入
    public func insert(_ entries: [RTreeEntry<T>]) {
        for entry in entries {
            insert(entry)
        }
    }
    
    /// 选择插入的叶子节点
    private func chooseLeaf(_ rect: Rectangle) -> RTreeNode<T> {
        guard let root = root else { return RTreeNode<T>() }
        
        var node = root
        
        while !node.isLeaf {
            var bestChild: RTreeNode<T>? = nil
            var minEnlargement = Double.infinity
            var minArea = Double.infinity
            
            for child in node.children ?? [] {
                let enlargement = child.rect.enlargement(rect)
                
                if enlargement < minEnlargement || 
                   (enlargement == minEnlargement && child.rect.area < minArea) {
                    minEnlargement = enlargement
                    minArea = child.rect.area
                    bestChild = child
                }
            }
            
            node = bestChild ?? node.children?.first ?? node
        }
        
        return node
    }
    
    // MARK: - Split
    
    /// 分裂节点
    private func split(_ node: RTreeNode<T>) {
        let groups = performSplit(node)
        
        if node.parent == nil {
            // 分裂根节点
            let newRoot = RTreeNode<T>(children: [])
            newRoot.level = node.level + 1
            
            let group1 = createNode(from: groups.group1, level: node.level, isLeaf: node.isLeaf)
            let group2 = createNode(from: groups.group2, level: node.level, isLeaf: node.isLeaf)
            
            newRoot.addChild(group1)
            newRoot.addChild(group2)
            
            root = newRoot
        } else {
            // 分裂子节点
            let parent = node.parent!
            let index = parent.indexOf(node) ?? 0
            parent.removeChild(at: index)
            
            let group1 = createNode(from: groups.group1, level: node.level, isLeaf: node.isLeaf)
            let group2 = createNode(from: groups.group2, level: node.level, isLeaf: node.isLeaf)
            
            parent.addChild(group1)
            parent.addChild(group2)
            
            if parent.count > config.maxEntries {
                split(parent)
            } else {
                adjustBounds(parent)
            }
        }
    }
    
    /// 执行分裂
    private func performSplit(_ node: RTreeNode<T>) -> (group1: [Any], group2: [Any]) {
        switch config.splitStrategy {
        case .linear:
            return linearSplit(node)
        case .quadratic:
            return quadraticSplit(node)
        case .rstar:
            return rstarSplit(node)
        }
    }
    
    /// 线性分裂
    private func linearSplit(_ node: RTreeNode<T>) -> (group1: [Any], group2: [Any]) {
        var items: [Any] = node.isLeaf ? 
            (node.entries ?? []).map { $0 as Any } : 
            (node.children ?? []).map { $0 as Any }
        
        // 找到沿每个轴的最大分离
        var bestAxis = 0
        var maxSeparation = 0.0
        
        // X 轴
        let minXVal = items.map { getMinX($0) }.min() ?? 0
        let maxXVal = items.map { getMaxX($0) }.max() ?? 0
        let xSeparation = maxXVal - minXVal
        
        // Y 轴
        let minYVal = items.map { getMinY($0) }.min() ?? 0
        let maxYVal = items.map { getMaxY($0) }.max() ?? 0
        let ySeparation = maxYVal - minYVal
        
        if ySeparation > xSeparation {
            bestAxis = 1
            maxSeparation = ySeparation
        } else {
            bestAxis = 0
            maxSeparation = xSeparation
        }
        
        // 沿选定轴排序
        if bestAxis == 0 {
            items.sort { getMinX($0) < getMinX($1) }
        } else {
            items.sort { getMinY($0) < getMinY($1) }
        }
        
        // 分配到两个组
        let mid = items.count / 2
        return (group1: items[0..<mid].map { $0 }, group2: items[mid..<items.count].map { $0 })
    }
    
    /// 二次分裂
    private func quadraticSplit(_ node: RTreeNode<T>) -> (group1: [Any], group2: [Any]) {
        var items: [Any] = node.isLeaf ? 
            (node.entries ?? []).map { $0 as Any } : 
            (node.children ?? []).map { $0 as Any }
        
        // 找到最大的组合面积
        var seed1 = 0
        var seed2 = 1
        var maxWaste = -Double.infinity
        
        for i in 0..<items.count {
            for j in (i+1)..<items.count {
                let rect1 = getRect(items[i])
                let rect2 = getRect(items[j])
                let combined = rect1.union(rect2)
                let waste = combined.area - rect1.area - rect2.area
                
                if waste > maxWaste {
                    maxWaste = waste
                    seed1 = i
                    seed2 = j
                }
            }
        }
        
        var group1: [Any] = [items[seed1]]
        var group2: [Any] = [items[seed2]]
        
        // 移除已分配的种子
        let removeIndices = seed1 > seed2 ? [seed1, seed2] : [seed2, seed1]
        for index in removeIndices {
            items.remove(at: index)
        }
        
        var rect1 = getRect(group1[0])
        var rect2 = getRect(group2[0])
        
        // 分配剩余条目
        for item in items {
            let itemRect = getRect(item)
            let enlargement1 = rect1.enlargement(itemRect)
            let enlargement2 = rect2.enlargement(itemRect)
            
            if enlargement1 < enlargement2 || 
               (enlargement1 == enlargement2 && rect1.area < rect2.area) {
                group1.append(item)
                rect1 = rect1.union(itemRect)
            } else {
                group2.append(item)
                rect2 = rect2.union(itemRect)
            }
            
            // 确保最小条目数
            if group1.count + items.count - (group1.count + group2.count - 2) == config.minEntries {
                // 将剩余全部放入 group1
                continue
            }
            if group2.count + items.count - (group1.count + group2.count - 2) == config.minEntries {
                // 将剩余全部放入 group2
                continue
            }
        }
        
        return (group1: group1, group2: group2)
    }
    
    /// R*-tree 分裂
    private func rstarSplit(_ node: RTreeNode<T>) -> (group1: [Any], group2: [Any]) {
        var items: [Any] = node.isLeaf ? 
            (node.entries ?? []).map { $0 as Any } : 
            (node.children ?? []).map { $0 as Any }
        
        let m = config.minEntries
        let M = config.maxEntries
        
        // 计算各轴的最小重叠
        var bestAxis = 0
        var minOverlap = Double.infinity
        var minArea = Double.infinity
        var bestDistribution = 0
        
        for axis in 0..<2 {
            // 沿轴排序（两种方向）
            let sortedLow = items.sorted { 
                axis == 0 ? getMinX($0) < getMinX($1) : getMinY($0) < getMinY($1) 
            }
            let sortedHigh = items.sorted { 
                axis == 0 ? getMaxX($0) < getMaxX($1) : getMaxY($0) < getMaxY($1) 
            }
            
            // 检查所有分布
            for k in m..<(M - m + 1) {
                // 低排序分布
                let group1Low = sortedLow[0..<k].map { $0 }
                let group2Low = sortedLow[k..<items.count].map { $0 }
                let overlapLow = computeOverlap(group1Low, group2Low)
                let areaLow = computeArea(group1Low) + computeArea(group2Low)
                
                if overlapLow < minOverlap || 
                   (overlapLow == minOverlap && areaLow < minArea) {
                    minOverlap = overlapLow
                    minArea = areaLow
                    bestAxis = axis
                    bestDistribution = k
                    items = sortedLow
                }
                
                // 高排序分布
                let group1High = sortedHigh[0..<k].map { $0 }
                let group2High = sortedHigh[k..<items.count].map { $0 }
                let overlapHigh = computeOverlap(group1High, group2High)
                let areaHigh = computeArea(group1High) + computeArea(group2High)
                
                if overlapHigh < minOverlap || 
                   (overlapHigh == minOverlap && areaHigh < minArea) {
                    minOverlap = overlapHigh
                    minArea = areaHigh
                    bestAxis = axis
                    bestDistribution = k
                    items = sortedHigh
                }
            }
        }
        
        let group1 = items[0..<bestDistribution].map { $0 }
        let group2 = items[bestDistribution..<items.count].map { $0 }
        
        return (group1: group1, group2: group2)
    }
    
    // MARK: - Helper Functions for Split
    
    private func getRect(_ item: Any) -> Rectangle {
        if let entry = item as? RTreeEntry<T> {
            return entry.rect
        } else if let node = item as? RTreeNode<T> {
            return node.rect
        }
        return Rectangle.empty
    }
    
    private func getMinX(_ item: Any) -> Double { return getRect(item).minX }
    private func getMaxX(_ item: Any) -> Double { return getRect(item).maxX }
    private func getMinY(_ item: Any) -> Double { return getRect(item).minY }
    private func getMaxY(_ item: Any) -> Double { return getRect(item).maxY }
    
    private func computeOverlap(_ group1: [Any], _ group2: [Any]) -> Double {
        let rect1 = group1.reduce(Rectangle.empty) { $0.union(getRect($1)) }
        let rect2 = group2.reduce(Rectangle.empty) { $0.union(getRect($1)) }
        return rect1.intersectionArea(rect2)
    }
    
    private func computeArea(_ group: [Any]) -> Double {
        return group.reduce(Rectangle.empty) { $0.union(getRect($1)) }.area
    }
    
    private func createNode(from items: [Any], level: Int, isLeaf: Bool) -> RTreeNode<T> {
        if isLeaf {
            let entries = items.compactMap { $0 as? RTreeEntry<T> }
            let node = RTreeNode<T>(entries: entries)
            node.level = level
            return node
        } else {
            let children = items.compactMap { $0 as? RTreeNode<T> }
            let node = RTreeNode<T>(children: children)
            node.level = level
            return node
        }
    }
    
    // MARK: - Adjust Bounds
    
    /// 向上调整边界
    private func adjustBounds(_ node: RTreeNode<T>) {
        var current: RTreeNode<T>? = node
        
        while current != nil {
            current?.updateRect()
            current = current?.parent
        }
    }
    
    // MARK: - Search
    
    /// 搜索范围内的条目
    public func search(_ rect: Rectangle) -> [RTreeEntry<T>] {
        var results: [RTreeEntry<T>] = []
        searchInNode(root, rect, &results)
        return results
    }
    
    /// 搜索范围内的数据
    public func searchData(_ rect: Rectangle) -> [T] {
        return search(rect).map { $0.data }
    }
    
    /// 搜索包含指定点的条目
    public func searchContaining(x: Double, y: Double) -> [RTreeEntry<T>] {
        let rect = Rectangle(x: x, y: y)
        return search(rect).filter { $0.rect.contains(x: x, y: y) }
    }
    
    /// 搜索包含指定点的数据
    public func searchContainingData(x: Double, y: Double) -> [T] {
        return searchContaining(x: x, y: y).map { $0.data }
    }
    
    /// 搜索与矩形相交的条目
    public func searchIntersecting(_ rect: Rectangle) -> [RTreeEntry<T>] {
        return search(rect).filter { $0.rect.intersects(rect) }
    }
    
    /// 搜索与矩形相交的数据
    public func searchIntersectingData(_ rect: Rectangle) -> [T] {
        return searchIntersecting(rect).map { $0.data }
    }
    
    /// 递归搜索
    private func searchInNode(_ node: RTreeNode<T>?, _ rect: Rectangle, _ results: inout [RTreeEntry<T>]) {
        guard let node = node, node.rect.intersects(rect) else { return }
        
        if node.isLeaf {
            for entry in node.entries ?? [] {
                if entry.rect.intersects(rect) {
                    results.append(entry)
                }
            }
        } else {
            for child in node.children ?? [] {
                searchInNode(child, rect, &results)
            }
        }
    }
    
    // MARK: - Nearest Neighbor Search
    
    /// 查找最近的 K 个条目
    public func nearest(x: Double, y: Double, k: Int = 1) -> [RTreeEntry<T>] {
        if k <= 0 || isEmpty { return [] }
        
        var results: [(entry: RTreeEntry<T>, distance: Double)] = []
        nearestSearch(root, x, y, k, &results)
        
        results.sort { $0.distance < $1.distance }
        return results.map { $0.entry }
    }
    
    /// 查找最近的 K 个数据
    public func nearestData(x: Double, y: Double, k: Int = 1) -> [T] {
        return nearest(x: x, y: y, k: k).map { $0.data }
    }
    
    /// 递归最近邻搜索
    private func nearestSearch(_ node: RTreeNode<T>?, _ x: Double, _ y: Double, _ k: Int,
                               _ results: inout [(entry: RTreeEntry<T>, distance: Double)]) {
        guard let node = node else { return }
        
        if node.isLeaf {
            for entry in node.entries ?? [] {
                let dist = entry.rect.distance(x: x, y: y)
                results.append((entry: entry, distance: dist))
            }
        } else {
            // 按最小距离排序子节点
            let sortedChildren = (node.children ?? []).sorted { 
                $0.rect.distance(x: x, y: y) < $1.rect.distance(x: x, y: y)
            }
            
            for child in sortedChildren {
                // 剪枝：如果最小可能距离大于当前第 k 个结果的距离，跳过
                if results.count >= k {
                    let maxDist = results.sorted { $0.distance < $1.distance }[min(k, results.count) - 1].distance
                    if child.rect.distance(x: x, y: y) > maxDist {
                        continue
                    }
                }
                
                nearestSearch(child, x, y, k, &results)
            }
        }
    }
    
    // MARK: - Remove
    
    /// 移除条目
    public func remove(_ entry: RTreeEntry<T>) -> Bool {
        guard let leaf = findLeaf(entry) else { return false }
        
        if let index = leaf.indexOf(entry) {
            leaf.removeEntry(at: index)
            count -= 1
            
            condenseTree(leaf)
            
            if root?.count == 1 && !root!.isLeaf {
                root = root?.children?.first
                root?.parent = nil
            }
            
            if count == 0 {
                root = nil
            }
            
            return true
        }
        
        return false
    }
    
    /// 移除指定数据（匹配矩形）
    public func remove(rect: Rectangle, data: T) -> Bool {
        let entries = search(rect).filter { $0.data == data }
        for entry in entries {
            if remove(entry) {
                return true
            }
        }
        return false
    }
    
    /// 查找包含条目的叶子节点
    private func findLeaf(_ entry: RTreeEntry<T>) -> RTreeNode<T>? {
        return findLeafInNode(root, entry)
    }
    
    private func findLeafInNode(_ node: RTreeNode<T>?, _ entry: RTreeEntry<T>) -> RTreeNode<T>? {
        guard let node = node, node.rect.intersects(entry.rect) else { return nil }
        
        if node.isLeaf {
            if node.contains(entry) {
                return node
            }
        } else {
            for child in node.children ?? [] {
                if let found = findLeafInNode(child, entry) {
                    return found
                }
            }
        }
        
        return nil
    }
    
    /// 压缩树（移除节点后重新组织）
    private func condenseTree(_ node: RTreeNode<T>) {
        var current: RTreeNode<T>? = node
        var orphaned: [RTreeNode<T>] = []
        
        while current != nil {
            if current!.count < config.minEntries && current!.parent != nil {
                // 节点条目不足，移除并收集孤立的条目
                let parent = current!.parent!
                if let index = parent.indexOf(current!) {
                    parent.removeChild(at: index)
                }
                orphaned.append(current!)
            } else {
                adjustBounds(current!)
            }
            
            current = current?.parent
        }
        
        // 重新插入孤立的条目
        for orphan in orphaned {
            if orphan.isLeaf {
                for entry in orphan.entries ?? [] {
                    insert(entry)
                    count -= 1  // 因为 insert 会增加 count
                }
            } else {
                for child in orphan.children ?? [] {
                    reinsertSubtree(child)
                }
            }
        }
    }
    
    /// 重新插入子树
    private func reinsertSubtree(_ node: RTreeNode<T>) {
        if node.isLeaf {
            for entry in node.entries ?? [] {
                insert(entry)
                count -= 1
            }
        } else {
            for child in node.children ?? [] {
                reinsertSubtree(child)
            }
        }
    }
    
    // MARK: - Clear
    
    /// 清空树
    public func clear() {
        root = nil
        count = 0
    }
    
    // MARK: - Statistics
    
    /// 统计节点数量
    public func nodeCount() -> Int {
        return countNodes(root)
    }
    
    private func countNodes(_ node: RTreeNode<T>?) -> Int {
        guard let node = node else { return 0 }
        
        if node.isLeaf {
            return 1
        } else {
            return 1 + (node.children ?? []).reduce(0) { $0 + countNodes($1) }
        }
    }
    
    /// 统计叶子节点数量
    public func leafCount() -> Int {
        return countLeaves(root)
    }
    
    private func countLeaves(_ node: RTreeNode<T>?) -> Int {
        guard let node = node else { return 0 }
        
        if node.isLeaf {
            return 1
        } else {
            return (node.children ?? []).reduce(0) { $0 + countLeaves($1) }
        }
    }
    
    /// 计算平均填充率
    public func averageFillRatio() -> Double {
        guard count > 0, let root = root else { return 0 }
        
        var totalEntries = 0
        var totalNodes = 0
        
        countStats(root, &totalEntries, &totalNodes)
        
        return Double(totalEntries) / (Double(totalNodes) * Double(config.maxEntries))
    }
    
    private func countStats(_ node: RTreeNode<T>, _ entries: inout Int, _ nodes: inout Int) {
        nodes += 1
        entries += node.count
        
        if !node.isLeaf {
            for child in node.children ?? [] {
                countStats(child, &entries, &nodes)
            }
        }
    }
    
    // MARK: - Traversal
    
    /// 遍历所有条目
    public func forEach(_ callback: (RTreeEntry<T>) -> Void) {
        traverseNode(root, callback)
    }
    
    private func traverseNode(_ node: RTreeNode<T>?, _ callback: (RTreeEntry<T>) -> Void) {
        guard let node = node else { return }
        
        if node.isLeaf {
            for entry in node.entries ?? [] {
                callback(entry)
            }
        } else {
            for child in node.children ?? [] {
                traverseNode(child, callback)
            }
        }
    }
    
    /// 获取所有条目
    public func allEntries() -> [RTreeEntry<T>] {
        var entries: [RTreeEntry<T>] = []
        forEach { entries.append($0) }
        return entries
    }
    
    /// 获取所有数据
    public func allData() -> [T] {
        return allEntries().map { $0.data }
    }
    
    // MARK: - Description
    
    public var description: String {
        return "RTree[count: \(count), height: \(height), bounds: \(bounds)]"
    }
    
    /// 打印树结构
    public func printTree() {
        printNode(root, 0)
    }
    
    private func printNode(_ node: RTreeNode<T>?, _ depth: Int) {
        guard let node = node else { return }
        
        let indent = String(repeating: "  ", count: depth)
        print("\(indent)\(node)")
        
        if node.isLeaf {
            for entry in node.entries ?? [] {
                print("\(indent)  Entry: \(entry.rect)")
            }
        } else {
            for child in node.children ?? [] {
                printNode(child, depth + 1)
            }
        }
    }
}

// MARK: - RTree Builder

/// R-tree 构建器
public struct RTreeBuilder<T> where T: Equatable {
    private var entries: [RTreeEntry<T>] = []
    private var config: RTreeConfig = .defaultConfig
    
    /// 添加条目
    public func add(_ entry: RTreeEntry<T>) -> RTreeBuilder<T> {
        var builder = self
        builder.entries.append(entry)
        return builder
    }
    
    /// 添加点
    public func add(x: Double, y: Double, data: T) -> RTreeBuilder<T> {
        return add(RTreeEntry(x: x, y: y, data: data))
    }
    
    /// 添加矩形
    public func add(rect: Rectangle, data: T) -> RTreeBuilder<T> {
        return add(RTreeEntry(rect: rect, data: data))
    }
    
    /// 设置配置
    public func withConfig(_ config: RTreeConfig) -> RTreeBuilder<T> {
        var builder = self
        builder.config = config
        return builder
    }
    
    /// 构建 R-tree
    public func build() -> RTree<T> {
        return RTree<T>(entries: entries, config: config)
    }
}

// MARK: - Extensions

extension RTreeEntry: Codable where T: Codable {
    public init(from decoder: Decoder) throws {
        let container = try decoder.container(keyedBy: CodingKeys.self)
        rect = try container.decode(Rectangle.self, forKey: .rect)
        data = try container.decode(T.self, forKey: .data)
    }
    
    public func encode(to encoder: Encoder) throws {
        var container = encoder.container(keyedBy: CodingKeys.self)
        try container.encode(rect, forKey: .rect)
        try container.encode(data, forKey: .data)
    }
    
    private enum CodingKeys: String, CodingKey {
        case rect, data
    }
}

// MARK: - Spatial Query Helpers

/// 空间查询辅助工具
public struct SpatialQuery<T> where T: Equatable {
    private let rtree: RTree<T>
    
    public init(_ rtree: RTree<T>) {
        self.rtree = rtree
    }
    
    /// 查找矩形内的所有条目
    public func within(_ rect: Rectangle) -> [RTreeEntry<T>] {
        return rtree.search(rect)
    }
    
    /// 查找矩形内的所有数据
    public func withinData(_ rect: Rectangle) -> [T] {
        return rtree.searchData(rect)
    }
    
    /// 查找与矩形相交的条目
    public func intersecting(_ rect: Rectangle) -> [RTreeEntry<T>] {
        return rtree.searchIntersecting(rect)
    }
    
    /// 查找最近的条目
    public func nearest(x: Double, y: Double, k: Int = 1) -> [RTreeEntry<T>] {
        return rtree.nearest(x: x, y: y, k: k)
    }
    
    /// 查找半径范围内的条目
    public func withinRadius(x: Double, y: Double, radius: Double) -> [RTreeEntry<T>] {
        let rect = Rectangle(
            minX: x - radius,
            minY: y - radius,
            maxX: x + radius,
            maxY: y + radius
        )
        
        return rtree.search(rect).filter { entry in
            let dx = entry.rect.centerX - x
            let dy = entry.rect.centerY - y
            return sqrt(dx * dx + dy * dy) <= radius
        }
    }
    
    /// 查找圆内的数据
    public func withinRadiusData(x: Double, y: Double, radius: Double) -> [T] {
        return withinRadius(x: x, y: y, radius: radius).map { $0.data }
    }
    
    /// 查找多边形内的条目（简单矩形多边形）
    public func withinPolygon(_ points: [(Double, Double)]) -> [RTreeEntry<T>] {
        guard points.count >= 3 else { return [] }
        
        // 计算边界矩形
        let minX = points.map { $0.0 }.min() ?? 0
        let maxX = points.map { $0.0 }.max() ?? 0
        let minY = points.map { $0.1 }.min() ?? 0
        let maxY = points.map { $0.1 }.max() ?? 0
        
        let bounds = Rectangle(minX: minX, minY: minY, maxX: maxX, maxY: maxY)
        
        // 先用边界矩形筛选，再用精确多边形检测
        return rtree.search(bounds).filter { entry in
            return pointInPolygon(entry.rect.centerX, entry.rect.centerY, points)
        }
    }
    
    /// 点是否在多边形内
    private func pointInPolygon(_ x: Double, _ y: Double, _ points: [(Double, Double)]) -> Bool {
        var inside = false
        let n = points.count
        
        for i in 0..<n {
            let j = (i + 1) % n
            let xi = points[i].0, yi = points[i].1
            let xj = points[j].0, yj = points[j].1
            
            if ((yi > y) != (yj > y)) &&
               (x < (xj - xi) * (y - yi) / (yj - yi) + xi) {
                inside = !inside
            }
        }
        
        return inside
    }
}