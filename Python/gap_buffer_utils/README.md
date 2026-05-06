# Gap Buffer Utils

Gap Buffer 数据结构实现 - 专为文本编辑器优化的高效数据结构。

## 简介

间隙缓冲区（Gap Buffer）是一种动态数组，在当前位置保留一个"间隙"（空空间），允许在光标位置进行高效的插入和删除操作。这使得它成为文本编辑器的理想选择，因为大多数编辑发生在光标附近。

## 特性

- **高效编辑**: 在光标位置插入/删除 O(1) 时间复杂度
- **完整功能**: 支持撤销/重做、选择、行/词导航
- **零依赖**: 仅使用 Python 标准库
- **完整测试**: 66 个单元测试覆盖所有功能

## 时间复杂度

| 操作 | 复杂度 |
|------|--------|
| 光标位置插入 | O(1) amortized |
| 光标位置删除 | O(1) |
| 移动光标 | O(k) k为移动距离 |
| 随机访问 | O(1) |

## 快速开始

### 基本使用

```python
from mod import GapBuffer

# 创建缓冲区
buf = GapBuffer(text="Hello")

# 插入文本
buf.insert(" World")
print(buf)  # "Hello World"

# 移动光标并插入
buf.move_cursor(5)
buf.insert(",")
print(buf)  # "Hello, World"

# 删除文本
buf.delete(6)  # 删除 ", World"
print(buf)  # "Hello"
```

### 撤销/重做

```python
from mod import GapBufferWithHistory

buf = GapBufferWithHistory(text="Hello")
buf.insert(" World")

buf.undo()  # 回退到 "Hello"
buf.redo()  # 重做到 "Hello World"
```

### 文本编辑器

```python
from mod import TextEditor

editor = TextEditor(text="Hello World")

# 选择文本
editor.move_cursor(6)
editor.start_selection()
editor.move_cursor(11, extend_selection=True)

# 替换选择
editor.type_text("Universe")
print(editor.text)  # "Hello Universe"

# 撤销
editor.undo()
```

## 主要类

### GapBuffer

基础间隙缓冲区实现：
- `insert(text)` - 在光标位置插入文本
- `delete(count)` - 删除字符（正数向前，负数向后）
- `move_cursor(position)` - 移动光标到指定位置
- `move_cursor_relative(offset)` - 相对移动光标
- `find(text)` / `rfind(text)` - 搜索文本
- `replace(old, new)` - 替换文本
- `line_info()` - 获取行信息
- `goto_line(line_number)` - 跳转到指定行
- `word_info()` - 获取词边界

### GapBufferWithHistory

带撤销/重做支持的缓冲区：
- `undo()` - 撤销上一操作
- `redo()` - 重做已撤销操作
- `can_undo()` / `can_redo()` - 检查可用性
- `begin_group()` / `end_group()` - 操作分组

### TextEditor

完整的文本编辑器接口：
- 选择操作（全选、选词、选行）
- 词/行导航
- 文档导航（开头/结尾）
- 查找功能

## 文件结构

```
gap_buffer_utils/
├── mod.py               # 主模块（~27KB）
├── gap_buffer_utils_test.py  # 测试文件
├── README.md            # 说明文档
└── examples/
    └── usage_examples.py    # 使用示例
```

## 测试

```bash
python -m pytest gap_buffer_utils_test.py -v
```

## 应用场景

- 文本编辑器核心数据结构
- 代码编辑器实现
- 富文本编辑器
- 终端编辑应用
- 实时协作编辑（配合其他机制）

## 设计原理

间隙缓冲区的工作原理：

```
文本: "Hello|World"，光标在位置 5

缓冲区: ['H','e','l','l','o','_','_','_','W','o','r','l','d']
               ↑pre-gap    ↑gap    ↑post-gap
```

- **pre-gap**: 光标前的内容
- **gap**: 用于插入的空空间
- **post-gap**: 光标后的内容

当光标移动时，间隙随之移动，通过复制相邻字符。插入填充间隙，删除扩展间隙。

## 作者

AllToolkit 自动生成 - 2026-05-07