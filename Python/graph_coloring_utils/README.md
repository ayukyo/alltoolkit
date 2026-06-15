# Graph Coloring Utils 🎨

图着色算法工具模块，解决图着色、调度优化等问题。

## 特性

- ✅ **多种算法** - 贪心、Welsh-Powell、DSatur、回溯
- ✅ **最优着色** - 回溯搜索最小着色数
- ✅ **色数边界** - 上下界估计
- ✅ **算法对比** - 比较不同算法效果
- ✅ **区间图检测** - 特殊图类支持
- ✅ **零依赖** - 仅使用 Python 标准库

## 快速开始

### 基本着色

```python
from graph_coloring_utils import Graph, greedy_coloring

# 创建图
g = Graph()
g.add_edge("A", "B")
g.add_edge("A", "C")
g.add_edge("B", "C")
g.add_edge("C", "D")

# 贪心着色
coloring = greedy_coloring(g)
print(coloring)  # {'A': 0, 'B': 1, 'C': 2, 'D': 0}
```

### 使用不同算法

```python
from graph_coloring_utils import welsh_powell_coloring, dsatur_coloring, backtracking_coloring

# Welsh-Powell
coloring = welsh_powell_coloring(g)

# DSatur（度数饱和度）
coloring = dsatur_coloring(g)

# 回溯搜索（最小着色数）
coloring = backtracking_coloring(g, max_colors=3)
```

### 验证与分组

```python
from graph_coloring_utils import is_valid_coloring, get_color_groups, count_colors

# 验证着色
is_valid = is_valid_coloring(g, coloring)
print(is_valid)  # True

# 按颜色分组
groups = get_color_groups(coloring)
print(groups)  # {0: ['A', 'D'], 1: ['B'], 2: ['C']}

# 颜色数量
num_colors = count_colors(coloring)
print(num_colors)  # 3
```

### 色数边界

```python
from graph_coloring_utils import chromatic_number_bounds

lower, upper = chromatic_number_bounds(g)
print(f"色数范围: [{lower}, {upper}]")
```

## API 参考

### 图类

| 类 | 说明 |
|---|------|
| `Graph` | 通用图结构 |
| `IntervalGraph` | 区间图（一定是二分图）|
| `BipartiteChecker` | 二分图检测器 |

### 核心函数

| 函数 | 说明 |
|------|------|
| `greedy_coloring(graph)` | 贪心着色 |
| `welsh_powell_coloring(graph)` | Welsh-Powell 算法 |
| `dsatur_coloring(graph)` | DSatur 算法 |
| `backtracking_coloring(graph, max_colors)` | 回溯最优着色 |
| `is_valid_coloring(graph, coloring)` | 验证着色有效性 |
| `chromatic_number_bounds(graph)` | 色数上下界 |
