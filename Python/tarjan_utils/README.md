# Tarjan Utils

一个完整的 Tarjan 算法工具库，用于在有向图中查找强连通分量（SCC）。零外部依赖，仅使用 Python 标准库。

## 功能特性

### 核心算法
- `tarjan(graph)` - 查找所有强连通分量
- `tarjan_with_info(graph)` - 返回完整的 SCC 信息（包含 TarjanResult 对象）

### 强连通性检查
- `is_strongly_connected(graph)` - 检查图是否强连通
- `count_scc(graph)` - 计算强连通分量数量

### SCC 分析
- `largest_scc(graph)` - 获取最大的 SCC
- `smallest_scc(graph)` - 获取最小的 SCC
- `scc_sizes(graph)` - 获取所有 SCC 大小
- `scc_distribution(graph)` - 获取 SCC 大小分布

### 环检测
- `has_cycle(graph)` - 检查图中是否有环
- `find_cycles(graph)` - 查找所有环
- `is_in_cycle(graph, node)` - 检查节点是否在环中

### 节点操作
- `get_scc_for_node(graph, node)` - 获取包含指定节点的 SCC
- `sort_nodes_by_scc(graph)` - 按 SCC 顺序排序节点

### 图操作
- `condensation_graph(graph)` - 构建缩点图（DAG）
- `build_scc_adjacency(graph)` - 构建 SCC 内部邻接表

### 图构建器
- `from_edge_list(edges)` - 从边列表构建图
- `from_adjacency_matrix(matrix)` - 从邻接矩阵构建图

## 使用示例

### 基本使用

```python
from tarjan_utils import tarjan, has_cycle

# 定义有向图
graph = {
    0: [1],
    1: [2],
    2: [0, 3],  # SCC: {0, 1, 2}
    3: [4],
    4: [3]      # SCC: {3, 4}
}

# 查找所有 SCC
sccs = tarjan(graph)
# [[0, 1, 2], [3, 4]]

# 检查是否有环
has_cycle(graph)  # True
```

### 检查强连通性

```python
from tarjan_utils import is_strongly_connected

# 强连通图（每个节点都能到达任何其他节点）
strong_graph = {
    0: [1],
    1: [2],
    2: [0]
}
is_strongly_connected(strong_graph)  # True

# 非强连通图
weak_graph = {
    0: [1],
    1: [2],
    2: []  # 不能回到起点
}
is_strongly_connected(weak_graph)  # False
```

### 查找环

```python
from tarjan_utils import find_cycles, is_in_cycle

graph = {
    0: [1], 1: [0],  # Cycle: {0, 1}
    2: []            # No cycle
}

# 查找所有环
cycles = find_cycles(graph)
# [[0, 1]]

# 检查节点是否在环中
is_in_cycle(graph, 0)  # True
is_in_cycle(graph, 2)  # False
```

### 构建缩点图

```python
from tarjan_utils import condensation_graph

graph = {
    0: [1], 1: [2], 2: [0, 3],  # SCC 0
    3: [4], 4: [3]              # SCC 1
}

# 缩点图（将 SCC 合并为单个节点）
condensed = condensation_graph(graph)
# {0: [1]}  # SCC 0 -> SCC 1
```

### 从边列表构建图

```python
from tarjan_utils import from_edge_list, tarjan

edges = [(0, 1), (1, 2), (2, 0), (2, 3)]
graph = from_edge_list(edges)
# {0: [1], 1: [2], 2: [0, 3], 3: []}

sccs = tarjan(graph)
# [[0, 1, 2], [3]]
```

## TarjanResult 对象

```python
from tarjan_utils import tarjan_with_info

result = tarjan_with_info(graph)
# result.sccs         - 所有 SCC
# result.scc_count    - SCC 数量
# result.node_to_scc  - 节点到 SCC 编号的映射
# result.is_dag       - 是否是无环图（DAG）
```

## 应用场景

1. **社交网络分析**: 找到紧密连接的群体
2. **编译器优化**: 检测循环依赖
3. **死锁检测**: 查找资源循环等待
4. **生物网络分析**: 分析基因调控网络
5. **依赖分析**: 检测软件包依赖循环
6. **图算法**: 作为其他图算法的基础

## 时间复杂度

Tarjan 算法的时间复杂度为 O(V + E)，其中 V 是节点数，E 是边数。

## 测试

```bash
cd Python/tarjan_utils
python test_tarjan_utils.py
```

## API 文档

```python
# 核心函数
tarjan(graph: Dict[Any, List[Any]]) -> List[List[Any]]
tarjan_with_info(graph: Dict[Any, List[Any]]) -> TarjanResult

# 强连通性
is_strongly_connected(graph: Dict[Any, List[Any]]) -> bool
count_scc(graph: Dict[Any, List[Any]]) -> int

# SCC 分析
largest_scc(graph: Dict[Any, List[Any]]) -> List[Any]
smallest_scc(graph: Dict[Any, List[Any]]) -> List[Any]
scc_sizes(graph: Dict[Any, List[Any]]) -> List[int]
scc_distribution(graph: Dict[Any, List[Any]]) -> Dict[int, int]

# 环检测
has_cycle(graph: Dict[Any, List[Any]]) -> bool
find_cycles(graph: Dict[Any, List[Any]]) -> List[List[Any]]
is_in_cycle(graph: Dict[Any, List[Any]], node: Any) -> bool

# 节点操作
get_scc_for_node(graph: Dict[Any, List[Any]], node: Any) -> List[Any]
sort_nodes_by_scc(graph: Dict[Any, List[Any]]) -> List[Any]

# 图操作
condensation_graph(graph: Dict[Any, List[Any]]) -> Dict[int, List[int]]
build_scc_adjacency(graph: Dict[Any, List[Any]])

# 图构建
from_edge_list(edges: List[Tuple[Any, Any]]) -> Dict[Any, List[Any]]
from_adjacency_matrix(matrix: List[List[int]]) -> Dict[int, List[int]]
```

## 许可证

MIT License

## 版本历史

- v1.0.0 (2026-05-12) - 初始版本，包含完整 Tarjan 算法实现