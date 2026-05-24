# name_parser_utils - 人名解析工具

将人名解析为组成部分：姓名、中间名、姓氏、前缀、后缀等。支持多种格式和中英文名称。

## 功能特性

- 🔤 **西方名称解析**: 支持解析英文名称，自动识别名、中间名、姓
- 🇨🇳 **中文名称解析**: 支持解析中文姓名，自动识别姓氏（包括复姓）
- 🔀 **混合名称解析**: 支持解析中英文混合名称
- 🏷️ **前缀后缀识别**: 自动识别 Mr., Dr., Jr., PhD 等前缀后缀
- 💬 **昵称提取**: 自动提取引号内的昵称
- 📝 **多种格式输出**: 支持西方格式、中文格式、姓在先格式、首字母格式
- ⚖️ **名称比较**: 比较两个名称是否可能属于同一人
- 🔤 **首字母提取**: 从名称中提取首字母

## 安装

```python
from name_parser_utils.mod import NameParser, parse_name
```

## 快速开始

### 基础使用

```python
from mod import parse_name

# 解析英文名
result = parse_name("John William Doe")
print(result.first_name)   # "John"
print(result.middle_name)  # "William"
print(result.last_name)    # "Doe"

# 解析中文名
result = parse_name("张三")
print(result.chinese_surname)    # "张"
print(result.chinese_given_name) # "三"

# 解析复姓
result = parse_name("欧阳锋")
print(result.chinese_surname)    # "欧阳"
print(result.chinese_given_name) # "锋"

# 解析带前缀后缀的名称
result = parse_name("Dr. Jane Smith PhD")
print(result.prefix)     # "Dr."
print(result.first_name) # "Jane"
print(result.last_name)  # "Smith"
print(result.suffix)      # "PHD"
```

### 批量解析

```python
from mod import parse_names

names = ["John Doe", "Jane Smith", "张三"]
results = parse_names(names)

for result in results:
    print(result.full_name())
```

### 格式化输出

```python
from mod import NameParser

parser = NameParser()
result = parser.parse("John William Doe")

# 不同格式
print(parser.format_name(result, "western"))      # "John William Doe"
print(parser.format_name(result, "last_first"))   # "Doe, John William"
print(parser.format_name(result, "initials"))     # "JWD"

# 带前缀后缀
result = parser.parse("Dr. Jane Smith PhD")
print(parser.format_name(result, "western", include_prefix=True, include_suffix=True))
# "Dr. Jane Smith PhD"
```

### 名称比较

```python
from mod import compare_names

# 比较两个名称
match, score = compare_names("John Doe", "John Doe")
print(match)  # True
print(score)   # 1.0

match, score = compare_names("John Doe", "Jane Doe")
print(match)  # False
```

### 首字母提取

```python
from mod import get_initials

initials = get_initials("John William Doe")
print(initials)  # "JD"

initials = get_initials("John William Doe", include_middle=True)
print(initials)  # "JWD"
```

## API 参考

### ParsedName

解析后的人名数据类。

| 属性 | 类型 | 说明 |
|------|------|------|
| `first_name` | str | 名/名字 |
| `middle_name` | str | 中间名 |
| `last_name` | str | 姓/姓氏 |
| `prefix` | str | 前缀 (Mr., Dr. 等) |
| `suffix` | str | 后缀 (Jr., PhD 等) |
| `chinese_surname` | str | 中文姓 |
| `chinese_given_name` | str | 中文名 |
| `nickname` | str | 昵称 |
| `original` | str | 原始输入 |
| `format_type` | str | 格式类型 |

### NameParser

人名解析器类。

#### 方法

| 方法 | 说明 |
|------|------|
| `parse(name)` | 解析人名，返回 ParsedName |
| `parse_list(names)` | 批量解析人名 |
| `format_name(parsed, format_style, ...)` | 格式化解析后的名称 |
| `compare_names(name1, name2)` | 比较两个名称 |
| `get_initials(name, include_middle)` | 获取首字母 |

### 便捷函数

| 函数 | 说明 |
|------|------|
| `parse_name(name)` | 解析人名 |
| `parse_names(names)` | 批量解析人名 |
| `format_name(name, format_style, ...)` | 格式化人名 |
| `compare_names(name1, name2)` | 比较两个名称 |
| `get_initials(name, include_middle)` | 获取首字母 |

## 支持的前缀

- 英文: Mr., Mrs., Ms., Miss, Dr., Prof., Rev., Hon., Sir, Lord, Lady 等
- 中文拼音: 先生(xiansheng), 女士(nvshi), 太太(taitai), 小姐(xiaojie) 等

## 支持的后缀

- 称号: Jr., Sr., II, III, IV, V
- 学位: PhD, MD, DDS, DVM, Esq.

## 支持的中文复姓

欧阳、司马、上官、诸葛、东方、皇甫、尉迟、公孙、慕容 等 100+ 复姓。

## 测试

```bash
python name_parser_utils_test.py
```

## 许可证

MIT License