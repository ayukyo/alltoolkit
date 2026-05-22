"""
Habit Chain Utils 使用示例

展示习惯链追踪功能的各种使用场景。
"""

import sys
sys.path.insert(0, '..')

import json
from datetime import date, timedelta

from mod import (
    HabitChain, HabitChainManager, HabitFrequency,
    create_daily_habit, create_weekday_habit, create_weekend_habit,
    create_custom_habit, calculate_streak_milestone, get_chain_health_score
)


def example_basic_usage():
    """基础使用示例"""
    print("=" * 50)
    print("示例1: 基础使用")
    print("=" * 50)
    
    # 创建一个每日习惯
    reading = create_daily_habit("每天阅读30分钟", "#4CAF50")
    
    # 标记今天完成
    reading.complete()
    
    # 标记过去几天完成（模拟连续完成）
    today = date.today()
    for i in range(1, 7):  # 过去6天
        reading.complete(today - timedelta(days=i))
    
    # 获取统计信息
    stats = reading.get_stats()
    print(f"\n习惯: {stats['name']}")
    print(f"当前连续天数: {stats['current_streak']} 天")
    print(f"最长连续天数: {stats['longest_streak']} 天")
    print(f"完成率: {stats['completion_rate'] * 100:.1f}%")
    print(f"最近30天完成率: {stats['last_30_days_rate'] * 100:.1f}%")
    print(f"今天是否完成: {stats['is_completed_today']}")
    
    # 查看里程碑
    milestone = calculate_streak_milestone(stats['current_streak'])
    print(f"\n里程碑进度:")
    if milestone['current_milestone']:
        print(f"  已达成: {milestone['current_milestone']['emoji']} {milestone['current_milestone']['name']}")
    if milestone['next_milestone']:
        print(f"  下一目标: {milestone['next_milestone']['emoji']} {milestone['next_milestone']['name']}")
        print(f"  进度: {milestone['progress_to_next'] * 100:.1f}%")


def example_multiple_habits():
    """管理多个习惯示例"""
    print("\n" + "=" * 50)
    print("示例2: 管理多个习惯")
    print("=" * 50)
    
    manager = HabitChainManager()
    
    # 创建多种类型的习惯
    habits = [
        create_daily_habit("阅读30分钟", "#4CAF50"),
        create_weekday_habit("健身1小时", "#2196F3"),
        create_weekend_habit("整理房间", "#FF9800"),
        create_custom_habit("写日记", {0, 3, 6}, "#9C27B0"),  # 周一、周四、周日
    ]
    
    for habit in habits:
        manager.add_chain(habit)
    
    # 模拟完成情况
    today = date.today()
    
    # 阅读连续14天
    reading = manager.get_chain("阅读30分钟")
    for i in range(14):
        reading.complete(today - timedelta(days=i))
    
    # 健身连续10个工作日
    exercise = manager.get_chain("健身1小时")
    for i in range(20):
        d = today - timedelta(days=i)
        if exercise._should_track(d):
            exercise.complete(d)
    
    # 写日记偶尔完成
    diary = manager.get_chain("写日记")
    diary.complete(today)
    diary.complete(today - timedelta(days=3))
    
    # 获取今日概览
    overview = manager.get_today_overview()
    print(f"\n今日概览 ({overview['date']}):")
    print(f"  总习惯数: {overview['total_habits']}")
    print(f"  今日需追踪: {overview['habits_to_track_today']}")
    print(f"  今日已完成: {overview['completed_today']}")
    print(f"  完成进度: {overview['completion_rate'] * 100:.1f}%")
    
    print("\n各习惯状态:")
    for habit in overview['habits']:
        status = "✅" if habit['completed_today'] else ("⏳" if habit['should_track_today'] else "💤")
        streak = f"连续{habit['current_streak']}天" if habit['current_streak'] > 0 else ""
        print(f"  {status} {habit['name']} {streak}")
    
    # 获取排行榜
    print("\n排行榜 (按当前连续天数):")
    leaderboard = manager.get_leaderboard(by="current_streak")
    for i, entry in enumerate(leaderboard, 1):
        print(f"  {i}. {entry['name']}: {entry['current_streak']} 天连续")
    
    # 激励消息
    print(f"\n激励消息: {manager.get_motivational_message()}")


def example_weekly_progress():
    """周进度追踪示例"""
    print("\n" + "=" * 50)
    print("示例3: 周进度追踪")
    print("=" * 50)
    
    manager = HabitChainManager()
    manager.add_chain(create_daily_habit("阅读", "#4CAF50"))
    manager.add_chain(create_weekday_habit("健身", "#2196F3"))
    
    # 获取本周进度
    overview = manager.get_weekly_overview()
    print(f"\n周概览 ({overview['week_start']} - {overview['week_end']}):")
    
    for name, data in overview['habits'].items():
        progress = data['progress']
        print(f"\n{name}:")
        print(f"  本周完成: {progress['completed']}/{progress['total_tracked_days']} 天")
        print(f"  完成率: {progress['rate'] * 100:.1f}%")
        
        # 显示每日状态
        days_display = []
        for day in progress['days']:
            if not day['should_track']:
                days_display.append("·")  # 不需要追踪
            elif day['completed']:
                days_display.append("✅")
            else:
                days_display.append("❌")
        print(f"  每日状态: {' '.join(days_display)}")


def example_calendar_heatmap():
    """日历热力图示例"""
    print("\n" + "=" * 50)
    print("示例4: 日历热力图")
    print("=" * 50)
    
    chain = create_daily_habit("阅读", "#4CAF50")
    today = date.today()
    
    # 模拟过去一个月的完成情况
    # 连续完成，偶尔中断
    for i in range(30):
        d = today - timedelta(days=i)
        if i not in [5, 12, 20]:  # 模拟几天中断
            chain.complete(d)
    
    # 获取当前月份的热力图
    heatmap = chain.get_calendar_heatmap(today.year, today.month)
    
    print(f"\n{today.year}年{today.month}月习惯追踪热力图:")
    print("周一 周二 周三 周四 周五 周六 周日")
    
    weekdays = ["周一", "周二", "周三", "周四", "周五", "周六", "周日"]
    
    for week in heatmap:
        week_display = []
        for day in week:
            if not day['in_month']:
                week_display.append("  · ")
            elif day['is_future']:
                week_display.append("  ? ")
            elif day['completed']:
                week_display.append(" ██ ")
            else:
                week_display.append(" ░░ ")
        print(" ".join(week_display))
    
    print("\n说明: ██ = 完成, ░░ = 未完成, · = 其他月, ? = 未来")


def example_health_score():
    """健康分数示例"""
    print("\n" + "=" * 50)
    print("示例5: 健康分数")
    print("=" * 50)
    
    # 创建不同状态的习惯
    habits = []
    
    # 高分习惯：连续30天
    excellent = create_daily_habit("冥想", "#9C27B0")
    for i in range(30):
        excellent.complete(date.today() - timedelta(days=i))
    habits.append(("冥想", excellent, "连续30天"))
    
    # 中等习惯：连续7天
    good = create_daily_habit("阅读", "#4CAF50")
    for i in range(7):
        good.complete(date.today() - timedelta(days=i))
    habits.append(("阅读", good, "连续7天"))
    
    # 低分习惯：刚开始
    new = create_daily_habit("跑步", "#FF5722")
    new.complete()
    habits.append(("跑步", new, "刚开始"))
    
    print("\n习惯健康分数:")
    for name, chain, desc in habits:
        score = get_chain_health_score(chain)
        stats = chain.get_stats()
        
        # 根据分数给出评价
        if score >= 80:
            rating = "优秀 🌟"
        elif score >= 60:
            rating = "良好 👍"
        elif score >= 40:
            rating = "一般 📊"
        else:
            rating = "起步 🌱"
        
        print(f"\n{name} ({desc}):")
        print(f"  健康分数: {score:.1f}/100")
        print(f"  评级: {rating}")
        print(f"  当前连续: {stats['current_streak']} 天")
        print(f"  最近30天完成率: {stats['last_30_days_rate'] * 100:.1f}%")
        print(f"  今日完成: {'是' if stats['is_completed_today'] else '否'}")


def example_data_persistence():
    """数据持久化示例"""
    print("\n" + "=" * 50)
    print("示例6: 数据持久化")
    print("=" * 50)
    
    manager = HabitChainManager()
    manager.add_chain(create_daily_habit("阅读", "#4CAF50"))
    manager.add_chain(create_weekday_habit("健身", "#2196F3"))
    
    # 模拟完成
    manager.complete("阅读")
    today = date.today()
    for i in range(7):
        manager.get_chain("阅读").complete(today - timedelta(days=i))
    
    # 导出为JSON
    json_data = manager.to_json()
    print("\n导出的JSON数据:")
    print(json.dumps(json.loads(json_data), indent=2, ensure_ascii=False)[:500] + "...")
    
    # 从JSON恢复
    restored = HabitChainManager.from_json(json_data)
    print(f"\n恢复后的习惯数: {len(restored.get_all_stats())}")
    print(f"阅读当前连续: {restored.get_chain('阅读').get_current_streak()} 天")


def example_motivation_features():
    """激励功能示例"""
    print("\n" + "=" * 50)
    print("示例7: 激励功能")
    print("=" * 50)
    
    manager = HabitChainManager()
    manager.add_chain(create_daily_habit("阅读", "#4CAF50"))
    manager.add_chain(create_daily_habit("冥想", "#9C27B0"))
    
    # 场景1: 全部完成
    manager.complete("阅读")
    manager.complete("冥想")
    print("\n场景: 全部完成")
    print(f"  消息: {manager.get_motivational_message()}")
    
    # 场景2: 有长链需要保护
    reading = manager.get_chain("阅读")
    today = date.today()
    for i in range(15):
        reading.complete(today - timedelta(days=i))
    reading.uncomplete()  # 今天未完成，链可能断裂
    
    manager.uncomplete("冥想")
    print("\n场景: 有长链需要保护")
    print(f"  消息: {manager.get_motivational_message()}")
    
    # 找最佳补链日
    manager.complete("阅读")  # 今天完成
    manager.uncomplete("阅读", today - timedelta(days=3))  # 3天前遗漏
    
    best_day, missing = manager.find_best_chain_day()
    print(f"\n最佳补链日: {best_day}")
    print(f"  该日缺失的习惯: {missing}")


def example_special_habits():
    """特殊习惯示例"""
    print("\n" + "=" * 50)
    print("示例8: 特殊习惯场景")
    print("=" * 50)
    
    # 场景1: 每周只需完成一次的习惯
    weekly = HabitChain("每周运动", HabitFrequency.WEEKLY)
    print("\n每周习惯:")
    print("  特点: 每周只需完成一次，任何天都可以追踪")
    
    # 场景2: 特定日期的习惯
    custom = create_custom_habit("周一三五跑步", {0, 2, 4})
    print("\n自定义习惯 (周一三五):")
    today = date.today()
    weekdays = ["周一", "周二", "周三", "周四", "周五", "周六", "周日"]
    print(f"  今天是{weekdays[today.weekday()]}")
    print(f"  今天需要追踪: {custom._should_track(today)}")
    
    # 场景3: 周末习惯
    weekend = create_weekend_habit("周末休闲")
    print("\n周末习惯:")
    print(f"  特点: 只在周六周日追踪")
    print(f"  今天需要追踪: {weekend._should_track(today)}")


def main():
    """运行所有示例"""
    example_basic_usage()
    example_multiple_habits()
    example_weekly_progress()
    example_calendar_heatmap()
    example_health_score()
    example_data_persistence()
    example_motivation_features()
    example_special_habits()
    
    print("\n" + "=" * 50)
    print("所有示例完成!")
    print("=" * 50)


if __name__ == "__main__":
    main()