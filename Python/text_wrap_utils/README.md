# Text Wrap 文本换行与排版工具模块

强大的文本换行、对齐、排版工具，支持 Unicode、CJK（中日韩）字符、ANSI 颜色码，零外部依赖。

## 功能特性

- **文本换行** - 智能换行，支持多种模式
- **文本对齐** - 左对齐、右对齐、居中、两端对齐
- **段落排版** - 缩进、悬挂缩进、行间距
- **CJK 支持** - 正确处理中日韩字符宽度
- **ANSI 支持** - 换行时保留 ANSI 颜色码
- **文本缩略** - 智能截断，添加占位符

## 快速使用

### 基本换行

```python
from text_wrap_utils import wrap, wrap_text

text = "这是一段很长的文本，需要自动换行处理..."

# 默认宽度 80
lines = wrap(text)

# 自定义宽度
lines = wrap_text(text, width=40)
```

### 文本对齐

```python
from text_wrap_utils import align_text, center, left_align, right_align, justify

# 居中
centered = center("Hello", width=20)

# 右对齐
right = right_align("Hello", width=20)

# 两端对齐
justified = justify("Hello World", width=20)
```

### CJK 文本处理

```python
from text_wrap_utils import wrap_text

chinese_text = "这是一个测试文本，用于演示中文字符的处理能力。"
lines = wrap_text(chinese_text, width=30)  # 正确计算中文字符宽度

for line in lines:
    print(f"|{line}|")
```

### 段落排版

```python
from text_wrap_utils import format_paragraph

para = format_paragraph(
    "这是一段示例文本...",
    width=50,
    first_line_indent=4,    # 首行缩进
    hanging_indent=2,       # 悬挂缩进
    alignment="justify"     # 两端对齐
)
print(para)
```

### 文本缩略

```python
from text_wrap_utils import shorten

long_text = "这是一段非常长的文本..."
short = shorten(long_text, width=20, placeholder="...")
print(short)
```

### TextWrapper 类

```python
from text_wrap_utils import TextWrapper

wrapper = TextWrapper(
    width=40,
    initial_indent="> ",     # 首行前缀
    subsequent_indent="  "   # 后续行前缀
)

lines = wrapper.wrap(text)
filled = wrapper.fill(text)  # 返回单字符串
```

## API 参考

### 核心函数

| 函数 | 描述 |
|------|------|
| `wrap_text(text, width, ...)` | 智能换行 |
| `align_text(text, width, alignment)` | 文本对齐 |
| `justify_text(text, width)` | 两端对齐 |
| `wrap_and_align(text, width, alignment)` | 换行并对齐 |
| `format_paragraph(text, width, ...)` | 段落排版 |

### 辅助函数

| 函数 | 描述 |
|------|------|
| `is_cjk_char(char)` | 检测中日韩字符 |
| `is_wide_char(char)` | 检测宽字符（占2格） |
| `display_width(text)` | 计算显示宽度 |
| `strip_ansi(text)` | 移除 ANSI 码 |
| `shorten_text(text, width, placeholder)` | 缩略文本 |
| `dedent_text(text)` | 移除公共缩进 |
| `indent_text(text, prefix)` | 添加缩进 |
| `center_block(text, width)` | 居中文本块 |
| `fill_text(text, width, ...)` | 填充文本 |

### 便捷函数

| 函数 | 描述 |
|------|------|
| `wrap(text, width=80)` | 基本换行 |
| `fill(text, width=80)` | 填充 |
| `center(text, width=80)` | 居中 |
| `left_align(text, width=80)` | 左对齐 |
| `right_align(text, width=80)` | 右对齐 |
| `justify(text, width=80)` | 两端对齐 |
| `shorten(text, width, placeholder)` | 缩略 |

### 枚举类型

```python
class Alignment(Enum):
    LEFT = "left"
    RIGHT = "right"
    CENTER = "center"
    JUSTIFY = "justify"

class WrapMode(Enum):
    SOFT = "soft"    # 尽量在词边界换行
    HARD = "hard"    # 强制在宽度处换行
    FILL = "fill"    # 尽量填充每行
```

### TextWrapper 类

```python
wrapper = TextWrapper(
    width=80,
    alignment=Alignment.LEFT,
    mode=WrapMode.SOFT,
    initial_indent="",
    subsequent_indent="",
    break_long_words=True,
    max_lines=None,
    placeholder="..."
)

wrapper.wrap(text)    # 返回行列表
wrapper.fill(text)    # 返回字符串
```

## CJK 字符宽度

CJK 字符（中文、日文、韩文）在终端中占用 2 个字符宽度，本模块自动处理：

```python
>>> display_width("中文")
4
>>> display_width("abc")
3
>>> display_width("中文abc")
7
```

## ANSI 颜色码支持

换行时保留 ANSI 颜色码：

```python
text = "\x1b[31m红色的文本\x1b[0m"
lines = wrap_text(text, width=10)  # 颜色码不受影响
```

## 测试

```bash
python Python/text_wrap_utils/text_wrap_utils_test.py
```

测试覆盖：
- CJK 字符检测
- 宽字符检测
- 显示宽度计算
- ANSI 码处理
- 各种换行模式
- 文本对齐
- 两端对齐
- 段落排版
- 文本缩略
- 边界情况

## 相关模块

- `text_utils` - 基本文本工具
- `markdown_utils` - Markdown 处理
- `format_utils` - 格式化工具

## License

MIT