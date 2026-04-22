# Graph Utils - Go 图算法工具库

零外部依赖、纯 Go 标准库实现的完整图数据结构与算法工具。

## 特性

### 图类型
- **无向图 (Undirected)** - 双向边
- **有向图 (Directed)** - 单向边

### 核心功能

#### 基本操作
- `NewGraph(vertices, type)` - 创建图
- `AddEdge(from, to, weight)` - 添加边
- `AddEdges([]Edge)` - 批量添加边
- `RemoveEdge(from, to)` - 删除边
- `HasEdge(from, to)` - 检查边是否存在
- `GetNeighbors(v)` - 获取邻接顶点
- `GetAllEdges()` - 获取所有边
- `Degree(v)` / `InDegree(v)` - 度数计算

#### 图遍历
- `BFS(start)` - 广度优先搜索
- `DFS(start)` - 深度优先搜索（递归）
- `DFSIterative(start)` - 深度优先搜索（迭代）

#### 最短路径
- `Dijkstra(source)` - Dijkstra 算法（非负权重）
- `BellmanFord(source)` - Bellman-Ford 算法（支持负权重）
- `ShortestPathResult.GetPath(target)` - 路径重建

#### 拓扑排序
- `TopologicalSort()` - 拓扑排序（仅 DAG）

#### 环检测
- `HasCycle()` - 环检测（有向/无向）

#### 连通性
- `ConnectedComponents()` - 连通分量
- `IsConnected()` - 连通性检查

#### 最小生成树
- `Kruskal()` - Kruskal 算法
- `Prim(start)` - Prim 算法

#### 二分图
- `Bipartite()` - 二分图检测与着色

#### 图操作
- `Clone()` - 深拷贝
- `Transpose()` - 转置图（仅限有向图）

## 安装

```bash
go get github.com/ayukyo/alltoolkit/Go/graph_utils
```

## 快速开始

### 创建图并添加边

```go
package main

import (
    "fmt"
    "graph_utils"
)

func main() {
    // 创建无向图
    g := graph_utils.NewGraph(5, graph_utils.Undirected)
    
    // 添加边
    g.AddEdge(0, 1, 1.0)
    g.AddEdge(1, 2, 2.0)
    g.AddEdge(2, 3, 3.0)
    
    fmt.Printf("Vertices: %d, Edges: %d\n", g.Vertices(), g.Edges())
}
```

### 广度优先搜索 (BFS)

```go
g := graph_utils.NewGraph(6, graph_utils.Undirected)
g.AddEdge(0, 1, 1.0)
g.AddEdge(0, 2, 1.0)
g.AddEdge(1, 3, 1.0)
g.AddEdge(2, 4, 1.0)

result, _ := g.BFS(0)
fmt.Println("BFS order:", result) // [0 1 2 3 4]
```

### Dijkstra 最短路径

```go
g := graph_utils.NewGraph(5, graph_utils.Directed)
g.AddEdge(0, 1, 10.0)
g.AddEdge(0, 2, 3.0)
g.AddEdge(1, 2, 1.0)
g.AddEdge(2, 3, 2.0)

result, _ := g.Dijkstra(0)
fmt.Println("Distance to 3:", result.Distances[3])
path := result.GetPath(3)
fmt.Println("Path:", path)
```

### 拓扑排序

```go
g := graph_utils.NewGraph(6, graph_utils.Directed)
g.AddEdge(5, 2, 1.0)
g.AddEdge(5, 0, 1.0)
g.AddEdge(4, 0, 1.0)
g.AddEdge(4, 1, 1.0)
g.AddEdge(2, 3, 1.0)
g.AddEdge(3, 1, 1.0)

order, err := g.TopologicalSort()
if err != nil {
    fmt.Println("Graph has cycle")
} else {
    fmt.Println("Topological order:", order)
}
```

### 最小生成树

```go
g := graph_utils.NewGraph(4, graph_utils.Undirected)
g.AddEdge(0, 1, 10.0)
g.AddEdge(0, 2, 6.0)
g.AddEdge(0, 3, 5.0)
g.AddEdge(1, 3, 15.0)
g.AddEdge(2, 3, 4.0)

// Kruskal
mst, _ := g.Kruskal()
fmt.Printf("MST weight: %.1f\n", mst.Weight)

// Prim
mst2, _ := g.Prim(0)
fmt.Printf("MST edges: %d\n", len(mst2.Edges))
```

### 连通分量

```go
g := graph_utils.NewGraph(9, graph_utils.Undirected)
g.AddEdge(0, 1, 1.0)
g.AddEdge(1, 2, 1.0)
g.AddEdge(4, 5, 1.0)
g.AddEdge(7, 8, 1.0)

components := g.ConnectedComponents()
fmt.Printf("Components: %d\n", len(components)) // 3
```

### 二分图检测

```go
g := graph_utils.NewGraph(4, graph_utils.Undirected)
g.AddEdge(0, 1, 1.0)
g.AddEdge(1, 2, 1.0)
g.AddEdge(2, 3, 1.0)
g.AddEdge(3, 0, 1.0)

isBipartite, colors := g.Bipartite()
fmt.Println("Is bipartite:", isBipartite) // true
fmt.Println("Colors:", colors) // [0 1 0 1]
```

## 示例

查看 `examples/` 目录获取完整示例：

- `basic.go` - 基本操作
- `traversal.go` - BFS/DFS 遍历
- `shortest_path.go` - 最短路径算法
- `topological_sort.go` - 拓扑排序
- `mst.go` - 最小生成树
- `components.go` - 连通分量与二分图
- `social_network.go` - 社交网络分析

## 算法复杂度

| 操作 | 时间复杂度 | 空间复杂度 |
|------|-----------|-----------|
| AddEdge | O(1) | O(1) |
| HasEdge | O(degree) | O(1) |
| BFS | O(V + E) | O(V) |
| DFS | O(V + E) | O(V) |
| Dijkstra | O((V + E) log V) | O(V) |
| BellmanFord | O(V × E) | O(V) |
| TopologicalSort | O(V + E) | O(V) |
| HasCycle | O(V + E) | O(V) |
| ConnectedComponents | O(V + E) | O(V) |
| Kruskal | O(E log E) | O(V) |
| Prim | O(E log V) | O(V) |
| Bipartite | O(V + E) | O(V) |

## 许可证

MIT License