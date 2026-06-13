# ANSI Utils 🎨

终端 ANSI 转义码工具模块，提供跨平台的终端样式、光标控制和颜色支持。

## 功能特性

- **256 色和真彩色支持** - 完整的 256 色 palette 和 24 位真彩色
- **文本样式** - 粗体、斜体、下划线、删除线、闪烁等
- **前景/背景色** - 16 种基础色 + 自定义 RGB
- **光标控制** - 移动、隐藏/显示、保存/恢复位置
- **屏幕操作** - 清屏、滚动、光标定位
- **进度条渲染** - 带颜色的终端进度条
- **自动检测** - 自动检测终端颜色支持能力

## 快速开始

```python
from ansi_utils import red, green, blue, bold, on_yellow

# 基础颜色
print(red("错误信息"))
print(green("成功信息"))
print(blue("提示信息"))

# 组合样式
print(bold(on_yellow("重要警告")))

# 自定义颜色 (RGB)
from ansi_utils import colorize
print(colorize("自定义颜色", fg=(255, 128, 0)))

# 彩虹渐变
from ansi_utils import rainbow, gradient
print(rainbow("彩虹文本"))
print(gradient("渐变", start_color=(255, 0, 0), end_color=(0, 0, 255)))
```

## 颜色函数

### 基础颜色

```python
from ansi_utils import (
    red, green, yellow, blue, magenta, cyan, white,
    bright_red, bright_green, bright_yellow, bright_blue,
    bright_magenta, bright_cyan, bright_white, black
)

print(red("红色文本"))
print(bright_green("亮绿色"))
```

### 背景色

```python
from ansi_utils import on_red, on_green, on_blue, on_yellow

print(on_red("红色背景"))
```

### 自定义颜色

```python
from ansi_utils import colorize

# 前景色 (RGB 元组)
print(colorize("文本", fg=(255, 128, 0)))

# 背景色
print(colorize("文本", bg=(0, 0, 128)))

# 同时设置前景和背景
print(colorize("文本", fg=(255, 255, 255), bg=(0, 128, 255)))
```

## 文本样式

```python
from ansi_utils import bold, italic, underline, strikethrough, blink, reverse

print(bold("粗体"))
print(italic("斜体"))
print(underline("下划线"))
print(strikethrough("删除线"))
print(blink("闪烁"))
print(reverse("反色"))
```

## 彩虹和渐变

```python
from ansi_utils import rainbow, gradient

# 彩虹文本
print(rainbow("彩虹🌈"))

# 自定义渐变
print(gradient(
    "渐变文本",
    start_color=(255, 0, 0),
    end_color=(0, 0, 255)
))
```

## 光标控制

```python
from ansi_utils import cursor_move, cursor_hide, cursor_show, cursor_save, cursor_restore

# 移动光标 (行, 列)
cursor_move(10, 1)

# 隐藏/显示光标
cursor_hide()
cursor_show()

# 保存/恢复光标位置
cursor_save()
# ... 做些操作 ...
cursor_restore()
```

## 屏幕操作

```python
from ansi_utils import clear_screen, clear_line, scroll_up, scroll_down

# 清屏
clear_screen()

# 清当前行
clear_line()

# 滚动屏幕
scroll_up()
scroll_down()
```

## 进度条

```python
from ansi_utils import ProgressBar

pb = ProgressBar(total=100, width=50, color='green')
for i in range(100):
    pb.update(i + 1)
```

## 样式链式调用

```python
from ansi_utils import style

result = style("链式调用").red().bold().underline()
print(result)
```

## ANSI 码处理

```python
from ansi_utils import strip_ansi, ansi_length

# 移除 ANSI 码
clean = strip_ansi("\033[1;31m红色\033[0m")  # "红色"

# 计算纯文本长度（不含 ANSI 码）
length = ansi_length("\033[1mHello\033[0m")  # 5
```

## 终端检测

```python
from ansi_utils import supports_color, supports_256color, supports_truecolor

if supports_truecolor():
    print("终端支持 24 位真彩色")
elif supports_256color():
    print("终端支持 256 色")
elif supports_color():
    print("终端支持基本颜色")
```

## 主要函数

| 函数 | 说明 |
|------|------|
| `strip_ansi(text)` | 移除 ANSI 转义码 |
| `colorize(text, fg, bg)` | 自定义颜色渲染 |
| `rainbow(text)` | 彩虹色文本 |
| `gradient(text, start, end)` | 颜色渐变 |
| `supports_color()` | 检测颜色支持 |
| `cursor_move(row, col)` | 移动光标 |
| `clear_screen()` | 清屏 |
| `ProgressBar` | 进度条类 |

## 测试

```bash
python -m pytest Python/ansi_utils/ -v
```

## 许可证

MIT License