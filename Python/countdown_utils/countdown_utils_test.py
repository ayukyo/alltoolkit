"""
Countdown Utils 测试文件
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from mod import (
    Countdown, CountdownError, CountdownTimer,
    create_countdown, countdown_from_delta, multi_countdown,
    format_duration, time_until, next_occurrence, countdown_to_next,
    days_until, hours_until, minutes_until
)
from datetime import datetime, timedelta


def test_countdown_basic():
    """测试基本的倒计时功能"""
    print("测试基本的倒计时功能...")
    
    # 创建一个未来1小时的倒计时
    target = datetime.now() + timedelta(hours=1)
    cd = Countdown(target)
    
    assert not cd.is_expired
    assert cd.total_seconds > 0
    assert cd.total_seconds <= 3600
    
    # 获取组件
    days, hours, minutes, seconds = cd.get_components()
    assert hours >= 0
    assert minutes >= 0
    
    print("✅ 基本倒计时测试通过")


def test_countdown_format():
    """测试格式化输出"""
    print("测试格式化输出...")
    
    target = datetime.now() + timedelta(days=2, hours=3, minutes=30, seconds=45)
    cd = Countdown(target, name="活动")
    
    # 默认格式
    formatted = cd.format()
    assert "天" in formatted or "小时" in formatted
    
    # 紧凑格式
    formatted = cd.format(style="compact")
    assert "d" in formatted or "h" in formatted
    
    # 中文格式
    formatted = cd.format(style="chinese")
    assert "天" in formatted or "小时" in formatted
    
    # 数字格式
    formatted = cd.format(style="digital")
    assert ":" in formatted
    
    # words 格式
    formatted = cd.format(style="words")
    assert "天" in formatted or "小时" in formatted or "分钟" in formatted
    
    # 包含名称
    formatted = cd.format(include_name=True)
    assert "活动" in formatted
    
    print("✅ 格式化输出测试通过")


def test_countdown_progress():
    """测试进度计算"""
    print("测试进度计算...")
    
    # 创建一个从过去开始的倒计时
    start = datetime.now() - timedelta(hours=1)
    target = datetime.now() + timedelta(hours=1)
    cd = Countdown(target, start=start)
    
    # 进度应该大约 0.5
    progress = cd.progress
    assert 0.4 <= progress <= 0.6
    
    # 进度条
    bar = cd.progress_bar()
    assert "[" in bar
    assert "]" in bar
    assert "%" in bar
    
    # 不显示百分比
    bar = cd.progress_bar(show_percent=False)
    assert "%" not in bar
    
    print("✅ 进度计算测试通过")


def test_countdown_expired():
    """测试过期倒计时"""
    print("测试过期倒计时...")
    
    # 创建一个已过期的倒计时（目标在过去）
    try:
        target = datetime.now() - timedelta(hours=1)
        cd = Countdown(target)
        assert False, "应该抛出异常"
    except CountdownError as e:
        assert "目标时间必须晚于开始时间" in str(e)
    
    print("✅ 过期倒计时测试通过")


def test_countdown_parse_datetime():
    """测试日期解析"""
    print("测试日期解析...")
    
    # 多种格式
    formats = [
        "2026-12-31 23:59:59",
        "2026-12-31",
        "2026/12/31 23:59",
        "2026/12/31",
        "2026年12月31日",
    ]
    
    for fmt in formats:
        # 使用未来日期避免过期错误
        future_fmt = fmt.replace("2026", "2027")
        cd = Countdown(future_fmt)
        assert cd.target.year == 2027
    
    print("✅ 日期解析测试通过")


def test_countdown_to_dict():
    """测试序列化"""
    print("测试序列化...")
    
    target = datetime.now() + timedelta(days=1)
    cd = Countdown(target, name="测试")
    
    d = cd.to_dict()
    assert d["name"] == "测试"
    assert "target" in d
    assert "remaining_seconds" in d
    assert "is_expired" in d
    assert "progress" in d
    assert "formatted" in d
    
    print("✅ 序列化测试通过")


def test_create_countdown():
    """测试便捷函数"""
    print("测试 create_countdown 函数...")
    
    target = datetime.now() + timedelta(hours=1)
    cd = create_countdown(target, name="活动")
    
    assert cd.name == "活动"
    assert not cd.is_expired
    
    print("✅ create_countdown 函数测试通过")


def test_countdown_from_delta():
    """测试从时间差创建"""
    print("测试 countdown_from_delta 函数...")
    
    # 使用 timedelta
    cd = countdown_from_delta(timedelta(hours=2), name="2小时后")
    assert cd.name == "2小时后"
    assert cd.total_seconds > 7000  # 约2小时
    
    # 使用秒数
    cd = countdown_from_delta(3600)  # 1小时
    assert cd.total_seconds <= 3600
    
    print("✅ countdown_from_delta 函数测试通过")


def test_multi_countdown():
    """测试批量倒计时"""
    print("测试 multi_countdown 函数...")
    
    targets = [
        (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d"),
        ("周末", (datetime.now() + timedelta(days=2)).strftime("%Y-%m-%d")),
        ("月末", "2027-05-31"),
    ]
    
    results = multi_countdown(targets)
    
    assert len(results) == 3
    
    # 检查排序（按剩余时间）
    for i in range(len(results) - 1):
        assert results[i]["remaining_seconds"] <= results[i+1]["remaining_seconds"]
    
    print("✅ multi_countdown 函数测试通过")


def test_format_duration():
    """测试持续时间格式化"""
    print("测试 format_duration 函数...")
    
    # 默认格式
    formatted = format_duration(3661)  # 1小时1分钟1秒
    assert "1小时" in formatted
    assert "1分钟" in formatted
    assert "1秒" in formatted
    
    # 紧凑格式
    formatted = format_duration(3661, style="compact")
    assert "1h" in formatted
    assert "1m" in formatted
    
    # 数字格式
    formatted = format_duration(3661, style="digital")
    assert "01" in formatted
    
    # 一天
    formatted = format_duration(86400)
    assert "1天" in formatted
    
    # 负数
    formatted = format_duration(-1)
    assert "已结束" in formatted
    
    print("✅ format_duration 函数测试通过")


def test_time_until():
    """测试 time_until 函数"""
    print("测试 time_until 函数...")
    
    # 未来时间
    target = datetime.now() + timedelta(hours=1)
    remaining = time_until(target)
    assert remaining.total_seconds() > 0
    assert remaining.total_seconds() <= 3600
    
    # 过去时间
    target = datetime.now() - timedelta(hours=1)
    remaining = time_until(target)
    assert remaining.total_seconds() < 0
    
    # 字符串格式
    future_str = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
    remaining = time_until(future_str)
    assert remaining.total_seconds() > 0
    
    print("✅ time_until 函数测试通过")


def test_next_occurrence():
    """测试 next_occurrence 函数"""
    print("测试 next_occurrence 函数...")
    
    # 当前时间之后的时间
    now = datetime.now()
    next_time = next_occurrence("23:59", reference=now)
    
    # 应该是今天或明天
    assert next_time >= now
    
    # 当前时间之前的时间（返回明天）
    early_time = next_occurrence("00:01", reference=now)
    if now.hour >= 0 and now.minute >= 1:
        # 如果当前已经过了00:01，返回明天的00:01
        assert early_time.date() > now.date() or early_time > now
    else:
        assert early_time >= now
    
    print("✅ next_occurrence 函数测试通过")


def test_countdown_to_next():
    """测试 countdown_to_next 函数"""
    print("测试 countdown_to_next 函数...")
    
    cd = countdown_to_next("23:59", name="睡觉时间")
    assert cd.name == "睡觉时间"
    assert not cd.is_expired
    
    print("✅ countdown_to_next 函数测试通过")


def test_days_until():
    """测试 days_until 函数"""
    print("测试 days_until 函数...")
    
    # 3天后
    target = datetime.now() + timedelta(days=3)
    days = days_until(target)
    assert days >= 2  # 可能是2或3，取决于具体时间
    
    print("✅ days_until 函数测试通过")


def test_hours_until():
    """测试 hours_until 函数"""
    print("测试 hours_until 函数...")
    
    # 2小时后
    target = datetime.now() + timedelta(hours=2)
    hours = hours_until(target)
    assert hours >= 1
    
    print("✅ hours_until 函数测试通过")


def test_minutes_until():
    """测试 minutes_until 函数"""
    print("测试 minutes_until 函数...")
    
    # 30分钟后
    target = datetime.now() + timedelta(minutes=30)
    minutes = minutes_until(target)
    assert minutes >= 29  # 可能略少于30
    
    print("✅ minutes_until 函数测试通过")


def test_countdown_timer():
    """测试计时器"""
    print("测试计时器...")
    
    import time
    
    timer = CountdownTimer()
    
    # 等待一小段时间
    time.sleep(0.1)
    
    # 检查流逝时间
    elapsed = timer.elapsed()
    assert elapsed.total_seconds() >= 0.1
    
    elapsed_seconds = timer.elapsed_seconds()
    assert elapsed_seconds >= 0.1
    
    # 格式化
    formatted = timer.elapsed_formatted()
    assert "秒" in formatted or "s" in formatted
    
    # 重置
    timer.reset()
    assert timer.elapsed_seconds() < 0.1
    
    print("✅ 计时器测试通过")


def test_countdown_timer_pause_resume():
    """测试计时器暂停和恢复"""
    print("测试计时器暂停和恢复...")
    
    import time
    
    timer = CountdownTimer()
    time.sleep(0.1)
    
    # 暂停
    timer.pause()
    paused_elapsed = timer.elapsed_seconds()
    
    time.sleep(0.1)  # 暂停期间时间流逝
    
    # 检查暂停期间时间没有增加
    after_pause_elapsed = timer.elapsed_seconds()
    assert abs(after_pause_elapsed - paused_elapsed) < 0.05
    
    # 恢复
    timer.resume()
    time.sleep(0.1)
    
    # 检查恢复后时间增加
    resumed_elapsed = timer.elapsed_seconds()
    assert resumed_elapsed > after_pause_elapsed
    
    print("✅ 计时器暂停和恢复测试通过")


def test_countdown_timer_lap():
    """测试计时器圈数"""
    print("测试计时器圈数...")
    
    import time
    
    timer = CountdownTimer()
    time.sleep(0.1)
    
    # 记录一圈
    lap_time = timer.lap()
    assert lap_time.total_seconds() >= 0.1
    
    # 计时器已重置
    assert timer.elapsed_seconds() < 0.1
    
    print("✅ 计时器圈数测试通过")


def test_countdown_repr():
    """测试 repr"""
    print("测试 repr...")
    
    target = datetime.now() + timedelta(hours=1)
    cd = Countdown(target, name="测试")
    
    r = repr(cd)
    assert "Countdown" in r
    assert "测试" in r
    
    print("✅ repr测试通过")


def test_countdown_str():
    """测试 str"""
    print("测试 str...")
    
    target = datetime.now() + timedelta(hours=1)
    cd = Countdown(target)
    
    s = str(cd)
    assert "小时" in s or "分钟" in s or "秒" in s
    
    print("✅ str测试通过")


def test_countdown_edge_cases():
    """测试边界情况"""
    print("测试边界情况...")
    
    # 零秒倒计时（即将过期）
    target = datetime.now() + timedelta(seconds=0.1)
    cd = Countdown(target)
    
    # 短时间格式化
    formatted = cd.format()
    assert "秒" in formatted
    
    print("✅ 边界情况测试通过")


def test_countdown_progress_bar_custom_chars():
    """测试自定义进度条字符"""
    print("测试自定义进度条字符...")
    
    start = datetime.now() - timedelta(hours=1)
    target = datetime.now() + timedelta(hours=1)
    cd = Countdown(target, start=start)
    
    bar = cd.progress_bar(filled_char="#", empty_char="-")
    assert "#" in bar
    assert "-" in bar
    
    bar = cd.progress_bar(width=10)
    assert len(bar.split("[")[1].split("]")[0]) == 10
    
    print("✅ 自定义进度条字符测试通过")


def run_all_tests():
    """运行所有测试"""
    print("=" * 50)
    print("Countdown Utils 测试套件")
    print("=" * 50)
    
    tests = [
        test_countdown_basic,
        test_countdown_format,
        test_countdown_progress,
        test_countdown_expired,
        test_countdown_parse_datetime,
        test_countdown_to_dict,
        test_create_countdown,
        test_countdown_from_delta,
        test_multi_countdown,
        test_format_duration,
        test_time_until,
        test_next_occurrence,
        test_countdown_to_next,
        test_days_until,
        test_hours_until,
        test_minutes_until,
        test_countdown_timer,
        test_countdown_timer_pause_resume,
        test_countdown_timer_lap,
        test_countdown_repr,
        test_countdown_str,
        test_countdown_edge_cases,
        test_countdown_progress_bar_custom_chars,
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            test()
            passed += 1
        except Exception as e:
            print(f"❌ {test.__name__} 失败: {e}")
            failed += 1
    
    print("=" * 50)
    print(f"测试结果: {passed} 通过, {failed} 失败")
    print("=" * 50)
    
    return failed == 0


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)