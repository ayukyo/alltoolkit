# Roman Numeral Utils

零外部依赖的罗马数字转换工具，支持完整的罗马数字与阿拉伯数字之间的双向转换及各种运算操作。

## 功能特性

- ✅ **阿拉伯数字转罗马数字** (1-3999 标准范围)
- ✅ **罗马数字转阿拉伯数字**
- ✅ **扩展支持** (使用括号表示上划线，支持到 3,999,999)
- ✅ **罗马数字验证**
- ✅ **算术运算** (加减乘除、取模、幂运算)
- ✅ **比较和排序**
- ✅ **链式构建器 API**
- ✅ **零外部依赖** - 纯 Python 实现

## 快速开始

### 基本转换

```python
from mod import to_roman, from_roman

# 阿拉伯数字 → 罗马数字
print(to_roman(1994))  # 'MCMXCIV'
print(to_roman(2023))  # 'MMXXIII'

# 罗马数字 → 阿拉伯数字
print(from_roman('MCMXCIV'))  # 1994
print(from_roman('MMXXIII'))  # 2023
```

### 验证

```python
from mod import is_valid_roman, validate_roman

# 快速验证
print(is_valid_roman('MCMXCIV'))  # True
print(is_valid_roman('IIII'))      # False (应该是 IV)

# 详细验证
valid, msg = validate_roman('ABC')
print(valid)  # False
print(msg)    # 'Invalid character in roman numeral: ABC'
```

### RomanNumeral 类

```python
from mod import RomanNumeral

r1 = RomanNumeral(10)   # X
r2 = RomanNumeral('V')  # V

# 算术运算
print(r1 + r2)   # XV (15)
print(r1 - r2)   # V (5)
print(r1 * r2)   # L (50)
print(r1 / r2)   # II (2)

# 与整数运算
print(r1 + 5)    # XV (15)

# 比较
print(r1 > r2)   # True
print(r1 == 10)  # True
print(r1 == 'X') # True
```

### 链式构建器

```python
from mod import RomanNumeralBuilder

result = (RomanNumeralBuilder()
          .add(10)        # 加 10
          .add('V')       # 加 5
          .multiply(2)    # 乘以 2
          .build())
print(result)  # XXX (30)
```

### 扩展罗马数字 (大数支持)

```python
from mod import to_roman, from_roman

# 标准范围: 1-3999
# 扩展范围: 1-3999999 (使用括号表示上划线)

print(to_roman(4000, extended=True))   # '(IV)'
print(to_roman(10000, extended=True))  # '(X)'
print(to_roman(100000, extended=True))  # '(C)'

print(from_roman('(IV)', extended=True))  # 4000
```

### 排序和范围

```python
from mod import roman_sort, roman_range

# 排序
print(roman_sort(['III', 'I', 'II', 'V', 'IV']))
# ['I', 'II', 'III', 'IV', 'V']

# 生成范围
print(roman_range(1, 5))
# ['I', 'II', 'III', 'IV', 'V']
```

### 求和

```python
from mod import roman_sum

print(roman_sum(['X', 'V', 'I']))  # 'XVI' (16)
```

## API 参考

### 函数

| 函数 | 描述 |
|------|------|
| `to_roman(num, extended=False)` | 阿拉伯数字转罗马数字 |
| `from_roman(roman, extended=False)` | 罗马数字转阿拉伯数字 |
| `is_valid_roman(roman, extended=False)` | 验证罗马数字格式 |
| `validate_roman(roman, extended=False)` | 详细验证，返回 (是否有效, 信息) |
| `roman_sort(romans, reverse=False, extended=False)` | 罗马数字排序 |
| `roman_range(start, end, step=1, extended=False)` | 生成罗马数字范围 |
| `roman_sum(romans, extended=False)` | 计算罗马数字和 |
| `roman(roman, extended=False)` | 便捷函数，创建 RomanNumeral |

### 类

#### RomanNumeral

罗马数字对象，支持完整的算术运算和比较操作。

```python
r = RomanNumeral(10)  # 或 RomanNumeral('X')
r.arabic  # 10 (阿拉伯数字表示)
r.roman   # 'X' (罗马数字表示)
```

#### RomanNumeralBuilder

链式构建器，支持累加操作。

```python
builder = RomanNumeralBuilder()
result = builder.from_int(10).add(5).multiply(2).build()
```

### 异常

- `RomanNumeralError`: 基础异常类
- `InvalidRomanNumeralError`: 无效的罗马数字格式
- `OutOfRangeError`: 数值超出范围

## 运行测试

```bash
cd Python/roman_numeral_utils
python -m pytest test_mod.py -v
```

## 运行示例

```bash
cd Python/roman_numeral_utils
python examples.py
```

## 罗马数字参考

| 阿拉伯数字 | 罗马数字 | 阿拉伯数字 | 罗马数字 |
|-----------|---------|-----------|---------|
| 1 | I | 50 | L |
| 5 | V | 100 | C |
| 10 | X | 500 | D |
| 4 | IV | 1000 | M |
| 9 | IX | 4000* | (IV) |

*扩展表示法，使用括号表示上划线

## 许可证

MIT License