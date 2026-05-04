"""
clock_utils 使用示例
展示世界时钟、秒表、计时器、倒计时等功能
"""

import time
from datetime import datetime, timedelta
from mod import (
    WorldClock, Stopwatch, Timer, TimeFormatter,
    TimeDifference, Countdown, AlarmClock, PomodoroTimer,
    ClockFormat, get_world_time, get_multiple_times,
    create_timer, create_stopwatch, format_duration
)


def demo_world_clock():
    """演示世界时钟功能"""
    print("=" * 50)
    print("🌍 世界时钟演示")
    print("=" * 50)
    
    # 创建不同城市的时钟
    beijing = WorldClock("Beijing")
    tokyo = WorldClock("Tokyo")
    newyork = WorldClock("NewYork")
    london = WorldClock("London")
    
    print(f"\n北京时间: {beijing.get_full_time_str()}")
    print(f"东京时间: {tokyo.get_full_time_str()}")
    print(f"纽约时间: {newyork.get_full_time_str()}")
    print(f"伦敦时间: {london.get_full_time_str()}")
    
    # 获取多城市时间
    print("\n多城市时间:")
    cities = ["Beijing", "Tokyo", "NewYork", "London", "Paris", "Sydney"]
    times = get_multiple_times(cities)
    for city, t in times.items():
        print(f"  {city}: {t}")
    
    # 支持的城市
    print(f"\n支持的城市: {', '.join(WorldClock.list_cities())}")


def demo_stopwatch():
    """演示秒表功能"""
    print("\n" + "=" * 50)
    print("⏱️ 秒表演示")
    print("=" * 50)
    
    sw = Stopwatch()
    
    print("\n开始秒表...")
    sw.start()
    
    for i in range(3):
        time.sleep(0.5)
        lap = sw.lap()
        print(f"  计次 {lap.lap_number}: {format_duration(lap.lap_time)} (累计: {format_duration(lap.total_time)})")
    
    sw.pause()
    print(f"\n暂停 - 当前时间: {sw.elapsed_str}")
    
    time.sleep(0.3)
    print(f"暂停期间时间不变: {sw.elapsed_str}")
    
    sw.start()
    time.sleep(0.5)
    
    print(f"\n最终时间: {sw.elapsed_str}")
    
    # 统计信息
    best = sw.get_best_lap()
    worst = sw.get_worst_lap()
    avg = sw.get_average_lap()
    
    print(f"\n最快计次: 第{best.lap_number}圈 - {format_duration(best.lap_time)}")
    print(f"最慢计次: 第{worst.lap_number}圈 - {format_duration(worst.lap_time)}")
    print(f"平均时间: {format_duration(avg)}")
    
    sw.reset()
    print(f"\n重置后: {sw.elapsed_str}")


def demo_timer():
    """演示计时器功能"""
    print("\n" + "=" * 50)
    print("⏳ 计时器演示")
    print("=" * 50)
    
    # 创建不同的计时器
    t1 = Timer.from_time_parts(seconds=3, name="3秒计时器")
    t2 = Timer.from_minutes(0.1, name="6秒计时器")  # 0.1分钟 = 6秒
    
    print("\n启动计时器...")
    t1.start()
    t2.start()
    
    while not t1.is_completed or not t2.is_completed:
        t1.check()
        t2.check()
        
        bar1 = t1.get_progress_bar(20)
        bar2 = t2.get_progress_bar(20)
        
        print(f"\r  {t1.name}: {bar1} {t1.remaining_str}  |  {t2.name}: {bar2} {t2.remaining_str}", end="")
        time.sleep(0.1)
    
    print("\n\n计时器完成！")
    
    # 进度演示
    print("\n进度条演示:")
    timer = Timer(5, name="演示")
    timer.start()
    
    for _ in range(10):
        timer.check()
        bar = timer.get_progress_bar(30, "█", "░")
        print(f"\r  {timer.name}: {bar} {timer.progress_percent:.1f}%", end="")
        time.sleep(0.5)
    
    print("\n")


def demo_time_formatter():
    """演示时间格式化功能"""
    print("\n" + "=" * 50)
    print("📝 时间格式化演示")
    print("=" * 50)
    
    # 时长格式化
    print("\n时长格式化:")
    durations = [0.5, 30, 90, 3661, 90061]
    for d in durations:
        print(f"  {d}秒 = {format_duration(d)} = {TimeFormatter.humanize_seconds(d)}")
    
    # 相对时间
    print("\n相对时间:")
    deltas = [
        timedelta(seconds=30),
        timedelta(minutes=5),
        timedelta(hours=3),
        timedelta(days=7),
        timedelta(days=60),
        timedelta(days=400),
    ]
    for delta in deltas:
        print(f"  {delta} = {TimeFormatter.format_relative(delta)}")
    
    # 倒计时格式化
    print("\n倒计时格式化:")
    targets = [
        datetime.now() + timedelta(seconds=30),
        datetime.now() + timedelta(minutes=5),
        datetime.now() + timedelta(hours=2, minutes=30),
        datetime.now() + timedelta(days=1, hours=3, minutes=15),
    ]
    for target in targets:
        print(f"  目标: {target.strftime('%H:%M:%S')}")
        print(f"  倒计时: {TimeFormatter.format_countdown(target)}")


def demo_time_difference():
    """演示时区差异计算"""
    print("\n" + "=" * 50)
    print("🌐 时区差异演示")
    print("=" * 50)
    
    # 时区偏移
    print("\n各城市UTC偏移:")
    cities = ["Beijing", "Tokyo", "NewYork", "London", "Sydney"]
    for city in cities:
        offset = TimeDifference.get_timezone_offset(city)
        sign = "+" if offset >= 0 else ""
        print(f"  {city}: UTC{sign}{offset}")
    
    # 城市时差
    print("\n城市时差:")
    pairs = [
        ("Beijing", "Tokyo"),
        ("Beijing", "NewYork"),
        ("London", "NewYork"),
        ("Sydney", "London"),
    ]
    for city1, city2 in pairs:
        diff = TimeDifference.get_time_difference(city1, city2)
        print(f"  {city1} → {city2}: {diff:+.1f}小时")
    
    # 时间转换
    print("\n时间转换:")
    print("  北京20:00 = 东京时间", end=" ")
    h, m = TimeDifference.convert_time("Beijing", "Tokyo", 20, 0)
    print(f"{h:02d}:{m:02d}")
    
    print("  北京09:00 = 纽约时间", end=" ")
    h, m = TimeDifference.convert_time("Beijing", "NewYork", 9, 0)
    print(f"{h:02d}:{m:02d}")


def demo_countdown():
    """演示倒计时功能"""
    print("\n" + "=" * 50)
    print("🎯 倒计时演示")
    print("=" * 50)
    
    # 创建倒计时到未来的时间点
    target1 = datetime.now() + timedelta(seconds=10)
    cd1 = Countdown(target1, "10秒倒计时")
    
    print(f"\n{cd1}")
    print(f"  详细: {cd1.get_formatted()}")
    print(f"  天数: {cd1.days}, 小时: {cd1.hours}, 分钟: {cd1.minutes}, 秒: {cd1.seconds}")
    
    # 到特定日期的倒计时
    year = datetime.now().year + 1
    new_year = Countdown.to_new_year(year)
    print(f"\n{new_year}")
    print(f"  距离{year}年新年还有: {new_year.get_formatted()}")
    
    christmas = Countdown.to_christmas()
    print(f"\n{christmas}")
    print(f"  距离圣诞节还有: {christmas.get_formatted()}")
    
    # 过期倒计时
    expired = Countdown(datetime.now() - timedelta(seconds=1), "已过期")
    print(f"\n{expired}")


def demo_alarm_clock():
    """演示闹钟功能"""
    print("\n" + "=" * 50)
    print("⏰ 闹钟演示")
    print("=" * 50)
    
    alarm = AlarmClock()
    
    # 添加闹钟
    print("\n添加闹钟:")
    alarm.add_alarm("会议", datetime.now() + timedelta(hours=1))
    alarm.add_alarm("午餐", datetime.now() + timedelta(hours=2))
    
    # 从时间添加
    future_hour = (datetime.now().hour + 3) % 24
    alarm.add_alarm_from_time("提醒", future_hour, 30)
    
    print("  已添加的闹钟:")
    for name, target in alarm.list_alarms().items():
        remaining = alarm.get_remaining(name)
        if remaining:
            print(f"    {name}: {target.strftime('%H:%M:%S')} (剩余 {format_duration(remaining.total_seconds())})")
    
    # 测试立即触发的闹钟
    alarm.add_alarm("即时", datetime.now() - timedelta(seconds=1))
    triggered = alarm.check()
    print(f"\n触发的闹钟: {triggered}")
    
    # 贪睡功能
    print("\n贪睡演示:")
    alarm.snooze("即时", minutes=5)
    print("  '即时'闹钟已延后5分钟")
    
    remaining = alarm.get_remaining("即时")
    print(f"  新的剩余时间: {format_duration(remaining.total_seconds())}")


def demo_pomodoro():
    """演示番茄钟功能"""
    print("\n" + "=" * 50)
    print("🍅 番茄钟演示")
    print("=" * 50)
    
    # 创建番茄钟（使用很短的时间便于演示）
    pomo = PomodoroTimer(
        work_minutes=0.05,  # 3秒工作
        short_break_minutes=0.03,  # 1.8秒休息
        long_break_minutes=0.1,  # 6秒长休息
        long_break_after=2  # 每2个工作周期后长休息
    )
    
    print(f"\n初始状态: {pomo}")
    
    for round_num in range(4):
        phase, duration = pomo.start()
        print(f"\n开始第{round_num + 1}轮: {phase} ({duration}秒)")
        
        while True:
            completed = pomo.check()
            print(f"\r  剩余: {pomo.remaining_str}", end="")
            
            if completed:
                print(f"\n  ✓ {completed}完成！")
                break
            
            time.sleep(0.5)
        
        print(f"  累计工作周期: {pomo.session_count}")
    
    print(f"\n最终状态: {pomo}")


def main():
    """主函数"""
    print("╔════════════════════════════════════════════╗")
    print("║        Clock Utils 时钟工具集演示          ║")
    print("╚════════════════════════════════════════════╝")
    
    demo_world_clock()
    demo_stopwatch()
    demo_timer()
    demo_time_formatter()
    demo_time_difference()
    demo_countdown()
    demo_alarm_clock()
    demo_pomodoro()
    
    print("\n" + "=" * 50)
    print("演示完成！")
    print("=" * 50)


if __name__ == "__main__":
    main()