"""
Undo/Redo Utils 使用示例

展示 UndoRedoManager 在各种场景下的使用方法。
"""

from undo_redo_utils import (
    UndoRedoManager, SetValueCommand, ListInsertCommand, ListRemoveCommand,
    DictSetCommand, DictDeleteCommand, MacroCommand, SimpleCommand,
    SnapshotManager, Transaction, MementoCommand
)
from dataclasses import dataclass, field
from typing import List, Dict, Any


# ========== 示例 1: 基本撤销/重做 ==========

def example_basic_undo_redo():
    """
    基本的撤销/重做操作示例。
    """
    print("\n=== 示例 1: 基本撤销/重做 ===")
    
    manager = UndoRedoManager()
    counter = {'value': 0}
    
    # 定义一个简单的计数器命令
    class IncrementCommand:
        def __init__(self, counter, amount):
            self.counter = counter
            self.amount = amount
            self.description = f"增加 {amount}"
        
        def execute(self):
            self.counter['value'] += self.amount
            return self.counter['value']
        
        def undo(self):
            self.counter['value'] -= self.amount
            return self.counter['value']
        
        def redo(self):
            return self.execute()
    
    # 执行几个命令
    cmd1 = IncrementCommand(counter, 5)
    cmd1.__class__.__bases__ = (object,)  # 简化
    
    # 使用 SimpleCommand 包装
    def increment(amount):
        counter['value'] += amount
        return counter['value']
    
    def decrement(amount):
        counter['value'] -= amount
        return counter['value']
    
    # 创建并执行命令
    manager.execute(SimpleCommand(
        lambda: increment(10),
        lambda: decrement(10),
        "增加 10"
    ))
    print(f"执行后: counter = {counter['value']}")
    
    manager.execute(SimpleCommand(
        lambda: increment(5),
        lambda: decrement(5),
        "增加 5"
    ))
    print(f"执行后: counter = {counter['value']}")
    
    # 撤销
    manager.undo()
    print(f"撤销后: counter = {counter['value']}")
    
    # 重做
    manager.redo()
    print(f"重做后: counter = {counter['value']}")
    
    # 查看状态
    print(f"可撤销: {manager.can_undo}, 可重做: {manager.can_redo}")
    print(f"撤销栈大小: {manager.undo_count}, 重做栈大小: {manager.redo_count}")


# ========== 示例 2: 对象属性修改 ==========

def example_object_attributes():
    """
    修改对象属性的撤销/重做示例。
    """
    print("\n=== 示例 2: 对象属性修改 ===")
    
    @dataclass
    class Person:
        name: str = ""
        age: int = 0
        email: str = ""
    
    manager = UndoRedoManager()
    person = Person(name="张三", age=25, email="zhangsan@example.com")
    
    print(f"初始状态: {person}")
    
    # 修改姓名
    manager.execute(SetValueCommand(person, 'name', '李四', "修改姓名"))
    print(f"修改姓名后: {person}")
    
    # 修改年龄
    manager.execute(SetValueCommand(person, 'age', 30, "修改年龄"))
    print(f"修改年龄后: {person}")
    
    # 修改邮箱
    manager.execute(SetValueCommand(person, 'email', 'lisi@example.com', "修改邮箱"))
    print(f"修改邮箱后: {person}")
    
    # 撤销所有修改
    manager.undo_all()
    print(f"撤销所有后: {person}")
    
    # 重做所有修改
    manager.redo_all()
    print(f"重做所有后: {person}")


# ========== 示例 3: 列表操作 ==========

def example_list_operations():
    """
    列表增删操作的撤销/重做示例。
    """
    print("\n=== 示例 3: 列表操作 ===")
    
    manager = UndoRedoManager()
    items: List[str] = ['苹果', '香蕉', '橙子']
    
    print(f"初始列表: {items}")
    
    # 在索引 1 处插入
    manager.execute(ListInsertCommand(items, 1, '葡萄', "插入葡萄"))
    print(f"插入后: {items}")
    
    # 删除索引 0 的元素
    manager.execute(ListRemoveCommand(items, 0, "删除苹果"))
    print(f"删除后: {items}")
    
    # 在末尾插入
    manager.execute(ListInsertCommand(items, len(items), '西瓜', "添加西瓜"))
    print(f"添加后: {items}")
    
    # 撤销一步
    manager.undo()
    print(f"撤销一步后: {items}")
    
    # 撤销两步
    manager.undo_n(2)
    print(f"撤销两步后: {items}")
    
    # 重做所有
    manager.redo_all()
    print(f"重做所有后: {items}")


# ========== 示例 4: 字典操作 ==========

def example_dict_operations():
    """
    字典键值操作的撤销/重做示例。
    """
    print("\n=== 示例 4: 字典操作 ===")
    
    manager = UndoRedoManager()
    config: Dict[str, Any] = {
        'theme': 'light',
        'language': 'zh-CN',
        'debug': False
    }
    
    print(f"初始配置: {config}")
    
    # 修改主题
    manager.execute(DictSetCommand(config, 'theme', 'dark', "切换深色主题"))
    print(f"修改主题后: {config}")
    
    # 添加新配置
    manager.execute(DictSetCommand(config, 'fontSize', 14, "设置字体大小"))
    print(f"添加配置后: {config}")
    
    # 删除配置
    manager.execute(DictDeleteCommand(config, 'debug', "关闭调试模式"))
    print(f"删除配置后: {config}")
    
    # 查看可撤销的操作
    print(f"可撤销的操作: {manager.get_undo_descriptions()}")
    
    # 撤销所有
    manager.undo_all()
    print(f"撤销所有后: {config}")


# ========== 示例 5: 批量操作（事务） ==========

def example_transactions():
    """
    使用事务批量执行命令，一次性撤销。
    """
    print("\n=== 示例 5: 批量操作（事务） ===")
    
    manager = UndoRedoManager()
    items: List[int] = []
    
    print(f"初始列表: {items}")
    
    # 使用事务批量添加元素
    with manager.transaction("批量添加 1-5"):
        manager.execute(ListInsertCommand(items, 0, 1))
        manager.execute(ListInsertCommand(items, 1, 2))
        manager.execute(ListInsertCommand(items, 2, 3))
        manager.execute(ListInsertCommand(items, 3, 4))
        manager.execute(ListInsertCommand(items, 4, 5))
    
    print(f"批量添加后: {items}")
    print(f"撤销栈大小: {manager.undo_count}")  # 只有 1 个（事务作为一个整体）
    
    # 单次撤销整个事务
    manager.undo()
    print(f"撤销事务后: {items}")
    
    # 重做整个事务
    manager.redo()
    print(f"重做事务后: {items}")


# ========== 示例 6: 宏命令 ==========

def example_macro_command():
    """
    使用宏命令组合多个操作。
    """
    print("\n=== 示例 6: 宏命令 ===")
    
    manager = UndoRedoManager()
    data = {'value': 0, 'multiplier': 1}
    
    # 创建宏命令
    macro = MacroCommand(description="复合计算操作")
    
    # 添加多个子命令
    macro.add_command(SimpleCommand(
        lambda: (data.update({'value': data['value'] + 10}), data['value'])[1],
        lambda: (data.update({'value': data['value'] - 10}), data['value'])[1],
        "增加 10"
    ))
    
    macro.add_command(SimpleCommand(
        lambda: (data.update({'multiplier': 2}), data['multiplier'])[1],
        lambda: (data.update({'multiplier': 1}), data['multiplier'])[1],
        "乘数翻倍"
    ))
    
    macro.add_command(SimpleCommand(
        lambda: (data.update({'value': data['value'] * data['multiplier']}), data['value'])[1],
        lambda: (data.update({'value': data['value'] // data['multiplier']}), data['value'])[1],
        "应用乘数"
    ))
    
    print(f"初始数据: {data}")
    
    # 执行宏命令
    manager.execute(macro)
    print(f"执行宏命令后: {data}")
    
    # 撤销整个宏命令
    manager.undo()
    print(f"撤销宏命令后: {data}")


# ========== 示例 7: 状态快照管理 ==========

def example_snapshot_manager():
    """
    使用状态快照进行撤销/重做。
    """
    print("\n=== 示例 7: 状态快照管理 ===")
    
    manager = SnapshotManager(max_snapshots=5)
    
    @dataclass
    class GameState:
        level: int = 1
        score: int = 0
        position: tuple = (0, 0)
    
    state = GameState()
    
    # 保存初始状态
    manager.save(state, "游戏开始")
    print(f"初始状态: {state}")
    
    # 玩家移动
    state.position = (10, 5)
    state.score = 100
    manager.save(state, "移动到 (10, 5)")
    print(f"状态 2: {state}")
    
    # 升级
    state.level = 2
    state.score = 500
    manager.save(state, "升到第 2 级")
    print(f"状态 3: {state}")
    
    # 获得更多分数
    state.score = 1000
    manager.save(state, "得分 1000")
    print(f"状态 4: {state}")
    
    print(f"\n快照历史: {manager.get_history()}")
    
    # 撤销到上一状态
    restored = manager.undo()
    print(f"撤销后: level={restored.level}, score={restored.score}, pos={restored.position}")
    
    # 再撤销一步
    restored = manager.undo()
    print(f"再撤销一步: level={restored.level}, score={restored.score}, pos={restored.position}")
    
    # 重做
    restored = manager.redo()
    print(f"重做后: level={restored.level}, score={restored.score}, pos={restored.position}")


# ========== 示例 8: 文本编辑器模拟 ==========

def example_text_editor():
    """
    模拟文本编辑器的撤销/重做功能。
    """
    print("\n=== 示例 8: 文本编辑器模拟 ===")
    
    @dataclass
    class TextEditor:
        content: str = ""
        cursor_pos: int = 0
    
    manager = UndoRedoManager()
    editor = TextEditor(content="Hello World", cursor_pos=5)
    
    print(f"初始内容: '{editor.content}', 光标位置: {editor.cursor_pos}")
    
    # 输入文本
    def insert_text(text, pos):
        old_content = editor.content
        editor.content = editor.content[:pos] + text + editor.content[pos:]
        editor.cursor_pos = pos + len(text)
        return old_content
    
    def remove_text(pos, length):
        removed = editor.content[pos:pos+length]
        editor.content = editor.content[:pos] + editor.content[pos+length:]
        editor.cursor_pos = pos
        return removed
    
    # 插入 "Beautiful "
    manager.execute(SimpleCommand(
        lambda: insert_text("Beautiful ", 6),
        lambda: setattr(editor, 'content', "Hello World") or setattr(editor, 'cursor_pos', 6),
        "插入 'Beautiful '"
    ))
    print(f"插入后: '{editor.content}', 光标位置: {editor.cursor_pos}")
    
    # 删除 "World"
    manager.execute(SimpleCommand(
        lambda: remove_text(16, 5),
        lambda: setattr(editor, 'content', "Hello Beautiful World") or setattr(editor, 'cursor_pos', 16),
        "删除 'World'"
    ))
    print(f"删除后: '{editor.content}', 光标位置: {editor.cursor_pos}")
    
    # 撤销删除
    manager.undo()
    print(f"撤销删除: '{editor.content}', 光标位置: {editor.cursor_pos}")
    
    # 撤销插入
    manager.undo()
    print(f"撤销插入: '{editor.content}', 光标位置: {editor.cursor_pos}")


# ========== 示例 9: 绘图应用模拟 ==========

def example_drawing_app():
    """
    模拟绘图应用的撤销/重做功能。
    """
    print("\n=== 示例 9: 绘图应用模拟 ===")
    
    @dataclass
    class DrawingCanvas:
        shapes: List[Dict] = field(default_factory=list)
        selected_shape: int = -1
    
    manager = UndoRedoManager()
    canvas = DrawingCanvas()
    
    print(f"初始画布: {canvas.shapes}")
    
    # 添加矩形
    manager.execute(ListInsertCommand(
        canvas.shapes, 0,
        {'type': 'rect', 'x': 10, 'y': 10, 'w': 100, 'h': 50},
        "添加矩形"
    ))
    print(f"添加矩形后: {canvas.shapes}")
    
    # 添加圆形
    manager.execute(ListInsertCommand(
        canvas.shapes, 1,
        {'type': 'circle', 'x': 200, 'y': 100, 'r': 30},
        "添加圆形"
    ))
    print(f"添加圆形后: {canvas.shapes}")
    
    # 修改矩形大小
    old_rect = canvas.shapes[0].copy()
    manager.execute(SimpleCommand(
        lambda: canvas.shapes[0].update({'w': 150, 'h': 80}),
        lambda: canvas.shapes[0].update(old_rect),
        "修改矩形大小"
    ))
    print(f"修改矩形后: {canvas.shapes}")
    
    # 撤销所有操作
    manager.undo_all()
    print(f"撤销所有后: {canvas.shapes}")


# ========== 示例 10: 回调事件 ==========

def example_callbacks():
    """
    使用回调事件更新 UI。
    """
    print("\n=== 示例 10: 回调事件 ===")
    
    manager = UndoRedoManager()
    
    # 设置回调
    def on_change():
        print(f"  [状态变化] 可撤销: {manager.can_undo}, 可重做: {manager.can_redo}")
    
    def on_execute(cmd):
        print(f"  [执行] {cmd.description}")
    
    def on_undo(cmd):
        print(f"  [撤销] {cmd.description}")
    
    def on_redo(cmd):
        print(f"  [重做] {cmd.description}")
    
    manager.on_change(on_change)
    manager.on_execute(on_execute)
    manager.on_undo(on_undo)
    manager.on_redo(on_redo)
    
    counter = {'value': 0}
    
    print("执行命令:")
    manager.execute(SimpleCommand(
        lambda: counter.update({'value': counter['value'] + 1}) or counter['value'],
        lambda: counter.update({'value': counter['value'] - 1}) or counter['value'],
        "增加计数"
    ))
    
    print("\n撤销命令:")
    manager.undo()
    
    print("\n重做命令:")
    manager.redo()


# ========== 运行所有示例 ==========

def run_all_examples():
    """
    运行所有示例。
    """
    print("=" * 60)
    print("Undo/Redo Utils 使用示例")
    print("=" * 60)
    
    example_basic_undo_redo()
    example_object_attributes()
    example_list_operations()
    example_dict_operations()
    example_transactions()
    example_macro_command()
    example_snapshot_manager()
    example_text_editor()
    example_drawing_app()
    example_callbacks()
    
    print("\n" + "=" * 60)
    print("所有示例完成!")
    print("=" * 60)


if __name__ == '__main__':
    run_all_examples()