# Syntax Highlight Utils

一个零依赖的 Python 语法高亮工具，支持 ANSI 终端输出和 HTML 格式输出。

## 特性

- ✅ **零外部依赖** - 纯 Python 标准库实现
- ✅ **多语言支持** - Python、JavaScript 等
- ✅ **ANSI 输出** - 终端彩色显示
- ✅ **HTML 输出** - 网页展示，可自定义样式
- ✅ **行号支持** - 可选显示行号
- ✅ **Token 分析** - 支持代码词法分析
- ✅ **多种语法元素** - 关键字、字符串、数字、注释、运算符等

## 安装

将 `syntax_highlight_utils` 目录复制到你的项目中：

```bash
cp -r syntax_highlight_utils/ your_project/
```

## 快速开始

### 基本使用

```python
from syntax_highlight import highlight, highlight_html

# 终端 ANSI 彩色输出
code = '''
def hello(name: str) -> str:
    return f"Hello, {name}!"
'''
print(highlight(code, lang="python"))

# HTML 输出
html = highlight_html(code, lang="python", line_numbers=True)
```

### 显示行号

```python
from syntax_highlight import highlight

code = '''
def fibonacci(n: int) -> int:
    if n <= 1:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)
'''

print(highlight(code, lang="python", line_numbers=True))
```

输出：
```
   1 | 
   2 | def fibonacci(n: int) -> int:
   3 |     if n <= 1:
   4 |         return n
   5 |     return fibonacci(n - 1) + fibonacci(n - 2)
   6 | 
```

### JavaScript 语法高亮

```python
from syntax_highlight import highlight

js_code = '''
const fetchData = async (url) => {
    const response = await fetch(url);
    return response.json();
};
'''

print(highlight(js_code, lang="javascript"))
```

### HTML 输出

```python
from syntax_highlight import highlight_html

code = 'def greet(): return "Hello"'
html = highlight_html(code, lang="python")

# 自定义样式
custom_style = "background: #1a1a2e; color: #e0e0e0; padding: 20px;"
html = highlight_html(code, lang="python", pre_style=custom_style)
```

### Token 分析

```python
from syntax_highlight import get_tokens

code = "x = 42  # variable"
tokens = get_tokens(code)

for token in tokens:
    print(f"{token.type.value}: {token.value!r}")
```

输出：
```
variable: 'x'
whitespace: ' '
operator: '='
whitespace: ' '
number: '42'
whitespace: '  '
comment: '# variable'
```

### 移除 ANSI 代码

```python
from syntax_highlight import highlight, strip_ansi

highlighted = highlight("def test(): pass")
plain_text = strip_ansi(highlighted)  # 移除颜色代码
```

## 支持的语言

| 语言 | 标识符 |
|------|--------|
| Python | `python` |
| JavaScript | `javascript`, `js` |

## 支持的语法元素

| 元素类型 | 说明 |
|----------|------|
| `keyword` | 关键字 (def, class, if, else...) |
| `string` | 字符串字面量 |
| `number` | 数字 (整数、浮点数、十六进制、二进制) |
| `comment` | 注释 |
| `operator` | 运算符 (+, -, *, ==, !=...) |
| `function` | 函数名 |
| `class` | 类名 |
| `decorator` | 装饰器 (@property...) |
| `builtin` | 内置函数 (print, len...) |
| `constant` | 常量 (True, False, None, ALL_CAPS) |
| `bracket` | 括号 ( ) [ ] { } |
| `punctuation` | 标点符号 (: , .) |

## 文件结构

```
syntax_highlight_utils/
├── syntax_highlight.py    # 主模块
├── test_syntax_highlight.py  # 测试文件
├── examples.py           # 使用示例
└── README.md            # 文档
```

## 运行测试

```bash
python -m pytest test_syntax_highlight.py -v
# 或
python test_syntax_highlight.py
```

## 运行示例

```bash
python examples.py
```

## API 参考

### `highlight(code, lang='python', line_numbers=False)`

返回 ANSI 彩色的代码字符串。

**参数：**
- `code` (str): 源代码
- `lang` (str): 语言标识符，默认 'python'
- `line_numbers` (bool): 是否显示行号，默认 False

**返回：** str - ANSI 彩色代码

### `highlight_html(code, lang='python', line_numbers=False, pre_style=None)`

返回 HTML 格式的代码。

**参数：**
- `code` (str): 源代码
- `lang` (str): 语言标识符
- `line_numbers` (bool): 是否显示行号
- `pre_style` (str): 自定义 CSS 样式

**返回：** str - HTML 代码

### `get_tokens(code, lang='python')`

返回代码的 Token 列表。

**参数：**
- `code` (str): 源代码
- `lang` (str): 语言标识符

**返回：** List[Token] - Token 对象列表

### `strip_ansi(text)`

移除文本中的 ANSI 转义序列。

**参数：**
- `text` (str): 包含 ANSI 代码的文本

**返回：** str - 纯文本

## 许可证

MIT License