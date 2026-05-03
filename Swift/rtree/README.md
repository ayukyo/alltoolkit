# R-tree 空间索引

R-tree 是一种用于空间索引的树形数据结构，特别适合存储和查询二维空间中的对象（如点、矩形、多边形等）。

## 核心功能

### Rectangle（矩形/边界框）
- 创建：从坐标、中心点、尺寸创建矩形
- 计算：宽度、高度、面积、中心点
- 检测：包含、相交、距离计算
- 操作：交集、合并、扩展

### RTree（R-tree 树）
- 插入：点数据、矩形数据、批量插入
- 搜索：范围搜索、相交搜索、包含点搜索
- 最近邻：K近邻查询
- 移除：精确移除、条件移除
- 统计：节点数、叶子数、填充率

### SpatialQuery（空间查询）
- 范围查询：矩形内、圆内、多边形内
- 最近邻：K近邻、半径内
- 相交查询：与矩形相交的对象

## 使用示例

```swift
// 创建 R-tree
let rtree = RTree<String>(config: RTreeConfig(maxEntries: 8))

// 插入数据
rtree.insert(x: 116.4, y: 39.9, data: "北京")
rtree.insert(x: 121.5, y: 31.2, data: "上海")

// 范围搜索
let area = Rectangle(minX: 115, minY: 30, maxX: 125, maxY: 45)
let cities = rtree.search(area)

// 最近邻查询
let nearest = rtree.nearest(x: 118, y: 35, k: 3)

// 使用 SpatialQuery
let query = SpatialQuery(rtree)
let nearby = query.withinRadius(x: 120, y: 32, radius: 100)
```

## 分裂策略

支持三种分裂策略：
- **Linear**：线性分裂，速度快但分组质量一般
- **Quadratic**：二次分裂，分组质量较好
- **R\***：R*-tree 分裂，最优分组质量

## 配置参数

```swift
RTreeConfig(
    maxEntries: 9,       // 每个节点最大条目数
    minEntries: 4,       // 每个节点最小条目数
    splitStrategy: .rstar // 分裂策略
)
```

预定义配置：
- `.defaultConfig`：标准配置（maxEntries: 9）
- `.highPerformance`：高性能配置（maxEntries: 16）
- `.lowMemory`：低内存配置（maxEntries: 4）

## 应用场景

1. **地理位置索引**：存储城市、商店等位置数据
2. **游戏碰撞检测**：快速检测物体间的碰撞
3. **地图标注**：管理地图上的标注点
4. **空间范围查询**：查找特定区域内的对象
5. **最近邻搜索**：查找距离最近的 K 个对象

## 性能特点

- 时间复杂度：
  - 插入：O(log n)
  - 搜索：O(log n + k)，k 为结果数量
  - 最近邻：O(log n + k)
- 空间复杂度：O(n)

## 文件结构

```
Swift/rtree/
├── mod.swift           # 主模块（Rectangle、RTree、SpatialQuery）
├── rtree_test.swift    # 测试套件
├── examples/
│   └── usage_examples.swift  # 使用示例
└── README.md           # 说明文档
```

## 测试覆盖

- 矩形操作测试
- 插入和查询测试
- 最近邻搜索测试
- 移除操作测试
- 统计信息测试
- 边界情况测试
- 不同分裂策略测试

## 零依赖

纯 Swift 实现，无外部依赖。