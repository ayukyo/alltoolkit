# Graph Utils - Lua 图算法工具库

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

完整的图数据结构和算法实现，支持有向图和无向图的常见操作。零外部依赖，仅使用 Lua 标准库。

## 特性

### 图类型
- **无向图** (Undirected Graph)
- **有向图** (Directed Graph)
- **带权图** (Weighted Graph)

### 图表示
- 邻接表实现
- 支持任意类型的顶点（字符串、数字等）

### 核心算法

| 类别 | 算法 | 说明 |
|------|------|------|
| **遍历** | BFS | 广度优先搜索，支持回调 |
| | DFS (迭代) | 深度优先搜索，迭代实现 |
| | DFS (递归) | 深度优先搜索，递归实现 |
| | 层序遍历 | 按层级返回顶点列表 |
| **最短路径** | Dijkstra | 单源最短路径（非负权） |
| | Bellman-Ford | 单源最短路径（支持负权） |
| | Floyd-Warshall | 全源最短路径 |
| **最小生成树** | Kruskal | 基于并查集的 MST 算法 |
| | Prim | 基于贪心的 MST 算法 |
| **拓扑排序** | DFS 拓扑排序 | 基于后序遍历 |
| | Kahn 算法 | BFS 入度消减法 |
| **连通性** | 连通分量 | 无向图连通分量检测 |
| | 强连通分量 | Kosaraju 算法 |
| **环检测** | hasCycle | 环存在检测 |
| | findCycles | 查找所有环 |
| | isDAG | 有向无环图判断 |
| **其他** | 二分图检测 | 染色法 |
| | 欧拉路径 | Hierholzer 算法 |
| | 图直径 | 最长最短路径 |

### 图操作
- 添加/删除顶点
- 添加/删除边
- 查询邻居
- 获取度数（入度/出度）
- 克隆图
- 序列化/反序列化

## 安装

```lua
local GraphUtils = dofile("path/to/graph_utils/mod.lua")
```

## 快速开始

### 创建图

```lua
local GraphUtils = dofile("graph_utils/mod.lua")

-- 创建无向图
local g = GraphUtils.undirected()

-- 创建有向图
local g = GraphUtils.directed()

-- 创建带权图
local g = GraphUtils.directed(true)
```

### 基本操作

```lua
-- 添加顶点
g:addVertex("A")
g:addVertex("B")

-- 添加边（自动创建顶点）
g:addEdge("A", "B")
g:addEdge("B", "C", 5)  -- 带权重

-- 查询
print(g:hasEdge("A", "B"))      -- true
print(g:getWeight("A", "B"))    -- nil 或权重值
print(g:getDegree("B"))          -- 度数

-- 获取邻居
local neighbors = g:getNeighbors("A")

-- 删除
g:removeEdge("A", "B")
g:removeVertex("A")
```

### 遍历算法

```lua
-- BFS
local order = g:bfs("A")
g:bfs("A", function(vertex, depth)
    print("访问:", vertex, "深度:", depth)
end)

-- DFS
local order = g:dfs("A")           -- 迭代版
local order = g:dfsRecursive("A")  -- 递归版

-- 层序遍历
local levels = g:bfsLevelOrder("A")
-- 返回: {{层1顶点}, {层2顶点}, ...}
```

### 最短路径

```lua
-- Dijkstra 算法
local distances, predecessors = g:dijkstra("A")
print("A 到 C 的距离:", distances["C"])

-- 获取路径
local path, dist = g:getShortestPath("A", "C")
-- path = {"A", "B", "C"}

-- Bellman-Ford（支持负权边）
local distances, preds, hasNegCycle = g:bellmanFord("A")

-- Floyd-Warshall（全源最短路径）
local allDist = g:floydWarshall()
print("A 到 B:", allDist["A"]["B"])
```

### 最小生成树

```lua
-- Kruskal 算法
local mst, weight, success = g:kruskal()
for _, edge in ipairs(mst) do
    print(edge.from, "->", edge.to, ":", edge.weight)
end
print("总权重:", weight)

-- Prim 算法
local mst, weight, success = g:prim("A")
```

### 拓扑排序

```lua
-- DFS 拓扑排序
local order = g:topologicalSort()
if order then
    print("拓扑序:", table.concat(order, " -> "))
else
    print("图中存在环")
end

-- Kahn 算法
local order = g:kahnSort()
```

### 连通性检测

```lua
-- 连通分量
local components = g:connectedComponents()
for i, comp in ipairs(components) do
    print("分量", i, ":", table.concat(comp, ", "))
end

-- 是否连通
if g:isConnected() then
    print("图是连通的")
end

-- 强连通分量（有向图）
local sccs = g:stronglyConnectedComponents()
```

### 环检测

```lua
-- 检测是否有环
if g:hasCycle() then
    print("图中存在环")
end

-- 是否为 DAG
if g:isDAG() then
    print("是有向无环图")
end

-- 查找所有环
local cycles = g:findCycles()
```

### 其他算法

```lua
-- 二分图检测
local isBipartite, partitions = g:isBipartite()
if isBipartite then
    print("左分区:", table.concat(partitions.left, ", "))
    print("右分区:", table.concat(partitions.right, ", "))
end

-- 欧拉路径
local path = g:getEulerianPath()

-- 图直径
local diameter, info = g:getDiameter()
```

### 工厂函数

```lua
-- 从边列表创建
local g = GraphUtils.fromEdgeList(
    {{"A", "B", 1}, {"B", "C", 2}},
    GraphUtils.GraphType.UNDIRECTED,
    true  -- 带权
)

-- 从邻接矩阵创建
local matrix = {
    {0, 1, 2},
    {0, 0, 3},
    {0, 0, 0},
}
local g = GraphUtils.fromAdjacencyMatrix(matrix, {"A", "B", "C"})
```

## API 参考

### Graph 类

#### 属性
- `vertexCount` - 顶点数量
- `edgeCount` - 边数量
- `graphType` - 图类型 ("undirected" 或 "directed")
- `weighted` - 是否带权

#### 方法

| 方法 | 说明 | 返回值 |
|------|------|--------|
| `addVertex(v)` | 添加顶点 | self |
| `removeVertex(v)` | 删除顶点 | boolean |
| `addEdge(from, to, weight?)` | 添加边 | self |
| `removeEdge(from, to)` | 删除边 | boolean |
| `hasEdge(from, to)` | 边是否存在 | boolean |
| `getWeight(from, to)` | 获取权重 | number\|nil |
| `getNeighbors(v)` | 获取邻居 | table |
| `getVertices()` | 获取所有顶点 | table |
| `getEdges()` | 获取所有边 | table |
| `getDegree(v)` | 获取度数 | number |
| `getInDegree(v)` | 获取入度 | number |
| `isEmpty()` | 是否空图 | boolean |
| `clear()` | 清空图 | - |
| `clone()` | 克隆图 | Graph |
| `toTable()` | 导出为表 | table |
| `fromTable(t)` | 从表导入 | Graph |

#### 遍历算法

| 方法 | 说明 | 返回值 |
|------|------|--------|
| `bfs(start, callback?)` | 广度优先搜索 | table |
| `dfs(start, callback?)` | 深度优先搜索（迭代） | table |
| `dfsRecursive(start, callback?)` | 深度优先搜索（递归） | table |
| `bfsLevelOrder(start)` | 层序遍历 | table |

#### 最短路径

| 方法 | 说明 | 返回值 |
|------|------|--------|
| `dijkstra(start)` | Dijkstra 算法 | distances, predecessors |
| `getShortestPath(from, to)` | 获取最短路径 | path, distance |
| `bellmanFord(start)` | Bellman-Ford 算法 | distances, predecessors, hasNegCycle |
| `floydWarshall()` | Floyd-Warshall 算法 | distance_matrix |

#### 最小生成树

| 方法 | 说明 | 返回值 |
|------|------|--------|
| `kruskal()` | Kruskal 算法 | mst, weight, success |
| `prim(start?)` | Prim 算法 | mst, weight, success |

#### 拓扑排序

| 方法 | 说明 | 返回值 |
|------|------|--------|
| `topologicalSort()` | DFS 拓扑排序 | table\|nil |
| `kahnSort()` | Kahn 算法 | table\|nil |

#### 连通性

| 方法 | 说明 | 返回值 |
|------|------|--------|
| `connectedComponents()` | 连通分量 | table |
| `isConnected()` | 是否连通 | boolean |
| `stronglyConnectedComponents()` | 强连通分量 | table |

#### 环检测

| 方法 | 说明 | 返回值 |
|------|------|--------|
| `hasCycle()` | 是否有环 | boolean |
| `findCycles()` | 查找所有环 | table |
| `isDAG()` | 是否为 DAG | boolean |

#### 其他

| 方法 | 说明 | 返回值 |
|------|------|--------|
| `isBipartite()` | 是否为二分图 | boolean, partitions |
| `getEulerianPath()` | 欧拉路径 | table\|nil |
| `getDiameter()` | 图直径 | diameter, info |

### 工厂函数

```lua
GraphUtils.undirected(weighted?)     -- 创建无向图
GraphUtils.directed(weighted?)        -- 创建有向图
GraphUtils.fromEdgeList(edges, type, weighted?)  -- 从边列表创建
GraphUtils.fromAdjacencyMatrix(matrix, names?, type?)  -- 从邻接矩阵创建
```

## 时间复杂度

| 算法 | 时间复杂度 | 空间复杂度 |
|------|-----------|-----------|
| BFS / DFS | O(V + E) | O(V) |
| Dijkstra | O(V²) | O(V) |
| Bellman-Ford | O(V × E) | O(V) |
| Floyd-Warshall | O(V³) | O(V²) |
| Kruskal | O(E log E) | O(V) |
| Prim | O(V²) | O(V) |
| 拓扑排序 | O(V + E) | O(V) |
| 连通分量 | O(V + E) | O(V) |
| 强连通分量 | O(V + E) | O(V) |
| 环检测 | O(V + E) | O(V) |

其中 V 为顶点数，E 为边数。

## 示例

更多示例请参见 `examples/` 目录。

## 许可证

MIT License