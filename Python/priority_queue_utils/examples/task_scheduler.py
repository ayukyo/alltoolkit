"""
任务调度器示例

演示 TaskScheduler 的使用：
- 添加任务
- 更新任务优先级
- 取消任务
- 获取任务数据
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mod import TaskScheduler


def simple_task_scheduling():
    """简单任务调度示例"""
    print("=" * 50)
    print("简单任务调度")
    print("=" * 50)
    
    scheduler = TaskScheduler()
    
    # 添加任务
    scheduler.add_task("发邮件", priority=5)
    scheduler.add_task("修复紧急 Bug", priority=1)
    scheduler.add_task("代码审查", priority=3)
    scheduler.add_task("写文档", priority=4)
    scheduler.add_task("会议准备", priority=2)
    
    print("\n任务执行顺序:")
    while scheduler:
        task = scheduler.get_next_task()
        print(f"  执行: {task}")
    
    print()


def task_with_data():
    """带数据的任务调度示例"""
    print("=" * 50)
    print("带附加数据的任务")
    print("=" * 50)
    
    scheduler = TaskScheduler()
    
    # 添加带数据的任务
    scheduler.add_task(
        "发邮件",
        priority=3,
        data={"to": "user@example.com", "subject": "项目更新"}
    )
    scheduler.add_task(
        "修复 Bug",
        priority=1,
        data={"bug_id": "BUG-123", "severity": "critical"}
    )
    scheduler.add_task(
        "代码审查",
        priority=2,
        data={"pr_id": 456, "author": "alice"}
    )
    
    print("\n执行任务（带附加信息）:")
    while scheduler:
        task = scheduler.get_next_task()
        data = scheduler.get_task_data(task)
        print(f"  任务: {task}")
        print(f"    数据: {data}")
    
    print()


def priority_update():
    """动态更新任务优先级示例"""
    print("=" * 50)
    print("动态更新任务优先级")
    print("=" * 50)
    
    scheduler = TaskScheduler()
    
    scheduler.add_task("任务A", priority=3)
    scheduler.add_task("任务B", priority=2)
    scheduler.add_task("任务C", priority=1)
    
    print("\n初始任务队列:")
    print(f"  下一个任务: {scheduler.peek_next_task()}")
    
    # 更新任务 B 的优先级为最高
    print("\n更新 '任务A' 的优先级为 0（最高）:")
    scheduler.update_task_priority("任务A", 0)
    print(f"  下一个任务: {scheduler.peek_next_task()}")
    
    print("\n执行任务:")
    while scheduler:
        print(f"  - {scheduler.get_next_task()}")
    
    print()


def task_cancellation():
    """任务取消示例"""
    print("=" * 50)
    print("任务取消")
    print("=" * 50)
    
    scheduler = TaskScheduler()
    
    scheduler.add_task("任务A", priority=1)
    scheduler.add_task("任务B", priority=2)
    scheduler.add_task("任务C", priority=3)
    
    print(f"\n初始队列大小: {len(scheduler)}")
    
    # 取消任务
    print("取消 '任务B':")
    result = scheduler.cancel_task("任务B")
    print(f"  取消结果: {result}")
    print(f"  当前队列大小: {len(scheduler)}")
    
    print("\n检查任务是否存在:")
    print(f"  '任务A' 存在: {scheduler.has_task('任务A')}")
    print(f"  '任务B' 存在: {scheduler.has_task('任务B')}")
    
    print("\n执行剩余任务:")
    while scheduler:
        print(f"  - {scheduler.get_next_task()}")
    
    print()


def deadline_scheduling():
    """截止时间调度示例"""
    print("=" * 50)
    print("按截止时间调度任务")
    print("=" * 50)
    
    from datetime import datetime, timedelta
    
    scheduler = TaskScheduler()
    
    # 当前时间
    now = datetime.now()
    
    # 添加任务，优先级 = 截止时间距离现在的分钟数（越小越紧急）
    tasks = [
        ("提交报告", now + timedelta(minutes=30)),
        ("回复客户", now + timedelta(minutes=10)),
        ("完成开发", now + timedelta(hours=2)),
        ("会议", now + timedelta(minutes=45)),
        ("代码审查", now + timedelta(minutes=20)),
    ]
    
    for task_name, deadline in tasks:
        minutes = (deadline - now).total_seconds() / 60
        scheduler.add_task(
            task_name,
            priority=minutes,
            data={"deadline": deadline.strftime("%H:%M")}
        )
    
    print("\n任务执行顺序（按截止时间）:")
    while scheduler:
        task = scheduler.get_next_task()
        data = scheduler.get_task_data(task)
        deadline = data["deadline"]
        print(f"  {task} (截止时间: {deadline})")
    
    print()


if __name__ == "__main__":
    simple_task_scheduling()
    task_with_data()
    priority_update()
    task_cancellation()
    deadline_scheduling()