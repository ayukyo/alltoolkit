"""
Pomodoro Timer 使用示例

演示番茄钟工具的各种功能：
- 基本使用
- 自定义配置
- 事件回调
- 统计追踪
- JSON 序列化
"""

import sys
import os
import time

# 添加路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from pomodoro_utils.mod import (
    PomodoroTimer, TimerState,
    create_timer, format_time, calculate_total_time,
    get_recommended_break, estimate_daily_goal
)


def example_basic_usage():
    """基本使用示例"""
    print("\n" + "="*60)
    print("示例 1: 基本使用")
    print("="*60)
    
    # 创建番茄钟计时器（使用默认配置）
    timer = PomodoroTimer()
    
    print(f"默认配置:")
    print(f"  - 工作时长: {timer.work_minutes} 分钟")
    print(f"  - 短休息: {timer.short_break_minutes} 分钟")
    print(f"  - 长休息: {timer.long_break_minutes} 分钟")
    print(f"  - 长休息间隔: {timer.long_break_interval} 个番茄")
    
    # 开始工作
    print("\n开始第1个番茄...")
    timer.start_work()
    print(f"状态: {timer.get_status_text()}")
    
    # 模拟工作完成
    timer.complete_session()
    print("第1个番茄完成!")
    print(f"今日完成: {timer.get_today_completed_count()} 个")
    
    # 开始短休息
    print("\n开始短休息...")
    timer.start_break(is_long=False)
    print(f"状态: {timer.get_status_text()}")
    timer.complete_session()
    print("休息完成!")
    
    # 继续第2个番茄
    print("\n开始第2个番茄...")
    timer.start_work()
    timer.complete_session()
    print(f"今日完成: {timer.get_today_completed_count()} 个")


def example_custom_config():
    """自定义配置示例"""
    print("\n" + "="*60)
    print("示例 2: 自定义配置")
    print("="*60)
    
    # 自定义番茄钟配置
    timer = PomodoroTimer(
        work_minutes=50,          # 50分钟工作
        short_break_minutes=10,    # 10分钟短休息
        long_break_minutes=30,     # 30分钟长休息
        long_break_interval=3,     # 每3个番茄后长休息
        auto_start_break=True      # 自动开始休息
    )
    
    print("自定义配置:")
    print(f"  - 工作时长: {timer.work_minutes} 分钟")
    print(f"  - 短休息: {timer.short_break_minutes} 分钟")
    print(f"  - 长休息: {timer.long_break_minutes} 分钟")
    print(f"  - 长休息间隔: {timer.long_break_interval} 个番茄")
    print(f"  - 自动开始休息: {timer.auto_start_break}")
    
    # 使用便捷函数创建
    timer2 = create_timer(30, 10, 20, 2)
    print("\n便捷函数创建:")
    print(f"  - 工作时长: {timer2.work_minutes} 分钟")


def example_callbacks():
    """事件回调示例"""
    print("\n" + "="*60)
    print("示例 3: 事件回调")
    print("="*60)
    
    events_log = []
    
    def log_event(event_name, session):
        events_log.append({
            "event": event_name,
            "state": session.state.value,
            "duration": session.duration_minutes
        })
        print(f"  事件触发: {event_name} ({session.state.value})")
    
    timer = PomodoroTimer()
    
    # 注册回调
    timer.on("on_start", lambda s: log_event("开始工作", s))
    timer.on("on_complete", lambda s: log_event("完成会话", s))
    timer.on("on_interrupt", lambda s: log_event("中断会话", s))
    timer.on("on_break_start", lambda s: log_event("开始休息", s))
    timer.on("on_break_end", lambda s: log_event("结束休息", s))
    
    print("注册的回调: on_start, on_complete, on_interrupt, on_break_start, on_break_end")
    
    # 演示回调触发
    print("\n触发工作开始:")
    timer.start_work()
    timer.complete_session()
    
    print("\n触发休息:")
    timer.start_break()
    timer.complete_session()
    
    print("\n触发中断:")
    timer.start_work()
    timer.interrupt_session("临时有事")
    
    print(f"\n共记录 {len(events_log)} 个事件")


def example_statistics():
    """统计追踪示例"""
    print("\n" + "="*60)
    print("示例 4: 统计追踪")
    print("="*60)
    
    timer = PomodoroTimer()
    
    # 模拟一天的工作
    print("模拟完成6个番茄:")
    for i in range(6):
        timer.start_work()
        timer.complete_session()
        
        # 每完成一个番茄后休息
        is_long = timer.should_take_long_break()
        timer.start_break(is_long)
        timer.complete_session()
        
        print(f"  完成 {i+1} 个番茄, 推荐休息: {'长休息' if is_long else '短休息'}")
    
    # 显示统计
    stats = timer.stats
    print("\n今日统计:")
    print(f"  - 总会话数: {stats.total_sessions}")
    print(f"  - 完成番茄: {stats.completed_sessions}")
    print(f"  - 工作时间: {stats.total_work_minutes} 分钟 ({stats.total_work_minutes/60:.1f} 小时)")
    print(f"  - 休息时间: {stats.total_break_minutes} 分钟")
    print(f"  - 中断次数: {stats.interrupted_sessions}")
    print(f"  - 生产力评分: {timer.get_productivity_score():.1f}/100")
    
    # 显示每日统计
    print("\n每日番茄数:")
    for date, count in stats.daily_sessions.items():
        print(f"  - {date}: {count} 个")


def example_pause_resume():
    """暂停和恢复示例"""
    print("\n" + "="*60)
    print("示例 5: 暂停和恢复")
    print("="*60)
    
    timer = PomodoroTimer(work_minutes=5)  # 使用较短时长便于演示
    
    print("开始5分钟番茄...")
    timer.start_work()
    print(f"状态: {timer.get_status_text()}")
    
    # 暂停
    print("\n暂停计时...")
    timer.pause()
    print(f"状态: {timer.get_status_text()}")
    
    # 模拟暂停期间
    time.sleep(1)
    print("暂停期间... (模拟1秒)")
    
    # 恢复
    print("\n恢复计时...")
    timer.resume()
    print(f"状态: {timer.get_status_text()}")
    
    # 显示时间
    print(f"\n已过时间: {format_time(timer.get_elapsed_seconds())}")
    print(f"剩余时间: {format_time(timer.get_remaining_seconds())}")
    print(f"进度: {timer.get_progress_percent():.1f}%")


def example_json_serialization():
    """JSON 序列化示例"""
    print("\n" + "="*60)
    print("示例 6: JSON 序列化")
    print("="*60)
    
    timer = PomodoroTimer(work_minutes=30)
    
    # 完成一些番茄
    for _ in range(3):
        timer.start_work()
        timer.complete_session()
    
    # 序列化
    json_str = timer.to_json()
    print("序列化结果 (截取前500字符):")
    print(json_str[:500] + "...")
    
    # 反序列化
    timer2 = PomodoroTimer.from_json(json_str)
    print("\n反序列化恢复:")
    print(f"  - 工作时长: {timer2.work_minutes} 分钟")
    print(f"  - 完成番茄: {timer2.stats.completed_sessions} 个")
    print(f"  - 会话历史: {len(timer2._sessions)} 个会话")


def example_time_estimation():
    """时间估算示例"""
    print("\n" + "="*60)
    print("示例 7: 时间估算")
    print("="*60)
    
    # 计算完成目标番茄需要的总时间
    sessions = 8
    total_time = calculate_total_time(
        sessions,
        work_minutes=25,
        short_break=5,
        long_break=15,
        long_break_interval=4
    )
    print(f"完成 {sessions} 个番茄需要的总时间: {total_time} 分钟 ({total_time/60:.1f} 小时)")
    
    # 估算每日目标
    target_hours = 3.0
    goal = estimate_daily_goal(target_hours, work_minutes=25)
    print(f"工作 {target_hours} 小时需要: {goal} 个番茄")
    
    # 获取推荐休息类型
    print("\n推荐休息类型:")
    for work_count in [1, 2, 3, 4, 5, 6, 7, 8]:
        break_type = get_recommended_break(work_count, long_break_interval=4)
        print(f"  完成 {work_count} 个番茄后: {'长休息' if break_type == 'long' else '短休息'}")


def example_session_management():
    """会话管理示例"""
    print("\n" + "="*60)
    print("示例 8: 会话管理")
    print("="*60)
    
    timer = PomodoroTimer()
    
    # 完成几个会话
    timer.start_work()
    timer.complete_session()
    
    timer.start_break()
    timer.complete_session()
    
    timer.start_work()
    timer.interrupt_session("临时打断")
    
    timer.start_work()
    timer.complete_session()
    
    # 获取会话历史
    sessions = timer.get_sessions()
    print(f"会话历史 ({len(sessions)} 个):")
    for i, session in enumerate(sessions):
        status = "完成" if session.completed else ("中断" if session.interrupted else "进行中")
        print(f"  {i+1}. {session.state.value} - {session.duration_minutes}分钟 - {status}")
    
    # 今日会话
    today = timer.get_today_sessions()
    print(f"\n今日会话: {len(today)} 个")
    
    # 限制数量
    recent = timer.get_sessions(limit=2)
    print(f"最近2个会话: {len(recent)} 个")


def example_status_display():
    """状态显示示例"""
    print("\n" + "="*60)
    print("示例 9: 状态显示")
    print("="*60)
    
    timer = PomodoroTimer(work_minutes=5)
    
    states = [
        ("空闲", lambda: None),
        ("工作中", lambda: timer.start_work()),
        ("暂停", lambda: timer.pause()),
        ("恢复后", lambda: timer.resume()),
        ("短休息", lambda: (timer.complete_session(), timer.start_break())),
        ("长休息", lambda: (timer.complete_session(), timer.start_break(is_long=True)))
    ]
    
    # 重置
    timer.reset_all()
    
    print("各种状态下的状态文本:")
    for name, action in states:
        if action():
            pass  # 执行动作
        print(f"  {name}: {timer.get_status_text()}")
        timer.reset()  # 重置以便下一个状态


def example_complete_workflow():
    """完整工作流示例"""
    print("\n" + "="*60)
    print("示例 10: 完整工作流")
    print("="*60)
    
    print("模拟一个番茄钟工作日:")
    
    timer = PomodoroTimer()
    completed_count = 0
    
    while completed_count < 6:
        # 开始工作
        print(f"\n番茄 #{completed_count + 1}: 开始工作 ({timer.work_minutes}分钟)")
        timer.start_work()
        
        # 模拟工作（简化，实际应用中会等待）
        # 这里直接完成
        timer.complete_session()
        completed_count += 1
        print(f"  ✓ 完成! 今日累计: {timer.get_today_completed_count()} 个")
        
        # 决定休息类型
        if timer.should_take_long_break():
            print(f"  🌴 开始长休息 ({timer.long_break_minutes}分钟)")
            timer.start_break(is_long=True)
        else:
            print(f"  ☕ 开始短休息 ({timer.short_break_minutes}分钟)")
            timer.start_break(is_long=False)
        
        timer.complete_session()
        print("  ✓ 休息结束!")
    
    # 最终统计
    print("\n" + "-"*60)
    print("今日工作总结:")
    print(f"  - 完成番茄: {timer.stats.completed_sessions} 个")
    print(f"  - 工作时间: {timer.stats.total_work_minutes} 分钟")
    print(f"  - 休息时间: {timer.stats.total_break_minutes} 分钟")
    print(f"  - 生产力评分: {timer.get_productivity_score():.1f}/100")


def main():
    """运行所有示例"""
    print("="*60)
    print("Pomodoro Timer 使用示例集")
    print("="*60)
    
    example_basic_usage()
    example_custom_config()
    example_callbacks()
    example_statistics()
    example_pause_resume()
    example_json_serialization()
    example_time_estimation()
    example_session_management()
    example_status_display()
    example_complete_workflow()
    
    print("\n" + "="*60)
    print("所有示例运行完成!")
    print("="*60)


if __name__ == "__main__":
    main()