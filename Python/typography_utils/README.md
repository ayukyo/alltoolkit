# Typography Utils - 智能文本排版工具

零外部依赖的 Python 排版工具集，提供智能引号转换、破折号规范化、省略号处理、文本换行等功能。

## 功能特性

### 🔤 引号处理
- **智能引号转换**：将直引号（`"` `'`）转换为弯引号（`"` `"` `''` `'`）
- **引号转直**：将弯引号转换回直引号
- 支持自定义引号字符
- 智能处理缩写（如 `it's`, `don't`）

### ➖ 破折号规范化
- 自动检测数字范围（使用 en dash `–`）
- 文本断句（使用 em dash `—`）
- 支持三种风格：`auto` / `en` / `em` / `hyphen`

### … 省略号处理
- 三点 (`...`) → 省略号字符 (`…`)
- 支持反向转换

### ✨ 综合排版
- 一键智能排版（引号 + 破折号 + 省略号 + 空格）
- 空白规范化（压缩多空格、移除首尾空白）
- 文本换行（支持缩进、段落处理）
- 寡妇/孤儿行处理

### 📊 字符统计
- 字符数（含/不含空格）
- 单词数（支持中英文混合）
- 句子数、段落数、行数
- 中英文字符分类统计

### 🔧 特殊字符处理
- HTML 转义/反转义
- Markdown 转义
- 标题格式转换
- URL Slug 生成

### 📐 对齐处理
- 左对齐、右对齐、居中
- 两端对齐

### 🀄 中文排版
- 中文标点规范化
- 段落首行缩进

## 安装

无需安装外部依赖，直接复制 `typography_utils.py` 到项目中即可使用。

## 快速开始

```python
from typography_utils import smartify, text_statistics, wrap_text

# 智能排版
text = 'He said "hello"... wait -- I mean "hi".'
result = smartify(text)
# 输出: He said "hello"… wait — I mean "hi".

# 文本统计
stats = text_statistics('Hello world. How are you?')
print(stats)
# {'chars': 26, 'words': 5, 'sentences': 2, ...}

# 文本换行
long_text = 'This is a very long text that needs to be wrapped.'
print(wrap_text(long_text, width=20))
```

## API 文档

### 引号处理

```python
smart_quotes(text, left_double='"', right_double='"', 
             left_single=''', right_single=''')
# 将直引号转换为智能引号

straighten_quotes(text)
# 将智能引号转换回直引号
```

### 破折号处理

```python
normalize_dashes(text, style='auto')
# 规范化破折号，style: 'auto' | 'en' | 'em' | 'hyphen'

em_dash(text)
# 转换为 em dash

en_dash(text)
# 转换为 en dash
```

### 省略号处理

```python
normalize_ellipsis(text, use_char=True)
# use_char=True: 使用 … 字符
# use_char=False: 使用 ...
```

### 综合排版

```python
smartify(text, quotes=True, dashes=True, ellipsis=True, spaces=True)
# 一站式智能排版
```

### 文本换行

```python
wrap_text(text, width=80, indent='', initial_indent='', 
          break_long_words=True, break_on_hyphens=True)
# 按指定宽度换行

wrap_paragraphs(text, width=80)
# 按段落换行
```

### 空白处理

```python
normalize_spaces(text)
# 规范化空白字符

remove_extra_blank_lines(text, max_blank=1)
# 移除多余空行
```

### 字符统计

```python
count_chars(text, include_spaces=True)
# 统计字符数

count_words(text)
# 统计单词数（支持中英文）

count_sentences(text)
# 统计句子数

count_paragraphs(text)
# 统计段落数

text_statistics(text)
# 获取完整统计信息
```

### 转义处理

```python
escape_html(text)
# HTML 转义

unescape_html(text)
# HTML 反转义

escape_markdown(text)
# Markdown 转义
```

### 标题与 Slug

```python
title_case(text, exceptions=None)
# 标题格式转换

slugify(text, separator='-', lowercase=True)
# 生成 URL 友好的 slug
```

### 对齐

```python
align_left(text, width, fillchar=' ')
# 左对齐

align_right(text, width, fillchar=' ')
# 右对齐

align_center(text, width, fillchar=' ')
# 居中

align_justify(text, width)
# 两端对齐
```

### 中文排版

```python
normalize_chinese_punctuation(text)
# 英文标点 → 中文标点

chinese_paragraph_indent(text, indent='　　')
# 添加首行缩进
```

## 示例

### 智能排版

```python
from typography_utils import smartify

text = '''
"The quick brown fox..." said Alice -- "jumps over the lazy dog!"
'''
print(smartify(text.strip()))
# 输出: "The quick brown fox…" said Alice — "jumps over the lazy dog!"
```

### 文本统计

```python
from typography_utils import text_statistics

article = '''
Python 是一门优雅的编程语言。
It is widely used in web development, data science, and automation.
'''
stats = text_statistics(article)
print(f"字符数: {stats['chars']}")
print(f"单词数: {stats['words']}")
print(f"中文字符: {stats['chinese_chars']}")
print(f"英文单词: {stats['english_words']}")
```

### 格式化输出

```python
from typography_utils import wrap_text, add_line_numbers, align_center

# 换行
long_text = "This is a long text that should be wrapped to fit within a specific width."
print(wrap_text(long_text, width=30))

# 添加行号
code = "def hello():\n    print('world')"
print(add_line_numbers(code, start=1))

# 居中
print(align_center("Hello", 20))
```

### 标题处理

```python
from typography_utils import title_case, slugify

# 标题格式
print(title_case('the lord of the rings'))
# 输出: The Lord of the Rings

# Slug 生成
print(slugify('Hello World! This is a Test.'))
# 输出: hello-world-this-is-a-test
```

## 运行测试

```bash
python typography_utils_test.py
```

## 版本历史

- **v1.0.0** (2026-05-21): 初始版本
  - 智能引号转换
  - 破折号规范化
  - 省略号处理
  - 文本统计
  - HTML/Markdown 转义
  - 标题格式和 Slug 生成
  - 文本对齐
  - 中文排版支持

## 许可证

MIT License

---

*由 AllToolkit 自动生成*