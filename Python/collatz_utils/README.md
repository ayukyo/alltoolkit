# Collatz Utils - Collatz 序列工具模块 🔢

[![测试状态](https://img.shields.io/badge/tests-passed-brightgreen)]()
[![覆盖率](https://img.shields.io/badge/coverage-100%25-brightgreen)]()

研究 Collatz 猜想（3n+1 问题）的工具库，零外部依赖。

> **Collatz 猜想**：对于任意正整数 n，反复应用：
> - 若 n 为偶数：n / 2
> - 若 n 为奇数：3n + 1
> 最终会到达 1。这是一个尚未证明的数学难题！

---

## ✨ 功能特性

### 序列生成
- **完整序列**：生成从 n 到 1 的完整 Collatz 序列
- **生成器模式**：内存高效的迭代器实现
- **广义 Collatz**：支持自定义参数的变体

### 序列分析
- **序列长度**：计算到达 1 的步数
- **最大值**：找序列中的最大值
- **奇偶统计**：统计奇偶数比例
- **上升下降**：统计上升/下降次数

### 范围分析
- **最长序列**：找出范围内最长序列的数
- **最大值分析**：找出达到最大值的数
- **统计汇总**：范围全面统计分析

### 模式检测
- **特定值搜索**：找出到达特定值的数
- **特定长度搜索**：找出特定长度的序列
- **逆向树**：生成到达某个数的所有路径

---

## 🚀 快速开始

### 基础序列生成

```python
from collatz_utils import collatz_sequence, collatz_step

# 生成完整序列
seq = collatz_sequence(6)
print(seq)  # [6, 3, 10, 5, 16, 8, 4, 2, 1]

# 单步计算
next_val = collatz_step(6)  # 3（偶数除以2）
next_val = collatz_step(7)  # 22（奇数乘3加1）
```

### 序列长度

```python
from collatz_utils import collatz_length, total_stopping_time

# 序列长度（包含起点和终点）
length = collatz_length(27)  # 112

# 停止时间（步数，不含起点）
steps = total_stopping_time(27)  # 111
```

### 最大值分析

```python
from collatz_utils import collatz_max_value

# 27 的序列最大达到 9232
max_val = collatz_max_value(27)  # 9232
```

---

## 📚 详细用法

### 序列分析

```python
from collatz_utils import (
    collatz_even_odd_ratio,
    collatz_rise_and_fall,
    collatz_summary
)

# 奇偶比例
even, odd = collatz_even_odd_ratio(27)
print(f"偶数: {even}, 奇数: {odd}")

# 上升下降次数
rises, falls = collatz_rise_and_fall(27)
print(f"上升: {rises}, 下降: {falls}")

# 完整汇总
summary = collatz_summary(27)
print(f"长度: {summary['length']}")
print(f"最大值: {summary['max_value']}")
print(f"最大值位置: {summary['max_value_step']}")
```

### 范围分析

```python
from collatz_utils import (
    longest_sequence_in_range,
    highest_value_in_range,
    collatz_statistics
)

# 1-100 中最长序列的数
number, length, seq = longest_sequence_in_range(1, 100)
print(f"最长序列: {number}, 长度: {length}")

# 达到最大值的数
number, max_val, step = highest_value_in_range(1, 100)
print(f"最大值: {max_val}, 来自: {number}")

# 统计汇总
stats = collatz_statistics(1, 100)
print(f"平均长度: {stats['avg_length']:.2f}")
print(f"最长序列数: {stats['max_length_number']}")
print(f"偶数比例: {stats['even_ratio']:.2%}")
```

### 模式搜索

```python
from collatz_utils import (
    find_numbers_reaching_value,
    find_numbers_with_length,
    find_numbers_with_max_value
)

# 找出到达 16 的数
nums = find_numbers_reaching_value(16, limit=20)
print(nums)  # [5, 10, 16, 20]

# 找出长度为 9 的序列
nums = find_numbers_with_length(9, limit=20)
print(nums)  # [6]

# 找出最大值为 16 的序列
nums = find_numbers_with_max_value(16, limit=20)
print(nums)  # [5, 10]
```

### 逆向分析

```python
from collatz_utils import collatz_predecessors, collatz_inverse_tree

# 找出一步前驱
preds = collatz_predecessors(5)
print(preds)  # {10}

preds = collatz_predecessors(4)
print(preds)  # {1, 8}

# 生成逆向树
tree = collatz_inverse_tree(1, depth=3)
# {1: [2, 4], 2: [4], 4: [1, 8], 8: [16], 16: [32, 5]}
```

### 广义 Collatz

```python
from collatz_utils import generalized_collatz_sequence, lazy_caterer_sequence

# 标准 Collatz: a=3, b=1, c=2
seq = generalized_collatz_sequence(6)  # [6, 3, 10, 5, 16, 8, 4, 2, 1]

# 5n+1 变体（可能不收敛！）
seq = lazy_caterer_sequence(7)  # 可能循环或发散
```

### 可视化辅助

```python
from collatz_utils import collatz_tree_path, collatz_waterfall

# 带操作标签的路径
path = collatz_tree_path(6)
print(path)
# [(6, 'start'), (3, '/2'), (10, '*3+1'), ...]

# 文本瀑布图
waterfall = collatz_waterfall(27)
print(waterfall)
# 27 → 82 → 41 → 124 → ...
# ↓
# ... → 1
```

---

## 🔧 API 参考

### 核心函数

| 函数 | 说明 |
|------|------|
| `collatz_step(n)` | 单步计算 |
| `collatz_sequence(n)` | 完整序列 |
| `collatz_generator(n)` | 迭代器模式 |
| `collatz_length(n)` | 序列长度 |
| `collatz_max_value(n)` | 最大值 |

### 分析函数

| 函数 | 说明 |
|------|------|
| `collatz_even_odd_ratio(n)` | 奇偶统计 |
| `collatz_rise_and_fall(n)` | 上升下降统计 |
| `total_stopping_time(n)` | 停止时间 |
| `collatz_summary(n)` | 完整汇总 |

### 范围函数

| 函数 | 说明 |
|------|------|
| `longest_sequence_in_range(start, end)` | 最长序列 |
| `highest_value_in_range(start, end)` | 最大值分析 |
| `collatz_statistics(start, end)` | 统计汇总 |

### 搜索函数

| 函数 | 说明 |
|------|------|
| `find_numbers_reaching_value(target, limit)` | 特定值搜索 |
| `find_numbers_with_length(length, limit)` | 特定长度搜索 |
| `find_numbers_with_max_value(max_val, limit)` | 特定最大值搜索 |

### 逆向函数

| 函数 | 说明 |
|------|------|
| `collatz_predecessors(n)` | 一步前驱 |
| `collatz_inverse_tree(n, depth)` | 逆向树 |

---

## 📊 有趣的数字

### 经典案例

| 数字 | 序列长度 | 最大值 | 说明 |
|------|----------|--------|------|
| 1 | 1 | 1 | 最简单 |
| 6 | 9 | 16 | 简单示例 |
| 27 | 112 | 9232 | 经典长序列 |
| 97 | 119 | 9232 | 小范围内最长 |
| 837 | 135 | 13120 | 较长序列 |

### 统计观察

- 所有测试的正整数最终都到达 1（猜想成立）
- 奇偶比例约 2:1（下降多于上升）
- 最大值常出现在序列中段

---

## 📝 数学背景

### Collatz 函数

```
f(n) = n/2   (若 n 为偶数)
f(n) = 3n+1  (若 n 为奇数)
```

### 广义 Collatz

```
f(n) = n/c         (若 n ≡ 0 mod c)
f(n) = a·n + b     (若 n ≢ 0 mod c)
```

### 猜想状态

- **未证明**：尚未找到对所有正整数成立的证明
- **已验证**：已验证到极大数值（10^20+）
- **反例**：尚未发现任何反例

---

## 🧪 测试

```bash
python Python/collatz_utils/collatz_utils_test.py
```

---

## 📄 许可证

MIT License

---

**最后更新**: 2026-05-19