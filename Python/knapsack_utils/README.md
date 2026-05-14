# Knapsack Utils 🎒

背包问题求解工具模块 - 提供多种背包问题求解算法实现。

## 功能特性

- **0/1 背包问题** - 动态规划、递归、分支限界
- **完全背包问题** - 物品可无限取用
- **多重背包问题** - 物品有数量限制
- **分数背包问题** - 贪心算法求解
- **多维背包问题** - 多约束条件
- **多目标背包问题** - 多目标优化
- **最优解回溯** - 获取具体物品选择

## 快速开始

```python
from knapsack_utils.mod import Item, solve_01_knapsack

# 创建物品列表
items = [
    Item(weight=2, value=3, name="物品A"),
    Item(weight=3, value=4, name="物品B"),
    Item(weight=4, value=5, name="物品C"),
    Item(weight=5, value=6, name="物品D"),
]

# 解决 0/1 背包问题
result = solve_01_knapsack(items, capacity=10)

print(f"最大价值: {result.max_value}")
print(f"总重量: {result.total_weight}")
print(f"选中物品: {result.selected_items}")
```

## 核心函数

### solve_01_knapsack

```python
from knapsack_utils.mod import solve_01_knapsack, KnapsackMethod

# 基础调用
result = solve_01_knapsack(items, capacity=10)

# 指定方法
result = solve_01_knapsack(
    items, 
    capacity=10,
    method=KnapsackMethod.DP_OPTIMIZED  # 空间优化的动态规划
)
```

### solve_complete_knapsack

```python
from knapsack_utils.mod import solve_complete_knapsack

# 完全背包：物品可无限取用
result = solve_complete_knapsack(items, capacity=10)
```

### solve_fractional_knapsack

```python
from knapsack_utils.mod import solve_fractional_knapsack

# 分数背包：物品可分割
result = solve_fractional_knapsack(items, capacity=10)
```

## 数据结构

### Item

```python
from knapsack_utils.mod import Item

item = Item(
    weight=2.5,      # 重量
    value=10,        # 价值
    name="商品A",    # 名称
    count=3          # 数量（用于多重背包）
)

# 价值密度（价值/重量）
print(item.ratio)  # 4.0
```

### KnapsackResult

```python
from knapsack_utils.mod import KnapsackResult

result = solve_01_knapsack(items, capacity=10)

print(result.max_value)        # 最大价值
print(result.total_weight)     # 实际重量
print(result.selected_items)   # 选中的物品列表
print(result.selected_indices) # 选中的物品索引
```

## 求解方法

| 方法 | 适用场景 | 特点 |
|------|----------|------|
| DP | 0/1背包 | 时间O(nW)，空间O(nW) |
| DP_OPTIMIZED | 0/1背包 | 时间O(nW)，空间O(W) |
| RECURSIVE | 小规模问题 | 记忆化搜索 |
| BRANCH_BOUND | 大规模问题 | 剪枝优化 |
| GREEDY | 分数背包 | 按价值密度排序 |

## 多维背包

```python
from knapsack_utils.mod import solve_multi_dimensional_knapsack

# 多约束背包（如：重量限制 + 体积限制）
constraints = {
    'weight': 10,   # 重量上限
    'volume': 8     # 体积上限
}
items_with_attrs = [
    Item(weight=2, value=3, name="A", attributes={'volume': 1}),
    Item(weight=3, value=4, name="B", attributes={'volume': 2}),
]

result = solve_multi_dimensional_knapsack(items_with_attrs, constraints)
```

## 最优解回溯

```python
from knapsack_utils.mod import backtrack_solution

# 获取具体选择了哪些物品
selected = backtrack_solution(items, capacity=10, dp_table=result.dp_table)
for item in selected:
    print(f"{item.name}: 重量={item.weight}, 价值={item.value}")
```

## 测试

```bash
python Python/knapsack_utils/knapsack_utils_test.py
```

## 许可证

MIT License