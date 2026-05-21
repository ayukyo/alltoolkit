# ASCII Banner Utils

ASCII 艺术横幅生成器，纯 Python 实现，零外部依赖。

## 功能特性

- **多种内置字体**: standard, block, mini, shadow, digital, bubble
- **ANSI 颜色支持**: 支持 16 种标准 ANSI 颜色
- **边框样式**: single, double, rounded, bold, ascii
- **对齐方式**: 左对齐、居中、右对齐
- **宽度限制**: 支持最大宽度限制和自动换行
- **流式 API**: BannerBuilder 提供链式调用
- **预定义模板**: welcome, hello, success, error, warning, done

## 快速开始

```python
from ascii_banner_utils.mod import render, print_banner, list_fonts

# 基础用法
print_banner("HELLO", font='standard')

# 获取可用字体
fonts = list_fonts()  # ['standard', 'block', 'mini', 'shadow', 'digital', 'bubble']
```

## 使用示例

### 不同字体

```python
# Standard 字体 - 经典 FIGLET 风格
print_banner("HELLO", font='standard')

# Block 字体 - 块状风格
print_banner("WORLD", font='block')

# Mini 字体 - 精简风格（3 行高）
print_banner("CODE", font='mini')

# Shadow 字体 - 带阴影效果（7 行高）
print_banner("SHADOW", font='shadow')

# Bubble 字体 - 气泡风格
print_banner("BUBBLE", font='bubble')
```

### 颜色支持

```python
from ascii_banner_utils.mod import print_banner, list_colors

# 获取可用颜色
colors = list_colors()  # ['black', 'red', 'green', 'yellow', 'blue', ...]

# 带颜色打印
print_banner("PYTHON", font='standard', color='cyan')
print_banner("ERROR", font='block', color='red')
print_banner("SUCCESS", font='shadow', color='bright_green')
```

### 边框样式

```python
# 单线边框
print_banner("TITLE", font='block', border='single')

# 双线边框
print_banner("WELCOME", font='standard', border='double')

# 圆角边框
print_banner("INFO", font='mini', border='rounded')

# 加粗边框
print_banner("ALERT", font='block', border='bold')
```

### 流式 API (BannerBuilder)

```python
from ascii_banner_utils.mod import BannerBuilder

BannerBuilder("HELLO")
    .font('block')
    .color('green')
    .border('rounded')
    .align('center')
    .width(80)
    .show()
```

### 预定义模板

```python
from ascii_banner_utils.mod import show_template, template

# 使用预定义模板
show_template('welcome')  # 双线边框 + cyan 颜色
show_template('success')  # 绿色 + 圆角边框
show_template('error')    # 红色 + 加粗边框

# 获取模板文本
banner_text = template('hello')
```

### 自定义填充字符

```python
# 替换默认的 █ 字符
print_banner("CUSTOM", font='block', fill_char='*')
print_banner("CUSTOM", font='standard', fill_char='#')
```

## API 参考

### ASCIIBannerGenerator 类

```python
class ASCIIBannerGenerator:
    def __init__(self, font: str = 'standard')
    
    def render_text(
        self,
        text: str,
        color: Optional[str] = None,
        fill_char: Optional[str] = None,
        border: Optional[str] = None,
        align: str = 'left',
        max_width: Optional[int] = None
    ) -> str
    
    def get_available_fonts(self) -> List[str]
    def set_font(self, font: str) -> None
```

### 便捷函数

| 函数 | 说明 |
|------|------|
| `render(text, font, **kwargs)` | 渲染文本为 ASCII 艺术横幅 |
| `print_banner(text, font, **kwargs)` | 打印 ASCII 艺术横幅 |
| `list_fonts()` | 获取所有可用字体 |
| `list_colors()` | 获取所有可用颜色 |
| `template(name)` | 使用预定义模板渲染 |
| `show_template(name)` | 打印预定义模板横幅 |

### BannerBuilder 类

```python
class BannerBuilder:
    def text(text: str) -> BannerBuilder
    def font(font: str) -> BannerBuilder
    def color(color: str) -> BannerBuilder
    def fill(char: str) -> BannerBuilder
    def border(style: str = 'single') -> BannerBuilder
    def align(align: str) -> BannerBuilder  # 'left', 'center', 'right'
    def width(max_width: int) -> BannerBuilder
    def build() -> str
    def show() -> None
```

## 预定义模板

| 模板名 | 文本 | 字体 | 颜色 | 边框 |
|--------|------|------|------|------|
| welcome | WELCOME | standard | cyan | double |
| hello | HELLO | block | green | - |
| success | SUCCESS! | shadow | bright_green | rounded |
| error | ERROR! | standard | red | bold |
| warning | WARNING | block | yellow | - |
| done | DONE | mini | bright_cyan | - |

## 字符支持

Standard 字体支持:
- 大写字母 A-Z
- 数字 0-9
- 常见符号: ! ? . , - _ : ; ( ) [ ] { } / \ | @ # $ % & * + = < > ~ ^ ' "

其他字体支持字符略有不同，请参考代码中的字体定义。

## 应用场景

- CLI 工具标题显示
- 终端欢迎信息
- 日志分隔符
- 错误/成功提示
- 应用启动 Banner

---

**测试覆盖**: 完整测试套件，覆盖所有字体、颜色、边框、对齐等功能