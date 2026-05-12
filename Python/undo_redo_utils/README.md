# Undo/Redo Utils - 撤销/重做工具库

一个完整的 Python 撤销/重做实现，基于 Command 模式和 Memento 模式。

## 功能特性

- **Command 模式实现**: 完整的命令执行、撤销、重做接口
- **多种命令类型**: 支持 SetValue、ListInsert/Remove、DictSet/Delete 等常用操作
- **事务支持**: 使用 `with` 语法批量执行命令，一次性撤销
- **宏命令**: 组合多个命令为一个整体
- **状态快照**: 基于 Memento 模式的状态管理
- **内存限制**: 可配置最大撤销/重做栈大小
- **回调事件**: 支持状态变化、执行、撤销、重做回调
- **零外部依赖**: 仅使用 Python 标准库

## 快速开始

### 基本使用

```python
from undo_redo_utils import UndoRedoManager, SetValueCommand

# 创建管理器
manager = UndoRedoManager()

# 创建一个对象
class Person:
    name = "张三"
    age = 25

person = Person()

# 执行命令
manager.execute(SetValueCommand(person, 'name', '李四', "修改姓名"))
print(person.name)  # 输出: 李四

# 撤销
manager.undo()
print(person.name)  # 输出: 张三

# 重做
manager.redo()
print(person.name)  # 输出: 李四
```

### 列表操作

```python
from undo_redo_utils import UndoRedoManager, ListInsertCommand, ListRemoveCommand

manager = UndoRedoManager()
items = ['苹果', '香蕉', '橙子']

# 插入元素
manager.execute(ListInsertCommand(items, 1, '葡萄', "插入葡萄"))
print(items)  # ['苹果', '葡萄', '香蕉', '橙子']

# 删除元素
manager.execute(ListRemoveCommand(items, 0, "删除苹果"))
print(items)  # ['葡萄', '香蕉', '橙子']

# 撤销删除
manager.undo()
print(items)  # ['苹果', '葡萄', '香蕉', '橙子']
```

### 字典操作

```python
from undo_redo_utils import UndoRedoManager, DictSetCommand, DictDeleteCommand

manager = UndoRedoManager()
config = {'theme': 'light', 'debug': False}

# 修改值
manager.execute(DictSetCommand(config, 'theme', 'dark', "切换主题"))
print(config)  # {'theme': 'dark', 'debug': False}

# 删除键
manager.execute(DictDeleteCommand(config, 'debug', "关闭调试"))
print(config)  # {'theme': 'dark'}

# 撤销所有
manager.undo_all()
print(config)  # {'theme': 'light', 'debug': False}
```

### 事务（批量操作）

```python
from undo_redo_utils import UndoRedoManager, ListInsertCommand

manager = UndoRedoManager()
items = []

# 使用事务批量添加
with manager.transaction("批量添加 1-5"):
    manager.execute(ListInsertCommand(items, 0, 1))
    manager.execute(ListInsertCommand(items, 1, 2))
    manager.execute(ListInsertCommand(items, 2, 3))
    manager.execute(ListInsertCommand(items, 3, 4))
    manager.execute(ListInsertCommand(items, 4, 5))

print(items)  # [1, 2, 3, 4, 5]
print(manager.undo_count)  # 1（整个事务作为一个单元）

# 一次撤销整个事务
manager.undo()
print(items)  # []
```

### 状态快照管理

```python
from undo_redo_utils import SnapshotManager

manager = SnapshotManager(max_snapshots=10)

# 创建游戏状态
game_state = {'level': 1, 'score': 0, 'position': (0, 0)}

# 保存状态
manager.save(game_state, "游戏开始")

# 玩家移动
game_state['position'] = (10, 5)
game_state['score'] = 100
manager.save(game_state, "移动到 (10, 5)")

# 升级
game_state['level'] = 2
manager.save(game_state, "升到第 2 级")

# 撤销到上一状态
restored = manager.undo()
print(restored)  # {'level': 1, 'score': 100, 'position': (10, 5)}
```

### 回调事件

```python
from undo_redo_utils import UndoRedoManager

manager = UndoRedoManager()

# 设置回调
manager.on_change(lambda: print(f"状态变化"))
manager.on_execute(lambda cmd: print(f"执行: {cmd.description}"))
manager.on_undo(lambda cmd: print(f"撤销: {cmd.description}"))
manager.on_redo(lambda cmd: print(f"重做: {cmd.description}"))
```

## 核心 API

### UndoRedoManager

主要管理器类，提供完整的撤销/重做功能。

| 方法 | 说明 |
|------|------|
| `execute(command)` | 执行命令并添加到撤销栈 |
| `undo()` | 撤销上一个命令 |
| `redo()` | 重做上一个撤销的命令 |
| `undo_n(n)` | 撤销 n 个命令 |
| `redo_n(n)` | 重做 n 个命令 |
| `undo_all()` | 撤销所有命令 |
| `redo_all()` | 重做所有命令 |
| `transaction(description)` | 创建事务上下文 |
| `clear()` | 清空所有历史 |
| `can_undo` | 是否可撤销 |
| `can_redo` | 是否可重做 |
| `undo_count` | 可撤销命令数 |
| `redo_count` | 可重做命令数 |

### 命令类型

| 命令 | 说明 |
|------|------|
| `SimpleCommand` | 简单命令，使用函数实现 |
| `SetValueCommand` | 设置对象属性值 |
| `ListInsertCommand` | 列表插入元素 |
| `ListRemoveCommand` | 列表删除元素 |
| `DictSetCommand` | 字典设置键值 |
| `DictDeleteCommand` | 字典删除键 |
| `MementoCommand` | 基于 Memento 模式的命令 |
| `MacroCommand` | 组合多个命令的宏命令 |

### SnapshotManager

基于状态快照的管理器。

| 方法 | 说明 |
|------|------|
| `save(state, description)` | 保存状态快照 |
| `undo()` | 恢复到上一个快照 |
| `redo()` | 恢复到下一个快照 |
| `current()` | 获取当前状态 |
| `get_history()` | 获取快照历史描述列表 |
| `clear()` | 清空所有快照 |

## 测试

运行测试：

```bash
python -m pytest undo_redo_utils_test.py -v
```

## 示例

运行示例：

```bash
python examples.py
```

## 适用场景

- 文本编辑器（撤销/重做编辑操作）
- 绘图应用（撤销/重做绘图操作）
- 表单编辑（撤销/重做表单数据修改）
- 游戏状态管理（撤销/重做游戏状态）
- 配置管理（撤销/重做配置修改）

## 文件结构

```
undo_redo_utils/
├── undo_redo_utils.py      # 主模块
├── undo_redo_utils_test.py # 单元测试 (47 个测试)
├── examples.py             # 使用示例 (10 个场景)
└── README.md               # 说明文档
```

## 许可证

MIT License