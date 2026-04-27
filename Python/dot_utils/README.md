# Dot Utils


AllToolkit - Graphviz DOT Utilities Module
===========================================
A comprehensive Graphviz DOT format generation utility module for Python with zero external dependencies.

Features:
    - DOT language generation for graph visualization
    - Directed graphs (digraph) and undirected graphs (graph)
    - Subgraph and cluster support
    - Node and edge attributes (color, shape, style, label)
    - HTML label support
    - Record-based nodes (tables)
    - Graph ranking and layout hints
    - State machine diagram generation
    - Tree visualization helpers
    - DOT parsing and manipulation

Author: AllToolkit Contributors
License: MIT


## 功能

### 类

- **GraphType**: Graph type enumeration
- **NodeShape**: Common node shapes for Graphviz
- **ArrowType**: Arrow types for edge heads and tails
- **Color**: Common color constants for Graphviz
  方法: rgb, rgba
- **RankDir**: Rank direction for graph layout
- **Style**: Common style values for nodes and edges
- **DotAttribute**: Container for DOT attribute with optional HTML escaping
  方法: to_dot
- **Node**: DOT node representation
  方法: set, label, shape, color, fillcolor ... (14 个方法)
- **Edge**: DOT edge representation
  方法: set, label, color, style, penwidth ... (12 个方法)
- **Subgraph**: DOT subgraph representation
  方法: set, label, style, color, bgcolor ... (11 个方法)
- **Graph**: DOT graph representation (main graph or digraph)
  方法: add_edge, rankdir, ranksep, nodesep, size ... (13 个方法)

### 函数

- **create_digraph(name**) - Create a directed graph.
- **create_graph(name**) - Create an undirected graph.
- **html_table(rows, border, cellborder**, ...) - Create an HTML table label for nodes.
- **record_label(fields, vertical**) - Create a record-based label for nodes.
- **create_state_machine(states, transitions, initial**, ...) - Create a state machine diagram.
- **create_tree(nodes, node_labels, name**) - Create a tree diagram.
- **create_flowchart(steps, name**) - Create a flowchart.
- **create_cluster_diagram(clusters, edges, name**) - Create a diagram with clustered nodes.
- **quick_graph(nodes, edges, directed**, ...) - Quickly create a simple graph.
- **parse_dot(dot_string**) - Parse a simple DOT string into a dictionary representation.

... 共 66 个函数

## 使用示例

```python
from mod import create_digraph

# 使用 create_digraph
result = create_digraph()
```

## 测试

运行测试：

```bash
python *_test.py
```

## 文件结构

```
{module_name}/
├── mod.py              # 主模块
├── *_test.py           # 测试文件
├── README.md           # 本文档
└── examples/           # 示例代码
    └── usage_examples.py
```

---

**Last updated**: 2026-04-28
