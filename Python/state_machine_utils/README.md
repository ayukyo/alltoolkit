# State Machine Utils


State Machine Utils - 零依赖状态机工具库

提供完整的状态机实现，包括：
- 状态定义和转换规则
- 条件转换验证
- 进入/退出状态回调
- 状态历史记录
- 异步状态转换
- 状态持久化和恢复


## 功能

### 类

- **TransitionError**: 状态转换错误
- **StateError**: 状态错误
- **Transition**: 状态转换定义
  方法: check_condition, execute_action
- **StateConfig**: 状态配置
  方法: enter, exit
- **StateRecord**: 状态历史记录
  方法: to_dict
- **StateMachine**: 状态机核心类

示例:
    sm = StateMachine('idle')
    sm
  方法: current_state, context, history, is_final, add_state ... (18 个方法)
- **HierarchicalStateMachine**: 层次状态机

支持嵌套状态，形成状态层次结构
  方法: add_substate, get_parent, get_children, get_state_path, is_in_state ... (7 个方法)
- **StateMachineBuilder**: 状态机构建器

使用流式 API 构建状态机
  方法: initial, state, transition, with_history, build

### 函数

- **create_order_state_machine(**) - 创建订单状态机
- **create_task_state_machine(**) - 创建任务状态机
- **create_game_character_state_machine(**) - 创建游戏角色状态机
- **create_tcp_connection_state_machine(**) - 创建 TCP 连接状态机
- **check_condition(self**) - 检查转换条件
- **execute_action(self**) - 执行转换动作
- **enter(self**) - 进入状态时执行
- **exit(self**) - 退出状态时执行
- **to_dict(self**)
- **current_state(self**) - 当前状态

... 共 39 个函数

## 使用示例

```python
from mod import create_order_state_machine

# 使用 create_order_state_machine
result = create_order_state_machine()
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
