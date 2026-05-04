# 汉诺塔工具 (Tower of Hanoi Utils)

经典汉诺塔问题的完整解决方案，支持多种求解算法和多柱扩展。

## 功能特性

- ✅ **递归求解算法** - 经典的分治解法
- ✅ **迭代求解算法** - 非递归实现，避免栈溢出
- ✅ **生成器模式** - 内存高效，支持大规模求解
- ✅ **状态管理** - 完整的状态类，支持移动验证
- ✅ **多柱汉诺塔** - Frame-Stewart算法支持4柱及以上
- ✅ **解验证** - 验证移动序列的正确性
- ✅ **可视化** - ASCII艺术可视化每一步
- ✅ **零依赖** - 纯Python实现

## 安装

```python
from hanoi_utils.mod import *
```

## 快速开始

### 基本求解

```python
from mod import solve_recursive, solve_iterative

# 递归求解
moves = solve_recursive(3)
for move in moves:
    print(move)
# 输出:
# 移动盘子 1 从柱 0 到柱 2
# 移动盘子 2 从柱 0 到柱 1
# ...

# 迭代求解
moves = solve_iterative(3)
```

### 使用求解器类

```python
from mod import HanoiSolver

solver = HanoiSolver(4)  # 4个盘子
solver.solve('recursive')
print(f"移动次数: {solver.move_count}")
print(f"是否最优: {solver.is_optimal()}")
```

### 快捷函数

```python
from mod import hanoi

moves = hanoi(3)  # 默认递归
moves = hanoi(3, method='iterative')  # 迭代
```

## 核心功能

### 1. 求解算法

```python
# 递归求解
moves = solve_recursive(num_disks, from_peg=0, to_peg=2, aux_peg=1)

# 迭代求解
moves = solve_iterative(num_disks, from_peg=0, to_peg=2, aux_peg=1)

# 生成器模式（内存高效）
for move in solve_generator(num_disks):
    print(move)
```

### 2. 状态管理

```python
from mod import HanoiState, MoveError

state = HanoiState(3)  # 3个盘子

# 查看状态
print(state)
#       │       │       │
#       │       │       │
#     ███       │       │
#    █████      │       │
#  ███████      │       │
#  ────────   ────────   ────────
#      0         1         2

# 移动验证
if state.is_valid_move(0, 2):
    state.move(0, 2)

# 检查是否解决
if state.is_solved():
    print("完成!")
```

### 3. 最少移动次数

```python
from mod import min_moves, min_moves_frame_stewart

# 3柱汉诺塔: 2^n - 1
print(min_moves(3))  # 7
print(min_moves(10)) # 1023

# 多柱汉诺塔
print(min_moves_frame_stewart(4, 4))  # 9 (4柱)
print(min_moves_frame_stewart(4, 5))  # 7 (5柱)
```

### 4. 多柱汉诺塔

```python
from mod import solve_frame_stewart

# 4柱汉诺塔（比3柱更少的移动）
moves = solve_frame_stewart(4, num_pegs=4)
print(f"4柱移动次数: {len(moves)}")  # 9次
# 对比3柱: 15次
```

### 5. 解验证

```python
from mod import validate_solution

moves = solve_recursive(3)
is_valid = validate_solution(3, moves)  # True

# 验证不完整的解
partial_moves = moves[:3]
is_valid = validate_solution(3, partial_moves)  # False
```

### 6. 解分析

```python
from mod import analyze_moves

moves = solve_recursive(5)
analysis = analyze_moves(moves)
print(f"总移动次数: {analysis['total_moves']}")
print(f"盘子1移动次数: {analysis['moves_per_disk'][1]}")  # 16次
print(f"盘子5移动次数: {analysis['moves_per_disk'][5]}")  # 1次
```

### 7. 可视化

```python
from mod import visualize_moves, hanoi_demo

# 步骤可视化
moves = solve_recursive(2)
for step in visualize_moves(2, moves):
    print(step)

# 完整演示
print(hanoi_demo(3))
```

## API 参考

### 核心函数

| 函数 | 说明 |
|------|------|
| `solve_recursive(n)` | 递归求解n个盘子 |
| `solve_iterative(n)` | 迭代求解n个盘子 |
| `solve_generator(n)` | 生成器求解 |
| `min_moves(n)` | 计算最少移动次数 (2^n - 1) |
| `hanoi(n)` | 快捷求解函数 |

### 多柱函数

| 函数 | 说明 |
|------|------|
| `solve_frame_stewart(n, p)` | 多柱汉诺塔求解 |
| `min_moves_frame_stewart(n, p)` | 多柱最少移动次数估计 |

### 验证函数

| 函数 | 说明 |
|------|------|
| `validate_solution(n, moves)` | 验证解的正确性 |
| `is_optimal_solution(n, moves)` | 判断是否为最优解 |

### 类

| 类 | 说明 |
|-----|------|
| `HanoiState` | 汉诺塔状态管理 |
| `HanoiSolver` | 求解器类（面向对象接口） |
| `Move` | 移动记录（dataclass） |

## 数学背景

### 3柱汉诺塔

- 最少移动次数：`2^n - 1`
- 解决方案：递归地将n-1个盘子移到辅助柱，移动最大盘，再递归移回

### 多柱汉诺塔（Frame-Stewart算法）

对于4柱及以上，使用Frame-Stewart算法估计最少移动次数：

```
T(n, p) = min(2 * T(k, p) + T(n-k, p-1))  for k in [1, n-1]
```

其中 `T(n, 3) = 2^n - 1`

## 示例输出

```
汉诺塔演示（3个盘子）
最少移动次数: 2^3 - 1 = 7
========================================
      │       │       │
    ███       │       │
   █████      │       │
 ███████      │       │
────────────────────────────

第 1 步: 移动盘子 1 从柱 0 到柱 2
...
```

## 测试

```bash
python -m pytest hanoi_utils_test.py -v
```

## 许可

MIT License