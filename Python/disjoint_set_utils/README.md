# Disjoint Set (Union-Find) Utilities - 并查集工具

[![Python 3.7+](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/downloads/)
[![MIT License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

零依赖、生产就绪的并查集（Disjoint Set / Union-Find）数据结构模块。

## 功能特性

- **路径压缩**：查找时自动压缩路径，优化后续查询
- **按秩合并**：合并时选择较小的树作为子树
- **泛型支持**：支持任意可哈希类型作为元素
- **分量计数**：追踪连通分量数量
- **分量大小**：追踪每个分量的大小
- **批量操作**：支持批量添加和合并
- **Kruskal MST**：最小生成树算法辅助工具
- **网络分析**：连通性分析工具

## 时间复杂度

所有操作的均摊时间复杂度接近 O(1)：
- **Find**: O(α(n)) ≈ O(1)
- **Union**: O(α(n)) ≈ O(1)
- **Connected**: O(α(n)) ≈ O(1)

其中 α 是反阿克曼函数，对于所有实际输入都小于 5。

## 安装

```bash
# 直接使用
from disjoint_set_utils import DisjointSet

# 或安装为包
pip install alltoolkit-disjoint-set-utils
```

## 快速开始

### 基本操作

```python
from disjoint_set_utils import DisjointSet

# 创建并查集
ds = DisjointSet[str]()

# 添加元素（每个元素初始为独立集合）
ds.make_set("A")
ds.make_set("B")
ds.make_set("C")

# 合并集合
ds.union("A", "B")  # A 和 B 现在在同一集合

# 检查连通性
print(ds.connected("A", "B"))  # True
print(ds.connected("A", "C"))  # False

# 查找代表元素
print(ds.find("A"))  # 'A' 或 'B'（代表元素）
```

### 批量操作

```python
from disjoint_set_utils import DisjointSet

ds = DisjointSet[int]()

# 批量添加元素
ds.make_set_batch([1, 2, 3, 4, 5])

# 批量合并
ds.union_batch([(1, 2), (3, 4), (4, 5)])
# 现在: {1, 2}, {3, 4, 5}
```

### 分量信息

```python
from disjoint_set_utils import DisjointSet

ds = DisjointSet[str]()
for elem in ["A", "B", "C", "D"]:
    ds.make_set(elem)

ds.union("A", "B")
ds.union("C", "D")

# 获取分量数量
print(ds.count_components())  # 2

# 获取分量大小
print(ds.size("A"))  # 2（{A, B} 的大小）

# 获取所有分量
print(ds.get_components())  # [{'A', 'B'}, {'C', 'D'}]
```

### 网络连通性分析

```python
from disjoint_set_utils import is_connected_graph, find_connected_groups

# 检查图是否完全连通
edges = [("A", "B"), ("B", "C"), ("C", "D")]
print(is_connected_graph(edges))  # True（A-B-C-D 连通）

# 找出连通分组
edges = [("A", "B"), ("C", "D")]
groups = find_connected_groups(edges, nodes=["A", "B", "C", "D"])
print(groups)  # [{'A', 'B'}, {'C', 'D'}]
```

### Kruskal 最小生成树

```python
from disjoint_set_utils import kruskal_mst

# 边列表：(u, v, weight)
edges = [
    ("A", "B", 1),
    ("B", "C", 2),
    ("A", "C", 3),
    ("C", "D", 1),
]

mst_edges, total_weight = kruskal_mst(edges)
print(f"MST 边: {mst_edges}")
print(f"总权重: {total_weight}")
```

## API 参考

### DisjointSet

```python
DisjointSet[T]()  # 泛型，T 必须是可哈希类型
```

**核心操作**:
- `make_set(element)` - 创建单元素集合
- `make_set_batch(elements)` - 批量创建
- `find(element)` - 查找代表元素
- `union(a, b)` - 合并两个集合
- `union_batch(pairs)` - 批量合并
- `connected(a, b)` - 检查是否连通

**查询操作**:
- `count_components()` - 分量数量
- `size(element)` - 元素所在分量大小
- `get_components()` - 获取所有分量
- `get_component(element)` - 获取元素所在分量
- `__contains__(element)` - 检查元素是否存在
- `__len__()` - 元素总数

### 辅助函数

```python
# Kruskal 最小生成树
kruskal_mst(edges: List[Tuple]) -> Tuple[List, float]

# 检查图是否完全连通
is_connected_graph(edges: List[Tuple]) -> bool

# 找出连通分组
find_connected_groups(edges: List[Tuple], nodes: List) -> List[Set]
```

## 使用场景

| 场景 | 说明 |
|------|------|
| 社交网络 | 查找好友圈子、判断两人是否连通 |
| 图像处理 | 连通区域标记 |
| 网络拓扑 | 判断网络连通性 |
| 最小生成树 | Kruskal 算法核心 |
| 动态连通性 | 实时判断元素连通关系 |
| 聚类分析 | 基于距离的层次聚类 |

## 测试

```bash
python disjoint_set_utils_test.py
```

## 许可证

MIT License