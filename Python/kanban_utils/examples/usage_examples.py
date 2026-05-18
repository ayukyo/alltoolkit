"""
Kanban Board Utilities 使用示例

展示:
- 创建标准看板
- 卡片操作
- WIP 限制管理
- 流程指标分析
- 瓶颈检测
- 累积流图
- 导入导出
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from datetime import datetime, timedelta

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


def example_1_create_basic_board():
    """示例 1: 创建基本看板"""
    print("\n" + "=" * 50)
    print("示例 1: 创建基本看板")
    print("=" * 50)
    
    # 使用辅助函数创建标准看板
    board = create_standard_kanban("我的项目看板")
    
    print(f"看板名称: {board.name}")
    print("列:")
    for col in board.get_columns():
        print(f"  - {col.name} (WIP: {col.wip_limit or '无限制'})")
    
    # 添加卡片
    board.add_card("T-1", "设计首页", "To Do", priority=1, tags=["design"])
    board.add_card("T-2", "实现登录功能", "To Do", priority=2, tags=["backend"])
    board.add_card("T-3", "编写测试", "To Do", tags=["testing"])
    
    print("\n卡片列表:")
    for card in board.get_all_cards():
        print(f"  - [{card.id}] {card.title} ({card.column})")


def example_2_card_operations():
    """示例 2: 卡片操作"""
    print("\n" + "=" * 50)
    print("示例 2: 卡片操作")
    print("=" * 50)
    
    board = create_standard_kanban()
    board.add_card("T-1", "任务1", "To Do")
    board.add_card("T-2", "任务2", "To Do")
    board.add_card("T-3", "任务3", "To Do")
    
    print("初始状态:")
    for col in board.get_columns():
        cards = board.get_cards_by_column(col.name)
        print(f"  {col.name}: {len(cards)} 张卡片")
    
    # 移动卡片
    board.move_card("T-1", "In Progress")
    print("\n移动 T-1 到 In Progress 后:")
    for col in board.get_columns():
        cards = board.get_cards_by_column(col.name)
        print(f"  {col.name}: {[c.id for c in cards]}")
    
    # 阻塞卡片
    board.block_card("T-1", "等待 API 文档")
    print(f"\n阻塞 T-1: {board.get_card('T-1').blocked_reason}")
    
    # 解除阻塞并完成
    board.unblock_card("T-1")
    board.move_card("T-1", "Done")
    print(f"完成 T-1 后的位置: {board.get_card('T-1').column}")
    
    # 查看历史
    print("\nT-1 的移动历史:")
    for col, time in board.get_card("T-1").history:
        print(f"  {col} @ {time.strftime('%H:%M:%S')}")


def example_3_wip_management():
    """示例 3: WIP 限制管理"""
    print("\n" + "=" * 50)
    print("示例 3: WIP 限制管理")
    print("=" * 50)
    
    # 创建带 WIP 限制的看板
    board = KanbanBoard("严格 WIP 看板")
    board.add_column("Backlog", wip_limit=0, is_start=True)
    board.add_column("Analysis", wip_limit=2)
    board.add_column("Development", wip_limit=3)
    board.add_column("Testing", wip_limit=2)
    board.add_column("Done", wip_limit=0, is_end=True)
    
    # 添加卡片
    for i in range(8):
        board.add_card(f"T-{i}", f"任务{i}", "Backlog")
    
    # 尝试移动到受限列
    print("尝试移动 4 张卡片到 Analysis (WIP=2):")
    for i in range(4):
        board.move_card(f"T-{i}", "Analysis")
    
    # 检查 WIP 状态
    wip_status = board.get_wip_status()
    for col, status in wip_status.items():
        indicator = "⚠️ 超限!" if status['is_over'] else "✅"
        print(f"  {col}: {status['count']}/{status['limit']} {indicator}")
    
    print("\nWIP 违规列:")
    for col, status in wip_status.items():
        if status['is_over']:
            print(f"  - {col}: 超出 {status['count'] - status['limit']} 张")


def example_4_flow_metrics():
    """示例 4: 流程指标分析"""
    print("\n" + "=" * 50)
    print("示例 4: 流程指标分析")
    print("=" * 50)
    
    board = create_scrum_kanban("Sprint 23")
    
    # 创建已完成的任务
    base_time = datetime.now() - timedelta(days=7)
    
    for i in range(5):
        card = board.add_card(f"S-{i}", f"Sprint 任务{i}", "Done")
        card.created_at = base_time + timedelta(hours=i*4)
        card.history = [
            ("Backlog", base_time + timedelta(hours=i*4)),
            ("Sprint Backlog", base_time + timedelta(hours=i*4 + 2)),
            ("In Progress", base_time + timedelta(hours=i*4 + 4)),
            ("Testing", base_time + timedelta(hours=i*4 + 20)),
            ("Done", base_time + timedelta(hours=i*4 + 24))
        ]
    
    # 获取流程指标
    metrics = board.get_flow_metrics()
    
    print("流程指标:")
    print(f"  总卡片数: {metrics['total_cards']}")
    print(f"  已完成: {metrics['completed_cards']}")
    print(f"  活跃: {metrics['active_cards']}")
    print(f"  阻塞: {metrics['blocked_cards']}")
    
    print("\n周期时间 (小时):")
    ct = metrics['cycle_time']
    print(f"  平均: {ct['avg_hours']:.1f}")
    print(f"  最小: {ct['min_hours']:.1f}")
    print(f"  最大: {ct['max_hours']:.1f}")
    print(f"  P50: {ct['p50_hours']:.1f}")
    print(f"  P85: {ct['p85_hours']:.1f}")
    print(f"  P95: {ct['p95_hours']:.1f}")
    
    print("\n交付时间 (小时):")
    lt = metrics['lead_time']
    print(f"  平均: {lt['avg_hours']:.1f}")
    print(f"  P50: {lt['p50_hours']:.1f}")
    print(f"  P95: {lt['p95_hours']:.1f}")
    
    # 吞吐量
    throughput = board.get_throughput(days=7)
    print(f"\n吞吐量 (7天):")
    print(f"  完成: {throughput['total_completed']}")
    print(f"  日均: {throughput['average_per_day']}")


def example_5_bottleneck_detection():
    """示例 5: 瓶颈检测"""
    print("\n" + "=" * 50)
    print("示例 5: 瓶颈检测")
    print("=" * 50)
    
    board = create_scrum_kanban()
    
    # 模拟瓶颈: Testing 列堆积
    for i in range(10):
        board.add_card(f"T-{i}", f"任务{i}", "Testing")
    
    for i in range(3):
        board.add_card(f"T-{10+i}", f"任务{10+i}", "In Progress")
    
    for i in range(2):
        board.add_card(f"T-{13+i}", f"任务{13+i}", "Done")
    
    # 检测瓶颈
    bottlenecks = board.detect_bottlenecks()
    
    print("列状态:")
    for col in board.get_columns():
        cards = board.get_cards_by_column(col.name)
        print(f"  {col.name}: {len(cards)} 张")
    
    print("\n检测到的瓶颈:")
    for bn in bottlenecks:
        print(f"  {bn['column']}: {bn['count']} 张 (平均 {bn['average']:.1f}, 比率 {bn['ratio']:.2f})")
        if bn['is_wip_violation']:
            print(f"    ⚠️ WIP 违规!")
    
    print("\n建议:")
    for bn in bottlenecks:
        print(f"  - 关注 {bn['column']} 列的阻塞原因")
        print(f"  - 考虑增加测试资源或调整 WIP 限制")


def example_6_cfd_generation():
    """示例 6: 累积流图数据"""
    print("\n" + "=" * 50)
    print("示例 6: 累积流图数据生成")
    print("=" * 50)
    
    board = create_standard_kanban()
    
    base_time = datetime(2026, 1, 1, 9, 0)
    board._created_at = base_time
    
    # 创建任务历史
    for i in range(5):
        card = board.add_card(f"T-{i}", f"任务{i}", "Done")
        card.history = [
            ("To Do", base_time + timedelta(hours=i*2)),
            ("In Progress", base_time + timedelta(hours=i*2 + 8)),
            ("Done", base_time + timedelta(hours=i*2 + 16))
        ]
    
    # 生成 CFD 数据
    cfd_data = board.generate_cfd_data(
        start_date=base_time,
        end_date=base_time + timedelta(hours=24),
        interval_hours=6
    )
    
    print("累积流图数据 (每 6 小时):")
    print("时间                | To Do | In Progress | Done")
    print("-" * 50)
    
    for point in cfd_data:
        time_str = point['timestamp'].split('T')[1][:5]
        print(f"{time_str}              | {point['To Do']:>5} | {point['In Progress']:>11} | {point['Done']:>4}")
    
    print("\n用于绘制累积流图:")
    print("  - X 轴: 时间")
    print("  - Y 轴: 各列卡片数量")
    print("  - 堆叠区域图展示工作流程")


def example_7_import_export():
    """示例 7: 导入导出"""
    print("\n" + "=" * 50)
    print("示例 7: 导入导出")
    print("=" * 50)
    
    # 创建看板并添加内容
    board = create_standard_kanban("导出演示")
    board.add_card("T-1", "设计", "Done", tags=["design"])
    board.add_card("T-2", "开发", "In Progress", priority=1)
    board.add_card("T-3", "测试", "To Do")
    board.block_card("T-2", "等待依赖")
    
    # 导出为 JSON
    json_str = board.to_json()
    print("导出的 JSON (部分):")
    print(json_str[:500] + "...")
    
    # 从 JSON 导入
    restored = KanbanBoard.from_json(json_str)
    print(f"\n导入成功: {restored.name}")
    print(f"列数: {len(restored.get_columns())}")
    print(f"卡片数: {len(restored.get_all_cards())}")
    
    # 验证阻塞状态保留
    blocked = restored.get_blocked_cards()
    print(f"阻塞卡片: {[c.id for c in blocked]}")
    print(f"T-2 阻塞原因: {restored.get_card('T-2').blocked_reason}")


def example_8_efficiency_analysis():
    """示例 8: 效率分析"""
    print("\n" + "=" * 50)
    print("示例 8: 看板效率分析")
    print("=" * 50)
    
    board = create_scrum_kanban("高效团队")
    
    # 模拟正常流程
    base_time = datetime.now() - timedelta(days=3)
    
    for i in range(10):
        card = board.add_card(f"E-{i}", f"效率任务{i}", "Done")
        card.history = [
            ("Backlog", base_time + timedelta(hours=i)),
            ("In Progress", base_time + timedelta(hours=i + 2)),
            ("Done", base_time + timedelta(hours=i + 8))
        ]
    
    # 添加阻塞
    board.add_card("E-blocked", "阻塞任务", "In Progress")
    board.block_card("E-blocked", "外部依赖")
    
    # 计算效率
    efficiency = calculate_efficiency(board)
    
    print("效率指标:")
    for key, value in efficiency.items():
        print(f"  {key}: {value}")
    
    print("\n健康状态评估:")
    if efficiency['blocked_cards'] > 0:
        print("  ⚠️ 有阻塞卡片，建议优先解决")
    if efficiency['wip_violations'] > 0:
        print("  ⚠️ WIP 违规，建议调整限制")
    else:
        print("  ✅ WIP 控制良好")
    
    if efficiency['bottleneck_columns'] == 0:
        print("  ✅ 无明显瓶颈")
    else:
        print(f"  ⚠️ 有 {efficiency['bottleneck_columns']} 个瓶颈列")


def example_9_custom_fields():
    """示例 9: 自定义字段"""
    print("\n" + "=" * 50)
    print("示例 9: 自定义字段")
    print("=" * 50)
    
    board = create_standard_kanban()
    
    # 添加带自定义字段的卡片
    board.add_card(
        "TASK-001",
        "用户认证功能",
        "In Progress",
        priority=1,
        tags=["backend", "security"],
        custom_fields={
            "estimate_hours": 16,
            "assignee": "张三",
            "story_points": 5,
            "epic": "用户系统"
        }
    )
    
    board.add_card(
        "TASK-002",
        "首页设计",
        "To Do",
        tags=["design"],
        custom_fields={
            "estimate_hours": 8,
            "assignee": "李四",
            "story_points": 3
        }
    )
    
    print("卡片详情:")
    for card in board.get_all_cards():
        print(f"\n[{card.id}] {card.title}")
        print(f"  列: {card.column}")
        print(f"  优先级: {card.priority}")
        print(f"  标签: {card.tags}")
        print(f"  自定义字段:")
        for key, value in card.custom_fields.items():
            print(f"    {key}: {value}")


def example_10_board_comparison():
    """示例 10: 看板类型对比"""
    print("\n" + "=" * 50)
    print("示例 10: 看板类型对比")
    print("=" * 50)
    
    # 标准看板
    standard = create_standard_kanban("标准看板")
    print("标准看板 (简单流程):")
    for col in standard.get_columns():
        print(f"  {col.name} (WIP: {col.wip_limit or '无'})")
    
    # Scrum 看板
    scrum = create_scrum_kanban("Scrum 看板")
    print("\nScrum 看板 (完整 Sprint 流程):")
    for col in scrum.get_columns():
        print(f"  {col.name} (WIP: {col.wip_limit or '无'})")
    
    # 自定义看板
    custom = KanbanBoard("自定义看板")
    custom.add_column("需求", wip_limit=5, is_start=True)
    custom.add_column("设计", wip_limit=3)
    custom.add_column("开发", wip_limit=4)
    custom.add_column("测试", wip_limit=2)
    custom.add_column("部署", wip_limit=1)
    custom.add_column("上线", is_end=True)
    
    print("\n自定义看板 (企业级流程):")
    for col in custom.get_columns():
        print(f"  {col.name} (WIP: {col.wip_limit or '无'})")
    
    print("\n适用场景:")
    print("  标准看板: 个人项目、简单任务")
    print("  Scrum 看板: Sprint 开发、团队协作")
    print("  自定义看板: 企业流程、复杂项目")


def run_all_examples():
    """运行所有示例"""
    print("=" * 60)
    print("Kanban Board Utilities 使用示例")
    print("=" * 60)
    
    examples = [
        example_1_create_basic_board,
        example_2_card_operations,
        example_3_wip_management,
        example_4_flow_metrics,
        example_5_bottleneck_detection,
        example_6_cfd_generation,
        example_7_import_export,
        example_8_efficiency_analysis,
        example_9_custom_fields,
        example_10_board_comparison,
    ]
    
    for example in examples:
        example()
    
    print("\n" + "=" * 60)
    print("示例完成!")
    print("=" * 60)


if __name__ == "__main__":
    run_all_examples()