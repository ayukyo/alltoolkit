"""
习惯追踪工具 - 使用示例

展示习惯追踪工具的各种用法。
"""

from datetime import date, timedelta
import json
import sys
import os

# 添加父目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# 导入习惯追踪模块
from mod import (
    HabitTracker,
    Habit,
    FrequencyType,
    HabitStats,
    HabitUtils,
    create_habit,
    calculate_streak,
    completion_rate,
)


def example_basic_usage():
    """基础用法示例"""
    print("\n=== 基础用法 ===\n")
    
    # 创建追踪器
    tracker = HabitTracker()
    
    # 添加习惯
    tracker.add_habit(
        name="跑步",
        description="每天跑步30分钟",
        frequency=FrequencyType.DAILY,
        target_value=30,
        icon="🏃",
        color="#FF5722",
        tags=["运动", "健康"],
        priority=5,
    )
    
    tracker.add_habit(
        name="阅读",
        description="每天阅读1小时",
        target_value=60,
        icon="📚",
        color="#2196F3",
        tags=["学习", "成长"],
    )
    
    # 完成习惯
    tracker.complete_habit("跑步", value=35, mood=4, note="跑了5公里，感觉很棒！")
    tracker.complete_habit("阅读", value=75)
    
    # 查看今日状态
    print("今日习惯状态:")
    status = tracker.get_today_status()
    for name, info in status.items():
        emoji = "✅" if info['completed'] else "⬜"
        print(f"  {emoji} {name}: {info}")
    
    # 查看统计
    print("\n跑步统计:")
    stats = tracker.get_stats("跑步")
    print(f"  当前连续: {stats.current_streak} 天")
    print(f"  完成天数: {stats.completed_days} 天")


def example_weekly_habits():
    """每周习惯示例"""
    print("\n=== 每周习惯 ===\n")
    
    tracker = HabitTracker()
    
    # 添加每周习惯 - 周一三五执行
    tracker.add_habit(
        name="健身房",
        description="去健身房锻炼",
        frequency=FrequencyType.WEEKLY,
        target_days=[0, 2, 4],  # 周一、周三、周五
        icon="💪",
        color="#E91E63",
    )
    
    # 添加每周习惯 - 仅周末
    tracker.add_habit(
        name="打扫房间",
        description="周末打扫房间",
        frequency=FrequencyType.WEEKLY,
        target_days=[5, 6],  # 周六、周日
        icon="🧹",
        color="#795548",
    )
    
    # 查看今天是否需要执行
    today = date.today()
    print(f"今天({tracker.DAY_NAMES[today.weekday()]})需要执行的习惯:")
    today_habits = tracker.get_today_habits()
    for habit in today_habits:
        print(f"  {habit.icon} {habit.name}")
    
    # 如果需要执行，标记完成
    for habit in today_habits:
        tracker.complete_habit(habit.name)
        print(f"  已标记完成: {habit.name}")


def example_simulate_history():
    """模拟历史数据示例"""
    print("\n=== 模拟历史数据 ===\n")
    
    tracker = HabitTracker()
    tracker.add_habit("跑步", "每天跑步", icon="🏃")
    
    today = date.today()
    
    # 模过去30天的数据（大部分完成，有几天中断）
    for i in range(30):
        d = today - timedelta(days=i)
        # 完成大部分天数，第10-12天中断
        if i not in [10, 11, 12]:
            tracker.complete_habit("跑步", target_date=d)
    
    # 获取统计
    stats = tracker.get_stats("跑步")
    
    print("30天统计报告:")
    print(f"  总天数: {stats.total_days}")
    print(f"  完成天数: {stats.completed_days}")
    print(f"  错过天数: {stats.missed_days}")
    print(f"  完成率: {stats.completion_rate * 100:.1f}%")
    print(f"  当前连续: {stats.current_streak} 天")
    print(f"  最长连续: {stats.longest_streak} 天")
    print(f"  最佳星期: {stats.best_day}")
    print(f"  最差星期: {stats.worst_day}")


def example_weekly_report():
    """周报告示例"""
    print("\n=== 周报告 ===\n")
    
    tracker = HabitTracker()
    tracker.add_habit("早起", "每天早起", icon="🌅")
    
    # 模拟本周数据
    today = date.today()
    week_start = today - timedelta(days=today.weekday())
    
    for i in range(7):
        d = week_start + timedelta(days=i)
        if i < 5:  # 周一到周五完成
            tracker.complete_habit("早起", target_date=d, mood=4)
    
    # 获取周报告
    report = tracker.get_weekly_report("早起")
    
    print(f"周报告 ({report['week_start']} - {report['week_end']}):")
    print("\n每日状态:")
    for day in report['daily_status']:
        emoji = "✅" if day['completed'] else "⬜"
        print(f"  {emoji} {day['day_name']}: {'已完成' if day['completed'] else '未完成'}")
    
    stats = report['stats']
    print(f"\n本周统计:")
    print(f"  完成率: {stats['completion_rate'] * 100:.1f}%")
    print(f"  完成天数: {stats['completed_days']} 天")


def example_monthly_calendar():
    """月度日历示例"""
    print("\n=== 月度日历 ===\n")
    
    tracker = HabitTracker()
    tracker.add_habit("喝水", "每天8杯水", target_value=8, icon="💧")
    
    today = date.today()
    
    # 模拟本月前15天的数据
    for i in range(15):
        d = today - timedelta(days=i)
        tracker.complete_habit("喝水", target_date=d, value=8)
    
    # 获取月度日历
    calendar = tracker.get_monthly_calendar("喝水", today.year, today.month)
    
    print(f"{calendar['year']}年{calendar['month']}月 日历视图:")
    print("\n已完成日期:")
    for day in calendar['calendar'][:20]:  # 显示前20天
        emoji = "✅" if day['completed'] else "⬜"
        if day['is_due']:
            print(f"  {emoji} {day['day_name']} {day['day']}日")


def example_heatmap():
    """热力图示例"""
    print("\n=== 年度热力图 ===\n")
    
    tracker = HabitTracker()
    tracker.add_habit("写代码", "每天写代码", icon="💻")
    
    today = date.today()
    
    # 模拟全年数据（隔天完成）
    for i in range(180):  # 半年数据
        d = today - timedelta(days=i)
        if i % 3 == 0:  # 每3天完成一次
            tracker.complete_habit("写代码", target_date=d)
    
    # 获取热力图
    heatmap = tracker.get_completion_heatmap("写代码")
    
    # 统计热力图数据
    completed_count = sum(1 for v in heatmap['heatmap'].values() if v['completed'])
    total_count = len(heatmap['heatmap'])
    
    print(f"{heatmap['year']}年 热力图统计:")
    print(f"  总记录天数: {total_count}")
    print(f"  完成天数: {completed_count}")
    print(f"  完成率: {completed_count / total_count * 100:.1f}%")
    
    # 显示最近10天的状态
    print("\n最近10天:")
    sorted_dates = sorted(heatmap['heatmap'].keys(), reverse=True)[:10]
    for d in sorted_dates:
        status = heatmap['heatmap'][d]
        emoji = "🟩" if status['completed'] else " "  # 用方块表示
        print(f"  {emoji} {d}")


def example_recommendations():
    """习惯推荐示例"""
    print("\n=== 习惯推荐 ===\n")
    
    tracker = HabitTracker()
    
    # 添加一些习惯
    tracker.add_habit("跑步", "每天跑步", icon="🏃")
    tracker.add_habit("冥想", "每天冥想", icon="🧘")
    tracker.add_habit("阅读", "每天阅读", icon="📚")
    
    # 获取推荐
    recommendations = tracker.recommend_habits()
    
    print("基于你现有习惯，推荐你尝试:")
    for i, rec in enumerate(recommendations, 1):
        tags = ", ".join(rec['tags'])
        print(f"  {i}. {rec['name']} - {rec['description']} [{tags}]")


def example_data_export():
    """数据导出导入示例"""
    print("\n=== 数据导出导入 ===\n")
    
    tracker = HabitTracker()
    
    tracker.add_habit("跑步", "每天跑步", icon="🏃")
    tracker.add_habit("阅读", "每天阅读", icon="📚")
    
    # 完成一些记录
    tracker.complete_habit("跑步", value=30)
    tracker.complete_habit("阅读", value=60)
    
    # 导出数据
    json_data = tracker.export_data()
    
    print("导出的JSON数据 (前500字符):")
    print(json_data[:500])
    print(f"\n总长度: {len(json_data)} 字符")
    
    # 导入到新追踪器
    new_tracker = HabitTracker()
    count = new_tracker.import_data(json_data)
    
    print(f"\n成功导入 {count} 个习惯")
    
    # 验证导入
    for name in new_tracker.habits:
        habit = new_tracker.get_habit(name)
        print(f"  - {habit.icon} {habit.name}")


def example_static_functions():
    """静态函数示例"""
    print("\n=== 静态函数使用 ===\n")
    
    # 直接使用静态函数计算连续天数
    today = date.today()
    
    # 创建模拟完成记录
    completions = {}
    for i in range(10):
        d = today - timedelta(days=i)
        # 第3天中断
        completions[d] = (i != 3)
    
    # 计算连续
    current, longest = calculate_streak(completions)
    print(f"完成记录分析:")
    print(f"  当前连续: {current} 天")
    print(f"  最长连续: {longest} 天")
    
    # 计算完成率
    rate = completion_rate(completions)
    print(f"  完成率: {rate * 100:.1f}%")
    
    # 计算最近5天的完成率
    start = today - timedelta(days=4)
    recent_rate = completion_rate(completions, start_date=start)
    print(f"  最近5天完成率: {recent_rate * 100:.1f}%")


def example_goal_tracking():
    """目标追踪示例"""
    print("\n=== 目标追踪 ===\n")
    
    tracker = HabitTracker()
    
    # 添加带目标的习惯
    tracker.add_habit(
        name="喝水",
        description="每天喝8杯水",
        target_value=8,
        icon="💧",
    )
    
    tracker.add_habit(
        name="步数",
        description="每天走10000步",
        target_value=10000,
        icon="🚶",
    )
    
    # 完成并记录实际值
    tracker.complete_habit("喝水", value=10)  # 今天喝了10杯
    tracker.complete_habit("步数", value=8500)  # 今天走了8500步
    
    # 模过去7天
    today = date.today()
    water_values = [8, 6, 10, 8, 7, 9, 10]  # 每天的喝水数
    step_values = [12000, 8000, 15000, 9000, 7000, 11000, 8500]  # 每天的步数
    
    for i in range(7):
        d = today - timedelta(days=i)
        tracker.complete_habit("喝水", target_date=d, value=water_values[i])
        tracker.complete_habit("步数", target_date=d, value=step_values[i])
    
    # 获取统计
    water_stats = tracker.get_stats("喝水")
    step_stats = tracker.get_stats("步数")
    
    print("喝水统计:")
    print(f"  总杯数: {water_stats.total_value} 杯")
    print(f"  平均: {water_stats.average_value:.1f} 杯/天")
    print(f"  目标: 8 杯/天")
    
    print("\n步数统计:")
    print(f"  总步数: {step_stats.total_value} 步")
    print(f"  平均: {step_stats.average_value:.0f} 步/天")
    print(f"  目标: 10000 步/天")


def example_mood_tracking():
    """心情追踪示例"""
    print("\n=== 心情追踪 ===\n")
    
    tracker = HabitTracker()
    tracker.add_habit("运动", "每天运动", icon="💪")
    
    # 完成并记录心情
    today = date.today()
    moods = [5, 4, 3, 4, 5, 2, 4]  # 1-5分
    
    for i in range(7):
        d = today - timedelta(days=i)
        tracker.complete_habit("运动", target_date=d, mood=moods[i], note=f"第{i+1}天")
    
    stats = tracker.get_stats("运动")
    
    print("心情统计:")
    print(f"  平均心情: {stats.average_mood:.1f} 分")
    print(f"  (1分=很差, 5分=很棒)")
    
    # 分析心情趋势
    habit = tracker.get_habit("运动")
    print("\n心情记录:")
    for d in sorted(habit.completions.keys()):
        comp = habit.completions[d]
        mood_emoji = {1: "😢", 2: "😔", 3: "😐", 4: "😊", 5: "😄"}
        if comp.mood:
            emoji = mood_emoji.get(comp.mood, "😐")
            print(f"  {d}: {emoji} {comp.mood}分")


def example_skip_habit():
    """跳过习惯示例"""
    print("\n=== 跳过习惯 ===\n")
    
    tracker = HabitTracker()
    tracker.add_habit("跑步", "每天跑步", icon="🏃")
    
    today = date.today()
    
    # 正常完成前几天
    for i in range(5):
        d = today - timedelta(days=i + 5)
        tracker.complete_habit("跑步", target_date=d)
    
    # 某天跳过（生病）
    skip_day = today - timedelta(days=2)
    tracker.skip_habit("跑步", target_date=skip_day, note="生病休息")
    
    # 今天完成
    tracker.complete_habit("跑步")
    
    stats = tracker.get_stats("跑步")
    
    print("统计报告:")
    print(f"  完成天数: {stats.completed_days}")
    print(f"  跳过天数: {stats.skipped_days}")
    print(f"  错过天数: {stats.missed_days}")
    
    # 查看跳过的记录
    habit = tracker.get_habit("跑步")
    print(f"\n跳过记录:")
    for d, comp in habit.completions.items():
        if not comp.completed:
            print(f"  {d}: {comp.note}")


def example_full_demo():
    """完整演示"""
    print("\n=== 完整演示 ===\n")
    
    tracker = HabitTracker()
    
    # 1. 添加多种习惯
    habits_data = [
        ("跑步", FrequencyType.DAILY, [], "🏃", "#FF5722"),
        ("健身房", FrequencyType.WEEKLY, [0, 2, 4], "💪", "#E91E63"),
        ("阅读", FrequencyType.DAILY, [], "📚", "#2196F3"),
        ("冥想", FrequencyType.DAILY, [], "🧘", "#9C27B0"),
        ("早起", FrequencyType.DAILY, [], "🌅", "#FFC107"),
    ]
    
    for name, freq, days, icon, color in habits_data:
        tracker.add_habit(
            name=name,
            frequency=freq,
            target_days=days,
            icon=icon,
            color=color,
        )
    
    # 2. 模过去30天的数据
    today = date.today()
    import random
    
    for i in range(30):
        d = today - timedelta(days=i)
        for name, habit in tracker.habits.items():
            if habit.is_due(d):
                # 随机完成率（60-90%）
                if random.random() < 0.85:
                    tracker.complete_habit(name, target_date=d, mood=random.randint(3, 5))
    
    # 3. 显示所有习惯统计
    print("所有习惯统计概览:")
    print("-" * 60)
    
    all_stats = tracker.get_all_stats()
    for name, stats in all_stats.items():
        if stats:
            habit = tracker.get_habit(name)
            completion = f"{stats.completion_rate * 100:.0f}%"
            streak = f"{stats.current_streak}天"
            longest = f"{stats.longest_streak}天"
            print(f"{habit.icon} {name:8} | 完成: {completion:5} | 连续: {streak:4} | 最长: {longest}")
    
    print("-" * 60)
    
    # 4. 今日状态
    print("\n今日待完成:")
    for habit in tracker.get_today_habits():
        status = "✅ 已完成" if habit.is_completed() else "⬜ 待完成"
        print(f"  {habit.icon} {habit.name}: {status}")
    
    # 5. 推荐新习惯
    print("\n推荐新习惯:")
    recs = tracker.recommend_habits()
    for rec in recs[:3]:
        print(f"  💡 {rec['name']}: {rec['description']}")


def main():
    """运行所有示例"""
    print("=" * 60)
    print("习惯追踪工具 - 使用示例")
    print("=" * 60)
    
    example_basic_usage()
    example_weekly_habits()
    example_simulate_history()
    example_weekly_report()
    example_monthly_calendar()
    example_heatmap()
    example_recommendations()
    example_data_export()
    example_static_functions()
    example_goal_tracking()
    example_mood_tracking()
    example_skip_habit()
    example_full_demo()
    
    print("\n" + "=" * 60)
    print("示例演示完成！")
    print("=" * 60)


if __name__ == "__main__":
    main()