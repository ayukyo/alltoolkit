# A* Pathfinding Utils

A* 寻路算法工具包，提供完整的路径规划功能。

## 功能特性

- **通用 A* 算法**: 支持任意类型的节点，自定义邻居函数和启发函数
- **2D 网格寻路**: 专门为网格地图优化，支持四方向和八方向移动
- **双向 A* 搜索**: 从起点和终点同时搜索，提高效率
- **路径平滑**: 移除不必要的中间节点，优化路径
- **可达区域查询**: 查找给定代价范围内的所有可达位置
- **可视化工具**: 将路径可视化为 ASCII 图形
- **零外部依赖**: 仅使用 Python 标准库

## 快速开始

### 基础使用

```python
from astar_utils import GridAStar

# 创建网格地图 (0=可通行, 1=障碍物)
grid = [
    [0, 0, 0, 0, 0],
    [0, 1, 1, 1, 0],
    [0, 0, 0, 1, 0],
    [0, 1, 0, 0, 0],
    [0, 0, 0, 0, 0]
]

# 创建寻路器
finder = GridAStar(grid)

# 查找路径
path = finder.find_path((0, 0), (4, 4))
print(path)  # [(0, 0), (0, 1), ...]
```

### 对角线移动

```python
finder = GridAStar(grid, diagonal=True)
path = finder.find_path((0, 0), (4, 4))
```

### 通用图寻路

```python
from astar_utils import AStar

# 定义图结构
graph = {
    'A': [('B', 1), ('C', 4)],
    'B': [('C', 2), ('D', 5)],
    'C': [('D', 1)],
    'D': []
}

# 创建寻路器
astar = AStar(
    neighbors_fn=lambda n: graph.get(n, []),
    heuristic_fn=lambda a, b: 0
)

# 查找路径
path, cost = astar.find_path('A', 'D')
```

## 启发函数

GridAStar 支持多种启发函数：

- `manhattan`: 曼哈顿距离（适合四方向移动）
- `euclidean`: 欧几里得距离
- `chebyshev`: 切比雪夫距离
- `octile`: 八方向距离（适合八方向移动）

```python
path = finder.find_path(start, goal, heuristic='octile')
```

## 可视化

```python
from astar_utils import visualize_path

visual = visualize_path(grid, path)
print(visual)
# S..#.
# .*#..
# .#*..
# ...*G
```

## API 参考

### GridAStar

```python
GridAStar(grid, diagonal=False, diagonal_cost=1.414, obstacle_values={1})
```

**方法:**
- `find_path(start, goal, heuristic='manhattan')` - 查找路径
- `find_path_with_cost(start, goal, heuristic)` - 查找路径并返回代价
- `find_all_reachable(start, max_cost)` - 查找所有可达位置
- `smooth_path(path)` - 平滑路径
- `is_valid(pos)` - 检查位置是否有效

### AStar

```python
AStar(neighbors_fn, heuristic_fn, is_goal_fn=None)
```

**方法:**
- `find_path(start, goal, max_iterations=100000)` - 查找路径
- `find_all_reachable(start, max_cost)` - 查找所有可达节点

### BidirectionalAStar

双向 A* 算法，从起点和终点同时搜索。

### 便捷函数

```python
astar_path(start, goal, neighbors_fn, heuristic_fn)  # 通用寻路
grid_path(grid, start, goal, diagonal=False)  # 网格寻路
create_grid_from_string(map_string)  # 从字符串创建网格
```

## 应用场景

- 游戏开发中的 NPC 寻路
- 机器人路径规划
- 迷宫求解
- 地图导航
- 网络路由优化

## 文件结构

```
astar_utils/
├── mod.py              # 主模块
├── astar_utils_test.py # 单元测试
├── README.md           # 说明文档
└── examples/
    └── usage_examples.py  # 使用示例
```

## 测试

```bash
python -m pytest astar_utils_test.py -v
```

## 许可证

MIT License