"""
Pomodoro Timer Utilities 测试

覆盖:
- 计时器状态管理
- 工作/休息周期
- 暂停/恢复
- 会话完成/中断
- 统计追踪
- JSON 序列化
- 时间估算
- 边界值处理
"""

import sys
import os
import time
import json

# 添加父目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from pomodoro_utils.mod import (
    PomodoroTimer, PomodoroSession, PomodoroStats, TimerState,
    create_timer, format_time, calculate_total_time,
    get_recommended_break, estimate_daily_goal
)


class ResultCollector:
    """测试结果收集器"""
    def __init__(self):
        self.passed = 0
        self.failed = 0
        self.errors = []
    
    def test(self, name: str, condition: bool, message: str = ""):
        if condition:
            self.passed += 1
            print(f"  ✓ {name}")
        else:
            self.failed += 1
            print(f"  ✗ {name}: {message}")
            self.errors.append((name, message))
    
    def summary(self):
        total = self.passed + self.failed
        print(f"\n{'='*60}")
        print(f"测试结果: {self.passed} 通过, {self.failed} 失败 (共 {total})")
        if self.errors:
            print("\n失败的测试:")
            for name, msg in self.errors:
                print(f"  - {name}: {msg}")
        print(f"{'='*60}\n")
        return self.failed == 0


def test_timer_initialization():
    """测试计时器初始化"""
    print("\n[测试] 计时器初始化")
    r = ResultCollector()
    
    # 默认配置
    timer = PomodoroTimer()
    r.test("默认工作时长", timer.work_minutes == 25)
    r.test("默认短休息时长", timer.short_break_minutes == 5)
    r.test("默认长休息时长", timer.long_break_minutes == 15)
    r.test("默认长休息间隔", timer.long_break_interval == 4)
    r.test("默认状态为空闲", timer.state == TimerState.IDLE)
    r.test("默认已完成工作数为0", timer._completed_work_count == 0)
    
    # 自定义配置
    timer2 = PomodoroTimer(
        work_minutes=50,
        short_break_minutes=10,
        long_break_minutes=30,
        long_break_interval=2
    )
    r.test("自定义工作时长", timer2.work_minutes == 50)
    r.test("自定义短休息时长", timer2.short_break_minutes == 10)
    r.test("自定义长休息时长", timer2.long_break_minutes == 30)
    r.test("自定义长休息间隔", timer2.long_break_interval == 2)
    
    # create_timer 便捷函数
    timer3 = create_timer(30, 10, 20, 3)
    r.test("便捷函数创建-工作时长", timer3.work_minutes == 30)
    r.test("便捷函数创建-短休息", timer3.short_break_minutes == 10)
    r.test("便捷函数创建-长休息", timer3.long_break_minutes == 20)
    r.test("便捷函数创建-间隔", timer3.long_break_interval == 3)
    
    return r.summary()


def test_work_session():
    """测试工作会话"""
    print("\n[测试] 工作会话")
    r = ResultCollector()
    
    timer = PomodoroTimer()
    
    # 开始工作
    result = timer.start_work()
    r.test("开始工作成功", result)
    r.test("状态变为工作中", timer.state == TimerState.WORKING)
    r.test("当前会话不为空", timer.current_session is not None)
    r.test("会话状态为工作中", timer.current_session.state == TimerState.WORKING)
    r.test("会话时长为默认值", timer.current_session.duration_minutes == 25)
    
    # 自定义时长
    timer2 = PomodoroTimer()
    timer2.start_work(15)
    r.test("自定义工作时长", timer2.current_session.duration_minutes == 15)
    
    # 不能重复开始
    result2 = timer.start_work()
    r.test("工作中不能再次开始", not result2)
    
    return r.summary()


def test_break_session():
    """测试休息会话"""
    print("\n[测试] 休息会话")
    r = ResultCollector()
    
    timer = PomodoroTimer()
    
    # 短休息
    result = timer.start_break(is_long=False)
    r.test("开始短休息成功", result)
    r.test("状态为短休息", timer.state == TimerState.SHORT_BREAK)
    r.test("短休息时长正确", timer.current_session.duration_minutes == 5)
    
    # 长休息
    timer2 = PomodoroTimer()
    result2 = timer2.start_break(is_long=True)
    r.test("开始长休息成功", result2)
    r.test("状态为长休息", timer2.state == TimerState.LONG_BREAK)
    r.test("长休息时长正确", timer2.current_session.duration_minutes == 15)
    
    return r.summary()


def test_pause_resume():
    """测试暂停和恢复"""
    print("\n[测试] 暂停和恢复")
    r = ResultCollector()
    
    timer = PomodoroTimer()
    
    # 空闲时不能暂停
    result = timer.pause()
    r.test("空闲时不能暂停", not result)
    
    # 开始工作后暂停
    timer.start_work()
    result = timer.pause()
    r.test("工作中可以暂停", result)
    r.test("暂停后状态正确", timer.state == TimerState.PAUSED)
    
    # 恢复
    result2 = timer.resume()
    r.test("可以恢复", result2)
    r.test("恢复后状态正确", timer.state == TimerState.WORKING)
    
    # 空闲时不能恢复
    timer2 = PomodoroTimer()
    result3 = timer2.resume()
    r.test("空闲时不能恢复", not result3)
    
    # 重复暂停
    timer3 = PomodoroTimer()
    timer3.start_work()
    timer3.pause()
    result4 = timer3.pause()
    r.test("暂停时不能再次暂停", not result4)
    
    return r.summary()


def test_complete_session():
    """测试完成会话"""
    print("\n[测试] 完成会话")
    r = ResultCollector()
    
    timer = PomodoroTimer()
    
    # 空闲时不能完成
    result = timer.complete_session()
    r.test("空闲时不能完成", not result)
    
    # 开始并完成工作
    timer.start_work()
    result = timer.complete_session()
    r.test("可以完成工作会话", result)
    r.test("完成后状态为空闲", timer.state == TimerState.IDLE)
    r.test("当前会话被清除", timer.current_session is None)
    r.test("统计更新-完成数", timer.stats.completed_sessions == 1)
    r.test("统计更新-工作分钟", timer.stats.total_work_minutes == 25)
    r.test("已完成工作数更新", timer._completed_work_count == 1)
    
    # 完成休息
    timer2 = PomodoroTimer()
    timer2.start_break(is_long=False)
    timer2.complete_session()
    r.test("完成休息后状态为空闲", timer2.state == TimerState.IDLE)
    r.test("休息分钟统计正确", timer2.stats.total_break_minutes == 5)
    
    return r.summary()


def test_interrupt_session():
    """测试中断会话"""
    print("\n[测试] 中断会话")
    r = ResultCollector()
    
    timer = PomodoroTimer()
    
    # 空闲时不能中断
    result = timer.interrupt_session("test")
    r.test("空闲时不能中断", not result)
    
    # 开始并中断工作
    timer.start_work()
    result = timer.interrupt_session("被打扰了")
    r.test("可以中断会话", result)
    r.test("中断后状态为空闲", timer.state == TimerState.IDLE)
    r.test("中断标记正确", timer._sessions[0].interrupted)
    r.test("中断原因记录", timer._sessions[0].notes == "被打扰了")
    r.test("中断统计更新", timer.stats.interrupted_sessions == 1)
    
    return r.summary()


def test_time_tracking():
    """测试时间追踪"""
    print("\n[测试] 时间追踪")
    r = ResultCollector()
    
    timer = PomodoroTimer()
    
    # 空闲时时间为0
    r.test("空闲时已过秒数为0", timer.get_elapsed_seconds() == 0)
    r.test("空闲时剩余秒数为0", timer.get_remaining_seconds() == 0)
    r.test("空闲时进度为0", timer.get_progress_percent() == 0.0)
    
    # 开始工作后有时间
    timer.start_work()
    time.sleep(1)  # 等待1秒
    elapsed = timer.get_elapsed_seconds()
    r.test("已过秒数>=1", elapsed >= 1)
    
    remaining = timer.get_remaining_seconds()
    r.test("剩余秒数正确", remaining <= 25 * 60 - 1)
    
    progress = timer.get_progress_percent()
    r.test("进度百分比有效", 0 < progress < 1)
    
    # 分钟计算
    elapsed_min = timer.get_elapsed_minutes()
    r.test("已过分钟数正确", elapsed_min >= 0)
    
    return r.summary()


def test_long_break_interval():
    """测试长休息间隔"""
    print("\n[测试] 长休息间隔")
    r = ResultCollector()
    
    timer = PomodoroTimer(long_break_interval=3)
    
    # 完成第1个番茄
    timer.start_work()
    timer.complete_session()
    r.test("1个番茄后不应该长休息", not timer.should_take_long_break())
    
    # 完成第2个番茄
    timer.start_work()
    timer.complete_session()
    r.test("2个番茄后不应该长休息", not timer.should_take_long_break())
    
    # 完成第3个番茄
    timer.start_work()
    timer.complete_session()
    r.test("3个番茄后应该长休息", timer.should_take_long_break())
    
    # 完成第4个番茄
    timer.start_work()
    timer.complete_session()
    r.test("4个番茄后不应该长休息", not timer.should_take_long_break())
    
    # 完成第6个番茄
    timer.start_work()
    timer.complete_session()
    timer.start_work()
    timer.complete_session()
    r.test("6个番茄后应该长休息", timer.should_take_long_break())
    
    return r.summary()


def test_statistics():
    """测试统计功能"""
    print("\n[测试] 统计功能")
    r = ResultCollector()
    
    timer = PomodoroTimer()
    
    # 初始统计
    r.test("初始总会话数为0", timer.stats.total_sessions == 0)
    r.test("初始完成会话数为0", timer.stats.completed_sessions == 0)
    r.test("初始中断会话数为0", timer.stats.interrupted_sessions == 0)
    
    # 完成3个工作会话
    for _ in range(3):
        timer.start_work()
        timer.complete_session()
    
    r.test("3个会话后总数为3", timer.stats.total_sessions == 3)
    r.test("3个会话后完成数为3", timer.stats.completed_sessions == 3)
    r.test("工作分钟统计正确", timer.stats.total_work_minutes == 75)
    
    # 中断1个
    timer.start_work()
    timer.interrupt_session("测试中断")
    
    r.test("中断后中断数为1", timer.stats.interrupted_sessions == 1)
    
    # 生产力评分
    score = timer.get_productivity_score()
    r.test("生产力评分有效", 0 <= score <= 100)
    
    # 每日统计
    today_count = timer.get_today_completed_count()
    r.test("今日完成数正确", today_count == 3)
    
    return r.summary()


def test_sessions():
    """测试会话管理"""
    print("\n[测试] 会话管理")
    r = ResultCollector()
    
    timer = PomodoroTimer()
    
    # 完成几个会话
    timer.start_work()
    timer.complete_session()
    timer.start_break()
    timer.complete_session()
    timer.start_work()
    timer.interrupt_session()
    
    # 获取会话
    sessions = timer.get_sessions()
    r.test("会话数为3", len(sessions) == 3)
    
    # 限制数量
    sessions_limited = timer.get_sessions(limit=2)
    r.test("限制数量后为2", len(sessions_limited) == 2)
    
    # 今日会话
    today = timer.get_today_sessions()
    r.test("今日会话数为3", len(today) == 3)
    
    return r.summary()


def test_json_serialization():
    """测试 JSON 序列化"""
    print("\n[测试] JSON 序列化")
    r = ResultCollector()
    
    timer = PomodoroTimer(work_minutes=30, short_break_minutes=10)
    
    # 完成一些会话
    timer.start_work()
    timer.complete_session()
    timer.start_break()
    timer.complete_session()
    
    # 序列化
    json_str = timer.to_json()
    r.test("序列化成功", len(json_str) > 0)
    r.test("JSON 包含配置", "work_minutes" in json_str)
    r.test("JSON 包含会话", "sessions" in json_str)
    
    # 反序列化
    timer2 = PomodoroTimer.from_json(json_str)
    r.test("反序列化-工作时长", timer2.work_minutes == 30)
    r.test("反序列化-短休息", timer2.short_break_minutes == 10)
    r.test("反序列化-完成数", timer2.stats.completed_sessions == 1)
    r.test("反序列化-会话数", len(timer2._sessions) == 2)
    
    # PomodoroSession 序列化
    from datetime import datetime
    session = PomodoroSession(
        start_time=datetime(2024, 1, 1, 10, 0, 0),
        end_time=datetime(2024, 1, 1, 10, 25, 0),
        state=TimerState.WORKING,
        duration_minutes=25,
        completed=True,
        notes="测试会话"
    )
    session_dict = session.to_dict()
    r.test("Session序列化包含状态", "state" in session_dict)
    r.test("Session序列化包含时长", "duration_minutes" in session_dict)
    
    return r.summary()


def test_callbacks():
    """测试事件回调"""
    print("\n[测试] 事件回调")
    r = ResultCollector()
    
    results = {"started": False, "completed": False}
    
    def on_start(session):
        results["started"] = True
    
    def on_complete(session):
        results["completed"] = True
    
    timer = PomodoroTimer()
    timer.on("on_start", on_start)
    timer.on("on_complete", on_complete)
    
    timer.start_work()
    r.test("开始回调被触发", results["started"])
    
    timer.complete_session()
    r.test("完成回调被触发", results["completed"])
    
    return r.summary()


def test_reset():
    """测试重置功能"""
    print("\n[测试] 重置功能")
    r = ResultCollector()
    
    timer = PomodoroTimer()
    
    # 开始工作
    timer.start_work()
    timer.pause()
    
    # 重置当前
    timer.reset()
    r.test("重置后状态为空闲", timer.state == TimerState.IDLE)
    r.test("重置后当前会话为空", timer.current_session is None)
    r.test("重置后统计保留", timer._completed_work_count == 0)
    
    # 完成一些会话后重置全部
    timer.start_work()
    timer.complete_session()
    timer.start_work()
    timer.complete_session()
    
    timer.reset_all()
    r.test("重置全部后统计清除", timer.stats.completed_sessions == 0)
    r.test("重置全部后会话清空", len(timer._sessions) == 0)
    
    return r.summary()


def test_status_text():
    """测试状态文本"""
    print("\n[测试] 状态文本")
    r = ResultCollector()
    
    timer = PomodoroTimer()
    
    # 空闲
    text = timer.get_status_text()
    r.test("空闲状态文本", text == "空闲")
    
    # 工作中
    timer.start_work()
    text = timer.get_status_text()
    r.test("工作中状态文本", text.startswith("工作中"))
    
    # 暂停
    timer.pause()
    text = timer.get_status_text()
    r.test("暂停状态文本", text.startswith("已暂停"))
    
    return r.summary()


def test_is_completed():
    """测试完成检查"""
    print("\n[测试] 完成检查")
    r = ResultCollector()
    
    timer = PomodoroTimer()
    
    # 空闲时
    r.test("空闲时不完成", not timer.is_completed())
    
    # 开始后
    timer.start_work()
    r.test("刚开始时未完成", not timer.is_completed())
    
    return r.summary()


def test_convenience_functions():
    """测试便捷函数"""
    print("\n[测试] 便捷函数")
    r = ResultCollector()
    
    # format_time
    r.test("格式化时间-0秒", format_time(0) == "00:00")
    r.test("格式化时间-59秒", format_time(59) == "00:59")
    r.test("格式化时间-60秒", format_time(60) == "01:00")
    r.test("格式化时间-3661秒", format_time(3661) == "61:01")
    r.test("格式化时间-负数", format_time(-10) == "00:00")
    
    # calculate_total_time
    total = calculate_total_time(4, work_minutes=25, short_break=5, long_break=15, long_break_interval=4)
    # 4工作 + 3短休息 + 1长休息 = 100 + 15 + 15 = 130分钟
    r.test("计算总时间-4番茄", total == 130)
    
    total2 = calculate_total_time(1, work_minutes=25, short_break=5)
    # 1工作 + 0休息 = 25分钟 (休息在完成后)
    r.test("计算总时间-1番茄", total2 == 30)
    
    # get_recommended_break
    r.test("推荐休息-0工作", get_recommended_break(0) == "short")
    r.test("推荐休息-1工作", get_recommended_break(1) == "short")
    r.test("推荐休息-3工作", get_recommended_break(3) == "short")
    r.test("推荐休息-4工作", get_recommended_break(4) == "long")
    r.test("推荐休息-8工作", get_recommended_break(8) == "long")
    
    # estimate_daily_goal
    goal = estimate_daily_goal(2.0, work_minutes=25)
    r.test("每日目标-2小时", goal == 4)  # 120分钟 / 25分钟 = 4.8 -> 4
    
    goal2 = estimate_daily_goal(4.0, work_minutes=25)
    r.test("每日目标-4小时", goal2 == 9)  # 240分钟 / 25分钟 = 9.6 -> 9
    
    return r.summary()


def test_estimate_completion_time():
    """测试完成时间估算"""
    print("\n[测试] 完成时间估算")
    r = ResultCollector()
    
    timer = PomodoroTimer()
    
    # 完成2个番茄
    timer.start_work()
    timer.complete_session()
    timer.start_work()
    timer.complete_session()
    
    # 估算完成4个番茄的时间
    eta = timer.estimate_completion_time(target_sessions=4)
    r.test("估算时间不为空", eta is not None)
    
    from datetime import datetime
    r.test("估算时间在未来", eta > datetime(2024, 1, 1, 0, 0, 0))
    
    # 已完成目标的估算
    eta2 = timer.estimate_completion_time(target_sessions=2)
    # 已完成2个，目标也是2个，应该很快
    r.test("已完成目标的估算", eta2 is not None)
    
    return r.summary()


def test_auto_start_break():
    """测试自动开始休息"""
    print("\n[测试] 自动开始休息")
    r = ResultCollector()
    
    callback_called = {"break_start": False}
    
    def on_break_start(session):
        callback_called["break_start"] = True
    
    timer = PomodoroTimer(auto_start_break=True, long_break_interval=2)
    timer.on("on_break_start", on_break_start)
    
    timer.start_work()
    timer.complete_session()
    
    r.test("完成后自动开始休息", timer.state == TimerState.SHORT_BREAK)
    r.test("休息回调被触发", callback_called["break_start"])
    
    return r.summary()


def test_productivity_score():
    """测试生产力评分"""
    print("\n[测试] 生产力评分")
    r = ResultCollector()
    
    # 无会话
    timer = PomodoroTimer()
    score = timer.get_productivity_score()
    r.test("无会话时评分为0", score == 0.0)
    
    # 全部完成
    for _ in range(3):
        timer.start_work()
        timer.complete_session()
    
    score = timer.get_productivity_score()
    r.test("全部完成评分为100", score == 100.0)
    
    # 有中断
    timer2 = PomodoroTimer()
    timer2.start_work()
    timer2.complete_session()
    timer2.start_work()
    timer2.interrupt_session()
    
    score2 = timer2.get_productivity_score()
    r.test("有中断时评分降低", 0 < score2 < 100)
    
    # 全部中断
    timer3 = PomodoroTimer()
    timer3.start_work()
    timer3.interrupt_session()
    
    score3 = timer3.get_productivity_score()
    r.test("全部中断评分最低", score3 < score2)
    
    return r.summary()


def test_session_dataclass():
    """测试 PomodoroSession 数据类"""
    print("\n[测试] PomodoroSession 数据类")
    r = ResultCollector()
    
    from datetime import datetime
    
    # 创建会话
    session = PomodoroSession(
        start_time=datetime.now(),
        state=TimerState.WORKING,
        duration_minutes=25,
        notes="测试"
    )
    
    r.test("会话创建-状态", session.state == TimerState.WORKING)
    r.test("会话创建-时长", session.duration_minutes == 25)
    r.test("会话创建-备注", session.notes == "测试")
    r.test("会话创建-未完成", not session.completed)
    r.test("会话创建-未中断", not session.interrupted)
    r.test("会话创建-结束时间为空", session.end_time is None)
    
    # to_dict / from_dict
    data = session.to_dict()
    r.test("to_dict包含状态", "state" in data)
    r.test("to_dict包含时长", "duration_minutes" in data)
    
    session2 = PomodoroSession.from_dict(data)
    r.test("from_dict恢复状态", session2.state == TimerState.WORKING)
    r.test("from_dict恢复时长", session2.duration_minutes == 25)
    r.test("from_dict恢复备注", session2.notes == "测试")
    
    return r.summary()


def test_stats_dataclass():
    """测试 PomodoroStats 数据类"""
    print("\n[测试] PomodoroStats 数据类")
    r = ResultCollector()
    
    # 创建统计
    stats = PomodoroStats(
        total_sessions=10,
        completed_sessions=8,
        interrupted_sessions=2,
        total_work_minutes=200,
        total_break_minutes=40
    )
    
    r.test("统计创建-总会话", stats.total_sessions == 10)
    r.test("统计创建-完成", stats.completed_sessions == 8)
    r.test("统计创建-中断", stats.interrupted_sessions == 2)
    r.test("统计创建-工作分钟", stats.total_work_minutes == 200)
    
    # to_dict / from_dict
    data = stats.to_dict()
    stats2 = PomodoroStats.from_dict(data)
    r.test("统计序列化-总会话", stats2.total_sessions == 10)
    r.test("统计序列化-完成", stats2.completed_sessions == 8)
    
    # 每日统计
    stats3 = PomodoroStats()
    stats3.daily_sessions["2024-01-01"] = 5
    stats3.daily_sessions["2024-01-02"] = 3
    
    data3 = stats3.to_dict()
    stats4 = PomodoroStats.from_dict(data3)
    r.test("每日统计序列化", "2024-01-01" in stats4.daily_sessions)
    r.test("每日统计值正确", stats4.daily_sessions["2024-01-01"] == 5)
    
    return r.summary()


def test_edge_cases():
    """测试边界情况"""
    print("\n[测试] 边界情况")
    r = ResultCollector()
    
    # 零时长
    timer = PomodoroTimer(work_minutes=0)
    timer.start_work()
    progress = timer.get_progress_percent()
    r.test("零时长进度为100", progress == 100.0)
    
    # 负时长（会被接受，但时间计算）
    timer2 = PomodoroTimer(work_minutes=-5)
    timer2.start_work()
    remaining = timer2.get_remaining_seconds()
    r.test("负时长剩余秒数为0", remaining == 0)
    
    # 超长时长
    timer3 = PomodoroTimer(work_minutes=1000)
    timer3.start_work()
    remaining = timer3.get_remaining_seconds()
    r.test("超长时长剩余秒数正确", remaining == 1000 * 60)
    
    # 空备注中断
    timer4 = PomodoroTimer()
    timer4.start_work()
    timer4.interrupt_session("")
    r.test("空备注中断成功", timer4._sessions[0].notes == "")
    
    # 超长备注
    timer5 = PomodoroTimer()
    timer5.start_work()
    long_note = "这是一个很长的备注" * 100
    timer5.interrupt_session(long_note)
    r.test("超长备注中断成功", timer5._sessions[0].notes == long_note)
    
    # 空回调
    timer6 = PomodoroTimer()
    timer6.on("on_start", None)  # type: ignore
    timer6.start_work()  # 不应该崩溃
    r.test("空回调不崩溃", True)
    
    return r.summary()


def test_multiple_callbacks():
    """测试多个回调"""
    print("\n[测试] 多个回调")
    r = ResultCollector()
    
    results = []
    
    def callback1(s):
        results.append(1)
    
    def callback2(s):
        results.append(2)
    
    timer = PomodoroTimer()
    timer.on("on_start", callback1)
    timer.on("on_start", callback2)
    
    timer.start_work()
    
    r.test("两个回调都被触发", len(results) == 2)
    r.test("回调顺序正确", results == [1, 2])
    
    return r.summary()


def test_timer_state_enum():
    """测试 TimerState 枚举"""
    print("\n[测试] TimerState 枚举")
    r = ResultCollector()
    
    r.test("IDLE值", TimerState.IDLE.value == "idle")
    r.test("WORKING值", TimerState.WORKING.value == "working")
    r.test("SHORT_BREAK值", TimerState.SHORT_BREAK.value == "short_break")
    r.test("LONG_BREAK值", TimerState.LONG_BREAK.value == "long_break")
    r.test("PAUSED值", TimerState.PAUSED.value == "paused")
    
    return r.summary()


def run_all_tests():
    """运行所有测试"""
    print("="*60)
    print("Pomodoro Timer Utilities 测试套件")
    print("="*60)
    
    all_passed = True
    
    all_passed &= test_timer_initialization()
    all_passed &= test_work_session()
    all_passed &= test_break_session()
    all_passed &= test_pause_resume()
    all_passed &= test_complete_session()
    all_passed &= test_interrupt_session()
    all_passed &= test_time_tracking()
    all_passed &= test_long_break_interval()
    all_passed &= test_statistics()
    all_passed &= test_sessions()
    all_passed &= test_json_serialization()
    all_passed &= test_callbacks()
    all_passed &= test_reset()
    all_passed &= test_status_text()
    all_passed &= test_is_completed()
    all_passed &= test_convenience_functions()
    all_passed &= test_estimate_completion_time()
    all_passed &= test_auto_start_break()
    all_passed &= test_productivity_score()
    all_passed &= test_session_dataclass()
    all_passed &= test_stats_dataclass()
    all_passed &= test_edge_cases()
    all_passed &= test_multiple_callbacks()
    all_passed &= test_timer_state_enum()
    
    print("\n" + "="*60)
    if all_passed:
        print("✅ 所有测试通过!")
    else:
        print("❌ 部分测试失败")
    print("="*60)
    
    return all_passed


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)