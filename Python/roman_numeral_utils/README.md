# Roman Numeral Utils - 罗马数字转换工具

一个完整的 Python 罗马数字转换工具，提供阿拉伯数字与罗马数字之间的相互转换、验证和运算功能。

## 功能特性

- ✅ **基本转换**：阿拉伯数字 ↔ 罗马数字双向转换
- ✅ **输入验证**：完整的罗马数字格式验证
- ✅ **算术运算**：支持加减乘除四则运算
- ✅ **比较功能**：罗马数字大小比较
- ✅ **信息查询**：获取罗马数字详细信息
- ✅ **范围生成**：批量生成指定范围的罗马数字
- ✅ **扩展支持**：支持上划线表示法处理大于 3999 的数字

## 安装

```python
# 无需外部依赖，直接导入使用
from mod import int_to_roman, roman_to_int
```

## 快速开始

### 基本转换

```python
from mod import int_to_roman, roman_to_int

# 阿拉伯数字 → 罗马数字
print(int_to_roman(2024))  # 输出: MMXXIV
print(int_to_roman(4))     # 输出: IV
print(int_to_roman(3999))  # 输出: MMMCMXCIX

# 罗马数字 → 阿拉伯数字
print(roman_to_int('MMXXIV'))  # 输出: 2024
print(roman_to_int('IV'))      # 输出: 4
print(roman_to_int('MCMLXXXIV'))  # 输出: 1984
```

### 验证功能

```python
from mod import is_valid_roman

print(is_valid_roman('IV'))     # True - 有效
print(is_valid_roman('IIII'))   # False - 无效（应该是IV）
print(is_valid_roman('MMXXIV')) # True - 有效
print(is_valid_roman('ABC'))    # False - 无效字符
```

### 算术运算

```python
from mod import roman_add, roman_subtract, roman_multiply, roman_divide

# 加法
print(roman_add('X', 'V'))      # 输出: XV (10 + 5 = 15)
print(roman_add('IV', 'VI'))    # 输出: X (4 + 6 = 10)

# 减法
print(roman_subtract('X', 'V'))  # 输出: V (10 - 5 = 5)
print(roman_subtract('X', 'I'))  # 输出: IX (10 - 1 = 9)

# 乘法
print(roman_multiply('V', 'II'))  # 输出: X (5 × 2 = 10)
print(roman_multiply('X', 'X'))   # 输出: C (10 × 10 = 100)

# 除法（返回商和余数）
print(roman_divide('X', 'III'))  # 输出: ('III', 'I') (10 ÷ 3 = 3 余 1)
print(roman_divide('X', 'II'))   # 输出: ('V', '') (10 ÷ 2 = 5 余 0)
```

### 比较功能

```python
from mod import roman_compare

print(roman_compare('V', 'X'))   # -1 (V < X)
print(roman_compare('X', 'V'))   # 1 (X > V)
print(roman_compare('X', 'X'))   # 0 (X = X)
```

### 获取详细信息

```python
from mod import get_roman_info

info = get_roman_info('MMXXIV')
print(info)
# {
#     'original': 'MMXXIV',
#     'value': 2024,
#     'valid': True,
#     'length': 6,
#     'components': ['M', 'M', 'X', 'X', 'IV'],
#     'digit_count': 4
# }
```

### 批量生成

```python
from mod import find_roman_range

# 生成1到10的罗马数字
for value, roman in find_roman_range(1, 10):
    print(f"{value}: {roman}")
# 输出:
# 1: I
# 2: II
# 3: III
# 4: IV
# 5: V
# ...
```

### 扩展模式（大于3999的数字）

```python
# 标准模式最大支持3999
# int_to_roman(4000)  # 抛出 OutOfRangeError

# 使用上划线表示法
print(int_to_roman(5000, use_overline=True))  # V̄ (V加上划线表示5000)
print(int_to_roman(10000, use_overline=True)) # X̄
```

## API 参考

### `int_to_roman(num: int, use_overline: bool = False) -> str`

将阿拉伯数字转换为罗马数字。

**参数:**
- `num`: 要转换的整数（标准模式: 1-3999）
- `use_overline`: 是否使用上划线表示法

**返回:** 罗马数字字符串

**异常:**
- `OutOfRangeError`: 数字超出范围
- `TypeError`: 输入不是整数

### `roman_to_int(roman: str) -> int`

将罗马数字转换为阿拉伯数字。

**参数:**
- `roman`: 罗马数字字符串

**返回:** 对应的整数

**异常:**
- `InvalidRomanError`: 输入不是有效的罗马数字
- `TypeError`: 输入不是字符串

### `is_valid_roman(roman: str) -> bool`

验证字符串是否为有效的罗马数字。

### `roman_add(roman1: str, roman2: str) -> str`
### `roman_subtract(roman1: str, roman2: str) -> str`
### `roman_multiply(roman1: str, roman2: str) -> str`
### `roman_divide(roman1: str, roman2: str) -> Tuple[str, str]`

罗马数字算术运算。

### `roman_compare(roman1: str, roman2: str) -> int`

比较两个罗马数字。返回 -1/0/1。

### `get_roman_info(roman: str) -> dict`

获取罗马数字的详细信息。

### `find_roman_range(start: int, end: int) -> list`

生成指定范围内的所有罗马数字。

### `search_by_value(value: int) -> Optional[str]`

根据整数值搜索对应的罗马数字。

## 罗马数字规则

本工具遵循标准罗马数字规则：

1. **基本符号**:
   - I = 1, V = 5, X = 10, L = 50
   - C = 100, D = 500, M = 1000

2. **减法原则**:
   - IV = 4, IX = 9, XL = 40, XC = 90
   - CD = 400, CM = 900

3. **重复规则**:
   - I, X, C, M 可以重复最多3次
   - V, L, D 不能重复

4. **标准范围**: 1 到 3999

## 运行测试

```bash
python roman_numeral_utils_test.py
```

## 常见问题

**Q: 为什么最大只支持3999？**
A: 标准罗马数字没有表示5000以上的专用符号。可以使用上划线表示法（use_overline=True）处理更大数字。

**Q: 为什么 IIII 不是有效的罗马数字？**
A: 根据罗马数字规则，4 应该写作 IV（减法原则），而不是 IIII。

**Q: 大小写敏感吗？**
A: 不敏感，`iv`、`IV`、`iV` 都会被识别为有效的罗马数字。

## 许可证

MIT License

## 作者

AllToolkit 自动生成