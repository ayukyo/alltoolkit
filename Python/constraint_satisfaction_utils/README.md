# 约束满足问题工具模块 (Constraint Satisfaction Utilities)

一个零外部依赖的约束满足问题（CSP）求解器，支持多种求解策略和启发式算法。

## 功能特性

### 核心功能
- **变量和域定义** - 定义问题的变量及其可能的取值
- **约束定义** - 支持多种约束类型
- **求解算法** - 回溯搜索、前向检查、AC-3 约束传播
- **启发式** - MRV、度启发式、LCV 等变量/值选择策略
- **多解查找** - 支持查找所有解

### 约束类型
- `UnaryConstraint` - 一元约束（单个变量的约束）
- `BinaryConstraint` - 二元约束（两个变量之间的关系）
- `AllDifferentConstraint` - 所有变量取值不同
- `AllEqualConstraint` - 所有变量取值相同
- `SumConstraint` - 变量值之和等于目标值
- `MaxValueConstraint` - 最大值约束
- 自定义约束 - 支持自定义约束类

### 预定义问题
- **N 皇后问题** - 经典棋盘布局问题
- **数独问题** - 9x9 数独求解
- **图着色问题** - 图的顶点着色
- **调度问题** - 任务调度约束

### 求解策略
- **变量选择启发式**
  - `none` - 默认顺序
  - `mrv` - 最小剩余值（Minimum Remaining Values）
  - `degree` - 度启发式
  - `mrv_degree` - MRV + 度启发式组合

- **值选择启发式**
  - `none` - 默认顺序
  - `lcv` - 最少约束值（Least Constraining Value）

- **推理方法**
  - `none` - 无推理
  - `forward_checking` - 前向检查
  - `ac3` - AC-3 约束传播

## 安装使用

```python
from constraint_satisfaction_utils.mod import (
    CSP, CSPSolver,
    BinaryConstraint, AllDifferentConstraint,
    solve_n_queens, solve_sudoku, solve_graph_coloring
)
```

## 使用示例

### 1. 基础 CSP 求解

```python
# 定义变量和域
variables = ['Alice', 'Bob', 'Charlie']
domains = {v: ['红', '绿', '蓝'] for v in variables}

# 定义约束：所有人颜色不同
constraints = [AllDifferentConstraint(variables)]

# 创建并求解
csp = CSP(variables, domains, constraints)
solver = CSPSolver(csp, inference='ac3')
solution = solver.solve()
# {'Alice': '红', 'Bob': '绿', 'Charlie': '蓝'}
```

### 2. N 皇后问题

```python
# 求解 8 皇后
solution = solve_n_queens(8)

# 打印棋盘
print(print_n_queens_solution(solution, 8))

# 计算解数量
count = count_n_queens_solutions(4)  # 2
```

### 3. 数独问题

```python
# 定义数独谜题
puzzle = [
    [5, 3, 0, 0, 7, 0, 0, 0, 0],
    [6, 0, 0, 1, 9, 5, 0, 0, 0],
    ...
]

# 求解
solution = solve_sudoku(puzzle)

# 打印解
print(print_sudoku_solution(solution))
```

### 4. 图着色问题

```python
vertices = ['A', 'B', 'C', 'D']
edges = [('A', 'B'), ('B', 'C'), ('C', 'D'), ('A', 'D')]
colors = ['红', '绿', '蓝']

solution = solve_graph_coloring(vertices, edges, colors)
# {'A': '红', 'B': '绿', 'C': '红', 'D': '蓝'}
```

### 5. 二元约束

```python
# 任务调度：某些任务不能同时执行
tasks = ['Task1', 'Task2', 'Task3']
time_slots = ['上午', '下午', '晚上']

constraints = [
    BinaryConstraint('Task1', 'Task2', lambda t1, t2: t1 != t2),
    BinaryConstraint('Task2', 'Task3', lambda t1, t2: t1 != t2),
]

csp = CSP(tasks, {t: time_slots for t in tasks}, constraints)
solver = CSPSolver(csp)
solution = solver.solve()
```

### 6. 自定义约束

```python
class MyConstraint(Constraint):
    def __init__(self, x, y):
        super().__init__([x, y])
        self.x = x
        self.y = y
    
    def is_satisfied(self, assignment):
        if self.x not in assignment or self.y not in assignment:
            return True
        return assignment[self.x] + assignment[self.y] > 10

csp.add_constraint(MyConstraint('a', 'b'))
```

### 7. 查找所有解

```python
solver = CSPSolver(csp)
solutions = solver.find_all_solutions(max_solutions=100)
```

## 性能统计

求解器提供统计数据：

```python
solver = CSPSolver(csp)
solution = solver.solve()

print(f"探索节点数: {solver.nodes_explored}")
print(f"回溯次数: {solver.backtracks}")
```

## API 参考

### CSP 类

```python
CSP(variables, domains, constraints)
```

- `variables`: 变量列表
- `domains`: 变量域字典 `{var: [values]}`
- `constraints`: 约束列表

### CSPSolver 类

```python
CSPSolver(csp, var_heuristic='mrv', value_heuristic='lcv', inference='ac3')
```

- `solve()`: 求解，返回解或 None
- `find_all_solutions(max_solutions=100)`: 查找所有解

### 便捷函数

- `solve_n_queens(n, inference='ac3')`: 求解 N 皇后
- `solve_sudoku(grid, inference='ac3')`: 求解数独
- `solve_graph_coloring(vertices, edges, colors, inference='ac3')`: 求解图着色
- `count_n_queens_solutions(n)`: 计算 N 皇后解数量
- `print_n_queens_solution(solution, n)`: 打印 N 皇后解
- `print_sudoku_solution(grid)`: 打印数独解

## 应用场景

- **调度系统** - 课程安排、会议时间分配
- **资源分配** - 带宽分配、座位分配
- **配置问题** - 产品配置、系统配置
- **游戏 AI** - 棋类游戏、逻辑谜题
- **网络设计** - 频率分配、通道分配
- **逻辑推理** - 知识推理、推理引擎

## 算法说明

### 回溯搜索
基本的深度优先搜索，按顺序尝试值，遇到冲突时回溯。

### 前向检查
在赋值后检查未赋值变量的域，移除不一致的值，提前发现失败。

### AC-3 约束传播
弧一致性算法，通过传播约束减少域大小，提高搜索效率。

### MRV 启发式
选择域最小的变量，减少分支因子。

### 度启发式
选择约束最多的变量，快速减少其他变量的域。

### LCV 启发式
选择对其他变量影响最小的值，保持更多的选择余地。

## 许可证

MIT License

## 作者

AllToolkit