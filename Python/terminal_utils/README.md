# Terminal Utils


Terminal Utilities - 终端控制工具集
零外部依赖的终端控制库，提供颜色输出、光标控制、进度条、表格等功能


## 功能

### 类

- **Color**: ANSI 颜色枚举
- **Style**: ANSI 样式枚举
- **TerminalSize**: 终端尺寸
- **Cursor**: 光标控制类
  方法: hide, show, move_to, move_up, move_down ... (10 个方法)
- **Ansi**: ANSI 转义序列处理类
  方法: color, strip, length
- **ProgressBar**: 终端进度条

支持多种样式、自定义填充字符、预估剩余时间等
  方法: start, update, set_progress
- **Spinner**: 终端加载动画

支持多种动画样式
  方法: start, update, stop, advance
- **Table**: 终端表格

支持多种边框样式、自动列宽、对齐等
  方法: add_row, render, print
- **TerminalMenu**: 终端交互菜单

支持键盘导航、多选等
  方法: select
- **Box**: 终端文本框

支持多种边框样式
  方法: render, print

### 函数

- **supports_color(**) - 检测终端是否支持颜色
- **get_terminal_size(**) - 获取终端尺寸
- **clear_screen(**) - 清屏
- **clear_line(mode**) - 清除当前行
- **red(text**)
- **green(text**)
- **yellow(text**)
- **blue(text**)
- **magenta(text**)
- **cyan(text**)

... 共 48 个函数

## 使用示例

```python
from mod import supports_color

# 使用 supports_color
result = supports_color()
```

## 测试

运行测试：

```bash
python *_test.py
```

## 文件结构

```
{module_name}/
├── mod.py              # 主模块
├── *_test.py           # 测试文件
├── README.md           # 本文档
└── examples/           # 示例代码
    └── usage_examples.py
```

---

**Last updated**: 2026-04-28
