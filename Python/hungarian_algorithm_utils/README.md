# Hungarian Algorithm Utils 📊

匈牙利算法工具模块 - 解决分配问题的最优算法。

## 功能特性

- **分配问题求解** - 找到最优分配方案
- **成本矩阵处理** - 支持任意大小的方阵
- **最大收益模式** - 可转换为收益最大化
- **时间复杂度 O(n³)** - 经典算法实现

## 快速开始

```python
from hungarian_algorithm_utils.mod import HungarianAlgorithm

# 成本矩阵：工人 i 完成任务 j 的成本
cost_matrix = [
    [10, 19, 8, 15],
    [17, 14, 12, 13],
    [15, 16, 13, 14],
    [12, 15, 11, 10],
]

# 创建算法实例
hungarian = HungarianAlgorithm(cost_matrix)

# 求解
assignment = hungarian.solve()
# [(0, 2), (1, 3), (2, 1), (3, 0)]
# 工人0→任务2，工人1→任务3，工人2→任务1，工人3→任务0

# 获取总成本
total_cost = hungarian.get_total_cost()
print(f"最小总成本: {total_cost}")
```

## 核心类

### HungarianAlgorithm

```python
from hungarian_algorithm_utils.mod import HungarianAlgorithm

hungarian = HungarianAlgorithm(cost_matrix)

# 求解分配
result = hungarian.solve()

# 获取总成本
cost = hungarian.get_total_cost()

# 获取分配详情
for worker, task in result:
    print(f"工人 {worker} → 任务 {task}")
```

## 应用场景

### 任务分配

```python
# 5个工人分配到5个任务
costs = [
    [10, 12, 19, 8, 15],
    [5, 17, 14, 12, 13],
    [15, 16, 13, 14, 11],
    [12, 15, 11, 10, 9],
    [8, 9, 10, 11, 12],
]

hungarian = HungarianAlgorithm(costs)
assignment = hungarian.solve()
```

### 收益最大化

```python
from hungarian_algorithm_utils.mod import solve_maximization

# 收益矩阵（转换为成本）
profit_matrix = [
    [100, 200, 150],
    [180, 120, 160],
    [140, 170, 130],
]

# 直接求解最大化问题
assignment = solve_maximization(profit_matrix)
```

### 非方阵处理

```python
from hungarian_algorithm_utils.mod import solve_assignment

# 工人多于任务（自动添加虚拟任务）
costs = [
    [10, 8],
    [12, 9],
    [15, 11],
    [8, 7],
]

assignment = solve_assignment(costs)
```

## 算法原理

匈牙利算法基于以下步骤：

1. **行缩减** - 每行减去最小值
2. **列缩减** - 每列减去最小值
3. **覆盖零** - 用最少线覆盖所有零
4. **调整** - 未覆盖元素减去最小未覆盖值
5. **迭代** - 直到找到最优分配

## 性能特点

| 特性 | 说明 |
|------|------|
| 时间复杂度 | O(n³) |
| 空间复杂度 | O(n²) |
| 适用规模 | n ≤ 1000 |

## 测试

```bash
python Python/hungarian_algorithm_utils/hungarian_algorithm_utils_test.py
```

## 许可证

MIT License