# ordinal_utils - 序数词工具

[![Test Coverage](https://img.shields.io/badge/coverage-100%25-brightgreen)](./ordinal_utils_test.py)

零依赖的序数词（1st, 2nd, 3rd 等）处理工具，支持多语言。

## 特性

- **基数转序数**: 1 → 1st, 2 → 2nd, 3 → 3rd
- **序数转基数**: "1st" → 1, "第3" → 3
- **序数词形式**: 1 → "first", 21 → "twenty-first"
- **多语言支持**: 英语、中文、法语、德语、西班牙语等 10+ 语言
- **罗马数字**: 支持 I, II, III 等罗马数字格式
- **日期格式化**: 带序数词的日期格式
- **排名显示**: 支持奖牌（🥇🥈🥉）和排名格式
- **零依赖**: 纯 Python 实现

## 安装

```python
from ordinal_utils import (
    to_ordinal,
    from_ordinal,
    to_ordinal_word,
    ordinal_to_roman,
    roman_to_ordinal,
    get_all_ordinal_forms,
    format_date_with_ordinal,
    format_ranking
)
```

## 快速开始

### 基础用法

```python
from ordinal_utils import to_ordinal, from_ordinal

# 转换为序数词
print(to_ordinal(1))    # "1st"
print(to_ordinal(2))    # "2nd"
print(to_ordinal(3))    # "3rd"
print(to_ordinal(11))   # "11th" (特殊规则)
print(to_ordinal(21))   # "21st"
print(to_ordinal(100))  # "100th"

# 解析序数词
print(from_ordinal("1st"))   # 1
print(from_ordinal("22nd"))  # 22
print(from_ordinal("第3"))   # 3 (中文)
print(from_ordinal("5."))    # 5 (德语格式)
```

### 序数词形式（单词）

```python
from ordinal_utils import to_ordinal_word

print(to_ordinal_word(1))    # "first"
print(to_ordinal_word(2))    # "second"
print(to_ordinal_word(21))   # "twenty-first"
print(to_ordinal_word(100))  # "hundredth"
```

### 多语言支持

```python
from ordinal_utils import to_ordinal, get_all_ordinal_forms

# 单语言转换
print(to_ordinal(5, language="fr"))  # "5e" (法语)
print(to_ordinal(5, language="de"))  # "5." (德语)
print(to_ordinal(5, language="zh"))  # "第5" (中文)
print(to_ordinal(5, language="ja"))  # "5番目" (日语)

# 获取所有语言形式
forms = get_all_ordinal_forms(5)
print(forms)  # {"en": "5th", "fr": "5e", "de": "5.", "zh": "第5", ...}
```

### 罗马数字

```python
from ordinal_utils import ordinal_to_roman, roman_to_ordinal

print(ordinal_to_roman(1))     # "I"
print(ordinal_to_roman(4))     # "IV"
print(ordinal_to_roman(2024))  # "MMXXIV"

print(roman_to_ordinal("IV"))   # 4
print(roman_to_ordinal("X"))    # 10
```

### 日期格式化

```python
from ordinal_utils import format_date_with_ordinal

print(format_date_with_ordinal(1, "January", 2026))
# "January 1st, 2026"

print(format_date_with_ordinal(22, "March", 2026, format_type="dmy"))
# "22nd March 2026"

print(format_date_with_ordinal(3, 5, 2026))  # 使用月份数字
# "May 3rd, 2026"
```

### 排名显示

```python
from ordinal_utils import format_ranking, get_rank_suffix

# 前三名使用奖牌符号
print(format_ranking(1, "Team Alpha", 100))  # "🥇 Team Alpha (100)"
print(format_ranking(2, "Team Beta", 95))    # "🥈 Team Beta (95)"
print(format_ranking(3, "Team Gamma", 90))   # "🥉 Team Gamma (90)"

# 其他排名使用序数词
print(format_ranking(4, "Team Delta", 85))   # "4th Team Delta (85)"
```

### 序数范围

```python
from ordinal_utils import ordinal_range

print(ordinal_range(1, 5))
# ['1st', '2nd', '3rd', '4th', '5th']

print(ordinal_range(1, 3, language="fr"))
# ['1er', '2e', '3e']
```

## API 参考

### 主要函数

| 函数 | 说明 |
|-----|------|
| `to_ordinal(n, language, gender)` | 转换为序数词字符串 |
| `from_ordinal(ordinal_str, language)` | 解析序数词为数字 |
| `to_ordinal_word(n, language, gender)` | 转换为序数词单词 |
| `is_ordinal(s, language)` | 检查是否为有效序数词 |
| `get_ordinal_suffix(n, language)` | 获取序数词后缀 |
| `get_all_ordinal_forms(n, gender)` | 获取所有语言的序数词形式 |

### 罗马数字函数

| 函数 | 说明 |
|-----|------|
| `ordinal_to_roman(n)` | 转换为罗马数字 |
| `roman_to_ordinal(roman)` | 解析罗马数字 |

### 日期和排名函数

| 函数 | 说明 |
|-----|------|
| `format_date_with_ordinal(day, month, year, ...)` | 格式化带序数的日期 |
| `get_rank_suffix(rank)` | 获取排名后缀（奖牌或序数词） |
| `format_ranking(rank, name, score)` | 格式化排名显示 |
| `ordinal_range(start, end, language)` | 生成序数词范围 |

### 比较函数

| 函数 | 说明 |
|-----|------|
| `compare_ordinals(ord1, ord2)` | 比较两个序数词 |

## 支持的语言

| 语言 | 代码 | 格式示例 |
|------|------|---------|
| English | en | 1st, 2nd, 3rd, 4th |
| Chinese | zh | 第1, 第2, 第3 |
| Japanese | ja | 1番目, 2番目 |
| French | fr | 1er, 2e, 3e |
| German | de | 1., 2., 3. |
| Spanish | es | 1o, 2o, 3o (支持性别) |
| Italian | it | 1o, 1a (支持性别) |
| Portuguese | pt | 1o, 1a (支持性别) |
| Dutch | nl | 1e, 2e, 3e |
| Russian | ru | 1-й, 2-й |

## 测试

```bash
python -m pytest ordinal_utils_test.py -v
```

## 许可证

MIT License