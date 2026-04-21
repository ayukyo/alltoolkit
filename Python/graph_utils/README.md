# Graph Utils - 图论算法工具包

完整的图论算法实现，零外部依赖，仅使用 Python 标准库。

## ✨ 功能特性

### 📊 图数据结构
- `Graph` 类：支持有向/无向、带权/无权图
- 邻接表内部表示，支持任意可哈希节点类型
- 完整的增删改查操作
- 邻接矩阵转换

### 🔍 遍历算法
- **BFS** - 广度优先搜索
- **DFS** - 深度优先搜索（递归/迭代）
- **DFS Postorder** - 后序遍历

### 🛤️ 最短路径算法
| 算法 | 时间复杂度 | 特点 |
|------|-----------|------|
| Dijkstra | O((V+E) log V) | 非负权边，单源 |
| Bellman-Ford | O(V·E) | 支持负权边，可检测负环 |
| Floyd-Warshall | O(V³) | 全源最短路径 |
| BFS Path | O(V+E) | 无权图最短路径 |

### 🌳 最小生成树
- **Prim** - 适用于连通图
- **Kruskal** - 支持最小生成森林

### 📋 拓扑排序
- **Kahn 算法** - BFS 实现
- **DFS 实现** - 递归检测环

### 🔗 连通性算法
- **连通分量** - 无向图
- **强连通分量** - Kosaraju 算法（有向图）
- **连通检测**

### 🔄 环检测
- 有向图/无向图环检测
- 环路径查找

### 🎯 其他算法
- **二分图检测** - BFS染色算法
- **欧拉图检测** - 欧拉回路/路径
- **割点检测** - 关节点查找
- **桥检测** - 割边查找
- **中心性计算** - 度中心性、介数中心性
- **聚类系数** - 局部/全局聚类系数

## 🚀 快速开始

### 创建图

```python
from mod import Graph

# 创建无向图
g = Graph[str]()
g.add_edge("A", "B", weight=5)
g.add_edge("B", "C", weight=3)
g.add_edge("A", "C", weight=10)

# 创建有向图
dg = Graph[int](directed=True)
dg.add_edge(1, 2)
dg.add_edge(2, 3)
dg.add_edge(1, 3)
```

### 遍历

```python
from mod import bfs, dfs

# BFS遍历
bfs_result = bfs(g, "A")  # ["A", "B", "C"]

# DFS遍历
dfs_result = dfs(g, "A")  # ["A", "B", "C"]
```

### 最短路径

```python
from mod import dijkstra, get_path

# Dijkstra最短路径
result = dijkstra(g, "A")
print(result["C"])  # (最短距离, 前驱节点)

# 获取具体路径
path = get_path({n: (d, p) for n, (d, p) in result.items()}, "A", "C")
# ["A", "B", "C"]
```

### 最小生成树

```python
from mod import prim, kruskal

# Prim算法
mst = prim(g)
for u, v, weight in mst:
    print(f"{u} -> {v}: {weight}")

# Kruskal算法
mst2 = kruskal(g)
```

### 拓扑排序

```python
from mod import topological_sort

dag = Graph[str](directed=True)
dag.add_edge("A", "B")
dag.add_edge("B", "C")
dag.add_edge("A", "C")

order = topological_sort(dag)
# ["A", "B", "C"]
```

### 环检测

```python
from mod import has_cycle, find_cycle

g_cycle = Graph[int]()
g_cycle.add_edge(1, 2)
g_cycle.add_edge(2, 3)
g_cycle.add_edge(3, 1)

has_cycle(g_cycle)  # True
find_cycle(g_cycle)  # [1, 2, 3, 1]
```

### 连通分量

```python
from mod import connected_components, strongly_connected_components

# 无向图连通分量
components = connected_components(g)

# 有向图强连通分量
dg = Graph[int](directed=True)
sccs = strongly_connected_components(dg)
```

### 中心性计算

```python
from mod import degree_centrality, betweenness_centrality, clustering_coefficient

# 度中心性
dc = degree_centrality(g)

# 介数中心性
bc = betweenness_centrality(g)

# 聚类系数
cc = clustering_coefficient(g)
avg_cc = average_clustering_coefficient(g)
```

## 📚 API 参考

### Graph 类

| 方法 | 描述 |
|------|------|
| `add_node(node)` | 添加节点 |
| `add_edge(u, v, weight=1)` | 添加边 |
| `remove_node(node)` | 移除节点 |
| `remove_edge(u, v)` | 移除边 |
| `neighbors(node)` | 获取邻居列表 |
| `get_nodes()` | 获取所有节点 |
| `get_edges()` | 获取所有边 |
| `has_node(node)` | 检查节点存在 |
| `has_edge(u, v)` | 检查边存在 |
| `degree(node)` | 获取节点度 |
| `node_count()` | 节点数 |
| `edge_count()` | 边数 |
| `copy()` | 深拷贝 |
| `to_adjacency_matrix()` | 转邻接矩阵 |

### 遍历函数

| 函数 | 参数 | 返回 |
|------|------|------|
| `bfs(g, start)` | 图, 起点 | 遍历序列 |
| `dfs(g, start, recursive=True)` | 图, 起点 | 遍历序列 |
| `dfs_postorder(g, start)` | 图, 起点 | 后序序列 |

### 最短路径函数

| 函数 | 参数 | 返回 |
|------|------|------|
| `dijkstra(g, start, end=None)` | 图, 起点, 终点 | {节点: (距离, 前驱)} |
| `bellman_ford(g, start)` | 图, 起点 | (结果, 是否有负环) |
| `floyd_warshall(g)` | 图 | (距离矩阵, 前驱矩阵) |
| `get_path(predecessors, start, end)` | 前驱字典 | 路径列表 |
| `shortest_path_bfs(g, start, end)` | 图, 起点, 终点 | 路径或 None |
| `all_paths(g, start, end, max_paths=1000)` | 图, 起点, 终点 | 所有路径列表 |

### MST 函数

| 函数 | 参数 | 返回 |
|------|------|------|
| `prim(g, start=None)` | 无向图 | MST边列表 |
| `kruskal(g)` | 无向图 | MST边列表 |

### 拓扑排序函数

| 函数 | 参数 | 返回 |
|------|------|------|
| `topological_sort(g)` | 有向图 | 拓扑序列或 None |
| `topological_sort_dfs(g)` | 有向图 | 拓扑序列或 None |

### 连通性函数

| 函数 | 参数 | 返回 |
|------|------|------|
| `connected_components(g)` | 无向图 | 连通分量列表 |
| `is_connected(g)` | 无向图 | 是否连通 |
| `strongly_connected_components(g)` | 有向图 | 强连通分量列表 |

### 环检测函数

| 函数 | 参数 | 返回 |
|------|------|------|
| `has_cycle(g)` | 图 | 是否有环 |
| `find_cycle(g)` | 图 | 环路径或 None |

### 其他函数

| 函数 | 参数 | 返回 |
|------|------|------|
| `is_bipartite(g)` | 无向图 | (是否二分图, 分区) |
| `is_eulerian(g)` | 无向图 | 是否欧拉图 |
| `is_semi_eulerian(g)` | 无向图 | 是否半欧拉图 |
| `articulation_points(g)` | 无向图 | 割点集合 |
| `bridges(g)` | 无向图 | 桥列表 |
| `degree_sequence(g)` | 图 | 度序列 |
| `degree_centrality(g)` | 图 | {节点: 中心性} |
| `betweenness_centrality(g)` | 图 | {节点: 中心性} |
| `clustering_coefficient(g, node=None)` | 无向图 | 聚类系数 |
| `average_clustering_coefficient(g)` | 无向图 | 平均聚类系数 |

## 🧪 测试

运行测试：

```bash
python graph_utils_test.py
```

测试覆盖：
- 图基本操作（25+ 测试）
- 遍历算法（15+ 测试）
- 最短路径（20+ 测试）
- MST（10+ 测试）
- 拓扑排序（10+ 测试）
- 连通性（10+ 测试）
- 环检测（10+ 测试）
- 二分图（5+ 测试）
- 特殊算法（10+ 测试）
- 中心性（5+ 测试）
- 聚类系数（5+ 测试）
- 边界情况（15+ 测试）

总计：**150+ 测试用例**

## ⚙️ 时间复杂度

| 算法 | 复杂度 |
|------|--------|
| BFS/DFS | O(V + E) |
| Dijkstra | O((V + E) log V) |
| Bellman-Ford | O(V · E) |
| Floyd-Warshall | O(V³) |
| Prim | O((V + E) log V) |
| Kruskal | O(E log E) |
| 拓扑排序 | O(V + E) |
| 连通分量 | O(V + E) |
| 强连通分量 | O(V + E) |
| 环检测 | O(V + E) |
| 割点/桥 | O(V + E) |
| 介数中心性 | O(V · (V + E)) |

## 📝 设计说明

1. **泛型设计**：支持任意可哈希类型作为节点（字符串、整数、元组等）
2. **零依赖**：仅使用 Python 标准库（collections, heapq）
3. **类型提示**：完整的类型标注，IDE友好
4. **错误处理**：参数验证、异常抛出
5. **算法正确性**：经典算法实现，经过充分测试

## 📄 许可证

MIT License

---

**创建日期**: 2026-04-21  
**版本**: 1.0.0  
**作者**: AllToolkit