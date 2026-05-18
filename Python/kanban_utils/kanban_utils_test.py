"""
Kanban Board Utilities 测试

测试覆盖:
- 看板创建和配置
- 列管理 (WIP 限制)
- 卡片操作 (添加、移动、阻塞、归档)
- 流程指标 (周期时间、交付时间)
- 瓶颈检测
- 累积流图数据生成
- 吞吐量统计
- 导入导出
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from datetime import datetime, timedelta
import json

try:
    from mod import (
        KanbanBoard, Card, Column, CardStatus,
        create_standard_kanban, create_scrum_kanban, calculate_efficiency
    )
except ImportError:
    from kanban_utils.mod import (
        KanbanBoard, Card, Column, CardStatus,
        create_standard_kanban, create_scrum_kanban, calculate_efficiency
    )


def test_result(passed: bool, message: str):
    """输出测试结果"""
    status = "✅ PASS" if passed else "❌ FAIL"
    print(f"{status}: {message}")
    if not passed:
        raise AssertionError(message)


# ==================== 列管理测试 ====================

def test_create_board():
    """测试创建看板"""
    board = KanbanBoard("Test Board")
    
    test_result(board.name == "Test Board", "看板名称正确")
    test_result(len(board.get_columns()) == 0, "新看板没有列")
    test_result(len(board.get_all_cards()) == 0, "新看板没有卡片")


def test_add_column():
    """测试添加列"""
    board = KanbanBoard()
    
    # 添加基本列
    col = board.add_column("To Do", wip_limit=5, is_start=True)
    test_result(col.name == "To Do", "列名称正确")
    test_result(col.wip_limit == 5, "WIP 限制正确")
    test_result(col.is_start == True, "起始列标记正确")
    test_result(col.is_end == False, "终点列标记正确")
    
    # 添加多个列
    board.add_column("In Progress", wip_limit=3)
    board.add_column("Done", is_end=True)
    
    columns = board.get_columns()
    test_result(len(columns) == 3, "列数量正确")
    test_result(columns[0].name == "To Do", "第一列顺序正确")
    test_result(columns[2].name == "Done", "最后一列顺序正确")


def test_remove_column():
    """测试移除列"""
    board = KanbanBoard()
    board.add_column("Backlog")
    board.add_column("Done")
    
    # 添加卡片
    board.add_card("1", "Task 1", "Backlog")
    
    # 移除列
    result = board.remove_column("Backlog")
    test_result(result == True, "移除列成功")
    test_result(len(board.get_columns()) == 1, "列数量减少")
    test_result(board.get_card("1").status == CardStatus.ARCHIVED, "卡片被归档")
    
    # 移除不存在的列
    result = board.remove_column("NonExistent")
    test_result(result == False, "移除不存在的列返回 False")


def test_wip_limit():
    """测试 WIP 限制"""
    board = KanbanBoard()
    board.add_column("In Progress", wip_limit=2)
    
    board.add_card("1", "Task 1", "In Progress")
    board.add_card("2", "Task 2", "In Progress")
    
    col = board.get_column("In Progress")
    test_result(col.count() == 2, "卡片数量正确")
    test_result(col.is_over_wip() == False, "未超过 WIP 限制")
    test_result(col.wip_remaining() == 0, "剩余容量为 0")
    
    board.add_card("3", "Task 3", "In Progress")
    test_result(col.is_over_wip() == True, "超过 WIP 限制")
    test_result(col.wip_remaining() == 0, "超限时剩余容量仍为 0")


def test_set_wip_limit():
    """测试设置 WIP 限制"""
    board = KanbanBoard()
    board.add_column("In Progress", wip_limit=3)
    
    result = board.set_wip_limit("In Progress", 5)
    test_result(result == True, "设置 WIP 限制成功")
    test_result(board.get_column("In Progress").wip_limit == 5, "WIP 限制更新正确")
    
    result = board.set_wip_limit("NonExistent", 5)
    test_result(result == False, "设置不存在列的 WIP 限制返回 False")


def test_start_end_columns():
    """测试起始和终点列"""
    board = KanbanBoard()
    board.add_column("Backlog", is_start=True)
    board.add_column("WIP")
    board.add_column("Done", is_end=True)
    
    test_result(board.get_start_column().name == "Backlog", "获取起始列正确")
    test_result(board.get_end_column().name == "Done", "获取终点列正确")
    
    # 无标记时的默认行为
    board2 = KanbanBoard()
    board2.add_column("First")
    board2.add_column("Last")
    
    test_result(board2.get_start_column().name == "First", "默认起始列为第一列")
    test_result(board2.get_end_column().name == "Last", "默认终点列为最后一列")


# ==================== 卡片管理测试 ====================

def test_add_card():
    """测试添加卡片"""
    board = KanbanBoard()
    board.add_column("To Do")
    
    card = board.add_card("1", "My Task", "To Do", priority=1, tags=["urgent", "bug"])
    
    test_result(card.id == "1", "卡片 ID 正确")
    test_result(card.title == "My Task", "卡片标题正确")
    test_result(card.column == "To Do", "卡片列正确")
    test_result(card.priority == 1, "卡片优先级正确")
    test_result("urgent" in card.tags, "标签正确")
    test_result(card.status == CardStatus.ACTIVE, "卡片状态为活跃")
    test_result(len(card.history) == 1, "历史记录初始化")
    
    # 重复 ID
    try:
        board.add_card("1", "Duplicate", "To Do")
        test_result(False, "重复 ID 应该抛出异常")
    except ValueError:
        test_result(True, "重复 ID 抛出异常正确")
    
    # 不存在的列
    try:
        board.add_card("2", "Task", "NonExistent")
        test_result(False, "不存在的列应该抛出异常")
    except ValueError:
        test_result(True, "不存在的列抛出异常正确")


def test_move_card():
    """测试移动卡片"""
    board = KanbanBoard()
    board.add_column("To Do")
    board.add_column("In Progress")
    board.add_column("Done")
    
    board.add_card("1", "Task", "To Do")
    original_time = board.get_card("1").created_at
    
    # 移动卡片
    result = board.move_card("1", "In Progress")
    test_result(result == True, "移动卡片成功")
    test_result(board.get_card("1").column == "In Progress", "卡片列更新正确")
    test_result(len(board.get_card("1").history) == 2, "历史记录增加")
    
    # 检查列中的卡片
    test_result(len(board.get_cards_by_column("To Do")) == 0, "原列无卡片")
    test_result(len(board.get_cards_by_column("In Progress")) == 1, "目标列有卡片")
    
    # 再次移动
    board.move_card("1", "Done")
    test_result(board.get_card("1").column == "Done", "再次移动正确")
    test_result(len(board.get_card("1").history) == 3, "历史记录正确")
    
    # 移动不存在的卡片
    result = board.move_card("999", "To Do")
    test_result(result == False, "移动不存在卡片返回 False")
    
    # 移动到不存在的列
    result = board.move_card("1", "NonExistent")
    test_result(result == False, "移动到不存在列返回 False")


def test_block_card():
    """测试阻塞卡片"""
    board = KanbanBoard()
    board.add_column("In Progress")
    board.add_card("1", "Task", "In Progress")
    
    result = board.block_card("1", "Waiting for API")
    test_result(result == True, "阻塞卡片成功")
    
    card = board.get_card("1")
    test_result(card.status == CardStatus.BLOCKED, "卡片状态为阻塞")
    test_result(card.blocked_reason == "Waiting for API", "阻塞原因正确")
    test_result(card.blocked_at is not None, "阻塞时间记录")
    
    # 解除阻塞
    result = board.unblock_card("1")
    test_result(result == True, "解除阻塞成功")
    test_result(card.status == CardStatus.ACTIVE, "卡片状态恢复活跃")
    test_result(card.blocked_reason is None, "阻塞原因清除")


def test_archive_card():
    """测试归档卡片"""
    board = KanbanBoard()
    board.add_column("Done")
    board.add_card("1", "Completed Task", "Done")
    
    result = board.archive_card("1")
    test_result(result == True, "归档卡片成功")
    test_result(board.get_card("1").status == CardStatus.ARCHIVED, "卡片状态为归档")
    
    # 归档后不包含在活跃卡片中
    active = board.get_all_cards(include_archived=False)
    test_result(len(active) == 0, "归档卡片不在活跃列表中")


def test_delete_card():
    """测试删除卡片"""
    board = KanbanBoard()
    board.add_column("To Do")
    board.add_card("1", "Task", "To Do")
    
    result = board.delete_card("1")
    test_result(result == True, "删除卡片成功")
    test_result(board.get_card("1") is None, "卡片已删除")
    test_result(len(board.get_cards_by_column("To Do")) == 0, "列中卡片已移除")
    
    # 删除不存在的卡片
    result = board.delete_card("999")
    test_result(result == False, "删除不存在卡片返回 False")


def test_get_cards():
    """测试获取卡片"""
    board = KanbanBoard()
    board.add_column("To Do")
    board.add_column("Done")
    
    board.add_card("1", "Task 1", "To Do", priority=0, tags=["bug"])
    board.add_card("2", "Task 2", "To Do", priority=1, tags=["bug", "urgent"])
    board.add_card("3", "Task 3", "Done", priority=2, tags=["feature"])
    board.archive_card("3")
    
    # 按列获取
    test_result(len(board.get_cards_by_column("To Do")) == 2, "按列获取卡片正确")
    test_result(len(board.get_cards_by_column("Done", include_archived=True)) == 1, "包含归档卡片")
    
    # 获取全部
    test_result(len(board.get_all_cards()) == 2, "获取全部活跃卡片")
    test_result(len(board.get_all_cards(include_archived=True)) == 3, "包含归档卡片")
    
    # 按标签获取
    bugs = board.get_cards_by_tag("bug")
    test_result(len(bugs) == 2, "按标签获取正确")
    
    # 按优先级获取
    urgent = board.get_cards_by_priority(1)
    test_result(len(urgent) == 1, "按优先级获取正确")
    
    # 获取阻塞卡片
    board.block_card("1", "Blocked")
    blocked = board.get_blocked_cards()
    test_result(len(blocked) == 1, "获取阻塞卡片正确")


def test_card_time_in_column():
    """测试卡片在列中停留时间"""
    board = KanbanBoard()
    board.add_column("To Do")
    board.add_column("In Progress")
    
    base_time = datetime(2026, 1, 1, 10, 0)
    card = Card(id="1", title="Task", column="To Do", created_at=base_time)
    
    # 移动卡片
    card.move_to("In Progress", base_time + timedelta(hours=2))
    card.move_to("Done", base_time + timedelta(hours=5))
    
    # 注意：这里 Done 列不存在于 board，但我们测试的是 Card 的方法
    time_in_todo = card.time_in_column("To Do")
    test_result(time_in_todo == timedelta(hours=2), "在 To Do 停留时间正确")
    
    time_in_progress = card.time_in_column("In Progress")
    test_result(time_in_progress == timedelta(hours=3), "在 In Progress 停留时间正确")


# ==================== 流程指标测试 ====================

def test_cycle_time():
    """测试周期时间计算"""
    board = KanbanBoard()
    board.add_column("To Do", is_start=True)
    board.add_column("In Progress")
    board.add_column("Done", is_end=True)
    
    base_time = datetime(2026, 1, 1, 10, 0)
    
    # 创建卡片并手动设置历史
    card = board.add_card("1", "Task", "Done")
    card.created_at = base_time
    card.history = [
        ("To Do", base_time),
        ("In Progress", base_time + timedelta(hours=2)),
        ("Done", base_time + timedelta(hours=5))
    ]
    
    cycle_time = board.calculate_cycle_time("1")
    test_result(cycle_time == timedelta(hours=5), "周期时间计算正确")


def test_lead_time():
    """测试交付时间计算"""
    board = KanbanBoard()
    board.add_column("Backlog", is_start=True)
    board.add_column("WIP")
    board.add_column("Done", is_end=True)
    
    base_time = datetime(2026, 1, 1, 10, 0)
    
    card = board.add_card("1", "Task", "Done")
    card.created_at = base_time
    card.history = [
        ("Backlog", base_time),
        ("WIP", base_time + timedelta(hours=3)),
        ("Done", base_time + timedelta(hours=8))
    ]
    
    lead_time = board.calculate_lead_time("1")
    test_result(lead_time == timedelta(hours=8), "交付时间计算正确")


def test_flow_metrics():
    """测试流程指标"""
    board = KanbanBoard()
    board.add_column("Backlog", is_start=True)
    board.add_column("WIP")
    board.add_column("Done", is_end=True)
    
    base_time = datetime(2026, 1, 1, 10, 0)
    
    # 创建已完成的卡片
    for i in range(3):
        card = board.add_card(str(i), f"Task {i}", "Done")
        card.created_at = base_time - timedelta(hours=(i+1)*10)
        card.history = [
            ("Backlog", base_time - timedelta(hours=(i+1)*10)),
            ("WIP", base_time - timedelta(hours=(i+1)*10 - 2)),
            ("Done", base_time - timedelta(hours=(i+1)*10 - 8))
        ]
    
    # 创建活跃卡片
    board.add_card("4", "Active Task", "WIP")
    board.add_card("5", "Blocked Task", "WIP")
    board.block_card("5", "Waiting")
    
    metrics = board.get_flow_metrics()
    
    test_result(metrics['total_cards'] == 5, "总卡片数正确")
    test_result(metrics['completed_cards'] == 3, "已完成卡片数正确")
    test_result(metrics['active_cards'] == 4, "活跃卡片数正确")
    test_result(metrics['blocked_cards'] == 1, "阻塞卡片数正确")
    test_result(metrics['cycle_time']['avg_hours'] > 0, "平均周期时间 > 0")
    test_result(metrics['lead_time']['avg_hours'] > 0, "平均交付时间 > 0")


def test_bottleneck_detection():
    """测试瓶颈检测"""
    board = KanbanBoard()
    board.add_column("To Do")
    board.add_column("In Progress", wip_limit=3)
    board.add_column("Done")
    
    # 大部分卡片在 In Progress
    for i in range(10):
        board.add_card(str(i), f"Task {i}", "In Progress")
    for i in range(2):
        board.add_card(str(10+i), f"Task {10+i}", "To Do")
    
    bottlenecks = board.detect_bottlenecks()
    
    test_result(len(bottlenecks) > 0, "检测到瓶颈")
    test_result(bottlenecks[0]['column'] == "In Progress", "瓶颈列正确")
    test_result(bottlenecks[0]['is_wip_violation'] == True, "WIP 违规")


def test_throughput():
    """测试吞吐量统计"""
    board = KanbanBoard()
    board.add_column("Backlog", is_start=True)
    board.add_column("Done", is_end=True)
    
    now = datetime.now()
    
    # 创建最近完成的卡片
    for i in range(5):
        card = board.add_card(str(i), f"Task {i}", "Done")
        card.history = [
            ("Backlog", now - timedelta(days=1, hours=i)),
            ("Done", now - timedelta(hours=i))
        ]
    
    throughput = board.get_throughput(days=7)
    
    test_result(throughput['period_days'] == 7, "统计周期正确")
    test_result(throughput['total_completed'] == 5, "完成数量正确")
    test_result(throughput['average_per_day'] > 0, "日均完成 > 0")


def test_wip_status():
    """测试 WIP 状态"""
    board = KanbanBoard()
    board.add_column("To Do")
    board.add_column("In Progress", wip_limit=2)
    board.add_column("Done")
    
    board.add_card("1", "Task 1", "To Do")
    board.add_card("2", "Task 2", "In Progress")
    board.add_card("3", "Task 3", "In Progress")
    board.add_card("4", "Task 4", "In Progress")  # 超过 WIP
    board.add_card("5", "Task 5", "Done")
    
    status = board.get_wip_status()
    
    test_result(status['To Do']['count'] == 1, "To Do 数量正确")
    test_result(status['In Progress']['count'] == 3, "In Progress 数量正确")
    test_result(status['In Progress']['limit'] == 2, "WIP 限制正确")
    test_result(status['In Progress']['is_over'] == True, "WIP 超限")
    test_result(status['Done']['count'] == 1, "Done 数量正确")


# ==================== 累积流图测试 ====================

def test_cfd_data():
    """测试累积流图数据生成"""
    board = KanbanBoard()
    board.add_column("To Do")
    board.add_column("In Progress")
    board.add_column("Done")
    
    base_time = datetime(2026, 1, 1, 10, 0)
    board._created_at = base_time
    
    # 创建卡片并设置历史
    card1 = board.add_card("1", "Task 1", "Done")
    card1.history = [
        ("To Do", base_time),
        ("In Progress", base_time + timedelta(hours=8)),
        ("Done", base_time + timedelta(hours=16))
    ]
    
    card2 = board.add_card("2", "Task 2", "In Progress")
    card2.history = [
        ("To Do", base_time + timedelta(hours=4)),
        ("In Progress", base_time + timedelta(hours=12))
    ]
    
    cfd_data = board.generate_cfd_data(
        start_date=base_time,
        end_date=base_time + timedelta(hours=24),
        interval_hours=8
    )
    
    test_result(len(cfd_data) > 0, "生成 CFD 数据")
    test_result('To Do' in cfd_data[0], "包含 To Do 列")
    test_result('timestamp' in cfd_data[0], "包含时间戳")


# ==================== 导入导出测试 ====================

def test_to_dict():
    """测试导出为字典"""
    board = KanbanBoard("Test Export")
    board.add_column("To Do", is_start=True)
    board.add_column("Done", is_end=True)
    board.add_card("1", "Task 1", "To Do", tags=["urgent"])
    
    data = board.to_dict()
    
    test_result(data['name'] == "Test Export", "导出名称正确")
    test_result(len(data['columns']) == 2, "导出列数量正确")
    test_result(len(data['cards']) == 1, "导出卡片数量正确")
    test_result(data['cards'][0]['tags'] == ["urgent"], "导出标签正确")


def test_to_json():
    """测试导出为 JSON"""
    board = KanbanBoard("JSON Test")
    board.add_column("To Do")
    board.add_card("1", "Task", "To Do")
    
    json_str = board.to_json()
    data = json.loads(json_str)
    
    test_result(data['name'] == "JSON Test", "JSON 导出名称正确")
    test_result('columns' in data, "JSON 包含列")
    test_result('cards' in data, "JSON 包含卡片")


def test_from_dict():
    """测试从字典导入"""
    data = {
        'name': 'Imported Board',
        'created_at': '2026-01-01T10:00:00',
        'columns': [
            {'name': 'To Do', 'wip_limit': 5, 'order': 0, 'is_start': True, 'is_end': False, 'card_count': 1},
            {'name': 'Done', 'wip_limit': 0, 'order': 1, 'is_start': False, 'is_end': True, 'card_count': 0}
        ],
        'cards': [
            {
                'id': '1',
                'title': 'Imported Task',
                'column': 'To Do',
                'created_at': '2026-01-01T10:00:00',
                'moved_at': None,
                'status': 'active',
                'priority': 1,
                'blocked_reason': None,
                'blocked_at': None,
                'tags': ['imported'],
                'custom_fields': {},
                'history': [['To Do', '2026-01-01T10:00:00']]
            }
        ]
    }
    
    board = KanbanBoard.from_dict(data)
    
    test_result(board.name == "Imported Board", "导入名称正确")
    test_result(len(board.get_columns()) == 2, "导入列数量正确")
    test_result(board.get_card("1").title == "Imported Task", "导入卡片正确")
    test_result('imported' in board.get_card("1").tags, "导入标签正确")


def test_from_json():
    """测试从 JSON 导入"""
    json_str = '''{
        "name": "JSON Import",
        "created_at": "2026-01-01T10:00:00",
        "columns": [
            {"name": "Backlog", "wip_limit": 10, "order": 0, "is_start": true, "is_end": false, "card_count": 0}
        ],
        "cards": []
    }'''
    
    board = KanbanBoard.from_json(json_str)
    
    test_result(board.name == "JSON Import", "JSON 导入名称正确")
    test_result(len(board.get_columns()) == 1, "JSON 导入列正确")


def test_export_import_roundtrip():
    """测试导出再导入"""
    original = KanbanBoard("Roundtrip Test")
    original.add_column("To Do", wip_limit=5, is_start=True)
    original.add_column("In Progress", wip_limit=3)
    original.add_column("Done", is_end=True)
    
    original.add_card("1", "Task 1", "To Do", priority=1, tags=["bug"])
    original.add_card("2", "Task 2", "In Progress")
    original.move_card("2", "Done")
    original.block_card("1", "Blocked")
    
    # 导出再导入
    restored = KanbanBoard.from_dict(original.to_dict())
    
    test_result(restored.name == original.name, "名称一致")
    test_result(len(restored.get_columns()) == len(original.get_columns()), "列数量一致")
    test_result(len(restored.get_all_cards()) == len(original.get_all_cards()), "卡片数量一致")
    test_result(restored.get_card("1").status == CardStatus.BLOCKED, "状态一致")
    test_result(restored.get_card("2").column == "Done", "移动历史一致")


# ==================== 辅助函数测试 ====================

def test_create_standard_kanban():
    """测试创建标准看板"""
    board = create_standard_kanban("My Board")
    
    test_result(board.name == "My Board", "标准看板名称正确")
    columns = board.get_columns()
    test_result(len(columns) == 3, "标准看板有 3 列")
    test_result(columns[0].name == "To Do", "第一列为 To Do")
    test_result(columns[1].name == "In Progress", "第二列为 In Progress")
    test_result(columns[2].name == "Done", "第三列为 Done")
    test_result(columns[1].wip_limit == 3, "In Progress 默认 WIP 为 3")


def test_create_standard_kanban_custom_wip():
    """测试自定义 WIP 的标准看板"""
    board = create_standard_kanban(wip_limits={'To Do': 10, 'In Progress': 5, 'Done': 0})
    
    test_result(board.get_column("To Do").wip_limit == 10, "自定义 To Do WIP")
    test_result(board.get_column("In Progress").wip_limit == 5, "自定义 In Progress WIP")


def test_create_scrum_kanban():
    """测试创建 Scrum 看板"""
    board = create_scrum_kanban("Sprint 1")
    
    test_result(board.name == "Sprint 1", "Scrum 看板名称正确")
    columns = board.get_columns()
    test_result(len(columns) == 6, "Scrum 看板有 6 列")
    test_result(columns[0].name == "Backlog", "第一列为 Backlog")
    test_result(columns[5].name == "Done", "最后一列为 Done")
    test_result(board.get_column("In Progress").wip_limit == 3, "In Progress WIP 限制")


def test_calculate_efficiency():
    """测试效率计算"""
    board = create_standard_kanban()
    board.add_card("1", "Task 1", "In Progress")
    board.add_card("2", "Task 2", "Done")
    board.block_card("1", "Waiting")
    
    efficiency = calculate_efficiency(board)
    
    test_result('flow_efficiency' in efficiency, "包含流程效率")
    test_result('blocked_cards' in efficiency, "包含阻塞卡片数")
    test_result('wip_violations' in efficiency, "包含 WIP 违规数")
    test_result(efficiency['blocked_cards'] == 1, "阻塞卡片数正确")


# ==================== 边界条件测试 ====================

def test_empty_board():
    """测试空看板"""
    board = KanbanBoard()
    
    test_result(len(board.get_columns()) == 0, "空看板无列")
    test_result(len(board.get_all_cards()) == 0, "空看板无卡片")
    test_result(board.get_start_column() is None, "空看板无起始列")
    test_result(board.get_end_column() is None, "空看板无终点列")
    
    metrics = board.get_flow_metrics()
    test_result(metrics['total_cards'] == 0, "空看板指标正确")


def test_card_without_moves():
    """测试从未移动的卡片"""
    board = KanbanBoard()
    board.add_column("To Do", is_start=True)
    board.add_column("Done", is_end=True)
    board.add_card("1", "New Task", "To Do")
    
    cycle_time = board.calculate_cycle_time("1")
    lead_time = board.calculate_lead_time("1")
    
    # 卡片从未完成，时间应该是 None
    test_result(cycle_time is None, "未移动卡片周期时间为 None")
    test_result(lead_time is None, "未移动卡片交付时间为 None")


def test_duplicate_column():
    """测试重复添加列"""
    board = KanbanBoard()
    board.add_column("To Do")
    
    try:
        board.add_column("To Do")
        test_result(False, "重复列应该抛出异常")
    except ValueError:
        test_result(True, "重复列抛出异常正确")


def test_card_equality():
    """测试卡片属性"""
    board = KanbanBoard()
    board.add_column("To Do")
    
    now = datetime.now()
    card = Card(
        id="test-1",
        title="Test Card",
        column="To Do",
        created_at=now,
        priority=2,
        tags=["important"],
        custom_fields={"estimate": 5}
    )
    
    test_result(card.id == "test-1", "卡片 ID 正确")
    test_result(card.title == "Test Card", "卡片标题正确")
    test_result(card.created_at == now, "创建时间正确")
    test_result(card.priority == 2, "优先级正确")
    test_result("important" in card.tags, "标签正确")
    test_result(card.custom_fields["estimate"] == 5, "自定义字段正确")


def test_column_card_management():
    """测试列的卡片管理"""
    col = Column("Test", wip_limit=2)
    
    card1 = Card("1", "Task 1", "Test")
    card2 = Card("2", "Task 2", "Test")
    
    col.add_card(card1)
    col.add_card(card2)
    
    test_result(col.count() == 2, "列卡片计数正确")
    test_result(len(col.get_cards()) == 2, "获取列卡片正确")
    
    removed = col.remove_card("1")
    test_result(removed.id == "1", "移除卡片返回正确")
    test_result(col.count() == 1, "移除后计数正确")
    
    removed = col.remove_card("999")
    test_result(removed is None, "移除不存在卡片返回 None")


def test_card_to_dict():
    """测试卡片转字典"""
    card = Card(
        id="dict-test",
        title="Dict Test",
        column="To Do",
        priority=1,
        tags=["test"],
        custom_fields={"key": "value"}
    )
    
    data = card.to_dict()
    
    test_result(data['id'] == "dict-test", "字典 ID 正确")
    test_result(data['title'] == "Dict Test", "字典标题正确")
    test_result(data['status'] == "active", "字典状态正确")
    test_result(data['priority'] == 1, "字典优先级正确")
    test_result(data['tags'] == ["test"], "字典标签正确")
    test_result(data['custom_fields'] == {"key": "value"}, "字典自定义字段正确")


def test_get_column_counts():
    """测试获取列计数"""
    board = KanbanBoard()
    board.add_column("To Do")
    board.add_column("Done")
    
    board.add_card("1", "Task 1", "To Do")
    board.add_card("2", "Task 2", "To Do")
    board.add_card("3", "Task 3", "Done")
    
    counts = board.get_column_counts()
    
    test_result(counts['To Do'] == 2, "To Do 计数正确")
    test_result(counts['Done'] == 1, "Done 计数正确")


def test_card_with_history():
    """测试带历史记录的卡片"""
    board = KanbanBoard()
    board.add_column("A", is_start=True)
    board.add_column("B")
    board.add_column("C", is_end=True)
    
    base_time = datetime(2026, 1, 1, 10, 0)
    card = board.add_card("hist-1", "History Task", "C")
    card.created_at = base_time
    card.history = [
        ("A", base_time),
        ("B", base_time + timedelta(hours=1)),
        ("C", base_time + timedelta(hours=3))
    ]
    
    # 计算时间
    time_a = card.time_in_column("A")
    time_b = card.time_in_column("B")
    
    test_result(time_a == timedelta(hours=1), "在 A 列时间正确")
    test_result(time_b == timedelta(hours=2), "在 B 列时间正确")


# ==================== 运行测试 ====================

def run_all_tests():
    """运行所有测试"""
    tests = [
        # 列管理
        ("test_create_board", test_create_board),
        ("test_add_column", test_add_column),
        ("test_remove_column", test_remove_column),
        ("test_wip_limit", test_wip_limit),
        ("test_set_wip_limit", test_set_wip_limit),
        ("test_start_end_columns", test_start_end_columns),
        
        # 卡片管理
        ("test_add_card", test_add_card),
        ("test_move_card", test_move_card),
        ("test_block_card", test_block_card),
        ("test_archive_card", test_archive_card),
        ("test_delete_card", test_delete_card),
        ("test_get_cards", test_get_cards),
        ("test_card_time_in_column", test_card_time_in_column),
        
        # 流程指标
        ("test_cycle_time", test_cycle_time),
        ("test_lead_time", test_lead_time),
        ("test_flow_metrics", test_flow_metrics),
        ("test_bottleneck_detection", test_bottleneck_detection),
        ("test_throughput", test_throughput),
        ("test_wip_status", test_wip_status),
        
        # CFD
        ("test_cfd_data", test_cfd_data),
        
        # 导入导出
        ("test_to_dict", test_to_dict),
        ("test_to_json", test_to_json),
        ("test_from_dict", test_from_dict),
        ("test_from_json", test_from_json),
        ("test_export_import_roundtrip", test_export_import_roundtrip),
        
        # 辅助函数
        ("test_create_standard_kanban", test_create_standard_kanban),
        ("test_create_standard_kanban_custom_wip", test_create_standard_kanban_custom_wip),
        ("test_create_scrum_kanban", test_create_scrum_kanban),
        ("test_calculate_efficiency", test_calculate_efficiency),
        
        # 边界条件
        ("test_empty_board", test_empty_board),
        ("test_card_without_moves", test_card_without_moves),
        ("test_duplicate_column", test_duplicate_column),
        ("test_card_equality", test_card_equality),
        ("test_column_card_management", test_column_card_management),
        ("test_card_to_dict", test_card_to_dict),
        ("test_get_column_counts", test_get_column_counts),
        ("test_card_with_history", test_card_with_history),
    ]
    
    passed = 0
    failed = 0
    
    print("=" * 60)
    print("Kanban Board Utilities 测试")
    print("=" * 60)
    
    for name, test_func in tests:
        try:
            test_func()
            passed += 1
        except AssertionError as e:
            print(f"❌ FAIL: {name} - {e}")
            failed += 1
        except Exception as e:
            print(f"❌ ERROR: {name} - {type(e).__name__}: {e}")
            failed += 1
    
    print("=" * 60)
    print(f"测试结果: {passed} 通过, {failed} 失败, 总计 {passed + failed}")
    print("=" * 60)
    
    return failed == 0


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)