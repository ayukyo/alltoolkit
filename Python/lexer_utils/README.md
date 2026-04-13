# Lexer Utils - 词法分析器工具

一个零依赖的词法分析器工具集，用于解析和标记文本。纯 Python 标准库实现，支持自定义规则、优先级匹配、错误处理和流式处理。

## 功能特性

### 核心功能
- **Token 类型定义**: 支持字符串匹配、正则匹配、优先级设置
- **词法分析器构建**: 灵活的 API 构建复杂分词器
- **流式处理**: 迭代器模式，支持大文件处理
- **位置跟踪**: 精确的行号、列号、字符位置信息
- **错误处理**: 自定义错误处理器，支持恢复和继续
- **Token 导航**: 查找、匹配、跳过、收集等操作

### Token 类型
- `LITERAL`: 字面量（数字、字符串等）
- `KEYWORD`: 关键字
- `IDENTIFIER`: 标识符
- `OPERATOR`: 操作符
- `PUNCTUATION`: 标点符号
- `WHITESPACE`: 空白字符
- `COMMENT`: 注释
- `ERROR`: 错误 token
- `EOF`: 文件结束

### 预构建分词器
- `simple_tokenize`: 通用文本分词
- `tokenize_code`: 编程语言代码分词
- `tokenize_json`: JSON 数据分词
- `tokenize_math`: 数学表达式分词

## 快速开始

### 基本用法

```python
from lexer_utils import Lexer, TokenType

# 创建词法分析器
lexer = Lexer()

# 添加 token 类型
lexer.add_type(TokenType("NUMBER", r"\d+"))
lexer.add_type(TokenType("PLUS", r"\+"))
lexer.add_type(TokenType("WHITESPACE", r"\s+", ignore=True))

# 分析文本
tokens = lexer.tokenize("123 + 456")
for token in tokens:
    print(f"{token.type.name}: {token.value}")
```

### 构建器模式

```python
from lexer_utils import LexerBuilder

lexer = (LexerBuilder()
    .keywords("if", "else", "while", "for")
    .operators("+", "-", "*", "/", "==", "!=", "<", ">")
    .punctuations("(", ")", "{", "}", ";", ",")
    .define("IDENTIFIER", r"[a-zA-Z_][a-zA-Z0-9_]*")
    .define("NUMBER", r"\d+(\.\d+)?")
    .define("STRING", r'"[^"]*"')
    .whitespace()
    .build())

tokens = lexer.tokenize("if (x == 10) { return x; }")
```

### 回调转换

```python
# 自动转换 token 值
lexer.add_type(TokenType(
    name="NUMBER",
    pattern=r"\d+(\.\d+)?",
    callback=lambda x: float(x) if "." in x else int(x),
))
```

### 预构建分词器

```python
from lexer_utils import tokenize_code, tokenize_json, tokenize_math

# 代码分词
tokens = tokenize_code("function add(a, b) { return a + b; }")

# JSON 分词
tokens = tokenize_json('{"name": "test", "value": 42}')

# 数学表达式分词
tokens = tokenize_math("sin(x) * cos(y) + 3.14")
```

### Token 流导航

```python
from lexer_utils import TokenStream

stream = TokenStream(tokens)

# 查看当前 token
print(stream.current)

# 查看后续 token
print(stream.peek(1), stream.peek(2))

# 匹配序列
if stream.match_sequence("IF", "LPAREN"):
    # 处理 if 语句
    pass

# 期望特定类型
number = stream.expect("NUMBER")

# 查找 token
pos = stream.find("RETURN")
```

## API 参考

### Lexer 类

| 方法 | 描述 |
|------|------|
| `add_type(token_type)` | 添加 token 类型 |
| `add_keyword(name, keyword)` | 添加关键字 |
| `add_operator(name, operator)` | 添加操作符 |
| `add_punctuation(name, punctuation)` | 添加标点符号 |
| `tokenize(text)` | 将文本转换为 token 列表 |
| `tokenize_iter(text)` | 流式生成 token |
| `on_error(handler)` | 设置错误处理器 |

### LexerBuilder 类

| 方法 | 描述 |
|------|------|
| `define(name, pattern, category, priority, ignore, callback)` | 定义 token 类型 |
| `keyword(keyword, name)` | 添加关键字 |
| `keywords(*keywords)` | 添加多个关键字 |
| `operator(op, name)` | 添加操作符 |
| `operators(*ops)` | 添加多个操作符 |
| `punctuation(punc, name)` | 添加标点符号 |
| `punctuations(*puncs)` | 添加多个标点符号 |
| `whitespace(ignore)` | 启用空白处理 |
| `on_error(handler)` | 设置错误处理器 |
| `build()` | 构建词法分析器 |

### TokenStream 类

| 方法 | 描述 |
|------|------|
| `current` | 获取当前 token |
| `peek(offset)` | 查看指定位置的 token |
| `advance()` | 前进并返回 token |
| `expect(type_name)` | 期望指定类型 |
| `accept(type_name)` | 接受指定类型 |
| `match_sequence(*types)` | 匹配类型序列 |
| `find(type_name, value)` | 查找 token |
| `find_all(type_name)` | 查找所有匹配 |

### 便捷函数

| 函数 | 描述 |
|------|------|
| `create_lexer(**kwargs)` | 快速创建词法分析器 |
| `tokenize(text, rules)` | 快速分词 |
| `simple_tokenize(text)` | 简单分词 |
| `tokenize_code(text)` | 代码分词 |
| `tokenize_json(text)` | JSON 分词 |
| `tokenize_math(text)` | 数学表达式分词 |
| `count_tokens(tokens)` | 统计 token 数量 |
| `filter_tokens(tokens, types, categories)` | 过滤 token |
| `tokens_to_dict(tokens)` | 转换为字典 |
| `dict_to_tokens(data)` | 从字典恢复 |

## 使用场景

1. **编程语言解析**: 构建自定义语言的词法分析器
2. **配置文件处理**: 解析自定义格式的配置文件
3. **数据提取**: 从文本中提取结构化数据
4. **代码分析**: 分析代码结构、统计关键字使用
5. **模板引擎**: 解析模板语法
6. **数学计算器**: 解析和计算数学表达式
7. **DSL 实现**: 实现领域特定语言的词法分析

## 文件结构

```
lexer_utils/
├── lexer_utils.py         # 主模块
├── lexer_utils_test.py    # 单元测试 (70+ 测试)
├── lexer_utils_examples.py # 使用示例 (13 个场景)
└── README.md              # 本文档
```

## 运行测试

```bash
python lexer_utils_test.py
```

## 运行示例

```bash
python lexer_utils_examples.py
```

## 特性

- ✅ 零外部依赖，纯 Python 标准库实现
- ✅ 支持自定义 token 类型和优先级
- ✅ 支持正则表达式模式匹配
- ✅ 支持回调函数转换 token 值
- ✅ 支持错误处理和恢复
- ✅ 支持流式处理（迭代器模式）
- ✅ 支持精确位置跟踪（行、列、字符索引）
- ✅ 支持 Token 流导航和查找
- ✅ 提供预构建分词器（代码、JSON、数学）
- ✅ 完整的类型提示
- ✅ 完整的单元测试覆盖

## 版本

- v1.0.0 (2026-04-13): 初始版本