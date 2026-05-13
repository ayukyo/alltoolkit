"""
模糊时钟工具模块使用示例
展示如何将精确时间转换为人类可读的模糊时间表达
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from datetime import datetime, timedelta
from mod import (
    FuzzyClock,
    fuzzy_time,
    colloquial_time,
    time_range,
    approximate_time,
    relative_time,
)


def demo_basic_usage():
    """基础用法示例"""
    print("=" * 50)
    print("基础用法示例")
    print("=" * 50)
    
    # 使用便捷函数
    print("\n【便捷函数】")
    print(f"3:00 -> {fuzzy_time(hour=3, minute=0)}")
    print(f"3:15 -> {fuzzy_time(hour=3, minute=15)}")
    print(f"3:30 -> {fuzzy_time(hour=3, minute=30)}")
    print(f"3:45 -> {fuzzy_time(hour=3, minute=45)}")
    
    # 使用 datetime 对象
    print("\n【使用 datetime 对象】")
    dt = datetime(2024, 1, 1, 14, 30)
    print(f"{dt.strftime('%H:%M')} -> {fuzzy_time(dt)}")


def demo_languages():
    """多语言支持示例"""
    print("\n" + "=" * 50)
    print("多语言支持示例")
    print("=" * 50)
    
    times = [(3, 0), (3, 15), (3, 30), (3, 45), (10, 5), (10, 55)]
    
    print("\n【中文 vs 英文】")
    for hour, minute in times:
        zh = fuzzy_time(hour=hour, minute=minute, language="zh")
        en = fuzzy_time(hour=hour, minute=minute, language="en")
        print(f"{hour:02d}:{minute:02d} -> 中文: {zh} | 英文: {en}")


def demo_precision_levels():
    """精度级别示例"""
    print("\n" + "=" * 50)
    print("精度级别示例")
    print("=" * 50)
    
    # 创建不同精度的时钟
    exact_clock = FuzzyClock(precision="exact")
    fuzzy_clock = FuzzyClock(precision="fuzzy")
    approx_clock = FuzzyClock(precision="approximate")
    
    times = [(3, 7), (3, 23), (3, 38), (3, 52)]
    
    print("\n【不同精度对比】")
    for hour, minute in times:
        exact = exact_clock.fuzzy_time(hour=hour, minute=minute)
        fuzzy = fuzzy_clock.fuzzy_time(hour=hour, minute=minute)
        approx = approx_clock.fuzzy_time(hour=hour, minute=minute)
        print(f"{hour:02d}:{minute:02d} -> 精确: {exact} | 模糊: {fuzzy} | 近似: {approx}")


def demo_colloquial():
    """口语化时间示例"""
    print("\n" + "=" * 50)
    print("口语化时间示例")
    print("=" * 50)
    
    hours = [3, 6, 8, 10, 12, 13, 15, 18, 20, 23]
    
    print("\n【各时段口语化表达】")
    for hour in hours:
        result = colloquial_time(hour=hour, minute=0)
        print(f"{hour:02d}:00 -> {result}")
    
    # 英文口语化
    print("\n【英文口语化】")
    for hour in [8, 12, 15, 20]:
        result = colloquial_time(hour=hour, minute=0, language="en")
        print(f"{hour:02d}:00 -> {result}")


def demo_time_range():
    """时间范围示例"""
    print("\n" + "=" * 50)
    print("时间范围示例")
    print("=" * 50)
    
    hours = [2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 22]
    
    print("\n【各时段范围描述】")
    for hour in hours:
        result = time_range(hour=hour, minute=0)
        print(f"{hour:02d}:00 -> {result}")
    
    # 英文
    print("\n【英文范围描述】")
    for hour in [6, 12, 15, 20]:
        result = time_range(hour=hour, minute=0, language="en")
        print(f"{hour:02d}:00 -> {result}")


def demo_approximate():
    """近似时间示例"""
    print("\n" + "=" * 50)
    print("近似时间示例")
    print("=" * 50)
    
    minutes = [5, 10, 15, 25, 35, 45, 55]
    
    print("\n【近似时间表达】")
    for minute in minutes:
        result = approximate_time(hour=3, minute=minute)
        print(f"03:{minute:02d} -> {result}")


def demo_relative():
    """相对时间示例"""
    print("\n" + "=" * 50)
    print("相对时间示例")
    print("=" * 50)
    
    now = datetime.now()
    
    print("\n【过去时间】")
    past_times = [
        now - timedelta(seconds=30),
        now - timedelta(minutes=5),
        now - timedelta(minutes=45),
        now - timedelta(hours=3),
        now - timedelta(hours=12),
        now - timedelta(days=2),
        now - timedelta(weeks=1),
    ]
    
    for t in past_times:
        result = relative_time(t)
        print(f"{t.strftime('%Y-%m-%d %H:%M')} -> {result}")
    
    print("\n【未来时间】")
    future_times = [
        now + timedelta(minutes=10),
        now + timedelta(hours=2),
        now + timedelta(days=3),
        now + timedelta(weeks=2),
    ]
    
    for t in future_times:
        result = relative_time(t)
        print(f"{t.strftime('%Y-%m-%d %H:%M')} -> {result}")
    
    print("\n【英文相对时间】")
    for t in [now - timedelta(minutes=30), now + timedelta(hours=2)]:
        result = relative_time(t, language="en")
        print(f"{t.strftime('%Y-%m-%d %H:%M')} -> {result}")


def demo_real_world():
    """实际应用场景示例"""
    print("\n" + "=" * 50)
    print("实际应用场景示例")
    print("=" * 50)
    
    # 场景1: 会议提醒
    meeting_time = datetime(2024, 1, 15, 14, 30)
    print(f"\n【场景1: 会议提醒】")
    print(f"会议时间: {meeting_time.strftime('%Y-%m-%d %H:%M')}")
    print(f"模糊表达: {colloquial_time(meeting_time)}")
    print(f"时间范围: {time_range(meeting_time)}")
    
    # 场景2: 日程安排
    print(f"\n【场景2: 日程安排】")
    schedule = [
        (datetime(2024, 1, 15, 9, 0), "上班"),
        (datetime(2024, 1, 15, 12, 30), "午餐"),
        (datetime(2024, 1, 15, 14, 15), "会议"),
        (datetime(2024, 1, 15, 18, 0), "下班"),
    ]
    for dt, activity in schedule:
        print(f"{activity}: {colloquial_time(dt)} ({time_range(dt)})")
    
    # 场景3: 国际化应用
    print(f"\n【场景3: 国际化应用】")
    event_time = datetime(2024, 1, 15, 15, 45)
    print(f"中文用户: {colloquial_time(event_time, language='zh')}")
    print(f"英文用户: {colloquial_time(event_time, language='en')}")


def demo_class_usage():
    """类实例用法示例"""
    print("\n" + "=" * 50)
    print("类实例用法示例")
    print("=" * 50)
    
    # 创建自定义配置的时钟
    clock = FuzzyClock(language="zh", precision="exact")
    
    print("\n【自定义精确时钟】")
    for minute in [0, 15, 25, 40, 55]:
        result = clock.fuzzy_time(hour=3, minute=minute)
        print(f"03:{minute:02d} -> {result}")
    
    # 切换精度
    clock.precision = "fuzzy"
    print("\n【切换为模糊精度】")
    for minute in [0, 15, 25, 40, 55]:
        result = clock.fuzzy_time(hour=3, minute=minute)
        print(f"03:{minute:02d} -> {result}")


def main():
    """运行所有示例"""
    demo_basic_usage()
    demo_languages()
    demo_precision_levels()
    demo_colloquial()
    demo_time_range()
    demo_approximate()
    demo_relative()
    demo_real_world()
    demo_class_usage()
    
    print("\n" + "=" * 50)
    print("所有示例完成！")
    print("=" * 50)


if __name__ == "__main__":
    main()