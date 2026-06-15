# Graph Metrics Utils 📊

图论中心性指标计算工具，提供度中心性、介数中心性、接近中心性等。

## 特性

- ✅ **度中心性** - 节点度数指标
- ✅ **介数中心性** - 最短路径经过次数
- ✅ **接近中心性** - 到其他节点距离
- ✅ **特征向量中心性** - PageRank 类似
- ✅ **零依赖** - 仅使用 Python 标准库

## 快速开始

```python
from graph_metrics_utils import degree_centrality, betweenness_centrality, closeness_centrality

graph = {
    "A": ["B", "C"],
    "B": ["A", "C"],
    "C": ["A", "B", "D"],
    "D": ["C"]
}

dc = degree_centrality(graph, "C")
print(dc)  # 3.0

bc = betweenness_centrality(graph, "C")
print(bc)  # 0.67
```

## API 参考

| 函数 | 说明 |
|------|------|
| `degree_centrality(graph, node)` | 度中心性 |
| `betweenness_centrality(graph, node)` | 介数中心性 |
| `closeness_centrality(graph, node)` | 接近中心性 |
| `eigenvector_centrality(graph)` | 特征向量中心性 |
