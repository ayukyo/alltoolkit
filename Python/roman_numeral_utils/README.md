# Roman Numeral Utils

罗马数字转换工具 - 零依赖，生产就绪

## 功能特性

- ✅ **基础转换**: 阿拉伯数字 ↔ 罗马数字
- ✅ **智能识别**: 自动判断输入类型
- ✅ **格式验证**: 严格/宽松两种验证模式
- ✅ **批量操作**: 批量转换，跳过无效值
- ✅ **算术运算**: 加减乘除、比较
- ✅ **文本搜索**: 从文本中提取罗马数字
- ✅ **规范化**: 非标准形式转标准形式
- ✅ **详细解释**: 分解罗马数字的构成

## 支持范围

- 最小值: 1 (I)
- 最大值: 3999 (MMMCMXCIX)

## 快速开始

```python
from roman_numeral_utils.mod import to_roman, from_roman, convert

# 阿拉伯数字转罗马数字
print(to_roman(2024))  # 'MMXXIV'
print(to_roman(1999))  # 'MCMXCIX'

# 罗马数字转阿拉伯数字
print(from_roman('XIV'))  # 14
print(from_roman('MMMCMXCIX'))  # 3999

# 智能转换
print(convert(10))      # 'X'
print(convert('X'))      # 10
```

## API 文档

### 核心函数

#### `to_roman(num: int, strict: bool = True) -> str`

将阿拉伯数字转换为罗马数字。

```python
to_roman(1)      # 'I'
to_roman(4)      # 'IV'
to_roman(2024)   # 'MMXXIV'
```

#### `from_roman(roman: str, strict: bool = True) -> int`

将罗马数字转换为阿拉伯数字。

```python
from_roman('I')       # 1
from_roman('IV')      # 4
from_roman('MMXXIV')  # 2024
```

#### `convert(value: Union[int, str], strict: bool = True) -> Union[str, int]`

智能转换，自动识别输入类型。

```python
convert(10)     # 'X'
convert('X')    # 10
```

### 验证函数

#### `is_valid_roman(roman: str) -> bool`

严格验证罗马数字格式。

```python
is_valid_roman('IV')    # True
is_valid_roman('IIII')  # False (4个I不标准)
is_valid_roman('VX')    # False (V不能被X减)
```

#### `is_roman_numeral(text: str) -> bool`

宽松检查，判断是否可能为罗马数字。

```python
is_roman_numeral('IIII')  # True (只检查字符)
is_roman_numeral('ABC')   # False
```

### 批量操作

#### `batch_to_roman(numbers: List[int], ...) -> List[Tuple[int, str, str]]`

批量转换阿拉伯数字到罗马数字。

```python
results = batch_to_roman([1, 2, 3])
# [(1, 'I', None), (2, 'II', None), (3, 'III', None)]
```

#### `batch_from_roman(romans: List[str], ...) -> List[Tuple[str, int, str]]`

批量转换罗马数字到阿拉伯数字。

```python
results = batch_from_roman(['I', 'II', 'III'])
# [('I', 1, None), ('II', 2, None), ('III', 3, None)]
```

#### `get_roman_range(start: int, end: int) -> List[Tuple[int, str]]`

生成范围内的罗马数字列表。

```python
get_roman_range(1, 5)
# [(1, 'I'), (2, 'II'), (3, 'III'), (4, 'IV'), (5, 'V')]
```

### 算术运算

```python
add_roman('X', 'V')       # 'XV' (10+5=15)
subtract_roman('X', 'V')   # 'V' (10-5=5)
multiply_roman('X', 'X')   # 'C' (10*10=100)
divide_roman('X', 'II')    # 'V' (10/2=5)

# 带余数的除法
q, r = divide_roman('X', 'III', remainder=True)
# q='III' (商3), r='I' (余1)

# 比较
compare_roman('X', 'V')   # 5 (正数=大于)
compare_roman('V', 'X')    # -5 (负数=小于)
compare_roman('X', 'X')   # 0 (相等)
```

### 工具函数

#### `find_roman_in_text(text: str) -> List[Tuple[str, int, int]]`

从文本中提取罗马数字。

```python
find_roman_in_text("Chapter XIV and Chapter XIII")
# [('XIV', 8, 11), ('XIII', 25, 28)]
```

#### `normalize_roman(roman: str) -> str`

规范化为标准形式。

```python
normalize_roman('iiii')   # 'IV'
normalize_roman('viiii')  # 'IX'
```

#### `roman_to_ordinal(roman: str) -> str`

转换为英文序数词。

```python
roman_to_ordinal('I')    # '1st'
roman_to_ordinal('II')   # '2nd'
roman_to_ordinal('III')  # '3rd'
roman_to_ordinal('IV')   # '4th'
```

#### `explain_roman(roman: str) -> List[Tuple[str, int, str]]`

解释罗马数字的构成。

```python
explain_roman('XIV')
# [('X', 10, '加'), ('IV', 4, '减法组合'), ('总计', 14, '')]
```

## 异常处理

```python
from roman_numeral_utils.mod import (
    to_roman, from_roman,
    InvalidRomanError, OutOfRangeError
)

# 超出范围
try:
    to_roman(0)      # ValueError
    to_roman(4000)   # ValueError
except OutOfRangeError as e:
    print(e)

# 无效格式
try:
    from_roman('ABC')   # InvalidRomanError
    from_roman('IIII')   # InvalidRomanError (严格模式)
except InvalidRomanError as e:
    print(e)
```

## 运行测试

```bash
python Python/roman_numeral_utils/roman_numeral_utils_test.py
```

## 运行示例

```bash
python Python/roman_numeral_utils/examples/usage_examples.py
```

## 许可证

MIT License

---

**Author**: AllToolkit  
**Created**: 2026-04-14