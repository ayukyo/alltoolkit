# Roman Numeral Utils

罗马数字转换工具库，零外部依赖的纯 Python 实现。

## 功能特性

- **阿拉伯数字转罗马数字**: 将整数转换为标准罗马数字
- **罗马数字转阿拉伯数字**: 解析罗马数字字符串
- **输入验证**: 严格验证罗马数字格式
- **算术运算**: 支持加减乘除运算
- **回文查找**: 查找指定范围内的罗马数字回文
- **类接口**: 提供 `RomanNumeral` 类支持面向对象操作

## 安装

无需安装，直接复制 `mod.py` 文件到项目中使用。

## 快速开始

```python
from mod import to_roman, from_roman, RomanNumeral

# 阿拉伯数字 → 罗马数字
print(to_roman(1994))  # 输出: MCMXCIV
print(to_roman(2023))  # 输出: MMXXIII

# 罗马数字 → 阿拉伯数字
print(from_roman('XIV'))      # 输出: 14
print(from_roman('MCMXCIV'))  # 输出: 1994

# 使用 RomanNumeral 类
r = RomanNumeral(10)
print(r)           # 输出: X
print(r.arabic)   # 输出: 10
print(r.roman)    # 输出: X
```

## API 文档

### 基本函数

#### `to_roman(num: int, *, validate: bool = True) -> str`

将阿拉伯数字转换为罗马数字。

```python
to_roman(1)     # 'I'
to_roman(4)     # 'IV'
to_roman(9)     # 'IX'
to_roman(1994)  # 'MCMXCIV'
```

**参数:**
- `num`: 要转换的整数 (1-3999)
- `validate`: 是否验证范围 (默认 True)

**异常:**
- `OutOfRangeError`: 数字超出范围
- `TypeError`: 输入不是整数

---

#### `from_roman(roman: str, *, validate: bool = True) -> int`

将罗马数字转换为阿拉伯数字。

```python
from_roman('I')        # 1
from_roman('IV')       # 4
from_roman('MCMXCIV')  # 1994
```

**参数:**
- `roman`: 罗马数字字符串
- `validate`: 是否验证格式 (默认 True)

**异常:**
- `InvalidRomanNumeralError`: 无效的罗马数字
- `TypeError`: 输入不是字符串

---

#### `is_valid_roman(roman: str) -> bool`

检查字符串是否为有效的罗马数字。

```python
is_valid_roman('XIV')   # True
is_valid_roman('IIII')  # False (应为 IV)
is_valid_roman('ABC')   # False
```

---

### 算术运算

#### `roman_add(roman1: str, roman2: str) -> str`

两个罗马数字相加。

```python
roman_add('X', 'V')   # 'XV' (15)
roman_add('IX', 'I')  # 'X' (10)
```

---

#### `roman_subtract(roman1: str, roman2: str) -> str`

两个罗马数字相减。

```python
roman_subtract('X', 'V')  # 'V' (5)
roman_subtract('X', 'I')  # 'IX' (9)
```

---

#### `roman_multiply(roman1: str, roman2: str) -> str`

两个罗马数字相乘。

```python
roman_multiply('X', 'V')  # 'L' (50)
roman_multiply('IV', 'V') # 'XX' (20)
```

---

#### `roman_divide(roman1: str, roman2: str) -> Tuple[str, str]`

两个罗马数字相除，返回商和余数。

```python
roman_divide('X', 'III')  # ('III', 'I') - 商为3，余数为1
roman_divide('XX', 'V')   # ('IV', '')   - 商为4，无余数
```

---

### 辅助函数

#### `get_roman_info(num: int) -> dict`

获取数字的详细信息。

```python
get_roman_info(1994)
# 返回:
# {
#     'arabic': 1994,
#     'roman': 'MCMXCIV',
#     'components': [('M', 1000), ('CM', 900), ('XC', 90), ('IV', 4)]
# }
```

---

#### `find_roman_palindromes(start: int = 1, end: int = 3999) -> list`

查找指定范围内的罗马数字回文。

```python
find_roman_palindromes(1, 20)
# 返回: [(1, 'I'), (2, 'II'), (3, 'III'), (8, 'VIII'), (9, 'IX')]
```

---

### RomanNumeral 类

面向对象的罗马数字操作类。

```python
from mod import RomanNumeral

# 创建实例
r1 = RomanNumeral(10)    # 从整数创建
r2 = RomanNumeral('V')   # 从字符串创建

# 属性
print(r1.arabic)  # 10
print(r1.roman)    # 'X'

# 算术运算
r3 = r1 + r2       # RomanNumeral('XV', 15)
r4 = r1 - 5        # RomanNumeral('V', 5)
r5 = r1 * 2        # RomanNumeral('XX', 20)

# 比较
r1 == 10           # True
r1 == 'X'          # True
r1 > r2            # True

# 转换
int(r1)            # 10
str(r1)            # 'X'
```

---

## 罗马数字规则

### 基本符号

| 符号 | 数值 |
|------|------|
| I    | 1    |
| V    | 5    |
| X    | 10   |
| L    | 50   |
| C    | 100  |
| D    | 500  |
| M    | 1000 |

### 减法规则

当一个较小的符号出现在较大的符号前面时，需要减去：

| 组合 | 数值 |
|------|------|
| IV   | 4    |
| IX   | 9    |
| XL   | 40   |
| XC   | 90   |
| CD   | 400  |
| CM   | 900  |

### 限制

- 支持范围: 1-3999
- 同一符号最多连续出现3次 (I, X, C, M)
- V, L, D 不能重复
- 零无法用罗马数字表示

## 运行测试

```bash
python test_mod.py
```

或使用 pytest:

```bash
python -m pytest test_mod.py -v
```

## 示例输出

```
=== Roman Numeral Utils Demo ===

Arabic to Roman:
     1 → I
     4 → IV
     9 → IX
    14 → XIV
    49 → XLIX
    99 → XCIX
   444 → CDXLIV
   999 → CMXCIX
  1994 → MCMXCIV
  2023 → MMXXIII
  3999 → MMMCMXCIX

Roman to Arabic:
        I → 1
       IV → 4
       IX → 9
      XIV → 14
     XLIX → 49
     XCIX → 99
    CDXLIV → 444
    CMXCIX → 999
  MCMXCIV → 1994
  MMXXIII → 2023

Arithmetic:
  X + V = XV
  X - V = V
  X * V = L
  X / III = ('III', 'I')

✓ Demo complete!
```

## 许可证

MIT License

## 作者

AllToolkit - 2025