# Number Words Utils

数字与文字转换工具模块，支持数字转文字、文字转数字、多语言支持（英语/中文）、序数转换、货币格式等。

## 功能特性

- **数字转文字**: `123` → `"one hundred twenty-three"`
- **文字转数字**: `"one hundred twenty-three"` → `123`
- **多语言支持**: 英语 (EN) 和中文 (ZH)
- **序数转换**: `1` → `"first"`, `21` → `"twenty-first"`
- **货币格式**: `$123.45` → `"one hundred twenty-three dollars and forty-five cents"`
- **小数支持**: `123.45` → `"one hundred twenty-three point four five"`
- **负数处理**: `-42` → `"minus forty-two"`
- **大数支持**: 支持到千万亿 (quintillion, 10^18)

## 安装

```python
from number_words_utils.mod import number_to_words, words_to_number, Language
```

## 快速开始

### 数字转文字

```python
from number_words_utils.mod import number_to_words, Language

# 英语
number_to_words(123)  # "one hundred twenty-three"
number_to_words(1000000)  # "one million"
number_to_words(123.45)  # "one hundred twenty-three point four five"

# 中文
number_to_words(123, Language.CHINESE)  # "一百二十三"
number_to_words(10000, Language.CHINESE)  # "一万"

# 序数
number_to_words(1, ordinal=True)  # "first"
number_to_words(21, ordinal=True)  # "twenty-first"
number_to_words(100, Language.CHINESE, ordinal=True)  # "第一百"
```

### 文字转数字

```python
from number_words_utils.mod import words_to_number, Language

# 英语
words_to_number("one hundred twenty-three")  # 123
words_to_number("two million three hundred thousand")  # 2300000
words_to_number("one point five")  # 1.5

# 中文
words_to_number("一百二十三", Language.CHINESE)  # 123
words_to_number("一万二千三百四十五", Language.CHINESE)  # 12345

# 序数
words_to_number("first")  # 1
words_to_number("第十", Language.CHINESE)  # 10
```

### 货币格式

```python
from number_words_utils.mod import number_to_currency_words, Language

# 英语货币
number_to_currency_words(123.45, "USD")  # "one hundred twenty-three dollars and forty-five cents"
number_to_currency_words(100, "EUR")  # "one hundred euros"

# 中文货币
number_to_currency_words(123.45, "CNY", Language.CHINESE)  # "一百二十三元四十五分"
```

### 工具函数

```python
from number_words_utils.mod import is_valid_number_word, get_number_words_list, Language

# 检查是否为有效数字词
is_valid_number_word("hundred")  # True
is_valid_number_word("hello")  # False

# 获取所有数字词列表
words = get_number_words_list(Language.ENGLISH)
# ['and', 'billion', 'eight', 'eighteen', 'eighty', ...]
```

## API 参考

### `number_to_words(number, language=Language.ENGLISH, ordinal=False)`

将数字转换为文字。

**参数:**
- `number` (int | float): 要转换的数字
- `language` (Language | str): 目标语言 ("en" 或 "zh")
- `ordinal` (bool): 是否返回序数形式

**返回:** str

### `words_to_number(words, language=Language.ENGLISH)`

将文字转换为数字。

**参数:**
- `words` (str): 数字词表示
- `language` (Language | str): 源语言

**返回:** int | float

### `number_to_currency_words(amount, currency="USD", language=Language.ENGLISH)`

将货币金额转换为文字。

**参数:**
- `amount` (int | float): 货币金额
- `currency` (str): 货币代码 ("USD", "EUR", "GBP", "CNY", "JPY")
- `language` (Language | str): 目标语言

**返回:** str

## 支持的语言

| 语言 | 代码 | 示例 |
|------|------|------|
| 英语 | `Language.ENGLISH` 或 `"en"` | `one hundred twenty-three` |
| 中文 | `Language.CHINESE` 或 `"zh"` | `一百二十三` |

## 支持的货币

| 货币 | 代码 | 英语形式 | 中文形式 |
|------|------|----------|----------|
| 美元 | USD | dollars/cents | 美元/美分 |
| 欧元 | EUR | euros/cents | 欧元/欧分 |
| 英镑 | GBP | pounds/pence | 英镑/便士 |
| 人民币 | CNY | yuan/fen | 元/分 |
| 日元 | JPY | yen/sen | 日元/钱 |

## 零外部依赖

本模块完全使用 Python 标准库实现，无需安装任何外部依赖。

## 许可证

MIT License