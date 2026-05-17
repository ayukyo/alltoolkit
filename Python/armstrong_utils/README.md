# Armstrong Number Utilities (阿姆斯特朗数与趣味数工具)

一个纯 Python 实现的趣味数检测和分析工具，零外部依赖。

## 功能特性

### 阿姆斯特朗数 (Armstrong Number)
- 也称为自恋数、自幂数、水仙花数
- 定义：一个 n 位数，其各位数字的 n 次方之和等于它本身
- 例如：153 = 1³ + 5³ + 3³ = 153

### 快乐数 (Happy Number)
- 定义：反复计算各位数字的平方和，最终达到 1 的数
- 例如：19 → 82 → 68 → 100 → 1

### 卡普雷卡尔数 (Kaprekar Number)
- 定义：一个数的平方可以分为两部分，使这两部分的和等于原数
- 例如：45² = 2025，20 + 25 = 45
- 卡普雷卡尔程序：4 位数通过降序减升序排列，最终达到 6174

### 完全数 (Perfect Number)
- 定义：一个数等于其所有真约数之和
- 例如：6 = 1 + 2 + 3，28 = 1 + 2 + 4 + 7 + 14
- 盈数和亏数检测

### 回文数 (Palindrome Number)
- 定义：正读和反读都相同的数
- 例如：121、12321
- Lychrel 数检测

### 其他趣味数
- Harshad 数（Niven 数）：能被其数位之和整除的数
- 数字根计算

## 安装

无需安装，直接导入使用：

```python
from mod import *
```

## 快速开始

### 阿姆斯特朗数

```python
from mod import is_armstrong, find_armstrong_numbers, get_armstrong_digits

# 检测是否为阿姆斯特朗数
print(is_armstrong(153))  # True
print(is_armstrong(154))  # False

# 获取位数、幂和、差值
print(get_armstrong_digits(153))  # (3, 153, 0)

# 查找范围内的阿姆斯特朗数
print(find_armstrong_numbers(10000))
# [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 153, 370, 371, 407, 1634, 8208, 9474]
```

### 快乐数

```python
from mod import is_happy, find_happy_numbers, get_happy_sequence

# 检测是否为快乐数
print(is_happy(19))  # True
print(is_happy(4))   # False

# 获取变换序列
print(get_happy_sequence(19))  # [19, 82, 68, 100, 1]

# 查找范围内的快乐数
print(find_happy_numbers(20))  # [1, 7, 10, 13, 19]
```

### 卡普雷卡尔数

```python
from mod import is_kaprekar, find_kaprekar_numbers, kaprekar_routine

# 检测是否为卡普雷卡尔数
print(is_kaprekar(45))  # True
print(is_kaprekar(10))  # False

# 查找范围内的卡普雷卡尔数
print(find_kaprekar_numbers(100))  # [1, 9, 45, 55, 99]

# 卡普雷卡尔程序（达到常数 6174）
sequence, reached = kaprekar_routine(3524)
print(sequence)  # [3524, 3087, 8352, 6174]
print(reached)   # True
```

### 完全数

```python
from mod import is_perfect, find_perfect_numbers, get_proper_divisors

# 检测是否为完全数
print(is_perfect(6))   # True
print(is_perfect(28))  # True

# 获取真约数
print(get_proper_divisors(28))  # [1, 2, 4, 7, 14]

# 查找范围内的完全数
print(find_perfect_numbers(10000))  # [6, 28, 496, 8128]
```

### 回文数

```python
from mod import is_palindrome, find_palindrome_numbers, reverse_number, is_lychrel

# 检测是否为回文数
print(is_palindrome(121))  # True
print(is_palindrome(123))  # False

# 数字反转
print(reverse_number(123))  # 321

# Lychrel 数检测
print(is_lychrel(196))  # True（已知的 Lychrel 数候选）
```

### 综合分析

```python
from mod import analyze_number, find_special_numbers

# 分析单个数的各种趣味数属性
result = analyze_number(153)
print(result)
# {
#   'number': 153,
#   'is_armstrong': True,
#   'is_happy': False,
#   'is_kaprekar': False,
#   'is_perfect': False,
#   'is_palindrome': False,
#   ...
# }

# 查找范围内的特殊数
result = find_special_numbers(100)
print(result['armstrong'])  # 阿姆斯特朗数
print(result['happy'])       # 快乐数
print(result['perfect'])    # 完全数
```

## API 参考

### 阿姆斯特朗数
- `is_armstrong(number)` - 检测是否为阿姆斯特朗数
- `get_armstrong_digits(number)` - 获取位数、幂和、差值
- `find_armstrong_numbers(limit)` - 查找范围内的阿姆斯特朗数
- `generate_armstrong_numbers()` - 生成器，生成所有阿姆斯特朗数
- `get_next_armstrong(number)` - 获取下一个阿姆斯特朗数
- `count_armstrong_digits(number)` - 计算数字位数
- `is_narcissistic(number)` - is_armstrong 的别名
- `is_pluperfect(number)` - is_armstrong 的别名

### 快乐数
- `is_happy(number)` - 检测是否为快乐数
- `get_happy_sequence(number)` - 获取变换序列
- `find_happy_numbers(limit)` - 查找范围内的快乐数
- `sum_of_squares_of_digits(number)` - 计算各位数字的平方和

### 卡普雷卡尔数
- `is_kaprekar(number)` - 检测是否为卡普雷卡尔数
- `find_kaprekar_numbers(limit)` - 查找范围内的卡普雷卡尔数
- `kaprekar_routine(number, max_iterations)` - 执行卡普雷卡尔程序

### 完全数
- `is_perfect(number)` - 检测是否为完全数
- `find_perfect_numbers(limit)` - 查找范围内的完全数
- `get_proper_divisors(number)` - 获取真约数
- `is_abundant(number)` - 检测是否为盈数
- `is_deficient(number)` - 检测是否为亏数

### 回文数
- `is_palindrome(number)` - 检测是否为回文数
- `find_palindrome_numbers(limit)` - 查找范围内的回文数
- `reverse_number(number)` - 反转数字
- `is_lychrel(number, max_iterations)` - 检测是否为 Lychrel 数
- `get_lychrel_sequence(number, max_iterations)` - 获取 Lychrel 变换序列

### 其他
- `is_harshad(number)` - 检测是否为 Harshad 数
- `find_harshad_numbers(limit)` - 查找范围内的 Harshad 数
- `digital_root(number)` - 计算数字根
- `analyze_number(number)` - 综合分析一个数
- `find_special_numbers(limit, number_type)` - 查找特殊数

## 数学背景

### 阿姆斯特朗数
阿姆斯特朗数只有有限的 88 个。最大的阿姆斯特朗数是一个 39 位数：
115132219018763992565095597973971522401

### 完全数
目前已知的完全数都是偶数，且与梅森素数有关。每个形如 2^(p-1) × (2^p - 1) 的数（其中 2^p - 1 是梅森素数）都是完全数。

### 卡普雷卡尔常数
对于 4 位数（各位不全相同），通过"降序减升序"的操作，最多 7 步就能达到 6174。

### Lychrel 数
196 是最著名的 Lychrel 数候选，至今尚未证明它能形成回文数。

## 测试

```bash
python -m pytest armstrong_utils_test.py -v
```

## 许可证

MIT License