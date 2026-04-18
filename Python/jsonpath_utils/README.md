# JSONPath Utils - JSONPath 查询工具

[English](#english) | [中文](#中文)

---

## 中文

### 简介

JSONPath Utils 是一个零依赖的 JSONPath 查询工具模块，用于从 JSON 数据中提取信息。支持完整的 JSONPath 语法，包括过滤器、切片、递归下降等高级功能。

### 特性

- ✅ **零依赖** - 仅使用 Python 标准库
- ✅ **完整语法** - 支持标准 JSONPath 语法
- ✅ **过滤器表达式** - 支持比较运算符和逻辑运算符
- ✅ **数组切片** - 支持 start:end:step 格式
- ✅ **递归下降** - 支持 `..` 递归查找
- ✅ **通配符** - 支持 `*` 和 `[*]`
- ✅ **联合查询** - 支持多索引/键选择 `[0,1,2]`
- ✅ **表达式编译** - 支持预编译提高性能

### 安装

无需安装，直接导入使用：

```python
from jsonpath_utils.mod import find, find_one, JSONPath
```

### 快速开始

```python
from mod import find, find_one

data = {
    "store": {
        "book": [
            {"title": "Book 1", "price": 10},
            {"title": "Book 2", "price": 20},
            {"title": "Book 3", "price": 30}
        ]
    }
}

# 获取所有书名
titles = find("$.store.book[*].title", data)
# ['Book 1', 'Book 2', 'Book 3']

# 获取第一本书
first_book = find_one("$.store.book[0]", data)
# {'title': 'Book 1', 'price': 10}

# 过滤价格大于15的书
expensive = find("$.store.book[?(@.price > 15)]", data)
# [{'title': 'Book 2', 'price': 20}, {'title': 'Book 3', 'price': 30}]
```

### 语法参考

| 表达式 | 说明 | 示例 |
|--------|------|------|
| `$` | 根对象 | `$` |
| `@` | 当前对象（在过滤器中） | `@.price` |
| `.` | 子属性访问 | `$.store.book` |
| `..` | 递归下降 | `$..price` |
| `*` | 通配符 | `$.store.*` |
| `[n]` | 数组索引 | `$[0]` |
| `[start:end]` | 数组切片 | `$[1:3]` |
| `[n1,n2]` | 联合查询 | `$[0,2]` |
| `[?(expr)]` | 过滤器 | `$[?(@.price < 10)]` |

### 过滤器运算符

| 运算符 | 说明 | 示例 |
|--------|------|------|
| `==` | 等于 | `@.price == 10` |
| `!=` | 不等于 | `@.category != "fiction"` |
| `<` | 小于 | `@.price < 10` |
| `<=` | 小于等于 | `@.price <= 10` |
| `>` | 大于 | `@.price > 10` |
| `>=` | 大于等于 | `@.price >= 10` |
| `&&` | 逻辑 AND | `@.price > 10 && @.price < 20` |
| `||` | 逻辑 OR | `@.price < 10 || @.price > 20` |
| `!` | 逻辑 NOT | `!@.isbn` |

### API 参考

#### `find(expression, data)`
查询 JSON 数据，返回所有匹配值列表。

```python
find("$.store.book[*].author", data)
```

#### `find_one(expression, data)`
查询 JSON 数据，返回第一个匹配值。

```python
find_one("$.store.bicycle.color", data)
```

#### `compile(expression)`
预编译 JSONPath 表达式，用于重复查询。

```python
path = compile("$.store.book[*]")
results = path.query(data)
```

#### `validate(expression)`
验证 JSONPath 表达式是否有效。

```python
validate("$.store.book[*]")  # True
validate("invalid")          # False
```

#### `JSONPath(expression)`
创建 JSONPath 对象，支持完整查询功能。

```python
path = JSONPath("$.store.book[?(@.price < 10)]")
results = path.query(data)
matches = path.match(data)  # 返回带路径的结果
```

### 测试

```bash
python jsonpath_utils_test.py
```

测试覆盖：
- 词法分析（Lexer）
- 语法解析（Parser）
- 基本查询（Root、Child、Index）
- 数组切片
- 通配符
- 联合查询
- 递归下降
- 过滤器表达式
- 边界值测试

---

## English

### Introduction

JSONPath Utils is a zero-dependency JSONPath query utility module for extracting data from JSON structures. Supports full JSONPath syntax including filters, slices, recursive descent, and advanced features.

### Features

- ✅ **Zero Dependencies** - Uses only Python standard library
- ✅ **Full Syntax** - Standard JSONPath syntax support
- ✅ **Filter Expressions** - Comparison and logical operators
- ✅ **Array Slicing** - start:end:step format
- ✅ **Recursive Descent** - `..` recursive search
- ✅ **Wildcards** - `*` and `[*]` support
- ✅ **Union Queries** - Multi-index/key selection `[0,1,2]`
- ✅ **Expression Compilation** - Pre-compile for performance

### Quick Start

```python
from mod import find, find_one

data = {
    "store": {
        "book": [
            {"title": "Book 1", "price": 10},
            {"title": "Book 2", "price": 20},
            {"title": "Book 3", "price": 30}
        ]
    }
}

# Get all book titles
titles = find("$.store.book[*].title", data)
# ['Book 1', 'Book 2', 'Book 3']

# Get first book
first_book = find_one("$.store.book[0]", data)
# {'title': 'Book 1', 'price': 10}

# Filter books with price > 15
expensive = find("$.store.book[?(@.price > 15)]", data)
# [{'title': 'Book 2', 'price': 20}, {'title': 'Book 3', 'price': 30}]
```

### Syntax Reference

| Expression | Description | Example |
|------------|-------------|---------|
| `$` | Root object | `$` |
| `@` | Current object (in filter) | `@.price` |
| `.` | Child accessor | `$.store.book` |
| `..` | Recursive descent | `$..price` |
| `*` | Wildcard | `$.store.*` |
| `[n]` | Array index | `$[0]` |
| `[start:end]` | Array slice | `$[1:3]` |
| `[n1,n2]` | Union | `$[0,2]` |
| `[?(expr)]` | Filter | `$[?(@.price < 10)]` |

### Testing

```bash
python jsonpath_utils_test.py
```

---

## License

MIT License - See LICENSE file for details.

---

**Author**: AllToolkit  
**Last Updated**: 2026-04-18