# Unicode Lookup Utils 🔤

Unicode 字符查询工具模块，提供字符信息查找、分类、搜索等功能。

## 特性

- ✅ **字符信息查询** - 通过字符或码点获取 Unicode 名称、分类、区块
- ✅ **名称搜索** - 按关键词搜索 Unicode 字符
- ✅ **分类检测** - 字母、数字、符号、标点等检测
- ✅ **编码信息** - UTF-8/UTF-16/HTML 实体编码
- ✅ **字符宽度** - 半角/全角判断
- ✅ **零依赖** - 仅使用 Python 标准库

## 快速开始

### 获取字符信息

```python
from unicode_lookup_utils import get_char_name, get_code_point, get_category

# 获取字符名称
name = get_char_name("A")
print(name)  # 'LATIN CAPITAL LETTER A'

# 获取码点
cp = get_code_point("中")
print(cp)  # 20013

# 获取分类
cat = get_category("5")
print(cat)  # 'Nd' (Decimal Number)
```

### 搜索字符

```python
from unicode_lookup_utils import search_by_name, search_by_category

# 按名称搜索
results = search_by_name("heart", limit=10)
for char_info in results:
    print(char_info['char'], char_info['name'])

# 按分类搜索
results = search_by_category("So")  # Symbol, other
print(results[:5])
```

### 完整字符信息

```python
from unicode_lookup_utils import get_full_info, UnicodeCharInfo

info = get_full_info("你好")
print(info.name)       # 'CJK UNIFIED IDEOGRAPH-4F60'
print(info.category)    # 'Lo'
print(info.block)      # 'CJK Unified Ideographs'
print(info.code_point) # 20320
print(info.utf8_hex)   # 'E4 BD A0'
```

### 字符类型检测

```python
from unicode_lookup_utils import (
    is_char_letter, is_char_digit, is_char_whitespace,
    is_char_punctuation, is_char_symbol
)

print(is_char_letter("A"))       # True
print(is_char_digit("5"))        # True
print(is_char_whitespace(" "))   # True
print(is_char_punctuation(","))  # True
print(is_char_symbol("$"))        # True
```

### HTML 实体与编码

```python
from unicode_lookup_utils import get_html_entity_named, get_char_by_code_point

# 获取 HTML 命名实体
entity = get_html_entity_named("&")
print(entity)  # '&amp;'

# 通过码点获取字符
char = get_char_by_code_point(0x1F600)
print(char)  # '😀'
```

## API 参考

### 核心函数

| 函数 | 说明 |
|------|------|
| `get_char_name(char)` | 获取字符的 Unicode 名称 |
| `get_code_point(char)` | 获取字符的码点值 |
| `get_category(char)` | 获取字符的分类代码 |
| `get_block(char)` | 获取字符所属的 Unicode 区块 |
| `get_full_info(char)` | 获取完整字符信息对象 |

### 搜索函数

| 函数 | 说明 |
|------|------|
| `search_by_name(keyword, limit)` | 按名称关键词搜索字符 |
| `search_by_category(category)` | 按分类代码搜索字符 |
| `get_char_by_name(name)` | 通过名称获取字符 |

### 类型检测函数

| 函数 | 说明 |
|------|------|
| `is_char_letter(char)` | 是否为字母 |
| `is_char_digit(char)` | 是否为数字 |
| `is_char_whitespace(char)` | 是否为空白字符 |
| `is_char_punctuation(char)` | 是否为标点 |
| `is_char_symbol(char)` | 是否为符号 |
| `is_char_control(char)` | 是否为控制字符 |
| `is_char_printable(char)` | 是否可打印 |
