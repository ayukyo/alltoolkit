# Fractions Utilities 🧮

**Python 分数运算工具模块 - 零依赖，生产就绪**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python: 3.7+](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/downloads/)

---

## 📖 简介

`fractions_utils` 是一个功能完整的分数运算工具模块，基于 Python 标准库的 `fractions` 模块构建。提供分数创建、解析、算术运算、比较、转换、序列生成等功能，所有操作均保持精确的有理数计算，避免浮点数精度问题。

### 核心特性

- ✅ **零依赖** - 仅使用 Python 标准库
- ✅ **精确计算** - 使用 `Fraction` 类型，避免浮点误差
- ✅ **功能完整** - 50+ 个函数覆盖所有常见分数操作
- ✅ **类型安全** - 完整的类型注解
- ✅ **测试覆盖** - 100+ 测试用例
- ✅ **文档完善** - 每个函数都有详细文档和示例

---

## 🚀 快速开始

### 安装

无需安装！只需将 `mod.py` 复制到你的项目中即可使用。

```bash
# 或者从 AllToolkit 复制
cp AllToolkit/Python/fractions_utils/mod.py your_project/
```

### 基本使用

```python
from mod import *

# 创建分数
f1 = parse_fraction("3/4")      # Fraction(3, 4)
f2 = parse_fraction(0.5)        # Fraction(1, 2)
f3 = create_fraction(2, 3)      # Fraction(2, 3)

# 算术运算
result = add(f1, f2)            # Fraction(5, 4)
result = multiply(f1, f2)       # Fraction(3, 8)
result = divide(f1, f2)         # Fraction(3, 2)

# 比较
compare(f1, f2)                 # 1 (f1 > f2)
equals("2/4", "1/2")            # True

# 转换
to_decimal(f1)                  # 0.75
to_percentage(f1)               # 75.0
to_string(f1, 'mixed')          # "3/4"
```

---

## 📚 API 参考

### 创建和解析

| 函数 | 描述 | 示例 |
|------|------|------|
| `create_fraction(num, denom)` | 创建分数 | `create_fraction(3, 4)` → `Fraction(3, 4)` |
| `parse_fraction(value)` | 解析各种输入为分数 | `parse_fraction("3/4")`, `parse_fraction(0.75)`, `parse_fraction((3, 4))` |
| `from_decimal(value, max_denom)` | 小数转分数 | `from_decimal(0.333)` → `Fraction(1, 3)` |
| `from_percentage(value)` | 百分比转分数 | `from_percentage(25)` → `Fraction(1, 4)` |

### 算术运算

| 函数 | 描述 | 示例 |
|------|------|------|
| `add(*fractions)` | 加法 | `add("1/2", "1/3")` → `Fraction(5, 6)` |
| `subtract(minuend, *subtrahends)` | 减法 | `subtract("3/4", "1/2")` → `Fraction(1, 4)` |
| `multiply(*fractions)` | 乘法 | `multiply("1/2", "2/3")` → `Fraction(1, 3)` |
| `divide(dividend, *divisors)` | 除法 | `divide("3/4", "1/2")` → `Fraction(3, 2)` |
| `power(base, exponent)` | 幂运算 | `power("1/2", 3)` → `Fraction(1, 8)` |
| `reciprocal(fraction)` | 倒数 | `reciprocal("3/4")` → `Fraction(4, 3)` |
| `negate(fraction)` | 取反 | `negate("3/4")` → `Fraction(-3, 4)` |
| `abs_fraction(fraction)` | 绝对值 | `abs_fraction("-3/4")` → `Fraction(3, 4)` |

### 比较运算

| 函数 | 描述 | 示例 |
|------|------|------|
| `compare(a, b)` | 比较两分数 | `compare("1/2", "2/3")` → `-1` |
| `equals(a, b)` | 相等判断 | `equals("2/4", "1/2")` → `True` |
| `less_than(a, b)` | 小于判断 | `less_than("1/3", "1/2")` → `True` |
| `greater_than(a, b)` | 大于判断 | `greater_than("3/4", "1/2")` → `True` |
| `min_fraction(*fractions)` | 最小值 | `min_fraction("1/2", "1/3")` → `Fraction(1, 3)` |
| `max_fraction(*fractions)` | 最大值 | `max_fraction("1/2", "2/3")` → `Fraction(2, 3)` |

### 简化和规范化

| 函数 | 描述 | 示例 |
|------|------|------|
| `simplify(fraction)` | 化简分数 | `simplify("6/8")` → `Fraction(3, 4)` |
| `normalize(fraction)` | 规范化（正分母） | `normalize("3/-4")` → `Fraction(-3, 4)` |
| `to_mixed_number(fraction)` | 转带分数 | `to_mixed_number("7/4")` → `(1, Fraction(3, 4))` |
| `to_improper_fraction(w, n, d)` | 带分数转假分数 | `to_improper_fraction(1, 3, 4)` → `Fraction(7, 4)` |

### 转换函数

| 函数 | 描述 | 示例 |
|------|------|------|
| `to_decimal(fraction, precision)` | 转小数 | `to_decimal("1/3")` → `0.3333333333` |
| `to_percentage(fraction, precision)` | 转百分比 | `to_percentage("1/4")` → `25.0` |
| `to_string(fraction, format)` | 转字符串 | `to_string("7/4", 'mixed')` → `"1 3/4"` |

### GCD/LCM 工具

| 函数 | 描述 | 示例 |
|------|------|------|
| `gcd(*numbers)` | 最大公约数 | `gcd(12, 18)` → `6` |
| `lcm(*numbers)` | 最小公倍数 | `lcm(4, 6)` → `12` |
| `common_denominator(*fractions)` | 公分母 | `common_denominator("1/4", "1/6")` → `12` |
| `with_common_denominator(*fractions)` | 通分 | `with_common_denominator("1/4", "1/6")` → `[3/12, 2/12]` |

### 批量操作

| 函数 | 描述 | 示例 |
|------|------|------|
| `sum_fractions(list)` | 求和 | `sum_fractions(["1/2", "1/3", "1/6"])` → `Fraction(1, 1)` |
| `product_fractions(list)` | 求积 | `product_fractions(["1/2", "2/3"])` → `Fraction(1, 3)` |
| `average_fractions(list)` | 平均值 | `average_fractions(["1/2", "1/4"])` → `Fraction(3, 8)` |
| `map_fractions(list, func)` | 映射 | `map_fractions(["1/2"], reciprocal)` → `[Fraction(2, 1)]` |
| `filter_fractions(list, pred)` | 过滤 | `filter_fractions(["1/2", "3/4"], lambda x: x > 0.5)` |

### 序列和级数

| 函数 | 描述 | 示例 |
|------|------|------|
| `arithmetic_sequence(first, diff, n)` | 等差数列 | `arithmetic_sequence(1, 1, 5)` → `[1, 2, 3, 4, 5]` |
| `geometric_sequence(first, ratio, n)` | 等比数列 | `geometric_sequence(1, "1/2", 4)` → `[1, 1/2, 1/4, 1/8]` |
| `arithmetic_series_sum(first, diff, n)` | 等差级数和 | `arithmetic_series_sum(1, 1, 5)` → `Fraction(15, 1)` |
| `geometric_series_sum(first, ratio, n)` | 等比级数和 | `geometric_series_sum("1/2", "1/2", 4)` → `Fraction(15, 16)` |
| `infinite_geometric_series_sum(first, ratio)` | 无穷等比级数 | `infinite_geometric_series_sum("1/2", "1/2")` → `Fraction(1, 1)` |

### 工具函数

| 函数 | 描述 | 示例 |
|------|------|------|
| `is_proper_fraction(fraction)` | 真分数判断 | `is_proper_fraction("3/4")` → `True` |
| `is_unit_fraction(fraction)` | 单位分数判断 | `is_unit_fraction("1/4")` → `True` |
| `is_integer(fraction)` | 整数判断 | `is_integer("4/2")` → `True` |
| `denominator_count(fraction)` | 分母位数 | `denominator_count("1/100")` → `3` |
| `approximate(target, max_denom)` | 最佳近似 | `approximate(3.14159, 100)` → `Fraction(311, 99)` |

---

## 💡 使用示例

### 示例 1：分数计算器

```python
from mod import *

def calculate(expression: str) -> str:
    """简单的分数表达式计算器"""
    # 解析表达式 "1/2 + 1/3"
    parts = expression.split()
    f1 = parse_fraction(parts[0])
    op = parts[1]
    f2 = parse_fraction(parts[2])
    
    if op == '+':
        result = add(f1, f2)
    elif op == '-':
        result = subtract(f1, f2)
    elif op == '*':
        result = multiply(f1, f2)
    elif op == '/':
        result = divide(f1, f2)
    
    return to_string(result, 'mixed')

print(calculate("1/2 + 1/3"))  # 输出：5/6
print(calculate("3/4 * 2/3"))  # 输出：1/2
```

### 示例 2：烘焙配方缩放

```python
from mod import *

# 原始配方（4 人份）
recipe = {
    'flour': parse_fraction("2 1/2"),  # 2.5 杯
    'sugar': parse_fraction("3/4"),     # 0.75 杯
    'butter': parse_fraction("1/2"),    # 0.5 杯
}

# 缩放到 6 人份（乘以 1.5）
scale_factor = parse_fraction("3/2")

scaled_recipe = {
    ingredient: multiply(amount, scale_factor)
    for ingredient, amount in recipe.items()
}

for ingredient, amount in scaled_recipe.items():
    print(f"{ingredient}: {to_string(amount, 'mixed')}")
# 输出:
# flour: 3 3/4
# sugar: 1 1/8
# butter: 3/4
```

### 示例 3：数学作业 helper

```python
from mod import *

# 比较分数大小
fractions = ["3/4", "5/6", "7/8", "2/3"]
sorted_fracs = sorted(fractions, key=lambda x: parse_fraction(x))
print("从小到大:", [to_string(f) for f in sorted_fracs])

# 找公分母
print("公分母:", common_denominator(*fractions))

# 通分后比较
common = with_common_denominator(*fractions)
print("通分后:", [to_string(f) for f in common])

# 计算平均值
avg = average_fractions(fractions)
print("平均值:", to_string(avg, 'mixed'))
```

### 示例 4：级数求和

```python
from mod import *

# 计算 1 + 2 + 3 + ... + 100
sum_100 = arithmetic_series_sum(1, 1, 100)
print(f"1 到 100 的和：{sum_100}")  # 5050

# 计算等比级数 1/2 + 1/4 + 1/8 + ... (无穷)
infinite_sum = infinite_geometric_series_sum("1/2", "1/2")
print(f"无穷级数和：{infinite_sum}")  # 1

# 计算前 10 项和
finite_sum = geometric_series_sum("1/2", "1/2", 10)
print(f"前 10 项和：{to_string(finite_sum)}")  # 1023/1024
```

---

## 🧪 运行测试

```bash
cd AllToolkit/Python/fractions_utils
python fractions_utils_test.py
```

### 测试覆盖

- ✅ 创建和解析（15+ 测试）
- ✅ 算术运算（20+ 测试）
- ✅ 比较运算（15+ 测试）
- ✅ 简化和规范化（10+ 测试）
- ✅ 转换函数（10+ 测试）
- ✅ GCD/LCM 工具（10+ 测试）
- ✅ 批量操作（10+ 测试）
- ✅ 序列和级数（15+ 测试）
- ✅ 工具函数（10+ 测试）
- ✅ 边界情况和错误处理（10+ 测试）

**总计：120+ 测试用例**

---

## 📝 注意事项

### 输入格式

`parse_fraction` 支持多种输入格式：

```python
parse_fraction("3/4")      # 字符串分数
parse_fraction("1 1/2")    # 带分数（空格分隔）
parse_fraction("-1 1/2")   # 负带分数
parse_fraction(0.75)       # 浮点数
parse_fraction("0.75")     # 小数字符串
parse_fraction((3, 4))     # 元组 (分子，分母)
parse_fraction(3)          # 整数
parse_fraction(Fraction(3, 4))  # Fraction 对象
```

### 精度说明

- 所有内部计算使用 `Fraction` 类型，保持精确的有理数运算
- 转换为小数时可通过 `precision` 参数控制精度
- `from_decimal` 和 `approximate` 使用 `limit_denominator` 避免无限循环小数

### 错误处理

以下情况会抛出异常：

- `ZeroDivisionError`: 分母为零、除以零、零的倒数
- `ValueError`: 无法解析的输入、未知的格式类型、空参数列表

---

## 🤝 贡献

欢迎提交问题、建议或 Pull Request！

---

## 📄 许可证

MIT License - 详见 [LICENSE](../../LICENSE)

---

## 🔗 相关链接

- [Python fractions 文档](https://docs.python.org/3/library/fractions.html)
- [AllToolkit 主项目](../../README.md)
- [其他 Python 工具](../)
