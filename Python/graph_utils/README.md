# Graph Utils - 图算法工具

完整的图数据结构和算法实现，零外部依赖。

## 功能

### 图表示
- 邻接表表示
- 邻接矩阵表示
- 有向图 / 无向图支持

### 图遍历
- **BFS** - 广度优先搜索
- **DFS** - 深度优先搜索（递归 / 迭代版本）

### 最短路径
- **Dijkstra** - 单源最短路径（无负权边）
- **Bellman-Ford** - 单源最短路径（支持负权边 + 负环检测）
- **Floyd-Warshall** - 全源最短路径

### 最小生成树
- **Kruskal** - 基于边排序的 MST
- **Prim** - 基于顶点的 MST

### 拓扑排序
- **Kahn 算法** - 基于入度
- **DFS 算法** - 基于深度遍历

### 连通性
- **连通分量** - 无向图
- **强连通分量** - Kosaraju 算法

### 环检测
- 环存在检测
- 环路径查找

### 特殊图检测
- **二分图检测** - 并获取分组
- **欧拉路径/回路** - Hierholzer 算法
- **树检测**

### 图分析
- **割点（关节点）** - Tarjan 算法
- **桥（割边）** - Tarjan 算法
- **图统计信息**

## 快速使用

```python
from graph_utils import create_graph, shortest_path, bfs, dfs

# 创建图
graph = create_graph([
    ('A', 'B', 1),
    ('B', 'C', 2),
    ('A', 'C', 4),
])

# 最短路径
path = shortest_path(graph, 'A', 'C')
print(path.path)       # ['A', 'B', 'C']
print(path.distance)   # 3

# 图遍历
print(bfs(graph, 'A'))  # ['A', 'B', 'C']
print(dfs(graph, 'A'))  # ['A', 'B', 'C']
```

## 详细用法

### 创建图

```python
from graph_utils import Graph, GraphType

# 无向图
graph = Graph()

# 有向图
graph = Graph(GraphType.DIRECTED)

# 添加顶点
graph.add_vertex('A')

# 添加边
graph.add_edge('A', 'B', 5)  # 权重为 5

# 从边列表创建
edges = [('A', 'B', 1), ('B', 'C', 2)]
graph = Graph.from_edges(edges, GraphType.DIRECTED)

# 从邻接表创建
adj = {'A': [('B', 1), ('C', 2)], 'B': [('C', 3)]}
graph = Graph.from_adjacency_list(adj, GraphType.DIRECTED)
```

### 最短路径

```python
# Dijkstra（单点到单点）
result = dijkstra(graph, 'A', 'C')

# Dijkstra（单点到所有点）
all_paths = dijkstra(graph, 'A')

# Bellman-Ford（支持负权边）
distances, previous, has_negative_cycle = bellman_ford(graph, 'A')

# Floyd-Warshall（所有点对）
dist_matrix, prev_matrix = floyd_warshall(graph)
```

### 最小生成树

```python
# Kruskal
mst = kruskal(graph)
print(mst.total_weight)  # 总权重
print(mst.edges)         # MST 边

# Prim（可指定起点）
mst = prim(graph, 'A')
```

### 拓扑排序

```python
# Kahn 算法
order = topological_sort(graph)

# DFS 算法
order = topological_sort_dfs(graph)

# 注意：有环图返回 None
```

### 连通分量

```python
# 无向图连通分量
result = connected_components(graph)
print(result.count)          # 分量数
print(result.is_connected)   # 是否连通

# 有向图强连通分量
result = strongly_connected_components(graph)
```

### 环检测

```python
# 检测是否存在环
has_cycle(graph)  # True/False

# 查找环路径
cycle = find_cycle(graph)  # 返回环路径或 None
```

### 二分图

```python
is_bip, coloring = is_bipartite(graph)
# coloring 是分组结果：{vertex: 0/1}
```

### 欧拉路径

```python
# 检测
has_eulerian_path(graph)      # 存在欧拉路径
has_eulerian_circuit(graph)   # 存在欧拉回路

# 查找路径
path = find_eulerian_path(graph)
```

### 图工具

```python
# 图统计
stats = graph_statistics(graph)

# 割点和桥
aps = get_articulation_points(graph)
bridges = get_bridges(graph)

# 孤立顶点
isolated = get_isolated_vertices(graph)

# 反转图
reversed = reverse_graph(graph)

# 是否为树
is_tree(graph)
```

## 测试

运行测试：

```bash
python graph_utils_test.py
```

## 依赖

零外部依赖，纯 Python 标准库实现。