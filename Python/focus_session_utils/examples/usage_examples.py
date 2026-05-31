"""
Focus Session Utils - 使用示例
"""

from datetime import datetime, timedelta
from focus_session_utils.mod import (
    FocusSessionManager,
    SessionStatus,
    DistractionCategory,
)


def basic_usage():
    """基础用法：创建并完成一个专注会话"""
    manager = FocusSessionManager(daily_goal_minutes=240)

    # 创建25分钟专注会话
    session = manager.create_session(planned_minutes=25, task_name="写季度报告")

    # 启动计时
    manager.start_session(session)

    # 专注中...（这里简化，实际使用时在另一个线程/进程中计时）
    # 期间发现被打断，微信消息
    manager.log_distraction(session, DistractionCategory.WEIXIN, note="工作群消息")

    # 继续专注...直到结束
    manager.end_session(session)

    print(f"会话: {session.task_name}")
    print(f"完成度: {session.completion_rate:.1f}%")
    print(f"质量评分: {session.quality_score:.1f}")
    print(f"打断次数: {session.distraction_count}")


def pomodoro_example():
    """番茄钟模式：25分钟专注 + 5分钟休息，循环4次"""
    manager = FocusSessionManager(daily_goal_minutes=120)

    for round_num in range(1, 5):
        # 25分钟专注
        session = manager.create_session(25, f"番茄#{round_num}")
        manager.start_session(session)

        # 模拟专注（实际应实时跟踪）
        session.end_time = session.start_time + timedelta(minutes=25)
        session.status = SessionStatus.COMPLETED
        print(f"完成番茄 #{round_num}: 质量 {session.quality_score:.1f}")

    report = manager.get_daily_report()
    print(f"\n今日报告:")
    print(f"  总专注: {report.total_focus_minutes} 分钟")
    print(f"  完成会话: {report.completed_sessions}")
    print(f"  目标完成率: {report.goal_achievement_rate}%")


def pause_resume_workflow():
    """暂停/恢复工作流：模拟接电话打断"""
    manager = FocusSessionManager()

    session = manager.create_session(60, "深度工作")
    manager.start_session(session)

    # 电话来了，暂停
    print("📞 电话来了，暂停专注...")
    d = manager.pause_session(session)
    # 通话中...
    import time; time.sleep(0.1)  # 模拟通话

    # 恢复，记录打断
    manager.resume_session(session, d, DistractionCategory.PHONE_CALL, "客户回访")

    print(f"通话时长: {d.duration_seconds}秒")
    print(f"质量评分: {session.quality_score:.1f}")


def daily_report_example():
    """每日报告示例"""
    manager = FocusSessionManager(daily_goal_minutes=240)

    # 模拟多个会话
    for i in range(3):
        s = manager.create_session(30, f"任务{i+1}")
        manager.start_session(s)
        s.end_time = s.start_time + timedelta(minutes=30)
        s.status = SessionStatus.COMPLETED
        if i == 1:
            s.distractions.append(s.distractions.__class__(
                timestamp=s.start_time + timedelta(minutes=10),
                category=DistractionCategory.WEIXIN,
                duration_seconds=120,
                note="查看消息"
            ))

    report = manager.get_daily_report()
    print(f"日期: {report.date}")
    print(f"总会话: {report.total_sessions}")
    print(f"完成: {report.completed_sessions}, 放弃: {report.abandoned_sessions}")
    print(f"总专注: {report.total_focus_minutes} 分钟")
    print(f"无打断专注: {report.distraction_free_minutes} 分钟")
    print(f"平均质量: {report.avg_quality_score}")
    print(f"目标完成率: {report.goal_achievement_rate}%")
    print(f"最多打断来源: {report.top_distraction_category.value if report.top_distraction_category else '无'}")


def best_hours_analysis():
    """最佳专注时段分析"""
    manager = FocusSessionManager()

    # 模拟过去7天的数据
    from datetime import date
    for day in range(7):
        for hour in [9, 14, 21]:
            s = manager.create_session(30)
            s.start_time = datetime.now().replace(hour=hour, minute=0) - timedelta(days=day)
            s.end_time = s.start_time + timedelta(minutes=30)
            s.status = SessionStatus.COMPLETED

    best = manager.get_best_focus_hours(days_back=7)
    print("最佳专注时段 (小时 -> 平均质量分):")
    for hour, score in best[:3]:
        print(f"  {hour:02d}:00 - 平均质量 {score:.1f}")


def csv_export_example():
    """导出CSV示例"""
    manager = FocusSessionManager()

    for name, mins in [("任务A", 25), ("任务B", 50), ("任务C", 30)]:
        s = manager.create_session(mins, name)
        manager.start_session(s)
        s.end_time = s.start_time + timedelta(minutes=mins)
        s.status = SessionStatus.COMPLETED

    csv_data = manager.export_to_csv()
    print("CSV导出预览:")
    for line in csv_data.split("\n")[:5]:
        print(f"  {line}")


if __name__ == "__main__":
    print("=" * 50)
    print("基础用法")
    print("=" * 50)
    basic_usage()

    print("\n" + "=" * 50)
    print("番茄钟模式")
    print("=" * 50)
    pomodoro_example()

    print("\n" + "=" * 50)
    print("暂停/恢复工作流")
    print("=" * 50)
    pause_resume_workflow()

    print("\n" + "=" * 50)
    print("每日报告")
    print("=" * 50)
    daily_report_example()

    print("\n" + "=" * 50)
    print("最佳专注时段分析")
    print("=" * 50)
    best_hours_analysis()

    print("\n" + "=" * 50)
    print("CSV导出")
    print("=" * 50)
    csv_export_example()
