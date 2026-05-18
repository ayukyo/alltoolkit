# kanban_utils - 看板管理工具库

看板（Kanban）状态管理工具，提供完整的看板功能实现，包括列管理、WIP 限制、流程指标分析和瓶颈检测。

## 功能特性

- ✅ **看板状态管理** - 创建、配置、操作看板
- ✅ **列管理** - 添加、移除、设置 WIP 限制
- ✅ **卡片操作** - 添加、移动、阻塞、归档、删除
- ✅ **流程指标** - 周期时间、交付时间、吞吐量
- ✅ **瓶颈检测** - 自动识别瓶颈列和 WIP 违规
- ✅ **累积流图** - CFD 数据生成
- ✅ **效率分析** - 流程效率、阻塞统计
- ✅ **导入导出** - JSON 序列化与反序列化
- ✅ **预设模板** - 标准看板、Scrum 看板

## 零依赖

仅使用 Python 标准库，无需任何外部依赖。

## 快速开始

### 创建看板

```python
from kanban_utils.mod import create_standard_kanban, create_scrum_kanban

# 创建标准看板 (To Do -> In Progress -> Done)
board = create_standard_kanban("我的项目")

# 创建 Scrum 看板 (6 列完整流程)
scrum_board = create_scrum_kanban("Sprint 23")

# 自定义看板
from kanban_utils.mod import KanbanBoard

board = KanbanBoard("企业看板")
board.add_column("需求", wip_limit=5, is_start=True)
board.add_column("开发", wip_limit=3)
board.add_column("测试", wip_limit=2)
board.add_column("上线", is_end=True)
```

### 卡片操作

```python
# 添加卡片
board.add_card("T-1", "用户认证功能", "需求", priority=1, tags=["backend"])

# 移动卡片
board.move_card("T-1", "开发")

# 阻塞卡片
board.block_card("T-1", "等待 API 文档")

# 解除阻塞
board.unblock_card("T-1")

# 归档卡片
board.archive_card("T-1")

# 删除卡片
board.delete_card("T-1")
```

### WIP 管理

```python
# 设置 WIP 限制
board.set_wip_limit("开发", 3)

# 检查 WIP 状态
wip_status = board.get_wip_status()
for column, status in wip_status.items():
    if status['is_over']:
        print(f"{column} 超过 WIP 限制!")
```

### 流程指标

```python
# 获取流程指标
metrics = board.get_flow_metrics()

print(f"平均周期时间: {metrics['cycle_time']['avg_hours']} 小时")
print(f"P85 周期时间: {metrics['cycle_time']['p85_hours']} 小时")
print(f"平均交付时间: {metrics['lead_time']['avg_hours']} 小时")

# 吞吐量统计
throughput = board.get_throughput(days=7)
print(f"日均完成: {throughput['average_per_day']} 张")
```

### 瓶颈检测

```python
bottlenecks = board.detect_bottlenecks()
for bn in bottlenecks:
    print(f"瓶颈列: {bn['column']}")
    print(f"卡片数: {bn['count']} (平均 {bn['average']})")
    if bn['is_wip_violation']:
        print("⚠️ WIP 违规!")
```

### 累积流图

```python
from datetime import datetime, timedelta

cfd_data = board.generate_cfd_data(
    start_date=datetime.now() - timedelta(days=7),
    end_date=datetime.now(),
    interval_hours=24
)

for point in cfd_data:
    print(f"{point['timestamp']}: {point}")
```

### 导入导出

```python
# 导出为 JSON
json_str = board.to_json()

# 从 JSON 导入
restored = KanbanBoard.from_json(json_str)

# 导出为字典
data = board.to_dict()

# 从字典导入
restored = KanbanBoard.from_dict(data)
```

## 核心 API

### KanbanBoard

主要类，管理看板状态。

| 方法 | 说明 |
|------|------|
| `add_column(name, wip_limit, is_start, is_end)` | 添加列 |
| `remove_column(name)` | 移除列 |
| `get_column(name)` | 获取列 |
| `get_columns()` | 获取所有列 |
| `set_wip_limit(name, limit)` | 设置 WIP 限制 |
| `add_card(id, title, column, priority, tags, custom_fields)` | 添加卡片 |
| `get_card(id)` | 获取卡片 |
| `move_card(id, to_column)` | 移动卡片 |
| `block_card(id, reason)` | 阻塞卡片 |
| `unblock_card(id)` | 解除阻塞 |
| `archive_card(id)` | 归档卡片 |
| `delete_card(id)` | 删除卡片 |
| `get_cards_by_column(column)` | 获取列内卡片 |
| `get_all_cards()` | 获取所有卡片 |
| `get_blocked_cards()` | 获取阻塞卡片 |
| `get_cards_by_tag(tag)` | 按标签获取 |
| `get_cards_by_priority(priority)` | 按优先级获取 |
| `get_wip_status()` | WIP 状态 |
| `detect_bottlenecks()` | 瓶颈检测 |
| `calculate_cycle_time(card_id)` | 周期时间 |
| `calculate_lead_time(card_id)` | 交付时间 |
| `get_flow_metrics()` | 流程指标 |
| `get_throughput(days)` | 吞吐量统计 |
| `generate_cfd_data(...)` | CFD 数据 |
| `to_json()` / `from_json()` | JSON 导入导出 |

### Card

卡片类，包含属性和历史记录。

| 属性 | 说明 |
|------|------|
| `id` | 卡片 ID |
| `title` | 卡片标题 |
| `column` | 当前列 |
| `status` | 状态 (ACTIVE/BLOCKED/ARCHIVED) |
| `priority` | 优先级 (0=普通, 1=高, 2=紧急) |
| `tags` | 标签列表 |
| `custom_fields` | 自定义字段 |
| `history` | 移动历史 [(column, timestamp), ...] |

### Column

列类，管理列状态和 WIP。

| 属性/方法 | 说明 |
|------------|------|
| `name` | 列名称 |
| `wip_limit` | WIP 限制 (0=无限制) |
| `is_start` | 是否为起始列 |
| `is_end` | 是否为终点列 |
| `count()` | 卡片数量 |
| `is_over_wip()` | 是否超 WIP |
| `wip_remaining()` | 剩余容量 |

### 辅助函数

```python
create_standard_kanban(name, wip_limits)  # 标准看板
create_scrum_kanban(name, wip_limits)     # Scrum 看板
calculate_efficiency(board)               # 效率分析
```

## 使用场景

1. **个人任务管理** - 使用标准看板跟踪个人任务
2. **团队协作** - Scrum 看板管理 Sprint 任务
3. **流程分析** - 流程指标分析团队效率
4. **瓶颈识别** - 自动检测流程瓶颈
5. **数据可视化** - CFD 数据用于图表展示
6. **项目报告** - 导出看板状态用于报告

## 测试

运行测试：

```bash
python Python/kanban_utils/kanban_utils_test.py
```

测试覆盖：
- 看板创建和配置
- 列管理（WIP 限制）
- 卡片操作（添加、移动、阻塞、归档）
- 流程指标（周期时间、交付时间）
- 瓶颈检测
- CFD 数据生成
- 导入导出
- 边界条件

## 示例

运行示例：

```bash
python Python/kanban_utils/examples/usage_examples.py
```

包含 10 个详细示例：
1. 创建基本看板
2. 卡片操作
3. WIP 管理
4. 流程指标分析
5. 瓶颈检测
6. CFD 数据生成
7. 导入导出
8. 效率分析
9. 自定义字段
10. 看板类型对比

## 文件结构

```
Python/kanban_utils/
├── mod.py              # 主模块
├── kanban_utils_test.py # 测试文件
├── README.md           # 文档
└── examples/
    └── usage_examples.py # 使用示例
```

## 版本历史

- **v1.0.0** (2026-05-19) - 初始版本
  - 看板状态管理
  - 列管理（WIP 限制）
  - 卡片操作
  - 流程指标
  - 瓶颈检测
  - CFD 数据生成
  - 导入导出
  - 预设模板

## 许可证

MIT License