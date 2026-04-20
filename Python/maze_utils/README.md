# Maze Utils - 迷宫生成与求解工具

一个完整的 Python 迷宫工具库，提供多种迷宫生成算法和求解算法，零外部依赖。

## 功能特性

### 迷宫生成算法
- **DFS（深度优先搜索）** - 生成长廊，路径曲折
- **Prim算法** - 均匀分布，分支多
- **Kruskal算法** - 无偏差的均匀迷宫
- **递归分割** - 先建房间再分割，长直走廊
- **Eller算法** - 逐行生成，内存高效
- **二叉树** - 最简单的算法，有对角偏差

### 迷宫求解算法
- **BFS（广度优先）** - 保证最短路径
- **DFS（深度优先）** - 快速找到任意路径
- **A*算法** - 启发式最短路径
- **墙跟随** - 简单有效，适合完美迷宫
- **死胡同填充** - 系统性消除死路

### 可视化
- ASCII渲染
- Unicode渲染（多种样式）
- 路径标记显示

### 序列化
- JSON格式
- 二进制格式（紧凑）
- CSV格式（数据分析）

## 快速开始

```python
from maze_utils import generate_dfs, solve_bfs, render_ascii

# 生成迷宫
maze = generate_dfs(15, 10, seed=42)

# 求解迷宫
path = solve_bfs(maze)

# 可视化
print(render_ascii(maze, path))
```

## 使用示例

### 不同生成算法

```python
from maze_utils import generate_prim, generate_kruskal, generate_ellers

# Prim算法生成
maze_prim = generate_prim(20, 20, seed=42)

# Kruskal算法生成
maze_kruskal = generate_kruskal(20, 20, seed=42)

# Eller算法生成（适合大迷宫）
maze_eller = generate_ellers(100, 100)
```

### 不同求解方法

```python
from maze_utils import solve_bfs, solve_astar, solve_wall_follower

# BFS求最短路径
shortest_path = solve_bfs(maze)

# A*启发式求解（同样最短）
astar_path = solve_astar(maze)

# 墙跟随算法
wall_path = solve_wall_follower(maze, hand='right')
```

### Unicode可视化

```python
from maze_utils import render_unicode

# 不同样式
print(render_unicode(maze, style='box'))    # 标准样式
print(render_unicode(maze, style='round'))  # 圆角样式
print(render_unicode(maze, style='double')) # 双线样式
```

### 序列化保存

```python
from maze_utils import to_json, from_json, to_binary, from_binary

# JSON格式（易读）
json_str = to_json(maze)
restored = from_json(json_str)

# 二进制格式（紧凑）
binary_data = to_binary(maze)
restored = from_binary(binary_data)
```

### 自定义起点终点

```python
maze = generate_dfs(10, 10, seed=42)
maze.start = (0, 5)
maze.end = (9, 5)
path = solve_bfs(maze)
```

## API 参考

### 生成器函数

| 函数 | 参数 | 返回 |
|------|------|------|
| `generate_dfs(width, height, seed)` | 尺寸和随机种子 | Maze |
| `generate_prim(width, height, seed)` | 尺寸和随机种子 | Maze |
| `generate_kruskal(width, height, seed)` | 尺寸和随机种子 | Maze |
| `generate_recursive_division(width, height, seed)` | 尺寸和随机种子 | Maze |
| `generate_ellers(width, height, seed)` | 尺寸和随机种子 | Maze |
| `generate_binary_tree(width, height, seed, bias)` | 尺寸、种子、偏差方向 | Maze |

### 求解器函数

| 函数 | 参数 | 返回 |
|------|------|------|
| `solve_bfs(maze, start, end)` | 迷宫、起点、终点 | Path or None |
| `solve_dfs(maze, start, end)` | 迷宫、起点、终点 | Path or None |
| `solve_astar(maze, start, end, heuristic)` | 迷宫、起点、终点、启发函数 | Path or None |
| `solve_wall_follower(maze, start, end, hand)` | 迷宫、起点、终点、左右手 | Path or None |
| `solve_dead_end_filling(maze, start, end)` | 迷宫、起点、终点 | Path or None |

### Maze 类方法

| 方法 | 描述 |
|------|------|
| `get_cell(x, y)` | 获取单元格 |
| `remove_wall(x1, y1, x2, y2)` | 移除相邻单元格间的墙 |
| `add_wall(x1, y1, x2, y2)` | 添加墙 |
| `get_passages(x, y)` | 获取可通行的邻居 |
| `is_perfect()` | 检查是否为完美迷宫 |
| `copy()` | 深拷贝迷宫 |

## 性能测试

在 50x50 迷宫上的测试结果：
- DFS生成：< 0.1秒
- BFS求解：< 0.05秒
- A*求解：< 0.05秒

## 许可证

MIT License

## 作者

AllToolkit 自动化生成
日期：2026-04-20