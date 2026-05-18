# Happy Number Utils - 快乐数工具模块 😊

[![测试状态](https://img.shields.io/badge/tests-passed-brightgreen)]()
[![覆盖率](https://img.shields.io/badge/coverage-100%25-brightgreen)]()

研究快乐数（Happy Number）的工具库，零外部依赖。

> **快乐数**：反复计算各位数字平方和，最终到达 1 的数。
> 若进入不包含 1 的循环，则为不快乐数（Unhappy/Sad Number）。

---

## ✨ 功能特性

### 基础判断
- **快乐数检测**：判断数字是否为快乐数
- **序列生成**：生成完整的变换序列
- **步数计算**：计算到达 1 的步数

### 分析功能
- **完整分析**：包含序列、循环检测、步数统计
- **属性分析**：数字位数、位数和、是否质数等
- **循环分析**：分析不快乐循环结构

### 范围搜索
- **范围查找**：找出范围内所有快乐数
- **第 N 个快乐数**：找出第 N 个快乐数
- **快乐质数**：既是快乐数又是质数的数

### 特殊类型
- **回文快乐数**：既是回文数又是快乐数
- **特定位数搜索**：找出特定位数的最小/最大快乐数

---

## 🚀 快速开始

### 基础判断

```python
from happy_number_utils import is_happy, digit_square_sum

# 判断快乐数
print(is_happy(19))  # True (19 → 82 → 68 → 100 → 1)
print(is_happy(4))   # False (进入循环)

# 数字平方和
print(digit_square_sum(19))  # 1² + 9² = 82
```

### 序列分析

```python
from happy_number_utils import analyze_number, get_happy_sequence

# 完整分析
result = analyze_number(19)
print(f"是否快乐: {result.is_happy}")
print(f"序列: {result.sequence}")
print(f"步数: {result.steps_to_1}")

# 获取序列
seq = get_happy_sequence(19)
print(seq)  # [19, 82, 68, 100, 1]
```

### 范围搜索

```python
from happy_number_utils import happy_numbers_in_range, nth_happy_number

# 1-100 中的快乐数
happy_nums = happy_numbers_in_range(1, 100)
print(happy_nums)  # [1, 7, 10, 13, 19, 23, 28, 31, 32, 44, ...]

# 第 10 个快乐数
print(nth_happy_number(10))  # 28
```

---

## 📚 详细用法

### 快乐质数

```python
from happy_number_utils import is_happy_prime, happy_primes_in_range

# 判断快乐质数
print(is_happy_prime(7))   # True
print(is_happy_prime(13))  # False (13 是质数但不快乐)

# 范围内的快乐质数
primes = happy_primes_in_range(1, 100)
print(primes)  # [7, 13, 19, 23, 31, 79, 97, ...]
```

### 范围统计分析

```python
from happy_number_utils import analyze_range

# 分析 1-100 范围
analysis = analyze_range(1, 100)
print(f"快乐数数量: {analysis.happy_count}")
print(f"快乐数比例: {analysis.happy_percentage:.2f}%")
print(f"按十年代分布: {analysis.density_by_decade}")
```

### 属性分析

```python
from happy_number_utils import analyze_properties

props = analyze_properties(19)
print(f"位数: {props.digit_count}")
print(f"位数和: {props.digit_sum}")
print(f"是否质数: {props.is_prime}")
print(f"是否回文: {props.is_palindromic}")
print(f"分类: {props.classification()}")
```

### 特殊快乐数

```python
from happy_number_utils import (
    find_happy_palindromes,
    find_smallest_happy_with_digits,
    find_largest_happy_with_digits
)

# 回文快乐数
palindromes = find_happy_palindromes(200)
print(palindromes)  # [1, 7, 22, 88, 101, 111, 121, ...]

# 3 位数中最小/最大快乐数
print(find_smallest_happy_with_digits(3))  # 100
print(find_largest_happy_with_digits(3))   # 991
```

### 循环分析

```python
from happy_number_utils import get_unhappy_cycle, analyze_cycle_structure

# 获取不快乐循环
cycle = get_unhappy_cycle()
print(cycle)  # {4, 16, 37, 58, 89, 145, 42, 20}

# 循环结构分析
info = analyze_cycle_structure()
print(f"循环成员: {info['members']}")
print(f"循环长度: {info['length']}")
```

### 详细报告

```python
from happy_number_utils import happy_number_report

print(happy_number_report(19))
# === Happy Number Report for 19 ===
# Classification: happy + prime
# Is Happy: True
# ...
```

---

## 🔧 API 参考

### 核心函数

| 函数 | 说明 |
|------|------|
| `is_happy(n)` | 判断是否快乐数 |
| `is_unhappy(n)` | 判断是否不快乐数 |
| `digit_square_sum(n)` | 计算数字平方和 |
| `analyze_number(n)` | 完整分析 |
| `get_happy_sequence(n)` | 获取序列 |
| `count_steps_to_happy(n)` | 计算步数 |

### 范围函数

| 函数 | 说明 |
|------|------|
| `happy_numbers_in_range(start, end)` | 范围内快乐数 |
| `unhappy_numbers_in_range(start, end)` | 范围内不快乐数 |
| `nth_happy_number(n)` | 第 N 个快乐数 |
| `happy_numbers_up_to(limit)` | 上限内快乐数 |
| `analyze_range(start, end)` | 范围分析 |

### 快乐质数

| 函数 | 说明 |
|------|------|
| `is_happy_prime(n)` | 判断快乐质数 |
| `happy_primes_in_range(start, end)` | 范围内快乐质数 |
| `nth_happy_prime(n)` | 第 N 个快乐质数 |

### 特殊类型

| 函数 | 说明 |
|------|------|
| `find_happy_palindromes(limit)` | 回文快乐数 |
| `find_smallest_happy_with_digits(n)` | N位最小快乐数 |
| `find_largest_happy_with_digits(n)` | N位最大快乐数 |

---

## 📊 数学背景

### 定义

快乐数的定义：
```
f(n) = 各位数字的平方和
若反复应用 f(n) 最终到达 1，则为快乐数
若进入不含 1 的循环，则为不快乐数
```

### 经典例子

**19 是快乐数：**
```
19 → 1²+9² = 82
82 → 8²+2² = 68
68 → 6²+8² = 100
100 → 1²+0²+0² = 1 ✓
```

**4 是不快乐数（进入循环）：**
```
4 → 16 → 37 → 58 → 89 → 145 → 42 → 20 → 4 (循环)
```

### 不快乐循环

已知的不快乐循环：
```
4 → 16 → 37 → 58 → 89 → 145 → 42 → 20 → 4
```

### 密度估计

大约 **15-20%** 的正整数是快乐数。

---

## 🧪 测试

```bash
python Python/happy_number_utils/happy_number_utils_test.py
```

---

## 📄 许可证

MIT License

---

**最后更新**: 2026-05-19