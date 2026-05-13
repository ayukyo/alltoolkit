"""
倒计时工具模块使用示例

展示 countdown_utils 的各种使用场景：
- 基本倒计时
- 批量倒计时管理
- 进度条显示
- 计时器功能
- 格式化输出
"""

from datetime import datetime, timedelta
import sys
import os

# 添加父目录到路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from mod import (
    Countdown, 
    create_countdown,
    countdown_from_delta,
    multi_countdown,
    format_duration,
    next_occurrence,
    countdown_to_next,
    CountdownTimer,
    days_until,
    hours_until,
    minutes_until
)


def example_basic_countdown():
    """基本倒计时示例"""
    print("\n" + "=" * 60)
    print("📅 基本倒计时示例")
    print("=" * 60)
    
    # 创建倒计时 - 使用字符串
    cd1 = create_countdown("2026-12-31 23:59:59", name="2026年结束")
    print(f"\n{cd1.format(include_name=True)}")
    
    # 创建倒计时 - 使用datetime
    target = datetime.now() + timedelta(days=7, hours=3, minutes=30)
    cd2 = Countdown(target, name="活动开始")
    print(f"{cd2.format(include_name=True)}")
    
    # 使用时间差创建
    cd3 = countdown_from_delta(timedelta(hours=2, minutes=15), name="限时优惠")
    print(f"{cd3.format(include_name=True)}")


def example_format_styles():
    """格式化输出示例"""
    print("\n" + "=" * 60)
    print("🎨 格式化输出示例")
    print("=" * 60)
    
    target = datetime.now() + timedelta(days=3, hours=5, minutes=30, seconds=45)
    cd = Countdown(target)
    
    print(f"\n默认格式: {cd.format()}")
    print(f"紧凑格式: {cd.format(style='compact')}")
    print(f"中文格式: {cd.format(style='chinese')}")
    print(f"数字格式: {cd.format(style='digital')}")
    print(f"文字格式: {cd.format(style='words')}")
    
    # 不包含秒
    print(f"\n不含秒: {cd.format(include_seconds=False)}")


def example_progress_bar():
    """进度条示例"""
    print("\n" + "=" * 60)
    print("📊 进度条示例")
    print("=" * 60)
    
    # 创建一个从10分钟前开始，到10分钟后的倒计时（当前正好在中间）
    start = datetime.now() - timedelta(minutes=10)
    target = datetime.now() + timedelta(minutes=10)
    cd = Countdown(target, start=start)
    
    print(f"\n默认进度条: {cd.progress_bar()}")
    print(f"自定义字符:  {cd.progress_bar(filled_char='▓', empty_char='░')}")
    print(f"星星样式:    {cd.progress_bar(filled_char='★', empty_char='☆')}")
    print(f"Emoji样式:  {cd.progress_bar(filled_char='🟩', empty_char='⬜')}")
    
    # 不同宽度
    print(f"\n窄进度条: {cd.progress_bar(width=10)}")
    print(f"宽进度条: {cd.progress_bar(width=30)}")


def example_multi_countdown():
    """批量倒计时示例"""
    print("\n" + "=" * 60)
    print("📋 批量倒计时管理")
    print("=" * 60)
    
    # 定义多个倒计时
    targets = [
        ("起床", "07:00"),  # 今天或明天的7点
        ("午饭", "12:00"),
        ("下班", "18:00"),
        ("周末", (datetime.now() + timedelta(days=(5 - datetime.now().weekday()) % 7 or 7)).strftime("%Y-%m-%d")),
        ("月末", "2026-05-31 23:59:59"),
        ("新年", "2027-01-01 00:00:00"),
    ]
    
    # 注意：简单的HH:mm格式需要使用countdown_to_next
    # 这里演示multi_countdown用完整日期时间
    full_targets = [
        ("周末", (datetime.now() + timedelta(days=(5 - datetime.now().weekday()) % 7 or 7)).strftime("%Y-%m-%d")),
        ("月末", "2026-05-31 23:59:59"),
        ("新年", "2027-01-01 00:00:00"),
    ]
    
    results = multi_countdown(full_targets)
    
    print("\n即将到来的事件:")
    print("-" * 50)
    for item in results:
        progress = item['progress'] * 100
        # 简化进度条显示
        bar_width = 15
        filled = int(item['progress'] * bar_width)
        bar = "█" * filled + "░" * (bar_width - filled)
        print(f"{item['name']:8} {item['formatted']:20} [{bar}] {progress:.1f}%")


def example_timer():
    """计时器示例"""
    print("\n" + "=" * 60)
    print("⏱️  计时器示例")
    print("=" * 60)
    
    import time
    
    timer = CountdownTimer()
    
    print("\n开始计时...")
    time.sleep(0.5)
    
    print(f"已用时间: {timer.elapsed_formatted()}")
    time.sleep(0.3)
    
    print(f"再过一会: {timer.elapsed_formatted(style='compact')}")
    
    print("\n暂停计时...")
    timer.pause()
    time.sleep(0.3)
    print(f"暂停期间: {timer.elapsed_formatted()} (应该不变)")
    
    print("\n恢复计时...")
    timer.resume()
    time.sleep(0.2)
    print(f"恢复后: {timer.elapsed_formatted()}")
    
    # 重置
    print("\n重置计时器...")
    timer.reset()
    print(f"重置后: {timer.elapsed_formatted()}")


def example_convenience_functions():
    """便捷函数示例"""
    print("\n" + "=" * 60)
    print("🔧 便捷函数示例")
    print("=" * 60)
    
    future = datetime.now() + timedelta(days=5, hours=3)
    future_str = future.strftime("%Y-%m-%d %H:%M:%S")
    
    print(f"\n目标时间: {future_str}")
    print(f"剩余天数: {days_until(future_str)} 天")
    print(f"剩余小时: {hours_until(future_str)} 小时")
    print(f"剩余分钟: {minutes_until(future_str)} 分钟")


def example_format_duration():
    """持续时间格式化示例"""
    print("\n" + "=" * 60)
    print("⌛ 持续时间格式化示例")
    print("=" * 60)
    
    durations = [
        45,           # 45秒
        180,          # 3分钟
        3661,         # 1小时1分1秒
        86400,        # 1天
        90061,        # 1天1小时1分1秒
    ]
    
    print("\n持续时间格式化:")
    print("-" * 60)
    print(f"{'秒数':>8} | {'默认格式':^20} | {'紧凑格式':^15} | {'数字格式':^12}")
    print("-" * 60)
    
    for secs in durations:
        default = format_duration(secs)
        compact = format_duration(secs, style="compact")
        digital = format_duration(secs, style="digital")
        print(f"{secs:>8} | {default:^20} | {compact:^15} | {digital:^12}")


def example_real_world():
    """实际应用场景"""
    print("\n" + "=" * 60)
    print("🎯 实际应用场景")
    print("=" * 60)
    
    # 场景1: 项目截止日期
    deadline = datetime(2026, 6, 30, 18, 0, 0)
    try:
        project_cd = Countdown(deadline, name="项目截止")
        print(f"\n📅 {project_cd.format(include_name=True, style='default')}")
        print(f"   进度: {project_cd.progress_bar(width=20)}")
    except CountdownError:
        print("\n📅 项目截止日期已过！")
    
    # 场景2: 考试倒计时
    exam_date = datetime(2026, 6, 15, 9, 0, 0)
    try:
        exam_cd = Countdown(exam_date, name="期末考试")
        print(f"\n📚 {exam_cd.format(include_name=True)}")
        print(f"   剩余天数: {days_until(exam_date.strftime('%Y-%m-%d'))} 天")
    except CountdownError:
        print("\n📚 考试已经结束！")
    
    # 场景3: 下班倒计时
    try:
        offwork_cd = countdown_to_next("18:00", name="下班")
        print(f"\n🏃 {offwork_cd.format(include_name=True, style='compact')}")
    except Exception as e:
        print(f"\n🏃 下班时间计算出错: {e}")
    
    # 场景4: 新年倒计时
    new_year = datetime(datetime.now().year + 1, 1, 1, 0, 0, 0)
    new_year_cd = Countdown(new_year, name=f"{new_year.year}年新年")
    print(f"\n🎆 {new_year_cd.format(include_name=True)}")
    
    # 场景5: 生日倒计时
    # 假设生日是6月15日
    birthday_month = 6
    birthday_day = 15
    today = datetime.now()
    birthday_this_year = datetime(today.year, birthday_month, birthday_day)
    birthday = birthday_this_year if birthday_this_year > today else datetime(today.year + 1, birthday_month, birthday_day)
    birthday_cd = Countdown(birthday, name="生日")
    print(f"\n🎂 {birthday_cd.format(include_name=True)}")


def example_data_export():
    """数据导出示例"""
    print("\n" + "=" * 60)
    print("📤 数据导出示例")
    print("=" * 60)
    
    # 导出为字典格式，便于JSON序列化
    target = datetime.now() + timedelta(days=7)
    cd = Countdown(target, name="活动开始")
    
    data = cd.to_dict()
    
    print("\n倒计时数据（字典格式）:")
    for key, value in data.items():
        print(f"  {key}: {value}")


def main():
    """运行所有示例"""
    print("=" * 60)
    print("🎉 倒计时工具模块使用示例")
    print("=" * 60)
    
    example_basic_countdown()
    example_format_styles()
    example_progress_bar()
    example_multi_countdown()
    example_timer()
    example_convenience_functions()
    example_format_duration()
    example_real_world()
    example_data_export()
    
    print("\n" + "=" * 60)
    print("✅ 示例演示完成！")
    print("=" * 60 + "\n")


if __name__ == "__main__":
    main()