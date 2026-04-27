# Maze Utils - 迷宫生成与求解工具 (Go 版本)

一个完整的 Go 迷宫工具库，提供多种迷宫生成算法和求解算法，零外部依赖。

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
- Unicode渲染（多种样式：Box/Round/Double/Block）
- 路径标记显示

### 序列化
- JSON格式
- 二进制格式（紧凑）
- CSV格式（数据分析）

## 快速开始

```go
package main

import (
    "fmt"
    maze "github.com/ayukyo/alltoolkit/Go/maze_utils"
)

func main() {
    // 生成迷宫
    m := maze.GenerateDFS(15, 10, 42)

    // 求解迷宫
    path := maze.SolveBFS(m, m.Start, m.End)

    // 可视化
    fmt.Println(maze.RenderUnicode(m, maze.StyleBox))
    fmt.Println(maze.RenderPath(m, path, maze.StyleBox))
}
```

## 使用示例

### 不同生成算法

```go
// DFS算法生成
mDFS := maze.GenerateDFS(20, 20, 42)

// Prim算法生成
mPrim := maze.GeneratePrim(20, 20, 42)

// Kruskal算法生成
mKruskal := maze.GenerateKruskal(20, 20, 42)

// Eller算法生成（适合大迷宫）
mEller := maze.GenerateEllers(100, 100, 42)

// 递归分割算法
mDivision := maze.GenerateRecursiveDivision(20, 20, 42)

// 二叉树算法（可指定偏差方向）
mBinary := maze.GenerateBinaryTree(20, 20, 42, "NE")
```

### 不同求解方法

```go
// BFS求最短路径
shortestPath := maze.SolveBFS(m, m.Start, m.End)

// DFS快速求解
anyPath := maze.SolveDFS(m, m.Start, m.End)

// A*启发式求解（同样最短）
astarPath := maze.SolveAStar(m, m.Start, m.End)

// 墙跟随算法
leftPath := maze.SolveWallFollower(m, m.Start, m.End, "left")
rightPath := maze.SolveWallFollower(m, m.Start, m.End, "right")
```

### Unicode可视化

```go
// 不同样式
fmt.Println(maze.RenderUnicode(m, maze.StyleBox))    // 标准样式
fmt.Println(maze.RenderUnicode(m, maze.StyleRound))  // 圆角样式
fmt.Println(maze.RenderUnicode(m, maze.StyleDouble)) // 双线样式
fmt.Println(maze.RenderUnicode(m, maze.StyleBlock))  // 方块样式
```

### 序列化保存

```go
// JSON格式（易读）
jsonStr, err := maze.ToJSON(m)
restored, err := maze.FromJSON(jsonStr)

// 二进制格式（紧凑）
binaryData := maze.ToBinary(m)
restored, err := maze.FromBinary(binaryData)

// CSV格式
csvData := maze.ToCSV(m)

// 文件保存/加载
maze.SaveToFile(m, "maze.json")
m, err := maze.LoadFromFile("maze.json")
```

### 自定义起点终点

```go
m := maze.GenerateDFS(10, 10, 42)
m.Start = [2]int{0, 5}
m.End = [2]int{9, 5}
path := maze.SolveBFS(m, m.Start, m.End)
```

### 迷宫操作

```go
// 移除墙
m.RemoveWall(0, 0, 1, 0)

// 添加墙
m.AddWall(0, 0, 1, 0)

// 获取可通行邻居
passages := m.GetPassages(0, 0)

// 检查是否为完美迷宫
isPerfect := m.IsPerfect()

// 复制迷宫
mCopy := m.Copy()
```

## API 参考

### 生成器函数

| 函数 | 参数 | 返回 |
|------|------|------|
| `GenerateDFS(width, height, seed)` | 尺寸和随机种子 | *Maze |
| `GeneratePrim(width, height, seed)` | 尺寸和随机种子 | *Maze |
| `GenerateKruskal(width, height, seed)` | 尺寸和随机种子 | *Maze |
| `GenerateRecursiveDivision(width, height, seed)` | 尺寸和随机种子 | *Maze |
| `GenerateEllers(width, height, seed)` | 尺寸和随机种子 | *Maze |
| `GenerateBinaryTree(width, height, seed, bias)` | 尺寸、种子、偏差方向 | *Maze |

### 求解器函数

| 函数 | 参数 | 返回 |
|------|------|------|
| `SolveBFS(maze, start, end)` | 迷宫、起点、终点 | Path |
| `SolveDFS(maze, start, end)` | 迷宫、起点、终点 | Path |
| `SolveAStar(maze, start, end)` | 迷宫、起点、终点 | Path |
| `SolveWallFollower(maze, start, end, hand)` | 迷宫、起点、终点、左右手 | Path |
| `SolveDeadEndFilling(maze, start, end)` | 迷宫、起点、终点 | Path |

### Maze 结构方法

| 方法 | 描述 |
|------|------|
| `GetCell(x, y)` | 获取单元格 |
| `RemoveWall(x1, y1, x2, y2)` | 移除相邻单元格间的墙 |
| `AddWall(x1, y1, x2, y2)` | 添加墙 |
| `GetPassages(x, y)` | 获取可通行的邻居 |
| `IsPerfect()` | 检查是否为完美迷宫 |
| `Copy()` | 深拷贝迷宫 |

### 渲染函数

| 函数 | 描述 |
|------|------|
| `RenderASCII(maze)` | ASCII 渲染 |
| `RenderUnicode(maze, style)` | Unicode 渲染 |
| `RenderPath(maze, path, style)` | 带路径渲染 |
| `RenderSimple(maze)` | 简单紧凑格式 |

## 性能测试

在 50x50 迷宫上的测试结果：
- DFS生成：< 1ms
- BFS求解：< 1ms
- A*求解：< 1ms

在 100x100 迷宫上的测试结果：
- Eller生成：< 5ms
- BFS求解：< 10ms

## 运行测试

```bash
cd Go/maze_utils
go test -v
```

## 运行示例

```bash
cd Go/maze_utils
go run examples_maze_utils.go
```

## 许可证

MIT License

## 作者

AllToolkit 自动化生成
日期：2026-04-27