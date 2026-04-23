# Text Wrap Utilities

A comprehensive text wrapping, justification and alignment utility module for Python with zero external dependencies.

## Features

- **Word Wrapping** - Wrap text at specified width with multiple modes
- **Text Alignment** - Left, right, center, and justified alignment
- **Paragraph Formatting** - First-line indent, hanging indent, line spacing
- **CJK Support** - Proper handling of Chinese, Japanese, Korean characters
- **ANSI Code Aware** - Preserves ANSI color codes during wrapping
- **Smart Truncation** - Shorten text with custom placeholders
- **Unicode Support** - Full Unicode and display width calculation

## Installation

No external dependencies required. Simply copy the module to your project.

```python
from text_wrap_utils.mod import wrap_text, align_text, justify_text
```

## Quick Start

### Basic Wrapping

```python
from text_wrap_utils.mod import wrap_text

text = "This is a sample text that will be wrapped to fit within a specified width."
lines = wrap_text(text, width=40)
for line in lines:
    print(line)
```

### Text Alignment

```python
from text_wrap_utils.mod import align_text, Alignment

# Left align
left = align_text("Hello", 20, Alignment.LEFT)

# Right align
right = align_text("Hello", 20, Alignment.RIGHT)

# Center
centered = align_text("Hello", 20, Alignment.CENTER)

# Justified
justified = justify_text("Hello world test", 30)
```

### Wrap and Align Combined

```python
from text_wrap_utils.mod import wrap_and_align, Alignment

text = "This is a sample text for wrap and align demonstration."
lines = wrap_and_align(text, width=30, alignment=Alignment.JUSTIFY)
for line in lines:
    print(line)
```

### Paragraph Formatting

```python
from text_wrap_utils.mod import format_paragraph

text = "This is a paragraph that will be formatted with indentation."
formatted = format_paragraph(
    text,
    width=50,
    alignment=Alignment.JUSTIFY,
    first_line_indent=4,
    hanging_indent=2
)
print(formatted)
```

### Using TextWrapper Class

```python
from text_wrap_utils.mod import TextWrapper

wrapper = TextWrapper(
    width=40,
    initial_indent="> ",
    subsequent_indent="  "
)

# Wrap to list
lines = wrapper.wrap(text)

# Fill to string
filled = wrapper.fill(text)
```

### Text Shortening

```python
from text_wrap_utils.mod import shorten_text

long_text = "This is a very long text that needs to be shortened."
shortened = shorten_text(long_text, width=20, placeholder="...")
print(shortened)  # "This is a very l..."
```

### CJK Text Handling

```python
from text_wrap_utils.mod import wrap_text, display_width

# Chinese text
chinese = "这是一个测试文本用于演示中文字符的换行功能。"
lines = wrap_text(chinese, width=30)

# Display width calculation (CJK chars = 2 cells)
width = display_width("中文")  # Returns 4
width = display_width("hello世界")  # Returns 9 (5 + 4)
```

### Convenience Functions

```python
from text_wrap_utils.mod import wrap, fill, center, justify, shorten

lines = wrap(text, width=80)  # Basic wrapping
filled = fill(text, width=80)  # Fill text
centered = center(text[:20], width=80)  # Center
justified = justify(text, width=80)  # Justify
shortened = shorten(text, width=30)  # Shorten
```

## API Reference

### Core Functions

| Function | Description |
|----------|-------------|
| `wrap_text(text, width, ...)` | Wrap text to specified width |
| `align_text(text, width, alignment)` | Align text within width |
| `justify_text(text, width)` | Justify text with space distribution |
| `wrap_and_align(text, width, alignment, ...)` | Combined wrap and align |

### Formatting Functions

| Function | Description |
|----------|-------------|
| `format_paragraph(text, ...)` | Format paragraph with indent |
| `fill_text(text, width, ...)` | Fill and wrap text |
| `shorten_text(text, width, ...)` | Shorten text to fit width |
| `indent_text(text, prefix, ...)` | Add indentation to lines |
| `dedent_text(text)` | Remove common indentation |
| `center_block(text, width)` | Center a block of text |

### Utility Functions

| Function | Description |
|----------|-------------|
| `is_cjk_char(char)` | Check if CJK character |
| `is_wide_char(char)` | Check if wide character |
| `display_width(text)` | Calculate display width |
| `strip_ansi(text)` | Remove ANSI escape codes |

### Classes

#### TextWrapper

Configurable text wrapper with OO interface.

```python
wrapper = TextWrapper(
    width=80,                  # Line width
    alignment=Alignment.LEFT,  # Alignment mode
    initial_indent="",         # First line indent
    subsequent_indent="",      # Subsequent lines indent
    break_long_words=True,     # Break words if needed
    max_lines=None,            # Maximum lines
    placeholder="..."          # Truncation placeholder
)

lines = wrapper.wrap(text)
filled = wrapper.fill(text)
```

### Enums

#### Alignment

- `LEFT` - Left alignment
- `RIGHT` - Right alignment
- `CENTER` - Center alignment
- `JUSTIFY` - Full justification

#### WrapMode

- `SOFT` - Wrap at word boundaries
- `HARD` - Wrap exactly at width
- `FILL` - Fill each line as much as possible

## Examples

### Console Output Formatting

```python
from text_wrap_utils.mod import wrap_text, center

# Center a title
title = center("Welcome to My App", width=60)
print(title)

# Wrap description
description = "A wonderful application that helps you manage your daily tasks with ease."
for line in wrap_text(description, width=60):
    print(line)
```

### Markdown-like Indentation

```python
from text_wrap_utils.mod import indent_text

code = "def hello():\n    print('world')"
indented = indent_text(code, prefix="    ", skip_first=True)
print(f"```\n{indented}\n```")
```

### Truncating Titles

```python
from text_wrap_utils.mod import shorten_text

title = "This is a Very Long Article Title That Needs to Be Shortened"
short_title = shorten_text(title, width=30)
print(short_title)  # "This is a Very Long Art..."
```

## License

MIT License - Part of AllToolkit project.