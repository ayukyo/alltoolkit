# ISBN Utils - 国际标准书号(ISBN)验证与处理工具库

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/Python-3.6+-blue.svg)](https://www.python.org/)

完整的ISBN验证与处理工具库，支持ISBN-10和ISBN-13格式。

## 功能特性

### 验证功能
- ✅ ISBN-10验证（模11算法，支持X检验位）
- ✅ ISBN-13验证（EAN-13算法，978/979前缀）
- ✅ 自动类型检测验证

### 计算功能
- ✅ ISBN-10检验位计算
- ✅ ISBN-13检验位计算

### 转换功能
- ✅ ISBN-10 → ISBN-13转换
- ✅ ISBN-13 → ISBN-10转换（仅978前缀）

### 格式化功能
- ✅ 标准化（移除分隔符）
- ✅ 格式化（添加分隔符）
- ✅ 自定义分隔符支持

### 解析功能
- ✅ 详细信息解析
- ✅ 分组/出版商识别
- ✅ ISBN各部分提取

### 批量操作
- ✅ 批量验证
- ✅ 文本中提取ISBN
- ✅ 统计分析

## 快速开始

### 安装

本模块为零依赖设计，可直接导入使用：

```python
from isbn_utils import (
    is_valid_isbn, is_valid_isbn10, is_valid_isbn13,
    format_isbn, normalize_isbn,
    isbn10_to_isbn13, isbn13_to_isbn10,
    extract_isbns, batch_validate
)
```

### 基础用法

#### 验证ISBN

```python
from isbn_utils import is_valid_isbn10, is_valid_isbn13, is_valid_isbn

# ISBN-10验证
print(is_valid_isbn10('0306406152'))    # True
print(is_valid_isbn10('0-306-40615-2')) # True
print(is_valid_isbn10('080442957X'))    # True (X检验位)

# ISBN-13验证
print(is_valid_isbn13('9780306406157'))       # True
print(is_valid_isbn13('978-0-306-40615-7'))   # True
print(is_valid_isbn13('9791091146135'))       # True (979前缀)

# 自动检测类型
print(is_valid_isbn('0306406152'))     # True (ISBN-10)
print(is_valid_isbn('9780306406157'))  # True (ISBN-13)
```

#### 检验位计算

```python
from isbn_utils import calculate_isbn10_check_digit, calculate_isbn13_check_digit

# ISBN-10检验位
print(calculate_isbn10_check_digit('030640615'))  # '2'
print(calculate_isbn10_check_digit('080442957'))  # 'X'

# ISBN-13检验位
print(calculate_isbn13_check_digit('978030640615'))  # '7'
```

#### 格式转换

```python
from isbn_utils import isbn10_to_isbn13, isbn13_to_isbn10

# ISBN-10 → ISBN-13
print(isbn10_to_isbn13('0306406152'))  # '9780306406157'

# ISBN-13 → ISBN-10 (仅978前缀)
print(isbn13_to_isbn10('9780306406157'))  # '0306406152'
print(isbn13_to_isbn10('9791091146135'))  # None (无法转换)
```

#### 格式化

```python
from isbn_utils import format_isbn, normalize_isbn

# 标准化（移除分隔符）
print(normalize_isbn('978-0-306-40615-7'))  # '9780306406157'

# 格式化（添加分隔符）
print(format_isbn('9780306406157'))  # '978-0-3064-0615-7'

# 自定义分隔符
print(format_isbn('9780306406157', ' '))  # '978 0 3064 0615 7'
print(format_isbn('9780306406157', ''))   # '9780306406157'
```

#### ISBN类

```python
from isbn_utils import ISBN, ISBNType

isbn = ISBN('978-0-306-40615-7')

print(isbn.is_valid())          # True
print(isbn.get_type())          # ISBNType.ISBN13
print(isbn.normalize())         # '9780306406157'
print(isbn.format())            # '978-0-3064-0615-7'
print(isbn.to_isbn10())         # '0306406152'

# 获取详细信息
info = isbn.get_info()
print(info.check_digit)         # '7'
print(info.prefix)              # '978'
```

#### 文本提取

```python
from isbn_utils import extract_isbns

text = "这本书的ISBN是978-0-306-40615-7，另一本是0-306-40615-2"
isbns = extract_isbns(text)
print(isbns)  # ['9780306406157', '0306406152']
```

#### 批量验证

```python
from isbn_utils import batch_validate

isbns = ['9780306406157', '0306406152', 'invalid', '080442957X']
result = batch_validate(isbns)

print(result['valid'])          # ['9780306406157', '0306406152', '080442957X']
print(result['invalid'])        # ['invalid']
print(result['stats'])
# {'total': 4, 'valid_count': 3, 'invalid_count': 1, 'isbn10_count': 2, 'isbn13_count': 1}
```

## API参考

### 验证函数

| 函数 | 说明 |
|------|------|
| `is_valid_isbn10(isbn)` | 验证ISBN-10 |
| `is_valid_isbn13(isbn)` | 验证ISBN-13 |
| `is_valid_isbn(isbn)` | 自动检测并验证 |

### 计算函数

| 函数 | 说明 |
|------|------|
| `calculate_isbn10_check_digit(digits)` | 计算ISBN-10检验位(9位→检验位) |
| `calculate_isbn13_check_digit(digits)` | 计算ISBN-13检验位(12位→检验位) |

### 转换函数

| 函数 | 说明 |
|------|------|
| `isbn10_to_isbn13(isbn10)` | ISBN-10转ISBN-13 |
| `isbn13_to_isbn10(isbn13)` | ISBN-13转ISBN-10(仅978前缀) |

### 格式化函数

| 函数 | 说明 |
|------|------|
| `format_isbn(isbn, separator='-')` | 格式化ISBN显示 |
| `normalize_isbn(isbn)` | 移除分隔符标准化 |

### 解析函数

| 函数 | 说明 |
|------|------|
| `parse_isbn(isbn)` | 解析并返回详细信息 |
| `get_isbn_info(isbn)` | 获取完整ISBNInfo对象 |
| `identify_prefix(code)` | 识别分组代码 |

### 批量函数

| 函数 | 说明 |
|------|------|
| `batch_validate(isbns)` | 批量验证并统计 |
| `extract_isbns(text)` | 从文本提取所有ISBN |

### ISBN类

```python
class ISBN:
    def __init__(isbn: str)
    def is_valid() -> bool
    def get_type() -> ISBNType
    def normalize() -> str
    def format(separator='-') -> str
    def to_isbn13() -> str | None
    def to_isbn10() -> str | None
    def get_info() -> ISBNInfo
```

## ISBN背景知识

### ISBN-10 (2007年前)
- 格式：X-XXXXX-XXX-X（分组-出版商-标题-检验位）
- 算法：模11，检验位可能是0-9或X（10）
- 例如：`0306406152`

### ISBN-13 (2007年后)
- 格式：XXX-X-XXXX-XXXX-X（前缀-分组-出版商-标题-检验位）
- 前缀：978或979
- 算法：EAN-13模10
- 例如：`9780306406157`

### 前缀含义
- **978**：可转换为ISBN-10
- **979**：无法转换为ISBN-10（新增前缀）

### 分组代码
- 0, 1：英语国家
- 2：法语国家
- 3：德语国家
- 4：日本
- 5：俄语国家
- 7：中国
- 957：台湾
- 962：香港

## 测试

运行测试：

```bash
python Python/isbn_utils/test_isbn_utils.py
```

测试覆盖：
- ISBN-10验证（有效/无效/边界）
- ISBN-13验证（978/979前缀）
- 检验位计算
- 格式转换
- 格式化输出
- 文本提取
- 批量操作

## 许可证

MIT License - 零外部依赖，纯Python标准库实现

## 参考

- [ISBN国际组织](https://www.isbn-international.org/)
- [ISBN Wikipedia](https://en.wikipedia.org/wiki/International_Standard_Book_Number)