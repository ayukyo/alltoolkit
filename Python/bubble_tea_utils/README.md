# Bubble Tea Utils

Bubble Tea TUI 框架风格的终端 UI 组件工具，零依赖。

## 功能特性

- **组件模型**: Model-Update-View 架构
- **状态管理**: 响应式状态更新
- **键盘事件**: 完整的键盘事件处理
- **动画支持**: 进度条、加载动画
- **布局组件**: Box、List、Table 等布局

## 快速开始

```python
from bubble_tea_utils.mod import Program, Model, Update, View

# 创建简单程序
class MyModel(Model):
    def __init__(self):
        self.counter = 0

def update(msg, model):
    if msg == 'up':
        model.counter += 1
    elif msg == 'down':
        model.counter -= 1
    return model

def view(model):
    return f"计数器: {model.counter}\n↑ 增加 | ↓ 减少 | q 退出"

program = Program(MyModel(), update, view)
program.run()
```

## 使用示例

### 基础组件

```python
from bubble_tea_utils.mod import Box, Text, Center

# 创建 Box 组件
box = Box(
    content="Hello World",
    border="rounded",
    padding=1
)

# 创建居中文本
centered = Center(Text("居中显示"))

# 渲染
print(box.render())
```

### 列表组件

```python
from bubble_tea_utils.mod import List, ListItem

# 创建列表
list_view = List([
    ListItem("选项 1"),
    ListItem("选项 2"),
    ListItem("选项 3"),
])

# 设置选中项
list_view.selected = 0

# 渲染
print(list_view.render())
```

### 进度条

```python
from bubble_tea_utils.mod import ProgressBar

# 创建进度条
progress = ProgressBar(
    total=100,
    current=50,
    width=40,
    style="block"  # block, dots, classic
)

print(progress.render())  # ████████████░░░░░░░░ 50%
```

### 加载动画

```python
from bubble_tea_utils.mod import Spinner

# 创建加载动画
spinner = Spinner(style="dots")  # dots, line, pulse

for frame in spinner.frames():
    print(f"\r{frame} 加载中...", end="")
```

### 表格组件

```python
from bubble_tea_utils.mod import Table, TableColumn

# 创建表格
table = Table(
    columns=[
        TableColumn("名称", width=20),
        TableColumn("值", width=10),
    ],
    rows=[
        ["项目 A", "100"],
        ["项目 B", "200"],
    ]
)

print(table.render())
```

## API 参考

### Model/Update/View

| 函数/类 | 说明 |
|---------|------|
| `Model` | 状态模型基类 |
| `update(msg, model)` | 更新函数 |
| `view(model)` | 渲染函数 |
| `Program` | 程序运行器 |

### Box/Text/Center

| 组件 | 说明 |
|------|------|
| `Box(content, border, padding)` | 边框容器 |
| `Text(content)` | 文本组件 |
| `Center(content)` | 居中容器 |

### List/Table

| 组件 | 说明 |
|------|------|
| `List(items)` | 列表组件 |
| `Table(columns, rows)` | 表格组件 |

### ProgressBar/Spinner

| 组件 | 说明 |
|------|------|
| `ProgressBar(total, current, width)` | 进度条 |
| `Spinner(style)` | 加载动画 |

---

**测试覆盖**: 完整测试套件，覆盖组件渲染、布局、动画等